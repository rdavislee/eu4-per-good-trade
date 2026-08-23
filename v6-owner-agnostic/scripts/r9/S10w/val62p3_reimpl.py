# -*- coding: utf-8 -*-
"""val part3: (a) the UNPATCHED v5 reimplementation against drain.py on the identity permutation;
(b) order-invariance of the orientation at several points of the European sweep."""
import collections, io, os, sys, types
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
V5 = os.path.join(HERE, "..", "..", "v5-owner-agnostic", "scripts")
sys.path.insert(0, HERE); os.chdir(HERE)
import pdx
from solver import N, ORDER, NIDX, EDGES_UND, ROWS
from drain import run_drain
from flowop import TIE_EPS, TIE_EPS2, LP_OPTS

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, PN, W)

_src = io.open(os.path.join(V5, "_audit_b_drain.py"), encoding="utf-8").read()
_OLD = 'res = linprog(c=np.ones(len(arcs)), A_eq=AEQ, b_eq=rhs, bounds=(0, None), method="highs")'
_NEW = ("_wv = np.asarray(wealth, dtype=float) if wealth is not None else np.zeros(n)\n"
        "        _sp = (_wv.max() - _wv.min()) or 1.0\n"
        "        _wn = (_wv - _wv.min()) / _sp\n"
        "        import math as _m\n"
        "        _c = np.array([1.0 + %r*(_wn[u]+_wn[v])/2.0 + %r*_m.modf(min(_wn[u],_wn[v])*max(_wn[u],_wn[v])*7919.0)[0] for (u, v, ei, sg) in arcs])\n"
        "        res = linprog(c=_c, A_eq=AEQ, b_eq=rhs, bounds=(0, None), method=\"highs\", options=%r)"
        % (TIE_EPS, TIE_EPS2, LP_OPTS))
def load(patched):
    m = types.ModuleType("abx"); m.__dict__["__name__"] = "abx"
    exec(compile(_src.replace(_OLD, _NEW) if patched else _src, "abx", "exec"), m.__dict__)
    return m

def field(w, a=2.0):
    t = (w / w.max()) ** a
    n = np.zeros(N); np.add.at(n, PN, t)
    return np.full(N, 1.0 / N) - n / n.sum()

def trial(mod, b, perm, nodew):
    inv = {perm[i]: i for i in range(N)}
    names = [None] * N
    for i in range(N): names[perm[i]] = ORDER[i]
    edges = sorted(tuple(sorted((perm[u], perm[v]))) for u, v in EDGES_UND)
    b2 = np.zeros(N); w2 = np.zeros(N)
    for i in range(N): b2[perm[i]] = b[i]; w2[perm[i]] = nodew[i]
    r = mod.drain(names, edges, b2, w2)
    d = r["directed"] if isinstance(r, dict) else r
    back = {(inv[u], inv[v]) for (u, v) in d}
    o = collections.Counter(u for u, _ in back)
    return back, tuple(sorted(ORDER[i] for i in range(N) if o[i] == 0))

BW = field(W)
ship = set(run_drain(BW)["directed"])
ident = list(range(N))
for tag, patched in (("UNPATCHED (old unit-cost Phase 2)", False), ("patched to TIE_COST", True)):
    m = load(patched)
    e, s = trial(m, BW, ident, NODEW)
    print("  %-34s edges disagreeing with drain.py: %3d of %d ; sinks %s"
          % (tag, len(e ^ ship) // 2, len(EDGES_UND), ",".join(s)))

print("\n=== order-invariance across the European sweep (patched instrument, 20 permutations each) ===")
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
EURP = set(int(x) for x in pdx.values(pdx.load(os.path.join(EU4, "map", "continent.txt")).get("europe")))
EM = np.array([r["pid"] in EURP for r in ROWS])
m = load(True)
rng = np.random.default_rng(31337)
for k in (1.000, 1.150, 1.250, 1.300, 1.365, 1.500, 1.705, 1.960, 2.200, 2.500, 2.600):
    w = np.where(EM, W * k, W)
    nw = NODEW   # the shipped TIE_COST is built once from BASE node wealth and never rescaled
    b = field(w)
    ref = set(run_drain(b)["directed"])
    odr = collections.Counter(u for u, _ in ref)
    refs = tuple(sorted(ORDER[i] for i in range(N) if odr[i] == 0))
    e0, s0 = trial(m, b, ident, nw)
    if e0 != ref:
        print("  x%.3f  INSTRUMENT FAILS IDENTITY (%d edges) - skipped" % (k, len(e0 ^ ref)//2)); continue
    moved = 0; sinkmoved = 0
    for _ in range(20):
        p = list(rng.permutation(N))
        e, s = trial(m, b, p, nw)
        moved += (len(e ^ ref) // 2 > 0); sinkmoved += (s != refs)
    print("  x%.3f  sinks %-42s runs moving an edge %2d/20  moving the sink set %2d/20"
          % (k, ",".join(refs), moved, sinkmoved))
