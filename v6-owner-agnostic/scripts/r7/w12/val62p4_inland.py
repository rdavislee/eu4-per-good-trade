import json, re, zipfile, os
ND = json.load(open("nodes.json"))
coastal = set(json.load(open("coastal.json")))
ORDER, NODES = ND["order"], ND["nodes"]
flag = [n for n in ORDER if NODES[n].get("inland")]
derived = [n for n in ORDER if not any(p in coastal for p in NODES[n]["members"])]
print("flag inland count:", len(flag), "derived inland count:", len(derived))
print("flag minus derived:", sorted(set(flag)-set(derived)))
print("derived minus flag:", sorted(set(derived)-set(flag)))
print("1781 coastal:", 1781 in coastal, "1782 coastal:", 1782 in coastal)
sib = NODES["siberia"]["members"]
print("siberia coastal members:", [p for p in sib if p in coastal])
