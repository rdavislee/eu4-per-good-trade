# -*- coding: utf-8 -*-
"""v6.1 batch AI -- the solver's optimality tolerance turns out to be a correctness requirement, and
pinning it makes the per-good graphs order-invariant too. That changes 1.6, 2.3, 2.4 and 2.2's
multiplayer position."""
import patch_lib
E = []

E.append(dict(id="AI1", clears="AI1: 1.6's per-good order-sensitivity is now zero", section="1.6",
old="""is a different vector. §2.3's **second-order** term addresses exactly that, and most of the way:
across 29 goods × 10 relabellings **13 of 290** runs move a per-good edge, down from 84 before it, and
the number of goods admitting an alternative optimum at all falls from **18 of 29 to 1**. So the
per-good figures in this section are still quoted at fixed node order, and the emitter must still fix
one canonical order and keep it — **the requirement is weaker than in v6.0 but not gone**: §2.2
propagates the per-good economy and writes it back, so a per-good arrow that moves with the node
numbering moves node values, the ledger and the economy tab with it. The value weights are the
exception — `V_g` is `price(g)` times a sum over producers, with no direction in it, so they are
order-independent by construction. Both guarantees here are measured over the orderings tried rather
than proved.""",
new="""is a different vector. Two changes closed that gap. §2.3's **second-order** term took per-good
relabelling sensitivity from **84 of 290** runs to 13 and the goods admitting an alternative optimum
from 18 of 29 to 1; **pinning the solver's optimality tolerance (§2.3) took the remainder to 0 of
290.** So on this field the per-good graphs are order-invariant over the orderings tried, as `Φ_w` is.

The emitter should still fix one canonical order, because both guarantees are measured rather than
proved and §2.2 propagates the per-good economy and writes it back — a per-good arrow that moved with
the node numbering would move node values, the ledger and the economy tab with it. The value weights
never could: `V_g` is `price(g)` times a sum over producers, with no direction in it."""))

E.append(dict(id="AI2", clears="AI2: 2.3 records the tolerance as a correctness requirement",
section="2.3",
old="""*What it costs:* self-coherence with the per-good graphs falls 0.1–0.2 points, and nothing else
measured moves.""",
new="""**The solver's optimality tolerance is a correctness requirement, not a performance knob.** HiGHS
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
nothing else measured moves."""))

E.append(dict(id="AI3", clears="AI3: 2.4 item 1's per-good residue is gone", section="2.4",
old="""   vector. §2.3's second-order generic term closes most of that gap: per-good relabelling sensitivity
   falls from **84 of 290** runs to **13**, and the goods admitting any alternative optimum from **18
   of 29 to 1**. What remains is small but real, so the installed aggregate graph is invariant over the
   orderings tried and the per-good graphs are very nearly so — and since §2.2 propagates the per-good
   economy and writes it back, that residue is what keeps a canonical order a correctness requirement
   rather than a convention.""",
new="""   vector. §2.3's second-order generic term took per-good relabelling sensitivity from **84 of 290**
   runs to **13**, and pinning the solver's optimality tolerance took it to **0 of 290**. So both the
   installed graph and the per-good graphs are order-invariant over the orderings tried. A canonical
   order remains an emitter requirement because that is a measurement and not a proof, and because
   §2.2 propagates the per-good economy and writes it back — but it is no longer the difference
   between a correct map and an arbitrary one."""))

patch_lib.apply(E)
