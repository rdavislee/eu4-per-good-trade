# -*- coding: utf-8 -*-
"""Lint an agent brief for steering, before it is launched.

Practical rule 1 of memory/audit-agent-prompts-stay-broad.md says to check the prompt against the
rule the way verify6.py checks the document against the install -- asserting a prompt is clean is not
checking it. This is that check, made executable.

Usage:  python lint_brief.py <brief.txt> [--role extraction|validation|preconfirm]
Exit 1 if anything fires.
"""
import hashlib, io, os, re, sys

# Phrases that hand the agent a conclusion, a suspect, or a defect class. Each entry is
# (regex, why it is banned). Drawn from briefs actually shipped in this project.
STEER = [
    (r"\bcheck\w*\b.{0,20}\bwhether\b.{0,80}\b(complete|moved|holds|survives|is right)\b",
     "hands over the conclusion to be reached"),
    (r"\bis not a violation\b|\bdoes not count as\b|\bis not in scope for the rules\b|\bnot a violation\b",
     "defines a finding class out of existence by fiat; scope is the auditor's call"),
    (r"\bhunt\b|\blook for violations\b|\bwatch (out )?for\b|\bbe alert for\b|\bpay special attention\b",
     "points the flashlight at a named target"),
    (r"\border your work by\b|\bhardest first\b|\bwhere the risk is\b|\brisk is concentrated\b",
     "risk-orders the work, so findings cluster where the author guessed"),
    (r"\bstruck you\b|\banything that strikes\b|\bwhat did you think of\b|\byour impressions?\b",
     "invites editorialising"),
    (r"\bthe most (important|valuable|useful) (case|finding|thing)\b",
     "ranks findings in advance"),
    (r"\bmost likely to be wrong\b|\bthe riskiest\b|\bsuspect\b",
     "names suspects"),
    (r"\bI (think|believe|suspect|expect)\b|\bmy own\b.{0,30}\b(view|read|guess)\b",
     "leaks the author's position"),
    (r"\bconfirm that\b|\bverify that\b.{0,40}\bis correct\b",
     "asks for confirmation rather than a verdict"),
    (r"\bfixes-agreed\b|\bpreconfirmation\.md\b|\bmy checklist\b|\bwhat I intended\b|\bnotes on the\b",
     "passes the author's own notes on the artifact, revealing intent"),
]

# Judgment solicitation -- banned for extraction, allowed nowhere as an open invitation.
JUDGMENT = [
    (r"\bcontradict\w*\b", "cross-section evaluation is the validator's job, not extraction's"),
    (r"\bself-consisten\w+\b|\binternal consistency\b", "evaluation, not enumeration"),
    (r"\bquality\b|\bwell-(written|argued|supported)\b", "evaluation, not enumeration"),
    (r"\bunrevised\b|\blooks stale\b|\bwhich passages\b", "evaluation, not enumeration"),
    (r"\bobey\w*\b.{0,30}\brules?\b|\brule compliance\b", "evaluation, not enumeration"),
]

# Method and format vocabulary that SHOULD be present -- absence means the output will not be
# comparable to the prior inventories, or the verdict will be undefined.
REQUIRED = {
    "extraction": [(r"\bID prefix\b|\buses `?Y", "the ID prefix, or the delta chain breaks"),
                   (r"UNCHANGED", "the Status vocabulary"),
                   (r"ENGINE\b.{0,80}MODEL\b", "the Type vocabulary"),
                   (r"stipulated\b.{0,120}numerical test\b", "the Provenance vocabulary"),
                   (r"numerical test\b.{0,200}engine test\b", "the numerical/engine test distinction")],
    "validation": [(r"CONFIRMED", "the verdict vocabulary"),
                   (r"REFUTED", "the verdict vocabulary"),
                   (r"\bMethod\b", "the required Method field"),
                   (r"\bEvidence\b", "the required Evidence field"),
                   (r"re-?deriv", "re-derive rather than inherit"),
                   (r"\bplausibility\b", "never confirm on plausibility")],
    "preconfirm": [(r"\bcompute\b|\bre-?measure\b|\bre-?derive\b", "that it must measure, not opine"),
                   (r"\bprimary source\b|\binstall\b", "the primary sources to measure against")],
}

# A match inside a prohibition is not a solicitation. "Do not assess whether a claim is
# well-supported" is the instruction working, not failing. Same bug class as verify6.py's R2 check
# flagging a quoted retraction -- a pattern cannot see its own polarity.
NEGATION = re.compile(r"(do not|don't|dont|never|avoid|out of scope|not in scope|is not your|skip|leave out)",
                      re.I)

def _negated(text, start):
    return bool(NEGATION.search(text[max(0, start - 140):start]))

# A brief also carries FACTS about its target: an MD5 to freeze against and a line count. Those go
# stale exactly the way document figures do -- this brief said "about 1,700 lines" for four rounds
# while the spec grew to 1,980, because an edit meant to update it never matched and nothing checked.
# Same defect class the audit keeps finding in the document, so it gets the same treatment.
def check_targets(text):
    """Verify every md5 and line count the brief asserts against the file it names."""
    out = []
    paths = re.findall(r"`([A-Za-z]:[^`]+\.md)`", text)
    md5s  = re.findall(r"MD5 `([0-9a-f]{32})`", text)
    lines = re.findall(r"about ([\d,]+) lines", text)
    target = None
    for q in paths:
        if q.endswith("per-good-trade-spec.md") and os.path.exists(q):
            target = q; break
    if target is None:
        return ["no readable spec path found in the brief, so its md5 and line count cannot be checked"]
    raw = io.open(target, "rb").read()
    got_md5 = hashlib.md5(raw).hexdigest()
    got_lines = raw.decode("utf-8", "replace").count(chr(10)) + 1
    for h in md5s:
        if h != got_md5:
            out.append("brief states MD5 %s; the file is %s" % (h[:12], got_md5[:12]))
    for l in lines:
        n = int(l.replace(",", ""))
        if abs(n - got_lines) > max(20, got_lines * 0.02):
            out.append("brief says about %s lines; the file has %d" % (l, got_lines))
    return out


def lint(path, role):
    t = io.open(path, encoding="utf-8").read()
    low = t.lower()
    fails = []
    def scan(rules, kind):
        for pat, why in rules:
            for m in re.finditer(pat, low, re.S):
                if _negated(low, m.start()):
                    continue
                fails.append((kind, m.group(0)[:60].replace(chr(10), " "), why))
    scan(STEER, "STEERING")
    if role == "extraction":
        scan(JUDGMENT, "JUDGMENT")

    missing = []
    for pat, what in REQUIRED.get(role, []):
        # case-insensitive: a brief may open a sentence with "Re-derive" or write "CONFIRMED"
        # mid-prose. Three of this linter's own bugs have been case or polarity, so both are
        # handled explicitly rather than by hoping the pattern matches the prose style.
        if not re.search(pat, t, re.S | re.I):
            missing.append(what)
    print("=" * 92)
    print("brief: %s   role: %s   %d words" % (os.path.basename(path), role, len(t.split())))
    print("=" * 92)
    for kind, hit, why in fails:
        print("  [%s] %-42r %s" % (kind, hit, why))
    for what in missing:
        print("  [MISSING] %s" % what)
    stale = check_targets(t)
    for w in stale:
        print("  [STALE] %s" % w)
    ok = not fails and not missing and not stale
    print("  %s" % ("CLEAN - safe to launch" if ok else
                    "%d steering/judgment hits, %d required elements missing" % (len(fails), len(missing))))
    return ok

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    role = "extraction"
    if "--role" in sys.argv:
        role = sys.argv[sys.argv.index("--role") + 1]
    sys.exit(0 if lint(args[0], role) else 1)
