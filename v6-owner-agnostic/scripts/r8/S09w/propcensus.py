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

# Build "upstream" adjacency: for node n, its downstream neighbours are OUT[n].
# A country c qualifies at downstream node m (>= RAWTHR raw province_power) and
# should propagate a share into each n such that m in OUT[n].
UP = collections.defaultdict(list)  # m -> list of n upstream of m (n has m in OUT[n])
for n in ND["order"]:
    for m in OUT.get(n, []):
        UP[m].append(n)

pairs = []  # (country, upstream_node, downstream_node, raw_power)
for m in ND["order"]:
    for c, d in info.get(m, {}).items():
        pp = d.get("province_power", 0.0)
        if pp >= RAWTHR:
            for n in UP.get(m, []):
                pairs.append((c, n, m, pp))

print("total threshold-qualifying (country, upstream_node[,downstream_source]) instances:", len(pairs))

# collapse to (country, upstream_node) pairs (a country may qualify via multiple downstream nodes into the same upstream node)
by_pair = collections.defaultdict(list)
for c, n, m, pp in pairs:
    by_pair[(c, n)].append((m, pp))

print("total distinct (country, upstream-node) threshold-qualifying pairs:", len(by_pair))

receiving = 0
missing = 0
missing_list = []
for (c, n), srcs in by_pair.items():
    e = info.get(n, {}).get(c)
    got = e.get("max_pow", 0.0) if e else 0.0
    if got > 0:
        receiving += 1
    else:
        missing += 1
        missing_list.append((c, n, srcs))

print("receiving something:", receiving, " | receiving nothing:", missing)

# England / english_channel -> chesapeake_bay specific check
eng_ec_pp = info.get("english_channel", {}).get("ENG", {}).get("province_power", 0.0)
print("ENG province_power in english_channel:", eng_ec_pp, " qualifies:", eng_ec_pp >= RAWTHR)
eng_in_cb = info.get("chesapeake_bay", {}).get("ENG")
print("ENG entry in chesapeake_bay:", eng_in_cb)

print()
print("sample of missing pairs (first 20):")
for row in missing_list[:20]:
    print("  ", row)
