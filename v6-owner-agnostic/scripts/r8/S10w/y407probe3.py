import re, zipfile
import numpy as np
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
rows=[]
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
    hp = re.search(r"\n\t\thighest_power=([\d.]+)", b)
    tot = re.search(r"\n\t\ttotal=([\d.]+)", b)
    mx = re.search(r"\n\t\tmax=([\d.]+)", b)
    pp = re.search(r"\n\t\tp_pow=([\d.]+)", b)
    cp = re.search(r"\n\t\tcollector_power=([\d.]+)", b)
    if hp and tot and mx and pp and cp:
        rows.append((nm, float(hp.group(1)), float(tot.group(1)), float(mx.group(1)), float(pp.group(1)), float(cp.group(1))))
print("n=",len(rows))
hp=np.array([r[1] for r in rows]); tot=np.array([r[2] for r in rows])
mx=np.array([r[3] for r in rows]); pp=np.array([r[4] for r in rows]); cp=np.array([r[5] for r in rows])
for lab,arr in (("total",tot),("max",mx),("p_pow",pp),("collector_power",cp)):
    ratio = hp/arr
    print(f"  hp/{lab}: min {ratio.min():.4f} max {ratio.max():.4f} mean {ratio.mean():.4f} std {ratio.std():.4f}")
