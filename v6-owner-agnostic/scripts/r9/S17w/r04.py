# -*- coding: utf-8 -*-
"""v6 batch 4 — R3: rejected-operator figures deleted (§1.6 dynamics tail, §3.9, §3.15)."""
import io, patch_lib
E = []

E.append(dict(id="R4-dyn", clears="X099/X100: node-set thresholds restated as observations",
section="1.6",
old_slice=("Other dynamics, measured: scaling **the 22 European nodes'** wealth ×2 makes `genua` the sole sink;",
           "intermediate boosts are expected behaviour, not noise.\n"),
new="""Other observations on the same field, for the emitter's benefit rather than as thresholds of the
model: scaling the 22 European *nodes* rather than European provinces makes `genua` the sole sink
from about ×1.65 (the 18-node western/central subset needs about ×2.15), and somewhere inside
roughly ×2.9–×3.5 the Cape of Good Hope **reverses** — 1444's Atlantic→Cape→Indian-Ocean drainage
becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast. The reversal is bounded above as well as
below, so it is a window and not a threshold, and its edges move with the field. *The 22 are the 18
western and central European nodes —* `english_channel`, `north_sea`, `baltic_sea`, `white_sea`,
`novgorod`, `lubeck`, `rheinland`, `saxony`, `wien`, `krakow`, `pest`, `venice`, `ragusa`, `genua`,
`champagne`, `bordeaux`, `valencia`, `sevilla` *— plus* `constantinople`, `crimea`, `kiev` *and*
`kazan`. Dev-stacking a single node's top province concentrates the map on that node; extra sinks at
intermediate boosts are expected behaviour, not noise.
"""))

E.append(dict(id="R4-39", clears="R3: no maintained figures for the superseded aggregate",
section="3.9",
old_slice=("- The value-weighted **marking order** `Φ_ord = Σ_g V_g·order_g` (v2.0's choice) is acyclic for",
           "  traded for legible, wealth-anchored, world-responsive ends.\n"),
new="""- The value-weighted **marking order** `Φ_ord = Σ_g V_g·order_g` (v2.0's choice) is acyclic for
  free and scores **higher** than `Φ_w` on self-coherence with the per-good graphs — that is the
  cost of the trade and it is not disputed. It was superseded on design grounds: its ends are
  artifacts of sweep scheduling rather than places, a majority of them terminate no good at all,
  none of the demand capitals is among them, and the end count does not concentrate as demand
  concentrates. *No figure is maintained for it here.* It is not the installed operator, its numbers
  moved with every change to the wealth field, and three successive audits spent their effort
  recounting them; the design argument above does not depend on any of them.
"""))

E.append(dict(id="R4-315a", clears="R3: 3.15's Phi_ord entry loses its figures", section="3.15",
old_slice=("most self-coherent aggregate measured (**60.3%** vs `Φ_w`'s 52.5%) and still acyclic for free —",
           "The ceiling is 60.3%, not the 62.7% v2.0 and v2.1 both quoted: that figure predates the"),
new="""the most self-coherent aggregate measured — better than `Φ_w` on that one axis, and still acyclic
for free — but its ends are scheduling artifacts rather than places and its end count does not
concentrate with demand (§3.9). *No figures are maintained for it.* v2.0 and v2.1 quoted a
self-coherence ceiling that predates the"""))

txt = io.open(patch_lib.SPEC, encoding="utf-8").read()
for e in E:
    if "old_slice" in e:
        a, b = e.pop("old_slice")
        i = txt.index(a); j = txt.index(b, i) + len(b)
        e["old"] = txt[i:j]
patch_lib.apply(E)
