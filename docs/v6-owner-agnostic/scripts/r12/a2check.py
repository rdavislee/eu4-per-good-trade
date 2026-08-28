# -*- coding: utf-8 -*-
"""r12/A2: is "cells sharing an owner sit at one ratio regardless of autonomy" true?
And what IS true of the owner-grouped control?"""
import os,re,sys,zipfile,collections,math
HERE=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")); sys.path.insert(0,HERE); os.chdir(HERE)
from solver import ROWS
EU4=r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
SAVE=r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\VANILLA_start.eu4"
GOODS=re.findall(r"^([a-z_]+) = \{", open(os.path.join(EU4,"common","tradegoods","00_tradegoods.txt"),encoding="latin-1").read(), re.M)
raw=zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")
def mb(s,i):
    d=0;k=i;q=False
    while k<len(s):
        c=s[k]
        if c=='"': q=not q
        elif not q:
            if c=="{": d+=1
            elif c=="}":
                d-=1
                if d==0: return k
        k+=1
    return len(s)-1
i1=raw.index("\nprovinces={"); j1=raw.index("{",i1); pb=raw[j1+1:mb(raw,j1)]
OWN={};AUT={}
for mm in re.finditer(r"^-(\d+)=\{", pb, re.M):
    pid=int(mm.group(1)); s2=pb.index("{",mm.start()); blk=pb[s2+1:mb(pb,s2)]
    m=re.search(r'^\t\towner="([A-Z]{3})"',blk,re.M); OWN[pid]=m.group(1) if m else None
    a=re.search(r"^\t\tlocal_autonomy=([\d.]+)",blk,re.M); AUT[pid]=float(a.group(1)) if a else 0.0
i2=raw.index("\ntrade={"); j2=raw.index("{",i2); tb=raw[j2+1:mb(raw,j2)]
ENG={}
for mm in re.finditer(r"^\tnode=\{", tb, re.M):
    s2=tb.index("{",mm.start()); nd=tb[s2+1:mb(tb,s2)]
    nm=re.search(r'definitions="([a-z_]+)"',nd).group(1)
    b=re.search(r"trade_goods_size=\{([^}]*)\}",nd,re.S); sz=[float(x) for x in b.group(1).split()] if b else []
    for k in range(1,min(len(sz),len(GOODS)+1)):
        if sz[k]: ENG[(nm,GOODS[k-1])]=sz[k]
cells=collections.defaultdict(list)
for r in ROWS: cells[(r["node"],r["good"])].append(r)
byowner=collections.defaultdict(list)
for k,v in cells.items():
    if len(v)!=1 or k not in ENG: continue
    r=v[0]
    if r["gp"]<=0: continue
    byowner[OWN.get(r["pid"])].append(dict(ratio=ENG[k]/r["gp"], aut=AUT.get(r["pid"],0.0), cell=k, pid=r["pid"]))

print("=== TEST 1: 'cells sharing an owner sit at one ratio regardless of autonomy' (as written) ===")
multi={t:v for t,v in byowner.items() if len(v)>=2}
one=[t for t,v in multi.items() if len(set(round(x['ratio'],3) for x in v))==1]
print("  owners with >=2 singleton cells      : %d" % len(multi))
print("  of those, ALL cells at one ratio(3dp): %d  (%.0f%%)" % (len(one), 100.0*len(one)/len(multi)))
print("  -> the universal is FALSE for %d owners" % (len(multi)-len(one)))
bad=sorted(((len(v),t,sorted(set(round(x['ratio'],4) for x in v))) for t,v in multi.items() if t not in one), reverse=True)[:8]
for n,t,rs in bad: print("     %-4s n=%-3d ratios=%s" % (t,n,rs))

print()
print("=== TEST 2: the control that actually has force — owners whose cells SPAN autonomy ===")
print("    (an owner-group is only a control on autonomy if its cells differ in autonomy)")
span=[(t,v) for t,v in byowner.items() if len(v)>=2 and (max(x['aut'] for x in v)-min(x['aut'] for x in v))>=20.0]
print("  owners with >=2 cells spanning >=20 autonomy points: %d" % len(span))
ok=0
for t,v in sorted(span, key=lambda z:-(max(x['aut'] for x in z[1])-min(x['aut'] for x in z[1]))):
    rs=sorted(set(round(x['ratio'],3) for x in v)); flat=(len(rs)==1)
    ok+=flat
    print("    %-4s n=%-2d aut %5.1f..%5.1f  ratios=%-26s %s" % (t,len(v),min(x['aut'] for x in v),max(x['aut'] for x in v),str(rs),"FLAT" if flat else "NOT FLAT"))
print("  flat within owner: %d of %d" % (ok,len(span)))

print()
print("=== TEST 3: within-owner correlation of ratio with autonomy (the honest population control) ===")
xs=[];ys=[]
for t,v in byowner.items():
    if len(v)<2: continue
    ma=sum(x['aut'] for x in v)/len(v); mr=sum(x['ratio'] for x in v)/len(v)
    for x in v: xs.append(x['aut']-ma); ys.append(x['ratio']-mr)
def pear(a,b):
    n=len(a); mx=sum(a)/n; my=sum(b)/n
    sx=math.sqrt(sum((u-mx)**2 for u in a)); sy=math.sqrt(sum((u-my)**2 for u in b))
    return sum((u-mx)*(w-my) for u,w in zip(a,b))/(sx*sy)
print("  cells in multi-cell owner groups: %d over %d owners" % (len(xs), len(multi)))
print("  within-owner (owner-demeaned) r(autonomy, ratio) = %+.4f" % pear(xs,ys))
print()
print("=== GEO, verbatim ===")
for x in sorted(byowner['GEO'], key=lambda z:z['aut']):
    print("    %-22s pid %-5d aut %5.1f%%  ratio %.4f" % (str(x['cell']),x['pid'],x['aut'],x['ratio']))
