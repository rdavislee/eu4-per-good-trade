# -*- coding: utf-8 -*-
"""Check the coordinator's alpha_Phi sweep under the corrected (15-province) wealth field."""
import os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pdx, solver
from solver import N, ORDER, NIDX, EDGES_UND, PRICES
from drain import run_drain

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
START = (1444, 11, 11)
DATE = re.compile(r"^(\d{1,4})\.(\d{1,2})\.(\d{1,2})$")
WK = ("trade_goods_size", "trade_goods_size_modifier", "local_tax_modifier", "trade_value_modifier")

defs = {}
for sub in ("event_modifiers", "static_modifiers"):
    d = os.path.join(EU4, "common", sub)
    for fn in os.listdir(d):
        if fn.endswith(".txt"):
            for k, v in pdx.load(os.path.join(d, fn)):
                if isinstance(v, pdx.Node):
                    defs[k] = {a: b for a, b in v if not isinstance(b, pdx.Node)}

FLAT = collections.defaultdict(float); TV = collections.defaultdict(float); TX = collections.defaultdict(float)
hist = os.path.join(EU4, "history", "provinces")
for fn in os.listdir(hist):
    m = re.match(r"^\s*(\d+)", fn)
    if not m:
        continue
    pid = int(m.group(1))

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
                    if nm and nm in defs:
                        g = defs[nm]
                        FLAT[pid] += float(g.get("trade_goods_size", 0))
                        TV[pid] += float(g.get("trade_value_modifier", 0))
                        TX[pid] += float(g.get("local_tax_modifier", 0))
                else:
                    scan(v)
    scan(pdx.load(os.path.join(hist, fn)))

mon = pdx.load(os.path.join(EU4, "common", "great_projects", "01_monuments.txt"))
print("=" * 96)
print("MONUMENT AUDIT: every great project, tier live at 1444, and its owner gate")
print("=" * 96)
print("%-30s %-7s %-11s %-5s %-6s %s" % ("key", "prov", "date", "tier", "gated", "accumulated province_modifiers (wealth keys)"))
live_ungated = []
for k, v in mon:
    if not isinstance(v, pdx.Node):
        continue
    st, dt = v.get("starting_tier"), v.get("date")
    if st is None or dt is None:
        continue
    dm = DATE.match(dt)
    if not dm:
        continue
    live = (int(dm.group(1)), int(dm.group(2)), int(dm.group(3))) <= START
    tier = int(st)
    trig = v.get("can_use_modifiers_trigger")
    gated = trig is not None and len(trig) > 0
    acc = {}
    for t in range(1, tier + 1):
        tb = v.get("tier_%d" % t)
        pm = tb.get("province_modifiers") if tb is not None else None
        if pm is None:
            continue
        for a, b in pm:
            if a in WK:
                acc[a] = acc.get(a, 0.0) + float(b)
    if live and tier >= 1 and acc:
        print("%-30s %-7s %-11s %-5d %-6s %s" % (k, v.get("start"), dt, tier, gated, acc))
        if not gated:
            live_ungated.append((k, int(v.get("start")), tier, acc))
print()
print("live, tier>=1, UNGATED (empty can_use_modifiers_trigger):", [(k, p, t) for k, p, t, _ in live_ungated])
gt1 = [(k, p, t) for k, p, t, _ in live_ungated if t > 1]
print("of those, starting_tier > 1:", gt1 if gt1 else "(none)")
print()
print("distribution of starting_tier over ALL monuments live at 1444:")
cnt = collections.Counter()
gatedcnt = collections.Counter()
for k, v in mon:
    if not isinstance(v, pdx.Node):
        continue
    st, dt = v.get("starting_tier"), v.get("date")
    if st is None or dt is None:
        continue
    dm = DATE.match(dt)
    if not dm or (int(dm.group(1)), int(dm.group(2)), int(dm.group(3))) > START:
        continue
    trig = v.get("can_use_modifiers_trigger")
    cnt[int(st)] += 1
    gatedcnt[(int(st), trig is not None and len(trig) > 0)] += 1
print("  starting_tier ->", dict(sorted(cnt.items())))
print("  (tier, owner-gated) ->", dict(sorted(gatedcnt.items())))

for k, p, tier, acc in live_ungated:
    FLAT[p] += acc.get("trade_goods_size", 0.0)
    TV[p] += acc.get("trade_value_modifier", 0.0)
    TX[p] += acc.get("local_tax_modifier", 0.0)

# ------------------------------------------------------------------ wealth fields
def rows_of(corrected):
    out = []
    for r in solver.ROWS:
        bp = solver.PROV[r["pid"]]["base_production"]; bt = solver.PROV[r["pid"]]["base_tax"]
        gp = 0.2 * bp + (FLAT.get(r["pid"], 0.0) if corrected else 0.0)
        tvm = solver.LOCAL_TV_MOD.get(r["good"], 0.0) + (TV.get(r["pid"], 0.0) if corrected else 0.0)
        txm = solver.LOCAL_TAX_MOD.get(r["good"], 0.0) + (TX.get(r["pid"], 0.0) if corrected else 0.0)
        out.append((NIDX[r["node"]], bt * (1 + txm) + gp * PRICES.get(r["good"], 0.0) * (1 + tvm)))
    return out


def phiw(rows, a, noise=None):
    w = np.array([x[1] for x in rows], float)
    if noise is not None:
        w = w * noise
    pn = np.array([x[0] for x in rows])
    c = np.zeros(N); np.add.at(c, pn, w ** a); c /= c.sum()
    r = run_drain(np.ones(N) / N - c)
    d = set(r["directed"])
    return d, tuple(sorted(ORDER[i] for i in range(N) if not any(u == i for u, _ in d))), len(r["fallbacks"])


BASE = rows_of(False); CORR = rows_of(True)
print()
print("=" * 96)
print("ALPHA_PHI SWEEP")
print("=" * 96)
print("%-7s %-42s %s" % ("alpha", "sinks on the SPEC field", "sinks on the CORRECTED field"))
for a in (1.0, 1.2, 1.3, 1.4, 1.45, 1.5, 1.6, 1.7, 1.8, 1.9, 1.95, 2.0, 2.05, 2.1, 2.2, 2.3, 2.5, 3.0, 4.0):
    _, sb, _ = phiw(BASE, a)
    _, sc, _ = phiw(CORR, a)
    mark = "  <== two sinks" if len(sc) == 2 else ""
    print("%-7s %-42s %s%s" % (a, "%d %s" % (len(sb), list(sb)), "%d %s" % (len(sc), list(sc)), mark))

print()
print("fine sweep on the corrected field, 1.40 -> 1.50:")
for a in (1.40, 1.41, 1.42, 1.43, 1.44, 1.45, 1.46, 1.48, 1.50):
    _, sc, _ = phiw(CORR, a)
    print("   a=%.2f  %d sinks %s" % (a, len(sc), list(sc)))

print()
print("noise stability of the corrected field at the candidate alphas (+/-1%%, 5 seeds):")
for a in (1.5, 2.0):
    d0, s0, _ = phiw(CORR, a)
    flips = []; changes = 0
    for seed in range(5):
        rng = np.random.default_rng(seed)
        nz = 1.0 + rng.uniform(-0.01, 0.01, len(CORR))
        d1, s1, _ = phiw(CORR, a, nz)
        flips.append(len(d0 - d1)); changes += (s1 != s0)
    print("   a=%.2f sinks=%s  edge flips per seed %s  sink-set changes %d/5" % (a, list(s0), flips, changes))
