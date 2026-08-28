# Optional, cosmetic only: give Mare Liberum a tile image in the Paradox launcher.
#
# The launcher only shows tile art it downloaded from Steam Workshop; it never reads a
# picture from a locally installed mod's folder, so a hand-installed mod gets a blank tile.
# This script does for Mare Liberum exactly what the launcher does for a Workshop mod, and
# nothing else:
#
#   1. copies mod\pgt\thumbnail.png into the launcher's image cache, as
#      .launcher-cache\local-mod-thumbnail-pgt\thumbnail.png, and
#   2. fills in one column (thumbnailPath) of the launcher's mod database
#      (launcher-v2.sqlite), on Mare Liberum's row only, pointing at that copy.
#
# It uses Windows' own SQLite (winsqlite3.dll, part of Windows 10+): nothing is installed
# and no network is touched. Run it with the launcher CLOSED, after the launcher has seen
# the mod at least once (so the row exists). Safe to re-run. To undo, delete the
# local-mod-thumbnail-pgt cache folder: the tile goes back to blank, nothing else changes.

$ErrorActionPreference = 'Stop'

$docs  = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Paradox Interactive\Europa Universalis IV'
$db    = Join-Path $docs 'launcher-v2.sqlite'
$src   = Join-Path $docs 'mod\pgt\thumbnail.png'
$cache = Join-Path $docs '.launcher-cache\local-mod-thumbnail-pgt'
$dest  = Join-Path $cache 'thumbnail.png'

if (Get-Process 'Paradox Launcher' -ErrorAction SilentlyContinue) {
    Write-Output 'The Paradox launcher is open. Close it, then run this again.'
    exit 1
}
if (-not (Test-Path $src)) {
    Write-Output "Not found: $src"
    Write-Output 'Install the pgt mod folder first (INSTALL.md step 2).'
    exit 1
}
if (-not (Test-Path $db)) {
    Write-Output "Not found: $db"
    Write-Output 'Run the launcher once first so it creates its database.'
    exit 1
}

New-Item -ItemType Directory -Force -Path $cache | Out-Null
Copy-Item $src $dest -Force

Add-Type -Namespace Pgt -Name Sqlite -MemberDefinition @'
[DllImport("winsqlite3.dll")] public static extern int sqlite3_open(byte[] filename, out IntPtr db);
[DllImport("winsqlite3.dll")] public static extern int sqlite3_prepare_v2(IntPtr db, byte[] sql, int nBytes, out IntPtr stmt, IntPtr tail);
[DllImport("winsqlite3.dll")] public static extern int sqlite3_bind_text(IntPtr stmt, int index, byte[] value, int nBytes, IntPtr destructor);
[DllImport("winsqlite3.dll")] public static extern int sqlite3_step(IntPtr stmt);
[DllImport("winsqlite3.dll")] public static extern int sqlite3_finalize(IntPtr stmt);
[DllImport("winsqlite3.dll")] public static extern int sqlite3_changes(IntPtr db);
[DllImport("winsqlite3.dll")] public static extern int sqlite3_close(IntPtr db);
'@

function ToUtf8z([string]$s) { [Text.Encoding]::UTF8.GetBytes($s + [char]0) }

$h = [IntPtr]::Zero
if ([Pgt.Sqlite]::sqlite3_open((ToUtf8z $db), [ref]$h) -ne 0) {
    Write-Output 'Could not open the launcher database.'
    exit 1
}
$sql  = "UPDATE mods SET thumbnailPath = ?1 WHERE gameRegistryId = 'mod/pgt.mod'"
$stmt = [IntPtr]::Zero
if ([Pgt.Sqlite]::sqlite3_prepare_v2($h, (ToUtf8z $sql), -1, [ref]$stmt, [IntPtr]::Zero) -ne 0) {
    [Pgt.Sqlite]::sqlite3_close($h) | Out-Null
    Write-Output 'Could not prepare the update: unexpected database schema.'
    exit 1
}
$val = [Text.Encoding]::UTF8.GetBytes($dest)
[Pgt.Sqlite]::sqlite3_bind_text($stmt, 1, $val, $val.Length, [IntPtr](-1)) | Out-Null
$rc = [Pgt.Sqlite]::sqlite3_step($stmt)      # 101 = SQLITE_DONE
[Pgt.Sqlite]::sqlite3_finalize($stmt) | Out-Null
$n = [Pgt.Sqlite]::sqlite3_changes($h)
[Pgt.Sqlite]::sqlite3_close($h) | Out-Null

if ($rc -ne 101) {
    Write-Output "Update failed (SQLite step returned $rc)."
    exit 1
}
if ($n -eq 0) {
    Write-Output 'Mare Liberum is not in the launcher database yet.'
    Write-Output 'Open the launcher once so it scans the mod folder, close it, and run this again.'
    exit 1
}
Write-Output "Done: launcher tile art set for Mare Liberum ($n row updated)."
Write-Output 'Open the launcher to see it. To undo, delete:'
Write-Output "  $cache"
