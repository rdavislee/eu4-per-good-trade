# Claim Inventory Delta — Per-Good Trade Network Spec v5.0

Extracted from `per-good-trade-spec.md` (v5.0, 1,498 lines) as a **delta against
`../v3-owner-agnostic/claims-v3.md`** (W001–W195), which is itself a delta against
`../v2-drain/claims-v2.md` (V001–V230) and `../v1-laplacian/claims.md` (C001–C685).
Extraction only: nothing here is validated, corrected, or commented on except where the brief
asks for observations.

**Method.** Four documents were read in full: the v5.0 spec, `claims-v3.md`, the **v4.0 spec**
(`../v4-owner-agnostic/per-good-trade-spec.md`), and `changes-v5.md`. Because **v4.0 never got a
claims file**, the v3.0→v4.0 and v4.0→v5.0 text diffs were computed and read line by line, so that
every v5.0 proposition can be dated to the version it entered. `claims-v2.md` and `claims.md` were
grepped to resolve specific IDs. Every row below was read off the v5.0 spec text itself;
`changes-v5.md` was used only to locate changed passages and is not a source for any claim.

**ID prefix.** v1 used `C`, v2 used `V`, v3 used `W`, v4 got none. **v5 uses `X`**, numbered in
document order.

**Statuses.** UNCHANGED — same proposition as an existing C/V/W ID; the old ID is recorded and no
X ID is issued. REVISED — the proposition changed; new X ID with the old ID(s) in `Replaces`.
NEW — no counterpart in any prior inventory. A proposition stated in two sections keeps one ID at
first appearance. Adding or removing an inline `[unverified in vN]` marker is **not** a
proposition change.

**Vocabularies carried over.** Type: ENGINE / MODEL / DESIGN / OUTCOME / WORLD. Provenance:
stipulated / derivation / file value / numerical test / engine test / prose source /
verified (method unstated) / UNSOURCED. `numerical test` (a solver experiment) and `engine test`
(an observation of EU4 running) are kept strictly distinct.

**Full-strength sections**, extracted row-by-row regardless of overlap, per the brief: **§1.3**
(the wealth definition and the modifier-classification table) and **§1.6** (the installed
aggregate map, its sink/source figures, the α_Φ band table, and the Europe/institution
demonstration).

**Markers.** **⚑** a row that introduces a new engine fact no prior inventory carried.
**§** a row whose stated evidence is a single observation. **†** a row whose `Replaces` target
could not be resolved to a specific ID.

**Origin column.** Each NEW row is dated `v4` (the proposition entered in v4.0 and had nowhere to
be recorded) or `v5` (it entered in v5.0). REVISED rows note where the revision landed when the
distinction matters.

---

# Summary

**196 delta claims extracted, X001–X196**, against the 195 v3 claims and 230 v2 claims:
**106 NEW, 90 REVISED** (replacing **67 W IDs, 27 V IDs, 3 C IDs, and 2 unresolved C-ranges** —
99 distinct prior IDs in all).

Of the 106 NEW rows, **32 entered in v4.0** and are recorded here for the first time because v4.0
was never inventoried; **74 are v5.0's own**.

### Delta claims by status and Type

| Type | NEW | REVISED | Total |
|---|---|---|---|
| MODEL | 42 | 53 | 95 |
| ENGINE | 30 | 21 | 51 |
| DESIGN | 21 | 14 | 35 |
| WORLD | 12 | 2 | 14 |
| OUTCOME | 1 | 0 | 1 |
| **Total** | **106** | **90** | **196** |

### Delta claims by Provenance

| Provenance | Count |
|---|---|
| numerical test | 72 |
| derivation | 60 |
| file value | 29 |
| stipulated | 21 |
| engine test | 14 |
| UNSOURCED | 0 |
| **Total** | **196** |

**No row in this delta carries UNSOURCED provenance**, which is what the v5.0 header claims for
itself. One caveat survives as an observation at the end: the carried-over UNCHANGED claim W071 is
still typed UNSOURCED even though v5.0 now measures its first clause.

**43 rows are marked ⚑** — new engine facts; **29 of them are NEW** rows, and **21 of those 29
sit in §1.3 alone**, which is where v5.0's whole-install sweep and v4.0's tooltip re-measurement
both land.

**Five rows are marked §** — evidence resting on a single observation: X022, X025, X027, X061,
X177. That is down from v3.0's 19, because v4.0 re-measured both wealth coefficients across four
and two provinces respectively and repeated the cycle crash a third time, and because the final
text replaced X110's single reading with a 79-of-79-node parse.

### Where the delta concentrates

| Section | X rows | What drove it |
|---|---|---|
| §1.3 Demand | 46 | the whole-install modifier classification (v5.0) plus v4.0's two-test rule and tooltip re-measurement |
| §1.6 Aggregate graph | 41 | one sink instead of two, the α_Φ band table, the Europe demonstration, the 1444 route geography |
| §1.1 Trade direction | 13 | the fallback branch and its reachability analysis |
| §3.2 Why a flow and a sweep | 13 | T3, the sparsity argument, regenerated Chinese-sink thresholds |
| §3.10 Income factoring | 11 | the identity/measurement split (v4.0) and the per-good propagation re-measurement (v5.0) |
| §2.8 Validation | 10 | regenerated rows and the fallback-widened sink assertions |
| §3.13 Open questions | 9 | two of three wealth questions settled and moved into §1.3 |
| §3.15 Rejected | 7 | every rejected-operator figure regenerated on the corrected field |
| §1.10 | 7 | the caravan re-measurement and the `highest_power` parse |
| §2.3 | 6 | the coefficient re-measurement and α_Φ's withdrawn calibration |
| §3.5 | 6 | the `change_price` census reopened twice |
| §2.2 Solver | 5 | the whole-install wealth pipeline and the measured solve cost |
| §3.9 | 5 | the `Φ_w` adoption rationale restated |
| §0, §2.4 | 4 each | |
| §2.2a, §1.8 | 2 each | |
| §1.5, §1.7, §3.1, §3.8, §3.14 | 1 each | |

---

# (a) Which propositions stand on no replaced predecessor?

`changes-v5.md` puts "Propositions standing on no replaced predecessor" at **0**, and states that
"no proposition in v5.0 stands on its own — each one either replaces a graded predecessor or
refines a claim whose predecessor was replaced." Derived independently, that is **almost right and
not exactly right**.

**The finding: the DRAIN fallback branch stands on no replaced predecessor.** V022 said "on a
stall, promote the heaviest flow-terminal demander into the sink set." v4.0 kept that sentence
intact and *appended* a second branch — "if the candidates hold no flow-terminal demander at all,
promote the highest-wealth candidate instead, ties by index." Nothing was replaced; a case that no
prior version's algorithm covered was added to Phase 3. v5.0 then built four further propositions
on top of that addition (X008–X011: when the branch is reachable, on which graphs, what decides
there, and what that forces on the emitter). So **X005–X011 — seven rows, four of them v5.0's own
— are a free-standing addition to the algorithm's definition**, not a repair of anything graded
wrong. They are the answer to "which property of the output does this spec still not state?" that
§3.16 asks for, which is why they read as a repair; but the predecessor they repair is an
*absence*, not a claim.

Everything else does fall into the author's three cases. Below, every NEW row with its case.

### Case 1 — inherited from v4.0, no inventory entry (32 rows)

These propositions entered in v4.0. They are NEW here only because v4.0 was never extracted.

| Rows | Subject |
|---|---|
| X005, X006, X007 | the fallback branch itself, its no-bootstrap argument, and the definition of *candidates* — **also free-standing, see above** |
| X014 | T3 as a third case breaking sink-set equality |
| X024, X025, X026 | ⚑ only the tooltips' `Base` lines are usable; the `Industrious` ruler personality explains Garnatah's window; personalities are rolled at game start |
| X030, X031 | the two tests: *local*, and *enters wealth* |
| X036, X037 | ⚑ 43 gems provinces, 29 incense provinces |
| X041, X042 | glass and chinaware classified out of wealth |
| X045 | ⚑ `bonus_from_merchant_republics` (`eu4.exe:0x1cc7128`) is not local |
| X058 | glass and chinaware are the whole of the rule-versus-vocabulary tension |
| X061, X062, X063 | ⚑ the tax multiplier is the sum of itemised percentages; a cored city sums to 1.00; every counted province is a treated-as-cored city |
| X104 | ⚑ no string, define or modifier ties trade range to link flow |
| X107 | the caravan cap is 8.6–32.0% of an inland node's power |
| X115 | "milliseconds each" holds with a generic LP; no projection is offered |
| X120 | ⚑ the displayed monthly tax is the truncation of `base_tax × 0.083333` |
| X134 | ⚑ the 8.96% run-to-run drift is over five named node fields |
| X140, X141 | the spices supply/demand ratio with the ε floor removed; sparsity is what survives |
| X144 | `girin`, `yumen`, `chengdu`, `lhasa` need 4.0–10.8× |
| X146, X149 | T3 worked in full; the narrow containment set would halt on correct behaviour |
| X156, X157 | ⚑ `NEW_DRAPERIES` at −0.25 → 1.875; v2's 13 was right and v3.0 reached 12 by parsing four of five trees |
| X167 | 5.7e-14 and 1.4e-14 are residuals of an exact identity |
| X176 | ⚑ the unenumerated `trade_goods_size` surface |

### Case 2 — refines a claim whose predecessor was replaced (70 rows)

| Rows | Refines / replaced claim |
|---|---|
| X002, X003 | the whole-install classification and the one-sink result — W041 ("exactly three"), V215 (two sinks) |
| X033, X034 | W041 / v4.0's "exactly two" |
| X040 | V038, extended from "these four keys exist" to their values, their tax-side effect, and their 1444 state |
| X038, X039, X043, X044, X046 | W041 — outputs of the sweep that replaced it |
| X048, X049, X050, X051, X052, X053, X054 | W041 — the great-project and permanent-modifier enumerations |
| X055, X056, X057 | W041, and the UNCHANGED DLC-third-axis claim |
| X066, X067 | V213 (the α_Φ calibration) and V224 (emergent count) |
| X071 | V215 |
| X077–X082, X192–X195 | V224 — the band table and its noise analysis, replacing "the count emerges from concentration" |
| X085, X086, X087, X088, X092, X093 | V215/V224 — the Europe demonstration that the one-sink result required |
| X089, X090, X091 | ⚑ the institution file facts imported for that demonstration |
| X094, X095, X096, X097, X098 | V215 — the 1444 route geography offered as evidence for the one-sink map |
| X108, X109, X110, X196 | the v4.0 caravan comparison (refuted) |
| X112, X113 | W041, W074 |
| X123 | V213 |
| X125, X151 | W130 ("the index never decides") |
| X127 | the v3.0/v4.0 two-end-node count |
| X131, X132 | the v3.0 Razed-China row |
| X155 | W146 (the `change_price` census) |
| X162, X163 | V220 (the `Φ_w` adoption rationale) |
| X165, X169, X171, X172, X173, X174 | C522, C526, C527 (§3.10's residuals and the 5.96-ducat figure) |
| X186 | V117 (supply contrast 10⁷) |
| X191 | W190/V225 (the gravity kernel) |

### Case 3 — genuinely free-standing (4 rows, plus the 3 v4.0 rows above)

**X008, X009, X010, X011** — v5.0's analysis of when the fallback branch is reachable, on which
graphs, what decides there, and why that makes emitter node order a correctness requirement. They
refine X005–X007, which replaced nothing. This is the one place v5.0 adds subject matter that
attaches to no graded predecessor at all.

### ⚑ NEW rows that name a new fact about EU4 (the case the brief singles out)

**29 of the 43 ⚑ rows are NEW**, and they are not evenly spread. The heaviest concentration is
§1.3's whole-install sweep, which imports facts about great projects, permanent province
modifiers, centers of trade, `production_leader`, buildings, static-modifier values, and the
Leviathan DLC gate — **none of which any prior inventory carried in any form**:
X038, X039, X040, X042, X043, X044, X045, X046, X048, X050, X051, X054, X055, X056.
The rest: X024, X025, X026 (tooltip semantics), X036, X037 (province counts), X061, X062 (the tax
multiplier decomposition), X089, X090 (institution start data), X104 (the trade-range file
sweep), X110 (the `highest_power` save field), X120, X134, X156, X176.

*(The other 14 ⚑ rows are REVISED — X021, X022, X023, X027, X029, X047, X060, X103, X105, X118,
X119, X124, X154, X177 — and each carries a new engine observation attached to a graded
predecessor.)*

**Observation on the author's framing.** `changes-v5.md`'s "v5.0 adds no new subject matter" is
defensible about *sections* and not about *facts*. Great projects, permanent province modifiers,
centers of trade, buildings-at-1444, the Leviathan gate, and the three institutions' start dates
and provinces are all subject matter the document did not previously contain, imported in v5.0.
Every one of them is sourced, and every one of them is unaudited.

---

# (b) Which prior IDs does v5.0 leave stranded?

**Eight** propositions are withdrawn — stated to be wrong, or deleted without replacement. Each is
verified against the v5.0 spec text below. As first extracted, four of them (marked ✚) were absent
from `changes-v5.md`'s account; the final text now carries all of them in an explicit withdrawal
table. A ninth candidate, **W004**, is **not** withdrawn — see the note under the table.

| Withdrawn ID | What it said | The v5.0 text that withdraws it |
|---|---|---|
| **V213** | α_Φ = 1.5 is "calibrated once so the 1444 start yields the hangzhou/english_channel two-sink map" | §2.3: *"**Its stated calibration is withdrawn.** v2.1 through v4.0 said 1.5 was 'calibrated so the 1444 start yields the two-sink hangzhou/english_channel map'; on the corrected wealth field of §1.3 it does not yield that map."* Replaced by X122/X083. |
| **V215** | two sinks at 1444, `hangzhou` and `english_channel`, both arriving by stall promotion, Phase 1 selecting `genua` | §1.6: *"**one sink, `hangzhou`** … Phase 1 selects `hangzhou` directly, so there are **0 promotions and 0 fallbacks**. *(v2 through v4 reported two sinks. That result was measured on a wealth field missing the sixteen provinces §1.3 now carries; correcting the field removes it.)*"* Replaced by X070/X072. |
| **V224** | the `Φ_w` sink count "is emergent … it tracks how many world-class wealth poles the flow separates, not α itself" | §1.6: *"**Their count is set by `α_Φ`; only their locations are emergent.** v2.0 through v4.0 said the count 'emerges from concentration exactly as per-good sink counts do' — it does not."* Replaced by X065/X084. |
| **V117** | supply contrast (10⁷) exceeds demand contrast (10²–10³) by four to five orders of magnitude | §3.15: *"that ratio was `max(s)` over v1's ε floor, and with the floor removed the contrasts run **4–97 on supply against 211–20,400 on demand** across the 29 goods — **the demand side is the wider one**."* Replaced by X139/X186. |
| **W145** ✚ | "The boundary is `< 2.0`, and three goods sit on it exactly — the likely origin of v2's off-by-one" | §3.5: *"v2's 13 was right; v3.0 reached 12 by parsing four of the five trees."* The off-by-one had a different cause; W145's explanation is deleted and its premise (three goods on the boundary) is refuted — v5.0 says two. Withdrawn in **v4.0**, unreplaced. |
| **W158** ✚ | Open question: do flat goods bonuses exist at 1444? *"no 1444 province was observed carrying one"* | §1.3: *"**Fifteen** 1444 provinces do carry a flat bonus in the first block."* §3.13: *"§1.3's whole-install sweep settles the additive block too."* Refuted; replaced by X029. |
| **W066** ✚ (half) | trade efficiency *"also feeds the caravan-power and collection tooltips"* — v3.0's only UNSOURCED ENGINE row in §1.7 | The clause is gone. v4.0 replaced it with a ledger-column argument; **v5.0 deleted that too**, leaving §1.7 with only *"trade efficiency and a flat income bonus are different quantities in EU4, and the define's own shipped comment settles which this one is."* The supporting proposition is withdrawn without replacement in either direction. |
| **V217** (half) ✚ | `Φ_w` under ±1% noise is *"stabler than any per-good graph"* | §1.6 retains *"0 edge flips and 0 sink-set changes under ±1% wealth noise across 5 seeds"* and drops the comparative clause. The measurement survives; the comparison does not. |

**W004 is subsumed, not withdrawn.** The header clause "four v1 corrections that v2 never applied
are folded in with them" is gone, but the lineage paragraph still carries V004 — *"Every
claim-audit correction from `../v1-laplacian/validation.md` settleable from files is folded in
here"* — and X001 generalises the fold-through to all four audits. V004 entails W004's content, so
the count is gone and the proposition is not. Recorded as a correction to this file's first pass.

**Two further withdrawals have no inventory ID at all**, because their only statement was in
v4.0: the fallback branch's rationale *"it is what a pocket with no net demander needs"* (deleted
in v5.0, and X008–X011 replace it with a much narrower reachability condition), and *"under the
18-node set alone … the Cape reverses at ×2"* (deleted; v5.0's X100 gives a ×3–×3.75 band for the
22-node set only).

**Not stranded, though `changes-v5.md`'s framing might suggest it:** W005 (the four game probes)
lost its header sentence but survives in full at §2.7; W064 (transient extra sinks are expected
behaviour) survives in §1.6's last paragraph; V038 survives at §1.2 and is *extended* at §1.3
(X040), not replaced.

---

## §0 — Front matter (lines 1–24)

**UNCHANGED:** C002, C003, C004, V001 *(via §2.5)*, V002, V003, W001, W002.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X001 | v5.0 folds through every refuted and partial claim from **all four audits to date, including v4.0's own**. | WORLD | stipulated | REVISED | W003 |
| X002 | v5.0's substantive change is to §1.3: the local-modifier classification is applied to the **whole install** rather than to the trade-good tables alone, which adds sixteen provinces. | DESIGN | stipulated | NEW *(v5)* | — |
| X003 | That change moves the aggregate graph from two 1444 sinks to one. | MODEL | numerical test | NEW *(v5)* | — |
| X004 | **No figure in v5.0 is unverified**, and the one place the document declines to project a number says so in place. | DESIGN | stipulated | REVISED | W006 |

## §1.1 — Trade direction (lines 29–128)

**UNCHANGED:** C005, C006, C010–C012, C019–C022, V005–V015, V017–V024, V026–V028, V031, V032,
V036, V037, W007–W011, W015–W022.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X005 | **Fallback branch:** if the candidates at a stall hold no flow-terminal demander at all, promote the **highest-wealth** candidate instead, ties by node index. | MODEL | stipulated | NEW *(v4)* | — |
| X006 | Node wealth is a good-independent input, so the fallback needs no bootstrap. | MODEL | derivation | NEW *(v4)* | — |
| X007 | *Candidates* at a stall are the unmarked nodes whose flow out-neighbours are all marked; the flow subgraph is acyclic, so at least one always exists and the sweep always advances. | MODEL | derivation | NEW *(v4)* | — |
| X008 | The fallback fires only when every candidate is support-isolated with zero balance — on a connected core, only when `b ≡ 0` across it — because a candidate with a flow out-arc is already *ready* and one with inflow is a flow-terminal demander. | MODEL | derivation | NEW *(v5)* | — |
| X009 | That happens for the aggregate graph on a uniform-wealth map, and for a per-good graph on a component with no producer and no consumer. | MODEL | derivation | NEW *(v5)* | — |
| X010 | In those cases the candidates are usually all *zero-wealth*, the wealth key ties, and the **node index decides**. | MODEL | derivation | NEW *(v5)* | — |
| X011 | That is why §2.4 item 1 makes a canonical emitter node order a correctness requirement rather than a convention, and why §2.8 asserts containment over a set that includes the fallbacks. | DESIGN | derivation | NEW *(v5)* | — |
| X012 | Every sink is a selected flow-terminal demand centre, a stall-promoted flow-terminal demander, a **fallback-promoted highest-wealth node**, or a Phase-0 pendant that absorbed a net-importing subtree. | MODEL | derivation | REVISED | W012 |
| X013 | Where Phase 0 is a no-op **and no fallback fires**, the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods on 1444, **1–7 sinks per good**, mean 3.6, **zero fallbacks**. | MODEL | numerical test | REVISED | W013, V030 |
| X014 | **T3:** a fallback promotion is a sink that is neither selected nor stall-promoted, so it breaks the equality inside the 2-core. | MODEL | numerical test | NEW *(v4)* | — |
| X015 | Ready-marking is a monotone closure, so the stall sequence and **both promotion branches** are provably scheduling-independent — each reads only the candidate set, which the closure fixes. | MODEL | derivation | REVISED | V033 |
| X016 | Free-edge direction is **deterministic** by construction; that it is a function of the graph and the balances *alone* — that the node indexing never decides — is **measured, not proved**, and holds exactly where the key has no exact ties. | MODEL | derivation | REVISED | V034, W130 |
| X017 | Measured: zero orientation changes under scheduler permutations, and **zero exact `(DEF, b)` ties on free edges**, 29/29 goods. | MODEL | numerical test | REVISED | V035 |

## §1.2 — Supply (lines 130–141)

**UNCHANGED:** C023, C025–C028, V038, V039, V040, V041. No delta claims.

## §1.3 — Demand (lines 143–266) — full-strength extraction

**UNCHANGED:** C031, C032, C033, C035, C036, C039, W023, W024, W025, W026, W030, W031, W032,
W033, W036, W042, W043, W044, W047, W050, W051, W052.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X018 | `goods_produced(p) = GP_COEFF · base_production(p) · (1 + Σ local goods-produced modifiers)`, plus local flat goods bonuses. | MODEL | derivation | REVISED | W027 |
| X019 | `trade_value(p) = goods_produced(p) · price(good(p)) · (1 + Σ local trade-value modifiers)`, ducats per year. | MODEL | derivation | REVISED | W028 |
| X020 | `tax_value(p) = TAX_COEFF · base_tax(p) · (1 + Σ local tax modifiers)`, ducats per year. | MODEL | derivation | REVISED | W029 |
| X021 | ⚑ The tax tooltip reads `Base: X (Yearly 12·X)` — `Base: 0.49 (Yearly 6.00)` at `base_tax` 6 and `Base: 0.16 (Yearly 2.00)` at `base_tax` 2. | ENGINE | engine test | REVISED | W034 |
| X022 | ⚑§ The monthly production tooltip's `Trade Value` line is the province window's *annual* `Trade Value` over twelve — observed 3.52 → `Trade Value: +0.29`. | ENGINE | engine test | REVISED | W035 |
| X023 | ⚑ Measured on **two** provinces: Garnatah (223, `base_tax` 6, `base_production` 4, silk, `local_autonomy` 0) and **Caceres (1747, `base_tax` 2, `base_production` 2, wool)**. | WORLD | engine test | REVISED | W037 |
| X024 | ⚑ **Only the tooltips' `Base` lines are used**: a province window's `Trade Value` also carries the owner's `global_trade_goods_size_modifier`. | ENGINE | engine test | NEW *(v4)* | — |
| X025 | ⚑§ Garnatah's window read 3.52 rather than 0.80 × 4.00 = 3.20 because Granada's 1444 monarch held the `Industrious` ruler personality, +10%. | ENGINE | engine test | NEW *(v4)* | — |
| X026 | ⚑ Ruler personalities are rolled at game start wherever country history scripts none, so any window figure is one sample of a random variable; the `Base` lines and the annual-over-twelve ratio are not. | ENGINE | derivation | NEW *(v4)* | — |
| X027 | ⚑§ `Base 0.49` then `Tax Income Efficiency 125.0%` gives **0.6125**, which the province window shows as 0.62. | ENGINE | engine test | REVISED | W038 |
| X028 | Flat goods bonuses add into `goods_produced` before the price multiply; the goods-produced tooltip's shape is **consistent with** that and does not establish it — an additive `Base Goods Produced` block above a separate multiplicative `Goods Produced Efficiency` block. | MODEL | derivation | REVISED | W039 |
| X029 | ⚑ **Fifteen** 1444 provinces carry a flat goods bonus in the additive block, so the ordering matters in practice and not only in principle. | ENGINE | file value | REVISED | W158, W159 |
| X030 | **Locality test:** a modifier is *local* iff its value depends only on the province's own attributes — terrain, climate, trade good, development, buildings — and on no country's state. | DESIGN | stipulated | NEW *(v4)* | — |
| X031 | **Wealth test:** it *enters wealth* iff it modifies a quantity `wealth` computes: `goods_produced`, `price`, or `tax_value`. A modifier must pass both. | DESIGN | stipulated | NEW *(v4)* | — |
| X032 | The engine's trade-good data model is one **instance** of the locality test and not the test itself, because modifiers reach a province from outside the trade-good tables. | ENGINE | derivation | REVISED | W040 |
| X033 | **The tests are applied to the whole install, not to one file.** | DESIGN | stipulated | NEW *(v5)* | — |
| X034 | v4.0 stated the rule and then swept only `common/tradegoods/`, concluded "exactly two", and missed sixteen provinces. | WORLD | derivation | NEW *(v5)* | — |
| X035 | The vanilla set of modifiers that are local **and** enter wealth is: `gems`, `incense`, great-project `province_modifiers`, `add_permanent_province_modifier`, and the five province-state static modifiers. | ENGINE | file value | REVISED | W041 |
| X036 | ⚑ `gems` `local_tax_modifier = 0.15` is live on **43 provinces** at 1444; local, and enters `tax_value`. | ENGINE | file value | NEW *(v4)* | — |
| X037 | ⚑ `incense` `trade_value_modifier = 0.1` is live on **29 provinces** at 1444; local, and enters `trade_value`. | ENGINE | file value | NEW *(v4)* | — |
| X038 | ⚑ **Great-project `province_modifiers` where `can_use_modifiers_trigger` is empty (6 provinces)**: local, and enter `goods_produced` and `trade_value`. | ENGINE | file value | NEW *(v5)* | — |
| X039 | ⚑ **`add_permanent_province_modifier` in the undated province-history block (10 provinces)**: local — applied to the place at the start date — and enters `goods_produced`. | ENGINE | file value | NEW *(v5)* | — |
| X040 | ⚑ The static province-state modifiers are `devastation` −2, `occupied` −0.5 and −0.5, `under_siege` −0.25, `prosperity` +0.25; all are local, all enter `goods_produced` and `tax_value`, and all are zero at the 1444 start. | ENGINE | file value | NEW *(v5)* | — |
| X041 | `glass` `local_production_efficiency = 0.1` is local but does **not** enter wealth: it modifies production *income*, which wealth does not compute. | ENGINE | derivation | NEW *(v4)* | — |
| X042 | ⚑ `chinaware` carries `local_autonomy = -0.1`; local, but does not enter wealth. | ENGINE | file value | NEW *(v4)* | — |
| X043 | ⚑ **361 provinces carry a centre of trade at 1444**, and no CoT level in `common/centers_of_trade/` grants any of the four keys wealth reads — a clean near-miss, recorded so it is not reopened. | ENGINE | file value | NEW *(v5)* | — |
| X044 | ⚑ `production_leader` `trade_goods_size_modifier = 0.10` is **not** local: which country leads a good's production is a country's state. | ENGINE | file value | NEW *(v5)* | — |
| X045 | ⚑ Goods-produced efficiency from nearby merchant republics, trading cities and trade companies (`bonus_from_merchant_republics`, `eu4.exe:0x1cc7128`) is **not** local: it is set by which neighbouring countries hold those government forms. | ENGINE | file value | NEW *(v4)* | — |
| X046 | ⚑ **Buildings are local by the test and empty at 1444** — no province's start state carries a temple, workshop or manufactory. | ENGINE | file value | NEW *(v5)* | — |
| X047 | ⚑ `terrain.txt` and the climate static modifiers are local but grant only `allowed_num_of_buildings`, `defence`, `local_defensiveness`, `local_development_cost`, `movement_cost`, `nation_designer_cost_multiplier`, `supply_limit`, colonial growth and hostile attrition — none of which wealth computes. | ENGINE | file value | REVISED | W045 |
| X048 | ⚑ A great project contributes the `province_modifiers` accumulated up to its `starting_tier` when its `can_use_modifiers_trigger` is empty. | ENGINE | file value | NEW *(v5)* | — |
| X049 | Tiers reached after the start date are owner spending and are out of scope. | DESIGN | stipulated | NEW *(v5)* | — |
| X050 | ⚑ **85 of the 130** great projects live at 1444 are gated on a country's culture, religion, government or flags. | ENGINE | file value | NEW *(v5)* | — |
| X051 | ⚑ Six projects carry a key wealth reads: `falun_copper_mine` (province 8, `trade_goods_size` 3.0), `krakow_cloth_hall` (262, `trade_goods_size_modifier` 0.10), and the four Grand Canal provinces (684, 1821, 1822, 2145; `trade_goods_size` 0.5 and `trade_value_modifier` 0.1 each). | ENGINE | file value | NEW *(v5)* | — |
| X052 | **Province 1821 is the richest single province in the game.** | MODEL | numerical test | NEW *(v5)* | — |
| X053 | The `starting_tier` is the right line and "owner action" is not: development is an owner action, so a rule excluding those would exclude `base_production`, which is wealth's primary input. | DESIGN | derivation | NEW *(v5)* | — |
| X054 | ⚑ The permanent province modifiers are `granary_of_the_mediterranean` (362, 363, 2316, 4316), `skanemarket` (6), `icelanding_fisher_sea` (370, 371), `diamond_mines_of_golconda_modifier` (542), `jingdezhen_kilns` (2151) and `coffea_arabica_modifier` (387), all flat `trade_goods_size`. | ENGINE | file value | NEW *(v5)* | — |
| X055 | ⚑ `province_triggered_modifiers`' `stora_kopparberget_modifier` is gated `NOT = { has_dlc = "Leviathan" }` and grants `trade_goods_size = 5.0` on province 8 — the same province as `falun_copper_mine`. | ENGINE | file value | NEW *(v5)* | — |
| X056 | ⚑ With Leviathan the project applies and gives 3.0; without it the project does not exist and the modifier gives 5.0. | ENGINE | derivation | NEW *(v5)* | — |
| X057 | Every wealth figure in the document was measured with **Leviathan installed**, which is why §2.3 makes DLC state a third input axis rather than a footnote. | WORLD | stipulated | NEW *(v5)* | — |
| X058 | glass and chinaware — local but not entering — are the whole of the rule-versus-vocabulary tension, and the second test excludes them for the same reason §1.3 excludes them by name. | DESIGN | derivation | NEW *(v4)* | — |
| X059 | Excluded by the rule as not local: `Reform Iqta` (+5%, government), `Clergy` (+5%, estate), national ideas (+15%), production efficiency from technology (+2%), and the owner's goods-produced modifiers. | MODEL | derivation | REVISED | W046 |
| X060 | ⚑ `Core` (+75%) and `City` (+25%) are the two that are **not** excluded, because they are already inside `TAX_COEFF`. | ENGINE | derivation | REVISED | W048, W049 |
| X061 | ⚑§ The engine's tax multiplier is the sum of the itemised percentages: Garnatah's `Tax Income Efficiency: 125.0%` is 75 + 25 + 5 + 5 + 15 and multiplies by 1.25; Caceres's `105.0%` is 75 + 25 + 5 and multiplies by 1.05. | ENGINE | engine test | NEW *(v4)* | — |
| X062 | ⚑ A cored city province carrying nothing else sums to exactly 1.00 and yields `base_tax` ducats a year — the reference condition `TAX_COEFF = 1.0` was measured at. | ENGINE | derivation | NEW *(v4)* | — |
| X063 | Every province the model counts is a city (`is_city = yes`) and, since ownership is not modelled, is treated as cored; carrying either term again would double-count it. | MODEL | derivation | NEW *(v4)* | — |

## §1.4 — Market concentration (lines 268–278)

**UNCHANGED:** C040–C047. No delta claims.

## §1.5 — Goods without a graph (lines 280–326)

**UNCHANGED:** C048, C051–C056, V050–V058, W053, W182–W186, W188, W189, W191.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X064 | Measured: repricing to coal the 45 owned latent-coal provinces flips **29 of 159 `Φ_w` edges** (`v5measure.py`). | MODEL | numerical test | REVISED | W187 |

## §1.6 — The aggregate graph (lines 327–440) — full-strength extraction

**UNCHANGED:** C059, C062, V063, V064, V212, V218, V221, W054, W055, W058, W063, W064.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X065 | **The `Φ_w` sink count is set by `α_Φ`; only the sinks' locations are emergent.** v2.0–v4.0's "the count emerges from concentration exactly as per-good sink counts do" is wrong: `α_Φ` is a stipulated constant and the count is a step function of it. | MODEL | numerical test | REVISED | V224 |
| X066 | v2.1 chose the value with a target count in view — a calibration §2.3 now withdraws, since the ground on which 1.5 is *retained* is the band table and not that target. | WORLD | derivation | NEW *(v5)* | — |
| X067 | What the world state moves is *where* the sinks are and *how the map drains toward them*, which is the property §3.1's first goal actually asks for. | DESIGN | derivation | NEW *(v5)* | — |
| X068 | Measured: identical orientation at ×1 and above, **16 edge flips at ×10⁻², and 83 at ×10⁻⁶** — the orientation degrades while the sink set happens to survive, so the sink set is not the quantity to watch here. | MODEL | numerical test | REVISED | W056 |
| X069 | 1444's `b_w` has largest magnitude **0.0227**. | MODEL | numerical test | REVISED | W057 |
| X070 | Measured at α_Φ = 1.5 (`v5measure.py`): **one sink, `hangzhou`** — rank 1 in the α_Φ-weighted wealth field `c_w`, and rank 10 in raw node wealth, where `english_channel` is 1st. | MODEL | numerical test | REVISED | V215, W059 |
| X071 | v2 through v4's two-sink result was measured on a wealth field missing the sixteen provinces §1.3 now carries; correcting the field removes the second sink. | WORLD | derivation | NEW *(v5)* | — |
| X072 | Phase 1 selects `hangzhou` directly, so there are **0 promotions and 0 fallbacks** — the self-correction never fires on this input. | MODEL | numerical test | REVISED | V215 |
| X073 | **Seven sources** — `kongo`, `patagonia`, `james_bay`, `mississippi_river`, `chengdu`, `australia`, `tunis` — all in the bottom half of the wealth field (`c_w` ranks 52–79), mean degree **3.0** against the map's 4.0. | MODEL | numerical test | REVISED | W060, V216 |
| X074 | Every node drains to the sink; acyclic, 159/159 oriented; **0 edge flips and 0 sink-set changes under ±1% wealth noise across 5 seeds**. | MODEL | numerical test | REVISED | V217 |
| X075 | Agreement with the per-good graphs is **52.5%** of edge-goods (**51.5%** value-weighted) against `Φ_ord`'s **60.3%** — a gap of **7.8 points**. | MODEL | numerical test | REVISED | W061 |
| X076 | `Φ_ord`'s edge-good agreement is **60.3%** under the deterministic sweep. | MODEL | numerical test | REVISED | W062 |
| X077 | **The sink count is a step function of `α_Φ`**, measured across α_Φ = 1.00…3.00 at 0.01. | MODEL | numerical test | NEW *(v5)* | — |
| X078 | Band: **1 sink, `hangzhou`, on [1.43, 1.93], width 0.50** — the widest band on this field, and the one α_Φ = 1.5 sits in. | MODEL | numerical test | NEW *(v5)* | — |
| X079 | Band: 3 sinks — `doab`, `genua`, `hangzhou` — on [2.26, 2.71], width 0.45. | MODEL | numerical test | NEW *(v5)* | — |
| X080 | Band: 2 sinks — `genua`, `hangzhou` — on [1.94, 2.25], width 0.31. | MODEL | numerical test | NEW *(v5)* | — |
| X081 | Band: 2 sinks — `english_channel`, `hangzhou` — on [1.41, 1.42], width 0.01. | MODEL | numerical test | NEW *(v5)* | — |
| X082 | That last window is v4.0's result and it is **not a band**: refined to 0.001 it spans **[1.406, 1.424]**, **0.018 wide**, against the one-sink band's **0.506** at the same resolution. | MODEL | numerical test | NEW *(v5)* | — |
| X192 | Under ±1% wealth noise across **8 seeds** that window's edges move by up to 0.02 and its width ranges **0.00 to 0.03** — it is the same size as the noise that perturbs it, and on some seeds it collapses to a single sampled α. | MODEL | numerical test | NEW *(v5)* | — |
| X193 | Over those same 8 seeds the three wide bands keep widths of **0.28–0.51** with edges moving ≤0.03. | MODEL | numerical test | NEW *(v5)* | — |
| X194 | A constant cannot honestly be placed inside a window narrower than the uncertainty in its own edges. | DESIGN | derivation | NEW *(v5)* | — |
| X195 | An earlier draft of the paragraph said the window "moves or disappears entirely" under noise; **at 8 seeds it disappears on none of them — it shrinks**, and the weaker claim is the true one and is sufficient. | WORLD | derivation | NEW *(v5)* | — |
| X083 | `α_Φ` is **retained at 1.5** because it sits inside the widest band and nothing now selects a different value — **not** because it was derived. | DESIGN | stipulated | REVISED | V213 |
| X084 | Sampled at the six values v2 used, the count is non-monotone: **5 → 1 → 2 → 4 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}. | MODEL | numerical test | REVISED | V224 |
| X085 | One sink at 1444 is a snapshot, not a fixed feature, and the map says so under load — holding α_Φ = 1.5 and moving nothing else (`europe.py`). | DESIGN | derivation | NEW *(v5)* | — |
| X086 | At **×1.02 across Europe's 823 counted provinces** the sinks are `{doab, english_channel, hangzhou, wien}`; `english_channel` is a sink at every larger factor tested. | MODEL | numerical test | NEW *(v5)* | — |
| X087 | At ×1.56 the sinks are `{english_channel, rheinland}` and Asia holds none. | MODEL | numerical test | NEW *(v5)* | — |
| X088 | **What the model claims here is the threshold, not the size of the historical edge**: 2% is enough, and the project measures nothing about how much development Europe actually gained. | DESIGN | stipulated | NEW *(v5)* | — |
| X089 | ⚑ `common/institutions/00_Core.txt`: Renaissance begins `1450.1.1` at Florence (province 116), Colonialism `1500.1.1` at Sevilla (224), Printing Press `1550.1.1` at Frankfurt (1876) — all three in Europe, inside the window. | ENGINE | file value | NEW *(v5)* | — |
| X090 | ⚑ The Renaissance's embracement bonus is `development_cost = -0.05`, a standing 5% discount on every subsequent development point. | ENGINE | file value | NEW *(v5)* | — |
| X091 | Those bonuses are country-scoped and so are excluded from wealth by §1.3; they reach the map only by changing how fast a province's development grows, which is the input `europe.py` scales directly. | MODEL | derivation | NEW *(v5)* | — |
| X092 | Developing only the nine Lowland provinces in `english_channel` (Holland, Zeeland, Vlaanderen, Brabant, Antwerpen, Utrecht, Gelre, Friesland, Breda) by ×1.20 makes `english_channel` a sink beside `hangzhou`, and it stays one through ×10. | MODEL | numerical test | NEW *(v5)* | — |
| X093 | ±2% *random* wealth noise leaves the 1444 sink set unchanged on three seeds; **+2% applied systematically to Europe alone changes it**. | MODEL | numerical test | NEW *(v5)* | — |
| X094 | The 1444 route from Europe to the sink is the Silk Road: `genua → alexandria → aleppo → persia → lahore → doab → ganges_delta → burma → gulf_of_siam → canton → hangzhou`. | MODEL | numerical test | NEW *(v5)* | — |
| X095 | From the north it is the Volga: `north_sea → white_sea → novgorod → kazan → astrakhan → persia → …`. | MODEL | numerical test | NEW *(v5)* | — |
| X096 | From the Channel it is the Hansa and the Danube: `english_channel → lubeck → saxony → wien → venice → ragusa → constantinople → aleppo → …`. | MODEL | numerical test | NEW *(v5)* | — |
| X097 | Nothing routes through the Cape in `Φ_w`, which is what a 1444 map should say. | OUTCOME | numerical test | NEW *(v5)* | — |
| X098 | The Cape is not idle: in the per-good graphs it already carries Asian spices to Europe — `malacca → cape_of_good_hope → zanzibar → gulf_of_aden → alexandria → genua`. | MODEL | numerical test | NEW *(v5)* | — |
| X099 | Scaling **the 22 European nodes'** wealth ×2 makes `genua` the sole sink; the 22 are 18 western and central European nodes plus `constantinople`, `crimea`, `kiev` and `kazan`, and under the 18-node set alone sole-`genua` needs ×2.5. | MODEL | numerical test | REVISED | V223 |
| X100 | Between **×3 and ×3.75** the Cape of Good Hope **reverses** — Atlantic→Cape→Indian-Ocean drainage becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast — and outside that window it does not, so the reversal is a **band and not a threshold**. | MODEL | numerical test | REVISED | V223 |
| X101 | Dev-stacking `hangzhou`'s top province keeps it the sole sink at ×20, ×30 and ×50, with a transient split into three at ×10. | MODEL | numerical test | REVISED | V223 |

## §1.7 — Merchants (lines 442–468)

**UNCHANGED:** C067–C083, V066, V068, V069, V070, W065, W192.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X102 | Trade efficiency and a flat income bonus are different quantities in EU4, and the define's own shipped comment settles which `TRADE_MERCHANT_PRESENT` is: `-- bonus on income if trade present`. | ENGINE | file value | REVISED | W066 |

## §1.8 — Collection and transfer (lines 470–500)

**UNCHANGED:** C084–C102, V072.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X103 | ⚑ What trade range gates is **reach, not flow**: every string, define and modifier that mentions it is about where a country may *send* something — `HINT_TRADERANGE_TEXT`, `TRADE_RANGE_IRO`, `TRADE_NODES_OUT_OF_RANGE`, `MAPMODE_TRADE_DESC`, `MERCENARY_COMPANY_TOO_FAR` / `MERC_RANGE_EXPLAINED`, `REQUIRES_CAPITAL_IN_TRADE_RANGE_TT`. | ENGINE | file value | REVISED | V071 |
| X104 | ⚑ **No string, define or modifier ties range to link flow** — which is a statement about the files, not a proof that no such mechanic exists; settling it needs value observed arriving at a node chain beyond every country's range. | ENGINE | file value | NEW *(v4)* | — |

## §1.9 — Trade power propagation (lines 502–511)

**UNCHANGED:** C103–C111, V073, W067, W068, W069. No delta claims.

## §1.10 — Direction-dependent systems (lines 513–562)

**UNCHANGED:** C112–C143, V074, V078, V079, V080, W070, W071.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X105 | ⚑ Propagate Religion is 50/50 in the default branch and 35/35 in the terminal branch, **neither banded**; the nine `N_trade_power_for_propogate_religion` country-flag rungs between them **are** banded, maintain trailing select by 5–10 points (10→5, 15→5, 20→10, 25→15, 30→20, 35→25, 40→30, 45→35), and the 5-flag carries no maintain share at all. | ENGINE | file value | REVISED | V075 |
| X106 | Improve Inland Routes is the one **unconditionally** banded mechanic and Propagate Religion is banded only on its flag ladder, so the flicker-risk set is "every country at a single-valued limit, plus flagless countries at Propagate Religion's 50/50 or 35/35", not "every country". | ENGINE | derivation | REVISED | V076, V077 |
| X107 | Measured on the 1444 start: the caravan cap of 50 is **8.6% to 32.0%** of an inland node's total trade power, median 17.9% over the **flag's** 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. | MODEL | numerical test | NEW *(v4)* | — |
| X108 | On §2.2's derived 25-node inland basis the range, the largest-holder span and the outweigh count are all identical, and only the median moves — to **17.5%**. | MODEL | numerical test | NEW *(v5)* | — |
| X109 | The largest single incumbent holder is **23.6 to 143.2**, so a country at the cap outweighs the largest incumbent in **7 of the 26** inland nodes and is outweighed in the other 19. | MODEL | numerical test | NEW *(v5)* | — |
| X110 | ⚑ v4.0 read the save's per-node `highest_power` field as the largest incumbent's power. **It is not**: parsed against each node's country sub-blocks at their own brace depth, `highest_power` differs from the largest single country's `val` on **79 of 79** nodes — at `venice` 53.2 against Venice's own 106.2 — and it matches no share of `total`, `max`, `p_pow` or `collector_power` either. The conclusion v4.0 drew from it inverted. | ENGINE | file value | NEW *(v5)* | — |
| X196 | What `highest_power` does hold **was not determined**, and the model does not read it; §1.10's power figures come from the country sub-blocks. | DESIGN | stipulated | NEW *(v5)* | — |

## §1.11 — Treasure fleets · §1.12 — What the game displays (lines 564–589)

**UNCHANGED:** C144–C148, C149–C165, V049, V065, V081. No delta claims.

## §2.1 — Shape (lines 595–612)

**UNCHANGED:** C167–C184, V082–V085, W072, W073. No delta claims.

## §2.2 — Solver (lines 614–651)

**UNCHANGED:** C185–C209, V064, V091, V092, V229, W075, W076.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X111 | Solver item 4 computes `TAX_COEFF · base_tax · (1 + local tax modifiers) + (GP_COEFF · base_production + local flat goods bonuses) · (1 + local goods-produced modifiers) · price · (1 + local trade-value modifiers)`, with no autonomy, efficiency, ideas or owner terms. | DESIGN | stipulated | REVISED | W074 |
| X112 | The solver reads the local modifiers from §1.3's classification applied to the whole install: at 1444 that is `gems` (43 provinces), `incense` (29), six great projects and ten permanent province modifiers — **16 provinces beyond the two trade goods**. | DESIGN | stipulated | NEW *(v5)* | — |
| X113 | World wealth is **10,677.50** annual ducats over **2,452** counted provinces. | MODEL | numerical test | NEW *(v5)* | — |
| X114 | Measured on the reference implementation (scipy/HiGHS plus the deterministic sweep, one machine): **0.17–0.21 s for all 29 goods, a mean of 5.7–7.3 ms per good across runs**, with individual goods ranging **5.4–24 ms**, so 7.3 is an average and not a maximum. | MODEL | numerical test | REVISED | V090 |
| X115 | "Milliseconds each" holds already with a generic LP; the all-29 figure is what a native network simplex would have to improve on, and no measurement in this project supports a specific projection, so none is offered. | DESIGN | derivation | NEW *(v4)* | — |

## §2.2a — What map this is for (lines 653–693)

**UNCHANGED:** W077–W085, W088.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X116 | Two further cases are independent of Phase 0 and both break sink-set equality inside the 2-core: **T2** (a free edge takes sinkhood from a selected flow-terminal demander) and **T3** (a fallback promotion). | MODEL | derivation | REVISED | W087 |
| X117 | Free-edge determinism is **proved as determinism** and **measured as independence from the node indexing** (zero exact `(DEF, b)` ties, 29/29 goods); both halves are unaffected by peeling, which does not touch the priority key. | MODEL | derivation | REVISED | W086 |

## §2.3 — Constants (lines 695–740) — full-strength for the coefficients

**UNCHANGED:** C211–C227, V094, W089, W090, W091, W097, W098, and the DLC-third-axis claim.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X118 | ⚑ **`GP_COEFF` = 0.2** goods produced per point of `base_production`, measured on **four provinces at four development levels** from the `Base Goods Produced` line: Caceres (1747) 2 → 0.40, Girona (212) 3 → 0.60, Garnatah (223) 4 → 0.80, Barcelona (213) 5 → 1.00. | ENGINE | engine test | REVISED | W092, W093 |
| X119 | ⚑ **`TAX_COEFF` = 1.0** ducat/year per point of `base_tax`, measured on **two provinces at two development levels** from the `(Yearly …)` parenthetical. | ENGINE | engine test | REVISED | W094, W095 |
| X120 | ⚑ The displayed monthly tax figure is the truncation of `base_tax × 0.083333`. | ENGINE | derivation | NEW *(v4)* | — |
| X121 | Both coefficients are read off the tooltips' **base** lines, which carry no owner term; neither is read off a province window, because a window figure carries the owner's modifiers and some of those are randomised at game start. | DESIGN | derivation | REVISED | W096 |
| X122 | **α_Φ's stated calibration is withdrawn**: v2.1 through v4.0 said 1.5 was calibrated so the 1444 start yields the two-sink hangzhou/english_channel map; on the corrected wealth field it does not yield that map, and the α_Φ window that does yield it is narrower than the uncertainty in its own edges under ±1% wealth noise. | DESIGN | derivation | REVISED | V213 |
| X123 | Any future change to `α_Φ` is a design decision about how many ends the installed graph should have, and should be recorded as one. | DESIGN | stipulated | NEW *(v5)* | — |

## §2.4 — The tradenodes file (lines 742–782)

**UNCHANGED:** C228–C233, C235–C242, V095, V148, W099, W100, W102–W107, W114.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X124 | ⚑ The cyclic-file crash is `EXCEPTION_STACK_OVERFLOW` at a **single exception address (`0x00007FF6DDE6A8B4`) under 1002 recorded `eu4.exe` frames** — the dump records no per-frame addresses — reproduced on **three** launches, with vanilla and the reversed-order file as controls. | ENGINE | engine test | REVISED | W101 |
| X125 | **The node order itself is a correctness requirement, not a convention**: §1.1's priority key breaks exact ties by node index and on the fallback branch (T3) the index alone decides, so the emitter must fix one canonical node order and keep it stable across rebuilds, or the same world can produce two different maps. | DESIGN | derivation | NEW *(v5)* | — |
| X126 | End flags: `end=yes` on every `Φ_w` sink — 1444 has **one** end node, `hangzhou`, against vanilla's three. | DESIGN | numerical test | REVISED | V215 |
| X127 | The end count is not fixed — it follows the wealth field and `α_Φ` — so the emitter reads it from the solve rather than assuming a number. | DESIGN | stipulated | NEW *(v5)* | — |

## §2.5 — Runtime attachment · §2.6 — Writing to the engine (lines 784–810)

**UNCHANGED:** C243–C250, C251–C272. No delta claims.

## §2.7 — Probes (lines 812–849)

**UNCHANGED:** C274–C293, V098–V101, W108–W114. No delta claims.

## §2.8 — Validation (lines 851–893)

**UNCHANGED:** C298–C342, V109–V112, W116, W117, W119, W195.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X128 | Baseline DRAIN: cloves sink at Venice, Kongo, **Deccan**, Australia and Brazil; under the §3.13 α-calibration `spices` sinks at **Genoa alone** and it is **cloves** that moves to **Deccan**. | MODEL | numerical test | REVISED | V106, W115 |
| X129 | Sinks are 1 to 7 per good; high-demand nodes are sinks at **14.5%** in the top demand decile against **6.9%** in the bottom — a barbell, LP branch ends landing in poor pockets. | MODEL | numerical test | REVISED | V108 |
| X130 | Zeroing `hangzhou`-node development moves the `Φ_w` sinks from `{hangzhou}` to `{doab, english_channel, gulf_of_siam, sevilla}`, with **22 of 159 edges flipping**. | MODEL | numerical test | REVISED | C298–C342 † |
| X131 | `hangzhou`, not `beijing`, is China's wealth pole under §1.3: `c_w` rank 1 against `beijing`'s 31, node wealth **245.0 against 143.8**, and it holds the richest single province. | MODEL | numerical test | NEW *(v5)* | — |
| X132 | Zeroing `beijing` **also** moves the map — 17 flips, sinks `{doab, english_channel, hangzhou, sevilla}` — because deleting 1.3% of world wealth renormalises `c_w` everywhere; what separates the two cases is that `hangzhou` survives as a sink when `beijing` is zeroed and does not when `hangzhou` is. | MODEL | numerical test | NEW *(v5)* | — |
| X133 | Ming losing the Mandate moves **nothing on the day it happens**: the Mandate is an owner property and §1.3 reads none, so the row is the owner-agnosticism check rather than a responsiveness check. | DESIGN | derivation | REVISED | C298–C342 † |
| X134 | ⚑ The 8.96% run-to-run drift spans the five node fields `current`, `local_value`, `outgoing`, `total` and `retention`, and it is the three power-dependent fields that inherit the randomised AI merchant placement. | ENGINE | engine test | NEW *(v4)* | — |
| X135 | `retention` is identical on 80 of 80 nodes and `total` on **78 of 79**, the exception — `zambezi` — drifting 0.012%. | ENGINE | engine test | REVISED | W118 |
| X136 | 2-core containment is asserted unconditionally against `{selected} ∪ {promoted} ∪ {fallbacks}` — the set the sweep actually maintains — because asserting over `{selected} ∪ {promoted}` alone would halt on **T3**, which is correct behaviour; the fallback set is part of the assertion, not an escape clause on it. | DESIGN | derivation | REVISED | W193 |
| X137 | Equality is monitored with **T2 and T3** named as the two ways it can fail while the algorithm behaves correctly; measured exact on 1444, 29/29 goods, zero fallbacks. | DESIGN | derivation | REVISED | W194 |

## §2.9 — Build order (lines 894–903) · §3.1 — Goals (lines 909–917)

**UNCHANGED:** C343–C352, C353–C365, V113. *(§2.9's assertion list now names the widened
containment set; that proposition is X136 at first appearance.)*

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X138 | Goal 1's worked example is a horde razing **`hangzhou`**, not Beijing. | DESIGN | stipulated | REVISED | C353–C365 † |

## §3.2 — Why a flow and a drainage sweep (lines 919–1017)

**UNCHANGED:** C366, C370–C375, C383–C385, V115, V116, V118–V122, V124, V128–V131, W120, W123,
W125, W126, W127, W128.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X139 | The Laplacian's right-hand side is set by supply geography because **supply is sparse where demand is dense**: spices are produced in 18 of 80 nodes and cloves in one, while every node with an owned province carries demand. | MODEL | numerical test | REVISED | V117 |
| X140 | With no regularizer the spices supply ratio over *producing* nodes is **36** against a demand ratio of **482.2**, which points the other way from v1's stated asymmetry. | MODEL | numerical test | NEW *(v4)* | — |
| X141 | Sparsity is the asymmetry that survives the regularizer's deletion, and the diagnosis rests on it. | MODEL | derivation | NEW *(v4)* | — |
| X142 | Better wealth inputs plausibly deliver about 1.7× — measured, `genua` becomes a co-sink at **×1.720**. | MODEL | numerical test | REVISED | W121 |
| X143 | A spice sink at any of the four Chinese trade nodes needs **3.6–4.9×**, i.e. **9.3–21.4%** of all world spice demand at one node: `beijing` 3.60× / 9.3%, `hangzhou` 3.83× / 21.4%, `xian` 4.59× / 12.3%, `canton` 4.86× / 17.8%. | MODEL | numerical test | REVISED | W121, W122 |
| X144 | The four China-region nodes outside that set — `girin`, `yumen`, `chengdu`, `lhasa` — need **4.0× to 10.8×**. | MODEL | numerical test | NEW *(v4)* | — |
| X145 | Sink placement holds where Phase 0 is a no-op **and no fallback fires**; **three** constructed inputs break it, all run through a faithful implementation of §1.1 (`toys.py`). | MODEL | numerical test | REVISED | W129 |
| X146 | **T3 worked:** a triangle A, B, C with `b = 0` at all three and node wealth 3, 2, 1 — Phase 1 selects nothing, every edge is free, the sweep stalls with no flow-terminal demander, the fallback promotes A, free edges orient B→A, C→A, C→B; actual sinks `{A}`, formula set empty, and A is in neither `{selected}` nor `{promoted}`. | MODEL | numerical test | NEW *(v4)* | — |
| X147 | What survives unconditionally is the ⊆-direction within the 2-core **over the set the sweep actually maintains**: every core node that is neither selected, promoted **nor fallback-promoted** is given an out-arc, and pendant net-importers are the only sinks outside that set. | MODEL | derivation | REVISED | W124 |
| X148 | Sink placement is checked at runtime as two checks (§2.8): containment asserted unconditionally against `{selected} ∪ {promoted} ∪ {fallbacks}`, and equality monitored with **T2 and T3** named as its legitimate failures. | DESIGN | stipulated | REVISED | W131 |
| X149 | Written against the narrower containment set, **T3 would halt the solver on correct behaviour**. | DESIGN | derivation | NEW *(v4)* | — |
| X150 | Free-edge direction is deterministic by construction; that the node indexing never decides is **measured, not proved**, and holds where the key has no exact ties — zero exact `(DEF, b)` ties on free edges, 29/29 goods. | MODEL | numerical test | REVISED | W130 |
| X151 | The one place the indexing is load-bearing is the fallback branch (T3), where the candidates are typically all zero-wealth and tied; §2.4 item 1 makes a canonical node order a correctness requirement for that reason. | MODEL | derivation | NEW *(v5)* | — |

## §3.3 — Why wealth, and why per province (lines 1019–1040)

**UNCHANGED:** C386–C406, C408, C412, C413, V132, V133, V135, W132–W139. No delta claims.
*(The `[unverified in v3.0]` markers on the node land-province counts and the Nippon comparison
were removed in v4.0; per the conventions that is not a proposition change.)*

## §3.4 — Why supply is pre-modifier (lines 1042–1052)

**UNCHANGED:** C415–C423, V137, V138, V139, W140, W141, W142. No delta claims.

## §3.5 — Why α is anchored absolutely (lines 1054–1079)

**UNCHANGED:** C427–C442, V140–V144, V147.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X152 | **13 of 30 goods** can be pushed strictly below 2.0 by a single vanilla `change_price` event (grain and wine reach 0.625). | ENGINE | file value | REVISED | W143 |
| X153 | **Two** more — `gems` and `silk` — land exactly on 2.0 and so reach α = 1 but not the sublinear regime; **four** have a negative event that does not reach 2.0; and 11 have no negative price event at all. | ENGINE | file value | REVISED | W144 |
| X154 | ⚑ All **161** `change_price` blocks were parsed — 93 in `events/`, **14 in `missions/`**, 1 in `common/`, and **53 in `history/`, of which 13 are negative**, all in `history/countries/HAB - Austria.txt`. | ENGINE | file value | REVISED | W146 |
| X155 | v4.0 said 154 and 7: its parser silently recovered nothing from five mission files, which a bare `except` hid, so the scan is now guarded by a per-file count assertion; the seven recovered blocks are all positive and the partition is unchanged. | WORLD | derivation | NEW *(v5)* | — |
| X156 | ⚑ `wool`'s largest single negative is `HAB - Austria.txt`'s `NEW_DRAPERIES` at −0.25 for 2.5 → **1.875**, against the −0.20 the same key carries in `events/PriceChanges.txt`; `change_price` entries are keyed, so 1.875 is the figure a campaign reaching 1540 holds. | ENGINE | file value | NEW *(v4)* | — |
| X157 | v2's 13 was right; v3.0 reached 12 by parsing four of the five trees. | WORLD | derivation | NEW *(v4)* | — |

## §3.6 — Why no hysteresis, and why there is no ε (lines 1081–1116)

**UNCHANGED:** C443–C446, C449, C452, V148, V152, V154, W147–W152. No delta claims. *(The
three-launch / exception-address revision of the cycle crash is X124 at first appearance.)*

## §3.7 — Why eligibility is per good (lines 1118–1124)

**UNCHANGED:** C463–C473. No delta claims.

## §3.8 — Why gates evaluate true (lines 1126–1144)

**UNCHANGED:** C474–C497, V155–V158, W154.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X158 | Measured under DRAIN, **92.2%** (5825 of 6320) of ordered node pairs are connected by at least one good on 1444 data. | MODEL | numerical test | REVISED | W153 |

## §3.9 — Why `Φ_w` is the installed graph (lines 1146–1189)

**UNCHANGED:** C502, C505–C510, C512, V160, V161, V162, V218, V221, V228.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X159 | A rich **non-sink** node — `genua`, `gulf_of_siam` and `sevilla`, ranking 3rd, 2nd and 7th by node wealth **on the corrected field** at 296.0, 299.2 and 266.5 against `english_channel`'s 316.6, and none of them a sink — draws more edges in than it sends out as a net demander even though flow passes through. | MODEL | numerical test | REVISED | W156 |
| X160 | `Φ_ord`'s ends are sweep-scheduling artifacts: of its **13** end nodes at 1444, **8** terminate no good at all, its end count never concentrates (**11–17** across cloves-α 2…64), and v2's "9–17 ends" is neither the right word for a range of 11–17 nor a band containing its own baseline of 13. | MODEL | numerical test | REVISED | W155, V222 |
| X161 | `Φ_w` is adopted for **one operator, one set of guarantees, and ends that move with the world**: it reuses §1.1 unchanged, so LP feasibility, acyclicity, determinism and scan-invariance come for free and the correctness check stays a single combinatorial comparison. | DESIGN | derivation | REVISED | V220 |
| X162 | v2.1 through v4.0 justified the adoption by "two vanilla-like ends at 1444"; on the corrected wealth field there is **one** end, in China, matching none of vanilla's three, so **that premise is withdrawn**. | WORLD | derivation | NEW *(v5)* | — |
| X163 | The trade is now stated as what it is: **7.8 points** of self-coherence given up for one operator and world-responsive ends, with the 1444 count whatever the field gives. | DESIGN | stipulated | NEW *(v5)* | — |

## §3.10 — Why the engine's economy is overwritten (lines 1191–1206)

**UNCHANGED:** C513–C521, C523–C525, C528–C530.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X164 | The income factoring is an **identity, not a measurement**: `powershare_C(n)` carries no `g`, so it factors out of the sum, and by §1.1's vocabulary the property is true by construction and carries no measurement. | MODEL | derivation | REVISED | C522 |
| X165 | Every term that feeds a collector's power at a node is node-wide — the merchant bonus, the off-home penalty, propagation off the one installed graph, the caravan grant — so none of them can reintroduce a `g`. | MODEL | derivation | NEW *(v5)* | — |
| X166 | What a run can show is only that the implementation does the algebra in doubles: across Sevilla, Genoa, Champagne, Malacca and the Gulf of Siam on each node's real 1444 country table, the two forms agree to a worst relative disagreement of **0 to 3.7e-16**. | MODEL | numerical test | REVISED | C522 |
| X167 | v1 through v4.0's "5.7e-14" and "1.4e-14" are floating-point residuals of an exact identity, produced by constructions none of those documents states — a theorem decorated with an experiment. | WORLD | derivation | NEW *(v4)* | — |
| X168 | Reading the one installed graph leaves the propagated term good-independent, so the identity survives it untouched — same construction, worst relative disagreement 0 to 3.7e-16. | MODEL | numerical test | REVISED | C526 |
| X169 | The driver is **not** how many distinct downstream sets a node has but whether its collectors hold differing power across the nodes those sets differ on: `gulf_of_siam` has eight distinct downstream sets and still shows a **0.003%** effect, because its collectors hold almost nothing in `burma`, `canton` or `malacca`. | MODEL | numerical test | NEW *(v5)* | — |
| X170 | Per-good propagation's error is **redistributive and single-digit percent, with the sign varying by collector** — Sevilla −0.82%, −0.87%, +7.44%; Champagne −1.69%, +1.69%, +1.53%; Genoa −0.23%, −0.22%, +0.70%. | MODEL | numerical test | REVISED | C527 |
| X171 | It is not a bias in one direction and it is not rounding: it is thirteen orders of magnitude above the float residual and it moves income between countries. | MODEL | derivation | NEW *(v5)* | — |
| X172 | Its size depends on which countries are collecting, which is a stated choice of the construction and not a property of the node, so no single percentage is quoted as one. | DESIGN | stipulated | NEW *(v5)* | — |
| X173 | No node in the model has local trade value near 250; **the largest is 112.6**. | MODEL | numerical test | NEW *(v5)* | — |
| X174 | v4.0's replacement figure, 0.41%, was an artifact of freezing one term at the alphabetically first commodity. | WORLD | derivation | NEW *(v5)* | — |

## §3.11 — Caravan power · §3.12 — Treasure fleets (lines 1208–1244)

**UNCHANGED:** C531–C547, C556–C560, V163–V172. No delta claims. *(The `[unverified in v3.0]`
marker on "nineteen countries at the cap" was removed in v4.0 — not a proposition change.)*

## §3.13 — Open questions (lines 1246–1305)

**UNCHANGED:** C561–C585, V173, V174, V175, V178, V181, V182, V183, W164.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X175 | The wealth model has **one** open question, not three, and it is a question rather than a number; two of v3.0's three are settled and have moved into §1.3. | DESIGN | stipulated | REVISED | W157 |
| X176 | ⚑ **Open:** what else multiplies `goods_produced`, and which side of the owner line does each source fall on? `trade_goods_size` and `trade_goods_size_modifier` appear in buildings, estate privileges, government reforms, church aspects, fervor, ages and event modifiers, and each needs the §1.3 locality test before a modded or late-game province can be priced. | ENGINE | derivation | NEW *(v4)* | — |
| X177 | ⚑§ **Settled:** `local_production_efficiency` from a trade good is outside wealth — Barcelona's production tooltip reads `Production Efficiency: +12.0% / From Technology: +2.0% / Producing Glass: +10.0%`, so the engine books glass's +10% on production income. | ENGINE | engine test | REVISED | W160, W161 |
| X178 | **Settled:** `TAX_COEFF` **is** 1.0 across the development range — `Base: 0.49 (Yearly 6.00)` at `base_tax` 6 and `Base: 0.16 (Yearly 2.00)` at 2 — with `GP_COEFF` linear at four levels. | ENGINE | engine test | REVISED | W162, W163 |
| X179 | The sublinear regime is reachable through vanilla price events for **13 of 30** goods, unreachable for 11, and exactly on the boundary for **2**. | DESIGN | derivation | REVISED | W165 |
| X180 | The sink-count-span calibration gives span exactly 1..5 with **spearman(price, sinks) = −0.20**. | MODEL | numerical test | REVISED | V177 |
| X181 | Under the calibration's α = 16, **Deccan** is demand rank 2 — with the rank-1 demander `hangzhou` acting as a transit node — and becomes the cloves sink; **Beijing is only demand rank 3**. | MODEL | numerical test | REVISED | W166, V179 |
| X182 | `hangzhou` holds the richest single province, at **30.4** against Beijing's 19.5. | MODEL | numerical test | REVISED | W167 |
| X183 | The twig tolerance re-routes arcs individually carrying <0.03% of world supply — up to about **0.18%** of a good's mass in total — and drops **cloves** to 99.97% reach. | MODEL | numerical test | REVISED | W168, V180 |

*(§3.13's "fifteen 1444 provinces carry a flat `trade_goods_size`, five from great projects and
ten from permanent province modifiers" is X029 at first appearance in §1.3.)*

## §3.14 — AI merchant assignment (lines 1307–1324)

**UNCHANGED:** C586–C624.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X184 | The survival table is about **1.5 MB at double precision** — 29 goods × 80 × 80 entries at 8 bytes is 1,484,800 bytes — and the solver's residuals sit at 1e-16, one ULP of a double. | MODEL | derivation | REVISED | W169, W170 |

## §3.15 — Rejected (lines 1326–1434)

**UNCHANGED:** C625–C672 as carried by v2, V184–V188, V192–V199, V226, V227, V228.

| ID | Claim | Type | Provenance | Status | Replaces |
|---|---|---|---|---|---|
| X185 | The Laplacian's supply signal is **sparse rather than large**, and with v1's ε floor removed the contrasts run **4–97 on supply against 211–20,400 on demand** across the 29 goods — the demand side is the wider one. | MODEL | numerical test | REVISED | V117, V184 |
| X186 | v3.0 through v4.0 repeated the 10⁷ / 10²–10³ ratio in §3.15 while §3.2 was withdrawing it. | WORLD | derivation | NEW *(v5)* | — |
| X187 | Ranked orientation wins the alignment statistics — ρ_val **+0.281** against DRAIN's **+0.054**, and **43.8%** of top-decile nodes are sinks against **14.5%** — and loses the rest: **83.0%** of demand reachable, **31** orphan sinks. | MODEL | numerical test | REVISED | W171, V189 |
| X188 | Ranked orientation posts **8** net-producer sinks where DRAIN, LAP and FLOW post zero, and **10–16** sinks per good against DRAIN's **1–7**. | MODEL | numerical test | REVISED | W172 |
| X189 | Seeded basin growth reaches **88.4%** at its best tuning. | MODEL | numerical test | REVISED | V191 |
| X190 | The 3-mass gravity kernel hits any chosen end count exactly for γ ≤ 0.7 and any count up to six; at γ = 0.9 the **four-, five- and six-mass fields all collapse to three ends**; best vanilla-arrow agreement is **61% at γ = 0.90–0.95 (97 of 159 arrows)**, with γ = 0.97 giving 93 and every larger γ worse. | MODEL | numerical test | REVISED | W190, V225 |
| X191 | v2.1 through v4.0 put the best agreement at γ = 0.97 and said the five- and six-mass fields give four ends at γ = 0.9; on the corrected wealth field neither holds. | WORLD | derivation | NEW *(v5)* | — |

## §3.16 — Evidence standard (lines 1436–1498)

**UNCHANGED:** C677, C680–C682, C684, C685, V200–V204, V206–V210, W173–W181. No delta claims.

---

# Observations

These were recorded, not fixed, at first extraction. **Five were acted on and the spec was
revised; the rows above describe the final text.** Each is kept here with its resolution, because
an inventory that silently absorbs its own findings is worth less than one that shows them.

### 1. §2.8 wore the unweighted agreement figure under the value-weighted label — **fixed**

§1.6 and §3.9 gave 52.5% edge-goods / **51.5%** value-weighted; §2.8's "Measured, not asserted"
block gave *"52.5% of value-weighted edge-goods"* — the unweighted number under the weighted
label, left behind when the v5.0 regeneration moved §1.6 and §3.9. §2.8 now reads *"**51.5%** of
edge-goods *weighted by trade value*, and on 52.5% unweighted (§1.6)"*. The proposition is X075 at
first appearance; §2.8 restates it and no longer contradicts it.

### 2. §3.9's node-wealth ranks had no v5.0 provenance — **fixed, and they held**

"`genua`, `gulf_of_siam` and `sevilla` rank 3rd, 2nd and 7th by node wealth" entered in v4.0 and
did not appear in the v4.0→v5.0 diff, so it stood on the field v5.0 says was missing sixteen
provinces, while every neighbouring figure had been regenerated. Re-measured on the corrected
field the three ranks are **unchanged**, and §3.9 now says so and carries the wealths — 296.0,
299.2, 266.5 against `english_channel`'s 316.6 (X159). A null result, and now a sourced one.

### 3. §1.10's caravan conclusion — **objection withdrawn, with a residue**

First extraction read *"enough to move a node's power shares by itself, and therefore to push
other countries across the thresholds above"* as undercut by the same paragraph's finding that a
country at the cap is outweighed by the largest incumbent in 19 of 26 inland nodes. **That reading
was wrong and is withdrawn.** The two statements measure different things: the cap's share of the
*node* (8.6–32.0%, median 17.9% — X107) and the cap against the largest *incumbent* (X109). A
country can be far from the biggest holder and still move every share materially, so the first
clause is now supported by X107 and there is no contradiction.

**What survives is smaller and is about provenance, not consistency.** The words that carry more
than X107 measures are **"and therefore to push *other* countries across the thresholds above"**.
That is a derivation from the share measurement, not a measurement: no country has been shown
crossing `JUSTIFY_TRADE_CONFLICT_LIMIT`, `TRADE_COMPANY_CONTROL_LIMIT` or any other §1.10 limit
because a caravan grant diluted its share. It is a reasonable derivation — diluting every
incumbent by 8.6–32% will cross a limit for anyone sitting near one — and it needs no spec change.
The inventory change it does suggest is that **W071, carried UNCHANGED from claims-v3.md and typed
`UNSOURCED` there, is now mis-typed**: its first clause has a measurement and its second is a
derivation. Re-typing W071 `derivation` in the next inventory would be the accurate move; that is
a claims-file correction, not a spec one, so it is left as a recommendation.

### 4. X110 asserted what a save field is *not* without saying what it is — **fixed**

The parenthetical now states the test it rests on: parsed at each node's country-sub-block brace
depth, `highest_power` differs from the largest single country's `val` on **79 of 79** nodes, at
`venice` 53.2 against Venice's own 106.2, and matches no share of `total`, `max`, `p_pow` or
`collector_power`. It also now says outright that what the field holds **was not determined** and
that the model does not read it (X196). The row's provenance moves from `derivation` to
`file value` and it loses its **§** marker: 79 of 79 nodes is not a single observation.

### 5. §1.6's noise claim was stronger than the test supported — **fixed, weaker, and correct**

Not on the first-pass list; raised and settled during the revision. The band-table paragraph said
v4.0's `{english_channel, hangzhou}` window *"moves or disappears entirely"* under ±1% wealth
noise. Run at 8 seeds it **disappears on none of them — it shrinks**. The paragraph now gives the
window refined to 0.001 at [1.406, 1.424], 0.018 wide against the one-sink band's 0.506, with
edges moving ≤0.02 and width ranging 0.00–0.03 under noise while the three wide bands hold
0.28–0.51 (X082, X192, X193), and rests the design decision on the sharper and weaker principle
that a constant cannot sit inside a window narrower than the uncertainty in its own edges (X194).
§2.3 carried the same overstatement and now states the window claim instead (X122). **This is the
one place where the first extraction's rows recorded a claim the document could not support**, and
it was the document's claim, not the extraction's.

### 6. "The ten permanent modifiers" then naming six keys — **withdrawn**

The objection is wrong and is withdrawn. `granary_of_the_mediterranean` covers four provinces and
`icelanding_fisher_sea` two, so six keys across ten provinces is exactly what the sentence says
when read with the table above it, and every total reconciles (6 project provinces + 10 modifier
provinces = 16; 5 flat project bonuses + 10 flat modifier bonuses = X029's fifteen). Terse, not
wrong.

### 7. `changes-v5.md` entry 56 was mis-headed §2.9 — **fixed**

The text it replaces is §2.8's Latent-good validation row. The spec was correct either way; only
the change log's section label was off, and it now reads §2.8.

---

# † Unresolvable IDs

Three v5 revisions replace sentences that entered in v1 and passed through v2 and v3 as
UNCHANGED, so their IDs live in `../v1-laplacian/claims.md`. They fall in **two** C-ranges. Each
row names the range from `claims-v2.md`'s UNCHANGED list for that section.

| X ID | Section | Replaced sentence | Believed C-range |
|---|---|---|---|
| X130 | §2.8 | the Razed-China row, "Zeroing Beijing-node development relocates the sink in one solve" | C298–C342 |
| X133 | §2.8 | the Ming row, "Beijing's pull collapses with its income" | C298–C342 |
| X138 | §3.1 | Goal 1's "A horde razing Beijing moves the sink because the wealth moved" | C353–C365 |

**Five † markers carried by `claims-v3.md` are resolved by this pass**, by grepping `claims.md`
and `claims-v2.md` rather than reading them: **W070**'s predecessor is **C135** ("Caravan power is
not a threshold mechanic but a step function on raw power"); §3.10's three figures are **C522**
(5.7e-14), **C526** (1.4e-14) and **C527** (5.96 ducats on a node paying ~250); §2.2's solve-cost
sentence is **V090**; §3.2's supply-contrast claim is **V117**; §2.2's inland derivation is
**V092**. Those IDs are used directly in the tables above.

---

# Revision note — this file was re-extracted against the final spec text

The first pass of this inventory was taken against the v5.0 spec at 1,498 lines / 130,389 bytes
(63 asserted edits). Five passages were then revised — two while the extraction was still running,
three in response to its observations — and this file has been brought into line with the final
text at **1,504 lines / 131,566 bytes (68 asserted edits)**. Only the rows covering those five
passages were re-extracted; nothing else was re-read.

| Passage | Rows changed | What moved |
|---|---|---|
| §1.6, the paragraph under the α_Φ band table | **X082 rewritten; X192, X193, X194, X195 added** | "not reproducible … moves or disappears entirely" replaced by the measured window: [1.406, 1.424] at 0.001, 0.018 wide against 0.506; edges ≤0.02 and width 0.00–0.03 under ±1% noise at 8 seeds; wide bands 0.28–0.51; the sharper principle about edge uncertainty; and the note that at 8 seeds the window disappears on none |
| §2.3, the withdrawn calibration | **X122 rewritten** | "the map it was fitted to is not reproducible under noise" → "the α_Φ window that does yield it is narrower than the uncertainty in its own edges under ±1% wealth noise" |
| §2.8, "Measured, not asserted" | none — proposition is X075 at first appearance | the mislabelled restatement now reads 51.5% value-weighted / 52.5% unweighted, cross-referenced to §1.6; observation 1 resolved |
| §3.9, the node-wealth ranks | **X159 rewritten** | ranks confirmed unchanged on the corrected field and the wealths added (296.0, 299.2, 266.5 against 316.6); observation 2 resolved |
| §1.10, the `highest_power` parenthetical | **X110 rewritten; X196 added** | the 79-of-79-node parse, the `venice` instance, the four fields it matches no share of, and the statement that what it holds was not determined and the model does not read it; provenance `derivation` → `file value`; **§** marker dropped; observation 4 resolved |

**Counts that moved.** 191 → **196** rows; 101 → **106** NEW (32 v4.0-origin unchanged, 69 → **74**
v5.0-origin); REVISED unchanged at **90**. Case 2 in answer (a) 65 → **70**; cases 1 and 3
unchanged, so **the answer to (a) is unchanged**: the fallback branch (X005–X011) is still the one
group standing on no replaced predecessor. Answer (b) moved from nine withdrawals to **eight**:
**W004 is subsumed by V004, not withdrawn**, which is a correction to this file rather than to the
spec. Marker counts: ⚑ unchanged at 43; **§ 6 → 5** (X110 no longer rests on one observation).
Provenance: numerical test 70 → 72, derivation 59 → 60, file value 28 → 29, stipulated 20 → 21,
engine test unchanged at 14, UNSOURCED still 0.

**Observations 3 and 6 are withdrawn** on the coordinator's argument, with a provenance residue
recorded under observation 3 (W071 is typed `UNSOURCED` in claims-v3.md and, after v5.0's
measurement, should be typed `derivation`). No spec change follows from either.
