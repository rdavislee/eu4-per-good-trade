# Per-Good Trade Network — Design Spec

**Version:** 3.0
**Status:** Living document
**Target:** EU4 1.37.5 Inca. Extended-timeline compatible. **Connected maps only** — see §2.2.
**Lineage:** supersedes v1.3 (`../v1-laplacian/`). v1 oriented each good by a Laplacian
potential; its sink placement was shown to be topological rather than economic
(`../v1-laplacian/diagnosis.md`), and after a four-operator bake-off the orientation core was
replaced by the DRAIN algorithm (`drain-orientation.md`). Every claim-audit correction from
`../v1-laplacian/validation.md` settleable from files is folded in here. **v2.1** replaces the
installed aggregate: `Φ_ord` (the value-weighted marking order) gives way to **`Φ_w`**, DRAIN run
once more with wealth itself as the good (§1.6, §3.9).

**v3.0** makes three changes. (a) **Wealth becomes owner-agnostic** — it is a property of the
place, not of who holds it: no autonomy, no production efficiency, no ideas, no owner modifiers
(§1.3, §3.3). (b) Every refutation and partial in `../v2-drain/validation-v2.md` is folded through,
including four v1 corrections that v2 never applied. (c) The four game probes settled in
`../v2-drain/game-session.md` are applied, two of them reversing v2's stated position (§2.4, §1.9).
Deleted text is quoted in `changes-v3.md`. Every measured number carries the script that produced
it; anything not regenerated for v3.0 is marked **[unverified in v3.0]**.

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
of ≤ N−1 edges **when the solver returns a basic (vertex) optimum**, which the simplex family
does; an interior-point solve without crossover can split flow across equal-length parallel paths
and return a support with an undirected cycle in it. §2.2 therefore requires network simplex or a
simplex LP. What holds for *any* optimum is the weaker and sufficient property: the support
contains **no directed cycle**, because with all costs 1 a directed cycle could be cancelled for
strictly lower cost. Edges with zero net flow are *free* and deferred to Phase 3.

**Phase 3 — gated drainage sweep.** Mark nodes Kahn-style: a node is *ready* when every flow
out-neighbour is already marked and it is a selected sink, has a flow out-arc, or has a free edge
to a marked node. Among ready nodes, pop by the deterministic priority key
**(DEF ascending, b ascending, index)**, where `DEF(v)` is total downstream demand on the
flow-arc subgraph (acyclic and fixed before any free edge, so no circularity). On a stall, promote
the heaviest flow-terminal demander into the sink set — the self-correction that supplies the real
sink count. Free edges then orient from later-marked to earlier-marked.

**Phase 4 — un-peel** the Phase-0 pendants in reverse.

Properties, all stated as checkable claims and **measured where measurement applies**
(`drain-orientation.md`; regenerated for v3.0 by `v3measure.py`). Where a property is proved for
any input the proof is named; where it is only measured, it says so and names the premise that
would be needed; and where it follows from the construction so directly that no measurement could
confirm or refute it, it carries none and says that too. **The three are never allowed to stand
for each other** — that discipline is what caught four over-claims between v2.0 and v3.0.

- **Global DAG.** Every arc points from later-marked to earlier-marked, so reversed marking order
  is a topological order; pendant edges are bridges and cannot close a cycle. Measured: acyclic
  29/29 goods.
- **Sink placement is explicit.** Every sink is either a selected demand centre that turned out
  flow-terminal, a stall-promoted flow-terminal demander, or a Phase-0 pendant that absorbed a
  net-importing subtree. On a map where Phase 0 is a no-op the third case is empty and the sink
  set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods on 1444,
  1–8 sinks per good, mean 3.6. **That equality is not a theorem in general**, and v2 asserted it
  as one. Two constructed cases break it: a pendant net-importing leaf is a sink outside the set,
  and inside the 2-core a selected flow-terminal demander can be handed an out-arc by a free edge
  to an earlier-marked node and cease to be a sink. Both are worked in §3.2. A node with no
  outgoing links for `g` is a **sink** for `g`; sinks differ per good; there is no global end node.
- **Reachability is a feasibility theorem on a connected map.** The orientation contains a flow
  serving 100% of every good's demand, because the LP imposes node balance and `Σ_n b_g(n) = 0`
  identically (both `s` and `c` are world shares). The premise that makes the LP *feasible* is
  connectedness: on a disconnected map the balance must hold per component, and share
  normalisation does not deliver that — a two-component graph with cross-component imbalance is
  infeasible outright. §2.2 states the connectedness requirement and what the solver does when it
  is violated. Measured on 1444, which is one component: 100.0% of demand reachable from supply,
  29/29 goods, zero orphan sinks.
- **Scan-invariance.** Ready-marking is a monotone closure, so the stall sequence, promotions and
  fallbacks are provably independent of scheduling; the priority key makes the remaining freedom
  (free-edge direction) a function of the graph and the balances alone. Measured: zero orientation
  changes under scheduler permutations; zero exact key ties.
- **Efficiency.** Unit costs make the certificate flow a fewest-hop routing in aggregate — the
  objective *is* `Σ (flow × hops)`, so the optimum minimises total flow-hops. No per-unit
  shortest-path claim is made, and none holds: a unit may detour when sink assignment demands it.
  **This one carries no measurement and wants none:** it is true by construction of the LP, and
  any hop count we produced would be re-deriving the objective rather than testing it. The §3.13
  calibration deliberately degrades it, which is a change to the program being solved, not
  evidence about this property.

Recomputed on a fixed monthly tick, aligned to the vanilla trade tick. Orientation is read from
the current solve every time, with no memory of the previous one. The LP is deterministic on one
machine and one build (six identical solves, one orientation, on the reference implementation);
across machines it is the open question of §3.13.

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

**Wealth is owner-agnostic.** It is a property of the *place* — what the land is worth per year,
before anyone's government touches it. No autonomy, no production efficiency, no national ideas,
no estate or government modifiers, no technology. Two provinces with the same terrain, development
and trade good have the same wealth whoever owns them, and a province's wealth does not change
when it is conquered.

```
goods_produced(p)   = GP_COEFF · base_production(p)          # + local flat goods bonuses
trade_value(p)      = goods_produced(p) · price(good(p))     # ducats / YEAR
tax_value(p)        = TAX_COEFF · base_tax(p)                # ducats / YEAR
wealth(p)           = tax_value(p) + trade_value(p)          # ducats / YEAR

c(n,g)  = Σ_{p ∈ n} wealth(p)^α(g)  /  Σ_{q ∈ world} wealth(q)^α(g)
```

`GP_COEFF` and `TAX_COEFF` are in §2.3. Both were measured from the running game, not assumed:
neither is a define (`defines.lua` was searched), so both are engine constants recovered by
observation and each carries the observation that produced it.

**The two terms share a time basis and are safe to add.** The engine's own province tooltips give
both as *annual* quantities divided by twelve for display: the tax tooltip reads
`Base: 0.49 (Yearly 6.00)` for a province with `base_tax = 6`, and the production tooltip reads
`Trade Value: +0.26 … yearly income of 3.25` for a province whose window shows an annual
`Trade Value` of 3.20. Both monthly figures are the annual value over twelve, so the annual forms
add directly with no conversion. *(Measured on Garnatah, province 223, `base_tax` 6,
`base_production` 4, silk, `local_autonomy` 0 — the itemised tooltips are quoted in
`changes-v3.md`.)*

**Modifiers apply after the coefficient, not before.** The engine computes the base from
development first and then applies a percentage — `Base 0.49` then `Tax Income Efficiency 125.0%`,
giving 0.61. Flat goods bonuses are the exception: they add into `goods_produced` *before* the
price multiply, which is why they appear in the goods-produced tooltip as their own line
(`Base Goods Produced: 0.80 / Base Production: +0.80`).

**Which modifiers are local.** The engine's own data model draws the line for us: a trade good's
`province = { … }` block is province-scoped and attaches to the place; its `modifier = { … }`
block is country-scoped and attaches to the owner. Only the first kind is local. In vanilla the
income-relevant local ones are exactly three — `gems` (`local_tax_modifier = 0.15`), `glass`
(`local_production_efficiency = 0.1`) and `incense` (`trade_value_modifier = 0.1`). Terrain and
climate carry none: `terrain.txt` grants only development cost, supply limit and defensiveness.

Everything the engine itemised on a real province that is *not* local is excluded by this rule:
`Core` (+75% — a fact about the owner's relationship to the province, not the province), `Reform
Iqta` (+5%, government), `Clergy` (+5%, estate), national ideas (+15%), and production efficiency
from technology (+2%). `City` (+25%) is place-intrinsic but is constant across every province the
model counts, so it cancels in the normalised share and is not carried.

Unowned provinces are outside the model: `s` and `c` are computed over provinces with an owner and
`is_city = yes`, because an unowned province produces nothing the trade system can move.

**What this buys.** Demand stops responding to who rules and starts responding only to what is
there. A conquest no longer moves the demand vector on the day it happens — only development,
trade goods and prices do. It also removes the single largest source of hidden owner-dependence
from the aggregate graph (§1.6), which is built from this same wealth field.

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
production income. Under v3.0's owner-agnostic wealth the exclusion is stronger still: `wealth(p)`
is built from `base_tax`, `base_production` and price (§1.3) and reads **no income field at all**,
so gold income is **invisible to demand entirely** — not merely diverted, and not merely booked
elsewhere. Gold is also inert in vanilla trade value
(`base_price = 0`, `goldtype = yes`), so the exclusion costs nothing. Whether the per-province
production-income *field* nevertheless carries the gold figure before the country-level split is
still unknown, and under v3.0 it is also **moot**: nothing in the model reads that field, which is
why §2.7 item 12 was dropped rather than run.

**Any good with zero world production this month.** `s(n,g)` is undefined when nothing produces
`g`, so the good has no graph, contributes nothing to the value weights (`V_g = 0`), and is absent
from the survival table. It acquires all three on the first month any province produces it.

**Activation is not a local addition — it moves the whole field.** A province produces exactly one
trade good at a time, so a latent good going live *replaces* what that province was producing. In
the month it converts:

- the new good gains a producer and the old good loses one, so **both** goods' supply shares
  `s(·,g)` renormalise across every node that produces either;
- the province is repriced — `trade_value(p) = goods_produced(p) · price(good(p))` — so `wealth(p)`
  changes, and with it `c(n,g)` for **every good in the game**, not just the two, because §1.3
  makes one wealth field the demand base for all of them;
- `V_g` moves for both goods, reweighting every display, link value and AI score;
- and `Φ_w` moves, because §1.6 runs DRAIN on that same wealth field.

So an activation is a world-state change on the scale of a development change or a conquest, and
every graph in the model is entitled to move on it. Measured: repricing to coal the **45** of the
latent-coal provinces that are owned at 1444 — §1.3 counts only owned provinces — flips **10 of
159 `Φ_w` edges** (`v3measure.py`). Coal's base price of 10.0 is the highest in vanilla, so this is
near the upper end of what one good's activation can do. *(v2.1 held that a latent good leaves
`Φ_w` unaffected because "`Φ_w` reads wealth, not goods". `Φ_w` does read wealth — and wealth reads
the province's trade good and its price, which is exactly what activation changes. The proposition
was true under v2.0's `Φ_ord`, where `V_g = 0` gave a latent good zero weight, and became false
with the operator change.)*

Latent goods stay latent for long stretches — coal produces nowhere at the 1444 start, and
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
concentration exactly as per-good sink counts do.

**Scale.** In exact arithmetic only the sign pattern and proportions of `b_w` matter: Phase 0
reads signs, Phase 1's HHI is built from mass *shares*, the LP optimum scales linearly with
identical net-flow signs, and the priority key is order-isomorphic under positive scaling. The
implementation adds one premise — the zero-flow tolerance is **absolute** (`1e-11`, §2.3), so
scaling `b` *down* pushes genuine flow arcs into the free set. Measured: identical orientation at
×1 and above, 13 edge flips at ×10⁻², and at ×10⁻⁶ the sink set collapses to a single node.
Normalising into (−1, 1) scales 1444's `b_w` *up* (its largest magnitude is 0.0226) and is safe;
scaling down is not. Either scale `b` up, or scale the tolerance with it.

Measured on 1444 data at α_Φ = 1.5 (`v3measure.py`): **two sinks, `hangzhou` and
`english_channel`**. Their ranks are 3 and 2 in the α_Φ-weighted wealth field `c_w` — *not* in raw
node wealth, where they are 12th and 1st; v2 wrote "wealth ranks" without saying which, and the
plain reading is wrong. Phase 1 selects `genua`, both sinks arrive by stall promotion, and `genua`
ends a transit node. **Eight sources**, all in the bottom half of the wealth field (`c_w` ranks
44–75, mean degree 3.1 against the map's 4.0 — v2 called them "cul-de-sacs", which their degrees
do not support). Every node drains to a sink; acyclic, 159/159 oriented, 0 fallbacks; **0 edge
flips and 0 sink-set changes under ±1% wealth noise across 5 seeds** — stabler than any per-good
graph. Its marking order is a per-node scalar whose descending comparison reproduces the DAG
(0 violations), so every consumer needing a potential still gets one.

Agreement with the per-good graphs is **53.4%** of edge-goods (52.1% value-weighted) against the
superseded `Φ_ord`'s **60.2%** — a gap of 6.8 points, not the 9.3 v2 quoted. v2's 62.7% was
measured under the *old scan-order sweep* and was never regenerated after §3.6 adopted the
deterministic one; 60.2% is the deterministic figure. That trade is recorded in §3.9.

Dynamics, measured: dev-stacking `hangzhou`'s top province ×30 makes it the sole world sink;
scaling European node wealth ×2 makes `genua` the sole sink; at ×3 the Cape of Good Hope
**reverses** — 1444's Atlantic→Cape→Indian-Ocean drainage becomes
malacca/comorin_cape/zanzibar→Cape→ivory_coast. Sink count breathes with concentration
(transient extra sinks at intermediate boosts are expected behaviour, not noise), and it is
**non-monotone in α_Φ** — measured 5→2→1→2→3→1 across α_Φ ∈ {1, 1.5, 2, 3, 4, 8} on 1444
(`v3measure.py`). The count tracks how many world-class wealth poles the flow separates, not α_Φ
itself.

The v1 diagnostic identity (`Φ ≡ φ₀` at α = 1) does not survive the operator change: DRAIN
performs no linear solve, so no linearity argument exists. Its replacement as the end-to-end
correctness check is **exact orientation equality** between the reference and DLL implementations
— a combinatorial comparison with no tolerance band (§2.8).

## 1.7 Merchants

Placement, range, and the collect/steer choice are vanilla. One merchant per country per node. A merchant present gives **+2 trade power** (`MERCHANT_MAX_POWER_BONUS`) and a **+10% bonus on trade income** (`TRADE_MERCHANT_PRESENT = 0.1`, whose shipped comment reads "bonus on income if trade present"), node-wide, regardless of what it is doing. *v1 and v2 both called the second one "+10% trade efficiency"; trade efficiency and a flat income bonus are different quantities in EU4 — efficiency also feeds the caravan-power and collection tooltips — and the define's own comment says income.*

**Collect** — vanilla, including the −50% penalty outside the home node.

**Steer** — the node window lists **every link incident to the node**. The vanilla window already
renders both an incoming and an outgoing link list as clickable entries
(`incoming_nodes_listbox` / `outgoing_nodes_listbox` in `tradeinterface.gui`, both populated by
the `TradeNodeLink` widget); what changes is **what an incoming entry does** — it must accept a
merchant assignment rather than merely navigate. §2.7 item 14 settled which of those it does today:
the entry **only navigates** — clicking `Safi` in Sevilla's window switched the window to Safi and
dispatched nothing — so this is a new interaction on an existing widget, not a behaviour change to
one that already dispatches. A merchant assigned to link `{n,m}`:

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

- A country whose provincial trade power in a node meets the threshold receives a share of it in **every** immediately upstream node — with **no condition on the receiving node**. The engine's own tooltip says power transfers "to trade nodes where it already has power", and that qualifier is descriptively false: measured, France holds zero provinces and zero merchants in Sevilla and still appears there with 3.3 power, which the engine itemises as `Transfers from traders downstream: +3.1` and nothing else. This line was §3.16's cautionary case; it is now closed, and it closed in favour of the spec. The share is `1 / TRADE_PROPAGATE_DIVIDER`. The threshold in raw power is `TRADE_PROPAGATE_THRESHOLD × TRADE_PROPAGATE_DIVIDER`, pending §2.7 probe 8 — see §3.13.
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

**Caravan power is in this group but is not a threshold mechanic.** It is **not a function of raw trade power at all**: it is total country development ÷ `CARAVAN_FACTOR` plus policy and idea modifiers, clamped to [`CARAVAN_POWER_MIN`, `CARAVAN_POWER_MAX`], switched on by a merchant condition — a gated, development-scaled bonus rather than a step on power (§3.11). When it applies it is worth up to the cap for any major power — enough to move a node's power shares by itself, and therefore to push *other* countries across the thresholds above. *v1 and v2 both described it as "a step function on raw power", which contradicted their own §3.11.*

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
the sweep is deterministic given the LP's support and a fixed accumulation order — its comparisons
are of input-derived floats (`DEF`, `b`), not of solver residuals, which is the distinction that
matters against v1's dense algebra, but it is not integer arithmetic and v2 called it that. Its
cross-machine reproducibility reduces to the LP's. Until that is built and verified, ship
single-player
only.

## 2.2 Solver

1. Parser for `common/tradenodes/00_tradenodes.txt` — adjacency, `members`, `path`/`control` render data, `end`/`inland`/AI flags.
2. Parser for non-ironman saves — province owner, `base_tax`, `base_production`, trade good, goods produced, development.
3. Parser for `common/defines.lua`, merged with `common/defines/` overrides in load order (§2.3).
4. Per-province `wealth` — **owner-agnostic** per §1.3: `TAX_COEFF · base_tax + GP_COEFF ·
   base_production · price`, with local goods modifiers only and no autonomy, efficiency, ideas or
   owner terms. Then per-node `trade_value`, `s`, `c` with per-province α, and the per-good
   balance `b = s − c`.
5. DRAIN per good: min-cost b-flow — **network simplex or a simplex LP, not interior-point without
   crossover**, because §1.1's spanning-tree-basis property requires a basic optimum — the
   deterministic drainage sweep, and the Phase-4 evaluator (`unserved` / `stranded`, which must be
   equal by conservation, since `Σ_n b_g(n) = 0` identically).
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

## 2.2a What map this is for

v2 called the target "map-agnostic" while proving its central properties only for the map it was
measured on. v3.0 picks the narrower, honest target and states the two premises the proofs
actually need.

**Premise 1 — the node graph is connected.** Reachability (§1.1) is LP feasibility, and the LP is
feasible because `Σ_n b_g(n) = 0` identically. On a graph with more than one component that global
balance is not enough: each component must balance separately, and share normalisation does not
deliver that. A two-component graph carrying cross-component imbalance is **infeasible outright** —
the solver returns no flow at all, not a worse one. Vanilla 1444 is one component (measured).

*What the solver does about it:* compute components once at load. On a single component, proceed.
On more than one, either renormalise `s` and `c` **within each component** so every component
balances — which makes each component its own closed economy, the honest reading of a disconnected
map — or refuse to start and say which nodes are unreachable. It must not silently hand an
infeasible program to the LP. v1 carried per-component renormalisation and v2 dropped it without
replacement; v3 restores the requirement.

**Premise 2 — Phase 0 is a no-op, or the map-dependent properties are read as measurements.**
Several §1.1 properties are proved for the 2-core and hold on any map where Phase 0 removes
nothing (minimum degree ≥ 2, no bridges — true of vanilla). Where Phase 0 acts, three of them
weaken and the spec now says so rather than asserting through it:

| Property | On a 2-core map | Where Phase 0 acts |
|---|---|---|
| Global DAG (§1.1) | proved | **still proved** — pendant edges are bridges and cannot close a cycle |
| Sink-set equality (§1.1, §3.2) | measured exact 29/29 | **fails** — a pendant net-importer is a sink outside the set |
| Marking order reproduces the DAG (§1.6) | proved | **fails** — pendants have no marking order, so `Φ_ord`-style order comparison is undefined on pendant edges |
| Free-edge determinism (§1.1) | proved | proved — unaffected by peeling |

A fourth case is independent of Phase 0: inside the 2-core, a selected flow-terminal demander can
lose sinkhood to a free edge that reaches an earlier-marked node, which also breaks sink-set
equality. Both cases are worked in §3.2.

**So the stated target is: connected maps.** On a connected map with minimum degree ≥ 2 every
property in §1.1 is either proved or measured-and-labelled. On a connected map with pendants the
algorithm still runs and still produces an acyclic, fully-oriented, demand-serving graph — only
the sink-set *characterisation* and the order-potential reconstruction weaken. On a disconnected
map the solver must renormalise per component or refuse.

## 2.3 Constants

Read at runtime; never hardcoded.

| Use | Define |
|---|---|
| Propagation share | `TRADE_PROPAGATE_DIVIDER` |
| Propagation threshold | `TRADE_PROPAGATE_THRESHOLD` — see §3.13 |
| Off-home collect penalty | `TRADE_NON_CAPITAL_OFFICE` |
| Home-node steering bonus | `TRADE_POWER_HOME_BONUS` |
| Merchant trade power | `MERCHANT_MAX_POWER_BONUS` |
| Merchant income bonus | `TRADE_MERCHANT_PRESENT` — a bonus on income, **not** trade efficiency (§1.7) |
| Link boost base | `TRADE_ADDED_VALUE_MODIFER` |
| Caravan | `CARAVAN_FACTOR`, `CARAVAN_POWER_MAX`, `CARAVAN_POWER_MIN` |
| Trade capital move cost | `PS_MOVE_TRADE_PORT` |

**Engine constants that are not defines.** The two wealth coefficients of §1.3 are hardcoded in
the binary — `defines.lua` and `common/defines/` were searched and contain neither. They are
therefore *measured*, and each is recorded with the observation that produced it. Re-measure them
against any patch that is not 1.37.5.

| Constant | Value | How it was measured |
|---|---|---|
| `GP_COEFF` | **0.2** goods produced per point of `base_production` | Garnatah (province 223), `base_production = 4`, goods-produced tooltip: `Base Goods Produced: 0.80 / Base Production: +0.80` |
| `TAX_COEFF` | **1.0** ducat/year per point of `base_tax` | Same province, `base_tax = 6`, tax tooltip: `Base: 0.49 (Yearly 6.00)` |

Both were read with `local_autonomy = 0` so no owner term was in play. Prices come from
`common/prices/00_prices.txt` at runtime and are never hardcoded.

Design constants: the excluded-goods list (defaults to gold), the α price anchor `P₀ = 2.0`,
the aggregate-graph exponent `α_Φ = 1.5` (calibrated so the 1444 start yields the two-sink
hangzhou/english_channel map, §1.6 — a constant like `P₀`; world-responsiveness flows through
wealth, never through this knob), and DRAIN's three knobs at their defaults — demand-mass
quantile `ρ = 1.0`, cluster dilation `r = 0`, and the zero-flow tolerance `1e-11`. That tolerance
is **not** purely numerical: it is an absolute threshold, so it couples to the scale of `b`. See
§1.6's scale-invariance note and §3.13. A measured calibration option
that moves all three plus α's clamp is recorded in §3.13; the baseline does not use it.

**DLC state is a third input axis.** Treasure-fleet diversion and caravan power are both DLC-conditional, and caravan modifier values are readable even when inert — so key on the DLC flag, never on the presence of a value.

## 2.4 The tradenodes file

Generated once from the campaign start date's `Φ_w`, then owned by the DLL in memory. No per-session regeneration; merchants are recalled only when the mod is rebuilt. A mid-campaign load runs on the start-date file for up to one month.

The engine performs no topological sort. It **validates** that the file is one, logging
`[tradenodedefinition.cpp:61]: X=>y ( ERROR: Trade nodes must always be defined so that an
outgoing is defined after in the file, or we get processing errors)` once per violating link — but
it **tolerates** violations. Measured: a file with all 159 links declared backwards logged exactly
159 such errors and then loaded and played normally, with node `total` and `retention` unchanged
and the power-dependent fields differing only within the engine's own run-to-run variance.

What the engine does **not** tolerate is a **cycle**. A hand-authored two-node cycle produced
`EXCEPTION_STACK_OVERFLOW` with 1002 stack frames at a single return address, reproduced on two
launches, with vanilla and the reversed-order file both loading fine as controls. Acyclicity is
therefore a hard correctness requirement of the emitter, established by observation rather than
assumed. *(Both from `../v2-drain/game-session.md`.)*

**And a reversed link is honoured completely.** Moving one `outgoing` block from `sevilla` to
`valencia` — path list reversed, control pairs reversed, per item 3 below — loaded with **zero**
errors and rebuilt the economy around the new direction: Valencia moved from Sevilla's outgoing
side to its incoming side, Sevilla became an end node with zero outgoing value, Castile's merchant
switched from steering to collecting, and the two countries that had held power in Sevilla purely
by downstream propagation disappeared from the node. Every provincial power figure was unchanged.
This is the mod's core premise verified end to end.

1. **Declaration order** — emit in decreasing `Φ_w` marking order. This is the convention the
   engine states and the shipped vanilla file follows (0 of 159 links violate it), and violating
   it is non-fatal but logs one error per link. One visible consequence: the node window renders
   its incoming/outgoing link lists **in file declaration order**, so reordering nodes reorders
   what the player sees — another reason to emit in a stable order.
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
though the claim audit found several are observable without one.

**Items 12–15 are done.** They were run against 1.37.5 in `../v2-drain/game-session.md` and their
results are folded into §1.9, §2.4 and §3.6. Item 12 was dropped rather than run: under v3.0's
owner-agnostic wealth (§1.3) the per-province production-income *field* is not read by anything,
so what it contains no longer matters. What each of the others found:

- **13 (cyclic node file) — settled, and it reverses the hedge.** The engine does not tolerate a
  cycle: `EXCEPTION_STACK_OVERFLOW`, 1002 frames at one address, twice. §2.4 and §3.6 updated.
- **14 (incoming-link button) — settled, spec confirmed.** The entry only navigates; clicking
  `Safi` in Sevilla's window switched the window to Safi and dispatched nothing. §1.7 stands.
- **15 (propagation source qualifier) — settled, and it reverses the spec's caution.** The
  tooltip's "where it already has power" is *not* a precondition. France holds zero provinces and
  zero merchants in Sevilla and still receives 3.3 power there, itemised by the engine as
  `Transfers from traders downstream: +3.1`. §1.9's "every immediately upstream node" is correct
  as written and gains no qualifier. §3.16's cautionary case closes.
- **The §2.4 item 3 link-reversal check — done and passed.** A hand-flipped link loaded with zero
  errors and rebuilt the economy around the new direction (§2.4).

The declaration-order companion question is also settled: the engine validates order and logs one
error per violating link, but tolerates violations (§2.4).

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

All writes land atomically at the tick hook with the sim paused.

## 2.8 Validation

| Case | Expected |
|---|---|
| Spice and cloves, 1444 | Source in Indonesia. Baseline DRAIN measured: spices sink at Genoa (demand rank 1) plus branch-end termini (Australia, Brazil); cloves at Venice, Kongo, Australia, Brazil. **No Chinese node holds a spices sink in either configuration** — under the §3.13 α-calibration `spices` sinks at Genoa and Doab, and it is **cloves** that moves to Beijing. The v1 expectation of simultaneous China+Europe spice sinks is not the baseline behaviour and is not recovered by the calibration either. *(v2 said "China holds a spice sink only under the calibration", which its own parenthetical contradicted.)* |
| Most goods, 1444 | Sinks are `{selected ∩ flow-terminal} ∪ promoted` (§1.1) — 1 to 8 per good; high-demand nodes are sinks at 14% in the top demand decile vs 7% in the bottom **[unverified in v3.0]** (a barbell: LP branch ends land in poor pockets) |
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
| Economy tab vs. overlay | Every displayed trade figure matches the per-good economy to the ducat. **This is a self-consistency check, not a comparison against stock EU4** — stock trade values are not reproducible run to run: two identical vanilla 1444 Castile starts differ on 49 of 80 nodes by up to 8.96% (AI merchant placement is randomised at start; only node `total` and `retention` are deterministic). Any comparison against unmodded numbers needs a tolerance and a null run |
| Reachability | 100% of every good's demand reachable from its supply, asserted every tick; zero orphan sinks (an LP feasibility theorem — its failure means the implementation broke, not the world) |
| Conservation | Phase-4 `Σ unserved == Σ stranded` to machine precision, every good, every tick |
| Determinism | Re-running a tick reproduces the orientation bit-for-bit; promotions and fallbacks are scheduler-invariant (monotone closure) |
| Acyclicity | Asserted on every per-good graph, on `Φ_w`, and on the emitted file's declaration order |
| Sink set, 2-core | Two checks, not one. **Containment is a hard assertion, every tick, unconditionally:** every sink inside the 2-core lies in `{selected} ∪ {promoted}`, because every other core node is handed an out-arc by the sweep (§3.2). A violation is an implementation bug. **Equality — `{selected ∩ flow-terminal} ∪ {promoted}` exactly — is monitored, not asserted:** it is measured exact on 1444 (29/29 goods) but is not a theorem, and **T2** (§3.2) is the way it can fail while the algorithm is behaving correctly, when a free edge hands a selected flow-terminal demander an out-arc to an earlier-marked node. Report an equality miss with the node and the good; halt only on a containment miss |
| Sink set, pendants | Where Phase 0 acts, the equality above **does not apply and is not asserted**. The check on a peeled edge is the Phase-4 orientation rule: the edge is oriented by the sign of its absorbed subtree balance, and the un-peel reproduces it. **A net-importing pendant leaf that ends a sink is expected behaviour, not a violation** — that is **T1** (§3.2), and treating it as a fault is how a weakened single assertion would hide it |
| Colonization | Observer run to 1600: New World colonization proceeds at roughly vanilla pace |
| AI convergence | Greedy assignment settles with damping rather than oscillating |
| Latent good | While latent: no graph, no value weight, no survival-table entry; acquires all three the month production begins. **`Φ_w` is unaffected only while the good stays latent.** On activation the whole field moves — the province is repriced, so both goods' supply shares, every good's `c`, both value weights and `Φ_w` all change (§1.5). Measured: repricing the 45 owned latent-coal provinces flips 10 of 159 `Φ_w` edges |
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

**Solver track** — the **defines parser first**: §2.3 makes every constant in the model a runtime read, so the eligibility threshold, the propagation share, the off-home penalty, the merchant bonuses and the caravan terms are all downstream of it and cannot be written correctly before it exists. Then the b-flow and sweep with their per-tick assertions (reachability, conservation, acyclicity, determinism, 2-core sink containment) and the per-tick sink-set equality monitor; per-good eligibility; realized flows; the Φ_w-vs-realized disagreement measurement; the reachability census; the flip-rate measurement.

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

Two families of orientation fail before this one. The first fails by theorem; the second fails by
an exact rule whose *consequence* is measured — v2 called both theorems, which overstates the
second.

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
destroys §1.4's regime split, and better wealth inputs plausibly deliver about 1.7× — enough to
make Genoa a *co-*sink, not enough to make demand the determinant of placement: a Chinese spice
sink needs 3.6–4.8×, i.e. 9.5–21.4% of all world spice demand at one node. (v2 wrote "1.7× where
4–5× is needed", which compressed two different thresholds into one comparison and understated
what inputs could buy.)

**What survives from both, and what DRAIN keeps.** The conservation lesson: operators that impose
node balance somewhere (the v1 solve; a min-cost flow) serve 100% of demand as a *theorem*;
operators that don't (rank, seeded basins) strand it. DRAIN takes conservation from the b-flow —
reachability is LP feasibility on a connected map (§2.2a), not an aspiration — and takes sink
*placement* out of field geometry entirely: sinks are the selected demand centres plus the
flow-terminal drains any acyclic drainage orientation would be forced to have anyway, plus (where
Phase 0 acts) pendant net-importers. Four claims, three of which v1 never stated — v1 *did* state
aggregate acyclicity, as C061, "`Φ` is a potential, so orienting edges by it is acyclic", and its
ε-machinery stated what decided dead-branch direction. What v1 genuinely never stated is the
sink-placement determinant and any reachability guarantee:

1. **Sink placement:** on a map where Phase 0 is a no-op, final sinks =
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
   would disappear into the clause.
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
routes 24% of world spice supply through it — both figures **[unverified in v3.0]** — where v1's
potential never used it at all).
Peripheral termini still exist — the LP's branch ends are consumed at the end of the line — and
value only arrives where someone holds power at both ends of the link.

## 3.3 Why wealth, and why per province

Demand is purchasing power, and under §1.3 purchasing power is what the *place* is worth per year. It captures return flows for free: a sugar island's production term is carried by its trade good rather than by its development, so it becomes a genuine consumer of cloth and tools. The effect is real but modest at vanilla prices — sugar (3.0), cocoa (4.0) and coffee (3.0) are 1.2–1.6× grain (2.5), not multiples; the largest price ratios belong to cloves (8.0) and coal (10.0), neither of which is a Caribbean sugar island. *v1 and v2 said "negligible development but large production income", which overstated the gap.* No colonial-nation dependency, no timeline restriction — and under v3.0 no owner dependency either.

**Wealth is chosen for what the place is, not for who runs it.** Under v3.0 the owner-side terms are gone: autonomy drift, national ideas, government reforms, estates and technology no longer move demand at all. What remains still moves, and deliberately: development changes, trade goods change (a latent good activating reprices its province), prices move with events, and `trade_goods_size` modifiers on the *place* — devastation, occupation, siege, prosperity — still bite within months. A besieged province genuinely produces less, so that volatility is economics rather than noise, and a trade map that ignored a decade-long war would fail Goal 1. What v3.0 removes is the volatility that was really about *ownership*: a province no longer changes what it demands on the day it is conquered. Plan around the world, not around the graph: the map is legible, not unchanging.

**Trade income is excluded for circularity, not speed.** Including it would close a demand → orientation → flow → demand loop, making the graph respond to merchants' decisions rather than to the world. The loop still closes the long way: trade income funds development, development raises tax and production income.

**Per province, because node boundaries are an authoring artifact.** Node sizes run from 19 land
provinces (`cape_of_good_hope`) to 77 (`girin`) **[unverified in v3.0]** — a 4× spread with no
structural rule behind it.
Raising a node's aggregate wealth to a power rewards node size, so luxuries would drain toward
whichever node the map authors sliced coarsest. The distortion is measured against the
per-province form the model actually defines, not against equal totals: node-level α overweights a
k-province node by `k^(α−1)` at fixed per-province wealth, so at α = 1.5 a 77-province node is
favoured over a 19-province one by `(77/19)^0.5 ≈ 2×` purely on slicing, and Nippon (68 land
provinces) over the Paris node (`champagne`, 33) by `(68/33)^0.5 ≈ 1.44×`
**[unverified in v3.0]**. (v2 said a 77-province
node "beats a 19-province node **of equal total wealth** by 2×"; at equal totals the node-level
form is count-blind and they tie — the comparison that shows the distortion is against the
per-province form.) With the exponent inside the sum,
superlinear demand concentrates where individual provinces are rich. At α = 1 the per-province and
node-aggregate forms coincide exactly.

## 3.4 Why supply is pre-modifier

Production efficiency does not conjure more cloves; it means the owner extracts more ducats from the same cloves. Letting it into supply would say a province ships more to the world market because its owner picked Trade ideas — incoherent in a model whose thesis is that where a good comes from is what makes its trade its own.

**Under v3.0 it does not belong in demand either.** v1 and v2 excluded owner effects from supply and then let them straight back in through `wealth`, so the same incoherence they rejected on the supply side ran the demand side. §1.3 now excludes them from both. Supply and demand are both properties of the place, and the argument below — which was written to defend the supply side — applies unchanged and with more force to demand.

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
how often that can happen: **12 of 30 goods** can be pushed strictly below 2.0 by a single vanilla
`change_price` event (grain and wine reach 0.625), three more — `gems`, `silk`, `wool` — land
*exactly on* 2.0 and so reach α = 1 but not the sublinear regime, and **11 goods have no negative
price event at all** and can never go sublinear in vanilla. (v2 said 13; the boundary is `< 2.0`,
and three goods sit on it exactly. All 101 `change_price` blocks in `events/`, `decisions/`,
`missions/` and `common/` were parsed; `history/` contributes only positive entries.) That is the point of having the regime: without it a
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
the **engine's** behaviour on a cyclic file, and that is now measured rather than assumed: **the
engine dies**. A hand-authored two-node cycle produced `EXCEPTION_STACK_OVERFLOW` with 1002 stack
frames at a single return address, reproduced on two launches, while vanilla and a file with all
159 links declared backwards both loaded and played. The engine walks the node graph recursively
and a cycle never terminates. Acyclicity is enforced because the engine **provably** cannot
survive its absence — not, as v2 had it, because we could not prove that it could.

Nothing needs to stop churn. A link whose flow-support membership alternates month to month
carries near-nothing either way *on the evidence available*, and merchant assignments are to
links, so they survive flips untouched. The "carries near-nothing" half is measured, not derived:
v1's continuity argument (a near-flat potential implies near-zero flow) does not port to an LP
support, which is a discrete selection. Measured on 1444: across 29 goods × 6 random 1e-9 demand
nudges, **zero** support-membership changes moved more than 1e-6 of flow, and the ±1% wealth-noise
flips all sat on near-zero-flow edges. At exactly degenerate inputs — two equal-hop corridors — the
map from `b` to the chosen support is discontinuous in principle, so this rests on the solver's
tie-selection being stable, which is the same premise §3.13 tracks for multiplayer.

**v1's ε is deleted, because the problem it patched no longer exists.** The Laplacian oriented
dead branches by comparing solved potentials that were mathematically equal and differed only by
floating-point residual — so orientation varied by machine, and a field-level regularizer was
needed to break ties on purpose. DRAIN's free edges are oriented combinatorially: the priority
sweep's key (DEF, b, index) is computed from input data over the LP's support structure — its
*values* come from the inputs, though which nodes are downstream comes from the solve — the
measured count of exact key
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

**Scopes read `Φ_w` rather than any-good reachability.** A gate is a boolean; a scope is a set or a path, and answering a scope question with any-good reachability is an enormous buff. `Φ_w` is the graph the engine already walks, so those call sites are left alone — which collapses the shared-predicate risk. It is legible: one map predicts where fleets sail. And it is balanced: area-effect mechanics scoped by any-good reachability would cover most of the map — measured, **90.9%** (5743 of 6320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. (v2 quoted 98.8%; that is v1's *Laplacian* figure, 6245/6320, carried across the operator change without being re-measured. The argument is unaffected — 90.9% is still most of the map — but the number was not v2's own.)

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
  free and remains the most self-coherent aggregate measured: **60.2%** edge-good agreement with
  the per-good graphs against `Φ_w`'s 53.4% (52.1% value-weighted). It was superseded on design
  grounds: its ends are artifacts of sweep scheduling rather than places — of its 18 end nodes at
  1444, 9 terminate no good at all and none of the demand capitals is among them — and its end
  count **never concentrates**: 13–22 ends measured across cloves-α 2…64, never approaching
  vanilla's three. (v2 called this "α-invariant … 9–17 ends", which is neither the right word for
  a quantity that ranges 13–22 nor a band containing its own baseline of 18.) Self-coherence was
  traded for legible, wealth-anchored, world-responsive ends.
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

Verified numerically **[unverified in v3.0]**: agreement to 5.7e-14 across a node with mixed sinks, mixed collectors and the home-node penalty in play. So one scalar per node reproduces every country's income exactly, and the engine's own math does the rest.

**This is also why propagation cannot be made per good.** Tested **[unverified in v3.0]**: with propagation reading the one installed graph, the node-scalar model reproduces per-good truth to 1.4e-14. With power varying by good, it is off by 5.96 ducats on a node paying ~250 — because `powershare_C` stops factoring out. Keeping propagation on a single graph is load-bearing for Goal 7, not merely convenient.

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
÷ 3 **plus policy and idea modifiers**, clamped to [2, 50]; nineteen countries **[unverified in v3.0]** are at the cap from
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

**Open in the v3.0 wealth model.** These are the parts of §1.3 that could not be settled
empirically this session. They are questions, not numbers, and §1.3 carries no value for any of
them.

- **Do local flat goods bonuses exist at 1444, and do any apply before the price multiply?** The
  goods-produced tooltip itemises contributions additively (`Base Production: +0.80`), so a flat
  `trade_goods_size` would appear as its own line and enter before the price multiply. No 1444
  province was observed carrying one. Settling observation: find a province with a non-zero
  `trade_goods_size` from a building or static modifier and read its goods-produced tooltip.
- **Is `local_production_efficiency` from a trade good (glass, +10%) inside or outside local
  wealth?** It is province-scoped in the engine's data model, so §1.3's rule includes it — but it
  is also literally a *production efficiency*, which §1.3 otherwise excludes. The rule and the
  vocabulary disagree, and only three goods are affected (gems, glass, incense). Settling
  observation: read a glass province's production tooltip and confirm whether the +10% appears
  under `Production Efficiency` alongside the technology term.
- **Does `TAX_COEFF` stay 1.0 across the development range?** It was measured at one province
  (`base_tax` 6 → yearly 6.00). A linear coefficient is the obvious reading and the goods
  coefficient is linear at the same province, but one point does not establish linearity.
  Settling observation: read the tax tooltip on two provinces with different `base_tax`.

**Calibration, and unresolved parameters.**

- `k`, `α_min`, `α_max`. The test is whether they produce the intended three-regime split, not whether they differentiate same-geography goods, which they are not meant to do.
- **The zero-flow tolerance is scale-coupled.** §2.3 now records it as absolute rather than purely numerical — v2.1 filed it as numerical-only — and being absolute is what makes it interact with the magnitude of `b` (§1.6). Either normalise `b` to a fixed scale before the solve or make the tolerance relative. Undecided.
- Does `α_min` ever bite? Bounded from files now (§3.5): the sublinear regime is reachable through
  vanilla price events for 12 of 30 goods, unreachable for 11, and exactly on the boundary for 3.
  Whether those events fire often enough in a real campaign remains the open half.
- **The sink-count-span option.** A measured calibration exists that makes sink counts track price
  — span exactly 1..5, spearman(price, sinks) = −0.54 **[unverified in v3.0]**: α unclamped at exponent 2 (cloves α = 16),
  demand-mass quantile ρ = 0.5, twig tolerance 3e-4 (`drain-orientation.md` §5–6). Its costs are
  real and recorded: unclamped α² is a *demand-model* decision (luxuries become court goods —
  Beijing, **demand rank 2** under α = 16 with the rank-1 demander `hangzhou` acting as a transit
  node, becomes the cloves sink; v2 said Beijing "holds the richest single province", which it
  does not — that is `hangzhou`, at 27.0 against Beijing's 19.5), the tolerance re-routes arcs
  individually carrying <0.03% of world supply — up to about **0.15%** of a good's mass in total,
  not <0.03% — and drops **silk** to 99.97% reach and cloves to 99.997%, and it is one-snapshot
  tuning. The baseline does not adopt it; adopting it is a §1.4 decision, not a solver knob.
- LP determinism across machines: the min-cost-flow solve must pivot identically on identical
  input (replaces v1's ε-magnitude question; see §2.1 and §3.6).
- AI merchant reassignment cadence (§3.14).

## 3.14 AI merchant assignment

The two ends of a link never compete: a merchant at `n` on `{n,m}` moves goods oriented `n→m`, one at `m` moves goods oriented `m→n`, disjoint sets. Competition stays where vanilla puts it — between merchants at the same node.

**One precompute serves every country.** For each good, a backward pass over its DAG gives `S_g[n][H]`, the expected fraction of a unit of `g` at `n` arriving at `H`, multiplying through collection, steering shares, and the per-link multi-merchant boost. `collected_share(n,g)` reaches 1 at `g`'s sink, which terminates the recursion. All three inputs are country-independent aggregates, so this is one table, not one per nation — **about 1.5 MB at double precision**, well under a million operations per solve. *v1 and v2 both said 0.75 MB, which is the single-precision figure; the rest of the solver is double precision, as its own 5.7e-14 and 1.4e-14 tolerances show, so the natural implementation is twice that.*

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

**Ranked orientation (`score = s − c`, harmonic extension on empty nodes).** Wins every
sink–demand *alignment* statistic (ρ_val +0.281 against DRAIN's +0.053; 46.6% of top-decile nodes
are sinks against 14.1%) and fails on delivery: it is monotone (§3.2), so demand must rise along
every route — 83.3% of demand reachable, 34 orphan sinks, Genoa a cloves sink that cloves cannot
reach. It also posts **9 net-producer sinks** where DRAIN, LAP and FLOW all post zero, and 11–17
sinks per good against DRAIN's 1–8. *v2 said it "wins every sink statistic"; it does not — it wins
the alignment ones and loses the rest.*
Every RANK figure in this entry is **[unverified in v3.0]** — all were measured in the v2
validation pass and none was re-run by `v3measure.py`.

**Seeded basin growth (multi-source Dijkstra with balance feedback).** Flow converges to the
chosen seeds and starves everything off a supply→seed path; 88.5% reach at its best tuning **[unverified in v3.0]**. Its
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
most self-coherent aggregate measured (**60.2%** vs `Φ_w`'s 53.4%) and still acyclic for free —
but its ends are sweep-scheduling artifacts, not places (§3.9), and no parameter steers their
count. Retained as the measured coherence ceiling any future aggregate should be compared against.
The ceiling is 60.2%, not the 62.7% v2.0 and v2.1 both quoted: that figure predates the
deterministic sweep of §3.6 and was never regenerated after it.

**Pinned-count wealth fields (top-k seeding, gravity kernels).** Tested en route to `Φ_w`: a
3-mass gravity field `Φ(n) = max_m c_α(m)·γ^dist(n,m)` over the top-3 pairwise-unconnected
demanders hits any chosen end count exactly, with **66%** vanilla-arrow agreement in the reproduced
construction. (v2.0 and v2.1 both quoted 69%; the count-follows-seeds behaviour reproduced, that
figure did not.) Rejected: it pins
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
Religion's gating — turned out wrong. The real signal in the audit was **provenance**: **nine of
the sixteen refuted ENGINE claims were UNSOURCED** (v2 said "nine of fourteen"; no partition of the
refuted set yields fourteen — there are sixteen ENGINE-typed refutations, or thirteen excluding the
three that carried `derivation` provenance). So the rule is not "trust derivations" and not
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
provable or measured-and-labelled, each is checked at runtime (§2.8) — as an assertion where it is
a theorem and as a monitor where it is a measurement, which is the distinction sink placement
forced — and each is exactly the kind of sentence whose
absence hid the last flaw. The next audit's first question should be: **which property of the
output does this spec still not state?**

**The cautionary case is now closed, and it closed the other way.** The propagation source
condition was corrected once (ship propagation under its modifier) and defended by two reviewers
against the wrong error; the engine's tooltip then appeared to carry a *second* qualifier ("to
trade nodes where it already has power") that §1.9 did not. Probe 15 settled it: the qualifier is
**descriptively false**. A country with no provinces and no merchant in the upstream node still
receives propagated power there, itemised by the engine as `Transfers from traders downstream`.
§1.9 was right not to carry it.

The lesson is not the one the case was filed under. It was filed as "agreement between reviewers
is not verification", which remains true. But what actually happened is that a **binary string** —
the class of evidence §3.16 above nominates as sufficient — was the unreliable source. A
localisation string describes intent, not behaviour. **Sources are necessary, not sufficient**;
add to the rule that an engine fact sourced to a *string* is settled only when something observes
the behaviour the string describes.

**One more failure mode this document should name, because v3.0 nearly shipped a false positive
on it.** During the declaration-order test, a permuted node file differed from vanilla on 61 of 80
nodes — a real measurement, from a real game, parsed from real save files, impeccable provenance.
It was meaningless: two runs of *the same vanilla build* differ on 49 of 80 nodes by up to 8.96%,
because the engine randomises AI merchant placement at start. **A measurement without a null
comparison is not evidence.** Every measured claim in this document that could vary run to run
should carry the control that bounds its noise floor.
