# Claim Inventory Delta — Per-Good Trade Network Spec v6.0

Extracted from `per-good-trade-spec.md` (v6.0, 1,699 lines / 147,947 bytes, 42 headings) as a
**delta against `../v5-owner-agnostic/claims-v5.md`** (X001–X196), which is itself a delta against
`../v3-owner-agnostic/claims-v3.md` (W001–W195), `../v2-drain/claims-v2.md` (V001–V230) and
`../v1-laplacian/claims.md` (C001–C685). Extraction only: nothing here is validated, corrected or
graded. Each row records what the document asserts, its Type, its Provenance, and how it relates to
the prior inventories.

**Method.** Three documents were read in full: the v6.0 spec, `claims-v5.md`, and the complete
v5.0→v6.0 text diff (35 hunks, 528 added and 332 removed lines), computed here rather than taken
from `changes-v6.md` so that every changed proposition could be read in its final form.
`changes-v6.md` was consulted only for its header — it describes a 1,608-line intermediate, so the
spec has moved past it — and is not a source for any row. `claims-v3.md`, `claims-v2.md` and
`claims.md` were grepped to resolve specific prior IDs (W025, W031, W032, W036, W050, W052, W067,
W089–W091, W189, V132, V138, V204, V225) rather than read whole.

**ID prefix.** v1 used `C`, v2 used `V`, v3 used `W`, v4 got no inventory, v5 used `X`.
**v6 uses `Y`**, numbered in document order.

**Statuses.** UNCHANGED — the same proposition as an existing C/V/W/X ID; the old ID is recorded in
the section preamble and no Y ID is issued. REVISED — the proposition changed; a new Y ID with the
old ID(s) in `Replaces`. NEW — no counterpart in any prior inventory. A proposition stated in two
sections keeps one ID at first appearance; later restatements are noted in the preamble. Swapping a
script attribution (`v5measure.py` → `measure6.py`) is **not** a proposition change; deleting a
figure and replacing it with a direction **is**.

**Vocabularies carried over.** Type: ENGINE (how EU4 behaves) / MODEL (the mathematical model) /
DESIGN (a stipulation, goal or choice) / OUTCOME (what the built mod will produce in play) / WORLD
(truth-apt claims about history or about the project's own review history). Provenance: stipulated /
derivation / file value / numerical test / engine test / prose source / verified (method unstated) /
UNSOURCED. `numerical test` (a solver or harness experiment) and `engine test` (an observation of
EU4 actually running) are kept strictly distinct.

**Markers.** **⚑** a row introducing an engine fact no prior inventory carried. **§** a row whose
stated evidence is a single observation. **†** a `Replaces` target believed to exist but not pinned
to a specific ID.

---

# Summary

**188 delta claims extracted, Y001–Y188** against the 196 v5 claims: **86 NEW, 102 REVISED**,
replacing **108 distinct prior IDs** — 96 X, 9 W (W025, W031, W032, W036, W050, W052, W067, W089,
W090) and 3 V (V138, V204, V225). Ten of those prior IDs are replaced by more than one Y row,
because v6.0 splits several v5.0 propositions apart: X040 by three rows (the four modifiers, their
tax reach, and the eleven devastated provinces that refute "all zero at 1444"), X065 by three (count,
placement, and the two prior mis-statements), and X063, X078, X125, X155, X176, X182, W031 and W050
by two each.

### Delta claims by status and Type

| Type | NEW | REVISED | Total |
|---|---|---|---|
| MODEL | 33 | 64 | 97 |
| DESIGN | 20 | 17 | 37 |
| ENGINE | 18 | 10 | 28 |
| WORLD | 14 | 10 | 24 |
| OUTCOME | 1 | 1 | 2 |
| **Total** | **86** | **102** | **188** |

### Delta claims by Provenance

| Provenance | NEW | REVISED | Total |
|---|---|---|---|
| numerical test | 22 | 48 | 70 |
| derivation | 32 | 28 | 60 |
| stipulated | 13 | 15 | 28 |
| file value | 18 | 7 | 25 |
| engine test | 0 | 4 | 4 |
| verified (method unstated) | 1 | 0 | 1 |
| prose source | 0 | 0 | 0 |
| UNSOURCED | 0 | 0 | 0 |
| **Total** | **86** | **102** | **188** |

**No row in this delta carries UNSOURCED provenance**, as in v5.0. One row carries
`verified (method unstated)` — **Y015**, §0's statement that a script is named about a dozen times
against roughly three times that many unguarded figures, which names no script and no count. It is
the only figure-bearing claim in the document whose own method is unstated, and it is a claim about
the document rather than about EU4.

**23 rows are marked ⚑** — new engine facts; **16 of them are NEW**. The concentration has moved:
where v5.0's ⚑ rows clustered in a whole-install *modifier* sweep, v6.0's cluster in the **start
state** (`on_startup` events, dated `add_base_*` accumulation, the absent `is_city` filter, the
twenty rolled trade goods, the eleven devastated provinces — Y052, Y053, Y056, Y057, Y059, Y060,
Y061, Y063, Y066) and in **rate limiters and file locations no prior inventory carried** (the three
cooldown defines Y116–Y119, `GP_COEFF`'s static-modifier block Y036, the ten non-executing
`change_price` blocks Y159, `cape_of_good_hope`'s sea-zone member Y155).

**Three rows are marked §** — evidence resting on a single observation: **Y041** (the production
tooltip's divisor, fixed only to within (11.73, 12.14] on one reading), **Y066** (the twenty rolled
goods on one save), and **Y143** (probe 15's propagation observation, which v6.0 now says explicitly
is not enough to promote §1.9's rule to a measurement). Down from v5.0's five, and the reduction is
the document's own doing: v6.0 re-describes X027's and X021's single tooltip readings as
arithmetic-bearing observations with the arithmetic worked (Y039, Y043) rather than as bare readings.

**No † markers.** Every `Replaces` target resolves to a specific ID.

### Where the delta concentrates

| Section | Y rows | What drove it |
|---|---|---|
| §1.3 Demand | 45 | the classifier's deletion, the three corrected start-state reads, the four province-condition modifiers, the twenty rolled goods, and the coefficient-provenance split |
| §1.6 Aggregate graph | 42 | two sinks instead of one, the 800-relabelling ordering study, the [1, 8] α_Φ scan replacing the band table, the rewritten Europe table and the corrected 1444 routes |
| §0 Front matter | 17 | the two prose conventions, the verification-coverage honesty block, and the three harness scripts |
| §2.4 The tradenodes file | 11 | Phase 2's degeneracy as the reason for a canonical node order, the 400-of-400 relabelling result, and the other places the priority key ties |
| §1.10, §3.5, §3.10 | 9 each | the trading-policy cooldowns and the caravan-share correction; the `change_price` fraction finding and the executable-block census; the `ps̄_C` argument replacing the per-good-propagation error table |
| §1.1 Trade direction | 8 | the post-peel balance condition and the demotion of sink-set equality to a one-input measurement |
| §2.2, §3.2 | 6 each | the wealth pipeline and the de-quantified solve cost; the sparsity restatement and the Chinese-node wealth multiples |
| §2.8, §3.13 | 5 each | regenerated validation rows and the razed-China ordering note; the open question reframed as a design question |
| §3.9, §3.15 | 4 each | the adoption argument restated as a direction; four rejected operators de-quantified |
| §1.5 | 2 | the coal reprice re-measured, with its devastation confound named |
| §2.2a, §2.3, §2.7, §3.3, §3.4, §3.16 | 1 each | |

Eighteen sections carry no delta claims at all and are textually identical to v5.0: §1.2, §1.4, §1.7,
§1.8, §1.9, §1.11, §1.12, §2.1, §2.5, §2.6, §2.9, §3.1, §3.6, §3.7, §3.8, §3.11, §3.12, §3.14.

---

## §0 — Front matter (lines 1–57)

**UNCHANGED:** C002, C003, C004, V001 *(via §2.5)*, V002, V003, W001, W002 — the target patch, the
v1→v2.1 lineage, the fold-through of `../v1-laplacian/validation.md`, and the three-section shape.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y001 | v6.0's substantive change is to §1.3: **wealth is a function of the province's development, its trade good and its own current condition, and of nothing else** — owner-agnosticism made true by construction rather than by a rule that has to be policed. | DESIGN | stipulated | REVISED | X002 |
| Y002 | The two-test modifier classifier and everything it governed — trade-good modifiers, great projects, permanent province modifiers, buildings, centres of trade, the DLC conditionality — are deleted, along with the whole-install sweep that maintained them. | DESIGN | stipulated | REVISED | X030, X031, X033 |
| Y003 | The deleted apparatus is dated by version: the two-test classifier is v4.0's, v3.0 used a structural rule about which block of a trade-good definition a modifier sits in, and the whole-install sweep is v5.0's alone. | WORLD | derivation | NEW | — |
| Y004 | On the 1444 start that apparatus was worth **105.30 ducats** — 0.98% of the 10,712.70 the field totalled with it, 0.99% of the 10,607.40 without. | MODEL | numerical test | NEW | — |
| Y005 | What it cost was an input surface whose classification was **wrong in both independent audits that examined it** — `validation-v3.md` W041 and `validation-v5.md` X035 — and passed by v4.0's own repair harness, which v5.0 then refuted. | WORLD | derivation | NEW | — |
| Y006 | Three start-state reads are corrected in the same pass: `on_startup` devastation, dated `add_base_*` accumulation, and the `is_city` filter the engine does not apply. | DESIGN | stipulated | NEW | — |
| Y007 | **Phase 2's min-cost flow is degenerate, so presentation order selects which optimum is returned** — that, and not any tiebreak in the sweep, is why a canonical node order is a correctness requirement (§2.4). | MODEL | numerical test | REVISED | X125 |
| Y008 | Prose convention: **no empirical absolutes** — no superlative, no universal quantifier and no threshold asserted as a fact about the world; a claim is either a directional design statement or an observation scoped to the field and script that produced it. | DESIGN | stipulated | NEW | — |
| Y009 | Prose convention: **no maintained figures for any rejected operator** — §3.15 keeps its design arguments and loses its measurements, covering `Φ_ord`, the gravity kernels, the v1 Laplacian, RANK, the seeded basins and anything else the section rejects. | DESIGN | stipulated | NEW | — |
| Y010 | Those rejected-operator numbers were re-measured and re-refuted in three successive audits, and not one of the rejection arguments depends on them. | WORLD | derivation | NEW | — |
| Y011 | Where a comparison is genuinely load-bearing it is stated as a direction ("scores higher on self-coherence", "does not concentrate its ends") rather than as a figure that has to be maintained across every change to the wealth field. | DESIGN | stipulated | NEW | — |
| Y012 | Every graded claim from `validation-v5.md` — **22 refuted, 39 partial, 1 unverifiable** — is folded through, and `fixes-agreed.md` maps each one to the change that answers it. | WORLD | stipulated | REVISED | X001 |
| Y013 | `scripts/verify6.py` reads figures **out of the document text** and fails when they disagree with a value computed from the install. | DESIGN | stipulated | NEW | — |
| Y014 | It does **not** cover every figure the document prints: **under half** of the printed figures are guarded, and the remainder are not all covered by anything else. | WORLD | numerical test | REVISED | X004 |
| Y015 | A script is named about a dozen times against roughly three times that many unguarded figures, and some of the most recent additions carry neither a guard nor an attribution. | WORLD | verified (method unstated) | NEW | — |
| Y016 | `scripts/coverage6.py` measures that honestly — it corrupts each spec-printed figure whether the harness looks at it or not — and should be re-run rather than quoted, because the number moves with every edit to the document. | DESIGN | stipulated | NEW | — |
| Y017 | `scripts/mutate6.py` reports a higher score and is not coverage: it plants errors only in figures `verify6.py` already checks, so it cannot fail — the same circularity v4.0's harness had, recorded rather than quietly fixed. | WORLD | derivation | NEW | — |

## §1.1 — Trade direction (lines 61–167)

**UNCHANGED:** C005, C006, C010–C012, C019–C022, V005–V015, V017–V024, V026–V028, V031, V032, V036,
V037, W007–W011, W015–W022, X005, X006, X007, X012, X014, X015, X016, X017 — the four phases, the
fallback branch itself, the candidate definition, the sink taxonomy, T1/T2/T3 as the three breakers,
scan-invariance, and the free-edge determinism measurement.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y018 | The fallback fires only when every candidate is support-isolated with zero **post-peel** balance. | MODEL | derivation | REVISED | X008 |
| Y019 | The balance the priority key reads is the one Phase 0 hands on, with each pendant's balance folded into its parent — not the raw input `b` — so the condition is about the folded field, and a map with non-zero raw balances can still reach the branch. | MODEL | derivation | NEW | — |
| Y020 | On a connected core the folded balance must vanish across the core: for a per-good graph that is a component with no producer and no consumer, and for the aggregate graph it needs each node's `Σ wealth^α_Φ` to be equal — which uniform *per-province* wealth does **not** give. | MODEL | derivation | REVISED | X009 |
| Y021 | ⚑ Nodes hold between **0 and 72** counted provinces, so equal per-province wealth makes unequal node sums. | ENGINE | file value | NEW | — |
| Y022 | Where the wealth key ties, the **node index decides** — stated without v5.0's claim that the tied candidates are usually all zero-wealth. | MODEL | derivation | REVISED | X010 |
| Y023 | The containment set §2.8 asserts includes the fallbacks because of **T3**, not because of the wealth tie, which is incidental to it; and that is **not** the reason §2.4 requires a canonical node order, which is a stronger requirement set by Phase 2. | DESIGN | derivation | REVISED | X011 |
| Y024 | On 1444 the fallback and pendant cases are empty and the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods, **1–8 sinks per good, mean 3.72**, zero fallbacks. | MODEL | numerical test | REVISED | X013 |
| Y025 | That equality is **a measurement on this input, not a theorem**, and it does not become one by attaching conditions: "Phase 0 a no-op and no fallback firing" looks sufficient and is not — **T2** satisfies both and still breaks it. | MODEL | numerical test | REVISED | X145 |

## §1.2 — Supply (lines 168–180)

**UNCHANGED:** C023, C025–C028, V038, V039, V040, V041. No delta claims — the section is textually
identical to v5.0, including the `00_static_modifiers.txt` attribution for the four volatility
modifiers.

## §1.3 — Demand (lines 181–332) — full-strength extraction

**UNCHANGED:** C031, C032, C033, C035, C036, C039, W023, W024, W026, W033, W051, X023, X024, X025,
X026, X059, X060, X061, X062 — wealth as a property of the place, the excluded-by-name list, the
shared time basis, the two-province measurement parenthetical and its ruler-personality caveat, the
not-local exclusion list, `Core`/`City` already inside `TAX_COEFF`, and the itemised-percentage sum.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y026 | Wealth **reads three things about the province**: its development, its trade good, and its own current condition. | MODEL | stipulated | NEW | — |
| Y027 | Two provinces with the same **development, trade good and condition** have the same wealth whoever owns them (v5.0 said terrain, development and trade good). | MODEL | derivation | REVISED | W025 |
| Y028 | Owner-agnosticism is **true by construction here, not by a rule that has to be policed** — the classifier was a large surface to keep correct. | DESIGN | stipulated | NEW | — |
| Y029 | `base_tax`, `base_production` and the trade good are bare attributes of the place, so nothing about them needs classifying. | MODEL | derivation | NEW | — |
| Y030 | *What this gives up:* `gems`' `local_tax_modifier` and `incense`' `trade_value_modifier` are genuinely province-scoped and are no longer read, along with great projects, permanent province modifiers and the DLC state they depended on. | DESIGN | stipulated | REVISED | X035 |
| Y031 | The deleted apparatus covered **89 of the 2,472** counted provinces — 43 `gems` plus **31** `incense` plus 16 great-project and permanent-modifier provinces, less one that is both (province 542). | MODEL | numerical test | REVISED | X036, X037 |
| Y032 | The count depends on the field: it is **87** under the withdrawn `is_city` filter, and 89 rather than 88 because province **4856** is one of the twenty whose good the engine rolls, and it rolled `incense`. | MODEL | numerical test | NEW | — |
| Y033 | `goods_produced(p) = GP_COEFF · base_production(p) · (1 + Σ province-state goods modifiers)` — no flat-goods-bonus term. | MODEL | derivation | REVISED | X018 |
| Y034 | `trade_value(p) = goods_produced(p) · price(good(p))`, ducats per year — **no trade-value-modifier term at all**. | MODEL | derivation | REVISED | X019 |
| Y035 | `tax_value(p) = TAX_COEFF · base_tax(p) · (1 + Σ province-state tax modifiers)`, ducats per year. | MODEL | derivation | REVISED | X020 |
| Y036 | ⚑ **`GP_COEFF` is a shipped file value**: `common/static_modifiers/00_static_modifiers.txt` carries `provincial_production_size = { trade_goods_size = 0.2 … }`, localised "Base Production" — the same tooltip line the coefficient was measured off. | ENGINE | file value | REVISED | W031, W089 |
| Y037 | It is therefore moddable and is **read at runtime**, not hardcoded. | DESIGN | derivation | REVISED | W032, W090 |
| Y038 | `TAX_COEFF` is in **no file that has been found** — neither `defines.lua`, `common/defines/`, nor that static-modifier block — so it stays a measured constant carrying the observation that produced it. | ENGINE | file value | REVISED | W031 |
| Y039 | ⚑ The tax tooltip reads `Base: trunc(base_tax × 0.0833333) (Yearly base_tax)`: the parenthetical is `base_tax` itself and the `Base` line its truncated twelfth — **not** twelve times the displayed figure, which would give 5.88 and 1.92 on the two observations. | ENGINE | engine test | REVISED | X021 |
| Y040 | v4.0 and v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both of its own data points; v3.0 carries neither that schema nor the 0.6125 arithmetic. | WORLD | derivation | NEW | — |
| Y041 | ⚑§ The monthly production tooltip's `Trade Value` line is **consistent with** the same relation on one observation, 3.52 → `+0.29`, which fixes the divisor only to within **(11.73, 12.14]**. | ENGINE | engine test | REVISED | X022 |
| Y042 | Both monthly figures being the annual value over twelve is what lets the annual forms add directly, and **the tax pair establishes it at two development levels**. | MODEL | derivation | REVISED | W036 |
| Y043 | ⚑ Observed on Garnatah: `base_tax` 6 with `Tax Income Efficiency 125.0%` displays `Base 0.49` then `0.62`. **0.49 × 1.25 = 0.6125 truncates to 0.61**, so the engine is not multiplying the displayed figure — it multiplies the untruncated monthly value, 0.49999… × 1.25 = 0.62499…, displayed 0.62. | ENGINE | engine test | REVISED | X027 |
| Y044 | The example establishes the ordering — base from development first, percentage second — **and nothing finer**. | DESIGN | derivation | NEW | — |
| Y045 | v4.0 and v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires rounding while §2.3 requires truncation; both cannot hold. | WORLD | derivation | NEW | — |
| Y046 | Flat goods bonuses *would* add into `goods_produced` before the price multiply — the tooltip carries an additive `Base Goods Produced` block above a multiplicative `Goods Produced Efficiency` block — but **under §1.3 no source grants one**, so the ordering is stated for the emitter's benefit and is exercised by no province in the model. | MODEL | derivation | REVISED | X028, X029 |
| Y047 | **Province condition is the one thing besides development and the good that wealth reads**: four static modifiers describe a province's own state, and all four are read from `common/static_modifiers/00_static_modifiers.txt`. | MODEL | stipulated | REVISED | X040 |
| Y048 | The four are `devastation` (`trade_goods_size_modifier = -2`, scaled by the devastation level), `prosperity` (+0.25), `under_siege` (−0.25) and `occupied` (`trade_goods_size_modifier = -0.5` **and** `local_tax_modifier = -0.5`). | ENGINE | file value | REVISED | X040 |
| Y049 | **The `devastation` scaling law is in no shipped file:** the model assumes the modifier applies in proportion to the level, `-2 × level/100`, and that proportionality is an assumption rather than a file value. | MODEL | stipulated | NEW | — |
| Y050 | Only `occupied` touches the tax term; the other three reach `goods_produced` alone. | ENGINE | derivation | NEW | — |
| Y051 | These four are what make the map answer to war — §1.2's volatility and §3.3's "a besieged province genuinely produces less" both rest on them, and §2.8's war rows are their test. | DESIGN | derivation | NEW | — |
| Y052 | ⚑ **They are not all quiet at the 1444 start.** Eleven counted provinces begin devastated — Bohemia at 50, Erzgebirge and Moravia at 20 — and no province-history file says so. | ENGINE | file value | REVISED | X040 |
| Y053 | ⚑ The devastation is applied by `on_startup`, which fires `flavor_boh.15` ("The Aftermath of the Hussite Wars"), by the chain `common/on_actions/00_on_actions.txt` → `on_startup_effect` → `common/scripted_effects/01_scripted_effects_for_on_actions.txt`. | ENGINE | file value | NEW | — |
| Y054 | It costs **13.40 ducats** across the eleven affected counted provinces (`measure6.py`). | MODEL | numerical test | NEW | — |
| Y055 | **The start state is what the engine produces, not what the history files say** — the general form of the point, and it costs three separate reads. | DESIGN | derivation | NEW | — |
| Y056 | ⚑ `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`, `flavor_geo.1` and others directly from its own `events = { }` list in `00_on_actions.txt` — a second path alongside the `on_startup_effect` chain. | ENGINE | file value | NEW | — |
| Y057 | ⚑ **Development itself does not move before the first tick:** the history parse matches the save on **2,472 of 2,472** provinces for `base_tax`, `base_production` and owner, and only `trade_goods` differs, on exactly twenty provinces. | ENGINE | file value | NEW | — |
| Y058 | v6.0's first draft said `flavor_geo.1` carries `add_base_tax` and could move development pre-tick; it does not — its whole effect is legitimacy, a country modifier and a flag, and those keys are in `flavor_geo.3`, which `on_startup` does not fire. | WORLD | file value | NEW | — |
| Y059 | ⚑ **`add_base_*` in a dated block before the start date accumulates**, and v5.0 and earlier overwrote instead of adding, silently dropping the grant. | ENGINE | file value | NEW | — |
| Y060 | ⚑ Province 1 (Uppland) has `base_tax = 5` undated plus 1 at `1436.4.28`; the game has 6. | ENGINE | file value | NEW | — |
| Y061 | ⚑ **`is_city = yes` is not a filter the engine applies:** 20 owned provinces omit or comment out the line — province 265 is one, and it is also one of the devastated eleven — and the engine treats them as cities. | ENGINE | file value | REVISED | X063, W050 |
| Y062 | The model counts a province when it has an owner and lies in a trade node — **2,472** provinces, not 2,452 — and unowned provinces stay outside because they produce nothing the trade system can move. | MODEL | stipulated | REVISED | W050 |
| Y063 | ⚑ **Twenty counted provinces have no trade good in their history file** (`trade_goods = unknown`); the engine assigns one at start from each good's `chance = { }` block. | ENGINE | file value | NEW | — |
| Y064 | The model does not predict the draw — it **reads the good the engine actually rolled**, as it does for development, and prices the province on that. | DESIGN | stipulated | NEW | — |
| Y065 | Pricing those twenty at zero instead understates world wealth by **12.70 ducats**. | MODEL | numerical test | NEW | — |
| Y066 | ⚑§ The field is therefore one sample: on this save the twenty came up seven `fur`, five `grain`, three `wool`, two `livestock`, and one each of `cotton`, `incense` and `naval_supplies`. | ENGINE | file value | NEW | — |
| Y067 | A different roll gives a slightly different field, and nothing in the model depends on which one. | DESIGN | derivation | NEW | — |
| Y068 | The model applies `TAX_COEFF` to every province it counts: ownership is not modelled, so every province is treated as **cored and settled**, and carrying either term again would double-count it. | MODEL | derivation | REVISED | X063 |
| Y069 | ⚑ That is a modelling choice with a known cost: `TAX_COEFF = 1.0` rests on two readings at `base_tax` 2 and 6, while `base_tax` at 1444 runs up to **15** (province 1821), with total development reaching **33** there. | WORLD | file value | NEW | — |
| Y070 | The change removes **a large** source of hidden owner-dependence from the aggregate graph — no longer "the single largest". | MODEL | derivation | REVISED | W052 |

## §1.4 — Market concentration (lines 333–344)

**UNCHANGED:** C040–C047. No delta claims.

## §1.5 — Goods without a graph (lines 345–395)

**UNCHANGED:** C048, C051–C056, V050–V058, W053, W182–W186, W188, W189, W191 — including coal's base
price of 10.0 being the highest in the shipped price table, now sourced to
`common/prices/00_prices.txt` (a provenance addition, not a proposition change).

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y071 | Measured: repricing to coal the 45 owned latent-coal provinces flips **10 of 159 `Φ_w` edges** and adds **214.60 ducats** to world wealth (`measure6.py`). | MODEL | numerical test | REVISED | X064 |
| Y072 | The counterfactual holds every non-repriced input fixed, which matters by more than rounding: province **4237** is both latent-coal and one of the devastated eleven, so a reprice that drops its devastation measures coal activating **plus** one province healing — worth 2.40 ducats and 3 extra flips. | MODEL | numerical test | NEW | — |

## §1.6 — The aggregate graph (lines 396–562) — full-strength extraction

**UNCHANGED:** C059, C062, V063, V064, V212, V218, V221, W054, W055, W058, W063, W064, X066, X067,
X089, X090, X091, X095, X098 — the `Φ_w` definition, the scale argument's exact-arithmetic half, the
marking-order-as-potential result, v2.1's target-count choice, the three institutions' start dates
and provinces, the Renaissance embracement bonus and its country scope, the Volga route, and the
Cape's per-good spice carriage.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y073 | **Both the sink count and the sink locations move with the wealth field, and `α_Φ` sets how sharply concentration is read.** | MODEL | derivation | REVISED | X065 |
| Y074 | At the stipulated α_Φ = 1.5 the 1444 field gives **two** sinks, and a modestly grown Europe gives three or one, so neither the count nor the placement is fixed by the constant. | MODEL | numerical test | REVISED | X065 |
| Y075 | v2.0–v4.0's "the count emerges from concentration" and v5.0's "the count is set by `α_Φ`" are **wrong the same way**: the count is a function of the field **and** the constant. | WORLD | derivation | REVISED | X065 |
| Y076 | Measured: identical orientation at ×1 and above, **12 edge flips at ×10⁻² and 100 at ×10⁻⁶**, where the sink set also collapses to `{genua}`. | MODEL | numerical test | REVISED | X068 |
| Y077 | 1444's `b_w` has largest magnitude **0.0225**. | MODEL | numerical test | REVISED | X069 |
| Y078 | Measured at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and `hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12. | MODEL | numerical test | REVISED | X070 |
| Y079 | **One of those two is a property of the world and the other is a property of the node ordering**, and the difference matters more than the count. | MODEL | derivation | NEW | — |
| Y080 | Over **800 relabellings** — eight seeds of 100, `α_Φ` and every input held fixed (`relabel6.py`) — the orientation changed every time, a mean of **25 of 159** edges moved, and the sink set came back exactly `{english_channel, hangzhou}` in **64 of 800** runs. | MODEL | numerical test | NEW | — |
| Y081 | `hangzhou` was an end in about **98%** of them and `english_channel` in about **40%**. | MODEL | numerical test | NEW | — |
| Y082 | The Asian end is the robust one — not invariant, since orderings exist where it loses its end, but near enough that it is a fact about that node. | MODEL | numerical test | NEW | — |
| Y083 | After `english_channel` the most frequent ends are `gulf_of_siam` (a little over half the runs), `wien` (about a third), then `rheinland` and `sevilla`; the count itself ranged **1 to 5**, most often 2 or 3. | MODEL | numerical test | NEW | — |
| Y084 | The two leading proportions are quoted to two figures and the trailing ones qualitatively because that is as far as the sample supports: across three independent 800-trial sets `hangzhou` came in at **784–789** and `english_channel` at **322–336**, `sevilla` ranged 79–117 and `rheinland` 112–136, and a per-seed range would be a function of which seeds are drawn. | MODEL | numerical test | NEW | — |
| Y085 | Conditional on the node order: the sink set's membership and size, and everything derived from them — §2.4's end-flag list, and which European node holds an end in the growth table. | DESIGN | derivation | NEW | — |
| Y086 | Not conditional over the same relabellings: the map is fully oriented (159/159) and acyclic every time, no fallback ever fires, and the LP objective is identical to within **4.44e-16** — different *optimal* orientations rather than different answers. | MODEL | numerical test | NEW | — |
| Y087 | Phase 1 selects `genua`; both sinks arrive by stall promotion and `genua` ends a transit node, so there are **2 promotions and 0 fallbacks**. | MODEL | numerical test | REVISED | X072 |
| Y088 | **Eight sources**, all in the bottom half of the wealth field, `c_w` ranks **44–75**, mean degree **3.1** against the map's 4.0 — and v2's "cul-de-sacs" is not supported by those degrees. | MODEL | numerical test | REVISED | X073 |
| Y089 | Every node drains to a sink; acyclic, 159/159 oriented; the sink set is unchanged under ±1% wealth noise on **three** seeds. | MODEL | numerical test | REVISED | X074 |
| Y090 | **89.6%** of ordered node pairs (**5,663 of 6,320**) are connected by at least one good's directed path. | MODEL | numerical test | REVISED | X158 |
| Y091 | Agreement with the per-good graphs is **53.6%** of edge-goods (**52.3%** value-weighted). | MODEL | numerical test | REVISED | X075 |
| Y092 | The superseded marking-order aggregate scored **higher** on that measure, and the document no longer maintains a figure for an operator the model does not install. | DESIGN | stipulated | REVISED | X076 |
| Y093 | `α_Φ = 1.5` is a **stipulated** design constant exactly as `P₀ = 2.0` is: superlinear so a few very rich provinces outweigh a dense mediocre region, and round. | DESIGN | stipulated | REVISED | X083 |
| Y094 | The document **no longer offers any derivation** for it: v2.1–v4.0's two-sink calibration was fitted to a field that no longer exists, and v5.0's widest-band ground depended on where the α scan was truncated. | WORLD | derivation | REVISED | X122 |
| Y095 | Scanned over [1, 8] rather than [1, 3], the widest band is **1.71** wide — [3.50, 5.21], `{doab, genua, hangzhou}` — and 1.5's is not the widest by any margin. | MODEL | numerical test | REVISED | X078, X082 |
| Y096 | Across α_Φ = 1.00…8.00 at 0.01 the sink set is a step function, and 1.5 sits in the band **[1.38, 1.63], width 0.25**, which gives `{english_channel, hangzhou}`. | MODEL | numerical test | REVISED | X077, X078 |
| Y097 | Sampled at the six values v2 used, the count is non-monotone: **6 → 2 → 1 → 2 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}. | MODEL | numerical test | REVISED | X084 |
| Y098 | A standing warning: the 1444 map has two ends and vanilla's authored map has three, and 1.5 must **not** be justified by that resemblance — that is the calibration §2.3 withdrew, and §3.9's adoption argument does not rest on it. | DESIGN | stipulated | NEW | — |
| Y099 | **"Europe becomes the centre of trade as it develops"** is the design claim, and it is what §3.1's first goal asks the field to deliver. | DESIGN | stipulated | REVISED | X085 |
| Y100 | The Channel's basin grows from **18 nodes to 28** by about **×1.44**. | MODEL | numerical test | NEW | — |
| Y101 | `genua` first holds an end at **×1.63** and is the sole end from ×1.64 through ×2.00, and past a broad range of European growth Asia holds no end at all. | MODEL | numerical test | NEW | — |
| Y102 | The mechanism carries it: wealth is linear in development, so developing a region moves its `c_w` share directly and `Φ_w`'s ends follow the wealth. | MODEL | derivation | NEW | — |
| Y103 | Growth table, holding α_Φ = 1.5 and scaling European development only (`europe.py`, **824** counted European provinces): ×1.00 → `{english_channel, hangzhou}`; ×1.02 → adds **`wien`**; ×1.56 → `{english_channel, rheinland}` with Asia holding none; ×2.00 → `genua` alone. | MODEL | numerical test | REVISED | X086, X087 |
| Y104 | Read the table as a **direction rather than a trajectory**, and on one node ordering: which European node holds an end at the smaller factors is ordering-dependent, so the direction is the claim and the membership is not. | DESIGN | derivation | REVISED | X088 |
| Y105 | The last row is the exception: at ×2.00 `genua` held an end in **60 of 60** relabellings, so a single Mediterranean end under that much European growth is a property of the field rather than of the ordering. | MODEL | numerical test | NEW | — |
| Y106 | Because §1.3's wealth is linear in development, **scaling development and scaling wealth are the same operation here** — maximum difference **0.0** across the European set — so the distinction that made v5.0's version of this table wrong does not arise. | MODEL | numerical test | NEW | — |
| Y107 | The 1444 Silk Road route is `genua → alexandria → aleppo → persia → lahore → lhasa → ganges_delta → burma → gulf_of_siam → canton → hangzhou` (v5.0 had it through `doab`). | MODEL | numerical test | REVISED | X094 |
| Y108 | **No route leaves `english_channel` at all** — it is a sink with out-degree 0, so the Hansa and the Danube carry power *into* it, and v5.0's "from the Channel it is the Hansa and the Danube" described a path that does not exist. | MODEL | numerical test | REVISED | X096 |
| Y109 | **No Europe→sink route passes the Cape of Good Hope** — checked from `genua`, `north_sea` and `english_channel`. | MODEL | numerical test | REVISED | X097 |
| Y110 | The Cape is a live conduit rather than an idle one: in-degree 1, out-degree 3, with **132 ordered node pairs** whose path runs through it (`measure6.py`), carrying Atlantic drainage into the Indian Ocean. | MODEL | numerical test | NEW | — |
| Y111 | v5.0's "nothing routes through the Cape" is false as a universal and was only ever checked on the Europe→sink routes. | WORLD | derivation | NEW | — |
| Y112 | Scaling the 22 European **nodes** rather than European provinces makes `genua` the sole sink from about **×1.65**, and the 18-node western/central subset needs about **×2.15**. | MODEL | numerical test | REVISED | X099 |
| Y113 | Somewhere inside roughly **×2.9–×3.5** the Cape of Good Hope **reverses** — Atlantic→Cape→Indian-Ocean becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast — bounded above as well as below, so it is a window and not a threshold, and its edges move with the field. | MODEL | numerical test | REVISED | X100 |
| Y114 | Dev-stacking a single node's top province concentrates the map on that node; extra sinks at intermediate boosts are expected behaviour, not noise. | MODEL | numerical test | REVISED | X101 |

## §1.7 — Merchants (lines 563–590) · §1.8 — Collection and transfer (lines 591–622) · §1.9 — Trade power propagation (lines 623–633)

**UNCHANGED:** C067–C083, C084–C102, C103–C111, V066, V068–V072, V073, W065, W066 *(as replaced by
X102)*, W067–W069, W192, X102, X103, X104. No delta claims — all three sections are textually
identical to v5.0, including §1.9's "no condition on the receiving node" and the France/Sevilla
observation.

## §1.10 — Direction-dependent systems (lines 634–691)

**UNCHANGED:** C112–C143, V074, V078, V079, V080, W070, W071, X105, X109, X110, X196 — the threshold
table, Propagate Religion's flag ladder, the caravan mechanic's shape, the largest-incumbent span
and the outweigh count, and the `highest_power` correction.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y115 | **Banding absorbs very little chatter** — softened from v5.0's "almost nothing absorbs threshold chatter" — while the flicker-risk set stays "every country at a single-valued limit, plus flagless countries at Propagate Religion's 50/50 or 35/35". | OUTCOME | derivation | REVISED | X106 |
| Y116 | ⚑ **Banding is not the only damper:** three shipped defines rate-limit the mechanics that carry these thresholds. | ENGINE | file value | NEW | — |
| Y117 | ⚑ `TRADING_POLICY_COOLDOWN_MONTHS = 12` applies to **seven of the nine entries** in `common/trading_policies/00_trading_policies.txt` — five distinct policies, four of them with an `_upgraded` twin, plus Propagate Religion which has none — so four of the five families are rate-limited. | ENGINE | file value | NEW | — |
| Y118 | ⚑ `maximize_profit` and `maximize_profit_upgraded` are the exceptions, carrying `cooldown = no` in the same file. | ENGINE | file value | NEW | — |
| Y119 | ⚑ `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` and `TRADE_COMPANY_COOLDOWN = 60` are the other two. | ENGINE | file value | NEW | — |
| Y120 | So a flickering share does not translate into a flickering *effect* at those three; what is left exposed is everything without a cooldown, which is most of the ladder. | OUTCOME | derivation | NEW | — |
| Y121 | Measured on 1444: the caravan cap of 50 is **9.4% to 47.0%** of an inland node's total trade power, median **21.6%** over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. | MODEL | numerical test | REVISED | X107 |
| Y122 | As a share of the node's total **after** the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, median 17.7%; v5.0 quoted those under the first description, which cannot be right since 8.6% of 532.0 is 45.8 rather than 50. | WORLD | numerical test | NEW | — |
| Y123 | On §2.2's derived 25-node inland basis the median is **21.3%**, or 17.5% after the grant. | MODEL | numerical test | REVISED | X108 |

## §1.11 — Treasure fleets (lines 692–699) · §1.12 — What the game displays (lines 700–720)

**UNCHANGED:** C144–C148, C149–C165, V049, V065, V081. No delta claims.

## §2.1 — Shape (lines 723–741)

**UNCHANGED:** C167–C184, V082–V085, W072, W073. No delta claims.

## §2.2 — Solver (lines 742–785)

**UNCHANGED:** C185–C209, V064, V091, V092, V229, W075, W076, X115 — the eight solver items, the
two-implementations rule, the derived-inland finding, and the refusal to project a native-simplex
figure.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y124 | Solver item 4 computes `TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production · (1 + province-state goods modifiers) · price`, with no autonomy, efficiency, ideas or owner terms and no trade-value-modifier factor. | DESIGN | stipulated | REVISED | X111 |
| Y125 | The only modifiers the solver reads are the four that describe the province's own condition, and at 1444 **only `devastation` is live, on eleven provinces**. | DESIGN | stipulated | REVISED | X112 |
| Y126 | World wealth is **10,607.40** annual ducats over **2,472** counted provinces. | MODEL | numerical test | REVISED | X113 |
| Y127 | Measured on the reference implementation (scipy/HiGHS plus the deterministic sweep, one machine): **of order 0.1 s for all 29 goods, and single-digit milliseconds per good on average** — and that is the whole of the claim. | MODEL | numerical test | REVISED | X114 |
| Y128 | Repeated 12-run experiments on one machine do not reproduce each other closely enough to support anything finer — three replicates gave per-good averages spanning **3.5–10.5, 3.5–10.8 and 3.1–4.7 ms** — so no range is quoted, because the quantity being measured is a machine and a scheduler rather than the algorithm. | MODEL | numerical test | NEW | — |
| Y129 | Across three replicates of twelve runs, the number of runs landing inside v5.0's quoted 0.17–0.21 s interval was **1, then 0, then 0**. | WORLD | numerical test | NEW | — |

## §2.2a — What map this is for (lines 786–827)

**UNCHANGED:** W077–W085, W088, X116 — the two premises, the disconnected-map requirement, the
weakening table's other three rows, and T2/T3 as the two Phase-0-independent breakers.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y130 | Where Phase 0 acts, free-edge determinism holds only in half: the determinism is unaffected, but the **index-independence half is not** — the key reads the post-fold balance β, so peeling can create exact ties the raw balances do not have, and the 1444 measurement does not transfer. | MODEL | derivation | REVISED | X117 |

## §2.3 — Constants (lines 828–879)

**UNCHANGED:** C211–C227, V094, W091, W097, W098, X118, X119, X120, X123, and the DLC-third-axis
claim — the define table, the two coefficient measurement rows, the truncated-monthly-tax
derivation, the re-measure-against-any-other-patch instruction, and the rule that a future `α_Φ`
change is a design decision to be recorded. *(§2.3's `GP_COEFF`/`TAX_COEFF` provenance split is
Y036–Y038 at first appearance in §1.3; its withdrawal of every `α_Φ` derivation is Y093–Y094 at
first appearance in §1.6.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y131 | v3.0 through v5.0 said neither coefficient was in a file, and shipped a whole-install modifier sweep that walked past the block holding one of them. | WORLD | derivation | NEW | — |

## §2.4 — The tradenodes file (lines 880–948)

**UNCHANGED:** C228–C233, C235–C242, V095, V148, W099, W100, W102–W107, W114, X124, X127 — the
generation policy, the engine's order validation and its tolerance of violations, the cyclic-file
crash, the honoured reversed link, the node window rendering links in file declaration order, the
link-reversal recipe, the preservation list, and the emitter reading the end count from the solve.
*(The degeneracy proposition itself is Y007 at first appearance in §0.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y132 | Measured on 1444: relabelling the nodes and running the aggregate graph end-to-end changed the orientation in **400 of 400** runs across four independent seeds, **always** by returning a different optimal vertex and **never** by a sweep tiebreak, with a mean of **25 of 159** edges moving and the LP objective identical to within 4.44e-16 (`relabel6.py`, which validates its instrument against `drain.py` on the identity permutation and aborts if that fails). | MODEL | numerical test | NEW | — |
| Y133 | Twenty-five flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event. | MODEL | derivation | NEW | — |
| Y134 | Earlier versions quoted a 580-of-580 per-good sweep and an arc-permutation result whose scripts were never shipped; both are withdrawn in favour of the figure a script in this tree reproduces. | WORLD | derivation | NEW | — |
| Y135 | The canonical order the emitter fixes must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks ties in. | DESIGN | derivation | REVISED | X125 |
| Y136 | Everything §1.6 and §2.8 report about stability is measured **at fixed node order**; re-order the same world and the map moves, with `α_Φ` and every input held fixed. | DESIGN | derivation | NEW | — |
| Y137 | The specific counts are HiGHS-specific in their detail but not in kind — any simplex returns *a* vertex of a degenerate optimal face. | MODEL | derivation | NEW | — |
| Y138 | Making the orientation independent of presentation order would need a tie-breaking objective (a lexicographic secondary cost, or a strictly convex perturbation); that is a design change and is not adopted here. | DESIGN | stipulated | NEW | — |
| Y139 | The priority key ties in more places than §1.1 documents: besides the free-edge sweep it decides Phase 1's within-cluster argmin, the stall promotion's identical form, and the top-k cut when two clusters carry equal mass. | MODEL | derivation | NEW | — |
| Y140 | **None of them fires on 1444** — zero exact `(DEF, β)` ties on free edges across 29/29 goods, zero within-cluster β ties, zero tied cluster masses — so no measured figure depends on them. | MODEL | numerical test | NEW | — |
| Y141 | The end-flag list is **a function of the canonical node order, not of the world alone**: fix the order, emit, and keep it, because changing it changes the flags without anything in the world changing. | DESIGN | derivation | NEW | — |
| Y142 | End flags at 1444 in the shipped order: **two** end nodes, `english_channel` and `hangzhou`, against vanilla's three. | DESIGN | numerical test | REVISED | X126 |

## §2.5 — Runtime attachment (lines 949–954) · §2.6 — Writing to the engine (lines 955–976)

**UNCHANGED:** C243–C250, C251–C272. No delta claims.

## §2.7 — Probes (lines 977–1016)

**UNCHANGED:** C274–C293, V098–V101, W108–W111, W113, W114 — the probe list, items 12–15 done, item
12 dropped, the cyclic-file result, the incoming-link button result, and the link-reversal pass.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y143 | § Item 15's finding is **consistent with** §1.9's "every immediately upstream node" — one observation on one node, enough to retire the cautionary case and **not enough to promote the rule to a measurement**; v3.0 through v5.0 said §1.9 was "correct as written and gains no qualifier". | WORLD | engine test | REVISED | W067 |

## §2.8 — Validation (lines 1017–1060)

**UNCHANGED:** C298–C342, V109–V112, W116, W117, W119, W195, X128, X133, X134, X135, X136, X137 —
the case table's other rows, the spice/cloves baseline, the Ming row as the owner-agnosticism check,
the run-to-run drift figures, and the two sink-set checks. *(The 52.3%/53.6% agreement restated in
"Measured, not asserted" is Y091; the latent-good row's 10-of-159 is Y071.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y144 | Most goods, 1444: sinks are `{selected ∩ flow-terminal} ∪ promoted`, **1 to 8** per good, and high-demand nodes are sinks at **16.8%** in the top demand decile against 6.9% in the bottom — a barbell, LP branch ends landing in poor pockets. | MODEL | numerical test | REVISED | X129 |
| Y145 | The Razed-China row is **ordering-robust where §1.6's sink membership is not**: it turns on `hangzhou` holding an end, which it does in about 98% of relabellings, and on the razed field `hangzhou` loses its end in every relabelling tried. | MODEL | numerical test | NEW | — |
| Y146 | Zeroing `hangzhou`-node development moves the `Φ_w` sinks from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`, with **22 of 159** edges flipping. | MODEL | numerical test | REVISED | X130 |
| Y147 | `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth **226.7 against 143.0**, and it holds the richest single province **the model counts**. | MODEL | numerical test | REVISED | X131, X182 |
| Y148 | Zeroing `beijing` **also** moves the map — **15** flips — because deleting a percent of world wealth renormalises `c_w` everywhere; what separates the two cases is that `hangzhou` survives as a sink when `beijing` is zeroed and does not when `hangzhou` is. | MODEL | numerical test | REVISED | X132 |

## §2.9 — Build order (lines 1061–1073) · §3.1 — Goals (lines 1076–1085)

**UNCHANGED:** C343–C352, C353–C365, V113, X138. No delta claims.

## §3.2 — Why a flow and a drainage sweep (lines 1086–1195)

**UNCHANGED:** C366, C370–C375, C383–C385, V115, V116, V118–V122, V124, V128–V131, W120, W123,
W125–W128, X139, X141, X146, X147, X148, X149 — the monotone-comparison failure, the Laplacian sink
rule, the sparsity diagnosis, T1/T2/T3 worked in full, the surviving ⊆-direction, and the two runtime
checks. *(The "measurement on one input, not a theorem" upgrade is Y025 at first appearance in §1.1.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y149 | **What the ratio metric cannot see is the thing the diagnosis rests on:** a max/min ratio over *producing* nodes is blind to sparsity by construction, and on the contrast metric itself the demand side is the wider one — a measurement §3.2 carries and §3.15 no longer copies. | MODEL | derivation | REVISED | X140 |
| Y150 | Better wealth inputs move Genoa to a *co-*sink at roughly **×1.7** without making demand the determinant of placement. | MODEL | numerical test | REVISED | X142 |
| Y151 | Moving the spice sink to a Chinese node takes a multiple of that node's **wealth** in the region of **3.6–4.8×** — `beijing` 3.63×, `hangzhou` 4.13×, `xian` 4.61×, `canton` 4.78×. | MODEL | numerical test | REVISED | X143 |
| Y152 | Those are **wealth** multiples, not demand multiples: because demand is `wealth^α` normalised over the world, the same move expressed in demand is a much larger factor. | MODEL | derivation | NEW | — |
| Y153 | The four named are not the cheapest — `girin` needs 3.89× and `yumen` 4.49×, both inside the range — so the claim is about the size of the intervention rather than about which node is easiest to move. | MODEL | numerical test | REVISED | X144 |
| Y154 | Two cautions on the free-edge measurement: the key reads the **post-fold** balance β, so peeling can create ties the raw balances lack; and the indexing is load-bearing wherever the key ties, which is **not only the fallback branch** — **and none of them is why §2.4 requires a canonical node order**. | MODEL | derivation | REVISED | X150, X151 |

## §3.3 — Why wealth, and why per province (lines 1196–1219)

**UNCHANGED:** C386–C406, C408, C412, C413, V132, V133, V135, W132–W139 — the purchasing-power
argument, the return-flow price comparison, the circularity exclusion, the 19-to-77 node-size spread
and the `k^(α−1)` distortion arithmetic.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y155 | ⚑ `cape_of_good_hope`'s `members` list has **20 entries**, but 1460 is a sea zone listed in `map/default.map`'s `sea_starts`, so the node holds 19 land provinces. | ENGINE | file value | NEW | — |

## §3.4 — Why supply is pre-modifier (lines 1220–1231)

**UNCHANGED:** C415–C423, V137, V139, W140, W141, W142.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y156 | In v1 the production-income substitution broke the α = 1 identity, measured as orientation agreement collapsing to **well under half the map** — the 159/159-to-68/159 figure is no longer carried. | MODEL | numerical test | REVISED | V138 |

## §3.5 — Why α is anchored absolutely (lines 1232–1276)

**UNCHANGED:** C427–C442, V140–V144, V147, X152, X153, X156, X157 — the absolute-anchor argument,
the 13/2/4/11 partition, the `NEW_DRAPERIES` history route to 1.875, and v2's 13 against v3.0's 12.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y157 | ⚑ **`change_price` values are fractions of the good's base price, not ducats**, and the shipped save `tutorial/eu4_tutorial_chapter10.eu4` settles it: `paper` at `current_price=4.375` on a base of 3.5 is ×1.25 and not +0.25, and `gems` at 5.000 on a base of 4.0. | ENGINE | file value | NEW | — |
| Y158 | The install carries **161** textual `change_price` blocks — 93 in `events/`, 14 in `missions/`, 1 in `common/`, 53 in `history/` of which 13 are negative (all in `history/countries/HAB - Austria.txt`), and **none in `decisions/`**. | ENGINE | file value | REVISED | X154 |
| Y159 | ⚑ **Ten of the 161 never execute:** four sit inside `effect_tooltip = "…"` strings, three inside the `effect = "…"` string of a `country_event_with_effect_insight`, and three inside `tooltip = { }` display wrappers — so **151 are executable**. | ENGINE | file value | NEW | — |
| Y160 | Six of the seven quoted ones duplicate a block already counted in `events/`, and the seventh names a price key no event in the install ever sets. | ENGINE | file value | NEW | — |
| Y161 | All ten are positive and every negative block in the install is executable, so the partition is identical under either census. | ENGINE | derivation | NEW | — |
| Y162 | v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them; **both were wrong about which number was the executable one**. | WORLD | derivation | REVISED | X155 |
| Y163 | v5.0's claim that the scan was "guarded by a per-file count assertion" is false — there was no assertion anywhere in its toolchain. | WORLD | derivation | REVISED | X155 |
| Y164 | `verify6.py` now checks the census, but only by requiring the printed total to match a computed one rather than by reconciling per file, and `measure6.py`'s walker still swallows parse failures in a bare `except`. | DESIGN | stipulated | NEW | — |
| Y165 | The reason a plain parse misses these is mechanical: `pdx.py` tokenises a quoted string as one opaque unit, so a `change_price` inside a tooltip string is invisible to the walker. | MODEL | derivation | NEW | — |

## §3.6 — Why no hysteresis (lines 1277–1313) · §3.7 — Why eligibility is per good (lines 1314–1321) · §3.8 — Why gates evaluate true (lines 1322–1341)

**UNCHANGED:** C443–C446, C449, C452, C463–C473, C474–C497, V148, V152, V154, V155–V158, W147–W152,
W154. No delta claims — §3.8's reachability figure is Y090 at first appearance in §1.6, and the
cycle-crash and determinism material is textually identical to v5.0.

## §3.9 — Why `Φ_w` is the installed graph (lines 1342–1388)

**UNCHANGED:** C502, C505–C510, C512, V160, V161, V162, V218, V221, V228, X161 — the power-not-cargo
framing, vanilla's three authored ends, the net-flow aggregate's cycles, the one-operator guarantee
list, and the note that a `Φ_w` difference is not the net value crossing a link.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y166 | On the corrected field `genua`, `gulf_of_siam` and `sevilla` rank **4th, 3rd and 7th** by node wealth (`mexico` is 2nd) at **296.0, 297.9 and 266.5** against `english_channel`'s 316.6, **which is a sink**. | MODEL | numerical test | REVISED | X159 |
| Y167 | `Φ_ord` scores **higher** than `Φ_w` on self-coherence — the cost of the trade, not disputed — and was superseded on design grounds: its ends are scheduling artifacts, **half** of them terminate no good at all (7 of 14 on the 1444 field), none of the demand capitals is among them, and its end count does not concentrate as demand concentrates. | MODEL | numerical test | REVISED | X160 |
| Y168 | The "two vanilla-like ends at 1444" premise **should not be revived even though the 1444 field again gives two ends**: the count is a property of the field, not the operator, and pinning the operator to it would be the calibration §2.3 withdrew. | WORLD | derivation | REVISED | X162 |
| Y169 | The trade is stated as a direction: what it costs is self-coherence with the per-good graphs, which the marking-order aggregate scores higher on, and what it buys is one operator, one set of guarantees, and ends that sit where the wealth is — with no points figure attached. | DESIGN | stipulated | REVISED | X163 |

## §3.10 — Why the engine's economy is overwritten (lines 1389–1407)

**UNCHANGED:** C513–C521, C523–C525, C528–C530, X164, X165, X167 — the display argument, the
factoring identity, the node-wide-terms argument, and the 5.7e-14/1.4e-14 diagnosis.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y170 | The two forms agree to a worst relative disagreement of **0 to 3.7e-16** — **one to three** units in the last place (v5.0 said at most one). | MODEL | numerical test | REVISED | X166 |
| Y171 | Propagation is kept on a single graph **and the reason is not the one v1 through v6.0's own first draft gave**: reading the one installed graph leaves the propagated term good-independent, so the identity holds by construction. | DESIGN | stipulated | REVISED | X168 |
| Y172 | Per-good propagation makes a country's power at a node differ by good, because §1.9 reads downstream neighbours and those differ per good: `gulf_of_siam`'s 29 goods leave it by **seven** distinct downstream sets (v5.0 said eight, with a 0.003% effect). | MODEL | numerical test | REVISED | X169 |
| Y173 | **What that does not do is break the identity:** with `ps̄_C = Σ_g v_g·cs_g·ps_C(g) / Σ_g v_g·cs_g`, `collect_pool · ps̄_C = income_C` follows algebraically and `Σ_C ps̄_C = 1`, so `ps̄_C` is a legal share vector and one scalar per node still reproduces every collector's income exactly. | MODEL | derivation | NEW | — |
| Y174 | Both inputs already exist per good at write time, and §2.6 sums exactly them into `collect_pool`. | MODEL | derivation | NEW | — |
| Y175 | **The real cost is that `ps̄_C` is not derivable from trade power alone:** it is value-weighted, so installing it means writing a country a fictitious per-node trade power whose ratio happens to equal it, and every other consumer of that power field then reads the fiction. | MODEL | derivation | REVISED | X170, X171 |
| Y176 | That is a claim about what the engine exposes rather than about a magnitude, and it is why the single graph stays: on one graph the scalar *is* the country's power share, needing no invention. | DESIGN | derivation | NEW | — |
| Y177 | Every magnitude previous versions quoted was an artifact of substituting some other weighting — v1–v3.0's "5.96 ducats on a node paying ~250" (deleted in v4.0, whose own harness asserted the deletion), v4.0's 0.41%, v5.0's "redistributive and single-digit percent", and v6.0's first draft's "at most 0.1%". | WORLD | derivation | REVISED | X173, X174 |
| Y178 | **No figure of the author's own is quoted here**, because the identity holds and the objection is structural. | DESIGN | stipulated | REVISED | X172 |

## §3.11 — Caravan power (lines 1408–1430) · §3.12 — Treasure fleets (lines 1431–1445)

**UNCHANGED:** C531–C547, C556–C560, V163–V172. No delta claims.

## §3.13 — Open questions (lines 1446–1505)

**UNCHANGED:** C561–C585, V173, V174, V175, V178, V181, V182, V183, W164, X175, X177, X178, X179,
X180, X183 — the prose-sourced and derived lists, the debugger-only shortlist, the one-open-question
framing, the two settled-and-moved wealth answers, the α-reachability bound, the calibration's span
and spearman, and the twig tolerance's cost.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y179 | The open wealth question is now **"should any source beyond province condition be allowed to multiply `goods_produced`?"** — a **design** question rather than a classification one, since §1.3 reads development, the trade good and the four province-state modifiers and nothing else. | DESIGN | stipulated | REVISED | X176 |
| Y180 | ⚑ `trade_goods_size` and `trade_goods_size_modifier` are granted in buildings, event modifiers, great projects, static and province-triggered modifiers, holy orders, state edicts and trade-company investments. | ENGINE | file value | REVISED | X176 |
| Y181 | Re-admitting any of those sources re-admits the maintenance burden with them, so the question to settle first is whether the fidelity is worth about one percent of world wealth either way the ratio is taken. | DESIGN | derivation | NEW | — |
| Y182 | Under the calibration's α = 16 the cloves demand order is `hangzhou`, `beijing`, `doab`, and the sink lands on a high-demand node rather than a geographic accident. | MODEL | numerical test | REVISED | X181 |
| Y183 | v2's "Beijing holds the richest single province" is wrong — that is `hangzhou` — with the 30.4/19.5 figures and the Deccan demand-rank claim no longer carried. | WORLD | numerical test | REVISED | X182 |

## §3.14 — AI merchant assignment (lines 1506–1524)

**UNCHANGED:** C586–C624, X184. No delta claims.

## §3.15 — Rejected (lines 1525–1636)

**UNCHANGED:** C625–C672 as carried by v2, V184–V188, V192–V199, V226, V227, V228 — every rejection
argument, and the graveyard's structure. *(The convention that no figures are maintained here is
Y009–Y011 at first appearance in §0.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y184 | The Laplacian entry keeps the sparsity argument, no longer maintains a copy of §3.2's contrast measurement, and adds that `cloves` has a single producer and so no contrast to measure at all — the sparsity point in miniature. | MODEL | derivation | REVISED | X185, X186 |
| Y185 | Ranked orientation is de-quantified: it puts a far higher share of top-demand nodes in its sink sets than DRAIN does, and fails on delivery — a large share of world demand stranded, orphan sinks a good cannot reach, net-producer sinks where DRAIN, LAP and FLOW post none, and several times DRAIN's sinks per good. | MODEL | numerical test | REVISED | X187, X188 |
| Y186 | Seeded basin growth leaves demand unserved **at every tuning tried** — the 88.4%-reach figure is dropped. | MODEL | numerical test | REVISED | X189 |
| Y187 | The 3-mass gravity kernel reproduces whatever end count it is seeded with while γ is small enough and loses that property as γ approaches 1; no figures are maintained, and a pure `wealth^α` edge comparison with no reach term does not concentrate ends at all because a local wealth maximum survives every positive α. | MODEL | numerical test | REVISED | X190, X191, V225 |

## §3.16 — Evidence standard (lines 1637–1699)

**UNCHANGED:** C677, C680–C682, C684, C685, V200–V203, V206–V210, W173–W181 — the refuted evidence
standard, the three failure mechanisms, the provenance signal and its partition correction, the
sink-placement gap, the closed cautionary case, and the null-comparison rule.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y188 | Failure mechanism 3 is restated with both magnitudes: implemented as written, the α = 1 identity's residual reached **1e-5 against v1's ε of 1e-6**, and would have been diagnosed as a solver bug. | MODEL | numerical test | REVISED | V204 |

---

# Prior IDs v6.0 strands

Recorded for the next audit's benefit, not as claims. **Twenty-eight X IDs and one W ID lose their
subject matter outright** when §1.3's classifier and §3.15's figures are deleted; they are not
replaced by anything, so no Y row names them.

| Stranded | What it said | Why it is gone |
|---|---|---|
| X032, X034, X058 | the trade-good data model as one instance of the locality test; v4.0's file-only sweep; glass and chinaware as the whole rule-versus-vocabulary tension | the tests they qualify are deleted (Y002) |
| X038, X039, X048, X049, X050, X051, X053, X054 | the great-project and permanent-modifier enumerations, the `starting_tier` line, and the owner-action argument | the sources are no longer read (Y030) |
| X041, X042, X043, X044, X045, X046, X047 | glass, chinaware, the 361 centres of trade, `production_leader`, `bonus_from_merchant_republics`, buildings-empty-at-1444, terrain and climate | classified-out rows with no classifier left |
| X052 | "Province 1821 is the richest single province in the game" | survives only as `base_tax` 15 / development 33 (Y069) and as `hangzhou` holding the richest province the model counts (Y147) |
| X055, X056, X057 | `stora_kopparberget_modifier`'s Leviathan gate, the 3.0-vs-5.0 consequence, and every figure being measured with Leviathan installed | the DLC conditionality of the wealth field is deleted |
| X029 | fifteen 1444 provinces carry a flat goods bonus | no source grants one under §1.3 (Y046) |
| X192, X193, X194, X195 | the narrow `{english_channel, hangzhou}` α_Φ window, its noise behaviour at 8 seeds, the edge-uncertainty principle, and the "it shrinks" correction | the [1, 3] band table they analysed is replaced by the [1, 8] scan (Y095, Y096) |
| W041 | "in vanilla the income-relevant local modifiers are exactly three" | already replaced by X035, which Y030 now replaces in turn |

Three further v5.0 propositions survive only as history rather than as claims about the model:
X143's demand percentages (9.3–21.4%), X170's per-collector error table, and X107's share
description, each explicitly corrected in place by Y151, Y175 and Y122.

---

# † Unresolvable IDs

**None.** Every `Replaces` target in this file resolves to a specific C, V, W or X ID. The three
C-range † markers `claims-v5.md` carried (X130, X133, X138 against C298–C342 and C353–C365) are not
inherited: X130 is replaced here by Y146 against **X130** itself, X133 and X138 are UNCHANGED in
v6.0, and no new revision in this pass reaches past X, W or V into an unresolved C-range.

Two `Replaces` entries are worth flagging as judgement calls rather than as unresolved IDs:

- **Y036–Y038** replace both W031 (§1.3's "neither coefficient is a define") and W089 (§2.3's "both
  are hardcoded in the binary"). These are the same proposition stated in two sections and inventoried
  twice by `claims-v3.md`; both are named so neither is left dangling.
- **Y143** replaces W067, whose second clause ("§1.9's 'every immediately upstream node' is correct as
  written and gains no qualifier") is what v6.0 rewrites. W067's first clause — the tooltip qualifier
  is descriptively false — survives unchanged in §1.9 and §2.7, so the row replaces half an ID.
