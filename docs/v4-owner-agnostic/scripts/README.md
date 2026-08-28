# v4.0 measurement toolchain

Every measured figure in `../per-good-trade-spec.md` is produced by one of these, run against
`C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV` (EU4 1.37.5.0 Inca).

Run from this directory. `nodes.json`, `prov1444.json` and `coastal.json` are extraction caches;
delete them and re-run `nodes.py`, `provinces.py` and `coastal.py` to rebuild from the install.

| Script | Produces |
|---|---|
| `v4measure.py` | Every figure §1.1, §1.3, §1.6, §3.8 quote |
| `validate_v4.py` | The 140 assertions behind `../validation-v4.md` Parts A, C, D |
| `validate_v4b.py` | The 40 assertions over the spec's untouched figures |
| `final.py` | §3.13's calibration, §3.11's caravan cap, the supply/demand contrasts |
| `verify.py` | The 33 cross-document checks, including Genoa's ×1.726 co-sink threshold |
| `w9.py` | §1.6's 22-European-node thresholds and the dev-stack series |
| `w10.py` | §3.5's price-event partition over all five trees |
| `rankrep.py`, `drainrep.py`, `rankop.py`, `basin.py` | §3.15's RANK and BASIN figures, §2.8's barbell |
| `phiw3.py` | §3.15's gravity kernel, §1.6's rank readings |
| `graphchk.py` | §3.3's land counts, §3.2's hop counts, the connectivity premise |
| `toys.py` | §3.2's T1 and T2 counterexamples |
| `leftovers.py` | §3.15's BASIN reach, the RANK cloves case |

`solver.py` is the reference wealth model. Its §1.3 local-modifier maps are at the top of
`province_table` — `LOCAL_TAX_MOD` and `LOCAL_TV_MOD` — and adding a modifier there is the only
edit needed if §1.3's classification table gains a row.

`drain.py` implements §1.1. Phase 3's fallback branch is `max(gated, key=(NODEW[v], -v))` in both
sweeps; `NODEW` is node wealth, computed once from `solver.ROWS`.
