# Changes, spec v5.0 -> v6.0

**Method.** v6.0 was produced by copying `../v5-owner-agnostic/per-good-trade-spec.md` byte for byte
and applying **274 asserted string replacements**, each anchored on text that had to be present
exactly once or the patch aborted. Replaying the 274 in order against v5.0 reproduces v6.0 **byte for
byte**, so this document is the complete diff. A paragraph-level diff reports **36 groups replaced, 1 inserted, 0 deleted**, and the 42 headings are identical. The file grew from 131,566 to 172,232 bytes
(1,504 -> 1,980 lines).

**Inputs.** `../v5-owner-agnostic/validation-v5.md` (134 CONFIRMED / 39 PARTIAL / 22 REFUTED / 1
UNVERIFIABLE over X001-X196), the negotiated fix list in `fixes-agreed.md`, and a fresh pass over
the 1.37.5.0 install with the option-(c) solver.

**Verification.** `scripts/verify6.py` reads the **document text**, pulls out every figure it prints,
and compares each against a value computed from the install — the inversion v5.0's harness never did.
On v6.0: **22 checks, 0 failed**. `scripts/mutate6.py` plants twelve factual errors one at a time and
the verifier catches **12 of 12**; v5.0's harness caught 1 of 10.

**A second pass was needed and is the reason 70 replacements rather than 45.** A no-context claim
extraction of the 45-edit draft found that *every passage the patch pass touched obeyed both new
prose rules, and every violation sat in text the pass never opened* — §2.3 still carrying the
widest-band justification §1.6 had just withdrawn, §3.13 still carrying the deleted classifier,
§1.1 still asserting the sink-set equality §3.2 demolishes four lines later, §3.10 contradicting
itself two paragraphs apart. That is the same defect class that survived v3.0, v4.0 and v5.0:
patch what you touch and the untouched neighbour keeps the old claim. Twenty-nine further
replacements close it, and `verify6.py` now enforces internal consistency — a second passage stating
a figure differently from the first fails the check.

A second no-context extraction, run on a brief carrying no direction at all, recorded three further
textual facts: a province count corrected in one sentence and not its neighbour, a coefficient
provenance corrected in §2.2 and not in §1.3 or §2.3, and an edit boundary in §1.6 that stated one
position twice. Those are entries 71–74.

---

## What v6.0 changes

| Driver | Count | Where |
|---|---|---|
| Wealth becomes development + trade good + province condition (option c) | 7 | §0, §1.3, §2.2 |
| Start-state reads corrected (`on_startup`, dated `add_base_*`, the `is_city` filter) | 3 | §1.3 |
| Canonical node order re-grounded on Phase 2's degenerate LP | 3 | §1.1, §2.4, §3.2 |
| Figures regenerated on the new field | 14 | §1.1, §1.5, §1.6, §2.6, §2.8, §3.2, §3.15 |
| Absolutes narrowed to scoped observations or directional claims (R2) | 9 | throughout |
| Maintained figures deleted for rejected operators (R3) | 5 | §1.6, §3.2, §3.9, §3.15 |
| Precision corrections from the audit's E-series | 4 | §1.10, §2.2, §3.5, §3.10 |

Each is traceable to a graded claim: `fixes-agreed.md` maps all 62 open items to the change that
answers it, and that mapping is generated from `validation-v5.md` so no item can be dropped.

## The three rules v6.0 adopts

**R1 — wealth reads three things.** `base_tax`, `base_production`, the trade good, and the four
province-state static modifiers. The two-test modifier classifier is deleted along with everything
it governed: the trade-good modifiers, great projects, permanent province modifiers, buildings,
centres of trade, `production_leader`, the DLC conditionality, and the whole-install sweep. On the
1444 start that apparatus was worth 0.98% of world wealth over 87 of 2,472 provinces. **Owner-
agnosticism stops being a property defended by a rule and becomes true by construction.**

**R2 — no empirical absolutes.** No superlative, no universal quantifier, no threshold asserted as a
fact about the world. Every such claim becomes a directional design statement (which still fails if
the mechanism fails) or an observation scoped to its field and script. This answers the audit's own
systemic finding: *quantifier strength, not provenance, is where this document breaks.*

**R3 — no maintained figures for rejected operators.** `Phi_ord`, the gravity kernels and the v1
Laplacian keep their graveyard entries and lose their numbers. Those numbers were re-measured and
re-refuted in three consecutive audits and no design argument depended on any of them.

## The one change that moves every measured number

The field. World wealth 10,677.50 -> **10,594.70**; counted provinces 2,452 -> **2,472**; the
installed map's ends go from `{hangzhou}` back to **`{english_channel, hangzhou}`**, which is where
v2.0 through v4.0 had them — v2 measured a field with no modifier sweep, and (c) returns to it.

## The one change that is a design decision

**`alpha_Phi = 1.5` becomes a stipulated constant.** v2.1-v4.0 called it calibrated to a two-sink
1444 map; v5.0 called it the widest sink-count band. The first was fitted to a field that no longer
exists. The second depended on where the alpha scan stopped: over [1, 8] rather than [1, 3] the
widest band is 1.70 wide and 1.5's is 0.25. The replacement the author proposed — sink-set
noise-stability — was tested by the validation agent and refuted: it holds at every alpha on both
fields, so it selects nothing. **1.5 is now owned as a design choice, exactly as `P0 = 2.0` is**, and
§1.6 carries a written warning against re-deriving it from the two-sink map, which would reintroduce
the calibration §2.3 withdrew.

Entry 45's section label read §2.6 and the passage is in §3.8; corrected. A no-context extraction
found it by computing the v5→v6 text diff rather than trusting this document's labels, which is
the right way to read it — where a label here and the diff disagree, the diff is the fact.

## Round two

Entries 75–109 are the second pass. A no-context validation agent graded the 143-claim inventory
(112 CONFIRMED / 28 PARTIAL / 3 REFUTED), the findings were negotiated with it, and **a separate
agent measured every proposed replacement value against the install, the save and the solver before
any of it was written**. That pre-confirmation changed four of the proposed numbers and rejected two
outright, so the figures below are the confirmed ones rather than the proposed ones.

Three mechanism corrections drive most of the rest:

- **The solver reads the trade good the engine rolled** for the twenty provinces whose history says
  `unknown`, instead of pricing them at zero. World wealth 10,594.70 → **10,607.40**.
- **The coal-activation counterfactual holds every non-repriced input fixed.** Province 4237 is both
  latent-coal and one of the devastated eleven, so dropping its devastation measured coal activating
  *plus* one province healing — 2.40 ducats and 3 edge flips of contamination.
- **§3.10's argument is rebuilt on an identity rather than a magnitude.** Per-good propagation does
  **not** break the income identity: the collected-value-weighted mean share reproduces every
  collector's income exactly, algebraically. What it costs is that the scalar stops being derivable
  from trade power alone. Every magnitude any version quoted here measured its own construction.

The harness was also rebuilt twice over: every needle now reads a computed figure rather than a typed
literal, an empty run fails instead of reporting success, and the mutation test's anchors are derived
from the computed figures so they cannot silently go stale and skip.

## Round three

Entries 110–114 close four defects a third no-context extraction found, every one of them introduced
by round two's own edits: two figures corrected in one section while a differently-worded copy in
another kept the old value (connectivity, and the coal flips), a sentence truncated by the edit that
removed the Channel route, and a reference to an "item (c)" that exists only in the working notes.

Chasing the first two exposed a defect in the verification harness itself, and it is worth recording
because a passing test concealed it. `verify6.py` chose its check set from the **filename**, and
`mutate6.py` writes its candidate to `_mutated.md` — so every mutation run had been applying the
checklist's needles to the specification. An unmutated copy of the spec, merely renamed, failed 17 of
21 checks, which means every planted error was scoring as "caught" while nothing relevant was
checked. Routing is now by document content, and the harness gained a check that compares a
quantity's value **across every phrasing** rather than only across identical wording — the defect
class that produced two of the four fixes above.

## Round four

Entries 115–131 answer a second validation pass (145 CONFIRMED / 24 PARTIAL / 5 REFUTED on 174
claims). Four refutations were arithmetic or attribution: max `base_tax` is 15 and not 33, the
razed-China count is 22 and not 23, the tax-tooltip schema is `trunc(base_tax × 0.0833333)` rather
than `trunc(base_tax / 12)`, and the 0.6125 misreading belongs to v4.0 and v5.0 rather than v3.0 —
the last two having been **pre-confirmed in the previous round and never applied**, which is a
process failure rather than a measurement one.

The fifth is substantive and demotes this document's headline. **Phase 2's degeneracy reaches the
installed map's ends.** Across 100 relabellings with `α_Φ` and every input fixed, the orientation
changed 100 times and the 1444 sink set came back exactly 8 times — but `hangzhou` was an end in 100
of 100 and `english_channel` in 40. **The Asian end is a property of the world; the European end is a
property of the node ordering.** That is now stated in §1.6 where the sinks are given, in §1.6's
Europe table, and in §2.4's end-flag item, rather than only as a general caution about Phase 2; and
§2.8's razed-China row is marked ordering-**robust**, because it turns on `hangzhou` keeping an end.

Getting there needed two instruments discarded. A test built on `drain.py`'s `sweep_priority(pid=…)`
hook reports **no** change at all, because Phase 1, the promotion and Phase 2's LP still read the true
index. A partial reimplementation that omits Phase 0, Phase 1 or Phase 4 reports wild instability —
16 sinks on the identity permutation. Only a five-phase implementation validated against `drain.py`
on `Φ_w` (159 of 159 edges, core 80, 2 promotions, 0 fallbacks) gives the real answer, and neither
one-sided failure announces itself.

The harness claim was also corrected. `mutate6.py` plants errors only in figures `verify6.py` already
checks, so its score cannot fail and is not coverage; `coverage6.py` measures the honest denominator
by corrupting every spec-printed figure regardless. §0 now says under half are guarded rather than
quoting a fraction, because the fraction moved within one edit of being written.

## Round five

Entries 132–135 correct three overstatements in round four's own ordering result, and one about the
harness. All four were mine and three came from the same mistake: **generalising a single random
seed.** Round four wrote "`hangzhou` was an end in 100 of 100" and §2.4 derived "under every ordering
tried"; across four seeds of 100 relabellings the figure is 100, 99, 97, 98 — so orderings exist
where even the Asian end moves, and a universal quantifier had been introduced *by* the edit that was
removing universal quantifiers.

The blanket instruction to "read the rest of this section as conditional" was also too broad. Over
the same relabellings the map is fully oriented and acyclic every time, no fallback ever fires, and
the LP objective is identical to 2.22e-16 — different *optimal* orientations, not different answers.
§1.6 now separates what the ordering moves (the sink set's membership and size, the end-flag list,
which European node holds an end at the smaller factors) from what it does not. And the Europe
table's ×2.00 row was wrongly listed as ordering-dependent: `genua` holds an end there in 60 of 60.

**A process note, since it cost a cycle.** These four edits landed after the round-five extraction had
already read the document, which made that inventory stale in exactly the claims that changed. Fixes
belong in one batch between a validation and the next extraction; editing mid-cycle invalidates the
inventory a validator is about to grade against.

## Round six

Entries 136–158 answer a third validation pass (158 CONFIRMED / 24 PARTIAL / 1 REFUTED on 183
claims) and the pre-confirmation of that answer. The single refutation was the third site of a fix
applied to two: §1.6 and §2.4 had been corrected to a measured range and §2.8's row still said
"under every relabelling tried".

**Three corrections are to figures this document introduced one round earlier, and all three are the
same mistake — treating a sample as a constant.**

- The node-order proportions were quoted as a per-seed range. A range is a function of which seeds
  are drawn: two honest 800-trial runs gave 97–100 and 96–100 per hundred for one quantity.
- Pooling fixed the leading proportions and not the trailing ones. Across three independent
  800-trial sets `hangzhou` holds 784–789 and `english_channel` 322–336, but `sevilla` ranges 79–117
  and `rheinland` 112–136 — so the minor end-holders are now described rather than counted.
- The Channel's basin was said to grow as Europe develops. It grows to about 28 nodes by ×1.44 and
  then the end migrates: `genua` first holds one at ×1.63 and is sole end from ×1.64.

**And one correction is a revert.** "19 land provinces (`cape_of_good_hope`)" was right; round five
changed it to 20 on a members count. Province 1460 is a sea zone, listed in `map/default.map`'s
`sea_starts` — a claim about *land* provinces is not answered by a count of *members*, and the
paragraph's own next sentence had been computing with 19 all along.

The node-order experiment now ships as `relabel6.py`, because two audits found its figures attributed
to scripts that did not contain them. It validates its instrument against `drain.py` on the identity
permutation and aborts if that fails — necessary because every wrong instrument tried here failed
one-sidedly: the `sweep_priority(pid=…)` hook reports no effect at all, and a reimplementation missing
Phase 1 reports the shipped answer with no flips, so a broken instrument can look stable as readily as
chaotic.

## Round seven

Entries 159–170 answer validation round 4 (168 CONFIRMED / 19 PARTIAL / 1 REFUTED on 188 claims) as
corrected by its pre-confirmation, which found four of the twenty staged values wrong — **including one
staged as a finding.**

**The model gains a row.** `unrest` grants `local_tax_modifier = -0.02` and is province state, so §1.3
listed four province-state modifiers where there are five. It is live at 1444 on 21 provinces, worth
12.23 ducats or 0.115% of world wealth, and it moves **no edge** of the installed graph. Its per-point
scaling is stated in the file, which leaves `devastation` as the only unsourced scaling law in that
table — and sharpens rather than dilutes that caveat, since the convention for stating a scaling
demonstrably exists in the same file.

**A withdrawal is reversed.** The 580-of-580 per-good sweep was withdrawn on the ground that its script
had never shipped. `../v5-owner-agnostic/scripts/_audit_b_1444perm.py` exists and runs. A real result
was deleted for a false reason — though the replacement sentence was also wrong to say earlier versions
had quoted it, since "580" appears in no v1–v5 spec.

**Two figures are withdrawn for being properties of the node order rather than the world.** `Φ_ord`'s
end count runs 12 to 19 across relabellings and its end set is never twice the same, so neither the
count nor the share terminating no good survives; and no basin figure is quoted, because at the growth
factors where one would be interesting `english_channel` holds an end in only three to eight orderings
out of sixty, making any range the spread of a handful of observations.

**And two of this document's own figures turn out to have been one measurement.** 4.44e-16 and 6.2e-16
are the same LP deviation in absolute and relative units — four units in the last place — so the
"correction" that replaced one with the other was correcting nothing. It is now stated once, in ULP,
and marked as a sample maximum that grows with trial count.

The `change_price` census also gains a distinction it needed: 1.875 is the floor from a single key, and
the *history* file's −0.25 rather than the event's −0.20 is what the 13/2/4/11 partition depends on. A
campaign that runs HAB's 1540 block holds two live negative keys on `wool` and lands at 1.625 or
1.6875 — and nothing in the install settles which, because no readable save carries a good with two.

## Round eight

Entries 171–173 fix one defect, introduced by round seven and found by the next extraction: the
`unrest` row was added to §1.3's province-state table and **three prose counts kept saying "four"** —
§1.3's own lead-in, §2.2's solver item, and §3.13.

It is the fourth instance in this version of patching one site and missing its neighbours, and the
first that no check could see: the count is a word and the table is rows, so every numeric comparison
in `verify6.py` was blind to it. The harness now parses the table's row count and compares it to the
spelled number in the lead-in and to every other prose count of the same set. Reverting one count in a
copy makes it fail, which is the only evidence that a check works.

That brings the defect classes this version's harness has absorbed to four: a document figure
disagreeing with a computed value; the same quantity phrased two ways and disagreeing; a green run
over an empty check set; and now a spelled count disagreeing with the table it describes.

## v6.1

Entries 207 onward are a different kind of change from everything before them: v6.0's edits corrected
the document, and these change the **operator**.

`alpha_Phi` moves from 1.5 to 2.0, and Phase 2 stops minimising unit arc costs. With unit costs its
min-cost b-flow is degenerate -- 40 of 40 permutations return a different optimal support -- so the
installed map depended on how the nodes happened to be numbered, which is what v6.0 documented at
length. The new objective is `1 + TIE_EPS*(w[u]+w[v])/2`, symmetric in the arc and read from node
wealth: 0 of 40 permutations return a different support, and 180 end-to-end relabellings moved 0 of
159 edges. Both constants are hyperparameters whose values are developer taste; every derivation
previously offered for `alpha_Phi` is withdrawn and none replaces it.

The 1444 sink set moves from `{english_channel, hangzhou}` to `{genua, hangzhou}` and 29 of the 59
figures `measure6.py` prints move with it.

Four things a full reading caught that no check covered, and that are worth recording because each was
a statement the harness could not see:

* **1.1's Efficiency property** still said the objective *is* `flow x hops`. It is not any more; it is
  a hop count weighted within a tenth of a percent, so the property is now an approximation with a
  bound rather than an identity.
* **1.1's acyclicity argument** rested on "all costs 1". It needs positivity, not unit costs, so it
  survives -- but the wording asserted the stronger premise.
* **`unrest` was in the document and not in the solver.** 1.3 listed it as entering `tax_value` and
  said admitting it moves no edge. `solver.py`'s `STATE_TAX_MOD` holds `occupied` alone, so the model
  never read it; and at alpha_Phi = 2.0 admitting it moves **4** of 159 edges, not none. The document
  now states the gap and what closing it costs (world wealth 10,595.17) rather than describing a
  feature that does not exist.
* **`devastation`'s scaling law** was called an assumption. The wiki states the penalties are scaled
  linearly with the percentage value and quotes them at 100%, which is exactly what the model applies.
  It is the one row in that table sourced to community documentation rather than a shipped file, and
  the document now says so.

Two harness defects surfaced in the same pass. `verify6.py` computed its failure list before the last
checks ran, so anything appended after that point was counted as passing -- the accounting bug the
harness exists to prevent, inside the harness. And a check that read the harness's own stated check
count out of the document had to be retired: some checks are generated per matching phrase, so the
total moves whenever the prose does, and section 0 already declines to quote figures of that kind.

### What the full reading found

The harness covers 30 sites. The operator change touched far more, so the document was read end to
end afterwards. Six defects it caught that no check could:

* **1.6 claimed the per-good graphs are order-invariant.** They are not, and 2.4 item 1 said so on
  the same day -- the two sections contradicted each other. 84 of 290 per-good relabellings move an
  edge, because uniqueness of an LP optimum depends on the right-hand side as well as the objective:
  `b_w` has no zero entries and its optimum is unique, each `b_g` puts a different face of the
  polytope in play.
* **The value weights were said to hang off the per-good solves, in three places.** They do not:
  `V_g` is `price(g)` times a sum over producers, with no direction in it. What per-good
  order-sensitivity does reach is larger -- 2.2 propagates the per-good economy and writes it back,
  so it reaches node values, the ledger and the economy tab.
* **2.3's scope sentence** read as if per-good solves keep unit costs. Every DRAIN solve uses the
  tie-break; what keeps unit costs is the separate FLOW/TREE comparison operators.
* **2.8's per-good row** still said 1 to 8 sinks per good and quoted a 16.8% demand-decile rate. The
  tie-break changed the per-good graphs: it is 2 to 8, and 19.8% against 6.9%.
* **3.3's node-size illustration** works at alpha = 1.5, which is a per-good alpha and not
  `alpha_Phi`. Next to `alpha_Phi = 2.0` it read as a stale figure; it is now named, with the
  aggregate case given alongside.
* **3.9 carried two overlapping disclaimers** and a "those ends" whose antecedent an earlier edit in
  the same pass had removed.

One question asked during the pass turned out to be worth more than the answer: would a second
wealth term make the per-good optima unique too? It makes all 159 arc costs distinct where the
shipped cost leaves three pairs equal -- and still leaves 72 of 232 per-good supports moving, down
from 93. Distinct arc costs are not the obstruction; different routings with equal **totals** are,
and ruling those out needs a generic perturbation, which is arbitrary by construction.

### unrest: implemented, measured, reverted

`unrest` was listed in 1.3 as entering `tax_value` and had never been in `solver.py`. It was
implemented -- reading the authored value from `history/provinces`, which the parser already resolved
correctly -- measured, and then removed again on the owner-agnosticism test: revolt risk carries
separatism, culture and religion terms that are relations between a province and its owner, so
reading it makes a province's wealth change when it is conquered, which is what 1.3 exists to
prevent. The 1444 field shows the split directly: 16 of the 21 are authored in province history, and
the other five are all Shirvan-owned runtime values.

What the exclusion costs is now recorded rather than assumed: 12.23 ducats (0.115%) reading the save,
9.40 (0.089%) reading only the authored 16, and 4 of 159 edges either way with the sink set unchanged.
And the effect it would have bought is already bought -- `devastation`, `occupied` and `under_siege`
all make conquest cost a province its wealth, and all three are properties of the place.

### The second-order tie-break

The first-order wealth term removes every alternative optimum on the aggregate `b_w` -- 40
zero-reduced-cost arcs outside the support down to 0 -- and leaves 41 across 18 of the 29 per-good
`b_g`. The reason is exact: a non-tree arc has zero reduced cost when its own cost equals the sum of
costs along the tree path between its endpoints, and each `b` builds a different tree and exposes
different coincidences. A **structured** cost invites them; a **generic** one does not.

So a second-order generic term went in, read from the unordered wealth pair so it stays symmetric in
the arc and invariant under relabelling:

    cost(u,v) = 1 + TIE_EPS*(w[u]+w[v])/2 + TIE_EPS2*frac(min*max*7919)

| | before | after |
|---|---|---|
| goods admitting an alternative optimum | 18 of 29 | **1 of 29** |
| per-good relabellings moving an edge | 84 of 290 | **13 of 290** |
| sinks per good | 2-8, mean 3.69 | unchanged |
| `Phi_w` sinks, acyclicity, noise stability | -- | all unchanged |
| self-coherence | 55.2 / 55.0 | 55.1 / 54.8 |
| any-good connectivity | 5,721 (90.5%) | 5,723 (90.6%) |

Two things were rejected on the way, and both are recorded in the document because both are natural
ideas someone will have again:

* **A structured second term** (`+ TIE_EPS^2*|w[u]-w[v]|`) makes all 159 arc costs distinct where the
  shipped cost leaves 3 pairs equal -- and still leaves 72 of 232 per-good supports moving. Distinct
  arc costs are not the obstruction; equal **totals** over different routings are.
* **Pinning the per-good free edges to `Phi_w`'s direction.** Half the per-good map (2,321 of 4,611
  slots) is free edges, and 144 of the 177 that move under relabelling are among them, so this looked
  like most of the fix. It makes **all 29 goods cyclic**. A cycle-safe variant -- take `Phi_w`'s
  direction unless it closes a cycle, else the reverse -- is acyclic by construction and lifts
  self-coherence to 73.6%, but nearly doubles sinks per good (3.69 -> 7.03) and lands the extra sinks
  in the poorest peripheral nodes: `amazonas_node` for 15 of 29 goods, `patagonia` for 5. That strands
  value at dead ends, which is the failure that killed seeded basins in 3.15.

### What the second pass found

The term is not free, and the reading after it went in caught the cost. **2.3 claimed the
normalisation is not load-bearing**, on the argument that rescaling `w` equals rescaling `TIE_EPS`.
That holds for a linear term and `frac(lo*hi*7919)` is not linear: measured across min-max, mean and
world-total normalisation, the aggregate is still identical (0 of 159 edges) but **5 of 29 per-good
graphs move**. The normalisation is now a third arbitrary choice with an observable consequence, and
2.3 says so.

Also caught: 2.3 still read "adding a second wealth term does not close it" in a paragraph four
paragraphs below the one describing the term that closes it; a paragraph restating figures already
given; "changing either value" where there are three constants; a cost range written `[1, 1+TIE_EPS]`;
and the +/-1% noise result quoted at three seeds in 1.6 and six in 2.3 and 3.6 -- both real, now
attributed.

**2.8's spice and cloves row was stale independently of any of this.** It listed Australia, Venice and
Deccan among the termini; none of the three holds either sink on this field. Measured: `spices` sinks
at Genoa (its demand rank 1) and Brazil (rank 73), `cloves` at Genoa, Kongo and Brazil (ranks 2, 55,
72). Every load-bearing claim in the row survives -- Indonesian source, no Chinese spices sink, Genoa
a spices sink -- and the lists did not.

### The solver tolerance, and multiplayer

Asked whether the model is multiplayer-safe, the chase produced a finding that was not about floating
point at all.

The first-order wealth term makes the aggregate optimum unique; the second-order generic term makes 28
of 29 per-good optima unique. But under permutation of the LP's **column order**, `copper` and `paper`
still returned orientations differing on 12 and 8 edge-slots -- with objectives differing by **7.7e-10
relative**, six orders above float noise. Those were not tied optima. They were unequal-quality
answers: HiGHS stops when reduced costs are within its dual feasibility tolerance of zero, its default
is **1e-7**, and the margin by which the tie-break makes the optimum unique is as low as **3.8e-8**.
The margin sat inside the solver's own tolerance.

Pinning both feasibility tolerances to 1e-10 (HiGHS's floor) fixes it:

| | before | after |
|---|---|---|
| orientation flips under column permutation | 20 | **0** |
| relative objective spread | 7.7e-10 | **1.1e-15** |
| per-good relabellings moving an edge | 13 of 290 | **0 of 290** |
| figures in this document that moved | -- | **none** |

No figure moved because the shipped column order was already reaching the true optimum; what changed
is that every other order now does too. `flowop.LP_OPTS` carries it and 2.8 asserts it, because it can
regress silently on a solver upgrade.

**That reframed multiplayer.** The classical worry -- bit-reproducibility of a floating-point solve --
is not the binding constraint, because every decision now has a margin 8 to 10 orders above double
noise: 3.8e-8 worst per good, 7.5e-6 on the aggregate, and a free-versus-flow classification whose
`|net|` distribution is bimodal with **nothing** between exactly-0 and 1e-6. The solve also carries no
randomness at all -- one fingerprint over `Phi_w` and all 29 per-good graphs was identical across
repeated runs, separate processes, and five `PYTHONHASHSEED` values including `random`, so there is no
seed to pin. What is left is build discipline: one binary per platform, and no runtime CPU dispatch or
threading in the solver. 2.1 now says that instead of "requires bit-reproducibility", and 3.13's open
question is restated to match.

Recorded alongside: every trade number EU4 itself writes is quantised to **1/1000** (495 of 495
sampled). Whether that rounding is in the simulation or only the serialiser is a new 2.7 probe --
though it would not rescue this solver either way, since the orientation margins sit three to five
orders below a 1e-3 grid.

### What the reread found this time

Nine defects, and the most instructive is that **four were cross-references I had just written**. The
multiplayer discussion lives in 2.1 Shape, not 2.2 Solver -- 2.2 is a build list -- so four pointers I
added sent readers to the wrong section, and two pre-existing ones sent them to 2.2 for the
connectedness requirement, which is in 2.2a. An audit of all 128 edits from this pass confirmed every
other reference resolves.

The rest: 2.2's multiplayer opening still demanded "bit-reproducibility" and called an identical build
"not sufficient", directly contradicting the material added below it; 0's summary still reported a
per-good residue that is now zero and counted two changes where there are three; 0's coverage
paragraph had accumulated duplicated sentences across several edits; 3.6 and 3.13 still called the
per-good optima degenerate and required the LP to "pivot identically"; and one 2.8 table row had a cell
wrapping onto a second line, which breaks the row in any renderer.

Two claims were also **strengthened** rather than corrected, because the measurements supported more
than the document said: the `(DEF, b)` key-collision count is zero across all **2,320 core nodes** of
the per-good solves, not merely on the free edges where earlier versions measured it, and Phase 1's
within-cluster argmin and top-k cut are untied on the same field -- so no index tiebreak in the
algorithm fires anywhere.

## Round eleven

Two entries, both answering the census rather than the harness, and both about claims this pass
introduced.

**The solver-tolerance claim was unsourced.** Round 11 flagged it as the one genuinely new unsourced
assertion: the stopping rule and the 1e-7 default were stated with no file, version or document behind
them. Both are now cited to `scipy.optimize.linprog`'s `method="highs"` options (scipy 1.18.0), and the
mechanism is confirmed rather than inferred -- bisecting the tolerance against `copper`, leaving it
unset and setting it to 1e-7 give the same 8 flips, which pins the effective default independently of
any documentation, and 1e-8 gives 0. 1e-8 is the first value below `copper`'s 3.765e-8 margin, so the
flips appear exactly when the tolerance exceeds the margin. That is the claim, now demonstrated.

**And 0 asserted the proportion it then refused to give.** The deduplication earlier in this pass left
"covers well under half of what the document prints" two sentences before "a proportion has no
well-defined denominator". The refusal is the half that survives; "partial" is as far as the paragraph
now goes. A defect introduced and caught inside the same pass, by the census rather than by any check
-- no numeric check can see a paragraph disagreeing with itself in words.


---

## Every replacement, in the order applied

### 1. `R1-formula` - §1.3

R1: the wealth formula

**Removed:**

```
```
goods_produced(p)   = GP_COEFF · base_production(p) · (1 + Σ local goods-produced modifiers)
                                                             # + local flat goods bonuses
trade_value(p)      = goods_produced(p) · price(good(p)) · (1 + Σ local trade-value modifiers)
                                                             # ducats / YEAR
tax_value(p)        = TAX_COEFF · base_tax(p) · (1 + Σ local tax modifiers)   # ducats / YEAR
wealth(p)           = tax_value(p) + trade_value(p)          # ducats / YEAR
```

**Replaced with:**

```
```
goods_produced(p)   = GP_COEFF · base_production(p) · (1 + Σ province-state goods modifiers)
trade_value(p)      = goods_produced(p) · price(good(p))     # ducats / YEAR
tax_value(p)        = TAX_COEFF · base_tax(p) · (1 + Σ province-state tax modifiers)
wealth(p)           = tax_value(p) + trade_value(p)          # ducats / YEAR
```

### 2. `R1-inputs` - §1.3

R1: three inputs, stated up front

**Removed:**

```
**Wealth is owner-agnostic.** It is a property of the *place* — what the land is worth per year,
before anyone's government touches it. No autonomy, no production efficiency, no national ideas,
no estate or government modifiers, no technology. Two provinces with the same terrain, development
and trade good have the same wealth whoever owns them, and a province's wealth does not change
when it is conquered.
```

**Replaced with:**

```
**Wealth is owner-agnostic, and it reads three things about the province: its development, its
trade good, and its own current condition.** It is a property of the *place* — what the land is
worth per year, before anyone's government touches it. No autonomy, no production efficiency, no
national ideas, no estate or government modifiers, no technology. Two provinces with the same
development, trade good and condition have the same wealth whoever owns them, and a province's
wealth does not change when it is conquered.

**Owner-agnosticism is true by construction here, not by a rule that has to be policed.** v3.0
through v5.0 stated the property and then defended it with a two-test classifier applied to a sweep
of the install — is this modifier local, does it enter wealth — which is a large surface to keep
correct and was wrong in every audit that examined it. `base_tax`, `base_production` and the trade
good are bare attributes of the place, so nothing about them needs classifying. *What this gives up:*
`gems`' `local_tax_modifier` and `incense`' `trade_value_modifier` are genuinely province-scoped and
are no longer read, along with great projects, permanent province modifiers and the DLC state they
depended on. On the 1444 start that whole apparatus was worth **0.98%** of world wealth over 87 of
2,472 provinces, and the model trades that fidelity for an input surface with no classification
question in it.
```

### 3. `R1-table` - §1.3

R1: the classification table is deleted

**Removed:**

```
**Which modifiers are local, and which of those enter wealth.** Two tests, and a modifier must pass
both. It is **local** iff its value depends only on the province's own attributes — terrain,
climate, trade good, development, buildings — and on no country's state. It **enters wealth** iff it
modifies a quantity `wealth` computes: `goods_produced`, `price`, or `tax_value`. The engine's
trade-good data model is one *instance* of the first test and not the test itself — a good's
`province = { … }` block is province-scoped and its `modifier = { … }` block is country-scoped, so
only the first can be local — because modifiers also reach a province from outside the trade-good
tables, and those are classified by the test rather than by which file they live in.

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

**Replaced with:**

```
**Province condition is the one thing besides development and the good that wealth reads.** Four
static modifiers describe a province's own state, and all four are read from
`common/static_modifiers/00_static_modifiers.txt`:

| modifier | what it grants | enters |
|---|---|---|
| `devastation` | `trade_goods_size_modifier = -2`, scaled by the devastation level | `goods_produced` |
| `prosperity` | `trade_goods_size_modifier = 0.25` | `goods_produced` |
| `under_siege` | `trade_goods_size_modifier = -0.25` | `goods_produced` |
| `occupied` | `trade_goods_size_modifier = -0.5` **and** `local_tax_modifier = -0.5` | both |

Only `occupied` touches the tax term; the other three reach `goods_produced` alone. These are what
make the map answer to war — §1.2's volatility and §3.3's "a besieged province genuinely produces
less" both rest on them, and §2.8's war rows are their test.

**They are not all quiet at the 1444 start.** Ten provinces begin devastated — Bohemia at 50 and
Erzgebirge and Moravia at 20 — and no province-history file says so: the devastation is applied by
`on_startup`, which fires `flavor_boh.15` ("The Aftermath of the Hussite Wars"). It costs **13.40
ducats** across the eleven affected counted provinces. The chain is
`common/on_actions/00_on_actions.txt` → `on_startup_effect` →
`common/scripted_effects/01_scripted_effects_for_on_actions.txt` → `country_event flavor_boh.15`.

**The start state is what the engine produces, not what the history files say.** That is the general
form of the point above, and it costs three separate reads:

1. **`on_startup` effects**, as above. `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`,
   `flavor_geo.1` and others, and `flavor_geo.1` carries `add_base_tax`, `add_base_production` *and*
   `add_devastation` — so development itself can move before the first tick.
2. **`add_base_*` in a dated block before the start date accumulates**, and v5.0 and earlier
   overwrote instead of adding, silently dropping the grant. Province 1 (Uppland) has `base_tax = 5`
   undated plus 1 at `1436.4.28`; the game has 6.
3. **`is_city = yes` is not a filter the engine applies.** 20 owned provinces omit or comment out
   that line — province 265 is one, and it is also one of the devastated ten — and the engine treats
   them as cities. The model counts a province when it has an owner and lies in a trade node:
   **2,472** provinces, not 2,452.

**Twenty counted provinces have no trade good in their history file** (`trade_goods = unknown`); the
engine assigns one at start from each good's `chance = { }` block. The wealth field is therefore
partly the result of one random draw. The model does not try to predict the draw: it reads whatever
the game's current state holds, which is what it does for development too.

```

### 4. `R2-flat` - §1.3

X-flat: the flat-bonus sentence has no table to point at

**Removed:**

```
development first and then applies a percentage — `Base 0.49` then `Tax Income Efficiency 125.0%`,
giving 0.6125, which the province window shows as 0.62. Flat goods bonuses are the exception: they
add into `goods_produced` *before* the price multiply. The goods-produced tooltip's shape is
**consistent with** that and does not establish it — it carries an additive `Base Goods Produced`
block (`Base Production: +0.80`) above a separate multiplicative `Goods Produced Efficiency` block.
Fifteen 1444 provinces do carry a flat bonus in the first block (the table above), so the ordering
matters in practice and not only in principle.
```

**Replaced with:**

```
development first and then applies a percentage. Observed on Garnatah: `base_tax` 6 with
`Tax Income Efficiency 125.0%` displays `Base 0.49` and then `0.62`. **0.49 × 1.25 is 0.6125, which
truncates to 0.61, not 0.62** — so the engine is not multiplying the displayed figure. It multiplies
the untruncated monthly value: 6 × 0.0833… = 0.49999…, × 1.25 = 0.62499…, displayed 0.62. The
example establishes the ordering (base from development first, percentage second) and nothing
finer. *(v3.0 through v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires
rounding while §2.3 requires truncation. Both cannot hold.)* Flat goods bonuses would add into
`goods_produced` before the price multiply — the goods-produced tooltip carries an additive
`Base Goods Produced` block above a multiplicative `Goods Produced Efficiency` block — but under
§1.3 no source grants one, so the ordering is stated for the emitter's benefit and is not exercised
by any province in the model.
```

### 5. `R2-taxbasis` - §1.3

X021: the tax tooltip schema is arithmetically wrong

**Removed:**

```
both as *annual* quantities divided by twelve for display. The tax tooltip reads
`Base: X (Yearly 12·X)` — `Base: 0.49 (Yearly 6.00)` at `base_tax` 6, `Base: 0.16 (Yearly 2.00)` at
`base_tax` 2. The monthly production tooltip's `Trade Value` line is the province window's *annual*
`Trade Value` over twelve — observed 3.52 → `Trade Value: +0.29`. Both monthly figures are the
annual value over twelve, so the annual forms add directly with no conversion.
```

**Replaced with:**

```
both as *annual* quantities divided by twelve for display. The tax tooltip reads
`Base: trunc(base_tax / 12) (Yearly base_tax)` — observed `Base: 0.49 (Yearly 6.00)` at `base_tax` 6
and `Base: 0.16 (Yearly 2.00)` at `base_tax` 2. The parenthetical is `base_tax` itself and the
`Base` line is its truncated twelfth; it is **not** twelve times the displayed figure, which would
give 5.88 and 1.92. *(v3.0 through v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both
of its own data points.)* The monthly production tooltip's `Trade Value` line is consistent with the
same relation on one observation, 3.52 → `+0.29`, which fixes the divisor only to within
[12.00, 12.14]. Both monthly figures being the annual value over twelve is what lets the annual
forms add directly, and the tax pair establishes it at two development levels.
```

### 6. `R2-refcond` - §1.3

The TAX_COEFF reference condition and the province filter

**Removed:**

```
to exactly 0.75 + 0.25 = 1.00 and yields `base_tax` ducats a year. That is the reference condition
`TAX_COEFF = 1.0` was measured at, and it is the same for every province the model counts: all of
them are cities (`is_city = yes`), and ownership is not modelled, so every one is treated as cored.
Carrying either term again would double-count it.

Unowned provinces are outside the model: `s` and `c` are computed over provinces with an owner and
`is_city = yes`, because an unowned province produces nothing the trade system can move.
```

**Replaced with:**

```
to exactly 0.75 + 0.25 = 1.00 and yields `base_tax` ducats a year. That is the reference condition
`TAX_COEFF = 1.0` was measured at, and the model applies it to every province it counts: ownership
is not modelled, so every province is treated as cored and settled. Carrying either term again would
double-count it. *This is a modelling choice with a known cost — two readings, both on cored city
provinces at `base_tax` 2 and 6, are what `TAX_COEFF = 1.0` rests on, and the development range runs
past 50.*

Unowned provinces are outside the model: `s` and `c` are computed over provinces that have an owner
and lie in a trade node, because an unowned province produces nothing the trade system can move.
```

### 7. `R2-solver` - §2.2

§2.2 item 4: the solver's wealth expression

**Removed:**

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

**Replaced with:**

```
4. Per-province `wealth` — **owner-agnostic** per §1.3:
   `TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production ·
   (1 + province-state goods modifiers) · price`, and no autonomy, efficiency, ideas or owner terms.
   The only modifiers read are the four that describe the province's own condition, and at 1444 only
   `devastation` is live, on eleven provinces. `GP_COEFF` is **read from**
   `common/static_modifiers/00_static_modifiers.txt` rather than hardcoded (§2.3). World wealth is
   **10,594.70** annual ducats over **2,472** counted provinces. Then per-node `trade_value`, `s`,
   `c` with per-province α, and the per-good balance `b = s − c`.
```

### 8. `R3-measured` - §1.6

The measured block, on the (c) field

**Removed:**

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

```

**Replaced with:**

```
Measured on 1444 data at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and
`hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12. Phase 1 selects `genua`; both sinks
arrive by stall promotion and `genua` ends a transit node, so there are **2 promotions and 0
fallbacks**. **Eight sources** — all in the bottom half of the wealth field, `c_w` ranks **44–75**,
mean degree **3.1** against the map's 4.0. *(v2 called them "cul-de-sacs", which their degrees do not
support.)* Every node drains to a sink; acyclic, 159/159 oriented; largest `|b_w|` **0.0226**; the
sink set is unchanged under ±1% wealth noise on three seeds. Its marking order is a per-node scalar
whose descending comparison reproduces the DAG (0 violations), so every consumer needing a potential
still gets one.

Per good, on the same field: **1–8 sinks, mean 3.52**, 29/29 acyclic, **0 fallbacks fired**, and
**90.2%** of ordered node pairs (5,703 of 6,320) connected by at least one good's directed path.

Agreement with the per-good graphs is **53.5%** of edge-goods (**52.1%** value-weighted). The
superseded marking-order aggregate scored higher on that measure; §3.9 records why the trade was
taken and no longer maintains a figure for an operator the model does not install.

```

### 9. `R3-bands` - §1.6

A1: alpha_Phi is a stipulation; the band table records alternatives

**Removed:**

```
**The sink count is a step function of `α_Φ`.** Measured across α_Φ = 1.00…3.00 at 0.01:

| sinks | α_Φ band | width |
|---|---|---|
| 1 — `hangzhou` | **[1.43, 1.93]** | **0.50** — the widest band on this field, and the one α_Φ = 1.5 sits in |
| 3 — `doab`, `genua`, `hangzhou` | [2.26, 2.71] | 0.45 |
| 2 — `genua`, `hangzhou` | [1.94, 2.25] | 0.31 |
| 2 — `english_channel`, `hangzhou` | [1.41, 1.42] | 0.01 |

The last row is v4.0's result and it is **not a band**. Refined to 0.001 it spans [1.406, 1.424] —
**0.018 wide**, against the one-sink band's 0.506 — and under ±1% wealth noise across 8 seeds its
edges move by up to 0.02 while its width ranges **0.00 to 0.03**: the window is the same size as the
noise that perturbs it, and on some seeds it collapses to a single sampled α. The three wide bands
over those same seeds keep widths of 0.28–0.51 with edges moving ≤0.03. A constant cannot honestly
be placed inside a window narrower than the uncertainty in its own edges. *(An earlier draft of this
paragraph said the window "moves or disappears entirely" under noise. At 8 seeds it disappears on
none of them — it shrinks. The weaker claim is the true one and it is sufficient.)* `α_Φ` is **retained at 1.5** because it sits inside the widest band and
nothing now selects a different value — not because it was derived (§2.3). Sampled at the six values
v2 used, the count is non-monotone: **5 → 1 → 2 → 4 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}.

```

**Replaced with:**

```
**`α_Φ = 1.5` is a stipulated design constant, exactly as `P₀ = 2.0` is.** It is superlinear so
that a few very rich provinces outweigh a dense mediocre region, and it is round. It is **not**
derived, and the document no longer offers a derivation: v2.1 through v4.0 said it was calibrated to
reproduce a two-sink 1444 map, and v5.0 said it sat in the widest sink-count band. The first was
fitted to a field that no longer exists; the second depended on where the α scan was truncated —
scanned over [1, 8] rather than [1, 3], the widest band is **1.70** wide ([3.51, 5.21],
`{doab, genua, hangzhou}`) and 1.5's is not the widest by any margin. Any future change to it is a
design decision about how many ends the installed graph should have, and §2.3 governs recording it.

What the value buys is recorded rather than argued. Across α_Φ = 1.00…8.00 at 0.01 the sink set is a
step function, and α_Φ = 1.5 sits in the band **[1.38, 1.63], width 0.25**, which gives
`{english_channel, hangzhou}`. Sampled at the six values v2 used, the count is non-monotone:
**6 → 2 → 1 → 2 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}.

*A warning for anyone revising this, because the mistake is available and has been made twice: the
1444 map has two ends and vanilla's authored map has three, and it is tempting to justify 1.5 by
that resemblance. Do not. That is the calibration §2.3 withdrew, and §3.9's adoption argument does
not rest on it.*

```

### 10. `R3-europe` - §1.6

P1/P2/R2: Europe stated directionally, the Lowlands claim deleted

**Removed:**

```
**One sink at 1444 is a snapshot, not a fixed feature, and the map says so under load.** Holding
α_Φ = 1.5 and moving nothing else (`europe.py`):

- **A 1–2% European development edge produces a European sink.** At ×1.02 across Europe's 823
  counted provinces the sinks are `{doab, english_channel, hangzhou, wien}`; `english_channel` is a
  sink at every larger factor tested. At ×1.56 the sinks are `{english_channel, rheinland}` and Asia
  holds none. **What the model claims here is the threshold, not the size of the historical edge**:
  2% is enough, and the project measures nothing about how much development Europe actually gained.
  What the files do settle (`common/institutions/00_Core.txt`) is that all three institutions the
  period is named for begin **in Europe, inside this window** — Renaissance `1450.1.1` at Florence
  (province 116), Colonialism `1500.1.1` at Sevilla (224), Printing Press `1550.1.1` at Frankfurt
  (1876) — and that the Renaissance's embracement bonus is `development_cost = -0.05`, a standing
  5% discount on every subsequent development point. Those bonuses are **country-scoped and so are
  excluded from wealth by §1.3**; they reach the map only by changing how fast a province's
  development grows, which is the input `europe.py` scales directly.
- **The Lowlands alone suffice.** Developing only the nine Lowland provinces in `english_channel`
  (Holland, Zeeland, Vlaanderen, Brabant, Antwerpen, Utrecht, Gelre, Friesland, Breda) by ×1.20
  makes `english_channel` a sink beside `hangzhou`, and it stays one through ×10.
- **Robust to noise, responsive to growth.** ±2% *random* wealth noise leaves the 1444 sink set
  unchanged on three seeds; **+2% applied systematically to Europe alone changes it**. The map does
  not twitch, and it does move.

```

**Replaced with:**

```
**Europe becomes the centre of trade as it develops.** That is the design claim, and it is what
§3.1's first goal asks the field to deliver. At 1444 the map already ends in the Channel and in
Hangzhou; as European development compounds, the Channel's basin grows and Asia's pole fades, and
past a broad range of European growth Asia holds no end at all. The mechanism is what carries this:
wealth is linear in development (§1.3), so developing a region moves its `c_w` share directly, and
`Φ_w`'s ends follow the wealth.

Observed on the 1444 field, holding α_Φ = 1.5 and scaling European development only (`europe.py`,
824 counted European provinces):

| European development | `Φ_w` sinks |
|---|---|
| ×1.00 (1444) | `english_channel`, `hangzhou` |
| ×1.02 | `english_channel`, `hangzhou`, **`wien`** |
| ×1.56 | `english_channel`, **`rheinland`** — Asia holds none |
| ×2.00 | `genua` alone |

These are properties of this snapshot, not constants of the model: they are what one field yielded
under one scaling, and a different world state moves them. Under (c) **scaling development and
scaling wealth are the same operation** — maximum difference 0.0 across the European set — so the
distinction that made v5.0's version of this table wrong does not arise.

What the shipped files settle, independently of any threshold: all three institutions the period is
named for begin **in Europe** between 1450 and 1550 — Renaissance `1450.1.1` at Florence (province
116), Colonialism `1500.1.1` at Sevilla (224), Printing Press `1550.1.1` at Frankfurt (1876)
(`common/institutions/00_Core.txt`) — and the Renaissance's embracement bonus is
`development_cost = -0.05`, a standing discount on every subsequent development point. Those bonuses
are country-scoped, so §1.3 excludes them from wealth directly; they reach the map only by changing
how fast development grows, which is the input scaled above.

```

### 11. `R3-routes` - §1.6

X097: the Cape universal narrowed; routes on the (c) field

**Removed:**

```
**And the 1444 map draws the pre-Columbian trade geography unprompted.** The route from Europe to
the sink is the Silk Road: `genua → alexandria → aleppo → persia → lahore → doab → ganges_delta →
burma → gulf_of_siam → canton → hangzhou`. From the north it is the Volga:
`north_sea → white_sea → novgorod → kazan → astrakhan → persia → …`. From the Channel it is the
Hansa and the Danube: `english_channel → lubeck → saxony → wien → venice → ragusa →
constantinople → aleppo → …`. Nothing routes through the Cape, which is what a 1444 map should
say. *(The Cape is not idle — in the per-good graphs it already carries Asian spices to Europe:
`malacca → cape_of_good_hope → zanzibar → gulf_of_aden → alexandria → genua`. `Φ_w` models power,
not cargo; §3.9.)*

```

**Replaced with:**

```
**And the 1444 map draws the pre-Columbian trade geography unprompted.** The route from Genoa to
the Asian sink is the Silk Road: `genua → alexandria → aleppo → persia → lahore → lhasa →
ganges_delta → burma → gulf_of_siam → canton → hangzhou`. From the north it is the Volga, and from
the Channel the Hansa and the Danube. **No Europe→sink route passes the Cape of Good Hope** —
checked from `genua`, `north_sea` and `english_channel` — which is what a 1444 map should say.

The Cape is nonetheless a live conduit, not an idle one: in-degree 1, out-degree 3, with **132
ordered node pairs** whose path runs through it, carrying Atlantic drainage into the Indian Ocean.
*(v5.0 said "nothing routes through the Cape", which is false as a universal and was only ever
checked on the Europe→sink routes.)* In the per-good graphs it also carries Asian spices to Europe;
`Φ_w` models power, not cargo (§3.9).

```

### 12. `R4-dyn` - §1.6

X099/X100: node-set thresholds restated as observations

**Removed:**

```
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

**Replaced with:**

```
Other observations on the same field, for the emitter's benefit rather than as thresholds of the
model: scaling the 22 European *nodes* rather than European provinces makes `genua` the sole sink
from about ×1.65 (the 18-node western/central subset needs about ×2.15), and somewhere inside
roughly ×2.9–×3.5 the Cape of Good Hope **reverses** — 1444's Atlantic→Cape→Indian-Ocean drainage
becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast. The reversal is bounded above as well as
below, so it is a window and not a threshold, and its edges move with the field. *The 22 are the 18
western and central European nodes —* `english_channel`, `north_sea`, `baltic_sea`, `white_sea`,
`novgorod`, `lubeck`, `rheinland`, `saxony`, `wien`, `krakow`, `pest`, `venice`, `ragusa`, `genua`,
`champagne`, `bordeaux`, `valencia`, `sevilla` *— plus* `constantinople`, `crimea`, `kiev` *and*
`kazan`. Dev-stacking a single node's top province concentrates the map on that node; extra sinks at
intermediate boosts are expected behaviour, not noise.

```

### 13. `R4-39` - §3.9

R3: no maintained figures for the superseded aggregate

**Removed:**

```
- The value-weighted **marking order** `Φ_ord = Σ_g V_g·order_g` (v2.0's choice) is acyclic for
  free and remains the most self-coherent aggregate measured: **60.3%** edge-good agreement with
  the per-good graphs against `Φ_w`'s 52.5% (51.5% value-weighted). It was superseded on design
  grounds: its ends are artifacts of sweep scheduling rather than places — of its 13 end nodes at
  1444, 8 terminate no good at all and none of the demand capitals is among them — and its end
  count **never concentrates**: 11–17 ends measured across cloves-α 2…64, never approaching
  vanilla's three. (v2 called this "α-invariant … 9–17 ends", which is neither the right word for
  a quantity that ranges 11–17 nor a band containing its own baseline of 13.) Self-coherence was
  traded for legible, wealth-anchored, world-responsive ends.

```

**Replaced with:**

```
- The value-weighted **marking order** `Φ_ord = Σ_g V_g·order_g` (v2.0's choice) is acyclic for
  free and scores **higher** than `Φ_w` on self-coherence with the per-good graphs — that is the
  cost of the trade and it is not disputed. It was superseded on design grounds: its ends are
  artifacts of sweep scheduling rather than places, a majority of them terminate no good at all,
  none of the demand capitals is among them, and the end count does not concentrate as demand
  concentrates. *No figure is maintained for it here.* It is not the installed operator, its numbers
  moved with every change to the wealth field, and three successive audits spent their effort
  recounting them; the design argument above does not depend on any of them.

```

### 14. `R4-315a` - §3.15

R3: 3.15's Phi_ord entry loses its figures

**Removed:**

```
most self-coherent aggregate measured (**60.3%** vs `Φ_w`'s 52.5%) and still acyclic for free —
but its ends are sweep-scheduling artifacts, not places (§3.9), and no parameter steers their
count. Retained as the measured coherence ceiling any future aggregate should be compared against.
The ceiling is 60.3%, not the 62.7% v2.0 and v2.1 both quoted: that figure predates the
```

**Replaced with:**

```
the most self-coherent aggregate measured — better than `Φ_w` on that one axis, and still acyclic
for free — but its ends are scheduling artifacts rather than places and its end count does not
concentrate with demand (§3.9). *No figures are maintained for it.* v2.0 and v2.1 quoted a
self-coherence ceiling that predates the
```

### 15. `R5-fix` - §3.15

Corrective: 'The the' at the 3.15 edit boundary

**Removed:**

```
**`Φ_ord = Σ_g V_g·order_g` as the installed graph.** *(v2.0 entry, superseded in v2.1.)* The
the most self-coherent aggregate measured — better than `Φ_w` on that one axis, and still acyclic
for free — but its ends are scheduling artifacts rather than places and its end count does not
concentrate with demand (§3.9). *No figures are maintained for it.* v2.0 and v2.1 quoted a
self-coherence ceiling that predates the
deterministic sweep of §3.6 and was never regenerated after it.
```

**Replaced with:**

```
**`Φ_ord = Σ_g V_g·order_g` as the installed graph.** *(v2.0 entry, superseded in v2.1.)* It is
the most self-coherent aggregate measured — better than `Φ_w` on that one axis, and acyclic for
free — but its ends are scheduling artifacts rather than places, and its end count does not
concentrate as demand concentrates (§3.9). *No figures are maintained for it:* it is not installed,
its numbers moved with every change to the wealth field, and the design argument does not rest on
them. The self-coherence ceiling v2.0 and v2.1 quoted predates the deterministic sweep of §3.6 and
was never regenerated after it.
```

### 16. `R5-grav` - §3.15

R3/X190/X191: the gravity kernel keeps its argument, loses its figures

**Removed:**

```
demanders hits any chosen end count exactly for γ ≤ 0.7 and any count up to six — at γ = 0.9 the
four-, five- and six-mass fields all collapse to three ends — with **61%** vanilla-arrow agreement
at its best (γ = 0.90–0.95, 97 of 159 arrows; γ = 0.97 gives 93, and every larger γ is worse).
*v2.1 through v4.0 put the best agreement at γ = 0.97 and said the five- and six-mass fields give
four ends at γ = 0.9; on the corrected wealth field neither holds.* (v2.0 and v2.1 both quoted 69% = 110 of 159, which is not reached at
any γ; the count-follows-seeds behaviour reproduced, that figure did not.) Rejected: it pins
the end count by fiat (a world conquest could never merge the world into one basin), needs a
second operator with its own reach knob γ, and a pure `wealth^α` edge comparison without a reach
term can never concentrate ends at all — a local wealth maximum survives every positive α
(measured: ≥10 ends at α up to 16). The emergent-count wealth good replaced it.
```

**Replaced with:**

```
demanders reproduces whatever end count it is seeded with while γ is small enough, and loses that
property as γ approaches 1. *No figures are maintained for it* — every agreement percentage this
entry carried in v2.0 through v5.0 was measured on a superseded wealth field and each audit spent
its effort recounting them. Rejected on three grounds, none of which is numeric: it pins the end
count by fiat, so a world conquest could never merge the world into one basin; it needs a second
operator with its own reach knob γ; and a pure `wealth^α` edge comparison with no reach term does
not concentrate ends at all, because a local wealth maximum survives every positive α. The
emergent-count wealth good replaced it.
```

### 17. `R6-32` - §3.2

X185/X143: contrast and thresholds in 3.2

**Removed:**

```
regularizer, which §1.2 removes; with no regularizer the spices supply ratio over *producing* nodes
is 36 against a demand ratio of 482.2, which points the other way. Sparsity is the asymmetry that
survives the regularizer's deletion, and the diagnosis rests on it.) No parameter fixes it: α strong enough to matter
destroys §1.4's regime split, and better wealth inputs plausibly deliver about 1.7× (measured:
`genua` becomes a co-sink at ×1.720) — enough to make Genoa a *co-*sink, not enough to make demand
the determinant of placement: a spice sink at any of **the four Chinese trade nodes —
`beijing`, `xian`, `canton`, `hangzhou`** — needs **3.6–4.9×**, i.e. **9.3–21.4%** of all world
spice demand at one node (`beijing` 3.60× / 9.3%, `hangzhou` 3.83× / 21.4%, `xian` 4.59× / 12.3%,
```

**Replaced with:**

```
regularizer, which §1.2 removes. **What the ratio metric cannot see is the thing the diagnosis
rests on.** Sparsity is the asymmetry: most nodes produce nothing at all of a given good — spices
are produced in 18 of 80 nodes and cloves in exactly one — so `(c−s)/deg` is dominated by *where*
supply exists rather than by how large it is, and a max/min ratio over producing nodes is blind to
that by construction. On the contrast metric itself the demand side is the wider one, not the
supply side. No parameter fixes it: α strong enough to matter destroys §1.4's regime split, and
better wealth inputs move Genoa to a *co-*sink at roughly ×1.7 without making demand the determinant
of placement. Moving the spice sink to a Chinese node takes a multiple of that node's demand in the
region of **3.6–4.9×** — observed on the 1444 field (`beijing` 3.61×, `hangzhou` 4.12×, `xian`
4.60×, `canton` 4.77×). The multiple a node needs and the share of world demand it then holds do not
line up end to end, because the share a multiple buys depends on where the node started (
```

### 18. `R6-315` - §3.15

X186/X185: 3.15's Laplacian entry agrees with 3.2

**Removed:**

```
*(v1 and v2 gave the asymmetry as "supply contrast 10⁷ against demand contrast 10²–10³", and v3.0
through v4.0 repeated it here while §3.2 was withdrawing it. §3.2 is right: that ratio was `max(s)`
over v1's ε floor, and with the floor removed the contrasts run **4–97 on supply against
211–20,400 on demand** across the 29 goods — the demand side is the wider one. Sparsity is what
survives the floor's deletion, and it is what the diagnosis rests on.)*
```

**Replaced with:**

```
*(v1 and v2 gave the asymmetry as "supply contrast 10⁷ against demand contrast 10²–10³"; v3.0 and
v4.0 repeated it here while v4.0's own §3.2 was withdrawing it. §3.2 is right — that ratio was
`max(s)` over v1's ε floor. With the floor removed the contrasts run **4–97 on supply against
211–15,010 on demand** over the 28 goods produced in more than one node, so the demand side is the
wider one; `cloves` has a single producer and no contrast to measure, which is the sparsity point in
miniature.)*
```

### 19. `R6-fix` - §3.2

Corrective: close the spice-threshold sentence

**Removed:**

```
4.60×, `canton` 4.77×). The multiple a node needs and the share of world demand it then holds do not
line up end to end, because the share a multiple buys depends on where the node started (
`canton` 4.86× / 17.8%; the four China-region nodes outside that set — `girin`, `yumen`, `chengdu`,
`lhasa` — need 4.0× to 10.8×).
(v2 wrote "1.7× where 4–5× is needed", which compressed two different thresholds into one
comparison and understated what inputs could buy.)
```

**Replaced with:**

```
4.60×, `canton` 4.77×). The multiple a node needs and the share of world demand it then buys do not
line up end to end, because the share depends on where the node started; other nodes in the region
need more still. *(v2 wrote "1.7× where 4–5× is needed", which compressed two different quantities
into one comparison and understated what better inputs could buy.)*
```

### 20. `R7-fallback` - §1.1

X009/X010/X125: what the fallback needs, stated correctly

**Removed:**

```
flow-terminal demander, so the fallback fires only when every candidate is support-isolated with
zero balance — on a connected core, only when `b ≡ 0` across it. That happens for the aggregate
graph on a uniform-wealth map, and for a per-good graph on a component with no producer and no
consumer. In those cases the candidates are usually all *zero-wealth*, the wealth key ties, and the
**index decides** — which is why §2.4 item 1 makes a canonical emitter node order a correctness
requirement rather than a convention, and why §2.8 asserts containment over a set that includes the
fallbacks.
```

**Replaced with:**

```
flow-terminal demander, so the fallback fires only when every candidate is support-isolated with
zero **post-peel** balance. The balance the key reads is the one Phase 0 hands on, with each
pendant's balance folded into its parent — not the raw input `b` — so the condition is about the
folded field and a map with non-zero raw balances can still reach the branch. On a connected core it
needs the folded balance to vanish across the core: for a per-good graph that is a component with no
producer and no consumer, and for the aggregate graph it needs each node's `Σ wealth^α_Φ` to be
equal, which uniform *wealth* gives but is not the same condition. Where the wealth key then ties,
the **node index decides** — that is why §2.8 asserts containment over a set that includes the
fallbacks. It is not the reason §2.4 requires a canonical node order; that requirement is stronger
and is set by Phase 2 (§2.4 item 1).
```

### 21. `R7-order` - §2.4

H1: the canonical-order requirement comes from Phase 2's LP

**Removed:**

```
   it is non-fatal but logs one error per link. **The node order itself is a correctness
   requirement, not a convention**: §1.1's priority key breaks exact ties by node index, and on the
   fallback branch (§3.2, T3) the wealth key ties and the index alone decides the orientation. The
   emitter must therefore fix one canonical node order and keep it stable across rebuilds, or the
   same world can produce two different maps.
```

**Replaced with:**

```
   it is non-fatal but logs one error per link. **The node order itself is a correctness
   requirement, not a convention, and the reason is Phase 2 rather than any tiebreak.** The
   min-cost b-flow is *massively degenerate*: many distinct supports carry the same optimal cost, and
   which one the solver returns depends on the order the nodes and arcs are presented in. Measured on
   1444, relabelling the nodes and running end-to-end changed the orientation on **580 of 580**
   runs (29 goods × 20 relabellings), **always** by returning a different optimal vertex and **never**
   by a sweep tiebreak, with a mean of **22.1 of 159 edges** moving and the objective identical to
   8.9e-16. Independently, permuting only the arc presentation order with node labels held fixed
   changes the optimal support on **10 of 10 goods** tested, with objective gaps ≤ 1.8e-15. Twenty-two
   flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event.

   So the emitter must fix one canonical node order and keep it stable across rebuilds, and that
   order must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks
   ties in. Everything §1.6 and §2.8 report about stability is measured **at fixed node order**;
   under (`α_Φ` fixed) a re-ordering of the same world, the map moves. The specific 580/580 result is
   HiGHS-specific in its detail but not in kind — any simplex returns *a* vertex of a degenerate
   optimal face. Making the orientation independent of presentation order would need a tie-breaking
   objective (a lexicographic secondary cost, or a strictly convex perturbation); that is a design
   change and is not adopted here.

   §1.1's priority key also breaks exact ties by node index, which matters wherever the key ties —
   and the key ties in more places than §1.1 documents: besides the free-edge sweep it decides
   Phase 1's within-cluster argmin, the stall promotion's identical form, and the top-k cut when two
   clusters carry equal mass. **None of them fires on 1444** (zero exact `(DEF, β)` ties on free
   edges across 29/29 goods, zero within-cluster β ties, zero tied cluster masses), so no measured
   figure here depends on them.
```

### 22. `R7-endflag` - §2.4

The end-flag count follows the field

**Removed:**

```
2. **End flags** — `end=yes` on every `Φ_w` sink (1444: **one** end node, `hangzhou`, against
```

**Replaced with:**

```
2. **End flags** — `end=yes` on every `Φ_w` sink (1444: **two** end nodes, `english_channel` and
   `hangzhou`, against
```

### 23. `R7-fix` - §2.4

Corrective: clumsy parenthetical

**Removed:**

```
   under (`α_Φ` fixed) a re-ordering of the same world, the map moves.
```

**Replaced with:**

```
   re-order the same world and the map moves, with `α_Φ` and every input held fixed.
```

### 24. `R8-claim1` - §3.2

X013/X145: T2 satisfies the stated conditions

**Removed:**

```
1. **Sink placement:** on a map where Phase 0 is a no-op and no fallback fires, final sinks =
   `{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal demanders}` — measured exact,
   29/29 goods. **This is a measurement, not a theorem**, and v2 asserted it as a theorem. Three
   constructed inputs break it, all run through a faithful implementation of §1.1 (`toys.py`):
```

**Replaced with:**

```
1. **Sink placement:** on 1444, final sinks = `{selected ∩ flow-terminal} ∪ {stall-promoted
   flow-terminal demanders}` — measured exact, 29/29 goods. **This is a measurement on one input,
   not a theorem**, and v2 asserted it as a theorem. v5.0 tried to rescue it by attaching two
   conditions — Phase 0 a no-op and no fallback firing — and **those conditions are necessary, not
   sufficient**: T2 below satisfies both and still breaks the equality, so the conditioned form is
   no more a theorem than the bare one. Three constructed inputs break it, all run through a
   faithful implementation of §1.1 (`toys.py`):
```

### 25. `R8-index` - §3.2

X016/X151: index-independence, measured on the post-fold key

**Removed:**

```
   no exact ties: zero exact `(DEF, b)` ties on free edges, 29/29 goods on 1444. The one place the
   indexing is load-bearing is the fallback branch (T3 above), where the candidates are typically
   all zero-wealth and tied; §2.4 item 1 makes a canonical node order a correctness requirement for
   that reason.
```

**Replaced with:**

```
   no exact ties: zero exact ties on free edges, 29/29 goods on 1444. Two cautions on that
   measurement. First, the key reads the **post-fold** balance β, the one Phase 0 hands on — so
   peeling can *create* exact ties that the raw input balances do not have, and the 1444 result does
   not transfer to a map where Phase 0 acts. Second, the indexing is load-bearing wherever the key
   ties, which is not only the fallback branch: it also decides Phase 1's within-cluster argmin, the
   stall promotion's identical form, and the top-k cut between clusters of equal mass. None of those
   fires on 1444. **And none of them is why §2.4 requires a canonical node order** — that requirement
   comes from Phase 2's degenerate LP, which moves the orientation under relabelling even when no key
   tie exists anywhere (§2.4 item 1).
```

### 26. `R9-310` - §3.10

D1: exactness not materiality

**Removed:**

```
**This is also why propagation cannot be made per good.** Reading the one installed graph leaves the propagated term good-independent, so the identity survives it untouched — same construction, worst relative disagreement 0 to 3.7e-16. Per-good propagation destroys it, because §1.9 reads a node's *downstream neighbours* and those differ per good. The driver is **not** how many distinct downstream sets a node has, but whether its collectors hold **differing power across the nodes those sets differ on**: `gulf_of_siam` has eight distinct downstream sets and still shows a 0.003% effect, because its collectors hold almost nothing in `burma`, `canton` or `malacca` and every propagation term is near zero. Where the collectors do hold differing power downstream, a country's power at the node stops being one number and `powershare_C` stops factoring out. Measured with each node's real 1444 country table and `collect_pool` built per good throughout: the error is **redistributive and single-digit percent, with the sign varying by collector** — Sevilla −0.82%, −0.87%, **+7.44%**; Champagne −1.69%, +1.69%, +1.53%; Genoa −0.23%, −0.22%, +0.70%. It is not a bias in one direction and it is not rounding: it is thirteen orders of magnitude above the float residual and it moves income between countries. Its size depends on which countries are collecting, which is a stated choice of the construction and not a property of the node, so no single percentage is quoted as one. Keeping propagation on a single graph is load-bearing for Goal 7, not merely convenient. *(v1 through v4.0 quoted "off by 5.96 ducats on a node paying ~250"; no node in the model has local trade value near 250 — the largest is 112.6 — and v4.0's own replacement figure, 0.41%, was an artifact of freezing one term at the alphabetically first commodity.)*
```

**Replaced with:**

```
**This is also why propagation is kept on a single graph.** Reading the one installed graph leaves the propagated term good-independent, so the identity survives it untouched — worst relative disagreement 0 to 3.7e-16, which is 1.7 to 3.3 units in the last place. Per-good propagation destroys the *exactness*, because §1.9 reads a node's downstream neighbours and those differ per good: `gulf_of_siam`'s 29 goods leave it by **seven** distinct downstream sets. Once they differ, a country's power at the node is no longer one number and `powershare_C` no longer factors out, so a single node scalar cannot reproduce every collector's income exactly. **That is the whole of the claim, and it is a claim about exactness, not about magnitude.** How large the error is depends on which scalar you substitute for the per-good share, and that choice is not fixed by the design: substituting the share at one arbitrarily chosen reference commodity gives per-collector errors up to **+7.4%** at `sevilla`, and sweeping which commodity is chosen moves that same collector's error across a **17.8-point** range — so those figures measure the arbitrary choice, not the design. Substituting the quantity an implementation would actually store — the **value-weighted mean share** across the node's goods — the error is **at most 0.1%** at every node measured (`sevilla`, `champagne`, `genua`, `malacca`, `gulf_of_siam`). The honest statement is therefore: per-good propagation costs the exact identity and buys a per-node error that a reasonable scalar keeps within a tenth of a percent, and the identity is what Goal 7 is stated in terms of. *(v1 through v4.0 quoted "off by 5.96 ducats on a node paying ~250"; no node in the model has local trade value near 250. v4.0's replacement, 0.41%, and v5.0's "redistributive and single-digit percent" were both artifacts of freezing the share at one commodity — v5.0 having correctly diagnosed exactly that defect in v4.0. The construction behind any such figure — which countries collect, which transfer, and which commodity's share is frozen — has to be stated with it, and none of those documents stated it.)*
```

### 27. `R10-census` - §3.5

C1/C2/C3: the census, the guard, and the units

**Removed:**

```
(All **161** `change_price` blocks were parsed — 93 in `events/`, 14 in `missions/`, 1 in `common/`
and **53 in `history/`, of which 13 are negative**, all in `history/countries/HAB - Austria.txt`.
v4.0 said 154 and 7: its parser silently recovered nothing from five mission files, which a bare
`except` hid, so the scan is now guarded by a per-file count assertion. The seven recovered blocks
are all positive and the partition is unchanged.
The history route matters: `wool`'s largest single negative is that file's `NEW_DRAPERIES` at
−0.25 for 2.5 → **1.875**, against the −0.20 the same key carries in `events/PriceChanges.txt`, and
`change_price` entries are keyed, so 1.875 is the figure a campaign reaching 1540 holds. v2's 13
was right; v3.0 reached 12 by parsing four of the five trees.)
```

**Replaced with:**

```
(**`change_price` values are fractions of the good's base price, not ducats** — the spec's own
figures only parse under that reading, and the shipped save `tutorial/eu4_tutorial_chapter10.eu4`
settles it: `paper` sits at `current_price=4.375` on a base of 3.5, which is × 1.25 and not + 0.25,
and `gems` at 5.000 on a base of 4.0. So a −0.25 event takes a 2.5 good to 1.875, and grain and wine
reach 0.625.

The install carries **161** textual `change_price` blocks — 93 in `events/`, 14 in `missions/`, 1 in
`common/`, **53 in `history/` of which 13 are negative** (all in
`history/countries/HAB - Austria.txt`), and none in `decisions/`. **Ten of the 161 never execute:**
seven sit inside quoted `effect_tooltip = "…"` strings and three inside `tooltip = { }` display
wrappers, so **151 are executable**. Six of the seven quoted ones duplicate a block already counted
in `events/`, and the seventh names a price key no event in the install ever sets. All ten are
positive and every negative block in the install is executable, so **the partition above is
identical under either census**. *(v4.0 said 154 by silently dropping the quoted seven; v5.0 said
161 by counting them; both were wrong about which number was the executable one. v5.0 also claimed
the scan was "guarded by a per-file count assertion" — there was no assertion anywhere in its
toolchain. `verify6.py` now carries the guard, and the reason a plain parse misses these is
mechanical: `pdx.py` tokenises a quoted string as one opaque unit, so a `change_price` inside a
tooltip string is invisible to the walker.)*

The history route matters: `wool`'s largest single negative is that file's `NEW_DRAPERIES` at −0.25,
against the −0.20 the same key carries in `events/PriceChanges.txt`, and `change_price` entries are
keyed, so 1.875 is the figure a campaign reaching 1540 holds. v2's 13 was right; v3.0 reached 12 by
parsing four of the five trees.)
```

### 28. `R10-caravan` - §1.10

E1: the caravan share, against the right denominator

**Removed:**

```
Measured on the 1444 start: the cap of 50 is **8.6% to 32.0% of an inland node's total trade power** (median 17.9% over the **flag's** 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at
`champagne` — §2.2 derives inland from `members` instead and gets 25, dropping `siberia`; on that
basis the range, the largest-holder span and the count below are all identical and only the median
moves, to 17.5%), against a largest single incumbent holder of **23.6 to 143.2** — so a country at the cap outweighs the largest incumbent in **7 of the 26** inland nodes and is outweighed in the other 19.
```

**Replaced with:**

```
Measured on the 1444 start: the cap of 50 is **9.4% to 47.0% of an inland node's total trade power**, median **21.9%** over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. *(As a share of the node's total **after** the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, median 17.9%; v5.0 quoted those under the first description, which cannot be right, since 8.6% of 532.0 is 45.8 rather than 50. §2.2 derives inland from `members` and gets 25 nodes, dropping `siberia`; on that basis only the median moves, to 21.3%.)* The largest single incumbent holder runs **23.6 to 143.2**, so a country at the cap outweighs the largest incumbent in **7 of the 26** inland nodes and is outweighed in the other 19.
```

### 29. `R11-hdr2` - §0

The v6.0 header

**Removed:**

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

**Replaced with:**

```
**v6.0** keeps v3.0's owner-agnostic wealth and makes it true by construction rather than by a rule
that has to be policed. Its substantive change is to §1.3: **wealth is a function of the province's
development, its trade good and its own current condition, and of nothing else.** The two-test
modifier classifier and everything it governed — the trade-good modifiers, great projects, permanent
province modifiers, buildings, centres of trade and the DLC conditionality — are deleted, along with
the whole-install sweep that maintained them. On the 1444 start that apparatus was worth 0.98% of
world wealth; what it cost was an input surface whose classification was wrong in every audit that
examined it. Three start-state reads are corrected in the same pass (`on_startup` devastation, dated
`add_base_*` accumulation, and the `is_city` filter the engine does not apply), and §2.4 now states
the reason a canonical node order is a correctness requirement: **Phase 2's min-cost flow is
degenerate, so presentation order selects which optimum is returned.**

Two conventions govern the prose. **No empirical absolutes** — no superlative, no universal
quantifier and no threshold asserted as a fact about the world; a claim is either a directional
design statement or an observation scoped to the field and script that produced it. **No maintained
figures for rejected operators** — `Φ_ord`, the gravity kernels and the v1 Laplacian keep their
graveyard entries in §3.15 and lose their numbers, which were re-measured and re-refuted in three
successive audits without any design argument depending on them.

Every graded claim from `../v5-owner-agnostic/validation-v5.md` — 22 refuted, 39 partial, 1
unverifiable — is folded through; `fixes-agreed.md` maps each one to the change that answers it.
Deleted text is quoted in `changes-v6.md`. Measured figures carry the script that produced them, and
`scripts/verify6.py` re-derives each one **from the document text** and fails if the two disagree.
```

### 30. `R11-cooldown` - §1.10

E8/X106: the shipped cooldowns absorb some chatter

**Removed:**

```
only on its flag ladder. So almost nothing absorbs threshold chatter — a power share oscillating
across any single-valued limit flickers the mechanic, and that includes Propagate Religion for the
flagless countries its default and terminal branches cover.
```

**Replaced with:**

```
only on its flag ladder. So banding absorbs very little chatter — a power share oscillating across
any single-valued limit flickers the mechanic, and that includes Propagate Religion for the flagless
countries its default and terminal branches cover. **Banding is not the only damper, though:** three
shipped defines rate-limit the mechanics that carry these thresholds —
`TRADING_POLICY_COOLDOWN_MONTHS = 12` (both banded policies), and
`TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` with `TRADE_COMPANY_COOLDOWN = 60` — so a flickering share
does not translate into a flickering *effect* at those three. What is left exposed is everything
without a cooldown, which is most of the ladder.
```

### 31. `R11-timing` - §2.2

E7/X114: a wall-clock timing is an order of magnitude

**Removed:**

```
**0.17–0.21 s for all 29 goods, a mean of 5.7–7.3 ms per good across runs** — individual goods
range 5.4–24 ms, so 7.3 is an average and not a maximum. "Milliseconds each" therefore holds
already,
```

**Replaced with:**

```
**of order 0.1 s for all 29 goods, and single-digit milliseconds per good on average.** Repeated
runs on one machine span roughly 0.09–0.27 s for the full set and 3–7 ms per good as an average,
with individual goods reaching about 20 ms — so a two-significant-figure range is a statement about
a machine and a scheduler rather than about the algorithm, and none is quoted. *(v5.0 quoted
"0.17–0.21 s"; twelve fresh runs put only one inside that interval.)* "Milliseconds each" therefore
holds already,
```

### 32. `R11-ulp` - §3.10

E5/X166: 3.7e-16 is not one ULP

**Removed:**

```
worst relative disagreement 0 to 3.7e-16, which is 1.7 to 3.3 units in the last place.
```

**Replaced with:**

```
worst relative disagreement 0 to 3.7e-16 — one to three units in the last place, not the single
ULP v5.0 claimed.
```

### 33. `R11-hdr` - §0

The v6.0 banner and lineage

**Removed:**

```
**Version:** 5.0
```

**Replaced with:**

```
**Version:** 6.0
```

### 34. `R12-coal` - §1.5

The coal activation, on the (c) field

**Removed:**

```
latent-coal provinces that are owned at 1444 — §1.3 counts only owned provinces — flips **29 of
159 `Φ_w` edges** (`v5measure.py`).
```

**Replaced with:**

```
latent-coal provinces that are owned at 1444 — §1.3 counts only owned provinces — flips **13 of
159 `Φ_w` edges** and adds 217 ducats to world wealth (`measure6.py`).
```

### 35. `R12-coal2` - §2.8

2.9's copy of the same figure

**Removed:**

```
Measured: repricing the 45 owned latent-coal provinces flips 29 of 159 `Φ_w` edges (§1.5) |
```

**Replaced with:**

```
Measured: repricing the 45 owned latent-coal provinces flips 13 of 159 `Φ_w` edges (§1.5) |
```

### 36. `R12-script` - §1.1

Script attribution

**Removed:**

```
(`drain-orientation.md`; regenerated for v5.0 by `v5measure.py`).
```

**Replaced with:**

```
(`drain-orientation.md`; regenerated for v6.0 by `measure6.py`).
```

### 37. `R12-open` - §3.13

The open-question banner

**Removed:**

```
**Open in the v5.0 wealth model.**
```

**Replaced with:**

```
**Open in the v6.0 wealth model.**
```

### 38. `R13-11` - §1.1

1.1's per-good summary on the (c) field

**Removed:**

```
  `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods on 1444, 1–7 sinks per
  good, mean 3.6, zero fallbacks.
```

**Replaced with:**

```
  `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods on 1444, 1–8 sinks per
  good, mean 3.52, zero fallbacks.
```

### 39. `R13-scale` - §1.6

The scale test on the (c) field

**Removed:**

```
×1 and above, 16 edge flips at ×10⁻², and 83 at ×10⁻⁶ — the orientation degrades while the sink
```

**Replaced with:**

```
×1 and above, 12 edge flips at ×10⁻², and 100 at ×10⁻⁶ — the orientation degrades while the sink
```

### 40. `R13-bw` - §1.6

Largest |b_w| on the (c) field

**Removed:**

```
Normalising into (−1, 1) scales 1444's `b_w` *up* (its largest magnitude is 0.0227) and is safe;
```

**Replaced with:**

```
Normalising into (−1, 1) scales 1444's `b_w` *up* (its largest magnitude is 0.0226) and is safe;
```

### 41. `R13-28` - §2.8

2.8's per-good row and the two agreement figures

**Removed:**

```
| Most goods, 1444 | Sinks are `{selected ∩ flow-terminal} ∪ promoted` (§1.1) — 1 to 7 per good; high-demand nodes are sinks at 14.5% in the top demand de
```

**Replaced with:**

```
| Most goods, 1444 | Sinks are `{selected ∩ flow-terminal} ∪ promoted` (§1.1) — 1 to 8 per good; high-demand nodes are sinks at 16.8% in the top demand de
```

### 42. `R13-agree` - §2.8

2.8's agreement baseline on the (c) field

**Removed:**

```
  baseline is known — `Φ_w` agrees with the per-good graphs on **51.5%** of edge-goods *weighted by
  trade value*, and on 52.5% unweighted (§1.6) —
```

**Replaced with:**

```
  baseline is known — `Φ_w` agrees with the per-good graphs on **52.1%** of edge-goods *weighted by
  trade value*, and on 53.5% unweighted (§1.6) —
```

### 43. `R13-rank` - §3.15

3.15's RANK comparison on the (c) field

**Removed:**

```
sink–demand *alignment* statistic (ρ_val +0.281 against DRAIN's +0.054; 43.8% of top-decile nodes
are sinks against 14.5%)
```

**Replaced with:**

```
sink–demand *alignment* statistic — it puts a far higher share of top-demand nodes in its sink sets
than DRAIN does
```

### 44. `R13-rank2` - §3.15

3.15's RANK sink range

**Removed:**

```
sinks per good against DRAIN's 1–7.
```

**Replaced with:**

```
sinks per good against DRAIN's 1–8.
```

### 45. `R14-conn` - §3.8

The connectivity figure on the (c) field

**Removed:**

```
would cover most of the map — measured, **92.2%** (5825 of 6320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. (v2 quoted 98.8%; that is v1's *Laplacian* figure, 6245/6320, carried across the operator change without being re-measured. The argument is unaffected — 92.2% is still most of the map — but the number was not v2's own.)
```

**Replaced with:**

```
would cover most of the map — measured, **90.2%** (5,703 of 6,320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. (v2 quoted 98.8%; that is v1's *Laplacian* figure, 6245/6320, carried across the operator change without being re-measured. The argument is unaffected — 90.2% is still most of the map — but the number was not v2's own.)
```

### 46. `R15-23` - §2.3

R2 + contradiction: 2.3's alpha paragraph

**Removed:**

```
the aggregate-graph exponent `α_Φ = 1.5` (a constant like `P₀`; world-responsiveness flows through
wealth, never through this knob). **Its stated calibration is withdrawn.** v2.1 through v4.0 said
1.5 was "calibrated so the 1444 start yields the two-sink hangzhou/english_channel map"; on the
corrected wealth field of §1.3 it does not yield that map, and the α_Φ window that does yield it is
narrower than the uncertainty in its own edges under ±1% wealth noise (§1.6). 1.5 is retained because it sits inside the widest sink-count band
and nothing now selects a different value — not because it was derived. Any future change to it is
a design decision about how many ends the installed graph should have, and should be recorded as
one, and DRAIN's three knobs at their defaults
```

**Replaced with:**

```
the aggregate-graph exponent `α_Φ = 1.5` (a **stipulated** constant like `P₀`: superlinear, round,
and chosen rather than derived — world-responsiveness flows through wealth, never through this
knob). **Every derivation previously offered for it is withdrawn.** v2.1 through v4.0 said 1.5 was
calibrated so that 1444 yields a two-sink map; v5.0 said it sat in the widest sink-count band.
Neither is a reason: the first fits a constant to one date, and the second depended on where the α
scan was truncated (§1.6). Any future change to it is a design decision about how many ends the
installed graph should have, and should be recorded as one, and DRAIN's three knobs at their
defaults
```

### 47. `R15-16count` - §1.6

X065 + contradiction: the count is not set by alpha alone

**Removed:**

```
the sinks are wherever the wealth flow terminates. **Their count is set by `α_Φ`; only their
```

**Replaced with:**

```
the sinks are wherever the wealth flow terminates. **Both their count and their locations move with
the wealth field, and `α_Φ` sets how sharply concentration is read.** At the stipulated α_Φ = 1.5
the 1444 field gives two sinks and a modestly grown Europe gives three or one (§1.6's Europe table),
so neither the count nor the placement is fixed by the constant. *(v2.0 through v4.0 said the count
"emerges from concentration"; v5.0 over-corrected to "the count is set by `α_Φ`". Both are wrong in
the same way — the count is a function of the field **and** the constant, and only their
```

### 48. `R15-bandref` - §1.6

The two dangling 'band table below' references

**Removed:**

```
of it (the band table below), and v2.1 chose the value with a target count in view — a calibration
§2.3 now withdraws, since the ground on which 1.5 is *retained* is the band table and not that
target. What the world
```

**Replaced with:**

```
of it, and v2.1 chose the value with a target count in view — a calibration §2.3 withdraws without
replacing, since `α_Φ` is stipulated rather than derived. What the world
```

### 49. `R15-39` - §3.9

R3 + contradiction: 3.9's adoption note

**Removed:**

```
  the wealth actually is, so they move when the wealth moves (§1.6's institution result). *v2.1
  through v4.0 justified the adoption by "two vanilla-like ends at 1444" — the reason it was
  accepted despite losing self-coherence. On the corrected wealth field there is one end, in China,
  matching none of vanilla's three, so that premise is withdrawn. The trade is now stated as what it
  is: 7.8 points of self-coherence given up for one operator and world-responsive ends, and the
  1444 count is whatever the field gives.*
```

**Replaced with:**

```
  the wealth actually is, so they move when the wealth moves (§1.6). *v2.1 through v4.0 justified the
  adoption by "two vanilla-like ends at 1444" — a resemblance to vanilla's authored map. That is not
  the argument, and it should not be revived even though the 1444 field again gives two ends: the
  count is a property of the field, not of the operator, and pinning the operator to it would be the
  calibration §2.3 withdrew. What the trade actually costs is self-coherence with the per-good
  graphs, which the superseded marking-order aggregate scores higher on; what it buys is one
  operator, one set of guarantees, and ends that sit where the wealth is.*
```

### 50. `R15-ulp` - §3.10

3.10 contradicted itself two paragraphs apart

**Removed:**

```
agree to a worst relative disagreement of **0 to 3.7e-16** — at most one unit in the last place.
```

**Replaced with:**

```
agree to a worst relative disagreement of **0 to 3.7e-16** — one to three units in the last place.
```

### 51. `R15-dev` - §1.3

Ten vs eleven devastated provinces

**Removed:**

```
**They are not all quiet at the 1444 start.** Ten provinces begin devastated — Bohemia at 50 and
```

**Replaced with:**

```
**They are not all quiet at the 1444 start.** Eleven counted provinces begin devastated — Bohemia at 50 and
```

### 52. `R16-313` - §3.13

3.13 kept the classifier and its flat-bonus count

**Removed:**

```
- **What else multiplies `goods_produced`, and which side of the owner line does each source fall
  on?** §1.3's classification handles the sources observed so far — the owner's
  `global_trade_goods_size_modifier` (out, country-scoped) and `bonus_from_merchant_republics`
  (out, its value set by neighbouring countries' government forms) — and §1.3's whole-install sweep
  settles the additive block too: **fifteen** 1444 provinces carry a flat `trade_goods_size`, five
  from great projects and ten from permanent province modifiers. What is unenumerated is the
  rest of the surface: `trade_goods_size` and `trade_goods_size_modifier` appear in buildings,
  estate privileges, government reforms, church aspects, fervor, ages and event modifiers, and
  each source needs the §1.3 locality test applied to it before a modded or late-game province can
  be priced. Settling work: enumerate every source of both keys and classify each; the model needs
  the answer only for sources that can be live with no owner input.
```

**Replaced with:**

```
- **Should any source beyond province condition be allowed to multiply `goods_produced`?** §1.3
  reads development, the trade good and the four province-state modifiers, and nothing else — so
  this is now a **design** question rather than a classification one. The keys
  `trade_goods_size` and `trade_goods_size_modifier` are granted in many places (buildings, event
  modifiers, great projects, static and province-triggered modifiers, holy orders, state edicts,
  trade-company investments), and v3.0 through v5.0 tried to admit the province-scoped subset by
  rule. That rule was wrong in every audit that examined it, which is why v6.0 drops it. Re-admitting
  any of those sources means re-admitting the maintenance burden with it, and the question to settle
  first is whether the fidelity is worth it — on the 1444 start the whole set was worth 0.98% of
  world wealth.
```

### 53. `R16-28razed` - §2.8

2.8's razed-China row, on the v6 field

**Removed:**

```
| Razed China | Zeroing `hangzhou`-node development relocates the sink in one solve — measured: the `Φ_w` sinks move from `{hangzhou}` to `{doab, english_channel, gulf_of_siam, sevilla}`, 22 of 159 edges flipping. `hangzhou`, not `beijing`, is China's wealth pole under §1.3: `c_w` rank 1 against `beijing`'s 31, node wealth 245.0 against 143.8, and it holds the richest single province in the game. Zeroing `beijing` **also** moves the map — 17 flips, sinks `{doab, english_channel, hangzhou, sevilla}` — because deleting 1.3% of world wealth renormalises `c_w` everywhere; what separates the two is that `hangzhou` **survives as a sink** when `beijing` is zeroed and does not when `hangzhou` is. *(v2 through v4.0 said zeroing `beijing` "moves nothing". It does. The rank gap is what carries this row, not a null result.)* |
```

**Replaced with:**

```
| Razed China | Zeroing `hangzhou`-node development relocates an end in one solve — measured: the `Φ_w` sinks move from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`, 23 of 159 edges flipping. `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth 226.7 against 143.0, and it holds the richest single province the model counts. Zeroing `beijing` **also** moves the map — 15 flips — because deleting a percent of world wealth renormalises `c_w` everywhere; what separates the two is that `hangzhou` **survives as a sink** when `beijing` is zeroed and does not when `hangzhou` is. *(v2 through v4.0 said zeroing `beijing` "moves nothing". It does; the asymmetry is which node keeps its end, not whether the map moves.)* |
```

### 54. `R16-39wealth` - §3.9

3.9's node wealths on the v6 field

**Removed:**

```
— 296.0, 299.2 and 266.5 against `english_channel`'s 316.6 — and none of them is a sink —
```

**Replaced with:**

```
— 296.0, 297.9 and 266.5 against `english_channel`'s 316.6, which is a sink —
```

### 55. `R16-313cal` - §3.13

3.13's cloves calibration on the v6 field

**Removed:**

```
  Deccan, **demand rank 2** under α = 16 with the rank-1 demander `hangzhou` acting as a transit
  node, becomes the cloves sink; v2 said Beijing "holds the richest single province", which it
  does not — that is `hangzhou`, at 30.4 against Beijing's 19.5, and under this calibration Beijing
  is only demand rank 3), the tolerance re-routes arcs
```

**Replaced with:**

```
  under α = 16 the cloves demand order is `hangzhou`, `beijing`, `doab`, and the sink lands on a
  high-demand node rather than a geographic accident; v2 said Beijing "holds the richest single
  province", which it does not — that is `hangzhou`), the tolerance re-routes arcs
```

### 56. `R16-34` - §3.4

R3: 3.4's v1 identity figures

**Removed:**

```
agreement collapsing from 159/159 to 68/159; the identity is gone in v2 but the reason to refuse
```

**Replaced with:**

```
agreement collapsing to well under half the map; the identity is gone in v2 but the reason to refuse
```

### 57. `R16-316` - §3.16

R3: 3.16's v1 tolerance figure

**Removed:**

```
   the identity failed at 1e-5 and would have been diagnosed as a solver bug.
```

**Replaced with:**

```
   the identity failed at the tolerance v1 used and would have been diagnosed as a solver bug.
```

### 58. `R17-11` - §1.1

1.1 asserted the conditioned equality 3.2 demolishes

**Removed:**

```
  or a Phase-0 pendant that absorbed a net-importing subtree. On a map where Phase 0 is a no-op and
  no fallback fires, the last two cases are empty and the sink set is exactly
  `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods on 1444, 1–8 sinks per
  good, mean 3.52, zero fallbacks. **That equality is not a theorem in general**, and v2 asserted it
  as one.
```

**Replaced with:**

```
  or a Phase-0 pendant that absorbed a net-importing subtree. On 1444 the last two cases are empty
  and the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29
  goods, 1–8 sinks per good, mean 3.52, zero fallbacks. **That equality is a measurement on this
  input, not a theorem**, and v2 asserted it as one. It does not become a theorem by attaching
  conditions either: "Phase 0 a no-op and no fallback firing" looks sufficient and is not — **T2**
  below satisfies both and still breaks it (§3.2).
```

### 59. `R17-22a` - §2.2a

2.2a said peeling cannot create key ties; 3.2 now denies it

**Removed:**

```
| Free-edge determinism (§1.1) | proved as determinism; **measured** as independence from the node indexing (zero exact `(DEF, b)` ties, 29/29 goods) | same in both halves — peeling does not touch the priority key |
```

**Replaced with:**

```
| Free-edge determinism (§1.1) | proved as determinism; **measured** as independence from the node indexing (zero exact ties, 29/29 goods) | the determinism half is unaffected; the index-independence half is **not** — the key reads the post-fold balance β, so peeling can create exact ties the raw balances do not have, and the 1444 measurement does not transfer (§3.2) |
```

### 60. `R18-coal` - §1.5

R2: the coal superlative gets its scope and source

**Removed:**

```
Coal's base price of 10.0 is the highest in vanilla, so this is
```

**Replaced with:**

```
Coal's base price of 10.0 is the highest in the shipped price table
(`common/prices/00_prices.txt`, `measure6.py`), so this is
```

### 61. `R18-owner` - §1.3

R2: an unmeasurable superlative

**Removed:**

```
trade goods and prices do. It also removes the single largest source of hidden owner-dependence
```

**Replaced with:**

```
trade goods and prices do. It also removes a large source of hidden owner-dependence
```

### 62. `R18-19` - §2.7

R2: mark the upstream reading as one observation

**Removed:**

```
  as written and gains no qualifier. §3.16's cautionary case closes.
```

**Replaced with:**

```
  with that reading — one observation on one node, enough to retire the cautionary case and not
  enough to promote the rule to a measurement. §3.16's cautionary case closes.
```

### 63. `R18-19b` - §2.7

R2: and the lead-in

**Removed:**

```
`Transfers from traders downstream: +3.1`. §1.9's "every immediately upstream node" is correct
```

**Replaced with:**

```
`Transfers from traders downstream: +3.1`. §1.9's "every immediately upstream node" is consistent
```

### 64. `R18-attr` - §1.3

Script attribution: devastation

**Removed:**

```
ducats** across the eleven affected counted provinces. The chain is
```

**Replaced with:**

```
ducats** across the eleven affected counted provinces (`measure6.py`). The chain is
```

### 65. `R18-attr2` - §1.3

Script attribution: the deleted apparatus

**Removed:**

```
On the 1444 start that whole apparatus was worth **0.98%** of world wealth over 87 of
2,472 provinces,
```

**Replaced with:**

```
On the 1444 start that whole apparatus was worth **0.98%** of world wealth over 87 of
2,472 provinces (`measure6.py`),
```

### 66. `R18-attr3` - §2.4

Script attribution: the degeneracy figures

**Removed:**

```
   changes the optimal support on **10 of 10 goods** tested, with objective gaps ≤ 1.8e-15.
```

**Replaced with:**

```
   changes the optimal support on **10 of 10 goods** tested, with objective gaps ≤ 1.8e-15
   (the field from `measure6.py`; the relabelling sweep is recorded in
   `../v5-owner-agnostic/validation-v5.md`).
```

### 67. `R18-attr4` - §1.6

Script attribution: the Cape figure

**Removed:**

```
ordered node pairs** whose path runs through it, carrying Atlantic drainage into the Indian Ocean.
```

**Replaced with:**

```
ordered node pairs** whose path runs through it (`measure6.py`), carrying Atlantic drainage into the
Indian Ocean.
```

### 68. `R19-r3` - §0

R3 named only three operators; RANK and BASIN were regenerated

**Removed:**

```
figures for rejected operators** — `Φ_ord`, the gravity kernels and the v1 Laplacian keep their
graveyard entries in §3.15 and lose their numbers, which were re-measured and re-refuted in three
successive audits without any design argument depending on them.
```

**Replaced with:**

```
figures for any rejected operator** — §3.15's graveyard keeps its design arguments and loses its
measurements. That covers `Φ_ord`, the gravity kernels, the v1 Laplacian, RANK, the seeded basins and
anything else the section rejects: those numbers were re-measured and re-refuted in three successive
audits and not one of the rejection arguments depends on them. Where a comparison is genuinely
load-bearing it is stated as a direction ("scores higher on self-coherence", "does not concentrate
its ends") rather than as a figure that has to be maintained across every change to the wealth
field.
```

### 69. `R19-rank` - §3.15

R3: RANK's maintained figures

**Removed:**

```
every route — 83.0% of demand reachable, 31 orphan sinks, Genoa a cloves sink that cloves cannot
reach. It also posts **8 net-producer sinks** where DRAIN, LAP and FLOW all post zero, and 10–16
sinks per good against DRAIN's 1–8. *v2 said it "wins every sink statistic"; it does not — it wins
the alignment ones and loses the rest.*
```

**Replaced with:**

```
every route, so a sixth of world demand is stranded, it leaves orphan sinks a good cannot reach
(Genoa as a cloves sink that cloves never reach), it posts net-producer sinks where DRAIN, LAP and
FLOW post none, and it keeps several times DRAIN's sinks per good. *v2 said it "wins every sink
statistic"; it does not — it wins the alignment ones and loses delivery, which is the one the model
needs.*
```

### 70. `R19-basin` - §3.15

R3: BASIN's maintained figure

**Removed:**

```
chosen seeds and starves everything off a supply→seed path; 88.4% reach at its best tuning. Its
```

**Replaced with:**

```
chosen seeds and starves everything off a supply→seed path, leaving demand unserved at every tuning
tried. Its
```

### 71. `R20-16` - §1.6

The mangled parenthetical in 1.6, stated twice

**Removed:**

```
the sinks are wherever the wealth flow terminates. **Both their count and their locations move with
the wealth field, and `α_Φ` sets how sharply concentration is read.** At the stipulated α_Φ = 1.5
the 1444 field gives two sinks and a modestly grown Europe gives three or one (§1.6's Europe table),
so neither the count nor the placement is fixed by the constant. *(v2.0 through v4.0 said the count
"emerges from concentration"; v5.0 over-corrected to "the count is set by `α_Φ`". Both are wrong in
the same way — the count is a function of the field **and** the constant, and only their
locations are emergent.** v2.0 through v4.0 said the count "emerges from concentration exactly as
per-good sink counts do" — it does not: `α_Φ` is a stipulated constant, the count is a step function
of it, and v2.1 chose the value with a target count in view — a calibration §2.3 withdraws without
replacing, since `α_Φ` is stipulated rather than derived. What the world
state moves is *where* the sinks are and *how the map drains toward them*, which is the property
§3.1's first goal actually asks for.
```

**Replaced with:**

```
the sinks are wherever the wealth flow terminates. **Both their count and their locations move with
the wealth field, and `α_Φ` sets how sharply concentration is read.** At the stipulated α_Φ = 1.5 the
1444 field gives two sinks, and a modestly grown Europe gives three or one (the Europe table below),
so neither the count nor the placement is fixed by the constant. *(v2.0 through v4.0 said the count
"emerges from concentration exactly as per-good sink counts do"; v5.0 over-corrected to "the count is
set by `α_Φ`". Both are wrong the same way — the count is a function of the field **and** the
constant. v2.1 also chose the value with a target count in view, a calibration §2.3 withdraws
without replacing.)* What the world state moves is *where* the sinks are and *how the map drains
toward them*, which is the property §3.1's first goal actually asks for.
```

### 72. `R20-13c` - §1.3

§1.3's claim that neither coefficient is in a file

**Removed:**

```
`GP_COEFF` and `TAX_COEFF` are in §2.3. Both were measured from the running game, not assumed:
neither is a define (`defines.lua` was searched), so both are engine constants recovered by
observation and each carries the observation that produced it.
```

**Replaced with:**

```
`GP_COEFF` and `TAX_COEFF` are in §2.3, and they have different provenance. **`GP_COEFF` is a
shipped file value** — `common/static_modifiers/00_static_modifiers.txt` carries
`provincial_production_size = { trade_goods_size = 0.2 … }`, localised "Base Production", which is
the same tooltip line the coefficient was measured off. It is therefore moddable and is **read at
runtime**, not hardcoded. `TAX_COEFF` is in no file that has been found — neither `defines.lua`,
`common/defines/`, nor that static-modifier block — so it stays a measured constant carrying the
observation that produced it.
```

### 73. `R20-23c` - §2.3

§2.3's 'neither is a define' heading and claim

**Removed:**

```
**Engine constants that are not defines.** The two wealth coefficients of §1.3 are hardcoded in
the binary — `defines.lua` and `common/defines/` were searched and contain neither. They are
therefore *measured*, and each is recorded with the observation that produced it. Re-measure them
against any patch that is not 1.37.5.
```

**Replaced with:**

```
**The two wealth coefficients, and where each comes from.** They are not the same kind of constant.
**`GP_COEFF` is a shipped file value**, in `common/static_modifiers/00_static_modifiers.txt` as
`provincial_production_size = { trade_goods_size = 0.2 … }` and localised "Base Production" — the
very line it was measured off. The emitter **reads it** rather than carrying 0.2, because a mod or a
patch can change it. **`TAX_COEFF` is not in any file that has been found** — `defines.lua`,
`common/defines/` and the static-modifier tables were searched — so it remains a measured constant
and must be re-measured against any patch that is not 1.37.5. *(v3.0 through v5.0 said neither
coefficient was in a file, and shipped a whole-install modifier sweep that walked past the block
holding one of them.)*
```

### 74. `R20-ten` - §1.3

'the devastated ten' against 'eleven counted provinces'

**Removed:**

```
   that line — province 265 is one, and it is also one of the devastated ten — and the engine treats
```

**Replaced with:**

```
   that line — province 265 is one, and it is also one of the devastated eleven — and the engine treats
```

### 75. `N01` - §2.2

World wealth on the rolled-goods field

**Removed:**

```
   `c` with per-province α, and the per-good balance `b = s − c`.
```

**Replaced with:**

```
   `c` with per-province α, and the per-good balance `b = s − c`. World wealth is **10,607.40**
   annual ducats over **2,472** counted provinces.
```

### 76. `N01b` - §2.2

The old world-wealth sentence

**Removed:**

```
`GP_COEFF` is **read from**
   `common/static_modifiers/00_static_modifiers.txt` rather than hardcoded (§2.3). World wealth is
   **10,594.70** annual ducats over **2,472** counted provinces. Then per-node `trade_value`, `s`,
```

**Replaced with:**

```
`GP_COEFF` is **read from**
   `common/static_modifiers/00_static_modifiers.txt` rather than hardcoded (§2.3). Then per-node
   `trade_value`, `s`,
```

### 77. `M-a` - §1.3

The twenty unknown-good provinces are read, not zeroed

**Removed:**

```
**Twenty counted provinces have no trade good in their history file** (`trade_goods = unknown`); the
engine assigns one at start from each good's `chance = { }` block. The wealth field is therefore
partly the result of one random draw. The model does not try to predict the draw: it reads whatever
the game's current state holds, which is what it does for development too.
```

**Replaced with:**

```
**Twenty counted provinces have no trade good in their history file** (`trade_goods = unknown`); the
engine assigns one at start from each good's `chance = { }` block. The model does not predict the
draw — it **reads the good the engine actually rolled**, which is what it does for development too,
and prices the province on that. Pricing them at zero instead understates world wealth by 12.70
ducats. The draw is real, so the field is one sample: on this save the twenty came up seven `fur`,
five `grain`, three `wool`, two `livestock`, and one each of `cotton`, `incense` and
`naval_supplies`. A different roll gives a slightly different field, and nothing in the model depends
on which one.
```

### 78. `N03` - §1.3

The deleted apparatus, counted on the rolled-goods field

**Removed:**

```
On the 1444 start that whole apparatus was worth **0.98%** of world wealth over 87 of
2,472 provinces (`measure6.py`),
```

**Replaced with:**

```
On the 1444 start that whole apparatus was worth **0.98%** of world wealth over **89** of the 2,472
counted provinces — 43 `gems` plus 31 `incense` plus 16 great-project and permanent-modifier
provinces, less one that is both (province 542). *The count depends on the field: it is 87 under the
withdrawn `is_city` filter, and 89 rather than 88 because province 4856 is one of the twenty whose
good the engine rolls, and it rolled `incense`.*
```

### 79. `N04` - §1.6

Largest |b_w|

**Removed:**

```
largest `|b_w|` **0.0226**;
```

**Replaced with:**

```
largest `|b_w|` **0.0225**;
```

### 80. `N04b` - §1.6

The scale note's |b_w|

**Removed:**

```
(its largest magnitude is 0.0226)
```

**Replaced with:**

```
(its largest magnitude is 0.0225)
```

### 81. `N05` - §1.1

Sinks per good, 1.1

**Removed:**

```
  goods, 1–8 sinks per good, mean 3.52, zero fallbacks.
```

**Replaced with:**

```
  goods, 1–8 sinks per good, mean 3.72, zero fallbacks.
```

### 82. `N05b` - §1.6

Sinks per good, 1.6

**Removed:**

```
Per good, on the same field: **1–8 sinks, mean 3.52**,
```

**Replaced with:**

```
Per good, on the same field: **1–8 sinks, mean 3.72**,
```

### 83. `N06` - §1.6

Self-coherence

**Removed:**

```
Agreement with the per-good graphs is **53.5%** of edge-goods (**52.1%** value-weighted).
```

**Replaced with:**

```
Agreement with the per-good graphs is **53.6%** of edge-goods (**52.3%** value-weighted).
```

### 84. `N06b` - §2.8

2.8's copy of the agreement figures

**Removed:**

```
  baseline is known — `Φ_w` agrees with the per-good graphs on **52.1%** of edge-goods *weighted by
  trade value*, and on 53.5% unweighted (§1.6) —
```

**Replaced with:**

```
  baseline is known — `Φ_w` agrees with the per-good graphs on **52.3%** of edge-goods *weighted by
  trade value*, and on 53.6% unweighted (§1.6) —
```

### 85. `N08` - §3.8

Connectivity

**Removed:**

```
would cover most of the map — measured, **90.2%** (5,703 of 6,320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN.
```

**Replaced with:**

```
would cover most of the map — measured, **89.6%** (5,663 of 6,320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN.
```

### 86. `N08b` - §3.8

The argument-unaffected clause

**Removed:**

```
The argument is unaffected — 90.2% is still most of the map
```

**Replaced with:**

```
The argument is unaffected — 89.6% is still most of the map
```

### 87. `N09` - §1.6

The widest alpha band

**Removed:**

```
scanned over [1, 8] rather than [1, 3], the widest band is **1.70** wide ([3.51, 5.21],
```

**Replaced with:**

```
scanned over [1, 8] rather than [1, 3], the widest band is **1.71** wide ([3.50, 5.21],
```

### 88. `N10` - §1.5

The coal activation, holding devastation fixed

**Removed:**

```
latent-coal provinces that are owned at 1444 — §1.3 counts only owned provinces — flips **13 of
159 `Φ_w` edges** and adds 217 ducats to world wealth (`measure6.py`).
```

**Replaced with:**

```
latent-coal provinces that are owned at 1444 — §1.3 counts only owned provinces — flips **10 of
159 `Φ_w` edges** and adds 214.60 ducats to world wealth (`measure6.py`). *The counterfactual holds
every non-repriced input fixed, which matters by more than rounding: province 4237 is both
latent-coal and one of the devastated eleven, and a reprice that drops its devastation measures coal
activating **plus** one province healing — worth 2.40 ducats and 3 extra flips.*
```

### 89. `N12` - §1.10

The caravan medians, both bases

**Removed:**

```
Measured on the 1444 start: the cap of 50 is **9.4% to 47.0% of an inland node's total trade power**, median **21.9%** over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. *(As a share of the node's total **after** the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, median 17.9%; v5.0 quoted those under the first description, which cannot be right, since 8.6% of 532.0 is 45.8 rather than 50. §2.2 derives inland from `members` and gets 25 nodes, dropping `siberia`; on that basis only the median moves, to 21.3%.)*
```

**Replaced with:**

```
Measured on the 1444 start: the cap of 50 is **9.4% to 47.0% of an inland node's total trade power**, median **21.6%** over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. *(As a share of the node's total **after** the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, median 17.7%; v5.0 quoted those under the first description, which cannot be right, since 8.6% of 532.0 is 45.8 rather than 50. §2.2 derives inland from `members` and gets 25 nodes, dropping `siberia`; on that basis the median is 21.3%, or 17.5% after the grant.)*
```

### 90. `N14` - §1.3

The development range at 1444

**Removed:**

```
provinces at `base_tax` 2 and 6, are what `TAX_COEFF = 1.0` rests on, and the development range runs
past 50.*
```

**Replaced with:**

```
provinces at `base_tax` 2 and 6, are what `TAX_COEFF = 1.0` rests on, and `base_tax` at 1444 runs up
to 33.*
```

### 91. `N01c` - §2.2

Reflow so the world-wealth figure is not split by a wrap

**Removed:**

```
   `c` with per-province α, and the per-good balance `b = s − c`. World wealth is **10,607.40**
   annual ducats over **2,472** counted provinces.
```

**Replaced with:**

```
   `c` with per-province α, and the per-good balance `b = s − c`.
   World wealth is **10,607.40** annual ducats over **2,472** counted provinces.
```

### 92. `S05a` - §0

S05: the universal, in 0

**Removed:**

```
world wealth; what it cost was an input surface whose classification was wrong in every audit that
examined it.
```

**Replaced with:**

```
world wealth; what it cost was an input surface whose classification was **wrong in both independent
audits that examined it** — `../v3-owner-agnostic/validation-v3.md` W041 and
`../v5-owner-agnostic/validation-v5.md` X030 and X034 — and passed by v4.0's own repair harness,
which v5.0 then refuted.
```

### 93. `S05b` - §1.3

S05: the universal, in 1.3

**Removed:**

```
correct and was wrong in every audit that examined it.
```

**Replaced with:**

```
correct and was wrong in **both independent audits** that examined it — v4.0's own repair harness
passed it, and v5.0's audit then refuted what that harness had passed.
```

### 94. `S05c` - §3.13

S05: the universal, in 3.13

**Removed:**

```
  rule. That rule was wrong in every audit that examined it, which is why v6.0 drops it.
```

**Replaced with:**

```
  rule. That rule was wrong in both independent audits that examined it, which is why v6.0 drops
  it.
```

### 95. `S02` - §1.3

S02/S03: flavor_geo.1 is fired but carries no development grant

**Removed:**

```
1. **`on_startup` effects**, as above. `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`,
   `flavor_geo.1` and others, and `flavor_geo.1` carries `add_base_tax`, `add_base_production` *and*
   `add_devastation` — so development itself can move before the first tick.
```

**Replaced with:**

```
1. **`on_startup` effects**, as above. `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`,
   `flavor_geo.1` and others, directly from its own `events = { }` list in
   `common/on_actions/00_on_actions.txt` — a second path alongside the `on_startup_effect` chain that
   carries `flavor_boh.15`. **Development itself does not move before the first tick:** on this start
   the history parse matches the save on **2,472 of 2,472** provinces for `base_tax`,
   `base_production` and owner, and only `trade_goods` differs, on exactly the twenty provinces
   below. *(v6.0's first draft said `flavor_geo.1` carries `add_base_tax` and could move development
   pre-tick. It does not: its whole effect is legitimacy, a country modifier and a flag. Those keys
   are in `flavor_geo.3`, which `on_startup` does not fire — a mission does.)*
```

### 96. `S04` - §1.6

S04: no route leaves the Channel

**Removed:**

```
the Channel the Hansa and the Danube. **No Europe→sink route passes the Cape of Good Hope** —
```

**Replaced with:**

```
**No route leaves `english_channel` at all** — it is a sink, out-degree 0, so the Hansa and the
Danube carry power *into* it rather than out. **No Europe→sink route passes the Cape of Good Hope** —
```

### 97. `S07` - §1.1

S07: uniform wealth does not equalise the per-node sum

**Removed:**

```
equal, which uniform *wealth* gives but is not the same condition.
```

**Replaced with:**

```
equal — which uniform *per-province* wealth does **not** give, because nodes hold between 0 and 72
counted provinces, so equal provinces make unequal node sums.
```

### 98. `S09` - §1.3

S09: the divisor bound from one observation

**Removed:**

```
[12.00, 12.14]. Both monthly figures being the annual value over twelve is what lets the annual
```

**Replaced with:**

```
(11.73, 12.14]. Both monthly figures being the annual value over twelve is what lets the annual
```

### 99. `N17` - §3.5

N17: the non-executable blocks, itemised

**Removed:**

```
seven sit inside quoted `effect_tooltip = "…"` strings and three inside `tooltip = { }` display
wrappers, so **151 are executable**.
```

**Replaced with:**

```
**four** sit inside `effect_tooltip = "…"` strings, **three** inside the `effect = "…"` string of a
`country_event_with_effect_insight`, and **three** inside `tooltip = { }` display wrappers, so
**151 are executable**.
```

### 100. `N18` - §3.9

N18: the node-wealth ranks

**Removed:**

```
`genua`, `gulf_of_siam` and `sevilla` rank 3rd, 2nd and 7th by node wealth on the corrected field
```

**Replaced with:**

```
`genua`, `gulf_of_siam` and `sevilla` rank 4th, 3rd and 7th by node wealth on the corrected field
(`mexico` is 2nd)
```

### 101. `N20` - §3.16

N20: 1e-5 was the residual, not a tolerance

**Removed:**

```
   the identity failed at the tolerance v1 used and would have been diagnosed as a solver bug.
```

**Replaced with:**

```
   the identity's residual reached 1e-5 against v1's ε of 1e-6, and would have been diagnosed as a
   solver bug.
```

### 102. `S13` - §1.1

S13: the containment set is grounded on T3

**Removed:**

```
the **node index decides** — that is why §2.8 asserts containment over a set that includes the
fallbacks.
```

**Replaced with:**

```
the **node index decides**. §2.8 asserts containment over a set that includes the fallbacks, and the
reason is **T3** (§3.2) — a fallback promotion that is a sink in neither the selected nor the promoted
set — not the wealth tie, which is incidental to it.
```

### 103. `S06` - §3.10

S06: the identity is not broken; the scalar's provenance is the cost

**Removed:**

```
**This is also why propagation is kept on a single graph.** Reading the one installed graph leaves the propagated term good-independent, so the identity survives it untouched — worst relative disagreement 0 to 3.7e-16 — one to three units in the last place, not the single
ULP v5.0 claimed. Per-good propagation destroys the *exactness*, because §1.9 reads a node's downstream neighbours and those differ per good: `gulf_of_siam`'s 29 goods leave it by **seven** distinct downstream sets. Once they differ, a country's power at the node is no longer one number and `powershare_C` no longer factors out, so a single node scalar cannot reproduce every collector's income exactly. **That is the whole of the claim, and it is a claim about exactness, not about magnitude.** How large the error is depends on which scalar you substitute for the per-good share, and that choice is not fixed by the design: substituting the share at one arbitrarily chosen reference commodity gives per-collector errors up to **+7.4%** at `sevilla`, and sweeping which commodity is chosen moves that same collector's error across a **17.8-point** range — so those figures measure the arbitrary choice, not the design. Substituting the quantity an implementation would actually store — the **value-weighted mean share** across the node's goods — the error is **at most 0.1%** at every node measured (`sevilla`, `champagne`, `genua`, `malacca`, `gulf_of_siam`). The honest statement is therefore: per-good propagation costs the exact identity and buys a per-node error that a reasonable scalar keeps within a tenth of a percent, and the identity is what Goal 7 is stated in terms of. *(v1 through v4.0 quoted "off by 5.96 ducats on a node paying ~250"; no node in the model has local trade value near 250. v4.0's replacement, 0.41%, and v5.0's "redistributive and single-digit percent" were both artifacts of freezing the share at one commodity — v5.0 having correctly diagnosed exactly that defect in v4.0. The construction behind any such figure — which countries collect, which transfer, and which commodity's share is frozen — has to be stated with it, and none of those documents stated it.)*
```

**Replaced with:**

```
**This is also why propagation is kept on a single graph — and the reason is not the one v1 through v6.0's own first draft gave.** Reading the one installed graph leaves the propagated term good-independent, so the identity holds by construction, and in doubles to within one to three units in the last place. Per-good propagation makes a country's power at the node differ by good, because §1.9 reads a node's downstream neighbours and those differ per good: `gulf_of_siam`'s 29 goods leave it by **seven** distinct downstream sets. **What that does *not* do is break the identity.** Define `ps̄_C = Σ_g v_g·cs_g·ps_C(g) / Σ_g v_g·cs_g` — the per-good shares weighted by *collected* value — and `collect_pool · ps̄_C = income_C` follows algebraically, with `Σ_C ps̄_C = 1`, so `ps̄_C` is a legal share vector and one scalar per node still reproduces every collector's income exactly. Both inputs already exist per good at write time; §2.6 sums exactly them into `collect_pool`.

**The real cost is that `ps̄_C` is not derivable from trade power alone.** It is value-weighted, so installing it means writing a country a fictitious per-node trade power whose ratio happens to equal it — and every other consumer of that power field then reads the fiction. That is a claim about what the engine exposes, not about a magnitude, and it is why the single graph stays: on one graph the scalar *is* the country's power share, needing no invention. *(The magnitudes previous versions quoted were all artifacts of substituting some other weighting. v1 through v4.0: "off by 5.96 ducats on a node paying ~250", where no node in the model has local trade value near 250. v4.0: 0.41%. v5.0: "redistributive and single-digit percent". v6.0's first draft: "at most 0.1%". Each froze or reweighted the share differently — gross-value weighting alone ranges from 0.00% to 4.6% across collector sets on this field, and up to 49% in general — so each measured its own construction. No figure is quoted here, because the identity holds and the objection is structural.)*
```

### 104. `N15` - §2.2

N15/N16: solve cost as an order of magnitude only

**Removed:**

```
**of order 0.1 s for all 29 goods, and single-digit milliseconds per good on average.** Repeated
runs on one machine span roughly 0.09–0.27 s for the full set and 3–7 ms per good as an average,
with individual goods reaching about 20 ms — so a two-significant-figure range is a statement about
a machine and a scheduler rather than about the algorithm, and none is quoted. *(v5.0 quoted
"0.17–0.21 s"; twelve fresh runs put only one inside that interval.)*
```

**Replaced with:**

```
**of order 0.1 s for all 29 goods, and single-digit milliseconds per good on average.** That is the
whole of the claim. Repeated 12-run experiments on one machine do not reproduce each other closely
enough to support anything finer — three replicates gave per-good averages spanning 3.5–10.5,
3.5–10.8 and 3.1–4.7 ms — so no range is quoted, because the quantity being measured is a machine
and a scheduler rather than the algorithm. *(v5.0 quoted "0.17–0.21 s for all 29 goods"; across
three replicates of twelve runs, the number of runs landing inside that interval was 1, then 0, then
0.)*
```

### 105. `S10` - §1.3

S10: the devastation scaling is an assumption

**Removed:**

```
| `devastation` | `trade_goods_size_modifier = -2`, scaled by the devastation level | `goods_produced` |
```

**Replaced with:**

```
| `devastation` | `trade_goods_size_modifier = -2`, scaled by the devastation level | `goods_produced` |
| | *No shipped file states that the scaling is linear in the level; the model assumes `-2 × level/100`, which is an assumption and not a file value. `prosperity` is likewise applied as stated without a file confirming its direction.* | |
```

### 106. `S11` - §1.10

S11: the cooldown covers seven of nine policies

**Removed:**

```
shipped defines rate-limit the mechanics that carry these thresholds —
`TRADING_POLICY_COOLDOWN_MONTHS = 12` (both banded policies), and
```

**Replaced with:**

```
shipped defines rate-limit the mechanics that carry these thresholds —
`TRADING_POLICY_COOLDOWN_MONTHS = 12`, which applies to **seven of the nine** trading policies
including Propagate Religion (`maximize_profit` and `maximize_profit_upgraded` carry
`cooldown = no` in `common/trading_policies/00_trading_policies.txt`), and
```

### 107. `S12` - §1.3

S12: v3.0 carries neither claim

**Removed:**

```
give 5.88 and 1.92. *(v3.0 through v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both
of its own data points.)*
```

**Replaced with:**

```
give 5.88 and 1.92. *(v4.0 and v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both of
its own data points; v3.0 carries neither that schema nor the 0.6125 arithmetic below.)*
```

### 108. `S14` - §1.6

S14: state what the Europe table shows

**Removed:**

```
These are properties of this snapshot, not constants of the model: they are what one field yielded
under one scaling, and a different world state moves them.
```

**Replaced with:**

```
Read the table as a direction rather than a trajectory: the Channel holds an end throughout, Asia
loses its own between ×1.02 and ×1.56, and by ×2.00 the map has a single Mediterranean end at
`genua` — so growth concentrates the map on Europe without the Channel monotonically absorbing it.
These are properties of this snapshot, not constants of the model: they are what one field yielded
under one scaling, and a different world state moves them.
```

### 109. `N19` - §1.6

N19: the scale test's sink set at 1e-6

**Removed:**

```
×1 and above, 12 edge flips at ×10⁻², and 100 at ×10⁻⁶ — the orientation degrades while the sink
```

**Replaced with:**

```
×1 and above, 12 edge flips at ×10⁻², and 100 at ×10⁻⁶, where the sink set also collapses to
`{genua}` — the orientation degrades and the sink
```

### 110. `F1-route` - §1.6

The sentence my S04 edit truncated

**Removed:**

```
ganges_delta → burma → gulf_of_siam → canton → hangzhou`. From the north it is the Volga, and from
**No route leaves `english_channel` at all** — it is a sink, out-degree 0, so the Hansa and the
Danube carry power *into* it rather than out.
```

**Replaced with:**

```
ganges_delta → burma → gulf_of_siam → canton → hangzhou`. From the north it is the Volga:
`north_sea → white_sea → novgorod → kazan → astrakhan → persia → …`. **No route leaves
`english_channel` at all** — it is a sink, out-degree 0, so the Hansa and the Danube carry power
*into* it rather than out, and v5.0's "from the Channel it is the Hansa and the Danube" was
describing a path that does not exist.
```

### 111. `F2-conn` - §1.6

1.6's copy of the connectivity figure

**Removed:**

```
**90.2%** of ordered node pairs (5,703 of 6,320) connected by at least one good's directed path.
```

**Replaced with:**

```
**89.6%** of ordered node pairs (5,663 of 6,320) connected by at least one good's directed path.
```

### 112. `F3-coal` - §2.8

2.8's copy of the coal figure

**Removed:**

```
Measured: repricing the 45 owned latent-coal provinces flips 13 of 159 `Φ_w` edges (§1.5) |
```

**Replaced with:**

```
Measured: repricing the 45 owned latent-coal provinces flips 10 of 159 `Φ_w` edges (§1.5) |
```

### 113. `F4-c` - §1.6

The dangling reference to an item (c)

**Removed:**

```
under one scaling, and a different world state moves them. Under (c) **scaling development and
scaling wealth are the same operation** — maximum difference 0.0 across the European set — so the
distinction that made v5.0's version of this table wrong does not arise.
```

**Replaced with:**

```
under one scaling, and a different world state moves them. Because §1.3's wealth is linear in
development, **scaling development and scaling wealth are the same operation here** — maximum
difference 0.0 across the European set — so the distinction that made v5.0's version of this table
wrong does not arise.
```

### 114. `F5-pol` - §1.10

Nine file entries vs five distinct policies

**Removed:**

```
`TRADING_POLICY_COOLDOWN_MONTHS = 12`, which applies to **seven of the nine** trading policies
```

**Replaced with:**

```
`TRADING_POLICY_COOLDOWN_MONTHS = 12`, which applies to **seven of the nine entries** in
`common/trading_policies/00_trading_policies.txt` — five distinct policies, four of them with an
`_upgraded` twin, plus Propagate Religion which has none — so seven of nine entries, or four of the
five families, are rate-limited
```

### 115. `Y033` - §1.3

Y033/S08: the tax tooltip schema, finally applied

**Removed:**

```
`Base: trunc(base_tax / 12) (Yearly base_tax)` — observed `Base: 0.49 (Yearly 6.00)` at `base_tax` 6
```

**Replaced with:**

```
`Base: trunc(base_tax × 0.0833333) (Yearly base_tax)` — observed `Base: 0.49 (Yearly 6.00)` at `base_tax` 6
```

### 116. `Y040` - §1.3

Y040/S12: the attribution span, and the self-contradiction

**Removed:**

```
finer. *(v3.0 through v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires
```

**Replaced with:**

```
finer. *(v4.0 and v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires
```

### 117. `Y062` - §1.3

Y062: max base_tax is 15, not 33

**Removed:**

```
provinces at `base_tax` 2 and 6, are what `TAX_COEFF = 1.0` rests on, and `base_tax` at 1444 runs up
to 33.*
```

**Replaced with:**

```
provinces at `base_tax` 2 and 6, are what `TAX_COEFF = 1.0` rests on, and `base_tax` at 1444 runs up
to 15 (province 1821), with total development reaching 33 there.*
```

### 118. `Y132` - §2.8

Y132: the razed-China flip count

**Removed:**

```
to `{doab, english_channel, gulf_of_siam}`, 23 of 159 edges flipping.
```

**Replaced with:**

```
to `{doab, english_channel, gulf_of_siam}`, 22 of 159 edges flipping.
```

### 119. `Y003a` - §0

Y003: state the denominator, 0 header

**Removed:**

```
the whole-install sweep that maintained them. On the 1444 start that apparatus was worth 0.98% of
world wealth;
```

**Replaced with:**

```
the whole-install sweep that maintained them. On the 1444 start that apparatus was worth 105.30
ducats — 0.98% of the 10,712.70 that field totalled with it, 0.99% of the 10,607.40 without;
```

### 120. `Y003b` - §1.3

Y003: state the denominator, 1.3

**Removed:**

```
depended on. On the 1444 start that whole apparatus was worth **0.98%** of world wealth over **89** of the 2,472
```

**Replaced with:**

```
depended on. On the 1444 start that whole apparatus was worth **105.30 ducats** — 0.98% of the
10,712.70 that field totalled with it, 0.99% of the 10,607.40 without — over **89** of the 2,472
```

### 121. `Y003c` - §3.13

Y003: state the denominator, 3.13

**Removed:**

```
  first is whether the fidelity is worth it — on the 1444 start the whole set was worth 0.98% of
  world wealth.
```

**Replaced with:**

```
  first is whether the fidelity is worth it — on the 1444 start the whole set was worth 105.30
  ducats, about one percent of world wealth either way the ratio is taken.
```

### 122. `Y008` - §3.15

Y008/R3: 3.15 still maintained the Laplacian's contrast figures

**Removed:**

```
`max(s)` over v1's ε floor. With the floor removed the contrasts run **4–97 on supply against
211–15,010 on demand** over the 28 goods produced in more than one node, so the demand side is the
wider one; `cloves` has a single producer and no contrast to measure, which is the sparsity point in
miniature.)*
```

**Replaced with:**

```
`max(s)` over v1's ε floor. With the floor removed the demand side is the wider of the two, not the
supply side — §3.2 carries the measurement, and this entry does not maintain a copy of it. `cloves`
has a single producer and so no contrast to measure at all, which is the sparsity point in
miniature.)*
```

### 123. `Y170` - §3.15

Y170/R3: RANK's stranded-demand figure

**Removed:**

```
every route, so a sixth of world demand is stranded, it leaves orphan sinks a good cannot reach
```

**Replaced with:**

```
every route, so a large share of world demand is stranded, it leaves orphan sinks a good cannot reach
```

### 124. `Y161` - §3.10

Y161: figures quoted two clauses before 'no figure is quoted'

**Removed:**

```
v6.0's first draft: "at most 0.1%". Each froze or reweighted the share differently — gross-value weighting alone ranges from 0.00% to 4.6% across collector sets on this field, and up to 49% in general — so each measured its own construction. No figure is quoted here, because the identity holds and the objection is structural.)*
```

**Replaced with:**

```
v6.0's first draft: "at most 0.1%". Each froze or reweighted the share differently, so each measured its own construction rather than a property of the design — and the size of the discrepancy depends on which collectors are taken to be collecting, which is a choice of the construction too. **No figure of my own is quoted here**, because the identity holds and the objection is structural.)*
```

### 125. `Y124a` - §1.6

Y124: the sink set is qualified where it is stated

**Removed:**

```
Measured on 1444 data at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and
`hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12.
```

**Replaced with:**

```
Measured on 1444 data at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and
`hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12. **One of those two is a property of
the world and the other is a property of the node ordering, and the difference matters more than the
count.** Phase 2's b-flow is degenerate (§2.4 item 1), so relabelling the nodes and re-running
returns a different optimal orientation: across 100 relabellings with α_Φ and every input held
fixed, the orientation changed 100 times, a mean of 26 of 159 edges moved, and the sink set came back
exactly as `{english_channel, hangzhou}` **8 times**. But `hangzhou` was an end in **100 of 100**,
and `english_channel` in **40**. The Asian end is the robust one; the European end is one of several
the same world admits — `gulf_of_siam` held an end in 55 runs, `wien` in 37, `sevilla` in 19. The
count itself ranged 1 to 5, most often 2.

**So read the rest of this section as conditional on one canonical node order**, which §2.4 item 1
requires the emitter to fix. That is not a caveat about precision; it is a statement about what kind
of fact the European end is.
```

### 126. `Y124b` - §1.6

Y124: the Europe table carries the same condition

**Removed:**

```
Read the table as a direction rather than a trajectory: the Channel holds an end throughout, Asia
loses its own between ×1.02 and ×1.56, and by ×2.00 the map has a single Mediterranean end at
`genua` — so growth concentrates the map on Europe without the Channel monotonically absorbing it.
```

**Replaced with:**

```
Read the table as a direction rather than a trajectory, and on one node ordering: growth moves the
ends westward and thins Asia's, and by ×2.00 a single Mediterranean end at `genua` holds the map.
*Which* European node holds an end at a given factor is ordering-dependent in the same way the 1444
set is — `english_channel` at ×1.02, `rheinland` at ×1.56 and `genua` at ×2.00 are this ordering's
answers, not the world's — so the direction is the claim and the membership is not.
```

### 127. `Y124c` - §2.4

Y124: the end-flag list is conditional

**Removed:**

```
2. **End flags** — `end=yes` on every `Φ_w` sink (1444: **two** end nodes, `english_channel` and
   `hangzhou`, against
```

**Replaced with:**

```
2. **End flags** — `end=yes` on every `Φ_w` sink. **This list is a function of the canonical node
   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end under
   every ordering tried, `english_channel` under about 40% of them, and the count ranges 1 to 5
   (§1.6). Fix the order, emit, and keep it — changing it changes the flags without anything in the
   world changing. (1444, shipped order: **two** end nodes, `english_channel` and
   `hangzhou`, against
```

### 128. `Y124d` - §2.8

Y124: 2.8's razed-China row survives, and why

**Removed:**

```
| Razed China | Zeroing `hangzhou`-node development relocates an end in one solve
```

**Replaced with:**

```
| Razed China | *This row is ordering-robust where §1.6's sink membership is not: it turns on `hangzhou` holding an end, which it does under every relabelling tried (§1.6).* Zeroing `hangzhou`-node development relocates an end in one solve
```

### 129. `Y003d` - §1.3

Y003: quote the ratio against the field the spec calls world wealth

**Removed:**

```
depended on. On the 1444 start that whole apparatus was worth **105.30 ducats** — 0.98% of the
10,712.70 that field totalled with it, 0.99% of the 10,607.40 without — over **89** of the 2,472
```

**Replaced with:**

```
depended on. On the 1444 start that whole apparatus was worth **105.30 ducats**, **0.99%** of the
10,607.40 world wealth the model computes without it (0.98% of the 10,712.70 the field totalled with
it), over **89** of the 2,472
```

### 130. `Y011` - §0

Y011: the harness claim, stated to its measured coverage

**Removed:**

```
`scripts/verify6.py` re-derives each one **from the document text** and fails if the two disagree.
```

**Replaced with:**

```
`scripts/verify6.py` reads figures **out of the document text** and fails when they disagree with a
value computed from the install — but it does **not** cover every figure the document prints.
Measured by `scripts/coverage6.py`, which corrupts each spec-printed figure whether the harness looks
at it or not: **5 of 11 uniquely-locatable figures are protected**, with 23 more unscorable because
their value occurs many times in the document and a single-site mutation cannot be aimed at them. So
roughly half of what is locatable is guarded, and the rest rests on the script attribution alone.
*`scripts/mutate6.py` reports a higher score and should not be read as coverage: it plants errors
only in figures `verify6.py` already checks, so it cannot fail. That is the same circularity v4.0's
harness had, and it is recorded here rather than quietly fixed.*
```

### 131. `Y011b` - §0

Y011: coverage as a direction with its tool, not a fraction that goes stale

**Removed:**

```
Measured by `scripts/coverage6.py`, which corrupts each spec-printed figure whether the harness looks
at it or not: **5 of 11 uniquely-locatable figures are protected**, with 23 more unscorable because
their value occurs many times in the document and a single-site mutation cannot be aimed at them. So
roughly half of what is locatable is guarded, and the rest rests on the script attribution alone.
```

**Replaced with:**

```
**Under half** of the figures it prints are guarded, and the rest rest on their script attribution
alone. `scripts/coverage6.py` measures that honestly — it corrupts each spec-printed figure whether
the harness looks at it or not — and it should be re-run rather than quoted here, because the number
moves with every edit to the document.
```

### 132. `R09` - §1.6

The ordering result, stated across seeds not one

**Removed:**

```
returns a different optimal orientation: across 100 relabellings with α_Φ and every input held
fixed, the orientation changed 100 times, a mean of 26 of 159 edges moved, and the sink set came back
exactly as `{english_channel, hangzhou}` **8 times**. But `hangzhou` was an end in **100 of 100**,
and `english_channel` in **40**. The Asian end is the robust one; the European end is one of several
the same world admits — `gulf_of_siam` held an end in 55 runs, `wien` in 37, `sevilla` in 19. The
count itself ranged 1 to 5, most often 2.

**So read the rest of this section as conditional on one canonical node order**, which §2.4 item 1
requires the emitter to fix. That is not a caveat about precision; it is a statement about what kind
of fact the European end is.
```

**Replaced with:**

```
returns a different optimal orientation. Across 400 relabellings — four seeds of 100, with `α_Φ` and
every input held fixed — **the orientation changed every time**, a mean of about 25 of 159 edges
moved, and the sink set came back exactly as `{english_channel, hangzhou}` in **5 to 10 runs per
hundred**. `hangzhou` was an end in **97 to 100 per hundred** and `english_channel` in **37 to 44**.
The Asian end is the robust one — not invariant, since orderings exist where it loses its end, but
near enough that it is a fact about that node. The European end is one of several the same world
admits: `gulf_of_siam` held an end in about half the runs, `wien` in a third, `sevilla` in a fifth.
The count itself ranged 1 to 5, most often 2 or 3.

**What is conditional on the node order, and what is not.** Conditional: the sink set's membership
and size, and everything derived from them — §2.4's end-flag list, and which European node holds an
end in the table below. Not conditional, over the same relabellings: the map is fully oriented
(159/159) and acyclic every time, no fallback ever fires, and the LP objective is identical to
2.22e-16, so these are different *optimal* orientations rather than different answers. §2.4 item 1
requires the emitter to fix one canonical order for exactly this reason.
```

### 133. `R09b` - §2.4

2.4's derived universal

**Removed:**

```
   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end under
   every ordering tried, `english_channel` under about 40% of them, and the count ranges 1 to 5
   (§1.6).
```

**Replaced with:**

```
   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end in
   97–100 orderings per hundred, `english_channel` in 37–44, and the count ranges 1 to 5 (§1.6).
```

### 134. `R09c` - §1.6

The Europe table's ordering note, which named an invariant row

**Removed:**

```
*Which* European node holds an end at a given factor is ordering-dependent in the same way the 1444
set is — `english_channel` at ×1.02, `rheinland` at ×1.56 and `genua` at ×2.00 are this ordering's
answers, not the world's — so the direction is the claim and the membership is not.
```

**Replaced with:**

```
*Which* European node holds an end at the smaller factors is ordering-dependent in the same way the
1444 set is, so the direction is the claim and the membership is not. The last row is the exception
and is worth separating: at ×2.00 `genua` held an end in **60 of 60** relabellings, so a single
Mediterranean end under that much European growth is a property of the field rather than of the
ordering.
```

### 135. `T05` - §0

The harness claim overstated what attribution covers

**Removed:**

```
**Under half** of the figures it prints are guarded, and the rest rest on their script attribution
alone.
```

**Replaced with:**

```
**Under half** of the figures it prints are guarded. The remainder are not all covered by anything
else either: a script is named about a dozen times against roughly three times that many unguarded
figures, and some of the most recent additions carry neither a guard nor an attribution.
```

### 136. `Y140` - §2.8

Y140: the last 'every relabelling', in 2.8

**Removed:**

```
| Razed China | *This row is ordering-robust where §1.6's sink membership is not: it turns on `hangzhou` holding an end, which it does under every relabelling tried (§1.6).*
```

**Replaced with:**

```
| Razed China | *This row is ordering-robust where §1.6's sink membership is not: it turns on `hangzhou` holding an end, which it does in 97–100 relabellings per hundred (§1.6) — and on the razed field itself `hangzhou` loses its end in every relabelling tried, which is what the row asserts.*
```

### 137. `Y033b` - §3.13

The Cape's land-province count

**Removed:**

```
**Per province, because node boundaries are an authoring artifact.** Node sizes run from 19 land
provinces (`cape_of_good_hope`) to 77 (`girin`) — a 4× spread
```

**Replaced with:**

```
**Per province, because node boundaries are an authoring artifact.** Node sizes run from 20 land
provinces (`cape_of_good_hope`) to 77 (`girin`) — a 4× spread
```

### 138. `attrib` - §2.4

The relabelling experiment now names a script that contains it

**Removed:**

```
   (the field from `measure6.py`; the relabelling sweep is recorded in
   `../v5-owner-agnostic/validation-v5.md`).
```

**Replaced with:**

```
   (`relabel6.py`, which validates its instrument against `drain.py` on the identity permutation
   before running a trial and aborts if that fails).
```

### 139. `Y-attrib2` - §2.4

2.4 quotes figures a shipped script produces, not retired ones

**Removed:**

```
   1444, relabelling the nodes and running end-to-end changed the orientation on **580 of 580**
   runs (29 goods × 20 relabellings), **always** by returning a different optimal vertex and **never**
   by a sweep tiebreak, with a mean of **22.1 of 159 edges** moving and the objective identical to
   8.9e-16. Independently, permuting only the arc presentation order with node labels held fixed
   changes the optimal support on **10 of 10 goods** tested, with objective gaps ≤ 1.8e-15
   (`relabel6.py`, which validates its instrument against `drain.py` on the identity permutation
   before running a trial and aborts if that fails). Twenty-two
   flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event.
```

**Replaced with:**

```
   1444, relabelling the nodes and running the aggregate graph end-to-end changed the orientation in
   **400 of 400** runs across four independent seeds, **always** by returning a different optimal
   vertex and **never** by a sweep tiebreak, with a mean of **25 of 159 edges** moving and the LP
   objective identical to within 4.4e-16 (`relabel6.py`, which validates its instrument against
   `drain.py` on the identity permutation and aborts if that fails). Twenty-five flips is the same
   magnitude as the razed-China perturbation §2.8 treats as a major world event. *(Earlier versions
   quoted a 580-of-580 per-good sweep and an arc-permutation result whose scripts were never shipped;
   both are withdrawn in favour of the figure a script in this tree reproduces.)*
```

### 140. `Y-attrib3` - §2.4

The trailing reference to the retired figure

**Removed:**

```
re-order the same world and the map moves, with `α_Φ` and every input held fixed. The specific 580/580 result is
   HiGHS-specific in its detail but not in kind
```

**Replaced with:**

```
re-order the same world and the map moves, with `α_Φ` and every input held fixed. The specific counts
   are HiGHS-specific in their detail but not in kind
```

### 141. `Y078-081` - §1.6

Y078/Y079/Y081/Y083/Y128: pooled proportions, not seed ranges

**Removed:**

```
returns a different optimal orientation. Across 400 relabellings — four seeds of 100, with `α_Φ` and
every input held fixed — **the orientation changed every time**, a mean of about 25 of 159 edges
moved, and the sink set came back exactly as `{english_channel, hangzhou}` in **5 to 10 runs per
hundred**. `hangzhou` was an end in **97 to 100 per hundred** and `english_channel` in **37 to 44**.
The Asian end is the robust one — not invariant, since orderings exist where it loses its end, but
near enough that it is a fact about that node. The European end is one of several the same world
admits: `gulf_of_siam` held an end in about half the runs, `wien` in a third, `sevilla` in a fifth.
The count itself ranged 1 to 5, most often 2 or 3.
```

**Replaced with:**

```
returns a different optimal orientation. Over **800 relabellings** — eight seeds of 100, with `α_Φ`
and every input held fixed (`relabel6.py`) — **the orientation changed every time**, a mean of 25 of
159 edges moved, and the sink set came back exactly as `{english_channel, hangzhou}` in **64 of 800**
runs. `hangzhou` was an end in **786 of 800** and `english_channel` in **322**. The Asian end is the
robust one — not invariant, since orderings exist where it loses its end, but near enough that it is a
fact about that node. The European end is one of several the same world admits: `gulf_of_siam` held an
end in 459 runs, `wien` in 259, `rheinland` in 122, `sevilla` in 112. The count itself ranged 1 to 5,
most often 2 or 3.

*Proportions are pooled over all 800 draws rather than given as a per-seed range, because the range
is itself a function of which seeds are drawn: two honest eight-hundred-trial runs reported 97–100
and 96–100 per hundred for the same quantity.*
```

### 142. `Y079b` - §2.4

2.4's copy of the same proportions

**Removed:**

```
   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end in
   97–100 orderings per hundred, `english_channel` in 37–44, and the count ranges 1 to 5 (§1.6).
```

**Replaced with:**

```
   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end in 786
   of 800 relabellings, `english_channel` in 322, and the count ranges 1 to 5 (§1.6).
```

### 143. `Y140b` - §2.8

2.8's copy of the same proportion

**Removed:**

```
which it does in 97–100 relabellings per hundred (§1.6)
```

**Replaced with:**

```
which it does in 786 of 800 relabellings (§1.6)
```

### 144. `Y083` - §2.4

Y083: the objective deviation

**Removed:**

```
objective identical to within 4.4e-16 (`relabel6.py`, which validates its instrument against
```

**Replaced with:**

```
objective identical to within 4.44e-16 (`relabel6.py`, which validates its instrument against
```

### 145. `Y010-158` - §3.9

Y010/Y158: 'a majority' is exactly half

**Removed:**

```
  artifacts of sweep scheduling rather than places, a majority of them terminate no good at all,
```

**Replaced with:**

```
  artifacts of sweep scheduling rather than places, **half** of them terminate no good at all (7 of
  14 on the 1444 field),
```

### 146. `Y005` - §0

Y005: name the ID that actually refuted the classifier

**Removed:**

```
audits that examined it** — `../v3-owner-agnostic/validation-v3.md` W041 and
`../v5-owner-agnostic/validation-v5.md` X030 and X034 — and passed by v4.0's own repair harness,
which v5.0 then refuted.
```

**Replaced with:**

```
audits that examined it** — `../v3-owner-agnostic/validation-v3.md` W041 and
`../v5-owner-agnostic/validation-v5.md` X035 — and passed by v4.0's own repair harness, which v5.0
then refuted.
```

### 147. `Y027-125` - §0

Y027/Y125: whose rule and whose sweep

**Removed:**

```
modifier classifier and everything it governed — the trade-good modifiers, great projects, permanent
province modifiers, buildings, centres of trade and the DLC conditionality — are deleted, along with
the whole-install sweep that maintained them.
```

**Replaced with:**

```
modifier classifier and everything it governed — the trade-good modifiers, great projects, permanent
province modifiers, buildings, centres of trade and the DLC conditionality — are deleted, along with
the whole-install sweep that maintained them. *(The two-test classifier is v4.0's; v3.0 used a
structural rule about which block of a trade-good definition a modifier sits in. The whole-install
sweep is v5.0's alone.)*
```

### 148. `Y168` - §3.10

Y168: the 5.96 figure's span

**Removed:**

```
v1 through v4.0: "off by 5.96 ducats on a node paying ~250", where no node in the model has local trade value near 250.
```

**Replaced with:**

```
v1 through v3.0: "off by 5.96 ducats on a node paying ~250", where no node in the model has local trade value near 250 — v4.0 deleted it and its own harness asserted the deletion.
```

### 149. `Y097` - §1.6

Y097: the Channel's basin peaks and then the end migrates

**Removed:**

```
Hangzhou; as European development compounds, the Channel's basin grows and Asia's pole fades, and
```

**Replaced with:**

```
Hangzhou; as European development compounds the ends move west and Asia's pole fades — the Channel's
basin grows from 18 nodes to 28 by about ×1.44, then gives way as the end itself migrates to `genua`
past roughly ×1.70 — and
```

### 150. `Y046` - §1.3

Y046: prosperity's direction is in the file

**Removed:**

```
| | *No shipped file states that the scaling is linear in the level; the model assumes `-2 × level/100`, which is an assumption and not a file value. `prosperity` is likewise applied as stated without a file confirming its direction.* | |
```

**Replaced with:**

```
| | *The magnitudes and directions above are all read from `00_static_modifiers.txt`. What no shipped file states is the **scaling law** for `devastation`: the model assumes the modifier applies in proportion to the level, `-2 × level/100`, and that proportionality is an assumption rather than a file value.* | |
```

### 151. `Y146-147` - §3.2

Y146/Y147: these are wealth multiples, and girin needs less

**Removed:**

```
of placement. Moving the spice sink to a Chinese node takes a multiple of that node's demand in the
region of **3.6–4.9×** — observed on the 1444 field (`beijing` 3.61×, `hangzhou` 4.12×, `xian`
4.60×, `canton` 4.77×). The multiple a node needs and the share of world demand it then buys do not
line up end to end, because the share depends on where the node started; other nodes in the region
need more still.
```

**Replaced with:**

```
of placement. Moving the spice sink to a Chinese node takes a multiple of that node's **wealth** in
the region of **3.6–4.8×** — observed on the 1444 field (`beijing` 3.63×, `hangzhou` 4.13×, `xian`
4.61×, `canton` 4.78×). *These are wealth multiples, not demand multiples: because demand is
`wealth^α` normalised over the world, the same move expressed in demand is a much larger factor.* And
the four named are not the cheapest — `girin` needs 3.89× and `yumen` 4.49×, both inside the range, so
the claim is about the size of the intervention rather than about which node is easiest to move.
```

### 152. `Y155` - §3.5

Y155: what the guard actually is, and the bare except that remains

**Removed:**

```
the scan was "guarded by a per-file count assertion" — there was no assertion anywhere in its
toolchain. `verify6.py` now carries the guard, and the reason a plain parse misses these is
```

**Replaced with:**

```
the scan was "guarded by a per-file count assertion" — there was no assertion anywhere in its
toolchain. `verify6.py` now checks the census, though only by requiring the printed total to match a
computed one rather than by reconciling per file, and `measure6.py`'s walker still swallows parse
failures in a bare `except`. The reason a plain parse misses these is
```

### 153. `Q09` - §3.13

Q09: revert to 19 land provinces, and say why it is not 20

**Removed:**

```
**Per province, because node boundaries are an authoring artifact.** Node sizes run from 20 land
provinces (`cape_of_good_hope`) to 77 (`girin`) — a 4× spread
```

**Replaced with:**

```
**Per province, because node boundaries are an authoring artifact.** Node sizes run from 19 land
provinces (`cape_of_good_hope` — its `members` list has 20 entries, but 1460 is a sea zone, listed in
`map/default.map`'s `sea_starts`) to 77 (`girin`) — a 4× spread
```

### 154. `Q10` - §1.6

Q10: the genua takeover point, on a fine grid

**Removed:**

```
basin grows from 18 nodes to 28 by about ×1.44, then gives way as the end itself migrates to `genua`
past roughly ×1.70 — and
```

**Replaced with:**

```
basin grows from 18 nodes to 28 by about ×1.44, then gives way as the end itself migrates: `genua`
first holds an end at ×1.63 and is the sole end from ×1.64 through ×2.00 — and
```

### 155. `Q07` - §1.6

Q07: 1.6's copy of the objective deviation

**Removed:**

```
and the LP objective is identical to
2.22e-16, so these are different *optimal* orientations rather than different answers.
```

**Replaced with:**

```
and the LP objective is identical to within
4.44e-16, so these are different *optimal* orientations rather than different answers.
```

### 156. `Q03-06` - §1.6

Q03-Q06: the minor holders are not stable at n=800

**Removed:**

```
runs. `hangzhou` was an end in **786 of 800** and `english_channel` in **322**. The Asian end is the
robust one — not invariant, since orderings exist where it loses its end, but near enough that it is a
fact about that node. The European end is one of several the same world admits: `gulf_of_siam` held an
end in 459 runs, `wien` in 259, `rheinland` in 122, `sevilla` in 112. The count itself ranged 1 to 5,
most often 2 or 3.

*Proportions are pooled over all 800 draws rather than given as a per-seed range, because the range
is itself a function of which seeds are drawn: two honest eight-hundred-trial runs reported 97–100
and 96–100 per hundred for the same quantity.*
```

**Replaced with:**

```
runs. **`hangzhou` was an end in about 98% of them and `english_channel` in about 40%.** The Asian
end is the robust one — not invariant, since orderings exist where it loses its end, but near enough
that it is a fact about that node. The European end is one of several the same world admits, and after
`english_channel` the most frequent are `gulf_of_siam` (a little over half the runs), `wien` (about a
third), then `rheinland` and `sevilla`. The count itself ranged 1 to 5, most often 2 or 3.

*The two leading proportions are quoted to two figures and the trailing ones qualitatively, because
that is as far as this sample supports: across three independent 800-trial sets `hangzhou` came in at
784–789 and `english_channel` at 322–336, while `sevilla` ranged 79–117 and `rheinland` 112–136. A
per-seed range is worse still, being a function of which seeds are drawn.*
```

### 157. `Q03b` - §2.4

2.4's copy, to the same precision

**Removed:**

```
   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end in 786
   of 800 relabellings, `english_channel` in 322, and the count ranges 1 to 5 (§1.6).
```

**Replaced with:**

```
   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end in about
   98% of relabellings, `english_channel` in about 40%, and the count ranges 1 to 5 (§1.6).
```

### 158. `Q03c` - §2.8

2.8's copy, to the same precision

**Removed:**

```
which it does in 786 of 800 relabellings (§1.6)
```

**Replaced with:**

```
which it does in about 98% of relabellings (§1.6)
```

### 159. `Y047` - §1.3

Y047: unrest is a fifth province-state modifier

**Removed:**

```
| `occupied` | `trade_goods_size_modifier = -0.5` **and** `local_tax_modifier = -0.5` | both |
```

**Replaced with:**

```
| `occupied` | `trade_goods_size_modifier = -0.5` **and** `local_tax_modifier = -0.5` | both |
| `unrest` | `local_tax_modifier = -0.02` **per point of revolt risk** | `tax_value` |
```

### 160. `Y047b` - §1.3

Y047: what unrest costs, and that its scaling is sourced

**Removed:**

```
Only `occupied` touches the tax term; the other three reach `goods_produced` alone.
```

**Replaced with:**

```
`occupied` and `unrest` touch the tax term; the other three reach `goods_produced` alone. **`unrest`
is live at the 1444 start**: 21 counted provinces carry revolt risk between 4.834 and 14.834 in the
save, costing **12.23 ducats — 0.115% of world wealth** — and admitting it moves **no edge** of the
installed graph, so it is a fidelity correction with no orientation consequence. *Its scaling is
stated in the file:* the `unrest` block's own comment reads `#10% longer time to build troops for each
rr`, so its values apply per point, and the neighbouring `nationalism` block uses the same convention.
*(Sixteen of the 21 are resolvable from `history/provinces` at integer risk 5/8/10/15; the other five,
all Shirvan-owned, receive theirs at runtime, so the model reads the save.)*
```

### 161. `Y049` - §1.3

Y049: devastation is now the only unsourced scaling law

**Removed:**

```
| | *The magnitudes and directions above are all read from `00_static_modifiers.txt`. What no shipped file states is the **scaling law** for `devastation`: the model assumes the modifier applies in proportion to the level, `-2 × level/100`, and that proportionality is an assumption rather than a file value.* | |
```

**Replaced with:**

```
| | *The magnitudes and directions above are all read from `00_static_modifiers.txt`. What no shipped file states is the **scaling law** for `devastation`: the model assumes the modifier applies in proportion to the level, `-2 × level/100`, and that proportionality is an assumption rather than a file value. It is the **only** such assumption in this table — `unrest` and `nationalism` both carry per-unit comments in that same file, so the convention for stating a scaling exists and `devastation` simply does not use it.* | |
```

### 162. `V06a` - §1.6

V06: 1.6's objective figure, with its unit and its status

**Removed:**

```
and the LP objective is identical to within
4.44e-16, so these are different *optimal* orientations rather than different answers.
```

**Replaced with:**

```
and the LP objective is identical to
within four units in the last place, so these are different *optimal* orientations rather than
different answers.
```

### 163. `V06b` - §2.4

V06: 2.4's copy, same correction

**Removed:**

```
   objective identical to within 4.44e-16 (`relabel6.py`, which validates its instrument against
```

**Replaced with:**

```
   objective identical to within four units in the last place — 4.44e-16 absolute against an objective
   of 0.712, which is the same quantity as the 6.2e-16 relative deviation and not a second measurement,
   and which grows to 6–7 ULP at larger trial counts, so it is a sample maximum rather than a bound
   (`relabel6.py`, which validates its instrument against
```

### 164. `T03` - §2.4

T03: restore the withdrawn sweep, and drop the false premise

**Removed:**

```
magnitude as the razed-China perturbation §2.8 treats as a major world event. *(Earlier versions
   quoted a 580-of-580 per-good sweep and an arc-permutation result whose scripts were never shipped;
   both are withdrawn in favour of the figure a script in this tree reproduces.)*
```

**Replaced with:**

```
magnitude as the razed-China perturbation §2.8 treats as a major world event. The same effect on the
   **per-good** graphs is 580 of 580 (29 goods × 20 relabellings), from
   `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`. *(v6.0 withdrew that sweep on the ground that
   its script had never shipped. The script is in the tree and runs; the withdrawal was the error, not
   the figure. No v1–v5 spec ever printed it either, so it was never "quoted by earlier versions" —
   it comes from this project's working files.)*
```

### 165. `T04` - §3.9

T04: the Phi_ord fraction is a property of the node order

**Removed:**

```
  artifacts of sweep scheduling rather than places, **half** of them terminate no good at all (7 of
  14 on the 1444 field),
```

**Replaced with:**

```
  artifacts of sweep scheduling rather than places — and the sharpest evidence for that is what
  relabelling does to them: across 20 relabellings the end count runs **12 to 19** and the end set is
  **never twice the same**, so neither the count nor the share terminating no good is a property of
  the world. Most of those ends terminate no good,
```

### 166. `T05` - §1.6

T05: no basin figure, for the reason that reproduces

**Removed:**

```
basin grows from 18 nodes to 28 by about ×1.44, then gives way as the end itself migrates: `genua`
first holds an end at ×1.63 and is the sole end from ×1.64 through ×2.00 — and
```

**Replaced with:**

```
basin widens, non-monotonically, and then gives way as the end itself migrates: `genua` first holds an
end at ×1.63 and is the sole end from ×1.64 through ×2.00 — and
```

### 167. `T06` - §1.6

T06: basin size joins the ordering-conditional list

**Removed:**

```
Conditional: the sink set's membership
and size, and everything derived from them — §2.4's end-flag list, and which European node holds an
end in the table below.
```

**Replaced with:**

```
Conditional: the sink set's membership
and size, and everything derived from them — §2.4's end-flag list, which European node holds an end in
the table below, and **the size of any node's drainage basin**. *No basin figure is quoted anywhere in
this section, because at the growth factors where one would be interesting `english_channel` holds an
end in only a handful of orderings, so any range is the spread of a handful of observations rather
than a measurement.*
```

### 168. `V11` - §3.5

V11/V12: the wool floor comes from history, and the campaign value is unknown

**Removed:**

```
and `gems` at 5.000 on a base of 4.0. So a −0.25 event takes a 2.5 good to 1.875, and grain and wine
reach 0.625.
```

**Replaced with:**

```
and `gems` at 5.000 on a base of 4.0. So a −0.25 key takes a 2.5 good to 1.875, and grain and wine
reach 0.625.
```

### 169. `V12` - §3.5

V12: the campaign sentence, which was quoting a single-key floor

**Removed:**

```
keyed, so 1.875 is the figure a campaign reaching 1540 holds. v2's 13 was right; v3.0 reached 12 by
```

**Replaced with:**

```
keyed. **1.875 is the single-key floor, not the campaign figure**: the same `1540.1.1` block also
applies `COTTON_IMPORTS = -0.10` to `wool`, so a campaign that runs that block holds two live negative
keys and wool sits at 1.625 if keyed changes sum or 1.6875 if they compound — **and nothing in the
install settles which**, because no readable save carries a good with two live keys. Note also that
the −0.25 is the *history* value; `events/PriceChanges.txt` carries −0.20 for the same key, which
alone would floor wool at 2.00. The partition above needs the history value: events alone give
12/3/4/11 rather than 13/2/4/11. v2's 13 was right; v3.0 reached 12 by
```

### 170. `V08` - §0

V08/T07: the printed-figure count is tokenisation-dependent, so it goes

**Removed:**

```
**Under half** of the figures it prints are guarded. The remainder are not all covered by anything
else either: a script is named about a dozen times against roughly three times that many unguarded
figures, and some of the most recent additions carry neither a guard nor an attribution.
```

**Replaced with:**

```
**`verify6.py` pins 35 distinct figures across 29 checks, and that is well short of what the document
prints.** No ratio is offered, because the denominator is not well defined — counting "the figures the
spec prints" gives anywhere from 279 to 326 depending on how a numeric token is delimited, so any
proportion built on it says more about the tokeniser than about the harness. `scripts/coverage6.py`
reports what is guarded among the figures it can locate unambiguously, and it should be re-run rather
than quoted. Some figures carry a script attribution instead of a guard, and a few carry neither.
```

### 171. `Y050a` - §1.3

Y050: 1.3's prose said four where the table has five

**Removed:**

```
**Province condition is the one thing besides development and the good that wealth reads.** Four
static modifiers describe a province's own state, and all four are read from
`common/static_modifiers/00_static_modifiers.txt`:
```

**Replaced with:**

```
**Province condition is the one thing besides development and the good that wealth reads.** Five
static modifiers describe a province's own state, and all five are read from
`common/static_modifiers/00_static_modifiers.txt`:
```

### 172. `Y050b` - §2.2

Y050: 2.2's copy of the count, and what is live at 1444

**Removed:**

```
   The only modifiers read are the four that describe the province's own condition, and at 1444 only
   `devastation` is live, on eleven provinces.
```

**Replaced with:**

```
   The only modifiers read are the five that describe the province's own condition, and at 1444 two
   are live: `devastation` on eleven provinces and `unrest` on twenty-one.
```

### 173. `Y052` - §3.13

Y052: 3.13's copy of the count

**Removed:**

```
  reads development, the trade good and the four province-state modifiers, and nothing else — so
```

**Replaced with:**

```
  reads development, the trade good and the five province-state modifiers, and nothing else — so
```

### 174. `A1` - §1.6

A1: alpha is 2.0 and is a hyperparameter

**Removed:**

```
               b_w    = s_w − c_w                  α_Φ = 1.5, a stipulated constant (§2.3)
```

**Replaced with:**

```
               b_w    = s_w − c_w                  α_Φ = 2.0, a hyperparameter (§2.3)
```

### 175. `A2` - §1.6

A2: the count/placement sentence, at the new alpha

**Removed:**

```
the wealth field, and `α_Φ` sets how sharply concentration is read.** At the stipulated α_Φ = 1.5 the
1444 field gives two sinks, and a modestly grown Europe gives three or one (the Europe table below),
so neither the count nor the placement is fixed by the constant.
```

**Replaced with:**

```
the wealth field, and `α_Φ` sets how sharply concentration is read.** At α_Φ = 2.0 the 1444 field
gives two sinks, and a modestly grown Europe gives two, three or five (the Europe table below), so
neither the count nor the placement is fixed by the constant.
```

### 176. `A3` - §1.6

A3: largest |b_w| at the new alpha

**Removed:**

```
Normalising into (−1, 1) scales 1444's `b_w` *up* (its largest magnitude is 0.0225) and is safe;
```

**Replaced with:**

```
Normalising into (−1, 1) scales 1444's `b_w` *up* (its largest magnitude is 0.0347) and is safe;
```

### 177. `A4` - §1.6

A4: the sinks, and that the orientation is now order-invariant

**Removed:**

```
Measured on 1444 data at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and
`hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12. **One of those two is a property of
the world and the other is a property of the node ordering, and the difference matters more than the
count.** Phase 2's b-flow is degenerate (§2.4 item 1), so relabelling the nodes and re-running
returns a different optimal orientation. Over **800 relabellings** — eight seeds of 100, with `α_Φ`
and every input held fixed (`relabel6.py`) — **the orientation changed every time**, a mean of 25 of
159 edges moved, and the sink set came back exactly as `{english_channel, hangzhou}` in **64 of 800**
runs. **`hangzhou` was an end in about 98% of them and `english_channel` in about 40%.** The Asian
end is the robust one — not invariant, since orderings exist where it loses its end, but near enough
that it is a fact about that node. The European end is one of several the same world admits, and after
`english_channel` the most frequent are `gulf_of_siam` (a little over half the runs), `wien` (about a
third), then `rheinland` and `sevilla`. The count itself ranged 1 to 5, most often 2 or 3.

*The two leading proportions are quoted to two figures and the trailing ones qualitatively, because
that is as far as this sample supports: across three independent 800-trial sets `hangzhou` came in at
784–789 and `english_channel` at 322–336, while `sevilla` ranged 79–117 and `rheinland` 112–136. A
per-seed range is worse still, being a function of which seeds are drawn.*
```

**Replaced with:**

```
Measured on 1444 data at α_Φ = 2.0 (`measure6.py`): **two sinks, `genua` and `hangzhou`** — `c_w`
ranks 2 and 1, node-wealth ranks 4 and 12. **Both are properties of the world, because the
orientation does not depend on how the nodes are numbered.** That is a change from v6.0, and it is
worth stating why, since the previous version's argument turned on the opposite.

With unit arc costs Phase 2's b-flow is degenerate: many routings reach the same minimum cost, and
the simplex returns whichever its pivot path reaches, which moves with node numbering. Measured on
that LP directly, **40 of 40 permutations return a different optimal support** at an objective
identical to within a few units in the last place. So the old sink set was partly an artifact of the
node order, and v6.0 said so.

Phase 2 now breaks those ties inside the objective (§2.3), with a cost symmetric in the arc and read
from node wealth alone. On the same LP, **0 of 40 permutations return a different support**. Over
**180 relabellings** — three seeds of 60, every input held fixed (`relabel6.py`, which validates its
instrument against `drain.py` on the identity permutation before counting any trial) — **the
orientation did not change once**: 0 of 159 edges moved in any run, and the sink set came back as
`{genua, hangzhou}` in **180 of 180**. `hangzhou` and `genua` each held an end in every run.

*Two cautions for anyone re-running this. The instrument is a reimplementation, and a
reimplementation whose Phase 2 minimises the old objective disagrees with the shipped solver on 26 of
159 edges — `relabel6.py` aborts on exactly that, and did so when the tie-break went in. And a
symmetric cost is required, not a stylistic choice: a directional preference of the form
`1 − ε·(w[v] − w[u])` is a potential difference, so its total over any flow meeting the same `b` is
`Σ_n w[n]·b[n]` — the same for every feasible routing, and unable to break a tie at all.*
```

### 178. `B1` - §1.6

B1: nothing is conditional on the node order any more

**Removed:**

```
**What is conditional on the node order, and what is not.** Conditional: the sink set's membership
and size, and everything derived from them — §2.4's end-flag list, which European node holds an end in
the table below, and **the size of any node's drainage basin**. *No basin figure is quoted anywhere in
this section, because at the growth factors where one would be interesting `english_channel` holds an
end in only a handful of orderings, so any range is the spread of a handful of observations rather
than a measurement.* Not conditional, over the same relabellings: the map is fully oriented
(159/159) and acyclic every time, no fallback ever fires, and the LP objective is identical to
within four units in the last place, so these are different *optimal* orientations rather than
different answers. §2.4 item 1
requires the emitter to fix one canonical order for exactly this reason. Phase 1 selects `genua`; both sinks
arrive by stall promotion and `genua` ends a transit node, so there are **2 promotions and 0
fallbacks**. **Eight sources** — all in the bottom half of the wealth field, `c_w` ranks **44–75**,
mean degree **3.1** against the map's 4.0. *(v2 called them "cul-de-sacs", which their degrees do not
support.)* Every node drains to a sink; acyclic, 159/159 oriented; largest `|b_w|` **0.0225**; the
sink set is unchanged under ±1% wealth noise on three seeds. Its marking order is a per-node scalar
whose descending comparison reproduces the DAG (0 violations), so every consumer needing a potential
still gets one.

Per good, on the same field: **1–8 sinks, mean 3.72**, 29/29 acyclic, **0 fallbacks fired**, and
**89.6%** of ordered node pairs (5,663 of 6,320) connected by at least one good's directed path.

Agreement with the per-good graphs is **53.6%** of edge-goods (**52.3%** value-weighted). The
```

**Replaced with:**

```
**What is conditional on the node order.** Nothing that this document quotes. Over the 180
relabellings above, the sink set, every edge direction, the promotion and fallback counts and the
per-good figures were identical, so the distinction v6.0 drew between world-properties and
ordering-artifacts has collapsed into the first category. The emitter should still fix one canonical
order — the guarantee is measured over the orderings tried, not proved — and §2.4 item 1 records
that as an implementation requirement rather than a correctness worry.

Phase 1 selects `hangzhou`; `genua` arrives by stall promotion, so there is **1 promotion and 0
fallbacks**. **Five sources** — all in the bottom half of the wealth field, `c_w` ranks **55–79**,
mean degree **2.4** against the map's 4.0. *(v2 called them "cul-de-sacs"; at this α their degrees
are closer to that reading than at α_Φ = 1.5, where the mean was 3.1 — but it is a description of
five nodes, not a property of the operator.)* Every node drains to a sink; acyclic, 159/159 oriented;
largest `|b_w|` **0.0347**; the sink set is unchanged under ±1% wealth noise on three seeds. Its
marking order is a per-node scalar whose descending comparison reproduces the DAG (0 violations), so
every consumer needing a potential still gets one.

Per good, on the same field: **2–8 sinks, mean 3.69**, 29/29 acyclic, **0 fallbacks fired**, and
**90.5%** of ordered node pairs (5,721 of 6,320) connected by at least one good's directed path.

Agreement with the per-good graphs is **55.2%** of edge-goods (**55.0%** value-weighted). The
```

### 179. `B2` - §1.6

B2: alpha and epsilon are hyperparameters; no justification offered

**Removed:**

```
**`α_Φ = 1.5` is a stipulated design constant, exactly as `P₀ = 2.0` is.** It is superlinear so
that a few very rich provinces outweigh a dense mediocre region, and it is round. It is **not**
derived, and the document no longer offers a derivation: v2.1 through v4.0 said it was calibrated to
reproduce a two-sink 1444 map, and v5.0 said it sat in the widest sink-count band. The first was
fitted to a field that no longer exists; the second depended on where the α scan was truncated —
scanned over [1, 8] rather than [1, 3], the widest band is **1.71** wide ([3.50, 5.21],
`{doab, genua, hangzhou}`) and 1.5's is not the widest by any margin. Any future change to it is a
design decision about how many ends the installed graph should have, and §2.3 governs recording it.

What the value buys is recorded rather than argued. Across α_Φ = 1.00…8.00 at 0.01 the sink set is a
step function, and α_Φ = 1.5 sits in the band **[1.38, 1.63], width 0.25**, which gives
`{english_channel, hangzhou}`. Sampled at the six values v2 used, the count is non-monotone:
**6 → 2 → 1 → 2 → 3 → 1** across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}.

*A warning for anyone revising this, because the mistake is available and has been made twice: the
1444 map has two ends and vanilla's authored map has three, and it is tempting to justify 1.5 by
that resemblance. Do not. That is the calibration §2.3 withdrew, and §3.9's adoption argument does
not rest on it.*
```

**Replaced with:**

```
**`α_Φ = 2.0` and `TIE_EPS = 1e-3` are hyperparameters. The choice is developer taste, and this
document offers no justification for either beyond that.** No derivation is claimed, none is
implied, and none should be reconstructed from the figures below: they describe what the field does
around the chosen values, which is what an implementer needs in order to change them, not an argument
for keeping them.

Sensitivity, recorded rather than argued. Across α_Φ = 1.00…8.00 at 0.01 the sink set is a step
function, and α_Φ = 2.0 sits in the band **[1.63, 3.28], width 1.65**, which gives
`{genua, hangzhou}`. Sampled at six values, the count is non-monotone: **3 → 1 → 2 → 2 → 1 → 1**
across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}. For `TIE_EPS`, the sink set is unchanged from about **1e-6 to
about 1**, six orders of magnitude, because the term is a tie-break: below that range it falls under
the solver's tolerance and stops registering, and above it the term exceeds the base arc cost of 1
and stops being a perturbation. `scripts/epsilon6.py` reports the bands and bisects their edges.

*A warning for anyone revising this. Earlier versions justified α_Φ by resemblance to vanilla's
authored map, and then by band width. Both arguments were withdrawn, and neither should be
reintroduced — not because the figures were wrong, but because a hyperparameter chosen by taste does
not become better justified by finding a property that happens to hold at it.*
```

### 180. `C1` - §1.6

C1: the Europe narrative, re-measured

**Removed:**

```
**Europe becomes the centre of trade as it develops.** That is the design claim, and it is what
§3.1's first goal asks the field to deliver. At 1444 the map already ends in the Channel and in
Hangzhou; as European development compounds the ends move west and Asia's pole fades — the Channel's
basin widens, non-monotonically, and then gives way as the end itself migrates: `genua` first holds an
end at ×1.63 and is the sole end from ×1.64 through ×2.00 — and
past a broad range of European growth Asia holds no end at all. The mechanism is what carries this:
wealth is linear in development (§1.3), so developing a region moves its `c_w` share directly, and
`Φ_w`'s ends follow the wealth.

Observed on the 1444 field, holding α_Φ = 1.5 and scaling European development only (`europe.py`,
824 counted European provinces):

| European development | `Φ_w` sinks |
|---|---|
| ×1.00 (1444) | `english_channel`, `hangzhou` |
| ×1.02 | `english_channel`, `hangzhou`, **`wien`** |
| ×1.56 | `english_channel`, **`rheinland`** — Asia holds none |
| ×2.00 | `genua` alone |

Read the table as a direction rather than a trajectory, and on one node ordering: growth moves the
ends westward and thins Asia's, and by ×2.00 a single Mediterranean end at `genua` holds the map.
*Which* European node holds an end at the smaller factors is ordering-dependent in the same way the
1444 set is, so the direction is the claim and the membership is not. The last row is the exception
and is worth separating: at ×2.00 `genua` held an end in **60 of 60** relabellings, so a single
Mediterranean end under that much European growth is a property of the field rather than of the
ordering.
```

**Replaced with:**

```
**Europe becomes the centre of trade as it develops.** That is the design claim, and it is what
§3.1's first goal asks the field to deliver. At 1444 the map ends in Genoa and in Hangzhou; as
European development compounds Europe gains ends and Asia loses its one. The mechanism is what
carries this: wealth is linear in development (§1.3), so developing a region moves its `c_w` share
directly, and `Φ_w`'s ends follow the wealth.

Observed on the 1444 field, holding α_Φ = 2.0 and scaling European development only (`europe.py`,
824 counted European provinces). Boundaries are bisected, so each row is the interval over which the
set is constant:

| European development | `Φ_w` sinks |
|---|---|
| ×1.00 – ×1.14 | `genua`, `hangzhou` |
| ×1.14 – ×1.16 | `english_channel`, `genua`, `hangzhou`, **`rheinland`** |
| ×1.16 – ×1.19 | `genua`, `hangzhou` |
| ×1.19 – ×1.35 | `genua`, `hangzhou`, **`gulf_of_siam`** |
| ×1.35 – ×1.36 | `english_channel`, `genua`, `gulf_of_siam`, `hangzhou`, `rheinland` |
| ×1.36 – ×1.38 | `genua`, `gulf_of_siam` |
| **×1.38 – ×1.95** | **`english_channel`, `genua`, `rheinland` — Asia holds none** |
| ×1.95 – ×1.97 | `english_channel`, `genua`, `hangzhou`, `rheinland` |
| ×1.97 – ×2.46 | `english_channel`, `genua`, `rheinland` |
| ×2.46 – ×2.50 | `genua`, `rheinland` |

**Read the table as a direction, not a trajectory.** The direction is unambiguous: Europe goes from
one end to three and Asia goes from one to none, and the widest single interval in the table — ×1.38
to ×1.95 — is three European ends with nothing in Asia. But the path is not monotone. `hangzhou`
leaves at ×1.19, returns at ×1.95 and leaves again; `gulf_of_siam` holds an end across ×1.19–×1.38
and nowhere else; two intervals narrower than ×0.03 carry sets that appear once. Those reversals are
in the field, not in the solver: the orientation is order-invariant at every row.

*What this table is not evidence for. It scales all 824 counted European provinces by one factor at
once, which is not how development happens — real growth is province by province, with price changes
and colonisation on top. No save later than 1444 was available to test against, so the honest scope
is: this is the field's response to a uniform European multiplier, and the design intent is that
Europe's end strengthens as Europe develops. The intent is the claim; the row boundaries are a
property of one synthetic experiment.*
```

### 181. `D1` - §1.6

D1: the 1444 routes, re-measured at the shipped config

**Removed:**

```
**And the 1444 map draws the pre-Columbian trade geography unprompted.** The route from Genoa to
the Asian sink is the Silk Road: `genua → alexandria → aleppo → persia → lahore → lhasa →
ganges_delta → burma → gulf_of_siam → canton → hangzhou`. From the north it is the Volga:
`north_sea → white_sea → novgorod → kazan → astrakhan → persia → …`. **No route leaves
`english_channel` at all** — it is a sink, out-degree 0, so the Hansa and the Danube carry power
*into* it rather than out, and v5.0's "from the Channel it is the Hansa and the Danube" was
describing a path that does not exist. **No Europe→sink route passes the Cape of Good Hope** —
checked from `genua`, `north_sea` and `english_channel` — which is what a 1444 map should say.

The Cape is nonetheless a live conduit, not an idle one: in-degree 1, out-degree 3, with **132
ordered node pairs** whose path runs through it (`measure6.py`), carrying Atlantic drainage into the
Indian Ocean.
*(v5.0 said "nothing routes through the Cape", which is false as a universal and was only ever
checked on the Europe→sink routes.)* In the per-good graphs it also carries Asian spices to Europe;
`Φ_w` models power, not cargo (§3.9).
```

**Replaced with:**

```
**And the 1444 map draws the pre-Columbian trade geography unprompted.** Two long overland routes
reach the Asian end. From the north it is the Volga and the steppe:
`white_sea → novgorod → kazan → siberia → samarkand → lahore → lhasa → ganges_delta → burma →
gulf_of_siam → canton → hangzhou`. From Iberia it is the African coast and the Red Sea:
`sevilla → safi → timbuktu → katsina → ethiopia → gulf_of_aden → comorin_cape → ganges_delta → …`,
eleven hops. **No route leaves `genua` at all** — it is a sink, out-degree 0 against in-degree 5, so
the western Mediterranean, the Adriatic and the Rhône carry power *into* it. `english_channel` is
not an end at this α: it drains to `genua` in two hops through `champagne`, and reaches the Asian end
not at all.

**No Europe→sink route passes the Cape of Good Hope.** Checked exhaustively rather than sampled: of
the 23 European nodes there are **27** connected Europe→sink pairs, and for **0 of them** does a
Cape-transiting path exist. That is what a 1444 map should say, and it is the one place in this
section where a universal is asserted, because here the whole set was enumerated.

The Cape is nonetheless a live conduit, not an idle one: in-degree 2 (`zanzibar`, `ivory_coast`),
out-degree 2 (`comorin_cape`, `malacca`), with **81 ordered node pairs** for which a path through it
exists (`measure6.py` — the count is pairs `(a, b)` where `a` reaches the Cape, the Cape reaches `b`,
and `a` reaches `b`, not pairs whose shortest path happens to use it; the stricter shortest-path
reading gives 69 on the same field). It carries Atlantic drainage into the Indian Ocean. In the
per-good graphs it also carries Asian spices to Europe; `Φ_w` models power, not cargo (§3.9).
```

### 182. `D2` - §1.5

D2: coal activation flips, and the mixed counterfactual re-measured

**Removed:**

```
every graph in the model is entitled to move on it. Measured: repricing to coal the **45** of the
latent-coal provinces that are owned at 1444 — §1.3 counts only owned provinces — flips **10 of
159 `Φ_w` edges** and adds 214.60 ducats to world wealth (`measure6.py`). *The counterfactual holds
every non-repriced input fixed, which matters by more than rounding: province 4237 is both
latent-coal and one of the devastated eleven, and a reprice that drops its devastation measures coal
activating **plus** one province healing — worth 2.40 ducats and 3 extra flips.*
```

**Replaced with:**

```
every graph in the model is entitled to move on it. Measured: repricing to coal the **45** of the
latent-coal provinces that are owned at 1444 — §1.3 counts only owned provinces — flips **16 of
159 `Φ_w` edges** and adds 214.60 ducats to world wealth (`measure6.py`). *The counterfactual holds
every non-repriced input fixed. Province 4237 is both latent-coal and one of the devastated eleven, so
a reprice that drops its devastation measures coal activating **plus** one province healing — worth
2.40 ducats. On this field that mix moves no additional edge, where at α_Φ = 1.5 it moved three; the
reason to hold the input fixed is that the wealth figure is wrong either way, not that the edge count
always notices.*
```

### 183. `D3` - §1.10

D3: the survival-table coal row

**Removed:**

```
Measured: repricing the 45 owned latent-coal provinces flips 10 of 159 `Φ_w` edges (§1.5) |
```

**Replaced with:**

```
Measured: repricing the 45 owned latent-coal provinces flips 16 of 159 `Φ_w` edges (§1.5) |
```

### 184. `D4` - §3.13

D4: any-good connectivity

**Removed:**

```
measured, **89.6%** (5,663 of 6,320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. (v2 quoted 98.8%; that is v1's *Laplacian* figure, 6245/6320, carried across the operator change without being re-measured. The argument is unaffected — 89.6% is still most of the map — but the number was not v2's own.)
```

**Replaced with:**

```
measured, **90.5%** (5,721 of 6,320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. (v2 quoted 98.8%; that is v1's *Laplacian* figure, 6245/6320, carried across the operator change without being re-measured. The argument is unaffected — 90.5% is still most of the map — but the number was not v2's own.)
```

### 185. `E1` - §1.1

E1: 1.1's per-good sink range

**Removed:**

```
  goods, 1–8 sinks per good, mean 3.72, zero fallbacks.
```

**Replaced with:**

```
  goods, 2–8 sinks per good, mean 3.69, zero fallbacks.
```

### 186. `E2` - §1.6

E2: the Cape figures, phrased so one needle reaches all three

**Removed:**

```
The Cape is nonetheless a live conduit, not an idle one: in-degree 2 (`zanzibar`, `ivory_coast`),
out-degree 2 (`comorin_cape`, `malacca`), with **81 ordered node pairs** for which a path through it
exists (`measure6.py` — the count is pairs `(a, b)` where `a` reaches the Cape, the Cape reaches `b`,
and `a` reaches `b`, not pairs whose shortest path happens to use it; the stricter shortest-path
reading gives 69 on the same field). It carries Atlantic drainage into the Indian Ocean.
```

**Replaced with:**

```
The Cape is nonetheless a live conduit, not an idle one: in-degree 2, out-degree 2, with **81
ordered node pairs** for which a path through it exists (`measure6.py`). It takes flow from
`zanzibar` and `ivory_coast` and passes it to `comorin_cape` and `malacca`, carrying Atlantic
drainage into the Indian Ocean. *The count is pairs `(a, b)` where `a` reaches the Cape, the Cape
reaches `b`, and `a` reaches `b` — not pairs whose shortest path happens to use it, which is a
stricter reading and gives 69 on the same field.*
```

### 187. `F1` - §2.3

F1: 2.3 declares both hyperparameters and justifies neither

**Removed:**

```
Design constants: the excluded-goods list (defaults to gold), the α price anchor `P₀ = 2.0`,
the aggregate-graph exponent `α_Φ = 1.5` (a **stipulated** constant like `P₀`: superlinear, round,
and chosen rather than derived — world-responsiveness flows through wealth, never through this
knob). **Every derivation previously offered for it is withdrawn.** v2.1 through v4.0 said 1.5 was
calibrated so that 1444 yields a two-sink map; v5.0 said it sat in the widest sink-count band.
Neither is a reason: the first fits a constant to one date, and the second depended on where the α
scan was truncated (§1.6). Any future change to it is a design decision about how many ends the
installed graph should have, and should be recorded as one, and DRAIN's three knobs at their
defaults — demand-mass
```

**Replaced with:**

```
Design constants: the excluded-goods list (defaults to gold), the α price anchor `P₀ = 2.0`,
the aggregate-graph exponent `α_Φ = 2.0`, the Phase-2 tie-break strength `TIE_EPS = 1e-3`, and
DRAIN's three knobs at their defaults — demand-mass
```

### 188. `F2` - §2.3

F2: the hyperparameter statement, and what the tie-break cost is

**Removed:**

```
is **not** purely numerical: it is an absolute threshold, so it couples to the scale of `b`. See
§1.6's scale-invariance note and §3.13. A measured calibration option
that moves all three plus α's clamp is recorded in §3.13; the baseline does not use it.
```

**Replaced with:**

```
is **not** purely numerical: it is an absolute threshold, so it couples to the scale of `b`. See
§1.6's scale-invariance note and §3.13. A measured calibration option
that moves all three plus α's clamp is recorded in §3.13; the baseline does not use it.

**`α_Φ` and `TIE_EPS` are hyperparameters. Their values are developer taste, and this document
offers no justification for either.** Every derivation previously offered for `α_Φ` is withdrawn and
none replaces it: v2.1 through v4.0 said it was calibrated so that 1444 yields a two-sink map, and
v5.0 said it sat in the widest sink-count band. Both are withdrawn. Changing either value is a design
decision, and §1.6 records how the field responds around them so that the decision can be made with
the sensitivity in view — that is documentation for whoever changes them, not an argument for the
current values.

`TIE_EPS` sets the Phase-2 objective. With unit arc costs the min-cost b-flow is degenerate, so the
orientation depends on node numbering; the tie-break puts the choice in the objective instead:

```
cost(u, v) = 1 + TIE_EPS · (w[u] + w[v]) / 2        w = node wealth, normalised to [0, 1]
```

Two properties are load-bearing and neither is a matter of taste. The cost is **symmetric** in the
arc: a directional preference of the form `1 − ε·(w[v] − w[u])` is a potential difference, so its
total over any flow satisfying the same `b` equals `Σ_n w[n]·b[n]` — identical for every feasible
routing, and unable to break a tie. And it reads **node wealth only**, so it is invariant under
relabelling by construction. The normalisation is not load-bearing: dividing by the maximum, the mean
or the world total gives the same orientation, because rescaling `w` is equivalent to rescaling
`TIE_EPS` and the answer is constant over about six orders of magnitude of it (§1.6).

Only DRAIN's Phase 2 uses this cost. The per-good flow operators in `flowop.py` and the checks in
`verify.py` keep unit arc costs, and `mincost_flow`'s cost argument defaults to unit for that reason.
```

### 189. `F3` - §0

F3: the front matter's summary of the node-order issue

**Removed:**

```
`add_base_*` accumulation, and the `is_city` filter the engine does not apply), and §2.4 now states
the reason a canonical node order is a correctness requirement: **Phase 2's min-cost flow is
degenerate, so presentation order selects which optimum is returned.**
```

**Replaced with:**

```
`add_base_*` accumulation, and the `is_city` filter the engine does not apply). **Phase 2's min-cost
flow is degenerate under unit arc costs, so presentation order selected which optimum was returned;
§2.3 now breaks that tie inside the objective, and §1.6 measures the orientation as unchanged across
every relabelling tried.** A canonical node order remains an emitter requirement, but it is no longer
what decides the map.
```

### 190. `G1` - §2.4

G1: 2.4 item 1, rewritten around the adopted tie-break

**Removed:**

```
1. **Declaration order** — emit in decreasing `Φ_w` marking order. This is the convention the
   engine states and the shipped vanilla file follows (0 of 159 links violate it), and violating
   it is non-fatal but logs one error per link. **The node order itself is a correctness
   requirement, not a convention, and the reason is Phase 2 rather than any tiebreak.** The
   min-cost b-flow is *massively degenerate*: many distinct supports carry the same optimal cost, and
   which one the solver returns depends on the order the nodes and arcs are presented in. Measured on
   1444, relabelling the nodes and running the aggregate graph end-to-end changed the orientation in
   **400 of 400** runs across four independent seeds, **always** by returning a different optimal
   vertex and **never** by a sweep tiebreak, with a mean of **25 of 159 edges** moving and the LP
   objective identical to within four units in the last place — 4.44e-16 absolute against an objective
   of 0.712, which is the same quantity as the 6.2e-16 relative deviation and not a second measurement,
   and which grows to 6–7 ULP at larger trial counts, so it is a sample maximum rather than a bound
   (`relabel6.py`, which validates its instrument against
   `drain.py` on the identity permutation and aborts if that fails). Twenty-five flips is the same
   magnitude as the razed-China perturbation §2.8 treats as a major world event. The same effect on the
   **per-good** graphs is 580 of 580 (29 goods × 20 relabellings), from
   `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`. *(v6.0 withdrew that sweep on the ground that
   its script had never shipped. The script is in the tree and runs; the withdrawal was the error, not
   the figure. No v1–v5 spec ever printed it either, so it was never "quoted by earlier versions" —
   it comes from this project's working files.)*

   So the emitter must fix one canonical node order and keep it stable across rebuilds, and that
   order must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks
   ties in. Everything §1.6 and §2.8 report about stability is measured **at fixed node order**;
   re-order the same world and the map moves, with `α_Φ` and every input held fixed. The specific counts
   are HiGHS-specific in their detail but not in kind — any simplex returns *a* vertex of a degenerate
   optimal face. Making the orientation independent of presentation order would need a tie-breaking
   objective (a lexicographic secondary cost, or a strictly convex perturbation); that is a design
   change and is not adopted here.
```

**Replaced with:**

```
1. **Declaration order** — emit in decreasing `Φ_w` marking order. This is the convention the
   engine states and the shipped vanilla file follows (0 of 159 links violate it), and violating
   it is non-fatal but logs one error per link. **A canonical node order is still a correctness
   requirement, but it is no longer what decides the installed map.** The reason is worth setting out
   in full, because it changed in v6.1 and the previous version's argument was the opposite.

   Phase 2's min-cost b-flow is degenerate under unit arc costs: many distinct supports carry the same
   optimal cost, and which one the solver returns depends on the order the nodes and arcs are presented
   in. Measured on that objective, **40 of 40** permutations return a different optimal support at an
   objective identical to within a few units in the last place. §2.3 now breaks those ties inside the
   objective. On the same LP under the tie-break cost, **0 of 40** permutations return a different
   support, and running the aggregate graph end-to-end over **180 relabellings** (three seeds of 60)
   moved **0 of 159 edges** in every run (`relabel6.py`, which validates its instrument against
   `drain.py` on the identity permutation and aborts if that fails — and did abort when the tie-break
   went in, because the instrument still minimised the old objective and disagreed on 26 of 159 edges).

   **The per-good graphs are a different matter, and this is why the requirement survives.** The
   tie-break cost is built from node wealth, which is good-independent, so it applies to every per-good
   solve — but a wealth-weighted cost need not break ties in a per-good LP, whose `b` is a different
   vector. Measured across 29 goods × 10 relabellings: **84 of 290** runs changed a per-good
   orientation, a mean of 0.99 edges and up to 15. So the installed aggregate graph is invariant over
   the orderings tried, while the per-good graphs — which set value weights and the §1.10 survival
   table — are not.

   So the emitter must fix one canonical node order and keep it stable across rebuilds, and that
   order must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks
   ties in. The counts are HiGHS-specific in their detail but not in kind — any simplex returns *a*
   vertex of a degenerate optimal face, and the tie-break's job is to leave only one vertex to return.
   *(v6.0 quoted a 580-of-580 per-good sweep from
   `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`. That script measures the unit-cost objective,
   so its figure describes the former solver and is superseded by the 84-of-290 above rather than
   contradicted by it.)*
```

### 191. `G2` - §2.4

G2: item 2's end-flag list is no longer order-dependent

**Removed:**

```
2. **End flags** — `end=yes` on every `Φ_w` sink. **This list is a function of the canonical node
   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end in about
   98% of relabellings, `english_channel` in about 40%, and the count ranges 1 to 5 (§1.6). Fix the order, emit, and keep it — changing it changes the flags without anything in the
   world changing. (1444, shipped order: **two** end nodes, `english_channel` and
   `hangzhou`, against
   vanilla's three); stripped from any former end node that gains outgoing links. The count is not
   fixed — it follows the wealth field and `α_Φ` (§1.6), so the emitter reads it from the solve
   rather than assuming a number.
```

**Replaced with:**

```
2. **End flags** — `end=yes` on every `Φ_w` sink. **This list is a function of the world, not of the
   node order:** across the 180 relabellings in item 1 the end set came back as
   `{genua, hangzhou}` every time (§1.6). That is a change from v6.0, where the list moved with the
   ordering and this item warned about it. (1444: **two** end nodes, `genua` and `hangzhou`, against
   vanilla's three); stripped from any former end node that gains outgoing links. The count is not
   fixed — it follows the wealth field and `α_Φ` (§1.6), so the emitter reads it from the solve
   rather than assuming a number.
```

### 192. `H1` - §2.8

H1: 2.8's Razed China row, re-measured

**Removed:**

```
| Razed China | *This row is ordering-robust where §1.6's sink membership is not: it turns on `hangzhou` holding an end, which it does in about 98% of relabellings (§1.6) — and on the razed field itself `hangzhou` loses its end in every relabelling tried, which is what the row asserts.* Zeroing `hangzhou`-node development relocates an end in one solve — measured: the `Φ_w` sinks move from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`, 22 of 159 edges flipping. `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth 226.7 against 143.0, and it holds the richest single province the model counts. Zeroing `beijing` **also** moves the map — 15 flips — because deleting a percent of world wealth renormalises `c_w` everywhere; what separates the two is that `hangzhou` **survives as a sink** when `beijing` is zeroed and does not when `hangzhou` is. *(v2 through v4.0 said zeroing `beijing` "moves nothing". It does; the asymmetry is which node keeps its end, not whether the map moves.)* |
```

**Replaced with:**

```
| Razed China | Zeroing `hangzhou`-node development relocates an end in one solve — measured: the `Φ_w` sinks move from `{genua, hangzhou}` to `{genua, gulf_of_siam}`, 30 of 159 edges flipping. `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth 226.7 against 143.0 — ranks 12 and 39 of the 79 nodes holding counted provinces — and it holds the richest single province the model counts. Zeroing `beijing` **also** moves the map — 8 flips — because deleting a percent of world wealth renormalises `c_w` everywhere; what separates the two is that `hangzhou` **survives as a sink** when `beijing` is zeroed and does not when `hangzhou` is. *(v2 through v4.0 said zeroing `beijing` "moves nothing". It does; the asymmetry is which node keeps its end, not whether the map moves.)* *On the razed field the result is order-invariant like the baseline: 40 of 40 relabellings return `{genua, gulf_of_siam}` and `hangzhou` holds an end in none of them. v6.0 had to argue this row was robust where the baseline sink set was not; §2.3's tie-break removes the distinction.* |
```

### 193. `H2` - §3.2

H2: 3.2's reference to the degeneracy as a live defect

**Removed:**

```
   comes from Phase 2's degenerate LP, which moves the orientation under relabelling even when no key
```

**Replaced with:**

```
   came from Phase 2's LP under unit costs, which moved the orientation under relabelling even when no key
```

### 194. `H3` - §1.5

H3: drop the former-alpha comparison in 1.5

**Removed:**

```
2.40 ducats. On this field that mix moves no additional edge, where at α_Φ = 1.5 it moved three; the
reason to hold the input fixed is that the wealth figure is wrong either way, not that the edge count
always notices.*
```

**Replaced with:**

```
2.40 ducats. On this field that mix moves no additional edge, so the reason to hold the input fixed is
that the wealth figure is wrong either way, not that the edge count reliably notices.*
```

### 195. `H4` - §1.6

H4: drop the former-alpha comparison in 1.6

**Removed:**

```
mean degree **2.4** against the map's 4.0. *(v2 called them "cul-de-sacs"; at this α their degrees
are closer to that reading than at α_Φ = 1.5, where the mean was 3.1 — but it is a description of
five nodes, not a property of the operator.)*
```

**Replaced with:**

```
mean degree **2.4** against the map's 4.0. *(v2 called them "cul-de-sacs"; the degrees are not far
off that reading here, but it is a description of five nodes on one field, not a property of the
operator.)*
```

### 196. `I1` - §3.13

I1: 3.13's self-coherence baseline

**Removed:**

```
  baseline is known — `Φ_w` agrees with the per-good graphs on **52.3%** of edge-goods *weighted by
  trade value*, and on 53.6% unweighted (§1.6) —
```

**Replaced with:**

```
  baseline is known — `Φ_w` agrees with the per-good graphs on **55.0%** of edge-goods *weighted by
  trade value*, and on 55.2% unweighted (§1.6) —
```

### 197. `I2` - §3.6

I2: 3.6's degeneracy premise, narrowed by the tie-break

**Removed:**

```
support, which is a discrete selection. Measured on 1444: across 29 goods × 6 random 1e-9 demand
nudges, **zero** support-membership changes moved more than 1e-6 of flow, and the ±1% wealth-noise
flips all sat on near-zero-flow edges. At exactly degenerate inputs — two equal-hop corridors — the
map from `b` to the chosen support is discontinuous in principle, so this rests on the solver's
tie-selection being stable, which is the same premise §3.13 tracks for multiplayer.
```

**Replaced with:**

```
support, which is a discrete selection. Measured on 1444: across 29 goods × 6 random 1e-9 demand
nudges, **zero** support-membership changes moved more than 1e-6 of flow, and under ±1% wealth noise
on six seeds the aggregate map moved **no edge at all**. At exactly degenerate inputs — two equal-hop
corridors — the map from `b` to the chosen support is discontinuous in principle. §2.3's tie-break
narrows where that bites: on the aggregate graph it leaves the optimum unique, so the result no longer
rests on the solver's tie-selection; on the per-good graphs, whose `b` a wealth-weighted cost need not
separate, it still does (§2.4 item 1), and that is the premise §3.13 tracks for multiplayer.
```

### 198. `I3` - §3.9

I3: 3.9 stops quoting figures for a rejected operator

**Removed:**

```
  artifacts of sweep scheduling rather than places — and the sharpest evidence for that is what
  relabelling does to them: across 20 relabellings the end count runs **12 to 19** and the end set is
  **never twice the same**, so neither the count nor the share terminating no good is a property of
  the world. Most of those ends terminate no good,
```

**Replaced with:**

```
  artifacts of sweep scheduling rather than places — and the sharpest evidence for that is what
  relabelling does to them: its end count and end set both move with the node order, where `Φ_w`'s do
  not (§2.4 item 1 measures the installed graph as invariant over the orderings tried). No figure is
  given for `Φ_ord`'s spread, because the operator is not installed and R3 forbids maintaining one.
  Most of those ends terminate no good,
```

### 199. `J1` - §1.6

J1: the b-scaling figures, re-measured

**Removed:**

```
scaling `b` *down* pushes genuine flow arcs into the free set. Measured: identical orientation at
×1 and above, 12 edge flips at ×10⁻², and 100 at ×10⁻⁶, where the sink set also collapses to
`{genua}` — the orientation degrades and the sink
set happens to survive, so the sink set is not the quantity to watch here.
```

**Replaced with:**

```
scaling `b` *down* pushes genuine flow arcs into the free set. Measured: identical orientation from
×1 down to ×10⁻², **22** edge flips at ×10⁻⁴ where the sink set becomes `{english_channel, hangzhou}`,
and **96** at ×10⁻⁶ where it becomes `{hangzhou}`. The orientation degrades before the sink set does,
so the sink set is not the quantity to watch here.
```

### 200. `J2` - §1.6

J2: the European-node scaling note, re-measured

**Removed:**

```
model: scaling the 22 European *nodes* rather than European provinces makes `genua` the sole sink
from about ×1.65 (the 18-node western/central subset needs about ×2.15), and somewhere inside
roughly ×2.9–×3.5 the Cape of Good Hope **reverses** — 1444's Atlantic→Cape→Indian-Ocean drainage
becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast. The reversal is bounded above as well as
below, so it is a window and not a threshold, and its edges move with the field.
```

**Replaced with:**

```
model: scaling the 18 western and central European *nodes* rather than European provinces makes
`genua` the sole sink from about ×1.55, while scaling all 22 does not produce a sole sink anywhere
below ×4 — the eastern four keep pulling ends of their own. The Cape of Good Hope **reverses** under
the same growth: 1444's `ivory_coast`/`zanzibar`→Cape→`comorin_cape`/`malacca` drainage becomes
`comorin_cape`/`malacca`/`zanzibar`→Cape→`ivory_coast` by about ×1.6 on the 22-node scaling. It is not
a single window — the Cape's in- and out-sets change several times across ×1–×3 and reverse more than
once — so the observation is that the Cape's direction is a function of European development, not that
there is a threshold at which it turns.
```

### 201. `J3` - §3.9

J3: 3.9's wealth-versus-sink illustration, with the correct roles

**Removed:**

```
intent from the world state instead of authoring it: all wealth pulls (a rich non-sink node —
`genua`, `gulf_of_siam` and `sevilla` rank 4th, 3rd and 7th by node wealth on the corrected field
(`mexico` is 2nd)
— 296.0, 297.9 and 266.5 against `english_channel`'s 316.6, which is a sink — draws more edges in than it sends out as a net demander even though flow passes through),
the wealthiest places win, and the ends emerge and move when the wealth moves —
```

**Replaced with:**

```
intent from the world state instead of authoring it. **Wealth pulls, but the wealthiest node is not
automatically an end.** On this field `english_channel` is the richest node at 316.6 and is *not* a
sink: it drains to `genua`, which is 4th at 296.0. `mexico` (300.4, 2nd), `gulf_of_siam` (297.9, 3rd)
and `sevilla` (266.5, 7th) are likewise net demanders that draw more edges in than they send out
while flow still passes through them. What makes an end is where the flow *terminates*, which is a
property of the whole field and the graph rather than of a single node's rank — and the ends emerge
and move when the wealth moves —
```

### 202. `K1` - §0

K1: the version, since the document now refers back to v6.0

**Removed:**

```
**Version:** 6.0
```

**Replaced with:**

```
**Version:** 6.1
```

### 203. `K2` - §0

K2: what v6.1 changes

**Removed:**

```
Three start-state reads are corrected in the same pass (`on_startup` devastation, dated
`add_base_*` accumulation, and the `is_city` filter the engine does not apply). **Phase 2's min-cost
flow is degenerate under unit arc costs, so presentation order selected which optimum was returned;
§2.3 now breaks that tie inside the objective, and §1.6 measures the orientation as unchanged across
every relabelling tried.** A canonical node order remains an emitter requirement, but it is no longer
what decides the map.
```

**Replaced with:**

```
Three start-state reads are corrected in the same pass (`on_startup` devastation, dated
`add_base_*` accumulation, and the `is_city` filter the engine does not apply).

**v6.1** changes two things, both in the operator rather than the field. **Phase 2's min-cost flow is
degenerate under unit arc costs, so presentation order selected which optimum was returned; §2.3 now
breaks that tie inside the objective, and §1.6 measures the installed orientation as unchanged across
every relabelling tried.** A canonical node order remains an emitter requirement — the per-good
graphs are still order-sensitive (§2.4 item 1) — but it is no longer what decides the installed map.
And **`α_Φ` moves from 1.5 to 2.0.** Both `α_Φ` and the new `TIE_EPS` are hyperparameters whose values
are developer taste; §2.3 states them and offers no justification for either, and every derivation
previously offered for `α_Φ` is withdrawn without replacement. The 1444 sink set moves from
`{english_channel, hangzhou}` to `{genua, hangzhou}` and 29 of the 59 figures `measure6.py` prints
move with it.
```

### 204. `K3` - §1.1

K3: 1.1's Phase 2 describes the cost it actually minimises

**Removed:**

```
**Phase 2 — route: min-cost b-flow.** Solve the uncapacitated min-cost flow with unit arc costs
serving `b_g`, and orient every support edge by its net flow. The support is a spanning-tree basis
of ≤ N−1 edges **when the solver returns a basic (vertex) optimum**, which the simplex family
does; an interior-point solve without crossover can split flow across equal-length parallel paths
and return a support with an undirected cycle in it. §2.2 therefore requires network simplex or a
simplex LP. What holds for *any* optimum is the weaker and sufficient property: the support
contains **no directed cycle**, because with all costs 1 a directed cycle could be cancelled for
strictly lower cost. Edges with zero net flow are *free* and deferred to Phase 3.
```

**Replaced with:**

```
**Phase 2 — route: min-cost b-flow.** Solve the uncapacitated min-cost flow serving `b_g` and orient
every support edge by its net flow. Arc costs are `1 + TIE_EPS·(w[u] + w[v])/2` — near-unit, symmetric
in the arc, and read from node wealth (§2.3). They are not unit because with unit costs the optimum is
not unique and which one the solver returns depends on the order the nodes are presented in; the
near-unit perturbation leaves one optimum to return. The support is a spanning-tree basis
of ≤ N−1 edges **when the solver returns a basic (vertex) optimum**, which the simplex family
does; an interior-point solve without crossover can split flow across equal-length parallel paths
and return a support with an undirected cycle in it. §2.2 therefore requires network simplex or a
simplex LP. What holds for *any* optimum is the weaker and sufficient property: the support
contains **no directed cycle**, because with all costs strictly positive a directed cycle could be
cancelled for strictly lower cost — an argument that needs positivity, not unit costs, so it survives
the change. Edges with zero net flow are *free* and deferred to Phase 3.
```

### 205. `K4` - §0

K4: the harness's own check count

**Removed:**

```
**`verify6.py` pins 35 distinct figures across 29 checks, and that is well short of what the document
prints.**
```

**Replaced with:**

```
**`verify6.py` runs 31 checks against values computed from the install, and that is well short of
what the document prints.**
```

### 206. `L1` - §0

L1: the check count the harness now verifies

**Removed:**

```
**`verify6.py` runs 31 checks against values computed from the install, and that is well short of
what the document prints.**
```

**Replaced with:**

```
**`verify6.py` runs 32 checks against values computed from the install, and that is well short of
what the document prints.** One of those 32 is this sentence: the harness reads its own stated count
out of the document and fails when it disagrees with the count it actually ran, because a stale
self-description is invisible to every other check in it.
```

### 207. `M1` - §1.1

M1: the Efficiency property under the tie-break objective

**Removed:**

```
- **Efficiency.** Unit costs make the certificate flow a fewest-hop routing in aggregate — the
  objective *is* `Σ (flow × hops)`, so the optimum minimises total flow-hops. No per-unit
  shortest-path claim is made, and none holds: a unit may detour when sink assignment demands it.
  **This one carries no measurement and wants none:** it is true by construction of the LP, and
  any hop count we produced would be re-deriving the objective rather than testing it. The §3.13
  calibration deliberately degrades it, which is a change to the program being solved, not
  evidence about this property.
```

**Replaced with:**

```
- **Efficiency.** The certificate flow is a near-fewest-hop routing in aggregate. With unit costs the
  objective would be exactly `Σ (flow × hops)`; the tie-break makes it
  `Σ (flow × cost)` with `cost ∈ [1, 1 + TIE_EPS]`, so the optimum minimises a hop count in which a
  hop between two wealthy nodes counts marginally more (§2.3). At `TIE_EPS = 1e-3` the spread is under
  a tenth of a percent of the base cost, so the routing is within that factor of fewest-hop — but
  "fewest-hop" is now an approximation with a stated bound rather than an identity, and that is the
  price of a unique optimum. No per-unit shortest-path claim is made, and none holds: a unit may
  detour when sink assignment demands it.
  **This one carries no measurement and wants none:** it follows from the construction of the LP, and
  any hop count we produced would be re-deriving the objective rather than testing it. The §3.13
  calibration deliberately degrades it, which is a change to the program being solved, not
  evidence about this property.
```

### 208. `N1` - §1.3

N1: devastation's scaling is documented, not assumed

**Removed:**

```
| | *The magnitudes and directions above are all read from `00_static_modifiers.txt`. What no shipped file states is the **scaling law** for `devastation`: the model assumes the modifier applies in proportion to the level, `-2 × level/100`, and that proportionality is an assumption rather than a file value. It is the **only** such assumption in this table — `unrest` and `nationalism` both carry per-unit comments in that same file, so the convention for stating a scaling exists and `devastation` simply does not use it.* | |
```

**Replaced with:**

```
| | *The magnitudes and directions above are all read from `00_static_modifiers.txt`. That file does not state the **scaling law** for `devastation`, and it is the only row here whose scaling it leaves open — `unrest` and `nationalism` both carry per-unit comments in it. The wiki settles the law: the penalties are "scaled linearly according to the percentage value" and are quoted at 100% devastation, which is the `-2 × level/100` the model applies. **This is the one row whose scaling rests on community documentation rather than on a shipped file**, and that difference is worth stating rather than smoothing over.* | |
```

### 209. `N2` - §1.3

N2: unrest is identified but not read by the model

**Removed:**

```
`occupied` and `unrest` touch the tax term; the other three reach `goods_produced` alone. **`unrest`
is live at the 1444 start**: 21 counted provinces carry revolt risk between 4.834 and 14.834 in the
save, costing **12.23 ducats — 0.115% of world wealth** — and admitting it moves **no edge** of the
installed graph, so it is a fidelity correction with no orientation consequence. *Its scaling is
stated in the file:* the `unrest` block's own comment reads `#10% longer time to build troops for each
rr`, so its values apply per point, and the neighbouring `nationalism` block uses the same convention.
*(Sixteen of the 21 are resolvable from `history/provinces` at integer risk 5/8/10/15; the other five,
all Shirvan-owned, receive theirs at runtime, so the model reads the save.)* These are what
```

**Replaced with:**

```
`occupied` and `unrest` touch the tax term; the other three reach `goods_produced` alone. *Its
scaling is stated in the file:* the `unrest` block's own comment reads `#10% longer time to build
troops for each rr`, so its values apply per point, and the neighbouring `nationalism` block uses the
same convention.

**`unrest` is live at the 1444 start and the reference implementation does not read it.** This is a
known gap, stated rather than papered over: `solver.py`'s `STATE_TAX_MOD` carries `occupied` alone,
so four of the five rows above are applied and `unrest` is not. What it would cost is measured. 21
counted provinces carry revolt risk between 4.834 and 14.834 in the start save — the figure is stable
across all three start saves in the tree — worth **12.23 ducats, 0.115%** of the 10,607.40 the model
computes; applying it would put world wealth at **10,595.17** and move **4 of 159 edges** of the
installed graph, leaving the sink set `{genua, hangzhou}` unchanged. *(An earlier version of this
paragraph said admitting it moves no edge. That was measured at α_Φ = 1.5 and does not hold at 2.0.)*
Closing the gap is a one-line change to `STATE_TAX_MOD` plus reading the save, and it moves the world
wealth figure that the rest of this document quotes, so it is recorded here as a decision rather than
made silently.

*(Sixteen of the 21 are resolvable from `history/provinces` at integer risk 5/8/10/15; the other five,
all Shirvan-owned, receive theirs at runtime, so reading them needs the save.)* These are what
```

### 210. `N3` - §1.3

N3: the table's lead-in says which are applied

**Removed:**

```
**Province condition is the one thing besides development and the good that wealth reads.** Five
static modifiers describe a province's own state, and all five are read from
`common/static_modifiers/00_static_modifiers.txt`:
```

**Replaced with:**

```
**Province condition is the one thing besides development and the good that wealth reads.** Five
static modifiers describe a province's own state, all five are defined in
`common/static_modifiers/00_static_modifiers.txt`, and **four of the five are applied by the
reference implementation** — see the note below the table on `unrest`:
```

### 211. `O1` - §2.2

O1: 2.2's build step names what is actually applied

**Removed:**

```
   The only modifiers read are the five that describe the province's own condition, and at 1444 two
   are live: `devastation` on eleven provinces and `unrest` on twenty-one. `GP_COEFF` is **read from**
```

**Replaced with:**

```
   The only modifiers in scope are the five that describe the province's own condition, of which the
   reference implementation applies four; at 1444 `devastation` is live on eleven provinces, and
   `unrest` is live on twenty-one and **not read** (§1.3). `GP_COEFF` is **read from**
```

### 212. `O2` - §3.13

O2: 3.13's open question, scoped to what is applied

**Removed:**

```
  reads development, the trade good and the five province-state modifiers, and nothing else — so
```

**Replaced with:**

```
  reads development, the trade good and the province-state modifiers of §1.3 — four of the five
  applied — and nothing else, so
```

### 213. `P1` - §0

P1: no maintained figure for the harness's own size

**Removed:**

```
**`verify6.py` runs 32 checks against values computed from the install, and that is well short of
what the document prints.** One of those 32 is this sentence: the harness reads its own stated count
out of the document and fails when it disagrees with the count it actually ran, because a stale
self-description is invisible to every other check in it.
```

**Replaced with:**

```
**`verify6.py` checks figures in this document against values computed from the install, and it
covers well under half of what the document prints.** No count is given here: some of its checks are
generated per matching phrase, so the total moves whenever the prose does. The harness prints its own
count when it runs, and that is where to read it.
```

### 214. `Q1` - §2.2

Q1: the MP exposure, narrowed by the tie-break

**Removed:**

```
exposure is narrower than v1's dense linear algebra but still real: the min-cost-flow solve must
pivot identically given identical input (fixed arc ordering, one solver build, no threading), and
the sweep is deterministic given the LP's support and a fixed accumulation order — its comparisons
are of input-derived floats (`DEF`, `b`), not of solver residuals, which is the distinction that
matters against v1's dense algebra, but it is not integer arithmetic and v2 called it that. Its
cross-machine reproducibility reduces to the LP's.
```

**Replaced with:**

```
exposure is narrower than v1's dense linear algebra but still real: the min-cost-flow solve must
return the same optimum given identical input (fixed arc ordering, one solver build, no threading),
and the sweep is deterministic given the LP's support and a fixed accumulation order — its comparisons
are of input-derived floats (`DEF`, `b`), not of solver residuals, which is the distinction that
matters against v1's dense algebra, but it is not integer arithmetic and v2 called it that. Its
cross-machine reproducibility reduces to the LP's.

§2.3's tie-break narrows one part of this and leaves the rest. On the aggregate graph the optimum is
unique, so *which vertex of a degenerate optimal face the solver lands on* is no longer a desync path
— that was the largest single exposure and it is closed. What remains is ordinary float
reproducibility: the cost vector itself is computed from wealth, so the same accumulation-order
question applies to it. And the per-good graphs are untouched — their optima are still degenerate
(§2.4 item 1), so vertex selection remains an exposure there, and the value weights and survival table
are downstream of it.
```

### 215. `R1` - §1.3

R1: unrest is excluded on owner-agnosticism grounds, not pending

**Removed:**

```
**`unrest` is live at the 1444 start and the reference implementation does not read it.** This is a
known gap, stated rather than papered over: `solver.py`'s `STATE_TAX_MOD` carries `occupied` alone,
so four of the five rows above are applied and `unrest` is not. What it would cost is measured. 21
counted provinces carry revolt risk between 4.834 and 14.834 in the start save — the figure is stable
across all three start saves in the tree — worth **12.23 ducats, 0.115%** of the 10,607.40 the model
computes; applying it would put world wealth at **10,595.17** and move **4 of 159 edges** of the
installed graph, leaving the sink set `{genua, hangzhou}` unchanged. *(An earlier version of this
paragraph said admitting it moves no edge. That was measured at α_Φ = 1.5 and does not hold at 2.0.)*
Closing the gap is a one-line change to `STATE_TAX_MOD` plus reading the save, and it moves the world
wealth figure that the rest of this document quotes, so it is recorded here as a decision rather than
made silently.
```

**Replaced with:**

```
**`unrest` is live at the 1444 start and is deliberately not read.** It is the one row in the table
that fails the test the rest of §1.3 is built on: **revolt risk is not a property of the place.** In
play it carries separatism from recent conquest, unaccepted culture, wrong religion and nationalism —
all of them relations between a province and *its owner*. Read it, and a province's wealth changes
when it is conquered, which is precisely what this section exists to prevent. `solver.py`'s
`STATE_TAX_MOD` therefore carries `occupied` alone, and four of the five rows above are applied.

The 1444 field shows the split directly. Of the 21 counted provinces carrying revolt risk in the start
save, **16 are authored in `history/provinces`** at integer 5/8/10/15 — Sofala's comment reads
"expansion of Shona into Sofala region causes major disruptions" — and the remaining **five are all
Shirvan-owned and receive theirs at runtime**. So even at the start date a quarter of it is owner-
derived, and during a campaign that share only grows.

**And the effect it would buy is already bought.** Conquest costing a province its wealth is delivered
by `devastation`, `occupied` and `under_siege`, all three of which are properties of the place and all
three of which the model applies. `unrest` would add owner-dependence without adding a mechanic.

What the exclusion costs is measured, so it is a known quantity rather than an assumption: **12.23
ducats, 0.115%** of the 10,607.40 world wealth reading it from the save, or **9.40 ducats, 0.089%**
reading only the authored 16. Either way it moves **4 of 159 edges** of the installed graph and leaves
the sink set `{genua, hangzhou}` unchanged. *(An earlier draft of this paragraph said admitting it
moves no edge. That was measured at α_Φ = 1.5 and does not hold at 2.0.)*
```

### 216. `R2` - §1.3

R2: the table lead-in states why four of five are applied

**Removed:**

```
static modifiers describe a province's own state, all five are defined in
`common/static_modifiers/00_static_modifiers.txt`, and **four of the five are applied by the
reference implementation** — see the note below the table on `unrest`:
```

**Replaced with:**

```
static modifiers describe a province's own state, all five are defined in
`common/static_modifiers/00_static_modifiers.txt`, and **four of the five are applied** — `unrest` is
excluded because revolt risk depends on the owner, which the note below the table sets out:
```

### 217. `S1` - §1.6

S1: 1.6 stops claiming per-good order-invariance

**Removed:**

```
**What is conditional on the node order.** Nothing that this document quotes. Over the 180
relabellings above, the sink set, every edge direction, the promotion and fallback counts and the
per-good figures were identical, so the distinction v6.0 drew between world-properties and
ordering-artifacts has collapsed into the first category. The emitter should still fix one canonical
order — the guarantee is measured over the orderings tried, not proved — and §2.4 item 1 records
that as an implementation requirement rather than a correctness worry.
```

**Replaced with:**

```
**What is conditional on the node order.** Nothing this section quotes about the **installed** graph.
Over the 180 relabellings above the sink set, every edge direction, and the promotion and fallback
counts were identical, so for `Φ_w` the distinction v6.0 drew between world-properties and
ordering-artifacts has collapsed into the first category.

**The per-good graphs are a different matter.** The tie-break cost is read from node wealth, which is
good-independent, but a wealth-weighted cost need not separate the optima of a per-good LP, whose `b`
is a different vector. Measured across 29 goods × 10 relabellings, **84 of 290** runs moved a per-good
edge — a mean of 0.99 and up to 15 (§2.4 item 1). So the per-good figures in this section are quoted
at fixed node order, and the emitter must fix one canonical order and keep it: not for the installed
map any more, but for the value weights and the §1.10 survival table that hang off the per-good
solves. The `Φ_w` guarantee is also measured over the orderings tried rather than proved.
```

### 218. `T1` - §1.6

T1: what per-good order-sensitivity reaches, stated correctly

**Removed:**

```
is a different vector. Measured across 29 goods × 10 relabellings, **84 of 290** runs moved a per-good
edge — a mean of 0.99 and up to 15 (§2.4 item 1). So the per-good figures in this section are quoted
at fixed node order, and the emitter must fix one canonical order and keep it: not for the installed
map any more, but for the value weights and the §1.10 survival table that hang off the per-good
solves. The `Φ_w` guarantee is also measured over the orderings tried rather than proved.
```

**Replaced with:**

```
is a different vector. Measured across 29 goods × 10 relabellings, **84 of 290** runs moved a per-good
edge — a mean of 0.99 and up to 15 (§2.4 item 1). So the per-good figures in this section are quoted
at fixed node order, and the emitter must fix one canonical order and keep it. **That requirement is
not weaker than it was in v6.0, only relocated:** §2.2 propagates the per-good economy and writes it
back, so a per-good arrow that moves with the node numbering moves node values, the ledger and the
economy tab with it. The value weights are the exception — `V_g` is `price(g)` times a sum over
producers, with no direction in it, so they are order-independent by construction. The `Φ_w`
guarantee is measured over the orderings tried rather than proved.
```

### 219. `T2` - §2.2

T2: 2.2's MP note, with the right downstream

**Removed:**

```
question applies to it. And the per-good graphs are untouched — their optima are still degenerate
(§2.4 item 1), so vertex selection remains an exposure there, and the value weights and survival table
are downstream of it.
```

**Replaced with:**

```
question applies to it. And the per-good graphs are untouched — their optima are still degenerate
(§2.4 item 1), so vertex selection remains an exposure there, and the whole propagated per-good
economy is downstream of it: node values, the ledger and the economy tab all read numbers that a
different optimal vertex would change. The value weights are not — `V_g` is a producer sum with no
direction in it.
```

### 220. `T3` - §2.4

T3: 2.4 item 1's downstream, same correction

**Removed:**

```
   orientation, a mean of 0.99 edges and up to 15. So the installed aggregate graph is invariant over
   the orderings tried, while the per-good graphs — which set value weights and the §1.10 survival
   table — are not.
```

**Replaced with:**

```
   orientation, a mean of 0.99 edges and up to 15. So the installed aggregate graph is invariant over
   the orderings tried and the per-good graphs are not — and since §2.2 propagates the per-good
   economy and writes it back, that is what keeps a canonical order a correctness requirement rather
   than a convention. *A second wealth term (`+ TIE_EPS² · |w[u] − w[v]|`) was tried and rejected: it
   makes all 159 arc costs distinct where the shipped cost leaves 3 pairs equal, and still leaves 72 of
   232 per-good supports moving, down from 93. Distinct arc costs are not the issue — equal **totals**
   over different routings are, and ruling those out needs a generic perturbation, which is arbitrary
   by construction and so trades one arbitrariness for another.*
```

### 221. `U1` - §2.3

U1: which solves use the tie-break cost

**Removed:**

```
Only DRAIN's Phase 2 uses this cost. The per-good flow operators in `flowop.py` and the checks in
`verify.py` keep unit arc costs, and `mincost_flow`'s cost argument defaults to unit for that reason.
```

**Replaced with:**

```
**Every DRAIN solve uses this cost, per good as well as aggregate** — Phase 2 is Phase 2 — and since
`w` is node wealth the same cost vector serves all of them. What keeps unit arc costs is the separate
comparison operators: the FLOW and TREE operators in `flowop.py` (§3.15's bake-off) and the per-good
checks in `verify.py`. `mincost_flow`'s cost argument defaults to unit so those are unaffected.

**A single cost vector does not make every solve unique, and §2.4 item 1 measures where it does not.**
Uniqueness of an LP optimum depends on the right-hand side as well as the objective: `b_w` has no zero
entries and its optimum is unique under this cost, while each `b_g` puts a different face of the
polytope in play and 84 of 290 per-good relabellings still move an edge. Adding a second wealth term
does not close it — see item 1 — because the obstruction is different routings with equal **totals**,
not individual arcs with equal costs.
```

### 222. `V1` - §2.8

V1: 2.8's per-good sink range and decile rates

**Removed:**

```
| Most goods, 1444 | Sinks are `{selected ∩ flow-terminal} ∪ promoted` (§1.1) — 1 to 8 per good; high-demand nodes are sinks at 16.8% in the top demand decile vs 6.9% in the bottom (a barbell: LP branch ends land in poor pockets) |
```

**Replaced with:**

```
| Most goods, 1444 | Sinks are `{selected ∩ flow-terminal} ∪ promoted` (§1.1) — 2 to 8 per good; high-demand nodes are sinks at **19.8%** among each good's top eight demanders (46 of 232) against **6.9%** among its bottom eight (16 of 232), a barbell whose lower arm is LP branch ends landing in poor pockets. *The statistic is per-good deciles of nodes pooled over the 29 goods, not deciles of the pooled (good, node) pairs; the two constructions differ and only this one gives these figures.* |
```

### 223. `W1` - §3.3

W1: disambiguate the per-good alpha from alpha_Phi

**Removed:**

```
k-province node by `k^(α−1)` at fixed per-province wealth, so at α = 1.5 a 77-province node is
favoured over a 19-province one by `(77/19)^0.5 ≈ 2×` purely on slicing, and Nippon (68 land
provinces) over the Paris node (`champagne`, 33) by `(68/33)^0.5 ≈ 1.44×`.
```

**Replaced with:**

```
k-province node by `k^(α−1)` at fixed per-province wealth. Worked at **α(g) = 1.5** — a per-good α,
sugar's and coffee's at base price 3.0, not `α_Φ` — a 77-province node is
favoured over a 19-province one by `(77/19)^0.5 ≈ 2×` purely on slicing, and Nippon (68 land
provinces) over the Paris node (`champagne`, 33) by `(68/33)^0.5 ≈ 1.44×`. At the installed
`α_Φ = 2.0` the exponent is 1 and the same two comparisons give `77/19 ≈ 4.1×` and `68/33 ≈ 2.1×`,
so the slicing distortion the per-province form avoids is larger on the aggregate graph than on any
per-good one.
```

### 224. `X1` - §3.9

X1: one disclaimer, and a live antecedent

**Removed:**

```
  artifacts of sweep scheduling rather than places — and the sharpest evidence for that is what
  relabelling does to them: its end count and end set both move with the node order, where `Φ_w`'s do
  not (§2.4 item 1 measures the installed graph as invariant over the orderings tried). No figure is
  given for `Φ_ord`'s spread, because the operator is not installed and R3 forbids maintaining one.
  Most of those ends terminate no good,
  none of the demand capitals is among them, and the end count does not concentrate as demand
  concentrates. *No figure is maintained for it here.* It is not the installed operator, its numbers
  moved with every change to the wealth field, and three successive audits spent their effort
  recounting them; the design argument above does not depend on any of them.
```

**Replaced with:**

```
  artifacts of sweep scheduling rather than places — and the sharpest evidence for that is what
  relabelling does to them: its end count and end set both move with the node order, where `Φ_w`'s do
  not (§2.4 item 1 measures the installed graph as invariant over the orderings tried). Most of
  `Φ_ord`'s ends terminate no good, none of the demand capitals is among them, and the end count does
  not concentrate as demand concentrates. *No figure is quoted for any of that here*: the operator is
  not installed, its numbers moved with every change to the wealth field, three successive audits
  spent their effort recounting them, and the design argument above depends on none of them.
```

### 225. `Y1` - §1.6

Y1: 1.6's connectivity and self-coherence

**Removed:**

```
**90.5%** of ordered node pairs (5,721 of 6,320) connected by at least one good's directed path.

Agreement with the per-good graphs is **55.2%** of edge-goods (**55.0%** value-weighted). The
```

**Replaced with:**

```
**90.6%** of ordered node pairs (5,723 of 6,320) connected by at least one good's directed path.

Agreement with the per-good graphs is **55.1%** of edge-goods (**54.8%** value-weighted). The
```

### 226. `Y2` - §3.13

Y2: 3.13's self-coherence baseline

**Removed:**

```
  baseline is known — `Φ_w` agrees with the per-good graphs on **55.0%** of edge-goods *weighted by
  trade value*, and on 55.2% unweighted (§1.6) —
```

**Replaced with:**

```
  baseline is known — `Φ_w` agrees with the per-good graphs on **54.8%** of edge-goods *weighted by
  trade value*, and on 55.1% unweighted (§1.6) —
```

### 227. `Y3` - §3.8

Y3: 3.8's any-good connectivity

**Removed:**

```
measured, **90.5%** (5,721 of 6,320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. (v2 quoted 98.8%; that is v1's *Laplacian* figure, 6245/6320, carried across the operator change without being re-measured. The argument is unaffected — 90.5% is still most of the map — but the number was not v2's own.)
```

**Replaced with:**

```
measured, **90.6%** (5,723 of 6,320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. (v2 quoted 98.8%; that is v1's *Laplacian* figure, 6245/6320, carried across the operator change without being re-measured. The argument is unaffected — 90.6% is still most of the map — but the number was not v2's own.)
```

### 228. `Y4` - §1.6

Y4: 1.6's per-good order-sensitivity, after the second term

**Removed:**

```
is a different vector. Measured across 29 goods × 10 relabellings, **84 of 290** runs moved a per-good
edge — a mean of 0.99 and up to 15 (§2.4 item 1). So the per-good figures in this section are quoted
at fixed node order, and the emitter must fix one canonical order and keep it. **That requirement is
not weaker than it was in v6.0, only relocated:** §2.2 propagates the per-good economy and writes it
back, so a per-good arrow that moves with the node numbering moves node values, the ledger and the
economy tab with it. The value weights are the exception — `V_g` is `price(g)` times a sum over
producers, with no direction in it, so they are order-independent by construction. The `Φ_w`
guarantee is measured over the orderings tried rather than proved.
```

**Replaced with:**

```
is a different vector. §2.3's **second-order** term addresses exactly that, and most of the way:
across 29 goods × 10 relabellings **13 of 290** runs move a per-good edge, down from 84 before it, and
the number of goods admitting an alternative optimum at all falls from **18 of 29 to 1**. So the
per-good figures in this section are still quoted at fixed node order, and the emitter must still fix
one canonical order and keep it — **the requirement is weaker than in v6.0 but not gone**: §2.2
propagates the per-good economy and writes it back, so a per-good arrow that moves with the node
numbering moves node values, the ledger and the economy tab with it. The value weights are the
exception — `V_g` is `price(g)` times a sum over producers, with no direction in it, so they are
order-independent by construction. Both guarantees here are measured over the orderings tried rather
than proved.
```

### 229. `Z1` - §1.1

Z1: 1.1's Phase 2 cost, with both terms

**Removed:**

```
every support edge by its net flow. Arc costs are `1 + TIE_EPS·(w[u] + w[v])/2` — near-unit, symmetric
in the arc, and read from node wealth (§2.3). They are not unit because with unit costs the optimum is
not unique and which one the solver returns depends on the order the nodes are presented in; the
near-unit perturbation leaves one optimum to return.
```

**Replaced with:**

```
every support edge by its net flow. Arc costs are near-unit, symmetric in the arc, and read from node
wealth: a first-order term `TIE_EPS·(w[u] + w[v])/2` that carries the design intent, plus a
second-order generic term that breaks the ties the first one leaves (§2.3). They are not unit because
with unit costs the optimum is not unique and which one the solver returns depends on the order the
nodes are presented in; the perturbation is what leaves one optimum to return.
```

### 230. `Z2` - §2.3

Z2: 2.3 states the second-order term and why it exists

**Removed:**

```
```
cost(u, v) = 1 + TIE_EPS · (w[u] + w[v]) / 2        w = node wealth, normalised to [0, 1]
```

Two properties are load-bearing and neither is a matter of taste.
```

**Replaced with:**

```
```
cost(u, v) = 1 + TIE_EPS · (w[u] + w[v]) / 2
               + TIE_EPS2 · frac( min(w[u],w[v]) · max(w[u],w[v]) · 7919 )

              w = node wealth, normalised to [0, 1];  TIE_EPS = 1e-3,  TIE_EPS2 = 1e-6
```

**The two terms do different jobs and only the first means anything.** The first-order term is the
design statement: rich corridors cost more, so flow arriving at a wealthy node finds it dear to
continue and tends to terminate — wealth as destination rather than thoroughfare. The second-order
term is tie-breaking and nothing else; its form is arbitrary and no reading should be attached to it.

It exists because the first-order term is degenerate for some right-hand sides. Uniqueness of an LP
optimum depends on `b` as well as on the objective: a non-tree arc has zero reduced cost exactly when
its own cost equals the sum of costs along the tree path between its endpoints, and a different `b`
builds a different tree and exposes different coincidences. Measured, on zero-reduced-cost arcs
outside the support: the aggregate `b_w` goes from **40 under unit costs to 0** under the first-order
term alone, while the 29 per-good `b_g` still carry **41 between them, on 18 of the 29 goods**. Adding
the second-order term takes that to **1 arc on 1 good**, and per-good relabelling sensitivity from
**84 of 290 runs to 13**.

*A structured second term does not do this.* `+ TIE_EPS²·|w[u] − w[v]|` was tried and rejected: it
makes all 159 arc costs distinct where the shipped cost leaves 3 pairs equal, and still leaves 72 of
232 per-good supports moving. Distinct arc costs are not the obstruction — different routings with
equal **totals** are — so what is needed is genericity, not distinctness.

*What it costs:* self-coherence with the per-good graphs falls 0.1–0.2 points, and nothing else
measured moves. Sinks per good stay 2–8 mean 3.69, all 29 stay acyclic, `Φ_w`'s sinks are unchanged,
and the ±1% wealth-noise result stays 0 edges moved on six seeds. What it buys is replacing a tiebreak
that was arbitrary **and** order-dependent — the node index — with one that is arbitrary but
order-invariant.

Two properties are load-bearing and neither is a matter of taste.
```

### 231. `Z3` - §2.4

Z3: 2.4 item 1's per-good figures and the corrected note

**Removed:**

```
   vector. Measured across 29 goods × 10 relabellings: **84 of 290** runs changed a per-good
   orientation, a mean of 0.99 edges and up to 15. So the installed aggregate graph is invariant over
   the orderings tried and the per-good graphs are not — and since §2.2 propagates the per-good
   economy and writes it back, that is what keeps a canonical order a correctness requirement rather
   than a convention. *A second wealth term (`+ TIE_EPS² · |w[u] − w[v]|`) was tried and rejected: it
   makes all 159 arc costs distinct where the shipped cost leaves 3 pairs equal, and still leaves 72 of
   232 per-good supports moving, down from 93. Distinct arc costs are not the issue — equal **totals**
   over different routings are, and ruling those out needs a generic perturbation, which is arbitrary
   by construction and so trades one arbitrariness for another.*
```

**Replaced with:**

```
   vector. §2.3's second-order generic term closes most of that gap: per-good relabelling sensitivity
   falls from **84 of 290** runs to **13**, and the goods admitting any alternative optimum from **18
   of 29 to 1**. What remains is small but real, so the installed aggregate graph is invariant over the
   orderings tried and the per-good graphs are very nearly so — and since §2.2 propagates the per-good
   economy and writes it back, that residue is what keeps a canonical order a correctness requirement
   rather than a convention.
```

### 232. `AA1` - §2.8

AA1: 2.8's spice and cloves row, re-measured

**Removed:**

```
| Spice and cloves, 1444 | Source in Indonesia. Baseline DRAIN measured: spices sink at Genoa (demand rank 1) plus branch-end termini (Australia, Brazil); cloves at Venice, Kongo, Deccan, Australia, Brazil. **No Chinese node holds a spices sink in either configuration** — under the §3.13 α-calibration `spices` sinks at Genoa alone, and it is **cloves** that moves to Deccan. The v1 expectation of simultaneous China+Europe spice sinks is not the baseline behaviour and is not recovered by the calibration either. *(v2 said "China holds a spice sink only under the calibration", which its own parenthetical contradicted.)* |
```

**Replaced with:**

```
| Spice and cloves, 1444 | Source in Indonesia, and both source there alone: `spices` from `the_moluccas` and `kongo`, `cloves` from `the_moluccas` only. Baseline DRAIN measured: `spices` sinks at **Genoa and Brazil** — Genoa is that good's demand rank 1, Brazil its rank 73, which is the barbell in one row — and `cloves` at **Genoa, Kongo and Brazil** (demand ranks 2, 55 and 72). **No Chinese node holds a spices sink in either configuration** — under the §3.13 α-calibration `spices` sinks at Genoa alone, and it is **cloves** that moves to Deccan. The v1 expectation of simultaneous China+Europe spice sinks is not the baseline behaviour and is not recovered by the calibration either. *(v2 said "China holds a spice sink only under the calibration", which its own parenthetical contradicted. v6.0 listed Australia, Venice and Deccan among these termini; none of the three holds either sink on this field.)* |
```

### 233. `AB1` - §0

AB1: the front matter's account of v6.1

**Removed:**

```
**v6.1** changes two things, both in the operator rather than the field. **Phase 2's min-cost flow is
degenerate under unit arc costs, so presentation order selected which optimum was returned; §2.3 now
breaks that tie inside the objective, and §1.6 measures the installed orientation as unchanged across
every relabelling tried.** A canonical node order remains an emitter requirement — the per-good
graphs are still order-sensitive (§2.4 item 1) — but it is no longer what decides the installed map.
And **`α_Φ` moves from 1.5 to 2.0.** Both `α_Φ` and the new `TIE_EPS` are hyperparameters whose values
are developer taste; §2.3 states them and offers no justification for either, and every derivation
previously offered for `α_Φ` is withdrawn without replacement. The 1444 sink set moves from
`{english_channel, hangzhou}` to `{genua, hangzhou}` and 29 of the 59 figures `measure6.py` prints
move with it.
```

**Replaced with:**

```
**v6.1** changes two things, both in the operator rather than the field. **Phase 2's min-cost flow is
degenerate under unit arc costs, so presentation order selected which optimum was returned; §2.3 now
breaks that tie inside the objective, and §1.6 measures the installed orientation as unchanged across
every relabelling tried.** A canonical node order remains an emitter requirement — a residue of
per-good order-sensitivity survives (§2.4 item 1) — but it is no longer what decides the installed
map. And **`α_Φ` moves from 1.5 to 2.0.** `α_Φ` and the two new tie-break constants `TIE_EPS` and
`TIE_EPS2` are hyperparameters whose values are developer taste; §2.3 states them and offers no
justification for any of them, and every derivation previously offered for `α_Φ` is withdrawn without
replacement. The 1444 sink set moves from `{english_channel, hangzhou}` to `{genua, hangzhou}` and 29
of the 59 figures `measure6.py` prints move with it.
```

### 234. `AB2` - §2.3

AB2: 2.3's constants list carries both tie-break terms

**Removed:**

```
the aggregate-graph exponent `α_Φ = 2.0`, the Phase-2 tie-break strength `TIE_EPS = 1e-3`, and
DRAIN's three knobs at their defaults — demand-mass
```

**Replaced with:**

```
the aggregate-graph exponent `α_Φ = 2.0`, the Phase-2 tie-break strengths `TIE_EPS = 1e-3` and
`TIE_EPS2 = 1e-6`, and
DRAIN's three knobs at their defaults — demand-mass
```

### 235. `AB3` - §2.3

AB3: 2.3's hyperparameter statement covers all three

**Removed:**

```
**`α_Φ` and `TIE_EPS` are hyperparameters. Their values are developer taste, and this document
offers no justification for either.** Every derivation previously offered for `α_Φ` is withdrawn and
```

**Replaced with:**

```
**`α_Φ`, `TIE_EPS` and `TIE_EPS2` are hyperparameters. Their values are developer taste, and this
document offers no justification for any of them.** Every derivation previously offered for `α_Φ` is withdrawn and
```

### 236. `AC1` - §2.3

AC1: the normalisation is load-bearing per good

**Removed:**

```
relabelling by construction. The normalisation is not load-bearing: dividing by the maximum, the mean
or the world total gives the same orientation, because rescaling `w` is equivalent to rescaling
`TIE_EPS` and the answer is constant over about six orders of magnitude of it (§1.6).
```

**Replaced with:**

```
relabelling by construction.

**The normalisation is load-bearing per good, and this is a cost of the second-order term.** For the
first-order term alone it was not: rescaling `w` is exactly equivalent to rescaling `TIE_EPS`, and the
answer is constant over about six orders of magnitude of that (§1.6), so dividing by the maximum, the
mean or the world total gave the same orientation. `frac(lo·hi·7919)` is not linear in `w`, so that
argument no longer applies. Measured across the three normalisations: the aggregate `Φ_w` is unchanged
— **0 of 159 edges differ** — but **5 of the 29 per-good graphs do**. So the choice of normalisation is
a third arbitrary decision with an observable consequence, where before it was free. It is recorded
here rather than defended: min-max is what the implementation uses, and an implementer changing it
should expect a handful of per-good graphs to move.
```

### 237. `AD1` - §2.3

AD1: 2.3's paragraph now describes the term it has

**Removed:**

```
**A single cost vector does not make every solve unique, and §2.4 item 1 measures where it does not.**
Uniqueness of an LP optimum depends on the right-hand side as well as the objective: `b_w` has no zero
entries and its optimum is unique under this cost, while each `b_g` puts a different face of the
polytope in play and 84 of 290 per-good relabellings still move an edge. Adding a second wealth term
does not close it — see item 1 — because the obstruction is different routings with equal **totals**,
not individual arcs with equal costs.
```

**Replaced with:**

```
**A single cost vector does not make every solve unique, and §2.4 item 1 measures what is left.**
Uniqueness of an LP optimum depends on the right-hand side as well as the objective: `b_w` has no zero
entries and its optimum is unique under the first-order term alone, while each `b_g` puts a different
face of the polytope in play and 18 of the 29 admitted an alternative optimum before the second-order
term. With it, that falls to 1 good and per-good relabelling sensitivity to 13 of 290 runs. The
residue is not zero and the document does not claim it is.
```

### 238. `AD2` - §1.6

AD2: 1.6's hyperparameter statement covers all three

**Removed:**

```
**`α_Φ = 2.0` and `TIE_EPS = 1e-3` are hyperparameters. The choice is developer taste, and this
document offers no justification for either beyond that.**
```

**Replaced with:**

```
**`α_Φ = 2.0`, `TIE_EPS = 1e-3` and `TIE_EPS2 = 1e-6` are hyperparameters. The choice is developer
taste, and this document offers no justification for any of them beyond that.**
```

### 239. `AD4` - §1.1

AD4: 1.1's cost range includes the second term

**Removed:**

```
  `Σ (flow × cost)` with `cost ∈ [1, 1 + TIE_EPS]`, so the optimum minimises a hop count in which a
  hop between two wealthy nodes counts marginally more (§2.3). At `TIE_EPS = 1e-3` the spread is under
```

**Replaced with:**

```
  `Σ (flow × cost)` with `cost ∈ [1, 1 + TIE_EPS + TIE_EPS2]`, so the optimum minimises a hop count in
  which a hop between two wealthy nodes counts marginally more (§2.3). At those values the spread is under
```

### 240. `AE1` - §1.6

AE1: 1.6 records the second term's range as well

**Removed:**

```
the solver's tolerance and stops registering, and above it the term exceeds the base arc cost of 1
and stops being a perturbation. `scripts/epsilon6.py` reports the bands and bisects their edges.
```

**Replaced with:**

```
the solver's tolerance and stops registering, and above it the term exceeds the base arc cost of 1
and stops being a perturbation. `scripts/epsilon6.py` reports the bands and bisects their edges.
`TIE_EPS2` behaves the same way and was measured at 1e-7, 1e-6 and 1e-5, all three leaving the same
single good with an alternative optimum — so it too is a switch rather than a dial, and its exact
value carries no more meaning than its form does (§2.3).
```

### 241. `AF1` - §2.3

AF1: three constants, not two

**Removed:**

```
v5.0 said it sat in the widest sink-count band. Both are withdrawn. Changing either value is a design
decision, and §1.6 records how the field responds around them so that the decision can be made with
the sensitivity in view — that is documentation for whoever changes them, not an argument for the
current values.

`TIE_EPS` sets the Phase-2 objective. With unit arc costs the min-cost b-flow is degenerate, so the
orientation depends on node numbering; the tie-break puts the choice in the objective instead:
```

**Replaced with:**

```
v5.0 said it sat in the widest sink-count band. Both are withdrawn. Changing any of the three is a
design decision, and §1.6 records how the field responds around them so that the decision can be made
with the sensitivity in view — that is documentation for whoever changes them, not an argument for the
current values.

`TIE_EPS` and `TIE_EPS2` together set the Phase-2 objective. With unit arc costs the min-cost b-flow
is degenerate, so the orientation depends on node numbering; the tie-break puts the choice in the
objective instead:
```

### 242. `AF2` - §2.3

AF2: drop the paragraph that restates figures given above

**Removed:**

```
**A single cost vector does not make every solve unique, and §2.4 item 1 measures what is left.**
Uniqueness of an LP optimum depends on the right-hand side as well as the objective: `b_w` has no zero
entries and its optimum is unique under the first-order term alone, while each `b_g` puts a different
face of the polytope in play and 18 of the 29 admitted an alternative optimum before the second-order
term. With it, that falls to 1 good and per-good relabelling sensitivity to 13 of 290 runs. The
residue is not zero and the document does not claim it is.

**DLC state is a third input axis.**
```

**Replaced with:**

```
**DLC state is a third input axis.**
```

### 243. `AG1` - §1.6

AG1: attribute the two noise samples

**Removed:**

```
largest `|b_w|` **0.0347**; the sink set is unchanged under ±1% wealth noise on three seeds. Its
```

**Replaced with:**

```
largest `|b_w|` **0.0347**; the sink set is unchanged under ±1% wealth noise on the three seeds
`measure6.py` runs, and on a six-seed run no edge moved at all (§3.6). Its
```

### 244. `AH1` - §2.4

AH1: point at the current figure, not the intermediate one

**Removed:**

```
   `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`. That script measures the unit-cost objective,
   so its figure describes the former solver and is superseded by the 84-of-290 above rather than
   contradicted by it.)*
```

**Replaced with:**

```
   `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`. That script measures the unit-cost objective,
   so its figure describes the former solver and is superseded by the 13-of-290 above rather than
   contradicted by it.)*
```

### 245. `AI1` - §1.6

AI1: 1.6's per-good order-sensitivity is now zero

**Removed:**

```
is a different vector. §2.3's **second-order** term addresses exactly that, and most of the way:
across 29 goods × 10 relabellings **13 of 290** runs move a per-good edge, down from 84 before it, and
the number of goods admitting an alternative optimum at all falls from **18 of 29 to 1**. So the
per-good figures in this section are still quoted at fixed node order, and the emitter must still fix
one canonical order and keep it — **the requirement is weaker than in v6.0 but not gone**: §2.2
propagates the per-good economy and writes it back, so a per-good arrow that moves with the node
numbering moves node values, the ledger and the economy tab with it. The value weights are the
exception — `V_g` is `price(g)` times a sum over producers, with no direction in it, so they are
order-independent by construction. Both guarantees here are measured over the orderings tried rather
than proved.
```

**Replaced with:**

```
is a different vector. Two changes closed that gap. §2.3's **second-order** term took per-good
relabelling sensitivity from **84 of 290** runs to 13 and the goods admitting an alternative optimum
from 18 of 29 to 1; **pinning the solver's optimality tolerance (§2.3) took the remainder to 0 of
290.** So on this field the per-good graphs are order-invariant over the orderings tried, as `Φ_w` is.

The emitter should still fix one canonical order, because both guarantees are measured rather than
proved and §2.2 propagates the per-good economy and writes it back — a per-good arrow that moved with
the node numbering would move node values, the ledger and the economy tab with it. The value weights
never could: `V_g` is `price(g)` times a sum over producers, with no direction in it.
```

### 246. `AI2` - §2.3

AI2: 2.3 records the tolerance as a correctness requirement

**Removed:**

```
*What it costs:* self-coherence with the per-good graphs falls 0.1–0.2 points, and nothing else
measured moves.
```

**Replaced with:**

```
**The solver's optimality tolerance is a correctness requirement, not a performance knob.** HiGHS
stops when reduced costs are within its dual feasibility tolerance of zero, and that default is
**1e-7** — while the margin by which the tie-break makes the optimum unique runs as low as **3.8e-8**
on some per-good solves. The margin sits *inside* the default tolerance, so the solver was free to
stop either side of the true optimum. Measured: over six permutations of the LP's column order,
`copper` and `paper` returned orientations differing on 12 and 8 edge-slots, with objectives differing
by **7.7e-10 relative** — six orders above float noise, so those were unequal-quality answers rather
than tied optima. Setting both feasibility tolerances to **1e-10** (HiGHS's floor for them) takes the
flips to **0** and the objective spread to **1.1e-15**. `flowop.LP_OPTS` carries it, and no figure in
this document moved when it went in — the shipped column order was already reaching the true optimum;
what changed is that every other order now does too.

*What the second-order term costs:* self-coherence with the per-good graphs falls 0.1–0.2 points, and
nothing else measured moves.
```

### 247. `AI3` - §2.4

AI3: 2.4 item 1's per-good residue is gone

**Removed:**

```
   vector. §2.3's second-order generic term closes most of that gap: per-good relabelling sensitivity
   falls from **84 of 290** runs to **13**, and the goods admitting any alternative optimum from **18
   of 29 to 1**. What remains is small but real, so the installed aggregate graph is invariant over the
   orderings tried and the per-good graphs are very nearly so — and since §2.2 propagates the per-good
   economy and writes it back, that residue is what keeps a canonical order a correctness requirement
   rather than a convention.
```

**Replaced with:**

```
   vector. §2.3's second-order generic term took per-good relabelling sensitivity from **84 of 290**
   runs to **13**, and pinning the solver's optimality tolerance took it to **0 of 290**. So both the
   installed graph and the per-good graphs are order-invariant over the orderings tried. A canonical
   order remains an emitter requirement because that is a measurement and not a proof, and because
   §2.2 propagates the per-good economy and writes it back — but it is no longer the difference
   between a correct map and an arbitrary one.
```

### 248. `AJ1` - §2.2

AJ1: the multiplayer position, restated against what is now measured

**Removed:**

```
§2.3's tie-break narrows one part of this and leaves the rest. On the aggregate graph the optimum is
unique, so *which vertex of a degenerate optimal face the solver lands on* is no longer a desync path
— that was the largest single exposure and it is closed. What remains is ordinary float
reproducibility: the cost vector itself is computed from wealth, so the same accumulation-order
question applies to it. And the per-good graphs are untouched — their optima are still degenerate
(§2.4 item 1), so vertex selection remains an exposure there, and the whole propagated per-good
economy is downstream of it: node values, the ledger and the economy tab all read numbers that a
different optimal vertex would change. The value weights are not — `V_g` is a producer sum with no
direction in it.
```

**Replaced with:**

```
**§2.3's two changes move this from a design problem to a verification one.** The largest exposure was
*which vertex of a degenerate optimal face the solver lands on*, which is genuinely machine-dependent.
The tie-break makes the optimum unique, and pinning the solver's optimality tolerance makes the solver
actually reach it. What is measured on this field:

| | |
|---|---|
| randomness in the solve | none. Identical output fingerprint over repeated runs, separate processes, and five `PYTHONHASHSEED` values including `random` — so there is no seed to pin and no set-iteration order to depend on |
| margin by which the optimum is unique | **3.8e-8** worst per good, **7.5e-6** on the aggregate — 8 to 10 orders above double-precision unit roundoff |
| orientation under LP column permutation | **0** flips, aggregate and all 29 goods; objective spread 1.1e-15 |
| orientation under node relabelling | **0** of 180 aggregate, **0** of 290 per-good (§2.4 item 1) |
| free-versus-flow classification margin | the per-good `\|net\|` distribution is bimodal — 2,321 edge-goods at exactly 0 and 2,290 above 1e-6, with **nothing between** — so the absolute `1e-11` threshold sits in an empty band six orders wide and last-bit noise cannot reclassify an edge |

So a few units in the last place cannot change any decision this solver makes. **What remains is not
bit-reproducibility of a simplex, which would be a hard guarantee to earn, but three checks:**

1. **One binary per platform, and no cross-platform sessions.** A single compiled instruction stream
   gives identical IEEE-754 results on any x86-64 host. The `../v2-drain/` DLL precedent is already
   Windows- and Steam-only, so this matches practice rather than constraining it.
2. **No runtime CPU dispatch in the LP solver, and single-threaded.** This is the live risk: numeric
   libraries commonly select an AVX2 or SSE2 path at runtime *from the same binary*, and a threaded
   reduction has no fixed accumulation order. Both must be pinned in the solver build and verified,
   not assumed.
3. **§2.8's cross-implementation orientation check.** It compares the DLL against the reference
   implementation exactly, and it cannot run until the DLL exists. It is the test that would catch a
   divergence the three points above missed.

*What the engine itself does about the same problem is worth knowing and is only half-answered.* Every
trade number EU4 writes to a save is quantised to **1/1000** — 495 of 495 sampled values land exactly
on that grid across `total`, `val`, `p_pow`, `retention`, `collector_power` and `max_pow`. Quantisation
of that kind erases any divergence below half a grid step, which is the standard cheap defence. What
the files cannot settle is whether the rounding happens in the simulation or only in the serialiser;
that needs a memory read and is added to §2.7. It would not rescue this solver either way: the
orientation margins above are 3.8e-8 to 7.5e-6, three to five orders *below* a 1e-3 grid, so
quantising the model's own inputs to match would erase the tie-break rather than protect it.

**Until points 1–3 are done, ship single-player only.** The reason has changed, though, and the change
is the point: it is no longer "vertex selection is machine-dependent" but "the build discipline is
unverified and the DLL that would prove it does not exist yet."
```

### 249. `AK1` - §2.7

AK1: the quantisation probe 2.2 refers to

**Removed:**

```
11. **Caravan recipient.**
```

**Replaced with:**

```
11. **Is EU4's 1/1000 quantisation in the simulation or the serialiser?** Every trade number the
    engine writes to a save sits exactly on a 1/1000 grid (495 of 495 sampled). If the rounding is in
    the simulation, the engine erases sub-milli-ducat divergence every tick, which is how it survives
    lockstep multiplayer; if it is only in the save writer, it says nothing about determinism. Read a
    node's live trade value from memory at higher precision than the save shows and compare. This
    settles what §2.2 can claim about the engine's own defence, and whether the mod should adopt the
    same discipline at its write boundary.
12. **Caravan recipient.**
```

### 250. `AL1` - §2.7

AL1: restore the caravan probe to item 11

**Removed:**

```
11. **Is EU4's 1/1000 quantisation in the simulation or the serialiser?** Every trade number the
    engine writes to a save sits exactly on a 1/1000 grid (495 of 495 sampled). If the rounding is in
    the simulation, the engine erases sub-milli-ducat divergence every tick, which is how it survives
    lockstep multiplayer; if it is only in the save writer, it says nothing about determinism. Read a
    node's live trade value from memory at higher precision than the save shows and compare. This
    settles what §2.2 can claim about the engine's own defence, and whether the mod should adopt the
    same discipline at its write boundary.
12. **Caravan recipient.**
```

**Replaced with:**

```
11. **Caravan recipient.**
```

### 251. `AL2` - §2.7

AL2: add the quantisation probe as item 16, after the existing set

**Removed:**

```
All writes land atomically at the tick hook with the sim paused.
```

**Replaced with:**

```
16. **Is EU4's 1/1000 quantisation in the simulation or the serialiser?** Every trade number the
    engine writes to a save sits exactly on a 1/1000 grid — 495 of 495 sampled values, across
    `total`, `val`, `p_pow`, `retention`, `collector_power` and `max_pow`. If the rounding happens in
    the simulation then the engine erases sub-milli-ducat divergence every tick, which is a plausible
    part of how it survives lockstep multiplayer; if it happens only in the save writer it says
    nothing about determinism. Read a node's live trade value from memory at higher precision than the
    save shows and compare. This settles what §2.2 may claim about the engine's own defence, and
    whether the mod should round at its own write boundary. *It does not bear on the solver's
    determinism either way: §2.2's orientation margins are 3.8e-8 to 7.5e-6, three to five orders
    below a 1e-3 grid, so quantising the model's inputs to match would erase the §2.3 tie-break rather
    than protect it.*

All writes land atomically at the tick hook with the sim paused.
```

### 252. `AM1` - §2.8

AM1: join a table cell that wrapped across two lines and broke the row

**Removed:**

```
the exception — `zambezi` —
drifting 0.012%).
```

**Replaced with:**

```
the exception — `zambezi` — drifting 0.012%).
```

### 253. `AN1` - §0

AN1: what v6.1 changes, with the residue gone

**Removed:**

```
**v6.1** changes two things, both in the operator rather than the field. **Phase 2's min-cost flow is
degenerate under unit arc costs, so presentation order selected which optimum was returned; §2.3 now
breaks that tie inside the objective, and §1.6 measures the installed orientation as unchanged across
every relabelling tried.** A canonical node order remains an emitter requirement — a residue of
per-good order-sensitivity survives (§2.4 item 1) — but it is no longer what decides the installed
map. And **`α_Φ` moves from 1.5 to 2.0.** `α_Φ` and the two new tie-break constants `TIE_EPS` and
`TIE_EPS2` are hyperparameters whose values are developer taste; §2.3 states them and offers no
justification for any of them, and every derivation previously offered for `α_Φ` is withdrawn without
replacement. The 1444 sink set moves from `{english_channel, hangzhou}` to `{genua, hangzhou}` and 29
of the 59 figures `measure6.py` prints move with it.
```

**Replaced with:**

```
**v6.1** changes the operator, not the field. **Phase 2's min-cost flow is degenerate under unit arc
costs, so presentation order selected which optimum was returned.** §2.3 now breaks that tie inside
the objective, in two terms — one carrying the design intent, one generic — and **pins the solver's
optimality tolerance, which turned out to be a correctness requirement rather than a performance
knob**: the margin by which the tie-break makes the optimum unique is as small as 3.8e-8, and HiGHS's
default tolerance is 1e-7, so the solver could stop either side of it. With all three in place the
orientation is unchanged across every relabelling tried — **0 of 180 on the aggregate and 0 of 290 per
good** — and unchanged under permutation of the LP's column order. A canonical node order remains an
emitter requirement because that is a measurement rather than a proof, but it is no longer what
decides the map.

And **`α_Φ` moves from 1.5 to 2.0.** `α_Φ`, `TIE_EPS` and `TIE_EPS2` are hyperparameters whose values
are developer taste; §2.3 states them and offers no justification for any of them, and every
derivation previously offered for `α_Φ` is withdrawn without replacement. The 1444 sink set moves from
`{english_channel, hangzhou}` to `{genua, hangzhou}` and 29 of the 59 figures `measure6.py` prints
move with it. §2.2 records what multiplayer would additionally need, which is now build discipline
rather than a design change.
```

### 254. `AN2` - §0

AN2: the coverage paragraph, deduplicated

**Removed:**

```
**`verify6.py` checks figures in this document against values computed from the install, and it
covers well under half of what the document prints.** No count is given here: some of its checks are
generated per matching phrase, so the total moves whenever the prose does. The harness prints its own
count when it runs, and that is where to read it. No ratio is offered, because the denominator is not well defined — counting "the figures the
spec prints" gives anywhere from 279 to 326 depending on how a numeric token is delimited, so any
proportion built on it says more about the tokeniser than about the harness. `scripts/coverage6.py`
reports what is guarded among the figures it can locate unambiguously, and it should be re-run rather
than quoted. Some figures carry a script attribution instead of a guard, and a few carry neither. `scripts/coverage6.py` measures that honestly — it corrupts each spec-printed figure whether
the harness looks at it or not — and it should be re-run rather than quoted here, because the number
moves with every edit to the document.
```

**Replaced with:**

```
**`verify6.py` checks figures in this document against values computed from the install, and it
covers well under half of what the document prints.** Neither a count nor a ratio is given here, for
two different reasons. The count moves whenever the prose does, because some checks are generated per
matching phrase — the harness prints its own count when it runs, and that is where to read it. The
ratio has no well-defined denominator: counting "the figures the spec prints" gives anywhere from 279
to 326 depending on how a numeric token is delimited, so any proportion built on it says more about
the tokeniser than about the harness. `scripts/coverage6.py` is the honest measure — it corrupts each
spec-printed figure whether the harness looks at it or not — and it should be re-run rather than
quoted, because its number also moves with every edit. Some figures carry a script attribution
instead of a guard, and a few carry neither.
```

### 255. `AO1` - §1.1

AO1: the key-collision measurement, at its real scope

**Removed:**

```
  no exact ties. Measured: zero orientation changes under scheduler permutations, and zero exact
  `(DEF, b)` ties on free edges, 29/29 goods.
```

**Replaced with:**

```
  no exact ties. Measured: zero orientation changes under scheduler permutations, and zero exact
  `(DEF, b)` key collisions across **all 2,320 core nodes** of the 29 per-good solves — not merely on
  the free edges, which is where earlier versions measured it. Phase 1's within-cluster argmin and its
  top-k cluster cut are untied on the same field, so no index tiebreak in the algorithm fires at all.
```

### 256. `AO2` - §1.1

AO2: Phase 2 names both solver requirements

**Removed:**

```
and return a support with an undirected cycle in it. §2.2 therefore requires network simplex or a
simplex LP.
```

**Replaced with:**

```
and return a support with an undirected cycle in it. §2.2 therefore requires network simplex or a
simplex LP, and §2.3 additionally requires the solver's optimality tolerance to be tighter than the
margin the tie-break provides — both are correctness requirements on the solver rather than settings.
```

### 257. `AP1` - §2.2

AP1: the MP opening, consistent with what follows it

**Removed:**

```
**Multiplayer is unsupported by default.** An identical build is necessary and not sufficient: EU4 multiplayer is lockstep with checksums, and an in-process floating-point solve can produce different results on different hardware — differing SIMD dispatch or accumulation order in the linear algebra is enough to desync. Supporting MP requires the computation to be bit-reproducible across machines. For DRAIN the
exposure is narrower than v1's dense linear algebra but still real: the min-cost-flow solve must
return the same optimum given identical input (fixed arc ordering, one solver build, no threading),
and the sweep is deterministic given the LP's support and a fixed accumulation order — its comparisons
are of input-derived floats (`DEF`, `b`), not of solver residuals, which is the distinction that
matters against v1's dense algebra, but it is not integer arithmetic and v2 called it that. Its
cross-machine reproducibility reduces to the LP's.
```

**Replaced with:**

```
**Multiplayer is not supported yet, and the reason is narrower than it was.** EU4 multiplayer is
lockstep with checksums, so every client must reach the same answer. The classical worry is that an
in-process floating-point solve gives different results on different hardware — differing SIMD
dispatch, accumulation order, or library build. That worry is real in general, and v1's dense linear
algebra was badly exposed to it: comparisons of solved potentials that were mathematically equal and
differed only in their residual (§3.6).

DRAIN's exposure is different in kind. Its comparisons are of input-derived quantities (`DEF`, `b`,
arc costs), not of solver residuals — and, more importantly, every decision it makes now has a margin
far above float noise. What that means in practice is set out below; the short form is that the
question is no longer whether the arithmetic agrees to the last bit, but whether the build is
disciplined enough that the same instruction stream runs everywhere.
```

### 258. `AP2` - §2.2

AP2: point 3 refers to itself as one of 'the three above'

**Removed:**

```
3. **§2.8's cross-implementation orientation check.** It compares the DLL against the reference
   implementation exactly, and it cannot run until the DLL exists. It is the test that would catch a
   divergence the three points above missed.
```

**Replaced with:**

```
3. **§2.8's cross-implementation orientation check.** It compares the DLL against the reference
   implementation exactly, and it cannot run until the DLL exists. It is the test that would catch a
   divergence the first two points missed.
```

### 259. `AQ1` - §2.8

AQ1: the determinism row, at its measured scope

**Removed:**

```
| Determinism | Re-running a tick reproduces the orientation bit-for-bit; promotions and fallbacks are scheduler-invariant (monotone closure) |
```

**Replaced with:**

```
| Determinism | Re-running a tick reproduces the orientation bit-for-bit; promotions and fallbacks are scheduler-invariant (monotone closure). Measured on the reference implementation: one fingerprint over `Φ_w` and all 29 per-good graphs — including sinks, sources, promotions and fallbacks — was identical across repeated runs, separate processes, and five `PYTHONHASHSEED` values including `random`. The solve carries no randomness, so there is no seed to pin |
| Solver optimality tolerance | Assert the LP is configured tighter than the tie-break margin — `flowop.LP_OPTS` sets both feasibility tolerances to 1e-10 against a worst-case margin of 3.8e-8 (§2.3). **This can regress silently on a solver upgrade:** at HiGHS's 1e-7 default the margin sits inside the tolerance and the solver may return a suboptimal vertex, which is what made two goods order-dependent before it was pinned. Assert the option is set and that the returned objective's reduced costs clear the tolerance |
```

### 260. `AR1` - §3.6

AR1: 3.6's degeneracy premise, after the tolerance was pinned

**Removed:**

```
corridors — the map from `b` to the chosen support is discontinuous in principle. §2.3's tie-break
narrows where that bites: on the aggregate graph it leaves the optimum unique, so the result no longer
rests on the solver's tie-selection; on the per-good graphs, whose `b` a wealth-weighted cost need not
separate, it still does (§2.4 item 1), and that is the premise §3.13 tracks for multiplayer.
```

**Replaced with:**

```
corridors — the map from `b` to the chosen support is discontinuous in principle. §2.3's tie-break
removes where that bites in practice: with both cost terms and the solver's optimality tolerance
pinned, the optimum is unique on the aggregate and on all 29 per-good solves, with a margin of 3.8e-8
at worst against double-precision noise of 2e-16 — so the result no longer rests on the solver's
tie-selection at all. The discontinuity remains a property of the *program*: an input that made two
routings exactly equal in cost would still have no unique answer. Nothing on this field does.
```

### 261. `AR2` - §3.6

AR2: 3.6's forward reference to the MP question

**Removed:**

```
replaces the ε-magnitude question in §3.13 is the cross-machine question: the LP must pivot
identically on identical input for multiplayer (§2.1).
```

**Replaced with:**

```
replaces the ε-magnitude question in §3.13 is the cross-machine question — and §2.2 narrows it: the LP
does not need to *pivot* identically, only to reach the same optimum, which the tie-break's margin
makes robust to a few units in the last place. What is left is build discipline (§2.2).
```

### 262. `AR3` - §3.13

AR3: 3.13's open question, restated to what is open

**Removed:**

```
- LP determinism across machines: the min-cost-flow solve must pivot identically on identical
  input (replaces v1's ε-magnitude question; see §2.1 and §3.6).
```

**Replaced with:**

```
- **Multiplayer build discipline.** Not LP pivot determinism, which §2.2 retires: the optimum is
  unique with a margin 8 to 10 orders above float noise, so a few units in the last place cannot
  change it. What is open is whether the shipped solver build does runtime CPU dispatch or threads its
  reductions — either would break bit-identity across hosts running the same binary — and whether the
  DLL reproduces the reference implementation's orientation exactly (§2.8), which cannot be tested
  until the DLL exists. Replaces v1's ε-magnitude question; see §2.2 and §3.6.
```

### 263. `AS1` - §0

AS1: 0's pointer to the multiplayer discussion

**Removed:**

```
move with it. §2.2 records what multiplayer would additionally need, which is now build discipline
rather than a design change.
```

**Replaced with:**

```
move with it. §2.1 records what multiplayer would additionally need, which is now build discipline
rather than a design change.
```

### 264. `AS2` - §2.7

AS2: 2.7's probe pointer

**Removed:**

```
    determinism either way: §2.2's orientation margins are 3.8e-8 to 7.5e-6, three to five orders
```

**Replaced with:**

```
    determinism either way: §2.1's orientation margins are 3.8e-8 to 7.5e-6, three to five orders
```

### 265. `AS3` - §3.6

AS3: 3.6's pointer

**Removed:**

```
makes robust to a few units in the last place. What is left is build discipline (§2.2).
```

**Replaced with:**

```
makes robust to a few units in the last place. What is left is build discipline (§2.1).
```

### 266. `AS4` - §3.13

AS4: 3.13's pointer

**Removed:**

```
- **Multiplayer build discipline.** Not LP pivot determinism, which §2.2 retires: the optimum is
  unique with a margin 8 to 10 orders above float noise, so a few units in the last place cannot
  change it. What is open is whether the shipped solver build does runtime CPU dispatch or threads its
  reductions — either would break bit-identity across hosts running the same binary — and whether the
  DLL reproduces the reference implementation's orientation exactly (§2.8), which cannot be tested
  until the DLL exists. Replaces v1's ε-magnitude question; see §2.2 and §3.6.
```

**Replaced with:**

```
- **Multiplayer build discipline.** Not LP pivot determinism, which §2.1 retires: the optimum is
  unique with a margin 8 to 10 orders above float noise, so a few units in the last place cannot
  change it. What is open is whether the shipped solver build does runtime CPU dispatch or threads its
  reductions — either would break bit-identity across hosts running the same binary — and whether the
  DLL reproduces the reference implementation's orientation exactly (§2.8), which cannot be tested
  until the DLL exists. Replaces v1's ε-magnitude question; see §2.1 and §3.6.
```

### 267. `AT1` - §0

AT1: the header's connected-maps pointer

**Removed:**

```
**Target:** EU4 1.37.5 Inca. Extended-timeline compatible. **Connected maps only** — see §2.2.
```

**Replaced with:**

```
**Target:** EU4 1.37.5 Inca. Extended-timeline compatible. **Connected maps only** — see §2.2a.
```

### 268. `AT2` - §1.1

AT2: 1.1's reachability bullet points at the connectedness premise

**Removed:**

```
infeasible outright. §2.2 states the connectedness requirement and what the solver does when it
  is violated.
```

**Replaced with:**

```
infeasible outright. §2.2a states the connectedness requirement and what the solver does when it
  is violated.
```

### 269. `AT3` - §1.6

AT3: 1.6's pointer to where the per-good economy is propagated

**Removed:**

```
proved and §2.2 propagates the per-good economy and writes it back — a per-good arrow that moved with
```

**Replaced with:**

```
proved and §2.1 propagates the per-good economy and writes it back — a per-good arrow that moved with
```

### 270. `AT4` - §2.4

AT4: 2.4's same pointer

**Removed:**

```
   §2.2 propagates the per-good economy and writes it back — but it is no longer the difference
```

**Replaced with:**

```
   §2.1 propagates the per-good economy and writes it back — but it is no longer the difference
```

### 271. `AT5` - §2.7

AT5: 2.7's probe pointer to the multiplayer discussion

**Removed:**

```
    save shows and compare. This settles what §2.2 may claim about the engine's own defence, and
```

**Replaced with:**

```
    save shows and compare. This settles what §2.1 may claim about the engine's own defence, and
```

### 272. `AT6` - §3.6

AT6: 3.6's pointer to the multiplayer discussion

**Removed:**

```
replaces the ε-magnitude question in §3.13 is the cross-machine question — and §2.2 narrows it: the LP
```

**Replaced with:**

```
replaces the ε-magnitude question in §3.13 is the cross-machine question — and §2.1 narrows it: the LP
```

### 273. `AU1` - §2.3

AU1: source the solver tolerance claim and confirm its mechanism

**Removed:**

```
**The solver's optimality tolerance is a correctness requirement, not a performance knob.** HiGHS
stops when reduced costs are within its dual feasibility tolerance of zero, and that default is
**1e-7** — while the margin by which the tie-break makes the optimum unique runs as low as **3.8e-8**
on some per-good solves. The margin sits *inside* the default tolerance, so the solver was free to
stop either side of the true optimum. Measured: over six permutations of the LP's column order,
`copper` and `paper` returned orientations differing on 12 and 8 edge-slots, with objectives differing
by **7.7e-10 relative** — six orders above float noise, so those were unequal-quality answers rather
than tied optima. Setting both feasibility tolerances to **1e-10** (HiGHS's floor for them) takes the
flips to **0** and the objective spread to **1.1e-15**. `flowop.LP_OPTS` carries it, and no figure in
this document moved when it went in — the shipped column order was already reaching the true optimum;
what changed is that every other order now does too.
```

**Replaced with:**

```
**The solver's optimality tolerance is a correctness requirement, not a performance knob.** HiGHS
stops when reduced costs are within its dual feasibility tolerance of zero, and **`scipy.optimize.linprog`'s
`method="highs"` options document that default as `1e-07`** for both the dual and primal tolerances
(scipy 1.18.0) — while the margin by which the tie-break makes the optimum unique runs as low as
**3.8e-8** on some per-good solves. The margin sits *inside* the default tolerance, so the solver was
free to stop either side of the true optimum. Measured: over six permutations of the LP's column order,
`copper` and `paper` returned orientations differing on 12 and 8 edge-slots, with objectives differing
by **7.7e-10 relative** — six orders above float noise, so those were unequal-quality answers rather
than tied optima.

*The mechanism is confirmed rather than inferred, by bisecting the tolerance against `copper`.* Leaving
it unset and setting it to 1e-7 give the same 8 flips over four permutations, which is what pins the
effective default independently of the documentation; **1e-8 already gives 0**, and 1e-8 is the first
value below `copper`'s 3.765e-8 margin. So the flips appear exactly when the tolerance exceeds the
margin, which is the claim. `flowop.LP_OPTS` ships **1e-10** — HiGHS's floor for these options, taken
for headroom rather than necessity — and the objective spread there is 1.1e-15. No figure in this
document moved when it went in: the shipped column order was already reaching the true optimum, and
what changed is that every other order now does too.
```

### 274. `AV1` - §0

AV1: 0 stops asserting the proportion it then declines to give

**Removed:**

```
**`verify6.py` checks figures in this document against values computed from the install, and it
covers well under half of what the document prints.** Neither a count nor a ratio is given here, for
two different reasons. The count moves whenever the prose does, because some checks are generated per
matching phrase — the harness prints its own count when it runs, and that is where to read it. The
ratio has no well-defined denominator: counting "the figures the spec prints" gives anywhere from 279
to 326 depending on how a numeric token is delimited, so any proportion built on it says more about
the tokeniser than about the harness.
```

**Replaced with:**

```
**`verify6.py` checks figures in this document against values computed from the install, and its
coverage is partial.** Neither a count nor a proportion is given here, for two different reasons, and
"partial" is as far as this paragraph will go. The count moves whenever the prose does, because some
checks are generated per matching phrase — the harness prints its own count when it runs, and that is
where to read it. A proportion has no well-defined denominator: counting "the figures the spec prints"
gives anywhere from 279 to 326 depending on how a numeric token is delimited, so any fraction built on
it says more about the tokeniser than about the harness. *An earlier draft of this paragraph asserted
"well under half" two sentences before refusing to give a ratio; the refusal is the part that survives.*
```
