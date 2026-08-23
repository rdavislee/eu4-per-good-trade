import zipfile,os,re,collections
def load(name):
    p=os.path.join(os.path.expanduser("~"),"OneDrive","Documents","Paradox Interactive","Europa Universalis IV","save games",name)
    return zipfile.ZipFile(p).read("gamestate").decode("latin-1")
def nodes(raw):
    i=raw.find("\ntrade=")
    seg=raw[i:]
    out={}
    # node blocks: definitions=name then fields
    for m in re.finditer(r'definitions="([a-z_]+)"',seg):
        name=m.group(1); s=m.end(); e=seg.find('definitions="',s)
        blk=seg[s:e if e>0 else s+40000]
        d={}
        for k in ("current","local_value","outgoing","total","retention","max","p_pow","collector_power","max_pow","pull_power","highest_power"):
            mm=re.search(r'\n\t*%s=([-\d.]+)'%k,blk)
            if mm: d[k]=float(mm.group(1))
        out[name]=d
    return out
A=nodes(load("VANILLA_start.eu4")); B=nodes(load("VANILLA2_start.eu4"))
print("nodes A/B:",len(A),len(B))
FIELDS=["current","local_value","outgoing","total","retention"]
diffnodes=set(); worst=0; worstinfo=None
per=collections.Counter()
for n in A:
    if n not in B: continue
    for f in FIELDS:
        a=A[n].get(f); b=B[n].get(f)
        if a is None or b is None: continue
        if a!=b:
            diffnodes.add(n); per[f]+=1
            if a!=0:
                r=abs(a-b)/abs(a)*100
                if r>worst: worst=r; worstinfo=(n,f,a,b)
print("nodes differing on any of the 5 fields:",len(diffnodes),"of",len(A))
print("worst relative diff: %.4f%%"%worst, worstinfo)
print("per-field differing node counts:",dict(per))
# retention identical?
same_ret=sum(1 for n in A if n in B and A[n].get('retention')==B[n].get('retention'))
have_ret=sum(1 for n in A if n in B and 'retention' in A[n] and 'retention' in B[n])
print("retention identical on %d of %d (have %d)"%(same_ret,len(A),have_ret))
tot_same=[n for n in A if n in B and 'total' in A[n] and 'total' in B[n] and A[n]['total']==B[n]['total']]
tot_have=[n for n in A if n in B and 'total' in A[n] and 'total' in B[n]]
print("total identical on %d of %d"%(len(tot_same),len(tot_have)))
for n in tot_have:
    if n not in tot_same:
        a,b=A[n]['total'],B[n]['total']; print("  total differs:",n,a,b,"%.4f%%"%(abs(a-b)/abs(a)*100 if a else 0))
# quantisation
vals=[]; 
for n in A:
    for k in ("total","p_pow","retention","collector_power","max_pow"):
        if k in A[n]: vals.append(A[n][k])
ok=sum(1 for v in vals if abs(v*1000-round(v*1000))<1e-6)
print("quantisation: %d of %d sampled values on the 1/1000 grid"%(ok,len(vals)))
