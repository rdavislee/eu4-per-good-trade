# -*- coding: utf-8 -*-
"""v4: V223 - name the European node set and re-measure the x2 / x3 thresholds."""
import numpy as np, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain

wealth=np.array([r["tax"]+r["prod_income"] for r in ROWS]); pn=np.array([NIDX[r["node"]] for r in ROWS])
WEST18 = ["english_channel","north_sea","baltic_sea","white_sea","novgorod","lubeck","rheinland",
          "saxony","wien","krakow","pest","venice","ragusa","genua","champagne","bordeaux",
          "valencia","sevilla"]
EXTRA4 = ["constantinople","crimea","kiev","kazan"]
def sets():
    for nm, S in (("18-node western/central", WEST18), ("22-node (18 + Constantinople, Crimea, Kiev, Kazan)", WEST18+EXTRA4)):
        yield nm, [n for n in S if n in NIDX]
def phi_w(w, a=1.5):
    t=(w/w.max())**a; num=np.zeros(N); np.add.at(num,pn,t); c=num/num.sum()
    return run_drain(np.full(N,1.0/N)-c)
def sinks(r):
    od=collections.Counter(u for u,_ in r["directed"])
    return sorted(ORDER[i] for i in range(N) if od[i]==0)
def cape(r):
    ci=NIDX["cape_of_good_hope"]
    return (sorted(ORDER[u] for u,v in r["directed"] if v==ci),
            sorted(ORDER[v] for u,v in r["directed"] if u==ci))
base=phi_w(wealth)
print("baseline sinks:",sinks(base),"| cape in<-",cape(base)[0],"out->",cape(base)[1])
for nm,S in sets():
    idx=np.array([k for k,r in enumerate(ROWS) if r["node"] in set(S)])
    print("\n=== %s (%d nodes, %d provinces) ===" % (nm,len(S),len(idx)))
    for f in (1.5,2.0,2.5,3.0,4.0):
        w=wealth.copy(); w[idx]*=f
        r=phi_w(w); ci,co=cape(r)
        print("  x%-4s sinks=%-42s cape in<-%s out->%s" % (f,sinks(r),ci,co))
print("\n=== dev-stack hangzhou's top province ===")
hz=[k for k,r in enumerate(ROWS) if r["node"]=="hangzhou"]
top=max(hz,key=lambda k: wealth[k])
print("  top province pid=%s w=%.2f" % (ROWS[top]["pid"], wealth[top]))
for f in (10,20,30,50):
    w=wealth.copy(); w[top]*=f
    print("  x%-3d sinks=%s" % (f, sinks(phi_w(w))))
