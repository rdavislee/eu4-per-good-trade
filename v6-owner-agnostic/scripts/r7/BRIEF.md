# Round-7 validation brief (read this first, in full)

You are grading claims made by a design specification against **primary sources**. Every claim gets
its own verdict, earned from the sources — never from the document's own restatement of them, and
never from plausibility.

## The document under test

`C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\per-good-trade-spec.md`
(2,127 lines, MD5 `4150af72da9ea1868b29fdd941bea604`). Read the document lines for your sections
before grading anything. **The current document's wording governs**, not the claim label you are
given and not any prior inventory text.

## Primary sources

- The EU4 1.37.5 install: `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV`
  (`common/`, `events/`, `missions/`, `decisions/`, `history/`, `map/`, `localisation/`).
  Crash dumps: that install's `crashes/` and `C:\Users\rdavi\Documents\Paradox Interactive\Europa Universalis IV\crashes\`.
- `...\v6-owner-agnostic\scripts\` — the reference implementation (`solver.py`, `drain.py`,
  `flowop.py`) and its instruments. **A script named in a claim's provenance is where to start, not
  what to trust**: settle measured claims by *running* the computation, not by reading comments.
- Prior-version directories `..\v1-laplacian\` … `..\v5-owner-agnostic\` for claims about what
  earlier versions said or did.

## FORBIDDEN sources

Do **not** open, quote, or be influenced by any prior verdict file in the v6 directory:
`validation-v62*.md`, `validation-v6-round*.md`, `preconfirm-round*.md`, `val62*` outputs in
`scripts/`. A claim graded in an earlier round is graded again **from sources**; prior verdicts do
not exist for your purposes. (`changes-v6.md`, `fixes-agreed.md`, `fixes-round*.md`,
`applied-round6.md` may be read only when a claim is *about* them — e.g. a PROCESS claim citing
`fixes-agreed.md` — never as a verdict.)
A wiki is not a source.

## Method — this defines the verdicts

- **Re-derive; never inherit.**
- **Read the file, not the document's quotation of it.** Where a claim cites a game file, open it
  and quote the line.
- **Re-run measurements.** Where a claim states a measured figure, produce the figure. Where the
  instrument disagrees with the document, the instrument's output is the evidence and the
  disagreement is the finding.
- **Attack derivations as arguments.** A derivation is graded by checking each step, not by
  re-measuring its conclusion. Say in Method which kind of check you did.
- **A universal is graded as a universal.** A claim asserted for any input but checked only on the
  1444 start is at most PARTIAL; a proof that holds on 1444 but fails on a constructible input is
  REFUTED.
- **No confirmation on plausibility, consensus, or community documentation.** Unsettleable with the
  materials above = UNTESTABLE, and the row states exactly what is missing.
- **Scope is yours.** Grade what the sentence asserts, including its qualifiers and its stated
  scope — not a friendlier reading.

## Verdicts

- **CONFIRMED** — the sources establish the claim as stated.
- **PARTIAL** — part holds, part does not, or the claim outruns its evidence in scope or precision.
  State which part fails.
- **REFUTED** — the sources contradict the claim. For a figure, report the value the sources give.
- **UNTESTABLE** — cannot be settled with these materials. State what would settle it.

## Already-run instrument outputs (use these; they are fresh runs of the shipped scripts)

In `scripts\r7\`: `m6.out` (measure6.py), `p6.out` (props6.py), `e6.out` (epsilon6.py),
`eu.out` (europe.py), `r6.out` (round6.py), `f.out` + `final.out` (final.py),
`prg.out` (p3_relabel_pergood.py), `rl.out` (relabel6.py), `v6.out` (verify6.py),
`rt.out` (redtest6.py), `c6.out` (coverage6.py), `mu.out` (mutate6.py).
Read them before re-running anything. If you need a figure they do not carry, **copy the scripts
into your own directory first** (`mkdir scripts\r7\wNN && cp scripts\*.py scripts\*.json scripts\r7\wNN\`)
and run there, so concurrent slices do not collide. Note some scripts resolve `../per-good-trade-spec.md`
relative to their own directory; a copy of the spec sits at `scripts\per-good-trade-spec.md` for that.
Python 3.12, scipy 1.18.0, numpy 2.4.6 are installed. Use `python`.

## Output

Write **one file**: `scripts\r7\out\<SLICE>.md`. No header, no prose — just markdown table rows,
one per claim, grouped by a `## §<section>` heading per section:

| ID | claim (short) | verdict | method | evidence |

- `method` = one of: measurement (say what you ran), file read (say which file), derivation check,
  observation cited by the claim, or the gap that makes it untestable.
- `evidence` = the concrete result — a number, a quote, a file path and line, a script output line —
  **sufficient for a reader to re-check without repeating your work**. Never "as stated in the doc".
- Escape any `|` inside cells as `\|`. Keep each row on one line.

Grade **every** claim in your slice. Do not skip. Do not editorialise.

## Report back

Verdict counts, and for each REFUTED and PARTIAL claim: the ID and a one-line reason with the
number or quote that drives it. Your parent will personally re-check every REFUTED and PARTIAL.
