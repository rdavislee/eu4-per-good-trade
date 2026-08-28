# -*- coding: utf-8 -*-
"""Try to break the 16-province fold-in: hunt a seventh source, and test whether the
alpha_Phi band table is a property of the model or of the 1444 snapshot."""
import os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pdx, solver
from solver import N, ORDER, NIDX, PRICES
from drain import run_drain

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
START = (1444, 11, 11)
D = re.compile(r"^(\d{1,4})\.(\d{1,2})\.(\d{1,2})$")
WK = ("trade_goods_size", "trade_goods_size_modifier", "local_tax_modifier", "trade_value_modifier")

print("=" * 96)
print("1. MONUMENTS: tiers 0..starting_tier, comment-only triggers, area_modifier")
print("=" * 96)
mon = pdx.load(os.path.join(EU4, "common", "great_projects", "01_monuments.txt"))
raw = open(os.path.join(EU4, "common", "great_projects", "01_monuments.txt"),
           encoding="latin-1", errors="replace").read()
ungated = []
for k, v in mon:
    if not isinstance(v, pdx.Node):
        continue
    st, dt = v.get("starting_tier"), v.get("date")
    if st is None or dt is None:
        continue
    m = D.match(dt)
    if not m or (int(m.group(1)), int(m.group(2)), int(m.group(3))) > START:
        continue
    tier = int(st)
    trig = v.get("can_use_modifiers_trigger")
    gated = trig is not None and len(trig) > 0
    prov, area, above = {}, {}, {}
    for t in range(0, tier + 1):
        tb = v.get("tier_%d" % t)
        if tb is None:
            continue
        pm = tb.get("province_modifiers")
        if pm:
            for a, b in pm:
                if a in WK:
                    prov[a] = prov.get(a, 0.0) + float(b)
        am = tb.get("area_modifier")
        if am:
            for a, b in am:
                if a in WK:
                    area[a] = area.get(a, 0.0) + float(b)
    for t in range(tier + 1, 5):
        tb = v.get("tier_%d" % t)
        if tb is None:
            continue
        pm = tb.get("province_modifiers")
        if pm:
            for a, b in pm:
                if a in WK:
                    above[a] = above.get(a, 0.0) + float(b)
    if prov or area:
        print("  %-26s pid=%-6s tier=%d gated=%-5s prov=%s area=%s (above tier: %s)"
              % (k, v.get("start"), tier, gated, prov or "-", area or "-", above or "-"))
        if not gated and prov:
            ungated.append((k, int(v.get("start")), prov))
    elif above and not gated:
        print("  %-26s pid=%-6s tier=%d gated=False  wealth keys only ABOVE starting_tier: %s -> correctly excluded"
              % (k, v.get("start"), tier, above))
print()
print("  ungated + carries a province-level wealth key:", [(k, p) for k, p, _ in ungated])

# comment-only triggers: does the parser see an empty block where the raw text has only comments?
print()
print("  monuments whose can_use_modifiers_trigger body is comments only (parser sees empty):")
n_comment_only = 0
for m in re.finditer(r"^(\w+) = \{", raw, re.M):
    key = m.group(1)
    seg = raw[m.end(): m.end() + 9000]
    tm = re.search(r"can_use_modifiers_trigger = \{(.*?)\n\t\}", seg, re.S)
    if tm and tm.group(1).strip() and all(
            (not ln.strip()) or ln.strip().startswith("#") for ln in tm.group(1).split("\n")):
        n_comment_only += 1
        print("    %-26s body=%r" % (key, tm.group(1).strip()[:50]))
print("    count:", n_comment_only, "(pdx.strip_comments removes these, so they parse as ungated - correct)")

print()
print("=" * 96)
print("2. SEVENTH-SOURCE HUNT")
print("=" * 96)
# centers of trade
cot = os.path.join(EU4, "common", "centers_of_trade")
print("  common/centers_of_trade/:")
for fn in sorted(os.listdir(cot)):
    for k, v in pdx.load(os.path.join(cot, fn)):
        if isinstance(v, pdx.Node):
            keys = set()
            for a, b in v:
                if isinstance(b, pdx.Node):
                    keys |= {x for x, _ in b}
                else:
                    keys.add(a)
            hit = sorted(keys & set(WK))
            print("    %-28s level=%-3s wealth keys: %s" % (k, v.get("level"), hit or "none"))
n_cot = 0
hist = os.path.join(EU4, "history", "provinces")
for fn in os.listdir(hist):
    txt = pdx.strip_comments(open(os.path.join(hist, fn), encoding="latin-1", errors="replace").read())
    head = re.split(r"\n\s*\d{3,4}\.\d{1,2}\.\d{1,2}\s*=", txt)[0]
    if re.search(r"^\s*center_of_trade\s*=\s*[123]", head, re.M):
        n_cot += 1
print("    provinces with a center_of_trade in the 1444 base block:", n_cot)

# province_triggered_modifiers referenced from 1444 history
ptm = os.path.join(EU4, "common", "province_triggered_modifiers")
defs_ptm = {}
if os.path.isdir(ptm):
    for fn in os.listdir(ptm):
        if fn.endswith(".txt"):
            for k, v in pdx.load(os.path.join(ptm, fn)):
                if isinstance(v, pdx.Node):
                    defs_ptm[k] = {a: b for a, b in v if not isinstance(b, pdx.Node)}
hits = {k: {a: b for a, b in d.items() if a in WK} for k, d in defs_ptm.items()}
hits = {k: v for k, v in hits.items() if v}
print("  common/province_triggered_modifiers/ carrying a wealth key:", hits or "none")

# climate / terrain static modifiers, re-checked for the four keys
sm = pdx.load(os.path.join(EU4, "common", "static_modifiers", "00_static_modifiers.txt"))
print("  static modifiers carrying a wealth key (province-scoped blocks):")
for k, v in sm:
    if isinstance(v, pdx.Node):
        hit = {a: b for a, b in v if a in WK}
        if hit:
            print("    %-34s %s" % (k, hit))
