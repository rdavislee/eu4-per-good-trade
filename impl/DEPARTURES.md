# Departures from spec

The specification (`per-good-trade-spec.md`, v6.6) is unchanged and remains the authority for
everything not listed here. Each entry below is a deliberate, user-directed departure: what the
spec says, what the implementation does instead, why, and how it is measured. Entries are dated;
none is applied without a user decision recorded in the entry.

---

## D1. Merchants never collect (2026-08-26)

**Spec.** §1.7: "Placement, range, and the collect/steer choice are vanilla." §3.14: the AI's
collect/steer choice is vanilla's.

**Departure.** No merchant collects, for the AI and the player alike. The only collecting standing
at a node is a country's trade capital, and no merchant may be placed at the trade capital.
Engine side: a prologue hook on the outer `SetTrader` (`0xB596E0`) forces transfer for any
trader record except a capital's; a per-tick sweep converts records that were collecting before
the hook existed. AI side: the frontier plan never targets the capital, and vanilla's 573
collect-at-home opening merchants are recalled first (value 0 under the rule). Player side: the
node window's collect action is inert (the hook), and the map-panel steer buttons are the control.

**Why.** The user's model of merchants: they exist to steer goods home along the per-good graphs;
collection is what the capital does with what arrives.

**Measured.** `[nocollect]` lines: 37-38 save-start collectors converted on tick 1, 0 after;
573 -> 8 capital merchants over 11 ticks; E1 ~660/660, E4 clean throughout (TESTING.md G block).

**Residual -- closed 2026-08-26.** At a Phi_w END node (genua, hangzhou) the engine has no
outgoing entry, and four of OUR guards (relink demotion, syncrec skip, the no-collect hook and
sweep) kept a merchant there at `type = 0` -- paid as a collector with the -50% non-capital
penalty (user-reported). The guards dated from the 0xB5654D crash, since fixed by the slack-padded
per-link buffer; the other engine check (0xB53C77) is a SIGNED compare that exits on index 0 at
N = 0. All four relaxed: end-node merchants are written as transferring with index 0 like any
reverse end. Measured: 10 monthly updates, no death, 0 merchants collect at end nodes, the AI
plans genua, E1 664/664. Appending reverse-end entries to the definition graph (relink's ALLOUT)
remains OFF: it corrupts the heap through the engine's own consumers (two deaths at tick 3,
`ntdll` heap fault, with and without our AI acting). D3 additionally makes any merchant record's
collector share 0, so the payment side never depends on the engine's type byte.

**Extensions (user, 2026-08-26 evening).** (a) No country STARTS with its merchants collecting:
vanilla parks ~570 merchants at their capitals at 1444 and the recall caps spread their
re-placement over ~11 months; on the FIRST monthly tick the caps and the AI shard are lifted and
the human's merchants are included once, so the opening state already follows the rule (from
tick 2 the player keeps their own). (b) The node window: no "Collect from Trade" button on any
node, a "Transfer Trade Power" button at END nodes too, and NO button at the player's home node
(nothing can be placed there). (c) Display: a reverse-panel merchant shield carries the same
hover text as a forward one; the node window's "We transfer X to <node>" names the table's
target (the engine names forward link #0); the Outgoing hover lists reverse destinations and
the trade-power hover shows the received power as "Transfers from traders downstream".

**How (implementation notes, 2026-08-26 night).** (a) The mod sets up INSIDE THE LOADING SCREEN
(earlyload.h): the engine's game-setup paths each make one trade call while loading -- the new-game
path calls the monthly driver 0xB4BA90 at 0x774C3B, the savegame path the reachability rebuild
0xB4DB00 at 0x775EEC -- and both call sites are repointed to a wrapper that lets the engine's call
run, then does the whole install on the loading thread, solves the orientation synchronously
(~120 ms) and runs the driver once more with income suppressed: our tick hook inside it is tick 1,
so the map appears already re-oriented and re-placed (measured: the worker defers, 'orientation
gen 1 solved in 120 ms', tick 1 done before the loading finished). The DLL must be in the process
before the campaign loads (the version.dll proxy, or the runner injecting at the main menu); injected
later, the frame poll runs the first tick at attach instead, holding the run's console commands
until it is done. Merchants left standing at their own capital after the plan is served are
returned to the pool through the engine's own recall (0x25BA70), not left collecting.
Vanilla's own opening placement -- 0x773B20's last loop parks one idle merchant per country at its
capital (0x774E05 -> PlaceMerchantAtNode, type 0), AFTER the loading-time tick -- is skipped (the
call is repointed to a stub), so a campaign opens with the plan's merchants posted and the rest idle.
PERSISTENCE: the table is written beside every save as <save>.eu4.pgt (the two save writers'
`.tmp -> .eu4` renames are wrapped) and restored before the loading-time tick of a load; a save
without a sidecar gets the opening rule once. The +10%/merchant home-node power bonus
(TRADE_POWER_HOME_BONUS) needs no change: the engine counts every transferring merchant of the
country gated by a reachability byte set for each merchant's own node, which the landing-triggered
rebuild keeps current (static RE 2026-08-26).
The engine's per-country x node reachability tables (CTradeManager+0x88/+0x90/+0x98, rebuilt by
0xB4DB00 only monthly) gate the steer buttons, the steer command and SetTrader itself; they are
rebuilt right after every relink and once per frame after any merchant lands, or every panel
reads "You cannot direct trade after it has passed your home" until the next month. (b) The node
window's buttons are runtime list items (CTradeNodeView::RebuildEnvoyItems 0x13D6120): four two-byte
patches drop the collect item on both paths and ignore the definition's `end` flag, so a node with
no merchant offers Transfer only (home: nothing -- the home gate stands, and the "Send Merchant"
label is hidden there), a node with our merchant offers Recall. A transfer placed by the window
(or by vanilla's AI) gets its table target set to the next link toward the country's home the
moment SetTrader runs (homeward.h), so nothing points downstream by default; among equally short hops the
one carrying the model's away-flow wins (bordeaux has no link to sevilla: its hop home is ivory_coast). (c) Texts: the
node-window formatter call (0x13D0539) and the outliner's (0x12BEDFA) are repointed to substitute
the table's target; at END nodes both builders bail before formatting, so the sentence is
produced after they return (endtext.h). A reverse panel's shield row is given the engine's
"mapicon_traderoute" tooltip key after it is rebuilt, which is all the hover text needed.

---

## D2. AI merchant assignment: the frontier model (2026-08-26)

**Spec.** §3.14 scores link ends by a denial/gain rule with vanilla's reassignment cadence as an
open question.

**Departure.** Home = the trade-capital node. Network = home + the nodes holding the country's
merchants, grown one node per placement. Candidates = frontier edges (one end in the network,
one out; the merchant stands outside and steers inward) that the engine's own
`CanSendMerchantTo` (`0x3532C0`) accepts. Score = flow moving inward on the edge x the product of
(my power / all power) at every node on the shortest network path home (with the merchant-present
floor at every network node except home) x the share at home. A posted merchant standing off the
plan is moved only when a planned node beats it by x1.5, with a three-month dwell. Cadence: the
working default the spec reserved for the user -- it fires 1-3 recalls per tick world-wide.

**Light ships (user, 2026-08-26; pgt_i26).** Vanilla's protect-trade AI scores nodes by (1 - share) x
value with a home bias and a reach penalty read from the definition graph, so it never sends ships to a
node where a merchant steers against Phi_w. The model owns that score now: the allocator (0x1B8340)
splits each country's light-ship budget in proportion to a per-node score, and a prologue detour
replaces the array with the tick's value -- at every node where the country has a table-owned
placement, the gain of that placement (frontier::added_value, the merchants' own figure), plus at
home the pool it does not yet own. Fleet choice, the surplus recall and the trade_mission command
stay the engine's. Privateer and pirate-hunt reserves are untouched. `pgt.NOSHIPS` restores vanilla.

**Measured.** TESTING.md G block: 25-35% of placements on Phi_w-incoming ends, zero target churn,
recalled envoys still at their target one and three ticks later.

---

## D3. Trade-power propagation split by good (approved 2026-08-26, implemented v2)

**Spec.** §1.9 preserves vanilla: a country's provincial power at node m, if it meets
`TRADE_PROPAGATE_THRESHOLD` (2), sends `1/TRADE_PROPAGATE_DIVIDER` (a fifth) of it to the nodes
immediately upstream of m, one hop, summed at the receiver, no merchant condition; direction is
read from Phi_w. §1.8 makes only the *eligibility* of that power per good.

**Measured vanilla rule (the engine's own records, 1444, two ticks).** The propagated amount is
folded into `val` (`rec+0x48`); `province_power` (`rec+0x28`) is the source. On the 186 records
that carry nothing but provincial power and propagation (no merchant, capital, ships or
subject transfers), `val - province_power` equals the sum over the downstream Phi_w neighbours
of `province_power/5` (threshold 2) for 98 records under the FULL rule -- each upstream node
receives the whole fifth -- and for 9 under a divided fifth. The engine's figure runs ~0.7%
above the exact fifth (fixed-point rounding). `rec+0x50/+0x54` are NOT propagation: they pair
between countries at the same node (subject -> overlord transfers; `+0xAF has_subject`).

**Departure (v2, the user's rule, 2026-08-26).** Trade power stays ONE number per (node,
country). What becomes good-aware is how a node's fifth is DIVIDED among its neighbours. A country
with provincial power pp_c(m) >= 2 at node m sends F = pp_c(m)/5, as in vanilla. F is split among
the goods by price, and each good's portion goes to the neighbours of m that are UPSTREAM of m in
that good's graph (equally among them if several); goods with no upstream neighbour at m take no
share, so F is fully distributed whenever anything flows into m:

    split(m -> n) = sum over g with n in U_g(m) of (price_g / |U_g(m)|)  /  sum over g with U_g(m) != {} of price_g
    received_c(n) = sum over m of [pp_c(m) >= 2] * pp_c(m)/5 * split(m -> n)
    P_c(n)        = own_c(n) + received_c(n),   own_c(n) = val_c(n) - vanilla's full fifths along the installed graph

What n receives is ordinary trade power: the model writes P back into the record (`val` +0x48
and `max_pow` +0x4C so the engine's cap does not clip it), so the node window, the engine's own
scorers and the daily AI all see it, and the collector split uses it. A country receiving power
at a node where it had no standing gets one (and the engine already has a record slot there).

**Three clarifications (review 2026-08-26).** (1) The weight is price alone: a good claims its
price share of m's fifth on the strength of having an upstream edge at m, whether or not a unit of
it moves there this month -- deliberate, so the split does not chase monthly flow noise. (2) A
country that receives power at a node where it had no standing becomes transfer-eligible there
under 1.8's reach rule for the goods it collects downstream of; that is an intended economic effect
of the ~1,400 new standings, not a side effect. (3) `val` (+0x48) excludes the subject/overlord
transfers (every engine reader adds t_in - t_out after the cap), so the model writes P minus those
transfers into val and the node totals +0xC8/+0xD0/+0xD4 from P, so that every share the engine
displays or the AI consumes has the model's numerator AND denominator. World power under the split
is ~5% below vanilla's aggregate (one fifth per source instead of one per upstream neighbour).

**No feedback, by construction.** The source of every fifth is the record's PROVINCIAL power
(`+0x28`), never the standing's total: power received at a node is never re-sent from it (one
hop, never chains -- spec 1.9's own rule), and the write-back cannot ratchet because the engine
wipes and recomputes `val` from provinces at the start of every month.

(v1, superseded the same day: each good's graph carried the FULL fifth as a per-good power
P_c(n,g); it made power per good, which the user rejected -- trade power is per node.)

**Consequences the implementation must carry.**
1. The model computes the collector division itself: `power_fraction` (`rec+0x2C`) is written
   per record before the engine's division as the collector's share of P among the node's
   collectors (0 for any non-collector, merchant records included), so pass 10 pays the model's
   figure. E1 predicts from the written shares.
2. A merchant the table says steers at an END node gets collector share 0 -- the engine and the
   model agree on who is paid without the engine needing an outgoing entry there. This closes
   D1's residual, and the AI may plan end nodes again.
3. The AI's path shares keep the aggregate power for now (own + vanilla propagation); the
   per-good gradient is the follow-up that also tells light ships where to go.

**Why.** Per-good graphs disagree with Phi_w on ~45% of edge-goods; propagating along Phi_w gives
a reverse-end merchant no upstream power for the goods it actually steers and credits power along
links a good never uses. Per-good propagation is what makes steering against Phi_w self-consistent
-- the "vibrant map" the user asked for.

**Implementation notes (review 2026-08-26).** The subtraction of the vanilla fifths follows the
INSTALLED graph (Phi_w, or the selected good's graph in a per-good view), never the attach-time link
list; `own` is signed (a subject's transfer deficit is carried, not clamped) and only the final
per-good power is clamped at 0, with the +2 merchant floor applied to that final power for
table-owned standings only. The written shares round to nearest permille and sum to 1.000 per
node where the engine's own summed to 0.995-0.998, so world collected income runs ~0.2-0.5%
above the engine's -- inside E3's null spread; not a regression. The normalisation divides by the
collected value of the goods that HAVE a collector at the node (a collector-less good's value is
redistributed onto the other goods' collectors: one engine pool must go somewhere). The optional
flow scaling is NOT implemented (documented only). The engine's amount runs ~0.7% above the exact
fifth (fixed-point rounding); it leaves `own` high by 0.007 x prop and cancels in the shares.
Open: whether `t_in - t_out` (subject transfers) is inside `val` or added after it -- install.h's
instruction reading and the probe disagree; a probe restricted to records with t_out > 0 settles
it. The offline suite (`aitest`, `econtest`, the 30/30 cross-check) still routes with the aggregate
power: it is a Phi_w-propagation CONTROL, not a model of the live tick.

**Measurement plan.** (a) offline: per-good powers reproduce vanilla's aggregate exactly when all
graphs equal Phi_w (identity test on the 1444 standings); (b) in game: E1 (engine-divided income ==
model prediction with the written shares) stays at all countries, E4 clean, world collected
income within the E3 null spread; (c) the number of AI placements on reverse ends and the flow on
them, before and after.

## The per-good view is a render overlay, never a tick (2026-08-27)

The month tick always writes the FULL aggregate economy -- pools (+0xB0), power, shares, E1/E4 --
whatever view is open; the active view is applied afterwards as a display overlay (link records,
node display fields, arrows), which never writes the pool and never touches standings. A province
click re-runs only that overlay from the last tick's cached model outputs, under the tick's own
g_inside exclusion, so clicking is instant (~40 ms), works paused, and cannot move a merchant,
deflate trade power (the i37 double-apply ratchet), or pay pass 10 on a single good's pool.
The trade-route layer and the reachability matrices rebuild on EVERY orientation install: relink
reports reversals against the FILE declaration, so '0 reversed' does not mean 'nothing changed'.

## In-session reloads are detected by the trade manager's identity (2026-08-27)

An in-game load (exit to menu -> load) reaches neither 0x5D00BC (the binary's only direct caller
of InitSaveGame 0x7751B0) nor the inner 0x775EEC site: a different loader builds the world, and
the mod used to keep running with the old world's plan and freed pointers (user: 'the game
reverted to vanilla'). Both the tick hook and the frame poll now compare the live trade manager
with the one the plan was set up for: a mismatch holds ticks and reruns the save setup from the
frame poll (world reset incl. relink/arrows/colorview caches, sidecar restore, suppressed driver,
solve), same as the loading-screen path.

## Direction gates: matrix B only, and the treasure router is not built (2026-08-27)

Spec 1.10 ("any mechanism gated on one nation being upstream or downstream of another evaluates
TRUE") is now installed -- it never had a caller before this session; the attach log listed
`direction_gates` as a pending seam. `gates::install` repoints the reach-matrix rebuild call and
patches the two out-of-line predicates (treasure-fleet gate 0x3E1D30, IsNodeUpstreamOfCountry
0xB4E020) to return true.

It fills **matrix B only**, deliberately:
- **C (mgr+0x98) belongs to the model.** `apply_matrix_c` writes the per-good reach there so
  vanilla's own light-ship scorer and the +10%/merchant home bonus consume the model's network.
  Filling it with 1 would erase that and tell the engine everything is reachable for everyone.
- **A (mgr+0x88) is also the treasure fleet's routing BFS.** `treasure.h` -- the spec 1.11 route
  ladder with privateer skimming -- does not exist. A router whose every hop test answers yes takes
  the first outgoing link and dead-ends, so filling A would convert a missing feature into a broken
  one. Treasure fleets are therefore **always granted** (spec 3.12, the claim the spec actually
  makes, via the patched gate) while routing keeps the engine's real reachability.

**Known residual:** the 1.11 route ladder / privateer skimming is unimplemented. Recorded as a gap,
not silently absent.

## The engine's reach matrices are allocated once, memset every rebuild (2026-08-27)

0xB4DB00 allocates its three matrices on the FIRST call only (`jne` past the allocation when the
pointer is non-null) but writes `countryCount x nodeCount` to mgr+0xA0 and memsets that many bytes
on EVERY call. If the country count ever grew after the first rebuild, every later rebuild would
overrun three engine-heap blocks.

**Correction (2026-08-28, reviewed).** This section used to describe a `gates::guard_matrices` that
tracked the allocated size. That guard was DELETED the same day this paragraph was written -- its
country-count reader called the wrong global and returned garbage (-1157598207) in vanilla while
looking plausible under a total conversion, and four of the six 0xB4DB00 call sites are outside our
control and advance mgr+0xA0 without reallocating, so it could not observe growth anyway. The
paragraph outlived the code it described; a review caught the mismatch. `matrix-resets` and
`engine-countries` do not exist either.

What is there instead is smaller and honest. The engine memsets mgr+0xA0 bytes over this same block
on every rebuild, so our writing that many bytes is exactly as safe as the engine's own write --
the hazard is shared, not one we create. `validate_region` cannot bound it (VirtualQuery reports the
page region, not the heap-block boundary), so `gates::fill_b` watches the COUNT: it records the size
at the pointer it first saw, re-baselines whenever the block is reallocated, and if the count ever
grows while the pointer stays put it clamps to the baseline and increments `gate-size-growth=`, which
rides the per-tick line. Measured 0 across the red/green gate runs on the 1635 world.

## Treasure fleets: the engine already routes Phi_w; the mod supplies the ladder's fallbacks (2026-08-27)

Disassembly of `CCountry::SendTreasureFleet` (0x3E1EC0..0x3E3939, one caller at 0x2F3E33 in the
monthly country update) settled what spec 1.11 needs and what it does not:

- The fleet **walks the trade graph hop by hop inside one call**. Loop head 0x3E2083: visited check,
  push, stamp, then every privateering country skims a share proportional to its power AT THAT NODE,
  then the arrival test. So the skim really is per node traversed, and it compounds.
- Hop selection (0x3E2358..0x3E2403) walks the definition's OUTGOING links and takes the first whose
  target satisfies matrix A. **Because the mod rewrites the definitions, that walk is already a
  Phi_w path** -- rung 1 of the 1.10 ladder is free, and with the gate predicate 0x3E1D30 forced
  true the overlord always receives (1.11's first sentence, 3.12).
- When Phi_w does NOT connect, the link scan exhausts and 0x3E2418 sets the current node straight to
  the destination: the fleet **teleports**. It still arrives -- nothing is destroyed -- but it skims
  at two nodes instead of four or five. Measured on the 1444 field at alpha_phi = 2.0: **55 of 144**
  (colonial node, European capital) pairs do not connect, and **mexico (11 gold provinces) and lima
  (2, incl. Potosi) reach no European capital at all** -- the canonical Spanish silver fleet is
  exactly the case that teleports. This is alpha-sensitive, not structural: at alpha_phi = 1.5 every
  New World node connects.
- The engine's denial branch (unreachable, gate not forced) simply leaves the gold with the colony:
  `TREASURE_FLEET_TOOLTIP_CANT_REACH_DELAYED` = "They will keep their gold income instead." Nothing
  is lost, which is why leaving matrix A real (see the gates note above) is safe.

**What the mod adds (`treasure.h`).** A hook at the top of hop selection supplies the next hop from
the full 1.10 ladder -- Phi_w, else one good's graph, else undirected -- so the fleet passes real
nodes and privateers skim en route. Everything else (the skim loop, payouts, inflation, messages) is
the engine's. Design constraints, all reviewed against the binary:
- The ladder is **precomputed once per orientation** into a flat int16 next-hop table, so the hook
  inside the money path is a table lookup plus bounds checks -- no allocation, no throw, no lock.
- The hook **declines whenever it is not certain** (unknown node, no path, hop already visited), and
  declining is exactly the engine's own behaviour, so the worst case is today's game.
- It must never hand back a visited node: that reaches 0x3E248C ("Stuck processing trade nodes"),
  the one branch that pays the privateers and then drops the overlord's gold.
- The redirect must reload EDX from [rbp+0x174] before re-entering the loop head -- EDX is a
  loop-carried live-in (the visited count) and all three engine backedges load it the same way.
  Off with `pgt.NOTREASURE`.

## Launcher gate (2026-08-28, user-directed)

Spec §2.5 has the DLL verify the build and attach unconditionally. The shipped DLL adds one
precondition ahead of the build gate: at attach it reads `dlc_load.json` (the engine's own
record of the enabled mod list, via the same modfs reader the solver uses) and arms only when
the data half is enabled -- the entry `mod/pgt.mod`, or any enabled descriptor named
"Mare Liberum". Otherwise it logs `DORMANT` and remains a pure version.dll proxy: no build
gate, no patches, no worker thread, a bit-vanilla game. Rationale: the launcher checkbox
becomes a true off switch, so the mod can stay installed while other playsets run. The empty
marker `pgt.FORCEDLL` beside the DLL arms it regardless, for probe sessions that run without
the data mod. Verified live both ways (dormant under an Anbennar-only playset; armed with
`mod/pgt.mod` enabled).

## Node-file sync (2026-08-28, user-found defect: Anbennar + Mare Liberum broke the trade map)

The shipped `00_tradenodes.txt` re-declares the VANILLA map, and the engine resolves same-named
files by descriptor filename, alphabetically first wins, ignoring the launcher's playset order
(measured: three playset orders and a `name=` change all left `pgt.mod`'s copy beating
`ugc_1385440355.mod`'s; the Aug-27 compat run only worked because Anbennar was then registered
as `anbennar.mod`, which sorts before `pgt.mod`). Rather than fight the sort, the DLL makes the
content identical: at attach (armed, after the build gate, before the engine reads game files)
it scans the enabled mods, and if any OTHER mod ships `common/tradenodes/*.txt` it writes that
content into the mod's own `00_tradenodes.txt`; with no such mod it restores `phiw.baseline`
(shipped beside the file; `dist/build-mod.ps1` emits both from `impl/out/00_tradenodes.txt`).
Whichever copy the engine picks, the bytes agree. Verified: menu probes show the file flipping
to Anbennar's bytes and back to baseline, byte-exact, per enabled list.
