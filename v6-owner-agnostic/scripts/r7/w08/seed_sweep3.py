# -*- coding: utf-8 -*-
import collections, io, os, sys, types, math
import numpy as np
HERE = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
sys.path.insert(0, HERE)
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
    if kind == "first":
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

mod_first = build("first", LP_OPTS)
mod_fulldef = build("full", {})

base_first = {k: trial(mod_first, B[k], IDENT) for k in B}
base_fulldef = {k: trial(mod_fulldef, B[k], IDENT) for k in B}

SEEDS = [int(x) for x in sys.argv[1:]]
for sd in SEEDS:
    rng1 = np.random.default_rng(sd)
    moved1 = 0
    for g in GL:
        for _ in range(NPERM):
            e = trial(mod_first, B[g], list(rng1.permutation(N)))
            if e != base_first[g]: moved1 += 1
    rng2 = np.random.default_rng(sd)
    moved2 = 0
    for g in GL:
        for _ in range(NPERM):
            e = trial(mod_fulldef, B[g], list(rng2.permutation(N)))
            if e != base_fulldef[g]: moved2 += 1
    print("seed %-6d first-order=%3d of 290   full-default=%3d of 290" % (sd, moved1, moved2))
