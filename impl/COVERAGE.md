# Coverage ledger — every spec section and every TESTING.md test

The single list that decides when the mod is done. Updated as each item lands.
Status: **DONE** (built and verified) · **LIVE** (running in the game) · **PARTIAL** · **OPEN**.

## Spec sections

| § | Requirement | Status | Where / what remains |
|---|---|---|---|
| 1.1 | Trade direction = DRAIN (peel → HHI → b-flow → sweep) | **DONE** | `drain.h`; exact parity with the reference, 30/30 graphs |
| 1.2 | Supply | **DONE** | `field.h` |
| 1.3 | Demand, owner-agnostic wealth | **LIVE** | `field.h` + `liveworld.h`: read from the live province table each month (2483 provinces / 10724.7 at 1452 vs 2472 / 10607.4 at 1444) |
| 1.4 | Market concentration α | **DONE** | `field.h` |
| 1.5 | Goods without a graph (latent) | **LIVE** | the monthly re-solve rebuilds the live-good set from live production each month, so a good activating mid-campaign gets its graph that month |
| 1.6 | Aggregate graph Φ_w | **DONE** | ends {genua, hangzhou} |
| 1.7 | Merchants: incoming-entry assignability; caravan needs actual steering | **PARTIAL** | assignment on either link end works in the model (`assign.h`, merged into routing, keyed by link END so flips leave it alone). The engine's own `steer_command` cannot express it — it writes an INDEX into the node's outgoing list, and a Φ_w-incoming link has no index there. The click gate is OPEN (5-byte patch at 0x8317EF). Remaining: the caravan condition (C5) |
| 1.8 | Collection/transfer, per-good eligibility, steering, sinks | **LIVE** | routing reads the real merchant field (1369 power entries, 330 steering in 1448) |
| 1.9 | Trade power propagation | **DONE (preserved)** | vanilla's own; the mod must not disturb it — regression-check after gate work |
| 1.10 | Direction gates evaluate TRUE | **OPEN** | three uint8 matrices G+0x2220/0x2228/0x2230, rebuilt at 0xB4BD0A → fill after rebuild |
| 1.11 | Treasure fleets always granted, route by the ladder, privateers skim | **OPEN** | router 0x3E1EC0; needs a detour at 0x3E2358, NOT just a table fill (else zero-hop teleport) |
| 1.12 | Displays: six fields, both link directions, per-good swap-on-view | **PARTIAL** | aggregate numbers LIVE; Φ_w is the drawn direction and now re-orients at runtime (arrows + node-window lists). Two-way panels + per-good arrow layer OPEN |
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
| B1 ★ map draws Φ_w | **PASS** | the definition graph is re-oriented at runtime (79–88 links/month) and the drawn arrows follow. Controlled A/B: pump `baltic_sea` and the Gulf of Finland arrows point west; pump `novgorod` and the same arrows point east, with the log naming `novgorod → baltic_sea became baltic_sea → novgorod`. Stable 1470→1502 |
| B2 ★ node numbers | **PARTIAL** | six fields reconcile via the engine's own identity; per-good views remain |
| B3 ★ both directions per link | **PARTIAL** | gross directed values written (never negative); second panel is UI work |
| B4 local == engine's own | **PASS** | local never written |
| C1–C5 ★ merchant on any link end | **PARTIAL** | the MODEL half works: `assign.h` holds assignments keyed by (country, link END) and merges them into routing, so a merchant on a Φ_w-**incoming** edge steers the goods oriented away from that node — verified live at `baltic_sea → lubeck`, an edge the engine has no index for. Keyed by END, so it survives a flip untouched (spec 1.7). The click gate is OPEN (5-byte patch at `0x8317EF`), and C5's caravan condition is installed (call-site redirect at `0xB53CC5`: a merchant steering no good on its link has its computed caravan power zeroed, and vanilla's own zero-means-no-grant path does the rest). Remaining: exercising both end-to-end in-game |
| D1–D5 ★ per-good view | **OPEN** | no engine-side "selected good" exists; entirely DLL-owned (arrow layer + widget repopulation) |
| E1 ★ country income matches the model | **PASS** | **592/592, 589/589, 588/588 countries agree**; worst \|diff\| 0.0015 ducats (the milli-ducat grid). Spec 3.10's identity confirmed live |
| E2–E4 ★ monthly money | **OPEN** | treasury reconciliation, world total vs a null run, NaN/leak soak |
| F1 flip honoured end to end | **PASS** | a flip re-orients the definition graph, the arrows, the node-window lists and the value in the same tick; verified by the shock A/B above |
| F2 razed China | **PASS (harness)** | {genua, gulf_of_siam} |
| F3–F5 console scenarios | **OPEN** | needs the monthly re-solve |
| F6 devastation scaling (probe 18) | **OPEN** | read two windows |
| G1–G4 ★ AI | **OPEN** | wire `ai.h` to live merchants |
| H1 determinism live | **PARTIAL** | harness identical; live save/reload repeat remains |
| H2 mid-campaign load | **PASS** | 1448 save loaded and installed cleanly |
| H3 tick cost | **PASS** | 11–12 ms measured over 16 months |
| H4 long-run soak | **OPEN** | 1444→1600 observer run |

## Critical path (in order)

1. ~~Monthly re-solve + runtime re-orientation~~ **DONE** — arrows and node-window lists both follow the solve (B1, F1).
2. **Merchant on any edge** (§1.7 interaction) → unlocks C1–C5.
3. ~~E1~~ **PASS**. E2–E4 remain.
4. **Per-good views** (§1.12) → D1–D5.
5. **AI wiring** (§3.14) → G1–G3.
6. **Direction gates + treasure fleets** (§1.10, §1.11) → G4.
7. **Probes** 1–11, 17–19; **F6**; **H1 live**, **H4 soak**.
