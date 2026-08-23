# -*- coding: utf-8 -*-
"""val part3: per-good relabelling sensitivity as a function of (TIE_EPS2, LP tolerance).

Same instrument as val5_relabel_pg.py (the v5 five-phase reimplementation with its Phase-2
objective patched), parameterised so the three stages the document quotes can each be run:
  first-order only + default tolerance   -> document says 84 of 290
  + second-order   + default tolerance   -> document says 13 of 290
  + second-order   + pinned 1e-10        -> document says  0 of 290
Usage: python val62p3_pergood.py <eps2> <lp: default|pinned> [per] [seed]
"""
import collections, io, os, sys, types
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
V5 = os.path.join(HERE, "..", "..", "v5-owner-agnostic", "scripts")
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop, drain
from solver import N, ORDER, NIDX, EDGES_UND, ROWS
from flowop import TIE_EPS, ARCS

EPS2 = float(sys.argv[1]) if len(sys.argv) > 1 else 1e-6
LPMODE = sys.argv[2] if len(sys.argv) > 2 else "pinned"
PER = int(sys.argv[3]) if len(sys.argv) > 3 else 10
SEED = int(sys.argv[4]) if len(sys.argv) > 4 else 606
LP = {"dual_feasibility_tolerance": 1e-10, "primal_feasibility_tolerance": 1e-10} if LPMODE == "pinned" else None
flowop.LP_OPTS = LP

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, PN, W)
WN = (NODEW - NODEW.min()) / (NODEW.max() - NODEW.min())
A1 = np.array([WN[u] for (u, v, e, s) in ARCS])
A2 = np.array([WN[v] for (u, v, e, s) in ARCS])
GEN = np.modf(np.minimum(A1, A2) * np.maximum(A1, A2) * 7919.0)[0]
flowop.TIE_COST = drain.TIE_COST = 1.0 + TIE_EPS * (A1 + A2) / 2.0 + EPS2 * GEN

from val5_pergood import B, GL           # noqa: E402  (imports solver only)
from drain import run_drain              # noqa: E402

_p5 = os.path.join(V5, "_audit_b_drain.py")
_src = io.open(_p5, encoding="utf-8").read()
_OLD = 'res = linprog(c=np.ones(len(arcs)), A_eq=AEQ, b_eq=rhs, bounds=(0, None), method="highs")'
assert _src.count(_OLD) == 1
_NEW = ("_wv = np.asarray(wealth, dtype=float) if wealth is not None else np.zeros(n)\n"
        "        _sp = (_wv.max() - _wv.min()) or 1.0\n"
        "        _wn = (_wv - _wv.min()) / _sp\n"
        "        import math as _m\n"
        "        _c = np.array([1.0 + %r*(_wn[u]+_wn[v])/2.0 + %r*_m.modf(min(_wn[u],_wn[v])*max(_wn[u],_wn[v])*7919.0)[0] for (u, v, ei, sg) in arcs])\n"
        "        res = linprog(c=_c, A_eq=AEQ, b_eq=rhs, bounds=(0, None), method=\"highs\", options=%r)"
        % (TIE_EPS, EPS2, LP))
ab = types.ModuleType("abd5"); ab.__dict__["__name__"] = "abd5"
exec(compile(_src.replace(_OLD, _NEW), "_audit_b_drain[tie]", "exec"), ab.__dict__)

def trial(b, perm):
    inv = {perm[i]: i for i in range(N)}
    names = [None] * N
    for i in range(N): names[perm[i]] = ORDER[i]
    edges = sorted(tuple(sorted((perm[u], perm[v]))) for u, v in EDGES_UND)
    b2 = np.zeros(N); w2 = np.zeros(N)
    for i in range(N):
        b2[perm[i]] = b[i]; w2[perm[i]] = NODEW[i]
    r = ab.drain(names, edges, b2, w2)
    d = r["directed"] if isinstance(r, dict) else r
    back = {(inv[u], inv[v]) for (u, v) in d}
    o = collections.Counter(u for u, _ in back)
    return back, tuple(sorted(ORDER[i] for i in range(N) if o[i] == 0))

ident = list(range(N)); ok = True; SHIP = {}
for gi, g in GL:
    r = run_drain(B[g]); e = set(r["directed"])
    od = collections.Counter(u for u, _ in e)
    s = tuple(sorted(ORDER[i] for i in range(N) if od[i] == 0))
    SHIP[g] = (e, s)
    e0, s0 = trial(B[g], ident)
    if e0 != e or s0 != s:
        ok = False
        print("  IDENTITY MISMATCH %-16s edges agreeing %d/%d" % (g, len(e0 & e), len(e)))
print("config: TIE_EPS2=%g  LP=%s  identity validation: %s" % (EPS2, LPMODE, "PASSED" if ok else "FAILED"))
if not ok: sys.exit("no figure usable")
rng = np.random.default_rng(SEED)
tot = chg = sinkchg = 0; flips = []; bad = []
for gi, g in GL:
    e, s = SHIP[g]
    for _ in range(PER):
        p = list(rng.permutation(N))
        e2, s2 = trial(B[g], p)
        tot += 1; f = len(e2 ^ e) // 2; flips.append(f)
        if f: chg += 1; bad.append(g)
        if s2 != s: sinkchg += 1
print("  runs moving an edge      : %d of %d" % (chg, tot))
print("  runs moving the sink set : %d of %d" % (sinkchg, tot))
print("  offenders                : %s" % collections.Counter(bad).most_common(10))
print("  distinct goods w/ >=1 flip: %d of %d" % (len(set(bad)), len(GL)))
