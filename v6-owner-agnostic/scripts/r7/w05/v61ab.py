# -*- coding: utf-8 -*-
"""v6.1 batch AB -- the front matter and 2.3's constants list and hyperparameter statement all name
one tie-break constant where there are now two."""
import patch_lib
E = []

E.append(dict(id="AB1", clears="AB1: the front matter's account of v6.1", section="0",
old="""**v6.1** changes two things, both in the operator rather than the field. **Phase 2's min-cost flow is
degenerate under unit arc costs, so presentation order selected which optimum was returned; §2.3 now
breaks that tie inside the objective, and §1.6 measures the installed orientation as unchanged across
every relabelling tried.** A canonical node order remains an emitter requirement — the per-good
graphs are still order-sensitive (§2.4 item 1) — but it is no longer what decides the installed map.
And **`α_Φ` moves from 1.5 to 2.0.** Both `α_Φ` and the new `TIE_EPS` are hyperparameters whose values
are developer taste; §2.3 states them and offers no justification for either, and every derivation
previously offered for `α_Φ` is withdrawn without replacement. The 1444 sink set moves from
`{english_channel, hangzhou}` to `{genua, hangzhou}` and 29 of the 59 figures `measure6.py` prints
move with it.""",
new="""**v6.1** changes two things, both in the operator rather than the field. **Phase 2's min-cost flow is
degenerate under unit arc costs, so presentation order selected which optimum was returned; §2.3 now
breaks that tie inside the objective, and §1.6 measures the installed orientation as unchanged across
every relabelling tried.** A canonical node order remains an emitter requirement — a residue of
per-good order-sensitivity survives (§2.4 item 1) — but it is no longer what decides the installed
map. And **`α_Φ` moves from 1.5 to 2.0.** `α_Φ` and the two new tie-break constants `TIE_EPS` and
`TIE_EPS2` are hyperparameters whose values are developer taste; §2.3 states them and offers no
justification for any of them, and every derivation previously offered for `α_Φ` is withdrawn without
replacement. The 1444 sink set moves from `{english_channel, hangzhou}` to `{genua, hangzhou}` and 29
of the 59 figures `measure6.py` prints move with it."""))

E.append(dict(id="AB2", clears="AB2: 2.3's constants list carries both tie-break terms", section="2.3",
old="""the aggregate-graph exponent `α_Φ = 2.0`, the Phase-2 tie-break strength `TIE_EPS = 1e-3`, and
DRAIN's three knobs at their defaults — demand-mass""",
new="""the aggregate-graph exponent `α_Φ = 2.0`, the Phase-2 tie-break strengths `TIE_EPS = 1e-3` and
`TIE_EPS2 = 1e-6`, and
DRAIN's three knobs at their defaults — demand-mass"""))

E.append(dict(id="AB3", clears="AB3: 2.3's hyperparameter statement covers all three", section="2.3",
old="""**`α_Φ` and `TIE_EPS` are hyperparameters. Their values are developer taste, and this document
offers no justification for either.** Every derivation previously offered for `α_Φ` is withdrawn and""",
new="""**`α_Φ`, `TIE_EPS` and `TIE_EPS2` are hyperparameters. Their values are developer taste, and this
document offers no justification for any of them.** Every derivation previously offered for `α_Φ` is withdrawn and"""))

patch_lib.apply(E)
