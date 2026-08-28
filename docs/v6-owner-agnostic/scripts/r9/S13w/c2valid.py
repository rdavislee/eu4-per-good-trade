# -*- coding: utf-8 -*-
"""C2: does final.py's calibration reimplementation agree with the shipped operator at baseline?

final.py's calibration loop is a second implementation of DRAIN with three knobs turned: the alpha
exponent (k_exp=2 unclamped), Phase 1's quantile (rho=0.5) and the flow-zero tolerance (3e-4). Until
C2 it also passed UNIT arc costs to Phase 2 -- which is not a knob, it is the degeneracy the whole
tie-break exists to remove. A reimplementation that differs from the shipped operator in a way nobody
declared is not a calibration; it is a second answer.

This checks the claim directly: set the three knobs to their baseline values and the calibration body
must reproduce drain.run_drain edge for edge, on all 30 b-vectors (29 goods + the aggregate).

Usage: python c2valid.py     Exit 1 on any disagreement.
"""
import numpy as np, sys
import drain, flowop
from solver import N, ORDER, NIDX, EDGES_UND, GOODS, PRICES, ROWS, build_sc
from drain import run_drain, phase0, phase1, sweep_priority, compile_dirs
from flowop import mincost_flow, net_per_edge, TIE_COST

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]


def calib_body(b, tol, cost):
    """final.py's loop body, parameterised on the two things C2 touches."""
    core, beta, Plog = phase0(b)
    Sset, info = phase1(core, beta)          # baseline: HHI-adaptive, not the rho quantile
    f, duals, res = mincost_flow(b + 0, np.zeros(N), cost=cost)
    net = net_per_edge(f)
    flow_arc, free = {}, []
    for ei, (u, v) in enumerate(EDGES_UND):
        if abs(net[ei]) > tol:
            flow_arc[ei] = (u, v) if net[ei] > 0 else (v, u)
        else:
            free.append(ei)
    old = drain.ZERO_TOL
    drain.ZERO_TOL = tol
    try:
        o, S2, promo, fb = sweep_priority(core, beta, Sset, flow_arc, free, net, "defasc_beta")
        return set(compile_dirs(core, o, flow_arc, free, Plog, beta))
    finally:
        drain.ZERO_TOL = old


# the 30 b-vectors: 29 live goods, plus the aggregate wealth vector
BV = [(g, S[gi] - C[gi]) for gi, g in GL]
wn = np.zeros(N)
for r in ROWS:
    wn[NIDX[r["node"]]] += r["tax"] + r["prod_income"]
BV.append(("__aggregate__", wn / wn.sum() - np.full(N, 1.0 / N)))

print("=" * 88)
print("C2: calibration body at BASELINE knobs vs drain.run_drain, %d b-vectors" % len(BV))
print("=" * 88)

TOL_BASE = flowop.ZERO_TOL
bad_fixed, bad_unit = [], []
for name, b in BV:
    ref = set(run_drain(b)["directed"])
    got = calib_body(b, TOL_BASE, TIE_COST)
    if got != ref:
        bad_fixed.append((name, len(ref ^ got)))
    # and what the pre-C2 unit-cost call gave, for contrast
    was = calib_body(b, TOL_BASE, None)
    if was != ref:
        bad_unit.append((name, len(ref ^ was)))

print("  with TIE_COST (post-C2) : %d of %d b-vectors disagree with run_drain" % (len(bad_fixed), len(BV)))
for n, d in bad_fixed[:6]:
    print("      %-16s %d edges differ" % (n, d))
print("  with unit costs (pre-C2): %d of %d disagree" % (len(bad_unit), len(BV)))
for n, d in bad_unit[:6]:
    print("      %-16s %d edges differ" % (n, d))
print()
print("RESULT: %d checks, %d failed" % (len(BV), len(bad_fixed)))
sys.exit(1 if bad_fixed else 0)
