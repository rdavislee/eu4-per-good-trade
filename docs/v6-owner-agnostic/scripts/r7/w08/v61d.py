# -*- coding: utf-8 -*-
"""v6.1 batch D -- the 1444 geography, the Cape, coal activation, connectivity."""
import patch_lib
E = []

E.append(dict(id="D1", clears="D1: the 1444 routes, re-measured at the shipped config", section="1.6",
old="""**And the 1444 map draws the pre-Columbian trade geography unprompted.** The route from Genoa to
the Asian sink is the Silk Road: `genua → alexandria → aleppo → persia → lahore → lhasa →
ganges_delta → burma → gulf_of_siam → canton → hangzhou`. From the north it is the Volga:
`north_sea → white_sea → novgorod → kazan → astrakhan → persia → …`. **No route leaves
`english_channel` at all** — it is a sink, out-degree 0, so the Hansa and the Danube carry power
*into* it rather than out, and v5.0's "from the Channel it is the Hansa and the Danube" was
describing a path that does not exist. **No Europe→sink route passes the Cape of Good Hope** —
checked from `genua`, `north_sea` and `english_channel` — which is what a 1444 map should say.

The Cape is nonetheless a live conduit, not an idle one: in-degree 1, out-degree 3, with **132
ordered node pairs** whose path runs through it (`measure6.py`), carrying Atlantic drainage into the
Indian Ocean.
*(v5.0 said "nothing routes through the Cape", which is false as a universal and was only ever
checked on the Europe→sink routes.)* In the per-good graphs it also carries Asian spices to Europe;
`Φ_w` models power, not cargo (§3.9).""",
new="""**And the 1444 map draws the pre-Columbian trade geography unprompted.** Two long overland routes
reach the Asian end. From the north it is the Volga and the steppe:
`white_sea → novgorod → kazan → siberia → samarkand → lahore → lhasa → ganges_delta → burma →
gulf_of_siam → canton → hangzhou`. From Iberia it is the African coast and the Red Sea:
`sevilla → safi → timbuktu → katsina → ethiopia → gulf_of_aden → comorin_cape → ganges_delta → …`,
eleven hops. **No route leaves `genua` at all** — it is a sink, out-degree 0 against in-degree 5, so
the western Mediterranean, the Adriatic and the Rhône carry power *into* it. `english_channel` is
not an end at this α: it drains to `genua` in two hops through `champagne`, and reaches the Asian end
not at all.

**No Europe→sink route passes the Cape of Good Hope.** Checked exhaustively rather than sampled: of
the 23 European nodes there are **27** connected Europe→sink pairs, and for **0 of them** does a
Cape-transiting path exist. That is what a 1444 map should say, and it is the one place in this
section where a universal is asserted, because here the whole set was enumerated.

The Cape is nonetheless a live conduit, not an idle one: in-degree 2 (`zanzibar`, `ivory_coast`),
out-degree 2 (`comorin_cape`, `malacca`), with **81 ordered node pairs** for which a path through it
exists (`measure6.py` — the count is pairs `(a, b)` where `a` reaches the Cape, the Cape reaches `b`,
and `a` reaches `b`, not pairs whose shortest path happens to use it; the stricter shortest-path
reading gives 69 on the same field). It carries Atlantic drainage into the Indian Ocean. In the
per-good graphs it also carries Asian spices to Europe; `Φ_w` models power, not cargo (§3.9)."""))

E.append(dict(id="D2", clears="D2: coal activation flips, and the mixed counterfactual re-measured",
section="1.5",
old="""every graph in the model is entitled to move on it. Measured: repricing to coal the **45** of the
latent-coal provinces that are owned at 1444 — §1.3 counts only owned provinces — flips **10 of
159 `Φ_w` edges** and adds 214.60 ducats to world wealth (`measure6.py`). *The counterfactual holds
every non-repriced input fixed, which matters by more than rounding: province 4237 is both
latent-coal and one of the devastated eleven, and a reprice that drops its devastation measures coal
activating **plus** one province healing — worth 2.40 ducats and 3 extra flips.*""",
new="""every graph in the model is entitled to move on it. Measured: repricing to coal the **45** of the
latent-coal provinces that are owned at 1444 — §1.3 counts only owned provinces — flips **16 of
159 `Φ_w` edges** and adds 214.60 ducats to world wealth (`measure6.py`). *The counterfactual holds
every non-repriced input fixed. Province 4237 is both latent-coal and one of the devastated eleven, so
a reprice that drops its devastation measures coal activating **plus** one province healing — worth
2.40 ducats. On this field that mix moves no additional edge, where at α_Φ = 1.5 it moved three; the
reason to hold the input fixed is that the wealth figure is wrong either way, not that the edge count
always notices.*"""))

E.append(dict(id="D3", clears="D3: the survival-table coal row", section="1.10",
old="""Measured: repricing the 45 owned latent-coal provinces flips 10 of 159 `Φ_w` edges (§1.5) |""",
new="""Measured: repricing the 45 owned latent-coal provinces flips 16 of 159 `Φ_w` edges (§1.5) |"""))

E.append(dict(id="D4", clears="D4: any-good connectivity", section="3.13",
old="""measured, **89.6%** (5,663 of 6,320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. (v2 quoted 98.8%; that is v1's *Laplacian* figure, 6245/6320, carried across the operator change without being re-measured. The argument is unaffected — 89.6% is still most of the map — but the number was not v2's own.)""",
new="""measured, **90.5%** (5,721 of 6,320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. (v2 quoted 98.8%; that is v1's *Laplacian* figure, 6245/6320, carried across the operator change without being re-measured. The argument is unaffected — 90.5% is still most of the map — but the number was not v2's own.)"""))

patch_lib.apply(E)
