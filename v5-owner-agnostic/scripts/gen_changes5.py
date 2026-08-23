# -*- coding: utf-8 -*-
"""Emit changes-v5.md: hand-written head + the 55 logged replacements, quoted verbatim."""
import io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v5-owner-agnostic\changes-v5.md"
head = io.open(os.path.join(HERE, "changes5_head.md"), encoding="utf-8").read()
ed = json.load(io.open(os.path.join(HERE, "edits5.json"), encoding="utf-8"))
parts = [head]
for i, e in enumerate(ed, 1):
    sec = e["section"]
    sec = "" if sec == "various" else " — §%s" % sec
    parts.append("### %d. `%s`%s\n\n%s\n\n**Removed:**\n\n```\n%s\n```\n\n**Replaced with:**\n\n```\n%s\n```\n"
                 % (i, e["id"], sec, e["clears"][0].upper() + e["clears"][1:], e["old"], e["new"]))
io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(parts))
print("wrote", OUT, os.path.getsize(OUT), "bytes,", len(ed), "entries")
