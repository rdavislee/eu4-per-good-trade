# Y143 / spec 2.4 item 1: per-good relabelling sensitivity under the FOUR cost/tolerance
# combinations the document's "84 -> 13 -> 0" sentence implies, including first-order at
# HiGHS's DEFAULT tolerance, which p3_relabel_pergood.py does not measure.
# Same instrument as relabel6.py/p3_relabel_pergood.py: the v5 five-phase reimplementation
# with its Phase-2 objective patched; validated against drain.py on the identity per good.
import collections, io, os, sys, types
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
from scipy.optimize import linprog
from solver import N, ORDER, NIDX, EDGES_UND, ROWS, GOODS, PRICES, build_sc
from drain import run_drain
from flowop import TIE_EPS, TIE_EPS2, LP_OPTS

V5 = os.path.join(HERE, "..", "..", "v5-owner-agnostic", "scripts")
_src = io.open(os.path.join(V5, "_audit_b_drain.py"), encoding="utf-8").read()
_OLD = 'res = linprog(c=np.ones(len(arcs)), A_eq=AEQ, b_eq=rhs, bounds=(0, None), method="highs")'
assert _src.count(_OLD) == 1

def build(kind, opts):
    if kind == "unit":
        expr = "1.0"
    elif kind == "first":
        expr = "1.0 + %r*(_wn[u]+_wn[v])/2.0" % TIE_EPS
    elif kind == "full":
        expr = ("1.0 + %r*(_wn[u]+_wn[v])/2.0 + %r*_m.modf(min(_wn[u],_wn[v])*max(_wn[u],_wn[v])*7919.0)[0]"
                % (TIE_EPS, TIE_EPS2))
    NEW = ("_wv = np.asarray(wealth, dtype=float) if wealth is not None else np.zeros(n)\n"
           "        _sp = (_wv.max() - _wv.min()) or 1.0\n"
           "        _wn = (_wv - _wv.min()) / _sp\n"
           "        import math as _m\n"
           "        _c = np.array([%s for (u, v, ei, sg) in arcs])\n"
           "        res = linprog(c=_c, A_eq=AEQ, b_eq=rhs, bounds=(0, None), method=\"highs\", options=%r)"
           % (expr, opts))
    m = types.ModuleType("abd_%s" % kind); m.__dict__["__name__"] = "abd"
    exec(compile(_src.replace(_OLD, NEW), "abd", "exec"), m.__dict__)
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
t = (W / W.max()) ** 2.0; n = np.zeros(N); np.add.at(n, pn, t)
B["__AGG__"] = np.full(N, 1.0 / N) - n / n.sum()
SHIP = {k: set(run_drain(b)["directed"]) for k, b in B.items()}

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
NPERM = 10
CONFIGS = [("unit cost,       default tol", "unit",  {}),
           ("unit cost,       LP_OPTS    ", "unit",  LP_OPTS),
           ("first-order,     default tol", "first", {}),
           ("first-order,     LP_OPTS    ", "first", LP_OPTS),
           ("full cost,       default tol", "full",  {}),
           ("full cost,       LP_OPTS    ", "full",  LP_OPTS)]
for label, kind, opts in CONFIGS:
    mod = build(kind, opts)
    if kind == "full" and opts == LP_OPTS:
        bad = [k for k in B if trial(mod, B[k], IDENT) != SHIP[k]]
        print("VALIDATION: identity reproduces drain.py on %d of %d b-vectors%s"
              % (len(B) - len(bad), len(B), "" if not bad else "  FAILED on %s" % bad))
        if bad: sys.exit("instrument failed validation")
    rng = np.random.default_rng(20260821)
    base = {k: trial(mod, B[k], IDENT) for k in B}
    moved = total = 0; gm = set()
    for g in GL:
        for _ in range(NPERM):
            if trial(mod, B[g], list(rng.permutation(N))) != base[g]:
                moved += 1; gm.add(g)
            total += 1
    print("%s per-good: %3d of %d runs move, on %2d of %d goods" % (label, moved, total, len(gm), len(GL)))
