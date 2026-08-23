import zipfile, re, json, os, collections
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
    name = re.search(r'definitions="([^"]+)"', blk).group(1)
    nodes[name] = blk

ND = json.load(open(os.path.join(HERE, "nodes.json")))
OUT = {n: ND["nodes"][n]["outgoing"] for n in ND["order"]}

# parse per-country entries per node
info = {}   # node -> tag -> dict
for name, blk in nodes.items():
    ents = {}
    for m in re.finditer(r'^\t\t([A-Z][A-Z0-9]{2})=\{', blk, re.M):
        st = blk.index('{', m.start())
        body = blk[st+1:mb(blk,st)]
        d = {}
        for k in ("val","max_pow","province_power","ship_power","already_sent"):
            g = re.search(r'^\t*%s=([\d.\-]+)' % k, body, re.M)
            if g: d[k] = float(g.group(1))
        d["trader"] = "has_trader=yes" in body
        d["capital"] = "has_capital=yes" in body
        d["light_ship"] = "light_ship=" in body
        ents[m.group(1)] = d
    info[name] = ents

DIV, THR = 5.0, 2.0
RAWTHR = THR*DIV
# prediction: for country c in node n with no province_power, no trader:
# received = sum over m in OUT[n] of province_power(c,m)/DIV if province_power(c,m)>=RAWTHR
ok = bad = 0
badrows = []
phantom = 0  # entries predicted but absent
for n in ND["order"]:
    for m2 in OUT[n]:
        pass
for n in ND["order"]:
    ents = info.get(n, {})
    # all countries with any province power anywhere downstream
    for c, d in ents.items():
        if d.get("province_power") or d["trader"] or d["light_ship"]:
            continue
        # pure-propagation entry
        pred = 0.0
        for m2 in OUT.get(n, []):
            pp = info.get(m2, {}).get(c, {}).get("province_power", 0.0)
            if pp >= RAWTHR:
                pred += pp/DIV
        got = d.get("max_pow", 0.0)
        if pred == 0:
            # entry exists but nothing predicted: chained propagation? note it
            badrows.append((n, c, "no source", got))
            continue
        if abs(pred-got) < 0.02*max(1.0, got):
            ok += 1
        else:
            bad += 1
            badrows.append((n, c, round(pred,3), got))
print("pure-propagation entries matching pred=sum(downstream pp/5, pp>=10):", ok)
print("mismatches:", bad)
for r in badrows[:25]: print("  ", r)

# one-hop test: countries with power TWO hops downstream but none one hop should NOT appear
twohop_only = 0; appear = 0
for n in ND["order"]:
    ents = info.get(n, {})
    for m1 in OUT.get(n, []):
        for m2 in OUT.get(m1, []):
            for c, d2 in info.get(m2, {}).items():
                pp2 = d2.get("province_power", 0.0)
                if pp2 < RAWTHR: continue
                pp1 = info.get(m1, {}).get(c, {}).get("province_power", 0.0)
                if pp1 >= RAWTHR: continue
                if c in ents and (ents[c].get("province_power") or ents[c]["trader"] or ents[c]["light_ship"]):
                    continue
                twohop_only += 1
                if c in ents and ents[c].get("max_pow",0) > 0:
                    # could be via another downstream branch; check all OUT[n]
                    direct = any(info.get(mm, {}).get(c, {}).get("province_power",0.0) >= RAWTHR for mm in OUT.get(n,[]))
                    if not direct:
                        appear += 1
print("two-hop-only (country,node) cases:", twohop_only, "| appearing anyway (chaining):", appear)

# threshold test: countries with 0 < pp < 10 downstream, no other source: do they appear upstream?
below = 0; leaked = []
for n in ND["order"]:
    for m1 in OUT.get(n, []):
        for c, d1 in info.get(m1, {}).items():
            pp = d1.get("province_power", 0.0)
            if 0 < pp < RAWTHR:
                others = any(info.get(mm, {}).get(c, {}).get("province_power",0.0) >= RAWTHR for mm in OUT.get(n,[]))
                if others: continue
                e = info.get(n, {}).get(c)
                below += 1
                if e and not (e.get("province_power") or e["trader"] or e["light_ship"]) and e.get("max_pow",0.0) > 0.05:
                    leaked.append((n, c, pp, e.get("max_pow")))
print("below-threshold downstream cases:", below, "| receiving anyway:", len(leaked), leaked[:10])
