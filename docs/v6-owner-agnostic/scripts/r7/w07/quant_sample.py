# -*- coding: utf-8 -*-
"""Independent sampler for the 1/1000-quantisation claim (spec 2.1, doc line 959).
Reads VANILLA_start.eu4's gamestate, isolates the trade={...} block, and tests every
occurrence of total/val/p_pow/retention/collector_power/max_pow for exact alignment
to a 1/1000 grid."""
import zipfile, re, os

SAVE = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                     "Europa Universalis IV", "save games", "VANILLA_start.eu4")
raw = zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")

# isolate the top-level trade={ ... } block by brace matching
i = raw.index(chr(10) + "trade={")
j = raw.index("{", i)
depth = 0; k = j; inq = False
while k < len(raw):
    c = raw[k]
    if c == '"':
        inq = not inq
    elif not inq:
        if c == "{": depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0: break
    k += 1
block = raw[j+1:k]
print("trade block length:", len(block))

FIELDS = ["total", "val", "p_pow", "retention", "collector_power", "max_pow"]
GRID = 1.0 / 1000.0
results = {}
for f in FIELDS:
    vals = [float(x) for x in re.findall(r'(?<![a-zA-Z_])' + f + r'=(-?\d+\.\d+)', block)]
    results[f] = vals

total_n = 0; total_on_grid = 0
for f in FIELDS:
    vals = results[f]
    n = len(vals)
    on_grid = sum(1 for v in vals if abs(round(v * 1000) - v * 1000) < 1e-6)
    off = [v for v in vals if abs(round(v * 1000) - v * 1000) >= 1e-6]
    total_n += n; total_on_grid += on_grid
    print("%-18s n=%5d  on-1/1000-grid=%5d  off-grid examples=%s" % (f, n, on_grid, off[:5]))

print()
print("TOTAL sampled=%d  on-grid=%d  (%.4f%%)" % (total_n, total_on_grid, 100.0*total_on_grid/total_n))

# also report a fixed-size 495 subsample (first N found in file order across all fields, interleaved)
print()
print("as a check: first 495 values in file order across all six fields")
allvals = []
for m in re.finditer(r'(?<![a-zA-Z_])(' + '|'.join(FIELDS) + r')=(-?\d+\.\d+)', block):
    allvals.append((m.group(1), float(m.group(2))))
first495 = allvals[:495]
on_grid_495 = sum(1 for _, v in first495 if abs(round(v*1000) - v*1000) < 1e-6)
print("first 495 (if that many exist): n=%d on-grid=%d" % (len(first495), on_grid_495))
