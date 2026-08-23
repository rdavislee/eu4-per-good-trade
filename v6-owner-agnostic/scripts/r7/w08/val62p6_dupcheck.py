# -*- coding: utf-8 -*-
"""Check whether the 7 quoted change_price blocks duplicate an executable events/ block."""
import os, re
ROOT = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
strip = lambda s: "\n".join(x.split("#")[0] for x in s.split("\n"))

files = [
    "missions/DOM_Britain_Missions.txt",
    "missions/KoK_Byzantine_Missions.txt",
    "missions/KoK_Persia_Missions.txt",
    "missions/KoK_Yemen_Missions.txt",
    "missions/WOC_Italian_Missions.txt",
]

DQ = chr(34)
quote_pat = re.compile(DQ + "([^" + DQ + "]*)" + DQ, re.S)

def extract_quoted_change_price(path):
    txt = open(path, encoding="cp1252", errors="replace").read()
    out = []
    for m in quote_pat.finditer(txt):
        body = m.group(1)
        if "change_price" not in body:
            continue
        for cm in re.finditer(r"change_price\s*=\s*\{([^}]*)\}", body):
            b = cm.group(1)
            g = re.search(r"trade_goods\s*=\s*([A-Za-z_]+)", b)
            v = re.search(r"value\s*=\s*(-?[0-9.]+)", b)
            k = re.search(r"key\s*=\s*([A-Za-z_0-9]+)", b)
            out.append((g.group(1) if g else None, k.group(1) if k else None,
                        float(v.group(1)) if v else None))
    return out

all_quoted = []
for rel in files:
    p = os.path.join(ROOT, rel)
    qs = extract_quoted_change_price(p)
    print(rel, "->", qs)
    all_quoted.extend((rel, q) for q in qs)

bare_events = set()
for dp, dn, fn in os.walk(os.path.join(ROOT, "events")):
    for f in fn:
        if not f.endswith(".txt"):
            continue
        p = os.path.join(dp, f)
        txt = strip(open(p, encoding="cp1252", errors="replace").read())
        for cm in re.finditer(r"change_price\s*=\s*\{([^}]*)\}", txt):
            b = cm.group(1)
            g = re.search(r"trade_goods\s*=\s*([A-Za-z_]+)", b)
            v = re.search(r"value\s*=\s*(-?[0-9.]+)", b)
            k = re.search(r"key\s*=\s*([A-Za-z_0-9]+)", b)
            bare_events.add((g.group(1) if g else None, k.group(1) if k else None,
                             float(v.group(1)) if v else None))

print()
print("total bare events/ change_price triples:", len(bare_events))
print()
dup_count = 0
for rel, q in all_quoted:
    is_dup = q in bare_events
    dup_count += is_dup
    print("%-45s %-35s duplicate-of-events: %s" % (rel, q, is_dup))
print()
print("duplicates:", dup_count, "of", len(all_quoted))
