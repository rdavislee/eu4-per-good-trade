# Coverage ledger — every spec section and every TESTING.md test

The single list that decides when the mod is done. Updated as each item lands.
Status: **DONE** (built and verified) · **LIVE** (running in the game) · **PARTIAL** · **OPEN**.

## Spec sections

| § | Requirement | Status | Where / what remains |
|---|---|---|---|
| 1.1 | Trade direction = DRAIN (peel → HHI → b-flow → sweep) | **DONE** | `drain.h`; exact parity with the reference, 30/30 graphs |
| 1.2 | Supply | **DONE** | `field.h` |
| 1.3 | Demand, owner-agnostic wealth | **DONE** | `field.h`; 2472 provinces, world wealth 10607.40 |
| 1.4 | Market concentration α | **DONE** | `field.h` |
| 1.5 | Goods without a graph (latent) | **DONE** (solver) | live re-check when a latent good activates → folded into the monthly re-solve |
| 1.6 | Aggregate graph Φ_w | **DONE** | ends {genua, hangzhou} |
| 1.7 | Merchants: incoming-entry assignability; caravan needs actual steering | **OPEN** | the UI interaction + the caravan condition. Path known: click 0x13CCE80 → dispatch 0x831790 → gate 0x1418E70 → `steer_command` (token 0x2DB9, Execute 0x5DA4F0) |
| 1.8 | Collection/transfer, per-good eligibility, steering, sinks | **LIVE** | routing reads the real merchant field (1369 power entries, 330 steering in 1448) |
| 1.9 | Trade power propagation | **DONE (preserved)** | vanilla's own; the mod must not disturb it — regression-check after gate work |
| 1.10 | Direction gates evaluate TRUE | **OPEN** | three uint8 matrices G+0x2220/0x2228/0x2230, rebuilt at 0xB4BD0A → fill after rebuild |
| 1.11 | Treasure fleets always granted, route by the ladder, privateers skim | **OPEN** | router 0x3E1EC0; needs a detour at 0x3E2358, NOT just a table fill (else zero-hop teleport) |
| 1.12 | Displays: six fields, both link directions, per-good swap-on-view | **PARTIAL** | aggregate numbers LIVE (no UI hook needed — everything recomputes from the sim fields). Two-way panels + per-good repopulation OPEN |
| 2.1 | Shape: runtime DLL, single-player, build discipline | **DONE** | |
| 2.2 | Solver deliverables 1–8 | **DONE** | incl. census + survival table |
| 2.3 | Constants from files, tie-break, pinned tolerance | **DONE** | |
| 2.4 | Emitted `00_tradenodes.txt` | **DONE** | A1–A3 pass in-game |
| 2.5 | Runtime attachment + build gate | **DONE** | refuses non-target, passes on 835bfdf8 |
| 2.6 | Writing to the engine at the tick | **LIVE** | inline hook at 0xB4BF09, 11–12 ms/tick |
| 2.7 | Probes 1–11, 16–19 | **PARTIAL** | 16 SETTLED (quantisation is in the sim). 13/14/15 settled pre-existing. Rest open |
| 2.8 | Validation battery | **DONE** (reference side) | live-side rows land with the tests below |
| 2.9 | Build order, both tracks | **DONE** | solver track complete; memory track complete enough to run |
| 3.14 | AI merchant assignment, shadow-vanilla cadence | **PARTIAL** | `ai.h` logic + fixtures built; NOT wired to live merchants. Vanilla's own cadence measured: 10+rng()%15 days, ×1.5 hysteresis (0x1BD206) |

## TESTING.md — the ★ bar

| Test | Status | Evidence / what remains |
|---|---|---|
| A1 file loads clean | **PASS** | 0 declaration errors, no crash, repeatedly |
| A2 end flags | **PASS** | {genua, hangzhou}, venice gone |
| A3 round-trip residue | **PASS** | byte-identical outside the intended diffs |
| A4 build gate | **PASS** | refuses non-target, passes target |
| A5 cross-impl orientation | **PASS** | EXACT, 30/30 graphs |
| B1 ★ map draws Φ_w | **PARTIAL** | arrows ARE Φ_w at load (Tunis→Valencia proven); they do not yet change month over month → needs the monthly re-solve + arrow rebuild (0x10AFA70) |
| B2 ★ node numbers | **PARTIAL** | six fields reconcile via the engine's own identity; per-good views remain |
| B3 ★ both directions per link | **PARTIAL** | gross directed values written (never negative); second panel is UI work |
| B4 local == engine's own | **PASS** | local never written |
| C1–C5 ★ merchant on any link end | **OPEN** | reading the merchant field works; the assignment interaction is the gap |
| D1–D5 ★ per-good view | **OPEN** | no engine-side "selected good" exists; entirely DLL-owned (arrow layer + widget repopulation) |
| E1–E4 ★ monthly money | **IN PROGRESS** | pool lands where pass 10 divides it; E1 reconciliation being measured |
| F1 flip honoured end to end | **PARTIAL** | flips now happen monthly and value rebuilds around them; the arrow redraw + the staleness instrumentation remain |
| F2 razed China | **PASS (harness)** | {genua, gulf_of_siam} |
| F3–F5 console scenarios | **OPEN** | needs the monthly re-solve |
| F6 devastation scaling (probe 18) | **OPEN** | read two windows |
| G1–G4 ★ AI | **OPEN** | wire `ai.h` to live merchants |
| H1 determinism live | **PARTIAL** | harness identical; live save/reload repeat remains |
| H2 mid-campaign load | **PASS** | 1448 save loaded and installed cleanly |
| H3 tick cost | **PASS** | 11–12 ms measured over 16 months |
| H4 long-run soak | **OPEN** | 1444→1600 observer run |

## Critical path (in order)

1. **Monthly re-solve + arrow rebuild** → unlocks B1, F1, F3, F4, F5, and 1.5's latent-good activation.
2. **Merchant on any edge** (§1.7 interaction) → unlocks C1–C5.
3. **E1–E4** money reconciliation.
4. **Per-good views** (§1.12) → D1–D5.
5. **AI wiring** (§3.14) → G1–G3.
6. **Direction gates + treasure fleets** (§1.10, §1.11) → G4.
7. **Probes** 1–11, 17–19; **F6**; **H1 live**, **H4 soak**.
