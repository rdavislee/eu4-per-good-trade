# -*- coding: utf-8 -*-
"""Paragraph-level diff statistics for changes-v5.md."""
import io, json, os, re, difflib, hashlib
V4 = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v4-owner-agnostic\per-good-trade-spec.md"
V5 = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v5-owner-agnostic\per-good-trade-spec.md"
a = io.open(V4, encoding="utf-8").read(); b = io.open(V5, encoding="utf-8").read()
print("v4 bytes/lines:", len(a.encode("utf-8")), a.count("\n")+1)
print("v5 bytes/lines:", len(b.encode("utf-8")), b.count("\n")+1)
pa = [p for p in a.split("\n\n")]; pb = [p for p in b.split("\n\n")]
sm = difflib.SequenceMatcher(None, pa, pb, autojunk=False)
rep = ins = dele = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "replace": rep += 1
    elif tag == "insert": ins += 1
    elif tag == "delete": dele += 1
print("paragraph groups: replaced=%d inserted=%d deleted=%d" % (rep, ins, dele))
ha = [l for l in a.split("\n") if l.startswith("#")]
hb = [l for l in b.split("\n") if l.startswith("#")]
print("headings v4/v5:", len(ha), len(hb), "identical:", ha == hb)
if ha != hb:
    for l in difflib.unified_diff(ha, hb, lineterm="", n=0):
        if l[:1] in "+-" and l[:3] not in ("+++", "---"): print("   ", l)
ed = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "edits5.json"), encoding="utf-8"))
print("edits logged:", len(ed))
import collections
print("by section:", dict(collections.Counter(e["section"] for e in ed)))
# The real integrity check is a replay: v4 + the 57 edits, in order, must reproduce v5 byte for byte.
# (A per-edit "is this 'new' still verbatim in v5" test would false-alarm wherever a later edit
# overlapped an earlier one's replacement text, which happens four times.)
t = a
for i, e in enumerate(ed, 1):
    assert e["old"] in t, "REPLAY: anchor %d (%s) not found" % (i, e["id"])
    assert t.count(e["old"]) == 1, "REPLAY: anchor %d (%s) matches %d times" % (i, e["id"], t.count(e["old"]))
    t = t.replace(e["old"], e["new"], 1)
print("replay reproduces v5 byte for byte:", t == b)
assert t == b
