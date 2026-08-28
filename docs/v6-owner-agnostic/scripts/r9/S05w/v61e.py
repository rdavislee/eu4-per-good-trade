# -*- coding: utf-8 -*-
"""v6.1 batch E -- the last three sites the harness still disagrees with."""
import patch_lib
E = []

E.append(dict(id="E1", clears="E1: 1.1's per-good sink range", section="1.1",
old="""  goods, 1–8 sinks per good, mean 3.72, zero fallbacks.""",
new="""  goods, 2–8 sinks per good, mean 3.69, zero fallbacks."""))

# The Cape figures are right but were written with the node names interrupting the three numbers, so
# the harness could not aim a single needle at them. Put the numbers contiguous and the names after.
E.append(dict(id="E2", clears="E2: the Cape figures, phrased so one needle reaches all three",
section="1.6",
old="""The Cape is nonetheless a live conduit, not an idle one: in-degree 2 (`zanzibar`, `ivory_coast`),
out-degree 2 (`comorin_cape`, `malacca`), with **81 ordered node pairs** for which a path through it
exists (`measure6.py` — the count is pairs `(a, b)` where `a` reaches the Cape, the Cape reaches `b`,
and `a` reaches `b`, not pairs whose shortest path happens to use it; the stricter shortest-path
reading gives 69 on the same field). It carries Atlantic drainage into the Indian Ocean.""",
new="""The Cape is nonetheless a live conduit, not an idle one: in-degree 2, out-degree 2, with **81
ordered node pairs** for which a path through it exists (`measure6.py`). It takes flow from
`zanzibar` and `ivory_coast` and passes it to `comorin_cape` and `malacca`, carrying Atlantic
drainage into the Indian Ocean. *The count is pairs `(a, b)` where `a` reaches the Cape, the Cape
reaches `b`, and `a` reaches `b` — not pairs whose shortest path happens to use it, which is a
stricter reading and gives 69 on the same field.*"""))

patch_lib.apply(E)
