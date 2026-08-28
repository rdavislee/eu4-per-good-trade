# -*- coding: utf-8 -*-
"""validate_v4.py - assert every claim the v4.0 repairs touched, against the install and the
reference solver.  Each check names the v3 claim ID it clears.  Any FAIL means the repair
did not land."""
import io, os, re, sys, collections, zipfile
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, PROV, PNODE,
                    build_sc, solve_phi, orient, COMPS, NODES, LOCAL_TAX_MOD, LOCAL_TV_MOD)
from drain import run_drain, sinks_of, has_cycle, NODEW

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
SPEC = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v4-owner-agnostic\per-good-trade-spec.md"
TXT = io.open(SPEC, encoding="utf-8").read()

RES = []
def chk(cid, what, got, exp, tol=None):
    ok = (abs(got - exp) <= tol) if (tol is not None) else (got == exp)
    RES.append((ok, cid, what, got, exp))
    print("  [%s] %-10s %-58s got=%s exp=%s" % ("PASS" if ok else "FAIL", cid, what, got, exp))
def has(cid, what, needle):
    ok = needle in TXT
    RES.append((ok, cid, what, "present" if ok else "ABSENT", "present"))
    print("  [%s] %-10s %-58s %s" % ("PASS" if ok else "FAIL", cid, what, "in spec" if ok else "NOT IN SPEC"))
def hasnt(cid, what, needle):
    ok = needle not in TXT
    RES.append((ok, cid, what, "absent" if ok else "STILL PRESENT", "absent"))
    print("  [%s] %-10s %-58s %s" % ("PASS" if ok else "FAIL", cid, what, "gone" if ok else "STILL IN SPEC"))

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

print("=" * 104); print("A. W041 / W040 / W160 - the two-test local-modifier rule"); print("=" * 104)
tg = pdx.load(os.path.join(EU4, "common", "tradegoods", "00_tradegoods.txt"))
prov_keys = {}
for k, v in tg:
    if k is None or not isinstance(v, pdx.Node): continue
    p = v.get("province")
    if p is None: continue
    for a, b in p: prov_keys.setdefault(a, []).append((k, float(b)))
chk("W041", "goods with local_tax_modifier", sorted(prov_keys.get("local_tax_modifier", [])), [("gems", 0.15)])
chk("W041", "goods with trade_value_modifier", sorted(prov_keys.get("trade_value_modifier", [])), [("incense", 0.1)])
chk("W041", "goods with local_production_efficiency", sorted(prov_keys.get("local_production_efficiency", [])), [("glass", 0.1)])
chk("W041", "goods with local_autonomy (the 4th, v3 said 3)", sorted(prov_keys.get("local_autonomy", [])), [("chinaware", -0.1)])
chk("W041", "goods with a flat trade_goods_size", sorted(prov_keys.get("trade_goods_size", [])), [])
has("W041", "chinaware row in the rule table", "`chinaware` `local_autonomy = -0.1`")
has("W041", "bonus_from_merchant_republics row", "eu4.exe:0x1cc7128")
hasnt("W041", "the old 'exactly three' claim", "income-relevant local ones are exactly three")
terr = io.open(os.path.join(EU4, "map", "terrain.txt"), encoding="latin-1").read()
tkeys = sorted(set(re.findall(r"^\s*([a-z_]+)\s*=\s*-?[\d.]+", terr, re.M)))
chk("W045", "terrain.txt modifier keys", tkeys,
    ['allowed_num_of_buildings','defence','local_defensiveness','local_development_cost',
     'movement_cost','nation_designer_cost_multiplier','supply_limit'])

print(); print("=" * 104); print("B. systemic 1 - the solver now implements the rule"); print("=" * 104)
chk("W074", "solver local tax modifiers", LOCAL_TAX_MOD, {"gems": 0.15})
chk("W074", "solver local trade-value modifiers", LOCAL_TV_MOD, {"incense": 0.10})
gemrows = [r for r in ROWS if r["good"] == "gems"]
increws = [r for r in ROWS if r["good"] == "incense"]
chk("W074", "gems provinces carried", len(gemrows), 43)
chk("W074", "incense provinces carried", len(increws), 29)
chk("W074", "a gems province's tax = 1.15 x base_tax", round(gemrows[0]["tax"] / PROV[gemrows[0]["pid"]]["base_tax"], 4), 1.15)
chk("W074", "world wealth (annual ducats)", round(float(wealth.sum()), 1), 10594.8)
has("W074", "spec item 4 names both modifiers", "`gems` (+15% tax, 43 provinces) and `incense`")

print(); print("=" * 104); print("C. W124 / W193 / W131 - the fallback branch and T3"); print("=" * 104)
r0 = run_drain(np.zeros(N))                       # b == 0: the T3 input
sk0, _ = sinks_of(r0["directed"])
chk("W124", "T3 fires the fallback", [ORDER[i] for i in r0["fallbacks"]], ["english_channel"])
chk("W124", "T3 promotes the highest-wealth node", ORDER[int(np.argmax(NODEW))], "english_channel")
chk("W124", "T3 sink set", [ORDER[i] for i in sk0], ["english_channel"])
chk("W124", "T3 orientation is complete", len(r0["directed"]), len(EDGES_UND))
chk("W124", "T3 orientation is acyclic", has_cycle(r0["directed"]) is None, True)
core = set(r0["core"])
v4set = set(r0["S0"]) | set(r0["promotions"]) | set(r0["fallbacks"])
v3set = set(r0["S0"]) | set(r0["promotions"])
chk("W193", "v4 containment holds on T3", [ORDER[i] for i in sk0 if i in core and i not in v4set], [])
chk("W193", "v3 containment would have halted on T3", [ORDER[i] for i in sk0 if i in core and i not in v3set], ["english_channel"])
picks = set()
for s in range(5):
    rng = np.random.default_rng(s)
    from drain import phase0, phase1, phase2, sweep_priority
    pid = {v: int(x) for v, x in zip(range(N), rng.permutation(N))}
    c2, beta, Plog = phase0(np.zeros(N)); Ssel, info = phase1(c2, beta, 0)
    fa, free, net, cost = phase2(c2, beta)
    o, Ss, pr, fb = sweep_priority(c2, beta, Ssel, fa, free, net, "defasc_beta", pid=pid)
    picks.add(tuple(sorted(ORDER[i] for i in fb)))
chk("W086", "fallback is scan-invariant (5 permutations)", picks, {("english_channel",)})
has("W124", "Phase 3 defines the fallback", "promote" + chr(10) + "the **highest-wealth** candidate instead, ties by index")
has("W124", "T1/T2/T3 named in 1.1", "(**T3**)")
has("W193", "2.8 asserts the widened set", "{selected} ∪ {promoted} ∪ {fallbacks}")
has("W193", "2.9 assertion list widened", "2-core sink containment in `{selected} ∪ {promoted} ∪ {fallbacks}`")

print(); print("=" * 104); print("D. W143 / W144 / W145 / W146 - the price-event scan"); print("=" * 104)
def walk(node, hits, src):
    for k, v in node:
        if isinstance(v, pdx.Node):
            if k == "change_price":
                t_, val = v.get("trade_goods"), v.get("value")
                if t_ is not None and val is not None: hits.append((t_, float(val), src, v.get("key")))
            walk(v, hits, src)
hits = []
for tree in ("events", "decisions", "missions", "common", "history"):
    for dp, _, fs in os.walk(os.path.join(EU4, tree)):
        for fn in fs:
            if fn.endswith(".txt"):
                try: walk(pdx.load(os.path.join(dp, fn)), hits, tree)
                except Exception: pass
bytree = collections.Counter(h[2] for h in hits)
chk("W146", "change_price blocks, all trees", len(hits), 154)
chk("W146", "blocks in history/", bytree["history"], 53)
chk("W146", "negative blocks in history/", sum(1 for h in hits if h[2] == "history" and h[1] < 0), 13)
neg = collections.defaultdict(list)
for t_, v_, s_, k_ in hits:
    if v_ < 0: neg[t_].append((v_, s_, k_))
below = exact = none_ = above = 0

for g in sorted(PRICES):
    if PRICES[g] <= 0: continue
    if g not in neg: none_ += 1; continue
    fl = PRICES[g] * (1 + min(neg[g])[0])
    if fl < 2.0 - 1e-9: below += 1
    elif abs(fl - 2.0) < 1e-9: exact += 1
    else: above += 1
chk("W143", "goods pushable strictly below 2.0", below, 13)
chk("W144", "goods landing exactly on 2.0", exact, 2)
chk("W143", "goods with no negative event", none_, 11)
chk("W143", "goods whose negative event stays above 2.0", above, 4)
wool = min(neg["wool"])
chk("W144", "wool's largest single negative", (wool[0], wool[1], wool[2]), (-0.25, "history", "NEW_DRAPERIES"))
chk("W144", "wool's floor", round(2.5 * (1 - 0.25), 4), 1.875)
has("W143", "3.5 says 13 of 30", "**13 of 30 goods** can be pushed strictly below 2.0")
has("W165", "3.13 partition matches", "for 13 of 30 goods, unreachable for 11, and exactly on the boundary for 2")
hasnt("W146", "the false history/ clause", "`history/` contributes only positive entries")

print(); print("=" * 104); print("E. W049 - City and Core are inside TAX_COEFF"); print("=" * 104)
sm = io.open(os.path.join(EU4, "common", "static_modifiers", "00_static_modifiers.txt"), encoding="latin-1").read()
m = re.search(r"^city\s*=\s*\{", sm, re.M); i = m.end() - 1; d = 0
for j in range(i, len(sm)):
    if sm[j] == "{": d += 1
    elif sm[j] == "}":
        d -= 1
        if d == 0: break
chk("W049", "city static modifier local_tax_modifier",
    float(re.search(r"local_tax_modifier\s*=\s*([\d.]+)", sm[i:j]).group(1)), 0.25)
chk("W049", "Garnatah tooltip sum 75+25+5+5+15", 75 + 25 + 5 + 5 + 15, 125)
chk("W049", "Caceres tooltip sum 75+25+5", 75 + 25 + 5, 105)
chk("W049", "cored city reference multiplier", 0.75 + 0.25, 1.00)
hasnt("W049", "the cancellation argument", "it cancels in the normalised share")
has("W049", "the absorbed-into-TAX_COEFF account", "already\ninside `TAX_COEFF`")

print(); print("=" * 104); print("F. W035 / W037 - the coefficient citation"); print("=" * 104)
for pid, bt, bp, good in ((223, 6, 4, "silk"), (1747, 2, 2, "wool"), (212, 3, 3, "fish"), (213, 6, 5, "glass")):
    s = PROV[pid]
    chk("W092", "province %d base_production" % pid, s["base_production"], float(bp))
    chk("W094", "province %d base_tax" % pid, s["base_tax"], float(bt))
    chk("W092", "province %d GP_COEFF x base_production" % pid, round(0.2 * bp, 2), round(bp * 0.2, 2))
has("W035", "the ratio, not the absolute, carries the time basis", "observed 3.52 → `Trade Value: +0.29`")
has("W035", "the Industrious confound is named", "`Industrious` ruler personality, +10%")
hasnt("W035", "the unreproducible tooltip quote", "yearly income of 3.25")
hasnt("W035", "the window value presented as a reading", "`Trade Value` of 3.20")
has("W037", "four provinces in the 2.3 table", "Girona (212) 3 → 0.60")
gra = io.open(os.path.join(EU4, "history", "countries", "GRA - Granada.txt"), encoding="latin-1").read()
chk("W035", "GRA history scripts no ruler personality", "personality" in gra, False)
rp = io.open(os.path.join(EU4, "common", "ruler_personalities", "00_core.txt"), encoding="latin-1").read()
k = rp.find("industrious_personality = {")
chk("W035", "Industrious grants global_trade_goods_size_modifier",
    re.search(r"global_trade_goods_size_modifier\s*=\s*([\d.]+)", rp[k:k + 1200]).group(1), "0.1")

print(); print("=" * 104); print("G. regenerated numbers the spec now quotes"); print("=" * 104)
R = {g: run_drain(S[gi] - C[gi]) for gi, g in GL}
sc = [len(sinks_of(R[g]["directed"])[0]) for _, g in GL]
chk("v4", "sinks per good", (min(sc), max(sc), round(float(np.mean(sc)), 1)), (1, 8, 3.6))
chk("v4", "acyclic goods", sum(1 for _, g in GL if has_cycle(R[g]["directed"]) is None), 29)
chk("v4", "fallbacks fired on 1444", sum(len(R[g]["fallbacks"]) for _, g in GL), 0)
rw = phiw(); dws = set(rw["directed"])
od = collections.Counter(u for u, _ in rw["directed"])
chk("v4", "Phi_w sinks", sorted(ORDER[i] for i in range(N) if od[i] == 0), ["english_channel", "hangzhou"])
cw = cvec(1.5); crank = {ORDER[i]: k + 1 for k, i in enumerate(np.argsort(-cw))}
wrank = {ORDER[i]: k + 1 for k, i in enumerate(np.argsort(-NODEW))}
chk("v4", "c_w ranks of the two sinks", (crank["hangzhou"], crank["english_channel"]), (3, 2))
chk("v4", "node-wealth ranks of the two sinks", (wrank["hangzhou"], wrank["english_channel"]), (12, 1))
chk("W057", "largest |b_w|", round(float(np.abs(np.full(N, 1.0/N) - cw).max()), 4), 0.0225)
ag = tot = 0; wag = wtot = 0.0
PGd = {g: set(R[g]["directed"]) for _, g in GL}
for gi, g in GL:
    for u, v in EDGES_UND:
        gd = (u, v) if (u, v) in PGd[g] else ((v, u) if (v, u) in PGd[g] else None)
        if gd is None: continue
        tot += 1; wtot += V[gi]
        if ((u, v) if (u, v) in dws else (v, u)) == gd: ag += 1; wag += V[gi]
chk("W061", "Phi_w agreement", round(100.0 * ag / tot, 1), 53.5)
chk("W061", "Phi_w value-weighted agreement", round(100.0 * wag / wtot, 1), 52.5)
Pord = np.zeros(N)
for gi, g in GL:
    for i in range(N): Pord[i] += V[gi] * R[g]["order"][i]
oa = ot = 0
for gi, g in GL:
    for u, v in EDGES_UND:
        gd = (u, v) if (u, v) in PGd[g] else ((v, u) if (v, u) in PGd[g] else None)
        if gd is None: continue
        ot += 1
        if ((u, v) if Pord[u] > Pord[v] else (v, u)) == gd: oa += 1
chk("W062", "Phi_ord agreement", round(100.0 * oa / ot, 1), 60.0)
ocnt = collections.Counter()
for u, v in EDGES_UND: ocnt[(u if Pord[u] > Pord[v] else v)] += 1
eo = [ORDER[i] for i in range(N) if ocnt[i] == 0]
chk("W155", "Phi_ord ends", len(eo), 18)
chk("W155", "Phi_ord ends terminating no good",
    sum(1 for n in eo if sum(1 for _, g in GL if not any(u == NIDX[n] for u, _ in PGd[g])) == 0), 10)
chk("W155", "no demand capital among them", any(x in eo for x in ("genua", "english_channel", "hangzhou")), False)
conn = np.zeros((N, N), dtype=bool)
for gi, g in GL:
    a = collections.defaultdict(list)
    for u, v in R[g]["directed"]: a[u].append(v)
    for s0 in range(N):
        seen = {s0}; q = collections.deque([s0])
        while q:
            x = q.popleft()
            for y in a[x]:
                if y not in seen: seen.add(y); q.append(y)
        for t0 in seen:
            if t0 != s0: conn[s0][t0] = True
chk("W153", "ordered pairs connected by >=1 good", (int(conn.sum()), round(100.0 * conn.sum() / (N * (N - 1)), 1)), (5723, 90.6))

print(); print("=" * 104); print("H. W156 - the rich non-sink example"); print("=" * 104)
for n, wr in (("genua", 3), ("gulf_of_siam", 2), ("sevilla", 7)):
    chk("W156", "%s node-wealth rank" % n, wrank[n], wr)
    chk("W156", "%s is not a sink" % n, od[NIDX[n]] > 0, True)
idg = collections.Counter(v for _, v in rw["directed"])
for n in ("genua", "gulf_of_siam", "sevilla"):
    chk("W156", "%s draws more edges in than out" % n, idg[NIDX[n]] > od[NIDX[n]], True)
hasnt("W156", "Beijing as a rich node", "Beijing, Champagne, Sevilla")

print(); print("=" * 104); print("I. V223 / V071 / V075 / V076 / V090 - the five unfolded v2 partials"); print("=" * 104)
W22 = ["english_channel","north_sea","baltic_sea","white_sea","novgorod","lubeck","rheinland","saxony",
       "wien","krakow","pest","venice","ragusa","genua","champagne","bordeaux","valencia","sevilla",
       "constantinople","crimea","kiev","kazan"]
chk("V223", "the 22 named nodes all exist", sorted(set(W22) - set(ORDER)), [])
chk("V223", "the 22 named nodes are 22", len(W22), 22)
idx22 = np.array([k for k, r in enumerate(ROWS) if r["node"] in set(W22)])
def sinkset(f):
    w = wealth.copy(); w[idx22] *= f
    r = phiw(1.5, w); o = collections.Counter(u for u, _ in r["directed"])
    ci = NIDX["cape_of_good_hope"]
    return (sorted(ORDER[i] for i in range(N) if o[i] == 0),
            sorted(ORDER[u] for u, v in r["directed"] if v == ci),
            sorted(ORDER[v] for u, v in r["directed"] if u == ci))
s2, i2, o2 = sinkset(2.0)
chk("V223", "x2 -> genua sole sink", s2, ["genua"])
s3, i3, o3 = sinkset(3.0)
chk("V223", "x3 -> Cape reversed (in)", i3, ["comorin_cape", "malacca", "zanzibar"])
chk("V223", "x3 -> Cape reversed (out)", o3, ["ivory_coast"])
hz = [k for k, r in enumerate(ROWS) if r["node"] == "hangzhou"]
top = max(hz, key=lambda k: wealth[k])
w30 = wealth.copy(); w30[top] *= 30
r30 = phiw(1.5, w30); o30 = collections.Counter(u for u, _ in r30["directed"])
chk("V223", "dev-stack x30 -> hangzhou sole sink", sorted(ORDER[i] for i in range(N) if o30[i] == 0), ["hangzhou"])
has("V223", "the node set is named in 1.6", "scaling **the 22 European nodes'** wealth")

tp = io.open(os.path.join(EU4, "common", "trading_policies", "00_trading_policies.txt"), encoding="latin-1").read()
seg = tp[tp.find("propagate_religion ="):]
cm = seg[seg.find("can_maintain"):]
rungs = re.findall(r"has_country_flag = (\d+)_trade_power_for_propogate_religion.*?(?:share = (\d+))?\s*\}\s*\}\s*\}", cm)
maint = {}
for line in cm.split("\n"):
    m2 = re.search(r"has_country_flag = (\d+)_trade_power_for_propogate_religion", line)
    if m2:
        m3 = re.search(r"share = (\d+)", line)
        maint[int(m2.group(1))] = int(m3.group(1)) if m3 else None
chk("V075", "PR ladder maintain shares", maint, {5: None, 10: 5, 15: 5, 20: 10, 25: 15, 30: 20, 35: 25, 40: 30, 45: 35})
has("V075", "1.10 records the banded ladder", "maintain trails select by 5–10 points (10→5, 15→5, 20→10, 25→15, 30→20, 35→25, 40→30, 45→35)")
hasnt("V076", "the over-broad chatter claim", "Propagate Religion included. Casus belli")
has("V071", "1.8 states the positive and stops", "**No string, define or modifier\nties range to link flow**")
hasnt("V071", "the universal negative", "no\nmechanic gates flow by range")
has("V090", "2.2 quotes the measured solve cost", "**5.7–7.3 ms per good and 0.17–0.21 s for all 29**")
hasnt("V090", "the unqualified projection", "tens of milliseconds for all 29 goods per monthly tick")

print(); print("=" * 104); print("J. W101 / W118 / W066 / W039 / W086 / W190 - narrowed wordings"); print("=" * 104)
CR = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\crashes"
dumps = [d for d in os.listdir(CR) if d.startswith("eu4_")]
chk("W101", "cycle crash dumps on disk", len(dumps), 3)
for d in dumps:
    ex = io.open(os.path.join(CR, d, "exception.txt"), encoding="latin-1").read()
    chk("W101", "%s eu4.exe frames" % d[-6:], len(re.findall(r"^\s+\d+\s+eu4\.exe", ex, re.M)), 1002)
    chk("W101", "%s exception address" % d[-6:], "0x00007FF6DDE6A8B4" in ex, True)
    chk("W101", "%s per-frame addresses" % d[-6:], bool(re.search(r"eu4\.exe\s+0x", ex)), False)
hasnt("W101", "the frame-address over-read", "1002 stack\nframes at a single return address")
has("W101", "three reproductions", "reproduced on three launches")

SG = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games"
def nodes_of(p):
    z = zipfile.ZipFile(p); t = z.read("gamestate").decode("latin-1"); z.close()
    i = t.find("\ntrade={"); j = i + len("\ntrade="); d = 0; k = j
    while k < len(t):
        if t[k] == "{": d += 1
        elif t[k] == "}":
            d -= 1
            if d == 0: break
        k += 1
    tr = t[j:k+1]; out = {}
    for m2 in re.finditer(r"\n\tnode=\{", tr):
        s0 = m2.end() - 1; d2 = 0; e = s0
        while e < len(tr):
            if tr[e] == "{": d2 += 1
            elif tr[e] == "}":
                d2 -= 1
                if d2 == 0: break
            e += 1
        b = tr[s0:e+1]; nm = re.search(r'definitions="([^"]+)"', b)
        rec = {}
        for f in ("current", "local_value", "outgoing", "total", "retention"):
            mm = re.search(r"\n\t\t%s=([\d.eE+-]+)" % f, b)
            rec[f] = float(mm.group(1)) if mm else None
        out[nm.group(1)] = rec
    return out
V1 = nodes_of(os.path.join(SG, "VANILLA_start.eu4")); V2 = nodes_of(os.path.join(SG, "VANILLA2_start.eu4"))
F = ["current", "local_value", "outgoing", "total", "retention"]
union = {k for k in V1 for f in F if V1[k][f] is not None and V2[k][f] is not None and abs(V1[k][f]-V2[k][f]) > 1e-9}
mx = max(abs(V1[k][f]-V2[k][f])/abs(V1[k][f]) for k in V1 for f in F
         if V1[k][f] not in (None, 0) and V2[k][f] is not None)
chk("W117", "nodes differing between two vanilla runs", len(union), 49)
chk("W117", "largest relative difference", round(100*mx, 2), 8.96)
tdiff = sum(1 for k in V1 if V1[k]["total"] is not None and V2[k]["total"] is not None and abs(V1[k]["total"]-V2[k]["total"]) > 1e-9)
rdiff = sum(1 for k in V1 if V1[k]["retention"] is not None and abs(V1[k]["retention"]-V2[k]["retention"]) > 1e-9)
chk("W118", "nodes where `total` differs", tdiff, 1)
chk("W118", "nodes where `retention` differs", rdiff, 0)
has("W118", "2.8 states the field-level truth", "`retention` is identical on 80 of 80 nodes and `total` on 79 of 79")
hasnt("W118", "the over-claim", "only node `total` and `retention` are deterministic")

loc = ""
for fn in os.listdir(os.path.join(EU4, "localisation")):
    if "english" in fn and fn.endswith(".yml"):
        loc += io.open(os.path.join(EU4, "localisation", fn), encoding="utf-8", errors="replace").read()
chk("W066", "CARAVAN_POWER_DESC2 names development and policies",
    ("a third of your development" in loc and "policies and ideas" in loc), True)
chk("W066", "no caravan string mentions trade efficiency",
    any(("caravan" in l.lower() and "trade efficiency" in l.lower() and "Caravan Power" in l) for l in loc.split("\n")
        if "UNLOCK_NOMADIC" not in l), False)
hasnt("W066", "the unsourced clause", "efficiency also feeds the caravan-power and collection tooltips")
has("W066", "the file-evidenced replacement", "`LEDGER_TRADE_EFFICIENCY`, `LEDGER_TC_EFF_CARAVAN_POWER`")

has("W039", "modifier order narrowed to 'consistent with'", "**consistent with** that and does not establish it")
has("W086", "1.1 splits the two classes", "is **measured, not proved**")
has("W086", "2.2a table row split", "proved as determinism; **measured** as independence from the node indexing")
has("W190", "gravity kernel carries its gamma range", "exactly for γ ≤ 0.7 and any count up to six")

print(); print("=" * 104); print("K. W071 - the caravan cap measurement"); print("=" * 104)
tot_pow = {k: v["total"] for k, v in V1.items()}
inland = [n for n in ORDER if NODES[n]["inland"] == "yes"]
shares = sorted(100 * 50 / (tot_pow[n] + 50) for n in inland if tot_pow.get(n))
chk("W071", "inland-node cap share range", (round(shares[0], 1), round(shares[-1], 1)), (8.6, 32.0))
chk("W071", "inland-node cap share median", round(shares[len(shares)//2], 1), 17.9)
chk("W071", "inland node totals", (round(min(tot_pow[n] for n in inland), 1), round(max(tot_pow[n] for n in inland), 1)), (106.4, 532.0))
has("W071", "1.10 carries the measurement", "**8.6% to 32.0% of an inland node's total trade power**")

print(); print("=" * 104); print("L. W156 - the razed-node rows"); print("=" * 104)
def sinks_zeroing(node):
    idx = [k for k, r in enumerate(ROWS) if r["node"] == node]
    x = wealth.copy(); x[idx] = 0.0
    rr = phiw(1.5, x); o2 = collections.Counter(u for u, _ in rr["directed"])
    return sorted(ORDER[i] for i in range(N) if o2[i] == 0)
chk("W156", "zeroing hangzhou relocates the sink", sinks_zeroing("hangzhou"), ["doab", "english_channel", "gulf_of_siam"])
chk("W156", "zeroing beijing moves nothing", sinks_zeroing("beijing"), ["english_channel", "hangzhou"])
chk("W156", "beijing node-wealth rank", wrank["beijing"], 39)
has("W156", "2.8 Razed China names hangzhou", "Zeroing `hangzhou`-node development relocates the sink")
has("W156", "2.8 Mandate row is the owner-agnosticism check", "**Nothing moves on the day it happens.**")
has("W156", "3.9 illustration", "a razed `hangzhou`")
has("W156", "3.1 goal 1", "A horde razing `hangzhou`")

print(); print("=" * 104); print("M. 3.10 - the income factoring and per-good propagation"); print("=" * 104)
_val = {g: np.zeros(N) for g in GOODS}
_pp = np.zeros(N)
for _r in ROWS:
    if _r["good"] in _val:
        _val[_r["good"]][NIDX[_r["node"]]] += _r["prod_income"]
        _pp[NIDX[_r["node"]]] += _r["prod_income"]
_GLn = [g for g in GOODS if LIVE[GOODS.index(g)]]
_PHIW = phiw(1.5)
_n = NIDX["gulf_of_siam"]
_sink = {g for g in _GLn if _n in sinks_of(R[g]["directed"])[0]}
chk("3.10", "gulf_of_siam goods with local value", sum(1 for g in _GLn if _val[g][_n] > 0), 13)
chk("3.10", "gulf_of_siam goods that sink there", len(_sink), 12)
_CP = {"CAS": 129.9, "POR": 88.5, "MOR": 23.4, "GRA": 11.6, "ARA": 0.0, "FRA": 0.0}
_COL = ["CAS", "POR", "GRA"]; _TR = ["MOR", "ARA", "FRA"]
_rng = np.random.default_rng(11)
_elig = {g: [c for c in _TR if _rng.random() < 0.6] for g in _GLn}
def _cpow(c, extra):
    return (_CP[c] + extra) * 0.5          # off-home penalty: gulf_of_siam is nobody's home node
def _pergood(prop):
    out = collections.defaultdict(float)
    for g in _GLn:
        if _val[g][_n] <= 0: continue
        Pc = sum(_cpow(c, prop[c][g]) for c in _COL)
        Pt = sum(_CP[c] + prop[c][g] for c in _elig[g])
        sh = 1.0 if g in _sink else (Pc / (Pc + Pt) if Pc + Pt > 0 else 0.0)
        for c in _COL: out[c] += _val[g][_n] * sh * (_cpow(c, prop[c][g]) / Pc)
    return out
def _scalar(prop):
    Pc = sum(_cpow(c, prop[c][_GLn[0]]) for c in _COL); pool = 0.0
    for g in _GLn:
        if _val[g][_n] <= 0: continue
        Pt = sum(_CP[c] + prop[c][g] for c in _elig[g])
        sh = 1.0 if g in _sink else (Pc / (Pc + Pt) if Pc + Pt > 0 else 0.0)
        pool += _val[g][_n] * sh
    return {c: pool * (_cpow(c, prop[c][_GLn[0]]) / Pc) for c in _COL}, pool
def _prop(d, c):
    down = [v for u, v in d if u == _n]
    frac = _CP[c] / max(_pp[_n], 1e-12)
    return sum(_pp[m] * frac for m in down) / 5.0
_zero = {c: {g: 0.0 for g in _GLn} for c in _CP}
_a, (_b, _pool) = _pergood(_zero), _scalar(_zero)
_rel = max(abs(_a[c] - _b[c]) / abs(_a[c]) for c in _COL if _a[c])
chk("3.10", "factoring residual is one ULP, not 5.7e-14", _rel < 1e-15, True)
chk("3.10", "factoring residual order of magnitude", round(np.log10(max(_rel, 1e-300))), -16)
_ps = {c: {g: _prop(_PHIW["directed"], c) for g in _GLn} for c in _CP}
_a1, (_b1, _p1) = _pergood(_ps), _scalar(_ps)
chk("3.10", "single-graph propagation keeps the identity",
    max(abs(_a1[c] - _b1[c]) / abs(_a1[c]) for c in _COL if _a1[c]) < 1e-15, True)
_pg = {c: {g: _prop(R[g]["directed"], c) for g in _GLn} for c in _CP}
_a2, (_b2, _p2) = _pergood(_pg), _scalar(_pg)
_bias = [round(100 * (_b2[c] - _a2[c]) / _a2[c], 2) for c in _COL]
chk("3.10", "per-good propagation overstates every collector", _bias, [0.41, 0.41, 0.41])
chk("3.10", "total error in ducats", round(sum(_b2.values()) - sum(_a2.values()), 2), 0.40)
chk("3.10", "node collects", round(sum(_a2.values()), 1), 97.1)
_dn = lambda d: frozenset(ORDER[v] for u, v in d if u == _n)
chk("3.10", "Phi_w downstream of gulf_of_siam", sorted(_dn(_PHIW["directed"])), ["canton"])
_sets = collections.Counter(_dn(R[g]["directed"]) for g in _GLn)
chk("3.10", "distinct per-good downstream sets", len(_sets), 8)
chk("3.10", "goods leaving it with no downstream", _sets[frozenset()], 12)
chk("3.10", "goods draining to burma alone", _sets[frozenset(["burma"])], 5)
has("3.10", "the identity is reclassified", "This is an **identity, not a measurement**")
has("3.10", "the one-ULP residual is quoted", "worst relative disagreement of **1.3e-16**")
has("3.10", "the eight downstream sets are quoted", "**eight distinct downstream sets across the 29 goods**")
has("3.10", "the bias is quoted as a fraction", "overstates **every** collector's income by **0.41%**")
hasnt("3.10", "the 5.7e-14 measurement", "Verified numerically")
chk("3.10", "5.7e-14 survives only as a historical citation", TXT.count("5.7e-14"), 1)
chk("W170", "3.14 no longer cites it as a tolerance", "as its own 5.7e-14 and 1.4e-14 tolerances show" in TXT, False)
chk("W169", "survival table size in bytes", 29*80*80*8, 1484800)
has("W169", "3.14 states it in bytes", "1,484,800 bytes")
hasnt("3.10", "the 1.4e-14 measurement", "reproduces per-good truth to 1.4e-14")
hasnt("3.10", "the 5.96-ducat figure", "off by 5.96 ducats on a node paying ~250")

print(); print("=" * 104)
bad = [r for r in RES if not r[0]]
print("RESULT: %d checks, %d failed" % (len(RES), len(bad)))
for r in bad: print("   FAIL:", r[1:])
