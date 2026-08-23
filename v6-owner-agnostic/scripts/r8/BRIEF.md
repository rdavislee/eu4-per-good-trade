# Round-8 validation brief (read this first, in full)

You are grading claims made by a design specification against **primary sources**. Every claim gets
its own verdict, earned from the sources — never from the document's own restatement of them, and
never from plausibility. You are an adversarial validator: trust nothing you cannot verify
yourself.

## The document under test

`C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\per-good-trade-spec.md`
(2,165 lines, MD5 `88da3fe76244ab4f43ef41edf3e50768`). **Read the document lines for your sections
before grading anything.** Your slice file gives each claim's spec line number; several claim texts
in the slice are elided with `…` — the current document's wording at that line governs, not the
slice's paraphrase and not any prior inventory.

Section line map of the current document:
```
1   # Per-Good Trade Network - Design Spec    1485 ## 3.2 Why a flow and a drainage sweep
119 # 1. Mechanics                            1598 ## 3.3 Why wealth, and why per province
121 ## 1.1 Trade direction                    1629 ## 3.4 Why supply is pre-modifier
255 ## 1.2 Supply                             1641 ## 3.5 Why alpha is anchored absolutely
268 ## 1.3 Demand                             1692 ## 3.6 Why no hysteresis, and why no eps
466 ## 1.4 Market concentration               1742 ## 3.7 Why eligibility is per good
478 ## 1.5 Goods without a graph              1750 ## 3.8 Why gates evaluate true
530 ## 1.6 The aggregate graph                1770 ## 3.9 Why Phi_w is the installed graph
750 ## 1.7 Merchants                          1823 ## 3.10 Why the engine's economy is overwritten
778 ## 1.8 Collection and transfer            1842 ## 3.11 Why caravan power needs a condition
812 ## 1.9 Trade power propagation            1867 ## 3.12 Why treasure fleets are always granted
823 ## 1.10 Direction-dependent systems       1882 ## 3.13 Open questions
889 ## 1.11 Treasure fleets                   1972 ## 3.14 AI merchant assignment
897 ## 1.12 What the game displays            1991 ## 3.15 Rejected
921 # 2. Implementation                       2102 ## 3.16 Evidence standard
923 ## 2.1 Shape
988 ## 2.2 Solver
1035 ## 2.2a What map this is for
1077 ## 2.3 Constants
1236 ## 2.4 The tradenodes file
1320 ## 2.5 Runtime attachment
1326 ## 2.6 Writing to the engine
1348 ## 2.7 Probes
1413 ## 2.8 Validation
1457 ## 2.9 Build order
1473 # 3. Reasoning
1475 ## 3.1 Goals
```

## Primary sources

- The EU4 1.37.5 install: `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV`
  (`common/`, `events/`, `missions/`, `decisions/`, `history/`, `map/`, `localisation/`,
  `eu4_rev.txt`, shipped saves).
  Crash dumps: `C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\crashes\`
  and `C:\Users\rdavi\Documents\Paradox Interactive\Europa Universalis IV\crashes\`.
- `...\v6-owner-agnostic\scripts\` — the reference implementation (`solver.py`, `drain.py`,
  `flowop.py`) and its instruments. **A script named in a claim's provenance is where to start, not
  what to trust**: settle measured claims by *running* the computation, not by reading comments.
- Prior-version directories `..\v1-laplacian\` … `..\v5-owner-agnostic\` for claims about what
  earlier versions said or did.
- Readable saves: look under `C:\Users\rdavi\Documents\Paradox Interactive\Europa Universalis IV\save games\`
  and the install's own `save games` — the spec and scripts name the ones they use.

## FORBIDDEN sources

Do **not** open, quote, or be influenced by any prior verdict file:
`validation-round7.md`, `validation-v62*.md`, `validation-v6-round*.md`, `preconfirm-round*.md`,
`val62*` outputs and `scripts/r7/out/*` in `scripts/`. A claim graded in an earlier round is graded
again **from sources**; prior verdicts do not exist for your purposes. (`changes-v6.md`,
`fixes-agreed.md`, `fixes-round*.md`, `applied-round6.md`, `claims-delta-*.md`, `round8.diff` may be
read only when a claim is *about* them — e.g. a PROCESS claim citing a round-8 fix or a diff —
never as a verdict.)
**A wiki is not a source.** Neither is the open web.

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
- **A claim scoped to a named observation, or explicitly marked in the document as
  specification-not-measurement, is validated at that scope**: the question is whether the spec's
  statement of it is accurate (does the document really carry that scoping, does it quote the
  observation correctly), not whether the underlying unverifiable thing is true.
- **No confirmation on plausibility, consensus, or community documentation.** Unsettleable with the
  materials above = UNTESTABLE, and the row states exactly what would settle it.
- **Scope is yours.** Grade what the sentence asserts, including its qualifiers and its stated
  scope — not a friendlier reading.

## Verdicts

- **CONFIRMED** — reproduced or verified as scoped. Not "plausible", not "internally consistent".
- **PARTIAL** — part holds, part does not, or the claim outruns its evidence in scope or precision.
  State exactly which part fails.
- **REFUTED** — the sources contradict the claim as scoped. For a figure, report the value the
  sources give.
- **UNTESTABLE** — cannot be settled with these materials (a debugger session, a live game probe, a
  build that does not exist, an era save). State exactly what would settle it.

Every PARTIAL and REFUTED you return will be independently re-run by the lead validator, so make
the disagreement precise and reproducible: name the command, the file and the line.

## Already-run instrument outputs (fresh runs of the shipped scripts, this round)

In `scripts\r8\`: `measure6.out`, `props6.out`, `epsilon6.out`, `europe.out`, `round6.out`,
`final.out`, `p3_relabel_pergood.out`, `p3_time.out`, `verify6.out`, `redtest6.out`,
`relabel6.out`, `coverage6.out`, `mutate6.out`.
Read those before re-running anything. If you need a figure they do not carry, **copy the scripts
into your own working directory first**:
`mkdir -p scripts/r8/<SLICE>w && cp scripts/*.py scripts/*.json scripts/r8/<SLICE>w/ && cp per-good-trade-spec.md scripts/r8/<SLICE>w/`
and run there, so concurrent slices do not collide. Note `relabel6.py` resolves the v5 tree
relative to its own directory and only runs from `scripts\` itself.
Python 3.12, scipy 1.18.0, numpy 2.4.6 are installed. Use `python`.
Put every probe you write under `scripts\r8\`.

## Output

Write **one file**: `scripts\r8\out\<SLICE>.md`. No header, no prose — just markdown table rows,
one per claim, grouped by a `## §<section>` heading per section:

| ID | claim (short) | verdict | method | evidence |

- `claim (short)` = a ≤140-char precis of what you graded.
- `method` = one of: measurement (say what you ran), file read (say which file/line), derivation
  check, engine test, or arithmetic check.
- `evidence` = the figures, quoted file lines with line numbers, or the derivation step that
  settles it. For PARTIAL/REFUTED, the exact disagreement — what the document says vs what the
  source gives.
- Escape any literal `|` inside a cell as `\|`.
- **One row per ID in your slice, in slice order. No ID missing, none added.**

Then, in your final message back, report only: the counts (CONFIRMED / PARTIAL / REFUTED /
UNTESTABLE) and a one-line reason for every non-CONFIRMED row. Do not paste the table.
