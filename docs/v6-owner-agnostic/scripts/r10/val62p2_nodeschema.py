import zipfile, re, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SAVE = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                    "Europa Universalis IV", "save games", "VANILLA_start.eu4")
raw = zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")
def mb(s, i):
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
nodes = {}
order = []
for m in re.finditer(r'\tnode=\{', trade):
    st = trade.index('{', m.start())
    blk = trade[st+1:mb(trade,st)]
    nm = re.search(r'definitions="([^"]+)"', blk).group(1)
    nodes[nm] = blk; order.append(nm)
# print top-level scalar fields + incoming blocks of african_great_lakes and sevilla
for nm in ("african_great_lakes", "sevilla", "tunis"):
    blk = nodes[nm]
    print("=====", nm, "=====")
    # strip country subblocks
    out = []
    k = 0
    depth = 0
    for line in blk.split("\n"):
        if re.match(r'^\t\t[A-Z][A-Z0-9]{2}=\{', line): depth += 1; continue
        if depth:
            depth += line.count("{") - line.count("}")
            if depth <= 0: depth = 0
            continue
        out.append(line)
    txt = "\n".join(out)
    print(txt[:2600])
