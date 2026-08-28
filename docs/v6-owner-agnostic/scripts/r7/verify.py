# -*- coding: utf-8 -*-
"""Re-verification of every headline number in diagnosis.md, flow-orientation.md,
ranked-orientation.md, basin-orientation.md. Prints PASS/FAIL per item."""
import numpy as np, collections, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc,
                    solve_phi, orient, EXCLUDED, solve_all, is_acyclic)
from flowop import mincost_flow, net_per_edge, ZERO_TOL, s_targeted, edges_from_net
from scipy.stats import spearmanr

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
EPS = 1e-6
E = len(EDGES_UND)
S0m, C0m, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
S_UNI, _, _, _, _, _ = build_sc(ALPHA, eps=EPS)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
GI = {g: GOODS.index(g) for g in GL}
DEG = np.array([len(UND[i]) for i in range(N)])
wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])

FAILS = []
def chk(doc, name, got, exp, tol=0.0):
    if isinstance(exp, (list, set, tuple)):
        ok = set(got) == set(exp); gs, es = sorted(got), sorted(exp)
    elif isinstance(exp, bool):
        ok = got == exp; gs, es = got, exp
    elif tol == 0.0:
        ok = got == exp; gs, es = got, exp
    else:
        ok = abs(got - exp) <= tol; gs, es = got, exp
    print("  [%s] %-58s got=%s exp=%s" % ("PASS" if ok else "FAIL", "%s :: %s" % (doc, name), gs, es))
    if not ok:
        FAILS.append((doc, name, gs, es))

def sinks_of(d):
    od = collections.Counter(u for u, _ in d)
    return [i for i in range(N) if od[i] == 0]

def reach(d, srcs):
    a = collections.defaultdict(list)
    for u, v in d: a[u].append(v)
    seen = set(srcs); q = collections.deque(srcs)
    while q:
        x = q.popleft()
        for y in a[x]:
            if y not in seen: seen.add(y); q.append(y)
    return seen

def has_cycle(d):
    a = collections.defaultdict(list)
    for u, v in d: a[u].append(v)
    col = [0]*N
    def dfs(u):
        col[u] = 1
        for w in a[u]:
            if col[w] == 1: return True
            if col[w] == 0 and dfs(w): return True
        col[u] = 2; return False
    return any(col[i] == 0 and dfs(i) for i in range(N))

LAPD = {g: orient(solve_phi(S_UNI[GI[g]] - C0m[GI[g]])) for g in GL}

print("=" * 100); print("DIAGNOSIS.MD"); print("=" * 100)
# identity at alpha=1
R1 = solve_all(lambda g: 1.0, eps=0.0)
tv = np.zeros(N)
for r in ROWS:
    if r["good"] in EXCLUDED or r["good"] not in PRICES: continue
    tv[NIDX[r["node"]]] += r["gp"] * PRICES[r["good"]]
s0 = tv / tv.sum()
c0 = np.zeros(N); np.add.at(c0, pn, wealth / wealth.sum())
phi0 = solve_phi(s0 - c0)
mask = np.abs(phi0) > 1e-12
k = (R1["Phi"][mask] / phi0[mask]).mean()
chk("valid", "Phi=k*phi0 scale k", round(k, 4), 3662.4)
chk("valid", "identity rel.residual < 1e-14", bool(np.abs(R1["Phi"] - k*phi0).max()/np.abs(R1["Phi"]).max() < 1e-14), True)
chk("valid", "identity orientation 159/159", len(set(orient(R1["Phi"])) & set(orient(phi0))), 159)
chk("valid", "per-good acyclicity 29/29", sum(1 for g in GL if not has_cycle(LAPD[g])), 29)
# exact sink criterion 2320/2320
Ra = solve_all(ALPHA, eps=EPS)
ok = 0; tot = 0
for gi, g in enumerate(GOODS):
    if not Ra["live"][gi]: continue
    ph = Ra["PHI"][gi]; od = collections.Counter(u for u, _ in orient(ph))
    for i in range(N):
        nb = UND[i]; nbphi = np.array([ph[j] for j in nb])
        drive = (Ra["C"][gi][i] - Ra["S"][gi][i]) / DEG[i]
        head = nbphi.mean() - nbphi.min()
        tot += 1
        if (drive > head) == (od[i] == 0): ok += 1
chk("diagnosis", "sink criterion exact", "%d/%d" % (ok, tot), "2320/2320")
# spices sink + c>s counts
gi = GI["spices"]
chk("diagnosis", "LAP spices sinks", [ORDER[i] for i in sinks_of(LAPD["spices"])], ["saxony"])
chk("diagnosis", "spices nodes with c>s", int((C0m[gi] > S_UNI[gi]).sum()), 64)
cgt = sum(int((C0m[GI[g]] > S_UNI[GI[g]]).sum()) for g in GL)
nsk = sum(len(sinks_of(LAPD[g])) for g in GL)
chk("diagnosis", "all-goods c>s pairs / sinks", "%d/%d" % (cgt, nsk), "1816/102")
# cape phi rank (doc says 'above 60 of the 80' -- measure the true number)
ph = solve_phi(S_UNI[gi] - C0m[gi])
below = int((ph < ph[NIDX["cape_of_good_hope"]]).sum())
print("  [INFO] diagnosis :: cape phi outranks N nodes: %d (doc says 'above 60' - imprecise if != 60)" % below)
# counterfactuals
cu = np.full(N, 1.0/N)
chk("diagnosis", "CF1 uniform-demand sinks", [ORDER[i] for i in sinks_of(orient(solve_phi(S_UNI[gi]-cu)))],
    ['patagonia','amazonas_node','saxony','baltic_sea','white_sea','valencia'])
chk("diagnosis", "CF2 uniform-supply sinks", [ORDER[i] for i in sinks_of(orient(solve_phi(cu-C0m[gi])))],
    ['gulf_of_siam','hangzhou','doab','wien'])
cg = np.full(N, 1e-9); cg[NIDX["genua"]] = 1.0 - 1e-9*(N-1)
chk("diagnosis", "CF3 all-demand-at-genua sink", [ORDER[i] for i in sinks_of(orient(solve_phi(S_UNI[gi]-cg)))], ["genua"])
# D threshold 1.725
a15 = 1.5
grows = np.array([kk for kk, r in enumerate(ROWS) if r["node"] == "genua"])
def spice_sinks_scaled(f):
    w = wealth.copy(); w[grows] *= f
    num = np.zeros(N); np.add.at(num, pn, w**a15); c = num/(w**a15).sum()
    return sinks_of(orient(solve_phi(S_UNI[gi]-c)))
lo, hi = 1.0, 200.0
for _ in range(40):
    mid = (lo+hi)/2
    if NIDX["genua"] in spice_sinks_scaled(mid): hi = mid
    else: lo = mid
chk("diagnosis", "D threshold f (genua co-sink)", round(hi, 3), 1.725, 0.005)

print("=" * 100); print("FLOW-ORIENTATION.MD (as corrected)"); print("=" * 100)
FL = {}
for g in GL:
    gi2 = GI[g]
    f, pi, res = mincost_flow(s_targeted(gi2), C0m[gi2])
    FL[g] = net_per_edge(f)
chk("flow", "spices support size", int((np.abs(FL["spices"]) > ZERO_TOL).sum()), 79)
chk("flow", "every good support = 79", all(int((np.abs(FL[g]) > ZERO_TOL).sum()) == 79 for g in GL), True)
same = opp = unor = 0
for g in GL:
    L = set(LAPD[g]); F = set(edges_from_net(FL[g]))
    for (u, v) in EDGES_UND:
        if (u, v) in F or (v, u) in F:
            if ((u, v) in F and (u, v) in L) or ((v, u) in F and (v, u) in L): same += 1
            else: opp += 1
        else: unor += 1
chk("flow", "same/opp/unoriented", "%d/%d/%d" % (same, opp, unor), "2158/133/2320")
Fagg = np.zeros(E)
for g in GL: Fagg += V[GI[g]] * FL[g]
chk("flow", "value-weighted aggregate net flow cyclic", has_cycle(edges_from_net(Fagg)), True)
f, pi, res = mincost_flow(s_targeted(GI["spices"]), C0m[GI["spices"]])
srcs_sp = [i for i in range(N) if GP[GI["spices"]][i] > 0]
def hops_to(i, srcset):
    if i in srcset: return 0
    seen = {i}; q = collections.deque([(i, 0)])
    while q:
        x, d = q.popleft()
        for y in UND[x]:
            if y in seen: continue
            if y in srcset: return d+1
            seen.add(y); q.append((y, d+1))
    return -1
H = np.array([hops_to(i, set(srcs_sp)) for i in range(N)])
chk("flow", "dual~distance spearman", round(float(spearmanr(pi - pi.min(), H).statistic), 4), 0.6097, 0.0005)
rr = [C0m[GI[g]][list(reach(edges_from_net(FL[g]), [i for i in range(N) if GP[GI[g]][i] > 0]))].sum() for g in GL]
chk("flow", "FLOW reach 100% all goods", all(x > 0.9999 for x in rr), True)
chk("flow", "LAP reach 100% all goods",
    all(C0m[GI[g]][list(reach(LAPD[g], [i for i in range(N) if GP[GI[g]][i] > 0]))].sum() > 0.9999 for g in GL), True)
# hop counts (the corrected claim)
def sp_via(a, z, via=None):
    def bfs(s, t):
        prev = {s: None}; q = collections.deque([s])
        while q:
            x = q.popleft()
            if x == t:
                p = []
                while x is not None: p.append(x); x = prev[x]
                return p[::-1]
            for y in UND[x]:
                if y not in prev: prev[y] = x; q.append(y)
        return None
    if via is None: return len(bfs(a, z)) - 1
    return len(bfs(a, via)) - 1 + len(bfs(via, z)) - 1
chk("flow", "malacca->channel via cape / via alexandria",
    "%d/%d" % (sp_via(NIDX["malacca"], NIDX["english_channel"], NIDX["cape_of_good_hope"]),
               sp_via(NIDX["malacca"], NIDX["english_channel"], NIDX["alexandria"])), "3/7")
ei_mc = next(ei for ei, (u, v) in enumerate(EDGES_UND) if {u, v} == {NIDX["malacca"], NIDX["cape_of_good_hope"]})
chk("flow", "spice flow malacca->cape", round(abs(FL["spices"][ei_mc]), 6), 0.242959, 1e-6)

print("=" * 100); print("RANKED-ORIENTATION.MD"); print("=" * 100)
from rankop import run as rank_run
RK = rank_run()
rr2 = []; orph = 0; totsk = 0
for g in GL:
    gi2 = GI[g]; srcs = [i for i in range(N) if GP[gi2][i] > 0]
    d = RK[g]["rank_dir"]; rs = reach(d, srcs)
    rr2.append(C0m[gi2][list(rs)].sum() / C0m[gi2].sum())
    sk = sinks_of(d); totsk += len(sk); orph += sum(1 for i in sk if i not in rs)
chk("ranked", "mean reach", round(100*np.mean(rr2), 2), 83.29, 0.02)
chk("ranked", "orphans/total sinks", "%d/%d" % (orph, totsk), "34/387")
ar, ai, av = [], [], []
for g in GL:
    gi2 = GI[g]; c = C0m[gi2]
    ss = set(sinks_of(RK[g]["rank_dir"]))
    for i in range(N):
        av.append(c[i]); ai.append(1 if i in ss else 0)
chk("ranked", "RANK rho_val", round(float(spearmanr(np.array(av), np.array(ai)).statistic), 3), 0.281, 0.001)
npn = sum(1 for g in GL for i in sinks_of(RK[g]["rank_dir"]) if S0m[GI[g]][i] > C0m[GI[g]][i])
chk("ranked", "RANK net-producer sinks", npn, 9)
D2 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "nodes.json")))
van_out = np.array([len(D2["nodes"][ORDER[i]]["outgoing"]) for i in range(N)])
cbar = np.zeros(N)
for g in GL: cbar += V[GI[g]] * C0m[GI[g]]
crank = np.argsort(np.argsort(-cbar))
chk("ranked", "vanilla outdeg spearman", round(float(spearmanr(crank, van_out).statistic), 3), 0.068, 0.001)
lo_ = np.array([np.mean([collections.Counter(u for u, _ in LAPD[g])[i] for g in GL]) for i in range(N)])
ro_ = np.array([np.mean([collections.Counter(u for u, _ in RK[g]["rank_dir"])[i] for g in GL]) for i in range(N)])
chk("ranked", "LAP outdeg spearman", round(float(spearmanr(crank, lo_).statistic), 3), -0.182, 0.001)
chk("ranked", "RANK outdeg spearman", round(float(spearmanr(crank, ro_).statistic), 3), 0.306, 0.001)

print("=" * 100); print("BASIN-ORIENTATION.MD"); print("=" * 100)
from basin import phase0 as b_p0, phase1 as b_p1, phase2 as b_p2, phase3 as b_p3, phase4 as b_p4, P as BP
def basin_run(b, S, K, sign, gamma):
    core, btil, pend, drains, pe = b_p0(b, UND)
    T, _ = b_p1(core, btil, UND, max(S, 1), BP["lam"], BP["R"])
    mu = {t: 1.0 for t in T}; scale = sum(max(0.0, -btil[v]) for v in core) or 1.0
    best = None
    for it in range(K):
        phi, basin, bal, tier, parent, SEED = b_p2(core, btil, UND, T, drains, mu, gamma,
                                                   BP["kplus"], BP["kminus"], BP["gmin"], BP["gmax"])
        d, key = b_p3(core, phi, tier, pe, UND)
        un, st = b_p4(core, btil, d, key)
        if best is None or un < best - 1e-15: best = un
        for t in mu: mu[t] = mu[t] * np.exp(sign * BP["eta"] * bal[t] / scale)
    return best
def lap_unserved(g):
    gi2 = GI[g]; b = S0m[gi2] - C0m[gi2]
    pl = solve_phi(S_UNI[gi2] - C0m[gi2])
    key = {v: (float(pl[v]), 0, v) for v in range(N)}
    un, st = b_p4(list(range(N)), {v: float(b[v]) for v in range(N)}, LAPD[g], key)
    return un
lu = np.mean([lap_unserved(g) for g in GL])
chk("basin", "LAP mean unserved (Phase4 eval)", round(float(lu), 4), 0.1037, 0.0005)
lapS = {g: len(sinks_of(LAPD[g])) for g in GL}
bw = np.mean([basin_run(S0m[GI[g]] - C0m[GI[g]], lapS[g], 8, -1.0, 0.0) for g in GL])
chk("basin", "BASIN as-written mean unserved", round(float(bw), 4), 0.3941, 0.001)
bf = np.mean([basin_run(S0m[GI[g]] - C0m[GI[g]], lapS[g], 8, +1.0, 0.0) for g in GL])
chk("basin", "BASIN sign-flipped mean unserved", round(float(bf), 4), 0.3242, 0.001)
bg = np.mean([basin_run(S0m[GI[g]] - C0m[GI[g]], lapS[g], 8, +1.0, 1000.0) for g in GL])
chk("basin", "BASIN gamma=1000 mean unserved", round(float(bg), 4), 0.2206, 0.001)
# LAP Phi self-coherence 52.6%
PhiL = np.zeros(N)
for g in GL: PhiL += V[GI[g]] * solve_phi(S_UNI[GI[g]] - C0m[GI[g]])
ag = tot2 = 0
for g in GL:
    for (x, y) in LAPD[g]:
        tot2 += 1
        if PhiL[x] > PhiL[y]: ag += 1
chk("basin", "LAP Phi self-coherence %", round(100*ag/tot2, 1), 52.6, 0.1)

print()
print("=" * 100)
print("RESULT: %d checks failed" % len(FAILS))
for f_ in FAILS: print("   FAIL:", f_)
