import os, sys, json, re, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import PROV, PNODE  # history-parse result (base_tax/base_production/owner/trade_goods)

save = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                    "Europa Universalis IV", "save games", "VANILLA_start.eu4")
raw = zipfile.ZipFile(save).read("gamestate").decode("latin-1")

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

i = raw.index(chr(10) + "provinces={"); j = raw.index("{", i)
body = raw[j+1:mb(raw, j)]
save_prov = {}
for m in re.finditer(r"^-(\d+)=\{", body, re.M):
    st = body.index("{", m.start())
    rec = body[st+1:mb(body, st)]
    pid = int(m.group(1))
    def field(name):
        mm = re.search(r"^\t\t" + name + r"=\"?([^\n\"]+)\"?", rec, re.M)
        return mm.group(1) if mm else None
    save_prov[pid] = dict(
        owner=field("owner"),
        base_tax=field("base_tax"),
        base_production=field("base_production"),
        trade_goods=field("trade_goods"),
    )

owned_in_node = [pid for pid in PROV if PROV[pid].get("owner") and pid in PNODE]
print("owned+in-node (counted) provinces:", len(owned_in_node))

mismatches_tax = []
mismatches_prod = []
mismatches_owner = []
mismatches_goods = []
missing_in_save = []
for pid in owned_in_node:
    sp = save_prov.get(pid)
    if sp is None:
        missing_in_save.append(pid); continue
    h = PROV[pid]
    try:
        if abs(float(sp["base_tax"]) - float(h["base_tax"])) > 1e-6:
            mismatches_tax.append((pid, sp["base_tax"], h["base_tax"]))
    except Exception as e:
        mismatches_tax.append((pid, sp["base_tax"], h["base_tax"], "ERR"))
    try:
        if abs(float(sp["base_production"]) - float(h["base_production"])) > 1e-6:
            mismatches_prod.append((pid, sp["base_production"], h["base_production"]))
    except Exception as e:
        mismatches_prod.append((pid, sp["base_production"], h["base_production"], "ERR"))
    if sp["owner"] != h["owner"]:
        mismatches_owner.append((pid, sp["owner"], h["owner"]))
    hg = h.get("trade_goods")
    sg = sp["trade_goods"]
    if hg in (None, "unknown"):
        hg_cmp = None
    else:
        hg_cmp = hg
    if sg != hg_cmp:
        mismatches_goods.append((pid, sg, hg))

print("missing in save:", len(missing_in_save), missing_in_save[:10])
print("base_tax mismatches:", len(mismatches_tax), mismatches_tax[:10])
print("base_production mismatches:", len(mismatches_prod), mismatches_prod[:10])
print("owner mismatches:", len(mismatches_owner), mismatches_owner[:10])
print("trade_goods mismatches:", len(mismatches_goods))
print(sorted(pid for pid,_,_ in mismatches_goods))
