# -*- coding: utf-8 -*-
"""v6 batch 6 — X185/X186/X143: the supply/demand contrast on the (c) field, stated over the goods
that have a contrast to measure; and the spice thresholds as observations."""
import patch_lib
E = []

E.append(dict(id="R6-32", clears="X185/X143: contrast and thresholds in 3.2", section="3.2",
old="""regularizer, which §1.2 removes; with no regularizer the spices supply ratio over *producing* nodes
is 36 against a demand ratio of 482.2, which points the other way. Sparsity is the asymmetry that
survives the regularizer's deletion, and the diagnosis rests on it.) No parameter fixes it: α strong enough to matter
destroys §1.4's regime split, and better wealth inputs plausibly deliver about 1.7× (measured:
`genua` becomes a co-sink at ×1.720) — enough to make Genoa a *co-*sink, not enough to make demand
the determinant of placement: a spice sink at any of **the four Chinese trade nodes —
`beijing`, `xian`, `canton`, `hangzhou`** — needs **3.6–4.9×**, i.e. **9.3–21.4%** of all world
spice demand at one node (`beijing` 3.60× / 9.3%, `hangzhou` 3.83× / 21.4%, `xian` 4.59× / 12.3%,""",
new="""regularizer, which §1.2 removes. **What the ratio metric cannot see is the thing the diagnosis
rests on.** Sparsity is the asymmetry: most nodes produce nothing at all of a given good — spices
are produced in 18 of 80 nodes and cloves in exactly one — so `(c−s)/deg` is dominated by *where*
supply exists rather than by how large it is, and a max/min ratio over producing nodes is blind to
that by construction. On the contrast metric itself the demand side is the wider one, not the
supply side. No parameter fixes it: α strong enough to matter destroys §1.4's regime split, and
better wealth inputs move Genoa to a *co-*sink at roughly ×1.7 without making demand the determinant
of placement. Moving the spice sink to a Chinese node takes a multiple of that node's demand in the
region of **3.6–4.9×** — observed on the 1444 field (`beijing` 3.61×, `hangzhou` 4.12×, `xian`
4.60×, `canton` 4.77×). The multiple a node needs and the share of world demand it then holds do not
line up end to end, because the share a multiple buys depends on where the node started ("""))

E.append(dict(id="R6-315", clears="X186/X185: 3.15's Laplacian entry agrees with 3.2", section="3.15",
old="""*(v1 and v2 gave the asymmetry as "supply contrast 10⁷ against demand contrast 10²–10³", and v3.0
through v4.0 repeated it here while §3.2 was withdrawing it. §3.2 is right: that ratio was `max(s)`
over v1's ε floor, and with the floor removed the contrasts run **4–97 on supply against
211–20,400 on demand** across the 29 goods — the demand side is the wider one. Sparsity is what
survives the floor's deletion, and it is what the diagnosis rests on.)*""",
new="""*(v1 and v2 gave the asymmetry as "supply contrast 10⁷ against demand contrast 10²–10³"; v3.0 and
v4.0 repeated it here while v4.0's own §3.2 was withdrawing it. §3.2 is right — that ratio was
`max(s)` over v1's ε floor. With the floor removed the contrasts run **4–97 on supply against
211–15,010 on demand** over the 28 goods produced in more than one node, so the demand side is the
wider one; `cloves` has a single producer and no contrast to measure, which is the sparsity point in
miniature.)*"""))

patch_lib.apply(E)
