# Claim Inventory Delta — Per-Good Trade Network Spec v2.0

Extracted from `per-good-trade-spec.md` (v2.0, DRAIN) as a **delta against
`../v1-laplacian/claims.md`** (v1.3, C001–C685). Extraction only: nothing here is validated,
corrected, or commented on. Only the two files were read.

**A v2.1 addendum (V212–V230) is appended at the end of this file** — the installed aggregate
changed from `Φ_ord` to `Φ_w` (spec v2.1, §1.6/§3.9); the v2.0 body above is unmodified history.

**Statuses.** Each claim in the v2 spec is one of:

- **UNCHANGED** — same proposition as an existing claims.md ID. The ID is recorded and not
  re-extracted (statement, type, provenance and dependencies stand as filed in claims.md).
- **REVISED** — the proposition changed. New `V` ID; the `Replaces` column names the old ID(s).
- **NEW** — no counterpart in claims.md.

**Conventions carried over from claims.md:** the Type vocabulary (ENGINE / MODEL / DESIGN /
OUTCOME, plus WORLD) and the Provenance vocabulary (stipulated / derivation / file value /
numerical test / engine test / prose source / verified (method unstated) / UNSOURCED). As in v1,
no claim is sourced to `engine test`. The global renaming `Φ → Φ_ord` and `L φ = s − c → DRAIN`
in claims that merely *reference* the aggregate or the per-good graphs is treated as UNCHANGED;
only claims about the operator or aggregate *themselves* are REVISED. A proposition stated in two
sections keeps one ID at first appearance.

**⚑ marks a new engine fact introduced by an audit fix** — the class that failed last time.

**Full-strength sections** (extracted row-by-row regardless of overlap, UNCHANGED rows included):
§1.1 (each of the five properties and each phase separately), §3.2, §3.6, §3.9, and the §3.15
rejections that changed with the operator.

## Summary

**211 delta claims extracted, V001–V211**, against 685 v1 claims: **140 NEW, 71 REVISED**
(replacing 105 claims.md IDs), **543 claims.md IDs UNCHANGED**, and **37 claims.md IDs orphaned**
(543 + 105 + 37 = 685).

### Delta claims by Type

| Type | NEW | REVISED | Total |
|---|---|---|---|
| MODEL | 65 | 24 | 89 |
| ENGINE | 37 | 22 | 59 |
| DESIGN | 25 | 22 | 47 |
| WORLD | 12 | 1 | 13 |
| OUTCOME | 1 | 2 | 3 |
| **Total** | **140** | **71** | **211** |

### Delta claims by Provenance

| Provenance | Count |
|---|---|
| derivation | 71 |
| stipulated | 48 |
| file value | 47 |
| numerical test | 35 |
| UNSOURCED | 10 |
| **Total** | **211** |

### UNSOURCED delta claims (10)

By v2's own §3.16 rule, each of these is a to-do, not a fact:

| ID | Claim |
|---|---|
| V001 | EU4's final patch is 1.37.5 ("Inca") |
| V043 | the 75% overseas rule is pre-Common-Sense |
| V054 | whether the per-province production-income field carries gold (open, §2.7 item 12) |
| V067 | whether `NextNodeButton` already accepts an assignment (open, §2.7 item 14) |
| V071 | trade range gates merchant placement, not value flow |
| V072 | there is no trade "supply range" in the engine |
| V084 | ironman saves are binary-encoded |
| V096 | whether the engine requires topological declaration order (open, §2.7 item 13) |
| V105 | whether power appears upstream where the country holds none (open, §2.7 item 15) |
| V149 | the engine's behaviour on a cyclic node file (open, §2.7 item 13) |

Five of the ten are §2.7 probe unknowns filed as claims, per v1 convention. V071 and V072 are
⚑-flagged fixes that arrived *without* a recorded source.

### ⚑ New engine facts introduced by fixes (47)

- **Autonomy floors & static modifiers:** V038, V042, V043, V044, V045, V046, V047
- **Gold fields and constants:** V050, V051, V052 (`INCOMEGOLD`, `gold_income`, `GOLD_MINE_SIZE`, `base_price = 0` / `goldtype`)
- **Coal trigger:** V055, V056, V057 (Enlightenment default, per-province conditions, 58 provinces)
- **Caravan power:** V068, V069, V163, V164, V167, V168 (grant identifiers, inland-node tooltip reading, formula with modifiers and [2, 50] clamp, nineteen-at-cap)
- **Thresholds & policies:** V074, V075 (Improve Inland Routes 50/40 + merchant + waiver; Propagate Religion 50/50 ladder), V155, V157, V158 (`00_trading_policies.txt` gates, no direction test, three-of-five thresholdless)
- **Range gates:** V071, V072 (placement-not-flow; no supply range)
- **Scripted content:** V078, V079 (zero node-name references; structural accessors only)
- **UI structures:** V066, V081 (incoming/outgoing listboxes in `tradeinterface.gui`; node-level value fields, none per-good)
- **Binary strings:** V073 ("where it already has power"), V082, V083 (achievements define, ironman load path), V098, V099, V100 (three direction call-site strings, trade-capital comparison, no colonisation string), V171 (denial branch string)
- **Prices & events:** V140, V141, V142, V145, V146 (2.0 minimum, six goods on the anchor, grain 2.5, 13-of-30 crashable, 11 with no negative event)
- **Map/file facts:** V092 (`siberia` inland-flag contradiction), V095 (vanilla file topologically sorted, 0/159), V132, V135 (node sizes 19–77; Nippon 68 / `champagne` 33), V148 (the format represents cycles)

### Orphaned claims.md IDs (37)

Spec text gone, no REVISED replacement (detail in the final section):

C013, C014, C015, C016, C017, C018, C024, C034, C064, C065, C066, C321, C369, C376, C379,
C380, C381, C414, C425, C426, C438, C454, C456, C457, C458, C460, C461, C462, C503, C504,
C511, C583, C673, C674, C675, C676, C678

---
## §0 — Front matter (lines 1–14)

**UNCHANGED:** C001, C002, C003, C004

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V001 | NEW | EU4's final patch is 1.37.5 ("Inca"). | ENGINE | UNSOURCED | — | — |
| V002 | NEW | v1's sink placement was topological rather than economic (diagnosed in `../v1-laplacian/diagnosis.md`). | MODEL | numerical test | — | — |
| V003 | NEW | The orientation core was replaced by DRAIN after a four-operator bake-off. | WORLD | stipulated | — | V002 |
| V004 | NEW | Every claim-audit correction from `validation.md` settleable from files is folded into v2. | WORLD | stipulated | — | — |

## §1.1 — Trade direction (lines 18–74) — full-strength extraction

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| C005 | UNCHANGED | Every trade good has its own directed network over the same node adjacency. | MODEL | stipulated | — | — |
| C006 | UNCHANGED | Direction is computed from state and never authored. | MODEL | stipulated | — | C005 |
| V005 | NEW | For each good `g` the balance is `b_g(n) = s_g(n) − c_g(n)`. | MODEL | stipulated | — | C023, C033 |
| V006 | REVISED | Orientation per good is by DRAIN — peel, select, route, sweep. | MODEL | stipulated | C007, C008 | V005 |
| V007 | NEW | Phase 0 repeatedly removes degree-1 nodes down to the 2-core, orienting each pendant edge by the sign of its absorbed subtree balance (net exporter → toward core; net importer → fed from core; zero → toward core) and folding the residual into the parent. | MODEL | stipulated | — | V006 |
| V008 | NEW | Phase 0 is exact, not heuristic: every removed edge is a bridge, and flow on a tree is determined by conservation. | MODEL | derivation | — | V007 |
| V009 | NEW | On the vanilla map Phase 0 is a no-op — minimum degree 2, zero bridges. | ENGINE | file value | — | — |
| V010 | NEW | Phase 0 exists for modded maps. | DESIGN | stipulated | — | V009 |
| V011 | NEW | Phase 1 takes the connected clusters of net demanders in the core, computes the Herfindahl index of their demand masses, sets `k = clamp(round(1/HHI), 1, n_clusters)`, and selects the heaviest demander of each of the top-k clusters. | MODEL | stipulated | — | V005 |
| V012 | NEW | Phase 1's knobs are a demand-mass quantile `ρ` (default 1.0) and a cluster dilation radius `r` (default 0). | DESIGN | stipulated | — | V011 |
| V013 | NEW | On vanilla 1444, demand is so ubiquitous that k = 1 for 27 of 29 goods at defaults. | MODEL | numerical test | — | V011 |
| V014 | NEW | Selection is deliberately weak because Phase 3 self-corrects upward. | DESIGN | stipulated | — | V011, V022 |
| V015 | NEW | Phase 2 solves the uncapacitated min-cost flow with unit arc costs serving `b_g` and orients every support edge by its net flow. | MODEL | stipulated | — | V005 |
| V016 | NEW | The flow support is a spanning-tree basis of ≤ N−1 edges. | MODEL | derivation | — | V015 |
| V017 | NEW | The support is acyclic by theorem: with all costs 1, any directed cycle could be cancelled for strictly lower cost. | MODEL | derivation | — | V015 |
| V018 | NEW | Edges with zero net flow are free and deferred to Phase 3. | MODEL | stipulated | — | V015 |
| V019 | NEW | Phase 3 marks nodes Kahn-style: a node is ready when every flow out-neighbour is already marked and it is a selected sink, has a flow out-arc, or has a free edge to a marked node. | MODEL | stipulated | — | V015, V018 |
| V020 | NEW | Ready nodes pop by the deterministic priority key (DEF ascending, b ascending, index), where `DEF(v)` is total downstream demand on the flow-arc subgraph. | MODEL | stipulated | — | V019 |
| V021 | NEW | The flow-arc subgraph is acyclic and fixed before any free edge, so DEF has no circularity. | MODEL | derivation | — | V017, V020 |
| V022 | NEW | On a stall, the heaviest flow-terminal demander is promoted into the sink set — the self-correction that supplies the real sink count. | MODEL | stipulated | — | V019 |
| V023 | NEW | Free edges orient from later-marked to earlier-marked. | MODEL | stipulated | — | V019 |
| V024 | NEW | Phase 4 un-peels the Phase-0 pendants in reverse. | MODEL | stipulated | — | V007 |
| V025 | NEW | All five §1.1 properties are stated as checkable claims and all verified on 1444 data. | DESIGN | stipulated | — | — |
| V026 | REVISED | Property 1, global DAG: every arc points from later-marked to earlier-marked, so reversed marking order is a topological order. | MODEL | derivation | C009 | V019, V023 |
| V027 | NEW | Pendant edges are bridges and cannot close a cycle. | MODEL | derivation | — | V007 |
| V028 | NEW | Measured: acyclic 29/29 goods on 1444 data. | MODEL | numerical test | — | V026 |
| V029 | NEW | Property 2, sink placement is explicit: the final sinks are exactly `{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal demanders}`. | MODEL | derivation | — | V011, V022 |
| V030 | NEW | Measured: 1–8 sinks per good, mean 3.6, on 1444 data. | MODEL | numerical test | — | V029 |
| C010 | UNCHANGED | A node with no outgoing links for `g` is a sink for `g`. | MODEL | stipulated | — | — |
| C011 | UNCHANGED | Sinks differ from good to good. | OUTCOME | derivation | — | C005, C010 |
| C012 | UNCHANGED | There is no global end node across the per-good networks. | MODEL | derivation | — | C011 |
| V031 | NEW | Property 3, reachability is a feasibility theorem: the orientation contains a flow serving 100% of every good's demand, because the LP imposes node balance. | MODEL | derivation | — | V015 |
| V032 | NEW | Measured: 100.0% of demand reachable from supply, 29/29 goods, zero orphan sinks. | MODEL | numerical test | — | V031 |
| V033 | NEW | Property 4, scan-invariance: ready-marking is a monotone closure, so the stall sequence, promotions and fallbacks are provably independent of scheduling. | MODEL | derivation | — | V019 |
| V034 | NEW | The priority key makes the remaining freedom (free-edge direction) a function of the graph and the balances alone. | MODEL | derivation | — | V020 |
| V035 | NEW | Measured: zero orientation changes under scheduler permutations; zero exact key ties. | MODEL | numerical test | — | V033, V034 |
| V036 | NEW | Property 5, efficiency: unit costs make the certificate flow a fewest-hop routing. | MODEL | derivation | — | V015 |
| C019 | UNCHANGED | The whole system is recomputed on a fixed monthly tick. | MODEL | stipulated | — | — |
| C020 | UNCHANGED | That tick is aligned to the vanilla trade tick. | MODEL | stipulated | — | C021 |
| C021 | UNCHANGED | EU4 has a monthly trade tick to align to. | ENGINE | UNSOURCED | — | — |
| C022 | UNCHANGED | Orientation is read from the current solve every time, with no memory of the previous one. | MODEL | stipulated | — | C019 |
| V037 | NEW | The LP is deterministic — six identical solves produced one orientation on the reference implementation. | MODEL | numerical test | — | V015 |

## §1.2 — Supply (lines 76–87)

**UNCHANGED:** C023, C025, C026, C027, C028

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V038 | NEW | ⚑ `00_static_modifiers.txt` carries `trade_goods_size_modifier` on `devastation`, `occupied`, `under_siege`, and `prosperity`. | ENGINE | file value | — | — |
| V039 | REVISED | There is no supply regularizer — v1's ε is deleted; DRAIN orients free edges combinatorially by the drainage sweep, not by comparing near-equal solved potentials. | DESIGN | derivation | C029, C030 | V023 |
| V040 | NEW | A node with `b = 0` exactly is handled as an ordinary conduit. | MODEL | derivation | — | V005 |
| V041 | NEW | Exactly one node has `b = 0` exactly at 1444: `cape_of_good_hope`. | MODEL | numerical test | — | V040 |

## §1.3 — Demand (lines 89–105)

**UNCHANGED:** C031, C032, C033, C035, C036, C039

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V042 | REVISED | ⚑ There is no flat 75% overseas autonomy floor in 1.37; autonomy floors are regime-dependent. | ENGINE | file value | C037 | V044, V045, V046, V047 |
| V043 | NEW | ⚑ The 75% overseas rule is pre-Common-Sense. | ENGINE | UNSOURCED | — | V042 |
| V044 | NEW | ⚑ A province in a territory is floored at 90% local autonomy (`territory_core` / `territory_non_core` in `00_static_modifiers.txt`). | ENGINE | file value | — | — |
| V045 | NEW | ⚑ A colonial core is floored at 50% local autonomy. | ENGINE | file value | — | — |
| V046 | NEW | ⚑ A pasha state is floored at 20% local autonomy. | ENGINE | file value | — | — |
| V047 | NEW | ⚑ A stated core is floored at 0 local autonomy. | ENGINE | file value | — | — |
| V048 | REVISED | The wealth pipeline applies the applicable floor per province — a territory province contributes ~10% of its development's income, a colonial core ~50%. | MODEL | derivation | C038 | V044, V045 |

## §1.4 — Market concentration (lines 107–117)

**UNCHANGED:** C040, C041, C042, C043, C044, C045, C046, C047

## §1.5 — Goods without a graph (lines 119–135)

**UNCHANGED:** C048, C051, C052, C053, C054, C055, C056

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V049 | REVISED | Gold excludes itself from demand: under `wealth = tax_income + production_income`, gold income is invisible to demand entirely — not merely diverted — whether or not the treasure-fleet diversion is active. | MODEL | derivation | C049, C050 | V050, V051 |
| V050 | NEW | ⚑ Gold-mine income is its own income category in the engine — `INCOMEGOLD`, with `gold_income` a distinct scriptable field. | ENGINE | file value | — | — |
| V051 | NEW | ⚑ Gold income is computed from mine value with its own constants (`GOLD_MINE_SIZE`) and is not booked as production income. | ENGINE | file value | — | V050 |
| V052 | NEW | ⚑ Gold is inert in vanilla trade value: `base_price = 0`, `goldtype = yes`. | ENGINE | file value | — | — |
| V053 | NEW | Excluding gold from the networks therefore costs nothing. | MODEL | derivation | — | V052 |
| V054 | NEW | Whether the per-province production-income *field* nevertheless carries the gold figure before the country-level split is unknown (§2.7 item 12). | ENGINE | UNSOURCED | — | V050 |
| V055 | REVISED | ⚑ Coal produces nowhere at the 1444 start, and its default trigger fires on Enlightenment — the Manufactories branches require special flags. | ENGINE | file value | C057 | — |
| V056 | NEW | ⚑ The coal trigger's per-province conditions: `development_discounting_tribal = 20` or owner innovativeness 20, that province's own institution progress at 100, and the owner having the institution. | ENGINE | file value | — | V055 |
| V057 | NEW | ⚑ There are 58 latent-coal provinces. | ENGINE | file value | — | — |
| V058 | REVISED | The latent-coal provinces convert province-by-province over years, not in a single tick; the graph grows as they do. | OUTCOME | derivation | C058 | V055, V056, V057 |

## §1.6 — The aggregate graph (lines 137–153)

**UNCHANGED:** C059, C062

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V059 | REVISED | `Φ_ord = Σ_g V_g · order_g`, where `order_g(v)` is `v`'s marking order in `g`'s drainage sweep. | MODEL | stipulated | C060 | C059, V019 |
| V060 | NEW | Each good's marking order is a per-node scalar whose descending comparison reproduces that good's DAG. | MODEL | derivation | — | V023, V026 |
| V061 | REVISED | The value-weighted sum of marking orders is a potential, so orienting edges by it is acyclic for free. | MODEL | derivation | C061 | V059, V060 |
| V062 | NEW | Measured on 1444 data, `Φ_ord` agrees with its own per-good graphs on 62.7% of edge-goods — against 52.6% for v1's `Φ` measured against v1's own per-good graphs. | MODEL | numerical test | — | V059 |
| V063 | REVISED | The v1 diagnostic identity (`Φ ≡ φ₀` at α = 1) does not survive the operator change: DRAIN performs no linear solve, so no linearity argument exists. | MODEL | derivation | C063 | V006 |
| V064 | REVISED | The replacement end-to-end correctness check is exact orientation equality between the reference and DLL implementations — a combinatorial comparison with no tolerance band. | DESIGN | stipulated | C206, C327 | V063 |

## §1.7 — Merchants (lines 155–179)

**UNCHANGED:** C067, C068, C069, C070, C071, C072, C074, C075, C076, C077, C078, C079, C080, C081, C082, C083

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V065 | REVISED | The UI change is what an incoming link entry *does* — it must accept a merchant assignment rather than merely navigate — not the addition of a list; this is the only UI change. | DESIGN | stipulated | C073, C166 | V066 |
| V066 | NEW | ⚑ The vanilla node window already renders both an incoming and an outgoing link list as clickable entries — `incoming_nodes_listbox` / `outgoing_nodes_listbox` in `tradeinterface.gui`, both populated by the `TradeNodeLink` widget. | ENGINE | file value | — | — |
| V067 | NEW | Whether the existing `NextNodeButton` already accepts a merchant assignment is unknown (§2.7 item 14). | ENGINE | UNSOURCED | — | V066 |
| V068 | REVISED | ⚑ The engine's caravan grant conditions are `merchant_present_inland` and `merchant_steering_to_inland`, with nothing checking whether value moves. | ENGINE | file value | C537 | — |
| V069 | REVISED | ⚑ The engine's tooltip reads as granting the caravan bonus in the inland node, not the adjacent one. | ENGINE | file value | C538 | V068 |
| V070 | NEW | §2.7 item 11 settles the caravan recipient; §3.11 carries both readings of the exposure surface. | DESIGN | stipulated | — | V068, V069 |

## §1.8 — Collection and transfer (lines 181–204)

**UNCHANGED:** C084, C085, C086, C087, C088, C089, C090, C091, C092, C093, C094, C095, C096, C097, C098, C099, C102

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V071 | REVISED | ⚑ Trade range gates merchant placement, not value flow — no mechanic gates flow by range. | ENGINE | UNSOURCED | C100 | — |
| V072 | REVISED | ⚑ There is no trade "supply range" in the engine; the only supply-range constructs are naval. | ENGINE | UNSOURCED | C101 | — |

## §1.9 — Trade power propagation (lines 206–215)

**UNCHANGED:** C103, C104, C105, C106, C107, C108, C109, C110, C111

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V073 | NEW | ⚑ The engine's propagation tooltip carries a receiving-side qualifier §1.9 does not: power transfers upstream "to trade nodes where it already has power". | ENGINE | file value | — | C104 |

## §1.10 — Direction-dependent systems (lines 217–260)

**UNCHANGED:** C112, C113, C114, C115, C116, C117, C118, C119, C120, C121, C122, C123, C124, C125, C126, C127, C133, C134, C135, C136, C137, C138, C140, C142, C143

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V074 | REVISED | ⚑ Improve Inland Routes requires 50% trade power to establish and 40% to maintain, plus a merchant present in the node, and is waived entirely by the `free_improve_inland_routes` government attribute. | ENGINE | file value | C128 | — |
| V075 | REVISED | ⚑ Propagate Religion requires 50% to establish and 50% to maintain in the default branch — a country-flag ladder runs 5–50, terminal fallback 35/35 — with no band. | ENGINE | file value | C129, C130 | — |
| V076 | REVISED | The banding is the reverse of what v1 recorded: Improve Inland Routes is the one banded mechanic, Propagate Religion has no band, and every other listed threshold is single-valued — so nothing absorbs threshold chatter on its own. | ENGINE | derivation | C131, C132 | V074, V075 |
| V077 | NEW | A power share oscillating across any of these limits flickers the mechanic, Propagate Religion included. | OUTCOME | derivation | — | V076 |
| V078 | REVISED | ⚑ No mission, decision, event, or trade company in 1.37.5 names a trade node — zero non-comment references across `common/`, `missions/`, `decisions/`, `events/`; trade companies are bare province lists — so the name-collision class of conflict is empty and the conclusion is stronger than v1 stated. | ENGINE | file value | C139, C141 | — |
| V079 | NEW | ⚑ Scripted content reaches nodes only structurally: `home_trade_node`, `any/random/every_active_trade_node`, `*_trade_node_member_province`, and `highest_value_trade_node`. | ENGINE | file value | — | — |
| V080 | NEW | What remains exposed is semantics: `highest_value_trade_node` and node-scoped triggers are evaluated against a reoriented graph. | MODEL | derivation | — | V079, C140 |

## §1.11 — Treasure fleets (lines 262–268)

**UNCHANGED:** C144, C145, C146, C147, C148 *(C148's basis is now V049: gold income never enters `wealth` in the first place, diverted or not.)*

## §1.12 — What the game displays (lines 270–287)

**UNCHANGED:** C149, C150, C151, C152, C153, C154, C155, C156, C157, C159, C160, C161, C162, C163, C164, C165

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V081 | REVISED | ⚑ The node window carries several node-level value fields (incoming / local / total / outgoing), but none takes a commodity argument — zero per-good fields, where thirty would be needed. | ENGINE | file value | C158 | — |
## §2.1 — Shape (lines 293–306)

**UNCHANGED:** C167, C168, C169, C170, C171, C172, C173, C174, C175, C177, C178, C179, C180, C181, C182, C184

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V082 | REVISED | ⚑ Achievements are off with any mod — `ACHIEVEMENTS_DISABLED_MODIFIED_GAME`. | ENGINE | file value | C176 | — |
| V083 | NEW | ⚑ The engine itself will load an ironman save in a modded game — "Loading ironman in modded game" is a shipped code path. | ENGINE | file value | — | — |
| V084 | NEW | Ironman saves are binary-encoded. | ENGINE | UNSOURCED | — | — |
| V085 | NEW | The parsers target non-ironman because of the binary encoding, not because ironman is unavailable in modded games. | DESIGN | derivation | — | V083, V084 |
| V086 | REVISED | For DRAIN the bit-reproducibility exposure is narrower than v1's dense linear algebra but still real: the min-cost-flow solve must pivot identically given identical input (fixed arc ordering, one solver build, no threading), and the sweep is already integer/combinatorial. | MODEL | derivation | C183 | C182, V015 |

## §2.2 — Solver (lines 308–331)

**UNCHANGED:** C185, C186, C187, C188, C189, C190, C194, C195, C196, C197, C198, C199, C202, C203, C204, C205, C207, C208, C209

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V087 | REVISED | Solver item 4 computes per-province `wealth` with the §1.3 regime-dependent autonomy floors, per-node `trade_value`, `s`, `c` with per-province α, and the per-good balance `b = s − c`. | DESIGN | stipulated | C191 | V048, V005 |
| V088 | REVISED | Solver item 5 is DRAIN per good: min-cost b-flow (network simplex or LP), the deterministic drainage sweep, and the Phase-4 evaluator (`unserved` / `stranded`); then `Φ_ord = Σ_g V_g · order_g`. | DESIGN | stipulated | C192, C193 | V006, V059 |
| V089 | NEW | `unserved` and `stranded` must be equal by conservation. | MODEL | derivation | — | V088 |
| V090 | REVISED | Cost per good is one uncapacitated min-cost flow on 80 nodes / 318 arcs plus an O(V+E) sweep — milliseconds each with network simplex, tens of milliseconds for all 29 goods per monthly tick. | MODEL | derivation | C200, C201 | C199, V091 |
| V091 | NEW | The vanilla node graph presents 318 arcs to the flow solve. | ENGINE | file value | — | C186 |
| V092 | REVISED | ⚑ The `inland` flag and the coastal-member derivation disagree at exactly one node: `siberia` carries `inland=yes` but has two Arctic-coast members (1781, 1782), so derivation gives 25 inland nodes against the flag's 26. | ENGINE | file value | C210 | C209 |

## §2.3 — Constants (lines 333–353)

**UNCHANGED:** C211, C212, C213, C214, C215, C216, C217, C218, C219, C220, C222, C223, C224, C225, C226, C227

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V093 | REVISED | The design constants are the excluded-goods list (defaults to gold), the α anchor `P₀ = 2.0`, and DRAIN's three knobs at defaults — `ρ = 1.0`, `r = 0`, and the zero-flow tolerance `1e-11` (numerical only). | DESIGN | stipulated | C221 | C222, V012 |
| V094 | NEW | A measured calibration option that moves all three knobs plus α's clamp is recorded in §3.13; the baseline does not use it. | DESIGN | stipulated | — | V177 |

## §2.4 — The tradenodes file (lines 355–366)

**UNCHANGED:** C228, C229, C230, C231, C232, C233, C234, C235, C236, C237, C238, C239, C240, C241, C242

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V095 | NEW | ⚑ The shipped vanilla `00_tradenodes.txt` is itself topologically sorted sources-first — 0 of 159 links violate declaration order. | ENGINE | file value | — | C186 |
| V096 | NEW | Whether the engine *requires* topological declaration order is open — §2.7 item 13's companion question. | ENGINE | UNSOURCED | — | C234 |

## §2.5 — Runtime attachment (lines 368–372)

**UNCHANGED:** C243, C244, C245, C246, C247, C248, C249, C250

## §2.6 — Writing to the engine (lines 374–394)

**UNCHANGED:** C251, C252, C253, C254, C255, C256, C257, C258, C259, C260, C261, C262, C263, C264, C265, C266, C267, C268, C269, C270, C271, C272

## §2.7 — Probes (lines 396–419)

**UNCHANGED:** C274, C275, C276, C277, C278, C279, C280, C281, C282, C283, C284, C285, C286, C287, C288, C289, C290, C291, C292, C293

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V097 | REVISED | Items 1–10 are the v1 probe set, settled with a debugger in one session — though several are observable without one; items 11–15 need no debugger at all (a save, a tooltip, or a single file edit), three of them change what the spec says rather than confirming it, and they are done first. | DESIGN | stipulated | C273 | — |
| V098 | NEW | ⚑ Static string-table analysis yields three named direction call sites: `DIPLO_SELLPROV_NOT_UPSTREAM`, `TREASURE_FLEET_TOOLTIP_CANT_REACH`, `TRADE_POWER_UPSTREAM`. | ENGINE | file value | — | — |
| V099 | NEW | ⚑ Both nation-pair direction gates compare trade capitals. | ENGINE | file value | — | V098 |
| V100 | NEW | ⚑ No colonisation refusal string exists in the binary. | ENGINE | file value | — | V098 |
| V101 | NEW | Probe 11: the caravan recipient is identifiable as whichever of the two node windows shows trade power jumping by `min(dev/3 + modifiers, 50)`. | DESIGN | stipulated | — | V068, V069, V167 |
| V102 | NEW | Probe 12: one gold-province Production income tooltip settles §1.5's residual — per-province gold figure or zero with gold only in the country's `INCOMEGOLD` line. | DESIGN | stipulated | — | V054 |
| V103 | NEW | Probe 13: hand-author a two-node cycle in `00_tradenodes.txt`, load fresh, read `logs/error.log` and the trade mapmode. | DESIGN | stipulated | — | V148, V149 |
| V104 | NEW | Probe 14: whether an incoming `TradeNodeLink` entry accepts a merchant assignment or only navigates decides whether §1.7's UI change is a behaviour change to an existing widget or a new interaction. | DESIGN | stipulated | — | V067 |
| V105 | NEW | Probe 15: whether a country with above-threshold power in X and zero power in upstream Y appears in Y is unknown. | ENGINE | UNSOURCED | — | V073 |

## §2.8 — Validation (lines 421–457)

**UNCHANGED:** C298, C299, C300, C301, C302, C303, C304, C305, C306, C307, C308, C309, C310, C311, C312, C313, C314, C315, C316, C317, C318, C319, C320, C323, C324, C325, C326, C328, C329, C330, C331, C332, C333, C334, C335, C336, C337, C338, C339, C340, C341, C342

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V106 | REVISED | Baseline DRAIN measured on 1444: spices sink at Genoa (demand rank 1) plus branch-end termini (Australia, Brazil); cloves at Venice, Kongo, Australia, Brazil. | MODEL | numerical test | C294, C295 | V029 |
| V107 | NEW | China holds a spice sink only under the §3.13 α-calibration option (which puts cloves at Beijing); v1's expectation of simultaneous China+Europe sinks is not the baseline behaviour. | MODEL | numerical test | — | V106, V177 |
| V108 | REVISED | Sinks are `{selected ∩ flow-terminal} ∪ promoted`, 1–8 per good; high-demand nodes are sinks at 14% in the top demand decile vs 7% in the bottom — a barbell, with LP branch ends landing in poor pockets. | MODEL | numerical test | C296, C297 | V029, V030 |
| V109 | REVISED | Acyclicity is asserted on every per-good graph, on `Φ_ord`, and on the emitted file's declaration order. | DESIGN | stipulated | C322 | V026, V061 |
| V110 | NEW | Reachability is asserted every tick — 100% of every good's demand reachable, zero orphan sinks; its failure means the implementation broke, not the world. | DESIGN | derivation | — | V031 |
| V111 | NEW | Conservation is asserted every tick — Phase-4 `Σ unserved == Σ stranded` to machine precision, every good. | DESIGN | stipulated | — | V089 |
| V112 | NEW | Determinism is asserted — re-running a tick reproduces the orientation bit-for-bit; promotions and fallbacks are scheduler-invariant (monotone closure). | DESIGN | derivation | — | V033, V037 |

## §2.9 — Build order (lines 459–467)

**UNCHANGED:** C343, C344, C345, C346, C348, C349, C350, C351, C352

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V113 | REVISED | After the defines parser, the solver track runs: the b-flow and sweep with their per-tick assertions (reachability, conservation, acyclicity, determinism), per-good eligibility, realized flows, the `Φ_ord`-vs-realized disagreement measurement, the reachability census, and the flip-rate measurement. | DESIGN | stipulated | C347 | V110, V111, V112 |
## §3.1 — Goals (lines 473–481)

**UNCHANGED:** C353, C354, C355, C356, C357, C358, C359, C360, C361, C362, C363, C364, C365

## §3.2 — Why a flow and a drainage sweep (lines 483–530) — full-strength extraction

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V114 | NEW | Two families of orientation fail before this one, and both failures are theorems, not taste. | MODEL | derivation | — | C370, V116 |
| C370 | UNCHANGED | Local comparison (rank orientation) is monotone. | MODEL | derivation | — | — |
| C371 | UNCHANGED | Under a monotone orientation no path can dip through a low-value intermediary and rise again. | MODEL | derivation | — | C370 |
| C372 | UNCHANGED | Malacca → … → Cape → … → Europe requires exactly such a dip and rise. | MODEL | derivation | — | — |
| C366 | UNCHANGED | Orienting each edge by comparing its endpoints fails on the Malacca–Cape corridor. | MODEL | derivation | — | C371, C372 |
| V115 | NEW | Monotonicity also killed the tested `s − c` operator: demand had to increase at every hop, one sixth of world demand became unreachable, and Genoa was crowned a cloves sink that cloves could not reach. | MODEL | numerical test | — | C370 |
| C373 | UNCHANGED | Merchants cannot repair a wrong orientation. | ENGINE | derivation | — | C374 |
| C374 | UNCHANGED | A merchant selects among existing outgoing arrows and cannot reverse one. | ENGINE | UNSOURCED | — | — |
| C375 | UNCHANGED | Route-awareness must therefore live in the orientation itself. | DESIGN | derivation | — | C373 |
| V116 | REVISED | v1's sink rule turns out to be exactly `(c − s)/deg > mean(neighbour φ) − min(neighbour φ)` — verified on every (good, node) pair. | MODEL | numerical test | C382 | — |
| V117 | NEW | Supply contrast (10⁷) exceeds demand contrast (10²–10³) by four to five orders of magnitude, so the rule's right-hand side is set by supply geography. | MODEL | numerical test | — | V116 |
| V118 | NEW | v1's sinks landed where the field was locally flat, not where demand was. | MODEL | numerical test | — | V116, V117 |
| V119 | NEW | Under v1, the highest-demand node in the game was never a spices sink. | MODEL | numerical test | — | V118 |
| V120 | NEW | Under v1, a node with literally zero demand outranked Genoa and Beijing. | MODEL | numerical test | — | V118 |
| V121 | NEW | Deleting demand variation entirely left the v1 sink unmoved. | MODEL | numerical test | — | V118 |
| V122 | NEW | No parameter fixes v1: α strong enough to matter destroys §1.4's regime split. | MODEL | derivation | — | C442 |
| V123 | NEW | Better wealth inputs move v1's threshold by 1.7× where 4–5× is needed. | MODEL | numerical test | — | V117 |
| V124 | NEW | The conservation lesson: operators that impose node balance somewhere serve 100% of demand as a theorem; operators that don't, strand it. | MODEL | derivation | — | V031, V115 |
| V125 | NEW | DRAIN takes sink placement out of field geometry entirely: sinks are the selected demand centres plus the flow-terminal drains any acyclic drainage orientation is forced to have anyway. | MODEL | derivation | — | V029 |
| V126 | NEW | Nothing outside that set can be a sink: every other node is given an out-arc by the sweep. | MODEL | derivation | — | V029 |
| V127 | NEW | v1 never stated the four claims now stated and checkable: sink placement, free-edge direction, reachability, aggregate acyclicity. | WORLD | stipulated | — | V029, V034, V031, V061 |
| V128 | REVISED | The 1444 Cape has `s = c = 0` exactly. | MODEL | numerical test | C367, C368 | V041 |
| V129 | REVISED | A conduit node (`s = c = 0`) carries flow through: the Cape's in- and out-degree are both nonzero for all 29 goods. | MODEL | numerical test | C377, C378 | V128 |
| V130 | NEW | The corridor runs through the Cape because it is the short route to Atlantic Europe — 3 hops to the Channel against 7 via Alexandria. | ENGINE | file value | — | C186 |
| V131 | NEW | The flow routes 24% of world spice supply through the Cape, where v1's potential never used it at all. | MODEL | numerical test | — | V129, V130 |
| C383 | UNCHANGED | Peripheral sinks are intended, not a defect. | DESIGN | stipulated | — | — |
| C384 | UNCHANGED | Goods flow to a periphery and are consumed at the end of the line. | OUTCOME | derivation | — | V125 |
| C385 | UNCHANGED | Value only arrives where someone holds power at both ends of the link. | ENGINE | derivation | — | C102 |

## §3.3 — Why wealth, and why per province (lines 532–547)

**UNCHANGED:** C386, C387, C388, C389, C390, C391, C392, C393, C394, C395, C396, C397, C398, C399, C400, C401, C402, C403, C404, C405, C406, C408, C412, C413

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V132 | REVISED | ⚑ Node sizes run from 19 land provinces (`cape_of_good_hope`) to 77 (`girin`) — a 4× spread with no structural rule behind it. | ENGINE | file value | C407 | — |
| V133 | REVISED | Raising a node's aggregate wealth to a power rewards node size, so luxuries would drain toward whichever node the map authors sliced *coarsest*. | MODEL | derivation | C409 | C408 |
| V134 | NEW | At α = 1.5 a 77-province node beats a 19-province node of equal total wealth by 2× purely on slicing. | MODEL | derivation | — | V133 |
| V135 | NEW | ⚑ Nippon has 68 land provinces; the Paris node (`champagne`) has 33. | ENGINE | file value | — | — |
| V136 | REVISED | Under node-level α, Nippon would out-consume the Paris node on province count. | OUTCOME | derivation | C410, C411 | V133, V135 |

## §3.4 — Why supply is pre-modifier (lines 549–557)

**UNCHANGED:** C415, C416, C417, C418, C419, C420, C421, C422, C423

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V137 | REVISED | Substituting production income for trade value would make `V_g` — and with it the aggregate's weighting — depend on owners' idea groups and autonomy. | MODEL | derivation | C424 | C421, C422, C423 |
| V138 | NEW | In v1 the same substitution measurably broke the α = 1 identity: orientation agreement collapsed from 159/159 to 68/159. | MODEL | numerical test | — | V137 |
| V139 | NEW | The identity is gone in v2, but the reason to refuse the substitution is unchanged. | DESIGN | derivation | — | V063, V137 |

## §3.5 — Why α is anchored absolutely (lines 559–574)

**UNCHANGED:** C427, C428, C429, C430, C431, C436, C439, C440, C441, C442

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V140 | REVISED | ⚑ At vanilla base prices nothing sits below the 2.0 anchor: the minimum tradeable base price is exactly 2.0. | ENGINE | file value | C432, C433, C434 | — |
| V141 | NEW | ⚑ Fur, naval supplies, slaves, tea, tropical wood, and livestock have base price exactly 2.0, sitting on the anchor at α = 1 exactly. | ENGINE | file value | — | V140 |
| V142 | NEW | ⚑ Grain's base price is 2.5, not the 1.25 v1 recorded. | ENGINE | file value | — | — |
| V143 | NEW | Both of v1's figures (grain 1.25, livestock 1.00) were price/P₀ ratios misread as prices. | WORLD | derivation | — | V141, V142 |
| V144 | REVISED | The sublinear regime is entered *only* when a price event pushes a good beneath the anchor. | MODEL | derivation | C435 | V140, C046 |
| V145 | NEW | ⚑ 13 of 30 goods can be pushed below 2.0 by a single vanilla `change_price` event; grain and wine reach 0.625. | ENGINE | file value | — | — |
| V146 | NEW | ⚑ 11 goods have no negative price event at all and can never go sublinear in vanilla. | ENGINE | file value | — | — |
| V147 | REVISED | Whether the sublinear regime engages often enough to earn its keep is now a bounded question, not an open one. | DESIGN | derivation | C437 | V145, V146 |

## §3.6 — Why no hysteresis, and why there is no ε (lines 576–600) — full-strength extraction

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| C443 | UNCHANGED | A margin on orientation is a correctness bug, not a tuning knob. | DESIGN | stipulated | — | C445 |
| C444 | UNCHANGED | Holding an edge against the current month's result splices orientations decided at different times. | MODEL | derivation | — | C022 |
| C445 | UNCHANGED | A splice of two acyclic orientations need not be acyclic. | MODEL | numerical test | — | C444, C446 |
| C446 | UNCHANGED | Tested in v1: with tol = 1e-3 and values {0, 0.0006, 0.0012}, tolerance-based tie-breaking produced A→B→C→A. | MODEL | numerical test | — | — |
| V148 | REVISED | ⚑ The node-file *format* represents cycles perfectly well: it is a list of named directed links with no acyclicity constraint. | ENGINE | file value | C447 | C186 |
| V149 | NEW | What the design depends on is the *engine's* behaviour on a cyclic file, which is unverified and load-bearing. | ENGINE | UNSOURCED | — | V148 |
| V150 | REVISED | Until §2.7 item 13 runs, acyclicity is enforced because we cannot prove the engine tolerates its absence. | DESIGN | derivation | C448 | V149 |
| C449 | UNCHANGED | Nothing needs to stop orientation churn. | DESIGN | stipulated | — | V151, C452 |
| V151 | REVISED | A link whose flow-support membership alternates month to month carries near-nothing either way. | MODEL | derivation | C450, C451 | V015, V018 |
| C452 | UNCHANGED | Merchant assignments are to links, so they survive flips untouched. | ENGINE | derivation | — | C076 |
| V152 | REVISED | v1's ε is deleted because the problem it patched no longer exists: the Laplacian oriented dead branches by comparing solved potentials that were mathematically equal and differed only by floating-point residual, so orientation varied by machine and a field-level regularizer was needed to break ties on purpose. | MODEL | derivation | C453, C455, C459 | V039 |
| V153 | NEW | DRAIN's priority key is computed from exact input data. | MODEL | derivation | — | V020 |
| V154 | NEW | Determinism is asserted per tick rather than approximated by a nudge. | DESIGN | stipulated | — | V112 |

## §3.7 — Why eligibility is per good (lines 602–608)

**UNCHANGED:** C463, C464, C465, C466, C467, C468, C469, C470, C471, C472, C473

## §3.8 — Why gates evaluate true (lines 610–628)

**UNCHANGED:** C474, C475, C476, C477, C478, C479, C480, C481, C482, C483, C484, C485, C489, C490, C491, C492, C493, C494, C495, C496, C497

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V155 | REVISED | ⚑ The shipped policy file gates Propagate Religion on the trade share AND the node being in a trade company region AND a merchant present AND a religion-group/flag disjunction AND `dominant_religion`, with `unique = yes` per node. | ENGINE | file value | C486 | C485 |
| V156 | NEW | v1's "gated on a trade-power threshold there and nothing else" was wrong, and was one of only three claims carrying `verified (method unstated)` provenance. | WORLD | derivation | — | V155 |
| V157 | REVISED | ⚑ What the trade-policy family shares is the absence of any direction test: no trading policy anywhere in `00_trading_policies.txt` tests upstream/downstream. | ENGINE | file value | C487, C488 | — |
| V158 | NEW | ⚑ Three of the five trading policies have no trade-share threshold at all (merchant-present only). | ENGINE | file value | — | V157 |
| V159 | REVISED | Measured: 98.8% of ordered node pairs are connected by at least one good on 1444 data. | MODEL | numerical test | C498 | C492 |

## §3.9 — Why `Φ_ord` is the installed graph (lines 630–646) — full-strength extraction

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| C499 | UNCHANGED | `Φ_ord` is a legal DAG, being a per-node scalar (a potential) itself. | MODEL | derivation | — | V061 |
| V160 | REVISED | `Φ_ord` is the value-weighted aggregate of the real per-good drainage orders rather than an invented baseline. | MODEL | derivation | C500 | V059 |
| V161 | REVISED | Once the displayed numbers are the model's numbers, the installed graph must be *close to* the one the economy actually runs. | DESIGN | derivation | C501 | C149 |
| V162 | NEW | Two aggregates were tested and one is impossible: the value-weighted net flow `Σ_g V_g·net_g` is a flow, flows circulate, and it measurably contains directed cycles — it cannot be installed. | MODEL | numerical test | — | — |
| C502 | UNCHANGED | A difference in `Φ_ord` across a link is not the net value crossing it. | MODEL | derivation | — | C506, C507 |
| C505 | UNCHANGED | Realized movement follows vanilla propagation rules instead. | ENGINE | derivation | — | C091 |
| C506 | UNCHANGED | A good with large Δ can be diluted by an even split across three links. | MODEL | derivation | — | C097 |
| C507 | UNCHANGED | A good with small Δ can be winner-take-all steered the other way. | MODEL | derivation | — | C095 |
| C508 | UNCHANGED | A link can be oriented `n → m` under `Φ_ord` while realized net flow runs `m → n`. | MODEL | derivation | — | C506, C507 |
| C509 | UNCHANGED | That is why the disagreement rate is measured rather than assumed. | DESIGN | derivation | — | C508, V062 |
| C510 | UNCHANGED | And why the negative-link display policy is deferred to data. | DESIGN | derivation | — | C508 |
| C512 | UNCHANGED | Link values are realized flows, which makes conservation hold by construction. | MODEL | derivation | — | C257 |

## §3.10 — Why the engine's economy is overwritten (lines 648–663)

**UNCHANGED:** C513, C514, C515, C516, C517, C518, C519, C520, C521, C522, C523, C524, C525, C526, C527, C528, C529, C530

## §3.11 — Why caravan power needs a condition added (lines 665–686)

**UNCHANGED:** C531, C533, C534, C535, C536, C539, C541, C544, C545, C546, C547

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V163 | NEW | ⚑ The engine's own hint states steering is outgoing-only: "You can never steer trade upstream or past your Main Trade City". | ENGINE | file value | — | C531 |
| V164 | REVISED | ⚑ The *display* is not outgoing-only: the node window already lists incoming links as clickable entries. | ENGINE | file value | C532 | V066 |
| V165 | REVISED | The exposure surface is either the ~26 inland nodes themselves (tooltip reading: "steers towards an inland trade node will give you extra trade power *in that node*") or every node adjacent to one (v1 reading) — smaller and differently shaped under the first. | MODEL | derivation | C540 | V069, C541 |
| V166 | NEW | §1.7's added condition is the right guard under both readings. | DESIGN | derivation | — | V165, C539 |
| V167 | REVISED | ⚑ Caravan power is total country development ÷ 3 **plus policy and idea modifiers**, clamped to [2, 50]. | ENGINE | file value | C542 | C219 |
| V168 | REVISED | ⚑ Nineteen countries are at the caravan cap from raw 1444 development alone; Burgundy, Korea, the Timurids and Portugal start 2–10% short and reach it with any caravan modifier. | ENGINE | file value | C543 | V167 |

## §3.12 — Why treasure fleets are always granted (lines 688–701)

**UNCHANGED:** C556, C557, C558, C559, C560

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V169 | REVISED | The argument is consistency with §3.8, and consistency carries the decision alone. | DESIGN | stipulated | C548 | C112, C144 |
| V170 | REVISED | v1's bistability argument is deleted: gold income never enters `wealth` at all, so neither granting nor denial moves the demand vector, and there is no direct feedback to be bistable. | MODEL | derivation | C549, C551, C552, C553, C554, C555 | V049 |
| V171 | REVISED | ⚑ The engine's own denial branch confirms what denial does: "They will keep their gold income instead." | ENGINE | file value | C550 | — |
| V172 | NEW | A slow second-order version survives — kept gold spent on development raises `base_tax` and `base_production` years later — but a multi-year indirect loop is not a bifurcation and does not carry the design decision. | MODEL | derivation | — | V170 |

## §3.13 — Open questions (lines 703–735)

**UNCHANGED:** C561, C562, C563, C564, C565, C566, C567, C568, C569, C570, C571, C572, C573, C574, C575, C578, C579, C580, C585

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V173 | NEW | Static string-table analysis leans against a colonization gate: the only direction-refusal strings in the binary belong to sell-province and treasure fleets, none to colonisation. | ENGINE | derivation | — | V098, V100 |
| V174 | REVISED | Of §2.7, only pass caching, pass-2 content, write windows and the caller enumeration truly need the debugger; items 11–15 need a save, a tooltip, or one file edit, and the propagation-threshold and one-hop questions are node-window reads. | DESIGN | stipulated | C576, C577 | V097 |
| V175 | NEW | Three of the cheap probes (caravan recipient, cyclic file, incoming-link button) change what the spec *says*; they are done first. | DESIGN | stipulated | — | V097 |
| V176 | REVISED | α_min's bite is bounded from files: the sublinear regime is reachable through vanilla price events for 13 of 30 goods and unreachable for 11; whether those events fire often enough in a real campaign remains the open half. | DESIGN | derivation | C581, C582 | V145, V146 |
| V177 | NEW | A measured calibration exists that makes sink counts track price: span exactly 1..5, spearman(price, sinks) = −0.54. | MODEL | numerical test | — | V030 |
| V178 | NEW | Its settings: α unclamped at exponent 2 (cloves α = 16), demand-mass quantile ρ = 0.5, twig tolerance 3e-4. | DESIGN | stipulated | — | V177 |
| V179 | NEW | Unclamped α² is a *demand-model* decision: luxuries become court goods — Beijing, holding the richest single province, becomes the cloves sink. | MODEL | numerical test | — | V178 |
| V180 | NEW | The twig tolerance sacrifices min-cost routing on <0.03% of mass and drops one good's reach to 99.97%. | MODEL | numerical test | — | V178 |
| V181 | NEW | The calibration is one-snapshot tuning. | DESIGN | stipulated | — | V177 |
| V182 | NEW | The baseline does not adopt the calibration; adopting it is a §1.4 decision, not a solver knob. | DESIGN | stipulated | — | V177, V179 |
| V183 | REVISED | The ε-magnitude question is replaced by the cross-machine question: the min-cost-flow solve must pivot identically on identical input for multiplayer. | DESIGN | stipulated | C584 | V086 |

## §3.14 — AI merchant assignment (lines 737–754)

**UNCHANGED:** C586, C587, C588, C589, C590, C591, C592, C593, C594, C595, C596, C597, C598, C599, C600, C601, C602, C603, C604, C605, C606, C607, C608, C609, C610, C611, C612, C613, C614, C615, C616, C617, C618, C619, C620, C621, C622, C623, C624

## §3.15 — Rejected (lines 756–834) — full-strength on entries changed with the operator

**UNCHANGED:** C625, C626, C627, C628, C629, C630, C631, C632, C633, C634, C635, C636, C637, C639, C640, C646, C647, C648, C649, C650, C651, C652, C653, C654, C655, C656, C657, C658, C659, C660, C661, C663, C664, C668, C669, C672

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V184 | NEW | The v1 Laplacian potential is rejected as the orientation core: its sink placement is topological — sinks land where the field is locally flat, demand enters only as `(c−s)/deg` against the local spread. | DESIGN | derivation | — | V116, V118 |
| V185 | NEW | What the Laplacian did guarantee — 100% reachability via conservation, exact conduit behaviour — DRAIN keeps by construction. | MODEL | derivation | — | V124, V129 |
| V186 | NEW | Pure min-cost-flow orientation (no sweep) is rejected: it orients only the ~79-edge support (a spanning-tree basis), leaving half the map undirected. | MODEL | derivation | — | V016 |
| V187 | NEW | Pure MCF's value-weighted aggregate contains directed cycles. | MODEL | numerical test | — | V162 |
| V188 | NEW | DRAIN is exactly pure MCF plus the drainage completion that fixes both defects. | MODEL | derivation | — | V006, V186, V187 |
| V189 | NEW | Ranked orientation (`score = s − c`, harmonic extension on empty nodes) is rejected: monotone, so demand must rise along every route — 83% of demand reachable, 34 orphan sinks, Genoa a cloves sink that cloves cannot reach. | MODEL | numerical test | — | C370, V115 |
| V190 | NEW | Ranked orientation wins every sink statistic and fails the one that matters. | MODEL | numerical test | — | V189 |
| V191 | NEW | Seeded basin growth (multi-source Dijkstra with balance feedback) is rejected: flow converges to the chosen seeds and starves everything off a supply→seed path — 88.5% reach at its best tuning. | MODEL | numerical test | — | — |
| V192 | NEW | Seeded basins' useful ideas — HHI-adaptive sink count, stall self-correction — survive inside DRAIN's Phases 1 and 3. | DESIGN | derivation | — | V011, V022 |
| V193 | NEW | DEF-descending free-edge priority is rejected: on the certificate, unmet demand is identically zero, so DEF is total demand, and pointing free edges into already-served subtrees strands greedy flow; the adopted key is DEF-ascending. | MODEL | numerical test | — | V020 |
| V194 | REVISED | Production income as the aggregate supply term: its v1 second strike — breaking the α = 1 identity — is moot with the identity gone; the first strike suffices. | DESIGN | derivation | C638 | C637, V063 |
| V195 | REVISED | Uniform supply in the aggregate solve: a v1 entry, moot in v2, retained for history — both `φ₀` and the identity left with the Laplacian. | DESIGN | stipulated | C641, C642, C643 | V063 |
| V196 | REVISED | `φ₀` as the installed graph: moot in v2 — the installed graph is `Φ_ord` and its correctness check is cross-implementation orientation equality. | DESIGN | stipulated | C644, C645 | V064 |
| V197 | REVISED | Emission-time pruning of near-flat links stays rejected at baseline; the §3.13 calibration's twig tolerance is a bounded, measured exception available as a deliberate trade. | DESIGN | stipulated | C662 | C663, C664, V180 |
| V198 | REVISED | The audit showed the unweighted metric was in fact the *cause* of v1's sink misplacement, so the honest options were to weight the metric or replace the operator; the operator was replaced, and conductance stays rejected because there is no longer a Laplacian to weight. | DESIGN | derivation | C665, C666, C667 | V116 |
| V199 | REVISED | "The aggregate map is not a DAG" is still an error, with v1's *reason* corrected: v1 defended it by claiming net flow is the gradient of `Φ` — contradicting its own §3.9 and false (the value-weighted net flow measurably contains cycles); the aggregate is a DAG because `Φ_ord` is a per-node scalar and orientation-by-scalar cannot cycle. | MODEL | derivation | C670, C671 | V162, V061 |

## §3.16 — Evidence standard (lines 836–875)

**UNCHANGED:** C677, C680, C681, C682, C684, C685

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V200 | NEW | The claim audit refuted v1's evidence standard itself ("every retraction traced to a premise that entered through prose; nothing built on file values or the model's own equations failed"). | WORLD | derivation | — | — |
| V201 | NEW | At least fifteen non-prose claims failed, by three distinct mechanisms. | WORLD | derivation | — | V200 |
| V202 | NEW | Failure mechanism 1: file values remembered from an older patch — the 75% overseas floor is pre-Common-Sense; 1.37 has regime floors of 90/50/20/0. | WORLD | derivation | — | V042 |
| V203 | NEW | Failure mechanism 2: file values transformed and then reported as raw — v1's grain and livestock base prices are exactly `price / P₀`. | WORLD | derivation | — | V143 |
| V204 | NEW | Failure mechanism 3: the spec's own algebra instantiated without checking — ε provably preserved the α = 1 identity only if applied to `φ₀`'s supply as well; implemented as written, the identity failed at 1e-5 and would have been diagnosed as a solver bug. | MODEL | numerical test | — | — |
| V205 | NEW | Nine of the fourteen refuted engine facts were UNSOURCED. | WORLD | derivation | — | V200 |
| V206 | REVISED | The rule: anything that entered without a recorded source is the risk, whatever it looks like once written down — every engine fact must carry its source (a file path, a binary string, or a named observation), and a claim without one is a to-do, not a fact. | DESIGN | stipulated | C679 | V200, V205 |
| V207 | NEW | v1 never stated what determines sink placement, so the claim inventory had nothing to extract, the validation had nothing to refute, and the model shipped with a fatal placement flaw that claim-checking structurally could not catch. | WORLD | derivation | — | V127 |
| V208 | NEW | The audit found the flaw only by running the solver and asking why the output looked wrong. | WORLD | derivation | — | V207 |
| V209 | NEW | The standing repair is structural: the properties that matter are stated as checkable claims, each provable and each asserted at runtime. | DESIGN | stipulated | — | V025, V127 |
| V210 | NEW | The next audit's first question should be: which property of the output does this spec still not state? | DESIGN | stipulated | — | V209 |
| V211 | REVISED | §1.9 still does not carry the tooltip's second qualifier ("where it already has power"), pending §2.7 item 15 — the cautionary case is not yet closed. | WORLD | derivation | C683 | V073, V105 |

## Orphaned claims.md IDs

v2 no longer asserts these propositions anywhere, and no REVISED claim replaces them (37 IDs):


- **§1.1 Laplacian solve machinery (6):** C013, C014, C015, C016, C017, C018 — singularity of `L`, the `Σ(s−c) = 0` balance condition, pinning, per-component renormalization, and the isolated-node skip. DRAIN's spec text states no counterpart (component handling is unstated in v2).
- **Normalization one-liners, still implied by retained formulas (2):** C024, C034 — "s/c is a share summing to 1" sentences are gone; the formulas they restated remain.
- **`φ₀` machinery (3):** C064, C065, C066 — the diagnostic solve, its supply term, and its never-drawn status left with the identity.
- **α = 1 identity check (1):** C321.
- **Laplacian conduit/sink mechanism (8):** C369, C376, C379, C380, C381 — endpoint-comparison consequence, harmonic-average conduit argument, Europe-draw mechanism, maximum-principle sink claims; C414 — the identity-preservation coincidence; C425, C426 — the identity-break debugging prediction.
- **Sublinear-regime speculation (2):** C438, C583 — the "P₀ mis-set or regime inert" conditional, both copies.
- **ε numerics (7):** C454, C456, C457, C458, C460, C461, C462 — the dead-branch harmonic claim, the 0.37/−0.87 solve values, the ±1e-16 flip, field-level-only, and identity preservation; superseded wholesale by ε's deletion (V039, V152).
- **Analytic ΔΦ figures (3):** C503, C504, C511 — the ΔΦ-is-net-value error acknowledgment and the unconsumed analytic flow.
- **Refuted evidence standard (5):** C673, C674, C675, C676, C678 — the adversarial-review history and "every retraction traced to prose" claims, refuted by the audit (V200–V205).

---

# v2.1 Addendum — the installed aggregate: `Φ_ord` → `Φ_w`

Extracted from `per-good-trade-spec.md` v2.1 (§1.6, §2.2–§2.4, §2.8, §3.9, §3.15) as a delta
against the v2.0 body above. Same statuses and vocabularies. **19 claims, V212–V230: 6 REVISED
(replacing V059, V061, V088, V160, V161, V196, V199 and claims.md C499), 13 NEW.**

**Renaming convention, carried forward:** the global renaming `Φ_ord → Φ_w` in claims that merely
*reference* the installed aggregate — propagation reads it (V065-region), scopes and the fallback
ladder, the tradenodes file source, the caravan probe, the per-link value direction, the
acyclicity assertion (V109), the build-order and disagreement measurements (V113), and the
§3.9 realized-flow caveats (C502, C505–C510, C512) — is treated as UNCHANGED; only claims about
the aggregate *itself* are REVISED. V062 stands unchanged as a true measurement of the superseded
`Φ_ord`.

| ID | Status | Statement | Type | Provenance | Replaces | Depends on |
|---|---|---|---|---|---|---|
| V212 | REVISED | `Φ_w = DRAIN(b_w)` with `s_w(n) = 1/N`, `c_w(n) = Σ_{p∈n} wealth(p)^α_Φ / Σ_world wealth^α_Φ`, `b_w = s_w − c_w` — the §1.1 operator run once more with wealth as the good; `Φ_w` is the graph installed in the game. | MODEL | stipulated | V059 | V006 |
| V213 | NEW | `α_Φ = 1.5` is a stipulated design constant like `P₀`, calibrated once so the 1444 start yields the hangzhou/english_channel two-sink map; world-responsiveness flows through the wealth field, never through the knob. | DESIGN | stipulated | — | V212 |
| V214 | NEW | DRAIN orientation is scale-invariant in `b`: only the sign pattern and proportions matter, so any (−1, 1) normalization of node wealth yields the same graph. | MODEL | derivation | — | V212 |
| V215 | NEW | Measured on 1444 data at α_Φ = 1.5: exactly two sinks — `hangzhou` (wealth rank 3) and `english_channel` (rank 2); Phase 1 selects `genua`; both sinks arrive by stall promotion; `genua` ends a transit node. | MODEL | numerical test | — | V212, V213 |
| V216 | NEW | Measured on 1444 data: 8 sources, all cul-de-sacs; every node drains to a sink; acyclic; 159/159 edges oriented; 0 fallback promotions. | MODEL | numerical test | — | V215 |
| V217 | NEW | Measured: 0 edge flips and 0 sink-set changes under ±1% province-wealth noise across 5 seeds — stabler than any per-good graph. | MODEL | numerical test | — | V215 |
| V218 | REVISED | The installed graph is a legal DAG: `Φ_w` is a DRAIN orientation, acyclic by the marking-order argument, and its own marking order is a per-node scalar whose descending comparison reproduces the DAG (0 violations measured) — every consumer needing a potential still gets one. | MODEL | numerical test | C499, V061 | V212, V026 |
| V219 | NEW | Measured: `Φ_w` agrees with the per-good graphs on 53.4% of edge-goods (52.1% value-weighted) — lower than the superseded `Φ_ord`'s 62.7%; the static baseline for the §2.8 Φ_w-vs-realized measurement. | MODEL | numerical test | — | V212, V062 |
| V220 | REVISED | Why `Φ_w` is installed: the direction-dependent systems model power, not commodity logistics; vanilla's authored arrows encode empires pointing at the biggest cities; `Φ_w` computes that intent from the world state, and self-coherence with the per-good economy was knowingly traded for legible, wealth-anchored, world-responsive ends. | DESIGN | stipulated | V160, V161 | V212, V219, V221 |
| V221 | NEW | Vanilla's `00_tradenodes.txt` declares exactly three end nodes: `genua`, `venice`, `english_channel`. | ENGINE | file value | — | — |
| V222 | NEW | `Φ_ord`'s ends are sweep-scheduling artifacts, not places: of its 18 end nodes at 1444, 9 terminate no good and none of the demand capitals is among them, and its end count is α-invariant under the adopted key (9–17 measured across α up to 16). | MODEL | numerical test | — | V062 |
| V223 | NEW | Measured dynamics: dev-stacking `hangzhou`'s top province ×30 makes it the sole world sink; scaling European node wealth ×2 makes `genua` the sole sink; at ×3 the Cape of Good Hope reverses — Atlantic→Cape→Indian-Ocean drainage becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast. | MODEL | numerical test | — | V212, V213 |
| V224 | NEW | The `Φ_w` sink count is emergent and non-monotone in α_Φ (5→2→1→2→3→1 across α = 1…8 on 1444): it tracks how many world-class wealth poles the flow separates, not α itself. | MODEL | numerical test | — | V212 |
| V225 | NEW | A pure `wealth^α` edge comparison can never concentrate ends: a local wealth maximum survives every positive α (measured ≥10 ends at all α up to 16); a 3-mass gravity kernel over the top-3 pairwise-unconnected demanders hits any chosen count exactly with 69% vanilla-arrow agreement. | MODEL | numerical test | — | V221 |
| V226 | NEW | Pinned-count wealth fields (top-k seeding, gravity kernels) are rejected: they pin the end count by fiat — a world conquest could never merge the world into one basin — and need a second operator with its own reach knob γ; the emergent-count wealth good replaced them. | DESIGN | stipulated | — | V224, V225 |
| V227 | REVISED | `φ₀` as the installed graph, graveyard entry updated: the installed graph is `Φ_w` (v2.0 briefly used `Φ_ord`) and its correctness check is cross-implementation orientation equality. | DESIGN | stipulated | V196 | V064, V212 |
| V228 | REVISED | "The aggregate map is not a DAG" is still an error: the aggregate is a DAG because `Φ_w` is a DRAIN orientation (marking-order argument) whose own marking order is a per-node scalar reproducing it. | MODEL | derivation | V199 | V218 |
| V229 | REVISED | Solver item 5 closes with `Φ_w`: one more DRAIN run with wealth as the good — the 30th solve, same code path. | DESIGN | stipulated | V088 | V212 |
| V230 | NEW | A latent good leaves `Φ_w` unaffected: `Φ_w` reads wealth, not goods. | MODEL | derivation | — | V212 |
