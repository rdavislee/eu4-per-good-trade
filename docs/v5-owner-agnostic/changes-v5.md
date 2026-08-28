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


### 1. `version` — §0

V5.0 banner

**Removed:**

```
**Version:** 4.0
```

**Replaced with:**

```
**Version:** 5.0
```

### 2. `v5-header` — §0

The fold-through claim

**Removed:**

```
**v4.0** keeps v3.0's three changes and closes the audit of them. (a) **Wealth is owner-agnostic**
— a property of the place, not of who holds it: no autonomy, no production efficiency, no ideas, no
owner modifiers (§1.3, §3.3). (b) Every refuted and partial claim in `../v2-drain/validation-v2.md`
**and** `../v3-owner-agnostic/validation-v3.md` is folded through — including the five
`validation-v2.md` partials v3.0 counted in its ledger but did not fold (§1.6, §1.8, §1.10, §2.2)
and four v1 corrections that v2 never applied. (c) The four game probes settled in
`../v2-drain/game-session.md` are applied, two of them reversing v2's stated position (§2.4, §1.9).
Deleted text is quoted in `changes-v4.md`. Every measured number carries the script that produced
it; anything not regenerated for v4.0 is marked **[unverified in v4.0]**.
```

**Replaced with:**

```
**v5.0** keeps the owner-agnostic wealth of v3.0 — a property of the place, not of who holds it:
no autonomy, no production efficiency, no ideas, no owner modifiers (§1.3, §3.3) — and folds through
every refuted and partial claim from all four audits to date, including v4.0's own. Its substantive
change is to §1.3: **the local-modifier classification is applied to the whole install rather than
to the trade-good tables alone**, which adds sixteen provinces and moves the aggregate graph from
two 1444 sinks to one (§1.6). Deleted text is quoted in `changes-v5.md`. Every measured number
carries the script that produced it; **no figure in v5.0 is unverified**, and the one place the
document declines to project a number says so in place.
```

### 3. `A1-A7` — §1.3

Changes 1-7: the classification table

**Removed:**

```
Applied to everything live on a 1444 province with no owner input:

| Modifier | Local? | Enters wealth? |
|---|---|---|
| `gems` `local_tax_modifier = 0.15` | yes, set by the province's good | **yes** — modifies `tax_value` |
| `incense` `trade_value_modifier = 0.1` | yes, set by the province's good | **yes** — modifies `trade_value` |
| `glass` `local_production_efficiency = 0.1` | yes, set by the province's good | no — modifies production *income*, which wealth does not compute |
| `chinaware` `local_autonomy = -0.1` | yes, set by the province's good | no — modifies local autonomy, which wealth does not compute |
| goods-produced efficiency from nearby merchant republics, trading cities and trade companies (`bonus_from_merchant_republics`, `eu4.exe:0x1cc7128`) | **no** — its value is set by which *neighbouring countries* hold those government forms | — |
| the owner's `global_trade_goods_size_modifier` (e.g. the `Industrious` ruler personality, +10%) | no — country-scoped | — |
| `terrain.txt` and the climate static modifiers | yes | no — they grant `allowed_num_of_buildings`, `defence`, `local_defensiveness`, `local_development_cost`, `movement_cost`, `nation_designer_cost_multiplier`, `supply_limit`, colonial growth and hostile attrition, none of which wealth computes |

So exactly **two** modifiers enter wealth in vanilla: `gems` on the tax term and `incense` on the
trade-value term. The reference solver applies both (§2.2 item 4). The two rows that are local but
do not enter — glass and chinaware — are the whole of the rule-versus-vocabulary tension: §1.3
excludes production efficiency and autonomy by name, and the second test excludes them again for the
same reason, so there is nothing left to decide.
```

**Replaced with:**

```
**The tests are applied to the whole install, not to one file.** v4.0 stated this rule and then
swept only `common/tradegoods/`, which is the mistake the rule exists to prevent: it concluded
"exactly two" and missed sixteen provinces. Applied to everything live on a 1444 province with no
owner input:

| Source | Local? | Enters wealth? |
|---|---|---|
| `gems` `local_tax_modifier = 0.15` (43 provinces) | yes, set by the province's good | **yes** — `tax_value` |
| `incense` `trade_value_modifier = 0.1` (29 provinces) | yes, set by the province's good | **yes** — `trade_value` |
| **Great-project `province_modifiers`** where `can_use_modifiers_trigger` is empty (6 provinces) | yes, the project is on the province | **yes** — `goods_produced` and `trade_value` |
| **`add_permanent_province_modifier` in the undated province-history block** (10 provinces) | yes, applied to the place at the start date | **yes** — `goods_produced` |
| `devastation` −2, `occupied` −0.5 and −0.5, `under_siege` −0.25, `prosperity` +0.25 (static modifiers) | yes, all are province state | **yes** — `goods_produced` and `tax_value`; all are zero at the 1444 start, and §1.2 and §3.3 both depend on them biting later |
| `glass` `local_production_efficiency = 0.1` | yes, set by the province's good | no — modifies production *income*, which wealth does not compute |
| `chinaware` `local_autonomy = -0.1` | yes, set by the province's good | no — modifies local autonomy, which wealth does not compute |
| **Centers of trade** (361 provinces carry one at 1444) | yes, CoT level is province state | no — no CoT level in `common/centers_of_trade/` grants any of the four keys wealth reads. A clean near-miss, recorded so it is not reopened |
| `production_leader` `trade_goods_size_modifier = 0.10` | **no** — which country leads a good's production is a country's state | — |
| goods-produced efficiency from nearby merchant republics, trading cities and trade companies (`bonus_from_merchant_republics`, `eu4.exe:0x1cc7128`) | **no** — set by which *neighbouring countries* hold those government forms | — |
| the owner's `global_trade_goods_size_modifier` (e.g. the `Industrious` ruler personality, +10%) | no — country-scoped | — |
| Buildings | yes by the test, and empty at 1444 — no province's start state carries a temple, workshop or manufactory | would be, if any existed |
| `terrain.txt` and the climate static modifiers | yes | no — they grant `allowed_num_of_buildings`, `defence`, `local_defensiveness`, `local_development_cost`, `movement_cost`, `nation_designer_cost_multiplier`, `supply_limit`, colonial growth and hostile attrition, none of which wealth computes |

**Great projects, in scope.** A project contributes the `province_modifiers` accumulated up to its
`starting_tier` when its `can_use_modifiers_trigger` is empty. Tiers reached after the start date
are owner spending and are out; so is any project whose trigger tests a country's culture, religion,
government or flags — 85 of the 130 live at 1444 are gated that way. That leaves six carrying a key
wealth reads: `falun_copper_mine` (province 8, `trade_goods_size` 3.0), `krakow_cloth_hall` (262,
`trade_goods_size_modifier` 0.10) and the four Grand Canal provinces (684, 1821, 1822, 2145;
`trade_goods_size` 0.5 and `trade_value_modifier` 0.1 each). Province 1821 is the richest single
province in the game. *The tier is the right line and "owner action" is not: development is an owner
action, so a rule excluding those would exclude `base_production`, which is wealth's primary input.*

**The ten permanent modifiers** are `granary_of_the_mediterranean` (362, 363, 2316, 4316),
`skanemarket` (6), `icelanding_fisher_sea` (370, 371), `diamond_mines_of_golconda_modifier` (542),
`jingdezhen_kilns` (2151) and `coffea_arabica_modifier` (387), all flat `trade_goods_size`.

**These figures are conditional on the DLC set.** `province_triggered_modifiers`'
`stora_kopparberget_modifier` is gated `NOT = { has_dlc = "Leviathan" }` and grants
`trade_goods_size = 5.0` on province 8 — the same province as `falun_copper_mine`. With Leviathan
the project applies and gives 3.0; without it the project does not exist and the modifier gives 5.0.
Every wealth figure in this document was measured with **Leviathan installed**, which is why §2.3
makes DLC state a third input axis rather than a footnote.

The two rows that are local but do not enter — glass and chinaware — are the whole of the
rule-versus-vocabulary tension: §1.3 excludes production efficiency and autonomy by name, and the
second test excludes them again for the same reason, so there is nothing left to decide.
```

### 4. `A3` — §1.3

Change 3: the flat-bonus denial

**Removed:**

```
**consistent with** that and does not establish it — it carries an additive `Base Goods Produced`
block (`Base Production: +0.80`) above a separate multiplicative `Goods Produced Efficiency` block,
and no 1444 province was observed carrying a flat bonus in the first block (§3.13).
```

**Replaced with:**

```
**consistent with** that and does not establish it — it carries an additive `Base Goods Produced`
block (`Base Production: +0.80`) above a separate multiplicative `Goods Produced Efficiency` block.
Fifteen 1444 provinces do carry a flat bonus in the first block (the table above), so the ordering
matters in practice and not only in principle.
```

### 5. `A8` — §2.2

Change 8-9: solver item 4

**Removed:**

```
4. Per-province `wealth` — **owner-agnostic** per §1.3:
   `TAX_COEFF · base_tax · (1 + local tax modifiers) + GP_COEFF · base_production · price ·
   (1 + local trade-value modifiers)`, and no autonomy, efficiency, ideas or owner terms. In vanilla
   the local modifiers that enter are exactly two — `gems` (+15% tax, 43 provinces) and `incense`
   (+10% trade value, 29 provinces) — and the reference solver applies both; v3.0 specified them and
   computed without them. Then per-node `trade_value`, `s`, `c` with per-province α, and the
   per-good balance `b = s − c`.
```

**Replaced with:**

```
4. Per-province `wealth` — **owner-agnostic** per §1.3:
   `TAX_COEFF · base_tax · (1 + local tax modifiers) + (GP_COEFF · base_production + local flat
   goods bonuses) · (1 + local goods-produced modifiers) · price · (1 + local trade-value
   modifiers)`, and no autonomy, efficiency, ideas or owner terms. The solver reads the local
   modifiers from §1.3's classification, applied to the whole install: in vanilla at 1444 that is
   `gems` (+15% tax, 43 provinces), `incense` (+10% trade value, 29 provinces), six great projects
   and ten permanent province modifiers — 16 provinces beyond the two trade goods. World wealth is
   **10,677.50** annual ducats over 2,452 counted provinces. Then per-node `trade_value`, `s`, `c`
   with per-province α, and the per-good balance `b = s − c`.
```

### 6. `B11` — §1.6

Change 11: delete the emergence claim

**Removed:**

```
the sinks are wherever the wealth flow terminates. Nothing pins their count; it emerges from
concentration exactly as per-good sink counts do.
```

**Replaced with:**

```
the sinks are wherever the wealth flow terminates. **Their count is set by `α_Φ`; only their
locations are emergent.** v2.0 through v4.0 said the count "emerges from concentration exactly as
per-good sink counts do" — it does not: `α_Φ` is a stipulated constant, the count is a step function
of it (the band table below), and the value was chosen with a target count in view. What the world
state moves is *where* the sinks are and *how the map drains toward them*, which is the property
§3.1's first goal actually asks for.
```

### 7. `B10-B12` — §1.6

Changes 10, 12, 16, 17, 18: the measured block

**Removed:**

```
Measured on 1444 data at α_Φ = 1.5 (`v4measure.py`): **two sinks, `hangzhou` and
`english_channel`**. Their ranks are 3 and 2 in the α_Φ-weighted wealth field `c_w` — *not* in raw
node wealth, where they are 12th and 1st; v2 wrote "wealth ranks" without saying which, and the
plain reading is wrong. Phase 1 selects `genua`, both sinks arrive by stall promotion, and `genua`
ends a transit node. **Eight sources**, all in the bottom half of the wealth field (`c_w` ranks
44–75, mean degree 3.1 against the map's 4.0 — v2 called them "cul-de-sacs", which their degrees
do not support). Every node drains to a sink; acyclic, 159/159 oriented, 0 fallbacks; **0 edge
flips and 0 sink-set changes under ±1% wealth noise across 5 seeds** — stabler than any per-good
graph. Its marking order is a per-node scalar whose descending comparison reproduces the DAG
(0 violations), so every consumer needing a potential still gets one.

Agreement with the per-good graphs is **53.5%** of edge-goods (52.5% value-weighted) against the
superseded `Φ_ord`'s **60.0%** — a gap of 6.5 points, not the 9.3 v2 quoted. v2's 62.7% was
measured under the *old scan-order sweep* and was never regenerated after §3.6 adopted the
deterministic one; 60.0% is the deterministic figure on v4.0's wealth field. That trade is recorded
in §3.9.

Dynamics, measured: dev-stacking `hangzhou`'s top province ×30 makes it the sole world sink
(also at ×20 and ×50; at ×10 the sink set is still three); scaling **the 22 European nodes'** wealth
×2 makes `genua` the sole sink; at ×3 the Cape of Good Hope **reverses** — 1444's
Atlantic→Cape→Indian-Ocean drainage becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast. *The
22 are the 18 western and central European nodes —* `english_channel`, `north_sea`, `baltic_sea`,
`white_sea`, `novgorod`, `lubeck`, `rheinland`, `saxony`, `wien`, `krakow`, `pest`, `venice`,
`ragusa`, `genua`, `champagne`, `bordeaux`, `valencia`, `sevilla` *— plus* `constantinople`,
`crimea`, `kiev` *and* `kazan`. *Both thresholds are set-dependent and land exactly under that
reading; under the 18-node set alone, sole-`genua` needs ×2.5 and the Cape reverses at ×2.* Sink
count breathes with concentration (transient extra sinks at intermediate boosts are expected
behaviour, not noise), and it is **non-monotone in α_Φ** — measured 5→2→1→2→3→1 across
α_Φ ∈ {1, 1.5, 2, 3, 4, 8} on 1444 (`v4measure.py`). The count tracks how many world-class wealth
poles the flow separates, not α_Φ itself.
```

**Replaced with:**

```
Measured on 1444 data at α_Φ = 1.5 (`v5measure.py`): **one sink, `hangzhou`** — rank 1 in the
α_Φ-weighted wealth field `c_w`, and rank 10 in raw node wealth, where `english_channel` is 1st.
*(v2 through v4 reported two sinks. That result was measured on a wealth field missing the sixteen
provinces §1.3 now carries; correcting the field removes it. v2 also wrote "wealth ranks" without
saying which, and the plain reading was wrong then too.)* Phase 1 selects `hangzhou` directly, so
there are **0 promotions and 0 fallbacks** — the self-correction never fires on this input. **Seven
sources** — `kongo`, `patagonia`, `james_bay`, `mississippi_river`, `chengdu`, `australia`, `tunis`
— all in the bottom half of the wealth field (`c_w` ranks 52–79, mean degree 3.0 against the map's
4.0; v2 called them "cul-de-sacs", which their degrees do not support). Every node drains to the
sink; acyclic, 159/159 oriented; **0 edge flips and 0 sink-set changes under ±1% wealth noise across
5 seeds**. Its marking order is a per-node scalar whose descending comparison reproduces the DAG
(0 violations), so every consumer needing a potential still gets one.

Agreement with the per-good graphs is **52.5%** of edge-goods (51.5% value-weighted) against the
superseded `Φ_ord`'s **60.3%** — a gap of 7.8 points. v2's 62.7% was measured under the *old
scan-order sweep* and was never regenerated after §3.6 adopted the deterministic one. That trade is
recorded in §3.9.

**The sink count is a step function of `α_Φ`.** Measured across α_Φ = 1.00…3.00 at 0.01:

| sinks | α_Φ band | width |
|---|---|---|
| 1 — `hangzhou` | **[1.43, 1.93]** | **0.51** — the widest band on this field, and the one α_Φ = 1.5 sits in |
| 3 — `doab`, `genua`, `hangzhou` | [2.26, 2.71] | 0.46 |
| 2 — `genua`, `hangzhou` | [1.94, 2.25] | 0.32 |
| 2 — `english_channel`, `hangzhou` | [1.41, 1.42] | 0.02 |

The last row is v4.0's result and it is **not reproducible**: under ±1% wealth noise that window
moves or disappears entirely, while the wide bands move by ≤0.03. It is not a band, so no constant
could honestly sit in it. `α_Φ` is **retained at 1.5** because it sits inside the widest band and
nothing now selects a different value — not because it was derived (§2.3). Sampled at the six values
v2 used, the count is non-monotone: **5 → 1 → 2 → 4 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}.

**One sink at 1444 is a snapshot, not a fixed feature, and the map says so under load.** Holding
α_Φ = 1.5 and moving nothing else (`europe.py`):

- **A 1–2% European development edge produces a European sink.** At ×1.02 across Europe's 823
  counted provinces the sinks are `{doab, english_channel, hangzhou, wien}`; `english_channel` is a
  sink at every larger factor tested. At ×1.56 the sinks are `{english_channel, rheinland}` and Asia
  holds none. That range is far below what the Renaissance, Colonialism and Printing Press deliver
  over 1450–1550.
- **The Lowlands alone suffice.** Developing only the nine Lowland provinces in `english_channel`
  (Holland, Zeeland, Vlaanderen, Brabant, Antwerpen, Utrecht, Gelre, Friesland, Breda) by ×1.20
  makes `english_channel` a sink beside `hangzhou`, and it stays one through ×10.
- **Robust to noise, responsive to growth.** ±2% *random* wealth noise leaves the 1444 sink set
  unchanged on three seeds; **+2% applied systematically to Europe alone changes it**. The map does
  not twitch, and it does move.

**And the 1444 map draws the pre-Columbian trade geography unprompted.** The route from Europe to
the sink is the Silk Road: `genua → alexandria → aleppo → persia → lahore → doab → ganges_delta →
burma → gulf_of_siam → canton → hangzhou`. From the north it is the Volga:
`north_sea → white_sea → novgorod → kazan → astrakhan → persia → …`. From the Channel it is the
Hansa and the Danube: `english_channel → lubeck → saxony → wien → venice → ragusa →
constantinople → aleppo → …`. Nothing routes through the Cape, which is what a 1444 map should
say. *(The Cape is not idle — in the per-good graphs it already carries Asian spices to Europe:
`malacca → cape_of_good_hope → zanzibar → gulf_of_aden → alexandria → genua`. `Φ_w` models power,
not cargo; §3.9.)*

Other dynamics, measured: scaling **the 22 European nodes'** wealth ×2 makes `genua` the sole sink;
between **×3 and ×3.75** the Cape of Good Hope **reverses** — 1444's Atlantic→Cape→Indian-Ocean
drainage becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast — and outside that window it does
not, so the reversal is a band and not a threshold. *The 22 are the 18 western and central European
nodes —* `english_channel`, `north_sea`, `baltic_sea`, `white_sea`, `novgorod`, `lubeck`,
`rheinland`, `saxony`, `wien`, `krakow`, `pest`, `venice`, `ragusa`, `genua`, `champagne`,
`bordeaux`, `valencia`, `sevilla` *— plus* `constantinople`, `crimea`, `kiev` *and* `kazan`; under
the 18-node set alone sole-`genua` needs ×2.5. Dev-stacking `hangzhou`'s top province keeps it the
sole sink at ×20, ×30 and ×50, with a transient split into three at ×10 — extra sinks at
intermediate boosts are expected behaviour, not noise.
```

### 8. `B-scale` — §1.6

Change 16: the scale figures

**Removed:**

```
×1 and above, 13 edge flips at ×10⁻², and at ×10⁻⁶ the sink set collapses to a single node.
Normalising into (−1, 1) scales 1444's `b_w` *up* (its largest magnitude is 0.0225) and is safe;
```

**Replaced with:**

```
×1 and above, 16 edge flips at ×10⁻², and 83 at ×10⁻⁶ — the orientation degrades while the sink
set happens to survive, so the sink set is not the quantity to watch here.
Normalising into (−1, 1) scales 1444's `b_w` *up* (its largest magnitude is 0.0227) and is safe;
```

### 9. `B13` — §2.3

Change 13: the calibration sentence

**Removed:**

```
the aggregate-graph exponent `α_Φ = 1.5` (calibrated so the 1444 start yields the two-sink
hangzhou/english_channel map, §1.6 — a constant like `P₀`; world-responsiveness flows through
wealth, never through this knob),
```

**Replaced with:**

```
the aggregate-graph exponent `α_Φ = 1.5` (a constant like `P₀`; world-responsiveness flows through
wealth, never through this knob). **Its stated calibration is withdrawn.** v2.1 through v4.0 said
1.5 was "calibrated so the 1444 start yields the two-sink hangzhou/english_channel map"; on the
corrected wealth field of §1.3 it does not yield that map, and the map it was fitted to is not
reproducible under noise (§1.6). 1.5 is retained because it sits inside the widest sink-count band
and nothing now selects a different value — not because it was derived. Any future change to it is
a design decision about how many ends the installed graph should have, and should be recorded as
one,
```

### 10. `B14` — §3.9

Change 14: the adoption rationale

**Removed:**

```
- `Φ_w`, adopted: two vanilla-like ends at 1444 that move with the world, from the same operator
  the goods already use.
```

**Replaced with:**

```
- `Φ_w`, adopted: **one operator, one set of guarantees, and ends that move with the world.** It
  reuses §1.1 unchanged, so LP feasibility, acyclicity, determinism and scan-invariance come for
  free and the correctness check stays a single combinatorial comparison; and its ends are places
  the wealth actually is, so they move when the wealth moves (§1.6's institution result). *v2.1
  through v4.0 justified the adoption by "two vanilla-like ends at 1444" — the reason it was
  accepted despite losing self-coherence. On the corrected wealth field there is one end, in China,
  matching none of vanilla's three, so that premise is withdrawn. The trade is now stated as what it
  is: 7.8 points of self-coherence given up for one operator and world-responsive ends, and the
  1444 count is whatever the field gives.*
```

### 11. `C19-C21` — §3.2

Changes 19-21: 3.2 claim 1

**Removed:**

```
1. **Sink placement:** on a map where Phase 0 is a no-op, final sinks =
   `{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal demanders}` — measured exact,
   29/29 goods. **This is a measurement, not a theorem**, and v2 asserted it as a theorem. Two
   constructed inputs break it, both run through a faithful implementation of §1.1:
   - **T1 — pendant importer.** Triangle A(+5), B(−3), D(0) with a leaf C(−2) on B. Phase 0 peels C,
     Phase 4 restores the edge B→C, and the actual sinks are `{C}` while the formula set is `{B}`.
     The pendant is a sink outside the set **and** it strips the selected sink of its sinkhood.
   - **T2 — free-edge race, inside the 2-core.** Five-cycle S1(+3)–u1(−3)–w(0)–u2(−2)–S2(+2)–S1 with a
     chord w–S1. Both u1 and u2 are selected flow-terminal demanders. Under the adopted
     DEF-ascending key u2 pops first, the conduit w becomes ready via its free edge to u2 and pops
     before u1, so the free edge orients u1→w and u1 is no longer a sink. Actual `{u2}`, formula
     `{u1, u2}`.

   What survives unconditionally is the ⊆-direction *within the 2-core*: every core node that is
   neither selected nor promoted is given an out-arc by the sweep, either a flow arc or a free
   edge to an earlier-marked node. Pendant net-importers are the only sinks outside the set, and
   the free-edge race is the only way a node inside it drops out. §2.8 therefore carries **two**
   runtime checks rather than one weakened one: containment inside the 2-core is asserted
   unconditionally every tick, and the equality is *monitored* every tick with T2 named as its
   legitimate failure. On pendant edges the Phase-4 orientation rule is the check and T1 is
   expected output. Written as a single assertion with an escape clause, both counterexamples
   would disappear into the clause.
```

**Replaced with:**

```
1. **Sink placement:** on a map where Phase 0 is a no-op and no fallback fires, final sinks =
   `{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal demanders}` — measured exact,
   29/29 goods. **This is a measurement, not a theorem**, and v2 asserted it as a theorem. Three
   constructed inputs break it, all run through a faithful implementation of §1.1 (`toys.py`):
   - **T1 — pendant importer.** Triangle A(+5), B(−3), D(0) with a leaf C(−2) on B. Phase 0 peels C,
     Phase 4 restores the edge B→C, and the actual sinks are `{C}` while the formula set is `{B}`.
     The pendant is a sink outside the set **and** it strips the selected sink of its sinkhood.
   - **T2 — free-edge race, inside the 2-core.** Five-cycle S1(+3)–u1(−3)–w(0)–u2(−2)–S2(+2)–S1 with a
     chord w–S1. Both u1 and u2 are selected flow-terminal demanders. Under the adopted
     DEF-ascending key u2 pops first, the conduit w becomes ready via its free edge to u2 and pops
     before u1, so the free edge orients u1→w and u1 is no longer a sink. Actual `{u2}`, formula
     `{u1, u2}`.
   - **T3 — the fallback branch, inside the 2-core.** Triangle A, B, C with `b = 0` at all three and
     node wealth 3, 2, 1. No node is a demander, so Phase 1 selects nothing; there is no flow, so
     every edge is free; no node is ready, so the sweep stalls with no flow-terminal demander and
     the fallback promotes A. Free edges then orient B→A, C→A, C→B. Actual sinks `{A}`, formula set
     empty — and A is in neither `{selected}` nor `{promoted}`.

   What survives unconditionally is the ⊆-direction *within the 2-core*, over the set the sweep
   actually maintains: every core node that is neither selected, promoted **nor fallback-promoted**
   is given an out-arc by the sweep, either a flow arc or a free edge to an earlier-marked node.
   Pendant net-importers are the only sinks outside that set. §2.8 therefore carries **two** runtime
   checks rather than one weakened one: containment inside the 2-core is asserted unconditionally
   every tick against `{selected} ∪ {promoted} ∪ {fallbacks}`, and the equality is *monitored* every
   tick with **T2 and T3** named as its legitimate failures. On pendant edges the Phase-4
   orientation rule is the check and T1 is expected output. Written as a single assertion with an
   escape clause, all three counterexamples would disappear into the clause — and written against
   the narrower containment set, T3 would halt the solver on correct behaviour.
```

### 12. `C22` — §3.2

Change 22: 3.2 item 2's index claim

**Removed:**

```
2. **Free-edge direction:** marking order under the (DEF asc, b asc, index) priority — a function
   of the graph and the balances; zero exact key ties measured, so the index never decides.
```

**Replaced with:**

```
2. **Free-edge direction:** marking order under the (DEF asc, b asc, index) priority. This is
   **deterministic** by construction; that it is a function of the graph and the balances *alone* —
   that the node indexing never decides — is **measured, not proved**, and holds where the key has
   no exact ties: zero exact `(DEF, b)` ties on free edges, 29/29 goods on 1444. The one place the
   indexing is load-bearing is the fallback branch (T3 above), where the candidates are typically
   all zero-wealth and tied; §2.4 item 1 makes a canonical node order a correctness requirement for
   that reason.
```

### 13. `C23` — §1.1

Change 23: the fallback's reachability

**Removed:**

```
the **highest-wealth** candidate instead, ties by index: that is the **fallback** branch, it is what
a pocket with no net demander needs, and node wealth is a good-independent input so it needs no
bootstrap. (*Candidates* at a stall are the unmarked nodes whose flow out-neighbours are all marked;
the flow subgraph is acyclic, so at least one always exists and the sweep always advances.) Free
```

**Replaced with:**

```
the **highest-wealth** candidate instead, ties by index: that is the **fallback** branch, and node
wealth is a good-independent input so it needs no bootstrap. (*Candidates* at a stall are the
unmarked nodes whose flow out-neighbours are all marked; the flow subgraph is acyclic, so at least
one always exists and the sweep always advances.) **Where this branch is reachable, and what decides
there.** A candidate carrying any flow out-arc is already *ready*, and a candidate with inflow is a
flow-terminal demander, so the fallback fires only when every candidate is support-isolated with
zero balance — on a connected core, only when `b ≡ 0` across it. That happens for the aggregate
graph on a uniform-wealth map, and for a per-good graph on a component with no producer and no
consumer. In those cases the candidates are usually all *zero-wealth*, the wealth key ties, and the
**index decides** — which is why §2.4 item 1 makes a canonical emitter node order a correctness
requirement rather than a convention, and why §2.8 asserts containment over a set that includes the
fallbacks. Free
```

### 14. `C24` — §2.4

Change 24: 2.4 item 1

**Removed:**

```
1. **Declaration order** — emit in decreasing `Φ_w` marking order. This is the convention the
   engine states and the shipped vanilla file follows (0 of 159 links violate it), and violating
   it is non-fatal but logs one error per link.
```

**Replaced with:**

```
1. **Declaration order** — emit in decreasing `Φ_w` marking order. This is the convention the
   engine states and the shipped vanilla file follows (0 of 159 links violate it), and violating
   it is non-fatal but logs one error per link. **The node order itself is a correctness
   requirement, not a convention**: §1.1's priority key breaks exact ties by node index, and on the
   fallback branch (§3.2, T3) the wealth key ties and the index alone decides the orientation. The
   emitter must therefore fix one canonical node order and keep it stable across rebuilds, or the
   same world can produce two different maps.
```

### 15. `D25-D29` — §3.10

Changes 25-29: the identity and per-good propagation

**Removed:**

```
This is an **identity, not a measurement**: `powershare_C(n)` carries no `g`, so it factors out of the sum, and by §1.1's vocabulary the property is true by construction and carries no measurement. What a run can show is only that the implementation does the algebra in doubles — on `gulf_of_siam`, with 13 goods carrying local value, 12 of them sinking there, transfer eligibility varying per good and the off-home penalty on two of the three collectors, the two forms agree to a worst relative disagreement of **1.3e-16**, one unit in the last place. So one scalar per node reproduces every country's income exactly, and the engine's own math does the rest. *(v1 through v3.0 quoted "agreement to 5.7e-14" here, and 1.4e-14 below. Both are floating-point residuals of an exact identity, produced by a construction none of those documents states — a theorem decorated with an experiment, which is the confusion §1.1 exists to prevent.)*
```

**Replaced with:**

```
This is an **identity, not a measurement**: `powershare_C(n)` carries no `g`, so it factors out of the sum, and by §1.1's vocabulary the property is true by construction and carries no measurement. Every term that feeds a collector's power at a node is node-wide — the merchant bonus, the off-home penalty, propagation off the one installed graph, the caravan grant — so none of them can reintroduce a `g`. What a run can show is only that the implementation does the algebra in doubles: across Sevilla, Genoa, Champagne, Malacca and the Gulf of Siam, using each node's real 1444 country table, the two forms agree to a worst relative disagreement of **0 to 3.7e-16** — at most one unit in the last place. So one scalar per node reproduces every country's income exactly, and the engine's own math does the rest. *(v1 through v4.0 quoted "agreement to 5.7e-14" here, and 1.4e-14 below. Both are floating-point residuals of an exact identity, produced by constructions none of those documents states — a theorem decorated with an experiment, which is the confusion §1.1 exists to prevent.)*
```

### 16. `D26-D28` — §3.10

Changes 26-28: the per-good propagation magnitude and cause

**Removed:**

```
**This is also why propagation cannot be made per good.** Reading the one installed graph leaves the propagated term good-independent, so the identity survives it untouched — same construction, worst relative disagreement **1.3e-16**. Per-good propagation destroys it, because §1.9 reads a node's *downstream neighbours* and those are per good: `gulf_of_siam` has **eight distinct downstream sets across the 29 goods** — twelve goods leave it with none at all, five drain to `burma`, four to `{burma, canton, malacca}` — against `Φ_w`'s single `{canton}`. A country's power at the node stops being one number and `powershare_C` stops factoring out. Measured on the same construction: the node-scalar model then overstates **every** collector's income by **0.41%**, a total of 0.40 ducats on a node collecting 97.1. That is thirteen orders of magnitude above the float residual and it is a systematic bias in one direction, not rounding. Keeping propagation on a single graph is load-bearing for Goal 7, not merely convenient.
```

**Replaced with:**

```
**This is also why propagation cannot be made per good.** Reading the one installed graph leaves the propagated term good-independent, so the identity survives it untouched — same construction, worst relative disagreement 0 to 3.7e-16. Per-good propagation destroys it, because §1.9 reads a node's *downstream neighbours* and those differ per good. The driver is **not** how many distinct downstream sets a node has, but whether its collectors hold **differing power across the nodes those sets differ on**: `gulf_of_siam` has eight distinct downstream sets and still shows a 0.003% effect, because its collectors hold almost nothing in `burma`, `canton` or `malacca` and every propagation term is near zero. Where the collectors do hold differing power downstream, a country's power at the node stops being one number and `powershare_C` stops factoring out. Measured with each node's real 1444 country table and `collect_pool` built per good throughout: the error is **redistributive and single-digit percent, with the sign varying by collector** — Sevilla −0.82%, −0.87%, **+7.44%**; Champagne −1.69%, +1.69%, +1.53%; Genoa −0.23%, −0.22%, +0.70%. It is not a bias in one direction and it is not rounding: it is thirteen orders of magnitude above the float residual and it moves income between countries. Its size depends on which countries are collecting, which is a stated choice of the construction and not a property of the node, so no single percentage is quoted as one. Keeping propagation on a single graph is load-bearing for Goal 7, not merely convenient. *(v1 through v4.0 quoted "off by 5.96 ducats on a node paying ~250"; no node in the model has local trade value near 250 — the largest is 112.6 — and v4.0's own replacement figure, 0.41%, was an artifact of freezing one term at the alphabetically first commodity.)*
```

### 17. `E30` — §1.10

Change 30: the caravan comparison

**Removed:**

```
(median 17.9% over the 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`), against a largest single incumbent holder of 9.6 to 20.7 — so one country at the cap outweighs every incumbent in every inland node.
```

**Replaced with:**

```
(median 17.9% over the 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`), against a largest single incumbent holder of **23.6 to 143.2** — so a country at the cap outweighs the largest incumbent in **7 of the 26** inland nodes and is outweighed in the other 19. *(v4.0 read the save's `highest_power` field, 9.6–20.7, as the largest incumbent's power. It is not, and the conclusion drawn from it inverted.)*
```

### 18. `E31` — §3.5

Change 31: the price-scan census

**Removed:**

```
(All **154** `change_price` blocks were parsed — 93 in `events/`, 7 in `missions/`, 1 in `common/`
and **53 in `history/`, of which 13 are negative**, all in `history/countries/HAB - Austria.txt`.
```

**Replaced with:**

```
(All **161** `change_price` blocks were parsed — 93 in `events/`, 14 in `missions/`, 1 in `common/`
and **53 in `history/`, of which 13 are negative**, all in `history/countries/HAB - Austria.txt`.
v4.0 said 154 and 7: its parser silently recovered nothing from five mission files, which a bare
`except` hid, so the scan is now guarded by a per-file count assertion. The seven recovered blocks
are all positive and the partition is unchanged.
```

### 19. `E32` — §2.8

Change 32: the deterministic-field count

**Removed:**

```
`retention` is identical on 80 of 80 nodes and `total` on 79 of 79, the exception drifting 0.012%
```

**Replaced with:**

```
`retention` is identical on 80 of 80 nodes and `total` on 78 of 79, the exception — `zambezi` —
drifting 0.012%
```

### 20. `E34` — §2.2

Change 34: the solve-cost range

**Removed:**

```
**5.7–7.3 ms per good and 0.17–0.21 s for all 29**. "Milliseconds each" therefore holds already,
```

**Replaced with:**

```
**0.17–0.21 s for all 29 goods, a mean of 5.7–7.3 ms per good across runs** — individual goods
range 5.4–24 ms, so 7.3 is an average and not a maximum. "Milliseconds each" therefore holds
already,
```

### 21. `E35` — §1.7

Change 35: the ledger clause

**Removed:**

```
trade efficiency and a flat income bonus are different quantities in EU4 — separate modifier keys with separate ledger columns (`LEDGER_TRADE_EFFICIENCY`, `LEDGER_TC_EFF_CARAVAN_POWER`), granted separately where both appear together — and the define's own comment says income.*
```

**Replaced with:**

```
trade efficiency and a flat income bonus are different quantities in EU4, and the define's own shipped comment settles which this one is: `TRADE_MERCHANT_PRESENT = 0.1,  -- bonus on income if trade present`.*
```

### 22. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
29/29 goods on 1444, 1–8 sinks per
  good, mean 3.6, zero fallbacks
```

**Replaced with:**

```
29/29 goods on 1444, 1–7 sinks per
  good, mean 3.6, zero fallbacks
```

### 23. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
(§1.1) — 1 to 8 per good
```

**Replaced with:**

```
(§1.1) — 1 to 7 per good
```

### 24. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
flips **10 of
159 `Φ_w` edges** (`v4measure.py`)
```

**Replaced with:**

```
flips **29 of
159 `Φ_w` edges** (`v5measure.py`)
```

### 25. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
sinks at 14.1% in the top demand decile vs 6.9%
```

**Replaced with:**

```
sinks at 14.5% in the top demand decile vs 6.9%
```

### 26. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
cloves at Venice, Kongo, Australia, Brazil
```

**Replaced with:**

```
cloves at Venice, Kongo, Deccan, Australia, Brazil
```

### 27. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
and it is **cloves** that moves to Beijing
```

**Replaced with:**

```
and it is **cloves** that moves to Deccan
```

### 28. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
`genua` becomes a co-sink at ×1.726
```

**Replaced with:**

```
`genua` becomes a co-sink at ×1.720
```

### 29. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
needs **3.6–4.7×**
```

**Replaced with:**

```
needs **3.6–4.9×**
```

### 30. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
i.e. **9.5–21.4%** of all world
```

**Replaced with:**

```
i.e. **9.3–21.4%** of all world
```

### 31. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
(`beijing` 3.59× / 9.5%, `hangzhou` 4.13× / 21.4%, `xian` 4.57× / 12.3%,
`canton` 4.74× / 17.6%; the four China-region nodes outside that set — `girin`, `yumen`, `chengdu`,
`lhasa` — need 3.9× to 10.6×)
```

**Replaced with:**

```
(`beijing` 3.60× / 9.3%, `hangzhou` 3.83× / 21.4%, `xian` 4.59× / 12.3%,
`canton` 4.86× / 17.8%; the four China-region nodes outside that set — `girin`, `yumen`, `chengdu`,
`lhasa` — need 4.0× to 10.8×)
```

### 32. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
is 36 against a demand ratio of 471.5
```

**Replaced with:**

```
is 36 against a demand ratio of 482.2
```

### 33. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
measured, **90.6%** (5723 of 6320)
```

**Replaced with:**

```
measured, **92.2%** (5825 of 6320)
```

### 34. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
The argument is unaffected — 90.6% is still most of the map
```

**Replaced with:**

```
The argument is unaffected — 92.2% is still most of the map
```

### 35. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
free and remains the most self-coherent aggregate measured: **60.0%** edge-good agreement with
  the per-good graphs against `Φ_w`'s 53.5% (52.5% value-weighted).
```

**Replaced with:**

```
free and remains the most self-coherent aggregate measured: **60.3%** edge-good agreement with
  the per-good graphs against `Φ_w`'s 52.5% (51.5% value-weighted).
```

### 36. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
grounds: its ends are artifacts of sweep scheduling rather than places — of its 18 end nodes at
  1444, 10 terminate no good at all
```

**Replaced with:**

```
grounds: its ends are artifacts of sweep scheduling rather than places — of its 13 end nodes at
  1444, 8 terminate no good at all
```

### 37. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
count **never concentrates**: 13–22 ends measured across cloves-α 2…64
```

**Replaced with:**

```
count **never concentrates**: 11–17 ends measured across cloves-α 2…64
```

### 38. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
a quantity that ranges 13–22 nor a band containing its own baseline of 18
```

**Replaced with:**

```
a quantity that ranges 11–17 nor a band containing its own baseline of 13
```

### 39. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
spearman(price, sinks) = −0.53
```

**Replaced with:**

```
spearman(price, sinks) = −0.20
```

### 40. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
not <0.03% — and drops **silk** to 99.97% reach and cloves to 99.996%
```

**Replaced with:**

```
not <0.03% — and drops **cloves** to 99.97% reach
```

### 41. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
up to about **0.15%** of a good's mass in total
```

**Replaced with:**

```
up to about **0.18%** of a good's mass in total
```

### 42. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
most self-coherent aggregate measured (**60.0%** vs `Φ_w`'s 53.5%)
```

**Replaced with:**

```
most self-coherent aggregate measured (**60.3%** vs `Φ_w`'s 52.5%)
```

### 43. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
The ceiling is 60.0%, not the 62.7%
```

**Replaced with:**

```
The ceiling is 60.3%, not the 62.7%
```

### 44. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
(ρ_val +0.283 against DRAIN's +0.055; 46.6% of top-decile nodes
are sinks against 14.1%)
```

**Replaced with:**

```
(ρ_val +0.281 against DRAIN's +0.054; 43.8% of top-decile nodes
are sinks against 14.5%)
```

### 45. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
every route — 83.3% of demand reachable, 34 orphan sinks
```

**Replaced with:**

```
every route — 83.0% of demand reachable, 31 orphan sinks
```

### 46. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
It also posts **9 net-producer sinks**
```

**Replaced with:**

```
It also posts **8 net-producer sinks**
```

### 47. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
and 11–17
sinks per good against DRAIN's 1–8
```

**Replaced with:**

```
and 10–16
sinks per good against DRAIN's 1–7
```

### 48. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
supply→seed path; 88.6% reach at its best tuning
```

**Replaced with:**

```
supply→seed path; 88.4% reach at its best tuning
```

### 49. `regen`

Figure regenerated on the v5 wealth field

**Removed:**

```
with **66%** vanilla-arrow agreement at its best
(γ = 0.97, 105 of 159 arrows)
```

**Replaced with:**

```
with **61%** vanilla-arrow agreement at its best
(γ = 0.97, 97 of 159 arrows)
```

### 50. `sweep`

V4->v5 reference and count

**Removed:**

```
(`drain-orientation.md`; regenerated for v4.0 by `v4measure.py`)
```

**Replaced with:**

```
(`drain-orientation.md`; regenerated for v5.0 by `v5measure.py`)
```

### 51. `sweep`

V4->v5 reference and count

**Removed:**

```
2. **End flags** — `end=yes` on every `Φ_w` sink (1444: two end nodes, `hangzhou` and
   `english_channel`, against vanilla's three); stripped from any former end node that gains outgoing links.
```

**Replaced with:**

```
2. **End flags** — `end=yes` on every `Φ_w` sink (1444: **one** end node, `hangzhou`, against
   vanilla's three); stripped from any former end node that gains outgoing links. The count is not
   fixed — it follows the wealth field and `α_Φ` (§1.6), so the emitter reads it from the solve
   rather than assuming a number.
```

### 52. `sweep`

V4->v5 reference and count

**Removed:**

```
  Beijing, **demand rank 2** under α = 16 with the rank-1 demander `hangzhou` acting as a transit
  node, becomes the cloves sink; v2 said Beijing "holds the richest single province", which it
  does not — that is `hangzhou`, at 27.0 against Beijing's 19.5), 
```

**Replaced with:**

```
  Deccan, **demand rank 2** under α = 16 with the rank-1 demander `hangzhou` acting as a transit
  node, becomes the cloves sink; v2 said Beijing "holds the richest single province", which it
  does not — that is `hangzhou`, at 30.4 against Beijing's 19.5, and under this calibration Beijing
  is only demand rank 3), 
```

### 53. `sweep`

V4->v5 reference and count

**Removed:**

```
**Open in the v4.0 wealth model.**
```

**Replaced with:**

```
**Open in the v5.0 wealth model.**
```

### 54. `sweep`

V4->v5 reference and count

**Removed:**

```
no measurement in this project supports a specific projection **[unverified in v4.0]**.
```

**Replaced with:**

```
no measurement in this project supports a specific projection, and none is offered.
```

### 55. `F55` — §1.6

Band widths: max-min, not the inclusive sample count

**Removed:**

```
| 1 — `hangzhou` | **[1.43, 1.93]** | **0.51** — the widest band on this field, and the one α_Φ = 1.5 sits in |
| 3 — `doab`, `genua`, `hangzhou` | [2.26, 2.71] | 0.46 |
| 2 — `genua`, `hangzhou` | [1.94, 2.25] | 0.32 |
| 2 — `english_channel`, `hangzhou` | [1.41, 1.42] | 0.02 |
```

**Replaced with:**

```
| 1 — `hangzhou` | **[1.43, 1.93]** | **0.50** — the widest band on this field, and the one α_Φ = 1.5 sits in |
| 3 — `doab`, `genua`, `hangzhou` | [2.26, 2.71] | 0.45 |
| 2 — `genua`, `hangzhou` | [1.94, 2.25] | 0.31 |
| 2 — `english_channel`, `hangzhou` | [1.41, 1.42] | 0.01 |
```

### 56. `F56` — §2.8

2.9's coal row still carried v4.0's flip count

**Removed:**

```
Measured: repricing the 45 owned latent-coal provinces flips 10 of 159 `Φ_w` edges |
```

**Replaced with:**

```
Measured: repricing the 45 owned latent-coal provinces flips 29 of 159 `Φ_w` edges (§1.5) |
```

### 57. `F57` — §3.15

3.15's gravity-kernel end counts at gamma = 0.9

**Removed:**

```
demanders hits any chosen end count exactly for γ ≤ 0.7 and any count up to six — at γ = 0.9 the
five- and six-mass fields both give four ends — with **61%** vanilla-arrow agreement at its best
(γ = 0.97, 97 of 159 arrows).
```

**Replaced with:**

```
demanders hits any chosen end count exactly for γ ≤ 0.7 and any count up to six — at γ = 0.9 the
four-, five- and six-mass fields all collapse to three ends — with **61%** vanilla-arrow agreement
at its best (γ = 0.90–0.95, 97 of 159 arrows; γ = 0.97 gives 93, and every larger γ is worse).
*v2.1 through v4.0 put the best agreement at γ = 0.97 and said the five- and six-mass fields give
four ends at γ = 0.9; on the corrected wealth field neither holds.*
```

### 58. `G58` — §3.13

3.13 still carried the flat-goods denial 1.3 refutes

**Removed:**

```
(out, its value set by neighbouring countries' government forms) — and no 1444 province was
  observed carrying a *flat* `trade_goods_size` in the additive block. What is unenumerated is the
```

**Replaced with:**

```
(out, its value set by neighbouring countries' government forms) — and §1.3's whole-install sweep
  settles the additive block too: **fifteen** 1444 provinces carry a flat `trade_goods_size`, five
  from great projects and ten from permanent province modifiers. What is unenumerated is the
```

### 59. `G59` — §2.8

2.8's Razed-China row was still on the v4.0 wealth field

**Removed:**

```
| Razed China | Zeroing `hangzhou`-node development relocates the sink in one solve — measured: the `Φ_w` sinks move from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`. `hangzhou`, not `beijing`, is China's wealth pole under §1.3: it is a `Φ_w` sink, `c_w` rank 3, node-wealth rank 12, and holds the richest single province in the game. Zeroing `beijing` (node-wealth rank 39) moves nothing |
```

**Replaced with:**

```
| Razed China | Zeroing `hangzhou`-node development relocates the sink in one solve — measured: the `Φ_w` sinks move from `{hangzhou}` to `{doab, english_channel, gulf_of_siam, sevilla}`, 22 of 159 edges flipping. `hangzhou`, not `beijing`, is China's wealth pole under §1.3: `c_w` rank 1 against `beijing`'s 31, node wealth 245.0 against 143.8, and it holds the richest single province in the game. Zeroing `beijing` **also** moves the map — 17 flips, sinks `{doab, english_channel, hangzhou, sevilla}` — because deleting 1.3% of world wealth renormalises `c_w` everywhere; what separates the two is that `hangzhou` **survives as a sink** when `beijing` is zeroed and does not when `hangzhou` is. *(v2 through v4.0 said zeroing `beijing` "moves nothing". It does. The rank gap is what carries this row, not a null result.)* |
```

### 60. `G60` — §3.15

3.15 still asserted the supply/demand ratio 3.2 withdraws

**Removed:**

```
sinks land where the field is locally flat, demand enters only as `(c−s)/deg` against the local
spread, and supply contrast (10⁷) drowns demand contrast (10²–10³). Diagnosed, measured, and
replaced
```

**Replaced with:**

```
sinks land where the field is locally flat, demand enters only as `(c−s)/deg` against the local
spread, and the supply signal is **sparse** rather than large — most nodes produce nothing at all
of a given good, so `(c−s)/deg` is dominated by where supply *exists*, not by how big it is.
*(v1 and v2 gave the asymmetry as "supply contrast 10⁷ against demand contrast 10²–10³", and v3.0
through v4.0 repeated it here while §3.2 was withdrawing it. §3.2 is right: that ratio was `max(s)`
over v1's ε floor, and with the floor removed the contrasts run **4–97 on supply against
211–20,400 on demand** across the 29 goods — the demand side is the wider one. Sparsity is what
survives the floor's deletion, and it is what the diagnosis rests on.)* Diagnosed, measured, and
replaced
```

### 61. `G61` — §1.10

1.10's caravan measurement did not say which inland basis it used

**Removed:**

```
(median 17.9% over the 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`)
```

**Replaced with:**

```
(median 17.9% over the **flag's** 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at
`champagne` — §2.2 derives inland from `members` instead and gets 25, dropping `siberia`; on that
basis the range, the largest-holder span and the count below are all identical and only the median
moves, to 17.5%)
```

### 62. `G62` — §1.6

1.6 gave two live justifications for the same constant

**Removed:**

```
of it (the band table below), and the value was chosen with a target count in view. What the world
```

**Replaced with:**

```
of it (the band table below), and v2.1 chose the value with a target count in view — a calibration
§2.3 now withdraws, since the ground on which 1.5 is *retained* is the band table and not that
target. What the world
```

### 63. `G63` — §1.6

The Europe demonstration's only unsourced sentence

**Removed:**

```
holds none. That range is far below what the Renaissance, Colonialism and Printing Press deliver
  over 1450–1550.
```

**Replaced with:**

```
holds none. **What the model claims here is the threshold, not the size of the historical edge**:
  2% is enough, and the project measures nothing about how much development Europe actually gained.
  What the files do settle (`common/institutions/00_Core.txt`) is that all three institutions the
  period is named for begin **in Europe, inside this window** — Renaissance `1450.1.1` at Florence
  (province 116), Colonialism `1500.1.1` at Sevilla (224), Printing Press `1550.1.1` at Frankfurt
  (1876) — and that the Renaissance's embracement bonus is `development_cost = -0.05`, a standing
  5% discount on every subsequent development point. Those bonuses are **country-scoped and so are
  excluded from wealth by §1.3**; they reach the map only by changing how fast a province's
  development grows, which is the input `europe.py` scales directly.
```

### 64. `H64` — §1.6

The narrow alpha window shrinks under noise; it does not disappear

**Removed:**

```
The last row is v4.0's result and it is **not reproducible**: under ±1% wealth noise that window
moves or disappears entirely, while the wide bands move by ≤0.03. It is not a band, so no constant
could honestly sit in it.
```

**Replaced with:**

```
The last row is v4.0's result and it is **not a band**. Refined to 0.001 it spans [1.406, 1.424] —
**0.018 wide**, against the one-sink band's 0.506 — and under ±1% wealth noise across 8 seeds its
edges move by up to 0.02 while its width ranges **0.00 to 0.03**: the window is the same size as the
noise that perturbs it, and on some seeds it collapses to a single sampled α. The three wide bands
over those same seeds keep widths of 0.28–0.51 with edges moving ≤0.03. A constant cannot honestly
be placed inside a window narrower than the uncertainty in its own edges. *(An earlier draft of this
paragraph said the window "moves or disappears entirely" under noise. At 8 seeds it disappears on
none of them — it shrinks. The weaker claim is the true one and it is sufficient.)*
```

### 65. `H65` — §2.3

2.3 repeated the same overstatement about the fitted map

**Removed:**

```
corrected wealth field of §1.3 it does not yield that map, and the map it was fitted to is not
reproducible under noise (§1.6).
```

**Replaced with:**

```
corrected wealth field of §1.3 it does not yield that map, and the α_Φ window that does yield it is
narrower than the uncertainty in its own edges under ±1% wealth noise (§1.6).
```

### 66. `J66` — §2.8

2.8 wore the unweighted agreement under the weighted label

**Removed:**

```
  baseline is known — `Φ_w` agrees with the per-good graphs on 52.5% of value-weighted edge-goods —
```

**Replaced with:**

```
  baseline is known — `Φ_w` agrees with the per-good graphs on **51.5%** of edge-goods *weighted by
  trade value*, and on 52.5% unweighted (§1.6) —
```

### 67. `J67` — §3.9

3.9's node-wealth ranks had no v5.0 provenance

**Removed:**

```
`genua`, `gulf_of_siam` and `sevilla` rank 3rd, 2nd and 7th by node wealth and none of them is a
sink
```

**Replaced with:**

```
`genua`, `gulf_of_siam` and `sevilla` rank 3rd, 2nd and 7th by node wealth on the corrected field
— 296.0, 299.2 and 266.5 against `english_channel`'s 316.6 — and none of them is a sink
```

### 68. `J68` — §1.10

What the save's highest_power field is not, stated with the test

**Removed:**

```
*(v4.0 read the save's `highest_power` field, 9.6–20.7, as the largest incumbent's power. It is not, and the conclusion drawn from it inverted.)*
```

**Replaced with:**

```
*(v4.0 read the save's per-node `highest_power` field as the largest incumbent's power. It is not: parsing each node's country sub-blocks at their own brace depth and comparing, `highest_power` differs from the largest single country's `val` on **79 of 79** nodes — at `venice` it is 53.2 against Venice's own 106.2 — and it matches no share of `total`, `max`, `p_pow` or `collector_power` either. What it does hold was not determined and the model does not read it; the figures above come from the country sub-blocks. The conclusion v4.0 drew from it inverted.)*
```
