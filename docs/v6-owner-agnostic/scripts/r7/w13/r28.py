# -*- coding: utf-8 -*-
"""v6 batch 28 — round 5, as corrected by pre-confirmation. Four of the twenty staged values were
wrong, including one I had staged as a *finding*: the claim that the shipped basin at x1.53 falls
outside its own relabelling range does not reproduce. The conclusion survives; the reason changes."""
import patch_lib
E = []

# ---- Y047: the fifth province-state modifier -----------------------------------------------------
E.append(dict(id="Y047", clears="Y047: unrest is a fifth province-state modifier", section="1.3",
old="""| `occupied` | `trade_goods_size_modifier = -0.5` **and** `local_tax_modifier = -0.5` | both |""",
new="""| `occupied` | `trade_goods_size_modifier = -0.5` **and** `local_tax_modifier = -0.5` | both |
| `unrest` | `local_tax_modifier = -0.02` **per point of revolt risk** | `tax_value` |"""))

E.append(dict(id="Y047b", clears="Y047: what unrest costs, and that its scaling is sourced",
section="1.3",
old="""Only `occupied` touches the tax term; the other three reach `goods_produced` alone.""",
new="""`occupied` and `unrest` touch the tax term; the other three reach `goods_produced` alone. **`unrest`
is live at the 1444 start**: 21 counted provinces carry revolt risk between 4.834 and 14.834 in the
save, costing **12.23 ducats — 0.115% of world wealth** — and admitting it moves **no edge** of the
installed graph, so it is a fidelity correction with no orientation consequence. *Its scaling is
stated in the file:* the `unrest` block's own comment reads `#10% longer time to build troops for each
rr`, so its values apply per point, and the neighbouring `nationalism` block uses the same convention.
*(Sixteen of the 21 are resolvable from `history/provinces` at integer risk 5/8/10/15; the other five,
all Shirvan-owned, receive theirs at runtime, so the model reads the save.)*"""))

E.append(dict(id="Y049", clears="Y049: devastation is now the only unsourced scaling law", section="1.3",
old="""| | *The magnitudes and directions above are all read from `00_static_modifiers.txt`. What no shipped file states is the **scaling law** for `devastation`: the model assumes the modifier applies in proportion to the level, `-2 × level/100`, and that proportionality is an assumption rather than a file value.* | |""",
new="""| | *The magnitudes and directions above are all read from `00_static_modifiers.txt`. What no shipped file states is the **scaling law** for `devastation`: the model assumes the modifier applies in proportion to the level, `-2 × level/100`, and that proportionality is an assumption rather than a file value. It is the **only** such assumption in this table — `unrest` and `nationalism` both carry per-unit comments in that same file, so the convention for stating a scaling exists and `devastation` simply does not use it.* | |"""))

# ---- V06: the two figures are one measurement in different units ---------------------------------
E.append(dict(id="V06a", clears="V06: 1.6's objective figure, with its unit and its status",
section="1.6",
old="""and the LP objective is identical to within
4.44e-16, so these are different *optimal* orientations rather than different answers.""",
new="""and the LP objective is identical to
within four units in the last place, so these are different *optimal* orientations rather than
different answers."""))

E.append(dict(id="V06b", clears="V06: 2.4's copy, same correction", section="2.4",
old="""   objective identical to within 4.44e-16 (`relabel6.py`, which validates its instrument against""",
new="""   objective identical to within four units in the last place — 4.44e-16 absolute against an objective
   of 0.712, which is the same quantity as the 6.2e-16 relative deviation and not a second measurement,
   and which grows to 6–7 ULP at larger trial counts, so it is a sample maximum rather than a bound
   (`relabel6.py`, which validates its instrument against"""))

# ---- T03: the 580 sweep, restored with an honest provenance --------------------------------------
E.append(dict(id="T03", clears="T03: restore the withdrawn sweep, and drop the false premise",
section="2.4",
old="""magnitude as the razed-China perturbation §2.8 treats as a major world event. *(Earlier versions
   quoted a 580-of-580 per-good sweep and an arc-permutation result whose scripts were never shipped;
   both are withdrawn in favour of the figure a script in this tree reproduces.)*""",
new="""magnitude as the razed-China perturbation §2.8 treats as a major world event. The same effect on the
   **per-good** graphs is 580 of 580 (29 goods × 20 relabellings), from
   `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`. *(v6.0 withdrew that sweep on the ground that
   its script had never shipped. The script is in the tree and runs; the withdrawal was the error, not
   the figure. No v1–v5 spec ever printed it either, so it was never "quoted by earlier versions" —
   it comes from this project's working files.)*"""))

# ---- Phi_ord: the fraction is ordering-conditional, so it goes ------------------------------------
E.append(dict(id="T04", clears="T04: the Phi_ord fraction is a property of the node order", section="3.9",
old="""  artifacts of sweep scheduling rather than places, **half** of them terminate no good at all (7 of
  14 on the 1444 field),""",
new="""  artifacts of sweep scheduling rather than places — and the sharpest evidence for that is what
  relabelling does to them: across 20 relabellings the end count runs **12 to 19** and the end set is
  **never twice the same**, so neither the count nor the share terminating no good is a property of
  the world. Most of those ends terminate no good,"""))

# ---- T05: the basin, with the reason that actually holds -----------------------------------------
E.append(dict(id="T05", clears="T05: no basin figure, for the reason that reproduces", section="1.6",
old="""basin grows from 18 nodes to 28 by about ×1.44, then gives way as the end itself migrates: `genua`
first holds an end at ×1.63 and is the sole end from ×1.64 through ×2.00 — and""",
new="""basin widens, non-monotonically, and then gives way as the end itself migrates: `genua` first holds an
end at ×1.63 and is the sole end from ×1.64 through ×2.00 — and"""))

E.append(dict(id="T06", clears="T06: basin size joins the ordering-conditional list", section="1.6",
old="""Conditional: the sink set's membership
and size, and everything derived from them — §2.4's end-flag list, and which European node holds an
end in the table below.""",
new="""Conditional: the sink set's membership
and size, and everything derived from them — §2.4's end-flag list, which European node holds an end in
the table below, and **the size of any node's drainage basin**. *No basin figure is quoted anywhere in
this section, because at the growth factors where one would be interesting `english_channel` holds an
end in only a handful of orderings, so any range is the spread of a handful of observations rather
than a measurement.*"""))

patch_lib.apply(E)
