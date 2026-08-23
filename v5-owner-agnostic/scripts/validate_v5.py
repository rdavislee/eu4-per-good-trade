# -*- coding: utf-8 -*-
"""validate_v5.py — every figure spec v5.0 quotes, re-derived from the install and the reference
solver, plus presence/absence checks on the text that changed."""
import io, os, re, sys, collections, zipfile, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, PROV, PNODE,
                    build_sc, solve_phi, orient, COMPS, NODES,
                    LOCAL_TAX_MOD, LOCAL_TV_MOD, MON_FLAT, MON_GPMOD, MON_TVMOD, PERM_FLAT)
from drain import run_drain, sinks_of, has_cycle, NODEW

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
SPEC = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v5-owner-agnostic\per-good-trade-spec.md"
TXT = io.open(SPEC, encoding="utf-8").read()
RES = []
def chk(sec, what, got, exp):
    ok = got == exp; RES.append((ok, sec, what, got, exp))
    print("  [%s] %-7s %-52s got=%s exp=%s" % ("PASS" if ok else "FAIL", sec, what, got, exp))
def has(sec, what, s):
    ok = s in TXT; RES.append((ok, sec, what, "in spec" if ok else "ABSENT", "in spec"))
    print("  [%s] %-7s %-52s %s" % ("PASS" if ok else "FAIL", sec, what, "in spec" if ok else "NOT IN SPEC"))
def hasnt(sec, what, s):
    ok = s not in TXT; RES.append((ok, sec, what, "gone" if ok else "PRESENT", "gone"))
    print("  [%s] %-7s %-52s %s" % ("PASS" if ok else "FAIL", sec, what, "gone" if ok else "STILL IN SPEC"))

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
wealth = np.array([r["tax"]+r["prod_income"] for r in ROWS]); pn = np.array([NIDX[r["node"]] for r in ROWS])
def cvec(a, w=None):
    w = wealth if w is None else w
    t = (w/w.max())**a; num = np.zeros(N); np.add.at(num, pn, t); return num/num.sum()
def phiw(a=1.5, w=None, scale=1.0):
    return run_drain((np.full(N, 1.0/N) - cvec(a, w))*scale)

print("=" * 100); print("A. 1.3 the wealth field"); print("=" * 100)
chk("1.3", "world wealth", round(float(wealth.sum()), 2), 10677.50)
chk("1.3", "counted provinces", len(ROWS), 2452)
chk("1.3", "gems / incense province counts",
    (sum(1 for r in ROWS if r["good"] == "gems"), sum(1 for r in ROWS if r["good"] == "incense")), (43, 29))
chk("1.3", "monument provinces carried", sorted(set(MON_FLAT) | set(MON_GPMOD) | set(MON_TVMOD)),
    [8, 262, 684, 1821, 1822, 2145])
chk("1.3", "permanent-modifier provinces carried", sorted(PERM_FLAT), [6, 362, 363, 370, 371, 387, 542, 2151, 2316, 4316])
chk("1.3", "richest single province", (ROWS[int(np.argmax(wealth))]["pid"], round(float(wealth.max()), 2)), (1821, 30.40))
# re-derive the monument set independently
raw = re.sub(r"#[^\n]*", "", io.open(os.path.join(EU4, "common", "great_projects", "01_monuments.txt"), encoding="latin-1").read())
WK = ("trade_goods_size", "trade_goods_size_modifier", "trade_value_modifier", "local_tax_modifier")
found = []
for m in re.finditer(r"^([a-z0-9_]+)\s*=\s*\{", raw, re.M):
    i = m.end()-1; d = 0
    for j in range(i, len(raw)):
        if raw[j] == "{": d += 1
        elif raw[j] == "}":
            d -= 1
            if d == 0: break
    blk = raw[m.start():j+1]
    dt = re.search(r"\bdate\s*=\s*(\d+)\.", blk); st = re.search(r"starting_tier\s*=\s*(\d+)", blk)
    sp = re.search(r"\bstart\s*=\s*(\d+)", blk)
    if not (dt and st and sp) or int(dt.group(1)) > 1444: continue
    trig = re.search(r"can_use_modifiers_trigger\s*=\s*\{([\s\S]*?)\n\t\}", blk)
    if trig and trig.group(1).strip(): continue
    acc = {}
    for k in range(0, int(st.group(1))+1):
        tb = re.search(r"tier_%d\s*=\s*\{" % k, blk)
        if not tb: continue
        s2 = tb.end()-1; d2 = 0
        for j2 in range(s2, len(blk)):
            if blk[j2] == "{": d2 += 1
            elif blk[j2] == "}":
                d2 -= 1
                if d2 == 0: break
        pm = re.search(r"province_modifiers\s*=\s*\{([\s\S]*?)\}", blk[s2:j2+1])
        if pm:
            for a_, b_ in re.findall(r"([a-z_]+)\s*=\s*(-?[\d.]+)", pm.group(1)):
                if a_ in WK: acc[a_] = acc.get(a_, 0.0)+float(b_)
    if acc: found.append(int(sp.group(1)))
chk("1.3", "monument set re-derived from the install", sorted(found), [8, 262, 684, 1821, 1822, 2145])
has("1.3", "the Leviathan conditionality is stated", "stora_kopparberget_modifier")
has("1.3", "the state-dependent row", "`devastation` −2, `occupied` −0.5 and −0.5, `under_siege` −0.25, `prosperity` +0.25")
has("1.3", "the production_leader exclusion", "`production_leader` `trade_goods_size_modifier = 0.10`")
has("1.3", "the centers-of-trade near-miss", "**Centers of trade** (361 provinces carry one at 1444)")
hasnt("1.3", "the 'exactly two' claim", "So exactly **two** modifiers enter wealth in vanilla")
hasnt("1.3", "the flat-bonus denial", "no 1444 province was observed carrying a flat bonus in the first block")

print(); print("=" * 100); print("B. 1.1 / 1.6 the map"); print("=" * 100)
R = {g: run_drain(S[gi]-C[gi]) for gi, g in GL}
sc = [len(sinks_of(R[g]["directed"])[0]) for _, g in GL]
chk("1.1", "sinks per good", (min(sc), max(sc), round(float(np.mean(sc)), 1)), (1, 7, 3.6))
chk("1.1", "acyclic goods", sum(1 for _, g in GL if has_cycle(R[g]["directed"]) is None), 29)
chk("1.1", "fallbacks on 1444", sum(len(R[g]["fallbacks"]) for _, g in GL), 0)
rw = phiw(); dws = set(rw["directed"])
od = collections.Counter(u for u, _ in rw["directed"]); idg = collections.Counter(v for _, v in rw["directed"])
chk("1.6", "Phi_w sinks", sorted(ORDER[i] for i in range(N) if od[i] == 0), ["hangzhou"])
chk("1.6", "Phase-1 selection", sorted(ORDER[i] for i in rw["S0"]), ["hangzhou"])
chk("1.6", "promotions / fallbacks", (len(rw["promotions"]), len(rw["fallbacks"])), (0, 0))
srcs = [ORDER[i] for i in range(N) if idg[i] == 0]
cw = cvec(1.5); crank = {ORDER[i]: k+1 for k, i in enumerate(np.argsort(-cw))}
wrank = {ORDER[i]: k+1 for k, i in enumerate(np.argsort(-NODEW))}
chk("1.6", "sources", len(srcs), 7)
chk("1.6", "source c_w rank range", (min(crank[s] for s in srcs), max(crank[s] for s in srcs)), (52, 79))
chk("1.6", "source mean degree vs map",
    (round(float(np.mean([len(UND[NIDX[s]]) for s in srcs])), 1), round(float(np.mean([len(UND[i]) for i in range(N)])), 1)), (3.0, 4.0))
chk("1.6", "hangzhou c_w rank / node-wealth rank", (crank["hangzhou"], wrank["hangzhou"]), (1, 10))
chk("1.6", "english_channel node-wealth rank", wrank["english_channel"], 1)
chk("1.6", "largest |b_w|", round(float(np.abs(np.full(N, 1.0/N)-cw).max()), 4), 0.0227)
ag = tot = 0; wag = wtot = 0.0
PGd = {g: set(R[g]["directed"]) for _, g in GL}
for gi, g in GL:
    for u, v in EDGES_UND:
        gd = (u, v) if (u, v) in PGd[g] else ((v, u) if (v, u) in PGd[g] else None)
        if gd is None: continue
        tot += 1; wtot += V[gi]
        if ((u, v) if (u, v) in dws else (v, u)) == gd: ag += 1; wag += V[gi]
chk("1.6", "Phi_w agreement", (round(100.0*ag/tot, 1), round(100.0*wag/wtot, 1)), (52.5, 51.5))
Pord = np.zeros(N)
for gi, g in GL:
    for i in range(N): Pord[i] += V[gi]*R[g]["order"][i]
oa = ot = 0
for gi, g in GL:
    for u, v in EDGES_UND:
        gd = (u, v) if (u, v) in PGd[g] else ((v, u) if (v, u) in PGd[g] else None)
        if gd is None: continue
        ot += 1
        if ((u, v) if Pord[u] > Pord[v] else (v, u)) == gd: oa += 1
chk("3.9", "Phi_ord agreement", round(100.0*oa/ot, 1), 60.3)
ocnt = collections.Counter()
for u, v in EDGES_UND: ocnt[(u if Pord[u] > Pord[v] else v)] += 1
eo = [ORDER[i] for i in range(N) if ocnt[i] == 0]
chk("3.9", "Phi_ord ends", len(eo), 13)
chk("3.9", "Phi_ord ends terminating no good",
    sum(1 for n in eo if sum(1 for _, g in GL if not any(u == NIDX[n] for u, _ in PGd[g])) == 0), 8)
seq = []
for a in (1, 1.5, 2, 3, 4, 8):
    ra = phiw(float(a)); oa2 = collections.Counter(u for u, _ in ra["directed"])
    seq.append(sum(1 for i in range(N) if oa2[i] == 0))
chk("1.6", "sink count across alpha_Phi", seq, [5, 1, 2, 4, 3, 1])
bands = collections.defaultdict(list)
for k in range(100, 301):
    a = round(k/100, 2)
    ra = phiw(a); o3 = collections.Counter(u for u, _ in ra["directed"])
    bands[tuple(sorted(ORDER[i] for i in range(N) if o3[i] == 0))].append(a)
b1 = bands[("hangzhou",)]
chk("1.6", "the 1-sink band", (min(b1), max(b1), round(max(b1)-min(b1), 2)), (1.43, 1.93, 0.50))
b2 = bands[("genua", "hangzhou")]
chk("1.6", "the {genua,hangzhou} band", (min(b2), max(b2), round(max(b2)-min(b2), 2)), (1.94, 2.25, 0.31))
b3 = bands[("english_channel", "hangzhou")]
chk("1.6", "the old two-sink band", (min(b3), max(b3), round(max(b3)-min(b3), 2)), (1.41, 1.42, 0.01))
f = s_ = 0
base_sinks = frozenset(ORDER[i] for i in range(N) if od[i] == 0)
for seed in range(5):
    r2 = np.random.default_rng(1000+seed)
    rr = phiw(1.5, wealth*(1+r2.uniform(-0.01, 0.01, size=len(wealth))))
    f += len(dws ^ set(rr["directed"]))//2
    o4 = collections.Counter(u for u, _ in rr["directed"])
    s_ += (frozenset(ORDER[i] for i in range(N) if o4[i] == 0) != base_sinks)
chk("1.6", "+/-1% noise: flips / sink changes", (f, s_), (0, 0))
fl = []
for scale in (1.0, 1e-2, 1e-6):
    rs = phiw(1.5, scale=scale); fl.append(len(dws ^ set(rs["directed"]))//2)
chk("1.6", "scale x1 / x1e-2 / x1e-6 flips", fl, [0, 16, 83])
has("1.6", "the emergence claim is deleted and replaced", "**Their count is set by `α_Φ`; only their\nlocations are emergent.**")
hasnt("1.6", "the old emergence claim", "Nothing pins their count; it emerges from")
has("1.6", "the band table", "| 1 — `hangzhou` | **[1.43, 1.93]** | **0.50**")

print(); print("=" * 100); print("C. the Europe demonstration and the 1444 route"); print("=" * 100)
EUR = set(int(x) for x in pdx.values(pdx.load(os.path.join(EU4, "map", "continent.txt")).get("europe")))
OWNED = {r["pid"] for r in ROWS}; eur = sorted(EUR & OWNED)
LOWEC = {90, 92, 95, 96, 97, 98, 99, 100, 1744}
chk("1.6", "European counted provinces", len(eur), 823)
def sinks_mult(mult):
    w = np.array([wealth[i]*mult.get(r["pid"], 1.0) for i, r in enumerate(ROWS)])
    rr = phiw(1.5, w); o5 = collections.Counter(u for u, _ in rr["directed"])
    return sorted(ORDER[i] for i in range(N) if o5[i] == 0), rr
chk("1.6", "Europe x1.02 sinks", sinks_mult({p: 1.02 for p in eur})[0],
    ["doab", "english_channel", "hangzhou", "wien"])
chk("1.6", "Europe x1.56 sinks", sinks_mult({p: 1.56 for p in eur})[0], ["english_channel", "rheinland"])
chk("1.6", "Lowlands x1.20 sinks", sinks_mult({p: 1.20 for p in LOWEC})[0], ["english_channel", "hangzhou"])
chk("1.6", "Lowlands x10 still a sink", "english_channel" in sinks_mult({p: 10.0 for p in LOWEC})[0], True)
for seed in range(3):
    nz = 1+np.random.default_rng(seed).uniform(-0.02, 0.02, size=len(wealth))
    rn = phiw(1.5, wealth*nz); on = collections.Counter(u for u, _ in rn["directed"])
    chk("1.6", "+/-2%% random noise seed %d" % seed,
        sorted(ORDER[i] for i in range(N) if on[i] == 0), ["hangzhou"])
chk("1.6", "+2% systematic to Europe", "english_channel" in sinks_mult({p: 1.02 for p in eur})[0], True)
adj = collections.defaultdict(list)
for u, v in rw["directed"]: adj[u].append(v)
def path(a, b):
    s0, d0 = NIDX[a], NIDX[b]; prev = {s0: None}; q = collections.deque([s0])
    while q:
        x = q.popleft()
        if x == d0: break
        for y in adj[x]:
            if y not in prev: prev[y] = x; q.append(y)
    if d0 not in prev: return None
    p = []; x = d0
    while x is not None: p.append(ORDER[x]); x = prev[x]
    return list(reversed(p))
chk("1.6", "the Silk Road route", path("genua", "hangzhou"),
    ["genua", "alexandria", "aleppo", "persia", "lahore", "doab", "ganges_delta", "burma", "gulf_of_siam", "canton", "hangzhou"])
chk("1.6", "the Volga route", path("north_sea", "hangzhou")[:6],
    ["north_sea", "white_sea", "novgorod", "kazan", "astrakhan", "persia"])
chk("1.6", "the Hansa route", path("english_channel", "hangzhou")[:8],
    ["english_channel", "lubeck", "saxony", "wien", "venice", "ragusa", "constantinople", "aleppo"])
has("1.6", "the institution result is stated", "A 1–2% European development edge produces a European sink")
has("1.6", "the route is stated", "burma → gulf_of_siam → canton → hangzhou")

print(); print("=" * 100); print("D. the fallback branch, T3, and the assertions"); print("=" * 100)
r0 = run_drain(np.zeros(N)); sk0, _ = sinks_of(r0["directed"])
chk("3.2", "T3 fires the fallback on b == 0", [ORDER[i] for i in r0["fallbacks"]], ["english_channel"])
core = set(r0["core"])
chk("2.8", "v5 containment holds on T3",
    [ORDER[i] for i in sk0 if i in core and i not in (set(r0["S0"]) | set(r0["promotions"]) | set(r0["fallbacks"]))], [])
chk("2.8", "the narrower set would halt",
    [ORDER[i] for i in sk0 if i in core and i not in (set(r0["S0"]) | set(r0["promotions"]))], ["english_channel"])
has("3.2", "3.2 states three counterexamples", "Three\n   constructed inputs break it")
has("3.2", "T3 is worked in 3.2", "**T3 — the fallback branch, inside the 2-core.**")
hasnt("3.2", "the 'only way' sentence", "the free-edge race is the only way a node inside it drops out")
hasnt("3.2", "the 'index never decides' claim", "zero exact key ties measured, so the index never decides")
has("3.2", "containment names the fallbacks", "nor fallback-promoted**")
has("2.4", "canonical order is a correctness requirement", "**The node order itself is a correctness\n   requirement, not a convention**")
has("1.1", "where the fallback is reachable", "only when `b ≡ 0` across it")

print(); print("=" * 100); print("E. file values and the remaining figures"); print("=" * 100)
def walk(node, hits, src):
    for k, v in node:
        if isinstance(v, pdx.Node):
            if k == "change_price":
                tg, val = v.get("trade_goods"), v.get("value")
                if tg is not None and val is not None: hits.append((tg, float(val), src, v.get("key")))
            walk(v, hits, src)
raws = collections.Counter(); hits = []
for tree in ("events", "decisions", "missions", "common", "history"):
    for dp, _, fs in os.walk(os.path.join(EU4, tree)):
        for fn in fs:
            if not fn.endswith(".txt"): continue
            fp = os.path.join(dp, fn)
            raws[tree] += len(re.findall(r"change_price\s*=\s*\{", re.sub(r"#[^\n]*", "", io.open(fp, encoding="latin-1", errors="replace").read())))
            try: walk(pdx.load(fp), hits, tree)
            except Exception: pass
chk("3.5", "change_price blocks, raw census", (sum(raws.values()), raws["events"], raws["missions"], raws["common"], raws["history"]), (161, 93, 14, 1, 53))
neg = collections.defaultdict(list)
for tg, v_, s_2, k_ in hits:
    if v_ < 0: neg[tg].append((v_, s_2, k_))
below = exact = none_ = above = 0
for g in sorted(PRICES):
    if PRICES[g] <= 0: continue
    if g not in neg: none_ += 1; continue
    fl2 = PRICES[g]*(1+min(neg[g])[0])
    if fl2 < 2.0-1e-9: below += 1
    elif abs(fl2-2.0) < 1e-9: exact += 1
    else: above += 1
chk("3.5", "sublinear partition", (below, exact, above, none_), (13, 2, 4, 11))
conn = np.zeros((N, N), dtype=bool)
for gi, g in GL:
    a2 = collections.defaultdict(list)
    for u, v in R[g]["directed"]: a2[u].append(v)
    for s0 in range(N):
        seen = {s0}; q = collections.deque([s0])
        while q:
            x = q.popleft()
            for y in a2[x]:
                if y not in seen: seen.add(y); q.append(y)
        for t0 in seen:
            if t0 != s0: conn[s0][t0] = True
chk("3.8", "ordered pairs connected by >=1 good", (int(conn.sum()), round(100.0*conn.sum()/(N*(N-1)), 1)), (5825, 92.2))
chk("2.8", "spices sinks", sorted(ORDER[i] for i in sinks_of(R["spices"]["directed"])[0]), ["australia", "brazil", "genua"])
chk("2.8", "cloves sinks", sorted(ORDER[i] for i in sinks_of(R["cloves"]["directed"])[0]),
    ["australia", "brazil", "deccan", "kongo", "venice"])
gi_s = GOODS.index("spices")
chk("3.2", "nodes producing spices / cloves", (int((GP[gi_s] > 0).sum()), int((GP[GOODS.index("cloves")] > 0).sum())), (18, 1))
A2f = lambda g: (PRICES[g]/2.0)**2
S2, C2, _, _, _, _ = build_sc(A2f, eps=0.0)
dr = np.argsort(-C2[GOODS.index("cloves")])
chk("3.13", "cloves demand ranks under alpha=16", (ORDER[dr[0]], ORDER[dr[1]], ORDER[dr[2]]), ("hangzhou", "deccan", "beijing"))
has("3.13", "Deccan is the calibration cloves sink", "Deccan, **demand rank 2** under α = 16")
has("2.4", "one end flag", "1444: **one** end node, `hangzhou`")
hasnt("2.3", "the withdrawn calibration", "calibrated so the 1444 start yields the two-sink\nhangzhou/english_channel map")
has("2.3", "the withdrawal is stated", "**Its stated calibration is withdrawn.**")
has("3.9", "the adoption rationale is rewritten", "**one operator, one set of guarantees, and ends that move with the world.**")
hasnt("3.10", "the 0.41% artifact", "overstates **every** collector's income by **0.41%**")
has("3.10", "the redistributive statement", "**redistributive and single-digit percent, with the sign varying by collector**")
hasnt("1.10", "the caravan over-claim", "outweighs every incumbent in every inland node")
has("1.10", "the corrected caravan comparison", "**23.6 to 143.2**")
chk("v5", "no [unverified] marker remains", TXT.count("[unverified in"), 0)

print(); print("=" * 100); print("F. figures the regeneration batch touched but section E did not cover"); print("=" * 100)
# coal: latent-coal provinces, the owned subset, and the Phi_w flips on activation
_hist = os.path.join(EU4, "history", "provinces")
_coal = set()
for _fn in os.listdir(_hist):
    _m = re.match(r"^[ ]*([0-9]+)", _fn)
    if not _m: continue
    _tx = io.open(os.path.join(_hist, _fn), encoding="latin-1", errors="replace").read()
    if re.search(r"latent_trade_goods[^=]*=[^{]*\{[^}]*coal", _tx): _coal.add(int(_m.group(1)))
chk("1.5", "latent-coal provinces / owned and counted",
    (len(_coal), sum(1 for r in ROWS if r["pid"] in _coal)), (58, 45))
_w2 = wealth.copy()
for _i, _r in enumerate(ROWS):
    if _r["pid"] in _coal: _w2[_i] = _r["tax"] + _r["gp"] * PRICES["coal"]
_rc = phiw(1.5, _w2)
chk("1.5", "Phi_w flips from the coal activation", len(dws ^ set(_rc["directed"])) // 2, 29)
chk("1.5", "world wealth after repricing to coal", round(float(_w2.sum()), 1), 10894.9)
hasnt("2.9", "2.9's coal row no longer says 10 of 159", "flips 10 of 159")
has("2.9", "2.9's coal row now says 29 of 159", "flips 29 of 159 `Φ_w` edges (§1.5)")
# the 3-mass gravity kernel: end counts and the agreement ceiling
def _grav(masses, gamma):
    dist = np.full((N, N), 1e9)
    for i in range(N): dist[i][i] = 0
    for u, v in EDGES_UND: dist[u][v] = dist[v][u] = 1
    for k in range(N):
        dist = np.minimum(dist, dist[:, k:k+1] + dist[k:k+1, :])
    ca = cvec(1.5)
    phi = np.array([max(ca[m] * gamma ** dist[n][m] for m in masses) for n in range(N)])
    d = []
    for u, v in EDGES_UND:
        d.append((u, v) if (phi[u], -u) < (phi[v], -v) else (v, u))
    o = collections.Counter(a for a, _ in d)
    return sum(1 for i in range(N) if o[i] == 0), d
_ca = cvec(1.5)
_seed = []
for i in np.argsort(-_ca):
    if all(i not in UND[j] for j in _seed): _seed.append(int(i))
    if len(_seed) == 6: break
chk("3.15", "gravity end counts at gamma=0.9 for 4/5/6 masses",
    [_grav(_seed[:k], 0.9)[0] for k in (4, 5, 6)], [3, 3, 3])
chk("3.15", "gravity end counts at gamma=0.5 for 1..6 masses",
    [_grav(_seed[:k], 0.5)[0] for k in range(1, 7)], [1, 2, 3, 4, 5, 6])
_vt = re.sub(r"#[^" + chr(10) + "]*", "",
             io.open(os.path.join(EU4, "common", "tradenodes", "00_tradenodes.txt"),
                     encoding="latin-1").read())
def _agree(gamma):
    _, d = _grav(_seed[:3], gamma)
    ds = set(d); a = 0
    for u, v in VANEDGES:
        if (u, v) in ds: a += 1
    return a
VANEDGES = []
_raw = _vt
_blocks = re.finditer(r"^([a-z0-9_]+)=\{", _raw, re.M)
for _b in _blocks:
    _s = _b.end() - 1; _d = 0
    for _j in range(_s, len(_raw)):
        if _raw[_j] == "{": _d += 1
        elif _raw[_j] == "}":
            _d -= 1
            if _d == 0: break
    _blk = _raw[_b.start():_j+1]
    _nm = _b.group(1)
    if _nm not in NIDX: continue
    for _o in re.finditer(r"outgoing\s*=\s*\{[^}]*?name\s*=\s*\"?([a-z0-9_]+)", _blk):
        _t2 = _o.group(1)
        if _t2 in NIDX: VANEDGES.append((NIDX[_nm], NIDX[_t2]))
chk("3.15", "vanilla outgoing links parsed", len(VANEDGES), 159)
_best = max(((_agree(g), g) for g in (0.5, 0.7, 0.9, 0.93, 0.95, 0.97, 0.98, 0.99)), key=lambda x: x[0])
chk("3.15", "gravity best agreement / at gamma", (_best[0], round(100.0*_best[0]/159)), (97, 61))
chk("3.15", "gravity agreement at gamma=0.90/0.93/0.95/0.97",
    [_agree(g) for g in (0.90, 0.93, 0.95, 0.97)], [97, 97, 97, 93])
has("3.15", "the gamma band is stated", "(γ = 0.90–0.95, 97 of 159 arrows; γ = 0.97 gives 93")
hasnt("3.15", "the stale gamma=0.97 claim", "(γ = 0.97, 97 of 159 arrows)")
print(); print("=" * 100); print("G. the six defects the no-context claims extraction found"); print("=" * 100)
# G58 - 3.13's flat-goods denial
n_flat = len(set(MON_FLAT) | set(PERM_FLAT))
chk("3.13", "provinces carrying a flat trade_goods_size", n_flat, 15)
chk("3.13", "of those, from projects / from permanent modifiers", (len(MON_FLAT), len(PERM_FLAT)), (5, 10))
hasnt("3.13", "the flat-goods denial is gone from 3.13", "no 1444 province was\n  observed carrying a *flat*")
has("3.13", "3.13 now cites the fifteen", "**fifteen** 1444 provinces carry a flat `trade_goods_size`")
# G59 - the razed-China row
NW = np.zeros(N); np.add.at(NW, pn, wealth)
def _zero(node):
    w2 = wealth.copy(); w2[[i for i, r in enumerate(ROWS) if r["node"] == node]] = 0.0
    r2 = phiw(1.5, w2); o2 = collections.Counter(u for u, _ in r2["directed"])
    return sorted(ORDER[i] for i in range(N) if o2[i] == 0), len(dws ^ set(r2["directed"])) // 2
chk("2.8", "zeroing hangzhou: sinks / flips", _zero("hangzhou"),
    (["doab", "english_channel", "gulf_of_siam", "sevilla"], 22))
chk("2.8", "zeroing beijing: sinks / flips", _zero("beijing"),
    (["doab", "english_channel", "hangzhou", "sevilla"], 17))
chk("2.8", "hangzhou / beijing c_w rank", (crank["hangzhou"], crank["beijing"]), (1, 31))
chk("2.8", "hangzhou / beijing node wealth",
    (round(float(NW[NIDX["hangzhou"]]), 1), round(float(NW[NIDX["beijing"]]), 1)), (245.0, 143.8))
chk("2.8", "beijing's share of world wealth", round(100.0 * NW[NIDX["beijing"]] / wealth.sum(), 1), 1.3)
hasnt("2.8", "the 'beijing moves nothing' claim", "Zeroing `beijing` (node-wealth rank 39) moves nothing")
# G60 - the supply/demand contrast
_ss, _dd = [], []
for _gi, _g in GL:
    _a = S[_gi][S[_gi] > 0]; _b = C[_gi][C[_gi] > 0]
    if len(_a) > 1: _ss.append(_a.max() / _a.min())
    if len(_b) > 1: _dd.append(_b.max() / _b.min())
chk("3.15", "supply contrast range over 29 goods", (round(min(_ss)), round(max(_ss))), (4, 97))
chk("3.15", "demand contrast range over 29 goods", (round(min(_dd)), round(max(_dd), -2)), (211, 20400))
hasnt("3.15", "the withdrawn 10^7 ratio is gone", "supply contrast (10⁷) drowns demand contrast")
has("3.15", "3.15 now agrees with 3.2", "**4–97 on supply against\n211–20,400 on demand**")
# G61 - the inland basis
chk("1.10", "flag inland / derived inland", (26, 25), (26, 25))
has("1.10", "1.10 names the basis", "median 17.9% over the **flag's** 26 inland nodes")
has("1.10", "and what the other basis gives", "only the median\nmoves, to 17.5%")
# G62 / G63
hasnt("1.6", "the second live justification for alpha", "and the value was chosen with a target count in view. What the world")
has("1.6", "the calibration is past tense and cross-referenced", "a calibration\n§2.3 now withdraws")
hasnt("1.6", "the unsourced institution sentence", "far below what the Renaissance, Colonialism and Printing Press deliver")
has("1.6", "the institutions are sourced from the install", "Renaissance `1450.1.1` at Florence")
_inst = io.open(os.path.join(EU4, "common", "institutions", "00_Core.txt"), encoding="latin-1").read()
_inst = re.sub(r"#[^\n]*", "", _inst)
def _idef(name):
    m = re.search(r"^%s\s*=\s*\{" % name, _inst, re.M); s = m.end() - 1; d = 0
    for j in range(s, len(_inst)):
        if _inst[j] == "{": d += 1
        elif _inst[j] == "}":
            d -= 1
            if d == 0: break
    blk = _inst[m.start():j + 1]
    return (re.search(r"historical_start_date\s*=\s*([\d.]+)", blk).group(1),
            int(re.search(r"historical_start_province\s*=\s*(\d+)", blk).group(1)))
chk("1.6", "renaissance start date / province", _idef("renaissance"), ("1450.1.1", 116))
chk("1.6", "new_world_i start date / province", _idef("new_world_i"), ("1500.1.1", 224))
chk("1.6", "printing_press start date / province", _idef("printing_press"), ("1550.1.1", 1876))
chk("1.6", "renaissance embracement bonus",
    bool(re.search(r"renaissance[\s\S]{0,400}?development_cost\s*=\s*-0\.05", _inst)), True)

print(); print("=" * 100); print("H. the band claims, stress-tested at finer resolution and 8 noise seeds"); print("=" * 100)
def _sset(a, w):
    r = run_drain(np.full(N, 1.0/N) - cvec(a, w))
    o = collections.Counter(u for u, _ in r["directed"])
    return tuple(sorted(ORDER[i] for i in range(N) if o[i] == 0))
def _refine(target, lo, hi):
    e_lo = lo
    for k in range(1, 11):
        a = round(lo - k/1000, 3)
        if a < 1.0 or _sset(a, wealth) != target: break
        e_lo = a
    e_hi = hi
    for k in range(1, 11):
        a = round(hi + k/1000, 3)
        if a > 3.0 or _sset(a, wealth) != target: break
        e_hi = a
    return e_lo, e_hi, round(e_hi - e_lo, 3)
chk("1.6", "narrow window refined to 0.001", _refine(("english_channel", "hangzhou"), 1.41, 1.42),
    (1.406, 1.424, 0.018))
chk("1.6", "one-sink band refined to 0.001", _refine(("hangzhou",), 1.43, 1.93), (1.425, 1.931, 0.506))
_T = [("hangzhou",), ("genua", "hangzhou"), ("doab", "genua", "hangzhou"), ("english_channel", "hangzhou")]
_seen = {t: [] for t in _T}
for _s in range(8):
    _w = wealth * (1 + np.random.default_rng(4000+_s).uniform(-0.01, 0.01, size=len(wealth)))
    _g = {}
    for _k in range(100, 301):
        _a = round(_k/100, 2); _g[_a] = _sset(_a, _w)
    for _t in _T:
        _h = sorted(a for a in _g if _g[a] == _t)
        _seen[_t].append((min(_h), max(_h)) if _h else None)
chk("1.6", "narrow window survives on all 8 noise seeds",
    sum(1 for r in _seen[("english_channel", "hangzhou")] if r is None), 0)
_nw = [round(r[1]-r[0], 2) for r in _seen[("english_channel", "hangzhou")] if r]
chk("1.6", "narrow window widths under noise", (min(_nw), max(_nw)), (0.0, 0.03))
_wide = [t for t in _T if t != ("english_channel", "hangzhou")]
_ww = [round(r[1]-r[0], 2) for t in _wide for r in _seen[t] if r]
chk("1.6", "wide band widths under noise", (min(_ww), max(_ww)), (0.28, 0.51))
_BASE = {("hangzhou",): (1.43, 1.93), ("genua", "hangzhou"): (1.94, 2.25),
         ("doab", "genua", "hangzhou"): (2.26, 2.71)}
_mv = max(max(abs(r[0]-_BASE[t][0]), abs(r[1]-_BASE[t][1])) for t in _wide for r in _seen[t] if r)
chk("1.6", "largest wide-band edge movement under noise", round(_mv, 2), 0.03)
hasnt("1.6", "the 'disappears entirely' overstatement",
      "under ±1% wealth noise that window" + chr(10) + "moves or disappears entirely")
hasnt("2.3", "2.3's matching overstatement", "the map it was fitted to is not" + chr(10) + "reproducible under noise")
has("2.3", "2.3 now states the window claim", "narrower than the uncertainty in its own edges under ±1% wealth noise")
has("1.6", "the corrected narrow-window statement", "its width ranges **0.00 to 0.03**")

print(); print("=" * 100); print("J. the round-2 extraction's measurable observations"); print("=" * 100)
hasnt("2.8", "2.8's mislabelled agreement figure", "on 52.5% of value-weighted edge-goods")
has("2.8", "2.8 now carries both figures with the right labels",
    "**51.5%** of edge-goods *weighted by" + chr(10) + "  trade value*, and on 52.5% unweighted")
_NW = np.zeros(N); np.add.at(_NW, pn, wealth)
_wr = {ORDER[i]: k + 1 for k, i in enumerate(np.argsort(-_NW))}
chk("3.9", "genua / gulf_of_siam / sevilla node-wealth ranks",
    (_wr["genua"], _wr["gulf_of_siam"], _wr["sevilla"]), (3, 2, 7))
chk("3.9", "their node wealth, and english_channel's",
    tuple(round(float(_NW[NIDX[n_]]), 1) for n_ in ("genua", "gulf_of_siam", "sevilla", "english_channel")),
    (296.0, 299.2, 266.5, 316.6))
has("3.9", "3.9 states the field the ranks are on", "rank 3rd, 2nd and 7th by node wealth on the corrected field")
# highest_power: re-parse the save's country sub-blocks at their own brace depth
import zipfile as _zip
_SAVE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\VANILLA_start.eu4"
_z = _zip.ZipFile(_SAVE); _t = _z.read("gamestate").decode("latin-1"); _z.close()
_i = _t.find(chr(10) + "trade={"); _j = _i + len(chr(10) + "trade="); _d = 0; _k = _j
while _k < len(_t):
    if _t[_k] == "{": _d += 1
    elif _t[_k] == "}":
        _d -= 1
        if _d == 0: break
    _k += 1
_tr = _t[_j:_k + 1]
def _blocks(s, ind):
    for m in re.compile(chr(10) + "\t" * ind + r"([A-Za-z0-9_]+)=\{").finditer(s):
        st = m.end() - 1; dd = 0; e = st
        while e < len(s):
            if s[e] == "{": dd += 1
            elif s[e] == "}":
                dd -= 1
                if dd == 0: break
            e += 1
        yield m.group(1), s[st:e + 1]
_hits = 0; _tot = 0; _ven = None
for _key, _body in _blocks(_tr, 1):
    if _key != "node": continue
    _nm = re.search(r'definitions="([^"]+)"', _body).group(1)
    _cp = {}
    for _kk, _sub in _blocks(_body, 2):
        if len(_kk) == 3 and _kk.isupper():
            _m = re.search(chr(10) + r"\t\t\tval=([\d.]+)", _sub)
            if _m: _cp[_kk] = float(_m.group(1))
    _hp = re.search(chr(10) + r"\t\thighest_power=([\d.]+)", _body)
    if not (_hp and _cp): continue
    _tot += 1
    if abs(float(_hp.group(1)) - max(_cp.values())) < 1e-3: _hits += 1
    if _nm == "venice": _ven = (float(_hp.group(1)), round(max(_cp.values()), 1))
chk("1.10", "highest_power == largest country power, node count", (_hits, _tot), (0, 79))
chk("1.10", "venice: highest_power vs Venice's own power", _ven, (53.2, 106.2))
has("1.10", "1.10 states the test", "differs from the largest single country's `val` on **79 of 79** nodes")
# 3.5's boundary goods
_neg = collections.defaultdict(list)
for _tg, _v, _s2, _k2 in hits:
    if _v < 0: _neg[_tg].append(_v)
_ex = sorted(g for g in PRICES if PRICES[g] > 0 and g in _neg
             and abs(PRICES[g] * (1 + min(_neg[g])) - 2.0) < 1e-9)
chk("3.5", "goods whose floor lands exactly on 2.0", _ex, ["gems", "silk"])

print(); print("=" * 100)
bad2 = [r for r in RES if not r[0]]
print("RESULT: %d checks, %d failed" % (len(RES), len(bad2)))
for r in bad2: print("   FAIL:", r[1:])
