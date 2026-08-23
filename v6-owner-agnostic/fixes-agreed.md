# v6.0 implementation checklist — agreed fixes, pre-confirmed

> **FROZEN AT v6.0.** This file records what v6.0 changed relative to v5.0 and is not maintained
> against later versions. Figures in it were correct when written and are not re-measured; where a
> later version moves one, the spec is the live document and this is the history. Neither harness
> targets it by default -- both refuse an unnamed target -- so a stale figure here cannot be
> mistaken for a current one by a green run.

**What this is.** The complete, authoritative list of changes v6.0 makes to v5.0. Negotiated with the
no-context validation agent that produced `../v5-owner-agnostic/validation-v5.md` (134 CONFIRMED /
39 PARTIAL / 22 REFUTED / 1 UNVERIFIABLE over X001–X196), then pre-confirmed by recomputation before
any edit was applied. **Every one of the 62 graded-open claims is mapped to an action in the table at
the end, and that mapping is generated from the validation file itself, so nothing can be silently
dropped.**

**Pre-confirmation.** Every replacement number below was computed on the **option-(c) wealth field**
before being written, by `measure6.py`, which reads the option-(c) `solver.py` directly. Numbers measured on v5.0's field were *not*
carried over; where (c) moves a figure, the (c) value is the one recorded here. Full record in
`../v5-owner-agnostic/preconfirmation.md`.

---

## 0. The three standing rules for v6.0

**R1 — the wealth model is option (c).**

```
wealth(p) = TAX_COEFF · base_tax(p) · (1 + province-state tax modifiers)
          + GP_COEFF · base_production(p) · (1 + province-state goods modifiers) · price(good(p))
```

Deleted: the two-test classification rule and its table, `gems` +15% tax, `incense` +10% trade
value, the six great projects, the ten permanent province modifiers, the Leviathan gate, the
`starting_tier` question, buildings, centres of trade, `production_leader`, and the whole-install
sweep. Kept: `devastation`, `occupied`, `under_siege`, `prosperity` — province state, and the
mechanism by which the map answers to war. `GP_COEFF = 0.2` is **read** from
`common/static_modifiers/00_static_modifiers.txt` (`provincial_production_size`, localised "Base
Production"), not hardcoded; `TAX_COEFF = 1.0` is not in that file and stays a measured constant.

**R2 — no empirical absolutes.** No superlative, no universal quantifier, and no threshold asserted
as a fact about the world. Every such statement becomes either a **directional design claim** (which
still fails if the mechanism fails) or an **explicitly scoped observation** naming its script and its
field. This is the single change that addresses the audit's own systemic finding — *"quantifier
strength, not provenance, is where this document breaks"* — and it is why most of the 39 partials
resolve by the claim saying less. Definitional and proved universals ("the flow subgraph is acyclic,
so a candidate always exists") are unaffected; the rule targets claims about measurements.

**R3 — no live figures for rejected operators.** `Φ_ord`, the 3-mass gravity kernel and the v1
Laplacian are superseded. They keep their graveyard entries and lose every maintained number, because
those numbers cost refutations on recount and buy one comparison sentence each. Pre-confirmed
footprint: **6 sites** — §1.6 l.375, §3.9 l.1172–1178, §3.2 l.950, §3.15 l.1338, l.1391–1394,
l.1400–1403. `Φ_ord` itself appears 7 times; 5 are historical notes that stay.

---

## 1. The (c) field at 1444 — pre-confirmed baseline

| quantity | v5.0 | **(c)** |
|---|---|---|
| world wealth | 10,677.50 | **10,594.70** over **2,472** counted provinces (the `is_city` fix adds 20) |
| `Φ_w` sinks | `hangzhou` | **`english_channel`, `hangzhou`** |
| their `c_w` / node-wealth ranks | 1 / 10 | **2 / 1** and **3 / 12** |
| Phase 1 selects | `hangzhou` | **`genua`**; both sinks by promotion, 2 promotions, 0 fallbacks |
| sources | 7 | **8**, `c_w` ranks **44–75**, mean degree **3.1** against the map's 4.0 |
| largest \|b_w\| | 0.0227 | **0.0226** |
| richest single province | 1821 @ 30.40 | **1821 @ 27.00** |
| `Φ_w` self-coherence | 52.5% / 51.5% | **53.5%** edge-goods, **52.1%** value-weighted |
| sinks per good | 1–7, mean 3.6 | **1–8, mean 3.52** |
| acyclic / fallbacks fired | 29/29 / 0 | **29/29 / 0** |
| ordered pairs connected by ≥1 good | 92.2% | **90.2%** (5,703 of 6,320) |
| supply / demand contrast | 4–97 / 211–20,400 | **4–97** over the 28 multi-producer goods / **211–15,010** |
| devastation's cost at 1444 | not modelled | **13.40 ducats** over **eleven** counted provinces |

**The (c) field reproduces v2.0's original §1.6 block almost exactly** — `genua` selected, both sinks
promoted, 8 sources, `c_w` 44–75, degree 3.1, \|b_w\| 0.0226. v2 measured a field with no modifier
sweep, which is where (c) returns. v5.0's rewrite of §1.6 was tracking a field (c) discards.

## 2. Three claims change meaning under (c), not just value

**P1 — `english_channel` is a sink at 1444 with no European growth at all.** §1.6's Europe
demonstration was built to prove Europe *can* hold a sink; under (c) it holds one at the start date.
Per **R2** the section is rewritten as a directional claim: *Europe becomes the centre of trade as it
develops* — at 1444 the map already ends in the Channel and in Hangzhou, and as European development
compounds the Channel's basin grows while Asia's pole fades. The measurements become scoped
observations (`europe.py`, on the 1444 field): ×1.02 → `{english_channel, hangzhou, wien}`;
×1.56 → `{english_channel, rheinland}`; ×2.00 → `{genua}`. **Pre-confirmed.** No threshold is
asserted as a constant of the model.

**P2 — the Lowlands result is vacuous and is deleted.** "Lowlands ×1.20 makes `english_channel` a
sink" is trivially true when it already is one. Pre-confirmed: ×1.20 and ×10 both return the baseline
set `{english_channel, hangzhou}`.

**P3 — `α_Φ = 1.5`'s band is [1.38, 1.63], width 0.25**, giving `{english_channel, hangzhou}`; the
widest band on [1, 8] is **1.70** wide ([3.51, 5.21], `{doab, genua, hangzhou}`). The "widest band" justification is
false on (c) as well, by a different margin — which confirms **A1** as the only defensible option on
either field.

## 3. B2 — the randomised trade goods, resolved

**20** counted provinces carry `trade_goods = unknown` in `history/provinces/` and are assigned a good by
the engine at start from each good's `chance = { }` block. **No modelling of the modal roll.** The
field is read from the game's current state at runtime and world wealth moves constantly in play, so
the 1444 snapshot is one draw and is stated as one. What survives from B2 is only the mechanism
defect underneath it, which is **M1**: the model must read the start state the engine produces, not
the history files alone.

---

## 4. The substantive fixes

**A1 — `α_Φ = 1.5` becomes a stipulation.** Its "widest band" justification is false on both fields
(pre-confirmed §2 P3). The agent tested and refuted the replacement I proposed: sink-set
noise-stability is 8/8 seeds at *every* α on *both* fields, so it selects everything, and it
contradicts §1.6's own finding that the sink set is not the quantity to watch under perturbation.
Orientation flip count discriminates (0 flips at α ∈ {1.2, 1.5}) but selects a range whose low end
gives five sinks. **Resolution:** own 1.5 as a design constant exactly as `P₀ = 2.0` is owned, with
the band table as a record of what other values give. **Written warning against re-justifying it by
the two-sink map** — that is V213, the calibration §2.3 withdrew, returning through the back door,
and under (c) the two-sink map is back and the temptation is live.

**M1 — the model misreads the 1444 start state.** The start state is `history/provinces/` **plus
`on_startup`**. Chain pre-confirmed: `common/on_actions/00_on_actions.txt:33` →
`common/scripted_effects/01_scripted_effects_for_on_actions.txt:4795` → `events/flavorBOH.txt`
`flavor_boh.15` → `add_devastation`. Three fixes, all in the solver:

| | defect | pre-confirmed |
|---|---|---|
| M1a | ten provinces carry devastation 20–50; §1.3 says all are zero at 1444 | costs **13.40 ducats**; `devastation` grants `trade_goods_size_modifier = -2`, scaled by level/100 |
| M1b | `add_base_tax` in a dated block before the start date is not applied | province 1 (Uppland) `base_tax` 5 → **6**, one province, 1.00 ducat |
| M1c | an `is_city = yes` filter the engine does not apply drops owned provinces | **20 provinces**, including 265 — which is also devastated, so M1a and M1c interact — and Brno, whose file has the line commented out. Counted provinces 2,452 → **2,472** |

**H1 — Phase 2's LP is degenerate, so the orientation is not a function of the world state alone.**
Pre-confirmed two ways: the sub-audit permuted node labels end-to-end (29 goods × 20 relabellings =
580 runs) and the orientation changed on **580 of 580**, always via a *different optimal LP vertex*
and never via a sweep tiebreak, mean **22.1 of 159 edges** moving with the objective identical to
8.9e-16; and independently, permuting only the arc presentation order into `linprog` with node labels
fixed changes the optimal support on **10 of 10 goods tested**, objective gaps ≤ 1.8e-15. Four
consequences, all written: §2.4's canonical-order requirement is right but its stated reason (the
fallback branch, which never fires on 1444) is wrong — it is **Phase 2's input order**; 22 flips is
the magnitude §2.8 treats as a major world event; every stability figure is restated as **"at fixed
node order"**; and §3.13's cross-machine determinism is a same-machine concern. Recorded as
HiGHS-specific in detail but not in kind — any simplex picks a vertex of a degenerate optimal face.
A tie-breaking objective would fix it and is **not** proposed here.

**D1 — §3.10's magnitude claim is restated as exactness, not materiality.** The nine per-collector
percentages are artifacts of freezing the powershare at one reference commodity; sweeping the
reference moves Sevilla's MOR from −9.84% to +7.93%. With the **value-weighted mean powershare** —
the scalar a real implementation would store — the error is **≤ 0.1% at all five nodes**
(pre-confirmed: sevilla −0.01/−0.01/+0.10, champagne ~0, genua −0.01/−0.00/+0.01, malacca
+0.01/−0.01/−0.00, gulf_of_siam ~0). So per-good propagation breaks **exactness**, not materiality,
and the magnitude is a property of the substituted scalar. The identity on a single graph
(0 to 3.7e-16) is untouched. Same defect class as v4.0's 0.41%, which v5.0 diagnosed and then
re-committed with a different arbitrary choice.

**C1 — the price census is 151 executable of 161 textual blocks.** Ten never execute: **seven** in
quoted `effect_tooltip = "…"` / `country_event_with_effect_insight` `effect = "…"` strings, **three**
in `tooltip = { }` wrappers (`WOC_Hisn_Kayfa:1448`, `:1459`, `events/flavorMAL.txt:1736`). `pdx.py`
swallows quoted strings but parses `tooltip = { }`, which is why v4.0 got 154 and v5.0 got 161 and
both were wrong. Six of the seven duplicate an `events/` block; the seventh names a price key no
event sets. **The 13/2/4/11 partition is unmoved** — all ten are positive, all 40 negatives are
executable.

**C2 — delete the claim of a guard that does not exist, then build it.** §3.5 says the scan is
"guarded by a per-file count assertion". **`validate_v5.py` contains zero `assert` statements.** The
document told a reader something was checked when nothing checked it — the most serious error class
in the audit. Also delete the stated mechanism: no exception ever fires; `pdx.TOK`'s `"[^"]*"`
alternative collapses a quoted tooltip into one token.

**C3 — `change_price` values are fractions of base price.** Pre-confirmed from shipped save state
(`tutorial/eu4_tutorial_chapter10.eu4`): `paper` `current_price=4.375` on base 3.5 (**× 1.25**), and
`gems` `5.000` on base 4.0. The spec never says this, so "−0.25 for 2.5 → 1.875" reads as an error.

**F1 — the harness is rebuilt, not patched.** Of 133 assertion sites: 51 text-presence, 66
self-confirming numeric, 13 genuine re-derivations, 5 tautological. **82 of the 83 numeric checks
never open the spec**, so nothing compared a figure *printed in the document* to one *computed from
the game*; a mutation test planting ten factual errors caught **one**, and world wealth altered to
12,345.67 passed while the same run printed `got=10677.5 exp=10677.5`. **v6's harness parses each
figure out of the spec text and compares it to a computed value, and its acceptance criterion is the
mutation test — ≥ 9 of 10 planted errors caught — not the pass count.** Also fix the README, which
credits the modifier sweep to `wealthmodel.py` when the numbers lived only in `q01.py`, the patch
script that typed them in.

**E-series — precision corrections, all pre-confirmed.** Caravan cap **9.4–47.0%, median 21.9%** of
the node's total (8.6–32.0% is the share *after* the grant, and 8.6% of 532.0 is 45.8, not 50);
`highest_power` is the **strongest single province's** power (matches `max(country province_power)` on
17 of 79 nodes, strictly less on 62); `gulf_of_siam` has **7** downstream sets and the small effect
is **near-proportionality** (shares 0.3724 at the node, 0.3725 at `burma`) not small holdings;
3.69e-16 is **1.7–3.3 ULP**; the float-to-effect gap spans **11.3–14.3** orders; solve cost is quoted
as an **order of magnitude** (12 runs gave 0.088–0.181 s against a stated 0.17–0.21); the three
shipped cooldowns are named (`TRADING_POLICY_COOLDOWN_MONTHS = 12`,
`TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30`, `TRADE_COMPANY_COOLDOWN = 60`); the Cape is a live conduit
(in-degree 1, out-degree 3, **132 ordered pairs**) with no Europe→sink route through it; supply
contrast is **4–97 over the 28 multi-producer goods**, `cloves` having one producer and no contrast
to measure; 22-node sole-`genua` at **×1.65** and 18-node at **×2.15** on (c); the Cape reverses on a
**single** contiguous run **[2.88, 3.45]** on (c); spice-sink thresholds **3.61 / 4.12 / 4.60 / 4.77**.

**ARG-series — derivations, confirmed by argument not measurement.** The fallback branch fires only
when every candidate is support-isolated with zero **post-peel** balance, and the aggregate case
needs uniform `Σ wealth^α_Φ` per node rather than uniform wealth; T3's candidates carry wealths
**3, 2, 1**, so "the wealth key ties" is false of the spec's own worked example and the branch's
index dependence must be stated for the general tie rather than for T3; the sink-set equality's two
conditions are **necessary, not sufficient** — T2 satisfies both and still breaks it; and §1.1
documents **two** index tiebreaks where there are **four** (Phase 1's cluster argmin, the stall
promotion's identical form, and the top-k cut's equal-mass enumeration order are undocumented), with
none of them biting on 1444.

---

## 5. Every graded-open claim, mapped

62 items. Codes: **MOOT** subject deleted by (c) · **DROP** rejected-operator figure deleted ·
**SOFT** absolute → scoped or directional (R2) · **VALUE** replacement number pre-confirmed ·
**ARG** confirmed by argument · **GAME** needs a running game, stated as one observation ·
**MECH** solver/emitter fix.

| ID | was | action | note |
|---|---|---|---|
| X004 | REFU | **SOFT** | 'no figure is unverified' -> per-section attribution, and three declines not one |
| X008 | PART | **ARG** | fallback-branch derivations: post-peel balance, uniform Σwealth^α, T3's own wealths |
| X009 | REFU | **ARG** | fallback-branch derivations: post-peel balance, uniform Σwealth^α, T3's own wealths |
| X010 | PART | **ARG** | fallback-branch derivations: post-peel balance, uniform Σwealth^α, T3's own wealths |
| X011 | PART | **ARG** | fallback-branch derivations: post-peel balance, uniform Σwealth^α, T3's own wealths |
| X013 | PART | **ARG** | sink-set equality: conditions are necessary, not sufficient (T2 satisfies both) |
| X016 | PART | **ARG** | index-independence is a measurement on post-fold balances; four tiebreaks, not two |
| X018 | PART | **MECH** | §1.3's goods_produced form: flat bonuses inside the multiply (moot under (c), form kept) |
| X021 | REFU | **GAME** | one tooltip observation; arithmetic restated, reading not generalised |
| X022 | UNVE | **GAME** | one tooltip observation; arithmetic restated, reading not generalised |
| X027 | REFU | **GAME** | one tooltip observation; arithmetic restated, reading not generalised |
| X030 | PART | **MECH** | start-state reads: on_startup devastation, pre-start add_base_*, the is_city filter |
| X033 | PART | **SOFT** | 'the whole of the tension' scoped to the trade-good tables (also MOOT under (c)) |
| X035 | REFU | **MOOT** | §1.3's classification table and its whole apparatus are deleted under (c) |
| X040 | REFU | **MECH** | start-state reads: on_startup devastation, pre-start add_base_*, the is_city filter |
| X043 | PART | **MOOT** | §1.3's classification table and its whole apparatus are deleted under (c) |
| X045 | PART | **MOOT** | §1.3's classification table and its whole apparatus are deleted under (c) |
| X046 | PART | **MOOT** | §1.3's classification table and its whole apparatus are deleted under (c) |
| X047 | PART | **MOOT** | §1.3's classification table and its whole apparatus are deleted under (c) |
| X048 | PART | **MOOT** | §1.3's classification table and its whole apparatus are deleted under (c) |
| X050 | REFU | **MOOT** | §1.3's classification table and its whole apparatus are deleted under (c) |
| X055 | PART | **MOOT** | §1.3's classification table and its whole apparatus are deleted under (c) |
| X056 | PART | **MOOT** | §1.3's classification table and its whole apparatus are deleted under (c) |
| X058 | REFU | **MOOT** | §1.3's classification table and its whole apparatus are deleted under (c) |
| X059 | PART | **MOOT** | §1.3's classification table and its whole apparatus are deleted under (c) |
| X065 | REFU | **VALUE** | recomputed on the (c) field |
| X067 | PART | **SOFT** | world-responsiveness stated directionally, not as a count rule |
| X078 | PART | **VALUE** | recomputed on the (c) field |
| X083 | REFU | **VALUE** | recomputed on the (c) field |
| X086 | PART | **VALUE** | recomputed on the (c) field |
| X087 | PART | **VALUE** | recomputed on the (c) field |
| X091 | REFU | **MOOT** | wealth-scaling vs development-scaling: identical under (c), max diff 0.00e+00 |
| X097 | REFU | **SOFT** | universal narrowed to the routes actually checked |
| X099 | PART | **VALUE** | recomputed on the (c) field |
| X100 | REFU | **VALUE** | recomputed on the (c) field |
| X106 | PART | **VALUE** | re-measured from primary sources |
| X107 | REFU | **VALUE** | re-measured from primary sources |
| X112 | REFU | **MOOT** | §1.3's classification table and its whole apparatus are deleted under (c) |
| X114 | PART | **VALUE** | re-measured from primary sources |
| X117 | PART | **ARG** | index-independence is a measurement on post-fold balances; four tiebreaks, not two |
| X124 | PART | **VALUE** | the crash record: two launches in game-session.md, third from validation-v3 |
| X125 | REFU | **ARG** | fallback-branch derivations: post-peel balance, uniform Σwealth^α, T3's own wealths |
| X143 | PART | **VALUE** | recomputed on the (c) field |
| X145 | PART | **ARG** | sink-set equality: conditions are necessary, not sufficient (T2 satisfies both) |
| X151 | REFU | **ARG** | index-independence is a measurement on post-fold balances; four tiebreaks, not two |
| X154 | PART | **VALUE** | re-measured from primary sources |
| X155 | REFU | **VALUE** | re-measured from primary sources |
| X160 | PART | **DROP** | rejected-operator figure deleted; the comparison is stated qualitatively |
| X165 | PART | **VALUE** | §3.10's identity and error, recomputed with the value-weighted mean share |
| X166 | PART | **VALUE** | re-measured from primary sources |
| X169 | REFU | **VALUE** | re-measured from primary sources |
| X170 | PART | **ARG** | §3.10: exactness, not materiality; the construction is stated |
| X171 | PART | **VALUE** | re-measured from primary sources |
| X172 | PART | **ARG** | §3.10: exactness, not materiality; the construction is stated |
| X176 | REFU | **MOOT** | §1.3's classification table and its whole apparatus are deleted under (c) |
| X177 | PART | **GAME** | one tooltip observation; arithmetic restated, reading not generalised |
| X178 | PART | **GAME** | one tooltip observation; arithmetic restated, reading not generalised |
| X179 | PART | **MOOT** | §1.3's classification table and its whole apparatus are deleted under (c) |
| X185 | REFU | **VALUE** | re-measured from primary sources |
| X186 | PART | **DROP** | rejected-operator figure deleted; the comparison is stated qualitatively |
| X190 | PART | **DROP** | rejected-operator figure deleted; the comparison is stated qualitatively |
| X191 | REFU | **DROP** | rejected-operator figure deleted; the comparison is stated qualitatively |

**Counts by action:** MOOT 15, DROP 4, SOFT 4, VALUE 19, ARG 12, GAME 5, MECH 3.

## 7. The v6.0 figures, as measured

`scripts/measure6.py` prints 57 labelled figures from the option-(c) `solver.py` and writes them to
`scripts/measure6.out`. `scripts/verify6.py` reads the **document** and checks each number it prints
against that file — the F1 design, applied to this checklist as well as to the spec. Headline set:

| | |
|---|---|
| `GP_COEFF` (read from `static_modifiers`) / `TAX_COEFF` | 0.2 / 1.0 |
| counted provinces / world wealth | 2,472 / **10,594.70** |
| devastation, 11 provinces | **−13.40 ducats** |
| `Φ_w` sinks | `english_channel` (c_w 2, wealth 1), `hangzhou` (c_w 3, wealth 12) |
| Phase 1 / promotions / fallbacks | `genua` / 2 / 0 |
| sources | 8, c_w 44–75, degree 3.1 vs 4.0 |
| oriented / acyclic / largest \|b_w\| | 159/159 / yes / 0.0226 |
| per good | 1–8 sinks, mean 3.52, 29/29 acyclic, 0 fallbacks |
| self-coherence | 53.5% edge-goods, 52.1% value-weighted |
| ordered pairs connected | 5,703 of 6,320 (90.2%) |
| α_Φ = 1.5's band / widest band on [1,8] | [1.38, 1.63] w 0.25 / [3.51, 5.21] w 1.70 |
| sink count at α ∈ {1, 1.5, 2, 3, 4, 8} | 6, 2, 1, 2, 3, 1 |
| Europe (824 provinces) dev ×1.02 / ×1.56 / ×2.00 | +`wien` / `{english_channel, rheinland}` / `{genua}` |
| development-scaling vs wealth-scaling | identical, max difference **0.0** |
| ±1% wealth noise, 3 seeds | sink set unchanged |
| Cape | in-degree 1, out-degree 3, 132 ordered pairs, no Europe→sink route |
| `change_price` textual / partition | 161 (events 93, missions 14, common 1, history 53, decisions 0) / 13-2-4-11 |
| the three cooldown defines | 12 months / 30 days / 60 days |

Two figures moved from the pre-confirmation pass because M1b and M1c changed the field after it was
run: world wealth 10,559.60 → **10,594.70** and the Cape's routed pairs 115 → **132**. Both are
recorded here at their final values, which is the point of verifying the document mechanically rather
than trusting a number written by hand.

## 6. Out of scope

Nothing else changes. The 134 CONFIRMED claims are untouched except where option (c) deletes their
subject, which is itself listed above. The 39 partials are not individually re-argued beyond the
table: each narrows to what is proved or measured, which is what **R2** requires — and that is the
step where v4.0's errors were introduced, so **F1**'s rebuilt harness is applied to them as well.
