# dist: what a player installs

Copy **`pgt.mod`** and the **`pgt`** folder into your EU4 mod directory
(`%USERPROFILE%\Documents\Paradox Interactive\Europa Universalis IV\mod`), then enable
**Mare Liberum** in the launcher. The DLL half is separate; see [../INSTALL.md](../INSTALL.md).

This folder is assembled from files that live elsewhere in the repo; it is committed so that
INSTALL.md's steps can actually be followed:

| file here | source of truth |
|---|---|
| `pgt/common/tradenodes/00_tradenodes.txt` | `impl/out/00_tradenodes.txt` |
| `pgt/interface/countrytradeview.gui` | `impl/mod/interface/countrytradeview.gui` |
| `pgt.mod`, `pgt/descriptor.mod` | written here |

Re-assemble after changing either source file:

```powershell
.\dist\build-mod.ps1
```

The mod folder carries no mechanics. The model lives entirely in the DLL. Installing this half
alone changes almost nothing, which is why the DLL is not optional.
