# Validation — Per-Good Trade Network Spec v6.0

Every claim in `claims-v6.md` (Y001–Y174) re-derived from primary sources. No status is inherited
from `validation-v5.md`, `validation-v3.md`, `scripts/validation-v6-round1.md` or any other prior
audit; where a prior audit is cited it is cited as a *document under examination*, never as evidence.

**Sources actually opened.** The 1.37.5.0 install at
`C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV` (province history, `common/`,
`events/`, `missions/`, `map/`, `localisation/`); the save
`save games\VANILLA_start.eu4` (`gamestate`, parsed independently of `prov1444.json`); the shipped
save `tutorial/eu4_tutorial_chapter10.eu4`; `scripts/solver.py`, `drain.py`, `flowop.py`,
`measure6.py`, `verify6.py`, `mutate6.py`, `toys.py`, `rankop.py`, `rankrep.py`, `drainrep.py`,
`basin.py`, `europe.py`, `pdx.py`; the v1–v5 spec, claims and validation documents; and
`per-good-trade-spec.md` itself.

**Method split.** Derivations are checked as arguments and measurements by re-running them; where a
claim carries both, the two verdicts are stated separately inside the section. Measurements were
re-run in a scratch tree (`/tmp/v6audit`) importing `scripts/solver.py` and `scripts/drain.py`, with
the file-value and save-parse claims cross-checked against the raw files by an independent parser
rather than against `prov1444.json`. `measure6.py` was re-run and reproduces `measure6.out` byte for
byte, so where a figure is only in `measure6.py` that is said explicitly.

---

## Summary

| Status | Count |
|---|---|
| CONFIRMED | 145 |
| PARTIAL | 24 |
| REFUTED | 5 |
| UNVERIFIABLE | 0 |
| **Total** | **174** |

### REFUTED

| ID | One-line reason |
|---|---|
| Y011 | `verify6.py` checks 15 numeric figures on the spec, not "every measured figure" — the spec's own 1.71-wide band, 22.1, 580/580, 13.40, 0.98%, 89, 226.7/143.0, 16.8%/6.9%, 23/15 flips, 3.61×, 21.6%/17.7% are all unchecked. |
| Y033 | `trunc(base_tax / 12)` gives 0.50 at `base_tax` 6, not the observed 0.49; the schema is `trunc(base_tax × 0.0833333)`. |
| Y040 | v3.0 writes "giving 0.61", not "0.6125 shown as 0.62" — correct span is v4.0 and v5.0, and the claim contradicts the spec's own sentence 19 lines above. |
| Y062 | Maximum `base_tax` over counted provinces is 15 (province 1821); 33 is the maximum *total development*. |
| Y132 | Zeroing `hangzhou`-node development flips 22 of 159 edges, not 23. |

### PARTIAL

| ID | One-line reason |
|---|---|
| Y003 | 105.30 ducats is 0.99% of the spec's own world wealth (10,607.40); 0.98% only against the apparatus-inclusive 10,712.70. |
| Y004 | Of the three IDs cited, only W041 is a refutation — X030 is PARTIAL and X034 is CONFIRMED (as v5's charge against v4). |
| Y007 | The convention is stated, but §3.5's "The install carries 161 textual `change_price` blocks" is an unscoped install-wide absolute and a whole-install sweep finds 162. |
| Y008 | §3.15 keeps two maintained measurements for rejected operators: the v1-Laplacian entry's 4–97 / 211–15,010 contrasts and RANK's "a sixth of world demand". |
| Y034 | "Not twelve times the displayed figure" holds; "the `Base` line is its truncated twelfth" fails at `base_tax` 6 (0.50 ≠ 0.49). |
| Y039 | The example rules out an additive percentage and rules out multiplying the truncated display, but cannot establish an *ordering* of a coefficient and a multiplicative percentage — they commute. |
| Y054 | The count (20) and the conclusion hold; "omit or comment out" is wrong for 12 of the 20, which carry `is_city = yes` only in a post-1444 dated block. |
| Y087 | The Channel's basin grows 18 → 28 nodes only to ×1.44, then shrinks and the Channel loses its end entirely at ×1.64. |
| Y090 | "The Channel holds an end throughout" is false at ×2.00, the table's own last row, where the sole sink is `genua`. |
| Y105 | File structure and all three define values confirmed; "the define applies to seven of the nine" is an inference from reading `cooldown = no` as an opt-out and is stated in no shipped file. |
| Y106 | "Most of the ladder" is not demonstrated — of §1.10's seven listed thresholds two are trading policies, and whether the two trade-company rows are covered by a leader-swap cooldown is not established. |
| Y115 | The three quoted per-good spans are not reproducible; fresh replicates give 3.5–10.2, 4.1–6.1 and 3.4–4.1 ms. |
| Y116 | v5.0's quote verified verbatim; the per-replicate counts inside the interval come out 0, 1, 0 rather than 1, 0, 0. |
| Y120 | 580/580 and "always a different optimal vertex, never a sweep tiebreak" confirmed; the mean is 21.5–21.9 flips on the v6 field, not 22.1, and the 8.9e-16 objective figure is reproducible from no script here. |
| Y121 | 10 of 10 goods confirmed; max objective gap on independent permutations is 2.22e-15, above the quoted ≤1.8e-15. |
| Y137 | The four figures reproduce to ±0.02 as multiples of the node's **wealth**, not of its demand; as demand multiples they are 6.9×–10.4×. |
| Y138 | The non-alignment holds; "other nodes in the region need more still" is false for `girin` (×3.89) and `yumen` (×4.49), both inside the quoted 3.6–4.9 band. |
| Y143 | Per-tree figures exact and summing to 161; a whole-install sweep finds 162 (`patchnotes/1.8 Patchnotes.txt`). |
| Y149 | "A majority terminate no good at all" is 7 of 14 — exactly half — on the v6 field. |
| Y152 | The magnitude class (an exact identity in doubles) is confirmed; an independent construction over the five named nodes gives 0 to 2.15e-16, not 3.7e-16, and no script reproduces the quoted figure. |
| Y159 | 0.41%, "redistributive and single-digit percent" and "at most 0.1%" all verified; the 5.96 figure is v1–v3.0 — v4.0 deleted it and asserts its absence in its own harness. |
| Y160 | The 0.00% floor reproduces; 4.6% and "up to 49% in general" have no construction on record, and an independent per-good-propagation construction gives 0.00%–1.24%. |
| Y161 | In tension with Y160 — the same parenthetical quotes 0.00%–4.6% and 49% two clauses before "No figure is quoted here". |
| Y170 | The alignment win, orphan sinks, net-producer sinks and the sinks-per-good multiple all confirmed; "a sixth of world demand stranded" measures ~30% on the v6 field, and quoting it contradicts the entry's own "No figures maintained". |

---

# §0 — Front matter

## Y001 — v6.0's substantive change is §1.3: wealth reads development, trade good and condition only

**Status:** CONFIRMED (stipulation)
**Method.** Read `per-good-trade-spec.md` lines 14–24 and §1.3 lines 176–200; read
`scripts/solver.py`'s `province_table()` and the four `STATE_*_MOD` dicts.
**Evidence.** The spec states it verbatim. `solver.py` computes
`tax = TAX_COEFF*base_tax*(1+tmod)` and `gp = GP_COEFF*base_production*(1+gmod)` with `gmod` from
the devastation static modifier only and `tmod = 0`, and reads `owner` solely as a counting filter.
No owner field enters any wealth term, so owner-agnosticism holds by construction rather than by a
rule. Internally consistent, and the rationale (an input surface with no classification question in
it) is what the implementation actually delivers.

## Y002 — the two-test classifier and everything it governed are deleted

**Status:** CONFIRMED
**Method.** Grepped the v6.0 spec for the deleted apparatus; diffed `scripts/solver.py` against
`../v5-owner-agnostic/scripts/solver.py`.
**Evidence.** "Leviathan" occurs 0 times in the v6.0 spec. The classification table, the
great-project/`starting_tier` paragraph, the ten permanent modifiers, the centre-of-trade row, the
`production_leader` row and the buildings row are all absent; the only surviving mentions are
historical (lines 16 and 182, describing what was removed) plus one §3.13 settled-note about
`local_production_efficiency`. v5's `LOCAL_TAX_MOD`, `LOCAL_TV_MOD`, `MON_FLAT`, `MON_GPMOD`,
`MON_TVMOD` and `PERM_FLAT` are gone from `solver.py`.
*Note, not a refutation:* the sweep script `scripts/wealthmodel.py` is still on disk, referenced by
no `.py` in `scripts/` and by no line of the spec — deleted from the model, not from the directory.

## Y003 — the deleted apparatus was worth 0.98% of world wealth on the 1444 start

**Status:** PARTIAL
**Method.** Re-added v5.0's classification (`gems` `local_tax_modifier` 0.15, `incense`
`trade_value_modifier` 0.10, the six great-project provinces, the ten permanent-modifier provinces)
on top of the v6.0 field and differenced; ran three orderings of the flat/multiplicative terms and
both province filters.
**Evidence.** Delta = **105.30** ducats under every variant. Against the v6.0 field
(10,607.40, the number the spec itself quotes as world wealth) that is **0.9927%, i.e. 0.99%**. It is
0.98% only if divided by the apparatus-*inclusive* total 10,712.70 (0.9829%). Under the `is_city`
filter: 105.10 on a base of 10,568.80 = 0.9944%.
**Should carry:** 0.99% of world wealth, or 0.98% of the apparatus-inclusive field with the
denominator named. As written the quoted digit depends on an unstated choice of denominator.

## Y004 — the classification was wrong in both independent audits that examined it

**Status:** PARTIAL
**Method.** Opened `../v3-owner-agnostic/validation-v3.md` at W041, `../v5-owner-agnostic/validation-v5.md`
at X030, X033, X034 and X035, and `../v4-owner-agnostic/validation-v4.md` plus
`../v4-owner-agnostic/scripts/validate_v4.py`.
**Evidence.** W041 is **REFUTED** in validation-v3.md ("At least a fourth, and a whole further class.
`chinaware` carries `province = { local_autonomy = -0.1 }`"). But **X030 is PARTIAL** and **X034 is
CONFIRMED** — X034 confirms *v5.0's charge against v4.0*; it is not itself a refutation of the
classification. The head-on refutation in v5.0's audit is **X035** ("The enumeration misses
`provincial_production_size` and the two non-owner-gated `province_triggered_modifiers`, and counts
five province-state static modifiers where there are four"), with X033 PARTIAL.
The harness half holds and is understated: validation-v4.md records "203 assertions, 0 failed" and
grades W041 CONFIRMED, and all six of its W041 assertions (`validate_v4.py` lines 44–58) read only
`common/tradegoods/00_tradegoods.txt` — the one-file sweep that *is* the error, so the harness
structurally could not have caught it.
**Should carry:** cite X035 (and X033) rather than X030/X034.

## Y005 — three start-state reads are corrected in the same pass

**Status:** CONFIRMED
**Method.** Verified each independently (Y046/Y048/Y050 for `on_startup`, Y053 for dated
`add_base_*`, Y054 for `is_city`) and checked `solver.py` implements all three
(`ON_STARTUP_DEVASTATION`; `province_table()` with the `is_city` test dropped; `prov1444.json`
carrying the accumulated `base_tax = 6` for province 1).
**Evidence.** All three corrections are real, all three are in the spec, all three are in the solver.

## Y006 — a canonical node order is a correctness requirement because Phase 2's LP is degenerate

**Status:** CONFIRMED (derivation, resting on Y119–Y121, which measure out)
**Method.** Re-ran the degeneracy experiments (Y119, Y120, Y121).
**Evidence.** Nine distinct optimal supports from nine arc orderings on every good tested, and
580/580 node relabellings changing the orientation with a different LP support every time.
Presentation order does select which optimum is returned, so the stated reason supports the stated
requirement.

## Y007 — prose convention: no empirical absolutes

**Status:** PARTIAL
**Method.** Read the convention at spec lines 26–30, then swept the spec for surviving superlatives,
universal quantifiers and unscoped thresholds and tested the checkable ones.
**Evidence.** The convention is stated as claimed and is mostly honoured — "Coal's base price of 10.0
is the highest **in the shipped price table**", "No Europe→sink route passes the Cape — **checked
from** `genua`, `north_sea` and `english_channel`", "**No shipped file** states that devastation's
scaling is linear" are all properly scoped and each verified true. The residual violation is §3.5's
"**The install carries 161 textual `change_price` blocks**" — an unscoped install-wide absolute that
a whole-install sweep contradicts: 162, the extra hit being `patchnotes/1.8 Patchnotes.txt:445` (see
Y143). §1.10's "No mission, decision, event, or trade company in 1.37.5 names a trade node" is a
second unscoped universal, though a verified one.
**Should carry:** the 161 sentence needs the per-tree scoping the rest of its own sentence already
has.

## Y008 — prose convention: no maintained figures for any rejected operator

**Status:** PARTIAL
**Method.** Read §3.15 entry by entry and checked which rejected-operator entries still carry numbers.
**Evidence.** Honoured for `Φ_ord` ("*No figures are maintained for it*"), the gravity kernels
("*No figures are maintained for it*") and the seeded basins. **Not** honoured for two entries the
claim explicitly lists as covered:
- the **v1 Laplacian** entry retains "the contrasts run **4–97 on supply against 211–15,010 on
  demand** over the 28 goods produced in more than one node" — a maintained measurement (it does
  reproduce: 4.0–97.0 and 211.1–15009.9 over 28 goods);
- the **RANK** entry retains "a sixth of world demand is stranded", which is a figure and does not
  reproduce (Y170).
**Should carry:** either add RANK's delivery figures and the Laplacian contrasts to the covered list,
or delete them.

## Y009 — load-bearing comparisons are stated as directions rather than maintained figures

**Status:** CONFIRMED
**Method.** Read §3.9, §3.15 and §1.6's superseded-aggregate sentence; then tested each direction on
the v6 field.
**Evidence.** "scores **higher** than `Φ_w` on self-coherence", "The superseded marking-order
aggregate scored higher on that measure", "its end count does not concentrate as demand
concentrates", "leaves demand unserved at every tuning tried" are all directional, and each direction
is independently true here: Φ_ord 60.4%/60.1% against Φ_w's 53.6%/52.3%; Φ_ord 14 ends at every
cloves-α from 2 to 64; basin unserved 0.45–0.53 at every seed count tried.

## Y010 — every graded claim from validation-v5.md (22 refuted, 39 partial, 1 unverifiable) is folded through

**Status:** CONFIRMED
**Method.** Counted `### Xnnn` / `**Status:**` pairs over X001–X196 in
`../v5-owner-agnostic/validation-v5.md`; compared to its own summary table; then listed
`fixes-agreed.md` §5's table rows and set-differenced against the 62 non-CONFIRMED IDs in both
directions.
**Evidence.** 134 CONFIRMED / 22 REFUTED / 39 PARTIAL / 1 UNVERIFIABLE = 196, body and summary table
agreeing exactly, no gaps or duplicate IDs. `fixes-agreed.md` §5 carries 62 rows and its ID set is
identical to the 62 non-CONFIRMED IDs — nothing missing in either direction; X022, the sole
UNVERIFIABLE, is present. Its own action tally (MOOT 15, DROP 4, SOFT 4, VALUE 19, ARG 12, GAME 5,
MECH 3) sums to 62.

## Y011 — verify6.py re-derives every measured figure from the document text and fails if the two disagree

**Status:** REFUTED
**Method.** Read `scripts/verify6.py` in full; ran it against the spec (`25 checks, 0 failed`) and
against `fixes-agreed.md` (`21 checks, 5 failed`); ran `scripts/mutate6.py` against the spec
(`caught 12 of 12`); counted the figures `measure6.py` computes against the figures `run_spec()`
compares.
**Evidence.** The inversion is real and the *second half* of the claim is true: needles are built from
computed values, routing is by document content, an empty check set now fails, and the harness does
fail a stale document. But "every measured figure" is false. `run_spec()` performs **15 numeric
comparisons, 2 cross-phrasing checks and 8 absence checks** — 25 in all — against `measure6.py`'s
**60** labelled figures and a considerably larger set of figures the spec prints. Unchecked figures
the spec prints include: the widest α_Φ band (**1.71** wide, **[3.50, 5.21]** — `run_spec` never
looks at it, while the checklist path `run()` still carries the *typed literals* 1.70 / 3.51 and so
certifies the stale value); the devastation cost 13.40; 0.98%; the 89 and 87 province counts; 31
`incense`; 12.70; 2.40; the 3 extra coal flips; 22.1 / 580 of 580 / 8.9e-16 / ≤1.8e-15 / 10 of 10;
226.7 and 143.0; 16.8% and 6.9%; the 23 and 15 razed-China flips; 3.61× / 4.12× / 4.60× / 4.77%;
9.4%–47.0%, 21.6%, 8.6%–32.0%, 17.7%, 21.3%, 17.5%; 106.4 and 532.0; 23.6–143.2; ×1.65 and ×2.15;
×2.9–×3.5; 4–97 and 211–15,010; 3.7e-16; 0.00%–4.6% and 49%; and "seven distinct downstream sets".
`mutate6.py`'s twelve mutations are derived from the same twelve checked figures, so the 12-of-12
result measures the harness against itself and is not coverage evidence.
**Should carry:** "re-derives fifteen of the measured figures from the document text and fails if the
two disagree", or the check set has to grow to match the claim.

# §1.1 — Trade direction

## Y012 — the fallback fires only when every candidate is support-isolated with zero post-peel balance

**Status:** CONFIRMED (derivation)
**Method.** Traced `drain.py`'s `sweep_priority()`: `ready(u)` requires `cnt[u] == 0` and
(`u in Sset` or `len(outs[u]) > 0` or a marked free neighbour); at a stall `gated` = unmarked with
`cnt == 0`, `terminals` = gated with `len(outs) == 0 and inflow > ZERO_TOL`, and the fallback fires
only when `terminals` is empty.
**Evidence.** If `cnt[u] == 0` and `len(outs[u]) > 0` then `u` is ready, so no gated node at a stall
has a flow out-arc. `terminals` empty then forces every gated node to have `inflow == 0` as well, so
every candidate carries no flow arc in either direction — support-isolated. A node with `β ≠ 0` must
carry flow (the LP imposes node balance), so every candidate has `β = 0`. The `β` in question is the
array returned by `phase0()`, i.e. the post-fold balance, not the raw `b` — confirmed by reading the
call chain `phase0(b) → beta → sweep_priority(core, beta, …)`.

## Y013 — the condition is about the folded field, so a map with non-zero raw balances can still reach the branch

**Status:** CONFIRMED (derivation)
**Method.** Followed the same call chain; constructed the folding case by hand.
**Evidence.** `phase0()` does `beta[u] += beta[v]` when peeling pendant `v` into parent `u`. A
pendant with `b = +x` on a parent with `b = −x` leaves the parent at `β = 0`, so a map whose raw
balances are all non-zero can present a wholly zero folded core. The claim follows directly.

## Y014 — on a connected core the branch needs the folded balance to vanish across the core

**Status:** CONFIRMED (derivation)
**Method.** Reconstructed the argument from `drain.py`'s sweep, then checked the two instantiations.
**Evidence.** The stronger statement is provable, not merely sufficient. Suppose the marked set is
non-empty and the core is connected. Any unmarked node adjacent to a marked node is either ready (a
free edge to a marked node, or its own flow out-arc with `cnt == 0`) or has `cnt > 0`, i.e. an
unmarked flow out-neighbour. Following out-arcs from such a node terminates (the flow subgraph is
acyclic) at a node with `cnt == 0` and non-zero inflow — a flow-terminal demander — which is gated,
so `terminals` is non-empty and the branch taken is *promotion*. Hence a fallback can only fire at
the very first stall, with nothing marked. Nothing marked and nothing ready implies no node has a
flow out-arc, hence no flow at all, hence `β ≡ 0` across the core (`Σβ = 0`, and any non-zero `β`
forces flow). Both instantiations then follow: per good, `β ≡ 0` on a component means no producer and
no consumer; in aggregate `b_w = 1/N − c_w ≡ 0` means `c_w(n) = 1/N` for all `n`, i.e. every node's
`Σ wealth^α_Φ` equal.

## Y015 — uniform per-province wealth does not deliver that, because nodes hold between 0 and 72 counted provinces

**Status:** CONFIRMED (measurement)
**Method.** Counted the model's counted provinces per node from `solver.ROWS`.
**Evidence.** Minimum **0** (one node holds no counted province), maximum **72** (`mexico`). Equal
per-province wealth therefore gives unequal node sums, so `c_w` is not uniform and `b_w ≢ 0`. The
derivation and the figures both hold.

## Y016 — where the wealth key ties, the node index decides

**Status:** CONFIRMED (derivation)
**Method.** Read `drain.py`'s fallback: `s_star = max(gated, key=lambda v: (NODEW[v], -v))`.
**Evidence.** Equal `NODEW` is broken by `-v`, so the lowest node index wins. Matches §1.1's "ties by
index".

## Y017 — §2.8's containment set includes the fallbacks because of T3, and the wealth tie is not why §2.4 needs a canonical order

**Status:** CONFIRMED (derivation)
**Method.** Ran `scripts/toys.py`; cross-read §2.8's sink-set rows and §2.4 item 1.
**Evidence.** T3 output: `S0(selected)=[]`, `promoted=[]`, `FALLBACK promoted: ['A']`, actual sinks
`{A}`, formula set empty, "sink inside {selected} ∪ {promoted}: False, inside ∪ {fallbacks}: True".
So containment needs the fallback set for a reason that has nothing to do with a tie — T3's wealths
are 3, 2, 1, distinct. The second half is Y140, independently confirmed: the canonical-order
requirement comes from the LP, which moves the orientation with no key tie anywhere (Y128 measures
zero ties on 1444 while Y120 measures 580/580 orientation changes).

## Y018 — on 1444 pendant and fallback cases are empty and the sink set is exactly {selected ∩ flow-terminal} ∪ {promoted}, 29/29, 1–8 sinks, mean 3.72, zero fallbacks

**Status:** CONFIRMED (measurement)
**Method.** Re-ran DRAIN for all 29 live goods, recomputing the formula set from `S0`, the flow-arc
out-degrees and the inflow, and set-comparing against the actual sinks.
**Evidence.** Phase 0 is a no-op on every good (`core` = 80 of 80). Sinks per good min 1, max 8, mean
**3.7241**. Acyclic 29/29. Fallbacks fired: **0**. Formula set equals actual sink set on **29/29**
goods with no mismatch printed. Every figure and the equality both reproduce.

## Y019 — the equality does not become a theorem by attaching conditions; T2 satisfies both and still breaks it

**Status:** CONFIRMED (derivation, with the counterexample run)
**Method.** Ran `scripts/toys.py` T2.
**Evidence.** T2 is core-only (Phase 0 a no-op) and reports `promoted=[]` with no fallback, yet
actual sinks `{u2}` against formula `{u1, u2}` — "EQUAL: False". Both stated conditions hold and the
equality fails, so they are necessary, not sufficient.

# §1.3 — Demand

## Y020 — wealth is owner-agnostic and reads development, trade good and condition

**Status:** CONFIRMED (stipulation)
**Method.** Read spec §1.3 lines 176–200 against `solver.py`'s `province_table()`.
**Evidence.** The three inputs are `PROV[pid]["base_tax"]`, `PROV[pid]["base_production"]` and
`r["good"]`, plus `ON_STARTUP_DEVASTATION` for condition. Nothing else is read. The stipulation and
the implementation agree.

## Y021 — two provinces with the same development, trade good and condition have the same wealth whoever owns them

**Status:** CONFIRMED (derivation)
**Method.** Inspected the wealth expression for owner terms.
**Evidence.** `wealth(p) = TAX_COEFF·base_tax·(1+tmod) + GP_COEFF·base_production·(1+gmod)·price`.
`owner` appears in `province_table()` only in the counting test `if not s.get("owner"): continue` and
as a recorded field. Two provinces agreeing on the three inputs therefore have identical wealth by
construction, and conquest cannot move it.

## Y022 — base_tax, base_production and the trade good are bare attributes, so nothing needs classifying

**Status:** CONFIRMED (derivation)
**Method.** Checked what determines each of the three in the engine's data.
**Evidence.** All three are per-province scalars in the province record (history file and save alike),
set by no country's state — verified by the 2472/2472 history-versus-save agreement on `base_tax`,
`base_production` and owner (Y051). There is no modifier surface to classify because no modifier is
read.

## Y023 — what this gives up: gems' local_tax_modifier, incense' trade_value_modifier, great projects, permanent modifiers and the DLC state

**Status:** CONFIRMED
**Method.** Opened `common/tradegoods/00_tradegoods.txt` at both goods; enumerated the great-project
and permanent-modifier sets from `common/great_projects/` and the undated province-history blocks;
grepped the spec for "Leviathan".
**Evidence.** `gems` carries `province = { local_tax_modifier = 0.15 }` (lines 2015–2022) and
`incense` `province = { trade_value_modifier = 0.1 }` (lines 1890–1897) — both genuinely
province-scoped, both no longer read by `solver.py`. The six great-project provinces (8, 262, 684,
1821, 1822, 2145) and ten permanent-modifier provinces (6, 362, 363, 370, 371, 387, 542, 2151, 2316,
4316) are likewise no longer read. "Leviathan" occurs 0 times in the spec, so the DLC state is gone
with them.

## Y024 — incense trade_value_modifier is live on 31 provinces at 1444

**Status:** CONFIRMED (file/save value)
**Method.** Counted counted provinces whose trade good is `incense`, independently from the save's
`gamestate` and from the history files.
**Evidence.** Save: **31** (385, 388, 389, 401, 402, 538, 557, 604, 619, 667, 676, 1022, 1206, 1207,
1212, 2160, 2161, 2222, 2331, 2342, 2373, 2374, 2677, 2786, 2788, 2789, 2790, 4278, 4283, 4822,
4856). History alone: 30 — the extra one is 4856, whose good the engine rolls (Y026). 31 is the
engine's start state, which is the right basis.

## Y025 — the deleted apparatus covered 89 of the 2,472 counted provinces (43 + 31 + 16 − 1, province 542)

**Status:** CONFIRMED (measurement, independently re-derived)
**Method.** Enumerated all four sets from the install: `gems` and `incense` provinces from the save;
great projects from `common/great_projects/` filtered to `date ≤ 1444.11.11`, a counted start
province, an empty `can_use_modifiers_trigger` and a `province_modifiers` block granting a key wealth
reads; permanent modifiers from undated `add_permanent_province_modifier` in history resolved through
`common/event_modifiers/`. Then took the distinct union.
**Evidence.** gems 43, incense 31, great projects **6** (8 `falun_copper_mine`, 262
`krakow_cloth_hall`, 684/1821/1822/2145 the four Grand Canal provinces), permanent modifiers **10**
(6 `skanemarket`, 362/363/2316/4316 `granary_of_the_mediterranean`, 370/371
`icelanding_fisher_sea`, 387 `coffea_arabica_modifier`, 542
`diamond_mines_of_golconda_modifier`, 2151 `jingdezhen_kilns`). Great projects ∩ permanent modifiers
= ∅, so the apparatus is 16 distinct provinces. gems ∩ incense = ∅; incense ∩ apparatus = ∅;
gems ∩ apparatus = **{542}** exactly. 43 + 31 + 16 − 1 = **89**, and the distinct union computed
directly is also 89. The great-project count is robust to the tier reading (cumulative tiers to
`starting_tier`: 6; `starting_tier` alone: 6).

## Y026 — 87 under the withdrawn is_city filter, and 89 rather than 88 because province 4856 rolled incense

**Status:** CONFIRMED (measurement)
**Method.** Re-ran the union of Y025 with the `is_city = yes` history test applied; checked 4856's
history value and the good the save holds for it.
**Evidence.** Under the filter the union is **87** — the two members dropped are 1207 and 4856, both
`incense`, taking incense from 31 to 29. Province 4856 (`4856 - Barunggam.txt`) has
`trade_goods = unknown` in history and `trade_goods=incense` in the save, so without the roll the
union would be 88. Both figures exact.

## Y027 — goods_produced = GP_COEFF · base_production · (1 + Σ province-state goods modifiers), no flat term

**Status:** CONFIRMED (derivation against the implementation)
**Method.** Compared the spec's code block (line 197) to `solver.py`.
**Evidence.** `gp = max(0.0, GOODS_PRODUCED_FACTOR * s["base_production"] * (1.0 + gmod))` — no
additive term anywhere. Identical to the stated formula.

## Y028 — trade_value = goods_produced · price(good), ducats per year, no local trade-value-modifier term

**Status:** CONFIRMED
**Method.** Same comparison.
**Evidence.** `prod_income = gp * price`. No `(1 + trade_value_modifier)` factor, matching the spec.

## Y029 — tax_value = TAX_COEFF · base_tax · (1 + Σ province-state tax modifiers), ducats per year

**Status:** CONFIRMED
**Method.** Same comparison.
**Evidence.** `tax = TAX_COEFF * s["base_tax"] * (1.0 + tmod)` with `tmod = 0.0` at 1444 and
`STATE_TAX_MOD = {"occupied": -0.5}` as the only tax-side entry. Matches the spec.

## Y030 — GP_COEFF is a shipped file value: provincial_production_size = { trade_goods_size = 0.2 … }, localised "Base Production"

**Status:** CONFIRMED (file value)
**Method.** Opened `common/static_modifiers/00_static_modifiers.txt` and
`localisation/EU4_l_english.yml`.
**Evidence.** Lines 251–254:
`provincial_production_size = { trade_goods_size = 0.2 ; ship_recruit_speed = -0.01 }` — the
ellipsis hides exactly one key. Localisation line 815: `provincial_production_size:0 "Base
Production"`. §2.3's own measurement table records Garnatah's itemisation as "Base Goods Produced:
0.80 / Base Production: +0.80", so the localised name matches the itemised sub-line and both read
0.80 — "the same tooltip line the coefficient was measured off" is fair, though it is the itemisation
line rather than the total line.

## Y031 — it is therefore moddable and is read at runtime, not hardcoded

**Status:** CONFIRMED (stipulation, implemented)
**Method.** Read `solver.py`'s `_read_gp_coeff()`.
**Evidence.** The function regex-reads `provincial_production_size` out of the install file at import
time and raises if the block or the key is missing; `GOODS_PRODUCED_FACTOR` is its return value, not a
literal. `measure6.py` prints "GP_COEFF read from static_modifiers 0.2". A patch or mod changing the
block changes the model.

## Y032 — TAX_COEFF is in no file that has been found

**Status:** CONFIRMED (file value, as a negative)
**Method.** Grepped `common/defines.lua`, all of `common/defines/`, and
`00_static_modifiers.txt` for any development-to-tax coefficient.
**Evidence.** No `TAX_COEFF`, no tax-per-development define. Every tax-named define is unrelated
(`PS_RAISE_WAR_TAXES`, `SCUTAGE_TAX_FRACTION`, `BASE_TAX_COST_MODIFIER`, `FLAT_TAX_AMOUNT`, …).
`common/defines/` contains no tax or `trade_goods_size` reference at all. The counterpart static
modifier `provincial_tax_income` (lines 244–249) grants only `regiment_recruit_speed`,
`local_great_project_upgrade_time`, `local_build_time` and `local_institution_spread` — no tax key.
The only `1.0`-magnitude tax values in the file are `local_tax_modifier = -1.0` on the two autonomy
multiplicative blocks. So the claim's negative holds, and the three places it names are exactly the
places searched.

## Y033 — the tax tooltip's schema is `Base: trunc(base_tax / 12) (Yearly base_tax)`

**Status:** REFUTED
**Method.** Evaluated the stated schema on its own two data points.
**Evidence.** `trunc(6 / 12)` to two decimals is **0.50**, and the observation is **0.49**. The
schema is false on its own first data point — the same defect the claim charges v4.0 and v5.0 with.
`trunc(2 / 12) = 0.16` matches, so only the `base_tax` 6 point discriminates. The schema that
reproduces both is `trunc(base_tax × 0.0833333)`: 6 × 0.0833333 = 0.4999998 → 0.49, and
2 × 0.0833333 = 0.1666666 → 0.16. This is the same constant Y038 uses two paragraphs later
("6 × 0.0833… = 0.49999…"), so the spec contradicts itself.
**Should carry:** `Base: trunc(base_tax × 0.0833333) (Yearly base_tax)`.
*The two observations themselves are single tooltip readings from a prior game session and cannot be
re-observed without running EU4; only the arithmetic is graded here, and the arithmetic fails.*

## Y034 — the parenthetical is base_tax and the Base line is its truncated twelfth; not twelve times the displayed figure, which would give 5.88 and 1.92

**Status:** PARTIAL
**Method.** Evaluated both halves.
**Evidence.** The negative half is exactly right: 12 × 0.49 = **5.88** ≠ 6.00 and 12 × 0.16 =
**1.92** ≠ 2.00, so the `12·X` schema is false on both data points, and the parenthetical is indeed
`base_tax` itself. The positive half — "the `Base` line is its truncated twelfth" — is the Y033
defect: the truncated twelfth of 6 is 0.50, not the observed 0.49.
**Should carry:** "the `Base` line is `base_tax` truncated at the engine's monthly constant
0.0833333", which is what Y038 already says.

## Y035 — v4.0 and v5.0 wrote the schema as `Base: X (Yearly 12·X)`; v3.0 carries neither that schema nor the 0.6125 arithmetic

**Status:** CONFIRMED
**Method.** Grepped all five prior specs for "Yearly 12" and "0.6125".
**Evidence.** "Yearly 12": absent in v1, v2, v3; present at `v4:163` and `v5:170`, identical text.
"0.6125": absent in v1, v2, v3; present at `v4:178` and `v5:185`. v1 and v2 carry no Garnatah tax
example at all. Every clause of the claim holds, and the "false on both of its own data points" part
is Y034's arithmetic.

## Y036 — the monthly production tooltip's Trade Value line is consistent with the same relation on one observation, 3.52 → +0.29, fixing the divisor only to within (11.73, 12.14]

**Status:** CONFIRMED (arithmetic; the observation itself is one game reading)
**Method.** Solved the truncation interval.
**Evidence.** A displayed 0.29 under truncation means 0.29 ≤ 3.52/d < 0.30, i.e.
3.52/0.30 < d ≤ 3.52/0.29, i.e. **11.7333 < d ≤ 12.1379** — the stated (11.73, 12.14] to two
decimals, with the half-open bracketing the right way round. v5.0's [12.00, 12.14] was the narrower,
wrong interval. The single-observation caveat the § marker records is accurate: one reading cannot
pin the divisor further, and only a running game could add another.

## Y037 — both monthly figures being the annual value over twelve is what lets the annual forms add directly, and the tax pair establishes it at two development levels

**Status:** CONFIRMED (derivation)
**Method.** Checked the two tax readings against the annual-over-twelve relation and checked the
additivity argument.
**Evidence.** `base_tax` 6 → 0.49 and `base_tax` 2 → 0.16 are both `trunc(base_tax × 0.0833333)`, so
the relation holds at two development levels (the divisor is 12.000005 rather than exactly 12, which
does not affect additivity). Two quantities on the same annual basis add without conversion; that is
the whole of the argument and it is sound.

## Y038 — 0.49 × 1.25 = 0.6125 truncates to 0.61, not 0.62, so the engine multiplies the untruncated monthly value

**Status:** CONFIRMED (arithmetic; the observation is one game reading)
**Method.** Evaluated both arithmetics.
**Evidence.** 0.49 × 1.25 = 0.6125 → truncated 0.61. The untruncated route:
6 × 0.0833333 = 0.4999998, × 1.25 = 0.62499975 → truncated **0.62**, matching the observation. The
inference is forced: the engine cannot be multiplying the displayed figure.

## Y039 — the example establishes only the ordering — base from development first, percentage second — and nothing finer

**Status:** PARTIAL
**Method.** Enumerated what the observation can and cannot distinguish.
**Evidence.** The observation does establish two things: the percentage **multiplies** rather than
adds (an additive reading gives (6 + 0.25)/12 → 0.52, not 0.62), and it multiplies the untruncated
monthly value rather than the displayed one (Y038). What it cannot establish is an *ordering*: for a
purely multiplicative modifier, `TAX_COEFF·base_tax·(1+m)` and `TAX_COEFF·(base_tax·(1+m))` are the
same expression, and 6 × 0.0833333 × 1.25 and 6 × 1.25 × 0.0833333 both give 0.62499975.
Multiplication commutes, so no observation of this shape can order the two operations. The ordering
becomes observable only once a *flat* bonus exists, which is the very next sentence's subject
(Y041) and which no province in the model has.
**Should carry:** "the example establishes that the percentage multiplies, and multiplies the
untruncated monthly value, and nothing finer; the ordering of the coefficient and a purely
multiplicative percentage is not observable, since they commute."

## Y040 — v3.0 through v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62"

**Status:** REFUTED
**Method.** Opened `../v3-owner-agnostic/per-good-trade-spec.md` at the Garnatah tax example and
grepped v3.0 for "0.6125" and "0.62".
**Evidence.** v3.0 lines 156–157 read: "The engine computes the base from development first and then
applies a percentage — `Base 0.49` then `Tax Income Efficiency 125.0%`, **giving 0.61**." That is the
correct truncation. "0.6125" occurs **0** times in v3.0's spec; "0.62" occurs only at line 861, about
`change_price` prices. The claim is false for v3.0, and it directly contradicts the v6.0 spec's own
sentence 19 lines earlier (line 218: "v3.0 carries neither that schema nor the 0.6125 arithmetic
below"). Both cannot hold.
**Should carry:** "v4.0 and v5.0 read this as …".

## Y041 — flat goods bonuses would add into goods_produced before the price multiply, but under §1.3 no source grants one

**Status:** CONFIRMED
**Method.** Checked what the four province-state modifiers grant, and what `solver.py` can produce.
**Evidence.** All four grant `trade_goods_size_modifier` (multiplicative): `devastation` −2,
`prosperity` 0.25, `under_siege` −0.25, `occupied` −0.5. None grants a flat `trade_goods_size`, and
`solver.py` has no additive term in `gp` at all. So no province in the model exercises the ordering,
exactly as the claim says, and the tooltip's two-block structure (additive `Base Goods Produced`
above multiplicative `Goods Produced Efficiency`) is on record from the prior tooltip sessions and
quoted in §2.3's own measurement table.

## Y042 — province condition is the one further input: four static modifiers from 00_static_modifiers.txt

**Status:** CONFIRMED (file value)
**Method.** Opened `common/static_modifiers/00_static_modifiers.txt` and quoted all four blocks.
**Evidence.** `devastation` (453–462): `trade_goods_size_modifier = -2` — plus
`supply_limit_modifier`, `local_institution_spread`, `local_development_cost`,
`local_manpower_modifier`, `local_sailors_modifier` and two movement-speed keys, none of which wealth
computes. `prosperity` (464–468): `trade_goods_size_modifier = 0.25` (plus `local_development_cost`,
`local_autonomy`). `under_siege` (444–450): `trade_goods_size_modifier = -0.25`. `occupied`
(433–442): `local_tax_modifier = -0.5` **and** `trade_goods_size_modifier = -0.5`. All four values
exactly as stated, all four in that one file.

## Y043 — no shipped file states that devastation's scaling is linear in the level; the model assumes −2 × level/100

**Status:** CONFIRMED (as a negative, verified)
**Method.** Searched for comments on the `devastation` and `prosperity` blocks; grepped the install
for "scaled with devastation", "devastation level", "per devastation", "devastation/100"; checked the
localisation.
**Evidence.** No comment sits on or near either block, though the file *does* document scaling
elsewhere when it applies (line 301 "# Multiplied in provinces of same religion", line 475
"# Multiplied with positive religious tolerance", line 889 "#… multiplied by negative piety in
code"). The only install-wide hit is `defines.lua:380`
`CELESTIAL_EMPIRE_MANDATE_PER_HUNDRED_DEVASTATION` — Mandate, not trade goods. Localisation resolves
the effect at runtime (`DEVASTATION_EFFECTS:0 "Current Effects of Devastation is:\n$WHY$"`) rather
than stating a formula, and prosperity's strings read as on/off. `solver.py` hardcodes
`gmod = -2.0 * dev` with `dev = level/100`. The claim's self-labelling as an assumption is exactly
right.

## Y044 — only occupied touches the tax term; the other three reach goods_produced alone

**Status:** CONFIRMED (file value)
**Method.** Enumerated every key in each of the four blocks.
**Evidence.** `local_tax_modifier` appears only in `occupied` (line 434). `devastation`, `prosperity`
and `under_siege` carry no tax key of any kind. Matches `solver.py`'s
`STATE_TAX_MOD = {"occupied": -0.5}`.

## Y045 — these four are what make the map answer to war: §1.2's volatility, §3.3's besieged province and §2.8's war rows all rest on them

**Status:** CONFIRMED (derivation)
**Method.** Read the three cited passages.
**Evidence.** §1.2: "It moves with devastation, occupation, and prosperity (`00_static_modifiers.txt`:
`devastation`, `occupied`, `under_siege`, `prosperity` all carry `trade_goods_size_modifier`)". §3.3:
"`trade_goods_size` modifiers on the *place* — devastation, occupation, siege, prosperity — still
bite within months. A besieged province genuinely produces less". §2.8: "Major war in China |
Corridors shift for the duration, revert as devastation heals". All three depend on precisely these
four, and nothing else in the model responds to war at all.

## Y046 — eleven counted provinces begin devastated (Bohemia 50, Erzgebirge and Moravia 20), and no province-history file says so; on_startup fires flavor_boh.15

**Status:** CONFIRMED (file value, and independently confirmed in the save)
**Method.** Grepped all 3,923 `history/provinces/*.txt` for `devastation`; opened
`events/flavorBOH.txt` at `flavor_boh.15`; resolved the three areas through `map/area.txt`; then
parsed the save's `provinces={}` block for a `devastation=` field.
**Evidence.** `devastation` occurs in **0** of 3,923 province-history files (the only `devastation`
string under `history/` is in `history/wars/KabyleAlgerianWar.txt`). `flavor_boh.15`
("The Aftermath of the Hussite Wars") is `is_triggered_only = yes` with no trigger gate and applies
`bohemia_area = { add_devastation = 50 }`, `erzgebirge_area = { add_devastation = 20 }`,
`moravia_area = { add_devastation = 20 }` inside a `hidden_effect`. Areas: `bohemia_area` =
{266, 2968, 2970, 4724, 4725} (5), `erzgebirge_area` = {267, 1771, 2967} (3), `moravia_area` =
{265, 4237, 4726} (3) — **11 distinct provinces**. The save carries exactly eleven `devastation`
records, all inside `provinces={}`, all counted: 265→20, 266→50, 267→20, 1771→20, 2967→20, 2968→50,
2970→50, 4237→20, 4724→50, 4725→50, 4726→20 — set-equal and value-equal to `solver.py`'s
`ON_STARTUP_DEVASTATION`, with no extras either way. Only the country modifier
`boh_hussite_destruction` is DLC-gated; the devastation is not.

## Y047 — that devastation costs 13.40 ducats across the eleven affected counted provinces

**Status:** CONFIRMED (measurement)
**Method.** Differenced the field against a no-devastation field province by province.
**Evidence.** **13.40** ducats over **11** provinces, reproducing `measure6.py`'s
"devastation cost in ducats 13.4".

## Y048 — the chain is 00_on_actions.txt → on_startup_effect → 01_scripted_effects_for_on_actions.txt → country_event flavor_boh.15

**Status:** CONFIRMED (file value)
**Method.** Followed all three hops in the install.
**Evidence.** `common/on_actions/00_on_actions.txt:4` `on_startup = {` … `:33`
`on_startup_effect = yes`. `common/scripted_effects/01_scripted_effects_for_on_actions.txt:4716`
`on_startup_effect = {` — the only definition install-wide. Same file, 4787–4796: a
`limit = { tag = BOH … }` guard then `country_event = { id = flavor_boh.15 }`. Every hop exact.

## Y049 — the start state is what the engine produces, not what the history files say, and that costs three separate reads

**Status:** CONFIRMED (derivation)
**Method.** Established each of the three reads independently (Y046/Y050, Y053, Y054) and checked
that each is a case where history and engine state differ.
**Evidence.** Devastation: 0 history files versus 11 save records. `add_base_*`: province 1 reads
`base_tax = 5` undated and the save holds 6. `is_city`: 20 owned counted provinces lack it at 1444
and the save gives all 20 `is_city=yes`. Three genuinely separate reads, each a real divergence.

## Y050 — on_startup also fires flavor_mng.42, flavor_mos.1, flavor_geo.1 and others directly from its own events = { } list

**Status:** CONFIRMED (file value)
**Method.** Read `common/on_actions/00_on_actions.txt` lines 23–32.
**Evidence.** The `events = { }` block inside `on_startup` lists `muslim_school_events.20`,
`flavor_got.1`, `flavor_mng.42`, `flavor_mos.1`, `flavor_fra.206`, `flavor_geo.1`, `flavor_mam.111`
(and one commented-out `flavor_fra.15000`) — seven live ids. All three the claim names are present,
and "and others" covers the remaining four. This is a second path, distinct from the
`on_startup_effect` scripted-effect chain that carries `flavor_boh.15`. `00_on_actions.txt` is the
only on_actions file in the install.

## Y051 — development does not move before the first tick: history matches the save on 2,472 of 2,472 for base_tax, base_production and owner; only trade_goods differs, on exactly twenty

**Status:** CONFIRMED (measurement, independent parser)
**Method.** Parsed every `history/provinces/*.txt` with dated-block accumulation and the save's
`provinces={}` records with an independent tokeniser, then diffed field by field over the counted
set.
**Evidence.** `base_tax` 2472/2472, `base_production` 2472/2472, `owner` 2472/2472 (and, unclaimed,
`base_manpower` 2472/2472 and `controller` 2472/2472). `trade_goods` matches 2452/2472 —
**20** diffs, every one `history=unknown`: 774, 862, 895, 897, 907, 966, 1809, 2014, 2503, 2510,
2571, 2593, 2596, 2669, 2671, 2932, 4856, 4901, 4902, 4923.

## Y052 — v6.0's first draft said flavor_geo.1 carries add_base_tax; it does not, and those keys sit in flavor_geo.3, which on_startup does not fire

**Status:** CONFIRMED (file value)
**Method.** Read `events/FlavorGEO.txt` at both events and grepped the install for `flavor_geo.3`.
**Evidence.** `flavor_geo.1` (lines 8–46): the whole `immediate` is `add_legitimacy = -20`,
`add_country_modifier = { name = "geo_powerful_nobles" duration = -1 }` and
`set_country_flag = geo_received_starting_event`; the single option is a `tooltip = { }` repeat plus a
`custom_tooltip`, so it applies nothing new. No `add_base_tax`, `add_base_production` or
`add_devastation`. `flavor_geo.3` (98–150) does carry them —
`capital_scope = { add_base_tax = 2 add_base_production = 2 add_base_manpower = 1 }` plus
`466 = { add_devastation = 50 }` in option b. Outside `localisation/`, `flavor_geo.3` appears only in
its own definition and at `missions/KoK_Georgian_Missions.txt:2043` inside mission `geo_sack_sarai`
(`trigger = { controls = 466 }`). `on_startup` never fires it. Every clause holds.

## Y053 — add_base_* in a dated block before the start date accumulates: province 1 has base_tax 5 undated plus 1 at 1436.4.28 and the game has 6

**Status:** CONFIRMED (file value + save)
**Method.** Read `history/provinces/1-Uppland.txt` and the save's `-1={` record; then swept all 3,923
history files for pre-start dated `add_base_*` and compared the accumulate, overwrite and ignore
readings against the save.
**Evidence.** Uppland: undated `base_tax = 5`, `base_production = 5`; dated
`1436.4.28 = { revolt = {…} controller = REB add_base_tax = 1 }`; and a post-start
`1444.11.12 = { add_base_tax = 2 }` which is correctly ignored. The save gives `base_tax=6.000`, and
its own embedded `history={ base_tax=5.000 … 1444.11.11={ base_tax=6.000 } }` shows the engine
materialising the accumulation at the start date. Reading comparison: accumulate reproduces the save
on 1/1, overwrite 0/1, v5.0's ignore 0/1. Province 1 is the **only** province in the install with a
pre-start dated `add_base_*`, so the correction is worth exactly one province — but it is the province
that carries the model's maximum development (Y062, Y167).

## Y054 — is_city = yes is not a filter the engine applies: 20 owned provinces omit or comment out the line, province 265 among them, and the engine treats them as cities

**Status:** PARTIAL
**Method.** Listed the counted provinces without `is_city = yes` in force at 1444.11.11 and
classified each by *why*; checked the save's `is_city` for all 20.
**Evidence.** The count and the conclusion hold exactly: **20** provinces (265, 774, 857, 913, 958,
966, 1035, 1038, 1207, 2527, 2579, 2593, 2617, 2671, 2779, 2932, 4573, 4576, 4640, 4856), province
**265** among them and also one of the devastated eleven, and the save gives **all 20**
`is_city=yes`. But "omit or comment out" is a two-way split where the reality is three-way:
**1 commented out** (265, `265 - Brno.txt:13` `#is_city = yes`), **7 with no `is_city` text at all**
(913, 958, 966, 1207, 2579, 2932, 4856), and **12 that do carry `is_city = yes` but only in a
post-1444 dated block** (774 at 1596.1.1, 857 at 1583.1.1, 1035 at 1732.1.1, 1038 at 1768.1.1, 2527
at 1650.1.1, 2593 at 1732.1.1, 2617 at 1532.1.1, 2671 at 1650.1.1, 2779 at 1650.1.1, 4573 at
1530.1.1, 4576 at 1532.1.1, 4640 at 1532.1.1). Those 12 neither omit nor comment out the line.
**Should carry:** "20 owned provinces have no `is_city = yes` in force at the start date — one
commented out, seven absent, twelve dated after 1444 — and the engine treats them as cities."

## Y055 — the model counts a province when it has an owner and lies in a trade node: 2,472, not 2,452

**Status:** CONFIRMED (measurement)
**Method.** Counted twice, from history files + `00_tradenodes.txt` `members`, and from the save's
records + `members`, with an independent parser; then with the `is_city` test added.
**Evidence.** Both derivations give **2,472** with an empty symmetric difference. Adding the
`is_city = yes` test gives **2,452** — the 20 of Y054. 80 trade nodes, 3,369 distinct member
provinces.

## Y056 — twenty counted provinces have no trade good in history; the engine assigns one at start from each good's chance = { } block

**Status:** CONFIRMED (file value)
**Method.** Counted `trade_goods = unknown` over counted provinces; checked
`common/tradegoods/00_tradegoods.txt` for `chance` blocks.
**Evidence.** **20** counted provinces carry `unknown` (794 history files do overall, the rest being
unowned or outside a node). Of the 32 defined goods, **31** carry a `chance = { }` block — every good
except `unknown` itself, e.g. `fur`'s `chance = { factor = 15 modifier = { factor = 0 OR = {
has_climate = tropical … } } … }`. The mechanism the claim names exists.

## Y057 — the model reads the good the engine actually rolled, as it does for development

**Status:** CONFIRMED (stipulation, implemented)
**Method.** Read `solver.py`'s `_rolled_trade_goods()` and `province_table()`.
**Evidence.** `_rolled_trade_goods()` opens `save games/VANILLA_start.eu4`, unzips `gamestate`, walks
into `provinces={` and regex-reads `^\t\ttrade_goods="?([a-z_]+)` at two-tab depth per record;
`province_table()` substitutes `ROLLED[pid]` when history gives `None` or `unknown`. It predicts
nothing; it reads the state. Symmetric with reading `base_tax` from the same source.

## Y058 — pricing those twenty at zero instead understates world wealth by 12.70 ducats

**Status:** CONFIRMED (measurement)
**Method.** Summed the production income of the 20 rolled provinces.
**Evidence.** **12.70** ducats. 10,607.40 − 12.70 = 10,594.70, which is exactly the world wealth
`changes-v6.md` records for the pre-round-2 field — a consistent cross-check.

## Y059 — on this save the twenty came up seven fur, five grain, three wool, two livestock, and one each of cotton, incense and naval_supplies

**Status:** CONFIRMED (save value; single observation as the § marker says)
**Method.** Tallied the save's goods for exactly those 20 provinces.
**Evidence.** fur 7 (966, 2503, 2510, 2571, 2593, 2671, 4901), grain 5 (897, 907, 2596, 2669, 4923),
wool 3 (774, 862, 2932), livestock 2 (1809, 4902), cotton 1 (2014), incense 1 (4856),
naval_supplies 1 (895). Sums to 20; exact dict match. This is one draw and cannot be reproduced by a
different game start, which the § marker records correctly.

## Y060 — a different roll gives a slightly different field, and nothing in the model depends on which one

**Status:** CONFIRMED (measurement supporting the structural reading)
**Method.** Re-priced all 20 rolled provinces to each of five uniform goods (grain, fur, cloves, coal,
gold) and recomputed the `Φ_w` sink set and the edge orientation.
**Evidence.** World wealth moves over 10,594.70–10,650.70 and the sink set is
`{english_channel, hangzhou}` in **every** case, with 0, 0, 4, 4 and 0 edge flips respectively. So no
rule and no structural property of the model depends on the draw, which is what the claim means. The
field itself does move — 12.70 ducats against the zero-priced baseline and up to 4 edge flips under an
extreme uniform reroll — which the sentence's first half already concedes.

## Y061 — TAX_COEFF = 1.0's reference condition is applied to every province the model counts; ownership is not modelled

**Status:** CONFIRMED (derivation, implemented)
**Method.** Read `solver.py` for any core/autonomy/settlement term.
**Evidence.** `tax = TAX_COEFF * base_tax * (1 + tmod)` with `tmod = 0.0` for all 2,472 provinces.
No `Core`, `City`, autonomy or coring term exists anywhere in the wealth path, so every province is
treated as cored and settled, uniformly. §1.3's justification (75 + 25 = 100% is exactly the 1.0
reference) is arithmetically consistent with the Garnatah/Caceres itemisations it quotes.

## Y062 — base_tax at 1444 runs up to 33

**Status:** REFUTED
**Method.** Took the maximum `base_tax` over counted provinces from `prov1444.json`, from the history
files under the accumulate reading, and from the save independently.
**Evidence.** All three agree: maximum `base_tax` = **15**, at province **1821** (Nanjing). Top six:
1821 → 15, 1816 (Beijing) → 13, 667 (Canton) → 12, 684 (Hangzhou) → 12, 685 (Yangzhou) → 12, 101
(Genova) → 10. **33** is the maximum *total development* — 1821's 15 tax + 15 production + 3 manpower
= 33 (runner-up 1816 at 31, then 116 Firenze at 28). The claim conflates the two, and it matters,
because the sentence's whole point is the distance between the two readings the coefficient rests on
(`base_tax` 2 and 6) and the top of the range: the honest gap is 2–6 against 15, not against 33.
**Should carry:** "`base_tax` at 1444 runs up to 15, and total development to 33."

## Y063 — owner-agnosticism removes a large source of hidden owner-dependence from the aggregate graph

**Status:** CONFIRMED (derivation)
**Method.** Traced every input to `Φ_w`.
**Evidence.** `Φ_w = DRAIN(1/N − c_w)` with `c_w = Σ wealth^α_Φ / Σ wealth^α_Φ`, and `wealth` reads
only `base_tax`, `base_production`, `price(good)` and the devastation level. No owner field reaches
the aggregate at all, so the owner-dependence is not reduced but eliminated — the claim is
directional and weaker than what holds. Correctly hedged ("a large source" rather than a figure).

# §1.5 — Goods without a graph

## Y064 — repricing the 45 owned latent-coal provinces flips 10 of 159 Φ_w edges and adds 214.60 ducats

**Status:** CONFIRMED (measurement)
**Method.** Independently re-derived the latent-coal set from `history/provinces/*.txt`
(`latent_trade_goods` blocks containing `coal`), intersected with the counted set, re-priced holding
devastation fixed, and counted edges whose direction differs.
**Evidence.** **58** latent-coal provinces in the install, **45** owned and counted; the 13 excluded
(621, 940, 951, 972, 982, 1039, 2023, 2549, 2732, 2806, 2856, 2887, 4857) are all in a trade node
with no owner at 1444. Save cross-check: 58 records with a coal latent block, 45 counted, symmetric
difference empty. Wealth delta **+214.60**; edges with a different direction **10** of 159. Both
figures exact.

## Y065 — the counterfactual holds every non-repriced input fixed: province 4237 is both latent-coal and devastated, worth 2.40 ducats and 3 extra flips

**Status:** CONFIRMED (measurement)
**Method.** Ran the contaminated variant (dropping devastation on the repriced provinces) beside the
clean one.
**Evidence.** 4237 is in both sets (save devastation 20.000), and it is the *only* overlap. Clean:
+214.60, 10 flips. Contaminated: +217.00, 13 flips — a difference of exactly **2.40** ducats and
**3** flips. The arithmetic also closes analytically: 0.2 × 3 × 10 × (1 − 0.6) = 2.40.

## Y066 — coal's base price of 10.0 is the highest in the shipped price table

**Status:** CONFIRMED (file value)
**Method.** Read every `base_price` in `common/prices/00_prices.txt`.
**Evidence.** coal 10 (written `10`, value 10.0), cloves 8, then a five-way tie at 4 (cocoa, dyes,
gems, ivory, silk), paper 3.5, eleven goods at 3, five at 2.5, six at 2, and gold and unknown at 0.
Coal is the maximum, and the claim is correctly scoped to the shipped table rather than asserted as a
fact about the world.

# §1.6 — The aggregate graph

## Y067 — both the sink count and the sink locations move with the wealth field, and α_Φ sets how sharply concentration is read

**Status:** CONFIRMED (measurement)
**Method.** Two sweeps: α_Φ held at 1.5 with the European field scaled (count and locations both
move), and the field held fixed with α_Φ swept over [1, 8] at 0.01.
**Evidence.** At fixed α_Φ = 1.5 the sink set takes at least twelve distinct values as Europe grows
from ×1.00 to ×2.00, with counts 2, 3, 4, 5, 3, 2, 1. At fixed field the α_Φ scan yields **9**
distinct sink sets with counts spanning **1 to 6**. Both halves hold.

## Y068 — at α_Φ = 1.5 the 1444 field gives two sinks and a modestly grown Europe gives three or one

**Status:** CONFIRMED (measurement)
**Method.** Re-ran the Europe-scaling table.
**Evidence.** ×1.00 → `{english_channel, hangzhou}` (two); ×1.02 → `{english_channel, hangzhou,
wien}` (three); ×2.00 → `{genua}` (one). Neither the count nor the placement is fixed by the
constant, which is the point being made.

## Y069 — v2.0–v4.0's "emerges from concentration" and v5.0's "the count is set by α_Φ" are wrong the same way

**Status:** CONFIRMED
**Method.** Grepped v2, v3, v4 and v5 for both phrasings; then tested the joint dependence.
**Evidence.** Identical sentence at `v2:154-155`, `v3:257-258`, `v4:306-307`: "Nothing pins their
count; it emerges from concentration exactly as per-good sink counts do." v5.0's replacement at
`v5:342-345`: "**Their count is set by `α_Φ`**; only their locations are emergent." Y067 shows the
count moves with the field at fixed α_Φ *and* with α_Φ at fixed field, so it is a function of both and
each prior formulation drops one argument.

## Y070 — v2.1 chose α_Φ with a target count in view — a calibration §2.3 withdraws without replacing

**Status:** CONFIRMED
**Method.** Grepped v2/v3/v4 §2.3 for the α_Φ justification; read v6.0 §2.3.
**Evidence.** Identical text at `v2:372-373`, `v3:558-559`, `v4:632-633`: "the aggregate-graph
exponent `α_Φ = 1.5` (**calibrated so the 1444 start yields the two-sink hangzhou/english_channel
map**, §1.6 …)". v6.0 §2.3 states "**Every derivation previously offered for it is withdrawn**" and
offers none in its place — the withdrawal is real and it is unreplaced.

## Y071 — scaling b down: identical orientation at ×1 and above, 12 flips at ×10⁻², 100 at ×10⁻⁶ where the sink set collapses to {genua}

**Status:** CONFIRMED (measurement)
**Method.** Multiplied `b_w` by 1, 10, 1e-2 and 1e-6 and recounted flips and sinks against the ×1
orientation.
**Evidence.** ×1: 0 flips. ×10: **0** flips (identical at and above ×1). ×1e-2: **12** flips, sink set
unchanged. ×1e-6: **100** flips and the sink set collapses to **{genua}**. Every figure exact, and the
mechanism the spec gives (an absolute 1e-11 zero-flow tolerance) is the right one.

## Y072 — 1444's b_w has largest magnitude 0.0225

**Status:** CONFIRMED (measurement)
**Method.** `max |1/N − c_w|` at α_Φ = 1.5.
**Evidence.** 0.022531 → **0.0225**.

## Y073 — two sinks, english_channel and hangzhou; c_w ranks 2 and 3, node-wealth ranks 1 and 12

**Status:** CONFIRMED (measurement)
**Method.** Re-ran DRAIN on `b_w`; ranked nodes by `c_w` and by raw node wealth.
**Evidence.** Sinks `['english_channel', 'hangzhou']`. `english_channel`: `c_w` rank 2, node-wealth
rank 1. `hangzhou`: `c_w` rank 3, node-wealth rank 12. Exactly as stated.
*Conditional on the node order:* Y124 measures this exact set returning in only 6 of 100
relabellings, with `hangzhou` stable at 97–98% and `english_channel` at 38–45%. The figures here
are correct for the order the emitter fixes; the European member of the pair is not order-robust.

## Y074 — Phase 1 selects genua; both sinks arrive by stall promotion and genua ends a transit node: 2 promotions, 0 fallbacks

**Status:** CONFIRMED (measurement)
**Method.** Read `S0`, `promotions` and `fallbacks` off the run and checked `genua`'s out-degree.
**Evidence.** `S0 = ['genua']`, `promotions = ['english_channel', 'hangzhou']`, `fallbacks = []`.
`genua` is not in the sink set, so it ends a transit node. 2 promotions, 0 fallbacks.

## Y075 — eight sources, all in the bottom half of the wealth field, c_w ranks 44–75, mean degree 3.1 against the map's 4.0

**Status:** CONFIRMED (measurement)
**Method.** Counted in-degree-zero nodes and their `c_w` ranks and degrees.
**Evidence.** **8** sources; `c_w` rank range **44–75** (all above 40 of 80, so all in the bottom
half); mean degree **3.1** against the map mean **4.0**. Reproduces `measure6.py` exactly.

## Y076 — every node drains to a sink; acyclic, 159/159 oriented; sink set unchanged under ±1% wealth noise on three seeds

**Status:** CONFIRMED (measurement)
**Method.** Reverse-reachability from the sink set over all 80 nodes; cycle check; edge count;
three ±1% uniform noise seeds.
**Evidence.** Nodes reaching no sink: **none**. Acyclic: True. Oriented **159/159**. Sink set
`{english_channel, hangzhou}` on all three seeds. All four sub-claims hold.

## Y077 — 89.6% of ordered node pairs (5,663 of 6,320) are connected by at least one good's directed path

**Status:** CONFIRMED (measurement)
**Method.** 29 goods × 80 forward BFS, union over goods, counted ordered pairs.
**Evidence.** **5,663 of 6,320 = 89.60%**. Reproduces `measure6.py`. Note this is the corrected
figure: `verify6.py`'s `every_site` check confirms both spec sites carry 5,663, and the checklist
`fixes-agreed.md` still carries the stale 5,703.

## Y078 — agreement with the per-good graphs is 53.6% of edge-goods, 52.3% value-weighted

**Status:** CONFIRMED (measurement)
**Method.** For each good and each edge that good orients, compared the direction to `Φ_w`'s, both
unweighted and weighted by the good's world trade value.
**Evidence.** **53.63%** edge-goods, **52.26%** value-weighted → 53.6% and 52.3%.

## Y079 — the superseded marking-order aggregate scored higher on that measure, and no figure is maintained for it

**Status:** CONFIRMED (measurement of the direction; the no-figure half checked by reading)
**Method.** Built `Φ_ord = Σ_g V_g · order_g` on the v6 field, oriented by descending `Φ_ord`, and
scored it against the same per-good graphs; then checked §1.6 and §3.9 for a maintained figure.
**Evidence.** `Φ_ord` scores **60.4%** edge-goods and **60.1%** value-weighted against `Φ_w`'s
53.6%/52.3% — higher on both, so the direction holds. Neither §1.6 nor §3.9 quotes a number for it.

## Y080 — α_Φ = 1.5 is a stipulated design constant, exactly as P₀ = 2.0 is: superlinear and round

**Status:** CONFIRMED (stipulation)
**Method.** Read §1.6 and §2.3; checked the stated rationale against the mechanism.
**Evidence.** Both sections call it stipulated and pair it with `P₀`. The rationale is internally
coherent: `α_Φ > 1` makes `Σ wealth^α_Φ` favour a few rich provinces over a dense mediocre region,
which is measurably true (at α_Φ = 1 the sink count is 6; at 1.5 it is 2), and 1.5 is round. Nothing
about the choice is presented as derived.

## Y081 — it is not derived, and both derivations previously offered are withdrawn

**Status:** CONFIRMED
**Method.** Located both prior derivations and confirmed the withdrawal text.
**Evidence.** The v2.1–v4.0 calibration is quoted verbatim in Y070. v5.0's widest-band argument is at
`v5:379-395`: a four-row band table over "α_Φ = 1.00…3.00 at 0.01" with `[1.43, 1.93]` marked
"**the widest band on this field, and the one α_Φ = 1.5 sits in**", and "`α_Φ` is **retained at 1.5**
because it sits inside the widest band". v6.0 §1.6 and §2.3 both withdraw both. No replacement
derivation is offered anywhere in v6.0.

## Y082 — scanned over [1, 8] rather than [1, 3] the widest band is 1.71 wide ([3.50, 5.21], {doab, genua, hangzhou})

**Status:** CONFIRMED (measurement)
**Method.** Swept α_Φ = 1.00…8.00 at 0.01, segmented into maximal constant-sink-set bands, took the
widest.
**Evidence.** Widest band = `{doab, genua, hangzhou}` on **[3.50, 5.21]**, width **1.71**. And v5.0's
scan really did stop at 3.00 (Y081's quote). 1.5's band (0.25) is not the widest by any margin.

## Y083 — across α_Φ = 1.00…8.00 at 0.01 the sink set is a step function, and 1.5 sits in [1.38, 1.63], width 0.25, giving {english_channel, hangzhou}

**Status:** CONFIRMED (measurement)
**Method.** Same sweep.
**Evidence.** The band containing 1.5 is `('english_channel', 'hangzhou')` on **[1.38, 1.63]**, width
**0.25**. Nine distinct sink sets over the whole scan, so the step-function description is right.

## Y084 — sampled at the six values v2 used the count is non-monotone: 6 → 2 → 1 → 2 → 3 → 1

**Status:** CONFIRMED (measurement)
**Method.** Evaluated the sink count at α_Φ ∈ {1, 1.5, 2, 3, 4, 8}.
**Evidence.** **[6, 2, 1, 2, 3, 1]** exactly.

## Y085 — a standing warning: 1.5 must not be justified by the two-ends resemblance to vanilla's three

**Status:** CONFIRMED (stipulation)
**Method.** Read §1.6's warning paragraph and cross-checked the two counts.
**Evidence.** 1444 has two ends (Y073) and the shipped `00_tradenodes.txt` has three (Y129), so the
resemblance the warning guards against is real and the temptation is live. The warning is internally
consistent with §2.3's withdrawal and with §3.9's stated adoption argument, which does not use the
count.

## Y086 — Europe becomes the centre of trade as it develops: the design claim, and what §3.1's first goal asks for

**Status:** CONFIRMED (stipulation)
**Method.** Read §3.1 goal 1 and §1.6's Europe paragraph.
**Evidence.** Goal 1 is "World responsiveness. Trade direction follows the world's current state,
never authored arrows." The Europe claim is the same property instantiated: the mechanism (Y088) is
that wealth is linear in development, so a developing region moves its `c_w` share and the ends
follow. Stated as a design claim, not as a measurement.

## Y087 — at 1444 the map ends in the Channel and Hangzhou; as Europe compounds the Channel's basin grows and Asia's pole fades, and past a broad range Asia holds no end

**Status:** PARTIAL
**Method.** Scaled European development in steps from ×1.00 to ×2.00 and measured, at each step, the
sink set and the *basin* (count of nodes that can reach the sink) of `english_channel` and
`hangzhou`.
**Evidence.** Asia's pole fades unambiguously: `hangzhou` basin 78 → 61 → 60 → 33 → 22 → 17 → gone,
and no Asian node holds an end from ×1.56 through ×2.00 — so "past a broad range of European growth
Asia holds no end at all" holds. The Channel's basin grows 18 → 18 → 19 → 21 → 23 → **28** at ×1.44,
then **shrinks to 26** at ×1.56 and the Channel stops being an end entirely at ×1.64, where `genua`
becomes the sole sink. So "the Channel's basin grows" is true over ×1.00–×1.44 and false past it.
**Should carry:** "the Channel's basin grows through about ×1.44 and Asia's pole fades throughout;
past roughly ×1.6 the map concentrates on a single Mediterranean end instead."

## Y088 — the mechanism: wealth is linear in development, so developing a region moves its c_w share directly and Φ_w's ends follow the wealth

**Status:** CONFIRMED (derivation, measured)
**Method.** Checked linearity in the wealth expression and measured it.
**Evidence.** `wealth = TAX_COEFF·base_tax + GP_COEFF·base_production·(1+gmod)·price` is linear and
homogeneous of degree 1 in (`base_tax`, `base_production`) with the flat terms gone, so scaling
development by `k` scales wealth by `k` exactly — measured max difference **0.0** across the 824
European provinces (Y092). `c_w` is a normalised `Σ wealth^α_Φ`, so it moves directly with it.

## Y089 — Europe-scaling on 824 counted European provinces: ×1.00 {english_channel, hangzhou}; ×1.02 adds wien; ×1.56 {english_channel, rheinland}; ×2.00 genua alone

**Status:** CONFIRMED (measurement)
**Method.** Derived the European province set from `map/continent.txt`'s `europe` list intersected
with the counted set, then re-ran each row.
**Evidence.** **824** counted European provinces (849 ids in the list, 838 in a trade node, 824
owned; identical using save-derived ownership). ×1.00 → `['english_channel', 'hangzhou']`; ×1.02 →
`['english_channel', 'hangzhou', 'wien']`; ×1.56 → `['english_channel', 'rheinland']`; ×2.00 →
`['genua']`. All four rows exact.

## Y090 — read as a direction: the Channel holds an end throughout, Asia loses its own between ×1.02 and ×1.56, by ×2.00 a single Mediterranean end

**Status:** PARTIAL
**Method.** Same scan as Y087, at 0.02 resolution.
**Evidence.** "Asia loses its own between ×1.02 and ×1.56" holds — hangzhou is still a sink at ×1.44
and gone by ×1.56. "By ×2.00 there is a single Mediterranean end" holds — `{genua}` from ×1.64. But
"**the Channel holds an end throughout**" is false at ×2.00, the table's own last row, where the sole
sink is `genua` and `english_channel` is not a sink at all. The sentence contradicts its own closing
clause.
**Should carry:** "the Channel holds an end until Europe outgrows it, Asia loses its own between
×1.02 and ×1.56, and by ×2.00 there is a single Mediterranean end."

## Y091 — these are properties of this snapshot, not constants of the model

**Status:** CONFIRMED (stipulation)
**Method.** Checked whether the figures are field-dependent.
**Evidence.** They are: the same table on the v5 field gave `{doab, english_channel, hangzhou, wien}`
at ×1.02 rather than three sinks, and Y124 shows the ×1.00 row itself moving under node relabelling
alone. The hedge is not merely prudent, it is required.

## Y092 — scaling development and scaling wealth are the same operation here — maximum difference 0.0 across the European set

**Status:** CONFIRMED (measurement)
**Method.** Built the field two ways (multiply the wealth vector; multiply development and recompute)
and took the max absolute difference over the 824 provinces.
**Evidence.** **0.0** exactly. And the reason v5.0's version was wrong is verifiable: v5's production
term was `(GP_COEFF·base_production + flat)·…`, and the additive `trade_goods_size` flats on 15
provinces do not scale with development, so wealth was not homogeneous in development there.
`europe.py` is byte-identical between v5 and v6 and scales *wealth*, with a docstring that says
development — under (c) the two coincide, which is exactly what the claim says.

## Y093 — all three institutions the period is named for begin in Europe between 1450 and 1550

**Status:** CONFIRMED (file value)
**Method.** Read `common/institutions/00_Core.txt` in full and cross-checked the three provinces
against `map/continent.txt`'s `europe` list.
**Evidence.** `renaissance` `historical_start_date = 1450.1.1`, `historical_start_province = 116`
(Firenze); `new_world_i` `1500.1.1`, `224` (Andalucia, commented "Sevilla"); `printing_press`
`1550.1.1`, `1876` (Frankfurt). All three ids are in the `europe` list. Eight institutions in the
file; the other five are `feudalism` (no start date), `global_trade` 1600 at 97, `manufactories` 1650
at 183, `enlightenment` 1700 at 236, `industrialization` 1750 at 244 — so **no** institution begins
in 1450–1550 outside Europe, and none begins in that window at all besides these three. Independent
of any threshold, as claimed.

## Y094 — the Renaissance's embracement bonus is development_cost = -0.05, a standing discount on every subsequent development point

**Status:** CONFIRMED (file value)
**Method.** Read the `renaissance` block.
**Evidence.** Lines 276–283: `bonus = { development_cost = -0.05  build_cost = -0.05 }`. The claimed
key and value are exact. Two notes that do not affect the verdict: the key is `bonus`, not
`on_embracement`, and `build_cost = -0.05` sits alongside it (the claim does not say "only").

## Y095 — the 1444 Silk Road route from Genoa runs … lahore → lhasa → ganges_delta …

**Status:** CONFIRMED (measurement)
**Method.** BFS on the `Φ_w` orientation from `genua` to `hangzhou`.
**Evidence.** `genua → alexandria → aleppo → persia → lahore → lhasa → ganges_delta → burma →
gulf_of_siam → canton → hangzhou` — eleven nodes, `lhasa` where v5.0 had `doab`. Exact.

## Y096 — no route leaves english_channel at all: it is a sink with out-degree 0, so the Hansa and the Danube carry power into it

**Status:** CONFIRMED (measurement + document check)
**Method.** Counted `english_channel`'s in- and out-degree in `Φ_w`; grepped v5.0 for the Hansa
sentence.
**Evidence.** out-degree **0**, in-degree **5**. v5.0 line 424–426 reads verbatim: "From the Channel
it is the Hansa and the Danube: `english_channel → lubeck → saxony → wien → venice → ragusa →
constantinople → aleppo → …`" — a path that cannot exist out of a node with out-degree 0. Both halves
hold.

## Y097 — no Europe→sink route passes the Cape of Good Hope, checked from genua, north_sea and english_channel

**Status:** CONFIRMED (measurement, and stronger than stated)
**Method.** For each of the three origins and each of the two sinks, took the BFS route and then
tested the stronger property: is the Cape reachable from the origin *and* is the sink reachable from
the Cape?
**Evidence.** For all six (origin, sink) pairs the "any path via the Cape" test is **False** — so it
is not merely that the shortest route avoids the Cape, but that no path through it exists. Routes:
`genua → … → hangzhou` via `lhasa`; `north_sea → white_sea → novgorod → kazan → astrakhan → persia →
lahore → lhasa → … → hangzhou`; `north_sea → english_channel`; and no route at all from `genua` or
`english_channel` to the other sink. Note that `measure6.py` only checks routes *to hangzhou*; the
routes to `english_channel` are checked here for the first time and also hold.

## Y098 — the Cape is a live conduit: in-degree 1, out-degree 3, with 132 ordered node pairs whose path runs through it

**Status:** CONFIRMED (measurement)
**Method.** Counted the Cape's degrees; counted ordered pairs (a, b) with `cape ∈ reach(a)`,
`b ∈ reach(cape)` and `b ∈ reach(a)`.
**Evidence.** in-degree **1** (`ivory_coast`), out-degree **3** (`comorin_cape`, `malacca`,
`zanzibar`), **132** ordered pairs. Atlantic drainage into the Indian Ocean, as described.

## Y099 — v5.0's "nothing routes through the Cape" is false as a universal and was only ever checked on the Europe→sink routes

**Status:** CONFIRMED
**Method.** Grepped v5.0 for the sentence; compared its scope to Y098's measurement.
**Evidence.** `v5:426-427`: "**Nothing routes through the Cape**, which is what a 1444 map should
say." — an unscoped universal, immediately followed by a parenthetical conceding the Cape is not idle
in the per-good graphs. 132 ordered pairs route through it in `Φ_w` on this field, so the universal is
false, and the only thing v5.0's own text supports is the Europe→sink statement.

## Y100 — in the per-good graphs the Cape also carries Asian spices to Europe; Φ_w models power, not cargo

**Status:** CONFIRMED (measurement)
**Method.** BFS on the spices graph from `malacca` to `genua`; counted the Cape's spices degrees.
**Evidence.** `malacca → cape_of_good_hope → zanzibar → gulf_of_aden → alexandria → genua`; Cape
spices in-degree 1, out-degree 3; spices sinks `{australia, brazil, genua}`. The generic claim holds
and the specific route v5.0 named is (as the parenthetical says) not asserted.

## Y101 — scaling the 22 European nodes makes genua the sole sink from about ×1.65, and the 18-node subset needs about ×2.15

**Status:** CONFIRMED (measurement)
**Method.** Scaled the wealth of every counted province in each node set in 0.05 steps and found the
first factor at which `{genua}` is the whole sink set.
**Evidence.** 22-node set: `genua` sole sink from **×1.65**. 18-node western/central subset:
**×2.15**. Both "about" figures land on the measured step exactly.

## Y102 — somewhere inside roughly ×2.9–×3.5 the Cape reverses, and the reversal is bounded above as well as below

**Status:** CONFIRMED (measurement)
**Method.** Scaled the 22 European nodes from ×2.50 to ×4.50 in 0.02 steps, recording the Cape's
in- and out-neighbour sets.
**Evidence.** Baseline ×1.00: in `{ivory_coast}`, out `{comorin_cape, malacca, zanzibar}`. The full
reversal (in `{comorin_cape, malacca, zanzibar}`, out `{ivory_coast}`) holds on a **contiguous**
interval **×2.90 to ×3.42** and on no step outside it — at ×2.88 and at ×3.44 the state is in
`{malacca}`, out `{comorin_cape, ivory_coast, zanzibar}`. So it is a window, bounded both ways, and it
sits inside "roughly ×2.9–×3.5".

## Y103 — dev-stacking a single node's top province concentrates the map on that node

**Status:** CONFIRMED (measurement)
**Method.** Scaled the single richest counted province of `hangzhou` and of `champagne` by ×10, ×20,
×30, ×50.
**Evidence.** `hangzhou`: ×10 → `{genua, gulf_of_siam, hangzhou}`, ×20/×30/×50 → `{hangzhou}` alone.
`champagne`: ×10 → `{genua, gulf_of_siam, hangzhou}`, ×20 → four sinks including `champagne`,
×30/×50 → `{champagne}` alone. The directional claim holds for two different nodes, and the
"extra sinks at intermediate boosts" note is visible at ×10 and ×20.

# §1.10 — Direction-dependent systems

## Y104 — banding absorbs very little chatter, narrower than v5.0's "almost nothing", because the cooldowns absorb some

**Status:** CONFIRMED (derivation)
**Method.** Read §1.10's threshold table and the banding paragraph; confirmed the v5.0 phrasing is
gone (`verify6.py` asserts the absence of "So almost nothing absorbs threshold chatter" and it
passes).
**Evidence.** Of the seven listed thresholds only Improve Inland Routes is banded unconditionally and
Propagate Religion is banded only on its flag ladder, so banding itself absorbs little; and the
cooldown defines of Y105 do absorb some, which is what makes the weaker phrasing the right one. The
retreat from an absolute to "very little" is exactly the move the R2 convention asks for.

## Y105 — TRADING_POLICY_COOLDOWN_MONTHS = 12 applies to seven of the nine entries in 00_trading_policies.txt; TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30 pairs with TRADE_COMPANY_COOLDOWN = 60

**Status:** PARTIAL
**Method.** Enumerated every top-level entry in `common/trading_policies/00_trading_policies.txt`,
grepped it for `cooldown`, read the three defines in `common/defines.lua`, and looked for any file
statement of the `cooldown` key's semantics.
**Evidence.** The file structure is exactly as claimed: **nine** entries — `maximize_profit` (3),
`maximize_profit_upgraded` (29), `hostile_trading` (55), `hostile_trading_upgraded` (78),
`improve_inland_routes` (101), `improve_inland_routes_upgraded` (146), `establish_communities` (192),
`establish_communities_upgraded` (218), `propagate_religion` (239) — i.e. five families, four with an
`_upgraded` twin plus Propagate Religion with none. `grep -n cooldown` returns exactly two hits,
lines 25 and 52, both `cooldown = no`, both on the `maximize_profit` pair. Defines confirmed:
`TRADING_POLICY_COOLDOWN_MONTHS = 12` (1045, comment "Cooldown until you can change Trading Policy
after selecting"), `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` (1212), `TRADE_COMPANY_COOLDOWN = 60`
(1214). What is **not** file-established is the inference: nothing in the install documents
`cooldown = no` as the opt-out, states a default, or links the key to the define. The circumstantial
support is the define's comment plus `TRADING_POLICY_IN_COOLDOWN` and a `$MONTHS$` localisation token
— a runtime substitution, not a per-policy mapping.
**Should carry:** "carries `cooldown = no` on two of the nine entries, and on the reading that
`cooldown = no` is the opt-out the 12-month define rate-limits the other seven" — the arithmetic is
an inference and the claim's ⚑ engine-fact marker over-states its provenance.

## Y106 — a flickering share does not translate into a flickering effect at those three; what is left exposed is most of the ladder

**Status:** PARTIAL
**Method.** Mapped each of §1.10's seven listed thresholds onto the three defines.
**Evidence.** Improve Inland Routes and Propagate Religion are trading policies, so both are covered
under Y105's reading — 2 of 7. The two trade-company rows (`TRADE_COMPANY_STRONG_LIMIT`,
`TRADE_COMPANY_CONTROL_LIMIT`) are the ones the trade-company defines would have to cover, but
`TRADE_COMPANY_DAYS_TO_SWAP_LEADER` is by its own name a *leader-swap* cooldown, and no file ties
either define to those two limits. On the reading that they are covered, 4 of 7 are damped and only 3
are exposed — **not** "most of the ladder"; on the reading that they are not, 5 of 7 are exposed and
the claim holds. The claim picks the second reading without saying so, and the files do not settle it.
**Should carry:** either name which mechanics the trade-company defines gate, or weaken to "much of
the ladder is left exposed, and which of the trade-company thresholds the trade-company cooldowns
cover is not settled from files."

## Y107 — the caravan cap of 50 is 9.4% to 47.0% of an inland node's total trade power, median 21.6% over the flag's 26 inland nodes, totals 106.4 at xian to 532.0 at champagne

**Status:** CONFIRMED (measurement)
**Method.** Parsed the save's `trade={ node={ … } }` block for each node's `total` and its country
sub-blocks' `val`; took the flag's inland set from `00_tradenodes.txt`.
**Evidence.** 26 flag-inland nodes. `50/total`: **9.4% to 47.0%**, median **21.6%**. Totals run
**106.4 at `xian`** to **532.0 at `champagne`**. Every figure exact.

## Y108 — as a share of the node's total after the grant lands the same figures read 8.6% to 32.0%, median 17.7%

**Status:** CONFIRMED (measurement)
**Method.** Same table, `50/(total+50)`.
**Evidence.** **8.6% to 32.0%**, median **17.7%**. Exact.

## Y109 — v5.0 quoted the after-grant figures under the before-grant description, which cannot be right: 8.6% of 532.0 is 45.8 rather than 50

**Status:** CONFIRMED
**Method.** Read v5.0's sentence; checked the arithmetic.
**Evidence.** `v5:553-554` verbatim: "the cap of 50 is **8.6% to 32.0% of an inland node's total
trade power** (median 17.9% over the **flag's** 26 inland nodes, whose totals run 106.4 at `xian` to
532.0 at `champagne` …)" — after-grant percentages, before-grant description, before-grant totals, one
sentence. 0.086 × 532.0 = **45.752**, i.e. 45.8, not 50. The contradiction is internal to v5.0 and the
arithmetic in v6.0's rebuttal is right (v5.0's own audit rounded it 45.7).

## Y110 — on §2.2's derived 25-node inland basis the median is 21.3%, or 17.5% after the grant

**Status:** CONFIRMED (measurement)
**Method.** Derived the inland set as "no coastal province among `members`" (`coastal.json`) and
recomputed.
**Evidence.** The derived set is **25** nodes, differing from the flag's 26 by `siberia` alone — the
one node §2.2 names. On that basis: median **21.3%** before the grant, **17.5%** after. Range,
largest-holder span (23.6–143.2) and the 7-of-N count are unchanged.

# §2.2 — Solver

## Y111 — solver item 4 computes TAX_COEFF·base_tax·(1+tax mods) + GP_COEFF·base_production·(1+goods mods)·price, with no autonomy, efficiency, ideas or owner terms

**Status:** CONFIRMED (stipulation matching the implementation)
**Method.** Compared §2.2 item 4 to `solver.py`'s `province_table()`.
**Evidence.** Term for term identical. No autonomy, production-efficiency, national-idea, estate,
government or technology term appears anywhere in the wealth path.

## Y112 — the only modifiers the solver reads are the four describing the province's own condition, and at 1444 only devastation is live, on eleven provinces

**Status:** CONFIRMED
**Method.** Read `STATE_GOODS_MOD`, `STATE_TAX_MOD` and their use sites; counted devastated counted
provinces.
**Evidence.** The four modifiers are declared; the only one with a live use site is
`STATE_GOODS_MOD["devastation"]`, applied through `ON_STARTUP_DEVASTATION` on exactly **11**
provinces, with `tmod = 0.0` everywhere. `prosperity`, `under_siege` and `occupied` are declared and
unexercised, which is the correct state for a 1444 start where no province is prosperous, besieged or
occupied.

## Y113 — world wealth is 10,607.40 annual ducats over 2,472 counted provinces

**Status:** CONFIRMED (measurement)
**Method.** Summed the field; counted rows.
**Evidence.** **10,607.40** over **2,472**. Reproduces `measure6.py`, and the count is independently
confirmed from both the history files and the save (Y055).

## Y114 — of order 0.1 s for all 29 goods, and single-digit milliseconds per good on average, and that is the whole of the claim

**Status:** CONFIRMED (measurement)
**Method.** Three replicates of twelve all-29-goods runs on this machine (Python 3.12.10, numpy
2.4.6, scipy 1.18.0), after a warm-up solve.
**Evidence.** All-29 totals spanned 0.100–0.296 s across the three replicates; per-good averages
spanned 3.4–10.2 ms. "Of order 0.1 s" and "single-digit milliseconds per good on average" both hold,
and the deliberate refusal to quote anything finer is vindicated by the spread.

## Y115 — three replicates gave per-good averages spanning 3.5–10.5, 3.5–10.8 and 3.1–4.7 ms, so no range is quoted

**Status:** PARTIAL
**Method.** Ran the same experiment shape: three replicates of twelve runs.
**Evidence.** My replicates gave **3.5–10.2**, **4.1–6.1** and **3.4–4.1** ms. The order of magnitude
and the argument reproduce — replicates genuinely do not reproduce each other, and the spread swamps
any range one might quote — but the three specific spans do not, and by the claim's own reasoning
they cannot: what is being measured is a machine and a scheduler. Quoting three exact spans as
evidence that exact spans are meaningless is self-undermining.
**Should carry:** the argument without the three spans, or the spans explicitly labelled
non-reproducible ("one session's replicates gave …").

## Y116 — of v5.0's "0.17–0.21 s for all 29 goods": across three replicates of twelve runs the number landing inside was 1, then 0, then 0

**Status:** PARTIAL
**Method.** Verified v5.0's quote; then counted, in each of my three replicates, the runs whose
all-29 total fell in [0.17, 0.21] s.
**Evidence.** v5.0's quote is verbatim and singular: `v5:642-646` "**0.17–0.21 s for all 29 goods, a
mean of 5.7–7.3 ms per good across runs**". My per-replicate counts inside the interval were **0, 1,
0** rather than 1, 0, 0. The substance — almost no run lands inside v5.0's interval — reproduces
robustly (1 of 36 here, 1 of 36 in the claim); the exact sequence does not, for the same reason
Y115 gives.
**Should carry:** "across three replicates of twelve runs, one of the thirty-six landed inside that
interval", which is reproducible in form if not in position.

## Y117 — where Phase 0 acts, free-edge determinism survives but index-independence does not

**Status:** CONFIRMED (derivation)
**Method.** Traced the priority key's inputs in `drain.py`; checked what the 1444 measurement
actually covers.
**Evidence.** `run_drain` computes `core, beta, Plog = phase0(b)` and then
`sweep_priority(core, beta, …)`, whose key is `(DEF[v], beta[v], pid[v])` with `DEF` built by
`flow_def(core, beta, flow_arc)`. Both key components read the **post-fold** `beta`, so peeling can
create exact `(DEF, β)` ties the raw balances do not have — determinism is unaffected (the key is
still a function of the folded input) but index-independence is not. And the 1444 measurement cannot
transfer: Phase 0 is a no-op there (`core` = 80 of 80 on all 29 goods, Y018), so it observes nothing
about maps where Phase 0 acts.

# §2.3 — Constants

## Y118 — v3.0 through v5.0 said neither wealth coefficient was in a file, and shipped a whole-install modifier sweep that walked past the block holding one of them

**Status:** CONFIRMED (and understated)
**Method.** Grepped v3/v4/v5 §1.3 and §2.3 for the provenance sentence; then opened each version's
sweep script and checked whether it reads `00_static_modifiers.txt`.
**Evidence.** Identical sentence at `v3:546-548`, `v4:616-618`, `v5:716-718`: "The two wealth
coefficients of §1.3 are **hardcoded in the binary** — `defines.lua` and `common/defines/` were
searched and contain neither." And `provincial_production_size = { trade_goods_size = 0.2 … }` *is*
`GP_COEFF` (Y030). Three ways the sweeps missed it: v5's `wealthmodel.py`, credited by v5's own
`scripts/README.md` as the whole-install sweep including "static modifiers", reads **no** install
modifier file at all — the whole sweep is three hardcoded literal dicts. v4's `audit_modifiers.py:21`
does load every static-modifier block into `defs`, then only ever queries `defs` *by name* for
modifiers referenced from `history/provinces/`, and `provincial_production_size` is applied by the
engine and never named in history, so it sat in `defs` unexamined. v4's `validate_v4.py:147-148`
literally opens the file and greps it for a different block (`^city\s*=\s*\{`). The claim is true and
milder than the facts.

# §2.4 — The tradenodes file

## Y119 — the min-cost b-flow is massively degenerate: many distinct supports carry the same optimal cost, and which one is returned depends on presentation order

**Status:** CONFIRMED (measurement)
**Method.** For ten goods, solved the same LP nine times with nine different arc column orderings and
counted distinct optimal supports.
**Evidence.** **9 distinct supports from 9 orderings** on every one of the ten goods tested — i.e. no
two orderings agreed — with objective values equal to within 2.22e-15. "Massively degenerate" is if
anything an understatement.

## Y120 — relabelling the nodes changed the orientation on 580 of 580 runs, always by a different optimal vertex and never by a sweep tiebreak, mean 22.1 of 159 edges, objective identical to 8.9e-16

**Status:** PARTIAL
**Method.** Copied v5's independent DRAIN reimplementation (`_audit_b_drain.py`, self-contained and
parameterised by node order), verified it agrees with v6's `drain.py` on all 29 goods (0/29
disagreements), then ran 29 goods × 20 full node relabellings on the **v6** field, comparing the
relabelled orientation and the relabelled LP support back through the inverse permutation. Repeated at
three seeds.
**Evidence.** Orientation changed on **580 of 580** runs. Same-support changes: **0**;
different-support changes: **580** — so "always by returning a different optimal vertex and never by a
sweep tiebreak" is exactly right. Mean edges moving: **21.68** (seed 4242), **21.88** (seed 1),
**21.51** (seed 12345) — min 2, max 48. Not 22.1. The 22.1 figure is v5's, measured on v5's field, as
the spec's own parenthetical half-concedes ("the relabelling sweep is recorded in
`../v5-owner-agnostic/validation-v5.md`") while the other half of the same parenthetical says "the
field from `measure6.py`" — the two cannot both be true of one number. The "objective identical to
8.9e-16" figure is reproducible from no script in `scripts/`; my arc-order experiment bounds the
objective spread at 2.22e-15, the same magnitude class.
**Should carry:** mean **21.7 of 159** on the v6 field (seed-dependent, 21.5–21.9 over three seeds),
and the field attribution fixed one way or the other.

## Y121 — permuting only the arc presentation order with node labels fixed changes the optimal support on 10 of 10 goods, with objective gaps ≤ 1.8e-15

**Status:** PARTIAL
**Method.** Built the LP arc list directly, permuted the columns eight times per good over ten goods,
compared supports and objectives.
**Evidence.** Support changed on **10 of 10** goods — confirmed, and in fact every one of the nine
orderings gave a distinct support. But the maximum absolute objective gap over my 80 permuted solves
was **2.22e-15**, above the quoted ≤1.8e-15. The bound is permutation- and build-specific; the
substantive claim (the objective is identical to machine precision while the support is not) holds.
**Should carry:** "objective gaps at machine precision (≤ 3e-15 observed)", or the bound has to be
re-measured with every rebuild.

## Y122 — twenty-two flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event

**Status:** CONFIRMED (derivation)
**Method.** Compared the relabelling mean to the measured razed-China flip count.
**Evidence.** Relabelling mean 21.7 (Y120); razed-China **22** of 159 (Y132, where the spec's own 23
is wrong). The two are the same magnitude — in fact essentially equal. The comparison holds under
either figure.

## Y123 — the canonical order must be the order Phase 2's LP input is built in, not merely the order the sweep breaks ties in

**Status:** CONFIRMED (derivation)
**Method.** Read the two experiments' scopes against each other.
**Evidence.** Y121 permutes **only** the arc presentation order with node labels and every input held
fixed, and the optimal support moves on 10 of 10 goods; Y128 measures zero sweep-key ties on 1444, so
the sweep's tiebreak decides nothing here. Fixing the sweep's order alone would therefore not fix the
orientation; the LP's input order must be fixed. The inference is forced.

## Y124 — everything §1.6 and §2.8 report about stability is measured at fixed node order; re-order the same world and the map moves, with α_Φ and every input held fixed

**Status:** CONFIRMED (measurement; the claim as written holds, and the effect is narrower and more
specific than "the map moves")
**Method.** Three steps, because the obvious shortcut does not work.
1. *Instrument.* The shipped `drain.py` bakes `N`, `ORDER`, `NIDX`, `UND`, `EDGES_UND` and `NODEW`
   into module state at import, so it cannot be relabelled in place. Its `sweep_priority(…, pid=…)`
   parameter re-keys **only** the sweep. I therefore used v5's `_audit_b_drain.py`, a self-contained
   reimplementation of all five phases (peel, HHI-adaptive Phase 1, LP Phase 2, priority sweep with
   both the promotion and the fallback branch, Phase 4 un-peel) parameterised by node order.
2. *Validate the instrument on the identity permutation, on `Φ_w` specifically* — not only on the
   per-good graphs. Result: sinks `['english_channel','hangzhou']` from both, **159 of 159 edges
   agreeing**, orientation sets identical, Phase-0 core 80 from both, promotions 2 and fallbacks 0
   from both. (On the 29 per-good graphs: 0 of 29 disagreements.)
3. *Relabel end to end and map back before comparing anything.* For a permutation `p`, rebuild the
   edge list as `sorted(tuple(sorted((p[u], p[v]))))`, scatter `b_w` and `NODEW` into the new
   labelling (`b2[p[i]] = bw[i]`), run the full pipeline, then invert with `inv = {p[i]: i}` and only
   then compare orientations and sink sets. 100 trials × 3 seeds, α_Φ = 1.5 and the wealth field
   untouched throughout.
**Evidence.** The claim holds, and three quantities matter more than the bare "it moves":

| | seed 4242 | seed 7 | seed 999 |
|---|---|---|---|
| orientation changed | 100/100 | 100/100 | 100/100 |
| same LP support as baseline | 0/100 | — | — |
| mean edges moving (of 159) | 26.8 | 26.0 | 26.4 |
| returns the baseline set `{english_channel, hangzhou}` | 6/100 | 6/100 | 6/100 |
| `hangzhou` is a sink | **98/100** | **97/100** | **97/100** |
| `english_channel` is a sink | **38/100** | 43/100 | 45/100 |
| sink-count distribution | 1:10 2:33 3:31 4:24 5:2 | 1:9 2:34 3:38 4:12 5:7 | 1:14 2:24 3:35 4:24 5:3 |

25 distinct sink sets over 100 trials at seed 4242. Every relabelling returned a *different optimal
LP vertex* (same-support 0/100), and fallbacks fired 0 times in 300 trials, so this is Phase 2 and not
a tiebreak — the same cause Y120 and Y121 isolate. Nine nodes hold an end in at least one relabelling:
`hangzhou` 98, `gulf_of_siam` 55, `english_channel` 38, `wien` 31, `rheinland` 21, `sevilla` 13,
`champagne` 10, `genua` 6, `ganges_delta` 3.

**The honest reading is narrower than "the ends move".** The **Asian end is stable** — `hangzhou`
holds an end in 97–98% of orderings — and it is the **European end that is order-dependent**:
`english_channel` holds one in only 38–45%, and where it does not, the European end is `wien`,
`rheinland`, `sevilla`, `champagne` or `genua`, or there is none. So §1.6's *count* (2), its
*European* member, §2.4 item 2's end-flag list and every row of the Europe table are conditional on a
fixed canonical order; §2.8's razed-China row, which turns on whether `hangzhou` keeps its end, is
not — 97–98% stability is a real fact about that node, not an artifact.

**A methodological warning worth recording, because it is the trap on both sides.** The shipped
`sweep_priority(pid=…)` hook, run the same 100 times, changes the orientation on **0 of 100** and
returns `{english_channel, hangzhou}` every time. It re-keys only the sweep, so Phase 1's
within-cluster argmin and the promotion still read the true index and Phase 2 still builds its LP in
node order — it cannot see this effect at all. A relabelling test built on that hook would report
perfect stability; one built on a partial reimplementation reports chaos (a naive sweep without
Phase 0, the HHI selection, the promotion branch and the un-peel returns 16 sinks on the identity
permutation against `drain.py`'s 2, agreeing on 51 of 159 edges). Only a full pipeline validated
against the shipped one on the identity permutation settles it, and the validation has to be run on
`Φ_w`, not only on the per-good graphs.

## Y125 — the 580/580 result is HiGHS-specific in its detail but not in kind: any simplex returns a vertex of a degenerate optimal face

**Status:** CONFIRMED (derivation)
**Method.** Checked the argument against the LP structure.
**Evidence.** With all arc costs 1 the optimal face of this transportation-style LP is high-dimensional
(Y119 exhibits nine distinct optimal supports on one instance), and a simplex method by construction
terminates at a basic feasible solution, i.e. a vertex. Which vertex depends on the pivoting sequence,
which depends on column order. The generalisation is standard and correct; only the specific counts
are solver-specific.

## Y126 — making the orientation independent of presentation order would need a tie-breaking objective, which is a design change and is not adopted

**Status:** CONFIRMED (stipulation)
**Method.** Checked whether anything in `flowop.py` or `drain.py` perturbs or lexicographically orders
the objective.
**Evidence.** `mincost_flow` passes `c = np.ones(A)` — a flat unit cost with no secondary term and no
convex perturbation. So the change is genuinely not adopted, and the two mechanisms named
(a lexicographic secondary cost, a strictly convex perturbation) are the standard ways to select a
unique optimum. Internally consistent.

## Y127 — the priority key ties in more places than §1.1 documents: Phase 1's within-cluster argmin, the stall promotion, and the top-k cut

**Status:** CONFIRMED (derivation)
**Method.** Located each tie site in `drain.py`.
**Evidence.** Phase 1 within-cluster argmin: `S.add(min(comps[j], key=lambda v: (beta[v], v)))`.
Stall promotion: `s_star = min(terminals, key=lambda v: (beta[v], v))` — the identical `(β, index)`
form. Top-k cut: `sorted(range(len(comps)), key=lambda j: -M[j])[:k]`, where equal masses are ordered
by cluster index, which derives from node order via the component-discovery loop. All three exist and
all three are index-decided, and §1.1 documents only the free-edge sweep.

## Y128 — none of those tie sites fires on 1444: zero exact (DEF, β) ties on free edges across 29/29 goods, zero within-cluster β ties, zero tied cluster masses

**Status:** CONFIRMED (measurement)
**Method.** For all 29 goods, recomputed `DEF` on the flow-arc subgraph and tested every free edge for
an exact `(DEF, β)` tie; rebuilt Phase 1's demander components and tested for a tied argmin and for
tied cluster masses.
**Evidence.** Free-edge exact ties: **0**. Goods with a within-cluster β tie at the argmin: **0**.
Goods with tied cluster masses: **0**. All three exact.

## Y129 — end=yes on every Φ_w sink, and 1444 has two end nodes against vanilla's three

**Status:** CONFIRMED (measurement + file value)
**Method.** Counted `end = yes` in `common/tradenodes/00_tradenodes.txt` (comments stripped) and
parsed the file to name them; took the 1444 sink set from `Φ_w`.
**Evidence.** Vanilla: **3** `end = yes` occurrences — `genua`, `venice`, `english_channel`. 1444
`Φ_w`: **2** sinks — `english_channel`, `hangzhou`. The claim's "the count is not fixed — it follows
the wealth field and `α_Φ`" is independently supported by Y083 and Y089, and Y124 adds that it also
follows the node order. Y124 quantifies that: over 300 relabellings the count runs 1 to 5 and
the emitted end-flag list would name `english_channel` in fewer than half of them.

# §2.7 — Probes

## Y130 — probe 15 is one observation on one node, enough to retire §3.16's cautionary case and not enough to promote §1.9's rule to a measurement, which is weaker than v3.0's claim

**Status:** CONFIRMED
**Method.** Read W067 and its grading in `../v3-owner-agnostic/validation-v3.md`; read v3.0's §1.9
text; compared to v6.0's §2.7 item 15 and §3.16.
**Evidence.** validation-v3.md grades W067 CONFIRMED on: "Fresh vanilla Castile 1444 start this
session; opened **Sevilla's** node window and hovered France's trade power … **France 0.0 / 0.0 / 5.1%
/ 3.3** … `Transfers from traders downstream: +3.1`". One node, one country, one session, and no
second-node note (unlike W066 three paragraphs above, which carries one). v3.0's spec asserted the
rule "**correct as written and gains no qualifier**"; v6.0 asserts only that the observation is
consistent with it. The weakening is real and correctly described. Only a running game could
strengthen it, and the spec says so.

# §2.8 — Validation

## Y131 — sinks are 1 to 8 per good, and high-demand nodes are sinks at 16.8% in the top demand decile against 6.9% in the bottom

**Status:** CONFIRMED (measurement)
**Method.** Per good, ranked nodes by `c(n,g)` and counted sink membership in the top and bottom
deciles (8 nodes each), pooled over 29 goods.
**Evidence.** Top decile **39 of 232 = 16.8%**; bottom decile **16 of 232 = 6.9%**. Sinks per good 1
to 8. All three figures exact.

## Y132 — razed China: zeroing hangzhou-node development moves the Φ_w sinks to {doab, english_channel, gulf_of_siam} with 23 of 159 edges flipping

**Status:** REFUTED
**Method.** Zeroed the wealth of every counted province in the `hangzhou` node, three ways (exact 0,
1e-12, and dropping the provinces from the field entirely), and counted edges whose direction differs
from the baseline both as `|D △ D₀|/2` and by explicit per-edge comparison.
**Evidence.** Sink relocation confirmed: `{english_channel, hangzhou}` → **`{doab, english_channel,
gulf_of_siam}`**. Flip count: **22** of 159 under all three zeroing variants and under both counting
methods. The 22 edges are listed explicitly (kongo–zambezi, kongo–ivory_coast, patagonia–cuiaba,
rio_grande–california, california–mexico, california–polynesia_node, girin–nippon, girin–siberia,
mexico–polynesia_node, lhasa–lahore, gulf_of_siam–canton, canton–hangzhou, cuiaba–laplata,
ganges_delta–doab, ganges_delta–comorin_cape, comorin_cape–gulf_of_aden, katsina–tunis, tunis–sevilla,
safi–sevilla, pest–krakow, krakow–saxony, panama–carribean_trade). The identical machinery reproduces
the coal figure (10) and the `beijing` figure (15) exactly, so this is not a methodology difference.
**Should carry:** 22 of 159. Y122's "twenty-two flips is the same magnitude" then becomes an
equality rather than a comparison.

## Y133 — hangzhou, not beijing, is China's wealth pole: node wealth 226.7 against 143.0, and it holds the richest single province

**Status:** CONFIRMED (measurement, twice independently)
**Method.** Summed the field per node; found each node's richest province. Independently recomputed
from raw history/save data and `00_prices.txt`.
**Evidence.** `hangzhou` **226.7** over 26 counted provinces, richest province 1821 (Nanjing, silk,
15/15) at **27.00**. `beijing` **143.0** over 28 counted provinces, richest 1816 (grain, 13/13) at
**19.50**. 1821 is the richest counted province in the world. All figures exact.

## Y134 — zeroing beijing also moves the map — 15 flips — and what separates the two cases is which node keeps its end

**Status:** CONFIRMED (measurement)
**Method.** Same three zeroing variants applied to the `beijing` node.
**Evidence.** **15** flips under all three variants, and the sink set stays `{english_channel,
hangzhou}` — so `hangzhou` survives as a sink when `beijing` is zeroed and does not when `hangzhou`
is. The asymmetry is exactly where the claim puts it, and the renormalisation explanation is right:
deleting `beijing`'s 143.0 of 10,607.40 moves every node's `c_w`.

# §3.2 — Why a flow and a drainage sweep

## Y135 — what the contrast-ratio metric cannot see is the thing the diagnosis rests on: sparsity

**Status:** CONFIRMED (derivation, with the sparsity figures measured)
**Method.** Checked the argument, then measured the producing-node counts and the contrast ranges.
**Evidence.** Spices are produced in **18 of 80** nodes and cloves in exactly **1** — measured. A
max/min ratio taken over *producing* nodes is by construction blind to how many nodes produce nothing,
so it cannot express sparsity; that is a structural point, not an empirical one, and it is sound. The
companion measurement confirms the direction the spec draws from it: supply contrast 4–97, demand
contrast 211–15,010 (Y168), so on the ratio metric itself the demand side is the wider one. v5.0's
36-against-482.2 spices figures are indeed no longer carried (v5:950-952 verified as their source).

## Y136 — better wealth inputs move Genoa to a co-sink at roughly ×1.7 without making demand the determinant of placement

**Status:** CONFIRMED (measurement)
**Method.** Under the v1 Laplacian operator on spices (the operator §3.2 is diagnosing), bisected the
multiplier on `genua`'s counted provinces' wealth until `genua` joins the sink set.
**Evidence.** `genua` becomes a LAP spices co-sink at **×1.724**, at which point the sink set is
`{saxony, genua}` — a co-sink, not the sink, so demand is still not the determinant. "Roughly ×1.7"
holds. (Baseline LAP spices sink on the v6 field: `saxony` alone.)

## Y137 — moving the spice sink to a Chinese node takes a multiple of that node's demand in the region of 3.6–4.9×: beijing 3.61×, hangzhou 4.12×, xian 4.60×, canton 4.77×

**Status:** PARTIAL
**Method.** Two readings, both bisected to convergence under the LAP spices operator: (a) multiply the
node's `c(n, spices)` and renormalise; (b) multiply the node's provinces' **wealth**.
**Evidence.** Under reading (b) the figures reproduce: `beijing` **×3.63**, `hangzhou` **×4.13**,
`xian` **×4.61**, `canton` **×4.78** — every one within 0.02 of the quoted value, and each node joins
the sink set beside `saxony` at that point. Under reading (a) — an actual demand multiple — the figures
are **×6.91, ×8.38, ×9.88, ×10.44**. The two differ by the exponent: `α(spices) = price/P₀ = 1.5`, so a
wealth multiple `f` is a demand multiple `f^1.5`, and 6.91^(1/1.5) = 3.63. The quoted numbers are
wealth multiples described as demand multiples. (The resulting world-demand shares — 9.5%, 21.4%,
12.3%, 17.6% — match v5.0's 9.3/21.4/12.3/17.8%, confirming the same construction was used there.)
**Should carry:** "a multiple of that node's wealth in the region of 3.6–4.9×", or "a multiple of that
node's demand in the region of 6.9–10.4×" — not the first magnitude under the second description.

## Y138 — the multiple and the demand share do not line up end to end, and other nodes in the region need more still

**Status:** PARTIAL
**Method.** Extended the Y137 sweep to `girin`, `yumen`, `chengdu` and `lhasa`.
**Evidence.** The non-alignment holds and is clear: `beijing` ×3.63 → 9.5%, `hangzhou` ×4.13 → 21.4%,
`xian` ×4.61 → 12.3%, `canton` ×4.78 → 17.6% — the largest multiple does not buy the largest share,
because the shares start at 1.5%, 3.2%, 1.4% and 2.0%. But "other nodes in the region need more still"
is false for two of the four: `girin` needs **×3.89** and `yumen` **×4.49**, both *inside* the quoted
3.6–4.9 band and both less than `canton`'s ×4.78. Only `chengdu` (×8.09) and `lhasa` (×10.67) need
more. (v5.0's withdrawn range 4.0–10.8× is confirmed as its source, and reproduces here as 3.89–10.67.)
**Should carry:** "some other nodes in the region need far more (`chengdu` and `lhasa`), and some need
no more than the four named."

## Y139 — sink placement is a measurement on one input, and v5.0's rescue by two conditions fails: those conditions are necessary, not sufficient, since T2 satisfies both

**Status:** CONFIRMED (measurement of the counterexample; derivation of the inference)
**Method.** Ran `scripts/toys.py`.
**Evidence.** T2 is the five-cycle S1(+3)–u1(−3)–w(0)–u2(−2)–S2(+2)–S1 with a chord w–S1, entirely
inside the 2-core, and reports `S0 = ['u1','u2']`, `promoted = []`, no fallback — so both of v5.0's
conditions (Phase 0 a no-op, no fallback firing) hold — yet actual sinks `{u2}` against formula
`{u1, u2}`, "EQUAL: False". Necessary-not-sufficient is exactly right. T1 and T3 also reproduce.

## Y140 — none of the key-tie sites is why §2.4 requires a canonical node order; that comes from Phase 2's degenerate LP

**Status:** CONFIRMED (derivation)
**Method.** Set the two measurements against each other.
**Evidence.** Y128 measures **zero** ties at all three key-tie sites on 1444, and Y120 measures
**580 of 580** relabellings changing the orientation with a different LP support each time. So the
orientation moves under relabelling with no key tie anywhere, and the requirement cannot be coming
from the tiebreaks. Y121's arc-only permutation isolates the LP as the cause directly, since it holds
the node labels — and therefore every tiebreak — fixed.

# §3.4 — Why supply is pre-modifier

## Y141 — in v1 the production-income substitution broke the α = 1 identity, measured as orientation agreement collapsing to well under half the map

**Status:** CONFIRMED
**Method.** Located V138 in `../v2-drain/claims-v2.md` and its grading in
`../v2-drain/validation-v2.md`; traced the underlying v1 figure.
**Evidence.** V138: "orientation agreement collapsed from 159/159 to 68/159", graded CONFIRMED on a
re-run: "rel. residual **1.512e+00** (vs 1.959e-15 with trade-value supply); orientation agreement
**68/159**". Original at `v1-laplacian/validation.md:4517`. 68/159 = **42.8%**, which is "well under
half" — 7.2 points below, so the phrase is true if not dramatic. One caveat the v6.0 wording drops:
v2's re-run notes that the collapse requires modelling the owner factors, because in the proxy
dataset raw production income equals trade value and substituting *that* alone changes nothing
(159/159, checked). Since §3.4's whole argument is about owner factors entering through production
income, the caveat does not undercut the claim.

# §3.5 — Why α is anchored absolutely

## Y142 — change_price values are fractions of the good's base price, settled by tutorial/eu4_tutorial_chapter10.eu4: paper 4.375 on a base of 3.5, gems 5.000 on 4.0

**Status:** CONFIRMED (file value, and the save does settle it)
**Method.** Located the shipped save (plain text, `EU4txt` header, `date=1492.2.6`), read its price
section, and cross-checked the base prices and the modifier provenance.
**Evidence.** The save carries `paper={ current_price=4.375 change_price={ key="PAPER_IN_BUREAUCRACY"
value=0.250 expiry_date=1821.1.2 } }` and `gems={ current_price=5.000 change_price={ key="FACETING"
value=0.250 … } }`, and exactly two of the 32 goods carry an active modifier. Base prices: paper 3.5,
gems 4.0. `3.5 × 1.25 = 4.375` and `4 × 1.25 = 5` exactly (checked in exact rationals);
`3.5 + 0.25 = 3.75 ≠ 4.375`. Three things close the additive loophole: the save records the modifier
list itself, so the additive reading has nothing else to add; no `change_price` anywhere in the install
carries a value of 0.875, and no additive combination of paper's four keys reaches it; and all 30 goods
with no modifier have `current_price` exactly equal to `base_price`, so `current_price` is
unambiguously the modified base. Provenance also checks out — `FACETING` fires 1485.1.1 and
`PAPER_IN_BUREAUCRACY` 1490.1.1, both before 1492.2.6, both `duration = -1`. *What it does not settle,
and the claim does not assert:* sum-of-fractions versus per-modifier compounding, since no shipped save
has two simultaneous modifiers on one good.

## Y143 — the install carries 161 textual change_price blocks: 93 events, 14 missions, 1 common, 53 history of which 13 negative (all in HAB - Austria.txt), none in decisions

**Status:** PARTIAL
**Method.** Counted `change_price\s*=\s*\{` per tree with comments stripped, under four stripping
modes (string-aware with multi-line strings, string-aware with newline-terminated strings, naive
`#`-to-EOL, and none), then swept **every** tree in the install.
**Evidence.** Per-tree figures exact and stable across all four stripping modes: events **93**,
missions **14**, common **1** (`common/parliament_issues/01_english_parliament_actions.txt:658`, tea
+0.5, key `the_tea_act`), history **53**, decisions **0** over 196 files — subtotal **161**. History
negatives: **13**, all in `history/countries/HAB - Austria.txt`. But a whole-install sweep finds a
**162nd** textual `change_price = {` at `patchnotes/1.8 Patchnotes.txt:445` — the patch note that
announced the effect. `tutorial/*.eu4` additionally carries 14 occurrences as save state. So the
per-tree census is right and the unscoped sentence "**The install carries 161 textual `change_price`
blocks**" is one off, in exactly the way v6.0's own R2 convention (Y007) exists to prevent.
**Should carry:** "161 across `events/`, `missions/`, `common/`, `history/` and `decisions/`" — the
scoping the rest of the sentence already supplies.

## Y144 — ten of the 161 never execute: four in effect_tooltip strings, three in the effect string of a country_event_with_effect_insight, three in tooltip = { } wrappers, so 151 are executable

**Status:** CONFIRMED (file value)
**Method.** Token-walked each file with a brace key-stack, re-scanning quoted-string contents, with
strings allowed to span newlines (a tokeniser that terminates strings at `\n` reports zero, which is
the trap).
**Evidence.** Seven inside quoted strings, and the 4/3 split is exact — `effect_tooltip`:
`missions/DOM_Britain_Missions.txt:919` (fur 0.25 `ENGLISH_FUR_TRADE`),
`missions/KoK_Persia_Missions.txt:3384/3390/3396` (silk 0.25, dyes 0.5, cloth 0.35); `effect` inside a
`country_event_with_effect_insight`: `missions/KoK_Byzantine_Missions.txt:2070` (silk 0.2),
`missions/KoK_Yemen_Missions.txt:954` (coffee 0.25), `missions/WOC_Italian_Missions.txt:2841`
(wine 0.4). Three inside `tooltip = { }`: `events/flavorMAL.txt:1736` (ivory 0.33),
`missions/WOC_Hisn_Kayfa_Missions.txt:1448` and `:1459` (grain 0.1 ×2). 161 − 10 = **151**.
`country_event_with_effect_insight` exists at `common/scripted_effects/00_scripted_effects.txt:6588`
and its body is `country_event = { id = $id$ … } custom_tooltip = … tooltip = { $effect$ }` — which is
*why* they never fire. One wording note: the three are one block each in three separate calls in three
different files, not three blocks in one call.

## Y145 — six of the seven quoted blocks duplicate a block already counted in events/, and the seventh names a price key no event ever sets

**Status:** CONFIRMED (as written)
**Method.** For each of the seven, matched `(trade_goods, value, key)` against every executable block
in `events/`, then searched the whole install for the key.
**Evidence.** Six have an exact `(good, value, key)` twin in `events/`: silk 0.2 `BYZ_growing_demand`
(`events/flavorBYZ.txt:1921`), silk 0.25 `PERSIAN_SILK` (`FlavorPER.txt:1463`), dyes 0.5
`PERSIAN_DYES` (`:1469`), cloth 0.35 `PERSIAN_CLOTH` (`:1475`), coffee 0.25
`YEM_coffee_price_boost` (`flavorYEM.txt:89`), wine 0.4 `ITA_wine_upgrade` (`flavorITA.txt:448`). The
seventh is **fur 0.25 `ENGLISH_FUR_TRADE`**, and `ENGLISH_FUR_TRADE` appears in exactly one place in
the install — that dead tooltip string. The claim says "names a **price key** no event in the install
ever sets", which is precisely true. (Under a looser (good, value) match all seven would duplicate
something, since three executable fur +0.25 blocks exist; the 6/1 split lives at key granularity, and
the claim's wording is the correct one.)

## Y146 — all ten are positive and every negative block in the install is executable, so the partition is identical under either census

**Status:** CONFIRMED (file value)
**Method.** Read the ten values; located every negative-value block install-wide and classified each
as executable or not; recomputed the partition under both censuses.
**Evidence.** The ten values are 0.33, 0.25, 0.2, 0.25, 0.5, 0.35, 0.25, 0.1, 0.1, 0.4 — all positive.
**40** negative blocks install-wide (27 in `events/`, 13 in `history/`), **all 40 executable** — none
in a quoted string or a `tooltip = { }`. The 13-2-4-11 partition is byte-identical under the 161 and
151 censuses, and no good's minimum changes. Independently, the partition itself reproduces: strictly
below 2.0 **13** (grain and wine both at 0.625), exactly 2.0 **2** (gems, silk), negative but above 2.0
**4**, no negative event **11**, summing to 30. *One loose word in the surrounding prose, not in this
claim:* wool's bucket depends on including `history/` — restricted to `events/` the partition becomes
12-3-4-11 — so "by a single vanilla `change_price` **event**" is imprecise, though §3.5's own next
paragraph says exactly that and gets it right.

## Y147 — v4.0 said 154 by dropping the quoted seven, v5.0 said 161 by counting them, v5.0's "per-file count assertion" existed nowhere, and the cause is pdx.py tokenising a quoted string as one unit

**Status:** CONFIRMED (all four parts)
**Method.** Grepped v4.0 and v5.0 for their censuses and for the assertion claim; searched all of
`../v5-owner-agnostic/scripts/` for a per-file assertion; read `scripts/pdx.py`; ran its tree walk
over the install.
**Evidence.** `v4:949` "All **154** `change_price` blocks were parsed — 93 in `events/`, **7 in
`missions/`**, 1 in `common/` and **53 in `history/`**". `v5:1073-1077` "All **161** … so **the scan is
now guarded by a per-file count assertion**". The assertion does not exist: `v5/scripts/w10.py` is
byte-identical to v4's, contains `except Exception: pass`, has zero `assert` statements, and its only
census is per-*tree* (`byt = collections.Counter(h[2] for h in hits)`); `validate_v5.py:241` asserts a
per-tree regex tuple `(161, 93, 14, 1, 53)` that is never compared to the `pdx` walk's `hits` list,
which is what the partition is computed from; no `assert` on `change_price` exists anywhere in that
directory. The mechanism is exactly as described: `pdx.py:9`
`TOK = re.compile(r'"[^"]*"|[{}=]|[^\s{}=]+')` — the string alternative wins at each position and
`[^"]` matches newlines, so a multi-line quoted string collapses to one token, stored as a scalar at
line 76 and never a `Node`. Measured: **pdx.py's tree walk finds 154; raw text finds 161**, and the 7
missing are exactly the 7 quoted blocks in exactly the 5 expected files — so 154 is the number a bare
`pdx.py` walk yields, which is v4.0's figure, and the diagnosis is confirmed end to end.

# §3.9 — Why Φ_w is the installed graph

## Y148 — genua, gulf_of_siam and sevilla rank 4th, 3rd and 7th by node wealth (mexico 2nd) — 296.0, 297.9, 266.5 against english_channel's 316.6, which is a sink

**Status:** CONFIRMED (measurement)
**Method.** Ranked all 80 nodes by summed counted-province wealth.
**Evidence.** 1 `english_channel` **316.6** (a sink), 2 `mexico` **300.4**, 3 `gulf_of_siam`
**297.9**, 4 `genua` **296.0**, 5 `malacca` 295.2, 6 `nippon` 293.6, 7 `sevilla` **266.5**. Every
rank and every figure exact. The accompanying derivation — a rich non-sink draws more edges in than
out as a net demander even though flow passes through — is consistent with `genua`'s role in Y074
(Phase-1 selected, ends a transit node).

## Y149 — Φ_ord is acyclic for free and scores higher on self-coherence, and was superseded on design grounds: sweep-scheduling artifacts, a majority terminate no good, no demand capital among them, the count does not concentrate

**Status:** PARTIAL
**Method.** Built `Φ_ord = Σ_g V_g · order_g` on the v6 field, oriented by descending `Φ_ord`, and
measured: acyclicity, self-coherence, the end set, how many ends terminate no good, whether any of
the top demand nodes is an end, and the end count as cloves-α sweeps 2…64.
**Evidence.** Acyclic for free: **True**, 159/159 oriented. Self-coherence **60.4% / 60.1%** against
`Φ_w`'s 53.6% / 52.3% — higher, confirmed. End count **14**; of those, the ends terminating no good at
all are `amazonas_node`, `rio_grande`, `james_bay`, `chengdu`, `yumen`, `basra`, `ragusa` — **7 of
14**, which is **exactly half, not a majority**. None of the top-five demand nodes (`genua`,
`english_channel`, `hangzhou`, `gulf_of_siam`, `champagne`) is among the 14 — confirmed. The end count
is **14 at every cloves-α from 2 to 64** — it does not concentrate, confirmed. And "no figure is
maintained for it" is honoured in §3.9's text.
**Should carry:** "half of them terminate no good at all" — and, since the number is a measurement the
section declines to maintain, better as "many of them" than as a fraction that must be recounted.

## Y150 — v2.1–v4.0's "two vanilla-like ends at 1444" is not the adoption argument and should not be revived

**Status:** CONFIRMED
**Method.** Verified the prior justification and read v6.0's §3.9 for what the adoption argument
actually rests on.
**Evidence.** The v2.1–v4.0 calibration text is verified at Y070. v6.0 §3.9's adoption bullet rests on
"one operator, one set of guarantees, and ends that move with the world" and on reuse of §1.1
unchanged — it nowhere counts ends. The warning is internally consistent with §2.3's withdrawal and
with §1.6's Y085 warning, and it is well motivated: the field does again give two ends (Y073), so the
temptation is live.

## Y151 — what the trade costs is self-coherence with the per-good graphs (no figure quoted); what it buys is one operator, one set of guarantees, and ends that sit where the wealth is

**Status:** CONFIRMED
**Method.** Checked §3.9 for a quoted figure for the cost; checked the "buys" side against the
guarantees §1.1 proves and against the sinks' wealth ranks.
**Evidence.** §3.9 quotes no number for the coherence gap (it says "scores **higher**" and "*No figure
is maintained for it here*"); Φ_w's own 53.6%/52.3% appears in §1.6 and §2.8, which is Φ_w's figure,
not the gap. The "buys" side checks out: `Φ_w` reuses §1.1 unchanged, so LP feasibility, acyclicity,
determinism and scan-invariance carry over (measured: acyclic, 159/159, every node drains to a sink),
and the ends are `c_w` ranks 2 and 3 — where the wealth is on the measure the operator reads.

# §3.10 — Why the engine's economy is overwritten

## Y152 — the two forms agree to a worst relative disagreement of 0 to 3.7e-16 — one to three units in the last place

**Status:** PARTIAL
**Method.** Built each of the five named nodes' real 1444 country table from the save's `trade={}`
block, formed `income_C = Σ_g v_g·cs_g·ps_C` and `ps_C·Σ_g v_g·cs_g` in doubles, and took the worst
relative difference over every collector at every node.
**Evidence.** Worst relative disagreement **2.15e-16** (at `malacca`), with per-node worsts
2.12e-16 (sevilla, genua, champagne) and 2.15e-16 (malacca, gulf_of_siam). One ULP of a double is
2.22e-16, so what I measure is 0 to ~1 ULP. The claim's magnitude class — an exact identity computed
in doubles, agreeing to a small number of ULP — is confirmed, and the framing ("This is an
**identity, not a measurement**") is right. But the specific 3.7e-16 is not reproducible: it depends on
the construction of `cs_g` and the summation order, neither of which the spec states, and no script in
`scripts/` computes it. 3.7e-16 is also 1.67 ULP, so "one to three units in the last place" is a loose
gloss on its own number.
**Should carry:** either name the construction (which node table, which `collected_share`, which
summation order) or state the bound as "to within a few units in the last place", which is what the
argument needs.

## Y153 — propagation is kept on a single graph, and the reason is not the one v1 through v6.0's own first draft gave

**Status:** CONFIRMED (derivation)
**Method.** Checked the stated reason against the algebra, and checked that the prior reason was
different.
**Evidence.** Reading one installed graph makes the propagated term carry no `g`, so `powershare_C(n)`
factors out of `Σ_g value_g·collected_share(n,g)` identically — the identity holds by construction,
and in doubles to within a few ULP (Y152). The prior reason (that per-good propagation *breaks* the
factoring, hence "Per-good propagation. Breaks the income factoring and with it Goal 7" in §3.15) is
different and, per Y155, wrong. Both halves hold.

## Y154 — per-good propagation makes a country's power at the node differ by good, because §1.9 reads downstream neighbours: gulf_of_siam's 29 goods leave it by seven distinct downstream sets

**Status:** CONFIRMED (measurement)
**Method.** For each of the 29 goods, took `gulf_of_siam`'s out-neighbour set in that good's
orientation and counted distinct sets.
**Evidence.** **7** distinct sets: `{}` (12 goods), `{burma}` (6), `{burma, canton, malacca}` (4),
`{canton}` (2), `{burma, canton}` (2), `{burma, malacca}` (2), `{canton, malacca}` (1) — 29 goods in
total. Exactly seven, and the mechanism is as described: §1.9 sums the contributions of a node's
downstream neighbours, and those differ per good.

## Y155 — that does not break the identity: with ps̄_C = Σ_g v_g·cs_g·ps_C(g) / Σ_g v_g·cs_g, collect_pool·ps̄_C = income_C follows algebraically and Σ_C ps̄_C = 1

**Status:** CONFIRMED (derivation)
**Method.** Checked both statements symbolically.
**Evidence.** `collect_pool = Σ_g v_g·cs_g` by §2.6's own definition of the collectible pool, so
`collect_pool · ps̄_C = Σ_g v_g·cs_g·ps_C(g) = income_C` immediately — the definition of `ps̄_C` is
constructed to make this an identity. And `Σ_C ps̄_C = Σ_g v_g·cs_g·(Σ_C ps_C(g)) / Σ_g v_g·cs_g = 1`
provided `Σ_C ps_C(g) = 1` for every `g`, which holds because `ps_C(g)` is a share among collectors.
So `ps̄_C` is a legal share vector and one scalar per node reproduces every collector's income exactly.
The only premise is `Σ_g v_g·cs_g > 0`, i.e. the node collects something — true wherever income is
nonzero. Sound.

## Y156 — both inputs already exist per good at write time, and §2.6 sums exactly them into collect_pool

**Status:** CONFIRMED (derivation)
**Method.** Compared `ps̄_C`'s inputs to §2.6's written fields.
**Evidence.** §2.6's table writes "Node collectible pool | `Σ_g value_g(n) · collected_share(n,g)`" —
which is `Σ_g v_g·cs_g`, exactly the denominator of `ps̄_C`, and exactly the two per-good quantities
its numerator needs. Both already exist at write time by construction of the value pass. Correct.

## Y157 — the real cost is that ps̄_C is not derivable from trade power alone: it is value-weighted, so installing it means writing a fictitious per-node trade power

**Status:** CONFIRMED (derivation)
**Method.** Checked the functional dependence of `ps̄_C`.
**Evidence.** `ps̄_C` is a function of `{v_g}`, `{cs_g}` and `{ps_C(g)}`. The first two are value
quantities and the weights do not cancel unless `ps_C(g)` is constant in `g` — which under per-good
propagation it is not (Y154). So `ps̄_C` is not a function of trade power alone, and the only way to
install it in a field the engine reads as trade power is to write a number whose *ratio* equals it.
Every other consumer of that field (propagation, privateering thresholds, trade-conflict CB limits,
trade-company limits — all of §1.10) then reads it. The cost is structural, as stated.

## Y158 — that is a claim about what the engine exposes, not a magnitude, and it is why the single graph stays

**Status:** CONFIRMED (derivation)
**Method.** Checked the contrast against the single-graph case.
**Evidence.** On one graph `ps_C` carries no `g`, so the scalar the engine needs simply *is* the
country's power share, needing no invented power field. The asymmetry between the two cases is
structural and not quantitative, so no measurement could settle it — consistent with §1.1's
three-way vocabulary (proved / measured / true-by-construction) which the spec says it enforces.

## Y159 — every magnitude previous versions quoted was an artifact: v1–v4.0's "5.96 ducats on a node paying ~250", v4.0's 0.41%, v5.0's "redistributive and single-digit percent", v6.0's first draft's "at most 0.1%"

**Status:** PARTIAL
**Method.** Grepped every prior spec for each figure and read v4.0's own treatment of the 5.96 figure.
**Evidence.** 0.41% is v4.0's alone (`v4:1076`, "overstates **every** collector's income by
**0.41%**, a total of 0.40 ducats on a node collecting 97.1"); "redistributive and single-digit
percent" is v5.0's alone (`v5:1210`). But **5.96 is v1 through v3.0, not v1 through v4.0**: it appears
at `v1:440`, `v2:708`, `v3:986` and **not** in v4.0's spec, because v4.0 removed it deliberately —
`v4/validation-v4.md:265` "### The `5.96 ducats on a node paying ~250` — REFUTED",
`v4/scripts/validate_v4.py:452` `hasnt("3.10", "the 5.96-ducat figure", "off by 5.96 ducats on a node
paying ~250")`, and `changes-v4.md:1545` "`5.96 ducats on a node paying ~250` names a node that does
not exist". v5.0 made the same one-version error first (`v5:1210`, "v1 through v4.0 quoted") and v6.0
inherited it. The general point — each figure measured its own construction — is sound and is
independently supported by Y152 and Y160.
**Should carry:** "v1 through v3.0's '5.96 ducats on a node paying ~250'".

## Y160 — gross-value weighting alone ranges from 0.00% to 4.6% across collector sets on this field, and up to 49% in general

**Status:** PARTIAL
**Method.** Searched `scripts/` for any script computing either figure; then built an independent
per-good propagation model (each country's node power = own `p_pow` plus, for each downstream
neighbour in that good's graph, that neighbour's `p_pow` / `TRADE_PROPAGATE_DIVIDER` = 5.0 from
`defines.lua`) and compared the collected-value-weighted mean share against the gross-value-weighted
one over three collector sets (all, top half by power, bottom half by power) at every node with a
country table.
**Evidence.** No script in `scripts/` computes either number; the 4.6% traces to
`scripts/validation-v6-round1.md`'s own measurement, and "up to 49% in general" has no derivation on
record anywhere. My construction over 237 (node, collector-set) pairs gives **0.000% to 1.238%** —
the 0.00% floor reproduces, the 4.6% ceiling does not. Since the *point* of the surrounding sentence
(Y159) is that every such magnitude measures its own construction, quoting two magnitudes without
stating the construction is the same defect one clause later.
**Should carry:** either name the construction and the collector sets, or drop both figures, which is
what Y161 already says the section does.

## Y161 — no figure is quoted here, because the identity holds and the objection is structural

**Status:** PARTIAL
**Method.** Read the sentence in place against the two clauses immediately preceding it.
**Evidence.** The claim is true of the *cost of per-good propagation*, for which §3.10 quotes no
magnitude. It is false of the paragraph: the same parenthetical quotes "0.00% to 4.6% across collector
sets on this field, and up to **49%** in general" two clauses earlier, plus 5.96, 0.41%, "single-digit
percent" and "at most 0.1%" as attributed artifacts. The stipulation is defensible under a narrow
reading (no figure for the *magnitude of the cost*) and self-contradicting under the plain one.
**Should carry:** "no figure is quoted for the cost", or delete Y160's figures so the sentence is true
as written.

## Y162 — no node in the model has local trade value near 250

**Status:** CONFIRMED (measurement)
**Method.** Summed per-province production income per node and ranked.
**Evidence.** Largest node local trade value **112.6** (`english_channel`), second **103.4**
(`mexico`) — nothing within a factor of two of 250. v5.0's withdrawn "the largest is 112.6"
(`v5:1210`) was itself correct, so the withdrawal is a convention choice, not a correction.

# §3.13 — Open questions

## Y163 — the one open wealth question is now a design question rather than a classification one

**Status:** CONFIRMED (derivation)
**Method.** Read §3.13's wealth bullet against §1.3.
**Evidence.** §1.3 reads development, the trade good and the four province-state modifiers and nothing
else (Y020, Y112 confirmed against `solver.py`), so there is no classification rule left to get right
and the only remaining question is whether to re-admit sources — a design decision. The restatement
follows from the change and is internally consistent with §1.3.

## Y164 — trade_goods_size and trade_goods_size_modifier are granted in many places, and v3.0 through v5.0 tried to admit the province-scoped subset by rule

**Status:** CONFIRMED (file value)
**Method.** Found a concrete instance in each of the eight categories the claim names; verified the
prior rule.
**Evidence.** buildings — `common/buildings/00_buildings.txt:2216` `manufactory`
`modifier = { trade_goods_size = 1.0 }`; event modifiers —
`common/event_modifiers/00_event_modifiers.txt:176` `encomienda_system`; great projects —
`common/great_projects/01_monuments.txt:9724` `potosi` `province_modifiers = { trade_goods_size = 1.0 }`;
static modifiers — `00_static_modifiers.txt:252` `provincial_production_size`, `:327`
`native_assimilation`, plus the four condition blocks; province-triggered modifiers —
`common/province_triggered_modifiers/00_modifiers.txt:867` `cerro_rico_modifier`
`trade_goods_size = 3.0`; holy orders — `common/holy_orders/00_holy_orders.txt:30`
`trade_goods_size_modifier = 0.1`; state edicts —
`common/state_edicts/zzz_urbanization.txt:13` `trade_goods_size_modifier = 0.33`; trade-company
investments — `common/tradecompany_investments/00_Investments.txt:206` and `:227`. No category is
empty. The prior rule is the two-test classifier quoted in `changes-v6.md`'s removal of the §1.3
table, present in v3/v4/v5.

## Y165 — re-admitting any of those sources means re-admitting the maintenance burden, so the question is whether the fidelity is worth it

**Status:** CONFIRMED (derivation)
**Method.** Checked what re-admission would require.
**Evidence.** Y164 shows eight distinct grant sites, six of which are country- or owner-conditional in
at least some instances, so admitting the province-scoped subset requires exactly the classifier v6.0
deleted — the surface Y004 shows was mis-classified in both audits that examined it. And the fidelity
at stake is measurable and small: 0.99% of world wealth over 89 of 2,472 provinces (Y003, Y025). The
trade-off the claim frames is real and correctly framed.

## Y166 — under the calibration's α = 16 the cloves demand order is hangzhou, beijing, doab, and the sink lands on a high-demand node rather than a geographic accident

**Status:** CONFIRMED (measurement)
**Method.** Set `α(cloves) = (price/P₀)² = (8/2)² = 16` (the §3.13 calibration's unclamped exponent-2
rule), ranked nodes by `c(n, cloves)`, then ran DRAIN with the calibration's twig tolerance 3e-4 in
place of the baseline 1e-11.
**Evidence.** α = 16 confirmed arithmetically. Demand order top three: **`hangzhou`, `beijing`,
`doab`** — exact. At the calibration's tolerance the cloves sink set is **`{beijing}`** alone — the
second-highest demand node, and `cloves` has exactly one producer (`the_moluccas`), so the sink is
nowhere near it geographically. At the baseline tolerance the sinks are
`{kongo, beijing, gujarat, timbuktu, genua}`, which is the geographic-accident behaviour the
calibration is meant to fix. Both halves hold.

## Y167 — hangzhou, not Beijing, holds the richest single province

**Status:** CONFIRMED (measurement)
**Method.** Global argmax over the wealth field; cross-checked from raw sources.
**Evidence.** Province **1821** (Nanjing, silk, `base_tax` 15, `base_production` 15) at **27.00**, in
the `hangzhou` node. Beijing's richest is 1816 at 19.50. v2's "Beijing, holding the richest single
province" (`v2:776-777`) is verified as the target of the correction, and was already refuted inside
v2's own audit. v5.0's withdrawn 30.4-against-19.5 (`v5:1303-1305`) is verified as its source.

# §3.15 — Rejected

## Y168 — with v1's ε floor removed the contrasts run 4–97 on supply against 211–15,010 on demand over the 28 goods produced in more than one node; cloves has a single producer

**Status:** CONFIRMED (measurement)
**Method.** Computed max/min of the positive entries of `s(·,g)` and of `c(·,g)` per good with ε = 0,
over goods with more than one producing node.
**Evidence.** Supply contrast **4.0 to 97.0** over **28** goods; demand contrast **211.1 to
15009.9** → 211–15,010; the single-producer good is **`cloves`** (producer `the_moluccas`). Every
figure exact, and the sparsity point in miniature holds — cloves has no supply contrast to measure at
all.

## Y169 — v3.0 and v4.0 repeated the 10⁷ / 10²–10³ ratio here while v4.0's own §3.2 was withdrawing it

**Status:** CONFIRMED
**Method.** Grepped v1–v5 for the ratio and resolved each hit to its enclosing section header.
**Evidence.** §3.15 carries it at `v2:807`, `v3:1109`, `v4:1200` (identical text: "**supply contrast
(10⁷) drowns demand contrast (10²–10³)**"), and v1 does not carry it at all. v4.0's **§3.2** at line
837 simultaneously withdraws it ("That ratio was `max(s)` over the **ε floor** of v1's regularizer").
So v4.0 does contradict itself across §3.2 and §3.15, and v3.0 does repeat it. One nuance: v2's §3.15
also carries the sentence, but v2's §3.2 does not withdraw it, so v2's document is internally
consistent and the "repeated it while it was being withdrawn" charge properly attaches only to v3.0
and v4.0 — which is what the claim says.

## Y170 — ranked orientation wins the sink–demand alignment statistics and loses delivery: a sixth of world demand stranded, orphan sinks, net-producer sinks where DRAIN, LAP and FLOW post none, several times DRAIN's sinks per good; no figures maintained

**Status:** PARTIAL
**Method.** Ran `rankop.py` and `rankrep.py`; then applied the shared Phase-4 delivery evaluator to
the RANK orientation for all 29 goods, and counted orphan sinks (sinks unreachable from any producer)
and net-producer sinks.
**Evidence.** Alignment: RANK P(sink | top demand decile) **46.6%** against DRAIN's 16.8% and LAP's
9.0%, with spearman −0.290 against LAP's −0.097 — "a far higher share of top-demand nodes" holds
decisively. Sinks per good: RANK **13.3** against DRAIN's 3.72 — "several times" holds (3.6×). Orphan
sinks: **32** across the 29 goods — holds. Net-producer sinks: RANK **8–9**, DRAIN **0 of 108**, LAP
**0 of 102** — holds. But "a sixth of world demand is stranded" does **not** reproduce: under the
shared evaluator RANK's mean unserved on the v6 field is **0.296**, i.e. about **30%**, nearly a
third, against DRAIN's 0.118. And quoting a figure at all sits badly with the entry's own
"**No figures maintained**" and with the R3 convention (Y008).
**Should carry:** "roughly a third of world demand stranded" — or, consistently with R3, no figure at
all, since the direction is what the argument needs.

## Y171 — seeded basin growth leaves demand unserved at every tuning tried

**Status:** CONFIRMED (measurement)
**Method.** Ran `scripts/basin.py`, which sweeps the seed count.
**Evidence.** Unserved (and stranded, equal by conservation) at every seed count tried: S=1 → 0.4518,
S=3 → 0.5303, S=5 → 0.5009, S=8 → 0.4994, S=13 → 0.4619. Every tuning strands 46–53% of demand, so
the directional claim holds with room to spare, and the withdrawn "88.4% at best tuning" figure is
correctly no longer carried.

## Y172 — Φ_ord as the installed graph: the most self-coherent aggregate measured and acyclic for free, superseded on design grounds, no figures maintained, and the coherence ceiling v2.0 and v2.1 quoted predates the deterministic sweep and was never regenerated

**Status:** CONFIRMED
**Method.** Re-measured Φ_ord (Y079, Y149); read §3.15's entry for figures; traced the ceiling through
v2–v5.
**Evidence.** Φ_ord is acyclic for free and is the most self-coherent aggregate measured here
(60.4%/60.1% against Φ_w's 53.6%/52.3%; the value-weighted net flow contains cycles and cannot be
installed at all). §3.15's entry carries no number. The ceiling history checks out: v2 quotes 62.7% at
three sites (`v2:165`, `:679`, `:852`), v2's own audit records that under the deterministic sweep the
figure is 60.2% and that 62.7% "predates the deterministic sweep the spec itself adopts", and the
successors never regenerated it consistently either — v3.0 used 60.2%, v4.0 60.0%, v5.0 60.3%, each
with the same explanatory sentence. So "was never regenerated after it" is true of v2's number, which
is what the claim asserts.

## Y173 — the 3-mass gravity kernel reproduces whatever end count it is seeded with while γ is small enough and loses that property as γ approaches 1; rejected on three non-numeric grounds

**Status:** CONFIRMED (measurement of the behavioural claim; derivation of the three grounds)
**Method.** Built `Φ(n) = max_m c_α(m)·γ^dist(n,m)` over the top-k pairwise-unconnected demanders on
the v6 field, oriented by descending Φ, and counted ends for k = 2…6 and γ ∈ {0.3, 0.5, 0.7, 0.9,
0.95, 0.99}. Separately oriented by a pure `wealth^α` endpoint comparison with no reach term for
α ∈ {0.5, 1, 2, 4, 8, 16, 32}.
**Evidence.** The seeded-count property holds exactly for γ ≤ 0.7 at every k tested (k=2→2, 3→3, 4→4,
5→5, 6→6) and degrades as γ → 1 (at γ=0.9: k=5→4 and k=6→4; at 0.95 both →3; at 0.99 every k→1). The
three grounds: (i) it pins the count by fiat — true, the count is the seed count over the whole usable
γ range, so no world state could merge the world into one basin; (ii) it needs a second operator with
its own reach knob γ — true, `dist` and γ are not in DRAIN; (iii) a pure `wealth^α` comparison with no
reach term does not concentrate ends — **measured**: ends stay 15, 15, 14, 11, 10, 12, 12 across α from
0.5 to 32, never approaching a small count, because a local wealth maximum survives every positive α.
All three, and none of them numeric in the sense R3 forbids.

# §3.16 — Evidence standard

## Y174 — implemented as written, the α = 1 identity's residual reached 1e-5 against v1's ε of 1e-6, and would have been diagnosed as a solver bug

**Status:** CONFIRMED
**Method.** Located V204 in `../v2-drain/claims-v2.md` and its grading; traced the underlying v1
figure to `../v1-laplacian/validation.md`.
**Evidence.** V204 is graded CONFIRMED on a re-run of both variants: "(a) ε = 1e-6 on each per-good
`s`, φ₀'s supply raw (the spec-as-written instantiation) … rel. residual **9.58e-06** — the ~1e-5
failure, which would indeed read as a solver bug against §2.8's 1e-14 working tolerance; (b) ε applied
to φ₀'s supply too … **1.72e-15** — identity restored." v1's own figure is 1.15e-5 at ε = 1e-6
(`v1-laplacian/validation.md:3516`, `:4921`, `:6238`, with the residual first-order in ε). So the
direction is right — 1e-6 is the *regulariser* and 1e-5 the *residual* — and both magnitudes hold.
This is the one place where the earlier, looser phrasing ("at the tolerance v1 used") would have
inverted the two, and v6.0's wording does not.

---

## Notes on the harness and on two items the audit could not settle from files

**`verify6.py`'s two paths are not equally maintained.** `run_spec()` builds every needle from a
computed value; `run()`, the checklist path, still carries typed literals — `5703`, `0.0227`, `1.70`,
`3.51`, `132`, `27.00`, `13.40`, `8` — and five of them now disagree with the install. Running
`verify6.py ../fixes-agreed.md` reports **21 checks, 5 failed**. That is the harness working as
designed on a stale document, but it also means the widest-band figure the *spec* prints (1.71,
[3.50, 5.21]) is checked nowhere, while the stale 1.70 / [3.51, 5.21] in the checklist passes.

**`mutate6.py` is not independent coverage.** Its twelve spec mutations are generated from the same
twelve figures `run_spec()` checks, so "caught 12 of 12" is a consistency check on the harness, not a
measure of what the harness would catch. I confirmed the run: 12 of 12, and every one of the twelve is
a figure already in the check set.

**Two claims rest on engine behaviour no file states.** Y043 (devastation's linear scaling) and Y105
(the `cooldown = no` opt-out) are both cases where the files are silent and the model or the prose
supplies the reading. Y043 says so in terms and is graded CONFIRMED on that basis; Y105 does not and is
graded PARTIAL for that reason. Neither can be settled without instrumenting a running game.

**Claims whose primary evidence is a single tooltip reading.** Y033, Y034, Y036, Y038 and Y039 all rest
on observations from prior game sessions that cannot be re-observed here. Where the arithmetic on those
observations is checkable I checked it, and that is what decided Y033 (refuted) and Y034/Y039
(partial); the observations themselves are taken as recorded.
