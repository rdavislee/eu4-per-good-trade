# Round-3 values, to be independently confirmed

Negotiated with the no-context validation agent that graded `claims-v6.md`
(145 CONFIRMED / 24 PARTIAL / 5 REFUTED over Y001–Y174).

**Process note, stated because it matters for how this file should be read.** In the previous round
these values were measured by an independent agent *before* being written into the specification. This
round they were **applied first** and are being confirmed after, which is the wrong order — a wrong
value has already landed in the document rather than being stopped at the door. Treat every row below
as unconfirmed until measured, and expect the correction to be an edit to the spec rather than a
change of plan.

Two mechanism changes accompany them:

- **`verify6.py`** gained five checks for figures `coverage6.py` reported unguarded, a
  cross-phrasing value check (`every_site`), content-based routing, and a non-empty-run guard.
- **`coverage6.py`** is new: it corrupts each spec-printed figure whether the harness checks it or
  not, which is the honest coverage denominator. `mutate6.py`'s score is not that number and the
  spec now says so.

---

## Numeric values now in the spec

| id | quantity | what the spec now says | was |
|---|---|---|---|
| R01 | max `base_tax` over counted provinces | **15**, at province 1821, with total development 33 there | "runs up to 33" |
| R02 | razed-`hangzhou` edge flips | **22** of 159 | 23 |
| R03 | the deleted apparatus | **105.30 ducats**, 0.99% of 10,607.40, or 0.98% of the 10,712.70 the field totalled with it | "0.98% of world wealth", no denominator |
| R04 | tax tooltip schema | `Base: trunc(base_tax × 0.0833333) (Yearly base_tax)` | `trunc(base_tax / 12)`, which gives 0.50 where 0.49 was observed |
| R05 | the 0.6125 attribution | **v4.0 and v5.0** | "v3.0 through v5.0" — v3.0 says "giving 0.61" |
| R06 | relabelling: orientation changes | **100 of 100** | not stated |
| R07 | relabelling: mean edges moving | **26** of 159 | not stated |
| R08 | relabelling: baseline sink set returned | **8 of 100** | not stated |
| R09 | relabelling: `hangzhou` is an end | **100 of 100** | not stated |
| R10 | relabelling: `english_channel` is an end | **40 of 100** | not stated |
| R11 | relabelling: other frequent end holders | `gulf_of_siam` 55, `wien` 37, `sevilla` 19 | not stated |
| R12 | relabelling: sink-count range | 1 to 5, most often 2 | not stated |

## Statements now in the spec

| id | claim |
|---|---|
| T01 | Of §1.6's two ends, `hangzhou` is a property of the world and `english_channel` is a property of the node ordering. The rest of §1.6 is conditional on one canonical order. |
| T02 | The Europe table's *direction* is the claim; which European node holds an end at a given factor is ordering-dependent. |
| T03 | §2.4's end-flag list is a function of the canonical node order, not of the world alone. |
| T04 | §2.8's razed-China row is ordering-**robust**, because it turns on `hangzhou` holding an end. |
| T05 | `verify6.py` does not cover every figure the document prints; under half are guarded and the rest rest on their script attribution. `mutate6.py` cannot fail, because it plants errors only in figures already checked. |
| T06 | §3.15 maintains no copy of the supply/demand contrast figures or RANK's stranded-demand share; both are directional, with §3.2 holding the one measurement. |
| T07 | §3.10 quotes no magnitude of its own for the per-good propagation error. |

## What to confirm

For each R-row: compute the value independently and report what you get. For the relabelling rows
R06–R12, note that a test built on `drain.py`'s `sweep_priority(pid=...)` hook reports **no** change
(it re-keys only the sweep, leaving Phase 1, the promotion and Phase 2's LP on the true index), and a
partial reimplementation that omits Phase 0, Phase 1 or Phase 4 reports wild instability. Validate
whatever instrument you use against `drain.py` on `Φ_w` **before** drawing a conclusion: it should
reproduce 159 of 159 edges, a Phase-0 core of 80, 2 promotions and 0 fallbacks.

For each T-row: the claim is about the document, a script, or an algebraic fact — settle it against
that source and report what it says.
