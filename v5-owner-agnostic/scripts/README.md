# v5.0 measurement toolchain

Every measured figure in `../per-good-trade-spec.md` is produced by one of these, run against
`C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV` (EU4 1.37.5.0 Inca, **with
Leviathan installed** — §1.3's province 8 figure depends on it).

Run from this directory. `nodes.json`, `prov1444.json`, `coastal.json`, `europe_provinces.json` and
`lowlands.json` are extraction caches; delete them and re-run `nodes.py`, `provinces.py`,
`coastal.py` and `europe.py` to rebuild from the install.

| Script | Produces |
|---|---|
| `validate_v5.py` | **The 135 self-checks v5.0 was built against.** Start here — it re-derives every figure the spec quotes and asserts the presence/absence of every wording v5.0 changed. It is the author's own harness, so it is evidence of internal consistency and *not* an independent audit; that is what `../validation-v5.md` is for |
| `v5measure.py` | Every figure §1.1, §1.3, §1.6, §3.8 quote, on the corrected wealth field |
| `europe.py` | §1.6's institution demonstration (Europe ×1.02 … ×1.56, Lowlands ×1.20) and the three 1444 Europe→Asia routes |
| `wealthmodel.py` | §1.3's whole-install modifier sweep — great projects, permanent province modifiers, centers of trade, buildings, static modifiers |
| `final.py` | §3.13's calibration, §3.11's caravan cap, the supply/demand contrasts |
| `verify.py` | The cross-document checks |
| `w9.py` | §1.6's 22-European-node thresholds and the dev-stack series |
| `w10.py` | §3.5's price-event partition over all five trees, with the per-file count assertion |
| `audit_f4.py` | §3.10's income-factoring identity and the per-good-propagation error, over five nodes' real 1444 country tables read from the vanilla save |
| `toys.py` | §3.2's **T1, T2 and T3** counterexamples, each run through a faithful reimplementation of §1.1 |
| `audit_alpha.py` | §1.6's `α_Φ` band table (1.00…3.00 at 0.01) and the noise test on each band |
| `rankrep.py`, `drainrep.py`, `rankop.py`, `basin.py` | §3.15's RANK and BASIN figures, §2.8's barbell |
| `phiw3.py` | §3.15's gravity kernel, §1.6's rank readings |
| `graphchk.py` | §3.3's land counts, §3.2's hop counts, the connectivity premise |
| `leftovers.py` | §3.15's BASIN reach, the RANK cloves case |
| `audit_delta2.py` | §2.8's two agreement figures, §3.9's node-wealth ranks, what the save's `highest_power` field is not, and §3.5's boundary goods |
| `audit_bands2.py` | §1.6's α_Φ band edges refined to 0.001, and every band's behaviour under ±1% wealth noise at 8 seeds |
| `audit_delta.py` | The four figures the no-context claims extraction flagged: §2.8's razed-China row, the inland-node basis, the spices supply/demand contrast, the caravan cap on both bases |

## Not a script

`claims-v5-round1.md` is the first no-context claim extraction of v5.0, kept because it is the
evidence behind entries 58–63 of `../changes-v5.md`: it found six places where one passage had been
regenerated on the corrected wealth field and a second passage stating the same fact had not. It was
extracted against the pre-repair text and is superseded by `../claims-v5.md`.

## The two files that carry the model

`solver.py` is the reference wealth model. §1.3's local-modifier tables are at the top:

```python
LOCAL_TAX_MOD = {"gems": 0.15}          # by trade good
LOCAL_TV_MOD  = {"incense": 0.10}       # by trade good
MON_FLAT / MON_GPMOD / MON_TVMOD        # by province id — great projects
PERM_FLAT                               # by province id — add_permanent_province_modifier
```

Adding a modifier to §1.3's classification table is one edit here. The wealth expression is
`TAX_COEFF·base_tax·(1 + local tax mods) + (GP_COEFF·base_production + flat goods bonuses)·
(1 + goods-produced mods)·price·(1 + trade-value mods)`, with `GP_COEFF = 0.2`, `TAX_COEFF = 1.0`.

`drain.py` implements §1.1. Phase 3's fallback branch is `max(gated, key=lambda v: (NODEW[v], -v))`
in both sweeps; `NODEW` is node wealth, computed once from `solver.ROWS`. The branch is unreachable
unless `b ≡ 0` across a connected core, and it fires on **0 of 29** goods and on `Φ_w` at 1444.

## Reproducing the spec itself

v5.0 is v4.0 plus 68 asserted string replacements, logged in `edits5.json`:

```
for n in 01 02 03 04 05 06 07 08 09; do python q$n.py; done      # apply the 57 edits to a copy of v4.0
python stats5.py                                                                   # replay + diff stats
python gen_changes5.py                                                             # rebuild ../changes-v5.md
```

`patch_lib.py` aborts if an anchor is missing or matches more than once, so a stale edit cannot be
applied silently. `stats5.py` replays all 68 against the v4.0 file and asserts the result is
byte-identical to v5.0.
