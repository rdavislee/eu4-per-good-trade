import zipfile,os,re,json,statistics
base=os.path.join(os.path.expanduser("~"),"OneDrive","Documents","Paradox Interactive","Europa Universalis IV","save games")
raw=zipfile.ZipFile(os.path.join(base,"VANILLA_start.eu4")).read("gamestate").decode("latin-1")
seg=raw[raw.find("\ntrade="):]
st=[(m.group(1),m.start()) for m in re.finditer(r'definitions="([a-z_]+)"',seg)]
tot={}; countries={}
for k,(n,s) in enumerate(st):
    e=st[k+1][1] if k+1<len(st) else len(seg)
    blk=seg[s:e]
    m=re.search(r'\n\t*total=([-\d.]+)',blk)
    if m: tot[n]=float(m.group(1))
    cs={}
    for mm in re.finditer(r'\n\t\t([A-Z0-9]{3})=\{',blk):
        tag=mm.group(1); a=mm.end(); d=1; j=a
        while d>0 and j<len(blk):
            if blk[j]=='{': d+=1
            elif blk[j]=='}': d-=1
            j+=1
        v=re.search(r'val=([-\d.]+)',blk[a:j])
        if v: cs[tag]=float(v.group(1))
    countries[n]=cs
EU4=r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
txt=open(os.path.join(EU4,"common","tradenodes","00_tradenodes.txt"),encoding="latin-1").read().split("\n")
inl=[]; depth=0; cur=None
for l in txt:
    s2=l.strip(); m=re.match(r'^([a-z_]+)\s*=\s*\{',s2)
    if depth==0 and m: cur=m.group(1)
    if s2=='inland=yes': inl.append(cur)
    depth+=l.count('{')-l.count('}')
print("flagged inland nodes:",len(inl))
vals=[(n,tot.get(n)) for n in inl]
vals=[(n,v) for n,v in vals if v]
print("with totals:",len(vals))
sh=sorted((50.0/v*100,n,v) for n,v in vals)
print("min %.1f%% (%s %.1f) max %.1f%% (%s %.1f)"%(sh[0][0],sh[0][1],sh[0][2],sh[-1][0],sh[-1][1],sh[-1][2]))
print("median %.1f%%"%statistics.median(x[0] for x in sh))
sh2=sorted(50.0/(v+50)*100 for n,v in vals)
print("after-grant: min %.1f%% max %.1f%% median %.1f%%"%(sh2[0],sh2[-1],statistics.median(sh2)))
print("totals: xian=%.1f champagne=%.1f"%(tot.get('xian',0),tot.get('champagne',0)))
inc=[max(countries[n].values()) for n,_ in vals if countries.get(n)]
print("largest incumbent range: %.1f to %.1f"%(min(inc),max(inc)))
print("cap outweighs largest incumbent in %d of %d"%(sum(1 for x in inc if 50>x),len(inc)))
