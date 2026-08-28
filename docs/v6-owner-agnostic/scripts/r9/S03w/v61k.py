# -*- coding: utf-8 -*-
"""v6.1 batch K -- the front matter and 1.1's Phase 2. The document was still calling itself 6.0
while referring to v6.0 as a previous version, and 1.1 still described Phase 2 as minimising unit arc
costs, which is the thing that changed."""
import patch_lib
E = []

E.append(dict(id="K1", clears="K1: the version, since the document now refers back to v6.0",
section="0",
old="""**Version:** 6.0""",
new="""**Version:** 6.1"""))

E.append(dict(id="K2", clears="K2: what v6.1 changes", section="0",
old="""Three start-state reads are corrected in the same pass (`on_startup` devastation, dated
`add_base_*` accumulation, and the `is_city` filter the engine does not apply). **Phase 2's min-cost
flow is degenerate under unit arc costs, so presentation order selected which optimum was returned;
§2.3 now breaks that tie inside the objective, and §1.6 measures the orientation as unchanged across
every relabelling tried.** A canonical node order remains an emitter requirement, but it is no longer
what decides the map.""",
new="""Three start-state reads are corrected in the same pass (`on_startup` devastation, dated
`add_base_*` accumulation, and the `is_city` filter the engine does not apply).

**v6.1** changes two things, both in the operator rather than the field. **Phase 2's min-cost flow is
degenerate under unit arc costs, so presentation order selected which optimum was returned; §2.3 now
breaks that tie inside the objective, and §1.6 measures the installed orientation as unchanged across
every relabelling tried.** A canonical node order remains an emitter requirement — the per-good
graphs are still order-sensitive (§2.4 item 1) — but it is no longer what decides the installed map.
And **`α_Φ` moves from 1.5 to 2.0.** Both `α_Φ` and the new `TIE_EPS` are hyperparameters whose values
are developer taste; §2.3 states them and offers no justification for either, and every derivation
previously offered for `α_Φ` is withdrawn without replacement. The 1444 sink set moves from
`{english_channel, hangzhou}` to `{genua, hangzhou}` and 29 of the 59 figures `measure6.py` prints
move with it."""))

E.append(dict(id="K3", clears="K3: 1.1's Phase 2 describes the cost it actually minimises",
section="1.1",
old="""**Phase 2 — route: min-cost b-flow.** Solve the uncapacitated min-cost flow with unit arc costs
serving `b_g`, and orient every support edge by its net flow. The support is a spanning-tree basis
of ≤ N−1 edges **when the solver returns a basic (vertex) optimum**, which the simplex family
does; an interior-point solve without crossover can split flow across equal-length parallel paths
and return a support with an undirected cycle in it. §2.2 therefore requires network simplex or a
simplex LP. What holds for *any* optimum is the weaker and sufficient property: the support
contains **no directed cycle**, because with all costs 1 a directed cycle could be cancelled for
strictly lower cost. Edges with zero net flow are *free* and deferred to Phase 3.""",
new="""**Phase 2 — route: min-cost b-flow.** Solve the uncapacitated min-cost flow serving `b_g` and orient
every support edge by its net flow. Arc costs are `1 + TIE_EPS·(w[u] + w[v])/2` — near-unit, symmetric
in the arc, and read from node wealth (§2.3). They are not unit because with unit costs the optimum is
not unique and which one the solver returns depends on the order the nodes are presented in; the
near-unit perturbation leaves one optimum to return. The support is a spanning-tree basis
of ≤ N−1 edges **when the solver returns a basic (vertex) optimum**, which the simplex family
does; an interior-point solve without crossover can split flow across equal-length parallel paths
and return a support with an undirected cycle in it. §2.2 therefore requires network simplex or a
simplex LP. What holds for *any* optimum is the weaker and sufficient property: the support
contains **no directed cycle**, because with all costs strictly positive a directed cycle could be
cancelled for strictly lower cost — an argument that needs positivity, not unit costs, so it survives
the change. Edges with zero net flow are *free* and deferred to Phase 3."""))

E.append(dict(id="K4", clears="K4: the harness's own check count", section="0",
old="""**`verify6.py` pins 35 distinct figures across 29 checks, and that is well short of what the document
prints.**""",
new="""**`verify6.py` runs 31 checks against values computed from the install, and that is well short of
what the document prints.**"""))

patch_lib.apply(E)
