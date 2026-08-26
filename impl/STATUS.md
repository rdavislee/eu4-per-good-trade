# Implementation status

## THE MOD RUNS IN THE LIVE GAME

Injected into a running `eu4.exe` (build 835bfdf8), the DLL:
1. verifies the build and **runs the full DRAIN solver in-process** (2472 provinces, Φ_w ends
   `{genua, hangzhou}`, all per-tick checks green);
2. **reads the engine's own per-node/per-good produced quantities** — the 33-slot
   `trade_goods_size` vector on each of the 81 live `CTradeNode`s (spec §1.8's `inject_g(n)`);
3. **solves all 29 per-good graphs** and routes each good's value along its own graph
   (routed world value 1241.91);
4. **writes the routed economy back into the engine's node fields** (81 nodes) — the change is
   visible in EU4's own trade-node window;
5. **re-installs on every monthly trade tick** (spec §2.6's cadence), verified over repeated
   ticks with the game running normally.

Run it: build+inject with `scratchpad/inject.ps1` (markers `pgt.INSTALL` and `pgt.MONTHLY` next
to the DLL enable the write and the monthly loop). `impl/accept.ps1` verifies the whole suite
including this live-game evidence.


Two tracks, per spec §2.9. **The solver track is built and passing; the memory/DLL track is the
open schedule risk the spec flags** — its live-memory offsets are undiscovered and need a
debugger session against the running game.

Run everything: `impl/accept.ps1` (from anywhere). Build alone: `impl/build.ps1`.

## Solver track — complete, all green

Header-only C++17 in `impl/src/`, driver `main.cpp`, dynamic build (`impl.exe`).

| Deliverable (spec) | Where | Verified |
|---|---|---|
| defines parser (§2.9 first) | `gamedata.h` | overrides merged in load order; difficulty files held separate |
| save parser, non-ironman (§2.2.2) | `save.h`, `zipread.h` | own inflate byte-identical to zlib over the 34 MB gamestate |
| prices / static-mods / tradenodes (§2.2.1) | `gamedata.h` | GP_COEFF read from file (0.2), 4 state modifiers read |
| wealth field, owner-agnostic (§1.3) | `field.h` | 2,472 counted provinces, world wealth 10,607.40 |
| DRAIN + network simplex (§1.1, §2.2.5) | `drain.h`, `netsimplex.h` | simplex-family, Bland anti-cycling, pinned tol |
| **cross-impl orientation equality (§2.8 / A5)** | `tools/compare.py` | **exact, 30/30 graphs** (Φ_w + 29 goods) |
| per-tick assertions (§2.8) | `drain.h` | acyclic · containment · conservation<2e-14 · reach 100% |
| **negative fixtures, each red (§2.9)** | `fixtures.h` | **12/12 red** incl. T1/T2/T3 counterexamples |
| tradenodes emitter (§2.4 / A2,A3) | `emit.h` | adjacency==Φ_w, ends {genua,hangzhou}, 0 order viol., A3 byte-clean |
| reachability census (§2.2.7) | `analytics.h` | 5,723 / 90.6% ordered pairs |
| survival-table skeleton (§2.2.6) | `analytics.h` | rows sum to 1, sinks collect fully (no-merchant baseline) |
| determinism (H1) | `main.cpp` | 3 re-solves identical fingerprint |
| synthetic shock (§2.2.8 / F2) | `main.cpp` | razed hangzhou → ends {genua, gulf_of_siam} |
| attach build gate (§2.5 / A4) | `attach.h`, `sha256.h` | passes on 835bfdf8, refuses others; SHA-256 = NIST vector |

Every spec figure the solver touches reproduces exactly, and `verify6.py` still reports 37
checks / 0 failed.

## Commands

```
impl.exe dump    <eu4> <save> <out.json>   full solve -> orientation dump
impl.exe checks  <eu4> <save>              per-tick assertion battery
impl.exe fixtures                          negative fixtures (each must go RED)
impl.exe census  <eu4> <save>              reachability census + survival skeleton
impl.exe determinism <eu4> <save>          re-solve fingerprint stability
impl.exe shock   <eu4> <save> <node>       zero a node's dev, re-solve, show ends
impl.exe emit    <eu4> <save> <out>        generate 00_tradenodes.txt
impl.exe verify-build <eu4>                attach build gate
```

## AI merchant assignment — logic built and tested (`ai.h`)

Cadence is **shadow-vanilla** (the user's choice A): each tick we diff every AI country's
merchant assignments; when vanilla moved one, that event triggers our re-placement. Mirrors
vanilla's cadence by construction, fires on conquest for free (the Ivory Coast case), no
flip-rate gate — merchants survive flips (§1.7). The **target** is ours: candidates are
(node, incident-link-end) pairs over both tab groups, active good set read from the per-good
orientations, scored through the survival table; a zero-steer candidate is never chosen. The
value terms are recomputed from the country's live power footprint each evaluation, so conquest
raises `V_new` immediately. A secondary dwell-floored gain test exists but is disabled
(`SECONDARY_TRIGGER=false`), keeping it strictly mirror-vanilla for now. Three AI fixtures pass:
value-driven placement at a conquered node, shadow-trigger fires only for the moved country,
zero-steer candidate never enumerated.

## DLL scaffold — builds, attaches, gates, runs the solver in-process (`dll/`)

`per-good-trade.dll` (1.7 MB) compiles with the whole solver embedded and exports the
`version.dll` forwarders so it can inject as that proxy (the EU4dll vector). On attach:
1. **Build gate** — in-memory `release_1.37.5` pattern scan of the loaded image (EU4dll's own
   method, `pattern.h`) **and** `eu4_rev.txt` + `eu4.exe` SHA-256. Verified: **refuses** a
   non-target host (fails closed), **passes** on the real install.
2. **Embedded solver self-test** — runs the full DRAIN solve *inside the process*: 2472
   provinces, ends `{hangzhou, genua}`, all per-tick checks green. Same code as the harness, now
   in a live address space.
3. **Hook seams** (`hooks.h`) — the 7 live-memory seams are declared with their purpose and the
   signature slot to fill; all report **pending** and the mod runs **read-only** until a debugger
   session resolves them. Nothing fabricates an offset.

## Data-file mod — installed and validated in the running game

`mod/pgt/` carries the emitted `00_tradenodes.txt`; enabled via `dlc_load.json`. Loaded a Castile
1444 campaign on the actual EU4 1.37.5 install and observed:
- **A1 PASS** — 0 `tradenodedefinition.cpp` declaration-order errors, no `EXCEPTION_STACK_OVERFLOW`,
  game runs. Since the engine hard-crashes on a cyclic file, this is the emitter's acyclicity
  proven against the real engine.
- Mod active (achievements-disabled gate fired).
- Trade reoriented — Tunis steers to Valencia where vanilla sent it to Sevilla; the Sevilla node
  window renders the reoriented connected-node tabs.

## Live-memory RE — trade structures LOCATED (build 835bfdf8)

Original RE (the community has published no EU4 trade-node offsets). Confirmed and baked into
`dll/hooks.h` (`tradeoff::`):
- **`CTradeNode` definition vtable = eu4.exe+0x1C439D0** — a pointer-scan enumerates all 80 nodes;
  name is an inline `std::string` at obj+0x10. `memtool nodes` prints 72+ live node names from the
  running game — the DLL's live-read path, proven.
- **TradeNodeDatabase singleton = .data eu4.exe+0x242B8C8**; **monthly tick = eu4.exe+0x2F374D**;
  **serializer = eu4.exe+0x13CFFB7** (iterates every node, every field).
- **`local_value = *(i32*)(*(void**)(node+0xF8)+0xB4) / 1000`** (fixed-point ×1000, the spec's
  quantization); the +0xF8 sub-object holds the stable per-node production values (§1.8 inject).
- The HW-breakpoint **tracer works** (SuspendThread + DR7 LE + RF for exec BPs); it caught trade
  code reading a stable node struct during a tick.

**Still open for a working per-good DLL:** the complete runtime `CTradeNode` field map (the
fluctuating power/total live in pooled/reallocated memory; the sub-object's per-good array needs
labelling against `trade_goods_size`), the tick write-back at 0x2F374D, the node-window UI, and AI.
EU4 ignores synthetic keyboard (raw input) so a manual save can't be triggered to capture the
serializer's runtime `r14`; autosave is off this session. Next step: hook the tick, or exec-BP the
serializer during a real save, to finish the field map.

## (earlier) Live-memory RE — toolkit

Two standalone tools were built and work against the running eu4.exe (pid confirmed, build gate
matches):
- **`dll/memtool.cpp`** — 20 commands: `proc`, `scan-float/double`, `scan-floats/doubles`
  (struct fingerprints), `scanlist`/`refine`/`snap`/`keepchanged`/`keepsame` (Cheat-Engine-style
  change scanning), `fseq` (array-in-node-order), `near`, `read`/`rdump`, `write-float/double`.
- **`dll/tracer.cpp`** — a real debugger: `DebugActiveProcess` + debug-register (DR0–3) hardware
  breakpoints on data read/write, logging every accessing RIP as `eu4.exe+offset` with the full
  register set. Detaches cleanly.
- **`tools/xref.py`** — static PE/capstone cross-reference finder over `eu4.exe`.

**What the RE established (all negative — the structs are hidden):** the displayed trade values
(node local/incoming/outgoing/total, per-country retained values and powers) are float, and every
value-scan hit is a **transient display cache**, not the sim: pokes to them don't change the UI,
HW write-breakpoints on them catch **0 writes** during monthly ticks, and they're reallocated on
each window open. Statically, the trade `__FILE__`/assert strings (`tradenode.cpp`,
`trademanager.cpp`, `tradenodedatabase.cpp`) exist in `.rdata` but have **no** code xref (asserts
compiled out of the release build), and no absolute-VA pointer references them.

**Conclusion:** the sim node array is pointer-chased and reference-stripped; locating it needs the
heavier RE workflow the spec calls the schedule risk — a Cheat-Engine pointer-scan (multi-level
pointer path from a static base to a node value) or IDA/Ghidra with type reconstruction, driven
iteratively. That is the concrete next step, and the tracer + memtool are the instruments for it.

Every ★ test in `TESTING.md` (map numbers, per-good views, monthly money, merchant-on-any-end, AI)
needs the sim node array + tick hook found first, so they remain pending that RE.

## AI merchant placement -- the frontier model (user-specified, 2026-08-26)

Replaces spec 3.14's scorer. Home = trade capital; network = home + nodes with the country's
merchants; candidates = frontier edges (one end in, one out; merchant stands outside, steers in);
score = inward flow x product of (my power / all power) at each node on the shortest network
path home x share at home; a merchant moves only if a candidate beats the weakest current one
by x1.5. Merchants never collect (user decision; spec 3.14 line 787 says collect/steer is vanilla
-- this diverges and should be folded into the spec).

**Offline regression test, no game:** `impl/aitest.exe <eu4_root> <VANILLA_start.eu4>
<standings1444.json> TAG[,k] ...` drives the real `src/frontier.h` from the save. Expected on
1444: MNG hangzhou->beijing 11.78, xian->beijing 11.38 (reverse Phi_w ends toward home), 3rd
canton->hangzhou 2.92; CAS safi->sevilla 0.62; VEN ragusa->venice 0.38. Regenerate the standings
with the extractor in the session log if the save changes.

**In-game (f7c51dc):** choices match the offline test; the gap is that 1,005 merchants stand off
their frontier because envoy travel is not driven. The send-merchant command is the next trace.

**Two-year run (pgt_sil2, 24 ticks):** G1 26% reverse-end placements, G2 zero churn, 516/527 placements
held, E1 636/636, E4 CLEAN. `4,598 refused: no free merchant` is the plan wanting more merchants than
countries own -- the model saturating, not a defect. Vanilla's merchant AI is silenced at 0x1B831D.
