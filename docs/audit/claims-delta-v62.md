# Claims Delta — Per-Good Trade Network Spec v6.1 → v6.2

**Current document:** `per-good-trade-spec.md`, 2,079 lines, MD5 `5ec633ef46e7fd68bb118e10e83692eb` (v6.2).
**Compared against:** `claims-v6.md` — the twelfth census, taken of the document at 1,979 lines, MD5
`59c84a97799db9db97fe889b6e3c6776` (v6.1; byte-identical to `per-good-trade-spec-v6.1-frozen.md`).
`round6.diff` (frozen → current, 44 hunks) was used as the textual diff; every classification below is
against the actual old and new text, not the census's paraphrases. Enumeration and classification only:
nothing here is graded or checked for truth.

**ID range found:** `Y001`–`Y1057`, 1,049 rows, every number used exactly once except the eight retired
IDs (`Y014`, `Y088`, `Y089`, `Y090`, `Y092`, `Y101`, `Y142`, `Y145`), which stay retired. Of the 1,049
rows, 894 were live against v6.1 and 155 were already `REMOVED` when the census was written (the census's
own status column is measured against v5.0; it is not carried into the status column below, which is
measured v6.1 → v6.2).

**First new ID assigned:** `Y1058` (new propositions run `Y1058`–`Y1141`, in document order).

**Counts:**

| status | rows |
|---|---|
| UNCHANGED | 809 |
| REWORDED | 20 |
| CHANGED | 46 |
| REMOVED — by this edit (v6.1 → v6.2) | 19 |
| REMOVED — carried (already removed when the census was written) | 155 |
| NEW | 84 |
| **total rows** | **1133** |

**Notes.** (1) A carried ID keeps its number even where the wording, the figure or the section moved
(`Y737` stays on §3.13's tolerance entry through its closure; `Y082`'s figure lost its §1.6 Scale-paragraph
statement but survives verbatim at L580, so it is UNCHANGED, not REMOVED). (2) The front-matter version
line moved 6.1 → 6.2; the census carried no row for it and none is added. (3) `Line` is the line in the
current document where the claim (or its anchor sentence) now sits; `—` for REMOVED. (4) Type vocabulary
is this delta's five-way one (ENGINE / MODEL / MEASURED / DESIGN / PROCESS); the census's extended
vocabulary (MATH, INSTALL, …) is mapped onto it, so a type differing from the census row is a
re-classification of the same claim, not a change in the claim.


## UNCHANGED — still asserted, in substance and in figure (compressed)

| ID | § | claim (label) | type | line |
|---|---|---|---|---|
| Y207 | §0 | The target build is EU4 1.37.5 Inca. | DESIGN | 5 |
| Y208 | §0 | The design is extended-timeline compatible. | DESIGN | 5 |
| Y209 | §0 | The design targets connected maps only. | DESIGN | 5 |
| Y210 | §0 | This document supersedes v1.3, which lives in `../v1-laplacian/`. | PROCESS | 6 |
| Y211 | §0 | v1 oriented each good by a Laplacian potential. | MODEL | 6 |
| Y212 | §0 | v1's sink placement was shown to be topological rather than economic. | MODEL | 7 |
| Y213 | §0 | A four-operator bake-off replaced the orientation core with the DRAIN algorithm. | MODEL | 8 |
| Y214 | §0 | Every claim-audit correction from `../v1-laplacian/validation.md` that is settleable from files is folded … | PROCESS | 9 |
| Y216 | §0 | This version keeps v3.0's owner-agnostic wealth. | DESIGN | 13 |
| Y001 | §0 | v6.0 makes owner-agnosticism true by construction rather than by a rule that has to be policed. | DESIGN | 13 |
| Y002 | §0 | The substantive change of v6.0 is to §1.3: wealth is a function of the province's development, its trade good … | DESIGN | 14 |
| Y003 | §0 | The two-test modifier classifier and everything it governed — trade-good modifiers, great projects, permanent … | DESIGN | 15 |
| Y004 | §0 | The two-test classifier is v4.0's; v3.0 used a structural rule about which block of a trade-good definition a … | MODEL | 18 |
| Y005 | §0 | On the 1444 start the deleted apparatus was worth 105.30 ducats — 0.98% of the 10,712.70 the field totalled … | MEASURED | 20 |
| Y006 | §0 | That classification was wrong in both independent audits that examined it … | PROCESS | 21 |
| Y007 | §0 | Three start-state reads are corrected in the same pass: `on_startup` devastation, dated `add_base_*` … | DESIGN | 24 |
| Y965 | §0 | v6.1 changes the operator, not the field. | DESIGN | 27 |
| Y008 | §0 | Phase 2's min-cost flow is degenerate under unit arc costs, so presentation order selected which optimum was … | MEASURED | 27 |
| Y966 | §0 | §2.3 now breaks that tie inside the objective, in two terms — one carrying the design intent, one generic. | MODEL | 28 |
| Y1000 | §0 | §2.3 also pins the solver's optimality tolerance, which turned out to be a correctness requirement rather … | MODEL | 29 |
| Y1001 | §0 | The margin by which the tie-break makes the optimum unique is as small as 3.8e-8 while HiGHS's default … | MEASURED | 31 |
| Y967 | §0 | With all three changes in place the orientation is unchanged across every relabelling tried — 0 of 180 on the … | MEASURED | 32 |
| Y1002 | §0 | The orientation is also unchanged under permutation of the LP's column order. | MODEL | 35 |
| Y968 | §0 | A canonical node order remains an emitter requirement because the order-invariance is a measurement rather … | MODEL | 35 |
| Y969 | §0 | `α_Φ` moves from 1.5 to 2.0. | MODEL | 38 |
| Y970 | §0 | `α_Φ`, `TIE_EPS` and `TIE_EPS2` are hyperparameters whose values are developer taste, and §2.3 states them … | DESIGN | 38 |
| Y971 | §0 | Every derivation previously offered for `α_Φ` is withdrawn without replacement. | MODEL | 40 |
| Y972 | §0 | The 1444 sink set moves from `{english_channel, hangzhou}` to `{genua, hangzhou}`. | MEASURED | 40 |
| Y1003 | §0 | §2.1 records what multiplayer would additionally need, which is now build discipline rather than a design … | MODEL | 46 |
| Y009 | §0 | Prose convention: no empirical absolutes — no superlative, no universal quantifier and no threshold asserted … | DESIGN | 65 |
| Y011 | §0 | Those rejected-operator numbers were re-measured and re-refuted in three successive audits, and not one of … | PROCESS | 70 |
| Y220 | §0 | Where a comparison is genuinely load-bearing it is stated as a direction rather than as a figure that has to … | DESIGN | 71 |
| Y218 | §0 | Deleted text is quoted in `changes-v6.md`. | PROCESS | 81 |
| Y217 | §0 | Measured figures carry the script that produced them. | DESIGN | 81 |
| Y013 | §0 | `scripts/verify6.py` reads figures out of the document text and fails when they disagree with a value … | PROCESS | 81 |
| Y974 | §0 | `verify6.py`'s coverage of the figures this document prints is partial. | PROCESS | 84 |
| Y1051 | §0 | Neither a count nor a proportion of that coverage is given here, for two different reasons, and "partial" is … | DESIGN | 85 |
| Y975 | §0 | No count is given here because some of the harness's checks are generated per matching phrase, so the total … | PROCESS | 86 |
| Y015 | §0 | No coverage proportion is offered because the denominator is not well defined: counting "the figures the spec … | PROCESS | 88 |
| Y1052 | §0 | An earlier draft of this paragraph asserted "well under half" two sentences before refusing to give a ratio, … | PROCESS | 90 |
| Y016 | §0 | `scripts/coverage6.py` is the honest measure — it corrupts each spec-printed figure whether the harness looks … | PROCESS | 91 |
| Y018 | §0 | `scripts/mutate6.py` reports a higher score that should not be read as coverage: it plants errors only in … | PROCESS | 97 |
| Y219 | §0 | The document has three sections: §1 Mechanics states what the system does, §2 Implementation states how it is … | DESIGN | 101 |
| Y221 | §1.1 | Every trade good has its own directed network over the same adjacency. | MODEL | 109 |
| Y222 | §1.1 | Direction is computed, never authored. | DESIGN | 109 |
| Y223 | §1.1 | For each good `g` the balance is `b_g(n) = s_g(n) − c_g(n)`, oriented by DRAIN in four named phases: peel, … | MODEL | 111 |
| Y225 | §1.1 | Phase 0 is exact rather than heuristic: every removed edge is a bridge and flow on a tree is determined by … | MODEL | 116 |
| Y226 | §1.1 | On the vanilla map Phase 0 is a no-op — minimum degree 2, zero bridges. | MEASURED | 117 |
| Y227 | §1.1 | Phase 0 exists for modded maps. | DESIGN | 118 |
| Y228 | §1.1 | Phase 1 takes the connected clusters of net demanders in the core, computes the Herfindahl index of their … | MODEL | 120 |
| Y230 | §1.1 | On vanilla 1444 demand is so ubiquitous that k = 1 for 27 of 29 goods at the default knobs. | MEASURED | 123 |
| Y231 | §1.1 | Phase 1's selection is deliberately weak because Phase 3 self-corrects upward. | DESIGN | 124 |
| Y232 | §1.1 | Phase 2 solves the uncapacitated min-cost flow serving `b_g` and orients every support edge by its net flow. | MODEL | 130 |
| Y976 | §1.1 | Phase 2's arc costs are near-unit, symmetric in the arc, and read from node wealth: a first-order term … | MODEL | 130 |
| Y977 | §1.1 | The costs are not unit because with unit costs the optimum is not unique and which one the solver returns … | MODEL | 133 |
| Y233 | §1.1 | The support is a spanning-tree basis of at most N−1 edges when the solver returns a basic (vertex) optimum, … | MODEL | 135 |
| Y234 | §1.1 | An interior-point solve without crossover can split flow across equal-length parallel paths and return a … | MODEL | 136 |
| Y235 | §1.1 | §2.2 therefore requires network simplex or a simplex LP. | DESIGN | 138 |
| Y1004 | §1.1 | §2.3 additionally requires the solver's optimality tolerance to be tighter than the margin the tie-break … | MODEL | 138 |
| Y236 | §1.1 | For any optimum the support contains no directed cycle, because with all costs strictly positive a directed … | MODEL | 140 |
| Y237 | §1.1 | Edges with zero net flow are free and are deferred to Phase 3. | MODEL | 143 |
| Y238 | §1.1 | Phase 3 marks nodes Kahn-style: a node is ready when every flow out-neighbour is already marked and it is a … | MODEL | 145 |
| Y239 | §1.1 | Among ready nodes the sweep pops by the priority key (DEF ascending, b ascending, index), where `DEF(v)` is … | MODEL | 147 |
| Y240 | §1.1 | The flow-arc subgraph is acyclic and fixed before any free edge, so `DEF` involves no circularity. | MODEL | 148 |
| Y241 | §1.1 | On a stall the sweep promotes the heaviest flow-terminal demander among the candidates into the sink set, and … | MODEL | 149 |
| Y242 | §1.1 | If the candidates hold no flow-terminal demander at all, the fallback branch promotes the highest-wealth … | MODEL | 151 |
| Y243 | §1.1 | Node wealth is a good-independent input, so the fallback branch needs no bootstrap. | MODEL | 152 |
| Y244 | §1.1 | Candidates at a stall are the unmarked nodes whose flow out-neighbours are all marked; because the flow … | MODEL | 153 |
| Y245 | §1.1 | A candidate carrying any flow out-arc is already ready, and a candidate with inflow is a flow-terminal … | MODEL | 155 |
| Y019 | §1.1 | The fallback branch fires only when every candidate is support-isolated with zero post-peel balance. | MODEL | 157 |
| Y020 | §1.1 | The balance the priority key reads is the one Phase 0 hands on, with each pendant's balance folded into its … | MODEL | 158 |
| Y021 | §1.1 | On a connected core the fallback needs the folded balance to vanish across the core: for a per-good graph … | MODEL | 160 |
| Y022 | §1.1 | Nodes hold between 0 and 72 counted provinces, so equal per-province wealth makes unequal node sums. | MEASURED | 163 |
| Y023 | §1.1 | Where the wealth key ties, the node index decides. | MODEL | 164 |
| Y024 | §1.1 | §2.8's containment set includes the fallbacks because of T3 — a fallback promotion that is a sink in neither … | DESIGN | 165 |
| Y246 | §1.1 | Free edges orient from later-marked to earlier-marked. | MODEL | 168 |
| Y248 | §1.1 | Each §1.1 property is labelled proved, measured, or true-by-construction, and the three are never allowed to … | DESIGN | 175 |
| Y250 | §1.1 | The §1.1 property measurements were regenerated for v6.0 by `measure6.py`. | MEASURED | 176 |
| Y249 | §1.1 | That labelling discipline caught four over-claims between v2.0 and v3.0. | MODEL | 179 |
| Y251 | §1.1 | Global DAG: every arc points from later-marked to earlier-marked, so reversed marking order is a topological … | MODEL | 182 |
| Y252 | §1.1 | Measured acyclic on 29 of 29 goods. | MEASURED | 183 |
| Y253 | §1.1 | Every sink is one of four kinds: a selected demand centre that turned out flow-terminal, a stall-promoted … | MODEL | 185 |
| Y025 | §1.1 | On 1444 the fallback and pendant cases are empty and the sink set is exactly `{selected ∩ flow-terminal} ∪ … | MEASURED | 187 |
| Y026 | §1.1 | That equality is a measurement on this input rather than a theorem, and v2 asserted it as one. | MODEL | 189 |
| Y027 | §1.1 | It does not become a theorem by attaching conditions: "Phase 0 a no-op and no fallback firing" looks … | MODEL | 191 |
| Y254 | §1.1 | Three constructed cases break the sink-set equality: a pendant net-importing leaf is a sink outside the set … | MEASURED | 192 |
| Y255 | §1.1 | A node with no outgoing links for `g` is a sink for `g`; sinks differ per good; there is no global end node. | MODEL | 195 |
| Y256 | §1.1 | The orientation contains a flow serving 100% of every good's demand, because the LP imposes node balance and … | MODEL | 197 |
| Y257 | §1.1 | The premise that makes the LP feasible is connectedness: on a disconnected map the balance must hold per … | MODEL | 199 |
| Y258 | §1.1 | §2.2 states the connectedness requirement and what the solver does when it is violated. | MODEL | 202 |
| Y259 | §1.1 | Measured on 1444, which is one component: 100.0% of demand reachable from supply, 29/29 goods, zero orphan … | MEASURED | 203 |
| Y260 | §1.1 | Ready-marking is a monotone closure, so the stall sequence and both promotion branches are provably … | MODEL | 205 |
| Y261 | §1.1 | Free-edge direction is deterministic, by the same closure argument plus the priority key's index tiebreak. | MODEL | 205 |
| Y1005 | §1.1 | Measured: zero exact `(DEF, b)` key collisions across all 2,320 core nodes of the 29 per-good solves — not … | MEASURED | 210 |
| Y1006 | §1.1 | Phase 1's within-cluster argmin and its top-k cluster cut are untied on the same field, so no index tiebreak … | MEASURED | 212 |
| Y263 | §1.1 | The certificate flow is a near-fewest-hop routing in aggregate: with unit costs the objective would be … | MODEL | 218 |
| Y264 | §1.1 | No per-unit shortest-path claim is made and none holds, because a unit may detour when sink assignment … | MODEL | 225 |
| Y265 | §1.1 | The efficiency property carries no measurement and wants none: it follows from the construction of the LP, … | DESIGN | 228 |
| Y266 | §1.1 | The §3.13 calibration deliberately degrades efficiency, which is a change to the program being solved rather … | DESIGN | 229 |
| Y267 | §1.1 | The orientation is recomputed on a fixed monthly tick, aligned to the vanilla trade tick. | MODEL | 233 |
| Y268 | §1.1 | Orientation is read from the current solve every time, with no memory of the previous one. | MODEL | 233 |
| Y270 | §1.1 | Across machines LP determinism is the open question of §3.13. | DESIGN | 237 |
| Y271 | §1.2 | `s(n,g) = goods_produced(n,g)` over the world sum of `goods_produced(m,g)`. | MODEL | 243 |
| Y272 | §1.2 | `goods_produced` is a physical quantity — pre-production-efficiency and pre-autonomy. | MODEL | 246 |
| Y273 | §1.2 | `goods_produced` moves with devastation, occupation and prosperity, because `00_static_modifiers.txt`'s … | ENGINE | 246 |
| Y274 | §1.2 | There is no regularizer: v1 mixed in `s ← (1 − ε)·s + ε/N` to keep dead branches from being oriented by … | MODEL | 248 |
| Y275 | §1.2 | DRAIN's free edges are oriented combinatorially by the drainage sweep rather than by comparing near-equal … | MODEL | 249 |
| Y276 | §1.2 | One node has `b = 0` exactly at 1444 — `cape_of_good_hope` — and it is handled as an ordinary conduit. | MEASURED | 250 |
| Y277 | §1.3 | Demand is assembled per province, then summed to the node. | MODEL | 255 |
| Y028 | §1.3 | Wealth is owner-agnostic and reads three things about the province: its development, its trade good, and its … | MODEL | 257 |
| Y278 | §1.3 | Wealth is a property of the place — what the land is worth per year, before anyone's government touches it. | DESIGN | 258 |
| Y029 | §1.3 | Two provinces with the same development, trade good and condition have the same wealth whoever owns them. | MODEL | 260 |
| Y280 | §1.3 | A province's wealth does not change when it is conquered. | MODEL | 262 |
| Y030 | §1.3 | Owner-agnosticism is true by construction rather than by a policed rule; v3.0 through v5.0 stated the … | DESIGN | 264 |
| Y031 | §1.3 | `base_tax`, `base_production` and the trade good are bare attributes of the place, so nothing about them … | MODEL | 268 |
| Y032 | §1.3 | What the change gives up: `gems`' `local_tax_modifier` and `incense`' `trade_value_modifier` are genuinely … | DESIGN | 269 |
| Y033 | §1.3 | The dropped apparatus was live on 89 of the 2,472 counted provinces — 43 `gems` plus 31 `incense` plus 16 … | ENGINE | 274 |
| Y034 | §1.3 | That count depends on the field: it is 87 under the withdrawn `is_city` filter, and 89 rather than 88 because … | ENGINE | 275 |
| Y281 | §1.3 | The model trades that fidelity for an input surface with no classification question in it. | DESIGN | 283 |
| Y035 | §1.3 | `goods_produced(p) = GP_COEFF · base_production(p) · (1 + sum of province-state goods modifiers)`, with no … | MODEL | 286 |
| Y036 | §1.3 | `trade_value(p) = goods_produced(p) · price(good(p))` in ducats per year, with no trade-value modifier term. | MODEL | 287 |
| Y282 | §1.3 | `wealth(p) = tax_value(p) + trade_value(p)`, in ducats per year. | MODEL | 289 |
| Y283 | §1.3 | `c(n,g)` is the node's share of world wealth raised to `α(g)`: the sum over provinces in the node of … | MODEL | 291 |
| Y284 | §1.3 | `GP_COEFF` and `TAX_COEFF` have different provenance from one another. | DESIGN | 294 |
| Y038 | §1.3 | `GP_COEFF` is a shipped file value: `common/static_modifiers/00_static_modifiers.txt` carries … | ENGINE | 294 |
| Y039 | §1.3 | `GP_COEFF` is therefore moddable and is read at runtime rather than hardcoded. | DESIGN | 298 |
| Y040 | §1.3 | `TAX_COEFF` is in no file that has been found — not `defines.lua`, not `common/defines/`, not that … | ENGINE | 298 |
| Y285 | §1.3 | The tax and trade terms share a time basis and are safe to add, because the engine's own province tooltips … | ENGINE | 302 |
| Y041 | §1.3 | The tax tooltip's schema is `Base: trunc(base_tax × 0.0833333) (Yearly base_tax)`, observed as `Base: 0.49 … | ENGINE | 303 |
| Y042 | §1.3 | The parenthetical is `base_tax` itself and the `Base` line is its truncated twelfth; it is not twelve times … | ENGINE | 306 |
| Y043 | §1.3 | v4.0 and v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both of its own data points, and v3.0 … | PROCESS | 307 |
| Y044 | §1.3 | The monthly production tooltip's `Trade Value` line is consistent with the same relation on one observation, … | ENGINE | 308 |
| Y045 | §1.3 | Both monthly figures being the annual value over twelve is what lets the annual forms add directly, and the … | MODEL | 310 |
| Y286 | §1.3 | The coefficients were measured on two provinces: Garnatah (223) with `base_tax` 6, `base_production` 4, silk … | ENGINE | 313 |
| Y287 | §1.3 | Only the tooltips' `Base` lines are used. | DESIGN | 314 |
| Y288 | §1.3 | A province window's `Trade Value` also carries the owner's `global_trade_goods_size_modifier`. | ENGINE | 315 |
| Y289 | §1.3 | Garnatah's window read 3.52 rather than 0.80 × 4.00 = 3.20 because Granada's 1444 monarch held the … | ENGINE | 316 |
| Y290 | §1.3 | Ruler personalities are rolled at game start wherever country history scripts none, so any window figure is … | ENGINE | 317 |
| Y291 | §1.3 | Modifiers apply after the coefficient, not before: the engine computes the base from development first and … | ENGINE | 321 |
| Y046 | §1.3 | Observed on Garnatah, `base_tax` 6 with `Tax Income Efficiency 125.0%` displays `Base 0.49` and then `0.62`; … | ENGINE | 322 |
| Y047 | §1.3 | The example establishes only the ordering — base from development first, percentage second — and nothing … | ENGINE | 325 |
| Y048 | §1.3 | v4.0 and v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires rounding while §2.3 requires … | PROCESS | 327 |
| Y049 | §1.3 | Flat goods bonuses would add into `goods_produced` before the price multiply — the goods-produced tooltip … | ENGINE | 328 |
| Y054 | §1.3 | `devastation`'s scaling law is the one row in the table not settled by a shipped file: … | ENGINE | 343 |
| Y059 | §1.3 | Eleven counted provinces begin devastated — Bohemia at 50, Erzgebirge and Moravia at 20 — and no … | ENGINE | 384 |
| Y060 | §1.3 | That devastation is applied by `on_startup`, which fires `flavor_boh.15` ("The Aftermath of the Hussite … | ENGINE | 385 |
| Y061 | §1.3 | The start devastation costs 13.40 ducats across the eleven affected counted provinces. | MEASURED | 386 |
| Y062 | §1.3 | The start state is what the engine produces rather than what the history files say, and that costs three … | DESIGN | 391 |
| Y063 | §1.3 | `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`, `flavor_geo.1` and others directly from its own … | ENGINE | 394 |
| Y064 | §1.3 | Development does not move before the first tick: on this start the history parse matches the save on 2,472 of … | ENGINE | 397 |
| Y065 | §1.3 | v6.0's first draft said `flavor_geo.1` carries `add_base_tax` and could move development pre-tick; it does … | ENGINE | 399 |
| Y066 | §1.3 | `add_base_*` in a dated block before the start date accumulates, and v5.0 and earlier overwrote instead of … | ENGINE | 403 |
| Y067 | §1.3 | `is_city = yes` is not a filter the engine applies: 20 owned provinces omit or comment out that line — … | ENGINE | 406 |
| Y068 | §1.3 | The model counts a province when it has an owner and lies in a trade node: 2,472 provinces, not 2,452. | DESIGN | 408 |
| Y069 | §1.3 | Twenty counted provinces have no trade good in their history file (`trade_goods = unknown`), and the engine … | ENGINE | 411 |
| Y070 | §1.3 | The model reads the good the engine actually rolled rather than predicting the draw, and pricing those … | DESIGN | 413 |
| Y071 | §1.3 | On this save the twenty came up seven `fur`, five `grain`, three `wool`, two `livestock`, and one each of … | ENGINE | 415 |
| Y293 | §1.3 | Everything the engine itemised on a real province that is not local is excluded: `Reform Iqta` (+5%, … | ENGINE | 420 |
| Y294 | §1.3 | `Core` (+75%) and `City` (+25%) are not excluded, because they are already inside `TAX_COEFF`. | MODEL | 424 |
| Y295 | §1.3 | The engine's tax multiplier is the sum of the itemised percentages: Garnatah's `Tax Income Efficiency: … | ENGINE | 425 |
| Y296 | §1.3 | A cored city province carrying nothing else sums to exactly 0.75 + 0.25 = 1.00 and yields `base_tax` ducats a … | ENGINE | 427 |
| Y072 | §1.3 | The model applies `TAX_COEFF = 1.0` to every province it counts: ownership is not modelled, so every province … | DESIGN | 429 |
| Y297 | §1.3 | Carrying either the `Core` or the `City` term again would double-count it. | MODEL | 430 |
| Y073 | §1.3 | That is a modelling choice with a known cost: two readings, both on cored city provinces at `base_tax` 2 and … | DESIGN | 431 |
| Y074 | §1.3 | `base_tax` at 1444 runs up to 15 (province 1821), with total development reaching 33 there. | ENGINE | 432 |
| Y298 | §1.3 | Unowned provinces are outside the model: `s` and `c` are computed over provinces that have an owner and lie … | DESIGN | 435 |
| Y299 | §1.3 | What owner-agnostic demand buys: demand stops responding to who rules and responds only to what is there, so … | DESIGN | 438 |
| Y075 | §1.3 | Owner-agnostic wealth also removes a large source of hidden owner-dependence from the aggregate graph of … | MODEL | 440 |
| Y300 | §1.4 | `α(g) = clamp((price(g)/P₀)^k, α_min, α_max)` with `P₀ = 2.0` ducats. | MODEL | 446 |
| Y301 | §1.4 | α > 1 makes demand superlinear in provincial wealth, so luxuries concentrate on individually rich provinces. | MODEL | 449 |
| Y302 | §1.4 | α = 1 makes demand proportional to economic size. | MODEL | 450 |
| Y303 | §1.4 | α < 1 makes demand sublinear, so bulk goods spread toward populous regions. | MODEL | 451 |
| Y304 | §1.4 | α moves with vanilla price events in both directions, with no smoothing. | MODEL | 453 |
| Y305 | §1.5 | Gold is excluded by configuration. | MODEL | 457 |
| Y306 | §1.5 | Gold-mine income is its own income category in the engine (`INCOMEGOLD`, `gold_income` as a distinct … | ENGINE | 457 |
| Y307 | §1.5 | Under owner-agnostic wealth the exclusion is stronger still: `wealth(p)` is built from `base_tax`, … | MODEL | 460 |
| Y308 | §1.5 | Gold is inert in vanilla trade value (`base_price = 0`, `goldtype = yes`), so the exclusion costs nothing. | ENGINE | 463 |
| Y310 | §1.5 | Any good with zero world production this month has no graph, because `s(n,g)` is undefined when nothing … | MODEL | 469 |
| Y311 | §1.5 | A latent good acquires graph, value weight and survival-table entry on the first month any province produces … | MODEL | 471 |
| Y312 | §1.5 | Activation is not a local addition: a province produces exactly one trade good at a time, so a latent good … | ENGINE | 473 |
| Y313 | §1.5 | In the month of conversion the new good gains a producer and the old good loses one, so both goods' supply … | MODEL | 477 |
| Y314 | §1.5 | The converting province is repriced, so `wealth(p)` changes and with it `c(n,g)` for every good in the game, … | MODEL | 479 |
| Y315 | §1.5 | `V_g` moves for both goods, reweighting every display, link value and AI score. | MODEL | 482 |
| Y316 | §1.5 | `Φ_w` moves on activation, because §1.6 runs DRAIN on that same wealth field. | MODEL | 483 |
| Y317 | §1.5 | An activation is a world-state change on the scale of a development change or a conquest, and every graph in … | DESIGN | 485 |
| Y076 | §1.5 | Repricing to coal the 45 latent-coal provinces that are owned at 1444 flips 16 of 159 `Φ_w` edges and adds … | MEASURED | 486 |
| Y077 | §1.5 | The counterfactual holds every non-repriced input fixed: province 4237 is both latent-coal and one of the … | MEASURED | 488 |
| Y318 | §1.5 | Coal's base price of 10.0 is the highest in the shipped price table. | ENGINE | 492 |
| Y320 | §1.5 | Coal produces nowhere at the 1444 start. | ENGINE | 500 |
| Y321 | §1.5 | Coal's default trigger fires on Enlightenment (the Manufactories branches require special flags), per … | ENGINE | 500 |
| Y322 | §1.5 | The 58 latent-coal provinces convert province-by-province over years rather than in a single tick, so the … | ENGINE | 503 |
| Y323 | §1.6 | `V_g = price(g) ·` the world sum of `goods_produced(m,g)` are the per-good value weights used for display, … | MODEL | 510 |
| Y324 | §1.6 | For the wealth good, supply is uniform: `s_w(n) = 1/N`. | MODEL | 512 |
| Y325 | §1.6 | For the wealth good, `c_w(n)` is the node's share of world wealth raised to `α_Φ`. | MODEL | 513 |
| Y326 | §1.6 | `b_w = s_w − c_w`, with `α_Φ = 2.0`, a hyperparameter. | MODEL | 514 |
| Y327 | §1.6 | `Φ_w = DRAIN(b_w)` — the §1.1 operator with wealth as the good. | MODEL | 516 |
| Y328 | §1.6 | `Φ_w` is the graph installed in the game. | DESIGN | 519 |
| Y329 | §1.6 | Under `Φ_w` every node supplies uniformly and rich nodes are net demanders, so all wealth in the world pulls … | MODEL | 519 |
| Y078 | §1.6 | Both the sinks' count and their locations move with the wealth field, and `α_Φ` sets how sharply … | MODEL | 522 |
| Y080 | §1.6 | v2.0 through v4.0 said the count "emerges from concentration" and v5.0 said "the count is set by `α_Φ`"; both … | MODEL | 525 |
| Y330 | §1.6 | What the world state moves is where the sinks are and how the map drains toward them, which is the property … | DESIGN | 530 |
| Y083 | §1.6 | Measured on 1444 data at `α_Φ = 2.0`: two sinks, `genua` and `hangzhou`, at `c_w` ranks 2 and 1 and … | MEASURED | 533 |
| Y084 | §1.6 | Both sinks are properties of the world, because the orientation does not depend on how the nodes are numbered … | MODEL | 534 |
| Y335 | §1.6 | With unit arc costs Phase 2's b-flow is degenerate: many routings reach the same minimum cost, and the … | MODEL | 538 |
| Y085 | §1.6 | Measured on that LP directly, 40 of 40 permutations return a different optimal support at an objective … | MEASURED | 540 |
| Y087 | §1.6 | So the old sink set was partly an artifact of the node order, and v6.0 said so. | MODEL | 541 |
| Y986 | §1.6 | Phase 2 now breaks those ties inside the objective, with a cost symmetric in the arc and read from node … | MODEL | 544 |
| Y987 | §1.6 | On the same LP under the tie-break cost, 0 of 40 permutations return a different support. | MEASURED | 545 |
| Y086 | §1.6 | Over 180 relabellings — three seeds of 60, every input held fixed — the orientation did not change once: 0 of … | MEASURED | 545 |
| Y988 | §1.6 | The instrument is a reimplementation, and a reimplementation whose Phase 2 minimises the old objective … | MEASURED | 551 |
| Y989 | §1.6 | A symmetric cost is required rather than a stylistic choice: a directional preference of the form `1 − … | MODEL | 554 |
| Y091 | §1.6 | Nothing this section quotes about the installed graph is conditional on the node order. | MODEL | 558 |
| Y093 | §1.6 | Over the 180 relabellings the sink set, every edge direction, and the promotion and fallback counts were … | MEASURED | 558 |
| Y990 | §1.6 | The per-good graphs are a different matter: the tie-break cost is read from good-independent node wealth, but … | MODEL | 563 |
| Y991 | §1.6 | Under the first-order tie-break term alone, 84 of 290 per-good relabelling runs moved an edge — the baseline … | MEASURED | 565 |
| Y1007 | §1.6 | §2.3's second-order term took per-good relabelling sensitivity from 84 of 290 runs to 13, and the goods … | MEASURED | 565 |
| Y1008 | §1.6 | Pinning the solver's optimality tolerance took the remaining per-good relabelling sensitivity to 0 of 290. | MEASURED | 567 |
| Y1009 | §1.6 | On this field the per-good graphs are order-invariant over the orderings tried, as `Φ_w` is. | MODEL | 568 |
| Y336 | §1.6 | The emitter should still fix one canonical order, because both order-invariance guarantees are measured … | DESIGN | 570 |
| Y993 | §1.6 | The value weights are the exception: `V_g` is `price(g)` times a sum over producers, with no direction in it, … | MODEL | 572 |
| Y094 | §1.6 | Phase 1 selects `hangzhou`; `genua` arrives by stall promotion, so there is 1 promotion and 0 fallbacks. | MEASURED | 576 |
| Y095 | §1.6 | Five sources, all in the bottom half of the wealth field, at `c_w` ranks 55–79 and mean degree 2.4 against … | MEASURED | 577 |
| Y337 | §1.6 | v2 called the sources "cul-de-sacs"; the degrees are not far off that reading here, but it is a description … | MODEL | 578 |
| Y096 | §1.6 | Every node drains to a sink, the map is acyclic and 159/159 oriented, the sink set is unchanged under ±1% … | MEASURED | 579 |
| Y082 | §1.6 | 1444's `b_w` has largest magnitude 0.0347. | MEASURED | 580 |
| Y338 | §1.6 | `Φ_w`'s marking order is a per-node scalar whose descending comparison reproduces the DAG (0 violations), so … | MEASURED | 582 |
| Y097 | §1.6 | Per good on the same field: 2–8 sinks, mean 3.69, 29/29 acyclic, 0 fallbacks fired, and 90.6% of ordered node … | MEASURED | 585 |
| Y098 | §1.6 | Agreement with the per-good graphs is 55.1% of edge-goods and 54.8% value-weighted. | MEASURED | 588 |
| Y100 | §1.6 | `α_Φ = 2.0`, `TIE_EPS = 1e-3` and `TIE_EPS2 = 1e-6` are hyperparameters; the choice is developer taste and … | DESIGN | 593 |
| Y102 | §1.6 | No derivation is claimed, none is implied, and none should be reconstructed from the figures below: they … | DESIGN | 595 |
| Y103 | §1.6 | Across `α_Φ` = 1.00…8.00 at 0.01 the sink set is a step function, and `α_Φ = 2.0` sits in the band [1.63, … | MEASURED | 599 |
| Y104 | §1.6 | Sampled at six values the sink count is non-monotone: 3 → 1 → 2 → 2 → 1 → 1 across `α_Φ` in {1, 1.5, 2, 3, 4, … | MEASURED | 601 |
| Y992 | §1.6 | For `TIE_EPS` the sink set is unchanged from about 1e-6 to about 1 — six orders of magnitude — because the … | MEASURED | 602 |
| Y1010 | §1.6 | `TIE_EPS2` behaves the same way as `TIE_EPS` and was measured at 1e-7, 1e-6 and 1e-5, all three leaving the … | MEASURED | 606 |
| Y105 | §1.6 | A written warning against reintroducing the withdrawn justifications for `α_Φ` — resemblance to vanilla's … | DESIGN | 610 |
| Y106 | §1.6 | "Europe becomes the centre of trade as it develops" is the design claim, and it is what §3.1's first goal … | DESIGN | 615 |
| Y107 | §1.6 | At 1444 the map ends in Genoa and in Hangzhou, and as European development compounds Europe gains ends and … | MEASURED | 616 |
| Y108 | §1.6 | The mechanism carrying that is that wealth is linear in development, so developing a region moves its `c_w` … | MODEL | 617 |
| Y341 | §1.6 | All three institutions the period is named for begin in Europe between 1450 and 1550: Renaissance `1450.1.1` … | ENGINE | 648 |
| Y342 | §1.6 | The Renaissance's embracement bonus is `development_cost = -0.05`, a standing discount on every subsequent … | ENGINE | 651 |
| Y343 | §1.6 | Those institution bonuses are country-scoped, so §1.3 excludes them from wealth directly; they reach the map … | MODEL | 652 |
| Y345 | §1.6 | From the north the route to the Asian end is the Volga and the steppe: `white_sea → novgorod → kazan → … | MEASURED | 657 |
| Y113 | §1.6 | From Iberia the route is the African coast and the Red Sea: `sevilla → safi → timbuktu → katsina → ethiopia → … | MODEL | 659 |
| Y114 | §1.6 | No route leaves `genua` at all — it is a sink, out-degree 0 against in-degree 5, so the western … | MEASURED | 661 |
| Y994 | §1.6 | `english_channel` is not an end at this α: it drains to `genua` in two hops through `champagne`, and reaches … | MODEL | 662 |
| Y115 | §1.6 | No Europe→sink route passes the Cape of Good Hope, checked exhaustively rather than sampled: of the 23 … | MEASURED | 666 |
| Y116 | §1.6 | The Cape is a live conduit rather than an idle one: in-degree 2, out-degree 2, with 81 ordered node pairs for … | MEASURED | 672 |
| Y117 | §1.6 | The 81 is a count of pairs `(a, b)` where `a` reaches the Cape, the Cape reaches `b`, and `a` reaches `b` — … | MEASURED | 675 |
| Y118 | §1.6 | In the per-good graphs the Cape also carries Asian spices to Europe; `Φ_w` models power, not cargo. | MODEL | 677 |
| Y120 | §1.6 | The Cape reverses under the same growth — 1444's `ivory_coast`/`zanzibar`→Cape→`comorin_cape`/`malacca` … | MEASURED | 687 |
| Y347 | §1.6 | The 22 European nodes are the 18 western and central ones (`english_channel`, `north_sea`, `baltic_sea`, … | MODEL | 692 |
| Y121 | §1.6 | Dev-stacking a single node's top province concentrates the map on that node, and extra sinks at intermediate … | MODEL | 696 |
| Y348 | §1.6 | The v1 diagnostic identity (`Φ ≡ φ₀` at α = 1) does not survive the operator change, because DRAIN performs … | MODEL | 715 |
| Y349 | §1.6 | Its replacement as the end-to-end correctness check is exact orientation equality between the reference and … | DESIGN | 716 |
| Y350 | §1.7 | Merchant placement, range and the collect/steer choice are vanilla, with one merchant per country per node. | ENGINE | 722 |
| Y351 | §1.7 | A merchant present gives +2 trade power (`MERCHANT_MAX_POWER_BONUS`) and a +10% bonus on trade income … | ENGINE | 722 |
| Y352 | §1.7 | v1 and v2 both called the second bonus "+10% trade efficiency"; trade efficiency and a flat income bonus are … | ENGINE | 722 |
| Y353 | §1.7 | Collect is vanilla, including the −50% penalty outside the home node. | ENGINE | 724 |
| Y354 | §1.7 | Under Steer the node window lists every link incident to the node. | MODEL | 726 |
| Y355 | §1.7 | The vanilla window already renders both an incoming and an outgoing link list as clickable entries … | ENGINE | 726 |
| Y356 | §1.7 | What changes is what an incoming entry does — it must accept a merchant assignment rather than merely … | DESIGN | 729 |
| Y357 | §1.7 | §2.7 item 14 settled that the incoming entry only navigates: clicking `Safi` in Sevilla's window switched the … | ENGINE | 730 |
| Y358 | §1.7 | A merchant assigned to link {n,m} steers every good oriented n → m. | MODEL | 735 |
| Y359 | §1.7 | A merchant assigned to link {n,m} is inert for every good oriented m → n. | MODEL | 736 |
| Y360 | §1.7 | A merchant keeps its assignment when a link flips; only its active good set changes. | MODEL | 737 |
| Y361 | §1.7 | The same physical link can host a merchant at each end, active on disjoint good sets. | MODEL | 739 |
| Y362 | §1.7 | Caravan power requires the merchant to be steering at least one good on that link; assignment alone does not … | MODEL | 741 |
| Y363 | §1.7 | That constrains only the two steering conditions — collecting at an inland node as main trading port is … | MODEL | 742 |
| Y364 | §1.7 | The engine's own caravan grant conditions are `merchant_present_inland` and `merchant_steering_to_inland`, … | ENGINE | 743 |
| Y365 | §1.7 | §2.7 item 11 settles the caravan recipient, and §3.11 carries both readings of the exposure surface. | DESIGN | 745 |
| Y366 | §1.8 | Trade power and collect/transfer intent are node-wide; what varies per good is what they produce. | MODEL | 750 |
| Y367 | §1.8 | `collected_share(n,g) = 1` if n is a sink for g, else `P_collect / (P_collect + P_transfer(g))`. | MODEL | 755 |
| Y368 | §1.8 | Transfer eligibility is per good: a country's power counts toward `P_transfer(g)` only if it has a merchant … | MODEL | 759 |
| Y369 | §1.8 | The remainder moves per good by the vanilla two-case rule. | MODEL | 761 |
| Y370 | §1.8 | If any country steers `g` at `n`, the outgoing value of `g` is divided across outgoing links in proportion to … | ENGINE | 763 |
| Y371 | §1.8 | An outgoing link with no steerer receives nothing, even when other links are steered. | ENGINE | 763 |
| Y372 | §1.8 | A single steerer takes all of `g`'s outgoing value down its link, however little power it holds. | ENGINE | 763 |
| Y373 | §1.8 | If no country steers `g` at `n`, the outgoing value splits evenly across `g`'s outgoing links. | ENGINE | 765 |
| Y374 | §1.8 | At `g`'s sink there is no remainder: 100% is collected and divided among collectors by trade power. | MODEL | 767 |
| Y375 | §1.8 | Vanilla gates still apply: trade range, and the rule that there is no transfer into a node where nobody holds … | ENGINE | 769 |
| Y376 | §1.8 | What trade range gates is reach, not flow: every string, define and modifier that mentions it is about where … | ENGINE | 770 |
| Y377 | §1.8 | No string, define or modifier ties range to link flow — which is a statement about the files rather than a … | ENGINE | 775 |
| Y378 | §1.8 | There is no trade "supply range" in the engine; the only supply-range constructs are naval. | ENGINE | 778 |
| Y379 | §1.9 | A country whose provincial trade power in a node meets the threshold receives a share of it in every … | ENGINE | 784 |
| Y380 | §1.9 | The engine's own tooltip says power transfers "to trade nodes where it already has power", and that qualifier … | ENGINE | 784 |
| Y381 | §1.9 | Measured: France holds zero provinces and zero merchants in Sevilla and still appears there with 3.3 power, … | ENGINE | 784 |
| Y382 | §1.9 | This line was §3.16's cautionary case; it is now closed, and it closed in favour of the spec. | DESIGN | 784 |
| Y383 | §1.9 | The propagation share is `1 / TRADE_PROPAGATE_DIVIDER`, and the threshold in raw power is … | ENGINE | 784 |
| Y384 | §1.9 | Ship trade power propagates only where the country has a ship-propagation modifier, at the compounded rate: … | ENGINE | 785 |
| Y385 | §1.9 | Propagation is strictly one hop and never chains. | ENGINE | 786 |
| Y386 | §1.9 | A node receives the summed contributions of all its downstream neighbours. | ENGINE | 787 |
| Y387 | §1.9 | Direction for propagation is read from `Φ_w`. | MODEL | 789 |
| Y388 | §1.10 | Any mechanism gated on one nation being upstream or downstream of another evaluates TRUE. | DESIGN | 793 |
| Y389 | §1.10 | Any node-pair direction dependency reads `Φ_w`. | DESIGN | 795 |
| Y390 | §1.10 | Where a gate scopes a set or a path, that scope reads `Φ_w` with a three-rung fallback ladder: the `Φ_w` … | DESIGN | 797 |
| Y391 | §1.10 | The mechanics below the gates are unpatched and unchanged; reorientation reaches them through the trade power … | ENGINE | 803 |
| Y392 | §1.10 | Nothing in that group is patched and all of it moves monthly. | MODEL | 803 |
| Y393 | §1.10 | Trade-conflict casus belli thresholds are `JUSTIFY_TRADE_CONFLICT_LIMIT` (target) and … | ENGINE | 809 |
| Y394 | §1.10 | Privateer blocking is thresholded by `MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER`. | ENGINE | 811 |
| Y395 | §1.10 | Trade-company extra merchant and control are thresholded by `TRADE_COMPANY_STRONG_LIMIT` and … | ENGINE | 812 |
| Y396 | §1.10 | Improve Inland Routes needs 50% to establish and 40% to maintain plus a merchant present in the node, and is … | ENGINE | 814 |
| Y397 | §1.10 | Propagate Religion needs 50% to establish and 50% to maintain in the default branch and 35/35 in the terminal … | ENGINE | 815 |
| Y398 | §1.10 | The nine `N_trade_power_for_propogate_religion` country-flag rungs are banded: maintain trails select by 5–10 … | ENGINE | 815 |
| Y399 | §1.10 | The banding is the reverse of what v1 recorded: Improve Inland Routes is the one unconditionally banded … | ENGINE | 817 |
| Y400 | §1.10 | Banding therefore absorbs very little chatter: a power share oscillating across any single-valued limit … | ENGINE | 819 |
| Y401 | §1.10 | Banding is not the only damper: three shipped defines rate-limit the mechanics that carry these thresholds. | ENGINE | 821 |
| Y122 | §1.10 | `TRADING_POLICY_COOLDOWN_MONTHS = 12` applies to seven of the nine entries in … | ENGINE | 822 |
| Y123 | §1.10 | `maximize_profit` and `maximize_profit_upgraded` carry `cooldown = no` in … | ENGINE | 827 |
| Y124 | §1.10 | `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` with `TRADE_COMPANY_COOLDOWN = 60` means a flickering share does not … | ENGINE | 828 |
| Y125 | §1.10 | What is left exposed is everything without a cooldown, which is most of the ladder. | ENGINE | 830 |
| Y402 | §1.10 | The flicker-risk set is "every country at a single-valued limit, plus flagless countries at Propagate … | ENGINE | 831 |
| Y403 | §1.10 | Casus belli availability is the most visible symptom, since it can appear and vanish month to month. | ENGINE | 833 |
| Y404 | §1.10 | Caravan power is in this group but is not a threshold mechanic and is not a function of raw trade power at … | ENGINE | 836 |
| Y405 | §1.10 | When caravan power applies it is worth up to the cap for any major power — enough to move a node's power … | MODEL | 836 |
| Y126 | §1.10 | Measured on the 1444 start, the caravan cap of 50 is 9.4% to 47.0% of an inland node's total trade power, … | MEASURED | 836 |
| Y127 | §1.10 | As a share of the node's total after the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, … | MEASURED | 836 |
| Y128 | §1.10 | On §2.2's derived 25-node inland basis (dropping `siberia`) the median is 21.3%, or 17.5% after the grant. | MEASURED | 836 |
| Y406 | §1.10 | The largest single incumbent holder runs 23.6 to 143.2, so a country at the caravan cap outweighs the largest … | MEASURED | 836 |
| Y407 | §1.10 | v4.0 read the save's per-node `highest_power` field as the largest incumbent's power; it is not — parsing … | ENGINE | 836 |
| Y408 | §1.10 | What `highest_power` does hold was not determined, and the model does not read it. | MODEL | 836 |
| Y409 | §1.10 | v1 and v2 both described caravan power as "a step function on raw power", which contradicted their own §3.11. | PROCESS | 836 |
| Y410 | §1.10 | No mission, decision, event, or trade company in 1.37.5 names a trade node — zero non-comment references … | ENGINE | 838 |
| Y411 | §1.10 | Trade companies are bare province lists. | ENGINE | 839 |
| Y413 | §1.10 | Nodes themselves never change under the mod — only connections do — so the name-collision class of conflict … | MODEL | 848 |
| Y414 | §1.10 | What remains exposed is semantics: `highest_value_trade_node` and node-scoped triggers are evaluated against … | ENGINE | 850 |
| Y415 | §1.10 | That semantic exposure is accepted and listed for the compatibility pass rather than engineered around. | DESIGN | 853 |
| Y416 | §1.11 | The overlord always receives the treasure fleet. | DESIGN | 858 |
| Y417 | §1.11 | The fleet routes by the §1.10 ladder, passing each node en route where privateers skim a share proportional … | MODEL | 858 |
| Y418 | §1.11 | Where the diversion mechanic is active, colonial gold income is diverted from the colonial nation. | ENGINE | 860 |
| Y419 | §1.11 | Diverted gold does not enter `wealth` at either end, for the deeper reason of §1.5: gold income is its own … | MODEL | 861 |
| Y420 | §1.12 | The in-game economy is the per-good economy: node values, the node window, pie charts, the ledger, the … | DESIGN | 866 |
| Y421 | §1.12 | Trade map mode colours provinces by node and draws arrows between nodes rendering `Φ_w`, with arrow weight … | MODEL | 868 |
| Y422 | §1.12 | Clicking a province switches province colouring to the vanilla trade-goods rendering for that good and … | MODEL | 870 |
| Y423 | §1.12 | Value broken down by commodity is not representable in the vanilla UI: the node window carries several … | ENGINE | 874 |
| Y424 | §1.12 | A link's two-way traffic is not representable: one scalar per link, shown as net. | ENGINE | 877 |
| Y425 | §1.12 | Per-country effective trade power where eligibility differs by good is not representable and is shown as a … | ENGINE | 878 |
| Y426 | §1.12 | There is no new art, sprites, shaders or map-mode chrome; making the node window's existing incoming-link … | DESIGN | 880 |
| Y427 | §2.1 | The implementation is one program: a runtime-attached DLL that each month reads live game state, solves per … | DESIGN | 889 |
| Y428 | §2.1 | It ships with a generated `00_tradenodes.txt` for load time and a companion overlay for what the engine … | DESIGN | 889 |
| Y429 | §2.1 | The target platform is Windows/Steam. | DESIGN | 891 |
| Y430 | §2.1 | Achievements are off with any mod (`ACHIEVEMENTS_DISABLED_MODIFIED_GAME`). | ENGINE | 891 |
| Y431 | §2.1 | The engine will load an ironman save in a modded game — `Loading ironman in modded game` is a shipped code … | ENGINE | 892 |
| Y432 | §2.1 | EU4 multiplayer is lockstep with checksums, so every client must reach the same answer; the classical worry … | ENGINE | 896 |
| Y434 | §2.1 | DRAIN's exposure is different in kind from v1's dense linear algebra, which was badly exposed to it: v1 … | MODEL | 898 |
| Y435 | §2.1 | DRAIN's comparisons are of input-derived quantities (`DEF`, `b`, arc costs) rather than of solver residuals, … | MODEL | 903 |
| Y1011 | §2.1 | The multiplayer question is no longer whether the arithmetic agrees to the last bit but whether the build is … | DESIGN | 905 |
| Y995 | §2.1 | §2.3's two changes move the desync question from a design problem to a verification one: the largest exposure … | MODEL | 909 |
| Y1012 | §2.1 | There is no randomness in the solve: an identical output fingerprint over repeated runs, separate processes … | MEASURED | 916 |
| Y1013 | §2.1 | The margin by which the optimum is unique is 3.8e-8 worst per good and 7.5e-6 on the aggregate — 8 to 10 … | MEASURED | 917 |
| Y1014 | §2.1 | Orientation under LP column permutation: 0 flips on the aggregate and on all 29 goods, with an objective … | MEASURED | 918 |
| Y1015 | §2.1 | The per-good `abs(net)` distribution is bimodal — 2,321 edge-goods at exactly 0 and 2,290 above 1e-6, with … | MEASURED | 920 |
| Y1016 | §2.1 | A few units in the last place cannot change any decision this solver makes, so what remains is not … | MODEL | 922 |
| Y1017 | §2.1 | Check 1 — one binary per platform and no cross-platform sessions, because a single compiled instruction … | DESIGN | 925 |
| Y1018 | §2.1 | The `../v2-drain/` DLL precedent is already Windows- and Steam-only, so the one-binary rule matches practice … | MODEL | 926 |
| Y1019 | §2.1 | Check 2 — no runtime CPU dispatch in the LP solver and single-threaded: this is the live risk, because … | DESIGN | 928 |
| Y1020 | §2.1 | Check 3 — §2.8's cross-implementation orientation check compares the DLL against the reference implementation … | DESIGN | 932 |
| Y1021 | §2.1 | Every trade number EU4 writes to a save is quantised to 1/1000: 495 of 495 sampled values land exactly on … | ENGINE | 936 |
| Y1022 | §2.1 | Quantisation of that kind erases any divergence below half a grid step, which is the standard cheap defence. | ENGINE | 938 |
| Y1023 | §2.1 | The files cannot settle whether the rounding happens in the simulation or only in the serialiser; that needs … | ENGINE | 939 |
| Y1024 | §2.1 | Quantisation would not rescue this solver either way: the orientation margins of 3.8e-8 to 7.5e-6 are three … | MODEL | 941 |
| Y436 | §2.1 | Until checks 1–3 are done, ship single-player only. | DESIGN | 945 |
| Y1025 | §2.1 | The reason for shipping single-player has changed: it is no longer "vertex selection is machine-dependent" … | MODEL | 945 |
| Y437 | §2.2 | Solver item 1 is a parser for `common/tradenodes/00_tradenodes.txt` reading adjacency, `members`, … | DESIGN | 951 |
| Y438 | §2.2 | Solver item 2 is a parser for non-ironman saves reading province owner, `base_tax`, `base_production`, trade … | DESIGN | 952 |
| Y439 | §2.2 | Solver item 3 is a parser for `common/defines.lua` merged with `common/defines/` overrides in load order. | DESIGN | 953 |
| Y440 | §2.2 | `GP_COEFF` is read from `common/static_modifiers/00_static_modifiers.txt` rather than hardcoded. | ENGINE | 959 |
| Y131 | §2.2 | World wealth is 10,607.40 annual ducats over 2,472 counted provinces. | MEASURED | 963 |
| Y441 | §2.2 | Solver item 5 is DRAIN per good: a min-cost b-flow using network simplex or a simplex LP rather than … | DESIGN | 964 |
| Y442 | §2.2 | The Phase-4 evaluator's `unserved` and `stranded` must be equal by conservation, since the sum of `b_g` over … | MODEL | 966 |
| Y443 | §2.2 | `Φ_w` is one more DRAIN run with wealth as the good — the 30th solve, same code path. | MODEL | 968 |
| Y444 | §2.2 | Solver item 6 is a survival table `S_g[n][H]` for AI scoring, one table serving every country. | DESIGN | 969 |
| Y445 | §2.2 | Solver item 7 is a mutual reachability census: 30 goods × 80 BFS producing an 80×80 matrix whose entry counts … | DESIGN | 970 |
| Y446 | §2.2 | Solver item 8 is a synthetic-shock harness that edits parsed province data and re-solves. | PROCESS | 971 |
| Y447 | §2.2 | Cost per good is one uncapacitated min-cost flow on 80 nodes and 318 arcs plus an O(V+E) sweep. | MODEL | 973 |
| Y133 | §2.2 | Repeated 12-run experiments on one machine do not reproduce each other closely enough to support anything … | MEASURED | 976 |
| Y134 | §2.2 | v5.0's "0.17–0.21 s for all 29 goods" is not reproducible: across three replicates of twelve runs the number … | MEASURED | 980 |
| Y448 | §2.2 | "Milliseconds each" holds already with a generic LP; the all-29 figure is what a native network simplex would … | DESIGN | 982 |
| Y449 | §2.2 | There are two implementations of one specification: the reference solver (standalone, run against parsed … | DESIGN | 987 |
| Y450 | §2.2 | The two implementations must agree on orientation exactly — a combinatorial comparison with no tolerance band … | DESIGN | 987 |
| Y451 | §2.2 | The parsers and the harness stay reference-only, and the DLL never reads a save. | PROCESS | 989 |
| Y452 | §2.2 | Inland is derived rather than trusted from the flag: a node with no coastal province among its `members`. | DESIGN | 991 |
| Y453 | §2.2 | The derivation and the flag disagree at exactly one node — `siberia` carries `inland=yes` but has two … | ENGINE | 992 |
| Y454 | §2.2a | v2 called the target "map-agnostic" while proving its central properties only for the map it was measured on; … | MODEL | 997 |
| Y455 | §2.2a | Premise 1 is that the node graph is connected: reachability is LP feasibility, and the LP is feasible because … | MODEL | 1001 |
| Y456 | §2.2a | On a graph with more than one component the global balance is not enough — each component must balance … | MODEL | 1002 |
| Y457 | §2.2a | Vanilla 1444 is one component. | MEASURED | 1005 |
| Y458 | §2.2a | The solver must compute components once at load; on a single component it proceeds, and on more than one it … | DESIGN | 1007 |
| Y459 | §2.2a | The solver must not silently hand an infeasible program to the LP. | DESIGN | 1010 |
| Y460 | §2.2a | v1 carried per-component renormalisation and v2 dropped it without replacement; v3 restores the requirement. | PROCESS | 1011 |
| Y461 | §2.2a | Premise 2 is that Phase 0 is a no-op, or the map-dependent properties are read as measurements: several §1.1 … | MODEL | 1014 |
| Y462 | §2.2a | Where Phase 0 acts, three properties weaken and the spec says so rather than asserting through it. | DESIGN | 1016 |
| Y463 | §2.2a | Global DAG is proved on a 2-core map and still proved where Phase 0 acts, because pendant edges are bridges … | MODEL | 1021 |
| Y464 | §2.2a | Sink-set equality is measured exact 29/29 on a 2-core map and fails where Phase 0 acts, because a pendant … | MEASURED | 1022 |
| Y135 | §2.2a | Where Phase 0 acts, free-edge determinism is unaffected but index-independence is not: the key reads the … | MODEL | 1024 |
| Y466 | §2.2a | Two further cases are independent of Phase 0 and both break sink-set equality inside the 2-core: a selected … | MEASURED | 1026 |
| Y467 | §2.2a | The stated target is connected maps: on a connected map with minimum degree at least 2 every §1.1 property is … | DESIGN | 1031 |
| Y468 | §2.2a | On a connected map with pendants the algorithm still runs and still produces an acyclic, fully-oriented, … | MODEL | 1032 |
| Y469 | §2.2a | On a disconnected map the solver must renormalise per component or refuse. | DESIGN | 1034 |
| Y470 | §2.3 | Constants are read at runtime and never hardcoded. | DESIGN | 1039 |
| Y471 | §2.3 | The nine runtime-read uses map to named defines: `TRADE_PROPAGATE_DIVIDER`, `TRADE_PROPAGATE_THRESHOLD`, … | ENGINE | 1041 |
| Y472 | §2.3 | `TRADE_MERCHANT_PRESENT` is a bonus on income, not trade efficiency. | ENGINE | 1048 |
| Y136 | §2.3 | The two wealth coefficients are not the same kind of constant: the emitter reads `GP_COEFF` rather than … | DESIGN | 1053 |
| Y137 | §2.3 | v3.0 through v5.0 said neither coefficient was in a file, and shipped a whole-install modifier sweep that … | PROCESS | 1059 |
| Y473 | §2.3 | `GP_COEFF` is 0.2 goods produced per point of `base_production`, measured on four provinces at four … | ENGINE | 1065 |
| Y474 | §2.3 | `TAX_COEFF` is 1.0 ducat per year per point of `base_tax`, measured on two provinces at two development … | ENGINE | 1066 |
| Y475 | §2.3 | Both coefficients are read off the tooltips' base lines, which carry no owner term — Garnatah also has … | ENGINE | 1068 |
| Y476 | §2.3 | Neither coefficient is read off a province window, because a window figure carries the owner's modifiers and … | ENGINE | 1069 |
| Y477 | §2.3 | Prices come from `common/prices/00_prices.txt` at runtime and are never hardcoded. | ENGINE | 1070 |
| Y478 | §2.3 | The design constants are the excluded-goods list (defaulting to gold), the α price anchor `P₀ = 2.0`, the … | DESIGN | 1073 |
| Y479 | §2.3 | `α_Φ`, `TIE_EPS` and `TIE_EPS2` are hyperparameters whose values are developer taste, the document offers no … | MODEL | 1083 |
| Y339 | §2.3 | Changing any of the three hyperparameters is a design decision, and §1.6 records how the field responds … | DESIGN | 1086 |
| Y996 | §2.3 | `TIE_EPS` and `TIE_EPS2` together set the Phase-2 objective, `cost(u,v) = 1 + TIE_EPS·(w[u]+w[v])/2 + … | MODEL | 1091 |
| Y1026 | §2.3 | The two cost terms do different jobs and only the first means anything: the first-order term is the design … | DESIGN | 1102 |
| Y1027 | §2.3 | The second-order term is tie-breaking and nothing else; its form is arbitrary and no reading should be … | DESIGN | 1104 |
| Y998 | §2.3 | A single cost vector does not make every solve unique, because uniqueness of an LP optimum depends on `b` as … | MODEL | 1107 |
| Y1028 | §2.3 | Measured on zero-reduced-cost arcs outside the support: the aggregate `b_w` goes from 40 under unit costs to … | MEASURED | 1110 |
| Y1029 | §2.3 | Adding the second-order term takes the zero-reduced-cost arcs to 1 arc on 1 good. | MEASURED | 1112 |
| Y1030 | §2.3 | The solver's optimality tolerance is a correctness requirement rather than a performance knob, and HiGHS … | MODEL | 1125 |
| Y1053 | §2.3 | `scipy.optimize.linprog`'s `method="highs"` options document that default as `1e-07`, for both the dual and … | MODEL | 1126 |
| Y1031 | §2.3 | The margin by which the tie-break makes the optimum unique runs as low as 3.8e-8 on some per-good solves, so … | MEASURED | 1128 |
| Y1032 | §2.3 | Measured: over six permutations of the LP's column order, `copper` and `paper` returned orientations … | MEASURED | 1130 |
| Y1054 | §2.3 | The tolerance mechanism is confirmed rather than inferred, by bisecting the tolerance against `copper`. | MODEL | 1135 |
| Y1055 | §2.3 | Leaving the tolerance unset and setting it to 1e-7 give the same 8 flips over four permutations, which is … | MEASURED | 1135 |
| Y1056 | §2.3 | 1e-8 already gives 0 flips, and 1e-8 is the first value below `copper`'s 3.765e-8 margin. | MEASURED | 1137 |
| Y1057 | §2.3 | The flips therefore appear exactly when the tolerance exceeds the margin, which is the claim. | MODEL | 1137 |
| Y1033 | §2.3 | `flowop.LP_OPTS` ships 1e-10 — HiGHS's floor for these options, taken for headroom rather than necessity — … | MEASURED | 1139 |
| Y1034 | §2.3 | No figure in this document moved when the pinned tolerance went in: the shipped column order was already … | PROCESS | 1140 |
| Y1035 | §2.3 | What the second-order term costs: self-coherence with the per-good graphs falls 0.1–0.2 points and nothing … | MEASURED | 1144 |
| Y1036 | §2.3 | What the second-order term buys is replacing a tiebreak that was arbitrary and order-dependent — the node … | DESIGN | 1146 |
| Y1037 | §2.3 | The normalisation of `w` is load-bearing per good and that is a cost of the second-order term: for the … | MODEL | 1156 |
| Y997 | §2.3 | Every DRAIN solve uses this cost, per good as well as aggregate, and since `w` is node wealth the same cost … | MODEL | 1177 |
| Y483 | §2.3 | DLC state is a third input axis: treasure-fleet diversion and caravan power are both DLC-conditional, and … | ENGINE | 1182 |
| Y484 | §2.4 | The tradenodes file is generated once from the campaign start date's `Φ_w` and then owned by the DLL in … | DESIGN | 1186 |
| Y485 | §2.4 | The engine performs no topological sort; it validates that the file is one, logging … | ENGINE | 1188 |
| Y486 | §2.4 | Measured: a file with all 159 links declared backwards logged exactly 159 such errors and then loaded and … | ENGINE | 1191 |
| Y487 | §2.4 | What the engine does not tolerate is a cycle: a hand-authored two-node cycle produced … | ENGINE | 1195 |
| Y488 | §2.4 | The crash dump records no per-frame addresses. | ENGINE | 1197 |
| Y489 | §2.4 | Acyclicity is therefore a hard correctness requirement of the emitter, established by observation rather than … | DESIGN | 1198 |
| Y490 | §2.4 | A reversed link is honoured completely: moving one `outgoing` block from `sevilla` to `valencia` with the … | ENGINE | 1202 |
| Y491 | §2.4 | In that test Valencia moved from Sevilla's outgoing side to its incoming side, Sevilla became an end node … | ENGINE | 1204 |
| Y492 | §2.4 | Every provincial power figure was unchanged in that test. | ENGINE | 1207 |
| Y493 | §2.4 | That test is the mod's core premise verified end to end. | DESIGN | 1208 |
| Y494 | §2.4 | Item 1: emit in decreasing `Φ_w` marking order, which is the convention the engine states and the shipped … | ENGINE | 1210 |
| Y138 | §2.4 | A canonical node order is still a correctness requirement but is no longer what decides the installed map: … | DESIGN | 1212 |
| Y495 | §2.4 | Phase 2's min-cost b-flow is degenerate under unit arc costs: many distinct supports carry the same optimal … | MODEL | 1216 |
| Y139 | §2.4 | Measured on that objective, 40 of 40 permutations return a different optimal support. | MEASURED | 1218 |
| Y140 | §2.4 | Those permutations reach an objective identical to within a few units in the last place. | MODEL | 1218 |
| Y147 | §2.4 | §2.3 now breaks those ties inside the objective. | MODEL | 1219 |
| Y141 | §2.4 | On the same LP under the tie-break cost 0 of 40 permutations return a different support, and running the … | MEASURED | 1220 |
| Y143 | §2.4 | The tie-break cost is built from good-independent node wealth so it applies to every per-good solve, but it … | MEASURED | 1226 |
| Y146 | §2.4 | The counts are HiGHS-specific in their detail but not in kind: any simplex returns a vertex of a degenerate … | MODEL | 1238 |
| Y144 | §2.4 | v6.0 quoted a 580-of-580 per-good sweep from `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`; that script … | MEASURED | 1240 |
| Y148 | §2.4 | §1.1's priority key ties in more places than §1.1 documents — besides the free-edge sweep it decides Phase … | MEASURED | 1245 |
| Y496 | §2.4 | One visible consequence of node order: the node window renders its incoming/outgoing link lists in file … | ENGINE | 1250 |
| Y497 | §2.4 | Item 2: `end=yes` on every `Φ_w` sink, stripped from any former end node that gains outgoing links. | DESIGN | 1253 |
| Y149 | §2.4 | The end-flag list is a function of the world rather than of the node order: across the 180 relabellings of … | DESIGN | 1253 |
| Y150 | §2.4 | 1444 has two end nodes, `genua` and `hangzhou`, against vanilla's three. | MEASURED | 1256 |
| Y498 | §2.4 | The end count is not fixed — it follows the wealth field and `α_Φ` — so the emitter reads it from the solve … | DESIGN | 1257 |
| Y499 | §2.4 | Item 3: link reversal means moving the `outgoing` block, reversing the `path` province list and reversing the … | DESIGN | 1260 |
| Y500 | §2.4 | Item 4: `location`, `members`, `inland=yes`, `ai_will_propagate_through_trade` and unrecognized keys … | DESIGN | 1261 |
| Y501 | §2.5 | Attachment uses pattern scanning and function hooking, following the EU4dll precedent, which provides the … | DESIGN | 1265 |
| Y502 | §2.5 | The mod ships a runtime-patching DLL rather than a modified executable. | DESIGN | 1265 |
| Y503 | §2.5 | The binary is frozen, so offsets found stay found. | ENGINE | 1265 |
| Y504 | §2.5 | The nation-pair direction gates of §1.10 are hooked and returned true at the call site rather than by forcing … | DESIGN | 1267 |
| Y505 | §2.6 | The monthly trade tick runs in three passes: static power and modifiers; a pass from the end nodes … | ENGINE | 1271 |
| Y506 | §2.6 | Written each tick: node trade value as the sum over goods of `value_g(n)`. | MODEL | 1277 |
| Y507 | §2.6 | Written each tick: node collectible pool as the sum over goods of `value_g(n) · collected_share(n,g)`. | MODEL | 1278 |
| Y508 | §2.6 | Written each tick: per-link value as net realized flow summed over goods, in the installed `Φ_w` direction. | MODEL | 1279 |
| Y509 | §2.6 | Country trade income is derived by the engine from the written fields, unless stored. | ENGINE | 1280 |
| Y510 | §2.6 | Feeding the engine the collectible pool is sufficient for a narrower reason than it looks: `collect_pool` is … | MODEL | 1282 |
| Y511 | §2.6 | What factors out is `powershare_C`, a country's share among collectors, and whether a country collects is a … | MODEL | 1282 |
| Y512 | §2.6 | There are two deadlines, not one window: display immediately after the value pass, because AI consumers read … | ENGINE | 1286 |
| Y513 | §2.6 | Payment is bounded by the month boundary, since the treasury reconciles at the start of each month against … | ENGINE | 1287 |
| Y514 | §2.6 | Per-link values are written net, which can be negative where realized flow opposes the drawn arrow. | MODEL | 1289 |
| Y515 | §2.7 | Items 1–10 are the v1 probe set, settled with a debugger on a vanilla install in one session, though the … | DESIGN | 1293 |
| Y516 | §2.7 | Items 12–15 are done: they were run against 1.37.5 in `../v2-drain/game-session.md` and their results are … | ENGINE | 1296 |
| Y517 | §2.7 | Item 12 was dropped rather than run, because under owner-agnostic wealth the per-province production-income … | DESIGN | 1297 |
| Y518 | §2.7 | Probe 13 settled and reversed the hedge: the engine does not tolerate a cycle — `EXCEPTION_STACK_OVERFLOW`, … | ENGINE | 1301 |
| Y519 | §2.7 | Probe 14 settled and confirmed the spec: the incoming-link entry only navigates, and clicking `Safi` in … | ENGINE | 1303 |
| Y520 | §2.7 | Probe 15 settled and reversed the spec's caution: the tooltip's "where it already has power" is not a … | ENGINE | 1305 |
| Y151 | §2.7 | §1.9's "every immediately upstream node" is consistent with probe 15's reading — one observation on one node, … | ENGINE | 1308 |
| Y521 | §2.7 | The §2.4 item 3 link-reversal check is done and passed: a hand-flipped link loaded with zero errors and … | ENGINE | 1311 |
| Y522 | §2.7 | The declaration-order companion question is settled: the engine validates order and logs one error per … | ENGINE | 1314 |
| Y523 | §2.7 | Probe 1 is pass caching: for each of the three passes independently, does flipping a link crash, produce … | DESIGN | 1317 |
| Y524 | §2.7 | Probe 2 is pass 2's content: what imposes its ordering, given that propagation is one hop and cannot chain. | DESIGN | 1318 |
| Y525 | §2.7 | Probe 3 is write windows: where income accumulation sits relative to the value pass, and whether writing … | DESIGN | 1319 |
| Y526 | §2.7 | Probe 4 is negative link values: write one and observe arrow rendering and protect-trade allocation. | DESIGN | 1320 |
| Y527 | §2.7 | Probe 5 is merchant storage: flip a link hosting a steering merchant and see whether the assignment dangles, … | DESIGN | 1321 |
| Y528 | §2.7 | Probe 6 is caravan, twice: does the engine grant it for a merchant assigned to a link that is incoming in … | DESIGN | 1322 |
| Y529 | §2.7 | Probe 7 is render data: is arrow render state separate from the economic link. | DESIGN | 1323 |
| Y530 | §2.7 | Probe 8 is `TRADE_PROPAGATE_THRESHOLD` semantics: set it to 4 and check whether the raw requirement doubles. | DESIGN | 1324 |
| Y531 | §2.7 | Probe 9 is diverted gold: does diverted colonial gold still appear in the per-province production income … | DESIGN | 1325 |
| Y532 | §2.7 | Probe 10 is caller enumeration: disassemble and list every call site of "is X downstream of Y", classified as … | DESIGN | 1326 |
| Y533 | §2.7 | Static string-table analysis already yields three named direction call sites — `DIPLO_SELLPROV_NOT_UPSTREAM`, … | ENGINE | 1326 |
| Y534 | §2.7 | Probe 11 is the caravan recipient: place a merchant in a coastal node steering toward an inland one, read … | DESIGN | 1327 |
| Y535 | §2.7 | The engine tooltip and the identifier `merchant_steering_to_inland` both read as the inland node, and if that … | ENGINE | 1327 |
| Y1040 | §2.7 | Probe 16 asks whether EU4's 1/1000 quantisation happens in the simulation or in the serialiser, to be settled … | DESIGN | 1329 |
| Y1041 | §2.7 | If the rounding happens in the simulation the engine erases sub-milli-ducat divergence every tick, which is a … | ENGINE | 1331 |
| Y1042 | §2.7 | Probe 16 settles what §2.1 may claim about the engine's own defence and whether the mod should round at its … | DESIGN | 1334 |
| Y536 | §2.7 | All writes land atomically at the tick hook with the sim paused. | DESIGN | 1341 |
| Y537 | §2.8 | Spice and cloves at 1444: source in Indonesia and both source there alone — `spices` from `the_moluccas` and … | MEASURED | 1347 |
| Y1043 | §2.8 | v6.0 listed Australia, Venice and Deccan among the spice and cloves termini; none of the three holds either … | MEASURED | 1347 |
| Y540 | §2.8 | Malacca to Cape post-1500: spice routes Malacca to Cape to Europe. | MODEL | 1349 |
| Y541 | §2.8 | Malacca to Cape pre-1500: the corridor is withheld by range and the power-at-both-ends gate, not by direction. | MODEL | 1350 |
| Y542 | §2.8 | A 1000 AD start puts sinks in the Muslim world and Song China, with no era data. | MODEL | 1351 |
| Y155 | §2.8 | `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth 226.7 against 143.0 — ranks 12 and … | MEASURED | 1352 |
| Y156 | §2.8 | Zeroing `beijing` also moves the map — 8 flips — because deleting a percent of world wealth renormalises … | MEASURED | 1352 |
| Y153 | §2.8 | On the razed field the result is order-invariant like the baseline: 40 of 40 relabellings return `{genua, … | MEASURED | 1352 |
| Y544 | §2.8 | Ming losing the Mandate moves nothing on the day it happens, because the Mandate is an owner property and … | MODEL | 1353 |
| Y545 | §2.8 | That row is the owner-agnosticism check, not a responsiveness check. | DESIGN | 1353 |
| Y546 | §2.8 | A major war in China shifts corridors for the duration, reverting as devastation heals. | MODEL | 1354 |
| Y547 | §2.8 | Many poor provinces versus few rich: luxury demand goes to the rich-province node and bulk to the … | MODEL | 1355 |
| Y548 | §2.8 | On a price crash α falls below 1 and regional sinks reappear. | MODEL | 1356 |
| Y549 | §2.8 | Caribbean 1650: sugar production income makes it a sink for cloth, tools and wine. | MODEL | 1357 |
| Y550 | §2.8 | Kilwa 1000: ivory income makes it a sink for Indian textiles. | MODEL | 1358 |
| Y551 | §2.8 | A consuming leaf terminates the DAG of every good it consumes but does not produce. | MODEL | 1359 |
| Y552 | §2.8 | An inert merchant's goods take the even split as if the node were empty, while node-wide bonuses still apply. | MODEL | 1360 |
| Y553 | §2.8 | A node sinking spice but not cloth collects spice fully and cloth at the ratio, with cloth's remainder pushed. | MODEL | 1361 |
| Y554 | §2.8 | A near-balanced link may flip monthly, carries near-zero either way, and assignments survive. | MODEL | 1362 |
| Y555 | §2.8 | A two-way Atlantic corridor has merchants at both ends on disjoint good sets, neither blocking the other. | MODEL | 1363 |
| Y556 | §2.8 | Economy tab versus overlay: every displayed trade figure matches the per-good economy to the ducat, and this … | DESIGN | 1364 |
| Y557 | §2.8 | Stock trade values are not reproducible run to run: two identical vanilla 1444 Castile starts differ on 49 of … | ENGINE | 1364 |
| Y558 | §2.8 | AI merchant placement is randomised at start, and it is the three power-dependent fields that inherit it: … | ENGINE | 1364 |
| Y559 | §2.8 | Any comparison against unmodded numbers needs a tolerance and a null run. | DESIGN | 1364 |
| Y560 | §2.8 | Reachability is asserted every tick: 100% of every good's demand reachable from its supply, zero orphan sinks … | MODEL | 1365 |
| Y561 | §2.8 | Conservation is asserted every good every tick: Phase-4 sum of `unserved` equals sum of `stranded` to machine … | MODEL | 1366 |
| Y562 | §2.8 | Determinism is asserted: re-running a tick reproduces the orientation bit-for-bit, and promotions and … | MODEL | 1367 |
| Y1044 | §2.8 | A new validation row asserts the LP is configured tighter than the tie-break margin: `flowop.LP_OPTS` sets … | MODEL | 1368 |
| Y563 | §2.8 | Acyclicity is asserted on every per-good graph, on `Φ_w`, and on the emitted file's declaration order. | DESIGN | 1369 |
| Y564 | §2.8 | Sink-set containment is a hard assertion every tick, unconditionally: every sink inside the 2-core lies in … | MODEL | 1370 |
| Y565 | §2.8 | Asserting containment in `{selected} ∪ {promoted}` alone would halt on T3, which is correct behaviour, so the … | MODEL | 1370 |
| Y566 | §2.8 | Sink-set equality is monitored rather than asserted: it is measured exact on 1444 (29/29 goods, zero … | MEASURED | 1370 |
| Y567 | §2.8 | Where Phase 0 acts the equality does not apply and is not asserted; the check on a peeled edge is the Phase-4 … | MODEL | 1371 |
| Y568 | §2.8 | Colonization check: an observer run to 1600 sees New World colonization proceed at roughly vanilla pace. | MODEL | 1372 |
| Y569 | §2.8 | AI convergence check: greedy assignment settles with damping rather than oscillating. | MODEL | 1373 |
| Y570 | §2.8 | Latent-good check: while latent there is no graph, no value weight and no survival-table entry, and all three … | MEASURED | 1374 |
| Y571 | §2.8 | Cross-implementation check: the DLL and the reference implementation agree on orientation exactly for every … | DESIGN | 1375 |
| Y572 | §2.8 | `Φ_w`-vs-realized sign disagreement is measured rather than asserted, weighted by trade value rather than … | MEASURED | 1379 |
| Y573 | §2.8 | Flip behaviour is measured per decade in peace versus war, along with whether flips revert as occupation … | MODEL | 1383 |
| Y574 | §2.8 | Propagated-share change per node is measured on each flip alongside the trade-power/in-degree covariance, and … | MODEL | 1384 |
| Y575 | §2.8 | Total propagated power is not the quantity to watch: reorientation cannot change edge count, so the sum of … | MODEL | 1384 |
| Y576 | §2.8 | Income balance is measured on two metrics — total world collected income and its distribution across … | DESIGN | 1385 |
| Y577 | §2.9 | The build is not phases but two tracks run in parallel. | DESIGN | 1389 |
| Y579 | §2.9 | Then the b-flow and sweep with their per-tick assertions (reachability, conservation, acyclicity, … | DESIGN | 1391 |
| Y581 | §2.9 | Then: write §1.10's classified call-site list into the spec, gate income balance on both metrics, and decide … | DESIGN | 1399 |
| Y582 | §3.1 | Goal 1, world responsiveness: trade direction follows the world's current state, never authored arrows, so a … | DESIGN | 1407 |
| Y583 | §3.1 | Goal 2, realism: commodities flow differently, and China is a silk source and a spice sink at once — … | DESIGN | 1408 |
| Y584 | §3.1 | Goal 3, preserve the feedback loop: sinks accumulate, fund development and reinforce, which is how mercantile … | DESIGN | 1409 |
| Y585 | §3.1 | Goal 4, represent return flows: export regions historically imported manufactures, and vanilla cannot express … | DESIGN | 1410 |
| Y586 | §3.1 | Goal 5, route-aware direction: direction must reflect where a good can ultimately reach, not which neighbour … | DESIGN | 1411 |
| Y587 | §3.1 | Goal 6: zero authored data. | DESIGN | 1412 |
| Y588 | §3.1 | Goal 7: the game's own numbers are the model's numbers, so anything reading trade income reads the real one. | DESIGN | 1413 |
| Y589 | §3.2 | Two families of orientation fail before this one: the first fails by theorem, the second by an exact rule … | MODEL | 1417 |
| Y590 | §3.2 | Local comparison is monotone: orienting each edge by comparing its endpoints — wealth, `s − c`, or any node … | MODEL | 1421 |
| Y591 | §3.2 | Monotonicity killed v1's rank-orientation strawman and the tested `s − c` operator the same way: demand had … | MEASURED | 1424 |
| Y592 | §3.2 | Merchants cannot repair a wrong orientation — a merchant selects among existing outgoing arrows and cannot … | ENGINE | 1426 |
| Y593 | §3.2 | v1's Laplacian sink rule is exactly `(c − s)/deg > mean(neighbour φ) − min(neighbour φ)`, verified on every … | MEASURED | 1430 |
| Y594 | §3.2 | Because supply is sparse where demand is dense, that right-hand side is set by supply geography: spices are … | MEASURED | 1432 |
| Y595 | §3.2 | Under v1's Laplacian, sinks landed where the field was locally flat rather than where demand was: the … | MEASURED | 1436 |
| Y596 | §3.2 | v1 and v2 quantified the asymmetry as "supply contrast 10⁷ against demand contrast 10²–10³", but that ratio … | MODEL | 1439 |
| Y157 | §3.2 | What the ratio metric cannot see is the thing the diagnosis rests on: sparsity — most nodes produce nothing … | MODEL | 1441 |
| Y158 | §3.2 | On the contrast metric itself the demand side is the wider one, not the supply side. | MODEL | 1445 |
| Y597 | §3.2 | No parameter fixes the Laplacian's placement: an α strong enough to matter destroys §1.4's regime split. | MODEL | 1446 |
| Y159 | §3.2 | Better wealth inputs move Genoa to a co-sink at roughly ×1.7 without making demand the determinant of … | MEASURED | 1447 |
| Y160 | §3.2 | Moving the spice sink to a Chinese node takes a multiple of that node's wealth in the region of 3.6–4.8×, … | MEASURED | 1448 |
| Y161 | §3.2 | These are wealth multiples rather than demand multiples: because demand is `wealth^α` normalised over the … | MODEL | 1450 |
| Y162 | §3.2 | The four named Chinese nodes are not the cheapest — `girin` needs 3.89× and `yumen` 4.49×, both inside the … | MEASURED | 1451 |
| Y598 | §3.2 | v2 wrote "1.7× where 4–5× is needed", which compressed two different quantities into one comparison and … | MODEL | 1453 |
| Y599 | §3.2 | The conservation lesson: operators that impose node balance somewhere (the v1 solve, a min-cost flow) serve … | MODEL | 1456 |
| Y600 | §3.2 | DRAIN takes conservation from the b-flow — reachability is LP feasibility on a connected map rather than an … | MODEL | 1456 |
| Y601 | §3.2 | Of the four claims, v1 did state aggregate acyclicity as C061 ("`Φ` is a potential, so orienting edges by it … | PROCESS | 1462 |
| Y163 | §3.2 | Sink placement is a measurement on one input: on 1444, final sinks = `{selected ∩ flow-terminal} ∪ … | MEASURED | 1467 |
| Y164 | §3.2 | v5.0 tried to rescue that equality by attaching two conditions — Phase 0 a no-op and no fallback firing — and … | MODEL | 1469 |
| Y602 | §3.2 | T1, pendant importer: triangle A(+5), B(−3), D(0) with a leaf C(−2) on B; Phase 0 peels C, Phase 4 restores … | MEASURED | 1474 |
| Y603 | §3.2 | T2, free-edge race inside the 2-core: a five-cycle S1(+3)–u1(−3)–w(0)–u2(−2)–S2(+2)–S1 with a chord w–S1, … | MEASURED | 1477 |
| Y604 | §3.2 | T3, the fallback branch inside the 2-core: triangle A, B, C with `b = 0` at all three and node wealth 3, 2, … | MEASURED | 1482 |
| Y605 | §3.2 | What survives unconditionally is the subset direction within the 2-core over the set the sweep maintains: … | MODEL | 1488 |
| Y606 | §3.2 | Pendant net-importers are the only sinks outside that set. | MODEL | 1491 |
| Y607 | §3.2 | §2.8 therefore carries two runtime checks rather than one weakened one: containment inside the 2-core … | DESIGN | 1491 |
| Y608 | §3.2 | On pendant edges the Phase-4 orientation rule is the check and T1 is expected output. | DESIGN | 1494 |
| Y609 | §3.2 | Written as a single assertion with an escape clause, all three counterexamples would disappear into the … | MODEL | 1495 |
| Y610 | §3.2 | Free-edge direction is marking order under the (DEF asc, b asc, index) priority, deterministic by … | MEASURED | 1498 |
| Y611 | §3.2 | Reachability: the orientation contains the LP certificate, so every unit of demand is servable — measured … | MODEL | 1510 |
| Y612 | §3.2 | Aggregate acyclicity: `Φ_w` is itself a DRAIN orientation, so it is acyclic by the same marking-order … | MODEL | 1512 |
| Y613 | §3.2 | `Φ_w`'s marking order is a per-node scalar reproducing the DAG, for any consumer that needs a potential. | MODEL | 1514 |
| Y615 | §3.2 | The corridor runs through the Cape, which is the short route to Atlantic Europe: Malacca reaches the Channel … | MEASURED | 1521 |
| Y616 | §3.2 | Peripheral termini still exist — the LP's branch ends are consumed at the end of the line — and value only … | MODEL | 1525 |
| Y617 | §3.3 | Demand is purchasing power, and under §1.3 purchasing power is what the place is worth per year. | DESIGN | 1530 |
| Y618 | §3.3 | Wealth captures return flows for free: a sugar island's production term is carried by its trade good rather … | MODEL | 1530 |
| Y619 | §3.3 | The return-flow effect is real but modest at vanilla prices: sugar (3.0), cocoa (4.0) and coffee (3.0) are … | ENGINE | 1530 |
| Y620 | §3.3 | v1 and v2 said "negligible development but large production income", which overstated the gap. | MODEL | 1530 |
| Y621 | §3.3 | There is no colonial-nation dependency, no timeline restriction and no owner dependency. | MODEL | 1530 |
| Y622 | §3.3 | Wealth is chosen for what the place is rather than who runs it: autonomy drift, national ideas, government … | MODEL | 1532 |
| Y623 | §3.3 | What remains still moves deliberately: development changes, trade goods change, prices move with events, and … | MODEL | 1532 |
| Y624 | §3.3 | A besieged province genuinely produces less, so that volatility is economics rather than noise, and a trade … | DESIGN | 1532 |
| Y625 | §3.3 | What the model removes is the volatility that was really about ownership: a province no longer changes what … | MODEL | 1532 |
| Y626 | §3.3 | The instruction is to plan around the world rather than around the graph: the map is legible, not unchanging. | DESIGN | 1532 |
| Y627 | §3.3 | Trade income is excluded for circularity rather than speed: including it would close a … | MODEL | 1534 |
| Y628 | §3.3 | The loop still closes the long way: trade income funds development, and development raises tax and production … | MODEL | 1534 |
| Y165 | §3.3 | `cape_of_good_hope`'s `members` list has 20 entries but province 1460 is a sea zone, listed in … | ENGINE | 1536 |
| Y629 | §3.3 | Node sizes run from 19 land provinces (`cape_of_good_hope`) to 77 (`girin`) — a 4× spread with no structural … | ENGINE | 1536 |
| Y630 | §3.3 | Raising a node's aggregate wealth to a power rewards node size, so luxuries would drain toward whichever node … | MODEL | 1540 |
| Y631 | §3.3 | The distortion is measured against the per-province form the model defines rather than against equal totals: … | MODEL | 1541 |
| Y632 | §3.3 | v2 said a 77-province node "beats a 19-province node of equal total wealth by 2×"; at equal totals the … | MODEL | 1549 |
| Y633 | §3.3 | With the exponent inside the sum, superlinear demand concentrates where individual provinces are rich, and at … | MODEL | 1552 |
| Y634 | §3.4 | Production efficiency does not conjure more cloves; it means the owner extracts more ducats from the same … | MODEL | 1558 |
| Y635 | §3.4 | Owner effects do not belong in demand either: v1 and v2 excluded them from supply and then let them back in … | MODEL | 1560 |
| Y636 | §3.4 | Supply and demand are both properties of the place, so the supply-side argument applies unchanged and with … | DESIGN | 1560 |
| Y637 | §3.4 | The aggregate uses trade value rather than production income because a province's trade value is unaffected … | MODEL | 1562 |
| Y166 | §3.4 | In v1 substituting production income also measurably broke the α = 1 identity, with orientation agreement … | MEASURED | 1564 |
| Y638 | §3.5 | Anchoring at 2 ducats rather than the price median means a good's market concentration moves only when its … | MODEL | 1570 |
| Y639 | §3.5 | Under a median anchor a good could concentrate because some unrelated commodity got expensive — noise dressed … | MODEL | 1570 |
| Y640 | §3.5 | At vanilla base prices nothing sits below the 2.0 anchor: the minimum tradeable base price is exactly 2.0, … | ENGINE | 1572 |
| Y641 | §3.5 | Grain is 2.5, not the 1.25 v1 recorded; both of v1's figures were price/P₀ misread as prices. | ENGINE | 1574 |
| Y642 | §3.5 | The sublinear regime is entered only when a price event pushes a good beneath the anchor, and the shipped … | ENGINE | 1575 |
| Y167 | §3.5 | `change_price` values are fractions of the good's base price rather than ducats, and the shipped save … | ENGINE | 1581 |
| Y168 | §3.5 | The install carries 161 textual `change_price` blocks — 93 in `events/`, 14 in `missions/`, 1 in `common/`, … | ENGINE | 1587 |
| Y169 | §3.5 | Ten of the 161 never execute — four inside `effect_tooltip = "…"` strings, three inside the `effect = "…"` … | ENGINE | 1589 |
| Y170 | §3.5 | Six of the seven quoted blocks duplicate a block already counted in `events/` and the seventh names a price … | ENGINE | 1592 |
| Y171 | §3.5 | v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them; both were wrong about … | PROCESS | 1595 |
| Y172 | §3.5 | v5.0 claimed the scan was "guarded by a per-file count assertion", and there was no assertion anywhere in its … | MODEL | 1596 |
| Y173 | §3.5 | `verify6.py` checks the census only by requiring the printed total to match a computed one rather than by … | PROCESS | 1598 |
| Y174 | §3.5 | The reason a plain parse misses the quoted blocks is mechanical: `pdx.py` tokenises a quoted string as one … | MODEL | 1600 |
| Y643 | §3.5 | The history route matters: `wool`'s largest single negative is `NEW_DRAPERIES` at −0.25 in the history file, … | ENGINE | 1604 |
| Y175 | §3.5 | 1.875 is the single-key floor rather than the campaign figure: the same `1540.1.1` block also applies … | ENGINE | 1606 |
| Y176 | §3.5 | The partition needs the history value: `events/PriceChanges.txt`'s −0.20 for the same key would alone floor … | ENGINE | 1609 |
| Y644 | §3.5 | v2's 13 was right, and v3.0 reached 12 by parsing four of the five trees. | PROCESS | 1612 |
| Y645 | §3.5 | The point of having the sublinear regime is that without it a crash could only fail to concentrate a market, … | DESIGN | 1613 |
| Y646 | §3.5 | α is deliberately mild: production geography is what differentiates goods and α expresses only how … | DESIGN | 1617 |
| Y647 | §3.6 | A margin on orientation is a correctness bug rather than a tuning knob: holding an edge against the current … | MODEL | 1621 |
| Y648 | §3.6 | Tested in v1: with tol = 1e-3 and values {0, 0.0006, 0.0012}, tolerance-based tie-breaking turned an acyclic … | MEASURED | 1623 |
| Y649 | §3.6 | The node-file format represents cycles perfectly well — it is a list of named directed links with no … | ENGINE | 1625 |
| Y650 | §3.6 | What the design depends on is the engine's behaviour on a cyclic file, and that is now measured rather than … | ENGINE | 1626 |
| Y651 | §3.6 | A hand-authored two-node cycle produced `EXCEPTION_STACK_OVERFLOW` at a single exception address under 1002 … | ENGINE | 1628 |
| Y652 | §3.6 | The engine walks the node graph recursively and a cycle never terminates. | ENGINE | 1630 |
| Y653 | §3.6 | Acyclicity is enforced because the engine provably cannot survive its absence, not — as v2 had it — because … | DESIGN | 1631 |
| Y654 | §3.6 | Nothing needs to stop churn: a link whose flow-support membership alternates month to month carries … | MODEL | 1634 |
| Y655 | §3.6 | The "carries near-nothing" half is measured rather than derived, because v1's continuity argument (a … | MODEL | 1636 |
| Y656 | §3.6 | Measured on 1444: across 29 goods × 6 random 1e-9 demand nudges, zero support-membership changes moved more … | MEASURED | 1638 |
| Y657 | §3.6 | At exactly degenerate inputs — two equal-hop corridors — the map from `b` to the chosen support is … | MODEL | 1640 |
| Y1046 | §3.6 | With both cost terms and the solver's optimality tolerance pinned, the optimum is unique on the aggregate and … | MEASURED | 1642 |
| Y1047 | §3.6 | The discontinuity remains a property of the program: an input that made two routings exactly equal in cost … | MODEL | 1652 |
| Y658 | §3.6 | v1's ε is deleted because the problem it patched no longer exists: the Laplacian oriented dead branches by … | MODEL | 1655 |
| Y659 | §3.6 | DRAIN's free edges are oriented combinatorially: the priority sweep's key (DEF, b, index) is computed from … | MODEL | 1658 |
| Y660 | §3.6 | The measured count of exact key ties on 1444 data is zero, and the LP itself is deterministic (six identical … | MEASURED | 1661 |
| Y661 | §3.6 | Determinism is asserted per tick rather than approximated by a nudge. | DESIGN | 1663 |
| Y662 | §3.6 | What replaces the ε-magnitude question in §3.13 is the cross-machine question, which §2.1 narrows. | DESIGN | 1663 |
| Y1048 | §3.6 | The LP does not need to pivot identically, only to reach the same optimum, which the tie-break's margin makes … | MODEL | 1664 |
| Y663 | §3.7 | Vanilla's rule is that effective trade power counts only countries which collect or transfer downstream, and … | ENGINE | 1670 |
| Y664 | §3.7 | Under a per-good model "downstream" is per good, so at a node where your home is downstream for cloth and … | MODEL | 1672 |
| Y665 | §3.7 | Per-good eligibility returns true for some goods at every node, so no nation is ever globally inert, while … | MODEL | 1672 |
| Y666 | §3.7 | Forcing eligibility true for all goods at once would be "direction doesn't exist" rather than "everyone is … | MODEL | 1672 |
| Y667 | §3.7 | The common misstatement — that any non-collecting country with trade power is transferring — is the loose … | ENGINE | 1674 |
| Y668 | §3.8 | The vanilla gates encode an assumption that a nation pair has one global relationship to trade, upstream or … | MODEL | 1678 |
| Y669 | §3.8 | Every province is upstream for some good, because a region that receives your cloth ships you its furs. | MODEL | 1678 |
| Y670 | §3.8 | There is no fact of the matter for the gate to test, so the honest fix is to stop consulting it rather than … | DESIGN | 1678 |
| Y671 | §3.8 | Node-pair dependencies are different and keep reading `Φ_w`, because propagation is a relation between two … | MODEL | 1680 |
| Y672 | §3.8 | That distinction is easy to miss and expensive to get wrong. | DESIGN | 1680 |
| Y673 | §3.8 | Propagate Religion is node-local — it establishes a centre of conversion in the node's own province — but … | ENGINE | 1682 |
| Y674 | §3.8 | The shipped policy file gates Propagate Religion on the trade share and the node being in a trade company … | ENGINE | 1685 |
| Y675 | §3.8 | No trading policy anywhere in `00_trading_policies.txt` tests upstream/downstream. | ENGINE | 1687 |
| Y676 | §3.8 | Three of the five trading policies have no trade-share threshold at all — merchant-present only. | ENGINE | 1689 |
| Y677 | §3.8 | This is written down because the deferred artifact does not exist yet, and a community restatement of the … | DESIGN | 1690 |
| Y678 | §3.8 | Scopes read `Φ_w` rather than any-good reachability, because a gate is a boolean while a scope is a set or a … | DESIGN | 1694 |
| Y679 | §3.8 | `Φ_w` is the graph the engine already walks, so those call sites are left alone, which collapses the … | ENGINE | 1694 |
| Y680 | §3.8 | Reading `Φ_w` for scopes is legible — one map predicts where fleets sail — and balanced, because area-effect … | DESIGN | 1694 |
| Y681 | §3.8 | Any-good connectivity on 1444 data under DRAIN is 90.6% (5,723 of 6,320) of ordered node pairs, and v2's … | MEASURED | 1694 |
| Y682 | §3.9 | The installed graph exists for the engine's direction-dependent systems — propagation, fleet routes, … | DESIGN | 1698 |
| Y683 | §3.9 | What vanilla's authored arrows encode is empires pointing at the biggest cities and richest areas, with three … | ENGINE | 1699 |
| Y177 | §3.9 | On this field `english_channel` is the richest node at 316.6 and is not a sink — it drains to `genua`, 4th at … | MEASURED | 1702 |
| Y685 | §3.9 | Wealth pulls but the wealthiest node is not automatically an end: what makes an end is where the flow … | MODEL | 1702 |
| Y686 | §3.9 | `Φ_w` reuses the §1.1 operator unchanged: one implementation, one set of guarantees (LP feasibility, … | DESIGN | 1716 |
| Y688 | §3.9 | The value-weighted net flow (the sum over goods of `V_g · net_g`) is a flow, flows circulate, and it … | MODEL | 1723 |
| Y690 | §3.9 | `Φ_w` is adopted for one operator, one set of guarantees, and ends that move with the world: reusing §1.1 … | DESIGN | 1728 |
| Y181 | §3.9 | v2.1 through v4.0's "two vanilla-like ends at 1444" justification is withdrawn and must not be revived even … | MODEL | 1731 |
| Y691 | §3.9 | A difference in `Φ_w` across a link is not the net value crossing it. | MODEL | 1738 |
| Y692 | §3.9 | Realized movement follows vanilla propagation — a good can be diluted by an even split across three links … | MODEL | 1739 |
| Y693 | §3.9 | That is why the disagreement rate is measured rather than assumed, and why display policy for negative link … | DESIGN | 1741 |
| Y694 | §3.9 | Link values are realized flows, which makes conservation hold by construction. | MODEL | 1743 |
| Y695 | §3.10 | Paying countries correctly while leaving the display wrong is a strictly weaker position: node values, pie … | ENGINE | 1747 |
| Y696 | §3.10 | The engine's data model is sufficient at node level for a narrower reason than it first appears: … | MODEL | 1749 |
| Y697 | §3.10 | What factors out is `powershare_C`, a country's share among collectors, and whether a country collects is a … | MODEL | 1749 |
| Y698 | §3.10 | `income_C(n)` = the sum over goods of `value_g(n) · collected_share(n,g) · powershare_C(n)` = … | MODEL | 1752 |
| Y699 | §3.10 | That is an identity rather than a measurement: `powershare_C(n)` carries no `g`, so it factors out of the … | MODEL | 1755 |
| Y700 | §3.10 | Every term that feeds a collector's power at a node is node-wide — the merchant bonus, the off-home penalty, … | MODEL | 1755 |
| Y701 | §3.10 | One scalar per node reproduces every country's income exactly, and the engine's own math does the rest. | MODEL | 1755 |
| Y702 | §3.10 | v1 through v4.0 quoted "agreement to 5.7e-14" here and 1.4e-14 below; both are floating-point residuals of an … | PROCESS | 1755 |
| Y184 | §3.10 | Propagation is kept on a single graph, and the reason is not the one v1 through v6.0's own first draft gave. | DESIGN | 1758 |
| Y186 | §3.10 | `gulf_of_siam`'s 29 goods leave it by seven distinct downstream sets. | MEASURED | 1758 |
| Y187 | §3.10 | Per-good propagation does not break the income identity: defining `ps̄_C` as the per-good shares weighted by … | MODEL | 1758 |
| Y188 | §3.10 | Both inputs to `ps̄_C` already exist per good at write time, and §2.6 sums exactly them into `collect_pool`. | MODEL | 1758 |
| Y189 | §3.10 | The real cost is that `ps̄_C` is not derivable from trade power alone: it is value-weighted, so installing it … | MODEL | 1760 |
| Y190 | §3.10 | That is a claim about what the engine exposes rather than about a magnitude, and it is why the single graph … | DESIGN | 1760 |
| Y191 | §3.10 | Every magnitude previous versions quoted here — v1 through v3.0's "off by 5.96 ducats on a node paying ~250" … | PROCESS | 1760 |
| Y192 | §3.10 | No figure of the author's own is quoted here, because the identity holds and the objection is structural, and … | DESIGN | 1760 |
| Y703 | §3.10 | Only the decomposition by good exceeds what the engine can hold. | ENGINE | 1762 |
| Y704 | §3.11 | In vanilla, steering is outgoing-only: trade cannot be steered upstream at any amount of power, per the … | ENGINE | 1766 |
| Y705 | §3.11 | The display is not outgoing-only: the node window already lists incoming links as clickable entries. | ENGINE | 1768 |
| Y706 | §3.11 | Because only outgoing links can be steered, "assigned" and "steering" are the same condition in vanilla and … | ENGINE | 1769 |
| Y707 | §3.11 | §1.7 makes incoming entries assignable and pulls "assigned" and "steering" apart. | DESIGN | 1772 |
| Y708 | §3.11 | The engine's caravan grant fires on `merchant_present_inland` or `merchant_steering_to_inland`, with nothing … | ENGINE | 1772 |
| Y709 | §3.11 | The caravan tooltip reads as granting the bonus in the inland node ("steers towards an inland trade node will … | ENGINE | 1774 |
| Y710 | §3.11 | §2.7 item 11 settles the recipient with one merchant and two node windows, and the exposure surface is either … | DESIGN | 1776 |
| Y711 | §3.11 | §1.7's added condition is the right guard under both readings. | DESIGN | 1779 |
| Y712 | §3.11 | Caravan power is total country development divided by 3 plus policy and idea modifiers, clamped to [2, 50]. | ENGINE | 1779 |
| Y713 | §3.11 | Nineteen countries are at the caravan cap from raw 1444 development alone, and Burgundy, Korea, the Timurids … | MEASURED | 1780 |
| Y714 | §3.11 | Caravan power does not scale with node presence at all. | ENGINE | 1782 |
| Y715 | §3.11 | Requiring the merchant to steer something restores the vanilla state of affairs, and granting on bare … | DESIGN | 1784 |
| Y716 | §3.12 | The argument is consistency with §3.8: the gate compares two trade capitals on a graph where the nation-pair … | DESIGN | 1789 |
| Y717 | §3.12 | v1 claimed a stronger argument — that the gate is bistable, denial raising the colonial node's wealth and … | MODEL | 1790 |
| Y718 | §3.12 | That bistability argument is deleted: gold income never enters `wealth` at all, so neither granting nor … | MODEL | 1792 |
| Y719 | §3.12 | The engine's own denial branch confirms what denial does: "They will keep their gold income instead." | ENGINE | 1794 |
| Y720 | §3.12 | A slow second-order version survives — kept gold spent on development raises `base_tax` and `base_production` … | DESIGN | 1795 |
| Y721 | §3.12 | Inflation scales with money received relative to economy size, so universal granting hits small … | ENGINE | 1800 |
| Y722 | §3.12 | The route rule is a balance dial, since privateers skim per node passed, which is why hop counts are compared … | DESIGN | 1800 |
| Y723 | §3.13 | Prose-sourced questions are to be distrusted and nothing built on them. | DESIGN | 1804 |
| Y724 | §3.13 | Colonization's gate shape rests on one mod author's report, contradicted in-thread, and the observed … | MODEL | 1806 |
| Y725 | §3.13 | Static string-table analysis leans the same way: the only direction-refusal strings in the binary belong to … | ENGINE | 1806 |
| Y726 | §3.13 | The caller enumeration must be able to return "no colonization gate exists" as a successful result. | DESIGN | 1806 |
| Y727 | §3.13 | Derived questions are probably right and cheaply falsifiable. | DESIGN | 1808 |
| Y728 | §3.13 | The `TRADE_PROPAGATE_THRESHOLD` file value and the documented raw requirement differ by exactly the … | ENGINE | 1810 |
| Y729 | §3.13 | Propagation is one hop and cannot chain, so something else in pass 2 imposes its ordering; eligibility … | ENGINE | 1811 |
| Y730 | §3.13 | The debugger-only list is shorter than v1 believed: of §2.7, only pass caching, pass-2 content, write windows … | DESIGN | 1813 |
| Y731 | §3.13 | Items 11–15 need a save, a tooltip, or one file edit, and the propagation-threshold and one-hop questions are … | DESIGN | 1814 |
| Y732 | §3.13 | Three of the cheap probes — caravan recipient, cyclic file, incoming-link button — change what this spec says. | DESIGN | 1816 |
| Y733 | §3.13 | One question is open in the v6.0 wealth model, and it is a question rather than a number, because §1.3 … | DESIGN | 1819 |
| Y193 | §3.13 | The one open wealth question is now a design question rather than a classification one: should any source … | DESIGN | 1821 |
| Y195 | §3.13 | The keys `trade_goods_size` and `trade_goods_size_modifier` are granted in many places: buildings, event … | ENGINE | 1824 |
| Y194 | §3.13 | v3.0 through v5.0 tried to admit the province-scoped subset by rule, and that rule was wrong in both … | MODEL | 1827 |
| Y196 | §3.13 | Re-admitting any of those sources re-admits the maintenance burden with it, and the question to settle first … | DESIGN | 1829 |
| Y734 | §3.13 | Settled and moved: `local_production_efficiency` from a trade good is outside wealth, because Barcelona's … | ENGINE | 1834 |
| Y735 | §3.13 | Settled and moved: `TAX_COEFF` is 1.0 across the development range — `Base: 0.49 (Yearly 6.00)` at `base_tax` … | ENGINE | 1837 |
| Y736 | §3.13 | `k`, `α_min` and `α_max` remain unresolved; the test is whether they produce the intended three-regime split, … | DESIGN | 1843 |
| Y738 | §3.13 | Whether `α_min` ever bites is now bounded from files: the sublinear regime is reachable through vanilla price … | ENGINE | 1862 |
| Y198 | §3.13 | v2 said Beijing "holds the richest single province", which it does not — that is `hangzhou` — and no … | PROCESS | 1876 |
| Y743 | §3.13 | The open multiplayer item is build discipline rather than LP pivot determinism, which §2.1 retires. | DESIGN | 1879 |
| Y1049 | §3.13 | What is open is whether the shipped solver build does runtime CPU dispatch or threads its reductions — either … | MODEL | 1881 |
| Y1050 | §3.13 | Also open is whether the DLL reproduces the reference implementation's orientation exactly, which cannot be … | DESIGN | 1883 |
| Y744 | §3.13 | AI merchant reassignment cadence is open. | DESIGN | 1885 |
| Y745 | §3.14 | The two ends of a link never compete: a merchant at `n` on {n,m} moves goods oriented n to m, one at `m` … | MODEL | 1889 |
| Y746 | §3.14 | One precompute serves every country: for each good, a backward pass over its DAG gives `S_g[n][H]`, the … | MODEL | 1891 |
| Y747 | §3.14 | `collected_share(n,g)` reaches 1 at `g`'s sink, which terminates the recursion. | MODEL | 1891 |
| Y748 | §3.14 | All three survival-table inputs are country-independent aggregates, so this is one table rather than one per … | MODEL | 1891 |
| Y749 | §3.14 | v1 and v2 both said 0.75 MB, which is the single-precision figure; the rest of the solver is double precision … | MODEL | 1891 |
| Y750 | §3.14 | Scoring reads the survival table for both steering and collecting, so the opportunity cost of collecting … | MODEL | 1893 |
| Y751 | §3.14 | The off-home penalty is a power modifier rather than a haircut on value: it reduces the country's trade power … | ENGINE | 1895 |
| Y752 | §3.14 | Scoring a collect candidate as value × share × 0.5 is wrong; the halving must be applied to power and the … | MODEL | 1895 |
| Y753 | §3.14 | That is also why the off-home penalty falls out of the survival table at all: the table is built from … | MODEL | 1895 |
| Y754 | §3.14 | The home-node bonus is voided entirely by placing any collector outside the home node, so a collect … | ENGINE | 1897 |
| Y755 | §3.14 | Greedy scoring against a moving field can oscillate between AIs; damping the shares between passes should … | MODEL | 1897 |
| Y756 | §3.14 | Reassignment cadence is undecided and is the one item left for the human, because merchants take travel time … | DESIGN | 1899 |
| Y757 | §3.14 | Mirroring vanilla's cadence is the stated preference, but the relevant define was not located in the visible … | DESIGN | 1901 |
| Y758 | §3.14 | The computed alternative moves a merchant when `(V_new − V_incumbent) × expected_tenure > V_incumbent × … | MODEL | 1902 |
| Y759 | §3.14 | The argument for computing the cadence is that vanilla's cadence was tuned against a graph that never moves, … | DESIGN | 1904 |
| Y760 | §3.15 | The v1 Laplacian potential as the orientation core is rejected: its sink placement is topological, sinks … | MODEL | 1908 |
| Y200 | §3.15 | v3.0 and v4.0 repeated the 10⁷ versus 10²–10³ ratio in this entry while v4.0's own §3.2 was withdrawing it. | PROCESS | 1912 |
| Y199 | §3.15 | The Laplacian entry maintains no copy of the contrast measurement — §3.2 carries it — and with v1's ε floor … | MODEL | 1914 |
| Y201 | §3.15 | `cloves` has a single producer and so no contrast to measure at all, which is the sparsity point in miniature. | MODEL | 1915 |
| Y761 | §3.15 | The Laplacian was diagnosed, measured and replaced, and what it did guarantee — 100% reachability via … | MODEL | 1917 |
| Y762 | §3.15 | Pure min-cost-flow orientation with no sweep is rejected: it orients only the roughly 79-edge support (a … | MEASURED | 1921 |
| Y202 | §3.15 | Ranked orientation wins the sink-demand alignment statistics — a far higher share of top-demand nodes in its … | MODEL | 1925 |
| Y203 | §3.15 | Seeded basin growth converges flow to the chosen seeds and starves everything off a supply-to-seed path, … | MODEL | 1934 |
| Y763 | §3.15 | Seeded basin growth's useful ideas — HHI-adaptive sink count and stall self-correction — survive inside … | MODEL | 1936 |
| Y764 | §3.15 | DEF-descending free-edge priority is rejected as measurably worse: on the certificate, unmet demand is … | MODEL | 1940 |
| Y765 | §3.15 | Authored demand weights are rejected: authored data in a model that needs none. | DESIGN | 1945 |
| Y766 | §3.15 | Trade income inside `wealth` is rejected: it reintroduces flow-demand-orientation-flow circularity, and the … | MODEL | 1947 |
| Y767 | §3.15 | Node-level α is rejected: it makes demand concentration a function of how finely the map was sliced. | MODEL | 1949 |
| Y768 | §3.15 | A median-relative α anchor is rejected: a good's concentration would shift because other goods changed price. | MODEL | 1951 |
| Y769 | §3.15 | α floored at 1 is rejected: it discards the cheap-bulk regime. | DESIGN | 1953 |
| Y770 | §3.15 | Production income as the aggregate supply term is rejected because it makes world supply depend on owners' … | MODEL | 1955 |
| Y771 | §3.15 | A τ margin on orientation is rejected: it manufactures cycles. | MODEL | 1957 |
| Y772 | §3.15 | Uniform supply in the aggregate solve is a v1 entry, moot in v2 and retained for history: it answered a … | MODEL | 1959 |
| Y205 | §3.15 | The 3-mass gravity field over the top-3 pairwise-unconnected demanders reproduces whatever end count it is … | MODEL | 1970 |
| Y775 | §3.15 | The emergent-count wealth good replaced the pinned-count fields. | MODEL | 1979 |
| Y776 | §3.15 | A vestigial in-game economy with net treasury settlement is rejected: correct treasuries, wrong displays, … | DESIGN | 1981 |
| Y778 | §3.15 | Node-level collect/transfer rules are rejected: the collect/transfer split is per good because whether a good … | MODEL | 1989 |
| Y779 | §3.15 | Treating unsteered goods as fully collected is rejected: transfer power does not come from merchants, and … | MODEL | 1991 |
| Y780 | §3.15 | Undirected shortest path as the primary fleet route is rejected: a geodesic over a directional structure can … | MODEL | 1993 |
| Y781 | §3.15 | Automatic per-good merchant targeting is rejected: one vanilla arrow click already achieves per-good … | DESIGN | 1995 |
| Y782 | §3.15 | Companion-overlay merchant assignment is rejected: assignment must stay a game action or vanilla knowledge … | DESIGN | 1997 |
| Y783 | §3.15 | Emission-time pruning of near-flat links is rejected: peripheral termini are intended consumption, and the … | DESIGN | 1999 |
| Y784 | §3.15 | Edge conductance / weighted Laplacian stays rejected: v1 rejected it as "too much mechanical surface", the … | MODEL | 2004 |
| Y785 | §3.15 | Staged delivery is rejected: the intermediate states are different designs sharing a solver rather than … | DESIGN | 2009 |
| Y786 | §3.15 | "The aggregate map is not a DAG" is still an error, with v1's reason corrected: v1 defended it by claiming … | MEASURED | 2011 |
| Y787 | §3.15 | The aggregate is a DAG because `Φ_w` is a DRAIN orientation, acyclic by the marking-order argument, whose own … | MODEL | 2013 |
| Y788 | §3.16 | v1 carried an evidence standard — "every retraction traced to a premise that entered through prose; nothing … | MODEL | 2019 |
| Y789 | §3.16 | At least fifteen non-prose claims failed, by three distinct mechanisms. | MODEL | 2021 |
| Y790 | §3.16 | Mechanism 1, file values remembered from an older patch: the 75% overseas autonomy floor is pre-Common-Sense, … | ENGINE | 2024 |
| Y791 | §3.16 | Mechanism 2, file values transformed and then reported as raw: v1's grain (1.25) and livestock (1.00) base … | ENGINE | 2026 |
| Y792 | §3.16 | Mechanism 3, the spec's own algebra instantiated without checking the instantiation: ε provably preserved the … | MODEL | 2029 |
| Y206 | §3.16 | Implemented as written, v1's ε left the α = 1 identity's residual at 1e-5 against v1's ε of 1e-6, and would … | MEASURED | 2031 |
| Y793 | §3.16 | One of only three claims carrying `verified (method unstated)` provenance — Propagate Religion's gating — … | MODEL | 2034 |
| Y794 | §3.16 | The real signal in the audit was provenance: nine of the sixteen refuted ENGINE claims were UNSOURCED, and … | MODEL | 2035 |
| Y795 | §3.16 | The rule is not "trust derivations" and not "distrust prose" but that anything which entered without a … | DESIGN | 2039 |
| Y796 | §3.16 | Every engine fact in this spec must carry its source — a file path, a binary string, or a named observation — … | DESIGN | 2040 |
| Y797 | §3.16 | The gap that mattered more than any refutation: v1 never stated what determines sink placement, so the claim … | PROCESS | 2043 |
| Y798 | §3.16 | The audit found that flaw only by running the solver and asking why the output looked wrong. | MODEL | 2046 |
| Y799 | §3.16 | The standing repair is in this document's structure: what determines sink placement, what determines … | PROCESS | 2046 |
| Y800 | §3.16 | Each of those properties is provable or measured-and-labelled and each is checked at runtime — as an … | DESIGN | 2050 |
| Y801 | §3.16 | The next audit's first question should be which property of the output this spec still does not state. | DESIGN | 2054 |
| Y802 | §3.16 | The cautionary case is now closed and it closed the other way: the propagation source condition was corrected … | MODEL | 2057 |
| Y803 | §3.16 | Probe 15 settled it: the qualifier is descriptively false, since a country with no provinces and no merchant … | ENGINE | 2060 |
| Y804 | §3.16 | The lesson is not the one the case was filed under: it was filed as "agreement between reviewers is not … | MODEL | 2065 |
| Y805 | §3.16 | A localisation string describes intent, not behaviour. | ENGINE | 2068 |
| Y806 | §3.16 | Sources are necessary but not sufficient, and an engine fact sourced to a string is settled only when … | DESIGN | 2068 |
| Y807 | §3.16 | During the declaration-order test a permuted node file differed from vanilla on 61 of 80 nodes — a real … | ENGINE | 2072 |
| Y808 | §3.16 | That measurement was meaningless, because two runs of the same vanilla build differ on 49 of 80 nodes by up … | ENGINE | 2074 |
| Y809 | §3.16 | A measurement without a null comparison is not evidence. | DESIGN | 2077 |
| Y810 | §3.16 | Every measured claim in this document that could vary run to run should carry the control that bounds its … | PROCESS | 2078 |

## REWORDED — same proposition, different words

| ID | § | claim | rewording | type | provenance | line |
|---|---|---|---|---|---|---|
| Y012 | §0 | Every graded claim from `../v5-owner-agnostic/validation-v5.md` — 22 refuted, 39 partial, 1 unverifiable — is folded through, and `fixes-agreed.md` … | gains "62 in all" (the sum of the unchanged 22/39/1) — figures and substance identical | PROCESS | cited to `../v5-owner-agnostic/validation-v5.md` and `fixes-agreed.md` | 76 |
| Y017 | §0 | Some figures carry a script attribution instead of a guard, and a few carry neither. | "a few carry neither" → "some carry neither"; same proposition | PROCESS | unsourced | 93 |
| Y224 | §1.1 | Phase 0 repeatedly removes degree-1 nodes, orienting each pendant edge by the sign of its absorbed subtree balance (net exporter toward core, net … | "orienting each pendant edge by" → "determining each pendant edge's orientation from"; same rule | MODEL | unsourced | 112 |
| Y247 | §1.1 | Phase 4 un-peels the Phase-0 pendants in reverse order. | "Phase 4 — un-peel" → "Phase 4 — un-peel and emit. Restore the Phase-0 pendants in reverse order"; same operation | MODEL | unsourced | 171 |
| Y269 | §1.1 | The LP is deterministic on one machine and one build — six identical solves gave one orientation on the reference implementation. | parenthetical recast as a clause: "six identical solves returning one orientation on the reference implementation"; same measurement | MEASURED | named observation (six solves on the reference implementation; no script at this line) | 233 |
| Y279 | §1.3 | Wealth reads no autonomy, no production efficiency, no national ideas, no estate or government modifiers, and no technology. | the exclusion list gains "no unrest" — an exclusion the document already asserted elsewhere (§1.3), restated into this list | MODEL | unsourced | 258 |
| Y050 | §1.3 | Province condition is the one thing besides development and the good that wealth reads: five static modifiers describe a province's own state, all … | counting frame recast: "five describe …, four of the five are applied" → "four static modifiers are applied … a fifth, `unrest`, is defined in the same file and is deliberately not read"; same substance (four applied, unrest excluded, all defined in the file) | ENGINE | `common/static_modifiers/00_static_modifiers.txt` | 334 |
| Y980 | §1.3 | Revolt risk is not a property of the place: in play it carries separatism from recent conquest, unaccepted culture, wrong religion and nationalism, … | expanded: adds "and the point of a revolt is that the rebels want the owner changed"; same argument (restated §0 L53-54) | MODEL | derivation | 361 |
| Y984 | §1.3 | The effect `unrest` would buy is already bought: conquest costing a province its wealth is delivered by `devastation`, `occupied` and `under_siege`, … | tightened: "all three of which are properties of the place and all three of which the model applies" → "all three properties of the place, and all three applied" (restated §0 L56-57) | MODEL | derivation | 369 |
| Y058 | §1.3 | The condition modifiers are what make the map answer to war: §1.2's volatility and §3.3's "a besieged province genuinely produces less" both rest on … | referent made explicit: "These are what make the map answer to war" → "`devastation`, `occupied` and `under_siege` are what make the map answer to war" | DESIGN | derivation | 379 |
| Y309 | §1.5 | Whether the per-province production-income field nevertheless carries the gold figure before the country-level split is still unknown, and is moot … | "it is also moot" → "it does not matter"; same proposition | MODEL | unsourced | 466 |
| Y319 | §1.5 | v2.1 held that a latent good leaves `Φ_w` unaffected because "`Φ_w` reads wealth, not goods"; that was true under v2.0's `Φ_ord`, where `V_g = 0` … | "true under v2.0's `Φ_ord`, where `V_g = 0` gave a latent good zero weight" → "held under v2.0's aggregate, which weighted each good by `V_g` and so gave a latent good none"; the operator name dropped, same mechanism | MODEL | derivation | 495 |
| Y110 | §1.6 | The table is to be read as a direction rather than a trajectory: it scales all 824 counted European provinces by one factor at once, which is not how … | "Read the table as a direction" → "Read this as a direction"; "the row boundaries are a property of one synthetic experiment" → "the interval quoted above is a property of one synthetic sweep"; same scoping | DESIGN | derivation | 624 |
| Y340 | §1.6 | These are properties of this snapshot rather than constants of the model — what one field yielded under one scaling, which a different world state … | "These are properties of this snapshot" → "It is what one field yielded under one scaling"; same proposition, singular referent | DESIGN | unsourced | 643 |
| Y112 | §1.6 | Because §1.3's wealth is linear in development, scaling development and scaling wealth are the same operation here — maximum difference 0.0 across … | "the distinction that made v5.0's version of this table wrong" → "… of this experiment wrong"; figure (max difference 0.0) unchanged | MEASURED | numerical test (block cites `europe.py`) | 644 |
| Y465 | §2.2a | Marking order reproduces the DAG on a 2-core map and fails where Phase 0 acts, because pendants have no marking order so `Φ_ord`-style order … | "`Φ_ord`-style order comparison is undefined on pendant edges" → "comparing nodes by marking order is undefined on pendant edges"; operator name dropped, same fact | MODEL | derivation | 1023 |
| Y1039 | §2.3 | The choice of normalisation is a third arbitrary decision with an observable consequence where before it was free; min-max is what the implementation … | "It is recorded here rather than defended" → "The choice is recorded rather than defended"; same stipulation and same expectation for implementers | DESIGN | unsourced | 1174 |
| Y614 | §3.2 | Conduits still work: a node with `s = c = 0` (the 1444 Cape exactly) carries flow through, with in- and out-degree both nonzero for all 29 goods. | reframed: the degree evidence is kept verbatim (in/out-degree nonzero for all 29 goods) but demoted to "the weaker evidence and … the only kind offered before"; the conduit claim itself unchanged | MEASURED | numerical test (degree); `round6.py` for the new flow-level evidence | 1516 |
| Y740 | §3.13 | Unclamped α-squared is a demand-model decision, because luxuries become court goods. | "Its costs are real and recorded" → "Its costs are qualitative and unchanged"; the α²-is-a-demand-model-decision point itself unchanged | DESIGN | derivation | 1872 |
| Y742 | §3.13 | The baseline does not adopt the calibration, and adopting it is a §1.4 decision rather than a solver knob. | "adopting it is a §1.4 decision, not a solver knob" → "adopting it is a §1.4 decision" (the "not a solver knob" tail moved into the α² clause); same stipulation | DESIGN | unsourced | 1876 |

## CHANGED — still asserted, but what it asserts moved

| ID | § | claim (census wording) | old → new | type | provenance | line |
|---|---|---|---|---|---|---|
| Y215 | §0 | v2.1 replaced the installed aggregate `Φ_ord` (the value-weighted marking order) with `Φ_w`, DRAIN run once more with wealth itself as the good. | old: names the superseded aggregate — "`Φ_ord` (the value-weighted marking order) gives way to `Φ_w`" → new: "replaces the installed aggregate with `Φ_w`"; the old operator is no longer named | MODEL | unsourced | 10 |
| Y010 | §0 | Prose convention: no maintained figures for any rejected operator — §3.15's graveyard keeps its design arguments and loses its measurements, covering … | old: graveyard coverage list opens with `Φ_ord` ("covers `Φ_ord`, the gravity kernels, …") → new: list is the gravity kernels, the v1 Laplacian, RANK and the seeded basins; `Φ_ord` no longer named | DESIGN | unsourced | 68 |
| Y229 | §1.1 | Phase 1 carries two knobs: a demand-mass quantile `ρ` defaulting to 1.0 and a cluster dilation radius `r` defaulting to 0. | old: Phase 1 carries two knobs — demand-mass quantile `ρ` (default 1.0) and dilation radius `r` (default 0) → new: one knob, `r` (default 0); `ρ` withdrawn as a parameter the shipped operator never had | MODEL | unsourced | 122 |
| Y262 | §1.1 | That free-edge direction is a function of the graph and the balances alone — that the node indexing never decides — is measured rather than proved … | old: "zero orientation changes under scheduler permutations" (count unstated) → new: "zero orientation changes over 145 scheduler permutations (29 goods × 5)", cited to `props6.py` | MEASURED | `props6.py` | 209 |
| Y978 | §1.1 | At those values the cost spread is under a tenth of a percent of the base cost, so the routing is within that factor of fewest-hop — which makes … | old: the spread is under a tenth of a percent of the base cost, so the routing is within that factor of fewest-hop → new: the bound is the interval `[1, 1 + TIE_EPS + TIE_EPS2]` itself; no percentage is derived, because the spread relative to base cost restates `TIE_EPS`. The "approximation with a stated bound, price of a unique optimum" core is retained | MODEL | derivation | 221 |
| Y037 | §1.3 | `tax_value(p) = TAX_COEFF · base_tax(p) · (1 + sum of province-state tax modifiers)`. | old: `tax_value(p) = TAX_COEFF · base_tax(p) · (1 + Σ province-state tax modifiers)` → new: `tax_value(p) = TAX_COEFF · base_tax(p)` — no modifier at all (restated L49-50, L349, L955) | MODEL | unsourced | 288 |
| Y979 | §1.3 | `unrest` is live at the 1444 start and is deliberately not read. | old: `unrest` is live at the 1444 start and is deliberately not read → new: `unrest` is deliberately not read; its 1444 liveness (the 21-province reading) is no longer asserted — the revolt-risk accounting is withdrawn | MODEL | unsourced | 337 |
| Y051 | §1.3 | The condition modifiers and their targets: `devastation` `trade_goods_size_modifier = -2` scaled by the devastation level into `goods_produced`; … | old: five-row table; `occupied` enters both terms; `unrest` row grants `local_tax_modifier = -0.02` per point into `tax_value` → new: four-row table; `occupied` enters `goods_produced` only, its tax half "granted by the file and not read"; no `unrest` row | ENGINE | `common/static_modifiers/00_static_modifiers.txt` | 341 |
| Y053 | §1.3 | `occupied` and `unrest` touch the tax term; the other three reach `goods_produced` alone. | old: `occupied` and `unrest` touch the tax term; the other three reach `goods_produced` alone → new: no modifier reaches the tax term at all; all four rows enter `goods_produced` | MODEL | derivation | 348 |
| Y981 | §1.3 | `solver.py`'s `STATE_TAX_MOD` carries `occupied` alone, so four of the five rows in the table are applied. | old: `solver.py`'s `STATE_TAX_MOD` carries `occupied` alone (four of five applied) → new: `STATE_TAX_MOD` is empty, kept as an empty declaration | MODEL | `solver.py` | 352 |
| Y079 | §1.6 | At `α_Φ = 2.0` the 1444 field gives two sinks and a modestly grown Europe gives two, three or five, so neither the count nor the placement is fixed … | old: a modestly grown Europe gives two, three or five sinks (the Europe table below) → new: scaling European development alone moves the count both up and down before it settles back at two (the sweep below) | MEASURED | `europe.py` (the sweep below) | 523 |
| Y109 | §1.6 | Observed on the 1444 field holding `α_Φ = 2.0` and scaling European development only over 824 counted European provinces, with bisected boundaries, … | old: bisected-boundary table, ten interval rows from ×1.00 to ×2.50, each row a sink set → new: the table is withdrawn ("A table of interval boundaries was published here and is withdrawn"); the sweep is re-reported on a uniform 0.001 grid ×1.000–×2.600, and the one interval still quoted is ×1.973–×2.456 (three European ends, none in Asia) | MEASURED | `europe.py` | 621 |
| Y111 | §1.6 | The path is not monotone — `hangzhou` leaves at ×1.19, returns at ×1.95 and leaves again; `gulf_of_siam` holds an end across ×1.19–×1.38 and nowhere … | old: `hangzhou` leaves at ×1.14/×1.19, returns at ×1.95; `gulf_of_siam` holds ×1.19–×1.38; two intervals narrower than ×0.03 → new: same non-monotonicity asserted without boundary figures; "several intervals narrower than ×0.01 carry sets that appear once" | MEASURED | `europe.py` (block citation) | 627 |
| Y344 | §1.6 | The 1444 map draws the pre-Columbian trade geography unprompted. | old: "the 1444 map draws THE pre-Columbian trade geography UNPROMPTED" → new: "draws A RECOGNISABLE pre-Columbian trade geography" — the definite claim and "unprompted" both softened | MEASURED | the routes enumerated in the same paragraph (`measure6.py` block) | 656 |
| Y346 | §1.6 | That no Europe→sink route passes the Cape is what a 1444 map should say, and it is the one place in this section where a universal is asserted, … | old: "it is the one place in this section where a universal is asserted, because here the whole set was enumerated" → new: "asserted as a universal because the whole set was enumerated rather than sampled — which is the only ground on which this document states one"; the uniqueness moved from section-local to a document-wide ground | DESIGN | unsourced | 667 |
| Y119 | §1.6 | Scaling the 18 western and central European nodes rather than European provinces makes `genua` the sole sink from about ×1.55, while scaling all 22 … | old: `genua` sole sink from about ×1.55; scaling all 22 gives no sole sink below ×4 — "the eastern four keep pulling ends of their own" → new: sole sink from ×1.52, continuous to the top of the swept range; all-22 gives no sole sink below ×25, the set settling at `{genua, rheinland}` from about ×2.50; the eastern-four clause refuted and deleted | MEASURED | `round6.py` | 682 |
| Y412 | §1.10 | Scripted content reaches nodes only structurally, through `home_trade_node`, `any/random/every_active_trade_node`, `*_trade_node_member_province` and … | old: unqualified enumeration — "reaches nodes only structurally: `home_trade_node`, `any/random/every_active_trade_node`, `*_trade_node_member_province`, and `highest_value_trade_node`" → new: "through four families" with the member-province family spelled out (`any/random/every/all_…`) and an explicit caveat that the bare-word token scan cannot see every compound key, so "bounded by class" holds only for the families named | ENGINE | `round6.py` (the scan); the four trees | 840 |
| Y129 | §2.2 | Solver item 4 computes `TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production · (1 + province-state goods modifiers) … | old: solver wealth formula carries `(1 + province-state tax modifiers)` on the tax term → new: `TAX_COEFF · base_tax + …` — "The tax term takes no modifier at all" | MODEL | unsourced (per §1.3) | 954 |
| Y130 | §2.2 | The only modifiers in scope are the five that describe the province's own condition, of which the reference implementation applies four; at 1444 … | old: five modifiers in scope, reference implementation applies four; at 1444 `devastation` live on eleven and `unrest` on twenty-one, not read → new: four modifiers in scope, all four reaching `goods_produced`; at 1444 only `devastation` is live, on eleven; `unrest` defined and not read | MEASURED | per §1.3 (`round6.py` there) | 956 |
| Y132 | §2.2 | Measured on the reference implementation (scipy/HiGHS plus the deterministic sweep, one machine): of order 0.1 s for all 29 goods, and single-digit … | old: "single-digit milliseconds per good on average" → new: "milliseconds rather than tens of milliseconds per good on average", with the withdrawal stated: two of the three replicates reach 10.5 and 10.8 ms, so "single-digit" is deliberately not claimed | MEASURED | named observation (the three 12-run replicates) | 975 |
| Y480 | §2.3 | DRAIN's three knobs sit at their defaults: demand-mass quantile `ρ = 1.0`, cluster dilation `r = 0`, and the zero-flow tolerance `1e-11`. | old: DRAIN's three knobs at defaults — `ρ = 1.0`, `r = 0`, zero-flow tolerance 1e-11 → new: two knobs — `r = 0` and the 1e-11 tolerance; `ρ` withdrawn as never shipped | MODEL | unsourced | 1076 |
| Y481 | §2.3 | The zero-flow tolerance is not purely numerical: it is an absolute threshold, so it couples to the scale of `b`. | old: the tolerance is "not purely numerical: it is an absolute threshold, so it couples to the scale of `b`. See §1.6's scale-invariance note and §3.13" (open) → new: "an absolute threshold rather than a relative one; §3.13 records why that is settled rather than open" | MODEL | derivation | 1077 |
| Y482 | §2.3 | A measured calibration option that moves all three knobs plus α's clamp is recorded in §3.13, and the baseline does not use it. | old: a measured calibration option "moves all three [knobs] plus α's clamp" → new: the option "replaces Phase 1, moves the zero-flow tolerance and removes α's clamp"; still recorded in §3.13, still not used by the baseline | DESIGN | unsourced | 1080 |
| Y999 | §2.3 | A structured second term does not do this: `+ TIE_EPS²·abs(w[u] − w[v])` was tried and rejected, because it makes all 159 arc costs distinct where … | old: the structured term makes all 159 arc costs distinct where the shipped cost leaves 3 pairs equal, and leaves 72 of 232 per-good supports moving → new: BOTH costs make all 159 edge costs distinct (the 3-pairs-equal claim gone); the structured term leaves 11 of 29 goods admitting an alternative optimum against the shipped term's 1 (`paper`). "Genericity, not distinctness" retained | MEASURED | `round6.py` | 1116 |
| Y1038 | §2.3 | Measured across the three normalisations — maximum, mean and world total — the aggregate `Φ_w` is unchanged, 0 of 159 edges differing, but 5 of the … | old: across the three normalisations the aggregate `Φ_w` is unchanged (0 of 159 edges) and 5 of 29 per-good graphs differ → new: dividing by the world total moves the aggregate by 7 of 159 edges, and 13 of 29 per-good graphs move under at least one candidate | MEASURED | `round6.py` | 1160 |
| Y538 | §2.8 | No Chinese node holds a spices sink in either configuration: under the §3.13 α-calibration `spices` sinks at Genoa alone and it is `cloves` that … | old: under the §3.13 α-calibration `spices` sinks at Genoa alone and `cloves` moves to Deccan; the v1 China+Europe expectation "not recovered by the calibration either" → new: under the calibration `spices` sinks at `doab` and `genua`, and `cloves` moves to `beijing`; the expectation "is met by no single good" — a Chinese end on cloves and a European one on spices, in two different graphs | MEASURED | numerical test (calibration re-run after §2.3's cost reached its Phase 2) | 1347 |
| Y152 | §2.8 | Sinks are `{selected ∩ flow-terminal} ∪ promoted`, 2 to 8 per good, and high-demand nodes are sinks at 19.8% among each good's top eight demanders … | old: high-demand nodes are sinks at 19.8% among top-eight demanders (46 of 232) against 6.9% among bottom-eight (16 of 232) → new: 19.4% (45 of 232) against 7.3% (17 of 232), cited to `round6.py` | MEASURED | `round6.py` | 1348 |
| Y154 | §2.8 | Zeroing `hangzhou`-node development moves the `Φ_w` sinks from `{genua, hangzhou}` to `{genua, gulf_of_siam}`, with 30 of 159 edges flipping. | old: 30 of 159 edges flip when `hangzhou` is zeroed → new: 32 of 159 (`round6.py`) | MEASURED | `round6.py` | 1352 |
| Y543 | §2.8 | v2 through v4.0 said zeroing `beijing` "moves nothing"; it does, and the asymmetry is which node keeps its end rather than whether the map moves. | old: "v2 through v4.0 said zeroing `beijing` 'moves nothing'" → new: "v4.0 said zeroing `beijing` 'moves nothing'" — the attribution narrowed to one version (and the correction now restates the 8-edge figure inline) | PROCESS | read from the prior spec versions | 1352 |
| Y1045 | §2.8 | That configuration can regress silently on a solver upgrade: at HiGHS's 1e-7 default the margin sits inside the tolerance and the solver may return a … | old: the check "asserts the option is set and that the returned objective's reduced costs clear the tolerance" → new: assert the option is set, then classify each off-support arc's reduced cost in three branches (halt / report / halt), because a single "clears the tolerance" test halts on correct behaviour — the genuine-tie report branch is the state `paper` is in today | MODEL | derivation plus `round6.py` | 1368 |
| Y578 | §2.9 | The solver track starts with the defines parser, because §2.3 makes every constant a runtime read, so the eligibility threshold, propagation share, … | old: "§2.3 makes every constant in the model a runtime read" → new: "every define the model reads" is a runtime read, with `TAX_COEFF` the named exception — the one constant in no shipped file that has been found | DESIGN | derivation (§2.3) | 1391 |
| Y580 | §2.9 | The memory track is the §2.7 probe session, all ten items on one trace. | old: the memory track is the §2.7 probe session, "all ten items on one trace" → new: "the twelve items still open there (1–11 and 16) on one trace" | DESIGN | unsourced | 1397 |
| Y687 | §3.9 | Three aggregates were tested; one is impossible and one was superseded. | old: "Three aggregates were tested; one is impossible and one was superseded" → new: "Two aggregates were tested and rejected before the third was adopted" | MODEL | unsourced | 1721 |
| Y689 | §3.9 | The value-weighted marking order `Φ_ord` is acyclic for free and scores higher than `Φ_w` on self-coherence with the per-good graphs, which is the … | old: `Φ_ord` is acyclic for free AND "scores higher than `Φ_w` on self-coherence with the per-good graphs — that is the cost of the trade and it is not disputed" → new: acyclic for free only; the self-coherence comparison is no longer made anywhere in the document | MODEL | derivation | 1725 |
| Y178 | §3.9 | `Φ_ord`'s ends are artifacts of sweep scheduling rather than places, and the sharpest evidence is what relabelling does to them: its end count and … | old: `Φ_ord`'s ends are artifacts of sweep scheduling, the sharpest evidence being relabelling (end count and set move with node order where `Φ_w`'s do not, §2.4) → new: the ends are "a function of the order Phase 3 pops its ready queue, which is a design choice inside the operator" — now derived from the definition, "needs no measurement"; the relabelling evidence dropped | MODEL | derivation | 1725 |
| Y180 | §3.9 | No figure is quoted for any of that: the operator is not installed, its numbers moved with every change to the wealth field, three successive audits … | old: no figure quoted, four reasons — not installed, numbers moved with every field change, three audits spent effort recounting, the argument depends on none → new: "That follows from the definition and needs no measurement" (§3.15: "The rejection is structural, so no figure is kept for it") | DESIGN | unsourced | 1727 |
| Y182 | §3.9 | What the trade costs is self-coherence with the per-good graphs, which the superseded marking-order aggregate scores higher on; what it buys is one … | old: "What the trade actually costs is self-coherence with the per-good graphs, which the superseded marking-order aggregate scores higher on; what it buys is …" → new: only the buys half — "What it buys is one operator, one set of guarantees, and ends that sit where the wealth is" | DESIGN | unsourced | 1735 |
| Y185 | §3.10 | Reading the one installed graph leaves the propagated term good-independent, so the identity holds by construction and in doubles to within one to … | old: "the identity holds by construction, and in doubles to within one to three units in the last place" → new: "the identity holds by construction." — the doubles residual clause deleted with the withdrawn measurement | MODEL | derivation | 1758 |
| Y737 | §3.13 | The zero-flow tolerance is scale-coupled: §2.3 records it as absolute rather than purely numerical (v2.1 filed it as numerical-only), and being … | old: scale-coupled and UNDECIDED — "either normalise `b` to a fixed scale before the solve or make the tolerance relative" → new: CLOSED — the hazard is not reachable from inside the model (no scale knob exists; see Y1137-Y1138), and the entry is kept "because the reasoning is what stops it being reopened" | MODEL | derivation (plus the §2.1 margin measurement) | 1844 |
| Y739 | §3.13 | A measured calibration exists that makes sink counts track price — span exactly 1..5, spearman(price, sinks) = −0.20 — with α unclamped at exponent 2 … | old: the calibration "makes sink counts track price — span exactly 1..5, spearman(price, sinks) = −0.20", with α unclamped (cloves α = 16), ρ = 0.5, twig tolerance 3e-4 → new: it tracks price "more closely than the baseline does"; only the configuration is recorded (α unclamped at exponent 2, ρ = 0.5 in its own Phase 1, twig 3e-4); the span and correlation figures are withdrawn | MEASURED | `drain-orientation.md` §5-6, `changes-v5.md` §39-41 | 1865 |
| Y197 | §3.13 | Under the calibration's α = 16 the cloves demand order is `hangzhou`, `beijing`, `doab`, and the sink lands on a high-demand node rather than a … | old: under α = 16 the cloves demand order is `hangzhou`, `beijing`, `doab`, and the sink lands on a high-demand node → new: the sink lands on a high-demand node rather than a geographic accident; the demand-order triple is withdrawn | MEASURED | numerical test (figure list withdrawn) | 1873 |
| Y741 | §3.13 | The calibration's twig tolerance re-routes arcs individually carrying under 0.03% of world supply — up to about 0.18% of a good's mass in total … | old: the twig tolerance re-routes arcs individually carrying <0.03% of world supply — up to about 0.18% of a good's mass — and drops `cloves` to 99.97% reach → new: it "re-routes arcs carrying a small fraction of a good's mass, and it costs one good full reach"; all three figures withdrawn | MEASURED | numerical test (figures withdrawn) | 1874 |
| Y773 | §3.15 | `φ₀` as the installed graph is a v1 entry, moot in v2: it was not the economy the model runs, the installed graph is `Φ_w` (v2.0 briefly used … | old: "the installed graph is `Φ_w` (v2.0 briefly used `Φ_ord`)" → new: "the installed graph is `Φ_w`" — the v2.0-history parenthetical dropped | PROCESS | unsourced | 1963 |
| Y774 | §3.15 | `Φ_ord` as the installed graph is the most self-coherent aggregate measured — better than `Φ_w` on that one axis, and acyclic for free — but its ends … | old: `Φ_ord` is "the most self-coherent aggregate measured — better than `Φ_w` on that one axis, and acyclic for free — but its ends are scheduling artifacts … and its end count does not concentrate as demand concentrates" → new: "a value-weighted aggregate of the per-good marking orders … acyclic for free, but its ends are a function of Phase 3's queue discipline rather than of the world"; the superlative, the comparison and the concentration claim all gone | MODEL | derivation | 1965 |
| Y204 | §3.15 | §3.15's `Φ_ord` entry maintains no figures and its "measured coherence ceiling any future aggregate should be compared against" role is withdrawn; … | old: no figures maintained; the "measured coherence ceiling" role withdrawn; the ceiling predates §3.6's deterministic sweep and was never regenerated → new: "The rejection is structural, so no figure is kept for it" — the ceiling history deleted | DESIGN | unsourced | 1968 |
| Y777 | §3.15 | Per-good propagation is rejected: it breaks the income factoring and with it Goal 7. | old: per-good propagation is rejected because it "breaks the income factoring and with it Goal 7" → new: it does NOT break the factoring (§3.10's `ps̄_C` identity survives); it is rejected because installing the share means writing each country a fictitious per-node trade power that every other consumer then reads — and that fiction is what costs Goal 7 | MODEL | derivation (§3.10) | 1983 |

## REMOVED by this edit — the document no longer makes this claim

| ID | § | claim (census wording) | what removed it | type | provenance (was) | line |
|---|---|---|---|---|---|---|
| Y973 | §0 | 29 of the 59 figures `measure6.py` prints move with the sink set. | the 29-of-59 count is withdrawn: "A count was quoted here. It is not maintained" (L45-46) | MEASURED | measure6.py (named in the withdrawn sentence) | — |
| Y052 | §1.3 | `unrest` grants `local_tax_modifier = -0.02` per point of revolt risk and enters `tax_value`. | the `unrest` table row is deleted; the grant magnitude (`local_tax_modifier = -0.02` per point) is asserted nowhere in the document — §1.3 now says only that `unrest` is defined in the same file and not read | ENGINE | was: read from `00_static_modifiers.txt` | — |
| Y292 | §1.3 | `unrest`'s scaling is stated in the file: the `unrest` block's own comment reads `#10% longer time to build troops for each rr`, so its values apply per point, and the … | the scaling sentence (the `#10% longer time to build troops for each rr` comment, per-point application, the `nationalism` convention) is deleted; only the devastation note's passing "`unrest` and `nationalism` both carry per-unit comments" remains, which is a different census row's claim | ENGINE | was: read from `00_static_modifiers.txt` | — |
| Y982 | §1.3 | 21 counted provinces carry revolt risk in the 1444 start save. | the 1444 revolt-risk census (21 counted provinces) is withdrawn with the whole `unrest` accounting (§0 L61-63) | ENGINE | was: read from the save | — |
| Y057 | §1.3 | Sixteen of the 21 are authored in `history/provinces` at integer risk 5/8/10/15 — Sofala's comment reads "expansion of Shona into Sofala region causes major disruptions" … | the 16-authored / 5-Shirvan split and the Sofala comment are deleted with the revolt-risk accounting | ENGINE | was: `history/provinces` plus the save | — |
| Y983 | §1.3 | Even at the start date a quarter of the revolt risk is owner-derived, and during a campaign that share only grows. | the quarter-owner-derived inference is deleted with the split it was computed from | MODEL | was: derivation over the 16/5 split | — |
| Y055 | §1.3 | Excluding `unrest` costs 12.23 ducats, 0.115% of the 10,607.40 world wealth reading it from the save, or 9.40 ducats, 0.089% reading only the authored 16. | the exclusion cost (12.23 ducats / 0.115%; 9.40 / 0.089%) is withdrawn: "No figure is quoted for what the exclusion costs, and none should be reconstructed" (L373-374) | MEASURED | was: numerical test, no script named | — |
| Y056 | §1.3 | Admitting `unrest` moves 4 of 159 edges of the installed graph and leaves the sink set `{genua, hangzhou}` unchanged. | the 4-of-159-edges / sink-set-unchanged measurement is withdrawn with the exclusion cost | MEASURED | was: numerical test | — |
| Y985 | §1.3 | An earlier draft of the paragraph said admitting `unrest` moves no edge; that was measured at `α_Φ = 1.5` and does not hold at 2.0. | the earlier-draft parenthetical (no-edge figure measured at α_Φ = 1.5) is deleted with the paragraph that carried it | PROCESS | was: a claim about this document's drafting | — |
| Y331 | §1.6 | In exact arithmetic only the sign pattern and proportions of `b_w` matter: Phase 0 reads signs, Phase 1's HHI is built from mass shares, the LP optimum scales linearly … | the whole exact-arithmetic scale-invariance paragraph is deleted from §1.6 | MODEL | was: algebraic derivation | — |
| Y332 | §1.6 | The implementation adds one premise: the zero-flow tolerance is absolute (`1e-11`), so scaling `b` down pushes genuine flow arcs into the free set. | the §1.6 implementation-premise statement is deleted with the Scale paragraph; the mechanism survives only inside §3.13's closed entry (see Y737), where it is stated as a hazard not reachable from inside the model | MODEL | was: algebraic derivation | — |
| Y081 | §1.6 | Measured: identical orientation from ×1 down to ×10⁻², 22 edge flips at ×10⁻⁴ where the sink set becomes `{english_channel, hangzhou}`, and 96 at ×10⁻⁶ where it becomes … | the scaling measurements (identical ×1–×10⁻²; 22 flips at ×10⁻⁴; 96 at ×10⁻⁶) are deleted with the Scale paragraph | MEASURED | was: numerical test | — |
| Y333 | §1.6 | The orientation degrades before the sink set does, so the sink set is not the quantity to watch here. | "the orientation degrades before the sink set does" is deleted with the Scale paragraph | MODEL | was: derivation over the deleted measurements | — |
| Y334 | §1.6 | Normalising into (−1, 1) scales 1444's `b_w` up and is safe; scaling down is not, so either scale `b` up or scale the tolerance with it. | the normalise-into-(−1,1) advice ("either scale b up, or scale the tolerance with it") is deleted; §3.13 now argues no scale knob exists | MODEL | was: algebraic derivation | — |
| Y099 | §1.6 | The superseded marking-order aggregate scored higher on that measure, and §3.9 records why the trade was taken while maintaining no figure for an operator the model does … | "the superseded marking-order aggregate scored higher on that measure" is deleted here, and the same comparison is deleted from §3.9 and §3.15 — the self-coherence score is no longer asserted anywhere | MODEL | was: numerical test, figure already unmaintained | — |
| Y539 | §2.8 | v2 said "China holds a spice sink only under the calibration", which its own parenthetical contradicted. | the parenthetical "v2 said 'China holds a spice sink only under the calibration', which its own parenthetical contradicted" is deleted from the row | PROCESS | was: read from the prior spec version | — |
| Y684 | §3.9 | A rich non-sink node draws more edges in than it sends out as a net demander, even though flow passes through. | the assertion that the named rich non-sinks "draw more edges in than they send out" is deleted; the new text asserts only that a node CAN do so and still be a thoroughfare, and demotes the degree comparison as the separator (see Y1131) | MODEL | was: derivation over the measured degrees | — |
| Y179 | §3.9 | Most of `Φ_ord`'s ends terminate no good, none of the demand capitals is among them, and its end count does not concentrate as demand concentrates. | "most of `Φ_ord`'s ends terminate no good, none of the demand capitals is among them, and the end count does not concentrate as demand concentrates" is deleted from §3.9 and from §3.15 | MODEL | was: derivation, figures already unmaintained | — |
| Y183 | §3.10 | Across Sevilla, Genoa, Champagne, Malacca and the Gulf of Siam, using each node's real 1444 country table, the two forms agree to a worst relative disagreement of 0 to … | the five-node doubles check (worst relative disagreement 0 to 3.7e-16) is withdrawn: "no residual is quoted for that" (see Y1136) | MEASURED | was: numerical test over five named nodes | — |

## REMOVED — carried (already removed when the census was written; unchanged by this edit)

| ID | § | claim (label) | type | line |
|---|---|---|---|---|
| Y811 | §0 (v5) | v5.0's substantive change was applying the local-modifier classification to the whole install rather than to the trade-good tables alone. | DESIGN | — |
| Y812 | §0 (v5) | The whole-install classification adds sixteen provinces and moves the aggregate graph from two 1444 sinks to one. | MEASURED | — |
| Y813 | §0 (v5) | No figure in v5.0 is unverified, and the one place the document declines to project a number says so in place. | DESIGN | — |
| Y814 | §1.1 (v5) | On a connected core the fallback branch fires only when `b` is identically 0 across it. | MODEL | — |
| Y815 | §1.1 (v5) | `b` identically 0 happens for the aggregate graph on a uniform-wealth map. | MODEL | — |
| Y816 | §1.1 (v5) | At a fallback stall the candidates are usually all zero-wealth, so the wealth key ties and the index decides. | MODEL | — |
| Y817 | §1.1 (v5) | That index tiebreak is why §2.4 item 1 makes a canonical emitter node order a correctness requirement rather than a convention. | DESIGN | — |
| Y818 | §1.1 (v5) | On 1444 the per-good sink counts are 1-7 per good with mean 3.6. | MEASURED | — |
| Y819 | §1.1 (v5) | The §1.1 property measurements were regenerated for v5.0 by `v5measure.py`. | MEASURED | — |
| Y820 | §1.1 (v5) | On a map where Phase 0 is a no-op and no fallback fires, the last two sink cases are empty and the sink set is exactly the formula set. | MODEL | — |
| Y821 | §1.3 (v5) | Two provinces with the same terrain, development and trade good have the same wealth whoever owns them. | MODEL | — |
| Y822 | §1.3 (v5) | `trade_value(p)` carries a `(1 + sum of local trade-value modifiers)` factor. | MODEL | — |
| Y823 | §1.3 (v5) | `goods_produced(p)` carries a local flat goods bonuses term added to `GP_COEFF · base_production`. | MODEL | — |
| Y824 | §1.3 (v5) | Both wealth coefficients were measured from the running game and neither is a define, `defines.lua` having been searched, so both are … | ENGINE | — |
| Y825 | §1.3 (v5) | The tax tooltip schema is `Base: X (Yearly 12·X)`. | ENGINE | — |
| Y826 | §1.3 (v5) | The monthly production tooltip's `Trade Value` line is the province window's annual `Trade Value` over twelve, observed 3.52 to +0.29. | ENGINE | — |
| Y827 | §1.3 (v5) | Both monthly figures are the annual value over twelve, so the annual forms add directly with no conversion. | MODEL | — |
| Y828 | §1.3 (v5) | `Base 0.49` then `Tax Income Efficiency 125.0%` gives 0.6125, which the province window shows as 0.62. | ENGINE | — |
| Y829 | §1.3 (v5) | Flat goods bonuses are the exception to modifier ordering: they add into `goods_produced` before the price multiply. | ENGINE | — |
| Y830 | §1.3 (v5) | Fifteen 1444 provinces carry a flat bonus in the additive `Base Goods Produced` block, so the ordering matters in practice and not only in … | ENGINE | — |
| Y831 | §1.3 (v5) | A modifier is local if and only if its value depends only on the province's own attributes — terrain, climate, trade good, development, … | MODEL | — |
| Y832 | §1.3 (v5) | A modifier enters wealth if and only if it modifies `goods_produced`, `price` or `tax_value`. | MODEL | — |
| Y833 | §1.3 (v5) | The engine's trade-good data model is one instance of the locality test: a good's `province = { }` block is province-scoped and its … | ENGINE | — |
| Y834 | §1.3 (v5) | The two tests are applied to the whole install rather than one file; v4.0 stated the rule and then swept only `common/tradegoods/`, … | MODEL | — |
| Y835 | §1.3 (v5) | `gems` `local_tax_modifier = 0.15` on 43 provinces is local and enters `tax_value`. | ENGINE | — |
| Y836 | §1.3 (v5) | `incense` `trade_value_modifier = 0.1` on 29 provinces is local and enters `trade_value`. | ENGINE | — |
| Y837 | §1.3 (v5) | Great-project `province_modifiers` where `can_use_modifiers_trigger` is empty (6 provinces) are local and enter `goods_produced` and … | ENGINE | — |
| Y838 | §1.3 (v5) | `add_permanent_province_modifier` in the undated province-history block (10 provinces) is local and enters `goods_produced`. | ENGINE | — |
| Y839 | §1.3 (v5) | The five static condition modifiers are all zero at the 1444 start, and §1.2 and §3.3 both depend on them biting later. | ENGINE | — |
| Y840 | §1.3 (v5) | `glass` `local_production_efficiency = 0.1` is local but does not enter wealth, because it modifies production income which wealth does not … | ENGINE | — |
| Y841 | §1.3 (v5) | `chinaware` `local_autonomy = -0.1` is local but does not enter wealth, because it modifies local autonomy which wealth does not compute. | ENGINE | — |
| Y842 | §1.3 (v5) | 361 provinces carry a centre of trade at 1444, and no CoT level in `common/centers_of_trade/` grants any of the four keys wealth reads — a … | ENGINE | — |
| Y843 | §1.3 (v5) | `production_leader` `trade_goods_size_modifier = 0.10` is not local, because which country leads a good's production is a country's state. | ENGINE | — |
| Y844 | §1.3 (v5) | Goods-produced efficiency from nearby merchant republics, trading cities and trade companies (`bonus_from_merchant_republics`, … | ENGINE | — |
| Y845 | §1.3 (v5) | Buildings are local by the test and empty at 1444, because no province's start state carries a temple, workshop or manufactory. | ENGINE | — |
| Y846 | §1.3 (v5) | `terrain.txt` and the climate static modifiers are local but grant only keys wealth does not compute — `allowed_num_of_buildings`, … | ENGINE | — |
| Y847 | §1.3 (v5) | A great project contributes the `province_modifiers` accumulated up to its `starting_tier` when its `can_use_modifiers_trigger` is empty, … | ENGINE | — |
| Y848 | §1.3 (v5) | 85 of the 130 great projects live at 1444 are gated on a country's culture, religion, government or flags. | ENGINE | — |
| Y849 | §1.3 (v5) | Six great projects carry a key wealth reads: `falun_copper_mine` (province 8, `trade_goods_size` 3.0), `krakow_cloth_hall` (262, … | ENGINE | — |
| Y850 | §1.3 (v5) | Province 1821 is the richest single province in the game. | MEASURED | — |
| Y851 | §1.3 (v5) | The starting tier is the right line and "owner action" is not, because development is an owner action so a rule excluding those would … | DESIGN | — |
| Y852 | §1.3 (v5) | The ten permanent modifiers are `granary_of_the_mediterranean` (362, 363, 2316, 4316), `skanemarket` (6), `icelanding_fisher_sea` (370, … | ENGINE | — |
| Y853 | §1.3 (v5) | `province_triggered_modifiers`' `stora_kopparberget_modifier` is gated `NOT = { has_dlc = "Leviathan" }` and grants `trade_goods_size = … | ENGINE | — |
| Y854 | §1.3 (v5) | Every wealth figure in v5.0 was measured with Leviathan installed. | MODEL | — |
| Y855 | §1.3 (v5) | Glass and chinaware — local but not entering — are the whole of the rule-versus-vocabulary tension, since §1.3 excludes production … | MODEL | — |
| Y856 | §1.3 (v5) | Every province the model counts is a city (`is_city = yes`). | ENGINE | — |
| Y857 | §1.3 (v5) | `s` and `c` are computed over provinces with an owner and `is_city = yes`. | DESIGN | — |
| Y858 | §1.3 (v5) | Owner-agnostic wealth removes the single largest source of hidden owner-dependence from the aggregate graph. | MODEL | — |
| Y859 | §1.5 (v5) | Repricing the 45 owned latent-coal provinces flips 29 of 159 `Φ_w` edges. | MEASURED | — |
| Y860 | §1.5 (v5) | Coal's base price of 10.0 is the highest in vanilla. | ENGINE | — |
| Y861 | §1.6 (v5) | `Φ_w`'s sink count is set by `α_Φ` and only the sink locations are emergent. | MODEL | — |
| Y862 | §1.6 (v5) | Downscaling `b_w` gives 16 edge flips at ×10⁻² and 83 at ×10⁻⁶. | MEASURED | — |
| Y863 | §1.6 (v5) | 1444's `b_w` has largest magnitude 0.0227. | MEASURED | — |
| Y864 | §1.6 (v5) | Measured at `α_Φ = 1.5` there is one sink, `hangzhou`, rank 1 in the `α_Φ`-weighted wealth field `c_w` and rank 10 in raw node wealth, … | MEASURED | — |
| Y865 | §1.6 (v5) | v2 through v4's two-sink result was measured on a wealth field missing the sixteen provinces v5's §1.3 carries, and correcting the field … | MEASURED | — |
| Y866 | §1.6 (v5) | v2 also wrote "wealth ranks" without saying which, and the plain reading was wrong then too. | PROCESS | — |
| Y867 | §1.6 (v5) | Phase 1 selects `hangzhou` directly, so there are 0 promotions and 0 fallbacks and the self-correction never fires on this input. | MEASURED | — |
| Y868 | §1.6 (v5) | Seven sources — `kongo`, `patagonia`, `james_bay`, `mississippi_river`, `chengdu`, `australia`, `tunis` — at `c_w` ranks 52-79 with mean … | MEASURED | — |
| Y869 | §1.6 (v5) | 0 edge flips and 0 sink-set changes under ±1% wealth noise across 5 seeds. | MEASURED | — |
| Y870 | §1.6 (v5) | Agreement with the per-good graphs is 52.5% of edge-goods (51.5% value-weighted) against the superseded `Φ_ord`'s 60.3% — a gap of 7.8 … | MEASURED | — |
| Y871 | §1.6 (v5) | v2's 62.7% was measured under the old scan-order sweep and was never regenerated after §3.6 adopted the deterministic one. | PROCESS | — |
| Y872 | §1.6 (v5) | The `α_Φ` sink-count band table: 1 sink `hangzhou` at [1.43, 1.93] width 0.50 (the widest band on this field); 3 sinks {doab, genua, … | MEASURED | — |
| Y873 | §1.6 (v5) | v4.0's two-sink result is not a band: refined to 0.001 it spans [1.406, 1.424], 0.018 wide against the one-sink band's 0.506. | MEASURED | — |
| Y874 | §1.6 (v5) | Under ±1% wealth noise across 8 seeds the narrow window's edges move by up to 0.02 while its width ranges 0.00 to 0.03, so the window is … | MEASURED | — |
| Y875 | §1.6 (v5) | The three wide bands over those same seeds keep widths of 0.28-0.51 with edges moving no more than 0.03. | MEASURED | — |
| Y876 | §1.6 (v5) | A constant cannot honestly be placed inside a window narrower than the uncertainty in its own edges. | DESIGN | — |
| Y877 | §1.6 (v5) | An earlier draft said the narrow window "moves or disappears entirely" under noise; at 8 seeds it disappears on none of them and only … | PROCESS | — |
| Y878 | §1.6 (v5) | `α_Φ` is retained at 1.5 because it sits inside the widest sink-count band and nothing now selects a different value. | DESIGN | — |
| Y879 | §1.6 (v5) | Sampled at the six values v2 used the sink count is 5, 1, 2, 4, 3, 1. | MEASURED | — |
| Y880 | §1.6 (v5) | A 1-2% European development edge produces a European sink: at ×1.02 across Europe's 823 counted provinces the sinks are {doab, … | MEASURED | — |
| Y881 | §1.6 (v5) | `english_channel` is a sink at every larger European growth factor tested. | MODEL | — |
| Y882 | §1.6 (v5) | What the model claims is the threshold rather than the size of the historical edge: 2% is enough, and the project measures nothing about … | DESIGN | — |
| Y883 | §1.6 (v5) | All three institutions the period is named for begin in Europe inside the 1450-1550 window. | ENGINE | — |
| Y884 | §1.6 (v5) | The Renaissance's embracement bonus is a standing 5% discount on every subsequent development point. | ENGINE | — |
| Y885 | §1.6 (v5) | The Lowlands alone suffice: developing only the nine Lowland provinces in `english_channel` (Holland, Zeeland, Vlaanderen, Brabant, … | MEASURED | — |
| Y886 | §1.6 (v5) | ±2% random wealth noise leaves the 1444 sink set unchanged on three seeds, while +2% applied systematically to Europe alone changes it, so … | MEASURED | — |
| Y887 | §1.6 (v5) | The 1444 Silk Road route runs through `doab`: genua, alexandria, aleppo, persia, lahore, doab, ganges_delta, burma, gulf_of_siam, canton, … | MEASURED | — |
| Y888 | §1.6 (v5) | From the Channel the route is the Hansa and the Danube: english_channel, lubeck, saxony, wien, venice, ragusa, constantinople, aleppo, and … | MODEL | — |
| Y889 | §1.6 (v5) | Nothing routes through the Cape, which is what a 1444 map should say. | MEASURED | — |
| Y890 | §1.6 (v5) | The Cape's per-good spice route is malacca, cape_of_good_hope, zanzibar, gulf_of_aden, alexandria, genua. | MODEL | — |
| Y891 | §1.6 (v5) | Scaling the 22 European nodes' wealth ×2 makes `genua` the sole sink, and under the 18-node set alone sole-`genua` needs ×2.5. | MEASURED | — |
| Y892 | §1.6 (v5) | Between ×3 and ×3.75 the Cape of Good Hope reverses and outside that window it does not, so the reversal is a band and not a threshold. | MEASURED | — |
| Y893 | §1.6 (v5) | Dev-stacking `hangzhou`'s top province keeps it the sole sink at ×20, ×30 and ×50, with a transient split into three at ×10. | MEASURED | — |
| Y894 | §1.10 (v5) | Almost nothing absorbs threshold chatter. | ENGINE | — |
| Y895 | §1.10 (v5) | The caravan cap of 50 is 8.6% to 32.0% of an inland node's total trade power, median 17.9% over the flag's 26 inland nodes, and on §2.2's … | MEASURED | — |
| Y433 | §2.1 (v5) | Supporting multiplayer requires the computation to be bit-reproducible across machines. | DESIGN | — |
| Y896 | §2.2 (v5) | Solver item 4's wealth formula includes local flat goods bonuses inside the goods term and a `(1 + local trade-value modifiers)` factor on … | DESIGN | — |
| Y897 | §2.2 (v5) | The solver reads local modifiers from §1.3's whole-install classification: `gems` (+15% tax, 43 provinces), `incense` (+10% trade value, 29 … | MEASURED | — |
| Y898 | §2.2 (v5) | World wealth is 10,677.50 annual ducats over 2,452 counted provinces. | MEASURED | — |
| Y899 | §2.2 (v5) | Solve cost is 0.17-0.21 s for all 29 goods, a mean of 5.7-7.3 ms per good across runs, with individual goods ranging 5.4-24 ms so 7.3 is an … | MEASURED | — |
| Y900 | §2.2a (v5) | Where Phase 0 acts, free-edge determinism is the same in both halves, because peeling does not touch the priority key. | MODEL | — |
| Y901 | §2.3 (v5) | The two wealth coefficients of §1.3 are hardcoded in the binary, `defines.lua` and `common/defines/` having been searched and containing … | ENGINE | — |
| Y902 | §2.3 (v5) | `α_Φ`'s stated calibration is withdrawn because on the corrected wealth field 1.5 does not yield the two-sink map, and the window that does … | MEASURED | — |
| Y903 | §2.3 (v5) | 1.5 is retained because it sits inside the widest sink-count band and nothing now selects a different value. | DESIGN | — |
| Y904 | §2.4 (v5) | The node order is a correctness requirement because §1.1's priority key breaks exact ties by node index and on the fallback branch the … | MODEL | — |
| Y905 | §2.4 (v5) | Without one canonical node order kept stable across rebuilds, the same world can produce two different maps. | MODEL | — |
| Y906 | §2.4 (v5) | 1444 has one end node, `hangzhou`, against vanilla's three. | MEASURED | — |
| Y907 | §2.7 (v5) | §1.9's "every immediately upstream node" is correct as written and gains no qualifier. | ENGINE | — |
| Y908 | §2.8 (v5) | Sinks are 1 to 7 per good, and high-demand nodes are sinks at 14.5% in the top demand decile against 6.9% in the bottom. | MEASURED | — |
| Y909 | §2.8 (v5) | Zeroing `hangzhou`-node development moves the `Φ_w` sinks from {hangzhou} to {doab, english_channel, gulf_of_siam, sevilla}. | MODEL | — |
| Y910 | §2.8 (v5) | `hangzhou`'s `c_w` rank is 1 against `beijing`'s 31, node wealth 245.0 against 143.8, and it holds the richest single province in the game. | MEASURED | — |
| Y911 | §2.8 (v5) | Zeroing `beijing` gives 17 flips with sinks {doab, english_channel, hangzhou, sevilla}, because it deletes 1.3% of world wealth. | MEASURED | — |
| Y912 | §2.8 (v5) | The rank gap is what carries the razed-China row, not a null result. | MODEL | — |
| Y913 | §2.8 (v5) | `Φ_w` agrees with the per-good graphs on 51.5% of edge-goods weighted by trade value and 52.5% unweighted. | MEASURED | — |
| Y914 | §3.2 (v5) | With no regularizer the spices supply ratio over producing nodes is 36 against a demand ratio of 482.2, which points the other way. | MEASURED | — |
| Y915 | §3.2 (v5) | Better wealth inputs plausibly deliver about 1.7×, measured as `genua` becoming a co-sink at ×1.720. | MEASURED | — |
| Y916 | §3.2 (v5) | A spice sink at any of the four Chinese trade nodes needs 3.6-4.9×, i.e. 9.3-21.4% of all world spice demand at one node: `beijing` 3.60× / … | MEASURED | — |
| Y917 | §3.2 (v5) | The four China-region nodes outside that set — `girin`, `yumen`, `chengdu`, `lhasa` — need 4.0× to 10.8×. | MEASURED | — |
| Y918 | §3.2 (v5) | v2's "1.7× where 4-5× is needed" compressed two different thresholds into one comparison. | MODEL | — |
| Y919 | §3.2 (v5) | The one place the node indexing is load-bearing is the fallback branch, where the candidates are typically all zero-wealth and tied, and … | MODEL | — |
| Y920 | §3.3 (v5) | `cape_of_good_hope` has 19 land provinces, stated without the `sea_starts` explanation. | ENGINE | — |
| Y921 | §3.4 (v5) | In v1 substituting production income collapsed orientation agreement from 159/159 to 68/159. | MEASURED | — |
| Y922 | §3.5 (v5) | All 161 `change_price` blocks were parsed. | ENGINE | — |
| Y923 | §3.5 (v5) | v4.0 said 154 and 7 because its parser silently recovered nothing from five mission files, which a bare `except` hid, so the scan is now … | MODEL | — |
| Y924 | §3.5 (v5) | 1.875 is the figure a campaign reaching 1540 holds. | ENGINE | — |
| Y925 | §3.8 (v5) | 92.2% (5825 of 6320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. | MEASURED | — |
| Y926 | §3.9 (v5) | `genua`, `gulf_of_siam` and `sevilla` rank 3rd, 2nd and 7th by node wealth on the corrected field at 296.0, 299.2 and 266.5 against … | MEASURED | — |
| Y927 | §3.9 (v5) | `Φ_ord` remains the most self-coherent aggregate measured, at 60.3% edge-good agreement with the per-good graphs against `Φ_w`'s 52.5% … | MEASURED | — |
| Y928 | §3.9 (v5) | Of `Φ_ord`'s 13 end nodes at 1444, 8 terminate no good at all and none of the demand capitals is among them. | MEASURED | — |
| Y929 | §3.9 (v5) | `Φ_ord`'s end count never concentrates: 11-17 ends measured across cloves-α 2 to 64, never approaching vanilla's three. | MEASURED | — |
| Y930 | §3.9 (v5) | v2 called that "α-invariant … 9-17 ends", which is neither the right word for a quantity ranging 11-17 nor a band containing its own … | PROCESS | — |
| Y931 | §3.9 (v5) | Self-coherence was traded for legible, wealth-anchored, world-responsive ends. | DESIGN | — |
| Y932 | §3.9 (v5) | On the corrected wealth field there is one end, in China, matching none of vanilla's three, so the two-vanilla-like-ends premise is … | MODEL | — |
| Y933 | §3.9 (v5) | The trade is 7.8 points of self-coherence given up for one operator and world-responsive ends, and the 1444 count is whatever the field … | MEASURED | — |
| Y934 | §3.10 (v5) | The two income forms agree to at most one unit in the last place. | MODEL | — |
| Y935 | §3.10 (v5) | Propagation cannot be made per good. | MODEL | — |
| Y936 | §3.10 (v5) | Per-good propagation destroys the income identity, because §1.9 reads a node's downstream neighbours and those differ per good. | MODEL | — |
| Y937 | §3.10 (v5) | The driver is not how many distinct downstream sets a node has but whether its collectors hold differing power across the nodes those sets … | MODEL | — |
| Y938 | §3.10 (v5) | `gulf_of_siam` has eight distinct downstream sets and still shows a 0.003% effect, because its collectors hold almost nothing in `burma`, … | MEASURED | — |
| Y939 | §3.10 (v5) | Per-good propagation's error is redistributive and single-digit percent with the sign varying by collector: Sevilla -0.82%, -0.87%, +7.44%; … | MEASURED | — |
| Y940 | §3.10 (v5) | That error is thirteen orders of magnitude above the float residual and it moves income between countries. | MODEL | — |
| Y941 | §3.10 (v5) | Keeping propagation on a single graph is load-bearing for Goal 7 rather than merely convenient. | DESIGN | — |
| Y942 | §3.10 (v5) | The largest local trade value of any node in the model is 112.6. | MEASURED | — |
| Y943 | §3.10 (v5) | v4.0's 0.41% replacement figure was an artifact of freezing one term at the alphabetically first commodity. | MODEL | — |
| Y944 | §3.13 (v5) | The open wealth question is what else multiplies `goods_produced` and which side of the owner line each source falls on. | DESIGN | — |
| Y945 | §3.13 (v5) | §1.3's classification handles the sources observed so far: the owner's `global_trade_goods_size_modifier` (out, country-scoped) and … | ENGINE | — |
| Y946 | §3.13 (v5) | Fifteen 1444 provinces carry a flat `trade_goods_size`, five from great projects and ten from permanent province modifiers. | ENGINE | — |
| Y947 | §3.13 (v5) | `trade_goods_size` and `trade_goods_size_modifier` appear in buildings, estate privileges, government reforms, church aspects, fervor, ages … | ENGINE | — |
| Y948 | §3.13 (v5) | The settling work is to enumerate every source of both keys and classify each, and the model needs the answer only for sources that can be … | DESIGN | — |
| Y949 | §3.13 (v5) | Deccan, demand rank 2 under α = 16 with the rank-1 demander `hangzhou` acting as a transit node, becomes the cloves sink. | MEASURED | — |
| Y950 | §3.13 (v5) | `hangzhou`'s richest province is 30.4 against Beijing's 19.5, and under the calibration Beijing is only demand rank 3. | MEASURED | — |
| Y951 | §3.15 (v5) | With v1's ε floor removed the contrasts run 4-97 on supply against 211-20,400 on demand across the 29 goods. | MEASURED | — |
| Y952 | §3.15 (v5) | Ranked orientation's alignment statistics: rho_val +0.281 against DRAIN's +0.054, and 43.8% of top-decile nodes are sinks against 14.5%. | MEASURED | — |
| Y953 | §3.15 (v5) | Ranked orientation reaches 83.0% of demand with 31 orphan sinks. | MEASURED | — |
| Y954 | §3.15 (v5) | Ranked orientation posts 8 net-producer sinks where DRAIN, LAP and FLOW all post zero. | MEASURED | — |
| Y955 | §3.15 (v5) | Ranked orientation keeps 10-16 sinks per good against DRAIN's 1-7. | MEASURED | — |
| Y956 | §3.15 (v5) | Seeded basin growth reaches 88.4% at its best tuning. | MEASURED | — |
| Y957 | §3.15 (v5) | `Φ_ord` is retained as the measured coherence ceiling any future aggregate should be compared against, and that ceiling is 60.3% rather … | MEASURED | — |
| Y958 | §3.15 (v5) | No parameter steers `Φ_ord`'s end count. | MODEL | — |
| Y959 | §3.15 (v5) | The 3-mass gravity field hits any chosen end count exactly for γ no greater than 0.7 and any count up to six, and at γ = 0.9 the four-, … | MEASURED | — |
| Y960 | §3.15 (v5) | The gravity field's best vanilla-arrow agreement is 61% (97 of 159 arrows) at γ = 0.90-0.95, with γ = 0.97 giving 93 and every larger γ … | MEASURED | — |
| Y961 | §3.15 (v5) | v2.1 through v4.0 put the gravity field's best agreement at γ = 0.97 and said the five- and six-mass fields give four ends at γ = 0.9; on … | MEASURED | — |
| Y962 | §3.15 (v5) | v2.0 and v2.1 both quoted 69% = 110 of 159 for the gravity field, which is not reached at any γ, and the count-follows-seeds behaviour … | MEASURED | — |
| Y963 | §3.15 (v5) | A local wealth maximum survives every positive α, measured as at least 10 ends at α up to 16. | MEASURED | — |
| Y964 | §3.16 (v5) | Implemented as written, v1's ε left the α = 1 identity failing at 1e-5. | MEASURED | — |

## NEW — propositions the census does not cover (`Y1058`–`Y1141`, document order)

| ID | § | claim | type | provenance | line |
|---|---|---|---|---|---|
| Y1058 | §0 | What moves with the sink set is every figure derived from the aggregate graph — the sink set and its ranks, the source set, the sensitivity bands, and the European scaling. | MODEL | unsourced | 41 |
| Y1059 | §0 | What holds is everything computed before the aggregate solve: the wealth field, the per-province and per-node totals, the price census, and the per-good graphs. | MODEL | unsourced | 43 |
| Y1060 | §0 | The per-good graphs' `α(g)` does not read `α_Φ`. | MODEL | unsourced | 44 |
| Y1061 | §0 | A count was quoted here and is not maintained: `measure6.py`'s figure list grows whenever a figure gains a guard, so the count moved for reasons that had nothing to do with `α_Φ`. | PROCESS | `measure6.py` | 45 |
| Y1062 | §0 | v6.2 narrows the wealth rule and changes no number on the 1444 field. | MODEL | unsourced | 49 |
| Y1063 | §0 | `unrest` is dropped from §1.3's table rather than carried as an excluded row. | PROCESS | unsourced | 50 |
| Y1064 | §0 | Both changes follow the same reading: a trade node is owner-agnostic, so wealth measures what a province can buy, and neither a revolt nor an occupier changes that. | DESIGN | unsourced | 51 |
| Y1065 | §0 | An occupying army is a fact about a war. | DESIGN | unsourced | 54 |
| Y1066 | §0 | What a revolt and an occupation cost the owner is real and is the owner's problem, which is exactly what §1.3 declines to model. | DESIGN | unsourced | 54 |
| Y1067 | §0 | The 1444 figures are unchanged because neither input was ever live on that field: `unrest` was already not read, and no province is occupied at a start date with no wars. | MODEL | unsourced | 59 |
| Y1068 | §0 | What moves is what happens during a campaign, which is where the rule now differs from v6.1. | MODEL | unsourced | 60 |
| Y1069 | §0 | Every figure the retired `unrest` accounting carried is withdrawn rather than repaired, and with it the `revolt_risk` parse — an input surface maintained for a quantity nothing reads. | PROCESS | unsourced | 61 |
| Y1070 | §0 | `fixes-agreed.md` carries a row for all 62 graded claims. | PROCESS | `fixes-agreed.md` | 78 |
| Y1071 | §0 | `fixes-agreed.md` is frozen at v6.0: it records what v6.0 changed relative to v5.0 and is not maintained against later versions. | PROCESS | `fixes-agreed.md` | 78 |
| Y1072 | §0 | Where a figure in `fixes-agreed.md` has since moved, this document is the live one. | PROCESS | unsourced | 79 |
| Y1073 | §0 | Neither harness targets `fixes-agreed.md` by default. | PROCESS | unsourced | 80 |
| Y1074 | §0 | A figure with no script named at its line, and none named for its block, has not been reproduced by anything in `scripts/` since it was written. | PROCESS | unsourced | 94 |
| Y1075 | §1.1 | The cluster dilation radius `r` links demanders within `r` hops before clustering. | MODEL | unsourced | 122 |
| Y1076 | §1.1 | A demand-mass quantile `ρ` was documented here as a second Phase-1 knob; the shipped operator has no such parameter — `drain.py`'s Phase 1 clusters every demander — so it is not listed. | PROCESS | `drain.py` (restated §2.3 L1078-1080) | 125 |
| Y1077 | §1.1 | The §3.13 calibration option carries its own Phase 1 and does implement a quantile; that is where `ρ` is described. | MODEL | unsourced (restated §2.3 L1079-1080, §3.13 L1866-1867) | 127 |
| Y1078 | §1.1 | Phase 4 emits the orientations Phase 0 determined for the pendants: Phase 0 decides those directions, Phase 4 is where they enter the graph. | MODEL | unsourced | 171 |
| Y1079 | §1.1 | A pendant sink is visible only after Phase 4 (T1, §3.2). | MODEL | derivation | 172 |
| Y1080 | §1.1 | Attribution of the determinism bullet's figures: `measure6.py` for the core-node count; `props6.py` for the permutations, the argmin and cut ties, and the reachability and orphan-sink figures. | PROCESS | `measure6.py`, `props6.py` | 214 |
| Y1081 | §1.1 | `props6.py` was renamed from a round-5 working file and the permutation loop was written for this citation — the figure had been quoted since v2 with nothing in the tree that computed it. | PROCESS | `props6.py` | 216 |
| Y1082 | §1.1 | The six identical solves are six solves inside a single process, blind to anything that varies between processes; `fingerprint6.py` covers that second question separately (§2.1). | MODEL | `fingerprint6.py` (restated §2.8 L1367) | 235 |
| Y1083 | §1.3 | The deleted-apparatus figures are reproduced by `apparatus6.py`, which holds the deleted classifier's constants frozen. | PROCESS | `apparatus6.py` | 278 |
| Y1084 | §1.3 | The frozen constants record what v5.0's input surface was worth, not a live table, and sit in their own file precisely so that nothing can wire them back into the wealth path. | DESIGN | unsourced | 279 |
| Y1085 | §1.3 | `measure6.py` imports the apparatus figures rather than restating them. | PROCESS | `measure6.py` | 281 |
| Y1086 | §1.3 | `occupied`'s `local_tax_modifier` is granted by the file and not read: an occupier's presence is a fact about who is standing on the province — the class of input §1.3 exists to exclude — and the production half already carries the effect that matters, since occupied land ships less. | DESIGN | derivation | 349 |
| Y1087 | §1.3 | `STATE_TAX_MOD` is kept as an empty declaration rather than deleted, so the shape of the exclusion stays legible in the code instead of becoming an absence a later editor has to infer. | DESIGN | `solver.py` | 352 |
| Y1088 | §1.3 | On the 1444 start `prosperity`, `under_siege` and `occupied` are live on no counted province — all three describe conditions a campaign produces and a start date without wars does not. | MEASURED | `round6.py` | 356 |
| Y1089 | §1.3 | The wealth rule carries four modifiers, of which one is exercised by the reference field. | MODEL | unsourced | 358 |
| Y1090 | §1.3 | A province in revolt still has the buying power its development gives it; whether its owner manages to collect against that buying power is a fact about the owner, and a trade node is not a fact about the owner. | DESIGN | unsourced | 366 |
| Y1091 | §1.3 | No figure is quoted for what the `unrest` exclusion costs, and none should be reconstructed. | DESIGN | unsourced | 373 |
| Y1092 | §1.3 | Earlier drafts carried such a figure, and keeping it accurate meant parsing `revolt_risk` out of the save — an input surface maintained for a quantity the model does not read, which is the maintenance §1.3 deleted the modifier classifier to be rid of. | PROCESS | unsourced | 374 |
| Y1093 | §1.3 | The exclusion is a decision about what wealth means, and a measured cost would not bear on it. | DESIGN | unsourced | 377 |
| Y1094 | §1.6 | The agreement figure is a description of how often one power map coincides with twenty-nine commodity maps, not a quality score: `Φ_w` models power and the per-good graphs model cargo (§3.9), so full agreement is neither expected nor wanted. | DESIGN | derivation (§3.9) | 588 |
| Y1095 | §1.6 | The European sweep samples uniformly on a 0.001 grid from ×1.000 to ×2.600. | MEASURED | `europe.py` | 622 |
| Y1096 | §1.6 | The widest interval carrying three European ends and none in Asia runs ×1.973 to ×2.456, with `english_channel`, `genua` and `rheinland` holding them. | MEASURED | `europe.py` (block citation) | 625 |
| Y1097 | §1.6 | A table of interval boundaries was published here and is withdrawn: its rows came from bisection and disagree with a uniform grid about where several boundaries lie. | PROCESS | unsourced | 632 |
| Y1098 | §1.6 | The effect of a boundary that sits between samples is a row that looks like a fact and is an artifact of the sampling. | MODEL | derivation | 633 |
| Y1099 | §1.6 | The direction and the widest interval survive the bisection-versus-grid difference; the row boundaries did not, and quoting them invited exactly the trajectory reading the paragraph warns against. | PROCESS | unsourced | 634 |
| Y1100 | §1.6 | Swept from ×2.50 to ×25.00 on the all-22 scaling, none of the eastern four holds an end at any multiple, and both surviving ends are western throughout. | MEASURED | `round6.py` | 684 |
| Y1101 | §1.6 | The earlier draft's clause attributing the no-sole-sink behaviour to "the eastern four pulling ends of their own" was invented and is deleted rather than repaired. | PROCESS | unsourced | 686 |
| Y1102 | §1.6 | This section's figures are measured under the shipped sweep key (DEF ascending, β ascending, index), which is a design choice inside Phase 3 rather than a property of the world, so a different key moves some of them. | MODEL | unsourced | 699 |
| Y1103 | §1.6 | Measured against DEF-descending on the same field: of the 19 aggregate-graph facts `round6.py` checks, 6 move and 13 do not. | MEASURED | `round6.py` | 701 |
| Y1104 | §1.6 | The thirteen that hold: the sink set and its count, the promotion count, the fallback count, acyclicity, the number of oriented edges, `genua`'s in- and out-degree, the Cape's in- and out-degree, the northern route's reach to `hangzhou`, and the two-hop `english_channel → champagne → genua` route and its via-`champagne` form. | MEASURED | `round6.py` | 702 |
| Y1105 | §1.6 | The six that move: the source count (5 against 10), the sources' `c_w` rank range, their mean degree, the Cape's ordered-pair count (81 against 42), and the two reaches that together are the Iberian long route. | MEASURED | `round6.py` | 705 |
| Y1106 | §1.6 | Under the descending key `sevilla` reaches neither `ganges_delta` nor the Asian end, so the Iberian route ceases to exist. | MEASURED | `round6.py` | 707 |
| Y1107 | §1.6 | The northern route's endpoints stay connected under both keys — the check is that `white_sea` still reaches `hangzhou`, not that it does so by the same hops — and the intermediate routing is exactly the kind of fact a key change moves. | MEASURED | `round6.py` | 708 |
| Y1108 | §1.6 | The two long routes are properties of this field and this key; the sink set is a property of the field alone. | MODEL | derivation over the key sweep | 711 |
| Y1109 | §1.10 | Measured across `common/`, `missions/`, `decisions/` and `events/` with comments stripped, the four structural construct families account for several hundred uses. | MEASURED | `round6.py` | 842 |
| Y1110 | §1.10 | None of the 80 node names appears anywhere in the four trees. | MEASURED | `round6.py` | 844 |
| Y1111 | §1.10 | The token scan matches `trade_node` as a bare word and by construction cannot see every compound key containing it; such keys exist (`add_trade_node_income`, `agenda_trade_node`, `trade_node_value` and others). | ENGINE | named observation (the token scan; the shipped script vocabulary) | 845 |
| Y1112 | §1.10 | "Bounded by class" is the honest claim only for the families named; the full key inventory is an emitter-time enumeration, not a figure this document maintains. | DESIGN | unsourced | 847 |
| Y1113 | §2.1 | The determinism fingerprint is one SHA-256 over `Φ_w` and all 29 per-good graphs, including sinks, sources, promotions, fallbacks and the Phase-2 objective. | MODEL | `fingerprint6.py` | 916 |
| Y1114 | §2.1 | The smallest non-zero per-good `\|net\|` magnitude is 6.94e-06. | MEASURED | `round6.py` | 920 |
| Y1115 | §2.3 | `\|w[u] − w[v]\|` telescopes: summed along a path it collapses to a function of the endpoints, so two routings between the same endpoints can still total the same and the term cancels exactly where a tie needs breaking; `frac(lo·hi·7919)` has no such structure, and that is the whole of its job. | MODEL | derivation | 1117 |
| Y1116 | §2.3 | `w/mean` and `N·w/sum` are algebraically the same vector, and on this field min-max and `w/max` are too, so a sweep over five normalisations is a sweep over three. | MODEL | derivation | 1165 |
| Y1117 | §2.3 | `cape_of_good_hope` holds no counted province at all: its 20 members are one sea zone and nineteen land provinces, none of them owned at 1444, and §1.3 counts only owned provinces. | ENGINE | named observation (the map files and the 1444 save, via §1.3's counting rule) | 1167 |
| Y1118 | §2.3 | A re-measuring probe must inherit `flowop.LP_OPTS`: without the pinned tolerance the same sweep undercounts — under `w/mean` it returns 5 goods against the pinned 9, and the 5 are a strict subset of the 9. | MEASURED | `round6.py` | 1169 |
| Y1119 | §2.8 | The calibration figures moved when §2.3's tie-break cost reached the calibration's own Phase 2 — it was the last solve in the tree still passing unit costs, and it had been reading a different vertex from the shipped operator on every good. | PROCESS | unsourced | 1347 |
| Y1120 | §2.8 | `paper` is today in the genuine-tie state: a zero reduced cost on an arc that carries no flow in any optimum — the report branch of the three-branch check. | MEASURED | `round6.py` | 1368 |
| Y1121 | §2.9 | Each per-tick assertion is paired with a negative fixture that makes it fail, because an assertion nobody has watched go red is an assertion nobody has tested. | DESIGN | unsourced | 1392 |
| Y1122 | §2.9 | Four of the defects the round-5 audit found were checks that could not fail. | PROCESS | unsourced | 1394 |
| Y1123 | §2.9 | `scripts/redtest6.py` is the reference-side version of the negative-fixture requirement. | PROCESS | `redtest6.py` | 1394 |
| Y1124 | §3.2 | Degree is the weaker evidence for conduit function and was the only kind offered before: an oriented edge is not a routed unit. | MODEL | derivation | 1517 |
| Y1125 | §3.2 | On the certificate flow itself the Cape has both incoming and outgoing flow on 28 of 29 goods; the exception is `paper`, which routes none through it in either direction. | MEASURED | `round6.py` | 1519 |
| Y1126 | §3.6 | The uniqueness margin is not a constant of the design, and how much of it is a gift of the chosen `α_Φ` is worth knowing. | DESIGN | unsourced | 1645 |
| Y1127 | §3.6 | On the aggregate the margin is 7.53e-06 at `α_Φ` = 2.0 and 1.267e-07 at 1.5 — a factor of sixty for a change §1.6 treats as taste. | MEASURED | `round6.py` | 1646 |
| Y1128 | §3.6 | Per good, two of the 29 solves sit inside HiGHS's 1e-7 default — `copper` at 3.765e-08 and `paper` at 8.92e-08 — and 27 sit above it. | MEASURED | `round6.py` (restated §2.8 L1368) | 1648 |
| Y1129 | §3.6 | `round6.py` reports the margin as the smallest positive reduced cost on an arc outside the support. | MODEL | `round6.py` | 1649 |
| Y1130 | §3.6 | Pinning the tolerance is load-bearing at these values rather than precautionary; a future change to `α_Φ` or to the wealth field should re-measure the margin rather than assume the headroom survives. | DESIGN | unsourced | 1650 |
| Y1131 | §3.9 | A node can draw more edges in than it sends out and still be a thoroughfare; the quantity that separates a net demander from an end is not a degree comparison. | MODEL | derivation | 1705 |
| Y1132 | §3.9 | The separating quantity is the flow identity the LP enforces: `flow_in(n) − flow_out(n) = −b_w(n)`. | MODEL | derivation | 1707 |
| Y1133 | §3.9 | The identity holds on all 36 net demanders and on all 80 nodes, to a maximum residual of 5.2e-17. | MEASURED | `round6.py` | 1708 |
| Y1134 | §3.9 | Every net demander absorbs exactly its own deficit and passes the rest on; an end is a node that passes none on. | MODEL | derivation | 1709 |
| Y1135 | §3.9 | 18 of 80 nodes have out-degree above zero while carrying no outgoing flow at all. | MEASURED | `round6.py` | 1710 |
| Y1136 | §3.10 | No residual is quoted for the doubles check: a floating-point residual of an exact identity measures the arithmetic, not the design, and every version that quoted one quoted a different number from a different construction. | DESIGN | unsourced | 1756 |
| Y1137 | §3.13 | `b_w` is built with `s_w(n) = 1/N` uniform against a `c_w` that sums to 1, so its largest magnitude cannot fall below `1/N` without changing what the model computes; there is no scale knob to turn. | MODEL | derivation | 1847 |
| Y1138 | §3.13 | The 1e-11 threshold is `flowop.ZERO_TOL`, a post-solve classification constant the implementation may set to anything; no solver floor constrains it. | MODEL | `flowop.py` | 1850 |
| Y1139 | §3.13 | The solver's feasibility tolerances (`flowop.LP_OPTS`) bottom out at HiGHS's 1e-10: below that the option is rejected with `Invalid option value` while `success` stays true, and the solver silently reverts to the 1e-7 default — worse than not setting it because it looks like it worked. | MODEL | named observation (HiGHS option behaviour) | 1853 |
| Y1140 | §3.13 | The revert is measured rather than inferred: on `copper`, an unset tolerance and 1e-7 each move 8 edge-slots over four column permutations, 1e-8 and 1e-10 each move none, and a rejected 1e-11 moves 8 — it behaves like the default, not like the last valid setting. | MEASURED | `round6.py` | 1857 |
| Y1141 | §3.13 | No span, correlation or reach figure is quoted for the calibration option: it is not adopted, its numbers move with every change to the wealth field and to §2.3's cost, and the decision about it does not turn on them — as the last such change demonstrated, moving its sink sets while the argument stayed the same. | DESIGN | unsourced | 1868 |
