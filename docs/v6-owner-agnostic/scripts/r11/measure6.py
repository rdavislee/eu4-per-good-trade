# -*- coding: utf-8 -*-
"""Every measured figure spec v6.0 quotes, from the option-(c) solver. Prints label = value so the
verifier can diff these against the numbers actually printed in the document."""
import io, os, re, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pdx
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, PROV,
                    GOODS_PRODUCED_FACTOR, TAX_COEFF, ON_STARTUP_DEVASTATION,
                    build_sc, solve_phi, orient)
from drain import run_drain, sinks_of, has_cycle
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
OUT = {}
def P(k, v):
    OUT[k] = v; print("%-46s %s" % (k, v))

A_PHI = 2.0                     # spec 2.3 aggregate-graph exponent; a hyperparameter
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NW = np.zeros(N); np.add.at(NW, pn, W)
def cv(a=A_PHI, w=None):
    w = W if w is None else w
    t = (w / w.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()
def ph(a=A_PHI, w=None): return run_drain(np.full(N, 1.0 / N) - cv(a, w))
def sk(r):
    o = collections.Counter(u for u, _ in r["directed"])
    return sorted(ORDER[i] for i in range(N) if o[i] == 0)

print("=" * 96); print("A. the field"); print("=" * 96)
P("GP_COEFF read from static_modifiers", GOODS_PRODUCED_FACTOR)
P("TAX_COEFF", TAX_COEFF)
P("counted provinces", len(ROWS))
P("world wealth", round(float(W.sum()), 2))
P("devastated provinces counted", sum(1 for r in ROWS if r["pid"] in ON_STARTUP_DEVASTATION))
Wnd = np.array([(TAX_COEFF * PROV[r["pid"]]["base_tax"]
                 + GOODS_PRODUCED_FACTOR * PROV[r["pid"]]["base_production"] * PRICES.get(r["good"], 0.0))
                for r in ROWS])
P("devastation cost in ducats", round(float(Wnd.sum() - W.sum()), 2))
P("richest single province", "pid %d %.2f" % (ROWS[int(np.argmax(W))]["pid"], W.max()))
P("provinces with trade_goods unknown", sum(1 for r in ROWS if r["good"] == "unknown"))

print(); print("=" * 96); print("B. the installed graph"); print("=" * 96)
base = ph(); BD = set(base["directed"])
cw = cv(); cr = {ORDER[i]: k + 1 for k, i in enumerate(np.argsort(-cw))}
wr = {ORDER[i]: k + 1 for k, i in enumerate(np.argsort(-NW))}
P("Phi_w sinks", sk(base))
for s in sk(base): P("  %s c_w / node-wealth rank" % s, (cr[s], wr[s]))
P("Phase-1 selection", sorted(ORDER[i] for i in base["S0"]))
P("promotions / fallbacks", (len(base["promotions"]), len(base["fallbacks"])))
ind = collections.Counter(v for _, v in base["directed"])
src = [ORDER[i] for i in range(N) if ind[i] == 0]
P("sources", len(src))
P("source c_w rank range", (min(cr[s] for s in src), max(cr[s] for s in src)))
P("source mean degree vs map",
  (round(float(np.mean([len(UND[NIDX[s]]) for s in src])), 1),
   round(float(np.mean([len(UND[i]) for i in range(N)])), 1)))
P("largest |b_w|", round(float(np.abs(np.full(N, 1.0 / N) - cw).max()), 4))
P("edges oriented", "%d/%d" % (len(BD), len(EDGES_UND)))
P("acyclic", has_cycle(base["directed"]) is None)

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for _, g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]
S = {}; C = {}; R = {}
for gi, g in GL:
    t = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, pn, t)
    C[g] = n / n.sum()
    S[g] = val[g] / val[g].sum() if val[g].sum() > 0 else np.zeros(N)
    R[g] = run_drain(S[g] - C[g])
VAL = {g: float(val[g].sum()) for _, g in GL}

# V_g (sec 1.6) is the ENGINE-injected value since v6.5: node trade_goods_size x current price,
# read from the save. val[] above still builds the ORIENTATION supply shares S[g] (model-side,
# owner-agnostic); only the agreement WEIGHT below reads the engine quantity.
def _inject_weights():
    import zipfile
    tgt = open(os.path.join(EU4, "common", "tradegoods", "00_tradegoods.txt"),
               encoding="latin-1").read()
    ORDERG = re.findall(r"^([a-z_]+) = \{", tgt, re.M)
    sg = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                      "Europa Universalis IV", "save games", "VANILLA_start.eu4")
    raw = zipfile.ZipFile(sg).read("gamestate").decode("latin-1")
    def mb(txt, i):
        d = 0; k = i; inq = False
        while k < len(txt):
            c = txt[k]
            if c == '"': inq = not inq
            elif not inq:
                if c == "{": d += 1
                elif c == "}":
                    d -= 1
                    if d == 0: return k
            k += 1
        return len(txt) - 1
    cur = {}
    mm0 = re.search(r"^change_price=\{", raw, re.M)
    st = raw.index("{", mm0.start()); pb = raw[st+1:mb(raw, st)]
    for mm in re.finditer(r"^\t([a-z_]+)=\{", pb, re.M):
        s2 = pb.index("{", mm.start()); blk = pb[s2+1:mb(pb, s2)]
        cp = re.search(r"current_price=([\d.]+)", blk)
        if cp: cur[mm.group(1)] = float(cp.group(1))
    i2 = raw.index(chr(10) + "trade={"); j2 = raw.index("{", i2); tb = raw[j2+1:mb(raw, j2)]
    size = collections.defaultdict(float)
    for mm in re.finditer(r"^\tnode=\{", tb, re.M):
        s2 = tb.index("{", mm.start()); nd = tb[s2+1:mb(tb, s2)]
        blk = re.search(r"trade_goods_size=\{([^}]*)\}", nd, re.S)
        sz = [float(x) for x in blk.group(1).split()] if blk else []
        for k in range(1, min(len(sz), len(ORDERG) + 1)):
            if sz[k]: size[ORDERG[k - 1]] += sz[k]
    return {g: size.get(g, 0.0) * cur.get(g, 0.0) for g in size}
INJ = _inject_weights()
PG = {g: set(R[g]["directed"]) for _, g in GL}
sc = [len(sinks_of(R[g]["directed"])[0]) for _, g in GL]
P("live goods", len(GL))
P("sinks per good min/max/mean", (min(sc), max(sc), round(float(np.mean(sc)), 2)))
P("acyclic goods", sum(1 for _, g in GL if has_cycle(R[g]["directed"]) is None))
P("fallbacks fired across goods", sum(len(R[g]["fallbacks"]) for _, g in GL))
ag = tot = 0; wag = wtot = 0.0
for _, g in GL:
    for u, v in EDGES_UND:
        gd = (u, v) if (u, v) in PG[g] else ((v, u) if (v, u) in PG[g] else None)
        if gd is None: continue
        tot += 1; wtot += INJ[g]
        if ((u, v) if (u, v) in BD else (v, u)) == gd: ag += 1; wag += INJ[g]
P("Phi_w self-coherence edge-goods", round(100.0 * ag / tot, 1))
P("Phi_w self-coherence value-weighted", round(100.0 * wag / wtot, 1))
conn = np.zeros((N, N), dtype=bool)
for _, g in GL:
    adj = collections.defaultdict(list)
    for u, v in R[g]["directed"]: adj[u].append(v)
    for s0 in range(N):
        seen = {s0}; q = collections.deque([s0])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if y not in seen: seen.add(y); q.append(y)
        for t0 in seen:
            if t0 != s0: conn[s0][t0] = True
P("ordered pairs connected", "%d of %d" % (conn.sum(), N * (N - 1)))
P("ordered pairs connected pct", round(100.0 * conn.sum() / (N * (N - 1)), 1))
sup = [S[g][S[g] > 0] for _, g in GL]; dem = [C[g][C[g] > 0] for _, g in GL]
s2 = [x.max() / x.min() for x in sup if len(x) > 1]
d2 = [y.max() / y.min() for y in dem if len(y) > 1]
P("supply contrast range", (round(min(s2)), round(max(s2))))
P("goods with more than one producer", len(s2))
P("single-producer goods", [g for _, g in GL if int((val[g] > 0).sum()) == 1])
P("demand contrast range", (round(min(d2)), round(max(d2), -1)))

print(); print("=" * 96); print("C. alpha bands and world response"); print("=" * 96)
def sset(a):
    r = ph(a); o = collections.Counter(u for u, _ in r["directed"])
    return tuple(sorted(ORDER[i] for i in range(N) if o[i] == 0))
grid = {}
for k in range(100, 801):
    a = round(k / 100, 2); grid[a] = sset(a)
bands = []; cur = grid[1.00]; lo = 1.00
for k in range(101, 801):
    a = round(k / 100, 2)
    if grid[a] != cur: bands.append((cur, lo, round(a - 0.01, 2))); cur = grid[a]; lo = a
bands.append((cur, lo, 8.00))
inb = [(s, l, h) for s, l, h in bands if l <= A_PHI <= h][0]
P("band containing alpha=%g" % A_PHI, ("+".join(inb[0]), inb[1], inb[2], round(inb[2] - inb[1], 2)))
wide = sorted(bands, key=lambda b: -(b[2] - b[1]))[0]
P("widest band on [1,8]", ("+".join(wide[0]), wide[1], wide[2], round(wide[2] - wide[1], 2)))
P("sink count at alpha 1,1.5,2,3,4,8", [len(sset(a)) for a in (1, 1.5, 2, 3, 4, 8)])
EUR = set(int(x) for x in pdx.values(pdx.load(os.path.join(EU4, "map", "continent.txt")).get("europe")))
eur = [i for i, r in enumerate(ROWS) if r["pid"] in EUR]
P("European counted provinces", len(eur))
def devscale(idx, k):
    w = W.copy(); w[idx] *= k; return w
for k in (1.02, 1.56, 2.0):
    P("Europe development x%.2f sinks" % k, sk(ph(A_PHI, devscale(eur, k))))
# Recompute wealth from SCALED DEVELOPMENT, not from the scaled wealth array. The previous form
# compared W*k against W*k and could only ever print 0.0 -- a tautology, which is exactly the defect
# this project criticised in v5.0's harness.
_k = 1.56
_E = set(eur)
def _from_dev(i, r, k):
    s = PROV[r["pid"]]
    f = k if i in _E else 1.0
    gp = GOODS_PRODUCED_FACTOR * s["base_production"] * f
    if r["pid"] in ON_STARTUP_DEVASTATION:          # the multiplier the field carries
        gp *= 1.0 + (-2.0 * ON_STARTUP_DEVASTATION[r["pid"]] / 100.0)
    return TAX_COEFF * s["base_tax"] * f + max(0.0, gp) * PRICES.get(r["good"], 0.0)
_dev = np.array([_from_dev(i, r, _k) for i, r in enumerate(ROWS)])
P("dev-scaled vs wealth-scaled (max diff)", round(float(np.abs(_dev - devscale(eur, _k)).max()), 12))
for s_ in range(3):
    nz = 1 + np.random.default_rng(9000 + s_).uniform(-0.01, 0.01, size=len(W))
    P("sinks under +/-1%% wealth noise seed %d" % s_, sk(ph(A_PHI, W * nz)))
cape = NIDX["cape_of_good_hope"]
P("cape in-degree", sum(1 for _, v in BD if v == cape))
P("cape out-degree", sum(1 for u, _ in BD if u == cape))
adj = collections.defaultdict(list)
for u, v in BD: adj[u].append(v)
def reach(s):
    seen = {s}; q = collections.deque([s])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in seen: seen.add(y); q.append(y)
    return seen
up = [i for i in range(N) if cape in reach(i) and i != cape]
down = reach(cape) - {cape}
P("ordered pairs routed through the cape", sum(1 for a in up for b in down if b in reach(a)))
def route(a, b):
    prev = {NIDX[a]: None}; q = collections.deque([NIDX[a]])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in prev: prev[y] = x; q.append(y)
    if NIDX[b] not in prev: return None
    p = []; x = NIDX[b]
    while x is not None: p.append(ORDER[x]); x = prev[x]
    return list(reversed(p))
for s_ in ("genua", "north_sea", "english_channel"):
    r_ = route(s_, "hangzhou")
    # "no route" and "a route that avoids the Cape" are different facts and used to print the same
    # False -- which read as a pass for a claim about a route that does not exist.
    P("route %s -> hangzhou" % s_,
      "NO ROUTE" if r_ is None else ("via cape" if "cape_of_good_hope" in r_ else "avoids cape"))
P("route genua -> hangzhou", route("genua", "hangzhou"))

# coal activation -- computed here so verify6.py never has to carry a literal for it
_h = os.path.join(EU4, "history", "provinces"); _coal = set()
for _fn in os.listdir(_h):
    _m = re.match(r"^\s*(\d+)", _fn)
    if not _m: continue
    _tx = io.open(os.path.join(_h, _fn), encoding="latin-1", errors="replace").read()
    if re.search(r"latent_trade_goods[^=]*=[^{]*\{[^}]*coal", _tx): _coal.add(int(_m.group(1)))
P("latent-coal provinces", len(_coal))
P("latent-coal owned and counted", sum(1 for r in ROWS if r["pid"] in _coal))
# Hold every non-repriced input fixed. Province 4237 is in the latent-coal set AND in the
# devastated eleven, so a reprice that drops its devastation measures "coal activates" PLUS
# "one province heals" -- a mixed counterfactual worth 0.2*3*10*(1-0.6) = 2.40 ducats and
# 3 edge flips. The devastation multiplier is retained here.
_W2 = W.copy()
for _i, _r in enumerate(ROWS):
    if _r["pid"] in _coal:
        _gp = GOODS_PRODUCED_FACTOR * PROV[_r["pid"]]["base_production"]
        if _r["pid"] in ON_STARTUP_DEVASTATION:
            _gp *= 1.0 + (-2.0 * ON_STARTUP_DEVASTATION[_r["pid"]] / 100.0)
        _W2[_i] = TAX_COEFF * PROV[_r["pid"]]["base_tax"] + max(0.0, _gp) * PRICES["coal"]
P("coal activation wealth delta", round(float(_W2.sum() - W.sum()), 2))
P("coal activation edge flips", len(BD ^ set(ph(A_PHI, _W2)["directed"])) // 2)

print(); print("=" * 96); print("D. file values"); print("=" * 96)
raw = re.sub("#[^" + chr(10) + "]*", "",
             io.open(os.path.join(EU4, "common", "static_modifiers", "00_static_modifiers.txt"),
                     encoding="latin-1").read())
m = re.search(r"provincial_production_size\s*=\s*\{([^}]*)\}", raw)
P("provincial_production_size block", " ".join(m.group(1).split()))
loc = io.open(os.path.join(EU4, "localisation", "EU4_l_english.yml"), encoding="utf-8-sig",
              errors="replace").read()
mm = re.search(r"provincial_production_size:\d*\s*\"([^\"]*)\"", loc)
P("its localisation", mm.group(1) if mm else "?")
hits = []
def walk(node, src):
    for k, v in node:
        if isinstance(v, pdx.Node):
            if k == "change_price":
                tg, vv = v.get("trade_goods"), v.get("value")
                if tg is not None and vv is not None: hits.append((tg, float(vv), src))
            walk(v, src)
rawc = collections.Counter()
for tree in ("events", "decisions", "missions", "common", "history"):
    for dp, _, fs in os.walk(os.path.join(EU4, tree)):
        for fn in fs:
            if not fn.endswith(".txt"): continue
            fp = os.path.join(dp, fn)
            body = re.sub("#[^" + chr(10) + "]*", "", io.open(fp, encoding="latin-1", errors="replace").read())
            rawc[tree] += len(re.findall(r"change_price\s*=\s*\{", body))
            try: walk(pdx.load(fp), tree)
            except Exception: pass
P("change_price textual blocks", sum(rawc.values()))
P("change_price by tree", dict(rawc))
neg = collections.defaultdict(list)
for tg, v_, _ in hits:
    if v_ < 0: neg[tg].append(v_)
below = exact = above = none_ = 0
for g in sorted(PRICES):
    if PRICES[g] <= 0: continue
    if g not in neg: none_ += 1; continue
    fl = PRICES[g] * (1 + min(neg[g]))
    if fl < 2.0 - 1e-9: below += 1
    elif abs(fl - 2.0) < 1e-9: exact += 1
    else: above += 1
P("price partition below/exact/above/none", (below, exact, above, none_))
for k in ("TRADING_POLICY_COOLDOWN_MONTHS", "TRADE_COMPANY_DAYS_TO_SWAP_LEADER", "TRADE_COMPANY_COOLDOWN"):
    d = io.open(os.path.join(EU4, "common", "defines.lua"), encoding="latin-1").read()
    mq = re.search(k + r"\s*=\s*([\d.]+)", d)
    P("define %s" % k, mq.group(1) if mq else "?")
# C1: the deleted-apparatus figures. Imported rather than inlined -- the twenty-two frozen v5
# constants live in apparatus6.py so they cannot be wired back into the live wealth path here.
# 105.30 was quoted in sections 0 and 1.3 with no instrument anywhere in the tree.
import apparatus6 as _AP
for _k, _v in _AP.FIGURES.items():
    P(_k, _v)

io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "measure6.out"),
        "w", encoding="utf-8", newline="\n").write(
    "\n".join("%s\t%s" % (k, v) for k, v in OUT.items()))
print()
print("wrote measure6.out with %d labelled figures" % len(OUT))
