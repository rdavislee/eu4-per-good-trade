# Per-Good Trade — an EU4 trade overhaul

**Every trade good gets its own trade network, and every arrow on the map is computed from the state
of the world instead of drawn by a designer.**

In vanilla, the trade map was decided once and never moves: Venice is rich because the arrows point
at Venice, and no amount of development turns a single one. Goods are cosmetic — grain, spices and
cloth all flow the same way to the same place.

Here trade is an outcome. Each good runs from where it is produced toward where the wealth wants it,
recomputed every month, so conquering a producer hands you a commodity to route home; developing
base tax pulls the world's goods toward your capital while base production makes a distant province
a source; and the world's centers of trade move when the wealth does. In a 200-year test campaign
they migrated from Genoa and Hangzhou to the English Channel, the Rhineland and Nippon — Britain
built the Channel into a market by developing both banks, while China lost the east by spending the
era at war. **Any nation can do it. There is no mission and no unique mechanic.**

### → [Install it](INSTALL.md)  ·  [What it changes, and why](ABOUT.md)

EU4 **1.37.5** (build `835bfdf8`), Windows/Steam, single-player. Drag-and-drop: one file into the
game folder, one folder into your mod folder.

---

*The rest of this file is for people working on the mod.*

Every good's network is computed monthly from the world state by the DRAIN operator; the engine's
own money is routed through those graphs and written back into the engine's own structures.

## The spec

**`per-good-trade-spec.md`** at this root is the release copy of the current specification —
**v6.6**, 2,283 lines, MD5 `48414cb316bd6b3c3355b1b87afdc3e2` — byte-identical to the canonical
file at `docs/v6-owner-agnostic/per-good-trade-spec.md`. The canonical copy is the one the harness
verifies and the one to edit; refresh this root copy from it on any change.

The spec is self-contained and implementable as-is: §1 mechanics, §2 implementation (§2.9 is the
build order), §3 reasoning and open questions. It survived eleven adversarial audit rounds; its
final graded state is **1,176 claims CONFIRMED, 0 REFUTED**
(`docs/audit/validation-round11.md`, with the full grading and its bookkeeping).

## Layout

| path | what it is |
|---|---|
| `per-good-trade-spec.md` | v6.6 release copy (read this) |
| `docs/v6-owner-agnostic/` | the canonical tree: spec, `changes-v6.md` (deleted text), `fixes-agreed.md` (v5→v6 ledger, frozen), and `scripts/` |
| `docs/v6-owner-agnostic/scripts/` | the reference implementation and harness (below), plus per-round validator probes in `r7/`–`r12/` |
| `docs/audit/` | the complete audit trail: validations, claim censuses, negotiated fix lists, frozen baselines and their byte-verified diffs (see `docs/README.md`) |
| `docs/v1-laplacian/` … `docs/v5-owner-agnostic/` | historical version trees, cited by the spec and the audit records; do not modify |
| `docs/v2-drain/drain-orientation.md` | the DRAIN operator's original write-up, cited by the spec by bare name |

## Verify before you build

```
cd docs/v6-owner-agnostic/scripts
python verify6.py ../per-good-trade-spec.md    # figures in the doc vs values computed from the install
```

Expected: `RESULT: 37 checks, 0 failed`. Requires the EU4 1.37.5 install at
`C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV` and the readable saves
(`VANILLA_start.eu4`, `Castile1444_12_22.eu4`) in the documents save-games directory; `numpy` and
`scipy` (HiGHS) in Python. Some figures also cite `measure6.py`, `round6.py`, `props6.py`,
`final.py` — all runnable the same way. `coverage6.py` measures what the harness does *not* guard;
re-run it rather than quoting it.

## Acceptance tests

**`TESTING.md`** is the live-game acceptance suite — what must be seen working in the running
game, from the `Φ_w` map mode and any-edge merchant assignment through per-good views and the
monthly income checks. The ★ tests are the bar for "it works".

## Implementation entry points

- **Build order**: spec §2.9 — defines parser first, then the save parser and `path`/`control`
  read, then the b-flow + sweep with their per-tick assertions (each paired with a negative
  fixture), and the survival table; the memory track is §2.7's fifteen open probes plus locating
  the live produced-quantity fields.
- **Reference implementation** (`scripts/`): `solver.py` (field build), `drain.py` (the DRAIN
  operator), `flowop.py` (LP + `LP_OPTS`, the pinned tolerances), `nodes.py` (tradenodes parse),
  `measure6.py` (the figure battery). The DLL must agree with it on **orientation exactly**
  (spec §2.8's cross-implementation check).
- **What the DLL adds**: live memory reads (per-node `trade_goods_size`, §1.8), the per-good
  routing and ÷12 engine writes (§2.6), the emitted `00_tradenodes.txt` (§2.4), the trade UI
  (§1.12), AI merchant scoring (§3.14), attachment via pattern scanning (§2.5, EU4dll precedent).
