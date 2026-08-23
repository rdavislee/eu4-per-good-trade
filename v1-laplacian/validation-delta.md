# Validation delta — consequences of the sink diagnosis

# BRANCH: C — structural property of the model

**With D as a bounded secondary effect. A and B are ruled out.**

The solver was correct. The model produced this result. Per the branch rules:

- `per-good-trade-spec.md` has **not** been edited.
- `validation.md` has **not** been rewritten, and **no status in it has been changed**.
- Nothing was tuned. The solver was not "fixed", because nothing in it is broken.

The evidence is in `diagnosis.md`. In one line: sinks are decided by
`(c−s)/deg > mean(neighbour φ) − min(neighbour φ)` — exact on 2320/2320 (good, node) pairs — and
because supply contrast (2.5×10⁷) exceeds demand contrast (~10²–10³) by four to five orders of
magnitude, the right-hand term is set by supply geometry. Demand only picks among the nodes the
geometry has already flattened.

**Why this is not partly A/B.** The two implementation hypotheses were tested directly and both
failed: the balance residual is 1.110e-16 before any correction is applied (A), and the solver
reproduces per-province `Σ_p wealth^α` to 3.123e-17 while differing from the node-level form by
9.733e-03 (B). There is no implementation component to this finding to keep separate.

**What D contributes, kept separate.** Correcting the wealth inputs for autonomy would plausibly
raise c(genua) by the 1.72× needed to make Genoa a **co-sink** with Saxony. It would not displace
Saxony (needs ≈4×, i.e. 22.5% of world spice demand at one node) and could not put a spice sink
in China (needs 3.6–4.8×, i.e. 9.5–21.4% at one node). So better inputs change the sink *set* at
the margin and change nothing about what *determines* it. **This is not a reason to defer the C
finding, and it is not a reason to rerun anything yet.**

---

## 1. Claims whose status should change

These are reported, not applied. `validation.md` is untouched.

| ID | § | Current | Should become | Why |
|---|---|---|---|---|
| **C295** | §2.8 | DEFERRED | **REFUTED** | "Spice and cloves sink in both China and Europe" — the China half is structurally unreachable, not merely unobserved. `canton` needs 17.6% and `hangzhou` 21.4% of all world spice demand in one node; both are adjacent to the Indonesian sources and carry headroom 0.0392 and 0.0431. The Europe half is reachable (Genoa at 1.72×). |
| **C296** | §2.8 | DEFERRED | **REFUTED** | "Most goods have their largest sinks in India and China" — sinks are local minima, not ranked magnitudes, so "largest sink" has no referent in this model; and the Chinese and Indian nodes nearest the sources are the *least* able to be sinks. Measured sink frequency is `safi` 12, `gulf_of_siam` 11, `saxony` 7. |
| **C297** | §2.8 | OUT_OF_SCOPE | **blast radius only** | Still a preference, so still not truth-apt — but it blesses a behaviour the model does not produce. Its premise C296 is refuted, so the sentence defends nothing. |
| **C310** | §2.8 | DEFERRED | DEFERRED, contrary | "1650 Caribbean sugar income makes it a sink for cloth, tools, wine" — `carribean_trade` has degree 8. No node of degree ≥ 6 is a sink for any good on the 1444 data. Compounding the C037/C038 autonomy error already recorded against this row. |
| **C311** | §2.8 | DEFERRED | DEFERRED, contrary | "Kilwa's ivory income makes it a sink for Indian textiles" — same mechanism; a production-income spike raises `c` but `c` is not what selects sinks. |
| **C384** | §3.2 | DEFERRED | **CONFIRMED, with a redefinition** | "Goods flow to a periphery and are consumed at the end of the line" — true, and now mechanised. But "periphery" means **graph** periphery (low neighbour-φ spread), not economic periphery. The spec's surrounding prose reads as though the two coincide. They do not. |
| **C011** | §1.1 | DEFERRED | **CONFIRMED** | "Sinks differ from good to good" — 36 distinct sink nodes across 29 goods, no node a sink for all. Now settled directly. |
| **C312** | §2.8 | CONFIRMED | CONFIRMED, sharpened | The claim is right *because it says leaf*: a degree-1 node has headroom identically 0, so any net consumption makes it a sink. It is the one place the spec states the converse of C382 correctly. Vacuous on the vanilla map — minimum degree is 2. |
| **C442** | §3.5 | CONFIRMED | CONFIRMED, strengthened | Now quantified: sinks move onto rich nodes only at α ≥ 4, which needs k = 5.13, which puts cloves at α = 1.2×10³. Price would not merely fight geography; it would obliterate the regime split. |
| **C439** | §3.5 | OUT_OF_SCOPE | **blast radius only** | "α is deliberately mild" is presented as a design taste. The measurement shows it is a binding constraint: there is no α that both fixes the sink placement and preserves §1.4. |

## 2. The two load-bearing passages named in the brief

### §3.2 — "Peripheral sinks are intended, not a defect" (C383, C380, C381, C382)

**Status: C383 stays OUT_OF_SCOPE (it is a preference). But it is now load-bearing in a way the
spec does not acknowledge, and one inference in the passage is invalid.**

The passage runs:

> Sinks are net consumers automatically: a DAG-sink is a local minimum of `φ`, and by the
> discrete maximum principle local minima occur only where `c > s`. Peripheral sinks are
> intended — goods flow to a periphery and are consumed at the end of the line.

Every individual claim here is confirmed. C380, C381 and C382 all hold, and C382 was verified
exhaustively (0 violations over 2320 pairs; and separately, 102 of 102 sink pairs have `c > s`).

**The invalid step is the implicature.** C382 gives a *necessary* condition — sink ⇒ `c > s`. The
passage is written so that a reader takes it as sufficient, and concludes that high-demand nodes
become sinks. They do not. The sufficient condition is the criterion in `diagnosis.md` §4, and it
contains a second term the spec never mentions anywhere: the local spread of φ. On the 1444 data
**64 of 80 nodes satisfy `c > s` for spices, and exactly one is a sink.** Across all 29 live
goods, **1816 (good, node) pairs satisfy `c > s` and 102 are sinks — the necessary condition
admits 1816 candidates and selects 5.6% of them.** `c > s` holds for 80% of the map and
discriminates almost nothing.

This is why the anomaly went unnoticed for the length of the spec: **nothing in §1 or §3 states
what determines sink location.** The spec states what a sink *is* (C010, no outgoing links), and
a necessary condition for one (C382), and never closes the gap. `claims.md` faithfully records
that gap — there is no claim to refute, because the proposition was never asserted.

Recommended, not applied: add the sufficient condition to §3.2 as a derived claim, and correct
"peripheral" to say graph-peripheral explicitly. The word currently does the work of an argument.

### §3.15 — the rejection of edge conductance / a weighted Laplacian (C665, C666, C667)

**Status: C667 stays CONFIRMED. C665 and C666 stay OUT_OF_SCOPE as choices — but the choice is
now known to be the direct cause of the anomaly, which the rejection does not price in.**

> **Edge conductance / weighted Laplacian.** Too much mechanical surface; the unweighted solve
> routes correctly through conduits.

C667 is true and was verified: the unweighted solve does route through conduits — the synthetic
path test gives interior nodes exactly the mean of their neighbours, and `cape_of_good_hope`, the
one real pure conduit on the map at 1444, sits mid-field at φ = +0.0618 with zero demand.

But the rejection's stated cost is "mechanical surface", and its **actual** cost is the finding in
`diagnosis.md`. With every edge at conductance 1, the headroom term is a function of topology
alone: it depends only on how many neighbours a node has and how far it sits from the supply
spikes. Nothing economic can enter it. That is precisely why a node with the highest demand in
the game and a node with zero demand can both fail to be sinks while a mid-ranked German node
succeeds.

So §3.15's rejection is not wrong — it is a legitimate choice — but it is currently justified
against the wrong consideration. It should record that the unweighted Laplacian is what makes
sink location topological, and accept or revisit that consequence explicitly.

## 3. Goal-level consequences

Two of §3.1's seven goals are affected, and one is affected badly.

- **Goal 3 (C358, C359) — "preserve the feedback loop in which sinks accumulate value, fund
  development, and reinforce themselves. This is how mercantile hegemonies form."**
  This is the serious one. Sinks collect 100% of a good's value (C086, C098). If sink location is
  set by graph flatness rather than by wealth, the feedback loop accrues value to
  graph-peripheral nodes — `saxony`, `safi`, `african_great_lakes`, `patagonia`, `white_sea` — and
  reinforces them. The loop still closes, but it closes on the wrong nodes, and it would build
  hegemonies in inland Germany and Morocco rather than in Italy or the Channel. Goal 3 as written
  is not delivered by the current operator. **This is the finding with the largest design
  consequence in this document, and it is not fixable by better wealth inputs (§D bound).**
- **Goal 5 (C363) — "direction must reflect where a good can ultimately reach, not which
  neighbour is richer."** Delivered, and *over*-delivered. Direction now reflects reachability
  almost exclusively: CF1 shows the field is 94.6% rank-preserved when demand variation is
  deleted entirely. Goal 5 and Goal 3 are in direct tension, and the spec does not note it.
- **Goal 2 (C355) — "commodities should flow differently from one another."** Delivered (36
  distinct sink nodes) but for a graph reason, not an economic one: goods differ because their
  *supply* geographies differ, not because demand differs. Consistent with §3.4's thesis (C419,
  "where a good comes from is what makes its trade its own"), which this result strongly
  vindicates — arguably more strongly than intended.
- **C356/C357 — "China is a silk source and a spice sink at once."** C357 (a single graph cannot
  represent both) stays CONFIRMED. But the specific example fails: no Chinese node can be a spice
  sink at any plausible demand. The motivating illustration of Goal 2 is not reproduced by the
  model built to serve it.

## 4. Options to put sinks at demand rather than at graph distance

Options with costs. Not a recommendation, and nothing here has been implemented.

Two of the six are already **ruled out by measurement** in this diagnosis; four are untested.

| Option | Mechanism | Cost | Status |
|---|---|---|---|
| **1. Weighted Laplacian / edge conductance** | Weight each edge by an economic capacity so headroom stops being purely topological. | Reverses §3.15 (C665, C666). Weights must come from a non-circular quantity — `goods_produced` or `wealth`, **not** realized flow, or it reintroduces exactly the demand→orientation→flow→demand loop §3.3 excludes trade income to avoid (C403, C628). Adds one authored choice of weighting function, in tension with Goal 6 (C364). | Untested |
| **2. Screened Poisson / mass term** | Solve `(L + κ·diag(c)) φ = s − c`. Demand becomes a local absorber, so a high-demand node can be a minimum on its own account rather than only by tilting its neighbourhood. | Breaks the §1.6 identity `Φ ≡ φ₀` (C063, C321, C462), which needs a κ-free operator linear in the RHS — that identity is the spec's only end-to-end correctness check. Adds constant κ, taking §2.3's design constants from two to three (C221). | Untested |
| **3. Dirichlet anchor** | Pin `φ = 0` at the highest-demand node instead of solving pure-Neumann, or add an absorbing boundary there. | Makes the sink a choice rather than an outcome — direct violation of Goal 1 (C353) and Goal 6 (C364). Cheapest to implement, most damaging to the design's premise. | Untested |
| **4. Raise α** | Increase demand contrast until it competes with supply contrast. | **Measured and ruled out.** Works at α ≥ 4 (Beijing) and α ≥ 6 (Genoa), but α is price-derived, so α(spices) = 8 requires k = 5.13, which puts cloves at α = 1.2×10³ and grain at 3.14. `α_max` clamps everything and §1.4's three-regime split collapses. Realises C442 exactly. | **Ruled out** |
| **5. Degree-normalise demand** | Solve `L φ = D(s − c)` to remove the `1/deg` division on the drive term. | **Measured and ruled out.** Sinks unchanged (`['saxony']`). The drive term is not what decides; headroom is. | **Ruled out** |
| **6. Reduce supply contrast** | Change §1.2 so `s` is less spiky (e.g. a concave transform of `goods_produced`). | Breaks §1.6's identity in the supply term specifically — `φ₀`'s supply is defined as the node share of world *trade value* (C064, C065), and C424/C643 show substituting anything else destroys the identity (residual 1.5e+00 and 2.5e+01 respectively, orientation agreement falling from 159/159 to 68/159 and 58/159). Also contradicts §3.4's thesis that supply geography is what differentiates goods (C419, C440). | Untested |
| **7. Accept and restate** | Keep the operator; rewrite the goals and expectations it actually satisfies. | §3.1 Goal 3 must be withdrawn or rewritten (C358, C359); §2.8's "sinks in India and China" and "Caribbean/Kilwa" rows must be replaced; §3.2 must state the sufficient condition and say graph-peripheral. Zero implementation cost, and it is the only option that costs no correctness. | Untested |

Note on options 1 and 6: both attack the headroom term, which is the term the measurements say
actually decides. Options 3 and 4 attack the drive term or bypass the operator, and option 4 is
already measured as ineffective at any usable parameter. If the goal is to make demand matter,
the evidence points at the headroom term, i.e. at options 1, 2 and 6 — but that is a statement
about where the lever is, not a recommendation to pull it.

## 5. What was not done, and why

- **No status in `validation.md` was edited.** Branch C forbids it, and the §1 table above is a
  report.
- **`per-good-trade-spec.md` untouched**, as in the previous session.
- **No rerun of the reference solver's validation pass.** Under branch C there is nothing to
  rerun: the solver produced correct output from correct inputs, and the MODEL claims that cite
  it — C063, C321, C382, C462, C521, C522, C527, C594, C595 — are all unaffected, because every
  one of them is a statement about the operator's algebra rather than about where sinks land.
  Their evidence stands verbatim.
- **Wealth inputs not improved.** The D bound says the improvement is worth making for its own
  sake — it would plausibly add Genoa to the spice sink set and it is needed anyway for C037's
  autonomy correction — but it will not change this diagnosis, so it is not a prerequisite for
  acting on it.
