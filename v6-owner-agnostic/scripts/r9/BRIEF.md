# Round-9 validation brief (read this first, in full)

You are grading claims made by a design specification against **primary sources**. Every claim gets
its own verdict, earned from the sources — never from the document's own restatement of them, and
never from plausibility. You are an adversarial validator: trust nothing you cannot verify
yourself.

## The document under test

`C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\per-good-trade-spec.md`
(2,190 lines, MD5 `0989f4dc54d31514123eed24f0aae5c5`, version stamp v6.4).
**Read the document lines for your sections before grading anything.** Your slice file gives each
claim's spec line number; many claim texts in the slice are elided with `…` or compressed — the
current document's wording at that line governs, not the slice's paraphrase and not any prior
inventory. Where a slice row carries a `CHANGED:`/`REWORDED:` note, that note describes how the
sentence moved since v6.3; grade the **new** text as it now stands.

Section line map of the current document:

```
1    # Per-Good Trade Network — Design Spec   1491 # 3. Reasoning
127  # 1. Mechanics                           1493 ## 3.1 Goals
129  ## 1.1 Trade direction                   1503 ## 3.2 Why a flow and a drainage sweep
264  ## 1.2 Supply                            1616 ## 3.3 Why wealth, and why per province
277  ## 1.3 Demand                            1647 ## 3.4 Why supply is pre-modifier
475  ## 1.4 Market concentration              1659 ## 3.5 Why alpha is anchored absolutely
487  ## 1.5 Goods without a graph             1710 ## 3.6 Why no hysteresis, and why no eps
539  ## 1.6 The aggregate graph               1760 ## 3.7 Why eligibility is per good
760  ## 1.7 Merchants                         1768 ## 3.8 Why gates evaluate true
788  ## 1.8 Collection and transfer           1788 ## 3.9 Why Phi_w is the installed graph
822  ## 1.9 Trade power propagation           1841 ## 3.10 Why the engine's economy is overwritten
833  ## 1.10 Direction-dependent systems      1860 ## 3.11 Why caravan power needs a condition
899  ## 1.11 Treasure fleets                  1885 ## 3.12 Why treasure fleets are always granted
907  ## 1.12 What the game displays           1900 ## 3.13 Open questions
931  # 2. Implementation                      1990 ## 3.14 AI merchant assignment
933  ## 2.1 Shape                             2009 ## 3.15 Rejected
1000 ## 2.2 Solver                            2120 ## 3.16 Evidence standard
1051 ## 2.2a What map this is for
1093 ## 2.3 Constants
1252 ## 2.4 The tradenodes file
1336 ## 2.5 Runtime attachment
1342 ## 2.6 Writing to the engine
1364 ## 2.7 Probes
1431 ## 2.8 Validation
1475 ## 2.9 Build order
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
- Prior-version directories `..\v1-laplacian\` ... `..\v5-owner-agnostic\` for claims about what
  earlier versions said or did.
- Readable saves: `C:\Users\rdavi\Documents\Paradox Interactive\Europa Universalis IV\save games\`
  and the install's own `save games` — the spec and scripts name the ones they use. (Saves under
  the OneDrive documents tree are unreadable placeholders; do not conclude anything from failing to
  read those.)

## FORBIDDEN sources

Do **not** open, quote, or be influenced by any prior verdict file:
`validation-round8.md`, `validation-round7.md`, `validation-v62*.md`, `validation-v6-round*.md`,
`preconfirm-round*.md`, and the directories `scripts\r7\out\`, `scripts\r8\out\`. A claim graded in
an earlier round is graded again **from sources**; prior verdicts do not exist for your purposes.
(`changes-v6.md`, `fixes-agreed.md`, `fixes-round*.md`, `applied-round6.md`, `claims-delta-*.md`,
`round9.diff` and the frozen spec snapshots may be read only when a claim is *about* them — e.g. a
PROCESS claim citing a round-9 fix or a diff — never as a verdict.)
**A wiki is not a source.** Neither is the open web.

**One narrow exception.** Claims `Y1142`, `Y1185` and `Y1237` are claims *about* the round-7 audit
record `scripts\r7\out\S01.md` row Y214 — what that row says, how many items it samples. For those
three rows only, open that one row and grade the document's description of it. Do not read the rest
of that file, and do not treat any verdict in it as evidence for any other claim.

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
- **A claim scoped to a named observation, to a stated design intent, or explicitly marked in the
  document as specification-not-measurement, is validated at that scope**: the question is whether
  the spec's statement of it is accurate (does the document really carry that scoping, does it
  quote the observation correctly), not whether the underlying unverifiable thing is true.
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

In `scripts\r9\`: `measure6.out`, `props6.out`, `epsilon6.out`, `europe.out`, `round6.out`,
`final.out`, `verify6.out`, `redtest6.out`, `coverage6.out`, `fingerprint6.out`, `apparatus6.out`
(plus `.err` siblings). Read those before re-running anything.
If you need a figure they do not carry, **copy the scripts into your own working directory first**:

```
mkdir -p scripts/r9/<SLICE>w
cp scripts/*.py scripts/*.json scripts/r9/<SLICE>w/
cp per-good-trade-spec.md scripts/r9/<SLICE>w/
```

and run there, so concurrent slices do not collide. Note `relabel6.py` resolves the v5 tree
relative to its own directory and only runs from `scripts\` itself; several scripts `os.chdir` to
their own directory, which is why the copy matters.
Python 3.12.10, scipy 1.18.0, numpy 2.4.6 are installed. Use `python`.
Put every probe you write under `scripts\r9\`.

## Output

Write **one file**: `scripts\r9\out\<SLICE>.md`. No header, no prose — just markdown table rows,
one per claim, grouped by a `## §<section>` heading per section:

| ID | claim (short) | verdict | method | evidence |

- `claim (short)` = a precis of what you graded, 140 characters or less.
- `method` = one of: measurement (say what you ran), file read (say which file/line), derivation
  check, engine test, or arithmetic check.
- `evidence` = the figures, quoted file lines with line numbers, or the derivation step that
  settles it. For PARTIAL/REFUTED, the exact disagreement — what the document says vs what the
  source gives.
- Escape any literal `|` inside a cell as `\|`. Keep every row on ONE line.
- **One row per ID in your slice, in slice order. No ID missing, none added.**

Then, in your final message back, report only: the counts (CONFIRMED / PARTIAL / REFUTED /
UNTESTABLE) and a one-line reason for every non-CONFIRMED row. Do not paste the table.
