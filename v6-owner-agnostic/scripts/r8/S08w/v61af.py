# -*- coding: utf-8 -*-
"""v6.1 batch AF -- 2.3 tidy: three constants not two, both terms set the objective, and one
paragraph restated figures already given four paragraphs earlier."""
import patch_lib
E = []

E.append(dict(id="AF1", clears="AF1: three constants, not two", section="2.3",
old="""v5.0 said it sat in the widest sink-count band. Both are withdrawn. Changing either value is a design
decision, and §1.6 records how the field responds around them so that the decision can be made with
the sensitivity in view — that is documentation for whoever changes them, not an argument for the
current values.

`TIE_EPS` sets the Phase-2 objective. With unit arc costs the min-cost b-flow is degenerate, so the
orientation depends on node numbering; the tie-break puts the choice in the objective instead:""",
new="""v5.0 said it sat in the widest sink-count band. Both are withdrawn. Changing any of the three is a
design decision, and §1.6 records how the field responds around them so that the decision can be made
with the sensitivity in view — that is documentation for whoever changes them, not an argument for the
current values.

`TIE_EPS` and `TIE_EPS2` together set the Phase-2 objective. With unit arc costs the min-cost b-flow
is degenerate, so the orientation depends on node numbering; the tie-break puts the choice in the
objective instead:"""))

E.append(dict(id="AF2", clears="AF2: drop the paragraph that restates figures given above",
section="2.3",
old="""**A single cost vector does not make every solve unique, and §2.4 item 1 measures what is left.**
Uniqueness of an LP optimum depends on the right-hand side as well as the objective: `b_w` has no zero
entries and its optimum is unique under the first-order term alone, while each `b_g` puts a different
face of the polytope in play and 18 of the 29 admitted an alternative optimum before the second-order
term. With it, that falls to 1 good and per-good relabelling sensitivity to 13 of 290 runs. The
residue is not zero and the document does not claim it is.

**DLC state is a third input axis.**""",
new="""**DLC state is a third input axis.**"""))

patch_lib.apply(E)
