# Re-assemble dist/pgt from the files it mirrors, so the two copies cannot drift silently.
$root = Split-Path $PSScriptRoot -Parent
$dist = $PSScriptRoot
New-Item -ItemType Directory -Force "$dist\pgt\common\tradenodes" | Out-Null
New-Item -ItemType Directory -Force "$dist\pgt\interface" | Out-Null
Copy-Item "$root\impl\out\00_tradenodes.txt"                 "$dist\pgt\common\tradenodes\00_tradenodes.txt" -Force
Copy-Item "$root\impl\out\00_tradenodes.txt"                 "$dist\pgt\common\tradenodes\phiw.baseline" -Force   # the DLL's restore copy (nodesync)
Copy-Item "$root\impl\mod\interface\countrytradeview.gui"    "$dist\pgt\interface\countrytradeview.gui" -Force
Write-Host "dist/pgt reassembled:"
Get-ChildItem -Recurse -File "$dist\pgt" | ForEach-Object { "  {0,8}  {1}" -f $_.Length, $_.FullName.Substring($dist.Length + 1) }
