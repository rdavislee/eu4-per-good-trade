"""Recover the trade_goods_size slot -> good mapping empirically."""
import zipfile, re, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import ROWS, NIDX, ORDER
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
tg = open(os.path.join(EU4, "common", "tradegoods", "00_tradegoods.txt"), encoding="latin-1").read()
ORDERG = re.findall(r"^([a-z_]+) = \{", tg, re.M)
SG = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                  "Europa Universalis IV", "save games", "VANILLA_start.eu4")
raw = zipfile.ZipFile(SG).read("gamestate").decode("latin-1")
def mb(s, i):
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
i2=raw.index(chr(10)+"trade={"); j2=raw.index("{", i2); tb=raw[j2+1:mb(raw,j2)]
ns={}
for mm in re.finditer(r"^\tnode=\{", tb, re.M):
    s2=tb.index("{", mm.start()); nd=tb[s2+1:mb(tb,s2)]
    name=re.search(r'definitions="([^"]+)"', nd).group(1)
    blk=re.search(r"trade_goods_size=\{([^}]*)\}", nd, re.S)
    ns[name]=[float(x) for x in blk.group(1).split()] if blk else []
NSLOT=len(next(iter(ns.values())))
# model-side: which nodes hold at least one province of good g
gnodes=collections.defaultdict(set)
for r in ROWS: gnodes[r["good"]].add(r["node"])
slotnodes={k:set(n for n,v in ns.items() if len(v)>k and v[k]>0) for k in range(NSLOT)}
print("slots:", NSLOT, "| goods in file:", len(ORDERG))
mapping={}
for k in range(NSLOT):
    best=None
    for g in set(list(gnodes)+ORDERG):
        a=slotnodes[k]; b=gnodes.get(g,set())
        if not a and not b: continue
        j=len(a&b)/max(1,len(a|b))
        if best is None or j>best[0]: best=(j,g)
    mapping[k]=best
    if best and best[0]>0:
        print("  slot %2d  jaccard %.3f  -> %-16s (slot nodes %d, good nodes %d)" % (k, best[0], best[1], len(slotnodes[k]), len(gnodes.get(best[1],set()))))
    else:
        print("  slot %2d  all-zero / unmatched" % k)
