# CLAUDE.md — implementation phase

EU4 per-good trade overhaul. The design phase is **done**; you are implementing a finished,
audited specification. Read `README.md` first, then the spec.

## Authority order

1. **`per-good-trade-spec.md` (v6.6) is the authority.** It survived eleven adversarial audit
   rounds; every figure in it is instrument-backed. Implement what it says. If it seems wrong,
   check `docs/audit/` before concluding that — most "bugs" you will suspect were already
   litigated there.
2. **The reference implementation** (`v6-owner-agnostic/scripts/`: `solver.py`, `drain.py`,
   `flowop.py`, `nodes.py`, `measure6.py`) is correct **by definition** where your code disagrees
   with it on orientation (spec §2.8). Diff against it early and often.
3. Everything else — audit records, probe outputs, historical `v1`–`v5` trees — is read-only
   context. **Do not edit the spec, `docs/audit/**`, or the historical trees** without explicit
   user direction.

## Hard rules

- **Byte fidelity is load-bearing.** `.gitattributes` pins no EOL conversion; the spec, frozen
  baselines and `round*.diff` files are MD5-pinned and the diff chain reconstructs byte-exactly.
  Never let a tool rewrite line endings in those files.
- If the spec must change: keep `python scripts/verify6.py ../per-good-trade-spec.md` (run from
  `v6-owner-agnostic/scripts/`) at **0 failed**, and refresh the root `per-good-trade-spec.md` as
  a byte-identical copy (update the MD5 quoted in `README.md`).
- **Target build only**: EU4 1.37.5, binary `835bfdf8`. The DLL must verify the build hash at
  attach and refuse others (§2.5). Any patch invalidates every found offset.
- **Single-player only.** Do not attempt multiplayer; §2.1's build-discipline checks gate it.
- New implementation code goes in a **new top-level directory** (e.g. `impl/`), not inside
  `v6-owner-agnostic/`.

## Environment

- EU4 install: `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV`
- Readable saves: `VANILLA_start.eu4`, `Castile1444_12_22.eu4` under
  `~\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\`
- Crash dumps from prior probing: `…\Europa Universalis IV\crashes\`
- Python with `numpy` + `scipy` (HiGHS) runs the reference and harness.

## What to build, in what order

Spec **§2.9** is the build order — two tracks in parallel:

- **Solver track**: defines parser → save parser + `path`/`control` → b-flow + sweep with per-tick
  assertions, *each paired with a negative fixture that makes it fail* (`scripts/redtest6.py` is
  the reference-side model of this) → eligibility, realized flows, census, survival table.
- **Memory track**: the §2.7 debugger session (fifteen open probes) + locating the live fields
  the §1.8 injection read needs. **This track is the schedule risk** — the trade structures,
  tick hook, UI data sources and per-node `trade_goods_size` in live memory are all undiscovered;
  the EU4dll precedent provides attach scaffolding only.

Solver constraints that are correctness, not tuning (§2.2/§2.3): simplex-family LP only (network
simplex ideal; never interior-point without crossover), optimality tolerances pinned tighter than
the 3.8e-8 worst-case margin, single-threaded, no runtime CPU dispatch. Test cross-implementation
orientation equality against the reference's dumps **before** any engine attachment — it needs no
game.

## Acceptance

`TESTING.md` is the live-game suite; the ★ tests are the bar. Fold the open §2.7 probes into
those sessions (TESTING.md §I maps which probe each session settles) and record results by probe
number.

## Known non-bugs — do not chase

- The 5 residual PARTIALs and 8 UNTESTABLEs in `docs/audit/validation-round11.md` are accepted
  documentation residuals; `docs/audit/fixes-round12.md` is their un-applied, annotated ledger.
- The save-based reference reconstruction runs **3.4% low** vs the engine's `local_value`,
  concentrated in New World nodes — a recorded reference-side limit (§2.8). The DLL's live read
  is the comparison basis, not the reconstruction.
- The reference deliberately does not build the survival table and reads three defines by regex —
  recorded gaps owned by §2.9, not defects.

## Decisions reserved for the user

- AI merchant **reassignment cadence** (§3.14): mirror vanilla's vs compute it. Ask when you
  reach AI work; do not decide unilaterally. **The user's stated prior**: the choice is
  low-stakes, because merchant choices are stable under the moving map — assignments are to link
  ends and survive flips with only the active good set changing (§1.7), homeward direction from a
  node is geography, and the flip-prone links carry near-zero value (§3.6) — so a conservative
  rule (computed-gain test plus a dwell floor of a few months) is expected to fire rarely and is
  the working default to propose.
- Any change to hyperparameters (`α_Φ`, `TIE_EPS`, `TIE_EPS2`) or to R1 (the §1.3 wealth rule).
