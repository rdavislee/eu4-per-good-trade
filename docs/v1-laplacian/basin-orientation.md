# BASIN: peel / select / grow / orient / evaluate / refine — tested against the Laplacian

**Verdict: the best of the three candidates tested, and it still loses to the Laplacian — by
2.2× on BASIN's own objective function, after correcting a sign bug in Phase 5 and exercising γ.
Mean demand reachable 88.5% against the Laplacian's 100.0%, with 0 of 29 goods complete against
29 of 29.**

It does deliver two things nothing else has: **exact control of the sink count**, and sinks that
never land in the bottom demand decile. Those are real and worth keeping in mind.

Implemented to spec with the stated defaults. `per-good-trade-spec.md` and `validation.md`
untouched. Code: `scratchpad/v/basin.py`, `basinrep.py`, `basinrep2.py`.

---

## 0. Two bugs in the algorithm as written

Both found by implementing it literally. Neither is fatal; both change the results.

### Phase 2: seeds never expand

```
∀t ∈ SEED:  φ(t)=0; ... finalize(t); push (0, t, t)
while PQ:
    (k, v, par) = pop_min
    if finalized(v): continue          <-- every seed hits this and returns
    ...
    for u ∈ N(v) ∩ core, not finalized: push(...)
```

A seed is finalized *before* being pushed, so when it is popped the guard fires and `continue`
skips the neighbour-push loop. No seed ever expands, and the field is empty beyond SEED. Fixed by
pushing seed neighbours explicitly at initialisation (equivalently: do not finalize seeds until
popped). All results below use that reading.

### Phase 5: the μ update has the sign inverted relative to its own comment

`g` is correct. Larger `g` means a larger key increment, hence slower expansion, and `g` puts
`(1+κ⁺·max(0,bal))` in the numerator — so a **surplus** basin slows down. That matches the prose
("once it has swallowed enough supply to go net-positive it slows and cedes ground").

The μ update contradicts it:

```
μ(t) ← μ(t) · exp(−η · bal(t) / scale)    # surplus basins shrink, deficit basins grow
```

For a deficit basin `bal < 0`, so `−η·bal > 0`, so **μ increases → g increases → the basin slows
and shrinks.** The update does the opposite of its comment. Instrumented on cloves, S = 3, K = 8:

```
pass  unserved   mu(hangzhou) mu(genua)  territory: hangzhou / genua / ganges_delta
0     0.799244        1.0000    1.0000        18 / 53 / 9
2     0.799244        0.6669    1.3612        40 / 29 / 11
4     0.799244        0.4703    1.7535        59 / 11 / 10
7     0.799244        0.3597    2.0738        72 /  6 / 2
```

`genua` has `bal = −0.543` (the deficit basin) and is squeezed from 53 nodes to 6. `hangzhou`,
`bal = +0.690`, grows from 18 to 72. Territory moves by 12–32 edges per pass, so the machinery
works — it is pointed the wrong way, and **`unserved` never improves at all: 0.799244 at every
pass.**

Flipping the sign to `exp(+η·bal/scale)` helps materially:

```
mean unserved over 29 goods:  as-written 0.3941  |  sign-flipped 0.3242  |  LAP 0.1037
tea      0.5342 -> 0.2046      incense  0.6437 -> 0.3416      cloves 0.7992 -> 0.5964
```

Everything below reports the sign-flipped version, which is the algorithm's stated intent.

---

## 1. Phase 0 is a no-op on this graph

```
min degree = 2 | nodes with degree <= 1 = 0 | bridges = 0 (2-edge-connected)
=> core = 80 of 80 | pendant edges = 0 | drains D = empty
```

The EU4 trade graph has **no degree-1 node and no bridge at all**. So:

- Phase 0 peels nothing, for every good. Its exactness argument ("every removed edge is a bridge,
  flow on a tree is uniquely determined") never applies here — correct, but inert.
- `D = ∅`, so `SEED = T`, tier 1 is empty, and the tier tiebreak never fires.
- The sink accounting collapses to one row: `t ∈ T, t ∉ D` → **sinks are exactly T, and
  |sinks| = S_actual exactly.**
- The feasibility check forces `S ≥ 1`.

**Input-domain note.** The spec requires `b(v) ≠ 0`. On 1444 data `cape_of_good_hope` has
`b = 0` exactly for all 29 goods — it holds zero owned provinces. It stays in the core with
`b̃ = 0`, is excluded from the Phase 1 candidate list (which needs `b̃ < 0`), and is eligible for
the fallback pool. Nothing breaks, but the precondition is violated at one node.

---

## 2. What BASIN does better than the Laplacian

### Exact sink-count control

```
S     S_actual  sinks  unserved  acyclic  dem.reach  T (first 5)
1            1      1  0.452560     True      59.1%  genua
2            2      2  0.352453     True      69.1%  genua,rheinland
3            3      3  0.518455     True      66.7%  genua,rheinland,english_channel
5            5      5  0.500700     True      72.5%  genua,rheinland,english_channel,hangzhou,pest
13          13     13  0.461868     True      66.2%  ...
30          30     30  0.584201     True      65.1%  ...
```

`S_actual = S` for every S from 1 to 30 — the greedy independent set never runs out on this graph.
**This is the only operator tested where the sink count is a dial rather than an emergent
property.** That is a genuine capability, and also a change in kind: §1.1 has sinks emerge from
the solve, and here they are selected.

Note `unserved` is not monotone in S (best at S = 2), so S cannot be tuned toward flow quality.

### Demand correlation, and never a poor sink

At `S` = the Laplacian's own sink count for each good, like-for-like:

```
operator  sinks/g  mean rank P(sink|top10) P(sink|bot10)   rho_rank    rho_val
LAP           3.5       29.4         9.0%         0.7%     -0.103     +0.104
BASIN         3.5       16.3        19.7%         0.0%     -0.225     +0.225
(reference: RANK +0.281, FLOW -0.132 anti-correlated; all-node mean rank 40.5)
```

Better than LAP on every column. **P(sink | bottom demand decile) = 0.0%** — BASIN never once
places a sink in the poorest tenth of nodes, across 29 goods. Neither LAP (0.7%) nor RANK (1.0%)
manages that. Mean sink demand rank 16.3 against an all-node mean of 40.5.

```
LAP   most frequent sinks: safi 12, gulf_of_siam 11, saxony 7, the_moluccas 7, doab 6
BASIN most frequent sinks: malacca 15, genua 13, english_channel 9, rheinland 8, ivory_coast 6
```

### Clean on the three "what breaks" checks

```
sinks that net-produce their good : LAP 0 of 102 | BASIN 0 of 102   (RANK had 9)
cape passes through as a conduit  : LAP 29/29    | BASIN 29/29
+/-1% wealth noise, edges flipped : LAP 0.0/159  | BASIN 0.0-0.4/159, 0/5 sink-set changes
```

Acyclic for all 29 goods at every S tested, guaranteed by construction (P1 and P2 both hold).
Phase 4's conservation identity `Σ unserved == Σ stranded` holds to the last digit in every run,
which is good evidence the evaluator is implemented correctly.

---

## 3. Why it loses

### The headline numbers

```
                      defaults  sign-fixed  +gamma=1000     LAP
mean unserved           0.3941      0.3242       0.2206  0.1037
mean demand reachable    72.3%       78.0%        88.5%  100.0%
goods reaching 100%       0/29        0/29         0/29   29/29
orphan sinks           3 of 102         --           --  0 of 102
```

LAP is measured under **BASIN's own Phase 4 evaluator**, so this is the algorithm's chosen
objective on the algorithm's own terms. The incumbent wins it by 2.2× at BASIN's best
configuration and by 3.8× at the stated defaults.

Per good, at the best configuration found:

```
good             S | BASIN uns  BASIN reach |  LAP uns  LAP reach
cloves           3 |    0.6544        44.7% |   0.1037     100.0%
fur              1 |    0.3701        74.5% |   0.1684     100.0%
slaves           4 |    0.3612        79.9% |   0.1547     100.0%
incense          5 |    0.2419        89.9% |   0.0836     100.0%
spices           1 |    0.2046        96.7% |   0.0558     100.0%
tea              3 |    0.1855        84.1% |   0.0822     100.0%
cloth            4 |    0.1010        99.1% |   0.0639     100.0%
grain            5 |    0.0668        99.1% |   0.0183     100.0%
```

### Loss source 1 — basins are flow-tight compartments

Orientation is high-φ → low-φ, and φ grows outward from each seed, so **every node drains to its
own basin's seed. Supply in basin A cannot cross into basin B.** Confirmed:

```
good        S | basins  net-neg  sum|neg|  sum pos  unserved
cloves      3 |      3        2    0.6896   0.6896    0.7992
incense     5 |      5        3    0.3443   0.3443    0.6437
tea         3 |      3        2    0.3980   0.3980    0.5342
grain       5 |      5        3    0.0417   0.0417    0.0950
```

Cloves is the clean case:

```
seed              bal      nodes  cloves supply inside
genua        -0.54348         53              0.00000
ganges_delta -0.14614          9              0.00000
hangzhou     +0.68962         18              0.98051
world cloves supply sits in: ['hangzhou']
```

**All world cloves supply is in the hangzhou basin. The genua basin holds 53 nodes, 54% of world
cloves demand, and zero cloves.** Genoa is selected as a cloves sink and is structurally unable to
receive cloves — the same failure mode as ranked orientation, reached by a different route.

### Loss source 2 — within-basin starvation, which is the deeper one

Set `S = 1` and cross-basin loss is identically zero, since there is one basin. The loss barely
moves:

```
spices  S=1 unserved = 0.452560     (LAP: 0.0558)
cloves  S=1 unserved = 0.822643     (LAP: 0.1037)
grain   S=1 unserved = 0.113799     (LAP: 0.0183)
```

So compartmentalisation is not the main problem. In a seeded-distance field **flow only moves
inward, toward the seeds.** A demand node at distance 5 from the sink can be served only by supply
that sits even farther out *on the same branch*; supply on a neighbouring branch at the same
distance flows past it, inward, and never reaches it.

The Laplacian does not have this property, and the reason is precise: its φ solves a global
balance equation, so **every supplier is a local maximum of φ** and flow radiates outward from each
supplier to the demand around it. A seeded-distance field has minima only at the S chosen seeds,
so all flow converges to those and everything off a supply→seed path starves.

### γ helps, as documented, then saturates

γ is the algorithm's own knob for this — "makes supply-rich regions tall, pushing ridges onto
suppliers rather than onto demand nodes with no inflow". It works, and it needs to be large,
because `b̃` values are O(10⁻²) while `w = 1 + γ·(…)/2`:

```
gamma    mean unserved  mean dem.reach  goods at 100%
0               0.3242           78.0%          0/29
10              0.2900           80.9%          0/29
100             0.2269           86.8%          0/29
1000            0.2206           88.5%          0/29
10000           0.2208           88.5%          0/29
```

Monotone improvement to a ceiling of 88.5% reach, saturating by γ ≈ 1000 at roughly 100× the
default of 0. It cannot close the gap, because raising `w` on supply nodes changes *distances*
while leaving the field's minima at the S chosen seeds. The starvation is topological, not metric.

---

## 4. Items carried over from the earlier tests

### The Cape and the corridor

```
spices  cape: b̃=0.000  basin=genua     in=1 out=3   conduit: True
  BASIN  malacca -> ganges_delta -> comorin_cape -> gulf_of_aden -> alexandria -> genua
  LAP    malacca -> ganges_delta -> comorin_cape -> gulf_of_aden -> alexandria -> genua
cloves  cape: b̃=0.000  basin=hangzhou  in=2 out=2   conduit: True
  BASIN  the_moluccas -> genua: NO DIRECTED PATH
  LAP    the_moluccas -> malacca -> ganges_delta -> comorin_cape -> gulf_of_aden -> alexandria -> genua
```

The Cape is a proper conduit under BASIN for all 29 goods. For spices, BASIN reproduces the
Laplacian's corridor edge for edge. For cloves it severs it — the same break RANK produced.

### Safi ↔ Sevilla

```
LAP and BASIN agree on this edge for 11 of 29 goods (38%)

good        s(safi)   c(safi) | LAP            BASIN
sugar      0.144330  0.011037 | safi->sevilla  safi->sevilla
spices     0.017467  0.011037 | safi->sevilla  safi->sevilla
iron       0.000000  0.011037 | sevilla->safi  safi->sevilla   <-- Safi exports iron it has none of
tea        0.000000  0.011246 | sevilla->safi  safi->sevilla   <-- same
cloves     0.000000  0.008394 | sevilla->safi  safi->sevilla   <-- same
silk       0.000000  0.010500 | sevilla->safi  safi->sevilla   <-- same
```

**BASIN orients `safi → sevilla` for all 29 goods**, regardless of whether Safi produces the good,
because Safi sits farther from the genua seed than Sevilla does. Direction here is distance-to-seed,
not who holds the good. Every one of the 18 disagreements is of this form.

### Φ and the α = 1 identity

```
Phi(BASIN) = sum_g V_g*(-phi_g)   acyclic: True
Phi(LAP)                          acyclic: True

aggregate Phi agrees with its own per-good orientations:
  LAP    2426/4611 (52.6%)
  BASIN  1339/4611 (29.0%)

Phi(BASIN, alpha=1) vs spec phi0: k=3.77e6  rel.residual=1.523e+00  orient agree 101/159
```

Φ(BASIN) is acyclic, but it agrees with the per-good graphs it aggregates on only 29% of
edge-goods — the installed graph would contradict the commodity graphs more often than not. The
α = 1 identity fails completely and unavoidably: φ is a seeded distance field, not a linear
functional of `s − c`, so there is no linearity-of-the-solve argument to inherit.

**A finding about the incumbent, worth recording:** LAP's own Φ agrees with its own per-good
orientations on only **52.6%** of edge-goods. That is consistent with §3.9 / C508 — the spec
already knows Φ direction is not realized net flow — but 47% disagreement is a larger number than
that passage implies, and no document had measured it.

---

## 5. Conclusion

| | LAP | BASIN (best) |
|---|---|---|
| **mean demand reachable** | **100.0%, 29/29 goods** | 88.5%, **0/29 goods** |
| **mean unserved (BASIN's own objective)** | **0.1037** | 0.2206 |
| orphan sinks | **0 of 102** | 3 of 102 (at defaults) |
| sink-count control | none (emergent) | **exact, S_actual = S** |
| ρ_val (sink/demand) | +0.104 | **+0.225** |
| P(sink \| bottom decile) | 0.7% | **0.0%** |
| acyclic per good | yes | **yes, by construction** |
| Φ acyclic | yes | yes |
| Φ coherent with per-good graphs | 52.6% | 29.0% |
| α = 1 identity | **exact (1.96e-15)** | fails (1.52) |
| sinks that net-produce their good | 0 | 0 |
| conduits preserved | 29/29 | 29/29 |
| noise stability | 0.0/159 | 0.0–0.4/159 |

BASIN is a better-engineered candidate than either predecessor: acyclicity is structural rather
than incidental, the sink count is controllable, sinks land on demand centres and never on poor
nodes, and the conduit and net-producer invariants both hold. Two implementation bugs in the spec
(Phase 2 seed expansion, Phase 5 μ sign) were found and corrected, and γ was exercised to
saturation.

It still loses. The reason it loses is shared with RANK but **not** with FLOW:

- **RANK** — `s − c` is purely local, so orientation is monotone and demand must rise at every hop
  (C371). Reach 83.3%.
- **BASIN** — φ is a seeded Dijkstra distance with minima only at the S chosen seeds, so flow
  converges to those and starves everything off a supply→seed path. Reach 88.5%.
- **FLOW** — reach **100.0%, 29/29 goods, 0 orphans**. It fails for unrelated reasons (49.7% edge
  coverage; cyclic aggregate).

### Correction to an earlier claim in this document

An earlier version said all three candidates discard the supply distribution's ability to shape the
field and all three fail reachability. **That is wrong about FLOW.** Min-cost flow imposes
`inflow − outflow = c − s` at every node, so demand satisfaction is an LP feasibility theorem for
it — it cannot fail reachability. Measured after the fact: 100.0% on all 29 goods, 0 orphan sinks
of 930, tying the Laplacian. `flow-orientation.md` has been corrected accordingly, along with a
second error there: the Cape route is *shorter* than the Alexandria route (3 hops vs 7 to the
Channel), and FLOW routes 24% of world spice supply through it, so FLOW handles §3.2's corridor
better than the incumbent does — the opposite of what that document originally claimed.

So the honest generalisation is narrower:

**Operators whose field has minima only at pre-selected or topologically-determined points starve
demand elsewhere.** That covers RANK (minima wherever local balance dips) and BASIN (minima at the
S seeds). It does not cover operators that impose conservation as a constraint — LAP via the balance
equation, FLOW via the LP. Conservation, not "supplier as local maximum", is what guarantees reach.

| operator | conservation imposed? | reach |
|---|---|---|
| LAP | yes, `L φ = s − c` | 100.0%, 29/29 |
| FLOW | yes, LP node balance | 100.0%, 29/29 |
| RANK | no | 83.3%, 2/29 |
| BASIN | no | 88.5%, 0/29 |

If the search continues, that table is the constraint to respect: any candidate that does not
impose node balance somewhere will strand demand. Within the conservation-respecting family, the
remaining levers on sink *placement* are the ones `diagnosis.md` §6 identified — the weighted
Laplacian and the screened Poisson mass term — both of which keep the balance equation and change
only the metric on it.
