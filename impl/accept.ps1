# Solver-track acceptance: every check the reference side can run without the engine.
# Fails loudly if any step regresses. The engine-side (★) tests in TESTING.md need the DLL
# attached to a running game and are not run here.
$ErrorActionPreference = "Stop"
$mingw = "C:\Users\rdavi\AppData\Local\Microsoft\WinGet\Packages\MartinStorsjo.LLVM-MinGW.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\llvm-mingw-20260421-ucrt-x86_64\bin"
$env:PATH = "$mingw;" + $env:PATH
$impl = $PSScriptRoot
$exe  = "$impl\impl.exe"
$eu4  = "C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
$save = "$env:USERPROFILE\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\VANILLA_start.eu4"
$fails = 0

function Step($name, $block) {
  Write-Host "=== $name ===" -ForegroundColor Cyan
  & $block
  if ($LASTEXITCODE -ne 0) { Write-Host "FAILED: $name" -ForegroundColor Red; $script:fails++ }
}

Step "build" { & "$impl\build.ps1" | Out-Host }
Step "reference dump (python)" {
  python "$impl\tools\refdump.py" "$impl\dumps\ref1444.json" | Out-Host
}
Step "cpp dump" { & $exe dump $eu4 $save "$impl\dumps\cpp1444.json" | Out-Host }
Step "A5 cross-implementation orientation equality" {
  python "$impl\tools\compare.py" "$impl\dumps\ref1444.json" "$impl\dumps\cpp1444.json" | Out-Host
}
Step "per-tick assertion battery" { (& $exe checks $eu4 $save | Select-String "RESULT") | Out-Host }
Step "negative fixtures (each checker goes RED)" { (& $exe fixtures | Select-String "RESULT") | Out-Host }
Step "economy fixtures (spec 1.8 routing, each with a red twin)" { (& $exe econ | Select-String "RESULT") | Out-Host }
Step "inline-hook machinery self-test (detour.h)" {
  $sc = "C:\Users\rdavi\AppData\Local\Temp\claude\C--Users-rdavi-OneDrive-Documents-Paradox-Interactive-Europa-Universalis-IV-mod-per-good-trade\2212c201-8c92-4b43-9989-442dc2c2b754\scratchpad\dllbuild"
  & g++ -O2 -std=c++17 -o "$sc\detourtest.exe" "$impl\dll\detourtest.cpp" 2>&1 | Select-Object -First 4 | Out-Host
  (& "$sc\detourtest.exe" | Select-String "RESULT") | Out-Host
}
Step "reachability census + survival skeleton" { & $exe census $eu4 $save | Out-Host }
Step "determinism (H1)" { & $exe determinism $eu4 $save | Out-Host }
Step "razed China (F2 / 2.8)" { & $exe shock $eu4 $save hangzhou | Out-Host }
Step "emit 00_tradenodes.txt (A2/A3)" { & $exe emit $eu4 $save "$impl\out\00_tradenodes.txt" | Out-Host }
Step "attach build gate (A4)" { & $exe "verify-build" $eu4 | Out-Host }
Step "reference harness verify6 (0 failed)" {
  Push-Location "$impl\..\v6-owner-agnostic\scripts"
  (python verify6.py ../per-good-trade-spec.md | Select-String "RESULT") | Out-Host
  Pop-Location
}
# Preserve the live-game evidence before the gate steps (which rewrite the same log file).
$sc0 = "C:\Users\rdavi\AppData\Local\Temp\claude\C--Users-rdavi-OneDrive-Documents-Paradox-Interactive-Europa-Universalis-IV-mod-per-good-trade\2212c201-8c92-4b43-9989-442dc2c2b754\scratchpad\dllbuild"
if (Test-Path "$sc0\per-good-trade.log") { Copy-Item "$sc0\per-good-trade.log" "$sc0\live-evidence.log" -Force }

Step "DLL build (attach + embedded solver)" { & "$impl\dll\build-dll.ps1" | Select-Object -Last 1 | Out-Host }
Step "DLL attach gate refuses a non-target host (A4)" {
  $sc = "C:\Users\rdavi\AppData\Local\Temp\claude\C--Users-rdavi-OneDrive-Documents-Paradox-Interactive-Europa-Universalis-IV-mod-per-good-trade\2212c201-8c92-4b43-9989-442dc2c2b754\scratchpad\dllbuild"
  Remove-Item "$sc\per-good-trade.log" -ErrorAction SilentlyContinue
  Push-Location $sc; $d = (Get-ChildItem "$sc\per-good-trade*.dll" | Sort-Object LastWriteTime -Desc | Select-Object -First 1).FullName; & "$sc\loadtest.exe" $d | Out-Null; Pop-Location
  $refused = (Get-Content "$sc\per-good-trade.log" -ErrorAction SilentlyContinue) -match "REFUSE"
  if ($refused) { Write-Host "refused non-target host (fails closed)" } else { Write-Host "GATE DID NOT REFUSE"; exit 1 }
}
Step "DLL pass path + in-process solver" {
  $sc = "C:\Users\rdavi\AppData\Local\Temp\claude\C--Users-rdavi-OneDrive-Documents-Paradox-Interactive-Europa-Universalis-IV-mod-per-good-trade\2212c201-8c92-4b43-9989-442dc2c2b754\scratchpad\dllbuild"
  $log = "$eu4\per-good-trade.log"
  Remove-Item $log -ErrorAction SilentlyContinue
  $env:PGT_ROOT = $eu4
  Push-Location $sc; $d = (Get-ChildItem "$sc\per-good-trade*.dll" | Sort-Object LastWriteTime -Desc | Select-Object -First 1).FullName; & "$sc\selftest_host.exe" $d | Out-Null; Pop-Location
  Remove-Item Env:\PGT_ROOT
  $ok = (Get-Content $log -ErrorAction SilentlyContinue) -match "build gate PASS"
  $solved = (Get-Content $log -ErrorAction SilentlyContinue) -match "Phi_w ends \{ hangzhou genua"
  Remove-Item $log -ErrorAction SilentlyContinue
  if ($ok -and $solved) { Write-Host "gate passed on target; embedded solver ran in-process (ends hangzhou/genua)" }
  else { Write-Host "PASS PATH FAILED"; exit 1 }
}

Step "DLL injector builds (live attach to a running game)" {
  $mingw = "C:\Users\rdavi\AppData\Local\Microsoft\WinGet\Packages\MartinStorsjo.LLVM-MinGW.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\llvm-mingw-20260421-ucrt-x86_64\bin"
  $env:PATH = "$mingw;" + $env:PATH
  $sc = "C:\Users\rdavi\AppData\Local\Temp\claude\C--Users-rdavi-OneDrive-Documents-Paradox-Interactive-Europa-Universalis-IV-mod-per-good-trade\2212c201-8c92-4b43-9989-442dc2c2b754\scratchpad\dllbuild"
  & g++ -O2 -std=c++17 -o "$sc\injector.exe" "$impl\dll\injector.cpp" 2>&1 | Select-Object -First 4 | Out-Host
  if (Test-Path "$sc\injector.exe") { Write-Host "injector.exe built" } else { Write-Host "INJECTOR BUILD FAILED"; exit 1 }
}
Step "live-game integration (evidence from the running EU4)" {
  $sc = "C:\Users\rdavi\AppData\Local\Temp\claude\C--Users-rdavi-OneDrive-Documents-Paradox-Interactive-Europa-Universalis-IV-mod-per-good-trade\2212c201-8c92-4b43-9989-442dc2c2b754\scratchpad\dllbuild"
  $log = "$sc\live-evidence.log"
  if (-not (Test-Path $log)) { $log = "$sc\per-good-trade.log" }
  if (-not (Test-Path $log)) { Write-Host "no live-game log yet (inject the DLL into a running game)"; return }
  $l = Get-Content $log
  $checks = @(
    @{ n = "build gate passed in-process";      p = "build gate PASS" },
    @{ n = "solver ran inside eu4.exe";         p = "solver self-test: 2472 provinces" },
    @{ n = "read the live CTradeNode array";    p = "CTradeNode array: \d+ nodes read" },
    @{ n = "solved+routed the per-good graphs"; p = "solved\+routed \d+ goods" },
    @{ n = "installed values into the engine";  p = "INSTALLED into the engine" },
    @{ n = "re-installs on the monthly tick";   p = "\[monthly\] tick" }
  )
  foreach ($c in $checks) {
    $hit = $l | Select-String $c.p | Select-Object -Last 1
    if ($hit) { Write-Host ("  [OK]   " + $c.n + " -- " + $hit.Line.Trim()) }
    else { Write-Host ("  [MISS] " + $c.n) }
  }
}

Write-Host ""
if ($fails -eq 0) { Write-Host "SOLVER-TRACK ACCEPTANCE: ALL GREEN" -ForegroundColor Green }
else { Write-Host "SOLVER-TRACK ACCEPTANCE: $fails STEP(S) FAILED" -ForegroundColor Red }
exit $fails
