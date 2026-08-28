# -*- coding: utf-8 -*-
"""v6.1 batch Y -- the second-order tie-break goes in. Four measured figures move; the per-good
order-sensitivity claims improve substantially; and the rejected-second-term note has to change,
because what was rejected was a STRUCTURED second term and what is adopted is a GENERIC one."""
import patch_lib
E = []

E.append(dict(id="Y1", clears="Y1: 1.6's connectivity and self-coherence", section="1.6",
old="""**90.5%** of ordered node pairs (5,721 of 6,320) connected by at least one good's directed path.

Agreement with the per-good graphs is **55.2%** of edge-goods (**55.0%** value-weighted). The""",
new="""**90.6%** of ordered node pairs (5,723 of 6,320) connected by at least one good's directed path.

Agreement with the per-good graphs is **55.1%** of edge-goods (**54.8%** value-weighted). The"""))

E.append(dict(id="Y2", clears="Y2: 3.13's self-coherence baseline", section="3.13",
old="""  baseline is known — `Φ_w` agrees with the per-good graphs on **55.0%** of edge-goods *weighted by
  trade value*, and on 55.2% unweighted (§1.6) —""",
new="""  baseline is known — `Φ_w` agrees with the per-good graphs on **54.8%** of edge-goods *weighted by
  trade value*, and on 55.1% unweighted (§1.6) —"""))

E.append(dict(id="Y3", clears="Y3: 3.8's any-good connectivity", section="3.8",
old="""measured, **90.5%** (5,721 of 6,320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. (v2 quoted 98.8%; that is v1's *Laplacian* figure, 6245/6320, carried across the operator change without being re-measured. The argument is unaffected — 90.5% is still most of the map — but the number was not v2's own.)""",
new="""measured, **90.6%** (5,723 of 6,320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. (v2 quoted 98.8%; that is v1's *Laplacian* figure, 6245/6320, carried across the operator change without being re-measured. The argument is unaffected — 90.6% is still most of the map — but the number was not v2's own.)"""))

E.append(dict(id="Y4", clears="Y4: 1.6's per-good order-sensitivity, after the second term",
section="1.6",
old="""is a different vector. Measured across 29 goods × 10 relabellings, **84 of 290** runs moved a per-good
edge — a mean of 0.99 and up to 15 (§2.4 item 1). So the per-good figures in this section are quoted
at fixed node order, and the emitter must fix one canonical order and keep it. **That requirement is
not weaker than it was in v6.0, only relocated:** §2.2 propagates the per-good economy and writes it
back, so a per-good arrow that moves with the node numbering moves node values, the ledger and the
economy tab with it. The value weights are the exception — `V_g` is `price(g)` times a sum over
producers, with no direction in it, so they are order-independent by construction. The `Φ_w`
guarantee is measured over the orderings tried rather than proved.""",
new="""is a different vector. §2.3's **second-order** term addresses exactly that, and most of the way:
across 29 goods × 10 relabellings **13 of 290** runs move a per-good edge, down from 84 before it, and
the number of goods admitting an alternative optimum at all falls from **18 of 29 to 1**. So the
per-good figures in this section are still quoted at fixed node order, and the emitter must still fix
one canonical order and keep it — **the requirement is weaker than in v6.0 but not gone**: §2.2
propagates the per-good economy and writes it back, so a per-good arrow that moves with the node
numbering moves node values, the ledger and the economy tab with it. The value weights are the
exception — `V_g` is `price(g)` times a sum over producers, with no direction in it, so they are
order-independent by construction. Both guarantees here are measured over the orderings tried rather
than proved."""))

patch_lib.apply(E)
