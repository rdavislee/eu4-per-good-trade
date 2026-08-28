import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import ROWS, PROV, ROLLED

LOCAL_TAX_MOD = {"gems": 0.15}
LOCAL_TV_MOD  = {"incense": 0.10}
MON_FLAT  = {8: 3.0, 684: 0.5, 1821: 0.5, 1822: 0.5, 2145: 0.5}
MON_GPMOD = {262: 0.10}
MON_TVMOD = {684: 0.1, 1821: 0.1, 1822: 0.1, 2145: 0.1}
PERM_FLAT = {6: 2.0, 362: 2.0, 363: 2.0, 370: 1.0, 371: 1.0,
             387: 3.0, 542: 4.0, 2151: 2.5, 2316: 2.0, 4316: 2.0}
FLAT_GOODS = dict(MON_FLAT); FLAT_GOODS.update(PERM_FLAT)

gems_pids = set()
incense_pids = set()
gp_pids = set()  # great-project/permanent-modifier

for r in ROWS:
    pid, g = r["pid"], r["good"]
    if g in LOCAL_TAX_MOD:
        gems_pids.add(pid)
    if g in LOCAL_TV_MOD:
        incense_pids.add(pid)
    if pid in FLAT_GOODS or pid in MON_GPMOD or pid in MON_TVMOD:
        gp_pids.add(pid)

touched = gems_pids | incense_pids | gp_pids
both = gems_pids & incense_pids
both_gp_gems = gems_pids & gp_pids
both_gp_incense = incense_pids & gp_pids

print("gems count:", len(gems_pids))
print("incense count:", len(incense_pids))
print("great-project/permanent count:", len(gp_pids))
print("union touched:", len(touched))
print("sum naive 43+31+16 =", 43+31+16)
print("gems & incense overlap:", both)
print("gems & gp overlap:", both_gp_gems)
print("incense & gp overlap:", both_gp_incense)
print("542 in gems:", 542 in gems_pids, "542 in incense:", 542 in incense_pids, "542 in gp:", 542 in gp_pids)
print("4856 good (rolled):", ROLLED.get(4856))
print("4856 in ROWS good field:", [r["good"] for r in ROWS if r["pid"]==4856])

# is_city withdrawn filter version: recompute count under is_city=yes filter requirement
# need raw history is_city flags -- check PROV dict fields
sample_pid = 265
print("PROV[265] keys sample:", {k:v for k,v in PROV.get(265,{}).items() if k in ('is_city','owner','base_tax')})
