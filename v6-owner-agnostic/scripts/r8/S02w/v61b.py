# -*- coding: utf-8 -*-
"""v6.1 batch B -- the rest of 1.6: what is conditional (nothing, now), the per-node figures, the
per-good figures, and alpha stripped of justification."""
import patch_lib
E = []

E.append(dict(id="B1", clears="B1: nothing is conditional on the node order any more", section="1.6",
old="""**What is conditional on the node order, and what is not.** Conditional: the sink set's membership
and size, and everything derived from them — §2.4's end-flag list, which European node holds an end in
the table below, and **the size of any node's drainage basin**. *No basin figure is quoted anywhere in
this section, because at the growth factors where one would be interesting `english_channel` holds an
end in only a handful of orderings, so any range is the spread of a handful of observations rather
than a measurement.* Not conditional, over the same relabellings: the map is fully oriented
(159/159) and acyclic every time, no fallback ever fires, and the LP objective is identical to
within four units in the last place, so these are different *optimal* orientations rather than
different answers. §2.4 item 1
requires the emitter to fix one canonical order for exactly this reason. Phase 1 selects `genua`; both sinks
arrive by stall promotion and `genua` ends a transit node, so there are **2 promotions and 0
fallbacks**. **Eight sources** — all in the bottom half of the wealth field, `c_w` ranks **44–75**,
mean degree **3.1** against the map's 4.0. *(v2 called them "cul-de-sacs", which their degrees do not
support.)* Every node drains to a sink; acyclic, 159/159 oriented; largest `|b_w|` **0.0225**; the
sink set is unchanged under ±1% wealth noise on three seeds. Its marking order is a per-node scalar
whose descending comparison reproduces the DAG (0 violations), so every consumer needing a potential
still gets one.

Per good, on the same field: **1–8 sinks, mean 3.72**, 29/29 acyclic, **0 fallbacks fired**, and
**89.6%** of ordered node pairs (5,663 of 6,320) connected by at least one good's directed path.

Agreement with the per-good graphs is **53.6%** of edge-goods (**52.3%** value-weighted). The""",
new="""**What is conditional on the node order.** Nothing that this document quotes. Over the 180
relabellings above, the sink set, every edge direction, the promotion and fallback counts and the
per-good figures were identical, so the distinction v6.0 drew between world-properties and
ordering-artifacts has collapsed into the first category. The emitter should still fix one canonical
order — the guarantee is measured over the orderings tried, not proved — and §2.4 item 1 records
that as an implementation requirement rather than a correctness worry.

Phase 1 selects `hangzhou`; `genua` arrives by stall promotion, so there is **1 promotion and 0
fallbacks**. **Five sources** — all in the bottom half of the wealth field, `c_w` ranks **55–79**,
mean degree **2.4** against the map's 4.0. *(v2 called them "cul-de-sacs"; at this α their degrees
are closer to that reading than at α_Φ = 1.5, where the mean was 3.1 — but it is a description of
five nodes, not a property of the operator.)* Every node drains to a sink; acyclic, 159/159 oriented;
largest `|b_w|` **0.0347**; the sink set is unchanged under ±1% wealth noise on three seeds. Its
marking order is a per-node scalar whose descending comparison reproduces the DAG (0 violations), so
every consumer needing a potential still gets one.

Per good, on the same field: **2–8 sinks, mean 3.69**, 29/29 acyclic, **0 fallbacks fired**, and
**90.5%** of ordered node pairs (5,721 of 6,320) connected by at least one good's directed path.

Agreement with the per-good graphs is **55.2%** of edge-goods (**55.0%** value-weighted). The"""))

E.append(dict(id="B2", clears="B2: alpha and epsilon are hyperparameters; no justification offered",
section="1.6",
old="""**`α_Φ = 1.5` is a stipulated design constant, exactly as `P₀ = 2.0` is.** It is superlinear so
that a few very rich provinces outweigh a dense mediocre region, and it is round. It is **not**
derived, and the document no longer offers a derivation: v2.1 through v4.0 said it was calibrated to
reproduce a two-sink 1444 map, and v5.0 said it sat in the widest sink-count band. The first was
fitted to a field that no longer exists; the second depended on where the α scan was truncated —
scanned over [1, 8] rather than [1, 3], the widest band is **1.71** wide ([3.50, 5.21],
`{doab, genua, hangzhou}`) and 1.5's is not the widest by any margin. Any future change to it is a
design decision about how many ends the installed graph should have, and §2.3 governs recording it.

What the value buys is recorded rather than argued. Across α_Φ = 1.00…8.00 at 0.01 the sink set is a
step function, and α_Φ = 1.5 sits in the band **[1.38, 1.63], width 0.25**, which gives
`{english_channel, hangzhou}`. Sampled at the six values v2 used, the count is non-monotone:
**6 → 2 → 1 → 2 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}.

*A warning for anyone revising this, because the mistake is available and has been made twice: the
1444 map has two ends and vanilla's authored map has three, and it is tempting to justify 1.5 by
that resemblance. Do not. That is the calibration §2.3 withdrew, and §3.9's adoption argument does
not rest on it.*""",
new="""**`α_Φ = 2.0` and `TIE_EPS = 1e-3` are hyperparameters. The choice is developer taste, and this
document offers no justification for either beyond that.** No derivation is claimed, none is
implied, and none should be reconstructed from the figures below: they describe what the field does
around the chosen values, which is what an implementer needs in order to change them, not an argument
for keeping them.

Sensitivity, recorded rather than argued. Across α_Φ = 1.00…8.00 at 0.01 the sink set is a step
function, and α_Φ = 2.0 sits in the band **[1.63, 3.28], width 1.65**, which gives
`{genua, hangzhou}`. Sampled at six values, the count is non-monotone: **3 → 1 → 2 → 2 → 1 → 1**
across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}. For `TIE_EPS`, the sink set is unchanged from about **1e-6 to
about 1**, six orders of magnitude, because the term is a tie-break: below that range it falls under
the solver's tolerance and stops registering, and above it the term exceeds the base arc cost of 1
and stops being a perturbation. `scripts/epsilon6.py` reports the bands and bisects their edges.

*A warning for anyone revising this. Earlier versions justified α_Φ by resemblance to vanilla's
authored map, and then by band width. Both arguments were withdrawn, and neither should be
reintroduced — not because the figures were wrong, but because a hyperparameter chosen by taste does
not become better justified by finding a property that happens to hold at it.*"""))

patch_lib.apply(E)
