import zipfile,os,re,glob
base=os.path.join(os.path.expanduser("~"),"OneDrive","Documents","Paradox Interactive","Europa Universalis IV","save games")
for fn in ("VANILLA_start.eu4","VANILLA2_start.eu4","Castile1444_12_22.eu4"):
    p=os.path.join(base,fn)
    if not os.path.exists(p): print(fn,"missing"); continue
    try: raw=zipfile.ZipFile(p).read("gamestate").decode("latin-1")
    except Exception as e: print(fn,"unreadable",e); continue
    seg=raw[raw.find("\ntrade="):]
    starts=[(m.group(1),m.start()) for m in re.finditer(r'definitions="([a-z_]+)"',seg)]
    print("=== %s ==="%fn)
    for k,(name,s) in enumerate(starts):
        if name not in ("sevilla","venice"): continue
        e=starts[k+1][1] if k+1<len(starts) else s+80000
        blk=seg[s:e]
        pp=re.search(r'pull_power=([-\d.]+)',blk)
        print("  %s pull_power=%s"%(name,pp.group(1) if pp else None))
        vals={}
        for m in re.finditer(r'\n\t\t([A-Z0-9]{3})=\{',blk):
            tag=m.group(1); st=m.end(); depth=1; j=st
            while depth>0 and j<len(blk):
                if blk[j]=='{': depth+=1
                elif blk[j]=='}': depth-=1
                j+=1
            sub=blk[st:j]
            v=re.search(r'val=([-\d.]+)',sub); t=re.search(r'type=(\d+)',sub); mo=re.search(r'money=([-\d.]+)',sub)
            if v: vals[tag]=(float(v.group(1)), t.group(1) if t else None, mo.group(1) if mo else None)
        tot=sum(v for v,_,_ in vals.values())
        coll=[k2 for k2,(v,t,mo) in vals.items() if mo is not None]
        noncoll=sum(v for k2,(v,t,mo) in vals.items() if mo is None)
        print("     countries with val: %d ; sum %.3f ; collectors(money) %s ; non-collector sum %.3f"%(len(vals),tot,coll,noncoll))
        print("     top vals:",sorted(vals.items(),key=lambda x:-x[1][0])[:6])
