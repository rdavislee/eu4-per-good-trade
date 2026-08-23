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
    tb = raw[j + 1:mb(raw, j)]
    out = []
    for m in re.finditer(r"^\tnode=\{", tb, re.M):
        st = tb.index("{", m.start()); rec = tb[st + 1:mb(tb, st)]
        nm = re.search(r'definitions="([^"]+)"', rec)
        d = {"name": nm.group(1) if nm else "?"}
        for f in FIELDS:
            mm = re.search(r"^\t\t" + f + r"=(-?[\d.]+)", rec, re.M)
            d[f] = mm.group(1) if mm else None
        out.append(d)
    return {d["name"]: d for d in out}
A = nodes("VANILLA_start.eu4"); B = nodes("VANILLA2_start.eu4")
worst=[]
anydiff=set()
for f in FIELDS:
    for k in A:
        a,b = A[k][f], B[k][f]
        if a is None or b is None: continue
        af, bf = float(a), float(b)
        if af != bf:
            anydiff.add(k)
            # percent relative to VANILLA_start's (A) own value, as base
            p = 100.0*abs(af-bf)/af if af else 0.0
            worst.append((p, f, k, a, b))
worst.sort(reverse=True)
for w in worst[:10]:
    print(w)
print("nodes differing on any field:", len(anydiff), "of", len(A))
