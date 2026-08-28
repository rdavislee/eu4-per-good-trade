import zipfile, re, json, os, collections
HERE=os.path.dirname(os.path.abspath(__file__))
SAVE=os.path.join(os.path.expanduser("~"),"OneDrive","Documents","Paradox Interactive","Europa Universalis IV","save games","VANILLA_start.eu4")
raw=zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")
def mb(s,i):
    d=0;k=i;inq=False
    while k<len(s):
        c=s[k]
        if c=='"': inq=not inq
        elif not inq:
            if c=='{': d+=1
            elif c=='}':
                d-=1
                if d==0: return k
        k+=1
    return len(s)-1
i=raw.index('\ntrade={'); j=raw.index('{',i); trade=raw[j+1:mb(raw,j)]
nodes={}
for m in re.finditer(r'\tnode=\{', trade):
    st=trade.index('{',m.start()); blk=trade[st+1:mb(trade,st)]
    nodes[re.search(r'definitions="([^"]+)"',blk).group(1)]=blk
ND=json.load(open(os.path.join(HERE,"nodes.json")))
OUT={n:ND["nodes"][n]["outgoing"] for n in ND["order"]}
info={}
for name,blk in nodes.items():
    ents={}
    for m in re.finditer(r'^\t\t([A-Z][A-Z0-9]{2})=\{',blk,re.M):
        st=blk.index('{',m.start()); body=blk[st+1:mb(blk,st)]
        d={}
        for k in ("val","max_pow","province_power","ship_power","already_sent"):
            g=re.search(r'^\t*%s=([\d.\-]+)'%k,body,re.M)
            if g: d[k]=float(g.group(1))
        d["trader"]="has_trader=yes" in body
        d["light_ship"]="light_ship=" in body
        ents[m.group(1)]=d
    info[name]=ents
DIV,RAWTHR=5.0,10.0
# per-node: does anybody receive propagation there?
miss=collections.Counter(); nodes_with_recv=set()
for n in ND["order"]:
    for c,d in info.get(n,{}).items():
        if d.get("province_power") or d["trader"] or d["light_ship"]: continue
        if d.get("max_pow",0.0)>0: nodes_with_recv.add(n)
missing=[]
for n in ND["order"]:
    for c,d in info.get(n,{}).items():
        if d.get("province_power") or d["trader"] or d["light_ship"]: continue
        pred=sum(info.get(m2,{}).get(c,{}).get("province_power",0.0)/DIV
                 for m2 in OUT.get(n,[]) if info.get(m2,{}).get(c,{}).get("province_power",0.0)>=RAWTHR)
        got=d.get("max_pow",0.0)
        if pred>0 and got==0.0:
            missing.append((n,c,round(pred,3)))
            miss[n]+=1
print("nodes where SOMEBODY receives propagation:", len(nodes_with_recv), "of", len(ND["order"]))
print("total missing (pred>0, got=0):", len(missing))
print("missing by node:", dict(miss))
print("do those nodes have any receiver at all?:", {n:(n in nodes_with_recv) for n in miss})
# ship power propagation: entries with ship_power but no province_power upstream
# and the propagation multiple check: got/pred ratios
ratios=collections.Counter()
for n in ND["order"]:
    for c,d in info.get(n,{}).items():
        if d.get("province_power") or d["trader"] or d["light_ship"]: continue
        got=d.get("max_pow",0.0)
        if got<=0: continue
        srcs=[(m2,info.get(m2,{}).get(c,{}).get("province_power",0.0)) for m2 in OUT.get(n,[])]
        tot=sum(pp for _,pp in srcs if pp>=RAWTHR)
        if tot>0: ratios[round(tot/got,3)]+=1
print("province_power_sum / received ratio histogram:", dict(ratios))
# threshold bracket restricted to nodes that DO have receivers
lo=[];hi=[]
for n in nodes_with_recv:
    for m2 in OUT.get(n,[]):
        for c,d1 in info.get(m2,{}).items():
            pp=d1.get("province_power",0.0)
            if pp<=0: continue
            others=[mm for mm in OUT.get(n,[]) if mm!=m2 and info.get(mm,{}).get(c,{}).get("province_power",0.0)>0]
            if others: continue
            e=info.get(n,{}).get(c)
            recv = e is not None and not (e.get("province_power") or e["trader"] or e["light_ship"]) and e.get("max_pow",0.0)>0
            (hi if recv else lo).append((pp,n,c))
lo.sort(); hi.sort()
print("largest pp NOT propagating (in live nodes):", lo[-3:] if lo else None)
print("smallest pp propagating:", hi[:3] if hi else None)
