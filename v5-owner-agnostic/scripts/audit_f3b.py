# -*- coding: utf-8 -*-
"""F3, corrected set: 10 start-applied permanent province modifiers + 6 ungated monuments
(incl. krakow_cloth_hall, a MULTIPLICATIVE trade_goods_size_modifier both audits missed)."""
import numpy as np, collections, sys, os
sys.path.insert(0, os.getcwd())
from solver import N, ORDER, NIDX, PROV, PRICES, ROWS
from drain import run_drain
FLAT  = {8:3.0, 684:0.5, 1821:0.5, 1822:0.5, 2145:0.5,          # monuments, flat
         6:2.0, 362:2.0, 363:2.0, 370:1.0, 371:1.0, 387:3.0, 542:4.0, 2151:2.5, 2316:2.0, 4316:2.0}
GPMOD = {262:0.10}                                              # krakow_cloth_hall, multiplicative
TVMOD = {684:0.1, 1821:0.1, 1822:0.1, 2145:0.1}
def wealth(mode):
    w=[]
    for r in ROWS:
        pid=r["pid"]; g=r["good"]
        gp=0.2*PROV[pid]["base_production"]; tv=0.10 if g=="incense" else 0.0
        tax=0.15 if g=="gems" else 0.0
        if mode:
            gp=(gp+FLAT.get(pid,0.0))*(1.0+GPMOD.get(pid,0.0))
            tv+=TVMOD.get(pid,0.0)
        w.append(PROV[pid]["base_tax"]*(1+tax)+gp*PRICES.get(g,0.0)*(1+tv))
    return np.array(w)
pn=np.array([NIDX[r["node"]] for r in ROWS])
def sinks(w,a,noise=None):
    ww=w if noise is None else w*noise
    t=(ww/ww.max())**a; num=np.zeros(N); np.add.at(num,pn,t)
    r=run_drain(np.full(N,1.0/N)-num/num.sum())
    o=collections.Counter(u for u,_ in r["directed"])
    return sorted(ORDER[i] for i in range(N) if o[i]==0), set(r["directed"])
w0,w1=wealth(False),wealth(True)
print("world wealth  as shipped %.2f  ->  corrected %.2f" % (w0.sum(), w1.sum()))
s0,d0=sinks(w0,1.5); s1,d1=sinks(w1,1.5)
print("alpha=1.5 sinks: %s -> %s   (edge flips %d)" % (s0,s1,len(d0^d1)//2))
bands=collections.defaultdict(list)
for k in range(100,301):
    a=round(k/100,2); s,_=sinks(w1,a); bands[tuple(s)].append(a)
print("\nbands on the corrected field (alpha 1.00..3.00, 0.01 step), 2-sink sets only:")
for s,al in sorted(bands.items(), key=lambda kv:-len(kv[1])):
    if len(s)!=2: continue
    print("   %-42s [%.2f, %.2f] width %.2f  centre %.2f" % (list(s),min(al),max(al),max(al)-min(al),(min(al)+max(al))/2))
print("\nwidest band overall:")
for s,al in sorted(bands.items(), key=lambda kv:-len(kv[1]))[:4]:
    print("   %d sinks %-42s [%.2f, %.2f] width %.2f" % (len(s),list(s),min(al),max(al),max(al)-min(al)))
