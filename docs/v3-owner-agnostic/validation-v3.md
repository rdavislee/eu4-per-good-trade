# Validation of `claims-v3.md` against EU4 1.37.5, the running game, and the reference solver

**Scope.** The 195 v3.0 delta claims **W001–W195**. UNCHANGED C/V IDs keep their status from
`../v1-laplacian/validation.md` and `../v2-drain/validation-v2.md` and are not re-validated, except
where a v3 claim depends on them or where the priority item requires it.

**Install audited.** `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV`,
`"version": "EU4 v1.37.5.0 Inca (491d)"` read from `launcher-settings.json` this session; crash
metadata gives SCM commit `835bfdf8ca24c291a1b3f1b5bc72d47e7df1ae18`. Vanilla checksum **491d**
observed on the main menu; with a probe mod loaded, **3047**.

**Documents validated.** `per-good-trade-spec.md` v3.0 (104,457 bytes), `claims-v3.md` (71,307
bytes), `changes-v3.md` (22,475 bytes). None was edited by this pass.

**Nothing inherited.** All game data was re-extracted from the install this session (`nodes.py`,
`provinces.py`, `coastal.py`, `strings.py` re-run; 80 nodes / 159 links / 2452 owned city
provinces / 137,820 exe strings). Every numerical claim was re-run (`v3measure.py`, `final.py`,
`verify.py` 33/33, `drainrep.py`, `rankrep.py`, `phiw3.py`, `leftovers.py`, `graphchk.py`,
`toys.py`, plus new scripts `w1.py`–`w8.py`, `w_noise.py`, `modchk.py`). Every ENGINE claim traced
to `../v2-drain/game-session.md` was re-derived either from the on-disk artifact (crash dumps,
`.eu4` saves, probe mod files) or by **running the game again this session** — four EU4 sessions:
vanilla Castile 1444, `pgt_permute` Castile 1444, `pgt_cycle` (crash), plus a vanilla control.

---

# Summary

## Counts by status

| Status | Count |
|---|---|
| CONFIRMED | 166 |
| REFUTED | **10** |
| PARTIAL | **19** |
| **Total** | **195** |

**REFUTED (10):** W003, W035, W041, W049, W066, W124, W144, W145, W146, W193.
**PARTIAL (19):** W006, W027, W037, W039, W040, W045, W086, W101, W118, W121, W122, W131, W143,
W156, W158, W160, W162, W165, W190.
Everything else is CONFIRMED.

Nothing is filed OUT_OF_SCOPE or DEFERRED. v1 and v2 set DESIGN aside and deferred OUTCOME; this
pass grades every row, because a DESIGN or OUTCOME claim still has a checkable core — *does it
accurately state what the spec requires, and is its stated reason true?* Three of the ten
refutations (W003, W049, W193) and four of the nineteen partials (W006, W131, W157-adjacent, W162)
are DESIGN or WORLD rows that would have been set aside under the earlier convention. **W193 in
particular is a DESIGN row, and it is the most consequential single finding in this pass** — it
would have gone ungraded.

`claims-v3.md`'s own tallies were re-derived from its tables and **all reproduce exactly**: 195 IDs
W001–W195 with no gaps, 130 NEW / 65 REVISED, MODEL 80 / ENGINE 49 / DESIGN 37 / WORLD 24 /
OUTCOME 5, and provenance derivation 97 / stipulated 28 / numerical test 26 / engine test 25 /
file value 17 / UNSOURCED 2.

**v1 had 23 refutations, v2 had 11, v3 has 10.** The rate did not fall because v3.0 is careful; it
fell because v3.0 is *shorter on new engine assertions than it looks*. Of the 45 ⚑ engine facts,
26 are new territory, and **five of the ten refutations are in that block** — the wealth
measurement, the local-modifier rule, and the price-event scan. The other five are a new runtime
assertion that repeats the trap it was written to avoid, an unfixed fold-through claim, and two
inherited-but-never-checked clauses.

## Refuted claims, with blast radius

| ID | Claim | What is actually true | Blast radius |
|---|---|---|---|
| **W003** | v3.0's second change: **every** refutation and partial in `validation-v2.md` is folded through. | **Five of v2's 24 partials were never folded** and survive verbatim in v3.0: **V071** (§1.8's universal negative "no mechanic gates flow by range"), **V075** and **V076** (§1.10's "Propagate Religion … no band" and "nothing absorbs threshold chatter" — the shipped flag ladder *is* banded on all nine rungs, re-read from `00_trading_policies.txt` this session), **V090** (§2.2's "tens of milliseconds for all 29 goods", still unqualified; the reference takes 190–210 ms), **V223** (§1.6's "scaling European node wealth ×2/×3" with the node set still unnamed). A sixth, **V001**, *was* folded silently (the header's "final patch" is gone). | Header §0; §1.6, §1.8, §1.10, §2.2. `changes-v3.md` §Summary ("Partials narrowed … 24"); `claims-v3.md`'s "Five partials cannot be checked" row, which is the right number of *unfixed* partials by accident and the wrong number of *unaccounted* ones. V071/V075/V076/V090/V223 ride into v3.0 as UNCHANGED with their v2 PARTIAL statuses still live. |
| **W035** | ⚑§ The production tooltip reads `Trade Value: +0.26 … yearly income of 3.25` for a province whose window shows an annual `Trade Value` of **3.20**. | Re-run this session on a fresh vanilla Castile 1444 start, Garnatah (223): the tooltip reads **`Trade Value: +0.29 … yearly income of 3.57`** and the window shows **Trade Value 3.52, Goods Produced 0.88**. The difference is a **`Goods Produced Efficiency: +10.00% — Industrious: +10.0%`** line that the quoted tooltip omits. `Industrious` is a **ruler personality** (`common/ruler_personalities/00_core.txt`: `global_trade_goods_size_modifier = 0.1`) and Granada's 1444 monarch carries **no scripted personality** (`history/countries/GRA - Granada.txt`), so it is rolled at game start — the figure is run-dependent. "3.20 = 0.80 × 4.00" is the *model's* arithmetic reported as the *window's* value. | §1.3's time-basis paragraph; `changes-v3.md`'s "Which give, all cross-checking" block; W037's single-observation basis; §3.16's own rule that a measurement without a null is not evidence — violated by the block v3.0 added to state it. `GP_COEFF` and `TAX_COEFF` themselves survive (see W092/W094). |
| **W041** | ⚑ In vanilla the income-relevant **local** modifiers are **exactly three** (gems, glass, incense). | At least a fourth, and a whole further class. **`chinaware` carries `province = { local_autonomy = -0.1 }`** — a province-scoped trade-good modifier that changes the province's tax *and* production income in the engine, and that §1.3's structural rule ("only the `province = {}` block is local") admits while §1.3's vocabulary ("no autonomy") excludes — the same collision §3.13 flags for glass and does not flag here. Separately, the engine applies **`bonus_from_merchant_republics`** (`eu4.exe:0x1cc7128`) as a *Goods Produced Efficiency*: observed **+3.7%** on Girona and **+3%** on Barcelona this session. That is a place-scoped, income-relevant modifier that is not a trade-good modifier at all, so §1.3's rule cannot see it. | §1.3's local-modifier paragraph and §2.2 item 4's "with local goods modifiers only"; W040's rule as a *complete* classifier; W160's open question (which is now the *second* instance of a collision, not the only one). |
| **W049** | So `City` (+25%) **cancels in the normalised share** and is not carried. | It does not cancel. `city` is `local_tax_modifier = 0.25` (`00_static_modifiers.txt`), so it multiplies **only the tax term**; `wealth = tax + trade_value` is not scaled by a constant. Measured over the 2452 counted provinces the per-province ratio `(1.25·tax + trade)/(tax + trade)` runs **1.0625 to 1.2500**. Carrying City moves the per-good graphs: **6 edge flips across 29 goods and one good's sink set changes** (`w7.py`). `Φ_w` is unaffected on 1444 — the derivation fails while its 1444 measurement passes. | §1.3's exclusion paragraph; W048's premise is true and its consequence is not; the argument, not the number, is what other maps would inherit. |
| **W066** | ⚑ Trade efficiency … **also feeds the caravan-power and collection tooltips**. *(UNSOURCED)* | The first half (trade efficiency ≠ a flat income bonus) is file-evidenced: separate modifier keys, separate ledger columns, and `HORDES_UNLOCK_NOMADIC_CARAVANS_PRIVILEGE` grants Caravan Power **and** Trade Efficiency as two distinct modifiers. The second half is false for caravan power: the engine's own tooltip **`CARAVAN_POWER_DESC2`** reads *"Inland caravans provide a total of $VALUE$ trade power, base of it coming from **a third of your development**($BASE$) and $MODIFIER$ from **policies and ideas**"* — development and policies/ideas only. No string in 137,820 exe strings or in the English localisation ties `trade_efficiency` to caravan power or to a collection tooltip. | §1.7's parenthetical (line 301). The C070 correction it decorates is sound and unaffected; only the supporting clause is wrong. It is one of v3.0's two UNSOURCED claims, and it fails — the class §3.16 nominates as the risk. |
| **W124** | What survives unconditionally is the ⊆-direction within the 2-core … **pendant net-importers are the only sinks outside the set**, and the free-edge race is the only way a node inside it drops out. | There is a third case, **inside** the 2-core: the sweep's **fallback** branch. When the core contains no net demander, Phase 1 selects nothing, no node is ever ready, and the reference implementation promotes a node by a documented fallback rule that the spec never states. That node ends the sole sink and is in neither `{selected}` nor `{promoted}`. Demonstrated on the **real vanilla 80-node graph** with `b ≡ 0` (uniform node wealth, which is exactly §1.6's `Φ_w` construction on a flat map): sink `african_great_lakes`, `fallbacks = ['african_great_lakes']`, containment violated (`w2.py`). | §3.2 claim 1's closing paragraph; §1.1's sink-placement bullet; §2.2a's premise-2 table; and W193 below, which converts the gap into a halt. |
| **W144** | ⚑ Three more — `gems`, `silk`, **`wool`** — land **exactly on** 2.0. | `wool` does not. `history/countries/HAB - Austria.txt` at **1540.1.1** applies `change_price = { trade_goods = wool key = NEW_DRAPERIES value = -0.25 duration = -1 }`, against the **−0.20** the same key carries in `events/PriceChanges.txt`. 2.5 × (1 − 0.25) = **1.875**, strictly sublinear. `change_price` entries are keyed, so the larger history value is what a campaign reaching 1540 ends up holding. `gems` (4.0, −0.50) and `silk` (4.0, −0.50) do land exactly on 2.0. | §3.5 line 861; §3.13's "exactly on the boundary for 3"; W145, W165. |
| **W145** | The boundary is `< 2.0`, and three goods sit on it exactly — **the likely origin of v2's off-by-one**. | There is no off-by-one to explain. Counting every `change_price` block shipped with the game, **13** goods can be pushed strictly below 2.0 by a single event — which is what v2 said. v3.0 reached 12 by parsing four trees and asserting the fifth contributes nothing negative (W146). The stated diagnosis attributes v2's number to a boundary confusion that did not occur. | §3.5's parenthetical "(v2 said 13; the boundary is `< 2.0`, and three goods sit on it exactly)"; §3.16's own list of failure modes gains a new one — *a corrected number whose correction came from an incomplete scan*. |
| **W146** | ⚑ All **101** `change_price` blocks across `events/`, `decisions/`, `missions/` and `common/` were parsed; **`history/` contributes only positive entries**. | The 101 is exact and reproduces. The second clause is false: `history/` carries **53** further `change_price` blocks, all in `history/countries/HAB - Austria.txt`, and **13 of them are negative** — wool −0.25 and −0.10, gems −0.50, paper −0.50, chinaware −0.50, coffee −0.40, spices −0.40, slaves −0.40, copper −0.35, incense −0.25, grain −0.20, fish −0.10 ×2. Total across the whole install: **154** blocks. | §3.5 line 864; §3.13's 12/11/3 partition; W143, W144, W145, W165. |
| **W193** | **2-core containment is a hard assertion, unconditional, every tick** … A violation is an implementation bug and **halts**. | Containment holds for the set the sweep actually maintains — `{selected} ∪ {promoted} ∪ {fallbacks}` — but the assertion is written over `{selected} ∪ {promoted}`, and the fallback case (W124) sits **inside** the 2-core. On a uniform-wealth map the assertion fires on correct behaviour and halts the solver. This is the *same* trap `claims-v3.md` says it avoided when it downgraded 2-core *equality* to a monitor because T2 sits inside the core: the fix moved the trap down one level rather than removing it. Call this case **T3**. | §2.8's `Sink set, 2-core` row; §2.9's build order ("2-core sink containment" in the per-tick assertion list); W131's "two checks rather than one weakened one" — it needs three, or a containment set that names the fallback. |

## Derivations that failed as proofs while their paired measurements passed

The discipline §1.1 introduced works; it just was not applied to everything.

- **W049 refuted / `Φ_w` measurement passes.** `City` provably does not factor out of a sum of two
  terms when it multiplies one of them; on 1444 `Φ_w` is nevertheless unmoved (0/159 flips) and only
  the per-good graphs shift (6 flips, 1 sink-set change).
- **W124 / W193 refuted / W013 confirmed.** The sink-set equality is measured exact 29/29 on 1444
  (reproduced), and the containment *theorem* the spec upgraded to an unconditional halt is false on
  a constructible input that vanilla never presents.
- **W086 partial.** "Free-edge determinism: **proved**" (§2.2a's table) conflates two things.
  Determinism (same input, same output) is proved — the index tiebreak is deterministic. What §1.1
  actually asserts is stronger, that free-edge direction is "a function of the graph and the
  balances **alone**", and that holds only when the priority key has no exact ties. Zero ties is
  **measured** on 1444 (reproduced: 0 across 29 goods) and is not a theorem; with a tie, direction is
  a function of the node indexing, i.e. of file order. §3.2 item 2 hedges correctly; §1.1 and §2.2a
  do not.
- **W027 partial / W028 confirmed.** `trade_value = goods_produced × price` reproduces on four
  provinces this session (0.88×4.00=3.52, 0.40×2.50=1.00, 0.62×2.50=1.55, 1.03×3.00≈3.11). The
  *input* to it, `goods_produced = GP_COEFF · base_production + flat bonuses`, is incomplete: the
  engine applies a multiplicative **Goods Produced Efficiency** after the base, which §1.3 does not
  model and §3.13 does not list as open.
- **W156 partial.** The mechanism (a rich net demander bends edges without being a sink) reproduces
  for Champagne and Sevilla; the third example is wrong (below).

## Every unfixed v2 partial or refutation

**The priority item, settled.** `changes-v3.md` reports 24 partials narrowed and tabulates 18 rows
covering 19 IDs. The arithmetic gap is **six, not five**, for two independent reasons:

1. `validation-v2.md` grades exactly **24** claims PARTIAL: V001, V016, V031, V060, V071, V075,
   V076, V086, V090, V114, V123, V151, V153, V179, V180, V190, V205, V214, V215, V216, V219, V222,
   V223, V225.
2. The §3 table's 19 IDs include **V036**, which `validation-v2.md` grades **CONFIRMED**, not
   PARTIAL. So the table accounts for **18** partials, not 19.

24 − 18 = **6 unaccounted**: **V001, V071, V075, V076, V090, V223**.

| v2 ID | v2 status | Folded into v3.0? | Evidence, re-derived this session |
|---|---|---|---|
| **V001** | PARTIAL | **Yes, silently.** | The header's "final patch" wording is gone (`Target: EU4 1.37.5 Inca.`). Not claimed anywhere as a fold-through; `claims-v3.md` files it under "Orphaned claims-v2.md IDs". Counting it as unaccounted is right; counting it as unfixed is not. |
| **V071** | PARTIAL | **No.** | §1.8 still reads *"trade range (which gates **merchant placement**, not value flow — no mechanic gates flow by range)"*. The positive half is file-evidenced and if anything broader than stated — range also gates mercenary hiring (`MERCENARY_COMPANY_TOO_FAR`, `MERC_RANGE_EXPLAINED`) and a capital-in-range diplomatic requirement (`REQUIRES_CAPITAL_IN_TRADE_RANGE_TT`). The universal negative remains unprovable from files and is asserted flat. `claims-v3.md` lists V071 as UNCHANGED under §1.8 and separately as still-UNSOURCED, so the spec knows it is unsourced and states it anyway. |
| **V075** | PARTIAL | **No.** | §1.10's table row is verbatim v2's: *"Propagate Religion \| 50% to establish **and 50% to maintain** in the default branch (a country-flag ladder runs 5–50; the terminal fallback is 35/35) — no band"*. Re-read from `common/trading_policies/00_trading_policies.txt` this session: every ladder rung is banded — select 10 → maintain 5, 15 → 5, 20 → 10, 25 → 15, 30 → 20, 35 → 25, 40 → 30, 45 → 35, and the 5-flag has **no** maintain share at all. Default 50/50 and terminal 35/35 are unbanded ✓. |
| **V076** | PARTIAL | **No.** | §1.10 still reads *"Improve Inland Routes is the one banded mechanic; Propagate Religion has no band … So nothing absorbs threshold chatter on its own — a power share oscillating across any of these limits flickers the mechanic, Propagate Religion included."* False for any country holding an `N_trade_power_for_propogate_religion` flag: those get 5–10 points of hysteresis. |
| **V090** | PARTIAL | **No.** | §2.2 still reads *"milliseconds each with network simplex, tens of milliseconds for all 29 goods per monthly tick"*, unqualified and unsourced. Re-timed this session: the reference solve is **0.19–0.21 s for 29 goods, 6.5–7.3 ms/good** (`v3measure.py`, `final.py`). "Milliseconds each" holds; "tens of milliseconds for all 29" is a projection onto native network simplex that no measurement in this project supports, and it is not marked `[unverified in v3.0]`. |
| **V223** | PARTIAL | **No.** | §1.6 still reads *"scaling European node wealth ×2 makes `genua` the sole sink; at ×3 the Cape of Good Hope **reverses**"* with no node set named. v2 established the thresholds land exactly under a 22-node reading and are off by half a step under an 18-node reading. `claims-v3.md` lists V223 under §1.6's UNCHANGED set. |

**Unfixed v2 refutations: none.** All eleven (V004, V029, V062, V107, V125, V126, V127, V134,
V145, V159, V230) are folded, and each fold was re-derived here rather than taken on trust —
60.2% vs the scan-order sweep's 62.7% (`w6.py`, both reproduced exactly), 90.9% = 5743/6320,
12-of-30 within the stated scope, spices→{doab, genua} under the calibration with cloves→beijing,
T1 and T2 through `toys.py`, C061 located in `../v1-laplacian/claims.md` line 210, the node-slicing
form corrected, the coal reprice at 45 provinces flipping 10 of 159 edges. **V145's fold is the one
that went wrong**, and it went wrong by narrowing the scan rather than by inheriting a number.

## Systemic findings (not attached to a single claim)

1. **The reference solver still does not implement §1.3.** v2 filed the missing autonomy floors as
   a defect; v3.0 answers that the solver was right and the spec was wrong. That is true of the
   autonomy term and false of the term §1.3 *added*: `solver.py` computes
   `wealth = base_tax + 0.2·base_production·price` with **no local goods modifiers**, while §1.3
   names three and §2.2 item 4 says "with local goods modifiers only". Applying the two that touch
   quantities v3.0's wealth actually computes — gems `local_tax_modifier = 0.15` (43 provinces) and
   incense `trade_value_modifier = 0.10` (29 provinces) — moves world wealth 10572.40 → 10594.80,
   flips **8 per-good edges** and changes **one good's sink set** (`w8.py`). `Φ_w` is unaffected.
   Every number in §2.8 is still measured on a wealth field the spec does not define.
2. **A measured figure whose named script prints the opposite.** §1.6 and `changes-v3.md` §6 both
   attribute "**0 edge flips and 0 sink-set changes** under ±1% wealth noise across 5 seeds" to
   `v3measure.py`. Run as shipped, `v3measure.py` prints `Phi_w sink-set changes under that noise
   5/5` — it compares a *sorted* list against an *index-ordered* one, so the test can never pass.
   The claim is **true** (re-derived with a set comparison: 0 flips, 0/5 sink changes, `w_noise.py`),
   but the rule `changes-v3.md` closes with — "a measured figure carries the script and the revision
   that produced it" — fails on its own flagship number.
3. **A premise measured under machinery the spec deleted.** §3.2's load-bearing "supply contrast
   exceeds demand contrast by four to five orders of magnitude" and §3.15's "supply contrast (10⁷)"
   are quantified by `changes-v3.md` §6 as "supply contrast 2.52×10⁷ vs demand 471.5". That 2.52×10⁷
   is `max(s) / (ε/N)` with **ε = 1e-6** — v1's regularizer, which §1.2 removes ("**No
   regularizer**"). Under v3.0's own supply definition the spices contrast over producing nodes is
   **36** (`final.py` PART E), and over all nodes it is undefined. The *conclusion* survives on the
   demand side (471.5 reproduces) but the headline ratio is an artifact of deleted machinery.
4. **The gap §3.16 asks about has an answer, and it is Phase 3's stall rule.** The word "fallback"
   appears three times in the spec — §1.1 ("promotions and fallbacks are provably independent of
   scheduling"), §1.6 ("0 fallbacks"), §2.8 ("promotions and fallbacks are scheduler-invariant") —
   and is **never defined**. §1.1's Phase 3 covers only the promotion branch, so the algorithm as
   written has no defined behaviour when a stall occurs with no flow-terminal demander. The
   reference implementation patches it with an undocumented rule; `claims-v3.md` extracts no claim
   about it; and §2.8's new unconditional assertion contradicts it (W193). §3.16's closing question
   — "which property of the output does this spec still not state?" — is answered by its own §1.1.
5. **Single-observation engine facts, re-run, split three ways.** Of the 19 `§` claims,
   **eight reproduced exactly** on an independent run (W034, W038, W046, W068, W095, W100, W107,
   W111), **one reproduced with a third repetition** (W101's crash), **two were extended from one
   province to three and got stronger** (W092/W094 — see below), and **one broke** (W035). The one
   the spec chose to flag as single-point (W094's `TAX_COEFF`, §3.13) is the one that survived.
6. **`changes-v3.md` reports a spec size the spec does not have** — "grew from 74,860 to 99,323
   bytes". v2 is 74,860 ✓; v3.0 is **104,457**. The repairs in `claims-v3.md`'s table landed after
   `changes-v3.md` was written and its diff statistics were never regenerated.

## Two §3.13 open questions are now closed, and one is mis-scoped

Both were closed by reading two more tooltips in the session that was already running.

- **W162 — "Does `TAX_COEFF` stay 1.0 across the development range?" — SETTLED, yes.** Garnatah
  (`base_tax = 6`): `Base: 0.49 (Yearly 6.00)`. Caceres (`base_tax = 2`): `Base: 0.16 (Yearly 2.00)`.
  Two points, both exactly `base_tax` per year. The `0.49` that looks like a rounding error is
  truncation of `6 × 0.083333 = 0.499998`; `2 × 0.083333 = 0.16666` truncates to `0.16` by the same
  rule.
- **W160 — "Is a trade good's `local_production_efficiency` inside or outside local wealth?" —
  SETTLED, outside.** Barcelona (glass) production tooltip, read this session:
  `Production Efficiency: +12.0% / From Technology: +2.0% / **Producing Glass: +10.0%**`. The engine
  books it as a production **efficiency on income**, and it does not touch Goods Produced or Trade
  Value. v3.0's wealth is built from trade value, so glass's +10% is outside it — the vocabulary
  reading is right and the structural reading is wrong.
- **W158 — "Do local flat goods bonuses exist at 1444?" — still open as asked, and asked about the
  wrong thing.** No *flat* `trade_goods_size` was observed. But **two of the four provinces sampled
  carry percentage Goods Produced Efficiency modifiers** — Garnatah +10% (owner: Industrious ruler),
  Girona +3.7% and Barcelona +3% (place: nearby merchant republics / trading cities / trade
  companies) — and §1.3 models neither. The open question that matters is not "are there flat
  bonuses" but "what else multiplies goods produced, and which side of the owner line does it fall
  on".

---

# Part 1 — The five unaccounted partials that were not folded

Ordered first per the brief. Each was re-derived from the install, not from `validation-v2.md`.

### W003 — REFUTED
**Claim.** v3.0's second change: every refutation and partial in `../v2-drain/validation-v2.md` is
folded through. *(WORLD / stipulated)*
**Method.** Enumerated `validation-v2.md`'s 24 `### Vxxx — PARTIAL` headings and its 11-row REFUTED
table; enumerated `changes-v3.md` §3's table; located each unmatched ID's sentence in the v3.0 spec;
re-derived the underlying fact from the install for each.
**Evidence.** 24 partials; 18 accounted for by `changes-v3.md` §3 (its 19th ID, **V036**, is
CONFIRMED in v2 — `validation-v2.md` line 809 — not PARTIAL). Unaccounted: V001, V071, V075, V076,
V090, V223. Of those, V001 was folded (header) and **five were not** — each sentence is quoted
against the current spec in the table above, and each underlying fact was re-checked: the
`propagate_religion` ladder read fresh (nine banded rungs), the trade-range string sweep re-run,
the solver re-timed (0.19–0.21 s / 29 goods), and §1.6's European-set sentence found unchanged.
**What is actually true.** Ten of eleven refutations and **eighteen** of twenty-four partials are
folded through; five partials are not, and the ledger that reports the count is wrong in both
directions — it over-counts the table by one (V036) and under-counts the gap by one (six, not five).
**Spec text to change.** §0: *"(b) Every refutation and partial in `../v2-drain/validation-v2.md` is
folded through, including four v1 corrections that v2 never applied."* → name the five that are not,
or fold them. `claims-v3.md`'s row *"| Partials claimed but not tabulated | 5 | **Still not
identifiable** from the permitted sources |"* → six, and they are identifiable from
`validation-v2.md` alone.
**Blast radius.** §0 header claim; `changes-v3.md`'s Summary table; `claims-v3.md`'s refutation
ledger, which calls this "the one open item". Downstream: §1.6, §1.8, §1.10, §2.2 each carry a
sentence a prior pass asked to be changed. This is the third consecutive round in which what
survived was a correction someone believed had been applied.

### V071 (carried into v3.0 as UNCHANGED) — still PARTIAL
**Claim.** Trade range gates merchant placement, not value flow — no mechanic gates flow by range.
*(ENGINE / UNSOURCED)*
**Method.** Fresh localisation sweep of every trade-range string; `defines.lua` range-key sweep;
137,820-string exe sweep re-extracted this session.
**Evidence.** `HINT_TRADERANGE_TEXT` "Trade Range determines how far away you may send a Merchant";
`TRADE_RANGE_IRO` "Our merchants can reach trade nodes within this range"; `TRADE_NODES_OUT_OF_RANGE`;
`MAPMODE_TRADE_DESC`; plus two the earlier passes did not surface —
`REQUIRES_CAPITAL_IN_TRADE_RANGE_TT` and `MERCENARY_COMPANY_TOO_FAR` / `MERC_RANGE_EXPLAINED`, which
gate a diplomatic action and mercenary hiring by trade range. Defines carry no link-flow range key.
**What is true.** The positive half is file-evidenced and *wider* than §1.8 states — range gates
merchant placement, mercenary hiring, and at least one diplomatic precondition. The universal
negative cannot be established from files and is still asserted flat.
**Spec text to change.** §1.8: *"trade range (which gates **merchant placement**, not value flow —
no mechanic gates flow by range)"* → "…which gates merchant placement (and, in vanilla, mercenary
hiring and one diplomatic precondition); no *string, define or modifier* ties range to link flow,
and no observation has yet tested it."
**Blast radius.** §1.8's vanilla-gates paragraph; the "Malacca ↔ Cape, pre-1500" row of §2.8, which
attributes corridor withholding to range.

### V075, V076 (carried into v3.0 as UNCHANGED) — still PARTIAL
**Claim.** Propagate Religion requires 50/50 in the default branch with **no band**; Improve Inland
Routes is the one banded mechanic; nothing absorbs threshold chatter on its own.
*(ENGINE / file value)*
**Method.** Full re-read of `common/trading_policies/00_trading_policies.txt` this session (five
policies plus four `_upgraded` variants).
**Evidence.** `improve_inland_routes`: `can_select` share 50, `can_maintain` share 40, both gated on
`has_trader = ROOT` and waived by `free_improve_inland_routes` ✓ banded. `propagate_religion`
default branch 50/50 ✓, terminal `else` 35/35 ✓ — and the nine flag rungs between them:
`5 → (no share requirement)`, `10 → 5`, `15 → 5`, `20 → 10`, `25 → 15`, `30 → 20`, `35 → 25`,
`40 → 30`, `45 → 35`. Every rung is banded by 5–10 points.
**What is true.** The claim holds exactly for flagless countries and fails for every holder of an
`N_trade_power_for_propogate_religion` flag. "Propagate Religion included" in the chatter sentence is
the part that is wrong.
**Spec text to change.** §1.10 table row → add "(the country-flag ladder's rungs *are* banded:
maintain trails select by 5–10)"; and §1.10's *"a power share oscillating across any of these limits
flickers the mechanic, **Propagate Religion included**"* → "…Propagate Religion included **for
flagless countries**".
**Blast radius.** §1.10's threshold table and banding paragraph; §2.8's "Propagated-share change per
node" measurement, whose stated failure mode is a share crossing a *single-valued* limit; V077
(DEFERRED) inherits the corrected flicker-risk set.

### V090 (carried into v3.0 as UNCHANGED) — still PARTIAL
**Claim.** Cost per good is one uncapacitated MCF on 80 nodes / 318 arcs plus an O(V+E) sweep —
milliseconds each with network simplex, tens of milliseconds for all 29 goods per monthly tick.
*(MODEL / derivation)*
**Method.** Re-timed the full 29-good reference solve twice this session (scipy/HiGHS LP +
deterministic sweep).
**Evidence.** `v3measure.py`: **0.21 s total, 7.3 ms/good**. `final.py`: **0.19 s total,
6.5 ms/good**. Structure verified: 80 nodes, 159 undirected edges, 318 arcs, support 78–79 edges.
**What is true.** "Milliseconds each" holds already, with a *generic* LP. "Tens of milliseconds for
all 29" is 10× faster than anything measured and rests entirely on an untested
network-simplex-in-native-code premise. It is neither sourced nor marked `[unverified in v3.0]`,
while less load-bearing figures in the same document are.
**Spec text to change.** §2.2: *"milliseconds each with network simplex, tens of milliseconds for
all 29 goods per monthly tick"* → "milliseconds each (measured 6.5–7.3 ms/good on the reference,
scipy/HiGHS); **projected** tens of milliseconds for all 29 with native network simplex
**[unverified in v3.0]**".
**Blast radius.** §2.2's cost line; §2.9's build order, which schedules per-tick assertions on the
assumption the solve is cheap; §2.1's monthly-tick budget.

### V223 (carried into v3.0 as UNCHANGED) — still PARTIAL
**Claim.** Dev-stacking `hangzhou` ×30 makes it the sole world sink; scaling European node wealth ×2
makes `genua` the sole sink; at ×3 the Cape reverses. *(MODEL / numerical test)*
**Method.** Read §1.6 as it now stands; confirmed no node set is named anywhere in the spec.
**Evidence.** §1.6 line 286 is v2's sentence verbatim. `namegrep`-style search of the v3.0 spec for
"European node" returns the one occurrence and no definition.
**What is true.** Every qualitative dynamic reproduces (v2 established this and nothing in v3.0
changed the field); the two stated multipliers are exact only under a 22-node reading of "European
node" and off by half a step under an 18-node reading. The fix v2 asked for is one clause long.
**Spec text to change.** §1.6: *"scaling European node wealth ×2 makes `genua` the sole sink"* →
name the set, e.g. "scaling the 22 European nodes' wealth (the 18 western/central nodes plus
Constantinople, Crimea, Kiev, Kazan) ×2 …".
**Blast radius.** §1.6's dynamics paragraph; §3.9's "a colonizing Europe that flips the Cape", which
inherits the undefined set.

---

# Part 2 — UNSOURCED claims (highest provenance risk)

### W066 — REFUTED
See the refutation table. **Method.** Localisation sweep for every caravan and trade-efficiency
string; re-extracted exe string table (137,820 strings) searched for both; read `CARAVAN_POWER_DESC2`
in full. **Evidence.** `CARAVAN_POWER_DESC2:1 "Inland caravans provide a total of $VALUE|Y$ trade
power, base of it coming from a third of your development($BASE|Y$) and $MODIFIER$ from policies and
ideas."` — the engine's own itemisation, with no efficiency term.
`HORDES_UNLOCK_NOMADIC_CARAVANS_PRIVILEGE` grants "+20.0% Caravan Power **and** +5.00% Trade
Efficiency" as two separate modifiers, which supports the first half of W066 and contradicts the
second. **Spec text to change.** §1.7: *"— efficiency also feeds the caravan-power and collection
tooltips —"* → delete, or replace with the supported distinction: "they are separate modifier keys
with separate ledger columns (`LEDGER_TRADE_EFFICIENCY`, `LEDGER_TC_EFF_CARAVAN_POWER`)".
**Blast radius.** §1.7 line 301 only; the C070 fold-through it decorates stands.

### W071 — CONFIRMED (promoted from UNSOURCED by measurement)
**Claim.** When caravan power applies it is worth up to the cap for any major power — enough to move
a node's power shares by itself, and therefore to push other countries across the §1.10 thresholds.
*(OUTCOME / UNSOURCED)*
**Method.** Its premise V168 (nineteen countries at the cap from raw 1444 development) re-run from
the install; then the missing half — node total trade power at every inland node — parsed out of
`VANILLA_start.eu4`'s `trade={ node={ … total=… } }` blocks and compared against
`CARAVAN_POWER_MAX = 50`.
**Evidence.** V168 reproduces: 19 countries at dev ≥ 150 (MNG ENG TUR CAS LIT VIJ FRA MAM ARA JNP
BAH MOS SHY POL BNG HUN VEN HAB QAR); BUR/KOR/TIM/POR 2.0–9.3% short. Inland-node total trade power
at 1444 runs **106.4 (xian) to 532.0 (champagne)**, median 231.9, and the largest *single existing
holder* in any inland node is **9.6–20.7**. A country at the +50 cap would therefore hold
**8.6%–32.0%** of an inland node's power (median ~21.5%) and would outweigh every incumbent in every
inland node. §1.10's thresholds are 0.1, 0.2, 0.2, 0.51, 0.6, 0.4/0.5.
**What is true.** The claim is right, and it now has a number. It should stop being UNSOURCED.
**Spec text to change.** §1.10: append the measurement, e.g. "— at 1444 the cap is 8.6–32.0% of an
inland node's total trade power (median 21.5%), against a largest incumbent holder of 9.6–20.7."

---

# Part 3 — ENGINE claims sourced to a prior document, re-derived by running the game

`../v2-drain/game-session.md` is a prior document. Every claim tracing to it was re-established from
the on-disk artifact or by a fresh run. Four EU4 sessions were run this session; config was moved
aside and **fully restored** (see Restoration).

### W099 — CONFIRMED
**Claim.** ⚑ The engine performs no topological sort but **validates** that the file is one, logging
`[tradenodedefinition.cpp:61]` once per violating link — and then **tolerates** the violation.
**Method.** Fresh launch with `pgt_permute` enabled via a hand-written `dlc_load.json`; `logs/error.log`
rotated before the run; error lines counted after.
**Evidence.** Checksum **3047** on the main menu (mod verifiably active; vanilla is 491d).
`Select-String 'tradenodedefinition.cpp:61'` → **exactly 159 matches**, first three
`Valencia=>genua`, `Champagne=>genua`, `Champagne=>english_channel`. The game reached the main menu
and played. `modchk.py` re-parsed the mod file independently: 80 blocks, 159 links, **159/159**
order violations, 0 cycles.

### W100 — CONFIRMED
**Claim.** ⚑§ A file with all 159 links declared backwards logged exactly 159 such errors and then
loaded and played normally, with node `total` and `retention` unchanged and the power-dependent
fields differing only within run-to-run variance.
**Method.** Re-ran the permuted build to a Castile 1444 start; separately re-derived the value
comparison from the three `.eu4` artifacts rather than from `game-session.md`'s table (`w5.py`).
**Evidence.** 159 errors, game playable ✓. Save diff, re-parsed: vanilla-vs-permuted differs on
`current` 55/77, `local_value` 31/79, `outgoing` 48/66, `total` 1/79, `retention` 0/80; the null
(vanilla run 1 vs run 2) differs on 49/77, 30/79, 37/66, 1/79, 0/80. Same size, same shape. In the
Sevilla node window under the permuted file every provincial power figure is identical to the
vanilla run to the digit (Castile 129.9/23.7%, Portugal 88.5/21.7%, Morocco 23.4/−46.9%,
Granada 11.6/21.2%) while the value fields move by the run-to-run margin (Incoming 1.41→1.40,
Local 7.23→7.18, Total 8.19→8.13).
**Note.** "`total` … unchanged" is true within the noise but not literally: `total` differs on one
node in the null run too (see W118).

### W101 — PARTIAL
**Claim.** ⚑ A hand-authored two-node cycle produced `EXCEPTION_STACK_OVERFLOW` with **1002 stack
frames at a single return address**, reproduced on two launches, with vanilla and the reversed-order
file both loading fine as controls.
**Method.** Read both prior crash dumps as artifacts, then **reproduced the crash a third time**
this session (`crashes/eu4_20260820_165621/`), with this session's own vanilla run (491d, played)
and permuted run (3047, played) as controls.
**Evidence.** Third dump: `Unhandled Exception C00000FD (EXCEPTION_STACK_OVERFLOW) at address
0x00007FF6DDE6A8B4`, `Mods: mod/pgt_cycle.mod`, **1002** `eu4.exe` frames, identical exception
address to both prior dumps. Its `logs/error.log` carries exactly one `tradenodedefinition.cpp:61`
line (`Valencia=>sevilla`). `modchk.py`: `pgt_cycle` = 80 blocks, 160 links, 1 order violation, **1
two-cycle** (`sevilla`↔`valencia`); `pgt_permute` = 159 violations, **0** cycles, loads. The
attribution is airtight: 159 backwards links do not crash it, one cycle does, three times.
**What is actually true.** Everything except "at a single return address". `exception.txt` records
each frame as `eu4.exe (function-name not available) (+ 0)` with **no address**; the only address in
the file is the exception address in the header. What is observed is 1002 identical anonymous frames
plus one exception address — consistent with unbounded recursion, but the per-frame identity is not
in the artifact.
**Spec text to change.** §2.4 and §3.6: *"`EXCEPTION_STACK_OVERFLOW` with 1002 stack frames at a
single return address"* → "…with 1002 recorded `eu4.exe` frames and the exception raised at a single
address (`0x00007FF6DDE6A8B4`); the dump records no per-frame addresses".
**Blast radius.** §2.4, §3.6, §2.7 item 13, W110, W147, W148 ("the engine walks the node graph
**recursively**" is an inference from the frame count, and remains a reasonable one).

### W103, W104, W105, W113 — CONFIRMED (artifact), not re-run
**Claim.** A reversed link is honoured completely; five named consequences; the mod's core premise
verified end to end; §2.4 item 3 done and passed.
**Method.** `pgt_flip_ordered`'s node file re-parsed from disk this session; the run itself was not
repeated (it needs a fourth full session and its result is not contested).
**Evidence.** `modchk.py`: `pgt_flip_ordered` = 80 blocks, **159** links, **0** order violations,
**0** cycles — exactly the isolation the claim describes (flip without an ordering confound).
`pgt_flip` (the unordered variant) shows 1 order violation, confirming the two builds differ only
in block placement. The economic consequences are corroborated indirectly by this session's Sevilla
window: Aragon (14.2) and France (3.3) hold power in Sevilla **only** via `Transfers from traders
downstream`, so removing Sevilla's downstream would remove them, as W104 reports.
**Status note.** Graded CONFIRMED on the artifact plus corroboration; the five consequences
themselves rest on one launch that this pass did not repeat.

### W107 — CONFIRMED
**Claim.** ⚑§ The node window renders its incoming/outgoing link lists **in file declaration order**.
**Method.** Opened the Sevilla node window in **both** this session's vanilla run and this session's
permuted run, and compared against the declaration order computed from each file.
**Evidence.** Vanilla `00_tradenodes.txt` declares Sevilla's incoming links in block order
`ivory_coast` (56), `tunis` (57), `safi` (59), `carribean_trade` (67); the vanilla window renders
`?????`, **Tunis**, **Safi**, `?????`. The permuted file reverses block order; the permuted window
renders `?????`, **Safi**, **Tunis**, `?????`. Same links, same directions, reversed enumeration.
Valencia's window renders `Tunis`, `Sevilla` — declaration order 57, 74 ✓, with `Genoa` on the
outgoing side.
**Note.** This is now a *two-run* result with a control, which no other §-flagged UI claim has.

### W111 — CONFIRMED
**Claim.** ⚑§ The incoming entry **only navigates** — clicking it switched the window and dispatched
nothing.
**Method.** Clicked the incoming `Sevilla` entry in Valencia's node window (a different node pair
from the original observation, which used `Safi` in Sevilla's window).
**Evidence.** The window title changed `Valencia` → `Sevilla`, the trade policy line changed
`Catalan Charter` → `Iberian Charter`, the figures changed (`+0.86/+3.19/−1.28/2.77` →
`+1.41/+7.23/−0.45/8.19`), the country table changed, and the tab row re-rendered with `Valencia`
now on the outgoing side. No merchant was dispatched; Castile's existing merchant in Sevilla was
untouched ("We earn 4.87 here"). Reproduced on a second node pair. ✓

### W067, W068, W069, W112, W175 — CONFIRMED
**Claim.** ⚑ The tooltip's "where it already has power" qualifier is descriptively false; ⚑§ France
holds zero provinces and zero merchants in Sevilla and still appears with **3.3** power, itemised as
`Transfers from traders downstream: +3.1`.
**Method.** Fresh vanilla Castile 1444 start this session; opened Sevilla's node window and hovered
France's trade power.
**Evidence.** The table reads, digit for digit: Castile 0.0 merchant / 129.9 / 23.7% / 140.2;
Portugal 0.0 / 88.5 / 21.7% / 94.9; Morocco 2.0 / 23.4 / −46.9% / 23.7; Granada 0.0 / 11.6 / 21.2% /
16.7; Aragon 2.0 / 0.0 / 8.7% / 14.2; **France 0.0 / 0.0 / 5.1% / 3.3**. The hover tooltip:
```
Current Trade Power: 3.3
--------------
Transfers from traders downstream: +3.1
And multiplied by 1.05 due to +5.10% Trade Power modifier in this node.
```
No base term, no merchant term, no provincial term. §1.9's "every immediately upstream node" with no
receiving-side condition is correct as written. §3.16's cautionary case closes in the spec's favour,
independently reproduced.

### W117 — CONFIRMED
**Claim.** ⚑§ Two identical vanilla 1444 Castile starts differ on **49 of 80 nodes by up to 8.96%**.
**Method.** Re-parsed `VANILLA_start.eu4` and `VANILLA2_start.eu4` directly (ZIP → `gamestate` →
`trade={ node={…} }`) rather than reading `game-session.md`'s table (`w5.py`).
**Evidence.** Union of nodes differing on any of `current`, `local_value`, `outgoing`, `total`,
`retention`: **49 of 80**. Largest relative difference across all fields: **8.96%** (`siberia`,
`local_value`). Per field: `current` 49/77 (max 7.20%), `local_value` 30/79 (max 8.96%), `outgoing`
37/66 (max 7.19%), `total` 1/79 (max 0.01%), `retention` 0/80. The composite "49 of 80 … up to
8.96%" is exact, not a merge of two rows.

### W118 — PARTIAL
**Claim.** ⚑ AI merchant placement is randomised at start; **only node `total` and `retention` are
deterministic**.
**Method.** Same two saves, field by field.
**Evidence.** `retention` is identical on 80/80 ✓. `total` is **not**: `zambezi` reads **147.384**
in run 1 and **147.366** in run 2 — 1 of 79, 0.012%. The permuted run reads 147.366, i.e. inside the
null. Randomised AI merchant placement is corroborated directly: this session's two starts differ in
merchant strength on the same links (`Safi 0.57 → to Sevilla` vs `Safi 0.56 → to Sevilla`) and in
advisor rosters.
**What is actually true.** `retention` is deterministic; `total` is deterministic on 79 of 80 nodes
and drifts by 0.012% on one. The claim's own source table already recorded `total` 1/79, so this is
a transcription over-reach, not a new measurement.
**Spec text to change.** §2.8: *"only node `total` and `retention` are deterministic"* → "`retention`
is deterministic and `total` is deterministic on 79 of 80 nodes (`zambezi` drifts 0.012%); the
power-dependent fields are not".
**Blast radius.** §2.4's "with node `total` and `retention` unchanged" inherits the same
over-statement; W100's null bound.

### W179, W180, W181 — CONFIRMED
**Claim.** ⚑§ A permuted node file differed from vanilla on **61 of 80 nodes** — a real measurement
with impeccable provenance, and meaningless; a measurement without a null comparison is not
evidence.
**Method.** Re-derived from `VANILLA_start.eu4` vs `PERMUTE_start.eu4` (`w5.py`).
**Evidence.** Union of nodes differing on any field: **61 of 80** ✓, against a null of 49 of 80 at
the same magnitude. On `local_value` the test difference (31/79, max 8.46%) is *smaller* than the
null (30/79, max 8.96%). The lesson is correct and this pass applied it — see W035, where the
missing null is what broke the claim.

### W110, W114, W108, W109 — CONFIRMED
Items 12–15 disposition, the declaration-order companion question, and the reasons. All follow from
W099–W101 and W111 above; item 12's drop is a design decision consistent with §1.3 reading no income
field (W191).

---

# Part 4 — The §1.3 / §2.3 wealth block (⚑, full-strength)

The largest injection of unaudited engine facts in the project. Re-measured in a fresh vanilla
Castile 1444 session on **four** provinces, not one.

### W031, W089, W090, W091 — CONFIRMED
**Claim.** Neither coefficient is a define; both are engine constants recovered by observation;
re-measure against any patch that is not 1.37.5.
**Method.** Searched `common/defines.lua` (2,700+ keys) and all five files in `common/defines/`.
**Evidence.** No goods-produced or tax coefficient exists in either. The only near-misses are
`TRADE_GOODS_ROTATE_SPEED`, `TRADE_GOODS_SPEED` (both UI) and `BASE_TAX_COST_MODIFIER`.

### W092, W093 — CONFIRMED, and strengthened from one province to three
**Claim.** ⚑§ `GP_COEFF` = 0.2 goods produced per point of `base_production`, measured on Garnatah
(223) from `Base Goods Produced: 0.80 / Base Production: +0.80`.
**Method.** Read the goods-produced tooltip on Garnatah (`base_production = 4`) and the Goods
Produced field on Caceres (2), Girona (3) and Barcelona (5) in a fresh run.
**Evidence.** Garnatah tooltip, read this session, verbatim:
```
Base Goods Produced: 0.80
   Base Production: +0.80
Goods Produced Efficiency: +10.00%
   Industrious: +10.0%
```
Girona tooltip: `Base Goods Produced: 0.60 / Base Production: +0.60 / Goods Produced Efficiency:
+3.70% / Nearby Merchant Republics, Trading Cities or Trade Companies: +3.7%`. Caceres field: 0.40
at `base_production = 2`. Barcelona: 1.03 at `base_production = 5` (1.00 base + ~3%).
**What is true.** `Base Goods Produced = 0.2 × base_production` at **2, 3, 4 and 5**. The coefficient
is confirmed and now multi-point — better than the spec claims for it. The quoted first two lines
are exact; the tooltip continues past where the quote stops.

### W094, W095, W096 — CONFIRMED, and W162's open question closed
**Claim.** ⚑§ `TAX_COEFF` = 1.0 ducat/year per point of `base_tax`, measured on Garnatah from
`Base: 0.49 (Yearly 6.00)`, with `local_autonomy = 0` so no owner term was in play.
**Method.** Read the tax tooltip on Garnatah (`base_tax = 6`, autonomy 0.0%) and on Caceres
(`base_tax = 2`).
**Evidence.** Garnatah, verbatim and byte-identical to the spec's quote:
```
Base: 0.49 (Yearly 6.00)
Tax Income Efficiency: 125.0%
   Core: +75.0%
   City: +25.0%
   Reform Iqta: +5.0%
   Clergy: +5.0%
   Granadan Traditions: +15.0%
```
Caceres: `Base: 0.16 (Yearly 2.00) / Tax Income Efficiency: 105.0% / Core +75.0% / City +25.0% /
Clergy +5.0% / Local Autonomy further modifies this by -3.5%`. Two development levels, both
`Yearly = base_tax`.
**Precision note.** The engine's *yearly income projection* is ~0.5% below `12 × monthly-ideal` on
both provinces (Garnatah 7.46 against 6.00 × 1.25 = 7.50; Caceres 2.01 against 2.00 × 1.05 × 0.965 =
2.03). The coefficient comes from the `(Yearly X)` base line, which is exact; the projection line is
not the same quantity and should not be used to derive it.

### W033, W034, W038, W046 — CONFIRMED
**Claim.** Time basis; the tax tooltip's `Base: 0.49 (Yearly 6.00)`; modifiers apply after the
coefficient as a percentage on the base; and the itemised owner terms the model excludes.
**Evidence.** All four reproduce exactly, on both provinces read. The modifier-ordering rule is
visible twice over: tax shows `Base` then a single `Tax Income Efficiency` percentage with its
sources indented under it; goods produced shows `Base Goods Produced` (additive block) then
`Goods Produced Efficiency` (multiplicative block). W046's enumeration of excluded terms is exactly
what Garnatah's tax tooltip lists.
**Note on W046's completeness.** It enumerates only the *tax* tooltip's owner terms. The same
province's *goods* tooltip carries a further owner term the enumeration omits — `Industrious +10.0%`
— and the *production* tooltip carries `From Technology: +2.0%` (listed) alongside, on a glass
province, `Producing Glass: +10.0%` (a local term, not listed anywhere).

### W035 — REFUTED
See the refutation table. **Method.** Fresh vanilla Castile 1444 start; read Garnatah's production
tooltip and province window; then traced the discrepancy to its source in the game files.
**Evidence.** Production tooltip, read at full resolution this session:
```
Trade Value: +0.29
Production Efficiency: +2.0%
   From Technology: +2.0%
---------------
This is the monthly production income of the province. It will generate a yearly income of 3.57.
```
Window: `Trade Power 6.9 / Trade Value 3.52 / Goods Produced 0.88`, node Sevilla, price 4.00. The
spec quotes `+0.26 … 3.25` and `Trade Value` 3.20. The gap is `Goods Produced Efficiency +10.00% —
Industrious`. `common/ruler_personalities/00_core.txt`: `industrious_personality = { …
global_trade_goods_size_modifier = 0.1 … }`. `history/countries/GRA - Granada.txt` contains no
`personality` entry at all, so Granada's 1444 ruler is assigned one at random.
**What is actually true.** The province's *base* figures are stable and the coefficients derived from
them are right. The *window* figures the spec quotes are a function of a randomised owner modifier
and are not reproducible. "Trade value 3.20 = 0.80 × 4.00 (silk price)" is the model recomputing
itself, presented as an engine reading.
**Spec text to change.** §1.3: *"the production tooltip reads `Trade Value: +0.26 … yearly income of
3.25` for a province whose window shows an annual `Trade Value` of 3.20"* → quote only the base
line, which is what the coefficient rests on, and state the ruler-personality confound; or re-measure
on a province whose owner carries no `global_trade_goods_size_modifier`. `changes-v3.md`'s "Which
give, all cross-checking" block needs the same treatment.
**Blast radius.** §1.3's time-basis paragraph and `changes-v3.md`'s derivation block; W036 (the
"no conversion" conclusion survives — both terms are still annual-over-twelve); W037's status as the
single observation carrying the whole argument; §3.16's null-comparison rule.

### W037 — PARTIAL
**Claim.** ⚑§ All of it was measured on Garnatah, province 223 — `base_tax` 6, `base_production` 4,
silk, `local_autonomy` 0.
**Evidence.** The province data is exact (`history/provinces/223 - Granada.txt`: `base_tax = 6`,
`base_production = 4`, `trade_goods = silk`, no `add_local_autonomy`; window shows `Autonomy 0.0%`).
**What is actually true.** The description of the province is right; "all of it was measured on"
*this* province is the problem, not the province. One province cannot separate place terms from
owner terms, and the one it happened to carry (Industrious) is randomised. Three more provinces cost
four clicks and turned a one-point coefficient into a four-point one.

### W027 — PARTIAL
**Claim.** `goods_produced(p) = GP_COEFF · base_production(p)`, plus local flat goods bonuses.
**Evidence.** The base term is exact at four development levels. The engine then applies a
**multiplicative Goods Produced Efficiency** which §1.3's formula has no slot for: +10% on Garnatah
(owner — Industrious ruler), +3.7% on Girona and ~+3% on Barcelona (place — `bonus_from_merchant_
republics`, `eu4.exe:0x1cc7128`).
**What is actually true.** `goods_produced = GP_COEFF · base_production · (1 + Σ goods-produced-
efficiency) + flat bonuses`. Under v3.0's owner-agnostic rule the Industrious term is correctly
excluded; the nearby-merchant-republics term is place-scoped and is *not* excluded by any stated
rule — it is simply absent.
**Spec text to change.** §1.3: `goods_produced(p) = GP_COEFF · base_production(p) # + local flat
goods bonuses` → add the efficiency factor and state which side of the owner line each known source
falls on; §3.13's open-question list should carry it.

### W028, W029, W030 — CONFIRMED
**Evidence.** `trade_value = goods_produced × price` verified on four provinces this session
(0.88×4.00=3.52, 0.40×2.50=1.00, 0.62×2.50=1.55, 1.03×3.00≈3.11). `tax_value = TAX_COEFF ·
base_tax` verified at `base_tax` 2 and 6. `wealth = tax_value + trade_value` is what `solver.py`
computes and what every measurement in this pass reproduces.

### W023, W024, W025, W026, W050, W051, W052 — CONFIRMED
Owner-agnostic wealth is a stipulation and the reference implements it: `solver.py` computes
`tax + 0.2·base_production·price` over provinces with an owner and `is_city = yes` (2452 at 1444),
with no autonomy, efficiency, idea or technology term. W025 and W026 follow immediately. Caceres's
observed `Local Autonomy further modifies this by -3.5%` and Girona's `Autonomy 91.0%` are exactly
the terms the model drops.

### W040 — PARTIAL
**Claim.** ⚑ A trade good's `province = {}` block is province-scoped; its `modifier = {}` block is
country-scoped. **Only the first kind is local.**
**Evidence.** Re-read `common/tradegoods/00_tradegoods.txt` in full: 30 goods, every one with both
blocks, and the split is exactly as described.
**What is actually true.** The rule is a correct classifier *for trade-good modifiers* and is stated
as if it were the classifier for local modifiers generally. It does not see `bonus_from_merchant_
republics` (place-scoped, income-relevant, not a trade good), nor building/great-project province
modifiers, nor the `city` static modifier it goes on to discuss two paragraphs later.
**Spec text to change.** §1.3: *"The engine's own data model draws the line for us"* → scope it to
trade goods, and state separately how non-trade-good province modifiers are classified.

### W041 — REFUTED
See the refutation table.

### W042, W043, W044 — CONFIRMED
`gems province = { local_tax_modifier = 0.15 }`, `glass province = { local_production_efficiency =
0.1 }`, `incense province = { trade_value_modifier = 0.1 }` — all three read fresh. ✓

### W045 — PARTIAL
**Claim.** ⚑ Terrain and climate carry no income-relevant local modifier: `terrain.txt` grants only
development cost, supply limit and defensiveness.
**Evidence.** `map/terrain.txt` modifier keys, fresh: `allowed_num_of_buildings`, `defence`,
`local_defensiveness`, `local_development_cost`, `movement_cost`, `nation_designer_cost_multiplier`,
`supply_limit`. Climate static modifiers (`tropical`, `arid`, `arctic`, the winters, the monsoons):
colonial growth, supply limit, hostile attrition, development cost, allowed buildings.
**What is actually true.** The substance holds — none of these touches income. The enumeration is
incomplete by four keys.

### W046, W047, W048 — CONFIRMED / W049 — REFUTED
W046 and W047 reproduce (the tax tooltip's five owner terms). W048's premise is true: the `city`
static modifier applies to every `is_city = yes` province and the model counts only those. W049's
inference does not follow — see the refutation table.

### W039 — PARTIAL
**Claim.** Flat goods bonuses add into `goods_produced` **before** the price multiply, which is why
they appear in the goods-produced tooltip as their own line.
**Evidence.** The tooltip's structure supports the ordering: an additive `Base Goods Produced` block
(with `Base Production: +X` as its only contributor on all four provinces observed) followed by a
multiplicative `Goods Produced Efficiency` block. So *if* a flat bonus exists it lands in the first
block, before the price multiply.
**What is actually true.** The rule is inferred from the tooltip's layout; **no flat bonus was
observed on any of four provinces**, which §3.13 concedes. The cited evidence line
(`Base Production: +0.80`) is the base-production contribution itself, not a flat bonus, so it
demonstrates the block exists rather than that flat bonuses enter it.

### W032, W097 — CONFIRMED (stipulated / file value)
Prices read from `common/prices/00_prices.txt`: 30 tradeable goods, min tradeable base price exactly
2.0, `gold` and `unknown` at 0.0. ✓

### W098 — CONFIRMED
Design constants as listed; the zero-flow tolerance `1e-11` is absolute in the reference
(`flowop.ZERO_TOL`) and its scale-coupling is demonstrated under W056.

---

# Part 5 — MODEL derivations, checked as arguments

### W007, W008, W009 — CONFIRMED
The spanning-tree-basis property for a **basic** optimum, the interior-point counterexample, and the
weaker no-**directed**-cycle property that holds for any optimum. The cycle-cancelling argument is
sound: with all costs 1 a directed cycle in the support can be cancelled for strictly lower cost.
Measured support 78–79 edges on 29/29 goods, N−1 = 79. ✓

### W010, W011 — CONFIRMED (the discipline itself)
The three-way vocabulary is real and is stated. Its application is audited property by property
below; one property is in the wrong class (W086) and one carries an assertion the class does not
support (W193).

### W012, W013, W014 — CONFIRMED
W013's equality is measured exact 29/29 on 1444, reproduced (`final.py`: "V029 measured … 29/29
goods; mismatches: []"). W012's three-case statement and W014's "not a theorem in general" are both
correct and correctly labelled. This is the property the discipline was built for and it is in the
right class.

### W015, W016, W017, W018 — CONFIRMED
Feasibility on a connected map: `Σ_n b_g(n) = 0` because both `s` and `c` are world shares (immediate);
uncapacitated min-cost flow on a connected graph with balanced supplies is feasible. Disconnected
counterexample re-run: `toys.py` T4 returns HiGHS `model_status is Infeasible`. Vanilla 1444 is
**one component** (`graphchk.py`, `v3measure.py`). Measured reach 100.0%, 29/29, zero orphan sinks.

### W019, W020, W021 — CONFIRMED
The LP objective with unit arc costs is `Σ_arcs f(a)`, which for any path decomposition equals
`Σ_paths (flow × hops)`; minimising it minimises total flow-hops. "In aggregate" is exactly right and
the per-unit denial is correct. **W021's classification is correct**: the property is true by
construction of the LP, so a hop count would re-derive the objective. This is the one property whose
class is unambiguously right, and inventing a measurement for it would have been the error.

### W022 — CONFIRMED
Six identical solves, one orientation (`final.py`, `v3measure.py`, both re-run). Correctly scoped to
one machine and one build.

### W086 — PARTIAL
See "Derivations that failed as proofs". Determinism is proved; the stronger property §1.1 states —
free-edge direction is "a function of the graph and the balances alone" — needs no exact key ties,
which is measured (0 across 29 goods, reproduced) and not proved. §2.2a's table calls it "proved" in
both columns.
**Spec text to change.** §2.2a table row *"| Free-edge determinism (§1.1) | proved | proved |"* →
"proved as determinism; **measured** as independence from node indexing (0 exact `(DEF, b)` ties on
1444)". §1.1's scan-invariance bullet needs the same split.

### W077–W085, W087, W088 — CONFIRMED
§2.2a's premises, the per-component requirement, and the four-row table are sound and the table's
three weakening rows are correctly assigned — **except** the free-edge row (W086) and except that the
table is incomplete by the fallback case (W124/W193), which is independent of Phase 0 and belongs in
it.

### W120 — CONFIRMED
"One failure is a theorem; the other is an exact rule whose consequence is measured." The sink rule
re-verified 2320/2320 exact (`verify.py`); the monotonicity theorem stands; the contrast gap is
empirical. Correctly split.
**But** the empirical half's cited magnitude is an ε artifact — see systemic finding 3.

### W121, W122 — PARTIAL
**Method.** Re-ran the D-threshold bisection under v1's Laplacian for every Chinese node
(`w3.py`); `verify.py`'s Genoa bisection re-run as a control.
**Evidence.** Genoa co-sink at **f = 1.725** ✓ (control passes). Chinese nodes: beijing 3.614
(9.5% of world spice demand), girin 3.930 (9.9%), hangzhou 4.123 (21.4%), xian 4.606 (12.4%),
yumen 4.500 (**6.8%**), canton 4.772 (17.6%), chengdu 8.078 (14.8%), lhasa 10.671 (10.7%).
**What is actually true.** "3.6–4.8×" and "9.5–21.4%" are exact under the reading "the four Chinese
trade nodes proper" = {beijing, hangzhou, canton, xian}. Under a wider reading, `yumen` sits inside
the multiplier band and outside the demand band (6.8%), and `chengdu` and `lhasa` need 8–11×. The
node set is unstated — the same defect as V223, in the same document, unfixed in both places.
**Spec text to change.** §3.2: *"a Chinese spice sink needs 3.6–4.8×, i.e. 9.5–21.4% of all world
spice demand at one node"* → name the nodes.

### W123, W125 — CONFIRMED
W125 re-derived from source: `../v1-laplacian/claims.md` line 210 carries **C061** verbatim
("`Φ` is a potential, so orienting edges by it is acyclic"), extracted and CONFIRMED in v1;
C499 and C670 depend on it. ✓
W123's three-case sink statement is right as far as it goes and inherits W124's omission.

### W124 — REFUTED / W126, W127, W128, W129, W130 — CONFIRMED
T1 and T2 both re-run through `toys.py` this session:
- **T1** — A(+5), B(−3), D(0), leaf C(−2) on B: selected {B}, flow-terminal {B, D}, promoted {};
  directed `A→B, A→D, B→C, D→B`; **actual sinks {C}, formula set {B}** ✓.
- **T2** — five-cycle S1(+3)–u1(−3)–w(0)–u2(−2)–S2(+2)–S1 with chord w–S1: selected {u1, u2},
  flow-terminal {u1, u2, w}; directed includes `u1→w`, `w→u2`; **actual {u2}, formula {u1, u2}** ✓.
W130's zero exact key ties reproduces (0 across 29 goods, `v3measure.py`).

### W131 — PARTIAL
**Claim.** Sink placement is checked at runtime as **two** checks rather than one weakened one, so
neither counterexample disappears into an escape clause.
**What is actually true.** The reasoning is right and the count is wrong: there are **three** ways the
naive identity fails — T1 (pendant), T2 (free-edge race), and T3 (fallback, this pass). Two checks
catch two of them and the third is converted into a halt on correct behaviour (W193). The document's
own stated reason for splitting the assertion — "written as a single assertion with an escape clause,
both counterexamples would disappear into the clause" — applies to its own fix.

### W134–W142, W147–W152 — CONFIRMED
W137/W138/W139's corrected node-slicing form re-derived: land-province counts `cape_of_good_hope` 19,
`girin` 77, `nippon` 68, `champagne` 33 (fresh, from `map/default.map`'s sea/lake sets), giving
`(77/19)^0.5 = 2.01` and `(68/33)^0.5 = 1.44` ✓ — the figures the spec marks `[unverified in v3.0]`
all reproduce. W150 re-run: across 29 goods × 6 random 1e-9 demand nudges, **zero** support changes
moved more than 1e-6 of flow; largest moved flow 2.18e-9. W147/W148 follow from the reproduced crash.
W152's "values from inputs, structure from the LP support" is exactly right.

### W153, W154 — CONFIRMED
90.9% = **5743/6320** re-measured (`v3measure.py`, `final.py`). 98.8% = **6245/6320** located in
`../v1-laplacian/validation.md` (three sites) as v1's Laplacian figure ✓.

### W155 — CONFIRMED
`Φ_ord` end count across cloves-α, re-run (`w4.py`): α=2 → 16, α=4 → **18** (baseline), α=8 → 15,
α=16 → **22**, α=32 → 17, α=64 → **13**. Range **13–22**, never approaching three, and the v2 band
"9–17" does not contain its own baseline ✓.

### W156 — PARTIAL
**Claim.** A rich **non-sink** node — Beijing, Champagne, Sevilla — bends every edge around it as a
net demander even though flow passes through.
**Evidence.** Under `Φ_w` at α_Φ = 1.5: Champagne `b = −0.0160`, in 1 / out 3, `c_w` rank 5, node
wealth rank 9. Sevilla `b = −0.0131`, in 4 / out 1, `c_w` rank 10, node wealth rank 7. **Beijing
`b = −0.0025`, in 2 / out 2, `c_w` rank 31, node wealth rank 39.**
**What is actually true.** The mechanism is real and Champagne and Sevilla illustrate it. Beijing is
not a rich node under v3.0's own owner-agnostic wealth field on either reading of "rich" — it is
mid-pack and nearly balanced. And "bends **every** edge around it" is not literally true of any of
the three (Champagne points three of four edges away).
**Spec text to change.** §3.9: *"a rich non-sink node — Beijing, Champagne, Sevilla — bends every
edge around it"* → drop Beijing, or replace it with a node that is actually rich under §1.3's wealth
(`gulf_of_siam`, `malacca`, `nippon`, `mexico` all outrank it); and soften "every edge" to "bends
the local flow toward itself".
**Blast radius.** §3.9's `Φ_w` rationale paragraph; §3.1 goal 1's "a horde razing Beijing moves the
sink" and §2.8's "Razed China" / "Ming loses the Mandate" rows all assume Beijing is a wealth pole,
which under owner-agnostic wealth it is not at 1444.

### W157 — CONFIRMED · W158, W160, W162 — PARTIAL (each stale, two now settled)
**W157** accurately describes the spec: §1.3 carries no value for any of the three questions ✓.
**W162** — PARTIAL. Its content ("measured at one province; one point does not establish
linearity") was true when written and is now **stale**: `Base: 0.49 (Yearly 6.00)` at `base_tax = 6`
and `Base: 0.16 (Yearly 2.00)` at `base_tax = 2`, read this session, give two points, and
`GP_COEFF` has four. The question should be struck from §3.13, not carried.
**W160** — PARTIAL. The stated collision between §1.3's structural rule and its vocabulary is real
✓, and the question is settled by W161's own one-tooltip prescription: Barcelona's production
tooltip reads `Production Efficiency: +12.0% / From Technology: +2.0% / Producing Glass: +10.0%`,
so the engine books glass's +10% on production **income** and it never touches Goods Produced or
Trade Value. v3.0's wealth is trade value, so glass's modifier is **outside** it. The collision
resolves in the vocabulary's favour, and it also exists — unflagged — for `chinaware`'s
`province = { local_autonomy = -0.1 }` (W041).
**W158** — PARTIAL. Correct that no *flat* goods bonus was observed (four provinces this session,
none carrying one), and mis-scoped: the class that does exist at 1444 is multiplicative
**Goods Produced Efficiency**, from both an owner source (Industrious ruler, +10%) and a place
source (`bonus_from_merchant_republics`, +3–3.7%), and §1.3 models neither.
W159, W161 and W163 (the settling observations) were each correct, and each took one tooltip.

### W164 — CONFIRMED
The tolerance is scale-coupled and the fix is undecided ✓ (see W055/W056).

### W166, W167, W168 — CONFIRMED
Re-run under the §3.13 calibration (`final.py` PART B): cloves α = 16 sinks at **beijing** ✓;
`hangzhou` holds the richest single province at **27.00** (pid 1821) against Beijing's 19.5 ✓;
max pruned twig mass **0.00149** = 0.149% ≈ 0.15% ✓; silk reach **99.9703%**, cloves **99.9969%** ✓;
span 1..5, spearman −0.539 ✓ (marked `[unverified in v3.0]` and it reproduces).

### W169, W170 — CONFIRMED
`S_g[n][H]` over 29 live goods × 80 × 80 = 185,600 entries × 8 bytes = **1.42 MB** (30 goods →
1.46 MB); at single precision 0.71–0.73 MB. "About 1.5 MB at double precision, 0.75 MB single" ✓.
The build cost, 29 × 80 × (80 + 159) ≈ 554k operations, is under a million ✓.

### W171, W172 — CONFIRMED
Every RANK figure re-measured despite its `[unverified in v3.0]` marker: ρ_val **+0.281** vs DRAIN's
**+0.053**; P(sink | top demand decile) **46.6%** vs **14.1%**; **9** net-producer sinks; **11–17**
sinks per good (387 total, mean 13.3) against DRAIN's **1–8** (mean 3.6); reach 83.29%, 34 orphan
sinks. All exact (`rankrep.py`, `drainrep.py`, `verify.py` 33/33).

### W173, W174 — CONFIRMED
Re-derived from `../v1-laplacian/` rather than from v2's summary. v1's REFUTED table has **23** rows
and its summary says 23 (v2's systemic finding 3 said the table lists 24 — it does not). Of those 23,
**16 are ENGINE-typed**: C037 C038 C049 C050 C101 C128 C130 C131 C139 C407 C433 C434 C447 C486 C532
C538. Their provenance: **9 UNSOURCED** (C037 C049 C101 C128 C130 C139 C447 C532 C538), 3 derivation
(C038 C050 C131), 3 file value, 1 verified-method-unstated. 16 − 3 = **13**. "Nine of the sixteen",
and "thirteen excluding the three that carried derivation" — both exact.

### W176, W177, W178, W180, W181 — CONFIRMED
The binary-string lesson is sound and this pass supplies a second instance of it: `CARAVAN_POWER_DESC2`
is a string that *does* describe behaviour correctly and W066 asserted the opposite without consulting
it, while the propagation string described intent and was wrong. Sources are necessary, not sufficient,
in both directions.

---

# Part 6 — `Φ_w` and the aggregate (§1.6, §3.9)

### W054, W055, W056, W057, W058 — CONFIRMED
Scale invariance in exact arithmetic (the four-part argument is sound: Phase 0 reads signs, HHI uses
mass shares, the LP optimum scales linearly with identical net-flow signs, the priority key is
order-isomorphic under positive scaling). Implementation premise re-measured (`w1.py`): identical
orientation at ×1, ×10, ×10³, ×10⁶; **13 edge flips at ×10⁻²** and at ×10⁻⁴; at **×10⁻⁶ the sink set
collapses to a single node** (`genua`). Largest |b_w| = **0.022576** ✓.

### W059, W060 — CONFIRMED
Re-measured (`v3measure.py`, `phiw3.py`): sinks `hangzhou`, `english_channel`; `c_w` ranks **3** and
**2**; node-wealth ranks **12** and **1**. Eight sources `kongo james_bay mississippi_river chengdu
cuiaba australia yumen safi`, `c_w` ranks **44–75**, mean degree **3.12** against the map's **3.98**.
Phase 1 selects `genua`; both sinks arrive by stall promotion; `genua` ends a transit node ✓.

### W061, W062, W063 — CONFIRMED
Re-run under **both** sweeps (`w6.py`): deterministic **2774/4611 = 60.2%**, scan-order
**2891/4611 = 62.7%**. `Φ_w` agreement **2462/4611 = 53.4%** (52.1% value-weighted). Gap 6.8 points
✓. W063's attribution of 62.7% to the superseded sweep is now demonstrated, not asserted.
*(Side observation: under the scan-order sweep `Φ_ord` has **13** ends, not 18 — so §3.9's "18 end
nodes, 9 of which terminate no good" is correctly the deterministic figure.)*

### W064 — CONFIRMED (stipulated)

### W053, W182–W189 — CONFIRMED
The latent-good treatment is the correction v3.0 got right. Re-derived: **58** provinces carry
`latent_trade_goods = { … coal … }`, **45** are owned at 1444 and all 45 are `is_city` and in a node
✓. Repricing those 45 to coal moves world wealth **10572.4 → 10788.8** and flips **10 of 159 `Φ_w`
edges** ✓ (`w1.py`). Coal's base price 10.0 is the highest in vanilla ✓. Coal is the only latent
good in vanilla. The reasoning chain W182→W186 is sound and is the correct reading of what v2.1 got
backwards.

### W190 — PARTIAL
**Claim.** The 3-mass gravity kernel hits any chosen end count exactly with **66%** vanilla-arrow
agreement in the reproduced construction.
**Evidence.** Re-run (`phiw3.py`): k masses → k ends exactly for k = 1…6 at γ ∈ {0.1, 0.3, 0.5, 0.7};
**at γ = 0.9 both k = 5 and k = 6 give 4 ends**. Best 3-mass agreement **105/159 = 66.0%** at
γ = 0.97 ✓; 69% would be 110/159 and is not reached at any γ tested.
**What is actually true.** 66% is right. "Hits any chosen end count exactly" holds over most of the
γ range and not all of it, and the construction's γ is unstated.

### W191, W192 — CONFIRMED
§1.5's gold argument now reads no income field ✓ (the last live reference to the superseded wealth
formula is gone — verified by search). §1.7's probe-14 disposition is consistent with W111.

### W115 — CONFIRMED
Re-run: under the §3.13 calibration `spices` sinks at **doab** and **genua**; **no Chinese node**;
`cloves` sinks at **beijing** ✓ (`final.py` PART B).

### W116, W119 — CONFIRMED (design, on W117's measurement)

---

# Part 7 — File values and remaining claims

### W132, W133 — CONFIRMED
`00_prices.txt` re-read: sugar 3.0, cocoa 4.0, coffee 3.0 against grain 2.5 → **1.2×, 1.6×, 1.2×** ✓.
Largest: coal **10.0**, cloves **8.0** ✓, neither Caribbean.

### W143 — PARTIAL / W144, W145, W146 — REFUTED
**Method.** Re-parsed every `change_price` block in the install, in two scopes (`leftovers.py` and a
fresh full-tree scan).
**Evidence.** Spec's four trees: **101** blocks → 12 below 2.0, 3 exactly on 2.0 (gems, silk, wool),
11 with no negative event. Whole install: **154** blocks (the extra 53 all in
`history/countries/HAB - Austria.txt`, 13 negative) → **13 below 2.0, 2 exactly on 2.0, 11 with no
negative event**. The single mover is wool, via `NEW_DRAPERIES` at −0.25 (history, 1540.1.1) against
−0.20 (`events/PriceChanges.txt`) under the same key.
**What is actually true.** "12 of 30" is correct *within the stated scope* and the stated scope is
justified by a false premise. The reachable-sublinear count in vanilla is **13**.
**Spec text to change.** §3.5: *"**12 of 30 goods** can be pushed strictly below 2.0 … three more —
`gems`, `silk`, `wool` — land *exactly on* 2.0 … All 101 `change_price` blocks in `events/`,
`decisions/`, `missions/` and `common/` were parsed; `history/` contributes only positive entries."*
→ "**13 of 30** … two more — `gems` and `silk` — land exactly on 2.0 … All **154** `change_price`
blocks were parsed, including the 53 in `history/countries/`, 13 of which are negative; `wool`'s
largest single negative is the history file's −0.25, not the event file's −0.20." §3.13's
"12 … 11 … 3" partition needs the same correction (W165).

### W165 — PARTIAL
Inherits W143's scope error: 13/11/2, not 12/11/3.

### W065 — CONFIRMED
`MERCHANT_MAX_POWER_BONUS = 2.0`; `TRADE_MERCHANT_PRESENT = 0.1, -- bonus on income if trade present`
✓, and §2.3's constants table does split the two rows ✓.

### W070 — CONFIRMED
`CARAVAN_FACTOR = 3.0` ("Development is divided by this factor"), `CARAVAN_POWER_MAX = 50`,
`CARAVAN_POWER_MIN = 2` ✓; and the engine's own `CARAVAN_POWER_DESC2` states development/3 plus
policies and ideas, with no trade-power term ✓.

### W072, W073 — CONFIRMED
The sweep's comparisons are of input-derived floats over the LP's support, not integer arithmetic;
cross-machine reproducibility reduces to the LP's. Sound, and the correction to v2 is right.

### W074, W075, W076 — CONFIRMED as design statements, with systemic finding 1
W075's simplex requirement follows from W007. W076's conservation identity is immediate from W016
and re-measured exact (`unserved == stranded` to <1e-9, 29/29). **W074 is the one that the reference
does not implement**: "with local goods modifiers only" is specified and absent from `solver.py` —
see systemic finding 1 for the measured consequence.

### W002, W004, W005 — CONFIRMED / W001 — CONFIRMED / W006 — PARTIAL
W004 verified line by line in the v3.0 text: §1.7 "+10% bonus on trade income" (C070) ✓; §1.10 "not
a function of raw trade power at all" (C135) ✓; §3.3 "1.2–1.6× grain" (C389) ✓; §3.14 "about 1.5 MB
at double precision" (C594) ✓. W006 is PARTIAL for systemic findings 2 and 3: two of v3.0's own
measured figures do not carry a script that produces them.

### W105, W106, W113 — CONFIRMED
W106's declaration-order instruction and its "non-fatal but logs one error per link" justification
are exactly what this session measured.

### W133 — CONFIRMED · W135, W136 — CONFIRMED
W135's "what still moves" list is exactly right under owner-agnostic wealth, and W053/W187 supply
the trade-good half of it with a number. W136's besieged-province argument follows from V038
(`trade_goods_size_modifier` on devastation, occupation, siege, prosperity), re-read this session in
`00_static_modifiers.txt`.

### W193 — REFUTED / W194, W195 — CONFIRMED
W194's equality-as-monitor and W195's pendant row are both correct, and T1/T2 are correctly
attributed: T1 is the pendant case (Phase 0), T2 is the free-edge race inside the 2-core. The
distinction between an unconditional halt and a monitor is **coherent as stated** — containment is
the weaker, always-true direction and equality is the measured one. It fails only because the
containment *set* is written as `{selected} ∪ {promoted}` when the sweep maintains
`{selected} ∪ {promoted} ∪ {fallbacks}`. The fix is one word in W193, not a restructuring: assert
containment in `{selected} ∪ {promoted} ∪ {fallbacks}`, and define the fallback in §1.1.

### Coverage check
Every ID W001–W195 is named above with a status; none is grouped without one. The 166 CONFIRMED
break down as: the wealth block minus its four partials and two refutations (Part 4), the §1.1 and
§2.2a derivations minus W086 (Part 5), the game-settled ENGINE facts minus W101 and W118 (Part 3),
the `Φ_w` block minus W190 (Part 6), and the file values minus W041/W045/W144–W146 (Part 7). The
DESIGN and OUTCOME rows are graded on whether they state the spec's requirement accurately and give
a true reason — which is how W193, a DESIGN row, ends up refuted.

---

# Method notes and restoration

**Game sessions run this session.** Four EU4 launches, all detached via
`Invoke-CimMethod Win32_Process Create`, driven by `SetCursorPos`/`mouse_event`/`keybd_event` with
DPI-aware `CopyFromScreen` capture at 2880×1800:

1. **Vanilla, Castile 1444** (checksum 491d) — Garnatah, Caceres, Girona and Barcelona province
   windows and tooltips; Valencia and Sevilla node windows; the France power itemisation; the
   incoming-entry click.
2. **`pgt_permute`, Castile 1444** (checksum 3047) — 159 `tradenodedefinition.cpp:61` errors; game
   played; Sevilla node window tab order.
3. **`pgt_cycle`** (checksum not reached) — `EXCEPTION_STACK_OVERFLOW`, third reproduction.
4. Vanilla again as the control for (2) and (3).

**Config handling.** OneDrive's cloud provider is still not running, so `settings.txt`,
`dlc_load.json`, `gameplaysettings.txt` and `continue_game.json` remain unreadable placeholders. As
in the prior session they were **renamed aside** (`*.wbak`), replaced with a low-VRAM `settings.txt`
and a hand-written `dlc_load.json`, and **restored afterwards**. Verified against the
pre-session snapshot: `settings.txt` 2509 B, `dlc_load.json` 185 B, `gameplaysettings.txt` 118 B,
`continue_game.json` 125 B, all still offline placeholders. No `.wbak` file remains.

**One thing not restored.** `logs/error.log` was rotated to `logs/error.w_vanilla.log` and
`logs/error.w_permute.log` for clean reads; EU4 had already overwritten the prior session's
`error.log` when this session's first vanilla run started. `logs/error_old.log` (14:45) is
untouched, and the prior session's crash-dump logs are preserved inside
`crashes/eu4_20260820_134250/` and `crashes/eu4_20260820_134617/`.

**Left in place as evidence.** `crashes/eu4_20260820_165621/` (this session's cycle crash) and the
two rotated logs. The probe mods and the three start-state saves were already present and were not
modified.

**What I did not do.** I did not re-run the `pgt_flip_ordered` link-reversal session (W103/W104), the
§3.10 income-factoring tolerances, or the §3.11 caravan-recipient probe. The first is graded on its
on-disk artifact plus indirect corroboration; the second and third are marked
`[unverified in v3.0]` in the spec and stay that way here.

**If this pass had found nothing.** It did not, so the question is moot — but the reason it found
what it did is worth stating, because it is repeatable: **three of the ten refutations came from
re-reading a tooltip the previous pass had quoted only the top of, and two more came from widening a
file scan the previous pass had narrowed.** Neither required a new idea. The single highest-yield
action available to the next pass is to re-run the four measurements this one could not: the
link-reversal session, the income-factoring tolerances, the caravan recipient, and the §3.13
calibration table — every one of which is currently carried on a document rather than a run.
