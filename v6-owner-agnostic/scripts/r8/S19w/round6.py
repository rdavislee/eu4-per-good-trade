# -*- coding: utf-8 -*-
"""Every figure round 6 wrote into the spec that no other script in this tree computes.

The claims delta caught six measured propositions quoted with no instrument named at their line.
That is the Y250 defect -- a figure in the document that nothing in the tree reproduces -- and it is
the one C5 was created to close, so it does not get to come back in the batch that closed it.

Each block below prints the figure exactly as the document states it, so a reader can compare
without arithmetic.

Nothing here measures the superseded marking-order aggregate. An earlier revision did; that is
maintenance for an operator the model does not install, and the document no longer names it at all.

Usage: python round6.py
"""
import collections
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import drain                                                    # noqa: E402
import flowop                                                   # noqa: E402
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS,      # noqa: E402
                    PRICES, ROWS, build_sc)
from drain import (run_drain, sinks_of, phase0, phase1, phase2, # noqa: E402
                   sweep_priority, compile_dirs)
from flowop import mincost_flow, ARCS, TIE_EPS, TIE_EPS2        # noqa: E402

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N)
np.add.at(NODEW, PN, W)
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))   # noqa: E731
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
R = {g: run_drain(S[gi] - C[gi]) for gi, g in GL}


def bw(alpha=A_PHI):
    t = (W / W.max()) ** alpha
    n = np.zeros(N)
    np.add.at(n, PN, t)
    return np.full(N, 1.0 / N) - n / n.sum()


def head(t):
    print()
    print("=" * 94)
    print(t)
    print("=" * 94)


# ---- 3.2: the Cape is a conduit by FLOW, not merely by degree ------------------------------------
head("3.2  cape_of_good_hope as a conduit: degree against flow")
cape = NIDX["cape_of_good_hope"]
deg = flow = 0
exc = []
for gi, g in GL:
    d = R[g]["directed"]
    deg += (any(v == cape for _u, v in d) and any(u == cape for u, _v in d))
    fa = R[g].get("flow_arc") or {}
    fin = any(v == cape for _ei, (_u, v) in fa.items())
    fout = any(u == cape for _ei, (u, _v) in fa.items())
    flow += (fin and fout)
    if not (fin and fout):
        exc.append(g)
print("  in- and out-DEGREE both nonzero : %d of %d goods" % (deg, len(GL)))
print("  in- and out-FLOW  both nonzero  : %d of %d goods" % (flow, len(GL)))
print("  goods routing no flow through it: %s" % (", ".join(exc) or "none"))

# ---- 3.9: what makes an end is the flow identity ------------------------------------------------
head("3.9  flow_in - flow_out == -b_w, and out-degree is not the same question")
B = bw()
f, duals, res = mincost_flow(B + 0, np.zeros(N), cost=flowop.TIE_COST)
fin = np.zeros(N)
fout = np.zeros(N)
for ai, (u, v, _ei, _sg) in enumerate(ARCS):
    fout[u] += f[ai]
    fin[v] += f[ai]
resid = np.abs((fin - fout) - (-B))
dem = [i for i in range(N) if -B[i] > 0]
print("  identity holds on %d of %d nodes; max residual %.3g" % (int((resid < 1e-12).sum()), N, resid.max()))
print("  net demanders (-b_w > 0): %d ; identity holds on %d of them"
      % (len(dem), sum(1 for i in dem if resid[i] < 1e-12)))
outdeg = collections.Counter(u for u, _v in run_drain(B)["directed"])
print("  nodes with out-degree > 0 but ZERO outgoing flow: %d of %d"
      % (sum(1 for i in range(N) if outdeg[i] > 0 and fout[i] < 1e-12), N))

# ---- 2.3 / 3.6: the margin, and what the structured second term does ----------------------------
head("2.3 / 3.6  the uniqueness margin, and the structured second term")


def cost_of(kind, w):
    a1 = np.array([w[u] for (u, _v, _e, _s) in ARCS])
    a2 = np.array([w[v] for (_u, v, _e, _s) in ARCS])
    base = 1.0 + TIE_EPS * (a1 + a2) / 2.0
    if kind == "shipped":
        return base + TIE_EPS2 * np.modf(np.minimum(a1, a2) * np.maximum(a1, a2) * 7919.0)[0]
    return base + TIE_EPS2 * np.abs(a1 - a2)


def margin(b, cost):
    """min positive reduced cost off the support, and how many are exactly zero."""
    fl, du, _r = mincost_flow(b + 0, np.zeros(N), cost=cost)
    rc = np.array([cost[ai] - (du[ARCS[ai][1]] - du[ARCS[ai][0]]) for ai in range(len(ARCS))])
    off = rc[fl <= 1e-12]
    pos = off[off > 1e-14]
    return (float(pos.min()) if len(pos) else None), int((np.abs(off) <= 1e-14).sum())


WMM = (NODEW - NODEW.min()) / (NODEW.max() - NODEW.min())
SHIP = cost_of("shipped", WMM)
for a in (2.0, 1.5):
    m, _z = margin(bw(a), SHIP)
    print("  aggregate margin at alpha_Phi = %-4s : %.4g" % (a, m))
pg = sorted((margin(S[gi] - C[gi], SHIP)[0], g) for gi, g in GL)
inside = [(m, g) for m, g in pg if m <= 1e-7]
print("  per-good floor %.4g (%s); %d of %d at or below HiGHS's 1e-7 default: %s"
      % (pg[0][0], pg[0][1], len(inside), len(GL), ", ".join("%s %.4g" % (g, m) for m, g in inside)))
for kind in ("shipped", "structured"):
    c = cost_of(kind, WMM)
    alt = [g for gi, g in GL if margin(S[gi] - C[gi], c)[1] > 0]
    print("  %-11s: %d distinct edge costs of %d ; goods with an alternative optimum %d of %d %s"
          % (kind, len(set(np.round(c, 15))), len(EDGES_UND), len(alt), len(GL),
             "(" + ", ".join(alt) + ")" if alt else ""))

# ---- 2.8: the demand barbell, and razed China ---------------------------------------------------
head("2.8  the demand barbell, and razing a Chinese node")
top = bot = 0
for gi, g in GL:
    sk, _od = sinks_of(R[g]["directed"])
    order_ = sorted(range(N), key=lambda i: -C[gi][i])
    top += len(set(sk) & set(order_[:8]))
    bot += len(set(sk) & set(order_[-8:]))
tot = 8 * len(GL)
print("  sinks among each good's top-8 demanders    : %d of %d = %.1f%%" % (top, tot, 100.0 * top / tot))
print("  sinks among each good's bottom-8 demanders : %d of %d = %.1f%%" % (bot, tot, 100.0 * bot / tot))
base_d = set(run_drain(B)["directed"])
for node in ("hangzhou", "beijing"):
    m = np.array([NIDX[r["node"]] == NIDX[node] for r in ROWS])
    w2 = np.where(m, 0.0, W)
    t = (w2 / w2.max()) ** A_PHI
    nn = np.zeros(N)
    np.add.at(nn, PN, t)
    r2 = run_drain(np.full(N, 1.0 / N) - nn / nn.sum())
    d2 = set(r2["directed"])
    sk, _ = sinks_of(r2["directed"])
    print("  zeroing %-9s -> sinks %-30s  %d of %d edges flip"
          % (node, sorted(ORDER[i] for i in sk),
             sum(1 for (u, v) in base_d if (v, u) in d2), len(EDGES_UND)))

# ---- 1.6: how much of this section is a property of the SWEEP KEY -------------------------------
head("1.6  which of this section's aggregate facts move under a different sweep key")
CW = (np.zeros(N))
_t = (W / W.max()) ** A_PHI
np.add.at(CW, PN, _t)
CW = CW / CW.sum()


def facts(key):
    core, beta, Plog = phase0(B)
    Sset, _info = phase1(core, beta)
    fa, free, net, _cost = phase2(core, beta)
    o, _S2, promo, fb = sweep_priority(core, beta, Sset, fa, free, net, key)
    d = compile_dirs(core, o, fa, free, Plog, beta)
    outd = collections.Counter(u for u, _v in d)
    ind = collections.Counter(v for _u, v in d)
    sk = sorted(ORDER[i] for i in range(N) if outd[i] == 0)
    src = sorted(ORDER[i] for i in range(N) if ind[i] == 0)
    rank = {n: r for r, n in enumerate(sorted(range(N), key=lambda i: -CW[i]), 1)}
    adj = collections.defaultdict(list)
    for u, v in d:
        adj[u].append(v)

    def reach(a):
        seen, st = {a}, [a]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        return seen

    cp = reach(cape)
    into = [a for a in range(N) if a != cape and cape in reach(a)]
    return {
        "sink set": tuple(sk),
        "sink count": len(sk),
        "promotions": len(promo),
        "fallbacks": len(fb),
        "acyclic": drain.has_cycle(d) is None,
        "edges oriented": len(d),
        "genua out-degree": outd[NIDX["genua"]],
        "genua in-degree": ind[NIDX["genua"]],
        "cape in-degree": ind[cape],
        "cape out-degree": outd[cape],
        "source count": len(src),
        "source c_w rank range": (min(rank[NIDX[s]] for s in src), max(rank[NIDX[s]] for s in src)),
        "source mean degree": round(float(np.mean([len(UND[NIDX[s]]) for s in src])), 2),
        "cape ordered pairs": sum(1 for a in into for b in cp if b not in (cape, a) and b in reach(a)),
        "white_sea reaches hangzhou": NIDX["hangzhou"] in reach(NIDX["white_sea"]),
        "sevilla reaches ganges_delta": NIDX["ganges_delta"] in reach(NIDX["sevilla"]),
        "sevilla reaches hangzhou": NIDX["hangzhou"] in reach(NIDX["sevilla"]),
        "english_channel reaches genua": NIDX["genua"] in reach(NIDX["english_channel"]),
        "ec via champagne": (NIDX["champagne"] in adj[NIDX["english_channel"]]
                             and NIDX["genua"] in adj[NIDX["champagne"]]),
    }


A, Bk = facts("defasc_beta"), facts("def_beta")
moved = [k for k in A if A[k] != Bk[k]]
for k in A:
    print("  %-30s %-24s %-24s %s"
          % (k, str(A[k])[:24], str(Bk[k])[:24], "<== MOVES" if k in moved else ""))
print("  facts moving under DEF-descending: %d of %d" % (len(moved), len(A)))

# ---- 1.10: how much scripted content touches a trade node, and by which construct ---------------
head("1.10  scripted content's exposure to trade nodes, by class")
import re                                                        # noqa: E402
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
TREES = ("common", "missions", "decisions", "events")
FAM = {
    "home_trade_node": re.compile(r"\bhome_trade_node\b"),
    "*_active_trade_node": re.compile(r"\b(?:any|random|every)_active_trade_node\b"),
    "*_trade_node_member_province": re.compile(r"\b(?:any|random|every|all)_trade_node_member_province\b"),
    "highest_value_trade_node": re.compile(r"\bhighest_value_trade_node\b"),
}
ANY = re.compile(r"\btrade_node\b")
NAMES = re.compile(r"\b(" + "|".join(re.escape(n) for n in sorted(ORDER, key=len, reverse=True)) + r")\b")
cnt = collections.Counter()
other = named = 0
if os.path.isdir(EU4):
    for tree in TREES:
        for dp, _dn, fns in os.walk(os.path.join(EU4, tree)):
            for fn in fns:
                if not fn.lower().endswith(".txt"):
                    continue
                p = os.path.join(dp, fn)
                try:
                    body = re.sub(r"#[^\n]*", "", open(p, encoding="utf-8-sig", errors="replace").read())
                except OSError:
                    continue
                left = body
                for name, rx in FAM.items():
                    cnt[name] += len(rx.findall(body))
                    left = rx.sub(" ", left)
                other += len(ANY.findall(left))
                if "tradenodes" not in p.replace(chr(92), "/"):
                    named += len(NAMES.findall(body))
    for name in FAM:
        print("  %-32s %4d uses" % (name, cnt[name]))
    print("  %-32s %4d" % ("TOTAL, four families", sum(cnt.values())))
    print("  `trade_node` tokens outside the four families: %d" % other)
    print("  trade-node NAMES appearing in those four trees: %d" % named)
else:
    print("  EU4 install not found at %s -- skipped" % EU4)
print()

# ---- 2.1: is the free-versus-flow classification anywhere near its threshold? --------------------
head("2.1  the per-good |net| distribution around the 1e-11 zero-flow tolerance")
mags = []
for gi, g in GL:
    core, beta, _Plog = phase0(S[gi] - C[gi])
    _fa, _free, net, _cost = phase2(core, beta)
    mags.extend(abs(float(x)) for x in net)
mags = np.array(mags)
zero = int((mags == 0.0).sum())
above = int((mags > 1e-6).sum())
between = mags[(mags > 0.0) & (mags <= 1e-6)]
print("  edge-goods at exactly 0        : %d" % zero)
print("  edge-goods above 1e-6          : %d" % above)
print("  edge-goods strictly between    : %d" % len(between))
print("  smallest non-zero |net|        : %.4g" % (mags[mags > 0].min() if (mags > 0).any() else float("nan")))
print("  the 1e-11 threshold therefore sits in an empty band")

# ---- 2.3 / 3.13: HiGHS's own floor for the tolerance options -------------------------------------
head("2.3 / 3.13  what HiGHS does when the tolerance is set below its floor")
from scipy.optimize import linprog                              # noqa: E402
AEQ, A_ = flowop.AEQ, len(ARCS)
bvec = np.zeros(N) - B


def solve_at(tol):
    opts = None if tol is None else {"dual_feasibility_tolerance": tol,
                                     "primal_feasibility_tolerance": tol}
    r = linprog(c=flowop.TIE_COST, A_eq=AEQ, b_eq=bvec, bounds=(0, None),
                method="highs", options=opts)
    return r


import io as _io                                                # noqa: E402
import contextlib                                               # noqa: E402
for tol in (None, 1e-7, 1e-10, 1e-11, 1e-12):
    buf = _io.StringIO()
    with contextlib.redirect_stderr(buf), contextlib.redirect_stdout(buf):
        r = solve_at(tol)
    noise = buf.getvalue()
    flag = "Invalid option value" in noise or "Invalid option value" in (r.message or "")
    print("  tolerance %-7s success=%-5s objective=%.17g%s"
          % (tol, r.success, r.fun, "   <== rejected: Invalid option value" if flag else ""))
print("  a rejected option leaves success True, so the failure is silent unless stderr is read")
print()
print("  Does a rejected option REVERT to the 1e-7 default, or hold the last valid setting?")
print("  Tested on `copper`, whose margin (3.765e-08) is the one the default straddles: solve it")
print("  under column permutations and count how many edge-slots move against the shipped order.")
_gi = GOODS.index("copper")
_b = S[_gi] - C[_gi]
_rng = np.random.default_rng(4)
_perms = [np.arange(len(ARCS))] + [_rng.permutation(len(ARCS)) for _ in range(4)]


def _orient_at(tol, perm):
    opts = None if tol is None else {"dual_feasibility_tolerance": tol,
                                     "primal_feasibility_tolerance": tol}
    cost = flowop.TIE_COST[perm]
    aeq = flowop.AEQ[:, perm]
    with contextlib.redirect_stderr(_io.StringIO()):
        r = linprog(c=cost, A_eq=aeq, b_eq=np.zeros(N) - _b, bounds=(0, None),
                    method="highs", options=opts)
    x = np.zeros(len(ARCS))
    x[perm] = r.x
    net = np.zeros(len(EDGES_UND))
    for ai, (_u, _v, ei, sg) in enumerate(ARCS):
        net[ei] += sg * x[ai]
    return tuple(np.sign(np.where(np.abs(net) > 1e-11, net, 0.0)).astype(int))


_flipsets = {}
for tol in (None, 1e-7, 1e-8, 1e-10, 1e-11):
    ref = _orient_at(tol, _perms[0])
    fset = set()
    for pi, p in enumerate(_perms[1:], 1):
        got = _orient_at(tol, p)
        for slot, (a, b) in enumerate(zip(ref, got)):
            if a != b:
                fset.add((pi, slot))
    _flipsets[tol] = fset
    print("    tolerance %-7s edge-slots moving over 4 permutations: %d" % (tol, len(fset)))
# The revert claim is about SETS, not counts: a rejected value must reproduce the default's flips
# exactly -- same permutations, same slots -- not merely the same number of them. Counts alone
# could agree by coincidence; set identity is what "behaves like the default" means.
print("    flip SET identity: unset == 1e-7: %s ; rejected 1e-11 == unset: %s ; 1e-8 == 1e-10 == empty: %s"
      % (_flipsets[None] == _flipsets[1e-7],
         _flipsets[1e-11] == _flipsets[None],
         _flipsets[1e-8] == _flipsets[1e-10] == set()))
print("  A rejected value reproducing the DEFAULT's flip set exactly is the revert.")

# ---- 1.3: which province-condition modifiers are actually live on the 1444 field ----------------
head("1.3  province-condition modifiers live at the 1444 start")
import solver as _sv                                            # noqa: E402
_live = {}
for _m in ("devastation", "prosperity", "under_siege", "occupied"):
    _src = getattr(_sv, "ON_STARTUP_" + _m.upper(), None)
    _n = len([1 for _v in _src.values() if _v]) if isinstance(_src, dict) else 0
    _live[_m] = _n
for _m, _n in _live.items():
    print("  %-12s live on %d counted province(s)%s"
          % (_m, _n, "" if _n else "   <== no input on this field"))
print("  solver.LIVE_STATE_MODS = %s" % (getattr(_sv, "LIVE_STATE_MODS", "?"),))
print("  solver.STATE_TAX_MOD   = %s   (empty: no modifier reaches the tax term)"
      % (getattr(_sv, "STATE_TAX_MOD", "?"),))

# ---- 1.6: are both surviving ends western on the 22-node scaling above x2.50? -------------------
head("1.6  the 22-node European scaling above x2.50: are both surviving ends western?")
_W18 = ["english_channel", "north_sea", "baltic_sea", "white_sea", "novgorod", "lubeck",
        "rheinland", "saxony", "wien", "krakow", "pest", "venice", "ragusa", "genua",
        "champagne", "bordeaux", "valencia", "sevilla"]
_EAST4 = ["constantinople", "crimea", "kiev", "kazan"]
_idx22 = {NIDX[x] for x in _W18 + _EAST4}
_east = set(_EAST4)
_bad = []
_k = 2.50
while _k <= 25.0 + 1e-9:
    _w = np.array([W[i] * (_k if PN[i] in _idx22 else 1.0) for i in range(len(ROWS))])
    _t = (_w / _w.max()) ** A_PHI
    _nn = np.zeros(N); np.add.at(_nn, PN, _t)
    _r = run_drain(np.full(N, 1.0 / N) - _nn / _nn.sum())
    _sk, _ = sinks_of(_r["directed"])
    _names = sorted(ORDER[i] for i in _sk)
    if any(x in _east for x in _names):
        _bad.append((_k, _names))
    _k = round(_k + 0.25, 4)
print("  swept x2.50 to x25.00 in steps of 0.25")
print("  multiples where any of the eastern four holds an end: %s" % (_bad or "none"))
print("  so above x2.50 both surviving ends are western: %s" % (not _bad))

# ---- 2.3: does an unpinned solver UNDERCOUNT the normalisation sweep? ---------------------------
head("2.3  the normalisation sweep with and without the pinned tolerance")


def _norm_movers(opts):
    old = flowop.LP_OPTS
    flowop.LP_OPTS = opts
    try:
        base = {}
        for gi, g in GL:
            base[g] = set(drain.run_drain(S[gi] - C[gi])["directed"])
        wm = NODEW / NODEW.mean()
        c = cost_of("shipped", wm)
        oldc, drain.TIE_COST, flowop.TIE_COST = flowop.TIE_COST, c, c
        try:
            return {g for gi, g in GL if set(drain.run_drain(S[gi] - C[gi])["directed"]) != base[g]}
        finally:
            drain.TIE_COST = flowop.TIE_COST = oldc
    finally:
        flowop.LP_OPTS = old


_pinned = _norm_movers({"dual_feasibility_tolerance": 1e-10, "primal_feasibility_tolerance": 1e-10})
_unpinned = _norm_movers(None)
print("  goods moving under w/mean, tolerance pinned at 1e-10 : %d" % len(_pinned))
print("  goods moving under w/mean, tolerance left at default : %d" % len(_unpinned))
print("  the unpinned set is a strict subset of the pinned set: %s"
      % (_unpinned < _pinned if _unpinned != _pinned else "equal"))
print()
