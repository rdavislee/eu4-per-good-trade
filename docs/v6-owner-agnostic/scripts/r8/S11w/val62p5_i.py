import sys, os, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc, solve_phi, orient
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
gi = GOODS.index("spices"); a = ALPHA("spices")
W = np.array([r["tax"]+r["prod_income"] for r in ROWS]); PN = np.array([NIDX[r["node"]] for r in ROWS])
S_UNI, C0, _,_,_,_ = build_sc(ALPHA, eps=1e-6); s = S_UNI[gi]
def is_sink(i,k):
    w=np.where(PN==i,W*k,W); t=w**a; c=np.zeros(N); np.add.at(c,PN,t/t.sum())
    return collections.Counter(u for u,_ in orient(solve_phi(s-c)))[i]==0
def bisect(i,hi=60.0):
    if is_sink(i,1.0): return 1.0
    if not is_sink(i,hi): return None
    lo=1.0
    for _ in range(34):
        mid=(lo+hi)/2
        if is_sink(i,mid): hi=mid
        else: lo=mid
    return hi
CH=["beijing","hangzhou","xian","canton","girin","yumen","chengdu"]
for k,n in sorted((bisect(NIDX[n]) or 1e9, n) for n in CH):
    print("%-10s %s" % (n, "%.3f" % k if k<1e8 else ">60"))
print()
print(sorted(ORDER))
