# -*- coding: utf-8 -*-
"""Y153: 40 relabellings on the razed-hangzhou field. Instrument = relabel6.py's
(the v5 five-phase reimplementation with the tie-break objective patched in), validated
against drain.py on the identity permutation for BOTH the baseline and the razed field."""
import collections, io, os, sys, types
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
from scipy.optimize import linprog
from solver import N, ORDER, NIDX, EDGES_UND, ROWS
from drain import run_drain
from flowop import TIE_EPS, TIE_EPS2, LP_OPTS
V5 = os.path.join(HERE, "..", "..", "v5-owner-agnostic", "scripts")
src = io.open(os.path.join(V5, "_audit_b_drain.py"), encoding="utf-8").read()
OLD = 'res = linprog(c=np.ones(len(arcs)), A_eq=AEQ, b_eq=rhs, bounds=(0, None), method="highs")'
NEW = ("_wv = np.asarray(wealth, dtype=float) if wealth is not None else np.zeros(n)\n"
       "        _sp = (_wv.max() - _wv.min()) or 1.0\n"
       "        _wn = (_wv - _wv.min()) / _sp\n"
       "        import math as _m\n"
       "        _c = np.array([1.0 + %r*(_wn[u]+_wn[v])/2.0 + %r*_m.modf(min(_wn[u],_wn[v])*max(_wn[u],_wn[v])*7919.0)[0] for (u, v, ei, sg) in arcs])\n"
       "        res = linprog(c=_c, A_eq=AEQ, b_eq=rhs, bounds=(0, None), method=\"highs\", options=%r)"
       % (TIE_EPS, TIE_EPS2, LP_OPTS))
assert src.count(OLD) == 1
ab = types.ModuleType("abd"); ab.__dict__["__name__"] = "abd"
exec(compile(src.replace(OLD, NEW), "abd", "exec"), ab.__dict__)
W = np.array([r["tax"] + r["prod_income"] for r in ROWS]); pn = np.array([NIDX[r["node"]] for r in ROWS])
def field(w):
    NW = np.zeros(N); np.add.at(NW, pn, w)
    t = (w / w.max()) ** 2.0; n = np.zeros(N); np.add.at(n, pn, t)
    return np.full(N, 1.0 / N) - n / n.sum(), NW
Wr = W.copy()
for i, r in enumerate(ROWS):
    if r["node"] == "hangzhou": Wr[i] = 0.0
def trial(b, nodew, perm):
    inv = {perm[i]: i for i in range(N)}
    names = [None]*N
    for i in range(N): names[perm[i]] = ORDER[i]
    edges = sorted(tuple(sorted((perm[u], perm[v]))) for u, v in EDGES_UND)
    b2 = np.zeros(N); w2 = np.zeros(N)
    for i in range(N): b2[perm[i]] = b[i]; w2[perm[i]] = nodew[i]
    r = ab.drain(names, edges, b2, w2)
    d = r["directed"] if isinstance(r, dict) else r
    back = {(inv[u], inv[v]) for (u, v) in d}
    o = collections.Counter(u for u, _ in back)
    return back, tuple(sorted(ORDER[i] for i in range(N) if o[i] == 0))
for tag, w in (("baseline", W), ("razed hangzhou", Wr)):
    b, nodew = field(w)
    ship = run_drain(b); SE = set(ship["directed"])
    od = collections.Counter(u for u, _ in SE)
    SS = tuple(sorted(ORDER[i] for i in range(N) if od[i] == 0))
    e0, s0 = trial(b, nodew, list(range(N)))
    ok = (s0 == SS) and (len(e0 & SE) == len(SE))
    print("%-15s instrument validation: identity agrees on %d/%d edges, sinks match %s"
          % (tag, len(e0 & SE), len(SE), s0 == SS))
    if not ok: sys.exit("INSTRUMENT FAILED VALIDATION on %s" % tag)
    rng = np.random.default_rng(20260821)
    same = 0; sets = collections.Counter(); hz = 0
    for _ in range(40):
        e, s = trial(b, nodew, list(rng.permutation(N)))
        sets[s] += 1; same += (s == SS); hz += ("hangzhou" in s)
    print("%-15s 40 relabellings: baseline sink set returned %d/40 | hangzhou an end in %d | sets %s"
          % (tag, same, hz, dict(sets)))
