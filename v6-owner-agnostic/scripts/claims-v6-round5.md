# Claim Inventory Delta — Per-Good Trade Network Spec v6.0

Extracted from `per-good-trade-spec.md` (v6.0, 1,678 lines) as a **delta against
`../v5-owner-agnostic/claims-v5.md`** (X001–X196), which is itself a delta against
`../v3-owner-agnostic/claims-v3.md` (W001–W195), `../v2-drain/claims-v2.md` (V001–V230) and
`../v1-laplacian/claims.md` (C001–C685). Extraction only: nothing here is validated, corrected or
commented on, and no claim below is assessed for truth, support or wording.

**Method.** The v6.0 spec was read in full — all 1,678 lines — and `claims-v5.md` in full (header,
all 196 rows and its own UNCHANGED lists). `changes-v6.md` was read for its 131 replacement entries
and used **only to locate changed passages**; every row below is read off the spec text itself.
`claims-v3.md` was read for the W-row texts needed to resolve `Replaces` targets in §1.3, §1.6,
§2.2a and §2.7; `claims-v2.md` and `claims.md` were grepped to resolve V138, V204, W063 and W067
rather than read whole.

*One thing about this file's IDs, because the project already contains Y numbers.* Four earlier
Y-numbered extractions sit in `scripts/` (`claims-v6-round1-clean.md`, `-round2`, `-round3`,
`-round4`, at 157, 143, 178 and 174 rows), each renumbered from Y001 against the draft it was taken
on; `validation-v6.md` grades the round-4 set. This file follows the same practice and renumbers
from Y001 in document order against the **final** text, which carries 17 replacements
(`changes-v6.md` entries 115–131) applied after that round-4 draft. Its Y IDs are therefore **not**
interchangeable with the round files' or with the Y IDs cited in `validation-v6.md`; the round-4 set
was used here as a coverage cross-check, not as a source.

**ID prefix.** v1 used `C`, v2 used `V`, v3 used `W`, v4 got no inventory, v5 used `X`.
**v6 uses `Y`**, numbered in document order.

**Statuses.** **UNCHANGED** — the same proposition as an existing C/V/W/X ID; the old ID is recorded
in the section's UNCHANGED line and no Y ID is issued. **REVISED** — the proposition changed; a new
Y ID with the old ID(s) in `Replaces`. **NEW** — no counterpart in any prior inventory. A
proposition stated in two sections keeps one ID at first appearance.

**Two extraction rules v6.0 exercises constantly.** (1) The "no maintained figures for any rejected
operator" convention deletes measurements while keeping the surrounding argument; where a row's
figure is withdrawn and only the direction survives, the proposition is weaker and is recorded as
**REVISED**, not UNCHANGED. (2) The "no empirical absolutes" convention rescopes claims ("the
highest in vanilla" → "the highest in the shipped price table"); a rescoping is also a proposition
change and is recorded as REVISED.

**Vocabularies carried over.** Type: ENGINE / MODEL / DESIGN / OUTCOME / WORLD. Provenance:
stipulated / derivation / file value / numerical test / engine test / prose source /
verified (method unstated) / UNSOURCED. `numerical test` (a solver or harness experiment) and
`engine test` (an observation of EU4 actually running) are kept strictly distinct; a parse of a
*save file* is recorded as `file value`, following claims-v5.md's treatment of X110.

**Markers.** **⚑** a claim introducing an engine fact no prior inventory carried. **§** a claim
whose stated evidence is a single observation. **†** a `Replaces` target believed to exist but not
pinnable to a specific ID.

---

# Summary

**184 delta claims extracted, Y001–Y184**, against the 196 v5 claims: **77 NEW, 107 REVISED**
(replacing **102 X IDs, 13 W IDs and 2 V IDs** — **117 distinct prior IDs**, and no C ID directly).

REVISED outnumbers NEW by three to two, which is the shape the two prose conventions force: a
version whose main work is deleting an input surface and stripping maintained figures rewrites more
propositions than it adds. The NEW rows are not evenly spread either — 24 of the 77 are §1.3's
start-state reads and 14 are §1.6's ordering analysis.

### Delta claims by status and Type

| Type | NEW | REVISED | Total |
|---|---|---|---|
| MODEL | 35 | 67 | 102 |
| DESIGN | 16 | 17 | 33 |
| ENGINE | 16 | 14 | 30 |
| WORLD | 9 | 8 | 17 |
| OUTCOME | 1 | 1 | 2 |
| **Total** | **77** | **107** | **184** |

### Delta claims by Provenance

| Provenance | Count |
|---|---|
| derivation | 71 |
| numerical test | 65 |
| file value | 24 |
| stipulated | 19 |
| engine test | 3 |
| prose source | 2 |
| verified (method unstated) | 0 |
| UNSOURCED | 0 |
| **Total** | **184** |

**No row carries UNSOURCED provenance.** Two rows carry `prose source` (Y004, Y010) and both are
claims about the project's own audit documents rather than about the game. **Only three rows carry
`engine test`** (Y036, Y039, Y041), all of them re-readings of the two tooltip sessions already in
the record: v6.0 adds no new game session, so every new measurement here is a file read, a save
parse, a solver run or a harness run. `derivation` overtaking `numerical test` is the same effect
seen from the other side — where v5.0 printed a figure, v6.0 often argues a direction.

**21 rows are marked ⚑** — engine facts no prior inventory carried, **15 of them NEW**. They cluster
in two places: §1.3's start-state reads (Y049, Y051, Y053–Y057, Y059, Y062 — the `on_startup` chain,
the `add_base_*` accumulation, the `is_city` non-filter and the rolled trade goods) and §3.5's
`change_price` census (Y152, Y154, Y155). The rest: Y033 (`GP_COEFF` located in a shipped file),
Y036/Y037 (the tax tooltip's arithmetic), Y039, Y041, Y045, Y046 (devastation's unsourced scaling),
Y065 (`base_tax` reaching 15) and Y113 (the three trading-policy cooldowns).

**Four rows are marked §** — evidence resting on a single observation: Y039, Y041, Y062, Y139. Down
from v5.0's five.

**No row needs a † marker.** Every `Replaces` target resolves to a specific C/V/W/X ID.

### Where the delta concentrates

| Section | Y rows | What drove it |
|---|---|---|
| §1.3 Demand | 44 | the classifier's deletion, the four province-state modifiers, and the three corrected start-state reads |
| §1.6 Aggregate graph | 42 | two sinks instead of one, the 100-relabelling ordering result, the withdrawn band table and the rewritten Europe table |
| §0 Front matter | 14 | the substantive change, the two prose conventions, and the harness's re-stated coverage |
| §2.4 The tradenodes file | 12 | Phase 2's degenerate LP as the reason for a canonical node order, and the conditional end-flag list |
| §3.10 Income factoring | 11 | the `ps̄_C` construction replacing every quoted per-good-propagation magnitude |
| §1.1 Trade direction | 8 | the post-fold reading of the fallback condition, and 1–8 sinks / mean 3.72 |
| §1.10 Direction-dependent systems | 7 | the trading-policy cooldowns and the caravan re-measurement |
| §2.2, §3.2, §3.5, §3.15 | 6 each | the withdrawn solve-cost range; the sparsity argument; the executable-versus-textual census; every rejected operator's figures deleted |
| §2.8 Validation, §3.13 | 5 each | regenerated razed-China rows; the wealth question restated as a design question |
| §3.9 | 4 | the adoption rationale restated without figures |
| §1.5 | 3 | the coal counterfactual |
| §2.2a, §2.3, §2.7, §3.4, §3.16 | 1 each | |

---

## §0 — Front matter (lines 1–54)

**UNCHANGED:** C002, C003, C004, V001 *(via §2.5)*, V002, V003, V004, W001, W002. *(The
"deleted text is quoted in `changes-vN.md`" pointer is a document reference and is not inventoried,
as in claims-v5.md.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y001 | v6.0's substantive change is to §1.3: **wealth is a function of the province's development, its trade good and its own current condition, and of nothing else**, so owner-agnosticism is true by construction rather than by a rule that has to be policed. | DESIGN | stipulated | REVISED | X002 |
| Y002 | The two-test modifier classifier and everything it governed — the trade-good modifiers, great projects, permanent province modifiers, buildings, centres of trade and the DLC conditionality — are **deleted**, along with the whole-install sweep that maintained them. | DESIGN | stipulated | REVISED | X030, X031, X033, X035 |
| Y003 | On the 1444 start that deleted apparatus was worth **105.30 ducats** — 0.98% of the 10,712.70 the field totalled with it, 0.99% of the 10,607.40 without. | MODEL | numerical test | NEW | — |
| Y004 | What it cost was an input surface whose classification was **wrong in both independent audits that examined it** — `../v3-owner-agnostic/validation-v3.md` W041 and `../v5-owner-agnostic/validation-v5.md` X030 and X034 — and which v4.0's own repair harness passed and v5.0 then refuted. | WORLD | prose source | REVISED | X034 |
| Y005 | Three start-state reads are corrected in the same pass: `on_startup` devastation, dated `add_base_*` accumulation, and the `is_city` filter the engine does not apply. | DESIGN | stipulated | NEW | — |
| Y006 | §2.4 now states the reason a canonical node order is a correctness requirement: **Phase 2's min-cost flow is degenerate**, so presentation order selects which optimum is returned. | MODEL | derivation | REVISED | X125 |
| Y007 | Prose convention: **no empirical absolutes** — no superlative, no universal quantifier and no threshold asserted as a fact about the world; a claim is either a directional design statement or an observation scoped to the field and script that produced it. | DESIGN | stipulated | NEW | — |
| Y008 | Prose convention: **no maintained figures for any rejected operator** — §3.15's graveyard keeps its design arguments and loses its measurements, covering `Φ_ord`, the gravity kernels, the v1 Laplacian, RANK and the seeded basins, because those numbers were re-measured and re-refuted in three successive audits and not one rejection argument depends on them. | DESIGN | stipulated | NEW | — |
| Y009 | Where a comparison is genuinely load-bearing it is stated as a **direction** ("scores higher on self-coherence", "does not concentrate its ends") rather than as a figure that has to be maintained across every change to the wealth field. | DESIGN | stipulated | NEW | — |
| Y010 | Every graded claim from `../v5-owner-agnostic/validation-v5.md` — **22 refuted, 39 partial, 1 unverifiable** — is folded through, and `fixes-agreed.md` maps each one to the change that answers it. | WORLD | prose source | REVISED | X001 |
| Y011 | Measured figures carry the script that produced them, and `scripts/verify6.py` reads figures **out of the document text** and fails when they disagree with a value computed from the install. | DESIGN | stipulated | REVISED | X004 |
| Y012 | The harness does **not** cover every figure the document prints: **under half** of them are guarded, and the rest rest on their script attribution alone. | WORLD | numerical test | NEW | — |
| Y013 | `scripts/coverage6.py` measures that honestly — it corrupts each spec-printed figure whether the harness looks at it or not — and it should be re-run rather than quoted, because the number moves with every edit to the document. | DESIGN | derivation | NEW | — |
| Y014 | `scripts/mutate6.py` reports a higher score that is **not** coverage: it plants errors only in figures `verify6.py` already checks, so it cannot fail — the same circularity v4.0's harness had, recorded here rather than quietly fixed. | WORLD | derivation | NEW | — |

## §1.1 — Trade direction (lines 58–163)

**UNCHANGED:** C005, C006, C010–C012, C019–C022, V005–V015, V017–V024, V026–V028, V031, V032,
V036, V037, W007–W011, W015–W022, X005, X006, X007, X012, X014, X015, X016, X017.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y015 | The fallback fires only when every candidate is support-isolated with zero **post-peel** balance — the balance Phase 0 hands on, each pendant's folded into its parent, not the raw input `b`. | MODEL | derivation | REVISED | X008 |
| Y016 | So the condition is about the folded field, and a map with non-zero raw balances can still reach the branch. | MODEL | derivation | NEW | — |
| Y017 | On a connected core the branch needs the folded balance to vanish across the core: per good, a component with no producer and no consumer; for the aggregate graph, every node's `Σ wealth^α_Φ` equal. | MODEL | derivation | REVISED | X009 |
| Y018 | Uniform *per-province* wealth does **not** deliver that, because nodes hold between **0 and 72** counted provinces, so equal provinces make unequal node sums. | MODEL | numerical test | NEW | — |
| Y019 | Where the wealth key then ties, the **node index** decides. | MODEL | derivation | REVISED | X010 |
| Y020 | §2.8 asserts containment over a set that includes the fallbacks because of **T3** — a fallback promotion that is a sink in neither the selected nor the promoted set — not because of the wealth tie, which is incidental to it; and the wealth tie is **not** the reason §2.4 requires a canonical node order, a requirement that is stronger and is set by Phase 2. | DESIGN | derivation | REVISED | X011 |
| Y021 | On 1444 the pendant and fallback cases are empty and the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods, **1–8 sinks per good, mean 3.72**, zero fallbacks. | MODEL | numerical test | REVISED | X013 |
| Y022 | That equality does not become a theorem by attaching conditions: "Phase 0 a no-op and no fallback firing" looks sufficient and is not — **T2** satisfies both and still breaks it. | MODEL | derivation | NEW | — |

## §1.2 — Supply (lines 165–176)

**UNCHANGED:** C023, C025–C028, V038, V039, V040, V041. No delta claims.

## §1.3 — Demand (lines 178–328) — full-strength extraction

**UNCHANGED:** C031, C032, C035, C036, C039, W024, W026, W030, W033, W042, W044, W051, X023,
X024, X025, X026, X036, X059, X060, X061, X062. *(X036's "43 `gems` provinces at 1444" survives
inside Y028 as an input to the 89-province total, though the modifier itself is no longer read. The
105.30-ducat / 0.99% figure this section restates is Y003 at first appearance in §0.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y023 | Wealth is owner-agnostic **and it reads three things about the province: its development, its trade good, and its own current condition** — a property of the *place*, what the land is worth per year before anyone's government touches it. | MODEL | stipulated | REVISED | W023 |
| Y024 | Two provinces with the same **development, trade good and condition** have the same wealth whoever owns them, and a province's wealth does not change when it is conquered. | MODEL | derivation | REVISED | W025 |
| Y025 | `base_tax`, `base_production` and the trade good are bare attributes of the place, so nothing about them needs classifying. | MODEL | derivation | NEW | — |
| Y026 | *What this gives up:* `gems`' `local_tax_modifier` and `incense`' `trade_value_modifier` are genuinely province-scoped and are no longer read, along with great projects, permanent province modifiers and the DLC state they depended on. | DESIGN | derivation | REVISED | X035 |
| Y027 | `incense`'s `trade_value_modifier` is live on **31** provinces at 1444. | ENGINE | file value | REVISED | X037 |
| Y028 | The deleted apparatus covered **89 of the 2,472** counted provinces — 43 `gems` plus 31 `incense` plus 16 great-project and permanent-modifier provinces, less one that is both (province 542). | MODEL | numerical test | NEW | — |
| Y029 | That count depends on the field: **87** under the withdrawn `is_city` filter, and 89 rather than 88 because province 4856 is one of the twenty whose good the engine rolls and it rolled `incense`. | MODEL | numerical test | NEW | — |
| Y030 | `goods_produced(p) = GP_COEFF · base_production(p) · (1 + Σ province-state goods modifiers)` — no flat-goods-bonus term. | MODEL | derivation | REVISED | X018 |
| Y031 | `trade_value(p) = goods_produced(p) · price(good(p))`, ducats per year — no local trade-value-modifier term. | MODEL | derivation | REVISED | X019 |
| Y032 | `tax_value(p) = TAX_COEFF · base_tax(p) · (1 + Σ province-state tax modifiers)`, ducats per year. | MODEL | derivation | REVISED | X020 |
| Y033 | ⚑ **`GP_COEFF` is a shipped file value**: `common/static_modifiers/00_static_modifiers.txt` carries `provincial_production_size = { trade_goods_size = 0.2 … }`, localised "Base Production" — the same tooltip line the coefficient was measured off. | ENGINE | file value | REVISED | W031, W089 |
| Y034 | It is therefore moddable and is **read at runtime**, not hardcoded. | DESIGN | stipulated | REVISED | W032, W090 |
| Y035 | `TAX_COEFF` is in no file that has been found — neither `defines.lua`, `common/defines/`, nor that static-modifier block — so it stays a measured constant carrying the observation that produced it. | ENGINE | file value | REVISED | W031 |
| Y036 | ⚑ The tax tooltip's schema is `Base: trunc(base_tax × 0.0833333) (Yearly base_tax)` — observed `Base: 0.49 (Yearly 6.00)` at `base_tax` 6 and `Base: 0.16 (Yearly 2.00)` at `base_tax` 2. | ENGINE | engine test | REVISED | X021 |
| Y037 | ⚑ The parenthetical is `base_tax` itself and the `Base` line is its truncated twelfth; it is **not** twelve times the displayed figure, which would give 5.88 and 1.92. | ENGINE | derivation | NEW | — |
| Y038 | v4.0 and v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both of its own data points; v3.0 carries neither that schema nor the 0.6125 arithmetic. | WORLD | derivation | NEW | — |
| Y039 | ⚑§ The monthly production tooltip's `Trade Value` line is **consistent with** the same relation on one observation, 3.52 → `+0.29`, which fixes the divisor only to within (11.73, 12.14]. | ENGINE | engine test | REVISED | X022 |
| Y040 | Both monthly figures being the annual value over twelve is what lets the annual forms add directly, and **the tax pair establishes it at two development levels**. | MODEL | derivation | REVISED | W036 |
| Y041 | ⚑§ `0.49 × 1.25` is 0.6125, which truncates to **0.61, not 0.62**, so the engine is not multiplying the displayed figure: it multiplies the untruncated monthly value — 6 × 0.0833… = 0.49999…, × 1.25 = 0.62499…, displayed 0.62. | ENGINE | engine test | REVISED | X027 |
| Y042 | The example establishes only the ordering — base from development first, percentage second — and nothing finer. | MODEL | derivation | NEW | — |
| Y043 | v4.0 and v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires rounding while §2.3 requires truncation; both cannot hold. | WORLD | derivation | NEW | — |
| Y044 | Flat goods bonuses *would* add into `goods_produced` before the price multiply — the tooltip carries an additive `Base Goods Produced` block above a multiplicative `Goods Produced Efficiency` block — but under §1.3 **no source grants one**, so the ordering is stated for the emitter's benefit and is exercised by no province in the model. | MODEL | derivation | REVISED | X028, X029 |
| Y045 | ⚑ **Province condition is the one thing besides development and the good that wealth reads:** four static modifiers, all read from `00_static_modifiers.txt` — `devastation` `trade_goods_size_modifier = -2` scaled by the devastation level, `prosperity` +0.25, `under_siege` −0.25, and `occupied` −0.5 **plus** `local_tax_modifier` −0.5. | ENGINE | file value | REVISED | X035, X040 |
| Y046 | ⚑ **No shipped file states that devastation's scaling is linear in the level**: the model assumes `-2 × level/100`, which is an assumption and not a file value, and `prosperity` is likewise applied as stated without a file confirming its direction. | MODEL | stipulated | NEW | — |
| Y047 | Only `occupied` touches the tax term; the other three reach `goods_produced` alone. | ENGINE | file value | NEW | — |
| Y048 | These four are what make the map answer to war: §1.2's volatility, §3.3's "a besieged province genuinely produces less" and §2.8's war rows all rest on them. | DESIGN | derivation | NEW | — |
| Y049 | ⚑ **Eleven counted provinces begin devastated at 1444** — Bohemia at 50, Erzgebirge and Moravia at 20 — and no province-history file says so: the devastation is applied by `on_startup`, which fires `flavor_boh.15` ("The Aftermath of the Hussite Wars"). | ENGINE | file value | REVISED | X040 |
| Y050 | That devastation costs **13.40 ducats** across the eleven affected counted provinces (`measure6.py`). | MODEL | numerical test | NEW | — |
| Y051 | ⚑ The chain is `common/on_actions/00_on_actions.txt` → `on_startup_effect` → `common/scripted_effects/01_scripted_effects_for_on_actions.txt` → `country_event flavor_boh.15`. | ENGINE | file value | NEW | — |
| Y052 | **The start state is what the engine produces, not what the history files say**, and that general point costs three separate reads. | DESIGN | derivation | NEW | — |
| Y053 | ⚑ `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`, `flavor_geo.1` and others directly from its own `events = { }` list in `00_on_actions.txt` — a second path alongside the `on_startup_effect` chain that carries `flavor_boh.15`. | ENGINE | file value | NEW | — |
| Y054 | ⚑ **Development itself does not move before the first tick:** the history parse matches the save on **2,472 of 2,472** provinces for `base_tax`, `base_production` and owner, and only `trade_goods` differs, on exactly twenty provinces. | ENGINE | file value | NEW | — |
| Y055 | ⚑ v6.0's first draft said `flavor_geo.1` carries `add_base_tax` and could move development pre-tick; it does not — its whole effect is legitimacy, a country modifier and a flag, and those keys sit in `flavor_geo.3`, which `on_startup` does not fire (a mission does). | ENGINE | file value | NEW | — |
| Y056 | ⚑ **`add_base_*` in a dated block before the start date accumulates:** province 1 (Uppland) has `base_tax = 5` undated plus 1 at `1436.4.28` and the game has 6, while v5.0 and earlier overwrote instead of adding and silently dropped the grant. | ENGINE | file value | NEW | — |
| Y057 | ⚑ **`is_city = yes` is not a filter the engine applies:** 20 owned provinces omit or comment out the line — province 265 among them, also one of the devastated eleven — and the engine treats them as cities. | ENGINE | file value | NEW | — |
| Y058 | The model counts a province when it has an owner **and lies in a trade node**: **2,472** provinces, not 2,452. | MODEL | derivation | REVISED | W050 |
| Y059 | ⚑ **Twenty counted provinces have no trade good in their history file** (`trade_goods = unknown`); the engine assigns one at start from each good's `chance = { }` block. | ENGINE | file value | NEW | — |
| Y060 | The model does not predict the draw — it **reads the good the engine actually rolled**, as it does for development, and prices the province on that. | DESIGN | stipulated | NEW | — |
| Y061 | Pricing those twenty at zero instead understates world wealth by **12.70 ducats**. | MODEL | numerical test | NEW | — |
| Y062 | ⚑§ On this save the twenty came up seven `fur`, five `grain`, three `wool`, two `livestock`, and one each of `cotton`, `incense` and `naval_supplies`. | ENGINE | file value | NEW | — |
| Y063 | A different roll gives a slightly different field, and nothing in the model depends on which one. | DESIGN | derivation | NEW | — |
| Y064 | `TAX_COEFF = 1.0`'s reference condition is applied to **every province the model counts**: ownership is not modelled, so every province is treated as cored and settled. | MODEL | derivation | REVISED | X063 |
| Y065 | ⚑ That is a modelling choice with a known cost: two readings, both on cored city provinces at `base_tax` 2 and 6, are all `TAX_COEFF = 1.0` rests on, and `base_tax` at 1444 runs up to **15** (province 1821), with total development reaching 33 there. | MODEL | file value | NEW | — |
| Y066 | Owner-agnosticism removes **a large** source of hidden owner-dependence from the aggregate graph (§1.6), which is built from this same wealth field. | MODEL | derivation | REVISED | W052 |

## §1.4 — Market concentration (lines 330–340)

**UNCHANGED:** C040–C047. No delta claims.

## §1.5 — Goods without a graph (lines 342–391)

**UNCHANGED:** C048, C051–C056, V050–V058, W053, W109, W182–W186, W188, W191.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y067 | Repricing to coal the **45** owned latent-coal provinces flips **10 of 159 `Φ_w` edges** and adds **214.60 ducats** to world wealth (`measure6.py`). | MODEL | numerical test | REVISED | X064 |
| Y068 | The counterfactual holds every non-repriced input fixed, and that matters by more than rounding: province 4237 is both latent-coal and one of the devastated eleven, so a reprice that also drops its devastation measures coal activating **plus** one province healing — worth 2.40 ducats and 3 extra flips. | MODEL | numerical test | NEW | — |
| Y069 | Coal's base price of 10.0 is the highest **in the shipped price table** (`common/prices/00_prices.txt`, `measure6.py`). | ENGINE | file value | REVISED | W189 |

## §1.6 — The aggregate graph (lines 393–544) — full-strength extraction

**UNCHANGED:** C059, C062, V063, V064, V212, V218, V221, W054, W055, W058, W064, X067, X091,
X095, X123. *(The per-good "1–8 sinks, mean 3.72, 0 fallbacks" line is Y021 at first appearance in
§1.1.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y070 | **Both the sink count and the sink locations move with the wealth field**, and `α_Φ` sets how sharply concentration is read. | MODEL | numerical test | REVISED | X065 |
| Y071 | At the stipulated α_Φ = 1.5 the 1444 field gives two sinks and a modestly grown Europe gives three or one, so neither the count nor the placement is fixed by the constant. | MODEL | numerical test | NEW | — |
| Y072 | v2.0–v4.0's "the count emerges from concentration exactly as per-good sink counts do" and v5.0's "the count is set by `α_Φ`" are wrong the same way: the count is a function of the field **and** the constant. | WORLD | derivation | NEW | — |
| Y073 | v2.1 chose `α_Φ` with a target count in view — a calibration §2.3 withdraws **without replacing**. | WORLD | derivation | REVISED | X066 |
| Y074 | Scaling `b` down breaks the orientation: identical orientation at ×1 and above, **12** edge flips at ×10⁻², and **100** at ×10⁻⁶, where the sink set also collapses to `{genua}` — so the sink set is not the quantity to watch here. | MODEL | numerical test | REVISED | X068 |
| Y075 | 1444's `b_w` has largest magnitude **0.0225**. | MODEL | numerical test | REVISED | X069 |
| Y076 | Measured at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and `hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12. | MODEL | numerical test | REVISED | X003, X070, X071 |
| Y077 | **One of those two is a property of the world and the other is a property of the node ordering**, and that difference matters more than the count. | MODEL | derivation | NEW | — |
| Y078 | Across 100 relabellings with `α_Φ` and every input held fixed the orientation changed **100 times**, a mean of **26 of 159 edges** moved, and the sink set came back exactly as `{english_channel, hangzhou}` **8 times**. | MODEL | numerical test | NEW | — |
| Y079 | Over those runs `hangzhou` was an end in **100 of 100** and `english_channel` in **40**, with `gulf_of_siam` holding an end in 55, `wien` in 37 and `sevilla` in 19; the count ranged **1 to 5**, most often 2. | MODEL | numerical test | NEW | — |
| Y080 | The rest of §1.6 is therefore **conditional on one canonical node order**, which §2.4 item 1 requires the emitter to fix — a statement about what kind of fact the European end is, not a caveat about precision. | DESIGN | derivation | NEW | — |
| Y081 | Phase 1 selects `genua`; both sinks arrive by stall promotion and `genua` ends a transit node, so there are **2 promotions and 0 fallbacks**. | MODEL | numerical test | REVISED | X072 |
| Y082 | **Eight sources**, all in the bottom half of the wealth field, `c_w` ranks **44–75**, mean degree **3.1** against the map's 4.0, which does not support v2's "cul-de-sacs". | MODEL | numerical test | REVISED | X073 |
| Y083 | Every node drains to a sink; acyclic, 159/159 oriented; and the sink set is unchanged under ±1% wealth noise on **three** seeds. | MODEL | numerical test | REVISED | X074, X093 |
| Y084 | **89.6%** of ordered node pairs (5,663 of 6,320) are connected by at least one good's directed path. | MODEL | numerical test | REVISED | X158 |
| Y085 | Agreement with the per-good graphs is **53.6%** of edge-goods and **52.3%** value-weighted. | MODEL | numerical test | REVISED | X075 |
| Y086 | The superseded marking-order aggregate scored **higher** on that measure, and no figure is maintained for an operator the model does not install. | MODEL | derivation | REVISED | X076 |
| Y087 | **`α_Φ = 1.5` is a stipulated design constant, exactly as `P₀ = 2.0` is:** superlinear so that a few very rich provinces outweigh a dense mediocre region, and round. | DESIGN | stipulated | REVISED | X083 |
| Y088 | It is **not** derived and the document no longer offers a derivation: both previously offered — v2.1–v4.0's two-sink calibration and v5.0's widest-band argument — are withdrawn. | DESIGN | derivation | REVISED | X122 |
| Y089 | Scanned over [1, 8] rather than [1, 3] the widest band is **1.71** wide ([3.50, 5.21], `{doab, genua, hangzhou}`), so 1.5's band is not the widest by any margin. | MODEL | numerical test | REVISED | X078 |
| Y090 | Across α_Φ = 1.00…8.00 at 0.01 the sink set is a step function, and α_Φ = 1.5 sits in the band **[1.38, 1.63], width 0.25**, which gives `{english_channel, hangzhou}`. | MODEL | numerical test | REVISED | X077, X081 |
| Y091 | Sampled at the six values v2 used, the count is non-monotone: **6 → 2 → 1 → 2 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}. | MODEL | numerical test | REVISED | X084 |
| Y092 | A standing warning to revisers: the 1444 map has two ends and vanilla's authored map has three, and 1.5 must **not** be justified by that resemblance — that is the calibration §2.3 withdrew. | DESIGN | stipulated | NEW | — |
| Y093 | **Europe becomes the centre of trade as it develops** — the design claim, and what §3.1's first goal asks the field to deliver. | DESIGN | stipulated | REVISED | X088 |
| Y094 | At 1444 the map already ends in the Channel and in Hangzhou; as European development compounds the Channel's basin grows and Asia's pole fades, and past a broad range of European growth Asia holds no end at all. | OUTCOME | numerical test | NEW | — |
| Y095 | The mechanism: wealth is linear in development, so developing a region moves its `c_w` share directly and `Φ_w`'s ends follow the wealth. | MODEL | derivation | NEW | — |
| Y096 | Europe-scaling observations on **824** counted European provinces (`europe.py`), α_Φ held at 1.5: ×1.00 gives `{english_channel, hangzhou}`; ×1.02 adds **`wien`**; ×1.56 gives `{english_channel, rheinland}` with Asia holding none; ×2.00 gives **`genua` alone**. | MODEL | numerical test | REVISED | X086, X087 |
| Y097 | Read the table as a direction rather than a trajectory, and on one node ordering: growth moves the ends westward and thins Asia's, and by ×2.00 a single Mediterranean end at `genua` holds the map. | MODEL | derivation | NEW | — |
| Y098 | *Which* European node holds an end at a given factor is ordering-dependent in the same way the 1444 set is — `english_channel` at ×1.02, `rheinland` at ×1.56 and `genua` at ×2.00 are this ordering's answers, not the world's — so the direction is the claim and the membership is not. | MODEL | numerical test | NEW | — |
| Y099 | These are properties of this snapshot, not constants of the model: they are what one field yielded under one scaling, and a different world state moves them. | DESIGN | stipulated | REVISED | X085 |
| Y100 | Because wealth is linear in development, **scaling development and scaling wealth are the same operation here** — maximum difference 0.0 across the European set — so the distinction that made v5.0's version of this table wrong does not arise. | MODEL | numerical test | NEW | — |
| Y101 | All three institutions the period is named for begin **in Europe** between 1450 and 1550 — Renaissance `1450.1.1` at Florence (116), Colonialism `1500.1.1` at Sevilla (224), Printing Press `1550.1.1` at Frankfurt (1876) — independently of any threshold. | ENGINE | file value | REVISED | X089 |
| Y102 | The Renaissance's embracement bonus is `development_cost = -0.05`, a standing discount on every subsequent development point. | ENGINE | file value | REVISED | X090 |
| Y103 | The 1444 route from Genoa to the Asian sink is the Silk Road: `genua → alexandria → aleppo → persia → lahore → **lhasa** → ganges_delta → burma → gulf_of_siam → canton → hangzhou`. | MODEL | numerical test | REVISED | X094 |
| Y104 | **No route leaves `english_channel` at all** — it is a sink with out-degree 0, so the Hansa and the Danube carry power *into* it, and v5.0's "from the Channel it is the Hansa and the Danube" described a path that does not exist. | MODEL | numerical test | REVISED | X096 |
| Y105 | **No Europe→sink route passes the Cape of Good Hope**, checked from `genua`, `north_sea` and `english_channel`. | OUTCOME | numerical test | REVISED | X097 |
| Y106 | The Cape is a live conduit, not an idle one: in-degree 1, out-degree 3, with **132 ordered node pairs** whose path runs through it (`measure6.py`), carrying Atlantic drainage into the Indian Ocean. | MODEL | numerical test | NEW | — |
| Y107 | v5.0's "nothing routes through the Cape" is false as a universal and was only ever checked on the Europe→sink routes. | WORLD | derivation | NEW | — |
| Y108 | In the per-good graphs the Cape also carries Asian spices to Europe; `Φ_w` models power, not cargo (§3.9). *(The specific per-good route v5.0 named is no longer asserted.)* | MODEL | numerical test | REVISED | X098 |
| Y109 | Scaling the 22 European **nodes** rather than European provinces makes `genua` the sole sink from about **×1.65**, and the 18-node western/central subset needs about **×2.15**. | MODEL | numerical test | REVISED | X099 |
| Y110 | Somewhere inside roughly **×2.9–×3.5** the Cape of Good Hope **reverses** — Atlantic→Cape→Indian-Ocean drainage becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast — and the reversal is bounded above as well as below, so it is a window and not a threshold, whose edges move with the field. | MODEL | numerical test | REVISED | X100 |
| Y111 | Dev-stacking a single node's top province concentrates the map on that node. *(v5.0's `hangzhou` ×20/×30/×50 figures are no longer carried.)* | MODEL | numerical test | REVISED | X101 |

## §1.7 — Merchants (546–572) · §1.8 — Collection and transfer (574–604) · §1.9 — Trade power propagation (606–615)

**UNCHANGED:** C067–C083, C084–C102, C103–C111, V066, V068–V072, V073, W065, W067 *(its
"descriptively false" clause; the "gains no qualifier" clause is revised at §2.7)*, W068, W069,
W192, X102, X103, X104. No delta claims.

## §1.10 — Direction-dependent systems (lines 617–673)

**UNCHANGED:** C112–C143, V074, V078, V079, V080, W070, W071, X105, X109, X110, X196.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y112 | **Banding absorbs very little chatter** — narrower than v5.0's "almost nothing absorbs threshold chatter", because the cooldowns below absorb some. | ENGINE | derivation | REVISED | X106 |
| Y113 | ⚑ **Banding is not the only damper:** `TRADING_POLICY_COOLDOWN_MONTHS = 12` applies to **seven of the nine entries** in `common/trading_policies/00_trading_policies.txt` — five distinct policies, four with an `_upgraded` twin, plus Propagate Religion which has none — including Propagate Religion, with `maximize_profit` and `maximize_profit_upgraded` carrying `cooldown = no`; and `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` pairs with `TRADE_COMPANY_COOLDOWN = 60`. | ENGINE | file value | NEW | — |
| Y114 | So a flickering share does not translate into a flickering *effect* at those three; what is left exposed is everything without a cooldown, which is most of the ladder. | ENGINE | derivation | NEW | — |
| Y115 | Measured on the 1444 start: the caravan cap of 50 is **9.4% to 47.0%** of an inland node's total trade power, median **21.6%** over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. | MODEL | numerical test | REVISED | X107 |
| Y116 | As a share of the node's total **after** the grant lands — 50/(total+50) — the same figures read **8.6% to 32.0%, median 17.7%**. | MODEL | numerical test | NEW | — |
| Y117 | v5.0 quoted the after-grant figures under the before-grant description, which cannot be right: 8.6% of 532.0 is 45.8 rather than 50. | WORLD | derivation | NEW | — |
| Y118 | On §2.2's derived 25-node inland basis the median is **21.3%**, or 17.5% after the grant. | MODEL | numerical test | REVISED | X108 |

## §1.11 — Treasure fleets (675–681) · §1.12 — What the game displays (683–702)

**UNCHANGED:** C144–C148, C149–C165, V049, V065, V081. No delta claims.

## §2.1 — Shape (lines 706–723)

**UNCHANGED:** C167–C184, V082–V085, W072, W073. No delta claims.

## §2.2 — Solver (lines 725–767)

**UNCHANGED:** C185–C209, V091, V092, V229, W075, W076, X115.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y119 | Solver item 4 computes `TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production · (1 + province-state goods modifiers) · price`, with no autonomy, efficiency, ideas or owner terms. | DESIGN | stipulated | REVISED | X111 |
| Y120 | The only modifiers the solver reads are the four that describe the province's own condition, and at 1444 only `devastation` is live, on eleven provinces. | DESIGN | stipulated | REVISED | X112 |
| Y121 | World wealth is **10,607.40** annual ducats over **2,472** counted provinces. | MODEL | numerical test | REVISED | X113 |
| Y122 | Measured on the reference implementation (scipy/HiGHS plus the deterministic sweep, one machine): **of order 0.1 s for all 29 goods, and single-digit milliseconds per good on average** — and that is the whole of the claim. | MODEL | numerical test | REVISED | X114 |
| Y123 | Repeated 12-run experiments on one machine do not reproduce each other closely enough to support anything finer: three replicates gave per-good averages spanning **3.5–10.5, 3.5–10.8 and 3.1–4.7 ms**, so no range is quoted, because the quantity measured is a machine and a scheduler rather than the algorithm. | MODEL | numerical test | NEW | — |
| Y124 | Of v5.0's "0.17–0.21 s for all 29 goods": across three replicates of twelve runs, the number of runs landing inside that interval was **1, then 0, then 0**. | WORLD | numerical test | NEW | — |

## §2.2a — What map this is for (lines 769–809)

**UNCHANGED:** W077–W085, W088, X116.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y125 | Where Phase 0 acts, free-edge **determinism** survives but **index-independence does not**: the key reads the post-fold balance β, so peeling can create exact ties the raw balances do not have, and the 1444 zero-ties measurement does not transfer. | MODEL | derivation | REVISED | W086, X117 |

## §2.3 — Constants (lines 811–861)

**UNCHANGED:** C211–C227, V094, W091, W096, W097, W098, X118, X119, X120, X121, and the
DLC-third-axis claim. *(§2.3's `GP_COEFF`-is-a-file-value and `TAX_COEFF`-in-no-file statements are
Y033/Y035 at first appearance in §1.3; its α_Φ paragraph is Y087/Y088 at first appearance in §1.6.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y126 | v3.0 through v5.0 said neither wealth coefficient was in a file, and shipped a whole-install modifier sweep that walked past the block holding one of them. | WORLD | derivation | NEW | — |

## §2.4 — The tradenodes file (lines 863–931)

**UNCHANGED:** C228–C233, C235–C242, V095, V148, W099–W107, W114, X124, X127.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y127 | The min-cost b-flow is **massively degenerate**: many distinct supports carry the same optimal cost, and which one the solver returns depends on the order the nodes and arcs are presented in. | MODEL | derivation | NEW | — |
| Y128 | Measured on 1444, relabelling the nodes and running end-to-end changed the orientation on **580 of 580** runs (29 goods × 20 relabellings), **always** by returning a different optimal vertex and **never** by a sweep tiebreak, with a mean of **22.1 of 159 edges** moving and the objective identical to 8.9e-16. | MODEL | numerical test | NEW | — |
| Y129 | Permuting only the **arc** presentation order with node labels held fixed changes the optimal support on **10 of 10 goods** tested, with objective gaps ≤ 1.8e-15. | MODEL | numerical test | NEW | — |
| Y130 | Twenty-two flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event. | MODEL | derivation | NEW | — |
| Y131 | The canonical order must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks ties in. | DESIGN | derivation | REVISED | X125 |
| Y132 | Everything §1.6 and §2.8 report about stability is measured **at fixed node order**; re-order the same world and the map moves, with `α_Φ` and every input held fixed. | MODEL | derivation | NEW | — |
| Y133 | The 580/580 result is HiGHS-specific in its detail but not in kind: any simplex returns *a* vertex of a degenerate optimal face. | MODEL | derivation | NEW | — |
| Y134 | Making the orientation independent of presentation order would need a tie-breaking objective — a lexicographic secondary cost or a strictly convex perturbation — which is a design change and is not adopted here. | DESIGN | stipulated | NEW | — |
| Y135 | The priority key ties in **more places than §1.1 documents**: besides the free-edge sweep it decides Phase 1's within-cluster argmin, the stall promotion's identical form, and the top-k cut when two clusters carry equal mass. | MODEL | derivation | NEW | — |
| Y136 | **None of those tie sites fires on 1444** — zero exact `(DEF, β)` ties on free edges across 29/29 goods, zero within-cluster β ties, zero tied cluster masses — so no measured figure here depends on them. | MODEL | numerical test | NEW | — |
| Y137 | The end-flag list is **a function of the canonical node order required by item 1, not of the world alone**: on the 1444 field `hangzhou` is an end under every ordering tried, `english_channel` under about 40% of them, and the count ranges 1 to 5, so changing the order changes the flags without anything in the world changing. | DESIGN | numerical test | NEW | — |
| Y138 | End flags: `end=yes` on every `Φ_w` sink, and 1444 in the shipped order has **two** end nodes, `english_channel` and `hangzhou`, against vanilla's three. | DESIGN | numerical test | REVISED | X126 |

## §2.5 — Runtime attachment (933–937) · §2.6 — Writing to the engine (939–959)

**UNCHANGED:** C243–C250, C251–C272. No delta claims.

## §2.7 — Probes (lines 961–999)

**UNCHANGED:** C274–C293, V098–V101, W108–W113.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y139 | § Probe 15 is **one observation on one node** — enough to retire §3.16's cautionary case and not enough to promote §1.9's "every immediately upstream node" to a measurement, which is weaker than v3.0's "correct as written and gains no qualifier". | WORLD | derivation | REVISED | W067 |

## §2.8 — Validation (lines 1001–1043)

**UNCHANGED:** C298–C342, V109–V112, W116, W117, W119, W193, W194, W195, X128, X133, X134, X135,
X136, X137. *(The latent-good row's 10-of-159 figure is Y067 and the agreement figures are Y085, at
first appearance in §1.5 and §1.6.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y140 | Most goods, 1444: sinks are 1 to 8 per good, and high-demand nodes are sinks at **16.8%** in the top demand decile against 6.9% in the bottom. | MODEL | numerical test | REVISED | X129 |
| Y141 | The razed-China row is **ordering-robust where §1.6's sink membership is not**: it turns on `hangzhou` holding an end, which it does under every relabelling tried. | MODEL | numerical test | NEW | — |
| Y142 | Zeroing `hangzhou`-node development relocates an end in one solve: the `Φ_w` sinks move from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`, with **22 of 159** edges flipping. | MODEL | numerical test | REVISED | X130 |
| Y143 | `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth **226.7 against 143.0**, and it holds the richest single province the model counts. | MODEL | numerical test | REVISED | X131 |
| Y144 | Zeroing `beijing` **also** moves the map — **15 flips** — because deleting a percent of world wealth renormalises `c_w` everywhere; what separates the two cases is which node keeps its end, not whether the map moves. | MODEL | numerical test | REVISED | X132 |

## §2.9 — Build order (1045–1056) · §3.1 — Goals (1060–1068)

**UNCHANGED:** C343–C352, C353–C365, V113, X138. No delta claims.

## §3.2 — Why a flow and a drainage sweep (lines 1070–1177)

**UNCHANGED:** C366, C370–C375, C383–C385, V115, V116, V118–V122, V124, V128–V131, W120, W123,
W125–W128, X139, X141, X146, X147, X148, X149, X150.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y145 | **What the contrast-ratio metric cannot see is the thing the diagnosis rests on:** most nodes produce nothing at all of a given good, so `(c−s)/deg` is dominated by *where* supply exists rather than by how large it is, and a max/min ratio over producing nodes is blind to that by construction. *(v5.0's 36-against-482.2 spices figures are no longer carried.)* | MODEL | derivation | REVISED | X140 |
| Y146 | Better wealth inputs move Genoa to a **co-sink at roughly ×1.7** without making demand the determinant of placement. | MODEL | numerical test | REVISED | X142 |
| Y147 | Moving the spice sink to a Chinese node takes a multiple of that node's demand **in the region of 3.6–4.9×** — observed on the 1444 field: `beijing` 3.61×, `hangzhou` 4.12×, `xian` 4.60×, `canton` 4.77×. | MODEL | numerical test | REVISED | X143 |
| Y148 | The multiple a node needs and the share of world demand it then buys **do not line up end to end**, because the share depends on where the node started; other nodes in the region need more still. *(v5.0's girin/yumen/chengdu/lhasa 4.0–10.8× range and its 9.3–21.4% demand shares are no longer carried.)* | MODEL | derivation | REVISED | X143, X144 |
| Y149 | Sink placement is a measurement **on one input**, and v5.0's attempted rescue by two conditions fails: those conditions are necessary, not sufficient, since T2 satisfies both and still breaks the equality. | MODEL | numerical test | REVISED | X145 |
| Y150 | **None of the key-tie sites is why §2.4 requires a canonical node order** — that requirement comes from Phase 2's degenerate LP, which moves the orientation under relabelling even when no key tie exists anywhere. | MODEL | derivation | REVISED | X151 |

## §3.3 — Why wealth, and why per province (lines 1179–1200)

**UNCHANGED:** C386–C406, C408, C412, C413, V132, V133, V135, W132–W139. No delta claims.

## §3.4 — Why supply is pre-modifier (lines 1202–1212)

**UNCHANGED:** C415–C423, V137, V139, W140, W141, W142.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y151 | In v1 the production-income substitution broke the α = 1 identity, measured as orientation agreement collapsing to **well under half the map**. *(The 159/159 → 68/159 figure is no longer carried.)* | MODEL | numerical test | REVISED | V138 |

## §3.5 — Why α is anchored absolutely (lines 1214–1255)

**UNCHANGED:** C427–C442, V140–V144, V147, X152, X153, X156, X157.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y152 | ⚑ **`change_price` values are fractions of the good's base price, not ducats**, settled by the shipped save `tutorial/eu4_tutorial_chapter10.eu4`: `paper` sits at `current_price = 4.375` on a base of 3.5 (× 1.25, not + 0.25) and `gems` at 5.000 on a base of 4.0. | ENGINE | file value | NEW | — |
| Y153 | The install carries **161 textual** `change_price` blocks — 93 in `events/`, 14 in `missions/`, 1 in `common/`, 53 in `history/` of which 13 are negative (all in `history/countries/HAB - Austria.txt`), and **none in `decisions/`**. | ENGINE | file value | REVISED | X154 |
| Y154 | ⚑ **Ten of the 161 never execute:** four sit inside `effect_tooltip = "…"` strings, three inside the `effect = "…"` string of a `country_event_with_effect_insight`, and three inside `tooltip = { }` display wrappers — so **151 are executable**. | ENGINE | file value | NEW | — |
| Y155 | ⚑ Six of the seven quoted blocks duplicate a block already counted in `events/`, and the seventh names a price key no event in the install ever sets. | ENGINE | file value | NEW | — |
| Y156 | All ten are positive and every negative block in the install is executable, so the sublinear-reachability partition is **identical under either census**. | ENGINE | derivation | NEW | — |
| Y157 | v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them; both were wrong about which number was the executable one, v5.0's claimed per-file count assertion existed nowhere in its toolchain, and the mechanical cause is that `pdx.py` tokenises a quoted string as one opaque unit so a `change_price` inside a tooltip string is invisible to the walker. | WORLD | derivation | REVISED | X155 |

## §3.6 — Why no hysteresis (1257–1292) · §3.7 — Why eligibility is per good (1294–1300) · §3.8 — Why gates evaluate true (1302–1320)

**UNCHANGED:** C443–C446, C449, C452, C463–C473, C474–C497, V148, V152, V154, V155–V158,
W147–W152, W154. No delta claims. *(§3.8's 89.6% reachability census is Y084 at first appearance in
§1.6.)*

## §3.9 — Why `Φ_w` is the installed graph (lines 1322–1366)

**UNCHANGED:** C502, C505–C510, C512, V160, V161, V162, V218, V221, V228, X161.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y158 | `genua`, `gulf_of_siam` and `sevilla` rank **4th, 3rd and 7th** by node wealth on the corrected field (`mexico` is 2nd) — 296.0, **297.9** and 266.5 against `english_channel`'s 316.6, **which is a sink** — and a rich non-sink draws more edges in than it sends out even though flow passes through. | MODEL | numerical test | REVISED | X159 |
| Y159 | `Φ_ord` is acyclic for free and scores **higher** than `Φ_w` on self-coherence — the acknowledged, undisputed cost of the trade — and was superseded on design grounds: its ends are sweep-scheduling artifacts rather than places, a majority terminate no good at all, none of the demand capitals is among them, and its end count does not concentrate as demand concentrates. **No figure is maintained for it.** | MODEL | derivation | REVISED | X160 |
| Y160 | v2.1–v4.0's "two vanilla-like ends at 1444" is not the adoption argument and should not be revived even though the 1444 field again gives two ends: the count is a property of the field, not of the operator, and pinning the operator to it would be the withdrawn calibration. | WORLD | derivation | REVISED | X162 |
| Y161 | What the trade costs is **self-coherence with the per-good graphs** (no figure quoted); what it buys is one operator, one set of guarantees, and ends that sit where the wealth is. | DESIGN | derivation | REVISED | X163 |

## §3.10 — Why the engine's economy is overwritten (lines 1368–1385)

**UNCHANGED:** C513–C521, C523–C525, C528–C530, X164, X165, X167.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y162 | The two forms agree to a worst relative disagreement of 0 to 3.7e-16 — **one to three** units in the last place. | MODEL | numerical test | REVISED | X166 |
| Y163 | Propagation is kept on a single graph, **and the reason is not the one v1 through v6.0's own first draft gave**: reading the one installed graph leaves the propagated term good-independent, so the identity holds by construction and in doubles to within one to three ULP. | MODEL | derivation | REVISED | X168 |
| Y164 | Per-good propagation makes a country's power at the node differ by good, because §1.9 reads a node's downstream neighbours and those differ per good: `gulf_of_siam`'s 29 goods leave it by **seven** distinct downstream sets. | MODEL | numerical test | REVISED | X169 |
| Y165 | **That does not break the identity:** with `ps̄_C = Σ_g v_g·cs_g·ps_C(g) / Σ_g v_g·cs_g`, `collect_pool · ps̄_C = income_C` follows algebraically and `Σ_C ps̄_C = 1`, so `ps̄_C` is a legal share vector and one scalar per node still reproduces every collector's income exactly. | MODEL | derivation | REVISED | X170, X171 |
| Y166 | Both inputs already exist per good at write time, and §2.6 sums exactly them into `collect_pool`. | MODEL | derivation | NEW | — |
| Y167 | **The real cost is that `ps̄_C` is not derivable from trade power alone:** it is value-weighted, so installing it means writing a country a fictitious per-node trade power whose ratio happens to equal it, and every other consumer of that power field then reads the fiction. | MODEL | derivation | NEW | — |
| Y168 | That is a claim about what the engine exposes, not about a magnitude, and it is why the single graph stays: on one graph the scalar **is** the country's power share, needing no invention. | DESIGN | derivation | REVISED | X172 |
| Y169 | Every magnitude previous versions quoted here was an artifact of substituting some other weighting — v1–v4.0's "5.96 ducats on a node paying ~250", v4.0's 0.41%, v5.0's "redistributive and single-digit percent", and v6.0's own first draft's "at most 0.1%" — so each measured its own construction rather than a property of the design. | WORLD | derivation | REVISED | X174 |
| Y170 | The size of the discrepancy also depends on which collectors are taken to be collecting, which is a choice of the construction too. | DESIGN | derivation | NEW | — |
| Y171 | **No figure of my own is quoted here**, because the identity holds and the objection is structural. | DESIGN | stipulated | NEW | — |
| Y172 | No node in the model has local trade value near 250. *(v5.0's "the largest is 112.6" is no longer carried.)* | MODEL | numerical test | REVISED | X173 |

## §3.11 — Why caravan power needs a condition added (1387–1408) · §3.12 — Why treasure fleets are always granted (1410–1423)

**UNCHANGED:** C531–C547, C556–C560, V163–V172. No delta claims.

## §3.13 — Open questions (lines 1425–1483)

**UNCHANGED:** C561–C585, V173, V174, V175, V178, V181, V182, V183, W164, X175, X177, X178, X179,
X180, X183. *(The 105.30-ducat figure this section restates is Y003 at first appearance in §0, and
"wrong in both independent audits" is Y004.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y173 | The one open wealth question is now a **design** question rather than a classification one: *should any source beyond province condition be allowed to multiply `goods_produced`?* — because §1.3 reads development, the trade good and the four province-state modifiers and nothing else. | DESIGN | derivation | REVISED | X176 |
| Y174 | `trade_goods_size` and `trade_goods_size_modifier` are granted in many places — buildings, event modifiers, great projects, static and province-triggered modifiers, holy orders, state edicts, trade-company investments — and v3.0 through v5.0 tried to admit the province-scoped subset by rule. | ENGINE | file value | REVISED | X176 |
| Y175 | Re-admitting any of those sources means re-admitting the maintenance burden with it, so the question to settle first is whether the fidelity is worth it. | DESIGN | derivation | NEW | — |
| Y176 | Under the calibration's α = 16 the cloves demand order is `hangzhou`, `beijing`, `doab`, and the sink lands on a **high-demand node rather than a geographic accident**. | MODEL | numerical test | REVISED | X181 |
| Y177 | `hangzhou`, not Beijing, holds the richest single province. *(v5.0's 30.4-against-19.5 figures are no longer carried.)* | MODEL | numerical test | REVISED | X182 |

## §3.14 — AI merchant assignment (lines 1485–1502)

**UNCHANGED:** C586–C624, X184. No delta claims.

## §3.15 — Rejected (lines 1504–1614)

**UNCHANGED:** C625–C672 as carried by v2, V184–V188, V192–V199, V226, V227, V228.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y178 | With v1's ε floor removed the demand side is the wider of the two, not the supply side, and **this entry maintains no copy of the measurement** (§3.2 carries it); `cloves` has a single producer and so no contrast to measure at all, which is the sparsity point in miniature. | MODEL | derivation | REVISED | X185 |
| Y179 | v3.0 and v4.0 repeated the 10⁷ / 10²–10³ ratio here while **v4.0's own** §3.2 was withdrawing it. | WORLD | derivation | REVISED | X186 |
| Y180 | Ranked orientation wins the sink–demand **alignment** statistics — it puts a far higher share of top-demand nodes in its sink sets than DRAIN — and loses delivery: a large share of world demand stranded, orphan sinks a good cannot reach, net-producer sinks where DRAIN, LAP and FLOW post none, and several times DRAIN's sinks per good. **No figures maintained.** | MODEL | derivation | REVISED | X187, X188 |
| Y181 | Seeded basin growth leaves demand unserved **at every tuning tried**. *(The 88.4%-at-best-tuning figure is no longer carried.)* | MODEL | derivation | REVISED | X189 |
| Y182 | `Φ_ord` as the installed graph: the most self-coherent aggregate measured and acyclic for free, superseded on design grounds, with **no figures maintained** — and the self-coherence ceiling v2.0 and v2.1 quoted predates the deterministic sweep of §3.6 and was never regenerated after it. | MODEL | derivation | REVISED | W063 |
| Y183 | The 3-mass gravity kernel **reproduces whatever end count it is seeded with while γ is small enough and loses that property as γ approaches 1**, with no figures maintained, and is rejected on three grounds none of which is numeric: it pins the end count by fiat, it needs a second operator with its own reach knob γ, and a pure `wealth^α` edge comparison with no reach term does not concentrate ends at all because a local wealth maximum survives every positive α. | MODEL | derivation | REVISED | X190, X191 |

## §3.16 — Evidence standard (lines 1616–1678)

**UNCHANGED:** C677, C680–C682, C684, C685, V200–V203, V206–V210, W173–W181.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y184 | Implemented as written, the α = 1 identity's residual reached **1e-5 against v1's ε of 1e-6**, and would have been diagnosed as a solver bug. | MODEL | numerical test | REVISED | V204 |

---

# Prior IDs v6.0 leaves stranded

Recorded for continuity with `claims-v5.md`'s section (b). These propositions are **withdrawn** —
deleted, or stated to be wrong — and **no Y ID replaces them**. Extraction only: no judgement is
offered on whether withdrawing them was right.

*(Four v5 IDs whose deletion v6.0 states in so many words are **not** listed here, because a Y row
names them: X030, X031 and X033 in Y002's `Replaces`, and X034 in Y004's. The rows below are the
ones the document simply stops carrying.)*

| Withdrawn IDs | What they said | Why they are gone |
|---|---|---|
| **X032** | the engine's trade-good data model is one *instance* of the locality test | there is no locality test left to instantiate |
| **X038, X039** | great-project `province_modifiers` (6 provinces) and undated `add_permanent_province_modifier` (10 provinces) are local and enter wealth | no longer read (Y026) |
| **X041, X042** | `glass` `local_production_efficiency` and `chinaware` `local_autonomy` are local but do not enter wealth | the classification is deleted; the glass finding survives as X177 in §3.13 |
| **X043–X047** | 361 centre-of-trade provinces; `production_leader`; `bonus_from_merchant_republics`; buildings local-but-empty; `terrain.txt` and the climate modifiers | the whole-install sweep that produced them is deleted |
| **X048–X054** | the great-project `starting_tier` rule, 85-of-130 gating, the six projects, province 1821 as the richest, the tier-versus-owner-action argument, and the six permanent-modifier keys | ditto |
| **X055, X056, X057** | `stora_kopparberget_modifier`'s Leviathan gate, the 3.0-versus-5.0 consequence, and "every wealth figure was measured with Leviathan installed" | "Leviathan" does not occur in the v6.0 spec |
| **X058** | glass and chinaware are the whole of the rule-versus-vocabulary tension | no rule, no tension |
| **X079, X080, X082, X192, X193, X194, X195** | the three narrower α_Φ bands, the [1.406, 1.424] window refined to 0.001, its noise behaviour at 8 seeds, the wide bands' 0.28–0.51 widths, the principle that a constant cannot sit inside a window narrower than its own edge uncertainty, and the "it shrinks rather than disappears" correction | the band table is replaced by a single band (Y090) and the retention argument is withdrawn (Y088) |
| **X092** | developing the nine Lowland provinces by ×1.20 makes `english_channel` a sink through ×10 | the Europe demonstration is rebuilt around Y096 |

Two further v5.0 propositions are **absorbed rather than withdrawn**: X071 (v2–v4's two-sink result
was measured on a field missing sixteen provinces) is folded into Y076's `Replaces`, since v6.0
reports two sinks again; and X093's random-noise half survives inside Y083 while its "+2% to Europe
alone changes the sink set" half does not.

---

# † Unresolvable IDs

**None.** Every `Replaces` target in this delta resolves to a specific C/V/W/X ID. Four lineages
that needed resolving were settled by grepping the older inventories rather than reading them:
§3.4's collapsed α = 1 identity figure is **V138**; §3.16's ε-instantiation residual is **V204**;
§3.15's `Φ_ord` coherence ceiling is **W063**; and §2.7's weakened probe-15 conclusion is **W067**,
whose "descriptively false" clause survives unchanged in §1.9 while its "gains no qualifier" clause
is what Y139 replaces.

---

# Extraction notes

Four things about this delta that a later reader would otherwise have to rediscover. None is a
judgement on the spec.

1. **Six prior IDs are named by more than one Y row, deliberately**, because v6.0 splits what an
   earlier version stated as one row: **X035** (Y002, Y026, Y045), **X040** (Y045, Y049), **X125**
   (Y006, Y131), **X143** (Y147, Y148), **X176** (Y173, Y174) and **W031** (Y033, Y035). That is why
   the 107 REVISED rows name only 117 distinct predecessors between them rather than more.
2. **Y082 returns to a pre-v5 proposition.** "Eight sources, `c_w` ranks 44–75, mean degree 3.1" is
   word-for-word W060's claim, which v5.0 had replaced with a seven-source figure (X073). It is
   recorded as REVISED against X073 — the live claim it changes — rather than UNCHANGED against W060.
3. **Rows whose only change is a deleted figure are REVISED.** Y111, Y148, Y151, Y172, Y177, Y178,
   Y180, Y181, Y182 and Y183 keep their predecessors' arguments and drop their numbers under §0's
   third convention; per the extraction rule in the header, a weaker proposition is a changed
   proposition.
4. **Three §0 rows are about the project's own verification tooling** (Y012, Y013, Y014) and are
   typed WORLD or DESIGN rather than MODEL, following claims-v5.md's treatment of X004. Y012's
   "under half" is the only figure in this delta whose own source says it should be re-run rather
   than quoted.
