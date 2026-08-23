# -*- coding: utf-8 -*-
"""16-province fold-in (incl. the multiplicative krakow_cloth_hall), full alpha band table,
and whether the band table is a property of the model or of the 1444 snapshot."""
import os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pdx, solver
from solver import N, ORDER, NIDX, PRICES
from drain import run_drain

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
START = (1444, 11, 11); D = re.compile(r"^(\d{1,4})\.(\d{1,2})\.(\d{1,2})$")
WK = ("trade_goods_size","trade_goods_size_modifier","local_tax_modifier","trade_value_modifier")
defs = {}
for sub in ("event_modifiers","static_modifiers"):
    p = os.path.join(EU4,"common",sub)
    for fn in os.listdir(p):
        if fn.endswith(".txt"):
            for k,v in pdx.load(os.path.join(p,fn)):
                if isinstance(v,pdx.Node): defs[k]={a:b for a,b in v if not isinstance(b,pdx.Node)}
FLAT=collections.defaultdict(float); GPM=collections.defaultdict(float)
TV=collections.defaultdict(float); TX=collections.defaultdict(float)
hist=os.path.join(EU4,"history","provinces")
for fn in os.listdir(hist):
    m=re.match(r"^\s*(\d+)",fn)
    if not m: continue
    pid=int(m.group(1))
    def scan(node):
        for k,v in node:
            if isinstance(v,pdx.Node):
                dm=D.match(k or "")
                if dm:
                    if (int(dm.group(1)),int(dm.group(2)),int(dm.group(3)))<=START: scan(v)
                    continue
                if k in ("add_permanent_province_modifier","add_province_modifier"):
                    nm=v.get("name")
                    if nm and nm in defs:
                        g=defs[nm]
                        FLAT[pid]+=float(g.get("trade_goods_size",0)); GPM[pid]+=float(g.get("trade_goods_size_modifier",0))
                        TV[pid]+=float(g.get("trade_value_modifier",0)); TX[pid]+=float(g.get("local_tax_modifier",0))
                else: scan(v)
    scan(pdx.load(os.path.join(hist,fn)))
for k,v in pdx.load(os.path.join(EU4,"common","great_projects","01_monuments.txt")):
    if not isinstance(v,pdx.Node): continue
    st,dt=v.get("starting_tier"),v.get("date")
    if st is None or dt is None: continue
    m=D.match(dt)
    if not m or (int(m.group(1)),int(m.group(2)),int(m.group(3)))>START: continue
    tr=v.get("can_use_modifiers_trigger")
    if tr is not None and len(tr)>0: continue
    p=int(v.get("start"))
    for t in range(0,int(st)+1):
        tb=v.get("tier_%d"%t); pm=tb.get("province_modifiers") if tb is not None else None
        if not pm: continue
        for a,b in pm:
            if a=="trade_goods_size": FLAT[p]+=float(b)
            elif a=="trade_goods_size_modifier": GPM[p]+=float(b)
            elif a=="trade_value_modifier": TV[p]+=float(b)
            elif a=="local_tax_modifier": TX[p]+=float(b)

def rows(corr):
    out=[]
    for r in solver.ROWS:
        pid=r["pid"]; bp=solver.PROV[pid]["base_production"]; bt=solver.PROV[pid]["base_tax"]
        gp=0.2*bp*(1+(GPM.get(pid,0.0) if corr else 0.0))+(FLAT.get(pid,0.0) if corr else 0.0)
        tvm=solver.LOCAL_TV_MOD.get(r["good"],0.0)+(TV.get(pid,0.0) if corr else 0.0)
        txm=solver.LOCAL_TAX_MOD.get(r["good"],0.0)+(TX.get(pid,0.0) if corr else 0.0)
        out.append((NIDX[r["node"]], bt*(1+txm)+gp*PRICES.get(r["good"],0.0)*(1+tvm)))
    return out
BASE=rows(False); CORR=rows(True)
touched=sorted(set(list(FLAT)+list(GPM)+list(TV)+list(TX)) & set(r["pid"] for r in solver.ROWS))
print("owned+is_city provinces whose wealth changes: %d"%len(touched))
print("world wealth: %.2f -> %.2f"%(sum(x[1] for x in BASE),sum(x[1] for x in CORR)))

def sinks(rws,a,noise=None):
    w=np.array([x[1] for x in rws]); 
    if noise is not None: w=w*noise
    pn=np.array([x[0] for x in rws]); c=np.zeros(N); np.add.at(c,pn,w**a); c/=c.sum()
    r=run_drain(np.ones(N)/N-c); d=set(r["directed"])
    return tuple(sorted(ORDER[i] for i in range(N) if not any(u==i for u,_ in d)))
def bands(rws,noise=None,lo=100,hi=301):
    out=[]; prev=None
    for i in range(lo,hi):
        a=i/100.0; s=sinks(rws,a,noise)
        if s!=prev: out.append([a,a,s]); prev=s
        else: out[-1][1]=a
    return out
print("\nBAND TABLE, corrected 16-province field, alpha 1.00-3.00 @0.01")
for lo,hi,s in sorted(bands(CORR),key=lambda x:-(x[1]-x[0])):
    print("  width %.2f  [%.2f, %.2f]  %d sinks %s"%(hi-lo+0.01,lo,hi,len(s),list(s)))
print("\nIs the band table a snapshot property?  same field, +/-1%% wealth noise, 3 seeds:")
for seed in range(3):
    rng=np.random.default_rng(seed); nz=1.0+rng.uniform(-0.01,0.01,len(CORR))
    b=[(round(lo,2),round(hi,2),len(s)) for lo,hi,s in bands(CORR,nz,140,231)]
    print("   seed %d: %s"%(seed,b))
print("\n   unperturbed, same window: %s"%[(round(lo,2),round(hi,2),len(s)) for lo,hi,s in bands(CORR,None,140,231)])
