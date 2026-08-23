# DRAIN: peel / cluster-select / b-flow / gated drainage sweep — tested against the Laplacian

**Verdict: the strongest candidate of the four tested, and the first to tie the Laplacian on every
structural requirement.** It orients all 159 edges (repairing FLOW's 49.7% coverage), is acyclic by
construction on every good, reaches 100.0% of demand on all 29 goods with 0 orphan sinks, keeps
1–8 sinks per good, and — the flagship result — **makes Genoa, the highest-demand node in the game,
the principal spices sink**, which `diagnosis.md` proved the Laplacian structurally cannot do.

It does not dominate. It loses narrowly on aggregate sink–demand correlation (+0.053 vs LAP's
+0.104, because the LP's branch-end termini drag in poor remote pockets), slightly on the shared
unserved metric (0.1206 vs 0.1037), and — like every non-solve operator — it has no §1.6
`Φ ≡ φ₀` identity. Whether it beats the incumbent is now a genuine judgement call, not a
measurement; the previous three candidates lost outright.

Nothing tuned. `per-good-trade-spec.md` and `validation.md` untouched. 1444.11.11 data, 29 live
goods, 80 nodes, 159 links, α(g) = (price/2)¹. Code: `scratchpad/v/drain.py`, `drainrep.py`.
A re-verification of all four earlier documents accompanies this report (appendix).

---

## 0. Implementation notes, and one harness bug disclosed

- **My first run had a sign bug** — I passed the balances to the LP with supply and demand
  swapped, which made the world's sole cloves *source* come out as its sink. Caught in the smoke
  test (cloves flow now runs `the_moluccas → malacca` at 0.8416, correct) before any results were
  recorded. Disclosed because the previous session's errors were of exactly this class.
- **The stall lemma held empirically.** The spec's Phase 3 lemma ("the unmarked set contains a
  flow-terminal demander") is not proven for a gate-true node with β = 0; I added a documented
  fallback for that case. **It never fired** — 0 uses across 29 goods, all promotions were genuine
  flow-terminal demanders. The lemma is validated on this data.
- **Input-domain violation, again benign:** the spec requires b(v) ≠ 0; `cape_of_good_hope` has
  b = 0 exactly for all 29 goods. It stays in the core, is never a Phase-1 candidate, and ends a
  conduit for all 29 goods.
- Phase 1's optional dilation and the un-peel phase are implemented; both are inert here (below).

## 1. Phase-by-phase findings on this graph

**Phase 0 is a no-op.** Minimum degree 2, zero bridges (the graph is 2-edge-connected), so the
2-core is the whole graph, there are no pendants, and the un-peel phase orients nothing. Same
finding as for BASIN.

**Phase 1's adaptive k is nearly inert — demand is too connected for cluster granularity.**
`H[Dset]` is one giant connected component for 19 of 29 goods, because nearly every node is a net
demander of nearly every good and demanders are adjacent. Result: **k = 1 for 27 of 29 goods**
(HHI ≥ 0.87); only `livestock` (8 clusters, HHI 0.64) and `salt` (7 clusters, HHI 0.53) get k = 2.
Dilation makes it *more* inert: at r = 2 livestock's clusters merge and k returns to 1. The
"effective number of demand clusters" premise assumes demand pockets separated by non-demand
territory; EU4's demand is ubiquitous, so the pockets don't exist.

**Selection ≠ sinkhood.** Of 31 nodes selected across all goods, only **13 became final sinks**.
The heaviest demander in a cluster is usually a *transit* node — `hangzhou` is selected for cloves
(demand rank 1) but carries through-flow toward Nippon and Beijing, so the gate marks it late and
it keeps its out-arcs. Selection lands a sink only when the chosen node is also flow-terminal
(`genua` for spices).

**Stall promotion is the real engine, exactly as the spec's guarantee 5 anticipates.** FLOW's
optimum has 26–39 flow-terminal drains per good; the drainage sweep's third ready-clause rescues
most of them (a free edge to an earlier-marked node becomes an out-arc), and the stalls promote
the remainder: **1–8 promotions per good, mean 2.9**. The final sink set is
{selected ∩ flow-terminal} ∪ {promoted}, sized 1–8, mean **3.6** — the same scale as LAP's 3.5,
against FLOW's unusable 32.1.

## 2. Guarantees, verified

| guarantee | claim | measured |
|---|---|---|
| 1 Feasibility | orientation carries a flow serving all demand | reach **100.0%, 29/29 goods, 0 orphan sinks of 104** |
| 2 Efficiency | fewest-hop routing | inherited from the unit-cost LP (theorem; LP deterministic — 6 identical solves, 1 orientation) |
| 3 Global DAG | reversed marking order is a topological order | `has_cycle` = none, 29/29 goods; aggregate options below |
| 4 Drainage | every node's out-arcs lead to a sink | **80/80 nodes, 29/29 goods** |
| 5 Adaptive sinks | k tracks concentration; self-corrects upward | k inert (see §1); the upward self-correction carries the whole mechanism and works |

## 3. Results against the incumbent

### Sink placement

```
         sinks/g  mean rank  P(top10)  P(bot10)  rho_val
LAP          3.5       29.4      9.0%      0.7%   +0.104
DRAIN        3.6       34.8     14.1%      6.9%   +0.053
(RANK +0.281 / BASIN +0.225 / FLOW −0.132 for reference)
```

**A barbell.** DRAIN places top-decile sinks more often than LAP (14.1% vs 9.0%) — and that is the
half that matters for §3.1 Goal 3 — but it also places 6.9% of bottom-decile nodes as sinks
(LAP: 0.7%), because the LP's dead-end branches must terminate somewhere and their ends are
Australia, Brazil, Kongo, La Plata. The Spearman nets out below LAP's.

The named nodes:

```
spices  DRAIN sinks: genua(rank 1), australia(65), brazil(73)        LAP: saxony(22)
cloves  DRAIN sinks: venice(7), kongo(55), australia(63), brazil(71) LAP: safi(40)
```

**Genoa — demand rank 1 — is the spices sink, and it is reachable** (it receives the
Alexandria-side flow; the LP serves every demander by construction). Venice (rank 7) is the
premier cloves sink. Saxony is not a sink for anything named. This is the outcome three previous
candidates chased: RANK achieved it and stranded a sixth of world demand; BASIN achieved it for
selection but not delivery; DRAIN achieves it with delivery intact.

### The corridor and the Cape

```
spices  cape in=1 out=3, conduit ✓   malacca -> cape ✓ (flow arc, 0.243 of world supply)
                                     cape -> genua: cape -> zanzibar -> gulf_of_aden -> alexandria -> genua
cloves  cape in=1 out=3, conduit ✓   the_moluccas -> malacca -> cape ✓ (0.448 of world supply)
                                     cape -> genua: cape -> ivory_coast -> sevilla -> valencia -> genua
```

Conduit for 29/29 goods, and both corridors exist as directed paths — including cloves, which
RANK and BASIN both severed. The Malacca→Cape artery is inherited from the LP (it is the corrected
finding of `flow-orientation.md`: the Cape route is the *short* way to Atlantic Europe).

### Everything else

```
edges oriented                 159/159, all goods           (FLOW: 79)
acyclic per good               29/29
aggregate (a) Σ V_g·net_g      cyclic — same failure as FLOW
aggregate (b) Σ V_g·order_g    ACYCLIC, orients 159/159, and agrees with its own
                               per-good graphs on 62.7% — better than LAP's own 52.6%
unserved (shared evaluator)    DRAIN 0.1206 | LAP 0.1037 | BASIN-best 0.2206
safi ↔ sevilla                 agrees with LAP on 27/29; the 5 goods where Safi "exports"
                               something it doesn't produce are the same 5 where LAP does it too
net-producer sinks             0 of 104   (LAP 0, RANK 9)
marking-order sensitivity      free edges move (15–31 of 159 across 3 scan permutations)
                               but the SINK SET is identical in every case, 3/3 goods tested
                               -> RESOLVED in section 6: flips are now 0 by construction
±1% wealth noise, 5 seeds      spices/cloves 0 flips; grain 1.0 flips, 1/5 sink-set changes
```

The aggregate finding deserves a line: the marking order is a genuine per-node scalar, so
`Φ_ord = Σ_g V_g·order_g` is a potential — acyclic for free — and it is **more coherent with its
per-good graphs (62.7%) than the spec's own Φ is with LAP's (52.6%)**. DRAIN has a *better* §1.6
replacement than FLOW's duals or BASIN's fields. What it cannot have is the `Φ ≡ φ₀` identity,
which requires a linear solve; that remains LAP's unique end-to-end check.

## 4. Scorecard, all five operators

| | LAP | FLOW | RANK | BASIN | **DRAIN** |
|---|---|---|---|---|---|
| edges oriented | 159 | **79** | 159 | 159 | 159 |
| acyclic per good | yes | yes | yes | yes | yes |
| acyclic aggregate | yes | **no** | yes | yes | yes (order-potential) |
| aggregate self-coherence | 52.6% | — | — | 29.0% | **62.7%** |
| demand reachable | 100% | 100% | **83.3%** | **88.5%** | 100% |
| orphan sinks | 0 | 0 | **34** | 3 | 0 |
| sinks per good | 1–7 | **26–39** | 11–17 | = S | 1–8 |
| ρ_val (sinks~demand) | +0.104 | −0.132 | **+0.281** | +0.225 | +0.053 |
| P(sink \| top decile) | 9.0% | 32.1%* | 46.6% | 19.7% | 14.1% |
| P(sink \| bottom decile) | **0.7%** | 52.1% | 1.0% | 0.0% | 6.9% |
| genua = spices sink | no | yes* | yes (orphan) | selected only | **yes, served** |
| net-producer sinks | 0 | 0 | 9 | 0 | 0 |
| unserved (shared eval) | **0.1037** | — | — | 0.2206 | 0.1206 |
| §1.6 identity | **exact** | no | no | no | no |

*FLOW's sink stats are inflated by its 32 sinks/good; not comparable at face value.*

**Bottom line.** DRAIN = FLOW's conservation-respecting routing + a drainage completion that fixes
both of FLOW's disqualifiers. It is the first candidate where choosing it over the Laplacian would
be a trade rather than a mistake: you give up the `Φ ≡ φ₀` identity, ~2 points of unserved, and
sink purity at the bottom decile; you gain Genoa-as-spice-sink (Goal 3's flagship case), a more
self-coherent aggregate, an explicit sink-count input, and the Cape artery. If the bottom-decile
termini are unacceptable, the surgical fix is in Phase 1/promotion policy (e.g. merge a promoted
terminal's demand into its nearest selected sink by reversing its starved branch), not in the flow
— but that is a design change beyond this test's scope, and nothing was tuned here.

---

## 5. Parameter exploration — sink-count disparity by price (requested follow-up)

**Ask:** make sink counts track the good's tier — cloves ≈ 1 sink, cheap bulk goods ≈ 5 — by
playing with the HHI-adaptive k, and with α unclamped and scaled. **Unlike everything above, this
section is deliberate tuning**: 36 configurations were run and one was chosen by looking at the
outcome. Every configuration was still held to the hard checks (acyclicity, 100% reach, orphans,
fallbacks), and none failed any of them.

### Levers tested (grid: 3 × 2 × 3 × 2 = 36 configs, all 29 goods each)

| lever | values | what it does |
|---|---|---|
| `k_exp` | 1, 2, 3 | α(g) = (price/2)^k_exp — demand contrast per price tier |
| clamp | on [0.2, 3.0] / **off** | spec §1.4's clamp; off lets cloves reach α = 16+ |
| `ρ` | 1.0 (as specified), 0.5 | Phase 1 clusters only the demanders covering the top-ρ of demand mass |
| `tol` | 1e-11 (as specified), 1e-4, 1e-3 | net flow below tol → edge is free, not a flow arc (twig pruning) |

### What actually moves the dial

1. **The HHI mechanism alone cannot do it.** At spec parameters the demand set is one connected
   blob (k = 1 for 27/29 goods, §1). The mass-quantile fix (ρ = 0.5) makes k genuinely adaptive —
   clusters 1–8, HHI 0.18–1.00, k spanning 1–5 across goods — but it changes final sink counts
   only marginally (spearman moves −0.488 → −0.494), because **selection still isn't sinkhood**:
   the sink count is set by the LP's terminal drains, not by S0.
2. **Unclamped α^k_exp is what differentiates the tiers.** At k_exp = 2 unclamped, cloves gets
   α = 16 (demand ∝ wealth¹⁶ — essentially only the richest courts), grain gets α = 1.56, and
   price-2.0 goods stay at exactly α = 1. At spec α (clamped, k_exp = 1) the price/sink-count
   correlation is **wrong-signed** (+0.06 to +0.11); unclamping and scaling flips it.
3. **Twig pruning (`tol`) converts the correlation from noise to signal.** The LP's thin branch
   ends are what promote poor pockets into sinks. At tol = 3e-4, edges carrying < 0.03% of world
   supply are left to the drainage sweep instead — on average only 5.8 of 79 flow arcs per good —
   and their pocket demanders get rescued (free edge out) rather than promoted. Correlation at
   fixed k_exp = 2: −0.07 (no pruning) → −0.49 (1e-4) → −0.53 (3e-4).

### Chosen configuration and result

**`k_exp = 2, α unclamped, ρ = 0.5, tol = 3e-4`** — span exactly **1..5**, mean 2.5,
**spearman(price, sink count) = −0.539**. The table below is under the deterministic sweep of §6
(regenerated after that change; 5 rows moved, span and pattern unchanged, correlation −0.526 →
−0.539). Verified: acyclic 29/29, reach 100.0% on 28 goods and 99.97% on silk (footnote), 0 orphan
sinks, 0 fallback promotions (42 stall promotions, all genuine flow-terminal demanders), and sink
sets unchanged under ±1% wealth noise (0/3 seeds × 3 goods, re-run under the deterministic sweep).

| price | good | sinks | sink nodes (demand rank under this config's α) |
|---|---|---|---|
| 8.0 | cloves | **1** | beijing(2) |
| 4.0 | cocoa | **1** | doab(3) |
| 4.0 | dyes | **1** | hangzhou(1) |
| 4.0 | ivory | **1** | genua(2) |
| 4.0 | gems | **1** | genua(2) |
| 4.0 | silk | 3 | hangzhou(1), champagne(7), timbuktu(21) |
| 3.5 | paper | 3 | beijing(12), timbuktu(23), kongo(55) |
| 3.0 | sugar | 1 | doab(6) |
| 3.0 | chinaware | 2 | genua(2), kongo(55) |
| 3.0 | cloth | 2 | gulf_of_siam(7), kongo(55) |
| 3.0 | coffee | 2 | champagne(4), australia(64) |
| 3.0 | copper | 2 | venice(10), mexico(15) |
| 3.0 | cotton | 2 | champagne(4), kongo(55) |
| 3.0 | spices | 2 | genua(2), doab(6) |
| 3.0 | tobacco | 2 | hangzhou(1), brazil(72) |
| 3.0 | glass | 5 | hangzhou(1), comorin_cape(18), safi(40), tunis(54), kongo(55) |
| 3.0 | iron | 4 | doab(6), gulf_of_siam(7), mexico(15), safi(40) |
| 3.0 | salt | 4 | genua(2), doab(6), nippon(8), timbuktu(28) |
| 2.5 | fish | 2 | champagne(4), deccan(17) |
| 2.5 | incense | 3 | champagne(4), timbuktu(26), kongo(53) |
| 2.5 | wool | 3 | hangzhou(3), mexico(9), white_sea(68) |
| 2.5 | grain | 3 | champagne(4), persia(19), zambezi(61) |
| 2.5 | wine | 4 | hangzhou(3), doab(12), timbuktu(26), kongo(53) |
| 2.0 | tea | 2 | genua(3), kongo(51) |
| 2.0 | slaves | 2 | gulf_of_siam(2), rheinland(8) |
| 2.0 | fur | 3 | gulf_of_siam(2), mexico(6), brazil(74) |
| 2.0 | tropical_wood | 3 | wien(14), zambezi(62), brazil(74) |
| 2.0 | livestock | 4 | gulf_of_siam(2), mexico(6), comorin_cape(10), african_great_lakes(63) |
| 2.0 | naval_supplies | **5** | mexico(6), rheinland(8), gujarat(26), burma(27), brazil(74) |

Every 4.0+ luxury has 1–3 sinks (five of six have exactly one; silk at 3 is the exception);
every bulk good at 2.0–2.5 has 2–5. Footnote on silk's reach: under the deterministic sweep, one
pruned-twig node (`ohio`, silk demand share 2.97e-4, just below the 3e-4 threshold) is unreachable —
99.97% of silk demand is served, and ohio is not a sink, so nothing strands there. Off-pattern rows exist and are honest: sugar (3.0) collapses to 1 sink because its demand
under α = 2.25 concentrates hard; tea (2.0) stays at 2 because its supply geography (10 sources)
gives the LP few terminal branches. Price explains about half the variance (ρ² ≈ 0.28); supply
geography explains the rest, which is consistent with §3.4's thesis that where a good comes from
is what makes its trade its own.

### Caveats, stated plainly

- **Unclamped α² is a demand-model change, not a solver knob.** α(cloves) = 16 means world cloves
  demand is effectively the single richest province (Beijing at 19.5 proxy wealth — hence Beijing,
  not Genoa, is the cloves sink here). Applied to the *Laplacian*, the same α would also move its
  sinks (`diagnosis.md` §6 measured LAP at α = 4 → beijing/rheinland). This lever belongs to
  §1.4, not to DRAIN, and adopting it means deciding that luxuries are court goods.
- **tol = 3e-4 discards the LP certificate on the pruned twigs.** Those pockets remain reachable
  (verified, 100.0%) but along drainage-oriented free edges rather than min-cost routes; guarantee
  2 (fewest-hop routing) now holds only for 99.97%+ of each good's mass.
- **Demand ranks in the table are under each good's own scaled α**, not under the spec's α; the
  two rankings differ most for the luxuries (Beijing is cloves rank 2 here, rank 12 under spec α).
- **Overfit risk.** One 1444 snapshot, 36 configs, chosen on the outcome. The noise test says the
  choice is not knife-edged, but nothing here was validated out-of-sample; a 1500s or 1600s
  dataset would be the honest test.

---

## 6. Deterministic free edges (requested follow-up)

**Problem.** A free edge is one the LP declined to use — a statement about optimal routing, not
about the endpoints being equivalent. Their orientation came from marking order, and order was
underdetermined whenever several nodes became ready simultaneously: the old sweep took whichever
the scan reached first. Measured cost of that arbitrariness: **767 and 501 edge-good orientations
flip** (out of 4,611) under two scan permutations. Sink sets never moved — only the free edges did.

**The fix adopted** (from a design discussion the user brought in): replace the scan with a
**priority ready-queue**, so `order` becomes a function of the graph and the balances rather than
of loop iteration. The candidate signals, in the proposed strength order: downstream unmet demand
(`def`), distance-to-sink (order itself), and local `s − c`. The circularity caution was honoured:
**DEF is computed on the flow-arc subgraph only**, which is acyclic and fully determined before any
free edge is touched.

**A structural fact worth recording first:** ready-marking is a monotone closure — marking a node
only ever enables more nodes — so the markable set before each stall, and therefore the stall
sequence, the promotions, and the fallbacks, are *provably* scan-invariant. Priority can only move
`order` values, never the sink-forcing events. Verified empirically: promotions identical 29/29
(untuned) and 42/42 with 0 fallbacks (tuned config).

**Three keys measured** (final tie-break = node index; "flips" = orientation changes when the index
key is permuted two ways, summed over 29 goods):

| key (among ready, pop first) | flips | sink sets vs old sweep | unserved proxy |
|---|---|---|---|
| old scan order | 767 / 501 | — | 0.1206 |
| (−DEF, β, id) — literal "toward want" | **0** | 28/29 (salt loses nippon) | 0.1415 |
| (−DEF, −\|β\|, id) — proposal as written | **0** | 28/29 | 0.1403 |
| **(+DEF, β, id) — adopted** | **0** | **29/29 identical** | **0.1252** |

**Exact key ties: 0** — for every free edge, on every good, the endpoints differ on (DEF, β). The
truly-symmetric residue predicted as the remainder is *empty*: the entire 15–31-edges-per-good
sensitivity was scan artifact, exactly as the design discussion anticipated.

**Why the literal reading loses, and why that's instructive.** The circularity guard changes the
quantity's meaning. On the flow subgraph, *unmet* demand is identically zero — the LP certificate
serves everyone — so DEF is necessarily **total** downstream demand, not unmet. Scheduling
high-DEF nodes early points free edges into subtrees that are *already served* by flow arcs, and
the greedy evaluator then diverts flow into them, stranding it at their sinks while other branches
starve (0.1206 → 0.1415). The ascending key gives free edges the opposite semantics — overflow
spills outward from the heavy trunk lines toward the quiet periphery — and it is the best
deterministic preserver of the validated behaviour on every axis: 0 flips, sink sets and promotions
exactly reproduced, unserved within 0.005 of the old sweep, all guarantees intact (acyclic 29/29,
reach 100.0% untuned, 0 orphans), and noise-stable (0/3 sink-set changes × 3 goods, re-run).

**Adopted as the default**: `run_drain(deterministic=True)` now uses the priority sweep with key
(DEF ascending, β ascending, index); the old scan survives behind `deterministic=False`.

**Interaction with §5's tuned configuration.** With 86 of 159 edges free (tol = 3e-4), rescue
timing matters more, so 5 of 29 sink sets shifted (copper, gems, glass, grain, salt); the span
stays 1..5 and the price correlation *improves* to −0.539. The §5 table above is the regenerated
one. One cost appeared and is footnoted there: silk's reach drops to 99.97% because `ohio` (silk
demand share 2.97e-4, just under the twig threshold) ends up on free edges oriented away from it —
a property of the aggressive §5 pruning, not of the deterministic sweep itself, which is at 100.0%
on all 29 goods at the untuned tolerance.

---

## Appendix — re-verification of all prior documents (this session)

Requested after the earlier model's Cape error. Every headline number in `diagnosis.md`,
`flow-orientation.md` (as corrected), `ranked-orientation.md`, and `basin-orientation.md` was
recomputed from scratch by `scratchpad/v/verify.py`. **33 of 33 checks pass**, including:

- identity k = 3662.4, residual < 1e-14, 159/159 orientation agreement (validation.md's C063/C321)
- the exact sink criterion, 2320/2320; the c>s counts (64/80 spices; 1816 pairs → 102 sinks)
- CF1/CF2/CF3 counterfactual sink sets, and the D-threshold f = 1.725 (bisection reproduced)
- FLOW: 79-edge support on every good, 2158/133/2320 agreement split, cyclic aggregate,
  dual~distance ρ = 0.6097, 100% reach, malacca→cape spice flow 0.242959, hop counts 3-vs-7
- RANK: 83.29% reach, 34/387 orphans, ρ_val +0.281, 9 net-producer sinks, out-degree
  Spearmans (+0.068 vanilla / −0.182 LAP / +0.306 RANK)
- BASIN: 0.3941 as-written / 0.3242 sign-flipped / 0.2206 at γ=1000 / LAP 0.1037; Φ coherence
  52.6% / 29.0%

One imprecision found and fixed in `diagnosis.md`: the Cape's φ places it above **66** of the 80
nodes, not "above 60" (the claim was a true understatement; the number is now exact). No other
discrepancy exists between the documents and the code as of this run.
