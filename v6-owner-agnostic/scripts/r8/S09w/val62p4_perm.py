# Y486 / Y492 / Y1021: compare the trade block of the reversed-order save against vanilla,
# and vanilla against a second vanilla run (the engine's own run-to-run variance).
import zipfile, re, os, collections
SG = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games"

def gamestate(sv):
    z = zipfile.ZipFile(os.path.join(SG, sv))
    return z.namelist(), z.read("gamestate").decode("latin-1")

def trade_block(raw):
    i = raw.index("\ntrade={")
    d = 0; j = raw.index("{", i); k = j
    while True:
        c = raw[k]
        if c == "{": d += 1
        elif c == "}":
            d -= 1
            if d == 0: break
        k += 1
    return raw[j:k + 1]

def nodes_of(block):
    """Split the trade block into per-node records keyed by definitions=."""
    out = collections.OrderedDict()
    for m in re.finditer(r'definitions="([^"]+)"', block):
        name = m.group(1)
        seg = block[m.end():m.end() + 1200]
        rec = {}
        for f in ("current", "local_value", "outgoing", "value_added_outgoing",
                  "retention", "total", "p_pow", "collector_power", "max_pow"):
            mm = re.search(r"\b%s=(-?[\d.]+)" % f, seg)
            if mm: rec[f] = mm.group(1)
        out[name] = rec
    return out

saves = {}
for sv in ("VANILLA_start.eu4", "VANILLA2_start.eu4", "PERMUTE_start.eu4"):
    names, raw = gamestate(sv)
    dm = re.search(r"\bdate=([\d.]+)", raw)
    blk = trade_block(raw)
    saves[sv] = nodes_of(blk)
    print("%-22s entries=%s date=%s nodes=%d" % (sv, names, dm.group(1) if dm else "?", len(saves[sv])))

def compare(a, b, fields):
    A, B = saves[a], saves[b]
    common = [n for n in A if n in B]
    res = {}
    for f in fields:
        diff = [n for n in common if A[n].get(f) != B[n].get(f)]
        res[f] = (len(diff), len(common))
    return res

FIELDS = ("total", "retention", "current", "local_value", "outgoing",
          "value_added_outgoing", "p_pow", "collector_power", "max_pow")
for pair in (("VANILLA_start.eu4", "VANILLA2_start.eu4"),
             ("VANILLA_start.eu4", "PERMUTE_start.eu4")):
    print()
    print("%s  vs  %s" % pair)
    for f, (d, n) in compare(pair[0], pair[1], FIELDS).items():
        print("   %-22s differing on %d of %d nodes" % (f, d, n))

# --- the 1/1000 grid, numerically (not by counting decimals) -----------------
print()
FQ = ("total", "val", "p_pow", "retention", "collector_power", "max_pow")
for sv in ("VANILLA_start.eu4", "VANILLA2_start.eu4", "PERMUTE_start.eu4",
           "Castile1444_12_22.eu4"):
    _, raw = gamestate(sv)
    blk = trade_block(raw)
    tot = off = 0
    for f in FQ:
        for v in re.findall(r"\b%s=(-?\d+(?:\.\d+)?)\b" % f, blk):
            tot += 1
            x = float(v) * 1000.0
            if abs(x - round(x)) > 1e-6: off += 1
    print("%-24s trade-block values on the 1/1000 grid: %d of %d" % (sv, tot - off, tot))
