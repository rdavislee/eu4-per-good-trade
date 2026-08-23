# -*- coding: utf-8 -*-
"""r12 independent probe: the autonomy half of 3.4's evidence note.
Y1366 (autonomy-heavy provinces reproduce the autonomy-free prediction exactly),
Y1367 (Barcelona pid 213, valencia-node glass cell, 91% local_autonomy),
Y1369 (r(local_autonomy, engine/model ratio) = -0.1 over 245 singleton cells)."""
import os, re, sys, zipfile, collections, math
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, HERE); os.chdir(HERE)
from solver import ROWS, PROV, GOODS_PRODUCED_FACTOR, ON_STARTUP_DEVASTATION, STATE_GOODS_MOD
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
SAVE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\VANILLA_start.eu4"
GOODS = re.findall(r"^([a-z_]+) = \{", open(os.path.join(EU4,"common","tradegoods","00_tradegoods.txt"),encoding="latin-1").read(), re.M)
raw = zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")
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
# provinces
i1=raw.index("\nprovinces={"); j1=raw.index("{",i1); pb=raw[j1+1:mb(raw,j1)]
AUT={}; OWN={}; NAME={}; TG={}; BP={}
for mm in re.finditer(r"^-(\d+)=\{", pb, re.M):
    pid=int(mm.group(1)); s2=pb.index("{",mm.start()); blk=pb[s2+1:mb(pb,s2)]
    def g(pat):
        m=re.search(pat, blk, re.M); return m.group(1) if m else None
    AUT[pid]=float(g(r"^\t\tlocal_autonomy=([\d.]+)") or 0.0)
    OWN[pid]=g(r'^\t\towner="([A-Z]{3})"')
    NAME[pid]=g(r'^\t\tname="([^"]*)"')
    TG[pid]=g(r'^\t\ttrade_goods="?([a-z_]+)"?')
    BP[pid]=float(g(r"^\t\tbase_production=([\d.]+)") or 0.0)
print("=== Y1367: Barcelona, pid 213 ===")
for pid in (213,):
    print("  save name=%r owner=%r trade_goods=%r base_production=%s local_autonomy=%s"
          % (NAME[pid], OWN[pid], TG[pid], BP[pid], AUT[pid]))
prow=[r for r in ROWS if r["pid"]==213]
print("  model row(s) for pid 213: %s" % [{k:v for k,v in r.items() if k in ("pid","node","good","base_production","gp")} for r in prow])
# localisation name
import glob
loc=None
for f in glob.glob(os.path.join(EU4,"localisation","prov_names_l_english.yml")):
    for ln in open(f,encoding="utf-8-sig",errors="replace"):
        if re.match(r"\s*PROV213:", ln): loc=ln.strip()
print("  localisation prov_names PROV213: %s" % loc)
# engine node x good
i2=raw.index("\ntrade={"); j2=raw.index("{",i2); tb=raw[j2+1:mb(raw,j2)]
ENG={}
for mm in re.finditer(r"^\tnode=\{", tb, re.M):
    s2=tb.index("{",mm.start()); nd=tb[s2+1:mb(tb,s2)]
    nm=re.search(r'definitions="([a-z_]+)"',nd).group(1)
    b=re.search(r"trade_goods_size=\{([^}]*)\}",nd,re.S)
    sz=[float(x) for x in b.group(1).split()] if b else []
    for k in range(1,min(len(sz),len(GOODS)+1)):
        if sz[k]: ENG[(nm,GOODS[k-1])]=sz[k]
cells=collections.defaultdict(list)
for r in ROWS: cells[(r["node"],r["good"])].append(r)
sing={k:v[0] for k,v in cells.items() if len(v)==1 and k in ENG}
print("\n=== Y1369: singleton (node,good) cells ===")
print("  model (node,good) cells total          : %d" % len(cells))
print("  singleton cells                        : %d" % sum(1 for v in cells.values() if len(v)==1))
print("  singleton cells WITH an engine quantity: %d" % len(sing))
rows=[]
for k,r in sing.items():
    pred=r["gp"]
    if pred<=0: continue
    rows.append(dict(node=k[0],good=k[1],pid=r["pid"],aut=AUT.get(r["pid"],0.0),
                     pred=pred,eng=ENG[k],ratio=ENG[k]/pred))
def pear(xs,ys):
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    sx=math.sqrt(sum((x-mx)**2 for x in xs)); sy=math.sqrt(sum((y-my)**2 for y in ys))
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/(sx*sy)
print("  cells used (pred>0)                    : %d" % len(rows))
print("  Pearson r(local_autonomy, engine/model ratio) = %+.4f" % pear([r["aut"] for r in rows],[r["ratio"] for r in rows]))
print("  cells with ratio == 1.000 exactly      : %d of %d" % (sum(1 for r in rows if abs(r["ratio"]-1)<1e-9), len(rows)))
print("\n=== Y1366: do autonomy-heavy provinces reproduce the autonomy-free prediction exactly? ===")
for thr in (5,10,20,30,50,60,80,90):
    hi=[r for r in rows if r["aut"]>=thr]
    ex=sum(1 for r in hi if abs(r["ratio"]-1)<1e-9)
    print("  autonomy >= %2d%% : %3d cells, %3d exact (%s)" % (thr,len(hi),ex, ("%.0f%%"%(100.0*ex/len(hi))) if hi else "-"))
print("\n  every cell with autonomy >= 50%:")
for r in sorted([r for r in rows if r["aut"]>=50], key=lambda z:-z["aut"]):
    print("    %-18s %-12s pid %-5d aut %5.1f%%  model %.4f engine %.4f ratio %.4f  %s"
          % (r["node"],r["good"],r["pid"],r["aut"],r["pred"],r["eng"],r["ratio"],
             "EXACT" if abs(r["ratio"]-1)<1e-9 else "MISS"))
print("\n  baseline for comparison — cells with autonomy == 0:")
z=[r for r in rows if r["aut"]==0]
print("    %d cells, %d exact (%.0f%%)" % (len(z), sum(1 for r in z if abs(r["ratio"]-1)<1e-9), 100.0*sum(1 for r in z if abs(r["ratio"]-1)<1e-9)/len(z)))
# mean ratio by autonomy band
print("\n  mean engine/model ratio by autonomy band:")
band=collections.defaultdict(list)
for r in rows: band[min(int(r["aut"]//20)*20,80)].append(r["ratio"])
for b in sorted(band): print("    aut %2d-%2d%% n=%-4d mean ratio %.4f  median %.4f" % (b,b+19,len(band[b]),sum(band[b])/len(band[b]),sorted(band[b])[len(band[b])//2]))
