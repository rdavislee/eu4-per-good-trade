# Round-12 fixes — DRAFT, NEVER NEGOTIATED TO CLOSURE, NOTHING APPLIED

**Status (2026-08-22): the loop closed at v6.6 with these five PARTIALs accepted as non-gating
residuals; this file is the reopening ledger, not an agreed list.** The round-11 validator was
stood down mid-review and issued no verdicts, but had already measured two rows and reported both
would have come back for revision — apply nothing here without re-negotiating:

- **A1**: the round-5 artifact is `validation-v6-round5-part2.md` L195/L199 (session record
  `../v2-drain/game-session.md` L170), reproduced by `scripts/r12/gate.py`.
- **A2 as drafted is wrong**: "cells sharing an owner sit at one ratio regardless of autonomy" is
  false for 13 of the 37 owners with ≥2 singleton cells (MNG {0.7, 1.0}, ARA {1.0, 1.097}, TIM
  four distinct ratios), and holds for only 3 of 7 owners whose cells span ≥20 autonomy points.
  The defensible forms: the GEO instance itself (four cells at ≈1.133 across 0%–52%, exact) and
  the owner-demeaned within-owner correlation **r = −0.030** (`scripts/r12/a2check.py`). Barcelona
  exact, 3-of-7 and ~60% all confirm.
- **A3 as drafted has a side effect**: "no note after 1.8" silently widens Y1372 (confirmed only
  at "no note later than 1.16") and re-asserts retired Y1353's 1.12 proposition by entailment.
  Keep the premise at Y1372's confirmed scope (no note after 1.16).


Answering `validation-round11.md`: **1,176 CONFIRMED · 5 PARTIAL · 0 REFUTED · 8 UNTESTABLE** over
1,189 live rows (27/5/0/0 on the 32 freshly graded). The spec is frozen at
`48414cb316bd6b3c3355b1b87afdc3e2` (2,283 lines) until this list is negotiated to unconditional
confirmation and separately preconfirmed. The 8 UNTESTABLE rows carry unchanged — the loop's
floor. **R1 is untouched by every row.** Three rows cover the five PARTIALs; the substantive one
(A1) integrates a recorded measurement the last two rounds' text wrongly denied existed.

| # | ID | fix |
|---|---|---|
| A1 | Y375, Y1158, Y1326 | The both-ends rule's evidence is upgraded from "none recorded" to what the tree actually holds, at **all three sites** (§1.8's rule sentence, §1.8's parenthetical, §2.7 item 19). The round-5 session's own artifact measured it per link on `Castile1444_12_22.eu4`, and your `scripts/r12/gate.py` reproduces it: of 159 links, **33 of 50 zero-value links have no both-ends holder against 3 of 109 value-carrying links** (χ² = 78.3) — a strong statistical association — while **three links carry value between disjoint power-holder sets** (`cuiaba→brazil`, `rio_grande→mississippi_river`, `california→mississippi_river`), so the rule's **absolute form is false** on the save's own evidence. The rewritten claim: value overwhelmingly fails to arrive where nobody holds power at both ends — the measured association above — but it is a **tendency the save supports, not a gate the save proves**: three exception links carry value between disjoint holder sets, the mechanism behind both the tendency and the exceptions is unprobed, and §2.7 item 19 stays open to settle it (its text updated to name the measurement and the exceptions as what the probe must explain). "No session has observed it" and "no recorded session supports it" both go — they were false against the tree's own round-5 record. Name the round-5 artifact's path in your confirmation so the applied text cites it alongside `scripts/r12/gate.py`. |
| A2 | Y1366 | §3.4's direct autonomy check restated to the evidence that actually carries it: Barcelona (pid 213, 91% autonomy) reproduces exactly, but across the seven singleton cells at ≥50% autonomy only three reproduce — high-autonomy cells reproduce *less* often (3 of 7) than zero-autonomy cells (about 60%), so per-cell reproduction rate is not the autonomy evidence. The **owner-grouped control is**: cells sharing an owner sit at one ratio regardless of autonomy — GEO's four cells all at ≈1.133 whether autonomy is 0% or 52% — so the engine/model ratio tracks **owner goods-produced modifiers, not autonomy**, which is the exclusion the sentence exists to establish. The r ≈ −0.1 correlation stays as the population-level statement; the "autonomy-heavy provinces reproducing the autonomy-free prediction exactly" clause is cut to the one province it is true of (Barcelona) and the owner-grouped control is stated as the evidence. |
| A3 | Y1371 | §3.16's supersession clause quote-aligns with its source: `1.16 Patchnotes.txt` L42's own words are that territories "have autonomy **and is considered to be overseas for many rules**" — so "whose territories carry autonomy in place of the overseas rule" overstates; territories remain overseas for many rules. The corrected clause: territories carry autonomy while remaining overseas for many rules (the line's own wording), and the supersession inference rests on the **floor appearing in no note after 1.8**, not on territories ceasing to be overseas. |

## What negotiation must settle

- Every row: CONFIRMED or REJECTED, no conditions; anything conditional comes back.
- A1 needs the round-5 artifact's path (the recorded session file your grading cited) so the
  applied text cites the record and your reproduction both.
- A1's rewritten claim states a measured association plus named exceptions plus an open mechanism
  probe — confirm that form grades CONFIRMED at its stated scope, or prescribe the form you will
  confirm.
- A2 keeps Barcelona and r ≈ −0.1 and adds the owner-grouped control as the carrying evidence —
  confirm the GEO figures and the 3-of-7 / ~60% split against your own probe.
