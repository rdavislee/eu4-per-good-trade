# -*- coding: utf-8 -*-
"""Probe: does the FULL node record show which fields plausibly are 'the three power-dependent
fields'? Extract ALL top-level scalar fields under one node= block from VANILLA_start.eu4 to see
what's actually present, then diff every field between the two vanilla saves."""
import zipfile, re, os
SG = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games"
def mb(s, i):
    d = 0; k = i; q = False
    while k < len(s):
        c = s[k]
        if c == '"': q = not q
        elif not q:
            if c == "{": d += 1
            elif c == "}":
                d -= 1
                if d == 0: return k
        k += 1
    return len(s) - 1
def raw_trade(fn):
    raw = zipfile.ZipFile(os.path.join(SG, fn)).read("gamestate").decode("latin-1")
    i = raw.index("\ntrade={"); j = raw.index("{", i)
    return raw[j+1:mb(raw, j)]

tb = raw_trade("VANILLA_start.eu4")
# grab the first node block entirely and print its scalar fields
m = re.search(r"^\tnode=\{", tb, re.M)
st = tb.index("{", m.start()); rec = tb[st+1:mb(tb, st)]
print("first node block scalar top-level keys:")
for mm in re.finditer(r"^\t\t(\w+)=([^\{\n][^\n]*)$", rec, re.M):
    print("  ", mm.group(1), "=", mm.group(2)[:40])
