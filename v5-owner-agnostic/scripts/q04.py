# -*- coding: utf-8 -*-
"""v5 batch 4 — Group D (3.10) and Group E (wrong numbers), changes 25–35."""
import patch_lib
E = []

E.append(dict(id="D25-D29", clears="changes 25-29: the identity and per-good propagation",
section="3.10",
old="""This is an **identity, not a measurement**: `powershare_C(n)` carries no `g`, so it factors out of the sum, and by §1.1's vocabulary the property is true by construction and carries no measurement. What a run can show is only that the implementation does the algebra in doubles — on `gulf_of_siam`, with 13 goods carrying local value, 12 of them sinking there, transfer eligibility varying per good and the off-home penalty on two of the three collectors, the two forms agree to a worst relative disagreement of **1.3e-16**, one unit in the last place. So one scalar per node reproduces every country's income exactly, and the engine's own math does the rest. *(v1 through v3.0 quoted "agreement to 5.7e-14" here, and 1.4e-14 below. Both are floating-point residuals of an exact identity, produced by a construction none of those documents states — a theorem decorated with an experiment, which is the confusion §1.1 exists to prevent.)*""",
new="""This is an **identity, not a measurement**: `powershare_C(n)` carries no `g`, so it factors out of the sum, and by §1.1's vocabulary the property is true by construction and carries no measurement. Every term that feeds a collector's power at a node is node-wide — the merchant bonus, the off-home penalty, propagation off the one installed graph, the caravan grant — so none of them can reintroduce a `g`. What a run can show is only that the implementation does the algebra in doubles: across Sevilla, Genoa, Champagne, Malacca and the Gulf of Siam, using each node's real 1444 country table, the two forms agree to a worst relative disagreement of **0 to 3.7e-16** — at most one unit in the last place. So one scalar per node reproduces every country's income exactly, and the engine's own math does the rest. *(v1 through v4.0 quoted "agreement to 5.7e-14" here, and 1.4e-14 below. Both are floating-point residuals of an exact identity, produced by constructions none of those documents states — a theorem decorated with an experiment, which is the confusion §1.1 exists to prevent.)*"""))

E.append(dict(id="D26-D28", clears="changes 26-28: the per-good propagation magnitude and cause",
section="3.10",
old="""**This is also why propagation cannot be made per good.** Reading the one installed graph leaves the propagated term good-independent, so the identity survives it untouched — same construction, worst relative disagreement **1.3e-16**. Per-good propagation destroys it, because §1.9 reads a node's *downstream neighbours* and those are per good: `gulf_of_siam` has **eight distinct downstream sets across the 29 goods** — twelve goods leave it with none at all, five drain to `burma`, four to `{burma, canton, malacca}` — against `Φ_w`'s single `{canton}`. A country's power at the node stops being one number and `powershare_C` stops factoring out. Measured on the same construction: the node-scalar model then overstates **every** collector's income by **0.41%**, a total of 0.40 ducats on a node collecting 97.1. That is thirteen orders of magnitude above the float residual and it is a systematic bias in one direction, not rounding. Keeping propagation on a single graph is load-bearing for Goal 7, not merely convenient.""",
new="""**This is also why propagation cannot be made per good.** Reading the one installed graph leaves the propagated term good-independent, so the identity survives it untouched — same construction, worst relative disagreement 0 to 3.7e-16. Per-good propagation destroys it, because §1.9 reads a node's *downstream neighbours* and those differ per good. The driver is **not** how many distinct downstream sets a node has, but whether its collectors hold **differing power across the nodes those sets differ on**: `gulf_of_siam` has eight distinct downstream sets and still shows a 0.003% effect, because its collectors hold almost nothing in `burma`, `canton` or `malacca` and every propagation term is near zero. Where the collectors do hold differing power downstream, a country's power at the node stops being one number and `powershare_C` stops factoring out. Measured with each node's real 1444 country table and `collect_pool` built per good throughout: the error is **redistributive and single-digit percent, with the sign varying by collector** — Sevilla −0.82%, −0.87%, **+7.44%**; Champagne −1.69%, +1.69%, +1.53%; Genoa −0.23%, −0.22%, +0.70%. It is not a bias in one direction and it is not rounding: it is thirteen orders of magnitude above the float residual and it moves income between countries. Its size depends on which countries are collecting, which is a stated choice of the construction and not a property of the node, so no single percentage is quoted as one. Keeping propagation on a single graph is load-bearing for Goal 7, not merely convenient. *(v1 through v4.0 quoted "off by 5.96 ducats on a node paying ~250"; no node in the model has local trade value near 250 — the largest is 112.6 — and v4.0's own replacement figure, 0.41%, was an artifact of freezing one term at the alphabetically first commodity.)*"""))

E.append(dict(id="E30", clears="change 30: the caravan comparison", section="1.10",
old="""(median 17.9% over the 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`), against a largest single incumbent holder of 9.6 to 20.7 — so one country at the cap outweighs every incumbent in every inland node.""",
new="""(median 17.9% over the 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`), against a largest single incumbent holder of **23.6 to 143.2** — so a country at the cap outweighs the largest incumbent in **7 of the 26** inland nodes and is outweighed in the other 19. *(v4.0 read the save's `highest_power` field, 9.6–20.7, as the largest incumbent's power. It is not, and the conclusion drawn from it inverted.)*"""))

E.append(dict(id="E31", clears="change 31: the price-scan census", section="3.5",
old="""(All **154** `change_price` blocks were parsed — 93 in `events/`, 7 in `missions/`, 1 in `common/`
and **53 in `history/`, of which 13 are negative**, all in `history/countries/HAB - Austria.txt`.""",
new="""(All **161** `change_price` blocks were parsed — 93 in `events/`, 14 in `missions/`, 1 in `common/`
and **53 in `history/`, of which 13 are negative**, all in `history/countries/HAB - Austria.txt`.
v4.0 said 154 and 7: its parser silently recovered nothing from five mission files, which a bare
`except` hid, so the scan is now guarded by a per-file count assertion. The seven recovered blocks
are all positive and the partition is unchanged.""",
))

E.append(dict(id="E32", clears="change 32: the deterministic-field count", section="2.8",
old="""`retention` is identical on 80 of 80 nodes and `total` on 79 of 79, the exception drifting 0.012%""",
new="""`retention` is identical on 80 of 80 nodes and `total` on 78 of 79, the exception — `zambezi` —
drifting 0.012%"""))

E.append(dict(id="E34", clears="change 34: the solve-cost range", section="2.2",
old="""**5.7–7.3 ms per good and 0.17–0.21 s for all 29**. "Milliseconds each" therefore holds already,""",
new="""**0.17–0.21 s for all 29 goods, a mean of 5.7–7.3 ms per good across runs** — individual goods
range 5.4–24 ms, so 7.3 is an average and not a maximum. "Milliseconds each" therefore holds
already,"""))

E.append(dict(id="E35", clears="change 35: the ledger clause", section="1.7",
old="""trade efficiency and a flat income bonus are different quantities in EU4 — separate modifier keys with separate ledger columns (`LEDGER_TRADE_EFFICIENCY`, `LEDGER_TC_EFF_CARAVAN_POWER`), granted separately where both appear together — and the define's own comment says income.*""",
new="""trade efficiency and a flat income bonus are different quantities in EU4, and the define's own shipped comment settles which this one is: `TRADE_MERCHANT_PRESENT = 0.1,  -- bonus on income if trade present`.*"""))

patch_lib.apply(E)
