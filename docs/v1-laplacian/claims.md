# Claim Inventory — Per-Good Trade Network Spec v1.3

Extracted from `per-good-trade-spec.md`. Extraction only: nothing here is validated,
corrected, or commented on. Statements are paraphrases in the extractor's words; where a
paraphrase risked changing the claim, the spec's own wording is kept.

## Summary

**685 claims extracted**, C001–C685, covering §0 (front matter) through §3.16.

### By Type

| Type | Count |
|---|---|
| DESIGN | 196 |
| MODEL | 195 |
| ENGINE | 186 |
| OUTCOME | 94 |
| WORLD | 14 |
| **Total** | **685** |

### By Provenance

| Provenance | Count |
|---|---|
| derivation | 279 |
| stipulated | 212 |
| UNSOURCED | 137 |
| file value | 35 |
| numerical test | 9 |
| prose source | 9 |
| verified (method unstated) | 3 |
| file value + prose source | 1 |
| engine test | 0 |
| **Total** | **685** |

### UNSOURCED claims (137)

By type: ENGINE 99, OUTCOME 23, WORLD 13, MODEL 2. Densest sections: §2.7 (16), §2.8 (11),
§2.6 (9), §3.3 (9), §1.8 (8), §3.16 (8).

**ENGINE (99)** — assertions about how EU4 behaves with no stated basis:

C021, C025, C026, C027, C028, C035, C037, C046, C049, C057, C068, C071, C076, C084, C092,
C093, C097, C099, C100, C101, C102, C109, C110, C128, C129, C130, C135, C139, C141, C146,
C147, C158, C161, C176, C179, C210, C224, C225, C226, C232, C234, C251, C252, C253, C254,
C258, C262, C267, C269, C272, C274, C275, C278, C280, C281, C282, C283, C284, C285, C287,
C288, C293, C303, C362, C367, C368, C374, C387, C389, C394, C395, C396, C397, C405, C406,
C415, C421, C422, C423, C447, C463, C464, C465, C474, C515, C516, C517, C518, C531, C532,
C533, C537, C538, C550, C556, C599, C606, C613, C624

**OUTCOME (23)** — predictions with no stated basis:

C002, C003, C056, C201, C273, C276, C279, C289, C294, C295, C296, C298, C300, C323, C324,
C326, C327, C332, C349, C401, C426, C610, C659

**WORLD (13)** — historical or project-history assertions with no stated basis:

C356, C359, C361, C477, C574, C673, C674, C675, C676, C678, C680, C681, C682

**MODEL (2)** — mathematical assertions with no stated basis:

C180, C609

### Notes on the extraction

- Every claim is filed under the section it appears in; a proposition stated twice in
  different sections (for example, "at vanilla base prices nothing sits below the anchor",
  C432 in §3.5 and again in §3.13) is given one ID at first appearance and referenced
  by `Depends on` from the second.
- `Depends on` records only dependencies the spec itself asserts or plainly implies. It is
  a claim-to-claim graph, not a citation list. All 685 IDs resolve; there are no dangling
  references.
- Formulas are entered as claims because they can be wrong as definitions of the intended
  quantity, even though they cannot be wrong as arithmetic.
- Probe questions in §2.7 are entered as the claims they presuppose (that there are three
  passes, that the passes may cache independently, that the sim can be paused at the tick
  hook), plus one claim per stated unknown.
- Validation rows in §2.8 are entered as OUTCOME predictions, not as tests.

## Type legend

| Type | Meaning |
|---|---|
| ENGINE | a fact about how EU4 behaves (including its files, UI, and AI) |
| MODEL | a mathematical or structural property of the design itself |
| DESIGN | a preference, goal, choice, or judgment; not truth-apt |
| OUTCOME | a prediction about what the finished mod will do |
| WORLD | a claim about history, the real world, or the project's own review history — truth-apt, but not about EU4 and not about the model |

`WORLD` is an addition to the four requested types. It is used only where a claim is
plainly truth-apt but is neither about EU4 nor about the design's mathematics, so filing
it as DESIGN would have mislabelled a falsifiable assertion as a preference.

## Provenance legend

| Provenance | Meaning |
|---|---|
| stipulated | authored by this spec as a definition, formula, design choice, or goal; no external basis claimed or needed |
| derivation | reasoned in the spec from other claims in the spec |
| file value | read from game files (defines, `00_tradenodes.txt`, saves, script) or from binary/dump inspection |
| numerical test | the spec reports a numerical experiment on the model or solver ("Tested:", "Verified numerically") |
| engine test | the spec reports observing EU4 itself |
| prose source | community post, wiki, forum thread, mod-author report, or external documentation |
| verified (method unstated) | the spec asserts verification without saying by what means |
| UNSOURCED | an assertion about EU4, the world, or the project with no stated or implied basis |

`numerical test` and `engine test` are kept apart deliberately: the spec's "Tested:" passages
are experiments on the solver, not observations of the game, and collapsing them into
`engine test` would overstate what has been checked against EU4. No claim in the spec is
sourced to `engine test`; every EU4 observation is either a probe not yet run (§2.7) or
carries a weaker provenance.

---

## §0 — Front matter (lines 3–7)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C001 | §0 | The mod targets EU4's final patch. | DESIGN | stipulated | — |
| C002 | §0 | The design is compatible with extended-timeline mods. | OUTCOME | UNSOURCED | — |
| C003 | §0 | The design is map-agnostic — it relies on no property of the specific vanilla map. | OUTCOME | UNSOURCED | — |
| C004 | §0 | The spec is a living document, i.e. not final. | DESIGN | stipulated | — |

## §1.1 — Trade direction (lines 13–33)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C005 | §1.1 | Every trade good has its own directed network defined over the same node adjacency. | MODEL | stipulated | — |
| C006 | §1.1 | Direction is computed from state and never authored. | MODEL | stipulated | C005 |
| C007 | §1.1 | For each good `g`, `φ_g` is the solution of the unweighted graph Laplacian equation `L φ_g = s_g − c_g`. | MODEL | stipulated | — |
| C008 | §1.1 | An edge is oriented `u → v` iff `φ_g(u) > φ_g(v)`. | MODEL | stipulated | C007 |
| C009 | §1.1 | The resulting per-good orientation is acyclic by construction. | MODEL | derivation | C007, C008 |
| C010 | §1.1 | A node with no outgoing links for `g` is a sink for `g`. | MODEL | stipulated | C008 |
| C011 | §1.1 | Sinks differ from good to good. | OUTCOME | derivation | C005, C010 |
| C012 | §1.1 | There is no global end node across the per-good networks. | MODEL | derivation | C011 |
| C013 | §1.1 | `L` is singular, with the constant vectors in its null space. | MODEL | derivation | C007 |
| C014 | §1.1 | A solution exists iff `Σ(s − c) = 0` within each connected component. | MODEL | derivation | C013 |
| C015 | §1.1 | That balance condition holds because both `s` and `c` are normalized shares. | MODEL | derivation | C014, C024, C034 |
| C016 | §1.1 | Pinning `φ = 0` at one reference node per component makes the solution unique. | MODEL | derivation | C013 |
| C017 | §1.1 | The solve runs per connected component, with `s` and `c` renormalized within each so they balance. | MODEL | stipulated | C015 |
| C018 | §1.1 | Isolated nodes are skipped. | MODEL | stipulated | — |
| C019 | §1.1 | The whole system is recomputed on a fixed monthly tick. | MODEL | stipulated | — |
| C020 | §1.1 | That tick is aligned to the vanilla trade tick. | MODEL | stipulated | C021 |
| C021 | §1.1 | EU4 has a monthly trade tick to align to. | ENGINE | UNSOURCED | — |
| C022 | §1.1 | Orientation is read from the current solve every time, with no memory of the previous one. | MODEL | stipulated | C019 |

## §1.2 — Supply (lines 35–47)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C023 | §1.2 | `s(n,g) = goods_produced(n,g) / Σ_m goods_produced(m,g)`. | MODEL | stipulated | — |
| C024 | §1.2 | `s` is therefore a share summing to 1 across all nodes producing `g`. | MODEL | derivation | C023 |
| C025 | §1.2 | `goods_produced` is a physical quantity, taken before production efficiency and before autonomy. | ENGINE | UNSOURCED | — |
| C026 | §1.2 | `goods_produced` moves with devastation. | ENGINE | UNSOURCED | — |
| C027 | §1.2 | `goods_produced` moves with occupation. | ENGINE | UNSOURCED | — |
| C028 | §1.2 | `goods_produced` moves with prosperity. | ENGINE | UNSOURCED | — |
| C029 | §1.2 | A regularizer `s ← (1 − ε)·s + ε/N` is mixed in on every solve. | MODEL | stipulated | C023 |
| C030 | §1.2 | `ε ≈ 10⁻⁶`. | DESIGN | stipulated | C029 |

## §1.3 — Demand (lines 49–60)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C031 | §1.3 | Demand is assembled per province and then summed to the node. | MODEL | stipulated | — |
| C032 | §1.3 | `wealth(p) = tax_income(p) + production_income(p)`. | MODEL | stipulated | — |
| C033 | §1.3 | `c(n,g) = Σ_{p∈n} wealth(p)^α(g) / Σ_{q∈world} wealth(q)^α(g)`. | MODEL | stipulated | C032 |
| C034 | §1.3 | `c` is therefore a world-normalized share summing to 1. | MODEL | derivation | C033 |
| C035 | §1.3 | Unowned provinces generate no tax or production income in EU4. | ENGINE | UNSOURCED | — |
| C036 | §1.3 | Unowned provinces therefore contribute nothing to demand. | MODEL | derivation | C032, C035 |
| C037 | §1.3 | EU4 floors overseas provinces at 75% autonomy. | ENGINE | UNSOURCED | — |
| C038 | §1.3 | Because of that floor, an overseas province contributes roughly a quarter of its development's income. | ENGINE | derivation | C037 |
| C039 | §1.3 | `wealth` as defined excludes trade income. | MODEL | stipulated | C032 |

## §1.4 — Market concentration (lines 62–72)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C040 | §1.4 | `α(g) = clamp((price(g)/P₀)^k, α_min, α_max)`. | MODEL | stipulated | — |
| C041 | §1.4 | `P₀ = 2.0` ducats. | DESIGN | stipulated | C040 |
| C042 | §1.4 | `α > 1` makes demand superlinear in provincial wealth. | MODEL | derivation | C033, C040 |
| C043 | §1.4 | With `α > 1`, demand for luxuries concentrates on individually rich provinces. | OUTCOME | derivation | C042 |
| C044 | §1.4 | `α = 1` makes demand proportional to economic size. | MODEL | derivation | C033 |
| C045 | §1.4 | `α < 1` makes demand sublinear, spreading bulk goods toward populous regions. | MODEL | derivation | C033 |
| C046 | §1.4 | Vanilla price events move prices in both directions, so α moves in both directions. | ENGINE | UNSOURCED | C040 |
| C047 | §1.4 | No smoothing is applied to α. | MODEL | stipulated | C040 |

## §1.5 — Goods without a graph (lines 74–78)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C048 | §1.5 | Gold is excluded from the per-good networks by configuration. | DESIGN | stipulated | — |
| C049 | §1.5 | Gold's value is still counted in `wealth` through production income. | ENGINE | UNSOURCED | C032 |
| C050 | §1.5 | The exception is gold diverted by the treasure-fleet mechanic. | ENGINE | derivation | C049, C147 |
| C051 | §1.5 | `s(n,g)` is undefined when nothing in the world produces `g`. | MODEL | derivation | C023 |
| C052 | §1.5 | A good with zero world production has no graph that month. | MODEL | derivation | C051 |
| C053 | §1.5 | Such a good contributes nothing to `Φ`, i.e. `V_g = 0`. | MODEL | derivation | C052, C059 |
| C054 | §1.5 | Such a good is absent from the survival table. | MODEL | derivation | C052 |
| C055 | §1.5 | A good acquires a graph in the first month any province produces it. | MODEL | derivation | C052 |
| C056 | §1.5 | Latent goods stay graphless for long stretches of a campaign. | OUTCOME | UNSOURCED | C052 |
| C057 | §1.5 | Coal is produced nowhere in EU4 until Manufactories arrives. | ENGINE | UNSOURCED | — |
| C058 | §1.5 | Coal therefore appears with a full graph in a single tick. | OUTCOME | derivation | C055, C057 |

## §1.6 — The aggregate graph (lines 80–89)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C059 | §1.6 | `V_g = price(g) · Σ_m goods_produced(m,g)`. | MODEL | stipulated | — |
| C060 | §1.6 | `Φ = Σ_g V_g · φ_g`. | MODEL | stipulated | C007, C059 |
| C061 | §1.6 | `Φ` is a potential, so orienting edges by it is acyclic. | MODEL | derivation | C060 |
| C062 | §1.6 | `Φ` is the graph installed in the game. | DESIGN | stipulated | C060 |
| C063 | §1.6 | With `α = 1` for every good, `Φ` collapses to a scalar multiple of `φ₀`. | MODEL | derivation | C033, C060, C064 |
| C064 | §1.6 | `φ₀` is the single solve with demand at α = 1 and supply as each node's share of world trade value. | MODEL | stipulated | — |
| C065 | §1.6 | A node's world trade value share uses `Σ_p goods_produced(p) × price(good(p))`. | MODEL | stipulated | C064 |
| C066 | §1.6 | The `φ₀` case is computed as a diagnostic but never drawn. | DESIGN | stipulated | C064 |

## §1.7 — Merchants (lines 91–105)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C067 | §1.7 | Merchant placement, range, and the collect/steer choice are unchanged from vanilla. | DESIGN | stipulated | — |
| C068 | §1.7 | Vanilla allows one merchant per country per node. | ENGINE | UNSOURCED | — |
| C069 | §1.7 | A merchant present gives +2 trade power, node-wide. | ENGINE | file value | — |
| C070 | §1.7 | A merchant present gives +10% trade efficiency, node-wide. | ENGINE | file value | — |
| C071 | §1.7 | Those merchant bonuses apply regardless of what the merchant is doing. | ENGINE | UNSOURCED | C069, C070 |
| C072 | §1.7 | Collect behaviour is vanilla, including the −50% penalty outside the home node. | ENGINE | file value | — |
| C073 | §1.7 | The node window is widened to list every link incident to the node, not only the outgoing ones. | DESIGN | stipulated | — |
| C074 | §1.7 | A merchant assigned to link `{n,m}` steers every good oriented `n → m`. | MODEL | stipulated | C073 |
| C075 | §1.7 | That merchant is inert for every good oriented `m → n`. | MODEL | stipulated | C073 |
| C076 | §1.7 | A merchant keeps its link assignment when the link flips. | ENGINE | UNSOURCED | — |
| C077 | §1.7 | Only the merchant's active good set changes when a link flips. | MODEL | derivation | C074, C075, C076 |
| C078 | §1.7 | The same physical link can host a merchant at each end, active on disjoint good sets. | OUTCOME | derivation | C074, C075 |
| C079 | §1.7 | Under the mod, caravan power requires the merchant to be steering at least one good on that link. | DESIGN | stipulated | C074 |
| C080 | §1.7 | Assignment alone does not qualify for caravan power. | DESIGN | stipulated | C079 |
| C081 | §1.7 | The added caravan condition constrains only the two steering conditions. | MODEL | derivation | C079 |
| C082 | §1.7 | Collecting at an inland node as main trading port is untouched by the change. | MODEL | derivation | C083 |
| C083 | §1.7 | The steering-list widening does not affect collection. | MODEL | derivation | C073 |

## §1.8 — Collection and transfer (lines 107–128)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C084 | §1.8 | In the engine, trade power and collect/transfer intent are node-wide, not per good. | ENGINE | UNSOURCED | — |
| C085 | §1.8 | What varies per good is what that node-wide power and intent produce. | MODEL | stipulated | C084 |
| C086 | §1.8 | `collected_share(n,g) = 1` when `n` is a sink for `g`. | MODEL | stipulated | C010 |
| C087 | §1.8 | Otherwise `collected_share(n,g) = P_collect / (P_collect + P_transfer(g))`. | MODEL | stipulated | — |
| C088 | §1.8 | Transfer eligibility is per good. | MODEL | stipulated | C005 |
| C089 | §1.8 | A country's power counts toward `P_transfer(g)` only if it steers `g` at `n` with a merchant, or collects at some node reachable from `n` in `φ_g`. | MODEL | stipulated | C088 |
| C090 | §1.8 | Power meeting neither condition is inert for that good. | MODEL | derivation | C089 |
| C091 | §1.8 | The uncollected remainder moves per good, by the vanilla two-case rule. | MODEL | stipulated | C087 |
| C092 | §1.8 | In vanilla, when any country steers `g` at `n`, outgoing value is divided across outgoing links in proportion to the modified trade power steering toward each link. | ENGINE | UNSOURCED | — |
| C093 | §1.8 | That division is not in proportion to power held in the node generally. | ENGINE | UNSOURCED | C092 |
| C094 | §1.8 | An outgoing link with no steerer receives nothing, even when other links are steered. | ENGINE | derivation | C092 |
| C095 | §1.8 | A single steerer takes all of a good's outgoing value down its link, however little power it holds. | ENGINE | derivation | C092 |
| C096 | §1.8 | Both of those consequences are load-bearing for the design. | DESIGN | stipulated | C094, C095 |
| C097 | §1.8 | If no country steers `g` at `n`, `g`'s outgoing value splits evenly across its outgoing links. | ENGINE | UNSOURCED | — |
| C098 | §1.8 | At `g`'s sink there is no remainder: 100% is collected. | MODEL | derivation | C086 |
| C099 | §1.8 | At a sink, collected value is divided among collectors by trade power. | ENGINE | UNSOURCED | — |
| C100 | §1.8 | Vanilla trade range still gates flow. | ENGINE | UNSOURCED | — |
| C101 | §1.8 | Vanilla supply range still gates flow. | ENGINE | UNSOURCED | — |
| C102 | §1.8 | No transfer occurs into a node where nobody holds power at both ends. | ENGINE | UNSOURCED | — |

## §1.9 — Trade power propagation (lines 130–139)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C103 | §1.9 | Trade power propagation is preserved from vanilla, unchanged. | DESIGN | stipulated | — |
| C104 | §1.9 | A country whose provincial trade power in a node meets the threshold receives a share of it in every immediately upstream node. | ENGINE | prose source | — |
| C105 | §1.9 | That share is `1 / TRADE_PROPAGATE_DIVIDER`. | ENGINE | file value | C104 |
| C106 | §1.9 | The threshold in raw power equals `TRADE_PROPAGATE_THRESHOLD × TRADE_PROPAGATE_DIVIDER`. | ENGINE | derivation | C104, C105, C567 |
| C107 | §1.9 | Ship trade power propagates only where the country has a ship-propagation modifier. | ENGINE | prose source | C104 |
| C108 | §1.9 | Ship propagation happens at the compounded rate: the propagation share multiplied by that modifier. | ENGINE | prose source | C105, C107 |
| C109 | §1.9 | Propagation is strictly one hop and never chains. | ENGINE | UNSOURCED | — |
| C110 | §1.9 | A node receives the summed contributions of all its downstream neighbours. | ENGINE | UNSOURCED | C104 |
| C111 | §1.9 | For propagation, direction is read from `Φ`. | DESIGN | stipulated | C062 |

## §1.10 — Direction-dependent systems (lines 141–171)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C112 | §1.10 | Any mechanism gated on one nation being upstream or downstream of another evaluates TRUE. | DESIGN | stipulated | — |
| C113 | §1.10 | Any node-pair direction dependency reads `Φ`. | DESIGN | stipulated | C062 |
| C114 | §1.10 | Where a gate scopes a set or a path, that scope reads `Φ`. | DESIGN | stipulated | C062 |
| C115 | §1.10 | Fallback rung 1 is the `Φ` path. | DESIGN | stipulated | C114 |
| C116 | §1.10 | Fallback rung 2, used when `Φ` does not connect the pair, is the shortest path within a single good's graph that does. | DESIGN | stipulated | C114 |
| C117 | §1.10 | Fallback rung 3, used only if no good connects them, is the undirected shortest path. | DESIGN | stipulated | C114 |
| C118 | §1.10 | The listed threshold mechanics are left unpatched and unchanged. | DESIGN | stipulated | — |
| C119 | §1.10 | Reorientation reaches those mechanics through the trade power distribution, not through any direction test. | MODEL | derivation | C103, C118 |
| C120 | §1.10 | Because propagation is direction-dependent, a flip moves propagated power at both ends of the flipped link. | MODEL | derivation | C104, C111 |
| C121 | §1.10 | A flip changes fan-out across the neighbourhood. | OUTCOME | derivation | C120 |
| C122 | §1.10 | All of these mechanics move monthly. | OUTCOME | derivation | C019, C120 |
| C123 | §1.10 | The trade-conflict casus belli target threshold is `JUSTIFY_TRADE_CONFLICT_LIMIT`. | ENGINE | file value | — |
| C124 | §1.10 | The trade-conflict casus belli actor threshold is `JUSTIFY_TRADE_CONFLICT_ACTOR_LIMIT`. | ENGINE | file value | — |
| C125 | §1.10 | The privateer-blocking threshold is `MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER`. | ENGINE | file value | — |
| C126 | §1.10 | The trade company extra-merchant threshold is `TRADE_COMPANY_STRONG_LIMIT`. | ENGINE | file value | — |
| C127 | §1.10 | The trade company control threshold is `TRADE_COMPANY_CONTROL_LIMIT`. | ENGINE | file value | — |
| C128 | §1.10 | Improve Inland Routes requires 33% trade power. | ENGINE | UNSOURCED | — |
| C129 | §1.10 | Propagate Religion requires 50% trade power to establish. | ENGINE | UNSOURCED | — |
| C130 | §1.10 | Propagate Religion requires 40% trade power to maintain. | ENGINE | UNSOURCED | — |
| C131 | §1.10 | All the listed thresholds are single-valued except Propagate Religion. | ENGINE | derivation | C123, C124, C125, C126, C127, C128, C129, C130 |
| C132 | §1.10 | Propagate Religion's 50/40 band absorbs threshold chatter on its own. | OUTCOME | derivation | C129, C130 |
| C133 | §1.10 | Casus belli availability is the most visible symptom of threshold crossing. | OUTCOME | derivation | C123, C124 |
| C134 | §1.10 | Casus belli availability can appear and vanish month to month. | OUTCOME | derivation | C122, C133 |
| C135 | §1.10 | Caravan power is not a threshold mechanic but a step function on raw power. | ENGINE | UNSOURCED | — |
| C136 | §1.10 | When caravan power applies it is worth up to the cap for any major power. | ENGINE | derivation | C135, C542 |
| C137 | §1.10 | Caravan power is enough to move a node's power shares by itself. | OUTCOME | derivation | C136 |
| C138 | §1.10 | Caravan power can therefore push other countries across the listed thresholds. | OUTCOME | derivation | C137 |
| C139 | §1.10 | Missions, decisions, events, and trade companies reference trade nodes by name. | ENGINE | UNSOURCED | — |
| C140 | §1.10 | Trade nodes themselves never change under the mod; only connections do. | MODEL | stipulated | — |
| C141 | §1.10 | The engine treats connection-only changes as conflict-free. | ENGINE | UNSOURCED | C140 |
| C142 | §1.10 | A mission whose sense depends on a specific authored direction can become moot under reorientation. | OUTCOME | derivation | C139, C140 |
| C143 | §1.10 | That breakage is accepted and deferred to a compatibility pass rather than engineered around. | DESIGN | stipulated | C142 |

## §1.11 — Treasure fleets (lines 173–177)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C144 | §1.11 | The overlord always receives the treasure fleet. | DESIGN | stipulated | — |
| C145 | §1.11 | The fleet routes by the §1.10 fallback ladder. | DESIGN | stipulated | C115, C116, C117 |
| C146 | §1.11 | Privateers skim a share of the fleet proportional to their power at each node it passes. | ENGINE | UNSOURCED | — |
| C147 | §1.11 | Where the diversion mechanic is active, colonial gold income is diverted from the colonial nation. | ENGINE | UNSOURCED | — |
| C148 | §1.11 | Diverted colonial gold does not enter `wealth` at either end. | MODEL | stipulated | C032, C147 |

## §1.12 — What the game displays (lines 179–193)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C149 | §1.12 | The in-game economy is the per-good economy. | DESIGN | stipulated | — |
| C150 | §1.12 | Node values, the node window, pie charts, the ledger, the economy tab, and tooltips all show the model's numbers. | OUTCOME | stipulated | C149 |
| C151 | §1.12 | Trade map mode colours provinces by node. | OUTCOME | stipulated | — |
| C152 | §1.12 | Trade map mode draws arrows between nodes from `Φ`. | OUTCOME | stipulated | C062 |
| C153 | §1.12 | Arrow weight comes from realized value crossing the link. | DESIGN | stipulated | C152 |
| C154 | §1.12 | Clicking a province switches province colouring to the vanilla trade-goods rendering for that good. | OUTCOME | stipulated | — |
| C155 | §1.12 | Clicking a province redirects the arrow layer to that good's graph. | OUTCOME | stipulated | C005 |
| C156 | §1.12 | A sink is then visible as a node with no outgoing arrows. | OUTCOME | derivation | C010, C155 |
| C157 | §1.12 | Clicking the node icon clears the view back to `Φ`. | OUTCOME | stipulated | C152 |
| C158 | §1.12 | The vanilla UI holds one value field per node. | ENGINE | UNSOURCED | — |
| C159 | §1.12 | EU4 has about thirty trade goods. | ENGINE | file value | — |
| C160 | §1.12 | Per-commodity value breakdown is therefore not representable in the vanilla UI. | ENGINE | derivation | C158, C159 |
| C161 | §1.12 | The vanilla UI holds one scalar per link. | ENGINE | UNSOURCED | — |
| C162 | §1.12 | A link's two-way traffic is therefore not representable and is shown as net. | ENGINE | derivation | C161 |
| C163 | §1.12 | Per-country effective trade power is not representable where eligibility differs by good. | ENGINE | derivation | C088, C084 |
| C164 | §1.12 | Those three quantities are shown in the companion overlay instead, with trade power as a value-weighted aggregate. | DESIGN | stipulated | C160, C162, C163 |
| C165 | §1.12 | No new art, sprites, shaders, or map-mode chrome is required. | OUTCOME | stipulated | — |
| C166 | §1.12 | The §1.7 steering-list widening is the only UI change. | DESIGN | stipulated | C073 |

## §2.1 — Shape (lines 199–205)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C167 | §2.1 | The mod is one program: a runtime-attached DLL. | DESIGN | stipulated | — |
| C168 | §2.1 | Each month the DLL reads live game state. | DESIGN | stipulated | C019 |
| C169 | §2.1 | Each month it solves per good. | DESIGN | stipulated | C007 |
| C170 | §2.1 | It propagates the per-good economy externally, outside the engine. | DESIGN | stipulated | — |
| C171 | §2.1 | It writes the result and the orientation back into the engine's own structures. | DESIGN | stipulated | — |
| C172 | §2.1 | It ships with a generated `00_tradenodes.txt` for load time. | DESIGN | stipulated | — |
| C173 | §2.1 | It ships with a companion overlay for what the engine cannot display. | DESIGN | stipulated | C164 |
| C174 | §2.1 | The target platform is Windows/Steam. | DESIGN | stipulated | — |
| C175 | §2.1 | The mod runs non-ironman only. | DESIGN | stipulated | — |
| C176 | §2.1 | Achievements and ironman are off with the mod installed. | ENGINE | UNSOURCED | C175 |
| C177 | §2.1 | Multiplayer is unsupported by default. | DESIGN | stipulated | — |
| C178 | §2.1 | An identical build on all machines is necessary but not sufficient for multiplayer. | MODEL | derivation | C179, C180 |
| C179 | §2.1 | EU4 multiplayer is lockstep with checksums. | ENGINE | UNSOURCED | — |
| C180 | §2.1 | An in-process floating-point solve can produce different results on different hardware. | MODEL | UNSOURCED | — |
| C181 | §2.1 | Differing SIMD dispatch or accumulation order in the linear algebra is enough to desync a session. | OUTCOME | derivation | C179, C180 |
| C182 | §2.1 | Multiplayer support requires the solve to be bit-reproducible across machines. | MODEL | derivation | C181 |
| C183 | §2.1 | Bit-reproducibility requires fixed accumulation order, no runtime-dispatched vector paths, and no threaded reduction. | MODEL | derivation | C182 |
| C184 | §2.1 | Until that is built and verified, the mod ships single-player only. | DESIGN | stipulated | C183 |

## §2.2 — Solver (lines 207–222)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C185 | §2.2 | A parser for `common/tradenodes/00_tradenodes.txt` is required. | DESIGN | stipulated | — |
| C186 | §2.2 | That file contains adjacency, `members`, `path`/`control` render data, and `end`/`inland`/AI flags. | ENGINE | file value | — |
| C187 | §2.2 | A parser for non-ironman saves is required. | DESIGN | stipulated | C175 |
| C188 | §2.2 | Non-ironman saves expose province owner, `base_tax`, `base_production`, trade good, goods produced, and development. | ENGINE | file value | — |
| C189 | §2.2 | A parser for `common/defines.lua` is required. | DESIGN | stipulated | C211 |
| C190 | §2.2 | `common/defines.lua` is merged with `common/defines/` overrides in load order. | ENGINE | file value | — |
| C191 | §2.2 | The solver computes per-province `wealth`, per-node `trade_value`, `s`, and `c` with per-province α, plus the ε regularizer. | DESIGN | stipulated | C029, C032, C033 |
| C192 | §2.2 | The per-good system is solved via sparse Cholesky. | DESIGN | stipulated | C007 |
| C193 | §2.2 | The solver computes `Φ`, and `φ₀` for the identity check. | DESIGN | stipulated | C060, C064 |
| C194 | §2.2 | A survival table `S_g[n][H]` is computed for AI scoring. | DESIGN | stipulated | — |
| C195 | §2.2 | One survival table serves every country. | MODEL | derivation | C588 |
| C196 | §2.2 | A mutual reachability census runs 30 goods × 80 BFS. | DESIGN | stipulated | C159, C199 |
| C197 | §2.2 | The census produces an 80×80 matrix whose entries count the goods having a directed path `n → … → m`. | MODEL | stipulated | C196 |
| C198 | §2.2 | A synthetic-shock harness edits parsed province data and re-solves. | DESIGN | stipulated | — |
| C199 | §2.2 | EU4 has roughly 80 trade nodes. | ENGINE | file value | — |
| C200 | §2.2 | Each per-good solve is a sparse SPD system of roughly 80×80. | MODEL | derivation | C199 |
| C201 | §2.2 | Each such solve costs microseconds. | OUTCOME | UNSOURCED | C200 |
| C202 | §2.2 | The listed solver is the reference implementation: standalone, run against parsed saves. | DESIGN | stipulated | — |
| C203 | §2.2 | Every validation in §2.8 is measured on the reference solver. | DESIGN | stipulated | C202 |
| C204 | §2.2 | The shipped DLL carries a second implementation of solver items 4–7 in the host language. | DESIGN | stipulated | — |
| C205 | §2.2 | The DLL implementation reads live memory instead of save files. | DESIGN | stipulated | C204 |
| C206 | §2.2 | The two implementations must agree. | DESIGN | stipulated | C202, C204 |
| C207 | §2.2 | Where they disagree, the reference is correct by definition. | DESIGN | stipulated | C206 |
| C208 | §2.2 | The parsers and the shock harness stay reference-only, and the DLL never reads a save. | DESIGN | stipulated | C205 |
| C209 | §2.2 | Inland status is derived as "no coastal province among the node's `members`" rather than trusted from the file's flag. | DESIGN | stipulated | C210 |
| C210 | §2.2 | The node file's `inland` flag cannot be trusted. | ENGINE | UNSOURCED | C186 |

## §2.3 — Constants (lines 224–241)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C211 | §2.3 | All engine constants are read at runtime and never hardcoded. | DESIGN | stipulated | — |
| C212 | §2.3 | `TRADE_PROPAGATE_DIVIDER` is the define governing the propagation share. | ENGINE | file value | C105 |
| C213 | §2.3 | `TRADE_PROPAGATE_THRESHOLD` is the define governing the propagation threshold. | ENGINE | file value | C106 |
| C214 | §2.3 | `TRADE_NON_CAPITAL_OFFICE` is the define governing the off-home collect penalty. | ENGINE | file value | C072 |
| C215 | §2.3 | `TRADE_POWER_HOME_BONUS` is the define governing the home-node steering bonus. | ENGINE | file value | C216 |
| C216 | §2.3 | Vanilla has a home-node steering bonus. | ENGINE | file value | — |
| C217 | §2.3 | `MERCHANT_MAX_POWER_BONUS` and `TRADE_MERCHANT_PRESENT` are the defines governing merchant power and efficiency. | ENGINE | file value | C069, C070 |
| C218 | §2.3 | `TRADE_ADDED_VALUE_MODIFER` is the define for the link boost base. | ENGINE | file value | — |
| C219 | §2.3 | `CARAVAN_FACTOR`, `CARAVAN_POWER_MAX`, and `CARAVAN_POWER_MIN` are the caravan defines. | ENGINE | file value | — |
| C220 | §2.3 | `PS_MOVE_TRADE_PORT` is the define for the trade capital move cost. | ENGINE | file value | — |
| C221 | §2.3 | Only two design constants remain in the model. | DESIGN | stipulated | C041, C222 |
| C222 | §2.3 | The excluded-goods list defaults to gold. | DESIGN | stipulated | C048 |
| C223 | §2.3 | DLC state is a third input axis alongside game files and saves. | DESIGN | stipulated | — |
| C224 | §2.3 | Treasure-fleet diversion is DLC-conditional. | ENGINE | UNSOURCED | — |
| C225 | §2.3 | Caravan power is DLC-conditional. | ENGINE | UNSOURCED | — |
| C226 | §2.3 | Caravan modifier values are readable even when the mechanic is inert. | ENGINE | UNSOURCED | C225 |
| C227 | §2.3 | Therefore the implementation must key on the DLC flag, never on the presence of a value. | DESIGN | derivation | C224, C225, C226 |

## §2.4 — The tradenodes file (lines 243–252)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C228 | §2.4 | `00_tradenodes.txt` is generated once from the campaign start date's `Φ`. | DESIGN | stipulated | C062 |
| C229 | §2.4 | After generation the node structure is owned by the DLL in memory. | DESIGN | stipulated | C171 |
| C230 | §2.4 | There is no per-session regeneration of the file. | DESIGN | stipulated | C228 |
| C231 | §2.4 | Merchants are recalled only when the mod is rebuilt. | OUTCOME | derivation | C230, C232 |
| C232 | §2.4 | Regenerating the node file recalls merchants. | ENGINE | UNSOURCED | — |
| C233 | §2.4 | A mid-campaign load runs on the start-date file for up to one month. | OUTCOME | derivation | C019, C228 |
| C234 | §2.4 | The engine performs no topological sort of the node file. | ENGINE | UNSOURCED | — |
| C235 | §2.4 | The emitted file must therefore itself be topologically sorted. | DESIGN | derivation | C234 |
| C236 | §2.4 | Declaration order is emitted in decreasing `Φ`. | DESIGN | stipulated | C235 |
| C237 | §2.4 | `end=yes` is emitted on every `Φ` sink. | DESIGN | stipulated | C062 |
| C238 | §2.4 | `end=yes` is stripped from any former end node that gains outgoing links. | DESIGN | stipulated | C237 |
| C239 | §2.4 | Reversing a link requires moving the `outgoing` block, reversing the `path` province list, and reversing the `control` pairs. | ENGINE | file value | C186 |
| C240 | §2.4 | One hand-flipped link is to be verified before generator code is written. | DESIGN | stipulated | C239 |
| C241 | §2.4 | `location`, `members`, `inland=yes`, `ai_will_propagate_through_trade`, and unrecognized keys round-trip byte-faithfully. | DESIGN | stipulated | — |
| C242 | §2.4 | The node file contains `location`, `members`, `inland`, and `ai_will_propagate_through_trade` keys. | ENGINE | file value | — |

## §2.5 — Runtime attachment (lines 254–258)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C243 | §2.5 | Attachment uses pattern scanning and function hooking. | DESIGN | stipulated | — |
| C244 | §2.5 | The EU4dll precedent provides attach scaffolding on this binary. | ENGINE | prose source | — |
| C245 | §2.5 | EU4dll provides nothing about trade structures. | ENGINE | prose source | C244 |
| C246 | §2.5 | The mod ships a runtime-patching DLL, not a modified executable. | DESIGN | stipulated | C167 |
| C247 | §2.5 | The EU4 binary is frozen. | ENGINE | derivation | C001 |
| C248 | §2.5 | Therefore offsets found stay found. | OUTCOME | derivation | C247 |
| C249 | §2.5 | The nation-pair direction gates of §1.10 are hooked and returned true at the call site. | DESIGN | stipulated | C112 |
| C250 | §2.5 | They are not implemented by forcing any shared predicate. | DESIGN | stipulated | C249 |

## §2.6 — Writing to the engine (lines 260–280)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C251 | §2.6 | The monthly trade tick runs in three passes. | ENGINE | UNSOURCED | — |
| C252 | §2.6 | Pass 1 computes static power and modifiers. | ENGINE | UNSOURCED | C251 |
| C253 | §2.6 | Pass 2 runs from the end nodes, determining modified power and adding propagation. | ENGINE | UNSOURCED | C251 |
| C254 | §2.6 | Pass 3 is a value pass from the origin nodes: node value → collect/steer split → collect division → outgoing division with steering bonuses. | ENGINE | UNSOURCED | C251 |
| C255 | §2.6 | Node trade value is written as `Σ_g value_g(n)`. | DESIGN | stipulated | — |
| C256 | §2.6 | Node collectible pool is written as `Σ_g value_g(n)·collected_share(n,g)`. | DESIGN | stipulated | C086, C087 |
| C257 | §2.6 | Per-link value is written as the net `Σ_g` realized flow in the installed `Φ` direction. | DESIGN | stipulated | C062 |
| C258 | §2.6 | Country trade income is derived by the engine from the written fields, unless it is stored. | ENGINE | UNSOURCED | — |
| C259 | §2.6 | Feeding the engine the collectible pool is sufficient to pay every country correctly. | MODEL | derivation | C264, C265 |
| C260 | §2.6 | `collect_pool` is per good on the inside. | MODEL | derivation | C256, C261 |
| C261 | §2.6 | `collected_share(n,g)` depends on `P_transfer(g)`, which §1.8 makes commodity-specific. | MODEL | derivation | C087, C088 |
| C262 | §2.6 | `powershare_C` is a country's share among collectors. | ENGINE | UNSOURCED | C099 |
| C263 | §2.6 | Whether a country collects is a merchant-or-home property with no good dependence. | MODEL | derivation | C067 |
| C264 | §2.6 | A good-independent share multiplying a per-good sum collapses to one scalar. | MODEL | derivation | C262, C263 |
| C265 | §2.6 | The engine's own vanilla collection math then reproduces every country's per-good income exactly. | MODEL | derivation | C264 |
| C266 | §2.6 | Display figures must be written immediately after the value pass. | DESIGN | derivation | C267 |
| C267 | §2.6 | AI consumers read those figures during the month. | ENGINE | UNSOURCED | — |
| C268 | §2.6 | Payment writes are bounded by the month boundary. | DESIGN | derivation | C269 |
| C269 | §2.6 | The treasury reconciles at the start of each month against the previous month's income. | ENGINE | UNSOURCED | — |
| C270 | §2.6 | There are two deadlines, not one window. | MODEL | derivation | C266, C268 |
| C271 | §2.6 | Per-link written values can be negative where realized flow opposes the drawn arrow. | MODEL | derivation | C257, C508 |
| C272 | §2.6 | The engine accepts a negative per-link value. | ENGINE | UNSOURCED | C271 |

## §2.7 — Probes (lines 282–297)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C273 | §2.7 | All ten probes can be settled with a debugger on a vanilla install in one session. | OUTCOME | UNSOURCED | — |
| C274 | §2.7 | The three passes may cache independently of one another. | ENGINE | UNSOURCED | C251 |
| C275 | §2.7 | Flipping a link may crash the engine, produce stale-but-running values, or rebuild cleanly. | ENGINE | UNSOURCED | C274 |
| C276 | §2.7 | Staleness would show as one-month corridor lag, value vanishing, tooltips disagreeing with arrows, or propagation crediting the wrong side. | OUTCOME | UNSOURCED | C275 |
| C277 | §2.7 | Pass 2 has an ordering requirement whose cause is unidentified. | ENGINE | derivation | C109, C253 |
| C278 | §2.7 | Where income accumulation sits relative to the value pass is unknown. | ENGINE | UNSOURCED | C254 |
| C279 | §2.7 | Writing country trade income before month-boundary reconciliation may make AI budgeting and AI cash read the same figure. | OUTCOME | UNSOURCED | C269 |
| C280 | §2.7 | A negative link value can be written and its arrow rendering observed. | ENGINE | UNSOURCED | C272 |
| C281 | §2.7 | Link values feed a protect-trade allocation. | ENGINE | UNSOURCED | — |
| C282 | §2.7 | Flipping a link that hosts a steering merchant may dangle, reset, or crash the assignment. | ENGINE | UNSOURCED | C076 |
| C283 | §2.7 | Whether the engine grants caravan power for a merchant assigned to a link that is incoming in `Φ` is unknown. | ENGINE | UNSOURCED | C079 |
| C284 | §2.7 | Whether the engine grants caravan power for a merchant whose link carries no goods is unknown. | ENGINE | UNSOURCED | C079 |
| C285 | §2.7 | Whether arrow render state is separate from the economic link is unknown. | ENGINE | UNSOURCED | — |
| C286 | §2.7 | Setting `TRADE_PROPAGATE_THRESHOLD` to 4 would double the raw requirement if the propagated-units reading is right. | ENGINE | derivation | C106 |
| C287 | §2.7 | Whether diverted colonial gold still appears in the per-province production income field is unknown. | ENGINE | UNSOURCED | C147 |
| C288 | §2.7 | The DLC flag is expected to agree with the observed diverted-gold field. | ENGINE | UNSOURCED | C224 |
| C289 | §2.7 | Every call site of "is X downstream of Y" can be enumerated by disassembly. | OUTCOME | UNSOURCED | — |
| C290 | §2.7 | Those call sites classify as: return true; return true and define the scope; or compute per good. | DESIGN | stipulated | C112, C114 |
| C291 | §2.7 | A companion "not members" list will be produced alongside the call-site list. | DESIGN | stipulated | C289 |
| C292 | §2.7 | All writes land atomically at the tick hook with the sim paused. | DESIGN | stipulated | C293 |
| C293 | §2.7 | The sim can be paused at the tick hook. | ENGINE | UNSOURCED | — |

## §2.8 — Validation (lines 299–333)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C294 | §2.8 | Spice and cloves in 1444 source in Indonesia. | OUTCOME | UNSOURCED | C023 |
| C295 | §2.8 | Spice and cloves in 1444 sink in both China and Europe. | OUTCOME | UNSOURCED | C010, C033 |
| C296 | §2.8 | In 1444 most goods have their largest sinks in India and China. | OUTCOME | UNSOURCED | C033 |
| C297 | §2.8 | That India/China sink concentration is correct behaviour, not a failure. | DESIGN | stipulated | C296 |
| C298 | §2.8 | Post-1500, spice routes Malacca → … → Cape → … → Europe. | OUTCOME | UNSOURCED | C008 |
| C299 | §2.8 | Pre-1500 that corridor is withheld by range and the power-at-both-ends gate, not by direction. | OUTCOME | derivation | C100, C101, C102 |
| C300 | §2.8 | A 1000 AD start puts sinks in the Muslim world and Song China with no era-specific data added. | OUTCOME | UNSOURCED | C033 |
| C301 | §2.8 | Zeroing Beijing-node development relocates the sink in one solve. | OUTCOME | derivation | C033, C022 |
| C302 | §2.8 | If Ming loses the Mandate, Beijing's pull collapses with its income. | OUTCOME | derivation | C032, C303 |
| C303 | §2.8 | Losing the Mandate of Heaven substantially cuts Ming's income. | ENGINE | UNSOURCED | — |
| C304 | §2.8 | A major war in China shifts corridors for its duration. | OUTCOME | derivation | C027 |
| C305 | §2.8 | Those corridors revert as devastation heals. | OUTCOME | derivation | C026 |
| C306 | §2.8 | Given many poor provinces versus few rich ones, luxury demand goes to the rich-province node. | OUTCOME | derivation | C043 |
| C307 | §2.8 | Bulk demand goes to the many-province node. | OUTCOME | derivation | C045 |
| C308 | §2.8 | A price crash drives α below 1. | OUTCOME | derivation | C040 |
| C309 | §2.8 | A price crash makes regional sinks reappear. | OUTCOME | derivation | C045, C308 |
| C310 | §2.8 | In the 1650 Caribbean, sugar production income makes it a sink for cloth, tools, and wine. | OUTCOME | derivation | C032 |
| C311 | §2.8 | In 1000, Kilwa's ivory income makes it a sink for Indian textiles. | OUTCOME | derivation | C032 |
| C312 | §2.8 | A consuming leaf node terminates the DAG of every good it consumes but does not produce. | MODEL | derivation | C010 |
| C313 | §2.8 | An inert merchant's goods take the even split as if the node were empty. | OUTCOME | derivation | C075, C097 |
| C314 | §2.8 | An inert merchant's node-wide bonuses still apply. | OUTCOME | derivation | C071 |
| C315 | §2.8 | At a node sinking spice but not cloth, spice is fully collected while cloth is collected at the ratio with its remainder pushed. | MODEL | derivation | C086, C087 |
| C316 | §2.8 | A near-balanced link may flip monthly. | OUTCOME | derivation | C019, C022 |
| C317 | §2.8 | A flipping link carries near-zero value either way. | OUTCOME | derivation | C316 |
| C318 | §2.8 | Merchant assignments survive such flips. | OUTCOME | derivation | C076 |
| C319 | §2.8 | A two-way Atlantic corridor works with merchants at both ends on disjoint good sets, neither blocking the other. | OUTCOME | derivation | C078 |
| C320 | §2.8 | Every displayed trade figure matches the per-good economy to the ducat. | OUTCOME | derivation | C265 |
| C321 | §2.8 | Forcing α = 1 makes `Φ` a scalar multiple of `φ₀` on real data. | MODEL | derivation | C063 |
| C322 | §2.8 | Acyclicity is asserted on every solve. | DESIGN | stipulated | C009 |
| C323 | §2.8 | An observer run to 1600 shows New World colonization proceeding at roughly vanilla pace. | OUTCOME | UNSOURCED | — |
| C324 | §2.8 | Greedy AI merchant assignment settles with damping rather than oscillating. | OUTCOME | UNSOURCED | C610 |
| C325 | §2.8 | A latent good has no graph, no `Φ` contribution and no survival-table entry, and acquires all three the month production begins. | MODEL | derivation | C052, C053, C054, C055 |
| C326 | §2.8 | The DLL solver and the reference solver agree on orientation exactly for every save in the historical set. | OUTCOME | UNSOURCED | C206 |
| C327 | §2.8 | They agree on `φ` to tolerance for every save in the historical set. | OUTCOME | UNSOURCED | C206 |
| C328 | §2.8 | There is a historical set of saves to validate against. | DESIGN | stipulated | — |
| C329 | §2.8 | `Φ`-vs-realized sign disagreement is weighted by trade value, not link count. | DESIGN | stipulated | C271 |
| C330 | §2.8 | That disagreement is predicted to cluster at nodes with 3+ outgoing links and partial merchant coverage. | OUTCOME | derivation | C092, C097 |
| C331 | §2.8 | It is predicted to thin as merchant coverage densifies. | OUTCOME | derivation | C330 |
| C332 | §2.8 | Flip behaviour per decade differs between peace and war. | OUTCOME | UNSOURCED | C027 |
| C333 | §2.8 | Flips revert as occupation lifts. | OUTCOME | derivation | C027 |
| C334 | §2.8 | Propagated-share change per node is measured on each flip, alongside the trade-power/in-degree covariance. | DESIGN | stipulated | C120 |
| C335 | §2.8 | That measurement is what catches the §1.10 threshold mechanics flickering. | OUTCOME | derivation | C119, C334 |
| C336 | §2.8 | A power share crossing a single-valued limit is the failure mode. | OUTCOME | derivation | C131 |
| C337 | §2.8 | Casus belli availability is the visible symptom of that failure. | OUTCOME | derivation | C133 |
| C338 | §2.8 | Total propagated power is not the quantity to watch. | MODEL | derivation | C339 |
| C339 | §2.8 | Reorientation cannot change edge count, so `Σ indeg` equals the edge count and is invariant. | MODEL | derivation | C140 |
| C340 | §2.8 | Only the trade-power/in-degree covariance moves under reorientation. | MODEL | derivation | C339 |
| C341 | §2.8 | Income balance is measured as total world collected income and as its distribution across historical great powers. | DESIGN | stipulated | — |
| C342 | §2.8 | The distribution metric is the gating one. | DESIGN | stipulated | C341 |

## §2.9 — Build order (lines 335–343)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C343 | §2.9 | The build is two parallel tracks, not phases. | DESIGN | stipulated | — |
| C344 | §2.9 | The defines parser comes first on the solver track. | DESIGN | stipulated | C345 |
| C345 | §2.9 | Because every constant is a runtime read, the eligibility threshold, propagation share, off-home penalty, merchant bonuses and caravan terms are all downstream of the defines parser. | MODEL | derivation | C211 |
| C346 | §2.9 | None of them can be written correctly before the defines parser exists. | MODEL | derivation | C345 |
| C347 | §2.9 | The solver track then does ε, per-good eligibility, realized flows, the `Φ`-vs-realized disagreement measurement, the reachability census, and the flip-rate measurement. | DESIGN | stipulated | — |
| C348 | §2.9 | The memory track is the §2.7 probe session. | DESIGN | stipulated | C273 |
| C349 | §2.9 | All ten probe items can be done on one trace. | OUTCOME | UNSOURCED | C273 |
| C350 | §2.9 | Afterwards the classified call-site list is written into the spec. | DESIGN | stipulated | C289 |
| C351 | §2.9 | Afterwards income balance is gated on both metrics. | DESIGN | stipulated | C341 |
| C352 | §2.9 | Afterwards the negative-link display policy is decided against a measured number. | DESIGN | stipulated | C329 |

## §3.1 — Goals (lines 349–357)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C353 | §3.1 | Goal 1: trade direction follows the world's current state and never authored arrows. | DESIGN | stipulated | C006 |
| C354 | §3.1 | A horde razing Beijing moves the sink because the wealth moved. | OUTCOME | derivation | C032, C301 |
| C355 | §3.1 | Goal 2: commodities should flow differently from one another. | DESIGN | stipulated | C005 |
| C356 | §3.1 | China is simultaneously a silk source and a spice sink. | WORLD | UNSOURCED | — |
| C357 | §3.1 | A single trade graph cannot represent a node that is source and sink at once for different goods. | MODEL | derivation | C005, C356 |
| C358 | §3.1 | Goal 3: preserve the feedback loop in which sinks accumulate value, fund development, and reinforce themselves. | DESIGN | stipulated | — |
| C359 | §3.1 | Value accumulation funding development is how mercantile hegemonies form. | WORLD | UNSOURCED | — |
| C360 | §3.1 | Goal 4: represent return flows. | DESIGN | stipulated | — |
| C361 | §3.1 | Export regions historically imported manufactures. | WORLD | UNSOURCED | — |
| C362 | §3.1 | Vanilla EU4 cannot express return flows at all. | ENGINE | UNSOURCED | — |
| C363 | §3.1 | Goal 5: direction must reflect where a good can ultimately reach, not which neighbour is richer. | DESIGN | stipulated | — |
| C364 | §3.1 | Goal 6: zero authored data. | DESIGN | stipulated | C006 |
| C365 | §3.1 | Goal 7: the game's own numbers are the model's numbers, so anything reading trade income reads the real one. | DESIGN | stipulated | C149 |

## §3.2 — Why a potential field (lines 359–367)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C366 | §3.2 | Orienting each edge by comparing its endpoints fails on the Malacca–Cape corridor. | MODEL | derivation | C369, C371 |
| C367 | §3.2 | The Cape has almost no wealth. | ENGINE | UNSOURCED | — |
| C368 | §3.2 | The Cape consumes almost nothing. | ENGINE | UNSOURCED | — |
| C369 | §3.2 | A local endpoint comparison therefore orients the Cape edge into Malacca. | MODEL | derivation | C367, C368 |
| C370 | §3.2 | The deeper failure is that rank orientation is monotone. | MODEL | derivation | — |
| C371 | §3.2 | Under a monotone orientation no path can dip through a low-value intermediary and rise again. | MODEL | derivation | C370 |
| C372 | §3.2 | Malacca → … → Cape → … → Europe requires exactly such a dip and rise. | MODEL | derivation | C367, C368 |
| C373 | §3.2 | Merchants cannot repair a wrong orientation. | ENGINE | derivation | C374 |
| C374 | §3.2 | A merchant selects among existing outgoing arrows and cannot reverse one. | ENGINE | UNSOURCED | — |
| C375 | §3.2 | Route-awareness must therefore live in the orientation itself. | DESIGN | derivation | C373 |
| C376 | §3.2 | Where `s(n) = c(n) = 0`, the equation reduces to `φ(n)` being the average of its neighbours. | MODEL | derivation | C007 |
| C377 | §3.2 | A pure conduit therefore lies strictly between its neighbours in `φ`. | MODEL | derivation | C376 |
| C378 | §3.2 | A pure conduit can only pass flow through. | MODEL | derivation | C377 |
| C379 | §3.2 | The Cape routes spice westward because Europe draws on the far end. | OUTCOME | derivation | C378 |
| C380 | §3.2 | Sinks are net consumers automatically. | MODEL | derivation | C381, C382 |
| C381 | §3.2 | A DAG-sink is a local minimum of `φ`. | MODEL | derivation | C008, C010 |
| C382 | §3.2 | By the discrete maximum principle, local minima of `φ` occur only where `c > s`. | MODEL | derivation | C007 |
| C383 | §3.2 | Peripheral sinks are intended, not a defect. | DESIGN | stipulated | — |
| C384 | §3.2 | Goods flow to a periphery and are consumed at the end of the line. | OUTCOME | derivation | C380 |
| C385 | §3.2 | Value only arrives where someone holds power at both ends of the link. | ENGINE | derivation | C102 |

## §3.3 — Why wealth, and why per province (lines 369–377)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C386 | §3.3 | Demand is purchasing power. | DESIGN | stipulated | — |
| C387 | §3.3 | Purchasing power is income the game already computes. | ENGINE | UNSOURCED | C032 |
| C388 | §3.3 | Using income captures return flows for free. | MODEL | derivation | C032, C360 |
| C389 | §3.3 | A sugar island has negligible development but large production income. | ENGINE | UNSOURCED | — |
| C390 | §3.3 | Such an island therefore becomes a genuine consumer of cloth and tools. | OUTCOME | derivation | C032, C389 |
| C391 | §3.3 | Using income introduces no colonial-nation dependency and no timeline restriction. | MODEL | derivation | C032 |
| C392 | §3.3 | Income was chosen for responsiveness rather than stability. | DESIGN | stipulated | — |
| C393 | §3.3 | Income is not a slow quantity. | ENGINE | derivation | C394, C395, C396, C397 |
| C394 | §3.3 | Autonomy drift is monthly. | ENGINE | UNSOURCED | — |
| C395 | §3.3 | Occupation halves goods produced for the duration of a war. | ENGINE | UNSOURCED | — |
| C396 | §3.3 | Devastation and sieges bite within months. | ENGINE | UNSOURCED | — |
| C397 | §3.3 | Ming's mandate swings enormously over years. | ENGINE | UNSOURCED | — |
| C398 | §3.3 | The resulting volatility is deliberate. | DESIGN | stipulated | C392 |
| C399 | §3.3 | A besieged province genuinely buys less, so the volatility is economics rather than noise. | DESIGN | stipulated | C396 |
| C400 | §3.3 | A trade map that ignored a decade-long war would fail Goal 1. | DESIGN | derivation | C353 |
| C401 | §3.3 | The resulting map is legible though not unchanging. | OUTCOME | UNSOURCED | C398 |
| C402 | §3.3 | Trade income is excluded from `wealth` for circularity, not speed. | DESIGN | stipulated | C039 |
| C403 | §3.3 | Including trade income would close a demand → orientation → flow → demand loop. | MODEL | derivation | C032, C039 |
| C404 | §3.3 | That loop would make the graph respond to merchants' decisions rather than to the world. | MODEL | derivation | C403 |
| C405 | §3.3 | The loop still closes the long way: trade income funds development, which raises tax and production income. | ENGINE | UNSOURCED | — |
| C406 | §3.3 | Node boundaries are an authoring artifact. | ENGINE | UNSOURCED | — |
| C407 | §3.3 | Some nodes hold forty provinces and some hold four. | ENGINE | file value | — |
| C408 | §3.3 | Raising a node's aggregate wealth to a power rewards node size. | MODEL | derivation | C033 |
| C409 | §3.3 | Under node-level α, luxuries would drain toward whichever node the map authors sliced finest. | MODEL | derivation | C408 |
| C410 | §3.3 | Under node-level α, Nippon would out-consume Paris on province count. | OUTCOME | derivation | C409, C411 |
| C411 | §3.3 | The Nippon node contains more provinces than the Paris node. | ENGINE | file value | — |
| C412 | §3.3 | With the exponent inside the sum, superlinear demand concentrates where individual provinces are rich. | MODEL | derivation | C033 |
| C413 | §3.3 | At α = 1 the per-province and node-aggregate forms coincide exactly. | MODEL | derivation | C033 |
| C414 | §3.3 | That coincidence is what preserves the §1.6 identity. | MODEL | derivation | C063, C413 |

## §3.4 — Why supply is pre-modifier (lines 379–383)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C415 | §3.4 | Production efficiency does not create more of a good; it means the owner extracts more ducats from the same quantity. | ENGINE | UNSOURCED | — |
| C416 | §3.4 | Production efficiency is therefore a fact about purchasing power and belongs in demand. | DESIGN | derivation | C415 |
| C417 | §3.4 | Letting production efficiency into supply would imply a province ships more to the world market because its owner picked Trade ideas. | MODEL | derivation | C023 |
| C418 | §3.4 | That would be incoherent with the model's thesis. | DESIGN | derivation | C419 |
| C419 | §3.4 | The model's thesis is that where a good comes from is what makes its trade its own. | DESIGN | stipulated | — |
| C420 | §3.4 | This is also why the aggregate supply term uses trade value rather than production income. | DESIGN | derivation | C416 |
| C421 | §3.4 | Trade value and production income are different quantities. | ENGINE | UNSOURCED | — |
| C422 | §3.4 | A province's trade value is unaffected by production efficiency or local autonomy. | ENGINE | UNSOURCED | — |
| C423 | §3.4 | Production income is defined by production efficiency and local autonomy. | ENGINE | UNSOURCED | — |
| C424 | §3.4 | Substituting production income would break the `Φ ≡ φ₀` identity on real data. | MODEL | derivation | C063, C422, C423 |
| C425 | §3.4 | That break would have nothing to do with the solver. | MODEL | derivation | C424 |
| C426 | §3.4 | It would cost about a day of debugging a correct pipeline. | OUTCOME | UNSOURCED | C424 |

## §3.5 — Why α is anchored absolutely (lines 385–391)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C427 | §3.5 | Anchoring α at 2 ducats rather than the price median means a good's concentration moves only when its own price moves. | MODEL | derivation | C040, C041 |
| C428 | §3.5 | Under absolute anchoring, `k` is a pure sensitivity knob that does not shift the neutral point. | MODEL | derivation | C040 |
| C429 | §3.5 | Under a median anchor a good could concentrate because an unrelated commodity got expensive. | MODEL | derivation | C040 |
| C430 | §3.5 | That would be noise dressed as economics. | DESIGN | stipulated | C429 |
| C431 | §3.5 | α < 1 is a crash-reachable state, not a starting condition. | OUTCOME | derivation | C432 |
| C432 | §3.5 | At vanilla base prices essentially nothing sits below the 2.0 anchor. | ENGINE | file value | C041 |
| C433 | §3.5 | Grain's base price is near 1.25. | ENGINE | file value | — |
| C434 | §3.5 | Livestock's base price is near 1.00. | ENGINE | file value | — |
| C435 | §3.5 | The sublinear regime is entered mainly when a price event pushes a good beneath the anchor. | OUTCOME | derivation | C432, C046 |
| C436 | §3.5 | Without a sublinear regime, a price crash could only fail to concentrate a market, never actively spread it. | MODEL | derivation | C045 |
| C437 | §3.5 | Whether the sublinear regime engages often enough to earn its keep is an open question. | DESIGN | stipulated | C435 |
| C438 | §3.5 | If it never engages, either `P₀` is set too low or the regime is doing no work. | MODEL | derivation | C437 |
| C439 | §3.5 | α is deliberately mild. | DESIGN | stipulated | — |
| C440 | §3.5 | Production geography is what differentiates goods. | DESIGN | stipulated | C419 |
| C441 | §3.5 | α expresses only how concentrated a market is. | DESIGN | stipulated | C040 |
| C442 | §3.5 | A concentration mechanism strong enough to reshape orientation would let price fight geography for control of the graph. | MODEL | derivation | C439, C440 |

## §3.6 — Why no hysteresis, and why ε (lines 393–399)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C443 | §3.6 | A margin on orientation is a correctness bug, not a tuning knob. | DESIGN | stipulated | C445 |
| C444 | §3.6 | Holding an edge against the current gradient makes the emitted orientation a splice of gradients from fields solved at different times. | MODEL | derivation | C022 |
| C445 | §3.6 | A splice of two acyclic orientations need not be acyclic. | MODEL | numerical test | C444, C446 |
| C446 | §3.6 | With tol = 1e-3 and `φ = {0, 0.0006, 0.0012}`, tolerance-based tie-breaking produced A→B→C→A. | MODEL | numerical test | — |
| C447 | §3.6 | The `00_tradenodes.txt` format cannot represent a cycle. | ENGINE | UNSOURCED | — |
| C448 | §3.6 | The whole design depends on cycles being impossible. | DESIGN | derivation | C447 |
| C449 | §3.6 | Nothing needs to stop orientation churn. | DESIGN | stipulated | C451, C452 |
| C450 | §3.6 | A link that alternates has near-zero Δφ. | MODEL | derivation | C008 |
| C451 | §3.6 | Such a link carries near-nothing in either direction. | OUTCOME | derivation | C450 |
| C452 | §3.6 | Merchant assignments are to links, so they survive flips untouched. | ENGINE | derivation | C076 |
| C453 | §3.6 | ε is required, and is a different thing from hysteresis. | DESIGN | stipulated | C029 |
| C454 | §3.6 | A dead branch is harmonic with zero flux, so `φ` is mathematically constant along it. | MODEL | derivation | C007 |
| C455 | §3.6 | In floating point, `φ` along a dead branch differs by numerical residual. | MODEL | numerical test | C454 |
| C456 | §3.6 | Four mathematically identical solves of one dead branch produced 0.37000000000000000, 0.36999999999999988, and −0.86999999999999988. | MODEL | numerical test | — |
| C457 | §3.6 | In those solves one edge oriented ← twice and → once on Δ of ±1e-16. | MODEL | numerical test | C456 |
| C458 | §3.6 | Exact ties occur in some runs and not others. | MODEL | numerical test | C456 |
| C459 | §3.6 | The tie-break therefore fires unpredictably and orientation varies by machine. | MODEL | derivation | C458 |
| C460 | §3.6 | ε is field-level. | MODEL | stipulated | C029 |
| C461 | §3.6 | Field-level is the only kind of regularizer the model permits. | DESIGN | stipulated | C460 |
| C462 | §3.6 | ε preserves the §1.6 identity exactly. | MODEL | derivation | C029, C063 |

## §3.7 — Why eligibility is per good (lines 401–407)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C463 | §3.7 | Vanilla counts effective trade power only for countries which collect or transfer downstream. | ENGINE | UNSOURCED | — |
| C464 | §3.7 | Vanilla does not count countries whose trade capital is upstream. | ENGINE | UNSOURCED | — |
| C465 | §3.7 | Power in a node not upstream of anywhere you collect is inert — neither retaining nor transferring. | ENGINE | UNSOURCED | C463, C464 |
| C466 | §3.7 | Under a per-good model, "downstream" is itself per good. | MODEL | derivation | C005 |
| C467 | §3.7 | At a node where your home is downstream for cloth and upstream for spice, your power counts for one and not the other. | MODEL | derivation | C089, C466 |
| C468 | §3.7 | Per-good eligibility returns true for some goods at every node, so no nation is ever globally inert. | OUTCOME | derivation | C089 |
| C469 | §3.7 | Per-good eligibility still prevents a nation's power from shoving a good away from where it collects that good. | MODEL | derivation | C089 |
| C470 | §3.7 | Forcing eligibility true for all goods at once would amount to "direction doesn't exist". | MODEL | derivation | C089 |
| C471 | §3.7 | That would inflate transfer power everywhere. | OUTCOME | derivation | C470 |
| C472 | §3.7 | The claim that any non-collecting country with trade power is transferring is the loose community summary. | ENGINE | prose source | — |
| C473 | §3.7 | That community claim is wrong. | ENGINE | derivation | C463, C464, C465 |

## §3.8 — Why gates evaluate true (lines 409–417)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C474 | §3.8 | The vanilla gates encode an assumption that a nation pair has one global relationship to trade. | ENGINE | UNSOURCED | — |
| C475 | §3.8 | Under thirty graphs that assumption is false, not merely inconvenient. | MODEL | derivation | C005, C159 |
| C476 | §3.8 | Every province is upstream for some good. | OUTCOME | derivation | C005 |
| C477 | §3.8 | A region that receives your cloth ships you its furs. | WORLD | UNSOURCED | — |
| C478 | §3.8 | There is no fact of the matter for the nation-pair gate to test. | MODEL | derivation | C475, C476 |
| C479 | §3.8 | The honest fix is to stop consulting the gate rather than engineer the graph so it passes. | DESIGN | derivation | C478 |
| C480 | §3.8 | Node-pair dependencies are different from nation-pair gates and keep reading `Φ`. | DESIGN | stipulated | C113 |
| C481 | §3.8 | Propagation is a relation between two nodes, not two nations. | ENGINE | derivation | C104 |
| C482 | §3.8 | Setting propagation's direction test true would grant every country propagated power into every neighbour. | ENGINE | derivation | C104 |
| C483 | §3.8 | That would multiply trade power across the map. | OUTCOME | derivation | C482 |
| C484 | §3.8 | The node/nation distinction is easy to miss and expensive to get wrong. | DESIGN | stipulated | C480 |
| C485 | §3.8 | Propagate Religion is node-local: it establishes a centre of conversion in the node's own province. | ENGINE | verified (method unstated) | — |
| C486 | §3.8 | Propagate Religion is gated on a trade-power threshold in that node and nothing else. | ENGINE | verified (method unstated) | C485 |
| C487 | §3.8 | The whole trade-policy family behaves the same way. | ENGINE | verified (method unstated) | C486 |
| C488 | §3.8 | A trade policy can be set in any node where the country meets the threshold, with no direction test anywhere. | ENGINE | derivation | C486, C487 |
| C489 | §3.8 | This is recorded now because the deferred call-site artifact does not exist yet. | DESIGN | stipulated | C350 |
| C490 | §3.8 | A community restatement of the "downstream target" claim would otherwise reintroduce these as gates. | OUTCOME | prose source | C472 |
| C491 | §3.8 | A gate is a boolean while a scope is a set or a path. | MODEL | stipulated | C114 |
| C492 | §3.8 | Answering a scope question with any-good reachability would be an enormous buff. | MODEL | derivation | C476, C491 |
| C493 | §3.8 | `Φ` is the graph the engine already walks. | ENGINE | derivation | C062 |
| C494 | §3.8 | Therefore the scope call sites are left alone. | DESIGN | derivation | C493 |
| C495 | §3.8 | Leaving them alone collapses the shared-predicate risk. | DESIGN | derivation | C494 |
| C496 | §3.8 | Scoping by `Φ` is legible: one map predicts where fleets sail. | DESIGN | stipulated | C114 |
| C497 | §3.8 | Scoping by `Φ` is balanced. | DESIGN | stipulated | C492 |
| C498 | §3.8 | Area-effect mechanics scoped by any-good reachability would cover a large fraction of the world. | OUTCOME | derivation | C492 |

## §3.9 — Why `Φ` is the installed graph (lines 419–425)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C499 | §3.9 | `Φ` is a legal DAG because it is itself a potential. | MODEL | derivation | C061 |
| C500 | §3.9 | `Φ` is the value-weighted aggregate of the real economy rather than an invented baseline. | MODEL | derivation | C060 |
| C501 | §3.9 | Once the displayed numbers are the model's numbers, the installed graph must be the one the economy actually runs. | DESIGN | derivation | C149 |
| C502 | §3.9 | `ΔΦ` is not the net value crossing an edge. | MODEL | derivation | C506, C507 |
| C503 | §3.9 | The earlier claim that `ΔΦ` is net value was an error. | MODEL | derivation | C502 |
| C504 | §3.9 | `ΔΦ = Σ_g V_g Δφ_g` is the analytic figure. | MODEL | derivation | C060 |
| C505 | §3.9 | Realized movement follows vanilla propagation rules instead. | ENGINE | derivation | C091 |
| C506 | §3.9 | A good with large Δφ can be diluted by an even split across three links. | MODEL | derivation | C097 |
| C507 | §3.9 | A good with small Δφ can be winner-take-all steered the other way. | MODEL | derivation | C095 |
| C508 | §3.9 | A link can therefore be oriented `n → m` under `Φ` while realized net flow runs `m → n`. | MODEL | derivation | C506, C507 |
| C509 | §3.9 | That is why the disagreement rate is measured rather than assumed. | DESIGN | derivation | C508 |
| C510 | §3.9 | And why the negative-link display policy is deferred to data. | DESIGN | derivation | C508 |
| C511 | §3.9 | The analytic `flow_g = V_g · Δ` has no consumer in the design. | DESIGN | derivation | C502 |
| C512 | §3.9 | Link values are realized flows, which makes conservation hold by construction. | MODEL | derivation | C257 |

## §3.10 — Why the engine's economy is overwritten (lines 427–442)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C513 | §3.10 | Paying countries correctly while leaving the display wrong is a strictly weaker position. | DESIGN | stipulated | C514 |
| C514 | §3.10 | With a wrong display, node values, pie charts and the ledger would describe an economy nobody is playing. | OUTCOME | derivation | C150 |
| C515 | §3.10 | AI light-ship building reads those figures. | ENGINE | UNSOURCED | — |
| C516 | §3.10 | AI trade-league behaviour reads those figures. | ENGINE | UNSOURCED | — |
| C517 | §3.10 | AI peace valuation reads those figures. | ENGINE | UNSOURCED | — |
| C518 | §3.10 | Income-threshold events read those figures. | ENGINE | UNSOURCED | — |
| C519 | §3.10 | The engine's data model is sufficient at node level. | MODEL | derivation | C521, C523 |
| C520 | §3.10 | `collect_pool` is per good on the inside because `collected_share` depends on `P_transfer(g)`. | MODEL | derivation | C087, C088 |
| C521 | §3.10 | `income_C(n) = Σ_g value_g(n)·collected_share(n,g)·powershare_C(n) = powershare_C(n)·collect_pool(n)`. | MODEL | derivation | C264 |
| C522 | §3.10 | Verified numerically to 5.7e-14 across a node with mixed sinks, mixed collectors and the home-node penalty in play. | MODEL | numerical test | C521 |
| C523 | §3.10 | One scalar per node reproduces every country's income exactly. | MODEL | derivation | C521, C522 |
| C524 | §3.10 | The engine's own math does the rest. | ENGINE | derivation | C523 |
| C525 | §3.10 | This is also why propagation cannot be made per good. | MODEL | derivation | C527, C528 |
| C526 | §3.10 | With propagation reading `Φ`, the node-scalar model reproduces per-good truth to 1.4e-14. | MODEL | numerical test | C111 |
| C527 | §3.10 | With power varying by good, the node-scalar model is off by 5.96 ducats on a node paying about 250. | MODEL | numerical test | — |
| C528 | §3.10 | The cause is that `powershare_C` stops factoring out. | MODEL | derivation | C527 |
| C529 | §3.10 | Keeping propagation on a single graph is load-bearing for Goal 7, not merely convenient. | DESIGN | derivation | C365, C525 |
| C530 | §3.10 | Only the decomposition by good exceeds what the engine can hold. | MODEL | derivation | C523 |

## §3.11 — Why caravan power needs a condition added (lines 444–450)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C531 | §3.11 | In vanilla, steering is outgoing-only. | ENGINE | UNSOURCED | — |
| C532 | §3.11 | The vanilla node map shows only the paths leaving a node. | ENGINE | UNSOURCED | C531 |
| C533 | §3.11 | In vanilla, trade cannot be steered upstream at any amount of power. | ENGINE | UNSOURCED | C531 |
| C534 | §3.11 | So in vanilla "assigned" and "steering" are the same condition. | ENGINE | derivation | C531, C533 |
| C535 | §3.11 | The engine therefore never had to distinguish them. | ENGINE | derivation | C534 |
| C536 | §3.11 | §1.7's widening to incident links pulls "assigned" and "steering" apart. | MODEL | derivation | C073 |
| C537 | §3.11 | Caravan power fires on a merchant plus an inland link end, with nothing checking whether value moves. | ENGINE | UNSOURCED | — |
| C538 | §3.11 | Steering from Crimea to Kiev grants the caravan bonus in Crimea. | ENGINE | UNSOURCED | C537 |
| C539 | §3.11 | Without an added condition, a merchant assigned to an incoming link and inert for every good would earn a major power the full caravan bonus. | OUTCOME | derivation | C075, C537 |
| C540 | §3.11 | That would apply at any node adjacent to one of the inland nodes. | OUTCOME | derivation | C539, C541 |
| C541 | §3.11 | There are roughly 26 inland nodes. | ENGINE | file value | — |
| C542 | §3.11 | Caravan power equals total country development ÷ 3, capped at 50. | ENGINE | file value | C219 |
| C543 | §3.11 | Every major power is at the caravan cap from 1444. | ENGINE | derivation | C542 |
| C544 | §3.11 | Caravan power does not scale with node presence at all. | ENGINE | derivation | C542 |
| C545 | §3.11 | Requiring the merchant to steer something restores the vanilla state of affairs. | DESIGN | derivation | C534 |
| C546 | §3.11 | Granting caravan power on bare assignment would be the deviation. | DESIGN | derivation | C545 |
| C547 | §3.11 | That deviation would be an unintended one. | DESIGN | derivation | C546 |

## §3.12 — Why treasure fleets are always granted (lines 452–458)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C548 | §3.12 | Consistency with §3.8 is the weaker argument for always granting treasure fleets. | DESIGN | stipulated | C112, C144 |
| C549 | §3.12 | The treasure-fleet gate is bistable. | MODEL | derivation | C551, C552 |
| C550 | §3.12 | Denial is not neutral: the colonial nation keeps the gold and any income gained from it. | ENGINE | UNSOURCED | — |
| C551 | §3.12 | Under denial the colonial node's wealth rises, making it more sink-like and keeping it denied. | MODEL | derivation | C032, C550 |
| C552 | §3.12 | Under granting the income is diverted, lowering the node's wealth, making it more source-like and keeping it granted. | MODEL | derivation | C032, C148 |
| C553 | §3.12 | Both states self-reinforce. | MODEL | derivation | C551, C552 |
| C554 | §3.12 | Two otherwise identical campaigns would diverge permanently on whichever state they started in. | OUTCOME | derivation | C553 |
| C555 | §3.12 | Granting removes a bifurcation, not just a lock-in. | MODEL | derivation | C554 |
| C556 | §3.12 | Inflation scales with money received relative to economy size. | ENGINE | UNSOURCED | — |
| C557 | §3.12 | Universal granting hits small previously-cut-off colonizers hardest. | OUTCOME | derivation | C556 |
| C558 | §3.12 | The route rule is a balance dial because privateers skim per node passed. | MODEL | derivation | C146 |
| C559 | §3.12 | Hop counts must be compared between candidate rules on the mod's own graph. | DESIGN | derivation | C560 |
| C560 | §3.12 | Comparing hop counts against vanilla's graph would be a counterfactual on a graph the mod has replaced. | DESIGN | derivation | C062 |

## §3.13 — Open questions (lines 460–478)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C561 | §3.13 | Prose-sourced premises are to be distrusted, and nothing is to be built on them. | DESIGN | stipulated | C674 |
| C562 | §3.13 | The evidence for a colonization trade-direction gate is one mod author's report. | ENGINE | prose source | — |
| C563 | §3.13 | That report is contradicted in-thread. | WORLD | prose source | C562 |
| C564 | §3.13 | The observed colonization behaviour needs no gate at all to explain it. | ENGINE | derivation | C565 |
| C565 | §3.13 | If colonial nodes route away from the AI's home, expected trade income collapses and low-scoring provinces are not colonized. | OUTCOME | derivation | C089 |
| C566 | §3.13 | The caller enumeration must be able to return "no colonization gate exists" as a successful result. | DESIGN | stipulated | C289 |
| C567 | §3.13 | The `TRADE_PROPAGATE_THRESHOLD` file value and the documented raw requirement differ by exactly the propagation divider. | ENGINE | file value + prose source | C105, C213 |
| C568 | §3.13 | That discrepancy reconciles if the threshold is expressed in propagated units. | ENGINE | derivation | C567 |
| C569 | §3.13 | Doubling the define would falsify the propagated-units reading. | ENGINE | derivation | C568 |
| C570 | §3.13 | Pass 2's ordering requirement comes from something other than propagation. | ENGINE | derivation | C109 |
| C571 | §3.13 | Eligibility resolution is a backward reachability from collection points. | MODEL | derivation | C089 |
| C572 | §3.13 | Eligibility resolution is the only named candidate for pass 2's ordering. | ENGINE | derivation | C571 |
| C573 | §3.13 | That is an argument from exhaustion. | DESIGN | stipulated | C572 |
| C574 | §3.13 | The project's inventory of engine mechanisms has been wrong before. | WORLD | UNSOURCED | — |
| C575 | §3.13 | §2.7 probe 2 settles pass 2's ordering. | DESIGN | stipulated | C277 |
| C576 | §3.13 | Everything in §2.7 is debugger-only. | DESIGN | stipulated | C273 |
| C577 | §3.13 | Pass caching and income accumulation timing are the principal debugger-only unknowns. | DESIGN | stipulated | C274, C278 |
| C578 | §3.13 | `k`, `α_min` and `α_max` are unresolved parameters. | DESIGN | stipulated | C040 |
| C579 | §3.13 | The test for them is whether they produce the intended three-regime split. | DESIGN | stipulated | C042, C044, C045 |
| C580 | §3.13 | They are not meant to differentiate same-geography goods. | DESIGN | stipulated | C440 |
| C581 | §3.13 | Whether `α_min` ever bites is unknown. | DESIGN | stipulated | C437 |
| C582 | §3.13 | The sublinear regime may be reachable only through price crashes. | OUTCOME | derivation | C432 |
| C583 | §3.13 | If it never engages in a full campaign, `P₀` is mis-set or the regime is inert. | MODEL | derivation | C438 |
| C584 | §3.13 | ε must be small enough to be invisible against any real economy and large enough to decide dead branches against floating-point noise. | DESIGN | derivation | C455 |
| C585 | §3.13 | AI merchant reassignment cadence is unresolved. | DESIGN | stipulated | — |

## §3.14 — AI merchant assignment (lines 480–497)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C586 | §3.14 | The two ends of a link never compete for goods. | MODEL | derivation | C074, C075 |
| C587 | §3.14 | Competition stays between merchants at the same node, as in vanilla. | ENGINE | derivation | C068, C586 |
| C588 | §3.14 | One survival-table precompute serves every country. | MODEL | derivation | C591 |
| C589 | §3.14 | For each good, a backward pass over its DAG gives `S_g[n][H]`, the expected fraction of a unit of `g` at `n` arriving at `H`. | MODEL | stipulated | C009 |
| C590 | §3.14 | The backward pass multiplies through collection, steering shares, and the per-link multi-merchant boost. | MODEL | stipulated | C589 |
| C591 | §3.14 | All three of those inputs are country-independent aggregates. | MODEL | derivation | C590 |
| C592 | §3.14 | Vanilla has a per-link multi-merchant boost. | ENGINE | file value | C218 |
| C593 | §3.14 | `collected_share(n,g)` reaches 1 at `g`'s sink, which terminates the recursion. | MODEL | derivation | C086 |
| C594 | §3.14 | The survival table is about 0.75 MB. | MODEL | derivation | C159, C199 |
| C595 | §3.14 | Building it costs well under a million operations per solve. | MODEL | derivation | C594 |
| C596 | §3.14 | Scoring reads the survival table for both steering and collecting. | DESIGN | stipulated | C589 |
| C597 | §3.14 | The opportunity cost of collecting therefore falls out as the same comparison a human player makes by hand. | MODEL | derivation | C596 |
| C598 | §3.14 | Denial scoring falls out of the same table evaluated against a rival's home node. | MODEL | derivation | C589 |
| C599 | §3.14 | The off-home penalty is a power modifier, not a haircut on value. | ENGINE | UNSOURCED | C072 |
| C600 | §3.14 | It reduces the country's trade power in that node. | ENGINE | derivation | C599 |
| C601 | §3.14 | The reduced power feeds both the collect/transfer ratio and the share among collectors. | ENGINE | derivation | C087, C600 |
| C602 | §3.14 | So it lowers both the fraction retained in the node and the collector's slice of it. | ENGINE | derivation | C601 |
| C603 | §3.14 | Scoring a collect candidate as `value × share × 0.5` is wrong. | MODEL | derivation | C602 |
| C604 | §3.14 | The halving must be applied to power, with the two-stage formula run from there. | MODEL | derivation | C603 |
| C605 | §3.14 | This is why the off-home penalty falls out of the survival table: the table is built from power-derived shares. | MODEL | derivation | C590 |
| C606 | §3.14 | The home-node bonus is voided entirely by placing any collector outside the home node. | ENGINE | UNSOURCED | C216 |
| C607 | §3.14 | So a collect candidate's true cost includes a penalty no single-merchant score can see. | MODEL | derivation | C606 |
| C608 | §3.14 | Running greedy twice — once all-steer with the bonus, once unconstrained without — and keeping the better portfolio handles that. | DESIGN | derivation | C607 |
| C609 | §3.14 | Greedy scoring against a moving field can oscillate between AIs. | MODEL | UNSOURCED | — |
| C610 | §3.14 | Damping the shares between passes should hold the oscillation. | OUTCOME | UNSOURCED | C609 |
| C611 | §3.14 | The prototype must verify the damping. | DESIGN | stipulated | C610 |
| C612 | §3.14 | Reassignment cadence is the one item left for the human to decide. | DESIGN | stipulated | C585 |
| C613 | §3.14 | Merchants take travel time. | ENGINE | UNSOURCED | — |
| C614 | §3.14 | An AI re-optimizing every solve would leave its merchants permanently in transit. | OUTCOME | derivation | C019, C613 |
| C615 | §3.14 | Mirroring vanilla's cadence is the stated preference. | DESIGN | stipulated | — |
| C616 | §3.14 | The define governing vanilla's cadence was not located in the visible portion of any dump. | ENGINE | file value | — |
| C617 | §3.14 | Mirroring therefore requires finding that define or measuring the cadence by observation. | DESIGN | derivation | C616 |
| C618 | §3.14 | The computed alternative moves a merchant when `(V_new − V_incumbent) × expected_tenure > V_incumbent × travel_time`. | DESIGN | stipulated | — |
| C619 | §3.14 | `MERCHANT_SPEED` exists as a define. | ENGINE | file value | — |
| C620 | §3.14 | `expected_tenure` is endogenous and should be wired to the flip-rate measurement. | DESIGN | stipulated | C618, C334 |
| C621 | §3.14 | Vanilla's cadence was tuned against a graph that never moves. | ENGINE | derivation | C531 |
| C622 | §3.14 | Copying it would import a constant fitted to different dynamics. | MODEL | derivation | C621 |
| C623 | §3.14 | Computing the cadence overrides a stated preference. | DESIGN | derivation | C615 |
| C624 | §3.14 | Node-to-node travel time still needs the game's distance metric. | ENGINE | UNSOURCED | C618 |

## §3.15 — Rejected (lines 499–539)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C625 | §3.15 | Authored demand weights are rejected. | DESIGN | stipulated | — |
| C626 | §3.15 | They would be authored data in a model that needs none. | DESIGN | derivation | C364 |
| C627 | §3.15 | Trade income inside `wealth` is rejected. | DESIGN | stipulated | C402 |
| C628 | §3.15 | It would reintroduce flow → demand → orientation → flow circularity. | MODEL | derivation | C403 |
| C629 | §3.15 | The graph would then respond to merchants rather than to the world. | MODEL | derivation | C404 |
| C630 | §3.15 | Node-level α is rejected. | DESIGN | stipulated | — |
| C631 | §3.15 | It would make demand concentration a function of how finely the map was sliced. | MODEL | derivation | C409 |
| C632 | §3.15 | A median-relative α anchor is rejected. | DESIGN | stipulated | — |
| C633 | §3.15 | Under it, a good's concentration would shift because other goods changed price. | MODEL | derivation | C429 |
| C634 | §3.15 | α floored at 1 is rejected. | DESIGN | stipulated | — |
| C635 | §3.15 | Flooring at 1 would discard the cheap-bulk regime. | MODEL | derivation | C045, C436 |
| C636 | §3.15 | Production income as the aggregate supply term is rejected. | DESIGN | stipulated | C420 |
| C637 | §3.15 | It would make world supply depend on owners' idea groups. | MODEL | derivation | C417 |
| C638 | §3.15 | It would break the `Φ ≡ φ₀` identity for reasons unrelated to the solver. | MODEL | derivation | C424 |
| C639 | §3.15 | A τ margin on orientation is rejected. | DESIGN | stipulated | C443 |
| C640 | §3.15 | A τ margin manufactures cycles. | MODEL | derivation | C446 |
| C641 | §3.15 | Uniform supply in the aggregate solve is rejected. | DESIGN | stipulated | — |
| C642 | §3.15 | It answers a question nobody asked. | DESIGN | stipulated | C641 |
| C643 | §3.15 | It destroys the identity that makes `φ₀` worth computing. | MODEL | derivation | C063 |
| C644 | §3.15 | `φ₀` as the installed graph is rejected. | DESIGN | stipulated | — |
| C645 | §3.15 | `φ₀` is not the economy the model runs. | MODEL | derivation | C064, C501 |
| C646 | §3.15 | A vestigial in-game economy with net treasury settlement is rejected. | DESIGN | stipulated | — |
| C647 | §3.15 | It would give correct treasuries but wrong displays and wrong AI inputs. | OUTCOME | derivation | C514 |
| C648 | §3.15 | Per-good propagation is rejected. | DESIGN | stipulated | C525 |
| C649 | §3.15 | It breaks the income factoring and with it Goal 7. | MODEL | derivation | C365, C527 |
| C650 | §3.15 | Node-level collect/transfer rules are rejected. | DESIGN | stipulated | — |
| C651 | §3.15 | The collect/transfer split is per good because whether a good has anywhere to go is per good. | MODEL | derivation | C086, C088 |
| C652 | §3.15 | Treating unsteered goods as fully collected is rejected. | DESIGN | stipulated | — |
| C653 | §3.15 | Transfer power does not come from merchants. | ENGINE | derivation | C089 |
| C654 | §3.15 | Full collection happens at a sink, which is a property of the graph. | MODEL | derivation | C086 |
| C655 | §3.15 | Undirected shortest path as the primary fleet route is rejected. | DESIGN | stipulated | C117 |
| C656 | §3.15 | A geodesic over a directional structure can route a fleet against every arrow on the map. | MODEL | derivation | C655 |
| C657 | §3.15 | Automatic per-good merchant targeting is rejected. | DESIGN | stipulated | — |
| C658 | §3.15 | One vanilla arrow click already achieves per-good resolution. | ENGINE | derivation | C074 |
| C659 | §3.15 | Automation would cost denial steering. | OUTCOME | UNSOURCED | C598 |
| C660 | §3.15 | Companion-overlay merchant assignment is rejected. | DESIGN | stipulated | — |
| C661 | §3.15 | Assignment must stay a game action or vanilla knowledge stops transferring. | DESIGN | stipulated | C067 |
| C662 | §3.15 | Emission-time pruning of near-flat links is rejected. | DESIGN | stipulated | — |
| C663 | §3.15 | Peripheral termini are intended consumption. | DESIGN | stipulated | C383 |
| C664 | §3.15 | The power-at-both-ends gate already withholds unworked corridors. | ENGINE | derivation | C102 |
| C665 | §3.15 | Edge conductance / a weighted Laplacian is rejected. | DESIGN | stipulated | — |
| C666 | §3.15 | A weighted Laplacian would add too much mechanical surface. | DESIGN | stipulated | C665 |
| C667 | §3.15 | The unweighted solve already routes correctly through conduits. | MODEL | derivation | C378 |
| C668 | §3.15 | Staged delivery is rejected. | DESIGN | stipulated | — |
| C669 | §3.15 | The intermediate states are different designs sharing a solver, not subsets of this one. | DESIGN | stipulated | C668 |
| C670 | §3.15 | The claim "the aggregate map is not a DAG" was an error. | MODEL | derivation | C061 |
| C671 | §3.15 | Net flow is the gradient of `Φ` and hence acyclic. | MODEL | derivation | C060 |
| C672 | §3.15 | That acyclicity is what makes an installable single network exist at all. | MODEL | derivation | C062, C671 |

## §3.16 — Evidence standard (lines 541–547)

| ID | § | Statement | Type | Provenance | Depends on |
|---|---|---|---|---|---|
| C673 | §3.16 | The spec was reviewed adversarially over many rounds by two reviewers. | WORLD | UNSOURCED | — |
| C674 | §3.16 | Every retraction on either side traced to a premise that entered through prose. | WORLD | UNSOURCED | C673 |
| C675 | §3.16 | Those prose premises included a community post, a wiki sentence read under the wrong heading, semantics inferred from a define name, and a forum thread title. | WORLD | UNSOURCED | C674 |
| C676 | §3.16 | Nothing built on adjacency data, file values, or the model's own equations failed. | WORLD | UNSOURCED | C674 |
| C677 | §3.16 | The rule is not that derivations are safe. | DESIGN | stipulated | C678 |
| C678 | §3.16 | Two retracted claims were sound derivations resting on false premises about the map. | WORLD | UNSOURCED | C674 |
| C679 | §3.16 | The standard is: trust the inference, audit the inputs, and treat any prose-sourced premise as provisional however much reasoning sits on top of it. | DESIGN | stipulated | C674, C678 |
| C680 | §3.16 | The cautionary case is the propagation source condition. | WORLD | UNSOURCED | C104 |
| C681 | §3.16 | Both reviewers signed off on it as correct while defending it against the wrong error. | WORLD | UNSOURCED | C680 |
| C682 | §3.16 | It was corrected only later to include ship propagation under its modifier. | WORLD | UNSOURCED | C107 |
| C683 | §3.16 | §1.9 carries the corrected version. | DESIGN | stipulated | C107 |
| C684 | §3.16 | Agreement between two reviewers is not verification. | DESIGN | stipulated | C681 |
| C685 | §3.16 | A line can be confidently defended against one mistake while carrying another. | DESIGN | stipulated | C681 |
