# -*- coding: utf-8 -*-
"""v5 batch 2 — Group B, the installed map (changes 10–18)."""
import patch_lib
E = []

E.append(dict(id="B11", clears="change 11: delete the emergence claim", section="1.6",
old="""the sinks are wherever the wealth flow terminates. Nothing pins their count; it emerges from
concentration exactly as per-good sink counts do.""",
new="""the sinks are wherever the wealth flow terminates. **Their count is set by `α_Φ`; only their
locations are emergent.** v2.0 through v4.0 said the count "emerges from concentration exactly as
per-good sink counts do" — it does not: `α_Φ` is a stipulated constant, the count is a step function
of it (the band table below), and the value was chosen with a target count in view. What the world
state moves is *where* the sinks are and *how the map drains toward them*, which is the property
§3.1's first goal actually asks for."""))

E.append(dict(id="B10-B12", clears="changes 10, 12, 16, 17, 18: the measured block", section="1.6",
old="""Measured on 1444 data at α_Φ = 1.5 (`v4measure.py`): **two sinks, `hangzhou` and
`english_channel`**. Their ranks are 3 and 2 in the α_Φ-weighted wealth field `c_w` — *not* in raw
node wealth, where they are 12th and 1st; v2 wrote "wealth ranks" without saying which, and the
plain reading is wrong. Phase 1 selects `genua`, both sinks arrive by stall promotion, and `genua`
ends a transit node. **Eight sources**, all in the bottom half of the wealth field (`c_w` ranks
44–75, mean degree 3.1 against the map's 4.0 — v2 called them "cul-de-sacs", which their degrees
do not support). Every node drains to a sink; acyclic, 159/159 oriented, 0 fallbacks; **0 edge
flips and 0 sink-set changes under ±1% wealth noise across 5 seeds** — stabler than any per-good
graph. Its marking order is a per-node scalar whose descending comparison reproduces the DAG
(0 violations), so every consumer needing a potential still gets one.

Agreement with the per-good graphs is **53.5%** of edge-goods (52.5% value-weighted) against the
superseded `Φ_ord`'s **60.0%** — a gap of 6.5 points, not the 9.3 v2 quoted. v2's 62.7% was
measured under the *old scan-order sweep* and was never regenerated after §3.6 adopted the
deterministic one; 60.0% is the deterministic figure on v4.0's wealth field. That trade is recorded
in §3.9.

Dynamics, measured: dev-stacking `hangzhou`'s top province ×30 makes it the sole world sink
(also at ×20 and ×50; at ×10 the sink set is still three); scaling **the 22 European nodes'** wealth
×2 makes `genua` the sole sink; at ×3 the Cape of Good Hope **reverses** — 1444's
Atlantic→Cape→Indian-Ocean drainage becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast. *The
22 are the 18 western and central European nodes —* `english_channel`, `north_sea`, `baltic_sea`,
`white_sea`, `novgorod`, `lubeck`, `rheinland`, `saxony`, `wien`, `krakow`, `pest`, `venice`,
`ragusa`, `genua`, `champagne`, `bordeaux`, `valencia`, `sevilla` *— plus* `constantinople`,
`crimea`, `kiev` *and* `kazan`. *Both thresholds are set-dependent and land exactly under that
reading; under the 18-node set alone, sole-`genua` needs ×2.5 and the Cape reverses at ×2.* Sink
count breathes with concentration (transient extra sinks at intermediate boosts are expected
behaviour, not noise), and it is **non-monotone in α_Φ** — measured 5→2→1→2→3→1 across
α_Φ ∈ {1, 1.5, 2, 3, 4, 8} on 1444 (`v4measure.py`). The count tracks how many world-class wealth
poles the flow separates, not α_Φ itself.""",
new="""Measured on 1444 data at α_Φ = 1.5 (`v5measure.py`): **one sink, `hangzhou`** — rank 1 in the
α_Φ-weighted wealth field `c_w`, and rank 10 in raw node wealth, where `english_channel` is 1st.
*(v2 through v4 reported two sinks. That result was measured on a wealth field missing the sixteen
provinces §1.3 now carries; correcting the field removes it. v2 also wrote "wealth ranks" without
saying which, and the plain reading was wrong then too.)* Phase 1 selects `hangzhou` directly, so
there are **0 promotions and 0 fallbacks** — the self-correction never fires on this input. **Seven
sources** — `kongo`, `patagonia`, `james_bay`, `mississippi_river`, `chengdu`, `australia`, `tunis`
— all in the bottom half of the wealth field (`c_w` ranks 52–79, mean degree 3.0 against the map's
4.0; v2 called them "cul-de-sacs", which their degrees do not support). Every node drains to the
sink; acyclic, 159/159 oriented; **0 edge flips and 0 sink-set changes under ±1% wealth noise across
5 seeds**. Its marking order is a per-node scalar whose descending comparison reproduces the DAG
(0 violations), so every consumer needing a potential still gets one.

Agreement with the per-good graphs is **52.5%** of edge-goods (51.5% value-weighted) against the
superseded `Φ_ord`'s **60.3%** — a gap of 7.8 points. v2's 62.7% was measured under the *old
scan-order sweep* and was never regenerated after §3.6 adopted the deterministic one. That trade is
recorded in §3.9.

**The sink count is a step function of `α_Φ`.** Measured across α_Φ = 1.00…3.00 at 0.01:

| sinks | α_Φ band | width |
|---|---|---|
| 1 — `hangzhou` | **[1.43, 1.93]** | **0.51** — the widest band on this field, and the one α_Φ = 1.5 sits in |
| 3 — `doab`, `genua`, `hangzhou` | [2.26, 2.71] | 0.46 |
| 2 — `genua`, `hangzhou` | [1.94, 2.25] | 0.32 |
| 2 — `english_channel`, `hangzhou` | [1.41, 1.42] | 0.02 |

The last row is v4.0's result and it is **not reproducible**: under ±1% wealth noise that window
moves or disappears entirely, while the wide bands move by ≤0.03. It is not a band, so no constant
could honestly sit in it. `α_Φ` is **retained at 1.5** because it sits inside the widest band and
nothing now selects a different value — not because it was derived (§2.3). Sampled at the six values
v2 used, the count is non-monotone: **5 → 1 → 2 → 4 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}.

**One sink at 1444 is a snapshot, not a fixed feature, and the map says so under load.** Holding
α_Φ = 1.5 and moving nothing else (`europe.py`):

- **A 1–2% European development edge produces a European sink.** At ×1.02 across Europe's 823
  counted provinces the sinks are `{doab, english_channel, hangzhou, wien}`; `english_channel` is a
  sink at every larger factor tested. At ×1.56 the sinks are `{english_channel, rheinland}` and Asia
  holds none. That range is far below what the Renaissance, Colonialism and Printing Press deliver
  over 1450–1550.
- **The Lowlands alone suffice.** Developing only the nine Lowland provinces in `english_channel`
  (Holland, Zeeland, Vlaanderen, Brabant, Antwerpen, Utrecht, Gelre, Friesland, Breda) by ×1.20
  makes `english_channel` a sink beside `hangzhou`, and it stays one through ×10.
- **Robust to noise, responsive to growth.** ±2% *random* wealth noise leaves the 1444 sink set
  unchanged on three seeds; **+2% applied systematically to Europe alone changes it**. The map does
  not twitch, and it does move.

**And the 1444 map draws the pre-Columbian trade geography unprompted.** The route from Europe to
the sink is the Silk Road: `genua → alexandria → aleppo → persia → lahore → doab → ganges_delta →
burma → gulf_of_siam → canton → hangzhou`. From the north it is the Volga:
`north_sea → white_sea → novgorod → kazan → astrakhan → persia → …`. From the Channel it is the
Hansa and the Danube: `english_channel → lubeck → saxony → wien → venice → ragusa →
constantinople → aleppo → …`. Nothing routes through the Cape, which is what a 1444 map should
say. *(The Cape is not idle — in the per-good graphs it already carries Asian spices to Europe:
`malacca → cape_of_good_hope → zanzibar → gulf_of_aden → alexandria → genua`. `Φ_w` models power,
not cargo; §3.9.)*

Other dynamics, measured: scaling **the 22 European nodes'** wealth ×2 makes `genua` the sole sink;
between **×3 and ×3.75** the Cape of Good Hope **reverses** — 1444's Atlantic→Cape→Indian-Ocean
drainage becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast — and outside that window it does
not, so the reversal is a band and not a threshold. *The 22 are the 18 western and central European
nodes —* `english_channel`, `north_sea`, `baltic_sea`, `white_sea`, `novgorod`, `lubeck`,
`rheinland`, `saxony`, `wien`, `krakow`, `pest`, `venice`, `ragusa`, `genua`, `champagne`,
`bordeaux`, `valencia`, `sevilla` *— plus* `constantinople`, `crimea`, `kiev` *and* `kazan`; under
the 18-node set alone sole-`genua` needs ×2.5. Dev-stacking `hangzhou`'s top province keeps it the
sole sink at ×20, ×30 and ×50, with a transient split into three at ×10 — extra sinks at
intermediate boosts are expected behaviour, not noise."""))

E.append(dict(id="B-scale", clears="change 16: the scale figures", section="1.6",
old="""×1 and above, 13 edge flips at ×10⁻², and at ×10⁻⁶ the sink set collapses to a single node.
Normalising into (−1, 1) scales 1444's `b_w` *up* (its largest magnitude is 0.0225) and is safe;""",
new="""×1 and above, 16 edge flips at ×10⁻², and 83 at ×10⁻⁶ — the orientation degrades while the sink
set happens to survive, so the sink set is not the quantity to watch here.
Normalising into (−1, 1) scales 1444's `b_w` *up* (its largest magnitude is 0.0227) and is safe;"""))

E.append(dict(id="B13", clears="change 13: the calibration sentence", section="2.3",
old="""the aggregate-graph exponent `α_Φ = 1.5` (calibrated so the 1444 start yields the two-sink
hangzhou/english_channel map, §1.6 — a constant like `P₀`; world-responsiveness flows through
wealth, never through this knob),""",
new="""the aggregate-graph exponent `α_Φ = 1.5` (a constant like `P₀`; world-responsiveness flows through
wealth, never through this knob). **Its stated calibration is withdrawn.** v2.1 through v4.0 said
1.5 was "calibrated so the 1444 start yields the two-sink hangzhou/english_channel map"; on the
corrected wealth field of §1.3 it does not yield that map, and the map it was fitted to is not
reproducible under noise (§1.6). 1.5 is retained because it sits inside the widest sink-count band
and nothing now selects a different value — not because it was derived. Any future change to it is
a design decision about how many ends the installed graph should have, and should be recorded as
one,"""))

E.append(dict(id="B14", clears="change 14: the adoption rationale", section="3.9",
old="""- `Φ_w`, adopted: two vanilla-like ends at 1444 that move with the world, from the same operator
  the goods already use.""",
new="""- `Φ_w`, adopted: **one operator, one set of guarantees, and ends that move with the world.** It
  reuses §1.1 unchanged, so LP feasibility, acyclicity, determinism and scan-invariance come for
  free and the correctness check stays a single combinatorial comparison; and its ends are places
  the wealth actually is, so they move when the wealth moves (§1.6's institution result). *v2.1
  through v4.0 justified the adoption by "two vanilla-like ends at 1444" — the reason it was
  accepted despite losing self-coherence. On the corrected wealth field there is one end, in China,
  matching none of vanilla's three, so that premise is withdrawn. The trade is now stated as what it
  is: 7.8 points of self-coherence given up for one operator and world-responsive ends, and the
  1444 count is whatever the field gives.*"""))

patch_lib.apply(E)
