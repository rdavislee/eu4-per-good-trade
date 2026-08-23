# -*- coding: utf-8 -*-
"""Is every `(measure6.py)` attribution in the spec earned?

The v6 audit found two figures citing a script that never computed them. A citation the reader
cannot follow is worse than no citation, so this checks each one: for every sentence that names
`measure6.py`, is there a labelled figure in `measure6.out` whose value actually appears nearby?

This is a SCREEN, not a verdict. It flags every number in an attributed sentence that no computed
figure produces, which catches stale figures but also flags stipulated constants (alpha_Phi = 1.5),
tolerances (1.8e-15) and some dates. Triage the flags; do not treat the count as a score. Its value
is the specific hits, and on v6.0 those were two: a stale coal figure and a province count.

Usage: python audit_attrib.py
"""
import io, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "per-good-trade-spec.md")
OUTF = os.path.join(HERE, "measure6.out")
if not os.path.exists(OUTF):
    sys.exit("measure6.out missing - run measure6.py first")

spec = io.open(SPEC, encoding="utf-8").read()
figs = {}
for line in io.open(OUTF, encoding="utf-8"):
    if "\t" in line:
        k, v = line.rstrip("\n").split("\t", 1)
        figs[k] = v

SECTION = re.compile(r"§\s*\d+(?:\.\d+)?[a-z]?")     # cross-references, not figures
YEAR    = re.compile(r"1[0-9]{3}")                      # 1444, 1550 ... dates, not figures
ORD     = re.compile(r"\d+(?:st|nd|rd|th)")             # 3rd, 12th

def numbers(s, strip_refs=True):
    """Every number in a string, normalised so 10,607.40 and 10607.4 compare equal. Section
    cross-references, years and ordinals are not figures and are removed first -- counting them
    made every attribution look earned by coincidence."""
    if strip_refs:
        s = ORD.sub(" ", YEAR.sub(" ", SECTION.sub(" ", s)))
    out = set()
    for m in re.finditer(r"-?\d[\d,]*\.?\d*", s):
        try: out.add(round(float(m.group(0).replace(",", "")), 4))
        except ValueError: pass
    return out

computed = set()
for v in figs.values(): computed |= numbers(v)

print("=" * 100)
print("%d labelled figures in measure6.out; %d distinct computed values" % (len(figs), len(computed)))
print("=" * 100)
bad = 0
# a sentence is the window: from the previous blank line or period to the next
for m in re.finditer(r"`measure6\.py`", spec):
    lo = max(spec.rfind("\n\n", 0, m.start()), spec.rfind(". ", 0, m.start() - 1))
    hi = spec.find("\n\n", m.end())
    ctx = " ".join(spec[max(0, lo):hi if hi > 0 else len(spec)].split())
    line = spec[:m.start()].count("\n") + 1
    got = numbers(ctx)
    matched = sorted(got & computed)
    unmatched = sorted(n for n in got if n not in computed and abs(n) >= 1.0)
    ok = bool(matched) and not unmatched
    if not ok: bad += 1
    def _s(x): return str(x).encode("ascii", "replace").decode("ascii")
    print("  [%s] line %-5d %s" % ("EARNED " if ok else "FLAGGED", line, _s(ctx)[:92]))
    if matched: print("            computed: %s" % matched[:6])
    if unmatched: print("            NOT computed anywhere: %s" % unmatched[:6])
print()
print("attributions checked: %d | unearned: %d" % (len(re.findall(r"`measure6\.py`", spec)), bad))
sys.exit(1 if bad else 0)
