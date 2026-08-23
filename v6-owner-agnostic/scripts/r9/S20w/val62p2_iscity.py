import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
PROV = {int(k): v for k, v in json.load(open(os.path.join(HERE, "prov1444.json"))).items()}
ND = json.load(open(os.path.join(HERE, "nodes.json")))
PNODE = {p: n for n in ND["order"] for p in ND["nodes"][n]["members"]}
counted = [p for p, s in PROV.items() if s.get("owner") and p in PNODE]
print("counted:", len(counted))
# scan history files directly for is_city presence (commented or absent) among counted provinces
hist_dir = os.path.join(EU4, "history", "provinces")
files = os.listdir(hist_dir)
fmap = {}
for fn in files:
    m = re.match(r"^(\d+)\s*-", fn) or re.match(r"^(\d+)-", fn)
    if m: fmap[int(m.group(1))] = fn
no_iscity = []
for p in counted:
    fn = fmap.get(p)
    if not fn: continue
    txt = open(os.path.join(hist_dir, fn), encoding="latin-1", errors="replace").read()
    # look for an active (non-commented) is_city = yes line before any date block (top of file)
    top = txt.split("\n")
    active = False
    for line in top:
        s = line.strip()
        if re.match(r"^\d+\.\d+\.\d+\s*=\s*\{", s):
            break
        if re.match(r"^is_city\s*=\s*yes", s):
            active = True
            break
    if not active:
        no_iscity.append((p, fn))
print("counted provinces without active is_city=yes:", len(no_iscity))
print(no_iscity[:25])
print("265 among them:", any(p==265 for p,_ in no_iscity))
