import zipfile, re, os
SG = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                  "Europa Universalis IV", "save games", "VANILLA_start.eu4")
raw = zipfile.ZipFile(SG).read("gamestate").decode("latin-1")
def mb(s, i):
    d = 0; k = i; inq = False
    while k < len(s):
        c = s[k]
        if c == '"': inq = not inq
        elif not inq:
            if c == "{": d += 1
            elif c == "}":
                d -= 1
                if d == 0: return k
        k += 1
    return len(s) - 1
i = raw.index(chr(10) + "provinces={"); j = raw.index("{", i)
body = raw[j + 1:mb(raw, j)]
recs = {}
for m in re.finditer(r"^-(\d+)=\{", body, re.M):
    st = body.index("{", m.start())
    recs[int(m.group(1))] = body[st + 1:mb(body, st)]
print("province records:", len(recs))
have = [p for p, r in recs.items() if re.search(r"^\t\tgoods_produced=", r, re.M)]
print("records with a top-level goods_produced field:", len(have))
# show Garnatah 223 fields of interest
r = recs[223]
for k in ("base_tax", "base_production", "base_manpower", "trade_goods", "goods_produced",
          "local_autonomy", "trade_power", "production_efficiency"):
    m = re.search(r"^\t\t%s=(.*)$" % k, r, re.M)
    print("  223 %-22s %s" % (k, m.group(1).strip() if m else "ABSENT"))
