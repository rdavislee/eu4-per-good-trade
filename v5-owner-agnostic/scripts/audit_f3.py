# -*- coding: utf-8 -*-
"""Independent check of the reviewer's F3: do the monument and permanent-province modifiers
that are live at 1444 with no owner condition change PHI_w's sink set?"""
import numpy as np, collections, sys, os, json
sys.path.insert(0, os.getcwd())
from solver import N, ORDER, NIDX, PROV, PNODE, PRICES, ROWS, GOODS, build_sc
from drain import run_drain

FLAT = {684:0.5, 1822:0.5, 2145:0.5, 1821:0.5, 8:3.0,
        6:2.0, 362:2.0, 363:2.0, 370:1.0, 371:1.0, 387:3.0, 542:4.0, 2151:2.5, 2316:2.0, 4316:2.0}
TVMOD = {684:0.1, 1822:0.1, 2145:0.1, 1821:0.1}
print("provinces named:", len(FLAT), "| owned+is_city+in a node:",
      sum(1 for p in FLAT if PROV.get(p,{}).get("owner") and PROV[p].get("is_city")=="yes" and p in PNODE))
for p in sorted(FLAT):
    s=PROV.get(p,{})
    print("   pid=%-5d owner=%-4s is_city=%-3s good=%-14s bp=%-4s flat=%.1f%s" %
          (p, s.get("owner"), s.get("is_city"), s.get("trade_goods"), s.get("base_production"),
           FLAT[p], "  tv+10%" if p in TVMOD else ""))

def wealth_vec(with_extras):
    w=[]
    for r in ROWS:
        pid=r["pid"]; g=r["good"]
        gp = 0.2*PROV[pid]["base_production"]
        tv_mod = 0.10 if g=="incense" else 0.0
        tax_mod = 0.15 if g=="gems" else 0.0
        if with_extras:
            gp += FLAT.get(pid,0.0)
            tv_mod += TVMOD.get(pid,0.0)
        w.append(PROV[pid]["base_tax"]*(1+tax_mod) + gp*PRICES.get(g,0.0)*(1+tv_mod))
    return np.array(w)

pn=np.array([NIDX[r["node"]] for r in ROWS])
def sinks(w):
    t=(w/w.max())**1.5; num=np.zeros(N); np.add.at(num,pn,t)
    r=run_drain(np.full(N,1.0/N)-num/num.sum())
    o=collections.Counter(u for u,_ in r["directed"])
    return sorted(ORDER[i] for i in range(N) if o[i]==0), set(r["directed"])

w0=wealth_vec(False); w1=wealth_vec(True)
s0,d0=sinks(w0); s1,d1=sinks(w1)
print("\nspec v4.0 baseline  world wealth %.2f  sinks %s" % (w0.sum(), s0))
print("with the extras     world wealth %.2f  sinks %s" % (w1.sum(), s1))
print("Phi_w edge flips: %d of 159" % (len(d0^d1)//2))
i=int(np.argmax(w0)); j=int(np.argmax(w1))
print("richest province: baseline pid=%s %s %.2f -> with extras pid=%s %s %.2f"
      % (ROWS[i]["pid"], ROWS[i]["node"], w0[i], ROWS[j]["pid"], ROWS[j]["node"], w1[j]))
NW0=np.zeros(N); np.add.at(NW0,pn,w0); NW1=np.zeros(N); np.add.at(NW1,pn,w1)
mv=sorted(((NW1[k]-NW0[k], ORDER[k]) for k in range(N)), reverse=True)[:5]
print("largest node-wealth moves:", [(n, round(NW0[NIDX[n]],1), round(NW1[NIDX[n]],1)) for _,n in mv])
