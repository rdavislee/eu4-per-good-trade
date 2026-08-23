import os,re,sys,zipfile,collections
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
    byowner[OWN.get(r["pid"])].append((ENG[k]/r["gp"], k, r["pid"], AUT.get(r["pid"],0.0)))
print("owner-level ratio consistency over the 245 singleton cells:")
print("%-5s %-4s %-8s %s" % ("tag","n","distinct ratios (rounded 4dp)","mean aut"))
for tag in sorted(byowner, key=lambda t:-len(byowner[t]))[:14]:
    v=byowner[tag]; rs=sorted(set(round(x[0],4) for x in v))
    print("  %-5s n=%-3d ratios=%s  mean_aut=%.1f" % (tag,len(v),rs[:6],sum(x[3] for x in v)/len(v)))
print()
for tag in ("MNG","GEO","SRH","ARA"):
    v=byowner.get(tag,[])
    print("%s: n=%d  ratios=%s" % (tag,len(v),sorted(set(round(x[0],4) for x in v))))
    if tag in ("GEO","SRH","ARA"):
        for ratio,k,pid,aut in sorted(v): print("     %-20s pid %-5d aut %5.1f ratio %.4f" % (str(k),pid,aut,ratio))
# is the ratio constant within owner? -> owner-level modifier, not autonomy
const=sum(1 for t,v in byowner.items() if len(set(round(x[0],4) for x in v))==1)
print("\nowners whose singleton cells ALL share one ratio: %d of %d owners with >=1 cell" % (const,len(byowner)))
multi={t:v for t,v in byowner.items() if len(v)>=3}
constm=sum(1 for t,v in multi.items() if len(set(round(x[0],4) for x in v))==1)
print("owners with >=3 cells: %d ; of those all-one-ratio: %d" % (len(multi),constm))
