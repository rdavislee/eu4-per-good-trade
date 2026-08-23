# Flow-based orientation, tested against the Laplacian

**Verdict up front: both candidates are worse than the Laplacian, and the ε change is a no-op
resting on a false premise. The current operator stays.**

Nothing was tuned. `per-good-trade-spec.md` and `validation.md` are untouched. All results are on
the 1444.11.11 dataset, 29 live goods, 80 nodes, 159 undirected links, α(g) = (price/2)¹.

Three operators compared:

| tag | definition |
|---|---|
| **LAP** | current spec §1.1: `L φ_g = s_g − c_g`, orient by φ, uniform ε (§1.2) |
| **FLOW** | per good, min-cost flow on the undirected adjacency, unit cost per arc, targeted ε; orient by sign of net flow |
| **TREE** | root a spanning tree, subtree totals of `s − c` bottom-up, orient tree edges by subtree sign and non-tree edges by comparing endpoint subtree totals; three trees tested |

Code: `scratchpad/v/flowop.py` (operators), `flowrep.py`, `flowrep2.py`, `flowrep3.py` (report).
The flow is solved as an LP over 318 directed arcs with 80 node-balance constraints via HiGHS
(`scipy.optimize.linprog`), which returns both the primal flow and the node duals.

---

## 0. The finding that decides it

**The min-cost-flow optimum orients only 79 of 159 edges — 49.7% — and this is structural, not
numerical.** An uncapacitated min-cost flow has a basic optimal solution whose support is a
spanning tree, so the support is *exactly* N−1 = 79 edges. The other 80 carry precisely zero net
flow and get no orientation at all.

The generated `00_tradenodes.txt` must declare a direction for every link. A per-good operator
that silently declines to orient half the map cannot supply one.

And where it does commit, it does not disagree with the Laplacian:

```
edge x good pairs: 4611
FLOW unoriented            : 2320 (50.3%)
FLOW oriented, SAME as LAP : 2158 (94.2% of oriented)
FLOW oriented, OPPOSITE    :  133 ( 5.8% of oriented)
```

So flow-based orientation is not a different answer to the orientation question. It is the same
answer on half the edges and silence on the other half.

---

## 1. Sink sets and correlation with demand rank

```
operator        sinks/g  mean rank P(sink|top10) P(sink|bot10)     spearman
LAP                 3.5       29.4         9.0%         0.7%       -0.103
FLOW               32.1       44.2        32.1%        52.1%       +0.132
bfs@malacca         7.5       43.4        11.0%         3.1%       +0.040
bfs@genua           8.4       37.2        10.3%         8.6%       -0.048
dfs@saxony          8.6       34.8        19.7%         2.8%       -0.085
```
*(rank 1 = highest demand; all-node mean rank is 40.5. Spearman is between demand rank and the
sink indicator, so **negative** means sinks are high-demand.)*

**This is the opposite of the intended effect.** FLOW's sinks are *anti*-correlated with demand:
a bottom-decile demand node is more likely to be a sink (52.1%) than a top-decile one (32.1%),
and the mean sink demand rank (44.2) is worse than chance (40.5).

**LAP is the best of the three on exactly the metric the candidates were meant to improve.** Its
top-decile enrichment is 9.0% against 0.7% in the bottom decile — a 13× ratio in the right
direction, and the only Spearman with a meaningfully negative sign.

I should correct my own framing in `diagnosis.md`: I said sinks do not track demand. More
precisely — *placement* is topological, as demonstrated there, but the Laplacian nonetheless
carries a real, if weak, demand signal, and it is stronger than anything either candidate
produces.

Most frequent sinks tell the same story:

```
LAP  : safi 12, gulf_of_siam 11, saxony 7, the_moluccas 7, doab 6, african_great_lakes 4
FLOW : patagonia 28, laplata 26, zambezi 25, amazonas_node 24, rio_grande 24, safi 23, ohio 22
```

FLOW's habitual sinks are the poorest and most remote nodes on the map. That is the same disease
as the Laplacian's, in a more advanced stage: a min-cost flow ships each unit along a shortest
path, so the flow arborescence's **leaves** have no outgoing flow, and the leaves are exactly the
nodes nothing routes through — Patagonia, La Plata, Amazonas, James Bay.

---

## 2. Cloves and spices at the named nodes

```
--- spices (alpha=1.50) ---
  node              c   rank    s>0 | LAP    FLOW   bfs@malacca  bfs@genua  dfs@saxony
  genua       0.03508      1     no | -      SINK   -            -          -
  venice      0.02077     15     no | -      -      -            -          -
  beijing     0.01503     31     no | -      SINK   -            -          -
  canton      0.02007     16     no | -      SINK   -            -          -
  saxony      0.01767     22     no | SINK   -      -            -          -
  safi        0.01104     44    yes | -      -      -            -          -

--- cloves (alpha=3.00) ---
  node              c   rank    s>0 | LAP    FLOW   bfs@malacca  bfs@genua  dfs@saxony
  genua       0.05957      2     no | -      -      -            -          SINK(no)
  venice      0.03072      7     no | -      SINK   -            -          SINK
  beijing     0.02425     12     no | -      SINK   -            -          -
  canton      0.03121      6     no | -      -      -            -          -
  saxony      0.01611     22     no | -      -      -            -          -
  safi        0.00839     40     no | SINK   SINK   -            -          -
```

Read naively, FLOW looks like a win on spices: Genoa, Beijing and Canton all become sinks and
Saxony stops being one. That reading is wrong, for two reasons.

- **Under FLOW, 33 of 80 nodes are spices sinks.** When 41% of the map is a sink, "Genoa is a
  sink" carries almost no information.
- **It is not consistent.** For cloves, Genoa — demand rank **2** — is *not* a sink, while Safi at
  rank 40 *is*. Canton at rank 6 is not; Beijing at rank 12 is. The pattern tracks routing
  topology, not demand, exactly as under the Laplacian.

---

## 3. Safi ↔ Sevilla, per good, both operators

`safi` has degree 2 (`timbuktu`, `sevilla`), so this edge is a clean test.

```
LAP vs FLOW on this edge, over 29 goods:
  ('sevilla->safi', 'sevilla->safi') : 17
  ('safi->sevilla', 'safi->sevilla') :  4
  ('safi->sevilla', 'unoriented')    :  7
  ('sevilla->safi', 'unoriented')    :  1
```

**On all 21 goods where FLOW commits, it agrees with the Laplacian. Zero disagreements.** On the
other 8 it is silent.

Both operators get the economics right, and for the same reason: where Safi has real supply the
edge points out of Safi, and where it has none it points in.

```
good        s(safi)    c(safi)   LAP             FLOW
sugar       0.144330   0.011037  safi->sevilla   safi->sevilla
cloth       0.026243   0.011037  safi->sevilla   safi->sevilla
grain       0.020290   0.011179  safi->sevilla   safi->sevilla
wool        0.014493   0.011179  safi->sevilla   safi->sevilla
iron        0.000000   0.011037  sevilla->safi   sevilla->safi
silk        0.000000   0.010500  sevilla->safi   sevilla->safi
spices      0.017467   0.011037  safi->sevilla   unoriented
```

The TREE baseline, by contrast, returns `safi->sevilla` for 22 of 29 goods regardless of whether
Safi produces the good — including `iron`, `silk`, `fur` and `tea`, where Safi's supply is exactly
zero. Its subtree totals are dominated by whatever else hangs below Safi in the chosen tree.

---

## 4. The Cape of Good Hope

`cape_of_good_hope` — degree 4, neighbours `malacca`, `comorin_cape`, `zanzibar`, `ivory_coast` —
holds **zero owned provinces** at 1444.11.11, so `s_raw = 0` and `c = 0` for every good. It is the
only true conduit on the map.

```
good        s_targ(=eps)    in   out   transit inflow   transit/eps
spices         1.000e-06     1     2        2.430e-01      242,959
cloves         1.000e-06     1     2        4.476e-01      447,581
silk           1.000e-06     1     1        1.386e-01      138,553
sugar          1.000e-06     1     3        8.309e-02       83,092
cloth          1.000e-06     2     1        1.021e-01      102,094
```

**Yes, it is a conduit under both operators** — in-degree and out-degree both nonzero — and
**its transit flow dominates its own ε by five orders of magnitude** (2.4×10⁵ for spices). The ε
is doing no work here whatsoever; the routing is.

### CORRECTION (this section was wrong; corrected against measurement)

An earlier version of this section claimed that min-cost flow *severs* the §3.2
Malacca → … → Cape → … → Europe corridor, "because the Cape route costs more hops." **Both the
claim and its stated reason are false.** The hop counts, measured on the undirected adjacency:

```
malacca -> english_channel :  3 hops via the Cape   |  7 hops via Alexandria
malacca -> sevilla         :  3 hops via the Cape   |  7 hops via Alexandria
malacca -> champagne       :  4 hops via the Cape   |  6 hops via Alexandria
malacca -> genua           :  5 hops via the Cape   |  5 hops via Alexandria   (tie)
malacca -> venice          :  5 hops via the Cape   |  5 hops via Alexandria   (tie)
```

**The Cape route is never longer, and to Atlantic Europe it is less than half the length.** The
reason is `ivory_coast`, which has degree 8 (`kongo`, `cape_of_good_hope`, `brazil`, `timbuktu`,
`carribean_trade`, `bordeaux`, `english_channel`, `sevilla`) and links the Cape straight into
Atlantic Europe.

And min-cost flow *uses* that corridor — heavily. Actual net flows on the Cape's four edges:

```
spices:  malacca -> cape 0.242959 | cape -> ivory_coast 0.234248 | cape -> zanzibar 0.008712
cloves:  malacca -> cape 0.447581 | cape -> ivory_coast 0.350077 | cape -> zanzibar 0.097504

share of world supply transiting each hub, FLOW:
good            thru cape   thru alexandria
spices           0.242959          0.136698
cloves           0.447581          0.059394
silk             0.138553          0.114717
sugar            0.083091          0.007989
tea              0.281607          0.032698
cotton           0.119004          0.134182
```

`malacca -> cape_of_good_hope` is the **single largest spice artery in the solution**, carrying 24%
of world supply, and the Cape outcarries Alexandria for five of the six goods sampled. Nor does the
Cape "carry flow only into Africa": `cape -> ivory_coast` moves 0.234 of world spice supply into
the Atlantic system that feeds the Channel, Sevilla and Bordeaux.

The one true observation was that there is no directed FLOW path `cape -> genua` for spices. That
is not the corridor being severed — it is Genoa being a *sink fed from the Mediterranean side*:

```
genua's incident spice flows: alexandria -> genua 0.032965 | tunis -> genua 0.002111
                              ragusa, champagne, valencia: zero
```

Genoa takes a 0.033 trickle via Alexandria while the Cape artery serves Atlantic Europe on a
different branch. Both are live. Absence of a `cape -> genua` path is not absence of a Cape
corridor.

**On this test FLOW is better than the Laplacian, not worse.** LAP's own `malacca -> genua` path
(`malacca -> ganges_delta -> comorin_cape -> gulf_of_aden -> alexandria -> genua`) does not touch
the Cape at all, while FLOW routes a quarter of world spice supply through it. §3.2's corridor is
handled *more* faithfully by the candidate than by the incumbent.

The LP is deterministic here — six identical solves returned one distinct orientation and identical
cost (spices 2.351052, cloves 4.064407) — so this is a straightforward error on my part, not a
sampling artefact of a degenerate optimum.

The verdict on FLOW is unchanged, but it now rests only on §0 (49.7% edge coverage) and §7
(cyclic aggregate), both of which are structural and independently verified. The corridor argument
is withdrawn.

---

## 5. Acyclicity

```
LAP            non-acyclic goods:  0/29
FLOW           non-acyclic goods:  0/29
bfs@malacca    non-acyclic goods: 26/29
bfs@genua      non-acyclic goods: 29/29
dfs@saxony     non-acyclic goods: 27/29
```

- **LAP**: acyclic because φ is a potential.
- **FLOW**: acyclic, and this is a *theorem*, not a repair. With every arc cost equal to 1, a
  positive-flow directed cycle could be cancelled to strictly lower cost, so no optimum contains
  one. Cycles found in the raw LP net flow before cancellation, summed over all 29 goods: **0**.
  The cycle-cancellation routine is implemented (`cancel_cycles`, minimum-flow cancellation around
  each detected cycle) and never fired.
- **TREE**: cycles in 26–29 of 29 goods, for all three spanning trees. Examples:

```
bfs@malacca  cloves    : patagonia -> laplata -> cuiaba -> patagonia
bfs@genua    cloth     : canton -> gulf_of_siam -> malacca -> canton
dfs@saxony   cloth     : samarkand -> siberia -> girin -> beijing -> yumen -> samarkand
```

The non-tree edges are the culprit: orienting them by comparing endpoint subtree totals is not
derived from any single consistent ordering, so it closes cycles against the tree edges.
**Acyclicity is non-negotiable, so the cheap baseline is disqualified outright** — no amount of
stability would rescue it.

### Zero net flow — how it is handled

Primary handling: **such an edge gets no orientation**, which is what the coverage figure reports.
I also tested the natural repair, since the LP hands it to us free. Complementary slackness gives
`π(v) − π(u) = 1` on flow-carrying arcs and `≤ 1` elsewhere, so the duals are a potential:

```
spices: zero-flow edges the dual can orient: 46 ; still tied: 34
combined (flow + dual) orientation covers 125 of 159 edges; acyclic: yes
```

Better, but still 34 edges (21%) unorientable, and it does not help the substance — see §7 for
what the dual actually is.

---

## 6. Sinks per good, and regional sinks surviving

```
operator              min        max  goods with >1       mean
LAP                     1          7          24/29        3.5
FLOW                   26         39          29/29       32.1
bfs@malacca             4         14          29/29        7.5
bfs@genua               5         13          29/29        8.4
dfs@saxony              4         12          29/29        8.6
```

All three keep multiple sinks for most goods, so on the letter of the requirement all three pass.
But **FLOW's 26–39 sinks per good is not "regional sinks surviving", it is the sink concept
ceasing to discriminate** — 33 to 49% of all nodes. LAP's range of 1–7, with 24 of 29 goods
keeping more than one, is the only result where a sink is a distinguished node.

The one place LAP is weakest is the 5 goods with a unique sink (spices among them). That is a real
shortcoming and it is what prompted this test — but neither candidate fixes it in a usable way.

---

## 7. Does `Φ = Σ_g V_g φ_g` still mean anything?

**Plainly: under FLOW there is no `φ_g`, so the §1.6 aggregate as written does not exist.**
Orientation comes from a per-edge quantity, not a per-node scalar. Two candidate replacements
were tested:

**(a) Value-weighted net flow, `F(e) = Σ_g V_g · net_g(e)`.** This is the natural aggregate — and
it is **not acyclic**:

```
aggregate flow orients 159 of 159 edges
aggregate flow acyclic: NO -> ganges_delta -> malacca -> gulf_of_siam -> burma -> ganges_delta
```

A sum of flows is a flow, and flows circulate. Each per-good flow is acyclic because it is
*optimal* for its own good, but the value-weighted sum is not optimal for anything, so nothing
prevents a circulation. This breaks §2.4 (the emitted file must be a DAG) and C672 (acyclicity is
what makes an installable single network exist). It is a full stop, not a wrinkle.

**(b) Value-weighted duals, `Σ_g V_g·(−π_g)`.** This *is* acyclic, and per good the dual
reproduces the flow orientation exactly:

```
flow arcs u->v with pi(v) > pi(u): 79 of 79   -> pi increases along flow
orient(-pi) agrees with flow on 79 of 79 flow-carrying edges
sum_g V_g (-pi_g) acyclic: yes
```

So a Φ-analogue does survive — but look at what it is:

```
pi (shifted to min 0) vs hop distance to nearest spices source:
  hops   nodes    mean pi
  0         18   2.722222
  1         29   3.689655
  2         18   4.666667
  3         12   5.916667
  4          3   5.666667
spearman(pi, hops) = 0.6097
```

**The min-cost-flow dual is graph distance from the source set.** With unit arc costs it could not
be anything else. So the candidate operator is a distance operator wearing different clothes, and
`diagnosis.md` established that the problem *is* distance-driven placement. It cannot cure the
disease it has.

---

## 8. Uncolonised nodes

```
nodes with zero owned city provinces at 1444.11.11: ['cape_of_good_hope']
```

**One node.** And the set of nodes with `c = 0` is identical for all 30 goods — also just
`cape_of_good_hope`. This is the entire population the targeted-ε rule was written for.

**(a) Do all its incident edges point outward, for every good?** No.

```
cape_of_good_hope  LAP  : all-outward for  0/29 goods ; any inflow 29/29 ; unoriented 0
cape_of_good_hope  FLOW : all-outward for  2/29 goods ; any inflow 27/29 ; unoriented 40
```

**(b) Does any good flow into one?** Yes — 29 of 29 goods under LAP, 27 of 29 under FLOW.

### The ε change does not work, and its premise is false

The brief's rationale was: *"an empty node with a little supply and no demand has something that
must leave and nothing that can arrive, so its edges point outward by conservation rather than by
tie-break."*

That is true only for a node that is empty **and a graph leaf**. `cape_of_good_hope` has degree 4
and sits on the Malacca–Africa–Europe corridor, so conservation does not point its edges outward —
it makes it a through-route. Its ε is 1×10⁻⁶ and its transit flow is 2.4×10⁻¹, a ratio of
**242,959:1**. The ε is invisible to its own orientation.

So the targeted ε is a **no-op with a false premise on this map**: one affected node, and on that
node it is swamped. It does no harm, and the intent it encodes would matter on a map with empty
degree-1 nodes — the vanilla map has none, since minimum degree is 2. It should not be adopted on
the strength of this test.

---

## Cheap baseline: how much does the spanning tree matter?

```
comparison                     same dir   opposite     % same
bfs@malacca vs bfs@genua           2822       1789      61.2%
bfs@malacca vs dfs@saxony          2923       1688      63.4%
bfs@genua   vs dfs@saxony          2922       1689      63.4%

LAP vs bfs@malacca                 3081       1530      66.8%
LAP vs bfs@genua                   2924       1687      63.4%
LAP vs dfs@saxony                  2897       1714      62.8%
```

**It changes a great deal — 37 to 39% of edge-good orientations flip on the choice of root.** The
sink sets are essentially unrelated between trees:

```
bfs@malacca : ohio 26, mexico 23, lima 23, kongo 20, katsina 17
bfs@genua   : the_moluccas 23, novgorod 21, kongo 20, doab 18, hangzhou 18
dfs@saxony  : ohio 26, kongo 20, timbuktu 17, north_sea 17, bordeaux 17
```

The brief's condition was "if it barely changes, the cheap version wins." It does not barely
change, and it is cyclic for 26–29 of 29 goods. **The cheap version loses on both counts.**

---

## What breaks

### Goods produced almost everywhere (grain, livestock)

Is `s − c` dominated by tiny differences, and does orientation look arbitrary? **No, on both
counts** — this worry does not survive measurement.

```
good           srcs     max|s-c|  median|s-c|   frac<1e-3   LAP sinks
grain            64    3.626e-02    4.957e-03       15.0%           5
livestock        49    4.495e-02    6.476e-03       12.5%           3
cloth            50    9.986e-02    6.734e-03       12.5%           4
spices           18    2.864e-01    1.143e-02       10.0%           1
cloves            1    9.805e-01    7.859e-03       17.5%           3
```

Grain's median `|s − c|` is 5.0×10⁻³ against a max of 3.6×10⁻², and only 15% of nodes fall inside
10⁻³ — barely more than the 10% for spices. Widely-produced goods are not degenerate; they are
just flatter.

Stability under a ±1% per-province wealth perturbation, 5 seeds:

```
good          LAP flips/159     FLOW flips   sink set changes
grain                   0.0            0.0            0/5
livestock               0.0            0.0            0/5
spices                  0.0            0.0            0/5
cloves                  0.0            0.0            0/5
```

**Zero edges flip, for any good, under either operator.** Orientation is not knife-edge with
respect to input noise. This is consistent with `diagnosis.md`: independent ±1% per-province noise
averages out across the 20–77 provinces in a node, so node-level `c` barely moves. It takes a
*systematic* shift — the 1.72× of the D analysis — to move anything. Per-province precision is not
the lever; per-node bias is.

### Any node that is a sink despite having supply and no demand

```
(good, operator, node) triples where a sink has s>0 and c==0: 0
```

**Vacuous, not passing.** Only `cape_of_good_hope` has `c = 0`, and it has `s_raw = 0` for every
good, so the pathological combination cannot arise on this dataset. Reporting it as a pass would
overstate the test.

The near-version is meaningful and both operators are clean:

```
sinks that are net SOURCES of their good (s > c, yet no outgoing edge):
  LAP  : 0 of 102 sink pairs
  FLOW : 0 of 930 sink pairs
```

No node is ever a sink for a good it net-produces, under either operator.

### Conduits

```
cape_of_good_hope (s=0, c=0, degree 4):
  LAP  : passes flow through (in>0 and out>0) for 29/29 goods ; terminates it 0/29
  FLOW : passes flow through for 27/29 goods ; terminates it 0/29
```

**Both operators pass flow through a conduit rather than terminating it**, which is what §3.2
requires (C376–C378). LAP does it for every good; FLOW for 27 of 29, with the other 2 unoriented
rather than terminated. This is the one requirement both candidates and the incumbent satisfy.

---

## Conclusion

**Both candidates are worse than the Laplacian. Neither should be adopted.**

| | LAP | FLOW | TREE |
|---|---|---|---|
| orients all 159 edges | **yes** | **no — 49.7%** | yes |
| acyclic per good | **yes** | yes (theorem) | **no — 26–29 of 29 goods** |
| acyclic aggregate | **yes** | **no** (net flow); yes via duals | not tested — disqualified |
| demand reachable from supply | **100.0%, 29/29 goods** | **100.0%, 29/29 goods** (theorem) | not tested |
| orphan sinks | **0 of 102** | **0 of 930** | not tested |
| sinks correlate with demand | weakly, correct sign (−0.103) | **anti-correlated (+0.132)** | ~none |
| sinks per good | 1–7 | 26–39 | 4–14 |
| §3.2 Cape corridor | not used at all | **used — 24% of spice supply** | not tested |
| §1.6 `Φ` survives | **yes** | only as value-weighted distance | n/a |
| stable to input noise | yes | yes | 37–39% flips on root choice |

**Reachability, added after the fact.** The metric introduced in `ranked-orientation.md` was never
applied to FLOW. It has been now, and FLOW **ties the Laplacian at a perfect 100.0% of demand
reachable on all 29 goods, with 0 orphan sinks out of 930.** That is not luck and I should have
predicted it: the LP imposes `inflow − outflow = c − s` at every node, so every unit of demand is
served *by construction*. Demand satisfaction is an LP feasibility theorem for this operator, not
an empirical finding. RANK (83.3%) and BASIN (88.5%) both fail this test; FLOW does not.

So FLOW is a stronger candidate than the first version of this document allowed. What actually
disqualifies it is narrower than I claimed: **it orients only half the edges, and its
value-weighted aggregate is cyclic.** Both are hard structural failures for generating a
`00_tradenodes.txt`, and both are independently verified. The rest of the case against it — the
sink statistics — is a quality complaint, not a disqualification.

The distance observation still stands on its own terms: **a min-cost flow with unit arc costs is a
distance operator.** Its dual is graph distance from the source set (ρ = 0.61 against hop count)
and its sinks are the leaves of a shortest-path arborescence, which is why its sink placement is
anti-correlated with demand. But note the limit of that argument, which the corrected §4 exposes:
being a distance operator did *not* stop it from serving all demand, and did not stop it from using
the Cape corridor better than the incumbent does.

If the goal remains putting sinks at demand, the evidence from both documents points at the
**headroom** term — the local spread of the field — which is what `diagnosis.md` §6 option 1
(weighted Laplacian) and option 2 (screened Poisson / mass term) attack. Unit-cost flow attacks
neither; it replaces the potential with a distance and keeps the topology in charge.

One correction to `diagnosis.md` worth carrying forward: the Laplacian's sinks *are* modestly
demand-correlated — 9.0% top-decile against 0.7% bottom-decile enrichment — and that is the best
demand tracking of any operator tested here. The problem identified in `diagnosis.md` stands, but
the incumbent is a stronger baseline than that document implied.
