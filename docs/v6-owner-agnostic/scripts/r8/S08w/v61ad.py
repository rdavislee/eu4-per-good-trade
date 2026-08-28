# -*- coding: utf-8 -*-
"""v6.1 batch AD -- four passages the sweep caught after the second term went in. One directly
contradicts itself now: 2.3 still said 'adding a second wealth term does not close it'."""
import patch_lib
E = []

E.append(dict(id="AD1", clears="AD1: 2.3's paragraph now describes the term it has", section="2.3",
old="""**A single cost vector does not make every solve unique, and §2.4 item 1 measures where it does not.**
Uniqueness of an LP optimum depends on the right-hand side as well as the objective: `b_w` has no zero
entries and its optimum is unique under this cost, while each `b_g` puts a different face of the
polytope in play and 84 of 290 per-good relabellings still move an edge. Adding a second wealth term
does not close it — see item 1 — because the obstruction is different routings with equal **totals**,
not individual arcs with equal costs.""",
new="""**A single cost vector does not make every solve unique, and §2.4 item 1 measures what is left.**
Uniqueness of an LP optimum depends on the right-hand side as well as the objective: `b_w` has no zero
entries and its optimum is unique under the first-order term alone, while each `b_g` puts a different
face of the polytope in play and 18 of the 29 admitted an alternative optimum before the second-order
term. With it, that falls to 1 good and per-good relabelling sensitivity to 13 of 290 runs. The
residue is not zero and the document does not claim it is."""))

E.append(dict(id="AD2", clears="AD2: 1.6's hyperparameter statement covers all three", section="1.6",
old="""**`α_Φ = 2.0` and `TIE_EPS = 1e-3` are hyperparameters. The choice is developer taste, and this
document offers no justification for either beyond that.**""",
new="""**`α_Φ = 2.0`, `TIE_EPS = 1e-3` and `TIE_EPS2 = 1e-6` are hyperparameters. The choice is developer
taste, and this document offers no justification for any of them beyond that.**"""))

E.append(dict(id="AD3", clears="AD3: 1.6's sensitivity note covers the second term", section="1.6",
old="""across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}. For `TIE_EPS`, the sink set is unchanged from about **1e-6 to
about 1**, six orders of magnitude, because the term is a tie-break: below that range it falls under
the solver's tolerance and stops registering, and above it the term exceeds the base arc cost of 1""",
new="""across α_Φ ∈ {1, 1.5, 2, 3, 4, 8}. For `TIE_EPS`, the sink set is unchanged from about **1e-6 to
about 1**, six orders of magnitude, because the term is a tie-break: below that range it falls under
the solver's tolerance and stops registering, and above it the term exceeds the base arc cost of 1"""))

E.append(dict(id="AD4", clears="AD4: 1.1's cost range includes the second term", section="1.1",
old="""  `Σ (flow × cost)` with `cost ∈ [1, 1 + TIE_EPS]`, so the optimum minimises a hop count in which a
  hop between two wealthy nodes counts marginally more (§2.3). At `TIE_EPS = 1e-3` the spread is under""",
new="""  `Σ (flow × cost)` with `cost ∈ [1, 1 + TIE_EPS + TIE_EPS2]`, so the optimum minimises a hop count in
  which a hop between two wealthy nodes counts marginally more (§2.3). At those values the spread is under"""))

patch_lib.apply(E)
