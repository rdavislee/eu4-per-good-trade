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
for m in re.finditer(r'\tnode=\{', trade):
    st = trade.index('{', m.start())
    blk = trade[st+1:mb(trade,st)]
    nodes[re.search(r'definitions="([^"]+)"', blk).group(1)] = blk
ND = json.load(open(os.path.join(HERE, "nodes.json")))
OUT = {n: ND["nodes"][n]["outgoing"] for n in ND["order"]}
info = {}
for name, blk in nodes.items():
    ents = {}
    for m in re.finditer(r'^\t\t([A-Z][A-Z0-9]{2})=\{', blk, re.M):
        st = blk.index('{', m.start())
        body = blk[st+1:mb(blk,st)]
        d = {}
        for k in ("val","max_pow","province_power"):
            g = re.search(r'^\t*%s=([\d.\-]+)' % k, body, re.M)
            if g: d[k] = float(g.group(1))
        d["trader"] = "has_trader=yes" in body
        d["light_ship"] = "light_ship=" in body
        ents[m.group(1)] = d
    info[name] = ents
DIV = 5.0
real_mm = []; multi = 0; matched = 0
for n in ND["order"]:
    for c, d in info.get(n, {}).items():
        if d.get("province_power") or d["trader"] or d["light_ship"]:
            continue
        got = d.get("max_pow", 0.0)
        srcs = [(m2, info.get(m2, {}).get(c, {}).get("province_power", 0.0)) for m2 in OUT.get(n, [])]
        pred_all = sum(pp/DIV for _, pp in srcs if pp >= 10.0)
        if got == 0.0 and pred_all == 0.0: continue
        if pred_all > 0 and abs(pred_all-got) < 0.02*max(1.0,got):
            matched += 1
            if sum(1 for _, pp in srcs if pp >= 10.0) >= 2: multi += 1
        else:
            real_mm.append((n, c, round(pred_all,3), got, srcs))
print("matched:", matched, "with 2+ contributing downstream neighbours:", multi)
print("REAL mismatches:", len(real_mm))
for r in real_mm[:15]: print("  ", r)
# threshold bracket: largest downstream pp that did NOT produce an upstream entry,
# smallest that DID (among single-source situations)
no_recv_max = 0.0; recv_min = 1e9
for n in ND["order"]:
    for m1 in OUT.get(n, []):
        for c, d1 in info.get(m1, {}).items():
            pp = d1.get("province_power", 0.0)
            if pp <= 0: continue
            others = [info.get(mm, {}).get(c, {}).get("province_power",0.0) for mm in OUT.get(n,[]) if mm != m1]
            if any(o > 0 for o in others): continue
            e = info.get(n, {}).get(c, {})
            if e.get("province_power") or e.get("trader") or e.get("light_ship"): continue
            got = e.get("max_pow", 0.0)
            if got > 0.01:
                recv_min = min(recv_min, pp)
            else:
                no_recv_max = max(no_recv_max, pp)
print("largest downstream pp producing NO upstream entry:", round(no_recv_max,3))
print("smallest downstream pp producing an upstream entry:", round(recv_min,3))
