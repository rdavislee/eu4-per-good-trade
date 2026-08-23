# Claim Inventory Delta — Per-Good Trade Network Spec v6.0

Extracted from `per-good-trade-spec.md` (v6.0, 1,645 lines) as a **delta against
`../v5-owner-agnostic/claims-v5.md`** (X001–X196), which is itself a delta against
`../v3-owner-agnostic/claims-v3.md` (W001–W195), `../v2-drain/claims-v2.md` (V001–V230) and
`../v1-laplacian/claims.md` (C001–C685). Extraction only: nothing here is validated, corrected or
graded. The tables say what the document asserts, how each assertion is typed and sourced, and how
it stands to the prior inventory.

**Method.** The v6.0 spec was read in full, and `claims-v5.md` in full (header conventions plus all
196 claim rows). A **sentence-level diff of the v5.0 spec against the v6.0 spec** was then computed
and read hunk by hunk — 50 changed regions, all of them `replace`, no pure insertions or deletions
— so that every v6.0 proposition could be classified as changed or carried. `claims-v3.md`,
`claims-v2.md` and `claims.md` were **grepped** (not read whole) to resolve or confirm specific W, V
and C IDs — W014, W023, W025, W026, W030–W036, W040–W052, W059, W062, W064, W067, W089, W189, V004,
V138, V204 — of which twelve W and two V IDs are used as `Replaces` targets and the rest are carried
UNCHANGED or noted. `changes-v6.md` was consulted only as a locator for changed passages; no row
below is taken from its description of the change.

**ID prefix.** v1 used `C`, v2 used `V`, v3 used `W`, v4 got no inventory, v5 used `X`.
**v6 uses `Y`**, numbered in document order.

**Statuses.** UNCHANGED — the same proposition as an existing C/V/W/X ID; the old ID is recorded in
the per-section list and no Y ID is issued. REVISED — the proposition changed; a new Y ID with the
old ID(s) in `Replaces`. NEW — no counterpart in any prior inventory. A proposition stated in two
sections keeps one ID at first appearance; restatements are noted where they could be mistaken for
new rows.

**Vocabularies.** Type: ENGINE (how EU4 behaves) / MODEL (the mathematical model) / DESIGN (a
stipulation, goal or choice) / OUTCOME (what the built mod will produce in play) / WORLD (truth-apt
claims about history or about the project's own review history). Provenance: stipulated /
derivation / file value / numerical test / engine test / prose source / verified (method unstated) /
UNSOURCED. `numerical test` (a solver or script experiment — `measure6.py`, `europe.py`, `toys.py`)
and `engine test` (an observation of EU4 actually running — a tooltip, a crash dump, a save the game
wrote) are kept strictly distinct; `file value` is a shipped game file read directly.

**Markers.** **⚑** a claim introducing an engine fact no prior inventory carried. **§** a claim whose
stated evidence is a single observation. **†** a `Replaces` target believed to exist but not pinnable
to a specific ID.

---

# Summary

**178 delta claims extracted, Y001–Y178**, against the 196 v5 claims: **67 NEW, 111 REVISED**,
replacing **99 X IDs, 12 W IDs and 2 V IDs** — 113 distinct prior IDs in all. No UNCHANGED row
carries a Y ID, by the convention above; the carried IDs are listed per section.

The v5 inventory partitions cleanly: of its 196 IDs, **99 are replaced here, 35 are withdrawn
without replacement** (section (b) below) and **62 are carried UNCHANGED**. The 35 strandings are
more than any previous version left behind, and the reason is that v6.0's substantive change is a
**deletion** — the two-test modifier classifier and the whole-install sweep that maintained it.
The new rows concentrate in three places the deletion opened up: the 1444 start-state reads (§1.3),
the degenerate-LP node-order result (§2.4), and the re-derived aggregate field (§1.6).

### Delta claims by status and Type

| Type | NEW | REVISED | Total |
|---|---|---|---|
| MODEL | 29 | 71 | 100 |
| ENGINE | 15 | 16 | 31 |
| DESIGN | 14 | 15 | 29 |
| WORLD | 9 | 9 | 18 |
| OUTCOME | 0 | 0 | 0 |
| **Total** | **67** | **111** | **178** |

The REVISED-heavy shape is the direct consequence of the two prose conventions in §0: a great many
propositions survive with their figure replaced by a direction, or with their scope narrowed from an
absolute to an observation, and each of those is a proposition change.

### Delta claims by Provenance

| Provenance | Count |
|---|---|
| numerical test | 63 |
| derivation | 62 |
| stipulated | 25 |
| file value | 18 |
| engine test | 10 |
| prose source | 0 |
| verified (method unstated) | 0 |
| UNSOURCED | 0 |
| **Total** | **178** |

**No row carries UNSOURCED provenance.** Every figure in the delta names either a file, a script or
a named observation. The v5.0 caveat about W071 (carried UNCHANGED and typed UNSOURCED in
`claims-v3.md` while v5.0 measured its first clause) still stands and is still a claims-file matter
rather than a spec one — §1.10's caravan paragraph is revised again in v6.0 (Y108–Y110) and W071's
second clause remains a derivation.

**15 rows are marked ⚑** — new engine facts — and **9 of them are NEW**. Eight of those nine sit in
§1.3 and §3.5: the `on_startup` chain and its second `events = { }` path, the `add_base_*`
accumulation rule, the `is_city` non-filter, the `trade_goods = unknown` draw, the devastation-scaling
gap, and `change_price`'s fraction semantics plus its ten non-executing blocks. The ninth is §1.10's
three cooldown defines. *(The other six ⚑ rows are REVISED — Y030, Y033, Y036, Y038, Y046, Y169 —
each attaching a new file or tooltip observation to a graded predecessor.)*

**Four rows are marked §** — evidence resting on a single observation: **Y036, Y038, Y060, Y132**.
Y036 and Y038 are v6.0 *adding* the marker to readings v4.0 and v5.0 stated flat (the production
tooltip's divisor, and the Garnatah truncation); Y060 and Y132 are new single observations (the
twenty rolled trade goods on one save, and probe 15's one node).

### Where the delta concentrates

| Section | Y rows | What drove it |
|---|---|---|
| §1.3 Demand | 43 | the classifier's deletion, the four province-state modifiers, and three corrected start-state reads |
| §1.6 Aggregate graph | 38 | two sinks again, one α_Φ band instead of a table, the rewritten Europe demonstration, the corrected route geography |
| §2.4 The tradenodes file | 11 | Phase 2's degenerate LP as the reason for canonical node order, with two permutation experiments |
| §0 Front matter | 11 | the new change statement plus two prose conventions |
| §3.10 Income factoring | 10 | the `ps̄_C` construction that keeps the identity and moves the objection to what the engine exposes |
| §1.1 Trade direction | 9 | the post-fold reachability condition for the fallback branch |
| §3.5 α anchor | 7 | `change_price` semantics and the executable-block census |
| §1.10 · §2.2 · §3.2 · §3.15 | 6 each | cooldown defines and the caravan denominators; the solve-cost retreat; sparsity restated as a direction; the graveyard's figures withdrawn |
| §2.8 Validation | 5 | regenerated razed-China and latent-coal rows |
| §3.9 | 5 | the `Φ_ord` comparison restated as a direction |
| §3.13 | 4 | the wealth question turned from classification into design |
| §1.5 · §2.3 | 3 each | |
| §2.2a · §2.7 · §3.4 · §3.8 · §3.16 | 1 each | |
| **Total** | **178** | |

---

# (a) Which propositions stand on no replaced predecessor?

Three groups, and they are the answer to "what subject matter is new in v6.0?".

1. **The 1444 start state as a distinct object from the history files** (§1.3: Y046–Y060). No prior
   version stated that the engine's start state differs from the parsed history files, and none of
   the three mechanisms — `on_startup` effects, `add_base_*` accumulation in a pre-start dated block,
   `is_city` not being applied as a filter — has a predecessor to replace. X063 said the opposite of
   the third ("every province the model counts is a city (`is_city = yes`)"), so Y055/Y056 do replace
   it; but the `on_startup` chain, the dated-block rule, and the twenty rolled trade goods are new
   subject matter, sourced and unaudited.

2. **Phase 2's degeneracy** (§2.4: Y121–Y127, and §0's Y006). v5.0's X125 and X151 said a canonical
   node order was required because the priority key's index tiebreak decides on the fallback branch.
   v6.0 keeps the requirement, **withdraws that reason**, and supplies a different and stronger one
   measured on 1444 — so Y006 replaces X125/X151, while the 580/580 relabelling result, the 10-of-10
   arc-permutation result, and the four consequences drawn from them replace nothing.

3. **The `ps̄_C` construction** (§3.10: Y161–Y163, Y166). v5.0's X170/X171 said per-good propagation
   *breaks* the income identity and measured the error. v6.0 shows algebraically that it does not
   break the identity, and relocates the objection to what the engine exposes. Y161 replaces X170 and
   X171; the value-weighted share vector itself, and the observation that installing it means writing
   a fictitious trade power, have no predecessor.

Everything else in the delta either replaces a graded predecessor or refines a claim whose
predecessor was replaced.

---

# (b) Which prior IDs does v6.0 leave stranded?

**35 X IDs are withdrawn without replacement** — deleted with the classifier, or stated to be wrong
with nothing put in their place. This is the largest stranding in the project's history and it is
deliberate: §0 states the deletion as the version's substantive change.

| Withdrawn | What it said | Why it is stranded |
|---|---|---|
| **X003** | v5.0's change "moves the aggregate graph from two 1444 sinks to one" | §1.6 measures **two** sinks again on the v6.0 field |
| **X030, X031** | the locality test and the wealth test | §1.3: the two-test classifier is deleted |
| **X032** | the trade-good data model is one *instance* of the locality test | deleted with the test |
| **X034** | v4.0 stated the rule and swept only `common/tradegoods/` | absorbed into Y004's "wrong in both audits" and no longer stated as its own finding |
| **X038, X039** | great-project `province_modifiers` and undated `add_permanent_province_modifier` are local and enter wealth | no longer read |
| **X041, X042** | `glass` and `chinaware` are local but do not enter wealth | classification deleted; glass survives only in §3.13's settled note (X177) |
| **X043** | 361 provinces carry a centre of trade at 1444, and no CoT level grants a key wealth reads | deleted |
| **X044, X045** | `production_leader` and `bonus_from_merchant_republics` are not local | deleted |
| **X046** | buildings are local by the test and empty at 1444 | deleted |
| **X047** | `terrain.txt` and the climate static modifiers are local but grant nothing wealth computes | deleted |
| **X048–X054** | the great-project scope rule, the 85-of-130 gating count, the six projects and their keys, province 1821 as the richest in the game, the `starting_tier` argument, the six permanent-modifier keys over ten provinces | deleted |
| **X055, X056, X057** | the Leviathan gate on `stora_kopparberget_modifier`, the 3.0/5.0 pair, and "every wealth figure was measured with Leviathan installed" | deleted; §2.3 keeps "DLC state is a third input axis" for treasure fleets and caravan power only |
| **X058** | glass and chinaware are the whole of the rule-versus-vocabulary tension | deleted |
| **X071** | v2–v4's two-sink result was measured on a field missing sixteen provinces | withdrawn; two sinks is again the measured result |
| **X079, X080, X082** | the 3-sink [2.26, 2.71], 2-sink [1.94, 2.25] and 2-sink [1.406, 1.424] bands | the band table is replaced by the single band of Y083 |
| **X192, X193, X194, X195** | the ±1%-noise analysis of the narrow window, the eight-seed band widths, "a constant cannot honestly be placed inside a window narrower than the uncertainty in its own edges", and the shrink-not-disappear finding | deleted with the band table; α_Φ is now stipulated outright and needs no band argument |
| **X092, X093** | the Lowlands-only ×1.20 result and the random-versus-systematic noise contrast | deleted from the Europe demonstration |

**Separately, ten X IDs survive as propositions but lose their figure**, and each is REVISED
rather than stranded because the surviving direction is still asserted: X029 (fifteen flat-bonus
provinces → refuted outright by Y041), X140 (36 against 482.2 → Y139), X144 (4.0–10.8× → Y142),
X163 (7.8 points → Y157), X173 (largest 112.6 → Y167), X182 (30.4 against 19.5 → Y171), and
X187–X190 (RANK's ρ_val, decile shares, 83.0% and 31 orphan sinks; the basins' 88.4%; the gravity
kernel's 61% at γ = 0.90–0.95 → Y174–Y177).

**Two prior positions are reversed rather than stranded**, and both get Y IDs: X097's "nothing routes
through the Cape" (Y097/Y098/Y099 — false as a universal, and the Cape carries 132 ordered node
pairs) and X065's "the count is set by α_Φ" (Y067/Y069 — the count is a function of the field *and*
the constant).

**Not stranded, though the deletion might suggest it:** W042 (`gems` `local_tax_modifier = 0.15`),
W043 (`glass` `local_production_efficiency = 0.1`) and W044 (`incense` `trade_value_modifier = 0.1`)
survive as **file facts** — §1.3 names all three in the "what this gives up" clause and §3.13 keeps
glass's tooltip evidence. What is withdrawn is their classification, not their existence.

---

## §0 — Front matter (lines 1–44)

**UNCHANGED:** C002, C003, C004, V001 *(via §2.5)*, V002, V003, V004, W001, W002, W005.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y001 | v6.0's substantive change is to §1.3: **wealth is a function of the province's development, its trade good and its own current condition, and of nothing else** — owner-agnosticism made true by construction rather than by a rule that has to be policed. | DESIGN | stipulated | REVISED | X002 |
| Y002 | The two-test modifier classifier and everything it governed — trade-good modifiers, great projects, permanent province modifiers, buildings, centres of trade and the DLC conditionality — are deleted, along with the whole-install sweep that maintained them. | DESIGN | stipulated | REVISED | X033 |
| Y003 | On the 1444 start that whole apparatus was worth **0.98%** of world wealth. | MODEL | numerical test | NEW | — |
| Y004 | What it cost was an input surface whose classification was **wrong in both independent audits that examined it** — `validation-v3.md` W041 and `validation-v5.md` X030/X034 — and which v4.0's own repair harness passed before v5.0's audit refuted it. | WORLD | derivation | NEW | — |
| Y005 | Three start-state reads are corrected in the same pass: `on_startup` devastation, dated `add_base_*` accumulation, and the `is_city` filter the engine does not apply. | DESIGN | stipulated | NEW | — |
| Y006 | The reason a canonical node order is a correctness requirement is **Phase 2**: its min-cost flow is degenerate, so presentation order selects which optimum is returned. Neither the sweep's index tiebreak nor the fallback branch is the reason. | MODEL | derivation | REVISED | X125, X151 |
| Y007 | Prose convention: **no empirical absolutes** — no superlative, no universal quantifier and no threshold asserted as a fact about the world; a claim is either a directional design statement or an observation scoped to the field and script that produced it. | DESIGN | stipulated | NEW | — |
| Y008 | Prose convention: **no maintained figures for any rejected operator** — §3.15 keeps its design arguments and loses its measurements, covering `Φ_ord`, the gravity kernels, the v1 Laplacian, RANK and the seeded basins. | DESIGN | stipulated | NEW | — |
| Y009 | Those numbers were re-measured and re-refuted in three successive audits and **not one** of the rejection arguments depends on them; where a comparison is load-bearing it is stated as a direction rather than a figure. | DESIGN | derivation | NEW | — |
| Y010 | Every graded claim from `../v5-owner-agnostic/validation-v5.md` — **22 refuted, 39 partial, 1 unverifiable** — is folded through, and `fixes-agreed.md` maps each one to the change that answers it. | WORLD | stipulated | REVISED | X001 |
| Y011 | Measured figures carry the script that produced them, and `scripts/verify6.py` re-derives each one **from the document text** and fails if the two disagree. | DESIGN | stipulated | REVISED | X004 |

## §1.1 — Trade direction (lines 50–155)

**UNCHANGED:** C005, C006, C010–C012, C019–C022, V005–V015, V017–V024, V026–V028, V031, V032,
V036, V037, W007–W011, W015–W022, X005, X006, X007, X012, X014, X015, X016, X017.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y012 | The fallback branch fires only when every candidate is support-isolated with zero **post-peel** balance. | MODEL | derivation | REVISED | X008 |
| Y013 | The balance the priority key reads is the one Phase 0 hands on, with each pendant's balance folded into its parent — **not** the raw input `b` — so the condition is about the folded field and a map with non-zero raw balances can still reach the branch. | MODEL | derivation | NEW | — |
| Y014 | On a connected core the branch needs the folded balance to vanish across the core: for a per-good graph that is a component with no producer and no consumer; for the aggregate graph it needs every node's `Σ wealth^α_Φ` to be equal. | MODEL | derivation | REVISED | X009 |
| Y015 | Uniform *per-province* wealth does **not** deliver that, because nodes hold between **0 and 72** counted provinces, so equal provinces make unequal node sums. | MODEL | file value | NEW | — |
| Y016 | Where the wealth key then ties, the **node index** decides. | MODEL | derivation | REVISED | X010 |
| Y017 | The containment set asserted in §2.8 includes the fallbacks because of **T3** — a fallback promotion that is a sink in neither the selected nor the promoted set — not because of the wealth tie, which is incidental to it; and that tie is **not** why §2.4 requires a canonical node order. | DESIGN | derivation | REVISED | X011 |
| Y018 | On 1444 the pendant and fallback cases are empty and the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods, **1–8 sinks per good, mean 3.72**, zero fallbacks. | MODEL | numerical test | REVISED | X013 |
| Y019 | That equality is **a measurement on this input**, not a theorem, and v2 asserted it as one. | WORLD | derivation | REVISED | W014 |
| Y020 | It does not become a theorem by attaching conditions either: "Phase 0 a no-op and no fallback firing" looks sufficient and is not — **T2** satisfies both and still breaks it. | MODEL | derivation | NEW | — |

## §1.2 — Supply (lines 157–168)

**UNCHANGED:** C023, C025–C028, V038, V039, V040, V041. No delta claims.

## §1.3 — Demand (lines 170–318)

**UNCHANGED:** C031, C032, C033, C035, C036, C039, W024, W026, W030, W033, W042, W043, W044, W047,
W051, X023, X024, X025, X026, X059, X060, X061, X062.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y021 | Wealth reads **three** things about the province — its development, its trade good and its own current condition — and it is a property of the *place*, what the land is worth per year before anyone's government touches it. | MODEL | stipulated | REVISED | W023 |
| Y022 | Two provinces with the same **development, trade good and condition** have the same wealth whoever owns them (v3.0–v5.0 said "terrain, development and trade good"). | MODEL | derivation | REVISED | W025 |
| Y023 | Owner-agnosticism is true **by construction**: `base_tax`, `base_production` and the trade good are bare attributes of the place, so nothing about them needs classifying. | DESIGN | derivation | NEW | — |
| Y024 | *What this gives up:* `gems`' `local_tax_modifier` and `incense`' `trade_value_modifier` are genuinely province-scoped and are no longer read, along with great projects, permanent province modifiers and the DLC state they depended on. | DESIGN | stipulated | REVISED | X035 |
| Y025 | That apparatus covered **89** of the 2,472 counted provinces — 43 `gems` plus **31** `incense` plus 16 great-project and permanent-modifier provinces, less province **542**, which is both. | ENGINE | file value | REVISED | X036, X037 |
| Y026 | The count depends on the field: **87** under the withdrawn `is_city` filter, and 89 rather than 88 because province **4856** is one of the twenty whose good the engine rolls and it rolled `incense`. | ENGINE | engine test | NEW | — |
| Y027 | `goods_produced(p) = GP_COEFF · base_production(p) · (1 + Σ province-state goods modifiers)` — no flat-goods-bonus term. | MODEL | derivation | REVISED | X018 |
| Y028 | `trade_value(p) = goods_produced(p) · price(good(p))`, ducats per year — no local trade-value modifier term. | MODEL | derivation | REVISED | X019 |
| Y029 | `tax_value(p) = TAX_COEFF · base_tax(p) · (1 + Σ province-state tax modifiers)`, ducats per year. | MODEL | derivation | REVISED | X020 |
| Y030 | ⚑ **`GP_COEFF` is a shipped file value:** `common/static_modifiers/00_static_modifiers.txt` carries `provincial_production_size = { trade_goods_size = 0.2 … }`, localised "Base Production" — the same tooltip line the coefficient was measured off. | ENGINE | file value | REVISED | W031, W089 |
| Y031 | It is therefore moddable and is **read at runtime**, not hardcoded. | DESIGN | derivation | NEW | — |
| Y032 | `TAX_COEFF` is in **no file that has been found** — neither `defines.lua`, `common/defines/`, nor that static-modifier block — so it stays a measured constant carrying the observation that produced it. | ENGINE | file value | REVISED | W031, W032, W089 |
| Y033 | ⚑ The tax tooltip's schema is `Base: trunc(base_tax / 12) (Yearly base_tax)` — observed `Base: 0.49 (Yearly 6.00)` at `base_tax` 6 and `Base: 0.16 (Yearly 2.00)` at `base_tax` 2. | ENGINE | engine test | REVISED | X021 |
| Y034 | The parenthetical is `base_tax` itself and the `Base` line is its truncated twelfth; it is **not** twelve times the displayed figure, which would give 5.88 and 1.92. | ENGINE | derivation | NEW | — |
| Y035 | v4.0 and v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both of its own data points; v3.0 carries neither that schema nor the 0.6125 arithmetic. | WORLD | derivation | NEW | — |
| Y036 | ⚑§ The monthly production tooltip's `Trade Value` line is only **consistent with** the annual-over-twelve relation, on one observation — 3.52 → `+0.29` — which fixes the divisor only to within **(11.73, 12.14]**. | ENGINE | engine test | REVISED | X022 |
| Y037 | The two wealth terms share a time basis and are safe to add; the tax pair establishes the annual-over-twelve relation at **two development levels**. | MODEL | derivation | REVISED | W036 |
| Y038 | ⚑§ Observed on Garnatah, `base_tax` 6 with `Tax Income Efficiency 125.0%` displays `Base 0.49` then `0.62`; since 0.49 × 1.25 = 0.6125 **truncates to 0.61**, the engine multiplies the untruncated monthly value — 6 × 0.0833… = 0.49999…, × 1.25 = 0.62499…, displayed 0.62. | ENGINE | engine test | REVISED | X027 |
| Y039 | The example establishes only the **ordering** — base from development first, percentage second — and nothing finer. | MODEL | derivation | NEW | — |
| Y040 | v3.0 through v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires rounding while §2.3 requires truncation; both cannot hold. | WORLD | derivation | NEW | — |
| Y041 | Flat goods bonuses *would* add into `goods_produced` before the price multiply — the tooltip carries an additive `Base Goods Produced` block above a multiplicative `Goods Produced Efficiency` block — but under §1.3 **no source grants one**, so the ordering is stated for the emitter and is exercised by no province in the model. | MODEL | derivation | REVISED | X028, X029 |
| Y042 | **Province condition is the one thing besides development and the good that wealth reads:** four static modifiers describe a province's own state, and all four are read from `common/static_modifiers/00_static_modifiers.txt`. | MODEL | stipulated | REVISED | X035 |
| Y043 | The four: `devastation` `trade_goods_size_modifier = -2` scaled by level, `prosperity` +0.25, `under_siege` −0.25, and `occupied` −0.5 **plus** `local_tax_modifier = -0.5`. Only `occupied` touches the tax term; the other three reach `goods_produced` alone. | ENGINE | file value | REVISED | X040 |
| Y044 | ⚑ **No shipped file states that the devastation scaling is linear in the level**; the model assumes `-2 × level/100`, which is an assumption and not a file value, and `prosperity` is likewise applied as stated without a file confirming its direction. | MODEL | stipulated | NEW | — |
| Y045 | The four are what make the map answer to war: §1.2's volatility, §3.3's "a besieged province genuinely produces less" and §2.8's war rows all rest on them. | DESIGN | derivation | NEW | — |
| Y046 | ⚑ **Eleven counted provinces begin devastated at 1444** — Bohemia at 50, Erzgebirge and Moravia at 20 — and no province-history file says so: the devastation is applied by `on_startup`, which fires `flavor_boh.15` ("The Aftermath of the Hussite Wars"). | ENGINE | engine test | REVISED | X040 |
| Y047 | It costs **13.40 ducats** across the eleven affected counted provinces. | MODEL | numerical test | NEW | — |
| Y048 | ⚑ The chain is `common/on_actions/00_on_actions.txt` → `on_startup_effect` → `common/scripted_effects/01_scripted_effects_for_on_actions.txt` → `country_event flavor_boh.15`. | ENGINE | file value | NEW | — |
| Y049 | **The start state is what the engine produces, not what the history files say** — the general form of the point, and it costs three separate reads. | DESIGN | derivation | NEW | — |
| Y050 | ⚑ `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`, `flavor_geo.1` and others directly from its own `events = { }` list in `00_on_actions.txt` — a second path alongside the `on_startup_effect` chain. | ENGINE | file value | NEW | — |
| Y051 | **Development itself does not move before the first tick:** the history parse matches the save on **2,472 of 2,472** provinces for `base_tax`, `base_production` and owner, and only `trade_goods` differs. | ENGINE | engine test | NEW | — |
| Y052 | v6.0's first draft said `flavor_geo.1` carries `add_base_tax` and could move development pre-tick; it does not — its whole effect is legitimacy, a country modifier and a flag, and those keys are in `flavor_geo.3`, which a mission fires and `on_startup` does not. | WORLD | file value | NEW | — |
| Y053 | ⚑ **`add_base_*` in a dated block before the start date accumulates:** province 1 (Uppland) has `base_tax = 5` undated plus 1 at `1436.4.28`, and the game has 6. | ENGINE | engine test | NEW | — |
| Y054 | v5.0 and earlier overwrote instead of adding, silently dropping the grant. | WORLD | derivation | NEW | — |
| Y055 | ⚑ **`is_city = yes` is not a filter the engine applies:** 20 owned provinces omit or comment out the line — province 265 among them, which is also one of the devastated eleven — and the engine treats them as cities. | ENGINE | engine test | NEW | — |
| Y056 | The model counts a province when it **has an owner and lies in a trade node**: **2,472** provinces, not 2,452. Unowned provinces stay outside the model. | MODEL | stipulated | REVISED | W050, X063 |
| Y057 | ⚑ **Twenty counted provinces have no trade good in their history file** (`trade_goods = unknown`); the engine assigns one at start from each good's `chance = { }` block. | ENGINE | file value | NEW | — |
| Y058 | The model does not predict the draw — it **reads the good the engine actually rolled**, as it does for development, and prices the province on that. | DESIGN | stipulated | NEW | — |
| Y059 | Pricing those twenty at zero instead would understate world wealth by **12.70 ducats**. | MODEL | numerical test | NEW | — |
| Y060 | §On this save the twenty came up seven `fur`, five `grain`, three `wool`, two `livestock`, and one each of `cotton`, `incense` and `naval_supplies`; a different roll gives a slightly different field and nothing in the model depends on which. | ENGINE | engine test | NEW | — |
| Y061 | `TAX_COEFF = 1.0`'s reference condition is applied to **every province the model counts**: ownership is not modelled, so every province is treated as cored **and settled** (v5.0 rested this on all of them being `is_city = yes`). | MODEL | derivation | REVISED | X063 |
| Y062 | *This is a modelling choice with a known cost* — two readings, both on cored city provinces at `base_tax` 2 and 6, are all `TAX_COEFF = 1.0` rests on, and `base_tax` at 1444 runs up to **33**. | MODEL | derivation | NEW | — |
| Y063 | Owner-agnostic wealth removes **a large** source of hidden owner-dependence from the aggregate graph (v3.0–v5.0: "the single largest"). | MODEL | derivation | REVISED | W052 |

## §1.4 — Market concentration (lines 320–331)

**UNCHANGED:** C040–C047. No delta claims.

## §1.5 — Goods without a graph (lines 334–381)

**UNCHANGED:** C048, C051–C056, V050–V058, W053, W182–W186, W188, W191.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y064 | Measured: repricing to coal the **45** owned latent-coal provinces flips **10 of 159** `Φ_w` edges and adds **214.60 ducats** to world wealth (`measure6.py`). | MODEL | numerical test | REVISED | X064 |
| Y065 | The counterfactual holds every non-repriced input fixed, and that matters by more than rounding: province **4237** is both latent-coal and one of the devastated eleven, so a reprice that also drops its devastation measures coal activating *plus* one province healing — worth 2.40 ducats and **3 extra flips**. | MODEL | numerical test | NEW | — |
| Y066 | Coal's base price of 10.0 is the highest **in the shipped price table** (`common/prices/00_prices.txt`) — scoped to the file rather than asserted of vanilla at large. | ENGINE | file value | REVISED | W189 |

## §1.6 — The aggregate graph (lines 384–517)

**UNCHANGED:** C059, C062, V063, V064, V212, V218, V221, W054, W055, W058, W063, X067, X090, X091,
X123.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y067 | **Both the count and the locations of `Φ_w`'s sinks move with the wealth field, and `α_Φ` sets how sharply concentration is read.** | MODEL | numerical test | REVISED | X065 |
| Y068 | At the stipulated α_Φ = 1.5 the 1444 field gives **two** sinks and a modestly grown Europe gives three or one, so neither the count nor the placement is fixed by the constant. | MODEL | numerical test | NEW | — |
| Y069 | v2.0–v4.0 ("the count emerges from concentration exactly as per-good sink counts do") and v5.0 ("the count is set by `α_Φ`") are **wrong the same way**: the count is a function of the field **and** the constant. | WORLD | derivation | REVISED | X065 |
| Y070 | v2.1 chose the value with a target count in view — a calibration §2.3 withdraws **without replacing**. | WORLD | derivation | REVISED | X066 |
| Y071 | Measured: identical orientation at ×1 and above, **12** edge flips at ×10⁻² and **100** at ×10⁻⁶, where the sink set also collapses to `{genua}`. | MODEL | numerical test | REVISED | X068 |
| Y072 | 1444's `b_w` has largest magnitude **0.0225**. | MODEL | numerical test | REVISED | X069 |
| Y073 | Measured at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and `hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12. *(Restores W059's rank pattern, which X070 had replaced.)* | MODEL | numerical test | REVISED | X070 |
| Y074 | Phase 1 selects **`genua`**; both sinks arrive by stall promotion and `genua` ends a transit node, so there are **2 promotions and 0 fallbacks**. | MODEL | numerical test | REVISED | X072 |
| Y075 | **Eight sources**, all in the bottom half of the wealth field, `c_w` ranks **44–75**, mean degree **3.1** against the map's 4.0 — and the node list v5.0 gave is dropped. | MODEL | numerical test | REVISED | X073 |
| Y076 | Every node drains to a sink; acyclic, 159/159 oriented; the sink set is unchanged under ±1% wealth noise on **three** seeds (v5.0: 0 edge flips and 0 sink changes across 5 seeds). | MODEL | numerical test | REVISED | X074 |
| Y077 | Per good on the same field, **90.2%** of ordered node pairs (**5,703 of 6,320**) are connected by at least one good's directed path. | MODEL | numerical test | NEW | — |
| Y078 | Agreement with the per-good graphs is **53.6%** of edge-goods, **52.3%** value-weighted. | MODEL | numerical test | REVISED | X075 |
| Y079 | The superseded marking-order aggregate **scored higher** on that measure; §3.9 records why the trade was taken and no figure is maintained for an operator the model does not install. | MODEL | derivation | REVISED | X076 |
| Y080 | **`α_Φ = 1.5` is a stipulated design constant exactly as `P₀ = 2.0` is:** superlinear so that a few very rich provinces outweigh a dense mediocre region, and round. | DESIGN | stipulated | REVISED | X083 |
| Y081 | It is **not** derived and the document no longer offers a derivation: v2.1–v4.0's two-sink calibration was fitted to a field that no longer exists, and v5.0's widest-band argument depended on where the α scan was truncated. | WORLD | derivation | REVISED | X083, X122 |
| Y082 | Scanned over [1, 8] rather than [1, 3], the widest band is **1.71** wide — [3.50, 5.21], `{doab, genua, hangzhou}` — and 1.5's is **not** the widest by any margin. | MODEL | numerical test | REVISED | X078 |
| Y083 | Across α_Φ = 1.00…8.00 at 0.01 the sink set is a step function, and α_Φ = 1.5 sits in the band **[1.38, 1.63], width 0.25**, which gives `{english_channel, hangzhou}`. | MODEL | numerical test | REVISED | X077, X078, X081 |
| Y084 | Sampled at the six values v2 used, the count is non-monotone: **6 → 2 → 1 → 2 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}. | MODEL | numerical test | REVISED | X084 |
| Y085 | A standing warning: the 1444 map has two ends and vanilla's authored map has three, and justifying 1.5 by that resemblance is the calibration §2.3 withdrew — a mistake already made twice. | DESIGN | stipulated | NEW | — |
| Y086 | **Europe becomes the centre of trade as it develops** is the design claim, and it is what §3.1's first goal asks the field to deliver. | DESIGN | stipulated | REVISED | X085, X088 |
| Y087 | At 1444 the map already ends in the Channel and in Hangzhou; as European development compounds the Channel's basin grows and Asia's pole fades, and past a broad range of European growth Asia holds no end at all. | MODEL | numerical test | NEW | — |
| Y088 | The mechanism carries it: wealth is linear in development, so developing a region moves its `c_w` share directly and `Φ_w`'s ends follow the wealth. | MODEL | derivation | NEW | — |
| Y089 | Scaling European development only over **824** counted European provinces (`europe.py`): ×1.00 → `{english_channel, hangzhou}`; ×1.02 → plus **`wien`**; ×1.56 → `{english_channel, rheinland}` with Asia holding none. | MODEL | numerical test | REVISED | X086, X087 |
| Y090 | At ×2.00 the map has a single end, **`genua` alone**. | MODEL | numerical test | NEW | — |
| Y091 | Read the table as a **direction rather than a trajectory**: the Channel holds an end throughout, Asia loses its own between ×1.02 and ×1.56, and growth concentrates the map on Europe without the Channel monotonically absorbing it. | MODEL | derivation | NEW | — |
| Y092 | These are properties of **this snapshot**, not constants of the model — what one field yielded under one scaling — and a different world state moves them. | DESIGN | stipulated | REVISED | X088 |
| Y093 | Scaling development and scaling wealth are **the same operation** — maximum difference 0.0 across the European set — so the distinction that made v5.0's version of this table wrong does not arise. | MODEL | numerical test | NEW | — |
| Y094 | All three institutions the period is named for begin **in Europe between 1450 and 1550**, independently of any threshold — Renaissance `1450.1.1` Florence (116), Colonialism `1500.1.1` Sevilla (224), Printing Press `1550.1.1` Frankfurt (1876). | ENGINE | file value | REVISED | X089 |
| Y095 | The 1444 route from Genoa to the Asian sink is the Silk Road: `genua → alexandria → aleppo → persia → lahore → **lhasa** → ganges_delta → burma → gulf_of_siam → canton → hangzhou`. | MODEL | numerical test | REVISED | X094 |
| Y096 | From the north the route is the Volga (the node list v5.0 gave is dropped). | MODEL | numerical test | REVISED | X095 |
| Y097 | **No route leaves `english_channel` at all** — it is a sink, out-degree 0 — so the Hansa and the Danube carry power *into* it rather than out. | MODEL | numerical test | REVISED | X096 |
| Y098 | **No Europe→sink route passes the Cape of Good Hope**, checked from `genua`, `north_sea` and `english_channel`. | MODEL | numerical test | REVISED | X097 |
| Y099 | The Cape is nonetheless a **live conduit**: in-degree 1, out-degree 3, with **132 ordered node pairs** whose path runs through it, carrying Atlantic drainage into the Indian Ocean. | MODEL | numerical test | NEW | — |
| Y100 | v5.0's "nothing routes through the Cape" is **false as a universal** and was only ever checked on the Europe→sink routes. | WORLD | derivation | NEW | — |
| Y101 | In the per-good graphs the Cape also carries Asian spices to Europe; `Φ_w` models power, not cargo. The route list v5.0 gave is dropped. | MODEL | numerical test | REVISED | X098 |
| Y102 | Scaling the 22 European **nodes** rather than European provinces makes `genua` the sole sink from about **×1.65**, and the 18-node western/central subset needs about **×2.15**. | MODEL | numerical test | REVISED | X099 |
| Y103 | Somewhere inside roughly **×2.9–×3.5** the Cape **reverses** — Atlantic→Cape→Indian-Ocean drainage becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast — and the reversal is bounded above as well as below, so it is a window whose edges move with the field. | MODEL | numerical test | REVISED | X100 |
| Y104 | Dev-stacking **a single node's** top province concentrates the map on that node, and extra sinks at intermediate boosts are expected behaviour, not noise — stated without the ×10/×20/×30/×50 `hangzhou` figures. | MODEL | numerical test | REVISED | X101, W064 |

## §1.7 — Merchants (lines 519–546) · §1.8 — Collection and transfer (lines 548–578) · §1.9 — Trade power propagation (lines 579–588)

**UNCHANGED:** C067–C083, V066, V068–V070, W065, W192, X102 *(§1.7)*; C084–C102, V072, X103, X104
*(§1.8)*; C103–C111, V073, W068, W069 *(§1.9)*. No delta claims — the probe-15 evidential revision
lands in §2.7 (Y132). **W067 is split:** its first clause (the tooltip's receiving-side qualifier is
descriptively false) is carried UNCHANGED and still stated in §1.9; its second clause (§1.9's rule
"is correct as written and gains no qualifier") is what Y132 replaces.

## §1.10 — Direction-dependent systems (lines 590–643)

**UNCHANGED:** C112–C143, V074, V078, V079, V080, W070, W071, X105, X109, X110, X196.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y105 | **Banding absorbs very little chatter** — a power share oscillating across any single-valued limit flickers the mechanic (v5.0: "almost nothing absorbs threshold chatter"). | ENGINE | derivation | REVISED | X106 |
| Y106 | ⚑ **Banding is not the only damper:** three shipped defines rate-limit the mechanics carrying these thresholds — `TRADING_POLICY_COOLDOWN_MONTHS = 12`, applying to **seven of the nine** trading policies including Propagate Religion (`maximize_profit` and `maximize_profit_upgraded` carry `cooldown = no` in `common/trading_policies/00_trading_policies.txt`), plus `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` and `TRADE_COMPANY_COOLDOWN = 60`. | ENGINE | file value | NEW | — |
| Y107 | So a flickering share does not translate into a flickering *effect* at those three; what is left exposed is everything without a cooldown, which is most of the ladder. | ENGINE | derivation | NEW | — |
| Y108 | Measured on the 1444 start: the caravan cap of 50 is **9.4% to 47.0%** of an inland node's total trade power, median **21.6%** over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. | MODEL | numerical test | REVISED | X107 |
| Y109 | As a share of the node's total **after** the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, median **17.7%**; v5.0 quoted those under the first description, which cannot be right, since 8.6% of 532.0 is 45.8 rather than 50. | MODEL | numerical test | REVISED | X107 |
| Y110 | On §2.2's derived 25-node inland basis the median is **21.3%**, or 17.5% after the grant. | MODEL | numerical test | REVISED | X108 |

## §1.11 — Treasure fleets · §1.12 — What the game displays (lines 645–670)

**UNCHANGED:** C144–C148, C149–C165, V049, V065, V081. No delta claims.

## §2.1 — Shape (lines 676–695)

**UNCHANGED:** C167–C184, V082–V085, W072, W073. No delta claims.

## §2.2 — Solver (lines 697–740)

**UNCHANGED:** C185–C209, V064, V091, V092, V229, W075, W076, X115.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y111 | Solver item 4 computes `TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production · (1 + province-state goods modifiers) · price`, with no autonomy, efficiency, ideas or owner terms and no local trade-value factor. | DESIGN | stipulated | REVISED | X111 |
| Y112 | The only modifiers read are the **four** describing the province's own condition, and at 1444 only `devastation` is live, on **eleven** provinces. | DESIGN | stipulated | REVISED | X112 |
| Y113 | World wealth is **10,607.40** annual ducats over **2,472** counted provinces. | MODEL | numerical test | REVISED | X113 |
| Y114 | Measured on the reference implementation (scipy/HiGHS plus the deterministic sweep, one machine): **of order 0.1 s for all 29 goods, and single-digit milliseconds per good on average** — "that is the whole of the claim". | MODEL | numerical test | REVISED | X114 |
| Y115 | Repeated 12-run experiments on one machine do not reproduce each other closely enough to support anything finer — three replicates gave per-good averages spanning 3.5–10.5, 3.5–10.8 and 3.1–4.7 ms — so no range is quoted, because the quantity measured is a machine and a scheduler rather than the algorithm. | MODEL | numerical test | NEW | — |
| Y116 | v5.0's "0.17–0.21 s for all 29 goods" was matched by **1, then 0, then 0** runs across three replicates of twelve. | WORLD | numerical test | NEW | — |

## §2.2a — What map this is for (lines 742–782)

**UNCHANGED:** W077–W085, W088, X116.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y117 | Where Phase 0 acts, free-edge determinism keeps its **determinism** half and loses its **index-independence** half: the key reads the post-fold balance β, so peeling can create exact ties the raw balances do not have, and the 1444 measurement does not transfer. v5.0 said peeling left both halves untouched. | MODEL | derivation | REVISED | X117 |

## §2.3 — Constants (lines 784–830)

**UNCHANGED:** C211–C227, V094, W090, W091, W097, W098, X118, X119, X120, X121, X123, and the
DLC-third-axis claim.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y118 | The two wealth coefficients are **not the same kind of constant**: `GP_COEFF` is read from a shipped file (Y030), while `TAX_COEFF` is in no file that has been found — `defines.lua`, `common/defines/` and the static-modifier tables were searched — and must be re-measured against any patch that is not 1.37.5. | ENGINE | file value | REVISED | W089 |
| Y119 | v3.0 through v5.0 said neither coefficient was in a file, and shipped a whole-install modifier sweep that walked past the block holding one of them. | WORLD | derivation | NEW | — |
| Y120 | **Every derivation previously offered for `α_Φ` is withdrawn** — the two-sink calibration (v2.1–v4.0) and the widest-band argument (v5.0) alike; neither is a reason. | DESIGN | stipulated | REVISED | X122 |

## §2.4 — The tradenodes file (lines 832–872)

**UNCHANGED:** C228–C233, C235–C242, V095, V148, W099, W100, W102–W107, W114, X124, X127.
*(The proposition that Phase 2, not a tiebreak, is why the node order is a correctness requirement is
Y006 at first appearance in §0.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y121 | The min-cost b-flow is **massively degenerate**: many distinct supports carry the same optimal cost, and which one the solver returns depends on the order the nodes and arcs are presented in. | MODEL | numerical test | NEW | — |
| Y122 | Measured on 1444: relabelling the nodes and running end-to-end changed the orientation on **580 of 580** runs (29 goods × 20 relabellings), **always** by returning a different optimal vertex and **never** by a sweep tiebreak, with a mean of **22.1 of 159** edges moving and the objective identical to 8.9e-16. | MODEL | numerical test | NEW | — |
| Y123 | Permuting only the **arc** presentation order with node labels held fixed changes the optimal support on **10 of 10** goods tested, with objective gaps ≤ 1.8e-15. | MODEL | numerical test | NEW | — |
| Y124 | Twenty-two flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event. | MODEL | derivation | NEW | — |
| Y125 | The canonical order must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks ties in. | DESIGN | derivation | NEW | — |
| Y126 | Everything §1.6 and §2.8 report about stability is measured **at fixed node order**; re-order the same world and the map moves, with `α_Φ` and every input held fixed. | MODEL | derivation | NEW | — |
| Y127 | The 580/580 result is HiGHS-specific in its detail but **not in kind** — any simplex returns *a* vertex of a degenerate optimal face. | MODEL | derivation | NEW | — |
| Y128 | Making the orientation independent of presentation order would need a tie-breaking objective — a lexicographic secondary cost or a strictly convex perturbation — which is a design change and is not adopted. | DESIGN | stipulated | NEW | — |
| Y129 | The priority key ties in **more places than §1.1 documents**: besides the free-edge sweep it decides Phase 1's within-cluster argmin, the stall promotion's identical form, and the top-k cut when two clusters carry equal mass. | MODEL | derivation | NEW | — |
| Y130 | **None of them fires on 1444** — zero exact `(DEF, β)` ties on free edges across 29/29 goods, zero within-cluster β ties, zero tied cluster masses — so no measured figure depends on them. | MODEL | numerical test | NEW | — |
| Y131 | End flags: 1444 has **two** end nodes, `english_channel` and `hangzhou`, against vanilla's three. | DESIGN | numerical test | REVISED | X126 |

## §2.5 — Runtime attachment · §2.6 — Writing to the engine (lines 874–900)

**UNCHANGED:** C243–C250, C251–C272. No delta claims.

## §2.7 — Probes (lines 902–939)

**UNCHANGED:** C274–C293, V098–V101, W108, W109 *(item 12 dropped)*, W110–W114.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y132 | §Probe 15: §1.9's "every immediately upstream node" is **consistent with** the observation — one observation on one node, enough to retire §3.16's cautionary case and **not** enough to promote the rule to a measurement. v3.0–v5.0 said the rule was "correct as written and gains no qualifier". | ENGINE | engine test | REVISED | W067 |

## §2.8 — Validation (lines 941–986)

**UNCHANGED:** C298–C342, V109–V112, W116, W117, W119, W195, X128, X133, X134, X135, X136, X137.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y133 | Sinks are **1 to 8** per good; high-demand nodes are sinks at **16.8%** in the top demand decile against 6.9% in the bottom — a barbell, LP branch ends landing in poor pockets. | MODEL | numerical test | REVISED | X129 |
| Y134 | Razed China: zeroing `hangzhou`-node development moves the `Φ_w` sinks from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`, with **23 of 159** edges flipping. | MODEL | numerical test | REVISED | X130 |
| Y135 | `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth **226.7 against 143.0**, and it holds the richest single province **the model counts** (the `c_w` rank comparison v5.0 gave is dropped). | MODEL | numerical test | REVISED | X131 |
| Y136 | Zeroing `beijing` **also** moves the map — **15** flips — because deleting a percent of world wealth renormalises `c_w` everywhere; what separates the two cases is that `hangzhou` survives as a sink when `beijing` is zeroed and does not when `hangzhou` is. | MODEL | numerical test | REVISED | X132 |
| Y137 | Latent-good row: repricing the 45 owned latent-coal provinces flips **13 of 159** `Φ_w` edges. | MODEL | numerical test | REVISED | X064 |

## §2.9 — Build order (lines 988–999) · §3.1 — Goals (lines 1005–1013)

**UNCHANGED:** C343–C352, C353–C365, V113, X136 *(the widened containment set)*, X138. No delta
claims.

## §3.2 — Why a flow and a drainage sweep (lines 1015–1112)

**UNCHANGED:** C366, C370–C375, C383–C385, V115, V116, V118–V122, V124, V128–V131, W120, W123,
W125–W128, X146, X147, X148, X149, X150.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y138 | **What the ratio metric cannot see is the thing the diagnosis rests on:** sparsity is the asymmetry — most nodes produce nothing at all of a given good, spices in 18 of 80 nodes and cloves in exactly one — so `(c−s)/deg` is dominated by *where* supply exists rather than by how large it is, and a max/min ratio over producing nodes is blind to that by construction. | MODEL | derivation | REVISED | X139, X141 |
| Y139 | On the contrast metric itself the demand side is the wider one, not the supply side — stated as a direction, with v5.0's 36-against-482.2 spices figures withdrawn. | MODEL | numerical test | REVISED | X140 |
| Y140 | Better wealth inputs move Genoa to a *co-*sink at **roughly ×1.7** without making demand the determinant of placement (v5.0: ×1.720). | MODEL | numerical test | REVISED | X142 |
| Y141 | Moving the spice sink to a Chinese node takes a multiple of that node's demand in the region of **3.6–4.9×** — observed on the 1444 field: `beijing` 3.61×, `hangzhou` 4.12×, `xian` 4.60×, `canton` 4.77×. The world-demand-share figures v5.0 paired with them are dropped. | MODEL | numerical test | REVISED | X143 |
| Y142 | The multiple a node needs and the share of world demand it then buys **do not line up end to end**, because the share depends on where the node started; other nodes in the region need more still. | MODEL | derivation | REVISED | X144 |
| Y143 | Sink placement: on 1444, final sinks = `{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal demanders}`, measured exact 29/29 — **a measurement on one input**, and v5.0's two rescuing conditions are necessary but not sufficient. | MODEL | numerical test | REVISED | X145 |

## §3.3 — Why wealth, and why per province (lines 1114–1136)

**UNCHANGED:** C386–C406, C408, C412, C413, V132, V133, V135, W132–W139. No delta claims.

## §3.4 — Why supply is pre-modifier (lines 1138–1146)

**UNCHANGED:** C415–C423, V137, V139, W140, W141, W142.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y144 | In v1 the production-income substitution broke the α = 1 identity, measured as orientation agreement **collapsing to well under half the map** — the 159/159 → 68/159 figures are withdrawn. | MODEL | numerical test | REVISED | V138 |

## §3.5 — Why α is anchored absolutely (lines 1148–1183)

**UNCHANGED:** C427–C442, V140–V144, V147, X152, X153, X156, X157.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y145 | ⚑ **`change_price` values are fractions of the good's base price, not ducats** — the shipped save `tutorial/eu4_tutorial_chapter10.eu4` settles it: `paper` sits at `current_price=4.375` on a base of 3.5, which is ×1.25 and not +0.25, and `gems` at 5.000 on a base of 4.0. | ENGINE | file value | NEW | — |
| Y146 | The install carries **161 textual** `change_price` blocks — 93 `events/`, 14 `missions/`, 1 `common/`, **53 `history/` of which 13 are negative** (all `history/countries/HAB - Austria.txt`) — and **none in `decisions/`**. | ENGINE | file value | REVISED | X154 |
| Y147 | ⚑ **Ten of the 161 never execute:** four sit inside `effect_tooltip = "…"` strings, three inside the `effect = "…"` string of a `country_event_with_effect_insight`, and three inside `tooltip = { }` display wrappers — so **151 are executable**. | ENGINE | file value | NEW | — |
| Y148 | Six of the seven quoted blocks duplicate one already counted in `events/`, and the seventh names a price key no event in the install ever sets. | ENGINE | file value | NEW | — |
| Y149 | All ten are positive and every negative block in the install is executable, so the sublinear-reachability partition is **identical under either census**. | ENGINE | derivation | REVISED | X155 |
| Y150 | v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them; both were wrong about which number was the executable one, and v5.0's claimed per-file count assertion **did not exist anywhere in its toolchain**. | WORLD | derivation | REVISED | X155 |
| Y151 | `verify6.py` now carries the guard, and a plain parse misses these for a mechanical reason: `pdx.py` tokenises a quoted string as one opaque unit, so a `change_price` inside a tooltip string is invisible to the walker. | WORLD | derivation | NEW | — |

## §3.6 — Why no hysteresis, and why there is no ε (lines 1185–1218) · §3.7 — Why eligibility is per good (lines 1220–1226)

**UNCHANGED:** C443–C446, C449, C452, V148, V152, V154, W147–W152; C463–C473. No delta claims.

## §3.8 — Why gates evaluate true (lines 1228–1248)

**UNCHANGED:** C474–C497, V155–V158, W154.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y152 | Measured under DRAIN, **89.6%** (**5,663 of 6,320**) of ordered node pairs are connected by at least one good on 1444 data, and the argument is unaffected because 89.6% is still most of the map. | MODEL | numerical test | REVISED | X158 |

## §3.9 — Why `Φ_w` is the installed graph (lines 1250–1288)

**UNCHANGED:** C502, C505–C510, C512, V160, V161, V162, V218, V221, V228, X161.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y153 | A rich non-sink node — `genua`, `gulf_of_siam` and `sevilla` rank **4th, 3rd and 7th** by node wealth on the corrected field, with **`mexico` 2nd**, at 296.0, 297.9 and 266.5 against `english_channel`'s 316.6, **which is a sink** — draws more edges in than it sends out. | MODEL | numerical test | REVISED | X159 |
| Y154 | `Φ_ord` scores **higher** than `Φ_w` on self-coherence with the per-good graphs — the cost of the trade, not disputed — but its ends are scheduling artifacts rather than places, **a majority** of them terminate no good, none of the demand capitals is among them, and the end count does not concentrate as demand concentrates. | MODEL | derivation | REVISED | X160 |
| Y155 | **No figure is maintained for `Φ_ord` here:** it is not the installed operator, its numbers moved with every change to the wealth field, three successive audits spent their effort recounting them, and the design argument does not depend on any of them. | DESIGN | stipulated | NEW | — |
| Y156 | v2.1–v4.0's "two vanilla-like ends at 1444" justification is not the argument and **should not be revived even though the 1444 field again gives two ends**: the count is a property of the field, not of the operator, and pinning the operator to it would be the withdrawn calibration. | WORLD | derivation | REVISED | X162 |
| Y157 | What the trade costs is self-coherence with the per-good graphs, which the marking-order aggregate scores higher on; what it buys is one operator, one set of guarantees and ends that sit where the wealth is — stated without the 7.8-point figure. | DESIGN | stipulated | REVISED | X163 |

## §3.10 — Why the engine's economy is overwritten (lines 1290–1306)

**UNCHANGED:** C513–C521, C523–C525, C528–C530, X164, X165, X167.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y158 | The two income forms agree to a worst relative disagreement of 0 to 3.7e-16 — **one to three** units in the last place (v5.0: "at most one unit"). | MODEL | numerical test | REVISED | X166 |
| Y159 | Propagation is **kept** on a single graph, and the reason is not the one v1 through v6.0's own first draft gave; reading the one installed graph leaves the propagated term good-independent, so the identity holds by construction. | MODEL | derivation | REVISED | X168 |
| Y160 | Per-good propagation makes a country's power at the node differ by good, because §1.9 reads a node's downstream neighbours and those differ per good: `gulf_of_siam`'s 29 goods leave it by **seven** distinct downstream sets (v5.0: eight). | MODEL | numerical test | REVISED | X169 |
| Y161 | **What that does *not* do is break the identity:** with `ps̄_C = Σ_g v_g·cs_g·ps_C(g) / Σ_g v_g·cs_g`, `collect_pool · ps̄_C = income_C` follows algebraically and `Σ_C ps̄_C = 1`, so `ps̄_C` is a legal share vector and one scalar per node still reproduces every collector's income exactly. | MODEL | derivation | REVISED | X170, X171 |
| Y162 | Both inputs already exist per good at write time, and §2.6 sums exactly them into `collect_pool`. | MODEL | derivation | NEW | — |
| Y163 | **The real cost is that `ps̄_C` is not derivable from trade power alone:** it is value-weighted, so installing it means writing a country a fictitious per-node trade power whose ratio happens to equal it, and every other consumer of that power field then reads the fiction. | ENGINE | derivation | NEW | — |
| Y164 | That is a claim about **what the engine exposes**, not about a magnitude, and it is why the single graph stays: on one graph the scalar *is* the country's power share, needing no invention. | DESIGN | derivation | REVISED | X172 |
| Y165 | Every magnitude previous versions quoted was an artifact of substituting some other weighting — v1–v4.0's "5.96 ducats on a node paying ~250", v4.0's 0.41%, v5.0's "redistributive and single-digit percent", v6.0's first draft's "at most 0.1%". | WORLD | derivation | REVISED | X170, X174 |
| Y166 | Gross-value weighting alone ranges from **0.00% to 4.6%** across collector sets on this field, and **up to 49%** in general, so each version measured its own construction; no figure is quoted here because the identity holds and the objection is structural. | MODEL | numerical test | NEW | — |
| Y167 | No node in the model has local trade value near 250 — stated without v5.0's "the largest is 112.6". | MODEL | numerical test | REVISED | X173 |

## §3.11 — Why caravan power needs a condition added · §3.12 — Why treasure fleets are always granted (lines 1308–1344)

**UNCHANGED:** C531–C547, C556–C560, V163–V172. No delta claims.

## §3.13 — Open questions (lines 1346–1424)

**UNCHANGED:** C561–C585, V173, V174, V175, V178, V181, V182, V183, W164, X175, X177, X178, X179,
X180, X183.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y168 | The one open wealth question is now a **design** question rather than a classification one: *should any source beyond province condition be allowed to multiply `goods_produced`?* §1.3 reads development, the trade good and the four province-state modifiers, and nothing else. | DESIGN | stipulated | REVISED | X176 |
| Y169 | ⚑ `trade_goods_size` and `trade_goods_size_modifier` are granted in many places — buildings, event modifiers, great projects, static and province-triggered modifiers, **holy orders, state edicts, trade-company investments** — and v3.0–v5.0 tried to admit the province-scoped subset by rule. | ENGINE | file value | REVISED | X176 |
| Y170 | Re-admitting any of those sources re-admits the maintenance burden with it, so the question to settle first is whether the fidelity is worth it. | DESIGN | stipulated | NEW | — |
| Y171 | Under the calibration's α = 16 the cloves demand order is `hangzhou`, `beijing`, `doab`, and the sink lands on a **high-demand node rather than a geographic accident**; v2's "Beijing holds the richest single province" is wrong — that is `hangzhou`. The Deccan demand-rank-2 framing and the 30.4/19.5 figures are dropped. | MODEL | numerical test | REVISED | X181, X182 |

## §3.14 — AI merchant assignment (lines 1426–1444)

**UNCHANGED:** C586–C624, X184. No delta claims.

## §3.15 — Rejected (lines 1446–1546)

**UNCHANGED:** C625–C672 as carried by v2, V184–V188, V192–V199, V226, V227, V228.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y172 | With v1's ε floor removed the contrasts run **4–97 on supply against 211–15,010 on demand** over the **28 goods produced in more than one node**, so the demand side is the wider one; `cloves` has a single producer and no contrast to measure, which is the sparsity point in miniature. | MODEL | numerical test | REVISED | X185 |
| Y173 | v3.0 and v4.0 repeated the 10⁷ ratio here while **v4.0's own** §3.2 was withdrawing it. | WORLD | derivation | REVISED | X186 |
| Y174 | Ranked orientation wins the sink–demand **alignment** statistics — it puts a far higher share of top-demand nodes in its sink sets than DRAIN — and loses on delivery: **a sixth of world demand** is stranded, it leaves orphan sinks a good cannot reach, it posts net-producer sinks where DRAIN, LAP and FLOW post none, and it keeps several times DRAIN's sinks per good. All stated as directions; no figures maintained. | MODEL | derivation | REVISED | X187, X188 |
| Y175 | Seeded basin growth leaves demand unserved **at every tuning tried** — the 88.4% best-tuning figure is withdrawn. | MODEL | derivation | REVISED | X189 |
| Y176 | The `Φ_ord` graveyard entry keeps **no figures**, and the self-coherence ceiling v2.0 and v2.1 quoted predates the deterministic sweep of §3.6 and was never regenerated after it. | MODEL | derivation | REVISED | X076 † |
| Y177 | The 3-mass gravity field **reproduces whatever end count it is seeded with while γ is small enough** and loses that property as γ approaches 1; no figures are maintained, and it is rejected on three grounds, **none numeric** — it pins the end count by fiat, it needs a second operator with its own reach knob γ, and a pure `wealth^α` edge comparison with no reach term does not concentrate ends at all because a local wealth maximum survives every positive α. | MODEL | derivation | REVISED | X190, X191 |

## §3.16 — Evidence standard (lines 1548–1645)

**UNCHANGED:** C677, C680–C682, C684, C685, V200–V203, V206–V210, W173–W181.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y178 | Implemented as written, the α = 1 identity's **residual reached 1e-5 against v1's ε of 1e-6**, and would have been diagnosed as a solver bug (v1–v5.0: "the identity failed at 1e-5"). | MODEL | numerical test | REVISED | V204 |

---

# Observations recorded during extraction

Not gradings — four places where the document states the same quantity twice with different values,
or states something the extraction could not attach to a single proposition. Recorded because an
inventory that absorbs them silently is worth less than one that shows them.

1. **Two figures for any-good pair connectivity.** §1.6 (Y077) gives **90.2%, 5,703 of 6,320**;
   §3.8 (Y152) gives **89.6%, 5,663 of 6,320**. Both are described as ordered node pairs connected by
   at least one good on 1444 data under DRAIN, and both are v6.0 figures.

2. **Two figures for the latent-coal flip count.** §1.5 (Y064) measures **10 of 159** edges under a
   counterfactual that holds every non-repriced input fixed, and notes **3 extra flips** if province
   4237's devastation is also dropped. §2.8's latent-good row (Y137) states **13 of 159** and
   cross-references §1.5. The two are reconcilable as the two counterfactuals, but §2.8 does not say
   which it is quoting.

3. **A truncated sentence in §1.6.** "From the north it is the Volga, and from **No route leaves
   `english_channel` at all**…" — the Volga clause is cut off mid-phrase and runs into the next
   proposition. Y096 and Y097 extract the two propositions the passage evidently intends; the text
   as it stands does not complete the first.

4. **A dangling cross-reference.** §1.6's "Under (c) scaling development and scaling wealth are the
   same operation" (Y093) refers to an item "(c)" that appears nowhere in the section. And §1.10
   counts **nine** trading policies (Y106) while §3.8 counts **five** ("Three of the five policies
   have no trade-share threshold at all", carried UNCHANGED as V155–V158/W154).

---

# † Unresolvable IDs

One `Replaces` target could not be pinned to a specific ID.

| Y ID | Section | Replaced proposition | Believed home |
|---|---|---|---|
| Y176 | §3.15 | "Retained as the measured coherence ceiling any future aggregate should be compared against" — the *stipulation*, as distinct from the 60.3% figure (which is X076, itself replacing W062). The stipulation was never extracted as its own row in `claims-v3.md` or `claims-v2.md`; greps for "ceiling" return only the note that `claims-v3.md` folds the §3.15 entry's figure into W062. | W062 / X076 |

**Two v5 † markers are left where they were.** X130 and X133 (the §2.8 Razed-China and Ming rows)
name C298–C342 as their believed range; Y134 and Y136 replace X130 and X132 directly, so the range
is not re-opened here. X138 (§3.1's Goal 1 example) is UNCHANGED in v6.0 and keeps its C353–C365 †.
