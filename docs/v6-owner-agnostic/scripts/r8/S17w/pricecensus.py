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
def walk(node, src, path):
    for k, v in node:
        if isinstance(v, pdx.Node):
            if k == "change_price":
                tg, vv = v.get("trade_goods"), v.get("value")
                if tg is not None and vv is not None: hits.append((tg, float(vv), src, path))
            walk(v, src, path)

rawc = collections.Counter()
for tree in ("events", "decisions", "missions", "common", "history"):
    for dp, _, fs in os.walk(os.path.join(EU4, tree)):
        for fn in fs:
            if not fn.endswith(".txt"): continue
            fp = os.path.join(dp, fn)
            body = re.sub("#[^\n]*", "", io.open(fp, encoding="latin-1", errors="replace").read())
            rawc[tree] += len(re.findall(r"change_price\s*=\s*\{", body))
            try:
                walk(pdx.load(fp), tree, fp)
            except Exception as e:
                print("PARSE FAIL", fp, e)

print("raw textual total:", sum(rawc.values()), dict(rawc))
print("parsed (executable via pdx) hits:", len(hits))
print("never-execute (161 - hits):", sum(rawc.values()) - len(hits))

neg = collections.defaultdict(list)
for tg, v_, src, path in hits:
    if v_ < 0: neg[tg].append((v_, path))

print()
print("=== per-good floor (single most negative key) ===")
below = exact = above = none_ = 0
for g in sorted(PRICES):
    if PRICES[g] <= 0: continue
    if g not in neg:
        none_ += 1
        continue
    mostneg = min(v for v,_ in neg[g])
    fl = PRICES[g] * (1 + mostneg)
    tag = "BELOW" if fl < 2.0-1e-9 else ("EXACT" if abs(fl-2.0)<1e-9 else "ABOVE")
    if tag=="BELOW": below+=1
    elif tag=="EXACT": exact+=1
    else: above+=1
    print(f"{g:16s} base={PRICES[g]:5.2f} mostneg={mostneg:7.4f} floor={fl:7.4f} {tag}")
print("none (no negative event):", none_, [g for g in sorted(PRICES) if PRICES[g]>0 and g not in neg])
print(f"partition below/exact/above/none = {below}/{exact}/{above}/{none_}")
