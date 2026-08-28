import os, sys, json
sys.path.insert(0, os.path.abspath('.'))
from solver import ROWS, PROV, ROLLED

LOCAL_TAX_MOD = {"gems": 0.15}
LOCAL_TV_MOD  = {"incense": 0.10}
MON_FLAT  = {8: 3.0, 684: 0.5, 1821: 0.5, 1822: 0.5, 2145: 0.5}
MON_GPMOD = {262: 0.10}
MON_TVMOD = {684: 0.1, 1821: 0.1, 1822: 0.1, 2145: 0.1}
PERM_FLAT = {6: 2.0, 362: 2.0, 363: 2.0, 370: 1.0, 371: 1.0,
             387: 3.0, 542: 4.0, 2151: 2.5, 2316: 2.0, 4316: 2.0}
FLAT_GOODS = dict(MON_FLAT); FLAT_GOODS.update(PERM_FLAT)

touched=set()
for r in ROWS:
    pid, g = r["pid"], r["good"]
    if g in LOCAL_TAX_MOD or g in LOCAL_TV_MOD or pid in FLAT_GOODS or pid in MON_GPMOD or pid in MON_TVMOD:
        touched.add(pid)

for pid in sorted(touched):
    ic = PROV[pid].get('is_city')
    if not ic:
        print(pid, ic, PROV[pid].get('owner'))
print("total touched", len(touched))
count_city = sum(1 for pid in touched if PROV[pid].get('is_city'))
print("touched with is_city truthy:", count_city)
total_owned_noded = len(ROWS)
city_yes = sum(1 for r in ROWS if PROV[r['pid']].get('is_city'))
print("overall ROWS:", total_owned_noded, "with is_city truthy:", city_yes)
