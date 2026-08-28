# Install the mod DLL as the game's version.dll proxy, so it loads WITH eu4.exe and sets the mod up
# inside the loading screen (earlyload.h) -- no injector, no runner. Also copies the marker files
# (pgt.*) the DLL reads from its own directory, and removes everything with -Uninstall.
#
#   .\install-proxy.ps1 -Dll <path\to\pgt_iNN.dll> [-Markers <dir with pgt.* files>]
#   .\install-proxy.ps1 -Uninstall
#
# The DLL exports the version.dll forwarders (version.def), so the game's own imports resolve
# through it to the real system version.dll. Steam's launch options are untouched.
param(
  [string]$Dll = "",
  [string]$Markers = "",
  [switch]$Uninstall
)
$game = "C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
$target = Join-Path $game "version.dll"
$orig = Join-Path $game "pgt_version_orig.dll"
if ($Uninstall) {
  if (Test-Path $target) { Remove-Item -LiteralPath $target -Force; Write-Host "removed $target" }
  if (Test-Path $orig) { Remove-Item -LiteralPath $orig -Force; Write-Host "removed $orig" }
  Get-ChildItem -LiteralPath $game -Filter "pgt.*" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force; Write-Host "removed $($_.Name)" }
  exit 0
}
if (-not $Dll -or -not (Test-Path -LiteralPath $Dll)) { Write-Host "usage: install-proxy.ps1 -Dll <pgt_iNN.dll> [-Markers <dir>]"; exit 1 }
if (Get-Process eu4 -ErrorAction SilentlyContinue) { Write-Host "EU4 is running: close it first (version.dll is locked while it runs)"; exit 2 }
# THE REAL version.dll, under a private name. Our exports forward to pgt_version_orig, never to
# "version" -- that name would resolve back to us (the game directory is searched first) and the
# self-referential forwarder kills the process at load, before any window or log.
$sys = Join-Path $env:SystemRoot (Join-Path 'System32' 'version.dll')
if (-not (Test-Path -LiteralPath $sys)) { Write-Host "FATAL: $sys not found"; exit 3 }
Copy-Item -LiteralPath $sys -Destination $orig -Force
Write-Host "installed $sys as $orig (the forwarder target)"
Copy-Item -LiteralPath $Dll -Destination $target -Force
Write-Host "installed $Dll as $target"
# a proxy that cannot resolve its forwarders is worse than no proxy: verify both files landed
if (-not (Test-Path -LiteralPath $orig) -or -not (Test-Path -LiteralPath $target)) { Write-Host "FATAL: proxy pair incomplete"; exit 4 }
if ($Markers -and (Test-Path -LiteralPath $Markers)) {
  Get-ChildItem -LiteralPath $Markers -Filter "pgt.*" | Where-Object { $_.Name -ne "pgt.CMD" } | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $game $_.Name) -Force; Write-Host "  marker $($_.Name)"
  }
}
Write-Host "the DLL logs to $game\per-good-trade.log; launch the game normally (a campaign sets up during its loading screen)"
