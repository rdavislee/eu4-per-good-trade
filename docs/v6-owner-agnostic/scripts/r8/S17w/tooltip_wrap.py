import os, re, io
import pdx

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"

hits = []
def walk(node, src, path, ancestors):
    for k, v in node:
        if isinstance(v, pdx.Node):
            if k == "change_price":
                tg, vv = v.get("trade_goods"), v.get("value")
                if tg is not None and vv is not None:
                    hits.append((tg, float(vv), src, path, list(ancestors)))
            walk(v, src, path, ancestors + [k])

for tree in ("events", "decisions", "missions", "common", "history"):
    for dp, _, fs in os.walk(os.path.join(EU4, tree)):
        for fn in fs:
            if not fn.endswith(".txt"): continue
            fp = os.path.join(dp, fn)
            try:
                walk(pdx.load(fp), tree, fp, [])
            except Exception as e:
                print("PARSE FAIL", fp, e)

print("total parsed hits:", len(hits))
tooltip_wrapped = [h for h in hits if "tooltip" in h[4]]
print("hits with 'tooltip' key as an ancestor:", len(tooltip_wrapped))
for h in tooltip_wrapped:
    print(h[0], h[1], h[3], h[4])
