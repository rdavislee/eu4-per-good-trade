# -*- coding: utf-8 -*-
"""Scan every readable save for change_price state: how many live keys per good."""
import os, re, zipfile, io
ROOT = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
SAVES = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games"

def body_of(path):
    try:
        if zipfile.is_zipfile(path):
            z = zipfile.ZipFile(path)
            names = z.namelist()
            out = []
            for n in names:
                try: out.append(z.read(n).decode("cp1252", "replace"))
                except Exception: pass
            return "\n".join(out), names
        return open(path, "rb").read().decode("cp1252", "replace"), ["<plain>"]
    except Exception as e:
        return None, str(e)

def analyse(path, label):
    txt, names = body_of(path)
    if txt is None:
        print("  %-42s UNREADABLE (%s)" % (label, names)); return
    i = txt.find("change_price={")
    if i < 0:
        print("  %-42s no change_price state block  (entries=%s)" % (label, names)); return
    # take the outer block
    d = 0; j = i + len("change_price=")
    start = j
    while j < len(txt):
        if txt[j] == "{": d += 1
        elif txt[j] == "}":
            d -= 1
            if d == 0: break
        j += 1
    blk = txt[start+1:j]
    goods = re.findall(r"([a-z_]+)=\{((?:[^{}]|\{[^{}]*\})*)\}", blk)
    multi = []
    tot = 0
    for g, b in goods:
        keys = re.findall(r'key="?([A-Za-z_0-9]+)"?', b)
        tot += len(keys)
        if len(keys) >= 2: multi.append((g, keys))
    print("  %-42s goods=%-3d total live keys=%-3d goods with >=2 keys: %s"
          % (label, len(goods), tot, multi if multi else "none"))

print("=== shipped tutorial saves ===")
for f in sorted(os.listdir(os.path.join(ROOT, "tutorial"))):
    if f.endswith(".eu4"):
        analyse(os.path.join(ROOT, "tutorial", f), f)
print("=== user save games (readable only) ===")
if os.path.isdir(SAVES):
    for f in sorted(os.listdir(SAVES)):
        if not f.lower().endswith(".eu4"): continue
        p = os.path.join(SAVES, f)
        try:
            sz = os.path.getsize(p)
        except Exception:
            continue
        if sz < 4096:
            continue   # OneDrive placeholder
        analyse(p, "%s (%d bytes)" % (f, sz))
