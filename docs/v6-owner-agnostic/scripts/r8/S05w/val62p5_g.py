# -*- coding: utf-8 -*-
"""Y1040: the 1/1000 grid across the six named trade fields, counted per save."""
import zipfile, re, os
from decimal import Decimal
SG = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games"
FIELDS = ("total","val","p_pow","retention","collector_power","max_pow")
def block(raw):
    i = raw.index("\ntrade={"); j = raw.index("{", i); d=0; k=j
    while True:
        c = raw[k]
        if c=="{": d+=1
        elif c=="}":
            d-=1
            if d==0: break
        k+=1
    return raw[j:k+1]
for sv in ("VANILLA_start.eu4","VANILLA2_start.eu4","PERMUTE_start.eu4","Castile1444_12_22.eu4"):
    p = os.path.join(SG, sv)
    if not os.path.exists(p): print(sv, "MISSING"); continue
    raw = zipfile.ZipFile(p).read("gamestate").decode("latin-1")
    b = block(raw)
    tot=off=0; per={}
    for f in FIELDS:
        vals = re.findall(r"\b%s=(-?\d+(?:\.\d+)?)\b" % f, b)
        bad = sum(1 for v in vals if (Decimal(v) * 1000) % 1 != 0)
        per[f]=(len(vals),bad); tot+=len(vals); off+=bad
    print("%-26s %s  TOTAL %d  off-grid %d" % (sv, per, tot, off))
