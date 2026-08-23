# -*- coding: utf-8 -*-
"""v6.1 batch AN -- the front matter. Its v6.1 paragraph still reports a per-good residue that is now
zero and counts two changes where there are three; its coverage paragraph has picked up duplication
across several edits."""
import patch_lib
E = []

E.append(dict(id="AN1", clears="AN1: what v6.1 changes, with the residue gone", section="0",
old="""**v6.1** changes two things, both in the operator rather than the field. **Phase 2's min-cost flow is
degenerate under unit arc costs, so presentation order selected which optimum was returned; §2.3 now
breaks that tie inside the objective, and §1.6 measures the installed orientation as unchanged across
every relabelling tried.** A canonical node order remains an emitter requirement — a residue of
per-good order-sensitivity survives (§2.4 item 1) — but it is no longer what decides the installed
map. And **`α_Φ` moves from 1.5 to 2.0.** `α_Φ` and the two new tie-break constants `TIE_EPS` and
`TIE_EPS2` are hyperparameters whose values are developer taste; §2.3 states them and offers no
justification for any of them, and every derivation previously offered for `α_Φ` is withdrawn without
replacement. The 1444 sink set moves from `{english_channel, hangzhou}` to `{genua, hangzhou}` and 29
of the 59 figures `measure6.py` prints move with it.""",
new="""**v6.1** changes the operator, not the field. **Phase 2's min-cost flow is degenerate under unit arc
costs, so presentation order selected which optimum was returned.** §2.3 now breaks that tie inside
the objective, in two terms — one carrying the design intent, one generic — and **pins the solver's
optimality tolerance, which turned out to be a correctness requirement rather than a performance
knob**: the margin by which the tie-break makes the optimum unique is as small as 3.8e-8, and HiGHS's
default tolerance is 1e-7, so the solver could stop either side of it. With all three in place the
orientation is unchanged across every relabelling tried — **0 of 180 on the aggregate and 0 of 290 per
good** — and unchanged under permutation of the LP's column order. A canonical node order remains an
emitter requirement because that is a measurement rather than a proof, but it is no longer what
decides the map.

And **`α_Φ` moves from 1.5 to 2.0.** `α_Φ`, `TIE_EPS` and `TIE_EPS2` are hyperparameters whose values
are developer taste; §2.3 states them and offers no justification for any of them, and every
derivation previously offered for `α_Φ` is withdrawn without replacement. The 1444 sink set moves from
`{english_channel, hangzhou}` to `{genua, hangzhou}` and 29 of the 59 figures `measure6.py` prints
move with it. §2.2 records what multiplayer would additionally need, which is now build discipline
rather than a design change."""))

E.append(dict(id="AN2", clears="AN2: the coverage paragraph, deduplicated", section="0",
old="""**`verify6.py` checks figures in this document against values computed from the install, and it
covers well under half of what the document prints.** No count is given here: some of its checks are
generated per matching phrase, so the total moves whenever the prose does. The harness prints its own
count when it runs, and that is where to read it. No ratio is offered, because the denominator is not well defined — counting "the figures the
spec prints" gives anywhere from 279 to 326 depending on how a numeric token is delimited, so any
proportion built on it says more about the tokeniser than about the harness. `scripts/coverage6.py`
reports what is guarded among the figures it can locate unambiguously, and it should be re-run rather
than quoted. Some figures carry a script attribution instead of a guard, and a few carry neither. `scripts/coverage6.py` measures that honestly — it corrupts each spec-printed figure whether
the harness looks at it or not — and it should be re-run rather than quoted here, because the number
moves with every edit to the document.""",
new="""**`verify6.py` checks figures in this document against values computed from the install, and it
covers well under half of what the document prints.** Neither a count nor a ratio is given here, for
two different reasons. The count moves whenever the prose does, because some checks are generated per
matching phrase — the harness prints its own count when it runs, and that is where to read it. The
ratio has no well-defined denominator: counting "the figures the spec prints" gives anywhere from 279
to 326 depending on how a numeric token is delimited, so any proportion built on it says more about
the tokeniser than about the harness. `scripts/coverage6.py` is the honest measure — it corrupts each
spec-printed figure whether the harness looks at it or not — and it should be re-run rather than
quoted, because its number also moves with every edit. Some figures carry a script attribution
instead of a guard, and a few carry neither."""))

patch_lib.apply(E)
