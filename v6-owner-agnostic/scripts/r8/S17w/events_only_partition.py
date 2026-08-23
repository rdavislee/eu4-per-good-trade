import os, re, io, collections
import pdx

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"

PRICES = {}
ptxt = re.sub("#[^\n]*", "", io.open(os.path.join(EU4,"common","prices","00_prices.txt"), encoding="latin-1").read())
for m in re.finditer(r"(\w+)\s*=\s*\{([^}]*)\}", ptxt):
    name, body = m.group(1), m.group(2)
    bm = re.search(r"base_price\s*=\s*([\d.]+)", body)
    if bm: PRICES[name] = float(bm.group(1))

hits = []
def walk(node, src):
    for k, v in node:
        if isinstance(v, pdx.Node):
            if k == "change_price":
                tg, vv = v.get("trade_goods"), v.get("value")
                if tg is not None and vv is not None: hits.append((tg, float(vv), src))
            walk(v, src)

# exclude history/ -- the four trees v3 supposedly parsed
for tree in ("events", "decisions", "missions", "common"):
    for dp, _, fs in os.walk(os.path.join(EU4, tree)):
        for fn in fs:
            if not fn.endswith(".txt"): continue
            fp = os.path.join(dp, fn)
            try: walk(pdx.load(fp), tree)
            except Exception: pass

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
print("excluding history/: below/exact/above/none =", below, exact, above, none_)
