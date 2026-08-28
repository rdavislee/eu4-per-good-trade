# -*- coding: utf-8 -*-
"""v6.1 batch S -- 1.6 claimed the per-good figures are order-invariant. They are not; 2.4 item 1
measures 84 of 290 per-good runs moving an edge. The two sections contradicted each other."""
import patch_lib
E = [dict(id="S1", clears="S1: 1.6 stops claiming per-good order-invariance", section="1.6",
old="""**What is conditional on the node order.** Nothing that this document quotes. Over the 180
relabellings above, the sink set, every edge direction, the promotion and fallback counts and the
per-good figures were identical, so the distinction v6.0 drew between world-properties and
ordering-artifacts has collapsed into the first category. The emitter should still fix one canonical
order — the guarantee is measured over the orderings tried, not proved — and §2.4 item 1 records
that as an implementation requirement rather than a correctness worry.""",
new="""**What is conditional on the node order.** Nothing this section quotes about the **installed** graph.
Over the 180 relabellings above the sink set, every edge direction, and the promotion and fallback
counts were identical, so for `Φ_w` the distinction v6.0 drew between world-properties and
ordering-artifacts has collapsed into the first category.

**The per-good graphs are a different matter.** The tie-break cost is read from node wealth, which is
good-independent, but a wealth-weighted cost need not separate the optima of a per-good LP, whose `b`
is a different vector. Measured across 29 goods × 10 relabellings, **84 of 290** runs moved a per-good
edge — a mean of 0.99 and up to 15 (§2.4 item 1). So the per-good figures in this section are quoted
at fixed node order, and the emitter must fix one canonical order and keep it: not for the installed
map any more, but for the value weights and the §1.10 survival table that hang off the per-good
solves. The `Φ_w` guarantee is also measured over the orderings tried rather than proved.""")]
patch_lib.apply(E)
