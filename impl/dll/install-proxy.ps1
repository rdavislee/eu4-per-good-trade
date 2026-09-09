# Install the mod DLL as the game's d3dx9_43.dll proxy, so it loads WITH eu4.exe and sets the mod
# up inside the loading screen (earlyload.h) -- no injector, no runner. Also copies the marker
# files (pgt.*) the DLL reads from its own directory, and removes everything with -Uninstall.
#
#   .\install-proxy.ps1 -Dll <path\to\pgt_iNN.dll> [-Markers <dir with pgt.* files>]
#   .\install-proxy.ps1 -Uninstall
#
# THE SLOT IS d3dx9_43.dll, NOT version.dll/d3d9.dll: those two names belong to the double-byte
# (CJK font) patches (EU4DLL and its kin), whose loaders already sit in the game directory and
# load their plugins from the plugins\ folder. eu4.exe imports d3dx9_43.dll by name (eight
# functions), no font patch claims that slot, and Windows loads the game-directory copy before
# the System32 one -- so this mod and the double-byte patch coexist unchanged, exactly like the
# Epic-store build (d3dx9_43.dll there too). Steam's launch options are untouched.
#
# The real System32 d3dx9_43.dll is NOT copied here: the DLL itself copies it to
# %TEMP%\pgt_d3dx9_orig.dll at attach and loads that (proxy.h), so install is one file.
param(
  [string]$Dll = "",
  [string]$Markers = "",
  [switch]$Uninstall
)
$game = "C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
$target = Join-Path $game "d3dx9_43.dll"
$legacyPlugin = Join-Path $game "plugins\per-good-trade.dll"
if ($Uninstall) {
  if (Test-Path $target) { Remove-Item -LiteralPath $target -Force; Write-Host "removed $target" }
  Get-ChildItem -LiteralPath $game -Filter "pgt.*" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force; Write-Host "removed $($_.Name)" }
  if (Test-Path $legacyPlugin) { Write-Host "note: legacy $legacyPlugin (plugin-folder install) left in place; remove it to uninstall the old deployment" }
  Write-Host "removed the mod's files. version.dll/d3d9.dll and plugins\* were NOT touched (they belong to the double-byte patch)."
  exit 0
}
if (-not $Dll -or -not (Test-Path -LiteralPath $Dll)) { Write-Host "usage: install-proxy.ps1 -Dll <pgt_iNN.dll> [-Markers <dir>]"; exit 1 }
if (Get-Process eu4 -ErrorAction SilentlyContinue) { Write-Host "EU4 is running: close it first (d3dx9_43.dll is locked while it runs)"; exit 2 }
if (Test-Path -LiteralPath $target) { Write-Host "FATAL: $target already exists -- refusing to overwrite (it may be the system DirectX copy or another mod's proxy)"; exit 3 }
# A legacy plugin-folder copy would attach BEFORE this proxy (EU4DLL loads plugins\* inside its
# own version.dll DllMain, which eu4.exe imports before d3dx9_43.dll) and the later copy would
# find the seams already claimed and stay inert -- confusing logs and a mod that depends on the
# double-byte patch's loader. Refuse to install over it rather than silently double-deploy.
if (Test-Path -LiteralPath $legacyPlugin) { Write-Host "FATAL: legacy plugin install present at $legacyPlugin"; Write-Host "  the new build must be the ONLY copy in the process. Remove it first:"; Write-Host "  Remove-Item '$legacyPlugin'"; exit 4 }
Copy-Item -LiteralPath $Dll -Destination $target -Force
Write-Host "installed $Dll as $target (the DLL resolves the real System32 d3dx9_43.dll itself at attach)"
if ($Markers -and (Test-Path -LiteralPath $Markers)) {
  Get-ChildItem -LiteralPath $Markers -Filter "pgt.*" | Where-Object { $_.Name -ne "pgt.CMD" } | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $game $_.Name) -Force; Write-Host "  marker $($_.Name)"
  }
}
Write-Host "the DLL logs to $game\per-good-trade.log; launch the game normally (a campaign sets up during its loading screen)"
