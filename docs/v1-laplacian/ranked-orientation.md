# Ranked orientation, tested against the Laplacian

**Verdict up front: ranked orientation wins item 1 decisively — it does not lose it — and then
fails on something item 1 does not measure. Under RANK, 16.7% of world demand sits on nodes the
good can never reach, against 0.0% under the Laplacian. Genoa becomes a cloves sink that cloves
cannot reach.**

Nothing was tuned. `per-good-trade-spec.md` and `validation.md` are untouched. 1444.11.11 data,
29 live goods, 80 nodes, 159 links, α(g) = (price/2)¹.

| tag | definition |
|---|---|
| **LAP** | spec §1.1: `L φ_g = s_g − c_g`, orient by φ, uniform ε (§1.2) |
| **RANK** | `score(n,g) = s(n,g) − c(n,g)` on scored nodes; harmonic extension on the empty set; orient by score; `Φ = Σ_g V_g·score_g` |

Code: `scratchpad/v/rankop.py`, `rankrep.py`, `rankrep2.py`, `rankrep3.py`.
ε is set to 0 for RANK: with the §1.2 uniform ε every node has supply, the empty set is empty and
the harmonic extension never fires. The harmonic extension *is* the candidate's regulariser.

---

## First: the zero-demand claim, confirmed with a correction

`flow-orientation.md` said exactly one node has zero demand for all goods. **Confirmed** — and
your suspicion about the uncolonised regions is right about the mechanism, so it is worth spelling
out, because it is more fragile than the bare claim suggests.

Uncolonised regions do *not* have zero demand, because in EU4 1444 they are not unowned — they
carry **native tags**, and a native-owned `is_city` province produces income like any other:

| node | members | owned + city | wealth | where the demand comes from |
|---|---|---|---|---|
| `carribean_trade` | 62 | **1** | 1.6 | Uyapari (2805), owner **CAB**, tax 1, prod 1, coffee |
| `amazonas_node` | 37 | **2** | 4.2 | Essequibo (743, **ARW**, sugar); Grao Para (748, **TPA**, cocoa) |
| `patagonia` | 20 | **1** | 1.5 | one native province |
| `laplata` | 34 | 2 | 5.0 | two native provinces |
| `brazil` | 44 | 3 | 6.0 | three native provinces |
| `california` | 74 | 9 | 11.0 | nine native provinces |
| **`cape_of_good_hope`** | 20 | **0** | **0.0** | — |

So the Caribbean's entire world demand for every good rests on **one Carib village**. The claim
holds, but by a margin of one province in three of these nodes.

**Consequence for the candidate: the empty set is `{cape_of_good_hope}` for every one of the 29
live goods** — size 1, always, with one connected region and a well-posed 1×1 Dirichlet problem
(four fixed boundary values). Harmonic extension is a single four-neighbour average.

```
empty-set size distribution over 29 goods: {1: 29}
connected empty regions per good: spices 1, cloves 1, grain 1
every empty region well-posed: True
```

---

## 1. Sink sets and demand correlation — the headline

```
operator  sinks/g  mean rank P(sink|top10) P(sink|bot10)    rho_rank     rho_val
LAP           3.5       29.4         9.0%         0.7%      -0.103      +0.104
RANK         13.3       26.0        46.6%         1.0%      -0.280      +0.281
```
*(`rho_rank` = ρ(demand rank, sink indicator), negative = good. `rho_val` = ρ(demand c, sink
indicator), positive = good. These are the same fact with opposite signs; `flow-orientation.md`
used the first convention, your brief the second. All-node mean rank is 40.5.)*

**RANK wins, and by a wide margin.** In your convention `rho_val` goes from +0.104 to **+0.281**,
2.7×. The sharper statistic: a top-decile demand node is a sink **46.6%** of the time under RANK
against **9.0%** under LAP — a 5.2× improvement — while the bottom decile barely moves
(0.7% → 1.0%). For reference, the operators from `flow-orientation.md`: FLOW `rho_rank` = +0.132
(anti-correlated), TREE +0.040 / −0.048 / −0.085.

So: **this does not lose to the Laplacian on item 1. It beats it clearly.**

---

## 2. Cloves and spices at the named nodes

```
--- spices (alpha=1.50) ---
  node                  c   rank  s>0        score | LAP    RANK
  genua           0.03508      1   no    -0.035076 | -      SINK
  english_channel 0.03412      2   no    -0.034122 | -      SINK
  hangzhou        0.03156      3   no    -0.031560 | -      SINK
  venice          0.02077     15   no    -0.020775 | -      -
  canton          0.02007     16   no    -0.020070 | -      -
  saxony          0.01767     22   no    -0.017666 | SINK   -
  beijing         0.01503     31   no    -0.015031 | -      -
  safi            0.01104     44  yes    +0.006430 | -      -

--- cloves (alpha=3.00) ---
  node                  c   rank  s>0        score | LAP    RANK
  hangzhou        0.10385      1   no    -0.103848 | -      SINK
  genua           0.05957      2   no    -0.059570 | -      SINK
  english_channel 0.03983      3   no    -0.039832 | -      SINK
  canton          0.03121      6   no    -0.031206 | -      -
  venice          0.03072      7   no    -0.030722 | -      SINK
  beijing         0.02425     12   no    -0.024249 | -      -
  saxony          0.01611     22   no    -0.016114 | -      -
  safi            0.00839     40   no    -0.008394 | SINK   -
```

**RANK makes the top three demand nodes sinks for both goods.** Genoa, the English Channel and
Hangzhou for spices; Hangzhou, Genoa, the Channel and Venice for cloves. Saxony stops being a
spices sink; Safi stops being a cloves sink. This is precisely the outcome `diagnosis.md` said the
Laplacian could not produce.

Beijing and Canton remain non-sinks in both. Under RANK that is because their neighbours include
Chinese producers with higher scores — a local comparison again, just a better-correlated one.

---

## 3. Safi ↔ Sevilla, per good

```
LAP and RANK agree on this edge for 16 of 29 goods (55%)
```

Where they disagree, RANK is sometimes economically wrong in a way LAP is not:

```
good        s(safi)   c(safi)  score(safi)  score(sevilla) | LAP            RANK
sugar      0.144330  0.011037    +0.133293       +0.067203 | safi->sevilla  safi->sevilla
spices     0.017467  0.011037    +0.006430       -0.025581 | safi->sevilla  safi->sevilla
wool       0.014493  0.011179    +0.003314       +0.017940 | safi->sevilla  sevilla->safi   <-- wrong
tea        0.000000  0.011246    -0.011246       -0.025207 | sevilla->safi  safi->sevilla   <-- wrong
tobacco    0.000000  0.011037    -0.011037       -0.025581 | sevilla->safi  safi->sevilla   <-- wrong
paper      0.000000  0.010813    -0.010813       -0.025340 | sevilla->safi  safi->sevilla   <-- wrong
```

- **wool**: Safi *net-produces* wool (s 0.0145 > c 0.0112) and RANK points wool **into** it,
  because Sevilla produces even more. The direction is decided by which side produces more, not by
  which side needs it.
- **tea, tobacco, paper**: Safi produces none of these and has real demand, yet RANK points them
  *out* of Safi, because Sevilla's demand is larger. Safi is asked to export a good it does not
  have.

That second pattern is the operator's signature and it is what causes the failure in §9.

---

## 4. The Cape of Good Hope

```
good         score(cape)   rank    in-deg   out-deg
spices          0.094243      4         2         2
cloves         -0.011148     47         2         2
silk           -0.010242     55         3         1
sugar          -0.010864     46         3         1
cloth          -0.002898     42         1         3
```

It is a conduit under RANK for every good (in-degree and out-degree both nonzero), by
construction: the harmonic extension makes its score the mean of four neighbours, so it lies
strictly between their max and min. Same argument as §3.2 / C376–C378.

**Spices — the corridor works, and it goes through the Cape:**

```
RANK  malacca -> cape_of_good_hope -> ivory_coast -> bordeaux -> champagne -> genua   (5 hops)
   0  malacca                    0.286379
   1  cape_of_good_hope          0.094243    -0.192136
   2  ivory_coast               -0.005311    -0.099554
   3  bordeaux                  -0.015155    -0.009844
   4  champagne                 -0.028540    -0.013385
   5  genua                     -0.035076    -0.006537
   strictly decreasing at every hop: True    passes through the Cape: True
```

That is better than LAP on this specific test — LAP routes Malacca→Genoa via Alexandria and
**not** through the Cape:

```
LAP   malacca -> ganges_delta -> comorin_cape -> gulf_of_aden -> alexandria -> genua  (5 hops)
   strictly decreasing at every hop: True    passes through the Cape: False
```

**Cloves — no corridor at all:**

```
RANK  the_moluccas -> genua : NO DIRECTED PATH
LAP   the_moluccas -> malacca -> ganges_delta -> comorin_cape -> gulf_of_aden -> alexandria -> genua
```

---

## 5. Acyclicity

```
LAP    non-acyclic goods: 0/29
RANK   non-acyclic goods: 0/29
Phi(LAP)  acyclic: True
Phi(RANK) acyclic: True
exact score ties over 4611 edge-good pairs: 0
```

**RANK is acyclic by construction** and needs no argument beyond the one the spec already uses for
φ: orientation is by a per-node scalar, so the score strictly decreases along any directed path.
This is the candidate's cleanest property — no cycle cancellation, no repair, zero ties.

---

## 6. `Φ = φ₀` residual at α = 1

**Not exact, and the failure is localised to exactly one node.**

```
Phi(RANK,a=1) vs spec phi0 (Laplacian solve of s0-c0)  k=    33.85  rel.residual=9.892e-01  orient agree 109/159
Phi(RANK,a=1) vs ranked analogue score0 = s0 - c0      k=  3662.40  rel.residual=2.439e-01  orient agree 158/159
sum_g V_g = 3662.400000 ; world trade value = 3662.400000
```

Against the spec's φ₀ — the *solution* of a Laplace equation — the identity is simply gone
(residual 0.989, orientation agreeing on 109 of 159). That is expected and not a defect of the
candidate: RANK performs no solve, so there is nothing for the linearity-of-the-solve argument
(C063) to act on. The §1.6 identity is a property of the operator, and removing the operator
removes the identity rather than breaking it.

Against the natural ranked analogue `score₀ = s₀ − c₀` the scalar is recovered exactly
(k = 3662.4000 = Σ V_g = world trade value) and the residual is confined:

```
top nodes by |Phi(RANK) - k*score0|:
  cape_of_good_hope   2.320802e+00     score0 = 0.000000e+00   Phi/k = 6.336835e-04
  gulf_of_siam        2.875478e-14
  crimea              2.309264e-14
residual on the 79 nodes EXCLUDING cape: max 2.875e-14
residual at cape:                             2.320802e+00
```

**The identity holds to machine precision on all 79 scored nodes and fails only at the single
harmonically-extended node** — where the two constructions differ by definition, since
`score₀(cape) = 0 − 0 = 0` while `Φ(RANK)(cape)` is the neighbour mean. That single node moves one
edge of 159.

This is a fair trade only if the identity's purpose is preserved, and it is not: per
`validation-delta.md` the identity is the spec's only end-to-end correctness check. Under RANK it
becomes a check that the arithmetic of a weighted sum is right — which cannot fail — rather than a
check that the solve is right.

---

## 7. Sinks per good; regional sinks surviving

```
operator    min    max    goods with >1     mean
LAP           1      7            24/29      3.5
RANK         11     17            29/29     13.3
```

**RANK keeps more than one sink for all 29 goods**, so the requirement is met — and it fixes LAP's
worst case, the 5 goods (spices among them) that have a unique sink. It is also far short of
FLOW's 26–39.

But 13.3 sinks per good is 17% of the map, and the frequency list shows the sinks are not all the
rich nodes the metric implies:

```
LAP  : safi 12, gulf_of_siam 11, saxony 7, the_moluccas 7, doab 6, african_great_lakes 4
RANK : ohio 26, mexico 23, lima 23, genua 22, novgorod 21, kongo 20, english_channel 20, sevilla 19
```

Genoa (22) and the Channel (20) are there as intended. So are `ohio` (26), `lima` (23) and `kongo`
(20) — poor, remote nodes. They are sinks because *all* their neighbours are producers with higher
scores. RANK has not removed the local-comparison defect; it has changed what is compared.

---

## 8. Out-degree against demand rank

**First, a correction to the premise.** The brief says vanilla has the richest nodes at out-degree
0, the next at 1, the next at 2. That is not what the shipped file does:

```
demand-rank bin    nodes |    VANILLA        LAP       RANK
1-8                   8 |       1.62       2.14       1.33
9-16                  8 |       2.00       2.08       1.67
17-24                 8 |       1.75       1.96       1.66
25-40                16 |       2.25       2.16       2.12
41-56                16 |       1.81       1.70       1.95
57-72                16 |       2.12       1.97       2.14
73-80                 8 |       2.12       2.06       2.78

spearman(demand rank, VANILLA out-degree) = +0.068
spearman(demand rank, LAP     out-degree) = -0.182
spearman(demand rank, RANK    out-degree) = +0.306
```

Vanilla's gradient is **essentially flat (+0.068)**. What is true is narrower: the three `end=yes`
nodes — Genoa, Venice, the English Channel — have out-degree 0 and are all high-demand. But the
top-8 demand bin averages 1.62 outgoing links, so there is no 0/1/2 staircase to reproduce.

Against the *intent* rather than the stated pattern: **RANK reproduces it (+0.306) and LAP gets
the sign backwards (−0.182)** — under the Laplacian, richer nodes have *more* outgoing links.
RANK is the only one of the three tested operators that puts rich nodes at low out-degree, and it
does so more strongly than vanilla itself.

---

## 9. The functional test RANK fails

Items 1–8 measure where sinks sit. None of them asks whether the good can get there. That test
decides it.

For each good: take the nodes with real supply, walk the directed graph, and measure the fraction
of world demand for that good sitting on a reachable node.

```
                     LAP                    RANK
good            srcs  dem.reach  orphans | dem.reach  orphans
chinaware          9     100.0%        0 |     72.8%        2
cloves             1     100.0%        0 |     32.3%        9
cocoa              4     100.0%        0 |     50.8%        3
coffee             8     100.0%        0 |     72.3%        1
fur               14     100.0%        0 |     75.2%       14
glass             13     100.0%        0 |     78.5%        2
incense            8     100.0%        0 |     72.9%        4
ivory             12     100.0%        0 |     75.1%        1
spices            18     100.0%        0 |     80.9%        2
tea               10     100.0%        0 |     71.8%        1
tobacco            4     100.0%        0 |     52.1%        3
tropical_wood     16     100.0%        0 |     74.9%        1
grain             64     100.0%        0 |    100.0%        0
salt              46     100.0%        0 |    100.0%        0

LAP   mean demand reachable = 100.00% | goods at 100% = 29/29 | orphan sinks =  0 of 102
RANK  mean demand reachable =  83.29% | goods at 100% =  2/29 | orphan sinks = 34 of 387
```

**Under LAP every good reaches 100% of its demand, for all 29 goods, with zero orphan sinks.
Under RANK the mean is 83.3%, only 2 of 29 goods reach everything, and 34 sinks are orphans — a
sink the good can never reach.**

And the orphans are exactly the nodes RANK was built to promote:

```
cloves    9 orphans: genua(rank 2), english_channel(rank 3), venice(rank 7), sevilla(rank 15),
                     aleppo(rank 17), timbuktu(rank 23)
incense   4 orphans: mexico(rank 6), novgorod(rank 22), lima(rank 54), ohio(rank 62)
cocoa     3 orphans: venice(rank 11), constantinople(rank 23), novgorod(rank 28)
tobacco   3 orphans: persia(rank 19), constantinople(rank 20), novgorod(rank 24)
```

**Genoa is a cloves sink that cloves cannot reach.** It has demand rank 2, it has no outgoing
edges, and no directed path from the world's only cloves source arrives. It is a sink on paper and
a dead end in fact — strictly worse than not being a sink, because the model will report 100%
collection of a value that never arrives.

### Why, exactly

```
cloves supply nodes: [('the_moluccas', 1.0)]     <- one node holds all world supply
score of the source and its neighbours:
  the_moluccas    +0.980510   (source)
  australia       -0.001900
  philippines     -0.005232
  malacca         -0.022813
RANK reachable from the source: 14 of 80 nodes, 32.3% of demand
```

Under `score = s − c`, a non-producing node's score is `−c(n)`. So a descending path can only move
to nodes of **strictly greater demand at every hop**. Once cloves reach Malacca (c = 0.0228), the
next node must have c > 0.0228, and Ganges Delta does not — so the edge points the wrong way and
the corridor is severed. Only 14 nodes lie on a monotonically-increasing-demand walk from the
Moluccas.

**This is C370/C371, which the spec already establishes and `validation.md` already confirmed:**

> Under a monotone orientation no path can dip through a low-value intermediary and rise again.
> — spec §3.2, C371, CONFIRMED with 0 counterexamples in 20,000 random rankings

The candidate is a rank orientation. §3.2 rejects rank orientations for exactly this reason. The
only difference is the ranking variable — `s − c` rather than wealth — and the theorem does not
care which. It bites here as *demand* having to increase monotonically along every trade route,
which is a strong and false requirement: transit nodes are typically poorer than the terminus they
feed.

The harmonic extension rescues the *one* node with neither supply nor demand — which is why the
Cape corridor works for spices — but it does nothing for the 79 nodes that have a little of both,
and those are where the corridors break.

---

## What breaks

### Widely-produced goods and ±1% wealth noise

Not a problem, for either operator.

```
good           srcs   max|score| median|score|   frac<1e-3   RANK sinks
grain            64    3.626e-02    5.301e-03      13.8%          11
livestock        49    4.495e-02    6.665e-03      11.2%          12
cloves            1    9.805e-01    8.511e-03      16.2%          13

+/-1% per-province wealth noise, 5 seeds:
good          LAP flips/159  RANK flips/159   LAP sink chg  RANK sink chg
grain                   0.0             0.0            0/5            0/5
livestock               0.0             0.2            0/5            0/5
spices                  0.0             0.0            0/5            0/5
cloves                  0.0             0.0            0/5            0/5
```

Grain's median |score| is 5.3×10⁻³ against a 3.6×10⁻² max, and 13.8% of nodes fall inside 10⁻³ —
barely above cloves' 16.2%. Under noise, RANK flips 0.2 of 159 edges on livestock and 0 elsewhere;
no sink set changes for either operator. Widely-produced goods are flatter, not degenerate, and
orientation is not noise-sensitive. Same conclusion as `flow-orientation.md`.

### A sink that net-produces the good

**RANK introduces this defect; LAP does not have it.**

```
LAP  : 0 of 102 sink pairs net-produce their good
RANK : 9 of 387 sink pairs net-produce their good
       cloth/deccan (s 0.0331 > c 0.0192), fur/james_bay (0.0171 > 0.0010),
       iron/white_sea (0.0080 > 0.0031), naval_supplies/nippon (0.0415 > 0.0278),
       naval_supplies/white_sea (0.0104 > 0.0042), paper/doab (0.0291 > 0.0246)
```

I predicted in the harness that RANK could not do this — that a net producer has `score > 0` and
any negative-score neighbour would give it an outgoing edge. **The data refutes that**: it happens
whenever *every* neighbour also net-produces the good and has a higher score. Deccan produces
cloth at 1.7× its own demand and cannot ship any of it, because Gujarat and its other neighbours
produce more still. That is a conservation violation the model has no way to express.

### Conduits terminating instead of passing through

Both clean.

```
LAP   cape passes through 29/29 goods ; terminates 0/29
RANK  cape passes through 29/29 goods ; terminates 0/29
```

Guaranteed for RANK by the harmonic extension, for the same reason as C376–C378.

### Empty set size and well-posedness

```
empty-set size distribution over 29 goods: {1: 29}
connected regions per good: 1
every region well-posed: True
```

One node, one region, always — a 1×1 system with four fixed boundary values. Well-posed
trivially. Worth noting that this is a property of the *1444 map*, not of the method: on a map with
a larger uncolonised interior (or with the native tags removed) the empty set would grow, regions
could become large, and a region with no scored boundary neighbour at all would be ill-posed. The
implementation handles that case by falling back to 0, which is a silent guess — acceptable
because it never fires here, but it is a latent hole rather than a solved problem.

---

## Conclusion

| | LAP | RANK |
|---|---|---|
| **demand reachable from supply** | **100.0%, 29/29 goods** | **83.3%, 2/29 goods** |
| **orphan sinks** | **0 of 102** | **34 of 387** |
| sink–demand correlation (ρ_val) | +0.104 | **+0.281** |
| P(sink \| top-decile demand) | 9.0% | **46.6%** |
| top-3 demand nodes are sinks | no | **yes, spices and cloves** |
| out-degree gradient vs demand | −0.182 (wrong sign) | **+0.306** |
| acyclic per good | yes | **yes, by construction** |
| `Φ` acyclic | yes | yes |
| §1.6 identity | **exact (1.96e-15)** | exact on 79/80 nodes; undefined against the spec's φ₀ |
| sinks per good | 1–7, 5 goods with a unique sink | 11–17, all goods keep >1 |
| sinks that net-produce their good | **0** | 9 |
| stable to ±1% noise | yes | yes |

**It does not lose on item 1 — it wins it, clearly and on every framing of the statistic.** The
honest finding is that item 1 was the wrong test to decide on. Ranked orientation buys
demand-correlated sinks by severing the routes that make a sink mean anything: it requires demand
to increase monotonically along every trade route, and where that fails the corridor breaks. One
sixth of world demand ends up unreachable, and the flagship result — Genoa as a cloves sink — is
the clearest instance of the defect rather than a success.

Two things are worth keeping from this test, independent of the verdict:

- **The reachability metric.** Neither `flow-orientation.md` nor `diagnosis.md` measured whether a
  good can reach its consumers. LAP scores a perfect 100.0% on all 29 goods, which is a strength of
  the incumbent that no document had recorded until now. Any future candidate should be held to it
  first.
  **Later correction:** the metric was subsequently applied to FLOW, which also scores 100.0% on
  all 29 goods with 0 orphan sinks — necessarily, since its LP imposes node balance. So the metric
  separates *conservation-respecting* operators (LAP, FLOW) from ones that impose no balance
  condition (RANK 83.3%, BASIN 88.5%); it does not separate LAP from FLOW. See the corrected
  conclusion in `basin-orientation.md`.
- **The out-degree finding.** LAP's out-degree correlates with demand at the *wrong sign*
  (−0.182): richer nodes have more outgoing links. That is a real defect of the incumbent, it is
  not explained by `diagnosis.md`'s headroom mechanism, and RANK shows it is fixable in principle.

The family is not closed the way flow was. Flow failed because a unit-cost flow *is* a distance
operator. Ranked orientation fails because it is monotone, which is C371 — a theorem the spec
already had. What both failures share is that they discard global information: flow discards
demand's magnitude, rank discards position. The Laplacian is the only one of the three that keeps
both, which is why it is the only one where every good reaches every consumer.
