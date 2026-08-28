# -*- coding: utf-8 -*-
"""v6.1 batch T -- correct what per-good order-sensitivity actually reaches. I wrote that the value
weights hang off the per-good solves. They do not: V_g = price * sum of goods_produced is a sum over
producers with no direction in it. What it does reach is larger -- 2.2 propagates the per-good economy
and writes it back, so it reaches the numbers the player sees."""
import patch_lib
E = []

E.append(dict(id="T1", clears="T1: what per-good order-sensitivity reaches, stated correctly",
section="1.6",
old="""is a different vector. Measured across 29 goods × 10 relabellings, **84 of 290** runs moved a per-good
edge — a mean of 0.99 and up to 15 (§2.4 item 1). So the per-good figures in this section are quoted
at fixed node order, and the emitter must fix one canonical order and keep it: not for the installed
map any more, but for the value weights and the §1.10 survival table that hang off the per-good
solves. The `Φ_w` guarantee is also measured over the orderings tried rather than proved.""",
new="""is a different vector. Measured across 29 goods × 10 relabellings, **84 of 290** runs moved a per-good
edge — a mean of 0.99 and up to 15 (§2.4 item 1). So the per-good figures in this section are quoted
at fixed node order, and the emitter must fix one canonical order and keep it. **That requirement is
not weaker than it was in v6.0, only relocated:** §2.2 propagates the per-good economy and writes it
back, so a per-good arrow that moves with the node numbering moves node values, the ledger and the
economy tab with it. The value weights are the exception — `V_g` is `price(g)` times a sum over
producers, with no direction in it, so they are order-independent by construction. The `Φ_w`
guarantee is measured over the orderings tried rather than proved."""))

E.append(dict(id="T2", clears="T2: 2.2's MP note, with the right downstream", section="2.2",
old="""question applies to it. And the per-good graphs are untouched — their optima are still degenerate
(§2.4 item 1), so vertex selection remains an exposure there, and the value weights and survival table
are downstream of it.""",
new="""question applies to it. And the per-good graphs are untouched — their optima are still degenerate
(§2.4 item 1), so vertex selection remains an exposure there, and the whole propagated per-good
economy is downstream of it: node values, the ledger and the economy tab all read numbers that a
different optimal vertex would change. The value weights are not — `V_g` is a producer sum with no
direction in it."""))

E.append(dict(id="T3", clears="T3: 2.4 item 1's downstream, same correction", section="2.4",
old="""   orientation, a mean of 0.99 edges and up to 15. So the installed aggregate graph is invariant over
   the orderings tried, while the per-good graphs — which set value weights and the §1.10 survival
   table — are not.""",
new="""   orientation, a mean of 0.99 edges and up to 15. So the installed aggregate graph is invariant over
   the orderings tried and the per-good graphs are not — and since §2.2 propagates the per-good
   economy and writes it back, that is what keeps a canonical order a correctness requirement rather
   than a convention. *A second wealth term (`+ TIE_EPS² · |w[u] − w[v]|`) was tried and rejected: it
   makes all 159 arc costs distinct where the shipped cost leaves 3 pairs equal, and still leaves 72 of
   232 per-good supports moving, down from 93. Distinct arc costs are not the issue — equal **totals**
   over different routings are, and ruling those out needs a generic perturbation, which is arbitrary
   by construction and so trades one arbitrariness for another.*"""))

patch_lib.apply(E)
