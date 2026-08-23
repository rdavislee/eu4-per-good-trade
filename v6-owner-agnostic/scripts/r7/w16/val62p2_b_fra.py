import zipfile, re, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SAVE = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                    "Europa Universalis IV", "save games", "VANILLA_start.eu4")
raw = zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")
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
i = raw.index('\ntrade={'); j = raw.index('{', i)
trade = raw[j+1:mb(raw,j)]
nodes={}
for m in re.finditer(r'\tnode=\{', trade):
    st=trade.index('{',m.start()); blk=trade[st+1:mb(trade,st)]
    nodes[re.search(r'definitions="([^"]+)"',blk).group(1)]=blk
def ent(node, tag):
    blk=nodes[node]
    m=re.search(r'^\t\t%s=\{'%tag, blk, re.M)
    if not m: return None
    st=blk.index('{',m.start()); return blk[st+1:mb(blk,st)]
print("### FRA in sevilla ###")
e=ent("sevilla","FRA"); print(e[:1400] if e else "NO ENTRY")
print("### nodes.json: sevilla outgoing/incoming ###")
ND=json.load(open(os.path.join(HERE,"nodes.json")))
print("sevilla out:",ND["nodes"]["sevilla"]["outgoing"], "in:", ND["nodes"]["sevilla"].get("incoming"))
for m2 in ND["nodes"]["sevilla"]["outgoing"]:
    e2=ent(m2,"FRA")
    pp=re.search(r'^\t*province_power=([\d.]+)',e2,re.M) if e2 else None
    print("  downstream",m2,"FRA province_power=",pp.group(1) if pp else None)
print("### ZAN in african_great_lakes ###")
e=ent("african_great_lakes","ZAN"); print(repr(e[:600]) if e else "NO ENTRY")
print("### ZAN in zanzibar ###")
e=ent("zanzibar","ZAN"); print(e[:800] if e else "NO ENTRY")
