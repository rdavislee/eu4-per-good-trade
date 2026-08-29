# Installing Mare Liberum

**TL;DR:** Get the release, drop `version.dll` next to `eu4.exe`, drop the `pgt` mod into
your mod folder, enable Mare Liberum in the launcher. EU4 **1.37.5** on Windows/Steam exactly
(the mod checks the binary and refuses anything else), single-player. Your antivirus may
complain about the DLL; you can verify it instead of trusting it by building it yourself.
Uninstalling is deleting one file.

Download the latest release from
**[github.com/rdavislee/eu4-per-good-trade/releases](https://github.com/rdavislee/eu4-per-good-trade/releases)**:
it contains `version.dll` (the mod itself) and the small `pgt` mod folder. Then it's two
drops and a checkbox:

1. Copy **`version.dll`** into your EU4 game folder, next to `eu4.exe`.
2. Copy **`pgt.mod`** and the **`pgt`** folder into your EU4 mod folder. *(Working from a
   clone of this repo instead of a release? They're under `dist/`, and `version.dll` is
   `impl/dll/per-good-trade.dll` renamed, or build it yourself, below.)*
3. Enable **Mare Liberum** in the launcher and play.

**The launcher checkbox is the whole on/off switch.** The mod runs only when Mare Liberum is
enabled in the launcher; with it disabled (or not in your playset), the DLL notices and stays
completely dormant, and the game runs plain vanilla. So the mod can sit installed while you
play other things, vanilla or other mods, with zero effect. Turning it on is enabling the mod,
nothing else.

*Your antivirus may flag `version.dll`. That's expected for this kind of mod, not a sign of
tampering; see [Antivirus](#troubleshooting) below, including how to verify the file instead
of trusting it.*

No injector, no separate launcher, no configuration files. Steam's launch options are
untouched: the DLL loads with the game however you start it, checks whether Mare Liberum is in
your enabled mod list (the same `dlc_load.json` the game itself reads), and either runs the
mod or goes dormant for that launch.

| | |
|---|---|
| game folder | `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV` |
| mod folder | `%USERPROFILE%\Documents\Paradox Interactive\Europa Universalis IV\mod` |

## Requirements

| | |
|---|---|
| Game | Europa Universalis IV **1.37.5**, Steam, Windows (64-bit) |
| Build check | the mod verifies `eu4.exe` itself at startup (full SHA-256, pinned to release 1.37.5) and refuses to run on any other build |
| Mode | **Single-player**, non-ironman. The mod doesn't detect ironman or multiplayer: nothing stops you, but see Multiplayer below |
| DLC | none required. ***Wealth of Nations* recommended**. It lets you move your trade capital, which is your only collection point under this mod |

**The version lock is real and it is deliberate.** The mod finds the engine's trade
structures at addresses discovered by disassembling this exact executable. A patch moves all
of them, so the mod checks the binary when it attaches and, on any other build, logs the
refusal and does nothing at all: writing to those addresses in a patched binary would
corrupt your game, and refusing is the only safe response. If Steam has updated you past
1.37.5: right-click EU4 in your library → **Properties → Betas** → select **1.37.5** and let
Steam re-download.

## Other mods, including total conversions

The mod reads trade nodes, goods, prices and modifiers the way the engine does (through your
enabled mod list, later mods winning, `replace_path` honoured), so it adapts to whatever map
is actually loaded rather than assuming vanilla's. It was developed and debugged against
**Anbennar** (129 trade nodes, 255 links; it adapts and runs) and **Extended Timeline**, and
also tested with **Voltaire's Nightmare**.

Two things to know:

- Mare Liberum ships two data files of its own: a re-declared `common/tradenodes/` file and a
  small `interface/countrytradeview.gui` tweak. The trade-node file is inherently a
  vanilla-map file, and EU4 resolves file conflicts by its own fixed rule while **ignoring the
  launcher's load order entirely** (measured; reordering the playset changes nothing). So the
  mod does not fight: at every launch the DLL checks the enabled mod list, and if any other
  mod ships trade-node files it copies that content over its own before the game reads
  anything, restoring its own map when no such mod is enabled. Load order does not matter.
  The one remaining fight is another mod that edits the trade UI file itself: unsupported.
- A mod that sits in your mod folder as a `.zip` is skipped (the log names it). Workshop
  mods arrive unpacked; if one of yours is still zipped, unzip it in place.

## Check that it worked

In game, open the trade map mode: the arrows will differ from vanilla's. Click a province
and the whole trade UI switches to that province's good, with its own network. That is the
mod working.

If you want certainty, the mod writes `per-good-trade.log` in the game folder. You don't need
to read it all. If the first line and the `build gate PASS` line are present, it's running:

```
version.dll proxy: 17/17 exports resolved from C:\Users\<you>\AppData\Local\Temp\pgt_version_orig.dll
build gate PASS: verified build 835bfdf8... (release_1.37.5): offsets valid
DIRECTION GATES OPEN (spec 1.10): 5/6 rebuild call sites hooked [MISSED 0x775EEC...]
[tick] monthly update 1: wrote 80 nodes inside the engine's value pass (pre-division), ...
```

`5/6` is correct, not an error: the sixth site is claimed by another part of the mod that
installs first. The log says so plainly rather than quietly rounding up.

## Optional: launcher tile art

Purely cosmetic, skip freely. The launcher will show Mare Liberum with a blank tile. That is
a launcher limitation, not a broken install: the launcher only shows tile art it downloaded
from Steam Workshop, and never reads a picture from a locally installed mod's folder (the mod
ships `thumbnail.png` and declares it in `pgt.mod`; the launcher ignores both).

`set-launcher-thumbnail.ps1`, next to `pgt.mod` in the release, fixes the tile by doing for
this mod exactly what the launcher does for a Workshop mod, and nothing else: it copies
`mod\pgt\thumbnail.png` into the launcher's image cache (as
`.launcher-cache\local-mod-thumbnail-pgt\thumbnail.png`) and fills in one column
(`thumbnailPath`) of the launcher's mod database (`launcher-v2.sqlite`), on Mare Liberum's row
only. It uses Windows' own SQLite (`winsqlite3.dll`), so nothing is installed and no network
is touched; the script is short and readable if you'd rather check than trust.

With the mod installed, the launcher run at least once since (so the mod is in its database),
and the launcher **closed**:

```powershell
powershell -ExecutionPolicy Bypass -File .\set-launcher-thumbnail.ps1
```

Run it from the folder holding the script (in a repo clone: `dist\`). Safe to re-run; if the
launcher ever rebuilds its database and the tile goes blank, run it again. To undo, delete the
`local-mod-thumbnail-pgt` folder from `.launcher-cache`: the tile returns to blank and nothing
else changes.

## What the mod writes (and doesn't)

Worth knowing before your file monitor tells you:

- **`per-good-trade.log`** (and `pgt_crash.log` if something goes wrong) in the game folder.
- **Its own `mod\pgt\common\tradenodes\00_tradenodes.txt`**, rewritten at launch when your
  enabled mods change what the trade map should be (see *Other mods* above): it becomes a copy
  of the enabled conversion's trade-node files, or of the shipped `phiw.baseline` beside it
  when no such mod is enabled. Only inside the mod's own folder, and only when the bytes
  differ; the log line starts with `[nodesync]`.
- **A small sidecar next to each save**: `<savename>.eu4.pgt`, plain text. It holds your
  merchant assignments, because the engine's save format can't express a merchant on a
  reverse link end. Deleting one costs you nothing but those placements.
- **A private copy of Windows' real `version.dll`** at `%TEMP%\pgt_version_orig.dll`,
  refreshed each launch, loaded by absolute path; that's how the proxy forwards the game's
  version-API calls. Safe to delete any time.
- At startup the DLL also looks for a developer test save (`VANILLA_start.eu4`) for a
  self-test; if it isn't there, it logs that and moves on. (If you run `strings` on the DLL
  you will find that save's path from the development machine embedded; the lookup is
  read-only and skips silently on yours.)
- **No network activity, ever.** The DLL opens no sockets and makes no HTTP calls. The
  source is in `impl/`; grep it for `WinHttp`, `InternetOpen` or `WSAStartup` and find
  nothing.

## Uninstall

Disabling the mod in the launcher is already a complete off switch: the DLL stays dormant and
the game runs plain vanilla. To remove it, delete `version.dll` from the game folder and
disable the mod in the launcher. Nothing is
patched on disk and the executable is never modified. Saves made with the mod are expected to
load fine without it; trade reverts to vanilla's rules (merchants you'd placed on reverse
ends come back steering vanilla's first outgoing link).

For a spotless removal, also delete the leftovers, all inert: `per-good-trade.log` and any
`pgt.*` marker files in the game folder, `%TEMP%\pgt_version_orig.dll`, the `.eu4.pgt`
sidecars beside your saves, the `pgt` folder + `pgt.mod` in your mod directory, and, if you
ran the optional tile-art script, `.launcher-cache\local-mod-thumbnail-pgt` next to the mod
directory.

## Why a file called `version.dll`

EU4 imports Windows' `version.dll` at startup, and Windows looks in the game folder before
the system folder. Naming the mod `version.dll` means the game loads it on its own. That is
the entire trick, and it is why there is nothing to run or inject.

The mod still has to *provide* the seventeen functions a real `version.dll` exports (the game
itself imports three of them). It does that at runtime, forwarding every call to the private
`%TEMP%` copy of the genuine system DLL described above.

*(If you used an earlier build, it required you to hand-copy the system DLL into the game
folder as `pgt_version_orig.dll`. The shipped mod no longer needs that; delete it. The
developer install script `install-proxy.ps1` still sets up the legacy pair; that's fine on a
dev machine.)*

## Troubleshooting

**The game never opens: no window, no loading screen.** The `version.dll` you installed is
not this mod, or it is a 32-bit or corrupted copy. Replace it; the log's first line reports
`17/17 exports resolved` when the file is good.

**Trade looks exactly like vanilla.** In likeliest order: the mod isn't enabled in the
launcher (the log ends with `DORMANT` and says so: that is the off switch working, not a
fault); `version.dll` isn't in the game folder or wasn't loaded (then there is no
`per-good-trade.log` at all); or the build check refused a patched executable (the log says
so).

**It stopped working after a Steam update.** The build check is refusing a patched
executable. Roll back to 1.37.5 through Steam's beta branches (steps under Requirements).

**The game crashes.** The mod writes `pgt_crash.log` in the game folder saying where. The
fastest diagnosis is bisection: the `pgt.NO*` switches under *For developers* turn the mod's
pieces off one at a time. Report it, with both logs, at the
[GitHub issues page](https://github.com/rdavislee/eu4-per-good-trade/issues).

**Antivirus quarantines the file.** Expected, and worth taking seriously as a category: this
is a DLL that loads into another process and patches its code, which is precisely what the
heuristic looks for. It does nothing else: no network, no reads outside the game and its own
files (see *What the mod writes*). The ordinary fix is to restore the file and exclude your
EU4 folder. If you'd rather not take a stranger's binary on trust (a fair instinct), don't:
the build is **bit-reproducible**, so you can build it from source and check that your hash
matches the release exactly (next section).

**Multiplayer.** Not supported, not tested. Trade is computed on each machine, and the
verification that two clients stay in lockstep has never been done. Expect desyncs.

## Build it yourself

The build is **bit-reproducible**: the same source and toolchain produce a byte-identical
DLL, so you can verify a release binary instead of trusting it. The release hashes:

| file | SHA-256 |
|---|---|
| `version.dll` (this release) | `ce1e948ab357b7e8a69e2f37ca3160dbaa9286857a9f6ae86f316c0883ed7716` |
| `eu4.exe` 1.37.5 (what the gate pins) | `9ad3efe1af169f40ee577f9dae5debbc87af6fb8b5450fb345ebf110dc4d771a` |

Hash what you installed, then build your own and compare:

```powershell
Get-FileHash "C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\version.dll" -Algorithm SHA256

winget install MartinStorsjo.LLVM-MinGW.UCRT     # toolchain, once
cd impl\dll
.\build-dll.ps1                                  # builds to %TEMP%\per-good-trade-build
Get-FileHash "$env:TEMP\per-good-trade-build\per-good-trade.dll" -Algorithm SHA256
```

Equal hashes mean the binary is exactly this source. To install your own build, rename
`per-good-trade.dll` to `version.dll` and drop it in the game folder. (Hash the installed
file *before* building: the script also copies its output over `impl\dll\per-good-trade.dll`.)

One caveat: byte-identity holds per toolchain. The release was built with
**llvm-mingw-20260421-ucrt-x86_64** (clang 22.1.4); any llvm-mingw UCRT x86_64 build should
produce a *working* DLL, but only that exact toolchain reproduces the release hash.
(Reproducibility itself comes from `-Wl,--no-insert-timestamp`: the PE timestamps were the
only bytes that ever differed between builds, four of them, measured.)

## For developers

`impl/dll/install-proxy.ps1` installs a chosen build and can copy marker files:

```powershell
.\install-proxy.ps1 -Dll <path>\pgt_iNN.dll     # install
.\install-proxy.ps1 -Uninstall                  # remove
```

The solver-side acceptance suite, which needs no running game, is `impl\accept.ps1`. One known
red if you run it: the economy fixture block reports 13 of 24 checks failed. That red is
present in the approved release source (recorded in commit `6e519df`) and is under
investigation as a stale-fixture issue; the live-game record in `TESTING.md`, which reconciles
the model against the engine's own ledger monthly for two centuries, is the acceptance
evidence for the shipped behavior.

Features default on; an empty marker file in the game folder (next to the DLL) turns one off.
Feature switches: `pgt.NOAI`, `pgt.NOARROWS`, `pgt.NOTICKHOOK`, `pgt.NOINSTALL`,
`pgt.NORELINK`, `pgt.NOREVPANEL`, `pgt.NOCLICKGATE`, `pgt.NOCARAVAN`, `pgt.NOLIVEFIELD`.
Finer-grained markers: `pgt.NOGATES`, `pgt.NOSHIPS` (vanilla light-ship placement),
`pgt.NOWRITE` (solve but write nothing: the control-run switch), `pgt.NOCOLOR`,
`pgt.NOOUTTIP`, `pgt.NOBUTTONS`, `pgt.NOTRANSFERTEXT`, `pgt.NOGATEFILL`, `pgt.NOFIRSTTICK`,
`pgt.NOREACHC`, `pgt.NOSHARE`. Two are opt-*in*: `pgt.TREASURE` (the unfinished §1.11 fleet
router: it has crashed on a late-game save; leave it off) and `pgt.FORCEDLL` (arm the DLL even
when Mare Liberum is not in the enabled mod list, for probe sessions that run without the data
mod). Bisecting by disabling one hook
at a time is how most of this mod's hard bugs were found.

---

*← [Overview](README.md) · [What it changes, and why](ABOUT.md)*
