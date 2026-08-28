# -*- coding: utf-8 -*-
"""v6.1 batch G -- 2.4 item 1 and item 2. The tie-breaking objective the section said was not adopted
has been adopted, and the reason a canonical order is still required has changed: the AGGREGATE graph
is now order-invariant, the PER-GOOD graphs are not."""
import patch_lib
E = []

E.append(dict(id="G1", clears="G1: 2.4 item 1, rewritten around the adopted tie-break", section="2.4",
old="""1. **Declaration order** — emit in decreasing `Φ_w` marking order. This is the convention the
   engine states and the shipped vanilla file follows (0 of 159 links violate it), and violating
   it is non-fatal but logs one error per link. **The node order itself is a correctness
   requirement, not a convention, and the reason is Phase 2 rather than any tiebreak.** The
   min-cost b-flow is *massively degenerate*: many distinct supports carry the same optimal cost, and
   which one the solver returns depends on the order the nodes and arcs are presented in. Measured on
   1444, relabelling the nodes and running the aggregate graph end-to-end changed the orientation in
   **400 of 400** runs across four independent seeds, **always** by returning a different optimal
   vertex and **never** by a sweep tiebreak, with a mean of **25 of 159 edges** moving and the LP
   objective identical to within four units in the last place — 4.44e-16 absolute against an objective
   of 0.712, which is the same quantity as the 6.2e-16 relative deviation and not a second measurement,
   and which grows to 6–7 ULP at larger trial counts, so it is a sample maximum rather than a bound
   (`relabel6.py`, which validates its instrument against
   `drain.py` on the identity permutation and aborts if that fails). Twenty-five flips is the same
   magnitude as the razed-China perturbation §2.8 treats as a major world event. The same effect on the
   **per-good** graphs is 580 of 580 (29 goods × 20 relabellings), from
   `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`. *(v6.0 withdrew that sweep on the ground that
   its script had never shipped. The script is in the tree and runs; the withdrawal was the error, not
   the figure. No v1–v5 spec ever printed it either, so it was never "quoted by earlier versions" —
   it comes from this project's working files.)*

   So the emitter must fix one canonical node order and keep it stable across rebuilds, and that
   order must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks
   ties in. Everything §1.6 and §2.8 report about stability is measured **at fixed node order**;
   re-order the same world and the map moves, with `α_Φ` and every input held fixed. The specific counts
   are HiGHS-specific in their detail but not in kind — any simplex returns *a* vertex of a degenerate
   optimal face. Making the orientation independent of presentation order would need a tie-breaking
   objective (a lexicographic secondary cost, or a strictly convex perturbation); that is a design
   change and is not adopted here.""",
new="""1. **Declaration order** — emit in decreasing `Φ_w` marking order. This is the convention the
   engine states and the shipped vanilla file follows (0 of 159 links violate it), and violating
   it is non-fatal but logs one error per link. **A canonical node order is still a correctness
   requirement, but it is no longer what decides the installed map.** The reason is worth setting out
   in full, because it changed in v6.1 and the previous version's argument was the opposite.

   Phase 2's min-cost b-flow is degenerate under unit arc costs: many distinct supports carry the same
   optimal cost, and which one the solver returns depends on the order the nodes and arcs are presented
   in. Measured on that objective, **40 of 40** permutations return a different optimal support at an
   objective identical to within a few units in the last place. §2.3 now breaks those ties inside the
   objective. On the same LP under the tie-break cost, **0 of 40** permutations return a different
   support, and running the aggregate graph end-to-end over **180 relabellings** (three seeds of 60)
   moved **0 of 159 edges** in every run (`relabel6.py`, which validates its instrument against
   `drain.py` on the identity permutation and aborts if that fails — and did abort when the tie-break
   went in, because the instrument still minimised the old objective and disagreed on 26 of 159 edges).

   **The per-good graphs are a different matter, and this is why the requirement survives.** The
   tie-break cost is built from node wealth, which is good-independent, so it applies to every per-good
   solve — but a wealth-weighted cost need not break ties in a per-good LP, whose `b` is a different
   vector. Measured across 29 goods × 10 relabellings: **84 of 290** runs changed a per-good
   orientation, a mean of 0.99 edges and up to 15. So the installed aggregate graph is invariant over
   the orderings tried, while the per-good graphs — which set value weights and the §1.10 survival
   table — are not.

   So the emitter must fix one canonical node order and keep it stable across rebuilds, and that
   order must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks
   ties in. The counts are HiGHS-specific in their detail but not in kind — any simplex returns *a*
   vertex of a degenerate optimal face, and the tie-break's job is to leave only one vertex to return.
   *(v6.0 quoted a 580-of-580 per-good sweep from
   `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`. That script measures the unit-cost objective,
   so its figure describes the former solver and is superseded by the 84-of-290 above rather than
   contradicted by it.)*"""))

E.append(dict(id="G2", clears="G2: item 2's end-flag list is no longer order-dependent", section="2.4",
old="""2. **End flags** — `end=yes` on every `Φ_w` sink. **This list is a function of the canonical node
   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end in about
   98% of relabellings, `english_channel` in about 40%, and the count ranges 1 to 5 (§1.6). Fix the order, emit, and keep it — changing it changes the flags without anything in the
   world changing. (1444, shipped order: **two** end nodes, `english_channel` and
   `hangzhou`, against
   vanilla's three); stripped from any former end node that gains outgoing links. The count is not
   fixed — it follows the wealth field and `α_Φ` (§1.6), so the emitter reads it from the solve
   rather than assuming a number.""",
new="""2. **End flags** — `end=yes` on every `Φ_w` sink. **This list is a function of the world, not of the
   node order:** across the 180 relabellings in item 1 the end set came back as
   `{genua, hangzhou}` every time (§1.6). That is a change from v6.0, where the list moved with the
   ordering and this item warned about it. (1444: **two** end nodes, `genua` and `hangzhou`, against
   vanilla's three); stripped from any former end node that gains outgoing links. The count is not
   fixed — it follows the wealth field and `α_Φ` (§1.6), so the emitter reads it from the solve
   rather than assuming a number."""))

patch_lib.apply(E)
