# -*- coding: utf-8 -*-
"""v5 batch 1 — Group A, the wealth field (changes 1–9)."""
import patch_lib
E = []

E.append(dict(id="version", clears="v5.0 banner", section="0",
old="""**Version:** 4.0""", new="""**Version:** 5.0"""))

E.append(dict(id="v5-header", clears="the fold-through claim", section="0",
old="""**v4.0** keeps v3.0's three changes and closes the audit of them. (a) **Wealth is owner-agnostic**
— a property of the place, not of who holds it: no autonomy, no production efficiency, no ideas, no
owner modifiers (§1.3, §3.3). (b) Every refuted and partial claim in `../v2-drain/validation-v2.md`
**and** `../v3-owner-agnostic/validation-v3.md` is folded through — including the five
`validation-v2.md` partials v3.0 counted in its ledger but did not fold (§1.6, §1.8, §1.10, §2.2)
and four v1 corrections that v2 never applied. (c) The four game probes settled in
`../v2-drain/game-session.md` are applied, two of them reversing v2's stated position (§2.4, §1.9).
Deleted text is quoted in `changes-v4.md`. Every measured number carries the script that produced
it; anything not regenerated for v4.0 is marked **[unverified in v4.0]**.""",
new="""**v5.0** keeps the owner-agnostic wealth of v3.0 — a property of the place, not of who holds it:
no autonomy, no production efficiency, no ideas, no owner modifiers (§1.3, §3.3) — and folds through
every refuted and partial claim from all four audits to date, including v4.0's own. Its substantive
change is to §1.3: **the local-modifier classification is applied to the whole install rather than
to the trade-good tables alone**, which adds sixteen provinces and moves the aggregate graph from
two 1444 sinks to one (§1.6). Deleted text is quoted in `changes-v5.md`. Every measured number
carries the script that produced it; **no figure in v5.0 is unverified**, and the one place the
document declines to project a number says so in place."""))

E.append(dict(id="A1-A7", clears="changes 1-7: the classification table", section="1.3",
old="""Applied to everything live on a 1444 province with no owner input:

| Modifier | Local? | Enters wealth? |
|---|---|---|
| `gems` `local_tax_modifier = 0.15` | yes, set by the province's good | **yes** — modifies `tax_value` |
| `incense` `trade_value_modifier = 0.1` | yes, set by the province's good | **yes** — modifies `trade_value` |
| `glass` `local_production_efficiency = 0.1` | yes, set by the province's good | no — modifies production *income*, which wealth does not compute |
| `chinaware` `local_autonomy = -0.1` | yes, set by the province's good | no — modifies local autonomy, which wealth does not compute |
| goods-produced efficiency from nearby merchant republics, trading cities and trade companies (`bonus_from_merchant_republics`, `eu4.exe:0x1cc7128`) | **no** — its value is set by which *neighbouring countries* hold those government forms | — |
| the owner's `global_trade_goods_size_modifier` (e.g. the `Industrious` ruler personality, +10%) | no — country-scoped | — |
| `terrain.txt` and the climate static modifiers | yes | no — they grant `allowed_num_of_buildings`, `defence`, `local_defensiveness`, `local_development_cost`, `movement_cost`, `nation_designer_cost_multiplier`, `supply_limit`, colonial growth and hostile attrition, none of which wealth computes |

So exactly **two** modifiers enter wealth in vanilla: `gems` on the tax term and `incense` on the
trade-value term. The reference solver applies both (§2.2 item 4). The two rows that are local but
do not enter — glass and chinaware — are the whole of the rule-versus-vocabulary tension: §1.3
excludes production efficiency and autonomy by name, and the second test excludes them again for the
same reason, so there is nothing left to decide.""",
new="""**The tests are applied to the whole install, not to one file.** v4.0 stated this rule and then
swept only `common/tradegoods/`, which is the mistake the rule exists to prevent: it concluded
"exactly two" and missed sixteen provinces. Applied to everything live on a 1444 province with no
owner input:

| Source | Local? | Enters wealth? |
|---|---|---|
| `gems` `local_tax_modifier = 0.15` (43 provinces) | yes, set by the province's good | **yes** — `tax_value` |
| `incense` `trade_value_modifier = 0.1` (29 provinces) | yes, set by the province's good | **yes** — `trade_value` |
| **Great-project `province_modifiers`** where `can_use_modifiers_trigger` is empty (6 provinces) | yes, the project is on the province | **yes** — `goods_produced` and `trade_value` |
| **`add_permanent_province_modifier` in the undated province-history block** (10 provinces) | yes, applied to the place at the start date | **yes** — `goods_produced` |
| `devastation` −2, `occupied` −0.5 and −0.5, `under_siege` −0.25, `prosperity` +0.25 (static modifiers) | yes, all are province state | **yes** — `goods_produced` and `tax_value`; all are zero at the 1444 start, and §1.2 and §3.3 both depend on them biting later |
| `glass` `local_production_efficiency = 0.1` | yes, set by the province's good | no — modifies production *income*, which wealth does not compute |
| `chinaware` `local_autonomy = -0.1` | yes, set by the province's good | no — modifies local autonomy, which wealth does not compute |
| **Centers of trade** (361 provinces carry one at 1444) | yes, CoT level is province state | no — no CoT level in `common/centers_of_trade/` grants any of the four keys wealth reads. A clean near-miss, recorded so it is not reopened |
| `production_leader` `trade_goods_size_modifier = 0.10` | **no** — which country leads a good's production is a country's state | — |
| goods-produced efficiency from nearby merchant republics, trading cities and trade companies (`bonus_from_merchant_republics`, `eu4.exe:0x1cc7128`) | **no** — set by which *neighbouring countries* hold those government forms | — |
| the owner's `global_trade_goods_size_modifier` (e.g. the `Industrious` ruler personality, +10%) | no — country-scoped | — |
| Buildings | yes by the test, and empty at 1444 — no province's start state carries a temple, workshop or manufactory | would be, if any existed |
| `terrain.txt` and the climate static modifiers | yes | no — they grant `allowed_num_of_buildings`, `defence`, `local_defensiveness`, `local_development_cost`, `movement_cost`, `nation_designer_cost_multiplier`, `supply_limit`, colonial growth and hostile attrition, none of which wealth computes |

**Great projects, in scope.** A project contributes the `province_modifiers` accumulated up to its
`starting_tier` when its `can_use_modifiers_trigger` is empty. Tiers reached after the start date
are owner spending and are out; so is any project whose trigger tests a country's culture, religion,
government or flags — 85 of the 130 live at 1444 are gated that way. That leaves six carrying a key
wealth reads: `falun_copper_mine` (province 8, `trade_goods_size` 3.0), `krakow_cloth_hall` (262,
`trade_goods_size_modifier` 0.10) and the four Grand Canal provinces (684, 1821, 1822, 2145;
`trade_goods_size` 0.5 and `trade_value_modifier` 0.1 each). Province 1821 is the richest single
province in the game. *The tier is the right line and "owner action" is not: development is an owner
action, so a rule excluding those would exclude `base_production`, which is wealth's primary input.*

**The ten permanent modifiers** are `granary_of_the_mediterranean` (362, 363, 2316, 4316),
`skanemarket` (6), `icelanding_fisher_sea` (370, 371), `diamond_mines_of_golconda_modifier` (542),
`jingdezhen_kilns` (2151) and `coffea_arabica_modifier` (387), all flat `trade_goods_size`.

**These figures are conditional on the DLC set.** `province_triggered_modifiers`'
`stora_kopparberget_modifier` is gated `NOT = { has_dlc = "Leviathan" }` and grants
`trade_goods_size = 5.0` on province 8 — the same province as `falun_copper_mine`. With Leviathan
the project applies and gives 3.0; without it the project does not exist and the modifier gives 5.0.
Every wealth figure in this document was measured with **Leviathan installed**, which is why §2.3
makes DLC state a third input axis rather than a footnote.

The two rows that are local but do not enter — glass and chinaware — are the whole of the
rule-versus-vocabulary tension: §1.3 excludes production efficiency and autonomy by name, and the
second test excludes them again for the same reason, so there is nothing left to decide."""))

E.append(dict(id="A3", clears="change 3: the flat-bonus denial", section="1.3",
old="""**consistent with** that and does not establish it — it carries an additive `Base Goods Produced`
block (`Base Production: +0.80`) above a separate multiplicative `Goods Produced Efficiency` block,
and no 1444 province was observed carrying a flat bonus in the first block (§3.13).""",
new="""**consistent with** that and does not establish it — it carries an additive `Base Goods Produced`
block (`Base Production: +0.80`) above a separate multiplicative `Goods Produced Efficiency` block.
Fifteen 1444 provinces do carry a flat bonus in the first block (the table above), so the ordering
matters in practice and not only in principle."""))

E.append(dict(id="A8", clears="change 8-9: solver item 4", section="2.2",
old="""4. Per-province `wealth` — **owner-agnostic** per §1.3:
   `TAX_COEFF · base_tax · (1 + local tax modifiers) + GP_COEFF · base_production · price ·
   (1 + local trade-value modifiers)`, and no autonomy, efficiency, ideas or owner terms. In vanilla
   the local modifiers that enter are exactly two — `gems` (+15% tax, 43 provinces) and `incense`
   (+10% trade value, 29 provinces) — and the reference solver applies both; v3.0 specified them and
   computed without them. Then per-node `trade_value`, `s`, `c` with per-province α, and the
   per-good balance `b = s − c`.""",
new="""4. Per-province `wealth` — **owner-agnostic** per §1.3:
   `TAX_COEFF · base_tax · (1 + local tax modifiers) + (GP_COEFF · base_production + local flat
   goods bonuses) · (1 + local goods-produced modifiers) · price · (1 + local trade-value
   modifiers)`, and no autonomy, efficiency, ideas or owner terms. The solver reads the local
   modifiers from §1.3's classification, applied to the whole install: in vanilla at 1444 that is
   `gems` (+15% tax, 43 provinces), `incense` (+10% trade value, 29 provinces), six great projects
   and ten permanent province modifiers — 16 provinces beyond the two trade goods. World wealth is
   **10,677.50** annual ducats over 2,452 counted provinces. Then per-node `trade_value`, `s`, `c`
   with per-province α, and the per-good balance `b = s − c`."""))

patch_lib.apply(E)
