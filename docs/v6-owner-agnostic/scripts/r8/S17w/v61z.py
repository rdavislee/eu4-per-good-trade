# -*- coding: utf-8 -*-
"""v6.1 batch Z -- 2.3 documents the second-order term; 2.4 item 1 records what it fixed and what it
did not; 1.1's Phase 2 names the cost it now minimises."""
import patch_lib
E = []

E.append(dict(id="Z1", clears="Z1: 1.1's Phase 2 cost, with both terms", section="1.1",
old="""every support edge by its net flow. Arc costs are `1 + TIE_EPS·(w[u] + w[v])/2` — near-unit, symmetric
in the arc, and read from node wealth (§2.3). They are not unit because with unit costs the optimum is
not unique and which one the solver returns depends on the order the nodes are presented in; the
near-unit perturbation leaves one optimum to return.""",
new="""every support edge by its net flow. Arc costs are near-unit, symmetric in the arc, and read from node
wealth: a first-order term `TIE_EPS·(w[u] + w[v])/2` that carries the design intent, plus a
second-order generic term that breaks the ties the first one leaves (§2.3). They are not unit because
with unit costs the optimum is not unique and which one the solver returns depends on the order the
nodes are presented in; the perturbation is what leaves one optimum to return."""))

E.append(dict(id="Z2", clears="Z2: 2.3 states the second-order term and why it exists", section="2.3",
old="""```
cost(u, v) = 1 + TIE_EPS · (w[u] + w[v]) / 2        w = node wealth, normalised to [0, 1]
```

Two properties are load-bearing and neither is a matter of taste.""",
new="""```
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

Two properties are load-bearing and neither is a matter of taste."""))

E.append(dict(id="Z3", clears="Z3: 2.4 item 1's per-good figures and the corrected note", section="2.4",
old="""   vector. Measured across 29 goods × 10 relabellings: **84 of 290** runs changed a per-good
   orientation, a mean of 0.99 edges and up to 15. So the installed aggregate graph is invariant over
   the orderings tried and the per-good graphs are not — and since §2.2 propagates the per-good
   economy and writes it back, that is what keeps a canonical order a correctness requirement rather
   than a convention. *A second wealth term (`+ TIE_EPS² · |w[u] − w[v]|`) was tried and rejected: it
   makes all 159 arc costs distinct where the shipped cost leaves 3 pairs equal, and still leaves 72 of
   232 per-good supports moving, down from 93. Distinct arc costs are not the issue — equal **totals**
   over different routings are, and ruling those out needs a generic perturbation, which is arbitrary
   by construction and so trades one arbitrariness for another.*""",
new="""   vector. §2.3's second-order generic term closes most of that gap: per-good relabelling sensitivity
   falls from **84 of 290** runs to **13**, and the goods admitting any alternative optimum from **18
   of 29 to 1**. What remains is small but real, so the installed aggregate graph is invariant over the
   orderings tried and the per-good graphs are very nearly so — and since §2.2 propagates the per-good
   economy and writes it back, that residue is what keeps a canonical order a correctness requirement
   rather than a convention."""))

patch_lib.apply(E)
