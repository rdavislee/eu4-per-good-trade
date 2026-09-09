# Install the mod DLL as the game's d3dx9_43.dll proxy, so it loads WITH eu4.exe and sets the mod
# up inside the loading screen (earlyload.h) -- no injector, no runner. Also copies the marker
# files (pgt.*) the DLL reads from its own directory, and removes everything with -Uninstall.
#
#   .\install-proxy.ps1 -Dll <path\to\per-good-trade.dll> [-Markers <dir with pgt.* files>]
#   .\install-proxy.ps1 -Uninstall
#
# THE SLOT IS d3dx9_43.dll (v1.0.2; v1.0 and v1.0.1 used version.dll). version.dll and d3d9.dll
# belong to the double-byte (CJK font) patches such as EU4DLL, whose loaders sit in the game
# directory at those names. eu4.exe imports d3dx9_43.dll by name (eight functions), no font patch
# claims that slot, and Windows loads the game-directory copy before the System32 one, so this mod
# and a font patch coexist. Steam's launch options are untouched.
#
# Files are recognised as OURS by content, never by name: every build of this mod carries the
# export-directory name "per-good-trade" (LIBRARY per-good-trade in the .def). A d3dx9_43.dll or
# version.dll without that string is somebody else's and is never touched.
#
# The real System32 d3dx9_43.dll is NOT copied here: the DLL itself copies it to
# %TEMP%\pgt_d3dx9_orig.dll at attach and loads that (proxy.h), so install is one file.
param(
  [string]$Dll = "",
  [string]$Markers = "",
  [switch]$Uninstall
)
$game = "C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
$target  = Join-Path $game "d3dx9_43.dll"
$oldslot = Join-Path $game "version.dll"            # where v1.0 and v1.0.1 installed
$oldorig = Join-Path $game "pgt_version_orig.dll"   # the pre-v1.0 hand-copied forwarder target
function IsOurs($path) {
  if (-not (Test-Path -LiteralPath $path)) { return $false }
  $bytes = [IO.File]::ReadAllBytes($path)
  return ([Text.Encoding]::GetEncoding(28591).GetString($bytes)).Contains("per-good-trade")
}
if ($Uninstall) {
  foreach ($f in @($target, $oldslot)) {
    if (Test-Path -LiteralPath $f) {
      if (IsOurs $f) { Remove-Item -LiteralPath $f -Force; Write-Host "removed $f" }
      else { Write-Host "left $f alone: not this mod (no per-good-trade export name; a font patch's or another tool's file)" }
    }
  }
  if (Test-Path -LiteralPath $oldorig) { Remove-Item -LiteralPath $oldorig -Force; Write-Host "removed $oldorig" }
  Get-ChildItem -LiteralPath $game -Filter "pgt.*" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force; Write-Host "removed $($_.Name)" }
  exit 0
}
if (-not $Dll -or -not (Test-Path -LiteralPath $Dll)) { Write-Host "usage: install-proxy.ps1 -Dll <per-good-trade.dll> [-Markers <dir>]"; exit 1 }
if (Get-Process eu4 -ErrorAction SilentlyContinue) { Write-Host "EU4 is running: close it first (d3dx9_43.dll is locked while it runs)"; exit 2 }
if (-not (IsOurs $Dll)) { Write-Host "FATAL: $Dll does not carry the per-good-trade export name; refusing to install a foreign DLL as the proxy"; exit 3 }
# A foreign d3dx9_43.dll (another tool's proxy, a stray runtime copy) is never overwritten.
if ((Test-Path -LiteralPath $target) -and -not (IsOurs $target)) { Write-Host "FATAL: $target exists and is not this mod; refusing to overwrite it"; exit 4 }
# An old build at version.dll loads BEFORE d3dx9_43.dll (eu4.exe's import order) and would own the
# process, leaving the new file inert (dllmain.cpp's one-instance test). Remove it; leave a font
# patch's version.dll alone.
if (Test-Path -LiteralPath $oldslot) {
  if (IsOurs $oldslot) { Remove-Item -LiteralPath $oldslot -Force; Write-Host "removed stale $oldslot (an older build of this mod)" }
  else { Write-Host "note: $oldslot is not this mod (a font patch's); left alone" }
}
if (Test-Path -LiteralPath $oldorig) { Remove-Item -LiteralPath $oldorig -Force; Write-Host "removed $oldorig (pre-v1.0 leftover)" }
Copy-Item -LiteralPath $Dll -Destination $target -Force
Write-Host "installed $Dll as $target (the DLL resolves the real System32 d3dx9_43.dll itself at attach)"
if ($Markers -and (Test-Path -LiteralPath $Markers)) {
  Get-ChildItem -LiteralPath $Markers -Filter "pgt.*" | Where-Object { $_.Name -ne "pgt.CMD" } | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $game $_.Name) -Force; Write-Host "  marker $($_.Name)"
  }
}
