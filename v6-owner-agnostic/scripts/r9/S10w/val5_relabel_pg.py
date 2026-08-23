# -*- coding: utf-8 -*-
"""Per-good node-relabelling experiment (the figure §0 states as "0 of 290 per good").

No shipped script measures this: relabel6.py permutes only the aggregate b_w. The instrument
is the same one relabel6.py uses -- the v5 five-phase reimplementation, with its Phase-2
objective patched to the shipped TIE_COST and the shipped LP options -- and it is validated
against drain.py on the identity permutation FOR EVERY GOOD before any trial is counted.
"""
import collections, io, os, sys, types
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
V5 = os.path.join(HERE, "..", "..", "v5-owner-agnostic", "scripts")
sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, EDGES_UND, ROWS
from drain import run_drain
from flowop import TIE_EPS, TIE_EPS2, LP_OPTS
from val5_pergood import B, GL

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
        % (TIE_EPS, TIE_EPS2, LP_OPTS))
ab = types.ModuleType("abd5"); ab.__dict__["__name__"] = "abd5"
exec(compile(_src.replace(_OLD, _NEW), "_audit_b_drain[tie]", "exec"), ab.__dict__)

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, PN, W)

def trial(b, perm):
    inv = {perm[i]: i for i in range(N)}
    names = [None]*N
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

ident = list(range(N))
ok = True
SHIP = {}
for gi, g in GL:
    r = run_drain(B[g]); e = set(r["directed"])
    od = collections.Counter(u for u, _ in e)
    s = tuple(sorted(ORDER[i] for i in range(N) if od[i] == 0))
    SHIP[g] = (e, s)
    e0, s0 = trial(B[g], ident)
    if e0 != e or s0 != s:
        ok = False
        print("  IDENTITY MISMATCH %-16s edges agreeing %d/%d sink match %s"
              % (g, len(e0 & e), len(e), s0 == s))
print("instrument validation on the identity permutation, per good: %s" % ("PASSED" if ok else "FAILED"))
if not ok:
    sys.exit("no figure from this run is usable")

per = int(sys.argv[1]) if len(sys.argv) > 1 else 10
rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 606)
tot = chg = sinkchg = 0; flips = []; bad = []
for gi, g in GL:
    e, s = SHIP[g]
    for _ in range(per):
        p = list(rng.permutation(N))
        e2, s2 = trial(B[g], p)
        tot += 1; f = len(e2 ^ e)//2; flips.append(f)
        if f: chg += 1; bad.append((g, f))
        if s2 != s: sinkchg += 1
print("per-good relabellings: %d trials (%d goods x %d)" % (tot, len(GL), per))
print("  runs moving an edge      : %d of %d" % (chg, tot))
print("  runs moving the sink set : %d of %d" % (sinkchg, tot))
print("  edges moving             : mean %.2f max %d" % (np.mean(flips), max(flips)))
print("  offenders                : %s" % collections.Counter(x[0] for x in bad).most_common(8))
