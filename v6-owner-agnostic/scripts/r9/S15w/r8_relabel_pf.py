# -*- coding: utf-8 -*-
"""The node-order sensitivity experiment §1.6 and §2.4 quote, as a shipped script.

Two audits found those figures attributed to scripts that do not contain them: the 580/580 per-good
sweep and the arc-permutation result lived only in an auditor's scratch files. This is the experiment,
in the tree, so the attribution is real and the numbers can be regenerated.

Two warnings, both learned the hard way and both one-sided:

  * `drain.py`'s `sweep_priority(..., pid=...)` hook re-keys ONLY the sweep. Phase 1, the stall
    promotion and Phase 2's LP still read the true index, so a test built on it reports NO effect.
  * A partial reimplementation reports whatever its omission implies, and none of it is trustworthy:
    dropping Phase 4's free-edge orientation leaves 18 sinks on the identity permutation, dropping
    Phase 2 leaves 1, and dropping Phase 1 leaves the shipped 2 with no flips at all -- so a wrong
    instrument can look stable as easily as chaotic. Validate on the identity before trusting a
    trial.
  * `solver.EDGES_UND` is a SORTED set, so a genuine relabelling must re-sort the arc list. Permuting
    only the LP's rows changes nothing.

So the instrument is validated against drain.py on the identity permutation before any trial runs,
and the run aborts if that fails.

Usage: python relabel6.py [n_per_seed] [seed ...]
"""
import collections, io, os, sys, types
import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
V5 = os.path.join(HERE, "..", "..", "v5-owner-agnostic", "scripts")
sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, EDGES_UND, ROWS
from drain import run_drain
from flowop import TIE_EPS, TIE_EPS2, LP_OPTS

# The reimplementation is a v5 file, so its Phase 2 still minimises unit arc cost. The shipped
# solver now breaks Phase 2's ties inside the objective (flowop.TIE_COST), so the two disagree
# unless the instrument carries the same objective. Patch exactly the one line that sets it, from
# the `wealth` argument the function already receives -- everything else stays byte-identical, and
# the identity-permutation check below is what proves the patch landed.
_p5 = os.path.join(V5, "_audit_b_drain.py")
if not os.path.exists(_p5):
    sys.exit("the five-phase reimplementation is missing; cannot run this experiment safely")
_src = io.open(_p5, encoding="utf-8").read()
_OLD = 'res = linprog(c=np.ones(len(arcs)), A_eq=AEQ, b_eq=rhs, bounds=(0, None), method="highs")'
if _src.count(_OLD) != 1:
    sys.exit("cannot locate the reimplementation's Phase-2 objective; refusing to guess")
_NEW = ("_wv = np.asarray(wealth, dtype=float) if wealth is not None else np.zeros(n)" + chr(10) +
        "        _sp = (_wv.max() - _wv.min()) or 1.0" + chr(10) +
        "        _wn = (_wv - _wv.min()) / _sp" + chr(10) +
        "        import math as _m" + chr(10) +
        "        _c = np.array([1.0 + %r*(_wn[u]+_wn[v])/2.0 + %r*_m.modf(min(_wn[u],_wn[v])*max(_wn[u],_wn[v])*7919.0)[0] for (u, v, ei, sg) in arcs])" % (TIE_EPS, TIE_EPS2)
        + chr(10) +
        '        res = linprog(c=_c, A_eq=AEQ, b_eq=rhs, bounds=(0, None), method="highs", options=' + repr(LP_OPTS) + ')')
ab = types.ModuleType("abd"); ab.__dict__["__name__"] = "abd"
exec(compile(_src.replace(_OLD, _NEW), "_audit_b_drain[tie-break]", "exec"), ab.__dict__)

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, W)
t = (W / W.max()) ** 2.0        # spec 2.3 alpha_Phi
num = np.zeros(N); np.add.at(num, pn, t)
BW = np.full(N, 1.0 / N) - num / num.sum()

shipped = run_drain(BW)
SHIP_E = set(shipped["directed"])
_od = collections.Counter(u for u, _ in SHIP_E)
SHIP_S = tuple(sorted(ORDER[i] for i in range(N) if _od[i] == 0))

def trial(perm):
    inv = {perm[i]: i for i in range(N)}
    names = [None] * N
    for i in range(N): names[perm[i]] = ORDER[i]
    edges = sorted(tuple(sorted((perm[u], perm[v]))) for u, v in EDGES_UND)   # re-sorted
    b2 = np.zeros(N); w2 = np.zeros(N)
    for i in range(N):
        b2[perm[i]] = BW[i]; w2[perm[i]] = NODEW[i]
    r = ab.drain(names, edges, b2, w2)
    d = r["directed"] if isinstance(r, dict) else r
    back = {(inv[u], inv[v]) for (u, v) in d}
    o = collections.Counter(u for u, _ in back)
    # the LP objective: total flow on the support, which is what min-cost b-flow minimises with
    # unit arc costs. The spec cites a deviation across relabellings, so it must be computed here.
    obj = None
    if isinstance(r, dict):
        fa = r.get("flow_arc") or r.get("flow") or {}
        try: obj = float(sum(abs(v) for v in fa.values()))
        except Exception: obj = None
    return back, tuple(sorted(ORDER[i] for i in range(N) if o[i] == 0)), r, obj

e0, s0, r0, obj0 = trial(list(range(N)))
ok = (s0 == SHIP_S) and (len(e0 & SHIP_E) == len(SHIP_E))
print("instrument validation on the identity permutation")
print("  edges agreeing with drain.py : %d of %d" % (len(e0 & SHIP_E), len(SHIP_E)))
print("  sink set matches             : %s" % (s0 == SHIP_S))
if not ok:
    sys.exit("INSTRUMENT FAILED VALIDATION - no figure from this run is usable")
print("  validated.\n")

# The degeneracy claim -- same optimal cost, different vertex -- is about Phase 2's LP, so it is
# measured by solving that LP directly under each permutation rather than inferred from the sweep.
def lp_objective(perm, tie):
    """Solve Phase 2 under a permutation. tie=False is the unit cost the shipped solver used to
    minimise -- the degeneracy that motivated the change. tie=True is the cost it minimises now."""
    arcs = []
    for (u, v) in sorted(tuple(sorted((perm[a], perm[b]))) for a, b in EDGES_UND):
        arcs.append((u, v)); arcs.append((v, u))
    A = np.zeros((N, len(arcs)))
    for k, (u, v) in enumerate(arcs):
        A[u, k] -= 1.0; A[v, k] += 1.0
    b2 = np.zeros(N); wn = np.zeros(N)
    _sp = (NODEW.max() - NODEW.min()) or 1.0
    for i in range(N):
        b2[perm[i]] = BW[i]; wn[perm[i]] = (NODEW[i] - NODEW.min()) / _sp
    c = (np.array([1.0 + TIE_EPS * (wn[u] + wn[v]) / 2.0 +
                   TIE_EPS2 * __import__("math").modf(min(wn[u], wn[v]) * max(wn[u], wn[v]) * 7919.0)[0]
                   for (u, v) in arcs]) if tie
         else np.ones(len(arcs)))
    r = linprog(c=c, A_eq=A, b_eq=b2, bounds=(0, None), method="highs", options=LP_OPTS)
    if not r.success: return None, None
    inv = {perm[i]: i for i in range(N)}
    return float(r.fun), frozenset((inv[u], inv[v]) for k, (u, v) in enumerate(arcs) if r.x[k] > 1e-9)

print("Phase 2 under relabelling: the degeneracy, and whether the tie-break removes it")
for _tie in (False, True):
    _o0, _s0 = lp_objective(list(range(N)), _tie)
    _rng = np.random.default_rng(20260821)
    _dev = []; _diff = 0; _n = 40
    for _ in range(_n):
        _o, _sup = lp_objective(list(_rng.permutation(N)), _tie)
        if _o is None: continue
        _dev.append(abs(_o - _o0) / max(1e-300, abs(_o0)))
        _diff += (_sup != _s0)
    print("  %-22s objective %.12f  max rel deviation %.3e" %
          ("tie-break cost" if _tie else "unit cost (former)", _o0, max(_dev)))
    print("  %-22s permutations returning a DIFFERENT optimal support: %d of %d" %
          ("", _diff, len(_dev)))
print()

per = int(sys.argv[1]) if len(sys.argv) > 1 else 100
seeds = [int(a) for a in sys.argv[2:]] or [4242, 7, 999, 20250821]
tot = chg = base = 0
hz = collections.Counter(); holders = collections.Counter(); counts = collections.Counter()
flips = []; per_seed = {}; objs = []
_PF = []
for sd in seeds:
    rng = np.random.default_rng(sd); s_hz = s_ec = s_base = 0
    for _ in range(per):
        e, s, _r, ob = trial(list(rng.permutation(N)))
        if isinstance(_r, dict):
            _PF.append((len(_r.get('promos', ())), len(_r.get('fbs', ()))))
        if ob is not None and obj0: objs.append(abs(ob - obj0) / max(1e-300, abs(obj0)))
        tot += 1; f = len(e ^ SHIP_E) // 2; flips.append(f)
        chg += (f > 0); base += (s == SHIP_S); s_base += (s == SHIP_S)
        s_hz += ("hangzhou" in s); s_ec += ("english_channel" in s)
        counts[len(s)] += 1
        for x in s: holders[x] += 1
    per_seed[sd] = (s_hz, s_ec, s_base)
    print("  seed %-9d hangzhou %3d/%d  english_channel %3d/%d  baseline set %2d/%d"
          % (sd, s_hz, per, s_ec, per, s_base, per))
print()
print("pooled over %d relabellings" % tot)
print("  orientation changed        : %d of %d" % (chg, tot))
print("  edges moving               : mean %.2f, range %d-%d" % (sum(flips)/len(flips), min(flips), max(flips)))
print("  baseline sink set returned : %d (%.1f%%)" % (base, 100.0*base/tot))
print("  hangzhou an end            : %d-%d per hundred" % (min(v[0] for v in per_seed.values()),
                                                            max(v[0] for v in per_seed.values())))
print("  english_channel an end     : %d-%d per hundred" % (min(v[1] for v in per_seed.values()),
                                                            max(v[1] for v in per_seed.values())))
print("  sink-count distribution    : %s" % dict(sorted(counts.items())))
print("  most frequent end holders  : %s" % holders.most_common(6))
if objs:
    print("  LP objective deviation     : max %.3e over %d trials" % (max(objs), len(objs)))
else:
    print("  LP objective deviation     : not available - the implementation exposes no flow map,")
    print("                               so no figure here may be attributed to this script")

import collections as _c2
print('promotion/fallback pairs over the run:', dict(_c2.Counter(_PF)))
_r0 = trial(list(range(N)))[2]
print('identity promo/fb:', (len(_r0.get('promos', ())), len(_r0.get('fbs', ()))))
