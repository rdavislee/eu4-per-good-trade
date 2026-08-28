# Changes, spec v2.1 → v3.0

**Method.** v3.0 was produced by **copying** `../v2-drain/per-good-trade-spec.md` and editing it in
place. No section was rewritten from scratch. A paragraph-level diff (`diffspec.py`) reports
**0 paragraphs deleted outright**, 29 replaced and 10 inserted: every removed sentence has a
replacement, and no section heading was lost (`## 2.2a` is the only addition). The file grew from
74,860 to 99,323 bytes.

**Inputs.** `per-good-trade-spec.md` v2.1, `../v2-drain/validation-v2.md` (11 refutations,
24 partials), `../v2-drain/game-session.md` (5 settled probes).

**Every deleted or replaced passage is quoted below**, grouped by what drove the change.

---

## Summary of what changed

| Driver | Count | Where |
|---|---|---|
| Refutations folded through | 11 | §1.1, §1.6, §1.7, §2.4, §2.8, §3.2, §3.3, §3.5, §3.8, §3.9, §3.13, §3.15, §3.16 |
| Partials narrowed to what is proved | 24 | throughout |
| v1 corrections v2 never folded | 4 | §1.7, §1.10, §3.3, §3.14 |
| Game probes closed | 5 | §1.9, §2.4, §2.7, §3.6, §3.16 |
| Wealth made owner-agnostic | — | §1.3, §2.2, §2.3, §3.3, §3.4 |
| Both-ways claims decided | 2 | §2.2a (new), §1.1 |

---

# 1. Wealth becomes owner-agnostic

## §1.3 — the autonomy paragraph, deleted

**Removed:**

```
Autonomy floors are regime-dependent — there is no flat overseas floor in 1.37 (the 75% rule is
pre-Common-Sense). From `00_static_modifiers.txt`: a province in a **territory** is floored at
**90%** local autonomy (`territory_core` / `territory_non_core`), a **colonial core** at **50%**,
a **pasha state** at **20%**, a stated core at 0. The wealth pipeline applies the applicable floor
per province — a territory province contributes ~10% of its development's income, a colonial core
~50%.
```

```
wealth(p) = tax_income(p) + production_income(p)
```

```
Unowned provinces generate no income and contribute nothing.
```

**Replaced by** the owner-agnostic definition, the empirical derivation of both coefficients, the
time-basis argument, the modifier-ordering rule, and the local/owner classification rule. The
autonomy floors are not corrected — they are **removed from the model entirely**, because under
v3.0 no owner property enters wealth. The floors remain true facts about EU4; they are simply no
longer facts this spec uses.

### How the replacement was derived

Nothing was inherited. `defines.lua` and `common/defines/` contain neither coefficient, so both
were measured in-game on **Garnatah (province 223)** — `base_tax = 6`, `base_production = 4`,
silk, **`local_autonomy = 0`** so no owner term was in play. The engine's own itemised tooltips:

```
Base: 0.49 (Yearly 6.00)
Tax Income Efficiency: 125.0%
   Core: +75.0%
   City: +25.0%
   Reform Iqta: +5.0%
   Clergy: +5.0%
   Granadan Traditions: +15.0%
---------------
This is the monthly tax income from this province. It will generate a yearly income of 7.46.
```

```
Trade Value: +0.26
Production Efficiency: +2.0%
   From Technology: +2.0%
---------------
This is the monthly production income of the province. It will generate a yearly income of 3.25.
```

```
Base Goods Produced: 0.80
   Base Production: +0.80
---------------
Goods Produced increases the Trade Value of a province by providing more trade goods.
```

Which give, all cross-checking: yearly tax base **6.00 = base_tax** (so `TAX_COEFF = 1.0`); goods
produced **0.80 = 0.2 × 4** (so `GP_COEFF = 0.2`); trade value **3.20 = 0.80 × 4.00** (silk price
from `00_prices.txt`); monthly production `3.20/12 × 1.02 = 0.27` ✓; monthly tax
`6/12 × 1.25 = 0.62` ✓.

- **Time basis:** both terms are annual-over-twelve, so the annual forms add with no conversion.
- **Modifier order:** after the coefficient, as a percentage on the base — except flat goods
  bonuses, which add into `goods_produced` before the price multiply.
- **Which modifiers are local:** the engine's own data model splits them — a trade good's
  `province = {}` block is province-scoped, its `modifier = {}` block is country-scoped. Only the
  first counts. In vanilla the income-relevant local ones are exactly `gems`
  (`local_tax_modifier = 0.15`), `glass` (`local_production_efficiency = 0.1`) and `incense`
  (`trade_value_modifier = 0.1`). `terrain.txt` carries none.
- Everything else the engine itemised — Core, Reform Iqta, Clergy, national ideas, technology
  production efficiency — is owner-derived and excluded. `City +25%` is place-intrinsic but
  constant across every province the model counts, so it cancels in the normalised share.

**Three things could not be settled empirically and became open questions in §3.13**, not numbers
in §1.3: whether local flat goods bonuses exist at 1444 and where they enter; whether a trade
good's `local_production_efficiency` is inside or outside local wealth (the structural rule and
the vocabulary disagree); and whether `TAX_COEFF` stays 1.0 across the development range, which
was measured at one province only.

### The reference solver did not change

`solver.py` already computed `wealth = base_tax + 0.2·base_production·price` with no autonomy
term. validation-v2 filed that as **systemic finding 1**, a defect — the solver not implementing
§1.3. Under v3.0 the solver was right and the spec was wrong, so **every measured number in v2
remains valid** and re-running reproduced them exactly (`v3measure.py`).

## §3.4 — added rather than removed

**Removed:**

```
Production efficiency does not conjure more cloves; it means the owner extracts more ducats from the same cloves. That is a fact about purchasing power and belongs in demand.
```

The clause "and belongs in demand" is now false. The replacement keeps the supply argument intact
and notes that v1 and v2 excluded owner effects from supply and then let them back in through
`wealth`, running the demand side on exactly the incoherence they rejected on the supply side.

---

# 2. Refutations folded through

## V062 — `Φ_ord` coherence, 62.7% → 60.2% (three sites)

**Removed (§1.6):**

```
Agreement with the per-good graphs is 53.4% of edge-goods (52.1% value-weighted) — *lower* than the superseded `Φ_ord`'s 62.7%; that trade is recorded in §3.9.
```

**Removed (§3.9):**

```
  free and remains the most self-coherent aggregate measured: 62.7% edge-good agreement with the
  per-good graphs against `Φ_w`'s 53.4% (52.1% value-weighted).
```

**Removed (§3.15):**

```
most self-coherent aggregate measured (62.7% vs `Φ_w`'s 53.4%) and still acyclic for free
```

62.7% was measured under the **old scan-order sweep** and never regenerated after §3.6 adopted the
deterministic one. The deterministic figure is **60.2%** (2774/4611). The coherence sacrificed by
moving to `Φ_w` is 6.8 points, not 9.3, and §3.15's "ceiling any future aggregate should be
compared against" was 2.5 points too high.

## V159 — any-good reachability, 98.8% → 90.9%

**Removed (§3.8):**

```
measured, 98.8% of ordered node pairs are connected by at least one good on 1444 data.
```

98.8% (6245/6320) is **v1's Laplacian measurement**, carried into v2 across the operator change
without being re-run. Under DRAIN it is **90.9%** (5743/6320). The argument survives; the number
was not v2's.

## V145 — price events, 13 of 30 → 12 of 30

**Removed (§3.5, and the same figure in §3.13):**

```
how often that can happen: **13 of 30 goods** can be pushed below 2.0 by a single vanilla
`change_price` event (grain and wine reach 0.625), and **11 goods have no negative price event at
all** and can never go sublinear in vanilla.
```

**12** goods reach strictly below 2.0. Three more — `gems`, `silk`, `wool` — land *exactly on*
2.0, reaching α = 1 but not the sublinear regime; that boundary is the likely origin of the
off-by-one. All 101 `change_price` blocks across `events/`, `decisions/`, `missions/` and
`common/` were parsed. The 11 with no negative event is exact.

## V107 — no Chinese node holds a spices sink

**Removed (§2.8):**

```
**China holds a spice sink only under the §3.13 α-calibration option** (which puts cloves at Beijing) — the v1 expectation of simultaneous China+Europe sinks is not the baseline behaviour
```

Under the calibration `spices` sinks at **Genoa and Doab**; it is **cloves** that moves to Beijing.
The sentence contradicted its own parenthetical.

## V029 / V125 / V126 — the sink identity is not a theorem

**Removed (§1.1):**

```
- **Sink placement is explicit:** the final sinks are exactly
  `{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal demanders}` — 1–8 per good, mean
  3.6, on 1444 data.
```

**Removed (§3.2):**

```
1. **Sink placement:** final sinks = `{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal
   demanders}`. Nothing else can be a sink (every other node is given an out-arc by the sweep).
```

**Removed (§3.2):**

```
geometry entirely: sinks are the selected demand centres plus the flow-terminal drains any acyclic
drainage orientation would be forced to have anyway.
```

Two constructed inputs break the equality in both directions — a pendant net-importer is a sink
outside the set, and inside the 2-core a selected flow-terminal demander can lose sinkhood to a
free edge reaching an earlier-marked node. Both are now worked in §3.2. What survives
unconditionally is the ⊆-direction within the 2-core.

## V127 — v1 *did* state aggregate acyclicity

**Removed (§3.2):**

```
The four claims v1 never stated, now stated
and checkable:
```

v1 stated aggregate acyclicity as **C061** ("`Φ` is a potential, so orienting edges by it is
acyclic"), and its ε-machinery stated what decided dead-branch direction. Genuinely unstated: the
sink-placement determinant and any reachability guarantee.

## V134 — the node-slicing distortion

**Removed (§3.3):**

```
at α = 1.5 a 77-province node beats a
19-province node of equal total wealth by 2× purely on slicing
```

At equal totals the node-level form is count-blind and the two **tie**. The distortion is against
the *per-province* form: node-level α overweights a k-province node by `k^(α−1)`, giving
`(77/19)^0.5 ≈ 2×` and Nippon over Paris by `(68/33)^0.5 ≈ 1.44×`.

## V230 — a latent good does move `Φ_w`

**Removed (§2.8):**

```
| Latent good | A good with zero world production has no graph, no value weight, no survival-table entry; acquires all three the month production begins; `Φ_w` is unaffected throughout |
```

`Φ_w` reads wealth, and wealth reads the province's good and its price. A latent good activating
*replaces* the province's trade good, so it moves the wealth field: repricing vanilla's 45 owned
latent-coal provinces to coal flips 10 of 159 `Φ_w` edges. This proposition was true under v2.0's
`Φ_ord` (where `V_g = 0` gave a latent good zero weight) and silently became false with the
operator change.

## V004 — the four v1 corrections v2 never folded

**Removed (§1.7):**

```
A merchant present gives +2 trade power and +10% trade efficiency, node-wide, regardless of what it is doing.
```
Trade efficiency and a flat income bonus are different quantities; `TRADE_MERCHANT_PRESENT = 0.1`
carries the shipped comment "bonus on income if trade present".

**Removed (§1.10):**

```
It is a step function on raw power: it either applies or it does not
```
Caravan power is not a function of trade power at all — it is development ÷ `CARAVAN_FACTOR` plus
modifiers, clamped, gated by a merchant condition. §1.10 contradicted §3.11.

**Removed (§3.3):**

```
a sugar island has negligible development but large production income
```
At vanilla prices sugar/cocoa/coffee are 1.2–1.6× grain, not multiples.

**Removed (§3.14):**

```
about 0.75 MB, well under a million operations per solve
```
0.75 MB is the single-precision figure; the solver is double precision, so 1.5 MB.

---

# 3. Partials narrowed to what is proved

Each of these asserted more than the evidence supported. The measurement is kept; the claim is
narrowed or its missing premise supplied.

| Claim | Was | Now |
|---|---|---|
| **V016** spanning-tree basis | asserted for any optimum | holds for a **basic** optimum; §2.2 now requires simplex, not interior-point without crossover |
| **V031** reachability | "a feasibility theorem" | a feasibility theorem **on a connected map**; §2.2a states the premise and what the solver does otherwise |
| **V060** marking order reproduces the DAG | asserted generally | holds on the 2-core; pendants have no marking order (§2.2a table) |
| **V036** efficiency | "fewest-hop routing" | fewest-hop **in aggregate**; no per-unit shortest-path claim |
| **V151** alternating links carry near-nothing | asserted | **measured** (0 support changes moving >1e-6 under 1e-9 nudges), with the tie-selection premise named |
| **V153** key from "exact input data" | asserted | values from inputs, **structure from the LP support** |
| **V086** sweep "integer/combinatorial" | asserted | deterministic float comparisons; reduces to the LP question |
| **V114** "both failures are theorems" | asserted | one theorem, one exact rule with a measured consequence |
| **V123** input precision | "1.7× where 4–5× is needed" | ~1.7× buys Genoa as a **co-sink**; a Chinese sink needs 3.6–4.8× |
| **V190** ranked orientation | "wins every sink statistic" | wins the **alignment** statistics; loses on 9 net-producer sinks and 11–17 sinks/good |
| **V205** provenance count | "nine of the fourteen" | **nine of the sixteen** refuted ENGINE claims |
| **V214** scale invariance | asserted | true in exact arithmetic; the **absolute** zero-flow tolerance breaks it downward (13 flips at ×10⁻², sink collapse at ×10⁻⁶) |
| **V215** `Φ_w` sink ranks | "wealth ranks 3 and 2" | ranks in the **α_Φ-weighted field**; by node wealth they are 12th and 1st |
| **V216** `Φ_w` sources | "all cul-de-sacs" | all in the **bottom half of the wealth field**; mean degree 3.1 vs the map's 4.0 |
| **V219** coherence comparator | vs 62.7% | vs **60.2%** (see V062) |
| **V222** `Φ_ord` end count | "α-invariant, 9–17" | **never concentrates**: 13–22 across cloves-α 2…64 |
| **V225** gravity kernel | "69% vanilla agreement" | count-follows-seeds confirmed; agreement **66%** in the reproduced construction |
| **V179/V180** calibration costs | "richest single province"; "<0.03% of mass" | Beijing is **demand rank 2** (hangzhou holds the richest province); up to **0.15%** of a good's mass; **silk** to 99.97%, cloves to 99.997% |

---

# 4. Game probes closed

## §2.7 — four items struck

**Removed verbatim:**

```
12. **Per-province gold.** Open one gold province's Production income tooltip: does the per-province field carry the gold figure, or is it zero with gold only in the country's `INCOMEGOLD` line? One tooltip settles §1.5's residual.
```

```
13. **Cyclic node file.** Hand-author a two-node cycle in `00_tradenodes.txt`, load a fresh game, read `logs/error.log` and the trade mapmode. The *format* represents cycles fine; what §2.4 depends on is the **engine** rejecting or tolerating one, which is unverified and load-bearing.
```

```
14. **Incoming-link button.** In the vanilla node window, does an incoming `TradeNodeLink` entry accept a merchant assignment or only navigate? Decides whether §1.7's UI change is a behaviour change to an existing widget or a new interaction.
```

```
15. **Propagation source qualifier.** The engine tooltip says power transfers upstream "to trade nodes **where it already has power**" — a receiving-side qualifier §1.9 does not carry. Country with above-threshold power in X and zero in upstream Y: does it appear in Y? This line is §3.16's cautionary case; it has already been corrected once.
```

Item 12 was **dropped, not run**: under owner-agnostic wealth nothing reads the per-province
production-income field, so its contents no longer matter. Items 13–15 were run.

## §2.4 — the ordering requirement, reversed in part

**Removed:**

```
The engine performs no topological sort — the file must be one.
```

```
1. **Declaration order** — emit in decreasing `Φ_w` marking order. (The shipped vanilla file is
   itself topologically sorted sources-first — 0 of 159 links violate it — so this matches the
   observed convention; whether the engine *requires* it is §2.7 item 13's companion question.)
```

The engine **validates** order and logs `[tradenodedefinition.cpp:61]` once per violating link,
then **tolerates** it — a file with all 159 links backwards loaded and played normally. What it
does *not* tolerate is a **cycle**: `EXCEPTION_STACK_OVERFLOW`, 1002 frames at one address,
reproduced twice, with vanilla and the reversed-order file as controls. So "must" was too strong
about ordering and too weak about acyclicity. §2.4 also now records that a **hand-reversed link is
honoured completely** (item 3's check, done and passed), and that the node window renders its link
lists in file declaration order.

## §3.6 — the cycle hedge, removed

**Removed:**

```
What the design depends on is
the **engine's** behaviour on a cyclic file, which is unverified and load-bearing: §2.7 item 13 is
the one-file-edit test, and until it runs, acyclicity is enforced because we cannot prove the
engine tolerates its absence.
```

Acyclicity is now enforced because the engine **provably cannot survive its absence**.

## §1.9 — the qualifier, resolved in the spec's favour

**Added**, not removed: §1.9's "in **every** immediately upstream node" was correct and gains an
explicit note that the tooltip's "where it already has power" is descriptively false. France holds
zero provinces and zero merchants in Sevilla and still receives 3.3 power there, itemised by the
engine as `Transfers from traders downstream: +3.1`.

## §3.16 — the cautionary case, closed

**Removed:**

```
The v1 cautionary case is retained because it is not yet closed: the propagation source condition
was corrected once (ship propagation under its modifier), defended by two reviewers against the
wrong error — and the engine's own tooltip carries a *second* qualifier ("where it already has
power") that §1.9 still does not, pending §2.7 item 15. A line can be confidently defended against
one mistake while carrying another; agreement between reviewers is not verification.
```

The case closed in the spec's favour, and the lesson changed: the unreliable source was a **binary
string**, the class §3.16 nominates as sufficient. Sources are necessary, not sufficient. §3.16
also gains a second failure mode — **a measurement without a null comparison is not evidence** —
after v3.0 nearly shipped a false positive on the declaration-order test.

---

# 5. Both-ways claims decided

## Connectedness — decided: connected maps only

**Removed (header):**

```
**Target:** EU4 (final patch, 1.37.5 Inca), extended timeline compatible, map-agnostic
```

The header now reads **"Connected maps only — see §2.2"**. A new **§2.2a** states the two premises
the proofs actually need, and what the solver must do when they fail: on more than one component,
either renormalise `s` and `c` per component or refuse to start. It must not hand an infeasible
program to the LP. v1 carried per-component renormalisation (C013–C018); v2 dropped it without
replacement; v3 restores the requirement.

## Map-agnosticism — decided: narrowed, with a table

§2.2a tabulates which §1.1 properties survive where Phase 0 acts. Global DAG and free-edge
determinism survive; sink-set equality and the marking-order reconstruction do not. The algorithm
still runs and still produces an acyclic, fully-oriented, demand-serving graph on a connected map
with pendants — only the *characterisations* weaken.

---

# 6. Measurement provenance

Every number in v3.0 was regenerated this session by **`v3measure.py`** against the 1.37.5 install,
except as listed below. Reproduced exactly from v2 (confirming the wealth model was already
owner-agnostic): 80 nodes / 159 edges / 318 arcs, 1 component, min degree 2, 0/159 order
violations, 3 end nodes; per good — acyclic 29/29, sinks 1–8 mean 3.6, k = 1 for 27 of 29, 0
fallbacks, support 78–79, reach 100% 29/29, 0 orphans, 0 flips, 0 key ties, LP deterministic over
6 solves; cape `b = 0` for all 29 goods and a conduit 29/29; `Φ_w` two sinks
(hangzhou/english_channel), 8 sources, 159/159 oriented, 0 order violations, 53.4%/52.1%
agreement, 0 flips and 0/5 sink changes under ±1% noise, sink counts 5→2→1→2→3→1 across
α_Φ ∈ {1, 1.5, 2, 3, 4, 8}; `Φ_ord` 60.2% and 18 ends of which 9 terminate no good; 90.9% ordered
pairs; supply contrast 2.52×10⁷ vs demand 471.5.

Other scripts: `graphchk.py` (hops, bridges, land counts), `leftovers.py` (price events),
`namegrep.py` (node-name references), `savefmt2.py` (save encodings), `toys.py` (sink-formula
counterexamples), `cmp3.py` (declaration-order null comparison), `phiw2.py`/`phiw3.py`
(`Φ_w` dynamics and gravity kernel).

## Not regenerated in v3.0 — **[unverified in v3.0]**

These numbers are carried from v2 or v1 documents and were **not** re-run this session. Each is
flagged in place in the spec where it appears.

- The **§3.13 calibration table** (span 1..5, spearman −0.539, per-good sink lists). Regenerated in
  the v2 validation pass but not by `v3measure.py`.
- The **barbell statistic** (§2.8: sinks at 14% in the top demand decile vs 7% in the bottom) and
  the sink–demand correlation ρ_val figures.
- The **§3.10 factoring tolerances** (5.7e-14, 1.4e-14, the 5.96-ducat per-good-propagation error).
- **BASIN** 88.5% reach and **RANK** 83.3% / 34 orphans — re-verified in the v2 pass, not here.
- **§3.11's nineteen countries at the caravan cap** and the 2–10% near-miss list.
- Hop counts, node land-province counts, and the 24% spice-through-Cape figure — verified in the
  v2 pass by `graphchk.py`/`verify.py`, not re-run by `v3measure.py`.

## A note on what "measured" is worth here

Two of v3.0's corrections exist because a previously-measured number was carried across a change
that invalidated it — V062 across the sweep change, V159 across the operator change. Both looked
impeccable. The rule this document now enforces: **a measured figure carries the script and the
revision that produced it**, and a figure that survives a change to the thing it measures is
re-run or marked unverified.
