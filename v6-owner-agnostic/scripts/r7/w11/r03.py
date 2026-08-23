# -*- coding: utf-8 -*-
"""v6 batch 3 — §1.6: the installed map on the (c) field, the alpha stipulation, Europe stated
directionally (R2), and the rejected-operator comparison figure removed (R3)."""
import io, patch_lib
E = []

E.append(dict(id="R3-measured", clears="the measured block, on the (c) field", section="1.6",
old_slice=("Measured on 1444 data at α_Φ = 1.5 (`v5measure.py`): **one sink, `hangzhou`**",
           "recorded in §3.9.\n"),
new="""Measured on 1444 data at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and
`hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12. Phase 1 selects `genua`; both sinks
arrive by stall promotion and `genua` ends a transit node, so there are **2 promotions and 0
fallbacks**. **Eight sources** — all in the bottom half of the wealth field, `c_w` ranks **44–75**,
mean degree **3.1** against the map's 4.0. *(v2 called them "cul-de-sacs", which their degrees do not
support.)* Every node drains to a sink; acyclic, 159/159 oriented; largest `|b_w|` **0.0226**; the
sink set is unchanged under ±1% wealth noise on three seeds. Its marking order is a per-node scalar
whose descending comparison reproduces the DAG (0 violations), so every consumer needing a potential
still gets one.

Per good, on the same field: **1–8 sinks, mean 3.52**, 29/29 acyclic, **0 fallbacks fired**, and
**90.2%** of ordered node pairs (5,703 of 6,320) connected by at least one good's directed path.

Agreement with the per-good graphs is **53.5%** of edge-goods (**52.1%** value-weighted). The
superseded marking-order aggregate scored higher on that measure; §3.9 records why the trade was
taken and no longer maintains a figure for an operator the model does not install.
"""))

E.append(dict(id="R3-bands", clears="A1: alpha_Phi is a stipulation; the band table records alternatives",
section="1.6",
old_slice=("**The sink count is a step function of `α_Φ`.** Measured across α_Φ = 1.00…3.00 at 0.01:",
           "v2 used, the count is non-monotone: **5 → 1 → 2 → 4 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}.\n"),
new="""**`α_Φ = 1.5` is a stipulated design constant, exactly as `P₀ = 2.0` is.** It is superlinear so
that a few very rich provinces outweigh a dense mediocre region, and it is round. It is **not**
derived, and the document no longer offers a derivation: v2.1 through v4.0 said it was calibrated to
reproduce a two-sink 1444 map, and v5.0 said it sat in the widest sink-count band. The first was
fitted to a field that no longer exists; the second depended on where the α scan was truncated —
scanned over [1, 8] rather than [1, 3], the widest band is **1.70** wide ([3.51, 5.21],
`{doab, genua, hangzhou}`) and 1.5's is not the widest by any margin. Any future change to it is a
design decision about how many ends the installed graph should have, and §2.3 governs recording it.

What the value buys is recorded rather than argued. Across α_Φ = 1.00…8.00 at 0.01 the sink set is a
step function, and α_Φ = 1.5 sits in the band **[1.38, 1.63], width 0.25**, which gives
`{english_channel, hangzhou}`. Sampled at the six values v2 used, the count is non-monotone:
**6 → 2 → 1 → 2 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}.

*A warning for anyone revising this, because the mistake is available and has been made twice: the
1444 map has two ends and vanilla's authored map has three, and it is tempting to justify 1.5 by
that resemblance. Do not. That is the calibration §2.3 withdrew, and §3.9's adoption argument does
not rest on it.*
"""))

E.append(dict(id="R3-europe", clears="P1/P2/R2: Europe stated directionally, the Lowlands claim deleted",
section="1.6",
old_slice=("**One sink at 1444 is a snapshot, not a fixed feature, and the map says so under load.**",
           "  not twitch, and it does move.\n"),
new="""**Europe becomes the centre of trade as it develops.** That is the design claim, and it is what
§3.1's first goal asks the field to deliver. At 1444 the map already ends in the Channel and in
Hangzhou; as European development compounds, the Channel's basin grows and Asia's pole fades, and
past a broad range of European growth Asia holds no end at all. The mechanism is what carries this:
wealth is linear in development (§1.3), so developing a region moves its `c_w` share directly, and
`Φ_w`'s ends follow the wealth.

Observed on the 1444 field, holding α_Φ = 1.5 and scaling European development only (`europe.py`,
824 counted European provinces):

| European development | `Φ_w` sinks |
|---|---|
| ×1.00 (1444) | `english_channel`, `hangzhou` |
| ×1.02 | `english_channel`, `hangzhou`, **`wien`** |
| ×1.56 | `english_channel`, **`rheinland`** — Asia holds none |
| ×2.00 | `genua` alone |

These are properties of this snapshot, not constants of the model: they are what one field yielded
under one scaling, and a different world state moves them. Under (c) **scaling development and
scaling wealth are the same operation** — maximum difference 0.0 across the European set — so the
distinction that made v5.0's version of this table wrong does not arise.

What the shipped files settle, independently of any threshold: all three institutions the period is
named for begin **in Europe** between 1450 and 1550 — Renaissance `1450.1.1` at Florence (province
116), Colonialism `1500.1.1` at Sevilla (224), Printing Press `1550.1.1` at Frankfurt (1876)
(`common/institutions/00_Core.txt`) — and the Renaissance's embracement bonus is
`development_cost = -0.05`, a standing discount on every subsequent development point. Those bonuses
are country-scoped, so §1.3 excludes them from wealth directly; they reach the map only by changing
how fast development grows, which is the input scaled above.
"""))

E.append(dict(id="R3-routes", clears="X097: the Cape universal narrowed; routes on the (c) field",
section="1.6",
old_slice=("**And the 1444 map draws the pre-Columbian trade geography unprompted.**",
           "not cargo; §3.9.)*\n"),
new="""**And the 1444 map draws the pre-Columbian trade geography unprompted.** The route from Genoa to
the Asian sink is the Silk Road: `genua → alexandria → aleppo → persia → lahore → lhasa →
ganges_delta → burma → gulf_of_siam → canton → hangzhou`. From the north it is the Volga, and from
the Channel the Hansa and the Danube. **No Europe→sink route passes the Cape of Good Hope** —
checked from `genua`, `north_sea` and `english_channel` — which is what a 1444 map should say.

The Cape is nonetheless a live conduit, not an idle one: in-degree 1, out-degree 3, with **132
ordered node pairs** whose path runs through it, carrying Atlantic drainage into the Indian Ocean.
*(v5.0 said "nothing routes through the Cape", which is false as a universal and was only ever
checked on the Europe→sink routes.)* In the per-good graphs it also carries Asian spices to Europe;
`Φ_w` models power, not cargo (§3.9).
"""))

txt = io.open(patch_lib.SPEC, encoding="utf-8").read()
for e in E:
    if "old_slice" in e:
        a, b = e.pop("old_slice")
        i = txt.index(a); j = txt.index(b, i) + len(b)
        e["old"] = txt[i:j]
patch_lib.apply(E)
