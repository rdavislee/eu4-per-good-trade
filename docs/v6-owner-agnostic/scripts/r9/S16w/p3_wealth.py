# -*- coding: utf-8 -*-
"""Independent re-derivation of Y131 (world wealth 10,607.40 over 2,472 provinces)
straight from the save + the install, bypassing prov1444.json entirely."""
import zipfile, re, os, sys
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
import pdx
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
SG = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games"
PRICES = {k: float(v.get("base_price", 1.0))
          for k, v in pdx.load(os.path.join(EU4, "common", "prices", "00_prices.txt"))
          if isinstance(v, pdx.Node)}
tree = pdx.load(os.path.join(EU4, "common", "tradenodes", "00_tradenodes.txt"))
PNODE = {}
for k, v in tree:
    if not isinstance(v, pdx.Node): continue
    for p in pdx.values(v.get("members")): PNODE[int(p)] = k
raw = zipfile.ZipFile(os.path.join(SG, "VANILLA_start.eu4")).read("gamestate").decode("latin-1")
def mb(s, i):
    d = 0; k = i; q = False
    while k < len(s):
        c = s[k]
        if c == '"': q = not q
        elif not q:
            if c == "{": d += 1
            elif c == "}":
                d -= 1
                if d == 0: return k
        k += 1
    return len(s) - 1
i = raw.index("\nprovinces={"); j = raw.index("{", i); body = raw[j + 1:mb(raw, j)]
GP = 0.2; TAX = 1.0
tot = 0.0; n = 0; skipped_no_node = 0; excl = 0
for m in re.finditer(r"^-(\d+)=\{", body, re.M):
    pid = int(m.group(1)); st = body.index("{", m.start()); rec = body[st + 1:mb(body, st)]
    if not re.search(r"^\t\towner=", rec, re.M): continue
    if pid not in PNODE: skipped_no_node += 1; continue
    def f(key, dflt=0.0):
        mm = re.search(r"^\t\t" + key + r"=(-?[\d.]+)", rec, re.M)
        return float(mm.group(1)) if mm else dflt
    g = re.search(r'^\t\ttrade_goods="?([a-z_]+)', rec, re.M)
    good = g.group(1) if g else None
    price = PRICES.get(good, 0.0)
    if good in ("gold", None): price = 0.0; excl += 1
    dev = f("devastation") / 100.0
    gp = max(0.0, GP * f("base_production") * (1.0 - 2.0 * dev))
    tot += TAX * f("base_tax") + gp * price
    n += 1
print("counted provinces (owner + in a trade node) : %d" % n)
print("owned provinces with no trade node          : %d" % skipped_no_node)
print("gold/unknown-good provinces priced at 0     : %d" % excl)
print("world wealth (annual ducats)                : %.2f" % tot)
