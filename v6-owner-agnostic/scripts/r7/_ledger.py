import zipfile,os,re
p=os.path.join(os.path.expanduser("~"),"OneDrive","Documents","Paradox Interactive","Europa Universalis IV","save games","VANILLA_start.eu4")
raw=zipfile.ZipFile(p).read("gamestate").decode("latin-1")
i=raw.find("\ntrade=")
seg=raw[i:]
starts=[(m.group(1),m.start()) for m in re.finditer(r'definitions="([a-z_]+)"',seg)]
for name,s in starts:
    if name not in ("sevilla","venice"): continue
    e=[t for (_n,t) in starts if t>s]
    blk=seg[s:(e[0] if e else s+60000)]
    pp=re.search(r'\n\t*pull_power=([-\d.]+)',blk)
    print("=== %s ===  pull_power=%s"%(name, pp.group(1) if pp else None))
    # country sub-blocks: TAG={ ... }
    for m in re.finditer(r'\n\t\t([A-Z0-9]{3})=\{',blk):
        tag=m.group(1); st=m.end(); depth=1; j=st
        while depth>0 and j<len(blk):
            if blk[j]=='{': depth+=1
            elif blk[j]=='}': depth-=1
            j+=1
        sub=blk[st:j]
        d={}
        for k in ("val","money","collector_power","type","t_in","t_out","privateer_money","has_trader","has_capital","light_ship"):
            mm=re.search(r'\n?\t*%s=([-\d."A-Za-z]+)'%k,sub)
            if mm: d[k]=mm.group(1)
        print("   %s %s"%(tag,d))
