import zipfile, re, os, sys, json
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
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
i=raw.index(chr(10)+"provinces={"); j=raw.index("{",i); body=raw[j+1:mb(raw,j)]
recs={}
for m in re.finditer(r"^-(\d+)=\{",body,re.M):
    st=body.index("{",m.start()); recs[int(m.group(1))]=body[st+1:mb(body,st)]
def f(rec,key):
    g=re.search(r'^\t\t%s="?([A-Za-z0-9_.\-]+)'%key,rec,re.M); return g.group(1) if g else None
PROV={int(k):v for k,v in json.load(open(os.path.join(HERE,"prov1444.json"))).items()}
ND=json.load(open(os.path.join(HERE,"nodes.json")))
PNODE={p:n for n in ND["order"] for p in ND["nodes"][n]["members"]}
counted=[p for p,s in PROV.items() if s.get("owner") and p in PNODE]
occ=[];prosp=[];siege=[];unr=[]
for p in counted:
    r=recs.get(p)
    if r is None: continue
    o=f(r,"owner"); c=f(r,"controller")
    if o and c and o!=c: occ.append((p,o,c))
    pr=f(r,"prosperity")
    if pr and float(pr)!=0.0: prosp.append((p,pr))
    if re.search(r'^\t\tsiege=',r,re.M): siege.append(p)
    for key in ("unrest","revolt_risk","nationalism","local_unrest"):
        v=f(r,key)
        if v and float(v)!=0.0: unr.append((p,key,v))
print("counted:",len(counted))
print("occupied (controller != owner):",len(occ),occ[:5])
print("prosperity nonzero:",len(prosp),prosp[:5])
print("under siege:",len(siege),siege[:5])
print("unrest-ish nonzero:",len(unr),unr[:8])
# field names present in a sample record
print("sample fields:",sorted(set(re.findall(r'^\t\t([a-z_]+)=',recs[223],re.M))))
# devastated province names via localisation
LOC=os.path.join(r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV","localisation","prov_names_l_english.yml")
lt=open(LOC,encoding='utf-8-sig',errors='replace').read()
DEV={266:50,2968:50,2970:50,4724:50,4725:50,265:20,267:20,1771:20,2967:20,4237:20,4726:20}
for pid,lvl in sorted(DEV.items(), key=lambda kv:(-kv[1],kv[0])):
    m=re.search(r'^ PROV%d:0 "([^"]*)"'%pid,lt,re.M)
    print("  prov",pid,"dev",lvl,"=",m.group(1) if m else "?")
