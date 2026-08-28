# -*- coding: utf-8 -*-
"""Audit of spec v4.0 §1.3: 'exactly two modifiers enter wealth in vanilla' and
'no 1444 province was observed carrying a flat bonus in the first block'.

Enumerates, from the install, every province-scoped source live at 1444.11.11 with no owner
input that touches goods_produced / trade_value / tax_value, then re-runs Phi_w with them.
"""
import os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pdx, solver
from solver import N, ORDER, NIDX, EDGES_UND, PRICES
from drain import run_drain

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
START = (1444, 11, 11)
DATE = re.compile(r"^(\d{1,4})\.(\d{1,2})\.(\d{1,2})$")

# ---- 1. every event/static modifier definition, flattened -------------------
defs = {}
for root, sub in (("common", "event_modifiers"), ("common", "static_modifiers")):
    d = os.path.join(EU4, root, sub)
    for fn in os.listdir(d):
        if not fn.endswith(".txt"):
            continue
        for k, v in pdx.load(os.path.join(d, fn)):
            if isinstance(v, pdx.Node):
                defs[k] = {kk: vv for kk, vv in v if not isinstance(vv, pdx.Node)}

WEALTH_KEYS = ("trade_goods_size", "trade_goods_size_modifier",
               "local_tax_modifier", "trade_value_modifier")

# ---- 2. start-applied province modifiers -----------------------------------
hist = os.path.join(EU4, "history", "provinces")
applied = collections.defaultdict(list)
for fn in os.listdir(hist):
    m = re.match(r"^\s*(\d+)", fn)
    if not m:
        continue
    pid = int(m.group(1))
    root = pdx.load(os.path.join(hist, fn))

    def scan(node):
        for k, v in node:
            if isinstance(v, pdx.Node):
                dm = DATE.match(k or "")
                if dm:
                    if (int(dm.group(1)), int(dm.group(2)), int(dm.group(3))) <= START:
                        scan(v)
                    continue
                if k in ("add_permanent_province_modifier", "add_province_modifier"):
                    nm = v.get("name")
                    if nm:
                        applied[pid].append(nm)
                else:
                    scan(v)
            elif k == "add_province_triggered_modifier":
                applied[pid].append(v)
    scan(root)

print("=" * 92)
print("A. province modifiers applied at/before 1444.11.11 that touch a wealth quantity")
print("=" * 92)
hits = collections.defaultdict(list)
for pid, names in applied.items():
    for nm in names:
        d = defs.get(nm, {})
        got = {k: d[k] for k in WEALTH_KEYS if k in d}
        if got:
            hits[(nm, tuple(sorted(got.items())))].append(pid)
for (nm, got), pids in sorted(hits.items()):
    print("  %-40s %-40s %d province(s): %s" % (nm, dict(got), len(pids), sorted(pids)))
if not hits:
    print("  (none)")

# ---- 3. monuments live at 1444 with an empty can_use_modifiers_trigger ------
print()
print("=" * 92)
print("B. great_projects live at 1444.11.11, starting_tier >= 1, EMPTY can_use_modifiers_trigger")
print("=" * 92)
mon = pdx.load(os.path.join(EU4, "common", "great_projects", "01_monuments.txt"))
monhits = []
for k, v in mon:
    if not isinstance(v, pdx.Node):
        continue
    st = v.get("starting_tier")
    dt = v.get("date")
    if st is None or dt is None:
        continue
    dm = DATE.match(dt)
    if not dm or (int(dm.group(1)), int(dm.group(2)), int(dm.group(3))) > START:
        continue
    tier = int(st)
    if tier < 1:
        continue
    trig = v.get("can_use_modifiers_trigger")
    gated = trig is not None and len(trig) > 0
    acc = {}
    for t in range(1, tier + 1):
        tb = v.get("tier_%d" % t)
        if tb is None:
            continue
        pm = tb.get("province_modifiers")
        if pm is None:
            continue
        for kk, vv in pm:
            if kk in WEALTH_KEYS:
                acc[kk] = acc.get(kk, 0.0) + float(vv)
    if acc:
        monhits.append((k, int(v.get("start")), tier, gated, acc))
for k, p, tier, gated, acc in monhits:
    print("  %-28s province %-6d tier %d  owner-gated=%-5s  %s" % (k, p, tier, gated, acc))

# ---- 4. what the reference solver applies -----------------------------------
print()
print("=" * 92)
print("C. what solver.py actually applies")
print("=" * 92)
print("  LOCAL_TAX_MOD =", solver.LOCAL_TAX_MOD, " LOCAL_TV_MOD =", solver.LOCAL_TV_MOD,
      " GOODS_PRODUCED_FACTOR =", solver.GOODS_PRODUCED_FACTOR)

# ---- 5. does folding the ungated ones in move Phi_w? ------------------------
FLAT_GP = collections.defaultdict(float)      # pid -> flat trade_goods_size
TVMOD = collections.defaultdict(float)        # pid -> extra trade_value_modifier
TAXMOD = collections.defaultdict(float)
for (nm, got), pids in hits.items():
    g = dict(got)
    for pid in pids:
        FLAT_GP[pid] += float(g.get("trade_goods_size", 0.0))
        TVMOD[pid] += float(g.get("trade_value_modifier", 0.0))
        TAXMOD[pid] += float(g.get("local_tax_modifier", 0.0))
for k, p, tier, gated, acc in monhits:
    if gated:
        continue
    FLAT_GP[p] += float(acc.get("trade_goods_size", 0.0))
    TVMOD[p] += float(acc.get("trade_value_modifier", 0.0))
    TAXMOD[p] += float(acc.get("local_tax_modifier", 0.0))

print()
print("=" * 92)
print("D. effect on the installed graph Phi_w (alpha_Phi = 1.5)")
print("=" * 92)


def phiw(rows, a=1.5):
    wealth = np.array([r["w"] for r in rows])
    pn = np.array([NIDX[r["node"]] for r in rows])
    c = np.zeros(N)
    np.add.at(c, pn, wealth ** a)
    c /= c.sum()
    r = run_drain(np.ones(N) / N - c)
    d = set(r["directed"])
    return d, sorted(ORDER[i] for i in range(N) if not any(u == i for u, _ in d))


base = [dict(node=r["node"], w=r["tax"] + r["prod_income"]) for r in solver.ROWS]
d0, s0 = phiw(base)
print("  spec baseline sinks:", s0)

corrected = []
touched = 0
for r in solver.ROWS:
    gp = solver.GOODS_PRODUCED_FACTOR * solver.PROV[r["pid"]]["base_production"] + FLAT_GP.get(r["pid"], 0.0)
    tv = gp * PRICES.get(r["good"], 0.0) * (1.0 + solver.LOCAL_TV_MOD.get(r["good"], 0.0) + TVMOD.get(r["pid"], 0.0))
    tax = solver.PROV[r["pid"]]["base_tax"] * (1.0 + solver.LOCAL_TAX_MOD.get(r["good"], 0.0) + TAXMOD.get(r["pid"], 0.0))
    if FLAT_GP.get(r["pid"]) or TVMOD.get(r["pid"]) or TAXMOD.get(r["pid"]):
        touched += 1
    corrected.append(dict(node=r["node"], w=tax + tv))
d1, s1 = phiw(corrected)
print("  provinces whose wealth changes:", touched)
print("  corrected sinks           :", s1)
print("  Phi_w edges flipped       : %d of %d" % (len(d0 - d1), len(EDGES_UND)))
bw = {}
for r, c in zip(base, corrected):
    bw[r["node"]] = bw.get(r["node"], [0.0, 0.0])
    bw[r["node"]][0] += r["w"]; bw[r["node"]][1] += c["w"]
worst = sorted(bw.items(), key=lambda kv: -(kv[1][1] - kv[1][0]))[:6]
print("  largest node-wealth moves :", [(k, round(v[0], 1), round(v[1], 1)) for k, v in worst])
print("  richest single province   : base %.2f -> corrected %.2f"
      % (max(r["w"] for r in base), max(r["w"] for r in corrected)))
