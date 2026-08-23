import os, re, io

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"

quoted_hits = []
for tree in ("events", "decisions", "missions", "common", "history"):
    for dp, _, fs in os.walk(os.path.join(EU4, tree)):
        for fn in fs:
            if not fn.endswith(".txt"): continue
            fp = os.path.join(dp, fn)
            raw = io.open(fp, encoding="latin-1", errors="replace").read()
            body = re.sub("#[^\n]*", "", raw)
            # find quoted spans
            spans = [m.span() for m in re.finditer(r'"[^"]*"', body, re.S)]
            for m in re.finditer(r"change_price\s*=\s*\{", body):
                pos = m.start()
                inside = None
                for (s,e) in spans:
                    if s <= pos < e:
                        inside = (s,e)
                        break
                if inside:
                    snippet = body[max(0,inside[0]-120):inside[0]]
                    quoted_hits.append((fp, pos, snippet[-200:]))

print("quoted (invisible-to-parser) change_price occurrences:", len(quoted_hits))
for fp, pos, snippet in quoted_hits:
    print("----")
    print(fp, "@", pos)
    print(repr(snippet[-160:]))
