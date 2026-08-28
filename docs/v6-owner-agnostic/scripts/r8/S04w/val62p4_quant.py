# Y1021: every trade number EU4 writes to a save is quantised to 1/1000, across
# total, val, p_pow, retention, collector_power, max_pow. Also Y475: Garnatah (223) local_autonomy.
import zipfile, re, os
SG = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games"
FIELDS = ("total", "val", "p_pow", "retention", "collector_power", "max_pow")
for sv in ("VANILLA_start.eu4", "Castile1444_12_22.eu4"):
    raw = zipfile.ZipFile(os.path.join(SG, sv)).read("gamestate").decode("latin-1")
    i = raw.index("\ntrade={")
    # take the trade block: from here to the next top-level key; approximate by matching braces
    d = 0; j = raw.index("{", i); k = j
    while True:
        c = raw[k]
        if c == "{": d += 1
        elif c == "}":
            d -= 1
            if d == 0: break
        k += 1
    block = raw[j:k+1]
    tot = off = 0
    per = {}
    for f in FIELDS:
        vals = re.findall(r"\b%s=(-?\d+(?:\.\d+)?)\b" % f, block)
        n = len(vals); bad = 0
        for v in vals:
            if "." in v and len(v.split(".")[1]) > 3:
                bad += 1
        per[f] = (n, bad)
        tot += n; off += bad
    print(sv, "trade-block fields:", per, "TOTAL", tot, "off-grid", off)
# Garnatah province 223 local_autonomy
raw = zipfile.ZipFile(os.path.join(SG, "VANILLA_start.eu4")).read("gamestate").decode("latin-1")
m = re.search(r"^-223=\{", raw, re.M)
seg = raw[m.start():m.start()+4000]
la = re.search(r"local_autonomy=([\d.]+)", seg)
print("province 223 local_autonomy:", la.group(1) if la else "ABSENT (defaults 0)")
print("223 header context:", re.search(r'name="([^"]+)"', seg).group(1))
