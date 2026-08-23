# -*- coding: utf-8 -*-
"""Independent parse of 00_tradenodes.txt + default.map: node members, land counts, ends."""
import re, os
ROOT = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
tn = open(os.path.join(ROOT, "common", "tradenodes", "00_tradenodes.txt"), encoding="cp1252", errors="replace").read()
dm = open(os.path.join(ROOT, "map", "default.map"), encoding="cp1252", errors="replace").read()
strip = lambda s: "\n".join(x.split("#")[0] for x in s.split("\n"))
dm = strip(dm); tn = strip(tn)

sea = set(int(x) for x in re.search(r"sea_starts\s*=\s*\{(.*?)\}", dm, re.S).group(1).split())
lakes = set(int(x) for x in re.search(r"lakes\s*=\s*\{(.*?)\}", dm, re.S).group(1).split())
print("sea_starts: %d ids ; lakes: %d ; 1460 in sea_starts: %s" % (len(sea), len(lakes), 1460 in sea))

# slice top-level node blocks
nodes = {}
pos = 0
tok = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{")
while True:
    mm = tok.search(tn, pos)
    if not mm:
        break
    name = mm.group(1)
    d = 1
    j = mm.end()
    while j < len(tn) and d > 0:
        if tn[j] == "{": d += 1
        elif tn[j] == "}": d -= 1
        j += 1
    nodes[name] = tn[mm.end():j-1]
    pos = j
print("top-level node blocks parsed:", len(nodes))

res, outg = {}, {}
for n, body in nodes.items():
    mm = re.search(r"\bmembers\s*=\s*\{([^}]*)\}", body)
    ids = [int(x) for x in mm.group(1).split()] if mm else []
    land = [p for p in ids if p not in sea and p not in lakes]
    res[n] = (len(ids), len(land), sorted(set(ids) & sea))
    outg[n] = re.findall(r'\bname\s*=\s*"([^"]+)"', body)

for k in ("cape_of_good_hope", "girin", "champagne", "nippon"):
    print("%-20s members=%-4d land=%-4d sea-ids-in-members=%s" % ((k,) + res[k]))
byland = sorted(res.items(), key=lambda kv: kv[1][1])
print("smallest 5 by land:", [(k, v[1]) for k, v in byland[:5]])
print("largest 5 by land :", [(k, v[1]) for k, v in byland[-5:]])
print("spread %d .. %d = %.3fx" % (byland[0][1][1], byland[-1][1][1], byland[-1][1][1]/byland[0][1][1]))
ends = sorted(n for n in nodes if not outg[n])
print("authored ends (no outgoing):", ends)
print("outgoing link declarations:", sum(len(v) for v in outg.values()))
print("total land provinces across members:", sum(v[1] for v in res.values()))
import math
print("(77/19)^0.5 = %.4f ; (68/33)^0.5 = %.4f ; 77/19 = %.4f ; 68/33 = %.4f"
      % (math.sqrt(77/19), math.sqrt(68/33), 77/19, 68/33))
