import zipfile, re, os, collections
SG = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                  "Europa Universalis IV", "save games")
for sv in ("VANILLA_start.eu4", "Castile1444_12_22.eu4"):
    z = zipfile.ZipFile(os.path.join(SG, sv))
    print("==", sv, "entries:", z.namelist())
    for ent in z.namelist():
        raw = z.read(ent).decode("latin-1")
        n = len(re.findall(r"goods_produced", raw))
        print("   %-12s %9d bytes  goods_produced tokens: %d" % (ent, len(raw), n))
        if n:
            for m in list(re.finditer(r".{0,60}goods_produced.{0,40}", raw))[:6]:
                print("      ...", m.group(0).replace(chr(10), " | "))
