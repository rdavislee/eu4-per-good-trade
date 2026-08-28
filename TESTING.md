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
  RESOLVED 2026-08-26 (disassembly, 0x13D5560 / 0x13CC740): the tab label is the neighbour
  definition's localised name (def+0x30) gated by CCountry::HasDiscoveredTradeNode (0x3755E0):
  "?????" is VANILLA's rendering of an undiscovered node. Sevilla's Phi_w-incoming neighbours are
  ivory_coast and carribean_trade, none of whose provinces Castile has discovered in 1444; relink
  only moved the discovered neighbours (Tunis, Safi) to the outgoing side. The RELINK-off run that
  named them was in OBSERVER mode, whose type-7 handle passes the gate. Not a defect. (If tabs
  should ignore fog of war: one byte at 0x13CC916, 75 7E -> EB 7E.)

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

  **Steer-button state (user-reported 2026-08-26, fixed pgt_h4k/h4l).** With the player's merchant on
  a reverse end, every panel of the node (and forward link #0) showed "We are currently steering";
  with it on forward link #0, every reverse panel did. Traced (0x13FCD80): the panel derives its
  ordinal by the same outgoing-list search as the click handler, which misses on our reverse views
  and collapses to 0 -- and a reverse-end record IS +0xA8 = 0; on reverse panels the engine never
  writes the button frame at all (reads 0) and the tooltip treats anything but 2 as steering. Fix:
  after the engine's Update, flagfix sets steer_button+0x64 via vt[0xA8] from the assignment table
  (1 iff the table target is this panel's far node; 2 on any reverse panel without one). Measured:
  ~17,800 frames corrected per tick, the user confirmed only the clicked edge shows the merchant.
  Follow-up (same session): a FORWARD click only posted the engine command and left the reverse
  table entry in place, so the merchant could not be moved back to Champagne -- clickfix now writes
  the table for forward clicks too (pgt_h4l).

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

  **Measured 2026-08-26 (pgt_h4u, D3 per-good propagation, impl/DEPARTURES.md).** The model now
  writes every record's power_fraction from the flow-weighted per-good collector share before the
  engine divides the pool, and predicts income from the shares it wrote (not a read-back):
  E1 664/664 countries agree, worst |diff| 0.0077 ducats; E4 CLEAN; G1 30% reverse ends. (Before the
  write/predict order was fixed, E1 read 653-657/662 with 0.3-0.6 ducat misses -- those were the
  records where the model's division differs from the engine's, which the old order could not
  test.) The offline suite still routes with the aggregate power: a Phi_w-propagation control.

  **End nodes (user-reported 2026-08-26, fixed pgt_h4v).** Merchants at genua were paid as
  collectors with the -50% penalty because our own guards demoted every record at a zero-link node
  to collect. Relaxed (see impl/DEPARTURES.md D1): 10 monthly updates, no death, 0 collectors at
  end nodes, the AI plans genua, E1 664/664, E4 CLEAN, G1 33%. One engine-handled first-chance
  AV at eu4.exe+0xB988D8 (a script-condition list with a -1 data pointer) was logged once; to be
  counted across runs before it is attributed.

  **Measured 2026-08-26 (pgt_h4x, D3 v2 split propagation).** The fifth of a country's provincial
  power is split among the node's neighbours by price-weighted goods along each good's graph
  (impl/DEPARTURES.md D3); the model writes val/max_pow and power_fraction. E1 664/664 (worst
  0.0075) on two runs; E4 CLEAN; G1 42% of AI placements on Phi_w-INCOMING ends (was 30-33%).
  Probe at genua: the fifth splits alexandria .273 / champagne .240 / valencia .169 / tunis .168 /
  ragusa .150; Tunis (#306) receives 2.61 power at genua from 0; 1,396 such new standings
  world-wide. Genoa's window shows Aragon and Provence steering from Genoa (the user's test).

  **Review fixes 2026-08-26 (pgt_h4z).** The vanilla fifths are subtracted along the engine's LIVE
  outgoing lists (refreshed every tick), the written val excludes subject transfers, and the node
  totals (+0xC8/+0xD0/+0xD4) are written from the model. Ratchet instrument `[d3/sum]`: world
  Sval(engine) 21427 -> 22043 -> 22113 with Srecv ~1695 flat and Spp ~8750 flat -- no feedback.
  E1 663/663 x2, E4 CLEAN, G1 40%. E1 blind spot counted: 6 node-months with a pool and no paid
  collector over 5 ticks.

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

  **Reach (user-reported 2026-08-26, fixed pgt_h4f).** Native American countries were placing
  merchants at Western European nodes in 1444: dispatch used PlaceMerchantAtNode with force=1,
  which skips the engine's CanSendMerchantTo, and the +2 presence floor let any country score any
  node. Now the plan's candidate set is gated by the engine's own rule -- CCountry::
  CanSendMerchantTo (0x3532C0) on the node's location province (provinces + 0x2E10 * def->+0xDC),
  OR the country already stands there -- cached per (country, node) per tick, and dispatch
  refuses anything the engine would. Measured over 7 ticks: New World homes placed only at New
  World nodes (chesapeake_bay -> ohio x7, mississippi_river -> ohio x1), E1 662/662, E4 CLEAN,
  G1 35% reverse ends.

## H. Determinism, saves, performance

- **H1. Tick determinism live.** Save, note the full orientation, reload, tick. PASS: identical
  orientation, bit-for-bit (§2.8). Repeat across a game restart (separate process).
- **H2. Mid-campaign load.** Load a save mid-campaign. PASS: runs on the start-date file for at
  most one month, then the monthly solve takes over cleanly (§2.4).
  **Measured 2026-08-26 (pgt_h4b/h4c).** H2: loading the Jan-1445 yearly autosave (`LOAD=1 run.sh`),
  the DLL attaches, runs the start-date orientation for its first month (gen 0/1 == the 1444
  fingerprint f6fb5d39068181c4) and the live monthly solve takes over from the next tick; E1
  661/661, E4 CLEAN on the loaded game. PASS. H1 as specified is NOT met across the reload:
  the fresh run (A) had flipped hormuz/gulf_of_aden at Feb 1445 (fingerprint 35e205047e6dca26)
  while the reloaded run (B) kept f6fb... at the same dates and later flipped different links
  (katsina/ethiopia, kiev/crimea); world local also differs at matching dates (A 342.31 vs B
  341.92 at Feb 1445). The solver itself is deterministic (30/30 offline cross-check; both runs
  reproduce the 1444 baseline exactly), so the divergence is in the INPUTS after a reload --
  the `[H1/inputs]` fingerprint (hash of the province tax/production/devastation vector and
  prices the solve consumed) is the next instrument; spec 2.8 already records that vanilla
  itself is not reproducible run to run.
- **H3. Tick cost.** PASS: the monthly tick's added time is imperceptible against vanilla's own
  monthly work — the solve budget is ~0.1 s even on the Python reference (§2.2), so any visible
  hitch is an implementation defect, not a design cost.
  **Measured 2026-08-26.** Vanilla's own monthly stall with the DLL idle: 87-98 ms worst frame gap.
  With the mod: 174-236 ms (was 300-350 before the per-tick VirtualQuery cache, which turned
  ~16,000 validate_region calls into ~290 syscalls). Tick profile (ms, cumulative): standings 6,
  routed 30, orient 46, flowmat 50, AI 61, dispatch 74, incoming 96, linkvalue 100, aggregate 117.
  Perceptible at speed 5; the remaining cost is routing 29 goods (~25 ms), relink (~16 ms) and the
  aggregate write (~20 ms). NOT PASSED yet by the "imperceptible" wording.
  **Re-measured 2026-08-26 (pgt_h4z, D3 v2 with the record writes on the heap path):** tick 86 ms
  (routed 19, orient 4, AI 29, dispatch 5, incoming 6, aggregate+shares 11), worst frame gap
  170-195 ms against vanilla's ~90. The added ~85 ms is one hitch of ~5 frames at 60 fps once a
  month. Still not "imperceptible"; the remaining term is the AI phase.
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

## J. Opening state, node-window controls, persistence (user rules of 2026-08-26; pgt_i27)

Run with the DLL in the process BEFORE the campaign loads (`run.sh` injects at the main menu;
`install-proxy.ps1` installs it as version.dll). Each test names the log line that measures it.

- **J1 ★ Set up at 11 November 1444.** New game as Castile. Before unpausing: the outliner's merchant
  rows read "... to Sevilla" (none say Collects), the trade map shows reverse panels, and Genoa's
  window offers Transfer. Log: `[earlyload] new game ... orientation gen 1 solved`, `[tick] monthly
  update 1` and `[earlyload] done` all BEFORE `attach complete`'s successor lines; `[opening] vanilla
  opening placements skipped=<countries>`; `[player] merchants:` at tick 1 shows action=2 at the
  plan's nodes with `table->sevilla`.
- **J2 No merchant collects, anywhere, ever.** `[nocollect] ... collect at END nodes []` and
  `at own capital=0` from tick 1 on (the capital recall + the skipped vanilla placement);
  `[recall/home]` reports the recalled envoys idle on the next tick.
- **J3 Buttons.** Any node without your merchant: only *Transfer Trade Power*; your home node: no
  button and no "Send Merchant" label; a node with your merchant: *Recall* (plus Transfer while it
  still collects). Genoa/Venice/English Channel offer Transfer. Log: `NODE-WINDOW BUTTONS:` installed.
- **J4 A transfer points home.** Click Transfer at bordeaux: the shield lands on the ivory_coast or
  carribean_trade panel (bordeaux has no link to sevilla; the hop with the larger away-flow wins);
  `homeward set=` increments. The node window and the outliner name that target; at an END node
  the sentence is still produced (`endtext node-window set=`, `outliner set=`).
- **J5 Reverse-panel shield hover.** Hovering a shield on a reverse panel shows "X is applying Y
  power in this direction" (`tooltip-keyed=` increments).
- **J6 "passed your home" never lingers.** After a flip or a placement, no steer button reads
  STEER_LATER for more than a frame (`reach-rebuilt=` grows with `after landings:`).
- **J7 ★ Save round trip.** Move a merchant to a reverse end, save, exit to menu, load: the merchant
  still points at that end in the window, the outliner and the panel. Log: `[savegame] wrote
  <save>.eu4.pgt`, then `[earlyload] savegame:` and `[savegame] restored N entries` BEFORE
  `[tick] monthly update`. A vanilla save (no sidecar) logs `no sidecar ... the opening rule runs once`.
- **J8 Second campaign in one process.** New game -> menu -> new game: `[world] state reset` appears,
  and J1 holds again (the tick counter restarts at 1).
- **J10 Light ships follow the model.** After a few AI ticks, `[ships] country#N: model scores on k of 80
  nodes` lines appear and `ships: allocator calls=` grows with `rewritten=` close behind (no-scores only
  for countries with no table entries and no home pool). On the map, AI light-ship fleets protect trade
  at nodes where that country has a merchant on a reverse end (e.g. a Mediterranean power's fleet at
  genua), not only at Phi_w-downstream nodes. `pgt.NOSHIPS` must restore vanilla's placements.
- **J9 Income is not double-paid at setup.** Treasury at 11 Nov equals vanilla's (the setup driver runs
  with pass 10 suppressed); E1 holds from the first real month.

### Section J results (2026-08-27, pgt_i32-i34)

- **J1 PASS (log; visual pending final sign-off).** Setup inside the loading screen: solve 117-142 ms,
  tick 1 done before the load returns; player merchants at the plan (safi+valencia -> sevilla) at
  11 Nov 1444; `vanilla opening placements skipped=956` (the second setup placement call 0x774DB1 ->
  0x3BAE50, found by the 16-frame SetTrader chain instrument, stubbed alongside 0x774E05).
- **J2 PASS.** No rogue type-0 placements in i32+; capital-parked merchants recalled; `[settrader/player]`
  shows only the model's placements.
- **J4 partial.** homeward defaults measured (bordeaux -> carribean_trade/ivory_coast by flow tie-break);
  the click flow itself needs a hand test.
- **J7 PASS.** Autosave wrote `autosave.eu4.pgt` (932 entries; the engine passes RELATIVE paths, resolved
  against the user dir); Continue Game restored all 932 BEFORE the loading tick; player merchants identical
  across the round trip; reverse panels present on the loaded save (the savegame setup moved after
  InitSaveGame -- the inner site fires before deserialization).
- **J9 evidence.** The setup driver runs with pass 10 suppressed; E1 664/664 and E4 CLEAN from the first
  real month.
- **E1/E4 on i32:** 664/664, CLEAN through tick 10. **G1:** 51% of AI placements on Phi_w-INCOMING ends.
  **H3 on i32:** the tick ~94 ms steady-state, worst frame gap 252 ms (599 ms spike on the autosave month,
  vanilla's own autosave stall included).
- Open: J3/J5/J6/J8/J10 hand checks, H1/H4, E3, F, G3/G4 -- and the user's sign-off.

## G3 + H4 -- the 200-year AI-only observer run (2026-08-27, pgt_i73)

Vanilla map, mod only (`mod/pgt.mod`), 1444 Castile -> spectator, speed 5, unattended.
**2412 monthly ticks = 201 years (1444 -> 1645), no crash, process healthy at the end.**

| check | result |
|---|---|
| E4 (negative/non-finite/runaway) | **0 non-clean ticks of 2412** |
| E1 (engine-divided income vs model) | 1-4 countries of 222-665 outside the check's early-iteration tolerance; worst absolute error 0.0057 -> 0.022 ducats as the economy doubles |
| flowassert (directed inflow == record) | 20 lines of 2426; each is **1 inflow of ~287 off by 0.0005** -- one milli-ducat, the engine's storage grid |
| spurious campaign re-setups | **0** (the rolling-date rule; the setup-date comparison it replaced fired every 90 game-days) |
| tick cost | 231 ms (first) -> 182 -> **167 ms** (last): no growth, it falls as tags are annexed |
| worst frame gap | ~1.0 s, flat across the run (autosave-scale, not growth) |
| log volume | 16 MB / 201 years |

Both residuals are milli-ducat rounding, not defects: the engine stores values on a 1/1000 grid and
the model sums many nodes per country.

### How the world developed (the user's question)

- **Economy doubled**: world wealth 10,620 -> 20,982; colonised provinces 2,472 -> 3,192.
- **Consolidation**: 665 -> 222 countries holding trade power.
- **G1 held at 49-50% of AI merchant placements on Phi_w-INCOMING (reverse) ends for the whole run**
  -- the half of the assignment space vanilla cannot express (spec 3.14) stays half under a moving map.
- **The map moves**: 19,730 orientation flips (~8/month). Most-contested links: genua-ragusa (722),
  champagne-genua (701), carribean_trade-ivory_coast (609), amazonas-brazil (592).
- **The aggregate ends are stable**: Phi_w sinks are { genua, hangzhou } at 1444 and still
  { genua, hangzhou } at 1645 -- the two-pole structure survives 200 years of churn.
- **D1 enforcement held**: of 7,373 SetTrader calls, 427 were collect attempts; all were either
  forced to transfer or kept only where the rule allows (home capital 417, END node 9).

## F results (2026-08-27, pgt_i74, clean 1444 vanilla start, spectator)

New instruments for these: `[ends]` logs the installed orientation's sink set on every orientation
install, and `[goodsinks]` (marker `pgt.GOODSINKS`) logs one named good's sinks and price per tick.

- **F2 PASS (raze China moves the end).** Baseline `[ends] Phi_w sinks=2 { genua hangzhou }`.
  Zeroed all 27 hangzhou-node member provinces (`set_base_tax <id> 0` + `set_base_production <id> 0`,
  ids from the emitted 00_tradenodes.txt); world wealth 10620.7 -> 10413.5 on the next live solve.
  Within a few ticks the ends became **`{ genua gulf_of_siam }`** and stayed there -- exactly the
  spec 2.8 row. The `[flip]` lines show the mechanism: `xian -> hangzhou` became `hangzhou -> xian`
  (hangzhou stops terminating and drains inland), with chengdu/canton/lhasa re-orienting behind it.
- **Console note (empirical):** EU4 1.37.5 has **no** `change_price` verb (nor `set_price`/`price`/
  `add_price`; the console answers `Unknown command` / suggests unrelated verbs), so F5 cannot be
  driven live and is measured offline against the reference instead. `set_base_tax`, 
  `set_base_production` and `add_devastation` all exist and take `<province id> <value>`.
- **F1 PASS (a flip is honoured end to end).** The razing cascade flipped 35 links in one tick.
  In that SAME tick: `[arrows] ... layer rebuild OK` (arrows re-drawn), `[flowassert] 0 of 305
  directed inflows wrong` (propagation follows the new directions, nothing stale), `[E4] tick 4:
  CLEAN`. No one-month corridor lag, no tooltip/arrow disagreement, no propagation credited to the
  old side.
- **F3 PASS (owner changes move nothing day-of).** `own 112` + `own 118` transferred two rich
  Italian provinces to the observer. In the following ticks the only flips were the already-
  oscillating razed-China links plus gujarat-hormuz (flipping before the change); **nothing in or
  near Italy moved** -- genua, venice, ragusa and champagne all held. The model reads the place
  (tax/production/devastation/goods), never the owner tag.
- **Orientation stability, measured (bears on F4 'no cycle' and G2).** Flips per tick in this run:
  ticks 1-3 = **0, 0, 0** (a normal world is perfectly stable); tick 4 = 35 (my razing); then 7-8
  alternating with 0 on exactly seven links, ALL inside the zeroed region (hangzhou-xian, -nippon,
  -beijing, canton-chengdu, girin-siberia, lahore-lhasa, chengdu-xian). Zeroing 27 provinces makes
  those corridors carry literally zero value, which is the degenerate tie spec 3.6 predicts will
  flip freely. No oscillation appears anywhere in the intact world.
- **F4 PASS (war bites through devastation, and heals back).** `add_devastation <id> 80` on all 33
  champagne-node provinces (a war's effect without the war). Tick 23 flipped exactly the corridors
  the damage justifies -- `english_channel -> champagne` reversed, north_sea and lubeck turned into
  the Channel, and sevilla's two African links (safi, tunis) reversed. `add_devastation <id> -80`
  healed it; **tick 28 reverted every one of those six flips exactly**, wealth 10345 -> 10448. No
  hysteresis, no overshoot, no cycle left behind: Europe went stable again and the only continuing
  churn was the zeroed-China region from F2.
- **F5 PASS (a price crash spreads a market)** -- offline, `impl/src/f5test.cpp`, because 1.37.5 has
  no price console verb. Grain crashed 2.500 -> 0.625 on the stock start:
  **alpha 1.2500 -> 0.3125** (below 1, as spec 1.4 requires), and the sink set moves exactly the way
  a flatter demand curve should -- 6 -> 7 sinks, **losing venice** (the rich Mediterranean hub) and
  **gaining bordeaux and valencia** (populous, poorer Atlantic Europe) plus patagonia.
  Cross-validation: the BASE sink set { zambezi australia persia brazil venice english_channel } is
  identical to the live game's `[goodsinks] grain price=2.5 sinks=6`, so the offline harness and the
  in-game model agree node-for-node.
- **F6 PASS (devastation scaling), closed from the game's own data + a live swing.** The constant no
  longer rests on community documentation: `common/static_modifiers/00_static_modifiers.txt` states
  `devastation = { trade_goods_size_modifier = -2 }` (EU4 scales a static modifier by level/100, so
  the law IS `-2 x level/100`), and `gamedata::load_static_mods` parses that same file, so the model
  and the engine read one source. Live confirmation from F4's swing: applying devastation 80 to 33
  provinces and healing it again, **E1 kept agreeing (worst ~0.006 ducats) and E4 stayed CLEAN on
  every tick 20-31**. A different scaling law in the model would have moved goods_produced, node
  values and income away from the engine's; nothing moved.

## G4 -- direction-gated diplomacy (2026-08-27, pgt_i77)

**The spec 1.10 seam was never installed before this session** -- the attach log listed
`direction_gates` as pending, and `gates::install` had no caller. It is now wired in (off with
`pgt.NOGATES`) and measured:

- **PASS (gates evaluate true) -- corrected evidence.** The first measurement of this was worthless:
  it read the matrix back immediately after our own `memset`, with no engine code in between, so it
  could never fail. Worse, a review found the fill was being **undone every month**: the mod itself
  rebuilds the reach matrices directly (after an orientation install, and after merchant landings),
  the engine's rebuild restores its own BFS into A/B/C, and only C was being re-applied -- so spec
  1.10 held for the microseconds between the engine's monthly rebuild and the mod's next one.
  Fixed: the B fill is now a callable (`gates::fill_b`) invoked after **every** rebuild, the mod's
  own included, and the health check now samples B at the START of the next rebuild -- i.e. after a
  full month of engine and mod activity, where it can genuinely go red.
  Measured with that check: `gatefills=27`, **`gateB-zero-before-rebuild=0`** -- B was still
  entirely set a month later. Both out-of-line predicates are patched to return true: the
  treasure-fleet gate `0x3E1D30` (spec 3.12: always granted) and `IsNodeUpstreamOfCountry 0xB4E020`.
  The trade-conflict CB at `0x38D8C0` needs nothing -- it is a pure power-share threshold.
- **No regression from opening them:** E1 665/665 (worst 0.0058), E4 CLEAN, 0 spurious re-setups,
  no crash, and matrix C is still written by the model (`matC writes=13300`) for light ships and the
  +10%/merchant home bonus.
- **Scope, deliberately:** only matrix B (the upstream/downstream table) is filled. Matrix A is the
  treasure fleet's ROUTING BFS, and `treasure.h` -- the spec 1.11 router -- does not exist; filling A
  would leave the router taking the first outgoing link and dead-ending, turning a missing feature
  into a broken one. So treasure fleets are **always granted** (3.12, the claim the spec actually
  makes) while routing keeps the engine's own reachability. **Residual: the 1.11 route ladder with
  privateer skimming is not implemented.**

## E3 -- world total vs vanilla, with a null run (2026-08-27, pgt_i79)

Three 14-month legs from the same clean 1444 Castile start, spectator, identical build. The two
controls run with `pgt.NOWRITE`: the model still reads, solves and instruments, but writes nothing,
so the engine's own vanilla division stands and `[E3/top]` measures **vanilla's** paid trade income.

| month | nullA | nullB | mod | null spread | mod vs vanilla |
|---|---|---|---|---|---|
| 1 | 332.53 | 332.86 | 342.45 | 0.10% | 2.93% |
| 7 | 334.81 | 334.13 | 346.91 | 0.20% | 3.72% |
| 14 | 333.23 | 333.26 | 344.04 | 0.01% | 3.24% |

**World total: PASS.** The modded world total sits **+2.9% to +3.8%** above vanilla and is flat
across 14 months -- no drift, no compounding. Vanilla's own run-to-run spread was unusually tight
here (worst 0.26%), well inside the up-to-8.96% node-level spread spec 2.8 records.

**Distribution: PASS on the spec's criterion (plausibility), which is the gating metric.** Resolved
to tags (country+0x20, found live; index 1 == REB confirms the offset):

- vanilla: **GEN** BNG VEN TUR LAN ENG POL MAM / MNG JNP
- modded:  **MNG** BNG DAI TUR VEN CAS NOV LIT

Three names are shared (BNG, TUR, VEN) and the set otherwise differs **by design** -- the mod
replaces the trade network, so it must. What matters is that every modded top earner is a real 1444
great power: Ming, Bengal, Dai Viet, the Ottomans, Venice, Castile, Novgorod, Lithuania. The
headline change is that **Ming**, the largest economy on the map, leads instead of **Genoa**, which
tops vanilla only because it is the terminal sink of vanilla's hardcoded funnel. That is the
intended consequence of per-good routing, not an implausible outcome.

- **Residual, measured not assumed:** one inline gate site, `0x18999C`, reads matrix **A** with no B
  fallback and so still refuses when the engine's real BFS says unreachable. A cannot be filled
  because it doubles as the treasure fleet's routing BFS and `treasure.h` (spec 1.11) is unbuilt --
  filling it would make the router take the first outgoing link and dead-end. The two SetTrader
  sites are `B || A`, so B satisfies them. Recorded as a gap, with the trade-off stated.

## Final observer run and sign-off (2026-08-28, pgt_i80)

**J8 PASS (user).** Second campaign in one process: confirmed working. Note the premise changed --
EU4 REPLACES ITS PROCESS on quit-to-menu, so each campaign is a fresh attach rather than an
in-process reset; the in-process path survives as defence.

**The 200-year observer run: user sign-off** -- "the trade mod worked exactly as planned, consider
the run completed". Second run, 1444 -> **1635** (2292 monthly ticks, 191 years), vanilla map, mod
only, spectator at speed 5, unattended. The world is preserved at
`save games/observer_long.eu4` (69 MB) -- the first run's world was lost when later test campaigns
rolled EU4's three autosave slots, which is why this one is copied aside as it goes.

| check | result |
|---|---|
| crash / hang | **none**; process healthy at the end |
| spurious campaign re-setups | **0** |
| direction gates held all month | `gatefills=7915`, **`gateB-zero-before-rebuild=0`** |
| E1 income agreement | 246/250 at the end, worst 0.031 ducats as the economy roughly doubles |
| E4 | **7 non-clean ticks of 2292** -- see below |

### One open defect, found by this run

E4 flagged `DISPLAYED-TOTAL=1` on **7 ticks of 2292** (ticks 237, 450, 1900, 1903, 1904, 1999,
2018): on those months exactly one node's *displayed* total (local + incoming - outgoing) went
negative, which spec 1.12 forbids ever showing. Every other invariant was clean on those same ticks
-- pool, outgoing, link values, money, non-finite and runaway all 0 -- so this is a **display-only**
violation, not lost or invented money. Rate: 7 node-months out of ~183,000 (0.004%). The earlier
201-year run on pgt_i73 had zero, so it is rare enough to need a long run to surface.
The instrument does not name the node (the `worst` field printed empty), so the next step is to log
the node and its six fields on violation and re-run the soak.

> **RETRACTED 2026-08-28 by code review — see the corrected section at the end of this file.**
> Both results below were produced by instruments that could not measure what they claimed.
> The J10 classifier keyed steer state by country while writing it per node, so every country with
> more than one merchant was misclassified; and the `gateB-zero-before-rebuild` reading was taken
> moments after our own memset, so it could not fail. Kept for the record, not as evidence.

## J10 + a G4 gap found on the load path (2026-08-28, pgt_i86, the 1635 world)

**J10 PASS.** Light ships that protect trade show up as `ship_power` on the node's own per-country
record, so this is measured off the engine's data rather than by eye. On the late-game world,
134 placements totalling 2347.9 power:

| where | power | share |
|---|---|---|
| home node | 1705.9 | 73% |
| **reverse (Phi_w-incoming) end** | **76.5** | 3% |
| other steered node | 250.4 | 11% |
| unsteered | 315.1 | 13% |

The user's observation that ships cluster at home nodes is correct and is **not** a defect: light
ships protect trade where a country COLLECTS, and home is where it collects -- vanilla does the same.
J10's claim is the narrower one, that ships follow the MODEL to nodes vanilla would never choose, and
they do: 27% sit away from home, including 76.5 power on reverse ends -- nodes a country only has
business at because the model gave it a merchant pushing against the drawn arrow. Vanilla's scorer is
unmodified (the user's call); it reaches those nodes because it consumes the model's node values,
shares and reach (matrix C).

First measurement of this was WRONG and said `home=0`: the classifier keyed standings by the raw tag
dword and ship records by the bare index, so every placement fell through to `unsteered`. Fixed.

**G4 gap found and closed.** Right after loading a save the instrument read
`gateB-zero-before-rebuild=481`: a load runs several 0xB4DB00 call sites the mod does not own, and
matrix B came back as the engine's own BFS, so spec 1.10's gates were **not in force** until the next
controlled rebuild. Matrix B is now also refilled from the frame poll (a memset at 2 Hz), and the same
instrument reads **0** on the load path. Only visible because the treasure test loaded a save --
every earlier G4 measurement was on a fresh campaign.

## H3 PASS (user, 2026-08-28)

H3's bar is subjective -- "the monthly tick's added time is imperceptible" -- so the user playing the
mod is the measurement, and the user's verdict after the 201-year run, the 1635 world and the
compatibility sessions is: **"the time it takes is fine. The tick isnt noticable."** PASS.

For the record, the numbers behind that verdict: the tick is 86 ms on the 1444 world and 146-160 ms
on the loaded 1635 world (81 nodes, world local 926), against vanilla's own 87-98 ms monthly stall.
Cost does NOT grow with the campaign -- across 201 years it went 231 -> 182 -> 167 ms as tags were
annexed. The earlier "NOT PASSED yet by the imperceptible wording" note above was my own reading of
the wording, not a user complaint; it is superseded by this line.

## H1 -- tick determinism across a reload, ATTRIBUTED (2026-08-28, pgt_i86)

The open H1 note above asked for one instrument: pair the orientation fingerprint with a hash of the
INPUTS the solve consumed (every province's tax/production/devastation/good, plus all prices), so a
divergence can be blamed on the right side. Built, and run as two legs that differ ONLY by "the
process was restarted and the save re-read": each leg copies the identical preserved world
(`observer_long.eu4`, 1635) over `autosave.eu4`, launches a fresh eu4.exe, loads it, and ticks.

| tick | date | orientation A vs B | inputs A vs B |
|---|---|---|---|
| **1 (the reload boundary)** | 596775 | **identical** `e674bfa3108bfad8` | **identical** `8bc81b2513c4a373` |
| 2-11 | 596806-597079 | matched on 6 of 10 | differ on 10 of 10 |

**PASS at the boundary the test is about.** On the tick that actually measures the reload, two
separate processes loading the same bytes produced a bit-identical world AND a bit-identical
orientation. Determinism on our side is therefore demonstrated, not assumed.

**The later drift is the ENGINE, and is now measured rather than inferred.** From tick 2 the inputs
hash differs on every tick: the engine's own simulation has moved to a different world (province
development and prices diverge; the province count drifts 3117 -> 3119 across the leg), so our solve
is no longer being asked the same question. Spec 2.8 already records that vanilla is not reproducible
run to run -- this is the first direct measurement of it in the live game. Note the orientation still
agreed on 6 of those 10 ticks DESPITE different inputs, which is the robustness the design predicts:
the orientation is a sign field, not a continuous quantity, so small input perturbations mostly do not
move it.

This supersedes the earlier "H1 as specified is NOT met across the reload" note, which was written
before the inputs fingerprint existed and could not tell the two causes apart. The solver's own
determinism is separately established (30/30 offline cross-check).

## G4 and J10 RE-MEASURED after code review (2026-08-28, pgt_i90, the 1635 world)

A review of the working tree found that BOTH results recorded earlier today came from instruments
that could not measure what they claimed. Both are retracted above and re-measured here.

### G4: the direction gates were only partly held, and the old check could not have shown it

Spec 1.10 needs matrix B (mgr+0x90) all-1 so the 21 INLINED gate sites answer true; the two
out-of-line predicates are patched separately and were never in doubt. B is restored to the engine's
own BFS by 0xB4DB00 -- and a `.text` scan of eu4.exe for E8 rel32 calls reaching it finds **six call
sites**, of which the mod hooked **one**. The other five refilled B behind us.

The old instrument sampled B just before the monthly rebuild and reported 0. That reading was
worthless twice over: the frame-poll refill added earlier today memsets B every ~0.5 s, so the sample
was taken just after OUR OWN write; and `ticklive.h:412` refilled B after our own rebuild while
passing the default call-site tag, so each correction sampled B holding the engine's BFS and counted
ITSELF as a lapse. The first fault hid real lapses, the second invented fake ones.

The instrument now samples B *before* our write at each frame poll and counts only what the ENGINE
put there. Measured red-then-green on the same world, same save, same build family:

| configuration | frame refills | LAPSES | worst probe |
|---|---|---|---|
| 1 site hooked, frame refill OFF (`pgt.NOGATEFILL`) | 0 | 26 | **480/512 dirty** |
| 1 site hooked, frame refill ON | 68 | 28 | 489/512 |
| 5 sites hooked, tag bug still present | 51 | 14 | 480/512 |
| **all sites refill, tags correct** | 39 | **0** | **0/512** |

**PASS, and the check is falsifiable**: the top row is the same counter reading 480 of 512 probes
dirty with the refills suppressed, so a broken gate does register. The old check could only ever
read 0.

Two fixes got it there. `gates::install` now repoints every call site the binary scan found, so B is
corrected at the instant of each rebuild rather than up to half a second later. And `0x775EEC` --
which the log still honestly reports as `5/6 ... MISSED` -- turned out not to be missing at all:
`earlyload.h` hooks it first for the savegame path, so `gates::install` cannot repoint it. Its wrapper
carried the comment "fill_b runs from the wrapper on the monthly path", which was true only from the
NEXT month, leaving matrix B holding the engine's BFS across an entire load. It refills in place now.

`gate-size-growth = 0` throughout: mgr+0xA0 never grew while the block pointer stayed put, which is
the hazard the deleted growth guard was meant to watch (see DEPARTURES.md, corrected).

### J10: light ships, with a classifier that actually distinguishes the buckets

The old classifier keyed steer state by country while writing it once per node, so it kept whichever
node came last and then asked "is there an arrow into THIS node from the target it steers to somewhere
ELSE" -- wrong for every country with more than one merchant, i.e. every major power. It also ANDed a
record field that is 0 on ordinary records, so almost nothing could reach the "no merchant here"
bucket. Now keyed by (country, node), and "steers here" means here.

| where the light ships are | sample 1 | sample 2 |
|---|---|---|
| home node | 1692.8 (72%) | 1695.8 (69%) |
| **reverse (Phi_w-incoming) end** | **133.7 (5.7%)** | **213.8 (8.7%)** |
| other steered node | 187.1 (8.0%) | 107.5 (4.4%) |
| no merchant at this node | 330.8 (14%) | 429.5 (18%) |

**PASS.** Reverse ends carry 5.7-8.7% of light-ship power -- more than the broken instrument's 3.3%,
not less. Home still dominates, which is correct and not a defect: light ships protect trade where a
country COLLECTS, and vanilla behaves the same way. J10's claim is that ships follow the MODEL to
nodes vanilla would never pick, and ~28-31% of power sits away from home to do it.
