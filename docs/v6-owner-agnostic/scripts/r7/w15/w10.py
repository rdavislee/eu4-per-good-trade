# -*- coding: utf-8 -*-
"""v4 §3.5/§3.13: the sublinear-reachability partition over ALL shipped change_price blocks."""
import os,sys,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import pdx
EU4=r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
prices={k:float(v.get("base_price",0)) for k,v in pdx.load(os.path.join(EU4,"common","prices","00_prices.txt")) if isinstance(v,pdx.Node)}
def walk(n,h,s):
    for k,v in n:
        if isinstance(v,pdx.Node):
            if k=="change_price":
                tg,val=v.get("trade_goods"),v.get("value")
                if tg is not None and val is not None: h.append((tg,float(val),s,v.get("key")))
            walk(v,h,s)
hits=[]
for r in ("events","decisions","missions","common","history"):
    for dp,_,fs in os.walk(os.path.join(EU4,r)):
        for fn in fs:
            if fn.endswith(".txt"):
                try: walk(pdx.load(os.path.join(dp,fn)),hits,r)
                except Exception: pass
byt=collections.Counter(h[2] for h in hits)
print("change_price blocks: %d total  %s" % (len(hits), dict(byt)))
print("negative blocks in history/: %d" % sum(1 for h in hits if h[2]=="history" and h[1]<0))
neg=collections.defaultdict(list)
for tg,v,s,k in hits:
    if v<0: neg[tg].append((v,s,k))
below=[];exact=[];above=[];none_=[]
for g in sorted(prices):
    if prices[g]<=0: continue
    if g not in neg: none_.append(g); continue
    w,src,key=min(neg[g]); fl=prices[g]*(1+w)
    row=(g,prices[g],w,round(fl,4),src,key)
    if   fl < 2.0-1e-9: below.append(row)
    elif abs(fl-2.0)<1e-9: exact.append(row)
    else: above.append(row)
print("\nBELOW 2.0 (sublinear reachable): %d" % len(below))
for x in sorted(below,key=lambda y:y[3]): print("   %-12s %.2f %+.2f -> %-7s %s/%s"%(x[0],x[1],x[2],x[3],x[4],x[5]))
print("EXACTLY 2.0 (alpha = 1, not sublinear): %d %s" % (len(exact),[x[0] for x in exact]))
print("ABOVE 2.0 despite a negative event: %d %s" % (len(above),[(x[0],x[3]) for x in above]))
print("NO negative event at all: %d %s" % (len(none_),none_))
print("total: %d" % (len(below)+len(exact)+len(above)+len(none_)))
print("\nwool, every shipped change_price:")
for tg,v,s,k in hits:
    if tg=="wool": print("   %+.2f key=%-22s %s" % (v,k,s))
