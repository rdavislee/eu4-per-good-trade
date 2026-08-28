# -*- coding: utf-8 -*-
"""validation-v2 numerical battery.

PART A  baseline DRAIN (deterministic sweep, spec defaults) - V013 V028 V029(meas)
        V030 V032 V035 V037 V041 V060 V061 V062 V089 V090 V128 V129 V159 V186
PART B  calibration config (k_exp=2 unclamped, rho=0.5, tol=3e-4) - V107 V177 V179 V180
PART C  v1 identity work - V138 V204 (and the corrected-identity control)
PART D  V168 country development
PART E  V117 supply/demand contrast magnitudes
"""
import numpy as np, collections, time, sys, os, io, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.stats import spearmanr
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, PROV, PNODE,
                    ROWS, EXCLUDED, build_sc, solve_phi, orient, COMPS)
import drain
from drain import run_drain, sinks_of, has_cycle, sweep_priority, phase0, compile_dirs
from flowop import mincost_flow, net_per_edge, ZERO_TOL, TIE_COST

# C3: final.py is the only producer of several figures the document asserts, and it is slow enough
# that verify6.py cannot call it inline. It therefore writes a cache -- but a cache verify6 trusted
# on AGE would go stale silently the moment someone edited an input and did not rerun. So the
# producer stamps the identity of everything it consumed, and the consumer recomputes that stamp.
# A missing cache is a hard failure, not a skip: "I could not check" must never read as a pass.
FINAL_OUT = {}


def input_fingerprint():
    """sha256 over the sources this run consumed. Identity, not mtime."""
    h = hashlib.sha256()
    for _f in ("solver.py", "drain.py", "flowop.py", "final.py"):
        h.update(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), _f), "rb").read())
    return h.hexdigest()


E = len(EDGES_UND)
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S0m, C0m, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
print("live goods:", len(GL), "| components:", len(COMPS))

def reach_share(directed, gi, c):
    srcs = [i for i in range(N) if GP[gi][i] > 0]
    a = collections.defaultdict(list)
    for u, v in directed: a[u].append(v)
    seen = set(srcs); q = collections.deque(srcs)
    while q:
        x = q.popleft()
        for y in a[x]:
            if y not in seen: seen.add(y); q.append(y)
    return c[list(seen)].sum() / c.sum(), seen

def eval_phase4_full(directed, b):
    """greedy DEF-weighted push; returns (unserved demand, stranded supply)."""
    outs = collections.defaultdict(list); indeg = collections.Counter()
    for (u, v) in directed:
        outs[u].append(v); indeg[v] += 1
    q = collections.deque([i for i in range(N) if indeg[i] == 0])
    ind = dict(indeg); topo = []
    while q:
        x = q.popleft(); topo.append(x)
        for y in outs[x]:
            ind[y] -= 1
            if ind[y] == 0: q.append(y)
    if len(topo) != N: return None, None
    dfc = {}
    for v in reversed(topo):
        dfc[v] = max(0.0, -b[v]) + sum(dfc[u] for u in outs[v])
    inflow = collections.defaultdict(float); uns = 0.0; stranded = 0.0
    for v in topo:
        if b[v] > 0: out = inflow[v] + b[v]
        else:
            srv = min(inflow[v], -b[v]); uns += (-b[v]) - srv; out = inflow[v] - srv
        tg = outs[v]
        if tg:
            ws = sum(dfc[t] for t in tg)
            for t in tg: inflow[t] += out * ((dfc[t]/ws) if ws > 0 else 1.0/len(tg))
        else:
            stranded += out
    return uns, stranded

# ============================================================ PART A: baseline
print("\n" + "="*100); print("PART A - baseline DRAIN, deterministic sweep"); print("="*100)
t0 = time.time()
R = {}
for gi, g in GL:
    b = S0m[gi] - C0m[gi]
    R[g] = run_drain(b)
t1 = time.time()
print("V090 wall time, all %d goods (LP+sweep, scipy HiGHS): %.2f s (%.1f ms/good)"
      % (len(GL), t1-t0, 1000*(t1-t0)/len(GL)))

acyc = 0; sink_counts = []; formula_ok = 0; formula_bad = []
order_repro_ok = 0; ties_defbeta = 0; supp_sizes = []
cons_ok = 0; reach_ok = 0; orphan_total = 0
for gi, g in GL:
    r = R[g]; d = r["directed"]
    sk, od = sinks_of(d); sink_counts.append(len(sk))
    if has_cycle(d) is None: acyc += 1
    # V029 measured: sinks == {S0 cap flow-terminal} U promoted
    ft = set(v for v in r["core"] if not any(True for ei,(u,vv) in r["flow_arc"].items() if u==v))
    claimed = (set(r["S0"]) & ft) | set(r["promotions"])
    if set(sk) == claimed: formula_ok += 1
    else: formula_bad.append((g, sorted(ORDER[i] for i in set(sk)^claimed)))
    # V060 measured: orientation by marking order descending == directed graph (core edges)
    o = r["order"]
    ok = all(((o[u] > o[v]) and (u,v) or (v,u)) in set(d) if False else True for u,v in [])
    repro = True
    dset = set(d)
    for ei, (u, v) in enumerate(EDGES_UND):
        want = (u, v) if o[u] > o[v] else (v, u)
        if want not in dset: repro = False; break
    order_repro_ok += repro
    supp_sizes.append(len(r["flow_arc"]))
    # V032: reach + orphans
    rs, seen = reach_share(d, gi, C0m[gi])
    if rs >= 1.0 - 1e-12: reach_ok += 1
    orphan_total += sum(1 for s in sk if s not in seen and C0m[gi][s] > 0)
    # V089: unserved == stranded
    uns, srd = eval_phase4_full(d, S0m[gi]-C0m[gi])
    if uns is not None and abs(uns - srd) < 1e-9: cons_ok += 1

print("V028 acyclic: %d/29" % acyc)
print("V030 sinks/good: min %d max %d mean %.1f" % (min(sink_counts), max(sink_counts), np.mean(sink_counts)))
print("V029 measured (sinks == {S0 cap ft} U promoted): %d/29 goods; mismatches: %s" % (formula_ok, formula_bad))
print("V060 measured (order-descending reproduces DAG): %d/29" % order_repro_ok)
print("V032 reach==100%%: %d/29 | orphan sinks total: %d" % (reach_ok, orphan_total))
print("V089 unserved==stranded (<1e-9): %d/29" % cons_ok)
print("V186 support sizes: min %d max %d (N-1 = %d)" % (min(supp_sizes), max(supp_sizes), N-1))
_kc = collections.Counter(R[g]["info"]["k"] for _, g in GL)
print("V013 k values: %s" % _kc)
FINAL_OUT["phase1 k==1 goods"] = str(_kc[1])
FINAL_OUT["phase1 live goods"] = str(len(GL))

# V041/V128: nodes with b == 0 exactly for every good; cape s=c=0
allzero = [i for i in range(N) if all(S0m[gi][i]==0.0 and C0m[gi][i]==0.0 for gi,_ in GL)]
bzero_pergood = collections.Counter()
for gi, g in GL:
    b = S0m[gi]-C0m[gi]
    for i in range(N):
        if b[i] == 0.0: bzero_pergood[ORDER[i]] += 1
print("V128 nodes with s=c=0 for ALL goods:", [ORDER[i] for i in allzero])
print("V041 nodes with b==0 exactly (count per node over 29 goods):", dict(bzero_pergood))

# V129 cape conduit
cape = NIDX["cape_of_good_hope"]; cond = 0
for gi, g in GL:
    d = R[g]["directed"]
    ind = sum(1 for u,v in d if v==cape); outd = sum(1 for u,v in d if u==cape)
    cond += (ind>0 and outd>0)
print("V129 cape in>0 and out>0: %d/29" % cond)

# V037: six identical solves
base = None; same = True
for it in range(6):
    r = run_drain(S0m[GOODS.index('spices')] - C0m[GOODS.index('spices')])
    key = tuple(sorted(r["directed"]))
    if base is None: base = key
    elif key != base: same = False
print("V037 six identical solves -> one orientation (spices):", same)

# V035: permute the index tie-break key, count orientation changes + exact key ties
rng = np.random.default_rng(7)
flips_total = 0; ties_total = 0
for gi, g in GL:
    b = S0m[gi] - C0m[gi]
    core, beta, Plog = phase0(b)
    from drain import phase1, phase2, flow_def
    S, info = phase1(core, beta, 0)
    flow_arc, free, net, cost = phase2(core, beta)
    o1, S1, p1, f1 = sweep_priority(core, beta, S, flow_arc, free, net, "defasc_beta")
    d1 = set(compile_dirs(core, o1, flow_arc, free, Plog, beta))
    for perm in range(2):
        pid = {v: int(x) for v, x in zip(range(N), rng.permutation(N))}
        o2, S2, p2, f2 = sweep_priority(core, beta, S, flow_arc, free, net, "defasc_beta", pid=pid)
        d2 = set(compile_dirs(core, o2, flow_arc, free, Plog, beta))
        flips_total += len(d1 ^ d2) // 2
    # exact (DEF, beta) ties across free edges
    DEF = flow_def(core, beta, flow_arc)
    for ei in free:
        u, v = EDGES_UND[ei]
        if DEF[u]==DEF[v] and beta[u]==beta[v]: ties_total += 1
print("V035 orientation flips under 2 index permutations x29 goods:", flips_total,
      "| exact (DEF,b) ties on free edges:", ties_total)

# V159: ordered node pairs connected by >=1 good
conn = np.zeros((N,N), dtype=bool)
for gi, g in GL:
    a = collections.defaultdict(list)
    for u,v in R[g]["directed"]: a[u].append(v)
    for s in range(N):
        seen={s}; q=collections.deque([s])
        while q:
            x=q.popleft()
            for y in a[x]:
                if y not in seen: seen.add(y); q.append(y)
        for t in seen:
            if t!=s: conn[s][t]=True
print("V159 ordered pairs connected by >=1 good: %d/%d (%.1f%%)" % (conn.sum(), N*(N-1), 100*conn.sum()/(N*(N-1))))
FINAL_OUT["connectivity pct"] = "%.1f" % (100.0 * conn.sum() / (N * (N - 1)))
FINAL_OUT["connectivity pairs"] = "%d/%d" % (conn.sum(), N * (N - 1))

# ==================================================== PART B: calibration
print("\n" + "="*100); print("PART B - calibration k_exp=2 unclamped, rho=0.5, tol=3e-4, deterministic sweep"); print("="*100)
wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
wmax = wealth.max()
def build_c2(g, k_exp, clamp):
    a = (PRICES[g]/2.0)**k_exp
    if clamp: a = min(max(a, 0.2), 3.0)
    t = (wealth/wmax)**a
    num = np.zeros(N); np.add.at(num, pn, t)
    return num/num.sum(), a

def phase1_q(core, beta, rho):
    dem = sorted([v for v in core if beta[v] < 0], key=lambda v: beta[v])
    D = sum(-beta[v] for v in dem)
    if not dem or D <= 0: return set(), dict(k=0)
    keep, acc = [], 0.0
    for v in dem:
        keep.append(v); acc += -beta[v]
        if acc >= rho*D: break
    ks = set(keep); comps=[]; seen=set()
    for v in keep:
        if v in seen: continue
        comp={v}; st=[v]; seen.add(v)
        while st:
            x=st.pop()
            for y in UND[x]:
                if y in ks and y not in comp: comp.add(y); seen.add(y); st.append(y)
        comps.append(sorted(comp))
    M=[sum(-beta[v] for v in c_) for c_ in comps]
    HHI=sum((m/sum(M))**2 for m in M)
    k=int(min(max(round(1.0/HHI),1),len(comps)))
    S=set()
    for j in sorted(range(len(comps)), key=lambda j:-M[j])[:k]:
        S.add(min(comps[j], key=lambda v:(beta[v],v)))
    return S, dict(k=k)

TOL = 3e-4
cal = {}
old_tol = drain.ZERO_TOL
for gi, g in GL:
    c2, a2 = build_c2(g, 2, False)
    b = S0m[gi] - c2
    core, beta, Plog = phase0(b)
    S, info = phase1_q(core, beta, 0.5)
    # C2: the last surviving unit-cost Phase-2 call. Unit costs leave the LP degenerate, so the
    # calibration read a vertex the solver happened to return rather than the one DRAIN installs.
    # TOL below is section 3.13's knob and is deliberately untouched; only the cost vector changes.
    f, duals, res = mincost_flow(b + 0, np.zeros(N), cost=TIE_COST)  # s=b, c=0
    net = net_per_edge(f)
    flow_arc = {}; free = []
    for ei,(u,v) in enumerate(EDGES_UND):
        if abs(net[ei]) > TOL: flow_arc[ei] = (u,v) if net[ei]>0 else (v,u)
        else: free.append(ei)
    drain.ZERO_TOL = TOL
    o, Sset, promo, fb = sweep_priority(core, beta, S, flow_arc, free, net, "defasc_beta")
    drain.ZERO_TOL = old_tol
    d = compile_dirs(core, o, flow_arc, free, Plog, beta)
    sk, od = sinks_of(d)
    rs, seen = reach_share(d, gi, c2)
    # pruned twig mass
    pruned = sum(abs(net[ei]) for ei in free if abs(net[ei]) > ZERO_TOL)
    cal[g] = dict(sinks=[ORDER[i] for i in sk], n=len(sk), acyc=has_cycle(d) is None,
                  reach=rs, fb=len(fb), alpha=a2, pruned=pruned, c=c2)

counts = [cal[g]["n"] for _, g in GL]
prices = [PRICES[g] for _, g in GL]
sp = spearmanr(prices, counts)
print("V177 span: %d..%d | spearman(price, sinks) = %.3f" % (min(counts), max(counts), sp.statistic))
print("V179 cloves alpha=%.0f sinks: %s" % (cal["cloves"]["alpha"], cal["cloves"]["sinks"]))
print("V107 spices sinks under calibration: %s" % cal["spices"]["sinks"])
china_nodes = [n for n in ("beijing","hangzhou","canton","xian","chengdu","girin","yumen") if n in [s for s in cal["spices"]["sinks"]]]
print("V107 China nodes among calibration spices sinks:", china_nodes)
low = sorted((cal[g]["reach"], g) for _, g in GL)[:3]
print("V180 lowest reach under calibration: %s" % [(g, "%.4f%%" % (100*r)) for r, g in low])
print("V180 max pruned twig mass (share of world supply): %.5f" % max(cal[g]["pruned"] for _, g in GL))
print("     acyclic: %d/29 | fallbacks: %d" % (sum(cal[g]["acyc"] for _,g in GL), sum(cal[g]["fb"] for _,g in GL)))
# richest single province (V179 context)
ri = int(np.argmax(wealth))
print("V179 richest single province: pid=%s node=%s wealth=%.2f" % (ROWS[ri]["pid"], ROWS[ri]["node"], wealth[ri]))

# ==================================================== PART C: v1 identity
print("\n" + "="*100); print("PART C - v1 alpha=1 identity variants (V138, V204)"); print("="*100)
from solver import solve_phi0, laplacian
A1 = lambda g: 1.0
# (a) as v1 spec wrote it: per-good s gets eps, phi0's supply does not
Sa, Ca, Va, LIVEa, gpa, worlda = build_sc(A1, eps=1e-6)
PHI = np.zeros((len(GOODS), N))
for gi in range(len(GOODS)):
    if LIVEa[gi]: PHI[gi] = solve_phi(Sa[gi] - Ca[gi])
Phi_a = (Va[:, None] * PHI).sum(axis=0)
phi0, s0, c0 = solve_phi0()
k = (Phi_a @ phi0) / (phi0 @ phi0)
res_a = np.linalg.norm(Phi_a - k*phi0) / np.linalg.norm(Phi_a)
agree_a = sum(1 for u,v in EDGES_UND if (Phi_a[u]-Phi_a[v])*(phi0[u]-phi0[v]) > 0)
print("V204(a) eps on per-good s only  : rel residual %.2e | orientation agreement %d/159" % (res_a, agree_a))
# (b) eps applied to phi0's supply too
s0e = (1-1e-6)*s0 + 1e-6/N
phi0e = solve_phi(s0e - c0)
k2 = (Phi_a @ phi0e) / (phi0e @ phi0e)
res_b = np.linalg.norm(Phi_a - k2*phi0e) / np.linalg.norm(Phi_a)
agree_b = sum(1 for u,v in EDGES_UND if (Phi_a[u]-Phi_a[v])*(phi0e[u]-phi0e[v]) > 0)
print("V204(b) eps on both sides       : rel residual %.2e | orientation agreement %d/159" % (res_b, agree_b))
# (c) V138: production income as the aggregate supply term
tvp = np.zeros(N)
for r in ROWS:
    if r["good"] in EXCLUDED or r["good"] not in PRICES: continue
    tvp[NIDX[r["node"]]] += r["prod_income"]   # production income (== gp*price here; autonomy/eff not modeled)
s0p = tvp / tvp.sum()
phi0p = solve_phi(s0p - c0)
agree_c = sum(1 for u,v in EDGES_UND if (Phi_a[u]-Phi_a[v])*(phi0p[u]-phi0p[v]) > 0)
print("V138 phi0 with production-income supply: orientation agreement with Phi(a=1): %d/159" % agree_c)

# ==================================================== PART D: V168 country dev
print("\n" + "="*100); print("PART D - V168 caravan cap from raw 1444 development"); print("="*100)
dev = collections.Counter()
for pid, s in PROV.items():
    if s.get("owner") and s.get("owner") != "---":
        dev[s["owner"]] += (s.get("base_tax") or 0) + (s.get("base_production") or 0) + (s.get("base_manpower") or 0)
atcap = sorted((d, t) for t, d in dev.items() if d >= 150.0)
print("countries with dev >= 150 (dev/3 >= cap 50): %d" % len(atcap))
print([t for d, t in sorted(atcap, reverse=True)])
for t in ("BUR", "KOR", "TIM", "POR"):
    d = dev.get(t, 0)
    print("  %s dev=%.1f  dev/3=%.2f  short of cap by %.1f%%" % (t, d, d/3, 100*(150-d)/150))

# ==================================================== PART E: V117 contrasts
print("\n" + "="*100); print("PART E - V117 supply vs demand contrast"); print("="*100)
for g in ("spices", "cloves", "grain"):
    gi = GOODS.index(g)
    s = S0m[gi]; c = C0m[gi]
    smax = s.max(); smin_pos = s[s>0].min() if (s>0).any() else float('nan')
    cmax = c.max(); cmin_pos = c[c>0].min() if (c>0).any() else float('nan')
    print("%-8s supply max/min+ = %.3g   demand max/min+ = %.3g" % (g, smax/smin_pos, cmax/cmin_pos))


# ---- C3: the cache ------------------------------------------------------------------------------
FINAL_OUT["input fingerprint"] = input_fingerprint()
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "final.out"),
        "w", encoding="utf-8", newline=chr(10)).write(
    chr(10).join("%s\t%s" % (k, v) for k, v in FINAL_OUT.items()))
print()
print("wrote final.out with %d figures, stamped %s"
      % (len(FINAL_OUT) - 1, FINAL_OUT["input fingerprint"][:12]))
