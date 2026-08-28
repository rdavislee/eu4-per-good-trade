"""Derive which land provinces are coastal from provinces.bmp, then test the
node file's `inland` flag against the spec's derivation rule (2.2):
    inland  <=>  no coastal province among the node's `members`.
"""
import os, sys, json, csv
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
HERE = os.path.dirname(os.path.abspath(__file__))

# rgb -> province id
rgb2id = {}
with open(os.path.join(EU4, "map", "definition.csv"), encoding="latin-1") as f:
    for i, line in enumerate(f):
        parts = line.strip().split(";")
        if i == 0 or len(parts) < 4:
            continue
        try:
            pid = int(parts[0]); r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
        except ValueError:
            continue
        rgb2id[(r, g, b)] = pid

img = Image.open(os.path.join(EU4, "map", "provinces.bmp")).convert("RGB")
a = np.asarray(img)
print("bitmap:", a.shape)
key = (a[:, :, 0].astype(np.int32) << 16) | (a[:, :, 1].astype(np.int32) << 8) | a[:, :, 2].astype(np.int32)
lut = np.full(1 << 24, -1, dtype=np.int32)
for (r, g, b), pid in rgb2id.items():
    lut[(r << 16) | (g << 8) | b] = pid
pid_map = lut[key]
print("unmapped pixels:", int((pid_map < 0).sum()))

dm = pdx.load(os.path.join(EU4, "map", "default.map"))
sea = set(int(x) for x in pdx.values(dm.get("sea_starts")))
lakes = set(int(x) for x in pdx.values(dm.get("lakes"))) if dm.get("lakes") else set()

seamask = np.zeros(int(pid_map.max()) + 2, dtype=bool)
for s in sea:
    if s < len(seamask):
        seamask[s] = True

is_sea_px = seamask[np.clip(pid_map, 0, None)]
coastal = set()
h, w = pid_map.shape
for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
    shifted_sea = np.roll(is_sea_px, (dy, dx), axis=(0, 1))
    shifted_pid = np.roll(pid_map, (dy, dx), axis=(0, 1))
    touch = (~is_sea_px) & shifted_sea & (pid_map >= 0)
    coastal.update(np.unique(pid_map[touch]).tolist())
coastal.discard(-1)
coastal = {int(c) for c in coastal if c not in sea}
print("coastal land provinces (touch a sea_starts province):", len(coastal))

# force_coastal from default.map
fc = dm.get("force_coastal")
forced = set(int(x) for x in pdx.values(fc)) if fc else set()
print("force_coastal entries:", len(forced))
coastal |= forced

D = json.load(open(os.path.join(HERE, "nodes.json")))
order, nodes = D["order"], D["nodes"]
rows = []
for n in order:
    mem = nodes[n]["members"]
    ncoast = sum(1 for p in mem if p in coastal)
    flag = nodes[n]["inland"] == "yes"
    derived = (ncoast == 0)
    rows.append((n, flag, derived, ncoast, len(mem)))

mismatch = [r for r in rows if r[1] != r[2]]
print()
print("nodes flagged inland=yes            :", sum(1 for r in rows if r[1]))
print("nodes derived inland (no coastal mbr):", sum(1 for r in rows if r[2]))
print("MISMATCHES:", len(mismatch))
print("%-26s %-6s %-8s %8s %8s" % ("node", "flag", "derived", "coastal", "members"))
for r in sorted(mismatch, key=lambda r: -r[3]):
    print("%-26s %-6s %-8s %8d %8d" % (r[0], r[1], r[2], r[3], r[4]))
print()
print("flagged-inland nodes and their coastal member counts:")
for r in rows:
    if r[1]:
        print("   %-26s coastal members=%d" % (r[0], r[3]))
json.dump(sorted(coastal), open(os.path.join(HERE, "coastal.json"), "w"))
