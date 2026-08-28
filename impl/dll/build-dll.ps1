# Build per-good-trade.dll (the runtime-attached mod) and its load-test host.
# REPRODUCIBLE: -Wl,--no-insert-timestamp zeroes the PE and debug-directory timestamps, which
# were the ONLY bytes that differed between two builds of identical source (4 bytes, measured).
# So anyone can rebuild this and compare hashes against a release binary rather than trusting it.
# Determinism flags per spec 2.1: SSE2 baseline instruction stream, no -march=native, no
# -ffast-math, single-threaded. Builds to the scratchpad first (the OneDrive tree deletes some
# freshly-linked binaries) then copies the DLL back next to this script.
#
# TOOLCHAIN: llvm-mingw, UCRT, x86_64 -- built and verified with llvm-mingw-20260421-ucrt-x86_64
# (clang 22.1.4). Install with:  winget install MartinStorsjo.LLVM-MinGW.UCRT
# Any llvm-mingw UCRT x86_64 build should do; plain MSYS2 mingw-w64 is untested here.
#
# Pass -Mingw for a specific toolchain bin directory and -Scratch to build elsewhere. Both were
# once hardcoded to one machine's paths, so nobody else could build this -- while INSTALL.md was
# telling readers to build it themselves if they would rather not trust a prebuilt DLL.
param(
  [switch]$Debug,
  [string]$Mingw = "",
  [string]$Scratch = ""
)
$here = $PSScriptRoot

if (-not $Mingw -and -not (Get-Command g++ -ErrorAction SilentlyContinue)) {
  # the usual winget install location, newest matching toolchain first
  $glob = Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Packages\MartinStorsjo.LLVM-MinGW.UCRT_*\llvm-mingw-*-ucrt-x86_64\bin"
  $found = Get-ChildItem -Path $glob -Directory -ErrorAction SilentlyContinue |
           Sort-Object Name -Descending | Select-Object -First 1
  if ($found) { $Mingw = $found.FullName }
}
if ($Mingw) { $env:PATH = "$Mingw;" + $env:PATH }
if (-not (Get-Command g++ -ErrorAction SilentlyContinue)) {
  Write-Host "FATAL: no g++ on PATH and no llvm-mingw found."
  Write-Host "  install:  winget install MartinStorsjo.LLVM-MinGW.UCRT"
  Write-Host "  or pass:  .\build-dll.ps1 -Mingw <path-to-toolchain>\bin"
  exit 1
}

# Build OUTSIDE the source tree by default: this repo commonly lives under OneDrive, whose sync
# can delete or lock a freshly linked binary mid-build.
if (-not $Scratch) { $Scratch = Join-Path $env:TEMP "per-good-trade-build" }
$scratch = $Scratch
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
$cmd = "g++ $opt -std=c++17 -shared -o `"$dll`" `"$here\dllmain.cpp`" `"$here\version.def`" -lversion -static-libgcc -static-libstdc++ '-Wl,--no-insert-timestamp'"
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
