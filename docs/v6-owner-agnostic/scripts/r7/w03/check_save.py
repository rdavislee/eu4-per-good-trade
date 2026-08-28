import zipfile, os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import solver

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
body = raw[j + 1:mb(raw, j)]

save_provs = {}
for m in re.finditer(r"\n-(\d+)=\{", body):
    st = body.index("{", m.start())
    end = mb(body, st)
    rec = body[st + 1:end]
    # only look at the TOP-LEVEL fields (before "history={" sub-block) to get the resolved 1444.11.11 state
    hidx = rec.find("\n\t\thistory={")
    top = rec[:hidx] if hidx >= 0 else rec
    owner_m = re.search(r'\bowner="?([A-Za-z0-9\-]+)"?', top)
    bt_m = re.search(r'\bbase_tax=([\d.]+)', top)
    bp_m = re.search(r'\bbase_production=([\d.]+)', top)
    tg_m = re.search(r'\btrade_goods=(\w+)', top)
    save_provs[int(m.group(1))] = dict(
        owner=owner_m.group(1) if owner_m else None,
        base_tax=float(bt_m.group(1)) if bt_m else None,
        base_production=float(bp_m.group(1)) if bp_m else None,
        trade_goods=tg_m.group(1) if tg_m else None,
    )

print("provinces found in save:", len(save_provs))

PROV = solver.PROV
owned_hist = {p: s for p, s in PROV.items() if s.get("owner")}
print("owned in history parse:", len(owned_hist))

mismatches_tax = []
mismatches_prod = []
mismatches_owner = []
mismatches_goods = []
checked = 0
for pid, s in owned_hist.items():
    sv = save_provs.get(pid)
    if sv is None:
        continue
    checked += 1
    if sv["owner"] != s.get("owner"):
        mismatches_owner.append((pid, s.get("owner"), sv["owner"]))
    ht = float(s.get("base_tax") or 0)
    hp = float(s.get("base_production") or 0)
    if sv["base_tax"] is not None and abs(sv["base_tax"] - ht) > 1e-6:
        mismatches_tax.append((pid, ht, sv["base_tax"]))
    if sv["base_production"] is not None and abs(sv["base_production"] - hp) > 1e-6:
        mismatches_prod.append((pid, hp, sv["base_production"]))
    hg = s.get("trade_goods")
    sg = sv["trade_goods"]
    if hg != sg:
        mismatches_goods.append((pid, hg, sg))

print("checked:", checked)
print("owner mismatches:", len(mismatches_owner), mismatches_owner[:10])
print("base_tax mismatches:", len(mismatches_tax), mismatches_tax[:10])
print("base_production mismatches:", len(mismatches_prod), mismatches_prod[:10])
print("trade_goods mismatches:", len(mismatches_goods))
print("  sample:", mismatches_goods[:25])
