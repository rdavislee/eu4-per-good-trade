import zipfile, re, os, json

sg = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                   "Europa Universalis IV", "save games", "VANILLA_start.eu4")
z = zipfile.ZipFile(sg)
gs = z.read("gamestate").decode("latin-1")

def match_brace(s, i):
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
    return len(s)-1

ti = gs.index("\ntrade={")
tj = gs.index("{", ti)
tbody = gs[tj+1: match_brace(gs, tj)]

nodes = {}
k = 0
while True:
    m = re.search(r'\bnode=\{', tbody[k:])
    if not m: break
    st = k + m.start()
    bopen = tbody.index("{", st)
    bclose = match_brace(tbody, bopen)
    block = tbody[bopen+1:bclose]
    nm = re.search(r'definitions="([a-z_]+)"', block)
    if nm:
        nodes[nm.group(1)] = block
    k = bclose+1

print("total nodes:", len(nodes))

# for each node block, extract top-level scalar fields and per-country sub-blocks
TOPFIELDS = ["current","local_value","outgoing","value_added_outgoing","retention",
             "num_collectors","num_collectors_including_pirates","total","p_pow","max",
             "collector_power","collector_power_including_pirates","pull_power","retain_power",
             "highest_power"]

node_data = {}
for name, block in nodes.items():
    top = {}
    for f in TOPFIELDS:
        m = re.search(r'\n\t\t'+re.escape(f)+r'=([\-0-9.]+)\n', block)
        if m:
            top[f] = float(m.group(1))
    # country sub blocks: TAG={ ... } where TAG is 2-4 uppercase letters (and not one of the top fields)
    countries = {}
    for cm in re.finditer(r'\n\t\t([A-Z][A-Z0-9]{1,3})=\{', block):
        tag = cm.group(1)
        bopen = block.index("{", cm.start())
        bclose = match_brace(block, bopen)
        cblock = block[bopen+1:bclose]
        cd = {}
        for fld in ["val","prev","max_pow","max_demand","province_power","power_fraction",
                    "money","total","already_sent","has_trader","has_capital","type",
                    "trading_policy"]:
            fm = re.search(r'\n\t\t\t'+re.escape(fld)+r'=([^\n]+)\n', cblock)
            if fm:
                v = fm.group(1).strip()
                cd[fld] = v
        countries[tag] = cd
    node_data[name] = {"top": top, "countries": countries}

json.dump(node_data, open("node_data.json","w"))
print("done, sample sevilla FRA:", node_data["sevilla"]["countries"].get("FRA"))
print("sample sevilla CAS:", node_data["sevilla"]["countries"].get("CAS"))
