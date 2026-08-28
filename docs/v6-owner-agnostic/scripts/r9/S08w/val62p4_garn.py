# Careful province-block extraction from the 1444 saves: base_tax/base_production/
# local_autonomy/trade goods for the provinces cited in spec 2.3's coefficient table.
import zipfile, re, os
SG = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games"

def load(sv):
    return zipfile.ZipFile(os.path.join(SG, sv)).read("gamestate").decode("latin-1")

def block(raw, pid):
    m = re.search(r"^-%d=\{" % pid, raw, re.M)
    if not m: return None
    j = raw.index("{", m.start()); d = 0; k = j
    while True:
        c = raw[k]
        if c == "{": d += 1
        elif c == "}":
            d -= 1
            if d == 0: break
        k += 1
    return raw[j:k+1]

for sv in ("VANILLA_start.eu4",):
    raw = load(sv)
    dm = re.search(r"^date=([\d.]+)", raw, re.M)
    print("%s  date=%s" % (sv, dm.group(1) if dm else "?"))
    for pid in (223, 1747, 212, 213):
        b = block(raw, pid)
        nm = re.search(r'name="([^"]+)"', b)
        out = {}
        for key in ("base_tax", "base_production", "base_manpower", "local_autonomy",
                    "trade_goods", "owner", "devastation"):
            # ANY indentation, but only at the top level of the province block (one tab depth
            # inside the block is depth 2 in the file); take all matches and report them.
            vals = re.findall(r"(?m)^\s*%s=\"?([^\"\n]*?)\"?\s*$" % key, b)
            out[key] = vals
        print("  %-5d %-12s %s" % (pid, nm.group(1), out))
