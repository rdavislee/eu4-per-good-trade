# -*- coding: utf-8 -*-
"""Does a European sink appear once the institutions give Europe the development edge?
Option 1 field (16 local-modifier provinces), alpha_Phi = 1.5 throughout - no knob is moved."""
import numpy as np, collections, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx
from wealthmodel import *
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
EUR = set(int(x) for x in pdx.values(pdx.load(os.path.join(EU4, "map", "continent.txt")).get("europe")))
LOW = set(json.load(open("lowlands.json")))
OWNED = {r["pid"] for r in ROWS}
eur_owned = sorted(EUR & OWNED)
print("European owned city provinces in the model: %d of %d owned" % (len(eur_owned), len(OWNED)))

def run(mult, label, show_route=False):
    w = wealth(mult); r, cw = phi_w(w, 1.5)
    s = sinks(r); nw = node_wealth(w)
    eu_nodes = {ORDER[NIDX[n]] for n in ORDER
                if any(p in EUR for p in NODES[n]["members"])}
    eu_sinks = [x for x in s if x in eu_nodes]
    print("  %-34s sinks=%-46s European sink: %s" % (label, s, eu_sinks or "none"))
    return r, s, eu_sinks, nw

print("\n=== 1. uniform European development growth (all %d provinces) ===" % len(eur_owned))
base = run({}, "1444 baseline (x1.00)")
for f in (1.1,1.2,1.3,1.4,1.5,1.6,1.8,2.0,2.5,3.0):
    run({p: f for p in eur_owned}, "Europe dev x%.2f" % f)

print("\n=== 2. the Lowlands only (%d provinces, 9 in english_channel) ===" % len(LOW))
for f in (2,3,4,5,6,8,10,12,15,20):
    run({p: f for p in LOW if p in OWNED}, "Lowlands dev x%d" % f)

print("\n=== 3. institution-realistic: western Europe leads, eastern Europe lags ===")
# Renaissance 1450 (Italy), Colonialism 1500 (Iberia), Printing Press 1550 (Germany).
# Embrace order -> growth advantage.  West = the 22 European trade nodes' members that are
# also on the Europe continent; East = the rest of European provinces.
WEST_NODES = ["english_channel","north_sea","baltic_sea","lubeck","rheinland","saxony","wien",
              "venice","ragusa","genua","champagne","bordeaux","valencia","sevilla"]
west = {p for n in WEST_NODES for p in NODES[n]["members"] if p in EUR and p in OWNED}
east = (EUR & OWNED) - west
print("  west %d provinces, east %d" % (len(west), len(east)))
for fw, fe in ((1.3,1.1),(1.5,1.15),(1.75,1.2),(2.0,1.25),(2.5,1.3)):
    m = {p: fw for p in west}; m.update({p: fe for p in east})
    run(m, "west x%.2f / east x%.2f" % (fw, fe))
