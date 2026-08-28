# -*- coding: utf-8 -*-
"""v6.1 batch AO -- two 1.1 statements can be strengthened from what was measured for v6.1: the key
collision count was measured over ALL core nodes, not only free edges; and Phase 2's solver
requirement now includes the tolerance, which is in the same family as the simplex requirement."""
import patch_lib
E = []

E.append(dict(id="AO1", clears="AO1: the key-collision measurement, at its real scope", section="1.1",
old="""  no exact ties. Measured: zero orientation changes under scheduler permutations, and zero exact
  `(DEF, b)` ties on free edges, 29/29 goods.""",
new="""  no exact ties. Measured: zero orientation changes under scheduler permutations, and zero exact
  `(DEF, b)` key collisions across **all 2,320 core nodes** of the 29 per-good solves — not merely on
  the free edges, which is where earlier versions measured it. Phase 1's within-cluster argmin and its
  top-k cluster cut are untied on the same field, so no index tiebreak in the algorithm fires at all."""))

E.append(dict(id="AO2", clears="AO2: Phase 2 names both solver requirements", section="1.1",
old="""and return a support with an undirected cycle in it. §2.2 therefore requires network simplex or a
simplex LP.""",
new="""and return a support with an undirected cycle in it. §2.2 therefore requires network simplex or a
simplex LP, and §2.3 additionally requires the solver's optimality tolerance to be tighter than the
margin the tie-break provides — both are correctness requirements on the solver rather than settings."""))

patch_lib.apply(E)
