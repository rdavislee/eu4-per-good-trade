# -*- coding: utf-8 -*-
"""Under the CORRECTED wealth field (F3), does any alpha_Phi give the two-sink map?"""
import numpy as np, collections, sys, os
sys.path.insert(0, os.getcwd())
from solver import N, ORDER, NIDX, PROV, PRICES, ROWS
from drain import run_drain
FLAT = {684:0.5,1822:0.5,2145:0.5,1821:0.5,8:3.0,6:2.0,362:2.0,363:2.0,370:1.0,371:1.0,
        387:3.0,542:4.0,2151:2.5,2316:2.0,4316:2.0}
TVMOD = {684:0.1,1822:0.1,2145:0.1,1821:0.1}
def wealth(extras):
    w=[]
    for r in ROWS:
        pid=r["pid"]; g=r["good"]
        gp=0.2*PROV[pid]["base_production"]; tv=0.10 if g=="incense" else 0.0
        tax=0.15 if g=="gems" else 0.0
        if extras: gp+=FLAT.get(pid,0.0); tv+=TVMOD.get(pid,0.0)
        w.append(PROV[pid]["base_tax"]*(1+tax)+gp*PRICES.get(g,0.0)*(1+tv))
    return np.array(w)
pn=np.array([NIDX[r["node"]] for r in ROWS])
def sinks(w,a):
    t=(w/w.max())**a; num=np.zeros(N); np.add.at(num,pn,t)
    r=run_drain(np.full(N,1.0/N)-num/num.sum())
    o=collections.Counter(u for u,_ in r["directed"])
    return sorted(ORDER[i] for i in range(N) if o[i]==0)
w0,w1=wealth(False),wealth(True)
print("alpha   v4.0 wealth (as shipped)                    corrected wealth (F3)")
for a in (1.0,1.1,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.7,1.8,2.0,2.5,3.0,4.0):
    print("%-6s %-42s %s" % (a, sinks(w0,a), sinks(w1,a)))
