import zipfile, re, os

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

# find each node= block at top level of tbody
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

print("total nodes found:", len(nodes))
print("sevilla" in nodes)
with open("sevilla_block.txt", "w", encoding="utf-8") as f:
    f.write(nodes.get("sevilla", "NOT FOUND"))
with open("all_node_names.txt","w") as f:
    f.write("\n".join(sorted(nodes.keys())))
