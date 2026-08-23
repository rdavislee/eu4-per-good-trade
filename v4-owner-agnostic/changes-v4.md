# Changes, spec v3.0 → v4.0

**Method.** v4.0 was produced by **copying** `../v3-owner-agnostic/per-good-trade-spec.md`
byte-for-byte and then applying **74 asserted string replacements**, each one anchored on text that
had to be present exactly once or the patch aborted. Every replacement is quoted in full below and
tagged with the claim it clears. A paragraph-level diff reports **38 paragraph groups replaced,
0 inserted and 0 deleted outright**, and **no heading was lost or gained**. The file grew from
104,457 to 116,649 bytes (1,269 → 1360 lines).

That "0 inserted" is the property this revision was built for. v4.0 adds no new subject matter: it
is a repair of v3.0, so every proposition in it either survives from v3.0 unchanged or **replaces**
a v3.0 proposition that `validation-v3.md` graded REFUTED or PARTIAL. A claims delta extracted
against `../v3-owner-agnostic/claims-v3.md` should therefore consist entirely of rows whose
`Replaces` column names a graded claim.

**Inputs.** `per-good-trade-spec.md` v3.0, `../v3-owner-agnostic/validation-v3.md` (10 refutations,
19 partials, 4 systemic findings, 5 unfolded v2 partials), and a fresh pass over the 1.37.5.0 Inca
install.

---

## What v4.0 changes, in one table

| Driver | Count | Where |
|---|---|---|
| v3.0 refutations folded through | 10 | §0, §1.1, §1.3, §1.7, §2.8, §2.9, §3.2, §3.5 |
| v3.0 partials narrowed to what is proved or measured | 19 | throughout |
| `validation-v2.md` partials v3.0 counted but never folded | 5 | §1.6, §1.8, §1.10, §2.2 |
| Systemic findings closed | 4 | §1.3, §2.2, §3.2, and this document's own statistics |
| Figures regenerated after the solver fix | 14 | §1.6, §2.8, §3.2, §3.8, §3.9, §3.13, §3.15 |
| `[unverified in v3.0]` markers cleared by re-running | 8 | §2.8, §3.2, §3.3, §3.11, §3.13, §3.15 |
| **Propositions added that replace nothing** | **0** | — |

## The one change that is a design decision, not a correction

Everything else in this revision narrows a sentence, corrects a number, or folds a scan that was
run too narrowly. **§1.1's Phase 3 gains a branch**, because `validation-v3.md` showed the
algorithm as written had no defined behaviour in a case the reference implementation had been
handling with an undocumented rule:

> On a stall, promote the heaviest flow-terminal demander among the candidates … **If the
> candidates hold no flow-terminal demander at all, promote the highest-wealth candidate instead,
> ties by index.**

The alternative considered and rejected was to promote `Φ_w`'s sinks. It does not work: `Φ_w`'s
sinks at 1444 are `hangzhou` and `english_channel`, and a stalled pocket containing neither would
stay stalled — and `Φ_w` is itself a DRAIN run that can reach the same branch, so it would need a
non-`Φ_w` base case anyway. Highest-wealth-in-the-candidate-set *is* that base case, it is always
in the pocket, node wealth is a good-independent input that needs no bootstrap, and it reads only
the candidate set, so it inherits the same scan-invariance proof as the flow-terminal branch.

Consequences, all of them replacements: §1.1's sink-placement bullet gains the fourth case and
names **T1**/**T2**/**T3**; §2.2a's premise-2 discussion names T3 alongside T2; §3.2's claim 1
gains T3's construction; and §2.8's 2-core containment assertion — which v3.0 introduced as an
unconditional halt over `{selected} ∪ {promoted}` — asserts over
`{selected} ∪ {promoted} ∪ {fallbacks}`, the set the sweep actually maintains. On 1444 the branch
never fires (0 fallbacks, 29/29 goods and `Φ_w`), so **no measured number moves because of it**.

## The one change that moves every measured number

`validation-v3.md`'s first systemic finding was that the reference solver never implemented §1.3's
local goods modifiers, so every figure in §2.8 was measured on a wealth field the spec did not
define. v4.0 fixes the solver rather than the spec: `solver.py` now applies `gems`
(`local_tax_modifier = 0.15`, 43 provinces) to the tax term and `incense`
(`trade_value_modifier = 0.1`, 29 provinces) to the trade-value term. World wealth moves
10,572.40 → **10,594.80**, and fourteen quoted figures move with it. All fourteen were regenerated
and are listed under "Measurement provenance" below; none of them changes a conclusion.

---

# Every replacement, quoted

Ordered as applied. `§0`–`§3.16` locate the change; **Clears** names the graded claim.

### W003+W006 — §0 front matter
**Clears:** W003 (REFUTED), W006 (PARTIAL)

**Removed:**

```
**Version:** 3.0
```

**Replaced by:**

```
**Version:** 4.0
```

### W003b — §0 front matter
**Clears:** W003 (REFUTED)

**Removed:**

```
**v3.0** makes three changes. (a) **Wealth becomes owner-agnostic** — it is a property of the
place, not of who holds it: no autonomy, no production efficiency, no ideas, no owner modifiers
(§1.3, §3.3). (b) Every refutation and partial in `../v2-drain/validation-v2.md` is folded through,
including four v1 corrections that v2 never applied. (c) The four game probes settled in
`../v2-drain/game-session.md` are applied, two of them reversing v2's stated position (§2.4, §1.9).
Deleted text is quoted in `changes-v3.md`. Every measured number carries the script that produced
it; anything not regenerated for v3.0 is marked **[unverified in v3.0]**.
```

**Replaced by:**

```
**v4.0** keeps v3.0's three changes and closes the audit of them. (a) **Wealth is owner-agnostic**
— a property of the place, not of who holds it: no autonomy, no production efficiency, no ideas, no
owner modifiers (§1.3, §3.3). (b) Every refuted and partial claim in `../v2-drain/validation-v2.md`
**and** `../v3-owner-agnostic/validation-v3.md` is folded through — including the five
`validation-v2.md` partials v3.0 counted in its ledger but did not fold (§1.6, §1.8, §1.10, §2.2)
and four v1 corrections that v2 never applied. (c) The four game probes settled in
`../v2-drain/game-session.md` are applied, two of them reversing v2's stated position (§2.4, §1.9).
Deleted text is quoted in `changes-v4.md`. Every measured number carries the script that produced
it; anything not regenerated for v4.0 is marked **[unverified in v4.0]**.
```

### W124a — §1.1 Phase 3
**Clears:** W124, W193, W131

**Removed:**

```
flow-arc subgraph (acyclic and fixed before any free edge, so no circularity). On a stall, promote
the heaviest flow-terminal demander into the sink set — the self-correction that supplies the real
sink count. Free edges then orient from later-marked to earlier-marked.
```

**Replaced by:**

```
flow-arc subgraph (acyclic and fixed before any free edge, so no circularity). On a stall, promote
the heaviest flow-terminal demander among the candidates into the sink set — the self-correction
that supplies the real sink count. If the candidates hold no flow-terminal demander at all, promote
the **highest-wealth** candidate instead, ties by index: that is the **fallback** branch, it is what
a pocket with no net demander needs, and node wealth is a good-independent input so it needs no
bootstrap. (*Candidates* at a stall are the unmarked nodes whose flow out-neighbours are all marked;
the flow subgraph is acyclic, so at least one always exists and the sweep always advances.) Free
edges then orient from later-marked to earlier-marked.
```

### W124b — §1.1 properties
**Clears:** W124 (REFUTED), W012 (kept true)

**Removed:**

```
- **Sink placement is explicit.** Every sink is either a selected demand centre that turned out
  flow-terminal, a stall-promoted flow-terminal demander, or a Phase-0 pendant that absorbed a
  net-importing subtree. On a map where Phase 0 is a no-op the third case is empty and the sink
  set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods on 1444,
  1–8 sinks per good, mean 3.6. **That equality is not a theorem in general**, and v2 asserted it
  as one. Two constructed cases break it: a pendant net-importing leaf is a sink outside the set,
  and inside the 2-core a selected flow-terminal demander can be handed an out-arc by a free edge
  to an earlier-marked node and cease to be a sink. Both are worked in §3.2. A node with no
  outgoing links for `g` is a **sink** for `g`; sinks differ per good; there is no global end node.
```

**Replaced by:**

```
- **Sink placement is explicit.** Every sink is either a selected demand centre that turned out
  flow-terminal, a stall-promoted flow-terminal demander, a fallback-promoted highest-wealth node,
  or a Phase-0 pendant that absorbed a net-importing subtree. On a map where Phase 0 is a no-op and
  no fallback fires, the last two cases are empty and the sink set is exactly
  `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods on 1444, 1–8 sinks per
  good, mean 3.6, zero fallbacks. **That equality is not a theorem in general**, and v2 asserted it
  as one. Three constructed cases break it: a pendant net-importing leaf is a sink outside the set
  (**T1**); inside the 2-core a selected flow-terminal demander can be handed an out-arc by a free
  edge to an earlier-marked node and cease to be a sink (**T2**); and a fallback promotion is a sink
  that is neither selected nor stall-promoted (**T3**). All three are worked in §3.2. A node with no
  outgoing links for `g` is a **sink** for `g`; sinks differ per good; there is no global end node.
```

### W086 — §1.1 properties
**Clears:** W086 (PARTIAL)

**Removed:**

```
- **Scan-invariance.** Ready-marking is a monotone closure, so the stall sequence, promotions and
  fallbacks are provably independent of scheduling; the priority key makes the remaining freedom
  (free-edge direction) a function of the graph and the balances alone. Measured: zero orientation
  changes under scheduler permutations; zero exact key ties.
```

**Replaced by:**

```
- **Scan-invariance.** Ready-marking is a monotone closure, so the stall sequence and both
  promotion branches are provably independent of scheduling — each reads only the candidate set,
  which the closure fixes. Free-edge direction is **deterministic** for the same reason plus the
  priority key's index tiebreak. That it is a function of the graph and the balances *alone* — that
  the node indexing never decides — is **measured, not proved**: it holds exactly where the key has
  no exact ties. Measured: zero orientation changes under scheduler permutations, and zero exact
  `(DEF, b)` ties on free edges, 29/29 goods.
```

### W027 — §1.3 formula
**Clears:** W027 (PARTIAL)

**Removed:**

```
goods_produced(p)   = GP_COEFF · base_production(p)          # + local flat goods bonuses
trade_value(p)      = goods_produced(p) · price(good(p))     # ducats / YEAR
tax_value(p)        = TAX_COEFF · base_tax(p)                # ducats / YEAR
wealth(p)           = tax_value(p) + trade_value(p)          # ducats / YEAR
```

**Replaced by:**

```
goods_produced(p)   = GP_COEFF · base_production(p) · (1 + Σ local goods-produced modifiers)
                                                             # + local flat goods bonuses
trade_value(p)      = goods_produced(p) · price(good(p)) · (1 + Σ local trade-value modifiers)
                                                             # ducats / YEAR
tax_value(p)        = TAX_COEFF · base_tax(p) · (1 + Σ local tax modifiers)   # ducats / YEAR
wealth(p)           = tax_value(p) + trade_value(p)          # ducats / YEAR
```

### W035 — §1.3 time basis
**Clears:** W035 (REFUTED), W037 (PARTIAL)

**Removed:**

```
**The two terms share a time basis and are safe to add.** The engine's own province tooltips give
both as *annual* quantities divided by twelve for display: the tax tooltip reads
`Base: 0.49 (Yearly 6.00)` for a province with `base_tax = 6`, and the production tooltip reads
`Trade Value: +0.26 … yearly income of 3.25` for a province whose window shows an annual
`Trade Value` of 3.20. Both monthly figures are the annual value over twelve, so the annual forms
add directly with no conversion. *(Measured on Garnatah, province 223, `base_tax` 6,
`base_production` 4, silk, `local_autonomy` 0 — the itemised tooltips are quoted in
`changes-v3.md`.)*
```

**Replaced by:**

```
**The two terms share a time basis and are safe to add.** The engine's own province tooltips give
both as *annual* quantities divided by twelve for display. The tax tooltip reads
`Base: X (Yearly 12·X)` — `Base: 0.49 (Yearly 6.00)` at `base_tax` 6, `Base: 0.16 (Yearly 2.00)` at
`base_tax` 2. The monthly production tooltip's `Trade Value` line is the province window's *annual*
`Trade Value` over twelve — observed 3.52 → `Trade Value: +0.29`. Both monthly figures are the
annual value over twelve, so the annual forms add directly with no conversion.

*(Measured on two provinces: Garnatah, 223 — `base_tax` 6, `base_production` 4, silk,
`local_autonomy` 0 — and Caceres, 1747 — `base_tax` 2, `base_production` 2, wool. **Only the
tooltips' `Base` lines are used.** A province window's `Trade Value` also carries the owner's
`global_trade_goods_size_modifier`: Garnatah's window read 3.52 rather than 0.80 × 4.00 = 3.20
because Granada's 1444 monarch held the `Industrious` ruler personality, +10%. Ruler personalities
are rolled at game start wherever country history scripts none, so any window figure is one sample
of a random variable; the `Base` lines and the annual-over-twelve ratio are not.)*
```

### W039 — §1.3 modifier order
**Clears:** W039 (PARTIAL)

**Removed:**

```
**Modifiers apply after the coefficient, not before.** The engine computes the base from
development first and then applies a percentage — `Base 0.49` then `Tax Income Efficiency 125.0%`,
giving 0.61. Flat goods bonuses are the exception: they add into `goods_produced` *before* the
price multiply, which is why they appear in the goods-produced tooltip as their own line
(`Base Goods Produced: 0.80 / Base Production: +0.80`).
```

**Replaced by:**

```
**Modifiers apply after the coefficient, not before.** The engine computes the base from
development first and then applies a percentage — `Base 0.49` then `Tax Income Efficiency 125.0%`,
giving 0.6125, which the province window shows as 0.62. Flat goods bonuses are the exception: they
add into `goods_produced` *before* the price multiply. The goods-produced tooltip's shape is
**consistent with** that and does not establish it — it carries an additive `Base Goods Produced`
block (`Base Production: +0.80`) above a separate multiplicative `Goods Produced Efficiency` block,
and no 1444 province was observed carrying a flat bonus in the first block (§3.13).
```

### W040+W041+W045+W160 — §1.3 which modifiers are local
**Clears:** W041 (REFUTED), W040 (PARTIAL), W045 (PARTIAL), W160 (PARTIAL)

**Removed:**

```
**Which modifiers are local.** The engine's own data model draws the line for us: a trade good's
`province = { … }` block is province-scoped and attaches to the place; its `modifier = { … }`
block is country-scoped and attaches to the owner. Only the first kind is local. In vanilla the
income-relevant local ones are exactly three — `gems` (`local_tax_modifier = 0.15`), `glass`
(`local_production_efficiency = 0.1`) and `incense` (`trade_value_modifier = 0.1`). Terrain and
climate carry none: `terrain.txt` grants only development cost, supply limit and defensiveness.
```

**Replaced by:**

```
**Which modifiers are local, and which of those enter wealth.** Two tests, and a modifier must pass
both. It is **local** iff its value depends only on the province's own attributes — terrain,
climate, trade good, development, buildings — and on no country's state. It **enters wealth** iff it
modifies a quantity `wealth` computes: `goods_produced`, `price`, or `tax_value`. The engine's
trade-good data model is one *instance* of the first test and not the test itself — a good's
`province = { … }` block is province-scoped and its `modifier = { … }` block is country-scoped, so
only the first can be local — because modifiers also reach a province from outside the trade-good
tables, and those are classified by the test rather than by which file they live in.

Applied to everything live on a 1444 province with no owner input:

| Modifier | Local? | Enters wealth? |
|---|---|---|
| `gems` `local_tax_modifier = 0.15` | yes, set by the province's good | **yes** — modifies `tax_value` |
| `incense` `trade_value_modifier = 0.1` | yes, set by the province's good | **yes** — modifies `trade_value` |
| `glass` `local_production_efficiency = 0.1` | yes, set by the province's good | no — modifies production *income*, which wealth does not compute |
| `chinaware` `local_autonomy = -0.1` | yes, set by the province's good | no — modifies local autonomy, which wealth does not compute |
| goods-produced efficiency from nearby merchant republics, trading cities and trade companies (`bonus_from_merchant_republics`, `eu4.exe:0x1cc7128`) | **no** — its value is set by which *neighbouring countries* hold those government forms | — |
| the owner's `global_trade_goods_size_modifier` (e.g. the `Industrious` ruler personality, +10%) | no — country-scoped | — |
| `terrain.txt` and the climate static modifiers | yes | no — they grant `allowed_num_of_buildings`, `defence`, `local_defensiveness`, `local_development_cost`, `movement_cost`, `nation_designer_cost_multiplier`, `supply_limit`, colonial growth and hostile attrition, none of which wealth computes |

So exactly **two** modifiers enter wealth in vanilla: `gems` on the tax term and `incense` on the
trade-value term. The reference solver applies both (§2.2 item 4). The two rows that are local but
do not enter — glass and chinaware — are the whole of the rule-versus-vocabulary tension: §1.3
excludes production efficiency and autonomy by name, and the second test excludes them again for the
same reason, so there is nothing left to decide.
```

### W049 — §1.3 exclusions
**Clears:** W049 (REFUTED), W048 (kept true)

**Removed:**

```
Everything the engine itemised on a real province that is *not* local is excluded by this rule:
`Core` (+75% — a fact about the owner's relationship to the province, not the province), `Reform
Iqta` (+5%, government), `Clergy` (+5%, estate), national ideas (+15%), and production efficiency
from technology (+2%). `City` (+25%) is place-intrinsic but is constant across every province the
model counts, so it cancels in the normalised share and is not carried.
```

**Replaced by:**

```
Everything the engine itemised on a real province that is *not* local is excluded by this rule:
`Reform Iqta` (+5%, government), `Clergy` (+5%, estate), national ideas (+15%), production
efficiency from technology (+2%), and the owner's goods-produced modifiers.

`Core` (+75%) and `City` (+25%) are the two that are **not** excluded, because they are already
inside `TAX_COEFF`. The engine's tax multiplier is the sum of the itemised percentages — Garnatah's
`Tax Income Efficiency: 125.0%` is 75 + 25 + 5 + 5 + 15 and multiplies the base by 1.25; Caceres's
`105.0%` is 75 + 25 + 5 and multiplies by 1.05 — so a cored city province carrying nothing else sums
to exactly 0.75 + 0.25 = 1.00 and yields `base_tax` ducats a year. That is the reference condition
`TAX_COEFF = 1.0` was measured at, and it is the same for every province the model counts: all of
them are cities (`is_city = yes`), and ownership is not modelled, so every one is treated as cored.
Carrying either term again would double-count it.
```

### script-1.5 — §1.5
**Clears:** W006 (PARTIAL)

**Removed:**

```
159 `Φ_w` edges** (`v3measure.py`). Coal's base price of 10.0 is the highest in vanilla, so this is
```

**Replaced by:**

```
159 `Φ_w` edges** (`v4measure.py`). Coal's base price of 10.0 is the highest in vanilla, so this is
```

### W057 — §1.6 scale
**Clears:** W057 (regenerated)

**Removed:**

```
Normalising into (−1, 1) scales 1444's `b_w` *up* (its largest magnitude is 0.0226) and is safe;
```

**Replaced by:**

```
Normalising into (−1, 1) scales 1444's `b_w` *up* (its largest magnitude is 0.0225) and is safe;
```

### 1.6-measured — §1.6
**Clears:** W059, W060 (regenerated), W006

**Removed:**

```
Measured on 1444 data at α_Φ = 1.5 (`v3measure.py`): **two sinks, `hangzhou` and
```

**Replaced by:**

```
Measured on 1444 data at α_Φ = 1.5 (`v4measure.py`): **two sinks, `hangzhou` and
```

### W061+W062 — §1.6
**Clears:** W061, W062 (regenerated under v4 wealth)

**Removed:**

```
Agreement with the per-good graphs is **53.4%** of edge-goods (52.1% value-weighted) against the
superseded `Φ_ord`'s **60.2%** — a gap of 6.8 points, not the 9.3 v2 quoted. v2's 62.7% was
measured under the *old scan-order sweep* and was never regenerated after §3.6 adopted the
deterministic one; 60.2% is the deterministic figure. That trade is recorded in §3.9.
```

**Replaced by:**

```
Agreement with the per-good graphs is **53.5%** of edge-goods (52.5% value-weighted) against the
superseded `Φ_ord`'s **60.0%** — a gap of 6.5 points, not the 9.3 v2 quoted. v2's 62.7% was
measured under the *old scan-order sweep* and was never regenerated after §3.6 adopted the
deterministic one; 60.0% is the deterministic figure on v4.0's wealth field. That trade is recorded
in §3.9.
```

### V223 — §1.6 dynamics
**Clears:** V223 (v2 PARTIAL, unfolded in v3.0)

**Removed:**

```
Dynamics, measured: dev-stacking `hangzhou`'s top province ×30 makes it the sole world sink;
scaling European node wealth ×2 makes `genua` the sole sink; at ×3 the Cape of Good Hope
**reverses** — 1444's Atlantic→Cape→Indian-Ocean drainage becomes
malacca/comorin_cape/zanzibar→Cape→ivory_coast. Sink count breathes with concentration
(transient extra sinks at intermediate boosts are expected behaviour, not noise), and it is
**non-monotone in α_Φ** — measured 5→2→1→2→3→1 across α_Φ ∈ {1, 1.5, 2, 3, 4, 8} on 1444
(`v3measure.py`). The count tracks how many world-class wealth poles the flow separates, not α_Φ
itself.
```

**Replaced by:**

```
Dynamics, measured: dev-stacking `hangzhou`'s top province ×30 makes it the sole world sink
(also at ×20 and ×50; at ×10 the sink set is still three); scaling **the 22 European nodes'** wealth
×2 makes `genua` the sole sink; at ×3 the Cape of Good Hope **reverses** — 1444's
Atlantic→Cape→Indian-Ocean drainage becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast. *The
22 are the 18 western and central European nodes —* `english_channel`, `north_sea`, `baltic_sea`,
`white_sea`, `novgorod`, `lubeck`, `rheinland`, `saxony`, `wien`, `krakow`, `pest`, `venice`,
`ragusa`, `genua`, `champagne`, `bordeaux`, `valencia`, `sevilla` *— plus* `constantinople`,
`crimea`, `kiev` *and* `kazan`. *Both thresholds are set-dependent and land exactly under that
reading; under the 18-node set alone, sole-`genua` needs ×2.5 and the Cape reverses at ×2.* Sink
count breathes with concentration (transient extra sinks at intermediate boosts are expected
behaviour, not noise), and it is **non-monotone in α_Φ** — measured 5→2→1→2→3→1 across
α_Φ ∈ {1, 1.5, 2, 3, 4, 8} on 1444 (`v4measure.py`). The count tracks how many world-class wealth
poles the flow separates, not α_Φ itself.
```

### W066 — §1.7
**Clears:** W066 (REFUTED)

**Removed:**

```
*v1 and v2 both called the second one "+10% trade efficiency"; trade efficiency and a flat income bonus are different quantities in EU4 — efficiency also feeds the caravan-power and collection tooltips — and the define's own comment says income.*
```

**Replaced by:**

```
*v1 and v2 both called the second one "+10% trade efficiency"; trade efficiency and a flat income bonus are different quantities in EU4 — separate modifier keys with separate ledger columns (`LEDGER_TRADE_EFFICIENCY`, `LEDGER_TC_EFF_CARAVAN_POWER`), granted separately where both appear together — and the define's own comment says income.*
```

### V071 — §1.8
**Clears:** V071 (v2 PARTIAL, unfolded in v3.0)

**Removed:**

```
Vanilla gates still apply: trade range (which gates **merchant placement**, not value flow — no
mechanic gates flow by range) and no transfer into a node where nobody holds power at both ends.
There is no trade "supply range" in the engine; the only supply-range constructs are naval.
```

**Replaced by:**

```
Vanilla gates still apply: trade range and the rule that there is no transfer into a node where
nobody holds power at both ends. What trade range gates is **reach, not flow**: every string,
define and modifier that mentions it is about where a country may *send* something —
`HINT_TRADERANGE_TEXT` ("how far away you may send a Merchant"), `TRADE_RANGE_IRO` ("our merchants
can reach trade nodes within this range"), `TRADE_NODES_OUT_OF_RANGE`, `MAPMODE_TRADE_DESC`, and
also `MERCENARY_COMPANY_TOO_FAR` / `MERC_RANGE_EXPLAINED` (mercenary hiring) and
`REQUIRES_CAPITAL_IN_TRADE_RANGE_TT` (a diplomatic precondition). **No string, define or modifier
ties range to link flow** — which is a statement about the files, not a proof that no such mechanic
exists; settling that needs value observed arriving at a node chain beyond every country's range.
There is no trade "supply range" in the engine; the only supply-range constructs are naval.
```

### V075 — §1.10 table
**Clears:** V075 (v2 PARTIAL, unfolded in v3.0)

**Removed:**

```
| Propagate Religion | 50% to establish **and 50% to maintain** in the default branch (a country-flag ladder runs 5–50; the terminal fallback is 35/35) — no band |
```

**Replaced by:**

```
| Propagate Religion | 50% to establish **and 50% to maintain** in the default branch, 35/35 in the terminal branch — neither banded. The nine `N_trade_power_for_propogate_religion` country-flag rungs between them **are** banded: maintain trails select by 5–10 points (10→5, 15→5, 20→10, 25→15, 30→20, 35→25, 40→30, 45→35), and the 5-flag carries no maintain share at all |
```

### V076 — §1.10 banding
**Clears:** V076 (v2 PARTIAL, unfolded in v3.0)

**Removed:**

```
The banding is the reverse of what v1 recorded: **Improve Inland Routes is the one banded
mechanic; Propagate Religion has no band**, and every other listed threshold is single-valued. So
nothing absorbs threshold chatter on its own — a power share oscillating across any of these
limits flickers the mechanic, Propagate Religion included. Casus belli availability is the most
visible symptom, since it can appear and vanish month to month.
```

**Replaced by:**

```
The banding is the reverse of what v1 recorded: **Improve Inland Routes is the one unconditionally
banded mechanic**, every other listed threshold is single-valued, and Propagate Religion is banded
only on its flag ladder. So almost nothing absorbs threshold chatter — a power share oscillating
across any single-valued limit flickers the mechanic, and that includes Propagate Religion for the
flagless countries its default and terminal branches cover. The flicker-risk set is "every country
at a single-valued limit, plus flagless countries at Propagate Religion's 50/50 or 35/35", not
"every country". Casus belli availability is the most visible symptom, since it can appear and
vanish month to month.
```

### W071 — §1.10 caravan
**Clears:** W071 (UNSOURCED -> measured)

**Removed:**

```
When it applies it is worth up to the cap for any major power — enough to move a node's power shares by itself, and therefore to push *other* countries across the thresholds above.
```

**Replaced by:**

```
When it applies it is worth up to the cap for any major power — enough to move a node's power shares by itself, and therefore to push *other* countries across the thresholds above. Measured on the 1444 start: the cap of 50 is **8.6% to 32.0% of an inland node's total trade power** (median 21.5% over the 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`), against a largest single incumbent holder of 9.6 to 20.7 — so one country at the cap outweighs every incumbent in every inland node.
```

### W074 — §2.2 item 4
**Clears:** systemic finding 1 (solver did not implement 1.3)

**Removed:**

```
4. Per-province `wealth` — **owner-agnostic** per §1.3: `TAX_COEFF · base_tax + GP_COEFF ·
   base_production · price`, with local goods modifiers only and no autonomy, efficiency, ideas or
   owner terms. Then per-node `trade_value`, `s`, `c` with per-province α, and the per-good
   balance `b = s − c`.
```

**Replaced by:**

```
4. Per-province `wealth` — **owner-agnostic** per §1.3:
   `TAX_COEFF · base_tax · (1 + local tax modifiers) + GP_COEFF · base_production · price ·
   (1 + local trade-value modifiers)`, and no autonomy, efficiency, ideas or owner terms. In vanilla
   the local modifiers that enter are exactly two — `gems` (+15% tax, 43 provinces) and `incense`
   (+10% trade value, 29 provinces) — and the reference solver applies both; v3.0 specified them and
   computed without them. Then per-node `trade_value`, `s`, `c` with per-province α, and the
   per-good balance `b = s − c`.
```

### V090 — §2.2 cost
**Clears:** V090 (v2 PARTIAL, unfolded in v3.0)

**Removed:**

```
Cost per good is one uncapacitated min-cost flow on 80 nodes / 318 arcs plus an O(V+E) sweep —
milliseconds each with network simplex, tens of milliseconds for all 29 goods per monthly tick.
```

**Replaced by:**

```
Cost per good is one uncapacitated min-cost flow on 80 nodes / 318 arcs plus an O(V+E) sweep.
Measured on the reference implementation (scipy/HiGHS plus the deterministic sweep, one machine):
**5.7–7.3 ms per good and 0.17–0.21 s for all 29**. "Milliseconds each" therefore holds already,
with a generic LP; the all-29 figure is what a native network simplex would have to improve on, and
no measurement in this project supports a specific projection **[unverified in v4.0]**.
```

### W086b — §2.2a table
**Clears:** W086 (PARTIAL)

**Removed:**

```
| Free-edge determinism (§1.1) | proved | proved — unaffected by peeling |
```

**Replaced by:**

```
| Free-edge determinism (§1.1) | proved as determinism; **measured** as independence from the node indexing (zero exact `(DEF, b)` ties, 29/29 goods) | same in both halves — peeling does not touch the priority key |
```

### W124c — §2.2a
**Clears:** W124 (REFUTED)

**Removed:**

```
A fourth case is independent of Phase 0: inside the 2-core, a selected flow-terminal demander can
lose sinkhood to a free edge that reaches an earlier-marked node, which also breaks sink-set
equality. Both cases are worked in §3.2.
```

**Replaced by:**

```
Two further cases are independent of Phase 0, and both break sink-set equality inside the 2-core: a
selected flow-terminal demander can lose sinkhood to a free edge that reaches an earlier-marked node
(**T2**), and a fallback promotion can become a sink that was neither selected nor stall-promoted
(**T3**). With the pendant case (**T1**) all three are worked in §3.2.
```

### W092+W094 — §2.3 constants
**Clears:** W035, W037 (citation), W094/W162

**Removed:**

```
| `GP_COEFF` | **0.2** goods produced per point of `base_production` | Garnatah (province 223), `base_production = 4`, goods-produced tooltip: `Base Goods Produced: 0.80 / Base Production: +0.80` |
| `TAX_COEFF` | **1.0** ducat/year per point of `base_tax` | Same province, `base_tax = 6`, tax tooltip: `Base: 0.49 (Yearly 6.00)` |

Both were read with `local_autonomy = 0` so no owner term was in play. Prices come from
`common/prices/00_prices.txt` at runtime and are never hardcoded.
```

**Replaced by:**

```
| `GP_COEFF` | **0.2** goods produced per point of `base_production` | Four provinces, four development levels, from the `Base Goods Produced` line: Caceres (1747) `base_production` 2 → 0.40, Girona (1751) 3 → 0.60, Garnatah (223) 4 → 0.80 with the itemisation `Base Goods Produced: 0.80 / Base Production: +0.80`, Barcelona (213) 5 → 1.00 |
| `TAX_COEFF` | **1.0** ducat/year per point of `base_tax` | Two provinces, two development levels, from the `(Yearly …)` parenthetical: Garnatah `base_tax` 6 → `Base: 0.49 (Yearly 6.00)`, Caceres `base_tax` 2 → `Base: 0.16 (Yearly 2.00)`. The displayed monthly is the truncation of `base_tax × 0.083333` |

Both coefficients are read off the tooltips' **base** lines, which carry no owner term — Garnatah
also has `local_autonomy = 0`. Neither is read off a province window, because a window figure
carries the owner's modifiers and some of those are randomised at game start (§1.3). Prices come
from `common/prices/00_prices.txt` at runtime and are never hardcoded.
```

### W101a — §2.4
**Clears:** W101 (PARTIAL)

**Removed:**

```
`EXCEPTION_STACK_OVERFLOW` with 1002 stack frames at a single return address, reproduced on two
launches, with vanilla and the reversed-order file both loading fine as controls.
```

**Replaced by:**

```
`EXCEPTION_STACK_OVERFLOW` at a single exception address (`0x00007FF6DDE6A8B4`) under 1002 recorded
`eu4.exe` frames — the dump records no per-frame addresses — reproduced on three launches, with
vanilla and the reversed-order file both loading fine as controls.
```

### W101b — §3.6
**Clears:** W101 (PARTIAL)

**Removed:**

```
engine dies**. A hand-authored two-node cycle produced `EXCEPTION_STACK_OVERFLOW` with 1002 stack
frames at a single return address, reproduced on two launches, while vanilla and a file with all
159 links declared backwards both loaded and played.
```

**Replaced by:**

```
engine dies**. A hand-authored two-node cycle produced `EXCEPTION_STACK_OVERFLOW` at a single
exception address under 1002 recorded `eu4.exe` frames, reproduced on three launches, while vanilla
and a file with all 159 links declared backwards both loaded and played.
```

### W193 — §2.8
**Clears:** W193 (REFUTED), W131 (PARTIAL)

**Removed:**

```
| Sink set, 2-core | Two checks, not one. **Containment is a hard assertion, every tick, unconditionally:** every sink inside the 2-core lies in `{selected} ∪ {promoted}`, because every other core node is handed an out-arc by the sweep (§3.2). A violation is an implementation bug. **Equality — `{selected ∩ flow-terminal} ∪ {promoted}` exactly — is monitored, not asserted:** it is measured exact on 1444 (29/29 goods) but is not a theorem, and **T2** (§3.2) is the way it can fail while the algorithm is behaving correctly, when a free edge hands a selected flow-terminal demander an out-arc to an earlier-marked node. Report an equality miss with the node and the good; halt only on a containment miss |
```

**Replaced by:**

```
| Sink set, 2-core | Two checks, not one. **Containment is a hard assertion, every tick, unconditionally:** every sink inside the 2-core lies in `{selected} ∪ {promoted} ∪ {fallbacks}` — the set the sweep actually maintains — because every other core node is handed an out-arc by the sweep (§3.2). A violation is an implementation bug. Asserting containment in `{selected} ∪ {promoted}` alone would halt on **T3** (§3.2), which is correct behaviour, so the fallback set is part of the assertion and not an escape clause on it. **Equality — `{selected ∩ flow-terminal} ∪ {promoted}` exactly — is monitored, not asserted:** it is measured exact on 1444 (29/29 goods, zero fallbacks) but is not a theorem, and **T2** and **T3** (§3.2) are the two ways it can fail while the algorithm is behaving correctly — a free edge handing a selected flow-terminal demander an out-arc to an earlier-marked node, and a fallback promotion. Report an equality miss with the node and the good; halt only on a containment miss |
```

### W193b — §2.9
**Clears:** W193 (REFUTED)

**Removed:**

```
acyclicity, determinism, 2-core sink containment) and the per-tick sink-set equality monitor;
```

**Replaced by:**

```
acyclicity, determinism, 2-core sink containment in `{selected} ∪ {promoted} ∪ {fallbacks}`) and
the per-tick sink-set equality monitor;
```

### W115 — §2.8
**Clears:** W115 (regenerated under v4 wealth)

**Removed:**

```
**No Chinese node holds a spices sink in either configuration** — under the §3.13 α-calibration `spices` sinks at Genoa and Doab, and it is **cloves** that moves to Beijing.
```

**Replaced by:**

```
**No Chinese node holds a spices sink in either configuration** — under the §3.13 α-calibration `spices` sinks at Genoa alone, and it is **cloves** that moves to Beijing.
```

### barbell — §2.8
**Clears:** [unverified in v3.0] cleared by re-run

**Removed:**

```
high-demand nodes are sinks at 14% in the top demand decile vs 7% in the bottom **[unverified in v3.0]** (a barbell: LP branch ends land in poor pockets) |
```

**Replaced by:**

```
high-demand nodes are sinks at 14.1% in the top demand decile vs 6.9% in the bottom (a barbell: LP branch ends land in poor pockets) |
```

### W118a — §2.8
**Clears:** W118 (PARTIAL)

**Removed:**

```
stock trade values are not reproducible run to run: two identical vanilla 1444 Castile starts differ on 49 of 80 nodes by up to 8.96% (AI merchant placement is randomised at start; only node `total` and `retention` are deterministic).
```

**Replaced by:**

```
stock trade values are not reproducible run to run: two identical vanilla 1444 Castile starts differ on 49 of 80 nodes by up to 8.96%, over the five node fields `current`, `local_value`, `outgoing`, `total` and `retention` (AI merchant placement is randomised at start, and it is the three power-dependent fields that inherit it: `retention` is identical on 80 of 80 nodes and `total` on 79 of 79, the exception drifting 0.012%).
```

### W118b — §3.16
**Clears:** W118 (PARTIAL)

**Removed:**

```
It was meaningless: two runs of *the same vanilla build* differ on 49 of 80 nodes by up to 8.96%,
```

**Replaced by:**

```
It was meaningless: two runs of *the same vanilla build* differ on 49 of 80 nodes by up to 8.96%
across the same five fields,
```

### contrast — §3.2
**Clears:** systemic finding 3 (eps artifact)

**Removed:**

```
`(c − s)/deg > mean(neighbour φ) − min(neighbour φ)` — verified on every (good, node) pair — and
because supply contrast exceeds demand contrast by four to five orders of magnitude, the
right-hand side is set by supply geography.
```

**Replaced by:**

```
`(c − s)/deg > mean(neighbour φ) − min(neighbour φ)` — verified on every (good, node) pair — and
because supply is *sparse* where demand is dense, the right-hand side is set by supply geography:
spices are produced in 18 of 80 nodes and cloves in one, while every node with an owned province
carries demand, so the neighbour spread that sets the threshold is a supply pattern almost
everywhere. (v1 and v2 quantified this as "supply contrast 10⁷ against demand contrast 10²–10³".
That ratio was `max(s)` over the **ε floor** of v1's regularizer, which §1.2 removes; with no
regularizer the spices supply ratio over *producing* nodes is 36 against a demand ratio of 471.5,
which points the other way. The sparsity is the real asymmetry and the diagnosis rests on it.)
```

### W121+W122 — §3.2
**Clears:** W121 (PARTIAL), W122 (PARTIAL)

**Removed:**

```
destroys §1.4's regime split, and better wealth inputs plausibly deliver about 1.7× — enough to
make Genoa a *co-*sink, not enough to make demand the determinant of placement: a Chinese spice
sink needs 3.6–4.8×, i.e. 9.5–21.4% of all world spice demand at one node. (v2 wrote "1.7× where
4–5× is needed", which compressed two different thresholds into one comparison and understated
what inputs could buy.)
```

**Replaced by:**

```
destroys §1.4's regime split, and better wealth inputs plausibly deliver about 1.7× (measured:
`genua` becomes a co-sink at ×1.726) — enough to make Genoa a *co-*sink, not enough to make demand
the determinant of placement: a spice sink at any of **the four Chinese trade nodes —
`beijing`, `xian`, `canton`, `hangzhou`** — needs **3.6–4.7×**, i.e. **9.5–21.4%** of all world
spice demand at one node (`beijing` 3.59× / 9.5%, `girin` 3.93× / 9.8%, `hangzhou` 4.13× / 21.4%,
`xian` 4.57× / 12.3%, `canton` 4.74× / 17.6%; `yumen`, `chengdu` and `lhasa` need more still).
(v2 wrote "1.7× where 4–5× is needed", which compressed two different thresholds into one
comparison and understated what inputs could buy.)
```

### cape — §3.2
**Clears:** [unverified in v3.0] cleared by re-run

**Removed:**

```
the short route to Atlantic Europe (3 hops to the Channel against 7 via Alexandria; the flow
routes 24% of world spice supply through it — both figures **[unverified in v3.0]** — where v1's
potential never used it at all).
```

**Replaced by:**

```
is the short route to Atlantic Europe (Malacca reaches the Channel in 3 hops through the Cape
against 7 through Alexandria; the flow routes 24% of world spice supply through it) where v1's
potential never used it at all.
```

### W122-fix — §3.2
**Clears:** W122 (PARTIAL)

**Removed:**

```
spice demand at one node (`beijing` 3.59× / 9.5%, `girin` 3.93× / 9.8%, `hangzhou` 4.13× / 21.4%,
`xian` 4.57× / 12.3%, `canton` 4.74× / 17.6%; `yumen`, `chengdu` and `lhasa` need more still).
```

**Replaced by:**

```
spice demand at one node (`beijing` 3.59× / 9.5%, `hangzhou` 4.13× / 21.4%, `xian` 4.57× / 12.3%,
`canton` 4.74× / 17.6%; the four China-region nodes outside that set — `girin`, `yumen`, `chengdu`,
`lhasa` — need 3.9× to 10.6×).
```

### landcount-a — §3.3
**Clears:** [unverified in v3.0] cleared by re-run

**Removed:**

```
provinces (`cape_of_good_hope`) to 77 (`girin`) **[unverified in v3.0]** — a 4× spread with no
```

**Replaced by:**

```
provinces (`cape_of_good_hope`) to 77 (`girin`) — a 4× spread with no
```

### landcount-b — §3.3
**Clears:** [unverified in v3.0] cleared by re-run

**Removed:**

```
provinces) over the Paris node (`champagne`, 33) by `(68/33)^0.5 ≈ 1.44×`
**[unverified in v3.0]**. (v2 said a 77-province
```

**Replaced by:**

```
provinces) over the Paris node (`champagne`, 33) by `(68/33)^0.5 ≈ 1.44×`. (v2 said a 77-province
```

### W143+W144+W145+W146 — §3.5
**Clears:** W144, W145, W146 (REFUTED), W143 (PARTIAL)

**Removed:**

```
entered only when a price event pushes a good beneath the anchor, and the shipped events answer
how often that can happen: **12 of 30 goods** can be pushed strictly below 2.0 by a single vanilla
`change_price` event (grain and wine reach 0.625), three more — `gems`, `silk`, `wool` — land
*exactly on* 2.0 and so reach α = 1 but not the sublinear regime, and **11 goods have no negative
price event at all** and can never go sublinear in vanilla. (v2 said 13; the boundary is `< 2.0`,
and three goods sit on it exactly. All 101 `change_price` blocks in `events/`, `decisions/`,
`missions/` and `common/` were parsed; `history/` contributes only positive entries.) That is the point of having the regime: without it a
```

**Replaced by:**

```
entered only when a price event pushes a good beneath the anchor, and the shipped data answers
how often that can happen: **13 of 30 goods** can be pushed strictly below 2.0 by a single vanilla
`change_price` event (grain and wine reach 0.625), two more — `gems` and `silk` — land *exactly on*
2.0 and so reach α = 1 but not the sublinear regime, four have a negative event that does not reach
2.0, and **11 goods have no negative price event at all** and can never go sublinear in vanilla.
(All **154** `change_price` blocks were parsed — 93 in `events/`, 7 in `missions/`, 1 in `common/`
and **53 in `history/`, of which 13 are negative**, all in `history/countries/HAB - Austria.txt`.
The history route matters: `wool`'s largest single negative is that file's `NEW_DRAPERIES` at
−0.25 for 2.5 → **1.875**, against the −0.20 the same key carries in `events/PriceChanges.txt`, and
`change_price` entries are keyed, so 1.875 is the figure a campaign reaching 1540 holds. v2's 13
was right; v3.0 reached 12 by parsing four of the five trees.) That is the point of having the regime: without it a
```

### W156 — §3.9
**Clears:** W156 (PARTIAL)

**Removed:**

```
intent from the world state instead of authoring it: all wealth pulls (a rich non-sink node —
Beijing, Champagne, Sevilla — bends every edge around it as a net demander even though flow
passes through), the wealthiest places win, and the ends emerge and move when the wealth moves —
```

**Replaced by:**

```
intent from the world state instead of authoring it: all wealth pulls (a rich non-sink node —
`genua`, `gulf_of_siam` and `sevilla` rank 3rd, 2nd and 7th by node wealth and none of them is a
sink — draws more edges in than it sends out as a net demander even though flow passes through),
the wealthiest places win, and the ends emerge and move when the wealth moves —
```

### W155+W062 — §3.9
**Clears:** W155, W062 (regenerated under v4 wealth)

**Removed:**

```
free and remains the most self-coherent aggregate measured: **60.2%** edge-good agreement with
  the per-good graphs against `Φ_w`'s 53.4% (52.1% value-weighted). It was superseded on design
  grounds: its ends are artifacts of sweep scheduling rather than places — of its 18 end nodes at
  1444, 9 terminate no good at all and none of the demand capitals is among them — and its end
```

**Replaced by:**

```
free and remains the most self-coherent aggregate measured: **60.0%** edge-good agreement with
  the per-good graphs against `Φ_w`'s 53.5% (52.5% value-weighted). It was superseded on design
  grounds: its ends are artifacts of sweep scheduling rather than places — of its 18 end nodes at
  1444, 10 terminate no good at all and none of the demand capitals is among them — and its end
```

### W157+W158+W160+W162 — §3.13
**Clears:** W158, W160, W162 (PARTIAL) — two settled, one rescoped

**Removed:**

```
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
```

**Replaced by:**

```
**Open in the v4.0 wealth model.** One question, and it is a question rather than a number — §1.3
carries no value for it. Two others that v3.0 listed here are settled and have moved into §1.3.

- **What else multiplies `goods_produced`, and which side of the owner line does each source fall
  on?** §1.3's classification handles the sources observed so far — the owner's
  `global_trade_goods_size_modifier` (out, country-scoped) and `bonus_from_merchant_republics`
  (out, its value set by neighbouring countries' government forms) — and no 1444 province was
  observed carrying a *flat* `trade_goods_size` in the additive block. What is unenumerated is the
  rest of the surface: `trade_goods_size` and `trade_goods_size_modifier` appear in buildings,
  estate privileges, government reforms, church aspects, fervor, ages and event modifiers, and
  each source needs the §1.3 locality test applied to it before a modded or late-game province can
  be priced. Settling work: enumerate every source of both keys and classify each; the model needs
  the answer only for sources that can be live with no owner input.

*(Settled and moved: `local_production_efficiency` from a trade good is **outside** wealth —
Barcelona's production tooltip reads `Production Efficiency: +12.0% / From Technology: +2.0% /
Producing Glass: +10.0%`, so the engine books glass's +10% on production income, which wealth does
not compute. And `TAX_COEFF` **is** 1.0 across the development range — `Base: 0.49 (Yearly 6.00)`
at `base_tax` 6 and `Base: 0.16 (Yearly 2.00)` at `base_tax` 2, with `GP_COEFF` linear at four
levels.)*
```

### script-1.1 — §1.1
**Clears:** W006

**Removed:**

```
(`drain-orientation.md`; regenerated for v3.0 by `v3measure.py`). Where a property is proved for
```

**Replaced by:**

```
(`drain-orientation.md`; regenerated for v4.0 by `v4measure.py`). Where a property is proved for
```

### marker-3.10a — §3.10
**Clears:** marker rename

**Removed:**

```
Verified numerically **[unverified in v3.0]**: agreement to 5.7e-14
```

**Replaced by:**

```
Verified numerically **[unverified in v4.0]**: agreement to 5.7e-14
```

### marker-3.10b — §3.10
**Clears:** marker rename

**Removed:**

```
**This is also why propagation cannot be made per good.** Tested **[unverified in v3.0]**:
```

**Replaced by:**

```
**This is also why propagation cannot be made per good.** Tested **[unverified in v4.0]**:
```

### marker-3.11 — §3.11
**Clears:** [unverified in v3.0] cleared by re-run

**Removed:**

```
÷ 3 **plus policy and idea modifiers**, clamped to [2, 50]; nineteen countries **[unverified in v3.0]** are at the cap from
```

**Replaced by:**

```
÷ 3 **plus policy and idea modifiers**, clamped to [2, 50]; nineteen countries are at the cap from
```

### calibration — §3.13
**Clears:** [unverified in v3.0] cleared by re-run; W166/W167/W168 regenerated

**Removed:**

```
— span exactly 1..5, spearman(price, sinks) = −0.54 **[unverified in v3.0]**: α unclamped at exponent 2 (cloves α = 16),
```

**Replaced by:**

```
— span exactly 1..5, spearman(price, sinks) = −0.53: α unclamped at exponent 2 (cloves α = 16),
```

### calibration-b — §3.13
**Clears:** W168 (regenerated under v4 wealth)

**Removed:**

```
individually carrying <0.03% of world supply — up to about **0.15%** of a good's mass in total,
  not <0.03% — and drops **silk** to 99.97% reach and cloves to 99.997%, and it is one-snapshot
```

**Replaced by:**

```
individually carrying <0.03% of world supply — up to about **0.15%** of a good's mass in total,
  not <0.03% — and drops **silk** to 99.97% reach and cloves to 99.996%, and it is one-snapshot
```

### W171+W172 — §3.15
**Clears:** [unverified in v3.0] cleared by re-run

**Removed:**

```
**Ranked orientation (`score = s − c`, harmonic extension on empty nodes).** Wins every
sink–demand *alignment* statistic (ρ_val +0.281 against DRAIN's +0.053; 46.6% of top-decile nodes
are sinks against 14.1%) and fails on delivery: it is monotone (§3.2), so demand must rise along
every route — 83.3% of demand reachable, 34 orphan sinks, Genoa a cloves sink that cloves cannot
reach. It also posts **9 net-producer sinks** where DRAIN, LAP and FLOW all post zero, and 11–17
sinks per good against DRAIN's 1–8. *v2 said it "wins every sink statistic"; it does not — it wins
the alignment ones and loses the rest.*
Every RANK figure in this entry is **[unverified in v3.0]** — all were measured in the v2
validation pass and none was re-run by `v3measure.py`.
```

**Replaced by:**

```
**Ranked orientation (`score = s − c`, harmonic extension on empty nodes).** Wins every
sink–demand *alignment* statistic (ρ_val +0.283 against DRAIN's +0.055; 46.6% of top-decile nodes
are sinks against 14.1%) and fails on delivery: it is monotone (§3.2), so demand must rise along
every route — 83.3% of demand reachable, 34 orphan sinks, Genoa a cloves sink that cloves cannot
reach. It also posts **9 net-producer sinks** where DRAIN, LAP and FLOW all post zero, and 11–17
sinks per good against DRAIN's 1–8. *v2 said it "wins every sink statistic"; it does not — it wins
the alignment ones and loses the rest.*
```

### basin — §3.15
**Clears:** [unverified in v3.0] cleared by re-run

**Removed:**

```
chosen seeds and starves everything off a supply→seed path; 88.5% reach at its best tuning **[unverified in v3.0]**. Its
```

**Replaced by:**

```
chosen seeds and starves everything off a supply→seed path; 88.6% reach at its best tuning. Its
```

### graveyard — §3.15
**Clears:** W062 (regenerated under v4 wealth)

**Removed:**

```
most self-coherent aggregate measured (**60.2%** vs `Φ_w`'s 53.4%) and still acyclic for free —
but its ends are sweep-scheduling artifacts, not places (§3.9), and no parameter steers their
count. Retained as the measured coherence ceiling any future aggregate should be compared against.
The ceiling is 60.2%, not the 62.7% v2.0 and v2.1 both quoted: that figure predates the
deterministic sweep of §3.6 and was never regenerated after it.
```

**Replaced by:**

```
most self-coherent aggregate measured (**60.0%** vs `Φ_w`'s 53.5%) and still acyclic for free —
but its ends are sweep-scheduling artifacts, not places (§3.9), and no parameter steers their
count. Retained as the measured coherence ceiling any future aggregate should be compared against.
The ceiling is 60.0%, not the 62.7% v2.0 and v2.1 both quoted: that figure predates the
deterministic sweep of §3.6 and was never regenerated after it.
```

### W190 — §3.15
**Clears:** W190 (PARTIAL)

**Removed:**

```
demanders hits any chosen end count exactly, with **66%** vanilla-arrow agreement in the reproduced
construction. (v2.0 and v2.1 both quoted 69%; the count-follows-seeds behaviour reproduced, that
figure did not.) Rejected: it pins
```

**Replaced by:**

```
demanders hits any chosen end count exactly for γ ≤ 0.7 and any count up to six — at γ = 0.9 the
five- and six-mass fields both give four ends — with **66%** vanilla-arrow agreement at its best
(γ = 0.97, 105 of 159 arrows). (v2.0 and v2.1 both quoted 69% = 110 of 159, which is not reached at
any γ; the count-follows-seeds behaviour reproduced, that figure did not.) Rejected: it pins
```

### W165 — §3.13
**Clears:** W165 (PARTIAL)

**Removed:**

```
vanilla price events for 12 of 30 goods, unreachable for 11, and exactly on the boundary for 3.
```

**Replaced by:**

```
vanilla price events for 13 of 30 goods, unreachable for 11, and exactly on the boundary for 2.
```

### ver-1.5a — §1.5
**Clears:** editorial

**Removed:**

```
production income. Under v3.0's owner-agnostic wealth the exclusion is stronger still: `wealth(p)`
```

**Replaced by:**

```
production income. Under owner-agnostic wealth the exclusion is stronger still: `wealth(p)`
```

### ver-1.5b — §1.5
**Clears:** editorial

**Removed:**

```
still unknown, and under v3.0 it is also **moot**: nothing in the model reads that field, which is
```

**Replaced by:**

```
still unknown, and under this model it is also **moot**: nothing in the model reads that field, which is
```

### ver-2.7 — §2.7
**Clears:** editorial

**Removed:**

```
results are folded into §1.9, §2.4 and §3.6. Item 12 was dropped rather than run: under v3.0's
```

**Replaced by:**

```
results are folded into §1.9, §2.4 and §3.6. Item 12 was dropped rather than run: under the model's
```

### ver-3.3a — §3.3
**Clears:** editorial

**Removed:**

```
No colonial-nation dependency, no timeline restriction — and under v3.0 no owner dependency either.
```

**Replaced by:**

```
No colonial-nation dependency, no timeline restriction — and no owner dependency either.
```

### ver-3.3b — §3.3
**Clears:** editorial

**Removed:**

```
**Wealth is chosen for what the place is, not for who runs it.** Under v3.0 the owner-side terms are gone:
```

**Replaced by:**

```
**Wealth is chosen for what the place is, not for who runs it.** The owner-side terms are gone:
```

### ver-3.3c — §3.3
**Clears:** editorial

**Removed:**

```
What v3.0 removes is the volatility that was really about *ownership*:
```

**Replaced by:**

```
What the model removes is the volatility that was really about *ownership*:
```

### ver-3.4 — §3.4
**Clears:** editorial

**Removed:**

```
**Under v3.0 it does not belong in demand either.**
```

**Replaced by:**

```
**It does not belong in demand either.**
```

### W061b — §2.8
**Clears:** W061 (regenerated under v4 wealth)

**Removed:**

```
baseline is known — `Φ_w` agrees with the per-good graphs on 52.1% of value-weighted edge-goods —
```

**Replaced by:**

```
baseline is known — `Φ_w` agrees with the per-good graphs on 52.5% of value-weighted edge-goods —
```

### W153 — §3.8
**Clears:** W153 (regenerated under v4 wealth)

**Removed:**

```
measured, **90.9%** (5743 of 6320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. (v2 quoted 98.8%; that is v1's *Laplacian* figure, 6245/6320, carried across the operator change without being re-measured. The argument is unaffected — 90.9% is still most of the map — but the number was not v2's own.)
```

**Replaced by:**

```
measured, **90.6%** (5723 of 6320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. (v2 quoted 98.8%; that is v1's *Laplacian* figure, 6245/6320, carried across the operator change without being re-measured. The argument is unaffected — 90.6% is still most of the map — but the number was not v2's own.)
```

### W071-median — §1.10
**Clears:** W071 (measurement precision)

**Removed:**

```
(median 21.5% over the 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`)
```

**Replaced by:**

```
(median 17.9% over the 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`)
```

### W156-razed — §2.8
**Clears:** W156 (PARTIAL) — same mis-cast, second site

**Removed:**

```
| Razed China | Zeroing Beijing-node development relocates the sink in one solve |
```

**Replaced by:**

```
| Razed China | Zeroing `hangzhou`-node development relocates the sink in one solve — measured: the `Φ_w` sinks move from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`. `hangzhou`, not `beijing`, is China's wealth pole under §1.3: it is a `Φ_w` sink, `c_w` rank 3, node-wealth rank 12, and holds the richest single province in the game. Zeroing `beijing` (node-wealth rank 39) moves nothing |
```

### W156-mandate — §2.8
**Clears:** W156 (PARTIAL) — the owner-event case

**Removed:**

```
| Ming loses the Mandate | Beijing's pull collapses with its income |
```

**Replaced by:**

```
| Ming loses the Mandate | **Nothing moves on the day it happens.** The Mandate is an owner property and §1.3 reads none, so the demand vector is unchanged; the pull collapses only as the consequences reach `base_tax` and `base_production`. This row is the owner-agnosticism check, not a responsiveness check |
```

### W156-3.9 — §3.9
**Clears:** W156 (PARTIAL) — third site

**Removed:**

```
a razed Beijing, a dev-stacked capital, a colonizing Europe that flips the Cape (§1.6).
```

**Replaced by:**

```
a razed `hangzhou`, a dev-stacked capital, a colonizing Europe that flips the Cape (§1.6).
```

### W156-3.1 — §3.1
**Clears:** W156 (PARTIAL) — fourth site

**Removed:**

```
A horde razing Beijing moves the sink because the wealth moved.
```

**Replaced by:**

```
A horde razing `hangzhou` moves the sink because the wealth moved.
```

### 3.10-identity — §3.10
**Clears:** the 5.7e-14 figure — refuted as a measurement

**Removed:**

```
Verified numerically **[unverified in v4.0]**: agreement to 5.7e-14 across a node with mixed sinks, mixed collectors and the home-node penalty in play. So one scalar per node reproduces every country's income exactly, and the engine's own math does the rest.
```

**Replaced by:**

```
This is an **identity, not a measurement**: `powershare_C(n)` carries no `g`, so it factors out of the sum, and by §1.1's vocabulary the property is true by construction and carries no measurement. What a run can show is only that the implementation does the algebra in doubles — on `gulf_of_siam`, with 13 goods carrying local value, 12 of them sinking there, transfer eligibility varying per good and the off-home penalty on two of the three collectors, the two forms agree to a worst relative disagreement of **1.3e-16**, one unit in the last place. So one scalar per node reproduces every country's income exactly, and the engine's own math does the rest. *(v1 through v3.0 quoted "agreement to 5.7e-14" here, and 1.4e-14 below. Both are floating-point residuals of an exact identity, produced by a construction none of those documents states — a theorem decorated with an experiment, which is the confusion §1.1 exists to prevent.)*
```

### 3.10-pergood — §3.10
**Clears:** the 1.4e-14 and 5.96-ducat figures — restated

**Removed:**

```
**This is also why propagation cannot be made per good.** Tested **[unverified in v4.0]**: with propagation reading the one installed graph, the node-scalar model reproduces per-good truth to 1.4e-14. With power varying by good, it is off by 5.96 ducats on a node paying ~250 — because `powershare_C` stops factoring out. Keeping propagation on a single graph is load-bearing for Goal 7, not merely convenient.
```

**Replaced by:**

```
**This is also why propagation cannot be made per good.** Reading the one installed graph leaves the propagated term good-independent, so the identity survives it untouched — same construction, worst relative disagreement **1.3e-16**. Per-good propagation destroys it, because §1.9 reads a node's *downstream neighbours* and those are per good: `gulf_of_siam` has **eight distinct downstream sets across the 29 goods** — twelve goods leave it with none at all, five drain to `burma`, four to `{burma, canton, malacca}` — against `Φ_w`'s single `{canton}`. A country's power at the node stops being one number and `powershare_C` stops factoring out. Measured on the same construction: the node-scalar model then overstates **every** collector's income by **0.41%**, a total of 0.40 ducats on a node collecting 97.1. That is thirteen orders of magnitude above the float residual and it is a systematic bias in one direction, not rounding. Keeping propagation on a single graph is load-bearing for Goal 7, not merely convenient.
```

### W170 — §3.14
**Clears:** W170 — dangling citation created by the 3.10 fix

**Removed:**

```
*v1 and v2 both said 0.75 MB, which is the single-precision figure; the rest of the solver is double precision, as its own 5.7e-14 and 1.4e-14 tolerances show, so the natural implementation is twice that.*
```

**Replaced by:**

```
*v1 and v2 both said 0.75 MB, which is the single-precision figure; the rest of the solver is double precision — 29 goods x 80 x 80 entries at 8 bytes is 1.42 MB, and its residuals sit at 1e-16, one ULP of a double (§3.10) — so the natural implementation is twice what v1 and v2 recorded.*
```

### W169 — §3.14
**Clears:** W169 - MB vs MiB ambiguity in the survival-table size

**Removed:**

```
double precision — 29 goods x 80 x 80 entries at 8 bytes is 1.42 MB, and its residuals sit at 1e-16, one ULP of a double (§3.10)
```

**Replaced by:**

```
double precision — 29 goods × 80 × 80 entries at 8 bytes is 1,484,800 bytes, and its residuals sit at 1e-16, one ULP of a double (§3.10)
```
---

# Measurement provenance

Every number in v4.0 was regenerated this session by **`v4measure.py`** against the 1.37.5.0 Inca
install, on the corrected wealth field. `v4measure.py` is `v3measure.py` with one bug fixed: its
±1% noise check compared a *sorted* sink list against an *index-ordered* one, so it printed
`sink-set changes 5/5` and could never have printed the `0/5` v3.0 quoted from it. The comparison
is now set-based and prints `0/5`, which is what the spec says.

## Figures that moved with the solver fix

| Figure | v3.0 | v4.0 |
|---|---|---|
| World wealth, annual ducats | 10,572.4 | **10,594.8** |
| `Φ_w` agreement with the per-good graphs | 53.4% (52.1% weighted) | **53.5% (52.5%)** |
| `Φ_ord` agreement, deterministic sweep | 60.2% | **60.0%** |
| The `Φ_ord` → `Φ_w` coherence gap | 6.8 points | **6.5 points** |
| `Φ_ord` ends that terminate no good | 9 of 18 | **10 of 18** |
| Ordered node pairs connected by ≥1 good | 90.9% (5743/6320) | **90.6% (5723/6320)** |
| Largest \|`b_w`\| | 0.0226 | **0.0225** |
| Calibration spearman(price, sinks) | −0.54 | **−0.53** |
| Calibration `spices` sinks | Genoa and Doab | **Genoa** |
| Calibration cloves reach | 99.997% | **99.996%** |
| RANK ρ_val vs DRAIN's | +0.281 / +0.053 | **+0.283 / +0.055** |
| BASIN best reach | 88.5% | **88.6%** |
| Barbell, top vs bottom demand decile | 14% / 7% | **14.1% / 6.9%** |
| Coal reprice, world wealth after | 10,789 | **10,811** |

## Figures that did not move, re-checked anyway

Two sinks `hangzhou`/`english_channel` with `c_w` ranks 3 and 2 and node-wealth ranks 12 and 1;
eight sources at `c_w` ranks 44–75, mean degree 3.1 against 4.0; 1–8 sinks per good, mean 3.6;
k = 1 for 27 of 29; support 78–79; 100% reach, 29/29, zero orphan sinks; zero fallbacks; zero
orientation flips under permutation and zero exact key ties; 0 flips and 0/5 sink-set changes under
±1% noise; the α_Φ sink sequence 5→2→1→2→3→1; 13 edge flips at ×10⁻² and sink collapse at ×10⁻⁶;
45 owned latent-coal provinces flipping 10 of 159 `Φ_w` edges; Genoa a co-sink at ×1.726; 24% of
world spice supply through the Cape and Malacca 3 hops against 7; land counts 19/77/68/33 and the
2.01× / 1.44× slicing ratios; span 1..5; `hangzhou` holding the richest province at 27.0 against
Beijing's 19.5; nineteen countries at the caravan cap; 9 RANK net-producer sinks, 11–17 sinks per
good, 83.3% reach and 34 orphans; 66% gravity-kernel agreement.

## `[unverified in v3.0]` markers, resolved

Eight were cleared by re-running the measurement: the barbell (§2.8), the Cape's hop counts and
24% (§3.2), both node land-count pairs (§3.3), the nineteen countries at the caravan cap (§3.11),
the calibration span and spearman (§3.13), every RANK figure and BASIN's reach (§3.15).

**The last two were run, and both failed.** §3.10's `5.7e-14` and `1.4e-14` are floating-point
residuals of an **exact identity** — `powershare_C(n)` carries no `g`, so it factors out
algebraically and there is nothing to measure; on a stated construction the residual is 1.3e-16,
one ULP. And `5.96 ducats on a node paying ~250` names a node that does not exist: the largest
local trade value in the model is 112.6. Both are replaced by §1.1's own classification (true by
construction, carrying no measurement) plus a stated construction for the per-good-propagation
breakage, which is a **0.41% systematic overstatement of every collector's income**, not a
rounding error. **No measured figure in v4.0 is left unverified.** The only remaining
`[unverified in v4.0]` marker is §2.2's statement that *no* measurement supports a
native-network-simplex projection, which is a marker on an absence.

## What this document got wrong last time

`changes-v3.md` reported "the file grew from 74,860 to 99,323 bytes" for a file that is 104,457
bytes: its diff statistics were computed before the repairs listed in `claims-v3.md` landed and were
never regenerated. The statistics at the top of this document were computed **after** the last
edit, from the two files as they now stand on disk, by the same script that produced them
(`diffstat`, paragraph-level `difflib.SequenceMatcher` over blank-line-separated blocks).
