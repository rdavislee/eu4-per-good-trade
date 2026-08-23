# Claim Census — Per-Good Trade Network Spec v6.1

Complete census of the claims in `per-good-trade-spec.md` (v6.1, 1,861 lines, MD5
`bf5b0e536a7a6c20b5c3e2c72d013021`), one row per claim. **Tenth inventory** of this version's
document. Enumeration only: nothing here is graded, corrected, or checked for truth.

**ID continuity.** The previous inventory, `scripts/claims-v6-round9.md`, was a full census of the
v6.0 text carrying `Y001`–`Y964`. Every one of those IDs that still sits on a proposition in this
document is carried here unchanged, matched by text rather than by position, even where v6.1
rewrote the wording or moved the figure. Seven round-9 IDs are **retired** — their proposition is
no longer in the document — and are listed in the summary; those numbers are not reused. Genuinely
new propositions take fresh IDs from **Y965** upward, in document order. No number is reused and no
gap is closed.

**Status** is measured against v5.0 (`../v5-owner-agnostic/per-good-trade-spec.md`) by direct text
diff, not by reading `changes-v6.md`. At paragraph granularity the two documents differ in **64
replaced groups and 1 inserted group (v6.1 L976–1010), 0 deleted**, so every line outside those
groups is byte-identical to v5.0 and its claims are `UNCHANGED` by construction. Inside a replaced
group each proposition was compared with the v5.0 text it replaced: `CHANGED` where the same
proposition is stated differently, `NEW` where v5.0 has no counterpart, `REMOVED` where v6.1 has
none. Note the consequence for v6.1's own edits: a proposition v6.0 inherited from v5.0 unchanged
and v6.1 then rewrote is `CHANGED` here where round 9 had it `UNCHANGED` (the Phase-2 arc costs, the
fewest-hop property, `α_Φ`'s value), while a proposition round 9 already scored `NEW` or `CHANGED`
keeps that score even where v6.1 moved its numbers, because the v5.0 comparison is unaffected.
`REMOVED` rows carry v5.0 line numbers and a `(v5)` section marker; every other locator is a v6.1
line number.

**Provenance** records how the document says it knows, in the fixed vocabulary. `numerical test` is
a computation over the model's own data; `engine test` is an observation of the running game;
`measured in-game` is a tooltip or window reading; these are never merged. Where the document
states a figure without an instrument, or where the nearest script citation covers a different
quantity, the cell says so as a fact about the page.

---

## §0 — Front matter (L1-69)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y207 | The target build is EU4 1.37.5 Inca. | UNCHANGED | DESIGN | stipulated | L5 `**Target:** EU4 1.37.5 Inca` |
| Y208 | The design is extended-timeline compatible. | UNCHANGED | DESIGN | stipulated | L5 "Extended-timeline compatible" |
| Y209 | The design targets connected maps only. | UNCHANGED | DESIGN | stipulated | L5 "**Connected maps only** — see §2.2" |
| Y210 | This document supersedes v1.3, which lives in `../v1-laplacian/`. | UNCHANGED | MODEL | stipulated | L6 |
| Y211 | v1 oriented each good by a Laplacian potential. | UNCHANGED | MODEL | stipulated | L6-7 |
| Y212 | v1's sink placement was shown to be topological rather than economic. | UNCHANGED | MODEL | cited to `../v1-laplacian/diagnosis.md`; no figure or script named at this line | L7-8 |
| Y213 | A four-operator bake-off replaced the orientation core with the DRAIN algorithm. | UNCHANGED | MODEL | cited to `drain-orientation.md` | L8-9 |
| Y214 | Every claim-audit correction from `../v1-laplacian/validation.md` that is settleable from files is folded into this document. | UNCHANGED | MODEL | stipulated | L9-10 |
| Y215 | v2.1 replaced the installed aggregate `Φ_ord` (the value-weighted marking order) with `Φ_w`, DRAIN run once more with wealth itself as the good. | UNCHANGED | MODEL | stipulated | L10-12 |
| Y216 | This version keeps v3.0's owner-agnostic wealth. | UNCHANGED | DESIGN | stipulated | L14 "keeps v3.0's owner-agnostic wealth" |
| Y001 | v6.0 makes owner-agnosticism true by construction rather than by a rule that has to be policed. | NEW | DESIGN | stipulated | L14-15 |
| Y002 | The substantive change of v6.0 is to §1.3: wealth is a function of the province's development, its trade good and its own current condition, and of nothing else. | CHANGED | DESIGN | stipulated | L15-16 |
| Y003 | The two-test modifier classifier and everything it governed — trade-good modifiers, great projects, permanent province modifiers, buildings, centres of trade and the DLC conditionality — are deleted, along with the whole-install sweep that maintained them. | CHANGED | DESIGN | stipulated | L16-19 |
| Y004 | The two-test classifier is v4.0's; v3.0 used a structural rule about which block of a trade-good definition a modifier sits in; the whole-install sweep is v5.0's alone. | NEW | MODEL | stipulated | L19-21 |
| Y005 | On the 1444 start the deleted apparatus was worth 105.30 ducats — 0.98% of the 10,712.70 the field totalled with it, 0.99% of the 10,607.40 without. | NEW | MODEL | numerical test; no script named at this line — the same figures recur at §1.3 L223-225, also unattributed, and `measure6.py` is first named 115 lines later for a different quantity | L21-22 |
| Y006 | That classification was wrong in both independent audits that examined it (`../v3-owner-agnostic/validation-v3.md` W041 and `../v5-owner-agnostic/validation-v5.md` X035) and was passed by v4.0's own repair harness, which v5.0 then refuted. | CHANGED | MODEL | cited to two named validation documents | L22-25 |
| Y007 | Three start-state reads are corrected in the same pass: `on_startup` devastation, dated `add_base_*` accumulation, and the `is_city` filter the engine does not apply. | NEW | DESIGN | stipulated | L25-26 |
| Y965 | v6.1 changes two things, both in the operator rather than in the field. | NEW | DESIGN | stipulated | L28 |
| Y008 | Phase 2's min-cost flow is degenerate under unit arc costs, so presentation order selected which optimum was returned. | NEW | MODEL | numerical test (argued at §2.3 and §2.4 item 1) | L28-29 |
| Y966 | §2.3 now breaks that tie inside the objective. | NEW | MODEL | stipulated | L29-30 |
| Y967 | §1.6 measures the installed orientation as unchanged across every relabelling tried. | NEW | MODEL | numerical test (§1.6) | L30-31 |
| Y968 | A canonical node order remains an emitter requirement because the per-good graphs are still order-sensitive, but it is no longer what decides the installed map. | NEW | MODEL | numerical test (§2.4 item 1) | L31-33 |
| Y969 | `α_Φ` moves from 1.5 to 2.0. | NEW | MODEL | stipulated | L33 |
| Y970 | Both `α_Φ` and the new `TIE_EPS` are hyperparameters whose values are developer taste, and §2.3 states them and offers no justification for either. | NEW | DESIGN | stipulated | L33-35 |
| Y971 | Every derivation previously offered for `α_Φ` is withdrawn without replacement. | NEW | MODEL | stipulated | L35 |
| Y972 | The 1444 sink set moves from `{english_channel, hangzhou}` to `{genua, hangzhou}`. | NEW | MODEL | numerical test | L35-36 |
| Y973 | 29 of the 59 figures `measure6.py` prints move with the sink set. | NEW | MODEL | numerical test (`measure6.py` named in the same sentence) | L36-37 |
| Y009 | Prose convention: no empirical absolutes — no superlative, no universal quantifier and no threshold asserted as a fact about the world; a claim is either a directional design statement or an observation scoped to the field and script that produced it. | NEW | DESIGN | stipulated | L39-41 |
| Y010 | Prose convention: no maintained figures for any rejected operator — §3.15's graveyard keeps its design arguments and loses its measurements, covering `Φ_ord`, the gravity kernels, the v1 Laplacian, RANK and the seeded basins. | NEW | DESIGN | stipulated | L41-44 |
| Y011 | Those rejected-operator numbers were re-measured and re-refuted in three successive audits, and not one of the rejection arguments depends on them. | NEW | MODEL | stipulated | L43-45 |
| Y220 | Where a comparison is genuinely load-bearing it is stated as a direction rather than as a figure that has to be maintained across every change to the wealth field. | NEW | DESIGN | stipulated | L45-48 |
| Y012 | Every graded claim from `../v5-owner-agnostic/validation-v5.md` — 22 refuted, 39 partial, 1 unverifiable — is folded through, and `fixes-agreed.md` maps each one to the change that answers it. | CHANGED | MODEL | cited to `validation-v5.md` and `fixes-agreed.md` | L50-51 |
| Y218 | Deleted text is quoted in `changes-v6.md`. | CHANGED | MODEL | stipulated (v5 cited `changes-v5.md`) | L52 |
| Y217 | Measured figures carry the script that produced them. | CHANGED | DESIGN | stipulated (v5 said "no figure in v5.0 is unverified") | L52 |
| Y013 | `scripts/verify6.py` reads figures out of the document text and fails when they disagree with a value computed from the install, but it does not cover every figure the document prints. | CHANGED | MODEL | stipulated | L52-54 |
| Y974 | `verify6.py` covers well under half of what the document prints. | NEW | MODEL | unsourced — a proportion asserted while the next sentence declines to give a count; no instrument named at this line | L55-56 |
| Y975 | No count is given here because some of the harness's checks are generated per matching phrase, so the total moves whenever the prose does, and the harness prints its own count when it runs. | NEW | MODEL | stipulated (about the harness's construction) | L56-58 |
| Y015 | No coverage ratio is offered because the denominator is not well defined: counting "the figures the spec prints" gives anywhere from 279 to 326 depending on how a numeric token is delimited, so any proportion built on it says more about the tokeniser than about the harness. | NEW | MODEL | numerical test over the document's own text; the instrument that produced 279-326 is not named | L58-60 |
| Y016 | `scripts/coverage6.py` reports what is guarded among the figures it can locate unambiguously, corrupts each spec-printed figure whether the harness looks at it or not, and should be re-run rather than quoted, because the number moves with every edit to the document. | NEW | DESIGN | stipulated | L60-64 |
| Y017 | Some figures carry a script attribution instead of a guard, and a few carry neither. | NEW | MODEL | unsourced — asserted about the document's own text with no instrument named | L62 |
| Y018 | `scripts/mutate6.py` reports a higher score that should not be read as coverage: it plants errors only in figures `verify6.py` already checks, so it cannot fail — the same circularity v4.0's harness had, recorded rather than quietly fixed. | NEW | MODEL | stipulated | L65-67 |
| Y219 | The document has three sections: §1 Mechanics states what the system does, §2 Implementation states how it is built, §3 Reasoning states why and records what is still unknown. | UNCHANGED | DESIGN | stipulated | L69 |

## §1.1 — Trade direction (L75-189)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y221 | Every trade good has its own directed network over the same adjacency. | UNCHANGED | MODEL | stipulated | L77 |
| Y222 | Direction is computed, never authored. | UNCHANGED | DESIGN | stipulated | L77 |
| Y223 | For each good `g` the balance is `b_g(n) = s_g(n) − c_g(n)`, oriented by DRAIN in four named phases: peel, select, route, sweep. | UNCHANGED | MODEL | stipulated | L79-80 |
| Y224 | Phase 0 repeatedly removes degree-1 nodes, orienting each pendant edge by the sign of its absorbed subtree balance (net exporter toward core, net importer fed from core, zero toward core) and folding the residual into the parent. | UNCHANGED | MODEL | stipulated | L82-84 |
| Y225 | Phase 0 is exact rather than heuristic: every removed edge is a bridge and flow on a tree is determined by conservation. | UNCHANGED | MATH | algebraic derivation | L84-85 |
| Y226 | On the vanilla map Phase 0 is a no-op — minimum degree 2, zero bridges. | UNCHANGED | MODEL | numerical test | L85-86 |
| Y227 | Phase 0 exists for modded maps. | UNCHANGED | DESIGN | stipulated | L86 |
| Y228 | Phase 1 takes the connected clusters of net demanders in the core, computes the Herfindahl index of their demand masses, sets `k = clamp(round(1/HHI), 1, number of clusters)`, and selects the heaviest demander of each of the top-k clusters. | UNCHANGED | MODEL | stipulated | L88-90 |
| Y229 | Phase 1 carries two knobs: a demand-mass quantile `ρ` defaulting to 1.0 and a cluster dilation radius `r` defaulting to 0. | UNCHANGED | MODEL | stipulated | L90-92 |
| Y230 | On vanilla 1444 demand is so ubiquitous that k = 1 for 27 of 29 goods at the default knobs. | UNCHANGED | MODEL | numerical test | L92-93 |
| Y231 | Phase 1's selection is deliberately weak because Phase 3 self-corrects upward. | UNCHANGED | DESIGN | stipulated | L93 |
| Y232 | Phase 2 solves the uncapacitated min-cost flow serving `b_g` and orients every support edge by its net flow. | CHANGED | MODEL | stipulated (v5 specified unit arc costs; v6.1 specifies a near-unit cost) | L95-96 |
| Y976 | Phase 2's arc costs are `1 + TIE_EPS·(w[u] + w[v])/2` — near-unit, symmetric in the arc, and read from node wealth (§2.3). | NEW | MODEL | stipulated | L96-97 |
| Y977 | The costs are not unit because with unit costs the optimum is not unique and which one the solver returns depends on the order the nodes are presented in; the near-unit perturbation leaves one optimum to return. | NEW | MODEL | algebraic derivation | L97-99 |
| Y233 | The support is a spanning-tree basis of at most N−1 edges when the solver returns a basic (vertex) optimum, which the simplex family does. | UNCHANGED | MATH | algebraic derivation | L99-100 |
| Y234 | An interior-point solve without crossover can split flow across equal-length parallel paths and return a support containing an undirected cycle. | UNCHANGED | MATH | algebraic derivation | L100-102 |
| Y235 | §2.2 therefore requires network simplex or a simplex LP. | UNCHANGED | DESIGN | stipulated | L102-103 |
| Y236 | For any optimum the support contains no directed cycle, because with all costs strictly positive a directed cycle could be cancelled for strictly lower cost — an argument that needs positivity rather than unit costs, so it survives the cost change. | CHANGED | MATH | algebraic derivation | L103-106 |
| Y237 | Edges with zero net flow are free and are deferred to Phase 3. | UNCHANGED | MODEL | stipulated | L106 |
| Y238 | Phase 3 marks nodes Kahn-style: a node is ready when every flow out-neighbour is already marked and it is a selected sink, has a flow out-arc, or has a free edge to a marked node. | UNCHANGED | MODEL | stipulated | L108-110 |
| Y239 | Among ready nodes the sweep pops by the priority key (DEF ascending, b ascending, index), where `DEF(v)` is total downstream demand on the flow-arc subgraph. | UNCHANGED | MODEL | stipulated | L110-111 |
| Y240 | The flow-arc subgraph is acyclic and fixed before any free edge, so `DEF` involves no circularity. | UNCHANGED | MATH | algebraic derivation | L111-112 |
| Y241 | On a stall the sweep promotes the heaviest flow-terminal demander among the candidates into the sink set, and this self-correction is what supplies the real sink count. | UNCHANGED | MODEL | stipulated | L112-114 |
| Y242 | If the candidates hold no flow-terminal demander at all, the fallback branch promotes the highest-wealth candidate instead, ties by index. | UNCHANGED | MODEL | stipulated | L114-115 |
| Y243 | Node wealth is a good-independent input, so the fallback branch needs no bootstrap. | UNCHANGED | MODEL | algebraic derivation | L115-116 |
| Y244 | Candidates at a stall are the unmarked nodes whose flow out-neighbours are all marked; because the flow subgraph is acyclic at least one always exists, so the sweep always advances. | UNCHANGED | MATH | algebraic derivation | L116-118 |
| Y245 | A candidate carrying any flow out-arc is already ready, and a candidate with inflow is a flow-terminal demander. | UNCHANGED | MATH | algebraic derivation | L118-120 |
| Y019 | The fallback branch fires only when every candidate is support-isolated with zero post-peel balance. | CHANGED | MODEL | algebraic derivation | L120-121 |
| Y020 | The balance the priority key reads is the one Phase 0 hands on, with each pendant's balance folded into its parent rather than the raw input `b`, so a map with non-zero raw balances can still reach the fallback branch. | NEW | MODEL | algebraic derivation | L121-123 |
| Y021 | On a connected core the fallback needs the folded balance to vanish across the core: for a per-good graph that is a component with no producer and no consumer, and for the aggregate graph it needs each node's sum of `wealth^α_Φ` to be equal, which uniform per-province wealth does not give. | CHANGED | MODEL | algebraic derivation | L123-126 |
| Y022 | Nodes hold between 0 and 72 counted provinces, so equal per-province wealth makes unequal node sums. | NEW | MODEL | numerical test; no script named at this line | L126-127 |
| Y023 | Where the wealth key ties, the node index decides. | CHANGED | MODEL | algebraic derivation | L127-128 |
| Y024 | §2.8's containment set includes the fallbacks because of T3 — a fallback promotion that is a sink in neither the selected nor the promoted set — and not because of the wealth tie, which is incidental; and it is not the reason §2.4 requires a canonical node order, which is a stronger requirement set by Phase 2. | CHANGED | DESIGN | algebraic derivation | L128-131 |
| Y246 | Free edges orient from later-marked to earlier-marked. | UNCHANGED | MODEL | stipulated | L131-132 |
| Y247 | Phase 4 un-peels the Phase-0 pendants in reverse order. | UNCHANGED | MODEL | stipulated | L134 |
| Y248 | Each §1.1 property is labelled proved, measured, or true-by-construction, and the three are never allowed to stand for each other. | UNCHANGED | DESIGN | stipulated | L136-141 |
| Y249 | That labelling discipline caught four over-claims between v2.0 and v3.0. | UNCHANGED | MODEL | stipulated | L140-141 |
| Y250 | The §1.1 property measurements were regenerated for v6.0 by `measure6.py`. | CHANGED | MODEL | computed by a named script (`measure6.py`; v5.0 named `v5measure.py`) | L137 |
| Y251 | Global DAG: every arc points from later-marked to earlier-marked, so reversed marking order is a topological order, and pendant edges are bridges that cannot close a cycle. | UNCHANGED | MATH | algebraic derivation | L143-145 |
| Y252 | Measured acyclic on 29 of 29 goods. | UNCHANGED | MODEL | numerical test | L144-145 |
| Y253 | Every sink is one of four kinds: a selected demand centre that turned out flow-terminal, a stall-promoted flow-terminal demander, a fallback-promoted highest-wealth node, or a Phase-0 pendant that absorbed a net-importing subtree. | UNCHANGED | MODEL | algebraic derivation | L146-148 |
| Y025 | On 1444 the fallback and pendant cases are empty and the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods, 2–8 sinks per good, mean 3.69, zero fallbacks. | CHANGED | MODEL | numerical test | L148-150 |
| Y026 | That equality is a measurement on this input rather than a theorem, and v2 asserted it as one. | CHANGED | MODEL | algebraic derivation | L150-152 |
| Y027 | It does not become a theorem by attaching conditions: "Phase 0 a no-op and no fallback firing" looks sufficient and is not, because T2 satisfies both and still breaks it. | NEW | MODEL | algebraic derivation | L152-153 |
| Y254 | Three constructed cases break the sink-set equality: a pendant net-importing leaf is a sink outside the set (T1); inside the 2-core a selected flow-terminal demander can be handed an out-arc by a free edge to an earlier-marked node and cease to be a sink (T2); and a fallback promotion is a sink that is neither selected nor stall-promoted (T3). | UNCHANGED | MODEL | numerical test (worked in §3.2) | L153-156 |
| Y255 | A node with no outgoing links for `g` is a sink for `g`; sinks differ per good; there is no global end node. | UNCHANGED | MODEL | stipulated | L156-157 |
| Y256 | The orientation contains a flow serving 100% of every good's demand, because the LP imposes node balance and the sum of `b_g` over nodes is 0 identically — both `s` and `c` are world shares. | UNCHANGED | MATH | algebraic derivation | L158-160 |
| Y257 | The premise that makes the LP feasible is connectedness: on a disconnected map the balance must hold per component, share normalisation does not deliver that, and a two-component graph with cross-component imbalance is infeasible outright. | UNCHANGED | MATH | algebraic derivation | L160-163 |
| Y258 | §2.2 states the connectedness requirement and what the solver does when it is violated. | UNCHANGED | MODEL | stipulated | L163-164 |
| Y259 | Measured on 1444, which is one component: 100.0% of demand reachable from supply, 29/29 goods, zero orphan sinks. | UNCHANGED | MODEL | numerical test | L164-165 |
| Y260 | Ready-marking is a monotone closure, so the stall sequence and both promotion branches are provably independent of scheduling — each reads only the candidate set the closure fixes. | UNCHANGED | MATH | algebraic derivation | L166-168 |
| Y261 | Free-edge direction is deterministic, by the same closure argument plus the priority key's index tiebreak. | UNCHANGED | MATH | algebraic derivation | L168-169 |
| Y262 | That free-edge direction is a function of the graph and the balances alone — that the node indexing never decides — is measured rather than proved, and holds exactly where the key has no exact ties: zero orientation changes under scheduler permutations and zero exact `(DEF, b)` ties on free edges, 29/29 goods. | UNCHANGED | MODEL | numerical test | L169-172 |
| Y263 | The certificate flow is a near-fewest-hop routing in aggregate: with unit costs the objective would be exactly the sum of flow times hops, and the tie-break makes it the sum of flow times cost with cost in [1, 1 + TIE_EPS], so the optimum minimises a hop count in which a hop between two wealthy nodes counts marginally more. | CHANGED | MATH | algebraic derivation | L173-176 |
| Y978 | At `TIE_EPS = 1e-3` the cost spread is under a tenth of a percent of the base cost, so the routing is within that factor of fewest-hop — which makes "fewest-hop" an approximation with a stated bound rather than an identity, and that is the price of a unique optimum. | NEW | MATH | algebraic derivation | L176-179 |
| Y264 | No per-unit shortest-path claim is made and none holds, because a unit may detour when sink assignment demands it. | UNCHANGED | MATH | algebraic derivation | L179-180 |
| Y265 | The efficiency property carries no measurement and wants none: it follows from the construction of the LP, and any hop count would re-derive the objective rather than test it. | UNCHANGED | DESIGN | stipulated | L181-182 |
| Y266 | The §3.13 calibration deliberately degrades efficiency, which is a change to the program being solved rather than evidence about the property. | UNCHANGED | DESIGN | stipulated | L182-184 |
| Y267 | The orientation is recomputed on a fixed monthly tick, aligned to the vanilla trade tick. | UNCHANGED | MODEL | stipulated | L186 |
| Y268 | Orientation is read from the current solve every time, with no memory of the previous one. | UNCHANGED | MODEL | stipulated | L186-187 |
| Y269 | The LP is deterministic on one machine and one build — six identical solves gave one orientation on the reference implementation. | UNCHANGED | MODEL | numerical test | L187-189 |
| Y270 | Across machines LP determinism is the open question of §3.13. | UNCHANGED | DESIGN | stipulated | L189 |

## §1.2 — Supply (L191-202)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y271 | `s(n,g) = goods_produced(n,g)` over the world sum of `goods_produced(m,g)`. | UNCHANGED | MODEL | stipulated | L194 |
| Y272 | `goods_produced` is a physical quantity — pre-production-efficiency and pre-autonomy. | UNCHANGED | MODEL | stipulated | L197 |
| Y273 | `goods_produced` moves with devastation, occupation and prosperity, because `00_static_modifiers.txt`'s `devastation`, `occupied`, `under_siege` and `prosperity` all carry `trade_goods_size_modifier`. | UNCHANGED | INSTALL | read from a file (`00_static_modifiers.txt`) | L197 |
| Y274 | There is no regularizer: v1 mixed in `s ← (1 − ε)·s + ε/N` to keep dead branches from being oriented by floating-point residual, and DRAIN does not need it. | UNCHANGED | MODEL | stipulated | L199-201 |
| Y275 | DRAIN's free edges are oriented combinatorially by the drainage sweep rather than by comparing near-equal solved potentials. | UNCHANGED | MODEL | algebraic derivation | L200-201 |
| Y276 | One node has `b = 0` exactly at 1444 — `cape_of_good_hope` — and it is handled as an ordinary conduit. | UNCHANGED | MODEL | numerical test | L201-202 |

## §1.3 — Demand (L204-385)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y277 | Demand is assembled per province, then summed to the node. | UNCHANGED | MODEL | stipulated | L206 |
| Y028 | Wealth is owner-agnostic and reads three things about the province: its development, its trade good, and its own current condition. | NEW | MODEL | stipulated | L208-210 |
| Y278 | Wealth is a property of the place — what the land is worth per year, before anyone's government touches it. | UNCHANGED | DESIGN | stipulated | L209-210 |
| Y279 | Wealth reads no autonomy, no production efficiency, no national ideas, no estate or government modifiers, and no technology. | UNCHANGED | MODEL | stipulated | L210-211 |
| Y029 | Two provinces with the same development, trade good and condition have the same wealth whoever owns them. | CHANGED | MODEL | algebraic derivation (v5 said "terrain, development and trade good") | L211-213 |
| Y280 | A province's wealth does not change when it is conquered. | UNCHANGED | MODEL | algebraic derivation | L213 |
| Y030 | Owner-agnosticism is true by construction rather than by a policed rule; v3.0 through v5.0 stated the property and then defended it with a two-test classifier applied to a sweep of the install, which is a large surface to keep correct and was wrong in both independent audits that examined it. | NEW | DESIGN | algebraic derivation | L215-219 |
| Y031 | `base_tax`, `base_production` and the trade good are bare attributes of the place, so nothing about them needs classifying. | NEW | MODEL | algebraic derivation | L219-220 |
| Y032 | What the change gives up: `gems`' `local_tax_modifier` and `incense`' `trade_value_modifier` are genuinely province-scoped and are no longer read, along with great projects, permanent province modifiers and the DLC state they depended on. | CHANGED | DESIGN | stipulated | L220-223 |
| Y033 | The dropped apparatus was live on 89 of the 2,472 counted provinces — 43 `gems` plus 31 `incense` plus 16 great-project and permanent-modifier provinces, less one that is both (province 542). | CHANGED | INSTALL | read from a file; no script named at this line | L225-227 |
| Y034 | That count depends on the field: it is 87 under the withdrawn `is_city` filter, and 89 rather than 88 because province 4856 is one of the twenty whose good the engine rolls and it rolled `incense`. | NEW | INSTALL | read from a file (the save, for the rolled good) | L227-229 |
| Y281 | The model trades that fidelity for an input surface with no classification question in it. | NEW | DESIGN | stipulated | L229-230 |
| Y035 | `goods_produced(p) = GP_COEFF · base_production(p) · (1 + sum of province-state goods modifiers)`, with no flat-bonus term. | CHANGED | MODEL | stipulated | L233 |
| Y036 | `trade_value(p) = goods_produced(p) · price(good(p))` in ducats per year, with no trade-value modifier term. | CHANGED | MODEL | stipulated | L234 |
| Y037 | `tax_value(p) = TAX_COEFF · base_tax(p) · (1 + sum of province-state tax modifiers)`. | CHANGED | MODEL | stipulated | L235 |
| Y282 | `wealth(p) = tax_value(p) + trade_value(p)`, in ducats per year. | UNCHANGED | MODEL | stipulated | L236 |
| Y283 | `c(n,g)` is the node's share of world wealth raised to `α(g)`: the sum over provinces in the node of `wealth^α(g)` over the world sum. | UNCHANGED | MODEL | stipulated | L238 |
| Y284 | `GP_COEFF` and `TAX_COEFF` have different provenance from one another. | NEW | DESIGN | stipulated | L241 |
| Y038 | `GP_COEFF` is a shipped file value: `common/static_modifiers/00_static_modifiers.txt` carries `provincial_production_size = { trade_goods_size = 0.2 … }`, localised "Base Production", the same tooltip line the coefficient was measured off. | CHANGED | INSTALL | read from a file | L241-245 |
| Y039 | `GP_COEFF` is therefore moddable and is read at runtime rather than hardcoded. | NEW | DESIGN | stipulated | L245 |
| Y040 | `TAX_COEFF` is in no file that has been found — not `defines.lua`, not `common/defines/`, not that static-modifier block — so it stays a measured constant carrying the observation that produced it. | CHANGED | INSTALL | read from a file (a negative search over named paths) | L245-247 |
| Y285 | The tax and trade terms share a time basis and are safe to add, because the engine's own province tooltips give both as annual quantities divided by twelve for display. | UNCHANGED | ENGINE | measured in-game | L249-250 |
| Y041 | The tax tooltip's schema is `Base: trunc(base_tax × 0.0833333) (Yearly base_tax)`, observed as `Base: 0.49 (Yearly 6.00)` at `base_tax` 6 and `Base: 0.16 (Yearly 2.00)` at `base_tax` 2. | CHANGED | ENGINE | measured in-game | L250-253 |
| Y042 | The parenthetical is `base_tax` itself and the `Base` line is its truncated twelfth; it is not twelve times the displayed figure, which would give 5.88 and 1.92. | NEW | ENGINE | algebraic derivation over the two observations | L253-254 |
| Y043 | v4.0 and v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both of its own data points, and v3.0 carries neither that schema nor the 0.6125 arithmetic. | NEW | MODEL | read from a file (the prior spec versions) | L254-255 |
| Y044 | The monthly production tooltip's `Trade Value` line is consistent with the same relation on one observation, 3.52 to +0.29, which fixes the divisor only to within (11.73, 12.14]. | CHANGED | ENGINE | measured in-game (one observation) | L255-257 |
| Y045 | Both monthly figures being the annual value over twelve is what lets the annual forms add directly, and the tax pair establishes it at two development levels. | CHANGED | MODEL | algebraic derivation | L257-258 |
| Y286 | The coefficients were measured on two provinces: Garnatah (223) with `base_tax` 6, `base_production` 4, silk and `local_autonomy` 0, and Caceres (1747) with `base_tax` 2, `base_production` 2, wool. | UNCHANGED | ENGINE | measured in-game | L260-262 |
| Y287 | Only the tooltips' `Base` lines are used. | UNCHANGED | DESIGN | stipulated | L261-262 |
| Y288 | A province window's `Trade Value` also carries the owner's `global_trade_goods_size_modifier`. | UNCHANGED | ENGINE | measured in-game | L262-263 |
| Y289 | Garnatah's window read 3.52 rather than 0.80 × 4.00 = 3.20 because Granada's 1444 monarch held the `Industrious` ruler personality, +10%. | UNCHANGED | ENGINE | measured in-game | L263-264 |
| Y290 | Ruler personalities are rolled at game start wherever country history scripts none, so any window figure is one sample of a random variable, while the `Base` lines and the annual-over-twelve ratio are not. | UNCHANGED | ENGINE | measured in-game | L264-266 |
| Y291 | Modifiers apply after the coefficient, not before: the engine computes the base from development first and then applies a percentage. | UNCHANGED | ENGINE | measured in-game | L268-269 |
| Y046 | Observed on Garnatah, `base_tax` 6 with `Tax Income Efficiency 125.0%` displays `Base 0.49` and then `0.62`; since 0.49 × 1.25 = 0.6125 truncates to 0.61, the engine multiplies the untruncated monthly value (6 × 0.0833… = 0.49999…, × 1.25 = 0.62499…, displayed 0.62). | CHANGED | ENGINE | measured in-game (one observation) | L269-272 |
| Y047 | The example establishes only the ordering — base from development first, percentage second — and nothing finer. | NEW | ENGINE | algebraic derivation | L272-273 |
| Y048 | v4.0 and v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires rounding while §2.3 requires truncation, and both cannot hold. | NEW | MODEL | read from a file (the prior spec versions) | L274-275 |
| Y049 | Flat goods bonuses would add into `goods_produced` before the price multiply — the goods-produced tooltip carries an additive `Base Goods Produced` block above a multiplicative `Goods Produced Efficiency` block — but under §1.3 no source grants one, so the ordering is stated for the emitter's benefit and is exercised by no province in the model. | CHANGED | ENGINE | measured in-game (tooltip shape) | L275-279 |
| Y050 | Province condition is the one thing besides development and the good that wealth reads: five static modifiers describe a province's own state, all five are defined in `common/static_modifiers/00_static_modifiers.txt`, and four of the five are applied, `unrest` being excluded because revolt risk depends on the owner. | CHANGED | INSTALL | read from a file | L281-284 |
| Y051 | The condition modifiers and their targets: `devastation` `trade_goods_size_modifier = -2` scaled by the devastation level into `goods_produced`; `prosperity` +0.25 into `goods_produced`; `under_siege` -0.25 into `goods_produced`; `occupied` -0.5 plus `local_tax_modifier = -0.5` into both. | CHANGED | INSTALL | read from a file | L288-292 |
| Y054 | `devastation`'s scaling law is the one row in the table not settled by a shipped file: `00_static_modifiers.txt` gives the magnitude but leaves the law open, and the wiki settles it — the penalties are "scaled linearly according to the percentage value" and are quoted at 100% devastation, which is the `-2 × level/100` the model applies. | CHANGED | INSTALL | read from a file (magnitudes) plus community documentation (the wiki) for the scaling law | L289 |
| Y052 | `unrest` grants `local_tax_modifier = -0.02` per point of revolt risk and enters `tax_value`. | NEW | INSTALL | read from a file | L293 |
| Y053 | `occupied` and `unrest` touch the tax term; the other three reach `goods_produced` alone. | CHANGED | MODEL | algebraic derivation | L295 |
| Y292 | `unrest`'s scaling is stated in the file: the `unrest` block's own comment reads `#10% longer time to build troops for each rr`, so its values apply per point, and the neighbouring `nationalism` block uses the same convention. | NEW | INSTALL | read from a file | L295-298 |
| Y979 | `unrest` is live at the 1444 start and is deliberately not read. | NEW | MODEL | stipulated | L300 |
| Y980 | Revolt risk is not a property of the place: in play it carries separatism from recent conquest, unaccepted culture, wrong religion and nationalism, all of them relations between a province and its owner, so reading it would make a province's wealth change when it is conquered. | NEW | MODEL | algebraic derivation | L300-304 |
| Y981 | `solver.py`'s `STATE_TAX_MOD` carries `occupied` alone, so four of the five rows in the table are applied. | NEW | MODEL | read from a file (the model's own solver) | L304-305 |
| Y982 | 21 counted provinces carry revolt risk in the 1444 start save. | NEW | INSTALL | read from a file (the save) | L307-308 |
| Y057 | Sixteen of the 21 are authored in `history/provinces` at integer risk 5/8/10/15 — Sofala's comment reads "expansion of Shona into Sofala region causes major disruptions" — and the other five, all Shirvan-owned, receive theirs at runtime, so reading them needs the save. | NEW | INSTALL | read from a file | L308-310, restated L323-324 |
| Y983 | Even at the start date a quarter of the revolt risk is owner-derived, and during a campaign that share only grows. | NEW | MODEL | algebraic derivation over the 16/5 split | L310-311 |
| Y984 | The effect `unrest` would buy is already bought: conquest costing a province its wealth is delivered by `devastation`, `occupied` and `under_siege`, all three properties of the place and all three applied, so `unrest` would add owner-dependence without adding a mechanic. | NEW | MODEL | algebraic derivation | L313-315 |
| Y055 | Excluding `unrest` costs 12.23 ducats, 0.115% of the 10,607.40 world wealth reading it from the save, or 9.40 ducats, 0.089% reading only the authored 16. | CHANGED | MODEL | numerical test; no script named at this line | L317-319 |
| Y056 | Admitting `unrest` moves 4 of 159 edges of the installed graph and leaves the sink set `{genua, hangzhou}` unchanged. | CHANGED | MODEL | numerical test | L319-320 |
| Y985 | An earlier draft of the paragraph said admitting `unrest` moves no edge; that was measured at `α_Φ = 1.5` and does not hold at 2.0. | NEW | MODEL | numerical test | L320-321 |
| Y058 | The condition modifiers are what make the map answer to war: §1.2's volatility and §3.3's "a besieged province genuinely produces less" both rest on them, and §2.8's war rows are their test. | CHANGED | DESIGN | algebraic derivation | L324-326 |
| Y059 | Eleven counted provinces begin devastated — Bohemia at 50, Erzgebirge and Moravia at 20 — and no province-history file says so. | NEW | INSTALL | read from a file (the save against `history/provinces`) | L328-329 |
| Y060 | That devastation is applied by `on_startup`, which fires `flavor_boh.15` ("The Aftermath of the Hussite Wars"), via the chain `common/on_actions/00_on_actions.txt` to `on_startup_effect` to `common/scripted_effects/01_scripted_effects_for_on_actions.txt` to `country_event flavor_boh.15`. | NEW | INSTALL | read from a file | L329-333 |
| Y061 | The start devastation costs 13.40 ducats across the eleven affected counted provinces. | NEW | MODEL | computed by a named script (`measure6.py`) | L330-331 |
| Y062 | The start state is what the engine produces rather than what the history files say, and that costs three separate reads. | NEW | DESIGN | algebraic derivation | L335-336 |
| Y063 | `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`, `flavor_geo.1` and others directly from its own `events = { }` list in `common/on_actions/00_on_actions.txt` — a second path alongside the `on_startup_effect` chain. | NEW | INSTALL | read from a file | L338-341 |
| Y064 | Development does not move before the first tick: on this start the history parse matches the save on 2,472 of 2,472 provinces for `base_tax`, `base_production` and owner, and only `trade_goods` differs, on exactly twenty provinces. | NEW | INSTALL | read from a file (history parse against the save) | L341-343 |
| Y065 | v6.0's first draft said `flavor_geo.1` carries `add_base_tax` and could move development pre-tick; it does not — its whole effect is legitimacy, a country modifier and a flag, and those keys are in `flavor_geo.3`, which `on_startup` does not fire (a mission does). | NEW | INSTALL | read from a file | L343-346 |
| Y066 | `add_base_*` in a dated block before the start date accumulates, and v5.0 and earlier overwrote instead of adding: province 1 (Uppland) has `base_tax = 5` undated plus 1 at `1436.4.28`, and the game has 6. | NEW | INSTALL | read from a file | L347-349 |
| Y067 | `is_city = yes` is not a filter the engine applies: 20 owned provinces omit or comment out that line — province 265 among them, also one of the devastated eleven — and the engine treats them as cities. | NEW | INSTALL | read from a file | L350-352 |
| Y068 | The model counts a province when it has an owner and lies in a trade node: 2,472 provinces, not 2,452. | CHANGED | DESIGN | stipulated | L352-353 |
| Y069 | Twenty counted provinces have no trade good in their history file (`trade_goods = unknown`), and the engine assigns one at start from each good's `chance = { }` block. | NEW | INSTALL | read from a file | L355-357 |
| Y070 | The model reads the good the engine actually rolled rather than predicting the draw, and pricing those provinces at zero instead understates world wealth by 12.70 ducats. | NEW | DESIGN | numerical test; no script named at this line | L357-359 |
| Y071 | On this save the twenty came up seven `fur`, five `grain`, three `wool`, two `livestock`, and one each of `cotton`, `incense` and `naval_supplies`; a different roll gives a slightly different field and nothing in the model depends on which one. | NEW | INSTALL | read from a file (the save) | L359-362 |
| Y293 | Everything the engine itemised on a real province that is not local is excluded: `Reform Iqta` (+5%, government), `Clergy` (+5%, estate), national ideas (+15%), production efficiency from technology (+2%), and the owner's goods-produced modifiers. | UNCHANGED | ENGINE | measured in-game | L364-366 |
| Y294 | `Core` (+75%) and `City` (+25%) are not excluded, because they are already inside `TAX_COEFF`. | UNCHANGED | MODEL | algebraic derivation | L368-369 |
| Y295 | The engine's tax multiplier is the sum of the itemised percentages: Garnatah's `Tax Income Efficiency: 125.0%` is 75+25+5+5+15 and multiplies the base by 1.25, and Caceres's 105.0% is 75+25+5 and multiplies by 1.05. | UNCHANGED | ENGINE | measured in-game | L369-371 |
| Y296 | A cored city province carrying nothing else sums to exactly 0.75 + 0.25 = 1.00 and yields `base_tax` ducats a year, which is the reference condition `TAX_COEFF = 1.0` was measured at. | UNCHANGED | ENGINE | measured in-game | L371-373 |
| Y072 | The model applies `TAX_COEFF = 1.0` to every province it counts: ownership is not modelled, so every province is treated as cored and settled. | CHANGED | DESIGN | stipulated | L373-374 |
| Y297 | Carrying either the `Core` or the `City` term again would double-count it. | UNCHANGED | MODEL | algebraic derivation | L374-375 |
| Y073 | That is a modelling choice with a known cost: two readings, both on cored city provinces at `base_tax` 2 and 6, are what `TAX_COEFF = 1.0` rests on. | NEW | DESIGN | algebraic derivation | L375-376 |
| Y074 | `base_tax` at 1444 runs up to 15 (province 1821), with total development reaching 33 there. | NEW | INSTALL | read from a file | L376-377 |
| Y298 | Unowned provinces are outside the model: `s` and `c` are computed over provinces that have an owner and lie in a trade node, because an unowned province produces nothing the trade system can move. | CHANGED | DESIGN | stipulated (v5 said "an owner and `is_city = yes`") | L379-380 |
| Y299 | What owner-agnostic demand buys: demand stops responding to who rules and responds only to what is there, so a conquest no longer moves the demand vector on the day it happens — only development, trade goods and prices do. | UNCHANGED | DESIGN | stipulated | L382-384 |
| Y075 | Owner-agnostic wealth also removes a large source of hidden owner-dependence from the aggregate graph of §1.6, which is built from the same wealth field. | CHANGED | MODEL | algebraic derivation | L384-385 |

## §1.4 — Market concentration (L387-397)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y300 | `α(g) = clamp((price(g)/P₀)^k, α_min, α_max)` with `P₀ = 2.0` ducats. | UNCHANGED | MODEL | stipulated | L390 |
| Y301 | α > 1 makes demand superlinear in provincial wealth, so luxuries concentrate on individually rich provinces. | UNCHANGED | MODEL | algebraic derivation | L393 |
| Y302 | α = 1 makes demand proportional to economic size. | UNCHANGED | MODEL | algebraic derivation | L394 |
| Y303 | α < 1 makes demand sublinear, so bulk goods spread toward populous regions. | UNCHANGED | MODEL | algebraic derivation | L395 |
| Y304 | α moves with vanilla price events in both directions, with no smoothing. | UNCHANGED | MODEL | stipulated | L397 |

## §1.5 — Goods without a graph (L399-449)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y305 | Gold is excluded by configuration. | UNCHANGED | MODEL | stipulated | L401 |
| Y306 | Gold-mine income is its own income category in the engine (`INCOMEGOLD`, `gold_income` as a distinct scriptable field), computed from mine value with its own constants (`GOLD_MINE_SIZE`), and is not booked as production income. | UNCHANGED | ENGINE | read from a file (named strings and defines) | L401-404 |
| Y307 | Under owner-agnostic wealth the exclusion is stronger still: `wealth(p)` is built from `base_tax`, `base_production` and price and reads no income field at all, so gold income is invisible to demand entirely. | UNCHANGED | MODEL | algebraic derivation | L404-407 |
| Y308 | Gold is inert in vanilla trade value (`base_price = 0`, `goldtype = yes`), so the exclusion costs nothing. | UNCHANGED | INSTALL | read from a file | L407-408 |
| Y309 | Whether the per-province production-income field nevertheless carries the gold figure before the country-level split is still unknown, and is moot because nothing in the model reads that field — which is why §2.7 item 12 was dropped rather than run. | UNCHANGED | MODEL | stipulated | L408-411 |
| Y310 | Any good with zero world production this month has no graph, because `s(n,g)` is undefined when nothing produces `g`; it contributes nothing to the value weights (`V_g = 0`) and is absent from the survival table. | UNCHANGED | MODEL | algebraic derivation | L413-415 |
| Y311 | A latent good acquires graph, value weight and survival-table entry on the first month any province produces it. | UNCHANGED | MODEL | stipulated | L415-416 |
| Y312 | Activation is not a local addition: a province produces exactly one trade good at a time, so a latent good going live replaces what that province was producing. | UNCHANGED | ENGINE | stipulated | L417-419 |
| Y313 | In the month of conversion the new good gains a producer and the old good loses one, so both goods' supply shares renormalise across every node that produces either. | UNCHANGED | MODEL | algebraic derivation | L421-422 |
| Y314 | The converting province is repriced, so `wealth(p)` changes and with it `c(n,g)` for every good in the game, because §1.3 makes one wealth field the demand base for all of them. | UNCHANGED | MODEL | algebraic derivation | L423-425 |
| Y315 | `V_g` moves for both goods, reweighting every display, link value and AI score. | UNCHANGED | MODEL | algebraic derivation | L426 |
| Y316 | `Φ_w` moves on activation, because §1.6 runs DRAIN on that same wealth field. | UNCHANGED | MODEL | algebraic derivation | L427 |
| Y317 | An activation is a world-state change on the scale of a development change or a conquest, and every graph in the model is entitled to move on it. | UNCHANGED | DESIGN | stipulated | L429-430 |
| Y076 | Repricing to coal the 45 latent-coal provinces that are owned at 1444 flips 16 of 159 `Φ_w` edges and adds 214.60 ducats to world wealth. | CHANGED | MODEL | computed by a named script (`measure6.py`) | L430-432 |
| Y077 | The counterfactual holds every non-repriced input fixed: province 4237 is both latent-coal and one of the devastated eleven, so a reprice that drops its devastation measures coal activating plus one province healing, worth 2.40 ducats — and on this field that mix moves no additional edge, so the reason to hold the input fixed is that the wealth figure is wrong either way rather than that the edge count reliably notices. | NEW | MODEL | numerical test; the script attribution (`measure6.py`) sits one sentence earlier on the main figure | L432-436 |
| Y318 | Coal's base price of 10.0 is the highest in the shipped price table. | CHANGED | INSTALL | read from a file (`common/prices/00_prices.txt`) with `measure6.py` cited alongside | L436-438 |
| Y319 | v2.1 held that a latent good leaves `Φ_w` unaffected because "`Φ_w` reads wealth, not goods"; that was true under v2.0's `Φ_ord`, where `V_g = 0` gave a latent good zero weight, and became false with the operator change. | UNCHANGED | MODEL | algebraic derivation | L438-442 |
| Y320 | Coal produces nowhere at the 1444 start. | UNCHANGED | INSTALL | read from a file | L444 |
| Y321 | Coal's default trigger fires on Enlightenment (the Manufactories branches require special flags), per province: `development_discounting_tribal = 20` or owner innovativeness 20, that province's own institution progress at 100, and the owner having the institution. | UNCHANGED | INSTALL | read from a file | L444-447 |
| Y322 | The 58 latent-coal provinces convert province-by-province over years rather than in a single tick, so the graph grows as they do. | UNCHANGED | INSTALL | read from a file | L447-449 |

## §1.6 — The aggregate graph (L451-654)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y323 | `V_g = price(g) ·` the world sum of `goods_produced(m,g)` are the per-good value weights used for display, link values and AI. | UNCHANGED | MODEL | stipulated | L454 |
| Y324 | For the wealth good, supply is uniform: `s_w(n) = 1/N`. | UNCHANGED | MODEL | stipulated | L456 |
| Y325 | For the wealth good, `c_w(n)` is the node's share of world wealth raised to `α_Φ`. | UNCHANGED | MODEL | stipulated | L457 |
| Y326 | `b_w = s_w − c_w`, with `α_Φ = 2.0`, a hyperparameter. | CHANGED | MODEL | stipulated (v5 had `α_Φ = 1.5`, "a stipulated constant") | L458 |
| Y327 | `Φ_w = DRAIN(b_w)` — the §1.1 operator with wealth as the good. | UNCHANGED | MODEL | stipulated | L460 |
| Y328 | `Φ_w` is the graph installed in the game. | UNCHANGED | DESIGN | stipulated | L463 |
| Y329 | Under `Φ_w` every node supplies uniformly and rich nodes are net demanders, so all wealth in the world pulls edges toward itself, arrows point from wealthy nodes toward the wealthiest, and the sinks are wherever the wealth flow terminates. | UNCHANGED | MODEL | algebraic derivation | L463-466 |
| Y078 | Both the sinks' count and their locations move with the wealth field, and `α_Φ` sets how sharply concentration is read. | CHANGED | MODEL | algebraic derivation | L466-467 |
| Y079 | At `α_Φ = 2.0` the 1444 field gives two sinks and a modestly grown Europe gives two, three or five, so neither the count nor the placement is fixed by the constant. | NEW | MODEL | numerical test (the Europe table below) | L467-469 |
| Y080 | v2.0 through v4.0 said the count "emerges from concentration" and v5.0 said "the count is set by `α_Φ`"; both are wrong the same way, since the count is a function of the field and the constant, and v2.1 also chose the value with a target count in view — a calibration §2.3 withdraws without replacing. | CHANGED | MODEL | algebraic derivation | L469-473 |
| Y330 | What the world state moves is where the sinks are and how the map drains toward them, which is the property §3.1's first goal asks for. | UNCHANGED | DESIGN | stipulated | L473-474 |
| Y331 | In exact arithmetic only the sign pattern and proportions of `b_w` matter: Phase 0 reads signs, Phase 1's HHI is built from mass shares, the LP optimum scales linearly with identical net-flow signs, and the priority key is order-isomorphic under positive scaling. | UNCHANGED | MATH | algebraic derivation | L476-479 |
| Y332 | The implementation adds one premise: the zero-flow tolerance is absolute (`1e-11`), so scaling `b` down pushes genuine flow arcs into the free set. | UNCHANGED | MODEL | algebraic derivation | L479-480 |
| Y081 | Measured: identical orientation from ×1 down to ×10⁻², 22 edge flips at ×10⁻⁴ where the sink set becomes `{english_channel, hangzhou}`, and 96 at ×10⁻⁶ where it becomes `{hangzhou}`. | CHANGED | MODEL | numerical test | L480-483 |
| Y333 | The orientation degrades before the sink set does, so the sink set is not the quantity to watch here. | CHANGED | MODEL | algebraic derivation (v5 said the orientation degrades "while the sink set happens to survive") | L482-483 |
| Y082 | 1444's `b_w` has largest magnitude 0.0347. | CHANGED | MODEL | numerical test | L484 |
| Y334 | Normalising into (−1, 1) scales 1444's `b_w` up and is safe; scaling down is not, so either scale `b` up or scale the tolerance with it. | UNCHANGED | MODEL | algebraic derivation | L484-485 |
| Y083 | Measured on 1444 data at `α_Φ = 2.0`: two sinks, `genua` and `hangzhou`, at `c_w` ranks 2 and 1 and node-wealth ranks 4 and 12. | CHANGED | MODEL | computed by a named script (`measure6.py`) | L487-488 |
| Y084 | Both sinks are properties of the world, because the orientation does not depend on how the nodes are numbered — a change from v6.0, whose argument turned on the opposite. | NEW | MODEL | algebraic derivation over the relabelling measurements below | L488-490 |
| Y335 | With unit arc costs Phase 2's b-flow is degenerate: many routings reach the same minimum cost, and the simplex returns whichever its pivot path reaches, which moves with node numbering. | NEW | MODEL | algebraic derivation | L492-494 |
| Y085 | Measured on that LP directly, 40 of 40 permutations return a different optimal support at an objective identical to within a few units in the last place. | NEW | MODEL | numerical test | L494-496 |
| Y087 | So the old sink set was partly an artifact of the node order, and v6.0 said so. | NEW | MODEL | algebraic derivation | L495-496 |
| Y986 | Phase 2 now breaks those ties inside the objective, with a cost symmetric in the arc and read from node wealth alone. | NEW | MODEL | stipulated (§2.3) | L498-499 |
| Y987 | On the same LP under the tie-break cost, 0 of 40 permutations return a different support. | NEW | MODEL | numerical test | L499 |
| Y086 | Over 180 relabellings — three seeds of 60, every input held fixed — the orientation did not change once: 0 of 159 edges moved in any run, the sink set came back as `{genua, hangzhou}` in 180 of 180, and `hangzhou` and `genua` each held an end in every run. | NEW | MODEL | computed by a named script (`relabel6.py`, which validates its instrument against `drain.py` on the identity permutation before counting any trial) | L499-503 |
| Y988 | The instrument is a reimplementation, and a reimplementation whose Phase 2 minimises the old objective disagrees with the shipped solver on 26 of 159 edges — `relabel6.py` aborts on exactly that, and did so when the tie-break went in. | NEW | MODEL | numerical test | L505-508 |
| Y989 | A symmetric cost is required rather than a stylistic choice: a directional preference of the form `1 − ε·(w[v] − w[u])` is a potential difference, so its total over any flow meeting the same `b` is the sum of `w[n]·b[n]` — the same for every feasible routing, and unable to break a tie at all. | NEW | MATH | algebraic derivation | L508-510 |
| Y091 | Nothing this section quotes about the installed graph is conditional on the node order. | CHANGED | MODEL | algebraic derivation | L512 |
| Y093 | Over the 180 relabellings the sink set, every edge direction, and the promotion and fallback counts were identical, so for `Φ_w` the distinction v6.0 drew between world-properties and ordering-artifacts has collapsed into the first category. | NEW | MODEL | numerical test | L512-515 |
| Y990 | The per-good graphs are a different matter: the tie-break cost is read from good-independent node wealth, but a wealth-weighted cost need not separate the optima of a per-good LP, whose `b` is a different vector. | NEW | MODEL | algebraic derivation | L517-519 |
| Y991 | Measured across 29 goods × 10 relabellings, 84 of 290 runs moved a per-good edge — a mean of 0.99 and up to 15. | NEW | MODEL | numerical test | L519-520 |
| Y145 | The per-good figures in this section are therefore quoted at fixed node order. | NEW | DESIGN | stipulated | L520-521 |
| Y336 | The emitter must fix one canonical order and keep it, and that requirement is not weaker than in v6.0 but only relocated: §2.2 propagates the per-good economy and writes it back, so a per-good arrow that moves with the node numbering moves node values, the ledger and the economy tab with it. | NEW | DESIGN | algebraic derivation | L521-524 |
| Y993 | The value weights are the exception: `V_g` is `price(g)` times a sum over producers, with no direction in it, so they are order-independent by construction. | NEW | MATH | algebraic derivation | L524-526 |
| Y094 | Phase 1 selects `hangzhou`; `genua` arrives by stall promotion, so there is 1 promotion and 0 fallbacks. | CHANGED | MODEL | numerical test | L528-529 |
| Y095 | Five sources, all in the bottom half of the wealth field, at `c_w` ranks 55–79 and mean degree 2.4 against the map's 4.0. | CHANGED | MODEL | numerical test | L529-530 |
| Y337 | v2 called the sources "cul-de-sacs"; the degrees are not far off that reading here, but it is a description of five nodes on one field rather than a property of the operator. | CHANGED | MODEL | algebraic derivation (v5 said the degrees "do not support" the reading) | L530-532 |
| Y096 | Every node drains to a sink, the map is acyclic and 159/159 oriented, and the sink set is unchanged under ±1% wealth noise on three seeds. | CHANGED | MODEL | numerical test | L532-534 |
| Y338 | `Φ_w`'s marking order is a per-node scalar whose descending comparison reproduces the DAG (0 violations), so every consumer needing a potential still gets one. | UNCHANGED | MODEL | numerical test | L534-536 |
| Y097 | Per good on the same field: 2–8 sinks, mean 3.69, 29/29 acyclic, 0 fallbacks fired, and 90.5% of ordered node pairs (5,721 of 6,320) connected by at least one good's directed path. | CHANGED | MODEL | numerical test | L537-538 |
| Y098 | Agreement with the per-good graphs is 55.2% of edge-goods and 55.0% value-weighted. | CHANGED | MODEL | numerical test | L540 |
| Y099 | The superseded marking-order aggregate scored higher on that measure, and §3.9 records why the trade was taken while maintaining no figure for an operator the model does not install. | CHANGED | DESIGN | stipulated | L540-542 |
| Y100 | `α_Φ = 2.0` and `TIE_EPS = 1e-3` are hyperparameters; the choice is developer taste and the document offers no justification for either beyond that. | CHANGED | DESIGN | stipulated | L544-546 |
| Y102 | No derivation is claimed, none is implied, and none should be reconstructed from the figures below: they describe what the field does around the chosen values, which is what an implementer needs in order to change them. | CHANGED | DESIGN | stipulated | L546-548 |
| Y103 | Across `α_Φ` = 1.00…8.00 at 0.01 the sink set is a step function, and `α_Φ = 2.0` sits in the band [1.63, 3.28], width 1.65, which gives `{genua, hangzhou}`. | CHANGED | MODEL | numerical test | L550-552 |
| Y104 | Sampled at six values the sink count is non-monotone: 3 → 1 → 2 → 2 → 1 → 1 across `α_Φ` in {1, 1.5, 2, 3, 4, 8}. | CHANGED | MODEL | numerical test | L552-553 |
| Y992 | For `TIE_EPS` the sink set is unchanged from about 1e-6 to about 1 — six orders of magnitude — because the term is a tie-break: below that range it falls under the solver's tolerance and stops registering, and above it the term exceeds the base arc cost of 1 and stops being a perturbation. | NEW | MODEL | numerical test (`scripts/epsilon6.py` reports the bands and bisects their edges) | L553-556 |
| Y105 | A written warning against reintroducing the withdrawn justifications for `α_Φ` — resemblance to vanilla's authored map, then band width — because a hyperparameter chosen by taste does not become better justified by finding a property that happens to hold at it. | NEW | DESIGN | stipulated | L558-561 |
| Y106 | "Europe becomes the centre of trade as it develops" is the design claim, and it is what §3.1's first goal asks the field to deliver. | CHANGED | DESIGN | stipulated | L563-564 |
| Y107 | At 1444 the map ends in Genoa and in Hangzhou, and as European development compounds Europe gains ends and Asia loses its one. | NEW | MODEL | numerical test (the table below) | L564-565 |
| Y108 | The mechanism carrying that is that wealth is linear in development, so developing a region moves its `c_w` share directly and `Φ_w`'s ends follow the wealth. | NEW | MODEL | algebraic derivation | L565-567 |
| Y109 | Observed on the 1444 field holding `α_Φ = 2.0` and scaling European development only over 824 counted European provinces, with bisected boundaries, the sink set is constant over ten intervals from ×1.00 to ×2.50, running `{genua, hangzhou}`; +`english_channel`/`rheinland`; back; +`gulf_of_siam`; a five-node set; `{genua, gulf_of_siam}`; `{english_channel, genua, rheinland}` over ×1.38–×1.95; +`hangzhou`; `{english_channel, genua, rheinland}`; and `{genua, rheinland}`. | CHANGED | MODEL | computed by a named script (`europe.py`) | L569-584 |
| Y110 | The table is to be read as a direction rather than a trajectory: it scales all 824 counted European provinces by one factor at once, which is not how development happens, no save later than 1444 was available to test against, so the design intent is the claim and the row boundaries are a property of one synthetic experiment. | NEW | DESIGN | algebraic derivation | L586-598 |
| Y111 | The path is not monotone — `hangzhou` leaves at ×1.19, returns at ×1.95 and leaves again; `gulf_of_siam` holds an end across ×1.19–×1.38 and nowhere else; two intervals narrower than ×0.03 carry sets that appear once — and those reversals are in the field rather than in the solver, since the orientation is order-invariant at every row. | NEW | MODEL | numerical test | L588-591 |
| Y340 | These are properties of this snapshot rather than constants of the model — what one field yielded under one scaling, which a different world state moves. | NEW | DESIGN | stipulated | L599-600 |
| Y112 | Because §1.3's wealth is linear in development, scaling development and scaling wealth are the same operation here — maximum difference 0.0 across the European set — so the distinction that made v5.0's version of this table wrong does not arise. | NEW | MODEL | numerical test | L600-603 |
| Y341 | All three institutions the period is named for begin in Europe between 1450 and 1550: Renaissance `1450.1.1` at Florence (province 116), Colonialism `1500.1.1` at Sevilla (224), Printing Press `1550.1.1` at Frankfurt (1876). | CHANGED | INSTALL | read from a file (`common/institutions/00_Core.txt`) | L605-608 |
| Y342 | The Renaissance's embracement bonus is `development_cost = -0.05`, a standing discount on every subsequent development point. | CHANGED | INSTALL | read from a file | L608-610 |
| Y343 | Those institution bonuses are country-scoped, so §1.3 excludes them from wealth directly; they reach the map only by changing how fast development grows. | UNCHANGED | MODEL | algebraic derivation | L609-611 |
| Y344 | The 1444 map draws the pre-Columbian trade geography unprompted. | UNCHANGED | MODEL | numerical test | L613 |
| Y345 | From the north the route to the Asian end is the Volga and the steppe: `white_sea → novgorod → kazan → siberia → samarkand → lahore → lhasa → ganges_delta → burma → gulf_of_siam → canton → hangzhou`. | CHANGED | MODEL | numerical test | L613-616 |
| Y113 | From Iberia the route is the African coast and the Red Sea: `sevilla → safi → timbuktu → katsina → ethiopia → gulf_of_aden → comorin_cape → ganges_delta → …`, eleven hops. | CHANGED | MODEL | numerical test | L616-618 |
| Y114 | No route leaves `genua` at all — it is a sink, out-degree 0 against in-degree 5, so the western Mediterranean, the Adriatic and the Rhône carry power into it. | CHANGED | MODEL | numerical test | L618-619 |
| Y994 | `english_channel` is not an end at this α: it drains to `genua` in two hops through `champagne`, and reaches the Asian end not at all. | NEW | MODEL | numerical test | L619-621 |
| Y115 | No Europe→sink route passes the Cape of Good Hope, checked exhaustively rather than sampled: of the 23 European nodes there are 27 connected Europe→sink pairs, and for 0 of them does a Cape-transiting path exist. | CHANGED | MODEL | numerical test | L623-626 |
| Y346 | That no Europe→sink route passes the Cape is what a 1444 map should say, and it is the one place in this section where a universal is asserted, because here the whole set was enumerated. | UNCHANGED | DESIGN | stipulated | L626 |
| Y116 | The Cape is a live conduit rather than an idle one: in-degree 2, out-degree 2, with 81 ordered node pairs for which a path through it exists, taking flow from `zanzibar` and `ivory_coast` and passing it to `comorin_cape` and `malacca`, carrying Atlantic drainage into the Indian Ocean. | CHANGED | MODEL | computed by a named script (`measure6.py`) | L628-631 |
| Y117 | The 81 is a count of pairs `(a, b)` where `a` reaches the Cape, the Cape reaches `b`, and `a` reaches `b` — not pairs whose shortest path happens to use it, which is a stricter reading and gives 69 on the same field. | NEW | MODEL | numerical test | L631-633 |
| Y118 | In the per-good graphs the Cape also carries Asian spices to Europe; `Φ_w` models power, not cargo. | CHANGED | MODEL | numerical test | L633-634 |
| Y119 | Scaling the 18 western and central European nodes rather than European provinces makes `genua` the sole sink from about ×1.55, while scaling all 22 does not produce a sole sink anywhere below ×4, the eastern four keeping ends of their own. | CHANGED | MODEL | numerical test | L636-639 |
| Y120 | The Cape reverses under the same growth — 1444's `ivory_coast`/`zanzibar`→Cape→`comorin_cape`/`malacca` drainage becomes `comorin_cape`/`malacca`/`zanzibar`→Cape→`ivory_coast` by about ×1.6 on the 22-node scaling — and it is not a single window, the Cape's in- and out-sets changing several times across ×1–×3 and reversing more than once, so the Cape's direction is a function of European development rather than a threshold at which it turns. | CHANGED | MODEL | numerical test | L639-644 |
| Y347 | The 22 European nodes are the 18 western and central ones (`english_channel`, `north_sea`, `baltic_sea`, `white_sea`, `novgorod`, `lubeck`, `rheinland`, `saxony`, `wien`, `krakow`, `pest`, `venice`, `ragusa`, `genua`, `champagne`, `bordeaux`, `valencia`, `sevilla`) plus `constantinople`, `crimea`, `kiev` and `kazan`. | UNCHANGED | MODEL | stipulated | L644-648 |
| Y121 | Dev-stacking a single node's top province concentrates the map on that node, and extra sinks at intermediate boosts are expected behaviour rather than noise. | CHANGED | MODEL | numerical test | L648-649 |
| Y348 | The v1 diagnostic identity (`Φ ≡ φ₀` at α = 1) does not survive the operator change, because DRAIN performs no linear solve so no linearity argument exists. | UNCHANGED | MATH | algebraic derivation | L651-652 |
| Y349 | Its replacement as the end-to-end correctness check is exact orientation equality between the reference and DLL implementations — a combinatorial comparison with no tolerance band. | UNCHANGED | DESIGN | stipulated | L652-654 |

## §1.7 — Merchants (L656-682)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y350 | Merchant placement, range and the collect/steer choice are vanilla, with one merchant per country per node. | UNCHANGED | ENGINE | stipulated | L658 |
| Y351 | A merchant present gives +2 trade power (`MERCHANT_MAX_POWER_BONUS`) and a +10% bonus on trade income (`TRADE_MERCHANT_PRESENT = 0.1`), node-wide, regardless of what it is doing. | UNCHANGED | INSTALL | read from a file (the defines and the shipped comment) | L658 |
| Y352 | v1 and v2 both called the second bonus "+10% trade efficiency"; trade efficiency and a flat income bonus are different quantities in EU4, and the define's own shipped comment settles which this one is. | UNCHANGED | INSTALL | read from a file | L658 |
| Y353 | Collect is vanilla, including the −50% penalty outside the home node. | UNCHANGED | ENGINE | stipulated | L660 |
| Y354 | Under Steer the node window lists every link incident to the node. | UNCHANGED | MODEL | stipulated | L662 |
| Y355 | The vanilla window already renders both an incoming and an outgoing link list as clickable entries (`incoming_nodes_listbox` / `outgoing_nodes_listbox` in `tradeinterface.gui`, both populated by the `TradeNodeLink` widget). | UNCHANGED | INSTALL | read from a file | L662-665 |
| Y356 | What changes is what an incoming entry does — it must accept a merchant assignment rather than merely navigate. | UNCHANGED | DESIGN | stipulated | L665-666 |
| Y357 | §2.7 item 14 settled that the incoming entry only navigates: clicking `Safi` in Sevilla's window switched the window to Safi and dispatched nothing, so this is a new interaction on an existing widget rather than a behaviour change to one that already dispatches. | UNCHANGED | ENGINE | engine test | L666-669 |
| Y358 | A merchant assigned to link {n,m} steers every good oriented n → m. | UNCHANGED | MODEL | stipulated | L671 |
| Y359 | A merchant assigned to link {n,m} is inert for every good oriented m → n. | UNCHANGED | MODEL | stipulated | L672 |
| Y360 | A merchant keeps its assignment when a link flips; only its active good set changes. | UNCHANGED | MODEL | stipulated | L673 |
| Y361 | The same physical link can host a merchant at each end, active on disjoint good sets. | UNCHANGED | MODEL | stipulated | L675 |
| Y362 | Caravan power requires the merchant to be steering at least one good on that link; assignment alone does not qualify. | UNCHANGED | MODEL | stipulated | L677-678 |
| Y363 | That constrains only the two steering conditions — collecting at an inland node as main trading port is untouched. | UNCHANGED | MODEL | algebraic derivation | L678-679 |
| Y364 | The engine's own caravan grant conditions are `merchant_present_inland` and `merchant_steering_to_inland`, and its tooltip reads as granting the bonus in the inland node rather than the adjacent one. | UNCHANGED | INSTALL | read from a file (identifiers and tooltip string) | L679-682 |
| Y365 | §2.7 item 11 settles the caravan recipient, and §3.11 carries both readings of the exposure surface. | UNCHANGED | DESIGN | stipulated | L681-682 |

## §1.8 — Collection and transfer (L684-714)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y366 | Trade power and collect/transfer intent are node-wide; what varies per good is what they produce. | UNCHANGED | MODEL | stipulated | L686 |
| Y367 | `collected_share(n,g) = 1` if n is a sink for g, else `P_collect / (P_collect + P_transfer(g))`. | UNCHANGED | MODEL | stipulated | L691-692 |
| Y368 | Transfer eligibility is per good: a country's power counts toward `P_transfer(g)` only if it has a merchant steering `g` at `n`, or it collects at some node reachable from `n` in `g`'s graph; power that is neither is inert for that good. | UNCHANGED | MODEL | stipulated | L695 |
| Y369 | The remainder moves per good by the vanilla two-case rule. | UNCHANGED | MODEL | stipulated | L697 |
| Y370 | If any country steers `g` at `n`, the outgoing value of `g` is divided across outgoing links in proportion to the modified trade power steering toward each link, not to power held in the node generally. | UNCHANGED | ENGINE | stipulated | L699 |
| Y371 | An outgoing link with no steerer receives nothing, even when other links are steered. | UNCHANGED | ENGINE | algebraic derivation | L699 |
| Y372 | A single steerer takes all of `g`'s outgoing value down its link, however little power it holds. | UNCHANGED | ENGINE | algebraic derivation | L699 |
| Y373 | If no country steers `g` at `n`, the outgoing value splits evenly across `g`'s outgoing links. | UNCHANGED | ENGINE | stipulated | L701 |
| Y374 | At `g`'s sink there is no remainder: 100% is collected and divided among collectors by trade power. | UNCHANGED | MODEL | stipulated | L703 |
| Y375 | Vanilla gates still apply: trade range, and the rule that there is no transfer into a node where nobody holds power at both ends. | UNCHANGED | ENGINE | stipulated | L705-706 |
| Y376 | What trade range gates is reach, not flow: every string, define and modifier that mentions it is about where a country may send something — `HINT_TRADERANGE_TEXT`, `TRADE_RANGE_IRO`, `TRADE_NODES_OUT_OF_RANGE`, `MAPMODE_TRADE_DESC`, `MERCENARY_COMPANY_TOO_FAR` / `MERC_RANGE_EXPLAINED`, and `REQUIRES_CAPITAL_IN_TRADE_RANGE_TT`. | UNCHANGED | INSTALL | read from a file (named strings) | L706-711 |
| Y377 | No string, define or modifier ties range to link flow — which is a statement about the files rather than a proof that no such mechanic exists; settling it needs value observed arriving at a node chain beyond every country's range. | UNCHANGED | INSTALL | read from a file | L711-713 |
| Y378 | There is no trade "supply range" in the engine; the only supply-range constructs are naval. | UNCHANGED | INSTALL | read from a file | L714 |

## §1.9 — Trade power propagation (L716-725)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y379 | A country whose provincial trade power in a node meets the threshold receives a share of it in every immediately upstream node, with no condition on the receiving node. | UNCHANGED | ENGINE | engine test (probe 15, one observation) | L720 |
| Y380 | The engine's own tooltip says power transfers "to trade nodes where it already has power", and that qualifier is descriptively false. | UNCHANGED | ENGINE | engine test | L720 |
| Y381 | Measured: France holds zero provinces and zero merchants in Sevilla and still appears there with 3.3 power, which the engine itemises as `Transfers from traders downstream: +3.1` and nothing else. | UNCHANGED | ENGINE | engine test | L720 |
| Y382 | This line was §3.16's cautionary case; it is now closed, and it closed in favour of the spec. | UNCHANGED | DESIGN | stipulated | L720 |
| Y383 | The propagation share is `1 / TRADE_PROPAGATE_DIVIDER`, and the threshold in raw power is `TRADE_PROPAGATE_THRESHOLD × TRADE_PROPAGATE_DIVIDER`, pending §2.7 probe 8. | UNCHANGED | ENGINE | read from a file (defines), with the raw-power reading flagged as pending | L720 |
| Y384 | Ship trade power propagates only where the country has a ship-propagation modifier, at the compounded rate: the propagation share multiplied by that modifier. | UNCHANGED | ENGINE | stipulated | L721 |
| Y385 | Propagation is strictly one hop and never chains. | UNCHANGED | ENGINE | stipulated | L722 |
| Y386 | A node receives the summed contributions of all its downstream neighbours. | UNCHANGED | ENGINE | stipulated | L723 |
| Y387 | Direction for propagation is read from `Φ_w`. | UNCHANGED | MODEL | stipulated | L725 |

## §1.10 — Direction-dependent systems (L727-783)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y388 | Any mechanism gated on one nation being upstream or downstream of another evaluates TRUE. | UNCHANGED | DESIGN | stipulated | L729 |
| Y389 | Any node-pair direction dependency reads `Φ_w`. | UNCHANGED | DESIGN | stipulated | L731 |
| Y390 | Where a gate scopes a set or a path, that scope reads `Φ_w` with a three-rung fallback ladder: the `Φ_w` path, else the shortest path within a single good's graph, else the undirected shortest path. | UNCHANGED | DESIGN | stipulated | L733-737 |
| Y391 | The mechanics below the gates are unpatched and unchanged; reorientation reaches them through the trade power distribution rather than any direction test, because §1.9's propagation is direction-dependent, so a flip moves propagated power at both ends and changes fan-out across the neighbourhood. | UNCHANGED | ENGINE | algebraic derivation | L739 |
| Y392 | Nothing in that group is patched and all of it moves monthly. | UNCHANGED | MODEL | stipulated | L739 |
| Y393 | Trade-conflict casus belli thresholds are `JUSTIFY_TRADE_CONFLICT_LIMIT` (target) and `JUSTIFY_TRADE_CONFLICT_ACTOR_LIMIT` (actor). | UNCHANGED | INSTALL | read from a file | L745-746 |
| Y394 | Privateer blocking is thresholded by `MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER`. | UNCHANGED | INSTALL | read from a file | L747 |
| Y395 | Trade-company extra merchant and control are thresholded by `TRADE_COMPANY_STRONG_LIMIT` and `TRADE_COMPANY_CONTROL_LIMIT`. | UNCHANGED | INSTALL | read from a file | L748-749 |
| Y396 | Improve Inland Routes needs 50% to establish and 40% to maintain plus a merchant present in the node, and is waived entirely by the `free_improve_inland_routes` government attribute. | UNCHANGED | INSTALL | read from a file | L750 |
| Y397 | Propagate Religion needs 50% to establish and 50% to maintain in the default branch and 35/35 in the terminal branch, neither banded. | UNCHANGED | INSTALL | read from a file | L751 |
| Y398 | The nine `N_trade_power_for_propogate_religion` country-flag rungs are banded: maintain trails select by 5–10 points (10→5, 15→5, 20→10, 25→15, 30→20, 35→25, 40→30, 45→35), and the 5-flag carries no maintain share at all. | UNCHANGED | INSTALL | read from a file | L751 |
| Y399 | The banding is the reverse of what v1 recorded: Improve Inland Routes is the one unconditionally banded mechanic, every other listed threshold is single-valued, and Propagate Religion is banded only on its flag ladder. | UNCHANGED | INSTALL | read from a file | L753-755 |
| Y400 | Banding therefore absorbs very little chatter: a power share oscillating across any single-valued limit flickers the mechanic, including Propagate Religion for the flagless countries its default and terminal branches cover. | CHANGED | ENGINE | algebraic derivation (v5 said "almost nothing absorbs threshold chatter") | L755-757 |
| Y401 | Banding is not the only damper: three shipped defines rate-limit the mechanics that carry these thresholds. | NEW | INSTALL | read from a file | L757-758 |
| Y122 | `TRADING_POLICY_COOLDOWN_MONTHS = 12` applies to seven of the nine entries in `common/trading_policies/00_trading_policies.txt` — five distinct policies, four of them with an `_upgraded` twin, plus Propagate Religion which has none — so seven of nine entries, or four of the five families, are rate-limited. | NEW | INSTALL | read from a file | L758-763 |
| Y123 | `maximize_profit` and `maximize_profit_upgraded` carry `cooldown = no` in `common/trading_policies/00_trading_policies.txt`, and Propagate Religion is inside the cooldown. | NEW | INSTALL | read from a file | L763-764 |
| Y124 | `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` with `TRADE_COMPANY_COOLDOWN = 60` means a flickering share does not translate into a flickering effect at those three mechanics. | NEW | INSTALL | read from a file | L764-766 |
| Y125 | What is left exposed is everything without a cooldown, which is most of the ladder. | NEW | ENGINE | algebraic derivation | L766-767 |
| Y402 | The flicker-risk set is "every country at a single-valued limit, plus flagless countries at Propagate Religion's 50/50 or 35/35", not "every country". | UNCHANGED | ENGINE | algebraic derivation | L767-769 |
| Y403 | Casus belli availability is the most visible symptom, since it can appear and vanish month to month. | UNCHANGED | ENGINE | algebraic derivation | L769-770 |
| Y404 | Caravan power is in this group but is not a threshold mechanic and is not a function of raw trade power at all: it is total country development divided by `CARAVAN_FACTOR` plus policy and idea modifiers, clamped to [`CARAVAN_POWER_MIN`, `CARAVAN_POWER_MAX`], switched on by a merchant condition. | UNCHANGED | INSTALL | read from a file | L772 |
| Y405 | When caravan power applies it is worth up to the cap for any major power — enough to move a node's power shares by itself and therefore to push other countries across the thresholds above. | UNCHANGED | MODEL | algebraic derivation | L772 |
| Y126 | Measured on the 1444 start, the caravan cap of 50 is 9.4% to 47.0% of an inland node's total trade power, median 21.6%, over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. | CHANGED | MODEL | numerical test over save data; no script named | L772 |
| Y127 | As a share of the node's total after the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, median 17.7%; v5.0 quoted those under the first description, which cannot be right since 8.6% of 532.0 is 45.8 rather than 50. | CHANGED | MODEL | numerical test | L772 |
| Y128 | On §2.2's derived 25-node inland basis (dropping `siberia`) the median is 21.3%, or 17.5% after the grant. | CHANGED | MODEL | numerical test | L772 |
| Y406 | The largest single incumbent holder runs 23.6 to 143.2, so a country at the caravan cap outweighs the largest incumbent in 7 of the 26 inland nodes and is outweighed in the other 19. | UNCHANGED | MODEL | numerical test | L772 |
| Y407 | v4.0 read the save's per-node `highest_power` field as the largest incumbent's power; it is not — parsing each node's country sub-blocks at their own brace depth, `highest_power` differs from the largest single country's `val` on 79 of 79 nodes (at `venice` 53.2 against Venice's own 106.2) and it matches no share of `total`, `max`, `p_pow` or `collector_power` either. | UNCHANGED | INSTALL | read from a file (the save) | L772 |
| Y408 | What `highest_power` does hold was not determined, and the model does not read it. | UNCHANGED | MODEL | stipulated | L772 |
| Y409 | v1 and v2 both described caravan power as "a step function on raw power", which contradicted their own §3.11. | UNCHANGED | MODEL | read from a file (the prior spec versions) | L772 |
| Y410 | No mission, decision, event, or trade company in 1.37.5 names a trade node — zero non-comment references across all of `common/`, `missions/`, `decisions/` and `events/`. | UNCHANGED | INSTALL | read from a file | L774-776 |
| Y411 | Trade companies are bare province lists. | UNCHANGED | INSTALL | read from a file | L775-776 |
| Y412 | Scripted content reaches nodes only structurally, through `home_trade_node`, `any/random/every_active_trade_node`, `*_trade_node_member_province` and `highest_value_trade_node`. | UNCHANGED | INSTALL | read from a file | L776-778 |
| Y413 | Nodes themselves never change under the mod — only connections do — so the name-collision class of conflict is empty and the conclusion is stronger than v1 stated. | UNCHANGED | MODEL | algebraic derivation | L778-779 |
| Y414 | What remains exposed is semantics: `highest_value_trade_node` and node-scoped triggers are evaluated against a reoriented graph, so a mission written against vanilla's flow can change sense without ever breaking. | UNCHANGED | ENGINE | algebraic derivation | L779-782 |
| Y415 | That semantic exposure is accepted and listed for the compatibility pass rather than engineered around. | UNCHANGED | DESIGN | stipulated | L782-783 |

## §1.11 — Treasure fleets (L785-792)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y416 | The overlord always receives the treasure fleet. | UNCHANGED | DESIGN | stipulated | L787 |
| Y417 | The fleet routes by the §1.10 ladder, passing each node en route where privateers skim a share proportional to their power there. | UNCHANGED | MODEL | stipulated | L787 |
| Y418 | Where the diversion mechanic is active, colonial gold income is diverted from the colonial nation. | UNCHANGED | ENGINE | stipulated | L789-790 |
| Y419 | Diverted gold does not enter `wealth` at either end, for the deeper reason of §1.5: gold income is its own engine category and never enters `wealth` in the first place, diverted or not. | UNCHANGED | MODEL | algebraic derivation | L790-791 |

## §1.12 — What the game displays (L793-810)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y420 | The in-game economy is the per-good economy: node values, the node window, pie charts, the ledger, the economy tab and tooltips all show the model's numbers. | UNCHANGED | DESIGN | stipulated | L795 |
| Y421 | Trade map mode colours provinces by node and draws arrows between nodes rendering `Φ_w`, with arrow weight from realized value crossing the link. | UNCHANGED | MODEL | stipulated | L797 |
| Y422 | Clicking a province switches province colouring to the vanilla trade-goods rendering for that good and redirects the arrow layer to that good's graph; a sink is visible as a node with no outgoing arrows; clicking the node icon clears back to `Φ_w`. | UNCHANGED | MODEL | stipulated | L799 |
| Y423 | Value broken down by commodity is not representable in the vanilla UI: the node window carries several node-level value fields (incoming, local, total, outgoing) but none takes a commodity argument — zero per-good fields, where thirty would be needed. | UNCHANGED | ENGINE | read from a file (the node window's fields) | L803-805 |
| Y424 | A link's two-way traffic is not representable: one scalar per link, shown as net. | UNCHANGED | ENGINE | stipulated | L806 |
| Y425 | Per-country effective trade power where eligibility differs by good is not representable and is shown as a value-weighted aggregate. | UNCHANGED | ENGINE | stipulated | L807 |
| Y426 | There is no new art, sprites, shaders or map-mode chrome; making the node window's existing incoming-link entries assignable is the only UI change. | UNCHANGED | DESIGN | stipulated | L809-810 |

## §2.1 — Shape (L816-843)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y427 | The implementation is one program: a runtime-attached DLL that each month reads live game state, solves per good, propagates the per-good economy externally, and writes the result and the orientation back into the engine's own structures. | UNCHANGED | DESIGN | stipulated | L818 |
| Y428 | It ships with a generated `00_tradenodes.txt` for load time and a companion overlay for what the engine cannot display. | UNCHANGED | DESIGN | stipulated | L818 |
| Y429 | The target platform is Windows/Steam. | UNCHANGED | DESIGN | stipulated | L820 |
| Y430 | Achievements are off with any mod (`ACHIEVEMENTS_DISABLED_MODIFIED_GAME`). | UNCHANGED | INSTALL | read from a file (a named string) | L820-821 |
| Y431 | The engine will load an ironman save in a modded game — `Loading ironman in modded game` is a shipped code path — so the parsers target non-ironman because ironman saves are binary-encoded rather than because ironman is unavailable. | UNCHANGED | INSTALL | read from a file (a binary string) | L821-823 |
| Y432 | Multiplayer is unsupported by default: an identical build is necessary and not sufficient, because EU4 multiplayer is lockstep with checksums and an in-process floating-point solve can produce different results on different hardware — differing SIMD dispatch or accumulation order in the linear algebra is enough to desync. | UNCHANGED | ENGINE | algebraic derivation | L825 |
| Y433 | Supporting multiplayer requires the computation to be bit-reproducible across machines. | UNCHANGED | DESIGN | algebraic derivation | L825 |
| Y434 | For DRAIN the exposure is narrower than v1's dense linear algebra but still real: the min-cost-flow solve must return the same optimum given identical input (fixed arc ordering, one solver build, no threading). | UNCHANGED | MODEL | algebraic derivation | L825-827 |
| Y435 | The sweep is deterministic given the LP's support and a fixed accumulation order, because its comparisons are of input-derived floats (`DEF`, `b`) rather than of solver residuals — which is the distinction that matters against v1's dense algebra, but it is not integer arithmetic and v2 called it that. | UNCHANGED | MODEL | algebraic derivation | L827-830 |
| Y436 | DRAIN's cross-machine reproducibility reduces to the LP's, so until that is built and verified the mod ships single-player only. | UNCHANGED | DESIGN | stipulated | L830-831, L841-843 |
| Y995 | §2.3's tie-break narrows one part of the desync exposure and leaves the rest: on the aggregate graph the optimum is unique, so which vertex of a degenerate optimal face the solver lands on is no longer a desync path and that was the largest single exposure; what remains is ordinary float reproducibility of a cost vector computed from wealth, plus the still-degenerate per-good optima (§2.4 item 1) and the whole propagated per-good economy downstream of them — node values, the ledger and the economy tab — with the direction-free value weights `V_g` the exception. | NEW | MODEL | algebraic derivation | L833-841 |

## §2.2 — Solver (L845-888)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y437 | Solver item 1 is a parser for `common/tradenodes/00_tradenodes.txt` reading adjacency, `members`, `path`/`control` render data, and `end`/`inland`/AI flags. | UNCHANGED | DESIGN | stipulated | L847 |
| Y438 | Solver item 2 is a parser for non-ironman saves reading province owner, `base_tax`, `base_production`, trade good, goods produced and development. | UNCHANGED | DESIGN | stipulated | L848 |
| Y439 | Solver item 3 is a parser for `common/defines.lua` merged with `common/defines/` overrides in load order. | UNCHANGED | DESIGN | stipulated | L849 |
| Y129 | Solver item 4 computes `TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production · (1 + province-state goods modifiers) · price`, with no autonomy, efficiency, ideas or owner terms. | CHANGED | DESIGN | stipulated | L850-852 |
| Y130 | The only modifiers in scope are the five that describe the province's own condition, of which the reference implementation applies four; at 1444 `devastation` is live on eleven provinces and `unrest` on twenty-one, and `unrest` is not read. | CHANGED | MODEL | numerical test | L853-856 |
| Y440 | `GP_COEFF` is read from `common/static_modifiers/00_static_modifiers.txt` rather than hardcoded. | CHANGED | INSTALL | read from a file | L855-856 |
| Y131 | World wealth is 10,607.40 annual ducats over 2,472 counted provinces. | CHANGED | MODEL | numerical test; no script named at this line | L859 |
| Y441 | Solver item 5 is DRAIN per good: a min-cost b-flow using network simplex or a simplex LP rather than interior-point without crossover, because §1.1's spanning-tree-basis property requires a basic optimum, then the deterministic drainage sweep and the Phase-4 evaluator. | UNCHANGED | DESIGN | stipulated | L860-863 |
| Y442 | The Phase-4 evaluator's `unserved` and `stranded` must be equal by conservation, since the sum of `b_g` over nodes is 0 identically. | UNCHANGED | MATH | algebraic derivation | L862-863 |
| Y443 | `Φ_w` is one more DRAIN run with wealth as the good — the 30th solve, same code path. | UNCHANGED | MODEL | stipulated | L864 |
| Y444 | Solver item 6 is a survival table `S_g[n][H]` for AI scoring, one table serving every country. | UNCHANGED | DESIGN | stipulated | L865 |
| Y445 | Solver item 7 is a mutual reachability census: 30 goods × 80 BFS producing an 80×80 matrix whose entry counts goods with a directed path from n to m. | UNCHANGED | DESIGN | stipulated | L866 |
| Y446 | Solver item 8 is a synthetic-shock harness that edits parsed province data and re-solves. | UNCHANGED | DESIGN | stipulated | L867 |
| Y447 | Cost per good is one uncapacitated min-cost flow on 80 nodes and 318 arcs plus an O(V+E) sweep. | UNCHANGED | MODEL | algebraic derivation | L869 |
| Y132 | Measured on the reference implementation (scipy/HiGHS plus the deterministic sweep, one machine): of order 0.1 s for all 29 goods, and single-digit milliseconds per good on average — and that is the whole of the claim. | CHANGED | MODEL | numerical test | L870-872 |
| Y133 | Repeated 12-run experiments on one machine do not reproduce each other closely enough to support anything finer — three replicates gave per-good averages spanning 3.5–10.5, 3.5–10.8 and 3.1–4.7 ms — so no range is quoted, because the quantity being measured is a machine and a scheduler rather than the algorithm. | NEW | MODEL | numerical test | L872-875 |
| Y134 | v5.0's "0.17–0.21 s for all 29 goods" is not reproducible: across three replicates of twelve runs the number of runs landing inside that interval was 1, then 0, then 0. | NEW | MODEL | numerical test | L875-877 |
| Y448 | "Milliseconds each" holds already with a generic LP; the all-29 figure is what a native network simplex would have to improve on, and no measurement in this project supports a specific projection, so none is offered. | UNCHANGED | DESIGN | stipulated | L877-880 |
| Y449 | There are two implementations of one specification: the reference solver (standalone, run against parsed saves, and the thing every §2.8 validation is measured on) and the shipped DLL, which carries a second implementation of items 4–7 in the host language reading live memory instead of save files. | UNCHANGED | DESIGN | stipulated | L882 |
| Y450 | The two implementations must agree on orientation exactly — a combinatorial comparison with no tolerance band — and where they disagree the reference is correct by definition. | UNCHANGED | DESIGN | stipulated | L882-884 |
| Y451 | The parsers and the harness stay reference-only, and the DLL never reads a save. | UNCHANGED | DESIGN | stipulated | L884 |
| Y452 | Inland is derived rather than trusted from the flag: a node with no coastal province among its `members`. | UNCHANGED | DESIGN | stipulated | L886-887 |
| Y453 | The derivation and the flag disagree at exactly one node — `siberia` carries `inland=yes` but has two Arctic-coast members (1781, 1782) — so derivation gives 25 inland nodes against the flag's 26. | UNCHANGED | INSTALL | read from a file | L887-888 |

## §2.2a — What map this is for (L890-930)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y454 | v2 called the target "map-agnostic" while proving its central properties only for the map it was measured on; v3.0 picks the narrower target and states the two premises the proofs actually need. | UNCHANGED | MODEL | stipulated | L892-894 |
| Y455 | Premise 1 is that the node graph is connected: reachability is LP feasibility, and the LP is feasible because the sum of `b_g` over nodes is 0 identically. | UNCHANGED | MATH | algebraic derivation | L896-897 |
| Y456 | On a graph with more than one component the global balance is not enough — each component must balance separately, share normalisation does not deliver that, and a two-component graph carrying cross-component imbalance is infeasible outright, so the solver returns no flow at all rather than a worse one. | UNCHANGED | MATH | algebraic derivation | L897-900 |
| Y457 | Vanilla 1444 is one component. | UNCHANGED | MODEL | numerical test | L900 |
| Y458 | The solver must compute components once at load; on a single component it proceeds, and on more than one it must either renormalise `s` and `c` within each component so every component balances, or refuse to start and say which nodes are unreachable. | UNCHANGED | DESIGN | stipulated | L902-905 |
| Y459 | The solver must not silently hand an infeasible program to the LP. | UNCHANGED | DESIGN | stipulated | L905-906 |
| Y460 | v1 carried per-component renormalisation and v2 dropped it without replacement; v3 restores the requirement. | UNCHANGED | MODEL | read from a file (the prior spec versions) | L906-907 |
| Y461 | Premise 2 is that Phase 0 is a no-op, or the map-dependent properties are read as measurements: several §1.1 properties are proved for the 2-core and hold on any map where Phase 0 removes nothing (minimum degree at least 2, no bridges — true of vanilla). | UNCHANGED | MATH | algebraic derivation | L909-911 |
| Y462 | Where Phase 0 acts, three properties weaken and the spec says so rather than asserting through it. | UNCHANGED | DESIGN | stipulated | L911-912 |
| Y463 | Global DAG is proved on a 2-core map and still proved where Phase 0 acts, because pendant edges are bridges and cannot close a cycle. | UNCHANGED | MATH | algebraic derivation | L916 |
| Y464 | Sink-set equality is measured exact 29/29 on a 2-core map and fails where Phase 0 acts, because a pendant net-importer is a sink outside the set. | UNCHANGED | MODEL | numerical test plus algebraic derivation | L917 |
| Y465 | Marking order reproduces the DAG on a 2-core map and fails where Phase 0 acts, because pendants have no marking order so `Φ_ord`-style order comparison is undefined on pendant edges. | UNCHANGED | MATH | algebraic derivation | L918 |
| Y135 | Where Phase 0 acts, free-edge determinism is unaffected but index-independence is not: the key reads the post-fold balance β, so peeling can create exact ties the raw balances do not have, and the 1444 measurement does not transfer. | CHANGED | MODEL | algebraic derivation | L919 |
| Y466 | Two further cases are independent of Phase 0 and both break sink-set equality inside the 2-core: a selected flow-terminal demander can lose sinkhood to a free edge that reaches an earlier-marked node (T2), and a fallback promotion can become a sink that was neither selected nor stall-promoted (T3). | UNCHANGED | MODEL | numerical test (worked in §3.2) | L921-924 |
| Y467 | The stated target is connected maps: on a connected map with minimum degree at least 2 every §1.1 property is either proved or measured-and-labelled. | UNCHANGED | DESIGN | stipulated | L926-927 |
| Y468 | On a connected map with pendants the algorithm still runs and still produces an acyclic, fully-oriented, demand-serving graph; only the sink-set characterisation and the order-potential reconstruction weaken. | UNCHANGED | MODEL | algebraic derivation | L927-929 |
| Y469 | On a disconnected map the solver must renormalise per component or refuse. | UNCHANGED | DESIGN | stipulated | L929-930 |

## §2.3 — Constants (L932-1011)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y470 | Constants are read at runtime and never hardcoded. | UNCHANGED | DESIGN | stipulated | L934 |
| Y471 | The nine runtime-read uses map to named defines: `TRADE_PROPAGATE_DIVIDER`, `TRADE_PROPAGATE_THRESHOLD`, `TRADE_NON_CAPITAL_OFFICE`, `TRADE_POWER_HOME_BONUS`, `MERCHANT_MAX_POWER_BONUS`, `TRADE_MERCHANT_PRESENT`, `TRADE_ADDED_VALUE_MODIFER`, the three caravan terms, and `PS_MOVE_TRADE_PORT`. | UNCHANGED | INSTALL | read from a file | L936-946 |
| Y472 | `TRADE_MERCHANT_PRESENT` is a bonus on income, not trade efficiency. | UNCHANGED | INSTALL | read from a file | L943 |
| Y136 | The two wealth coefficients are not the same kind of constant: the emitter reads `GP_COEFF` rather than carrying 0.2 because a mod or a patch can change it, and only `TAX_COEFF` must be re-measured against any patch that is not 1.37.5. | CHANGED | DESIGN | stipulated | L948-954 |
| Y137 | v3.0 through v5.0 said neither coefficient was in a file, and shipped a whole-install modifier sweep that walked past the block holding one of them. | NEW | MODEL | read from a file (the prior spec versions and their sweep) | L954-956 |
| Y473 | `GP_COEFF` is 0.2 goods produced per point of `base_production`, measured on four provinces at four development levels from the `Base Goods Produced` line: Caceres (1747) at 2 gives 0.40, Girona (212) at 3 gives 0.60, Garnatah (223) at 4 gives 0.80 with the itemisation `Base Goods Produced: 0.80 / Base Production: +0.80`, and Barcelona (213) at 5 gives 1.00. | UNCHANGED | ENGINE | measured in-game | L960 |
| Y474 | `TAX_COEFF` is 1.0 ducat per year per point of `base_tax`, measured on two provinces at two development levels from the `(Yearly …)` parenthetical, and the displayed monthly is the truncation of `base_tax × 0.083333`. | UNCHANGED | ENGINE | measured in-game | L961 |
| Y475 | Both coefficients are read off the tooltips' base lines, which carry no owner term — Garnatah also has `local_autonomy = 0`. | UNCHANGED | ENGINE | measured in-game | L963-964 |
| Y476 | Neither coefficient is read off a province window, because a window figure carries the owner's modifiers and some of those are randomised at game start. | UNCHANGED | ENGINE | measured in-game | L964-965 |
| Y477 | Prices come from `common/prices/00_prices.txt` at runtime and are never hardcoded. | UNCHANGED | INSTALL | read from a file | L965-966 |
| Y478 | The design constants are the excluded-goods list (defaulting to gold), the α price anchor `P₀ = 2.0`, the aggregate-graph exponent `α_Φ = 2.0`, and the Phase-2 tie-break strength `TIE_EPS = 1e-3`. | CHANGED | DESIGN | stipulated | L968-970 |
| Y479 | `α_Φ` and `TIE_EPS` are hyperparameters whose values are developer taste, the document offers no justification for either, and every derivation previously offered for `α_Φ` is withdrawn with none replacing it — v2.1 through v4.0's two-sink calibration and v5.0's widest-band argument are both withdrawn. | CHANGED | MODEL | stipulated | L976-979 |
| Y339 | Changing either value is a design decision, and §1.6 records how the field responds around them so the decision can be made with the sensitivity in view — documentation for whoever changes them rather than an argument for the current values. | CHANGED | DESIGN | stipulated | L979-982 |
| Y480 | DRAIN's three knobs sit at their defaults: demand-mass quantile `ρ = 1.0`, cluster dilation `r = 0`, and the zero-flow tolerance `1e-11`. | UNCHANGED | MODEL | stipulated | L970-971 |
| Y481 | The zero-flow tolerance is not purely numerical: it is an absolute threshold, so it couples to the scale of `b`. | UNCHANGED | MODEL | algebraic derivation | L971-973 |
| Y482 | A measured calibration option that moves all three knobs plus α's clamp is recorded in §3.13, and the baseline does not use it. | UNCHANGED | DESIGN | stipulated | L973-974 |
| Y996 | `TIE_EPS` sets the Phase-2 objective as `cost(u, v) = 1 + TIE_EPS · (w[u] + w[v]) / 2` with `w` node wealth normalised to [0, 1]; the cost's symmetry and its reading node wealth only are load-bearing (a directional preference is a potential difference and cannot break a tie; a wealth-only cost is invariant under relabelling by construction), while the normalisation is not, because rescaling `w` is equivalent to rescaling `TIE_EPS` and the answer is constant over about six orders of magnitude of it. | NEW | MATH | algebraic derivation | L984-997 |
| Y997 | Every DRAIN solve uses this cost, per good as well as aggregate, and since `w` is node wealth the same cost vector serves all of them; what keeps unit arc costs is the separate comparison operators — the FLOW and TREE operators in `flowop.py` and the per-good checks in `verify.py` — because `mincost_flow`'s cost argument defaults to unit. | NEW | MODEL | read from a file (the named scripts) | L999-1002 |
| Y998 | A single cost vector does not make every solve unique: `b_w` has no zero entries and its optimum is unique under this cost, while each `b_g` puts a different face of the polytope in play and 84 of 290 per-good relabellings still move an edge; adding a second wealth term does not close it, because the obstruction is different routings with equal totals rather than individual arcs with equal costs. | NEW | MATH | algebraic derivation plus numerical test (§2.4 item 1) | L1004-1009 |
| Y483 | DLC state is a third input axis: treasure-fleet diversion and caravan power are both DLC-conditional, and caravan modifier values are readable even when inert, so the model keys on the DLC flag and never on the presence of a value. | UNCHANGED | ENGINE | stipulated | L1011 |

## §2.4 — The tradenodes file (L1013-1093)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y484 | The tradenodes file is generated once from the campaign start date's `Φ_w` and then owned by the DLL in memory, with no per-session regeneration; merchants are recalled only when the mod is rebuilt, and a mid-campaign load runs on the start-date file for up to one month. | UNCHANGED | DESIGN | stipulated | L1015 |
| Y485 | The engine performs no topological sort; it validates that the file is one, logging `[tradenodedefinition.cpp:61]` once per violating link, but it tolerates violations. | UNCHANGED | ENGINE | engine test | L1017-1020 |
| Y486 | Measured: a file with all 159 links declared backwards logged exactly 159 such errors and then loaded and played normally, with node `total` and `retention` unchanged and the power-dependent fields differing only within the engine's own run-to-run variance. | UNCHANGED | ENGINE | engine test | L1020-1022 |
| Y487 | What the engine does not tolerate is a cycle: a hand-authored two-node cycle produced `EXCEPTION_STACK_OVERFLOW` at a single exception address (`0x00007FF6DDE6A8B4`) under 1002 recorded `eu4.exe` frames, reproduced on three launches, with vanilla and the reversed-order file both loading fine as controls. | UNCHANGED | ENGINE | engine test (cited to `../v2-drain/game-session.md`) | L1024-1029 |
| Y488 | The crash dump records no per-frame addresses. | UNCHANGED | ENGINE | engine test | L1026 |
| Y489 | Acyclicity is therefore a hard correctness requirement of the emitter, established by observation rather than assumed. | UNCHANGED | DESIGN | engine test | L1027-1029 |
| Y490 | A reversed link is honoured completely: moving one `outgoing` block from `sevilla` to `valencia` with the path list and control pairs reversed loaded with zero errors and rebuilt the economy around the new direction. | UNCHANGED | ENGINE | engine test | L1031-1033 |
| Y491 | In that test Valencia moved from Sevilla's outgoing side to its incoming side, Sevilla became an end node with zero outgoing value, Castile's merchant switched from steering to collecting, and the two countries that had held power in Sevilla purely by downstream propagation disappeared from the node. | UNCHANGED | ENGINE | engine test | L1033-1036 |
| Y492 | Every provincial power figure was unchanged in that test. | UNCHANGED | ENGINE | engine test | L1036 |
| Y493 | That test is the mod's core premise verified end to end. | UNCHANGED | DESIGN | stipulated | L1037 |
| Y494 | Item 1: emit in decreasing `Φ_w` marking order, which is the convention the engine states and the shipped vanilla file follows (0 of 159 links violate it), and violating it is non-fatal but logs one error per link. | UNCHANGED | INSTALL | read from a file plus engine test | L1039-1041 |
| Y138 | A canonical node order is still a correctness requirement but is no longer what decides the installed map: the emitter must fix one canonical order and keep it stable across rebuilds, that order must be the order Phase 2's LP input is built in rather than merely the order the sweep breaks ties in, and what keeps it a requirement is that the installed aggregate graph is invariant over the orderings tried while the per-good graphs are not, with §2.2 propagating the per-good economy and writing it back. | CHANGED | DESIGN | algebraic derivation over the measurements in this item | L1041-1043, L1059-1062, L1068-1070 |
| Y495 | Phase 2's min-cost b-flow is degenerate under unit arc costs: many distinct supports carry the same optimal cost, and which one the solver returns depends on the order the nodes and arcs are presented in. | NEW | MATH | algebraic derivation | L1045-1047 |
| Y139 | Measured on that objective, 40 of 40 permutations return a different optimal support. | NEW | MODEL | numerical test | L1047-1048 |
| Y140 | Those permutations reach an objective identical to within a few units in the last place. | NEW | MODEL | numerical test | L1047-1048 |
| Y147 | §2.3 now breaks those ties inside the objective. | NEW | MODEL | stipulated | L1048 |
| Y141 | On the same LP under the tie-break cost 0 of 40 permutations return a different support, and running the aggregate graph end-to-end over 180 relabellings (three seeds of 60) moved 0 of 159 edges in every run; `relabel6.py` validates its instrument against `drain.py` on the identity permutation and aborts if that fails — and did abort when the tie-break went in, because the instrument still minimised the old objective and disagreed on 26 of 159 edges. | NEW | MODEL | computed by a named script (`relabel6.py`) | L1049-1053 |
| Y143 | The tie-break cost is built from good-independent node wealth so it applies to every per-good solve, but it need not break ties in a per-good LP whose `b` is a different vector: measured across 29 goods × 10 relabellings, 84 of 290 runs changed a per-good orientation, a mean of 0.99 edges and up to 15. | NEW | MODEL | numerical test | L1055-1059 |
| Y999 | A second wealth term (`+ TIE_EPS² · abs(w[u] − w[v])`) was tried and rejected: it makes all 159 arc costs distinct where the shipped cost leaves 3 pairs equal, and still leaves 72 of 232 per-good supports moving, down from 93 — distinct arc costs are not the issue, equal totals over different routings are, and ruling those out needs a generic perturbation, which is arbitrary by construction. | NEW | MODEL | numerical test | L1062-1066 |
| Y146 | The counts are HiGHS-specific in their detail but not in kind: any simplex returns a vertex of a degenerate optimal face, and the tie-break's job is to leave only one vertex to return. | NEW | MODEL | algebraic derivation | L1070-1071 |
| Y144 | v6.0 quoted a 580-of-580 per-good sweep from `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`; that script measures the unit-cost objective, so its figure describes the former solver and is superseded by the 84-of-290 rather than contradicted by it. | NEW | MODEL | read from a file (the named script) | L1072-1075 |
| Y148 | §1.1's priority key ties in more places than §1.1 documents — besides the free-edge sweep it decides Phase 1's within-cluster argmin, the stall promotion's identical form, and the top-k cut when two clusters carry equal mass — and none of them fires on 1444 (zero exact `(DEF, β)` ties on free edges across 29/29 goods, zero within-cluster β ties, zero tied cluster masses), so no measured figure here depends on them. | CHANGED | MODEL | numerical test | L1077-1082 |
| Y496 | One visible consequence of node order: the node window renders its incoming/outgoing link lists in file declaration order, so reordering nodes reorders what the player sees. | UNCHANGED | ENGINE | engine test | L1082-1084 |
| Y497 | Item 2: `end=yes` on every `Φ_w` sink, stripped from any former end node that gains outgoing links. | UNCHANGED | DESIGN | stipulated | L1085, L1088-1089 |
| Y149 | The end-flag list is a function of the world rather than of the node order: across the 180 relabellings of item 1 the end set came back as `{genua, hangzhou}` every time, which is a change from v6.0, where the list moved with the ordering and this item warned about it. | NEW | DESIGN | numerical test | L1085-1088 |
| Y150 | 1444 has two end nodes, `genua` and `hangzhou`, against vanilla's three. | CHANGED | MODEL | numerical test | L1088-1089 |
| Y498 | The end count is not fixed — it follows the wealth field and `α_Φ` — so the emitter reads it from the solve rather than assuming a number. | UNCHANGED | DESIGN | stipulated | L1089-1091 |
| Y499 | Item 3: link reversal means moving the `outgoing` block, reversing the `path` province list and reversing the `control` pairs, and one hand-flipped link is to be verified before writing generator code. | UNCHANGED | DESIGN | stipulated | L1092 |
| Y500 | Item 4: `location`, `members`, `inland=yes`, `ai_will_propagate_through_trade` and unrecognized keys round-trip byte-faithfully. | UNCHANGED | DESIGN | stipulated | L1093 |

## §2.5 — Runtime attachment (L1095-1099)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y501 | Attachment uses pattern scanning and function hooking, following the EU4dll precedent, which provides the attach scaffolding on this binary but nothing about trade structures. | UNCHANGED | DESIGN | stipulated | L1097 |
| Y502 | The mod ships a runtime-patching DLL rather than a modified executable. | UNCHANGED | DESIGN | stipulated | L1097 |
| Y503 | The binary is frozen, so offsets found stay found. | UNCHANGED | ENGINE | stipulated | L1097 |
| Y504 | The nation-pair direction gates of §1.10 are hooked and returned true at the call site rather than by forcing any shared predicate. | UNCHANGED | DESIGN | stipulated | L1099 |

## §2.6 — Writing to the engine (L1101-1121)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y505 | The monthly trade tick runs in three passes: static power and modifiers; a pass from the end nodes determining modified power and adding propagation; and a value pass from the origin nodes computing node value, collect/steer split, collect division, and outgoing division with steering bonuses. | UNCHANGED | ENGINE | stipulated | L1103 |
| Y506 | Written each tick: node trade value as the sum over goods of `value_g(n)`. | UNCHANGED | MODEL | stipulated | L1109 |
| Y507 | Written each tick: node collectible pool as the sum over goods of `value_g(n) · collected_share(n,g)`. | UNCHANGED | MODEL | stipulated | L1110 |
| Y508 | Written each tick: per-link value as net realized flow summed over goods, in the installed `Φ_w` direction. | UNCHANGED | MODEL | stipulated | L1111 |
| Y509 | Country trade income is derived by the engine from the written fields, unless stored. | UNCHANGED | ENGINE | stipulated | L1112 |
| Y510 | Feeding the engine the collectible pool is sufficient for a narrower reason than it looks: `collect_pool` is itself per good on the inside, because `collected_share(n,g)` depends on `P_transfer(g)`. | UNCHANGED | MODEL | algebraic derivation | L1114 |
| Y511 | What factors out is `powershare_C`, a country's share among collectors, and whether a country collects is a merchant-or-home property with no good dependence at all, so a good-independent share multiplies a per-good sum, the sum collapses to one scalar, and the engine's own vanilla collection math reproduces every country's per-good income exactly. | UNCHANGED | MATH | algebraic derivation | L1114 |
| Y512 | There are two deadlines, not one window: display immediately after the value pass, because AI consumers read these figures during the month. | UNCHANGED | ENGINE | stipulated | L1118 |
| Y513 | Payment is bounded by the month boundary, since the treasury reconciles at the start of each month against the previous month's income. | UNCHANGED | ENGINE | stipulated | L1119 |
| Y514 | Per-link values are written net, which can be negative where realized flow opposes the drawn arrow. | UNCHANGED | MODEL | algebraic derivation | L1121 |

## §2.7 — Probes (L1123-1161)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y515 | Items 1–10 are the v1 probe set, settled with a debugger on a vanilla install in one session, though the claim audit found several are observable without one. | UNCHANGED | DESIGN | stipulated | L1125-1126 |
| Y516 | Items 12–15 are done: they were run against 1.37.5 in `../v2-drain/game-session.md` and their results are folded into §1.9, §2.4 and §3.6. | UNCHANGED | ENGINE | engine test (cited to a named session log) | L1128-1129 |
| Y517 | Item 12 was dropped rather than run, because under owner-agnostic wealth the per-province production-income field is not read by anything. | UNCHANGED | DESIGN | stipulated | L1129-1131 |
| Y518 | Probe 13 settled and reversed the hedge: the engine does not tolerate a cycle — `EXCEPTION_STACK_OVERFLOW`, 1002 frames at one address, twice. | UNCHANGED | ENGINE | engine test | L1133-1134 |
| Y519 | Probe 14 settled and confirmed the spec: the incoming-link entry only navigates, and clicking `Safi` in Sevilla's window switched the window to Safi and dispatched nothing. | UNCHANGED | ENGINE | engine test | L1135-1136 |
| Y520 | Probe 15 settled and reversed the spec's caution: the tooltip's "where it already has power" is not a precondition, since France holds zero provinces and zero merchants in Sevilla and still receives 3.3 power there, itemised as `Transfers from traders downstream: +3.1`. | UNCHANGED | ENGINE | engine test | L1137-1140 |
| Y151 | §1.9's "every immediately upstream node" is consistent with probe 15's reading — one observation on one node, enough to retire the cautionary case and not enough to promote the rule to a measurement. | CHANGED | ENGINE | engine test (one observation) | L1140-1142 |
| Y521 | The §2.4 item 3 link-reversal check is done and passed: a hand-flipped link loaded with zero errors and rebuilt the economy around the new direction. | UNCHANGED | ENGINE | engine test | L1143-1144 |
| Y522 | The declaration-order companion question is settled: the engine validates order and logs one error per violating link, but tolerates violations. | UNCHANGED | ENGINE | engine test | L1146-1147 |
| Y523 | Probe 1 is pass caching: for each of the three passes independently, does flipping a link crash, produce stale-but-running values, or rebuild cleanly, instrumented for staleness. | UNCHANGED | DESIGN | stipulated | L1149 |
| Y524 | Probe 2 is pass 2's content: what imposes its ordering, given that propagation is one hop and cannot chain. | UNCHANGED | DESIGN | stipulated | L1150 |
| Y525 | Probe 3 is write windows: where income accumulation sits relative to the value pass, and whether writing country trade income before month-boundary reconciliation makes AI budgeting and AI cash read the same figure. | UNCHANGED | DESIGN | stipulated | L1151 |
| Y526 | Probe 4 is negative link values: write one and observe arrow rendering and protect-trade allocation. | UNCHANGED | DESIGN | stipulated | L1152 |
| Y527 | Probe 5 is merchant storage: flip a link hosting a steering merchant and see whether the assignment dangles, resets, or crashes. | UNCHANGED | DESIGN | stipulated | L1153 |
| Y528 | Probe 6 is caravan, twice: does the engine grant it for a merchant assigned to a link that is incoming in `Φ_w`, and for one whose link carries no goods. | UNCHANGED | DESIGN | stipulated | L1154 |
| Y529 | Probe 7 is render data: is arrow render state separate from the economic link. | UNCHANGED | DESIGN | stipulated | L1155 |
| Y530 | Probe 8 is `TRADE_PROPAGATE_THRESHOLD` semantics: set it to 4 and check whether the raw requirement doubles. | UNCHANGED | DESIGN | stipulated | L1156 |
| Y531 | Probe 9 is diverted gold: does diverted colonial gold still appear in the per-province production income field, asserting the DLC flag agrees with the observed field. | UNCHANGED | DESIGN | stipulated | L1157 |
| Y532 | Probe 10 is caller enumeration: disassemble and list every call site of "is X downstream of Y", classified as return true, return true and define the scope, or compute per good, as a written artifact plus a companion "not members" list. | UNCHANGED | DESIGN | stipulated | L1158 |
| Y533 | Static string-table analysis already yields three named direction call sites — `DIPLO_SELLPROV_NOT_UPSTREAM`, `TREASURE_FLEET_TOOLTIP_CANT_REACH` and `TRADE_POWER_UPSTREAM` — both nation-pair gates compare trade capitals, and no colonisation refusal string exists. | UNCHANGED | INSTALL | read from a file (binary string table) | L1158 |
| Y534 | Probe 11 is the caravan recipient: place a merchant in a coastal node steering toward an inland one, read trade power in both nodes, and whichever jumps by `min(dev/3 + modifiers, 50)` is the recipient. | UNCHANGED | DESIGN | stipulated | L1159 |
| Y535 | The engine tooltip and the identifier `merchant_steering_to_inland` both read as the inland node, and if that holds §3.11's exposure surface inverts. | UNCHANGED | INSTALL | read from a file (tooltip string and identifier) | L1159 |
| Y536 | All writes land atomically at the tick hook with the sim paused. | UNCHANGED | DESIGN | stipulated | L1161 |

## §2.8 — Validation (L1163-1206)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y537 | Spice and cloves at 1444: source in Indonesia, with baseline DRAIN measured as spices sinking at Genoa (demand rank 1) plus branch-end termini (Australia, Brazil) and cloves at Venice, Kongo, Deccan, Australia and Brazil. | UNCHANGED | MODEL | numerical test | L1167 |
| Y538 | No Chinese node holds a spices sink in either configuration: under the §3.13 α-calibration `spices` sinks at Genoa alone and it is `cloves` that moves to Deccan, so the v1 expectation of simultaneous China+Europe spice sinks is not the baseline behaviour and is not recovered by the calibration either. | UNCHANGED | MODEL | numerical test | L1167 |
| Y539 | v2 said "China holds a spice sink only under the calibration", which its own parenthetical contradicted. | UNCHANGED | MODEL | read from a file (the prior spec version) | L1167 |
| Y152 | Sinks are `{selected ∩ flow-terminal} ∪ promoted`, 2 to 8 per good, and high-demand nodes are sinks at 19.8% among each good's top eight demanders (46 of 232) against 6.9% among its bottom eight (16 of 232) — a barbell whose lower arm is LP branch ends landing in poor pockets; the statistic is per-good deciles of nodes pooled over the 29 goods, not deciles of the pooled (good, node) pairs. | CHANGED | MODEL | numerical test | L1168 |
| Y540 | Malacca to Cape post-1500: spice routes Malacca to Cape to Europe. | UNCHANGED | MODEL | stipulated | L1169 |
| Y541 | Malacca to Cape pre-1500: the corridor is withheld by range and the power-at-both-ends gate, not by direction. | UNCHANGED | MODEL | stipulated | L1170 |
| Y542 | A 1000 AD start puts sinks in the Muslim world and Song China, with no era data. | UNCHANGED | MODEL | stipulated | L1171 |
| Y154 | Zeroing `hangzhou`-node development moves the `Φ_w` sinks from `{genua, hangzhou}` to `{genua, gulf_of_siam}`, with 30 of 159 edges flipping. | CHANGED | MODEL | numerical test | L1172 |
| Y155 | `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth 226.7 against 143.0 — ranks 12 and 39 of the 79 nodes holding counted provinces — and it holds the richest single province the model counts. | CHANGED | MODEL | numerical test | L1172 |
| Y156 | Zeroing `beijing` also moves the map — 8 flips — because deleting a percent of world wealth renormalises `c_w` everywhere; what separates the two is that `hangzhou` survives as a sink when `beijing` is zeroed and does not when `hangzhou` is. | CHANGED | MODEL | numerical test | L1172 |
| Y543 | v2 through v4.0 said zeroing `beijing` "moves nothing"; it does, and the asymmetry is which node keeps its end rather than whether the map moves. | UNCHANGED | MODEL | read from a file (the prior spec versions) | L1172 |
| Y153 | On the razed field the result is order-invariant like the baseline: 40 of 40 relabellings return `{genua, gulf_of_siam}` and `hangzhou` holds an end in none of them, so §2.3's tie-break removes the distinction v6.0 had to draw between this row and the baseline sink set. | CHANGED | MODEL | numerical test | L1172 |
| Y544 | Ming losing the Mandate moves nothing on the day it happens, because the Mandate is an owner property and §1.3 reads none, so the demand vector is unchanged and the pull collapses only as the consequences reach `base_tax` and `base_production`. | UNCHANGED | MODEL | algebraic derivation | L1173 |
| Y545 | That row is the owner-agnosticism check, not a responsiveness check. | UNCHANGED | DESIGN | stipulated | L1173 |
| Y546 | A major war in China shifts corridors for the duration, reverting as devastation heals. | UNCHANGED | MODEL | stipulated | L1174 |
| Y547 | Many poor provinces versus few rich: luxury demand goes to the rich-province node and bulk to the many-province node. | UNCHANGED | MODEL | stipulated | L1175 |
| Y548 | On a price crash α falls below 1 and regional sinks reappear. | UNCHANGED | MODEL | stipulated | L1176 |
| Y549 | Caribbean 1650: sugar production income makes it a sink for cloth, tools and wine. | UNCHANGED | MODEL | stipulated | L1177 |
| Y550 | Kilwa 1000: ivory income makes it a sink for Indian textiles. | UNCHANGED | MODEL | stipulated | L1178 |
| Y551 | A consuming leaf terminates the DAG of every good it consumes but does not produce. | UNCHANGED | MODEL | algebraic derivation | L1179 |
| Y552 | An inert merchant's goods take the even split as if the node were empty, while node-wide bonuses still apply. | UNCHANGED | MODEL | stipulated | L1180 |
| Y553 | A node sinking spice but not cloth collects spice fully and cloth at the ratio, with cloth's remainder pushed. | UNCHANGED | MODEL | stipulated | L1181 |
| Y554 | A near-balanced link may flip monthly, carries near-zero either way, and assignments survive. | UNCHANGED | MODEL | stipulated | L1182 |
| Y555 | A two-way Atlantic corridor has merchants at both ends on disjoint good sets, neither blocking the other. | UNCHANGED | MODEL | stipulated | L1183 |
| Y556 | Economy tab versus overlay: every displayed trade figure matches the per-good economy to the ducat, and this is a self-consistency check rather than a comparison against stock EU4. | UNCHANGED | DESIGN | stipulated | L1184 |
| Y557 | Stock trade values are not reproducible run to run: two identical vanilla 1444 Castile starts differ on 49 of 80 nodes by up to 8.96% over the five node fields `current`, `local_value`, `outgoing`, `total` and `retention`. | UNCHANGED | ENGINE | engine test | L1184 |
| Y558 | AI merchant placement is randomised at start, and it is the three power-dependent fields that inherit it: `retention` is identical on 80 of 80 nodes and `total` on 78 of 79, the exception `zambezi` drifting 0.012%. | UNCHANGED | ENGINE | engine test | L1184-1185 |
| Y559 | Any comparison against unmodded numbers needs a tolerance and a null run. | UNCHANGED | DESIGN | stipulated | L1185 |
| Y560 | Reachability is asserted every tick: 100% of every good's demand reachable from its supply, zero orphan sinks — an LP feasibility theorem whose failure means the implementation broke rather than the world. | UNCHANGED | MATH | algebraic derivation | L1186 |
| Y561 | Conservation is asserted every good every tick: Phase-4 sum of `unserved` equals sum of `stranded` to machine precision. | UNCHANGED | MATH | algebraic derivation | L1187 |
| Y562 | Determinism is asserted: re-running a tick reproduces the orientation bit-for-bit, and promotions and fallbacks are scheduler-invariant by monotone closure. | UNCHANGED | MODEL | algebraic derivation | L1188 |
| Y563 | Acyclicity is asserted on every per-good graph, on `Φ_w`, and on the emitted file's declaration order. | UNCHANGED | DESIGN | stipulated | L1189 |
| Y564 | Sink-set containment is a hard assertion every tick, unconditionally: every sink inside the 2-core lies in `{selected} ∪ {promoted} ∪ {fallbacks}`, the set the sweep actually maintains, because every other core node is handed an out-arc by the sweep, and a violation is an implementation bug. | UNCHANGED | MATH | algebraic derivation | L1190 |
| Y565 | Asserting containment in `{selected} ∪ {promoted}` alone would halt on T3, which is correct behaviour, so the fallback set is part of the assertion rather than an escape clause on it. | UNCHANGED | MODEL | algebraic derivation | L1190 |
| Y566 | Sink-set equality is monitored rather than asserted: it is measured exact on 1444 (29/29 goods, zero fallbacks) but is not a theorem, and T2 and T3 are the two ways it can fail while the algorithm behaves correctly; report an equality miss with the node and the good and halt only on a containment miss. | UNCHANGED | MODEL | numerical test plus algebraic derivation | L1190 |
| Y567 | Where Phase 0 acts the equality does not apply and is not asserted; the check on a peeled edge is the Phase-4 orientation rule, and a net-importing pendant leaf that ends a sink is expected behaviour (T1) rather than a violation. | UNCHANGED | MODEL | algebraic derivation | L1191 |
| Y568 | Colonization check: an observer run to 1600 sees New World colonization proceed at roughly vanilla pace. | UNCHANGED | MODEL | stipulated | L1192 |
| Y569 | AI convergence check: greedy assignment settles with damping rather than oscillating. | UNCHANGED | MODEL | stipulated | L1193 |
| Y570 | Latent-good check: while latent there is no graph, no value weight and no survival-table entry, and all three are acquired the month production begins; `Φ_w` is unaffected only while the good stays latent, and on activation the whole field moves — measured, repricing the 45 owned latent-coal provinces flips 16 of 159 `Φ_w` edges. | CHANGED | MODEL | numerical test (§1.5) | L1194 |
| Y571 | Cross-implementation check: the DLL and the reference implementation agree on orientation exactly for every save in the historical set — the primary end-to-end check, replacing v1's α = 1 identity. | UNCHANGED | DESIGN | stipulated | L1195 |
| Y572 | `Φ_w`-vs-realized sign disagreement is measured rather than asserted, weighted by trade value rather than link count, against a known static baseline — `Φ_w` agrees with the per-good graphs on 55.0% of edge-goods weighted by trade value and 55.2% unweighted — and is predicted to cluster at nodes with 3+ outgoing links and partial merchant coverage, thinning as coverage densifies. | CHANGED | MODEL | numerical test (§1.6) | L1199-1202 |
| Y573 | Flip behaviour is measured per decade in peace versus war, along with whether flips revert as occupation lifts. | UNCHANGED | MODEL | stipulated | L1203 |
| Y574 | Propagated-share change per node is measured on each flip alongside the trade-power/in-degree covariance, and this is what catches the §1.10 threshold mechanics flickering. | UNCHANGED | MODEL | stipulated | L1204 |
| Y575 | Total propagated power is not the quantity to watch: reorientation cannot change edge count, so the sum of in-degrees equals the edge count and is invariant, and only the covariance moves. | UNCHANGED | MATH | algebraic derivation | L1204 |
| Y576 | Income balance is measured on two metrics — total world collected income and its distribution across historical great powers — and distribution is the gating one. | UNCHANGED | DESIGN | stipulated | L1205 |

## §2.9 — Build order (L1207-1216)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y577 | The build is not phases but two tracks run in parallel. | UNCHANGED | DESIGN | stipulated | L1209 |
| Y578 | The solver track starts with the defines parser, because §2.3 makes every constant a runtime read, so the eligibility threshold, propagation share, off-home penalty, merchant bonuses and caravan terms are all downstream of it and cannot be written correctly before it exists. | UNCHANGED | DESIGN | algebraic derivation | L1211 |
| Y579 | Then the b-flow and sweep with their per-tick assertions (reachability, conservation, acyclicity, determinism, 2-core sink containment), the per-tick sink-set equality monitor, per-good eligibility, realized flows, the `Φ_w`-vs-realized disagreement measurement, the reachability census, and the flip-rate measurement. | UNCHANGED | DESIGN | stipulated | L1211-1212 |
| Y580 | The memory track is the §2.7 probe session, all ten items on one trace. | UNCHANGED | DESIGN | stipulated | L1214 |
| Y581 | Then: write §1.10's classified call-site list into the spec, gate income balance on both metrics, and decide the negative-link display policy against a measured number. | UNCHANGED | DESIGN | stipulated | L1216 |

## §3.1 — Goals (L1222-1230)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y582 | Goal 1, world responsiveness: trade direction follows the world's current state, never authored arrows, so a horde razing `hangzhou` moves the sink because the wealth moved. | UNCHANGED | DESIGN | stipulated | L1224 |
| Y583 | Goal 2, realism: commodities flow differently, and China is a silk source and a spice sink at once — impossible under one graph. | UNCHANGED | DESIGN | stipulated | L1225 |
| Y584 | Goal 3, preserve the feedback loop: sinks accumulate, fund development and reinforce, which is how mercantile hegemonies form. | UNCHANGED | DESIGN | stipulated | L1226 |
| Y585 | Goal 4, represent return flows: export regions historically imported manufactures, and vanilla cannot express this at all. | UNCHANGED | DESIGN | stipulated | L1227 |
| Y586 | Goal 5, route-aware direction: direction must reflect where a good can ultimately reach, not which neighbour is richer. | UNCHANGED | DESIGN | stipulated | L1228 |
| Y587 | Goal 6: zero authored data. | UNCHANGED | DESIGN | stipulated | L1229 |
| Y588 | Goal 7: the game's own numbers are the model's numbers, so anything reading trade income reads the real one. | UNCHANGED | DESIGN | stipulated | L1230 |

## §3.2 — Why a flow and a drainage sweep (L1232-1340)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y589 | Two families of orientation fail before this one: the first fails by theorem, the second by an exact rule whose consequence is measured, and v2 called both theorems, which overstates the second. | UNCHANGED | MODEL | algebraic derivation | L1234-1236 |
| Y590 | Local comparison is monotone: orienting each edge by comparing its endpoints — wealth, `s − c`, or any node ranking — means no path can dip through a low-value intermediary and rise again, and Malacca to Cape to Europe requires exactly that dip. | UNCHANGED | MATH | algebraic derivation | L1238-1241 |
| Y591 | Monotonicity killed v1's rank-orientation strawman and the tested `s − c` operator the same way: demand had to increase at every hop, so one sixth of world demand became unreachable and Genoa was crowned a cloves sink that cloves could not reach. | UNCHANGED | MODEL | numerical test | L1241-1243 |
| Y592 | Merchants cannot repair a wrong orientation — a merchant selects among existing outgoing arrows and cannot reverse one — so route-awareness has to live in the orientation. | UNCHANGED | ENGINE | algebraic derivation | L1243-1245 |
| Y593 | v1's Laplacian sink rule is exactly `(c − s)/deg > mean(neighbour φ) − min(neighbour φ)`, verified on every (good, node) pair. | UNCHANGED | MODEL | numerical test | L1247-1249 |
| Y594 | Because supply is sparse where demand is dense, that right-hand side is set by supply geography: spices are produced in 18 of 80 nodes and cloves in one, while every node with an owned province carries demand, so the neighbour spread that sets the threshold is a supply pattern almost everywhere. | UNCHANGED | MODEL | numerical test | L1249-1253 |
| Y595 | Under v1's Laplacian, sinks landed where the field was locally flat rather than where demand was: the highest-demand node in the game was never a spices sink, a node with literally zero demand outranked Genoa and Beijing, and deleting demand variation entirely left the sink unmoved. | UNCHANGED | MODEL | numerical test (cited to `../v1-laplacian/diagnosis.md`) | L1253-1256 |
| Y596 | v1 and v2 quantified the asymmetry as "supply contrast 10⁷ against demand contrast 10²–10³", but that ratio was `max(s)` over the ε floor of v1's regularizer, which §1.2 removes. | UNCHANGED | MODEL | algebraic derivation | L1256-1258 |
| Y157 | What the ratio metric cannot see is the thing the diagnosis rests on: sparsity — most nodes produce nothing at all of a given good (spices in 18 of 80 nodes, cloves in exactly one) — so `(c−s)/deg` is dominated by where supply exists, and a max/min ratio over producing nodes is blind to that by construction. | CHANGED | MODEL | algebraic derivation | L1258-1262 |
| Y158 | On the contrast metric itself the demand side is the wider one, not the supply side. | CHANGED | MODEL | numerical test; no figure and no script are given | L1262-1263 |
| Y597 | No parameter fixes the Laplacian's placement: an α strong enough to matter destroys §1.4's regime split. | UNCHANGED | MODEL | algebraic derivation | L1263-1264 |
| Y159 | Better wealth inputs move Genoa to a co-sink at roughly ×1.7 without making demand the determinant of placement. | CHANGED | MODEL | numerical test | L1264-1265 |
| Y160 | Moving the spice sink to a Chinese node takes a multiple of that node's wealth in the region of 3.6–4.8×, observed on the 1444 field: `beijing` 3.63×, `hangzhou` 4.13×, `xian` 4.61×, `canton` 4.78×. | CHANGED | MODEL | numerical test | L1265-1267 |
| Y161 | These are wealth multiples rather than demand multiples: because demand is `wealth^α` normalised over the world, the same move expressed in demand is a much larger factor. | NEW | MATH | algebraic derivation | L1267-1268 |
| Y162 | The four named Chinese nodes are not the cheapest — `girin` needs 3.89× and `yumen` 4.49×, both inside the range — so the claim is about the size of the intervention rather than which node is easiest to move. | CHANGED | MODEL | numerical test | L1268-1270 |
| Y598 | v2 wrote "1.7× where 4–5× is needed", which compressed two different quantities into one comparison and understated what better inputs could buy. | CHANGED | MODEL | algebraic derivation (v5 said "two different thresholds") | L1270-1271 |
| Y599 | The conservation lesson: operators that impose node balance somewhere (the v1 solve, a min-cost flow) serve 100% of demand as a theorem, and operators that do not (rank, seeded basins) strand it. | UNCHANGED | MATH | algebraic derivation | L1273-1275 |
| Y600 | DRAIN takes conservation from the b-flow — reachability is LP feasibility on a connected map rather than an aspiration — and takes sink placement out of field geometry entirely: sinks are the selected demand centres plus the flow-terminal drains any acyclic drainage orientation would be forced to have, plus pendant net-importers where Phase 0 acts. | UNCHANGED | MODEL | algebraic derivation | L1273-1279 |
| Y601 | Of the four claims, v1 did state aggregate acyclicity as C061 ("`Φ` is a potential, so orienting edges by it is acyclic") and its ε-machinery stated what decided dead-branch direction; what v1 genuinely never stated is the sink-placement determinant and any reachability guarantee. | UNCHANGED | MODEL | read from a file (the v1 spec and its claim inventory) | L1279-1282 |
| Y163 | Sink placement is a measurement on one input: on 1444, final sinks = `{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal demanders}`, measured exact 29/29 goods, and three constructed inputs break it. | CHANGED | MODEL | numerical test (`toys.py`) | L1284-1290 |
| Y164 | v5.0 tried to rescue that equality by attaching two conditions — Phase 0 a no-op and no fallback firing — and those conditions are necessary rather than sufficient, because T2 satisfies both and still breaks the equality, so the conditioned form is no more a theorem than the bare one. | NEW | MODEL | algebraic derivation | L1286-1289 |
| Y602 | T1, pendant importer: triangle A(+5), B(−3), D(0) with a leaf C(−2) on B; Phase 0 peels C, Phase 4 restores the edge B to C, and the actual sinks are {C} while the formula set is {B}, so the pendant is a sink outside the set and it also strips the selected sink of its sinkhood. | UNCHANGED | MODEL | numerical test (`toys.py`) | L1291-1293 |
| Y603 | T2, free-edge race inside the 2-core: a five-cycle S1(+3)–u1(−3)–w(0)–u2(−2)–S2(+2)–S1 with a chord w–S1, where both u1 and u2 are selected flow-terminal demanders; under the DEF-ascending key u2 pops first, w becomes ready via its free edge to u2 and pops before u1, so the free edge orients u1 to w and u1 is no longer a sink — actual {u2}, formula {u1, u2}. | UNCHANGED | MODEL | numerical test (`toys.py`) | L1294-1298 |
| Y604 | T3, the fallback branch inside the 2-core: triangle A, B, C with `b = 0` at all three and node wealth 3, 2, 1; Phase 1 selects nothing, every edge is free, the sweep stalls with no flow-terminal demander and the fallback promotes A, free edges orient B to A, C to A and C to B, so actual sinks are {A} while the formula set is empty and A is in neither {selected} nor {promoted}. | UNCHANGED | MODEL | numerical test (`toys.py`) | L1299-1303 |
| Y605 | What survives unconditionally is the subset direction within the 2-core over the set the sweep maintains: every core node that is neither selected, promoted nor fallback-promoted is given an out-arc by the sweep, either a flow arc or a free edge to an earlier-marked node. | UNCHANGED | MATH | algebraic derivation | L1305-1307 |
| Y606 | Pendant net-importers are the only sinks outside that set. | UNCHANGED | MATH | algebraic derivation | L1308 |
| Y607 | §2.8 therefore carries two runtime checks rather than one weakened one: containment inside the 2-core asserted unconditionally every tick against `{selected} ∪ {promoted} ∪ {fallbacks}`, and the equality monitored every tick with T2 and T3 named as its legitimate failures. | UNCHANGED | DESIGN | stipulated | L1308-1311 |
| Y608 | On pendant edges the Phase-4 orientation rule is the check and T1 is expected output. | UNCHANGED | DESIGN | stipulated | L1311-1312 |
| Y609 | Written as a single assertion with an escape clause, all three counterexamples would disappear into the clause, and written against the narrower containment set T3 would halt the solver on correct behaviour. | UNCHANGED | MODEL | algebraic derivation | L1312-1314 |
| Y610 | Free-edge direction is marking order under the (DEF asc, b asc, index) priority, deterministic by construction, while independence from the node indexing is measured rather than proved and holds where the key has no exact ties (zero exact ties on free edges, 29/29 goods on 1444) — with two cautions: the key reads the post-fold balance β so peeling can create ties the raw balances lack, and the indexing is load-bearing wherever the key ties, none of which fires on 1444 and none of which is why §2.4 requires a canonical node order, that requirement coming from Phase 2's LP under unit costs. | UNCHANGED | MODEL | numerical test | L1315-1326 |
| Y611 | Reachability: the orientation contains the LP certificate, so every unit of demand is servable — measured 100.0%, 29/29 goods, zero orphan sinks. | UNCHANGED | MATH | algebraic derivation plus numerical test | L1327-1328 |
| Y612 | Aggregate acyclicity: `Φ_w` is itself a DRAIN orientation, so it is acyclic by the same marking-order argument as every per-good graph, and the flow support by the cycle-cancelling argument. | UNCHANGED | MATH | algebraic derivation | L1329-1331 |
| Y613 | `Φ_w`'s marking order is a per-node scalar reproducing the DAG, for any consumer that needs a potential. | UNCHANGED | MODEL | algebraic derivation | L1331-1332 |
| Y614 | Conduits still work: a node with `s = c = 0` (the 1444 Cape exactly) carries flow through, with in- and out-degree both nonzero for all 29 goods. | UNCHANGED | MODEL | numerical test | L1334-1335 |
| Y615 | The corridor runs through the Cape, which is the short route to Atlantic Europe: Malacca reaches the Channel in 3 hops through the Cape against 7 through Alexandria, and the flow routes 24% of world spice supply through it, where v1's potential never used it at all. | UNCHANGED | MODEL | numerical test | L1335-1338 |
| Y616 | Peripheral termini still exist — the LP's branch ends are consumed at the end of the line — and value only arrives where someone holds power at both ends of the link. | UNCHANGED | MODEL | algebraic derivation | L1339-1340 |

## §3.3 — Why wealth, and why per province (L1342-1368)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y617 | Demand is purchasing power, and under §1.3 purchasing power is what the place is worth per year. | UNCHANGED | DESIGN | stipulated | L1344 |
| Y618 | Wealth captures return flows for free: a sugar island's production term is carried by its trade good rather than by its development, so it becomes a genuine consumer of cloth and tools. | UNCHANGED | MODEL | algebraic derivation | L1344 |
| Y619 | The return-flow effect is real but modest at vanilla prices: sugar (3.0), cocoa (4.0) and coffee (3.0) are 1.2–1.6× grain (2.5) rather than multiples, and the largest price ratios belong to cloves (8.0) and coal (10.0), neither of which is a Caribbean sugar island. | UNCHANGED | INSTALL | read from a file (the price table) | L1344 |
| Y620 | v1 and v2 said "negligible development but large production income", which overstated the gap. | UNCHANGED | MODEL | algebraic derivation | L1344 |
| Y621 | There is no colonial-nation dependency, no timeline restriction and no owner dependency. | UNCHANGED | MODEL | stipulated | L1344 |
| Y622 | Wealth is chosen for what the place is rather than who runs it: autonomy drift, national ideas, government reforms, estates and technology no longer move demand at all. | UNCHANGED | MODEL | stipulated | L1346 |
| Y623 | What remains still moves deliberately: development changes, trade goods change, prices move with events, and `trade_goods_size` modifiers on the place — devastation, occupation, siege, prosperity — still bite within months. | UNCHANGED | MODEL | algebraic derivation | L1346 |
| Y624 | A besieged province genuinely produces less, so that volatility is economics rather than noise, and a trade map that ignored a decade-long war would fail Goal 1. | UNCHANGED | DESIGN | stipulated | L1346 |
| Y625 | What the model removes is the volatility that was really about ownership: a province no longer changes what it demands on the day it is conquered. | UNCHANGED | MODEL | algebraic derivation | L1346 |
| Y626 | The instruction is to plan around the world rather than around the graph: the map is legible, not unchanging. | UNCHANGED | DESIGN | stipulated | L1346 |
| Y627 | Trade income is excluded for circularity rather than speed: including it would close a demand-orientation-flow-demand loop, making the graph respond to merchants' decisions rather than to the world. | UNCHANGED | MODEL | algebraic derivation | L1348 |
| Y628 | The loop still closes the long way: trade income funds development, and development raises tax and production income. | UNCHANGED | MODEL | algebraic derivation | L1348 |
| Y165 | `cape_of_good_hope`'s `members` list has 20 entries but province 1460 is a sea zone, listed in `map/default.map`'s `sea_starts`, so the node holds 19 land provinces. | NEW | INSTALL | read from a file | L1350-1352 |
| Y629 | Node sizes run from 19 land provinces (`cape_of_good_hope`) to 77 (`girin`) — a 4× spread with no structural rule behind it. | UNCHANGED | INSTALL | read from a file | L1350-1353 |
| Y630 | Raising a node's aggregate wealth to a power rewards node size, so luxuries would drain toward whichever node the map authors sliced coarsest. | UNCHANGED | MATH | algebraic derivation | L1354-1355 |
| Y631 | The distortion is measured against the per-province form the model defines rather than against equal totals: node-level α overweights a k-province node by `k^(α−1)` at fixed per-province wealth, so at α(g) = 1.5 — a per-good α, sugar's and coffee's — a 77-province node is favoured over a 19-province one by about 2× and Nippon (68) over `champagne` (33) by about 1.44×, while at the installed `α_Φ = 2.0` the exponent is 1 and the same two comparisons give 4.1× and 2.1×, so the slicing distortion is larger on the aggregate graph than on any per-good one. | CHANGED | MATH | algebraic derivation | L1355-1366 |
| Y632 | v2 said a 77-province node "beats a 19-province node of equal total wealth by 2×"; at equal totals the node-level form is count-blind and they tie, so the comparison that shows the distortion is against the per-province form. | UNCHANGED | MATH | algebraic derivation | L1363-1366 |
| Y633 | With the exponent inside the sum, superlinear demand concentrates where individual provinces are rich, and at α = 1 the per-province and node-aggregate forms coincide exactly. | UNCHANGED | MATH | algebraic derivation | L1366-1368 |

## §3.4 — Why supply is pre-modifier (L1370-1380)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y634 | Production efficiency does not conjure more cloves; it means the owner extracts more ducats from the same cloves, so letting it into supply would say a province ships more to the world market because its owner picked Trade ideas. | UNCHANGED | MODEL | algebraic derivation | L1372 |
| Y635 | Owner effects do not belong in demand either: v1 and v2 excluded them from supply and then let them back in through `wealth`, so the same incoherence they rejected on the supply side ran the demand side, and §1.3 now excludes them from both. | UNCHANGED | MODEL | algebraic derivation | L1374 |
| Y636 | Supply and demand are both properties of the place, so the supply-side argument applies unchanged and with more force to demand. | UNCHANGED | DESIGN | algebraic derivation | L1374 |
| Y637 | The aggregate uses trade value rather than production income because a province's trade value is unaffected by production efficiency or local autonomy while production income is defined by them, so substituting production income would make `V_g` depend on owners' idea groups and autonomy. | UNCHANGED | MODEL | algebraic derivation | L1376-1378 |
| Y166 | In v1 substituting production income also measurably broke the α = 1 identity, with orientation agreement collapsing to well under half the map. | CHANGED | MODEL | numerical test; no count is quoted | L1378-1380 |

## §3.5 — Why α is anchored absolutely (L1382-1431)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y638 | Anchoring at 2 ducats rather than the price median means a good's market concentration moves only when its own price moves, and `k` becomes a pure sensitivity knob that does not shift the neutral point. | UNCHANGED | MATH | algebraic derivation | L1384 |
| Y639 | Under a median anchor a good could concentrate because some unrelated commodity got expensive — noise dressed as economics. | UNCHANGED | MATH | algebraic derivation | L1384 |
| Y640 | At vanilla base prices nothing sits below the 2.0 anchor: the minimum tradeable base price is exactly 2.0, with fur, naval supplies, slaves, tea, tropical wood and livestock on the anchor at α = 1 exactly. | UNCHANGED | INSTALL | read from a file | L1386-1389 |
| Y641 | Grain is 2.5, not the 1.25 v1 recorded; both of v1's figures were price/P₀ misread as prices. | UNCHANGED | INSTALL | read from a file | L1388-1389 |
| Y642 | The sublinear regime is entered only when a price event pushes a good beneath the anchor, and the shipped data bounds how often that can happen: 13 of 30 goods can be pushed strictly below 2.0 by a single vanilla `change_price` event (grain and wine reach 0.625), two more (`gems` and `silk`) land exactly on 2.0, four have a negative event that does not reach 2.0, and 11 goods have no negative price event at all. | UNCHANGED | INSTALL | read from a file | L1389-1394 |
| Y167 | `change_price` values are fractions of the good's base price rather than ducats, and the shipped save `tutorial/eu4_tutorial_chapter10.eu4` settles it: `paper` sits at `current_price=4.375` on a base of 3.5 (×1.25, not +0.25) and `gems` at 5.000 on a base of 4.0, so a −0.25 key takes a 2.5 good to 1.875 and grain and wine reach 0.625. | NEW | INSTALL | read from a file (a shipped save) | L1395-1399 |
| Y168 | The install carries 161 textual `change_price` blocks — 93 in `events/`, 14 in `missions/`, 1 in `common/`, 53 in `history/` of which 13 are negative (all in `history/countries/HAB - Austria.txt`), and none in `decisions/`. | CHANGED | INSTALL | read from a file | L1401-1403 |
| Y169 | Ten of the 161 never execute — four inside `effect_tooltip = "…"` strings, three inside the `effect = "…"` string of a `country_event_with_effect_insight`, and three inside `tooltip = { }` display wrappers — so 151 are executable. | NEW | INSTALL | read from a file | L1403-1406 |
| Y170 | Six of the seven quoted blocks duplicate a block already counted in `events/` and the seventh names a price key no event in the install ever sets; all ten are positive and every negative block in the install is executable, so the partition is identical under either census. | NEW | INSTALL | read from a file | L1406-1409 |
| Y171 | v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them; both were wrong about which number was the executable one. | CHANGED | MODEL | read from a file (the prior spec versions) | L1409-1410 |
| Y172 | v5.0 claimed the scan was "guarded by a per-file count assertion", and there was no assertion anywhere in its toolchain. | CHANGED | MODEL | read from a file (v5.0's toolchain) | L1410-1412 |
| Y173 | `verify6.py` checks the census only by requiring the printed total to match a computed one rather than by reconciling per file, and `measure6.py`'s walker still swallows parse failures in a bare `except`. | NEW | MODEL | read from a file (the harness scripts) | L1412-1414 |
| Y174 | The reason a plain parse misses the quoted blocks is mechanical: `pdx.py` tokenises a quoted string as one opaque unit, so a `change_price` inside a tooltip string is invisible to the walker. | NEW | MODEL | read from a file (`pdx.py`) | L1414-1416 |
| Y643 | The history route matters: `wool`'s largest single negative is `NEW_DRAPERIES` at −0.25 in the history file, against the −0.20 the same key carries in `events/PriceChanges.txt`, and `change_price` entries are keyed. | UNCHANGED | INSTALL | read from a file | L1418-1419 |
| Y175 | 1.875 is the single-key floor rather than the campaign figure: the same `1540.1.1` block also applies `COTTON_IMPORTS = -0.10` to `wool`, so a campaign that runs it holds two live negative keys and wool sits at 1.625 if keyed changes sum or 1.6875 if they compound — and nothing in the install settles which, because no readable save carries a good with two live keys. | CHANGED | INSTALL | read from a file | L1420-1423 |
| Y176 | The partition needs the history value: `events/PriceChanges.txt`'s −0.20 for the same key would alone floor wool at 2.00, and events alone give 12/3/4/11 rather than 13/2/4/11. | NEW | INSTALL | read from a file | L1423-1426 |
| Y644 | v2's 13 was right, and v3.0 reached 12 by parsing four of the five trees. | UNCHANGED | MODEL | read from a file (the prior spec versions) | L1426-1427 |
| Y645 | The point of having the sublinear regime is that without it a crash could only fail to concentrate a market, never actively spread it, and whether it engages often enough to earn its keep is now a bounded question rather than an open one. | UNCHANGED | DESIGN | stipulated | L1427-1429 |
| Y646 | α is deliberately mild: production geography is what differentiates goods and α expresses only how concentrated a market is, because a mechanism strong enough to reshape orientation would let price fight geography for control of the graph. | UNCHANGED | DESIGN | stipulated | L1431 |

## §3.6 — Why no hysteresis, and why there is no ε (L1433-1470)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y647 | A margin on orientation is a correctness bug rather than a tuning knob: holding an edge against the current month's result splices orientations decided at different times, and a splice of two acyclic orientations need not be acyclic. | UNCHANGED | MATH | algebraic derivation | L1435-1437 |
| Y648 | Tested in v1: with tol = 1e-3 and values {0, 0.0006, 0.0012}, tolerance-based tie-breaking turned an acyclic prior into A → B → C → A. | UNCHANGED | MODEL | numerical test | L1437-1438 |
| Y649 | The node-file format represents cycles perfectly well — it is a list of named directed links with no acyclicity constraint — which corrects how v1 stated the stakes. | UNCHANGED | INSTALL | read from a file | L1439-1440 |
| Y650 | What the design depends on is the engine's behaviour on a cyclic file, and that is now measured rather than assumed: the engine dies. | UNCHANGED | ENGINE | engine test | L1440-1442 |
| Y651 | A hand-authored two-node cycle produced `EXCEPTION_STACK_OVERFLOW` at a single exception address under 1002 recorded `eu4.exe` frames, reproduced on three launches, while vanilla and a file with all 159 links declared backwards both loaded and played. | UNCHANGED | ENGINE | engine test | L1442-1444 |
| Y652 | The engine walks the node graph recursively and a cycle never terminates. | UNCHANGED | ENGINE | algebraic derivation from the crash observation | L1444-1445 |
| Y653 | Acyclicity is enforced because the engine provably cannot survive its absence, not — as v2 had it — because we could not prove that it could. | UNCHANGED | DESIGN | engine test | L1445-1446 |
| Y654 | Nothing needs to stop churn: a link whose flow-support membership alternates month to month carries near-nothing either way on the evidence available, and merchant assignments are to links so they survive flips untouched. | UNCHANGED | MODEL | numerical test | L1448-1450 |
| Y655 | The "carries near-nothing" half is measured rather than derived, because v1's continuity argument (a near-flat potential implies near-zero flow) does not port to an LP support, which is a discrete selection. | UNCHANGED | MATH | algebraic derivation | L1450-1452 |
| Y656 | Measured on 1444: across 29 goods × 6 random 1e-9 demand nudges, zero support-membership changes moved more than 1e-6 of flow, and under ±1% wealth noise on six seeds the aggregate map moved no edge at all. | CHANGED | MODEL | numerical test | L1452-1454 |
| Y657 | At exactly degenerate inputs — two equal-hop corridors — the map from `b` to the chosen support is discontinuous in principle, and §2.3's tie-break narrows where that bites: on the aggregate graph it leaves the optimum unique so the result no longer rests on the solver's tie-selection, while on the per-good graphs it still does, and that is the premise §3.13 tracks for multiplayer. | CHANGED | MATH | algebraic derivation | L1454-1458 |
| Y658 | v1's ε is deleted because the problem it patched no longer exists: the Laplacian oriented dead branches by comparing solved potentials that were mathematically equal and differed only by floating-point residual, so orientation varied by machine and a field-level regularizer was needed to break ties on purpose. | UNCHANGED | MODEL | algebraic derivation | L1460-1463 |
| Y659 | DRAIN's free edges are oriented combinatorially: the priority sweep's key (DEF, b, index) is computed from input data over the LP's support structure — its values come from the inputs, though which nodes are downstream comes from the solve. | UNCHANGED | MODEL | algebraic derivation | L1463-1466 |
| Y660 | The measured count of exact key ties on 1444 data is zero, and the LP itself is deterministic (six identical solves, one orientation). | UNCHANGED | MODEL | numerical test | L1466-1468 |
| Y661 | Determinism is asserted per tick rather than approximated by a nudge. | UNCHANGED | DESIGN | stipulated | L1468 |
| Y662 | What replaces the ε-magnitude question in §3.13 is the cross-machine question: the LP must pivot identically on identical input for multiplayer. | UNCHANGED | DESIGN | stipulated | L1469-1470 |

## §3.7 — Why eligibility is per good (L1472-1478)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y663 | Vanilla's rule is that effective trade power counts only countries which collect or transfer downstream, and not those whose trade capital is upstream, so power in a node not upstream of anywhere you collect is inert — neither retaining nor transferring. | UNCHANGED | ENGINE | stipulated | L1474 |
| Y664 | Under a per-good model "downstream" is per good, so at a node where your home is downstream for cloth and upstream for spice your power counts for one and not the other. | UNCHANGED | MODEL | algebraic derivation | L1476 |
| Y665 | Per-good eligibility returns true for some goods at every node, so no nation is ever globally inert, while still preventing a nation's power from shoving a good away from where it collects that good. | UNCHANGED | MODEL | algebraic derivation | L1476 |
| Y666 | Forcing eligibility true for all goods at once would be "direction doesn't exist" rather than "everyone is upstream and downstream", which inflates transfer power everywhere. | UNCHANGED | MODEL | algebraic derivation | L1476 |
| Y667 | The common misstatement — that any non-collecting country with trade power is transferring — is the loose community summary and is wrong. | UNCHANGED | ENGINE | stipulated | L1478 |

## §3.8 — Why gates evaluate true (L1480-1498)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y668 | The vanilla gates encode an assumption that a nation pair has one global relationship to trade, upstream or downstream, and under thirty graphs that assumption is not inconvenient but false. | UNCHANGED | MODEL | algebraic derivation | L1482 |
| Y669 | Every province is upstream for some good, because a region that receives your cloth ships you its furs. | UNCHANGED | MODEL | algebraic derivation | L1482 |
| Y670 | There is no fact of the matter for the gate to test, so the honest fix is to stop consulting it rather than to engineer the graph so it happens to pass. | UNCHANGED | DESIGN | stipulated | L1482 |
| Y671 | Node-pair dependencies are different and keep reading `Φ_w`, because propagation is a relation between two nodes rather than two nations, and setting it true would grant every country propagated power into every neighbour and multiply trade power across the map. | UNCHANGED | MODEL | algebraic derivation | L1484 |
| Y672 | That distinction is easy to miss and expensive to get wrong. | UNCHANGED | DESIGN | stipulated | L1484 |
| Y673 | Propagate Religion is node-local — it establishes a centre of conversion in the node's own province — but v1's "gated on a trade-power threshold there and nothing else" was wrong, and it was one of only three claims carrying `verified (method unstated)` provenance. | UNCHANGED | INSTALL | read from a file | L1486-1489 |
| Y674 | The shipped policy file gates Propagate Religion on the trade share and the node being in a trade company region and a merchant present and a religion-group/flag disjunction and `dominant_religion`, with `unique = yes` per node. | UNCHANGED | INSTALL | read from a file | L1489-1491 |
| Y675 | No trading policy anywhere in `00_trading_policies.txt` tests upstream/downstream. | UNCHANGED | INSTALL | read from a file | L1491-1493 |
| Y676 | Three of the five trading policies have no trade-share threshold at all — merchant-present only. | UNCHANGED | INSTALL | read from a file | L1493-1494 |
| Y677 | This is written down because the deferred artifact does not exist yet, and a community restatement of the "downstream target" claim would otherwise put direction tests back. | UNCHANGED | DESIGN | stipulated | L1494-1496 |
| Y678 | Scopes read `Φ_w` rather than any-good reachability, because a gate is a boolean while a scope is a set or a path, and answering a scope question with any-good reachability is an enormous buff. | UNCHANGED | DESIGN | algebraic derivation | L1498 |
| Y679 | `Φ_w` is the graph the engine already walks, so those call sites are left alone, which collapses the shared-predicate risk. | UNCHANGED | ENGINE | algebraic derivation | L1498 |
| Y680 | Reading `Φ_w` for scopes is legible — one map predicts where fleets sail — and balanced, because area-effect mechanics scoped by any-good reachability would cover most of the map. | UNCHANGED | DESIGN | stipulated | L1498 |
| Y681 | Any-good connectivity on 1444 data under DRAIN is 90.5% (5,721 of 6,320) of ordered node pairs, and v2's 98.8% is v1's Laplacian figure, 6245/6320, carried across the operator change without being re-measured — the argument is unaffected because the current figure is still most of the map. | CHANGED | MODEL | numerical test | L1498 |

## §3.9 — Why `Φ_w` is the installed graph (L1500-1548)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y682 | The installed graph exists for the engine's direction-dependent systems — propagation, fleet routes, upstream/downstream scopes — and those systems model power rather than commodity logistics. | UNCHANGED | DESIGN | stipulated | L1502-1503 |
| Y683 | What vanilla's authored arrows encode is empires pointing at the biggest cities and richest areas, with three authored ends (`genua`, `venice`, `english_channel`). | UNCHANGED | INSTALL | read from a file | L1503-1505 |
| Y177 | On this field `english_channel` is the richest node at 316.6 and is not a sink — it drains to `genua`, 4th at 296.0 — while `mexico` (300.4, 2nd), `gulf_of_siam` (297.9, 3rd) and `sevilla` (266.5, 7th) are likewise net demanders. | CHANGED | MODEL | numerical test | L1506-1509 |
| Y684 | A rich non-sink node draws more edges in than it sends out as a net demander, even though flow passes through. | UNCHANGED | MODEL | algebraic derivation | L1508-1510 |
| Y685 | Wealth pulls but the wealthiest node is not automatically an end: what makes an end is where the flow terminates, a property of the whole field and the graph rather than of a single node's rank, and the ends emerge and move when the wealth moves — a razed `hangzhou`, a dev-stacked capital, a colonizing Europe that flips the Cape. | CHANGED | MODEL | algebraic derivation | L1506-1513 |
| Y686 | `Φ_w` reuses the §1.1 operator unchanged: one implementation, one set of guarantees (LP feasibility, acyclicity, determinism, scan-invariance), and the correctness check stays a single combinatorial comparison. | UNCHANGED | DESIGN | stipulated | L1513-1516 |
| Y687 | Three aggregates were tested; one is impossible and one was superseded. | UNCHANGED | MODEL | stipulated | L1518 |
| Y688 | The value-weighted net flow (the sum over goods of `V_g · net_g`) is a flow, flows circulate, and it measurably contains directed cycles, so it cannot be installed. | UNCHANGED | MODEL | numerical test | L1520-1521 |
| Y689 | The value-weighted marking order `Φ_ord` is acyclic for free and scores higher than `Φ_w` on self-coherence with the per-good graphs, which is the cost of the trade and is not disputed. | UNCHANGED | MATH | algebraic derivation | L1522-1524 |
| Y178 | `Φ_ord`'s ends are artifacts of sweep scheduling rather than places, and the sharpest evidence is what relabelling does to them: its end count and end set both move with the node order, where `Φ_w`'s do not. | CHANGED | MODEL | numerical test (§2.4 item 1) | L1523-1527 |
| Y179 | Most of `Φ_ord`'s ends terminate no good, none of the demand capitals is among them, and its end count does not concentrate as demand concentrates. | CHANGED | MODEL | algebraic derivation; no figure is carried | L1527-1529 |
| Y180 | No figure is quoted for any of that: the operator is not installed, its numbers moved with every change to the wealth field, three successive audits spent their effort recounting them, and the design argument depends on none of them. | NEW | DESIGN | stipulated | L1529-1531 |
| Y690 | `Φ_w` is adopted for one operator, one set of guarantees, and ends that move with the world: reusing §1.1 unchanged gives LP feasibility, acyclicity, determinism and scan-invariance for free, and its ends are places the wealth actually is. | UNCHANGED | DESIGN | stipulated | L1532-1535 |
| Y181 | v2.1 through v4.0's "two vanilla-like ends at 1444" justification is withdrawn and must not be revived even though the 1444 field again gives two ends, because the count is a property of the field rather than of the operator and pinning the operator to it would be the calibration §2.3 withdrew. | CHANGED | MODEL | algebraic derivation | L1535-1539 |
| Y182 | What the trade costs is self-coherence with the per-good graphs, which the superseded marking-order aggregate scores higher on; what it buys is one operator, one set of guarantees, and ends that sit where the wealth is. | CHANGED | DESIGN | stipulated; no point gap is quoted | L1539-1541 |
| Y691 | A difference in `Φ_w` across a link is not the net value crossing it. | UNCHANGED | MODEL | algebraic derivation | L1543-1544 |
| Y692 | Realized movement follows vanilla propagation — a good can be diluted by an even split across three links while another gets winner-take-all steered the other way — so a link can be oriented n to m under `Φ_w` while realized net flow runs m to n. | UNCHANGED | MODEL | algebraic derivation | L1544-1546 |
| Y693 | That is why the disagreement rate is measured rather than assumed, and why display policy for negative link values is a decision deferred to data. | UNCHANGED | DESIGN | stipulated | L1546-1548 |
| Y694 | Link values are realized flows, which makes conservation hold by construction. | UNCHANGED | MATH | algebraic derivation | L1548 |

## §3.10 — Why the engine's economy is overwritten (L1550-1567)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y695 | Paying countries correctly while leaving the display wrong is a strictly weaker position: node values, pie charts and the ledger would describe an economy nobody is playing, and AI light-ship building, trade-league behaviour, peace valuation and income-threshold events all read those figures. | UNCHANGED | ENGINE | algebraic derivation | L1552 |
| Y696 | The engine's data model is sufficient at node level for a narrower reason than it first appears: `collect_pool` is per good on the inside, since `collected_share(n,g)` depends on `P_transfer(g)` and §1.8 makes transfer eligibility commodity-specific. | UNCHANGED | MODEL | algebraic derivation | L1554 |
| Y697 | What factors out is `powershare_C`, a country's share among collectors, and whether a country collects is a merchant-or-home property with no good dependence, so a good-independent share multiplying a per-good sum collapses to one scalar. | UNCHANGED | MATH | algebraic derivation | L1554 |
| Y698 | `income_C(n)` = the sum over goods of `value_g(n) · collected_share(n,g) · powershare_C(n)` = `powershare_C(n) · collect_pool(n)`. | UNCHANGED | MATH | algebraic derivation | L1557-1558 |
| Y699 | That is an identity rather than a measurement: `powershare_C(n)` carries no `g`, so it factors out of the sum, and by §1.1's vocabulary the property is true by construction and carries no measurement. | UNCHANGED | MATH | algebraic derivation | L1561 |
| Y700 | Every term that feeds a collector's power at a node is node-wide — the merchant bonus, the off-home penalty, propagation off the one installed graph, the caravan grant — so none of them can reintroduce a `g`. | UNCHANGED | MODEL | algebraic derivation | L1561 |
| Y183 | Across Sevilla, Genoa, Champagne, Malacca and the Gulf of Siam, using each node's real 1444 country table, the two forms agree to a worst relative disagreement of 0 to 3.7e-16 — one to three units in the last place. | CHANGED | MODEL | numerical test | L1561 |
| Y701 | One scalar per node reproduces every country's income exactly, and the engine's own math does the rest. | UNCHANGED | MATH | algebraic derivation | L1561 |
| Y702 | v1 through v4.0 quoted "agreement to 5.7e-14" here and 1.4e-14 below; both are floating-point residuals of an exact identity, produced by constructions none of those documents states — a theorem decorated with an experiment. | UNCHANGED | MODEL | read from a file (the prior spec versions) | L1561 |
| Y184 | Propagation is kept on a single graph, and the reason is not the one v1 through v6.0's own first draft gave. | NEW | DESIGN | algebraic derivation | L1563 |
| Y185 | Reading the one installed graph leaves the propagated term good-independent, so the identity holds by construction and in doubles to within one to three units in the last place. | CHANGED | MODEL | numerical test | L1563 |
| Y186 | `gulf_of_siam`'s 29 goods leave it by seven distinct downstream sets. | CHANGED | MODEL | numerical test | L1563 |
| Y187 | Per-good propagation does not break the income identity: defining `ps̄_C` as the per-good shares weighted by collected value, `collect_pool · ps̄_C = income_C` follows algebraically with the shares summing to 1, so `ps̄_C` is a legal share vector and one scalar per node still reproduces every collector's income exactly. | CHANGED | MATH | algebraic derivation | L1563 |
| Y188 | Both inputs to `ps̄_C` already exist per good at write time, and §2.6 sums exactly them into `collect_pool`. | NEW | MODEL | algebraic derivation | L1563 |
| Y189 | The real cost is that `ps̄_C` is not derivable from trade power alone: it is value-weighted, so installing it means writing a country a fictitious per-node trade power whose ratio happens to equal it, and every other consumer of that power field then reads the fiction. | NEW | MODEL | algebraic derivation | L1565 |
| Y190 | That is a claim about what the engine exposes rather than about a magnitude, and it is why the single graph stays: on one graph the scalar is the country's power share, needing no invention. | NEW | DESIGN | algebraic derivation | L1565 |
| Y191 | Every magnitude previous versions quoted here — v1 through v3.0's "off by 5.96 ducats on a node paying ~250" (where no node in the model has local trade value near 250, and which v4.0 deleted with its own harness asserting the deletion), v4.0's 0.41%, v5.0's "redistributive and single-digit percent", and v6.0's first draft's "at most 0.1%" — froze or reweighted the share differently, so each measured its own construction. | CHANGED | MODEL | read from a file (the prior spec versions) | L1565 |
| Y192 | No figure of the author's own is quoted here, because the identity holds and the objection is structural, and the size of any discrepancy depends on which collectors are taken to be collecting, which is a choice of the construction. | CHANGED | DESIGN | stipulated | L1565 |
| Y703 | Only the decomposition by good exceeds what the engine can hold. | UNCHANGED | ENGINE | algebraic derivation | L1567 |

## §3.11 — Why caravan power needs a condition added (L1569-1590)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y704 | In vanilla, steering is outgoing-only: trade cannot be steered upstream at any amount of power, per the engine's own hint "You can never steer trade upstream or past your Main Trade City". | UNCHANGED | INSTALL | read from a file (a named hint string) | L1571-1572 |
| Y705 | The display is not outgoing-only: the node window already lists incoming links as clickable entries. | UNCHANGED | INSTALL | read from a file | L1573 |
| Y706 | Because only outgoing links can be steered, "assigned" and "steering" are the same condition in vanilla and the engine never had to distinguish them. | UNCHANGED | ENGINE | algebraic derivation | L1574-1575 |
| Y707 | §1.7 makes incoming entries assignable and pulls "assigned" and "steering" apart. | UNCHANGED | DESIGN | stipulated | L1577 |
| Y708 | The engine's caravan grant fires on `merchant_present_inland` or `merchant_steering_to_inland`, with nothing checking whether value moves. | UNCHANGED | INSTALL | read from a file | L1577-1579 |
| Y709 | The caravan tooltip reads as granting the bonus in the inland node ("steers towards an inland trade node will give you extra trade power in that node"), the opposite of v1's reading that steering from Crimea to Kiev pays out in Crimea. | UNCHANGED | INSTALL | read from a file (a tooltip string) | L1579-1581 |
| Y710 | §2.7 item 11 settles the recipient with one merchant and two node windows, and the exposure surface is either the roughly 26 inland nodes themselves (tooltip reading) or every node adjacent to one (v1 reading), smaller and differently shaped under the first. | UNCHANGED | DESIGN | stipulated | L1581-1584 |
| Y711 | §1.7's added condition is the right guard under both readings. | UNCHANGED | DESIGN | stipulated | L1584 |
| Y712 | Caravan power is total country development divided by 3 plus policy and idea modifiers, clamped to [2, 50]. | UNCHANGED | INSTALL | read from a file | L1584-1585 |
| Y713 | Nineteen countries are at the caravan cap from raw 1444 development alone, and Burgundy, Korea, the Timurids and Portugal start 2–10% short and reach it with any caravan modifier. | UNCHANGED | MODEL | numerical test | L1585-1587 |
| Y714 | Caravan power does not scale with node presence at all. | UNCHANGED | ENGINE | algebraic derivation | L1587 |
| Y715 | Requiring the merchant to steer something restores the vanilla state of affairs, and granting on bare assignment would be the deviation — an unintended one. | UNCHANGED | DESIGN | stipulated | L1589-1590 |

## §3.12 — Why treasure fleets are always granted (L1592-1605)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y716 | The argument is consistency with §3.8: the gate compares two trade capitals on a graph where the nation-pair relation has no single truth value, so it is not consulted. | UNCHANGED | DESIGN | algebraic derivation | L1594-1595 |
| Y717 | v1 claimed a stronger argument — that the gate is bistable, denial raising the colonial node's wealth and granting lowering it, locking campaigns into whichever state they started in. | UNCHANGED | MODEL | read from a file (the v1 spec) | L1595-1597 |
| Y718 | That bistability argument is deleted: gold income never enters `wealth` at all, so neither granting nor denial moves the demand vector and there is no direct feedback to be bistable. | UNCHANGED | MODEL | algebraic derivation | L1597-1599 |
| Y719 | The engine's own denial branch confirms what denial does: "They will keep their gold income instead." | UNCHANGED | INSTALL | read from a file (a named string) | L1599-1600 |
| Y720 | A slow second-order version survives — kept gold spent on development raises `base_tax` and `base_production` years later — but a multi-year indirect loop is not a bifurcation and does not carry the design decision, so consistency carries it alone. | UNCHANGED | DESIGN | algebraic derivation | L1600-1603 |
| Y721 | Inflation scales with money received relative to economy size, so universal granting hits small previously-cut-off colonizers hardest. | UNCHANGED | ENGINE | algebraic derivation | L1605 |
| Y722 | The route rule is a balance dial, since privateers skim per node passed, which is why hop counts are compared between candidate rules on the mod's own graph rather than against vanilla's — that being a counterfactual on a graph the mod has replaced. | UNCHANGED | DESIGN | stipulated | L1605 |

## §3.13 — Open questions (L1607-1666)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y723 | Prose-sourced questions are to be distrusted and nothing built on them. | UNCHANGED | DESIGN | stipulated | L1609 |
| Y724 | Colonization's gate shape rests on one mod author's report, contradicted in-thread, and the observed behaviour needs no gate at all: if colonial nodes route away from the AI's home, expected trade income collapses and low-scoring provinces do not get colonized. | UNCHANGED | MODEL | unsourced beyond a contradicted forum report, as the document itself states | L1611 |
| Y725 | Static string-table analysis leans the same way: the only direction-refusal strings in the binary belong to sell-province and treasure fleets, none to colonisation. | UNCHANGED | INSTALL | read from a file (binary string table) | L1611 |
| Y726 | The caller enumeration must be able to return "no colonization gate exists" as a successful result. | UNCHANGED | DESIGN | stipulated | L1611 |
| Y727 | Derived questions are probably right and cheaply falsifiable. | UNCHANGED | DESIGN | stipulated | L1613 |
| Y728 | The `TRADE_PROPAGATE_THRESHOLD` file value and the documented raw requirement differ by exactly the propagation divider, which reconciles if the threshold is expressed in propagated units, and it is falsifiable by doubling the define. | UNCHANGED | INSTALL | read from a file plus algebraic derivation | L1615 |
| Y729 | Propagation is one hop and cannot chain, so something else in pass 2 imposes its ordering; eligibility resolution is a backward reachability from collection points and is the only candidate named — an argument from exhaustion, which §2.7 probe 2 settles. | UNCHANGED | ENGINE | algebraic derivation | L1616 |
| Y730 | The debugger-only list is shorter than v1 believed: of §2.7, only pass caching, pass-2 content, write windows and the caller enumeration truly need the debugger. | UNCHANGED | DESIGN | algebraic derivation | L1618-1620 |
| Y731 | Items 11–15 need a save, a tooltip, or one file edit, and the propagation-threshold and one-hop questions are node-window reads. | UNCHANGED | DESIGN | algebraic derivation | L1619-1620 |
| Y732 | Three of the cheap probes — caravan recipient, cyclic file, incoming-link button — change what this spec says. | UNCHANGED | DESIGN | stipulated | L1621-1622 |
| Y733 | One question is open in the v6.0 wealth model, and it is a question rather than a number, because §1.3 carries no value for it; two others that v3.0 listed here are settled and have moved into §1.3. | CHANGED | DESIGN | stipulated | L1624-1625 |
| Y193 | The one open wealth question is now a design question rather than a classification one: should any source beyond province condition be allowed to multiply `goods_produced`? | CHANGED | DESIGN | stipulated | L1627-1630 |
| Y195 | The keys `trade_goods_size` and `trade_goods_size_modifier` are granted in many places: buildings, event modifiers, great projects, static and province-triggered modifiers, holy orders, state edicts and trade-company investments. | CHANGED | INSTALL | read from a file | L1630-1633 |
| Y194 | v3.0 through v5.0 tried to admit the province-scoped subset by rule, and that rule was wrong in both independent audits that examined it, which is why v6.0 drops it. | CHANGED | MODEL | read from a file (the prior validations) | L1633-1635 |
| Y196 | Re-admitting any of those sources re-admits the maintenance burden with it, and the question to settle first is whether the fidelity is worth it — on the 1444 start the whole set was worth 105.30 ducats, about one percent of world wealth either way the ratio is taken. | NEW | DESIGN | algebraic derivation over the §1.3 figure | L1635-1638 |
| Y734 | Settled and moved: `local_production_efficiency` from a trade good is outside wealth, because Barcelona's production tooltip reads `Production Efficiency: +12.0% / From Technology: +2.0% / Producing Glass: +10.0%`, so the engine books glass's +10% on production income, which wealth does not compute. | UNCHANGED | ENGINE | measured in-game | L1640-1643 |
| Y735 | Settled and moved: `TAX_COEFF` is 1.0 across the development range — `Base: 0.49 (Yearly 6.00)` at `base_tax` 6 and `Base: 0.16 (Yearly 2.00)` at `base_tax` 2 — with `GP_COEFF` linear at four levels. | UNCHANGED | ENGINE | measured in-game | L1643-1645 |
| Y736 | `k`, `α_min` and `α_max` remain unresolved; the test is whether they produce the intended three-regime split, not whether they differentiate same-geography goods, which they are not meant to do. | UNCHANGED | DESIGN | stipulated | L1649 |
| Y737 | The zero-flow tolerance is scale-coupled: §2.3 records it as absolute rather than purely numerical (v2.1 filed it as numerical-only), and being absolute is what makes it interact with the magnitude of `b`; either normalise `b` before the solve or make the tolerance relative — undecided. | UNCHANGED | MODEL | algebraic derivation | L1650 |
| Y738 | Whether `α_min` ever bites is now bounded from files: the sublinear regime is reachable through vanilla price events for 13 of 30 goods, unreachable for 11, and exactly on the boundary for 2, and whether those events fire often enough in a real campaign remains the open half. | UNCHANGED | INSTALL | read from a file | L1651-1653 |
| Y739 | A measured calibration exists that makes sink counts track price — span exactly 1..5, spearman(price, sinks) = −0.20 — with α unclamped at exponent 2 (cloves α = 16), demand-mass quantile ρ = 0.5, and twig tolerance 3e-4. | UNCHANGED | MODEL | numerical test (cited to `drain-orientation.md` §5-6) | L1654-1656 |
| Y740 | Unclamped α-squared is a demand-model decision, because luxuries become court goods. | UNCHANGED | DESIGN | algebraic derivation | L1656-1658 |
| Y197 | Under the calibration's α = 16 the cloves demand order is `hangzhou`, `beijing`, `doab`, and the sink lands on a high-demand node rather than a geographic accident. | CHANGED | MODEL | numerical test | L1658-1659 |
| Y198 | v2 said Beijing "holds the richest single province", which it does not — that is `hangzhou` — and no province-wealth figures are quoted. | CHANGED | MODEL | numerical test | L1659-1660 |
| Y741 | The calibration's twig tolerance re-routes arcs individually carrying under 0.03% of world supply — up to about 0.18% of a good's mass in total rather than under 0.03% — and drops `cloves` to 99.97% reach, and it is one-snapshot tuning. | UNCHANGED | MODEL | numerical test | L1660-1663 |
| Y742 | The baseline does not adopt the calibration, and adopting it is a §1.4 decision rather than a solver knob. | UNCHANGED | DESIGN | stipulated | L1663 |
| Y743 | LP determinism across machines is open: the min-cost-flow solve must pivot identically on identical input, replacing v1's ε-magnitude question. | UNCHANGED | DESIGN | stipulated | L1664-1665 |
| Y744 | AI merchant reassignment cadence is open. | UNCHANGED | DESIGN | stipulated | L1666 |

## §3.14 — AI merchant assignment (L1668-1685)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y745 | The two ends of a link never compete: a merchant at `n` on {n,m} moves goods oriented n to m, one at `m` moves goods oriented m to n, disjoint sets, so competition stays where vanilla puts it — between merchants at the same node. | UNCHANGED | MODEL | algebraic derivation | L1670 |
| Y746 | One precompute serves every country: for each good, a backward pass over its DAG gives `S_g[n][H]`, the expected fraction of a unit of `g` at `n` arriving at `H`, multiplying through collection, steering shares and the per-link multi-merchant boost. | UNCHANGED | MODEL | algebraic derivation | L1672 |
| Y747 | `collected_share(n,g)` reaches 1 at `g`'s sink, which terminates the recursion. | UNCHANGED | MATH | algebraic derivation | L1672 |
| Y748 | All three survival-table inputs are country-independent aggregates, so this is one table rather than one per nation — about 1.5 MB at double precision, well under a million operations per solve. | UNCHANGED | MODEL | algebraic derivation | L1672 |
| Y749 | v1 and v2 both said 0.75 MB, which is the single-precision figure; the rest of the solver is double precision — 29 goods × 80 × 80 entries at 8 bytes is 1,484,800 bytes, and its residuals sit at 1e-16, one ULP of a double — so the natural implementation is twice what v1 and v2 recorded. | UNCHANGED | MODEL | algebraic derivation | L1672 |
| Y750 | Scoring reads the survival table for both steering and collecting, so the opportunity cost of collecting falls out as the same comparison a human player makes by hand, and denial scoring falls out of the same table against a rival's home node. | UNCHANGED | MODEL | algebraic derivation | L1674 |
| Y751 | The off-home penalty is a power modifier rather than a haircut on value: it reduces the country's trade power in that node, and that reduced power feeds both the collect/transfer ratio and the share among collectors, so it lowers the fraction retained in the node and the collector's slice of it. | UNCHANGED | ENGINE | algebraic derivation | L1676 |
| Y752 | Scoring a collect candidate as value × share × 0.5 is wrong; the halving must be applied to power and the two-stage formula run from there. | UNCHANGED | MODEL | algebraic derivation | L1676 |
| Y753 | That is also why the off-home penalty falls out of the survival table at all: the table is built from power-derived shares. | UNCHANGED | MODEL | algebraic derivation | L1676 |
| Y754 | The home-node bonus is voided entirely by placing any collector outside the home node, so a collect candidate's true cost includes a penalty no single-merchant score can see — run the greedy twice, once all-steer with the bonus and once unconstrained without, and keep the better portfolio. | UNCHANGED | ENGINE | algebraic derivation | L1678 |
| Y755 | Greedy scoring against a moving field can oscillate between AIs; damping the shares between passes should hold it, and the prototype must verify. | UNCHANGED | MODEL | stipulated | L1678 |
| Y756 | Reassignment cadence is undecided and is the one item left for the human, because merchants take travel time so an AI re-optimizing every solve leaves them permanently in transit. | UNCHANGED | DESIGN | stipulated | L1680 |
| Y757 | Mirroring vanilla's cadence is the stated preference, but the relevant define was not located in the visible portion of any dump, so it requires finding it or measuring it by observation. | UNCHANGED | DESIGN | stipulated (the define's absence is a negative search result) | L1682 |
| Y758 | The computed alternative moves a merchant when `(V_new − V_incumbent) × expected_tenure > V_incumbent × travel_time`, using `MERCHANT_SPEED` and the survival table, both of which exist, with `expected_tenure` endogenous and wired to the flip-rate measurement. | UNCHANGED | MODEL | stipulated | L1683 |
| Y759 | The argument for computing the cadence is that vanilla's cadence was tuned against a graph that never moves, so copying it would import a constant fitted to different dynamics; the argument against is that it overrides a stated preference and node-to-node travel time still needs the game's distance metric. | UNCHANGED | DESIGN | stipulated | L1685 |

## §3.15 — Rejected (L1687-1797)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y760 | The v1 Laplacian potential as the orientation core is rejected: its sink placement is topological, sinks landing where the field is locally flat, demand entering only as `(c−s)/deg` against the local spread, and the supply signal being sparse rather than large. | UNCHANGED | MODEL | algebraic derivation | L1689-1692 |
| Y200 | v3.0 and v4.0 repeated the 10⁷ versus 10²–10³ ratio in this entry while v4.0's own §3.2 was withdrawing it. | CHANGED | MODEL | read from a file (the prior spec versions) | L1693-1695 |
| Y199 | The Laplacian entry maintains no copy of the contrast measurement — §3.2 carries it — and with v1's ε floor removed the demand side is the wider of the two. | CHANGED | MODEL | algebraic derivation | L1695-1697 |
| Y201 | `cloves` has a single producer and so no contrast to measure at all, which is the sparsity point in miniature. | NEW | MODEL | algebraic derivation | L1696-1698 |
| Y761 | The Laplacian was diagnosed, measured and replaced, and what it did guarantee — 100% reachability via conservation and exact conduit behaviour — DRAIN keeps by construction. | UNCHANGED | MODEL | cited to `../v1-laplacian/diagnosis.md` and `drain-orientation.md` | L1698-1700 |
| Y762 | Pure min-cost-flow orientation with no sweep is rejected: it orients only the roughly 79-edge support (a spanning-tree basis), leaving half the map undirected, and its value-weighted aggregate contains directed cycles; DRAIN is exactly this plus the drainage completion that fixes both. | UNCHANGED | MODEL | numerical test | L1702-1704 |
| Y202 | Ranked orientation wins the sink-demand alignment statistics — a far higher share of top-demand nodes in its sink sets than DRAIN — and fails on delivery: it is monotone, so a large share of world demand is stranded, it leaves orphan sinks a good cannot reach (Genoa as a cloves sink cloves never reach), it posts net-producer sinks where DRAIN, LAP and FLOW post none, and it keeps several times DRAIN's sinks per good. | CHANGED | MODEL | algebraic derivation; no figures are carried | L1706-1713 |
| Y203 | Seeded basin growth converges flow to the chosen seeds and starves everything off a supply-to-seed path, leaving demand unserved at every tuning tried. | CHANGED | MODEL | algebraic derivation; no reach figure is quoted | L1715-1717 |
| Y763 | Seeded basin growth's useful ideas — HHI-adaptive sink count and stall self-correction — survive inside DRAIN's Phases 1 and 3. | UNCHANGED | MODEL | stipulated | L1717-1719 |
| Y764 | DEF-descending free-edge priority is rejected as measurably worse: on the certificate, unmet demand is identically zero so DEF is total demand, and pointing free edges into already-served subtrees strands greedy flow; the adopted key is DEF-ascending. | UNCHANGED | MODEL | numerical test (cited to `drain-orientation.md` §6) | L1721-1724 |
| Y765 | Authored demand weights are rejected: authored data in a model that needs none. | UNCHANGED | DESIGN | stipulated | L1726 |
| Y766 | Trade income inside `wealth` is rejected: it reintroduces flow-demand-orientation-flow circularity, and the graph would respond to merchants rather than to the world. | UNCHANGED | MODEL | algebraic derivation | L1728 |
| Y767 | Node-level α is rejected: it makes demand concentration a function of how finely the map was sliced. | UNCHANGED | MATH | algebraic derivation | L1730 |
| Y768 | A median-relative α anchor is rejected: a good's concentration would shift because other goods changed price. | UNCHANGED | MATH | algebraic derivation | L1732 |
| Y769 | α floored at 1 is rejected: it discards the cheap-bulk regime. | UNCHANGED | DESIGN | stipulated | L1734 |
| Y770 | Production income as the aggregate supply term is rejected because it makes world supply depend on owners' idea groups; its v1 second strike, breaking the α = 1 identity, is moot with the identity gone, so the first strike suffices. | UNCHANGED | MODEL | algebraic derivation | L1736 |
| Y771 | A τ margin on orientation is rejected: it manufactures cycles. | UNCHANGED | MATH | algebraic derivation | L1738 |
| Y772 | Uniform supply in the aggregate solve is a v1 entry, moot in v2 and retained for history: it answered a question nobody asked and destroyed the identity that made `φ₀` worth computing, and both left with the Laplacian. | UNCHANGED | MODEL | algebraic derivation | L1740-1742 |
| Y773 | `φ₀` as the installed graph is a v1 entry, moot in v2: it was not the economy the model runs, the installed graph is `Φ_w` (v2.0 briefly used `Φ_ord`), and its correctness check is cross-implementation orientation equality. | UNCHANGED | MODEL | stipulated | L1744-1746 |
| Y774 | `Φ_ord` as the installed graph is the most self-coherent aggregate measured — better than `Φ_w` on that one axis, and acyclic for free — but its ends are scheduling artifacts rather than places and its end count does not concentrate as demand concentrates. | CHANGED | MODEL | numerical test plus algebraic derivation | L1748-1751 |
| Y204 | §3.15's `Φ_ord` entry maintains no figures and its "measured coherence ceiling any future aggregate should be compared against" role is withdrawn; the ceiling v2.0 and v2.1 quoted predates §3.6's deterministic sweep and was never regenerated after it. | CHANGED | DESIGN | stipulated | L1751-1754 |
| Y205 | The 3-mass gravity field over the top-3 pairwise-unconnected demanders reproduces whatever end count it is seeded with while γ is small enough and loses that property as γ approaches 1; no figures are maintained, and the rejection rests on three grounds none of which is numeric — it pins the end count by fiat, it needs a second operator with its own reach knob, and a pure `wealth^α` edge comparison with no reach term does not concentrate ends at all because a local wealth maximum survives every positive α. | CHANGED | MODEL | algebraic derivation; no figures are maintained | L1756-1765 |
| Y775 | The emergent-count wealth good replaced the pinned-count fields. | UNCHANGED | MODEL | stipulated | L1765 |
| Y776 | A vestigial in-game economy with net treasury settlement is rejected: correct treasuries, wrong displays, wrong AI inputs. | UNCHANGED | DESIGN | algebraic derivation | L1767 |
| Y777 | Per-good propagation is rejected: it breaks the income factoring and with it Goal 7. | UNCHANGED | MODEL | algebraic derivation | L1769 |
| Y778 | Node-level collect/transfer rules are rejected: the collect/transfer split is per good because whether a good has anywhere to go is per good. | UNCHANGED | MODEL | algebraic derivation | L1771 |
| Y779 | Treating unsteered goods as fully collected is rejected: transfer power does not come from merchants, and full collection happens at a sink, which is a property of the graph. | UNCHANGED | MODEL | algebraic derivation | L1773 |
| Y780 | Undirected shortest path as the primary fleet route is rejected: a geodesic over a directional structure can route a fleet against every arrow on the map. | UNCHANGED | MATH | algebraic derivation | L1775 |
| Y781 | Automatic per-good merchant targeting is rejected: one vanilla arrow click already achieves per-good resolution, and automation would cost denial steering. | UNCHANGED | DESIGN | stipulated | L1777 |
| Y782 | Companion-overlay merchant assignment is rejected: assignment must stay a game action or vanilla knowledge stops transferring. | UNCHANGED | DESIGN | stipulated | L1779 |
| Y783 | Emission-time pruning of near-flat links is rejected: peripheral termini are intended consumption, and the power-at-both-ends gate already withholds unworked corridors, with the §3.13 calibration option's twig tolerance a bounded measured exception. | UNCHANGED | DESIGN | stipulated | L1781-1784 |
| Y784 | Edge conductance / weighted Laplacian stays rejected: v1 rejected it as "too much mechanical surface", the audit showed the unweighted metric was in fact the cause of v1's sink misplacement, the operator was replaced, and there is no longer a Laplacian to weight. | UNCHANGED | MODEL | algebraic derivation | L1786-1789 |
| Y785 | Staged delivery is rejected: the intermediate states are different designs sharing a solver rather than subsets of this one. | UNCHANGED | DESIGN | stipulated | L1791 |
| Y786 | "The aggregate map is not a DAG" is still an error, with v1's reason corrected: v1 defended it by claiming net flow is the gradient of `Φ`, contradicting its own §3.9 and false, since the value-weighted net flow measurably contains cycles. | UNCHANGED | MODEL | numerical test | L1793-1795 |
| Y787 | The aggregate is a DAG because `Φ_w` is a DRAIN orientation, acyclic by the marking-order argument, whose own marking order is a per-node scalar reproducing it — which is what makes an installable single network exist at all. | UNCHANGED | MATH | algebraic derivation | L1795-1797 |

## §3.16 — Evidence standard (L1799-1861)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y788 | v1 carried an evidence standard — "every retraction traced to a premise that entered through prose; nothing built on adjacency data, file values, or the model's own equations failed" — and the claim audit refuted the standard itself. | UNCHANGED | MODEL | read from a file (the v1 spec and its validation) | L1801-1803 |
| Y789 | At least fifteen non-prose claims failed, by three distinct mechanisms. | UNCHANGED | MODEL | read from a file (the validation) | L1803-1804 |
| Y790 | Mechanism 1, file values remembered from an older patch: the 75% overseas autonomy floor is pre-Common-Sense, and 1.37 has regime floors of 90/50/20/0. | UNCHANGED | INSTALL | read from a file | L1806-1807 |
| Y791 | Mechanism 2, file values transformed and then reported as raw: v1's grain (1.25) and livestock (1.00) base prices are exactly `price / P₀`, the ratio computed and then written down as the price. | UNCHANGED | INSTALL | read from a file | L1808-1810 |
| Y792 | Mechanism 3, the spec's own algebra instantiated without checking the instantiation: ε provably preserved the α = 1 identity only if applied to `φ₀`'s supply as well. | UNCHANGED | MATH | algebraic derivation | L1811-1813 |
| Y206 | Implemented as written, v1's ε left the α = 1 identity's residual at 1e-5 against v1's ε of 1e-6, and would have been diagnosed as a solver bug. | CHANGED | MODEL | numerical test | L1813-1814 |
| Y793 | One of only three claims carrying `verified (method unstated)` provenance — Propagate Religion's gating — turned out wrong. | UNCHANGED | MODEL | read from a file (the validation) | L1816-1817 |
| Y794 | The real signal in the audit was provenance: nine of the sixteen refuted ENGINE claims were UNSOURCED, and v2's "nine of fourteen" matches no partition of the refuted set, since there are sixteen ENGINE-typed refutations or thirteen excluding the three that carried derivation provenance. | UNCHANGED | MODEL | read from a file (the validation) | L1817-1820 |
| Y795 | The rule is not "trust derivations" and not "distrust prose" but that anything which entered without a recorded source is the risk, whatever it looks like once written down. | UNCHANGED | DESIGN | stipulated | L1821-1822 |
| Y796 | Every engine fact in this spec must carry its source — a file path, a binary string, or a named observation — and a claim without one is a to-do rather than a fact. | UNCHANGED | DESIGN | stipulated | L1822-1823 |
| Y797 | The gap that mattered more than any refutation: v1 never stated what determines sink placement, so the claim inventory had nothing to extract, the validation had nothing to refute, and the model shipped with a fatal placement flaw that claim-checking structurally could not catch. | UNCHANGED | MODEL | algebraic derivation | L1825-1828 |
| Y798 | The audit found that flaw only by running the solver and asking why the output looked wrong. | UNCHANGED | MODEL | stipulated | L1828 |
| Y799 | The standing repair is in this document's structure: what determines sink placement, what determines free-edge direction, what guarantees reachability, why the aggregate is acyclic, and why the result is scheduler-invariant are now stated as checkable claims. | UNCHANGED | DESIGN | stipulated | L1828-1832 |
| Y800 | Each of those properties is provable or measured-and-labelled and each is checked at runtime — as an assertion where it is a theorem and as a monitor where it is a measurement, which is the distinction sink placement forced. | UNCHANGED | DESIGN | stipulated | L1832-1835 |
| Y801 | The next audit's first question should be which property of the output this spec still does not state. | UNCHANGED | DESIGN | stipulated | L1836-1837 |
| Y802 | The cautionary case is now closed and it closed the other way: the propagation source condition was corrected once (ship propagation under its modifier) and defended by two reviewers against the wrong error, and the engine's tooltip then appeared to carry a second qualifier that §1.9 did not. | UNCHANGED | MODEL | stipulated | L1839-1842 |
| Y803 | Probe 15 settled it: the qualifier is descriptively false, since a country with no provinces and no merchant in the upstream node still receives propagated power there, itemised by the engine as `Transfers from traders downstream`, so §1.9 was right not to carry it. | UNCHANGED | ENGINE | engine test | L1842-1845 |
| Y804 | The lesson is not the one the case was filed under: it was filed as "agreement between reviewers is not verification", which remains true, but what actually happened is that a binary string — the class of evidence §3.16 nominates as sufficient — was the unreliable source. | UNCHANGED | MODEL | algebraic derivation | L1847-1849 |
| Y805 | A localisation string describes intent, not behaviour. | UNCHANGED | ENGINE | algebraic derivation | L1850 |
| Y806 | Sources are necessary but not sufficient, and an engine fact sourced to a string is settled only when something observes the behaviour the string describes. | UNCHANGED | DESIGN | stipulated | L1850-1852 |
| Y807 | During the declaration-order test a permuted node file differed from vanilla on 61 of 80 nodes — a real measurement from a real game, parsed from real save files. | UNCHANGED | ENGINE | engine test | L1854-1856 |
| Y808 | That measurement was meaningless, because two runs of the same vanilla build differ on 49 of 80 nodes by up to 8.96% across the same five fields, since the engine randomises AI merchant placement at start. | UNCHANGED | ENGINE | engine test | L1856-1859 |
| Y809 | A measurement without a null comparison is not evidence. | UNCHANGED | DESIGN | stipulated | L1859-1860 |
| Y810 | Every measured claim in this document that could vary run to run should carry the control that bounds its noise floor. | UNCHANGED | DESIGN | stipulated | L1860-1861 |

## §0 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y811 | v5.0's substantive change was applying the local-modifier classification to the whole install rather than to the trade-good tables alone. | REMOVED | DESIGN | stipulated | v5 L14-18 |
| Y812 | The whole-install classification adds sixteen provinces and moves the aggregate graph from two 1444 sinks to one. | REMOVED | MODEL | numerical test | v5 L18-19 |
| Y813 | No figure in v5.0 is unverified, and the one place the document declines to project a number says so in place. | REMOVED | DESIGN | stipulated | v5 L20-21 |

## §1.1 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y814 | On a connected core the fallback branch fires only when `b` is identically 0 across it. | REMOVED | MODEL | algebraic derivation | v5 L100-101 |
| Y815 | `b` identically 0 happens for the aggregate graph on a uniform-wealth map. | REMOVED | MODEL | algebraic derivation | v5 L101-102 |
| Y816 | At a fallback stall the candidates are usually all zero-wealth, so the wealth key ties and the index decides. | REMOVED | MODEL | algebraic derivation | v5 L103-104 |
| Y817 | That index tiebreak is why §2.4 item 1 makes a canonical emitter node order a correctness requirement rather than a convention. | REMOVED | DESIGN | algebraic derivation | v5 L104-106 |
| Y818 | On 1444 the per-good sink counts are 1-7 per good with mean 3.6. | REMOVED | MODEL | numerical test | v5 L133-134 |
| Y819 | The §1.1 property measurements were regenerated for v5.0 by `v5measure.py`. | REMOVED | MODEL | computed by a named script | v5 L119 |
| Y820 | On a map where Phase 0 is a no-op and no fallback fires, the last two sink cases are empty and the sink set is exactly the formula set. | REMOVED | MODEL | algebraic derivation | v5 L130-133 |

## §1.3 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y821 | Two provinces with the same terrain, development and trade good have the same wealth whoever owns them. | REMOVED | MODEL | algebraic derivation | v5 L157-160 |
| Y822 | `trade_value(p)` carries a `(1 + sum of local trade-value modifiers)` factor. | REMOVED | MODEL | stipulated | v5 L165-166 |
| Y823 | `goods_produced(p)` carries a local flat goods bonuses term added to `GP_COEFF · base_production`. | REMOVED | MODEL | stipulated | v5 L163-164 |
| Y824 | Both wealth coefficients were measured from the running game and neither is a define, `defines.lua` having been searched, so both are engine constants recovered by observation. | REMOVED | INSTALL | read from a file (a negative search) | v5 L171-173 |
| Y825 | The tax tooltip schema is `Base: X (Yearly 12·X)`. | REMOVED | ENGINE | measured in-game | v5 L176-178 |
| Y826 | The monthly production tooltip's `Trade Value` line is the province window's annual `Trade Value` over twelve, observed 3.52 to +0.29. | REMOVED | ENGINE | measured in-game | v5 L178-180 |
| Y827 | Both monthly figures are the annual value over twelve, so the annual forms add directly with no conversion. | REMOVED | MODEL | algebraic derivation | v5 L180-181 |
| Y828 | `Base 0.49` then `Tax Income Efficiency 125.0%` gives 0.6125, which the province window shows as 0.62. | REMOVED | ENGINE | measured in-game | v5 L183-186 |
| Y829 | Flat goods bonuses are the exception to modifier ordering: they add into `goods_produced` before the price multiply. | REMOVED | ENGINE | measured in-game | v5 L186-187 |
| Y830 | Fifteen 1444 provinces carry a flat bonus in the additive `Base Goods Produced` block, so the ordering matters in practice and not only in principle. | REMOVED | INSTALL | read from a file | v5 L190-192 |
| Y831 | A modifier is local if and only if its value depends only on the province's own attributes — terrain, climate, trade good, development, buildings — and on no country's state. | REMOVED | MODEL | stipulated | v5 L194-197 |
| Y832 | A modifier enters wealth if and only if it modifies `goods_produced`, `price` or `tax_value`. | REMOVED | MODEL | stipulated | v5 L197-199 |
| Y833 | The engine's trade-good data model is one instance of the locality test: a good's `province = { }` block is province-scoped and its `modifier = { }` block is country-scoped, so only the first can be local. | REMOVED | INSTALL | read from a file | v5 L199-203 |
| Y834 | The two tests are applied to the whole install rather than one file; v4.0 stated the rule and then swept only `common/tradegoods/`, concluding "exactly two" and missing sixteen provinces. | REMOVED | MODEL | read from a file (v4.0's sweep) | v5 L205-208 |
| Y835 | `gems` `local_tax_modifier = 0.15` on 43 provinces is local and enters `tax_value`. | REMOVED | INSTALL | read from a file | v5 L212 |
| Y836 | `incense` `trade_value_modifier = 0.1` on 29 provinces is local and enters `trade_value`. | REMOVED | INSTALL | read from a file | v5 L213 |
| Y837 | Great-project `province_modifiers` where `can_use_modifiers_trigger` is empty (6 provinces) are local and enter `goods_produced` and `trade_value`. | REMOVED | INSTALL | read from a file | v5 L214 |
| Y838 | `add_permanent_province_modifier` in the undated province-history block (10 provinces) is local and enters `goods_produced`. | REMOVED | INSTALL | read from a file | v5 L215 |
| Y839 | The five static condition modifiers are all zero at the 1444 start, and §1.2 and §3.3 both depend on them biting later. | REMOVED | INSTALL | read from a file | v5 L216 |
| Y840 | `glass` `local_production_efficiency = 0.1` is local but does not enter wealth, because it modifies production income which wealth does not compute. | REMOVED | INSTALL | read from a file | v5 L217 |
| Y841 | `chinaware` `local_autonomy = -0.1` is local but does not enter wealth, because it modifies local autonomy which wealth does not compute. | REMOVED | INSTALL | read from a file | v5 L218 |
| Y842 | 361 provinces carry a centre of trade at 1444, and no CoT level in `common/centers_of_trade/` grants any of the four keys wealth reads — a clean near-miss, recorded so it is not reopened. | REMOVED | INSTALL | read from a file | v5 L219 |
| Y843 | `production_leader` `trade_goods_size_modifier = 0.10` is not local, because which country leads a good's production is a country's state. | REMOVED | INSTALL | read from a file | v5 L220 |
| Y844 | Goods-produced efficiency from nearby merchant republics, trading cities and trade companies (`bonus_from_merchant_republics`, `eu4.exe:0x1cc7128`) is not local, being set by which neighbouring countries hold those government forms. | REMOVED | INSTALL | read from a file (a binary offset) | v5 L221 |
| Y845 | Buildings are local by the test and empty at 1444, because no province's start state carries a temple, workshop or manufactory. | REMOVED | INSTALL | read from a file | v5 L223 |
| Y846 | `terrain.txt` and the climate static modifiers are local but grant only keys wealth does not compute — `allowed_num_of_buildings`, `defence`, `local_defensiveness`, `local_development_cost`, `movement_cost`, `nation_designer_cost_multiplier`, `supply_limit`, colonial growth and hostile attrition. | REMOVED | INSTALL | read from a file | v5 L224 |
| Y847 | A great project contributes the `province_modifiers` accumulated up to its `starting_tier` when its `can_use_modifiers_trigger` is empty, and tiers reached after the start date are owner spending and are out. | REMOVED | INSTALL | read from a file | v5 L226-228 |
| Y848 | 85 of the 130 great projects live at 1444 are gated on a country's culture, religion, government or flags. | REMOVED | INSTALL | read from a file | v5 L228-230 |
| Y849 | Six great projects carry a key wealth reads: `falun_copper_mine` (province 8, `trade_goods_size` 3.0), `krakow_cloth_hall` (262, `trade_goods_size_modifier` 0.10) and the four Grand Canal provinces (684, 1821, 1822, 2145; `trade_goods_size` 0.5 and `trade_value_modifier` 0.1 each). | REMOVED | INSTALL | read from a file | v5 L230-233 |
| Y850 | Province 1821 is the richest single province in the game. | REMOVED | MODEL | numerical test | v5 L233 |
| Y851 | The starting tier is the right line and "owner action" is not, because development is an owner action so a rule excluding those would exclude `base_production`, wealth's primary input. | REMOVED | DESIGN | algebraic derivation | v5 L233-235 |
| Y852 | The ten permanent modifiers are `granary_of_the_mediterranean` (362, 363, 2316, 4316), `skanemarket` (6), `icelanding_fisher_sea` (370, 371), `diamond_mines_of_golconda_modifier` (542), `jingdezhen_kilns` (2151) and `coffea_arabica_modifier` (387), all flat `trade_goods_size`. | REMOVED | INSTALL | read from a file | v5 L237-240 |
| Y853 | `province_triggered_modifiers`' `stora_kopparberget_modifier` is gated `NOT = { has_dlc = "Leviathan" }` and grants `trade_goods_size = 5.0` on province 8, the same province as `falun_copper_mine`, so with Leviathan the project gives 3.0 and without it the modifier gives 5.0. | REMOVED | INSTALL | read from a file | v5 L242-247 |
| Y854 | Every wealth figure in v5.0 was measured with Leviathan installed. | REMOVED | MODEL | stipulated | v5 L246-247 |
| Y855 | Glass and chinaware — local but not entering — are the whole of the rule-versus-vocabulary tension, since §1.3 excludes production efficiency and autonomy by name and the second test excludes them again. | REMOVED | MODEL | algebraic derivation | v5 L249-251 |
| Y856 | Every province the model counts is a city (`is_city = yes`). | REMOVED | INSTALL | read from a file | v5 L259-261 |
| Y857 | `s` and `c` are computed over provinces with an owner and `is_city = yes`. | REMOVED | DESIGN | stipulated | v5 L263-264 |
| Y858 | Owner-agnostic wealth removes the single largest source of hidden owner-dependence from the aggregate graph. | REMOVED | MODEL | algebraic derivation | v5 L269-270 |

## §1.5 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y859 | Repricing the 45 owned latent-coal provinces flips 29 of 159 `Φ_w` edges. | REMOVED | MODEL | computed by a named script (`v5measure.py`) | v5 L327-329 |
| Y860 | Coal's base price of 10.0 is the highest in vanilla. | REMOVED | INSTALL | read from a file | v5 L329-330 |

## §1.6 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y861 | `Φ_w`'s sink count is set by `α_Φ` and only the sink locations are emergent. | REMOVED | MODEL | algebraic derivation | v5 L358-360 |
| Y862 | Downscaling `b_w` gives 16 edge flips at ×10⁻² and 83 at ×10⁻⁶. | REMOVED | MODEL | numerical test | v5 L376-378 |
| Y863 | 1444's `b_w` has largest magnitude 0.0227. | REMOVED | MODEL | numerical test | v5 L379-380 |
| Y864 | Measured at `α_Φ = 1.5` there is one sink, `hangzhou`, rank 1 in the `α_Φ`-weighted wealth field `c_w` and rank 10 in raw node wealth, where `english_channel` is 1st. | REMOVED | MODEL | computed by a named script (`v5measure.py`) | v5 L382-384 |
| Y865 | v2 through v4's two-sink result was measured on a wealth field missing the sixteen provinces v5's §1.3 carries, and correcting the field removes it. | REMOVED | MODEL | numerical test | v5 L384-386 |
| Y866 | v2 also wrote "wealth ranks" without saying which, and the plain reading was wrong then too. | REMOVED | MODEL | read from a file (the prior spec version) | v5 L386-387 |
| Y867 | Phase 1 selects `hangzhou` directly, so there are 0 promotions and 0 fallbacks and the self-correction never fires on this input. | REMOVED | MODEL | numerical test | v5 L387-388 |
| Y868 | Seven sources — `kongo`, `patagonia`, `james_bay`, `mississippi_river`, `chengdu`, `australia`, `tunis` — at `c_w` ranks 52-79 with mean degree 3.0 against the map's 4.0. | REMOVED | MODEL | numerical test | v5 L388-391 |
| Y869 | 0 edge flips and 0 sink-set changes under ±1% wealth noise across 5 seeds. | REMOVED | MODEL | numerical test | v5 L392-393 |
| Y870 | Agreement with the per-good graphs is 52.5% of edge-goods (51.5% value-weighted) against the superseded `Φ_ord`'s 60.3% — a gap of 7.8 points. | REMOVED | MODEL | numerical test | v5 L396-398 |
| Y871 | v2's 62.7% was measured under the old scan-order sweep and was never regenerated after §3.6 adopted the deterministic one. | REMOVED | MODEL | read from a file (the prior spec version) | v5 L398-400 |
| Y872 | The `α_Φ` sink-count band table: 1 sink `hangzhou` at [1.43, 1.93] width 0.50 (the widest band on this field); 3 sinks {doab, genua, hangzhou} at [2.26, 2.71] width 0.45; 2 sinks {genua, hangzhou} at [1.94, 2.25] width 0.31; 2 sinks {english_channel, hangzhou} at [1.41, 1.42] width 0.01. | REMOVED | MODEL | numerical test | v5 L402-409 |
| Y873 | v4.0's two-sink result is not a band: refined to 0.001 it spans [1.406, 1.424], 0.018 wide against the one-sink band's 0.506. | REMOVED | MODEL | numerical test | v5 L411-413 |
| Y874 | Under ±1% wealth noise across 8 seeds the narrow window's edges move by up to 0.02 while its width ranges 0.00 to 0.03, so the window is the same size as the noise that perturbs it and on some seeds collapses to a single sampled α. | REMOVED | MODEL | numerical test | v5 L413-416 |
| Y875 | The three wide bands over those same seeds keep widths of 0.28-0.51 with edges moving no more than 0.03. | REMOVED | MODEL | numerical test | v5 L416-417 |
| Y876 | A constant cannot honestly be placed inside a window narrower than the uncertainty in its own edges. | REMOVED | DESIGN | stipulated | v5 L417-418 |
| Y877 | An earlier draft said the narrow window "moves or disappears entirely" under noise; at 8 seeds it disappears on none of them and only shrinks. | REMOVED | MODEL | numerical test | v5 L418-420 |
| Y878 | `α_Φ` is retained at 1.5 because it sits inside the widest sink-count band and nothing now selects a different value. | REMOVED | DESIGN | numerical test | v5 L420-422 |
| Y879 | Sampled at the six values v2 used the sink count is 5, 1, 2, 4, 3, 1. | REMOVED | MODEL | numerical test | v5 L422-423 |
| Y880 | A 1-2% European development edge produces a European sink: at ×1.02 across Europe's 823 counted provinces the sinks are {doab, english_channel, hangzhou, wien}. | REMOVED | MODEL | computed by a named script (`europe.py`) | v5 L428-431 |
| Y881 | `english_channel` is a sink at every larger European growth factor tested. | REMOVED | MODEL | numerical test | v5 L430-431 |
| Y882 | What the model claims is the threshold rather than the size of the historical edge: 2% is enough, and the project measures nothing about how much development Europe actually gained. | REMOVED | DESIGN | stipulated | v5 L431-433 |
| Y883 | All three institutions the period is named for begin in Europe inside the 1450-1550 window. | REMOVED | INSTALL | read from a file | v5 L433-437 |
| Y884 | The Renaissance's embracement bonus is a standing 5% discount on every subsequent development point. | REMOVED | INSTALL | read from a file | v5 L437-439 |
| Y885 | The Lowlands alone suffice: developing only the nine Lowland provinces in `english_channel` (Holland, Zeeland, Vlaanderen, Brabant, Antwerpen, Utrecht, Gelre, Friesland, Breda) by ×1.20 makes `english_channel` a sink beside `hangzhou`, and it stays one through ×10. | REMOVED | MODEL | computed by a named script (`europe.py`) | v5 L441-444 |
| Y886 | ±2% random wealth noise leaves the 1444 sink set unchanged on three seeds, while +2% applied systematically to Europe alone changes it, so the map does not twitch and it does move. | REMOVED | MODEL | numerical test | v5 L445-448 |
| Y887 | The 1444 Silk Road route runs through `doab`: genua, alexandria, aleppo, persia, lahore, doab, ganges_delta, burma, gulf_of_siam, canton, hangzhou. | REMOVED | MODEL | numerical test | v5 L450-452 |
| Y888 | From the Channel the route is the Hansa and the Danube: english_channel, lubeck, saxony, wien, venice, ragusa, constantinople, aleppo, and onward. | REMOVED | MODEL | numerical test | v5 L454-456 |
| Y889 | Nothing routes through the Cape, which is what a 1444 map should say. | REMOVED | MODEL | numerical test | v5 L456-457 |
| Y890 | The Cape's per-good spice route is malacca, cape_of_good_hope, zanzibar, gulf_of_aden, alexandria, genua. | REMOVED | MODEL | numerical test | v5 L457-459 |
| Y891 | Scaling the 22 European nodes' wealth ×2 makes `genua` the sole sink, and under the 18-node set alone sole-`genua` needs ×2.5. | REMOVED | MODEL | numerical test | v5 L461-469 |
| Y892 | Between ×3 and ×3.75 the Cape of Good Hope reverses and outside that window it does not, so the reversal is a band and not a threshold. | REMOVED | MODEL | numerical test | v5 L462-465 |
| Y893 | Dev-stacking `hangzhou`'s top province keeps it the sole sink at ×20, ×30 and ×50, with a transient split into three at ×10. | REMOVED | MODEL | numerical test | v5 L469-471 |

## §1.10 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y894 | Almost nothing absorbs threshold chatter. | REMOVED | ENGINE | algebraic derivation | v5 L560-561 |
| Y895 | The caravan cap of 50 is 8.6% to 32.0% of an inland node's total trade power, median 17.9% over the flag's 26 inland nodes, and on §2.2's 25-node derived basis only the median moves, to 17.5%. | REMOVED | MODEL | numerical test | v5 L570 |

## §2.2 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y896 | Solver item 4's wealth formula includes local flat goods bonuses inside the goods term and a `(1 + local trade-value modifiers)` factor on price. | REMOVED | DESIGN | stipulated | v5 L620-623 |
| Y897 | The solver reads local modifiers from §1.3's whole-install classification: `gems` (+15% tax, 43 provinces), `incense` (+10% trade value, 29 provinces), six great projects and ten permanent province modifiers — 16 provinces beyond the two trade goods. | REMOVED | MODEL | numerical test | v5 L623-628 |
| Y898 | World wealth is 10,677.50 annual ducats over 2,452 counted provinces. | REMOVED | MODEL | numerical test | v5 L628-629 |
| Y899 | Solve cost is 0.17-0.21 s for all 29 goods, a mean of 5.7-7.3 ms per good across runs, with individual goods ranging 5.4-24 ms so 7.3 is an average and not a maximum. | REMOVED | MODEL | numerical test | v5 L641-645 |

## §2.2a (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y900 | Where Phase 0 acts, free-edge determinism is the same in both halves, because peeling does not touch the priority key. | REMOVED | MODEL | algebraic derivation | v5 L682 |

## §2.3 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y901 | The two wealth coefficients of §1.3 are hardcoded in the binary, `defines.lua` and `common/defines/` having been searched and containing neither. | REMOVED | INSTALL | read from a file (a negative search) | v5 L700-703 |
| Y902 | `α_Φ`'s stated calibration is withdrawn because on the corrected wealth field 1.5 does not yield the two-sink map, and the window that does is narrower than the uncertainty in its own edges under ±1% wealth noise. | REMOVED | MODEL | numerical test | v5 L708-713 |
| Y903 | 1.5 is retained because it sits inside the widest sink-count band and nothing now selects a different value. | REMOVED | DESIGN | numerical test | v5 L713-715 |

## §2.4 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y904 | The node order is a correctness requirement because §1.1's priority key breaks exact ties by node index and on the fallback branch the wealth key ties and the index alone decides the orientation. | REMOVED | MODEL | algebraic derivation | v5 L743-747 |
| Y905 | Without one canonical node order kept stable across rebuilds, the same world can produce two different maps. | REMOVED | MODEL | algebraic derivation | v5 L747-749 |
| Y906 | 1444 has one end node, `hangzhou`, against vanilla's three. | REMOVED | MODEL | numerical test | v5 L752-753 |

## §2.7 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y907 | §1.9's "every immediately upstream node" is correct as written and gains no qualifier. | REMOVED | ENGINE | engine test | v5 L787-788 |

## §2.8 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y908 | Sinks are 1 to 7 per good, and high-demand nodes are sinks at 14.5% in the top demand decile against 6.9% in the bottom. | REMOVED | MODEL | numerical test | v5 L806 |
| Y909 | Zeroing `hangzhou`-node development moves the `Φ_w` sinks from {hangzhou} to {doab, english_channel, gulf_of_siam, sevilla}. | REMOVED | MODEL | numerical test | v5 L810 |
| Y910 | `hangzhou`'s `c_w` rank is 1 against `beijing`'s 31, node wealth 245.0 against 143.8, and it holds the richest single province in the game. | REMOVED | MODEL | numerical test | v5 L810 |
| Y911 | Zeroing `beijing` gives 17 flips with sinks {doab, english_channel, hangzhou, sevilla}, because it deletes 1.3% of world wealth. | REMOVED | MODEL | numerical test | v5 L810 |
| Y912 | The rank gap is what carries the razed-China row, not a null result. | REMOVED | MODEL | algebraic derivation | v5 L810 |
| Y913 | `Φ_w` agrees with the per-good graphs on 51.5% of edge-goods weighted by trade value and 52.5% unweighted. | REMOVED | MODEL | numerical test | v5 L826-829 |

## §3.2 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y914 | With no regularizer the spices supply ratio over producing nodes is 36 against a demand ratio of 482.2, which points the other way. | REMOVED | MODEL | numerical test | v5 L893-896 |
| Y915 | Better wealth inputs plausibly deliver about 1.7×, measured as `genua` becoming a co-sink at ×1.720. | REMOVED | MODEL | numerical test | v5 L897-899 |
| Y916 | A spice sink at any of the four Chinese trade nodes needs 3.6-4.9×, i.e. 9.3-21.4% of all world spice demand at one node: `beijing` 3.60× / 9.3%, `hangzhou` 3.83× / 21.4%, `xian` 4.59× / 12.3%, `canton` 4.86× / 17.8%. | REMOVED | MODEL | numerical test | v5 L899-904 |
| Y917 | The four China-region nodes outside that set — `girin`, `yumen`, `chengdu`, `lhasa` — need 4.0× to 10.8×. | REMOVED | MODEL | numerical test | v5 L903-904 |
| Y918 | v2's "1.7× where 4-5× is needed" compressed two different thresholds into one comparison. | REMOVED | MODEL | algebraic derivation | v5 L905-906 |
| Y919 | The one place the node indexing is load-bearing is the fallback branch, where the candidates are typically all zero-wealth and tied, and §2.4 item 1 makes a canonical node order a correctness requirement for that reason. | REMOVED | MODEL | algebraic derivation | v5 L951-955 |

## §3.3 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y920 | `cape_of_good_hope` has 19 land provinces, stated without the `sea_starts` explanation. | REMOVED | INSTALL | read from a file | v5 L963-965 |

## §3.4 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y921 | In v1 substituting production income collapsed orientation agreement from 159/159 to 68/159. | REMOVED | MODEL | numerical test | v5 L1002-1004 |

## §3.5 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y922 | All 161 `change_price` blocks were parsed. | REMOVED | INSTALL | read from a file | v5 L1021-1024 |
| Y923 | v4.0 said 154 and 7 because its parser silently recovered nothing from five mission files, which a bare `except` hid, so the scan is now guarded by a per-file count assertion, and the seven recovered blocks are all positive with the partition unchanged. | REMOVED | MODEL | read from a file (v4.0's toolchain) | v5 L1024-1027 |
| Y924 | 1.875 is the figure a campaign reaching 1540 holds. | REMOVED | INSTALL | read from a file | v5 L1028-1031 |

## §3.8 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y925 | 92.2% (5825 of 6320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. | REMOVED | MODEL | numerical test | v5 L1094 |

## §3.9 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y926 | `genua`, `gulf_of_siam` and `sevilla` rank 3rd, 2nd and 7th by node wealth on the corrected field at 296.0, 299.2 and 266.5 against `english_channel`'s 316.6, and none of them is a sink. | REMOVED | MODEL | numerical test | v5 L1101-1105 |
| Y927 | `Φ_ord` remains the most self-coherent aggregate measured, at 60.3% edge-good agreement with the per-good graphs against `Φ_w`'s 52.5% (51.5% value-weighted). | REMOVED | MODEL | numerical test | v5 L1114-1117 |
| Y928 | Of `Φ_ord`'s 13 end nodes at 1444, 8 terminate no good at all and none of the demand capitals is among them. | REMOVED | MODEL | numerical test | v5 L1118-1120 |
| Y929 | `Φ_ord`'s end count never concentrates: 11-17 ends measured across cloves-α 2 to 64, never approaching vanilla's three. | REMOVED | MODEL | numerical test | v5 L1120-1122 |
| Y930 | v2 called that "α-invariant … 9-17 ends", which is neither the right word for a quantity ranging 11-17 nor a band containing its own baseline of 13. | REMOVED | MODEL | read from a file (the prior spec version) | v5 L1122-1124 |
| Y931 | Self-coherence was traded for legible, wealth-anchored, world-responsive ends. | REMOVED | DESIGN | stipulated | v5 L1124-1125 |
| Y932 | On the corrected wealth field there is one end, in China, matching none of vanilla's three, so the two-vanilla-like-ends premise is withdrawn. | REMOVED | MODEL | numerical test | v5 L1131-1133 |
| Y933 | The trade is 7.8 points of self-coherence given up for one operator and world-responsive ends, and the 1444 count is whatever the field gives. | REMOVED | MODEL | numerical test | v5 L1133-1135 |

## §3.10 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y934 | The two income forms agree to at most one unit in the last place. | REMOVED | MODEL | numerical test | v5 L1147 |
| Y935 | Propagation cannot be made per good. | REMOVED | MODEL | algebraic derivation | v5 L1149 |
| Y936 | Per-good propagation destroys the income identity, because §1.9 reads a node's downstream neighbours and those differ per good. | REMOVED | MODEL | algebraic derivation | v5 L1149 |
| Y937 | The driver is not how many distinct downstream sets a node has but whether its collectors hold differing power across the nodes those sets differ on. | REMOVED | MODEL | numerical test | v5 L1149 |
| Y938 | `gulf_of_siam` has eight distinct downstream sets and still shows a 0.003% effect, because its collectors hold almost nothing in `burma`, `canton` or `malacca` and every propagation term is near zero. | REMOVED | MODEL | numerical test | v5 L1149 |
| Y939 | Per-good propagation's error is redistributive and single-digit percent with the sign varying by collector: Sevilla -0.82%, -0.87%, +7.44%; Champagne -1.69%, +1.69%, +1.53%; Genoa -0.23%, -0.22%, +0.70%. | REMOVED | MODEL | numerical test | v5 L1149 |
| Y940 | That error is thirteen orders of magnitude above the float residual and it moves income between countries. | REMOVED | MODEL | numerical test | v5 L1149 |
| Y941 | Keeping propagation on a single graph is load-bearing for Goal 7 rather than merely convenient. | REMOVED | DESIGN | algebraic derivation | v5 L1149 |
| Y942 | The largest local trade value of any node in the model is 112.6. | REMOVED | MODEL | numerical test | v5 L1149 |
| Y943 | v4.0's 0.41% replacement figure was an artifact of freezing one term at the alphabetically first commodity. | REMOVED | MODEL | read from a file (v4.0's construction) | v5 L1149 |

## §3.13 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y944 | The open wealth question is what else multiplies `goods_produced` and which side of the owner line each source falls on. | REMOVED | DESIGN | stipulated | v5 L1183-1184 |
| Y945 | §1.3's classification handles the sources observed so far: the owner's `global_trade_goods_size_modifier` (out, country-scoped) and `bonus_from_merchant_republics` (out, its value set by neighbouring countries' government forms). | REMOVED | INSTALL | read from a file | v5 L1184-1187 |
| Y946 | Fifteen 1444 provinces carry a flat `trade_goods_size`, five from great projects and ten from permanent province modifiers. | REMOVED | INSTALL | read from a file | v5 L1187-1189 |
| Y947 | `trade_goods_size` and `trade_goods_size_modifier` appear in buildings, estate privileges, government reforms, church aspects, fervor, ages and event modifiers. | REMOVED | INSTALL | read from a file | v5 L1189-1192 |
| Y948 | The settling work is to enumerate every source of both keys and classify each, and the model needs the answer only for sources that can be live with no owner input. | REMOVED | DESIGN | stipulated | v5 L1192-1193 |
| Y949 | Deccan, demand rank 2 under α = 16 with the rank-1 demander `hangzhou` acting as a transit node, becomes the cloves sink. | REMOVED | MODEL | numerical test | v5 L1199-1201 |
| Y950 | `hangzhou`'s richest province is 30.4 against Beijing's 19.5, and under the calibration Beijing is only demand rank 3. | REMOVED | MODEL | numerical test | v5 L1201-1203 |

## §3.15 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y951 | With v1's ε floor removed the contrasts run 4-97 on supply against 211-20,400 on demand across the 29 goods. | REMOVED | MODEL | numerical test | v5 L1224-1227 |
| Y952 | Ranked orientation's alignment statistics: rho_val +0.281 against DRAIN's +0.054, and 43.8% of top-decile nodes are sinks against 14.5%. | REMOVED | MODEL | numerical test | v5 L1233-1235 |
| Y953 | Ranked orientation reaches 83.0% of demand with 31 orphan sinks. | REMOVED | MODEL | numerical test | v5 L1235-1237 |
| Y954 | Ranked orientation posts 8 net-producer sinks where DRAIN, LAP and FLOW all post zero. | REMOVED | MODEL | numerical test | v5 L1237-1238 |
| Y955 | Ranked orientation keeps 10-16 sinks per good against DRAIN's 1-7. | REMOVED | MODEL | numerical test | v5 L1238-1239 |
| Y956 | Seeded basin growth reaches 88.4% at its best tuning. | REMOVED | MODEL | numerical test | v5 L1241-1243 |
| Y957 | `Φ_ord` is retained as the measured coherence ceiling any future aggregate should be compared against, and that ceiling is 60.3% rather than the 62.7% v2.0 and v2.1 both quoted. | REMOVED | MODEL | numerical test | v5 L1252-1257 |
| Y958 | No parameter steers `Φ_ord`'s end count. | REMOVED | MODEL | algebraic derivation | v5 L1254-1255 |
| Y959 | The 3-mass gravity field hits any chosen end count exactly for γ no greater than 0.7 and any count up to six, and at γ = 0.9 the four-, five- and six-mass fields all collapse to three ends. | REMOVED | MODEL | numerical test | v5 L1259-1263 |
| Y960 | The gravity field's best vanilla-arrow agreement is 61% (97 of 159 arrows) at γ = 0.90-0.95, with γ = 0.97 giving 93 and every larger γ worse. | REMOVED | MODEL | numerical test | v5 L1262-1264 |
| Y961 | v2.1 through v4.0 put the gravity field's best agreement at γ = 0.97 and said the five- and six-mass fields give four ends at γ = 0.9; on the corrected wealth field neither holds. | REMOVED | MODEL | numerical test | v5 L1264-1266 |
| Y962 | v2.0 and v2.1 both quoted 69% = 110 of 159 for the gravity field, which is not reached at any γ, and the count-follows-seeds behaviour reproduced while that figure did not. | REMOVED | MODEL | numerical test | v5 L1266-1268 |
| Y963 | A local wealth maximum survives every positive α, measured as at least 10 ends at α up to 16. | REMOVED | MODEL | numerical test | v5 L1271-1273 |

## §3.16 (v5) — REMOVED (no counterpart in v6.1)

| ID | Claim | Status | Type | Provenance | Locator |
|---|---|---|---|---|---|
| Y964 | Implemented as written, v1's ε left the α = 1 identity failing at 1e-5. | REMOVED | MODEL | numerical test | v5 L1370-1372 |

---

# Summary

**992 claims enumerated: `Y001`–`Y999` less the seven retired IDs** (no gaps closed, no number reused).
838 of them are live in v6.1; 154 are v5.0 propositions with no counterpart here.

### By status

| Status | Count |
|---|---|
| UNCHANGED | 566 |
| CHANGED | 142 |
| NEW | 130 |
| REMOVED | 154 |
| **Total** | **992** |

### By type

| Type | Count |
|---|---|
| MODEL | 493 |
| DESIGN | 215 |
| INSTALL | 124 |
| ENGINE | 97 |
| MATH | 63 |
| **Total** | **992** |

### By type and status

| Type | UNCHANGED | CHANGED | NEW | REMOVED | Total |
|---|---|---|---|---|---|
| MODEL | 224 | 95 | 71 | 103 | 493 |
| DESIGN | 153 | 23 | 25 | 14 | 215 |
| INSTALL | 56 | 13 | 24 | 31 | 124 |
| ENGINE | 82 | 6 | 3 | 6 | 97 |
| MATH | 51 | 5 | 7 | 0 | 63 |
| **Total** | **566** | **142** | **130** | **154** | **992** |

### By provenance

Grouped to the fixed vocabulary; the parenthetical qualifiers each row carries are kept in the
tables above and folded into their base category here. The five rows whose cell reads "cited to
`<document>`" are counted as `read from a file`, that document being the file cited.

| Provenance | Count |
|---|---|
| stipulated | 317 |
| algebraic derivation | 254 |
| numerical test | 190 |
| read from a file | 163 |
| engine test | 29 |
| measured in-game | 23 |
| computed by a named script | 13 |
| unsourced | 3 |
| **Total** | **992** |

`numerical test` and `engine test` are never merged: the 190 numerical tests are computations over
the model's own data (`measure6.py`, `relabel6.py`, `europe.py`, `epsilon6.py`, `toys.py`, and
unattributed counts of the same kind), the 29 engine tests are observations of the running game
(the cyclic-file crash, the reversed-link load, probes 13–15, the null-run variance), and the 23
`measured in-game` rows are tooltip and window readings.

### ID carry-over

| | Count |
|---|---|
| Round-9 IDs (`Y001`–`Y964`) still attached to the same proposition | 957 |
| of those, live in v6.1 | 803 |
| of those, `REMOVED` (v5.0 propositions, unchanged from round 9) | 154 |
| Round-9 IDs retired — proposition no longer in the document | 7 |
| New IDs issued (`Y965`–`Y999`) | 35 |
| **Rows in this census** | **992** |

The seven retired IDs, all round-9 propositions v6.1 deleted rather than restated:

| ID | What it said | Why it is gone |
|---|---|---|
| Y014 | `verify6.py` pins 35 distinct figures across 29 checks | §0 now declines to give a count at all (Y974, Y975) |
| Y088 | after `english_channel` the most frequent end-holders are `gulf_of_siam`, `wien`, `rheinland`, `sevilla`, count 1 to 5 | the relabelling distribution is gone; the installed sink set no longer moves under relabelling |
| Y089 | across three 800-trial sets `hangzhou` 784-789, `english_channel` 322-336, `sevilla` 79-117, `rheinland` 112-136 | same |
| Y090 | the two leading proportions are quoted to two figures and the trailing ones qualitatively | same — there are no proportions left to qualify |
| Y092 | no basin figure is quoted anywhere in §1.6 | §1.6 no longer discusses drainage-basin size |
| Y101 | scanned over [1, 8] the widest sink-count band is 1.71 wide at [3.50, 5.21], and 1.5's is not the widest | the band-width argument is withdrawn (Y479); §1.6 quotes only the band containing the chosen value (Y103) |
| Y142 | twenty-five flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event | there are no relabelling flips left to compare |

Round 9 retired nothing; this is the first inventory of this version to retire an ID. No ID changed
which proposition it points at.

### The 35 new IDs

`Y965`–`Y975` (§0) record v6.1's own change note — the two things it changes, the tie-break, the
`α_Φ` move to 2.0, the hyperparameter framing, the new 1444 sink set, the 29-of-59 figure churn, and
the three sentences that replaced the withdrawn `verify6.py` count. `Y976`–`Y978` (§1.1) are the
Phase-2 cost formula, why it is not unit, and the `TIE_EPS = 1e-3` bound on the fewest-hop
approximation. `Y979`–`Y985` (§1.3) are the `unrest` exclusion and its cost. `Y986`–`Y994` (§1.6) are
the tie-break's measurements, the two cautions about the relabelling instrument, the per-good
carve-out, the `TIE_EPS` band, `V_g`'s order-independence, and `english_channel`'s two-hop drain to
`genua`. `Y995` (§2.1) is the desync exposure the tie-break closes and what it leaves.
`Y996`–`Y998` (§2.3) are the cost's definition and load-bearing properties, its use in every solve,
and why one cost vector does not make every solve unique. `Y999` (§2.4) is the rejected second
wealth term.

### Which v5.0 claims are gone

154 v5.0 propositions have no counterpart in v6.1 — the same 154 round 9 found, filed under a `(v5)`
section marker. v6.1's edits removed no further v5.0 proposition: every v5.0 claim v6.0 had kept and
v6.1 rewrote is recorded here as `CHANGED`, not `REMOVED` (the Phase-2 arc costs Y232, the
no-directed-cycle argument Y236, the fewest-hop property Y263, `α_Φ`'s value Y326, the scale
measurements Y081–Y082, the `devastation` scaling law Y054, the `±1%` noise result Y656, and the
any-good connectivity figure Y681, among others). Where they fall:

| v5.0 section | REMOVED | What went |
|---|---|---|
| §0 | 3 | the whole-install classification as v5.0's headline change, and the "no figure is unverified" claim |
| §1.1 | 7 | the `b == 0` characterisation of the fallback branch, the zero-wealth-tie reason for a canonical node order, and the 1-7 / mean 3.6 sink counts |
| §1.3 | 38 | the entire two-test modifier classifier and its table — gems, incense, great projects, permanent modifiers, centres of trade, buildings, terrain/climate, `production_leader`, `bonus_from_merchant_republics` — plus the Leviathan DLC conditionality and the `is_city` filter |
| §1.5 | 2 | the 29-of-159 coal flip count and "highest in vanilla" for coal's price |
| §1.6 | 33 | the one-sink 1444 result, the four-row `α_Φ` band table and its noise analysis, the widest-band retention argument, the 2% European threshold, the Lowlands result, and the doab/Hansa/Cape routes |
| §1.10 | 2 | "almost nothing absorbs threshold chatter" and the 8.6-32.0% caravan share under the pre-grant description |
| §2.2 | 4 | the local-modifier terms in the solver formula, the 16-extra-province list, world wealth 10,677.50 over 2,452 provinces, and the 0.17-0.21 s timing |
| §2.2a | 1 | "peeling does not touch the priority key" |
| §2.3 | 3 | both coefficients hardcoded in the binary, and the widest-band retention of `α_Φ` |
| §2.4 | 3 | the tiebreak reason for a canonical node order, the two-maps-from-one-world consequence, and the one-end 1444 file |
| §2.7 | 1 | "correct as written and gains no qualifier" for probe 15 |
| §2.8 | 6 | the one-sink razed-China baseline, the `c_w` rank gap, and the 51.5 / 52.5% agreement pair |
| §3.2 | 6 | the 36-against-482.2 contrast figures, the ×1.720 co-sink figure, the demand-percentage column on the Chinese-sink multiples, and chengdu/lhasa |
| §3.3 | 1 | the bare 19-land-province statement without the `sea_starts` explanation |
| §3.4 | 1 | the 159/159 to 68/159 collapse figure |
| §3.5 | 3 | "all 161 blocks were parsed", the per-file count assertion, and 1.875 as the campaign figure |
| §3.8 | 1 | the 92.2% (5825 of 6320) any-good connectivity figure |
| §3.9 | 8 | every `Φ_ord` figure (60.3%, 13 ends, 8 terminating none, 11-17 across cloves-α) and the 7.8-point trade |
| §3.10 | 10 | "propagation cannot be made per good" and every magnitude attached to it — the 0.003% gulf_of_siam effect, the per-collector percentages, and the 112.6 largest node value |
| §3.13 | 7 | the classification framing of the open question, the fifteen flat-bonus provinces, and the Deccan/30.4-vs-19.5 calibration figures |
| §3.15 | 13 | every maintained figure in the graveyard — the 4-97 / 211-20,400 contrasts, RANK's alignment and delivery numbers, the basins' 88.4%, `Φ_ord`'s coherence ceiling, and the gravity kernel's γ table |
| §3.16 | 1 | the bare "failed at 1e-5" without the ε = 1e-6 comparison |
| **Total** | **154** | |

### Where v6.1's edits land

For orientation only — the diff, not a judgement. Of the 65 v5→v6.1 diff groups, 33 were already
present in v6.0; the rest are v6.1's. The sections v6.1 touched, by row count affected:

| Section | Rows CHANGED or NEW by v6.1's own edits | What moved |
|---|---|---|
| §0 | 12 | the v6.1 change note; the `verify6.py` coverage paragraph |
| §1.1 | 6 | Phase-2 arc costs; the no-directed-cycle argument; the fewest-hop property; the 2–8 / mean 3.69 sink counts |
| §1.3 | 10 | the `unrest` exclusion block; `devastation`'s scaling law sourced to the wiki; the 4-of-159 edge figure |
| §1.5 | 3 | 16 of 159 coal flips; "moves no additional edge" |
| §1.6 | 30 | the whole relabelling argument inverted; `α_Φ = 2.0`; the ten-row Europe table; the sink set, sources, agreement and route figures |
| §2.1 | 1 | the desync paragraph |
| §2.2 | 1 | four of five condition modifiers applied |
| §2.3 | 6 | `α_Φ = 2.0` and `TIE_EPS`; the cost definition; the per-solve scope; the uniqueness limit |
| §2.4 | 12 | item 1 rewritten around the tie-break; item 2's end list now world-determined |
| §2.8 | 6 | the razed-China row; the barbell percentages; the latent-good and disagreement figures |
| §3.3 | 1 | the `α_Φ = 2.0` slicing comparison |
| §3.6 | 2 | the ±1% noise result; where degeneracy still bites |
| §3.8 | 1 | 90.5% any-good connectivity |
| §3.9 | 4 | the wealth-rank paragraph; `Φ_ord`'s relabelling behaviour |
