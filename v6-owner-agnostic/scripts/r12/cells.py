import os,re,sys,zipfile,collections
HERE=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
sys.path.insert(0,HERE); os.chdir(HERE)
from solver import ROWS, PROV
import nodes as NODESMOD
EU4=r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
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
SP={}
for mm in re.finditer(r"^-(\d+)=\{", pb, re.M):
    pid=int(mm.group(1)); s2=pb.index("{",mm.start()); blk=pb[s2+1:mb(pb,s2)]
    def g(p,d=None):
        m=re.search(p,blk,re.M); return m.group(1) if m else d
    SP[pid]=dict(name=g(r'^\t\tname="([^"]*)"'),tg=g(r'^\t\ttrade_goods="?([a-z_]+)"?'),
                 bp=float(g(r"^\t\tbase_production=([\d.]+)","0")),owner=g(r'^\t\towner="([A-Z]{3})"'),
                 aut=float(g(r"^\t\tlocal_autonomy=([\d.]+)","0")),
                 city=g(r"^\t\tis_city=(yes|no)"))
# node -> province members from the tradenodes file
tn=open(os.path.join(EU4,"common","tradenodes","00_tradenodes.txt"),encoding="latin-1").read()
def mb2(s,i): return mb(s,i)
NODEPROV={}
for mm in re.finditer(r"^([a-z_]+)=\{", tn, re.M):
    s2=tn.index("{",mm.start()); blk=tn[s2+1:mb(tn,s2)]
    mmm=re.search(r"members=\{([^}]*)\}",blk,re.S)
    NODEPROV[mm.group(1)]=[int(x) for x in mmm.group(1).split()] if mmm else []
modelcells=collections.defaultdict(list)
for r in ROWS: modelcells[(r["node"],r["good"])].append(r["pid"])
for node,good in [("chengdu","copper"),("crimea","fish"),("crimea","cloth"),("lahore","salt"),("valencia","glass")]:
    engprovs=[p for p in NODEPROV.get(node,[]) if SP.get(p,{}).get("tg")==good]
    print("%s / %s" % (node,good))
    print("   model provinces : %s" % modelcells[(node,good)])
    print("   save provinces in node with that good:")
    for p in engprovs:
        s=SP[p]
        print("      pid %-5d %-16s bp=%-5s owner=%-4s aut=%-5s is_city=%-4s  -> 0.2*bp = %.3f" % (p,s["name"],s["bp"],s["owner"],s["aut"],s["city"],0.2*s["bp"]))
    print("   sum 0.2*bp over ALL save provinces with that good in the node: %.3f" % sum(0.2*SP[p]["bp"] for p in engprovs))
    print("   sum over is_city=yes only                                   : %.3f" % sum(0.2*SP[p]["bp"] for p in engprovs if SP[p]["city"]=="yes"))
    print()
