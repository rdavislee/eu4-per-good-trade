# -*- coding: utf-8 -*-
"""v6.1 batch M -- 1.1's Efficiency property. The objective is no longer flow x hops, so the property
has to be restated rather than kept: it is now a wealth-weighted hop count."""
import patch_lib
E = [dict(id="M1", clears="M1: the Efficiency property under the tie-break objective", section="1.1",
old="""- **Efficiency.** Unit costs make the certificate flow a fewest-hop routing in aggregate — the
  objective *is* `Σ (flow × hops)`, so the optimum minimises total flow-hops. No per-unit
  shortest-path claim is made, and none holds: a unit may detour when sink assignment demands it.
  **This one carries no measurement and wants none:** it is true by construction of the LP, and
  any hop count we produced would be re-deriving the objective rather than testing it. The §3.13
  calibration deliberately degrades it, which is a change to the program being solved, not
  evidence about this property.""",
new="""- **Efficiency.** The certificate flow is a near-fewest-hop routing in aggregate. With unit costs the
  objective would be exactly `Σ (flow × hops)`; the tie-break makes it
  `Σ (flow × cost)` with `cost ∈ [1, 1 + TIE_EPS]`, so the optimum minimises a hop count in which a
  hop between two wealthy nodes counts marginally more (§2.3). At `TIE_EPS = 1e-3` the spread is under
  a tenth of a percent of the base cost, so the routing is within that factor of fewest-hop — but
  "fewest-hop" is now an approximation with a stated bound rather than an identity, and that is the
  price of a unique optimum. No per-unit shortest-path claim is made, and none holds: a unit may
  detour when sink assignment demands it.
  **This one carries no measurement and wants none:** it follows from the construction of the LP, and
  any hop count we produced would be re-deriving the objective rather than testing it. The §3.13
  calibration deliberately degrades it, which is a change to the program being solved, not
  evidence about this property."""),]
patch_lib.apply(E)
