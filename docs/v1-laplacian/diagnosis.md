# Diagnosis — why sink locations do not track the demand distribution

**Subject.** The reference solver (`scratchpad/v/solver.py`) places the sole spices sink at
`saxony` on the 1444.11.11 dataset, and `safi` is the most frequent sink overall (12 of 29
goods). No node containing a top-development province is a spices sink. This document
diagnoses why.

**Constraints observed.** Wealth inputs were not improved. `validation.md` was not rerun. No
input, exponent or ε was tuned at any point.

---

## 1. Pre-registration (written and committed to disk before any instrumentation was run)

Derived from spec §1.2–§1.4 only:

```
s(n,g) = goods_produced(n,g) / Σ_m goods_produced(m,g)
s     ← (1 − ε)·s + ε/N
wealth(p) = tax_income(p) + production_income(p)
c(n,g) = Σ_{p ∈ n} wealth(p)^α(g)  /  Σ_{q ∈ world} wealth(q)^α(g)
α(spices) = (price/P₀)^k = (3.0 / 2.0)^1 = 1.5
```

The solver's proxy for the two income terms is
`wealth(p) = base_tax(p) + 0.2 · base_production(p) · base_price(good(p))`.
This is **not** development: `base_manpower` contributes nothing, which is correct for an income
measure, and production is discounted roughly 2:1 against tax at typical prices. So the "top
development" list in the anomaly statement is not the ranking that drives `c`.

### 1.1 Hand-computed province wealths (top provinces of the seven named nodes)

| Province | node | tax | prod | good (price) | wealth | wealth^1.5 |
|---|---|---|---|---|---|---|
| Beijing | beijing | 13 | 13 | grain (2.5) | 19.5 | 86.1 |
| Canton | canton | 12 | 12 | incense (2.5) | 18.0 | 76.4 |
| Venezia | venice | 10 | 12 | glass (3.0) | 17.2 | 71.3 |
| Genoa | genua | 10 | 10 | paper (3.5) | 17.0 | 70.1 |
| Firenze | genua | 10 | 12 | wine (2.5) | 16.0 | 64.0 |
| Roma | genua | 9 | 9 | paper (3.5) | 15.3 | 59.9 |
| Ile-de-France | champagne | 8 | 8 | paper (3.5) | 13.6 | 50.2 |
| Prague | saxony | 8 | 8 | cloth (3.0) | 12.8 | 45.8 |
| Milan | genua | 8 | 7 | cloth (3.0) | 12.2 | 42.6 |
| Al-Djazair | safi | 5 | 5 | grain (2.5) | 7.5 | 20.5 |

### 1.2 Committed prediction — Σ_p wealth^1.5 per node, and c(spices)

Node totals estimated from the top-7 provinces exactly plus the remaining provinces at the
node's residual average. World denominator estimated at ≈ 3.2 × 10⁴.

| Rank | Node | predicted Σ w^1.5 | predicted c(spices) |
|---|---|---|---|
| 1 | `genua` | ≈ 910 | ≈ 0.028 |
| 2 | `champagne` | ≈ 719 | ≈ 0.022 |
| 3 | `canton` | ≈ 580 | ≈ 0.018 |
| 4 | `venice` | ≈ 538 | ≈ 0.017 |
| 5 | `beijing` | ≈ 445 | ≈ 0.014 |
| 6 | `saxony` | ≈ 403 | ≈ 0.013 |
| 7 | `safi` | ≈ 290 | ≈ 0.009 |

**Committed rank order:** `genua` > `champagne` > `canton` > `venice` > `beijing` > `saxony` > `safi`.

**Committed ratios:** c(genua)/c(safi) ≈ **3.1**; c(genua)/c(saxony) ≈ **2.3**;
c(saxony)/c(safi) ≈ **1.4**.

### 1.3 The load-bearing part of the prediction

`saxony` is predicted **sixth of seven** — second lowest. `safi` is predicted **last**.

The discriminating decision rule, committed in advance:

- **If the solver's `c` roughly matches this table**, then `c` is computed to spec, `saxony` is
  not the highest-demand node, and its sinkhood is *not* caused by demand magnitude. The cause
  must be elsewhere → discriminator **C** (or D).
- **If the solver's `c` is inverted** (saxony and safi high, genua low), that is an
  implementation bug → **A** or **B**.
- **If the solver's `c` is flat** across nodes (all ≈ 1/80 = 0.0125), the α exponent is not
  being applied per province → **B**.

Secondary pre-registered expectation: because α = 1.5 > 1 rewards individually rich provinces
and `saxony` is fragmented (35 provinces, largest wealth 12.8) while `genua` is both larger in
total and top-heavy, **node-level α would help `saxony` relatively less than it helps `genua`**.
So a node-level-α bug (B) would not by itself explain a `saxony` sink either. I expect B to be
ruled out.

---

## 2. Prediction vs actual

Actual values from `build_sc()` on the 1444 dataset, α(spices) = 1.5:

| Node | pred Σw^1.5 | actual Σw^1.5 | pred c | actual c | actual/pred |
|---|---|---|---|---|---|
| `genua` | 910 | 866.1 | 0.0280 | 0.035076 | 1.25 |
| `champagne` | 719 | 704.7 | 0.0220 | 0.028540 | 1.30 |
| `canton` | 580 | 495.6 | 0.0180 | 0.020070 | 1.12 |
| `venice` | 538 | 513.0 | 0.0170 | 0.020775 | 1.22 |
| `beijing` | 445 | 371.2 | 0.0140 | 0.015031 | 1.07 |
| `saxony` | 403 | 436.2 | 0.0130 | 0.017666 | 1.36 |
| `safi` | 290 | 272.5 | 0.0090 | 0.011037 | 1.23 |

- Predicted order: `genua` > `champagne` > `canton` > `venice` > `beijing` > `saxony` > `safi`
- Actual order: `genua` > `champagne` > `venice` > `canton` > `saxony` > `beijing` > `safi`

Two adjacent transpositions (canton↔venice, saxony↔beijing). Ratios: predicted
c(genua)/c(safi) 3.1, **actual 3.178**; predicted c(genua)/c(saxony) 2.3, actual 1.986;
predicted c(saxony)/c(safi) 1.4, actual 1.601. The uniform ~1.25× on the absolute values is my
world-denominator estimate (32000 vs actual **24692.67**), not a discrepancy in `c`.

**The load-bearing prediction is confirmed.** `saxony` is not the highest-demand node — it has
**half** of `genua`'s demand (0.0177 vs 0.0351). Per the pre-registered decision rule, the cause
is **C** or **D**, not A or B.

---

## 3. Instrumentation

### Item 1 — balance, per component per good

The graph is a single component of 80 nodes. `solver.solve_phi()` contains `rhs -= rhs.mean()`,
which *forces* balance, so the meaningful residual is the one measured **before** that line.
Both are reported.

```
spices  comp0 (80 nodes): residual BEFORE mean-subtraction = 1.110e-16 ; AFTER = 5.551e-17
worst residual over all 29 live goods x 1 component: -2.914e-16  (livestock)
renormalisation factor actually applied (b.mean()*N) for spices: 2.776e-17
```

ε ordering: `build_sc()` computes `S = gp/world` and *then* `S = (1-eps)*S + eps/N`, i.e.
**ε is applied after normalisation**, and it preserves the sum exactly since
`(1-eps)·1 + N·(eps/N) = 1`. Measured `sum_n s(n,spices) = 0.99999999999999978`.

**The solve is consistent.** The mean-subtraction is a no-op at 2.8e-17. Nothing downstream is
an artifact of imbalance.

### Item 4 — index sets

```
ROWS (provinces entering BOTH s and c): 2452
filter: owner set AND is_city=='yes' AND province is a member of some node
owned city provinces NOT in any node: 0
sum_n s(n,spices) = 0.99999999999999978
sum_n c(n,spices) = 1.00000000000000000
```

`s`'s numerator and denominator are both sums over `ROWS`; `c`'s numerator and denominator are
both sums over `ROWS`. **Same index set, no scale mismatch.** Zero owned city provinces sit
outside a node, so the spec's `Σ_{q∈world}` and the implementation's index set coincide exactly
on this dataset.

### Item 3 — per-province vs node-level exponent

```
per-province  sum_p w^a :  c(genua)=0.03507643  c(safi)=0.01103738  ratio = 3.177967
node-level  (sum_p w)^a :  c(genua)=0.03627694  c(safi)=0.00923562  ratio = 3.927939
solver's C[spices]      :  c(genua)=0.03507643  c(safi)=0.01103738  ratio = 3.177967

max |solver - per-province| = 3.123e-17
max |solver - node-level|   = 9.733e-03
```

**The implementation matches per-province `Σ_p wealth^α`, per spec §1.3.** The two forms are
distinguishable at 9.7e-3 and the solver sits on the correct one to machine precision.

### Item 2 — the spices field

Raw denominators: `Σ_m goods_produced(m,spices) = 45.800000`;
`Σ_q wealth^1.5 = 24692.668992`; per-component renormalisation factor `b.mean() = 3.469e-19`.

Top and bottom of the field, sorted by φ descending (full 80-row dump is the `diag.py` output):

| node | s | c | s−c | φ | deg | out | in |
|---|---|---|---|---|---|---|---|
| `the_moluccas` | 1.616e-01 | 1.715e-02 | 1.444e-01 | **+0.172718** | 3 | 3 | 0 |
| `malacca` | 3.144e-01 | 2.803e-02 | 2.864e-01 | +0.148035 | 6 | 5 | 1 |
| `philippines` | 5.677e-02 | 6.516e-03 | 5.025e-02 | +0.121425 | 3 | 2 | 1 |
| `gulf_of_siam` | 1.250e-08 | 2.855e-02 | −2.855e-02 | +0.105828 | 3 | 2 | 1 |
| `canton` | 1.250e-08 | 2.007e-02 | −2.007e-02 | +0.101872 | 5 | 2 | 3 |
| `cape_of_good_hope` | 1.250e-08 | **0.000e+00** | +1.250e-08 | +0.061776 | 4 | 2 | 2 |
| `beijing` | 1.250e-08 | 1.503e-02 | −1.503e-02 | +0.034915 | 4 | 2 | 2 |
| … | | | | | | | |
| `genua` | 1.250e-08 | **3.508e-02** (highest in game) | −3.508e-02 | −0.058464 | 5 | 2 | 3 |
| `venice` | 1.250e-08 | 2.077e-02 | −2.077e-02 | −0.067475 | 3 | 1 | 2 |
| `champagne` | 1.250e-08 | 2.854e-02 | −2.854e-02 | −0.068307 | 4 | 1 | 3 |
| `rheinland` | 1.250e-08 | 2.637e-02 | −2.637e-02 | −0.087782 | 4 | 1 | 3 |
| **`saxony`** | 1.250e-08 | 1.767e-02 | −1.767e-02 | **−0.089590** | 4 | **0** | 4 |

`argmin φ = saxony (−0.089590)`; `argmax φ = the_moluccas (+0.172718)`; range **0.262307**.

Two rows settle the question on their own:

- **`cape_of_good_hope` has c = 0.000000** — literally zero demand, because it holds zero owned
  provinces at 1444.11.11 — and its φ = +0.061776 places it **above 66 of the 80 nodes**. A node
  with no demand whatsoever outranks Genoa, Venice, Champagne and Beijing.
- **`genua` has the highest demand in the game** (0.035076) and is not a sink.

φ is not ordering nodes by demand.

### Item 5 — every sink of every live good

102 (good, sink) pairs across 29 live goods.

```
n=102 | mean degree 3.12 (all-node mean 3.98) | mean wealth rank 30.5 of 80 | mean hops 2.28
degree distribution of sinks: {3: 50, 2: 24, 4: 20, 5: 8}
hops distribution of sinks:   {2: 29, 1: 23, 3: 15, 4: 14, 0: 12, 5: 4, 6: 4, 7: 1}
sink frequency: safi 12, gulf_of_siam 11, saxony 7, the_moluccas 7, doab 6,
                african_great_lakes 4, valencia 4, venice 3, hangzhou 3, champagne 3
spices/saxony: deg 4, wealth rank 21, hops-to-source 3
max hops from any node to nearest spices source: 4
```

Three facts here **contradict the naive graph-distance story** and must be stated plainly:

- `saxony` is at **3** hops from a spice source, and the maximum over all nodes is **4**. It is
  *not* the graph-farthest node.
- **12 sink pairs are at hops = 0** — the sink *is* a producer of that good (e.g. `iron` sinks
  at `the_moluccas`, `livestock` at `safi`).
- `gulf_of_siam` is the second most frequent sink (11 goods) and is the **second-richest node in
  the game** by wealth rank. High demand is not disqualifying.

So "sinks land graph-farthest from sources" is the wrong mechanism. The right one is local.

---

## 4. The mechanism

Row `n` of `L φ = s − c` is `deg(n)·φ(n) − Σ_{m~n} φ(m) = s(n) − c(n)`, so exactly:

```
φ(n) = mean(neighbour φ)  +  (s(n) − c(n)) / deg(n)
```

`n` is a sink iff φ(n) is below *every* neighbour, not merely below their mean. Therefore:

```
      (c(n) − s(n)) / deg(n)   >   mean(nbr φ) − min(nbr φ)
      \__________________/         \___________________/
            "drive"                     "headroom"
```

**Tested on every (good, node) pair: the criterion classifies sinkhood with accuracy 1.000
(2320/2320), zero violations.** Neither term alone exceeds 0.957.

Demand therefore enters in exactly two degraded ways: **divided by degree**, and **only in
comparison to the local spread of the field**. It never competes on its own magnitude.

### 4.1 Genoa versus Saxony, head to head

```
genua   c=0.035076 s=0.000000 deg=5  drive=0.007015  headroom=0.016858  margin=-0.009843
    neighbours: alexandria -0.029179, tunis -0.043425, valencia -0.049740,
                ragusa -0.066591, champagne -0.068307
saxony  c=0.017666 s=0.000000 deg=4  drive=0.004417  headroom=0.002609  margin=+0.001808  SINK
    neighbours: lubeck -0.080986, wien -0.085879, krakow -0.086045, rheinland -0.087782
canton  c=0.020070 s=0.000000 deg=5  drive=0.004014  headroom=0.039165  margin=-0.035151
    neighbours: malacca +0.148035, philippines +0.121425, gulf_of_siam +0.105828,
                chengdu +0.087421, hangzhou +0.066720
safi    c=0.011037 s=0.017467 deg=2  drive=-0.003215 headroom=0.004174  margin=-0.007389
```

Genoa's **drive is 1.59× Saxony's**. Genoa's **headroom is 6.46× Saxony's**. Headroom wins.

Genoa sits mid-gradient on the live spice corridor: its neighbours span 0.039 of φ, from
Alexandria at −0.029 down to Champagne at −0.068. To be a local minimum it would have to
undercut Champagne, two hops further from the source. Saxony's neighbours span 0.0068 — the far
field has levelled out, so a small drive suffices.

Canton is the extreme case: adjacent to Malacca at φ = +0.148, giving headroom 0.0392. It cannot
be a spice sink at any realistic demand. `safi` is not a spices sink at all because it
*produces* spices — its drive is negative.

Note the knife-edge: Saxony's winning margin is **0.001808 against a field range of 0.262307 —
0.69%**. Rheinland's margin is exactly **−0.001808**; the two are neighbours, locked together,
and the sink is decided by a hair. This is directly why discriminator D turns out to be live.

### 4.2 The required demonstration — φ along a real graph path

The path Malacca → Alexandria → Genoa → Saxony, resolved into actual graph edges:

```
full path (8 hops): malacca -> ganges_delta -> comorin_cape -> gulf_of_aden
                    -> alexandria -> genua -> champagne -> rheinland -> saxony

hop  node                     phi      delta phi   monotone?
0    malacca             0.148035
1    ganges_delta        0.092918     -0.055117    yes
2    comorin_cape        0.079611     -0.013306    yes
3    gulf_of_aden        0.025265     -0.054346    yes
4    alexandria         -0.029179     -0.054444    yes
5    genua              -0.058464     -0.029285    yes
6    champagne          -0.068307     -0.009843    yes
7    rheinland          -0.087782     -0.019475    yes
8    saxony             -0.089590     -0.001808    yes

strictly decreasing at every hop: True
total drop malacca -> saxony: 0.237624 over 8 hops
```

Strictly monotone at all 8 hops, as required. Note the step sizes: the drop per hop *shrinks*
toward the end (−0.0551 early, −0.0018 at the last hop). The field is steep near the source and
flat at the far end — that is the headroom gradient, seen directly.

### 4.3 Why the far field wins

```
supply s(spices): 18 of 80 nodes hold 0.999999 of the mass.
  max s = 3.1441e-01 (malacca) ; non-source s = 1.25e-08 (the eps/N floor)
  supply contrast = 2.515e+07
demand c(spices): max = 3.5076e-02 (genua) ; min = 0 (cape_of_good_hope)
  contrast among nodes with nonzero demand = 471.5, and ~3x across the populated majority

hops  nodes    mean phi   phi spread   mean headroom   sinks
0        18    0.047876     0.216143        0.024592   -
1        29    0.014416     0.173302        0.029709   -
2        18   -0.022369     0.120794        0.022110   -
3        12   -0.059736     0.084134        0.011265   saxony
4         3   -0.053453     0.077507        0.003593   -
```

Mean headroom falls from 0.0246–0.0297 in the near field to **0.0036** at 4 hops. Graph distance
matters, but only through this — it flattens the field, lowering the bar a node must clear. That
is why `saxony` at 3 hops beats the three nodes at 4 hops: those have even lower headroom but
far lower demand.

**The root asymmetry: supply contrast is 2.5×10⁷ and demand contrast is ~10²–10³.** The RHS
`s − c` is dominated by the supply spikes, so the potential's shape is set by supply geometry and
demand only perturbs it.

### 4.4 Counterfactuals isolating the cause

```
CF1  real supply, UNIFORM demand (c = 1/80 everywhere)
     baseline sinks : ['saxony']
     uniform-demand : ['patagonia','amazonas_node','saxony','baltic_sea','white_sea','valencia']
     rank correlation of phi(real c) vs phi(uniform c) = 0.945710
     max |phi_real - phi_uniform| = 0.049210 against a phi range of 0.262307

CF2  UNIFORM supply (s = 1/80), real demand
     sinks: ['gulf_of_siam','hangzhou','doab','wien']
     their demand ranks: gulf_of_siam #4, hangzhou #3, doab #12, wien #14

CF3  real supply, ALL world demand concentrated at genua
     sinks: ['genua'] ; phi(genua) = -0.390349
```

These are decisive, and CF2 names the cause precisely:

- **CF1**: delete demand variation entirely and `saxony` is *still* a sink. Its sinkhood owes
  nothing to its own demand. The field is 94.6% rank-preserved by supply geometry alone.
- **CF2**: spread supply evenly and **three of the four sinks are top-12 demand nodes**. The
  model *is* capable of putting sinks at demand — it is the supply concentration that prevents
  it.
- **CF3**: concentrate demand as hard as supply and the sink moves to `genua`. The operator is
  not broken; the two input contrasts are simply orders of magnitude apart.

### 4.5 Degree

```
degree   nodes   share   sink pairs   sink share
2            7    8.8%           24       23.5%
3           26   32.5%           50       49.0%
4           22   27.5%           20       19.6%
5           17   21.2%            8        7.8%
6+           8   10.0%            0        0.0%
```

Degree-2 nodes are 2.7× overrepresented among sinks; no node of degree ≥ 6 is ever a sink for
any good. Both criterion terms favour low degree: the drive is divided by `deg`, and fewer
neighbours means a smaller expected spread. A degree-1 node would have headroom identically 0
and would be a sink for every good it net-consumes — which is exactly claim C312, analytically
exact but vacuous here, since the vanilla map has no degree-1 node.

---

## 5. Discrimination

### A — normalisation or consistency bug: **RULED OUT**

`Σ(s−c)` per component per good is 1.110e-16 for spices and worst −2.914e-16 across all 29 live
goods, measured **before** the mean-subtraction; the correction actually applied is 2.776e-17.
ε is applied after normalisation and preserves `Σs = 1` exactly. `s` and `c` are normalised over
the identical index set (2452 provinces; zero owned city provinces excluded).

### B — node-level α instead of per-province: **RULED OUT**

The solver reproduces `Σ_p wealth^α` to 3.123e-17 and differs from `(Σ_p wealth)^α` by
9.733e-03. The two forms give c(genua)/c(safi) = 3.178 and 3.928; the solver gives 3.178. The
pre-registered secondary expectation also held: node-level α would have made `genua`
*relatively better off*, so B could never have explained a `saxony` sink anyway.

### C — structural property of the model: **CONFIRMED, and dominant**

With mechanism (§4) and demonstration (§4.2). Established by an exact criterion accurate on
2320/2320 pairs; a strictly monotone 8-hop path; and CF1, in which removing demand variation
entirely leaves `saxony` a sink.

Two corrections to the hypothesis as stated in the brief:

1. It is **not** that sinks land graph-farthest from sources. `saxony` is at 3 hops of a maximum
   4, and 12 sink pairs are at 0 hops. The mechanism is local — drive versus headroom — and
   graph distance enters only because the far field is flatter.
2. "Entry-point nodes are structurally source-side" is right for **Canton** (φ = +0.1019,
   adjacent to Malacca, headroom 0.0392) but wrong for **Venice and Genoa**, which sit at
   φ = −0.067 and −0.058, in the bottom third of the field. They are not source-side; they are
   late-gradient nodes that fail to be *local* minima only because something downstream of them
   is lower.

The honest general statement: **sinks land where the field is locally flat and the node
net-consumes; the field is flat wherever supply is far away. Demand sets which of the flat nodes
wins, and nothing more.**

### D — input precision: **LIVE, but bounded — not ruled out**

Scaling every `genua` province's income by `f` (tax and production alike):

```
f       c(genua)   phi(genua)  sinks
1.0     0.035076   -0.058464   ['saxony']
1.725   0.076084   -0.0720     ['saxony','genua']      <- genua becomes a CO-sink
2.0     0.093232   -0.078466   ['saxony','genua']
4.0     0.225294   -0.123889   ['rheinland','genua']   <- saxony ceases to be a sink
10.0    0.534783   -0.230338   ['genua']               <- genua sole sink
```

Three readings, three answers:

| Reading of "move the sink to Genoa" | required f | implied c(genua) | plausible? |
|---|---|---|---|
| Genoa becomes a co-sink | **1.725×** | 0.076 = 7.6% of world spice demand | **yes** |
| Saxony stops being a sink | ≈ **4×** | 0.225 = 22.5% at one node | no |
| Genoa is the sole sink | **10×** | 0.535 = 53.5% at one node | no |

Can autonomy and production efficiency account for 1.725×? **Yes, plausibly.** The proxy
applies neither. Autonomy multiplies income by `(1 − autonomy)`, spanning 1.00 at a stated core
down to 0.10 at the `territory_core` floor of 90% — a 10× relative swing. Genoa's provinces are
stated European cores at ~0 autonomy, so the correction raises Genoa's share not by raising its
numerator but by **cutting the world denominator** wherever provinces sit in territories.
Because `c` is a normalised share, a 30–50% average reduction in non-European income alone lifts
c(genua) by 1.4–2×. Production efficiency is 0 for everyone at 1444 tech, so it contributes
nothing at the start date, up to 2× later.

Can they account for 4× or 10×? **No.** Those require one node to hold 22.5% or 53.5% of world
demand for a single good. Autonomy can only *reduce* income relative to nominal, the reduction
is bounded at 10×, and it would have to apply to essentially the entire world outside northern
Italy.

So **D is real but cannot carry the anomaly.** Better wealth inputs can plausibly add Genoa to
the spice sink set; they cannot make demand the determinant of sink location, and they cannot
put a spice sink in China (§6).

---

## 6. The structural ceiling

Demand share each node needs to become a spices sink, by bisection on a wealth multiplier with a
full re-solve each step:

| node | deg | c now | headroom | c required | wealth × | required share of world demand |
|---|---|---|---|---|---|---|
| `saxony` | 4 | 0.017666 | 0.002609 | — | 1.00 | already the sink |
| `rheinland` | 4 | 0.026366 | 0.008399 | 0.035332 | 1.22 | 3.5% |
| `safi` | 2 | 0.011037 | 0.004174 | 0.024376 | 1.71 | 2.4% |
| `genua` | 5 | 0.035076 | 0.016858 | 0.076084 | 1.72 | 7.6% |
| `venice` | 3 | 0.020775 | 0.025329 | 0.077333 | 2.50 | 7.7% |
| `champagne` | 4 | 0.028540 | 0.026610 | 0.113585 | 2.67 | 11.4% |
| `english_channel` | 5 | 0.034122 | 0.027757 | 0.143736 | 2.83 | 14.4% |
| `sevilla` | 5 | 0.025581 | 0.019007 | 0.111539 | 2.84 | 11.2% |
| `constantinople` | 4 | 0.017984 | 0.022686 | 0.094120 | 3.18 | 9.4% |
| `beijing` | 4 | 0.015031 | 0.027584 | 0.094910 | 3.61 | 9.5% |
| `hangzhou` | 5 | 0.031560 | 0.043069 | 0.214341 | 4.12 | 21.4% |
| `canton` | 5 | 0.020070 | 0.039165 | 0.175933 | 4.77 | 17.6% |

The European entry nodes are 1.7–2.8× away. **The Chinese nodes are 3.6–4.8× away and would
need 9.5–21.4% of all world spice demand in a single node.** That is not an input-precision gap;
it is a structural ceiling imposed by their adjacency to Malacca and the Indonesian sources.

### α is not the lever

```
alpha   c(genua)   c(saxony)   c contrast   sinks
1.0     0.027997   0.017092         211.1   ['saxony']
1.5     0.035076   0.017666         471.5   ['saxony']       <- current
2.0     0.043013   0.017674        1301.3   ['saxony']
3.0     0.059570   0.016114       15009.9   ['rheinland']
4.0     0.071202   0.012911      206092.1   ['beijing','rheinland']
6.0     0.062250   0.005703      4.97e+07   ['hangzhou','baltic_sea','rheinland','genua']
8.0     0.034334   0.001790      1.38e+10   ['hangzhou']
```

Raising α *does* eventually move sinks onto rich nodes — Beijing at α = 4, Genoa at α = 6. But α
is set by price: α(spices) = (3.0/2.0)^k, so α = 8 needs **k = 5.13**, and the same k puts cloves
(price 8.0) at α = 4.0^5.13 = **1.2×10³** and grain at 3.14. `α_max` would clamp all of them and
the three-regime split of §1.4 collapses. This is C442 ("a concentration mechanism strong enough
to reshape orientation would let price fight geography for control of the graph") realised as a
measurement — and it shows C439's "α is deliberately mild" is not a taste but a constraint.

### Degree normalisation is not the lever either

```
L phi = s - c        (current)                  sinks: ['saxony']
L phi = D (s - c)    (removes the 1/deg divide) sinks: ['saxony']
```

Removing the degree division changes nothing. The headroom term, not the drive term, decides.

---

## 7. Verdict

**Mixed, C-dominant. A and B are ruled out by measurement. C is the cause. D is a real but
bounded secondary effect.**

- **A: ruled out.** Balance residual ≤ 2.9e-16 before any correction; ε applied after
  normalisation and sum-preserving; identical index sets.
- **B: ruled out.** Per-province α confirmed to 3.1e-17; node-level would have helped Genoa,
  not Saxony.
- **C: confirmed, dominant.** Sinks are local minima and the test is
  `(c−s)/deg > mean(nbr φ) − min(nbr φ)`, exact on 2320/2320 pairs. Because supply contrast
  (2.5×10⁷) exceeds demand contrast (~10²–10³) by four to five orders of magnitude, the field's
  shape is set by supply geometry; demand only chooses among nodes the geometry has already
  flattened. CF1 removes demand variation and Saxony stays a sink; CF2 flattens supply and sinks
  jump onto the top demand nodes.
- **D: live, bounded.** 1.72× on Genoa's income makes it a co-sink and is plausible from
  autonomy alone. 4× (to displace Saxony) and 10× (sole sink) require one node to hold 22.5% and
  53.5% of world demand and are not plausible. Chinese nodes need 3.6–4.8× and 9.5–21.4% share;
  unreachable.

The proxy wealth inputs are **not** what moved Milan below Saxony. Milan is in `genua`; `genua`
has the highest demand in the game and still is not a sink. Nothing about the inputs explains
that. The operator does.

Nothing was tuned. No status in `validation.md` was changed. Consequences in
`validation-delta.md`.
