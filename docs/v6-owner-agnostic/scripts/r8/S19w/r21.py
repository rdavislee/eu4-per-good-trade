# -*- coding: utf-8 -*-
"""v6 batch 21 — the pre-confirmed round-2 fix set. Every number here was computed by an independent
agent from the install, the save or the solver before being written; four of my proposed values were
wrong and carry the corrected figure."""
import patch_lib
E = []

# ---- N01, M-a: the field now reads the goods the engine rolled -----------------------------------
E.append(dict(id="N01", clears="world wealth on the rolled-goods field", section="2.2",
old="""   `c` with per-province α, and the per-good balance `b = s − c`.""",
new="""   `c` with per-province α, and the per-good balance `b = s − c`. World wealth is **10,607.40**
   annual ducats over **2,472** counted provinces."""))

E.append(dict(id="N01b", clears="the old world-wealth sentence", section="2.2",
old="""`GP_COEFF` is **read from**
   `common/static_modifiers/00_static_modifiers.txt` rather than hardcoded (§2.3). World wealth is
   **10,594.70** annual ducats over **2,472** counted provinces. Then per-node `trade_value`, `s`,""",
new="""`GP_COEFF` is **read from**
   `common/static_modifiers/00_static_modifiers.txt` rather than hardcoded (§2.3). Then per-node
   `trade_value`, `s`,"""))

E.append(dict(id="M-a", clears="the twenty unknown-good provinces are read, not zeroed", section="1.3",
old="""**Twenty counted provinces have no trade good in their history file** (`trade_goods = unknown`); the
engine assigns one at start from each good's `chance = { }` block. The wealth field is therefore
partly the result of one random draw. The model does not try to predict the draw: it reads whatever
the game's current state holds, which is what it does for development too.""",
new="""**Twenty counted provinces have no trade good in their history file** (`trade_goods = unknown`); the
engine assigns one at start from each good's `chance = { }` block. The model does not predict the
draw — it **reads the good the engine actually rolled**, which is what it does for development too,
and prices the province on that. Pricing them at zero instead understates world wealth by 12.70
ducats. The draw is real, so the field is one sample: on this save the twenty came up seven `fur`,
five `grain`, three `wool`, two `livestock`, and one each of `cotton`, `incense` and
`naval_supplies`. A different roll gives a slightly different field, and nothing in the model depends
on which one."""))

# ---- N03: 89, not 88 -- and the reason is M-a itself --------------------------------------------
E.append(dict(id="N03", clears="the deleted apparatus, counted on the rolled-goods field", section="1.3",
old="""On the 1444 start that whole apparatus was worth **0.98%** of world wealth over 87 of
2,472 provinces (`measure6.py`),""",
new="""On the 1444 start that whole apparatus was worth **0.98%** of world wealth over **89** of the 2,472
counted provinces — 43 `gems` plus 31 `incense` plus 16 great-project and permanent-modifier
provinces, less one that is both (province 542). *The count depends on the field: it is 87 under the
withdrawn `is_city` filter, and 89 rather than 88 because province 4856 is one of the twenty whose
good the engine rolls, and it rolled `incense`.*"""))

# ---- N04-N09: figures the field moved -----------------------------------------------------------
E.append(dict(id="N04", clears="largest |b_w|", section="1.6",
old="""largest `|b_w|` **0.0226**;""", new="""largest `|b_w|` **0.0225**;"""))

E.append(dict(id="N04b", clears="the scale note's |b_w|", section="1.6",
old="""(its largest magnitude is 0.0226)""", new="""(its largest magnitude is 0.0225)"""))

E.append(dict(id="N05", clears="sinks per good, 1.1", section="1.1",
old="""  goods, 1–8 sinks per good, mean 3.52, zero fallbacks.""",
new="""  goods, 1–8 sinks per good, mean 3.72, zero fallbacks."""))

E.append(dict(id="N05b", clears="sinks per good, 1.6", section="1.6",
old="""Per good, on the same field: **1–8 sinks, mean 3.52**,""",
new="""Per good, on the same field: **1–8 sinks, mean 3.72**,"""))

E.append(dict(id="N06", clears="self-coherence", section="1.6",
old="""Agreement with the per-good graphs is **53.5%** of edge-goods (**52.1%** value-weighted).""",
new="""Agreement with the per-good graphs is **53.6%** of edge-goods (**52.3%** value-weighted)."""))

E.append(dict(id="N06b", clears="2.8's copy of the agreement figures", section="2.8",
old="""  baseline is known — `Φ_w` agrees with the per-good graphs on **52.1%** of edge-goods *weighted by
  trade value*, and on 53.5% unweighted (§1.6) —""",
new="""  baseline is known — `Φ_w` agrees with the per-good graphs on **52.3%** of edge-goods *weighted by
  trade value*, and on 53.6% unweighted (§1.6) —"""))

E.append(dict(id="N08", clears="connectivity", section="3.8",
old="""would cover most of the map — measured, **90.2%** (5,703 of 6,320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN.""",
new="""would cover most of the map — measured, **89.6%** (5,663 of 6,320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN."""))

E.append(dict(id="N08b", clears="the argument-unaffected clause", section="3.8",
old="""The argument is unaffected — 90.2% is still most of the map""",
new="""The argument is unaffected — 89.6% is still most of the map"""))

E.append(dict(id="N09", clears="the widest alpha band", section="1.6",
old="""scanned over [1, 8] rather than [1, 3], the widest band is **1.70** wide ([3.51, 5.21],""",
new="""scanned over [1, 8] rather than [1, 3], the widest band is **1.71** wide ([3.50, 5.21],"""))

# ---- N10, N11, M-b: the coal counterfactual -----------------------------------------------------
E.append(dict(id="N10", clears="the coal activation, holding devastation fixed", section="1.5",
old="""latent-coal provinces that are owned at 1444 — §1.3 counts only owned provinces — flips **13 of
159 `Φ_w` edges** and adds 217 ducats to world wealth (`measure6.py`).""",
new="""latent-coal provinces that are owned at 1444 — §1.3 counts only owned provinces — flips **10 of
159 `Φ_w` edges** and adds 214.60 ducats to world wealth (`measure6.py`). *The counterfactual holds
every non-repriced input fixed, which matters by more than rounding: province 4237 is both
latent-coal and one of the devastated eleven, and a reprice that drops its devastation measures coal
activating **plus** one province healing — worth 2.40 ducats and 3 extra flips.*"""))

# ---- N12, N13: the caravan medians -------------------------------------------------------------
E.append(dict(id="N12", clears="the caravan medians, both bases", section="1.10",
old="""Measured on the 1444 start: the cap of 50 is **9.4% to 47.0% of an inland node's total trade power**, median **21.9%** over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. *(As a share of the node's total **after** the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, median 17.9%; v5.0 quoted those under the first description, which cannot be right, since 8.6% of 532.0 is 45.8 rather than 50. §2.2 derives inland from `members` and gets 25 nodes, dropping `siberia`; on that basis only the median moves, to 21.3%.)*""",
new="""Measured on the 1444 start: the cap of 50 is **9.4% to 47.0% of an inland node's total trade power**, median **21.6%** over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. *(As a share of the node's total **after** the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, median 17.7%; v5.0 quoted those under the first description, which cannot be right, since 8.6% of 532.0 is 45.8 rather than 50. §2.2 derives inland from `members` and gets 25 nodes, dropping `siberia`; on that basis the median is 21.3%, or 17.5% after the grant.)*"""))

# ---- N14: development range ---------------------------------------------------------------------
E.append(dict(id="N14", clears="the development range at 1444", section="1.3",
old="""provinces at `base_tax` 2 and 6, are what `TAX_COEFF = 1.0` rests on, and the development range runs
past 50.*""",
new="""provinces at `base_tax` 2 and 6, are what `TAX_COEFF = 1.0` rests on, and `base_tax` at 1444 runs up
to 33.*"""))

patch_lib.apply(E)
