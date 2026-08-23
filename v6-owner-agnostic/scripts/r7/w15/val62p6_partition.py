# -*- coding: utf-8 -*-
"""Independent sublinear-reachability partition, computed from raw text (quote-aware)."""
import os, re, collections
ROOT = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
strip = lambda s: "\n".join(x.split("#")[0] for x in s.split("\n"))

prices = {}
pt = strip(open(os.path.join(ROOT, "common", "prices", "00_prices.txt"), encoding="cp1252").read())
for m in re.finditer(r"([a-z_]+)\s*=\s*\{([^}]*)\}", pt):
    bp = re.search(r"base_price\s*=\s*([0-9.]+)", m.group(2))
    if bp: prices[m.group(1)] = float(bp.group(1))
tradeable = {g: p for g, p in prices.items() if p > 0 and g != "unknown"}
print("goods with base_price>0 excluding 'unknown': %d ; min = %.2f at %s"
      % (len(tradeable), min(tradeable.values()),
         sorted(g for g, p in tradeable.items() if p == min(tradeable.values()))))
print("goldtype good present:", "gold" in prices, "-> base_price", prices.get("gold"))

# collect change_price blocks, textual, from raw text (catches quoted ones too)
hits = []   # (tree, path, good, value, key)
for tree in ("events", "missions", "decisions", "common", "history"):
    for dp, _, fs in os.walk(os.path.join(ROOT, tree)):
        for fn in fs:
            if not fn.endswith(".txt"): continue
            p = os.path.join(dp, fn)
            body = strip(open(p, encoding="cp1252", errors="replace").read())
            for m in re.finditer(r"change_price\s*=\s*\{(.*?)\}", body, re.S):
                b = m.group(1)
                g = re.search(r"trade_goods\s*=\s*([A-Za-z_]+)", b)
                v = re.search(r"value\s*=\s*(-?[0-9.]+)", b)
                k = re.search(r"key\s*=\s*([A-Za-z_0-9]+)", b)
                if g and v:
                    hits.append((tree, p, g.group(1), float(v.group(1)), k.group(1) if k else None))
print("change_price blocks with trade_goods+value parsed:", len(hits))
print("by tree:", dict(collections.Counter(h[0] for h in hits)))

def partition(pool, label):
    neg = collections.defaultdict(list)
    for t, p, g, v, k in pool:
        if v < 0: neg[g].append(v)
    below = exact = above = none_ = 0
    bl, ex, ab, no = [], [], [], []
    for g, base in sorted(tradeable.items()):
        if g not in neg:
            none_ += 1; no.append(g); continue
        fl = base * (1 + min(neg[g]))
        if fl < 2.0 - 1e-9: below += 1; bl.append("%s@%.4g" % (g, fl))
        elif abs(fl - 2.0) < 1e-9: exact += 1; ex.append(g)
        else: above += 1; ab.append("%s@%.4g" % (g, fl))
    print("\n%s -> below/exact/above/none = %d/%d/%d/%d" % (label, below, exact, above, none_))
    print("   below :", bl)
    print("   exact :", ex)
    print("   above :", ab)
    print("   none  :", no)

partition(hits, "ALL FIVE TREES")
partition([h for h in hits if h[0] == "events"], "events/ ONLY")

print("\n=== wool negative keys ===")
for t, p, g, v, k in hits:
    if g == "wool" and v < 0:
        print("   %-9s %-55s key=%-22s value=%s -> 2.5*(1+v)=%.4f"
              % (t, os.path.relpath(p, ROOT), str(k), v, 2.5*(1+v)))
print("   sum of -0.25 and -0.10 : 2.5*(1-0.35) = %.4f" % (2.5*0.65))
print("   compounded             : 2.5*0.75*0.90 = %.5f" % (2.5*0.75*0.90))
