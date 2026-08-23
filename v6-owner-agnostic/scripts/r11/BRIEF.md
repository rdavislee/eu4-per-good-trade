# Round-11 validation brief (delta-scoped, adversarial)

You are grading claims from a game-mod design spec against primary sources. Trust nothing you
cannot verify yourself.

## Materials (absolute paths)
- Spec under test: `C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\per-good-trade-spec.md` (2,270 lines, v6.5)
- Claim census (row text + line numbers + what changed): same dir, `claims-delta-round10.md`
- Prior validation (for context on what round 9 found): same dir, `validation-round9.md`
- Diff of this round's edits: same dir, `round10.diff`
- Instruments: same dir, `scripts\` (and `scripts\r7`, `r8`, `r9`, `r10` for prior probes)
- EU4 install: `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\`
- Saves: `C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\VANILLA_start.eu4`
  and the non-OneDrive save dir; also `Castile1444_12_22.eu4`
- Crash dumps: `C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\crashes\`
- Prior version trees: `..\v1-laplacian\`, `..\v2-drain\`, `..\v3-owner-agnostic\`, `..\v4-owner-agnostic\`, `..\v5-owner-agnostic\`

Put any probe scripts you write in `scripts\r11\` with a filename prefix given in your slice.

## Method
For each assigned claim ID:
1. Read the census row (grep the ID in `claims-delta-round10.md`) for the claim text, section, type,
   provenance and spec line number.
2. Read the spec at that line to see the claim in context, and confirm the census row faithfully
   states what the spec says.
3. Settle it against a PRIMARY source: open the named file and quote the line; re-run the named
   instrument and quote its output; re-derive the arithmetic. Do not accept a prior validation's
   word for anything — reproduce it.
4. Grade at the claim's stated scope. A claim scoped to a named observation, a stated design intent,
   or marked specification-not-measurement is validated at that scope: the question is whether the
   spec's statement is accurate, not whether the unbuilt thing works. For DESIGN/stipulated rows the
   test is (a) does the spec actually say this, and (b) is any factual component it rests on true.
   For rows citing another section (`provenance: §X`), check that §X actually says what is claimed.

## Verdicts
- CONFIRMED — reproduced or verified as scoped.
- PARTIAL — part holds, part fails, or the claim outruns its evidence. State the EXACT disagreement.
- REFUTED — the sources contradict it as scoped. State the EXACT disagreement.
- UNTESTABLE — unsettleable with these materials; say exactly what would settle it.

## Output
Return, as your final message, one line per claim in this pipe-delimited form:

`Yxxx | VERDICT | method | evidence`

- method: what you did (e.g. "file read `interface/mapicons.gui` L120-140", "ran `measure6.py`").
- evidence: the quoted line, the reproduced number, or the exact disagreement. Be specific and
  quote primary text. Keep each row to a few sentences.

Do not write a report file. Return the rows in your message.
