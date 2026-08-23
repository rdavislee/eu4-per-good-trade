# Claim Inventory Delta — Per-Good Trade Network Spec v6.0

Extracted from `per-good-trade-spec.md` (v6.0, 1,601 lines) as a **delta against
`../v5-owner-agnostic/claims-v5.md`** (X001–X196), which is itself a delta against
`../v3-owner-agnostic/claims-v3.md` (W001–W195), `../v2-drain/claims-v2.md` (V001–V230) and
`../v1-laplacian/claims.md` (C001–C685). Extraction only: nothing here is validated or corrected.

**Method.** The v6.0 spec was read in full, and `claims-v5.md` was read in full — header plus every
claim row. A line-level diff of the v5.0 and v6.0 spec texts was computed and read hunk by hunk
(55 hunks) so that every v6.0 proposition could be dated and every deleted v5.0 proposition
accounted for. `claims-v3.md`, `claims-v2.md` and `claims.md` were grepped to resolve the specific
prior IDs named in the `Replaces` column (W002, W023, W025, W036, W050, W052, W060, W062, W067,
W189, V138, V204, V215, V218, V225, V226). `changes-v6.md` was read for its method note and
replacement index and was used **only to locate changed passages** — no row below is sourced to it;
every row was read off the v6.0 spec text itself.

**ID prefix.** v1 used `C`, v2 used `V`, v3 used `W`, v4 got none, v5 used `X`. **v6 uses `Y`**,
numbered in document order.

**Statuses.** UNCHANGED — the same proposition as an existing C/V/W/X ID; the old ID is recorded and
no Y ID is issued. REVISED — the proposition changed; a new Y ID with the old ID(s) in `Replaces`.
NEW — no counterpart in any prior inventory. A proposition stated in two sections keeps one ID at
first appearance. Renaming a script (`v5measure.py` → `measure6.py`) or bumping a version number
inside otherwise identical prose is **not** a proposition change.

**Vocabularies carried over.** Type: ENGINE / MODEL / DESIGN / OUTCOME / WORLD. Provenance:
stipulated / derivation / file value / numerical test / engine test / prose source /
verified (method unstated) / UNSOURCED. `numerical test` (a solver experiment — `measure6.py`,
`europe.py`, `toys.py`) and `engine test` (an observation of EU4 actually running — a tooltip, a
save, a crash dump) are kept strictly distinct.

**Markers.** **⚑** a row introducing an engine fact no prior inventory carried. **§** a row whose
stated evidence is a single observation. **†** a `Replaces` target believed to exist but not pinned
to a specific ID.

---

# Summary

**157 delta claims extracted, Y001–Y157**, against v5's 196: **54 NEW, 103 REVISED**.

The REVISED rows replace **106 X IDs** plus **12 older IDs** (W002, W023, W025, W036, W050, W052,
W062†, W067, W189, V138, V204, V225†) — 118 distinct prior IDs. A further **63 X IDs are carried
UNCHANGED**, and **27 X IDs are withdrawn** — stated wrong, or deleted without replacement; see
"Stranded prior IDs". 63 + 27 + 106 = 196, so every v5 ID is accounted for.

### Delta claims by status and Type

| Type | NEW | REVISED | Total |
|---|---|---|---|
| MODEL | 19 | 67 | 86 |
| DESIGN | 12 | 18 | 30 |
| ENGINE | 12 | 10 | 22 |
| WORLD | 11 | 7 | 18 |
| OUTCOME | 0 | 1 | 1 |
| **Total** | **54** | **103** | **157** |

### Delta claims by Provenance

| Provenance | Count |
|---|---|
| numerical test | 58 |
| derivation | 57 |
| stipulated | 23 |
| file value | 14 |
| engine test | 5 |
| prose source | 0 |
| verified (method unstated) | 0 |
| UNSOURCED | 0 |
| **Total** | **157** |

No row in this delta carries UNSOURCED or `verified (method unstated)` provenance.

**Fifteen rows are marked ⚑** — engine facts no prior inventory carried; **ten of the fifteen are
NEW**, and ten of the fifteen sit in §1.3, where the three corrected start-state reads land
(Y028, Y029, Y033, Y038, Y041, Y043, Y045, Y046, Y047, Y049; the rest are Y090, Y125, Y127, Y128,
Y146). **Four rows are marked §** — evidence resting on a single observation: Y031, Y033, Y046,
Y114. **Two `Replaces` targets are marked †**: W062 (Y154) and V225 (Y156).

### Where the delta concentrates

| Section | Y rows | What drove it |
|---|---|---|
| §1.3 Demand | 35 | the classifier's deletion, the four province-state modifiers, three corrected start-state reads |
| §1.6 Aggregate graph | 32 | two sinks instead of one, α_Φ made stipulated, the Europe table, the Cape re-check |
| §0 Front matter | 12 | the new wealth rule and the two prose conventions (R2, R3) |
| §2.4 The tradenodes file | 11 | Phase 2's degenerate LP as the ground for a canonical node order |
| §3.10 Income factoring | 8 | the exactness/magnitude split and the value-weighted-mean-share measurement |
| §1.1 Trade direction | 7 | the post-peel balance, and the equality's conditions shown insufficient |
| §3.5 α anchoring | 7 | the `change_price` census reopened a third time — textual versus executable |
| §3.15 Rejected | 7 | every rejected-operator figure deleted under R3 |
| §1.10 · §2.2 | 6 each | the cooldown defines and the caravan share re-description; the new field and the timing retreat |
| §3.2 · §3.9 · §3.13 | 5 each | |
| §2.8 | 4 | regenerated razed-China and sink-decile rows |
| §1.5 | 2 | |
| §2.2a · §2.3 · §2.7 · §3.4 · §3.16 | 1 each | |

---

## §0 — Front matter (lines 1–41)

**UNCHANGED:** C002, C003, C004, V001 *(via §2.5)*, V002, V003, W001.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y001 | v6.0 keeps v3.0's owner-agnostic wealth and makes it **true by construction** rather than by a rule that has to be policed. | DESIGN | stipulated | REVISED | W002 |
| Y002 | v6.0's substantive change is to §1.3: **wealth is a function of the province's development, its trade good and its own current condition, and of nothing else.** | DESIGN | stipulated | REVISED | X002 |
| Y003 | The two-test modifier classifier and everything it governed — trade-good modifiers, great projects, permanent province modifiers, buildings, centres of trade, the DLC conditionality — are deleted, together with the whole-install sweep that maintained them. | DESIGN | stipulated | REVISED | X033, X035 |
| Y004 | On the 1444 start that deleted apparatus was worth **0.98%** of world wealth, over **87 of 2,472** provinces (`measure6.py`). | MODEL | numerical test | NEW | — |
| Y005 | What the apparatus cost was an input surface whose classification was wrong in **every audit that examined it**. | WORLD | derivation | REVISED | X034 |
| Y006 | Three start-state reads are corrected in the same pass: `on_startup` devastation, dated `add_base_*` accumulation, and the `is_city` filter the engine does not apply. | WORLD | derivation | NEW | — |
| Y007 | A canonical node order is a correctness requirement because **Phase 2's min-cost flow is degenerate, so presentation order selects which optimum is returned** (worked at §2.4 item 1). | MODEL | numerical test | REVISED | X125 |
| Y008 | Prose convention **R2 — no empirical absolutes**: no superlative, no universal quantifier and no threshold asserted as a fact about the world; every claim is either a directional design statement or an observation scoped to the field and script that produced it. | DESIGN | stipulated | NEW | — |
| Y009 | Prose convention **R3 — no maintained figures for any rejected operator**: §3.15 keeps its design arguments and loses its measurements, covering `Φ_ord`, the gravity kernels, the v1 Laplacian, RANK and the seeded basins. | DESIGN | stipulated | NEW | — |
| Y010 | Those rejected-operator numbers were re-measured and re-refuted in three successive audits, and not one of the rejection arguments depends on them. | WORLD | derivation | NEW | — |
| Y011 | Every graded claim from `../v5-owner-agnostic/validation-v5.md` — **22 refuted, 39 partial, 1 unverifiable** — is folded through, `fixes-agreed.md` maps each to the change that answers it, and deleted text is quoted in `changes-v6.md`. | WORLD | file value | REVISED | X001 |
| Y012 | Measured figures carry the script that produced them, and `scripts/verify6.py` re-derives each one **from the document text** and fails if the two disagree. | DESIGN | stipulated | REVISED | X004 |

## §1.1 — Trade direction (lines 45–150)

**UNCHANGED:** C005, C006, C010–C012, C019–C022, V005–V015, V017–V024, V026–V028, V031, V032,
V036, V037, W007–W011, W015–W022, X005, X006, X007, X012, X014, X015, X016, X017.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y013 | The fallback branch fires only when every candidate is support-isolated with zero **post-peel** balance. | MODEL | derivation | REVISED | X008 |
| Y014 | The balance the priority key reads is the one Phase 0 hands on, each pendant's balance folded into its parent — not the raw input `b` — so the condition is about the folded field, and a map with non-zero raw balances can still reach the branch. | MODEL | derivation | NEW | — |
| Y015 | On a connected core the branch needs the folded balance to vanish across the core: for a per-good graph a component with no producer and no consumer; for the aggregate graph, every node's `Σ wealth^α_Φ` equal — which uniform *wealth* gives but is not the same condition. | MODEL | derivation | REVISED | X009 |
| Y016 | Where the wealth key then ties, the **node index decides**, which is why §2.8 asserts containment over a set that includes the fallbacks. | MODEL | derivation | REVISED | X010 |
| Y017 | That tie is **not** the reason §2.4 requires a canonical node order; that requirement is stronger and is set by Phase 2. | MODEL | derivation | REVISED | X011, X151 |
| Y018 | On 1444 the fallback and pendant cases are empty and the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods, **1–8 sinks per good, mean 3.52**, zero fallbacks. | MODEL | numerical test | REVISED | X013 |
| Y019 | That equality is a measurement on this input, not a theorem, and it **does not become one by attaching conditions**: "Phase 0 a no-op and no fallback firing" looks sufficient and is not — **T2** satisfies both and still breaks it. | MODEL | derivation | REVISED | X013, X145 |

## §1.2 — Supply (lines 152–163)

**UNCHANGED:** C023, C025–C028, V038–V041. No delta claims.

## §1.3 — Demand (lines 165–290)

**UNCHANGED:** C031, C032, C033, C035, C036, C039, W024, W026, W030, W031, W032, W033, W042, W043,
W044, W047, W051, X023, X024, X025, X026, X059, X060, X061, X062.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y020 | Wealth is owner-agnostic **and reads three things about the province**: its development, its trade good, and its own current condition. | MODEL | stipulated | REVISED | W023 |
| Y021 | Two provinces with the same **development, trade good and condition** have the same wealth whoever owns them — terrain drops out of the list. | MODEL | derivation | REVISED | W025 |
| Y022 | Owner-agnosticism is true by construction, not by a policed rule: `base_tax`, `base_production` and the trade good are bare attributes of the place, so nothing about them needs classifying. | MODEL | derivation | NEW | — |
| Y023 | v3.0 through v5.0 stated the property and then defended it with a two-test classifier over a sweep of the install — a large surface to keep correct, and wrong in every audit that examined it. | WORLD | derivation | NEW | — |
| Y024 | What the deletion gives up: `gems`' `local_tax_modifier` and `incense`' `trade_value_modifier` are genuinely province-scoped and are no longer read, along with great projects, permanent province modifiers and the DLC state they depended on. | DESIGN | derivation | REVISED | X035, X036, X037, X038, X039, X057 |
| Y025 | `goods_produced(p) = GP_COEFF · base_production(p) · (1 + Σ province-state goods modifiers)` — the flat-goods-bonus term is gone from the formula. | MODEL | derivation | REVISED | X018 |
| Y026 | `trade_value(p) = goods_produced(p) · price(good(p))`, ducats per year — **no trade-value modifier term**. | MODEL | derivation | REVISED | X019 |
| Y027 | `tax_value(p) = TAX_COEFF · base_tax(p) · (1 + Σ province-state tax modifiers)`. | MODEL | derivation | REVISED | X020 |
| Y028 | ⚑ The tax tooltip's schema is `Base: trunc(base_tax / 12) (Yearly base_tax)` — observed `Base: 0.49 (Yearly 6.00)` at `base_tax` 6 and `Base: 0.16 (Yearly 2.00)` at `base_tax` 2. | ENGINE | engine test | REVISED | X021 |
| Y029 | ⚑ The parenthetical is `base_tax` itself and the `Base` line is its truncated twelfth; it is **not** twelve times the displayed figure, which would give 5.88 and 1.92. | ENGINE | derivation | NEW | — |
| Y030 | v3.0 through v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both of its own data points. | WORLD | derivation | NEW | — |
| Y031 | § The monthly production tooltip's `Trade Value` line is only **consistent with** the same relation, on one observation (3.52 → +0.29), which fixes the divisor to within **[12.00, 12.14]**. | ENGINE | engine test | REVISED | X022 |
| Y032 | Both monthly figures being the annual value over twelve is what lets the annual forms add directly, and **the tax pair establishes it at two development levels**. | MODEL | derivation | REVISED | W036 |
| Y033 | ⚑§ Garnatah at `base_tax` 6 with `Tax Income Efficiency 125.0%` displays `Base 0.49` then `0.62`; 0.49 × 1.25 = 0.6125 truncates to 0.61, so the engine multiplies the **untruncated** monthly value (0.49999… × 1.25 = 0.62499…, displayed 0.62). | ENGINE | engine test | REVISED | X027 |
| Y034 | The example establishes only the ordering — base from development first, percentage second — and nothing finer. | MODEL | derivation | NEW | — |
| Y035 | v3.0 through v5.0 read the same figures as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires rounding while §2.3 requires truncation; both cannot hold. | WORLD | derivation | NEW | — |
| Y036 | Flat goods bonuses **would** add into `goods_produced` before the price multiply, but under §1.3 no source grants one, so the ordering is stated for the emitter's benefit and is exercised by no province in the model. | MODEL | derivation | REVISED | X028 |
| Y037 | **Province condition is the only thing besides development and the trade good that wealth reads**: four static modifiers, all read from `common/static_modifiers/00_static_modifiers.txt`. | DESIGN | stipulated | REVISED | X030, X031 |
| Y038 | ⚑ The four are `devastation` (`trade_goods_size_modifier = -2`, scaled by the devastation level), `prosperity` (+0.25), `under_siege` (−0.25) and `occupied` (−0.5 **and** `local_tax_modifier = -0.5`). | ENGINE | file value | REVISED | X040 |
| Y039 | Only `occupied` touches the tax term; the other three reach `goods_produced` alone. | MODEL | derivation | NEW | — |
| Y040 | These four are what make the map answer to war: §1.2's volatility, §3.3's besieged province and §2.8's war rows all rest on them. | DESIGN | derivation | NEW | — |
| Y041 | ⚑ They are **not all quiet at the 1444 start**: eleven counted provinces begin devastated — Bohemia at 50, Erzgebirge and Moravia at 20 — and no province-history file says so; the devastation is applied by `on_startup`, which fires `flavor_boh.15` ("The Aftermath of the Hussite Wars"). | ENGINE | file value | REVISED | X040 |
| Y042 | That start devastation costs **13.40 ducats** across the eleven affected counted provinces (`measure6.py`). | MODEL | numerical test | NEW | — |
| Y043 | ⚑ The chain is `common/on_actions/00_on_actions.txt` → `on_startup_effect` → `common/scripted_effects/01_scripted_effects_for_on_actions.txt` → `country_event flavor_boh.15`. | ENGINE | file value | NEW | — |
| Y044 | **The start state is what the engine produces, not what the history files say** — the general form of the point, and it costs three separate reads. | DESIGN | stipulated | NEW | — |
| Y045 | ⚑ `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`, `flavor_geo.1` and others, and `flavor_geo.1` carries `add_base_tax`, `add_base_production` **and** `add_devastation` — so development itself can move before the first tick. | ENGINE | file value | NEW | — |
| Y046 | ⚑§ `add_base_*` in a dated block before the start date **accumulates**: province 1 (Uppland) has `base_tax = 5` undated plus 1 at `1436.4.28` and the game has 6, where v5.0 and earlier overwrote and silently dropped the grant. | ENGINE | engine test | NEW | — |
| Y047 | ⚑ `is_city = yes` **is not a filter the engine applies**: 20 owned provinces omit or comment out the line — province 265 among them — and the engine treats them as cities. | ENGINE | file value | NEW | — |
| Y048 | The model counts a province when it has an owner and lies in a trade node: **2,472** provinces, not 2,452. | DESIGN | numerical test | REVISED | W050, X063 |
| Y049 | ⚑ **Twenty counted provinces have no trade good in their history file** (`trade_goods = unknown`); the engine assigns one at start from each good's `chance = { }` block. | ENGINE | file value | NEW | — |
| Y050 | The wealth field is therefore partly the result of one random draw, and the model does not try to predict it — it reads whatever the game's current state holds, as it does for development. | DESIGN | stipulated | NEW | — |
| Y051 | The model applies the cored-city reference condition to **every province it counts**: ownership is not modelled, so every province is treated as cored and settled. | MODEL | derivation | REVISED | X063 |
| Y052 | That is a modelling choice with a known cost: two readings, both on cored city provinces at `base_tax` 2 and 6, are all `TAX_COEFF = 1.0` rests on, and the development range runs past 50. | WORLD | derivation | NEW | — |
| Y053 | Unowned provinces are outside the model: `s` and `c` are computed over provinces that **have an owner and lie in a trade node**, no longer "with an owner and `is_city = yes`". | MODEL | stipulated | REVISED | W050 |
| Y054 | Owner-agnostic wealth removes **a large** source of hidden owner-dependence from the aggregate graph — v3.0–v5.0's "the single largest source" narrowed. | MODEL | derivation | REVISED | W052 |

## §1.4 — Market concentration (lines 292–306)

**UNCHANGED:** C040–C047. No delta claims.

## §1.5 — Goods without a graph (lines 308–355)

**UNCHANGED:** C048, C051–C056, V050–V058, W053, W182–W186, W188, W191.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y055 | Measured: repricing to coal the **45** owned latent-coal provinces flips **13 of 159 `Φ_w` edges** and adds **217 ducats** to world wealth (`measure6.py`). | MODEL | numerical test | REVISED | X064 |
| Y056 | Coal's base price of 10.0 is the highest **in the shipped price table** (`common/prices/00_prices.txt`, `measure6.py`) — v3.0–v5.0's "highest in vanilla" narrowed. | ENGINE | file value | REVISED | W189 |

## §1.6 — The aggregate graph (lines 357–478)

**UNCHANGED:** C059, C062, V063, V064, V212, V218, V221, W054, W055, W058, W063, W064, X067, X089,
X090, X091, X123.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y057 | **Both the count and the locations of `Φ_w`'s sinks move with the wealth field, and `α_Φ` sets how sharply concentration is read** — the count is a function of the field *and* the constant. | MODEL | derivation | REVISED | X065 |
| Y058 | At the stipulated α_Φ = 1.5 the 1444 field gives two sinks and a modestly grown Europe gives three or one, so neither the count nor the placement is fixed by the constant. | MODEL | numerical test | NEW | — |
| Y059 | v2.0–v4.0 said the count "emerges from concentration" and v5.0 over-corrected to "the count is set by `α_Φ`"; both are wrong in the same way, and only the locations are emergent. | WORLD | derivation | NEW | — |
| Y060 | v2.1 chose α_Φ with a target count in view — a calibration §2.3 withdraws **without replacing**, since α_Φ is stipulated rather than derived. | WORLD | derivation | REVISED | X066 |
| Y061 | Scale: identical orientation at ×1 and above, **12 edge flips at ×10⁻²**, **100 at ×10⁻⁶**. | MODEL | numerical test | REVISED | X068 |
| Y062 | 1444's `b_w` has largest magnitude **0.0226**. | MODEL | numerical test | REVISED | X069 |
| Y063 | Measured at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and `hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12. | MODEL | numerical test | REVISED | X070 |
| Y064 | Phase 1 selects `genua`; both sinks arrive by stall promotion and `genua` ends a transit node, so there are **2 promotions and 0 fallbacks**. | MODEL | numerical test | REVISED | X072 |
| Y065 | **Eight sources**, all in the bottom half of the wealth field, `c_w` ranks **44–75**, mean degree **3.1** against the map's 4.0. | MODEL | numerical test | REVISED | X073 |
| Y066 | Every node drains to a sink; acyclic, 159/159 oriented; the sink set is unchanged under ±1% wealth noise **on three seeds**. | MODEL | numerical test | REVISED | X074 |
| Y067 | **90.2%** of ordered node pairs (5,703 of 6,320) are connected by at least one good's directed path on the 1444 field. | MODEL | numerical test | REVISED | X158 |
| Y068 | Agreement with the per-good graphs is **53.5%** of edge-goods and **52.1%** value-weighted. | MODEL | numerical test | REVISED | X075 |
| Y069 | The superseded marking-order aggregate **scored higher** on that measure; no figure is maintained for an operator the model does not install. | DESIGN | stipulated | REVISED | X076 |
| Y070 | `α_Φ = 1.5` is a **stipulated design constant exactly as `P₀ = 2.0` is** — superlinear, round, chosen rather than derived — and the document no longer offers a derivation. | DESIGN | stipulated | REVISED | X083 |
| Y071 | Scanned over [1, 8] rather than [1, 3] the widest sink-count band is **1.70** wide ([3.51, 5.21], `{doab, genua, hangzhou}`), so v5.0's widest-band ground depended on where the scan was truncated and 1.5's band is not the widest by any margin. | MODEL | numerical test | REVISED | X078, X082, X192, X193, X194, X195 |
| Y072 | Across α_Φ = 1.00…8.00 at 0.01 the sink set is a step function and 1.5 sits in the band **[1.38, 1.63], width 0.25**, which gives `{english_channel, hangzhou}`. | MODEL | numerical test | REVISED | X077, X081 |
| Y073 | Sampled at the six values v2 used the count is non-monotone: **6 → 2 → 1 → 2 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}. | MODEL | numerical test | REVISED | X084 |
| Y074 | A written warning against re-deriving 1.5 from the resemblance between the 1444 map's two ends and vanilla's three — that is the calibration §2.3 withdrew, and the mistake has been made twice. | DESIGN | stipulated | NEW | — |
| Y075 | **Europe becomes the centre of trade as it develops** — the design claim §3.1's first goal asks the field to deliver: the Channel's basin grows, Asia's pole fades, and past a broad range of European growth Asia holds no end at all. | DESIGN | derivation | REVISED | X085, X088 |
| Y076 | The mechanism carries it: wealth is linear in development, so developing a region moves its `c_w` share directly and `Φ_w`'s ends follow the wealth. | MODEL | derivation | NEW | — |
| Y077 | Europe table (`europe.py`, **824** counted European provinces, α_Φ = 1.5): ×1.00 → `{english_channel, hangzhou}`; ×1.02 adds `wien`; ×1.56 → `{english_channel, rheinland}` with Asia holding none; ×2.00 → `genua` alone. | MODEL | numerical test | REVISED | X086, X087 |
| Y078 | Those rows are properties of one snapshot under one scaling, not constants of the model. | DESIGN | stipulated | NEW | — |
| Y079 | Under the v6.0 wealth model **scaling development and scaling wealth are the same operation** — maximum difference 0.0 across the European set — so the distinction that made v5.0's version of the table wrong does not arise. | MODEL | numerical test | NEW | — |
| Y080 | The 1444 Silk Road route from Genoa to the Asian sink is `genua → alexandria → aleppo → persia → lahore → lhasa → ganges_delta → burma → gulf_of_siam → canton → hangzhou`. | MODEL | numerical test | REVISED | X094 |
| Y081 | From the north the route is the Volga and from the Channel the Hansa and the Danube — named without node chains. | MODEL | numerical test | REVISED | X095, X096 |
| Y082 | **No Europe→sink route passes the Cape of Good Hope**, checked from `genua`, `north_sea` and `english_channel`. | OUTCOME | numerical test | REVISED | X097 |
| Y083 | The Cape is a live conduit, not idle: in-degree 1, out-degree 3, with **132 ordered node pairs** whose path runs through it (`measure6.py`). | MODEL | numerical test | NEW | — |
| Y084 | v5.0's "nothing routes through the Cape" is false as a universal and was only ever checked on the Europe→sink routes. | WORLD | derivation | NEW | — |
| Y085 | In the per-good graphs the Cape also carries Asian spices to Europe; `Φ_w` models power, not cargo — the node chain no longer given. | MODEL | numerical test | REVISED | X098 |
| Y086 | Scaling the 22 European **nodes** makes `genua` the sole sink from about **×1.65**, and the 18-node western/central subset needs about **×2.15**. | MODEL | numerical test | REVISED | X099 |
| Y087 | Somewhere inside roughly **×2.9–×3.5** the Cape reverses — Atlantic→Cape→Indian-Ocean becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast — bounded above as well as below, so a window and not a threshold, with edges that move with the field. | MODEL | numerical test | REVISED | X100 |
| Y088 | Dev-stacking a single node's top province concentrates the map on that node; extra sinks at intermediate boosts are expected behaviour, not noise — the ×10/×20/×30/×50 figures dropped. | MODEL | derivation | REVISED | X101 |

## §1.7 — Merchants (lines 480–506)

**UNCHANGED:** C067–C083, V066, V068–V070, W065, W192, X102. No delta claims.

## §1.8 — Collection and transfer (lines 508–538)

**UNCHANGED:** C084–C102, V072, X103, X104. No delta claims.

## §1.9 — Trade power propagation (lines 540–549)

**UNCHANGED:** C103–C111, V073, W068, W069. No delta claims. *(W067's revision lands in §2.7 —
see Y114.)*

## §1.10 — Direction-dependent systems (lines 551–580)

**UNCHANGED:** C112–C143, V074, V078–V080, W070, W071, X105, X109, X110, X196.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y089 | **Banding absorbs very little chatter** — v5.0's "almost nothing absorbs threshold chatter" narrowed: a share oscillating across any single-valued limit flickers the mechanic, including Propagate Religion for the flagless countries its default and terminal branches cover. | ENGINE | derivation | REVISED | X106 |
| Y090 | ⚑ **Banding is not the only damper:** three shipped defines rate-limit the mechanics carrying these thresholds — `TRADING_POLICY_COOLDOWN_MONTHS = 12` (both banded policies), `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` and `TRADE_COMPANY_COOLDOWN = 60` — so a flickering share does not translate into a flickering *effect* at those three. | ENGINE | file value | NEW | — |
| Y091 | What is left exposed is everything without a cooldown, which is most of the ladder. | ENGINE | derivation | NEW | — |
| Y092 | Measured on the 1444 start: the caravan cap of 50 is **9.4% to 47.0% of an inland node's total trade power**, median **21.9%** over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. | MODEL | numerical test | REVISED | X107 |
| Y093 | As a share of the node's total **after** the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, median 17.9%; v5.0 quoted those under the first description, which cannot be right since 8.6% of 532.0 is 45.8 rather than 50. | WORLD | derivation | NEW | — |
| Y094 | On §2.2's derived 25-node inland basis only the median moves, to **21.3%**. | MODEL | numerical test | REVISED | X108 |

## §1.11 — Treasure fleets · §1.12 — What the game displays (lines 582–640)

**UNCHANGED:** C144–C148, C149–C165, V049, V065, V081. No delta claims.

## §2.1 — Shape (lines 646–664)

**UNCHANGED:** C167–C184, V082–V085, W072, W073. No delta claims.

## §2.2 — Solver (lines 666–706)

**UNCHANGED:** C185–C209, V064, V091, V092, V229, W075, W076, X115.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y095 | Solver item 4 computes `TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production · (1 + province-state goods modifiers) · price`, with no autonomy, efficiency, ideas or owner terms. | DESIGN | stipulated | REVISED | X111 |
| Y096 | The only modifiers the solver reads are the four describing the province's own condition, and at 1444 only `devastation` is live — on eleven provinces. | DESIGN | stipulated | REVISED | X112 |
| Y097 | `GP_COEFF` is **read from** `common/static_modifiers/00_static_modifiers.txt` rather than hardcoded. | DESIGN | stipulated | NEW | — |
| Y098 | World wealth is **10,594.70** annual ducats over **2,472** counted provinces. | MODEL | numerical test | REVISED | X113 |
| Y099 | Measured on the reference implementation: **of order 0.1 s for all 29 goods and single-digit milliseconds per good on average** — repeated runs span roughly 0.09–0.27 s and 3–7 ms, individual goods reaching about 20 ms, so a two-significant-figure range describes a machine and a scheduler and none is quoted. | MODEL | numerical test | REVISED | X114 |
| Y100 | v5.0 quoted "0.17–0.21 s"; twelve fresh runs put only one inside that interval. | WORLD | numerical test | NEW | — |

## §2.2a — What map this is for (lines 708–748)

**UNCHANGED:** W077–W085, W088, X116.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y101 | Where Phase 0 acts, free-edge determinism keeps its determinism half but **loses** the index-independence half: the key reads the post-fold balance β, so peeling can create exact ties the raw balances do not have, and the 1444 measurement does not transfer. | MODEL | derivation | REVISED | X117 |

## §2.3 — Constants (lines 750–796)

**UNCHANGED:** C211–C227, V094, W089, W090, W091, W097, W098, X118, X119, X120, X121, X123, and
the DLC-third-axis claim.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y102 | `α_Φ = 1.5` is recorded as a **stipulated** constant like `P₀`, and **every derivation previously offered for it is withdrawn** — v2.1–v4.0's two-sink calibration and v5.0's widest-band ground alike, neither being a reason. | DESIGN | stipulated | REVISED | X122 |

## §2.4 — The tradenodes file (lines 798–864)

**UNCHANGED:** C228–C233, C235–C242, V095, V148, W099, W100, W102–W107, W114, X124, X127.
*(The node-order/Phase-2 proposition itself is Y007, at first appearance in §0.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y103 | The min-cost b-flow is **massively degenerate**: many distinct supports carry the same optimal cost, and which one the solver returns depends on the order the nodes and arcs are presented in. | MODEL | numerical test | NEW | — |
| Y104 | Measured on 1444: relabelling the nodes and running end-to-end changed the orientation on **580 of 580** runs (29 goods × 20 relabellings), **always** by returning a different optimal vertex and never by a sweep tiebreak, with a mean of **22.1 of 159 edges** moving and the objective identical to 8.9e-16. | MODEL | numerical test | NEW | — |
| Y105 | Permuting only the arc presentation order with node labels held fixed changes the optimal support on **10 of 10 goods** tested, objective gaps ≤ 1.8e-15. | MODEL | numerical test | NEW | — |
| Y106 | Twenty-two flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event. | MODEL | derivation | NEW | — |
| Y107 | The canonical order must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks ties in, and it must stay stable across rebuilds. | DESIGN | derivation | REVISED | X125 |
| Y108 | Everything §1.6 and §2.8 report about stability is measured **at fixed node order**; re-order the same world and the map moves with `α_Φ` and every input held fixed. | MODEL | derivation | NEW | — |
| Y109 | The 580/580 result is HiGHS-specific in its detail but not in kind — any simplex returns *a* vertex of a degenerate optimal face. | MODEL | derivation | NEW | — |
| Y110 | Making the orientation independent of presentation order would need a tie-breaking objective (a lexicographic secondary cost, or a strictly convex perturbation); that is a design change and is not adopted here. | DESIGN | stipulated | NEW | — |
| Y111 | The priority key ties in more places than §1.1 documents: besides the free-edge sweep it decides Phase 1's within-cluster argmin, the stall promotion's identical form, and the top-k cut when two clusters carry equal mass. | MODEL | derivation | NEW | — |
| Y112 | None of those tie sites fires on 1444 — zero exact `(DEF, β)` ties on free edges across 29/29 goods, zero within-cluster β ties, zero tied cluster masses — so no measured figure here depends on them. | MODEL | numerical test | NEW | — |
| Y113 | End flags: 1444 has **two** end nodes, `english_channel` and `hangzhou`, against vanilla's three. | DESIGN | numerical test | REVISED | X126 |

## §2.5 — Runtime attachment · §2.6 — Writing to the engine (lines 866–898)

**UNCHANGED:** C243–C250, C251–C272. No delta claims.

## §2.7 — Probes (lines 900–930)

**UNCHANGED:** C274–C293, V098–V101, W108–W114.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y114 | § Probe 15 makes §1.9's "every immediately upstream node" **consistent with** the observation rather than confirmed by it — one observation on one node, enough to retire the cautionary case and not enough to promote the rule to a measurement. | ENGINE | engine test | REVISED | W067 |

## §2.8 — Validation (lines 932–976)

**UNCHANGED:** C298–C342, V109–V112, W116, W117, W119, W195, X128, X133, X134, X135, X136, X137.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y115 | Most goods, 1444: **1 to 8** sinks per good; high-demand nodes are sinks at **16.8%** in the top demand decile against 6.9% in the bottom. | MODEL | numerical test | REVISED | X129 |
| Y116 | Razed China: zeroing `hangzhou`-node development moves the `Φ_w` sinks from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`, **23 of 159** edges flipping. | MODEL | numerical test | REVISED | X130 |
| Y117 | `hangzhou`, not `beijing`, is China's wealth pole: node wealth **226.7 against 143.0**, and it holds the richest single province **the model counts**. | MODEL | numerical test | REVISED | X131 |
| Y118 | Zeroing `beijing` also moves the map — **15 flips** — because deleting a percent of world wealth renormalises `c_w` everywhere; the asymmetry is which node keeps its end, not whether the map moves. | MODEL | numerical test | REVISED | X132 |

## §2.9 — Build order (lines 978–984) · §3.1 — Goals (lines 990–998)

**UNCHANGED:** C343–C352, C353–C365, V113, X138. No delta claims.

## §3.2 — Why a flow and a drainage sweep (lines 1000–1102)

**UNCHANGED:** C366, C370–C375, C383–C385, V115, V116, V118–V122, V124, V128–V131, W120, W123,
W125–W128, X146, X147, X148, X149, X150.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y119 | **What the ratio metric cannot see is the thing the diagnosis rests on:** sparsity — most nodes produce nothing at all of a given good (spices in 18 of 80 nodes, cloves in exactly one) — so `(c−s)/deg` is dominated by *where* supply exists, and a max/min ratio over producing nodes is blind to that by construction. | MODEL | derivation | REVISED | X139, X141 |
| Y120 | On the contrast metric itself the demand side is the wider one, not the supply side — the ratio figures now live only in §3.15. | MODEL | numerical test | REVISED | X140 |
| Y121 | Better wealth inputs move Genoa to a **co-**sink at roughly ×1.7 without making demand the determinant of placement (v5.0's ×1.720 rounded away). | MODEL | numerical test | REVISED | X142 |
| Y122 | Moving the spice sink to a Chinese node takes a demand multiple in the region of **3.6–4.9×**, observed on the 1444 field: `beijing` 3.61×, `hangzhou` 4.12×, `xian` 4.60×, `canton` 4.77×. | MODEL | numerical test | REVISED | X143 |
| Y123 | The multiple a node needs and the share of world demand it then buys do not line up end to end, because the share depends on where the node started; other nodes in the region need more still. The per-node demand shares and the `girin`/`yumen`/`chengdu`/`lhasa` multiples are dropped. | MODEL | derivation | REVISED | X144 |

## §3.3 — Why wealth, and why per province (lines 1104–1114)

**UNCHANGED:** C386–C406, C408, C412, C413, V132, V133, V135, W132–W139. No delta claims.

## §3.4 — Why supply is pre-modifier (lines 1116–1126)

**UNCHANGED:** C415–C423, V137, V139, W140, W141, W142.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y124 | In v1 substituting production income broke the α = 1 identity, with orientation agreement collapsing **to well under half the map** — the 159/159 → 68/159 figure is withdrawn. | MODEL | numerical test | REVISED | V138 |

## §3.5 — Why α is anchored absolutely (lines 1128–1180)

**UNCHANGED:** C427–C442, V140–V144, V147, X152, X153, X156, X157.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y125 | ⚑ **`change_price` values are fractions of the good's base price, not ducats** — settled by the shipped save `tutorial/eu4_tutorial_chapter10.eu4`, where `paper` sits at `current_price=4.375` on a base of 3.5 (×1.25, not +0.25) and `gems` at 5.000 on a base of 4.0. | ENGINE | file value | NEW | — |
| Y126 | The install carries **161 textual** `change_price` blocks — 93 in `events/`, 14 in `missions/`, 1 in `common/`, 53 in `history/` of which 13 are negative (all in `history/countries/HAB - Austria.txt`), and **none in `decisions/`**. | ENGINE | file value | REVISED | X154 |
| Y127 | ⚑ **Ten of the 161 never execute** — seven inside quoted `effect_tooltip = "…"` strings and three inside `tooltip = { }` display wrappers — so **151 are executable**. | ENGINE | file value | NEW | — |
| Y128 | ⚑ Six of the seven quoted blocks duplicate a block already counted in `events/`, and the seventh names a price key no event in the install ever sets. | ENGINE | file value | NEW | — |
| Y129 | All ten are positive and every negative block in the install is executable, so the goods partition (13 sublinear-reachable / 2 on the boundary / 4 negative-but-short / 11 with no negative event) is identical under either census. | ENGINE | derivation | NEW | — |
| Y130 | v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them; both were wrong about which number was the executable one, and v5.0's claimed "per-file count assertion" existed nowhere in its toolchain. | WORLD | derivation | REVISED | X155 |
| Y131 | The mechanical reason a plain parse misses them: `pdx.py` tokenises a quoted string as one opaque unit, so a `change_price` inside a tooltip string is invisible to the walker. | WORLD | derivation | NEW | — |

## §3.6 — Why no hysteresis, and why there is no ε (lines 1182–1216)

**UNCHANGED:** C443–C446, C449, C452, V148, V152, V154, W147–W152. No delta claims.

## §3.7 — Why eligibility is per good (lines 1218–1224)

**UNCHANGED:** C463–C473. No delta claims.

## §3.8 — Why gates evaluate true (lines 1226–1248)

**UNCHANGED:** C474–C497, V155–V158, W154. No delta claims.
*(The 90.2% any-good connectivity figure is Y067, at first appearance in §1.6.)*

## §3.9 — Why `Φ_w` is the installed graph (lines 1250–1290)

**UNCHANGED:** C502, C505–C510, C512, V160, V161, V162, V218, V221, V228, X161.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y132 | The rich non-sinks `genua`, `gulf_of_siam` and `sevilla` rank 3rd, 2nd and 7th by node wealth at **296.0, 297.9 and 266.5** against `english_channel`'s 316.6, **which is a sink**. | MODEL | numerical test | REVISED | X159 |
| Y133 | `Φ_ord` **scores higher than `Φ_w` on self-coherence** — the acknowledged cost of the trade — but its ends are scheduling artifacts, a majority terminate no good, none of the demand capitals is among them, and its end count does not concentrate as demand concentrates. **No figure is maintained for it.** | MODEL | derivation | REVISED | X160, X076 |
| Y134 | It is not the installed operator, its numbers moved with every change to the wealth field, and three successive audits spent their effort recounting them; the design argument does not depend on any of them. | DESIGN | derivation | NEW | — |
| Y135 | v2.1–v4.0's "two vanilla-like ends at 1444" adoption argument **is not the argument and should not be revived even though the 1444 field again gives two ends**: the count is a property of the field, not of the operator, and pinning the operator to it would be the withdrawn calibration. | WORLD | derivation | REVISED | X162 |
| Y136 | What the trade costs is self-coherence with the per-good graphs, which the marking-order aggregate scores higher on; what it buys is one operator, one set of guarantees, and ends that sit where the wealth is — the 7.8-point figure dropped. | DESIGN | stipulated | REVISED | X163 |

## §3.10 — Why the engine's economy is overwritten (lines 1292–1310)

**UNCHANGED:** C513–C521, C523–C525, C528–C530, X164, X165, X167.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y137 | The two forms agree to a worst relative disagreement of **0 to 3.7e-16** — **one to three** units in the last place. | MODEL | numerical test | REVISED | X166 |
| Y138 | Reading the one installed graph leaves the propagated term good-independent, so the identity survives untouched at 0 to 3.7e-16 — one to three ULP, **not the single ULP v5.0 claimed**. | MODEL | numerical test | REVISED | X168 |
| Y139 | `gulf_of_siam`'s 29 goods leave it by **seven** distinct downstream sets. | MODEL | numerical test | REVISED | X169 |
| Y140 | Once the downstream sets differ, a country's power at the node is no longer one number and `powershare_C` no longer factors out, so a single node scalar cannot reproduce every collector's income exactly — **the claim is about exactness, not magnitude**. | MODEL | derivation | REVISED | X170 |
| Y141 | Substituting the share at one arbitrarily chosen reference commodity gives per-collector errors up to **+7.4%** at `sevilla`, and sweeping which commodity is chosen moves that same collector's error across a **17.8-point** range — so those figures measure the arbitrary choice, not the design. | MODEL | numerical test | REVISED | X170, X172 |
| Y142 | Substituting the quantity an implementation would actually store — the **value-weighted mean share** across the node's goods — the error is **at most 0.1%** at every node measured (`sevilla`, `champagne`, `genua`, `malacca`, `gulf_of_siam`). | MODEL | numerical test | NEW | — |
| Y143 | The honest statement: per-good propagation costs the exact identity and buys a per-node error a reasonable scalar keeps within a tenth of a percent, and the identity is what Goal 7 is stated in terms of. | DESIGN | derivation | NEW | — |
| Y144 | v4.0's 0.41% and v5.0's "redistributive and single-digit percent" were both artifacts of freezing the share at one commodity — v5.0 having correctly diagnosed exactly that defect in v4.0 — and the construction behind any such figure has to be stated with it. | WORLD | derivation | REVISED | X174 |

## §3.11 — Caravan power · §3.12 — Treasure fleets (lines 1312–1346)

**UNCHANGED:** C531–C547, C556–C560, V163–V172. No delta claims.

## §3.13 — Open questions (lines 1348–1408)

**UNCHANGED:** C561–C585, V173, V174, V175, V178, V181, V182, V183, W164, X175, X177, X178, X179,
X180, X183.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y145 | The one open wealth question becomes a **design** question rather than a classification one: should any source beyond province condition be allowed to multiply `goods_produced`? §1.3 reads development, the trade good and the four province-state modifiers and nothing else. | DESIGN | stipulated | REVISED | X176 |
| Y146 | ⚑ `trade_goods_size` and `trade_goods_size_modifier` are granted in buildings, event modifiers, great projects, static and province-triggered modifiers, **holy orders, state edicts and trade-company investments**. | ENGINE | file value | REVISED | X176 |
| Y147 | v3.0–v5.0 tried to admit the province-scoped subset by rule; that rule was wrong in every audit that examined it, so v6.0 drops it, and re-admitting any source re-admits the maintenance burden with it. | DESIGN | derivation | NEW | — |
| Y148 | Under the calibration's α = 16 the cloves demand order is `hangzhou`, `beijing`, `doab`, and the sink lands on a high-demand node rather than a geographic accident. | MODEL | numerical test | REVISED | X181 |
| Y149 | `hangzhou`, not Beijing, holds the richest single province — the 30.4 / 19.5 figures withdrawn. | MODEL | numerical test | REVISED | X182 |

## §3.14 — AI merchant assignment (lines 1410–1428)

**UNCHANGED:** C586–C624, X184. No delta claims.

## §3.15 — Rejected (lines 1430–1536)

**UNCHANGED:** C625–C672 as carried by v2, V184–V188, V192–V199, V226, V227, V228.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y150 | With v1's ε floor removed the contrasts run **4–97 on supply against 211–15,010 on demand** over the **28 goods produced in more than one node**; `cloves` has a single producer and no contrast to measure, which is the sparsity point in miniature. | MODEL | numerical test | REVISED | X185 |
| Y151 | v3.0 and v4.0 repeated the 10⁷ / 10²–10³ ratio here while **v4.0's own §3.2** was withdrawing it. | WORLD | derivation | REVISED | X186 |
| Y152 | Ranked orientation puts a far higher share of top-demand nodes in its sink sets than DRAIN and fails on delivery: monotone, so **a sixth of world demand is stranded**, it leaves orphan sinks a good cannot reach, posts net-producer sinks where DRAIN, LAP and FLOW post none, and keeps several times DRAIN's sinks per good — all stated without figures. | MODEL | numerical test | REVISED | X187, X188 |
| Y153 | Seeded basin growth leaves demand unserved **at every tuning tried** — the 88.4% best-tuning figure is withdrawn. | MODEL | numerical test | REVISED | X189 |
| Y154 | The `Φ_ord` graveyard entry maintains **no figures**: it is not installed, its numbers moved with every change to the wealth field, and the design argument does not rest on them; the self-coherence ceiling v2.0 and v2.1 quoted predates §3.6's deterministic sweep. | DESIGN | stipulated | REVISED | W062 † |
| Y155 | The 3-mass gravity kernel reproduces whatever end count it is seeded with while γ is small enough and loses that property as γ approaches 1; **no figures are maintained** — every agreement percentage the entry carried in v2.0 through v5.0 was measured on a superseded wealth field. | MODEL | numerical test | REVISED | X190, X191 |
| Y156 | A pure `wealth^α` edge comparison with no reach term does not concentrate ends at all, because a local wealth maximum survives every positive α — the "≥10 ends at α up to 16" measurement is dropped. | MODEL | derivation | REVISED | V225 † |

## §3.16 — Evidence standard (lines 1538–1601)

**UNCHANGED:** C677, C680–C682, C684, C685, V200–V203, V206–V210, W173–W181.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y157 | v1's ε instantiation "failed at the tolerance v1 used" — the 1e-5 figure is withdrawn. | MODEL | numerical test | REVISED | V204 |

---

# Stranded prior IDs

## X IDs carried UNCHANGED (63)

X005, X006, X007, X012, X014, X015, X016, X017, X023, X024, X025, X026, X059, X060, X061, X062,
X067, X089, X090, X091, X102, X103, X104, X105, X109, X110, X115, X116, X118, X119, X120, X121,
X123, X124, X127, X128, X133, X134, X135, X136, X137, X138, X146, X147, X148, X149, X150, X152,
X153, X156, X157, X161, X164, X165, X167, X175, X177, X178, X179, X180, X183, X184, X196.

## X IDs withdrawn — stated wrong, or deleted with no replacement (27)

| Withdrawn ID | What it said | Where v6.0 leaves it |
|---|---|---|
| **X003** | v5.0's classification change "moves the aggregate graph from two 1444 sinks to one" | §1.6 measures **two** sinks on the v6.0 field; the proposition is gone from the header |
| **X029** | ⚑ Fifteen 1444 provinces carry a flat goods bonus in the additive block | §1.3: "under §1.3 no source grants one" — the ordering is retained, the count is gone |
| **X032** | The engine's trade-good data model is one *instance* of the locality test, not the test itself | Deleted with the classifier |
| **X041**, **X042** | glass `local_production_efficiency` and chinaware `local_autonomy` are local but do not enter wealth | Table deleted; glass survives only as §3.13's settled note, which is UNCHANGED |
| **X043** | ⚑ 361 provinces carry a centre of trade at 1444 and no CoT level grants a key wealth reads | Deleted |
| **X044** | ⚑ `production_leader` `trade_goods_size_modifier = 0.10` is not local | Deleted |
| **X045** | ⚑ `bonus_from_merchant_republics` (`eu4.exe:0x1cc7128`) is not local | Deleted |
| **X046** | ⚑ Buildings are local by the test and empty at 1444 | Deleted |
| **X047** | ⚑ `terrain.txt` and the climate static modifiers grant only nine named non-wealth keys | Deleted |
| **X048**, **X049**, **X050** | Great projects contribute `province_modifiers` up to `starting_tier`; later tiers are owner spending; 85 of 130 are country-gated | Deleted |
| **X051**, **X052** | The six projects carrying a wealth key; province 1821 is the richest single province in the game | Deleted — §2.8 now says only "the richest single province the model counts", of `hangzhou` |
| **X053** | `starting_tier` is the right line and "owner action" is not | Deleted |
| **X054** | ⚑ The permanent province modifiers, by name and province | Deleted |
| **X055**, **X056** | ⚑ `stora_kopparberget_modifier` gated `NOT = has_dlc Leviathan`, granting 5.0 where the project gives 3.0 | Deleted |
| **X058** | glass and chinaware are the whole of the rule-versus-vocabulary tension | Deleted with the second test |
| **X071** | v2–v4's two-sink result was measured on a field missing sixteen provinces; correcting it removes the second sink | §1.6 measures two sinks again; the explanation is withdrawn |
| **X079**, **X080** | The 3-sink [2.26, 2.71] and 2-sink `{genua, hangzhou}` [1.94, 2.25] α_Φ bands | Band table deleted; only 1.5's own band survives (Y072) |
| **X092** | Developing the nine Lowland provinces by ×1.20 makes `english_channel` a sink and it stays one through ×10 | Deleted with the Europe bullet list |
| **X093** | ±2% random noise leaves the sink set unchanged on three seeds; +2% on Europe alone changes it | The noise half survives as Y066; the contrast is gone |
| **X171** | The per-good propagation error is thirteen orders of magnitude above the float residual and moves income between countries | Deleted; §3.10 now frames the claim as exactness, not magnitude (Y140) |
| **X173** | No node has local trade value near 250; the largest is 112.6 | The "near 250" half survives in the parenthetical; the **112.6** figure is deleted |

## Older IDs replaced for the first time in v6.0 (12)

W002 (→ Y001), W023 (→ Y020), W025 (→ Y021), W036 (→ Y032), W050 (→ Y048, Y053), W052 (→ Y054),
W062 † (→ Y154), W067 (→ Y114), W189 (→ Y056), V138 (→ Y124), V204 (→ Y157), V225 † (→ Y156).

## Propositions restored to an earlier version's wording

Two v6.0 measurements return to figures a pre-v5 inventory already carried, after v5.0 had replaced
them. They are recorded as REVISED against the v5 ID, with the older ID noted here:

- **Y065** (eight sources, `c_w` ranks 44–75, mean degree 3.1) is **W060** verbatim; X073 had
  replaced it with seven sources, ranks 52–79, degree 3.0.
- **Y063** (two sinks, `english_channel` and `hangzhou`) restores **V215's count**, which X070 had
  replaced with one sink — though the ranks, the Phase-1 selection and the promotion count all
  differ from V215's.

# † Unresolvable `Replaces` targets

- **Y154** — the `Φ_ord` graveyard entry's "retained as the measured coherence ceiling any future
  aggregate should be compared against" is a DESIGN proposition distinct from the 60.3% figure
  itself. `claims-v3.md` records the graveyard ceiling as **W062 at first appearance**, so W062 is
  named; but no prior inventory issued a separate ID for the *retain-as-benchmark* stipulation.
- **Y156** — the "a local wealth maximum survives every positive α" clause is carried inside
  **V225**, whose other half (the gravity kernel's seeded-count behaviour) went to W190 and then to
  X190. V225 is named for the α clause; no ID isolates it.

# Recorded without assessment

Three textual facts about the document, noted so a later pass can find them. No judgement is offered
about which reading is intended:

1. §1.3 says "**Eleven** counted provinces begin devastated" and, later in the same section, "province
   265 … is also one of the devastated **ten**" (Y041, Y047).
2. §2.2 item 4 says `GP_COEFF` is "**read from** `common/static_modifiers/00_static_modifiers.txt`
   rather than hardcoded" (Y097); §2.3 says the two wealth coefficients "are hardcoded in the
   binary — `defines.lua` and `common/defines/` were searched and contain neither" and are therefore
   *measured* (X118, X119, both UNCHANGED).
3. §1.6's opening parenthetical states the v2.0–v4.0 position twice and closes with an unmatched
   `**` before its closing paren ("only their locations are emergent.**").
