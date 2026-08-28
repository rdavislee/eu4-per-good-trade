import re, zipfile
SAVE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\VANILLA_start.eu4"
z = zipfile.ZipFile(SAVE); txt = z.read("gamestate").decode("latin-1"); z.close()
i = txt.find("\ntrade={"); j = i + len("\ntrade="); d = 0; k = j
while k < len(txt):
    if txt[k] == "{": d += 1
    elif txt[k] == "}":
        d -= 1
        if d == 0: break
    k += 1
tr = txt[j:k+1]
for m in re.finditer(r"\n\tnode=\{", tr):
    s = m.end()-1; dd=0; e=s
    while e < len(tr):
        if tr[e]=="{": dd+=1
        elif tr[e]=="}":
            dd-=1
            if dd==0: break
        e+=1
    b = tr[s:e+1]
    nm = re.search(r'definitions="([^"]+)"', b).group(1)
    if nm != "venice": continue
    m2 = re.search(r'\n\t\tVEN=\{([^{}]*)\}', b)
    print("VEN block:", m2.group(0) if m2 else None)
    # find max val among country subblocks
    best=None
    for mm in re.finditer(r'\n\t\t([A-Z0-9]{3})=\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', b):
        tag, body = mm.group(1), mm.group(2)
        vm = re.search(r'val=([\d.]+)', body)
        if vm:
            v=float(vm.group(1))
            if best is None or v>best[1]: best=(tag,v)
    print("largest val country:", best)
