# -*- coding: utf-8 -*-
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, ROWS, NODES

node = NODES["cape_of_good_hope"]
members = node["members"]
print("cape_of_good_hope members: %d" % len(members))
print("members:", sorted(members))

counted_pids = {r["pid"] for r in ROWS}
counted_members = [p for p in members if p in counted_pids]
print("counted (owned) members among them: %d -> %s" % (len(counted_members), counted_members))

# check node type / sea vs land: pdx.py or provinces.py might carry province type info
import pdx
prov = json.load(open("prov1444.json", encoding="utf-8")) if os.path.exists("prov1444.json") else None
if prov:
    for p in sorted(members):
        info = prov.get(str(p)) or prov.get(p)
        print(p, info.get("owner") if isinstance(info, dict) else info, info.get("is_sea") if isinstance(info, dict) else None)
