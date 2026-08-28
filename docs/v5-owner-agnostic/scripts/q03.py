# -*- coding: utf-8 -*-
"""v5 batch 3 — Group C, the algorithm's fallback branch (changes 19–24)."""
import patch_lib
E = []

E.append(dict(id="C19-C21", clears="changes 19-21: 3.2 claim 1", section="3.2",
old="""1. **Sink placement:** on a map where Phase 0 is a no-op, final sinks =
   `{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal demanders}` — measured exact,
   29/29 goods. **This is a measurement, not a theorem**, and v2 asserted it as a theorem. Two
   constructed inputs break it, both run through a faithful implementation of §1.1:
   - **T1 — pendant importer.** Triangle A(+5), B(−3), D(0) with a leaf C(−2) on B. Phase 0 peels C,
     Phase 4 restores the edge B→C, and the actual sinks are `{C}` while the formula set is `{B}`.
     The pendant is a sink outside the set **and** it strips the selected sink of its sinkhood.
   - **T2 — free-edge race, inside the 2-core.** Five-cycle S1(+3)–u1(−3)–w(0)–u2(−2)–S2(+2)–S1 with a
     chord w–S1. Both u1 and u2 are selected flow-terminal demanders. Under the adopted
     DEF-ascending key u2 pops first, the conduit w becomes ready via its free edge to u2 and pops
     before u1, so the free edge orients u1→w and u1 is no longer a sink. Actual `{u2}`, formula
     `{u1, u2}`.

   What survives unconditionally is the ⊆-direction *within the 2-core*: every core node that is
   neither selected nor promoted is given an out-arc by the sweep, either a flow arc or a free
   edge to an earlier-marked node. Pendant net-importers are the only sinks outside the set, and
   the free-edge race is the only way a node inside it drops out. §2.8 therefore carries **two**
   runtime checks rather than one weakened one: containment inside the 2-core is asserted
   unconditionally every tick, and the equality is *monitored* every tick with T2 named as its
   legitimate failure. On pendant edges the Phase-4 orientation rule is the check and T1 is
   expected output. Written as a single assertion with an escape clause, both counterexamples
   would disappear into the clause.""",
new="""1. **Sink placement:** on a map where Phase 0 is a no-op and no fallback fires, final sinks =
   `{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal demanders}` — measured exact,
   29/29 goods. **This is a measurement, not a theorem**, and v2 asserted it as a theorem. Three
   constructed inputs break it, all run through a faithful implementation of §1.1 (`toys.py`):
   - **T1 — pendant importer.** Triangle A(+5), B(−3), D(0) with a leaf C(−2) on B. Phase 0 peels C,
     Phase 4 restores the edge B→C, and the actual sinks are `{C}` while the formula set is `{B}`.
     The pendant is a sink outside the set **and** it strips the selected sink of its sinkhood.
   - **T2 — free-edge race, inside the 2-core.** Five-cycle S1(+3)–u1(−3)–w(0)–u2(−2)–S2(+2)–S1 with a
     chord w–S1. Both u1 and u2 are selected flow-terminal demanders. Under the adopted
     DEF-ascending key u2 pops first, the conduit w becomes ready via its free edge to u2 and pops
     before u1, so the free edge orients u1→w and u1 is no longer a sink. Actual `{u2}`, formula
     `{u1, u2}`.
   - **T3 — the fallback branch, inside the 2-core.** Triangle A, B, C with `b = 0` at all three and
     node wealth 3, 2, 1. No node is a demander, so Phase 1 selects nothing; there is no flow, so
     every edge is free; no node is ready, so the sweep stalls with no flow-terminal demander and
     the fallback promotes A. Free edges then orient B→A, C→A, C→B. Actual sinks `{A}`, formula set
     empty — and A is in neither `{selected}` nor `{promoted}`.

   What survives unconditionally is the ⊆-direction *within the 2-core*, over the set the sweep
   actually maintains: every core node that is neither selected, promoted **nor fallback-promoted**
   is given an out-arc by the sweep, either a flow arc or a free edge to an earlier-marked node.
   Pendant net-importers are the only sinks outside that set. §2.8 therefore carries **two** runtime
   checks rather than one weakened one: containment inside the 2-core is asserted unconditionally
   every tick against `{selected} ∪ {promoted} ∪ {fallbacks}`, and the equality is *monitored* every
   tick with **T2 and T3** named as its legitimate failures. On pendant edges the Phase-4
   orientation rule is the check and T1 is expected output. Written as a single assertion with an
   escape clause, all three counterexamples would disappear into the clause — and written against
   the narrower containment set, T3 would halt the solver on correct behaviour."""))

E.append(dict(id="C22", clears="change 22: 3.2 item 2's index claim", section="3.2",
old="""2. **Free-edge direction:** marking order under the (DEF asc, b asc, index) priority — a function
   of the graph and the balances; zero exact key ties measured, so the index never decides.""",
new="""2. **Free-edge direction:** marking order under the (DEF asc, b asc, index) priority. This is
   **deterministic** by construction; that it is a function of the graph and the balances *alone* —
   that the node indexing never decides — is **measured, not proved**, and holds where the key has
   no exact ties: zero exact `(DEF, b)` ties on free edges, 29/29 goods on 1444. The one place the
   indexing is load-bearing is the fallback branch (T3 above), where the candidates are typically
   all zero-wealth and tied; §2.4 item 1 makes a canonical node order a correctness requirement for
   that reason."""))

E.append(dict(id="C23", clears="change 23: the fallback's reachability", section="1.1",
new="""the **highest-wealth** candidate instead, ties by index: that is the **fallback** branch, and node
wealth is a good-independent input so it needs no bootstrap. (*Candidates* at a stall are the
unmarked nodes whose flow out-neighbours are all marked; the flow subgraph is acyclic, so at least
one always exists and the sweep always advances.) **Where this branch is reachable, and what decides
there.** A candidate carrying any flow out-arc is already *ready*, and a candidate with inflow is a
flow-terminal demander, so the fallback fires only when every candidate is support-isolated with
zero balance — on a connected core, only when `b ≡ 0` across it. That happens for the aggregate
graph on a uniform-wealth map, and for a per-good graph on a component with no producer and no
consumer. In those cases the candidates are usually all *zero-wealth*, the wealth key ties, and the
**index decides** — which is why §2.4 item 1 makes a canonical emitter node order a correctness
requirement rather than a convention, and why §2.8 asserts containment over a set that includes the
fallbacks. Free""",
old="""the **highest-wealth** candidate instead, ties by index: that is the **fallback** branch, it is what
a pocket with no net demander needs, and node wealth is a good-independent input so it needs no
bootstrap. (*Candidates* at a stall are the unmarked nodes whose flow out-neighbours are all marked;
the flow subgraph is acyclic, so at least one always exists and the sweep always advances.) Free"""))

E.append(dict(id="C24", clears="change 24: 2.4 item 1", section="2.4",
old="""1. **Declaration order** — emit in decreasing `Φ_w` marking order. This is the convention the
   engine states and the shipped vanilla file follows (0 of 159 links violate it), and violating
   it is non-fatal but logs one error per link.""",
new="""1. **Declaration order** — emit in decreasing `Φ_w` marking order. This is the convention the
   engine states and the shipped vanilla file follows (0 of 159 links violate it), and violating
   it is non-fatal but logs one error per link. **The node order itself is a correctness
   requirement, not a convention**: §1.1's priority key breaks exact ties by node index, and on the
   fallback branch (§3.2, T3) the wealth key ties and the index alone decides the orientation. The
   emitter must therefore fix one canonical node order and keep it stable across rebuilds, or the
   same world can produce two different maps."""))

patch_lib.apply(E)
