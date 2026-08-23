# -*- coding: utf-8 -*-
"""v6 batch 24 — Y124. The installed map's European end is a property of the node ordering, not of
the world. Stated at the point of use, not only in 2.4. Confirmed twice: the auditor's five-phase
reimplementation and my own run of it, both validated against drain.py on Phi_w (159/159 edges,
core 80, promotions 2, fallbacks 0) before being trusted."""
import patch_lib
E = []

E.append(dict(id="Y124a", clears="Y124: the sink set is qualified where it is stated", section="1.6",
old="""Measured on 1444 data at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and
`hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12.""",
new="""Measured on 1444 data at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and
`hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12. **One of those two is a property of
the world and the other is a property of the node ordering, and the difference matters more than the
count.** Phase 2's b-flow is degenerate (§2.4 item 1), so relabelling the nodes and re-running
returns a different optimal orientation: across 100 relabellings with α_Φ and every input held
fixed, the orientation changed 100 times, a mean of 26 of 159 edges moved, and the sink set came back
exactly as `{english_channel, hangzhou}` **8 times**. But `hangzhou` was an end in **100 of 100**,
and `english_channel` in **40**. The Asian end is the robust one; the European end is one of several
the same world admits — `gulf_of_siam` held an end in 55 runs, `wien` in 37, `sevilla` in 19. The
count itself ranged 1 to 5, most often 2.

**So read the rest of this section as conditional on one canonical node order**, which §2.4 item 1
requires the emitter to fix. That is not a caveat about precision; it is a statement about what kind
of fact the European end is."""))

E.append(dict(id="Y124b", clears="Y124: the Europe table carries the same condition", section="1.6",
old="""Read the table as a direction rather than a trajectory: the Channel holds an end throughout, Asia
loses its own between ×1.02 and ×1.56, and by ×2.00 the map has a single Mediterranean end at
`genua` — so growth concentrates the map on Europe without the Channel monotonically absorbing it.""",
new="""Read the table as a direction rather than a trajectory, and on one node ordering: growth moves the
ends westward and thins Asia's, and by ×2.00 a single Mediterranean end at `genua` holds the map.
*Which* European node holds an end at a given factor is ordering-dependent in the same way the 1444
set is — `english_channel` at ×1.02, `rheinland` at ×1.56 and `genua` at ×2.00 are this ordering's
answers, not the world's — so the direction is the claim and the membership is not."""))

E.append(dict(id="Y124c", clears="Y124: the end-flag list is conditional", section="2.4",
old="""2. **End flags** — `end=yes` on every `Φ_w` sink (1444: **two** end nodes, `english_channel` and
   `hangzhou`, against""",
new="""2. **End flags** — `end=yes` on every `Φ_w` sink. **This list is a function of the canonical node
   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end under
   every ordering tried, `english_channel` under about 40% of them, and the count ranges 1 to 5
   (§1.6). Fix the order, emit, and keep it — changing it changes the flags without anything in the
   world changing. (1444, shipped order: **two** end nodes, `english_channel` and
   `hangzhou`, against"""))

E.append(dict(id="Y124d", clears="Y124: 2.8's razed-China row survives, and why", section="2.8",
old="""| Razed China | Zeroing `hangzhou`-node development relocates an end in one solve""",
new="""| Razed China | *This row is ordering-robust where §1.6's sink membership is not: it turns on `hangzhou` holding an end, which it does under every relabelling tried (§1.6).* Zeroing `hangzhou`-node development relocates an end in one solve"""))

E.append(dict(id="Y003d", clears="Y003: quote the ratio against the field the spec calls world wealth",
section="1.3",
old="""depended on. On the 1444 start that whole apparatus was worth **105.30 ducats** — 0.98% of the
10,712.70 that field totalled with it, 0.99% of the 10,607.40 without — over **89** of the 2,472""",
new="""depended on. On the 1444 start that whole apparatus was worth **105.30 ducats**, **0.99%** of the
10,607.40 world wealth the model computes without it (0.98% of the 10,712.70 the field totalled with
it), over **89** of the 2,472"""))

patch_lib.apply(E)
