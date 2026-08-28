# Installing Per-Good Trade

Two drops and a checkbox:

1. Copy **`version.dll`** into your EU4 game folder, next to `eu4.exe`.
2. Copy **`pgt.mod`** and the **`pgt`** folder into your EU4 mod folder.
3. Enable **Per-Good Trade** in the launcher and play.

That is the whole installation. No injector, no separate launcher, no script, no configuration
files. Steam's launch options are untouched — the mod loads with the game however you start it.

| | |
|---|---|
| game folder | `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV` |
| mod folder | `%USERPROFILE%\Documents\Paradox Interactive\Europa Universalis IV\mod` |

## Requirements

| | |
|---|---|
| Game | Europa Universalis IV **1.37.5**, Steam, Windows (64-bit) |
| Build hash | **`835bfdf8`** — verified at startup |
| Mode | **Single-player only** |
| DLC | none required; works with or without |

**The version lock is real and it is deliberate.** The mod finds the engine's trade structures at
fixed addresses found by disassembling this exact executable. A patch moves all of them, so the mod
checks the build hash when it attaches and, if it does not match, logs the refusal and does nothing
at all. Writing to those addresses in a patched binary would corrupt your save; refusing is the only
safe response. If Steam has updated you past 1.37.5, roll back through Steam's beta branches.

**Mod compatibility.** Total conversions work — Anbennar and Extended Timeline are both tested. The
mod reads trade nodes, goods, prices and modifiers the way the engine does, through your enabled mod
list with `replace_path` honoured, so it adapts to whatever map is loaded rather than assuming
vanilla's.

## Why a file called `version.dll`

EU4 imports Windows' `version.dll` at startup, and Windows looks in the game folder before the
system folder. Naming the mod `version.dll` means the game loads it on its own — that is the entire
trick, and it is why there is nothing to run or inject.

The mod still has to *provide* the seventeen functions the game expects from the real
`version.dll`. It does that at runtime: on startup it makes a private copy of the genuine system DLL
in your temp folder and forwards every call there. You never see or manage that copy.

*(If you used an earlier build, it required you to hand-copy the system DLL into the game folder as
`pgt_version_orig.dll`. That is no longer needed — delete it.)*

## Check that it worked

The mod writes `per-good-trade.log` in the game folder. After loading a campaign it should contain:

```
version.dll proxy: 17/17 exports resolved from ...\pgt_version_orig.dll
DIRECTION GATES OPEN (spec 1.10): 5/6 rebuild call sites hooked [MISSED 0x775EEC...]
[tick] monthly update 1: wrote 80 nodes inside the engine's value pass ...
```

`5/6` is correct, not an error: the sixth site is claimed by another part of the mod that installs
first. The log says so plainly rather than quietly rounding up.

In game, open the trade map mode — the arrows will differ from vanilla's. Click a province and the
map switches to that province's trade good, with its own network. That is the mod working.

## Uninstall

Delete `version.dll` from the game folder, and remove the mod in the launcher. That's all — nothing
is patched on disk, the executable is never modified, and saves made with the mod still load (their
trade simply reverts to vanilla's rules).

## Troubleshooting

**The game never opens — no window, no loading screen.** The `version.dll` you installed is not this
mod, or it is a 32-bit or corrupted copy. Replace it. (For the curious: an earlier build could do
this to itself, because the copy of the real DLL it loaded resolved back to the mod and every
forwarded call recursed until the process died. Fixed — the log now reports `17/17 exports resolved`
so this failure can never again be silent.)

**Trade looks exactly like vanilla.** The mod is not enabled in the launcher, or the build check
refused. The log says which.

**Antivirus quarantines the file.** Expected, and worth taking seriously as a category: this is a DLL
that loads into another process and patches its code, which is precisely what the heuristic looks
for. You are trusting whoever built the binary. Build it yourself from this repository if you would
rather not.

**It stopped working after a Steam update.** The build check is refusing a patched executable. Roll
back to 1.37.5.

**Multiplayer.** Not supported, not tested. Trade is computed locally; two clients would diverge.

## For developers

`impl/dll/install-proxy.ps1` installs a chosen build and can copy marker files:

```powershell
.\install-proxy.ps1 -Dll <path>\pgt_iNN.dll     # install
.\install-proxy.ps1 -Uninstall                  # remove
```

Every feature is on by default and each has a `pgt.<NAME>` escape hatch — an empty file in the game
folder named `pgt.NOAI`, `pgt.NOARROWS`, `pgt.NOTICKHOOK`, `pgt.NOINSTALL`, `pgt.NORELINK`,
`pgt.NOREVPANEL`, `pgt.NOCLICKGATE`, `pgt.NOCARAVAN`, `pgt.NOLIVEFIELD`, `pgt.NOGATES` turns that
piece off. Bisecting by disabling one hook at a time is how most of this mod's hard bugs were found.
