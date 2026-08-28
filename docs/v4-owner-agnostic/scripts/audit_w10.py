# -*- coding: utf-8 -*-
"""Audit of w10.py: it swallows parse failures (`except Exception: pass`), so any file the
minimal PDX parser chokes on is silently dropped from the change_price census."""
import os, sys, collections, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
prices = {k: float(v.get("base_price", 0)) for k, v in
          pdx.load(os.path.join(EU4, "common", "prices", "00_prices.txt")) if isinstance(v, pdx.Node)}


def walk(n, h, s, fn):
    for k, v in n:
        if isinstance(v, pdx.Node):
            if k == "change_price":
                tg, val = v.get("trade_goods"), v.get("value")
                if tg is not None and val is not None:
                    h.append((tg, float(val), s, v.get("key"), fn))
            walk(v, h, s, fn)


hits = []
failed = []
raw = collections.Counter()
for r in ("events", "decisions", "missions", "common", "history"):
    for dp, _, fs in os.walk(os.path.join(EU4, r)):
        for fn in fs:
            if not fn.endswith(".txt"):
                continue
            p = os.path.join(dp, fn)
            txt = pdx.strip_comments(open(p, encoding="latin-1", errors="replace").read())
            n_raw = len(re.findall(r"\bchange_price\s*=\s*\{", txt))
            raw[r] += n_raw
            before = len(hits)
            try:
                walk(pdx.load(p), hits, r, p)
            except Exception as e:
                failed.append((p, repr(e)[:80]))
                continue
            got = len(hits) - before
            if got != n_raw:
                print("  MISMATCH %-60s raw=%d parsed=%d" % (os.path.relpath(p, EU4), n_raw, got))

print()
print("raw (non-comment) `change_price = {` occurrences per tree:", dict(raw), "total", sum(raw.values()))
print("blocks w10.py's parser actually recovered           :",
      dict(collections.Counter(h[2] for h in hits)), "total", len(hits))
print("files whose parse raised (silently dropped by w10)  :", len(failed))
for p, e in failed:
    print("   ", os.path.relpath(p, EU4), e)

print()
print("the mission blocks w10.py MISSED:")
seen = set((h[4], h[0], h[1]) for h in hits)
for dp, _, fs in os.walk(os.path.join(EU4, "missions")):
    for fn in fs:
        if not fn.endswith(".txt"):
            continue
        p = os.path.join(dp, fn)
        txt = pdx.strip_comments(open(p, encoding="latin-1", errors="replace").read())
        for m in re.finditer(r"change_price\s*=\s*\{([^}]*)\}", txt):
            body = m.group(1)
            tg = re.search(r"trade_goods\s*=\s*(\S+)", body)
            val = re.search(r"value\s*=\s*(\S+)", body)
            if tg and val and (p, tg.group(1), float(val.group(1))) not in seen:
                print("   %-46s %-14s %s" % (os.path.basename(p), tg.group(1), val.group(1)))

print()
print("does adding them change the partition?  most-negative event per good, ALL trees, regex census:")
neg = collections.defaultdict(list)
allb = 0
for r in ("events", "decisions", "missions", "common", "history"):
    for dp, _, fs in os.walk(os.path.join(EU4, r)):
        for fn in fs:
            if not fn.endswith(".txt"):
                continue
            p = os.path.join(dp, fn)
            txt = pdx.strip_comments(open(p, encoding="latin-1", errors="replace").read())
            for m in re.finditer(r"change_price\s*=\s*\{([^}]*)\}", txt):
                body = m.group(1)
                tg = re.search(r"trade_goods\s*=\s*(\S+)", body)
                val = re.search(r"value\s*=\s*(\S+)", body)
                if tg and val:
                    allb += 1
                    v = float(val.group(1))
                    if v < 0:
                        neg[tg.group(1)].append((v, r, os.path.basename(p)))
print("  total change_price blocks by regex over all five trees:", allb)
below = exact = above = none_ = 0
bl = []
for g in sorted(prices):
    if prices[g] <= 0:
        continue
    if g not in neg:
        none_ += 1
        continue
    w = min(neg[g])
    fl = prices[g] * (1 + w[0])
    if fl < 2.0 - 1e-9:
        below += 1; bl.append((g, round(fl, 4), w[1], w[2]))
    elif abs(fl - 2.0) < 1e-9:
        exact += 1
    else:
        above += 1
print("  BELOW 2.0: %d   EXACTLY 2.0: %d   ABOVE: %d   NO negative: %d" % (below, exact, above, none_))
for x in sorted(bl, key=lambda y: y[1]):
    print("     ", x)
