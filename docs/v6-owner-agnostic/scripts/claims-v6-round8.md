# Claim Inventory Delta — Per-Good Trade Network Spec v6.0

Extracted from `per-good-trade-spec.md` (v6.0, **1,728 lines / 150,902 bytes** as measured;
`changes-v6.md` says 1,729) as a **delta against
`../v5-owner-agnostic/claims-v5.md`** (X001–X196), which is a delta against
`../v3-owner-agnostic/claims-v3.md` (W001–W195), `../v2-drain/claims-v2.md` (V001–V230) and
`../v1-laplacian/claims.md` (C001–C685). Extraction only: nothing here is validated, corrected or
graded. What each row records is what the document asserts, how the assertion is typed and sourced,
and how it relates to the prior inventory.

**Method.** The v6.0 spec was read in full, and `claims-v5.md` was read in full (header and all 196
claim rows). To fix NEW / REVISED / UNCHANGED without trusting any prose account of the edits, the
**v5.0 → v6.0 text diff was computed directly** (paragraph-level, then word-level inside each
changed group): **33 groups replaced, 0 inserted, 0 deleted**, which is also what `changes-v6.md`
reports. Every paragraph outside those 33 groups is byte-identical to v5.0, so any prior ID whose
supporting sentence sits in an untouched paragraph is UNCHANGED by construction. `claims-v3.md`,
`claims-v2.md` and `claims.md` were grepped to resolve specific W/V/C IDs (W014, W025, W031, W032,
W036, W050, W052, W063, W067, W189, V138, V204 among them). `changes-v6.md` was used only to locate
changed passages; **no row below is taken from it**, and where its section labels and the diff
disagree the diff was followed.

**ID prefix.** v1 used `C`, v2 used `V`, v3 used `W`, v4 got none, v5 used `X`. **v6 uses `Y`**,
numbered in document order.

**Statuses.** UNCHANGED — the same proposition as an existing C/V/W/X ID; the old ID is recorded in
the section header and **no Y ID is issued**. REVISED — the proposition changed; a Y ID with the old
ID(s) in `Replaces`. NEW — no counterpart in any prior inventory. A proposition stated in two
sections keeps one ID at first appearance, and the later restatement is noted in the section it
appears in. Re-attributing a figure to a new script, or adding a file path to a claim whose content
is unchanged, is **not** a proposition change.

**Vocabularies carried over.** Type: ENGINE / MODEL / DESIGN / OUTCOME / WORLD. Provenance:
stipulated / derivation / file value / numerical test / engine test / prose source /
verified (method unstated) / UNSOURCED. `numerical test` (a solver experiment) and `engine test`
(an observation of EU4 actually running) are kept strictly distinct; a read of a **save file** is
`file value`, as in v5.

**Markers.** **⚑** a row that introduces an engine fact no prior inventory carried. **§** a row
whose stated evidence is a single observation. **†** a `Replaces` target believed to exist but not
pinned to a specific ID.

---

# Summary

**206 delta claims extracted, Y001–Y206**: **98 NEW, 108 REVISED**, replacing **106 distinct prior
IDs** — 95 X, 9 W (W014, W025, W031, W032, W036, W050, W052, W063, W067) and 2 V (V138, V204). A
further **930 prior IDs are carried UNCHANGED** (594 C, 155 V, 116 W, 65 X) and are listed in the
section headers rather than as rows; as in v5.0, the C and V figures are whole ranges inherited from
the earlier inventories' own UNCHANGED lists.

v6.0 is not a small revision. Three of its four largest changes delete propositions rather than
correct them — the two-test modifier classifier and its whole-install sweep (§1.3), the α_Φ band
table (§1.6), and every maintained figure for a rejected operator (§3.9, §3.15) — and the fourth,
the node-order/degeneracy result, adds a class of claim the document did not previously contain.

### Delta claims by status and Type

| Type | NEW | REVISED | Total |
|---|---|---|---|
| MODEL | 35 | 64 | 99 |
| DESIGN | 22 | 20 | 42 |
| ENGINE | 25 | 12 | 37 |
| WORLD | 16 | 12 | 28 |
| OUTCOME | 0 | 0 | 0 |
| **Total** | **98** | **108** | **206** |

### Delta claims by Provenance

| Provenance | Count |
|---|---|
| derivation | 71 |
| numerical test | 68 |
| file value | 33 |
| stipulated | 28 |
| engine test | 4 |
| verified (method unstated) | 2 |
| prose source | 0 |
| UNSOURCED | 0 |
| **Total** | **206** |

**No row carries UNSOURCED provenance.** Two rows carry `verified (method unstated)` — Y015 (the
279–326 token count) and Y017 (which figures carry a script attribution) — because the document
states a measurement over its own text without naming the instrument that produced it.

**25 rows are marked ⚑** — engine facts no prior inventory carried, and **all 25 are NEW or REVISED
rows carrying a fact class the document did not previously contain**. Seventeen are in §1.3, which
is where the start-state reads (`on_startup` devastation, dated `add_base_*`, the `is_city` filter,
the twenty rolled trade goods), the `unrest` row and `GP_COEFF`'s file location all land. The other
eight: §1.10's three trading-policy cooldown defines (3), §3.5's `change_price`-as-fraction finding,
its ten never-executing blocks and wool's second negative key (3), §3.3's `sea_starts` clarification
(1), and §3.13's widened list of `trade_goods_size` grantors (1).

**Three rows are marked §** — Y044 (the production tooltip's divisor, one observation),
Y046 (Garnatah's 0.62, one observation) and Y151 (probe 15's propagation reading, which the
document itself now scopes to "one observation on one node"). Down from v5.0's five, because §1.3's
tooltip arithmetic gained a second data point and §1.10's `highest_power` row was already at 79 of
79 nodes.

### Where the delta concentrates

| Section | Y rows | What drove it |
|---|---|---|
| §1.3 Demand | 48 | wealth becomes development + good + condition; the classifier deleted; three start-state reads corrected; the `unrest` row added |
| §1.6 Aggregate graph | 44 | two sinks again, the 800-relabelling ordering result, the band table replaced by one band, the Europe table restated directionally, the Cape and Channel routes corrected |
| §0 Front matter | 18 | the R1/R2/R3 conventions, the apparatus cost, the harness's own coverage limits |
| §2.4 Tradenodes file | 13 | Phase 2's degeneracy as the reason for a canonical node order, 400 of 400, 580 of 580, the ULP figure |
| §3.5 α anchoring | 10 | `change_price` as a fraction, the ten never-executing blocks, wool's second negative key |
| §3.10 Income factoring | 10 | the argument rebuilt on an identity, every magnitude withdrawn |
| §1.1 Trade direction | 9 | the fallback branch's post-peel condition; the equality's status |
| §3.2 Why a flow and a sweep | 8 | the contrast metric withdrawn, the Chinese-sink multiples regenerated as wealth multiples |
| §1.10, §3.15 | 7 each | the cooldown defines and the caravan re-measurement; the graveyard's figures deleted |
| §2.2, §3.9, §3.13 | 6 each | the (c) field's wealth and solve cost; `Φ_ord` under relabelling; the open question becomes a design question |
| §2.8 | 5 | regenerated rows plus the ordering-robustness note on razed China |
| §1.5, §2.3 | 2 each | the coal counterfactual; the coefficients' split provenance |
| §2.2a, §2.7, §3.3, §3.4, §3.16 | 1 each | |
| §1.2, §1.4, §1.7–§1.9, §1.11, §1.12, §2.1, §2.5, §2.6, §2.9, §3.1, §3.6, §3.7, §3.8, §3.11, §3.12, §3.14 | 0 | untouched by the diff (§3.8's one figure is Y097 at first appearance in §1.6) |

---

## §0 — Front matter (lines 1–59)

**UNCHANGED:** C002, C003, C004, V001 *(via §2.5)*, V002, V003, W001, W002 *(v6.0 keeps v3.0's
owner-agnostic wealth)*, V004 *(the v1 audit fold-through)*, W005 *(via §2.7)*.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y001 | v6.0 makes owner-agnosticism **true by construction** rather than a property defended by a rule that has to be policed. | DESIGN | stipulated | NEW | — |
| Y002 | The substantive change is to §1.3: **wealth is a function of the province's development, its trade good and its own current condition, and of nothing else.** | DESIGN | stipulated | REVISED | X002 |
| Y003 | The two-test modifier classifier and everything it governed — trade-good modifiers, great projects, permanent province modifiers, buildings, centres of trade, the DLC conditionality — are deleted, along with the whole-install sweep that maintained them. | DESIGN | stipulated | REVISED | X002, X033 |
| Y004 | The two-test classifier is **v4.0's**; v3.0 used a structural rule about which block of a trade-good definition a modifier sits in; the whole-install sweep is **v5.0's alone**. | WORLD | derivation | NEW | — |
| Y005 | On the 1444 start that apparatus was worth **105.30 ducats** — 0.98% of the **10,712.70** the field totalled with it, 0.99% of the **10,607.40** without. | MODEL | numerical test | NEW | — |
| Y006 | Its classification was **wrong in both independent audits that examined it** (`validation-v3.md` W041, `validation-v5.md` X035), and v4.0's own repair harness passed what v5.0 then refuted. | WORLD | derivation | REVISED | X034 |
| Y007 | Three start-state reads are corrected in the same pass: `on_startup` devastation, dated `add_base_*` accumulation, and the `is_city` filter the engine does not apply. | DESIGN | stipulated | NEW | — |
| Y008 | §2.4 now states the reason a canonical node order is a correctness requirement: **Phase 2's min-cost flow is degenerate, so presentation order selects which optimum is returned.** *(Restated at §1.6 and argued at §2.4 item 1.)* | MODEL | numerical test | NEW | — |
| Y009 | **Prose convention R2 — no empirical absolutes**: no superlative, no universal quantifier and no threshold asserted as a fact about the world; every such claim becomes a directional design statement or an observation scoped to the field and script that produced it. | DESIGN | stipulated | NEW | — |
| Y010 | **Prose convention R3 — no maintained figures for any rejected operator**: §3.15's graveyard keeps its design arguments and loses its measurements, covering `Φ_ord`, the gravity kernels, the v1 Laplacian, RANK and the seeded basins. Load-bearing comparisons are stated as directions instead. | DESIGN | stipulated | NEW | — |
| Y011 | Those rejected-operator numbers were re-measured and re-refuted in **three successive audits**, and not one of the rejection arguments depends on any of them. | WORLD | derivation | NEW | — |
| Y012 | Every graded claim from `validation-v5.md` — **22 refuted, 39 partial, 1 unverifiable** — is folded through, and `fixes-agreed.md` maps each one to the change that answers it. | WORLD | stipulated | REVISED | X001 |
| Y013 | `scripts/verify6.py` reads figures **out of the document text** and fails when they disagree with a value computed from the install — but it does **not** cover every figure the document prints. | DESIGN | stipulated | REVISED | X004 |
| Y014 | `verify6.py` pins **35 distinct figures across 29 checks**, well short of what the document prints. | WORLD | file value | NEW | — |
| Y015 | No coverage ratio is offered because the denominator is ill-defined: counting "the figures the spec prints" gives anywhere from **279 to 326** depending on how a numeric token is delimited. | WORLD | verified (method unstated) | NEW | — |
| Y016 | `scripts/coverage6.py` corrupts each spec-printed figure whether the harness looks at it or not, and should be re-run rather than quoted, because the number moves with every edit to the document. | DESIGN | stipulated | NEW | — |
| Y017 | Some figures carry a script attribution instead of a guard, and a few carry neither. | WORLD | verified (method unstated) | NEW | — |
| Y018 | `scripts/mutate6.py`'s score is not coverage: it plants errors only in figures `verify6.py` already checks, so it cannot fail — the same circularity v4.0's harness had, recorded rather than quietly fixed. | WORLD | derivation | NEW | — |

## §1.1 — Trade direction (lines 64–169)

**UNCHANGED:** C005, C006, C010–C012, C019–C022, V005–V015, V017–V024, V026–V028, V031, V032,
V036, V037, W007–W011, W015–W022, X005, X006, X007, X012, X014, X015, X016, X017.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y019 | The fallback branch fires only when every candidate is support-isolated with zero **post-peel** balance. | MODEL | derivation | REVISED | X008 |
| Y020 | The balance the priority key reads is the one Phase 0 hands on, with each pendant's balance folded into its parent — **not** the raw input `b` — so a map with non-zero raw balances can still reach the branch. | MODEL | derivation | NEW | — |
| Y021 | On a connected core the folded balance must vanish across the core: for a per-good graph that is a component with no producer and no consumer; for the aggregate graph every node's `Σ wealth^α_Φ` must be equal, which uniform *per-province* wealth does **not** deliver. | MODEL | derivation | REVISED | X009 |
| Y022 | Nodes hold between **0 and 72** counted provinces, so equal per-province wealth makes unequal node sums. | MODEL | file value | NEW | — |
| Y023 | Where the wealth key then ties, the **node index decides**. | MODEL | derivation | REVISED | X010 |
| Y024 | §2.8's containment set includes the fallbacks because of **T3** — a fallback promotion that is a sink in neither the selected nor the promoted set — and not because of the wealth tie, which is incidental; and this is **not** the reason §2.4 requires a canonical node order, which is a stronger requirement set by Phase 2. | DESIGN | derivation | REVISED | X011 |
| Y025 | On 1444 the fallback and pendant cases are empty and the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods, **1–8 sinks per good, mean 3.72**, zero fallbacks. | MODEL | numerical test | REVISED | X013 |
| Y026 | That equality is **a measurement on this input**, not a theorem, and v2 asserted it as one. | WORLD | derivation | REVISED | W014 |
| Y027 | It does not become a theorem by attaching conditions either: "Phase 0 a no-op and no fallback firing" looks sufficient and is not — **T2** satisfies both and still breaks it. | MODEL | derivation | NEW | — |

## §1.2 — Supply (lines 171–182)

**UNCHANGED:** C023, C025–C028, V038, V039, V040, V041. No delta claims.

## §1.3 — Demand (lines 184–342)

**UNCHANGED:** C031, C032, C033, C035, C036, C039, W023, W024, W026, W030, W033, W042 and W044
*(the `gems` and `incense` keys are still named as province-scoped, though their values are no
longer printed)*, W051, X023, X024, X025, X026, X059, X060, X061, X062.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y028 | Wealth reads **three things** about the province: its development, its trade good, and its own current condition. | MODEL | stipulated | NEW | — |
| Y029 | Two provinces with the same **development, trade good and condition** have the same wealth whoever owns them. | MODEL | derivation | REVISED | W025 |
| Y030 | Owner-agnosticism is true by construction, not by a rule that has to be policed; the classifier was a large surface to keep correct. | DESIGN | derivation | NEW | — |
| Y031 | `base_tax`, `base_production` and the trade good are bare attributes of the place, so nothing about them needs classifying. | MODEL | derivation | NEW | — |
| Y032 | *What this gives up:* `gems`' `local_tax_modifier` and `incense`' `trade_value_modifier` are genuinely province-scoped and are **no longer read**, along with great projects, permanent province modifiers and the DLC state they depended on. | DESIGN | stipulated | REVISED | X035 |
| Y033 | The dropped apparatus was live on **89 of the 2,472** counted provinces — 43 `gems`, **31** `incense`, 16 great-project and permanent-modifier provinces, less one that is both (province 542). | ENGINE | file value | REVISED | X036, X037 |
| Y034 | That count depends on the field: **87** under the withdrawn `is_city` filter, and 89 rather than 88 because province **4856** is one of the twenty whose good the engine rolls and it rolled `incense`. | ENGINE | file value | NEW | — |
| Y035 | `goods_produced(p) = GP_COEFF · base_production(p) · (1 + Σ province-state goods modifiers)` — no flat-bonus term and no other local modifiers. | MODEL | derivation | REVISED | X018 |
| Y036 | `trade_value(p) = goods_produced(p) · price(good(p))`, ducats per year — **no trade-value modifier term**. | MODEL | derivation | REVISED | X019 |
| Y037 | `tax_value(p) = TAX_COEFF · base_tax(p) · (1 + Σ province-state tax modifiers)`. | MODEL | derivation | REVISED | X020 |
| Y038 | ⚑ **`GP_COEFF` is a shipped file value**: `common/static_modifiers/00_static_modifiers.txt` carries `provincial_production_size = { trade_goods_size = 0.2 … }`, localised "Base Production" — the same tooltip line the coefficient was measured off. | ENGINE | file value | REVISED | W031 |
| Y039 | It is therefore moddable and is **read at runtime**, not hardcoded. *(Restated at §2.2 item 4 and §2.3.)* | DESIGN | stipulated | NEW | — |
| Y040 | `TAX_COEFF` is in **no file that has been found** — `defines.lua`, `common/defines/` and that static-modifier block were all searched — so it stays a measured constant carrying the observation that produced it. | ENGINE | file value | REVISED | W031 |
| Y041 | ⚑ The tax tooltip's schema is `Base: trunc(base_tax × 0.0833333) (Yearly base_tax)` — observed `Base: 0.49 (Yearly 6.00)` at `base_tax` 6 and `Base: 0.16 (Yearly 2.00)` at 2. | ENGINE | engine test | REVISED | X021 |
| Y042 | The parenthetical is `base_tax` itself and the `Base` line is its truncated twelfth; it is **not** twelve times the displayed figure, which would give 5.88 and 1.92. | ENGINE | derivation | NEW | — |
| Y043 | v4.0 and v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both of its own data points; **v3.0 carries neither that schema nor the 0.6125 arithmetic**. | WORLD | derivation | NEW | — |
| Y044 | § The monthly production tooltip's `Trade Value` line is *consistent with* the same relation on one observation, 3.52 → `+0.29`, which fixes the divisor only to within **(11.73, 12.14]**. | ENGINE | engine test | REVISED | X022 |
| Y045 | Both monthly figures being the annual value over twelve is what lets the annual forms add directly, and **the tax pair establishes it at two development levels**. | MODEL | derivation | REVISED | W036 |
| Y046 | ⚑§ Observed on Garnatah: `base_tax` 6 at `Tax Income Efficiency 125.0%` displays `Base 0.49` and then `0.62`; 0.49 × 1.25 = 0.6125 truncates to 0.61, so the engine multiplies the **untruncated** monthly value (6 × 0.0833… = 0.49999…, × 1.25 = 0.62499… → 0.62). | ENGINE | engine test | REVISED | X027 |
| Y047 | The example establishes only the ordering — base from development first, percentage second — and nothing finer. | ENGINE | derivation | NEW | — |
| Y048 | v4.0 and v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires rounding while §2.3 requires truncation; both cannot hold. | WORLD | derivation | NEW | — |
| Y049 | Flat goods bonuses *would* add into `goods_produced` before the price multiply, but under §1.3 **no source grants one**, so the ordering is stated for the emitter's benefit and is exercised by no province in the model. | MODEL | derivation | REVISED | X028, X029 |
| Y050 | **Province condition is the one thing besides development and the good that wealth reads**: four static modifiers describe a province's own state, all read from `common/static_modifiers/00_static_modifiers.txt`. | ENGINE | file value | REVISED | X040 |
| Y051 | Their keys and targets: `devastation` `trade_goods_size_modifier = -2` scaled by level → `goods_produced`; `prosperity` +0.25 → `goods_produced`; `under_siege` −0.25 → `goods_produced`; `occupied` −0.5 **and** `local_tax_modifier = -0.5` → both. | ENGINE | file value | REVISED | X040 |
| Y052 | ⚑ `unrest` grants `local_tax_modifier = -0.02` **per point of revolt risk** and enters `tax_value`; it appears as a fifth row in the table the prose calls four. | ENGINE | file value | NEW | — |
| Y053 | `occupied` and `unrest` touch the tax term; the other three reach `goods_produced` alone. | MODEL | derivation | REVISED | X040 |
| Y054 | ⚑ `devastation`'s **scaling law is an assumption, not a file value**: the model assumes `-2 × level/100`. It is the only such assumption in the table — `unrest` and `nationalism` both carry per-unit comments in the same file, so the convention for stating a scaling exists. | ENGINE | file value | NEW | — |
| Y055 | ⚑ `unrest` is **live at the 1444 start**: 21 counted provinces carry revolt risk between 4.834 and 14.834 in the save, worth **12.23 ducats — 0.115% of world wealth**. | ENGINE | file value | NEW | — |
| Y056 | Admitting `unrest` moves **no edge** of the installed graph, so it is a fidelity correction with no orientation consequence. | MODEL | numerical test | NEW | — |
| Y057 | ⚑ Sixteen of the 21 are resolvable from `history/provinces` at integer risk 5/8/10/15; the other five, all Shirvan-owned, receive theirs at runtime, so the model reads the save. | ENGINE | file value | NEW | — |
| Y058 | These modifiers are what make the map answer to war: §1.2's volatility and §3.3's besieged-province claim rest on them, and §2.8's war rows are their test. | DESIGN | derivation | REVISED | X040 |
| Y059 | ⚑ **Eleven counted provinces begin devastated** — Bohemia at 50, Erzgebirge and Moravia at 20 — and no province-history file says so. | ENGINE | file value | NEW | — |
| Y060 | ⚑ That devastation is applied by `on_startup` firing `flavor_boh.15` ("The Aftermath of the Hussite Wars"), via `common/on_actions/00_on_actions.txt` → `on_startup_effect` → `common/scripted_effects/01_scripted_effects_for_on_actions.txt`. | ENGINE | file value | NEW | — |
| Y061 | It costs **13.40 ducats** across the eleven affected counted provinces. | MODEL | numerical test | NEW | — |
| Y062 | **The start state is what the engine produces, not what the history files say**, and that costs three separate reads. | DESIGN | derivation | NEW | — |
| Y063 | ⚑ `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`, `flavor_geo.1` and others directly from its own `events = { }` list — a second path alongside the `on_startup_effect` chain. | ENGINE | file value | NEW | — |
| Y064 | ⚑ **Development does not move before the first tick**: the history parse matches the save on **2,472 of 2,472** provinces for `base_tax`, `base_production` and owner, and only `trade_goods` differs, on exactly the twenty provinces named below. | ENGINE | file value | NEW | — |
| Y065 | ⚑ v6.0's first draft said `flavor_geo.1` carries `add_base_tax` and could move development pre-tick; it does not — its whole effect is legitimacy, a country modifier and a flag, and those keys are in `flavor_geo.3`, which `on_startup` does not fire. | WORLD | file value | NEW | — |
| Y066 | ⚑ **`add_base_*` in a dated block before the start date accumulates**, and v5.0 and earlier overwrote instead of adding: province 1 (Uppland) has `base_tax = 5` undated plus 1 at `1436.4.28`, and the game has 6. | ENGINE | file value | NEW | — |
| Y067 | ⚑ **`is_city = yes` is not a filter the engine applies**: 20 owned provinces omit or comment out the line — province 265 among them, also one of the devastated eleven — and the engine treats them as cities. | ENGINE | file value | NEW | — |
| Y068 | The model counts a province when it has an owner and lies in a trade node: **2,472** provinces, not 2,452. | DESIGN | derivation | REVISED | W050 |
| Y069 | ⚑ **Twenty counted provinces have `trade_goods = unknown`** in their history file, and the engine assigns one at start from each good's `chance = { }` block. | ENGINE | file value | NEW | — |
| Y070 | The model reads the good the engine actually rolled rather than predicting the draw; pricing those provinces at zero instead understates world wealth by **12.70 ducats**. | DESIGN | numerical test | NEW | — |
| Y071 | ⚑ On this save the twenty came up seven `fur`, five `grain`, three `wool`, two `livestock`, and one each of `cotton`, `incense` and `naval_supplies`; a different roll gives a slightly different field and nothing in the model depends on which one. | ENGINE | file value | NEW | — |
| Y072 | `TAX_COEFF = 1.0` is applied to every province the model counts: ownership is not modelled, so every province is treated as **cored and settled**. | DESIGN | derivation | REVISED | X063 |
| Y073 | That is a modelling choice with a known cost: **two readings**, both on cored city provinces at `base_tax` 2 and 6, are all `TAX_COEFF = 1.0` rests on. | DESIGN | derivation | NEW | — |
| Y074 | ⚑ `base_tax` at 1444 runs up to **15** (province 1821), with total development reaching **33** there. | ENGINE | file value | NEW | — |
| Y075 | Owner-agnostic wealth removes **a large** source of hidden owner-dependence from the aggregate graph. | MODEL | derivation | REVISED | W052 |

## §1.4 — Market concentration (lines 344–354)

**UNCHANGED:** C040–C047. No delta claims.

## §1.5 — Goods without a graph (lines 356–405)

**UNCHANGED:** C048, C051–C056, V050–V058, W053, W182–W186, W188, W189 *(coal's 10.0 is the
highest base price; v6.0 adds the file path and script but not a new proposition)*, W191.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y076 | Repricing to coal the 45 owned latent-coal provinces flips **10 of 159** `Φ_w` edges and adds **214.60 ducats** to world wealth (`measure6.py`). *(Restated in §2.8's Latent-good row.)* | MODEL | numerical test | REVISED | X064 |
| Y077 | The counterfactual holds every non-repriced input fixed: province **4237** is both latent-coal and one of the devastated eleven, so a reprice that dropped its devastation would measure coal activating **plus** one province healing — 2.40 ducats and 3 extra flips. | MODEL | numerical test | NEW | — |

## §1.6 — The aggregate graph (lines 407–576)

**UNCHANGED:** C059, C062, V063, V064, V212, V218, V221, W054, W055, W058, W064, X067, X089, X090
*(the Renaissance's `development_cost = -0.05`; "5%" was dropped as an R2 narrowing, not a
proposition change)*, X091, X095, X123 *(via §2.3)*.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y078 | **Both the sinks' count and their locations move with the wealth field**, and `α_Φ` sets how sharply concentration is read. | MODEL | derivation | REVISED | X065 |
| Y079 | At the stipulated α_Φ = 1.5 the 1444 field gives **two** sinks and a modestly grown Europe gives three or one, so neither count nor placement is fixed by the constant. | MODEL | numerical test | NEW | — |
| Y080 | v2.0–v4.0 ("the count emerges from concentration") and v5.0 ("the count is set by `α_Φ`") are wrong the same way — the count is a function of the field **and** the constant; v2.1 also chose the value with a target count in view, a calibration §2.3 withdraws without replacing. | WORLD | derivation | REVISED | X066 |
| Y081 | Measured: identical orientation at ×1 and above, **12** edge flips at ×10⁻², and **100** at ×10⁻⁶, where the sink set also collapses to `{genua}`. | MODEL | numerical test | REVISED | X068 |
| Y082 | 1444's `b_w` has largest magnitude **0.0225**. | MODEL | numerical test | REVISED | X069 |
| Y083 | Measured at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and `hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12. | MODEL | numerical test | REVISED | X070 |
| Y084 | One of the two is a property of the world and the other a property of the node ordering, and that difference matters more than the count. | MODEL | derivation | NEW | — |
| Y085 | Over **800 relabellings** (eight seeds of 100, `α_Φ` and every input fixed, `relabel6.py`) the orientation changed every time, a mean of **25 of 159** edges moved, and the sink set came back exactly `{english_channel, hangzhou}` in **64 of 800** runs. | MODEL | numerical test | NEW | — |
| Y086 | `hangzhou` was an end in **about 98%** of them and `english_channel` in **about 40%**. | MODEL | numerical test | NEW | — |
| Y087 | The Asian end is robust but **not invariant** — orderings exist where it loses its end — and the European end is one of several the same world admits. | MODEL | derivation | NEW | — |
| Y088 | After `english_channel` the most frequent end-holders are `gulf_of_siam` (a little over half the runs), `wien` (about a third), then `rheinland` and `sevilla`; the count itself ranged **1 to 5**, most often 2 or 3. | MODEL | numerical test | NEW | — |
| Y089 | Across three independent 800-trial sets `hangzhou` came in at **784–789** and `english_channel` at **322–336**, while `sevilla` ranged 79–117 and `rheinland` 112–136. | MODEL | numerical test | NEW | — |
| Y090 | The two leading proportions are quoted to two figures and the trailing ones qualitatively because that is as far as the sample supports; a per-seed range is worse still, being a function of which seeds are drawn. | DESIGN | derivation | NEW | — |
| Y091 | Conditional on the node order: the sink set's membership and size, §2.4's end-flag list, which European node holds an end in the table, and **the size of any node's drainage basin**. | MODEL | derivation | NEW | — |
| Y092 | **No basin figure is quoted anywhere in §1.6**, because at the growth factors where one would be interesting `english_channel` holds an end in only a handful of orderings. | DESIGN | derivation | NEW | — |
| Y093 | Not conditional over the same relabellings: the map is fully oriented (159/159) and acyclic every time, no fallback ever fires, and the LP objective is identical to within four units in the last place — different *optimal* orientations, not different answers. | MODEL | numerical test | NEW | — |
| Y094 | Phase 1 selects `genua`; both sinks arrive by stall promotion and `genua` ends a transit node, so **2 promotions and 0 fallbacks**. | MODEL | numerical test | REVISED | X072 |
| Y095 | **Eight sources**, all in the bottom half of the wealth field, `c_w` ranks **44–75**, mean degree **3.1** against the map's 4.0. | MODEL | numerical test | REVISED | X073 |
| Y096 | Every node drains to a sink; acyclic, 159/159 oriented; the sink set is unchanged under ±1% wealth noise on **three** seeds. | MODEL | numerical test | REVISED | X074 |
| Y097 | Per good on the same field: 1–8 sinks, mean 3.72, 29/29 acyclic, 0 fallbacks, and **89.6%** of ordered node pairs (**5,663 of 6,320**) connected by at least one good's directed path. *(Restated in §3.8.)* | MODEL | numerical test | REVISED | X158 |
| Y098 | Agreement with the per-good graphs is **53.6%** of edge-goods, **52.3%** value-weighted. *(Restated in §2.8's "Measured, not asserted".)* | MODEL | numerical test | REVISED | X075 |
| Y099 | The superseded marking-order aggregate **scored higher** on that measure, and no figure is maintained for an operator the model does not install. | DESIGN | stipulated | REVISED | X076 |
| Y100 | **`α_Φ = 1.5` is a stipulated design constant, exactly as `P₀ = 2.0` is** — superlinear and round — and the document no longer offers any derivation for it. | DESIGN | stipulated | REVISED | X083 |
| Y101 | Scanned over [1, 8] rather than [1, 3], the widest sink-count band is **1.71** wide, **[3.50, 5.21]**, giving `{doab, genua, hangzhou}`, and 1.5's is not the widest by any margin. | MODEL | numerical test | REVISED | X078 |
| Y102 | Both prior derivations are withdrawn: v2.1–v4.0's two-sink calibration was fitted to a field that no longer exists, and v5.0's widest-band argument depended on where the α scan was truncated. *(Restated at §2.3.)* | WORLD | derivation | REVISED | X122 |
| Y103 | Across α_Φ = 1.00…8.00 at 0.01 the sink set is a step function, and 1.5 sits in the band **[1.38, 1.63], width 0.25**, giving `{english_channel, hangzhou}`. | MODEL | numerical test | REVISED | X077, X078 |
| Y104 | Sampled at the six values v2 used, the count is non-monotone: **6 → 2 → 1 → 2 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}. | MODEL | numerical test | REVISED | X084 |
| Y105 | A written warning against re-deriving 1.5 from the two-ends-versus-vanilla's-three resemblance, because that is the calibration §2.3 withdrew and the mistake has been made twice. | DESIGN | stipulated | NEW | — |
| Y106 | **Europe becomes the centre of trade as it develops** is the design claim, and it is what §3.1's first goal asks the field to deliver. | DESIGN | stipulated | REVISED | X085, X088 |
| Y107 | As European development compounds the ends move west and Asia's pole fades: the Channel's basin widens non-monotonically, `genua` first holds an end at **×1.63** and is sole end from **×1.64 through ×2.00**, and past a broad range of European growth Asia holds no end at all. | MODEL | numerical test | NEW | — |
| Y108 | The mechanism carrying it: wealth is linear in development, so developing a region moves its `c_w` share directly and `Φ_w`'s ends follow the wealth. | MODEL | derivation | NEW | — |
| Y109 | Scaling European development only (`europe.py`, **824** counted European provinces): ×1.00 → `{english_channel, hangzhou}`; ×1.02 → adds `wien`; ×1.56 → `{english_channel, rheinland}` with Asia holding none; ×2.00 → `genua` alone. | MODEL | numerical test | REVISED | X086, X087 |
| Y110 | The table is to be read as a direction on one node ordering; which European node holds an end at the smaller factors is ordering-dependent, so the direction is the claim and the membership is not. | DESIGN | derivation | NEW | — |
| Y111 | The ×2.00 row is the exception: `genua` held an end in **60 of 60** relabellings, so a single Mediterranean end under that much European growth is a property of the field. | MODEL | numerical test | NEW | — |
| Y112 | Because wealth is linear in development, **scaling development and scaling wealth are the same operation here** — maximum difference 0.0 across the European set — so the distinction that made v5.0's version of this table wrong does not arise. | MODEL | numerical test | NEW | — |
| Y113 | The 1444 Silk Road route from Genoa to the Asian sink is `genua → alexandria → aleppo → persia → lahore → lhasa → ganges_delta → burma → gulf_of_siam → canton → hangzhou`. | MODEL | numerical test | REVISED | X094 |
| Y114 | **No route leaves `english_channel` at all** — it is a sink with out-degree 0, so the Hansa and the Danube carry power *into* it, and v5.0's "from the Channel it is the Hansa and the Danube" described a path that does not exist. | MODEL | numerical test | REVISED | X096 |
| Y115 | **No Europe→sink route passes the Cape of Good Hope**, checked from `genua`, `north_sea` and `english_channel`. | MODEL | numerical test | REVISED | X097 |
| Y116 | The Cape is a live conduit: in-degree 1, out-degree 3, with **132 ordered node pairs** whose path runs through it, carrying Atlantic drainage into the Indian Ocean. | MODEL | numerical test | NEW | — |
| Y117 | v5.0's "nothing routes through the Cape" is false as a universal and was only ever checked on the Europe→sink routes. | WORLD | derivation | NEW | — |
| Y118 | In the per-good graphs the Cape also carries Asian spices to Europe; `Φ_w` models power, not cargo. | MODEL | numerical test | REVISED | X098 |
| Y119 | Scaling the 22 European **nodes** makes `genua` the sole sink from about **×1.65**, and the 18-node western/central subset needs about **×2.15**. | MODEL | numerical test | REVISED | X099 |
| Y120 | Somewhere inside roughly **×2.9–×3.5** the Cape reverses; the reversal is bounded above as well as below, so it is a window and not a threshold, and its edges move with the field. | MODEL | numerical test | REVISED | X100 |
| Y121 | Dev-stacking a single node's top province concentrates the map on that node. | MODEL | numerical test | REVISED | X101 |

## §1.7 — Merchants (lines 578–604)

**UNCHANGED:** C067–C083, V066, V068, V069, V070, W065, W192, X102. No delta claims.

## §1.8 — Collection and transfer (lines 606–636)

**UNCHANGED:** C084–C102, V072, X103, X104. No delta claims.

## §1.9 — Trade power propagation (lines 638–647)

**UNCHANGED:** C103–C111, V073, W067 *(the tooltip qualifier is descriptively false — §1.9's own
paragraph is untouched; §2.7's restatement is weakened, see Y151)*, W068, W069. No delta claims.

## §1.10 — Direction-dependent systems (lines 649–705)

**UNCHANGED:** C112–C143, V074, V078, V079, V080, W070, W071, X105, X106, X109, X110, X196.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y122 | ⚑ `TRADING_POLICY_COOLDOWN_MONTHS = 12` applies to **seven of the nine entries** in `common/trading_policies/00_trading_policies.txt` — five distinct policies, four of them with an `_upgraded` twin, plus Propagate Religion which has none — so four of the five families are rate-limited. | ENGINE | file value | NEW | — |
| Y123 | ⚑ `maximize_profit` and `maximize_profit_upgraded` carry `cooldown = no`, and Propagate Religion is inside the cooldown. | ENGINE | file value | NEW | — |
| Y124 | ⚑ `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` and `TRADE_COMPANY_COOLDOWN = 60` rate-limit the trade-company thresholds, so a flickering share does not translate into a flickering *effect* at those three. | ENGINE | file value | NEW | — |
| Y125 | What is left exposed is everything without a cooldown, which is most of the ladder. | ENGINE | derivation | NEW | — |
| Y126 | The caravan cap of 50 is **9.4% to 47.0%** of an inland node's total trade power, median **21.6%**, over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. | MODEL | numerical test | REVISED | X107 |
| Y127 | As a share of the node's total **after** the grant lands — 50/(total+50) — the same figures read 8.6%–32.0%, median 17.7%; v5.0 quoted those under the first description, which cannot hold since 8.6% of 532.0 is 45.8 rather than 50. | MODEL | numerical test | REVISED | X107 |
| Y128 | On §2.2's derived 25-node inland basis the median is **21.3%**, or 17.5% after the grant. | MODEL | numerical test | REVISED | X108 |

## §1.11 — Treasure fleets · §1.12 — What the game displays (lines 707–734)

**UNCHANGED:** C144–C148, C149–C165, V049, V065, V081. No delta claims.

## §2.1 — Shape (lines 738–755)

**UNCHANGED:** C167–C184, V082–V085, W072, W073. No delta claims.

## §2.2 — Solver (lines 757–799)

**UNCHANGED:** C185–C209, V064, V091, V092, V229, W075, W076, X115.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y129 | Solver item 4 computes `TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production · (1 + province-state goods modifiers) · price`, with no autonomy, efficiency, ideas or owner terms. | DESIGN | stipulated | REVISED | X111 |
| Y130 | The only modifiers read are the four that describe the province's own condition, and at 1444 **only `devastation` is live, on eleven provinces**. | DESIGN | stipulated | REVISED | X112 |
| Y131 | World wealth is **10,607.40** annual ducats over **2,472** counted provinces. | MODEL | numerical test | REVISED | X113 |
| Y132 | Measured on the reference implementation: **of order 0.1 s for all 29 goods, single-digit milliseconds per good on average** — and that is the whole of the claim. | MODEL | numerical test | REVISED | X114 |
| Y133 | Repeated 12-run experiments on one machine do not reproduce each other closely enough to support anything finer — three replicates gave per-good averages spanning 3.5–10.5, 3.5–10.8 and 3.1–4.7 ms — so no range is quoted, because the quantity measured is a machine and a scheduler rather than the algorithm. | MODEL | numerical test | NEW | — |
| Y134 | v5.0's "0.17–0.21 s for all 29 goods" is not reproducible: across three replicates of twelve runs the number of runs landing inside that interval was 1, then 0, then 0. | WORLD | numerical test | NEW | — |

## §2.2a — What map this is for (lines 801–841)

**UNCHANGED:** W077–W085, W088, X116.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y135 | Where Phase 0 acts, free-edge **determinism** is unaffected and **index-independence is not**: the key reads the post-fold balance β, so peeling can create exact ties the raw balances do not have, and the 1444 measurement does not transfer. *(Restated at §3.2 item 2.)* | MODEL | derivation | REVISED | X117 |

## §2.3 — Constants (lines 843–893)

**UNCHANGED:** C211–C227, V094, W089, W090, W091, W097, W098, X118, X119, X120, X121, X123, and
the DLC-third-axis claim. *(§2.3's α_Φ paragraph restates Y100 and Y102.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y136 | The two wealth coefficients are **not the same kind of constant**: the emitter reads `GP_COEFF` rather than carrying 0.2, and only `TAX_COEFF` must be re-measured against any patch that is not 1.37.5. | DESIGN | stipulated | REVISED | W032 |
| Y137 | v3.0 through v5.0 said neither coefficient was in a file, and shipped a whole-install modifier sweep that **walked past the block holding one of them**. | WORLD | derivation | NEW | — |

## §2.4 — The tradenodes file (lines 895–968)

**UNCHANGED:** C228–C233, C235–C242, V095, V148, W099, W100, W102–W107, W114, X124, X127.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y138 | The node order is a correctness requirement and **the reason is Phase 2 rather than any tiebreak**; the emitter must fix one canonical order, and it must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks ties in. | DESIGN | derivation | REVISED | X125 |
| Y139 | Measured on 1444: relabelling the nodes changed the aggregate orientation in **400 of 400** runs across four independent seeds, **always** by returning a different optimal vertex and **never** by a sweep tiebreak, with a mean of **25 of 159** edges moving. | MODEL | numerical test | NEW | — |
| Y140 | The LP objective is identical to within four units in the last place — **4.44e-16** absolute against an objective of **0.712**, the same quantity as the 6.2e-16 relative deviation and not a second measurement — and it grows to **6–7 ULP** at larger trial counts, so it is a sample maximum rather than a bound. | MODEL | numerical test | NEW | — |
| Y141 | `relabel6.py` validates its instrument against `drain.py` on the identity permutation and aborts if that fails. | DESIGN | stipulated | NEW | — |
| Y142 | Twenty-five flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event. | MODEL | derivation | NEW | — |
| Y143 | The same effect on the **per-good** graphs is **580 of 580** (29 goods × 20 relabellings), from `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`. | MODEL | numerical test | NEW | — |
| Y144 | v6.0 withdrew that sweep on the ground that its script had never shipped; the script is in the tree and runs, so the withdrawal was the error rather than the figure — and no v1–v5 spec ever printed it, so it was never "quoted by earlier versions". | WORLD | derivation | NEW | — |
| Y145 | Everything §1.6 and §2.8 report about stability is measured **at fixed node order**; re-order the same world and the map moves with `α_Φ` and every input held fixed. | DESIGN | stipulated | NEW | — |
| Y146 | The specific counts are HiGHS-specific in their detail but not in kind: any simplex returns *a* vertex of a degenerate optimal face. | MODEL | derivation | NEW | — |
| Y147 | Making the orientation independent of presentation order would need a tie-breaking objective — a lexicographic secondary cost or a strictly convex perturbation — which is a design change and is not adopted here. | DESIGN | stipulated | NEW | — |
| Y148 | The priority key ties in more places than §1.1 documents — Phase 1's within-cluster argmin, the stall promotion's identical form, and the top-k cut between equal-mass clusters — and **none of them fires on 1444** (zero exact `(DEF, β)` ties on free edges 29/29, zero within-cluster β ties, zero tied cluster masses). *(Restated at §3.2 item 2.)* | MODEL | numerical test | REVISED | X151 |
| Y149 | The end-flag list is **a function of the canonical node order, not of the world alone**: on the 1444 field `hangzhou` is an end in about 98% of relabellings and `english_channel` in about 40%, so changing the order changes the flags with nothing in the world changing. | DESIGN | derivation | NEW | — |
| Y150 | 1444 in shipped order has **two** end nodes, `english_channel` and `hangzhou`, against vanilla's three. | DESIGN | numerical test | REVISED | X126 |

## §2.5 — Runtime attachment · §2.6 — Writing to the engine (lines 970–996)

**UNCHANGED:** C243–C250, C251–C272. No delta claims.

## §2.7 — Probes (lines 998–1036)

**UNCHANGED:** C274–C293, V098–V101, W108–W114.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y151 | § §1.9's "every immediately upstream node" is *consistent with* probe 15's observation — **one observation on one node**, enough to retire §3.16's cautionary case and not enough to promote the rule to a measurement. | ENGINE | engine test | REVISED | W067 |

## §2.8 — Validation (lines 1038–1080)

**UNCHANGED:** C298–C342, V109–V112, W116, W117, W119, W195, X128, X133, X134, X135, X136, X137.
*(§2.8 restates Y025, Y076, Y098 and Y131.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y152 | High-demand nodes are sinks at **16.8%** in the top demand decile against 6.9% in the bottom — a barbell, LP branch ends landing in poor pockets. | MODEL | numerical test | REVISED | X129 |
| Y153 | The razed-China row is **ordering-robust** where §1.6's sink membership is not: it turns on `hangzhou` holding an end, which it does in about 98% of relabellings, and on the razed field `hangzhou` loses its end in every relabelling tried. | MODEL | numerical test | NEW | — |
| Y154 | Zeroing `hangzhou`-node development moves the `Φ_w` sinks from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`, with **22 of 159** edges flipping. | MODEL | numerical test | REVISED | X130 |
| Y155 | `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth **226.7 against 143.0**, and it holds the richest single province the model counts. | MODEL | numerical test | REVISED | X131 |
| Y156 | Zeroing `beijing` **also** moves the map — **15 flips** — because deleting a percent of world wealth renormalises `c_w` everywhere; the asymmetry is which node keeps its end, not whether the map moves. | MODEL | numerical test | REVISED | X132 |

## §2.9 — Build order (lines 1082–1093) · §3.1 — Goals (lines 1097–1105)

**UNCHANGED:** C343–C352, C353–C365, V113, X138. No delta claims. *(§2.9's assertion list names the
widened containment set `{selected} ∪ {promoted} ∪ {fallbacks}`; that proposition is X136, carried
UNCHANGED at its first appearance in §2.8.)*

## §3.2 — Why a flow and a drainage sweep (lines 1107–1215)

**UNCHANGED:** C366, C370–C375, C383–C385, V115, V116, V118–V122, V124, V128–V131, W120, W123,
W125–W128, X139, X146, X147, X148, X149, X150. *(§3.2 item 2 restates Y135, Y148 and Y008.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y157 | **What the ratio metric cannot see is the thing the diagnosis rests on**: sparsity — most nodes produce nothing at all of a given good (spices in 18 of 80 nodes, cloves in exactly one) — so `(c−s)/deg` is dominated by *where* supply exists, and a max/min ratio over producing nodes is blind to that by construction. | MODEL | derivation | REVISED | X141 |
| Y158 | On the contrast metric itself the demand side is the wider one, not the supply side; **no figure is carried for it**. | MODEL | numerical test | REVISED | X140 |
| Y159 | Better wealth inputs move Genoa to a **co-**sink at roughly **×1.7** without making demand the determinant of placement. | MODEL | numerical test | REVISED | X142 |
| Y160 | Moving the spice sink to a Chinese node takes a multiple of that node's **wealth** in the region of **3.6–4.8×** — `beijing` 3.63×, `hangzhou` 4.13×, `xian` 4.61×, `canton` 4.78× on the 1444 field. | MODEL | numerical test | REVISED | X143 |
| Y161 | These are **wealth** multiples, not demand multiples: because demand is `wealth^α` normalised over the world, the same move expressed in demand is a much larger factor. | MODEL | derivation | NEW | — |
| Y162 | The four named are not the cheapest — `girin` needs 3.89× and `yumen` 4.49×, both inside the range — so the claim is about the size of the intervention rather than which node is easiest to move. | MODEL | numerical test | REVISED | X144 |
| Y163 | Sink placement is a measurement **on one input**: on 1444, final sinks = `{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal demanders}`, measured exact 29/29, and three constructed inputs (T1, T2, T3) break it. | MODEL | numerical test | REVISED | X145 |
| Y164 | v5.0 tried to rescue that equality by attaching two conditions — Phase 0 a no-op and no fallback firing — and **those conditions are necessary, not sufficient**: T2 satisfies both and still breaks it, so the conditioned form is no more a theorem than the bare one. | WORLD | derivation | NEW | — |

## §3.3 — Why wealth, and why per province (lines 1217–1239)

**UNCHANGED:** C386–C406, C408, C412, C413, V132, V133, V135, W132–W139.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y165 | ⚑ `cape_of_good_hope`'s `members` list has 20 entries but province 1460 is a **sea zone**, listed in `map/default.map`'s `sea_starts`, so the node has 19 **land** provinces. | ENGINE | file value | NEW | — |

## §3.4 — Why supply is pre-modifier (lines 1241–1251)

**UNCHANGED:** C415–C423, V137, V139, W140, W141, W142.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y166 | In v1 substituting production income measurably broke the α = 1 identity, with orientation agreement collapsing to **well under half the map** (no count quoted). | MODEL | numerical test | REVISED | V138 |

## §3.5 — Why α is anchored absolutely (lines 1253–1302)

**UNCHANGED:** C427–C442, V140–V144, V147, X152, X153, X157.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y167 | ⚑ **`change_price` values are fractions of the good's base price, not ducats**, and the shipped save `tutorial/eu4_tutorial_chapter10.eu4` settles it: `paper` at `current_price=4.375` on a base of 3.5 (×1.25, not +0.25) and `gems` at 5.000 on a base of 4.0. | ENGINE | file value | NEW | — |
| Y168 | The install carries **161** textual `change_price` blocks — 93 in `events/`, 14 in `missions/`, 1 in `common/`, **53 in `history/` of which 13 are negative** (all in `history/countries/HAB - Austria.txt`), and **none in `decisions/`**. | ENGINE | file value | REVISED | X154 |
| Y169 | ⚑ **Ten of the 161 never execute** — four inside `effect_tooltip = "…"` strings, three inside a `country_event_with_effect_insight`'s `effect = "…"` string, three inside `tooltip = { }` display wrappers — so **151 are executable**. | ENGINE | file value | NEW | — |
| Y170 | Six of the seven quoted blocks duplicate one already counted in `events/` and the seventh names a price key no event ever sets; all ten are positive and every negative block is executable, so **the partition is identical under either census**. | ENGINE | file value | NEW | — |
| Y171 | v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them; both were wrong about which number was the **executable** one. | WORLD | derivation | REVISED | X155 |
| Y172 | v5.0's claim that the scan was "guarded by a per-file count assertion" is false — there was no assertion anywhere in its toolchain. | WORLD | derivation | REVISED | X155 |
| Y173 | `verify6.py` checks the census only by requiring the printed total to match a computed one rather than reconciling per file, and `measure6.py`'s walker still swallows parse failures in a bare `except`. | WORLD | stipulated | NEW | — |
| Y174 | The reason a plain parse misses the quoted blocks is mechanical: `pdx.py` tokenises a quoted string as one opaque unit, so a `change_price` inside a tooltip string is invisible to the walker. | WORLD | derivation | NEW | — |
| Y175 | ⚑ **1.875 is the single-key floor, not the campaign figure**: the same `1540.1.1` block also applies `COTTON_IMPORTS = -0.10` to `wool`, so a campaign running it holds two live negative keys and wool sits at **1.625 if keyed changes sum or 1.6875 if they compound** — and nothing in the install settles which, because no readable save carries a good with two live keys. | ENGINE | file value | REVISED | X156 |
| Y176 | The partition needs the **history** value: `events/PriceChanges.txt`'s −0.20 for the same key would alone floor wool at 2.00, and events alone give **12/3/4/11** rather than 13/2/4/11. | ENGINE | file value | NEW | — |

## §3.6 — Why no hysteresis, and why there is no ε (lines 1304–1339)

**UNCHANGED:** C443–C446, C449, C452, V148, V152, V154, W147–W152, X124. No delta claims.

## §3.7 — Why eligibility is per good (lines 1341–1347)

**UNCHANGED:** C463–C473. No delta claims.

## §3.8 — Why gates evaluate true (lines 1349–1367)

**UNCHANGED:** C474–C497, V155–V158, W154. *(The 89.6% / 5,663-of-6,320 connectivity figure is
Y097 at first appearance in §1.6; §3.8 restates it, including the note that v2's 98.8% was v1's
Laplacian figure carried across the operator change.)*

## §3.9 — Why `Φ_w` is the installed graph (lines 1369–1416)

**UNCHANGED:** C502, C505–C510, C512, V160, V161, V162, V218, V221, V228, X161.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y177 | `genua`, `gulf_of_siam` and `sevilla` rank **4th, 3rd and 7th** by node wealth on the corrected field (`mexico` is 2nd) at **296.0, 297.9 and 266.5** against `english_channel`'s 316.6, **which is a sink**. | MODEL | numerical test | REVISED | X159 |
| Y178 | Across 20 relabellings `Φ_ord`'s end count runs **12 to 19** and its end set is **never twice the same**, so neither the count nor the share terminating no good is a property of the world. | MODEL | numerical test | REVISED | X160 |
| Y179 | **Most** of `Φ_ord`'s ends terminate no good, none of the demand capitals is among them, and its end count does not concentrate as demand concentrates. | MODEL | derivation | REVISED | X160 |
| Y180 | No figure is maintained for `Φ_ord`: it is not the installed operator, its numbers moved with every change to the wealth field, and three successive audits spent their effort recounting them. | DESIGN | stipulated | NEW | — |
| Y181 | v2.1–v4.0's "two vanilla-like ends at 1444" premise is withdrawn and **must not be revived** even though the 1444 field again gives two ends: the count is a property of the field, not of the operator, and pinning the operator to it would be the calibration §2.3 withdrew. | WORLD | derivation | REVISED | X162 |
| Y182 | What the trade costs is self-coherence with the per-good graphs, which the superseded marking-order aggregate scores higher on; what it buys is one operator, one set of guarantees, and ends that sit where the wealth is. **No point gap is quoted.** | DESIGN | stipulated | REVISED | X163 |

## §3.10 — Why the engine's economy is overwritten (lines 1418–1435)

**UNCHANGED:** C513–C521, C523–C525, C528–C530, X164, X165, X167.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y183 | The two forms agree to a worst relative disagreement of **0 to 3.7e-16** — **one to three** units in the last place. | MODEL | numerical test | REVISED | X166 |
| Y184 | Propagation is kept on a single graph, **and the reason is not the one v1 through v6.0's own first draft gave**. | DESIGN | derivation | NEW | — |
| Y185 | Reading the one installed graph leaves the propagated term good-independent, so the identity holds by construction, and in doubles to within one to three ULP. | MODEL | numerical test | REVISED | X168 |
| Y186 | `gulf_of_siam`'s 29 goods leave it by **seven** distinct downstream sets. | MODEL | numerical test | REVISED | X169 |
| Y187 | Per-good propagation does **not** break the income identity: with `ps̄_C = Σ_g v_g·cs_g·ps_C(g) / Σ_g v_g·cs_g`, `collect_pool · ps̄_C = income_C` follows algebraically and `Σ_C ps̄_C = 1`, so `ps̄_C` is a legal share vector and one scalar per node still reproduces every collector's income exactly. | MODEL | derivation | REVISED | X170 |
| Y188 | Both inputs already exist per good at write time, and §2.6 sums exactly them into `collect_pool`. | MODEL | derivation | NEW | — |
| Y189 | **The real cost is that `ps̄_C` is not derivable from trade power alone**: it is value-weighted, so installing it means writing a country a fictitious per-node trade power whose ratio happens to equal it — and every other consumer of that power field then reads the fiction. | MODEL | derivation | NEW | — |
| Y190 | That is a claim about what the engine exposes, not about a magnitude, and it is why the single graph stays: on one graph the scalar **is** the country's power share, needing no invention. | DESIGN | derivation | NEW | — |
| Y191 | Every magnitude previous versions quoted here — v1–v3.0's "5.96 ducats on a node paying ~250" (which v4.0 deleted, its own harness asserting the deletion), v4.0's 0.41%, v5.0's "single-digit percent", v6.0's first draft's "at most 0.1%" — froze or reweighted the share differently, so each measured its own construction. | WORLD | derivation | REVISED | X173, X174 |
| Y192 | **No figure of the author's own is quoted here**, because the identity holds and the objection is structural; the size of any discrepancy depends on which collectors are taken to be collecting, which is a choice of the construction. | DESIGN | stipulated | REVISED | X172 |

## §3.11 — Caravan power · §3.12 — Treasure fleets (lines 1437–1473)

**UNCHANGED:** C531–C547, C556–C560, V163–V172. No delta claims.

## §3.13 — Open questions (lines 1475–1533)

**UNCHANGED:** C561–C585, V173, V174, V175, V178, V181, V182, V183, W164, X175, X177, X178, X179,
X180, X183.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y193 | The one open wealth question is now a **design** question rather than a classification one: should any source beyond province condition be allowed to multiply `goods_produced`? | DESIGN | stipulated | REVISED | X176 |
| Y194 | v3.0 through v5.0 tried to admit the province-scoped subset by rule, and that rule was wrong in both independent audits that examined it, which is why v6.0 drops it. | WORLD | derivation | REVISED | X176 |
| Y195 | ⚑ `trade_goods_size` and `trade_goods_size_modifier` are granted in **buildings, event modifiers, great projects, static and province-triggered modifiers, holy orders, state edicts and trade-company investments**. | ENGINE | file value | REVISED | X176 |
| Y196 | Re-admitting any of those sources re-admits the maintenance burden with it, and the question to settle first is whether the fidelity — about one percent of world wealth either way the ratio is taken — is worth it. | DESIGN | derivation | NEW | — |
| Y197 | Under the calibration's α = 16 the cloves demand order is `hangzhou`, `beijing`, `doab`, and the sink lands on a high-demand node rather than a geographic accident. | MODEL | numerical test | REVISED | X181 |
| Y198 | v2 said Beijing "holds the richest single province", which it does not — that is `hangzhou`. **No province-wealth figures are quoted.** | WORLD | numerical test | REVISED | X182 |

## §3.14 — AI merchant assignment (lines 1535–1552)

**UNCHANGED:** C586–C624, X184. No delta claims.

## §3.15 — Rejected (lines 1554–1664)

**UNCHANGED:** C625–C672 as carried by v2, V184–V188, V192–V199, V226, V227, V228.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y199 | The Laplacian entry **maintains no copy** of the contrast measurement: §3.2 carries it, and with v1's ε floor removed the demand side is the wider of the two. | MODEL | derivation | REVISED | X185 |
| Y200 | v3.0 and v4.0 repeated the 10⁷ / 10²–10³ ratio here while **v4.0's own §3.2** was withdrawing it. | WORLD | derivation | REVISED | X186 |
| Y201 | `cloves` has a single producer and so no contrast to measure at all — the sparsity point in miniature. | MODEL | derivation | NEW | — |
| Y202 | Ranked orientation wins the alignment statistics directionally — a far higher share of top-demand nodes in its sink sets than DRAIN — and loses delivery: a large share of world demand is stranded, it leaves orphan sinks a good cannot reach, it posts net-producer sinks where DRAIN, LAP and FLOW post none, and it keeps several times DRAIN's sinks per good. **No figures are carried.** | MODEL | derivation | REVISED | X187, X188 |
| Y203 | Seeded basin growth leaves demand unserved **at every tuning tried**, with no reach figure quoted. | MODEL | derivation | REVISED | X189 |
| Y204 | §3.15's `Φ_ord` entry maintains no figures and its "measured coherence ceiling any future aggregate should be compared against" role is withdrawn; the ceiling v2.0 and v2.1 quoted predates §3.6's deterministic sweep and was never regenerated. | DESIGN | stipulated | REVISED | X076, W063 |
| Y205 | The 3-mass gravity kernel reproduces whatever end count it is seeded with while γ is small enough and loses that property as γ approaches 1; **no figures are maintained**, and the rejection rests on three grounds none of which is numeric. | MODEL | derivation | REVISED | X190, X191 |

## §3.16 — Evidence standard (lines 1666–1728)

**UNCHANGED:** C677, C680–C682, C684, C685, V200–V203, V205–V210, W173–W181.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y206 | Implemented as written, v1's ε left the α = 1 identity's **residual at 1e-5 against v1's ε of 1e-6**, and would have been diagnosed as a solver bug. | MODEL | numerical test | REVISED | V204 |

---

# Prior IDs v6.0 leaves stranded

These propositions are deleted outright or stated to be wrong, with nothing in v6.0 taking their
place. They are recorded here rather than as rows, since a withdrawal issues no Y ID. Each was
checked against the v6.0 text.

| Group | Prior IDs | What v6.0 does |
|---|---|---|
| **The two-test classifier** | X030, X031, X032, W040 | The locality test, the wealth test, the trade-good-block instance argument and the local/owner rule are deleted with the classifier. §1.3 replaces them with three named inputs (Y028). |
| **The whole-install sweep's findings** | X035 *(partly, see Y032)*, X038, X039, X041, X042, X043, X044, X045, X046, X047, X048, X049, X050, X051, X052, X053, X054, X055, X056, X057, X058, W041, W045 | Great projects, permanent province modifiers, centres of trade, `production_leader`, `bonus_from_merchant_republics`, buildings, terrain/climate, the Leviathan gate, the "richest single province in the game", the tier rule and the glass/chinaware tension all leave the document. Two of them survive elsewhere in weaker form: glass's `local_production_efficiency` is still settled in §3.13 (X177), and 43 `gems` provinces still appear inside Y033. |
| **§1.6's band table** | X079, X080, X081, X082, X192, X193, X194, X195 | The four [1, 3] bands, the 0.001 refinement, the 8-seed noise analysis and the "a constant cannot sit inside a window narrower than the uncertainty in its own edges" principle are all deleted; one band (Y103) and one [1, 8] comparison (Y101) survive. |
| **§1.6's Europe demonstration** | X092, X093 | The nine-Lowland-province result and the random-versus-systematic noise contrast are gone. X085 and X088 are not stranded: Y106 replaces both, turning the "2% is the threshold" framing into a directional design claim. |
| **The one-sink field** | X071 | "v2 through v4's two-sink result was measured on a wealth field missing sixteen provinces" — v6.0 returns to two sinks, so the diagnosis it offered no longer holds. |
| **§3.10's magnitude claims** | X171 | "Thirteen orders of magnitude above the float residual and it moves income between countries" is deleted along with the per-collector percentages (X170, revised into Y187). |
| **Half-refuted** | W031 | "Neither coefficient is a define: `defines.lua` and `common/defines/` were searched and contain neither" — half of it survives (Y040) and half is refuted (Y038). |

Not stranded, though the deletions might suggest it: **W042** and **W044** survive, because §1.3
still names `gems`' `local_tax_modifier` and `incense`' `trade_value_modifier` as genuinely
province-scoped; **W067** survives in §1.9's own untouched paragraph and is weakened only in §2.7's
restatement (Y151); **W189** survives with a file path added; **X104**, **X110**, **X196**,
**X115**, **X184** are untouched.

---

# † Unresolvable IDs

**None.** Every `Replaces` target in this delta resolves to a specific C/V/W/X ID. The four prior
inventories' own † markers were not re-opened: v5.0's three unresolved C-ranges (X130, X133, X138
against C298–C342 and C353–C365) are inherited as they stand, and the two v6.0 rows that touch
those passages — Y154 (razed China) and Y153 (its ordering-robustness note) — record X130 as their
predecessor rather than reaching past it into the C range.
