# -*- coding: utf-8 -*-
"""Y557/Y558: re-derive the vanilla-vs-vanilla noise from the saves under several
percentage bases, to locate the 8.96% figure the spec quotes."""
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
FIELDS = ["current", "local_value", "outgoing", "total", "retention"]
def nodes(fn):
    raw = zipfile.ZipFile(os.path.join(SG, fn)).read("gamestate").decode("latin-1")
    i = raw.index("\ntrade={"); j = raw.index("{", i)
    tb = raw[j+1:mb(raw, j)]
    out = {}
    for m in re.finditer(r"^\tnode=\{", tb, re.M):
        st = tb.index("{", m.start()); rec = tb[st+1:mb(tb, st)]
        nm = re.search(r'definitions="([^"]+)"', rec)
        d = {"name": nm.group(1) if nm else "?"}
        for f in FIELDS:
            mm = re.search(r"^\t\t"+f+r"=(-?[\d.]+)", rec, re.M)
            d[f] = float(mm.group(1)) if mm else None
        out[d["name"]] = d
    return out
A = nodes("VANILLA_start.eu4"); B = nodes("VANILLA2_start.eu4")
for basis in ("max", "first", "min"):
    print("basis = %s" % basis)
    anyd = set(); gmax = 0.0; gwho = None
    for f in FIELDS:
        n=dn=0; mx=0.0; who=None
        for k in A:
            a,b = A[k][f], B[k][f]
            if a is None or b is None: continue
            n += 1
            if a != b:
                dn += 1; anyd.add(k)
                den = {"max":max(abs(a),abs(b)),"first":abs(a),"min":min(abs(a),abs(b))}[basis]
                p = 100.0*abs(a-b)/den if den else float('inf')
                if p > mx: mx, who = p, k
        if mx > gmax: gmax, gwho = mx, who
        print("   %-12s %2d of %2d differ, max %.3f%% (%s)" % (f, dn, n, mx, who))
    print("   nodes differing on ANY: %d of %d ; overall max %.3f%% (%s)" % (len(anyd), len(A), gmax, gwho))
