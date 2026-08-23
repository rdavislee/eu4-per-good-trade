# -*- coding: utf-8 -*-
"""Honest coverage: how many of the figures the SPEC PRINTS would a wrong value get caught on?

`mutate6.py` plants errors only in figures `verify6.py` already checks, so its score is guaranteed
by construction and measures nothing. This finds every value `measure6.py` computes that also appears
in the spec text, corrupts each one in place, and asks whether the verifier notices. The denominator
is what the document asserts, not what the harness happens to look at.

Usage: python coverage6.py
"""
import io, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "per-good-trade-spec.md")
# D11b: this script used to IGNORE any path given on the command line and always read the constant
# above -- D2's defect again, a harness that picks its own subject. It also made a probe OF THIS
# VERY FIX read as confirmation, because the probe document was never opened.
if len(sys.argv) > 1:
    SPEC = sys.argv[1]
if not os.path.exists(SPEC):
    print("no such document: %s" % SPEC); sys.exit(2)
# D7: import rather than read the cache. verify6.py recomputes measure6.OUT in-process, so a
# stale measure6.out made the two disagree silently -- coverage targets stopped matching the
# document and the denominator shrank with no signal. Every verify6 subprocess pays for this
# import already.
sys.path.insert(0, HERE)
import measure6 as _M

spec = io.open(SPEC, encoding="utf-8").read()
figs = {}
for line in ("%s	%s" % (k, v) for k, v in _M.OUT.items()):
    if "\t" in line:
        k, v = line.rstrip("\n").split("\t", 1)
        figs[k] = v

def renderings(v):
    """the ways a computed value plausibly appears in prose"""
    out = set()
    for m in re.finditer(r"-?\d+\.?\d*", str(v)):
        x = m.group(0)
        try: f = float(x)
        except ValueError: continue
        if abs(f) < 1.0 or abs(f) > 1e7: continue
        out.add(x)
        if f == int(f):
            out.add("%d" % int(f)); out.add("{:,}".format(int(f)))
        else:
            out.add("%.1f" % f); out.add("%.2f" % f); out.add("{:,.2f}".format(f))
    return {s for s in out if len(s) >= 2}

def corrupt(s):
    """change the number without changing its shape, so the edit is legible in prose"""
    d = list(s)
    for i in range(len(d) - 1, -1, -1):
        if d[i].isdigit():
            d[i] = "7" if d[i] != "7" else "3"
            return "".join(d)
    return s

# Only mutate a rendering that occurs EXACTLY ONCE in the spec. A short string like "10" appears
# dozens of times, and corrupting the first occurrence tests some unrelated sentence -- which would
# report a MISS against a figure the harness does check. Ambiguous ones are listed, not scored.
targets, ambiguous = [], []
for key, val in figs.items():
    # Deterministic order: renderings() is a set, and equal-length candidates tied under a bare
    # len key, so WHICH rendering got mutated varied per process (the score did not, but the
    # mutated site was irreproducible). Length first, then lexical.
    cands = sorted(renderings(val), key=lambda r: (-len(r), r))
    uniq = [r for r in cands if spec.count(r) == 1]
    if uniq:
        targets.append((key, uniq[0]))
    elif any(r in spec for r in cands):
        ambiguous.append((key, next(r for r in cands if r in spec), spec.count(next(r for r in cands if r in spec))))

print("=" * 100)
print("%d computed figures; %d of them appear verbatim in the spec" % (len(figs), len(targets)))
print("=" * 100)
# Per-process temp names. These were fixed strings in the shared scripts/ directory, so two
# concurrent runs -- this script and redtest6.py, which invokes it -- overwrote each other's
# mutated document and sidecar, and both reported a denominator that was neither run's. Observed
# live: the same document scored 4 of 7, 3 of 6 and 2 of 5 depending on what else was running.
tmp = os.path.join(HERE, "_cov_%d.md" % os.getpid())
side = os.path.join(HERE, "_cov_side_%d.json" % os.getpid())


def _verify(path):
    """Run verify6 on `path`; return (stdout, {name: ok}, {name: keys})."""
    res = subprocess.run([sys.executable, os.path.join(HERE, "verify6.py"), path],
                         capture_output=True, text=True, encoding="utf-8", errors="replace",
                         env=dict(os.environ, VERIFY6_SIDECAR=side))
    rows = json.load(io.open(side, encoding="utf-8")) if os.path.exists(side) else []
    if os.path.exists(side):
        os.remove(side)
    return ((res.stdout or ""), {r["name"]: r["ok"] for r in rows},
            {r["name"]: r["keys"] for r in rows})


# D11: subtract the BASELINE. "Did the harness go red?" is the wrong question; the right one is
# "did it go red BECAUSE OF THIS MUTATION". A check that already fails on the unmutated document
# is evidence about nothing, and counting it turns every genuinely-unprotected figure from MISSED
# into NO SITE -- which are unscored. Two always-failing checks moved this score from 4 of 7 to
# 4 of 4: the coverage number would have read 100% precisely BECAUSE something else was broken.
_bout, _bok, _bkeys = _verify(SPEC)
BASE_FAILED = {n for n, ok in _bok.items() if not ok}
if BASE_FAILED:
    print("baseline: %d check(s) already fail on the unmutated document. They are excluded from"
          % len(BASE_FAILED))
    print("          attribution below -- they are evidence for and against nothing.")
    for _n in sorted(BASE_FAILED):
        print("            %s" % _n)
    print()

caught, missed, miscredit, errors = [], [], [], []
for key, r in targets:
    mutated = spec.replace(r, corrupt(r), 1)
    if mutated == spec:
        continue
    io.open(tmp, "w", encoding="utf-8", newline="\n").write(mutated)
    out, okmap, keymap = _verify(tmp)
    # D6: credit a figure only when the check that FAILED is the one guarding it. Scoring on the
    # exit code counted any non-zero as a catch -- including verify6 exiting 2 for "0 checks ran",
    # so a crashed harness would have reported perfect coverage.
    if not re.search(r"RESULT: .d+ checks, [1-9].d* failed".replace(".d", chr(92) + "d"), out):
        if "0 checks ran" in out or not out.strip():
            errors.append((key, r))
        else:
            missed.append((key, r))
    else:
        # only checks that were GREEN on the unmutated document say anything about this mutation
        newly = [n for n, ok in okmap.items() if not ok and n not in BASE_FAILED]
        if not newly:
            missed.append((key, r))
        else:
            failed_keys = {k for n in newly for k in keymap.get(n, [])}
            (caught if key in failed_keys else miscredit).append((key, r))
if os.path.exists(tmp): os.remove(tmp)

for key, r in caught: print("  [CAUGHT] %-44s (%s)" % (key[:44], r))
for key, r in missed: print("  [MISSED] %-44s (%s)" % (key[:44], r))
for key, r in miscredit: print("  [NO SITE] %-43s (%s -- the failing check guards a different figure)" % (key[:43], r))
for key, r in errors:    print("  [ERROR]  %-44s (%s -- harness did not run)" % (key[:44], r))
print()
n = len(caught) + len(missed)   # miscredits are unscored, not missed: the document does not print them
print("coverage: %d of %d uniquely-locatable spec figures are protected (%.0f%%)"
      % (len(caught), n, 100.0 * len(caught) / max(1, n)))
if ambiguous:
    print()
    print("%d further figures print a value that occurs more than once in the spec, so a single-site"
          % len(ambiguous))
    print("mutation cannot be aimed at them; they are unscored rather than assumed protected:")
    for key, r, c in ambiguous:
        print("   %-46s (%s appears %dx)" % (key[:46], r, c))
print("mutate6.py's score is not this number: it plants errors only in figures verify6 already")
print("checks, so it cannot fail. This is the denominator that matters.")
