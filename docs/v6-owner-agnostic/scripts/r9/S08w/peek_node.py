import zipfile, re, os
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
# find a node with multiple outgoing steering entries: look at 'sevilla'
blk = nodes["sevilla"]
print(blk[:4000])
