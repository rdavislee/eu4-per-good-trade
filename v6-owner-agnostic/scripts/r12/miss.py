import os,re,sys,zipfile,collections
HERE=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
sys.path.insert(0,HERE); os.chdir(HERE)
from solver import ROWS, PROV, ON_STARTUP_DEVASTATION
SAVE=r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\VANILLA_start.eu4"
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
want={4511,675,2196,422,213}
blocks={}
for mm in re.finditer(r"^-(\d+)=\{", pb, re.M):
    pid=int(mm.group(1))
    if pid in want:
        s2=pb.index("{",mm.start()); blocks[pid]=pb[s2+1:mb(pb,s2)]
for pid in (213,4511,675,2196,422):
    b=blocks[pid]
    keys=["name","owner","trade_goods","base_production","local_autonomy","devastation","prosperity",
          "trade_power","center_of_trade","buildings","territorial_core","active_trade_company","hre"]
    out=[]
    for k in keys:
        m=re.search(r"^\t\t%s=(.*)$"%k, b, re.M)
        if m: out.append("%s=%s"%(k,m.group(1).strip()[:70]))
    print("pid %-5d %s" % (pid, " | ".join(out)))
    print("        model gp=%s  devastation in solver dict=%s" % ([r['gp'] for r in ROWS if r['pid']==pid], ON_STARTUP_DEVASTATION.get(pid)))
print()
# owner ruler personalities / country goods-produced modifiers for the owners of the miss cells
i3=raw.index("\ncountries={"); j3=raw.index("{",i3); cb=raw[j3+1:mb(raw,j3)]
owners=set()
for pid in (4511,675,2196,422,213):
    m=re.search(r'^\t\towner="([A-Z]{3})"', blocks[pid], re.M)
    if m: owners.add((pid,m.group(1)))
print("owners:",owners)
for pid,tag in sorted(owners):
    mm=re.search(r'^\t%s=\{'%tag, cb, re.M)
    s2=cb.index("{",mm.start()); blk=cb[s2+1:mb(cb,s2)]
    pers=re.findall(r"(\w*personality\w*)=?\{?([^}\n]*)", blk)[:0]
    p2=re.findall(r"^\t\t\t(\w+_personality)", blk, re.M)
    print("  %s (pid %d) ruler personalities: %s" % (tag,pid,sorted(set(p2))))
    for key in ("global_trade_goods_size_modifier","trade_goods_size"):
        print("     %s occurrences in country block: %d" % (key, blk.count(key)))
