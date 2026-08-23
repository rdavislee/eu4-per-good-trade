# Claim Inventory Delta — Per-Good Trade Network Spec v5.0

Extracted from `per-good-trade-spec.md` (v5.0) as a **delta against `../v3-owner-agnostic/claims-v3.md`**
(W001–W195, itself a delta against `../v2-drain/claims-v2.md`, V001–V230, itself a delta against
`../v1-laplacian/claims.md`, C001–C685). Extraction only: nothing here is validated, corrected, or
commented on.

**Method.** Four documents were read in full: the v5.0 spec (1,477 lines), `claims-v3.md` (all 217
claim rows plus its header conventions), the v4.0 spec, and `changes-v5.md`. Because **v4.0 never
had a claims file**, the v4.0 spec was diffed against the v3.0 spec line-by-line to separate
propositions that arrived in v4.0 from those that arrived in v5.0; `changes-v5.md` was used only to
locate the 55 changed passages, and every row below was extracted from the spec text itself.
`claims-v2.md` and `claims.md` were grepped (not read whole) to resolve V- and C-IDs — V022, V030,
V033–V035, V071, V075–V077, V090, V107, V108, V117, V177, V180, V189, V191, V213, V215–V217,
V219, V220, V222–V225, C301, C302, C354, C522, C526–C528 were all resolved this way.

**ID prefix.** v1 used `C`, v2 used `V`, v3 used `W`, v4 got none. **v5 uses `X`**, numbered in
document order.

**Statuses.** UNCHANGED — same proposition as an existing C/V/W ID; the old ID is recorded and no X
ID is issued. REVISED — the proposition changed; new X ID, with `Replaces` naming the old ID(s).
NEW — no counterpart in any prior inventory. **A proposition that arrived in v4.0 and has no C/V/W
counterpart is graded against the inventory, not against v4.0** — so it appears here as NEW or
REVISED, with the "arrived in v4.0" fact noted in the row or in question (a) below.

**Vocabularies carried over:** Type (ENGINE / MODEL / DESIGN / OUTCOME / WORLD) and Provenance
(stipulated / derivation / file value / numerical test / engine test / prose source / verified
(method unstated) / UNSOURCED). `numerical test` (a solver experiment) and `engine test` (an
observation of EU4 running) are kept strictly distinct. Adding or removing an inline
`[unverified in vN]` marker is **not** a proposition change — v5.0 removed all ten of v3.0's
markers and added none, and that is recorded once, not as ten rows.

**Full-strength sections** (extracted row-by-row regardless of overlap): **§1.3** — the wealth
definition and its modifier-classification table — and **§1.6** — the installed aggregate map, its
sink/source figures, the α_Φ band table, and the Europe/institution demonstration. One row per
measured constant, per classification rule, per stated threshold.

**⚑** marks a row introducing an engine fact no prior inventory carried.
**§** marks a row whose stated evidence is a single observation.
**†** marks a row whose `Replaces` target is believed to exist but could not be pinned to a
specific ID.

---

# Summary

**164 delta claims extracted, X001–X164**, against the 195 W-claims of v3.0 (and through them
V001–V230, C001–C685): **74 NEW, 90 REVISED.**

| Type | NEW | REVISED | Total |
|---|---|---|---|
| MODEL | 32 | 49 | 81 |
| ENGINE | 21 | 22 | 43 |
| DESIGN | 12 | 10 | 22 |
| WORLD | 8 | 5 | 13 |
| OUTCOME | 1 | 4 | 5 |
| **Total** | **74** | **90** | **164** |

| Provenance | Count |
|---|---|
| numerical test | 57 |
| derivation | 52 |
| file value | 23 |
| engine test | 17 |
| stipulated | 14 |
| UNSOURCED | 1 |
| **Total** | **164** |

**Where the delta lands.** §1.3 (44 rows) and §1.6 (33 rows) together carry **47%** of the
inventory, which is what the extraction brief predicted: the whole-install re-sweep of the
modifier classification and the aggregate map it moves are v5.0's subject. §3.13, §3.15, §2.8 and
§3.10 carry the rest of the weight, almost all of it as regenerated figures.

**One class is absent by construction.** v5.0 removed every `[unverified in vN]` marker (ten in
v3.0, five surviving in v4.0) and added none. Per the conventions that is not a proposition change
and no row records it; the front-matter proposition that *no figure is unverified* is X003.

**Engine-test provenance is thinner than v3.0's, not richer.** v3.0 carried 25 `engine test`
claims from one game session; v5.0's delta carries 17 — X019–X021, X023, X025, X026, X038, X055,
X057, X100, X101, X109, X110, X115, X122, X152, X153 — of which most are re-readings of tooltips
on provinces added since v3.0 (Caceres, Girona, Barcelona) and three are save-file reads. **No new
game session was run for v5.0**: the one observation upgraded from single to repeated (X115, the
cycle crash, two launches → three) came from a re-reading of the v2 session dump, not a new launch.

---

# (a) Does v5.0 introduce any proposition that replaces nothing?

`changes-v5.md` asserts: *"v5.0 adds no new subject matter: every proposition in it either survives
from v4.0 unchanged or replaces a v4.0 proposition… A claims delta extracted against
claims-v3.md should therefore consist entirely of rows whose `Replaces` column names an existing
claim."*

**That claim is false as stated, and false by a wide margin: 74 of 164 rows (45%) replace
nothing.** Part of the reason is structural — the assertion is about v5.0 relative to **v4.0**,
but the extraction target is v3.0's inventory, and **v4.0 itself was never extracted**. But the
assertion fails on its own terms too: **52 of the 74 NEW rows are v5.0 text, not v4.0 text**, so
v5.0's own 55 edits added 52 propositions that replace nothing.

The 74 NEW rows sort into three classes (plus one that turned out empty).

### Class 1 — genuinely new subject matter, introduced by v5.0 (52 rows)

Nothing in v4.0, v3.0 or any earlier inventory says anything on the topic. These are the rows that
falsify the "**Propositions added that replace nothing — 0**" line in `changes-v5.md`'s own table.

- **The whole-install classification's new sources (16):** X027 ⚑, X034 ⚑, X035 ⚑, X036 ⚑, X037,
  X040 ⚑, X041 ⚑, X044 ⚑, X046, X047 ⚑, X048 ⚑, X049, X050, X051 ⚑, X052 ⚑, X053. Great projects
  and their tier rule, permanent province modifiers, centres of trade, buildings,
  `production_leader`, the static-modifier values, the Leviathan gating of
  `stora_kopparberget_modifier`, and the flat-bonus census. **Eleven are ⚑ new engine facts.**
- **The α_Φ band table, the Europe demonstration and the route reading (20):** X062, X063, X067,
  X072–X077, X080–X090. A sweep of α_Φ across [1.00, 3.00] at 0.01, four sink-count bands with
  their widths, six European and Lowland development scenarios, and four named trade routes. None
  of this exists in any prior document, and one row (X083 ⚑) is UNSOURCED.
- **The fallback branch's reachability analysis (4):** X007, X008, X009, X012. Where `b ≡ 0` can
  occur, and what decides the orientation there.
- **Twelve loose rows:** X002 (v5.0's own change description), X101 ⚑ and X102 ⚑ (the incumbent
  power figures and what `highest_power` is not), X104 (world wealth), X114 (α_Φ changes are
  design decisions), X116 and X117 (canonical node order; the end count read from the solve),
  X133 (the narrower containment set would halt the solver on correct behaviour), X137 (the bare
  `except` in v4.0's price scan), X144, X149 and X150 (the node-wide-terms argument, the
  construction-dependence of the propagation error, and the 112.6 maximum).

### Class 2 — genuinely new subject matter, introduced by v4.0 and never inventoried (22 rows)

New relative to the inventory, but not new relative to v4.0. `changes-v5.md`'s assertion is
literally true of these, and the inventory still has to carry them because no claims file for v4.0
exists.

X005, X006 (the fallback branch itself, and the candidate set); X022, X023 ⚑, X024 ⚑ (the
`Base`-lines-only rule and the `Industrious` window contamination); X029, X030 (the enters-wealth
test and the data-model-is-an-instance argument); X039 ⚑, X042 ⚑, X043 (three classification
rows); X057 ⚑, X058, X059 (the `Core`/`City`-inside-`TAX_COEFF` argument); X091 (the 22-node
European set); X096 (files-not-proof on trade range); X100 ⚑ (the caravan cap as a share of node
power); X106 (no projection offered); X111 ⚑ (the monthly-tax truncation); X127 (the ε-floor
origin of the 10⁷ ratio); X130 (T3's construction); X138 ⚑ (`NEW_DRAPERIES`); X146 (the 5.7e-14
residual gloss).

### Class 3 — ⚑ NEW rows naming a new fact about EU4 (22 rows — the class the brief asks to surface)

A **cross-cut** of classes 1 and 2, not a third bucket: fourteen of these are v5.0's, eight are
v4.0's. This is the most important case, because §3.16 makes every engine fact carry a source and
this is the largest injection of unaudited engine facts since v3.0's wealth block. (Ten further
rows carry ⚑ as REVISED — X019, X020, X025, X095, X097, X109, X110, X115, X136, X152 — because
they add a new engine fact while displacing an old one.)

| ID | The new engine fact | Provenance |
|---|---|---|
| X023 ⚑§ | Garnatah's window read 3.52 because Granada's 1444 monarch held `Industrious`, +10% | engine test |
| X024 ⚑ | Ruler personalities are rolled at game start wherever country history scripts none | derivation |
| X027 ⚑ | Fifteen 1444 provinces carry a flat bonus in the additive goods-produced block | file value |
| X034 ⚑ | Great-project `province_modifiers` with an empty `can_use_modifiers_trigger` — 6 provinces | file value |
| X035 ⚑ | `add_permanent_province_modifier` in the undated history block — 10 provinces | file value |
| X036 ⚑ | The five static modifiers' values: −2, −0.5, −0.5, −0.25, +0.25 | file value |
| X039 ⚑ | `chinaware` `local_autonomy = −0.1` | file value |
| X040 ⚑ | 361 provinces carry a centre of trade at 1444, and no CoT level grants a key wealth reads | file value |
| X041 ⚑ | `production_leader` `trade_goods_size_modifier = 0.10` is country state | file value |
| X042 ⚑ | `bonus_from_merchant_republics` at `eu4.exe:0x1cc7128` | file value |
| X044 ⚑ | No 1444 province's start state carries a temple, workshop or manufactory | file value |
| X047 ⚑ | 85 of the 130 great projects live at 1444 are gated on country state | file value |
| X048 ⚑ | The six ungated projects and their exact modifier values | file value |
| X051 ⚑ | The ten permanent province modifiers and their province IDs | file value |
| X052 ⚑ | `stora_kopparberget_modifier` is gated `NOT = { has_dlc = "Leviathan" }`, 5.0 on province 8 | file value |
| X057 ⚑§ | The engine's tax multiplier is the **sum** of the itemised percentages | engine test |
| X083 ⚑ | The Renaissance, Colonialism and the Printing Press deliver far more than 1–2% development over 1450–1550 | **UNSOURCED** |
| X100 ⚑§ | The caravan cap is 8.6–32.0% of an inland node's total trade power | engine test |
| X101 ⚑§ | The largest single incumbent holder in an inland node runs 23.6 to 143.2 | engine test |
| X102 ⚑§ | The save's `highest_power` field is **not** the largest incumbent's power | derivation |
| X111 ⚑§ | The displayed monthly tax is the truncation of `base_tax × 0.083333` | derivation |
| X138 ⚑ | `NEW_DRAPERIES` in `HAB - Austria.txt` is −0.25, against −0.20 for the same key in `events/` | file value |

**X083 is the one UNSOURCED claim in the delta**, and by the spec's own §3.16 rule it is a to-do,
not a fact. It is also load-bearing: it is the sentence that converts the ×1.02 measurement into
the argument that Europe will in fact become a sink in play.

### Class 4 — REVISED rows that could not be resolved to a prior ID (0 rows)

**There are none.** Every row whose text visibly displaces an earlier proposition resolved to a
C/V/W ID, with one partial exception, **X142** †, which replaces §3.9's `Φ_w` adoption bullet
("two vanilla-like ends at 1444"). That sentence is carried by claims-v3 as UNCHANGED under V220,
but V220's own statement text does not contain the two-ends premise. The proposition lives in the
V218–V221 range and X142 names V220 as the best available target.

---

# (b) Which prior IDs does v5.0 strand?

Six propositions from the prior inventories are **withdrawn** by v5.0 — stated to be wrong, or
deleted with nothing taking their place. `changes-v5.md` names three of them (V213, V224, and
v4.0's own 0.41%); three more are found only in the spec text.

| Prior ID | The withdrawn proposition | The v5.0 text that withdraws it | Named in `changes-v5.md`? |
|---|---|---|---|
| **W130** | "Zero exact key ties were measured, so the index never decides." | §1.1: *"the candidates are usually all zero-wealth, the wealth key ties, and the **index decides** — which is why §2.4 item 1 makes a canonical emitter node order a correctness requirement rather than a convention"*; §3.2 item 2: *"The one place the indexing is load-bearing is the fallback branch (T3 above)"* | yes (as "T3 settles §3.2's item 2") |
| **W158** | "No 1444 province was observed carrying a flat goods bonus." | §1.3: *"**Fifteen** 1444 provinces do carry a flat bonus in the first block (the table above), so the ordering matters in practice and not only in principle."* | yes (change 4) |
| **V213** | "`α_Φ = 1.5` … calibrated once so the 1444 start yields the hangzhou/english_channel two-sink map." | §2.3: *"**Its stated calibration is withdrawn.** … on the corrected wealth field of §1.3 it does not yield that map, and the map it was fitted to is not reproducible under noise."* | yes (change 9) |
| **V224** | "The `Φ_w` sink count is emergent … it tracks how many world-class wealth poles the flow separates, not α itself." | §1.6: *"**Their count is set by `α_Φ`; only their locations are emergent.** v2.0 through v4.0 said the count 'emerges from concentration exactly as per-good sink counts do' — it does not."* | yes (change 6) |
| **V217** (second clause) | The `Φ_w` graph under ±1% noise is *"stabler than any per-good graph."* | The clause is **deleted without replacement**; §1.6 now ends the sentence at *"0 edge flips and 0 sink-set changes under ±1% wealth noise across 5 seeds"* | **no** |
| **W066** | Trade efficiency *"also feeds the caravan-power and collection tooltips."* | §1.7 now reads *"trade efficiency and a flat income bonus are different quantities in EU4, and the define's own shipped comment settles which this one is"* — the caravan/collection-tooltip clause is gone, as is v4.0's replacement for it (the two `LEDGER_*` columns) | **no** |

**Two more are compressed rather than withdrawn**, and are recorded so that they are not read as
losses:

- **W004** ("four v1 corrections that v2 never applied are folded in") and **W005** ("the four game
  probes settled in `game-session.md` are applied") both lose their front-matter sentences to
  v5.0's *"folds through every refuted and partial claim from all four audits to date"* (X001).
  W004's proposition survives in the unchanged Lineage paragraph; W005's survives in §2.7, which
  still carries all four probe results in full.
- **W061**'s trailing clause "not the 9.3 v2 quoted" is dropped when the gap is regenerated
  (X070); the corrected gap is now stated without the v2 comparison.

**One prior refutation is silently reinstated.** §3.15's Laplacian entry still reads *"supply
contrast (10⁷) drowns demand contrast (10²–10³)"* — the exact ratio §3.2 (X126, X127) now says was
an artifact of v1's ε floor. V117 is therefore simultaneously revised in §3.2 and carried unchanged
in §3.15. This is listed under "Internal inconsistencies" below rather than as a withdrawal,
because the spec asserts both.

---

## §0 — Front matter (lines 1–24)

**UNCHANGED:** C002, C003, C004, V001 *(via §2.5)*, V002, V003, V004, W001, W002.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X001 | v5.0 folds through every refuted and partial claim from **all four audits to date, including v4.0's own**. | WORLD | stipulated | REVISED | W003 |
| X002 | v5.0's substantive change is to §1.3: the local-modifier classification is applied to the **whole install** rather than to the trade-good tables alone, which adds sixteen provinces and moves the aggregate graph from two 1444 sinks to one. | WORLD | stipulated | NEW | — |
| X003 | Every measured number carries the script that produced it, and **no figure in v5.0 is unverified**; the one place the document declines to project a number says so in place. | DESIGN | stipulated | REVISED | W006 |

## §1.1 — Trade direction (lines 29–128)

**UNCHANGED:** C005, C006, C010, C011, C012, C019–C022, V005–V015, V017–V021, V023, V024,
V026–V028, V031, V032, V036, V037, W007–W011, W014–W022.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X004 | On a stall, the promoted node is the heaviest flow-terminal demander **among the candidates**, not among all nodes. | MODEL | stipulated | REVISED | V022 |
| X005 | **The fallback branch:** if the candidates hold no flow-terminal demander at all, the sweep promotes the **highest-wealth** candidate, ties by index; node wealth is a good-independent input, so it needs no bootstrap. *(Arrived in v4.0.)* | MODEL | stipulated | NEW | — |
| X006 | *Candidates* at a stall are the unmarked nodes whose flow out-neighbours are all marked; the flow subgraph is acyclic, so at least one always exists and the sweep always advances. *(Arrived in v4.0.)* | MODEL | derivation | NEW | — |
| X007 | The fallback fires only when every candidate is support-isolated with zero balance — on a connected core, only when `b ≡ 0` across it — because a candidate with a flow out-arc is already *ready* and one with inflow is a flow-terminal demander. | MODEL | derivation | NEW | — |
| X008 | That condition arises for the aggregate graph on a uniform-wealth map, and for a per-good graph on a component with no producer and no consumer. | MODEL | derivation | NEW | — |
| X009 | In those cases the candidates are usually all *zero-wealth*, the wealth key ties, and **the node index decides** the orientation. | MODEL | derivation | NEW | — |
| X010 | Every sink is a selected flow-terminal demand centre, a stall-promoted flow-terminal demander, **a fallback-promoted highest-wealth node**, or a Phase-0 pendant that absorbed a net-importing subtree. | MODEL | derivation | REVISED | W012 |
| X011 | On a map where Phase 0 is a no-op **and no fallback fires**, the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods on 1444, **1–7 sinks per good**, mean 3.6, zero fallbacks. | MODEL | numerical test | REVISED | W013, V030 |
| X012 | A fallback promotion is a sink that is neither selected nor stall-promoted — the third case that breaks the equality (**T3**). | MODEL | derivation | NEW | — |
| X013 | The stall sequence and **both promotion branches** are provably independent of scheduling, because each reads only the candidate set, which the monotone closure fixes. | MODEL | derivation | REVISED | V033 |
| X014 | Free-edge direction is **deterministic** by construction, but that it is a function of the graph and the balances *alone* — that the node indexing never decides — is **measured, not proved**, and holds exactly where the key has no exact ties. | MODEL | derivation | REVISED | V034, W130 |
| X015 | Measured: zero orientation changes under scheduler permutations, and **zero exact `(DEF, b)` ties on free edges**, 29/29 goods. | MODEL | numerical test | REVISED | V035 |

## §1.2 — Supply (lines 130–141)

**UNCHANGED:** C023, C025–C028, V038–V041. No delta claims.

## §1.3 — Demand (lines 143–266) — full-strength extraction

**UNCHANGED:** C031, C032, C033, C035, C036, C039 (the per-province α-weighted demand share),
W023, W024, W025, W026, W030, W031, W032, W033, W036, W050, W051, W052.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X016 | `goods_produced(p) = GP_COEFF · base_production(p) · (1 + Σ local goods-produced modifiers)`, plus local flat goods bonuses. | MODEL | derivation | REVISED | W027 |
| X017 | `trade_value(p) = goods_produced(p) · price(good(p)) · (1 + Σ local trade-value modifiers)`, ducats per year. | MODEL | derivation | REVISED | W028 |
| X018 | `tax_value(p) = TAX_COEFF · base_tax(p) · (1 + Σ local tax modifiers)`, ducats per year. | MODEL | derivation | REVISED | W029 |
| X019 | ⚑ The tax tooltip reads `Base: X (Yearly 12·X)` — `Base: 0.49 (Yearly 6.00)` at `base_tax` 6 and `Base: 0.16 (Yearly 2.00)` at `base_tax` 2. | ENGINE | engine test | REVISED | W034 |
| X020 | ⚑§ The monthly production tooltip's `Trade Value` line is the province window's *annual* `Trade Value` over twelve — observed 3.52 → `Trade Value: +0.29`. | ENGINE | engine test | REVISED | W035 |
| X021 | The time-basis argument is measured on **two** provinces: Garnatah (223) and Caceres (1747 — `base_tax` 2, `base_production` 2, wool). | WORLD | engine test | REVISED | W037 |
| X022 | **Only the tooltips' `Base` lines are used**, because a province window's `Trade Value` also carries the owner's `global_trade_goods_size_modifier`. *(Arrived in v4.0.)* | DESIGN | derivation | NEW | — |
| X023 | ⚑§ Garnatah's window read 3.52 rather than 0.80 × 4.00 = 3.20 because Granada's 1444 monarch held the `Industrious` ruler personality, +10%. *(Arrived in v4.0.)* | ENGINE | engine test | NEW | — |
| X024 | ⚑ Ruler personalities are rolled at game start wherever country history scripts none, so any province-window figure is one sample of a random variable. *(Arrived in v4.0.)* | ENGINE | derivation | NEW | — |
| X025 | ⚑§ Modifiers apply after the coefficient: `Base 0.49` then `Tax Income Efficiency 125.0%` gives **0.6125**, which the province window shows as 0.62. | ENGINE | engine test | REVISED | W038 |
| X026 | The goods-produced tooltip's shape is only **consistent with** flat bonuses entering before the price multiply and does not establish it — an additive `Base Goods Produced` block above a separate multiplicative `Goods Produced Efficiency` block. | ENGINE | engine test | REVISED | W039 |
| X027 | ⚑ **Fifteen 1444 provinces carry a flat bonus in the additive block**, so the ordering matters in practice and not only in principle. | ENGINE | file value | NEW | — |
| X028 | **Locality test:** a modifier is *local* iff its value depends only on the province's own attributes — terrain, climate, trade good, development, buildings — and on no country's state. | MODEL | stipulated | REVISED | W040 |
| X029 | **Enters-wealth test:** a modifier *enters wealth* iff it modifies `goods_produced`, `price` or `tax_value`; a modifier must pass both tests. *(Arrived in v4.0.)* | MODEL | stipulated | NEW | — |
| X030 | The engine's trade-good data model (`province` block vs `modifier` block) is one *instance* of the locality test and not the test itself, because modifiers reach a province from outside the trade-good tables. *(Arrived in v4.0.)* | MODEL | derivation | NEW | — |
| X031 | Applied to the **whole install** rather than `common/tradegoods/` alone, the classification finds **sixteen provinces beyond the two trade goods**; v4.0's "exactly two" was the result of sweeping one directory. | WORLD | derivation | REVISED | W041 |
| X032 | `gems` `local_tax_modifier = 0.15` is local and **enters wealth** through `tax_value`; **43 provinces** carry it. | ENGINE | file value | REVISED | W042 |
| X033 | `incense` `trade_value_modifier = 0.1` is local and **enters wealth** through `trade_value`; **29 provinces** carry it. | ENGINE | file value | REVISED | W044 |
| X034 | ⚑ **Great-project `province_modifiers`** whose `can_use_modifiers_trigger` is empty are local and enter wealth through `goods_produced` and `trade_value` — **6 provinces**. | ENGINE | file value | NEW | — |
| X035 | ⚑ **`add_permanent_province_modifier` in the undated province-history block** is local (applied to the place at the start date) and enters wealth through `goods_produced` — **10 provinces**. | ENGINE | file value | NEW | — |
| X036 | ⚑ The static modifiers `devastation` −2, `occupied` −0.5 and −0.5, `under_siege` −0.25 and `prosperity` +0.25 are all province state, so all are local, and all enter wealth through `goods_produced` and `tax_value`. | ENGINE | file value | NEW | — |
| X037 | All five static modifiers are **zero at the 1444 start**, and §1.2 and §3.3 both depend on them biting later. | MODEL | derivation | NEW | — |
| X038 | `glass` `local_production_efficiency = 0.1` is local but does **not** enter wealth: it modifies production *income*, which wealth does not compute. | ENGINE | engine test | REVISED | W043, W160 |
| X039 | ⚑ `chinaware` `local_autonomy = −0.1` is local but does not enter wealth. *(Arrived in v4.0.)* | ENGINE | file value | NEW | — |
| X040 | ⚑ **361 provinces carry a centre of trade at 1444**; CoT level is province state and therefore local, but no CoT level in `common/centers_of_trade/` grants any of the four keys wealth reads. | ENGINE | file value | NEW | — |
| X041 | ⚑ `production_leader` `trade_goods_size_modifier = 0.10` is **not local** — which country leads a good's production is a country's state. | ENGINE | file value | NEW | — |
| X042 | ⚑ Goods-produced efficiency from nearby merchant republics, trading cities and trade companies (`bonus_from_merchant_republics`, `eu4.exe:0x1cc7128`) is **not local** — its value is set by which neighbouring countries hold those government forms. *(Arrived in v4.0.)* | ENGINE | file value | NEW | — |
| X043 | The owner's `global_trade_goods_size_modifier` is **not local** — it is country-scoped. *(Arrived in v4.0.)* | MODEL | derivation | NEW | — |
| X044 | ⚑ **Buildings are local by the test and empty at 1444** — no province's start state carries a temple, workshop or manufactory — and would enter wealth if any existed. | ENGINE | file value | NEW | — |
| X045 | `terrain.txt` and the climate static modifiers are local but grant only `allowed_num_of_buildings`, `defence`, `local_defensiveness`, `local_development_cost`, `movement_cost`, `nation_designer_cost_multiplier`, `supply_limit`, colonial growth and hostile attrition — none of which wealth computes. | ENGINE | file value | REVISED | W045 |
| X046 | A great project contributes the `province_modifiers` accumulated **up to its `starting_tier`** when `can_use_modifiers_trigger` is empty; tiers reached after the start date are owner spending and are excluded. | DESIGN | stipulated | NEW | — |
| X047 | ⚑ **85 of the 130 great projects live at 1444** are gated on a country's culture, religion, government or flags. | ENGINE | file value | NEW | — |
| X048 | ⚑ Six ungated projects carry a key wealth reads: `falun_copper_mine` (province 8, `trade_goods_size` 3.0), `krakow_cloth_hall` (262, `trade_goods_size_modifier` 0.10) and the four Grand Canal provinces (684, 1821, 1822, 2145; `trade_goods_size` 0.5 and `trade_value_modifier` 0.1 each). | ENGINE | file value | NEW | — |
| X049 | **Province 1821 is the richest single province in the game** under §1.3's wealth. | MODEL | numerical test | NEW | — |
| X050 | The `starting_tier` is the right line and "owner action" is not: development is an owner action, so a rule excluding owner actions would exclude `base_production`, which is wealth's primary input. | DESIGN | derivation | NEW | — |
| X051 | ⚑ The ten permanent province modifiers are `granary_of_the_mediterranean` (362, 363, 2316, 4316), `skanemarket` (6), `icelanding_fisher_sea` (370, 371), `diamond_mines_of_golconda_modifier` (542), `jingdezhen_kilns` (2151) and `coffea_arabica_modifier` (387), all flat `trade_goods_size`. | ENGINE | file value | NEW | — |
| X052 | ⚑ `province_triggered_modifiers`' `stora_kopparberget_modifier` is gated `NOT = { has_dlc = "Leviathan" }` and grants `trade_goods_size = 5.0` on province 8 — the same province as `falun_copper_mine`, which gives 3.0 when Leviathan is present. | ENGINE | file value | NEW | — |
| X053 | Every wealth figure in the document was measured **with Leviathan installed**, which is why §2.3 makes DLC state a third input axis rather than a footnote. | WORLD | stipulated | NEW | — |
| X054 | The two local-but-not-entering rows — glass and chinaware — are the whole of the rule-versus-vocabulary tension, and both tests exclude them for the same reason, so nothing is left to decide. | DESIGN | derivation | REVISED | W160 |
| X055 | What the engine itemised on a real province and the model excludes is `Reform Iqta` +5%, `Clergy` +5%, national ideas +15%, technology production efficiency +2% and the owner's goods-produced modifiers — **`Core` is no longer on that list**. | ENGINE | engine test | REVISED | W046 |
| X056 | `Core` (+75%) and `City` (+25%) are the two that are **not excluded**, because they are already inside `TAX_COEFF`. | MODEL | derivation | REVISED | W047, W048, W049 |
| X057 | ⚑§ The engine's tax multiplier is the **sum of the itemised percentages**: Garnatah's `Tax Income Efficiency: 125.0%` is 75 + 25 + 5 + 5 + 15 (×1.25) and Caceres's `105.0%` is 75 + 25 + 5 (×1.05). *(Arrived in v4.0.)* | ENGINE | engine test | NEW | — |
| X058 | A cored city province carrying nothing else sums to exactly 0.75 + 0.25 = 1.00 and yields `base_tax` ducats a year — the reference condition `TAX_COEFF = 1.0` was measured at. *(Arrived in v4.0.)* | MODEL | derivation | NEW | — |
| X059 | Every province the model counts is a city (`is_city = yes`) and is treated as cored because ownership is not modelled, so carrying either term again would double-count it. *(Arrived in v4.0.)* | MODEL | derivation | NEW | — |

## §1.4 — Market concentration (lines 268–278)

**UNCHANGED:** C040–C047. No delta claims.

## §1.5 — Goods without a graph (lines 280–325)

**UNCHANGED:** C048, C051–C056, V050–V058, W053, W182–W186, W188, W189, W191.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X060 | Measured: repricing the 45 owned latent-coal provinces to coal flips **29 of 159 `Φ_w` edges**. | MODEL | numerical test | REVISED | W187 |

## §1.6 — The aggregate graph (lines 327–431) — full-strength extraction

**UNCHANGED:** C059, C062, V063, V064, V212, V214 *(as narrowed by W054)*, V218, V221, W054,
W055, W058, W063, W064.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X061 | **The `Φ_w` sink count is set by `α_Φ`; only the sink locations are emergent** — the count is a step function of a stipulated constant. | MODEL | derivation | REVISED | V224 |
| X062 | v2.0 through v4.0's "the count emerges from concentration exactly as per-good sink counts do" is wrong, and the value of `α_Φ` was chosen with a target count in view. | WORLD | derivation | NEW | — |
| X063 | What the world state moves is *where* the sinks are and *how the map drains toward them*, which is the property §3.1's first goal actually asks for. | DESIGN | derivation | NEW | — |
| X064 | Measured: identical orientation at ×1 and above, **16 edge flips at ×10⁻² and 83 at ×10⁻⁶** — the orientation degrades while the sink set happens to survive, so the sink set is not the quantity to watch. | MODEL | numerical test | REVISED | W056 |
| X065 | 1444's `b_w` has largest magnitude **0.0227**. | MODEL | numerical test | REVISED | W057 |
| X066 | Measured on 1444 at α_Φ = 1.5: **one sink, `hangzhou`** — rank **1** in the α_Φ-weighted wealth field `c_w` and rank **10** in raw node wealth, where `english_channel` is 1st. | MODEL | numerical test | REVISED | V215, W059 |
| X067 | v2 through v4's two-sink result was measured on a wealth field missing the sixteen provinces §1.3 now carries; correcting the field removes the second sink. | WORLD | derivation | NEW | — |
| X068 | Phase 1 selects `hangzhou` **directly**, so there are **0 promotions and 0 fallbacks** — the self-correction never fires on this input. | MODEL | numerical test | REVISED | V215 |
| X069 | **Seven sources** — `kongo`, `patagonia`, `james_bay`, `mississippi_river`, `chengdu`, `australia`, `tunis` — all in the bottom half of the wealth field (`c_w` ranks 52–79), mean degree **3.0** against the map's 4.0. | MODEL | numerical test | REVISED | W060, V216 |
| X070 | `Φ_w` agrees with the per-good graphs on **52.5%** of edge-goods (51.5% value-weighted) against `Φ_ord`'s 60.3% — a gap of **7.8 points**. | MODEL | numerical test | REVISED | W061, V219 |
| X071 | `Φ_ord`'s edge-good agreement under the deterministic sweep is **60.3%**. | MODEL | numerical test | REVISED | W062 |
| X072 | The sink count was measured as a step function of `α_Φ` across **α_Φ = 1.00…3.00 at 0.01**. | MODEL | numerical test | NEW | — |
| X073 | **1 sink (`hangzhou`) over α_Φ ∈ [1.43, 1.93], width 0.50** — the widest band on this field and the one α_Φ = 1.5 sits in. | MODEL | numerical test | NEW | — |
| X074 | **3 sinks (`doab`, `genua`, `hangzhou`) over [2.26, 2.71], width 0.45.** | MODEL | numerical test | NEW | — |
| X075 | **2 sinks (`genua`, `hangzhou`) over [1.94, 2.25], width 0.31.** | MODEL | numerical test | NEW | — |
| X076 | **2 sinks (`english_channel`, `hangzhou`) over [1.41, 1.42], width 0.01** — v4.0's reported sink set. | MODEL | numerical test | NEW | — |
| X077 | That window is **not reproducible**: under ±1% wealth noise it moves or disappears entirely, while the wide bands move by ≤0.03, so it is not a band and no constant could honestly sit in it. | MODEL | numerical test | NEW | — |
| X078 | `α_Φ` is **retained** at 1.5 because it sits inside the widest band and nothing now selects a different value — not because it was derived. | DESIGN | stipulated | REVISED | V213 |
| X079 | Sampled at the six values v2 used, the count is non-monotone: **5 → 1 → 2 → 4 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}. | MODEL | numerical test | REVISED | V224 |
| X080 | One sink at 1444 is a **snapshot, not a fixed feature**, and the map says so under load. | DESIGN | derivation | NEW | — |
| X081 | Scaling **Europe's 823 counted provinces** by ×1.02 gives the sinks `{doab, english_channel, hangzhou, wien}`, and `english_channel` is a sink at every larger factor tested. | MODEL | numerical test | NEW | — |
| X082 | At Europe ×1.56 the sinks are `{english_channel, rheinland}` and Asia holds none. | MODEL | numerical test | NEW | — |
| X083 | ⚑ A 1–2% European development edge is **far below** what the Renaissance, Colonialism and the Printing Press deliver over 1450–1550. | WORLD | UNSOURCED | NEW | — |
| X084 | Developing only the nine Lowland provinces in `english_channel` (Holland, Zeeland, Vlaanderen, Brabant, Antwerpen, Utrecht, Gelre, Friesland, Breda) by ×1.20 makes `english_channel` a sink beside `hangzhou`, and it stays one through ×10. | MODEL | numerical test | NEW | — |
| X085 | ±2% *random* wealth noise leaves the 1444 sink set unchanged on three seeds, while **+2% applied systematically to Europe alone changes it**. | MODEL | numerical test | NEW | — |
| X086 | The 1444 route from Europe to the sink is the Silk Road: `genua → alexandria → aleppo → persia → lahore → doab → ganges_delta → burma → gulf_of_siam → canton → hangzhou`. | MODEL | numerical test | NEW | — |
| X087 | From the north the route is the Volga: `north_sea → white_sea → novgorod → kazan → astrakhan → persia → …`. | MODEL | numerical test | NEW | — |
| X088 | From the Channel it is the Hansa and the Danube: `english_channel → lubeck → saxony → wien → venice → ragusa → constantinople → aleppo → …`. | MODEL | numerical test | NEW | — |
| X089 | Nothing in `Φ_w` routes through the Cape at 1444, which is what a 1444 map should say. | OUTCOME | numerical test | NEW | — |
| X090 | The Cape is not idle: in the per-good graphs it already carries Asian spices to Europe (`malacca → cape_of_good_hope → zanzibar → gulf_of_aden → alexandria → genua`) — `Φ_w` models power, not cargo. | MODEL | numerical test | NEW | — |
| X091 | The "22 European nodes" are the 18 western and central European nodes plus `constantinople`, `crimea`, `kiev` and `kazan`; under the 18-node set alone sole-`genua` needs ×2.5. *(Arrived in v4.0.)* | MODEL | numerical test | NEW | — |
| X092 | The Cape of Good Hope reverses **between ×3 and ×3.75** of European wealth and does not outside that window, so the reversal is a **band and not a threshold**. | MODEL | numerical test | REVISED | V223 |
| X093 | Dev-stacking `hangzhou`'s top province keeps it the sole sink at ×20, ×30 and ×50, with a transient split into three at ×10. | MODEL | numerical test | REVISED | V223 |

## §1.7 — Merchants (lines 433–459)

**UNCHANGED:** C067–C083, V066, V068, V069, V070, W065, W192.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X094 | Trade efficiency and a flat income bonus are different quantities in EU4, and the define's own **shipped comment** settles which `TRADE_MERCHANT_PRESENT` is: `-- bonus on income if trade present`. | ENGINE | file value | REVISED | W066 |

## §1.8 — Collection and transfer (lines 461–492)

**UNCHANGED:** C084–C102, V072.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X095 | ⚑ What trade range gates is **reach, not flow**: every string, define and modifier that mentions it is about where a country may *send* something — `HINT_TRADERANGE_TEXT`, `TRADE_RANGE_IRO`, `TRADE_NODES_OUT_OF_RANGE`, `MAPMODE_TRADE_DESC`, `MERCENARY_COMPANY_TOO_FAR` / `MERC_RANGE_EXPLAINED` and `REQUIRES_CAPITAL_IN_TRADE_RANGE_TT`. *(Arrived in v4.0; converts V071 from UNSOURCED to file value.)* | ENGINE | file value | REVISED | V071 |
| X096 | "No string, define or modifier ties range to link flow" is a statement about the files, not a proof that no such mechanic exists; settling it needs value observed arriving at a node chain beyond every country's range. *(Arrived in v4.0.)* | DESIGN | derivation | NEW | — |

## §1.9 — Trade power propagation (lines 493–502)

**UNCHANGED:** C103–C111, V073, W067, W068, W069. No delta claims.

## §1.10 — Direction-dependent systems (lines 504–550)

**UNCHANGED:** C112–C143, V074, V078, V079, V080, W070, W071.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X097 | ⚑ Propagate Religion is 50/50 in the default branch and 35/35 in the terminal branch, **neither banded**; the nine `N_trade_power_for_propogate_religion` country-flag rungs between them **are** banded, maintain trailing select by 5–10 points (10→5, 15→5, 20→10, 25→15, 30→20, 35→25, 40→30, 45→35), and the 5-flag carries no maintain share at all. *(Arrived in v4.0.)* | ENGINE | file value | REVISED | V075 |
| X098 | Improve Inland Routes is the one **unconditionally** banded mechanic; every other listed threshold is single-valued, and Propagate Religion is banded only on its flag ladder. | ENGINE | derivation | REVISED | V076 |
| X099 | The flicker-risk set is "every country at a single-valued limit, plus flagless countries at Propagate Religion's 50/50 or 35/35" — **not "every country"**. | OUTCOME | derivation | REVISED | V077 |
| X100 | ⚑§ Measured on the 1444 start: the caravan cap of 50 is **8.6% to 32.0% of an inland node's total trade power** (median 17.9% over the 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`). *(Arrived in v4.0.)* | ENGINE | engine test | NEW | — |
| X101 | ⚑§ The largest single incumbent holder in an inland node runs **23.6 to 143.2**, so a country at the cap outweighs the largest incumbent in **7 of the 26** inland nodes and is outweighed in the other 19. | ENGINE | engine test | NEW | — |
| X102 | ⚑§ The save's `highest_power` field (9.6–20.7) is **not** the largest incumbent's power, and v4.0's conclusion drawn from reading it that way inverted. | ENGINE | derivation | NEW | — |

## §1.11 — Treasure fleets · §1.12 — What the game displays (lines 552–577)

**UNCHANGED:** C144–C165, V049, V065, V081. No delta claims.

## §2.1 — Shape (lines 583–600)

**UNCHANGED:** C167–C184, V082–V085, W072, W073. No delta claims.

## §2.2 — Solver (lines 602–639)

**UNCHANGED:** C185–C209, V064, V091, V092, V229, W075, W076.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X103 | Solver item 4 computes `TAX_COEFF · base_tax · (1 + local tax mods) + (GP_COEFF · base_production + local flat goods bonuses) · (1 + local goods-produced mods) · price · (1 + local trade-value mods)`, reading the local modifiers from §1.3's classification **applied to the whole install** — gems (43 provinces), incense (29), six great projects and ten permanent modifiers, 16 provinces beyond the two goods. | DESIGN | stipulated | REVISED | W074 |
| X104 | **World wealth is 10,677.50 annual ducats over 2,452 counted provinces.** *(Arrived in v4.0 as a solver figure; the value is v5.0's.)* | MODEL | numerical test | NEW | — |
| X105 | Measured on the reference implementation (scipy/HiGHS plus the deterministic sweep, one machine): **0.17–0.21 s for all 29 goods, a mean of 5.7–7.3 ms per good across runs**, with individual goods ranging 5.4–24 ms, so 7.3 is an average and not a maximum. | MODEL | numerical test | REVISED | V090 |
| X106 | "Milliseconds each" holds already with a generic LP; no measurement in this project supports a projection for a native network simplex, **and none is offered**. *(Arrived in v4.0; v5.0 removes its `[unverified]` marker and states the refusal.)* | DESIGN | derivation | NEW | — |

## §2.2a — What map this is for (lines 641–681)

**UNCHANGED:** W077–W085, W088.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X107 | Free-edge determinism is **proved as determinism** but **measured** as independence from the node indexing (zero exact `(DEF, b)` ties, 29/29 goods), and both halves survive Phase 0 because peeling does not touch the priority key. | MODEL | derivation | REVISED | W086 |
| X108 | **Two** cases independent of Phase 0 break sink-set equality inside the 2-core: the free-edge race (**T2**) and a fallback promotion (**T3**). | MODEL | derivation | REVISED | W087 |

## §2.3 — Constants (lines 683–728) — measured constants, row per constant

**UNCHANGED:** C211–C227 (the defines table and "read at runtime, never hardcoded"), V094, W089,
W090, W091, W092 (`GP_COEFF` = 0.2), W094 (`TAX_COEFF` = 1.0), W097, W098, and the DLC-third-axis
claim.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X109 | ⚑ `GP_COEFF = 0.2` is measured on **four provinces at four development levels** from the `Base Goods Produced` line: Caceres (1747) 2 → 0.40, Girona (212) 3 → 0.60, Garnatah (223) 4 → 0.80, Barcelona (213) 5 → 1.00. | ENGINE | engine test | REVISED | W093 |
| X110 | ⚑ `TAX_COEFF = 1.0` is measured on **two provinces at two development levels** from the `(Yearly …)` parenthetical: Garnatah 6 → `Base: 0.49 (Yearly 6.00)`, Caceres 2 → `Base: 0.16 (Yearly 2.00)`. | ENGINE | engine test | REVISED | W095 |
| X111 | ⚑§ The displayed monthly tax is the **truncation** of `base_tax × 0.083333`. *(Arrived in v4.0.)* | ENGINE | derivation | NEW | — |
| X112 | Both coefficients are read off the tooltips' **base** lines, which carry no owner term, and **neither off a province window**, because a window figure carries owner modifiers some of which are randomised at game start. | DESIGN | derivation | REVISED | W096 |
| X113 | **`α_Φ`'s stated calibration is withdrawn**: v2.1 through v4.0 said 1.5 was calibrated so the 1444 start yields the two-sink hangzhou/english_channel map, and on the corrected wealth field it does not yield that map. | WORLD | derivation | REVISED | V213 |
| X114 | Any future change to `α_Φ` is a **design decision about how many ends the installed graph should have**, and should be recorded as one. *(Arrived in v4.0 in spirit; stated in v5.0.)* | DESIGN | stipulated | NEW | — |

## §2.4 — The tradenodes file (lines 730–771)

**UNCHANGED:** C228–C242, V095, V148, V221, W099, W100, W102–W107, W114.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X115 | ⚑ The two-node cycle produced `EXCEPTION_STACK_OVERFLOW` at a single **exception address** (`0x00007FF6DDE6A8B4`) under **1002 recorded `eu4.exe` frames** — the dump records no per-frame addresses — reproduced on **three** launches. *(Arrived in v4.0; corrects W101's "1002 stack frames at a single return address, reproduced on two launches".)* | ENGINE | engine test | REVISED | W101 |
| X116 | **The node order itself is a correctness requirement, not a convention:** the emitter must fix one canonical node order and keep it stable across rebuilds, or the same world can produce two different maps. | DESIGN | derivation | NEW | — |
| X117 | The end-node count is **not fixed** — it follows the wealth field and `α_Φ`, so the emitter reads it from the solve rather than assuming a number. | DESIGN | derivation | NEW | — |

## §2.5 — Runtime attachment · §2.6 — Writing to the engine (lines 772–798)

**UNCHANGED:** C243–C272. No delta claims.

## §2.7 — Probes (lines 800–837)

**UNCHANGED:** C274–C293, V098–V101, W108–W114. No delta claims.

## §2.8 — Validation (lines 839–881)

**UNCHANGED:** C298–C342, V106, V109–V112, W116, W119, W195.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X118 | Baseline cloves sinks are **Venice, Kongo, Deccan, Australia, Brazil**; under the §3.13 α-calibration `spices` sinks at **Genoa alone** and it is cloves that moves to **Deccan**. | MODEL | numerical test | REVISED | W115 |
| X119 | High-demand nodes are sinks at **14.5%** in the top demand decile against 6.9% in the bottom — a barbell, since LP branch ends land in poor pockets. *(The 1-to-7 range is X011.)* | MODEL | numerical test | REVISED | V108 |
| X120 | Zeroing **`hangzhou`**-node development relocates the sink in one solve — measured, the `Φ_w` sinks move from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`; `hangzhou`, not `beijing`, is China's wealth pole, and zeroing `beijing` (node-wealth rank 39) moves nothing. *(Arrived in v4.0 and **not regenerated for v5.0** — see the inconsistency note.)* | OUTCOME | numerical test | REVISED | C301 |
| X121 | If Ming loses the Mandate, **nothing moves on the day it happens**: the Mandate is an owner property and §1.3 reads none, so the pull collapses only as the consequences reach `base_tax` and `base_production`. *(Arrived in v4.0.)* | OUTCOME | derivation | REVISED | C302 |
| X122 | The two-run vanilla divergence spans five node fields (`current`, `local_value`, `outgoing`, `total`, `retention`); `retention` is identical on 80 of 80 nodes and `total` on **78 of 79**, the exception — **`zambezi`** — drifting 0.012%. | ENGINE | engine test | REVISED | W117, W118 |
| X123 | 2-core containment is asserted every tick against `{selected} ∪ {promoted} ∪ {fallbacks}` — the set the sweep actually maintains — because asserting the narrower set would halt on **T3**, which is correct behaviour. | DESIGN | derivation | REVISED | W193 |
| X124 | Sink-set equality is *monitored* with **T2 and T3** named as its two legitimate failures; it is measured exact on 1444, 29/29 goods, **zero fallbacks**. | DESIGN | derivation | REVISED | W194 |

## §2.9 — Build order · §3.1 — Goals (lines 882–905)

**UNCHANGED:** C343–C352, C353, C355–C365, V113.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X125 | Goal 1's worked example is a horde razing **`hangzhou`**, not Beijing. *(Restated in §3.9; one ID at first appearance.)* | OUTCOME | derivation | REVISED | C354 |

## §3.2 — Why a flow and a drainage sweep (lines 907–1005)

**UNCHANGED:** C366, C370–C375, C383–C385, V115, V116, V118–V122, V124, V128–V131, W120, W123,
W125–W129 *(W129 as revised by X131)*, W131.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X126 | The Laplacian's asymmetry is **sparsity, not contrast**: supply is sparse where demand is dense — spices are produced in 18 of 80 nodes and cloves in one, while every node with an owned province carries demand. *(Arrived in v4.0.)* | MODEL | numerical test | REVISED | V117 |
| X127 | v1 and v2's "supply contrast 10⁷ against demand contrast 10²–10³" was `max(s)` over the **ε floor** of v1's regularizer; with no regularizer the spices supply ratio over *producing* nodes is **36 against a demand ratio of 482.2**, which points the other way. *(Arrived in v4.0; the 482.2 is v5.0's.)* | WORLD | numerical test | NEW | — |
| X128 | Better wealth inputs deliver about 1.7× — measured, `genua` becomes a co-sink at **×1.720**. | MODEL | numerical test | REVISED | W121 |
| X129 | A spices sink at any of the four Chinese trade nodes needs **3.6–4.9×**, i.e. **9.3–21.4%** of all world spice demand at one node (`beijing` 3.60× / 9.3%, `hangzhou` 3.83× / 21.4%, `xian` 4.59× / 12.3%, `canton` 4.86× / 17.8%); `girin`, `yumen`, `chengdu` and `lhasa` need 4.0× to 10.8×. | MODEL | numerical test | REVISED | W121, W122 |
| X130 | **T3 — the fallback branch inside the 2-core.** A triangle with `b = 0` at all three nodes and wealth 3, 2, 1: Phase 1 selects nothing, every edge is free, the sweep stalls with no flow-terminal demander, the fallback promotes A, and the actual sinks are `{A}` while the formula set is empty — A is in neither `{selected}` nor `{promoted}`. *(Arrived in v4.0.)* | MODEL | numerical test | NEW | — |
| X131 | All **three** constructed counterexamples were run through a faithful implementation of §1.1 (**`toys.py`**). | WORLD | numerical test | REVISED | W129 |
| X132 | The ⊆-direction holds within the 2-core **over the set the sweep actually maintains**: every core node that is neither selected, promoted **nor fallback-promoted** is handed an out-arc, and pendant net-importers are the only sinks outside that set. | MODEL | derivation | REVISED | W124 |
| X133 | Written against the narrower containment set, **T3 would halt the solver on correct behaviour**. | DESIGN | derivation | NEW | — |

## §3.3 — Why wealth, and why per province · §3.4 — Why supply is pre-modifier (lines 1007–1040)

**UNCHANGED:** C386–C423, V132, V133, V135, V137–V139, W132–W142. No delta claims.

## §3.5 — Why α is anchored absolutely (lines 1042–1067)

**UNCHANGED:** C427–C442, V140–V144, V146, V147.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X134 | **13 of 30 goods** can be pushed strictly below 2.0 by a single vanilla `change_price` event (grain and wine reach 0.625). | ENGINE | file value | REVISED | W143 |
| X135 | **Two** goods — `gems` and `silk` — land exactly on 2.0; four have a negative event that does not reach 2.0; **11 have no negative price event at all**. | ENGINE | file value | REVISED | W144, W145 |
| X136 | ⚑ All **161** `change_price` blocks were parsed: 93 in `events/`, **14 in `missions/`**, 1 in `common/`, and **53 in `history/` of which 13 are negative**, all in `history/countries/HAB - Austria.txt`. | ENGINE | file value | REVISED | W146 |
| X137 | v4.0's 154-and-7 came from a parser that silently recovered nothing from five mission files behind a bare `except`; the scan is now guarded by a per-file count assertion, and the seven recovered blocks are all positive. | WORLD | derivation | NEW | — |
| X138 | ⚑ `wool`'s largest single negative is `HAB - Austria.txt`'s `NEW_DRAPERIES` at −0.25 (2.5 → **1.875**) against the −0.20 the same key carries in `events/PriceChanges.txt`; `change_price` entries are keyed, so 1.875 is the figure a campaign reaching 1540 holds. *(Arrived in v4.0.)* | ENGINE | file value | NEW | — |

## §3.6 — Why no hysteresis, and why there is no ε (lines 1069–1104)

**UNCHANGED:** C443–C452, V148, V152, V154, W147–W152. No delta claims. *(The cycle-crash
re-description is X115, at its first appearance in §2.4.)*

## §3.7 — Why eligibility is per good (lines 1106–1113)

**UNCHANGED:** C463–C473. No delta claims.

## §3.8 — Why gates evaluate true (lines 1114–1132)

**UNCHANGED:** C474–C497, V155–V158, W154.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X139 | Measured under DRAIN, **92.2%** (5825 of 6320) of ordered node pairs are connected by at least one good on 1444 data. | MODEL | numerical test | REVISED | W153 |

## §3.9 — Why `Φ_w` is the installed graph (lines 1134–1177)

**UNCHANGED:** C502, C505–C512, V160–V162, V218, V221, V228.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X140 | The rich non-sink nodes are **`genua`, `gulf_of_siam` and `sevilla`** — node-wealth ranks 3, 2 and 7, none of them a sink — each drawing more edges in than it sends out. *(Arrived in v4.0.)* | MODEL | numerical test | REVISED | W156 |
| X141 | `Φ_ord` has **13 end nodes at 1444, 8 of which terminate no good at all**, and its end count never concentrates: **11–17** ends across cloves-α 2…64, against its own baseline of 13. | MODEL | numerical test | REVISED | V222, W155 |
| X142 | † `Φ_w`'s adoption rationale is **one operator, one set of guarantees, and ends that move with the world**; the "two vanilla-like ends at 1444" premise is **withdrawn**, and the trade is now 7.8 points of self-coherence given up for world-responsive ends whose 1444 count is whatever the field gives. | DESIGN | stipulated | REVISED | V220 † (the two-ends premise sits in the V218–V221 range) |

## §3.10 — Why the engine's economy is overwritten (lines 1179–1194)

**UNCHANGED:** C513–C521, C523–C525, C529, C530.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X143 | The income factoring is an **identity, not a measurement**: `powershare_C(n)` carries no `g`, so it factors out of the sum and the property is true by construction and carries no measurement. *(Arrived in v4.0.)* | MODEL | derivation | REVISED | C522 |
| X144 | Every term feeding a collector's power at a node is node-wide — merchant bonus, off-home penalty, propagation off the one installed graph, caravan grant — so none of them can reintroduce a `g`. | MODEL | derivation | NEW | — |
| X145 | Across **Sevilla, Genoa, Champagne, Malacca and the Gulf of Siam**, using each node's real 1444 country table, the two forms agree to a worst relative disagreement of **0 to 3.7e-16** — at most one unit in the last place. | MODEL | numerical test | REVISED | C522, C526 |
| X146 | v1 through v4.0's 5.7e-14 and 1.4e-14 are floating-point residuals of an exact identity, produced by constructions none of those documents states — a theorem decorated with an experiment. *(Arrived in v4.0.)* | WORLD | derivation | NEW | — |
| X147 | The per-good propagation driver is **not** how many distinct downstream sets a node has but whether its collectors hold **differing power across the nodes those sets differ on** — `gulf_of_siam` has eight distinct sets and still shows a **0.003%** effect. | MODEL | numerical test | REVISED | C528 |
| X148 | The per-good propagation error is **redistributive and single-digit percent, with the sign varying by collector**: Sevilla −0.82%, −0.87%, **+7.44%**; Champagne −1.69%, +1.69%, +1.53%; Genoa −0.23%, −0.22%, +0.70%. | MODEL | numerical test | REVISED | C527 |
| X149 | Its size depends on which countries are collecting — a stated choice of the construction, not a property of the node — so no single percentage is quoted as one. | DESIGN | derivation | NEW | — |
| X150 | **No node in the model has local trade value near 250 — the largest is 112.6** — and v4.0's replacement figure of 0.41% was an artifact of freezing one term at the alphabetically first commodity. | MODEL | numerical test | NEW | — |

## §3.11 — Caravan power · §3.12 — Treasure fleets (lines 1196–1232)

**UNCHANGED:** C531–C547, C556–C560, V163–V172. No delta claims.

## §3.13 — Open questions (lines 1234–1292)

**UNCHANGED:** C561–C585, V173–V175, V178, V181, V182, V183, W159, W164.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X151 | **One** §1.3 wealth question remains open — what else multiplies `goods_produced`, and which side of the owner line each source falls on — the other two having been settled and moved into §1.3. | DESIGN | stipulated | REVISED | W157, W158 |
| X152 | ⚑§ Barcelona's production tooltip reads `Production Efficiency: +12.0% / From Technology: +2.0% / Producing Glass: +10.0%`, so the engine books glass's +10% on production income. *(Arrived in v4.0; settles W160/W161.)* | ENGINE | engine test | REVISED | W161 |
| X153 | `TAX_COEFF` **is** 1.0 across the development range, with `GP_COEFF` linear at four levels — W162's open question is closed. | ENGINE | engine test | REVISED | W162, W163 |
| X154 | The sublinear regime is reachable through vanilla price events for **13 of 30** goods, unreachable for 11, and exactly on the boundary for **2**. | DESIGN | derivation | REVISED | W165 |
| X155 | The calibration's sink-count span is exactly 1..5 with **spearman(price, sinks) = −0.20**. | MODEL | numerical test | REVISED | V177 |
| X156 | Under the calibration's α = 16, **Deccan** is demand rank 2 — with the rank-1 demander `hangzhou` acting as a transit node — and becomes the cloves sink, while **Beijing is only demand rank 3**. | MODEL | numerical test | REVISED | W166 |
| X157 | `hangzhou` holds the richest single province at **30.4** against Beijing's 19.5. | MODEL | numerical test | REVISED | W167 |
| X158 | The twig tolerance re-routes arcs individually carrying <0.03% of world supply but **up to about 0.18%** of a good's mass in total, and drops **cloves** to 99.97% reach. | MODEL | numerical test | REVISED | W168, V180 |

## §3.14 — AI merchant assignment (lines 1294–1311)

**UNCHANGED:** C586–C624, W169.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X159 | The survival table is 29 goods × 80 × 80 entries at 8 bytes = **1,484,800 bytes**, and the solver's residuals sit at **1e-16, one ULP of a double**. *(Arrived in v4.0; replaces the 5.7e-14 / 1.4e-14 justification.)* | MODEL | derivation | REVISED | W170 |

## §3.15 — Rejected (lines 1313–1413)

**UNCHANGED:** C625–C672, V184–V188, V192–V199, V226–V228. *(V117's "supply contrast 10⁷"
survives verbatim in this section — see the inconsistency note.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X160 | Ranked orientation's alignment statistics are ρ_val **+0.281** against DRAIN's **+0.054**, with **43.8%** of top-decile nodes sinks against **14.5%**. | MODEL | numerical test | REVISED | W171 |
| X161 | Ranked orientation reaches **83.0%** of demand with **31** orphan sinks. | MODEL | numerical test | REVISED | V189 |
| X162 | It posts **8** net-producer sinks where DRAIN, LAP and FLOW all post zero, and **10–16** sinks per good against DRAIN's 1–7. | MODEL | numerical test | REVISED | W172 |
| X163 | Seeded basin growth reaches **88.4%** at its best tuning. | MODEL | numerical test | REVISED | V191 |
| X164 | The 3-mass gravity kernel hits any chosen end count exactly **for γ ≤ 0.7 and any count up to six** — at γ = 0.9 the five- and six-mass fields both give four ends — with **61%** vanilla-arrow agreement at its best (γ = 0.97, **97 of 159** arrows), and v2's 69% = 110 of 159 is not reached at any γ. | MODEL | numerical test | REVISED | W190, V225 |

## §3.16 — Evidence standard (lines 1415–1477)

**UNCHANGED:** C677–C685, V200–V210, W173–W181. No delta claims. *(The "five fields" clause added
here in v4.0 is X122, at its first appearance in §2.8.)*

---

## § Single-observation evidence (9)

Every row below rests on **one** observation. The spec flags none of them as single-observation,
though §3.16's own closing rule — "every measured claim that could vary run to run should carry
the control that bounds its noise floor" — applies to all nine.

| ID | The single observation |
|---|---|
| X020 | One production tooltip reading (3.52 → +0.29) carries the whole annual-over-twelve ratio for the trade-value term |
| X023 | One province window (Garnatah), attributed to one randomised ruler personality |
| X025 | One province's tax itemisation (0.49 × 125.0% = 0.6125) carries the modifier-ordering rule |
| X057 | Two arithmetic decompositions (Garnatah 125.0%, Caceres 105.0%) — one per province, no repeat |
| X100, X101 | One 1444 save's inland-node power tables |
| X102 | One reading of one save field, used to overturn v4.0's inverted conclusion |
| X111 | One inferred truncation from two tooltip readings |
| X152 | One tooltip (Barcelona), used to close an open question |

**Newly *repeated*.** X115 upgrades the cycle crash from two launches to three, so it remains the
one engine-test claim in the project carrying both a repeat and a null.

---

## † Unresolvable IDs

**One.**

| X ID | Section | The proposition it replaces | Believed range |
|---|---|---|---|
| X142 | §3.9 | "`Φ_w`, adopted: two vanilla-like ends at 1444 that move with the world, from the same operator the goods already use." | **V218–V221.** claims-v3 carries the §3.9 adoption bullet as UNCHANGED under V220, but V220's recorded statement text is the *power-not-logistics* rationale and does not contain the two-ends premise. The premise may be an unextracted clause of V220 or may sit with V215/V221's end-count facts. |

The nine `†` C-range rows inherited from claims-v3 (W001, W030, W050, W070, W099/W106, W116, W132,
W140, W169) are all UNCHANGED in v5.0 and need no further resolution here.

---

## Internal inconsistencies observed during extraction

Recorded as observations, per the extraction brief; nothing was corrected and the spec was not
edited.

1. **The coal-activation figure disagrees with itself.** §1.5 says repricing the 45 owned
   latent-coal provinces flips **29 of 159** `Φ_w` edges (X060); §2.8's `Latent good` row still
   says **10 of 159**. `changes-v5.md` entry 24 regenerated one occurrence and not the other.
2. **§3.13 contradicts §1.3 on flat goods bonuses.** §1.3 says *"Fifteen 1444 provinces do carry a
   flat bonus in the first block"* (X027); §3.13's surviving open question still says *"no 1444
   province was observed carrying a flat `trade_goods_size` in the additive block"*. These are the
   refuted claim and its refutation, both asserted.
3. **§2.8's `Razed China` row is on the old wealth field.** It says the `Φ_w` sinks move *from*
   `{english_channel, hangzhou}` and that `hangzhou` is `c_w` rank 3 and node-wealth rank 12 —
   against §1.6's one sink, `c_w` rank 1, node-wealth rank 10 (X066). The row was not regenerated.
4. **§3.15 still carries the ratio §3.2 refutes.** §3.2 says the 10⁷-vs-10²–10³ contrast was an
   artifact of v1's ε floor and the real ratio is 36 against 482.2 (X126, X127); §3.15's Laplacian
   entry still reads *"supply contrast (10⁷) drowns demand contrast (10²–10³)"*.
5. **The inland-node count is used two ways.** §2.2 says derivation gives **25** inland nodes
   against the flag's 26 and that the flag is not to be trusted; §1.10's caravan measurement
   (X100, X101) and §3.11 both work over **26** inland nodes.
6. **"mean 3.6" survived a wealth-field change that moved everything around it.** §1.1's sink
   figures were regenerated from 1–8 to 1–7 sinks per good, but the mean is carried across
   unchanged at 3.6; `changes-v5.md` entry 22 replaces the range and leaves the mean inside the
   same sentence.
7. **§1.6 calls `α_Φ` "a stipulated constant" while stating it was chosen against a target.**
   X061/X062 say the value "was chosen with a target count in view" and X078 says it is retained
   because it sits in the widest band — two different selection stories for one number, both in
   §1.6, with §2.3 (X113) withdrawing a third.
