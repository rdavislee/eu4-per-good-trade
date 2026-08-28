# Claim Inventory Delta — Per-Good Trade Network Spec v6.0

Extracted from `per-good-trade-spec.md` (v6.0, 1,686 lines) as a **delta against
`../v5-owner-agnostic/claims-v5.md`** (X001–X196), which is itself a delta against
`../v3-owner-agnostic/claims-v3.md` (W001–W195), `../v2-drain/claims-v2.md` (V001–V230) and
`../v1-laplacian/claims.md` (C001–C685). Extraction only: nothing here is validated, corrected or
commented on. No claim below is assessed for truth, support or wording.

**Method.** The v6.0 spec was read in full (all 1,686 lines) and `claims-v5.md` was read in full
(header, conventions, all 196 claim rows, its UNCHANGED lists and its withdrawal table). A
paragraph-level diff of the v5.0 and v6.0 spec texts was then computed and read end to end — **32
changed passages** — so that every v6.0 proposition could be classed as changed or carried without
guessing. `claims-v3.md`, `claims-v2.md` and `claims.md` were grepped (not read whole) to resolve
individual W, V and C IDs where a v6.0 revision lands on a sentence that v5.0 carried UNCHANGED:
W025, W031, W032, W036, W050, W052, W056–W062, W064, W067, W108–W114, W187, W189, V138, V204, V225
were resolved this way. `changes-v6.md` was **not** used as a source for any claim; every row was
read off the spec text itself.

**ID prefix.** v1 used `C`, v2 used `V`, v3 used `W`, v4 got no inventory, v5 used `X`.
**v6 uses `Y`**, numbered in document order.

**Statuses.** UNCHANGED — the same proposition as an existing C/V/W/X ID; the old ID is recorded in
the section's carry-forward list and no Y ID is issued. REVISED — the proposition changed; a new Y
ID with the old ID(s) in `Replaces`. NEW — no counterpart in any prior inventory. A proposition
stated in two sections keeps one ID at first appearance; later restatements are noted in the row
rather than given an ID of their own. Adding or removing a script attribution, or adding a file
path to an otherwise identical claim, is **not** treated as a proposition change.

**Type.** ENGINE (how EU4 behaves) / MODEL (the mathematical model) / DESIGN (a stipulation, goal or
choice) / OUTCOME (what the built mod will produce in play) / WORLD (truth-apt claims about history
or about the project's own review history).

**Provenance.** stipulated / derivation / file value / numerical test / engine test / prose source /
verified (method unstated) / UNSOURCED. `numerical test` (a solver or harness experiment) and
`engine test` (an observation of EU4 actually running) are kept strictly distinct.

**Markers.** **⚑** a claim introducing an engine fact no prior inventory carried. **§** a claim
whose stated evidence is a single observation. **†** a `Replaces` target believed to exist but not
pinned to a specific ID.

---

# Summary

**183 delta claims extracted, Y001–Y183**: **90 NEW, 93 REVISED**. The 93 REVISED rows replace
**99 distinct prior IDs** — 90 X IDs, 7 W IDs and 2 V IDs. A further **38 X IDs are withdrawn**
without a successor (table at the end). **933 prior IDs are carried UNCHANGED** across the
per-section carry-forward lists below — 594 C, 153 V, 118 W, 68 X — counted by expanding the ranges
those lists name.

### Delta claims by status and Type

| Type | NEW | REVISED | Total |
|---|---|---|---|
| MODEL | 42 | 61 | 103 |
| DESIGN | 17 | 13 | 30 |
| ENGINE | 17 | 11 | 28 |
| WORLD | 13 | 8 | 21 |
| OUTCOME | 1 | 0 | 1 |
| **Total** | **90** | **93** | **183** |

### Delta claims by Provenance

| Provenance | NEW | REVISED | Total |
|---|---|---|---|
| numerical test | 32 | 45 | 77 |
| derivation | 32 | 27 | 59 |
| file value | 16 | 6 | 22 |
| stipulated | 10 | 11 | 21 |
| engine test | 0 | 4 | 4 |
| prose source | 0 | 0 | 0 |
| verified (method unstated) | 0 | 0 | 0 |
| UNSOURCED | 0 | 0 | 0 |
| **Total** | **90** | **93** | **183** |

**No row in this delta carries UNSOURCED, prose-source or `verified (method unstated)` provenance.**
The one surviving UNSOURCED row in the whole inventory is W071, carried UNCHANGED at §1.10 —
`claims-v5.md` recommended re-typing it `derivation`, and this pass has not applied that either.

**18 rows are marked ⚑** — engine facts no prior inventory carried: Y018, Y034, Y036, Y038, Y040,
Y045, Y049, Y051, Y053, Y055, Y056, Y057, Y059, Y065, Y114, Y115, Y149, Y151. **13 of the 18 are
NEW**, and **13 of the 18 sit in §1.3 alone**, which is where v6.0's start-state reads
(`on_startup` devastation, dated `add_base_*`, the absent `is_city` filter, the rolled trade goods)
land. The count is down from v5.0's 43 because the whole-install modifier sweep — which supplied
most of them — is deleted rather than extended.

**Four rows are marked §** — evidence resting on a single observation: Y038, Y040, Y062 and Y138.
That is down from v5.0's five, and Y138 is new to the list: v6.0 adds the single-observation hedge
to probe 15 itself.

### Where the delta concentrates

| Section | Y rows | What drove it |
|---|---|---|
| §1.6 Aggregate graph | 44 | two sinks instead of one, the 400-relabelling node-order study, the withdrawn α_Φ derivations, the rewritten Europe table and route geography |
| §1.3 Demand | 43 | the classifier's deletion and the three corrected start-state reads |
| §0 Front matter | 15 | the harness-coverage disclosure and the two prose conventions |
| §2.4 The tradenodes file | 11 | Phase 2's degeneracy as the reason for a canonical node order |
| §3.10 Income factoring | 9 | the `ps̄_C` argument replacing every quoted magnitude |
| §1.1, §3.5 | 8 each | the post-peel fallback condition · the `change_price` executability census |
| §1.10, §3.15 | 7 each | the trading-policy cooldowns · the graveyard's de-figuring |
| §3.13 | 6 | the wealth question restated as a design question |
| §2.8 | 5 | regenerated rows plus the ordering-robustness note |
| §2.2, §3.2, §3.9 | 4 each | |
| §1.5, §2.3 | 2 each | |
| §2.2a, §2.7, §3.4, §3.16 | 1 each | |

---

# §0 — Front matter (lines 1–53)

**UNCHANGED:** C002, C003, C004, V001, V002, V003, W001, W002.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y001 | v6.0's substantive change is to §1.3: **wealth is a function of the province's development, its trade good and its own current condition, and of nothing else.** | DESIGN | stipulated | REVISED | X002 |
| Y002 | v6.0 keeps v3.0's owner-agnostic wealth and makes it **true by construction** rather than by a rule that has to be policed. | DESIGN | stipulated | NEW | — |
| Y003 | The two-test modifier classifier and everything it governed — trade-good modifiers, great projects, permanent province modifiers, buildings, centres of trade and the DLC conditionality — are deleted, along with the whole-install sweep that maintained them. | DESIGN | stipulated | NEW | — |
| Y004 | On the 1444 start that apparatus was worth **105.30 ducats** — 0.98% of the **10,712.70** the field totalled with it, 0.99% of the **10,607.40** without. | MODEL | numerical test | NEW | — |
| Y005 | What it cost was an input surface whose classification was **wrong in both independent audits that examined it** — `../v3-owner-agnostic/validation-v3.md` W041 and `../v5-owner-agnostic/validation-v5.md` X030 and X034 — and passed by v4.0's own repair harness, which v5.0 then refuted. | WORLD | derivation | NEW | — |
| Y006 | Three start-state reads are corrected in the same pass: `on_startup` devastation, dated `add_base_*` accumulation, and the `is_city` filter the engine does not apply. | DESIGN | stipulated | NEW | — |
| Y007 | The reason a canonical node order is a correctness requirement is that **Phase 2's min-cost flow is degenerate, so presentation order selects which optimum is returned** — not the priority key's index tiebreak. | MODEL | numerical test | REVISED | X125 |
| Y008 | Prose convention: **no empirical absolutes** — no superlative, no universal quantifier and no threshold asserted as a fact about the world; a claim is either a directional design statement or an observation scoped to the field and script that produced it. | DESIGN | stipulated | NEW | — |
| Y009 | Prose convention: **no maintained figures for any rejected operator** — §3.15's graveyard keeps its design arguments and loses its measurements (`Φ_ord`, the gravity kernels, the v1 Laplacian, RANK, the seeded basins). | DESIGN | stipulated | NEW | — |
| Y010 | Those rejected-operator numbers were re-measured and re-refuted in three successive audits and not one of the rejection arguments depends on them. | WORLD | derivation | NEW | — |
| Y011 | Every graded claim from `../v5-owner-agnostic/validation-v5.md` — **22 refuted, 39 partial, 1 unverifiable** — is folded through, and `fixes-agreed.md` maps each one to the change that answers it. | WORLD | stipulated | REVISED | X001 |
| Y012 | `scripts/verify6.py` reads figures **out of the document text** and fails when they disagree with a value computed from the install, but it does **not** cover every figure the document prints. | DESIGN | stipulated | REVISED | X004 |
| Y013 | **Under half** of the printed figures are guarded, and the remainder are not all covered by anything else: a script is named about a dozen times against roughly three times that many unguarded figures, and some of the most recent additions carry neither a guard nor an attribution. | WORLD | numerical test | NEW | — |
| Y014 | `scripts/coverage6.py` measures coverage honestly — it corrupts each spec-printed figure whether the harness looks at it or not — and should be re-run rather than quoted, because the number moves with every edit to the document. | DESIGN | stipulated | NEW | — |
| Y015 | `scripts/mutate6.py` reports a higher score and is **not** coverage: it plants errors only in figures `verify6.py` already checks, so it cannot fail — the same circularity v4.0's harness had, recorded rather than quietly fixed. | WORLD | derivation | NEW | — |

## §1.1 — Trade direction (lines 57–164)

**UNCHANGED:** C005, C006, C010–C012, C019–C022, V005–V015, V017–V024, V026–V028, V031, V032,
V036, V037, W007–W011, W015–W022, X005, X006, X007, X012, X014, X015, X016, X017.
*(The properties preamble now names `measure6.py` in place of `v5measure.py`; per the conventions
that is not a proposition change.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y016 | The fallback branch fires only when every candidate is support-isolated with zero **post-peel** balance: the key reads the balance Phase 0 hands on, with each pendant's balance folded into its parent, so a map with non-zero raw balances can still reach the branch. | MODEL | derivation | REVISED | X008 |
| Y017 | On a connected core the branch needs the **folded** balance to vanish across the core — for a per-good graph, a component with no producer and no consumer; for the aggregate graph, each node's `Σ wealth^α_Φ` equal. | MODEL | derivation | REVISED | X009 |
| Y018 | ⚑ Uniform *per-province* wealth does **not** deliver that, because nodes hold between **0 and 72** counted provinces, so equal provinces make unequal node sums. | MODEL | file value | NEW | — |
| Y019 | Where the wealth key ties, the **node index** decides. | MODEL | derivation | REVISED | X010 |
| Y020 | §2.8 asserts containment over a set that includes the fallbacks, and the reason is **T3** — a fallback promotion that is a sink in neither the selected nor the promoted set — not the wealth tie, which is incidental to it. | DESIGN | derivation | REVISED | X011 |
| Y021 | The fallback branch is **not** the reason §2.4 requires a canonical node order; that requirement is stronger and is set by Phase 2. This withdraws the claim that the index tiebreak (or T3) carries the node-order requirement. | DESIGN | derivation | REVISED | X011, X151 |
| Y022 | On 1444 the pendant and fallback cases are empty and the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods, **1–8 sinks per good, mean 3.72**, zero fallbacks. | MODEL | numerical test | REVISED | X013, X145 |
| Y023 | The equality does not become a theorem by attaching conditions: "Phase 0 a no-op and no fallback firing" looks sufficient and is not — **T2** satisfies both and still breaks it. | MODEL | derivation | NEW | — |

## §1.2 — Supply (lines 166–177)

**UNCHANGED:** C023, C025–C028, V038–V041. No delta claims.

## §1.3 — Demand (lines 179–329) — full-strength extraction

**UNCHANGED:** C031, C032, C033, C035, C036, C039, W023, W024, W026, W030, W033, W042, W044,
W047, W051, X023, X024, X025, X026, X059, X060, X061, X062.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y024 | Wealth reads exactly **three** things about the province — its development, its trade good, and its own current condition — and nothing else. | MODEL | stipulated | NEW | — |
| Y025 | Two provinces with the same development, trade good and **condition** have the same wealth whoever owns them. (v3.0–v5.0 said "terrain, development and trade good".) | MODEL | derivation | REVISED | W025 |
| Y026 | Owner-agnosticism is true by construction because `base_tax`, `base_production` and the trade good are bare attributes of the place, so nothing about them needs classifying. | DESIGN | derivation | NEW | — |
| Y027 | v3.0 through v5.0 defended the property with a two-test classifier applied to a sweep of the install, which was wrong in **both independent audits** that examined it: v4.0's own repair harness passed it and v5.0's audit then refuted what that harness had passed. | WORLD | derivation | REVISED | X034 |
| Y028 | *What this gives up:* `gems`' `local_tax_modifier` and `incense`' `trade_value_modifier` are genuinely province-scoped and are **no longer read**, along with great projects, permanent province modifiers and the DLC state they depended on. | DESIGN | stipulated | REVISED | X035 |
| Y029 | The deleted apparatus covered **89 of the 2,472** counted provinces — 43 `gems` plus **31** `incense` plus 16 great-project and permanent-modifier provinces, less one that is both (province 542). | ENGINE | file value | REVISED | X036, X037, X038, X039 |
| Y030 | That count depends on the field: it is **87** under the withdrawn `is_city` filter, and 89 rather than 88 because province **4856** is one of the twenty whose good the engine rolls, and it rolled `incense`. | MODEL | numerical test | NEW | — |
| Y031 | `goods_produced(p) = GP_COEFF · base_production(p) · (1 + Σ province-state goods modifiers)` — no local flat goods-bonus term. | MODEL | derivation | REVISED | X018 |
| Y032 | `trade_value(p) = goods_produced(p) · price(good(p))`, ducats per year — the local trade-value-modifier factor is gone (restoring W028's form). | MODEL | derivation | REVISED | X019 |
| Y033 | `tax_value(p) = TAX_COEFF · base_tax(p) · (1 + Σ province-state tax modifiers)`. | MODEL | derivation | REVISED | X020 |
| Y034 | ⚑ **`GP_COEFF` is a shipped file value**: `common/static_modifiers/00_static_modifiers.txt` carries `provincial_production_size = { trade_goods_size = 0.2 … }`, localised "Base Production" — the same tooltip line it was measured off — so it is moddable and is **read at runtime**, not hardcoded. | ENGINE | file value | REVISED | W031, W032 |
| Y035 | `TAX_COEFF` is in no file that has been found — neither `defines.lua`, `common/defines/`, nor that static-modifier block — so it stays a measured constant carrying the observation that produced it. | ENGINE | file value | REVISED | W031 |
| Y036 | ⚑ The tax tooltip's schema is `Base: trunc(base_tax × 0.0833333) (Yearly base_tax)`: the parenthetical is `base_tax` itself and the `Base` line is its truncated twelfth. It is **not** twelve times the displayed figure, which would give 5.88 and 1.92 on the two observations. | ENGINE | engine test | REVISED | X021 |
| Y037 | v4.0 and v5.0 wrote the schema as `Base: X (Yearly 12·X)`, which is false on both of its own data points; v3.0 carries neither that schema nor the 0.6125 arithmetic. | WORLD | derivation | NEW | — |
| Y038 | ⚑§ The monthly production tooltip's `Trade Value` line is **consistent with** the annual-over-twelve relation on one observation, 3.52 → `+0.29`, which fixes the divisor only to within **(11.73, 12.14]**. | ENGINE | engine test | REVISED | X022 |
| Y039 | Both monthly figures being the annual value over twelve is what lets the annual forms add directly, and it is the **tax pair** that establishes it, at two development levels. | MODEL | derivation | REVISED | W036 |
| Y040 | ⚑§ **0.49 × 1.25 is 0.6125, which truncates to 0.61, not 0.62** — so the engine is not multiplying the displayed figure; it multiplies the untruncated monthly value (6 × 0.0833… = 0.49999…, × 1.25 = 0.62499…, displayed 0.62). | ENGINE | engine test | REVISED | X027 |
| Y041 | v4.0 and v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires rounding while §2.3 requires truncation; both cannot hold. | WORLD | derivation | NEW | — |
| Y042 | The Garnatah example establishes only the **ordering** — base from development first, percentage second — and nothing finer. | ENGINE | derivation | NEW | — |
| Y043 | Flat goods bonuses *would* add into `goods_produced` before the price multiply, but under §1.3 **no source grants one**, so the ordering is stated for the emitter's benefit and is not exercised by any province in the model. | MODEL | derivation | REVISED | X028 |
| Y044 | Province condition is the one thing besides development and the good that wealth reads: **four** static modifiers describe a province's own state, and all four are read from `common/static_modifiers/00_static_modifiers.txt`. | MODEL | stipulated | NEW | — |
| Y045 | ⚑ The four values: `devastation` `trade_goods_size_modifier = -2` scaled by the devastation level; `prosperity` `= 0.25`; `under_siege` `= -0.25`; `occupied` `= -0.5` **and** `local_tax_modifier = -0.5`. | ENGINE | file value | REVISED | X040 |
| Y046 | **No shipped file states that the devastation scaling is linear in the level**; the model assumes `-2 × level/100`, which is an assumption and not a file value, and `prosperity` is likewise applied as stated without a file confirming its direction. | MODEL | file value | NEW | — |
| Y047 | Only `occupied` touches the tax term; the other three reach `goods_produced` alone. | ENGINE | file value | NEW | — |
| Y048 | These four are what make the map answer to war — §1.2's volatility and §3.3's "a besieged province genuinely produces less" both rest on them, and §2.8's war rows are their test. | DESIGN | derivation | NEW | — |
| Y049 | ⚑ **Eleven counted provinces begin devastated at 1444** — Bohemia at 50, Erzgebirge and Moravia at 20 — and no province-history file says so: the devastation is applied by `on_startup`, which fires `flavor_boh.15` ("The Aftermath of the Hussite Wars"). | ENGINE | file value | NEW | — |
| Y050 | That devastation costs **13.40 ducats** across the eleven affected counted provinces (`measure6.py`). | MODEL | numerical test | NEW | — |
| Y051 | ⚑ The chain is `common/on_actions/00_on_actions.txt` → `on_startup_effect` → `common/scripted_effects/01_scripted_effects_for_on_actions.txt` → `country_event flavor_boh.15`. | ENGINE | file value | NEW | — |
| Y052 | **The start state is what the engine produces, not what the history files say**, and that costs three separate reads. | DESIGN | derivation | NEW | — |
| Y053 | ⚑ `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`, `flavor_geo.1` and others directly from its own `events = { }` list in `00_on_actions.txt` — a second path alongside the `on_startup_effect` chain that carries `flavor_boh.15`. | ENGINE | file value | NEW | — |
| Y054 | **Development itself does not move before the first tick:** the history parse matches the save on **2,472 of 2,472** provinces for `base_tax`, `base_production` and owner, and only `trade_goods` differs, on exactly twenty provinces. | MODEL | numerical test | NEW | — |
| Y055 | ⚑ `flavor_geo.1` does **not** carry `add_base_tax` — v6.0's first draft said it did. Its whole effect is legitimacy, a country modifier and a flag; those keys are in `flavor_geo.3`, which `on_startup` does not fire (a mission does). | ENGINE | file value | NEW | — |
| Y056 | ⚑ **`add_base_*` in a dated block before the start date accumulates**: province 1 (Uppland) has `base_tax = 5` undated plus 1 at `1436.4.28` and the game has 6. v5.0 and earlier overwrote instead of adding, silently dropping the grant. | ENGINE | file value | NEW | — |
| Y057 | ⚑ **`is_city = yes` is not a filter the engine applies:** 20 owned provinces omit or comment out the line — province 265 is one, and it is also one of the devastated eleven — and the engine treats them as cities. | ENGINE | file value | NEW | — |
| Y058 | The model counts a province when it has an owner and lies in a trade node: **2,472** provinces, not 2,452, and world wealth on that field is **10,607.40** annual ducats. | MODEL | stipulated | REVISED | W050, X113 |
| Y059 | ⚑ **Twenty counted provinces have no trade good in their history file** (`trade_goods = unknown`); the engine assigns one at start from each good's `chance = { }` block. | ENGINE | file value | NEW | — |
| Y060 | The model does not predict the draw — it **reads the good the engine actually rolled** and prices the province on that, as it does for development. | DESIGN | stipulated | NEW | — |
| Y061 | Pricing those twenty at zero instead understates world wealth by **12.70 ducats**. | MODEL | numerical test | NEW | — |
| Y062 | § On this save the twenty came up seven `fur`, five `grain`, three `wool`, two `livestock`, and one each of `cotton`, `incense` and `naval_supplies`, so the field is one sample; a different roll gives a slightly different field and nothing in the model depends on which one. | MODEL | numerical test | NEW | — |
| Y063 | The `TAX_COEFF = 1.0` reference condition is applied to **every** province the model counts: ownership is not modelled, so every province is treated as cored **and settled** — the `is_city = yes` premise is dropped. | MODEL | derivation | REVISED | X063 |
| Y064 | That is a modelling choice with a known cost: two readings, both on cored city provinces at `base_tax` 2 and 6, are all `TAX_COEFF = 1.0` rests on. | DESIGN | derivation | NEW | — |
| Y065 | ⚑ `base_tax` at 1444 runs up to **15** (province 1821), with total development reaching **33** there. | ENGINE | file value | NEW | — |
| Y066 | Owner-agnostic wealth removes **a large** source of hidden owner-dependence from the aggregate graph — not "the single largest", as v3.0 through v5.0 had it. | MODEL | derivation | REVISED | W052 |

## §1.4 — Market concentration (lines 331–341)

**UNCHANGED:** C040–C047. No delta claims.

## §1.5 — Goods without a graph (lines 343–392)

**UNCHANGED:** C048, C051–C056, V050–V058, W053, W182–W186, W188, W189, W191.
*(W189 now cites `common/prices/00_prices.txt` for coal's base price of 10.0 being the highest;
adding the file path is not a proposition change.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y067 | Measured: repricing to coal the 45 owned latent-coal provinces flips **10 of 159 `Φ_w` edges** and adds **214.60 ducats** to world wealth (`measure6.py`). The flip count returns to W187's value after v5.0 reported 29. | MODEL | numerical test | REVISED | X064 |
| Y068 | The counterfactual holds every non-repriced input fixed, which matters by more than rounding: province **4237** is both latent-coal and one of the devastated eleven, and a reprice that also drops its devastation measures coal activating **plus** one province healing — worth 2.40 ducats and 3 extra flips. | MODEL | numerical test | NEW | — |

## §1.6 — The aggregate graph (lines 394–552) — full-strength extraction

**UNCHANGED:** C059, C062, V063, V064, V212, V218, V221, W054, W055, W058, W063, W064, X067,
X087, X089, X090, X091, X095, X123.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y069 | **Both the sink count and the sink locations move with the wealth field, and `α_Φ` sets how sharply concentration is read** — the count is a function of the field **and** the constant. | MODEL | numerical test | REVISED | X065 |
| Y070 | At the stipulated α_Φ = 1.5 the 1444 field gives **two** sinks and a modestly grown Europe gives three or one, so neither the count nor the placement is fixed by the constant. | MODEL | numerical test | NEW | — |
| Y071 | v2.0–v4.0's "the count emerges from concentration exactly as per-good sink counts do" and v5.0's "the count is set by `α_Φ`" are wrong the same way. | WORLD | derivation | REVISED | X065 |
| Y072 | v2.1 chose the value with a target count in view — a calibration §2.3 withdraws **without replacing**; the band-table ground on which v5.0 retained 1.5 is withdrawn too. | WORLD | derivation | REVISED | X066 |
| Y073 | Measured: identical orientation at ×1 and above, **12 edge flips at ×10⁻²**, and **100 at ×10⁻⁶**, where the sink set also collapses to `{genua}`. | MODEL | numerical test | REVISED | X068 |
| Y074 | 1444's `b_w` has largest magnitude **0.0225**, so normalising into (−1, 1) scales it up and is safe. | MODEL | numerical test | REVISED | X069 |
| Y075 | Measured at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and `hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12 (restoring W059's figures). | MODEL | numerical test | REVISED | X070 |
| Y076 | **One of those two is a property of the world and the other is a property of the node ordering, and the difference matters more than the count.** | MODEL | numerical test | NEW | — |
| Y077 | Phase 2's b-flow is degenerate — many distinct supports carry the same optimal cost — so relabelling the nodes and re-running returns a **different optimal orientation**. | MODEL | numerical test | NEW | — |
| Y078 | Across **400 relabellings** (four seeds of 100, `α_Φ` and every input held fixed) the orientation changed **every time**, a mean of about **25 of 159** edges moved, and the sink set came back exactly as `{english_channel, hangzhou}` in **5 to 10 runs per hundred**. | MODEL | numerical test | NEW | — |
| Y079 | `hangzhou` was an end in **97 to 100 per hundred** relabellings and `english_channel` in **37 to 44**. | MODEL | numerical test | NEW | — |
| Y080 | The Asian end is the robust one — not invariant, since orderings exist where it loses its end, but near enough that it is a fact about that node. | MODEL | numerical test | NEW | — |
| Y081 | The European end is one of several the same world admits: `gulf_of_siam` held an end in about half the runs, `wien` in a third, `sevilla` in a fifth; the count itself ranged **1 to 5**, most often 2 or 3. | MODEL | numerical test | NEW | — |
| Y082 | Conditional on the node order: the sink set's membership and size, and everything derived from them — §2.4's end-flag list, and which European node holds an end in the Europe table. | MODEL | numerical test | NEW | — |
| Y083 | Not conditional over the same relabellings: the map is fully oriented (159/159) and acyclic every time, no fallback ever fires, and the LP objective is identical to **2.22e-16** — so these are different *optimal* orientations rather than different answers. | MODEL | numerical test | NEW | — |
| Y084 | Phase 1 selects `genua`; both sinks arrive by **stall promotion** and `genua` ends a transit node, so there are **2 promotions and 0 fallbacks**. | MODEL | numerical test | REVISED | X072 |
| Y085 | **Eight sources**, all in the bottom half of the wealth field, `c_w` ranks **44–75**, mean degree **3.1** against the map's 4.0 (restoring W060's figures; the seven named nodes of v5.0 are not enumerated). | MODEL | numerical test | REVISED | X073 |
| Y086 | Every node drains to a sink; acyclic, 159/159 oriented; the sink set is unchanged under ±1% wealth noise **on three seeds** — the "0 edge flips … across 5 seeds" of v5.0 is not restated. | MODEL | numerical test | REVISED | X074 |
| Y087 | Per good on the same field, **89.6%** of ordered node pairs (**5,663 of 6,320**) are connected by at least one good's directed path. | MODEL | numerical test | REVISED | X158 |
| Y088 | Agreement with the per-good graphs is **53.6%** of edge-goods (**52.3%** value-weighted). | MODEL | numerical test | REVISED | X075 |
| Y089 | The superseded marking-order aggregate scored **higher** on that measure, and no figure is maintained for it — §3.9 records why the trade was taken instead. | MODEL | numerical test | REVISED | X076 |
| Y090 | **`α_Φ = 1.5` is a stipulated design constant, exactly as `P₀ = 2.0` is** — superlinear so that a few very rich provinces outweigh a dense mediocre region, and round; chosen, not derived. | DESIGN | stipulated | REVISED | X083 |
| Y091 | **Every derivation previously offered for it is withdrawn**: v2.1 through v4.0 said it was calibrated to reproduce a two-sink 1444 map, and v5.0 said it sat in the widest sink-count band. | WORLD | derivation | NEW | — |
| Y092 | Scanned over **[1, 8]** rather than [1, 3] the widest band is **1.71** wide (**[3.50, 5.21]**, `{doab, genua, hangzhou}`), and 1.5's is not the widest by any margin. | MODEL | numerical test | NEW | — |
| Y093 | Across α_Φ = 1.00…8.00 at 0.01 the sink set is a step function, and α_Φ = 1.5 sits in the band **[1.38, 1.63], width 0.25**, which gives `{english_channel, hangzhou}`. | MODEL | numerical test | REVISED | X077, X078 |
| Y094 | Sampled at the six values v2 used, the count is non-monotone: **6 → 2 → 1 → 2 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}. | MODEL | numerical test | REVISED | X084 |
| Y095 | A warning to future revisers: the 1444 map has two ends and vanilla's authored map has three, and 1.5 must **not** be justified by that resemblance — that is the calibration §2.3 withdrew. | DESIGN | stipulated | NEW | — |
| Y096 | **Europe becomes the centre of trade as it develops** — the design claim §3.1's first goal asks the field to deliver. | DESIGN | stipulated | REVISED | X085 |
| Y097 | At 1444 the map already ends in the Channel and in Hangzhou; as European development compounds the Channel's basin grows and Asia's pole fades, and past a broad range of European growth Asia holds no end at all. | OUTCOME | numerical test | NEW | — |
| Y098 | The mechanism: wealth is linear in development, so developing a region moves its `c_w` share directly and `Φ_w`'s ends follow the wealth. | MODEL | derivation | NEW | — |
| Y099 | Observed with `europe.py` over **824** counted European provinces: ×1.02 gives `{english_channel, hangzhou, wien}`. | MODEL | numerical test | REVISED | X086 |
| Y100 | At ×2.00 European development the sink set is **`genua` alone**. | MODEL | numerical test | NEW | — |
| Y101 | Read the table as a direction rather than a trajectory, and on **one node ordering**: which European node holds an end at the smaller factors is ordering-dependent, so the direction is the claim and the membership is not. | MODEL | numerical test | NEW | — |
| Y102 | The ×2.00 row is the exception: `genua` held an end in **60 of 60** relabellings, so a single Mediterranean end under that much European growth is a property of the field rather than of the ordering. | MODEL | numerical test | NEW | — |
| Y103 | Because §1.3's wealth is linear in development, **scaling development and scaling wealth are the same operation here** — maximum difference 0.0 across the European set — so the distinction that made v5.0's version of this table wrong does not arise. | MODEL | numerical test | NEW | — |
| Y104 | The 1444 Silk Road route from Genoa to the Asian sink runs `genua → alexandria → aleppo → persia → lahore → **lhasa** → ganges_delta → burma → gulf_of_siam → canton → hangzhou`. | MODEL | numerical test | REVISED | X094 |
| Y105 | **No route leaves `english_channel` at all** — it is a sink with out-degree 0, so the Hansa and the Danube carry power *into* it, and v5.0's "from the Channel it is the Hansa and the Danube" describes a path that does not exist. | MODEL | numerical test | REVISED | X096 |
| Y106 | **No Europe→sink route passes the Cape of Good Hope**, checked from `genua`, `north_sea` and `english_channel`. | MODEL | numerical test | REVISED | X097 |
| Y107 | The Cape is a live `Φ_w` conduit, not an idle one: in-degree 1, out-degree 3, with **132 ordered node pairs** whose path runs through it (`measure6.py`), carrying Atlantic drainage into the Indian Ocean. | MODEL | numerical test | NEW | — |
| Y108 | v5.0's "nothing routes through the Cape" is false as a universal and was only ever checked on the Europe→sink routes. | WORLD | derivation | NEW | — |
| Y109 | In the per-good graphs the Cape also carries Asian spices to Europe; `Φ_w` models power, not cargo. The specific `malacca → cape_of_good_hope → …` route v5.0 quoted is no longer given. | MODEL | numerical test | REVISED | X098 |
| Y110 | Scaling the **22 European nodes** rather than European provinces makes `genua` the sole sink from about **×1.65**, and the 18-node western/central subset needs about **×2.15**. | MODEL | numerical test | REVISED | X099 |
| Y111 | The Cape of Good Hope reverses somewhere inside roughly **×2.9–×3.5** — bounded above as well as below, so a window and not a threshold, with edges that move with the field. | MODEL | numerical test | REVISED | X100 |
| Y112 | Dev-stacking a single node's top province concentrates the map on that node; extra sinks at intermediate boosts are expected behaviour, not noise. The `hangzhou`-specific ×10/×20/×30/×50 figures are dropped. | MODEL | numerical test | REVISED | X101 |

## §1.7 — Merchants (lines 554–580)

**UNCHANGED:** C067–C083, V066, V068, V069, V070, W065, W192, X102. No delta claims.

## §1.8 — Collection and transfer (lines 582–612)

**UNCHANGED:** C084–C102, V072, X103, X104. No delta claims.

## §1.9 — Trade power propagation (lines 614–623)

**UNCHANGED:** C103–C111, V073, W067, W068, W069. No delta claims. *(§1.9 still carries W067's
"descriptively false"; the hedge on that evidence is Y138 at §2.7.)*

## §1.10 — Direction-dependent systems (lines 625–681)

**UNCHANGED:** C112–C143, V074, V078, V079, V080, W070, W071, X105, X109, X110, X196.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y113 | **Banding absorbs very little chatter** — not "almost nothing absorbs threshold chatter", because banding is not the only damper. | ENGINE | derivation | REVISED | X106 |
| Y114 | ⚑ `TRADING_POLICY_COOLDOWN_MONTHS = 12` applies to **seven of the nine entries** in `common/trading_policies/00_trading_policies.txt` — five distinct policies, four with an `_upgraded` twin, plus Propagate Religion which has none — so four of the five families are rate-limited, including Propagate Religion; `maximize_profit` and `maximize_profit_upgraded` carry `cooldown = no`. | ENGINE | file value | NEW | — |
| Y115 | ⚑ `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` and `TRADE_COMPANY_COOLDOWN = 60` are shipped defines. | ENGINE | file value | NEW | — |
| Y116 | At those three, a flickering power share does not translate into a flickering *effect*; what is left exposed is everything without a cooldown, which is most of the ladder. | ENGINE | derivation | NEW | — |
| Y117 | Measured on the 1444 start: the caravan cap of 50 is **9.4% to 47.0%** of an inland node's total trade power, median **21.6%** over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. | MODEL | numerical test | REVISED | X107 |
| Y118 | As a share of the node's total **after** the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, median 17.7%; v5.0 quoted those under the first description, which cannot be right since 8.6% of 532.0 is 45.8 rather than 50. | WORLD | derivation | NEW | — |
| Y119 | On §2.2's derived 25-node inland basis the median is **21.3%** pre-grant, or 17.5% after. | MODEL | numerical test | REVISED | X108 |

## §1.11 — Treasure fleets · §1.12 — What the game displays (lines 683–713)

**UNCHANGED:** C144–C148, C149–C165, V049, V065, V081. No delta claims.

## §2.1 — Shape (lines 719–736)

**UNCHANGED:** C167–C184, V082–V085, W072, W073. No delta claims.

## §2.2 — Solver (lines 738–781)

**UNCHANGED:** C185–C209, V091, V092, V229, W075, W076, X115.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y120 | Solver item 4 computes `TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production · (1 + province-state goods modifiers) · price`, with no autonomy, efficiency, ideas or owner terms; the only modifiers read are the four province-condition ones, and at 1444 only `devastation` is live, on eleven provinces. | DESIGN | stipulated | REVISED | X111 |
| Y121 | Measured on the reference implementation (scipy/HiGHS plus the deterministic sweep, one machine): **of order 0.1 s for all 29 goods, and single-digit milliseconds per good on average** — and that is the whole of the claim. | MODEL | numerical test | REVISED | X114 |
| Y122 | Repeated 12-run experiments on one machine do not reproduce each other closely enough to support anything finer — three replicates gave per-good averages spanning **3.5–10.5, 3.5–10.8 and 3.1–4.7 ms** — so no range is quoted, because the quantity measured is a machine and a scheduler rather than the algorithm. | MODEL | numerical test | NEW | — |
| Y123 | v5.0 quoted "0.17–0.21 s for all 29 goods"; across three replicates of twelve runs, the number of runs landing inside that interval was **1, then 0, then 0**. | WORLD | numerical test | NEW | — |

## §2.2a — What map this is for (lines 783–823)

**UNCHANGED:** W077–W085, W088, X116.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y124 | Where Phase 0 acts, free-edge **determinism** is unaffected but the **index-independence** half is not: the key reads the post-fold balance β, so peeling can create exact ties the raw balances do not have, and the 1444 measurement does not transfer. | MODEL | derivation | REVISED | X117 |

## §2.3 — Constants (lines 825–871)

**UNCHANGED:** C211–C227, V094, W089, W090, W091, W097, W098, the DLC-third-axis claim, X118,
X119, X120, X121. *(The two coefficients' split provenance is Y034/Y035 at first appearance in
§1.3; §2.3 restates it and adds the tabulated measurements, which are unchanged.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y125 | v3.0 through v5.0 said neither wealth coefficient was in a file, and shipped a whole-install modifier sweep that walked past the block holding one of them. | WORLD | derivation | NEW | — |
| Y126 | **Every derivation previously offered for `α_Φ` is withdrawn, and neither is a reason:** the first fits a constant to one date, and the second depended on where the α scan was truncated. (v5.0's rejection ground — that the window is narrower than the uncertainty in its own edges under noise — is not the ground given.) | DESIGN | derivation | REVISED | X122 |

## §2.4 — The tradenodes file (lines 873–928)

**UNCHANGED:** C228–C233, C235–C242, V095, V148, W099, W100, W102–W107, W114, X124, X127.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y127 | The canonical order must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks ties in. | DESIGN | derivation | NEW | — |
| Y128 | Measured on 1444: relabelling the nodes and running end-to-end changed the orientation on **580 of 580** runs (29 goods × 20 relabellings), **always** by returning a different optimal vertex and **never** by a sweep tiebreak, with a mean of **22.1 of 159** edges moving and the objective identical to **8.9e-16**. | MODEL | numerical test | NEW | — |
| Y129 | Permuting only the **arc presentation order** with node labels held fixed changes the optimal support on **10 of 10** goods tested, with objective gaps ≤ **1.8e-15** (`measure6.py`). | MODEL | numerical test | NEW | — |
| Y130 | Twenty-two flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event. | MODEL | derivation | NEW | — |
| Y131 | Everything §1.6 and §2.8 report about stability is measured **at fixed node order**; re-order the same world and the map moves, with `α_Φ` and every input held fixed. | MODEL | numerical test | NEW | — |
| Y132 | The specific 580/580 result is HiGHS-specific in its detail but not in kind — any simplex returns *a* vertex of a degenerate optimal face. | MODEL | derivation | NEW | — |
| Y133 | Making the orientation independent of presentation order would need a tie-breaking objective — a lexicographic secondary cost, or a strictly convex perturbation — which is a design change and is not adopted here. | DESIGN | derivation | NEW | — |
| Y134 | §1.1's priority key ties in **more places than §1.1 documents**: besides the free-edge sweep it decides Phase 1's within-cluster argmin, the stall promotion's identical form, and the top-k cut when two clusters carry equal mass. | MODEL | derivation | NEW | — |
| Y135 | **None of them fires on 1444** — zero exact `(DEF, β)` ties on free edges across 29/29 goods, zero within-cluster β ties, zero tied cluster masses — so no measured figure depends on them. | MODEL | numerical test | NEW | — |
| Y136 | The end-flag list is **a function of the canonical node order required by item 1, not of the world alone**; fix the order, emit, and keep it, because changing it changes the flags without anything in the world changing. | DESIGN | derivation | NEW | — |
| Y137 | End flags at 1444 in the shipped order: **two** end nodes, `english_channel` and `hangzhou`, against vanilla's three. | DESIGN | numerical test | REVISED | X126 |

## §2.5 — Runtime attachment · §2.6 — Writing to the engine (lines 930–964)

**UNCHANGED:** C243–C250, C251–C272. No delta claims.

## §2.7 — Probes (lines 966–1010)

**UNCHANGED:** C274–C293, V098–V101, W108–W114.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y138 | § Probe 15's finding is **one observation on one node** — enough to retire §3.16's cautionary case and *not* enough to promote §1.9's "every immediately upstream node" to a measurement; v3.0 through v5.0 said the rule was "correct as written and gains no qualifier". | ENGINE | engine test | REVISED | W067 |

## §2.8 — Validation (lines 1012–1049)

**UNCHANGED:** C298–C342, V109–V112, W116, W117, W119, W195, X128, X133, X134, X135, X136, X137.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y139 | Most goods, 1444: sinks are **1 to 8** per good; high-demand nodes are sinks at **16.8%** in the top demand decile against 6.9% in the bottom. | MODEL | numerical test | REVISED | X129 |
| Y140 | The Razed-China row is **ordering-robust where §1.6's sink membership is not**: it turns on `hangzhou` holding an end, which it does under every relabelling tried. | MODEL | numerical test | NEW | — |
| Y141 | Zeroing `hangzhou`-node development moves the `Φ_w` sinks from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`, with **22 of 159** edges flipping. | MODEL | numerical test | REVISED | X130 |
| Y142 | `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth **226.7 against 143.0**, and it holds the richest single province **the model counts**. The `c_w` rank-1-against-31 comparison is not restated. | MODEL | numerical test | REVISED | X131 |
| Y143 | Zeroing `beijing` **also** moves the map — **15 flips** — because deleting a percent of world wealth renormalises `c_w` everywhere; what separates the two cases is which node keeps its end, not whether the map moves. | MODEL | numerical test | REVISED | X132 |

## §2.9 — Build order (lines 1051–1061) · §3.1 — Goals (lines 1065–1075)

**UNCHANGED:** C343–C352, C353–C365, V113, X138. No delta claims.

## §3.2 — Why a flow and a drainage sweep (lines 1077–1156)

**UNCHANGED:** C366, C370–C375, C383–C385, V115, V116, V118–V122, V124, V128–V131, W120, W123,
W125–W128, X139, X141, X146, X147, X148, X149, X150.
*(§3.2's post-fold and multiple-tie-site cautions are Y124 and Y134 at first appearance; its
"conditions are necessary, not sufficient" argument is Y023.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y144 | **What the ratio metric cannot see is the thing the diagnosis rests on:** a max/min contrast ratio over *producing* nodes is blind to sparsity by construction, and on the contrast metric itself the demand side is the wider one. v5.0's 36-against-482.2 spices figures are not restated. | MODEL | derivation | REVISED | X140 |
| Y145 | Better wealth inputs move Genoa to a *co-*sink at **roughly ×1.7** without making demand the determinant of placement; the ×1.720 figure is no longer given. | MODEL | numerical test | REVISED | X142 |
| Y146 | Moving the spice sink to a Chinese node takes a multiple of that node's demand in the region of **3.6–4.9×**: `beijing` **3.61×**, `hangzhou` **4.12×**, `xian` **4.60×**, `canton` **4.77×**. The paired world-demand-share percentages are dropped. | MODEL | numerical test | REVISED | X143 |
| Y147 | The multiple a node needs and the share of world demand it then buys do not line up end to end, because the share depends on where the node started; other nodes in the region need more still. The `girin`/`yumen`/`chengdu`/`lhasa` 4.0–10.8× figures are dropped. | MODEL | derivation | REVISED | X144 |

## §3.3 — Why wealth, and why per province (lines 1158–1210)

**UNCHANGED:** C386–C406, C408, C412, C413, V132, V133, V135, W132–W139. No delta claims.

## §3.4 — Why supply is pre-modifier (lines 1212–1220)

**UNCHANGED:** C415–C423, V137, V139, W140, W141, W142.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y148 | In v1, substituting production income broke the α = 1 identity, measured as orientation agreement **collapsing to well under half the map** — the 159/159 → 68/159 figures are no longer given. | MODEL | numerical test | REVISED | V138 |

## §3.5 — Why α is anchored absolutely (lines 1222–1256)

**UNCHANGED:** C427–C442, V140–V144, V147, X152, X153, X156, X157.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y149 | ⚑ **`change_price` values are fractions of the good's base price, not ducats**, and the shipped save `tutorial/eu4_tutorial_chapter10.eu4` settles it: `paper` sits at `current_price=4.375` on a base of 3.5 (× 1.25, not + 0.25) and `gems` at 5.000 on a base of 4.0. | ENGINE | file value | NEW | — |
| Y150 | The install carries **161 textual** `change_price` blocks — 93 in `events/`, 14 in `missions/`, 1 in `common/`, 53 in `history/` of which 13 are negative (all in `history/countries/HAB - Austria.txt`), and **none in `decisions/`**. | ENGINE | file value | REVISED | X154 |
| Y151 | ⚑ **Ten of the 161 never execute:** four sit inside `effect_tooltip = "…"` strings, three inside the `effect = "…"` string of a `country_event_with_effect_insight`, and three inside `tooltip = { }` display wrappers, so **151 are executable**. | ENGINE | file value | NEW | — |
| Y152 | Six of the seven quoted blocks duplicate a block already counted in `events/`, and the seventh names a price key no event in the install ever sets. | ENGINE | file value | NEW | — |
| Y153 | All ten are positive and every negative block in the install is executable, so the 13/2/4/11 partition is identical under either census. | ENGINE | derivation | NEW | — |
| Y154 | v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them; **both were wrong about which number was the executable one**. | WORLD | derivation | REVISED | X155 |
| Y155 | v5.0 also claimed the scan was "guarded by a per-file count assertion" — there was no assertion anywhere in its toolchain; `verify6.py` now carries the guard. | WORLD | derivation | NEW | — |
| Y156 | The reason a plain parse misses these is mechanical: `pdx.py` tokenises a quoted string as one opaque unit, so a `change_price` inside a tooltip string is invisible to the walker. | MODEL | derivation | NEW | — |

## §3.6 — Why no hysteresis, and why there is no ε (lines 1258–1288)

**UNCHANGED:** C443–C446, C449, C452, V152, V154, W147–W152. No delta claims.

## §3.7 — Why eligibility is per good (lines 1290–1296)

**UNCHANGED:** C463–C473. No delta claims.

## §3.8 — Why gates evaluate true (lines 1298–1310)

**UNCHANGED:** C474–C497, V155–V158, W154. No delta claims. *(The 89.6% reachability census is
Y087 at first appearance in §1.6.)*

## §3.9 — Why `Φ_w` is the installed graph (lines 1312–1350)

**UNCHANGED:** C502, C505–C510, C512, V160, V161, V162, V228, X161.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y157 | `genua`, `gulf_of_siam` and `sevilla` rank **4th, 3rd and 7th** by node wealth on the corrected field (`mexico` is 2nd) — **296.0, 297.9 and 266.5** against `english_channel`'s 316.6, **which is a sink**. | MODEL | numerical test | REVISED | X159 |
| Y158 | `Φ_ord` scores **higher** than `Φ_w` on self-coherence — the cost of the trade, not disputed — and was superseded on design grounds: its ends are scheduling artifacts rather than places, a majority terminate no good at all, none of the demand capitals is among them, and the end count does not concentrate as demand concentrates. **No figure is maintained for it.** | MODEL | numerical test | REVISED | X160 |
| Y159 | v2.1 through v4.0 justified the adoption by "two vanilla-like ends at 1444" — a resemblance to vanilla's authored map. That is not the argument and should not be revived **even though the 1444 field again gives two ends**, because the count is a property of the field, not of the operator. | WORLD | derivation | REVISED | X162 |
| Y160 | What the trade costs is self-coherence with the per-good graphs; what it buys is one operator, one set of guarantees, and ends that sit where the wealth is. The "7.8 points" figure is withdrawn. | DESIGN | stipulated | REVISED | X163 |

## §3.10 — Why the engine's economy is overwritten (lines 1352–1370)

**UNCHANGED:** C513–C521, C523–C525, C528–C530, X164, X165, X167, X172.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y161 | Across Sevilla, Genoa, Champagne, Malacca and the Gulf of Siam on each node's real 1444 country table, the two income forms agree to a worst relative disagreement of 0 to 3.7e-16 — **one to three** units in the last place, not "at most one". | MODEL | numerical test | REVISED | X166 |
| Y162 | Reading the one installed graph leaves the propagated term good-independent, so the identity **holds by construction**, and in doubles to within one to three units in the last place. | MODEL | derivation | REVISED | X168 |
| Y163 | `gulf_of_siam`'s 29 goods leave it by **seven** distinct downstream sets. | MODEL | numerical test | REVISED | X169 |
| Y164 | **Per-good propagation does not break the identity.** Define `ps̄_C = Σ_g v_g·cs_g·ps_C(g) / Σ_g v_g·cs_g` — the per-good shares weighted by *collected* value — and `collect_pool · ps̄_C = income_C` follows algebraically, with `Σ_C ps̄_C = 1`, so one scalar per node still reproduces every collector's income exactly. | MODEL | derivation | NEW | — |
| Y165 | Both inputs to `ps̄_C` already exist per good at write time, and §2.6 sums exactly them into `collect_pool`. | MODEL | derivation | NEW | — |
| Y166 | **The real cost is that `ps̄_C` is not derivable from trade power alone:** it is value-weighted, so installing it means writing a country a fictitious per-node trade power whose ratio happens to equal it, and every other consumer of that power field then reads the fiction. | MODEL | derivation | NEW | — |
| Y167 | That is a claim about what the engine exposes, not about a magnitude, and **no figure of the document's own is quoted**, because the identity holds and the objection is structural. | DESIGN | stipulated | REVISED | X170, X171 |
| Y168 | Every magnitude previous versions quoted was an artifact of substituting some other weighting: v1–v4.0's "5.96 ducats on a node paying ~250", v4.0's 0.41%, v5.0's "redistributive and single-digit percent", and v6.0's first draft's "at most 0.1%". | WORLD | derivation | REVISED | X174 |
| Y169 | No node in the model has local trade value near 250; the "largest is 112.6" figure is no longer maintained. | MODEL | numerical test | REVISED | X173 |

## §3.11 — Why caravan power needs a condition added · §3.12 — Why treasure fleets are always granted (lines 1372–1410)

**UNCHANGED:** C531–C547, C556–C560, V163–V172. No delta claims.

## §3.13 — Open questions (lines 1412–1466)

**UNCHANGED:** C561–C585, V173, V174, V175, V178, V181, V182, V183, W043, W164, X175, X177,
X178, X179, X180, X183.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y170 | The one open wealth question is now a **design** question, not a classification one: *should any source beyond province condition be allowed to multiply `goods_produced`?* | DESIGN | stipulated | REVISED | X176 |
| Y171 | `trade_goods_size` and `trade_goods_size_modifier` are granted in buildings, event modifiers, great projects, static and province-triggered modifiers, holy orders, state edicts and trade-company investments. | ENGINE | file value | REVISED | X176 |
| Y172 | v3.0 through v5.0 tried to admit the province-scoped subset by rule; that rule was wrong in both independent audits that examined it, which is why v6.0 drops it. | WORLD | derivation | NEW | — |
| Y173 | Re-admitting any of those sources re-admits the maintenance burden with it, so the question to settle first is whether the fidelity is worth it — the whole set was worth 105.30 ducats, about one percent of world wealth either way the ratio is taken. | DESIGN | derivation | NEW | — |
| Y174 | Under the calibration's α = 16 the cloves demand order is `hangzhou`, `beijing`, `doab`, and the sink lands on a high-demand node rather than a geographic accident. v5.0's "Deccan is demand rank 2 / Beijing rank 3" framing is replaced. | MODEL | numerical test | REVISED | X181 |
| Y175 | `hangzhou`, not Beijing, holds the richest single province; the 30.4-against-19.5 figures are no longer maintained. | MODEL | numerical test | REVISED | X182 |

## §3.14 — AI merchant assignment (lines 1468–1486)

**UNCHANGED:** C586–C624, X184. No delta claims.

## §3.15 — Rejected (lines 1488–1600)

**UNCHANGED:** C625–C672 as carried by v2, V184–V188, V192–V199, V226, V227.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y176 | §3.15 **does not maintain a copy** of the supply/demand contrast measurement; §3.2 carries it, and the 4–97 against 211–20,400 figures are dropped from this entry. | MODEL | derivation | REVISED | X185 |
| Y177 | `cloves` has a single producer and so **no contrast to measure at all**, which is the sparsity point in miniature. | MODEL | numerical test | NEW | — |
| Y178 | v3.0 **and v4.0** repeated the 10⁷ / 10²–10³ ratio here while **v4.0's own §3.2** was withdrawing it. | WORLD | derivation | REVISED | X186 |
| Y179 | Ranked orientation's win and loss are now stated as directions with no figures: it puts a far higher share of top-demand nodes in its sink sets than DRAIN does, strands a large share of world demand, leaves orphan sinks a good cannot reach, posts net-producer sinks where DRAIN, LAP and FLOW post none, and keeps several times DRAIN's sinks per good. | MODEL | numerical test | REVISED | X187, X188 |
| Y180 | Seeded basin growth leaves demand **unserved at every tuning tried**; the 88.4% best-tuning reach figure is dropped. | MODEL | numerical test | REVISED | X189 |
| Y181 | The 3-mass gravity kernel **reproduces whatever end count it is seeded with while γ is small enough, and loses that property as γ approaches 1**; no agreement percentages or end counts are maintained. | MODEL | numerical test | REVISED | X190 |
| Y182 | Pinned-count wealth fields are rejected on three grounds, **none of which is numeric**: the end count is pinned by fiat, a second operator with its own reach knob γ is needed, and a pure `wealth^α` comparison with no reach term does not concentrate ends because a local wealth maximum survives every positive α. | DESIGN | derivation | NEW | — |

## §3.16 — Evidence standard (lines 1602–1686)

**UNCHANGED:** C677, C680–C682, C684, C685, V200–V203, V206–V210, W173–W181.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y183 | Failure mechanism 3: implemented as written, the α = 1 identity's **residual reached 1e-5 against v1's ε of 1e-6**, and would have been diagnosed as a solver bug. (v1–v5.0 said only "the identity failed at 1e-5".) | MODEL | numerical test | REVISED | V204 |

---

# Prior IDs this delta strands

**38 X IDs are withdrawn** — deleted with the apparatus they described, or stated to be wrong,
with no successor proposition. Recorded so a later audit does not go looking for them.

| Withdrawn | What it said | Where v6.0 drops it |
|---|---|---|
| X003 | the whole-install classification moves the aggregate graph from two 1444 sinks to one | §1.6 reports two sinks again (Y075); the one-sink result and its explanation are gone |
| X071 | v2–v4's two-sink result was measured on a field missing sixteen provinces | same passage; the parenthetical is deleted |
| X029 | fifteen 1444 provinces carry a flat goods bonus in the additive block | §1.3 states that **no** source under v6.0 grants a flat bonus (Y043) |
| X030, X031 | the locality test and the wealth test | §1.3 deletes the two-test classifier (Y003) |
| X032 | the engine's trade-good data model is one *instance* of the locality test | same |
| X033 | the tests are applied to the whole install, not one file | same |
| X041, X042 | glass and chinaware are local but do not enter wealth | same; only §3.13's `local_production_efficiency` finding survives, as X177 |
| X043 | 361 provinces carry a centre of trade at 1444, and no CoT level grants a key wealth reads | same |
| X044, X045 | `production_leader` and `bonus_from_merchant_republics` are not local | same |
| X046 | buildings are local by the test and empty at 1444 | same |
| X047 | `terrain.txt` and the climate static modifiers grant only non-wealth keys | same |
| X048, X049, X050, X051, X052, X053 | the great-project rule, its 85-of-130 gate count, the six carrying projects, province 1821 as richest, and the `starting_tier` argument | same |
| X054 | the ten permanent province modifiers enumerated | same |
| X055, X056, X057 | the Leviathan gate on `stora_kopparberget_modifier`, its 3.0-vs-5.0 consequence, and the Leviathan-installed provenance of every wealth figure | same; §2.3's DLC-third-axis claim survives on other grounds |
| X058 | glass and chinaware are the whole of the rule-versus-vocabulary tension | same |
| X079, X080, X081, X082 | the three other α_Φ bands and the [1.406, 1.424] window | §1.6 reports only 1.5's band and the widest band over [1, 8] (Y092, Y093) |
| X191 | v2.1–v4.0 put the gravity kernel's best agreement at γ = 0.97 and said the five- and six-mass fields give four ends at γ = 0.9 | §3.15's gravity entry maintains no figures at all (Y181), so the correction to them goes with them |
| X192, X193, X194, X195 | the 8-seed noise analysis of that window and the principle drawn from it | same passage, deleted with the band table |
| X088 | "what the model claims here is the threshold, not the size of the historical edge — 2% is enough" | §1.6's Europe table is read as a direction, and §0's no-absolutes convention forbids the threshold form |
| X092 | developing the nine Lowland provinces by ×1.20 makes `english_channel` a sink through ×10 | deleted from §1.6 |
| X093 | ±2% random noise leaves the sink set unchanged but +2% to Europe changes it | deleted; only the ±1%/three-seed statement survives (Y086) |
| X112 | the solver reads local modifiers from the whole-install classification — 16 provinces beyond the two trade goods | §2.2 item 4 now reads only the four province-condition modifiers (Y120) |

**Not stranded, though a reader might expect it:** X127 (the end count is read from the solve, not
assumed) survives at §2.4 item 2; W071 survives at §1.10 and is still typed `UNSOURCED` in
`claims-v3.md`, the re-typing `claims-v5.md` recommended having not been applied here either;
X136 and X137 (the two-check sink assertions) survive verbatim at §2.8.

---

# † Unresolvable IDs

**None.** Every `Replaces` target in this delta resolves to a specific C, V, W or X ID. Two
targets are worth flagging as judgement calls rather than unresolved:

- **Y138** replaces **W067**, whose first clause ("the tooltip's receiving-side qualifier is
  descriptively false") still stands verbatim at §1.9. Only the second clause — "§1.9's 'every
  immediately upstream node' is correct as written and gains no qualifier" — is revised, and it is
  revised at §2.7 rather than at §1.9. Recorded against W067 because that is where the sentence
  entered.
- **Y029** collapses four v5.0 rows (X036–X039) into one province-count row, because v6.0 no
  longer separates the great-project and permanent-modifier counts.

**Three v5.0 figures return to a pre-v5.0 value** rather than moving on, which the `Replaces`
column cannot show on its own: Y067's coal flip count (10 of 159) restores **W187**, Y075's `c_w`
and node-wealth ranks restore **W059**, and Y085's source count, rank band and mean degree restore
**W060**. Each is recorded as REVISED against the v5.0 row it displaces.
