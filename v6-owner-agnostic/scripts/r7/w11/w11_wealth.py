import sys, os, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, ROWS

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NW = np.zeros(N); np.add.at(NW, pn, W)
counted = np.zeros(N, dtype=bool)
for r in ROWS: counted[NIDX[r["node"]]] = True
n_counted = int(counted.sum())
print("nodes holding counted provinces:", n_counted)
wr = {ORDER[i]: k + 1 for k, i in enumerate(np.argsort(-NW))}
print("hangzhou wealth", NW[NIDX["hangzhou"]], "rank", wr["hangzhou"])
print("beijing wealth", NW[NIDX["beijing"]], "rank", wr["beijing"])

# richest single province
import collections as c
best = max(ROWS, key=lambda r: r["tax"]+r["prod_income"])
print("richest single province:", best.get("pid"), best["node"], best["tax"]+best["prod_income"])
