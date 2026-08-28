# -*- coding: utf-8 -*-
"""Y015 / Y1052 probe: how many "figures the spec prints" under different numeric tokenisations,
and Y1002: LP column-order permutation invariance of the orientation."""
import io, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "per-good-trade-spec.md")
doc = io.open(SPEC, encoding="utf-8").read()

def strip_code(d):
    d = re.sub(r"```.*?```", " ", d, flags=re.S)
    d = re.sub(r"`[^`]*`", " ", d)
    return d

def strip_secrefs(d):
    return re.sub(r"§\s*\d+(\.\d+[a-z]?)?", " ", d)

variants = {}
base = doc
nocode = strip_code(doc)
nosec = strip_secrefs(doc)
nocodenosec = strip_secrefs(strip_code(doc))

PATS = {
  "digitruns  \d+":                        r"\d+",
  "num w/ dot  \d+(\.\d+)?":             r"\d+(?:\.\d+)?",
  "num w/ dot+comma":                       r"\d[\d,]*(?:\.\d+)?",
  "verify6 NUMPAT":                         r"[0-9][0-9.,\u2013]*[0-9]|[0-9]",
  "num+comma+dot+e+pct+x":                  r"[\u00d7x]?\d[\d,]*(?:\.\d+)?(?:e[+-]?\d+)?%?",
}
for pname, pat in PATS.items():
    for dname, d in (("full", base), ("no-code", nocode), ("no-secref", nosec),
                     ("no-code+no-secref", nocodenosec)):
        toks = re.findall(pat, d)
        variants["%s | %s" % (pname, dname)] = (len(toks), len(set(toks)))

for k in sorted(variants, key=lambda k: variants[k][0]):
    n, u = variants[k]
    print("%-46s occurrences %4d   distinct %4d" % (k, n, u))
vals = [v[0] for v in variants.values()] + [v[1] for v in variants.values()]
print("range over these tokenisations: %d .. %d" % (min(vals), max(vals)))
