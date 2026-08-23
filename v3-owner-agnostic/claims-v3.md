# Claim Inventory Delta — Per-Good Trade Network Spec v3.0

Extracted from `per-good-trade-spec.md` (v3.0, owner-agnostic wealth) as a **delta against
`../v2-drain/claims-v2.md`** (v2.0 body V001–V211 plus the v2.1 addendum V212–V230, itself a delta
against `../v1-laplacian/claims.md`, C001–C685). Extraction only: nothing here is validated,
corrected, or commented on. Three files were read — the v3.0 spec, `claims-v2.md`, and
`changes-v3.md`.

**Statuses.** Each claim in the v3 spec is one of:

- **UNCHANGED** — same proposition as an existing claims-v2.md / claims.md ID. The ID is recorded
  and not re-extracted.
- **REVISED** — the proposition changed. New `W` ID; the `Replaces` column names the old ID(s).
- **NEW** — no counterpart in either prior inventory.

**Conventions carried over:** the Type vocabulary (ENGINE / MODEL / DESIGN / OUTCOME / WORLD) and
the Provenance vocabulary (stipulated / derivation / file value / numerical test / engine test /
prose source / verified (method unstated) / UNSOURCED). A proposition stated in two sections keeps
one ID at first appearance. Adding an inline **[unverified in v3.0]** marker to an otherwise
identical sentence is *not* a proposition change — those stay UNCHANGED and are inventoried
separately below.

**⚑ marks a new engine fact introduced by a v3 fix** — the class that failed in both prior audits.
**§ marks a claim whose evidence is a single observation** rather than a repeated one.

**Full-strength sections** (extracted row-by-row regardless of overlap): **§1.3** and **§2.3** —
the wealth redefinition and the measured coefficients, per the extraction brief. Each measured
constant, each modifier-classification rule, and each time-basis claim is a separate row.

**Unresolvable IDs.** Ten v3 revisions replace sentences that entered in v1 and passed through v2
as UNCHANGED, so their IDs live in `claims.md`, which was not read. Those rows name the C-range and
say so. They are marked `†` and listed at the end.

---

# Summary

**195 delta claims extracted, W001–W195**, against 230 v2 claims: **130 NEW, 65 REVISED**
(replacing **51 claims-v2.md IDs**, plus C070 and 9 unresolved claims.md IDs).

Extracted in three passes: W001–W181 against the spec as received; W182–W192 after six gaps found
by that extraction were repaired; W193–W195 after the three remaining cross-reference decisions
were taken (see "Repairs made after first extraction" and "Internal cross-references"). Every row
below describes the spec as it now stands.

### Refutations and partials — status after the v3.0 repair pass

`changes-v3.md` reports **11 refutations** and **24 partials** from `validation-v2.md` folded
through. The first extraction of this delta found two that the spec text did not actually carry;
**both have since been applied to the spec** (see "Repairs made after first extraction" below), and
the rows above describe the corrected spec.

| Class | Count | Status |
|---|---|---|
| Refuted v2 IDs (V004, V029, V062, V107, V125, V126, V127, V134, V145, V159, V230) | 11 | **11 of 11 applied** — V230 repaired this pass |
| Partials tabulated in `changes-v3.md` | 19 IDs / 18 rows | **19 of 19 applied** — V225 repaired this pass |
| Partials claimed but not tabulated | 5 | **Still not identifiable** from the permitted sources |

**Five partials cannot be checked.** `changes-v3.md` states 24 partials narrowed but tabulates 18
rows covering 19 IDs (V016, V031, V036, V060, V086, V114, V123, V151, V153, V179, V180, V190,
V205, V214, V215, V216, V219, V222, V225). The remaining five are not named in any permitted
source, so whether they were folded through is unverifiable from here. **This is the one open item
in the refutation ledger.**

### Repairs made after first extraction

The delta was extracted first, then these gaps were fixed in the spec and the delta re-extracted
against the corrected text. Recording them because a claim inventory that silently absorbs its own
findings is worth less than one that shows them:

| # | What the extraction found | Fix |
|---|---|---|
| 1 | **V225 unapplied.** `changes-v3.md` narrows the gravity kernel to "66% in the reproduced construction"; §3.15 still said 69%, and `66%` occurred nowhere in the spec. | §3.15 now states 66% and names the superseded figure. **W190.** |
| 2 | **V230 applied inconsistently.** §2.8 carried the corrected proposition and pointed to "the note below the table" — no such note existed, the 10-of-159 measurement was absent, and §1.5 still carried the pre-refutation rationale *"`Φ_w` reads wealth, not goods, and is unaffected."* | §1.5 now carries the full activation treatment; §2.8's row points to §1.5. **W053, W182–W189.** |
| 3 | **Four figures `changes-v3.md` says are "flagged in place" were not.** | Markers added: hop counts (§3.2), node land-province counts (§3.3, both), 1.4e-14 / 5.96 (§3.10), every RANK figure (§3.15). |
| 4 | **V224's regenerated sink-count series was missing.** `changes-v3.md` §6 lists it among figures `v3measure.py` produced; §1.6 stated only the qualitative claim. | Series restored to §1.6; V224 is UNCHANGED, no longer orphaned. |
| 5 | **§1.5's gold argument cited the v2 wealth formula** `wealth = tax_income + production_income`, which §1.3 had replaced — the last live reference to the superseded definition. | Rewritten to the v3.0 argument: wealth reads no income field at all. **W191.** |
| 6 | **Three fixes landed in one section and not its counterpart** — §1.7 still filed probe 14 as open, §1.5 filed the gold field as a live residual, §3.13 said "§2.3 calls it numerical" after §2.3 stopped doing so. | All three updated. **W192**; W109 and W164 unchanged. |
| 7 | **Three cross-references needed a decision, not a transcription** — the missing §2.8 sink-set assertion, the preamble-vs-Efficiency contradiction, and §2.3's "Merchant power / efficiency" row. | Resolved in the section below. **W193–W195**; W010, W021, W065, W131 rewritten. |

### The latent-good rule, restated

The user-facing change in this pass. v2.1 held that a latent good leaves `Φ_w` alone because
"`Φ_w` reads wealth, not goods". `Φ_w` does read wealth — and **wealth reads the province's trade
good and its price**, which is exactly what activation changes. §1.5 now states the full
consequence: a province produces one good at a time, so activation *replaces* what it was
producing, and that moves both goods' supply shares, **every** good's demand vector `c`, both value
weights, and `Φ_w`. An activation is a world-state change on the scale of a conquest, not a local
addition (W182–W189).

### Delta claims by status and Type

| Type | NEW | REVISED | Total |
|---|---|---|---|
| MODEL | 44 | 36 | 80 |
| ENGINE | 40 | 9 | 49 |
| DESIGN | 24 | 13 | 37 |
| WORLD | 18 | 6 | 24 |
| OUTCOME | 4 | 1 | 5 |
| **Total** | **130** | **65** | **195** |

### Delta claims by Provenance

| Provenance | Count |
|---|---|
| derivation | 97 |
| stipulated | 28 |
| numerical test | 26 |
| engine test | 25 |
| file value | 17 |
| UNSOURCED | 2 |
| **Total** | **195** |

**`engine test` provenance appears for the first time in this project.** claims.md recorded that no
v1 claim was sourced to `engine test`; claims-v2.md recorded the same for v2. v3.0 carries **25**,
all of them from one session (`../v2-drain/game-session.md`) against a 1.37.5 install. That is the
largest single change in the evidence profile, and "Single-observation evidence" below is its cost.

**`derivation` is now the plurality provenance (97 of 195, 50%, against v2's 34%).** Most of the
increase is the reasoning attached to fixes — "v2 said X, the correct reading is Y" — rather than
new load-bearing inference. §3.16 records that three of the sixteen refuted ENGINE claims carried
`derivation`, so the class is not self-certifying.

### UNSOURCED delta claims (2)

By the spec's own §3.16 rule each is a to-do, not a fact:

| ID | Claim |
|---|---|
| W066 | Trade efficiency "also feeds the caravan-power and collection tooltips" — no define, file path or string cited |
| W071 | Caravan power at the cap is "enough to move a node's power shares by itself, and therefore to push other countries across the thresholds" — no measurement, and its premise V168 is itself `[unverified in v3.0]` |

*(W131 was the third until this pass: the assertion it referred to now exists in §2.8 as two rows,
W193–W195.)*

### v2 UNSOURCED claims: four now settled, six still open

Of claims-v2.md's ten UNSOURCED claims, the game session closed four:

| ID | Was | Now |
|---|---|---|
| V067 | whether `NextNodeButton` accepts an assignment | **settled** — it only navigates (W111) |
| V096 | whether the engine requires topological declaration order | **settled** — it validates, logs, and tolerates (W099, W114) |
| V105 | whether power appears upstream where the country holds none | **settled** — it does (W068) |
| V149 | the engine's behaviour on a cyclic file | **settled** — `EXCEPTION_STACK_OVERFLOW` (W101) |

Still UNSOURCED and carried into v3.0 unchanged: **V001** (1.37.5 is the final patch), **V043**
(the 75% overseas rule is pre-Common-Sense), **V054** (whether the per-province production-income
field carries gold), **V071** (trade range gates placement, not flow), **V072** (no trade supply
range in the engine), **V084** (ironman saves are binary-encoded). **V054's only settling route was
deleted this revision** — §2.7 item 12 was dropped rather than run (W109). §1.5 now records the
question as **moot as well as unknown**: nothing in the model reads that field. It stays an
UNSOURCED claim, but it is no longer load-bearing, which is the right resting place for it.

### Orphaned claims-v2.md IDs

**No v2 claim was dropped outright without a replacement.** Two propositions survive only in
compressed form (a third, V224, was restored to §1.6 this pass and is now UNCHANGED):

| ID(s) | What happened |
|---|---|
| V044, V045, V046, V047 | The four autonomy floors leave the model entirely (§1.3 is owner-agnostic) but survive as facts in §3.16: *"1.37 has regime floors of 90/50/20/0"*. The four **values** are still asserted; the **per-regime attributions** (`territory_core`/`territory_non_core` → 90%, colonial core → 50%, pasha → 20%, stated core → 0) and the `00_static_modifiers.txt` citation are not. Compressed, not orphaned. V042 and V043 are stated in full in §3.16. |
| V001 | The header's "final patch" wording is gone (v2: *"EU4 (final patch, 1.37.5 Inca)"*; v3: *"EU4 1.37.5 Inca"*), and §2.3 now says *"Re-measure them against any patch that is not 1.37.5"*. The proposition survives at §2.5 ("The binary is frozen — offsets found stay found"). |

### v1 claims that v2 orphaned and v3 re-adopts

Two propositions from the six v2 orphaned as "§1.1 Laplacian solve machinery" (C013–C018) return
in §2.2a, which is the point of that section:

- **`Σ_n b_g(n) = 0` identically** — the balance condition, restated as W016 with a new reason
  (both `s` and `c` are world shares).
- **Per-component renormalisation** — restated as W080. The spec says so explicitly: *"v1 carried
  per-component renormalisation and v2 dropped it without replacement; v3 restores the
  requirement."*

The other four (singularity of `L`, pinning, the isolated-node skip) stay orphaned — there is no
Laplacian to be singular.

### ⚑ New engine facts introduced by v3 fixes (45)

The class that failed in both prior audits. Grouped:

- **Wealth coefficients, the tooltip model and the local-modifier rule (18):** W031, W033, W034,
  W035, W037, W038, W040, W041, W042, W043, W044, W045, W046, W089, W092, W093, W094, W095.
- **Latent-good activation (2):** W188, W189.
- **Declaration order, cycles and link reversal (7):** W099, W100, W101, W103, W104, W107, W114.
- **Prices and price events (6):** W132, W133, W143, W144, W146, W167.
- **Merchants and caravans (3):** W065, W066, W070.
- **Run-to-run variance (3):** W117, W118, W179.
- **Measurement provenance corrections (3):** W063, W115, W154.
- **Propagation (2):** W067, W068.
- **UI behaviour (1):** W111.

**Twenty-six of the 45 are entirely new territory** — the wealth block and the game-session
results. This is the largest single injection of unaudited engine facts in the project's history,
and it lands in the two sections the extraction brief singled out.

### § Single-observation evidence (19)

Every claim below rests on **one** observation. The spec flags exactly one of them (W094's
`TAX_COEFF`, in §3.13); the other sixteen are stated without a repeat and without a null.

| ID(s) | The single observation |
|---|---|
| W033, W034, W035, W037, W038, W046 | **One province** — Garnatah (223) — carries the entire time-basis argument, the modifier-ordering rule, and the owner/local classification's worked example |
| W092, W093, W094, W095, W096 | The same one province carries **both** measured engine constants. §3.13 flags `TAX_COEFF`'s single point and not `GP_COEFF`'s, though both were read from the same tooltip session |
| W068 | One country (France) in one node (Sevilla), one tooltip line |
| W100 | One launch of the all-159-links-reversed file |
| W103, W104 | One hand-reversed link (`sevilla` → `valencia`), one launch — described in the spec as "the mod's core premise verified end to end" |
| W107 | One node window |
| W111 | One click (`Safi` in Sevilla's window) |
| W117 | n = 2 — two vanilla runs establish the noise floor that every other engine-test claim is measured against |
| W179 | One permuted-file run — the false positive §3.16 now uses to argue that a single measurement without a null is not evidence |

**The one probe that was repeated** is the cycle crash (W101: "reproduced on two launches, with
vanilla and the reversed-order file both loading fine as controls"). It is the only engine-test
claim in v3.0 carrying both a repeat and a null.

### `[unverified in v3.0]` inventory

The spec now marks **10** figures inline, up from 7. `changes-v3.md` §6 says of its
not-regenerated list that "each is flagged in place in the spec where it appears" — which was not
true of four of them until this pass. Current state:

| Figure | Where | Marked |
|---|---|---|
| Barbell: sinks 14% top decile vs 7% bottom | §2.8 | ✓ (was already) |
| 24% spice-through-Cape | §3.2 | ✓ (was already) |
| 5.7e-14 income-factoring agreement | §3.10 | ✓ (was already) |
| Nineteen countries at the caravan cap, 2–10% near-miss list | §3.11 | ✓ (was already) |
| Calibration span 1..5, spearman −0.54 | §3.13 | ✓ (was already) |
| BASIN 88.5% reach | §3.15 | ✓ (was already) |
| 3 hops to the Channel vs 7 via Alexandria | §3.2 | ✓ **added this pass** |
| Node land-province counts 19 / 77 | §3.3 | ✓ **added this pass** |
| Node land-province counts 68 / 33 | §3.3 | ✓ **added this pass** |
| 1.4e-14 and the 5.96-ducat propagation error | §3.10 | ✓ **added this pass** |
| Every RANK figure — ρ_val +0.281 / +0.053, 46.6% / 14.1%, 83.3%, 34 orphans, 9 net-producer sinks, 11–17 sinks per good | §3.15 | ✓ **entry-wide marker added this pass**, replacing the single marker on "34 orphan sinks" |

The RANK marker was widened deliberately: `changes-v3.md` names "RANK 83.3% / 34 orphans" and "the
sink–demand correlation ρ_val figures" separately, and the 9-net-producer-sinks and 11–17-sinks
figures appear in *neither* its regenerated list nor its unverified list. All of them came from the
same v2 validation pass, so the entry now carries one marker covering the lot rather than a marker
whose scope had to be guessed.

### Internal cross-references that a v3 fix left dangling

**All seven found at first extraction are now resolved** — four transcriptions (repair-table items
1–4) and three that needed a decision:

1. **§3.2 vs §2.8 — sink-set assertion. Resolved as two checks, not one.** §2.8 now carries a
   `Sink set, 2-core` row and a `Sink set, pendants` row. Containment inside the 2-core is a hard
   unconditional assertion (**W193**); the equality is *monitored* with **T2** named as its
   legitimate failure (**W194**); on pendant edges the Phase-4 orientation rule is the check and
   **T1** is expected output, not a fault (**W195**). §3.2's counterexamples are now labelled T1
   and T2 so the assertion rows can name them. W131 is no longer UNSOURCED.
   *One deviation from the instruction as given, flagged:* the 2-core check was specified as
   equality firing unconditionally. T2 sits **inside** the 2-core, so an unconditional equality
   assert would halt on correct behaviour — the same trap §2.2a names for pendants. What holds
   unconditionally in the core is the ⊆-direction, which §3.2 already says. The row therefore
   asserts containment and monitors equality. That keeps both counterexamples visible, which was
   the stated reason for splitting the assertion in the first place.
2. **§1.1 preamble vs Efficiency. Resolved in the Efficiency bullet's favour.** The preamble's
   "all verified on 1444 data" was the wrong sentence. It now reads "measured where measurement
   applies", and the property vocabulary is three-way: proved for any input, measured with its
   missing premise named, or true by construction and carrying no measurement (**W010**).
   Efficiency is the third kind — the LP objective *is* `Σ (flow × hops)`, so a hop count would
   re-derive the objective rather than test it (**W021**). No measurement was invented.
3. **§2.3 defines table. Fixed by splitting the row** into "Merchant trade power"
   (`MERCHANT_MAX_POWER_BONUS`) and "Merchant income bonus" (`TRADE_MERCHANT_PRESENT`), the latter
   noting it is a bonus on income and not trade efficiency. The C070 correction now holds in §1.7
   and §2.3 both (**W065**).

---

## §0 — Front matter (lines 1–24)

**UNCHANGED:** C002, C003, C004, V001 *(via §2.5)*, V002, V003, V004.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W001 | REVISED | The target is **connected maps only** (§2.2a); v2's "map-agnostic" target is withdrawn. | DESIGN | stipulated | C001–C004 † (the header "map-agnostic" clause) | W078, W088 |
| W002 | NEW | v3.0's first change: wealth becomes **owner-agnostic** — a property of the place, not of who holds it (§1.3, §3.3). | MODEL | stipulated | — | W023 |
| W003 | NEW | v3.0's second change: every refutation and partial in `../v2-drain/validation-v2.md` is folded through. | WORLD | stipulated | — | — |
| W004 | NEW | Four v1 corrections that v2 never applied are folded in with them. | WORLD | stipulated | — | V004 |
| W005 | NEW | v3.0's third change: the four game probes settled in `../v2-drain/game-session.md` are applied, two of them reversing v2's stated position (§2.4, §1.9). | WORLD | stipulated | — | W108 |
| W006 | NEW | Every measured number in v3.0 carries the script that produced it, and anything not regenerated for v3.0 is marked **[unverified in v3.0]**. | DESIGN | stipulated | — | — |

## §1.1 — Trade direction (lines 28–109)

**UNCHANGED:** C005, C006, C010, C011, C012, C019, C020, C021, C022, V005, V006, V007, V008,
V009, V010, V011, V012, V013, V014, V015, V017, V018, V019, V020, V021, V022, V023, V024, V026,
V027, V028, V030, V032, V033, V034, V035.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W007 | REVISED | The flow support is a spanning-tree basis of ≤ N−1 edges **when the solver returns a basic (vertex) optimum**, which the simplex family does. | MODEL | derivation | V016 | V015 |
| W008 | NEW | An interior-point solve without crossover can split flow across equal-length parallel paths and return a support containing an undirected cycle. | MODEL | derivation | — | W007 |
| W009 | NEW | What holds for *any* optimum is the weaker and sufficient property: the support contains no **directed** cycle. | MODEL | derivation | — | V017, W007 |
| W010 | REVISED | The §1.1 properties are stated as checkable claims and **measured where measurement applies**: each says whether it is proved for any input (naming the proof), only measured (naming the premise a proof would need), or true by construction and carrying no measurement. The three are never allowed to stand for each other. | DESIGN | stipulated | V025 | W021 |
| W011 | NEW | That discipline is what caught four over-claims between v2.0 and v3.0. | WORLD | derivation | — | W010 |
| W012 | REVISED | Every sink is a selected demand centre that turned out flow-terminal, a stall-promoted flow-terminal demander, **or a Phase-0 pendant that absorbed a net-importing subtree**. | MODEL | derivation | V029 | V007, V011, V022 |
| W013 | REVISED | On a map where Phase 0 is a no-op the third case is empty and the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — **measured** exact, 29/29 goods on 1444, not derived. | MODEL | numerical test | V029, V125, V126 | W012, V009 |
| W014 | NEW | That equality is **not a theorem in general**, and v2 asserted it as one. | WORLD | derivation | — | W013, W126, W128 |
| W015 | REVISED | Reachability is a feasibility theorem **on a connected map**: the orientation contains a flow serving 100% of demand because the LP imposes node balance and `Σ_n b_g(n) = 0` identically. | MODEL | derivation | V031 | V015, W016, W078 |
| W016 | NEW | `Σ_n b_g(n) = 0` holds identically because both `s` and `c` are world shares. | MODEL | derivation | — | V005 |
| W017 | NEW | On a disconnected map, balance must hold per component and share normalisation does not deliver it — a two-component graph with cross-component imbalance is **infeasible outright**, and the solver returns no flow at all rather than a worse one. | MODEL | derivation | — | W016 |
| W018 | NEW | Vanilla 1444 is **one component** (measured). | ENGINE | numerical test | — | — |
| W019 | REVISED | Unit costs make the certificate flow a fewest-hop routing **in aggregate**: the objective is `Σ (flow × hops)`, so the optimum minimises total flow-hops. | MODEL | derivation | V036 | V015 |
| W020 | NEW | No per-unit shortest-path claim is made and none holds — a unit may detour when sink assignment demands it. | MODEL | derivation | — | W019 |
| W021 | NEW | Efficiency **carries no measurement and wants none**: it is true by construction of the LP, so any hop count would re-derive the objective rather than test it. The §3.13 calibration degrades it, which is a change to the program being solved, not evidence about the property. | DESIGN | derivation | — | W019, V180 |
| W022 | REVISED | The LP is deterministic **on one machine and one build** (six identical solves, one orientation); across machines it is the open question of §3.13. | MODEL | numerical test | V037 | V015, V183 |

## §1.2 — Supply (lines 111–122)

**UNCHANGED:** C023, C025, C026, C027, C028, V038, V039, V040, V041. No delta claims.

## §1.3 — Demand (lines 124–181) — full-strength extraction

**UNCHANGED (carried, not re-extracted):** C031, C032, C033, C035, C036, C039 — including the
per-province α-weighted demand share `c(n,g) = Σ_{p∈n} wealth(p)^α / Σ_{q∈world} wealth(q)^α`,
which is unchanged in form; only what `wealth(p)` means changed.

**Note on the autonomy floors:** V042–V047 are *not* revised here. §1.3 does not correct them — it
**removes them from the model**. They survive as EU4 facts in §3.16 (see the orphan table above).
Only V048, which put them in the pipeline, is replaced.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W023 | REVISED | **Wealth is owner-agnostic**: a property of the place — what the land is worth per year, before anyone's government touches it. | MODEL | stipulated | V048 | — |
| W024 | NEW | Excluded by name: autonomy, production efficiency, national ideas, estate modifiers, government modifiers, technology. | MODEL | stipulated | — | W023 |
| W025 | NEW | Two provinces with the same terrain, development and trade good have the same wealth whoever owns them. | MODEL | derivation | — | W023 |
| W026 | NEW | A province's wealth does not change when it is conquered. | OUTCOME | derivation | — | W023 |
| W027 | NEW | `goods_produced(p) = GP_COEFF · base_production(p)`, plus local flat goods bonuses. | MODEL | derivation | — | W092, W039 |
| W028 | NEW | `trade_value(p) = goods_produced(p) · price(good(p))`, in ducats per **year**. | MODEL | derivation | — | W027, W033 |
| W029 | NEW | `tax_value(p) = TAX_COEFF · base_tax(p)`, in ducats per **year**. | MODEL | derivation | — | W094, W033 |
| W030 | REVISED | `wealth(p) = tax_value(p) + trade_value(p)`, in ducats per year — trade value, not production income. | MODEL | derivation | C031–C039 † (`wealth(p) = tax_income(p) + production_income(p)`) | W028, W029 |
| W031 | NEW | ⚑ Neither coefficient is a define: `defines.lua` and `common/defines/` were searched and contain neither. | ENGINE | file value | — | — |
| W032 | NEW | Both are therefore engine constants recovered by observation, and each carries the observation that produced it. | DESIGN | stipulated | — | W031 |
| W033 | NEW | ⚑§ **Time basis:** the engine's province tooltips give both terms as *annual* quantities divided by twelve for display. | ENGINE | engine test | — | W034, W035 |
| W034 | NEW | ⚑§ The tax tooltip reads `Base: 0.49 (Yearly 6.00)` for a province with `base_tax = 6`. | ENGINE | engine test | — | W037 |
| W035 | NEW | ⚑§ The production tooltip reads `Trade Value: +0.26 … yearly income of 3.25` for a province whose window shows an annual `Trade Value` of 3.20. | ENGINE | engine test | — | W037 |
| W036 | NEW | Both monthly figures are the annual value over twelve, so the annual forms add directly with **no conversion**. | MODEL | derivation | — | W033, W034, W035 |
| W037 | NEW | ⚑§ All of it was measured on **Garnatah, province 223** — `base_tax` 6, `base_production` 4, silk, `local_autonomy` 0. | WORLD | engine test | — | — |
| W038 | NEW | ⚑§ **Modifier order:** modifiers apply *after* the coefficient, as a percentage on the base — `Base 0.49` then `Tax Income Efficiency 125.0%`, giving 0.61. | ENGINE | engine test | — | W037 |
| W039 | NEW | **Flat goods bonuses are the exception:** they add into `goods_produced` *before* the price multiply, which is why they appear in the goods-produced tooltip as their own line (`Base Goods Produced: 0.80 / Base Production: +0.80`). | ENGINE | derivation | — | W093, W158 |
| W040 | NEW | ⚑ **The local/owner rule:** a trade good's `province = { … }` block is province-scoped and attaches to the place; its `modifier = { … }` block is country-scoped and attaches to the owner. Only the first kind is local. | ENGINE | file value | — | — |
| W041 | NEW | ⚑ In vanilla the income-relevant local modifiers are **exactly three**. | ENGINE | file value | — | W040 |
| W042 | NEW | ⚑ `gems` carries `local_tax_modifier = 0.15`. | ENGINE | file value | — | W041 |
| W043 | NEW | ⚑ `glass` carries `local_production_efficiency = 0.1`. | ENGINE | file value | — | W041, W160 |
| W044 | NEW | ⚑ `incense` carries `trade_value_modifier = 0.1`. | ENGINE | file value | — | W041 |
| W045 | NEW | ⚑ Terrain and climate carry no income-relevant local modifier: `terrain.txt` grants only development cost, supply limit and defensiveness. | ENGINE | file value | — | W040 |
| W046 | NEW | ⚑§ What the engine itemised on a real province and the model excludes: `Core` +75%, `Reform Iqta` +5%, `Clergy` +5%, national ideas +15%, technology production efficiency +2%. | ENGINE | engine test | — | W037 |
| W047 | NEW | Each of those is owner-derived — a fact about the owner's relationship to the province, its government, its estate, its ideas or its technology — and is excluded by the rule. | MODEL | derivation | — | W040, W046 |
| W048 | NEW | `City` (+25%) is place-intrinsic but **constant across every province the model counts**. | ENGINE | derivation | — | W046, W050 |
| W049 | NEW | So `City` cancels in the normalised share and is not carried. | MODEL | derivation | — | W048 |
| W050 | REVISED | Unowned provinces are outside the model: `s` and `c` are computed over provinces with an owner **and `is_city = yes`**, because an unowned province produces nothing the trade system can move. | MODEL | stipulated | C031–C039 † ("Unowned provinces generate no income and contribute nothing") | W023 |
| W051 | NEW | What this buys: demand responds only to what is there — a conquest no longer moves the demand vector on the day it happens; only development, trade goods and prices do. | OUTCOME | derivation | — | W023, W026 |
| W052 | NEW | It also removes the single largest source of hidden owner-dependence from the aggregate graph (§1.6), which is built from this same wealth field. | MODEL | derivation | — | W023, V212 |

## §1.4 — Market concentration (lines 183–193)

**UNCHANGED:** C040, C041, C042, C043, C044, C045, C046, C047. No delta claims.

## §1.5 — Goods without a graph (lines 195–240)

**UNCHANGED:** C048, C051, C052, C053, C054, C055, C056, V050, V051, V052, V053, V054, V055,
V056, V057, V058.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W053 | REVISED | `Φ_w` is unaffected **only while a good stays latent**; activation reprices its provinces and does move `Φ_w`, because §1.6 runs DRAIN on the wealth field and wealth reads the province's good. | MODEL | derivation | V230 | W023, V212 |
| W182 | NEW | A province produces exactly **one trade good at a time**, so a latent good going live *replaces* what that province was producing. | ENGINE | derivation | — | — |
| W183 | NEW | In the month it converts, the new good gains a producer and the old good loses one, so **both** goods' supply shares `s(·,g)` renormalise across every node that produces either. | MODEL | derivation | — | W182, C023 |
| W184 | NEW | The province is repriced, so `wealth(p)` changes and with it `c(n,g)` for **every good in the game** — not just the two — because §1.3 makes one wealth field the demand base for all of them. | MODEL | derivation | — | W182, W028, W030 |
| W185 | NEW | `V_g` moves for both goods, reweighting every display, link value and AI score. | MODEL | derivation | — | W182, C059 |
| W186 | NEW | An activation is therefore a world-state change on the scale of a development change or a conquest, and **every graph in the model is entitled to move on it**. | OUTCOME | derivation | — | W183, W184, W185, W053 |
| W187 | NEW | Measured: repricing to coal the 45 owned latent-coal provinces flips **10 of 159 `Φ_w` edges**. | MODEL | numerical test | — | W053, W188 |
| W188 | NEW | ⚑ **45** of the 58 latent-coal provinces are owned at 1444 — §1.3 counts only owned provinces. | ENGINE | file value | — | V057, W050 |
| W189 | NEW | ⚑ Coal's base price of **10.0 is the highest in vanilla**, so a coal activation is near the upper end of what one good's activation can do. | ENGINE | file value | — | W133 |
| W191 | REVISED | Gold income is invisible to demand entirely because v3.0's `wealth(p)` is built from `base_tax`, `base_production` and price and reads **no income field at all** — not merely because gold income is booked to its own engine category. | MODEL | derivation | V049 | W030, V050 |

*(V054 stays UNCHANGED and UNSOURCED, but §1.5 now records it as **moot** as well as unknown:
nothing in the model reads the per-province production-income field, which is why §2.7 item 12 was
dropped rather than run — W109.)*

## §1.6 — The aggregate graph (lines 242–297)

**UNCHANGED:** C059, C062, V063, V064, V212, V213, V217, V220, V221, V223, V224; V218 is narrowed
in §2.2a (W085), not here.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W054 | REVISED | Scale invariance holds **in exact arithmetic**: Phase 0 reads signs, Phase 1's HHI is built from mass shares, the LP optimum scales linearly with identical net-flow signs, and the priority key is order-isomorphic under positive scaling. | MODEL | derivation | V214 | V212 |
| W055 | NEW | The implementation adds one premise: the zero-flow tolerance is **absolute** (`1e-11`), so scaling `b` *down* pushes genuine flow arcs into the free set. | MODEL | derivation | — | W054, W098 |
| W056 | NEW | Measured: identical orientation at ×1 and above, **13 edge flips at ×10⁻²**, and at **×10⁻⁶ the sink set collapses to a single node**. | MODEL | numerical test | — | W055 |
| W057 | NEW | 1444's `b_w` has largest magnitude **0.0226**, so normalising into (−1, 1) scales it *up* and is safe; scaling down is not. | MODEL | numerical test | — | W055 |
| W058 | NEW | Either scale `b` up, or scale the tolerance with it. | DESIGN | derivation | — | W057 |
| W059 | REVISED | `hangzhou` and `english_channel` rank 3 and 2 **in the α_Φ-weighted wealth field `c_w`** — *not* in raw node wealth, where they are 12th and 1st; v2 wrote "wealth ranks" without saying which, and the plain reading is wrong. | MODEL | numerical test | V215 | V212, V213 |
| W060 | REVISED | The eight sources are all in the **bottom half of the wealth field** (`c_w` ranks 44–75), with mean degree **3.1** against the map's 4.0 — v2 called them "cul-de-sacs", which their degrees do not support. | MODEL | numerical test | V216 | V212 |
| W061 | REVISED | `Φ_w` agrees with the per-good graphs on 53.4% of edge-goods (52.1% value-weighted) against `Φ_ord`'s **60.2%** — a gap of **6.8 points, not the 9.3 v2 quoted**. | MODEL | numerical test | V219 | W062 |
| W062 | REVISED | `Φ_ord`'s edge-good agreement is **60.2%**, measured under the deterministic sweep. | MODEL | numerical test | V062 | V059 |
| W063 | NEW | ⚑ v2's 62.7% was measured under the **old scan-order sweep** and was never regenerated after §3.6 adopted the deterministic one. | WORLD | derivation | — | W062 |
| W064 | NEW | Transient extra sinks at intermediate wealth boosts are expected behaviour, not noise. | MODEL | stipulated | — | V223, V224 |

## §1.7 — Merchants (lines 299–325)

**UNCHANGED:** C067–C083, V066, V068, V069, V070.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W192 | REVISED | §1.7's UI change is a **new interaction on an existing widget**, not a behaviour change to one that already dispatches: probe 14 settled that the incoming entry only navigates today. | DESIGN | derivation | V065, V104 | W111, V066 |
| W065 | REVISED | ⚑ A merchant present gives +2 trade power (`MERCHANT_MAX_POWER_BONUS`) and a **+10% bonus on trade income** (`TRADE_MERCHANT_PRESENT = 0.1`, shipped comment "bonus on income if trade present") — **not** +10% trade efficiency. §2.3's constants table now splits the two into separate rows, so the correction holds in both places. | ENGINE | file value | C070 | — |
| W066 | NEW | ⚑ Trade efficiency and a flat income bonus are different quantities in EU4; efficiency also feeds the caravan-power and collection tooltips. | ENGINE | UNSOURCED | — | W065 |

## §1.8 — Collection and transfer (lines 327–350)

**UNCHANGED:** C084–C102, V071, V072. No delta claims.

## §1.9 — Trade power propagation (lines 352–361)

**UNCHANGED:** C103, C104, C105, C106, C107, C108, C109, C110, C111, V073.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W067 | NEW | ⚑ The tooltip's receiving-side qualifier — power transfers "to trade nodes where it already has power" — is **descriptively false**; §1.9's "every immediately upstream node" is correct as written and gains no qualifier. | ENGINE | derivation | — | W068, V073 |
| W068 | NEW | ⚑§ Measured: France holds zero provinces and zero merchants in Sevilla and still appears there with **3.3 power**, itemised by the engine as `Transfers from traders downstream: +3.1` and nothing else. | ENGINE | engine test | — | — |
| W069 | REVISED | This line was §3.16's cautionary case; it is now **closed, in the spec's favour**. | WORLD | derivation | V211, V105 | W067 |

## §1.10 — Direction-dependent systems (lines 363–406)

**UNCHANGED:** C112–C143, V074, V075, V076, V077, V078, V079, V080.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W070 | REVISED | ⚑ Caravan power is **not a function of raw trade power at all** — not a step function on it: it is total country development ÷ `CARAVAN_FACTOR` plus policy and idea modifiers, clamped to [`CARAVAN_POWER_MIN`, `CARAVAN_POWER_MAX`], switched on by a merchant condition. | ENGINE | file value | C112–C143 † ("a step function on raw power") | V167 |
| W071 | NEW | When it applies it is worth up to the cap for any major power — enough to move a node's power shares by itself, and therefore to push *other* countries across the §1.10 thresholds. | OUTCOME | UNSOURCED | — | W070, V168 |

## §1.11 — Treasure fleets (lines 408–414) · §1.12 — What the game displays (lines 416–437)

**UNCHANGED:** C144–C148, C149–C165, V049, V065, V081. No delta claims.

## §2.1 — Shape (lines 439–456)

**UNCHANGED:** C167–C184, V082, V083, V084, V085.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W072 | REVISED | The sweep is deterministic given the LP's support and a fixed accumulation order, and its comparisons are of **input-derived floats** (`DEF`, `b`) rather than solver residuals — the distinction that matters against v1's dense algebra — **but it is not integer arithmetic, and v2 called it that**. | MODEL | derivation | V086 | V020 |
| W073 | NEW | The sweep's cross-machine reproducibility therefore reduces to the LP's. | MODEL | derivation | — | W072, V183 |

## §2.2 — Solver (lines 458–485)

**UNCHANGED:** C185–C209, V064, V090, V091, V092, V229.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W074 | REVISED | Solver item 4 computes **owner-agnostic** per-province wealth — `TAX_COEFF · base_tax + GP_COEFF · base_production · price`, local goods modifiers only, no autonomy, efficiency, ideas or owner terms — then per-node `trade_value`, `s`, `c` with per-province α, and `b = s − c`. | DESIGN | stipulated | V087 | W023, W030 |
| W075 | REVISED | Solver item 5 requires **network simplex or a simplex LP, not interior-point without crossover**, because §1.1's spanning-tree-basis property requires a basic optimum. | DESIGN | stipulated | V088 | W007, W008 |
| W076 | REVISED | The Phase-4 evaluator's `unserved` and `stranded` must be equal by conservation **because `Σ_n b_g(n) = 0` identically**. | MODEL | derivation | V089 | W016 |

## §2.2a — What map this is for (lines 487–526) — new section

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W077 | NEW | v2 called the target "map-agnostic" while proving its central properties only for the map it was measured on. | WORLD | derivation | — | W001 |
| W078 | NEW | **Premise 1 — the node graph is connected.** Reachability is LP feasibility, and feasibility rests on connectedness. | MODEL | derivation | — | W015, W017 |
| W079 | NEW | On more than one component each component must balance separately, and share normalisation does not deliver that. | MODEL | derivation | — | W016, W017 |
| W080 | NEW | The solver computes components once at load; on more than one it must either renormalise `s` and `c` **within each component** or refuse to start and say which nodes are unreachable — it must not silently hand an infeasible program to the LP. | DESIGN | stipulated | — | W079 |
| W081 | NEW | Per-component renormalisation makes each component its own closed economy — the honest reading of a disconnected map. | DESIGN | derivation | — | W080 |
| W082 | NEW | v1 carried per-component renormalisation, v2 dropped it without replacement, and v3 restores the requirement. | WORLD | derivation | — | W080 |
| W083 | NEW | **Premise 2** — several §1.1 properties are proved for the 2-core and hold on any map where Phase 0 removes nothing (minimum degree ≥ 2, no bridges — true of vanilla). | MODEL | derivation | — | V007, V009 |
| W084 | REVISED | Where Phase 0 acts, **sink-set equality fails**: a pendant net-importer is a sink outside the set. | MODEL | derivation | V029 | W012, W126 |
| W085 | REVISED | Where Phase 0 acts, **the marking-order reconstruction fails**: pendants have no marking order, so `Φ_ord`-style order comparison is undefined on pendant edges. | MODEL | derivation | V060, V218 | V007 |
| W086 | NEW | Global DAG and free-edge determinism both survive where Phase 0 acts — pendant edges are bridges, and peeling does not touch the priority key. | MODEL | derivation | — | V027, V034 |
| W087 | NEW | A fourth breaking case is independent of Phase 0: inside the 2-core, a selected flow-terminal demander can lose sinkhood to a free edge that reaches an earlier-marked node. | MODEL | derivation | — | W128 |
| W088 | NEW | The stated target: on a connected map with minimum degree ≥ 2 every §1.1 property is proved or measured-and-labelled; on a connected map with pendants the algorithm still produces an acyclic, fully-oriented, demand-serving graph and only the *characterisations* weaken; on a disconnected map the solver renormalises per component or refuses. | DESIGN | derivation | — | W080, W083, W084, W085 |

## §2.3 — Constants (lines 528–566) — full-strength extraction

**UNCHANGED:** C211, C212, C213, C214, C215, C216, C217, C218, C219, C220, C222, C223, C224,
C225, C226, C227 (the defines table and "Read at runtime; never hardcoded"), V094, V213, and the
DLC-state third-axis claim. *(The merchant row is now two rows — "Merchant trade power" and
"Merchant income bonus" — which corrects the label, not a proposition; the proposition is W065.)*

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W089 | NEW | ⚑ The two wealth coefficients of §1.3 are **hardcoded in the binary**. | ENGINE | derivation | — | W031 |
| W090 | NEW | They are therefore *measured*, and each is recorded with the observation that produced it. | DESIGN | stipulated | — | W089 |
| W091 | NEW | Re-measure them against any patch that is not 1.37.5. | DESIGN | stipulated | — | W089 |
| W092 | NEW | ⚑§ **`GP_COEFF` = 0.2** goods produced per point of `base_production`. | ENGINE | engine test | — | W093 |
| W093 | NEW | ⚑§ Measured on Garnatah (province 223), `base_production = 4`, goods-produced tooltip `Base Goods Produced: 0.80 / Base Production: +0.80`. | ENGINE | engine test | — | W037 |
| W094 | NEW | ⚑§ **`TAX_COEFF` = 1.0** ducat/year per point of `base_tax`. | ENGINE | engine test | — | W095, W162 |
| W095 | NEW | ⚑§ Measured on the same province, `base_tax = 6`, tax tooltip `Base: 0.49 (Yearly 6.00)`. | ENGINE | engine test | — | W037 |
| W096 | NEW | §Both were read with `local_autonomy = 0`, so no owner term was in play. | ENGINE | engine test | — | W037 |
| W097 | NEW | Prices come from `common/prices/00_prices.txt` at runtime and are never hardcoded. | DESIGN | file value | — | — |
| W098 | REVISED | The design constants are the excluded-goods list, `P₀ = 2.0`, **`α_Φ = 1.5`**, and DRAIN's three knobs at defaults — and the zero-flow tolerance `1e-11` is **not** purely numerical: it is absolute, so it couples to the scale of `b`. | DESIGN | stipulated | V093 | W055, V213 |

## §2.4 — The tradenodes file (lines 568–601)

**UNCHANGED:** C228–C233, C235–C242, V095, V148, V215, V221.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W099 | REVISED | ⚑ The engine performs no topological sort but **validates** that the file is one, logging `[tradenodedefinition.cpp:61]: X=>y ( ERROR: Trade nodes must always be defined so that an outgoing is defined after in the file, or we get processing errors)` once per violating link — and then **tolerates** the violation. | ENGINE | engine test | C234 †, V096 | — |
| W100 | REVISED | ⚑§ Measured: a file with all 159 links declared backwards logged exactly 159 such errors and then loaded and played normally, with node `total` and `retention` unchanged and the power-dependent fields differing only within the engine's own run-to-run variance. | ENGINE | engine test | — | W099, W117 |
| W101 | REVISED | ⚑ What the engine does **not** tolerate is a cycle: a hand-authored two-node cycle produced `EXCEPTION_STACK_OVERFLOW` with 1002 stack frames at a single return address, reproduced on two launches, with vanilla and the reversed-order file both loading fine as controls. | ENGINE | engine test | V149 | V148 |
| W102 | REVISED | Acyclicity is a hard correctness requirement of the emitter, **established by observation** rather than assumed. | DESIGN | derivation | V150 | W101 |
| W103 | NEW | ⚑§ A reversed link is honoured completely: moving one `outgoing` block from `sevilla` to `valencia` — path list reversed, control pairs reversed — loaded with **zero** errors and rebuilt the economy around the new direction. | ENGINE | engine test | — | — |
| W104 | NEW | ⚑§ Its five observed consequences: Valencia moved from Sevilla's outgoing side to its incoming side; Sevilla became an end node with zero outgoing value; Castile's merchant switched from steering to collecting; the two countries holding power in Sevilla purely by downstream propagation disappeared from the node; every provincial power figure was unchanged. | ENGINE | engine test | — | W103 |
| W105 | NEW | This is the mod's core premise verified end to end. | WORLD | derivation | — | W103, W104 |
| W106 | REVISED | Declaration order is emitted in decreasing `Φ_w` marking order because it is the convention the engine states and the shipped file follows; **violating it is non-fatal** but logs one error per link. | DESIGN | derivation | C234 † | W099, V095 |
| W107 | NEW | ⚑§ The node window renders its incoming/outgoing link lists **in file declaration order**, so reordering nodes reorders what the player sees. | ENGINE | engine test | — | — |

## §2.5 — Runtime attachment (lines 603–607) · §2.6 — Writing to the engine (lines 609–629)

**UNCHANGED:** C243–C250, C251–C272. No delta claims.

## §2.7 — Probes (lines 631–668)

**UNCHANGED:** C274–C293, V098, V099, V100, V101.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W108 | REVISED | Items **12–15 are done** — run against 1.37.5 in `../v2-drain/game-session.md`, with their results folded into §1.9, §2.4 and §3.6; items 1–11 remain, and items 1–10 are the debugger set. | DESIGN | stipulated | V097 | — |
| W109 | REVISED | Item 12 was **dropped rather than run**: under owner-agnostic wealth nothing reads the per-province production-income field, so what it contains no longer matters. | DESIGN | derivation | V102 | W023, V054 |
| W110 | REVISED | Item 13 is settled **and it reverses the hedge** — the engine does not tolerate a cycle. | WORLD | engine test | V103 | W101 |
| W111 | REVISED | ⚑§ Item 14 is settled and the spec is confirmed: the entry **only navigates** — clicking `Safi` in Sevilla's window switched the window to Safi and dispatched nothing. | ENGINE | engine test | V067, V104 | V066 |
| W112 | REVISED | Item 15 is settled **and it reverses the spec's caution** — the tooltip's qualifier is not a precondition. | WORLD | engine test | V105 | W067, W068 |
| W113 | NEW | The §2.4 item 3 link-reversal check is **done and passed**. | WORLD | engine test | — | W103 |
| W114 | REVISED | ⚑ The declaration-order companion question is settled: the engine validates order, logs one error per violating link, and tolerates violations. | ENGINE | engine test | V096 | W099 |

## §2.8 — Validation (lines 670–710)

**UNCHANGED:** C298–C342, V106, V108 *[unverified in v3.0]*, V109, V110, V111, V112, V219.
*(W053 carries the Latent-good row.)*

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W115 | REVISED | ⚑ **No Chinese node holds a spices sink in either configuration**: under the §3.13 α-calibration `spices` sinks at **Genoa and Doab**, and it is **cloves** that moves to Beijing; the v1 China+Europe expectation is not the baseline and is not recovered by the calibration either. | MODEL | numerical test | V107 | V106, V177 |
| W116 | REVISED | The economy-tab check is a **self-consistency check, not a comparison against stock EU4**. | DESIGN | stipulated | C298–C342 † | W117 |
| W117 | NEW | ⚑§ Stock trade values are not reproducible run to run: two identical vanilla 1444 Castile starts differ on **49 of 80 nodes by up to 8.96%**. | ENGINE | engine test | — | — |
| W118 | NEW | ⚑ AI merchant placement is randomised at start; only node `total` and `retention` are deterministic. | ENGINE | derivation | — | W117 |
| W119 | NEW | Any comparison against unmodded numbers needs a tolerance and a null run. | DESIGN | derivation | — | W117 |
| W193 | NEW | **2-core containment is a hard assertion, unconditional, every tick:** every sink inside the 2-core lies in `{selected} ∪ {promoted}`, because every other core node is handed an out-arc by the sweep. A violation is an implementation bug and halts. | DESIGN | derivation | — | W124 |
| W194 | NEW | **2-core equality is monitored, not asserted:** `{selected ∩ flow-terminal} ∪ {promoted}` is measured exact on 1444 but is not a theorem, and **T2** is the way it can fail while the algorithm is behaving correctly. An equality miss is reported with its node and good; only a containment miss halts. | DESIGN | derivation | — | W013, W128, W193 |
| W195 | NEW | **On pendant edges the equality does not apply and is not asserted:** the check is the Phase-4 orientation rule, and a net-importing pendant leaf that ends a sink is expected output — **T1**, not a fault. | DESIGN | derivation | — | W084, W126 |

## §2.9 — Build order (lines 712–724) · §3.1 — Goals (lines 726–734)

**UNCHANGED:** C343–C352, C353–C365, V113. No delta claims.

## §3.2 — Why a flow and a drainage sweep (lines 736–813)

**UNCHANGED:** C366, C370, C371, C372, C373, C374, C375, C383, C384, C385, V115, V116, V117,
V118, V119, V120, V121, V122, V124, V128, V129, V130 *[unverified in v3.0]*,
V131 *[unverified in v3.0]*.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W120 | REVISED | The first family of orientation fails **by theorem**; the second fails by an **exact rule whose consequence is measured** — v2 called both theorems, which overstates the second. | MODEL | derivation | V114 | C370, V116 |
| W121 | REVISED | Better wealth inputs plausibly deliver about **1.7×**, enough to make Genoa a **co-sink** but not enough to make demand the determinant of placement; a Chinese spice sink needs **3.6–4.8×**. v2's "1.7× where 4–5× is needed" compressed two different thresholds into one comparison. | MODEL | numerical test | V123 | V117 |
| W122 | NEW | 3.6–4.8× is **9.5–21.4% of all world spice demand at one node**. | MODEL | numerical test | — | W121 |
| W123 | REVISED | DRAIN's sinks are the selected demand centres, plus the flow-terminal drains any acyclic drainage orientation would be forced to have anyway, **plus (where Phase 0 acts) pendant net-importers**. | MODEL | derivation | V125 | W012 |
| W124 | REVISED | What survives unconditionally is the **⊆-direction within the 2-core**: every core node that is neither selected nor promoted is given an out-arc by the sweep, a flow arc or a free edge to an earlier-marked node. Pendant net-importers are the only sinks outside the set, and the free-edge race is the only way a node inside it drops out. | MODEL | derivation | V126 | W126, W128 |
| W125 | REVISED | v1 **did** state aggregate acyclicity, as C061 ("`Φ` is a potential, so orienting edges by it is acyclic"), and its ε-machinery stated what decided dead-branch direction; what v1 genuinely never stated is the sink-placement determinant and any reachability guarantee. | WORLD | derivation | V127 | — |
| W126 | NEW | **Counterexample 1, pendant importer.** Triangle A(+5), B(−3), D(0) with a leaf C(−2) on B: Phase 0 peels C, Phase 4 restores the edge B→C, the actual sinks are `{C}` and the formula set is `{B}`. | MODEL | numerical test | — | W013 |
| W127 | NEW | The pendant is a sink outside the set **and** it strips the selected sink of its sinkhood. | MODEL | derivation | — | W126 |
| W128 | NEW | **Counterexample 2, free-edge race inside the 2-core.** Five-cycle S1(+3)–u1(−3)–w(0)–u2(−2)–S2(+2)–S1 with a chord w–S1: under the DEF-ascending key u2 pops first, the conduit w becomes ready via its free edge to u2 and pops before u1, so the free edge orients u1→w and u1 is no longer a sink. Actual `{u2}`, formula `{u1, u2}`. | MODEL | numerical test | — | V020 |
| W129 | NEW | Both constructed inputs were run through a faithful implementation of §1.1. | WORLD | numerical test | — | W126, W128 |
| W130 | NEW | Zero exact key ties were measured, so the index never decides. | MODEL | numerical test | — | V035, V020 |
| W131 | NEW | Sink placement is checked at runtime as **two** checks rather than one weakened one (§2.8, W193–W195), so that neither counterexample disappears into an escape clause. The two constructed inputs are labelled **T1** (pendant importer) and **T2** (free-edge race) so the assertion rows can name them. | DESIGN | stipulated | — | W193, W194, W195 |

## §3.3 — Why wealth, and why per province (lines 815–837)

**UNCHANGED:** C386–C406, C408, C412, C413, V132 *[unverified in v3.0]*, V133,
V135 *[unverified in v3.0]*.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W132 | REVISED | ⚑ The return-flow effect is real but **modest at vanilla prices**: sugar (3.0), cocoa (4.0) and coffee (3.0) are **1.2–1.6× grain (2.5)**, not multiples. v1 and v2's "negligible development but large production income" overstated the gap. | ENGINE | file value | C386–C413 † ("a sugar island has negligible development but large production income") | — |
| W133 | NEW | ⚑ The largest price ratios belong to **cloves (8.0)** and **coal (10.0)**, neither of which is a Caribbean sugar island. | ENGINE | file value | — | W132 |
| W134 | NEW | Under v3.0 the owner-side terms are gone: autonomy drift, national ideas, government reforms, estates and technology no longer move demand at all. | MODEL | derivation | — | W023, W024 |
| W135 | NEW | What still moves, deliberately: development changes, trade-good changes (a latent good activating reprices its province), price events, and `trade_goods_size` modifiers on the **place** — devastation, occupation, siege, prosperity. | MODEL | derivation | — | W023, V038, W053 |
| W136 | NEW | A besieged province genuinely produces less, so that volatility is economics rather than noise; a trade map that ignored a decade-long war would fail Goal 1. | DESIGN | derivation | — | W135 |
| W137 | REVISED | The slicing distortion is measured against **the per-province form the model actually defines, not against equal totals**: node-level α overweights a k-province node by `k^(α−1)` at fixed per-province wealth, so at α = 1.5 a 77-province node is favoured over a 19-province one by `(77/19)^0.5 ≈ 2×`. | MODEL | derivation | V134 | V132, V133 |
| W138 | NEW | At equal totals the node-level form is **count-blind and the two tie** — which is what v2's version of the comparison actually says. | MODEL | derivation | — | W137 |
| W139 | REVISED | Node-level α would favour Nippon (68 land provinces) over the Paris node (`champagne`, 33) by `(68/33)^0.5 ≈ 1.44×`. | OUTCOME | derivation | V136 | W137, V135 |

## §3.4 — Why supply is pre-modifier (lines 839–849)

**UNCHANGED:** C415, C416, C417, C418, C419, C420, C421, C422, C423, V137, V138, V139.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W140 | REVISED | Production efficiency is a fact about the owner's extraction, and under v3.0 it **does not belong in demand either** — the clause "and belongs in demand" is deleted. | MODEL | derivation | C415–C423 † ("That is a fact about purchasing power and belongs in demand") | W023 |
| W141 | NEW | v1 and v2 excluded owner effects from supply and then let them straight back in through `wealth`, so the same incoherence they rejected on the supply side ran the demand side. | WORLD | derivation | — | W140 |
| W142 | NEW | Supply and demand are both properties of the place, so the pre-modifier argument written to defend supply applies unchanged, and with more force, to demand. | MODEL | derivation | — | W140, W023 |

## §3.5 — Why α is anchored absolutely (lines 851–869)

**UNCHANGED:** C427–C442, V140, V141, V142, V143, V144, V146, V147.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W143 | REVISED | ⚑ **12 of 30 goods** can be pushed strictly below 2.0 by a single vanilla `change_price` event (grain and wine reach 0.625). | ENGINE | file value | V145 | V140 |
| W144 | NEW | ⚑ Three more — `gems`, `silk`, `wool` — land **exactly on** 2.0, reaching α = 1 but not the sublinear regime. | ENGINE | file value | — | W143 |
| W145 | NEW | The boundary is `< 2.0`, and three goods sit on it exactly — the likely origin of v2's off-by-one. | WORLD | derivation | — | W144 |
| W146 | NEW | ⚑ All **101** `change_price` blocks across `events/`, `decisions/`, `missions/` and `common/` were parsed; `history/` contributes only positive entries. | ENGINE | file value | — | W143 |

## §3.6 — Why no hysteresis, and why there is no ε (lines 871–906)

**UNCHANGED:** C443, C444, C445, C446, C449, C452, V148, V152, V154.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W147 | REVISED | Acyclicity is enforced because the engine **provably cannot survive its absence** — not, as v2 had it, because we could not prove that it could. | DESIGN | derivation | V149, V150 | W101 |
| W148 | NEW | The engine walks the node graph **recursively**, and a cycle never terminates. | ENGINE | derivation | — | W101 |
| W149 | REVISED | "A flipping link carries near-nothing either way" is **measured, not derived**: v1's continuity argument (a near-flat potential implies near-zero flow) does not port to an LP support, which is a discrete selection. | MODEL | derivation | V151 | V015 |
| W150 | NEW | Measured on 1444: across 29 goods × 6 random 1e-9 demand nudges, **zero** support-membership changes moved more than 1e-6 of flow, and the ±1% wealth-noise flips all sat on near-zero-flow edges. | MODEL | numerical test | — | W149 |
| W151 | NEW | At exactly degenerate inputs — two equal-hop corridors — the map from `b` to the chosen support is discontinuous in principle, so this rests on the **solver's tie-selection being stable**, the same premise §3.13 tracks for multiplayer. | MODEL | derivation | — | W150, V183 |
| W152 | REVISED | The priority key's **values** come from the inputs, but **which nodes are downstream comes from the solve** — it is computed from input data *over the LP's support structure*. | MODEL | derivation | V153 | V020 |

## §3.7 — Why eligibility is per good (lines 908–914)

**UNCHANGED:** C463–C473. No delta claims.

## §3.8 — Why gates evaluate true (lines 916–934)

**UNCHANGED:** C474–C497, V155, V156, V157, V158.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W153 | REVISED | Measured under DRAIN, **90.9%** (5743 of 6320) of ordered node pairs are connected by at least one good on 1444 data. | MODEL | numerical test | V159 | V006 |
| W154 | NEW | ⚑ v2's 98.8% is **v1's Laplacian figure** (6245/6320), carried across the operator change without being re-measured; the argument is unaffected but the number was not v2's own. | WORLD | derivation | — | W153 |

## §3.9 — Why `Φ_w` is the installed graph (lines 936–971)

**UNCHANGED:** C502, C505, C506, C507, C508, C509, C510, C512, V160, V161, V162, V218, V220,
V221, V228. *(W062 carries the 60.2% figure at its first appearance in §1.6.)*

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W155 | REVISED | `Φ_ord`'s end count **never concentrates**: 13–22 ends measured across cloves-α 2…64, never approaching vanilla's three. v2's "α-invariant … 9–17 ends" is neither the right word for a quantity that ranges 13–22 nor a band containing its own baseline of 18. | MODEL | numerical test | V222 | V059, V221 |
| W156 | NEW | A rich **non-sink** node — Beijing, Champagne, Sevilla — bends every edge around it as a net demander even though flow passes through. | MODEL | derivation | — | V212 |

## §3.10 — Why the engine's economy is overwritten (lines 973–988)

**UNCHANGED:** C513–C530, with `5.7e-14`, `1.4e-14` and the 5.96-ducat propagation error all now
marked *[unverified in v3.0]*. No delta claims.

## §3.11 — Caravan power (lines 990–1011) · §3.12 — Treasure fleets (lines 1013–1026)

**UNCHANGED:** C531–C547, C556–C560, V163, V164, V165, V166, V167, V168 *[unverified in v3.0]*,
V169, V170, V171, V172. No delta claims. *(W070 carries §1.10's caravan correction.)*

## §3.13 — Open questions (lines 1028–1084)

**UNCHANGED:** C561–C585, V173, V174, V175, V177 *[unverified in v3.0]*, V178, V181, V182, V183.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W157 | NEW | The three §1.3 wealth questions below are **questions, not numbers**: §1.3 carries no value for any of them. | DESIGN | stipulated | — | W023 |
| W158 | NEW | **Open:** do local flat goods bonuses exist at 1444, and do any apply before the price multiply? The goods-produced tooltip itemises additively, so a flat `trade_goods_size` would appear as its own line and enter before the price multiply — but **no 1444 province was observed carrying one**. | ENGINE | derivation | — | W039 |
| W159 | NEW | Its settling observation: find a province with a non-zero `trade_goods_size` from a building or static modifier and read its goods-produced tooltip. | DESIGN | stipulated | — | W158 |
| W160 | NEW | **Open:** is a trade good's `local_production_efficiency` (glass, +10%) inside or outside local wealth? It is province-scoped, so §1.3's structural rule includes it, but it is literally a production efficiency, which §1.3 excludes — **the rule and the vocabulary disagree**, and only three goods are affected. | ENGINE | derivation | — | W040, W043, W024 |
| W161 | NEW | Its settling observation: read a glass province's production tooltip and confirm whether the +10% appears under `Production Efficiency` alongside the technology term. | DESIGN | stipulated | — | W160 |
| W162 | NEW | **Open:** does `TAX_COEFF` stay 1.0 across the development range? It was measured at **one province** (`base_tax` 6 → yearly 6.00); a linear coefficient is the obvious reading and the goods coefficient is linear at the same province, but one point does not establish linearity. | ENGINE | derivation | — | W094 |
| W163 | NEW | Its settling observation: read the tax tooltip on two provinces with different `base_tax`. | DESIGN | stipulated | — | W162 |
| W164 | NEW | The zero-flow tolerance is **scale-coupled**, and the fix — normalise `b` to a fixed scale before the solve, or make the tolerance relative — is **undecided**. | DESIGN | derivation | — | W055, W098 |
| W165 | REVISED | The sublinear regime is reachable through vanilla price events for **12 of 30** goods, unreachable for 11, and exactly on the boundary for 3. | DESIGN | derivation | V176 | W143, W144, V146 |
| W166 | REVISED | Under the calibration's α = 16, Beijing is **demand rank 2** — with the rank-1 demander `hangzhou` acting as a transit node — and becomes the cloves sink. | MODEL | numerical test | V179 | V178 |
| W167 | NEW | ⚑ `hangzhou` holds the richest single province, at **27.0** against Beijing's **19.5**; v2 said Beijing held it, which it does not. | MODEL | numerical test | — | W166 |
| W168 | REVISED | The twig tolerance re-routes arcs individually carrying <0.03% of world supply but **up to about 0.15% of a good's mass in total**, and drops **silk** to 99.97% reach and cloves to 99.997%. | MODEL | numerical test | V180 | V178 |

## §3.14 — AI merchant assignment (lines 1086–1103)

**UNCHANGED:** C586–C624.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W169 | REVISED | The survival table is about **1.5 MB at double precision**; 0.75 MB is the single-precision figure. | MODEL | derivation | C586–C624 † ("about 0.75 MB") | W170 |
| W170 | NEW | The rest of the solver is double precision, as its own 5.7e-14 and 1.4e-14 tolerances show. | MODEL | derivation | — | — |

## §3.15 — Rejected (lines 1105–1206)

**UNCHANGED:** C625–C672 as carried by v2, V184, V185, V186, V187, V188, V189
*[unverified in v3.0]*, V191 *[unverified in v3.0]*, V192, V193, V194, V195, V196, V197, V198,
V199, V226, V227, V228. *(The `Φ_ord` graveyard entry's 60.2% ceiling is W062 at first
appearance.)*

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W190 | REVISED | The 3-mass gravity kernel hits any chosen end count exactly with **66%** vanilla-arrow agreement in the reproduced construction; the count-follows-seeds behaviour reproduced, the 69% v2.0 and v2.1 both quoted did not. | MODEL | numerical test | V225 | V226 |
| W171 | REVISED | Ranked orientation wins the sink–demand **alignment** statistics — ρ_val +0.281 against DRAIN's +0.053, and 46.6% of top-decile nodes are sinks against 14.1% — and **loses the rest**; v2's "wins every sink statistic" is wrong. | MODEL | numerical test | V190 | V189 |
| W172 | NEW | It also posts **9 net-producer sinks** where DRAIN, LAP and FLOW all post zero, and **11–17 sinks per good** against DRAIN's 1–8. | MODEL | numerical test | — | W171 |

## §3.16 — Evidence standard (lines 1208–1269)

**UNCHANGED:** C677, C680, C681, C682, C684, C685, V200, V201, V202, V203, V204, V206, V207,
V208, V209, V210. *(V042–V047's floors survive here — see the orphan table.)*

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| W173 | REVISED | **Nine of the sixteen** refuted ENGINE claims were UNSOURCED. | WORLD | derivation | V205 | V200 |
| W174 | NEW | No partition of the refuted set yields fourteen: there are sixteen ENGINE-typed refutations, or thirteen excluding the three that carried `derivation` provenance. | WORLD | derivation | — | W173 |
| W175 | REVISED | The cautionary case is closed **and it closed the other way**: probe 15 showed the qualifier is descriptively false, and §1.9 was right not to carry it. | WORLD | derivation | V211 | W067, W112 |
| W176 | NEW | The lesson is not the one the case was filed under: the unreliable source was a **binary string** — the class §3.16 nominates as sufficient. | WORLD | derivation | — | W175, V206 |
| W177 | NEW | A localisation string describes **intent, not behaviour**. | WORLD | derivation | — | W176 |
| W178 | NEW | **Sources are necessary, not sufficient**: an engine fact sourced to a *string* is settled only when something observes the behaviour the string describes. | DESIGN | stipulated | — | W177 |
| W179 | NEW | ⚑§ During the declaration-order test a permuted node file differed from vanilla on **61 of 80 nodes** — a real measurement from a real game with impeccable provenance, and meaningless. | ENGINE | engine test | — | W117 |
| W180 | NEW | **A measurement without a null comparison is not evidence.** | DESIGN | stipulated | — | W179, W117 |
| W181 | NEW | Every measured claim in the document that could vary run to run should carry the control that bounds its noise floor. | DESIGN | stipulated | — | W180 |

---

## † Unresolved claims.md IDs

**Nine** v3 revisions replace sentences that entered in v1 and passed through v2 as UNCHANGED, so
their IDs are in `../v1-laplacian/claims.md`, which the extraction brief excluded. Each row names
the C-range from claims-v2.md's UNCHANGED list for that section and quotes the replaced sentence
from `changes-v3.md`. *(A tenth — W065, the merchant "+10% trade efficiency" sentence — was
resolved to **C070** by the spec's author and is filed normally in §1.7.)*

| W ID | Section | Replaced sentence | C-range |
|---|---|---|---|
| W001 | header | "Target: EU4 (final patch, 1.37.5 Inca), extended timeline compatible, **map-agnostic**" | C001–C004 |
| W030 | §1.3 | "`wealth(p) = tax_income(p) + production_income(p)`" | C031–C039 |
| W050 | §1.3 | "Unowned provinces generate no income and contribute nothing." | C031–C039 |
| W070 | §1.10 | "It is a step function on raw power: it either applies or it does not" | C112–C143 |
| W099, W106 | §2.4 | "The engine performs no topological sort — the file must be one." | C228–C242 (V096 cites C234) |
| W116 | §2.8 | the economy-tab row's stock-EU4 comparison | C298–C342 |
| W132 | §3.3 | "a sugar island has negligible development but large production income" | C386–C413 |
| W140 | §3.4 | "That is a fact about purchasing power and belongs in demand." | C415–C423 |
| W169 | §3.14 | "about 0.75 MB, well under a million operations per solve" | C586–C624 |

Resolving these needs `claims.md`; the propositions themselves are recorded above and none is
ambiguous.
