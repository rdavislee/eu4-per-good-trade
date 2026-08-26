# Extract per-node country standings from an EU4 text save into standings1444.json for aitest.
#   python extract_standings.py <save.eu4> <out.json>
# The save is a ZIP whose `gamestate` entry is EU4txt. Inside trade={ node={ definitions="X" ...
# each country has a sub-block TAG={ val=.. max_pow=.. has_capital=yes .. }. We keep val and
# has_capital, which is all frontier::plan needs (power = val, home = has_capital).
import sys, zipfile, re, json
save, out = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(save) as z:
    txt = z.read('gamestate').decode('latin-1')
i = txt.index('\ntrade={')
# walk braces to the end of the trade block
depth = 0; j = i
while True:
    c = txt[j]
    if c == '{': depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0: break
    j += 1
trade = txt[i:j+1]
nodes = []
for m in re.finditer(r'\n\tnode=\{', trade):
    s = m.end(); d = 1; k = s
    while d:
        c = trade[k]
        if c == '{': d += 1
        elif c == '}': d -= 1
        k += 1
    body = trade[s:k]
    name = re.search(r'definitions="([^"]+)"', body).group(1)
    countries = {}
    for cm in re.finditer(r'\n\t\t([A-Z0-9]{3})=\{', body):
        cs = cm.end(); d = 1; ck = cs
        while d:
            c = body[ck]
            if c == '{': d += 1
            elif c == '}': d -= 1
            ck += 1
        cb = body[cs:ck]
        v = re.search(r'\bval=([-\d.]+)', cb)
        hc = re.search(r'\bhas_capital=yes', cb)
        countries[cm.group(1)] = {"val": float(v.group(1)) if v else 0.0, "has_capital": bool(hc)}
    nodes.append({"name": name, "countries": countries})
json.dump(nodes, open(out, 'w'), indent=1)
print(f"{len(nodes)} nodes, {sum(len(n['countries']) for n in nodes)} standings, {sum(1 for n in nodes for c in n['countries'].values() if c['has_capital'])} capitals -> {out}")
