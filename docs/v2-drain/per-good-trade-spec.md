# Per-Good Trade Network — Design Spec

**Version:** 2.1
**Status:** Living document
**Target:** EU4 (final patch, 1.37.5 Inca), extended timeline compatible, map-agnostic
**Lineage:** supersedes v1.3 (`../v1-laplacian/`). v1 oriented each good by a Laplacian
potential; its sink placement was shown to be topological rather than economic
(`../v1-laplacian/diagnosis.md`), and after a four-operator bake-off the orientation core was
replaced by the DRAIN algorithm (`drain-orientation.md`). Every claim-audit correction from
`../v1-laplacian/validation.md` settleable from files is folded in here. **v2.1** replaces the
installed aggregate: `Φ_ord` (the value-weighted marking order) gives way to **`Φ_w`**, DRAIN run
once more with wealth itself as the good (§1.6, §3.9).

Three sections. **§1 Mechanics** states what the system does. **§2 Implementation** states how it is built. **§3 Reasoning** states why, and records what is still unknown.

---

# 1. Mechanics

## 1.1 Trade direction

Every trade good has its own directed network over the same adjacency. Direction is computed, never authored.

For each good `g`, form the balance `b_g(n) = s_g(n) − c_g(n)` and orient by **DRAIN** — peel,
select, route, sweep:

**Phase 0 — peel to the 2-core.** Repeatedly remove degree-1 nodes, orienting each pendant edge
by the sign of its absorbed subtree balance (net exporter → toward core; net importer → fed from
core; zero → toward core) and folding the residual into the parent. Exact, not heuristic: every
removed edge is a bridge and flow on a tree is determined by conservation. On the vanilla map this
is a no-op (minimum degree 2, zero bridges); it exists for modded maps.

**Phase 1 — select the sink set.** Take the connected clusters of net demanders in the core,
compute the Herfindahl index of their demand masses, set `k = clamp(round(1/HHI), 1, |clusters|)`,
and select the heaviest demander of each of the top-k clusters. Knobs: a demand-mass quantile `ρ`
(cluster only the demanders covering the top-ρ of demand mass; default 1.0) and a cluster
dilation radius `r` (default 0). On vanilla 1444 demand is so ubiquitous that k = 1 for 27 of 29
goods at defaults; selection is deliberately weak because Phase 3 self-corrects upward.

**Phase 2 — route: min-cost b-flow.** Solve the uncapacitated min-cost flow with unit arc costs
serving `b_g`, and orient every support edge by its net flow. The support is a spanning-tree basis
(≤ N−1 edges) and is **acyclic by theorem**: with all costs 1, any directed cycle could be
cancelled for strictly lower cost. Edges with zero net flow are *free* and deferred to Phase 3.

**Phase 3 — gated drainage sweep.** Mark nodes Kahn-style: a node is *ready* when every flow
out-neighbour is already marked and it is a selected sink, has a flow out-arc, or has a free edge
to a marked node. Among ready nodes, pop by the deterministic priority key
**(DEF ascending, b ascending, index)**, where `DEF(v)` is total downstream demand on the
flow-arc subgraph (acyclic and fixed before any free edge, so no circularity). On a stall, promote
the heaviest flow-terminal demander into the sink set — the self-correction that supplies the real
sink count. Free edges then orient from later-marked to earlier-marked.

**Phase 4 — un-peel** the Phase-0 pendants in reverse.

Properties, all stated as checkable claims and all verified on 1444 data
(`drain-orientation.md`):

- **Global DAG.** Every arc points from later-marked to earlier-marked, so reversed marking order
  is a topological order; pendant edges are bridges and cannot close a cycle. Measured: acyclic
  29/29 goods.
- **Sink placement is explicit:** the final sinks are exactly
  `{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal demanders}` — 1–8 per good, mean
  3.6, on 1444 data. A node with no outgoing links for `g` is a **sink** for `g`; sinks differ per
  good; there is no global end node.
- **Reachability is a feasibility theorem, not an aspiration.** The orientation contains a flow
  serving 100% of every good's demand, because the LP imposes node balance. Measured: 100.0% of
  demand reachable from supply, 29/29 goods, zero orphan sinks.
- **Scan-invariance.** Ready-marking is a monotone closure, so the stall sequence, promotions and
  fallbacks are provably independent of scheduling; the priority key makes the remaining freedom
  (free-edge direction) a function of the graph and the balances alone. Measured: zero orientation
  changes under scheduler permutations; zero exact key ties.
- **Efficiency.** Unit costs make the certificate flow a fewest-hop routing.

Recomputed on a fixed monthly tick, aligned to the vanilla trade tick. Orientation is read from
the current solve every time, with no memory of the previous one. The LP is deterministic (six
identical solves, one orientation, on the reference implementation).

## 1.2 Supply

```
s(n,g) = goods_produced(n,g) / Σ_m goods_produced(m,g)
```

`goods_produced` is a physical quantity — pre-production-efficiency, pre-autonomy. It moves with devastation, occupation, and prosperity (`00_static_modifiers.txt`: `devastation`, `occupied`, `under_siege`, `prosperity` all carry `trade_goods_size_modifier`).

**No regularizer.** v1 mixed in `s ← (1 − ε)·s + ε/N` to keep dead branches from being oriented
by floating-point residual. DRAIN does not need it: free edges are oriented combinatorially by the
drainage sweep, not by comparing near-equal solved potentials, and a node with `b = 0` exactly
(one exists at 1444: `cape_of_good_hope`) is handled as an ordinary conduit. See §3.6.

## 1.3 Demand

Assembled per province, then summed to the node.

```
wealth(p) = tax_income(p) + production_income(p)
c(n,g)    = Σ_{p ∈ n} wealth(p)^α(g)  /  Σ_{q ∈ world} wealth(q)^α(g)
```

Unowned provinces generate no income and contribute nothing.

Autonomy floors are regime-dependent — there is no flat overseas floor in 1.37 (the 75% rule is
pre-Common-Sense). From `00_static_modifiers.txt`: a province in a **territory** is floored at
**90%** local autonomy (`territory_core` / `territory_non_core`), a **colonial core** at **50%**,
a **pasha state** at **20%**, a stated core at 0. The wealth pipeline applies the applicable floor
per province — a territory province contributes ~10% of its development's income, a colonial core
~50%.

## 1.4 Market concentration

```
α(g) = clamp( ( price(g) / P₀ )^k ,  α_min ,  α_max )        P₀ = 2.0 ducats
```

- **α > 1** — demand superlinear in provincial wealth. Luxuries concentrate on individually rich provinces.
- **α = 1** — demand proportional to economic size.
- **α < 1** — demand sublinear. Bulk goods spread toward populous regions.

α moves with vanilla price events in both directions. No smoothing.

## 1.5 Goods without a graph

**Gold.** Excluded by configuration — and it excludes itself from demand too. Gold-mine income
is its own income category in the engine (`INCOMEGOLD`, `gold_income` as a distinct scriptable
field), computed from mine value with its own constants (`GOLD_MINE_SIZE`), not booked as
production income. Under `wealth = tax_income + production_income`, gold income is therefore
**invisible to demand entirely** — not merely diverted. Gold is also inert in vanilla trade value
(`base_price = 0`, `goldtype = yes`), so the exclusion costs nothing. One residual observation:
whether the per-province production-income *field* nevertheless carries the gold figure before the
country-level split (§2.7 item 12).

**Any good with zero world production this month.** `s(n,g)` is undefined when nothing produces `g`, so the good has no graph, contributes nothing to the value weights (`V_g = 0`), and is absent from the survival table; `Φ_w` reads wealth, not goods, and is unaffected. It acquires a graph on the first month any province produces it. Latent goods behave this way for long stretches — coal produces nowhere at the 1444 start, and
its default trigger fires on **Enlightenment** (the Manufactories branches require special flags),
per province: `development_discounting_tribal = 20` or owner innovativeness 20, that province's
own institution progress at 100, and the owner having the institution. The 58 latent-coal
provinces therefore convert province-by-province over years, not in a single tick; the graph grows
as they do.

## 1.6 The aggregate graph

```
V_g     = price(g) · Σ_m goods_produced(m,g)     # per-good value weights (display, link values, AI)

wealth good:   s_w(n) = 1/N                       # uniform supply
               c_w(n) = Σ_{p ∈ n} wealth(p)^α_Φ / Σ_{q ∈ world} wealth(q)^α_Φ
               b_w    = s_w − c_w                  α_Φ = 1.5, a stipulated constant (§2.3)

Φ_w     = DRAIN(b_w)                              # the §1.1 operator, wealth as the good
```

**`Φ_w` is the graph installed in the game.** It is the §1.1 operator run once more with wealth
itself as the good: every node supplies uniformly, rich nodes are net demanders, so all wealth in
the world pulls edges toward itself — arrows point from wealthy nodes toward the wealthiest — and
the sinks are wherever the wealth flow terminates. Nothing pins their count; it emerges from
concentration exactly as per-good sink counts do. Only the sign pattern of `b_w` matters — DRAIN
orientation is scale-invariant, so any (−1, 1) normalization of node wealth yields the same graph.

Measured on 1444 data at α_Φ = 1.5: **two sinks, `hangzhou` and `english_channel`** (wealth ranks
3 and 2; Phase 1 selects `genua`, both sinks arrive by stall promotion and `genua` ends up a
transit node). Eight sources, all cul-de-sacs; every node drains to a sink; acyclic, 159/159
oriented, 0 fallbacks; **0 edge flips under ±1% wealth noise across 5 seeds** — stabler than any
per-good graph. Its marking order is a per-node scalar whose descending comparison reproduces the
DAG (0 violations), so every consumer needing a potential still gets one. Agreement with the
per-good graphs is 53.4% of edge-goods (52.1% value-weighted) — *lower* than the superseded
`Φ_ord`'s 62.7%; that trade is recorded in §3.9.

Dynamics, measured: dev-stacking `hangzhou`'s top province ×30 makes it the sole world sink;
scaling European node wealth ×2 makes `genua` the sole sink; at ×3 the Cape of Good Hope
**reverses** — 1444's Atlantic→Cape→Indian-Ocean drainage becomes
malacca/comorin_cape/zanzibar→Cape→ivory_coast. Sink count breathes with concentration
(transient extra sinks at intermediate boosts are expected behaviour, not noise).

The v1 diagnostic identity (`Φ ≡ φ₀` at α = 1) does not survive the operator change: DRAIN
performs no linear solve, so no linearity argument exists. Its replacement as the end-to-end
correctness check is **exact orientation equality** between the reference and DLL implementations
— a combinatorial comparison with no tolerance band (§2.8).

## 1.7 Merchants

Placement, range, and the collect/steer choice are vanilla. One merchant per country per node. A merchant present gives +2 trade power and +10% trade efficiency, node-wide, regardless of what it is doing.

**Collect** — vanilla, including the −50% penalty outside the home node.

**Steer** — the node window lists **every link incident to the node**. The vanilla window already
renders both an incoming and an outgoing link list as clickable entries
(`incoming_nodes_listbox` / `outgoing_nodes_listbox` in `tradeinterface.gui`, both populated by
the `TradeNodeLink` widget); what changes is **what an incoming entry does** — it must accept a
merchant assignment rather than merely navigate (whether the existing `NextNodeButton` already
accepts one is §2.7 item 14). A merchant assigned to link `{n,m}`:

- steers every good oriented `n → m`,
- is inert for every good oriented `m → n`,
- keeps its assignment when a link flips; only its active good set changes.

The same physical link can host a merchant at each end, active on disjoint good sets.

**Caravan power** requires the merchant to be steering at least one good on that link; assignment
alone does not qualify. This constrains only the two steering conditions — collecting at an inland
node as main trading port is untouched, since the change above does not affect collection. The
engine's own grant conditions are `merchant_present_inland` and `merchant_steering_to_inland`, and
its tooltip reads as granting the bonus **in the inland node**, not the adjacent one — §2.7
item 11 settles the recipient, and §3.11 carries both readings of the exposure surface.

## 1.8 Collection and transfer

Trade power and collect/transfer intent are node-wide. What varies per good is what they produce.

For each good `g` at node `n`:

```
collected_share(n,g) = 1                          if n is a sink for g
                     = P_collect / (P_collect + P_transfer(g))   otherwise
```

**Transfer eligibility is per good.** A country's power counts toward `P_transfer(g)` only if it has a merchant steering `g` at `n`, or it collects at some node reachable from `n` in `g`'s graph. Power that is neither is inert for that good.

**The remainder moves per good**, by the vanilla two-case rule.

*If any country steers `g` at `n`:* the outgoing value of `g` is divided across outgoing links in proportion to the modified trade power steering **toward each link**, not to power held in the node generally. Two consequences follow and both are load-bearing. An outgoing link with no steerer receives **nothing**, even when other links are steered. And a single steerer takes **all** of `g`'s outgoing value down its link, however little power it holds.

*If no country steers `g` at `n`:* the outgoing value splits evenly across `g`'s outgoing links.

*At `g`'s sink:* there is no remainder. 100% is collected and divided among collectors by trade power.

Vanilla gates still apply: trade range (which gates **merchant placement**, not value flow — no
mechanic gates flow by range) and no transfer into a node where nobody holds power at both ends.
There is no trade "supply range" in the engine; the only supply-range constructs are naval.

## 1.9 Trade power propagation

Preserved from vanilla, unchanged:

- A country whose provincial trade power in a node meets the threshold receives a share of it in **every** immediately upstream node. The share is `1 / TRADE_PROPAGATE_DIVIDER`. The threshold in raw power is `TRADE_PROPAGATE_THRESHOLD × TRADE_PROPAGATE_DIVIDER`, pending §2.7 probe 8 — see §3.13.
- Ship trade power propagates only where the country has a ship-propagation modifier, at the compounded rate: the propagation share multiplied by that modifier.
- Propagation is strictly one hop and never chains.
- A node receives the summed contributions of all its downstream neighbours.

Direction is read from `Φ_w`.

## 1.10 Direction-dependent systems

**Any mechanism gated on one nation being upstream or downstream of another evaluates TRUE.**

**Any node-pair direction dependency reads `Φ_w`.**

Where a gate scopes a set or a path, that scope reads `Φ_w`, with this fallback ladder:

1. `Φ_w` path.
2. If `Φ_w` does not connect, the shortest path within a single good's graph that does.
3. Undirected shortest path, only if no good connects them.

**Not gates: what moves anyway.** The mechanics below are unpatched and unchanged. Reorientation reaches them through the **trade power distribution**, not through any direction test — §1.9's propagation is direction-dependent, so a flip moves propagated power at both ends and changes fan-out across the neighbourhood. Nothing here is patched; all of it moves monthly.

Threshold mechanics that a shifted power share can cross:

| Mechanic | Threshold |
|---|---|
| Trade-conflict casus belli, target | `JUSTIFY_TRADE_CONFLICT_LIMIT` |
| Trade-conflict casus belli, actor | `JUSTIFY_TRADE_CONFLICT_ACTOR_LIMIT` |
| Privateer blocking | `MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER` |
| Trade company, extra merchant | `TRADE_COMPANY_STRONG_LIMIT` |
| Trade company, control | `TRADE_COMPANY_CONTROL_LIMIT` |
| Improve Inland Routes | 50% to establish, 40% to maintain — plus a merchant present in the node; waived entirely by the `free_improve_inland_routes` government attribute |
| Propagate Religion | 50% to establish **and 50% to maintain** in the default branch (a country-flag ladder runs 5–50; the terminal fallback is 35/35) — no band |

The banding is the reverse of what v1 recorded: **Improve Inland Routes is the one banded
mechanic; Propagate Religion has no band**, and every other listed threshold is single-valued. So
nothing absorbs threshold chatter on its own — a power share oscillating across any of these
limits flickers the mechanic, Propagate Religion included. Casus belli availability is the most
visible symptom, since it can appear and vanish month to month.

**Caravan power is in this group but is not a threshold mechanic.** It is a step function on raw power: it either applies or it does not, and when it applies it is worth up to the cap for any major power — enough to move a node's power shares by itself, and therefore to push *other* countries across the thresholds above.

**Scripted content.** No mission, decision, event, or trade company in 1.37.5 names a trade node
— zero non-comment references across all of `common/`, `missions/`, `decisions/`, `events/`;
trade companies are bare province lists. Scripted content reaches nodes only structurally:
`home_trade_node`, `any/random/every_active_trade_node`, `*_trade_node_member_province`, and
`highest_value_trade_node`. Nodes themselves never change under the mod — only connections do —
so the name-collision class of conflict is empty and the conclusion is *stronger* than v1 stated.
What remains exposed is the semantics: `highest_value_trade_node` and node-scoped triggers are
evaluated against a reoriented graph, so a mission written against vanilla's flow can change
*sense* without ever breaking. Accepted; listed for the compatibility pass rather than engineered
around.

## 1.11 Treasure fleets

The overlord always receives. The fleet routes by the §1.10 ladder, passing each node en route where privateers skim a share proportional to their power there.

Where the diversion mechanic is active, colonial gold income is diverted from the colonial
nation. It does not enter `wealth` at either end — though for the deeper reason of §1.5: gold
income is its own engine category and never enters `wealth` in the first place, diverted or not.

## 1.12 What the game displays

The in-game economy **is** the per-good economy. Node values, the node window, pie charts, the ledger, the economy tab, and tooltips all show the model's numbers.

**Trade map mode.** Provinces coloured by node, arrows between nodes, drawing `Φ_w`. Arrow weight from realized value crossing the link.

**Selecting a commodity.** Clicking a province switches province colouring to the vanilla trade-goods rendering for that good and redirects the arrow layer to that good's graph. A sink is visible as a node with no outgoing arrows. Clicking the node icon clears back to `Φ_w`.

**Not representable in the vanilla UI**, and shown in the companion overlay instead:

- Value broken down by commodity. The node window carries several node-level value fields
  (incoming / local / total / outgoing), but none takes a commodity argument — zero per-good
  fields, where thirty would be needed.
- A link's two-way traffic. One scalar per link, shown as net.
- Per-country effective trade power where eligibility differs by good. Shown as a value-weighted aggregate.

No new art, sprites, shaders, or map-mode chrome. Making the node window's existing incoming-link
entries assignable (§1.7) is the only UI change.

---

# 2. Implementation

## 2.1 Shape

One program: a runtime-attached DLL that each month reads live game state, solves per good, propagates the per-good economy externally, and writes the result and the orientation back into the engine's own structures. Ships with a generated `00_tradenodes.txt` for load time and a companion overlay for what the engine cannot display.

Windows/Steam. Non-ironman by choice: achievements are off with any mod
(`ACHIEVEMENTS_DISABLED_MODIFIED_GAME`), but the engine itself will load an ironman save in a
modded game (`Loading ironman in modded game` is a shipped code path) — the parsers target
non-ironman because ironman saves are binary-encoded, not because ironman is unavailable.

**Multiplayer is unsupported by default.** An identical build is necessary and not sufficient: EU4 multiplayer is lockstep with checksums, and an in-process floating-point solve can produce different results on different hardware — differing SIMD dispatch or accumulation order in the linear algebra is enough to desync. Supporting MP requires the computation to be bit-reproducible across machines. For DRAIN the
exposure is narrower than v1's dense linear algebra but still real: the min-cost-flow solve must
pivot identically given identical input (fixed arc ordering, one solver build, no threading), and
the sweep is already integer/combinatorial. Until that is built and verified, ship single-player
only.

## 2.2 Solver

1. Parser for `common/tradenodes/00_tradenodes.txt` — adjacency, `members`, `path`/`control` render data, `end`/`inland`/AI flags.
2. Parser for non-ironman saves — province owner, `base_tax`, `base_production`, trade good, goods produced, development.
3. Parser for `common/defines.lua`, merged with `common/defines/` overrides in load order (§2.3).
4. Per-province `wealth` (with the §1.3 regime-dependent autonomy floors), per-node
   `trade_value`, `s`, `c` with per-province α, and the per-good balance `b = s − c`.
5. DRAIN per good: min-cost b-flow (network simplex or LP), the deterministic drainage sweep,
   and the Phase-4 evaluator (`unserved` / `stranded`, which must be equal by conservation).
   Then `Φ_w`: one more DRAIN run with wealth as the good (§1.6) — the 30th solve, same code path.
6. Survival table `S_g[n][H]` for AI scoring — one table serving every country.
7. Mutual reachability census: 30 goods × 80 BFS, producing an 80×80 matrix whose entry counts goods with a directed path `n → … → m`.
8. Synthetic-shock harness: edit parsed province data and re-solve.

Cost per good is one uncapacitated min-cost flow on 80 nodes / 318 arcs plus an O(V+E) sweep —
milliseconds each with network simplex, tens of milliseconds for all 29 goods per monthly tick.

**Two implementations, one specification.** The list above is the reference solver: standalone, run against parsed saves, and the thing every validation in §2.8 is measured on. The shipped DLL carries a second implementation of items 4–7 in the host language, reading live memory instead of save files. They must agree — on **orientation exactly**, a combinatorial comparison with no tolerance band,
which replaces v1's identity check (§2.8) — and where they disagree the reference is correct by
definition. The parsers and the harness stay reference-only; the DLL never reads a save.

**Inland is derived, not trusted from the flag:** a node with no coastal province among its
`members`. The two disagree at exactly one node — `siberia` carries `inland=yes` but has two
Arctic-coast members (1781, 1782) — so derivation gives 25 inland nodes against the flag's 26.

## 2.3 Constants

Read at runtime; never hardcoded.

| Use | Define |
|---|---|
| Propagation share | `TRADE_PROPAGATE_DIVIDER` |
| Propagation threshold | `TRADE_PROPAGATE_THRESHOLD` — see §3.13 |
| Off-home collect penalty | `TRADE_NON_CAPITAL_OFFICE` |
| Home-node steering bonus | `TRADE_POWER_HOME_BONUS` |
| Merchant power / efficiency | `MERCHANT_MAX_POWER_BONUS`, `TRADE_MERCHANT_PRESENT` |
| Link boost base | `TRADE_ADDED_VALUE_MODIFER` |
| Caravan | `CARAVAN_FACTOR`, `CARAVAN_POWER_MAX`, `CARAVAN_POWER_MIN` |
| Trade capital move cost | `PS_MOVE_TRADE_PORT` |

Design constants: the excluded-goods list (defaults to gold), the α price anchor `P₀ = 2.0`,
the aggregate-graph exponent `α_Φ = 1.5` (calibrated so the 1444 start yields the two-sink
hangzhou/english_channel map, §1.6 — a constant like `P₀`; world-responsiveness flows through
wealth, never through this knob), and DRAIN's three knobs at their defaults — demand-mass
quantile `ρ = 1.0`, cluster dilation `r = 0`, and the zero-flow tolerance (numerical only,
`1e-11`). A measured calibration option
that moves all three plus α's clamp is recorded in §3.13; the baseline does not use it.

**DLC state is a third input axis.** Treasure-fleet diversion and caravan power are both DLC-conditional, and caravan modifier values are readable even when inert — so key on the DLC flag, never on the presence of a value.

## 2.4 The tradenodes file

Generated once from the campaign start date's `Φ_w`, then owned by the DLL in memory. No per-session regeneration; merchants are recalled only when the mod is rebuilt. A mid-campaign load runs on the start-date file for up to one month.

The engine performs no topological sort — the file must be one.

1. **Declaration order** — emit in decreasing `Φ_w` marking order. (The shipped vanilla file is
   itself topologically sorted sources-first — 0 of 159 links violate it — so this matches the
   observed convention; whether the engine *requires* it is §2.7 item 13's companion question.)
2. **End flags** — `end=yes` on every `Φ_w` sink (1444: two end nodes, `hangzhou` and
   `english_channel`, against vanilla's three); stripped from any former end node that gains outgoing links.
3. **Link reversal** — move the `outgoing` block, reverse the `path` province list, reverse the `control` pairs. Verify one hand-flipped link before writing generator code.
4. **Preservation** — `location`, `members`, `inland=yes`, `ai_will_propagate_through_trade`, and unrecognized keys round-trip byte-faithfully.

## 2.5 Runtime attachment

Pattern scanning and function hooking, following the EU4dll precedent, which provides the attach scaffolding on this binary but nothing about trade structures. Ship a runtime-patching DLL, not a modified executable. The binary is frozen — offsets found stay found.

Also hooked here: the nation-pair direction gates of §1.10, returned true at the call site rather than by forcing any shared predicate.

## 2.6 Writing to the engine

The monthly trade tick runs in three passes: static power and modifiers; a pass from the end nodes determining modified power and adding propagation; and a value pass from the origin nodes computing node value → collect/steer split → collect division → outgoing division with steering bonuses.

**Written each tick:**

| Field | Value |
|---|---|
| Node trade value | `Σ_g value_g(n)` |
| Node collectible pool | `Σ_g value_g(n) · collected_share(n,g)` |
| Per-link value | net `Σ_g` realized flow, in the installed `Φ_w` direction |
| Country trade income | derived by the engine from the above, unless stored |

Feeding the engine the collectible pool is sufficient, and the reason is narrower than it looks. `collect_pool` is itself per good on the inside — `collected_share(n,g)` depends on `P_transfer(g)`, which §1.8 makes commodity-specific. What factors out is the *other* term: `powershare_C` is a country's share **among collectors**, and whether a country collects is a merchant-or-home property with no good dependence at all. So a good-independent share multiplies a per-good sum, the sum collapses to one scalar, and the engine's own vanilla collection math reproduces every country's per-good income exactly. See §3.10.

**Two deadlines, not one window:**

- **Display** — immediately after the value pass. AI consumers read these figures during the month.
- **Payment** — bounded by the month boundary, since the treasury reconciles at the start of each month against the previous month's income.

Per-link values are written net, which can be negative where realized flow opposes the drawn arrow.

## 2.7 Probes

Items 1–10 are the v1 probe set, settled with a debugger on a vanilla install in one session —
though the claim audit found several are observable without one. Items 11–14 are new, need **no
debugger at all** (a save, a tooltip, or a single file edit), and three of them change what this
spec says rather than merely confirming it; do them first.

1. **Pass caching.** For each of the three passes independently: does flipping a link crash, produce stale-but-running values, or rebuild cleanly? Instrument for staleness — one-month corridor lag, value vanishing, tooltips disagreeing with arrows, propagation crediting the wrong side.
2. **Pass 2's content.** What imposes its ordering, given that propagation is one hop and cannot chain.
3. **Write windows.** Where income accumulation sits relative to the value pass; whether writing country trade income before month-boundary reconciliation makes AI budgeting and AI cash read the same figure.
4. **Negative link values.** Write one; observe arrow rendering and protect-trade allocation.
5. **Merchant storage.** Flip a link hosting a steering merchant — does the assignment dangle, reset, or crash?
6. **Caravan, twice.** Does the engine grant it for a merchant assigned to a link that is incoming in `Φ_w`? For one whose link carries no goods?
7. **Render data.** Is arrow render state separate from the economic link?
8. **`TRADE_PROPAGATE_THRESHOLD` semantics.** Set it to 4 and check whether the raw requirement doubles.
9. **Diverted gold.** Does diverted colonial gold still appear in the per-province production income field? Assert the DLC flag agrees with the observed field.
10. **Caller enumeration.** Disassemble and list every call site of "is X downstream of Y," classified as: return true; return true and define the scope; or compute per good. Produce the list as a written artifact, plus a companion "not members" list. (Static string-table analysis already yields three named sites: `DIPLO_SELLPROV_NOT_UPSTREAM`, `TREASURE_FLEET_TOOLTIP_CANT_REACH`, `TRADE_POWER_UPSTREAM` — both nation-pair gates compare trade capitals, and no colonisation refusal string exists.)
11. **Caravan recipient.** Merchant in a coastal node steering toward an inland one; read trade power in **both** nodes; whichever jumps by `min(dev/3 + modifiers, 50)` is the recipient. The engine tooltip and the identifier `merchant_steering_to_inland` both read as the **inland** node — if that holds, §3.11's exposure surface inverts.
12. **Per-province gold.** Open one gold province's Production income tooltip: does the per-province field carry the gold figure, or is it zero with gold only in the country's `INCOMEGOLD` line? One tooltip settles §1.5's residual.
13. **Cyclic node file.** Hand-author a two-node cycle in `00_tradenodes.txt`, load a fresh game, read `logs/error.log` and the trade mapmode. The *format* represents cycles fine; what §2.4 depends on is the **engine** rejecting or tolerating one, which is unverified and load-bearing.
14. **Incoming-link button.** In the vanilla node window, does an incoming `TradeNodeLink` entry accept a merchant assignment or only navigate? Decides whether §1.7's UI change is a behaviour change to an existing widget or a new interaction.
15. **Propagation source qualifier.** The engine tooltip says power transfers upstream "to trade nodes **where it already has power**" — a receiving-side qualifier §1.9 does not carry. Country with above-threshold power in X and zero in upstream Y: does it appear in Y? This line is §3.16's cautionary case; it has already been corrected once.

All writes land atomically at the tick hook with the sim paused.

## 2.8 Validation

| Case | Expected |
|---|---|
| Spice and cloves, 1444 | Source in Indonesia. Baseline DRAIN measured: spices sink at Genoa (demand rank 1) plus branch-end termini (Australia, Brazil); cloves at Venice, Kongo, Australia, Brazil. **China holds a spice sink only under the §3.13 α-calibration option** (which puts cloves at Beijing) — the v1 expectation of simultaneous China+Europe sinks is not the baseline behaviour |
| Most goods, 1444 | Sinks are `{selected ∩ flow-terminal} ∪ promoted` (§1.1) — 1 to 8 per good; high-demand nodes are sinks at 14% in the top demand decile vs 7% in the bottom (a barbell: LP branch ends land in poor pockets) |
| Malacca ↔ Cape, post-1500 | Spice routes Malacca → … → Cape → … → Europe |
| Malacca ↔ Cape, pre-1500 | Corridor withheld by range and the power-at-both-ends gate, not by direction |
| 1000 AD start | Sinks in the Muslim world and Song China, no era data |
| Razed China | Zeroing Beijing-node development relocates the sink in one solve |
| Ming loses the Mandate | Beijing's pull collapses with its income |
| Major war in China | Corridors shift for the duration, revert as devastation heals |
| Many poor provinces vs. few rich | Luxury demand goes to the rich-province node; bulk to the many-province node |
| Price crash | α falls below 1; regional sinks reappear |
| Caribbean, 1650 | Sugar production income makes it a sink for cloth, tools, wine |
| Kilwa, 1000 | Ivory income makes it a sink for Indian textiles |
| Consuming leaf | Terminates the DAG of every good it consumes but does not produce |
| Inert merchant | Its goods take the even split as if the node were empty; node-wide bonuses still apply |
| Node sinking spice but not cloth | Spice fully collected; cloth collected at the ratio with its remainder pushed |
| Near-balanced link | May flip monthly; carries near-zero either way; assignments survive |
| Two-way Atlantic corridor | Merchants at both ends, disjoint good sets, neither blocking the other |
| Economy tab vs. overlay | Every displayed trade figure matches the per-good economy to the ducat |
| Reachability | 100% of every good's demand reachable from its supply, asserted every tick; zero orphan sinks (an LP feasibility theorem — its failure means the implementation broke, not the world) |
| Conservation | Phase-4 `Σ unserved == Σ stranded` to machine precision, every good, every tick |
| Determinism | Re-running a tick reproduces the orientation bit-for-bit; promotions and fallbacks are scheduler-invariant (monotone closure) |
| Acyclicity | Asserted on every per-good graph, on `Φ_w`, and on the emitted file's declaration order |
| Colonization | Observer run to 1600: New World colonization proceeds at roughly vanilla pace |
| AI convergence | Greedy assignment settles with damping rather than oscillating |
| Latent good | A good with zero world production has no graph, no value weight, no survival-table entry; acquires all three the month production begins; `Φ_w` is unaffected throughout |
| Cross-implementation | The DLL and the reference implementation agree on **orientation exactly** for every save in the historical set — the primary end-to-end check, replacing v1's α = 1 identity |

**Measured, not asserted:**

- **Φ_w-vs-realized sign disagreement**, weighted by trade value, not link count. The static
  baseline is known — `Φ_w` agrees with the per-good graphs on 52.1% of value-weighted edge-goods —
  so the realized number has a floor to be compared against. Predicted to cluster at nodes with 3+ outgoing links and partial merchant coverage, thinning as coverage densifies.
- **Flip behaviour** per decade in peace versus war, and whether flips revert as occupation lifts.
- **Propagated-share change per node** on each flip, alongside the trade-power/in-degree covariance. This is what catches the §1.10 threshold mechanics flickering — a share crossing a single-valued limit is the failure mode, and casus belli availability the visible one. Total propagated power is not the quantity to watch: reorientation cannot change edge count, so `Σ indeg = |E|` is invariant and only the covariance moves.
- **Income balance, two metrics.** Total world collected income, and its distribution across historical great powers. Distribution is the gating one.

## 2.9 Build order

Not phases. Two tracks, run in parallel.

**Solver track** — the **defines parser first**: §2.3 makes every constant in the model a runtime read, so the eligibility threshold, the propagation share, the off-home penalty, the merchant bonuses and the caravan terms are all downstream of it and cannot be written correctly before it exists. Then the b-flow and sweep with their per-tick assertions (reachability, conservation, acyclicity, determinism); per-good eligibility; realized flows; the Φ_w-vs-realized disagreement measurement; the reachability census; the flip-rate measurement.

**Memory track** — the §2.7 probe session, all ten items on one trace.

**Then** — write §1.10's classified call-site list into the spec; gate income balance on both metrics; decide the negative-link display policy against a measured number.

---

# 3. Reasoning

## 3.1 Goals

1. **World responsiveness.** Trade direction follows the world's current state, never authored arrows. A horde razing Beijing moves the sink because the wealth moved.
2. **Realism.** Commodities flow differently. China is a silk source and a spice sink at once — impossible under one graph.
3. **Preserve the feedback loop.** Sinks accumulate, fund development, reinforce. This is how mercantile hegemonies form.
4. **Represent return flows.** Export regions historically imported manufactures. Vanilla cannot express this at all.
5. **Route-aware direction.** Direction must reflect where a good can ultimately reach, not which neighbour is richer.
6. **Zero authored data.**
7. **The game's own numbers are the model's numbers.** Anything reading trade income reads the real one.

## 3.2 Why a flow and a drainage sweep

Two families of orientation fail before this one, and both failures are theorems, not taste.

**Local comparison is monotone.** Orienting each edge by comparing its endpoints — wealth, or
`s − c`, or any node ranking — means no path can dip through a low-value intermediary and rise
again. Malacca → … → Cape → … → Europe requires exactly that dip. This killed v1's rank-orientation
strawman and it killed the tested `s − c` operator the same way: demand had to increase at every
hop, so one sixth of world demand became unreachable and Genoa was crowned a cloves sink that
cloves could not reach. Merchants cannot repair a wrong orientation — a merchant selects among
existing outgoing arrows, it cannot reverse one — so route-awareness has to live in the
orientation.

**A global potential solve puts sinks in the wrong place.** v1 oriented by the Laplacian potential
`L φ = s − c`. Its sink rule turns out to be exactly
`(c − s)/deg > mean(neighbour φ) − min(neighbour φ)` — verified on every (good, node) pair — and
because supply contrast exceeds demand contrast by four to five orders of magnitude, the
right-hand side is set by supply geography. Sinks landed where the field was locally flat, not
where demand was: the highest-demand node in the game was never a spices sink, a node with
literally zero demand outranked Genoa and Beijing, and deleting demand variation entirely left the
sink unmoved (`../v1-laplacian/diagnosis.md`). No parameter fixes it: α strong enough to matter
destroys §1.4's regime split, and better wealth inputs move the threshold by 1.7× where 4–5× is
needed.

**What survives from both, and what DRAIN keeps.** The conservation lesson: operators that impose
node balance somewhere (the v1 solve; a min-cost flow) serve 100% of demand as a *theorem*;
operators that don't (rank, seeded basins) strand it. DRAIN takes conservation from the b-flow —
reachability is LP feasibility, not an aspiration — and takes sink *placement* out of field
geometry entirely: sinks are the selected demand centres plus the flow-terminal drains any acyclic
drainage orientation would be forced to have anyway. The four claims v1 never stated, now stated
and checkable:

1. **Sink placement:** final sinks = `{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal
   demanders}`. Nothing else can be a sink (every other node is given an out-arc by the sweep).
2. **Free-edge direction:** marking order under the (DEF asc, b asc, index) priority — a function
   of the graph and the balances; zero exact key ties measured, so the index never decides.
3. **Reachability:** the orientation contains the LP certificate, so every unit of demand is
   servable; measured 100.0%, 29/29 goods, zero orphan sinks.
4. **Aggregate acyclicity:** `Φ_w` is itself a DRAIN orientation, so it is acyclic by the same
   marking-order argument as every per-good graph; the flow support by the cycle-cancelling
   argument. (Its marking order is a per-node scalar reproducing the DAG, for any consumer that
   needs a potential.)

Conduits still work: a node with `s = c = 0` (the 1444 Cape exactly) carries flow through — in-
and out-degree both nonzero for all 29 goods — and the corridor runs *through* the Cape, which is
the short route to Atlantic Europe (3 hops to the Channel against 7 via Alexandria; the flow
routes 24% of world spice supply through it, where v1's potential never used it at all).
Peripheral termini still exist — the LP's branch ends are consumed at the end of the line — and
value only arrives where someone holds power at both ends of the link.

## 3.3 Why wealth, and why per province

Demand is purchasing power, and purchasing power is income the game already computes. It captures return flows for free: a sugar island has negligible development but large production income, so it becomes a genuine consumer of cloth and tools. No colonial-nation dependency, no timeline restriction.

**Income is chosen for responsiveness, not stability.** It is not a slow quantity — autonomy drift is monthly, occupation halves goods produced for a war's duration, devastation and sieges bite in months, Ming's mandate swings enormously over years. That is deliberate. A besieged province genuinely buys less, so the volatility is economics rather than noise, and a trade map that ignored a decade-long war would fail Goal 1. Plan around the world, not around the graph: the map is legible, not unchanging.

**Trade income is excluded for circularity, not speed.** Including it would close a demand → orientation → flow → demand loop, making the graph respond to merchants' decisions rather than to the world. The loop still closes the long way: trade income funds development, development raises tax and production income.

**Per province, because node boundaries are an authoring artifact.** Node sizes run from 19 land
provinces (`cape_of_good_hope`) to 77 (`girin`) — a 4× spread with no structural rule behind it.
Raising a node's aggregate wealth to a power rewards node size, so luxuries would drain toward
whichever node the map authors sliced coarsest — at α = 1.5 a 77-province node beats a
19-province node of equal total wealth by 2× purely on slicing — Nippon (68 land provinces)
out-consuming the Paris node (`champagne`, 33) on count. With the exponent inside the sum,
superlinear demand concentrates where individual provinces are rich. At α = 1 the per-province and
node-aggregate forms coincide exactly.

## 3.4 Why supply is pre-modifier

Production efficiency does not conjure more cloves; it means the owner extracts more ducats from the same cloves. That is a fact about purchasing power and belongs in demand. Letting it into supply as well would say a province ships more to the world market because its owner picked Trade ideas — incoherent in a model whose thesis is that where a good comes from is what makes its trade its own.

This is also why the aggregate uses **trade value** rather than production income. The two are different quantities: a province's trade value is unaffected by production efficiency or local autonomy, and production income is defined by them. Substituting production income would make `V_g` — and with it the aggregate's weighting — depend
on owners' idea groups and autonomy, importing exactly the incoherence the previous paragraph
rejects. (In v1 the same substitution also broke the α = 1 identity, measured as orientation
agreement collapsing from 159/159 to 68/159; the identity is gone in v2 but the reason to refuse
the substitution is unchanged.)

## 3.5 Why α is anchored absolutely

Anchoring at 2 ducats rather than the price median means a good's market concentration moves only when *its own* price moves, and `k` becomes a pure sensitivity knob that doesn't shift the neutral point. Under a median anchor, a good could concentrate because some unrelated commodity got expensive — noise dressed as economics.

**α < 1 is a crash-reachable state, not a starting condition.** At vanilla base prices **nothing**
sits below the 2.0 anchor: the minimum tradeable base price is exactly 2.0 (fur, naval supplies,
slaves, tea, tropical wood, livestock sit on the anchor at α = 1 exactly; grain is 2.5, not the
1.25 v1 recorded — both of v1's figures were price/P₀ misread as prices). The sublinear regime is
entered only when a price event pushes a good beneath the anchor, and the shipped events answer
how often that can happen: **13 of 30 goods** can be pushed below 2.0 by a single vanilla
`change_price` event (grain and wine reach 0.625), and **11 goods have no negative price event at
all** and can never go sublinear in vanilla. That is the point of having the regime: without it a
crash could only fail to concentrate a market, never actively spread it. Whether it engages often
enough to earn its keep is now a bounded question (§3.13) rather than an open one.

α is deliberately mild. Production geography is what differentiates goods; α expresses only how concentrated a market is. A mechanism strong enough to reshape orientation would let price fight geography for control of the graph.

## 3.6 Why no hysteresis, and why there is no ε

**A margin on orientation is a correctness bug, not a tuning knob.** Holding an edge against the
current month's result splices orientations decided at different times, and a splice of two
acyclic orientations need not be acyclic. Tested in v1: with tol = 1e-3 and values
{0, 0.0006, 0.0012}, tolerance-based tie-breaking turned an acyclic prior into **A→B→C→A**. One
correction to how v1 stated the stakes: the node-file *format* represents cycles perfectly well —
it is a list of named directed links with no acyclicity constraint. What the design depends on is
the **engine's** behaviour on a cyclic file, which is unverified and load-bearing: §2.7 item 13 is
the one-file-edit test, and until it runs, acyclicity is enforced because we cannot prove the
engine tolerates its absence.

Nothing needs to stop churn. A link whose flow-support membership alternates month to month
carries near-nothing either way, and merchant assignments are to links, so they survive flips
untouched.

**v1's ε is deleted, because the problem it patched no longer exists.** The Laplacian oriented
dead branches by comparing solved potentials that were mathematically equal and differed only by
floating-point residual — so orientation varied by machine, and a field-level regularizer was
needed to break ties on purpose. DRAIN's free edges are oriented combinatorially: the priority
sweep's key (DEF, b, index) is computed from exact input data, the measured count of exact key
ties on 1444 data is **zero**, and the LP itself is deterministic (six identical solves, one
orientation). Determinism is asserted per tick (§2.8) rather than approximated by a nudge. What
replaces the ε-magnitude question in §3.13 is the cross-machine question: the LP must pivot
identically on identical input for multiplayer (§2.1).

## 3.7 Why eligibility is per good

Vanilla's rule: effective trade power counts only countries which collect or transfer downstream, and not those whose trade capital is upstream. Power in a node not upstream of anywhere you collect is inert — neither retaining nor transferring.

Under a per-good model, "downstream" is per good. At a node where your home is downstream for cloth and upstream for spice, your power counts for one and not the other. This is what keeps the design honest: it returns true for *some* goods at every node, so no nation is ever globally inert, while still preventing a nation's power from shoving a good away from where it collects that good. Forcing it true for all goods at once would not be "everyone is upstream and downstream" — it would be "direction doesn't exist," which inflates transfer power everywhere.

The common misstatement — that any non-collecting country with trade power is transferring — is the loose community summary and is wrong.

## 3.8 Why gates evaluate true

The vanilla gates encode an assumption that a nation pair has one global relationship to trade: upstream or downstream. Under thirty graphs that assumption is not inconvenient, it is false. Every province is upstream for some good, because a region that receives your cloth ships you its furs. There is no fact of the matter for the gate to test, so the honest fix is to stop consulting it rather than to engineer the graph so it happens to pass.

**Node-pair dependencies are different and keep reading `Φ_w`.** Propagation is a relation between two nodes, not two nations. Setting it true would grant every country propagated power into every neighbour and multiply trade power across the map. This distinction is easy to miss and expensive to get wrong.

**Verified not members, recorded now rather than deferred.** Propagate Religion is node-local — it
establishes a centre of conversion in the node's own province — but v1's "gated on a trade-power
threshold there and nothing else" was wrong, and it was one of only three claims carrying
`verified (method unstated)` provenance. The shipped policy file gates it on the trade share
**and** the node being in a trade company region **and** a merchant present **and** a
religion-group/flag disjunction **and** `dominant_religion`, with `unique = yes` per node. What
the family does share, and what matters here, is the absence of any direction test: no trading
policy anywhere in `00_trading_policies.txt` tests upstream/downstream. Three of the five policies
have no trade-share threshold at all (merchant-present only). This is written down because the
deferred artifact does not exist yet, and a community restatement of the "downstream target" claim
would otherwise put direction tests back.

**Scopes read `Φ_w` rather than any-good reachability.** A gate is a boolean; a scope is a set or a path, and answering a scope question with any-good reachability is an enormous buff. `Φ_w` is the graph the engine already walks, so those call sites are left alone — which collapses the shared-predicate risk. It is legible: one map predicts where fleets sail. And it is balanced: area-effect mechanics scoped by any-good reachability would cover most of the map — measured, 98.8% of ordered node pairs are connected by at least one good on 1444 data.

## 3.9 Why `Φ_w` is the installed graph

The installed graph exists for the engine's direction-dependent systems — propagation, fleet
routes, upstream/downstream scopes — and those systems model *power*, not commodity logistics.
What vanilla's authored arrows encode is empires pointing at the biggest cities and richest
areas, with three authored ends (`genua`, `venice`, `english_channel`). `Φ_w` computes that
intent from the world state instead of authoring it: all wealth pulls (a rich non-sink node —
Beijing, Champagne, Sevilla — bends every edge around it as a net demander even though flow
passes through), the wealthiest places win, and the ends emerge and move when the wealth moves —
a razed Beijing, a dev-stacked capital, a colonizing Europe that flips the Cape (§1.6). It reuses
the §1.1 operator unchanged: one implementation, one set of guarantees (LP feasibility,
acyclicity, determinism, scan-invariance), and the correctness check stays a single combinatorial
comparison.

Three aggregates were tested; one is impossible and one was superseded:

- The value-weighted **net flow** `Σ_g V_g·net_g` is a flow, flows circulate, and it measurably
  contains directed cycles — it cannot be installed.
- The value-weighted **marking order** `Φ_ord = Σ_g V_g·order_g` (v2.0's choice) is acyclic for
  free and remains the most self-coherent aggregate measured: 62.7% edge-good agreement with the
  per-good graphs against `Φ_w`'s 53.4% (52.1% value-weighted). It was superseded on design
  grounds: its ends are artifacts of sweep scheduling rather than places — of its 18 end nodes at
  1444, 9 terminate no good at all and none of the demand capitals is among them — and its end
  count is essentially un-steerable (α-invariant under the adopted key; measured 9–17 ends across
  α up to 16). Self-coherence was traded for legible, wealth-anchored, world-responsive ends.
- `Φ_w`, adopted: two vanilla-like ends at 1444 that move with the world, from the same operator
  the goods already use.

Note what `Φ_w` is **not**: a difference in `Φ_w` across a link is *not* the net value crossing
it. Realized movement follows vanilla propagation — a good can be diluted by an even split across
three links while another gets winner-take-all steered the other way — so a link can be oriented
`n → m` under `Φ_w` while realized net flow runs `m → n`. That is why the disagreement rate is
measured rather than assumed, and why display policy for negative link values is a decision
deferred to data. Link values are realized flows, which makes conservation hold by construction.

## 3.10 Why the engine's economy is overwritten

Paying countries correctly while leaving the display wrong is a strictly weaker position: node values, pie charts and the ledger would describe an economy nobody is playing, and AI light-ship building, trade-league behaviour, peace valuation and income-threshold events all read those figures.

The engine's data model turns out to be sufficient at node level, for a narrower reason than it first appears. `collect_pool` is per good on the inside, since `collected_share(n,g)` depends on `P_transfer(g)` and §1.8 makes transfer eligibility commodity-specific. What factors out is the other term: `powershare_C` is a country's share **among collectors**, and whether a country collects is a merchant-or-home property with no good dependence. A good-independent share multiplying a per-good sum collapses to one scalar:

```
income_C(n) = Σ_g value_g(n) · collected_share(n,g) · powershare_C(n)
            = powershare_C(n) · collect_pool(n)
```

Verified numerically: agreement to 5.7e-14 across a node with mixed sinks, mixed collectors and the home-node penalty in play. So one scalar per node reproduces every country's income exactly, and the engine's own math does the rest.

**This is also why propagation cannot be made per good.** Tested: with propagation reading the one installed graph, the node-scalar model reproduces per-good truth to 1.4e-14. With power varying by good, it is off by 5.96 ducats on a node paying ~250 — because `powershare_C` stops factoring out. Keeping propagation on a single graph is load-bearing for Goal 7, not merely convenient.

Only the *decomposition* by good exceeds what the engine can hold.

## 3.11 Why caravan power needs a condition added

In vanilla, **steering** is outgoing-only — trade cannot be steered upstream at any amount of
power ("You can never steer trade upstream or past your Main Trade City", the engine's own hint).
The *display* is not: the node window already lists incoming links as clickable entries (§1.7).
But since only outgoing links can be steered, "assigned" and "steering" are the same condition,
and the engine never had to distinguish them.

§1.7 makes incoming entries assignable and pulls the two apart. The engine's caravan grant fires
on `merchant_present_inland` or `merchant_steering_to_inland`, with nothing checking whether value
moves. Its tooltip reads as granting the bonus **in the inland node** ("steers towards an inland
trade node will give you extra trade power *in that node*") — the opposite of v1's reading that
steering from Crimea to Kiev pays out in Crimea. §2.7 item 11 settles it with one merchant and two
node windows; the exposure surface is either the ~26 inland nodes themselves (tooltip reading) or
every node adjacent to one (v1 reading) — smaller and differently shaped under the first, and
§1.7's added condition is the right guard under both. Caravan power is total country development
÷ 3 **plus policy and idea modifiers**, clamped to [2, 50]; nineteen countries are at the cap from
raw 1444 development alone (Burgundy, Korea, the Timurids and Portugal start 2–10% short and reach
it with any caravan modifier), and it does not scale with node presence at all.

Requiring the merchant to steer something **restores the vanilla state of affairs**. Granting on
bare assignment would be the deviation, and an unintended one.

## 3.12 Why treasure fleets are always granted

The argument is consistency with §3.8: the gate compares two trade capitals on a graph where the
nation-pair relation has no single truth value, so it is not consulted. v1 claimed a stronger
argument — that the gate is bistable, denial raising the colonial node's wealth and granting
lowering it, locking campaigns into whichever state they started in. **That argument is deleted:**
gold income never enters `wealth` at all (§1.5 — it is its own engine income category), so neither
granting nor denial moves the demand vector, and there is no direct feedback to be bistable. The
engine's own denial branch confirms what denial does: "They will keep their gold income instead."
A slow, second-order version survives — kept gold spent on development raises `base_tax` and
`base_production` years later — but a multi-year indirect loop is not a bifurcation and does not
carry the design decision. Consistency carries it alone.

Two consequences priced in advance. Inflation scales with money received relative to economy size, so universal granting hits small previously-cut-off colonizers hardest. And the route rule is a balance dial, since privateers skim per node passed — which is why hop counts are compared between candidate rules on the mod's own graph rather than against vanilla's, that being a counterfactual on a graph we have replaced.

## 3.13 Open questions

**Prose-sourced — distrust, build nothing on them.**

- Colonization's gate shape. The evidence is one mod author's report, contradicted in-thread, and the observed behaviour needs no gate at all: if colonial nodes route away from the AI's home, expected trade income collapses and low-scoring provinces don't get colonized. Static string-table analysis now leans the same way — the only direction-refusal strings in the binary belong to sell-province and treasure fleets, none to colonisation. The caller enumeration must still be able to return "no colonization gate exists" as a *successful* result.

**Derived — probably right, cheaply falsifiable.**

- `TRADE_PROPAGATE_THRESHOLD` semantics. The file value and the documented raw requirement differ by exactly the propagation divider, which reconciles if the threshold is expressed in propagated units. Falsify by doubling the define.
- Pass 2's ordering requirement. Propagation is one hop and cannot chain, so something else in that pass imposes it; eligibility resolution is a backward reachability from collection points and is the only candidate named. An argument from exhaustion, and our inventory has been wrong before — §2.7 probe 2 settles it.

**Debugger-only — a shorter list than v1 believed.** Of §2.7, only pass caching, pass-2 content,
write windows and the caller enumeration truly need the debugger. Items 11–15 need a save, a
tooltip, or one file edit; the propagation-threshold and one-hop questions are node-window reads.
Do the cheap ones first: three of them (caravan recipient, cyclic file, incoming-link button)
change what this spec *says*.

**Calibration, and unresolved parameters.**

- `k`, `α_min`, `α_max`. The test is whether they produce the intended three-regime split, not whether they differentiate same-geography goods, which they are not meant to do.
- Does `α_min` ever bite? Bounded from files now (§3.5): the sublinear regime is reachable through
  vanilla price events for 13 of 30 goods and unreachable for 11. Whether those events fire often
  enough in a real campaign remains the open half.
- **The sink-count-span option.** A measured calibration exists that makes sink counts track price
  — span exactly 1..5, spearman(price, sinks) = −0.54: α unclamped at exponent 2 (cloves α = 16),
  demand-mass quantile ρ = 0.5, twig tolerance 3e-4 (`drain-orientation.md` §5–6). Its costs are
  real and recorded: unclamped α² is a *demand-model* decision (luxuries become court goods —
  Beijing, holding the richest single province, becomes the cloves sink), the tolerance sacrifices
  min-cost routing on <0.03% of mass and drops one good's reach to 99.97%, and it is one-snapshot
  tuning. The baseline does not adopt it; adopting it is a §1.4 decision, not a solver knob.
- LP determinism across machines: the min-cost-flow solve must pivot identically on identical
  input (replaces v1's ε-magnitude question; see §2.1 and §3.6).
- AI merchant reassignment cadence (§3.14).

## 3.14 AI merchant assignment

The two ends of a link never compete: a merchant at `n` on `{n,m}` moves goods oriented `n→m`, one at `m` moves goods oriented `m→n`, disjoint sets. Competition stays where vanilla puts it — between merchants at the same node.

**One precompute serves every country.** For each good, a backward pass over its DAG gives `S_g[n][H]`, the expected fraction of a unit of `g` at `n` arriving at `H`, multiplying through collection, steering shares, and the per-link multi-merchant boost. `collected_share(n,g)` reaches 1 at `g`'s sink, which terminates the recursion. All three inputs are country-independent aggregates, so this is one table, not one per nation — about 0.75 MB, well under a million operations per solve.

Scoring reads that table for both steering and collecting, so the opportunity cost of collecting falls out as the same comparison a human player makes by hand. Denial scoring falls out of the same table against a rival's home node.

**The off-home penalty is a power modifier, not a haircut on value.** It reduces the country's trade power in that node, and that reduced power then feeds *both* the collect/transfer ratio and the share among collectors — so it lowers the fraction retained in the node *and* the collector's slice of it. Scoring a collect candidate as `value × share × 0.5` is wrong; the halving must be applied to power and the two-stage formula run from there. This is also why the penalty "falls out" of the survival table at all: the table is built from power-derived shares.

**Two things resist naive greedy scoring.** The home-node bonus is voided entirely by placing any collector outside the home node, so a collect candidate's true cost includes a penalty no single-merchant score can see — run the greedy twice, once all-steer with the bonus, once unconstrained without, and keep the better portfolio. And greedy against a moving field can oscillate between AIs; damping the shares between passes should hold it, and the prototype must verify.

**Reassignment cadence is undecided and is the one item left for the human.** Merchants take travel time, so an AI re-optimizing every solve leaves them permanently in transit. Two options:

- **Mirror vanilla's cadence.** The stated preference. The relevant define was not located in the visible portion of any dump, so this requires finding it or measuring it by observation.
- **Compute it.** Move when `(V_new − V_incumbent) × expected_tenure > V_incumbent × travel_time`, using `MERCHANT_SPEED` and the survival table, both of which exist. `expected_tenure` is endogenous and should be wired to the flip-rate measurement.

The argument for computing: vanilla's cadence, whatever it is, was tuned against a graph that never moves, so copying it would import a constant fitted to different dynamics. The argument against: it overrides a stated preference, and node-to-node travel time still needs the game's distance metric.

## 3.15 Rejected

**The v1 Laplacian potential as the orientation core.** Its sink placement is topological:
sinks land where the field is locally flat, demand enters only as `(c−s)/deg` against the local
spread, and supply contrast (10⁷) drowns demand contrast (10²–10³). Diagnosed, measured, and
replaced (`../v1-laplacian/diagnosis.md`, `drain-orientation.md`). What it did guarantee —
100% reachability via conservation, exact conduit behaviour — DRAIN keeps by construction.

**Pure min-cost-flow orientation (no sweep).** Orients only the ~79-edge support (a spanning-tree
basis), leaving half the map undirected, and its value-weighted aggregate contains directed
cycles. DRAIN is exactly this plus the drainage completion that fixes both.

**Ranked orientation (`score = s − c`, harmonic extension on empty nodes).** Wins every sink
statistic and fails the one that matters: it is monotone (§3.2), so demand must rise along every
route — 83% of demand reachable, 34 orphan sinks, Genoa a cloves sink that cloves cannot reach.

**Seeded basin growth (multi-source Dijkstra with balance feedback).** Flow converges to the
chosen seeds and starves everything off a supply→seed path; 88.5% reach at its best tuning. Its
useful ideas — HHI-adaptive sink count, stall self-correction — survive inside DRAIN's Phases 1
and 3.

**DEF-descending free-edge priority** (point free edges toward downstream demand). Sounds
principled, measurably worse: on the certificate, *unmet* demand is identically zero, so DEF is
total demand, and pointing free edges into already-served subtrees strands greedy flow. The
adopted key is DEF-ascending (`drain-orientation.md` §6).

**Authored demand weights.** Authored data in a model that needs none.

**Trade income inside `wealth`.** Reintroduces flow → demand → orientation → flow circularity; the graph would respond to merchants rather than to the world.

**Node-level α.** Makes demand concentration a function of how finely the map was sliced.

**Median-relative α anchor.** A good's concentration would shift because other goods changed price.

**α floored at 1.** Discards the cheap-bulk regime.

**Production income as the aggregate supply term.** Makes world supply depend on owners' idea groups (§3.4). Its v1 second strike — breaking the α = 1 identity — is moot with the identity gone; the first strike suffices.

**A τ margin on orientation.** Manufactures cycles (§3.6).

**Uniform supply in the aggregate solve.** *(v1 entry, moot in v2 — retained for history.)* It
answered a question nobody asked and destroyed the identity that made `φ₀` worth computing; both
`φ₀` and the identity left with the Laplacian.

**`φ₀` as the installed graph.** *(v1 entry, moot in v2.)* It was not the economy the model runs;
the installed graph is `Φ_w` (v2.0 briefly used `Φ_ord`) and its correctness check is
cross-implementation orientation equality.

**`Φ_ord = Σ_g V_g·order_g` as the installed graph.** *(v2.0 entry, superseded in v2.1.)* The
most self-coherent aggregate measured (62.7% vs `Φ_w`'s 53.4%) and still acyclic for free — but
its ends are sweep-scheduling artifacts, not places (§3.9), and no parameter steers their count.
Retained as the measured coherence ceiling any future aggregate should be compared against.

**Pinned-count wealth fields (top-k seeding, gravity kernels).** Tested en route to `Φ_w`: a
3-mass gravity field `Φ(n) = max_m c_α(m)·γ^dist(n,m)` over the top-3 pairwise-unconnected
demanders hits any chosen end count exactly and 69% vanilla-arrow agreement. Rejected: it pins
the end count by fiat (a world conquest could never merge the world into one basin), needs a
second operator with its own reach knob γ, and a pure `wealth^α` edge comparison without a reach
term can never concentrate ends at all — a local wealth maximum survives every positive α
(measured: ≥10 ends at α up to 16). The emergent-count wealth good replaced it.

**A vestigial in-game economy with net treasury settlement.** Correct treasuries, wrong displays, wrong AI inputs (§3.10).

**Per-good propagation.** Breaks the income factoring and with it Goal 7.

**Node-level collect/transfer rules.** The collect/transfer split is per good because whether a good has anywhere to go is per good.

**Treating unsteered goods as fully collected.** Transfer power does not come from merchants; full collection happens at a sink, which is a property of the graph.

**Undirected shortest path as the primary fleet route.** A geodesic over a directional structure can route a fleet against every arrow on the map.

**Automatic per-good merchant targeting.** One vanilla arrow click already achieves per-good resolution, and automation would cost denial steering.

**Companion-overlay merchant assignment.** Assignment must stay a game action or vanilla knowledge stops transferring.

**Emission-time pruning of near-flat links.** Peripheral termini are intended consumption, and
the power-at-both-ends gate already withholds unworked corridors. (The §3.13 calibration option's
twig tolerance is a bounded, measured exception to this stance — rejected at baseline, available
as a deliberate trade.)

**Edge conductance / weighted Laplacian.** v1 rejected it as "too much mechanical surface" —
the audit showed the unweighted metric was in fact the *cause* of v1's sink misplacement, and the
honest options were to weight the metric or replace the operator. The operator was replaced;
conductance stays rejected because there is no longer a Laplacian to weight.

**Staged delivery.** The intermediate states are different designs sharing a solver, not subsets of this one.

**"The aggregate map is not a DAG."** Still an error, with v1's *reason* corrected: v1 defended
it by claiming net flow is the gradient of `Φ` — contradicting its own §3.9, and false (the
value-weighted net flow measurably contains cycles). The aggregate is a DAG because `Φ_w` is a
DRAIN orientation (acyclic by the marking-order argument) whose own marking order is a per-node
scalar reproducing it — which is what makes an installable single network exist at all.

## 3.16 Evidence standard

v1 carried an evidence standard — "every retraction traced to a premise that entered through
prose; nothing built on adjacency data, file values, or the model's own equations failed" — and
the claim audit **refuted the standard itself**. At least fifteen non-prose claims failed, by
three distinct mechanisms:

1. **File values remembered from an older patch.** The 75% overseas autonomy floor is
   pre-Common-Sense; 1.37 has regime floors of 90/50/20/0.
2. **File values transformed and then reported as raw.** v1's grain (1.25) and livestock (1.00)
   base prices are exactly `price / P₀` — the ratio was computed and then written down as the
   price.
3. **The spec's own algebra instantiated without checking the instantiation.** ε provably
   preserved the α = 1 identity only if applied to `φ₀`'s supply as well; implemented as written,
   the identity failed at 1e-5 and would have been diagnosed as a solver bug.

And one of only three claims carrying `verified (method unstated)` provenance — Propagate
Religion's gating — turned out wrong. The real signal in the audit was **provenance**: nine of the
fourteen refuted engine facts were UNSOURCED. So the rule is not "trust derivations" and not
"distrust prose". It is: **anything that entered without a recorded source is the risk, whatever
it looks like once written down.** Every engine fact in this spec must carry its source — a file
path, a binary string, or a named observation — and a claim without one is a to-do, not a fact.

**The gap that mattered more than any refutation.** v1 never stated what determines sink
placement — so the claim inventory had nothing to extract, the validation had nothing to refute,
and the model shipped with a fatal placement flaw that claim-checking structurally could not
catch. The audit found it only by running the solver and asking why the output looked wrong. The
standing repair is in this document's structure: the properties that matter are now stated as
checkable claims — what determines sink placement (§1.1, §3.2), what determines free-edge
direction (§1.1, §3.2), what guarantees reachability (§1.1: LP feasibility), why the aggregate is
acyclic (§1.6, §3.9), and why the result is scheduler-invariant (§1.1: monotone closure). Each is
provable, each is asserted at runtime (§2.8), and each is exactly the kind of sentence whose
absence hid the last flaw. The next audit's first question should be: **which property of the
output does this spec still not state?**

The v1 cautionary case is retained because it is not yet closed: the propagation source condition
was corrected once (ship propagation under its modifier), defended by two reviewers against the
wrong error — and the engine's own tooltip carries a *second* qualifier ("where it already has
power") that §1.9 still does not, pending §2.7 item 15. A line can be confidently defended against
one mistake while carrying another; agreement between reviewers is not verification.
