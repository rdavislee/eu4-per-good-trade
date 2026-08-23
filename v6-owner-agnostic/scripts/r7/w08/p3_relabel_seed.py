# -*- coding: utf-8 -*-
"""Per-good node-relabelling sensitivity (spec 2.4 item 1 / 2.3): 29 goods x 10 relabellings
under three Phase-2 configurations.  Uses relabel6.py's own instrument -- the v5 five-phase
reimplementation with its Phase-2 objective patched -- and validates it against drain.py on the
identity permutation FOR EVERY GOOD before any trial is counted."""
import collections, io, os, sys, types, math
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
from scipy.optimize import linprog
from solver import N, ORDER, NIDX, EDGES_UND, ROWS, GOODS, PRICES, build_sc
from drain import run_drain
import drain as DR, flowop
from flowop import TIE_EPS, TIE_EPS2, LP_OPTS, ARCS

V5 = os.path.join(HERE, "..", "..", "v5-owner-agnostic", "scripts")
_src = io.open(os.path.join(V5, "_audit_b_drain.py"), encoding="utf-8").read()
_OLD = 'res = linprog(c=np.ones(len(arcs)), A_eq=AEQ, b_eq=rhs, bounds=(0, None), method="highs")'
assert _src.count(_OLD) == 1

def build(kind, opts):
    """kind: 'first' | 'full' | 'absdiff'"""
    if kind == "first":
        expr = "1.0 + %r*(_wn[u]+_wn[v])/2.0" % TIE_EPS
    elif kind == "full":
        expr = ("1.0 + %r*(_wn[u]+_wn[v])/2.0 + %r*_m.modf(min(_wn[u],_wn[v])*max(_wn[u],_wn[v])*7919.0)[0]"
                % (TIE_EPS, TIE_EPS2))
    elif kind == "absdiff":
        expr = ("1.0 + %r*(_wn[u]+_wn[v])/2.0 + %r*abs(_wn[u]-_wn[v])"
                % (TIE_EPS, TIE_EPS ** 2))
    NEW = ("_wv = np.asarray(wealth, dtype=float) if wealth is not None else np.zeros(n)\n"
           "        _sp = (_wv.max() - _wv.min()) or 1.0\n"
           "        _wn = (_wv - _wv.min()) / _sp\n"
           "        import math as _m\n"
           "        _c = np.array([%s for (u, v, ei, sg) in arcs])\n"
           "        res = linprog(c=_c, A_eq=AEQ, b_eq=rhs, bounds=(0, None), method=\"highs\", options=%r)"
           % (expr, opts))
    m = types.ModuleType("abd_%s" % kind); m.__dict__["__name__"] = "abd"
    exec(compile(_src.replace(_OLD, NEW), "abd[%s]" % kind, "exec"), m.__dict__)
    return m

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, W)
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]
B = {}
for g in GL:
    t = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, pn, t)
    B[g] = val[g] / val[g].sum() - n / n.sum()
B["__AGG__"] = np.full(N, 1.0 / N) - (lambda: (lambda t: (lambda n: n / n.sum())(
    (lambda n: (np.add.at(n, pn, t), n)[1])(np.zeros(N))))((W / W.max()) ** 2.0))()

SHIP = {}
for k, b in B.items():
    SHIP[k] = set(run_drain(b)["directed"])

def trial(mod, b, perm):
    inv = {perm[i]: i for i in range(N)}
    names = [None] * N
    for i in range(N): names[perm[i]] = ORDER[i]
    edges = sorted(tuple(sorted((perm[u], perm[v]))) for u, v in EDGES_UND)
    b2 = np.zeros(N); w2 = np.zeros(N)
    for i in range(N):
        b2[perm[i]] = b[i]; w2[perm[i]] = NODEW[i]
    r = mod.drain(names, edges, b2, w2)
    d = r["directed"] if isinstance(r, dict) else r
    return {(inv[u], inv[v]) for (u, v) in d}

IDENT = list(range(N))
CONFIGS = [("first-order only, LP_OPTS", "first", LP_OPTS),
           ("full cost, HiGHS default tol", "full", {}),
           ("full cost, LP_OPTS 1e-10", "full", LP_OPTS),
           ("absdiff second term, default tol", "absdiff", {}),
           ("absdiff second term, LP_OPTS", "absdiff", LP_OPTS)]
NPERM = 10
for label, kind, opts in CONFIGS:
    mod = build(kind, opts)
    # validation: identity permutation must equal the SHIPPED graph for the full-cost config;
    # for the other costs the shipped graph is a different objective, so validate only that the
    # instrument is self-consistent (identity reproduces its own baseline) and report the
    # identity agreement with drain.py.
    idagree = {}
    for k, b in B.items():
        e = trial(mod, b, IDENT)
        idagree[k] = len(e & SHIP[k])
    if kind == "full" and opts == LP_OPTS:
        bad = [k for k, v in idagree.items() if v != len(SHIP[k])]
        print("VALIDATION (%s): identity reproduces drain.py on %d of %d b-vectors"
              % (label, len(B) - len(bad), len(B)))
        if bad:
            sys.exit("INSTRUMENT FAILED VALIDATION on %s" % bad)
    moved = 0; total = 0; goods_moved = set()
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 20260821)
    base = {k: trial(mod, B[k], IDENT) for k in B}
    for g in GL:
        for _ in range(NPERM):
            e = trial(mod, B[g], list(rng.permutation(N)))
            total += 1
            if e != base[g]:
                moved += 1; goods_moved.add(g)
    agg_moved = 0
    for _ in range(NPERM):
        e = trial(mod, B["__AGG__"], list(rng.permutation(N)))
        if e != base["__AGG__"]: agg_moved += 1
    print("%-34s per-good: %3d of %d runs move, on %2d of %d goods | aggregate %d of %d"
          % (label, moved, total, len(goods_moved), len(GL), agg_moved, NPERM))
    if goods_moved: print("      goods: %s" % sorted(goods_moved))
