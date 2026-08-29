# Mare Liberum

*"The free sea": an EU4 trade overhaul where every arrow on the map is computed from the
state of the world, not drawn by a designer.*

**For Europa Universalis IV 1.37.5 · Steam · Windows · single-player · no DLC required**

**TL;DR:** Vanilla's trade map is hardwired and everything drains to Europe, forever. Mare
Liberum recomputes the whole trade map every in-game month, one network per trade good, from
where things are made and where the wealth is, so trade can flow in any direction and the
world's trade capitals are earned, not scripted. The controls stay vanilla's, with one
decision fewer. Installing is two drops and a checkbox, and the checkbox is a true off
switch: with Mare Liberum disabled in the launcher the game runs plain vanilla, so the mod can
stay installed while you play anything else.

What if the trade map answered to the world?

In vanilla EU4 the arrows between trade nodes (the routes trade value travels on the map)
were drawn once, before release, and no action in the game moves one. Every route on the
planet eventually drains into the English Channel, Genoa or Venice, in 1444 and in 1821,
whoever owns the world. You can fight for a bigger share of the flow; you can never change
where the flow goes. And the moment goods enter that network they become one number: the game
still lists what's in the barrel, but grain, silk and spices all ride the same arrows to the
same three rooms in Europe.

**Mare Liberum computes the arrows instead.** Every trade good gets its own trade network
(29 of them at the 1444 start), each one re-derived every in-game month from where that good
is actually produced and where the world's wealth actually sits. The same strait can carry
cloth east and furs west at the same time. And the places everything ultimately drains toward
are an output of *your* campaign, not a line in a data file.

- **Conquer the source, not the arrows.** A province's pull on the world's goods comes from
  its development and its land, not its flag, so painting the map bigger doesn't bend the
  arrows toward you on its own. Conquest still buys trade power and share, as it always did;
  what's new is that it buys *supply*. Take the region that grows the spices and you hold the
  source of the spice network, and the map carries the good toward whoever wants it most.
  Make sure that's you.
- **Build the next Venice.** An *end* (a node with no outgoing arrows, where the world's
  trade stops) is computed from wealth, not chosen by a designer. In one two-century
  hands-off test the ends held at Genoa and Hangzhou; in another, by 1635 they were the
  English Channel, the Rhineland and Nippon. No mission, no special mechanic: the ends are
  yours to fight over.
- **Play both directions.** A merchant can work either end of a link, including pushing
  goods *against* the prevailing current, the way European cloth really did sail toward the
  colonies. The AI plays the reverse board too: Ming's first picks steer Hangzhou and Xi'an
  inland, toward Beijing.
- **Spend development like a trader.** Base tax is pure demand: it makes a place hungrier,
  and goods orient toward hunger. Base production is supply; it makes the province a source
  (and, since goods are worth money, adds some pull of its own). Two buttons, two different
  instruments.
- **Let war bend the map.** Vanilla already makes devastated land produce less; here it also
  stops *pulling*, and when a region stops pulling, arrows turn around. Stripping the
  Hangzhou node bare flipped 35 links in one tick and moved the East's terminus within
  months; devastating Champagne reversed the Channel's trade, and healing it reverted every
  flip, exactly.
- **Keep your instincts.** Vanilla nodes, vanilla goods and prices, vanilla merchant range.
  And your income is still booked by the engine itself. You never issue an order for a single
  good; every control stays node-wide. One choice is gone outright: collecting is your
  capital's job now, and merchants exist to steer. Collecting abroad was only ever vanilla's
  workaround for a one-way map that stranded value downstream of your home; with goods
  flowing in every direction, nothing is stranded. You steer it home instead.

### → [Install it](INSTALL.md): two drops and a checkbox. · [What it changes, and why](ABOUT.md) · [The story](WHY.md)

**Does it hold up?** A 201-year hands-off campaign (1444–1645) ran unattended at speed 5
without a crash, and every month of it each country's ledger trade income was checked against
what the mod computed. The worst disagreement in two centuries was about three hundredths of
a ducat. In separate control tests from the same start, world trade income ran a steady ~3%
above unmodded runs with no drift or compounding. The live-game test record, residuals
included, is [`TESTING.md`](TESTING.md).

| | |
|---|---|
| Game | EU4 **1.37.5**, Steam, Windows 64-bit. The mod verifies the game binary at startup and refuses any other build |
| Mode | Single-player, non-ironman (achievements off, as with any mod) |
| DLC | None required. *Wealth of Nations* is worth having: it lets you move your trade capital, which is now your only collection point |
| Other mods | Total conversions supported by design, in any load order; developed and debugged against Anbennar and Extended Timeline, also tested with Voltaire's Nightmare ([notes](INSTALL.md#other-mods-including-total-conversions)) |
| Distribution | [GitHub releases](https://github.com/rdavislee/eu4-per-good-trade/releases): half the mod is a native plug-in (`version.dll`) that Steam Workshop can't host. Nothing on disk is patched, the game's exe is never modified, the DLL makes no network connections, and the build is bit-reproducible so you can build it yourself and check the hash ([how](INSTALL.md#build-it-yourself)) |

---

*The rest of this file is for people working on the mod. The project's working name in the
spec, the code, the log and the DLL is **per-good trade** (`pgt`); Mare Liberum is the
player-facing title.*

## The spec

**`per-good-trade-spec.md`** at this root is the release copy of the specification (**v6.6**,
MD5 `48414cb316bd6b3c3355b1b87afdc3e2`), byte-identical to the canonical file at
`docs/v6-owner-agnostic/per-good-trade-spec.md`. The canonical copy is the one the harness
verifies and the one to edit; refresh this root copy from it on any change. §1 is mechanics,
§2 implementation, §3 reasoning. It survived eleven adversarial audit rounds
(`docs/audit/validation-round11.md` has the final grading).

## Layout

| path | what it is |
|---|---|
| `per-good-trade-spec.md` | v6.6 release copy (read this first) |
| `impl/` | the DLL and solver implementation; `impl/DEPARTURES.md` records where the build deliberately differs from the spec |
| `dist/` | the shippable mod folder (`pgt.mod` + `pgt/`) |
| `docs/v6-owner-agnostic/` | the canonical tree: spec, reference implementation and harness (`scripts/`) |
| `docs/audit/` | the complete audit trail (see `docs/README.md`) |
| `docs/v1-laplacian/` … `docs/v5-owner-agnostic/` | historical version trees, cited by the spec; do not modify |

## Verify and build

```
cd docs/v6-owner-agnostic/scripts
python verify6.py ../per-good-trade-spec.md    # figures in the spec vs values computed from the install
```

Expected: `RESULT: 37 checks, 0 failed` (requires the 1.37.5 install, the readable saves, and
`numpy` + `scipy`). The reference implementation is `solver.py`, `drain.py`, `flowop.py`,
`nodes.py`, `measure6.py`; the DLL must agree with it on orientation exactly (spec §2.8).
Building the DLL from source is covered in [`INSTALL.md`](INSTALL.md#build-it-yourself);
the build is bit-reproducible, so a release binary can be verified rather than trusted.
`TESTING.md` is the live-game acceptance suite; the ★ tests are the bar.
