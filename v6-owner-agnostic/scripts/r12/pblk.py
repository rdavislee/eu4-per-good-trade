import re,zipfile
SAVE=r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\VANILLA_start.eu4"
raw=zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")
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
i1=raw.index("\nprovinces={"); j1=raw.index("{",i1); pb=raw[j1+1:mb(raw,j1)]
for mm in re.finditer(r"^-(\d+)=\{", pb, re.M):
    pid=int(mm.group(1))
    if pid in (675,2196,213):
        s2=pb.index("{",mm.start()); blk=pb[s2+1:mb(pb,s2)]
        print("========== pid %d ==========" % pid)
        print(blk[:2600])
        print("...")
