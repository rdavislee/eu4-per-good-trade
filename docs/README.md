# Audit trail

Everything in `audit/` is a **record** — nothing here is live, and nothing in the spec or the
harness reads these files (the three `*_round11.py` census tools in
`../v6-owner-agnostic/scripts/` point here explicitly). The v6 loop's method per round: negotiate
a fix list with the round's validator to unconditional confirmation, independently preconfirm the
same text, apply with write-time re-measurement, byte-verify the diff against a frozen baseline,
re-run the harness, reread the whole spec, audit the implementation, re-census the claims, and
validate the delta.

## The current record

- `validation-round11.md` — the **final graded state** of spec v6.6: 1,176 CONFIRMED, 0 REFUTED,
  5 accepted PARTIALs, 8 UNTESTABLE, over 1,189 live claims.
- `claims-delta-round11.md` — the current claim census (IDs to Y1372).
- `fixes-round12.md` — drafted, **never negotiated to closure, never applied**: the annotated
  repair plan for the five residual PARTIALs, with the round-11 validator's parting corrections
  inline. Re-negotiate before applying anything from it.

## Round-by-round

| round | validation | census | fix list | baseline → diff |
|---|---|---|---|---|
| v6.2 era | `validation-v62*.md` (8 parts) | `claims-delta-v62.md` | `fixes-round2..6*.md`, `preconfirm-round2..6.md`, `applied-round6.md` | `per-good-trade-spec-v6.1-frozen.md` → `round6.diff` |
| 7 | `validation-round7.md` | `claims-delta-round7.md` | `fixes-round7.md` | `…v6.2-prevalidation-frozen.md` → `round7.diff` |
| 8 | `validation-round8.md` | `claims-delta-round8.md` | `fixes-round8.md` | `…v6.2-round8-frozen.md` → `round8.diff` |
| 9 | `validation-round9.md` | `claims-delta-round9.md` | `fixes-round9.md` | `…v6.3-round9-frozen.md` → `round9.diff` |
| 10 | `validation-round10.md` | `claims-delta-round10.md` | `fixes-round10.md` | `…v6.4-round10-frozen.md` → `round10.diff` |
| 11 | `validation-round11.md` | `claims-delta-round11.md` | `fixes-round11.md` | `…v6.5-round11-frozen.md` → `round11.diff` |

Each `roundN.diff` was verified at apply time to reconstruct the then-current spec byte-exactly
from its frozen baseline — that chain is what licenses the delta-scoped validations' carrying of
unchanged verdicts. `validation-v6-round5-part*.md` and `claims-v6.md` are the earlier v6-loop
records several later rounds cite (round 11's both-ends measurement lives in
`validation-v6-round5-part2.md`). Validator working files and probes sit next to the instruments
in `../v6-owner-agnostic/scripts/r7/`–`r12/`.

Trajectory across the loop: 14 REFUTED + 83 PARTIAL → 0+41 → 0+26 → 1+18 → 0+14 → 0+8 → 0+5.
