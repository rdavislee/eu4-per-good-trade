# -*- coding: utf-8 -*-
"""v6 batch 8 — X013/X145 (the sink-set conditions are necessary, not sufficient: T2 satisfies
both) and X016/X151 (index-independence is a measurement on post-fold balances)."""
import patch_lib
E = []

E.append(dict(id="R8-claim1", clears="X013/X145: T2 satisfies the stated conditions", section="3.2",
old="""1. **Sink placement:** on a map where Phase 0 is a no-op and no fallback fires, final sinks =
   `{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal demanders}` — measured exact,
   29/29 goods. **This is a measurement, not a theorem**, and v2 asserted it as a theorem. Three
   constructed inputs break it, all run through a faithful implementation of §1.1 (`toys.py`):""",
new="""1. **Sink placement:** on 1444, final sinks = `{selected ∩ flow-terminal} ∪ {stall-promoted
   flow-terminal demanders}` — measured exact, 29/29 goods. **This is a measurement on one input,
   not a theorem**, and v2 asserted it as a theorem. v5.0 tried to rescue it by attaching two
   conditions — Phase 0 a no-op and no fallback firing — and **those conditions are necessary, not
   sufficient**: T2 below satisfies both and still breaks the equality, so the conditioned form is
   no more a theorem than the bare one. Three constructed inputs break it, all run through a
   faithful implementation of §1.1 (`toys.py`):"""))

E.append(dict(id="R8-index", clears="X016/X151: index-independence, measured on the post-fold key",
section="3.2",
old="""   no exact ties: zero exact `(DEF, b)` ties on free edges, 29/29 goods on 1444. The one place the
   indexing is load-bearing is the fallback branch (T3 above), where the candidates are typically
   all zero-wealth and tied; §2.4 item 1 makes a canonical node order a correctness requirement for
   that reason.""",
new="""   no exact ties: zero exact ties on free edges, 29/29 goods on 1444. Two cautions on that
   measurement. First, the key reads the **post-fold** balance β, the one Phase 0 hands on — so
   peeling can *create* exact ties that the raw input balances do not have, and the 1444 result does
   not transfer to a map where Phase 0 acts. Second, the indexing is load-bearing wherever the key
   ties, which is not only the fallback branch: it also decides Phase 1's within-cluster argmin, the
   stall promotion's identical form, and the top-k cut between clusters of equal mass. None of those
   fires on 1444. **And none of them is why §2.4 requires a canonical node order** — that requirement
   comes from Phase 2's degenerate LP, which moves the orientation under relabelling even when no key
   tie exists anywhere (§2.4 item 1)."""))

patch_lib.apply(E)
