# -*- coding: utf-8 -*-
"""validate_v4b.py - the v4.0 spec's *untouched* measured figures, re-checked against the
regenerated wealth field.  Anything that drifted with the solver fix and was not updated
shows up here."""
import io, os, re, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, PROV, build_sc, COMPS, NODES)
from drain import run_drain, sinks_of, has_cycle, NODEW, phase0, phase1, phase2, sweep_priority, compile_dirs, flow_def

RES = []
def chk(cid, what, got, exp):
    ok = got == exp
    RES.append((ok, cid, what, got, exp))
    print("  [%s] %-8s %-56s got=%s exp=%s" % ("PASS" if ok else "FAIL", cid, what, got, exp))

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
def cvec(a, w=None):
    w = wealth if w is None else w
    t = (w / w.max()) ** a
    num = np.zeros(N); np.add.at(num, pn, t); return num / num.sum()
def phiw(a=1.5, w=None, scale=1.0):
    return run_drain((np.full(N, 1.0/N) - cvec(a, w)) * scale)

print("== 1.1 / 1.2 properties ==")
R = {g: run_drain(S[gi] - C[gi]) for gi, g in GL}
chk("1.1", "acyclic goods", sum(1 for _, g in GL if has_cycle(R[g]["directed"]) is None), 29)
sc = [len(sinks_of(R[g]["directed"])[0]) for _, g in GL]
chk("1.1", "sinks per good min/max/mean", (min(sc), max(sc), round(float(np.mean(sc)), 1)), (1, 8, 3.6))
chk("1.1", "k = 1 for 27 of 29 goods", collections.Counter(R[g]["info"]["k"] for _, g in GL)[1], 27)
supp = [len(R[g]["flow_arc"]) for _, g in GL]
chk("1.1", "support size <= N-1", (min(supp), max(supp), N - 1), (78, 79, 79))
def reach(d, gi, c):
    a = collections.defaultdict(list)
    for u, v in d: a[u].append(v)
    srcs = [i for i in range(N) if GP[gi][i] > 0]
    seen = set(srcs); q = collections.deque(srcs)
    while q:
        x = q.popleft()
        for y in a[x]:
            if y not in seen: seen.add(y); q.append(y)
    return c[list(seen)].sum() / c.sum(), seen
ok = orph = 0
for gi, g in GL:
    rs, seen = reach(R[g]["directed"], gi, C[gi])
    if rs >= 1 - 1e-12: ok += 1
    orph += sum(1 for s0 in sinks_of(R[g]["directed"])[0] if s0 not in seen and C[gi][s0] > 0)
chk("1.1", "goods at 100% demand reach", ok, 29)
chk("1.1", "orphan sinks", orph, 0)
rng = np.random.default_rng(7); flips = ties = 0
for gi, g in GL:
    b = S[gi] - C[gi]
    core, beta, Plog = phase0(b); Ssel, info = phase1(core, beta, 0)
    fa, free, net, cost = phase2(core, beta)
    o1, _, _, _ = sweep_priority(core, beta, Ssel, fa, free, net, "defasc_beta")
    d1 = set(compile_dirs(core, o1, fa, free, Plog, beta))
    for _ in range(2):
        pid = {v: int(x) for v, x in zip(range(N), rng.permutation(N))}
        o2, _, _, _ = sweep_priority(core, beta, Ssel, fa, free, net, "defasc_beta", pid=pid)
        flips += len(d1 ^ set(compile_dirs(core, o2, fa, free, Plog, beta))) // 2
    DEF = flow_def(core, beta, fa)
    for ei in free:
        u, v = EDGES_UND[ei]
        if DEF[u] == DEF[v] and beta[u] == beta[v]: ties += 1
chk("1.1", "orientation flips under permutation", flips, 0)
chk("1.1", "exact (DEF,b) ties on free edges", ties, 0)
chk("1.1", "fallbacks on 1444", sum(len(R[g]["fallbacks"]) for _, g in GL), 0)
zero_b = [ORDER[i] for i in range(N) if all((S[gi][i] - C[gi][i]) == 0.0 for gi, _ in GL)]
chk("1.2", "nodes with b == 0 for every good", zero_b, ["cape_of_good_hope"])
cape = NIDX["cape_of_good_hope"]
chk("3.2", "cape is a conduit for every good",
    sum(1 for _, g in GL if any(v == cape for u, v in R[g]["directed"]) and any(u == cape for u, v in R[g]["directed"])), 29)

print("== 1.6 Phi_w ==")
rw = phiw(); dws = set(rw["directed"])
od = collections.Counter(u for u, _ in rw["directed"]); idg = collections.Counter(v for _, v in rw["directed"])
srcs = [ORDER[i] for i in range(N) if idg[i] == 0]
cw = cvec(1.5); crank = {ORDER[i]: k + 1 for k, i in enumerate(np.argsort(-cw))}
chk("1.6", "sources", len(srcs), 8)
chk("1.6", "source c_w rank range", (min(crank[s] for s in srcs), max(crank[s] for s in srcs)), (44, 75))
chk("1.6", "source mean degree vs map", (round(float(np.mean([len(UND[NIDX[s]]) for s in srcs])), 1),
                                          round(float(np.mean([len(UND[i]) for i in range(N)])), 1)), (3.1, 4.0))
chk("1.6", "edges oriented", len(rw["directed"]), 159)
chk("1.6", "acyclic", has_cycle(rw["directed"]) is None, True)
o = rw["order"]
chk("1.6", "order-descending reproduces the DAG",
    sum(1 for u, v in EDGES_UND if ((u, v) if o[u] > o[v] else (v, u)) not in dws), 0)
chk("1.6", "Phase-1 selection", sorted(ORDER[i] for i in rw["S0"]), ["genua"])
chk("1.6", "promotions", sorted(ORDER[i] for i in rw["promotions"]), ["english_channel", "hangzhou"])
chk("1.6", "fallbacks", len(rw["fallbacks"]), 0)
f = s = 0
base_sinks = frozenset(ORDER[i] for i in range(N) if od[i] == 0)
for seed in range(5):
    r2 = np.random.default_rng(1000 + seed)
    w2 = wealth * (1 + r2.uniform(-0.01, 0.01, size=len(wealth)))
    rr = phiw(1.5, w2); d2 = set(rr["directed"])
    f += len(dws ^ d2) // 2
    o2 = collections.Counter(u for u, _ in rr["directed"])
    s += (frozenset(ORDER[i] for i in range(N) if o2[i] == 0) != base_sinks)
chk("1.6", "+/-1% noise: flips / sink-set changes", (f, s), (0, 0))
seq = []
for a in (1, 1.5, 2, 3, 4, 8):
    ra = phiw(float(a)); oa = collections.Counter(u for u, _ in ra["directed"])
    seq.append(sum(1 for i in range(N) if oa[i] == 0))
chk("1.6", "sink count across alpha_Phi", seq, [5, 2, 1, 2, 3, 1])
fl = []
for scale in (1.0, 1e-2, 1e-6):
    rs = phiw(1.5, scale=scale); os_ = collections.Counter(u for u, _ in rs["directed"])
    fl.append((len(dws ^ set(rs["directed"])) // 2, sum(1 for i in range(N) if os_[i] == 0)))
chk("1.6", "scale x1 / x1e-2 / x1e-6", fl, [(0, 2), (13, 2), (100, 1)])

print("== 2.2 / 2.4 / 2.8 map and file facts ==")
coastal = set(__import__("json").load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "coastal.json"))))
derived_inland = [n for n in ORDER if not any(p in coastal for p in NODES[n]["members"])]
flagged = [n for n in ORDER if NODES[n]["inland"] == "yes"]
chk("2.2", "inland derived vs flagged", (len(derived_inland), len(flagged)), (25, 26))
chk("2.2", "the one disagreement", sorted(set(flagged) - set(derived_inland)), ["siberia"])
chk("2.4", "vanilla end=yes nodes", [n for n in ORDER if NODES[n]["end"] == "yes"], ["genua", "venice", "english_channel"])
chk("2.4", "declaration-order violations", sum(1 for n in ORDER for m in NODES[n]["outgoing"] if ORDER.index(n) > ORDER.index(m)), 0)
chk("2.2a", "connected components", len(COMPS), 1)
chk("2.2a", "minimum degree", min(len(UND[i]) for i in range(N)), 2)
gi = GOODS.index("spices")
chk("2.8", "spices sinks", sorted(ORDER[i] for i in sinks_of(R["spices"]["directed"])[0]), ["australia", "brazil", "genua"])
chk("2.8", "cloves sinks", sorted(ORDER[i] for i in sinks_of(R["cloves"]["directed"])[0]), ["australia", "brazil", "kongo", "venice"])
chk("3.2", "nodes producing spices", int((GP[gi] > 0).sum()), 18)
chk("3.2", "nodes producing cloves", int((GP[GOODS.index("cloves")] > 0).sum()), 1)

print("== 3.3 / 3.5 file values ==")
dm = pdx.load(os.path.join(r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV", "map", "default.map"))
sea = set(int(x) for x in pdx.values(dm.get("sea_starts")))
lakes = set(int(x) for x in pdx.values(dm.get("lakes"))) if dm.get("lakes") else set()
land = {n: sum(1 for p in NODES[n]["members"] if p not in sea | lakes) for n in ORDER}
chk("3.3", "land counts cape/girin/nippon/champagne",
    (land["cape_of_good_hope"], land["girin"], land["nippon"], land["champagne"]), (19, 77, 68, 33))
chk("3.3", "slicing ratios", (round((77/19) ** 0.5, 2), round((68/33) ** 0.5, 2)), (2.01, 1.44))
chk("3.3", "sugar/cocoa/coffee vs grain",
    (round(PRICES["sugar"]/PRICES["grain"], 1), round(PRICES["cocoa"]/PRICES["grain"], 1), round(PRICES["coffee"]/PRICES["grain"], 1)), (1.2, 1.6, 1.2))
chk("3.5", "highest prices", (PRICES["coal"], PRICES["cloves"]), (10.0, 8.0))
chk("3.5", "minimum tradeable base price", min(p for p in PRICES.values() if p > 0), 2.0)

print("== 3.13 calibration ==")
A2 = lambda g: (PRICES[g] / 2.0) ** 2
S2, C2, V2_, L2, GP2, W2 = build_sc(A2, eps=0.0)
gc = GOODS.index("cloves")
dr = np.argsort(-C2[gc])
chk("3.13", "cloves demand rank 1 / 2 under alpha=16", (ORDER[dr[0]], ORDER[dr[1]]), ("hangzhou", "beijing"))
top = np.argsort(-wealth)[0]
bj = max(r["tax"] + r["prod_income"] for r in ROWS if r["node"] == "beijing")
chk("3.13", "richest province, hangzhou vs beijing",
    (ROWS[top]["node"], round(float(wealth[top]), 1), round(float(bj), 1)), ("hangzhou", 27.0, 19.5))

print("=" * 100)
bad = [r for r in RES if not r[0]]
print("RESULT: %d checks, %d failed" % (len(RES), len(bad)))
for r in bad: print("   FAIL:", r[1:])
