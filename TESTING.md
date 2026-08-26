# Live-game acceptance tests

What the implementer must see **in the running game** before the mod counts as working. This is
the playtest protocol; it complements, and does not replace, the reference-side battery
(`v6-owner-agnostic/scripts/`, spec §2.8) and the engine probes (spec §2.7). Tests marked ★ are
the core set — the mod is not done until every ★ passes.

**Environment**: EU4 1.37.5 (build `835bfdf8`), Windows/Steam, non-ironman, the stock 1444 start,
console available for the scenario tests. **Known-good 1444 constants to check against** (all from
the verified reference solve): `Φ_w` sinks = `{genua, hangzhou}`; `genua` in-arcs =
`valencia, tunis, ragusa, champagne, alexandria`; `english_channel` is the richest node and drains
to `genua` via `champagne`; 29 live goods; 2–8 sinks per good; coal produces nowhere.

---

## A. Load and attach

- **A1. Emitted file loads clean.** Start a 1444 campaign with the generated `00_tradenodes.txt`.
  PASS: zero `tradenodedefinition.cpp` declaration-order errors in the log, no crash, game plays.
  (A cycle hard-crashes the engine with `EXCEPTION_STACK_OVERFLOW` — §2.4 — so a successful load
  is itself the acyclicity check on the emitted file.)
- **A2. End flags match the solve.** PASS: exactly `genua` and `hangzhou` carry `end=yes` on the
  1444 emit; vanilla's `venice` end is gone.
- **A3. Round-trip preservation.** Diff the emitted file against vanilla's. PASS: only `outgoing`
  blocks (with their `path`/`control`), declaration order, and `end` flags differ — `members`,
  `location`, `inland`, `ai_will_propagate_through_trade` and unrecognized keys byte-identical.
- **A4. DLL attaches on this build only.** PASS: pattern scan succeeds on `835bfdf8` and the DLL
  refuses (with a clear message) on any other binary — §2.5's a-patch-is-a-new-binary rule.
- **A5. Cross-implementation orientation equality.** Dump the DLL's 30 orientations at the first
  tick and compare with the reference solve on the same start. PASS: **exact** match, every arc,
  every good, plus `Φ_w` — no tolerance (§2.8's primary end-to-end check).

## B. ★ Trade map mode — the aggregate view (`Φ_w`)

- **B1. ★ The map draws `Φ_w`.** Enter trade map mode. PASS: the arrows are the installed `Φ_w` —
  spot-check against the reference dump: no arrow leaves `genua`; five arrows enter it from
  `valencia`, `tunis`, `ragusa`, `champagne`, `alexandria`; `english_channel → champagne → genua`;
  `hangzhou` has no outgoing arrow.
- **B2. Node numbers are the per-good economy summed.** PASS: the map-mode node box shows total
  node value = Σ over all goods of the model's node values (÷12 monthly display); the node window's
  six fields (`incoming/local/total/outgoing/our_from_this/piracy`) all reconcile with the overlay
  to the ducat.
- **B3. ★ Both directions on every link.** PASS: every incident link on a node shows **two**
  directional value figures, each ≥ 0; no negative number appears anywhere in the trade UI, even
  on links where realized net opposes the drawn arrow (find one via the overlay's disagreement
  list — §2.8 predicts them at nodes with 3+ outgoing links and partial merchant coverage).
- **B4. Live local value equals the engine's own.** On tick one, before any steering changes
  settle: each node's **local** value equals what unmodded vanilla shows for the same node at the
  same date. PASS on all 80 nodes — origination is the engine's own `inject_g(n)` by construction
  (§1.8), so any mismatch is a read or ÷12 bug. (Total/incoming/outgoing legitimately differ —
  the routing changed; local must not.)

  **Measured 2026-08-26 (pgt_h3k, clean 1444 start, observer).** B3: in trade map mode every link
  carries two panels (the engine's forward panel plus the DLL's reverse panel built from the
  merchant table), each with its own >= 0 figure; E4's per-tick assertion reports
  `DISPLAYED-TOTAL=0` negatives on all 24 ticks. B1: relink installs Phi_w into the definition graph
  every tick (`[relink] applied: 2-3 links reversed`); the engine-list-vs-Phi_w equality check is
  the `[B1]` line (see below).

## C. ★ Merchant assignment on any link end

- **C1. ★ Tabs and buttons.** Open a node window. PASS: connected-node tabs across the top,
  incoming on the left, outgoing on the right, grouped by the active view's graph — and the
  assign-merchant button is present and works on **both** groups (§1.12; §1.7's incoming-entry
  change — today that entry only navigates, so this is the observable difference).
- **C2. ★ Assignment on a `Φ_w`-incoming edge steers the right goods.** Assign a merchant at node
  *n* on a link drawn *into* n. PASS: the merchant steers exactly the goods oriented **away from
  n** on that link (check the per-good views: those goods' outgoing split shifts to that link,
  winner-take-all if it is the lone steerer — §1.8); goods oriented the other way are untouched.
- **C3. Two ends, disjoint sets.** Put a merchant at each end of the same physical link. PASS:
  each steers only its own direction's goods; neither blocks the other (§2.8's two-way Atlantic
  corridor row).
- **C4. Assignment survives a flip.** Force a link flip (see F1). PASS: the merchant stays
  assigned to the link; only its active good set changes; no dangling state, no crash (§1.7;
  §2.7 probe 5).
- **C5. Caravan grant needs actual steering.** A merchant assigned to a link carrying zero goods
  in its direction gets no caravan power; the same merchant on a carrying link does (§1.7's added
  condition; fold §2.7 items 6 and 11 into this session — the recipient node question).

  **Attempted 2026-08-26 (pgt_h3q, seated as Castile, paused 23 Dec 1444).** Clicking the steer
  button on a Sevilla map panel produced the engine's own refusal tooltip -- "You can't steer where
  you Collect from Trade" -- and the handler at 0x13FD5F0 never ran (`[click]` count stayed 0):
  the button is disabled by the engine's collect rule before our prologue hook can see it. Both of
  Castile's 1444 merchants collect (Sevilla = home, Bordeaux), so C2 through the panel needs a
  TRANSFERRING merchant at a non-home node -- which is the player-side no-collect enforcement the
  user deferred ("worry about making the game steer only later"). C1/C2 are blocked on that, not
  on the hook. The AI path (G1) already exercises the same table + syncrec representation the
  click writes. C1 as observed in the same session: the Sevilla window shows its three Phi_w-outgoing
  tabs named (Valencia, Tunis, Safi) and its two incoming tabs as "?????" -- the incoming group's
  names do not resolve through relink's rebuilt incoming lists. DEFECT, open. Narrowed 2026-08-26:
  with `pgt.RELINK` absent (vanilla lists, before any rebuild) the same window names them
  (Ivory Coast, Caribbean), so the label is read from something relink's step 2/3 does not carry
  over -- not the def pointer (LISTDUMP resolves those) and not the def key. Next probe: dump the
  raw 0x78-byte outgoing entries and the def incoming vectors of sevilla before and after
  relink::apply and diff them field by field.

  **C2 MEASURED 2026-08-26 (pgt_h3v, seated as Castile, no-collect enforced).** With the sweep
  having flipped the Bordeaux merchant to transfer, clicking the steer button of the reverse panel
  at bordeaux for the Phi_w link ivory_coast -> bordeaux: `[click] steer_button #1 (REVERSE view)`,
  `player country#185 assigned a merchant at bordeaux to steer the REVERSE end toward ivory_coast`;
  the engine accepted its own command (tooltip "We are currently steering trade towards Ivory
  Coast", Castile shield drawn under that panel at once). Next tick the per-good split at bordeaux
  (`pgt.SPLIT`) shows `country#185 power=2 collects=no steers_to=ivory_coast`; Castile is ELIGIBLE
  on exactly the goods oriented bordeaux -> ivory_coast (glass, iron, naval_supplies, salt, wine,
  wool: e.g. iron -> ivory_coast 0.189 vs st_lawrence 0.401 = its 2/(2+4.24) power share against
  the two st_lawrence steerers) and on none of the goods oriented the other way (cloth, fish,
  grain, livestock send nothing to ivory_coast). `[flow] bordeaux -> ivory_coast 0.0064`
  ducats/month. PASS. (C1: the button that works on both groups is the MAP PANEL steer button;
  the node window's incoming tabs remain vanilla -- unnamed here, see above, and buttonless.)

## D. ★ Per-good view

- **D1. ★ Click a province, get its good's network.** Click a cloves province. PASS: province
  colouring switches to the vanilla trade-goods rendering for cloves and the arrow layer redraws
  as **cloves' graph** — different from `Φ_w` (spot-check against the reference dump; cloves has a
  single source node, `the_moluccas`). Clicking the node icon returns to the aggregate view.
- **D2. ★ Per-good numbers in the same widgets.** In that view: PASS — the node box and all six
  window fields show **that good's** figures alone; each edge shows one direction only (a per-good
  graph orients every edge one way) with that good's realized flow on it.
- **D3. ★ Sinks visible per good.** PASS: a sink for the selected good is a node with **no**
  outgoing arrow in that view (2–8 per good), and its window shows `collected_share = 1` — the
  full incoming value collected, none forwarded (§1.8).
- **D4. The decomposition sums.** For at least three nodes (one rich hub, one conduit, one
  sink): sum a field across all 29 per-good views. PASS: equals the aggregate view's figure for
  that field to the ducat (swap-on-view is a display of one economy, not 29 separate ones).
- **D5. Conduit behaviour.** `cape_of_good_hope` (zero local production at 1444): PASS — nonzero
  through-flow on most goods' views (28 of 29 carry flow through it on the reference; `paper`
  routes none), local value 0.

  **Measured 2026-08-26 (pgt_h3k).** Selecting cloves through the `pgt.VIEW` harness: the arrow
  layer re-orients 74 of 159 links away from Phi_w (`[arrows] view=cloves ... re-oriented 74 drawn
  routes`), every European panel reads 0.00, and nonzero cloves flow radiates only from
  the_moluccas (1.5 / 0.31 / 0.29 leaving it; 0.2 / 0.02 at malacca; 0.01 philippines) -- the
  single-source spot-check. RESIDUALS: (1) the player-facing province-click trigger and the
  trade-goods province colouring are not built -- the view is selected by marker only; (2) in the
  per-good view each link showed both panels, the reverse one reading 0.00, where D2 asks for
  one direction only -- FIXED 2026-08-26 (pgt_h4a): the reverse-panel augmentation is gated on the
  aggregate view; in the cloves view the layer rebuild adds no reverse panels (revpanel logs
  nothing) and on return to the aggregate view it adds the 159 again; (3) D3 is logged per view
  (`[D3] view=cloves sinks=3 with collected_share==1: 3`).

## E. ★ Monthly ticks — the money is right

- **E1. ★ Country income matches the model, every month.** Run 12 monthly ticks. Each month, for
  at least five countries of different sizes (e.g. Castile, Venice, Ming, a one-province minor, a
  steppe horde): PASS — ledger trade income = `powershare_C(n) · collect_pool(n)` summed over the
  country's collecting nodes, to the ducat, matching the overlay's per-good breakdown (§2.6/§3.10
  identity; §2.8's economy-tab row). Any drift compounding month over month is a write-window bug.
- **E2. ★ Treasury reconciliation agrees with the display.** At each month boundary: PASS — the
  income the treasury actually books equals the displayed trade income from during the month
  (§2.6's two deadlines; §2.7 probe 3's question, answered by observation).
- **E3. World total tracks vanilla — with a null run.** Record 12 months of world collected trade
  income modded and unmodded from the same start, **plus a second unmodded run** (the null:
  vanilla differs from itself run to run — 49/80 nodes, up to 8.96%, §2.8). PASS: the
  modded-vs-vanilla gap is explainable by steering/routing differences and is not persistently
  larger than the null spread, and the **distribution across the historical great powers** stays
  plausible — distribution is the gating metric (§2.8).
- **E4. Nothing NaNs, nothing leaks.** Over the same 12 ticks: no negative collected income, no
  node value exploding or draining to zero without cause, no good's world value appearing from or
  vanishing to nowhere (conservation is asserted per tick — §2.8 — this is its visible face).

  **Measured 2026-08-26.** E1, E2 and E4 all run from the pass-10 wrapper's last node -- inside the
  same monthly pass, after every record is paid; the earlier worker-thread read after Sleep(400)
  raced the pass (measured 3.8 s with the booking log on) and read half-paid records.
  - E1: **662/662** countries agree, worst |diff| 0.002 ducats.
  - E2: **662/662** countries, worst |diff| 0. Basis corrected: `country+0x68` is NOT the trade income
    accumulator (it moved 0.25 while 8.69 was booked to Ming); the test now compares the engine's own
    category-2 `AddDelayedIncome` bookings (both pass-10 call sites logged, `pgt.BOOKLOG`) against
    SUM rec.money. Booked == computed, to the cent, for every country.
  - E4: CLEAN every tick.
  Run: `touch dllbuild/pgt.AI dllbuild/pgt.BOOKLOG; bash run.sh <dll> 3`; read `[E1]`, `[E2]`, `[E4]`.

## F. Reorientation and responsiveness (console scenarios)

- **F1. A flip is honoured end to end.** Pick a near-balanced link (§2.8), nudge development via
  console until it flips at the next tick. PASS: arrows, node windows, propagation and value all
  rebuild around the new direction within that tick — no one-month corridor lag, no tooltips
  disagreeing with arrows, no propagation crediting the wrong side (§2.7 probe 1's staleness
  instrumentation, run as an acceptance test).
- **F2. Razed China moves the end.** Console-zero `hangzhou`-node development. PASS: next tick
  the `Φ_w` ends are `{genua, gulf_of_siam}` and `hangzhou` keeps no end (§2.8's measured row).
- **F3. Owner changes move nothing day-of.** Tag-switch/annex a rich province (or strip Ming's
  mandate). PASS: the orientation is unchanged on the day it happens — demand reads the place,
  not the owner (§1.3; §2.8's Mandate row). The money moves only as devastation/development do.
- **F4. War bites through devastation.** Fight a war in China; watch corridors shift while
  devastation is up and revert as it heals (§2.8). PASS: direction responds to the world, on the
  monthly cadence, with no hysteresis artifacts (no cycle ever appears — §3.6).
- **F5. Price crash spreads a market.** Console a `change_price` crash on grain (reachable to
  0.625). PASS: α drops below 1 and grain's sinks visibly de-concentrate toward populous regions
  (§1.4, §2.8).
- **F6. Devastation scaling (probe 18).** At the stock start read `goods_produced` in the Bohemia
  (50) and Erzgebirge/Moravia (20) windows. PASS: the `-2 × level/100` law holds linearly through
  both points — this closes the one §1.3 scaling that rests on community documentation.

## G. AI

- **G1. AI uses reversed edges.** Observe AI merchant placements over a few years. PASS: AIs
  place merchants on `Φ_w`-incoming link ends where per-good flow justifies it (§3.14's candidate
  enumeration is link-ends, both tab groups) — at minimum, chain placements appear along
  high-value per-good corridors, not only along drawn arrows.
- **G2. No oscillation.** PASS: AI merchants settle under damping rather than thrashing between
  candidates every month (§2.8's convergence row; §3.14's cadence question resolved one way or
  the other and recorded).
- **G3. The world still runs.** Observer game to 1600. PASS: New World colonization proceeds at
  roughly vanilla pace, AI light ships still get built, trade leagues still form, no AI budget
  collapse traceable to trade income (§2.8; §3.10's readers).
- **G4. Direction-gated diplomacy is unblocked.** PASS: trade-conflict CBs, sell-province and
  treasure-fleet interactions never refuse on upstream/downstream grounds (§1.10 gates evaluate
  true); treasure fleets are always granted and route by the §1.10 ladder with privateers
  skimming en route (§1.11, §3.12).

  **Measured 2026-08-26 (commit 981ddb5+), clean 1444 start, 24 monthly ticks, vanilla's merchant AI
  silenced (aisilence.h), ours dispatching through the engine's own 0x3BAD90:**
  - G1: 716 AI placements, **192 (26%) on Phi_w-INCOMING ends** -- the tab group vanilla cannot
    express. Offline (impl/aitest.exe on the same save): Ming's top two picks are hangzhou->beijing
    and xian->beijing, both reverse ends toward home.
  - G2: **worst churn on any (country, node) = 0 target changes over 21 ticks**; 516 of 527
    placements still hold their node; dispatch settles at ~3 per tick once the plan is satisfied.
  - E1 636/636 countries agree (worst 0.0019 ducats), E4 CLEAN throughout.
  Run: `touch dllbuild/pgt.AI; bash run.sh pgt_sil2.dll 4`; read `[G1]`, `[G2]`, `[envoy] ... still hold one`.

  **Measured 2026-08-26 (pgt_h3t, commit 684d630+, 10 ticks).** RECALL: a posted merchant standing
  off its plan is re-placed on a planned node when that node beats it by x1.5, victims and
  candidates scored on the same network (home + standing + planned), dwell keyed on the last tick
  a node was sent to or recalled from, at most 2 recalls per country per tick. 24 recalls landed,
  16 refused by the x1.5 test; every recalled envoy still at its target 1 and 3 ticks later
  (23/0, 20/0); the engine clears the old record and detaches the old construction itself.
  G1 232 of 832 placements (27%) on Phi_w-INCOMING ends; G2 worst churn 0 target changes; 593 of
  600 sent-to nodes still hold a merchant (1 lost, 6 vacated by our own recall); E1 660/660; E4
  CLEAN. The human is excluded from step and dispatch. Cadence (spec 3.14, reserved for the user):
  the working default -- computed gain x1.5 plus a 3-month dwell -- fires 1-3 times per tick
  world-wide, i.e. rarely, as the prior expected.

  **Measured 2026-08-26 (pgt_h3z, 11 ticks, no-collect v2).** Vanilla parks a collecting merchant
  at every AI country's own trade capital at the 1444 start (573 of them); under the rule they are
  worth nothing there and are the first recall victims: 573 -> 8 over 11 ticks, 644 recalls landed,
  every one still at its target 1 and 3 ticks later (624/0, 540/0). G1 494 of 1437 placements
  (34%) on Phi_w-INCOMING ends; G2 worst churn 0 target changes; 1160 of 1213 sent-to nodes hold
  (3 lost, 50 vacated by our own recall); E1 657/657; E4 CLEAN. The sweep converts 38 save-start
  collectors on tick 1 through the OUTER SetTrader (engine-scored steer ordinal), 0 fail to land;
  4 merchants collect at the two Phi_w END nodes (genua 3, hangzhou 1) where the engine has no
  link to steer along -- the model now agrees with the engine about them (install.h: collects =
  has_capital || (has_trader && type == 0)); the plan never stands a merchant at such a node.

## H. Determinism, saves, performance

- **H1. Tick determinism live.** Save, note the full orientation, reload, tick. PASS: identical
  orientation, bit-for-bit (§2.8). Repeat across a game restart (separate process).
- **H2. Mid-campaign load.** Load a save mid-campaign. PASS: runs on the start-date file for at
  most one month, then the monthly solve takes over cleanly (§2.4).
- **H3. Tick cost.** PASS: the monthly tick's added time is imperceptible against vanilla's own
  monthly work — the solve budget is ~0.1 s even on the Python reference (§2.2), so any visible
  hitch is an implementation defect, not a design cost.
  **Measured 2026-08-26.** Vanilla's own monthly stall with the DLL idle: 87-98 ms worst frame gap.
  With the mod: 174-236 ms (was 300-350 before the per-tick VirtualQuery cache, which turned
  ~16,000 validate_region calls into ~290 syscalls). Tick profile (ms, cumulative): standings 6,
  routed 30, orient 46, flowmat 50, AI 61, dispatch 74, incoming 96, linkvalue 100, aggregate 117.
  Perceptible at speed 5; the remaining cost is routing 29 goods (~25 ms), relink (~16 ms) and the
  aggregate write (~20 ms). NOT PASSED yet by the "imperceptible" wording.
- **H4. Long-run soak.** Hands-off observer run, 1444 → 1600, autosaves on. PASS: no crash, no
  save corruption, no monotonic drift in world trade value beyond what development growth
  explains.

## I. While you're in there — open probes worth folding into these sessions

The playtest sessions above can settle most of §2.7's open probes at near-zero extra cost:
probe 1 (F1), 3 (E2), 4 (write one negative link value; watch rendering and protect-trade), 5
(C4), 6 and 11 (C5), 8 (double `TRADE_PROPAGATE_THRESHOLD`, check the raw requirement), 17 (near
and far propagation pairs for one country), 18 (F6), 19 (find a link where the receiving side
holds power at one end only; watch whether transfer arrives — the round-5 statistical record and
its three exception links are in `docs/audit/`, §2.7 item 19 names what the probe must explain).
Record results against the probe numbers so the spec's §2.7/§2.9 open counts can be closed.
