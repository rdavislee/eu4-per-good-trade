# Y1117: cape_of_good_hope's 20 members = 1 sea zone + 19 land provinces, none owned at 1444.
import os, re, json, zipfile
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
SG  = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games"

src = re.sub(r"#[^\n]*", "", open(os.path.join(EU4, "common", "tradenodes",
                                               "00_tradenodes.txt"), encoding="latin-1").read())
m = re.search(r"cape_of_good_hope=\{(.*?)\n\}", src, re.S)
blk = m.group(1)
mem = re.search(r"members=\{([^}]*)\}", blk)
members = [int(x) for x in mem.group(1).split()]
print("cape_of_good_hope members: %d -> %s" % (len(members), members))

# sea zones: default.map's sea_starts list
dm = re.sub("#[^" + chr(10) + "]*", "", open(os.path.join(EU4, "map", "default.map"), encoding="latin-1").read())
sea = set(int(x) for x in re.search(r"sea_starts\s*=\s*\{([^}]*)\}", dm, re.S).group(1).split())
lakes = re.search(r"lakes\s*=\s*\{([^}]*)\}", dm, re.S)
lake = set(int(x) for x in lakes.group(1).split()) if lakes else set()
print("  sea zones among members : %s" % sorted(p for p in members if p in sea))
print("  lakes among members     : %s" % sorted(p for p in members if p in lake))
print("  land provinces          : %d" % len([p for p in members if p not in sea and p not in lake]))

# ownership at 1444, from the save
raw = zipfile.ZipFile(os.path.join(SG, "VANILLA_start.eu4")).read("gamestate").decode("latin-1")
def prov_block(pid):
    mm = re.search(r"^-%d=\{" % pid, raw, re.M)
    if not mm: return None
    j = raw.index("{", mm.start()); d = 0; k = j
    while True:
        c = raw[k]
        if c == "{": d += 1
        elif c == "}":
            d -= 1
            if d == 0: break
        k += 1
    return raw[j:k+1]
owned = []
for p in members:
    if p in sea or p in lake: continue
    b = prov_block(p)
    if b is None: continue
    o = re.search(r'(?m)^\s*owner="([^"]+)"', b)
    if o: owned.append((p, o.group(1)))
print("  land members OWNED at 1444: %d %s" % (len(owned), owned))

# and the node wealth the model assigns it
import sys
sys.path.insert(0, r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts")
os.chdir(r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts")
import numpy as np
from solver import N, NIDX, ORDER, ROWS
NODEW = np.zeros(N)
for r in ROWS: NODEW[NIDX[r["node"]]] += r["tax"] + r["prod_income"]
print("  model node wealth of cape_of_good_hope : %r  (global min %r, argmin %s)"
      % (NODEW[NIDX["cape_of_good_hope"]], NODEW.min(), ORDER[int(NODEW.argmin())]))
print("  counted ROWS in that node              : %d"
      % len([r for r in ROWS if r["node"] == "cape_of_good_hope"]))
