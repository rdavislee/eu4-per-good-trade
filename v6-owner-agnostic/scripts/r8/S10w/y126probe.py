import re, zipfile, json
import numpy as np
SAVE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\VANILLA_start.eu4"
nd=json.load(open('nodes.json'))
inland=set(n for n in nd['order'] if nd['nodes'][n].get('inland'))
derived_drop = {'siberia'}
z = zipfile.ZipFile(SAVE); txt = z.read("gamestate").decode("latin-1"); z.close()
i = txt.find("\ntrade={"); j = i + len("\ntrade="); d = 0; k = j
while k < len(txt):
    if txt[k] == "{": d += 1
    elif txt[k] == "}":
        d -= 1
        if d == 0: break
    k += 1
tr = txt[j:k+1]
rows={}
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
    if nm not in inland: continue
    tot = re.search(r"\n\t\ttotal=([\d.]+)", b)
    total = float(tot.group(1)) if tot else None
    best=None
    for mm in re.finditer(r'\n\t\t([A-Z0-9]{3})=\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', b):
        tag, body = mm.group(1), mm.group(2)
        vm = re.search(r'val=([\d.]+)', body)
        if vm:
            v=float(vm.group(1))
            if best is None or v>best[1]: best=(tag,v)
    rows[nm]=(total,best)

print("nodes found:", len(rows), "expected 26")
missing = inland - set(rows)
print("missing:", missing)

CAP=50.0
data=[]
for nm,(total,best) in rows.items():
    if total is None: continue
    pct_before = 100*CAP/total
    pct_after = 100*CAP/(total+CAP)
    data.append((nm, total, pct_before, pct_after, best))

data.sort(key=lambda x: x[1])
for nm,total,pb,pa,best in data:
    print(f"  {nm:22s} total={total:8.1f} before={pb:6.2f}% after={pa:6.2f}%  incumbent={best}")

arr_before = np.array([d[2] for d in data])
arr_after = np.array([d[3] for d in data])
totals = np.array([d[1] for d in data])
print()
print(f"n={len(data)} (26 flag basis)")
print(f"before%: min {arr_before.min():.2f} max {arr_before.max():.2f} median {np.median(arr_before):.2f}")
print(f"after%: min {arr_after.min():.2f} max {arr_after.max():.2f} median {np.median(arr_after):.2f}")
print(f"totals: min {totals.min():.2f} ({data[np.argmin(totals)][0]}) max {totals.max():.2f} ({data[np.argmax(totals)][0]})")

incumbents = np.array([d[4][1] for d in data])
print(f"incumbent val: min {incumbents.min():.2f} max {incumbents.max():.2f}")
outweigh = sum(1 for d in data if CAP > d[4][1])
print(f"cap(50) outweighs incumbent in {outweigh}/{len(data)}, outweighed in {len(data)-outweigh}")

print()
print("=== 25-node derived basis (drop siberia) ===")
data25 = [d for d in data if d[0] not in derived_drop]
arr_before25 = np.array([d[2] for d in data25])
arr_after25 = np.array([d[3] for d in data25])
print(f"n={len(data25)}")
print(f"before% median {np.median(arr_before25):.2f}")
print(f"after% median {np.median(arr_after25):.2f}")
