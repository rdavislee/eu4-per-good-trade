import zipfile, re, os
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
tg = open(os.path.join(EU4,"common","tradegoods","00_tradegoods.txt"),encoding="latin-1").read()
ORDERG = re.findall(r"^([a-z_]+) = \{", tg, re.M)
SG = os.path.join(os.path.expanduser("~"),"OneDrive","Documents","Paradox Interactive",
                  "Europa Universalis IV","save games","VANILLA_start.eu4")
raw = zipfile.ZipFile(SG).read("gamestate").decode("latin-1")
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
m=re.search(r"^change_price=\{",raw,re.M); st=raw.index("{",m.start()); pb=raw[st+1:mb(raw,st)]
CUR={}
for mm in re.finditer(r"^\t([a-z_]+)=\{",pb,re.M):
    s2=pb.index("{",mm.start()); blk=pb[s2+1:mb(pb,s2)]
    cp=re.search(r"current_price=([\d.]+)",blk)
    if cp: CUR[mm.group(1)]=float(cp.group(1))
i2=raw.index(chr(10)+"trade={"); j2=raw.index("{",i2); tb=raw[j2+1:mb(raw,j2)]
tot_lv=0.0; tot_raw=0.0
for mm in re.finditer(r"^\tnode=\{",tb,re.M):
    s2=tb.index("{",mm.start()); nd=tb[s2+1:mb(tb,s2)]
    name=re.search(r'definitions="([^"]+)"',nd).group(1)
    lvm=re.search(r"^\t\tlocal_value=(.*)$",nd,re.M)
    lv=float(lvm.group(1)) if lvm else 0.0
    blk=re.search(r"trade_goods_size=\{([^}]*)\}",nd,re.S)
    sz=[float(x) for x in blk.group(1).split()] if blk else []
    r_=sum(sz[i]*CUR.get(ORDERG[i-1],0.0) for i in range(1,min(len(sz),len(ORDERG)+1)))
    tot_lv+=lv; tot_raw+=r_
    if name in ("sevilla","genua"):
        print("  %-8s local_value(month)=%7.3f   size*price (A2's inject)=%8.3f   ratio %.2f" % (name,lv,r_,r_/lv))
print("world  Σlocal_value(month)=%8.3f   Σsize*price=%9.3f   ratio %.2f" % (tot_lv,tot_raw,tot_raw/tot_lv))
print("world  Σsize*price/12    =%8.3f   (A8's reconstruction; %.2f%% vs local_value)" % (tot_raw/12.0, 100*(tot_raw/12.0-tot_lv)/tot_lv))
