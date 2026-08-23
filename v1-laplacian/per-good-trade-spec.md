# Per-Good Trade Network — Design Spec

**Version:** 1.3
**Status:** Living document
**Target:** EU4 (final patch), extended timeline compatible, map-agnostic

Three sections. **§1 Mechanics** states what the system does. **§2 Implementation** states how it is built. **§3 Reasoning** states why, and records what is still unknown.

---

# 1. Mechanics

## 1.1 Trade direction

Every trade good has its own directed network over the same adjacency. Direction is computed, never authored.

For each good `g`, solve over the unweighted graph Laplacian `L`:

```
L φ_g = s_g − c_g

orient u → v   iff   φ_g(u) > φ_g(v)
```

- Acyclic by construction.
- A node with no outgoing links for `g` is a **sink** for `g`.
- Sinks differ per good. There is no global end node.

**Solving it.** `L` is singular, with the constants in its null space. A solution exists iff `Σ(s − c) = 0` within each connected component, which holds because both are normalized shares. Pin `φ = 0` at one reference node per component.

Solve **per connected component**, renormalizing `s` and `c` within each so they balance. Skip isolated nodes.

Recomputed on a fixed monthly tick, aligned to the vanilla trade tick. Orientation is read from the current solve every time, with no memory of the previous one.

## 1.2 Supply

```
s(n,g) = goods_produced(n,g) / Σ_m goods_produced(m,g)
```

`goods_produced` is a physical quantity — pre-production-efficiency, pre-autonomy. It moves with devastation, occupation, and prosperity.

A regularizer is mixed in on every solve:

```
s ← (1 − ε)·s + ε/N          ε ≈ 10⁻⁶
```

## 1.3 Demand

Assembled per province, then summed to the node.

```
wealth(p) = tax_income(p) + production_income(p)
c(n,g)    = Σ_{p ∈ n} wealth(p)^α(g)  /  Σ_{q ∈ world} wealth(q)^α(g)
```

Unowned provinces generate no income and contribute nothing.

Overseas provinces are floored at 75% autonomy, so they contribute roughly a quarter of their development's income.

## 1.4 Market concentration

```
α(g) = clamp( ( price(g) / P₀ )^k ,  α_min ,  α_max )        P₀ = 2.0 ducats
```

- **α > 1** — demand superlinear in provincial wealth. Luxuries concentrate on individually rich provinces.
- **α = 1** — demand proportional to economic size.
- **α < 1** — demand sublinear. Bulk goods spread toward populous regions.

α moves with vanilla price events in both directions. No smoothing.

## 1.5 Goods without a graph

**Gold.** Excluded by configuration. Its value is counted in `wealth` through production income, except where diverted by the treasure-fleet mechanic (§1.11).

**Any good with zero world production this month.** `s(n,g)` is undefined when nothing produces `g`, so the good has no graph, contributes nothing to `Φ` (`V_g = 0`), and is absent from the survival table. It acquires a graph on the first month any province produces it. Latent goods behave this way for long stretches — coal produces nowhere until Manufactories arrives, then appears with a full graph in a single tick.

## 1.6 The aggregate graph

```
V_g = price(g) · Σ_m goods_produced(m,g)
Φ   = Σ_g V_g · φ_g
```

`Φ` is a potential, so orienting by it is acyclic. **`Φ` is the graph installed in the game.**

A diagnostic special case, computed but never drawn: with `α = 1` for all goods, `Φ` collapses to a scalar multiple of `φ₀`, the single solve with demand at α = 1 and supply as each node's share of world **trade value** (`Σ_p goods_produced(p) × price(good(p))`).

## 1.7 Merchants

Placement, range, and the collect/steer choice are vanilla. One merchant per country per node. A merchant present gives +2 trade power and +10% trade efficiency, node-wide, regardless of what it is doing.

**Collect** — vanilla, including the −50% penalty outside the home node.

**Steer** — the node window lists **every link incident to the node**, not only the outgoing ones. A merchant assigned to link `{n,m}`:

- steers every good oriented `n → m`,
- is inert for every good oriented `m → n`,
- keeps its assignment when a link flips; only its active good set changes.

The same physical link can host a merchant at each end, active on disjoint good sets.

**Caravan power** requires the merchant to be steering at least one good on that link; assignment alone does not qualify. This constrains only the two steering conditions — collecting at an inland node as main trading port is untouched, since the widening above does not affect collection. See §3.11.

## 1.8 Collection and transfer

Trade power and collect/transfer intent are node-wide. What varies per good is what they produce.

For each good `g` at node `n`:

```
collected_share(n,g) = 1                          if n is a sink for g
                     = P_collect / (P_collect + P_transfer(g))   otherwise
```

**Transfer eligibility is per good.** A country's power counts toward `P_transfer(g)` only if it has a merchant steering `g` at `n`, or it collects at some node reachable from `n` in `φ_g`. Power that is neither is inert for that good.

**The remainder moves per good**, by the vanilla two-case rule.

*If any country steers `g` at `n`:* the outgoing value of `g` is divided across outgoing links in proportion to the modified trade power steering **toward each link**, not to power held in the node generally. Two consequences follow and both are load-bearing. An outgoing link with no steerer receives **nothing**, even when other links are steered. And a single steerer takes **all** of `g`'s outgoing value down its link, however little power it holds.

*If no country steers `g` at `n`:* the outgoing value splits evenly across `g`'s outgoing links.

*At `g`'s sink:* there is no remainder. 100% is collected and divided among collectors by trade power.

Vanilla gates still apply: trade range, supply range, and no transfer into a node where nobody holds power at both ends.

## 1.9 Trade power propagation

Preserved from vanilla, unchanged:

- A country whose provincial trade power in a node meets the threshold receives a share of it in **every** immediately upstream node. The share is `1 / TRADE_PROPAGATE_DIVIDER`. The threshold in raw power is `TRADE_PROPAGATE_THRESHOLD × TRADE_PROPAGATE_DIVIDER`, pending §2.7 probe 8 — see §3.13.
- Ship trade power propagates only where the country has a ship-propagation modifier, at the compounded rate: the propagation share multiplied by that modifier.
- Propagation is strictly one hop and never chains.
- A node receives the summed contributions of all its downstream neighbours.

Direction is read from `Φ`.

## 1.10 Direction-dependent systems

**Any mechanism gated on one nation being upstream or downstream of another evaluates TRUE.**

**Any node-pair direction dependency reads `Φ`.**

Where a gate scopes a set or a path, that scope reads `Φ`, with this fallback ladder:

1. `Φ` path.
2. If `Φ` does not connect, the shortest path within a single good's graph that does.
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
| Improve Inland Routes | 33% |
| Propagate Religion | 50% to establish, 40% to maintain |

All are single-valued except Propagate Religion, whose band absorbs chatter on its own. Casus belli availability is the most visible symptom, since it can appear and vanish month to month.

**Caravan power is in this group but is not a threshold mechanic.** It is a step function on raw power: it either applies or it does not, and when it applies it is worth up to the cap for any major power — enough to move a node's power shares by itself, and therefore to push *other* countries across the thresholds above.

**Scripted content.** Missions, decisions, events, and trade companies reference trade nodes by name, and nodes themselves never change — only connections do, which the engine treats as conflict-free. A mission whose *sense* depends on a specific authored direction can become moot under reorientation. Accepted; listed for the compatibility pass rather than engineered around.

## 1.11 Treasure fleets

The overlord always receives. The fleet routes by the §1.10 ladder, passing each node en route where privateers skim a share proportional to their power there.

Where the diversion mechanic is active, colonial gold income is diverted from the colonial nation and does not enter `wealth` at either end.

## 1.12 What the game displays

The in-game economy **is** the per-good economy. Node values, the node window, pie charts, the ledger, the economy tab, and tooltips all show the model's numbers.

**Trade map mode.** Provinces coloured by node, arrows between nodes, drawing `Φ`. Arrow weight from realized value crossing the link.

**Selecting a commodity.** Clicking a province switches province colouring to the vanilla trade-goods rendering for that good and redirects the arrow layer to that good's graph. A sink is visible as a node with no outgoing arrows. Clicking the node icon clears back to `Φ`.

**Not representable in the vanilla UI**, and shown in the companion overlay instead:

- Value broken down by commodity. One value field per node, not thirty.
- A link's two-way traffic. One scalar per link, shown as net.
- Per-country effective trade power where eligibility differs by good. Shown as a value-weighted aggregate.

No new art, sprites, shaders, or map-mode chrome. The steering list widening in §1.7 is the only UI change.

---

# 2. Implementation

## 2.1 Shape

One program: a runtime-attached DLL that each month reads live game state, solves per good, propagates the per-good economy externally, and writes the result and the orientation back into the engine's own structures. Ships with a generated `00_tradenodes.txt` for load time and a companion overlay for what the engine cannot display.

Windows/Steam. Non-ironman. Achievements and ironman are off.

**Multiplayer is unsupported by default.** An identical build is necessary and not sufficient: EU4 multiplayer is lockstep with checksums, and an in-process floating-point solve can produce different results on different hardware — differing SIMD dispatch or accumulation order in the linear algebra is enough to desync. Supporting MP requires the solve to be bit-reproducible across machines: fixed accumulation order, no runtime-dispatched vector paths, no threaded reduction. Until that is built and verified, ship single-player only.

## 2.2 Solver

1. Parser for `common/tradenodes/00_tradenodes.txt` — adjacency, `members`, `path`/`control` render data, `end`/`inland`/AI flags.
2. Parser for non-ironman saves — province owner, `base_tax`, `base_production`, trade good, goods produced, development.
3. Parser for `common/defines.lua`, merged with `common/defines/` overrides in load order (§2.3).
4. Per-province `wealth`, per-node `trade_value`, `s`, `c` with per-province α, the ε regularizer, and `L φ = s − c` per good via sparse Cholesky.
5. `Φ`, and `φ₀` for the identity check.
6. Survival table `S_g[n][H]` for AI scoring — one table serving every country.
7. Mutual reachability census: 30 goods × 80 BFS, producing an 80×80 matrix whose entry counts goods with a directed path `n → … → m`.
8. Synthetic-shock harness: edit parsed province data and re-solve.

Cost is a sparse SPD solve of roughly 80×80 per good — microseconds each.

**Two implementations, one specification.** The list above is the reference solver: standalone, run against parsed saves, and the thing every validation in §2.8 is measured on. The shipped DLL carries a second implementation of items 4–7 in the host language, reading live memory instead of save files. They must agree — see §2.8 — and where they disagree the reference is correct by definition. The parsers and the harness stay reference-only; the DLL never reads a save.

**Inland is derived, not trusted from the flag:** a node with no coastal province among its `members`.

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

Two design constants remain: the excluded-goods list (defaults to gold) and the α price anchor `P₀ = 2.0`.

**DLC state is a third input axis.** Treasure-fleet diversion and caravan power are both DLC-conditional, and caravan modifier values are readable even when inert — so key on the DLC flag, never on the presence of a value.

## 2.4 The tradenodes file

Generated once from the campaign start date's `Φ`, then owned by the DLL in memory. No per-session regeneration; merchants are recalled only when the mod is rebuilt. A mid-campaign load runs on the start-date file for up to one month.

The engine performs no topological sort — the file must be one.

1. **Declaration order** — emit in decreasing `Φ`.
2. **End flags** — `end=yes` on every `Φ` sink; stripped from any former end node that gains outgoing links.
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
| Per-link value | net `Σ_g` realized flow, in the installed `Φ` direction |
| Country trade income | derived by the engine from the above, unless stored |

Feeding the engine the collectible pool is sufficient, and the reason is narrower than it looks. `collect_pool` is itself per good on the inside — `collected_share(n,g)` depends on `P_transfer(g)`, which §1.8 makes commodity-specific. What factors out is the *other* term: `powershare_C` is a country's share **among collectors**, and whether a country collects is a merchant-or-home property with no good dependence at all. So a good-independent share multiplies a per-good sum, the sum collapses to one scalar, and the engine's own vanilla collection math reproduces every country's per-good income exactly. See §3.10.

**Two deadlines, not one window:**

- **Display** — immediately after the value pass. AI consumers read these figures during the month.
- **Payment** — bounded by the month boundary, since the treasury reconciles at the start of each month against the previous month's income.

Per-link values are written net, which can be negative where realized flow opposes the drawn arrow.

## 2.7 Probes

Settled with a debugger on a vanilla install, in one session.

1. **Pass caching.** For each of the three passes independently: does flipping a link crash, produce stale-but-running values, or rebuild cleanly? Instrument for staleness — one-month corridor lag, value vanishing, tooltips disagreeing with arrows, propagation crediting the wrong side.
2. **Pass 2's content.** What imposes its ordering, given that propagation is one hop and cannot chain.
3. **Write windows.** Where income accumulation sits relative to the value pass; whether writing country trade income before month-boundary reconciliation makes AI budgeting and AI cash read the same figure.
4. **Negative link values.** Write one; observe arrow rendering and protect-trade allocation.
5. **Merchant storage.** Flip a link hosting a steering merchant — does the assignment dangle, reset, or crash?
6. **Caravan, twice.** Does the engine grant it for a merchant assigned to a link that is incoming in `Φ`? For one whose link carries no goods?
7. **Render data.** Is arrow render state separate from the economic link?
8. **`TRADE_PROPAGATE_THRESHOLD` semantics.** Set it to 4 and check whether the raw requirement doubles.
9. **Diverted gold.** Does diverted colonial gold still appear in the per-province production income field? Assert the DLC flag agrees with the observed field.
10. **Caller enumeration.** Disassemble and list every call site of "is X downstream of Y," classified as: return true; return true and define the scope; or compute per good. Produce the list as a written artifact, plus a companion "not members" list.

All writes land atomically at the tick hook with the sim paused.

## 2.8 Validation

| Case | Expected |
|---|---|
| Spice and cloves, 1444 | Source in Indonesia; sinks in **both** China and Europe |
| Most goods, 1444 | Largest sinks in India and China — correct, not a failure |
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
| `Φ` ≡ `φ₀` at α = 1 | Forcing α = 1 makes `Φ` a scalar multiple of `φ₀` |
| Acyclicity | Asserted on every solve |
| Colonization | Observer run to 1600: New World colonization proceeds at roughly vanilla pace |
| AI convergence | Greedy assignment settles with damping rather than oscillating |
| Latent good | A good with zero world production has no graph, no `Φ` contribution, no survival-table entry; acquires all three the month production begins |
| Cross-implementation | The DLL solver and the reference solver agree on orientation exactly, and on `φ` to tolerance, for every save in the historical set |

**Measured, not asserted:**

- **Φ-vs-realized sign disagreement**, weighted by trade value, not link count. Predicted to cluster at nodes with 3+ outgoing links and partial merchant coverage, thinning as coverage densifies.
- **Flip behaviour** per decade in peace versus war, and whether flips revert as occupation lifts.
- **Propagated-share change per node** on each flip, alongside the trade-power/in-degree covariance. This is what catches the §1.10 threshold mechanics flickering — a share crossing a single-valued limit is the failure mode, and casus belli availability the visible one. Total propagated power is not the quantity to watch: reorientation cannot change edge count, so `Σ indeg = |E|` is invariant and only the covariance moves.
- **Income balance, two metrics.** Total world collected income, and its distribution across historical great powers. Distribution is the gating one.

## 2.9 Build order

Not phases. Two tracks, run in parallel.

**Solver track** — the **defines parser first**: §2.3 makes every constant in the model a runtime read, so the eligibility threshold, the propagation share, the off-home penalty, the merchant bonuses and the caravan terms are all downstream of it and cannot be written correctly before it exists. Then ε; per-good eligibility; realized flows; the Φ-vs-realized disagreement measurement; the reachability census; the flip-rate measurement.

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

## 3.2 Why a potential field

Orienting each edge by comparing its endpoints fails on the Malacca–Cape corridor. The Cape has almost no wealth and consumes almost nothing, so a local comparison orients the edge into Malacca. The failure isn't that the Cape becomes a sink — it's that rank orientation is monotone, so no path can dip through a low-value intermediary and rise again. Malacca → … → Cape → … → Europe requires exactly that.

Merchants cannot repair it: a merchant selects among existing outgoing arrows, it cannot reverse one. Route-awareness has to live in the orientation.

The potential formulation fixes it for free. Where `s(n) = c(n) = 0`, the equation reduces to `φ(n)` = the average of its neighbours, so a pure conduit lies strictly between them and can only pass flow through. The Cape routes spice westward because Europe draws on the far end.

Sinks are net consumers automatically: a DAG-sink is a local minimum of `φ`, and by the discrete maximum principle local minima occur only where `c > s`. Peripheral sinks are intended — goods flow to a periphery and are consumed at the end of the line, and value only arrives where someone holds power at both ends of the link.

## 3.3 Why wealth, and why per province

Demand is purchasing power, and purchasing power is income the game already computes. It captures return flows for free: a sugar island has negligible development but large production income, so it becomes a genuine consumer of cloth and tools. No colonial-nation dependency, no timeline restriction.

**Income is chosen for responsiveness, not stability.** It is not a slow quantity — autonomy drift is monthly, occupation halves goods produced for a war's duration, devastation and sieges bite in months, Ming's mandate swings enormously over years. That is deliberate. A besieged province genuinely buys less, so the volatility is economics rather than noise, and a trade map that ignored a decade-long war would fail Goal 1. Plan around the world, not around the graph: the map is legible, not unchanging.

**Trade income is excluded for circularity, not speed.** Including it would close a demand → orientation → flow → demand loop, making the graph respond to merchants' decisions rather than to the world. The loop still closes the long way: trade income funds development, development raises tax and production income.

**Per province, because node boundaries are an authoring artifact.** Some nodes hold forty provinces and some hold four. Raising a node's aggregate wealth to a power rewards node size, so luxuries would drain toward whichever node the map authors sliced finest — Nippon out-consuming Paris on province count. With the exponent inside the sum, superlinear demand concentrates where individual provinces are rich. At α = 1 the two coincide exactly, which is what preserves the §1.6 identity.

## 3.4 Why supply is pre-modifier

Production efficiency does not conjure more cloves; it means the owner extracts more ducats from the same cloves. That is a fact about purchasing power and belongs in demand. Letting it into supply as well would say a province ships more to the world market because its owner picked Trade ideas — incoherent in a model whose thesis is that where a good comes from is what makes its trade its own.

This is also why the aggregate uses **trade value** rather than production income. The two are different quantities: a province's trade value is unaffected by production efficiency or local autonomy, and production income is defined by them. Substituting production income would break the `Φ ≡ φ₀` identity on real data for reasons having nothing to do with the solver — a day of debugging a correct pipeline.

## 3.5 Why α is anchored absolutely

Anchoring at 2 ducats rather than the price median means a good's market concentration moves only when *its own* price moves, and `k` becomes a pure sensitivity knob that doesn't shift the neutral point. Under a median anchor, a good could concentrate because some unrelated commodity got expensive — noise dressed as economics.

**α < 1 is a crash-reachable state, not a starting condition.** At vanilla base prices essentially nothing sits below the 2.0 anchor — grain lands near 1.25 and livestock near 1.00 — so the sublinear regime is entered mainly when a price event pushes a good beneath the anchor. That is the point of having it: without it a crash could only fail to concentrate a market, never actively spread it. Whether it engages often enough to earn its keep is an open question (§3.13), and if the answer is never, either `P₀` is set too low or the regime is doing no work.

α is deliberately mild. Production geography is what differentiates goods; α expresses only how concentrated a market is. A mechanism strong enough to reshape orientation would let price fight geography for control of the graph.

## 3.6 Why no hysteresis, and why ε

**A margin on orientation is a correctness bug, not a tuning knob.** Holding an edge against the current gradient means the emitted orientation is a splice of gradients from fields solved at different times, and a splice of two acyclic orientations need not be acyclic. Tested: with tol = 1e-3 and φ = {0, 0.0006, 0.0012}, tolerance-based tie-breaking produces **A→B→C→A**. A cycle — which the file format cannot represent and the whole design depends on being impossible.

Nothing needs to stop churn. A link that alternates has near-zero Δ and carries near-nothing either way. Merchant assignments are to links, so they survive flips untouched.

**ε is a different thing and is required.** A dead branch is harmonic with zero flux, so `φ` is mathematically constant along it but differs by numerical residual. Tested across four mathematically identical solves of one dead branch: `0.37000000000000000`, `0.36999999999999988`, `−0.86999999999999988`, with one edge orienting `←` twice and `→` once on Δ of ±1e-16. Exact ties occur in some runs and not others, so the tie-break fires unpredictably and orientation varies by machine. ε is field-level — the only kind the model permits — and it preserves the §1.6 identity exactly.

## 3.7 Why eligibility is per good

Vanilla's rule: effective trade power counts only countries which collect or transfer downstream, and not those whose trade capital is upstream. Power in a node not upstream of anywhere you collect is inert — neither retaining nor transferring.

Under a per-good model, "downstream" is per good. At a node where your home is downstream for cloth and upstream for spice, your power counts for one and not the other. This is what keeps the design honest: it returns true for *some* goods at every node, so no nation is ever globally inert, while still preventing a nation's power from shoving a good away from where it collects that good. Forcing it true for all goods at once would not be "everyone is upstream and downstream" — it would be "direction doesn't exist," which inflates transfer power everywhere.

The common misstatement — that any non-collecting country with trade power is transferring — is the loose community summary and is wrong.

## 3.8 Why gates evaluate true

The vanilla gates encode an assumption that a nation pair has one global relationship to trade: upstream or downstream. Under thirty graphs that assumption is not inconvenient, it is false. Every province is upstream for some good, because a region that receives your cloth ships you its furs. There is no fact of the matter for the gate to test, so the honest fix is to stop consulting it rather than to engineer the graph so it happens to pass.

**Node-pair dependencies are different and keep reading `Φ`.** Propagation is a relation between two nodes, not two nations. Setting it true would grant every country propagated power into every neighbour and multiply trade power across the map. This distinction is easy to miss and expensive to get wrong.

**Verified not members, recorded now rather than deferred.** Propagate Religion is node-local: it establishes a centre of conversion in the node's own province, gated on a trade-power threshold there and nothing else. The whole trade-policy family behaves the same way — a policy can be set in any node where the country meets the threshold, with no direction test anywhere. This is written down because the deferred artifact does not exist yet, and a community restatement of the "downstream target" claim would otherwise put them back.

**Scopes read `Φ` rather than any-good reachability.** A gate is a boolean; a scope is a set or a path, and answering a scope question with any-good reachability is an enormous buff. `Φ` is the graph the engine already walks, so those call sites are left alone — which collapses the shared-predicate risk. It is legible: one map predicts where fleets sail. And it is balanced: area-effect mechanics scoped by any-good reachability would cover a large fraction of the world.

## 3.9 Why `Φ` is the installed graph

`Φ` is a legal DAG, being a potential itself. It is the value-weighted aggregate of the real economy rather than an invented baseline. And once the displayed numbers are the model's numbers, the installed graph must be the one the economy actually runs.

Note what `Φ` is **not**: `ΔΦ` is *not* the net value crossing an edge. That was an error. `ΔΦ = Σ_g V_g Δφ_g` is the analytic figure, while realized movement follows vanilla propagation — goods with large Δφ can be diluted by an even split across three links while goods with small Δφ get winner-take-all steered the other way. So a link can be oriented `n → m` under `Φ` while realized net flow runs `m → n`. That is why the disagreement rate is measured rather than assumed, and why display policy for negative link values is a decision deferred to data.

For the same reason, the analytic `flow_g = V_g · Δ` has no consumer. Link values are realized flows, which makes conservation hold by construction.

## 3.10 Why the engine's economy is overwritten

Paying countries correctly while leaving the display wrong is a strictly weaker position: node values, pie charts and the ledger would describe an economy nobody is playing, and AI light-ship building, trade-league behaviour, peace valuation and income-threshold events all read those figures.

The engine's data model turns out to be sufficient at node level, for a narrower reason than it first appears. `collect_pool` is per good on the inside, since `collected_share(n,g)` depends on `P_transfer(g)` and §1.8 makes transfer eligibility commodity-specific. What factors out is the other term: `powershare_C` is a country's share **among collectors**, and whether a country collects is a merchant-or-home property with no good dependence. A good-independent share multiplying a per-good sum collapses to one scalar:

```
income_C(n) = Σ_g value_g(n) · collected_share(n,g) · powershare_C(n)
            = powershare_C(n) · collect_pool(n)
```

Verified numerically: agreement to 5.7e-14 across a node with mixed sinks, mixed collectors and the home-node penalty in play. So one scalar per node reproduces every country's income exactly, and the engine's own math does the rest.

**This is also why propagation cannot be made per good.** Tested: with propagation reading `Φ`, the node-scalar model reproduces per-good truth to 1.4e-14. With power varying by good, it is off by 5.96 ducats on a node paying ~250 — because `powershare_C` stops factoring out. Keeping propagation on a single graph is load-bearing for Goal 7, not merely convenient.

Only the *decomposition* by good exceeds what the engine can hold.

## 3.11 Why caravan power needs a condition added

In vanilla, steering is outgoing-only — the map shows the paths leaving a node and nothing else, and trade cannot be steered upstream at any amount of power. So "assigned" and "steering" are the same condition, and the engine never had to distinguish them.

§1.7 widens the steering list to incident links and pulls them apart. Caravan power fires on a merchant plus an inland link end, with nothing checking whether value moves — steering from Crimea to Kiev grants the bonus in Crimea. So without a condition, a merchant assigned to an incoming link, inert for every good, would earn a major power the full caravan bonus at any node adjacent to one of the roughly 26 inland nodes. Since caravan power is total country development ÷ 3 capped at 50, every major power is at the cap from 1444 and it does not scale with node presence at all.

Requiring the merchant to steer something **restores the vanilla state of affairs**. Granting on bare assignment would be the deviation, and an unintended one.

## 3.12 Why treasure fleets are always granted

Consistency with §3.8 is the weaker argument. The stronger one is that the gate is bistable.

Denial is not neutral: the colonial nation keeps the gold *and any income gained from it*, so its node's wealth rises, making it more sink-like, keeping it denied. Granting diverts that income, lowering the node's wealth, making it more source-like, keeping it granted. Both states self-reinforce, so two otherwise identical campaigns diverge permanently on whichever state they started in. Granting removes a bifurcation, not just a lock-in.

Two consequences priced in advance. Inflation scales with money received relative to economy size, so universal granting hits small previously-cut-off colonizers hardest. And the route rule is a balance dial, since privateers skim per node passed — which is why hop counts are compared between candidate rules on the mod's own graph rather than against vanilla's, that being a counterfactual on a graph we have replaced.

## 3.13 Open questions

**Prose-sourced — distrust, build nothing on them.**

- Colonization's gate shape. The evidence is one mod author's report, contradicted in-thread, and the observed behaviour needs no gate at all: if colonial nodes route away from the AI's home, expected trade income collapses and low-scoring provinces don't get colonized. The caller enumeration must be able to return "no colonization gate exists" as a *successful* result.

**Derived — probably right, cheaply falsifiable.**

- `TRADE_PROPAGATE_THRESHOLD` semantics. The file value and the documented raw requirement differ by exactly the propagation divider, which reconciles if the threshold is expressed in propagated units. Falsify by doubling the define.
- Pass 2's ordering requirement. Propagation is one hop and cannot chain, so something else in that pass imposes it; eligibility resolution is a backward reachability from collection points and is the only candidate named. An argument from exhaustion, and our inventory has been wrong before — §2.7 probe 2 settles it.

**Debugger-only.** Everything in §2.7, principally pass caching and income accumulation timing.

**Calibration, and unresolved parameters.**

- `k`, `α_min`, `α_max`. The test is whether they produce the intended three-regime split, not whether they differentiate same-geography goods, which they are not meant to do.
- Does `α_min` ever bite? At vanilla base prices nothing starts below the anchor, so the sublinear regime may be reachable only through price crashes (§3.5). If it never engages in a full campaign, `P₀` is mis-set or the regime is inert.
- ε magnitude: small enough to be invisible against any real economy, large enough to decide dead branches against floating-point noise.
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

**Authored demand weights.** Authored data in a model that needs none.

**Trade income inside `wealth`.** Reintroduces flow → demand → orientation → flow circularity; the graph would respond to merchants rather than to the world.

**Node-level α.** Makes demand concentration a function of how finely the map was sliced.

**Median-relative α anchor.** A good's concentration would shift because other goods changed price.

**α floored at 1.** Discards the cheap-bulk regime.

**Production income as the aggregate supply term.** Makes world supply depend on owners' idea groups and breaks the `Φ ≡ φ₀` identity for reasons unrelated to the solver.

**A τ margin on orientation.** Manufactures cycles (§3.6).

**Uniform supply in the aggregate solve.** Answers a question nobody asked and destroys the identity that makes `φ₀` worth computing.

**`φ₀` as the installed graph.** It is not the economy the model runs.

**A vestigial in-game economy with net treasury settlement.** Correct treasuries, wrong displays, wrong AI inputs (§3.10).

**Per-good propagation.** Breaks the income factoring and with it Goal 7.

**Node-level collect/transfer rules.** The collect/transfer split is per good because whether a good has anywhere to go is per good.

**Treating unsteered goods as fully collected.** Transfer power does not come from merchants; full collection happens at a sink, which is a property of the graph.

**Undirected shortest path as the primary fleet route.** A geodesic over a directional structure can route a fleet against every arrow on the map.

**Automatic per-good merchant targeting.** One vanilla arrow click already achieves per-good resolution, and automation would cost denial steering.

**Companion-overlay merchant assignment.** Assignment must stay a game action or vanilla knowledge stops transferring.

**Emission-time pruning of near-flat links.** Peripheral termini are intended consumption, and the power-at-both-ends gate already withholds unworked corridors.

**Edge conductance / weighted Laplacian.** Too much mechanical surface; the unweighted solve routes correctly through conduits.

**Staged delivery.** The intermediate states are different designs sharing a solver, not subsets of this one.

**"The aggregate map is not a DAG."** An error. Net flow is the gradient of `Φ`, hence acyclic — which is what makes an installable single network exist at all.

## 3.16 Evidence standard

This spec was reviewed adversarially over many rounds by two reviewers. Every retraction on either side — without exception — traced to a premise that entered through prose: a community post, a wiki sentence read under the wrong heading, semantics inferred from a define name, a forum thread title. Nothing built on adjacency data, file values, or the model's own equations failed.

The rule is **not** that derivations are safe. Two retracted claims were sound derivations resting on false premises about the map. The rule is: **trust the inference, audit the inputs, and treat any prose-sourced premise as provisional however much reasoning sits on top of it.**

The cautionary case is the propagation source condition. Both reviewers signed off on it as correct while defending it against the wrong error, and it was corrected only later to include ship propagation under its modifier. §1.9 carries the corrected version; the lesson is that agreement between two reviewers is not verification, and that a line can be confidently defended against one mistake while carrying another.
