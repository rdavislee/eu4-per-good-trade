# -*- coding: utf-8 -*-
"""v6 batch 7 — the algorithm: X009/X010/X125 (fallback reachability), H1 (LP degeneracy as the
real reason a canonical order is required), and the end-flag count."""
import patch_lib
E = []

E.append(dict(id="R7-fallback", clears="X009/X010/X125: what the fallback needs, stated correctly",
section="1.1",
old="""flow-terminal demander, so the fallback fires only when every candidate is support-isolated with
zero balance — on a connected core, only when `b ≡ 0` across it. That happens for the aggregate
graph on a uniform-wealth map, and for a per-good graph on a component with no producer and no
consumer. In those cases the candidates are usually all *zero-wealth*, the wealth key ties, and the
**index decides** — which is why §2.4 item 1 makes a canonical emitter node order a correctness
requirement rather than a convention, and why §2.8 asserts containment over a set that includes the
fallbacks.""",
new="""flow-terminal demander, so the fallback fires only when every candidate is support-isolated with
zero **post-peel** balance. The balance the key reads is the one Phase 0 hands on, with each
pendant's balance folded into its parent — not the raw input `b` — so the condition is about the
folded field and a map with non-zero raw balances can still reach the branch. On a connected core it
needs the folded balance to vanish across the core: for a per-good graph that is a component with no
producer and no consumer, and for the aggregate graph it needs each node's `Σ wealth^α_Φ` to be
equal, which uniform *wealth* gives but is not the same condition. Where the wealth key then ties,
the **node index decides** — that is why §2.8 asserts containment over a set that includes the
fallbacks. It is not the reason §2.4 requires a canonical node order; that requirement is stronger
and is set by Phase 2 (§2.4 item 1)."""))

E.append(dict(id="R7-order", clears="H1: the canonical-order requirement comes from Phase 2's LP",
section="2.4",
old="""   it is non-fatal but logs one error per link. **The node order itself is a correctness
   requirement, not a convention**: §1.1's priority key breaks exact ties by node index, and on the
   fallback branch (§3.2, T3) the wealth key ties and the index alone decides the orientation. The
   emitter must therefore fix one canonical node order and keep it stable across rebuilds, or the
   same world can produce two different maps.""",
new="""   it is non-fatal but logs one error per link. **The node order itself is a correctness
   requirement, not a convention, and the reason is Phase 2 rather than any tiebreak.** The
   min-cost b-flow is *massively degenerate*: many distinct supports carry the same optimal cost, and
   which one the solver returns depends on the order the nodes and arcs are presented in. Measured on
   1444, relabelling the nodes and running end-to-end changed the orientation on **580 of 580**
   runs (29 goods × 20 relabellings), **always** by returning a different optimal vertex and **never**
   by a sweep tiebreak, with a mean of **22.1 of 159 edges** moving and the objective identical to
   8.9e-16. Independently, permuting only the arc presentation order with node labels held fixed
   changes the optimal support on **10 of 10 goods** tested, with objective gaps ≤ 1.8e-15. Twenty-two
   flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event.

   So the emitter must fix one canonical node order and keep it stable across rebuilds, and that
   order must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks
   ties in. Everything §1.6 and §2.8 report about stability is measured **at fixed node order**;
   under (`α_Φ` fixed) a re-ordering of the same world, the map moves. The specific 580/580 result is
   HiGHS-specific in its detail but not in kind — any simplex returns *a* vertex of a degenerate
   optimal face. Making the orientation independent of presentation order would need a tie-breaking
   objective (a lexicographic secondary cost, or a strictly convex perturbation); that is a design
   change and is not adopted here.

   §1.1's priority key also breaks exact ties by node index, which matters wherever the key ties —
   and the key ties in more places than §1.1 documents: besides the free-edge sweep it decides
   Phase 1's within-cluster argmin, the stall promotion's identical form, and the top-k cut when two
   clusters carry equal mass. **None of them fires on 1444** (zero exact `(DEF, β)` ties on free
   edges across 29/29 goods, zero within-cluster β ties, zero tied cluster masses), so no measured
   figure here depends on them."""))

E.append(dict(id="R7-endflag", clears="the end-flag count follows the field", section="2.4",
old="""2. **End flags** — `end=yes` on every `Φ_w` sink (1444: **one** end node, `hangzhou`, against""",
new="""2. **End flags** — `end=yes` on every `Φ_w` sink (1444: **two** end nodes, `english_channel` and
   `hangzhou`, against"""))

patch_lib.apply(E)
