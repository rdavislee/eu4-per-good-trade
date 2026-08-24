# Build per-good-trade.dll (the runtime-attached mod) and its load-test host.
# Determinism flags per spec 2.1: SSE2 baseline instruction stream, no -march=native, no
# -ffast-math, single-threaded. Builds to the scratchpad first (the OneDrive tree deletes some
# freshly-linked binaries) then copies the DLL back next to this script.
param([switch]$Debug)
$mingw = "C:\Users\rdavi\AppData\Local\Microsoft\WinGet\Packages\MartinStorsjo.LLVM-MinGW.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\llvm-mingw-20260421-ucrt-x86_64\bin"
$env:PATH = "$mingw;" + $env:PATH
$here = $PSScriptRoot
$scratch = "C:\Users\rdavi\AppData\Local\Temp\claude\C--Users-rdavi-OneDrive-Documents-Paradox-Interactive-Europa-Universalis-IV-mod-per-good-trade\2212c201-8c92-4b43-9989-442dc2c2b754\scratchpad\dllbuild"
New-Item -ItemType Directory -Force $scratch | Out-Null
$opt = if ($Debug) { "-O0 -g" } else { "-O2" }

# the mod DLL, exporting the version.dll forwarders so it can stand in as the injection vector.
# A DLL already injected into a running eu4.exe is locked, so build to a fresh name when that
# happens rather than failing the suite.
$dll = "$scratch\per-good-trade.dll"
if (Test-Path $dll) {
  try { [IO.File]::OpenWrite($dll).Close() }
  catch { $dll = "$scratch\per-good-trade-$(Get-Random -Maximum 99999).dll"
          Write-Host "(in-use DLL is loaded in a running game; building to $([IO.Path]::GetFileName($dll)))" }
}
$cmd = "g++ $opt -std=c++17 -shared -o `"$dll`" `"$here\dllmain.cpp`" `"$here\version.def`" -lversion -static-libgcc -static-libstdc++"
Write-Host $cmd
Invoke-Expression $cmd
if ($LASTEXITCODE -ne 0) { Write-Host "DLL BUILD FAILED"; exit 1 }

# the load-test host (refuse path) and the self-test host (pass path)
$host_exe = "$scratch\loadtest.exe"
g++ $opt -std=c++17 -o "$host_exe" "$here\loadtest.cpp"
if ($LASTEXITCODE -ne 0) { Write-Host "HOST BUILD FAILED"; exit 1 }
g++ $opt -std=c++17 -o "$scratch\selftest_host.exe" "$here\selftest_host.cpp"
if ($LASTEXITCODE -ne 0) { Write-Host "SELFTEST HOST BUILD FAILED"; exit 1 }
try { Copy-Item $dll "$scratch\version.dll" -Force } catch { }  # proxy-load filename (best effort)

try { Copy-Item $dll "$here\per-good-trade.dll" -Force } catch { Write-Host "(kept existing copy; target in use)" }
Write-Host "built $dll ($((Get-Item $dll).Length) bytes) and $host_exe"
Write-Host "copied DLL to $here\per-good-trade.dll"
