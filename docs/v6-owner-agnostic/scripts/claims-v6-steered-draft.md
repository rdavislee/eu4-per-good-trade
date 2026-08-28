# Claim Inventory Delta — Per-Good Trade Network Spec v6.0

Extracted from `per-good-trade-spec.md` (v6.0, 1,587 lines) as a **delta against
`../v5-owner-agnostic/claims-v5.md`** (X001–X196), which is itself a delta against
`../v3-owner-agnostic/claims-v3.md` (W001–W195), `../v2-drain/claims-v2.md` (V001–V230) and
`../v1-laplacian/claims.md` (C001–C685). **Extraction only.** Nothing here is validated, corrected,
or graded; where the brief asks for observations about the document's own two prose rules, those are
findings about the *text*, not verdicts on the propositions.

**Method.** Four documents read in full: the v6.0 spec, `claims-v5.md`, `changes-v6.md` and
`fixes-agreed.md`. Every row below was read off the v6.0 spec text itself. `changes-v6.md`'s 45
replacements were used **only** to locate changed passages, and `fixes-agreed.md` only to see what
the author intended to change — neither is a source for any claim, and both are contradicted by the
spec in places (recorded under (b) and in the Observations). `claims-v3.md` was grepped to resolve
four IDs (W025, W036, W050, W063); `claims-v2.md` and `claims.md` were not read.

**ID prefix.** v1 `C`, v2 `V`, v3 `W`, v4 none, v5 `X`. **v6 uses `Y`**, numbered in document order.

**Statuses.** UNCHANGED — same proposition as an existing C/V/W/X ID; the old ID is recorded and no
Y ID is issued. REVISED — the proposition changed; new Y ID with the old ID(s) in `Replaces`. NEW —
no counterpart in any prior inventory. A proposition stated in two sections keeps one ID at first
appearance. Renaming the script that produced a figure (`v5measure.py` → `measure6.py`) is **not** a
proposition change; changing the figure is.

**Vocabularies carried over.** Type: ENGINE / MODEL / DESIGN / OUTCOME / WORLD. Provenance:
stipulated / derivation / file value / numerical test / engine test / prose source /
verified (method unstated) / UNSOURCED. `numerical test` (a solver experiment) and `engine test`
(an observation of EU4 running) are kept strictly distinct.

**Full-strength sections**, extracted row-by-row per the brief: **§1.3** (the wealth definition and
the province-state modifiers) and **§1.6** (the installed map, the α_Φ band, and the Europe claims).

**Markers.** **⚑** a row introducing an engine fact no prior inventory carried. **§** a row whose
stated evidence is a single observation. **†** a row whose `Replaces` target is believed to exist but
could not be pinned to an ID.

---

# Summary

**142 delta claims extracted, Y001–Y142**: **54 NEW, 88 REVISED**, replacing **89 distinct prior
IDs** (85 X, 4 W). No row carries †.

### By status and Type

| Type | NEW | REVISED | Total |
|---|---|---|---|
| MODEL | 22 | 58 | 80 |
| ENGINE | 13 | 11 | 24 |
| DESIGN | 11 | 14 | 25 |
| WORLD | 8 | 5 | 13 |
| OUTCOME | 0 | 0 | 0 |
| **Total** | **54** | **88** | **142** |

### By Provenance

| Provenance | Count |
|---|---|
| derivation | 51 |
| numerical test | 50 |
| stipulated | 20 |
| file value | 17 |
| engine test | 4 |
| UNSOURCED | 0 |
| **Total** | **142** |

No row carries UNSOURCED provenance. Ten figures do, however, carry **no named script** although §0
promises that "measured figures carry the script that produced them" — listed in Observation 8.

**17 rows are marked ⚑** (11 NEW, 6 REVISED). **3 rows are marked §** — Y028, Y030, Y047; two are
the carried tooltip observations, one is new (Uppland).

### Where the delta concentrates

| Section | Y rows | What drove it |
|---|---|---|
| §1.3 Demand | 39 | option (c): the classifier deleted, the province-state table, three corrected start-state reads |
| §1.6 Aggregate graph | 32 | the two-sink result returns, α_Φ becomes a stipulation, Europe restated directionally, the Cape |
| §2.4 The tradenodes file | 11 | Phase 2's degenerate LP and the four index tiebreaks |
| §0 Front matter | 10 | the (c) headline plus the two new prose rules R2 and R3 |
| §3.2, §3.5, §3.10 | 8 each | sparsity vs contrast; the executable price census; exactness-not-materiality |
| §3.15 Rejected | 6 | R3 deletions plus regenerated RANK and gravity-kernel entries |
| §1.10, §2.2 | 6 each | the caravan denominator and the cooldowns; the (c) wealth pipeline |
| §1.1 | 5 | the fallback branch restated on the post-peel balance |
| §1.5, §2.8, §3.9 | 1 each | |

---

# (a) Which propositions stand on no replaced predecessor?

v6.0 deletes a large apparatus and adds a smaller one. The 54 NEW rows fall into four groups; only
the third is new subject matter in the strong sense, and only eleven rows assert a new fact about
EU4.

### Group 1 — the *deletion* of the classifier, and its bookkeeping (10 rows)

**Y002, Y003, Y004, Y017, Y018, Y019, Y021, Y022, Y031, Y032.** These are NEW because a deletion has
no predecessor: no prior inventory contains "the classifier is gone", "it was worth 0.98% of world
wealth", or "owner-agnosticism is now true by construction". Every one of them is a **re-scoping**
statement — it asserts something *about* X030–X058 rather than adding subject matter. Y003 and Y021
(0.98%, 87 of 2,472) are the only measurements in the group, and they are the measurement of the
deleted apparatus's footprint.

### Group 2 — the corrected start-state reads (11 NEW rows plus the REVISED Y041; 6 of them ⚑)

**Y005, Y041–Y048, Y050, Y051, Y053.** This is **genuinely new subject matter**: no prior inventory
carried `on_startup`, `on_startup_effect`, `flavor_boh.15`, dated `add_base_*` accumulation, or the
`is_city` non-filter. v5.0's X040 asserted the *opposite* of Y041 ("all are zero at the 1444 start"),
so Y041 is a REVISED row, but the mechanism behind it (Y042, Y045) is new ground. ⚑ on **Y042**
(the `on_startup` → `flavor_boh.15` chain), **Y045** (`flavor_geo.1` moves development before the
first tick), **Y046** (dated `add_base_*` accumulates), **Y047** (Uppland 5+1 = 6, §), **Y048**
(`is_city = yes` is not a filter the engine applies), **Y050** (twenty provinces with
`trade_goods = unknown`, assigned from `chance = { }`).

### Group 3 — the LP-degeneracy account (10 NEW rows plus the REVISED Y100)

**Y006, Y101–Y109.** **Genuinely new subject matter, and the largest free-standing addition in
v6.0.** No prior inventory contains any proposition about Phase 2's optimal face. v5.0's X125 said
the canonical node order is required *because of the sweep's index tiebreak*; v6.0 does not refine
that, it replaces the reason (Y100, REVISED) and then builds ten propositions on ground v5.0 never
occupied: 580/580 relabellings, 10/10 arc permutations, the objective gaps, the HiGHS-specific/in-kind
distinction, the tie-breaking-objective option, and the four index tiebreak sites. None asserts a
fact about EU4 — they are all facts about the solver — so none carries ⚑.

### Group 4 — everything else (23 rows)

| Rows | Subject | New matter or re-scoping? |
|---|---|---|
| Y007, Y008 | the R2 and R3 prose rules themselves | new matter (a convention, not a claim about the world) |
| Y027, Y039 | the v3.0–v5.0 tooltip schema was false on both its data points; only `occupied` touches the tax term | re-scoping of X021 / X040 |
| Y070 | the written warning against re-deriving α_Φ = 1.5 from the two-sink resemblance | new matter (a prohibition) |
| Y072 | wealth is linear in development, so `c_w` shares move directly | re-scoping — the mechanism under X085 |
| Y075, Y077 | ×2.00 → `genua` alone; development-scaling ≡ wealth-scaling, max difference 0.0 | Y077 is new matter and it is what makes X091 moot |
| Y082, Y083 | the Cape as a live conduit (132 ordered pairs); v5.0's universal was false | Y082 new matter, Y083 re-scoping |
| Y089 ⚑ | the three shipped cooldown defines | **new fact about EU4** |
| Y090, Y092 | what is left exposed; the after-the-grant denominator | re-scoping of X106 / X107 |
| Y096 ⚑ | `GP_COEFF` is **read from** `00_static_modifiers.txt` | **new fact about EU4** — and it contradicts §1.3 and §2.3 (Observation 1) |
| Y099 | twelve fresh runs put one inside v5.0's stated interval | re-scoping of X114 |
| Y120 ⚑, Y122 ⚑, Y123 ⚑, Y124, Y126, Y127 | `change_price` is a fraction of base price; ten of 161 never execute; the duplicate/dead partition; the missing guard; the `pdx.py` tokeniser | Y120/Y122/Y123 are **new facts about EU4**; Y126/Y127 are facts about v5.0's toolchain |
| Y133, Y134 | the value-weighted mean share keeps the error ≤ 0.1%; the honest statement | new matter — the scalar a real implementation would store was never named before |

### ⚑ NEW rows asserting a new fact about EU4 (11)

**Y042, Y045, Y046, Y047 §, Y048, Y050** (§1.3's start state) · **Y089** (§1.10's cooldowns) ·
**Y096** (§2.2's `GP_COEFF` source) · **Y120, Y122, Y123** (§3.5's price census). Six ⚑ REVISED rows
also carry new observations: Y026, Y028, Y030, Y035, Y041, Y121.

**Observation on the trade.** v5.0 imported 21 ⚑ rows into §1.3 alone through the whole-install
sweep. v6.0 deletes all of them and imports six — the start-state reads. The new six are cheaper to
keep correct (four file paths and one save-state read) and are the only place v6.0 adds engine
surface; the classifier's fourteen file-value rows are gone with their subject.

---

# (b) Which prior IDs does v6.0 strand?

v6.0 removes or withdraws propositions carried by **82 prior IDs**: **38 deleted because their
subject is gone**, **5 deleted under R3**, and **39 withdrawn as wrong** (several in half — the
row's other clause survives). **Forty-four of the 82 were CONFIRMED** in `validation-v5.md` — they are
absent from `fixes-agreed.md`'s 62-item graded-open table, which is that file's own definition of an
untouched claim — and they split two ways:

- **25 CONFIRMED and deleted as moot** (subject gone): X029, X031, X032, X034, X036, X037, X038,
  X039, X041, X042, X044, X049, X051, X052, X053, X054, X057, X092, X093, X095, X096, X098, X101,
  X144, X173.
- **19 CONFIRMED and withdrawn as wrong**: X002, X003, X063, X070, X071, X072, X077, X079, X080,
  X081, X082, X088, X126, X192, X193, X194, X195 — the whole one-sink result, its band table and its
  noise study — plus **X076** and **X187**, deleted under R3. This is the sharper half of the answer:
  v6.0 does not only drop confirmed claims whose subject it deletes, it reverses nineteen the last
  audit had confirmed, because the wealth field moved under them.

### Deleted because the subject is gone: the modifier classifier and everything it governed

The whole of §1.3's classification apparatus. The v6.0 text that does it is §0
(*"The two-test modifier classifier and everything it governed … are deleted, along with the
whole-install sweep that maintained them"*) and §1.3 (*"`base_tax`, `base_production` and the trade
good are bare attributes of the place, so nothing about them needs classifying"*), plus the physical
absence of the classification table.

| Prior ID | What it said | v5.0 grade | How v6.0 removes it |
|---|---|---|---|
| X030 | the locality test | PART | table deleted — **but §3.13 l.1363 still requires "the §1.3 locality test"** (Obs. 3) |
| X031 | the wealth test | CONFIRMED | table deleted; no replacement test |
| X032 | the trade-good data model is one *instance* of the locality test | CONFIRMED | absent |
| X033 | the tests are applied to the whole install | PART | **§3.13 l.1358 still cites "§1.3's whole-install sweep"** (Obs. 3) |
| X034 | v4.0 swept only `common/tradegoods/` and missed sixteen provinces | CONFIRMED | absent |
| X035 | the vanilla local-and-enters set | REFU | narrowed to Y020: `gems`/`incense` are province-scoped and *no longer read* |
| X036, X037 | `gems` on 43 provinces; `incense` on 29 | CONFIRMED | counts absent; the keys survive only as "what this gives up" |
| X038, X039 | great-project `province_modifiers` (6 provinces); `add_permanent_province_modifier` (10) | CONFIRMED | absent |
| X041, X042 | `glass` `local_production_efficiency`; `chinaware` `local_autonomy` | CONFIRMED | absent from §1.3; the glass reading survives only in §3.13's settled note |
| X043 | 361 provinces carry a centre of trade; no CoT level grants a key wealth reads | PART | absent — the "clean near-miss, recorded so it is not reopened" is itself gone |
| X044 | `production_leader` is not local | CONFIRMED | absent |
| X045 | `bonus_from_merchant_republics` (`eu4.exe:0x1cc7128`) is not local | PART | deleted from §1.3 — **but retained as an example in §3.13 l.1357** |
| X046 | buildings are local by the test and empty at 1444 | PART | absent |
| X047 | `terrain.txt` and the climate modifiers grant nothing wealth computes | PART | absent — and §1.3's own owner-agnosticism sentence dropped "terrain" (Y016) |
| X048, X049, X053 | the `starting_tier` rule; post-start tiers are owner spending; why "owner action" is the wrong line | PART/CONF/CONF | absent |
| X050, X051, X052, X054 | 85 of 130 projects gated; the six named projects; province 1821 is the richest single province; the ten permanent modifiers named | REFU/CONF/CONF/CONF | absent |
| X055, X056, X057 | the `stora_kopparberget_modifier` Leviathan gate; 3.0 with / 5.0 without; every figure measured with Leviathan installed | PART/PART/CONF | absent — §2.3's "DLC state is a third input axis" survives but no longer has a wealth figure depending on it |
| X058 | glass and chinaware are the whole of the rule-versus-vocabulary tension | REFU | absent |
| X029 | fifteen 1444 provinces carry a flat goods bonus | CONFIRMED | §1.3 now says *"under §1.3 no source grants one"* — **but §3.13 l.1359 still states the fifteen** (Obs. 3) |
| X112 | the solver reads the classification: 16 provinces beyond the two trade goods | REFU | replaced by Y095 (four province-state modifiers, `devastation` live on eleven) |
| X092 | the Lowlands ×1.20 result | CONFIRMED | deleted with no replacement (`fixes-agreed` P2: vacuous once the Channel is already a sink) |
| X093 | ±2% random noise vs +2% systematic Europe | CONFIRMED | deleted; Y061 gives ±1% on three seeds instead |
| X173 | no node's local trade value is near 250; **the largest is 112.6** | CONFIRMED | §3.10 keeps the first clause and drops the figure |
| X101's figures | `hangzhou` sole sink at ×20/×30/×50, transient split at ×10 | REVISED-in-v5 | generalised into Y087 |
| X144 | `girin`, `yumen`, `chengdu`, `lhasa` need 4.0–10.8× | CONFIRMED | generalised into Y116 ("other nodes in the region need more still") |
| X095, X096 | the Volga and Hansa/Danube node lists | CONFIRMED | routes named, node lists deleted (Y080) |
| X098's route | `malacca → cape_of_good_hope → zanzibar → gulf_of_aden → alexandria → genua` | CONFIRMED | route deleted, claim kept (Y084) |

### Deleted because the operator is rejected (R3)

| Prior ID | What it said | How v6.0 removes it |
|---|---|---|
| X076 | `Φ_ord`'s edge-good agreement is **60.3%** under the deterministic sweep | §1.6: *"The superseded marking-order aggregate scored higher on that measure"* — comparative kept, figure gone (Y064) |
| X160 | `Φ_ord` has 13 end nodes at 1444, 8 terminating no good, count 11–17 across cloves-α 2…64 | §3.9: *"a majority of them terminate no good at all … the end count does not concentrate"* (Y128) |
| X187's alignment figures | ρ_val +0.281 vs +0.054; 43.8% vs 14.5% of top-decile nodes | §3.15: *"it puts a far higher share of top-demand nodes in its sink sets than DRAIN does"* (Y139) |
| X190's gravity figures | any count for γ ≤ 0.7; the γ = 0.9 collapse to three ends; 61% = 97 of 159 arrows | §3.15: *"reproduces whatever end count it is seeded with while γ is small enough"* + *"No figures are maintained for it"* (Y141) |
| X191 | v2.1–v4.0's γ = 0.97 and four-end readings do not hold on the corrected field | absorbed into Y141's blanket "every agreement percentage this entry carried in v2.0 through v5.0" |

### Withdrawn as wrong

| Prior ID | What it said | The v6.0 text that withdraws it |
|---|---|---|
| **X002, X003** | v5.0's substantive change is the whole-install classification, and it moves the aggregate from two 1444 sinks to one | §0 (Y001) replaces the change; §1.6 (Y058) restores **two sinks**, so X003 is reversed outright |
| **X021** | the tax tooltip reads `Base: X (Yearly 12·X)` | §1.3: *"it is **not** twelve times the displayed figure, which would give 5.88 and 1.92. (v3.0 through v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both of its own data points.)"* → Y026 |
| **X027** | `Base 0.49` × 125% gives 0.6125, shown as 0.62 | §1.3: *"0.49 × 1.25 is 0.6125, which truncates to 0.61, not 0.62 … requires rounding while §2.3 requires truncation. Both cannot hold."* → Y030 |
| **X063** | every counted province is a city (`is_city = yes`) | §1.3 item 3: *"`is_city = yes` is not a filter the engine applies"* → Y048, Y049, Y052 |
| **X040** (half) | the province-state static modifiers are **all zero at the 1444 start** | §1.3: *"**They are not all quiet at the 1444 start.** Ten provinces begin devastated"* → Y041 |
| **X070, X072** | one sink, `hangzhou`, c_w rank 1 / wealth rank 10; Phase 1 selects it directly; 0 promotions | §1.6: two sinks, c_w ranks 2 and 3, Phase 1 selects `genua`, 2 promotions → Y058, Y059 |
| **X071** | the two-sink result was an artifact of a field missing sixteen provinces | deleted without replacement; the two-sink result returns on the field that has no sweep at all |
| **X077–X082, X192–X195** | the α_Φ = 1.00…3.00 band table, the [1.406, 1.424] refinement, the 8-seed noise analysis, and the principle that a constant cannot sit inside a window narrower than its own edge uncertainty | §1.6's replacement paragraph: one band ([1.38, 1.63], width 0.25) and the [1, 8] scan; the table, the noise study and X194's principle are gone → Y067, Y068 |
| **X083, X078** | α_Φ = 1.5 is retained because it sits inside the **widest** band | §1.6: *"1.5's is not the widest by any margin"* → Y065, Y066. **§2.3 still asserts X083 verbatim** (Obs. 1) |
| **X088** | what the model claims is **the threshold**: 2% is enough | §1.6: *"These are properties of this snapshot, not constants of the model"* → Y076 |
| **X097** | nothing routes through the Cape in `Φ_w` | §1.6: *"v5.0 said 'nothing routes through the Cape', which is false as a universal"* → Y081, Y083 |
| **X107** | the caravan cap is 8.6–32.0% of an inland node's total power | §1.10: *"which cannot be right, since 8.6% of 532.0 is 45.8 rather than 50"* → Y091, Y092 |
| **X114** | 0.17–0.21 s for all 29 goods | §2.2: *"twelve fresh runs put only one inside that interval"* → Y098, Y099 |
| **X125** | the node order is a correctness requirement **because §1.1's key breaks ties by index** | §2.4: *"the reason is Phase 2 rather than any tiebreak"* → Y100 |
| **X126** | one end node at 1444 | §2.4 item 2: two end nodes → Y110 |
| **X145, X013** (half) | the sink-set equality holds where Phase 0 is a no-op and no fallback fires | §3.2: *"those conditions are **necessary, not sufficient**: T2 below satisfies both and still breaks the equality"* → Y117. **§1.1 still asserts the conditioned form** (Obs. 2) |
| **X151** | the one place the indexing is load-bearing is the fallback branch | §3.2: four tiebreak sites, *"which is not only the fallback branch"* → Y119 |
| **X117** (half) | free-edge determinism's two halves are unaffected by peeling | §3.2: *"peeling can **create** exact ties that the raw input balances do not have"* → Y118. **§2.2a's table still asserts the old form** (Obs. 2) |
| **X011** | the fallback branch is why §2.4 makes node order a correctness requirement | §1.1: *"It is not the reason §2.4 requires a canonical node order"* → Y015 |
| **X010** | at a fallback the candidates are *usually all zero-wealth* | §1.1 drops "zero-wealth" for the general tie (T3's own candidates carry wealths 3, 2, 1) → Y014 |
| **X008, X009** | the fallback needs `b ≡ 0` across a connected core; uniform wealth suffices for the aggregate | §1.1: **post-peel** balance, and the aggregate needs uniform `Σ wealth^α_Φ`, *"which uniform wealth gives but is not the same condition"* → Y012, Y013 |
| **X155** (half) | the price scan is guarded by a per-file count assertion | §3.5: *"there was no assertion anywhere in its toolchain"* → Y126 |
| **X166** (half) | 3.7e-16 is *at most one unit in the last place* | §3.10 l.1292: *"one to three units in the last place, not the single ULP v5.0 claimed"* → Y129. **§3.10 l.1290 still says "at most one unit in the last place"** (Obs. 4) |
| **X169, X170, X171** | eight downstream sets and a 0.003% effect; nine per-collector percentages; thirteen orders of magnitude above the float residual | §3.10: seven sets, and *"a claim about exactness, not about magnitude"* → Y130, Y131, Y132 |

### Not stranded, though `fixes-agreed.md` says MOOT

**X045, X029, X030, X033, X176, X179** are all marked MOOT in the checklist because option (c)
deletes their subject — and all six **survive in §3.13**, which was edited only to change its banner
from "v5.0" to "v6.0". **X091** is likewise marked MOOT and survives verbatim in §1.6.

---

# (c) Does v6.0 obey its own two stated prose rules?

Both rules are new in v6.0 and neither is fully kept. The pattern is consistent and diagnostic:
**every passage the 45 replacements touched obeys R2 and R3; the violations are all in passages the
patch pass did not open.** R2 is broken in sixteen places, R3 in three (plus one that R3's own
three-name scope lets through). Quoted retractions ("v5.0 said X, which is false") are not counted.

## R2 — no superlative, no universal quantifier, no threshold asserted as a fact about the world

### Violations in passages v6.0 rewrote — none

The rewritten passages are the rule working. §1.6 l.454-455 states the Cape result as
*"**No Europe→sink route passes the Cape of Good Hope** — checked from `genua`, `north_sea` and
`english_channel`"*; §1.6 l.439-441 labels the Europe table *"properties of this snapshot, not
constants of the model"*; §1.6 l.465-468 converts a threshold into a window *"bounded above as well
as below … and its edges move with the field"*. These are the template.

### Violations

| # | Line | Text | Why it violates R2 |
|---|---|---|---|
| 1 | §2.3, 773 | *"1.5 is retained because it sits inside the **widest** sink-count band and nothing now selects a different value"* | superlative, and the *withdrawn* one: §1.6 l.408 says *"1.5's is not the widest by any margin"*. The most consequential violation in the document — see Obs. 1 |
| 2 | §1.6, 366 | *"**Their count is set by `α_Φ`**; only their locations are emergent"* | a threshold-style absolute contradicted by §1.6's own Europe table, where the count moves from 2 to 3 to 2 to 1 at fixed α_Φ, and by §2.4 item 2 (*"it follows the wealth field **and** `α_Φ`"*) |
| 3 | §1.5, 337 | *"Coal's base price of 10.0 is the **highest** in vanilla"* | superlative about shipped data, no scope, no script |
| 4 | §2.8, 924 | *"it holds the **richest single province in the game**"* | superlative; its §1.3 source row (X052) was deleted in this very version, so nothing in v6.0 supports it |
| 5 | §3.13, 1385-1388 | *"that is `hangzhou`, at **30.4** against Beijing's 19.5"* | the same superlative, plus a figure the (c) field moves to 27.00 (`fixes-agreed` §1) |
| 6 | §1.3, 289 | *"removes the **single largest** source of hidden owner-dependence"* | superlative with no measurement anywhere in the document; W052, carried UNCHANGED since v3.0 |
| 7 | §1.9, 544 | *"receives a share of it in **every** immediately upstream node — with **no condition on the receiving node**"* | universal quantifier over an engine behaviour, evidence one node (France in Sevilla) |
| 8 | §1.8, 538 | *"There is **no** trade 'supply range' in the engine; the **only** supply-range constructs are naval"* | unscoped universal about the engine — and the sentence three lines above it models the compliant form perfectly |
| 9 | §1.10, 593-598 | *"**No** mission, decision, event, or trade company in 1.37.5 names a trade node — zero non-comment references across **all** of `common/`, `missions/`, `decisions/`, `events/`"*, and *"Nodes themselves **never** change under the mod … so the name-collision class of conflict is **empty**"* | universals over the install with no script named |
| 10 | §3.5, 1132-1134 | *"At vanilla base prices **nothing** sits below the 2.0 anchor: the **minimum** tradeable base price is exactly 2.0"* | absolute + superlative about shipped data |
| 11 | §3.5, 1140 | *"**11 goods have no negative price event at all** and can **never** go sublinear in vanilla"* | universal over campaign futures |
| 12 | §3.5, 1152-1153 | *"**All** ten are positive and **every** negative block in the install is executable"* | universal over the census (v6.0's own new text — the one R2 lapse inside a rewritten passage) |
| 13 | §3.15, 1475 | *"It is **the most self-coherent aggregate measured**"* | R3 took this entry's numbers and left its superlative standing |
| 14 | §1.12, 622-624 | *"**none** takes a commodity argument — **zero** per-good fields, where thirty would be needed"* | universal over the node window's fields |
| 15 | §3.3, 1101-1103 | *"a 4× spread with **no structural rule behind it**"* | universal about the map authors' intent |
| 16 | §3.13, 1339 | *"the **only** direction-refusal strings in the binary belong to sell-province and treasure fleets"* | universal over the binary — mitigated by sitting under the "prose-sourced, distrust" banner |

## R3 — no maintained figures for `Φ_ord`, the gravity kernels, or the v1 Laplacian

| # | Line | Text | Verdict |
|---|---|---|---|
| 1 | §3.9, 1269 | *"**7.8 points** of self-coherence given up for one operator and world-responsive ends"* | **Violation, and the worst one.** 7.8 is exactly `Φ_ord`'s 60.3% minus `Φ_w`'s 52.5% — both endpoints deleted elsewhere in this same version, and 52.5% is no longer even v6.0's number (53.5% is). A maintained figure for the rejected operator, in the bullet that adopts `Φ_w` |
| 2 | §3.4, 1124-1126 | *"In v1 the same substitution also broke the α = 1 identity, measured as orientation agreement collapsing from **159/159 to 68/159**"* | **Violation.** A maintained v1-Laplacian measurement, load-bearing in a live design argument (why production income is refused) — though the paragraph then says the reason is unchanged without it |
| 3 | §3.16, 1537-1539 | *"implemented as written, the identity **failed at 1e-5**"* | **Violation, narrowly.** A maintained v1-Laplacian figure; it serves the evidence-standard anecdote rather than a design argument, which is the mitigation |
| 4 | §3.15, 1423-1424 | *"the contrasts run **4–97 on supply against 211–15,010 on demand** over the 28 goods produced in more than one node"* | **Not a violation, but the only numbers left in the three graveyard entries.** They describe the *input field*, not the Laplacian, and the author re-measured them deliberately (`fixes-agreed` E-series) |
| 5 | §3.8, 1233 | *"(v2 quoted 98.8%; that is v1's *Laplacian* figure, 6245/6320 …)"* | **Not a violation** — a quoted retraction, per the brief |

**A gap in R3 as written, not a violation of it.** R3 names three operators. Four other rejected
operators keep live figures, and two of them were *regenerated in this pass*: RANK's
`83.0% reachable / 31 orphan sinks / 8 net-producer sinks / 10–16 sinks per good` (Y139, Y140) and
seeded basin growth's `88.4%` (X189, UNCHANGED). If R3's rationale is "those numbers cost refutations
on recount and buy one comparison sentence each", it applies to these identically.

---

# Claim tables

## §0 — Front matter (lines 1–38)

**UNCHANGED:** C002, C003, C004, V001 *(via §2.5)*, V002, V003, V004, W001, W002.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y001 | v6.0's substantive change is to §1.3: **wealth is a function of the province's development, its trade good and its own current condition, and of nothing else.** Restated as the definition at §1.3. | DESIGN | stipulated | REVISED | X002 |
| Y002 | The two-test modifier classifier and everything it governed — trade-good modifiers, great projects, permanent province modifiers, buildings, centres of trade and the DLC conditionality — are deleted, along with the whole-install sweep that maintained them. | DESIGN | stipulated | NEW | — |
| Y003 | On the 1444 start that apparatus was worth **0.98%** of world wealth. | MODEL | numerical test | NEW | — |
| Y004 | What it cost was an input surface whose classification was wrong in every audit that examined it. | WORLD | derivation | NEW | — |
| Y005 | Three start-state reads are corrected in the same pass: `on_startup` devastation, dated `add_base_*` accumulation, and the `is_city` filter the engine does not apply. | MODEL | derivation | NEW | — |
| Y006 | **Phase 2's min-cost flow is degenerate, so presentation order selects which optimum is returned** — the reason a canonical node order is a correctness requirement. Measured at §2.4. | MODEL | numerical test | NEW | — |
| Y007 | **R2 — no empirical absolutes:** no superlative, no universal quantifier and no threshold asserted as a fact about the world; a claim is either a directional design statement or an observation scoped to the field and script that produced it. | DESIGN | stipulated | NEW | — |
| Y008 | **R3 — no maintained figures for rejected operators:** `Φ_ord`, the gravity kernels and the v1 Laplacian keep their §3.15 graveyard entries and lose their numbers, which were re-measured and re-refuted in three successive audits without any design argument depending on them. | DESIGN | stipulated | NEW | — |
| Y009 | Every graded claim from `validation-v5.md` — **22 refuted, 39 partial, 1 unverifiable** — is folded through, and `fixes-agreed.md` maps each one to the change that answers it. | WORLD | stipulated | REVISED | X001 |
| Y010 | Measured figures carry the script that produced them, and `scripts/verify6.py` re-derives each one **from the document text** and fails if the two disagree. | DESIGN | stipulated | REVISED | X004 |

## §1.1 — Trade direction (lines 44–146)

**UNCHANGED:** C005, C006, C010–C012, C019–C022, V005–V015, V017–V024, V026–V028, V031, V032,
V036, V037, W007–W011, W015–W022, X005, X006, X007, X012, X014, X015, X016, X017.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y011 | Where Phase 0 is a no-op and no fallback fires the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods on 1444, **1–8 sinks per good, mean 3.52**, zero fallbacks (`measure6.py`). | MODEL | numerical test | REVISED | X013 |
| Y012 | The fallback fires only when every candidate is support-isolated with zero **post-peel** balance: the key reads the balance Phase 0 hands on, with each pendant folded into its parent, not the raw input `b`, so a map with non-zero raw balances can still reach the branch. | MODEL | derivation | REVISED | X008 |
| Y013 | On a connected core the branch needs the folded balance to vanish across the core — for a per-good graph a component with no producer and no consumer; for the aggregate graph each node's `Σ wealth^α_Φ` equal, **which uniform wealth gives but is not the same condition**. | MODEL | derivation | REVISED | X009 |
| Y014 | Where the wealth key ties, the **node index decides** — which is why §2.8 asserts containment over a set that includes the fallbacks. The "usually all zero-wealth" premise is dropped. | MODEL | derivation | REVISED | X010 |
| Y015 | The fallback branch is **not** the reason §2.4 requires a canonical node order; that requirement is stronger and is set by Phase 2. | DESIGN | derivation | REVISED | X011 |

## §1.2 — Supply (lines 148–159)

**UNCHANGED:** C023, C025–C028, V038, V039, V040, V041. No delta claims.

## §1.3 — Demand (lines 161–290) — full-strength extraction

**UNCHANGED:** C031, C032, C033, C035, C036, C039, W023, W024, W026, W030, W031, W032, W033, W042,
W043, W044, W047, W051, W052 *(the superlative at (c) #6)*, X059 *(orphaned — see Obs. 5)*, X060,
X061 §, X062.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y016 | Two provinces with the same **development, trade good and condition** have the same wealth whoever owns them, and a province's wealth does not change when it is conquered. ("Terrain" is dropped from the v3.0–v5.0 formulation.) | MODEL | stipulated | REVISED | W025 |
| Y017 | **Owner-agnosticism is true by construction here, not by a rule that has to be policed.** | DESIGN | stipulated | NEW | — |
| Y018 | v3.0 through v5.0 stated the property and then defended it with a two-test classifier applied to a sweep of the install — a large surface to keep correct, and wrong in every audit that examined it. | WORLD | derivation | NEW | — |
| Y019 | `base_tax`, `base_production` and the trade good are bare attributes of the place, so nothing about them needs classifying. | MODEL | derivation | NEW | — |
| Y020 | *What this gives up:* `gems`' `local_tax_modifier` and `incense`' `trade_value_modifier` are genuinely province-scoped and are **no longer read**, along with great projects, permanent province modifiers and the DLC state they depended on. | DESIGN | derivation | REVISED | X035, X036, X037 |
| Y021 | The deleted apparatus covered **87 of 2,472** provinces. | MODEL | numerical test | NEW | — |
| Y022 | The model trades that fidelity for an input surface with no classification question in it. | DESIGN | stipulated | NEW | — |
| Y023 | `goods_produced(p) = GP_COEFF · base_production(p) · (1 + Σ province-state goods modifiers)` — no flat-bonus term. | MODEL | derivation | REVISED | X018 |
| Y024 | `trade_value(p) = goods_produced(p) · price(good(p))` ducats/year — **no trade-value modifier term at all**. | MODEL | derivation | REVISED | X019 |
| Y025 | `tax_value(p) = TAX_COEFF · base_tax(p) · (1 + Σ province-state tax modifiers)` ducats/year. | MODEL | derivation | REVISED | X020 |
| Y026 | ⚑ The tax tooltip reads `Base: trunc(base_tax / 12) (Yearly base_tax)` — observed `0.49 (Yearly 6.00)` at `base_tax` 6 and `0.16 (Yearly 2.00)` at 2. The parenthetical is `base_tax` itself and the `Base` line its truncated twelfth; it is **not** twelve times the displayed figure, which would give 5.88 and 1.92. | ENGINE | engine test | REVISED | X021 |
| Y027 | v3.0 through v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both of its own data points. | WORLD | derivation | NEW | — |
| Y028 | ⚑§ The monthly production tooltip's `Trade Value` line is **consistent with** the same relation on one observation, 3.52 → `+0.29`, which fixes the divisor only to within **[12.00, 12.14]**. | ENGINE | engine test | REVISED | X022 |
| Y029 | Both monthly figures being the annual value over twelve is what lets the annual forms add directly, and **the tax pair establishes it at two development levels** (the "no conversion" absolute is dropped). | MODEL | derivation | REVISED | W036 |
| Y030 | ⚑§ Observed on Garnatah: `base_tax` 6 with 125.0% displays `Base 0.49` then `0.62`. **0.49 × 1.25 = 0.6125 truncates to 0.61, not 0.62** — so the engine multiplies the untruncated monthly value: 6 × 0.0833… = 0.49999…, × 1.25 = 0.62499…, displayed 0.62. | ENGINE | engine test | REVISED | X027 |
| Y031 | The example establishes the ordering — base from development first, percentage second — **and nothing finer**. | MODEL | derivation | NEW | — |
| Y032 | v3.0–v5.0's reading requires rounding while §2.3 requires truncation; **both cannot hold**. | WORLD | derivation | NEW | — |
| Y033 | Flat goods bonuses *would* add into `goods_produced` before the price multiply — the tooltip carries an additive block above a multiplicative one — but **under §1.3 no source grants one**, so the ordering is stated for the emitter's benefit and is not exercised by any province in the model. | MODEL | derivation | REVISED | X028, X029 |
| Y034 | **Province condition is the one thing besides development and the good that wealth reads:** four static modifiers, all read from `common/static_modifiers/00_static_modifiers.txt`. | MODEL | stipulated | REVISED | X040 |
| Y035 | ⚑ `devastation` grants `trade_goods_size_modifier = -2`, **scaled by the devastation level**, and enters `goods_produced`. | ENGINE | file value | REVISED | X040 |
| Y036 | `prosperity` grants `trade_goods_size_modifier = 0.25` and enters `goods_produced`. | ENGINE | file value | REVISED | X040 |
| Y037 | `under_siege` grants `trade_goods_size_modifier = -0.25` and enters `goods_produced`. | ENGINE | file value | REVISED | X040 |
| Y038 | `occupied` grants `trade_goods_size_modifier = -0.5` **and** `local_tax_modifier = -0.5`, entering both terms. | ENGINE | file value | REVISED | X040 |
| Y039 | **Only `occupied` touches the tax term**; the other three reach `goods_produced` alone. | ENGINE | derivation | NEW | — |
| Y040 | These four are what make the map answer to war: §1.2's volatility, §3.3's besieged province and §2.8's war rows all rest on them. | DESIGN | derivation | REVISED | X040 |
| Y041 | ⚑ **They are not all quiet at the 1444 start.** Ten provinces begin devastated — Bohemia at 50, Erzgebirge and Moravia at 20 — and no province-history file says so. | ENGINE | file value | REVISED | X040 |
| Y042 | ⚑ The devastation is applied by `on_startup`, which fires `flavor_boh.15` ("The Aftermath of the Hussite Wars"); the chain is `common/on_actions/00_on_actions.txt` → `on_startup_effect` → `common/scripted_effects/01_scripted_effects_for_on_actions.txt` → `country_event flavor_boh.15`. | ENGINE | file value | NEW | — |
| Y043 | It costs **13.40 ducats** across the eleven affected counted provinces. | MODEL | numerical test | NEW | — |
| Y044 | **The start state is what the engine produces, not what the history files say** — and it costs three separate reads. | MODEL | stipulated | NEW | — |
| Y045 | ⚑ `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`, `flavor_geo.1` and others, and `flavor_geo.1` carries `add_base_tax`, `add_base_production` *and* `add_devastation` — so development itself can move before the first tick. | ENGINE | file value | NEW | — |
| Y046 | ⚑ **`add_base_*` in a dated block before the start date accumulates**; v5.0 and earlier overwrote instead of adding, silently dropping the grant. | ENGINE | file value | NEW | — |
| Y047 | ⚑§ Province 1 (Uppland) has `base_tax = 5` undated plus 1 at `1436.4.28`; **the game has 6**. | ENGINE | engine test | NEW | — |
| Y048 | ⚑ **`is_city = yes` is not a filter the engine applies.** 20 owned provinces omit or comment out the line — province 265 among them, itself one of the devastated ten — and the engine treats them as cities. | ENGINE | file value | NEW | — |
| Y049 | The model counts a province when it has an owner and lies in a trade node: **2,472** provinces, not 2,452. | MODEL | numerical test | REVISED | X063 |
| Y050 | ⚑ **Twenty counted provinces have no trade good in their history file** (`trade_goods = unknown`); the engine assigns one at start from each good's `chance = { }` block. | ENGINE | file value | NEW | — |
| Y051 | The wealth field is therefore partly the result of one random draw; the model does not predict the draw but reads whatever the game's current state holds, as it does for development. | MODEL | derivation | NEW | — |
| Y052 | `TAX_COEFF = 1.0`'s reference condition is applied to **every province the model counts**: ownership is not modelled, so every province is treated as cored **and settled**. | MODEL | derivation | REVISED | X063 |
| Y053 | *This is a modelling choice with a known cost* — two readings, both on cored city provinces at `base_tax` 2 and 6, are what `TAX_COEFF = 1.0` rests on, and the development range runs past 50. | WORLD | derivation | NEW | — |
| Y054 | `s` and `c` are computed over provinces that **have an owner and lie in a trade node** (v3.0–v5.0: "an owner and `is_city = yes`"). | MODEL | stipulated | REVISED | W050 |

## §1.4 — Market concentration (lines 292–302)

**UNCHANGED:** C040–C047. No delta claims.

## §1.5 — Goods without a graph (lines 304–349)

**UNCHANGED:** C048, C051–C056, V050–V058, W053, W182–W186, W188, W189, W191.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y055 | Repricing to coal the **45** owned latent-coal provinces flips **13 of 159** `Φ_w` edges and adds **217 ducats** to world wealth (`measure6.py`). | MODEL | numerical test | REVISED | X064 |

## §1.6 — The aggregate graph (lines 351–478) — full-strength extraction

**UNCHANGED:** C059, C062, V063, V064, V212, V218, V221, W054, W055, W058, W064, X065 *(now in
tension with Y073–Y075 — see (c) #2)*, X066 *(now in tension with Y065–Y067 — Obs. 6)*, X067, X090,
X091.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y056 | Scale: identical orientation at ×1 and above, **12 edge flips at ×10⁻² and 100 at ×10⁻⁶** — the orientation degrades while the sink set survives, so the sink set is not the quantity to watch. | MODEL | numerical test | REVISED | X068 |
| Y057 | 1444's `b_w` has largest magnitude **0.0226**. | MODEL | numerical test | REVISED | X069 |
| Y058 | Measured at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and `hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12. | MODEL | numerical test | REVISED | X070 |
| Y059 | Phase 1 selects `genua`; both sinks arrive by **stall promotion** and `genua` ends a transit node, so there are **2 promotions and 0 fallbacks**. | MODEL | numerical test | REVISED | X072 |
| Y060 | **Eight sources**, all in the bottom half of the wealth field, `c_w` ranks **44–75**, mean degree **3.1** against the map's 4.0. | MODEL | numerical test | REVISED | X073 |
| Y061 | Every node drains to a sink; acyclic, 159/159 oriented; the **sink set is unchanged under ±1% wealth noise on three seeds**. | MODEL | numerical test | REVISED | X074 |
| Y062 | **90.2%** of ordered node pairs (**5,703 of 6,320**) are connected by at least one good's directed path. Restated at §3.8. | MODEL | numerical test | REVISED | X158 |
| Y063 | Agreement with the per-good graphs is **53.5%** of edge-goods, **52.1%** value-weighted. Restated at §2.8. | MODEL | numerical test | REVISED | X075 |
| Y064 | The superseded marking-order aggregate scored **higher** on that measure; §3.9 records why the trade was taken and **no figure is maintained** for an operator the model does not install. | DESIGN | stipulated | REVISED | X076 |
| Y065 | **`α_Φ = 1.5` is a stipulated design constant, exactly as `P₀ = 2.0` is** — superlinear so that a few very rich provinces outweigh a dense mediocre region, and round. | DESIGN | stipulated | REVISED | X083 |
| Y066 | It is **not** derived and the document no longer offers a derivation: v2.1–v4.0's two-sink calibration was fitted to a field that no longer exists, and v5.0's widest-band ground depended on where the α scan was truncated. | WORLD | derivation | REVISED | X083, X122 |
| Y067 | Scanned over **[1, 8]** rather than [1, 3], the widest band is **1.70** wide (**[3.51, 5.21]**, `{doab, genua, hangzhou}`), and 1.5's is not the widest by any margin. | MODEL | numerical test | REVISED | X078 |
| Y068 | Across α_Φ = 1.00…8.00 at 0.01 the sink set is a step function, and α_Φ = 1.5 sits in the band **[1.38, 1.63], width 0.25**, which gives `{english_channel, hangzhou}`. | MODEL | numerical test | REVISED | X077, X081 |
| Y069 | Sampled at v2's six values the count is non-monotone: **6 → 2 → 1 → 2 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}. | MODEL | numerical test | REVISED | X084 |
| Y070 | A written warning: the 1444 map has two ends and vanilla's authored map has three, and justifying 1.5 by that resemblance is the calibration §2.3 withdrew — **do not**. | DESIGN | stipulated | NEW | — |
| Y071 | **Europe becomes the centre of trade as it develops** — the directional design claim §3.1's first goal asks the field to deliver: at 1444 the map already ends in the Channel and in Hangzhou, and as European development compounds the Channel's basin grows and Asia's pole fades, past a broad range of growth holding no Asian end at all. | DESIGN | derivation | REVISED | X085, X088 |
| Y072 | The mechanism carries it: wealth is linear in development, so developing a region moves its `c_w` share directly and `Φ_w`'s ends follow the wealth. | MODEL | derivation | NEW | — |
| Y073 | Observed (`europe.py`, **824** counted European provinces, α_Φ = 1.5): European development ×1.02 → `{english_channel, hangzhou, wien}`. | MODEL | numerical test | REVISED | X086 |
| Y074 | ×1.56 → `{english_channel, rheinland}`, **Asia holds none**. | MODEL | numerical test | REVISED | X087 |
| Y075 | ×2.00 → `genua` alone. | MODEL | numerical test | NEW | — |
| Y076 | These are **properties of this snapshot, not constants of the model**: what one field yielded under one scaling, and a different world state moves them. | DESIGN | stipulated | REVISED | X088 |
| Y077 | Under (c) **scaling development and scaling wealth are the same operation** — maximum difference **0.0** across the European set — so the distinction that made v5.0's table wrong does not arise. | MODEL | numerical test | NEW | — |
| Y078 | All three institutions the period is named for begin **in Europe** between 1450 and 1550 — Renaissance `1450.1.1` Florence (116), Colonialism `1500.1.1` Sevilla (224), Printing Press `1550.1.1` Frankfurt (1876) — **independently of any threshold**. | ENGINE | file value | REVISED | X089 |
| Y079 | The 1444 Silk Road route from Genoa to the Asian sink: `genua → alexandria → aleppo → persia → lahore → `**`lhasa`**` → ganges_delta → burma → gulf_of_siam → canton → hangzhou`. | MODEL | numerical test | REVISED | X094 |
| Y080 | From the north it is the Volga, and from the Channel the Hansa and the Danube — named without node lists. | MODEL | numerical test | REVISED | X095, X096 |
| Y081 | **No Europe→sink route passes the Cape of Good Hope** — checked from `genua`, `north_sea` and `english_channel`. | MODEL | numerical test | REVISED | X097 |
| Y082 | The Cape is a **live conduit**: in-degree 1, out-degree 3, with **132 ordered node pairs** whose path runs through it, carrying Atlantic drainage into the Indian Ocean. | MODEL | numerical test | NEW | — |
| Y083 | v5.0's "nothing routes through the Cape" is **false as a universal** and was only ever checked on the Europe→sink routes. | WORLD | derivation | NEW | — |
| Y084 | In the per-good graphs the Cape also carries Asian spices to Europe; `Φ_w` models power, not cargo. | MODEL | numerical test | REVISED | X098 |
| Y085 | Scaling the 22 European **nodes** makes `genua` the sole sink from about **×1.65**; the 18-node western/central subset needs about **×2.15**. | MODEL | numerical test | REVISED | X099 |
| Y086 | Somewhere inside roughly **×2.9–×3.5** the Cape **reverses** — Atlantic→Cape→Indian-Ocean becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast. Bounded above as well as below, so a window not a threshold, and its edges move with the field. | MODEL | numerical test | REVISED | X100 |
| Y087 | Dev-stacking a single node's top province concentrates the map on that node; extra sinks at intermediate boosts are expected behaviour, not noise. | MODEL | numerical test | REVISED | X101 |

## §1.7 — Merchants · §1.8 — Collection and transfer · §1.9 — Propagation (lines 480–549)

**UNCHANGED:** C067–C083, C084–C102, C103–C111, V066, V068–V072, V073, W065, W067–W069, W192,
X102, X103, X104. No delta claims. *(See (c) #7 and #8: §1.8's supply-range sentence and §1.9's
"every immediately upstream node" are R2 exposures in unrewritten text.)*

## §1.10 — Direction-dependent systems (lines 551–602)

**UNCHANGED:** C112–C143, V074, V078, V079, V080, W070, W071, X105, X109, X110, X196.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y088 | **Banding absorbs very little chatter** (v5.0: "almost nothing absorbs threshold chatter"). | ENGINE | derivation | REVISED | X106 |
| Y089 | ⚑ Three shipped defines rate-limit the mechanics carrying these thresholds — `TRADING_POLICY_COOLDOWN_MONTHS = 12` (both banded policies), `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30`, `TRADE_COMPANY_COOLDOWN = 60` — so a flickering share does not translate into a flickering *effect* at those three. | ENGINE | file value | NEW | — |
| Y090 | What is left exposed is everything without a cooldown, which is most of the ladder. | ENGINE | derivation | NEW | — |
| Y091 | The caravan cap of 50 is **9.4% to 47.0%** of an inland node's total trade power, median **21.9%** over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. | MODEL | numerical test | REVISED | X107 |
| Y092 | As a share of the node's total **after** the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, median 17.9%; v5.0 quoted those under the first description, **which cannot be right, since 8.6% of 532.0 is 45.8 rather than 50**. | MODEL | derivation | NEW | — |
| Y093 | On §2.2's derived 25-node inland basis only the median moves, to **21.3%**. | MODEL | numerical test | REVISED | X108 |

## §1.11 — Treasure fleets · §1.12 — What the game displays (lines 604–629)

**UNCHANGED:** C144–C148, C149–C165, V049, V065, V081. No delta claims.

## §2.1 — Shape (lines 635–652)

**UNCHANGED:** C167–C184, V082–V085, W072, W073. No delta claims.

## §2.2 — Solver (lines 654–693)

**UNCHANGED:** C185–C209, V091, V092, V229, W075, W076, X115.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y094 | Solver item 4 computes `TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production · (1 + province-state goods modifiers) · price`, with no autonomy, efficiency, ideas or owner terms. | DESIGN | stipulated | REVISED | X111 |
| Y095 | The only modifiers read are the four describing the province's own condition, and **at 1444 only `devastation` is live, on eleven provinces**. | DESIGN | stipulated | REVISED | X112 |
| Y096 | ⚑ **`GP_COEFF` is read from `common/static_modifiers/00_static_modifiers.txt` rather than hardcoded.** | DESIGN | file value | NEW | — |
| Y097 | World wealth is **10,594.70** annual ducats over **2,472** counted provinces. | MODEL | numerical test | REVISED | X113 |
| Y098 | Solve cost is **of order 0.1 s for all 29 goods and single-digit ms per good on average**; repeated runs span 0.09–0.27 s and 3–7 ms with individual goods reaching about 20 ms, so a two-significant-figure range is a statement about a machine and a scheduler and **none is quoted**. | MODEL | numerical test | REVISED | X114 |
| Y099 | v5.0 quoted "0.17–0.21 s"; **twelve fresh runs put only one inside that interval**. | WORLD | numerical test | NEW | — |

## §2.2a — What map this is for (lines 695–735)

**UNCHANGED:** W077–W085, W088, X116, X117 *(its second half is contradicted by Y118 — Obs. 2)*.
No delta claims.

## §2.3 — Constants (lines 737–782)

**UNCHANGED:** C211–C227, V094, W089–W091, W097, W098, X118, X119, X120, X121, X122, X123, and the
DLC-third-axis claim. No delta claims — **§2.3 is the one section `changes-v6.md` never opens, and
it now contradicts §1.6 and §2.2 (Obs. 1).**

## §2.4 — The tradenodes file (lines 784–846)

**UNCHANGED:** C228–C233, C235–C242, V095, V148, W099, W100, W102–W107, W114, X124, X127.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y100 | **The node order is a correctness requirement, not a convention, and the reason is Phase 2 rather than any tiebreak.** | DESIGN | derivation | REVISED | X125 |
| Y101 | Relabelling the nodes and running end-to-end changed the orientation on **580 of 580** runs (29 goods × 20 relabellings), **always** by returning a different optimal vertex and **never** by a sweep tiebreak, with a mean of **22.1 of 159 edges** moving and the objective identical to 8.9e-16. | MODEL | numerical test | NEW | — |
| Y102 | Permuting only the arc presentation order with node labels held fixed changes the optimal support on **10 of 10 goods** tested, objective gaps ≤ 1.8e-15. | MODEL | numerical test | NEW | — |
| Y103 | Twenty-two flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event. | MODEL | derivation | NEW | — |
| Y104 | The canonical order must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks ties in. | DESIGN | derivation | NEW | — |
| Y105 | Everything §1.6 and §2.8 report about stability is measured **at fixed node order**; re-order the same world and the map moves, with `α_Φ` and every input held fixed. | DESIGN | derivation | NEW | — |
| Y106 | The 580/580 result is HiGHS-specific in its detail but not in kind — any simplex returns *a* vertex of a degenerate optimal face. | MODEL | derivation | NEW | — |
| Y107 | Making the orientation independent of presentation order would need a tie-breaking objective — a lexicographic secondary cost or a strictly convex perturbation — which is a design change and is **not adopted**. | DESIGN | stipulated | NEW | — |
| Y108 | The priority key ties in more places than §1.1 documents: besides the free-edge sweep it decides Phase 1's within-cluster argmin, the stall promotion's identical form, and the top-k cut when two clusters carry equal mass. | MODEL | derivation | NEW | — |
| Y109 | **None of them fires on 1444** — zero exact `(DEF, β)` ties on free edges across 29/29 goods, zero within-cluster β ties, zero tied cluster masses — so no measured figure depends on them. | MODEL | numerical test | NEW | — |
| Y110 | End flags: 1444 has **two** end nodes, `english_channel` and `hangzhou`, against vanilla's three. | DESIGN | numerical test | REVISED | X126 |

## §2.5 — Runtime attachment · §2.6 — Writing to the engine · §2.7 — Probes (lines 848–913)

**UNCHANGED:** C243–C250, C251–C272, C274–C293, V098–V101, W108–W114. No delta claims.

## §2.8 — Validation (lines 915–957)

**UNCHANGED:** C298–C342, V109–V112, W116, W117, W119, W195, X128, X130 †, X131, X132, X133 †,
X134, X135, X136, X137. *(X130/X131/X132 are now measured on a superseded field — Obs. 7.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y111 | Sinks are **1 to 8** per good; high-demand nodes are sinks at **16.8%** in the top demand decile against 6.9% in the bottom — a barbell, LP branch ends landing in poor pockets. | MODEL | numerical test | REVISED | X129 |

## §2.9 — Build order · §3.1 — Goals (lines 959–982)

**UNCHANGED:** C343–C352, C353–C365, V113, X138 †. No delta claims.

## §3.2 — Why a flow and a drainage sweep (lines 984–1091)

**UNCHANGED:** C366, C370–C375, C383–C385, V115, V116, V118–V122, V124, V128–V131, W120, W123,
W125–W128, X139, X146, X147, X148, X149.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y112 | **What the ratio metric cannot see is the thing the diagnosis rests on.** Sparsity is the asymmetry — spices are produced in 18 of 80 nodes and cloves in exactly one — so `(c−s)/deg` is dominated by *where* supply exists rather than by how large it is, and a max/min ratio over producing nodes is blind to that by construction. | MODEL | derivation | REVISED | X140, X141 |
| Y113 | On the contrast metric itself the demand side is the wider one, not the supply side (the 36-vs-482.2 spices figures are dropped). | MODEL | numerical test | REVISED | X140 |
| Y114 | Better wealth inputs move Genoa to a *co-*sink at **roughly ×1.7** without making demand the determinant of placement. | MODEL | numerical test | REVISED | X142 |
| Y115 | Moving the spice sink to a Chinese node takes a multiple of that node's demand in the region of **3.6–4.9×** — observed on the 1444 field: `beijing` 3.61×, `hangzhou` 4.12×, `xian` 4.60×, `canton` 4.77×. | MODEL | numerical test | REVISED | X143 |
| Y116 | The multiple a node needs and the share of world demand it then buys do not line up end to end, because the share depends on where the node started; **other nodes in the region need more still** (the four named nodes and their percentages are dropped). | MODEL | derivation | REVISED | X143, X144 |
| Y117 | Sink placement on 1444 is **a measurement on one input, not a theorem**, and v5.0's two rescuing conditions — Phase 0 a no-op and no fallback firing — are **necessary, not sufficient**: T2 satisfies both and still breaks the equality, so the conditioned form is no more a theorem than the bare one. | MODEL | derivation | REVISED | X013, X145 |
| Y118 | First caution on the index-independence measurement: the key reads the **post-fold** balance β, so peeling can *create* exact ties the raw input balances do not have, and the 1444 result does not transfer to a map where Phase 0 acts. | MODEL | derivation | REVISED | X117, X150 |
| Y119 | Second caution: the indexing is load-bearing wherever the key ties — **not only the fallback branch** but Phase 1's within-cluster argmin, the stall promotion's identical form and the top-k cut between equal-mass clusters; none fires on 1444, and **none of them is why §2.4 requires a canonical node order**. | MODEL | derivation | REVISED | X151 |

## §3.3 — Why wealth, and why per province · §3.4 — Why supply is pre-modifier (lines 1093–1126)

**UNCHANGED:** C386–C406, C408, C412, C413, C415–C423, V132, V133, V135, V137–V139, W132–W142.
No delta claims. *(§3.4 retains the v1 `159/159 → 68/159` figure — (c) R3 #2.)*

## §3.5 — Why α is anchored absolutely (lines 1128–1168)

**UNCHANGED:** C427–C442, V140–V144, V147, X152, X153, X156, X157, X179.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y120 | ⚑ **`change_price` values are fractions of the good's base price, not ducats** — the shipped save `tutorial/eu4_tutorial_chapter10.eu4` settles it: `paper` at `current_price = 4.375` on a base of 3.5 (× 1.25, not + 0.25) and `gems` at 5.000 on a base of 4.0. So a −0.25 event takes a 2.5 good to 1.875 and grain and wine reach 0.625. | ENGINE | file value | NEW | — |
| Y121 | ⚑ The install carries **161 textual** `change_price` blocks — 93 `events/`, 14 `missions/`, 1 `common/`, 53 `history/` of which 13 are negative (all in `history/countries/HAB - Austria.txt`), and **none in `decisions/`**. | ENGINE | file value | REVISED | X154 |
| Y122 | ⚑ **Ten of the 161 never execute** — seven inside quoted `effect_tooltip = "…"` strings and three inside `tooltip = { }` display wrappers — so **151 are executable**. | ENGINE | file value | NEW | — |
| Y123 | ⚑ Six of the seven quoted ones duplicate a block already counted in `events/`, and the seventh names a price key no event in the install ever sets. | ENGINE | file value | NEW | — |
| Y124 | All ten are positive and every negative block in the install is executable, so **the 13/2/4/11 partition is identical under either census**. | ENGINE | derivation | NEW | — |
| Y125 | v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them; **both were wrong about which number was the executable one**. | WORLD | derivation | REVISED | X155 |
| Y126 | v5.0 also claimed the scan was "guarded by a per-file count assertion" — **there was no assertion anywhere in its toolchain**; `verify6.py` now carries the guard. | WORLD | derivation | NEW | — |
| Y127 | The reason a plain parse misses these is mechanical: `pdx.py` tokenises a quoted string as one opaque unit, so a `change_price` inside a tooltip string is invisible to the walker. | MODEL | derivation | NEW | — |

## §3.6 — Why no hysteresis · §3.7 — Why eligibility is per good · §3.8 — Why gates evaluate true (lines 1170–1233)

**UNCHANGED:** C443–C446, C449, C452, C463–C473, C474–C497, V148, V152, V154–V158, W147–W152,
W154. No delta claims — §3.8's 90.2% is Y062 at first appearance in §1.6.

## §3.9 — Why `Φ_w` is the installed graph (lines 1235–1277)

**UNCHANGED:** C502, C505–C510, C512, V160, V161, V162, V220, V228, X159 *(measured on the
superseded field — Obs. 7)*, X161, X162 *(now false against Y058 — Obs. 6)*, X163 *(an R3
violation — (c) R3 #1)*.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y128 | `Φ_ord` is acyclic for free and scores **higher** than `Φ_w` on self-coherence — the cost of the trade, not disputed — and was superseded on design grounds: its ends are sweep-scheduling artifacts rather than places, **a majority** terminate no good at all, none of the demand capitals is among them, and the end count does not concentrate as demand concentrates. *No figure is maintained for it.* | MODEL | derivation | REVISED | X076, X160 |

## §3.10 — Why the engine's economy is overwritten (lines 1279–1295)

**UNCHANGED:** C513–C521, C523–C525, C528–C530, X164, X165, X167.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y129 | Reading the one installed graph leaves the propagated term good-independent, so the identity survives untouched — worst relative disagreement 0 to 3.7e-16, **one to three units in the last place, not the single ULP v5.0 claimed**. | MODEL | numerical test | REVISED | X166, X168 |
| Y130 | `gulf_of_siam`'s 29 goods leave it by **seven** distinct downstream sets. | MODEL | numerical test | REVISED | X169 |
| Y131 | Per-good propagation destroys the **exactness**: once downstream sets differ, a country's power at the node is no longer one number, `powershare_C` no longer factors out, and a single node scalar cannot reproduce every collector's income exactly. **That is the whole of the claim, and it is about exactness, not magnitude.** | MODEL | derivation | REVISED | X170, X171 |
| Y132 | Substituting the share at one arbitrarily chosen reference commodity gives per-collector errors up to **+7.4%** at `sevilla`, and sweeping which commodity is chosen moves that collector's error across a **17.8-point** range — so those figures measure the arbitrary choice, not the design. | MODEL | numerical test | REVISED | X170 |
| Y133 | Substituting the quantity an implementation would actually store — the **value-weighted mean share** across the node's goods — the error is **at most 0.1%** at every node measured (`sevilla`, `champagne`, `genua`, `malacca`, `gulf_of_siam`). | MODEL | numerical test | NEW | — |
| Y134 | The honest statement: per-good propagation costs the exact identity and buys a per-node error a reasonable scalar keeps within a tenth of a percent, and **the identity is what Goal 7 is stated in terms of**. | DESIGN | derivation | NEW | — |
| Y135 | v4.0's 0.41% and v5.0's "redistributive and single-digit percent" were **both** artifacts of freezing the share at one commodity — v5.0 having correctly diagnosed exactly that defect in v4.0. | WORLD | derivation | REVISED | X174 |
| Y136 | The construction behind any such figure — which countries collect, which transfer, and which commodity's share is frozen — has to be stated with it, and **none of those documents stated it**. | DESIGN | stipulated | REVISED | X172 |

## §3.11 — Caravan power · §3.12 — Treasure fleets · §3.13 — Open questions · §3.14 — AI merchants (lines 1297–1413)

**UNCHANGED:** C531–C547, C556–C560, C561–C585, C586–C624, V163–V175, V178, V181–V183, W164,
X175, X176, X177 §, X178, X180, X181, X182, X183, X184. No delta claims — the only §3.13 edit was
the banner ("Open in the **v6.0** wealth model"), which is not a proposition change.
**§3.13 is where the deleted apparatus survives (Obs. 3) and where X182's 30.4 is stale (Obs. 7).**

## §3.15 — Rejected (lines 1415–1523)

**UNCHANGED:** C625–C672 as carried by v2, V184–V188, V192–V199, V226–V228, X189.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| Y137 | With v1's ε floor removed the contrasts run **4–97 on supply against 211–15,010 on demand** over the **28** goods produced in more than one node, so the demand side is the wider one; `cloves` has a single producer and no contrast to measure, which is the sparsity point in miniature. | MODEL | numerical test | REVISED | X185 |
| Y138 | v3.0 **and v4.0** repeated the 10⁷ / 10²–10³ ratio here while **v4.0's own §3.2** was withdrawing it. | WORLD | derivation | REVISED | X186 |
| Y139 | Ranked orientation puts **a far higher share** of top-demand nodes in its sink sets than DRAIN does (the ρ_val and decile figures are dropped) and fails on delivery: 83.0% of demand reachable, 31 orphan sinks. | MODEL | numerical test | REVISED | X187 |
| Y140 | It posts 8 net-producer sinks where DRAIN, LAP and FLOW post zero, and **10–16** sinks per good against DRAIN's **1–8**. | MODEL | numerical test | REVISED | X188 |
| Y141 | The 3-mass gravity kernel **reproduces whatever end count it is seeded with while γ is small enough, and loses that property as γ approaches 1**; *no figures are maintained for it*, and it is rejected on three non-numeric grounds — it pins the count by fiat, it needs a second reach knob γ, and a pure `wealth^α` comparison with no reach term does not concentrate ends at all. | MODEL | derivation | REVISED | X190, X191 |
| Y142 | `Φ_ord`'s graveyard entry keeps its argument and loses its numbers: *no figures are maintained for it*, and the self-coherence ceiling v2.0 and v2.1 quoted predates the deterministic sweep of §3.6 and was never regenerated after it. | MODEL | derivation | REVISED | W063 |

## §3.16 — Evidence standard (lines 1525–1587)

**UNCHANGED:** C677, C680–C682, C684, C685, V200–V204, V206–V210, W173–W181. No delta claims.
*(Retains the v1 `1e-5` identity failure — (c) R3 #3.)*

---

# Observations

Recorded, not fixed. These are properties of the v6.0 text as extracted.

### 1. §2.3 was never opened, and now contradicts §1.6 and §2.2 in three ways

None of the 45 replacements touches §2.3's constants prose. As a result:

- **The withdrawn justification is still asserted.** §2.3 l.773: *"1.5 is retained because it sits
  inside the **widest** sink-count band and nothing now selects a different value"* — the exact
  ground §1.6 l.405-408 withdraws (*"1.5's is not the widest by any margin"*). `fixes-agreed`'s A1
  says §2.3 is where the stipulation gets recorded; §1.6 twice says *"§2.3 governs recording it"*
  and *"the calibration §2.3 withdrew"*. §2.3 records neither.
- **§2.3 asserts the opposite of §1.6 about the map itself.** §2.3: *"on the corrected wealth field
  of §1.3 it does not yield that map"* (the two-sink `hangzhou`/`english_channel` map). §1.6 Y068:
  α_Φ = 1.5 sits in the band that **does** give `{english_channel, hangzhou}`.
- **§2.3 cross-references a deleted analysis.** *"the α_Φ window that does yield it is narrower than
  the uncertainty in its own edges under ±1% wealth noise (§1.6)"* — §1.6's 8-seed noise study and
  its band table were both deleted in replacement 9, so the pointer resolves to nothing.
- **`GP_COEFF`'s provenance now has two incompatible statements.** §2.2 item 4 (Y096): *"`GP_COEFF`
  is **read from** `common/static_modifiers/00_static_modifiers.txt` rather than hardcoded"*. §2.3:
  *"The two wealth coefficients of §1.3 are **hardcoded in the binary** … They are therefore
  measured."* §1.3 l.192-194 agrees with §2.3: *"neither is a define … so both are engine constants
  recovered by observation."* The contradicted rows are **W031**, **W032** and **X118**, all carried
  UNCHANGED; `fixes-agreed` R1 backs §2.2 and names the key (`provincial_production_size`).

### 2. Two sections still assert propositions §3.2 withdraws in the same version

- **§1.1 l.111-113** states the conditioned sink-set equality (*"On a map where Phase 0 is a no-op
  and no fallback fires … the sink set is exactly …"*) and then, four lines later, gives T2 as a
  counterexample inside the 2-core. §3.2 Y117 says exactly that the conditions are *necessary, not
  sufficient* because T2 satisfies both. §1.1 was patched at the fallback paragraph and the sink
  counts but not here.
- **§2.2a's Phase-0 table** row for free-edge determinism reads *"same in both halves — peeling does
  not touch the priority key"*. §3.2 Y118 says peeling can **create** exact ties the raw balances do
  not have and that the 1444 result does not transfer where Phase 0 acts.
- Minor: §1.1 and §2.2a write the key as `(DEF, b)`; §2.4 and §3.2 now write `(DEF, β)` and say the
  distinction is what the measurement is about.

### 3. §3.13 keeps the apparatus §0 and §1.3 delete

§3.13's open question still reads *"§1.3's **whole-install sweep** settles the additive block too:
**fifteen** 1444 provinces carry a flat `trade_goods_size`, **five from great projects and ten from
permanent province modifiers**"*, and *"each source needs the **§1.3 locality test** applied to it"*,
and cites `bonus_from_merchant_republics` as a classified example. §1.3 says *"under §1.3 no source
grants one"* and §0 says the sweep, the projects, the permanent modifiers and the classifier are all
deleted. Six claims the checklist marked MOOT (X029, X030, X033, X045, X176, X179) survive here.

### 4. §3.10 contradicts itself two paragraphs apart

L.1290: *"the two forms agree to a worst relative disagreement of 0 to 3.7e-16 — **at most one unit
in the last place**."* L.1292: *"worst relative disagreement 0 to 3.7e-16 — **one to three units in
the last place, not the single ULP v5.0 claimed**."* Replacement 32 fixed the second occurrence only,
so the sentence correcting v5.0 sits directly beneath the v5.0 claim it corrects.

### 5. "Not local" survives without the rule that defined it

§1.3 l.269: *"Everything the engine itemised on a real province that is **not local** is excluded by
**this rule**."* Both tests that defined "local" are deleted, and the rule now in force is the
three-inputs rule, which does not use the word. X059 is UNCHANGED as a proposition and orphaned as a
justification.

### 6. Three §1.6/§3.9 sentences survive the change of result they were written for

- §1.6 l.366: *"Their count is set by `α_Φ`; only their locations are emergent"* — contradicted by
  §1.6's own Europe table (count 2 → 3 → 2 → 1 at fixed α_Φ) and by §2.4 item 2.
- §1.6 l.369-370: *"the count is a step function of it (**the band table below**) … the ground on
  which 1.5 is *retained* is **the band table** and not that target"* — there is no band table in
  §1.6 any more; the only table is the Europe one, and the new paragraph says the retention ground
  is a stipulation, not a band.
- §3.9 l.1266-1270: *"On the corrected wealth field there is **one end, in China**, matching none of
  vanilla's three … **7.8 points** of self-coherence given up"* — the one-sink result is reversed by
  Y058, and 7.8 is a maintained `Φ_ord` gap under R3, computed from two figures this version
  deleted.

### 7. Figures carried across the field change without regeneration

The (c) field moves world wealth from 10,677.50 to 10,594.70 and adds 20 provinces, so node wealths
move. These were not re-measured:

- §3.9 (X159): `genua` 296.0, `gulf_of_siam` 299.2, `sevilla` 266.5, `english_channel` 316.6 —
  identical to v5.0. This is the same sentence v5.0's own Observation 2 flagged for exactly this
  reason.
- §2.8 Razed China (X130–X132): the baseline sink set is given as `{hangzhou}`, `hangzhou`'s `c_w`
  rank as **1**, and its node wealth as **245.0** against `beijing`'s 143.8. §1.6 Y058 gives two
  baseline sinks, `hangzhou` at `c_w` rank **3** and node-wealth rank **12** — and 245.0 against
  §3.9's 316.6 top figure cannot be a rank-12 wealth.
- §3.13 (X182): `hangzhou` holds the richest single province *"at 30.4 against Beijing's 19.5"*.
  `fixes-agreed` §1 pre-confirms the (c) value as **27.00**.

### 8. Ten figures carry no script, against §0's own promise

§0: *"Measured figures carry the script that produced them."* Without one: 0.98% and 87 of 2,472
(§0, §1.3); 13.40 ducats (§1.3); 12 and 100 edge flips (§1.6); 132 ordered node pairs (§1.6);
580/580, 22.1 of 159, 8.9e-16, 10 of 10 and 1.8e-15 (§2.4); 16.8% / 6.9% (§2.8); 3.61/4.12/4.60/4.77
(§3.2); +7.4%, the 17.8-point range and 0.1% (§3.10). `measure6.py` is named in §1.1, §1.5 and §1.6,
and `europe.py` in §1.6.

### 9. Ten devastated provinces, eleven affected

§1.3 says *"**Ten** provinces begin devastated"* and, three lines later, *"It costs 13.40 ducats
across the **eleven** affected counted provinces"*; §2.2 says *"only `devastation` is live, on
**eleven** provinces"*. §1.3 also says province 265 *"is also one of the devastated ten"*, so the
eleventh is unaccounted for in the document.

### 10. One E-series finding did not reach the spec

`fixes-agreed`'s E-series records that `highest_power` **is** the strongest single province's power
(matching `max(country province_power)` on 17 of 79 nodes, strictly less on 62). §1.10 still reads
*"What it does hold was not determined and the model does not read it"* (X196, UNCHANGED).

### 11. `changes-v6.md` mislabels one replacement

Entry 45 (`R14-conn`) is headed §2.6; the text it replaces (the 90.2% reachability census) is in
**§3.8**. The spec is correct either way; only the change log's section label is off.

---

# † Unresolvable IDs

**None introduced by this pass.** Four IDs that `claims-v5.md` carried as UNCHANGED were resolved by
grepping `claims-v3.md` and are used directly above: **W025** (two provinces with the same terrain,
development and trade good), **W036** (both monthly figures are annual/12, so the annual forms add
directly), **W050** (unowned provinces are outside the model; `s` and `c` over owner + `is_city`),
**W063** (v2's 62.7% predates the deterministic sweep).

Three † markers are **inherited** on rows that remain UNCHANGED in v6.0 and are not re-resolved
here, since their targets live in `../v1-laplacian/claims.md`: **X130** and **X133** (§2.8's Razed
China and Ming rows, believed C298–C342) and **X138** (§3.1's Goal 1 example, believed C353–C365).
