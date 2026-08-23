# Round-6 fixes — negotiated, awaiting preconfirmation

Answering validation round 5: **894 verdicts across four slices — 672 CONFIRMED, 83 PARTIAL, 14
REFUTED, 125 UNTESTABLE.** Every item below was negotiated to unconditional confirmation with the
agent that raised it. **The spec is frozen at `59c84a97799db9db97fe889b6e3c6776`; nothing here is
applied.** Measure every figure before it is written.

**47 rows.** Four of them state on their face that they correct an earlier draft of the same row
(B7, D3, D8, D9); more were corrected during negotiation, but this file records agreed text rather
than its history, so that count is not derivable from what is written here and no number is given
for it. What can be said precisely: the harness group **D** has ten rows, more than any section of
the document contributes, and every one is the same defect — a check that trusts a declaration
rather than measuring behaviour. That is why this list goes to preconfirmation rather than straight
to the document.

---

## A. The wealth model (R1)

| # | change | source |
|---|---|---|
| A1 | `unrest` moves to §1.3's excluded list beside autonomy. Rebels want the owner changed, so revolt risk is a relation between a province and its ruler; `tax_value` measures the province's buying power, which exists whether or not the owner collects it. | owner ruling |
| A2 | Every unrest figure **retired, not repaired** — 12.23, 9.40, the 4-of-159 edges, the 16/5 split, the Shirvan claim, `revolt_risk` parsing. No replacement figure and no directional sentence. | P1 Y057/Y983 |
| A3 | `tax_value(p) = TAX_COEFF · base_tax(p)` — the `(1 + Σ province-state tax modifiers)` factor dropped rather than left an empty sum. | owner ruling |
| A4 | `STATE_TAX_MOD = {}` kept as a declaration of intent; **not** deleted. | P1 |
| A5 | §1.3's table becomes **four** rows, all reaching `goods_produced`. Claim narrowed: *the wealth rule carries four; on the 1444 start only `devastation` is live, and the other three have no input until the emitter reads live province state.* Eight sites edited. | P1 |

## B. The operator and its figures

| # | change | source |
|---|---|---|
| B1 | §1.6's **Scale paragraph deleted entirely** (L487–497), with §2.3's cross-reference. Seven measured attempts failed the same way. | owner ruling |
| B2 | §3.13's "tolerance is scale-coupled" **closed, not deleted**: coupling is to the *primal* tolerance; hazard unreachable structurally since `\|b\|max ≥ 1/N`; scaling the tolerance is not available — below 1e-10 HiGHS rejects with `Invalid option value`, `success` stays true, and it silently reverts to 1e-7. | P2 |
| B3 | §2.8 spice/cloves: `Deccan` → **`beijing`**; the v2 retraction deleted (v2's sentence was correct — `spice` names the class, the parenthetical specifies the member); "not recovered by the calibration" qualified to **no single good**. | P3 Y538/Y539 |
| B4 | §2.8 razed-China: 30 → **32** flips; "v2 through v4.0" → **v4.0** alone. | P3 |
| B5 | §2.8 barbell: 19.8%/6.9% → **19.4%/7.3%** (45/17 of 232); per-good sinks 1–8 → **2–8**. | P3 |
| B6 | §2.3's structured-second-term note: both costs make all 159 arc costs distinct, so the contrast is the **mechanism** — `\|w[u]−w[v]\|` telescopes, `frac(lo·hi·7919)` does not — and 11 of 29 goods against 0. | P3 Y999 |
| B7 | §2.3 normalisation: **7 of 159** aggregate under world-total, **13 of 29** per-good. Both cautions kept: `w/mean` and `N·w/sum` are the same vector, and an unpinned solver **undercounts** (5 against 9, a subset). | P3 Y1038 |
| B8 | §3.9's `Φ_ord` bullet rebuilt on the **sweep key** (14/8/8 against `Φ_w`'s 2) — relabelling cannot separate the operators because the tie-break made both stable. Trade stated two-against-two. | P4 Y178 |
| B9 | §3.9's degree clause replaced by the flow identity: `flow_in − flow_out = −b_w > 0`, 36 of 36, residual 5.2e-17, plus 18 of 80 nodes with out-degree > 0 and zero outgoing flow. | P4 Y684 |
| B10 | §3.2's conduit claim evidenced by **flow**: 28 of 29, `paper` the exception, `cape_of_good_hope → malacca` named as the same fact twice. | P4 Y614 |
| B11 | §3.6's margin fragility: 7.53e-06 at α=2.0 but **1.267e-07 at α=1.5**; two of 29 per-good solves inside the 1e-7 default (`copper`, `paper`), 27 above. | P4 |
| B12 | §3.10/§3.15: §3.15 keeps its verdict, loses "breaks the income factoring", keeps Goal 7 via the fictitious power field. Y183's residual dropped entirely. | P4 |
| B13 | §3.13's calibration figures dropped per the `Φ_ord` precedent — span, spearman, reach digit — configuration and qualitative costs kept, with `changes-v5.md` §39–41 provenance. | P4 |
| B14 | §1.6's Europe table **dropped**; headline kept with its resolution: ×1.974–×2.457, uniform on a 0.001 grid, three European ends and none in Asia. | P2 |
| B15 | §1.6 gains a sweep-key scope statement: seven of its figures change under a different key, including both long routes — the Iberian one ceasing to exist. "Unprompted" goes. | P2 |
| B16 | §1.10/§3.x: Y412 narrowed — *nothing names a node, nothing tests direction* — with exposure by class: ~2,249 uses against the 425 the four structural families cover. | P2 |
| B17 | Y119: 18-node sole sink from **×1.52**, continuous to ×3.20; 22-node none below ×20; the "eastern four" clause deleted as invented. | P2 |
| B18 | Y383 as one observation: threshold in (5.01, 10.04], consistent with 2×5 = 10, no-threshold excluded. Y099 as measured: `Φ_ord` 59.8/59.6 against 55.1/54.8. | P2 |
| B19 | §3.8/§1.6 connectivity 90.5% → **90.6%** (5,723 of 6,320); self-coherence 55.2/55.0 → **55.1/54.8**. | P3 |

## C. Provenance and instruments

| # | change | source |
|---|---|---|
| C1 | **105.30 instrumented, not withdrawn.** `apparatus6.py` reproduces 105.3 / 10,712.7 / 89 exactly; imported by `measure6.py`, not inlined; `EXPECT` stripped. §1.3 gains the frozen-table clause. | P4 Y196 |
| C2 | `final.py:245` → `TIE_COST`; `TOL = 3e-4` untouched as §3.13's knob; validated at **baseline** knobs against `drain.run_drain` on all 30 b-vectors. Acceptance: **`V107` moves `['genua']` → `{doab, genua}`.** V035 dropped — it reads 0 today. | P3/P4 |
| C3 | `final.py` writes `final.out`; `verify6.py` gains two `shows()` checks reading it. Guarded on **identity, not age** — the producer stamps the fingerprint of what it consumed. Missing cache is a hard failure. | P3 |
| C4 | §2.1's fingerprint claim and §2.8's Determinism row cite `fingerprint6.py`. `V037` described as six solves in one process, blind to between-process variation. | P3 |
| C5 | `props6.py` (renamed from `val5_pergood.py`) **gains the scheduler-permutation loop** before being cited — the figure lives nowhere in the tree today. §1.1 cites `measure6.py` for three figures and `props6.py` for the rest. | P1 Y250 |
| C6 | §1.1: Phase 0 **determines** pendant orientation from the sign; Phase 4 un-peels **and emits**. | P1/P2 |
| C7 | §1.1's key-collision measurement at its real scope: zero across **all 2,320 core nodes**, not merely free edges; Phase 1's argmin and top-k cut untied too. | P4 |
| C8 | §0's coverage sentence rewritten (P1's wording); "well under half" dropped as the proportion the next sentence declines to give. | P1 Y016/Y974 |
| C9 | `ρ` deleted from §1.1 and §2.3 — no implementation exists. `r` stays; `drain.py`'s "is NOT applied" docstring corrected. | P1 Y229 |
| C10 | `eps` becomes a **required keyword** on `build_sc` *and* `solve_all`. Every shipped caller already passes it. | P1 Y274 |
| C11 | Y973's count replaced by P1's **partition** — what moves versus what holds — which survives the next operator change. | P1 |
| C12 | Y978: `cost ∈ [1, 1 + TIE_EPS + TIE_EPS2]`, no percentage. Y309 ends at "nothing in the model reads that field". | P1 |
| C13 | `fixes-agreed.md` kept and header-marked frozen at v6.0; out of both harness defaults. Y012 cites it and all 63 v5 rows are present. | P1 |

## D. Harness defects — 10 rows, one class: a check that trusts rather than measures

| # | defect | fix |
|---|---|---|
| D1 | `mutate6.py` crashes on the spec path (`KeyError: 'band containing alpha=1.5'`) and its no-argument path scores 10/10 against a frozen document. | Derive `BANDKEY` from `M.A_PHI`; both harnesses **refuse an unnamed target**. |
| D2 | `mutate6.py` routes by **filename**; `verify6.py` routes by content. | Route by `SPEC_MARK`/`CHECKLIST_MARK`. |
| D3 | `shows()` **passes** when its consistency scan matches nothing — live today on `spec: sources`. | Fail a template that matches no scannable site. `WORD` gains `0: "Zero"`; scan and comparison both case-insensitive. Ships **before** A5. |
| D4 | §1.3's table check **skips silently** if its marker phrase is absent — and A5 rewrites that sentence. | Locate the table **structurally**; fail closed. |
| D5 | `absent()` tests that a *string* is gone; any rewording satisfies it. | Kept for the five phrases and three dead-operator figures; boundary-anchored value checks added for 12.23 and 9.40. |
| D6 | `coverage6.py` scores **any non-zero exit** as a catch — so a crashed harness reports 100%. | Score on `RESULT: N checks, M failed` with `M > 0`; credit by `OUT` key via a per-run temp sidecar. **Coverage becomes 4 of 7**, unscored 23 → 25. |
| D7 | `coverage6.py` reads `measure6.out` from disk while `verify6.py` recomputes in-process — they can silently disagree. | `coverage6.py` imports `measure6`; the file read goes. |
| D8 | A5's tax assertion as first drafted looped over an empty dict — zero iterations, zero checks. | Assert **behaviourally**: `r["tax"] == TAX_COEFF · base_tax(r)` for every counted province. |
| D9 | §2.8's tolerance row as drafted would halt on `paper` today, on correct behaviour. | Three branches: halt if min *positive* rc ≤ tolerance; report if rc = 0 and max-flow = 0; **halt** if rc = 0 and max-flow > 0. Floor: 2.498e-08 over 124 solves. |
| D10 | Nothing tests that the harness goes **red** when it must. | Negative-fixture suite in §2.9's build order: unscannable needle, removed locator, RESULT-less stub, cross-figure mutation. |

---

## What preconfirmation must check

Every figure above, independently. Three deserve particular attention:

- **B7's 7-of-159 and 13-of-29.** My own measurement gave 0-and-5 from two compounding defects —
  `N·w/sum` is algebraically `w/mean`, so the only normalisation that moves the aggregate was never
  tested, and the probe did not inherit `LP_OPTS`. Assert the normalisation vectors are **pairwise
  distinct** before trusting any diff.
- **C2's acceptance test.** `V035` reads 0 before *and* after the repair, because `final.py:169`
  calls `drain.phase2` (already carrying `TIE_COST`) outside the permutation loop. Only `V107`
  discriminates.
- **C1's 105.30.** Reproducible from twenty frozen constants in
  `../v5-owner-agnostic/scripts/solver.py:59-75`. No classification happens — W041 and X035 refuted
  the *rule*, never these values.

Instruments in `scripts/`: 22 `p3_*.py`, five `val5_*.py`, `apparatus6.py`. Each was validated
against the shipped code before use.
