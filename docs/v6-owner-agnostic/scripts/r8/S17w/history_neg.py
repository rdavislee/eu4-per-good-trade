import os, re, io, collections
import pdx

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"

hits = []
def walk(node, src, path):
    for k, v in node:
        if isinstance(v, pdx.Node):
            if k == "change_price":
                tg, vv = v.get("trade_goods"), v.get("value")
                if tg is not None and vv is not None: hits.append((tg, float(vv), src, path))
            walk(v, src, path)

for dp, _, fs in os.walk(os.path.join(EU4, "history")):
    for fn in fs:
        if not fn.endswith(".txt"): continue
        fp = os.path.join(dp, fn)
        try: walk(pdx.load(fp), "history", fp)
        except Exception as e: print("FAIL", fp, e)

print("total history change_price blocks parsed:", len(hits))
neg = [h for h in hits if h[1] < 0]
print("negative history change_price blocks:", len(neg))
files = set(h[3] for h in neg)
print("files containing negatives:", files)

# also raw textual count (regex) for history to cross-check the 53 raw figure
rawc = 0
for dp, _, fs in os.walk(os.path.join(EU4, "history")):
    for fn in fs:
        if not fn.endswith(".txt"): continue
        fp = os.path.join(dp, fn)
        body = re.sub("#[^\n]*", "", io.open(fp, encoding="latin-1", errors="replace").read())
        rawc += len(re.findall(r"change_price\s*=\s*\{", body))
print("raw textual change_price blocks in history/:", rawc)
