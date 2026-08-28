# -*- coding: utf-8 -*-
"""v6.1 batch X -- tidy 3.9's Phi_ord bullet. Batch I3 removed the relabelling figures and left two
overlapping disclaimers plus a 'those ends' whose antecedent went with them."""
import patch_lib
E = [dict(id="X1", clears="X1: one disclaimer, and a live antecedent", section="3.9",
old="""  artifacts of sweep scheduling rather than places — and the sharpest evidence for that is what
  relabelling does to them: its end count and end set both move with the node order, where `Φ_w`'s do
  not (§2.4 item 1 measures the installed graph as invariant over the orderings tried). No figure is
  given for `Φ_ord`'s spread, because the operator is not installed and R3 forbids maintaining one.
  Most of those ends terminate no good,
  none of the demand capitals is among them, and the end count does not concentrate as demand
  concentrates. *No figure is maintained for it here.* It is not the installed operator, its numbers
  moved with every change to the wealth field, and three successive audits spent their effort
  recounting them; the design argument above does not depend on any of them.""",
new="""  artifacts of sweep scheduling rather than places — and the sharpest evidence for that is what
  relabelling does to them: its end count and end set both move with the node order, where `Φ_w`'s do
  not (§2.4 item 1 measures the installed graph as invariant over the orderings tried). Most of
  `Φ_ord`'s ends terminate no good, none of the demand capitals is among them, and the end count does
  not concentrate as demand concentrates. *No figure is quoted for any of that here*: the operator is
  not installed, its numbers moved with every change to the wealth field, three successive audits
  spent their effort recounting them, and the design argument above depends on none of them.""")]
patch_lib.apply(E)
