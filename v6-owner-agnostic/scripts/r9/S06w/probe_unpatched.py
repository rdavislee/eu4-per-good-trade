import collections, io, os, sys, types
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "..")
V5 = os.path.join(SCRIPTS, "..", "..", "v5-owner-agnostic", "scripts")
sys.path.insert(0, SCRIPTS); os.chdir(SCRIPTS)
from solver import N, ORDER, NIDX, EDGES_UND, ROWS
from drain import run_drain

_p5 = os.path.join(V5, "_audit_b_drain.py")
_src = io.open(_p5, encoding="utf-8").read()
ab = types.ModuleType("abd"); ab.__dict__["__name__"] = "abd"
exec(compile(_src, "_audit_b_drain[unpatched]", "exec"), ab.__dict__)

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, W)
t = (W / W.max()) ** 2.0
num = np.zeros(N); np.add.at(num, pn, t)
BW = np.full(N, 1.0 / N) - num / num.sum()

shipped = run_drain(BW)
SHIP_E = set(shipped["directed"])

names = list(ORDER)
edges = sorted(tuple(sorted((u,v))) for u,v in EDGES_UND)
r = ab.drain(names, edges, BW, NODEW)
d = r["directed"] if isinstance(r, dict) else r
D = set(d)
print("shipped edges:", len(SHIP_E), "unpatched-repro edges:", len(D))
print("edges disagreeing:", len(SHIP_E ^ D)//1, "  (symmetric diff count, each differing edge contributes up to 2 if reversed)")
disagree = 0
SHIP_UND = {}
for (u,v) in SHIP_E:
    SHIP_UND[frozenset((u,v))] = (u,v)
D_UND = {}
for (u,v) in D:
    D_UND[frozenset((u,v))] = (u,v)
common_keys = set(SHIP_UND) & set(D_UND)
for k in common_keys:
    if SHIP_UND[k] != D_UND[k]:
        disagree += 1
print("undirected edges present in both:", len(common_keys))
print("of those, disagreeing in direction:", disagree)
print("edges only in shipped:", len(set(SHIP_UND)-set(D_UND)))
print("edges only in unpatched-repro:", len(set(D_UND)-set(SHIP_UND)))
