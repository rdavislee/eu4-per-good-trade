# -*- coding: utf-8 -*-
"""v6.1 batch H -- 2.8's Razed China row, and the remaining degeneracy references in 3.2 and 1.5/1.6."""
import patch_lib
E = []

E.append(dict(id="H1", clears="H1: 2.8's Razed China row, re-measured", section="2.8",
old="""| Razed China | *This row is ordering-robust where §1.6's sink membership is not: it turns on `hangzhou` holding an end, which it does in about 98% of relabellings (§1.6) — and on the razed field itself `hangzhou` loses its end in every relabelling tried, which is what the row asserts.* Zeroing `hangzhou`-node development relocates an end in one solve — measured: the `Φ_w` sinks move from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`, 22 of 159 edges flipping. `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth 226.7 against 143.0, and it holds the richest single province the model counts. Zeroing `beijing` **also** moves the map — 15 flips — because deleting a percent of world wealth renormalises `c_w` everywhere; what separates the two is that `hangzhou` **survives as a sink** when `beijing` is zeroed and does not when `hangzhou` is. *(v2 through v4.0 said zeroing `beijing` "moves nothing". It does; the asymmetry is which node keeps its end, not whether the map moves.)* |""",
new="""| Razed China | Zeroing `hangzhou`-node development relocates an end in one solve — measured: the `Φ_w` sinks move from `{genua, hangzhou}` to `{genua, gulf_of_siam}`, 30 of 159 edges flipping. `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth 226.7 against 143.0 — ranks 12 and 39 of the 79 nodes holding counted provinces — and it holds the richest single province the model counts. Zeroing `beijing` **also** moves the map — 8 flips — because deleting a percent of world wealth renormalises `c_w` everywhere; what separates the two is that `hangzhou` **survives as a sink** when `beijing` is zeroed and does not when `hangzhou` is. *(v2 through v4.0 said zeroing `beijing` "moves nothing". It does; the asymmetry is which node keeps its end, not whether the map moves.)* *On the razed field the result is order-invariant like the baseline: 40 of 40 relabellings return `{genua, gulf_of_siam}` and `hangzhou` holds an end in none of them. v6.0 had to argue this row was robust where the baseline sink set was not; §2.3's tie-break removes the distinction.* |"""))

E.append(dict(id="H2", clears="H2: 3.2's reference to the degeneracy as a live defect", section="3.2",
old="""   comes from Phase 2's degenerate LP, which moves the orientation under relabelling even when no key""",
new="""   came from Phase 2's LP under unit costs, which moved the orientation under relabelling even when no key"""))

# Two backward references to the former alpha, added in this pass. R3: do not maintain a figure for a
# value the model does not use. The comparison adds nothing the sensitivity note does not carry.
E.append(dict(id="H3", clears="H3: drop the former-alpha comparison in 1.5", section="1.5",
old="""2.40 ducats. On this field that mix moves no additional edge, where at α_Φ = 1.5 it moved three; the
reason to hold the input fixed is that the wealth figure is wrong either way, not that the edge count
always notices.*""",
new="""2.40 ducats. On this field that mix moves no additional edge, so the reason to hold the input fixed is
that the wealth figure is wrong either way, not that the edge count reliably notices.*"""))

E.append(dict(id="H4", clears="H4: drop the former-alpha comparison in 1.6", section="1.6",
old="""mean degree **2.4** against the map's 4.0. *(v2 called them "cul-de-sacs"; at this α their degrees
are closer to that reading than at α_Φ = 1.5, where the mean was 3.1 — but it is a description of
five nodes, not a property of the operator.)*""",
new="""mean degree **2.4** against the map's 4.0. *(v2 called them "cul-de-sacs"; the degrees are not far
off that reading here, but it is a description of five nodes on one field, not a property of the
operator.)*"""))

patch_lib.apply(E)
