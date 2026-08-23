# Round-4 values, to be independently confirmed

Answering the third validation pass (158 CONFIRMED / 24 PARTIAL / 1 REFUTED over Y001–Y183). Applied
as 17 replacements, entries 136–152 of `changes-v6.md`. Every row below is already in the document, so
a mismatch means an edit to the spec rather than a change of plan.

One mechanism addition: **`scripts/relabel6.py`** now ships the node-order experiment §1.6 and §2.4
quote. Two audits found those figures attributed to scripts that did not contain them. It validates
its instrument against `drain.py` on the identity permutation and aborts if that fails.

---

## Numeric values

| id | quantity | what the spec now says |
|---|---|---|
| Q01 | relabellings where the orientation changed | **800 of 800** (8 seeds × 100) |
| Q02 | mean edges moving under relabelling | **25** of 159 |
| Q03 | relabellings returning the baseline sink set | **64 of 800** |
| Q04 | relabellings where `hangzhou` is an end | **786 of 800** |
| Q05 | relabellings where `english_channel` is an end | **322 of 800** |
| Q06 | other frequent end holders | `gulf_of_siam` 459, `wien` 259, `rheinland` 122, `sevilla` 112 |
| Q07 | LP objective deviation across relabellings | within **4.44e-16** |
| Q08 | `Φ_ord` ends terminating no good | **7 of 14** — half, not a majority |
| Q09 | Cape of Good Hope land provinces | **20** |
| Q10 | Channel basin under European growth | 18 → 28 by about **×1.44**, then the end migrates to `genua` past about **×1.70** |
| Q11 | spice-sink **wealth** multiples | `beijing` 3.63×, `hangzhou` 4.13×, `xian` 4.61×, `canton` 4.78×, `girin` 3.89×, `yumen` 4.49× |
| Q12 | dev-scaled vs wealth-scaled wealth, max difference | **0.0** — and the check must recompute from development, not compare `W·k` to `W·k` |

## Statements

| id | claim |
|---|---|
| P01 | The proportions in Q04/Q05 are pooled over all 800 draws because a per-seed range is itself seed-dependent: two honest runs gave 97–100 and 96–100 per hundred for the same quantity. |
| P02 | The spice figures are multiples of a node's **wealth**, not of its demand; and the four named nodes are not the cheapest — `girin` needs less than three of them. |
| P03 | The two-test classifier is v4.0's; v3.0 used a structural rule about which block of a trade-good definition a modifier sits in. The whole-install sweep is v5.0's alone. |
| P04 | The ID that refuted the classifier is `validation-v5.md` X035, not X030 or X034. |
| P05 | "off by 5.96 ducats on a node paying ~250" spans v1 through v3.0; v4.0 deleted it and its own harness asserted the deletion. |
| P06 | `verify6.py` checks the `change_price` census only by matching a printed total against a computed one, not by reconciling per file; and `measure6.py`'s walker still swallows parse failures in a bare `except`. |
| P07 | Every magnitude and direction in §1.3's province-state table is read from `00_static_modifiers.txt`. What no file states is the **scaling law** for `devastation` — the model's `-2 × level/100` proportionality is an assumption. |
| P08 | On the razed field, `hangzhou` loses its end under every relabelling tried, which is what §2.8's row asserts. |

## What to confirm

For each Q-row, compute the value independently and report what you get. For Q01–Q07, validate the
instrument against `drain.py` on the identity permutation first — it should reproduce 159 of 159
edges, a Phase-0 core of 80, 2 promotions and 0 fallbacks — and say what the validation showed. Note
that a test built on `drain.py`'s `sweep_priority(pid=…)` hook reports no change at all, that a
reimplementation omitting Phase 0, Phase 1 or Phase 4 reports wild instability, and that
`solver.EDGES_UND` is a sorted set so a genuine relabelling must re-sort the arc list.

For each P-row, settle the claim against the file, script or document it is about.
