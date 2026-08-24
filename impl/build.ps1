# Build the impl solver harness. Determinism flags per spec 2.1: single compiled instruction
# stream at the x86-64 SSE2 baseline, no -ffast-math, no -march=native, single-threaded code.
param([switch]$Debug)
$src = Join-Path $PSScriptRoot "src\main.cpp"
$out = Join-Path $PSScriptRoot "impl.exe"
$opt = if ($Debug) { "-O0 -g" } else { "-O2" }
# NOT -static: something on this machine silently deletes freshly-linked static MinGW exes
# (no Defender event logged; a copied exe persists, a static-linked one vanishes in seconds).
# The dynamic build persists and runs; it needs llvm-mingw's bin on PATH for libc++/winpthread.
$flags = "$opt -std=c++17 -Wall -Wextra -Wno-unused-parameter"
$cmd = "g++ $flags `"$src`" -o `"$out`""
Write-Host $cmd
Invoke-Expression $cmd
if ($LASTEXITCODE -eq 0) { Write-Host "built $out" } else { Write-Host "BUILD FAILED" }
exit $LASTEXITCODE
