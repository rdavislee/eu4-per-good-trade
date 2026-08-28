# -*- coding: utf-8 -*-
"""v6.1 batch F -- 2.3's constants and 0's front-matter summary. alpha and epsilon are declared as
hyperparameters chosen by taste, with every derivation withdrawn and none substituted."""
import patch_lib
E = []

E.append(dict(id="F1", clears="F1: 2.3 declares both hyperparameters and justifies neither",
section="2.3",
old="""Design constants: the excluded-goods list (defaults to gold), the α price anchor `P₀ = 2.0`,
the aggregate-graph exponent `α_Φ = 1.5` (a **stipulated** constant like `P₀`: superlinear, round,
and chosen rather than derived — world-responsiveness flows through wealth, never through this
knob). **Every derivation previously offered for it is withdrawn.** v2.1 through v4.0 said 1.5 was
calibrated so that 1444 yields a two-sink map; v5.0 said it sat in the widest sink-count band.
Neither is a reason: the first fits a constant to one date, and the second depended on where the α
scan was truncated (§1.6). Any future change to it is a design decision about how many ends the
installed graph should have, and should be recorded as one, and DRAIN's three knobs at their
defaults — demand-mass""",
new="""Design constants: the excluded-goods list (defaults to gold), the α price anchor `P₀ = 2.0`,
the aggregate-graph exponent `α_Φ = 2.0`, the Phase-2 tie-break strength `TIE_EPS = 1e-3`, and
DRAIN's three knobs at their defaults — demand-mass"""))

E.append(dict(id="F2", clears="F2: the hyperparameter statement, and what the tie-break cost is",
section="2.3",
old="""is **not** purely numerical: it is an absolute threshold, so it couples to the scale of `b`. See
§1.6's scale-invariance note and §3.13. A measured calibration option
that moves all three plus α's clamp is recorded in §3.13; the baseline does not use it.""",
new="""is **not** purely numerical: it is an absolute threshold, so it couples to the scale of `b`. See
§1.6's scale-invariance note and §3.13. A measured calibration option
that moves all three plus α's clamp is recorded in §3.13; the baseline does not use it.

**`α_Φ` and `TIE_EPS` are hyperparameters. Their values are developer taste, and this document
offers no justification for either.** Every derivation previously offered for `α_Φ` is withdrawn and
none replaces it: v2.1 through v4.0 said it was calibrated so that 1444 yields a two-sink map, and
v5.0 said it sat in the widest sink-count band. Both are withdrawn. Changing either value is a design
decision, and §1.6 records how the field responds around them so that the decision can be made with
the sensitivity in view — that is documentation for whoever changes them, not an argument for the
current values.

`TIE_EPS` sets the Phase-2 objective. With unit arc costs the min-cost b-flow is degenerate, so the
orientation depends on node numbering; the tie-break puts the choice in the objective instead:

```
cost(u, v) = 1 + TIE_EPS · (w[u] + w[v]) / 2        w = node wealth, normalised to [0, 1]
```

Two properties are load-bearing and neither is a matter of taste. The cost is **symmetric** in the
arc: a directional preference of the form `1 − ε·(w[v] − w[u])` is a potential difference, so its
total over any flow satisfying the same `b` equals `Σ_n w[n]·b[n]` — identical for every feasible
routing, and unable to break a tie. And it reads **node wealth only**, so it is invariant under
relabelling by construction. The normalisation is not load-bearing: dividing by the maximum, the mean
or the world total gives the same orientation, because rescaling `w` is equivalent to rescaling
`TIE_EPS` and the answer is constant over about six orders of magnitude of it (§1.6).

Only DRAIN's Phase 2 uses this cost. The per-good flow operators in `flowop.py` and the checks in
`verify.py` keep unit arc costs, and `mincost_flow`'s cost argument defaults to unit for that reason."""))

E.append(dict(id="F3", clears="F3: the front matter's summary of the node-order issue", section="0",
old="""`add_base_*` accumulation, and the `is_city` filter the engine does not apply), and §2.4 now states
the reason a canonical node order is a correctness requirement: **Phase 2's min-cost flow is
degenerate, so presentation order selects which optimum is returned.**""",
new="""`add_base_*` accumulation, and the `is_city` filter the engine does not apply). **Phase 2's min-cost
flow is degenerate under unit arc costs, so presentation order selected which optimum was returned;
§2.3 now breaks that tie inside the objective, and §1.6 measures the orientation as unchanged across
every relabelling tried.** A canonical node order remains an emitter requirement, but it is no longer
what decides the map."""))

patch_lib.apply(E)
