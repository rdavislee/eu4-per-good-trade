# -*- coding: utf-8 -*-
"""v6.1 batch A -- section 1.6. The tie-break makes Phase 2's optimum unique, so the section's
central distinction (one sink is the world's, one is the node ordering's) no longer exists. alpha and
epsilon lose their justifications: they are hyperparameters and the choice is developer taste."""
import patch_lib
E = []

E.append(dict(id="A1", clears="A1: alpha is 2.0 and is a hyperparameter", section="1.6",
old="""               b_w    = s_w − c_w                  α_Φ = 1.5, a stipulated constant (§2.3)""",
new="""               b_w    = s_w − c_w                  α_Φ = 2.0, a hyperparameter (§2.3)"""))

E.append(dict(id="A2", clears="A2: the count/placement sentence, at the new alpha", section="1.6",
old="""the wealth field, and `α_Φ` sets how sharply concentration is read.** At the stipulated α_Φ = 1.5 the
1444 field gives two sinks, and a modestly grown Europe gives three or one (the Europe table below),
so neither the count nor the placement is fixed by the constant.""",
new="""the wealth field, and `α_Φ` sets how sharply concentration is read.** At α_Φ = 2.0 the 1444 field
gives two sinks, and a modestly grown Europe gives two, three or five (the Europe table below), so
neither the count nor the placement is fixed by the constant."""))

E.append(dict(id="A3", clears="A3: largest |b_w| at the new alpha", section="1.6",
old="""Normalising into (−1, 1) scales 1444's `b_w` *up* (its largest magnitude is 0.0225) and is safe;""",
new="""Normalising into (−1, 1) scales 1444's `b_w` *up* (its largest magnitude is 0.0347) and is safe;"""))

# ---- the heart of it: the ordering argument inverts ----------------------------------------------
E.append(dict(id="A4", clears="A4: the sinks, and that the orientation is now order-invariant",
section="1.6",
old="""Measured on 1444 data at α_Φ = 1.5 (`measure6.py`): **two sinks, `english_channel` and
`hangzhou`** — `c_w` ranks 2 and 3, node-wealth ranks 1 and 12. **One of those two is a property of
the world and the other is a property of the node ordering, and the difference matters more than the
count.** Phase 2's b-flow is degenerate (§2.4 item 1), so relabelling the nodes and re-running
returns a different optimal orientation. Over **800 relabellings** — eight seeds of 100, with `α_Φ`
and every input held fixed (`relabel6.py`) — **the orientation changed every time**, a mean of 25 of
159 edges moved, and the sink set came back exactly as `{english_channel, hangzhou}` in **64 of 800**
runs. **`hangzhou` was an end in about 98% of them and `english_channel` in about 40%.** The Asian
end is the robust one — not invariant, since orderings exist where it loses its end, but near enough
that it is a fact about that node. The European end is one of several the same world admits, and after
`english_channel` the most frequent are `gulf_of_siam` (a little over half the runs), `wien` (about a
third), then `rheinland` and `sevilla`. The count itself ranged 1 to 5, most often 2 or 3.

*The two leading proportions are quoted to two figures and the trailing ones qualitatively, because
that is as far as this sample supports: across three independent 800-trial sets `hangzhou` came in at
784–789 and `english_channel` at 322–336, while `sevilla` ranged 79–117 and `rheinland` 112–136. A
per-seed range is worse still, being a function of which seeds are drawn.*""",
new="""Measured on 1444 data at α_Φ = 2.0 (`measure6.py`): **two sinks, `genua` and `hangzhou`** — `c_w`
ranks 2 and 1, node-wealth ranks 4 and 12. **Both are properties of the world, because the
orientation does not depend on how the nodes are numbered.** That is a change from v6.0, and it is
worth stating why, since the previous version's argument turned on the opposite.

With unit arc costs Phase 2's b-flow is degenerate: many routings reach the same minimum cost, and
the simplex returns whichever its pivot path reaches, which moves with node numbering. Measured on
that LP directly, **40 of 40 permutations return a different optimal support** at an objective
identical to within a few units in the last place. So the old sink set was partly an artifact of the
node order, and v6.0 said so.

Phase 2 now breaks those ties inside the objective (§2.3), with a cost symmetric in the arc and read
from node wealth alone. On the same LP, **0 of 40 permutations return a different support**. Over
**180 relabellings** — three seeds of 60, every input held fixed (`relabel6.py`, which validates its
instrument against `drain.py` on the identity permutation before counting any trial) — **the
orientation did not change once**: 0 of 159 edges moved in any run, and the sink set came back as
`{genua, hangzhou}` in **180 of 180**. `hangzhou` and `genua` each held an end in every run.

*Two cautions for anyone re-running this. The instrument is a reimplementation, and a
reimplementation whose Phase 2 minimises the old objective disagrees with the shipped solver on 26 of
159 edges — `relabel6.py` aborts on exactly that, and did so when the tie-break went in. And a
symmetric cost is required, not a stylistic choice: a directional preference of the form
`1 − ε·(w[v] − w[u])` is a potential difference, so its total over any flow meeting the same `b` is
`Σ_n w[n]·b[n]` — the same for every feasible routing, and unable to break a tie at all.*"""))

patch_lib.apply(E)
