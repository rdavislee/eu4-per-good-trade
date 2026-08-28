"""Round-11 reproduction of the "verified two ways on the save" claim (Y1341, spec sec 3.4):
inject inherits §3.4's production-efficiency and autonomy exclusion, by vanilla's own construction.

Way 1 (file/structural, printed by the grep this script's header documents, not reproduced here):
common/static_modifiers/00_static_modifiers.txt's autonomy-tier regime blocks (core, colonial_core,
territory_core, territory_non_core, pasha_state) grant local_tax_modifier / local_manpower_modifier /
local_sailors_modifier / local_missionary_strength / min_local_autonomy / local_governing_cost --
never trade_goods_size_modifier. "production_efficiency" / "local_production_efficiency" (tech,
ideas, buildings) is a wholly separate Paradox modifier key from trade_goods_size /
trade_goods_size_modifier / local_trade_goods_size_modifier / global_trade_goods_size_modifier --
by the engine's own modifier-key construction, the former cannot feed the latter.

Way 2 (save/measured, this script): find (node, good) cells fed by exactly one counted province,
where that province's local_autonomy in the save is materially nonzero, and check whether the
engine's trade_goods_size for that cell still equals the raw, autonomy-free model prediction
(0.2 * base_production, adjusted only for §1.3's four state modifiers). If autonomy suppressed
goods_produced, high-autonomy singleton provinces would show a large negative residual; if it
does not, the residual should be ~0 regardless of autonomy.
"""
import zipfile, re, os, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "r10"))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "r10"))
from solver import ROWS, PROV, GOODS_PRODUCED_FACTOR, ON_STARTUP_DEVASTATION, STATE_GOODS_MOD

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
tg = open(os.path.join(EU4, "common", "tradegoods", "00_tradegoods.txt"), encoding="latin-1").read()
ORDERG = re.findall(r"^([a-z_]+) = \{", tg, re.M)

SG = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                  "Europa Universalis IV", "save games", "VANILLA_start.eu4")
raw = zipfile.ZipFile(SG).read("gamestate").decode("latin-1")

def mb(s, i):
    d = 0; k = i; q = False
    while k < len(s):
        c = s[k]
        if c == '"': q = not q
        elif not q:
            if c == "{": d += 1
            elif c == "}":
                d -= 1
                if d == 0: return k
        k += 1
    return len(s) - 1

# --- engine trade_goods_size per (node, good), same slot-map method as A_effaut.py ---
i2 = raw.index(chr(10) + "trade={"); j2 = raw.index("{", i2); tb = raw[j2+1:mb(raw, j2)]
eng = collections.defaultdict(float)
for mm in re.finditer(r"^\tnode=\{", tb, re.M):
    s2 = tb.index("{", mm.start()); nd = tb[s2+1:mb(tb, s2)]
    name = re.search(r'definitions="([^"]+)"', nd).group(1)
    blk = re.search(r"trade_goods_size=\{([^}]*)\}", nd, re.S)
    sz = [float(x) for x in blk.group(1).split()] if blk else []
    for k in range(1, min(len(sz), len(ORDERG)+1)):
        if sz[k]: eng[(name, ORDERG[k-1])] += sz[k]

# --- per-province local_autonomy from the save ---
i3 = raw.index(chr(10) + "provinces={"); j3 = raw.index("{", i3)
pbody = raw[j3+1:mb(raw, j3)]
autonomy = {}
for m in re.finditer(r"^-(\d+)=\{", pbody, re.M):
    st = pbody.index("{", m.start())
    rec = pbody[st+1:mb(pbody, st)]
    a = re.search(r"^\t\tlocal_autonomy=([0-9.]+)", rec, re.M)
    if a:
        autonomy[int(m.group(1))] = float(a.group(1))

# --- which (node, good) cells are fed by exactly one counted province ---
cell_provs = collections.defaultdict(list)
for r in ROWS:
    cell_provs[(r["node"], r["good"])].append(r["pid"])

singles = {k: v[0] for k, v in cell_provs.items() if len(v) == 1}
print("counted (node,good) cells:", len(cell_provs), "| singleton-province cells:", len(singles))

rows_out = []
for (node, good), pid in singles.items():
    aut = autonomy.get(pid, 0.0)
    s = PROV[pid]
    dev = ON_STARTUP_DEVASTATION.get(pid, 0.0) / 100.0
    gmod = STATE_GOODS_MOD["devastation"] * dev
    predicted = max(0.0, GOODS_PRODUCED_FACTOR * s["base_production"] * (1.0 + gmod))
    actual = eng.get((node, good), 0.0)
    resid = actual - predicted
    rows_out.append((pid, node, good, aut, s["base_production"], predicted, actual, resid))

# provinces with material autonomy among the clean singleton cells
high_aut = sorted([r for r in rows_out if r[3] >= 5.0], key=lambda r: -r[3])
print("\nsingleton cells whose sole province carries local_autonomy >= 5:", len(high_aut))
print("%-6s %-16s %-12s %6s %6s %9s %9s %8s" %
      ("pid", "node", "good", "aut%", "bprod", "pred", "engine", "resid"))
for pid, node, good, aut, bprod, pred, actual, resid in high_aut[:25]:
    print("%-6d %-16s %-12s %6.1f %6.1f %9.3f %9.3f %8.3f" %
          (pid, node, good, aut, bprod, pred, actual, resid))

exact = sum(1 for r in high_aut if abs(r[7]) < 1e-6)
print("\nof the >=5%% autonomy singleton cells: %d/%d match the raw autonomy-free prediction exactly"
      % (exact, len(high_aut)))

# correlation check across ALL singleton cells (not just high-autonomy) between autonomy and residual
import statistics
if len(rows_out) > 2:
    auts = [r[3] for r in rows_out]
    resids = [r[7] for r in rows_out]
    ma, mr = statistics.fmean(auts), statistics.fmean(resids)
    cov = sum((a-ma)*(rr-mr) for a, rr in zip(auts, resids)) / len(auts)
    sa = statistics.pstdev(auts); sr = statistics.pstdev(resids)
    corr = cov / (sa*sr) if sa > 0 and sr > 0 else float("nan")
    print("\nPearson r(local_autonomy, residual) over all %d singleton cells: %.4f" % (len(rows_out), corr))
