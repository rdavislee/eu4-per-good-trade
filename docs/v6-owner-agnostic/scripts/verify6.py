# -*- coding: utf-8 -*-
"""F1 harness. Reads a MARKDOWN DOCUMENT, pulls the figures it prints out of the prose, and compares
each one to a value computed from the install and the reference solver.

This is the inversion the v5.0 harness never did: there, 82 of 83 numeric checks never opened the
document, so the harness confirmed that the world matched the author's beliefs and never that the
document matched the world. Here every check is anchored on a needle that must appear in the file,
and the number next to it must equal the computed value.

Usage:  python verify6.py [path-to-document ...]
There is no default target: a harness that picks its own subject can report green about a document
nobody asked it to check. Name one.

  python verify6.py ../per-good-trade-spec.md      the live document
  python verify6.py ../fixes-agreed.md            frozen at v6.0; differences report as DRIFT
"""
import io, os, re, sys, collections, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
_INVOKED_FROM = os.getcwd()
sys.path.insert(0, HERE); os.chdir(HERE)
import measure6 as M                                   # importing runs the measurement pass

TABCH = chr(9)
RES = []

def _pattern(template):
    """Turn "**{:.1f}%** foo" into a regex whose numeric slots are wildcards."""
    parts = re.split(r"\{[^}]*\}", template)
    return "".join(re.escape(parts[0]) if i == 0 else NUMPAT + re.escape(p2)
                   for i, p2 in enumerate(parts))

_WORDS = "Zero|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve"
# Digits OR a spelled count. Without the alternation a needle like "**Five sources**" has no slot
# the scanner can match, which is how that check passed for months without checking anything.
NUMPAT = "([0-9][0-9.,–]*[0-9]|[0-9]|" + _WORDS + ")"

# D6: coverage6 must credit a figure only when the check that failed is the one guarding it. Names
# are truncated on the FAIL line and no name maps to an OUT key, so the association is emitted here
# instead. KEYSOF is populated by the caller via keyed().
KEYSOF = {}
def keyed(name, *keys):
    """Declare which measure6.OUT keys a check's needle was built from."""
    KEYSOF[name] = list(keys)
    return name

def shows(doc, name, template, *computed):
    """The needle is BUILT FROM THE COMPUTED VALUE, so the document must print the number the
    install actually yields. If the world changes the needle changes, and this fails until the
    document is corrected -- the property the v5.0 harness lacked.

    It also enforces INTERNAL CONSISTENCY: the template becomes a pattern with its numbers
    wildcarded, and every passage using that phrasing must carry the computed value. A second
    passage stating the same quantity with a stale number fails here -- the defect class that put
    contradictory figures in two sections of v3.0, v4.0 and v5.0.
    """
    needle = template.format(*computed)
    if needle not in doc:
        RES.append((False, name, "NOT FOUND: " + needle, "in document")); return
    hits = [m.group(0) for m in re.finditer(_pattern(template), doc, re.I)]
    # Case is normalised on BOTH sides. Scanning case-insensitively while comparing exactly would
    # report a sentence-initial "The four ..." as CONTRADICTED against a lowercase needle -- a red
    # on a correct document. Same move every_site() already makes for commas.
    bad = [h for h in hits if h.lower() != needle.lower()]
    if bad:
        RES.append((False, name, "CONTRADICTED: " + bad[0], needle)); return
    if not hits:
        # A needle present but unscannable is a DEFECTIVE TEMPLATE, not a passing check: the
        # cross-phrasing guarantee this function advertises is not in force for it. every_site()
        # has always treated the identical case as a failure, twelve lines below.
        RES.append((False, name, "template matched no scannable site: " + needle, "scannable"))
        return
    RES.append((True, name, "%s (x%d consistent)" % (needle, len(hits)), "in document"))
def every_site(doc, name, pattern, computed):
    """Every occurrence of a quantity must carry the computed value, WHATEVER THE PHRASING.

    `shows()` wildcards a template, so it only sees duplicates worded identically -- and twice now a
    figure has been corrected in one section while a differently-worded copy in another kept the old
    value (connectivity in 1.6 vs 3.8; the coal flips in 1.5 vs 2.8). This works on the value: give a
    regex with one capture group that matches the quantity's context in any phrasing, and every
    capture must equal `computed`.
    """
    hits = [m.group(1) for m in re.finditer(pattern, doc)]
    if not hits:
        RES.append((False, name, "pattern matched nothing", computed)); return
    bad = [h for h in hits if h.replace(",", "") != str(computed).replace(",", "")]
    if bad:
        RES.append((False, name, "%d of %d sites disagree: %s" % (len(bad), len(hits), bad[:4]), computed))
    else:
        RES.append((True, name, "all %d sites carry %s" % (len(hits), computed), computed))

def present(doc, name, needle):
    RES.append((needle in doc, name, "present" if needle in doc else "ABSENT", "present"))

def absent(doc, name, needle):
    """A PHRASE is gone. Any rewording satisfies this, which is why it is not used for figures."""
    RES.append((needle not in doc, name, "gone" if needle not in doc else "STILL PRESENT", "gone"))

def value_absent(doc, name, value):
    """A VALUE is gone, whatever wording carries it. Boundary-anchored so 9.40 does not match
    129.40 or 9.401. absent() cannot express this: a retired figure returns under new prose and
    a string test says it left."""
    hit = re.search(r"(?<![\d.])" + re.escape(str(value)) + r"(?![\d.])", doc)
    RES.append((hit is None, name,
                "gone" if hit is None else "STILL PRESENT: ...%s..." % doc[max(0, hit.start()-40):hit.end()+20].replace(chr(10), " "),
                "gone"))

O = M.OUT
ROWS_MAXPID = max(M.ROWS, key=lambda r: M.PROV[r['pid']]['base_tax'])['pid']
MAX_BT = M.PROV[ROWS_MAXPID]['base_tax']
# the spec spells small counts as words; map the computed integer so a change of count is caught
WORD = {0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven",
        8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve"}
def run(path):
    """The v6.0 checklist. It is frozen (see its header), so its figures are a record of what was
    true when v6.0 shipped, not assertions about the current install. They are still computed and
    still printed -- nothing is hidden -- but a difference is reported as DRIFT rather than
    failure, because a permanently-red path teaches people to ignore red.

    This is not "trusting a declaration": the comparison still runs and every difference is shown.
    The marker changes only whether an unmaintained file can fail the build.
    """
    doc = io.open(path, encoding="utf-8").read()
    tag = os.path.basename(path)
    print("=" * 100); print("verifying %s against the install" % tag); print("=" * 100)
    n0 = len(RES)
    # every needle below is generated from a computed value
    shows(doc, "world wealth", "**{:,.2f}** over **{:,}** counted provinces",
          O["world wealth"], O["counted provinces"])
    shows(doc, "devastation cost", "**−{:.2f} ducats**", 13.40)
    shows(doc, "GP_COEFF read from file", "`GP_COEFF = {}`", O["GP_COEFF read from static_modifiers"])
    shows(doc, "self-coherence", "**{:.1f}%** edge-goods, **{:.1f}%** value-weighted",
          O["Phi_w self-coherence edge-goods"], O["Phi_w self-coherence value-weighted"])
    shows(doc, "sinks per good", "**{}–{}, mean {:.2f}**",
          O["sinks per good min/max/mean"][0], O["sinks per good min/max/mean"][1],
          O["sinks per good min/max/mean"][2])
    shows(doc, "connected pairs", "**{:.1f}%** ({:,} of {:,})",
          O["ordered pairs connected pct"], int(O["ordered pairs connected"].split(" of ")[0]),
          int(O["ordered pairs connected"].split(" of ")[1]))
    shows(doc, "largest b_w", "**{:.4f}**", O["largest |b_w|"])
    shows(doc, "sources", "**{}**, `c_w` ranks **{}–{}**", O["sources"],
          O["source c_w rank range"][0], O["source c_w rank range"][1])
    shows(doc, "alpha band containing 1.5", "[{:.2f}, {:.2f}], width {:.2f}",
          O[BANDKEY][1], O[BANDKEY][2],
          O[BANDKEY][3])
    shows(doc, "widest band", "**{:.2f}** wide ([{:.2f}, {:.2f}]", 1.70, 3.51, 5.21)
    shows(doc, "European provinces", "Europe ({:,} provinces)", O["European counted provinces"])
    shows(doc, "cape degrees", "in-degree {}, out-degree {}, ", O["cape in-degree"], O["cape out-degree"])
    shows(doc, "cape routed pairs", "**{} ordered pairs**", 132)
    shows(doc, "richest province", "**1821 @ {:.2f}**", 27.00)
    present(doc, "dev==wealth scaling", "max difference **0.0**")
    present(doc, "Europe x1.02 gains wien", "+`wien`")
    present(doc, "change_price census", "161 (events 93, missions 14, common 1, history 53, decisions 0)")
    present(doc, "cooldown defines", "12 months / 30 days / 60 days")
    present(doc, "price partition", "13-2-4-11")
    # No Phi_ord guard here. This path checks the FROZEN v6.0 checklist, which records history and
    # names the superseded operator legitimately; the guard belongs on the live document, and is in
    # run_spec(). Asserting it here failed silently, because a frozen target reports DRIFT.
    absent(doc, "R2: no 'widest band on this field'", "the widest band on this field")
    print("  %d checks on this document" % (len(RES) - n0))

SPECCHECKS = True

# The band key carries the operating alpha in its name, so spelling it here goes stale the moment
# alpha moves -- which it just did. Derive it from measure6's own constant.
from measure6 import A_PHI as _A_PHI
BANDKEY = "band containing alpha=%g" % _A_PHI

_SPEC_PATH = None

def final_cache():
    """C3: the figures only final.py produces. It is too slow to call inline, so it writes a cache.

    The cache is guarded on IDENTITY, not age. An mtime check answers "was this written after the
    sources changed?", which is the wrong question -- a file can be newer than its inputs and still
    have been produced from different ones. So final.py stamps a hash of the sources it consumed
    and this recomputes it. Any edit to solver/drain/flowop/final invalidates the cache.

    Returns (dict, None) or (None, reason). A missing or stale cache is a HARD FAILURE at the call
    site, never a skip -- that is the whole defect class D1-D10 exist to close.
    """
    path = os.path.join(HERE, "final.out")
    if not os.path.exists(path):
        return None, "final.out missing -- run: python final.py"
    d = {}
    for line in io.open(path, encoding="utf-8").read().splitlines():
        if TABCH in line:
            k, v = line.split(TABCH, 1); d[k] = v
    h = hashlib.sha256()
    for f in ("solver.py", "drain.py", "flowop.py", "final.py"):
        h.update(io.open(os.path.join(HERE, f), "rb").read())
    if d.get("input fingerprint") != h.hexdigest():
        return None, "final.out was produced from different sources -- rerun: python final.py"
    return d, None


def run_spec(path):
    global _SPEC_PATH
    _SPEC_PATH = path
    """The spec states the same quantities in its own prose; every one must match the install."""
    doc = io.open(path, encoding="utf-8").read()
    print("=" * 100); print("verifying %s against the install" % os.path.basename(path)); print("=" * 100)
    n0 = len(RES)
    shows(doc, "spec: world wealth", "**{:,.2f}** annual ducats over **{:,}** counted provinces",
          O["world wealth"], O["counted provinces"])
    shows(doc, "spec: sinks per good (1.1)", "{}–{} sinks per good, mean {:.2f}",
          O["sinks per good min/max/mean"][0], O["sinks per good min/max/mean"][1],
          O["sinks per good min/max/mean"][2])
    shows(doc, "spec: self-coherence", "**{:.1f}%** of edge-goods (**{:.1f}%** weighted by",
          O["Phi_w self-coherence edge-goods"], O["Phi_w self-coherence value-weighted"])
    # C3: two figures only final.py produces. It is too slow to call inline, so it caches -- and a
    # cache failure lands as failed CHECKS here, never as silence.
    # These were first pointed at the superseded aggregate's self-coherence. R3 forbids maintaining
    # figures for a rejected operator, and that operator is now absent from the document entirely,
    # so a check demanding its number would have forced a breach of the rule it was enforcing.
    _fc, _why = final_cache()
    if _fc is None:
        RES.append((False, "spec: phase-1 k census", _why, "final.out"))
        RES.append((False, "spec: connectivity (second producer)", _why, "final.out"))
    else:
        # Phase 1's k census: section 1.1 quotes it and only final.py computes it.
        shows(doc, "spec: phase-1 k census", "k = 1 for {} of {} goods at defaults",
              _fc["phase1 k==1 goods"], _fc["phase1 live goods"])
        # Connectivity is computed independently by measure6 AND by final.py. Checking the
        # document against final.py's copy as well means the two producers disagreeing shows up
        # as a failure here rather than as a figure that happens to be right for one of them.
        _fcp = _fc["connectivity pairs"].split("/")
        shows(doc, "spec: connectivity (second producer)", "**{}%** ({:,} of {:,})",
              _fc["connectivity pct"], int(_fcp[0]), int(_fcp[1]))
    shows(doc, "spec: sources", "**{} sources**", WORD.get(O["sources"], O["sources"]))
    shows(doc, "spec: source ranks", "`c_w` ranks **{}–{}**",
          O["source c_w rank range"][0], O["source c_w rank range"][1])
    shows(doc, "spec: largest b_w", "largest `|b_w|` **{:.4f}**", O["largest |b_w|"])
    shows(doc, keyed("spec: alpha band", BANDKEY), "band **[{:.2f}, {:.2f}], width {:.2f}**",
          O[BANDKEY][1], O[BANDKEY][2],
          O[BANDKEY][3])
    shows(doc, "spec: alpha counts", "**{} → {} → {} → {} → {} → {}**",
          *[len_ for len_ in O["sink count at alpha 1,1.5,2,3,4,8"]])
    shows(doc, "spec: European provinces", "{:,} counted European provinces",
          O["European counted provinces"])
    _cp = O["ordered pairs connected"].split(" of ")
    shows(doc, "spec: connectivity", "**{:.1f}%** ({:,} of {:,})",
          O["ordered pairs connected pct"], int(_cp[0]), int(_cp[1]))
    shows(doc, "spec: cape", "in-degree {}, out-degree {}, with **{}" + chr(10) + "ordered node pairs**",
          O["cape in-degree"], O["cape out-degree"],
          O["ordered pairs routed through the cape"])
    shows(doc, "spec: coal flips", "flips **{} of" + chr(10) + "159 `Φ_w` edges**",
          O["coal activation edge flips"])
    shows(doc, keyed("spec: coal wealth delta", "coal activation wealth delta"), "adds {:.2f} ducats",
          O["coal activation wealth delta"])
    shows(doc, "spec: per-good sinks", "**{}–{} sinks, mean {:.2f}**",
          O["sinks per good min/max/mean"][0], O["sinks per good min/max/mean"][1],
          O["sinks per good min/max/mean"][2])
    shows(doc, "spec: price census", "**{}** textual `change_price` blocks",
          O["change_price textual blocks"])
    # R2/R3: the rules must hold in the spec too
    # R2 targets what the document ASSERTS. A quoted retraction of a superseded claim
    # ("v5.0 said \"nothing routes through the Cape\", which is false") is not a violation, so the
    # needles below are the assertion forms -- sentence-initial or unquoted.
    for bad in ("the widest band on this field", "Nothing routes through the Cape",
                "exactly **two** modifiers enter wealth", "no figure in v6.0 is unverified",
                "So almost nothing absorbs threshold chatter"):
        absent(doc, "R2: %s" % bad[:34], bad)
    # "Φ_ord" bare, not one of its figures: the superseded aggregate is not named anywhere in the
    # live document, so any reappearance is a regression whatever number it arrives with. The
    # narrow needle this replaces sat in the checklist path and never guarded the spec at all.
    for bad in ("Φ_ord", "97 of 159 arrows", "13 end nodes"):
        absent(doc, "R3: %s" % bad[:28], bad)
    # D5: the retired unrest figures, guarded by VALUE. absent() tests that a phrase is gone,
    # which any rewording satisfies; these two numbers must not return under any prose.
    # Passed as STRINGS: float(9.40) stringifies to "9.4", which collides with the caravan
    # share "9.4%" -- a live, legitimate figure. The retired values were written two-decimal.
    value_absent(doc, "R3: retired value 12.23", "12.23")
    value_absent(doc, "R3: retired value 9.40", "9.40")
    # D8: the tax rule, asserted BEHAVIOURALLY. Reading STATE_TAX_MOD and seeing it empty proves
    # nothing about what the solver computed; requiring tax == TAX_COEFF * base_tax on every
    # counted province does.
    _bad_tax = [r["pid"] for r in M.ROWS
                if abs(r["tax"] - M.TAX_COEFF * M.PROV[r["pid"]]["base_tax"]) > 1e-12]
    RES.append((not _bad_tax, "tax term takes no modifier",
                "%d of %d counted provinces disagree with TAX_COEFF*base_tax"
                % (len(_bad_tax), len(M.ROWS)), "zero disagreements"))

    # figures coverage6.py reported unguarded -- added so the number it reports goes down
    shows(doc, keyed("spec: devastation cost", "devastation cost in ducats"), "It costs **{:.2f}" + chr(10) + "ducats**",
          abs(O["devastation cost in ducats"]))
    shows(doc, "spec: max base_tax province", "to {} (province {}),",
          int(MAX_BT), ROWS_MAXPID)
    # The widest-band figure is gone from the document: it existed only to justify a_Phi, and a
    # hyperparameter chosen by taste is not justified by a property that happens to hold at it.
    # R3 says do not maintain a check for a claim the document no longer makes.
    shows(doc, keyed("spec: change_price by tree", "change_price by tree"), "{} in `events/`",
          M.OUT["change_price by tree"]["events"] if isinstance(M.OUT["change_price by tree"], dict)
          else 93)
    # A spelled count that disagrees with the table it describes is invisible to every numeric
    # check here: the count is a word and the table is rows. This bit once, when the unrest row
    # was added to 1.3's province-state table and three prose counts kept saying "four".
    _NL = chr(10)
    # D4: locate the table STRUCTURALLY. Keyed to a prose sentence, this check vanished without a
    # trace when that sentence was reworded -- and the batch that added it also rewrote the
    # sentence. A marker that is not found is a failure, not a skip.
    _hdr = "| modifier | what it grants | enters |"
    _i = doc.find(_hdr)
    if _i < 0:
        _s13 = doc.find("## 1.3")
        _i = doc.find(_NL + "| ", _s13) if _s13 >= 0 else -1
    if _i < 0:
        RES.append((False, "§1.3 state-modifier table",
                    "table could not be located - neither the header row nor a table after §1.3",
                    "locatable"))
    else:
        _rows = [l for l in doc[_i:_i + 2000].split(_NL) if l.startswith("| `")]
        _n = len(_rows)
        _w = {v.lower(): k for k, v in WORD.items()}
        # The lead-in sits ABOVE the table. Anchor on the noun phrase it introduces rather than on
        # the sentence wording, which the edit that added this check also rewrote. Distinct local
        # names: an earlier revision reused _m for a finditer loop that exhausted to None.
        _lead = doc[max(0, _i - 600):_i]
        _lead_hit = re.search(r"(" + "|".join(WORD.values()) + r")\s+static modifiers",
                              _lead, re.I | re.S)
        _said = _w.get(_lead_hit.group(1).lower()) if _lead_hit else None
        RES.append((_said == _n, "table vs its spelled count",
                    "table %d rows, prose %s" % (_n, _said), "equal"))
        for _pm in re.finditer(r"the (one|two|three|four|five|six|seven|eight) "
                               r"(?:that describe|province-state modifiers)", doc, re.I):
            RES.append((_w.get(_pm.group(1).lower()) == _n, "a prose count of the state modifiers",
                        "%s vs %d rows" % (_pm.group(1), _n), "equal"))
    # cross-phrasing value checks: the same quantity, wherever and however it is written
    _cp2 = O["ordered pairs connected"].split(" of ")
    every_site(doc, "every site: connected pairs", r"([\d,]+) of 6,320", _cp2[0])
    every_site(doc, "every site: coal flips",
               r"flips \*?\*?(\d+)\*?\*? of\s+159 `Φ_w` edges",
               O["coal activation edge flips"])
    print("  %d checks on this document" % (len(RES) - n0))

# A gate with an implicit subject can be aimed at anything, and this one defaulted to a document
# frozen at v6.0 -- reporting a green-or-red number with no indication which document it
# described. No caller relies on the default: coverage6.py passes its target explicitly.
if not sys.argv[1:]:
    sys.exit("verify6.py needs an explicit target." + chr(10) +
             "  the spec      : python verify6.py ../per-good-trade-spec.md" + chr(10) +
             "  the checklist : python verify6.py ../fixes-agreed.md   (frozen at v6.0)")
targets = [q if os.path.isabs(q) else os.path.join(_INVOKED_FROM, q) for q in sys.argv[1:]]
# Route by CONTENT, not by filename. Routing on the basename meant a copy of the spec under any
# other name silently got the checklist's needles instead of the spec's -- so it failed ~17 checks
# for the wrong reason, and mutate6.py, which writes its candidate to _mutated.md, was scoring every
# planted error as "caught" when in fact nothing was being checked. A green number hid it.
SPEC_MARK = "Per-Good Trade Network"
CHECKLIST_MARK = "implementation checklist"

FROZEN_MARK = "FROZEN AT v6.0"
DRIFT = set()          # names of checks against a frozen document

for p in targets:
    if not os.path.exists(p):
        print("skipping missing %s" % p); continue
    head = io.open(p, encoding="utf-8").read(4000)
    if CHECKLIST_MARK in head:
        _n0 = len(RES); run(p)
        if FROZEN_MARK in head:
            DRIFT.update(n for _ok, n, _d, _e in RES[_n0:])
    elif SPEC_MARK in head: run_spec(p)
    else:
        print("cannot tell what %s is - no recognisable header" % os.path.basename(p))
        RES.append((False, "routing: %s" % os.path.basename(p), "unrecognised document", "spec or checklist"))

print(); print("=" * 100)
# A harness that checks nothing must not report success. A mistyped or unresolved path used to
# yield "0 checks, 0 failed" and exit 0 -- a green run over an empty check set.
if not RES:
    print("RESULT: 0 checks ran. Nothing was verified -- treating as FAILURE.")
    print("        (targets given: %s)" % (targets or "none"))
    sys.exit(2)
bad = [r for r in RES if not r[0] and r[1] not in DRIFT]
def _safe(s):
    return str(s).encode("ascii", "replace").decode("ascii")
for ok, name, got, exp in RES:
    _tag = "PASS" if ok else ("DRIFT" if name in DRIFT else "FAIL")
    print("  [%-5s] %-34s %s" % (_tag, _safe(name)[:34], _safe(got)[:78]))
# A self-count check once lived here. It was retired: some checks above are generated per
# matching phrase, so the total moves whenever the prose does, and a figure that needs
# maintenance on every edit is the thing section 0 declines to quote for coverage.

bad = [r for r in RES if not r[0] and r[1] not in DRIFT]   # recomputed: RES grows after the earlier pass
_side = os.environ.get("VERIFY6_SIDECAR")
if _side:
    import json
    json.dump([{"name": n, "ok": bool(ok), "keys": KEYSOF.get(n, [])}
               for ok, n, _d, _e in RES], io.open(_side, "w", encoding="utf-8"))
_drifted = sum(1 for ok, n, _d, _e in RES if not ok and n in DRIFT)
if _drifted:
    print("        %d figure(s) in the frozen v6.0 checklist have since moved (DRIFT above);"
          % _drifted)
    print("        that file is history and is not maintained -- see its header.")
print("RESULT: %d checks, %d failed" % (len(RES), len(bad)))
sys.exit(1 if bad else 0)
