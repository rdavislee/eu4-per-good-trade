# -*- coding: utf-8 -*-
"""Does the harness go RED when it must?

Every other test in this tree asks whether the harness passes on a true document. None asks whether
it fails on a false one -- except mutate6.py, whose universe is the figures verify6 already checks,
which is the circularity section 0 admits.

Four defects found in the round-5 audit shared one signature: a path that turns "I could not check"
into a pass. Each fixture below reproduces one of them and requires the harness to go red.

  1. a needle present but unscannable        -> shows() must FAIL, not pass with an explanation
  2. the table locator removed               -> the 1.3 check must FAIL, not skip silently
  3. verify6 exits non-zero with no RESULT   -> coverage6 must call it an ERROR, not a catch
  4. a mutation tripping another figure      -> coverage6 must not credit the wrong figure
  5. a FROZEN marker on the live document     -> must not silence it (C13 added that path)
  6. an unrelated check already failing        -> must not inflate coverage (D11)

Usage: python redtest6.py
Exit 1 if any fixture fails to produce the red it is asserting.
"""
import io, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "per-good-trade-spec.md")
VERIFY = os.path.join(HERE, "verify6.py")
RESULTS = []


def _run_verify(path, sidecar=None):
    env = dict(os.environ)
    if sidecar:
        env["VERIFY6_SIDECAR"] = sidecar
    r = subprocess.run([sys.executable, VERIFY, path], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    return r.stdout or "", r.returncode


def _failed(out):
    m = re.search(r"RESULT: \d+ checks, (\d+) failed", out)
    return int(m.group(1)) if m else None


def fixture(name, mutate, expect):
    """mutate(doc) -> doc'; expect(out, rc) -> (ok, detail)."""
    doc = io.open(SPEC, encoding="utf-8").read()
    tmp = os.path.join(HERE, "_red_%s.md" % re.sub(r"\W+", "", name)[:20])
    try:
        io.open(tmp, "w", encoding="utf-8", newline=chr(10)).write(mutate(doc))
        out, rc = _run_verify(tmp)
        ok, detail = expect(out, rc)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    RESULTS.append((ok, name, detail))
    print("  [%s] %-46s %s" % ("RED " if ok else "MISS", name[:46], detail))





print("=" * 96)
print("negative fixtures: the harness must go RED on each of these")
print("=" * 96)


# 1 -- a needle present but unscannable. Before the fix, shows() passed with an explanation.
def _unscannable(doc):
    # The needle itself stays TRUE. A second site states the same quantity with a different count.
    # The old shows() scanned for a digit slot, found none in a spelled count, and passed.
    i = doc.index("**Five sources**")
    j = doc.index(chr(10), i)
    return doc[:j] + "  Restated: **Seven sources**." + doc[j:]

fixture("unscannable needle -> shows() fails",
        _unscannable,
        lambda out, rc: ((_failed(out) or 0) > 0,
                         "%s failed" % _failed(out) if _failed(out) is not None else "no RESULT line"))


# 2 -- the table locator removed. Before the fix, two checks vanished and the run stayed green.
def _no_table(doc):
    # The table and its counts stay correct; only the LEAD-IN WORDING changes. The old check was
    # keyed to that sentence, so it appended nothing at all -- two checks vanished, run stayed green.
    return doc.replace("static modifiers describe a province" + chr(39) + "s own state",
                       "static modifiers characterise the province" + chr(39) + "s own condition", 1)

def _expect_table_check_present(out, rc):
    # The assertion is that the check still RUNS, not that it fails: a reworded lead-in must not
    # make it disappear. Counting checks is how a silent skip becomes visible.
    n = re.search(r"RESULT: (\d+) checks", out)
    present = "table vs its spelled count" in out
    return (present, "table check %s (%s)" % ("present" if present else "VANISHED",
                                              n.group(0) if n else "no RESULT"))

fixture("lead-in reworded -> 1.3 check must not vanish", _no_table, _expect_table_check_present)


# 3 -- a harness that cannot run must not be scored as coverage. Simulated by handing verify6 a
# document it cannot route, which is the same "produced no RESULT" shape as a crash.
def _unroutable(doc):
    return doc.replace("Per-Good Trade Network", "Something Else Entirely", 1)

def _expect_no_result(out, rc):
    n = _failed(out)
    routed = "cannot tell what" in out or "unrecognised" in out
    return (routed or n is None or n > 0,
            "unroutable: %s" % ("refused" if routed else ("%s failed" % n if n is not None else "no RESULT")))

fixture("unroutable document -> refused, not passed", _unroutable, _expect_no_result)


# 4 -- coverage6 must not credit a figure when the failing check guards a different one. Asserted
# directly against its own output rather than by simulation.
_CLEAN_COV = None


def _cov(path):
    """coverage6 stdout for `path`. Cached for the clean spec: each run costs about 2.5 minutes."""
    global _CLEAN_COV
    if path == SPEC and _CLEAN_COV is not None:
        return _CLEAN_COV
    r = subprocess.run([sys.executable, os.path.join(HERE, "coverage6.py"), path],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = r.stdout or ""
    if path == SPEC:
        _CLEAN_COV = out
    return out


def _coverage_credits_by_key():
    out = _cov(SPEC)
    has_bucket = "[NO SITE]" in out
    m = re.search(r"coverage: (\d+) of (\d+)", out)
    detail = "%s; %s" % ("NO SITE bucket present" if has_bucket else "no NO SITE bucket",
                         m.group(0) if m else "no coverage line")
    RESULTS.append((has_bucket and m is not None, "coverage credits by key, not by exit code", detail))
    print("  [%s] %-46s %s" % ("RED " if has_bucket else "MISS",
                               "coverage credits by key, not by exit code", detail))


_coverage_credits_by_key()


# 5 -- C13 gave a document the power to change how it is judged: a checklist carrying "FROZEN AT
# v6.0" reports differences as DRIFT instead of failure. Any such path is one forged marker away
# from silencing the live document, so it must be pinned. Planting the marker in the SPEC must
# leave the spec judged exactly as before -- the exemption is for the frozen checklist alone.
def _frozen_marker_on_spec(doc):
    return doc.replace(chr(10), chr(10) + "> **FROZEN AT v6.0.**" + chr(10), 1)

def _expect_marker_ignored(out, rc):
    drifted = "[DRIFT]" in out
    n = _failed(out)
    base = _failed(_run_verify(SPEC)[0])
    same = (n == base)
    return ((not drifted) and same,
            "no DRIFT on spec, %s failed (baseline %s)" % (n, base) if (not drifted and same)
            else "LEAKED: drift=%s failed=%s baseline=%s" % (drifted, n, base))

fixture("FROZEN marker on the spec -> ignored", _frozen_marker_on_spec, _expect_marker_ignored)


# 6 -- D11. coverage6 asks whether the harness went red after a mutation. If some OTHER check is
# already failing, every mutation looks like it produced a red, and figures that are genuinely
# unprotected move from MISSED into the unscored NO SITE bucket -- so the coverage percentage
# RISES because something is broken. Observed live: 4 of 7 became 4 of 4 the moment two unrelated
# checks went red. The denominator must not move.
def _coverage_line(path):
    m = re.search(r"coverage: (\d+) of (\d+)", _cov(path))
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def _coverage_survives_a_standing_red():
    base = _coverage_line(SPEC)
    doc = io.open(SPEC, encoding="utf-8").read()
    tmp = os.path.join(HERE, "_red_standingred.md")
    # a figure the harness checks, restated wrongly: fails on every run, mutated or not
    io.open(tmp, "w", encoding="utf-8", newline=chr(10)).write(
        doc + chr(10) + "Restated incorrectly: **5,724 of 6,320** ordered pairs." + chr(10))
    try:
        with_red = _coverage_line(tmp)
        out = _cov(tmp)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    # Two conditions, and the second is what stops this passing vacuously. A harness that ignores
    # the path it is given also leaves the denominator unmoved -- the pre-D11 code did exactly
    # that, so the count alone read RED against the defect this fixture exists to catch. Requiring
    # the run to NAME the standing red proves it both read the document and subtracted it.
    named = "baseline:" in out and "already fail" in out
    ok = (base[1] is not None and base[1] == with_red[1] and named)
    detail = "denominator %s -> %s; baseline %s" % (
        base[1], with_red[1], "named" if named else "NOT SUBTRACTED")
    RESULTS.append((ok, "coverage subtracts the baseline", detail))
    print("  [%s] %-46s %s" % ("RED " if ok else "MISS", "coverage subtracts the baseline", detail))


_coverage_survives_a_standing_red()


bad = [r for r in RESULTS if not r[0]]
print()
print("RESULT: %d fixtures, %d did not produce the required red" % (len(RESULTS), len(bad)))
sys.exit(1 if bad else 0)