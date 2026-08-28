# -*- coding: utf-8 -*-
"""DRAIN vs LAP (and the earlier candidates' reference numbers), full evaluation."""
import numpy as np, collections, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drain import run_drain, sinks_of, has_cycle
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc,
                    solve_phi, orient, EXCLUDED)
from flowop import ZERO_TOL
from scipy.stats import spearmanr

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
EPS = 1e-6
E = len(EDGES_UND)
S0m, C0m, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
S_UNI, _, _, _, _, _ = build_sc(ALPHA, eps=EPS)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
GI = {g: GOODS.index(g) for g in GL}
DEG = np.array([len(UND[i]) for i in range(N)])
LAPD = {g: orient(solve_phi(S_UNI[GI[g]] - C0m[GI[g]])) for g in GL}


def reach(d, srcs):
    a = collections.defaultdict(list)
    for u, v in d: a[u].append(v)
    seen = set(srcs); q = collections.deque(srcs)
    while q:
        x = q.popleft()
        for y in a[x]:
            if y not in seen: seen.add(y); q.append(y)
    return seen


def eval_phase4(directed, b):
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
    if len(topo) != N: return None
    dfc = {}
    for v in reversed(topo):
        dfc[v] = max(0.0, -b[v]) + sum(dfc[u] for u in outs[v])
    inflow = collections.defaultdict(float); uns = 0.0
    for v in topo:
        if b[v] > 0: out = inflow[v] + b[v]
        else:
            srv = min(inflow[v], -b[v]); uns += (-b[v]) - srv; out = inflow[v] - srv
        tg = outs[v]
        if tg:
            ws = sum(dfc[t] for t in tg)
            for t in tg: inflow[t] += out * ((dfc[t]/ws) if ws > 0 else 1.0/len(tg))
    return uns


def drains_to_sink(directed):
    """does every node reach a sink following out-arcs? (guarantee 4)"""
    a = collections.defaultdict(list)
    for u, v in directed: a[u].append(v)
    sk = set(sinks_of(directed)[0])
    ok = 0
    for s in range(N):
        seen = {s}; q = collections.deque([s]); hit = s in sk
        while q and not hit:
            x = q.popleft()
            for y in a[x]:
                if y in sk: hit = True; break
                if y not in seen: seen.add(y); q.append(y)
        ok += hit
    return ok


# ------------------------------------------------------------- per-good run --
print("=" * 108)
print("DRAIN - per-good results (dilate r=0, defaults)")
print("=" * 108)
print("  %-14s %4s %5s %2s | %3s %5s %3s | %6s %8s %7s %9s %8s %9s" %
      ("good", "clus", "HHI", "k", "S0", "promo", "fb", "sinks", "acyclic", "edges", "reach", "orphans", "drains"))
RES = {}
for g in GL:
    gi = GI[g]; b = S0m[gi] - C0m[gi]
    r = run_drain(b)
    d = r["directed"]
    sk, od = sinks_of(d)
    srcs = [i for i in range(N) if GP[gi][i] > 0]
    rs = reach(d, srcs)
    dem = C0m[gi][list(rs)].sum() / C0m[gi].sum()
    orph = sum(1 for i in sk if i not in rs)
    RES[g] = dict(r=r, d=d, sk=sk, dem=dem, orph=orph)
    print("  %-14s %4d %5.2f %2d | %3d %5d %3d | %6d %8s %7d %8.1f%% %8d %6d/80" %
          (g, r["info"]["nclusters"], r["info"]["HHI"], r["info"]["k"],
           len(r["S0"]), len(r["promotions"]), len(r["fallbacks"]),
           len(sk), has_cycle(d) is None, len(d), 100*dem, orph, drains_to_sink(d)))
print()
allsk = [len(RES[g]["sk"]) for g in GL]
print("  sinks/good: min %d max %d mean %.1f | goods with >1 sink: %d/29"
      % (min(allsk), max(allsk), np.mean(allsk), sum(1 for x in allsk if x > 1)))
print("  fallback promotions (outside the stall lemma) fired: %d times total"
      % sum(len(RES[g]["r"]["fallbacks"]) for g in GL))
print("  k > 1 for any good: %s" % any(RES[g]["r"]["info"]["k"] > 1 for g in GL))
print("  S0 members that ended up as final sinks: %d of %d"
      % (sum(len(set(RES[g]["r"]["S0"]) & set(RES[g]["sk"])) for g in GL),
         sum(len(RES[g]["r"]["S0"]) for g in GL)))
print()

# --------------------------------------------------------------- dilation ----
print("=" * 108); print("PHASE 1 DILATION (optional r): does it ever change k?"); print("=" * 108)
for rr_ in (0, 1, 2):
    ks = [run_drain(S0m[GI[g]] - C0m[GI[g]], dilate_r=rr_)["info"]["k"] for g in ("spices", "grain", "cloves", "livestock")]
    print("  r=%d : k for spices/grain/cloves/livestock = %s" % (rr_, ks))
print()

# ------------------------------------------------------------- correlation ---
print("=" * 108); print("SINK-DEMAND CORRELATION"); print("=" * 108)
rows = []
for tag in ("LAP", "DRAIN"):
    ar, ai, av, per = [], [], [], []
    t10 = b10 = t10n = b10n = 0
    for g in GL:
        gi = GI[g]; c = C0m[gi]
        rank = np.empty(N, dtype=int); rank[np.argsort(-c)] = np.arange(1, N+1)
        ss = set(sinks_of(LAPD[g])[0] if tag == "LAP" else RES[g]["sk"]); per.append(len(ss))
        for i in range(N):
            ar.append(rank[i]); av.append(c[i]); ai.append(1 if i in ss else 0)
            if rank[i] <= 10: t10n += 1; t10 += (i in ss)
            if rank[i] > N-10: b10n += 1; b10 += (i in ss)
    ar = np.array(ar); ai = np.array(ai); av = np.array(av)
    print("  %-6s sinks/g %.1f | mean rank %.1f | P(top10) %.1f%% | P(bot10) %.1f%% | rho_val %+.3f"
          % (tag, np.mean(per), ar[ai == 1].mean(), 100*t10/t10n, 100*b10/b10n,
             float(spearmanr(av, ai).statistic)))
print("  (references: RANK +0.281, BASIN +0.225, FLOW -0.132)")
fr = collections.Counter()
for g in GL:
    for i in RES[g]["sk"]: fr[ORDER[i]] += 1
print("  DRAIN most frequent sinks: %s" % fr.most_common(10))
print()

# ---------------------------------------------------------------- unserved ---
print("=" * 108); print("UNSERVED (shared Phase-4 evaluator, all 159/29-good orientations)"); print("=" * 108)
lu = np.mean([eval_phase4(LAPD[g], S0m[GI[g]] - C0m[GI[g]]) for g in GL])
du = np.mean([eval_phase4(RES[g]["d"], S0m[GI[g]] - C0m[GI[g]]) for g in GL])
print("  LAP   mean unserved %.4f" % lu)
print("  DRAIN mean unserved %.4f" % du)
print("  (references: BASIN best 0.2206; the LP certificate flow itself serves 100%% by construction)")
print()

# ----------------------------------------------------------- named nodes -----
print("=" * 108); print("SPICES / CLOVES AT THE NAMED NODES"); print("=" * 108)
for g in ("spices", "cloves"):
    gi = GI[g]; c = C0m[gi]
    rank = np.empty(N, dtype=int); rank[np.argsort(-c)] = np.arange(1, N+1)
    lsk = set(sinks_of(LAPD[g])[0]); dsk = set(RES[g]["sk"])
    print("  --- %s ---  DRAIN sinks: %s" % (g, [(ORDER[i], int(rank[i])) for i in sorted(dsk, key=lambda i: rank[i])]))
    for nm in ("genua", "venice", "beijing", "canton", "saxony", "safi", "english_channel", "hangzhou"):
        i = NIDX[nm]
        print("    %-16s c=%.5f rank=%2d | LAP %-4s DRAIN %-4s"
              % (nm, c[i], rank[i], "SINK" if i in lsk else "-", "SINK" if i in dsk else "-"))
print()

# ---------------------------------------------------------------- corridor ---
print("=" * 108); print("CAPE & CORRIDOR"); print("=" * 108)
cp = NIDX["cape_of_good_hope"]
for g in ("spices", "cloves"):
    d = RES[g]["d"]; D = set(d)
    ind = sum(1 for (u, v) in D if v == cp); outd = sum(1 for (u, v) in D if u == cp)
    a = collections.defaultdict(list)
    for u, v in d: a[u].append(v)
    def path(s, t):
        prev = {s: None}; q = collections.deque([s])
        while q:
            x = q.popleft()
            if x == t:
                p = []
                while x is not None: p.append(x); x = prev[x]
                return p[::-1]
            for y in a[x]:
                if y not in prev: prev[y] = x; q.append(y)
        return None
    src = NIDX["malacca"] if GP[GI[g]][NIDX["malacca"]] > 0 else int(np.argmax(GP[GI[g]]))
    p1 = path(src, cp); p2 = path(cp, NIDX["genua"])
    print("  %-8s cape in=%d out=%d conduit=%s" % (g, ind, outd, ind > 0 and outd > 0))
    print("     %s -> cape : %s" % (ORDER[src], " -> ".join(ORDER[x] for x in p1) if p1 else "NO PATH"))
    print("     cape -> genua : %s" % (" -> ".join(ORDER[x] for x in p2) if p2 else "NO PATH"))
print()

# --------------------------------------------------------------- safi edge ---
print("=" * 108); print("SAFI <-> SEVILLA"); print("=" * 108)
u, v = NIDX["safi"], NIDX["sevilla"]
agree = 0; wrongdir = []
for g in GL:
    gi = GI[g]
    def dof(dd):
        dd = set(dd)
        return "safi->sevilla" if (u, v) in dd else ("sevilla->safi" if (v, u) in dd else "unoriented")
    l, d_ = dof(LAPD[g]), dof(RES[g]["d"])
    agree += (l == d_)
    if S0m[gi][u] == 0 and d_ == "safi->sevilla": wrongdir.append(g)
print("  LAP/DRAIN agree on %d of 29 goods" % agree)
print("  goods where safi exports something it does not produce (DRAIN): %d %s" % (len(wrongdir), wrongdir[:8]))
print()

# ------------------------------------------------------------- aggregates ----
print("=" * 108); print("AGGREGATE Phi OPTIONS"); print("=" * 108)
# (a) value-weighted net flow = FLOW's aggregate -> known cyclic
Fagg = np.zeros(E)
for g in GL:
    Fagg += V[GI[g]] * RES[g]["r"]["net"]
dirs_f = []
for ei, (x, y) in enumerate(EDGES_UND):
    if Fagg[ei] > ZERO_TOL: dirs_f.append((x, y))
    elif Fagg[ei] < -ZERO_TOL: dirs_f.append((y, x))
print("  (a) value-weighted net flow: orients %d/159, cyclic: %s" % (len(dirs_f), has_cycle(dirs_f) is not None))
# (b) value-weighted marking order (a per-node scalar; arcs run high order -> low order)
PhiO = np.zeros(N)
for g in GL:
    o = RES[g]["r"]["order"]
    PhiO += V[GI[g]] * np.array([o[i] for i in range(N)])
do = orient(PhiO)
print("  (b) value-weighted marking order: orients %d/159, acyclic: %s" % (len(do), has_cycle(do) is None))
for tag, Phi, per in (("LAP", None, LAPD), ("DRAIN(order)", PhiO, {g: RES[g]["d"] for g in GL})):
    if Phi is None:
        Phi = np.zeros(N)
        for g in GL: Phi += V[GI[g]] * solve_phi(S_UNI[GI[g]] - C0m[GI[g]])
    ag = tot = 0
    for g in GL:
        for (x, y) in per[g]:
            tot += 1
            if Phi[x] > Phi[y]: ag += 1
    print("      %-13s aggregate agrees with its per-good graphs: %d/%d (%.1f%%)" % (tag, ag, tot, 100*ag/tot))
print()

# ------------------------------------------------------- order sensitivity ---
print("=" * 108); print("MARKING-ORDER SENSITIVITY (3 scan priorities)"); print("=" * 108)
for g in ("spices", "cloves", "grain"):
    gi = GI[g]; b = S0m[gi] - C0m[gi]
    sets = []
    for seed, prio in (("index", list(range(N))), ("reverse", list(range(N))[::-1]),
                       ("perm7", list(np.random.default_rng(7).permutation(N)))):
        pr = {v: prio.index(v) if isinstance(prio, list) else prio[v] for v in range(N)}
        pr = {v: k for k, v in enumerate(prio)}
        r2 = run_drain(b, prio=pr)
        sets.append((seed, frozenset(r2["directed"]), frozenset(sinks_of(r2["directed"])[0])))
    base = sets[0]
    for tag, dd, ss in sets:
        diff = len(base[1] ^ dd) // 2
        print("  %-8s %-8s edges differing from index-order: %3d/159 | sinks: %s"
              % (g, tag, diff, sorted(ORDER[i] for i in ss)))
print()

# ------------------------------------------------------------------ noise ----
print("=" * 108); print("+/-1% WEALTH NOISE, 5 seeds"); print("=" * 108)
wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
for g in ("grain", "spices", "cloves"):
    gi = GI[g]; a15 = ALPHA(g)
    base = set(RES[g]["d"]); bsk = frozenset(RES[g]["sk"])
    fl = []; skc = 0
    for seed in range(5):
        rng = np.random.default_rng(seed)
        w2 = wealth * (1 + rng.uniform(-0.01, 0.01, len(wealth)))
        num = np.zeros(N); np.add.at(num, pn, w2**a15); c2 = num / (w2**a15).sum()
        r2 = run_drain(S0m[gi] - c2)
        d2 = set(r2["directed"])
        fl.append(sum(1 for (x, y) in base if (y, x) in d2))
        if frozenset(sinks_of(r2["directed"])[0]) != bsk: skc += 1
    print("  %-8s edges flipped %.1f/159 | sink-set changes %d/5" % (g, np.mean(fl), skc))
print()

# --------------------------------------------------------- net-producers -----
npn = sum(1 for g in GL for i in RES[g]["sk"] if S0m[GI[g]][i] > C0m[GI[g]][i])
print("  sinks that net-produce their good: DRAIN %d of %d (LAP 0/102, RANK 9/387)"
      % (npn, sum(len(RES[g]["sk"]) for g in GL)))
cp_thr = sum(1 for g in GL
             if sum(1 for (x, y) in set(RES[g]["d"]) if y == cp) > 0
             and sum(1 for (x, y) in set(RES[g]["d"]) if x == cp) > 0)
print("  cape is a conduit (in>0 and out>0): %d/29 goods" % cp_thr)
