"""Is A4's re-measure well-posed? Rebuild V_g from the save's engine-modified quantity and
re-run measure6's value-weighted self-coherence under it."""
import zipfile, re, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import N, ORDER, NIDX, EDGES_UND, GOODS, PRICES, ROWS
from drain import run_drain, sinks_of
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
tg = open(os.path.join(EU4, "common", "tradegoods", "00_tradegoods.txt"), encoding="latin-1").read()
ORDERG = re.findall(r"^([a-z_]+) = \{", tg, re.M)
SG = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                  "Europa Universalis IV", "save games", "VANILLA_start.eu4")
raw = zipfile.ZipFile(SG).read("gamestate").decode("latin-1")
def mb(s, i):
    d = 0; k = i; inq = False
    while k < len(s):
        c = s[k]
        if c == '"': inq = not inq
        elif not inq:
            if c == "{": d += 1
            elif c == "}":
                d -= 1
                if d == 0: return k
        k += 1
    return len(s) - 1
m = re.search(r"^change_price=\{", raw, re.M); st = raw.index("{", m.start()); pb = raw[st+1:mb(raw, st)]
CUR = {}
for mm in re.finditer(r"^\t([a-z_]+)=\{", pb, re.M):
    s2 = pb.index("{", mm.start()); blk = pb[s2+1:mb(pb, s2)]
    cp = re.search(r"current_price=([\d.]+)", blk)
    if cp: CUR[mm.group(1)] = float(cp.group(1))
i2 = raw.index(chr(10) + "trade={"); j2 = raw.index("{", i2); tb = raw[j2+1:mb(raw, j2)]
size = collections.defaultdict(float)          # good -> world engine goods_produced
node_size = {}                                 # node -> {good: size}
for mm in re.finditer(r"^\tnode=\{", tb, re.M):
    s2 = tb.index("{", mm.start()); nd = tb[s2+1:mb(tb, s2)]
    name = re.search(r'definitions="([^"]+)"', nd).group(1)
    blk = re.search(r"trade_goods_size=\{([^}]*)\}", nd, re.S)
    sz = [float(x) for x in blk.group(1).split()] if blk else []
    d = {}
    for k in range(1, min(len(sz), len(ORDERG)+1)):
        if sz[k]: d[ORDERG[k-1]] = sz[k]; size[ORDERG[k-1]] += sz[k]
    node_size[name] = d
NEWV = {g: size.get(g, 0.0) * CUR.get(g, 0.0) for g in ORDERG}
# ---- shipped orientation, untouched
A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
t = (W / W.max()) ** A_PHI; nn = np.zeros(N); np.add.at(nn, pn, t); c = nn / nn.sum()
BD = set(run_drain(np.full(N, 1.0/N) - c)["directed"])
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
from solver import build_sc
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]
S = {}; C = {}; R = {}
for g in GL:
    tt = (W / W.max()) ** ALPHA(g); n2 = np.zeros(N); np.add.at(n2, pn, tt)
    C[g] = n2 / n2.sum()
    S[g] = val[g] / val[g].sum() if val[g].sum() > 0 else np.zeros(N)
    R[g] = run_drain(S[g] - C[g])
PG = {g: set(R[g]["directed"]) for g in GL}
OLDV = {g: float(val[g].sum()) for g in GL}
def coh(weight):
    ag = tot = 0; wag = wtot = 0.0
    for g in GL:
        for u, v in EDGES_UND:
            gd = (u, v) if (u, v) in PG[g] else ((v, u) if (v, u) in PG[g] else None)
            if gd is None: continue
            tot += 1; wtot += weight[g]
            if ((u, v) if (u, v) in BD else (v, u)) == gd: ag += 1; wag += weight[g]
    return round(100.0*ag/tot, 1), round(100.0*wag/wtot, 1)
u_old, w_old = coh(OLDV)
u_new, w_new = coh({g: NEWV.get(g, 0.0) for g in GL})
print("shipped weights (measure6 VAL = per-good production income):  unweighted %.1f  value-weighted %.1f" % (u_old, w_old))
print("A4 weights (engine goods_produced x current price, from save): unweighted %.1f  value-weighted %.1f" % (u_new, w_new))
print()
print("world engine value by good (top 8):", sorted(((round(NEWV[g],1), g) for g in GL), reverse=True)[:8])
print("model prod-income by good (top 8): ", sorted(((round(OLDV[g],1), g) for g in GL), reverse=True)[:8])
print("goods with NEWV == 0 among live goods:", [g for g in GL if NEWV.get(g, 0.0) == 0.0])
