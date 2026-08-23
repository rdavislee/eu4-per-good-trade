"""Does vanilla's trade value carry production efficiency or autonomy?
Compare the engine's per-node per-good goods_produced against 0.2*base_production summed
over the model's provinces, and against autonomy in those provinces."""
import zipfile, re, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import ROWS, PROV, GOODS_PRODUCED_FACTOR
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
tg = open(os.path.join(EU4, "common", "tradegoods", "00_tradegoods.txt"), encoding="latin-1").read()
ORDERG = re.findall(r"^([a-z_]+) = \{", tg, re.M)
SG = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                  "Europa Universalis IV", "save games", "VANILLA_start.eu4")
raw = zipfile.ZipFile(SG).read("gamestate").decode("latin-1")
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
i2=raw.index(chr(10)+"trade={"); j2=raw.index("{",i2); tb=raw[j2+1:mb(raw,j2)]
eng=collections.defaultdict(float)
for mm in re.finditer(r"^\tnode=\{", tb, re.M):
    s2=tb.index("{",mm.start()); nd=tb[s2+1:mb(tb,s2)]
    name=re.search(r'definitions="([^"]+)"',nd).group(1)
    blk=re.search(r"trade_goods_size=\{([^}]*)\}",nd,re.S)
    sz=[float(x) for x in blk.group(1).split()] if blk else []
    for k in range(1,min(len(sz),len(ORDERG)+1)):
        if sz[k]: eng[(name,ORDERG[k-1])]+=sz[k]
mod=collections.defaultdict(float)
for r in ROWS:
    mod[(r["node"], r["good"])] += GOODS_PRODUCED_FACTOR*PROV[r["pid"]]["base_production"]
keys=set(eng)|set(mod)
exact=sum(1 for k in keys if abs(eng.get(k,0.0)-mod.get(k,0.0))<1e-6)
print("GOODS_PRODUCED_FACTOR (model GP_COEFF) =", GOODS_PRODUCED_FACTOR)
print("(node,good) cells:", len(keys), "| engine size == 0.2*base_production exactly:", exact,
      "(%.1f%%)" % (100.0*exact/len(keys)))
diff=sorted(((round(eng.get(k,0.0)-mod.get(k,0.0),3),k) for k in keys), key=lambda t:-abs(t[0]))
print("largest mismatches (engine - model):")
for d,k in diff[:10]: print("   %-34s %+8.3f  engine %.3f  model %.3f" % (str(k), d, eng.get(k,0.0), mod.get(k,0.0)))
# devastated provinces should be the model-side reduction; check Bohemia (node?)
dev=[r for r in ROWS if PROV[r["pid"]].get("devastation")]
print("model provinces carrying devastation:", len(dev))

low = [(round(eng.get(k,0.0)-mod.get(k,0.0),4), k) for k in keys if eng.get(k,0.0) - mod.get(k,0.0) < -1e-6]
print()
print("cells where the ENGINE quantity is LOWER than raw 0.2*base_production:", len(low))
for d,k in sorted(low)[:10]: print("   ", k, d)
tot_e = sum(eng.values()); tot_m = sum(mod.values())
print("world engine goods_produced %.2f  vs raw 0.2*base_production %.2f  (ratio %.4f)" % (tot_e, tot_m, tot_e/tot_m))
