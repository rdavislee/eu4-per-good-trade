import zipfile,os,re
p=os.path.join(os.path.expanduser("~"),"OneDrive","Documents","Paradox Interactive","Europa Universalis IV","save games","VANILLA_start.eu4")
raw=zipfile.ZipFile(p).read("gamestate").decode("latin-1")
i=raw.find("\ntrade=")
seg=raw[i:]
starts=[(m.group(1),m.start()) for m in re.finditer(r'definitions="([a-z_]+)"',seg)]
for k,(name,s) in enumerate(starts):
    if name!="sevilla": continue
    e=starts[k+1][1] if k+1<len(starts) else s+80000
    blk=seg[s:e]
    print("block len",len(blk))
    for m in re.finditer(r'pull_power=([-\d.]+)',blk): print("  pull_power",m.group(1),"at",m.start())
    for tag in ("FRA","ARA","CAS","POR"):
        for m in re.finditer(r'\n\t*%s=\{'%tag,blk):
            st=m.end(); depth=1; j=st
            while depth>0 and j<len(blk):
                if blk[j]=='{': depth+=1
                elif blk[j]=='}': depth-=1
                j+=1
            print("  ---",tag,"---"); print("   ",blk[st:j].replace("\n"," ")[:400])
