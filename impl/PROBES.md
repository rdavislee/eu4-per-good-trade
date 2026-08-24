# Acceptance ledger — TESTING.md tests and spec §2.7 probes

Recorded by test id / probe number as the live sessions settle them (CLAUDE.md: "record results
by probe number"). Status: **PASS** (seen in the running game), **PASS (harness)** (reference-side
check, no engine needed), **OPEN**. Evidence is the log line, screenshot or dump named.

## A. Load and attach

| Test | Status | Evidence |
|---|---|---|
| A1 emitted file loads clean | **PASS** | 0 `tradenodedefinition.cpp` errors, no `EXCEPTION_STACK_OVERFLOW`, campaign plays (session 2026-08-23); mod-active gate fires on every Continue |
| A2 end flags | **PASS (harness)** + in-game | `impl.exe emit`: ends `{genua, hangzhou}`, venice not an end; loaded file is the one the game runs |
| A3 round-trip residue | **PASS (harness)** | `emit.h` A3 residue byte-identical; independently re-parsed |
| A4 DLL attaches on this build only | **PASS** | `loadtest.exe` → `REFUSE` on a non-target host; `selftest_host.exe` → `build gate PASS` on 835bfdf8 (accept.ps1) |
| A5 cross-implementation orientation | **PASS (harness)** | `tools/compare.py`: EXACT ORIENTATION EQUALITY 30/30 graphs; the same solver code runs in-process (`solver self-test` log line) |

## B–H (engine-side)

| Test | Status | Notes |
|---|---|---|
| B1 map draws Φ_w | OPEN | emitted file is Φ_w; arrow-layer spot check pending |
| B2 node numbers = per-good economy | **PARTIAL PASS** | Sevilla node window reads Incoming +2.93, Local +7.18, Outgoing -9.16, **Total 0.94** — the engine's identity `total = local + Σincoming − outgoing` closes on the model's numbers; 80 nodes + **159 link values** written per install. Per-good (D) views still open. |
| B3 both directions on every link | **partial** | link values are written as GROSS directed flows (never negative, spec 1.12); the second directional panel per link is the remaining UI work |
| B4 local value equals the engine's own | **PASS** | local (+0xB4) is never written; the node window shows the engine's own +7.18 while the model drives pool/outgoing/links. Model annual local 3919.44/12 = 326.6 vs engine 337.9 monthly = the recorded 3.4% reference-side gap (spec 2.8), not a mod defect |
| C1–C5 merchant on any link end | **partial** | the mod now READS the live merchant field: 1134 country-node power entries, 707 collecting, 171 steering, with each steerer's target link resolved — routing uses real steering (spec 1.8), not the even split. Assignment-on-incoming-entry (the UI change) still open |
| D1–D5 per-good view | OPEN | UI hook |
| E1–E4 monthly money | OPEN | path identified and coded: pool → node+0xB0 and per-country power_fraction → rec+0x2C, consumed by the engine's own pass 10 (`rec.total = current*pf/1000`, `money`, `AddDelayedIncome(country, 2)`). Needs the tick hook at 0xB4BF09 to land inside the pass |
| F1–F6 | OPEN (F2 PASS harness: razed hangzhou → `{genua, gulf_of_siam}`) | live inputs needed for F1/F3/F4/F5 |
| G1–G4 | OPEN | AI wiring |
| H1 determinism | **PASS (harness)** | 3 re-solves identical fingerprint; live repeat pending |
| H2–H4 | OPEN | |

## §2.7 probes

| Probe | Status | Result |
|---|---|---|
| 13 cyclic file | settled (spec) | hard crash |
| 14 incoming-link button | settled (spec) | navigates only |
| 15 propagation qualifier | settled (spec) | not a precondition |
| **16 quantisation: sim or serialiser?** | **SETTLED: in the simulation.** | Every CTradeNode value field is an `int32` fixed-point ×1000 in live memory (`+0xB0/+0xB4/+0xB8/+0xBC/+0xC4/+0xCC`, and the 33-slot `trade_goods_size` vector) — e.g. the live read `local=57.129` is the int 57129; the write path stores `round(ducats×1000)`. The engine erases sub-milli-ducat divergence every tick in the sim itself, not only in the save writer. Consequence for the mod: round at the write boundary (the DLL already does), and — as the spec says — this does not bear on the solver's own margins. Evidence: `dll/hooks.h` offsets, `livetrade::read_sim_nodes`, live TSV dump `per-good-trade.log.nodes.tsv`. |
| 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 17, 18, 19 | OPEN | folded into the sessions TESTING.md §I maps |
