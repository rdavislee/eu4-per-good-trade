import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import PROV, PNODE, ROWS, ROLLED

owned_all = {pid: s for pid, s in PROV.items() if s.get("owner")}
print("owned provinces total (regardless of node membership):", len(owned_all))

# is_city check
no_iscity = [pid for pid, s in owned_all.items() if s.get("is_city") != "yes" and pid in PNODE]
print("owned+in-node provinces where is_city != 'yes':", len(no_iscity))
print("265 in no_iscity list:", 265 in no_iscity)
print("265 base data:", owned_all.get(265))
print("265 devastated (20)?", 265 in {265,267,1771,2967,4237,4726})

owned_in_node = [pid for pid in owned_all if pid in PNODE]
print("owned AND in a trade node:", len(owned_in_node))
iscity_count = sum(1 for pid in owned_in_node if owned_all[pid].get("is_city")=="yes")
print("owned+in-node with is_city==yes:", iscity_count)

# unknown trade goods
unknown = [pid for pid in owned_in_node if owned_all[pid].get("trade_goods") in (None,"unknown")]
print("owned+in-node with trade_goods unknown/none:", len(unknown))
print(sorted(unknown))
rolled_goods = [ROLLED.get(pid) for pid in unknown]
from collections import Counter
print("rolled good counts:", Counter(rolled_goods))
