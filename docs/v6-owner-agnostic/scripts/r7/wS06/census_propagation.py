import zipfile, re, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SAVE = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                     "Europa Universalis IV", "save games", "VANILLA_start.eu4")
NODES = json.load(open(os.path.join(HERE, "nodes.json")))["nodes"]

def mb(s, i):
    d = 0; k = i; inq = False
    while k < len(s):
        c = s[k]
        if c == '"': inq = not inq
        elif not inq:
            if c == "{": d += 1
            elif c == "}":
                d -= 1
                if d == 0: return k
        k += 1
    return len(s) - 1

raw = zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")
i = raw.index("\ntrade={")
j = raw.index("{", i)
end = mb(raw, j)
body = raw[j + 1:end]

nodeiter = list(re.finditer(r"\n\tnode=\{", body))
print("node blocks found:", len(nodeiter))

# parse every node block -> { def_name: {country: {field: value}} }
NODE_DATA = {}
for m in nodeiter:
    st = body.index("{", m.start())
    e = mb(body, st)
    blk = body[st + 1:e]
    dm = re.search(r'definitions="([a-z_]+)"', blk)
    name = dm.group(1)
    countries = {}
    for cm in re.finditer(r"\n\t\t([A-Z][A-Z0-9]{2})=\{", blk):
        st2 = blk.index("{", cm.start())
        e2 = mb(blk, st2)
        sub = blk[st2 + 1:e2]
        d = {}
        for km in re.finditer(r"\n\t\t\t([a-z_]+)=\"?([^\n\"]*)\"?", sub):
            key, val = km.group(1), km.group(2)
            d[key] = val
        countries[cm.group(1)] = d
    NODE_DATA[name] = countries

print("nodes parsed:", len(NODE_DATA))

# upstream map: X is immediately upstream of N iff N in NODES[X]["outgoing"]
UPSTREAM = {n: [] for n in NODES}
for x, info in NODES.items():
    for n in info["outgoing"]:
        UPSTREAM.setdefault(n, []).append(x)

THRESHOLD_DIVIDER = 5
THRESHOLD_RAW = 2
RAW_THRESHOLD = THRESHOLD_RAW * THRESHOLD_DIVIDER  # 10, per doc's stated (pending) formula

def province_power(node, country):
    d = NODE_DATA.get(node, {}).get(country)
    if not d:
        return 0.0
    pp = d.get("province_power")
    return float(pp) if pp is not None else 0.0

def has_val(node, country):
    d = NODE_DATA.get(node, {}).get(country)
    if not d:
        return False
    v = d.get("val")
    if v is None:
        return False
    try:
        return float(v) > 0.0
    except ValueError:
        return False

def val_of(node, country):
    d = NODE_DATA.get(node, {}).get(country)
    if not d:
        return None
    return d.get("val")

# --- census over threshold = TRADE_PROPAGATE_THRESHOLD * TRADE_PROPAGATE_DIVIDER = 10 ---
qualifying_pairs = []  # (country, downstream_node, upstream_node)
for n, countries in NODE_DATA.items():
    for c, d in countries.items():
        pp = d.get("province_power")
        if pp is None:
            continue
        pp = float(pp)
        if pp >= RAW_THRESHOLD:
            for x in UPSTREAM.get(n, []):
                qualifying_pairs.append((c, n, x))

total_pairs = len(qualifying_pairs)
nothing = [(c, n, x) for (c, n, x) in qualifying_pairs if not has_val(x, c)]
print()
print("RAW_THRESHOLD =", RAW_THRESHOLD)
print("total (country, downstream-node)->(upstream-node) pairs:", total_pairs)
print("pairs receiving NOTHING (no val>0 in upstream node):", len(nothing))
print()

# distinct qualifying (country,node) count for reference
qn = set((c, n) for (c, n, x) in qualifying_pairs)
print("distinct (country, node-with-qualifying-power) count:", len(qn))

print()
print("sample of 'nothing' pairs (up to 20):")
for c, n, x in nothing[:20]:
    print(" ", c, "qualifies in", n, "(pp=%.3f)" % province_power(n, c), "-> nothing in upstream", x)

print()
print("Specifically: does ENG qualify in english_channel? province_power =",
      province_power("english_channel", "ENG"))
print("ENG val in chesapeake_bay:", val_of("chesapeake_bay", "ENG"))
print("Is chesapeake_bay upstream of english_channel?", "chesapeake_bay" in UPSTREAM.get("english_channel", []))

print()
print("FRA in sevilla: province_power=%s val=%s has_trader=%s" % (
    NODE_DATA["sevilla"].get("FRA", {}).get("province_power"),
    NODE_DATA["sevilla"].get("FRA", {}).get("val"),
    NODE_DATA["sevilla"].get("FRA", {}).get("has_trader")))
