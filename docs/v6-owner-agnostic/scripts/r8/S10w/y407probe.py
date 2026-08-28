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
    print(b[:3000])
