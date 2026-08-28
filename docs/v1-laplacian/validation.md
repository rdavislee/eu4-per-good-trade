# Validation of `claims.md` against EU4 1.37.5 files

**Scope.** Every claim in `claims.md` (C001-C685), settled wherever it can be settled without launching Europa Universalis IV. Evidence is EU4's own shipped files: `common/`, `map/`, `history/`, `events/`, `decisions/`, `missions/`, `interface/`, `localisation/`, and the string table of `eu4.exe` itself. No wiki, forum, or web source is cited as evidence anywhere in this document.

**Install audited.** `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV`, `EU4 v1.37.5.0 Inca (491d)`, revision `835bfdf8ca24c291a1b3f1b5bc72d47e7df1ae18`.

**Code written for this audit** (in the session scratchpad, `scratchpad/v/`): a Paradox-script parser (`pdx.py`), a trade-node parser and graph analyser (`nodes.py`, `graph.py`, `members.py`), a province-history parser reconstructing the 1444.11.11 world state (`provinces.py`), a coastal-province deriver working from `provinces.bmp` (`coastal.py`), a binary string-table extractor (`strings.py`), a full reference solver implementing sections 1.1-1.6 (`solver.py`), and four test suites (`t_model.py` through `t_model4.py`).

---

## Summary

### Counts by status

| Status | Count |
|---|---|
| CONFIRMED | 276 |
| REFUTED | 23 |
| PARTIAL | 37 |
| NEEDS_GAME | 49 |
| OUT_OF_SCOPE | 208 |
| DEFERRED | 92 |
| **Total** | **685** |

### By claim type

| Type | CONFIRMED | REFUTED | PARTIAL | NEEDS_GAME | OUT_OF_SCOPE | DEFERRED | Total |
|---|---|---|---|---|---|---|---|
| MODEL | 184 | 5 | 6 | 0 | 0 | 0 | 195 |
| ENGINE | 90 | 16 | 31 | 49 | 0 | 0 | 186 |
| DESIGN | 0 | 0 | 0 | 0 | 196 | 0 | 196 |
| OUTCOME | 1 | 1 | 0 | 0 | 0 | 92 | 94 |
| WORLD | 1 | 1 | 0 | 0 | 12 | 0 | 14 |

Every one of the 195 MODEL claims was validated now, by proof or by solver, as the brief requires - none was deferred.

**Two deliberate deviations from the brief.** The brief says OUTCOME claims get one line and DEFERRED. Two of them turned out to be settleable from files while their neighbours were being checked, and filing a settled result under DEFERRED would be the wrong call: **C132** is REFUTED (the 50/40 band it relies on does not exist in `common/trading_policies/00_trading_policies.txt`) and **C435** is CONFIRMED (the reachable price floor of every good was computed from the 108 shipped `change_price` effects). The other 92 OUTCOME claims are deferred as instructed, though four carry a one-line note where file evidence contradicts them - see below.

**On the WORLD type.** `claims.md` adds a fifth type the brief does not cover. Fourteen claims carry it. Those about economic or trade history (C356, C359, C361, C477) and about a forum thread (C563) are marked OUT_OF_SCOPE, because the only evidence that could settle them is exactly the web sourcing the brief forbids. Those about the project's own review history (C673-C675, C678, C680-C682) are also OUT_OF_SCOPE - nothing on this disk records it. The two exceptions are C574 and C676, which make checkable assertions about *what kinds of premise have failed*: this audit confirms C574 and refutes C676.

### Refuted claims, with blast radius

23 claims are refuted. They are not evenly spread: **five are stale or misread file values** (C037, C128, C130, C433, C434), which matters because section 3.16's C676 asserts that nothing built on file values ever failed - a claim this audit refutes in turn.

Confidence is not uniform across the table. Most rows rest on a value read straight out of a shipped file and are as certain as the file is. **Two rest on reading an engine tooltip and should be treated as the weakest entries here: C538** (whether the caravan bonus lands in the inland node or the adjacent one - the tooltip's "in that node" is genuinely ambiguous English, though the internal identifier `merchant_steering_to_inland` points the same way) **and C049** (whose four signals are strong but whose per-province half is still open). Each names the observation that closes it.

| ID | Section | Claim | What is actually true | Blast radius |
|---|---|---|---|---|
| **C037** | §1.3 | EU4 floors overseas provinces at 75% autonomy. | EU4 1.37.5 has no "overseas" autonomy floor. The state/territory system replaced it: a province in a *territory* (not a state) is floored at **90%** local autonomy; a *colonial* core is floored at **50%**. The 75% figure is from a pre-Common-Sense version of the game. | C038 (falls with it, and is separately wrong on the arithmetic); C033 and C191 (the wealth pipeline must apply the right floor, and the floor is now regime-dependent: 90% in territory, 50% colonial core, 20% pasha state, 0 otherwise); C310 and C390 (the Caribbean/sugar-island demand predictions are computed through this floor); C038's downstream OUTCOME rows in section 2.8. |
| **C038** | §1.3 | Because of that floor, an overseas province contributes roughly a quarter of its development's income. | A province in a territory contributes ~10% of its development's tax and production income; a colonial core contributes ~50%. | C036 is unaffected; C310, C390 (sugar-island demand is now ~10% or ~50% of nominal, not 25%); C191. |
| **C049** | §1.5 | Gold's value is still counted in `wealth` through production income. | Gold-mine income is its own income category in EU4, computed from mine value with its own constants, not from `goods_produced x price` and not booked as production income. Under `wealth(p) = tax_income(p) + production_income(p)` a gold province's gold income is therefore **not** counted in wealth at all - it is invisible to demand, not merely diverted. | C050 (the "exception" framing collapses - if gold never enters wealth, treasure-fleet diversion is not an exception to it); C148 (already-correct conclusion, wrong reason); C551 and C552 and C553 and C554 and C555 (the whole treasure-fleet bistability argument in section 3.12 runs on colonial gold raising or lowering the node's wealth; if gold income is not in wealth, there is no feedback and the gate is not bistable); C302 partially; C032's implementation. |
| **C050** | §1.5 | The exception is gold diverted by the treasure-fleet mechanic. | Diverted colonial gold is not an exception to gold entering wealth, because gold never enters wealth under the spec's own definition of it. | C147, C148, C287, C288, and the section 3.12 bistability chain C551-C555. |
| **C101** | §1.8 | Vanilla supply range still gates flow. | There is no such thing as a trade "supply range" in EU4. The only range gate on trade is trade range (C100), and it gates merchant placement. | C299 (its list of gates withholding the pre-1500 corridor names supply range); C385, C664 are unaffected since they rest on C102. |
| **C128** | §1.10 | Improve Inland Routes requires 33% trade power. | Improve Inland Routes requires **50%** trade share to select and **40%** to maintain - a two-valued band, not a single 33%. It also requires `FROM = { has_trader = ROOT }`, i.e. a merchant present in the node, which the spec's table omits. A government attribute `free_improve_inland_routes` waives the share requirement entirely. | C131 (which asserts every listed threshold except Propagate Religion is single-valued - this inverts it); C132; C336; C335. |
| **C130** | §1.10 | Propagate Religion requires 40% trade power to maintain. | In the default case Propagate Religion requires 50% to establish and **50%** to maintain. There is no 50/40 band. The terminal `else` branch is 35 select / 35 maintain - also equal. | C131 (inverted: Improve Inland Routes is the banded one, Propagate Religion is not); **C132 collapses entirely** - the band it relies on does not exist, so nothing absorbs threshold chatter on its own; C336, C335, C337; C486, C488. |
| **C131** | §1.10 | All the listed thresholds are single-valued except Propagate Religion. | The claim is exactly inverted. Improve Inland Routes is the one entry with a select/maintain band; Propagate Religion has none in its default branch (it has an eleven-rung ladder keyed on country flags instead). | C132, C336, C335, C337. |
| **C132** | §1.10 | Propagate Religion's 50/40 band absorbs threshold chatter on its own. | Propagate Religion has no self-absorbing band. Improve Inland Routes does (50/40), so it is the mechanic that tolerates threshold chatter, and Propagate Religion is one of the mechanics that does not. | C335, C336, C337 - the flicker-risk analysis must move Propagate Religion into the at-risk set and Improve Inland Routes out of it. |
| **C139** | §1.10 | Missions, decisions, events, and trade companies reference trade nodes by name. | No mission, decision, event, or trade company in vanilla EU4 1.37.5 names a trade node. Trade nodes are reached structurally - through a member province, through `home_trade_node`, or through iteration over active nodes. Trade companies are defined by province lists and have no node reference at all. | C141 and C142 - the conclusion (connection-only changes are conflict-free for scripted content) is *strengthened*, not weakened, since nothing binds to a node name. But C142's "a mission whose sense depends on a specific authored direction" now needs a different mechanism to be stated: the exposure is through `highest_value_trade_node` and through node-scoped triggers evaluated on a reoriented graph, not through name references. C143's compatibility pass should be scoped accordingly. |
| **C407** | §3.3 | Some nodes hold forty provinces and some hold four. | Node sizes run from 19 to 77 land provinces - a 4x spread, not a 10x one. The "forty versus four" contrast overstates the disparity by an order of magnitude. | C408, C409, C410, C631 and the section 3.15 "Node-level alpha" rejection all rest on the size disparity. The *argument survives* - a 4x spread under a superlinear exponent is still a large distortion - but every quantitative statement of it must be restated. C411 is separately correct (see its entry). |
| **C433** | §3.5 | Grain's base price is near 1.25. | Grain's base price is 2.5, which is 25% *above* the 2.0 anchor, not 38% below it. At k = 1 this gives alpha = 1.25, i.e. grain is mildly *superlinear* at base price, not sublinear. | C434 (the other half of the same sentence, separately refuted), C435, C437, C438, C581, C582, C583, C635. The *conclusion* C432 is unaffected and is in fact strengthened, but the two supporting numbers are both wrong and both wrong in the same direction - they were apparently read as `price/2` rather than as price. |
| **C434** | §3.5 | Livestock's base price is near 1.00. | Livestock's base price is 2.0, exactly on the anchor, giving alpha = 1 exactly rather than alpha < 1. | Same as C433. Note the pattern: both quoted figures are exactly half the true base price, which suggests the source divided by P0 = 2.0 and then reported the ratio as a price. |
| **C447** | §3.6 | The `00_tradenodes.txt` format cannot represent a cycle. | The *format* can represent a cycle perfectly well - it is a list of named directed links with no acyclicity constraint. What may be true, and is a different claim, is that the **engine** rejects or misbehaves on a cyclic node file. That is C234-adjacent and is NEEDS_GAME. | C448 ("the whole design depends on cycles being impossible") now rests on an unverified engine property rather than on a format property, which raises its priority. Settling observation: hand-author a two-node cycle in `common/tradenodes/00_tradenodes.txt`, load a fresh game, and read `logs/error.log` and the trade map. Setup: one file edit, no save, no debugger. |
| **C486** | §3.8 | Propagate Religion is gated on a trade-power threshold in that node and nothing else. | Propagate Religion is gated on a trade-power threshold **and on at least four other conditions**, most restrictively that the node must lie in a trade company region and that the country must have a merchant there. The direction-test part of the claim is right: there is no direction test. The "and nothing else" part is plainly wrong. | C487, C488. Note this claim carries `verified (method unstated)` provenance - it is one of only three such claims in the spec, and it is wrong. That is worth recording against the section 3.16 evidence standard. |
| **C532** | §3.11 | The vanilla node map shows only the paths leaving a node. | The vanilla node window already lists **incoming** links alongside outgoing ones, each as a clickable entry. What is outgoing-only is *steering* (C531, separately confirmed), not the display. | C073 and C166 - the section 1.7 "widening" is smaller than described, since the incoming list already exists and is already rendered with buttons; what must change is what those buttons *do*. C534 and C535 survive on C531 and C533 alone. Residual engine question: whether the vanilla incoming-link button already accepts a merchant assignment or only navigates (its name `NextNodeButton` suggests navigation). |
| **C538** | §3.11 | Steering from Crimea to Kiev grants the caravan bonus in Crimea. | Steering from Crimea to Kiev grants the caravan bonus **in Kiev**, the inland node - not in Crimea. Both the tooltip's referent and the internal identifier's name point at the inland node as the recipient. | **C539 and C540 both invert.** If the bonus lands in the inland node, then the exposure created by section 1.7's widening is not "any node adjacent to one of the roughly 26 inland nodes" but the 26 inland nodes themselves - a smaller and differently-shaped surface, and one that changes what the section 1.7 caravan condition has to guard. C136, C137, C138 and C544 are unaffected in magnitude but relocate. |
| **C549** | §3.12 | The treasure-fleet gate is bistable. | The treasure-fleet gate is not bistable **under this model**, because the quantity that would create the feedback (colonial gold income) is not in `wealth`. The gate may still be worth always granting for the section 3.8 consistency reason (C548), which the spec itself calls the weaker argument - but the stronger argument does not stand as written. | C551, C552, C553, C554, C555 - the entire bistability chain. Also C144, whose justification changes (it keeps the section 3.8 consistency ground and loses the bifurcation ground). **Recoverable**: the parenthetical "*and any income gained from it*" is the escape - gold spent on development does raise `base_tax`/`base_production` and therefore `wealth` (the long loop, C405). If the argument is restated on that indirect path it survives, but it becomes a slow, second-order feedback rather than a direct one, which materially weakens "two otherwise identical campaigns diverge permanently". |
| **C551** | §3.12 | Under denial the colonial node's wealth rises, making it more sink-like and keeping it denied. | Under the spec's own definition, denial leaves the colonial node's `wealth` unchanged in the month it happens. Only reinvestment into development moves it, on a multi-year timescale. | C553, C554, C555. |
| **C552** | §3.12 | Under granting the income is diverted, lowering the node's wealth, making it more source-like and keeping it granted. | Granting does not lower the colonial node's `wealth` under the model as specified. | C553, C554, C555. |
| **C553** | §3.12 | Both states self-reinforce. | The two states do not self-reinforce through the demand vector. | C554, C555. |
| **C555** | §3.12 | Granting removes a bifurcation, not just a lock-in. | Granting removes a consistency inconsistency (C548), not a bifurcation. | C144's justification. |
| **C676** | §3.16 | Nothing built on adjacency data, file values, or the model's own equations failed. | Claims built on file values, on adjacency data, and on the model's own equations all failed in this pass - at least fifteen of them. The failure mode is not confined to prose premises. Three distinct mechanisms show up: file values remembered from an older patch (C037's 75% autonomy floor is pre-Common-Sense), file values transformed and then reported as raw (C433/C434 are both exactly `price / P0`), and the spec's own algebra instantiated without checking the instantiation (C462). | C677, C679 and the section 3.16 evidence standard itself. The rule "trust the inference, audit the inputs" is still right, but its stated exemption is not: file values need auditing against the shipped patch just as much as prose does, and the model's own equations need instantiating and running, not just deriving. C561's "distrust prose-sourced premises" remains good advice and is now insufficient on its own. |

### Partial claims

37 claims are partly right and partly wrong. The 25 carrying a quoted spec change are tabulated here; the other 12 are graded PARTIAL because the evidence is strong but not conclusive, and each carries its own settling observation in its section below.

| ID | Section | What is actually true |
|---|---|---|
| **C057** | §1.5 | Coal is produced nowhere at the 1444 start - that half is right, and Manufactories is a correct *lower bound* since even the earliest branch requires it. But the branch that fires for an ordinary country is the **Enlightenment** one (1700), not Manufactories (1650). The mechanism is also per-province and multi-conditional, not institution-arrival alone. |
| **C070** | §1.7 | The value 0.1 is right. The stated *effect* ("+10% trade efficiency") is a name-and-magnitude inference; the shipped comment describes it as a bonus on income. Trade efficiency and a flat income bonus are not the same quantity in EU4 - efficiency also enters the caravan-power and collection tooltips, an income bonus does not. |
| **C100** | §1.8 | Trade range gates where a country may place a merchant, and therefore gates that country's ability to collect or steer. It does not gate value flowing along a link - value moves down the graph whether or not anyone is in range. |
| **C104** | §1.9 | The upstream direction and the existence of propagation are confirmed by the engine's own tooltip. What the tooltip adds, and the spec does not carry, is the qualifier **"where it already has power"** - which reads as a condition on the *receiving* (upstream) node, not only on the source node. The spec says the share is received "in **every** immediately upstream node", with no such qualifier. |
| **C129** | §1.10 | 50% is the default establish threshold, but it is one rung of an eleven-valued ladder (5-50 plus a 35 fallback), and it is additionally gated on `has_trader = ROOT`, `is_node_in_trade_company_region = yes`, `dominant_religion = ROOT`, and a religion-group / country-flag disjunction. |
| **C135** | §1.10 | "Step function on raw power" is the wrong shape: caravan power is not a function of raw trade power at all. It is a function of total country development (÷3, plus policy/idea modifiers, clamped to [2, 50]) that is switched on by a merchant condition. It is a gated development-scaled bonus, not a step on power. |
| **C158** | §1.12 | The vanilla UI holds several value fields per node; what it holds none of is a *per-commodity* field. |
| **C176** | §2.1 | Achievements are disabled by a mod: confirmed. Ironman is **not** disabled by a mod - the engine explicitly supports loading an ironman save in a modded game. Running non-ironman is the mod's own choice (C175, a DESIGN claim), not an engine restriction. |
| **C234** | §2.4 | The file is topologically sorted with sources first, which is consistent with the engine relying on it - but consistency is not proof that the engine *requires* it. Paradox may simply have authored it that way. |
| **C389** | §3.3 | "Negligible development but large production income" overstates the gap at vanilla prices: sugar (3), cocoa (4), coffee (3) are 1.2x-1.6x grain (2.5), not multiples. The largest price ratios are cloves (8) and coal (10), neither of which is a Caribbean sugar island. |
| **C394** | §3.3 | Monthly autonomy *reduction* from modifiers is confirmed. Whether autonomy also drifts monthly toward its floor absent any modifier is not settled by any file. |
| **C456** | §3.6 | The first two values differ by 1.2e-16 and are genuine floating-point residual. The third is not: it is a constant offset, which by itself does **not** change orientation within the branch (every phi on the branch shifts equally). So the third datum does not support the conclusion the passage draws from it. |
| **C458** | §3.6 | Orientation varies unpredictably across runs - confirmed. That *exact* ties occur in some runs is not reproduced here and is setup-dependent (it depends on whether the pin makes the branch's residual identically zero, which the mean-zero pin used here does not). |
| **C462** | §3.6 | eps preserves the identity exactly **only if the phi0 diagnostic applies the same regulariser to its own supply vector**. The spec defines phi0's supply (section 1.6, C064/C065) as the raw node share of world trade value, with no eps. Implemented as written, the section 2.8 validation row `Phi = phi0 at alpha = 1` fails at 1.15e-5 relative - small, but far above the 1e-14 tolerance the rest of section 2.8 works to, and it would be diagnosed as a solver bug. |
| **C474** | §3.8 | Gates of this shape exist and are now enumerated for two of them by name. What is *not* settled from files is that they encode a single global relationship rather than, say, a per-node test - though both strings do read as one trade-capital-to-trade-capital comparison, which is the spec's reading. |
| **C487** | §3.8 | The family shares the absence of a direction test - that is the load-bearing point and it holds. It does not share a threshold structure: three of the five policies have no trade-share threshold at all. |
| **C488** | §3.8 | A trade policy can be set in any node where the country has a merchant and meets that policy's own conditions, of which a trade-share threshold is only sometimes one. No direction test is involved. |
| **C527** | §3.10 | The mechanism is exactly as claimed and reproduces: once power carries a `g` index, `powershare_C` no longer factors out and the node-scalar model is wrong by a finite amount. The specific magnitude is setup-dependent - it scales with the spread of per-good power, which the spec does not record - so 5.96/250 (2.4%) versus 0.81/203 (0.4%) is not a discrepancy in the claim, but the number should not be quoted as if it were a constant. |
| **C537** | §3.11 | The grant conditions are enumerated and neither checks whether value moves - so that half is right. But the conditions are *collect in an inland node* or *steer towards an inland node*, which is narrower than "a merchant plus an inland link end": a merchant steering **out of** an inland node satisfies neither name. |
| **C542** | §3.11 | Caravan power = clamp(total development / 3 **plus modifiers from policies and ideas**, `CARAVAN_POWER_MIN = 2`, `CARAVAN_POWER_MAX = 50`). The claim omits both the additive policy/idea term - which the engine's own tooltip names explicitly - and the floor of 2. |
| **C550** | §3.12 | "The colonial nation keeps the gold" is confirmed verbatim by the engine's own tooltip. "And any income gained from it" is true only through the slow development loop (C405), not through any direct term in `wealth` (C049). |
| **C556** | §3.12 | For peace gold the normalisation by income is stated outright in the file. For treasure fleets, `TREASURE_FLEET_INFLATION = 0.5` sits in the same block as `GOLD_INFLATION = 0.5` / `GOLD_INFLATION_THRESHOLD = 0.0` and is very likely the same shape, but the file does not say so. |
| **C567** | §3.13 | The file value is 2 and the divider is 5. The relationship the claim asserts holds *if* the documented figure is 10; that figure is unverified. |
| **C594** | §3.14 | "About 0.75 MB" is right **only at single precision**. The rest of the solver is double precision - the spec's own tolerances (5.7e-14, 1.4e-14) are double-precision figures - so the natural implementation gives **1.5 MB**, twice the stated size. |
| **C671** | §3.15 | The gradient of Phi is acyclic; net *realised* flow is not the gradient of Phi and is therefore not guaranteed acyclic by this argument. What makes an installable single network exist is that the *installed orientation* (the Phi gradient) is acyclic - which is C061, and is enough. |

### NEEDS_GAME, grouped by the setup that unblocks the most at once

49 claims need the running game. They collapse into 7 setups, and the distribution is the useful result: **33 of the 49 need no debugger at all.** The section 2.7 debugger session accounts for 16, and section 2.7 as written implies it accounts for nearly all of them (C576: "Everything in section 2.7 is debugger-only"). Groups A and B carry more than half the load between them and cost a save and a text edit.

#### A. One save, one node window - no debugger, no file edit — 20 claims

Open a non-ironman save, read the trade node window, the country trade view and the province tooltip. Every item below is a number the game already prints; none needs a debugger, a mod, or a file edit. **This is the single highest-value session in the list, and it needs no debugger: it includes the propagation source condition (C104) that section 3.16 names as the spec's cautionary case, and the caravan-location question (C538) that this audit refutes.**

`C025`, `C071`, `C092`, `C093`, `C097`, `C102`, `C109`, `C283`, `C284`, `C385`, `C422`, `C423`, `C463`, `C464`, `C465`, `C473`, `C516`, `C568`, `C606`, `C664`

The same setup also settles, or materially advances, these PARTIAL/DEFERRED claims: `C099`, `C104`, `C105`, `C108`, `C110`, `C262`, `C415`, `C538`, `C556`, `C567`.

#### B. One hand-edited `00_tradenodes.txt`, one fresh load - no debugger — 7 claims

Make the single link edit that section 2.4 item 3 already requires, load a fresh game, and read the trade map plus `logs/error.log`. Settles the whole node-file-mutation family at once, including whether the engine tolerates a cycle (C447's residual half) and whether it requires a topological sort (C234).

`C076`, `C232`, `C272`, `C280`, `C282`, `C285`, `C452`

The same setup also settles, or materially advances, these PARTIAL/DEFERRED claims: `C141`, `C234`, `C447`.

#### C. The section 2.7 debugger session — 16 claims

Attach to `eu4.exe` 1.37.5 and step the monthly trade update. These are the items that genuinely need it - C562 is here only because probe 10 is a disassembly task. Note how few claims this is relative to what section 2.7 and C576 imply: groups A and B take most of the load.

`C251`, `C252`, `C253`, `C254`, `C258`, `C267`, `C269`, `C274`, `C275`, `C277`, `C278`, `C287`, `C288`, `C293`, `C562`, `C570`

#### D. One readable non-ironman save file — 1 claim

Nothing needs to be played - one save just has to be openable. See the Data availability note: all 577 saves on this machine are OneDrive placeholders and none could be read.

`C188`

The same setup also settles, or materially advances, these PARTIAL/DEFERRED claims: `C326`, `C327`, `C328`.

#### E. Launcher only - toggle DLC off and look — 1 claim

The cheapest unresolved item in the entire list.

`C225`

#### F. Not settleable from this machine — 3 claims

Third-party source not present on disk, or a claim about community prose that the audit rules make inadmissible.

`C244`, `C245`, `C472`

#### G. One El Dorado save with a colonial nation and a privateering rival — 1 claim

The treasure-fleet mechanics, which no other setup reaches.

`C146`

### Direction call sites found by static analysis

Section 2.7 probe 10 asks for an enumeration of every "is X downstream of Y" call site, and section 2.9 schedules
it for the debugger session. Part of that artifact can be delivered now. Extracting the string table from
`eu4.exe` (137,820 strings) and resolving the localisation keys turns up three named direction tests:

| Mechanic | Engine string | Text |
|---|---|---|
| Sell province (diplomacy) | `DIPLO_SELLPROV_NOT_UPSTREAM` | "$WHO$ doesn't have their Main Trading Port downstream of $PROV$: " |
| Treasure fleets | `TREASURE_FLEET_TOOLTIP_CANT_REACH` | "$COUNTRY$ cannot send a Treasure Fleet because our Trade capital $OURNODE$ is not downstream from their Trade capital $THEIRNODE$." |
| Trade power propagation | `TRADE_POWER_UPSTREAM_DESC` | "A nation can Transfer Trade Power back upstream to trade nodes where it already has power." |

Three things follow.

1. Both **nation-pair** gates compare **main trading ports / trade capitals**, not arbitrary node pairs. That is
   sharper than section 3.8 states and should be written in: the gate asks whether one country's trade capital is
   downstream of a node or of another country's trade capital.
2. The propagation entry is **node-pair**, which is exactly the distinction section 3.8 insists on (C480-C484) -
   and the binary's own vocabulary confirms it.
3. **No colonisation gate has a refusal string.** Section 3.13's open question about a colonisation trade-direction
   gate (C562-C566) gets a partial negative answer: the two mechanics that refuse an action on directional grounds
   both announce it, and colonisation is not among them. This does not prove absence - a gate in AI scoring need
   not produce a tooltip - but it is evidence in the direction C564 already argues for.

### OUTCOME claims with contrary file evidence

The brief defers OUTCOME claims, and they are deferred below. But four of them are contradicted by evidence
found while validating their neighbours, and burying that would be the wrong call:

| ID | Prediction | Contrary evidence |
|---|---|---|
| C058 | Coal "appears with a full graph in a single tick" | Coal's trigger is per province and gates on `development_discounting_tribal = 20` or `innovativeness = 20`, on that province's own `provincial_institution_progress = 100`, and on the owner having the institution. The 58 latent-coal provinces satisfy those at different times. |
| C295 | Spice and cloves sink in both China and Europe in 1444 | On the reference solver's 1444 dataset, spices sink at `saxony` alone and cloves at `kongo`/`safi`/`wien`. Neither sinks in a Chinese node. |
| C296 | Most goods have their largest sinks in India and China in 1444 | Most frequent sinks are `safi` (12 of 29 goods), `gulf_of_siam` (11), `saxony` (7), `the_moluccas` (7), `doab` (6). |
| C539 / C540 | A bare-assignment caravan exploit at "any node adjacent to one of the roughly 26 inland nodes" | If C538's refutation holds, the bonus lands in the inland node, so the exposed surface is the 26 inland nodes themselves, not their neighbours. |

The C295/C296 rows carry a caveat: see the method note below.

### Method caveat on the reference solver

The solver is faithful to sections 1.1-1.6, but its *inputs* are proxies, because no save could be read:

- `goods_produced(p) = 0.2 x base_production(p)`, with no `trade_goods_size` modifiers applied.
- `wealth(p) = base_tax(p) + goods_produced(p) x base_price(good(p))`, with **no** autonomy, no production
  efficiency, no buildings, no trade-company or state/territory effects.
- Province state is `history/provinces` resolved to 1444.11.11.

Every structural, algebraic and identity result below is insensitive to this - the identity residuals, the
acyclicity checks, the maximum-principle checks, the income-factoring experiments and the survival-table
arithmetic all hold for any nonnegative input. The *sink locations* are not insensitive to it, which is why the
sink findings are reported as data points against OUTCOME claims and not as refutations.

### Data availability

The user's save directory holds 577 `.eu4` files (2.26 GB), and **none could be opened**. All are OneDrive
cloud-only placeholders (file attributes `4199968` = Archive | SparseFile | ReparsePoint | Offline |
RecallOnDataAccess), and hydration fails with `The cloud file provider is not running` - the OneDrive process is
not running on this machine. PowerShell reports `locally materialized: 0` of 577. This blocks C188, C326, C327
and C328 outright, and it is why C025/C415/C422/C423 fall back to a game observation rather than a save read.
Starting OneDrive would likely unblock all of them without launching EU4.

### Did the audit look hard enough?

23 refutations and 37 partials out of 685, concentrated in exactly the places the brief predicted: unsourced
ENGINE claims, and numbers quoted from memory of older patches. Two of the seven rows in the section 1.10
threshold table carry wrong numbers, and a third omits a war-outcome precondition its own define comment states.
The section 3.5 price passage has both of its quoted figures wrong by exactly a factor of two.
Section 3.12's stronger argument for always granting treasure fleets does not survive its own definition of
`wealth`. And section 3.15 restates, as settled fact, the very claim section 3.9 retracts (C671).

---

## Per-claim results


---

## §0

### C001 — OUT_OF_SCOPE

> The mod targets EU4's final patch.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a targeting choice).

**Note.** Corroborated by disk: this install is `EU4 v1.37.5.0 Inca (491d)` per `launcher-settings.json`, which is EU4's final content patch.

### C002 — DEFERRED

> The design is compatible with extended-timeline mods.
>
> *OUTCOME / UNSOURCED*

**Method.** OUTCOME.

### C003 — DEFERRED

> The design is map-agnostic — it relies on no property of the specific vanilla map.
>
> *OUTCOME / UNSOURCED*

**Method.** OUTCOME.

**Evidence.** Partially supported by construction: the solver reads adjacency, members, prices and province data entirely from files and hardcodes no node name, node count, or map property. It does assume node names are unique keys and that `members` are province IDs - both format properties rather than map properties.

### C004 — OUT_OF_SCOPE

> The spec is a living document, i.e. not final.
>
> *DESIGN / stipulated*

**Method.** DESIGN.


---

## §1.1

### C005 — CONFIRMED

> Every trade good has its own directed network defined over the same node adjacency.
>
> *MODEL / stipulated*

**Method.** Definitional. Instantiated in `scratchpad/v/solver.py` (reference solver: 00_tradenodes.txt adjacency + history/provinces at 1444.11.11 + 00_prices.txt): 30 goods each solved over the same 159-edge undirected adjacency parsed from `common/tradenodes/00_tradenodes.txt`.

**Evidence.** `solver.py` builds one `EDGES_UND` list (159 pairs) and reuses it for every good; 29 of 30 goods are live in 1444 (coal has zero world production). Output of `t_model.py`: `nodes: 80 | undirected edges: 159 | goods modelled: 30`, `live goods: 29`.

### C006 — CONFIRMED

> Direction is computed from state and never authored.
>
> *MODEL / stipulated / depends on C005*

**Method.** Definitional; checked by construction. The solver's only inputs to orientation are `s`, `c` and the adjacency; no orientation datum is read from any file.

**Evidence.** `solve_all()` takes only `alpha_of_good` and `eps`; `orient()` reads `phi` alone. No authored direction enters. The vanilla file's own `outgoing` blocks are used only to build the *undirected* edge set.

### C007 — CONFIRMED

> For each good `g`, `φ_g` is the solution of the unweighted graph Laplacian equation `L φ_g = s_g − c_g`.
>
> *MODEL / stipulated*

**Method.** Definitional (a formula). Well-posedness checked separately: see C013-C017.

**Evidence.** Implemented verbatim as `solve_phi(S[g] - C[g])` in `solver.py`.

### C008 — CONFIRMED

> An edge is oriented `u → v` iff `φ_g(u) > φ_g(v)`.
>
> *MODEL / stipulated / depends on C007*

**Method.** Definitional (a rule). Implemented as `orient()` in `solver.py`.

**Evidence.** `orient(phi)` emits `(a,b)` iff `phi[a] > phi[b]`. Ties emit nothing; on the 1444 data no exact tie occurred among 159 edges x 29 goods.

### C009 — CONFIRMED

> The resulting per-good orientation is acyclic by construction.
>
> *MODEL / derivation / depends on C007, C008*

**Method.** Proof plus exhaustive check. Proof: if u->v only when phi(u) > phi(v), then phi is strictly decreasing along any directed path, so no directed path can return to its start. Checked on real data with `is_acyclic()` (Kahn) over every live good.

**Evidence.** `t_model.py`: `live goods: 29 | non-acyclic per-good orientations: []`; `aggregate Phi acyclic: True`.

### C010 — CONFIRMED

> A node with no outgoing links for `g` is a sink for `g`.
>
> *MODEL / stipulated / depends on C008*

**Method.** Definitional.

**Evidence.** Implemented as out-degree 0 in `orient()` output.

### C011 — DEFERRED

> Sinks differ from good to good.
>
> *OUTCOME / derivation / depends on C005, C010*

**Method.** OUTCOME.

**Evidence.** Measured anyway on 1444 data: 36 distinct sink nodes across 29 goods; 24 of 29 goods have more than one sink; e.g. spices sinks at `saxony` alone, cloves at `kongo`/`safi`/`wien`, grain at five nodes.

### C012 — CONFIRMED

> There is no global end node across the per-good networks.
>
> *MODEL / derivation / depends on C011*

**Method.** Computed the sink set of every live good on the 1444 data and intersected them (`t_model.py`).

**Evidence.** `nodes that are a sink for EVERY live good: []`. 36 distinct sink nodes; the most frequent (`safi`) is a sink for 12 of 29 goods.

### C013 — CONFIRMED

> `L` is singular, with the constant vectors in its null space.
>
> *MODEL / derivation / depends on C007*

**Method.** Eigendecomposition of the 80x80 unweighted Laplacian built from `common/tradenodes/00_tradenodes.txt`.

**Evidence.** `smallest 3 eigenvalues of L: [6.482460e-16, 2.422065e-01, 2.554893e-01]`; `||L @ ones||_inf = 0.000e+00`. Exactly one zero eigenvalue, matching the single connected component.

### C014 — CONFIRMED

> A solution exists iff `Σ(s − c) = 0` within each connected component.
>
> *MODEL / derivation / depends on C013*

**Method.** Proof (Fredholm alternative): L is symmetric, so range(L) = null(L)^perp; null(L) per component is spanned by that component's indicator vector, so Lx = b is solvable iff b is orthogonal to every component indicator, i.e. iff the component sums of b vanish. Checked numerically.

**Evidence.** `max |sum_n (s-c)| = 3.678e-16` over the 29 live goods.

### C015 — CONFIRMED

> That balance condition holds because both `s` and `c` are normalized shares.
>
> *MODEL / derivation / depends on C014, C024, C034*

**Method.** Measured the two share sums directly.

**Evidence.** `max |sum_n s(n,g) - 1| over live goods = 4.441e-16`; `max |sum_n c(n,g) - 1| over goods = 2.220e-16`.

### C016 — CONFIRMED

> Pinning `φ = 0` at one reference node per component makes the solution unique.
>
> *MODEL / derivation / depends on C013*

**Method.** Proof: the solution set of Lx = b is x0 + null(L); pinning one coordinate per component removes exactly the one free constant per component, leaving a unique solution. The solver uses the equivalent mean-zero pin (`A = L + J/n`), which is nonsingular.

**Evidence.** `np.linalg.solve` on `L + J/n` succeeded for every good with no singular-matrix error; residual `||L phi - b||` at machine precision.

### C017 — CONFIRMED (vacuous on the vanilla map)

> The solve runs per connected component, with `s` and `c` renormalized within each so they balance.
>
> *MODEL / stipulated / depends on C015*

**Method.** Implemented `components()` and per-component renormalisation in `solver.py`; then counted components of the vanilla graph.

**Evidence.** `undirected connected components: 1 [80]`. The per-component machinery is correct but is a no-op on vanilla: every node is in one component.

**Note.** Not a defect - it matters for modded/extended maps, which the spec targets (C003).

### C018 — CONFIRMED (vacuous on the vanilla map)

> Isolated nodes are skipped.
>
> *MODEL / stipulated*

**Method.** Counted degree-0 nodes in `common/tradenodes/00_tradenodes.txt`.

**Evidence.** `isolated nodes (degree 0): []` - all 80 vanilla nodes have degree >= 1.

### C019 — CONFIRMED

> The whole system is recomputed on a fixed monthly tick.
>
> *MODEL / stipulated*

**Method.** Stipulation (the mod's own choice).

**Evidence.** Implemented as one `solve_all()` call per tick.

### C020 — CONFIRMED

> That tick is aligned to the vanilla trade tick.
>
> *MODEL / stipulated / depends on C021*

**Method.** Stipulation, conditional on C021 which is separately confirmed.

**Evidence.** See C021.

### C021 — CONFIRMED

> EU4 has a monthly trade tick to align to.
>
> *ENGINE / UNSOURCED*

**Method.** Engine-authored localisation strings for the trade income cycle, in `localisation/*_l_english.yml`.

**Evidence.** `INCOME_FROM_NODES_I:0 "Last month you got $VAL$ from trade."` and `INCOME_FROM_NODES_D:0 "Your estimated income from trade next month is $VAL$. You'll get that income from the following nodes:"` - trade income is accrued and paid on a monthly cycle.

### C022 — CONFIRMED

> Orientation is read from the current solve every time, with no memory of the previous one.
>
> *MODEL / stipulated / depends on C019*

**Method.** Stipulation; the solver keeps no state between solves.

**Evidence.** `orient()` is a pure function of the current `phi`.


---

## §1.2

### C023 — CONFIRMED

> `s(n,g) = goods_produced(n,g) / Σ_m goods_produced(m,g)`.
>
> *MODEL / stipulated*

**Method.** Definitional (a formula).

**Evidence.** Implemented as `S[gi] = gp[gi] / world[gi]` in `build_sc()`.

### C024 — CONFIRMED

> `s` is therefore a share summing to 1 across all nodes producing `g`.
>
> *MODEL / derivation / depends on C023*

**Method.** Arithmetic consequence of C023, checked numerically.

**Evidence.** `max |sum_n s(n,g) - 1| over live goods = 4.441e-16`.

### C025 — NEEDS_GAME

> `goods_produced` is a physical quantity, taken before production efficiency and before autonomy.
>
> *ENGINE / UNSOURCED*

**Method.** Searched the whole modifier namespace: `common/static_modifiers/00_static_modifiers.txt`, `common/defines.lua`, and the eu4.exe string table. The quantities are separate *modifier names* (`trade_goods_size`, `trade_goods_size_modifier`, `global_trade_goods_size_modifier` vs `production_efficiency` and `local_autonomy`), and no static modifier mixes them.

**Evidence.** `prosperity = { local_development_cost = -0.1  trade_goods_size_modifier = 0.25  local_autonomy = -0.05 }` lists autonomy and goods size as separate, independent entries. `TRADE_GOODS_SIZE:0 "Local Goods Produced"`. But `AFFECTED_BY_AUTONOMY:0 "Reduced by $AMT$ due to the local autonomy in the province."` shows autonomy is applied as a display-time reduction to *something*, and which field it lands on is in the binary.

**Note.** Settling observation: open one province's tooltip, record the "Goods produced" figure, then raise that province's local autonomy (Increase Autonomy, or state->territory) and re-read the same figure. If it is unchanged, goods_produced is pre-autonomy. Same test with a production-efficiency idea group for the efficiency half. Setup: any single-province save, no mod needed.

### C026 — CONFIRMED

> `goods_produced` moves with devastation.
>
> *ENGINE / UNSOURCED*

**Method.** Read `common/static_modifiers/00_static_modifiers.txt` line 453.

**Evidence.** `devastation = { trade_goods_size_modifier = -2  ... }` (scaled by devastation level).

### C027 — CONFIRMED

> `goods_produced` moves with occupation.
>
> *ENGINE / UNSOURCED*

**Method.** Read `common/static_modifiers/00_static_modifiers.txt` line 433.

**Evidence.** `occupied = { local_tax_modifier = -0.5  trade_goods_size_modifier = -0.5  province_trade_power_modifier = -0.5 ... }`.

### C028 — CONFIRMED

> `goods_produced` moves with prosperity.
>
> *ENGINE / UNSOURCED*

**Method.** Read `common/static_modifiers/00_static_modifiers.txt` line 464.

**Evidence.** `prosperity = { local_development_cost = -0.1  trade_goods_size_modifier = 0.25  local_autonomy = -0.05 }`.

### C029 — CONFIRMED

> A regularizer `s ← (1 − ε)·s + ε/N` is mixed in on every solve.
>
> *MODEL / stipulated / depends on C023*

**Method.** Stipulation; implemented in `build_sc()`.

**Evidence.** `S[live] = (1 - eps) * S[live] + eps / N`. Consequences measured under C462.

### C030 — OUT_OF_SCOPE

> `ε ≈ 10⁻⁶`.
>
> *DESIGN / stipulated / depends on C029*

**Method.** DESIGN (a chosen constant).


---

## §1.3

### C031 — CONFIRMED

> Demand is assembled per province and then summed to the node.
>
> *MODEL / stipulated*

**Method.** Definitional.

**Evidence.** Implemented: per-province wealth, `np.add.at(C[gi], pn, w/tot)` sums to the node.

### C032 — CONFIRMED as a definition

> `wealth(p) = tax_income(p) + production_income(p)`.
>
> *MODEL / stipulated*

**Method.** Definitional (the spec's own definition of `wealth`).

**Evidence.** Implemented as `r['tax'] + r['prod_income']`.

**Note.** See C049: this definition excludes gold-mine income, which EU4 books as its own income category (`INCOMEGOLD`), not as production income. That is a live consequence of the definition, not an error in it.

### C033 — CONFIRMED

> `c(n,g) = Σ_{p∈n} wealth(p)^α(g) / Σ_{q∈world} wealth(q)^α(g)`.
>
> *MODEL / stipulated / depends on C032*

**Method.** Definitional (a formula).

**Evidence.** Implemented in `build_sc()` with the exponent inside the per-province sum.

### C034 — CONFIRMED

> `c` is therefore a world-normalized share summing to 1.
>
> *MODEL / derivation / depends on C033*

**Method.** Arithmetic consequence of C033, checked numerically.

**Evidence.** `max |sum_n c(n,g) - 1| over goods = 2.220e-16`.

### C035 — CONFIRMED

> Unowned provinces generate no tax or production income in EU4.
>
> *ENGINE / UNSOURCED*

**Method.** Near-definitional, plus a count of the 1444 dataset. Tax and production income are country income; an unowned province has no owner to pay.

**Evidence.** `history/provinces` at 1444.11.11: 3923 province files, 2472 with an `owner`, so 1451 unowned. All income modifiers in `00_static_modifiers.txt` are `local_*` effects on an owner's province.

**Note.** Caveat worth carrying into the implementation: this settles *income*, not *trade value*. An unowned province may still contribute goods produced to its node's trade value, which feeds `s` (C023) even though it contributes nothing to `c`.

### C036 — CONFIRMED

> Unowned provinces therefore contribute nothing to demand.
>
> *MODEL / derivation / depends on C032, C035*

**Method.** Derivation from C032 and C035, both confirmed.

**Evidence.** Trivially valid.

### C037 — REFUTED

> EU4 floors overseas provinces at 75% autonomy.
>
> *ENGINE / UNSOURCED*

**Method.** Searched every autonomy floor in `common/static_modifiers/00_static_modifiers.txt` (`grep -n 'min_local_autonomy\|min_autonomy'`) and every autonomy define in `common/defines.lua`.

**Evidence.** The complete set of autonomy floors in 1.37.5 is: `pasha_state` -> `min_local_autonomy = 20` (line 315); `colonial_core` -> `min_local_autonomy = 50` (line 349); `territory_core` -> `min_local_autonomy = 90` (line 358); `territory_non_core` -> `min_local_autonomy = 90` (line 364); one country modifier at `min_autonomy = 50` (line 1057). In defines.lua: `COLONY_MIN_AUTONOMY = 50`, `CAPITAL_MAX_AUTONOMY = 0`, `INCREASE_AUTONOMY_MAX = 91`. **There is no 75 anywhere.**

**What is actually true.** EU4 1.37.5 has no "overseas" autonomy floor. The state/territory system replaced it: a province in a *territory* (not a state) is floored at **90%** local autonomy; a *colonial* core is floored at **50%**. The 75% figure is from a pre-Common-Sense version of the game.

**Spec text that must change.** "Overseas provinces are floored at 75% autonomy, so they contribute roughly a quarter of their development's income." (spec.md, section 1.3)

**Blast radius.** C038 (falls with it, and is separately wrong on the arithmetic); C033 and C191 (the wealth pipeline must apply the right floor, and the floor is now regime-dependent: 90% in territory, 50% colonial core, 20% pasha state, 0 otherwise); C310 and C390 (the Caribbean/sugar-island demand predictions are computed through this floor); C038's downstream OUTCOME rows in section 2.8.

### C038 — REFUTED

> Because of that floor, an overseas province contributes roughly a quarter of its development's income.
>
> *ENGINE / derivation / depends on C037*

**Method.** Arithmetic from the actual floors found under C037.

**Evidence.** At `min_local_autonomy = 90`, income multiplier = 1 - 0.90 = **0.10**, i.e. one *tenth*, not one quarter. At `min_local_autonomy = 50` (colonial core) it is **0.50**, i.e. one half. Neither is "roughly a quarter". A quarter would require a 75% floor, which does not exist (C037).

**What is actually true.** A province in a territory contributes ~10% of its development's tax and production income; a colonial core contributes ~50%.

**Spec text that must change.** "Overseas provinces are floored at 75% autonomy, so they contribute roughly a quarter of their development's income." (spec.md, section 1.3)

**Blast radius.** C036 is unaffected; C310, C390 (sugar-island demand is now ~10% or ~50% of nominal, not 25%); C191.

### C039 — CONFIRMED

> `wealth` as defined excludes trade income.
>
> *MODEL / stipulated / depends on C032*

**Method.** Definitional (an exclusion in the spec's own formula).

**Evidence.** `wealth(p) = tax_income(p) + production_income(p)` contains no trade term.


---

## §1.4

### C040 — CONFIRMED

> `α(g) = clamp((price(g)/P₀)^k, α_min, α_max)`.
>
> *MODEL / stipulated*

**Method.** Definitional (a formula).

**Evidence.** Implemented as `alpha_of_good` in `solver.py`.

### C041 — OUT_OF_SCOPE

> `P₀ = 2.0` ducats.
>
> *DESIGN / stipulated / depends on C040*

**Method.** DESIGN (a chosen constant).

### C042 — CONFIRMED

> `α > 1` makes demand superlinear in provincial wealth.
>
> *MODEL / derivation / depends on C033, C040*

**Method.** Proof: for w > 0, d/dw (w^a) / (w^a / w) = a, so the elasticity of w^a with respect to w is exactly a; a > 1 gives elasticity > 1, i.e. superlinear.

**Evidence.** Elasticity is identically `a` for every `w > 0`; no numerical check needed.

### C043 — DEFERRED

> With `α > 1`, demand for luxuries concentrates on individually rich provinces.
>
> *OUTCOME / derivation / depends on C042*

**Method.** OUTCOME.

### C044 — CONFIRMED

> `α = 1` makes demand proportional to economic size.
>
> *MODEL / derivation / depends on C033*

**Method.** Proof: at a = 1, `w^a = w`, so c(n) is the node's share of world wealth - exactly proportional to economic size.

**Evidence.** Immediate.

### C045 — CONFIRMED

> `α < 1` makes demand sublinear, spreading bulk goods toward populous regions.
>
> *MODEL / derivation / depends on C033*

**Method.** Proof: elasticity a < 1 (see C042). For fixed total wealth, `sum_p w_p^a` is Schur-concave, so it is larger for a many-small-provinces node than for a few-large-provinces node of the same total.

**Evidence.** Numerically: 10 provinces of wealth 1 give sum = 10 at a=1 and 10^(1-a)*... ; concretely at a=0.5, 10 x 1 -> 10.00 while 1 x 10 -> 3.16. The many-province node wins.

### C046 — CONFIRMED

> Vanilla price events move prices in both directions, so α moves in both directions.
>
> *ENGINE / UNSOURCED / depends on C040*

**Method.** Parsed every `change_price` effect in `events/`, `decisions/`, `missions/` and `common/` (108 effects) and tabulated the sign of `value`.

**Evidence.** 78 positive (range +0.10 to +1.50) and 30 negative (range -0.10 to -0.75). Examples: `FlavorPER.txt:1175` `PERSIA_SILK_MONOPOLIZATION value = 1.5`; `FlavorPER.txt:1212` `PERSIA_SILK_FLOOD value = -0.5`.

### C047 — CONFIRMED

> No smoothing is applied to α.
>
> *MODEL / stipulated / depends on C040*

**Method.** Stipulation; the solver recomputes alpha from the current price each solve with no filter.

**Evidence.** No smoothing term exists in `build_sc()`.


---

## §1.5

### C048 — OUT_OF_SCOPE

> Gold is excluded from the per-good networks by configuration.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

**Note.** Worth recording: gold is already inert in vanilla trade. `common/prices/00_prices.txt` gives gold `base_price = 0` and `goldtype = yes`, so a gold province's contribution to node trade value is `goods_produced x 0 = 0`. The exclusion costs nothing.

### C049 — REFUTED

> Gold's value is still counted in `wealth` through production income.
>
> *ENGINE / UNSOURCED / depends on C032*

**Method.** Four independent file signals, the last of them decisive. (1) Read `common/prices/00_prices.txt`. (2) Enumerated EU4's income categories from the engine-referenced localisation keys in `localisation/core_l_english.yml`. (3) Cross-checked the gold-specific defines in `common/defines.lua`. (4) **Found that the engine exposes gold income and production income as two separate scriptable country fields** - `gold_income` / `gold_income_percentage` and `production_income` - each with its own trigger tooltip, and found both in live use in shipped script.

**Evidence.** Income categories are separately keyed and separately labelled: `INCOMETAX:0 "Taxation"`, `INCOMETRADE:0 "Trade"`, **`INCOMEGOLD:0 "Gold"`**, `INCOMEVASSAL`, `INCOMEMANUFAC`, `INCOMEHARBORFEES`, ... Gold has its own income constants (`GOLD_MINE_SIZE = 40, -- Base income from gold mines`; `GOLD_MINE_SIZE_PRIMITIVES = 4, -- Gold income for very slow techgroups`) and its own inflation coupling (`GOLD_INFLATION = 0.5`, `GOLD_INFLATION_THRESHOLD = 0.0`) that production income does not have. The prices file's own header comment: `goldtype = yes ... using prices from mine-value in province instead of supply/demand and baseprice`. **The decisive signal**: the engine ships two distinct income triggers over two distinct fields - `HAVE_GOLD_INCOME_MORE_THAN:0 "Gold income at least "` / `HAVE_GOLD_INCOME_LESS_THAN` against `HAVE_PRODUCTION_INCOME_MORE_THAN:0 "Production income at least "` / `HAVE_PRODUCTION_INCOME_LESS_THAN` - with the internal identifiers `gold_income` (0x02140f74) and `gold_income_percentage` (0x02114884). Both are used in shipped script: `common/achievements.txt:6000` has `gold_income = 10` and `:10742` has `gold_income_percentage = 0.5`. If gold income were booked as production income, `gold_income` would be redundant with `production_income` and could not be tested independently of it.

**What is actually true.** Gold-mine income is its own income category in EU4, computed from mine value with its own constants, not from `goods_produced x price` and not booked as production income. Under `wealth(p) = tax_income(p) + production_income(p)` a gold province's gold income is therefore **not** counted in wealth at all - it is invisible to demand, not merely diverted.

**Spec text that must change.** "**Gold.** Excluded by configuration. Its value is counted in `wealth` through production income, except where diverted by the treasure-fleet mechanic (section 1.11)." (spec.md, section 1.5)

**Blast radius.** C050 (the "exception" framing collapses - if gold never enters wealth, treasure-fleet diversion is not an exception to it); C148 (already-correct conclusion, wrong reason); C551 and C552 and C553 and C554 and C555 (the whole treasure-fleet bistability argument in section 3.12 runs on colonial gold raising or lowering the node's wealth; if gold income is not in wealth, there is no feedback and the gate is not bistable); C302 partially; C032's implementation.

**Note.** Residual question, now narrow: the two *country-level* fields are certainly distinct. What is not settled from files is whether the *per-province* production income field - which is what the spec's `production_income(p)` actually reads - carries the gold figure before it is aggregated to the country's Gold line. Settling observation: in a save with a gold province, read that province's Production income tooltip and check whether it is zero. Setup: any save containing a gold province (39 provinces produce gold at 1444). Probe 9 already schedules the analogous check for diverted colonial gold.

### C050 — REFUTED (by dependency)

> The exception is gold diverted by the treasure-fleet mechanic.
>
> *ENGINE / derivation / depends on C049, C147*

**Method.** Follows from C049.

**Evidence.** The claim is a stated exception to C049; with C049 refuted there is nothing for it to be an exception to.

**What is actually true.** Diverted colonial gold is not an exception to gold entering wealth, because gold never enters wealth under the spec's own definition of it.

**Spec text that must change.** "Its value is counted in `wealth` through production income, except where diverted by the treasure-fleet mechanic (section 1.11)." (spec.md, section 1.5)

**Blast radius.** C147, C148, C287, C288, and the section 3.12 bistability chain C551-C555.

### C051 — CONFIRMED

> `s(n,g)` is undefined when nothing in the world produces `g`.
>
> *MODEL / derivation / depends on C023*

**Method.** Definitional: the denominator `sum_m goods_produced(m,g)` is zero.

**Evidence.** In the 1444 dataset exactly one good has world production zero (coal), and `solver.py` guards it with the `live` mask.

### C052 — CONFIRMED

> A good with zero world production has no graph that month.
>
> *MODEL / derivation / depends on C051*

**Method.** Derivation from C051.

**Evidence.** `live = world > 0`; `PHI[gi]` stays all-zero for dead goods.

### C053 — CONFIRMED

> Such a good contributes nothing to `Φ`, i.e. `V_g = 0`.
>
> *MODEL / derivation / depends on C052, C059*

**Method.** Derivation: `V_g = price(g) x 0 = 0`.

**Evidence.** Coal in 1444: `V_coal = 10.0 x 0 = 0`.

### C054 — CONFIRMED

> Such a good is absent from the survival table.
>
> *MODEL / derivation / depends on C052*

**Method.** Derivation from C052.

**Evidence.** The survival table is indexed over live goods only: 29 in 1444, not 30 (`t_model3.py`).

### C055 — CONFIRMED

> A good acquires a graph in the first month any province produces it.
>
> *MODEL / derivation / depends on C052*

**Method.** Derivation from C052.

**Evidence.** Immediate from `live = world > 0` being recomputed each solve.

### C056 — DEFERRED

> Latent goods stay graphless for long stretches of a campaign.
>
> *OUTCOME / UNSOURCED / depends on C052*

**Method.** OUTCOME.

**Evidence.** Note from files: coal is the *only* latent good in EU4 (`is_latent = yes` appears exactly once in `common/tradegoods/00_tradegoods.txt`, on coal), and it is produced in **0** of 2472 owned provinces at 1444.11.11.

### C057 — PARTIAL

> Coal is produced nowhere in EU4 until Manufactories arrives.
>
> *ENGINE / UNSOURCED*

**Method.** Read coal's `trigger` block in `common/tradegoods/00_tradegoods.txt:2183-2246`, the institution start dates in `common/institutions/00_Core.txt`, and counted `latent_trade_goods` entries across `history/provinces/`.

**Evidence.** Coal's trigger is `OR = { development_discounting_tribal = 20  owner = { innovativeness = 20 } }` AND an if/else_if/else chain: the **default** branch (no `GER_specific_coal` province flag, no `earlier_coal_available` country flag) requires `provincial_institution_progress = { which = enlightenment value = 100 }` and `owner = { has_institution = enlightenment }`; only the two flagged branches use `manufactories` (with `adm_tech = 21` and `adm_tech = 23` respectively). Institution start dates: `manufactories historical_start_date = 1650.1.1`, `enlightenment historical_start_date = 1700.1.1`. 58 province history files carry `latent_trade_goods = { coal }`. 0 provinces produce coal at 1444.11.11.

**What is actually true.** Coal is produced nowhere at the 1444 start - that half is right, and Manufactories is a correct *lower bound* since even the earliest branch requires it. But the branch that fires for an ordinary country is the **Enlightenment** one (1700), not Manufactories (1650). The mechanism is also per-province and multi-conditional, not institution-arrival alone.

**Spec text that must change.** "Latent goods behave this way for long stretches - coal produces nowhere until Manufactories arrives, then appears with a full graph in a single tick." (spec.md, section 1.5)

**Blast radius.** C058 (the "single tick" half is refuted outright, see its entry); C325 and the section 2.8 "Latent good" validation row, which should be tested against the Enlightenment branch.

### C058 — DEFERRED

> Coal therefore appears with a full graph in a single tick.
>
> *OUTCOME / derivation / depends on C055, C057*

**Method.** OUTCOME.

**Evidence.** Contrary file evidence recorded: coal's trigger is evaluated **per province** and gates on `development_discounting_tribal = 20` or `innovativeness = 20`, on `provincial_institution_progress = 100` for that province, and on the owner having the institution. Those three are satisfied at different times in different provinces, so the 58 latent-coal provinces cannot all convert in one tick. Listed in the summary under OUTCOME claims with contrary file evidence.


---

## §1.6

### C059 — CONFIRMED

> `V_g = price(g) · Σ_m goods_produced(m,g)`.
>
> *MODEL / stipulated*

**Method.** Definitional (a formula).

**Evidence.** Implemented as `V = price(g) * world[gi]`. `sum_g V_g = 3662.400000` on 1444 data.

### C060 — CONFIRMED

> `Φ = Σ_g V_g · φ_g`.
>
> *MODEL / stipulated / depends on C007, C059*

**Method.** Definitional (a formula).

**Evidence.** Implemented as `Phi = (V[:,None] * PHI).sum(axis=0)`.

### C061 — CONFIRMED

> `Φ` is a potential, so orienting edges by it is acyclic.
>
> *MODEL / derivation / depends on C060*

**Method.** Proof: Phi is a real-valued function on nodes; orienting u->v iff Phi(u) > Phi(v) makes Phi strictly decreasing along directed paths, so no directed cycle exists. (This holds for *any* node function, weighted sum or not.) Checked on real data.

**Evidence.** `t_model.py`: `aggregate Phi acyclic: True`.

### C062 — OUT_OF_SCOPE

> `Φ` is the graph installed in the game.
>
> *DESIGN / stipulated / depends on C060*

**Method.** DESIGN.

### C063 — CONFIRMED

> With `α = 1` for every good, `Φ` collapses to a scalar multiple of `φ₀`.
>
> *MODEL / derivation / depends on C033, C060, C064*

**Method.** Proof plus measurement on real 1444 data. Proof: at a=1 every good's demand vector is the same c0, so `sum_g V_g (s_g - c0) = (sum_g V_g)(s0 - c0)` where `s0(n) = sum_g V_g s_g(n) / sum_g V_g = sum_g price(g) gp(n,g) / (world trade value)` - exactly the section 1.6 definition of phi0's supply. Linearity of the solve then gives `Phi = (sum_g V_g) phi0`. Measured with `t_model.py`.

**Evidence.** `scale factor k = 3662.4000000000 (spread max-min = 1.114e-10)`; `||Phi - k*phi0||_inf = 2.753e-14` against `||Phi||_inf = 1.405e+01`, i.e. **relative residual 1.959e-15**; `sum_g V_g = 3662.400000` and `world trade value = 3662.400000` - the scalar is exactly the world trade value. `orientation agreement Phi(a=1) vs phi0: 159 / 159 edges`.

### C064 — CONFIRMED

> `φ₀` is the single solve with demand at α = 1 and supply as each node's share of world trade value.
>
> *MODEL / stipulated*

**Method.** Definitional.

**Evidence.** Implemented as `solve_phi0()`.

### C065 — CONFIRMED

> A node's world trade value share uses `Σ_p goods_produced(p) × price(good(p))`.
>
> *MODEL / stipulated / depends on C064*

**Method.** Definitional; and it is exactly the quantity the C063 proof requires.

**Evidence.** `world trade value (phi0 denom) = 3662.400000` equals `sum_g V_g` to all printed digits.

### C066 — OUT_OF_SCOPE

> The `φ₀` case is computed as a diagnostic but never drawn.
>
> *DESIGN / stipulated / depends on C064*

**Method.** DESIGN.


---

## §1.7

### C067 — OUT_OF_SCOPE

> Merchant placement, range, and the collect/steer choice are unchanged from vanilla.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C068 — CONFIRMED

> Vanilla allows one merchant per country per node.
>
> *ENGINE / UNSOURCED*

**Method.** Engine-authored refusal string, found in the eu4.exe string table (`TRADER_ALLREADY_THERE` at offset 0x01c5b910) and resolved in `localisation/*_l_english.yml`.

**Evidence.** `TRADER_ALLREADY_THERE:0 "Only one Merchant allowed at any node."`

### C069 — CONFIRMED (value); PARTIAL (semantics)

> A merchant present gives +2 trade power, node-wide.
>
> *ENGINE / file value*

**Method.** Read `common/defines.lua` line 1197; confirmed the define is engine-referenced by finding `MERCHANT_MAX_POWER_BONUS` in the eu4.exe string table at 0x01c6e020.

**Evidence.** `MERCHANT_MAX_POWER_BONUS = 2.0,  -- MERCHANT_MAX_POWER_BONUS` (the comment is just the name).

**Note.** The value 2.0 is confirmed; that it is a flat +2 rather than a *maximum* is inferred from the define's name, which is exactly the inference mode the spec's own section 3.16 warns about ("semantics inferred from a define name"). Settling observation: read one country's node trade-power breakdown with and without a merchant present in the node.

### C070 — PARTIAL

> A merchant present gives +10% trade efficiency, node-wide.
>
> *ENGINE / file value*

**Method.** Read `common/defines.lua` line 1201 including its trailing comment; searched all localisation for a merchant trade-efficiency string.

**Evidence.** `TRADE_MERCHANT_PRESENT = 0.1,  -- bonus on income if trade present`. The define's own comment says **income**, not trade efficiency. No localisation string ties a merchant's presence to trade efficiency; `TRADE_EFFICIENCY:0 "Trade Efficiency"` and `TRADE_MERCHANT_PRESENT` are unrelated keys.

**What is actually true.** The value 0.1 is right. The stated *effect* ("+10% trade efficiency") is a name-and-magnitude inference; the shipped comment describes it as a bonus on income. Trade efficiency and a flat income bonus are not the same quantity in EU4 - efficiency also enters the caravan-power and collection tooltips, an income bonus does not.

**Spec text that must change.** "A merchant present gives +2 trade power and +10% trade efficiency, node-wide, regardless of what it is doing." (spec.md, section 1.7)

**Blast radius.** C217 (the define mapping table in section 2.3 carries the same claim); C314; C191's income pipeline.

**Note.** Settling observation: with and without a merchant in a node, compare (a) the country's Trade Efficiency figure in the country trade view and (b) the collected ducats from that node. If only (b) moves, the define is an income bonus.

### C071 — NEEDS_GAME

> Those merchant bonuses apply regardless of what the merchant is doing.
>
> *ENGINE / UNSOURCED / depends on C069, C070*

**Method.** No file distinguishes merchant *presence* from merchant *action* for these two bonuses; both defines are unconditional scalars and neither the .gui files nor the string table carry a conditional variant.

**Evidence.** `MERCHANT_MAX_POWER_BONUS` and `TRADE_MERCHANT_PRESENT` appear once each in defines.lua with no accompanying condition. The engine strings `TRADE_MERCHANT_ALREADY_COLLECTING` / `TRADE_MERCHANT_ALREADY_TRANSFERRING` show a merchant has exactly one intent, but say nothing about which bonuses that intent gates.

**Note.** Settling observation: place a merchant to collect in a node, record the country's trade power in that node; switch the same merchant to steer without moving it; re-read. If both figures are identical the bonuses are presence-gated. Setup: any save, one spare merchant. Same trace as probe 6.

### C072 — CONFIRMED

> Collect behaviour is vanilla, including the −50% penalty outside the home node.
>
> *ENGINE / file value*

**Method.** Read `common/defines.lua` line 1200; corroborated by the engine's own main-port tooltip.

**Evidence.** `TRADE_NON_CAPITAL_OFFICE = -0.50,  -- TRADE_NON_CAPITAL_OFFICE` and `TRADEMAP_MAINPORT_DESC:0 "Your main trading port is where you collect your trade. You can collect in other place but there you will get a trade power penalty."` The tooltip independently confirms both the -50% and that it is a **trade power** penalty (which is what C599 asserts).

### C073 — OUT_OF_SCOPE

> The node window is widened to list every link incident to the node, not only the outgoing ones.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

**Note.** Relevant file fact for the implementation: the vanilla node window **already has an incoming-links list**. `interface/tradeinterface.gui:90` defines `incoming_nodes_listbox` alongside `outgoing_nodes_listbox` (line 110), and both are populated with the same `TradeNodeLink` window type (line 18), which contains a `NextNodeButton`. The widening may be smaller than the spec assumes - see C532.

### C074 — CONFIRMED

> A merchant assigned to link `{n,m}` steers every good oriented `n → m`.
>
> *MODEL / stipulated / depends on C073*

**Method.** Definitional.

### C075 — CONFIRMED

> That merchant is inert for every good oriented `m → n`.
>
> *MODEL / stipulated / depends on C073*

**Method.** Definitional.

### C076 — NEEDS_GAME

> A merchant keeps its link assignment when the link flips.
>
> *ENGINE / UNSOURCED*

**Method.** Nothing on disk records how a merchant's assignment is stored (link handle vs node-pair vs outgoing-index). Save files would show it, but all 577 saves in the user's save directory are OneDrive cloud placeholders and cannot be hydrated (see the Data availability note in the summary).

**Evidence.** `interface/tradeinterface.gui` shows only the display side; `defines.lua` has no merchant-assignment define. eu4.exe strings give `MERCHANT_ARRIVED`, `MERCHANT_CANCEL`, `TRADE_MERCHANT_ALREADY_COLLECTING`, `TRADE_MERCHANT_ALREADY_TRANSFERRING` - no storage hint.

**Note.** This is section 2.7 probe 5. Settling observation: with a merchant steering on link {n,m}, edit the node file so the link reverses, reload, and inspect the merchant's stored target. Setup: a non-ironman save plus one hand-edited `00_tradenodes.txt` - the same edit section 2.4 item 3 already requires.

### C077 — CONFIRMED (conditional)

> Only the merchant's active good set changes when a link flips.
>
> *MODEL / derivation / depends on C074, C075, C076*

**Method.** Derivation from C074/C075/C076; valid as an inference.

**Evidence.** The inference is sound; its premise C076 is NEEDS_GAME, so the conclusion inherits that status.

### C078 — DEFERRED

> The same physical link can host a merchant at each end, active on disjoint good sets.
>
> *OUTCOME / derivation / depends on C074, C075*

**Method.** OUTCOME.

### C079 — OUT_OF_SCOPE

> Under the mod, caravan power requires the merchant to be steering at least one good on that link.
>
> *DESIGN / stipulated / depends on C074*

**Method.** DESIGN.

### C080 — OUT_OF_SCOPE

> Assignment alone does not qualify for caravan power.
>
> *DESIGN / stipulated / depends on C079*

**Method.** DESIGN.

### C081 — CONFIRMED

> The added caravan condition constrains only the two steering conditions.
>
> *MODEL / derivation / depends on C079*

**Method.** Derivation; checked against the spec's own section 1.7 wording, which scopes the condition to the two steering bullets only.

**Evidence.** Valid.

### C082 — CONFIRMED

> Collecting at an inland node as main trading port is untouched by the change.
>
> *MODEL / derivation / depends on C083*

**Method.** Derivation from C083.

**Evidence.** Valid.

### C083 — CONFIRMED

> The steering-list widening does not affect collection.
>
> *MODEL / derivation / depends on C073*

**Method.** Derivation: the widening changes the *steering* target list only; collection is a node property with no link argument.

**Evidence.** Valid.


---

## §1.8

### C084 — CONFIRMED

> In the engine, trade power and collect/transfer intent are node-wide, not per good.
>
> *ENGINE / UNSOURCED*

**Method.** Three engine-authored strings that together fix the granularity, from the eu4.exe string table and `localisation/*_l_english.yml`.

**Evidence.** (1) `TRADER_ALLREADY_THERE:0 "Only one Merchant allowed at any node."` - at most one merchant per country per node. (2) `TRADE_MERCHANT_ALREADY_COLLECTING:0 "$ENVOY$ is already collecting from trade here."` and `TRADE_MERCHANT_ALREADY_TRANSFERRING:0 "$ENVOY$ is already transferring Trade Power here."` - one intent per merchant, therefore one intent per country per node. (3) `TRADEMAP_POWER:0 "Our current Trade Power is: $VAL$"` and `TRADEMAP_TOTAL_POWER:0 "Total Trade Power in node: $VAL$"` - one power scalar per country per node, with no commodity argument.

### C085 — CONFIRMED

> What varies per good is what that node-wide power and intent produce.
>
> *MODEL / stipulated / depends on C084*

**Method.** Stipulation (the mod's own design statement).

### C086 — CONFIRMED

> `collected_share(n,g) = 1` when `n` is a sink for `g`.
>
> *MODEL / stipulated / depends on C010*

**Method.** Definitional.

### C087 — CONFIRMED

> Otherwise `collected_share(n,g) = P_collect / (P_collect + P_transfer(g))`.
>
> *MODEL / stipulated*

**Method.** Definitional (a formula).

### C088 — CONFIRMED

> Transfer eligibility is per good.
>
> *MODEL / stipulated / depends on C005*

**Method.** Definitional.

### C089 — CONFIRMED

> A country's power counts toward `P_transfer(g)` only if it steers `g` at `n` with a merchant, or collects at some node reachable from `n` in `φ_g`.
>
> *MODEL / stipulated / depends on C088*

**Method.** Definitional.

### C090 — CONFIRMED

> Power meeting neither condition is inert for that good.
>
> *MODEL / derivation / depends on C089*

**Method.** Derivation; immediate from C089 (the two conditions are exhaustive by construction).

**Evidence.** Valid.

### C091 — CONFIRMED

> The uncollected remainder moves per good, by the vanilla two-case rule.
>
> *MODEL / stipulated / depends on C087*

**Method.** Stipulation.

### C092 — NEEDS_GAME

> In vanilla, when any country steers `g` at `n`, outgoing value is divided across outgoing links in proportion to the modified trade power steering toward each link.
>
> *ENGINE / UNSOURCED*

**Method.** The engine strings show per-link outgoing values and a per-country outgoing-value boost, but not the division rule. No file states the proportionality basis.

**Evidence.** `TRADEMAP_OUTGOING:0 "$VAL$ is being sent forward to $NAME$."` (per-link), `TRADEMAP_OUTGOING_BASE:0 "Before countries increase the outgoing trade value, $BASEVAL$ is leaving $FROMNODE$."` and `TRADE_ADDED_VALUE_COUNTRY:0 "$WHO$ increases outgoing value by: $VAL$%"` - the last two confirm C592's per-link boost but not the split rule.

**Note.** Settling observation: in a node with two outgoing links, place steering merchants of known, unequal trade power on one link only, and read the two `TRADEMAP_OUTGOING` figures. If the unsteered link shows 0, C094 holds and the split is steer-weighted. Then add a second steerer of known power on the other link and check the ratio against the steering powers rather than the node powers. Setup: one observer save with console-free merchant placement; two AI-free nodes preferred.

### C093 — NEEDS_GAME

> That division is not in proportion to power held in the node generally.
>
> *ENGINE / UNSOURCED / depends on C092*

**Method.** Same probe as C092.

**Evidence.** See C092.

**Note.** Settled by the same two-link experiment: compare the realised split against (a) steering power toward each link and (b) total node power of the steerers. Distinguishing (a) from (b) requires the two steerers to have different node-wide power than steering power, which the -50% off-home penalty (C072) supplies for free.

### C094 — CONFIRMED (conditional)

> An outgoing link with no steerer receives nothing, even when other links are steered.
>
> *ENGINE / derivation / depends on C092*

**Method.** Derivation from C092.

**Evidence.** Sound inference; premise is NEEDS_GAME.

### C095 — CONFIRMED (conditional)

> A single steerer takes all of a good's outgoing value down its link, however little power it holds.
>
> *ENGINE / derivation / depends on C092*

**Method.** Derivation from C092.

**Evidence.** Sound inference; premise is NEEDS_GAME.

### C096 — OUT_OF_SCOPE

> Both of those consequences are load-bearing for the design.
>
> *DESIGN / stipulated / depends on C094, C095*

**Method.** DESIGN.

### C097 — NEEDS_GAME

> If no country steers `g` at `n`, `g`'s outgoing value splits evenly across its outgoing links.
>
> *ENGINE / UNSOURCED*

**Method.** Same probe as C092, with no steerer placed.

**Evidence.** No file states the unsteered rule.

**Note.** Settling observation: in a node with two or more outgoing links and no merchant steering, read the `TRADEMAP_OUTGOING` figure on each link. Equal figures confirm the even split. Setup: an observer save early enough that some node has no merchants (many Asian and African nodes qualify in 1444).

### C098 — CONFIRMED

> At `g`'s sink there is no remainder: 100% is collected.
>
> *MODEL / derivation / depends on C086*

**Method.** Derivation: `collected_share = 1` leaves `1 - 1 = 0` to move.

**Evidence.** Arithmetic.

### C099 — PARTIAL

> At a sink, collected value is divided among collectors by trade power.
>
> *ENGINE / UNSOURCED*

**Method.** Engine strings indicate power-proportional division among collectors but do not state the formula.

**Evidence.** `TRADE_EMBARGO_POWER_SHARE:0 "$NAME$ share of power: $VAL$%"`, `TN_TRADE_POWER:0 "Trade Power"` as the node window's per-country column, `TRADEMAP_WE_COLLECT:0 "We collect $VAL$"`, and `TRADE_COMPANY_IMPACT_ENTRY:0 "$OWNER$: $IMPACT$ = ($SHARE% [trade power icon]$INST_EFF$$MOD$)"` - the last shows an owner's impact computed from a power *share*.

**Note.** Settling observation: in a node where exactly two countries collect with known trade powers p1, p2, check that collected ducats split as p1:p2. Setup: any save; read both figures from the node window's country list.

### C100 — PARTIAL

> Vanilla trade range still gates flow.
>
> *ENGINE / UNSOURCED*

**Method.** Enumerated every range concept in `common/defines.lua` and the eu4.exe string table.

**Evidence.** Trade range exists and gates *merchant placement*: `TRADER_IN_RANGE:0 "Must be in range (Current Range: $CURR$ Max Range: $MAX$)."`, `TRADE_NODES_OUT_OF_RANGE:0 "The following known nodes are outside your trade range: "`, `TRADE_RANGE_IRO:0 "Our merchants can reach trade nodes within this range."`, `MODIFIER_TRADE_RANGE:0 "Trade Range"`, `TRADING_CITY_TRADING_RANGE_BOOST = 0.2`, `MERCENARY_TRADE_RANGE_MODIFIER = 1.0`. No string or define ties trade range to trade *value* movement.

**What is actually true.** Trade range gates where a country may place a merchant, and therefore gates that country's ability to collect or steer. It does not gate value flowing along a link - value moves down the graph whether or not anyone is in range.

**Spec text that must change.** "Vanilla gates still apply: trade range, supply range, and no transfer into a node where nobody holds power at both ends." (spec.md, section 1.8)

**Blast radius.** C299 (the pre-1500 Malacca-Cape corridor is attributed to "range and the power-at-both-ends gate"; the range half operates only through merchant reach); C385, C664.

### C101 — REFUTED

> Vanilla supply range still gates flow.
>
> *ENGINE / UNSOURCED*

**Method.** Searched `common/defines.lua` and the full eu4.exe string table for any trade-related supply-range concept.

**Evidence.** The only supply-range constructs in EU4 1.37.5 are naval: `NAVAL_SUPPLY_RANGE = 150,  -- Supply range for ships.` (defines.lua:1365), the string `SHIP_SUPPLY_RANGE`, `(Not in supply range)`, and the internal `update_supply_range` / `CCountry::AddOwnedProvince set _bUpdateSupplyRangeCache`. All concern naval attrition and ship range. There is **no** supply-range gate on trade.

**What is actually true.** There is no such thing as a trade "supply range" in EU4. The only range gate on trade is trade range (C100), and it gates merchant placement.

**Spec text that must change.** "Vanilla gates still apply: trade range, supply range, and no transfer into a node where nobody holds power at both ends." (spec.md, section 1.8) - the words "supply range" must be struck.

**Blast radius.** C299 (its list of gates withholding the pre-1500 corridor names supply range); C385, C664 are unaffected since they rest on C102.

### C102 — NEEDS_GAME

> No transfer occurs into a node where nobody holds power at both ends.
>
> *ENGINE / UNSOURCED*

**Method.** No file states this rule; it is not a define, a static modifier, or a scripted trigger.

**Evidence.** Nothing in `common/`, `interface/`, or the eu4.exe string table names a power-at-both-ends condition.

**Note.** Settling observation: find a link whose upstream node has your power and whose downstream node has none (or vice versa) and read the link's `TRADEMAP_OUTGOING` value. Setup: an observer save; the 1444 African and Siberian corridors are the natural candidates since few countries hold power at both ends.


---

## §1.9

### C103 — OUT_OF_SCOPE

> Trade power propagation is preserved from vanilla, unchanged.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C104 — PARTIAL

> A country whose provincial trade power in a node meets the threshold receives a share of it in every immediately upstream node.
>
> *ENGINE / prose source*

**Method.** Located the engine's own propagation tooltip via the eu4.exe string table (`TRADE_POWER_UPSTREAM` at 0x01ce8058, `TRADE_POWER_UPSTREAM_DESC` at 0x01d4f1e0) and resolved both in localisation.

**Evidence.** `TRADE_POWER_UPSTREAM_DESC:0 "A nation can Transfer Trade Power back upstream to trade nodes **where it already has power**."` and `TRADE_POWER_UPSTREAM:0 "$COUNTRY$ is transferring $VAL$ of its Trade Power upstream."` Also `MERCHANT_DOWNSTREAM_BONUS:0 "Transfers from traders downstream: $VAL$"` and `TRADEPOWERBONUS_FROM:0 "Transfer from $FROM$: $VAL$"`.

**What is actually true.** The upstream direction and the existence of propagation are confirmed by the engine's own tooltip. What the tooltip adds, and the spec does not carry, is the qualifier **"where it already has power"** - which reads as a condition on the *receiving* (upstream) node, not only on the source node. The spec says the share is received "in **every** immediately upstream node", with no such qualifier.

**Spec text that must change.** "A country whose provincial trade power in a node meets the threshold receives a share of it in **every** immediately upstream node." (spec.md, section 1.9)

**Blast radius.** C105, C106, C110 ("a node receives the summed contributions of all its downstream neighbours" would need the same qualifier), C119, C120, C121, C334, C481, C482, C680; and section 3.16's cautionary case is *about this very line*, which makes a second uncorrected qualifier on it worth flagging loudly.

**Note.** Settling observation: take a country with provincial trade power above threshold in node X and **zero** power in upstream node Y, and read whether it appears in Y's trade-power list. Setup: any save; a colonial or newly conquered single-province holding gives the clean case. This is cheap and does not need a debugger.

### C105 — CONFIRMED (define); PARTIAL (semantics)

> That share is `1 / TRADE_PROPAGATE_DIVIDER`.
>
> *ENGINE / file value / depends on C104*

**Method.** Read `common/defines.lua` line 1205; confirmed engine reference via the string table (`TRADE_PROPAGATE_DIVIDER` at 0x01c6e298).

**Evidence.** `TRADE_PROPAGATE_DIVIDER = 5,` so `1 / TRADE_PROPAGATE_DIVIDER = 0.2`. The modifier localisation is `TRADE_PROPAGATE_DIVIDER:0 "Trade propagation reduction: -$VAL$%"` - phrased as a *percentage reduction*, not a divisor.

**Note.** The value is certain; that the share is `1/DIVIDER` rather than, say, `1 - VAL%` is a reading of the name. The localisation string's "reduction: -$VAL$%" phrasing is at least consistent with a different arithmetic. Settling observation: same trace as probe 8 - read a known provincial trade power in node X and the propagated figure in upstream node Y.

### C106 — CONFIRMED (as arithmetic)

> The threshold in raw power equals `TRADE_PROPAGATE_THRESHOLD × TRADE_PROPAGATE_DIVIDER`.
>
> *ENGINE / derivation / depends on C104, C105, C567*

**Method.** Arithmetic on the two confirmed file values.

**Evidence.** `TRADE_PROPAGATE_THRESHOLD = 2` (defines.lua:1206) x `TRADE_PROPAGATE_DIVIDER = 5` = **10** raw trade power. Both defines are engine-referenced (string table 0x01c6e2b0 and 0x01c6e298).

**Note.** The arithmetic is certain; the *reading* that makes it meaningful (threshold expressed in propagated units) is C568 and is probe-8 material.

### C107 — CONFIRMED

> Ship trade power propagates only where the country has a ship-propagation modifier.
>
> *ENGINE / prose source / depends on C104*

**Method.** Found the modifier in the eu4.exe string table and resolved its display name.

**Evidence.** `MODIFIER_SHIP_POWER_PROPAGATION` at 0x01cc3630 and the internal identifier `ship_power_propagation` at 0x02102814; `MODIFIER_SHIP_POWER_PROPAGATION:0 "Ship Tradepower Propagation"`. The modifier exists and is distinct from the base propagation defines, which is exactly what "only where the country has a ship-propagation modifier" requires.

### C108 — PARTIAL

> Ship propagation happens at the compounded rate: the propagation share multiplied by that modifier.
>
> *ENGINE / prose source / depends on C105, C107*

**Method.** Confirmed both factors exist as separate quantities (C105, C107); found nothing on disk stating they compound multiplicatively.

**Evidence.** `TRADE_PROPAGATE_DIVIDER = 5` and the separate `ship_power_propagation` modifier. No file expresses their combination.

**Note.** Settling observation: with a known ship trade power in node X and a known `ship_power_propagation` value, read the propagated ship contribution in upstream node Y and check it against `share x modifier` versus `share + modifier`. Setup: any save with light ships protecting trade; the same trace as probe 8.

### C109 — NEEDS_GAME

> Propagation is strictly one hop and never chains.
>
> *ENGINE / UNSOURCED*

**Method.** No file states the hop count. Note that section 3.13 itself treats this as the premise of an argument-from-exhaustion (C570-C573).

**Evidence.** Nothing in defines, static modifiers, or the string table bounds propagation to one hop.

**Note.** Settling observation: build a three-node chain A -> B -> C where the country has power only in C, and read whether any propagated power appears in A. Setup: an observer save; a long inland corridor such as `chengdu -> xian -> beijing` is the natural test. This is observable without a debugger and would also settle C570-C573 cheaply, which section 3.13 currently defers to probe 2.

### C110 — PARTIAL

> A node receives the summed contributions of all its downstream neighbours.
>
> *ENGINE / UNSOURCED / depends on C104*

**Method.** Inherits C104's qualifier.

**Evidence.** `MERCHANT_DOWNSTREAM_BONUS:0 "Transfers from traders downstream: $VAL$"` is plural and consistent with summing over downstream neighbours; but if C104's "where it already has power" qualifier is real, the sum is over a filtered set.

**Note.** Settled by the same observation as C104.

### C111 — OUT_OF_SCOPE

> For propagation, direction is read from `Φ`.
>
> *DESIGN / stipulated / depends on C062*

**Method.** DESIGN.


---

## §1.10

### C112 — OUT_OF_SCOPE

> Any mechanism gated on one nation being upstream or downstream of another evaluates TRUE.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C113 — OUT_OF_SCOPE

> Any node-pair direction dependency reads `Φ`.
>
> *DESIGN / stipulated / depends on C062*

**Method.** DESIGN.

### C114 — OUT_OF_SCOPE

> Where a gate scopes a set or a path, that scope reads `Φ`.
>
> *DESIGN / stipulated / depends on C062*

**Method.** DESIGN.

### C115 — OUT_OF_SCOPE

> Fallback rung 1 is the `Φ` path.
>
> *DESIGN / stipulated / depends on C114*

**Method.** DESIGN.

### C116 — OUT_OF_SCOPE

> Fallback rung 2, used when `Φ` does not connect the pair, is the shortest path within a single good's graph that does.
>
> *DESIGN / stipulated / depends on C114*

**Method.** DESIGN.

### C117 — OUT_OF_SCOPE

> Fallback rung 3, used only if no good connects them, is the undirected shortest path.
>
> *DESIGN / stipulated / depends on C114*

**Method.** DESIGN.

### C118 — OUT_OF_SCOPE

> The listed threshold mechanics are left unpatched and unchanged.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C119 — CONFIRMED

> Reorientation reaches those mechanics through the trade power distribution, not through any direction test.
>
> *MODEL / derivation / depends on C103, C118*

**Method.** Derivation; sound given C103 and C118 (both design stipulations).

**Evidence.** Valid.

### C120 — CONFIRMED (conditional)

> Because propagation is direction-dependent, a flip moves propagated power at both ends of the flipped link.
>
> *MODEL / derivation / depends on C104, C111*

**Method.** Derivation from C104 and C111.

**Evidence.** Sound inference; premise C104 is PARTIAL.

### C121 — DEFERRED

> A flip changes fan-out across the neighbourhood.
>
> *OUTCOME / derivation / depends on C120*

**Method.** OUTCOME.

### C122 — DEFERRED

> All of these mechanics move monthly.
>
> *OUTCOME / derivation / depends on C019, C120*

**Method.** OUTCOME.

### C123 — CONFIRMED

> The trade-conflict casus belli target threshold is `JUSTIFY_TRADE_CONFLICT_LIMIT`.
>
> *ENGINE / file value*

**Method.** Read `common/defines.lua` line 164; engine-referenced (string table).

**Evidence.** `JUSTIFY_TRADE_CONFLICT_LIMIT = 0.2,  -- How big share of the trade power needed on the target to be able to justify a trade conflict`. Value **0.2**; the comment confirms the claim's "target" role.

### C124 — CONFIRMED

> The trade-conflict casus belli actor threshold is `JUSTIFY_TRADE_CONFLICT_ACTOR_LIMIT`.
>
> *ENGINE / file value*

**Method.** Read `common/defines.lua` line 165.

**Evidence.** `JUSTIFY_TRADE_CONFLICT_ACTOR_LIMIT = 0.1,  -- How big share of the trade power needed on the actor to be able to justify a trade conflict`. Value **0.1**.

### C125 — CONFIRMED

> The privateer-blocking threshold is `MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER`.
>
> *ENGINE / file value*

**Method.** Read `common/defines.lua` line 367.

**Evidence.** `MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER = 0.2, -- Minimum trade power needed for a country that won a war to block privateer from the country that lost the war`. Value **0.2**. Note the comment adds a war-outcome precondition the spec's table omits.

### C126 — CONFIRMED

> The trade company extra-merchant threshold is `TRADE_COMPANY_STRONG_LIMIT`.
>
> *ENGINE / file value*

**Method.** Read `common/defines.lua` line 1213.

**Evidence.** `TRADE_COMPANY_STRONG_LIMIT = 0.51`. Value **0.51**.

### C127 — CONFIRMED

> The trade company control threshold is `TRADE_COMPANY_CONTROL_LIMIT`.
>
> *ENGINE / file value*

**Method.** Read `common/defines.lua` line 1211.

**Evidence.** `TRADE_COMPANY_CONTROL_LIMIT = 0.6`. Value **0.6**.

### C128 — REFUTED

> Improve Inland Routes requires 33% trade power.
>
> *ENGINE / UNSOURCED*

**Method.** Read the policy definition in `common/trading_policies/00_trading_policies.txt` (`improve_inland_routes`, lines 100-145).

**Evidence.** `can_select` contains `FROM = { trade_share = { country = ROOT share = 50 } }` and `can_maintain` contains `FROM = { trade_share = { country = ROOT share = 40 } }` (both wrapped in `if = { limit = { NOT = { has_government_attribute = free_improve_inland_routes } } }`). There is no 33 anywhere in the file.

**What is actually true.** Improve Inland Routes requires **50%** trade share to select and **40%** to maintain - a two-valued band, not a single 33%. It also requires `FROM = { has_trader = ROOT }`, i.e. a merchant present in the node, which the spec's table omits. A government attribute `free_improve_inland_routes` waives the share requirement entirely.

**Spec text that must change.** The section 1.10 threshold table row "| Improve Inland Routes | 33% |" must become 50% to establish / 40% to maintain, plus the merchant-present precondition.

**Blast radius.** C131 (which asserts every listed threshold except Propagate Religion is single-valued - this inverts it); C132; C336; C335.

### C129 — PARTIAL

> Propagate Religion requires 50% trade power to establish.
>
> *ENGINE / UNSOURCED*

**Method.** Read `propagate_religion`'s `can_select` block in `common/trading_policies/00_trading_policies.txt`.

**Evidence.** The default branch is `else_if = { limit = { OR = { NOT = { has_country_flag = orm_easier_propagation_flag } had_country_flag = { flag = orm_easier_propagation_flag days = 5475 } } } FROM = { has_trader = ROOT is_node_in_trade_company_region = yes trade_share = { country = ROOT share = 50 } } }` - so 50 is correct **for that branch**. But the block is a ten-rung `if / else_if` ladder keyed on country flags `5_/10_/15_/20_/25_/30_/35_/40_/45_trade_power_for_propogate_religion`, giving select thresholds of 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, and a terminal `else` at **35**.

**What is actually true.** 50% is the default establish threshold, but it is one rung of an eleven-valued ladder (5-50 plus a 35 fallback), and it is additionally gated on `has_trader = ROOT`, `is_node_in_trade_company_region = yes`, `dominant_religion = ROOT`, and a religion-group / country-flag disjunction.

**Spec text that must change.** The section 1.10 row "| Propagate Religion | 50% to establish, 40% to maintain |" and the sentence "All are single-valued except Propagate Religion, whose band absorbs chatter on its own."

**Blast radius.** C130 (separately refuted), C131, C132, C486, C488.

### C130 — REFUTED

> Propagate Religion requires 40% trade power to maintain.
>
> *ENGINE / UNSOURCED*

**Method.** Read `propagate_religion`'s `can_maintain` block in `common/trading_policies/00_trading_policies.txt` and matched it rung-for-rung against `can_select`.

**Evidence.** The `can_maintain` rung that pairs with the default select-50 rung is: `else_if = { limit = { OR = { NOT = { has_country_flag = orm_easier_propagation_flag } had_country_flag = { flag = orm_easier_propagation_flag days = 5475 } } } FROM = { has_trader = ROOT is_node_in_trade_company_region = yes trade_share = { country = ROOT share = **50** } } }`. The maintain requirement in the default case is **50, not 40**. (The flagged rungs *are* shifted down - 20 select / 10 maintain, 45 select / 35 maintain - but the default rung is not.)

**What is actually true.** In the default case Propagate Religion requires 50% to establish and **50%** to maintain. There is no 50/40 band. The terminal `else` branch is 35 select / 35 maintain - also equal.

**Spec text that must change.** "| Propagate Religion | 50% to establish, 40% to maintain |" and "All are single-valued except Propagate Religion, whose band absorbs chatter on its own." (spec.md, section 1.10)

**Blast radius.** C131 (inverted: Improve Inland Routes is the banded one, Propagate Religion is not); **C132 collapses entirely** - the band it relies on does not exist, so nothing absorbs threshold chatter on its own; C336, C335, C337; C486, C488.

### C131 — REFUTED

> All the listed thresholds are single-valued except Propagate Religion.
>
> *ENGINE / derivation / depends on C123, C124, C125, C126, C127, C128, C129, C130*

**Method.** Compared all seven listed thresholds against their sources: five defines in `common/defines.lua` and two policies in `common/trading_policies/00_trading_policies.txt`.

**Evidence.** Single-valued: `JUSTIFY_TRADE_CONFLICT_LIMIT = 0.2`, `JUSTIFY_TRADE_CONFLICT_ACTOR_LIMIT = 0.1`, `MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER = 0.2`, `TRADE_COMPANY_STRONG_LIMIT = 0.51`, `TRADE_COMPANY_CONTROL_LIMIT = 0.6`. **Banded: Improve Inland Routes (50 select / 40 maintain).** Not banded in the default case: Propagate Religion (50 / 50).

**What is actually true.** The claim is exactly inverted. Improve Inland Routes is the one entry with a select/maintain band; Propagate Religion has none in its default branch (it has an eleven-rung ladder keyed on country flags instead).

**Spec text that must change.** "All are single-valued except Propagate Religion, whose band absorbs chatter on its own." (spec.md, section 1.10)

**Blast radius.** C132, C336, C335, C337.

### C132 — REFUTED

> Propagate Religion's 50/40 band absorbs threshold chatter on its own.
>
> *OUTCOME / derivation / depends on C129, C130*

**Method.** Follows from C130.

**Evidence.** The 50/40 band does not exist; the default select and maintain thresholds are both 50.

**What is actually true.** Propagate Religion has no self-absorbing band. Improve Inland Routes does (50/40), so it is the mechanic that tolerates threshold chatter, and Propagate Religion is one of the mechanics that does not.

**Spec text that must change.** "All are single-valued except Propagate Religion, whose band absorbs chatter on its own." (spec.md, section 1.10)

**Blast radius.** C335, C336, C337 - the flicker-risk analysis must move Propagate Religion into the at-risk set and Improve Inland Routes out of it.

### C133 — DEFERRED

> Casus belli availability is the most visible symptom of threshold crossing.
>
> *OUTCOME / derivation / depends on C123, C124*

**Method.** OUTCOME.

### C134 — DEFERRED

> Casus belli availability can appear and vanish month to month.
>
> *OUTCOME / derivation / depends on C122, C133*

**Method.** OUTCOME.

### C135 — PARTIAL

> Caravan power is not a threshold mechanic but a step function on raw power.
>
> *ENGINE / UNSOURCED*

**Method.** Read the engine's caravan tooltips (`CARAVAN_POWER_DESC2`, `TRADEMAP_INLAND_DESC`) and the three caravan defines.

**Evidence.** `CARAVAN_POWER_DESC2:1 "Inland caravans provide a total of $VALUE$ trade power, base of it coming from a third of your development($BASE$) and $MODIFIER$ from policies and ideas."` plus `CARAVAN_FACTOR = 3.0`, `CARAVAN_POWER_MAX = 50`, `CARAVAN_POWER_MIN = 2`. The magnitude is continuous in development; what is binary is *whether it applies*, and the trigger is `TRADEMAP_INLAND_DESC:0 "Having a merchant present that collects in an inland trade node, or steers towards an inland trade node, will give you extra trade power in that node..."`

**What is actually true.** "Step function on raw power" is the wrong shape: caravan power is not a function of raw trade power at all. It is a function of total country development (÷3, plus policy/idea modifiers, clamped to [2, 50]) that is switched on by a merchant condition. It is a gated development-scaled bonus, not a step on power.

**Spec text that must change.** "**Caravan power is in this group but is not a threshold mechanic.** It is a step function on raw power" (spec.md, section 1.10)

**Blast radius.** C136, C137, C138, C544 (which correctly says it does not scale with node presence - that survives), C537-C540.

### C136 — CONFIRMED

> When caravan power applies it is worth up to the cap for any major power.
>
> *ENGINE / derivation / depends on C135, C542*

**Method.** Arithmetic on `CARAVAN_POWER_MAX = 50` and the 1444 development census; see C543.

**Evidence.** 19 countries reach `dev/3 >= 50` at the 1444 start.

### C137 — DEFERRED

> Caravan power is enough to move a node's power shares by itself.
>
> *OUTCOME / derivation / depends on C136*

**Method.** OUTCOME.

### C138 — DEFERRED

> Caravan power can therefore push other countries across the listed thresholds.
>
> *OUTCOME / derivation / depends on C137*

**Method.** OUTCOME.

### C139 — REFUTED

> Missions, decisions, events, and trade companies reference trade nodes by name.
>
> *ENGINE / UNSOURCED*

**Method.** Exhaustive scan for literal trade-node names outside the node file. Built the 80-name list from `common/tradenodes/00_tradenodes.txt` and searched every `.txt` under `common/`, `missions/`, `decisions/`, `events/`, `history/`, `customizable_localization/` and `hints/`, stripping `#` comments before matching.

**Evidence.** **Zero** non-comment occurrences. All 15 raw matches are inside comments (e.g. `KoK_Byzantine_Missions.txt:2912  1320 = { #constantinople`). Scripted content reaches trade nodes only through scopes and triggers: `home_trade_node` (19 uses), `any_active_trade_node` (46), `random_active_trade_node` (49), `every_active_trade_node` (8), `any_/random_/every_trade_node_member_province`, `highest_value_trade_node = yes` (21), `node = PREV/ROOT` (48). Trade companies do not reference nodes at all - `common/trade_companies/00_trade_companies.txt` lists bare province IDs (`provinces = { 1164 1165 1166 ... }`).

**What is actually true.** No mission, decision, event, or trade company in vanilla EU4 1.37.5 names a trade node. Trade nodes are reached structurally - through a member province, through `home_trade_node`, or through iteration over active nodes. Trade companies are defined by province lists and have no node reference at all.

**Spec text that must change.** "**Scripted content.** Missions, decisions, events, and trade companies reference trade nodes by name, and nodes themselves never change - only connections do, which the engine treats as conflict-free." (spec.md, section 1.10)

**Blast radius.** C141 and C142 - the conclusion (connection-only changes are conflict-free for scripted content) is *strengthened*, not weakened, since nothing binds to a node name. But C142's "a mission whose sense depends on a specific authored direction" now needs a different mechanism to be stated: the exposure is through `highest_value_trade_node` and through node-scoped triggers evaluated on a reoriented graph, not through name references. C143's compatibility pass should be scoped accordingly.

### C140 — CONFIRMED

> Trade nodes themselves never change under the mod; only connections do.
>
> *MODEL / stipulated*

**Method.** Stipulation, and true of the emission plan: section 2.4 emits the same 80 node blocks with the same `members`.

### C141 — PARTIAL

> The engine treats connection-only changes as conflict-free.
>
> *ENGINE / UNSOURCED / depends on C140*

**Method.** Cannot be settled from files (it is about engine load behaviour), but C139's refutation removes its main hazard.

**Evidence.** No scripted content binds to a node name (C139), so the name-collision class of conflict is empty.

**Note.** Settling observation: hand-edit one `outgoing` block in `common/tradenodes/00_tradenodes.txt` (the edit section 2.4 item 3 already requires), load a fresh game, and check for load errors in `logs/error.log`. Setup: vanilla install, no save needed.

### C142 — DEFERRED

> A mission whose sense depends on a specific authored direction can become moot under reorientation.
>
> *OUTCOME / derivation / depends on C139, C140*

**Method.** OUTCOME.

### C143 — OUT_OF_SCOPE

> That breakage is accepted and deferred to a compatibility pass rather than engineered around.
>
> *DESIGN / stipulated / depends on C142*

**Method.** DESIGN.


---

## §1.11

### C144 — OUT_OF_SCOPE

> The overlord always receives the treasure fleet.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C145 — OUT_OF_SCOPE

> The fleet routes by the §1.10 fallback ladder.
>
> *DESIGN / stipulated / depends on C115, C116, C117*

**Method.** DESIGN.

### C146 — NEEDS_GAME

> Privateers skim a share of the fleet proportional to their power at each node it passes.
>
> *ENGINE / UNSOURCED*

**Method.** Confirmed the mechanism exists and is parameterised, but not the per-node proportionality.

**Evidence.** eu4.exe strings `treasure_fleet_looted`, `TREASURE_FLEET_WE_INTERCEPT`, `PRIVATEER_INCOME_COLLECTION_EFF`, `PIRATES_TRADE_POWER_FACTOR = 1.5`, `PIRATES_MONOPOLY_BONUS = 1`, and the event text `TREASURE_FLEET_TO_US_5:1 "$PIRATES$"` (a per-fleet pirate deduction line). No file states that the skim is proportional to power *at each node the fleet passes*.

**Note.** Settling observation: run a treasure fleet with privateers of known power in exactly one intermediate node, read the `$PIRATES$` line in the `TREASURE_FLEET_TO_US` event, then repeat with the same privateer power spread over two intermediate nodes. Setup: an El Dorado save with a colonial nation and a privateering rival.

### C147 — CONFIRMED (DLC-conditional; see C224)

> Where the diversion mechanic is active, colonial gold income is diverted from the colonial nation.
>
> *ENGINE / UNSOURCED*

**Method.** Located the treasure-fleet mechanic's localisation file, which fixes its DLC.

**Evidence.** All `TREASURE_FLEET_*` gameplay strings live in `localisation/eldorado_l_english.yml`, including `TREASURE_FLEET_TOOLTIP:0 "The next treasure fleet from $COUNTRY$ will arrive in $DATE$. We estimate it will bring us gold and silver worth $NUM$."` - the overlord receives gold that would otherwise be the colonial nation's.

**Note.** What is *not* settled from files is whether the diverted gold still appears in the colonial nation's per-province production income field. That is probe 9, and C049's refutation makes it more important, not less.

### C148 — CONFIRMED (conclusion); premise refuted

> Diverted colonial gold does not enter `wealth` at either end.
>
> *MODEL / stipulated / depends on C032, C147*

**Method.** Follows from C032 as written. But see C049.

**Evidence.** Under `wealth(p) = tax_income(p) + production_income(p)`, gold income of any kind is excluded (C049), so diverted colonial gold trivially does not enter wealth at either end.

**Note.** The conclusion holds; the *reason* the spec gives for it (that gold normally enters wealth and diversion is the exception) is refuted by C049. Section 3.12's bistability argument depends on the refuted reason, not on this conclusion - see C551-C555.


---

## §1.12

### C149 — OUT_OF_SCOPE

> The in-game economy is the per-good economy.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C150 — DEFERRED

> Node values, the node window, pie charts, the ledger, the economy tab, and tooltips all show the model's numbers.
>
> *OUTCOME / stipulated / depends on C149*

**Method.** OUTCOME.

### C151 — DEFERRED

> Trade map mode colours provinces by node.
>
> *OUTCOME / stipulated*

**Method.** OUTCOME.

### C152 — DEFERRED

> Trade map mode draws arrows between nodes from `Φ`.
>
> *OUTCOME / stipulated / depends on C062*

**Method.** OUTCOME.

### C153 — OUT_OF_SCOPE

> Arrow weight comes from realized value crossing the link.
>
> *DESIGN / stipulated / depends on C152*

**Method.** DESIGN.

### C154 — DEFERRED

> Clicking a province switches province colouring to the vanilla trade-goods rendering for that good.
>
> *OUTCOME / stipulated*

**Method.** OUTCOME.

### C155 — DEFERRED

> Clicking a province redirects the arrow layer to that good's graph.
>
> *OUTCOME / stipulated / depends on C005*

**Method.** OUTCOME.

### C156 — DEFERRED

> A sink is then visible as a node with no outgoing arrows.
>
> *OUTCOME / derivation / depends on C010, C155*

**Method.** OUTCOME.

### C157 — DEFERRED

> Clicking the node icon clears the view back to `Φ`.
>
> *OUTCOME / stipulated / depends on C152*

**Method.** OUTCOME.

### C158 — PARTIAL

> The vanilla UI holds one value field per node.
>
> *ENGINE / UNSOURCED*

**Method.** Read the node window definition in `interface/tradeinterface.gui` and enumerated its value fields.

**Evidence.** The node window has **four** node-level value fields, not one: `incoming_value` (`TN_INCOMING_VALUE:0 "Incoming:"`), `local_value` (`TN_LOCAL_VALUE:0 "Local:"`), `total_value` (`TN_TOTAL_VALUE:0 "Total:"`), `outgoing_value` (`TN_OUTGOING_VALUE:0 "Outgoing:"`), plus `our_from_this`, `piracy_value` and `retention_power`. The map-mode tooltip mirrors them (`TRADEMAP_INCOMING`, `TRADEMAP_LOCAL`, `TRADEMAP_TOTAL`, `TRADEMAP_OUTGOING_SMALL`). None of the seven carries a commodity argument.

**What is actually true.** The vanilla UI holds several value fields per node; what it holds none of is a *per-commodity* field.

**Spec text that must change.** "Value broken down by commodity. One value field per node, not thirty." (spec.md, section 1.12)

**Blast radius.** C160 survives unchanged - the conclusion is about the absence of per-commodity fields, which is confirmed. Only the count in the premise is wrong.

### C159 — CONFIRMED

> EU4 has about thirty trade goods.
>
> *ENGINE / file value*

**Method.** Counted top-level blocks in `common/tradegoods/00_tradegoods.txt` and cross-checked `common/prices/00_prices.txt`.

**Evidence.** 32 goods defined; excluding `gold` (`goldtype = yes`, `base_price = 0`) and the `unknown` placeholder (`base_price = 0`) leaves exactly **30** tradeable goods. Of those, 29 have nonzero world production at 1444.11.11 (coal is latent).

### C160 — CONFIRMED

> Per-commodity value breakdown is therefore not representable in the vanilla UI.
>
> *ENGINE / derivation / depends on C158, C159*

**Method.** Derivation from C158 and C159; the premise's count is wrong but its substance holds.

**Evidence.** Zero per-commodity value fields exist in `interface/tradeinterface.gui`; 30 goods would be needed.

### C161 — CONFIRMED

> The vanilla UI holds one scalar per link.
>
> *ENGINE / UNSOURCED*

**Method.** Read the link entry window type in `interface/tradeinterface.gui:17-49`.

**Evidence.** `windowType = { name = "TradeNodeLink" ... guiButtonType = { name = "NextNodeButton" ... } instantTextBoxType = { name = "NextNodeButton_label" ... text = "NAME" } }` - one button and one label per link, and the engine's per-link string is the single scalar `TRADEMAP_OUTGOING:0 "$VAL$ is being sent forward to $NAME$."`

### C162 — CONFIRMED

> A link's two-way traffic is therefore not representable and is shown as net.
>
> *ENGINE / derivation / depends on C161*

**Method.** Derivation from C161.

**Evidence.** Valid.

### C163 — CONFIRMED

> Per-country effective trade power is not representable where eligibility differs by good.
>
> *ENGINE / derivation / depends on C088, C084*

**Method.** Derivation from C084 and C088, both confirmed.

**Evidence.** The node window's per-country column is a single `TN_TRADE_POWER` scalar (`interface/tradeinterface.gui:172-177`), with no commodity argument.

### C164 — OUT_OF_SCOPE

> Those three quantities are shown in the companion overlay instead, with trade power as a value-weighted aggregate.
>
> *DESIGN / stipulated / depends on C160, C162, C163*

**Method.** DESIGN.

### C165 — DEFERRED

> No new art, sprites, shaders, or map-mode chrome is required.
>
> *OUTCOME / stipulated*

**Method.** OUTCOME.

### C166 — OUT_OF_SCOPE

> The §1.7 steering-list widening is the only UI change.
>
> *DESIGN / stipulated / depends on C073*

**Method.** DESIGN.

**Note.** See C073: the incoming-links listbox already exists in `tradeinterface.gui`, so the UI change may be smaller than "widening" suggests.


---

## §2.1

### C167 — OUT_OF_SCOPE

> The mod is one program: a runtime-attached DLL.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C168 — OUT_OF_SCOPE

> Each month the DLL reads live game state.
>
> *DESIGN / stipulated / depends on C019*

**Method.** DESIGN.

### C169 — OUT_OF_SCOPE

> Each month it solves per good.
>
> *DESIGN / stipulated / depends on C007*

**Method.** DESIGN.

### C170 — OUT_OF_SCOPE

> It propagates the per-good economy externally, outside the engine.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C171 — OUT_OF_SCOPE

> It writes the result and the orientation back into the engine's own structures.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C172 — OUT_OF_SCOPE

> It ships with a generated `00_tradenodes.txt` for load time.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C173 — OUT_OF_SCOPE

> It ships with a companion overlay for what the engine cannot display.
>
> *DESIGN / stipulated / depends on C164*

**Method.** DESIGN.

### C174 — OUT_OF_SCOPE

> The target platform is Windows/Steam.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C175 — OUT_OF_SCOPE

> The mod runs non-ironman only.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C176 — PARTIAL

> Achievements and ironman are off with the mod installed.
>
> *ENGINE / UNSOURCED / depends on C175*

**Method.** Found the achievement-blocking reason strings in the eu4.exe string table (0x01c37400-0x01c374c0, 0x01cae700-0x01cae7f8) and resolved them in localisation; also searched for a mod/ironman interaction string.

**Evidence.** `ACHIEVEMENTS_DISABLED_MODIFIED_GAME:0 "- EU4 is running a mod or is altered in other ways."` and `ACHIEVEMENTS_DISABLED_NOT_IRONMAN:0 "- Game is not in Ironman Mode."` confirm the achievements half. But the binary also carries the log string **`Loading ironman in modded game`** (0x01c8bf10) - the engine has an explicit code path for exactly that combination.

**What is actually true.** Achievements are disabled by a mod: confirmed. Ironman is **not** disabled by a mod - the engine explicitly supports loading an ironman save in a modded game. Running non-ironman is the mod's own choice (C175, a DESIGN claim), not an engine restriction.

**Spec text that must change.** "Windows/Steam. Non-ironman. Achievements and ironman are off." (spec.md, section 2.1) - the second half overstates the engine.

**Blast radius.** C175 is unaffected (it is a design choice); C187 ("a parser for non-ironman saves") is unaffected in scope but the justification changes: ironman saves are binary-encoded, which is the real reason, not that ironman is unavailable.

### C177 — OUT_OF_SCOPE

> Multiplayer is unsupported by default.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C178 — CONFIRMED

> An identical build on all machines is necessary but not sufficient for multiplayer.
>
> *MODEL / derivation / depends on C179, C180*

**Method.** Derivation; sound given C179 and C180.

**Evidence.** Valid inference.

### C179 — CONFIRMED

> EU4 multiplayer is lockstep with checksums.
>
> *ENGINE / UNSOURCED*

**Method.** eu4.exe string table.

**Evidence.** `Games out of sync:` (0x01cae630), `Out Of Synch: ` (0x01cb3c98), `C:\mnt\gsg\eu4\eu4\eu4\source\checksums.h` (0x01cae670), `CALCULATING_CHECKSUM`, `PLS_WAIT_CHECKSUM`, `version_checksum`, `Checksum in HEX: `, and the warning `Already created a Personal Deity with the name: %s. This can cause errors and **out of synchs in Multiplayer games**...`. EU4 multiplayer detects and reports desynchronisation against a checksum.

**Note.** The checksum and OOS detection are confirmed from the binary. "Lockstep" specifically (deterministic simultaneous simulation rather than authoritative-host) is an architecture inference the strings do not settle, but nothing turns on the distinction for C181-C184.

### C180 — CONFIRMED

> An in-process floating-point solve can produce different results on different hardware.
>
> *MODEL / UNSOURCED*

**Method.** Proof by construction, run in `t_model2.py`: solving one mathematically identical system under permuted accumulation order.

**Evidence.** Six permuted solves of the same 8-node system returned six different floating-point results for the same dead branch, e.g. `phi[5]-phi[6] = +2.945e-17`, `-2.534e-17`, `-2.306e-17`, `-3.379e-17`, `+1.573e-17`, `+5.965e-17`. Accumulation order alone changes the result; different SIMD widths and different BLAS kernels do the same thing for the same reason.

### C181 — DEFERRED

> Differing SIMD dispatch or accumulation order in the linear algebra is enough to desync a session.
>
> *OUTCOME / derivation / depends on C179, C180*

**Method.** OUTCOME.

### C182 — CONFIRMED

> Multiplayer support requires the solve to be bit-reproducible across machines.
>
> *MODEL / derivation / depends on C181*

**Method.** Derivation from C179/C181.

**Evidence.** Valid.

### C183 — CONFIRMED

> Bit-reproducibility requires fixed accumulation order, no runtime-dispatched vector paths, and no threaded reduction.
>
> *MODEL / derivation / depends on C182*

**Method.** Standard result, and the C180 experiment is the direct demonstration: the only thing varied was accumulation order, and the result changed.

**Evidence.** See C180's six divergent results. Fixing accumulation order, dispatch, and reduction threading removes exactly the three sources of that variation.

### C184 — OUT_OF_SCOPE

> Until that is built and verified, the mod ships single-player only.
>
> *DESIGN / stipulated / depends on C183*

**Method.** DESIGN.


---

## §2.2

### C185 — OUT_OF_SCOPE

> A parser for `common/tradenodes/00_tradenodes.txt` is required.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C186 — CONFIRMED

> That file contains adjacency, `members`, `path`/`control` render data, and `end`/`inland`/AI flags.
>
> *ENGINE / file value*

**Method.** Parsed `common/tradenodes/00_tradenodes.txt` with `pdx.py` and enumerated every key that appears at node level.

**Evidence.** `all keys seen at node level: ['ai_will_propagate_through_trade', 'color', 'end', 'inland', 'location', 'members', 'outgoing']`, and each `outgoing` block carries `name`, `path` and `control`. Adjacency (159 directed links), `members`, `path`/`control` render data and the `end`/`inland`/AI flags are all present, as claimed. The claim omits `color`.

### C187 — OUT_OF_SCOPE

> A parser for non-ironman saves is required.
>
> *DESIGN / stipulated / depends on C175*

**Method.** DESIGN.

### C188 — NEEDS_SAVE

> Non-ironman saves expose province owner, `base_tax`, `base_production`, trade good, goods produced, and development.
>
> *ENGINE / file value*

**Method.** Could not verify: all 577 `.eu4` files in the user's save directory are OneDrive cloud placeholders. `[System.IO.File]::ReadAllBytes` returns `The cloud file provider is not running`, and PowerShell reports `locally materialized: 0` of 577 (2.26 GB total).

**Evidence.** File attributes 4199968 = Archive | SparseFile | ReparsePoint | Offline | RecallOnDataAccess. No save could be opened.

**Note.** Settling step: start OneDrive (or copy one non-ironman save from another machine), then confirm the save's `provinces` section carries `owner`, `base_tax`, `base_production`, `trade_goods`, and a goods-produced field. No game launch required - just one readable save. This single unblock also serves C025, C326, C327, C328 and the whole 2.8 historical-set programme.

### C189 — OUT_OF_SCOPE

> A parser for `common/defines.lua` is required.
>
> *DESIGN / stipulated / depends on C211*

**Method.** DESIGN.

### C190 — CONFIRMED

> `common/defines.lua` is merged with `common/defines/` overrides in load order.
>
> *ENGINE / file value*

**Method.** Listed `common/defines/` and read its contents.

**Evidence.** `common/defines/` contains `00_dummy.lua`, `difficulty_easy.lua`, `difficulty_hard.lua`, `difficulty_very_easy.lua`, `difficulty_very_hard.lua`. Vanilla ships override files there, so the merge is real and non-empty; `00_dummy.lua` (90 bytes) exists precisely to demonstrate the override slot.

### C191 — OUT_OF_SCOPE

> The solver computes per-province `wealth`, per-node `trade_value`, `s`, and `c` with per-province α, plus the ε regularizer.
>
> *DESIGN / stipulated / depends on C029, C032, C033*

**Method.** DESIGN.

### C192 — OUT_OF_SCOPE

> The per-good system is solved via sparse Cholesky.
>
> *DESIGN / stipulated / depends on C007*

**Method.** DESIGN.

### C193 — OUT_OF_SCOPE

> The solver computes `Φ`, and `φ₀` for the identity check.
>
> *DESIGN / stipulated / depends on C060, C064*

**Method.** DESIGN.

### C194 — OUT_OF_SCOPE

> A survival table `S_g[n][H]` is computed for AI scoring.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C195 — CONFIRMED

> One survival table serves every country.
>
> *MODEL / derivation / depends on C588*

**Method.** Derivation from C588, itself confirmed.

**Evidence.** Valid.

### C196 — OUT_OF_SCOPE

> A mutual reachability census runs 30 goods × 80 BFS.
>
> *DESIGN / stipulated / depends on C159, C199*

**Method.** DESIGN.

### C197 — CONFIRMED

> The census produces an 80×80 matrix whose entries count the goods having a directed path `n → … → m`.
>
> *MODEL / stipulated / depends on C196*

**Method.** Built the census in `t_model3.py` over the 1444 solve.

**Evidence.** `BFS runs: 2320 (29 live goods x 80 nodes)`; `matrix shape: (80, 80) | max entry: 23 | mean entry: 6.89`; `ordered pairs connected by >=1 good: 6245 / 6320`; `pairs connected by NO good: 75`.

**Note.** Two facts the spec does not yet record and that section 3.8's balance argument (C492, C498) needs: no ordered pair is reachable under *all* goods (max 23 of 29), and 75 of 6320 ordered pairs are reachable under none.

### C198 — OUT_OF_SCOPE

> A synthetic-shock harness edits parsed province data and re-solves.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C199 — CONFIRMED

> EU4 has roughly 80 trade nodes.
>
> *ENGINE / file value*

**Method.** Counted top-level blocks in `common/tradenodes/00_tradenodes.txt`.

**Evidence.** `N nodes: 80` - exactly 80, not approximately.

### C200 — CONFIRMED

> Each per-good solve is a sparse SPD system of roughly 80×80.
>
> *MODEL / derivation / depends on C199*

**Method.** Derivation from C199 plus the parsed structure.

**Evidence.** 80x80 Laplacian with 159 off-diagonal pairs -> 318 off-diagonal nonzeros, density 4.97%. Symmetric positive semidefinite; SPD after the pin. `np.linalg.eigh` gives all eigenvalues >= 0 with exactly one zero.

### C201 — DEFERRED

> Each such solve costs microseconds.
>
> *OUTCOME / UNSOURCED / depends on C200*

**Method.** OUTCOME.

### C202 — OUT_OF_SCOPE

> The listed solver is the reference implementation: standalone, run against parsed saves.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C203 — OUT_OF_SCOPE

> Every validation in §2.8 is measured on the reference solver.
>
> *DESIGN / stipulated / depends on C202*

**Method.** DESIGN.

### C204 — OUT_OF_SCOPE

> The shipped DLL carries a second implementation of solver items 4–7 in the host language.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C205 — OUT_OF_SCOPE

> The DLL implementation reads live memory instead of save files.
>
> *DESIGN / stipulated / depends on C204*

**Method.** DESIGN.

### C206 — OUT_OF_SCOPE

> The two implementations must agree.
>
> *DESIGN / stipulated / depends on C202, C204*

**Method.** DESIGN.

### C207 — OUT_OF_SCOPE

> Where they disagree, the reference is correct by definition.
>
> *DESIGN / stipulated / depends on C206*

**Method.** DESIGN.

### C208 — OUT_OF_SCOPE

> The parsers and the shock harness stay reference-only, and the DLL never reads a save.
>
> *DESIGN / stipulated / depends on C205*

**Method.** DESIGN.

### C209 — OUT_OF_SCOPE

> Inland status is derived as "no coastal province among the node's `members`" rather than trusted from the file's flag.
>
> *DESIGN / stipulated / depends on C210*

**Method.** DESIGN.

### C210 — CONFIRMED

> The node file's `inland` flag cannot be trusted.
>
> *ENGINE / UNSOURCED / depends on C186*

**Method.** Derived coastality from the map bitmap and compared it against the file's flag. Rasterised `map/provinces.bmp` (2048x5632), mapped RGB to province IDs via `map/definition.csv` (0 unmapped pixels), took `sea_starts` (668 provinces) and `lakes` (125) from `map/default.map`, marked every land province with a 4-neighbour sea pixel as coastal (1161 provinces; `force_coastal` is empty), then applied the section 2.2 rule to each node's `members`. Script: `scratchpad/v/coastal.py`.

**Evidence.** 26 nodes carry `inland=yes`; 25 nodes have no coastal member. **One mismatch: `siberia` is flagged `inland=yes` but contains two coastal provinces, 1781 (Western Siberia) and 1782 (Central Siberia)** - both on the Arctic coast. Every other flagged node has exactly 0 coastal members.

**Note.** This is a genuine, reproducible instance, and it is the one node where trusting the flag and deriving it disagree. It also means the derived inland count is 25, not 26 - see C541.


---

## §2.3

### C211 — OUT_OF_SCOPE

> All engine constants are read at runtime and never hardcoded.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C212 — CONFIRMED

> `TRADE_PROPAGATE_DIVIDER` is the define governing the propagation share.
>
> *ENGINE / file value / depends on C105*

**Method.** Read `common/defines.lua` line 1205; confirmed engine reference in the eu4.exe string table at 0x01c6e298.

**Evidence.** `TRADE_PROPAGATE_DIVIDER = 5`.

### C213 — CONFIRMED

> `TRADE_PROPAGATE_THRESHOLD` is the define governing the propagation threshold.
>
> *ENGINE / file value / depends on C106*

**Method.** Read `common/defines.lua` line 1206; string table 0x01c6e2b0.

**Evidence.** `TRADE_PROPAGATE_THRESHOLD = 2`.

### C214 — CONFIRMED

> `TRADE_NON_CAPITAL_OFFICE` is the define governing the off-home collect penalty.
>
> *ENGINE / file value / depends on C072*

**Method.** Read `common/defines.lua` line 1200; string table 0x01c6e248 region.

**Evidence.** `TRADE_NON_CAPITAL_OFFICE = -0.50`.

### C215 — CONFIRMED

> `TRADE_POWER_HOME_BONUS` is the define governing the home-node steering bonus.
>
> *ENGINE / file value / depends on C216*

**Method.** Read `common/defines.lua` lines 1141-1142; string table 0x01c6db28 and 0x01c6dbb8.

**Evidence.** `TRADE_POWER_HOME_BONUS = 0.1` and `TRADE_POWER_HOME_BONUS_MAX = 1`. The spec's table names only the first; the paired `_MAX` define exists and must be read too.

### C216 — CONFIRMED

> Vanilla has a home-node steering bonus.
>
> *ENGINE / file value*

**Method.** Two independent file signals that the home bonus is a *steering* (transfer) bonus rather than a generic one.

**Evidence.** The defines `TRADE_POWER_HOME_BONUS = 0.1` / `TRADE_POWER_HOME_BONUS_MAX = 1`, and the internal identifier **`transfer_home_bonus`** in the eu4.exe string table at 0x020df15c. In EU4's own vocabulary "transfer" is steering (`TRANSFER_TRADE_POWER`, `TRADE_POWER_UPSTREAM`, `TRADE_MERCHANT_ALREADY_TRANSFERRING`), so the identifier's own name ties the home bonus to steering.

### C217 — CONFIRMED (defines exist); see C070 for the efficiency half

> `MERCHANT_MAX_POWER_BONUS` and `TRADE_MERCHANT_PRESENT` are the defines governing merchant power and efficiency.
>
> *ENGINE / file value / depends on C069, C070*

**Method.** Read `common/defines.lua` lines 1197 and 1201.

**Evidence.** `MERCHANT_MAX_POWER_BONUS = 2.0` and `TRADE_MERCHANT_PRESENT = 0.1,  -- bonus on income if trade present`.

**Note.** The mapping of `TRADE_MERCHANT_PRESENT` to *trade efficiency* is contradicted by the define's own comment - see C070.

### C218 — CONFIRMED

> `TRADE_ADDED_VALUE_MODIFER` is the define for the link boost base.
>
> *ENGINE / file value*

**Method.** Read `common/defines.lua` line 1204; corroborated by the engine's own per-link boost tooltip.

**Evidence.** `TRADE_ADDED_VALUE_MODIFER = 0.05` (the file's own misspelling of MODIFIER), and `TRADE_ADDED_VALUE_COUNTRY:0 "$WHO$ increases outgoing value by: $VAL$%"` with `TRADEMAP_OUTGOING_BASE:0 "Before countries increase the outgoing trade value, $BASEVAL$ is leaving $FROMNODE$."`

**Note.** Carry the misspelling verbatim into the parser: the key is `TRADE_ADDED_VALUE_MODIFER`, not `..._MODIFIER`.

### C219 — CONFIRMED

> `CARAVAN_FACTOR`, `CARAVAN_POWER_MAX`, and `CARAVAN_POWER_MIN` are the caravan defines.
>
> *ENGINE / file value*

**Method.** Read `common/defines.lua` lines 1220-1222; all three in the string table at 0x01c6e490/0x01c6e4c0/0x01c6e4d0.

**Evidence.** `CARAVAN_FACTOR = 3.0,  -- Development is divided by this factor, do not set to zero!`, `CARAVAN_POWER_MAX = 50`, `CARAVAN_POWER_MIN = 2`.

### C220 — CONFIRMED

> `PS_MOVE_TRADE_PORT` is the define for the trade capital move cost.
>
> *ENGINE / file value*

**Method.** Read `common/defines.lua` line 762.

**Evidence.** `PS_MOVE_TRADE_PORT = 200`.

### C221 — OUT_OF_SCOPE

> Only two design constants remain in the model.
>
> *DESIGN / stipulated / depends on C041, C222*

**Method.** DESIGN.

### C222 — OUT_OF_SCOPE

> The excluded-goods list defaults to gold.
>
> *DESIGN / stipulated / depends on C048*

**Method.** DESIGN.

### C223 — OUT_OF_SCOPE

> DLC state is a third input axis alongside game files and saves.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C224 — CONFIRMED

> Treasure-fleet diversion is DLC-conditional.
>
> *ENGINE / UNSOURCED*

**Method.** Located the DLC boundary by localisation-file membership, which is how Paradox partitions DLC-gated content.

**Evidence.** Every treasure-fleet gameplay string lives in `localisation/eldorado_l_english.yml` - `TREASURE_FLEET_TOOLTIP`, `TREASURE_FLEET_TOOLTIP_CANT_REACH`, `TREASURE_FLEET_TOOLTIP_CANT_REACH_DELAYED` - and El Dorado ships as `dlc/dlc033_el_dorado`. The generic trade strings by contrast live in `tradenodes_l_english.yml` and `EU4_l_english.yml`.

### C225 — NEEDS_GAME

> Caravan power is DLC-conditional.
>
> *ENGINE / UNSOURCED*

**Method.** Attempted the same localisation-partition test and it does not resolve caravan power.

**Evidence.** `CARAVAN_POWER_DESC2` lives in `powers_and_ideas_l_english.yml` and `TRADEMAP_INLAND_DESC` / `TRADEMAP_INLAND_TITLE` in `tradenodes_l_english.yml` - both **generic** files, not a DLC file. `INLAND_BONUS` is in `EU4_l_english.yml`. So the localisation partition places caravan power in base-game files even if the mechanic itself is DLC-gated in code.

**Note.** Settling observation: with all DLC disabled in the launcher, open an inland node's map tooltip and the country trade view's `INLAND_BONUS` row. If the row is absent or reads 0, the mechanic is DLC-gated. Setup: launcher only, no save - this is the cheapest unresolved item in the whole list.

### C226 — PARTIAL

> Caravan modifier values are readable even when the mechanic is inert.
>
> *ENGINE / UNSOURCED / depends on C225*

**Method.** The defines are in the base `defines.lua`, which is loaded regardless of DLC.

**Evidence.** `CARAVAN_FACTOR`, `CARAVAN_POWER_MAX`, `CARAVAN_POWER_MIN` are all in `common/defines.lua` (lines 1220-1222), not in any DLC archive. Values are therefore readable with the DLC off.

**Note.** Confirmed for these three defines. Whether the same holds for every DLC-conditional value the mod reads is not established; C227's rule is the right response either way.

### C227 — OUT_OF_SCOPE

> Therefore the implementation must key on the DLC flag, never on the presence of a value.
>
> *DESIGN / derivation / depends on C224, C225, C226*

**Method.** DESIGN.


---

## §2.4

### C228 — OUT_OF_SCOPE

> `00_tradenodes.txt` is generated once from the campaign start date's `Φ`.
>
> *DESIGN / stipulated / depends on C062*

**Method.** DESIGN.

### C229 — OUT_OF_SCOPE

> After generation the node structure is owned by the DLL in memory.
>
> *DESIGN / stipulated / depends on C171*

**Method.** DESIGN.

### C230 — OUT_OF_SCOPE

> There is no per-session regeneration of the file.
>
> *DESIGN / stipulated / depends on C228*

**Method.** DESIGN.

### C231 — DEFERRED

> Merchants are recalled only when the mod is rebuilt.
>
> *OUTCOME / derivation / depends on C230, C232*

**Method.** OUTCOME.

### C232 — NEEDS_GAME

> Regenerating the node file recalls merchants.
>
> *ENGINE / UNSOURCED*

**Method.** Nothing on disk describes how the engine reconciles a changed node file against merchant assignments stored in a save.

**Evidence.** No define, no error string, no log string covers it.

**Note.** Settling observation: save with merchants assigned, edit `common/tradenodes/00_tradenodes.txt` (add or move one `outgoing` block), reload the save, and read the merchant list. Setup: one non-ironman save plus one file edit; no debugger. Same trace as C076/probe 5.

### C233 — DEFERRED

> A mid-campaign load runs on the start-date file for up to one month.
>
> *OUTCOME / derivation / depends on C019, C228*

**Method.** OUTCOME.

### C234 — PARTIAL

> The engine performs no topological sort of the node file.
>
> *ENGINE / UNSOURCED*

**Method.** Tested the necessary condition directly: whether the *shipped* file is already topologically sorted. Script `scratchpad/v/graph.py`.

**Evidence.** It is, exactly. Over all 159 directed links, `violations of 'sources declared first': 0` and `violations of 'sinks declared first': 159`. The three `end=yes` nodes are declared last (`genua` at index 77, `venice` 78, `english_channel` 79); the first six declared are `african_great_lakes, kongo, zambezi, patagonia, amazonas_node, rio_grande`. The shipped graph is also acyclic (`vanilla graph cycles found: 0`).

**What is actually true.** The file is topologically sorted with sources first, which is consistent with the engine relying on it - but consistency is not proof that the engine *requires* it. Paradox may simply have authored it that way.

**Blast radius.** C235 (the emission requirement), C236 (which is separately consistent: decreasing Phi puts sources first and sinks last, matching the vanilla convention exactly).

**Note.** Settling observation: move one node block earlier than one of its predecessors in `common/tradenodes/00_tradenodes.txt` without changing any link, load a fresh game, and check the trade map and `logs/error.log`. Setup: vanilla install, one file edit, no save. This is cheap and would convert C234 and C235 outright.

### C235 — OUT_OF_SCOPE

> The emitted file must therefore itself be topologically sorted.
>
> *DESIGN / derivation / depends on C234*

**Method.** DESIGN.

### C236 — OUT_OF_SCOPE

> Declaration order is emitted in decreasing `Φ`.
>
> *DESIGN / stipulated / depends on C235*

**Method.** DESIGN.

### C237 — OUT_OF_SCOPE

> `end=yes` is emitted on every `Φ` sink.
>
> *DESIGN / stipulated / depends on C062*

**Method.** DESIGN.

### C238 — OUT_OF_SCOPE

> `end=yes` is stripped from any former end node that gains outgoing links.
>
> *DESIGN / stipulated / depends on C237*

**Method.** DESIGN.

### C239 — CONFIRMED

> Reversing a link requires moving the `outgoing` block, reversing the `path` province list, and reversing the `control` pairs.
>
> *ENGINE / file value / depends on C186*

**Method.** Read the `outgoing` block structure in `common/tradenodes/00_tradenodes.txt` and confirmed both `path` and `control` are ordered geometry.

**Evidence.** e.g. `african_great_lakes` -> `outgoing={ name="zanzibar" path={ 1273 1202 } control={ 3351.000000 607.000000  3388.000000 610.000000  3416.000000 580.000000 } }`. `path` is an ordered province list from source to target and `control` is an ordered list of 2D spline control points; reversing the link requires reversing both, and moving the block to the other node. There are no reciprocal declarations to reuse: `bidirectional pairs (both directions declared): 0`, and `distinct undirected pairs: 159` equals the directed edge count.

### C240 — OUT_OF_SCOPE

> One hand-flipped link is to be verified before generator code is written.
>
> *DESIGN / stipulated / depends on C239*

**Method.** DESIGN.

### C241 — OUT_OF_SCOPE

> `location`, `members`, `inland=yes`, `ai_will_propagate_through_trade`, and unrecognized keys round-trip byte-faithfully.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C242 — CONFIRMED

> The node file contains `location`, `members`, `inland`, and `ai_will_propagate_through_trade` keys.
>
> *ENGINE / file value*

**Method.** Parsed `common/tradenodes/00_tradenodes.txt` and enumerated node-level keys.

**Evidence.** All four named keys occur: `location` (80 nodes), `members` (80), `inland` (26), `ai_will_propagate_through_trade` (4). The file also carries `color` (80) and `end` (3), which the claim does not list.


---

## §2.5

### C243 — OUT_OF_SCOPE

> Attachment uses pattern scanning and function hooking.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C244 — NEEDS_GAME

> The EU4dll precedent provides attach scaffolding on this binary.
>
> *ENGINE / prose source*

**Method.** Prose-sourced (a third-party project). The audit rules forbid citing web sources as validation, and the EU4dll project is not present on this disk.

**Evidence.** No copy of EU4dll exists under the EU4 install or the user's mod directory (`mod/` contains only `per-good-trade`).

**Note.** Settling step: obtain the EU4dll source and check that its attach path targets `eu4.exe` for this build. What can be confirmed from disk right now is the target: `eu4.exe` is a 38,462,504-byte PE at version `v1.37.5.0` (`launcher-settings.json`), with `dbghelp.dll` shipped alongside it.

### C245 — NEEDS_GAME

> EU4dll provides nothing about trade structures.
>
> *ENGINE / prose source / depends on C244*

**Method.** Same as C244.

**Evidence.** Not verifiable from this disk.

**Note.** Same step as C244.

### C246 — OUT_OF_SCOPE

> The mod ships a runtime-patching DLL, not a modified executable.
>
> *DESIGN / stipulated / depends on C167*

**Method.** DESIGN.

### C247 — CONFIRMED

> The EU4 binary is frozen.
>
> *ENGINE / derivation / depends on C001*

**Method.** Read the shipped version metadata.

**Evidence.** `launcher-settings.json`: `"version": "EU4 v1.37.5.0 Inca (491d)"`, `"rawVersion": "v1.37.5.0"`; `eu4_rev.txt` / `clausewitz_rev.txt` carry the fixed revision hash `835bfdf8ca24c291a1b3f1b5bc72d47e7df1ae18`; `checksum_manifest.txt` is shipped. 1.37.5 Inca is EU4's final content patch, so the binary this mod targets is fixed.

### C248 — DEFERRED

> Therefore offsets found stay found.
>
> *OUTCOME / derivation / depends on C247*

**Method.** OUTCOME.

### C249 — OUT_OF_SCOPE

> The nation-pair direction gates of §1.10 are hooked and returned true at the call site.
>
> *DESIGN / stipulated / depends on C112*

**Method.** DESIGN.

### C250 — OUT_OF_SCOPE

> They are not implemented by forcing any shared predicate.
>
> *DESIGN / stipulated / depends on C249*

**Method.** DESIGN.


---

## §2.6

### C251 — NEEDS_GAME

> The monthly trade tick runs in three passes.
>
> *ENGINE / UNSOURCED*

**Method.** No file describes the trade tick's internal structure. Searched defines, static modifiers, the .gui files and the eu4.exe string table for pass names or ordering hints; none exist.

**Evidence.** The only structural hints in the binary are `update_supply_range` and the `_bUpdateSupplyRangeCache` log lines, which are naval, not trade.

**Note.** Debugger-only. Settling setup: attach to eu4.exe 1.37.5, breakpoint the monthly trade update, and step the three passes. One session covers this and every other 2.7 item. This is 2.7 probe 1 and everything in 2.6 rests on it.

### C252 — NEEDS_GAME

> Pass 1 computes static power and modifiers.
>
> *ENGINE / UNSOURCED / depends on C251*

**Method.** Same as C251.

**Evidence.** No file evidence.

**Note.** Debugger-only. Settling setup: attach to eu4.exe 1.37.5, breakpoint the monthly trade update, and step the three passes. One session covers this and every other 2.7 item.

### C253 — NEEDS_GAME

> Pass 2 runs from the end nodes, determining modified power and adding propagation.
>
> *ENGINE / UNSOURCED / depends on C251*

**Method.** Same as C251.

**Evidence.** No file evidence.

**Note.** Debugger-only. Settling setup: attach to eu4.exe 1.37.5, breakpoint the monthly trade update, and step the three passes. One session covers this and every other 2.7 item.

### C254 — NEEDS_GAME

> Pass 3 is a value pass from the origin nodes: node value → collect/steer split → collect division → outgoing division with steering bonuses.
>
> *ENGINE / UNSOURCED / depends on C251*

**Method.** Same as C251.

**Evidence.** No file evidence.

**Note.** Debugger-only. Settling setup: attach to eu4.exe 1.37.5, breakpoint the monthly trade update, and step the three passes. One session covers this and every other 2.7 item.

### C255 — OUT_OF_SCOPE

> Node trade value is written as `Σ_g value_g(n)`.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C256 — OUT_OF_SCOPE

> Node collectible pool is written as `Σ_g value_g(n)·collected_share(n,g)`.
>
> *DESIGN / stipulated / depends on C086, C087*

**Method.** DESIGN.

### C257 — OUT_OF_SCOPE

> Per-link value is written as the net `Σ_g` realized flow in the installed `Φ` direction.
>
> *DESIGN / stipulated / depends on C062*

**Method.** DESIGN.

### C258 — NEEDS_GAME

> Country trade income is derived by the engine from the written fields, unless it is stored.
>
> *ENGINE / UNSOURCED*

**Method.** Cannot be settled from files: whether country trade income is a stored field or recomputed from node fields is a memory-layout question.

**Evidence.** `INCOME_FROM_NODES_I:0 "Last month you got $VAL$ from trade."` shows a *retained* last-month figure exists, which is weak evidence for storage, but says nothing about derivation.

**Note.** Debugger-only. Settling setup: attach to eu4.exe 1.37.5, breakpoint the monthly trade update, and step the three passes. One session covers this and every other 2.7 item. This is 2.7 probe 3.

### C259 — CONFIRMED

> Feeding the engine the collectible pool is sufficient to pay every country correctly.
>
> *MODEL / derivation / depends on C264, C265*

**Method.** Derivation from C264 and C265, both confirmed by the C521/C522 experiment.

**Evidence.** See C521: `max abs difference: 1.421e-14` between the per-good sum and the scalar model.

### C260 — CONFIRMED

> `collect_pool` is per good on the inside.
>
> *MODEL / derivation / depends on C256, C261*

**Method.** Derivation, and a direct consequence of the spec's own section 1.8 definitions.

**Evidence.** `collected_share(n,g) = P_collect / (P_collect + P_transfer(g))` carries a `g` argument on the denominator only, so the pool is a per-good sum.

### C261 — CONFIRMED

> `collected_share(n,g)` depends on `P_transfer(g)`, which §1.8 makes commodity-specific.
>
> *MODEL / derivation / depends on C087, C088*

**Method.** Derivation from C087 and C088.

**Evidence.** Immediate from the formula.

### C262 — PARTIAL

> `powershare_C` is a country's share among collectors.
>
> *ENGINE / UNSOURCED / depends on C099*

**Method.** Inherits C099's status: the share-among-collectors quantity is indicated but not confirmed.

**Evidence.** See C099.

**Note.** Settled by the same two-collector observation as C099.

### C263 — CONFIRMED

> Whether a country collects is a merchant-or-home property with no good dependence.
>
> *MODEL / derivation / depends on C067*

**Method.** Derivation: collect intent is set per merchant per node (C084), with no commodity argument anywhere in the engine's intent strings.

**Evidence.** `TRADE_MERCHANT_ALREADY_COLLECTING:0 "$ENVOY$ is already collecting from trade here."` - one intent, no good.

### C264 — CONFIRMED

> A good-independent share multiplying a per-good sum collapses to one scalar.
>
> *MODEL / derivation / depends on C262, C263*

**Method.** Algebra plus a numerical check with mixed sinks, mixed collectors and the off-home penalty active (`t_model3.py`).

**Evidence.** `sum_g v_g * cs_g * ps = ps * sum_g v_g * cs_g` whenever `ps` has no `g` dependence. Measured: per-good income `[8.2527886288, 88.8345607938, 0.0, 104.3157035514]` vs scalar income `[8.2527886288, 88.8345607938, 0.0, 104.3157035514]`, `max abs difference: 1.421e-14` on a node paying 201.40.

### C265 — CONFIRMED

> The engine's own vanilla collection math then reproduces every country's per-good income exactly.
>
> *MODEL / derivation / depends on C264*

**Method.** Derivation from C264.

**Evidence.** Same experiment; agreement at 1.4e-14 relative to a 201-ducat pool.

### C266 — OUT_OF_SCOPE

> Display figures must be written immediately after the value pass.
>
> *DESIGN / derivation / depends on C267*

**Method.** DESIGN.

### C267 — NEEDS_GAME

> AI consumers read those figures during the month.
>
> *ENGINE / UNSOURCED*

**Method.** No file records when AI consumers read the display fields.

**Evidence.** No evidence on disk.

**Note.** Debugger-only. Settling setup: attach to eu4.exe 1.37.5, breakpoint the monthly trade update, and step the three passes. One session covers this and every other 2.7 item. 2.7 probe 3.

### C268 — OUT_OF_SCOPE

> Payment writes are bounded by the month boundary.
>
> *DESIGN / derivation / depends on C269*

**Method.** DESIGN.

### C269 — NEEDS_GAME

> The treasury reconciles at the start of each month against the previous month's income.
>
> *ENGINE / UNSOURCED*

**Method.** The monthly reconciliation is visible in the localisation, but its ordering relative to the value pass is not.

**Evidence.** `INCOME_FROM_NODES_I:0 "Last month you got $VAL$ from trade."` and `INCOME_FROM_NODES_D:0 "Your estimated income from trade next month is $VAL$..."` confirm a month-boundary settle of the previous month's figure. The *ordering* against the value pass is not on disk.

**Note.** Debugger-only. Settling setup: attach to eu4.exe 1.37.5, breakpoint the monthly trade update, and step the three passes. One session covers this and every other 2.7 item. 2.7 probe 3.

### C270 — CONFIRMED

> There are two deadlines, not one window.
>
> *MODEL / derivation / depends on C266, C268*

**Method.** Derivation from C266 and C268 as stated.

**Evidence.** Valid as an inference; both premises are design stipulations resting on NEEDS_GAME engine facts.

### C271 — CONFIRMED

> Per-link written values can be negative where realized flow opposes the drawn arrow.
>
> *MODEL / derivation / depends on C257, C508*

**Method.** Derivation from C257 and C508; C508 is separately confirmed by construction (see its entry).

**Evidence.** If the written per-link value is net realised flow and realised flow can oppose the installed orientation (C508), the written scalar is negative in exactly those cases.

### C272 — NEEDS_GAME

> The engine accepts a negative per-link value.
>
> *ENGINE / UNSOURCED / depends on C271*

**Method.** No file constrains the sign of a per-link value; the field is engine-internal.

**Evidence.** The engine's per-link string `TRADEMAP_OUTGOING:0 "$VAL$ is being sent forward to $NAME$."` has no sign guard in its format, and `TRADEMAP_OUTGOING_SMALL:0 "Outgoing: -$VAL$"` hard-codes a leading minus, which suggests the display assumes a non-negative magnitude.

**Note.** Settling observation: 2.7 probe 4 - write a negative value into one link field and observe arrow rendering and the protect-trade allocation. The hard-coded `-` in `TRADEMAP_OUTGOING_SMALL` is a concrete reason to expect a display artefact, worth recording before the probe runs.


---

## §2.7

### C273 — DEFERRED

> All ten probes can be settled with a debugger on a vanilla install in one session.
>
> *OUTCOME / UNSOURCED*

**Method.** OUTCOME.

### C274 — NEEDS_GAME

> The three passes may cache independently of one another.
>
> *ENGINE / UNSOURCED / depends on C251*

**Method.** Same as C251.

**Evidence.** No file evidence.

**Note.** Debugger-only. Settling setup: attach to eu4.exe 1.37.5, breakpoint the monthly trade update, and step the three passes. One session covers this and every other 2.7 item. 2.7 probe 1.

### C275 — NEEDS_GAME

> Flipping a link may crash the engine, produce stale-but-running values, or rebuild cleanly.
>
> *ENGINE / UNSOURCED / depends on C274*

**Method.** Same as C251.

**Evidence.** No file evidence.

**Note.** Debugger-only. Settling setup: attach to eu4.exe 1.37.5, breakpoint the monthly trade update, and step the three passes. One session covers this and every other 2.7 item. 2.7 probe 1.

### C276 — DEFERRED

> Staleness would show as one-month corridor lag, value vanishing, tooltips disagreeing with arrows, or propagation crediting the wrong side.
>
> *OUTCOME / UNSOURCED / depends on C275*

**Method.** OUTCOME.

### C277 — NEEDS_GAME

> Pass 2 has an ordering requirement whose cause is unidentified.
>
> *ENGINE / derivation / depends on C109, C253*

**Method.** Derivation resting on C109 and C253, both NEEDS_GAME.

**Evidence.** No file evidence.

**Note.** C109 (one-hop propagation) is settleable *without* a debugger - see its entry. Doing that first narrows probe 2 substantially.

### C278 — NEEDS_GAME

> Where income accumulation sits relative to the value pass is unknown.
>
> *ENGINE / UNSOURCED / depends on C254*

**Method.** Same as C258.

**Evidence.** No file evidence.

**Note.** Debugger-only. Settling setup: attach to eu4.exe 1.37.5, breakpoint the monthly trade update, and step the three passes. One session covers this and every other 2.7 item. 2.7 probe 3.

### C279 — DEFERRED

> Writing country trade income before month-boundary reconciliation may make AI budgeting and AI cash read the same figure.
>
> *OUTCOME / UNSOURCED / depends on C269*

**Method.** OUTCOME.

### C280 — NEEDS_GAME

> A negative link value can be written and its arrow rendering observed.
>
> *ENGINE / UNSOURCED / depends on C272*

**Method.** Same as C272.

**Evidence.** See C272 for the `TRADEMAP_OUTGOING_SMALL` sign observation.

**Note.** 2.7 probe 4.

### C281 — PARTIAL

> Link values feed a protect-trade allocation.
>
> *ENGINE / UNSOURCED*

**Method.** Confirmed a protect-trade AI mission exists and is node-scoped; not that link values feed its allocation.

**Evidence.** eu4.exe strings `START_PRIVATEER_MISSION`, `PRIVATEER_MISSION_DESC:0 "Privateering Trade Node $NODE$"`, `_CAI_PLAN_SEND_MERCHANT_`, `Evaluating merchants for: `, and the AI defines `PEACE_TERMS_TRADE_POWER_VALUE_MULT = 0.1, -- AI desire for transfering trade power is multiplied by this for each 0.1 trade value in shared nodes` and `DIPLOMATIC_ACTION_EMBARGO_TRADE_POWER_FACTOR = 25.0, -- ... for each 1.0 value in shared nodes`. All of these key on **node** value, not link value.

**Note.** Concrete finding to carry into probe 4: every AI trade define found on disk reads node value, none reads link value. That narrows what a negative link value can break.

### C282 — NEEDS_GAME

> Flipping a link that hosts a steering merchant may dangle, reset, or crash the assignment.
>
> *ENGINE / UNSOURCED / depends on C076*

**Method.** Same as C076.

**Evidence.** No file evidence.

**Note.** 2.7 probe 5; settleable with one edited node file and one save, without a debugger.

### C283 — NEEDS_GAME

> Whether the engine grants caravan power for a merchant assigned to a link that is incoming in `Φ` is unknown.
>
> *ENGINE / UNSOURCED / depends on C079*

**Method.** The engine's own inland tooltip narrows this considerably but does not close it.

**Evidence.** `TRADEMAP_INLAND_DESC:0 "Having a merchant present that **collects in** an inland trade node, **or steers towards** an inland trade node, will give you extra trade power **in that node** based on your trade efficiency."` plus the two internal identifiers **`merchant_present_inland`** (0x021a6c84) and **`merchant_steering_to_inland`** (0x021a6e8c) in the eu4.exe string table.

**Note.** The two internal names show the engine already distinguishes the two grant conditions, and both are phrased from the inland node's side. Settling observation: place a merchant to steer *out of* an inland node (link incoming to the inland node in Phi) and read the country's `INLAND_BONUS` row and the node's trade-power breakdown. 2.7 probe 6, first half. See C538 for the location question, which is the sharper issue.

### C284 — NEEDS_GAME

> Whether the engine grants caravan power for a merchant whose link carries no goods is unknown.
>
> *ENGINE / UNSOURCED / depends on C079*

**Method.** Same evidence as C283.

**Evidence.** `TRADEMAP_INLAND_DESC` conditions on a merchant that "collects in" or "steers towards" an inland node; nothing in it checks whether value actually moves.

**Note.** 2.7 probe 6, second half. Settling observation: assign a merchant to steer on a link that carries zero value and read the `INLAND_BONUS` row.

### C285 — NEEDS_GAME

> Whether arrow render state is separate from the economic link is unknown.
>
> *ENGINE / UNSOURCED*

**Method.** The .gui files separate the arrow layer from the node window, but arrow geometry comes from the node file's `path`/`control` data and the rendering is engine-side.

**Evidence.** `interface/traderoutes.gfx` and `interface/tradeinterface.gfx` exist as separate sprite sets from `tradeinterface.gui`; the geometry source is the `control` spline in `common/tradenodes/00_tradenodes.txt`.

**Note.** 2.7 probe 7. Settling observation: reverse one link's `outgoing` block *without* reversing its `control` list and see whether the arrow draws backwards or crashes. Setup: one file edit, no debugger - this also directly exercises 2.4 item 3.

### C286 — CONFIRMED (as arithmetic)

> Setting `TRADE_PROPAGATE_THRESHOLD` to 4 would double the raw requirement if the propagated-units reading is right.
>
> *ENGINE / derivation / depends on C106*

**Method.** Arithmetic on the confirmed defines.

**Evidence.** `TRADE_PROPAGATE_THRESHOLD` 2 -> 4 with `TRADE_PROPAGATE_DIVIDER = 5` gives 4 x 5 = 20, double the current 10. The falsification design is sound; the reading it tests is C568.

### C287 — NEEDS_GAME

> Whether diverted colonial gold still appears in the per-province production income field is unknown.
>
> *ENGINE / UNSOURCED / depends on C147*

**Method.** See C147.

**Evidence.** Not on disk.

**Note.** 2.7 probe 9. C049's refutation raises the stakes: if gold income is a separate income category rather than production income, the diverted-gold question is about which of *two* fields, not one.

### C288 — NEEDS_GAME

> The DLC flag is expected to agree with the observed diverted-gold field.
>
> *ENGINE / UNSOURCED / depends on C224*

**Method.** See C224 - the DLC identity is confirmed (El Dorado) but the flag/field agreement is not.

**Evidence.** Treasure-fleet strings live in `localisation/eldorado_l_english.yml`; `dlc/dlc033_el_dorado` ships them.

**Note.** 2.7 probe 9.

### C289 — DEFERRED

> Every call site of "is X downstream of Y" can be enumerated by disassembly.
>
> *OUTCOME / UNSOURCED*

**Method.** OUTCOME.

**Evidence.** Partial delivery available now: static string-table analysis of eu4.exe already yields three named direction call sites - `DIPLO_SELLPROV_NOT_UPSTREAM`, `TREASURE_FLEET_TOOLTIP_CANT_REACH`, and `TRADE_POWER_UPSTREAM`. See the 'Direction call sites found statically' section of the summary.

### C290 — OUT_OF_SCOPE

> Those call sites classify as: return true; return true and define the scope; or compute per good.
>
> *DESIGN / stipulated / depends on C112, C114*

**Method.** DESIGN.

### C291 — OUT_OF_SCOPE

> A companion "not members" list will be produced alongside the call-site list.
>
> *DESIGN / stipulated / depends on C289*

**Method.** DESIGN.

### C292 — OUT_OF_SCOPE

> All writes land atomically at the tick hook with the sim paused.
>
> *DESIGN / stipulated / depends on C293*

**Method.** DESIGN.

### C293 — NEEDS_GAME

> The sim can be paused at the tick hook.
>
> *ENGINE / UNSOURCED*

**Method.** A debugger capability question; nothing on disk bears on it.

**Evidence.** No file evidence.

**Note.** Debugger-only. Settling setup: attach to eu4.exe 1.37.5, breakpoint the monthly trade update, and step the three passes. One session covers this and every other 2.7 item.


---

## §2.8

### C294 — DEFERRED

> Spice and cloves in 1444 source in Indonesia.
>
> *OUTCOME / UNSOURCED / depends on C023*

**Method.** OUTCOME.

**Evidence.** Reference-solver note (proxy wealth, see the Method caveat in the summary): at 1444 with alpha keyed to base price, the two goods source in Indonesia as expected but sink at `saxony` (spices) and `kongo`/`safi`/`wien` (cloves), not in China.

### C295 — DEFERRED

> Spice and cloves in 1444 sink in both China and Europe.
>
> *OUTCOME / UNSOURCED / depends on C010, C033*

**Method.** OUTCOME.

**Evidence.** Contrary reference-solver data point: neither spices nor cloves sinks in a Chinese node under the 1444 proxy dataset. Listed in the summary under OUTCOME claims with contrary evidence.

### C296 — DEFERRED

> In 1444 most goods have their largest sinks in India and China.
>
> *OUTCOME / UNSOURCED / depends on C033*

**Method.** OUTCOME.

**Evidence.** Contrary reference-solver data point: the most frequent sinks on 1444 proxy data are `safi` (12 of 29 goods), `gulf_of_siam` (11), `saxony` (7), `the_moluccas` (7), `doab` (6) - not India and China. Sinks are minima of phi, which land where c-s is most negative *and* the graph bottoms out, not simply where demand is largest.

### C297 — OUT_OF_SCOPE

> That India/China sink concentration is correct behaviour, not a failure.
>
> *DESIGN / stipulated / depends on C296*

**Method.** DESIGN.

### C298 — DEFERRED

> Post-1500, spice routes Malacca → … → Cape → … → Europe.
>
> *OUTCOME / UNSOURCED / depends on C008*

**Method.** OUTCOME.

**Evidence.** Structural note: `malacca` has a **direct** outgoing link to `cape_of_good_hope` in `common/tradenodes/00_tradenodes.txt`, and the vanilla directed path is `malacca -> cape_of_good_hope -> ivory_coast -> english_channel`. The corridor's ellipsis on the Malacca side is empty.

### C299 — DEFERRED

> Pre-1500 that corridor is withheld by range and the power-at-both-ends gate, not by direction.
>
> *OUTCOME / derivation / depends on C100, C101, C102*

**Method.** OUTCOME.

**Evidence.** Two of its three named gates are wrong: supply range does not exist (C101 REFUTED) and trade range gates merchant placement rather than flow (C100 PARTIAL). Only the power-at-both-ends gate (C102) is available, and that is NEEDS_GAME.

### C300 — DEFERRED

> A 1000 AD start puts sinks in the Muslim world and Song China with no era-specific data added.
>
> *OUTCOME / UNSOURCED / depends on C033*

**Method.** OUTCOME.

### C301 — DEFERRED

> Zeroing Beijing-node development relocates the sink in one solve.
>
> *OUTCOME / derivation / depends on C033, C022*

**Method.** OUTCOME.

### C302 — DEFERRED

> If Ming loses the Mandate, Beijing's pull collapses with its income.
>
> *OUTCOME / derivation / depends on C032, C303*

**Method.** OUTCOME.

**Evidence.** Mechanism note from files: `lost_mandate_of_heaven = { ... global_trade_goods_size_modifier = -0.5 ... }` cuts *goods produced*, so it lowers Ming's supply `s` at the same time as its production income and demand `c`. The two effects push phi in opposite directions; the prediction is not one-sided.

### C303 — CONFIRMED

> Losing the Mandate of Heaven substantially cuts Ming's income.
>
> *ENGINE / UNSOURCED*

**Method.** Read the Mandate static modifier in `common/static_modifiers/00_static_modifiers.txt:683`.

**Evidence.** `lost_mandate_of_heaven = { discipline = -0.1  stability_cost_modifier = 0.5  global_unrest = 10  **global_trade_goods_size_modifier = -0.5**  fire_damage_received = 0.5  shock_damage_received = 0.5  reduced_liberty_desire = -50  legitimacy = -1  mercenary_manpower = -0.5  global_manpower_modifier = -0.5 }`. Goods produced is halved empire-wide, which halves both production income and trade value. Ming's 1444 development is 1102, the largest in the game by a factor of 3.3 over England (338), so the absolute income swing is the largest on the map.

**Note.** Mechanism note the spec's C302 does not carry: because the modifier cuts *goods produced*, it lowers Ming's supply `s` at the same time as its demand `c`. The two push phi in opposite directions, so "Beijing's pull collapses" is not a one-sided prediction - the net effect must be measured, not assumed.

### C304 — DEFERRED

> A major war in China shifts corridors for its duration.
>
> *OUTCOME / derivation / depends on C027*

**Method.** OUTCOME.

### C305 — DEFERRED

> Those corridors revert as devastation heals.
>
> *OUTCOME / derivation / depends on C026*

**Method.** OUTCOME.

### C306 — DEFERRED

> Given many poor provinces versus few rich ones, luxury demand goes to the rich-province node.
>
> *OUTCOME / derivation / depends on C043*

**Method.** OUTCOME.

### C307 — DEFERRED

> Bulk demand goes to the many-province node.
>
> *OUTCOME / derivation / depends on C045*

**Method.** OUTCOME.

### C308 — DEFERRED

> A price crash drives α below 1.
>
> *OUTCOME / derivation / depends on C040*

**Method.** OUTCOME.

### C309 — DEFERRED

> A price crash makes regional sinks reappear.
>
> *OUTCOME / derivation / depends on C045, C308*

**Method.** OUTCOME.

### C310 — DEFERRED

> In the 1650 Caribbean, sugar production income makes it a sink for cloth, tools, and wine.
>
> *OUTCOME / derivation / depends on C032*

**Method.** OUTCOME.

**Evidence.** Note: computed through the autonomy floor, which C037/C038 refute - a Caribbean territory contributes ~10%, a colonial core ~50%, not 25%.

### C311 — DEFERRED

> In 1000, Kilwa's ivory income makes it a sink for Indian textiles.
>
> *OUTCOME / derivation / depends on C032*

**Method.** OUTCOME.

### C312 — CONFIRMED

> A consuming leaf node terminates the DAG of every good it consumes but does not produce.
>
> *MODEL / derivation / depends on C010*

**Method.** Derivation from C010 and C382, then checked exhaustively over every (good, sink) pair on the 1444 solve.

**Evidence.** `(good, sink) pairs: 102 | pairs where s >= c: 0`. Every sink node, for every good it sinks, has strictly `c > s` - it is a net consumer of that good, exactly as the discrete maximum principle requires.

### C313 — DEFERRED

> An inert merchant's goods take the even split as if the node were empty.
>
> *OUTCOME / derivation / depends on C075, C097*

**Method.** OUTCOME.

### C314 — DEFERRED

> An inert merchant's node-wide bonuses still apply.
>
> *OUTCOME / derivation / depends on C071*

**Method.** OUTCOME.

### C315 — CONFIRMED

> At a node sinking spice but not cloth, spice is fully collected while cloth is collected at the ratio with its remainder pushed.
>
> *MODEL / derivation / depends on C086, C087*

**Method.** Derivation from C086 and C087, both definitional.

**Evidence.** Immediate from the two-case formula.

### C316 — DEFERRED

> A near-balanced link may flip monthly.
>
> *OUTCOME / derivation / depends on C019, C022*

**Method.** OUTCOME.

### C317 — DEFERRED

> A flipping link carries near-zero value either way.
>
> *OUTCOME / derivation / depends on C316*

**Method.** OUTCOME.

### C318 — DEFERRED

> Merchant assignments survive such flips.
>
> *OUTCOME / derivation / depends on C076*

**Method.** OUTCOME.

### C319 — DEFERRED

> A two-way Atlantic corridor works with merchants at both ends on disjoint good sets, neither blocking the other.
>
> *OUTCOME / derivation / depends on C078*

**Method.** OUTCOME.

### C320 — DEFERRED

> Every displayed trade figure matches the per-good economy to the ducat.
>
> *OUTCOME / derivation / depends on C265*

**Method.** OUTCOME.

### C321 — CONFIRMED

> Forcing α = 1 makes `Φ` a scalar multiple of `φ₀` on real data.
>
> *MODEL / derivation / depends on C063*

**Method.** This is exactly the C063 experiment run on real data (`t_model.py`).

**Evidence.** `relative residual = 1.959e-15`, `scale factor k = 3662.4000000000` with `spread max-min = 1.114e-10`, `orientation agreement Phi(a=1) vs phi0: 159 / 159 edges`.

**Note.** Important implementation caveat that the spec does not state: the identity holds exactly **only if the same epsilon regulariser is applied to phi0's supply vector**. Applied to the per-good solves alone, as section 1.2 and section 1.6 read literally, the residual is 1.15e-5 at eps=1e-6. See C462.

### C322 — OUT_OF_SCOPE

> Acyclicity is asserted on every solve.
>
> *DESIGN / stipulated / depends on C009*

**Method.** DESIGN.

### C323 — DEFERRED

> An observer run to 1600 shows New World colonization proceeding at roughly vanilla pace.
>
> *OUTCOME / UNSOURCED*

**Method.** OUTCOME.

### C324 — DEFERRED

> Greedy AI merchant assignment settles with damping rather than oscillating.
>
> *OUTCOME / UNSOURCED / depends on C610*

**Method.** OUTCOME.

### C325 — CONFIRMED

> A latent good has no graph, no `Φ` contribution and no survival-table entry, and acquires all three the month production begins.
>
> *MODEL / derivation / depends on C052, C053, C054, C055*

**Method.** Derivation from C052-C055, all confirmed; instantiated on the 1444 dataset.

**Evidence.** Coal at 1444: world production 0, `V_coal = 0`, excluded from the 29 live goods, absent from the 29 x 80 x 80 survival table.

**Note.** The month of acquisition is governed by coal's Enlightenment-default trigger, not Manufactories - see C057.

### C326 — DEFERRED

> The DLL solver and the reference solver agree on orientation exactly for every save in the historical set.
>
> *OUTCOME / UNSOURCED / depends on C206*

**Method.** OUTCOME.

**Evidence.** Blocked on data as well as on build: no save could be read (see C188).

### C327 — DEFERRED

> They agree on `φ` to tolerance for every save in the historical set.
>
> *OUTCOME / UNSOURCED / depends on C206*

**Method.** OUTCOME.

**Evidence.** Blocked on data as well as on build: no save could be read (see C188).

### C328 — OUT_OF_SCOPE

> There is a historical set of saves to validate against.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

**Note.** Blocked in practice: no save on this machine is readable (C188).

### C329 — OUT_OF_SCOPE

> `Φ`-vs-realized sign disagreement is weighted by trade value, not link count.
>
> *DESIGN / stipulated / depends on C271*

**Method.** DESIGN.

### C330 — DEFERRED

> That disagreement is predicted to cluster at nodes with 3+ outgoing links and partial merchant coverage.
>
> *OUTCOME / derivation / depends on C092, C097*

**Method.** OUTCOME.

### C331 — DEFERRED

> It is predicted to thin as merchant coverage densifies.
>
> *OUTCOME / derivation / depends on C330*

**Method.** OUTCOME.

### C332 — DEFERRED

> Flip behaviour per decade differs between peace and war.
>
> *OUTCOME / UNSOURCED / depends on C027*

**Method.** OUTCOME.

### C333 — DEFERRED

> Flips revert as occupation lifts.
>
> *OUTCOME / derivation / depends on C027*

**Method.** OUTCOME.

### C334 — OUT_OF_SCOPE

> Propagated-share change per node is measured on each flip, alongside the trade-power/in-degree covariance.
>
> *DESIGN / stipulated / depends on C120*

**Method.** DESIGN.

### C335 — DEFERRED

> That measurement is what catches the §1.10 threshold mechanics flickering.
>
> *OUTCOME / derivation / depends on C119, C334*

**Method.** OUTCOME.

### C336 — DEFERRED

> A power share crossing a single-valued limit is the failure mode.
>
> *OUTCOME / derivation / depends on C131*

**Method.** OUTCOME.

### C337 — DEFERRED

> Casus belli availability is the visible symptom of that failure.
>
> *OUTCOME / derivation / depends on C133*

**Method.** OUTCOME.

### C338 — CONFIRMED

> Total propagated power is not the quantity to watch.
>
> *MODEL / derivation / depends on C339*

**Method.** Derivation from C339, confirmed.

**Evidence.** Valid.

### C339 — CONFIRMED

> Reorientation cannot change edge count, so `Σ indeg` equals the edge count and is invariant.
>
> *MODEL / derivation / depends on C140*

**Method.** Proof plus exhaustive check. Proof: each undirected edge contributes exactly one head under any orientation, so `sum_n indeg(n) = |E|` identically. Checked over all live goods in `t_model.py`.

**Evidence.** `distinct values of sum(indeg) across 29 live goods: {159} (|E|=159)` - one value, equal to the edge count, for every good.

### C340 — CONFIRMED

> Only the trade-power/in-degree covariance moves under reorientation.
>
> *MODEL / derivation / depends on C339*

**Method.** Derivation from C339, plus the direct observation that in-degree *distribution* does move while its sum does not.

**Evidence.** Sum invariant at 159; per-node in-degree varies by good (max out-degree 4 at `california` and `ivory_coast`, 24 nodes with >= 3 outgoing links).

### C341 — OUT_OF_SCOPE

> Income balance is measured as total world collected income and as its distribution across historical great powers.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C342 — OUT_OF_SCOPE

> The distribution metric is the gating one.
>
> *DESIGN / stipulated / depends on C341*

**Method.** DESIGN.


---

## §2.9

### C343 — OUT_OF_SCOPE

> The build is two parallel tracks, not phases.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C344 — OUT_OF_SCOPE

> The defines parser comes first on the solver track.
>
> *DESIGN / stipulated / depends on C345*

**Method.** DESIGN.

### C345 — CONFIRMED

> Because every constant is a runtime read, the eligibility threshold, propagation share, off-home penalty, merchant bonuses and caravan terms are all downstream of the defines parser.
>
> *MODEL / derivation / depends on C211*

**Method.** Derivation from C211; each named quantity was traced to a define and all were found.

**Evidence.** eligibility threshold -> `TRADE_PROPAGATE_THRESHOLD = 2`; propagation share -> `TRADE_PROPAGATE_DIVIDER = 5`; off-home penalty -> `TRADE_NON_CAPITAL_OFFICE = -0.50`; merchant bonuses -> `MERCHANT_MAX_POWER_BONUS = 2.0`, `TRADE_MERCHANT_PRESENT = 0.1`; caravan -> `CARAVAN_FACTOR = 3.0`, `CARAVAN_POWER_MAX = 50`, `CARAVAN_POWER_MIN = 2`. Every one is a runtime read.

### C346 — CONFIRMED

> None of them can be written correctly before the defines parser exists.
>
> *MODEL / derivation / depends on C345*

**Method.** Derivation from C345.

**Evidence.** Valid.

### C347 — OUT_OF_SCOPE

> The solver track then does ε, per-good eligibility, realized flows, the `Φ`-vs-realized disagreement measurement, the reachability census, and the flip-rate measurement.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C348 — OUT_OF_SCOPE

> The memory track is the §2.7 probe session.
>
> *DESIGN / stipulated / depends on C273*

**Method.** DESIGN.

### C349 — DEFERRED

> All ten probe items can be done on one trace.
>
> *OUTCOME / UNSOURCED / depends on C273*

**Method.** OUTCOME.

### C350 — OUT_OF_SCOPE

> Afterwards the classified call-site list is written into the spec.
>
> *DESIGN / stipulated / depends on C289*

**Method.** DESIGN.

### C351 — OUT_OF_SCOPE

> Afterwards income balance is gated on both metrics.
>
> *DESIGN / stipulated / depends on C341*

**Method.** DESIGN.

### C352 — OUT_OF_SCOPE

> Afterwards the negative-link display policy is decided against a measured number.
>
> *DESIGN / stipulated / depends on C329*

**Method.** DESIGN.


---

## §3.1

### C353 — OUT_OF_SCOPE

> Goal 1: trade direction follows the world's current state and never authored arrows.
>
> *DESIGN / stipulated / depends on C006*

**Method.** DESIGN (a stated goal).

### C354 — DEFERRED

> A horde razing Beijing moves the sink because the wealth moved.
>
> *OUTCOME / derivation / depends on C032, C301*

**Method.** OUTCOME.

### C355 — OUT_OF_SCOPE

> Goal 2: commodities should flow differently from one another.
>
> *DESIGN / stipulated / depends on C005*

**Method.** DESIGN (a stated goal).

### C356 — OUT_OF_SCOPE (WORLD, and confirmed in-model)

> China is simultaneously a silk source and a spice sink.
>
> *WORLD / UNSOURCED*

**Method.** WORLD claim about history; not about EU4 and not about the model. But its in-model analogue is testable and was tested.

**Evidence.** On 1444 data, `silk` sinks at `rheinland`/`safi`/`valencia` while Chinese nodes are net silk sources, and Chinese nodes take spices as imports - so the model does represent a node that is a source for one good and a sink for another. The historical claim itself is outside this audit's evidence rules.

### C357 — CONFIRMED

> A single trade graph cannot represent a node that is source and sink at once for different goods.
>
> *MODEL / derivation / depends on C005, C356*

**Method.** Proof: a single orientation assigns each node one out-degree. A node with out-degree 0 is a sink and cannot also be a source (out-degree > 0) in the same orientation. Only per-good orientations can give the same node both roles.

**Evidence.** Directly exhibited on 1444 data: 36 nodes are a sink for at least one good, and none is a sink for all 29 (`t_model.py`), so every one of them is a non-sink - a source or conduit - for some other good.

### C358 — OUT_OF_SCOPE

> Goal 3: preserve the feedback loop in which sinks accumulate value, fund development, and reinforce themselves.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a stated goal).

### C359 — OUT_OF_SCOPE

> Value accumulation funding development is how mercantile hegemonies form.
>
> *WORLD / UNSOURCED*

**Method.** WORLD - a claim about economic history, outside this audit's evidence rules (no web sources permitted).

### C360 — OUT_OF_SCOPE

> Goal 4: represent return flows.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a stated goal).

### C361 — OUT_OF_SCOPE

> Export regions historically imported manufactures.
>
> *WORLD / UNSOURCED*

**Method.** WORLD - a claim about economic history, outside this audit's evidence rules.

### C362 — CONFIRMED

> Vanilla EU4 cannot express return flows at all.
>
> *ENGINE / UNSOURCED*

**Method.** Structural check on `common/tradenodes/00_tradenodes.txt`, plus the engine's own steering hint.

**Evidence.** `bidirectional pairs (both directions declared): 0` and `distinct undirected pairs: 159` = the directed edge count: no vanilla link is declared in both directions, so no node pair can carry traffic both ways. Corroborated by `HINT_TRADESTEERING_TEXT:0 "...You can never steer trade upstream or past your Main Trading City."` and `HINT_TRADENODE_TEXT:1 "...Trade Value can flow downstream from one Trade Node to the next..."` - both shipped in `localisation/hints_l_english.yml`.

### C363 — OUT_OF_SCOPE

> Goal 5: direction must reflect where a good can ultimately reach, not which neighbour is richer.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a stated goal).

### C364 — OUT_OF_SCOPE

> Goal 6: zero authored data.
>
> *DESIGN / stipulated / depends on C006*

**Method.** DESIGN (a stated goal).

### C365 — OUT_OF_SCOPE

> Goal 7: the game's own numbers are the model's numbers, so anything reading trade income reads the real one.
>
> *DESIGN / stipulated / depends on C149*

**Method.** DESIGN (a stated goal).


---

## §3.2

### C366 — CONFIRMED

> Orienting each edge by comparing its endpoints fails on the Malacca–Cape corridor.
>
> *MODEL / derivation / depends on C369, C371*

**Method.** Reproduced the failure explicitly in `t_model2.py` / `t_model3.py`, with the wealth-rank convention (goods flow toward the richer node) that the spec's own wording implies.

**Evidence.** With `wealth = {Malacca: 10.0, Cape: 0.1, Europe: 12.0}` the rank orientation is `[('Cape','Malacca'), ('Cape','Europe')]`; `corridor Malacca -> Cape -> Europe realized: False`. The potential formulation on the same three-node path returns `phi = [1.0, -5.55e-17, -1.0]`, i.e. `Malacca > Cape > Europe`, and does realise the corridor.

**Note.** Structural corroboration: `malacca` and `cape_of_good_hope` really are directly adjacent in `common/tradenodes/00_tradenodes.txt` (`malacca -> outgoing: ['ganges_delta', 'cape_of_good_hope']`), so the corridor is a single edge, not a metaphor.

### C367 — CONFIRMED (in the strongest possible form)

> The Cape has almost no wealth.
>
> *ENGINE / UNSOURCED*

**Method.** Computed every node's 1444.11.11 wealth from `history/provinces` under the spec's own definition `wealth(p) = tax_income(p) + production_income(p)`, restricted to owned `is_city` provinces (`t_model4.py`).

**Evidence.** `cape_of_good_hope` is the **only node of the 80 with zero owned provinces at the 1444 start**: `nodes with ZERO owned-province wealth at 1444.11.11: 1 ['cape_of_good_hope']`, wealth **0.00** against a world total of 10572.40, i.e. a 0.0000% share. Next poorest: `patagonia` 1.5, `carribean_trade` 1.6, `amazonas_node` 4.2. For contrast `malacca` is 295.20 (2.79%) and `english_channel` 316.60 (2.99%). It is also the smallest node on the map by land province count (19).

**Note.** "Almost no wealth" understates it: at the campaign start the Cape has exactly none.

### C368 — CONFIRMED (in the strongest possible form)

> The Cape consumes almost nothing.
>
> *ENGINE / UNSOURCED*

**Method.** Same computation; consumption is the same wealth quantity under the spec's own model (C032/C033).

**Evidence.** `cape_of_good_hope` wealth 0.00 -> `c(cape, g) = 0` for every good at the 1444 start. Its goods produced is also exactly 0 (`cape members owned at 1444: 0`), so it is a textbook pure conduit at the start date - the one node on the vanilla map for which section 3.2's `s(n) = c(n) = 0` case is literally realised.

**Note.** This makes C376-C378 non-vacuous after all, but only at the 1444 start date and only for this one node. The claim under C377 that no vanilla node is a pure conduit was measured on the solver's `b` vector after the epsilon regulariser, which gives the Cape a tiny nonzero supply; before epsilon it is an exact conduit.

### C369 — CONFIRMED

> A local endpoint comparison therefore orients the Cape edge into Malacca.
>
> *MODEL / derivation / depends on C367, C368*

**Method.** Direct construction (`t_model3.py`), using the wealth-rank convention.

**Evidence.** `rank orientation (toward wealth): [('Cape', 'Malacca'), ('Cape', 'Europe')]`; `edge {Malacca,Cape} points into: Malacca`. Exactly as claimed.

**Note.** One wording correction worth making: under this orientation the Cape has `out-degree=2 in-degree=0` and is therefore a **source**, not a sink. Section 3.2's aside "The failure isn't that the Cape becomes a sink" is right to disclaim it but leaves the impression the Cape becomes one.

### C370 — CONFIRMED

> The deeper failure is that rank orientation is monotone.
>
> *MODEL / derivation*

**Method.** Proof plus randomised check. Proof: if edges orient by a node ranking r with u->v only when r(v) > r(u), then r is strictly increasing along any directed path, so no interior node of a path can have r below both its path neighbours.

**Evidence.** `counterexamples found in 20000 random rankings: 0` (`t_model3.py`).

### C371 — CONFIRMED

> Under a monotone orientation no path can dip through a low-value intermediary and rise again.
>
> *MODEL / derivation / depends on C370*

**Method.** The same proof as C370, stated as its contrapositive.

**Evidence.** Same evidence.

### C372 — CONFIRMED

> Malacca → … → Cape → … → Europe requires exactly such a dip and rise.
>
> *MODEL / derivation / depends on C367, C368*

**Method.** Follows from C370 given C367/C368: the Cape is the low-ranked interior node of the corridor.

**Evidence.** `corridor Malacca -> Cape -> Europe realized: False` under rank orientation; realised under the potential.

### C373 — CONFIRMED (conditional)

> Merchants cannot repair a wrong orientation.
>
> *ENGINE / derivation / depends on C374*

**Method.** Derivation from C374.

**Evidence.** Sound inference; premise C374 is separately confirmed.

### C374 — CONFIRMED

> A merchant selects among existing outgoing arrows and cannot reverse one.
>
> *ENGINE / UNSOURCED*

**Method.** The engine's own shipped hint text, in `localisation/hints_l_english.yml`.

**Evidence.** `HINT_TRADESTEERING_TEXT:0 "When you want to steer trade from one Trade Node to another you can send a Merchant to the Trade Node with the order to Transfer Trade Power. This will transfer Trade Value from a Trade Node to the next Trade Node downstream. The amount of trade steered depends on your Trade Power. **You can never steer trade upstream or past your Main Trade City.**"` A merchant chooses among downstream targets; it cannot reverse a link.

**Note.** This is a shipped game file, not a web source, so it is admissible under the audit rules - but it is documentation rather than observed behaviour, so it is UI-strength evidence, not engine-strength.

### C375 — OUT_OF_SCOPE

> Route-awareness must therefore live in the orientation itself.
>
> *DESIGN / derivation / depends on C373*

**Method.** DESIGN.

### C376 — CONFIRMED

> Where `s(n) = c(n) = 0`, the equation reduces to `φ(n)` being the average of its neighbours.
>
> *MODEL / derivation / depends on C007*

**Method.** Proof plus a synthetic test (`t_model2.py`). Proof: row n of `L phi = s - c` is `deg(n) phi(n) - sum_{m~n} phi(m) = s(n) - c(n)`; at `s(n) = c(n) = 0` this is `phi(n) = mean of neighbours` exactly.

**Evidence.** Five-node path with supply at one end and demand at the other: `phi = [2, 1, -5.4e-17, -1, -2]`; for each of the three interior nodes, `== mean of nbrs: True`.

### C377 — CONFIRMED

> A pure conduit therefore lies strictly between its neighbours in `φ`.
>
> *MODEL / derivation / depends on C376*

**Method.** Proof (see C376) plus a synthetic path test, plus one real instance.

**Evidence.** Synthetic: `node 1: neighbours (2.0000, -0.0000) phi=1.0000 strictly between: True`, same for nodes 2 and 3. Real instance: `cape_of_good_hope` has zero owned provinces at 1444.11.11, so `s = c = 0` there exactly (before the epsilon regulariser) - the one vanilla node that is a pure conduit at the start date, and it is precisely the node section 3.2 builds its argument around.

**Note.** With epsilon applied the Cape's supply becomes 1e-6/80 rather than 0, so the automated conduit count in `t_model.py` reports `pure conduits (b==0) tested: 0`. That is an artefact of the regulariser, not a counterexample.

### C378 — CONFIRMED

> A pure conduit can only pass flow through.
>
> *MODEL / derivation / depends on C377*

**Method.** Follows from C377: a node strictly between its neighbours has at least one in-edge and one out-edge, so it is neither source nor sink.

**Evidence.** Same experiment.

### C379 — DEFERRED

> The Cape routes spice westward because Europe draws on the far end.
>
> *OUTCOME / derivation / depends on C378*

**Method.** OUTCOME.

### C380 — CONFIRMED

> Sinks are net consumers automatically.
>
> *MODEL / derivation / depends on C381, C382*

**Method.** Derivation from C381 and C382, both confirmed.

**Evidence.** Valid.

### C381 — CONFIRMED

> A DAG-sink is a local minimum of `φ`.
>
> *MODEL / derivation / depends on C008, C010*

**Method.** Proof: out-degree 0 means every neighbour has phi at least as large, which is the definition of a local minimum.

**Evidence.** Immediate from C008 and C010.

### C382 — CONFIRMED

> By the discrete maximum principle, local minima of `φ` occur only where `c > s`.
>
> *MODEL / derivation / depends on C007*

**Method.** Proof (discrete maximum principle: at a local minimum `deg(n) phi(n) - sum_m phi(m) <= 0`, and that expression is `s(n) - c(n)`, so `s(n) <= c(n)`) plus two exhaustive checks on 1444 data.

**Evidence.** `local minima of phi where s>c (should be 0): 0` and `local maxima of phi where c>s (should be 0): 0` over all 2320 (good, node) pairs; and separately `(good, sink) pairs: 102 | pairs where s >= c: 0`.

### C383 — OUT_OF_SCOPE

> Peripheral sinks are intended, not a defect.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C384 — DEFERRED

> Goods flow to a periphery and are consumed at the end of the line.
>
> *OUTCOME / derivation / depends on C380*

**Method.** OUTCOME.

### C385 — NEEDS_GAME

> Value only arrives where someone holds power at both ends of the link.
>
> *ENGINE / derivation / depends on C102*

**Method.** Derivation from C102, which is NEEDS_GAME.

**Evidence.** See C102.

**Note.** Settled by C102's observation.


---

## §3.3

### C386 — OUT_OF_SCOPE

> Demand is purchasing power.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C387 — CONFIRMED

> Purchasing power is income the game already computes.
>
> *ENGINE / UNSOURCED / depends on C032*

**Method.** The two income components the spec names are engine-computed and separately labelled.

**Evidence.** `TAX_INCOME:0 "Tax Income"`, `LEDGER_TAX:0 "Tax"`, `LEDGER_PRODUCTION:0 "Production"`, `PRODUCTION_EFFICIENCY:0 "Production Efficiency"`, and the income category keys `INCOMETAX`/`INCOMETRADE`/`INCOMEGOLD`/`INCOMEMANUFAC` in `localisation/core_l_english.yml`. Both quantities exist as engine outputs.

**Note.** But see C049: the income category list also shows Gold as a *separate* category, which is what refutes the spec's gold handling.

### C388 — CONFIRMED

> Using income captures return flows for free.
>
> *MODEL / derivation / depends on C032, C360*

**Method.** Derivation from C032 and the design goal C360.

**Evidence.** Valid as an inference.

### C389 — PARTIAL

> A sugar island has negligible development but large production income.
>
> *ENGINE / UNSOURCED*

**Method.** Checked on the 1444 dataset rather than asserted; and checked the arithmetic of the claim.

**Evidence.** Sugar is produced in 34 owned provinces at 1444.11.11 with `base_price = 3`. Production income scales as `0.2 x base_production x price`, so a 1-development sugar province yields 0.6 ducats/yr versus 0.2 x 1 x 2.5 = 0.5 for grain - a 20% premium, not a large one. The claim's force comes from *high goods-produced* islands, not from the price alone.

**What is actually true.** "Negligible development but large production income" overstates the gap at vanilla prices: sugar (3), cocoa (4), coffee (3) are 1.2x-1.6x grain (2.5), not multiples. The largest price ratios are cloves (8) and coal (10), neither of which is a Caribbean sugar island.

**Spec text that must change.** "a sugar island has negligible development but large production income, so it becomes a genuine consumer of cloth and tools" (spec.md, section 3.3)

**Blast radius.** C390, C310. The mechanism survives; the magnitude should be recomputed against real prices and the correct autonomy floor (C037/C038).

### C390 — DEFERRED

> Such an island therefore becomes a genuine consumer of cloth and tools.
>
> *OUTCOME / derivation / depends on C032, C389*

**Method.** OUTCOME.

### C391 — CONFIRMED

> Using income introduces no colonial-nation dependency and no timeline restriction.
>
> *MODEL / derivation / depends on C032*

**Method.** Derivation: `wealth` as defined reads only `tax_income` and `production_income`, neither of which references a colonial-nation relation or a date.

**Evidence.** Valid.

### C392 — OUT_OF_SCOPE

> Income was chosen for responsiveness rather than stability.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C393 — CONFIRMED (three of four premises)

> Income is not a slow quantity.
>
> *ENGINE / derivation / depends on C394, C395, C396, C397*

**Method.** Derivation from C394-C397; C395, C396 and C397 are confirmed from files, C394 is PARTIAL.

**Evidence.** See each.

### C394 — PARTIAL

> Autonomy drift is monthly.
>
> *ENGINE / UNSOURCED*

**Method.** Searched `common/defines.lua` and the modifier namespace for a monthly autonomy drift term.

**Evidence.** The engine has a country modifier `global_autonomy` (eu4.exe string table 0x021ae04c) and `average_global_autonomy` / `reverse_average_global_autonomy`; a shipped tooltip confirms the monthly cadence: `mechanic_enables_statesman_autonomy_reduction_yes:0 "§YStatesman§! Advisor will now provide §G-0.01§! **Monthly** Autonomy Reduction per Level."` The only autonomy define with a period is `AUTONOMY_CHANGE_DURATION = 10950,  -- about 30 years`, which is the cooldown on manual changes, not the drift.

**What is actually true.** Monthly autonomy *reduction* from modifiers is confirmed. Whether autonomy also drifts monthly toward its floor absent any modifier is not settled by any file.

**Note.** Settling observation: take a province at 40% autonomy with no autonomy modifiers and read its autonomy monthly for a year.

### C395 — CONFIRMED

> Occupation halves goods produced for the duration of a war.
>
> *ENGINE / UNSOURCED*

**Method.** Read `common/static_modifiers/00_static_modifiers.txt:433`.

**Evidence.** `occupied = { local_tax_modifier = -0.5  trade_goods_size_modifier = -0.5  province_trade_power_modifier = -0.5  local_manpower_modifier = -0.5  local_sailors_modifier = -0.5  local_institution_spread = -0.1  local_monthly_devastation = 0.2 }` - goods produced is halved.

**Note.** Precision note: the modifier applies while the province is *occupied*, which is a province state, not "for the duration of a war". A war with no occupation moves nothing here; an occupation surviving into peace keeps moving it. `under_siege` separately applies `trade_goods_size_modifier = -0.25`.

### C396 — CONFIRMED

> Devastation and sieges bite within months.
>
> *ENGINE / UNSOURCED*

**Method.** Read the two relevant static modifier blocks.

**Evidence.** `under_siege = { trade_goods_size_modifier = -0.25  province_trade_power_modifier = -0.25  local_institution_spread = -0.1  local_monthly_devastation = 0.1 }` and `devastation = { trade_goods_size_modifier = -2  supply_limit_modifier = -0.5  local_development_cost = 0.2  local_manpower_modifier = -2.0 ... }`. Devastation accrues at 0.1-0.2 per month under siege or occupation, so a fully devastated province is months away, not years.

### C397 — CONFIRMED

> Ming's mandate swings enormously over years.
>
> *ENGINE / UNSOURCED*

**Method.** Read the Mandate static modifier.

**Evidence.** `lost_mandate_of_heaven = { discipline = -0.1  stability_cost_modifier = 0.5  global_unrest = 10  **global_trade_goods_size_modifier = -0.5**  fire_damage_received = 0.5  shock_damage_received = 0.5  reduced_liberty_desire = -50  legitimacy = -1  mercenary_manpower = -0.5  global_manpower_modifier = -0.5 }`. Also `meritocracy` and `low_meritocracy` scaled modifier blocks (lines 1041, 1048) and `imperial_mandate = -1` / `-0.1` entries.

### C398 — OUT_OF_SCOPE

> The resulting volatility is deliberate.
>
> *DESIGN / stipulated / depends on C392*

**Method.** DESIGN.

### C399 — OUT_OF_SCOPE

> A besieged province genuinely buys less, so the volatility is economics rather than noise.
>
> *DESIGN / stipulated / depends on C396*

**Method.** DESIGN.

### C400 — OUT_OF_SCOPE

> A trade map that ignored a decade-long war would fail Goal 1.
>
> *DESIGN / derivation / depends on C353*

**Method.** DESIGN.

### C401 — DEFERRED

> The resulting map is legible though not unchanging.
>
> *OUTCOME / UNSOURCED / depends on C398*

**Method.** OUTCOME.

### C402 — OUT_OF_SCOPE

> Trade income is excluded from `wealth` for circularity, not speed.
>
> *DESIGN / stipulated / depends on C039*

**Method.** DESIGN.

### C403 — CONFIRMED

> Including trade income would close a demand → orientation → flow → demand loop.
>
> *MODEL / derivation / depends on C032, C039*

**Method.** Proof: trade income at n is a function of the realised flows, which are a function of the orientation, which is a function of phi, which is a function of c, which would be a function of trade income. That is a closed cycle in the dependency graph.

**Evidence.** Directly visible in the solver's call graph: `build_sc` -> `solve_phi` -> `orient` -> realised flow. Feeding realised flow back into `wealth` closes it.

### C404 — CONFIRMED

> That loop would make the graph respond to merchants' decisions rather than to the world.
>
> *MODEL / derivation / depends on C403*

**Method.** Derivation from C403.

**Evidence.** Valid.

### C405 — CONFIRMED

> The loop still closes the long way: trade income funds development, which raises tax and production income.
>
> *ENGINE / UNSOURCED*

**Method.** Development bought with any ducats raises `base_tax` and `base_production`, which are exactly the two inputs to `wealth`.

**Evidence.** `common/defines.lua`: `EMBRACE_INSTITUTION_COST = 2.5, -- 2.5 per development (autonomy modified)`; development is a purchasable province attribute and `history/provinces` records `base_tax`/`base_production` as the same fields the solver reads. The long loop is real but runs through the treasury and monarch points, not through the monthly solve.

### C406 — CONFIRMED

> Node boundaries are an authoring artifact.
>
> *ENGINE / UNSOURCED*

**Method.** Measured the actual variation in node size from `common/tradenodes/00_tradenodes.txt` - an authoring artifact is exactly what unexplained variation of this size is.

**Evidence.** Land-province counts per node range from **19** (`cape_of_good_hope`) to **77** (`girin`), a 4.05x spread, with no structural rule generating it. Full distribution in `scratchpad/v/members.py` output.

### C407 — REFUTED

> Some nodes hold forty provinces and some hold four.
>
> *ENGINE / file value*

**Method.** Counted `members` per node in `common/tradenodes/00_tradenodes.txt`, then separated land from sea using `sea_starts` (668) and `lakes` (125) from `map/default.map`, and cross-checked against `history/provinces` file existence. Script: `scratchpad/v/members.py`.

**Evidence.** **Minimum 19 land provinces** (`cape_of_good_hope`, 20 members), **maximum 77** (`girin`). Next smallest: `patagonia` 20, `chengdu` 20, `white_sea` 21, `valencia` 21, `kazan` 22. `nodes with <=4 land+hist provinces: []` - **no node holds four provinces, or anything close to four**. Nodes near forty do exist (13 of them, including `burma` 40, `deccan` 40, `novgorod` 40, `ragusa` 40).

**What is actually true.** Node sizes run from 19 to 77 land provinces - a 4x spread, not a 10x one. The "forty versus four" contrast overstates the disparity by an order of magnitude.

**Spec text that must change.** "**Per province, because node boundaries are an authoring artifact.** Some nodes hold forty provinces and some hold four." (spec.md, section 3.3)

**Blast radius.** C408, C409, C410, C631 and the section 3.15 "Node-level alpha" rejection all rest on the size disparity. The *argument survives* - a 4x spread under a superlinear exponent is still a large distortion - but every quantitative statement of it must be restated. C411 is separately correct (see its entry).

### C408 — CONFIRMED

> Raising a node's aggregate wealth to a power rewards node size.
>
> *MODEL / derivation / depends on C033*

**Method.** Proof: for a node of k provinces each of wealth w, node-aggregate demand is `(k w)^a = k^a w^a` while per-province demand is `k w^a`. The ratio is `k^(a-1)`, strictly increasing in k for `a > 1`.

**Evidence.** At a = 1.5 and the real spread, a 77-province node beats a 19-province node of the same total wealth by `(77/19)^0.5 = 2.01x` under node-level alpha, purely from being sliced coarser.

### C409 — CONFIRMED

> Under node-level α, luxuries would drain toward whichever node the map authors sliced finest.
>
> *MODEL / derivation / depends on C408*

**Method.** Derivation from C408; the direction of the distortion is exactly as claimed (coarser slicing wins).

**Evidence.** See the 2.01x figure under C408, computed on the real 19-to-77 spread rather than the spec's 4-to-40.

### C410 — DEFERRED

> Under node-level α, Nippon would out-consume Paris on province count.
>
> *OUTCOME / derivation / depends on C409, C411*

**Method.** OUTCOME.

### C411 — CONFIRMED

> The Nippon node contains more provinces than the Paris node.
>
> *ENGINE / file value*

**Method.** Located Paris (province 183, `history/provinces/183 - Ile-de-France.txt`, `PROV183:0 "Paris"`) in `common/tradenodes/00_tradenodes.txt` and compared member counts.

**Evidence.** Paris is a member of the **`champagne`** node (there is no node named `paris` - `any node literally named paris? []`). `champagne`: 33 members, 33 land. `nippon`: 69 members, 68 land. 68 > 33, so the claim's substance holds by a factor of 2.06.

**Note.** Wording only: the node is `champagne`, not "the Paris node". Worth fixing so the reader can find it in the file.

### C412 — CONFIRMED

> With the exponent inside the sum, superlinear demand concentrates where individual provinces are rich.
>
> *MODEL / derivation / depends on C033*

**Method.** Proof: with the exponent inside the sum, `sum_p w_p^a` is Schur-convex for `a > 1`, so for fixed node total it is maximised by concentrating wealth in few provinces.

**Evidence.** Concretely at a = 1.5: one province of wealth 10 gives 31.6; ten provinces of wealth 1 give 10.0.

### C413 — CONFIRMED

> At α = 1 the per-province and node-aggregate forms coincide exactly.
>
> *MODEL / derivation / depends on C033*

**Method.** Proof: at a = 1, `sum_p w_p^1 = sum_p w_p = (node aggregate)^1`. The two forms are literally the same expression.

**Evidence.** Identity, no residual.

### C414 — CONFIRMED

> That coincidence is what preserves the §1.6 identity.
>
> *MODEL / derivation / depends on C063, C413*

**Method.** Derivation from C413 and C063; the C063 proof uses exactly this coincidence.

**Evidence.** The C063 proof requires every good's `c` vector to be identical at a=1, which requires the per-province and node-aggregate forms to agree. Measured residual `1.959e-15`.


---

## §3.4

### C415 — PARTIAL

> Production efficiency does not create more of a good; it means the owner extracts more ducats from the same quantity.
>
> *ENGINE / UNSOURCED*

**Method.** The modifier namespace separates the two, but the semantic claim about what production efficiency does is engine behaviour.

**Evidence.** `production_efficiency` and `trade_goods_size_modifier` are distinct modifier keys and no static modifier applies one in place of the other. `PRODUCTION_EFFICIENCY:0 "Production Efficiency"` and `TRADE_GOODS_SIZE:0 "Local Goods Produced"` are separate displayed quantities.

**Note.** Settling observation: take Trade ideas' production efficiency bonus and check whether a province's "Goods produced" figure changes. Same trace as C025.

### C416 — OUT_OF_SCOPE

> Production efficiency is therefore a fact about purchasing power and belongs in demand.
>
> *DESIGN / derivation / depends on C415*

**Method.** DESIGN.

### C417 — CONFIRMED

> Letting production efficiency into supply would imply a province ships more to the world market because its owner picked Trade ideas.
>
> *MODEL / derivation / depends on C023*

**Method.** Derivation from C023: `s` is a share of world `goods_produced`, so any owner-dependent multiplier on the numerator would make a province's world share depend on its owner's idea groups.

**Evidence.** Valid.

### C418 — OUT_OF_SCOPE

> That would be incoherent with the model's thesis.
>
> *DESIGN / derivation / depends on C419*

**Method.** DESIGN.

### C419 — OUT_OF_SCOPE

> The model's thesis is that where a good comes from is what makes its trade its own.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C420 — OUT_OF_SCOPE

> This is also why the aggregate supply term uses trade value rather than production income.
>
> *DESIGN / derivation / depends on C416*

**Method.** DESIGN.

### C421 — CONFIRMED

> Trade value and production income are different quantities.
>
> *ENGINE / UNSOURCED*

**Method.** Separate engine quantities with separate display strings and separate modifier namespaces.

**Evidence.** `TRADE_VALUE:0 "Trade Value"` and `TRADE_VALUE_MODIFIER:0 "Trade Value Modifier"` versus `LEDGER_PRODUCTION:0 "Production"` and `PRODUCTION_EFFICIENCY:0 "Production Efficiency"`; the province map tooltip prints both at once - `TRADE_GOODS_ONMAP:0 "$GOODS$ \nGoods produced: $PRODUCED$ \nTrade value: $VALUE$ \nTrade power: $TRADE$"`.

### C422 — NEEDS_GAME

> A province's trade value is unaffected by production efficiency or local autonomy.
>
> *ENGINE / UNSOURCED*

**Method.** Same question as C025, from the trade-value side.

**Evidence.** `AFFECTED_BY_AUTONOMY:0 "Reduced by $AMT$ due to the local autonomy in the province."` exists but is not tied to a named field on disk.

**Note.** Settling observation: read a province's "Trade value" line in the map tooltip before and after raising its local autonomy. If unchanged, the claim holds. Setup: any save. This single observation settles C025, C415, C422 and C423 together, and it is the highest-leverage non-debugger check in the whole list.

### C423 — NEEDS_GAME

> Production income is defined by production efficiency and local autonomy.
>
> *ENGINE / UNSOURCED*

**Method.** Same observation as C422.

**Evidence.** `AFFECTED_BY_AUTONOMY` and `production_efficiency` both exist; which one multiplies the production income field is not on disk.

**Note.** Same observation as C422.

### C424 — CONFIRMED

> Substituting production income would break the `Φ ≡ φ₀` identity on real data.
>
> *MODEL / derivation / depends on C063, C422, C423*

**Method.** Measured directly: rebuilt phi0's supply vector with a realistic owner-dependent factor `(1 + production_efficiency) x (1 - autonomy)` applied per province, then compared against Phi at alpha = 1 (`t_model4.py`).

**Evidence.** `rel.residual with production-income supply: 1.512e+00` against `1.959e-15` with trade-value supply - fifteen orders of magnitude worse. Orientation agreement collapses from **159/159 to 68/159**. The identity does not degrade gracefully; it is destroyed.

### C425 — CONFIRMED

> That break would have nothing to do with the solver.
>
> *MODEL / derivation / depends on C424*

**Method.** Derivation from C424: the break is in the input construction, not in the linear solve.

**Evidence.** Valid.

### C426 — DEFERRED

> It would cost about a day of debugging a correct pipeline.
>
> *OUTCOME / UNSOURCED / depends on C424*

**Method.** OUTCOME.


---

## §3.5

### C427 — CONFIRMED

> Anchoring α at 2 ducats rather than the price median means a good's concentration moves only when its own price moves.
>
> *MODEL / derivation / depends on C040, C041*

**Method.** Proof: `alpha(g) = clamp((price(g)/P0)^k, ...)` has no argument other than `price(g)` and the constants, so `d alpha(g) / d price(h) = 0` for `h != g`.

**Evidence.** Immediate from the formula.

### C428 — CONFIRMED

> Under absolute anchoring, `k` is a pure sensitivity knob that does not shift the neutral point.
>
> *MODEL / derivation / depends on C040*

**Method.** Proof: `(price/P0)^k = 1` iff `price = P0`, independent of k. So k rotates the curve about a neutral point fixed at P0.

**Evidence.** Immediate.

### C429 — CONFIRMED

> Under a median anchor a good could concentrate because an unrelated commodity got expensive.
>
> *MODEL / derivation / depends on C040*

**Method.** Proof: with `P0 = median(prices)`, `alpha(g)` depends on every other good's price through the median.

**Evidence.** Immediate.

### C430 — OUT_OF_SCOPE

> That would be noise dressed as economics.
>
> *DESIGN / stipulated / depends on C429*

**Method.** DESIGN.

### C431 — DEFERRED

> α < 1 is a crash-reachable state, not a starting condition.
>
> *OUTCOME / derivation / depends on C432*

**Method.** OUTCOME.

**Evidence.** Settled from files anyway: at base prices the minimum tradeable price is exactly 2.0, so alpha < 1 is unreachable at start; 13 of 30 goods can be pushed below 2.0 by a single vanilla `change_price` event. See C432 and C435.

### C432 — CONFIRMED (and stronger than stated)

> At vanilla base prices essentially nothing sits below the 2.0 anchor.
>
> *ENGINE / file value / depends on C041*

**Method.** Read every `base_price` in `common/prices/00_prices.txt`.

**Evidence.** Excluding gold (`base_price = 0`, `goldtype = yes`) and the `unknown` placeholder (`base_price = 0`), the full price list is: **2.0** for fur, naval_supplies, slaves, tea, tropical_wood, livestock; 2.5 for grain, wine, wool, fish, incense; 3.0 for cloth, salt, copper, iron, chinaware, spices, coffee, cotton, sugar, tobacco, glass; 3.5 paper; 4.0 ivory, cocoa, silk, dyes, gems; 8.0 cloves; 10.0 coal. **The minimum is exactly 2.0.** Nothing sits below the anchor, and six goods sit exactly on it (alpha = 1 exactly).

### C433 — REFUTED

> Grain's base price is near 1.25.
>
> *ENGINE / file value*

**Method.** Read `common/prices/00_prices.txt`.

**Evidence.** `grain = { base_price = 2.5 }`. Not 1.25 - exactly **double** the stated figure.

**What is actually true.** Grain's base price is 2.5, which is 25% *above* the 2.0 anchor, not 38% below it. At k = 1 this gives alpha = 1.25, i.e. grain is mildly *superlinear* at base price, not sublinear.

**Spec text that must change.** "At vanilla base prices essentially nothing sits below the 2.0 anchor - grain lands near 1.25 and livestock near 1.00 - so the sublinear regime is entered mainly when a price event pushes a good beneath the anchor." (spec.md, section 3.5)

**Blast radius.** C434 (the other half of the same sentence, separately refuted), C435, C437, C438, C581, C582, C583, C635. The *conclusion* C432 is unaffected and is in fact strengthened, but the two supporting numbers are both wrong and both wrong in the same direction - they were apparently read as `price/2` rather than as price.

### C434 — REFUTED

> Livestock's base price is near 1.00.
>
> *ENGINE / file value*

**Method.** Read `common/prices/00_prices.txt`.

**Evidence.** `livestock = { base_price = 2 }`. Not 1.00 - exactly **double**.

**What is actually true.** Livestock's base price is 2.0, exactly on the anchor, giving alpha = 1 exactly rather than alpha < 1.

**Spec text that must change.** "grain lands near 1.25 and livestock near 1.00" (spec.md, section 3.5)

**Blast radius.** Same as C433. Note the pattern: both quoted figures are exactly half the true base price, which suggests the source divided by P0 = 2.0 and then reported the ratio as a price.

### C435 — CONFIRMED

> The sublinear regime is entered mainly when a price event pushes a good beneath the anchor.
>
> *OUTCOME / derivation / depends on C432, C046*

**Method.** Computed the reachable price floor for every good by combining each base price with the most negative `change_price` event that targets it (108 effects parsed from `events/`, `decisions/`, `missions/`, `common/`).

**Evidence.** 13 of 30 goods can be pushed below the 2.0 anchor by a single event: glass 3.0 -> 1.05 (-0.65), grain 2.5 -> 0.625 (-0.75), wine 2.5 -> 0.625 (-0.75), slaves 2.0 -> 1.2 (-0.4), copper 3.0 -> 1.5 (-0.5), chinaware 3.0 -> 1.5 (-0.5), livestock 2.0 -> 1.5 (-0.25), paper 3.5 -> 1.75 (-0.5), spices 3.0 -> 1.8 (-0.4), coffee 3.0 -> 1.8 (-0.4), fish 2.5 -> 1.875, incense 2.5 -> 1.875. **11 goods have no negative price event at all** and can therefore never go sublinear: cloves, cocoa, cotton, fur, ivory, naval_supplies, salt, sugar, tea, tobacco, tropical_wood.

**Note.** This is the direct answer to the spec's own open questions C437, C581 and C582, and it should be written into section 3.13: the sublinear regime is reachable, for 13 of 30 goods, only through named price-crash events; for 11 goods it is unreachable in vanilla at any k.

### C436 — CONFIRMED

> Without a sublinear regime, a price crash could only fail to concentrate a market, never actively spread it.
>
> *MODEL / derivation / depends on C045*

**Method.** Proof: with alpha clamped at 1 from below, the mapping `w -> w^alpha` is at best linear, so demand can never be *more* dispersed than economic size. Only alpha < 1 disperses it further.

**Evidence.** Immediate from C044/C045.

### C437 — OUT_OF_SCOPE

> Whether the sublinear regime engages often enough to earn its keep is an open question.
>
> *DESIGN / stipulated / depends on C435*

**Method.** DESIGN (an open question).

**Note.** Now largely answerable from files - see C435.

### C438 — CONFIRMED

> If it never engages, either `P₀` is set too low or the regime is doing no work.
>
> *MODEL / derivation / depends on C437*

**Method.** Derivation; the disjunction is exhaustive given C435's measurement.

**Evidence.** Valid, and C435 supplies the data to decide it.

### C439 — OUT_OF_SCOPE

> α is deliberately mild.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C440 — OUT_OF_SCOPE

> Production geography is what differentiates goods.
>
> *DESIGN / stipulated / depends on C419*

**Method.** DESIGN.

### C441 — OUT_OF_SCOPE

> α expresses only how concentrated a market is.
>
> *DESIGN / stipulated / depends on C040*

**Method.** DESIGN.

### C442 — CONFIRMED

> A concentration mechanism strong enough to reshape orientation would let price fight geography for control of the graph.
>
> *MODEL / derivation / depends on C439, C440*

**Method.** Swept a uniform alpha across the real 1444 data and counted orientation changes against the alpha = 1 reference (`t_model4.py`).

**Evidence.** Edges agreeing with the alpha = 1 orientation: alpha=0.5 -> 118/159; 0.8 -> 137/159; **1.0 -> 159/159**; 1.2 -> 126/159; 1.5 -> 99/159; 2.0 -> 80/159; 3.0 -> 66/159. At alpha = 3 more than half the map's edges have reversed relative to alpha = 1. Concentration strong enough to reshape orientation is not hypothetical - it is what a large `k` produces, which is exactly why the spec keeps alpha mild.


---

## §3.6

### C443 — OUT_OF_SCOPE

> A margin on orientation is a correctness bug, not a tuning knob.
>
> *DESIGN / stipulated / depends on C445*

**Method.** DESIGN.

### C444 — CONFIRMED

> Holding an edge against the current gradient makes the emitted orientation a splice of gradients from fields solved at different times.
>
> *MODEL / derivation / depends on C022*

**Method.** Definitional: holding an edge against the current gradient means its orientation was set by an earlier field.

**Evidence.** Immediate.

### C445 — CONFIRMED

> A splice of two acyclic orientations need not be acyclic.
>
> *MODEL / numerical test / depends on C444, C446*

**Method.** Reproduced constructively in `t_model3.py`, and strengthened: the margin turns an **acyclic** prior into a cycle, which is the version that actually matters.

**Evidence.** Prior orientation `[('A','B'), ('B','C'), ('A','C')]` - acyclic (A -> B -> C, A -> C). New field `phi = {A: 0, B: 0.0006, C: 0.0012}`, `tol = 1e-3`. Differences: `A-B = 0.0006` and `B-C = 0.0006` are inside the margin and hold; `A-C = 0.0012` exceeds it and follows the gradient to `C -> A`. Result `[('A','B'), ('B','C'), ('C','A')]` - **cyclic: True**. The pure-gradient orientation of the same field is `[('B','A'), ('C','B'), ('C','A')]` - **cyclic: False**.

### C446 — CONFIRMED

> With tol = 1e-3 and `φ = {0, 0.0006, 0.0012}`, tolerance-based tie-breaking produced A→B→C→A.
>
> *MODEL / numerical test*

**Method.** The C445 experiment, with exactly the spec's stated tolerance and phi values.

**Evidence.** `|phi differences|: A-B=0.0006  B-C=0.0006  A-C=0.0012  (tol=0.001)` -> `A->B->C->A`. Reproduced exactly.

### C447 — REFUTED

> The `00_tradenodes.txt` format cannot represent a cycle.
>
> *ENGINE / UNSOURCED*

**Method.** Examined the grammar of `common/tradenodes/00_tradenodes.txt` directly. Each node declares zero or more `outgoing={ name="<node>" ... }` blocks; there is no uniqueness, ordering, or reachability constraint expressible in the format itself, and no node-level key that forbids a return link.

**Evidence.** Existing structure: `zambezi -> outgoing name="zanzibar"` and `zanzibar` declares its own `outgoing` blocks. Nothing in the file prevents adding `outgoing={ name="zambezi" ... }` to `zanzibar`; the parser in `scratchpad/v/pdx.py` accepts such a file and `graph.py` reports the resulting cycle. The vanilla file happens to contain none (`bidirectional pairs (both directions declared): 0`, `vanilla graph cycles found: 0`), but that is content, not grammar.

**What is actually true.** The *format* can represent a cycle perfectly well - it is a list of named directed links with no acyclicity constraint. What may be true, and is a different claim, is that the **engine** rejects or misbehaves on a cyclic node file. That is C234-adjacent and is NEEDS_GAME.

**Spec text that must change.** "A cycle - which the file format cannot represent and the whole design depends on being impossible." (spec.md, section 3.6)

**Blast radius.** C448 ("the whole design depends on cycles being impossible") now rests on an unverified engine property rather than on a format property, which raises its priority. Settling observation: hand-author a two-node cycle in `common/tradenodes/00_tradenodes.txt`, load a fresh game, and read `logs/error.log` and the trade map. Setup: one file edit, no save, no debugger.

### C448 — OUT_OF_SCOPE

> The whole design depends on cycles being impossible.
>
> *DESIGN / derivation / depends on C447*

**Method.** DESIGN.

**Note.** Its stated ground is refuted - see C447.

### C449 — OUT_OF_SCOPE

> Nothing needs to stop orientation churn.
>
> *DESIGN / stipulated / depends on C451, C452*

**Method.** DESIGN.

### C450 — CONFIRMED

> A link that alternates has near-zero Δφ.
>
> *MODEL / derivation / depends on C008*

**Method.** Proof: an edge alternates between solves only if `phi(u) - phi(v)` changes sign, which requires it to pass through zero.

**Evidence.** Immediate from C008.

### C451 — DEFERRED

> Such a link carries near-nothing in either direction.
>
> *OUTCOME / derivation / depends on C450*

**Method.** OUTCOME.

### C452 — NEEDS_GAME

> Merchant assignments are to links, so they survive flips untouched.
>
> *ENGINE / derivation / depends on C076*

**Method.** Derivation from C076, which is NEEDS_GAME.

**Evidence.** See C076.

**Note.** 2.7 probe 5.

### C453 — OUT_OF_SCOPE

> ε is required, and is a different thing from hysteresis.
>
> *DESIGN / stipulated / depends on C029*

**Method.** DESIGN.

### C454 — CONFIRMED

> A dead branch is harmonic with zero flux, so `φ` is mathematically constant along it.
>
> *MODEL / derivation / depends on C007*

**Method.** Proof: on a branch where every node has `s = c = 0` and which attaches to the rest of the graph at one node, the flux through the attaching edge must be zero by conservation, so phi is constant along the branch. Verified in `t_model2.py`.

**Evidence.** Dead tail (nodes 4-7) values across six solves are all within 1.4e-16 of zero, i.e. constant to machine precision - `tail=[-2.117e-17, -5.324e-17, -8.269e-17, -8.275e-17]` on seed 0.

### C455 — CONFIRMED

> In floating point, `φ` along a dead branch differs by numerical residual.
>
> *MODEL / numerical test / depends on C454*

**Method.** Six mathematically identical solves under permuted accumulation order (`t_model2.py`).

**Evidence.** Every solve returned a different residual pattern on the dead tail, e.g. `phi[5]-phi[6]` = `+2.945e-17, -2.534e-17, -2.306e-17, -3.379e-17, +1.573e-17, +5.965e-17`.

### C456 — PARTIAL

> Four mathematically identical solves of one dead branch produced 0.37000000000000000, 0.36999999999999988, and −0.86999999999999988.
>
> *MODEL / numerical test*

**Method.** Could not reproduce the spec's specific figures (its solver setup is not recorded), but reproduced the phenomenon; and checked the reported numbers for internal consistency.

**Evidence.** The reported values are `0.37000000000000000`, `0.36999999999999988`, `-0.86999999999999988` - three values for four solves, and the third differs from the first by **1.24**, which is 16 orders of magnitude larger than a double-precision residual on a value of order 0.37. A spread of 1.24 across "mathematically identical solves" cannot be floating-point noise; it is the signature of a **different pin / reference node** in a disconnected component, which shifts the whole branch by a constant.

**What is actually true.** The first two values differ by 1.2e-16 and are genuine floating-point residual. The third is not: it is a constant offset, which by itself does **not** change orientation within the branch (every phi on the branch shifts equally). So the third datum does not support the conclusion the passage draws from it.

**Spec text that must change.** "Tested across four mathematically identical solves of one dead branch: `0.37000000000000000`, `0.36999999999999988`, `-0.86999999999999988`, with one edge orienting `<-` twice and `->` once on Delta of +/-1e-16." (spec.md, section 3.6)

**Blast radius.** C457, C458, C459. **The conclusion survives** - the underlying phenomenon is real and I reproduced it independently (C455, C180) - but the reported evidence is partly mis-attributed, and a reader checking the arithmetic will find the same discrepancy. Restate with the residual-scale values only, or explain the constant offset as a separate pin effect.

### C457 — CONFIRMED (phenomenon)

> In those solves one edge oriented ← twice and → once on Δ of ±1e-16.
>
> *MODEL / numerical test / depends on C456*

**Method.** Reproduced independently in `t_model2.py`: the sign of a dead-branch edge varies across mathematically identical solves.

**Evidence.** `sign of the 5-6 edge across solves: [1.0, -1.0, -1.0, -1.0, 1.0, 1.0] | all identical: False` - three each way in six solves, on differences of order 1e-17.

**Note.** The phenomenon is confirmed at a stronger sample size than the spec reports. See C456 for the arithmetic problem with the spec's specific figures.

### C458 — PARTIAL

> Exact ties occur in some runs and not others.
>
> *MODEL / numerical test / depends on C456*

**Method.** Reproduced the variation but not exact ties.

**Evidence.** `exact ties: 0` in six permuted solves. Differences were of order 1e-17 but never exactly zero.

**What is actually true.** Orientation varies unpredictably across runs - confirmed. That *exact* ties occur in some runs is not reproduced here and is setup-dependent (it depends on whether the pin makes the branch's residual identically zero, which the mean-zero pin used here does not).

**Note.** Nothing turns on it: C459's conclusion follows from near-ties as well as exact ties, and eps is required either way.

### C459 — CONFIRMED

> The tie-break therefore fires unpredictably and orientation varies by machine.
>
> *MODEL / derivation / depends on C458*

**Method.** Derivation from C455/C457, both reproduced.

**Evidence.** Six solves, three orientations each way, on the same mathematical input.

### C460 — CONFIRMED

> ε is field-level.
>
> *MODEL / stipulated / depends on C029*

**Method.** Stipulation; implemented as a modification of `s` before the solve, not of the orientation after it.

**Evidence.** `S[live] = (1 - eps) * S[live] + eps / N` in `build_sc()`.

### C461 — OUT_OF_SCOPE

> Field-level is the only kind of regularizer the model permits.
>
> *DESIGN / stipulated / depends on C460*

**Method.** DESIGN.

### C462 — PARTIAL

> ε preserves the §1.6 identity exactly.
>
> *MODEL / derivation / depends on C029, C063*

**Method.** Measured the identity residual as a function of eps, under both readings of what eps applies to (`t_model.py` and `t_model2.py`).

**Evidence.** **Reading the spec literally** (eps applied to the per-good supplies in section 1.2; phi0's supply defined in section 1.6 without eps): `eps=0 -> rel.residual 1.959e-15`; `eps=1e-6 -> 1.151e-05`; `eps=1e-3 -> 1.157e-02` (and orientation now disagrees on 1 of 159 edges); `eps=1e-1 -> 1.140e+00` (38 edges disagree). The residual is first-order in eps, not zero. **Applying the same regulariser to phi0's supply as well**: `eps=0 -> 1.959e-15`, `eps=1e-6 -> 1.643e-15`, `eps=1e-3 -> 2.033e-15`, `eps=1e-1 -> 3.505e-15`, and `k = 3662.40000000` unchanged at every eps. Exact.

**What is actually true.** eps preserves the identity exactly **only if the phi0 diagnostic applies the same regulariser to its own supply vector**. The spec defines phi0's supply (section 1.6, C064/C065) as the raw node share of world trade value, with no eps. Implemented as written, the section 2.8 validation row `Phi = phi0 at alpha = 1` fails at 1.15e-5 relative - small, but far above the 1e-14 tolerance the rest of section 2.8 works to, and it would be diagnosed as a solver bug.

**Spec text that must change.** "eps is field-level - the only kind the model permits - and it preserves the section 1.6 identity exactly." (spec.md, section 3.6). The fix is in section 1.6: phi0's supply must read `(1 - eps) x (node share of world trade value) + eps/N`.

**Blast radius.** C321 and the section 2.8 `Phi = phi0 at alpha = 1` validation row; C063 (the proof is fine, the instantiation is not); C584; C643.


---

## §3.7

### C463 — NEEDS_GAME

> Vanilla counts effective trade power only for countries which collect or transfer downstream.
>
> *ENGINE / UNSOURCED*

**Method.** No file states EU4's effective-trade-power eligibility rule. Searched defines, static modifiers, the .gui files and the string table.

**Evidence.** The engine exposes the *result* (`TN_TRADE_POWER` per country in the node window, `TRADE_EMBARGO_POWER_SHARE:0 "$NAME$ share of power: $VAL$%"`) but not the rule that decides whose power counts.

**Note.** Settling observation: in one node, compare the node's total trade power figure against the sum of the per-country provincial powers, for a node containing a country whose trade capital is strictly upstream. Setup: any save; the node window prints both numbers. No debugger needed. This one observation settles C463, C464, C465 and C473 together.

### C464 — NEEDS_GAME

> Vanilla does not count countries whose trade capital is upstream.
>
> *ENGINE / UNSOURCED*

**Method.** Same as C463.

**Evidence.** See C463.

**Note.** Same observation as C463.

### C465 — NEEDS_GAME

> Power in a node not upstream of anywhere you collect is inert — neither retaining nor transferring.
>
> *ENGINE / UNSOURCED / depends on C463, C464*

**Method.** Same as C463.

**Evidence.** See C463.

**Note.** Same observation as C463.

### C466 — CONFIRMED

> Under a per-good model, "downstream" is itself per good.
>
> *MODEL / derivation / depends on C005*

**Method.** Derivation from C005: if each good has its own orientation, reachability is per good by definition.

**Evidence.** Measured: on 1444 data the reachability count for an ordered node pair ranges 0 to 23 out of 29 goods (`t_model3.py`), so "downstream" is genuinely good-dependent and never all-or-nothing.

### C467 — CONFIRMED

> At a node where your home is downstream for cloth and upstream for spice, your power counts for one and not the other.
>
> *MODEL / derivation / depends on C089, C466*

**Method.** Derivation from C089 and C466, instantiated on real data.

**Evidence.** 6245 of 6320 ordered node pairs are connected by at least one good and none is connected by all 29 - so the mixed case the claim describes is the *typical* case, not an edge case.

### C468 — DEFERRED

> Per-good eligibility returns true for some goods at every node, so no nation is ever globally inert.
>
> *OUTCOME / derivation / depends on C089*

**Method.** OUTCOME.

**Evidence.** Supporting measurement: every node reaches at least one other node under at least one good on 1444 data, and no node has zero outgoing edges across all goods.

### C469 — CONFIRMED

> Per-good eligibility still prevents a nation's power from shoving a good away from where it collects that good.
>
> *MODEL / derivation / depends on C089*

**Method.** Derivation from C089: the condition names the good, so a country's power is inert for goods it neither steers nor collects downstream of.

**Evidence.** Valid.

### C470 — CONFIRMED

> Forcing eligibility true for all goods at once would amount to "direction doesn't exist".
>
> *MODEL / derivation / depends on C089*

**Method.** Derivation from C089: setting the eligibility predicate identically true removes every reference to phi_g from `P_transfer`, which is exactly the statement that direction plays no role.

**Evidence.** Valid.

### C471 — DEFERRED

> That would inflate transfer power everywhere.
>
> *OUTCOME / derivation / depends on C470*

**Method.** OUTCOME.

### C472 — NEEDS_GAME

> The claim that any non-collecting country with trade power is transferring is the loose community summary.
>
> *ENGINE / prose source*

**Method.** A claim about what the community says, and the audit rules forbid citing web sources.

**Evidence.** Not checkable from disk.

**Note.** Not worth game time either. What matters is C463-C465, which the C463 observation settles.

### C473 — NEEDS_GAME

> That community claim is wrong.
>
> *ENGINE / derivation / depends on C463, C464, C465*

**Method.** Derivation from C463-C465, all NEEDS_GAME.

**Evidence.** See C463.

**Note.** Settled by C463's observation.


---

## §3.8

### C474 — PARTIAL

> The vanilla gates encode an assumption that a nation pair has one global relationship to trade.
>
> *ENGINE / UNSOURCED*

**Method.** Three nation-pair direction gates were found by static analysis of the eu4.exe string table, which is the first direct evidence that such gates exist at all.

**Evidence.** (1) `DIPLO_SELLPROV_NOT_UPSTREAM:0 "$WHO$ doesn't have their Main Trading Port downstream of $PROV$: "` - the sell-province diplomatic action. (2) `TREASURE_FLEET_TOOLTIP_CANT_REACH:0 "$COUNTRY$ cannot send a Treasure Fleet because our Trade capital $OURNODE$ is not downstream from their Trade capital $THEIRNODE$."` - treasure fleets. (3) `TRADE_POWER_UPSTREAM_DESC` for propagation, which is node-pair rather than nation-pair (and section 3.8 correctly separates it).

**What is actually true.** Gates of this shape exist and are now enumerated for two of them by name. What is *not* settled from files is that they encode a single global relationship rather than, say, a per-node test - though both strings do read as one trade-capital-to-trade-capital comparison, which is the spec's reading.

**Note.** Both found gates compare **trade capitals**, not arbitrary nation pairs. That is a sharper statement than section 3.8 makes and should be written in: the gates ask whether one country's main trading port is downstream of a specific node or of another country's main trading port.

### C475 — CONFIRMED

> Under thirty graphs that assumption is false, not merely inconvenient.
>
> *MODEL / derivation / depends on C005, C159*

**Method.** Derivation from C005 and C159, made concrete by the reachability census.

**Evidence.** On 1444 data, no ordered node pair is reachable under all 29 live goods (max 23) and 75 of 6320 are reachable under none. A single global upstream/downstream relation between two nodes therefore has no truth value that all goods agree on.

### C476 — DEFERRED

> Every province is upstream for some good.
>
> *OUTCOME / derivation / depends on C005*

**Method.** OUTCOME.

### C477 — OUT_OF_SCOPE

> A region that receives your cloth ships you its furs.
>
> *WORLD / UNSOURCED*

**Method.** WORLD - a claim about trade history, outside this audit's evidence rules.

### C478 — CONFIRMED

> There is no fact of the matter for the nation-pair gate to test.
>
> *MODEL / derivation / depends on C475, C476*

**Method.** Derivation from C475 and C476.

**Evidence.** Measured: the reachability count per ordered pair takes 24 distinct values (0 to 23) on 1444 data. A boolean gate must pick a threshold, and no threshold is distinguished.

### C479 — OUT_OF_SCOPE

> The honest fix is to stop consulting the gate rather than engineer the graph so it passes.
>
> *DESIGN / derivation / depends on C478*

**Method.** DESIGN.

### C480 — OUT_OF_SCOPE

> Node-pair dependencies are different from nation-pair gates and keep reading `Φ`.
>
> *DESIGN / stipulated / depends on C113*

**Method.** DESIGN.

### C481 — CONFIRMED

> Propagation is a relation between two nodes, not two nations.
>
> *ENGINE / derivation / depends on C104*

**Method.** The engine's own propagation tooltip is phrased node-to-node.

**Evidence.** `TRADE_POWER_UPSTREAM_DESC:0 "A nation can Transfer Trade Power back upstream to trade nodes where it already has power."` - the relation named is between nodes; the nation is the subject holding power, not one side of the relation. Contrast `TREASURE_FLEET_TOOLTIP_CANT_REACH`, which compares two *countries'* trade capitals.

### C482 — CONFIRMED

> Setting propagation's direction test true would grant every country propagated power into every neighbour.
>
> *ENGINE / derivation / depends on C104*

**Method.** Derivation from C104: removing the direction test from a relation over adjacent node pairs makes every adjacency qualify.

**Evidence.** 159 undirected edges; under the direction test each contributes propagation in one direction, without it in both - exactly a doubling of propagation edges, plus the reversal of the 159 currently-inactive directions.

### C483 — DEFERRED

> That would multiply trade power across the map.
>
> *OUTCOME / derivation / depends on C482*

**Method.** OUTCOME.

### C484 — OUT_OF_SCOPE

> The node/nation distinction is easy to miss and expensive to get wrong.
>
> *DESIGN / stipulated / depends on C480*

**Method.** DESIGN.

### C485 — CONFIRMED

> Propagate Religion is node-local: it establishes a centre of conversion in the node's own province.
>
> *ENGINE / verified (method unstated)*

**Method.** Read `propagate_religion` in `common/trading_policies/00_trading_policies.txt` in full.

**Evidence.** The policy declares `center_of_reformation = yes` and `show_alert = yes`, and every condition in `can_select` / `can_maintain` is scoped either to ROOT or to `FROM` (the node). There is no province-outside-the-node scope and no direction test anywhere in the file.

### C486 — REFUTED

> Propagate Religion is gated on a trade-power threshold in that node and nothing else.
>
> *ENGINE / verified (method unstated) / depends on C485*

**Method.** Read `propagate_religion`'s `can_select` block in full rather than only its threshold.

**Evidence.** The block also requires, before any threshold is reached: a religion-group disjunction (`religion_group = muslim` OR `religion_group = zoroastrian_group` OR `religion_group = dharmic` with `mission_completed = mnd_maj_porch_of_mecca` OR the `can_use_propagate_religion` country flag OR `has_reform = reformer_state_reform` in the age of discovery or reformation); `dominant_religion = ROOT` in the default branch; `FROM = { has_trader = ROOT }` - a merchant must be present in the node; and **`is_node_in_trade_company_region = yes`** on every single rung of the threshold ladder. The policy is also `unique = yes` - only one country per node may hold it.

**What is actually true.** Propagate Religion is gated on a trade-power threshold **and on at least four other conditions**, most restrictively that the node must lie in a trade company region and that the country must have a merchant there. The direction-test part of the claim is right: there is no direction test. The "and nothing else" part is plainly wrong.

**Spec text that must change.** "Propagate Religion is node-local: it establishes a centre of conversion in the node's own province, gated on a trade-power threshold there and nothing else." (spec.md, section 3.8)

**Blast radius.** C487, C488. Note this claim carries `verified (method unstated)` provenance - it is one of only three such claims in the spec, and it is wrong. That is worth recording against the section 3.16 evidence standard.

### C487 — PARTIAL

> The whole trade-policy family behaves the same way.
>
> *ENGINE / verified (method unstated) / depends on C486*

**Method.** Read all nine policies in `common/trading_policies/00_trading_policies.txt` and grepped the file for any direction predicate.

**Evidence.** **No direction test appears anywhere in the file** - confirmed for the whole family. But the family does not behave the same way otherwise: `maximize_profit` / `maximize_profit_upgraded`, `hostile_trading` / `hostile_trading_upgraded`, `establish_communities` / `establish_communities_upgraded` require only `FROM = { has_trader = ROOT }` with **no threshold at all**; `improve_inland_routes` requires 50/40 trade share; `propagate_religion` requires the ladder plus four other conditions.

**What is actually true.** The family shares the absence of a direction test - that is the load-bearing point and it holds. It does not share a threshold structure: three of the five policies have no trade-share threshold at all.

**Spec text that must change.** "The whole trade-policy family behaves the same way - a policy can be set in any node where the country meets the threshold, with no direction test anywhere." (spec.md, section 3.8)

**Blast radius.** C488.

### C488 — PARTIAL

> A trade policy can be set in any node where the country meets the threshold, with no direction test anywhere.
>
> *ENGINE / derivation / depends on C486, C487*

**Method.** Derivation from C486 and C487; the direction half survives, the threshold half does not.

**Evidence.** Confirmed: no direction test in `common/trading_policies/00_trading_policies.txt`. Refuted: "any node where the country meets the threshold" - every policy additionally requires `has_trader = ROOT`, and `propagate_religion` requires `is_node_in_trade_company_region = yes` plus religion conditions.

**What is actually true.** A trade policy can be set in any node where the country has a merchant and meets that policy's own conditions, of which a trade-share threshold is only sometimes one. No direction test is involved.

**Spec text that must change.** "a policy can be set in any node where the country meets the threshold, with no direction test anywhere" (spec.md, section 3.8)

**Blast radius.** C290, C489.

### C489 — OUT_OF_SCOPE

> This is recorded now because the deferred call-site artifact does not exist yet.
>
> *DESIGN / stipulated / depends on C350*

**Method.** DESIGN.

### C490 — DEFERRED

> A community restatement of the "downstream target" claim would otherwise reintroduce these as gates.
>
> *OUTCOME / prose source / depends on C472*

**Method.** OUTCOME.

### C491 — CONFIRMED

> A gate is a boolean while a scope is a set or a path.
>
> *MODEL / stipulated / depends on C114*

**Method.** Definitional (a type distinction).

**Evidence.** Valid.

### C492 — CONFIRMED

> Answering a scope question with any-good reachability would be an enormous buff.
>
> *MODEL / derivation / depends on C476, C491*

**Method.** Measured directly on the 1444 reachability census (`t_model3.py`).

**Evidence.** Under any-good reachability, **6245 of 6320** ordered node pairs qualify - 98.8% of the map. Under a single graph the figure is bounded by the Phi DAG's transitive closure, which is far smaller. The buff is as large as claimed, and now quantified.

### C493 — CONFIRMED

> `Φ` is the graph the engine already walks.
>
> *ENGINE / derivation / depends on C062*

**Method.** True by construction of the design, and checked against the node file's role. The mod emits Phi as `00_tradenodes.txt` (C228/C236/C237), and that file is the only graph the engine has.

**Evidence.** The engine reads adjacency exclusively from `common/tradenodes/00_tradenodes.txt` - 159 `outgoing` blocks across 80 nodes, with no second adjacency source anywhere in `common/`, `map/`, or the eu4.exe string table. Whatever orientation is emitted there is definitionally the graph the engine walks.

### C494 — OUT_OF_SCOPE

> Therefore the scope call sites are left alone.
>
> *DESIGN / derivation / depends on C493*

**Method.** DESIGN.

### C495 — OUT_OF_SCOPE

> Leaving them alone collapses the shared-predicate risk.
>
> *DESIGN / derivation / depends on C494*

**Method.** DESIGN.

### C496 — OUT_OF_SCOPE

> Scoping by `Φ` is legible: one map predicts where fleets sail.
>
> *DESIGN / stipulated / depends on C114*

**Method.** DESIGN.

### C497 — OUT_OF_SCOPE

> Scoping by `Φ` is balanced.
>
> *DESIGN / stipulated / depends on C492*

**Method.** DESIGN.

### C498 — DEFERRED

> Area-effect mechanics scoped by any-good reachability would cover a large fraction of the world.
>
> *OUTCOME / derivation / depends on C492*

**Method.** OUTCOME.

**Evidence.** Quantified under C492: 98.8% of ordered node pairs.


---

## §3.9

### C499 — CONFIRMED

> `Φ` is a legal DAG because it is itself a potential.
>
> *MODEL / derivation / depends on C061*

**Method.** Derivation from C061.

**Evidence.** Same proof and the same real-data check: `aggregate Phi acyclic: True`.

### C500 — CONFIRMED

> `Φ` is the value-weighted aggregate of the real economy rather than an invented baseline.
>
> *MODEL / derivation / depends on C060*

**Method.** Derivation from C060: Phi is `sum_g V_g phi_g` with `V_g` the good's realised world trade value, so it is a value-weighted aggregate by construction.

**Evidence.** `sum_g V_g = 3662.400000` equals the world trade value computed independently from `history/provinces` x `00_prices.txt`.

### C501 — OUT_OF_SCOPE

> Once the displayed numbers are the model's numbers, the installed graph must be the one the economy actually runs.
>
> *DESIGN / derivation / depends on C149*

**Method.** DESIGN.

### C502 — CONFIRMED

> `ΔΦ` is not the net value crossing an edge.
>
> *MODEL / derivation / depends on C506, C507*

**Method.** Derivation from C506/C507, both confirmed.

**Evidence.** Valid.

### C503 — CONFIRMED

> The earlier claim that `ΔΦ` is net value was an error.
>
> *MODEL / derivation / depends on C502*

**Method.** A self-correction internal to the spec; the corrected version (C502) is confirmed.

**Evidence.** See C502.

### C504 — CONFIRMED

> `ΔΦ = Σ_g V_g Δφ_g` is the analytic figure.
>
> *MODEL / derivation / depends on C060*

**Method.** Definitional: differencing `Phi = sum_g V_g phi_g` across an edge gives `sum_g V_g (phi_g(u) - phi_g(v))` by linearity.

**Evidence.** Immediate.

### C505 — CONFIRMED (conditional)

> Realized movement follows vanilla propagation rules instead.
>
> *ENGINE / derivation / depends on C091*

**Method.** Derivation from C091, a design stipulation resting on C092/C097, both NEEDS_GAME.

**Evidence.** Sound inference.

### C506 — CONFIRMED

> A good with large Δφ can be diluted by an even split across three links.
>
> *MODEL / derivation / depends on C097*

**Method.** Constructed the case explicitly on the real graph. A node with three outgoing links and no steerer splits its outgoing value into thirds (C097); the resulting per-link flow is one third of `V_g` regardless of how large `Delta phi_g` is.

**Evidence.** 24 of 80 vanilla nodes have >= 3 outgoing links; max out-degree is 4 (`california`, `ivory_coast`). The dilution factor there is 1/4.

### C507 — CONFIRMED

> A good with small Δφ can be winner-take-all steered the other way.
>
> *MODEL / derivation / depends on C095*

**Method.** Same construction from the other side: a single steerer takes all of `g`'s outgoing value down its link (C095) however small `Delta phi_g` is.

**Evidence.** Given C095, realised flow on the steered link is `V_g x outgoing_share`, independent of `Delta phi_g`.

### C508 — CONFIRMED

> A link can therefore be oriented `n → m` under `Φ` while realized net flow runs `m → n`.
>
> *MODEL / derivation / depends on C506, C507*

**Method.** Constructed by combining C506 and C507 arithmetically: pick a link where a large-`V_g` good is diluted three ways in the Phi direction and a smaller-`V_h` good is winner-take-all steered the other way. Whenever `V_h > V_g/3` the net crosses zero and reverses.

**Evidence.** The construction needs only that a node have >= 3 outgoing links and partial merchant coverage, which describes 24 of 80 vanilla nodes.

### C509 — OUT_OF_SCOPE

> That is why the disagreement rate is measured rather than assumed.
>
> *DESIGN / derivation / depends on C508*

**Method.** DESIGN.

### C510 — OUT_OF_SCOPE

> And why the negative-link display policy is deferred to data.
>
> *DESIGN / derivation / depends on C508*

**Method.** DESIGN.

### C511 — OUT_OF_SCOPE

> The analytic `flow_g = V_g · Δ` has no consumer in the design.
>
> *DESIGN / derivation / depends on C502*

**Method.** DESIGN.

### C512 — CONFIRMED

> Link values are realized flows, which makes conservation hold by construction.
>
> *MODEL / derivation / depends on C257*

**Method.** Proof: if link values are the realised flows themselves, then node balance `in + local = out + collected` is an identity of the flow bookkeeping, not a property to be checked.

**Evidence.** Trivially true by construction; nothing to measure.


---

## §3.10

### C513 — OUT_OF_SCOPE

> Paying countries correctly while leaving the display wrong is a strictly weaker position.
>
> *DESIGN / stipulated / depends on C514*

**Method.** DESIGN.

### C514 — DEFERRED

> With a wrong display, node values, pie charts and the ledger would describe an economy nobody is playing.
>
> *OUTCOME / derivation / depends on C150*

**Method.** OUTCOME.

### C515 — PARTIAL

> AI light-ship building reads those figures.
>
> *ENGINE / UNSOURCED*

**Method.** Searched the AI defines in `common/defines.lua` for consumers of node trade figures; found several, none specifically about light-ship building.

**Evidence.** Confirmed AI consumers of trade figures: `PEACE_TERMS_TRADE_POWER_VALUE_MULT = 0.1, -- AI desire for transfering trade power is multiplied by this for each 0.1 trade value in shared nodes`; `PEACE_TERMS_TRADE_POWER_VALUE_MAX = 2.0`; `DIPLOMATIC_ACTION_EMBARGO_TRADE_POWER_FACTOR = 25.0, -- ... for each 1.0 value in shared nodes`; `DIPLOMATIC_ACTION_TRADE_POWER_FACTOR = 25.0`; `UPGRADE_CENTER_OF_TRADE_AI_POWER_DESIRE = 5.0, -- ... division on the amount of trade power AI has in node`; `TRADE_INTEREST_THRESHOLD = 3, -- Number of merchants required to be a nation with trade interest`. No light-ship define references node value; `LIGHT_SHIP_MAINT_FACTOR = 0.03` is a cost constant only.

**Note.** Settling observation: not worth game time on its own - the point (AI reads node figures) is established by C517 and by the defines above.

### C516 — NEEDS_GAME

> AI trade-league behaviour reads those figures.
>
> *ENGINE / UNSOURCED*

**Method.** No trade-league AI define references node trade value.

**Evidence.** The trade-league defines found are structural: `TRADE_LEAGUE_MUST_TRANSFER_TO_LEADER`, `TRADE_LEAGUE_TOO_BIG:0 "Trade League members may only have one province."`, `TRADELEAGUE_MAX_SIZE`, `TRADE_LEAGUE_BREAK_OPINION`. None keys on value.

**Note.** Settling observation: not high value. Section 3.10's argument needs only one AI consumer to exist, and C517 supplies two by name.

### C517 — CONFIRMED

> AI peace valuation reads those figures.
>
> *ENGINE / UNSOURCED*

**Method.** Read the peace-term AI defines in `common/defines.lua`.

**Evidence.** `PEACE_TERMS_TRADE_POWER_VALUE_MULT = 0.1, -- AI desire for transfering trade power is multiplied by this for each 0.1 trade value in shared nodes` and `PEACE_TERMS_TRADE_POWER_VALUE_MAX = 2.0, -- Max AI desire for transfering trade power from shared node value`. AI peace valuation reads node trade value explicitly.

### C518 — CONFIRMED

> Income-threshold events read those figures.
>
> *ENGINE / UNSOURCED*

**Method.** Found income-threshold triggers in the scripted-trigger vocabulary.

**Evidence.** `INCOME_BALANCE_MORE_THAN:0 "Last Month's Income Balance more than "` and `INCOME_BALANCE_LESS_THAN:0 "Last Month's Income Balance less than "` are engine trigger tooltips, and `INCOME_FROM_NODES_I` shows trade income is part of the balance. Events keyed on those triggers therefore read the written figures.

### C519 — CONFIRMED

> The engine's data model is sufficient at node level.
>
> *MODEL / derivation / depends on C521, C523*

**Method.** Derivation from C521 and C523, both confirmed numerically.

**Evidence.** See C521.

### C520 — CONFIRMED

> `collect_pool` is per good on the inside because `collected_share` depends on `P_transfer(g)`.
>
> *MODEL / derivation / depends on C087, C088*

**Method.** Derivation from C087/C088; identical to C260.

**Evidence.** Immediate from the formula.

### C521 — CONFIRMED

> `income_C(n) = Σ_g value_g(n)·collected_share(n,g)·powershare_C(n) = powershare_C(n)·collect_pool(n)`.
>
> *MODEL / derivation / depends on C264*

**Method.** Algebraic proof plus a numerical experiment with mixed sinks, mixed collectors, per-good transfer eligibility and the off-home penalty in play (`t_model3.py`). Proof: `sum_g v_g cs_g ps_C = ps_C sum_g v_g cs_g` whenever `ps_C` carries no `g` index.

**Evidence.** Per-good income `[8.2527886288, 88.8345607938, 0.0, 104.3157035514]`; scalar-model income `[8.2527886288, 88.8345607938, 0.0, 104.3157035514]`; `max abs difference: 1.421e-14` on a node paying 201.40 - agreement at the 7e-17 relative level.

### C522 — CONFIRMED (independently reproduced)

> Verified numerically to 5.7e-14 across a node with mixed sinks, mixed collectors and the home-node penalty in play.
>
> *MODEL / numerical test / depends on C521*

**Method.** Re-ran the spec's experiment from scratch with an independently generated setup.

**Evidence.** The spec reports 5.7e-14; this audit's independent run gives **1.421e-14** on a 201.40-ducat node with 4 countries, 6 goods, 2 of 6 goods at their sink, 3 of 4 countries collecting, one of them off-home at `TRADE_NON_CAPITAL_OFFICE = -0.50`, and per-good transfer eligibility drawn at random. Same order of magnitude, same conclusion.

### C523 — CONFIRMED

> One scalar per node reproduces every country's income exactly.
>
> *MODEL / derivation / depends on C521, C522*

**Method.** Derivation from C521/C522.

**Evidence.** Same experiment.

### C524 — CONFIRMED (conditional)

> The engine's own math does the rest.
>
> *ENGINE / derivation / depends on C523*

**Method.** Derivation from C523; conditional on the engine's collection math being power-proportional (C099).

**Evidence.** Sound inference; C099 is PARTIAL.

### C525 — CONFIRMED

> This is also why propagation cannot be made per good.
>
> *MODEL / derivation / depends on C527, C528*

**Method.** Derivation from C527/C528, reproduced independently.

**Evidence.** See C527.

### C526 — CONFIRMED (independently reproduced)

> With propagation reading `Φ`, the node-scalar model reproduces per-good truth to 1.4e-14.
>
> *MODEL / numerical test / depends on C111*

**Method.** The C521 experiment is exactly this case: propagation reading a single graph means power has no `g` index.

**Evidence.** Spec reports 1.4e-14; this audit's independent run gives 1.421e-14 on a comparable node. Same result.

### C527 — CONFIRMED (mechanism); PARTIAL (magnitude)

> With power varying by good, the node-scalar model is off by 5.96 ducats on a node paying about 250.
>
> *MODEL / numerical test*

**Method.** Re-ran the spec's contrast: same node, but with trade power varying by good (`t_model3.py`).

**Evidence.** Per-good truth `[9.460273, 86.468248, 0.0, 107.121975]` versus the best node-scalar model (value-weighted power share) `[9.321272, 85.794865, 0.0, 107.934358]`; **`max abs error: 0.8124 ducats on a node paying 203.05`**. The spec reports 5.96 ducats on a node paying ~250.

**What is actually true.** The mechanism is exactly as claimed and reproduces: once power carries a `g` index, `powershare_C` no longer factors out and the node-scalar model is wrong by a finite amount. The specific magnitude is setup-dependent - it scales with the spread of per-good power, which the spec does not record - so 5.96/250 (2.4%) versus 0.81/203 (0.4%) is not a discrepancy in the claim, but the number should not be quoted as if it were a constant.

**Spec text that must change.** "Tested: ... With power varying by good, it is off by 5.96 ducats on a node paying ~250 - because `powershare_C` stops factoring out." (spec.md, section 3.10) - the figure needs its setup recorded, or it should be given as a range.

**Blast radius.** C528, C529, C649. All survive; only the number needs a caveat.

### C528 — CONFIRMED

> The cause is that `powershare_C` stops factoring out.
>
> *MODEL / derivation / depends on C527*

**Method.** Proof: `sum_g v_g cs_g ps_C(g)` has no common factor when `ps_C` depends on g.

**Evidence.** Demonstrated by the 0.81-ducat residual under C527.

### C529 — OUT_OF_SCOPE

> Keeping propagation on a single graph is load-bearing for Goal 7, not merely convenient.
>
> *DESIGN / derivation / depends on C365, C525*

**Method.** DESIGN.

### C530 — CONFIRMED

> Only the decomposition by good exceeds what the engine can hold.
>
> *MODEL / derivation / depends on C523*

**Method.** Derivation from C523: the node scalar suffices for income; only per-good *display* exceeds the one-field-per-node UI (C158/C160).

**Evidence.** Valid.


---

## §3.11

### C531 — CONFIRMED

> In vanilla, steering is outgoing-only.
>
> *ENGINE / UNSOURCED*

**Method.** The engine's own shipped steering hint.

**Evidence.** `HINT_TRADESTEERING_TEXT:0 "...This will transfer Trade Value from a Trade Node to the next Trade Node **downstream**. ... **You can never steer trade upstream** or past your Main Trade City."` (`localisation/hints_l_english.yml`). Corroborated structurally: `common/tradenodes/00_tradenodes.txt` declares no link in both directions (`bidirectional pairs: 0`).

### C532 — REFUTED

> The vanilla node map shows only the paths leaving a node.
>
> *ENGINE / UNSOURCED / depends on C531*

**Method.** Read the node window definition in `interface/tradeinterface.gui`.

**Evidence.** The vanilla node window has **both** lists. Line 90: `OverlappingElementsBoxType = { name = "incoming_nodes_listbox" position = { x = 10 y = -15 } size = { x = 400 y = 32 } ... }`. Line 110: `OverlappingElementsBoxType = { name = "outgoing_nodes_listbox" ... }`. Both are populated with the same `TradeNodeLink` window type (line 17), which contains a clickable `guiButtonType = { name = "NextNodeButton" ... }`. The labels `INCOMING_LINKS:0 "Incoming"` and `OUTGOING_LINKS:0 "Outgoing"` exist (currently commented out in the .gui, but the listboxes are live). The second node-window variant at line 509 has the same pair.

**What is actually true.** The vanilla node window already lists **incoming** links alongside outgoing ones, each as a clickable entry. What is outgoing-only is *steering* (C531, separately confirmed), not the display.

**Spec text that must change.** "In vanilla, steering is outgoing-only - the map shows the paths leaving a node and nothing else, and trade cannot be steered upstream at any amount of power." (spec.md, section 3.11) - the middle clause is wrong.

**Blast radius.** C073 and C166 - the section 1.7 "widening" is smaller than described, since the incoming list already exists and is already rendered with buttons; what must change is what those buttons *do*. C534 and C535 survive on C531 and C533 alone. Residual engine question: whether the vanilla incoming-link button already accepts a merchant assignment or only navigates (its name `NextNodeButton` suggests navigation).

### C533 — CONFIRMED

> In vanilla, trade cannot be steered upstream at any amount of power.
>
> *ENGINE / UNSOURCED / depends on C531*

**Method.** Same source as C531.

**Evidence.** `"You can never steer trade upstream or past your Main Trade City."`

### C534 — CONFIRMED

> So in vanilla "assigned" and "steering" are the same condition.
>
> *ENGINE / derivation / depends on C531, C533*

**Method.** Derivation from C531 and C533; C532's refutation does not touch it, because it concerns display rather than steering.

**Evidence.** Valid.

### C535 — CONFIRMED

> The engine therefore never had to distinguish them.
>
> *ENGINE / derivation / depends on C534*

**Method.** Derivation from C534.

**Evidence.** Valid.

### C536 — CONFIRMED

> §1.7's widening to incident links pulls "assigned" and "steering" apart.
>
> *MODEL / derivation / depends on C073*

**Method.** Derivation from C073.

**Evidence.** Valid.

### C537 — PARTIAL

> Caravan power fires on a merchant plus an inland link end, with nothing checking whether value moves.
>
> *ENGINE / UNSOURCED*

**Method.** Located the engine's caravan grant conditions - both the tooltip and the two internal identifiers.

**Evidence.** `TRADEMAP_INLAND_DESC:0 "Having a merchant present that **collects in** an inland trade node, **or steers towards** an inland trade node, will give you extra trade power in that node based on your trade efficiency."` and, in the eu4.exe string table, the two internal names **`merchant_present_inland`** (0x021a6c84) and **`merchant_steering_to_inland`** (0x021a6e8c).

**What is actually true.** The grant conditions are enumerated and neither checks whether value moves - so that half is right. But the conditions are *collect in an inland node* or *steer towards an inland node*, which is narrower than "a merchant plus an inland link end": a merchant steering **out of** an inland node satisfies neither name.

**Spec text that must change.** "Caravan power fires on a merchant plus an inland link end, with nothing checking whether value moves" (spec.md, section 3.11)

**Blast radius.** C538 (separately and more seriously wrong), C539, C540. The section 1.7 caravan condition (C079/C080) is still the right fix, but the exposure it closes is smaller than section 3.11 states.

### C538 — REFUTED

> Steering from Crimea to Kiev grants the caravan bonus in Crimea.
>
> *ENGINE / UNSOURCED / depends on C537*

**Method.** Read the engine's inland tooltip against the specific example the spec gives, and checked which nodes are inland.

**Evidence.** `kiev` **is** inland (`inland=yes` in `common/tradenodes/00_tradenodes.txt`; and it has 0 coastal members by derivation). `crimea` is not. `TRADEMAP_INLAND_DESC` says a merchant that "steers towards an inland trade node" gives extra trade power **"in that node"** - and the tooltip is the *inland node's* map tooltip, so "that node" is the inland node. The internal identifier is `merchant_steering_to_inland`, again named from the inland node's side.

**What is actually true.** Steering from Crimea to Kiev grants the caravan bonus **in Kiev**, the inland node - not in Crimea. Both the tooltip's referent and the internal identifier's name point at the inland node as the recipient.

**Spec text that must change.** "Caravan power fires on a merchant plus an inland link end, with nothing checking whether value moves - steering from Crimea to Kiev grants the bonus in Crimea." (spec.md, section 3.11)

**Blast radius.** **C539 and C540 both invert.** If the bonus lands in the inland node, then the exposure created by section 1.7's widening is not "any node adjacent to one of the roughly 26 inland nodes" but the 26 inland nodes themselves - a smaller and differently-shaped surface, and one that changes what the section 1.7 caravan condition has to guard. C136, C137, C138 and C544 are unaffected in magnitude but relocate.

**Note.** This is the single most consequential engine finding in this audit that is *not* fully settled, so state the settling observation precisely. **Observation:** place a merchant in a coastal node adjacent to an inland node, set it to steer toward the inland node, and read the country's trade power in **both** nodes before and after. Whichever node's figure jumps by `min(dev/3 + modifiers, 50)` is the recipient. Setup: any save, one merchant, two node windows. No debugger. This is 2.7 probe 6 and it should be promoted out of the debugger session, since it needs none.

### C539 — DEFERRED

> Without an added condition, a merchant assigned to an incoming link and inert for every good would earn a major power the full caravan bonus.
>
> *OUTCOME / derivation / depends on C075, C537*

**Method.** OUTCOME.

**Evidence.** Contrary evidence: its location premise (C538) is refuted - the bonus appears to land in the inland node, not the adjacent one.

### C540 — DEFERRED

> That would apply at any node adjacent to one of the inland nodes.
>
> *OUTCOME / derivation / depends on C539, C541*

**Method.** OUTCOME.

**Evidence.** Same: relocates to the 26 inland nodes if C538's refutation holds.

### C541 — CONFIRMED

> There are roughly 26 inland nodes.
>
> *ENGINE / file value*

**Method.** Counted `inland=yes` in `common/tradenodes/00_tradenodes.txt` and independently derived inland status from the map bitmap (`scratchpad/v/coastal.py`).

**Evidence.** **26** nodes carry `inland=yes`: african_great_lakes, kongo, zambezi, ohio, lhasa, chengdu, xian, siberia, yumen, doab, lahore, deccan, katsina, ethiopia, samarkand, persia, astrakhan, kiev, kazan, timbuktu, pest, krakow, wien, saxony, rheinland, champagne. By the section 2.2 derivation rule (no coastal member) the count is **25** - `siberia` has two coastal members (1781 Western Siberia, 1782 Central Siberia). See C210.

**Note.** "Roughly 26" is right either way, but the implementation must decide which number it means: the flag gives 26, the derivation gives 25, and section 2.2 (C209) chooses the derivation.

### C542 — PARTIAL

> Caravan power equals total country development ÷ 3, capped at 50.
>
> *ENGINE / file value / depends on C219*

**Method.** Read the three caravan defines in `common/defines.lua` lines 1220-1222 and the engine's own caravan tooltip.

**Evidence.** `CARAVAN_FACTOR = 3.0,  -- Development is divided by this factor, do not set to zero!`, `CARAVAN_POWER_MAX = 50`, **`CARAVAN_POWER_MIN = 2`**. Tooltip: `CARAVAN_POWER_DESC2:1 "Inland caravans provide a total of $VALUE$ trade power, base of it coming from a **third of your development**($BASE$) **and $MODIFIER$ from policies and ideas**."`

**What is actually true.** Caravan power = clamp(total development / 3 **plus modifiers from policies and ideas**, `CARAVAN_POWER_MIN = 2`, `CARAVAN_POWER_MAX = 50`). The claim omits both the additive policy/idea term - which the engine's own tooltip names explicitly - and the floor of 2.

**Spec text that must change.** "Since caravan power is total country development / 3 capped at 50, every major power is at the cap from 1444 and it does not scale with node presence at all." (spec.md, section 3.11)

**Blast radius.** C136, C543, C544. All three survive - the additive term only makes the cap easier to reach, and the floor only matters for tiny countries - but the formula as written is incomplete and the solver must read `CARAVAN_POWER_MIN` too.

### C543 — CONFIRMED (with a named exception list)

> Every major power is at the caravan cap from 1444.
>
> *ENGINE / derivation / depends on C542*

**Method.** Computed total development (`base_tax + base_production + base_manpower` over owned `is_city` provinces) for every country at 1444.11.11 from `history/provinces`, then compared `dev/3` against `CARAVAN_POWER_MAX = 50`.

**Evidence.** **19 of 652 countries have dev >= 150 and are therefore at the cap at the 1444 start**: MNG (1102 dev, 367.3), ENG (338, 112.7), TUR (320, 106.7), CAS (281, 93.7), LIT (268, 89.3), VIJ (263, 87.7), FRA (252, 84.0), MAM (242, 80.7), ARA (221, 73.7), JNP (212, 70.7), BAH (201, 67.0), MOS (197, 65.7), SHY (189, 63.0), POL (183, 61.0), BNG (177, 59.0), HUN (176, 58.7), VEN (175, 58.3), HAB (171, 57.0), QAR (161, 53.7). Just below: **BUR 147 (49.0), KOR 145 (48.3), TIM 142 (47.3), POR 136 (45.3), AYU 134, NOV 131**. 522 of 652 countries clear `CARAVAN_POWER_MIN = 2`.

**Note.** "Every major power" is right for 19 countries and wrong for Burgundy, Korea, the Timurids and Portugal, which start 2-10% short. Given C542's additive policy/idea term, all four reach the cap with any caravan modifier at all, so the substance holds - but the exception list is worth recording, especially Portugal, whose caravan power matters for the colonial argument.

### C544 — CONFIRMED

> Caravan power does not scale with node presence at all.
>
> *ENGINE / derivation / depends on C542*

**Method.** The formula's arguments are country development and the three constants; no term references the node.

**Evidence.** `CARAVAN_FACTOR` divides *country* development; `CARAVAN_POWER_MAX`/`MIN` clamp the result. `CARAVAN_POWER_DESC2` describes it as a country total. Nothing in the defines or the tooltip references provinces held in the node.

### C545 — OUT_OF_SCOPE

> Requiring the merchant to steer something restores the vanilla state of affairs.
>
> *DESIGN / derivation / depends on C534*

**Method.** DESIGN.

### C546 — OUT_OF_SCOPE

> Granting caravan power on bare assignment would be the deviation.
>
> *DESIGN / derivation / depends on C545*

**Method.** DESIGN.

### C547 — OUT_OF_SCOPE

> That deviation would be an unintended one.
>
> *DESIGN / derivation / depends on C546*

**Method.** DESIGN.


---

## §3.12

### C548 — OUT_OF_SCOPE

> Consistency with §3.8 is the weaker argument for always granting treasure fleets.
>
> *DESIGN / stipulated / depends on C112, C144*

**Method.** DESIGN.

### C549 — REFUTED (by dependency)

> The treasure-fleet gate is bistable.
>
> *MODEL / derivation / depends on C551, C552*

**Method.** Derivation from C551 and C552, both of which rest on the refuted C049.

**Evidence.** The bistability requires colonial gold income to enter `wealth`. Under the spec's own `wealth(p) = tax_income(p) + production_income(p)` and EU4's separate `INCOMEGOLD` category (C049), gold income never enters wealth - so granting or denying the treasure fleet moves nothing in the demand vector, and the feedback loop does not close.

**What is actually true.** The treasure-fleet gate is not bistable **under this model**, because the quantity that would create the feedback (colonial gold income) is not in `wealth`. The gate may still be worth always granting for the section 3.8 consistency reason (C548), which the spec itself calls the weaker argument - but the stronger argument does not stand as written.

**Spec text that must change.** "Consistency with section 3.8 is the weaker argument. The stronger one is that the gate is bistable. Denial is not neutral: the colonial nation keeps the gold *and any income gained from it*, so its node's wealth rises..." (spec.md, section 3.12)

**Blast radius.** C551, C552, C553, C554, C555 - the entire bistability chain. Also C144, whose justification changes (it keeps the section 3.8 consistency ground and loses the bifurcation ground). **Recoverable**: the parenthetical "*and any income gained from it*" is the escape - gold spent on development does raise `base_tax`/`base_production` and therefore `wealth` (the long loop, C405). If the argument is restated on that indirect path it survives, but it becomes a slow, second-order feedback rather than a direct one, which materially weakens "two otherwise identical campaigns diverge permanently".

### C550 — PARTIAL

> Denial is not neutral: the colonial nation keeps the gold and any income gained from it.
>
> *ENGINE / UNSOURCED*

**Method.** Confirmed the denial branch exists and what it does with the gold; the 'and any income gained from it' half is the disputed part.

**Evidence.** `TREASURE_FLEET_TOOLTIP_CANT_REACH_DELAYED:0 "§RThey will keep their gold income instead.§!\n\nIf we would move our Trade capital to a node downstream to theirs, we would receive Treasure Fleets."` - the engine states plainly that on denial the colonial nation keeps the gold income.

**What is actually true.** "The colonial nation keeps the gold" is confirmed verbatim by the engine's own tooltip. "And any income gained from it" is true only through the slow development loop (C405), not through any direct term in `wealth` (C049).

**Spec text that must change.** "Denial is not neutral: the colonial nation keeps the gold *and any income gained from it*, so its node's wealth rises, making it more sink-like, keeping it denied." (spec.md, section 3.12)

**Blast radius.** C551, C553, C554, C555.

### C551 — REFUTED (by dependency)

> Under denial the colonial node's wealth rises, making it more sink-like and keeping it denied.
>
> *MODEL / derivation / depends on C032, C550*

**Method.** See C549 and C049.

**Evidence.** Gold income is not in `wealth`, so keeping it does not raise the node's wealth directly.

**What is actually true.** Under the spec's own definition, denial leaves the colonial node's `wealth` unchanged in the month it happens. Only reinvestment into development moves it, on a multi-year timescale.

**Spec text that must change.** "the colonial nation keeps the gold and any income gained from it, so its node's wealth rises, making it more sink-like, keeping it denied" (spec.md, section 3.12)

**Blast radius.** C553, C554, C555.

### C552 — REFUTED (by dependency)

> Under granting the income is diverted, lowering the node's wealth, making it more source-like and keeping it granted.
>
> *MODEL / derivation / depends on C032, C148*

**Method.** See C549 and C049.

**Evidence.** Symmetrically: granting diverts income that was never in `wealth`, so it lowers nothing.

**What is actually true.** Granting does not lower the colonial node's `wealth` under the model as specified.

**Spec text that must change.** "Granting diverts that income, lowering the node's wealth, making it more source-like, keeping it granted." (spec.md, section 3.12)

**Blast radius.** C553, C554, C555.

### C553 — REFUTED (by dependency)

> Both states self-reinforce.
>
> *MODEL / derivation / depends on C551, C552*

**Method.** Derivation from C551 and C552, both refuted.

**Evidence.** Neither state reinforces itself through `wealth`.

**What is actually true.** The two states do not self-reinforce through the demand vector.

**Spec text that must change.** "Both states self-reinforce" (spec.md, section 3.12)

**Blast radius.** C554, C555.

### C554 — DEFERRED

> Two otherwise identical campaigns would diverge permanently on whichever state they started in.
>
> *OUTCOME / derivation / depends on C553*

**Method.** OUTCOME.

**Evidence.** Its premise C553 is refuted by dependency.

### C555 — REFUTED (by dependency)

> Granting removes a bifurcation, not just a lock-in.
>
> *MODEL / derivation / depends on C554*

**Method.** Derivation from C554.

**Evidence.** No bifurcation exists if the states do not self-reinforce.

**What is actually true.** Granting removes a consistency inconsistency (C548), not a bifurcation.

**Spec text that must change.** "Granting removes a bifurcation, not just a lock-in." (spec.md, section 3.12)

**Blast radius.** C144's justification.

### C556 — PARTIAL

> Inflation scales with money received relative to economy size.
>
> *ENGINE / UNSOURCED*

**Method.** Read every inflation define in `common/defines.lua` and checked which are share-based.

**Evidence.** `GOLD_INFLATION = 0.5` with `GOLD_INFLATION_THRESHOLD = 0.0` (a threshold on a *share*, which only makes sense if the input is a ratio), `TREASURE_FLEET_INFLATION = 0.5`, and decisively `INFLATION_FROM_PEACE_GOLD = 0.02, -- **inflation per month of income** taken in peace (also applied to province sales)` - explicitly normalised by the recipient's income. Also `INFLATION_FROM_LOAN = 0.1`, `BASE_YEARLY_INFLATION = 0`.

**What is actually true.** For peace gold the normalisation by income is stated outright in the file. For treasure fleets, `TREASURE_FLEET_INFLATION = 0.5` sits in the same block as `GOLD_INFLATION = 0.5` / `GOLD_INFLATION_THRESHOLD = 0.0` and is very likely the same shape, but the file does not say so.

**Note.** Settling observation: receive one treasure fleet of known size as a small country and as a large one, and compare the inflation tick. Setup: an El Dorado save, or two.

### C557 — DEFERRED

> Universal granting hits small previously-cut-off colonizers hardest.
>
> *OUTCOME / derivation / depends on C556*

**Method.** OUTCOME.

### C558 — CONFIRMED (conditional)

> The route rule is a balance dial because privateers skim per node passed.
>
> *MODEL / derivation / depends on C146*

**Method.** Derivation from C146, which is NEEDS_GAME.

**Evidence.** If privateers skim per node passed, hop count is a linear lever on the loss. Sound inference.

### C559 — OUT_OF_SCOPE

> Hop counts must be compared between candidate rules on the mod's own graph.
>
> *DESIGN / derivation / depends on C560*

**Method.** DESIGN.

### C560 — OUT_OF_SCOPE

> Comparing hop counts against vanilla's graph would be a counterfactual on a graph the mod has replaced.
>
> *DESIGN / derivation / depends on C062*

**Method.** DESIGN.


---

## §3.13

### C561 — OUT_OF_SCOPE

> Prose-sourced premises are to be distrusted, and nothing is to be built on them.
>
> *DESIGN / stipulated / depends on C674*

**Method.** DESIGN.

### C562 — NEEDS_GAME

> The evidence for a colonization trade-direction gate is one mod author's report.
>
> *ENGINE / prose source*

**Method.** Prose-sourced; web sources are not admissible as validation under the audit rules. What *can* be reported is that no colonization direction gate is visible in any game file.

**Evidence.** Searched `common/`, `events/`, `decisions/`, `missions/` for any colonization trigger referencing trade direction: none. The colonisation defines found are `COLONIST_DISTANCE_DIVISOR = 1000`, `COLONIST_TIME = 0.3`, `COLONIAL_MAINTENANCE_FACTOR = 8.0`, `LARGE_COLONIAL_NATION_LIMIT = 10`, `CONQUEST_INTEREST_DISTANCE = 100` - all distance or cost, none directional. The three direction call sites found by static string analysis are sell-province, treasure fleets and propagation (see the summary) - **none is colonisation**.

**Note.** This is a real partial result for section 3.13: static analysis of the shipped binary's string table turned up direction gates for two mechanics and colonisation was not among them. It does not prove absence (a gate need not have a tooltip string), but it is evidence in the direction C564 already argues for. Settling step: 2.7 probe 10's disassembly.

### C563 — OUT_OF_SCOPE

> That report is contradicted in-thread.
>
> *WORLD / prose source / depends on C562*

**Method.** WORLD - a claim about a forum thread, outside this audit's evidence rules.

### C564 — PARTIAL

> The observed colonization behaviour needs no gate at all to explain it.
>
> *ENGINE / derivation / depends on C565*

**Method.** Derivation from C565; supported by the negative result under C562.

**Evidence.** No colonisation-direction gate appears in any shipped file, and no `*_NOT_UPSTREAM`-style refusal string exists for colonisation in the eu4.exe string table (the only two such strings are `DIPLO_SELLPROV_NOT_UPSTREAM` and `TREASURE_FLEET_TOOLTIP_CANT_REACH`).

**Note.** Evidence for absence, not proof of it. Settling step: probe 10.

### C565 — DEFERRED

> If colonial nodes route away from the AI's home, expected trade income collapses and low-scoring provinces are not colonized.
>
> *OUTCOME / derivation / depends on C089*

**Method.** OUTCOME.

### C566 — OUT_OF_SCOPE

> The caller enumeration must be able to return "no colonization gate exists" as a successful result.
>
> *DESIGN / stipulated / depends on C289*

**Method.** DESIGN.

### C567 — PARTIAL

> The `TRADE_PROPAGATE_THRESHOLD` file value and the documented raw requirement differ by exactly the propagation divider.
>
> *ENGINE / file value + prose source / depends on C105, C213*

**Method.** Confirmed the file value; the "documented raw requirement" half is prose-sourced and inadmissible here.

**Evidence.** `TRADE_PROPAGATE_THRESHOLD = 2` and `TRADE_PROPAGATE_DIVIDER = 5` (defines.lua:1205-1206). If the documented raw requirement is 10, then 10/2 = 5 = the divider exactly, so the arithmetic of the claim checks out. But the figure 10 comes from prose and cannot be validated here.

**What is actually true.** The file value is 2 and the divider is 5. The relationship the claim asserts holds *if* the documented figure is 10; that figure is unverified.

**Note.** Settling observation: 2.7 probe 8 as designed (set the define to 4 and check whether the raw requirement doubles), or more cheaply: read a country's provincial trade power in a node, find the smallest value at which it propagates upstream, and compare against 10.

### C568 — NEEDS_GAME

> That discrepancy reconciles if the threshold is expressed in propagated units.
>
> *ENGINE / derivation / depends on C567*

**Method.** Derivation resting on the unverified prose figure in C567.

**Evidence.** See C567.

**Note.** Probe 8.

### C569 — CONFIRMED (as experimental design)

> Doubling the define would falsify the propagated-units reading.
>
> *ENGINE / derivation / depends on C568*

**Method.** The falsification logic is sound: if the threshold is in propagated units, doubling the define doubles the raw requirement; if it is in raw units, doubling doubles it too - so the test must compare against the *predicted number*, not merely observe a change.

**Evidence.** Arithmetic: propagated-units reading predicts 4 x 5 = 20 raw; raw-units reading predicts 4 raw. The two predictions differ by 5x, so the test discriminates cleanly.

**Note.** Worth recording in section 2.7: the probe must record the *value*, not just whether it changed.

### C570 — NEEDS_GAME

> Pass 2's ordering requirement comes from something other than propagation.
>
> *ENGINE / derivation / depends on C109*

**Method.** Derivation from C109, which is NEEDS_GAME - but C109 is settleable without a debugger.

**Evidence.** See C109.

**Note.** Settling C109 first (a three-node chain observation, no debugger) either validates this whole line of reasoning or kills it, before probe 2 costs a session.

### C571 — CONFIRMED

> Eligibility resolution is a backward reachability from collection points.
>
> *MODEL / derivation / depends on C089*

**Method.** Definitional given C089: 'collects at some node reachable from n' is a reachability query, and resolving it for all n is a backward pass from collection points.

**Evidence.** Implemented as the reverse-BFS in the C196 census machinery.

### C572 — CONFIRMED

> Eligibility resolution is the only named candidate for pass 2's ordering.
>
> *ENGINE / derivation / depends on C571*

**Method.** Read section 3.13 of `per-good-trade-spec.md` and counted the candidates it names for pass 2's ordering requirement. This is a claim about the spec's own candidate list, which is checkable by reading it.

**Evidence.** Section 3.13: "Propagation is one hop and cannot chain, so something else in that pass imposes it; eligibility resolution is a backward reachability from collection points and **is the only candidate named**." One candidate is named. The claim is accurate about the document.

**Note.** Accuracy about the list is not evidence that the list is complete - which is exactly what C573 concedes and what C574 warns about. Note also that the premise the whole argument rests on (C109, one-hop propagation) is itself unverified and is settleable without a debugger; doing that first is cheaper than probe 2.

### C573 — OUT_OF_SCOPE

> That is an argument from exhaustion.
>
> *DESIGN / stipulated / depends on C572*

**Method.** DESIGN (a methodological self-assessment).

### C574 — CONFIRMED

> The project's inventory of engine mechanisms has been wrong before.
>
> *WORLD / UNSOURCED*

**Method.** This audit is the evidence. Counted refutations of ENGINE claims against EU4 1.37.5's shipped files.

**Evidence.** Refuted ENGINE claims in this pass: C037 (no 75% overseas autonomy floor exists), C049 (gold income is its own income category, not production income), C101 (there is no trade supply-range gate at all), C128 (Improve Inland Routes is 50/40, not 33%), C130 (Propagate Religion maintains at 50, not 40), C131 (the banded/single-valued split is inverted), C139 (no scripted content names a trade node), C433 and C434 (grain and livestock base prices both wrong by exactly 2x), C486 (Propagate Religion has four further gates), C532 (the vanilla node window already lists incoming links), C538 (the caravan bonus appears to land in the inland node, not the adjacent one). Twelve engine-inventory errors in one pass.

**Note.** This claim is the one WORLD entry in the spec that this audit positively supports, and it supports it strongly.

### C575 — OUT_OF_SCOPE

> §2.7 probe 2 settles pass 2's ordering.
>
> *DESIGN / stipulated / depends on C277*

**Method.** DESIGN.

### C576 — OUT_OF_SCOPE

> Everything in §2.7 is debugger-only.
>
> *DESIGN / stipulated / depends on C273*

**Method.** DESIGN.

**Note.** Not true as stated for at least four 2.7 items: probe 5 (C076/C232/C282), probe 6 (C283/C284/C538), probe 7 (C285) and probe 8 (C286/C567) are all settleable with a file edit and a node window, without a debugger. See the summary's unblocking table.

### C577 — OUT_OF_SCOPE

> Pass caching and income accumulation timing are the principal debugger-only unknowns.
>
> *DESIGN / stipulated / depends on C274, C278*

**Method.** DESIGN.

### C578 — OUT_OF_SCOPE

> `k`, `α_min` and `α_max` are unresolved parameters.
>
> *DESIGN / stipulated / depends on C040*

**Method.** DESIGN.

### C579 — OUT_OF_SCOPE

> The test for them is whether they produce the intended three-regime split.
>
> *DESIGN / stipulated / depends on C042, C044, C045*

**Method.** DESIGN.

### C580 — OUT_OF_SCOPE

> They are not meant to differentiate same-geography goods.
>
> *DESIGN / stipulated / depends on C440*

**Method.** DESIGN.

### C581 — OUT_OF_SCOPE

> Whether `α_min` ever bites is unknown.
>
> *DESIGN / stipulated / depends on C437*

**Method.** DESIGN (an open question).

**Note.** Now answerable from files: alpha_min bites only for goods with a negative `change_price` event, and 11 of 30 goods have none. See C435.

### C582 — DEFERRED

> The sublinear regime may be reachable only through price crashes.
>
> *OUTCOME / derivation / depends on C432*

**Method.** OUTCOME.

**Evidence.** Settled from files: yes for 13 of 30 goods, and *never* for the other 11 (cloves, cocoa, cotton, fur, ivory, naval_supplies, salt, sugar, tea, tobacco, tropical_wood), which have no negative price event in vanilla. See C435.

### C583 — CONFIRMED

> If it never engages in a full campaign, `P₀` is mis-set or the regime is inert.
>
> *MODEL / derivation / depends on C438*

**Method.** Derivation from C438; the disjunction is exhaustive.

**Evidence.** Valid, and C435 supplies the data to decide it: the regime is reachable but only through 30 named events covering 19 goods.

### C584 — OUT_OF_SCOPE

> ε must be small enough to be invisible against any real economy and large enough to decide dead branches against floating-point noise.
>
> *DESIGN / derivation / depends on C455*

**Method.** DESIGN.

**Note.** Now has a measured upper bound: at eps = 1e-3 the identity residual is 1.16e-2 and one of 159 edges already flips versus the eps=0 orientation; at eps = 1e-6 the residual is 1.15e-5 and no edge flips. See C462.

### C585 — OUT_OF_SCOPE

> AI merchant reassignment cadence is unresolved.
>
> *DESIGN / stipulated*

**Method.** DESIGN.


---

## §3.14

### C586 — CONFIRMED

> The two ends of a link never compete for goods.
>
> *MODEL / derivation / depends on C074, C075*

**Method.** Proof from C074/C075: the good sets `{g : n->m}` and `{g : m->n}` are disjoint by construction, since an edge has one orientation per good.

**Evidence.** Checked on 1444 data: for every link and every good, exactly one direction is emitted (`orient()` emits one tuple per edge per good; total emitted = 159 per good for all 29 goods).

### C587 — CONFIRMED (conditional)

> Competition stays between merchants at the same node, as in vanilla.
>
> *ENGINE / derivation / depends on C068, C586*

**Method.** Derivation from C068 (confirmed) and C586 (confirmed).

**Evidence.** `TRADER_ALLREADY_THERE:0 "Only one Merchant allowed at any node."` - competition is between the different countries' single merchants in the same node.

### C588 — CONFIRMED

> One survival-table precompute serves every country.
>
> *MODEL / derivation / depends on C591*

**Method.** Derivation from C591, confirmed.

**Evidence.** Valid.

### C589 — CONFIRMED

> For each good, a backward pass over its DAG gives `S_g[n][H]`, the expected fraction of a unit of `g` at `n` arriving at `H`.
>
> *MODEL / stipulated / depends on C009*

**Method.** Definitional, and implementable: the recursion is well-founded because the per-good orientation is a DAG (C009), so a reverse topological order exists.

**Evidence.** 29 of 29 live goods are acyclic on 1444 data, so the backward pass terminates for every good.

### C590 — CONFIRMED

> The backward pass multiplies through collection, steering shares, and the per-link multi-merchant boost.
>
> *MODEL / stipulated / depends on C589*

**Method.** Definitional.

### C591 — CONFIRMED

> All three of those inputs are country-independent aggregates.
>
> *MODEL / derivation / depends on C590*

**Method.** Checked each of the three inputs for a country index. `collected_share(n,g)` (C087) is a ratio of node-aggregate powers; the steering share (C092) is a ratio of node-aggregate steering powers; the per-link boost is `TRADE_ADDED_VALUE_MODIFER` applied per merchant on the link. None carries a country subscript in the aggregate.

**Evidence.** Confirmed as the same factoring that makes C521 work: the country index enters only through `powershare_C`, which is not one of these three.

### C592 — CONFIRMED

> Vanilla has a per-link multi-merchant boost.
>
> *ENGINE / file value / depends on C218*

**Method.** Read `common/defines.lua` line 1204 and the engine's own boost tooltips.

**Evidence.** `TRADE_ADDED_VALUE_MODIFER = 0.05`; `TRADE_ADDED_VALUE_COUNTRY:0 "$WHO$ increases outgoing value by: $VAL$%"`; `TRADEMAP_OUTGOING_BASE:0 "Before countries increase the outgoing trade value, $BASEVAL$ is leaving $FROMNODE$."` The plural "countries" and the per-country attribution confirm it is per-link and multi-merchant.

### C593 — CONFIRMED

> `collected_share(n,g)` reaches 1 at `g`'s sink, which terminates the recursion.
>
> *MODEL / derivation / depends on C086*

**Method.** Derivation from C086 and C009: at a sink `collected_share = 1`, so the recursive term is multiplied by `1 - 1 = 0`.

**Evidence.** Arithmetic; and every good's DAG has at least one sink (36 distinct sink nodes on 1444 data).

### C594 — PARTIAL

> The survival table is about 0.75 MB.
>
> *MODEL / derivation / depends on C159, C199*

**Method.** Computed the table's exact size on the 1444 solve (`t_model3.py`).

**Evidence.** `entries = 29 goods x 80 nodes x 80 homes = 185600`. At float32: `742400 bytes = 0.742 MB (0.708 MiB)`. At float64: `1484800 bytes = 1.485 MB (1.416 MiB)`. At the full 30 goods: 0.768 MB / 1.536 MB.

**What is actually true.** "About 0.75 MB" is right **only at single precision**. The rest of the solver is double precision - the spec's own tolerances (5.7e-14, 1.4e-14) are double-precision figures - so the natural implementation gives **1.5 MB**, twice the stated size.

**Spec text that must change.** "All three inputs are country-independent aggregates, so this is one table, not one per nation - about 0.75 MB, well under a million operations per solve." (spec.md, section 3.14)

**Blast radius.** C595 is unaffected (it is about operations, not bytes). Nothing else depends on the figure; it is a sizing note, but a doubling is worth getting right before it is used to argue the table is cheap.

### C595 — CONFIRMED

> Building it costs well under a million operations per solve.
>
> *MODEL / derivation / depends on C594*

**Method.** Counted the backward pass exactly (`t_model3.py`): for each good, cost is `|E| x N` multiply-adds, since each directed edge contributes one term for each of the 80 home nodes.

**Evidence.** `backward-pass multiply-adds = sum_g |E| x N homes = 368880`; `under one million: True`. At the full 30 goods it is 381,600 - still well under.

### C596 — OUT_OF_SCOPE

> Scoring reads the survival table for both steering and collecting.
>
> *DESIGN / stipulated / depends on C589*

**Method.** DESIGN.

### C597 — CONFIRMED

> The opportunity cost of collecting therefore falls out as the same comparison a human player makes by hand.
>
> *MODEL / derivation / depends on C596*

**Method.** Derivation from C596: reading one table for both options makes the comparison a single subtraction in the same units.

**Evidence.** Valid.

### C598 — CONFIRMED

> Denial scoring falls out of the same table evaluated against a rival's home node.
>
> *MODEL / derivation / depends on C589*

**Method.** Derivation from C589: `S_g[n][H]` evaluated at a rival's home node is exactly the denial quantity.

**Evidence.** Valid; requires no additional table.

### C599 — CONFIRMED

> The off-home penalty is a power modifier, not a haircut on value.
>
> *ENGINE / UNSOURCED / depends on C072*

**Method.** The engine's own main-port tooltip states the penalty's kind explicitly.

**Evidence.** `TRADEMAP_MAINPORT_DESC:0 "Your main trading port is where you collect your trade. You can collect in other place but there you will get a **trade power penalty**."` Corroborated by the define's placement among power terms (`TRADE_NON_CAPITAL_OFFICE = -0.50`) and by the existence of the countermodifier `reduced_trade_penalty_on_non_main_tradenode` (eu4.exe 0x02308fb4; `MODIFIER_REDUCED_TRADE_PENALTY_ON_NON_MAIN_TRADE_NODE` at 0x01cc1808), which is expressed as a modifier on the penalty rather than on income.

### C600 — CONFIRMED

> It reduces the country's trade power in that node.
>
> *ENGINE / derivation / depends on C599*

**Method.** Derivation from C599, and the same tooltip states it.

**Evidence.** See C599.

### C601 — CONFIRMED (conditional)

> The reduced power feeds both the collect/transfer ratio and the share among collectors.
>
> *ENGINE / derivation / depends on C087, C600*

**Method.** Derivation from C087 and C600; conditional on C099 for the collector-share half.

**Evidence.** Sound inference.

### C602 — CONFIRMED (conditional)

> So it lowers both the fraction retained in the node and the collector's slice of it.
>
> *ENGINE / derivation / depends on C601*

**Method.** Derivation from C601.

**Evidence.** Sound inference.

### C603 — CONFIRMED

> Scoring a collect candidate as `value × share × 0.5` is wrong.
>
> *MODEL / derivation / depends on C602*

**Method.** Arithmetic. `value x share x 0.5` applies the halving once, to the output. The correct computation applies it to power, which then enters two ratios.

**Evidence.** Worked example: node value 100, your raw power 50, other collectors 50, no transfer. Naive: `100 x 0.5 x 0.5 = 25`. Correct: halved power 25, so `P_collect = 75`, `collected_share = 1` (sink), your share `25/75 = 1/3`, income `33.3`. The naive figure is wrong by 25% in this case, and wrong in the *other* direction than intuition suggests.

### C604 — CONFIRMED

> The halving must be applied to power, with the two-stage formula run from there.
>
> *MODEL / derivation / depends on C603*

**Method.** Follows from C603.

**Evidence.** Same worked example.

### C605 — CONFIRMED

> This is why the off-home penalty falls out of the survival table: the table is built from power-derived shares.
>
> *MODEL / derivation / depends on C590*

**Method.** Derivation from C590: the table's inputs are power-derived ratios, so a power modifier propagates through them automatically.

**Evidence.** Valid.

### C606 — NEEDS_GAME

> The home-node bonus is voided entirely by placing any collector outside the home node.
>
> *ENGINE / UNSOURCED / depends on C216*

**Method.** The two home-bonus defines exist but nothing on disk states the voiding condition.

**Evidence.** `TRADE_POWER_HOME_BONUS = 0.1`, `TRADE_POWER_HOME_BONUS_MAX = 1`, internal identifier `transfer_home_bonus` (0x020df15c). The `_MAX` define suggests the bonus accumulates toward a cap rather than being a single on/off grant, which is *not* obviously consistent with 'voided entirely by placing any collector outside the home node'.

**Note.** Settling observation: with all merchants collecting at home, record the home node's trade power; move one merchant to collect elsewhere and re-read the home node figure. If it drops by the full bonus, the claim holds; if it drops partially, `TRADE_POWER_HOME_BONUS_MAX` is doing something the spec does not model. Setup: any save with two or more merchants. No debugger.

### C607 — CONFIRMED (conditional)

> So a collect candidate's true cost includes a penalty no single-merchant score can see.
>
> *MODEL / derivation / depends on C606*

**Method.** Derivation from C606, which is NEEDS_GAME.

**Evidence.** Sound inference.

### C608 — OUT_OF_SCOPE

> Running greedy twice — once all-steer with the bonus, once unconstrained without — and keeping the better portfolio handles that.
>
> *DESIGN / derivation / depends on C607*

**Method.** DESIGN.

### C609 — CONFIRMED

> Greedy scoring against a moving field can oscillate between AIs.
>
> *MODEL / UNSOURCED*

**Method.** Standard result, and directly demonstrable: best-response dynamics on a shared resource with simultaneous updates need not converge. The shared resource here is the node's power shares, which every AI's score reads and every AI's move changes.

**Evidence.** The structure is a congestion game with simultaneous best-response updates, for which two-cycles are the generic failure mode. No numerical experiment is needed to establish possibility; C610's damping claim is the one that needs measurement.

### C610 — DEFERRED

> Damping the shares between passes should hold the oscillation.
>
> *OUTCOME / UNSOURCED / depends on C609*

**Method.** OUTCOME.

### C611 — OUT_OF_SCOPE

> The prototype must verify the damping.
>
> *DESIGN / stipulated / depends on C610*

**Method.** DESIGN.

### C612 — OUT_OF_SCOPE

> Reassignment cadence is the one item left for the human to decide.
>
> *DESIGN / stipulated / depends on C585*

**Method.** DESIGN.

### C613 — CONFIRMED

> Merchants take travel time.
>
> *ENGINE / UNSOURCED*

**Method.** Read the merchant travel defines in `common/defines.lua` and the engine's arrival strings.

**Evidence.** `MERCHANT_SPEED = 20.0` (line 1196), `MERCHANT_TIME_DISTANCE = 0.25` (line 1182), and the engine strings `MERCHANT_ARRIVED`, `TRADE_ENROUTE`, `TRADE_ENROUTE_STATUS`, `TRADER_CHANGE`. A merchant has a speed, a distance-scaled time, an en-route state and an arrival event - travel time is real and parameterised.

### C614 — DEFERRED

> An AI re-optimizing every solve would leave its merchants permanently in transit.
>
> *OUTCOME / derivation / depends on C019, C613*

**Method.** OUTCOME.

### C615 — OUT_OF_SCOPE

> Mirroring vanilla's cadence is the stated preference.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C616 — CONFIRMED (and strengthened)

> The define governing vanilla's cadence was not located in the visible portion of any dump.
>
> *ENGINE / file value*

**Method.** The claim says the define was not found in the *visible portion of a dump*. I searched the **complete shipped `common/defines.lua`** (2744 lines) for every `MERCHANT` and every AI trade define, and separately searched the NAI and NAIEconomy sections.

**Evidence.** All `MERCHANT` defines in the file: `SLANDER_MERCHANTS_COST`, `SLANDER_MERCHANTS_DURATION`, `MERCHANT_TIME_DISTANCE = 0.25`, `MERCHANT_CHANCE = 0.35`, `MERCHANT_COMPETE = 0.5`, `MERCHANT_COMPETE_PERCENT_OWNED_BASE = 0.25`, `MERCHANT_SPEED = 20.0`, `MERCHANT_MAX_POWER_BONUS = 2.0`, `TRADE_MERCHANT_PRESENT = 0.1`, and two `DIPLOMATIC_ACTION_SLANDER_MERCHANTS_*` scores. **None governs reassignment cadence.** The NAI section's trade defines are all scoring weights (`TRADE_POLICY_*_SCORE`, `PEACE_TERMS_TRADE_POWER_*`, `DIPLOMATIC_ACTION_TRADE_*`); NAIEconomy has no trade entry at all.

**Note.** Stronger than the claim: the define is absent from the entire shipped defines file, not merely from a dump. `MERCHANT_CHANCE = 0.35` is the closest candidate by name and is worth checking, but its `_EDEF_MERCHANT_CHANCE_` comment gives nothing away.

### C617 — OUT_OF_SCOPE

> Mirroring therefore requires finding that define or measuring the cadence by observation.
>
> *DESIGN / derivation / depends on C616*

**Method.** DESIGN.

### C618 — OUT_OF_SCOPE

> The computed alternative moves a merchant when `(V_new − V_incumbent) × expected_tenure > V_incumbent × travel_time`.
>
> *DESIGN / stipulated*

**Method.** DESIGN.

### C619 — CONFIRMED

> `MERCHANT_SPEED` exists as a define.
>
> *ENGINE / file value*

**Method.** Read `common/defines.lua` line 1196; confirmed engine-referenced at eu4.exe 0x01c6e010.

**Evidence.** `MERCHANT_SPEED = 20.0,  -- MERCHANT_SPEED`.

### C620 — OUT_OF_SCOPE

> `expected_tenure` is endogenous and should be wired to the flip-rate measurement.
>
> *DESIGN / stipulated / depends on C618, C334*

**Method.** DESIGN.

### C621 — CONFIRMED

> Vanilla's cadence was tuned against a graph that never moves.
>
> *ENGINE / derivation / depends on C531*

**Method.** Derivation from C531/C533 plus the structural fact that the vanilla node file is static.

**Evidence.** Vanilla's graph is authored once in `common/tradenodes/00_tradenodes.txt` and never recomputed; `bidirectional pairs: 0`, `vanilla graph cycles found: 0`, and the file ships with a fixed topological order. Any cadence constant tuned against it was fitted to a graph that never moves.

### C622 — CONFIRMED

> Copying it would import a constant fitted to different dynamics.
>
> *MODEL / derivation / depends on C621*

**Method.** Derivation from C621.

**Evidence.** Valid.

### C623 — OUT_OF_SCOPE

> Computing the cadence overrides a stated preference.
>
> *DESIGN / derivation / depends on C615*

**Method.** DESIGN.

### C624 — CONFIRMED

> Node-to-node travel time still needs the game's distance metric.
>
> *ENGINE / UNSOURCED / depends on C618*

**Method.** Confirmed a distance metric exists and is exposed to the merchant system.

**Evidence.** `MERCHANT_TIME_DISTANCE = 0.25` (a distance-scaled travel time), `COLONIST_DISTANCE_DIVISOR = 1000`, `MISSIONARY_TIME_DISTANCE = 0.2`, `OVERSEAS_DISTANCE = 150`, `CONQUEST_INTEREST_DISTANCE = 100`. The engine has a distance metric and merchant travel already reads it; what the mod would need is *access* to it, which is a hooking question, not a question of whether it exists.


---

## §3.15

### C625 — OUT_OF_SCOPE

> Authored demand weights are rejected.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a rejection, i.e. a choice).

### C626 — OUT_OF_SCOPE

> They would be authored data in a model that needs none.
>
> *DESIGN / derivation / depends on C364*

**Method.** DESIGN.

### C627 — OUT_OF_SCOPE

> Trade income inside `wealth` is rejected.
>
> *DESIGN / stipulated / depends on C402*

**Method.** DESIGN (a rejection, i.e. a choice).

### C628 — CONFIRMED

> It would reintroduce flow → demand → orientation → flow circularity.
>
> *MODEL / derivation / depends on C403*

**Method.** Derivation from C403, confirmed.

**Evidence.** Same dependency-cycle argument.

### C629 — CONFIRMED

> The graph would then respond to merchants rather than to the world.
>
> *MODEL / derivation / depends on C404*

**Method.** Derivation from C404.

**Evidence.** Valid.

### C630 — OUT_OF_SCOPE

> Node-level α is rejected.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a rejection, i.e. a choice).

### C631 — CONFIRMED

> It would make demand concentration a function of how finely the map was sliced.
>
> *MODEL / derivation / depends on C409*

**Method.** Derivation from C409, confirmed - with the quantitative caveat from C407.

**Evidence.** The real spread is 19-77 land provinces, not 4-40; at alpha = 1.5 that still gives a 2.01x advantage to the coarsest slicing.

### C632 — OUT_OF_SCOPE

> A median-relative α anchor is rejected.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a rejection, i.e. a choice).

### C633 — CONFIRMED

> Under it, a good's concentration would shift because other goods changed price.
>
> *MODEL / derivation / depends on C429*

**Method.** Derivation from C429, confirmed by proof.

**Evidence.** Valid.

### C634 — OUT_OF_SCOPE

> α floored at 1 is rejected.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a rejection, i.e. a choice).

### C635 — CONFIRMED

> Flooring at 1 would discard the cheap-bulk regime.
>
> *MODEL / derivation / depends on C045, C436*

**Method.** Derivation from C045 and C436, both confirmed.

**Evidence.** Valid.

**Note.** Its practical weight is now measurable: the cheap-bulk regime is reachable for 13 of 30 goods and unreachable for 11. See C435.

### C636 — OUT_OF_SCOPE

> Production income as the aggregate supply term is rejected.
>
> *DESIGN / stipulated / depends on C420*

**Method.** DESIGN (a rejection, i.e. a choice).

### C637 — CONFIRMED

> It would make world supply depend on owners' idea groups.
>
> *MODEL / derivation / depends on C417*

**Method.** Derivation from C417, confirmed.

**Evidence.** Valid.

### C638 — CONFIRMED

> It would break the `Φ ≡ φ₀` identity for reasons unrelated to the solver.
>
> *MODEL / derivation / depends on C424*

**Method.** Derivation from C424, confirmed.

**Evidence.** Valid.

### C639 — OUT_OF_SCOPE

> A τ margin on orientation is rejected.
>
> *DESIGN / stipulated / depends on C443*

**Method.** DESIGN (a rejection, i.e. a choice).

### C640 — CONFIRMED

> A τ margin manufactures cycles.
>
> *MODEL / derivation / depends on C446*

**Method.** Derivation from C446, reproduced exactly.

**Evidence.** `A->B->C->A` at tol=1e-3 on `phi = {0, 0.0006, 0.0012}`.

### C641 — OUT_OF_SCOPE

> Uniform supply in the aggregate solve is rejected.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a rejection, i.e. a choice).

### C642 — OUT_OF_SCOPE

> It answers a question nobody asked.
>
> *DESIGN / stipulated / depends on C641*

**Method.** DESIGN.

### C643 — CONFIRMED

> It destroys the identity that makes `φ₀` worth computing.
>
> *MODEL / derivation / depends on C063*

**Method.** Measured: replaced phi0's supply with the uniform vector `1/N` and re-tested the identity (`t_model4.py`).

**Evidence.** Trade-value supply (as specified): `k = 3662.4000, rel.residual = 1.959e-15, orientation agrees 159/159`. Uniform supply: `k = -7244.7074, rel.residual = 2.456e+01, orientation agrees 58/159`. The scalar even changes sign. The identity is not weakened by uniform supply - it is gone.

### C644 — OUT_OF_SCOPE

> `φ₀` as the installed graph is rejected.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a rejection, i.e. a choice).

### C645 — CONFIRMED

> `φ₀` is not the economy the model runs.
>
> *MODEL / derivation / depends on C064, C501*

**Method.** Derivation from C064 and C501: phi0 uses alpha = 1 for every good by definition, which is not the model's alpha.

**Evidence.** Valid.

### C646 — OUT_OF_SCOPE

> A vestigial in-game economy with net treasury settlement is rejected.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a rejection, i.e. a choice).

### C647 — DEFERRED

> It would give correct treasuries but wrong displays and wrong AI inputs.
>
> *OUTCOME / derivation / depends on C514*

**Method.** OUTCOME.

### C648 — OUT_OF_SCOPE

> Per-good propagation is rejected.
>
> *DESIGN / stipulated / depends on C525*

**Method.** DESIGN (a rejection, i.e. a choice).

### C649 — CONFIRMED

> It breaks the income factoring and with it Goal 7.
>
> *MODEL / derivation / depends on C365, C527*

**Method.** Derivation from C527, reproduced.

**Evidence.** 0.81-ducat error on a 203-ducat node once power varies by good.

### C650 — OUT_OF_SCOPE

> Node-level collect/transfer rules are rejected.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a rejection, i.e. a choice).

### C651 — CONFIRMED

> The collect/transfer split is per good because whether a good has anywhere to go is per good.
>
> *MODEL / derivation / depends on C086, C088*

**Method.** Derivation from C086 and C088: `collected_share = 1` at a sink is a per-good condition, since sinks differ per good (C011).

**Evidence.** 36 distinct sink nodes across 29 goods on 1444 data, and no node is a sink for all of them - so 'has anywhere to go' is genuinely per good.

### C652 — OUT_OF_SCOPE

> Treating unsteered goods as fully collected is rejected.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a rejection, i.e. a choice).

### C653 — CONFIRMED

> Transfer power does not come from merchants.
>
> *ENGINE / derivation / depends on C089*

**Method.** Derivation from C089: the merchant-steering clause is one of two disjuncts, and the other (collecting downstream) has no merchant in it.

**Evidence.** Valid.

### C654 — CONFIRMED

> Full collection happens at a sink, which is a property of the graph.
>
> *MODEL / derivation / depends on C086*

**Method.** Derivation from C086 and C010: sinkhood is defined by out-degree in the good's orientation.

**Evidence.** Valid.

### C655 — OUT_OF_SCOPE

> Undirected shortest path as the primary fleet route is rejected.
>
> *DESIGN / stipulated / depends on C117*

**Method.** DESIGN (a rejection, i.e. a choice).

### C656 — CONFIRMED

> A geodesic over a directional structure can route a fleet against every arrow on the map.
>
> *MODEL / derivation / depends on C655*

**Method.** Constructed on the real graph: an undirected geodesic ignores orientation by definition, so it can traverse edges against Phi.

**Evidence.** Example on the vanilla graph: the undirected path from `english_channel` back to `malacca` is `english_channel - ivory_coast - cape_of_good_hope - malacca` (3 hops), every hop of which runs against the directed edges `malacca -> cape_of_good_hope -> ivory_coast -> english_channel`. A geodesic fleet route would sail the whole corridor backwards.

### C657 — OUT_OF_SCOPE

> Automatic per-good merchant targeting is rejected.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a rejection, i.e. a choice).

### C658 — CONFIRMED (conditional)

> One vanilla arrow click already achieves per-good resolution.
>
> *ENGINE / derivation / depends on C074*

**Method.** Derivation from C074, a design stipulation; and the vanilla per-link UI exists to click.

**Evidence.** `interface/tradeinterface.gui:17` `TradeNodeLink` with `NextNodeButton` - one clickable entry per link, in both the incoming and outgoing lists (C532).

### C659 — DEFERRED

> Automation would cost denial steering.
>
> *OUTCOME / UNSOURCED / depends on C598*

**Method.** OUTCOME.

### C660 — OUT_OF_SCOPE

> Companion-overlay merchant assignment is rejected.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a rejection, i.e. a choice).

### C661 — OUT_OF_SCOPE

> Assignment must stay a game action or vanilla knowledge stops transferring.
>
> *DESIGN / stipulated / depends on C067*

**Method.** DESIGN (a rejection, i.e. a choice).

### C662 — OUT_OF_SCOPE

> Emission-time pruning of near-flat links is rejected.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a rejection, i.e. a choice).

### C663 — OUT_OF_SCOPE

> Peripheral termini are intended consumption.
>
> *DESIGN / stipulated / depends on C383*

**Method.** DESIGN (a rejection, i.e. a choice).

### C664 — NEEDS_GAME

> The power-at-both-ends gate already withholds unworked corridors.
>
> *ENGINE / derivation / depends on C102*

**Method.** Derivation from C102, which is NEEDS_GAME.

**Evidence.** See C102.

**Note.** Note that the companion gate the spec pairs it with, supply range, does not exist (C101 REFUTED), so this rejection now rests on C102 alone.

### C665 — OUT_OF_SCOPE

> Edge conductance / a weighted Laplacian is rejected.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a rejection, i.e. a choice).

### C666 — OUT_OF_SCOPE

> A weighted Laplacian would add too much mechanical surface.
>
> *DESIGN / stipulated / depends on C665*

**Method.** DESIGN (a rejection, i.e. a choice).

### C667 — CONFIRMED

> The unweighted solve already routes correctly through conduits.
>
> *MODEL / derivation / depends on C378*

**Method.** Derivation from C378, confirmed by proof and by the synthetic conduit test.

**Evidence.** Five-node path: `phi = [2, 1, 0, -1, -2]`, every interior node exactly the mean of its neighbours, flow passes through.

**Note.** Caveat carried from C377: no vanilla node is a pure conduit (`pure conduits (b==0) tested: 0`), so on the vanilla map this is a statement about near-conduits, not exact ones.

### C668 — OUT_OF_SCOPE

> Staged delivery is rejected.
>
> *DESIGN / stipulated*

**Method.** DESIGN (a rejection, i.e. a choice).

### C669 — OUT_OF_SCOPE

> The intermediate states are different designs sharing a solver, not subsets of this one.
>
> *DESIGN / stipulated / depends on C668*

**Method.** DESIGN (a rejection, i.e. a choice).

### C670 — CONFIRMED

> The claim "the aggregate map is not a DAG" was an error.
>
> *MODEL / derivation / depends on C061*

**Method.** A self-correction internal to the spec; the corrected version (C061/C671) is confirmed.

**Evidence.** `aggregate Phi acyclic: True` on 1444 data.

### C671 — PARTIAL

> Net flow is the gradient of `Φ` and hence acyclic.
>
> *MODEL / derivation / depends on C060*

**Method.** Two different quantities are conflated here, and the spec's own section 3.9 says so.

**Evidence.** `Phi` is a potential and its **gradient orientation** is acyclic - confirmed (C061). But section 3.9 (C502, C508) establishes that **realised net flow is not the gradient of Phi**: a link can be oriented `n -> m` under Phi while realised net flow runs `m -> n`.

**What is actually true.** The gradient of Phi is acyclic; net *realised* flow is not the gradient of Phi and is therefore not guaranteed acyclic by this argument. What makes an installable single network exist is that the *installed orientation* (the Phi gradient) is acyclic - which is C061, and is enough.

**Spec text that must change.** "**\"The aggregate map is not a DAG.\"** An error. Net flow is the gradient of `Phi`, hence acyclic - which is what makes an installable single network exist at all." (spec.md, section 3.15)

**Blast radius.** C672. The conclusion (an installable single network exists) survives on C061 alone. But 'net flow is the gradient of Phi' contradicts section 3.9's own correction (C502: 'Delta Phi is *not* the net value crossing an edge'), so section 3.15 restates the error that section 3.9 retracts.

**Note.** This is a genuine internal contradiction between two sections of the same document, both written after the retraction they discuss.

### C672 — CONFIRMED

> That acyclicity is what makes an installable single network exist at all.
>
> *MODEL / derivation / depends on C062, C671*

**Method.** The conclusion holds on C061 alone, independently of C671's faulty premise.

**Evidence.** `aggregate Phi acyclic: True`; the emitted node file is therefore representable.


---

## §3.16

### C673 — OUT_OF_SCOPE

> The spec was reviewed adversarially over many rounds by two reviewers.
>
> *WORLD / UNSOURCED*

**Method.** WORLD - a claim about the project's own review history; not checkable from disk or from EU4.

### C674 — OUT_OF_SCOPE

> Every retraction on either side traced to a premise that entered through prose.
>
> *WORLD / UNSOURCED / depends on C673*

**Method.** WORLD - a claim about the project's own review history; not checkable from disk or from EU4.

**Note.** This audit is partial counter-evidence. Of the 21 refutations, several trace to *file values read wrongly* rather than to prose: C433 and C434 (grain and livestock base prices, both exactly half the true value), C407 (node sizes), C128/C130/C131 (threshold values read from `00_trading_policies.txt`). Those are not prose premises - they are file premises that were mis-read or read from an older patch. The section 3.16 rule ("nothing built on file values failed") does not hold up.

### C675 — OUT_OF_SCOPE

> Those prose premises included a community post, a wiki sentence read under the wrong heading, semantics inferred from a define name, and a forum thread title.
>
> *WORLD / UNSOURCED / depends on C674*

**Method.** WORLD - a claim about the project's own review history; not checkable from disk or from EU4.

### C676 — REFUTED

> Nothing built on adjacency data, file values, or the model's own equations failed.
>
> *WORLD / UNSOURCED / depends on C674*

**Method.** This audit is the counterexample set. Sorted every refutation and partial by the *kind* of premise that failed.

**Evidence.** Failures resting on **file values**: C037 (autonomy floors in `00_static_modifiers.txt`), C128, C129, C130, C131 (thresholds in `common/trading_policies/00_trading_policies.txt`), C433, C434 (base prices in `common/prices/00_prices.txt`), C542 (the caravan formula in `defines.lua` plus its own tooltip), C070 (the `TRADE_MERCHANT_PRESENT` comment). Failures resting on **adjacency / map data**: C407 (node member counts from `00_tradenodes.txt` - 19 to 77, not 4 to 40), C139 (no node-name references anywhere in scripted content), C541 (26 by flag vs 25 by derivation). Failures resting on **the model's own equations**: C462 (epsilon does *not* preserve the section 1.6 identity as the spec defines phi0 - residual 1.15e-5, not 0), C671 (section 3.15 asserts net flow is the gradient of Phi, which section 3.9 explicitly retracts), C456 (the reported dead-branch figures are internally inconsistent - a 1.24 spread cannot be double-precision residual), C594 (0.75 MB is a single-precision figure for a double-precision solver).

**What is actually true.** Claims built on file values, on adjacency data, and on the model's own equations all failed in this pass - at least fifteen of them. The failure mode is not confined to prose premises. Three distinct mechanisms show up: file values remembered from an older patch (C037's 75% autonomy floor is pre-Common-Sense), file values transformed and then reported as raw (C433/C434 are both exactly `price / P0`), and the spec's own algebra instantiated without checking the instantiation (C462).

**Spec text that must change.** "Every retraction on either side - without exception - traced to a premise that entered through prose: a community post, a wiki sentence read under the wrong heading, semantics inferred from a define name, a forum thread title. **Nothing built on adjacency data, file values, or the model's own equations failed.**" (spec.md, section 3.16)

**Blast radius.** C677, C679 and the section 3.16 evidence standard itself. The rule "trust the inference, audit the inputs" is still right, but its stated exemption is not: file values need auditing against the shipped patch just as much as prose does, and the model's own equations need instantiating and running, not just deriving. C561's "distrust prose-sourced premises" remains good advice and is now insufficient on its own.

### C677 — OUT_OF_SCOPE

> The rule is not that derivations are safe.
>
> *DESIGN / stipulated / depends on C678*

**Method.** DESIGN (a methodological statement).

### C678 — OUT_OF_SCOPE

> Two retracted claims were sound derivations resting on false premises about the map.
>
> *WORLD / UNSOURCED / depends on C674*

**Method.** WORLD - a claim about the project's own review history; not checkable from disk or from EU4.

### C679 — OUT_OF_SCOPE

> The standard is: trust the inference, audit the inputs, and treat any prose-sourced premise as provisional however much reasoning sits on top of it.
>
> *DESIGN / stipulated / depends on C674, C678*

**Method.** DESIGN (a methodological rule).

**Note.** This audit suggests amending it: audit the inputs *including the file values*, and re-read file values against the shipped patch rather than against memory of them. Five refutations here are stale or mis-read file values.

### C680 — OUT_OF_SCOPE

> The cautionary case is the propagation source condition.
>
> *WORLD / UNSOURCED / depends on C104*

**Method.** WORLD - a claim about the project's own review history; not checkable from disk or from EU4.

**Note.** Still carrying an uncorrected qualifier - see C104, where the engine's own tooltip adds "where it already has power".

### C681 — OUT_OF_SCOPE

> Both reviewers signed off on it as correct while defending it against the wrong error.
>
> *WORLD / UNSOURCED / depends on C680*

**Method.** WORLD - a claim about the project's own review history; not checkable from disk or from EU4.

### C682 — OUT_OF_SCOPE

> It was corrected only later to include ship propagation under its modifier.
>
> *WORLD / UNSOURCED / depends on C107*

**Method.** WORLD - a claim about the project's own review history; not checkable from disk or from EU4.

### C683 — OUT_OF_SCOPE

> §1.9 carries the corrected version.
>
> *DESIGN / stipulated / depends on C107*

**Method.** DESIGN.

**Note.** Section 1.9 does carry ship propagation (C107, confirmed), but see C104 for a second qualifier still missing from the same passage.

### C684 — OUT_OF_SCOPE

> Agreement between two reviewers is not verification.
>
> *DESIGN / stipulated / depends on C681*

**Method.** DESIGN (a methodological statement).

### C685 — OUT_OF_SCOPE

> A line can be confidently defended against one mistake while carrying another.
>
> *DESIGN / stipulated / depends on C681*

**Method.** DESIGN (a methodological statement).

