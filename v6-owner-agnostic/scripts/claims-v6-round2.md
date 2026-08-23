# Claim Inventory Delta — Per-Good Trade Network Spec v6.0

Extracted from `per-good-trade-spec.md` (v6.0, 1,607 lines) as a **delta against
`../v5-owner-agnostic/claims-v5.md`** (X001–X196), which is itself a delta against
`../v3-owner-agnostic/claims-v3.md` (W001–W195), `../v2-drain/claims-v2.md` (V001–V230) and
`../v1-laplacian/claims.md` (C001–C685). Extraction only: nothing here is validated, corrected or
commented on. Every row records what the document asserts, how it is typed, where its evidence
comes from, and how it stands against the prior inventory.

**Method.** The v6.0 spec was read in full, and `claims-v5.md` was read in full (header and all
196 rows). The v5.0 → v6.0 text diff was then computed and read hunk by hunk — 34 hunks,
313 removed lines against 409 added — so that every v6.0 proposition can be placed as unchanged text, changed text, or
new text, and so that the propositions v6.0 *deletes* can be identified rather than inferred.
`changes-v6.md` was used only to locate changed passages and to check that no edit had been missed;
it is not a source for any row, and where its section labels disagree with the diff (entry 45 is
§3.8, not §2.6) the diff was taken as authoritative. `claims-v3.md`, `claims-v2.md` and `claims.md`
were grepped to resolve nine `Replaces` targets that live outside `claims-v5.md`.

**ID prefix.** v1 used `C`, v2 used `V`, v3 used `W`, v4 got none, v5 used `X`. **v6 uses `Y`**,
numbered in document order, Y001–Y143 with no gaps.

**Statuses.** UNCHANGED — the same proposition as an existing C/V/W/X ID; the old ID is recorded in
the section's UNCHANGED list and no Y ID is issued. REVISED — the proposition changed; a new Y ID
with the old ID(s) in `Replaces`. NEW — no counterpart in any prior inventory. A proposition stated
in two sections keeps one ID at its first appearance, and the later section says which row it is.

**Vocabularies.** Type: ENGINE / MODEL / DESIGN / OUTCOME / WORLD. Provenance: stipulated /
derivation / file value / numerical test / engine test / prose source / verified (method unstated) /
UNSOURCED. `numerical test` (a solver experiment) and `engine test` (an observation of EU4 actually
running) are kept strictly distinct.

**Markers.** **⚑** a row introducing an engine fact no prior inventory carried. **§** a row whose
stated evidence is a single observation. **†** an unresolvable `Replaces` target — none occurs.

**Full-strength sections.** §1.3 (the rewritten wealth definition, the province-condition table and
the three start-state reads) and §1.6 (the two-sink result, the α_Φ paragraphs, the Europe table and
the 1444 route geography) were extracted row by row regardless of overlap, because that is where
v6.0's substantive change and its regenerated field both land.

---

# Summary

**143 delta claims extracted, Y001–Y143**, against v5.0's 196: **50 NEW, 93 REVISED**, replacing
**109 distinct prior IDs** (100 X, 7 W, 2 V, 0 C). A further **33 prior propositions are withdrawn
without a successor** — 24 of them the two-test classifier and its whole-install enumerations — and
are listed in their own table at the end.

### Delta claims by status and Type

| Type | NEW | REVISED | Total |
|---|---|---|---|
| MODEL | 15 | 63 | 78 |
| DESIGN | 12 | 12 | 24 |
| WORLD | 14 | 7 | 21 |
| ENGINE | 9 | 10 | 19 |
| OUTCOME | 0 | 1 | 1 |
| **Total** | **50** | **93** | **143** |

### Delta claims by Provenance

| Provenance | Count |
|---|---|
| derivation | 57 |
| numerical test | 51 |
| stipulated | 17 |
| file value | 14 |
| engine test | 4 |
| prose source | 0 |
| verified (method unstated) | 0 |
| UNSOURCED | 0 |
| **Total** | **143** |

No row in this delta carries UNSOURCED, prose-source or method-unstated provenance. The
derivation-heavy profile is the direct signature of v6.0's two prose rules: deleting the classifier
removed most of the file-value surface, and R3 converted maintained figures into directional
statements, which are typed `derivation`.

**Twelve rows are marked ⚑** — engine facts no prior inventory carried: Y025, Y027, Y031, Y034
(REVISED) and Y037, Y040, Y041, Y043, Y045, Y082, Y115, Y117 (NEW). Eight of the twelve are the
start-state and census work: `on_startup` devastation, `flavor_geo.1`'s development grants, dated
`add_base_*` accumulation, the missing `is_city` lines, the twenty unknown trade goods, the three
trading-policy cooldowns, and the two `change_price` findings.

**Three rows are marked §** — evidence resting on a single observation: Y029 (the production
tooltip's divisor, fixed only to [12.00, 12.14]), Y031 (Garnatah's 0.62) and Y104 (probe 15's one
node). That is down from v5.0's five, and two of the three now say so in the spec text itself.

### Where the delta concentrates

| Section | Y rows | What drove it |
|---|---|---|
| §1.3 Demand | 31 | wealth reduced to development + good + condition, the four-modifier table, and the three corrected start-state reads |
| §1.6 Aggregate graph | 31 | the regenerated field (two sinks again), α_Φ demoted to stipulated, the Europe table, the Cape correction |
| §0 Front matter | 11 | the new change summary plus the two prose rules R2 and R3 |
| §2.4 Tradenodes file | 9 | Phase 2's degenerate LP: the 580/580 relabelling sweep, the arc-permutation test, the wider tie inventory |
| §3.10 Income factoring | 9 | the exactness/magnitude split and the two substitution measurements |
| §3.5 α anchor | 8 | `change_price` as a fraction of base price, and the executable-versus-textual census |
| §1.1 Trade direction | 6 | the post-peel fallback condition and the "conditions are necessary, not sufficient" correction |
| §1.10, §2.2, §3.2, §3.15 | 5 each | cooldowns and the caravan-share re-reading; the field and the timing figure; the sparsity argument; R3 applied to the graveyard |
| §2.8, §3.9 | 4 each | |
| §1.5, §2.3, §3.13 | 2 each | |
| §2.2a, §2.7, §3.4, §3.16 | 1 each | |

Sections with no delta at all: §1.2, §1.4, §1.7, §1.8, §1.9, §1.11, §1.12, §2.1, §2.5, §2.6, §2.9,
§3.1, §3.3, §3.6, §3.7, §3.8, §3.11, §3.12, §3.14.
---

## §0 — Front matter (lines 1–44)

**UNCHANGED:** C002, C003, C004, V001 *(via §2.5)*, V002, V003, W001, W002.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y001 | v6.0 keeps v3.0's owner-agnostic wealth and makes it true **by construction** rather than by a rule that has to be policed; the substantive change to §1.3 is that wealth is a function of the province's development, its trade good and its own current condition, and of nothing else. | DESIGN | stipulated | REVISED | X002 |
| Y002 | The two-test modifier classifier and everything it governed — trade-good modifiers, great projects, permanent province modifiers, buildings, centres of trade, the DLC conditionality — are deleted, along with the whole-install sweep that maintained them. | DESIGN | stipulated | REVISED | X033, X035 |
| Y003 | On the 1444 start that deleted apparatus was worth **0.98%** of world wealth (§1.3 restates it as 87 of 2,472 provinces, `measure6.py`). | MODEL | numerical test | NEW | — |
| Y004 | What the apparatus cost was an input surface whose classification was wrong in every audit that examined it. | WORLD | derivation | NEW | — |
| Y005 | Three start-state reads are corrected in the same pass: `on_startup` devastation, dated `add_base_*` accumulation, and the `is_city` filter the engine does not apply. | WORLD | derivation | NEW | — |
| Y006 | A canonical node order is a correctness requirement because **Phase 2's min-cost flow is degenerate**, so presentation order selects which optimum is returned (argued in full at §2.4 item 1). | MODEL | numerical test | REVISED | X125 |
| Y007 | Prose convention **R2 — no empirical absolutes**: no superlative, no universal quantifier and no threshold asserted as a fact about the world; every claim is either a directional design statement or an observation scoped to the field and script that produced it. | DESIGN | stipulated | NEW | — |
| Y008 | Prose convention **R3 — no maintained figures for any rejected operator**: §3.15's graveyard keeps its design arguments and loses its measurements (`Φ_ord`, the gravity kernels, the v1 Laplacian, RANK, the seeded basins), and a load-bearing comparison is stated as a direction rather than a figure. | DESIGN | stipulated | NEW | — |
| Y009 | Those rejected-operator numbers were re-measured and re-refuted in three successive audits and not one of the rejection arguments depends on them. | WORLD | derivation | NEW | — |
| Y010 | Every graded claim from `validation-v5.md` — **22 refuted, 39 partial, 1 unverifiable** — is folded through, and `fixes-agreed.md` maps each one to the change that answers it. | WORLD | stipulated | REVISED | X001 |
| Y011 | Measured figures carry the script that produced them, and `scripts/verify6.py` re-derives each one **from the document text** and fails if the two disagree. | DESIGN | stipulated | REVISED | X004 |

## §1.1 — Trade direction (lines 48–152)

**UNCHANGED:** the v5 list for this section, plus X005, X006, X007, X012, X014, X015, X016, X017 —
the four phases, the fallback rule itself, the four stated properties, scan-invariance and the
efficiency non-measurement are all carried verbatim.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y012 | The fallback fires only when every candidate is support-isolated with zero **post-peel** balance: the key reads the balance Phase 0 hands on, with each pendant folded into its parent, so a map with non-zero raw balances can still reach the branch. | MODEL | derivation | REVISED | X008 |
| Y013 | On a connected core the folded balance must vanish across the core — for a per-good graph a component with no producer and no consumer, and for the aggregate graph each node's `Σ wealth^α_Φ` equal, which uniform *wealth* gives but is not the same condition. | MODEL | derivation | REVISED | X009 |
| Y014 | Where the wealth key ties, the **node index decides**, which is why §2.8 asserts containment over a set that includes the fallbacks. | MODEL | derivation | REVISED | X010 |
| Y015 | The fallback's index tiebreak is **not** the reason §2.4 requires a canonical node order; that requirement is stronger and is set by Phase 2. | MODEL | derivation | REVISED | X011 |
| Y016 | On 1444 the fallback and pendant cases are empty and the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods, **1–8 sinks per good, mean 3.52**, zero fallbacks. | MODEL | numerical test | REVISED | X013 |
| Y017 | That equality is a measurement on this input and does not become a theorem by attaching conditions: "Phase 0 a no-op and no fallback firing" looks sufficient and is not, because **T2** satisfies both and still breaks it. | MODEL | derivation | REVISED | X145 |

## §1.2 — Supply (lines 153–165)

**UNCHANGED:** C023, C025–C028, V038–V041. No delta claims.

## §1.3 — Demand (lines 166–300) — full-strength extraction

**UNCHANGED:** C031, C032, C033, C035, C036, C039, W024, W025, W026, W030, W031, W032, W042,
W043, W044, W047, W051, and X023, X024, X025, X026, X059, X060, X061, X062. The classifier rows
v6.0 deletes outright are listed under *Withdrawn prior IDs* at the end.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y018 | Wealth reads three things about the province — its development, its trade good and its own current condition — and two provinces alike in those three have the same wealth whoever owns them. | MODEL | stipulated | REVISED | W023 |
| Y019 | Owner-agnosticism is true by construction, not by a policed rule: `base_tax`, `base_production` and the trade good are bare attributes of the place, so nothing about them needs classifying. | DESIGN | derivation | NEW | — |
| Y020 | v3.0 through v5.0 stated the property and then defended it with a two-test classifier over an install sweep — a large surface to keep correct, and one that was wrong in every audit that examined it. | WORLD | derivation | NEW | — |
| Y021 | What this gives up: `gems`' `local_tax_modifier` and `incense`' `trade_value_modifier` are genuinely province-scoped and are no longer read, along with great projects, permanent province modifiers, and the DLC state they depended on. | DESIGN | stipulated | REVISED | X035, X036, X037 |
| Y022 | `goods_produced(p) = GP_COEFF · base_production(p) · (1 + Σ province-state goods modifiers)` — no local-modifier sweep term and no flat-bonus term. | MODEL | derivation | REVISED | X018 |
| Y023 | `trade_value(p) = goods_produced(p) · price(good(p))` ducats per year, with no trade-value-modifier term. | MODEL | derivation | REVISED | X019 |
| Y024 | `tax_value(p) = TAX_COEFF · base_tax(p) · (1 + Σ province-state tax modifiers)`, ducats per year. | MODEL | derivation | REVISED | X020 |
| Y025 | ⚑ **`GP_COEFF` is a shipped file value**: `common/static_modifiers/00_static_modifiers.txt` carries `provincial_production_size = { trade_goods_size = 0.2 … }`, localised "Base Production" — the same tooltip line it was measured off — so it is moddable and is read at runtime rather than hardcoded. | ENGINE | file value | REVISED | W089 |
| Y026 | `TAX_COEFF` is in no file that has been found — `defines.lua`, `common/defines/` and that static-modifier block were searched — so it stays a measured constant carrying its observation. | ENGINE | file value | REVISED | W089 |
| Y027 | ⚑ The tax tooltip's schema is `Base: trunc(base_tax / 12) (Yearly base_tax)`: the parenthetical is `base_tax` itself and the `Base` line its truncated twelfth, **not** twelve times the displayed figure, which would give 5.88 and 1.92 — observed `0.49 (Yearly 6.00)` at `base_tax` 6 and `0.16 (Yearly 2.00)` at 2. | ENGINE | engine test | REVISED | X021 |
| Y028 | v3.0 through v5.0 wrote that schema as `Base: X (Yearly 12·X)`, which is false on both of its own data points. | WORLD | derivation | NEW | — |
| Y029 | § The monthly production tooltip's `Trade Value` line is *consistent with* the same annual-over-twelve relation on one observation, 3.52 → `+0.29`, which fixes the divisor only to within [12.00, 12.14]. | ENGINE | engine test | REVISED | X022 |
| Y030 | Both monthly figures being the annual value over twelve is what lets the annual forms add directly, and the tax pair establishes it at two development levels. | MODEL | derivation | REVISED | W036 |
| Y031 | ⚑§ On Garnatah, `base_tax` 6 with `Tax Income Efficiency 125.0%` displays `Base 0.49` and then `0.62`; since 0.49 × 1.25 = 0.6125 truncates to 0.61, the engine multiplies the *untruncated* monthly value (0.49999… × 1.25 = 0.62499…), and the example establishes the ordering — base from development first, percentage second — and nothing finer. | ENGINE | engine test | REVISED | X027 |
| Y032 | v3.0 through v5.0 read that observation as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires rounding while §2.3 requires truncation; both cannot hold. | WORLD | derivation | NEW | — |
| Y033 | Flat goods bonuses *would* add into `goods_produced` before the price multiply — the tooltip's additive block sits above a multiplicative one — but under §1.3 no source grants one, so the ordering is stated for the emitter's benefit and is exercised by no province in the model. | MODEL | derivation | REVISED | X028, X029 |
| Y034 | ⚑ Province condition is the one thing besides development and the good that wealth reads: four static modifiers from `00_static_modifiers.txt` — `devastation` (`trade_goods_size_modifier = -2`, **scaled by the devastation level**), `prosperity` +0.25, `under_siege` −0.25, and `occupied` −0.5 plus `local_tax_modifier` −0.5. | ENGINE | file value | REVISED | X040 |
| Y035 | Only `occupied` touches the tax term; the other three reach `goods_produced` alone. | MODEL | derivation | NEW | — |
| Y036 | Those four are what make the map answer to war: §1.2's volatility and §3.3's "a besieged province genuinely produces less" both rest on them, and §2.8's war rows are their test. | DESIGN | derivation | NEW | — |
| Y037 | ⚑ **Eleven counted provinces begin the 1444 start devastated** — Bohemia at 50, Erzgebirge and Moravia at 20 — with no province-history file saying so: the devastation comes from `on_startup` firing `flavor_boh.15`, via `00_on_actions.txt` → `on_startup_effect` → `01_scripted_effects_for_on_actions.txt`. Refutes X040's "all are zero at the 1444 start". | ENGINE | file value | NEW | — |
| Y038 | That start devastation costs **13.40 ducats** across the eleven affected counted provinces (`measure6.py`). | MODEL | numerical test | NEW | — |
| Y039 | The start state is what the engine produces, not what the history files say — the general form of the point, and it costs three separate reads. | DESIGN | derivation | NEW | — |
| Y040 | ⚑ `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`, `flavor_geo.1` and others, and `flavor_geo.1` carries `add_base_tax`, `add_base_production` *and* `add_devastation`, so development itself can move before the first tick. | ENGINE | file value | NEW | — |
| Y041 | ⚑ `add_base_*` in a dated block before the start date **accumulates**: province 1 (Uppland) has `base_tax = 5` undated plus 1 at `1436.4.28`, and the game has 6. | ENGINE | file value | NEW | — |
| Y042 | v5.0 and earlier overwrote instead of adding such grants, silently dropping them. | WORLD | derivation | NEW | — |
| Y043 | ⚑ **`is_city = yes` is not a filter the engine applies**: 20 owned provinces omit or comment out the line — province 265 among them, itself one of the devastated eleven — and the engine treats them as cities. | ENGINE | file value | NEW | — |
| Y044 | The model counts a province when it has an owner and lies in a trade node — **2,472** provinces, not 2,452 — and treats every counted province as cored and settled, since ownership is not modelled. | MODEL | derivation | REVISED | X063, W050 |
| Y045 | ⚑ **Twenty counted provinces carry no trade good in their history file** (`trade_goods = unknown`), and the engine assigns one at start from each good's `chance = { }` block. | ENGINE | file value | NEW | — |
| Y046 | The wealth field is therefore partly the result of one random draw, and the model does not predict the draw: it reads whatever state the game currently holds, as it does for development. | DESIGN | stipulated | NEW | — |
| Y047 | `TAX_COEFF = 1.0` is a modelling choice with a known cost: two readings, both on cored city provinces at `base_tax` 2 and 6, are what it rests on, and the development range runs past 50. | DESIGN | derivation | NEW | — |
| Y048 | Owner-agnostic wealth removes **a large** source of hidden owner-dependence from the aggregate graph — not "the single largest", as v3.0 through v5.0 had it. | MODEL | derivation | REVISED | W052 |

## §1.4 — Market concentration (lines 301–312)

**UNCHANGED:** C040–C047. No delta claims.

## §1.5 — Goods without a graph (lines 313–360)

**UNCHANGED:** C048, C051–C056, V050–V058, W053, W182–W186, W188, W191 — the gold exclusion
paragraph and the whole activation-moves-the-field argument are carried verbatim from v5.0.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y049 | Measured: repricing to coal the 45 owned latent-coal provinces flips **13 of 159 `Φ_w` edges** and adds **217 ducats** to world wealth (`measure6.py`). | MODEL | numerical test | REVISED | X064 |
| Y050 | Coal's base price of 10.0 is the highest **in the shipped price table** (`common/prices/00_prices.txt`, `measure6.py`), so a coal activation is near the upper end of what one good's activation can do. | ENGINE | file value | REVISED | W189 |

## §1.6 — The aggregate graph (lines 361–491) — full-strength extraction

**UNCHANGED:** C059, C062, V063, V064, V212, V218, V221, W054, W055, W058, W063, W064, and X067
(what the world state moves), X089, X090, X091 (the institution file facts). *(X090's wording lost
its "5%" gloss while keeping `development_cost = -0.05`, and X089's "inside the window" became
"between 1450 and 1550"; neither changes the proposition.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y051 | **Both the sink count and the sink locations move with the wealth field**, and `α_Φ` sets how sharply concentration is read: at α_Φ = 1.5 the 1444 field gives two sinks and a modestly grown Europe gives three or one, so neither is fixed by the constant. | MODEL | numerical test | REVISED | X065 |
| Y052 | v2.0–v4.0's "the count emerges from concentration" and v5.0's "the count is set by `α_Φ`" are wrong the same way: the count is a function of the field **and** the constant. | WORLD | derivation | NEW | — |
| Y053 | v2.1 chose the value with a target count in view — a calibration §2.3 withdraws **without replacing**. | WORLD | derivation | REVISED | X066 |
| Y054 | Scale: identical orientation at ×1 and above, **12 edge flips at ×10⁻² and 100 at ×10⁻⁶**, so the orientation degrades while the sink set happens to survive. | MODEL | numerical test | REVISED | X068 |
| Y055 | 1444's `b_w` has largest magnitude **0.0226**. | MODEL | numerical test | REVISED | X069 |
| Y056 | Measured at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and `hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12. | MODEL | numerical test | REVISED | X070 |
| Y057 | Phase 1 selects `genua`; both sinks arrive by **stall promotion** and `genua` ends a transit node, so there are **2 promotions and 0 fallbacks**. | MODEL | numerical test | REVISED | X072 |
| Y058 | **Eight sources**, all in the bottom half of the wealth field (`c_w` ranks **44–75**), mean degree **3.1** against the map's 4.0 — which is what v2's "cul-de-sacs" does not survive. | MODEL | numerical test | REVISED | X073 |
| Y059 | Every node drains to a sink; acyclic, 159/159 oriented; the sink set is unchanged under ±1% wealth noise on **three** seeds. | MODEL | numerical test | REVISED | X074 |
| Y060 | Per good on the same field: 29/29 acyclic, 0 fallbacks fired, and **90.2%** of ordered node pairs (5,703 of 6,320) connected by at least one good's directed path. | MODEL | numerical test | REVISED | X158 |
| Y061 | Agreement with the per-good graphs is **53.5%** of edge-goods, **52.1%** value-weighted. | MODEL | numerical test | REVISED | X075 |
| Y062 | The superseded marking-order aggregate scored **higher** on that measure, and no figure for it is maintained here. | MODEL | derivation | REVISED | X076 |
| Y063 | `α_Φ = 1.5` is a **stipulated** design constant exactly as `P₀ = 2.0` is — superlinear so a few very rich provinces outweigh a dense mediocre region, and round — and the document offers no derivation for it. | DESIGN | stipulated | REVISED | X083 |
| Y064 | Scanned over [1, 8] rather than [1, 3] the widest sink-count band is **1.70** wide ([3.51, 5.21], `{doab, genua, hangzhou}`) and 1.5's is not the widest by any margin, so v5.0's widest-band ground depended on where the scan was truncated. | MODEL | numerical test | NEW | — |
| Y065 | Across α_Φ = 1.00…8.00 at 0.01 the sink set is a step function, and 1.5 sits in the band **[1.38, 1.63], width 0.25**, which gives `{english_channel, hangzhou}`. | MODEL | numerical test | REVISED | X077, X078, X079, X080, X081 |
| Y066 | Sampled at the six values v2 used, the count is non-monotone: **6 → 2 → 1 → 2 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}. | MODEL | numerical test | REVISED | X084 |
| Y067 | A written warning against re-deriving 1.5 from the resemblance between the two-end 1444 map and vanilla's three authored ends: that is the calibration §2.3 withdrew, and §3.9's adoption argument does not rest on it. | DESIGN | stipulated | NEW | — |
| Y068 | Design claim: **Europe becomes the centre of trade as it develops** — at 1444 the map already ends in the Channel and in Hangzhou, and as European development compounds the Channel's basin grows, Asia's pole fades, and past a broad range of European growth Asia holds no end at all. | DESIGN | stipulated | REVISED | X085, X088 |
| Y069 | The mechanism carries it: wealth is linear in development, so developing a region moves its `c_w` share directly and `Φ_w`'s ends follow the wealth. | MODEL | derivation | NEW | — |
| Y070 | Observed on the 1444 field at α_Φ = 1.5, scaling European development only (`europe.py`, **824** counted European provinces): ×1.00 → `{english_channel, hangzhou}`; ×1.02 → plus **`wien`**; ×1.56 → `{english_channel, rheinland}` with Asia holding none; ×2.00 → `genua` alone. | MODEL | numerical test | REVISED | X086, X087 |
| Y071 | Those rows are properties of this snapshot, not constants of the model — what one field yielded under one scaling. | DESIGN | stipulated | NEW | — |
| Y072 | Under the v6.0 wealth model **scaling development and scaling wealth are the same operation** — maximum difference 0.0 across the European set — so the distinction that made v5.0's version of this table wrong does not arise. | MODEL | numerical test | NEW | — |
| Y073 | The 1444 Genoa→Asian-sink route is the Silk Road: `genua → alexandria → aleppo → persia → lahore → lhasa → ganges_delta → burma → gulf_of_siam → canton → hangzhou`. | MODEL | numerical test | REVISED | X094 |
| Y074 | From the north the route is the Volga and from the Channel the Hansa and the Danube — stated without node chains. | MODEL | numerical test | REVISED | X095, X096 |
| Y075 | **No Europe→sink route passes the Cape of Good Hope**, checked from `genua`, `north_sea` and `english_channel`, which is what a 1444 map should say. | OUTCOME | numerical test | REVISED | X097 |
| Y076 | The Cape is a live conduit rather than an idle one: in-degree 1, out-degree 3, with **132 ordered node pairs** whose path runs through it (`measure6.py`), carrying Atlantic drainage into the Indian Ocean. | MODEL | numerical test | NEW | — |
| Y077 | v5.0's "nothing routes through the Cape" is false as a universal and was only ever checked on the Europe→sink routes. | WORLD | derivation | NEW | — |
| Y078 | In the per-good graphs the Cape also carries Asian spices to Europe; `Φ_w` models power, not cargo. | MODEL | derivation | REVISED | X098 |
| Y079 | Scaling the 22 European **nodes** rather than European provinces makes `genua` the sole sink from about **×1.65**, and the 18-node western/central subset needs about **×2.15**. | MODEL | numerical test | REVISED | X099 |
| Y080 | Somewhere inside roughly **×2.9–×3.5** the Cape of Good Hope **reverses** — Atlantic→Cape→Indian-Ocean becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast — and it is bounded above as well as below, so a window and not a threshold, with edges that move with the field. | MODEL | numerical test | REVISED | X100 |
| Y081 | Dev-stacking a single node's top province concentrates the map on that node, and extra sinks at intermediate boosts are expected behaviour rather than noise. | MODEL | numerical test | REVISED | X101 |

## §1.7 — Merchants (lines 492–519)

**UNCHANGED:** C067–C083, V066, V068, V069, V070, W065, W192, X102. No delta claims.

## §1.8 — Collection and transfer (lines 520–551)

**UNCHANGED:** C084–C102, V072, X103, X104. No delta claims.

## §1.9 — Trade power propagation (lines 552–562)

**UNCHANGED:** C103–C111, V073, W068, W069. *(W067 is revised at §2.7, Y104.)* No delta claims.

## §1.10 — Direction-dependent systems (lines 563–615)

**UNCHANGED:** C112–C143, V074, V078, V079, V080, W070, W071, X105, X109, X110, X196.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y082 | ⚑ Three shipped defines rate-limit the mechanics that carry these thresholds — `TRADING_POLICY_COOLDOWN_MONTHS = 12` (both banded policies), `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` and `TRADE_COMPANY_COOLDOWN = 60` — so a flickering power share does not translate into a flickering *effect* at those three. | ENGINE | file value | NEW | — |
| Y083 | Banding absorbs **very little** chatter rather than almost none, cooldowns damp three mechanics, what is left exposed is everything without a cooldown (most of the ladder), and the flicker-risk set stays "every country at a single-valued limit, plus flagless countries at Propagate Religion's 50/50 or 35/35". | ENGINE | derivation | REVISED | X106 |
| Y084 | Measured on the 1444 start: the caravan cap of 50 is **9.4% to 47.0%** of an inland node's total trade power, median **21.9%** over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. | MODEL | numerical test | REVISED | X107 |
| Y085 | As a share of the node's total **after** the grant lands — 50/(total+50) — the same figures read 8.6%–32.0%, median 17.9%; v5.0 quoted those under the first description, which cannot be right since 8.6% of 532.0 is 45.8 rather than 50. | WORLD | derivation | NEW | — |
| Y086 | On §2.2's derived 25-node inland basis only the median moves, to **21.3%**. | MODEL | numerical test | REVISED | X108 |

## §1.11 — Treasure fleets · §1.12 — What the game displays (lines 616–642)

**UNCHANGED:** C144–C148, C149–C165, V049, V065, V081. No delta claims.

## §2.1 — Shape (lines 647–665)

**UNCHANGED:** C167–C184, V082–V085, W072, W073. No delta claims.

## §2.2 — Solver (lines 666–706)

**UNCHANGED:** C185–C209, V064, V091, V092, V229, W075, W076, X115 (the refused projection), and
the derived-inland result — 25 nodes against the flag's 26, disagreeing only at `siberia`.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y087 | Solver item 4 computes `TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production · (1 + province-state goods modifiers) · price`, with no autonomy, efficiency, ideas or owner terms. | DESIGN | stipulated | REVISED | X111 |
| Y088 | The only modifiers the solver reads are the four describing the province's own condition, and at 1444 only `devastation` is live, on eleven provinces; `GP_COEFF` is read from `00_static_modifiers.txt` rather than hardcoded. | DESIGN | stipulated | REVISED | X112 |
| Y089 | World wealth is **10,594.70** annual ducats over **2,472** counted provinces. | MODEL | numerical test | REVISED | X113 |
| Y090 | Measured on the reference implementation: **of order 0.1 s for all 29 goods and single-digit milliseconds per good on average** — repeated runs span roughly 0.09–0.27 s and 3–7 ms per good, with individual goods reaching about 20 ms, so no two-significant-figure range is quoted. | MODEL | numerical test | REVISED | X114 |
| Y091 | v5.0 quoted "0.17–0.21 s"; twelve fresh runs put only one inside that interval. | WORLD | numerical test | NEW | — |

## §2.2a — What map this is for (lines 707–748)

**UNCHANGED:** W077–W085, W088, X116.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y092 | Where Phase 0 acts, free-edge determinism weakens asymmetrically: the determinism half is unaffected, but the **index-independence half is not** — the key reads the post-fold balance β, so peeling can create exact ties the raw balances do not have, and the 1444 measurement does not transfer. | MODEL | derivation | REVISED | X117 |

## §2.3 — Constants (lines 749–800)

**UNCHANGED:** C211–C227, V094, W090, W091, W097, W098, the DLC-third-axis claim, and X118, X119,
X120, X121, X123 — the two coefficient measurements, the truncation rule, the base-line
justification and the recording rule for any future `α_Φ`.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y093 | v3.0 through v5.0 said neither wealth coefficient was in a file, and shipped a whole-install modifier sweep that walked past the block holding one of them. | WORLD | derivation | NEW | — |
| Y094 | **Every derivation previously offered for `α_Φ` is withdrawn**: v2.1–v4.0's two-sink calibration fits a constant to one date, and v5.0's widest-band argument depended on where the α scan was truncated. | DESIGN | derivation | REVISED | X122 |

## §2.4 — The tradenodes file (lines 801–866)

**UNCHANGED:** C228–C233, C235–C242, V095, V148, W099, W100, W102–W107, W114, X124, X127, and the
node-window-renders-in-declaration-order consequence. *(The degeneracy proposition itself is Y006 at
first appearance in §0.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y095 | Measured on 1444: relabelling the nodes and running end-to-end changed the orientation on **580 of 580** runs (29 goods × 20 relabellings), **always** by returning a different optimal vertex and never by a sweep tiebreak, with a mean of **22.1 of 159 edges** moving and the objective identical to 8.9e-16. | MODEL | numerical test | NEW | — |
| Y096 | Permuting only the arc presentation order with node labels held fixed changes the optimal support on **10 of 10 goods** tested, with objective gaps ≤ 1.8e-15. | MODEL | numerical test | NEW | — |
| Y097 | Twenty-two flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event. | MODEL | derivation | NEW | — |
| Y098 | The canonical order must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks ties in, and everything §1.6 and §2.8 report about stability is measured at fixed node order — re-order the same world and the map moves with `α_Φ` and every input held fixed. | DESIGN | derivation | NEW | — |
| Y099 | The 580/580 result is HiGHS-specific in its detail but not in kind: any simplex returns *a* vertex of a degenerate optimal face. | MODEL | derivation | NEW | — |
| Y100 | Making the orientation independent of presentation order would need a tie-breaking objective — a lexicographic secondary cost or a strictly convex perturbation — which is a design change and is not adopted here. | DESIGN | stipulated | NEW | — |
| Y101 | The priority key ties in more places than §1.1 documents: besides the free-edge sweep it decides Phase 1's within-cluster argmin, the stall promotion's identical form, and the top-k cut when two clusters carry equal mass. | MODEL | derivation | NEW | — |
| Y102 | None of those tie sites fires on 1444 — zero exact `(DEF, β)` ties on free edges across 29/29 goods, zero within-cluster β ties, zero tied cluster masses — so no measured figure here depends on them. | MODEL | numerical test | NEW | — |
| Y103 | End flags: 1444 has **two** end nodes, `english_channel` and `hangzhou`, against vanilla's three. | DESIGN | numerical test | REVISED | X126 |

## §2.5 — Runtime attachment · §2.6 — Writing to the engine (lines 867–894)

**UNCHANGED:** C243–C250, C251–C272. No delta claims.

## §2.7 — Probes (lines 895–934)

**UNCHANGED:** C274–C293, V098–V101, W108–W114, including item 12's drop and the settled results
for probes 13 and 14 and the link-reversal check.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y104 | § Probe 15: §1.9's "every immediately upstream node" is **consistent with** the observation rather than confirmed by it — one observation on one node, enough to retire the cautionary case and not enough to promote the rule to a measurement. | ENGINE | engine test | REVISED | W067 |

## §2.8 — Validation (lines 935–978)

**UNCHANGED:** C298–C342, V109–V112, W116, W117, W119, W195, X128, X133, X134, X135, X136, X137.
*(The agreement figures and the latent-coal flip count are Y061 and Y049 at first appearance.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y105 | Most goods, 1444: sinks are 1 to **8** per good, and high-demand nodes are sinks at **16.8%** in the top demand decile against 6.9% in the bottom. | MODEL | numerical test | REVISED | X129 |
| Y106 | Razed China: zeroing `hangzhou`-node development moves the `Φ_w` sinks from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`, with **23 of 159** edges flipping. | MODEL | numerical test | REVISED | X130 |
| Y107 | `hangzhou`, not `beijing`, is China's wealth pole under §1.3 — node wealth **226.7 against 143.0** — and it holds the richest single province **the model counts**. | MODEL | numerical test | REVISED | X131 |
| Y108 | Zeroing `beijing` also moves the map — **15 flips** — because deleting a percent of world wealth renormalises `c_w` everywhere; the asymmetry is which node keeps its end, not whether the map moves. | MODEL | numerical test | REVISED | X132 |

## §2.9 — Build order (lines 979–989) · §3.1 — Goals (lines 994–1003)

**UNCHANGED:** C343–C352, C353–C365, V113, X138 (Goal 1's razed `hangzhou`). No delta claims.

## §3.2 — Why a flow and a drainage sweep (lines 1004–1112)

**UNCHANGED:** C366, C370–C375, C383–C385, V115, V116, V118–V122, V124, V128–V131, W120, W123,
W125–W128, X139, X146, X147, X148, X149. *(The "necessary, not sufficient" correction is Y017 at
first appearance in §1.1; the post-fold caution is Y092 at first appearance in §2.2a.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y109 | What the contrast-ratio metric cannot see is what the diagnosis rests on: **sparsity** — most nodes produce nothing of a given good (spices in 18 of 80 nodes, cloves in exactly one) — so `(c−s)/deg` is dominated by *where* supply exists, and a max/min ratio over producing nodes is blind to that by construction; on the contrast metric itself the demand side is the wider one. | MODEL | derivation | REVISED | X140, X141 |
| Y110 | Better wealth inputs move Genoa to a **co-sink at roughly ×1.7** without making demand the determinant of placement. | MODEL | numerical test | REVISED | X142 |
| Y111 | Moving the spice sink to a Chinese node takes a multiple of that node's demand in the region of **3.6–4.9×** — observed on the 1444 field: `beijing` 3.61×, `hangzhou` 4.12×, `xian` 4.60×, `canton` 4.77×. | MODEL | numerical test | REVISED | X143 |
| Y112 | The multiple a node needs and the share of world demand it then buys do not line up end to end, because the share depends on where the node started, and other nodes in the region need more still. | MODEL | derivation | REVISED | X144 |
| Y113 | The node indexing is load-bearing wherever the key ties, which is not only the fallback branch, and **none** of those sites is why §2.4 requires a canonical node order — that comes from Phase 2's degenerate LP. | MODEL | derivation | REVISED | X150, X151 |

## §3.3 — Why wealth, and why per province (lines 1113–1135)

**UNCHANGED:** C386–C406, C408, C412, C413, V132, V133, V135, W132–W139. No delta claims.

## §3.4 — Why supply is pre-modifier (lines 1136–1147)

**UNCHANGED:** C415–C423, V137, V139, W140, W141, W142.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y114 | In v1, substituting production income broke the α = 1 identity, with orientation agreement collapsing to **well under half the map** — the 159/159 → 68/159 figures are no longer carried. | MODEL | numerical test | REVISED | V138 |

## §3.5 — Why α is anchored absolutely (lines 1148–1189)

**UNCHANGED:** C427–C442, V140–V144, V147, X152, X153, X156, X157.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y115 | ⚑ **`change_price` values are fractions of the good's base price, not ducats**, settled by the shipped save `tutorial/eu4_tutorial_chapter10.eu4`: `paper` at `current_price = 4.375` on a base of 3.5 (× 1.25, not + 0.25) and `gems` at 5.000 on a base of 4.0 — so a −0.25 event takes a 2.5 good to 1.875, and grain and wine reach 0.625. | ENGINE | file value | NEW | — |
| Y116 | The install carries **161** textual `change_price` blocks — 93 in `events/`, 14 in `missions/`, 1 in `common/`, 53 in `history/` of which 13 are negative (all in `HAB - Austria.txt`) — and **none in `decisions/`**. | ENGINE | file value | REVISED | X154 |
| Y117 | ⚑ **Ten of the 161 never execute**: seven sit inside quoted `effect_tooltip = "…"` strings and three inside `tooltip = { }` display wrappers, so **151 are executable**. | ENGINE | file value | NEW | — |
| Y118 | Six of the seven quoted blocks duplicate a block already counted in `events/`, and the seventh names a price key no event in the install ever sets. | ENGINE | file value | NEW | — |
| Y119 | All ten non-executing blocks are positive and every negative block in the install is executable, so the sublinear-reachability partition is identical under either census. | MODEL | derivation | NEW | — |
| Y120 | v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them; both were wrong about which number was the executable one. | WORLD | derivation | REVISED | X155 |
| Y121 | v5.0's claim that the scan was "guarded by a per-file count assertion" was false — no assertion existed anywhere in its toolchain — and `verify6.py` now carries the guard. | WORLD | derivation | NEW | — |
| Y122 | The mechanical reason a plain parse misses those blocks: `pdx.py` tokenises a quoted string as one opaque unit, so a `change_price` inside a tooltip string is invisible to the walker. | WORLD | derivation | NEW | — |

## §3.6 — Why no hysteresis, and why there is no ε (lines 1190–1226)

**UNCHANGED:** C443–C446, C449, C452, V148, V152, V154, W147–W152. No delta claims.

## §3.7 — Why eligibility is per good (lines 1227–1234)

**UNCHANGED:** C463–C473. No delta claims.

## §3.8 — Why gates evaluate true (lines 1235–1254)

**UNCHANGED:** C474–C497, V155–V158, W154. *(The 90.2% any-good reachability census is Y060 at
first appearance in §1.6.)* No delta claims.

## §3.9 — Why `Φ_w` is the installed graph (lines 1255–1299)

**UNCHANGED:** C502, C505–C510, C512, V160–V162, V218, V221, V228, X161.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y123 | Rich non-sink nodes on the corrected field: `genua`, `gulf_of_siam` and `sevilla` rank 3rd, 2nd and 7th by node wealth at **296.0, 297.9 and 266.5** against `english_channel`'s 316.6, **which is a sink**. | MODEL | numerical test | REVISED | X159 |
| Y124 | `Φ_ord` scores **higher** than `Φ_w` on self-coherence — the undisputed cost of the trade — but its ends are scheduling artifacts, a majority terminate no good at all, none of the demand capitals is among them, and its end count does not concentrate as demand concentrates; no figure is maintained for it. | MODEL | derivation | REVISED | X160 |
| Y125 | v2.1–v4.0's "two vanilla-like ends at 1444" is **not** the adoption argument and should not be revived even though the 1444 field again gives two ends: the count is a property of the field, not of the operator, and pinning the operator to it would be the withdrawn calibration. | WORLD | derivation | REVISED | X162 |
| Y126 | What the trade costs is self-coherence with the per-good graphs and what it buys is one operator, one set of guarantees, and ends that sit where the wealth is — stated without a points figure. | DESIGN | stipulated | REVISED | X163 |

## §3.10 — Why the engine's economy is overwritten (lines 1300–1317)

**UNCHANGED:** C513–C521, C523–C525, C528–C530, X164, X165, X167.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y127 | The two income forms agree to a worst relative disagreement of **0 to 3.7e-16** — one to **three** units in the last place. | MODEL | numerical test | REVISED | X166 |
| Y128 | Propagation is **kept** on a single graph: reading the one installed graph leaves the propagated term good-independent and the identity survives it, at 0 to 3.7e-16 — one to three ULP, not the single ULP v5.0 claimed. | MODEL | numerical test | REVISED | X168 |
| Y129 | `gulf_of_siam`'s 29 goods leave it by **seven** distinct downstream sets. | MODEL | numerical test | REVISED | X169 |
| Y130 | Per-good propagation destroys the **exactness**: once downstream sets differ, a country's power at the node is no longer one number, `powershare_C` no longer factors out, and a single node scalar cannot reproduce every collector's income exactly — a claim about exactness, not about magnitude. | MODEL | derivation | REVISED | X170, X171 |
| Y131 | Substituting the share at one arbitrarily chosen reference commodity gives per-collector errors up to **+7.4%** at `sevilla`, and sweeping which commodity is chosen moves that collector's error across a **17.8-point** range — so those figures measure the arbitrary choice, not the design. | MODEL | numerical test | REVISED | X172 |
| Y132 | Substituting the quantity an implementation would actually store — the **value-weighted mean share** across the node's goods — keeps the error at **at most 0.1%** at every node measured (`sevilla`, `champagne`, `genua`, `malacca`, `gulf_of_siam`). | MODEL | numerical test | NEW | — |
| Y133 | The honest statement: per-good propagation costs the exact identity and buys a per-node error that a reasonable scalar keeps within a tenth of a percent, and the identity is what Goal 7 is stated in terms of. | DESIGN | derivation | NEW | — |
| Y134 | v1–v4.0's "off by 5.96 ducats on a node paying ~250" has no node with local trade value near 250 behind it — and the 112.6 figure v5.0 added is no longer carried. | WORLD | derivation | REVISED | X173 |
| Y135 | v4.0's 0.41% and v5.0's "redistributive and single-digit percent" were both artifacts of freezing the share at one commodity — v5.0 having correctly diagnosed that defect in v4.0 — and the construction behind any such figure has to be stated with it, which none of those documents did. | WORLD | derivation | REVISED | X174 |

## §3.11 — Caravan power · §3.12 — Treasure fleets (lines 1318–1355)

**UNCHANGED:** C531–C547, C556–C560, V163–V172. No delta claims.

## §3.13 — Open questions (lines 1356–1414)

**UNCHANGED:** C561–C585, V173–V175, V178, V181–V183, W164, X175, X177, X178, X179, X180, X183.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y136 | The one open wealth question is now a **design** question rather than a classification one — should any source beyond province condition multiply `goods_produced`? The two keys are granted in many places (buildings, event modifiers, great projects, static and province-triggered modifiers, holy orders, state edicts, trade-company investments); v3.0–v5.0 tried to admit the province-scoped subset by rule, that rule was wrong in every audit that examined it, and re-admitting any source re-admits the maintenance burden for 0.98% of world wealth. | DESIGN | derivation | REVISED | X176 |
| Y137 | Under the calibration's α = 16 the cloves demand order is `hangzhou`, `beijing`, `doab`, and the sink lands on a high-demand node rather than a geographic accident; v2's "Beijing holds the richest single province" is wrong — that is `hangzhou`. | MODEL | numerical test | REVISED | X181, X182 |

## §3.14 — AI merchant assignment (lines 1415–1433)

**UNCHANGED:** C586–C624, X184. No delta claims.

## §3.15 — Rejected (lines 1434–1545)

**UNCHANGED:** C625–C672 as carried by v2, V184–V188, V192–V199, V226, V227, V228.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y138 | With v1's ε floor removed the contrasts run **4–97 on supply against 211–15,010 on demand** over the **28** goods produced in more than one node, so the demand side is the wider one; `cloves` has a single producer and no contrast to measure. | MODEL | numerical test | REVISED | X185 |
| Y139 | v3.0 and v4.0 repeated the 10⁷ / 10²–10³ ratio in §3.15 while v4.0's own §3.2 was withdrawing it. | WORLD | derivation | REVISED | X186 |
| Y140 | Ranked orientation wins the sink–demand **alignment** statistics (a far higher share of top-demand nodes in its sink sets than DRAIN) and loses delivery — a sixth of world demand stranded, orphan sinks a good cannot reach, net-producer sinks where DRAIN, LAP and FLOW post none, several times DRAIN's sinks per good — all stated without figures. | MODEL | derivation | REVISED | X187, X188 |
| Y141 | Seeded basin growth leaves demand unserved at every tuning tried; the 88.4% reach figure is dropped. | MODEL | derivation | REVISED | X189 |
| Y142 | The 3-mass gravity field reproduces whatever end count it is seeded with while γ is small enough and loses that property as γ approaches 1; no figures are maintained, and the three rejection grounds are non-numeric — it pins the count by fiat, it needs a second operator with its own reach knob γ, and a pure `wealth^α` comparison with no reach term does not concentrate ends at all. | MODEL | derivation | REVISED | X190, X191 |

## §3.16 — Evidence standard (lines 1546–1607)

**UNCHANGED:** C677, C680–C682, C684, C685, V200–V203, V206–V210, W173–W181.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y143 | v1's ε instantiation failed the α = 1 identity at **the tolerance v1 used**; the 1e-5 figure is no longer carried. | MODEL | numerical test | REVISED | V204 |

---

# Withdrawn prior IDs — propositions v6.0 drops or reverses

Recorded for comparability with `claims-v5.md`'s answer (b). None of these has a v6.0 successor;
each is either deleted with the classifier or replaced by a scoped statement that asserts less.

| Group | IDs | What v6.0 does |
|---|---|---|
| The two-test classifier and its whole-install enumerations | X030, X031, X032, X034, X038, X039, X041, X042, X043, X044, X045, X046, X047, X048, X049, X050, X051, X052, X053, X054, X055, X056, X057, X058 | §1.3 deletes the rule and everything it governed, so the great projects, permanent province modifiers, centres of trade, buildings, `production_leader`, `bonus_from_merchant_republics`, terrain/climate and the Leviathan gate all leave the document. X033 and X035 are the two that keep a successor, in Y002 and Y021 |
| The one-sink field and its diagnosis | X003, X071 | the v6.0 field gives two sinks again, and the claim that v5.0's second sink vanished because the field was missing sixteen provinces is gone |
| The α_Φ band table's narrow window and its noise analysis | X082, X192, X193, X194, X195 | X077–X081 are replaced by one band figure (Y065) plus the [1, 8] scan (Y064); the 0.018-wide window, its 8-seed noise analysis and the edge-uncertainty principle are not carried at all |
| The Europe demonstration's other bullets | X092 (Lowlands ×1.20), X093 (±2% random noise against Europe-only) | dropped in favour of the four-row scaling table (Y070) and its snapshot caveat (Y071) |

# † Unresolvable IDs

**None.** Every `Replaces` target in this delta resolves to a specific C, V, W or X ID. Nine
targets live outside `claims-v5.md` and were resolved by grepping the older inventories:
**W023** (wealth is owner-agnostic), **W036** (both monthly figures are the annual value over
twelve, so the annual forms add directly), **W050** (unowned provinces are outside the model —
owner *and* `is_city = yes`), **W052** ("the single largest source of hidden owner-dependence"),
**W067** (the propagation tooltip qualifier is descriptively false and §1.9 "gains no qualifier"),
**W089** (both wealth coefficients are hardcoded in the binary), **W189** (coal's 10.0 is the
highest base price in vanilla), **V138** (orientation agreement collapsing 159/159 → 68/159) and
**V204** (the ε instantiation failing the identity at 1e-5).

The three † markers `claims-v5.md` carried — X130, X133 and X138 against the C298–C342 and
C353–C365 ranges — introduce no new unresolved range here: X130's proposition is revised as Y106,
and X133 and X138 are UNCHANGED.
