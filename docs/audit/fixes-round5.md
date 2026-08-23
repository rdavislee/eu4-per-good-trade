# Round-5 fixes, to be independently confirmed

Answering validation round 4 (168 CONFIRMED / 19 PARTIAL / 1 REFUTED over Y001–Y188), negotiated with
the agent that produced it. **The spec is frozen at `f597de9d10ade20b0e69c5089932e8b4`; nothing here is
applied.** Measure every row before it is written.

Seven of the nineteen partials repair by **deletion** rather than re-measurement (Y080, Y084, Y086,
Y092, Y106, Y129, Y132). Only Y047 adds anything. That ratio is the shape of what is left in this
document: figures quoted more precisely than their sample supports.

---

## Values

| id | quantity | proposed | now |
|---|---|---|---|
| V01 | provinces with `unrest` > 0 at 1444, counted | **21** | absent |
| V02 | their unrest values | 4.834 ×1, 7.834 ×3, 9.834 ×6, 14.834 ×11 | absent |
| V03 | tax forgone to `unrest` at −0.02 per point | **12.23 ducats**, 0.115% of world wealth | absent |
| V04 | `Φ_w` edge flips caused by admitting `unrest` | **0** | absent |
| V05 | LP objective, identity permutation | **0.712275977829** | absent |
| V06 | LP objective, max relative deviation under relabelling | **6.235e-16** over 40 permutations | 4.44e-16 |
| V07 | permutations returning a different optimal support | **40 of 40** | absent |
| V08 | distinct numeric figures the spec prints | **303** | "roughly three times a dozen" |
| V09 | distinct numeric figures `verify6.py` pins | **35**, across 29 checks | absent |
| V10 | `Φ_ord` ends terminating no good | **7 of 14** — half, and *not to be printed* (see T04) | "half … (7 of 14 …)" |
| V11 | `NEW_DRAPERIES` single-event floor for `wool` | **1.875** — correct for the 13/2/4/11 partition | 1.875, applied to a campaign |
| V12 | `wool` in a campaign reaching 1540 | between **1.625 and 1.6875**, composition rule unknown | 1.875 |

## Statements

| id | claim |
|---|---|
| T01 | `unrest` is a **fifth** province-state modifier entering wealth via `local_tax_modifier = -0.02`. Its per-point scaling **is stated in the file** — the `unrest` block's own comment reads `#…for each rr`, and `nationalism` uses the same convention. |
| T02 | `devastation` is therefore the **only** unverified scaling law in §1.3: its block carries no per-unit comment, though the convention exists in that same file. |
| T03 | The 580-of-580 relabelling sweep is a real result from `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`, which exists in the tree. v6.0 withdrew it on the false ground that its script was never shipped; the withdrawal is reversed and the citation corrected. |
| T04 | §3.9 says "half of them terminate no good at all" with **no parenthetical figure**. The count has been 9 → 10 → 8 → 7 across four versions while the end count moved 13 → 14; the disclaimer six lines below ("no figure is maintained for it here") then stands honestly. *("A majority" is false — 7 of 14 is exactly half — so the previous round's fix and this round's cannot both be taken; this is the resolution of that conflict.)* |
| T05 | No basin figure is quotable. Across 60 relabellings the ×1.00 basin ranges **16–75** against a shipped 18, and at ×1.53 the shipped 33 falls **outside** the 24–29 range the orderings produce. §1.6 states the basin widens non-monotonically and the end migrates to `genua` at ×1.64, and nothing more. |
| T06 | **Basin size is added to §1.6's list of quantities conditional on the node order**, which currently names sink membership and size but omits it. |
| T07 | §0 states two directly checkable counts — the spec prints 303 distinct figures, the harness pins 35 — instead of a ratio. The ratio has moved four times inside this version. |
| T08 | `relabel6.py` computes the LP objective it is credited with, and where its reimplementation cannot produce a figure it says so rather than letting the citation stand. |

## What to confirm

Compute every V-row independently. Three deserve particular attention because the batch depends on
them most:

- **V04**, that admitting `unrest` moves no edge — a fidelity correction with no orientation
  consequence is a different kind of change from one that moves the map.
- **T05's ordering table**, including the claim that the shipped basin at ×1.53 lies outside the range
  its own relabellings produce.
- **V12**, the composition of two simultaneous `change_price` keys. No save in the install is believed
  to carry a good with two live keys; if that holds, the campaign value is genuinely unknown between
  the two bounds and should be stated as unknown rather than resolved.

Validate any instrument against `drain.py` on the identity permutation first — 159 of 159 edges, a
Phase-0 core of 80, 2 promotions, 0 fallbacks — and say what the validation showed. A test built on
`drain.py`'s `sweep_priority(pid=…)` hook reports no ordering effect at all; a reimplementation
missing a phase reports the shipped answer with no flips, or wild instability, depending on which
phase. `solver.EDGES_UND` is a sorted set, so a genuine relabelling must re-sort the arc list.
