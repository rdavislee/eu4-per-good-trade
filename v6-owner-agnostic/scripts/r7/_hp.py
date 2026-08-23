import zipfile,os,re
base=os.path.join(os.path.expanduser("~"),"OneDrive","Documents","Paradox Interactive","Europa Universalis IV","save games")
raw=zipfile.ZipFile(os.path.join(base,"VANILLA_start.eu4")).read("gamestate").decode("latin-1")
seg=raw[raw.find("\ntrade="):]
st=[(m.group(1),m.start()) for m in re.finditer(r'definitions="([a-z_]+)"',seg)]
n_eq=0; n_have=0; rows=[]
for k,(n,s) in enumerate(st):
    e=st[k+1][1] if k+1<len(st) else len(seg)
    blk=seg[s:e]
    hp=re.search(r'\n\t*highest_power=([-\d.]+)',blk)
    cs={}
    for mm in re.finditer(r'\n\t\t([A-Z0-9]{3})=\{',blk):
        tag=mm.group(1); a=mm.end(); d=1; j=a
        while d>0 and j<len(blk):
            if blk[j]=='{': d+=1
            elif blk[j]=='}': d-=1
            j+=1
        v=re.search(r'val=([-\d.]+)',blk[a:j])
        if v: cs[tag]=float(v.group(1))
    if hp and cs:
        n_have+=1
        mx=max(cs.values())
        if abs(float(hp.group(1))-mx)<1e-9: n_eq+=1
        rows.append((n,float(hp.group(1)),mx))
print("nodes with highest_power and country blocks:",n_have)
print("highest_power == largest single country's val on %d of %d"%(n_eq,n_have))
for n,h,m in rows:
    if n in ("venice","sevilla","genua"): print("  %-10s highest_power=%.3f largest val=%.3f"%(n,h,m))
