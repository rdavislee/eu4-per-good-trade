import zipfile, re, json, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
SAVE = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                    "Europa Universalis IV", "save games", "VANILLA_start.eu4")

def mb(s, i):
    d = 0; k = i; inq = False
    while k < len(s):
        c = s[k]
        if c == '"':
            inq = not inq
        elif not inq:
            if c == '{':
                d += 1
            elif c == '}':
                d -= 1
                if d == 0:
                    return k
        k += 1
    return len(s) - 1

raw = zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")
i = raw.index('\ntrade={'); j = raw.index('{', i)
trade = raw[j+1:mb(raw, j)]
nodes = {}
for m in re.finditer(r'\tnode=\{', trade):
    st = trade.index('{', m.start())
    blk = trade[st+1:mb(trade, st)]
    name = re.search(r'definitions="([^"]+)"', blk).group(1)
    nodes[name] = blk

ND = json.load(open(os.path.join(HERE, "nodes.json")))
OUT = {n: ND["nodes"][n]["outgoing"] for n in ND["order"]}

info = {}
for name, blk in nodes.items():
    ents = {}
    for m in re.finditer(r'^\t\t([A-Z][A-Z0-9]{2})=\{', blk, re.M):
        st = blk.index('{', m.start())
        body = blk[st+1:mb(blk, st)]
        d = {}
        for k in ("val", "max_pow", "province_power", "ship_power", "already_sent"):
            g = re.search(r'^\t*%s=([\d.\-]+)' % k, body, re.M)
            if g: d[k] = float(g.group(1))
        d["trader"] = "has_trader=yes" in body
        d["light_ship"] = "light_ship=" in body
        ents[m.group(1)] = d
    info[name] = ents

DIV, THR = 5.0, 2.0
RAWTHR = THR * DIV  # 10.0

UP = collections.defaultdict(list)
for n in ND["order"]:
    for m in OUT.get(n, []):
        UP[m].append(n)

# Only count (country, upstream_node) as "qualifying" if that country's entry in the
# upstream node itself (if any) is a PURE propagation-only entry -- i.e. no province_power,
# no trader, no light_ship there (so max_pow there, if nonzero, could only be propagation).
qualifying = set()
qual_srcs = collections.defaultdict(list)
for m in ND["order"]:
    for c, d in info.get(m, {}).items():
        pp = d.get("province_power", 0.0)
        if pp >= RAWTHR:
            for n in UP.get(m, []):
                e = info.get(n, {}).get(c)
                if e is not None and (e.get("province_power", 0.0) > 0 or e["trader"] or e["light_ship"]):
                    continue  # not a pure-propagation candidate; power there has another source
                qualifying.add((c, n))
                qual_srcs[(c, n)].append((m, pp))

print("pure-propagation-candidate (country, upstream-node) qualifying pairs:", len(qualifying))
receiving = 0
missing = 0
missing_list = []
for (c, n) in qualifying:
    e = info.get(n, {}).get(c)
    got = e.get("max_pow", 0.0) if e else 0.0
    if got > 0:
        receiving += 1
    else:
        missing += 1
        missing_list.append((c, n, qual_srcs[(c, n)]))
print("receiving:", receiving, "| missing:", missing)
print()
print("England/english_channel -> chesapeake_bay:")
print("  qualifies:", ("ENG","chesapeake_bay") in qualifying)
e = info.get("chesapeake_bay", {}).get("ENG")
print("  ENG entry in chesapeake_bay:", e)
