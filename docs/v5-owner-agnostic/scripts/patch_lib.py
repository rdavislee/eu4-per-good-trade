# -*- coding: utf-8 -*-
"""Auditable spec patcher: every edit is an asserted old->new replacement, logged for changes-v4.md."""
import io, json, os, sys
SPEC = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v5-owner-agnostic\per-good-trade-spec.md"
LOG  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "edits5.json")

def load():
    return io.open(SPEC, encoding="utf-8").read()

def save(t):
    io.open(SPEC, "w", encoding="utf-8", newline="\n").write(t)

def apply(edits):
    """edits: list of dicts {id, clears, section, old, new}"""
    t = load()
    done = []
    for e in edits:
        assert e["old"] in t, "ANCHOR NOT FOUND for %s (%s):\n%r" % (e["id"], e["section"], e["old"][:160])
        assert t.count(e["old"]) == 1, "ANCHOR NOT UNIQUE for %s: %d hits" % (e["id"], t.count(e["old"]))
        t = t.replace(e["old"], e["new"], 1)
        done.append(e)
    save(t)
    prev = []
    if os.path.exists(LOG):
        prev = json.load(io.open(LOG, encoding="utf-8"))
    json.dump(prev + done, io.open(LOG, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("applied %d edits (%d total logged)" % (len(done), len(prev) + len(done)))
