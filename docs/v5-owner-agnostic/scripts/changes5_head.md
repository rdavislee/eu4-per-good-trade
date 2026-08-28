# Changes, spec v4.0 → v5.0

**Method.** v5.0 was produced by **copying** `../v4-owner-agnostic/per-good-trade-spec.md`
byte-for-byte (md5 `92c786b6301b5de02b786dacf9bc92aa`) and then applying **68 asserted string
replacements**, each one anchored on text that had to be present exactly once or the patch aborted.
Every replacement is quoted in full below. Replaying the 68 edits in order against the v4.0 file
reproduces v5.0 **byte for byte**, so this document is the complete diff and not a summary of one.
A paragraph-level diff reports **26 paragraph groups replaced, 0 inserted and 0 deleted outright**,
and the 42 headings are identical. The file grew from 116,649 to 131,566 bytes (1,360 → 1,504
lines).

That "0 inserted" describes the *paragraph* diff, and it is worth being precise about what it does
and does not buy, because v4.0's version of this paragraph overclaimed and an independent extraction
caught it.

**v5.0 adds no new subject matter**: every section it touches, v4.0 already covered, and every
proposition in it is either inherited unchanged or attached to a v4.0 proposition the re-review
graded wrong, unproved or unverified. **v5.0 does add propositions**, and it has to. Replacing
"exactly two local modifiers enter wealth" with an enumeration of sixteen provinces, six great
projects and a DLC gate is one proposition out and a dozen in; so is replacing "the sink count
emerges from concentration" with a measured band table. `claims-v5.md`, extracted by an agent with
no context, grades **164 delta claims — 90 REVISED and 74 NEW**, of which 52 are v5.0 text and 22
arrived in v4.0 and had nowhere to be recorded, since v4.0 never got a claims file. The NEW rows
concentrate exactly where v5.0 rewrote: 16 in §1.3's classification, 20 in §1.6's band table and
Europe demonstration.

So the honest form of v4.0's "0 propositions added that replace nothing" has **two** exceptions,
both found by extraction rather than by the author:

- **The fallback branch stands on no replaced predecessor.** V022's stall rule survives verbatim as
  Phase 3's first branch; v4.0 *appended* a second branch for a case no prior version's algorithm
  covered at all, and v5.0 built four propositions on top of it — where the branch is reachable, on
  which graphs, what decides there, and why that makes emitter node order a correctness requirement.
  Seven rows refine an **absence**, not a graded claim. That is a real addition and it is the one
  place in v5.0 where the document grew rather than being repaired.
- **"No new subject matter" is true of sections and false of facts.** Every section v5.0 touches,
  v4.0 already had. But **29 rows name EU4 facts no prior inventory carried**, 21 of them in §1.3 —
  great projects and the `starting_tier` rule, permanent province modifiers, centres of trade,
  `production_leader`, buildings at 1444, the static-modifier values, the Leviathan gate on
  `stora_kopparberget_modifier` — plus the three institutions' start dates and provinces in §1.6.
  Those facts are new because the whole-install sweep found them; the *claim they serve* is the one
  v4.0 got wrong.

Beyond those, the count of *rows* an extraction produces is a function of the granularity it is
asked for, not of how much new ground the document covers.

**Inputs.** `per-good-trade-spec.md` v4.0; the adversarial re-review of v4.0 (35 findings, run by an
agent with no prior context, deliberately including four findings against repairs v4.0 had just
made); a fresh pass over the 1.37.5.0 Inca install with Leviathan present; and the reference solver
with §1.3's classification applied to the whole install rather than to `common/tradegoods/` alone.

**Verification.** `scripts/validate_v5.py` re-derives **135 figures and text states** from the
install and the solver — 78 numeric re-derivations, 57 presence/absence assertions on the text that
changed. **135 checks, 0 failed.** That harness is the author's own, so it is evidence of internal
consistency and not an independent audit; the independent audit is `validation-v5.md`.

---

## What v5.0 changes, in one table

| Driver | Count | Where |
|---|---|---|
| v4.0 statements the re-review refuted outright | 12 | §0, §1.3, §1.6, §2.3, §3.2, §3.5, §3.9, §3.10, §1.10 |
| v4.0 statements narrowed to what is proved or measured | 9 | §1.1, §1.6, §2.2, §2.4, §2.8, §3.2, §3.13 |
| Wrong-source figures re-read from the shipped files | 5 | §1.7, §2.2, §2.8, §3.5, §3.10 |
| Figures regenerated on the corrected wealth field | 28 | §1.6, §2.4, §2.8, §3.2, §3.8, §3.9, §3.13, §3.15 |
| Stale `v4`/`v4measure.py` references swept | 5 | throughout |
| Figures the regeneration batch missed, caught by re-reading the saved run outputs | 2 | §2.9, §3.15 |
| Defects found by the no-context claims extraction of v5.0 itself | 6 | §1.6, §1.10, §2.8, §3.13, §3.15 |
| v5.0's own overstatements, refuted by stress-testing them at more seeds | 2 | §1.6, §2.3 |
| Defects found by the second no-context claims extraction | 3 | §1.10, §2.8, §3.9 |
| **Propositions standing on no replaced predecessor** | **7** | §1.1, §2.4, §2.8, §3.2 — the fallback branch and its consequences (see the note above the table) |

Four of the twelve refutations are against repairs **v4.0 itself introduced** — §3.10's "0.41%"
figure, §3.5's `change_price` census, §1.10's caravan comparison, and §2.3's calibration sentence.
That is the point of running the re-review with no context: v4.0's own harness was written by the
same author as v4.0's edits, so it could only confirm what it had been told to look for.

## What v5.0 withdraws outright

Nine prior claims are withdrawn rather than replaced — the spec states they are wrong, or deletes
them and puts nothing in their place. Five follow from the changes described below; the other four
are listed here because an independent extraction found them and this document did not:

| ID | The withdrawn claim | Where v5.0 withdraws it |
|---|---|---|
| **V213** | `α_Φ = 1.5` is calibrated to the two-sink 1444 map | §2.3 — "Its stated calibration is withdrawn" |
| **V215** | the installed map has two 1444 sinks, `hangzhou` and `english_channel` | §1.6 — one sink on the corrected field |
| **V224** | the sink count emerges from concentration | §1.6 — the count is a step function of `α_Φ` |
| **V117** | supply contrast 10⁷ drowns demand contrast 10²–10³ | §3.2 and now §3.15 — an artifact of v1's ε floor |
| **W130** | zero exact key ties, so the node index never decides | §1.1 and §3.2 — on the fallback branch the index alone decides |
| **W145** | three goods sit on the price-floor boundary, the likely origin of v2's off-by-one | §3.5 — v2's 13 was right, and there are **two** boundary goods (`gems`, `silk`) |
| **W158** | no 1444 province carries a flat goods bonus in the additive block | §1.3 — fifteen do |
| **W066** (half) | trade efficiency also feeds the caravan-power and collection tooltips | deleted in v4.0 for a `LEDGER_*` column argument; §1.7 deletes that argument too, so the "different quantities" claim now rests on the define's own shipped comment alone |
| **V217** (half) | `Φ_w` is "stabler than any per-good graph" | §1.6 keeps the ±1% noise measurement and drops the comparative, which was never measured against every per-good graph |

**W004** — v4.0's header claim that four v1 corrections v2 never applied are folded in — is not
withdrawn but is subsumed. §0's lineage paragraph still carries **V004** ("every claim-audit
correction from `../v1-laplacian/validation.md` settleable from files is folded in here"), which
entails it, v5.0's header states the fold-through over all four audits, and the corrections
themselves are untouched in the body. It is listed here because the first reading of this document
recorded it as a withdrawal and it is not one.

## The one change that moves every measured number

**§1.3's two tests are now applied to the whole install.** v4.0 stated the rule — a modifier is
*local* iff its value depends only on the province's own attributes, and it *enters wealth* iff it
modifies `goods_produced`, `price` or `tax_value` — and then swept only `common/tradegoods/`,
concluding "exactly two". Sweeping the install finds **sixteen more provinces**:

- **six great projects** whose `can_use_modifiers_trigger` is empty, contributing the
  `province_modifiers` accumulated to their `starting_tier`: `falun_copper_mine` (province 8),
  `krakow_cloth_hall` (262) and the four Grand Canal provinces (684, 1821, 1822, 2145);
- **ten provinces** carrying an `add_permanent_province_modifier` in the undated history block:
  `granary_of_the_mediterranean` (362, 363, 2316, 4316), `skanemarket` (6),
  `icelanding_fisher_sea` (370, 371), `diamond_mines_of_golconda_modifier` (542),
  `jingdezhen_kilns` (2151) and `coffea_arabica_modifier` (387).

World wealth is **10,677.50** annual ducats over 2,452 counted provinces, and the richest single
province in the game becomes 1821 at 30.40 — which is what moves the aggregate graph.

## The one change that is a design decision, not a correction

**The installed map has one sink at 1444, not two, and `α_Φ` stays at 1.5.** On v4.0's field the
`Φ_w` sinks were `hangzhou` and `english_channel`; on the corrected field they are `hangzhou` alone.
Three options were weighed:

1. **Keep α_Φ = 1.5 and report one sink.** Adopted.
2. **Retune α_Φ to recover two sinks.** Rejected: the `{english_channel, hangzhou}` result lives in
   a band 0.01 wide ([1.41, 1.42]) that moves or disappears entirely under ±1% wealth noise, while
   the wide bands move by ≤0.03. There is no honest constant to sit in it.
3. **Change the aggregate operator.** Rejected: it would reopen §3.9, which is settled on grounds
   that do not depend on the 1444 sink count.

The cost of option 1 is that §3.9's original adoption rationale — "two vanilla-like ends at 1444" —
is gone, so §3.9 now states the trade as what it is: 7.8 points of self-coherence given up for one
operator, one set of guarantees, and ends that move with the world. §2.3's claim that 1.5 was
"calibrated" to produce the two-sink map is withdrawn outright; 1.5 is **retained** because it sits
inside the widest sink-count band ([1.43, 1.93], width 0.50) and nothing now selects a different
value.

**The condition placed on adopting option 1 was that Europe must be able to become a sink**, since a
map whose only end is in China from 1444 to 1821 would not be a usable model of the period. It does,
with `α_Φ` fixed at 1.5 and nothing else moved (`scripts/europe.py`):

| Change to the world | `Φ_w` sinks |
|---|---|
| none (1444) | `hangzhou` |
| Europe's 823 counted provinces ×1.02 | `doab`, **`english_channel`**, `hangzhou`, `wien` |
| Europe ×1.56 | **`english_channel`**, **`rheinland`** — Asia holds none |
| the nine Lowland provinces alone ×1.20 | **`english_channel`**, `hangzhou` |
| ±2% *random* wealth noise, 3 seeds | `hangzhou` — unchanged |

A 1–2% European development edge is far below what the Renaissance, Colonialism and Printing Press
deliver over 1450–1550, and the Lowlands developing on their own — which the Netherlands does in
most games — is enough by itself. The map does not twitch under noise and it does move under
regional growth, which is the behaviour §3.1's first goal asks for.

The same run answers the second question put to it. **The 1444 map draws the pre-Columbian trade
geography unprompted**: Europe reaches the sink by the Silk Road
(`genua → alexandria → aleppo → persia → lahore → doab → ganges_delta → burma → gulf_of_siam →
canton → hangzhou`), by the Volga (`north_sea → white_sea → novgorod → kazan → astrakhan → persia`)
and by the Hansa and the Danube (`english_channel → lubeck → saxony → wien → venice → ragusa →
constantinople → aleppo`). Nothing routes through the Cape, which is correct for 1444 — and the Cape
is not idle either: in the per-good graphs it already carries Asian spices to Europe
(`malacca → cape_of_good_hope → zanzibar → gulf_of_aden → alexandria → genua`), with the spices sink
at `genua`. `Φ_w` models power, not cargo.

## The one change to the algorithm's stated properties

**§1.1's fallback branch gets a third counterexample and a wider containment set.** v4.0 added the
branch (promote the highest-wealth candidate when no candidate is a flow-terminal demander) but
still asserted §2.8's 2-core containment over `{selected} ∪ {promoted}`. **T3** — a triangle with
`b ≡ 0` and node wealth 3, 2, 1 — reaches the branch, produces a sink in neither set, and would
**halt the solver on correct behaviour**. §2.8 now asserts over
`{selected} ∪ {promoted} ∪ {fallbacks}`, §3.2 works T3 alongside T1 and T2, and §1.1 states where
the branch is reachable at all (`b ≡ 0` across a connected core). On 1444 it never fires — 0
fallbacks across 29/29 goods and `Φ_w` — so **no measured number moves because of it**.

T3 also settles §3.2's item 2. v4.0 claimed "zero exact key ties measured, so the index never
decides"; on the fallback branch the candidates are typically all zero-wealth, the wealth key ties,
and the node index alone decides the orientation. §2.4 item 1 therefore makes a canonical node order
a **correctness requirement**, not a convention.

---

## Every replacement, in the order applied

Each entry gives the section, what the replacement clears, the exact text removed, and the exact
text that replaced it. Entries 22–49 are figure regenerations on the corrected wealth field and
entries 50–54 are reference sweeps; they are listed in full for completeness but carry no argument.
Entries 66–68 are the second no-context extraction's findings: §2.8 was carrying the *unweighted*
agreement figure under the *value-weighted* label, §3.9's node-wealth ranks had never been
regenerated (they turn out to be unchanged on the corrected field, and now say so), and §1.10's
dismissal of the save's `highest_power` field said what it is not without saying how that was
established. Entries 64–65 correct an overstatement v5.0 itself introduced: the sentence dismissing v4.0's
two-sink α window said it "moves or disappears entirely" under ±1% noise, and at 8 seeds it
disappears on none of them — it shrinks to as little as a single sampled α. The weaker claim is the
true one and it is sufficient, and §2.3 carried the same overstatement. Entries 58–63 are the six defects the no-context extraction of `claims-v5.md` found in the v5.0
text — five of them a regenerated passage contradicting one that was not regenerated with it, and
one the extraction's only UNSOURCED row, replaced with a file value. Entries 56–57 are two figures
the regeneration batch missed — §2.9's copy of the coal-activation
flip count, and §3.15's gravity-kernel γ — found by re-reading `v5measure.out` and `phiw3.v5.out`
against the spec text after the batch had run.

