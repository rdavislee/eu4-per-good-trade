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

total_qual = 0
miss2 = 0
eng_ches = None
for n in ND["order"]:
    for c,d in info.get(n,{}).items():
        if d.get("province_power") or d["trader"] or d["light_ship"]: continue
        pred=sum(info.get(m2,{}).get(c,{}).get("province_power",0.0)/DIV
                 for m2 in OUT.get(n,[]) if info.get(m2,{}).get(c,{}).get("province_power",0.0)>=RAWTHR)
        got=d.get("max_pow",0.0)
        if pred>0:
            total_qual+=1
            if got==0.0:
                miss2+=1
                if n=="chesapeake_bay" and c=="ENG":
                    eng_ches=(pred,got)
print("total qualifying pairs:", total_qual)
print("missing:", miss2)
print("eng chesapeake_bay pred/got:", eng_ches)
print("ENG in english_channel:", info.get("english_channel",{}).get("ENG"))
