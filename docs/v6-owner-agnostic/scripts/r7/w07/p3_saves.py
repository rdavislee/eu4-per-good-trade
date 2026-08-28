# -*- coding: utf-8 -*-
"""Y486/Y557/Y558: parse the three start-date saves' trade node blocks and compare
the five node fields. Primary source: the save files themselves."""
import zipfile, re, os, sys, collections
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
FIELDS = ["current", "local_value", "outgoing", "total", "retention"]
def nodes(fn):
    raw = zipfile.ZipFile(os.path.join(SG, fn)).read("gamestate").decode("latin-1")
    i = raw.index("\ntrade={"); j = raw.index("{", i)
    tb = raw[j + 1:mb(raw, j)]
    out = []
    for m in re.finditer(r"^\tnode=\{", tb, re.M):
        st = tb.index("{", m.start()); rec = tb[st + 1:mb(tb, st)]
        nm = re.search(r'definitions="([^"]+)"', rec)
        d = {"name": nm.group(1) if nm else "?"}
        for f in FIELDS:
            mm = re.search(r"^\t\t" + f + r"=(-?[\d.]+)", rec, re.M)
            d[f] = float(mm.group(1)) if mm else None
        out.append(d)
    return {d["name"]: d for d in out}
A = nodes("VANILLA_start.eu4"); B = nodes("VANILLA2_start.eu4"); C = nodes("PERMUTE_start.eu4")
print("nodes parsed: VANILLA %d  VANILLA2 %d  PERMUTE %d" % (len(A), len(B), len(C)))
def cmp(x, y, tag):
    anydiff = set(); rows = []
    for f in FIELDS:
        n = d = 0; mx = 0.0; who = None
        for k in x:
            a, b = x[k][f], y[k][f]
            if a is None or b is None: continue
            n += 1
            if a != b:
                d += 1; anydiff.add(k)
                base = max(abs(a), abs(b))
                p = 100.0 * abs(a - b) / base if base else 0.0
                if p > mx: mx, who = p, k
        rows.append((f, d, n, mx, who))
    print("  %s" % tag)
    for f, d, n, mx, who in rows:
        print("    %-12s %2d of %2d differ, max %.3f%% (%s)" % (f, d, n, mx, who))
    print("    nodes differing on ANY of the five: %d of %d, overall max %.2f%%"
          % (len(anydiff), len(x), max(r[3] for r in rows)))
cmp(A, B, "VANILLA vs VANILLA2 (run-to-run control)")
cmp(A, C, "VANILLA vs PERMUTE (test)")
