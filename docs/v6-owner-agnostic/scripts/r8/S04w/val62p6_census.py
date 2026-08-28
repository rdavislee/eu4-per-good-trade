# -*- coding: utf-8 -*-
"""Independent textual census of change_price blocks, with quote/tooltip context."""
import os, re, sys

ROOT = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
TREES = ["events", "missions", "decisions", "common", "history"]

def strip_comment(line):
    out = []
    inq = False
    for ch in line:
        if ch == '"':
            inq = not inq
        if ch == '#' and not inq:
            break
        out.append(ch)
    return "".join(out)

hits = []
for tree in TREES:
    base = os.path.join(ROOT, tree)
    for dp, dn, fn in os.walk(base):
        for f in fn:
            if not f.lower().endswith(".txt"):
                continue
            p = os.path.join(dp, f)
            try:
                txt = open(p, "r", encoding="cp1252", errors="replace").read()
            except Exception as e:
                print("READFAIL", p, e); continue
            # walk char by char, tracking quote state and brace depth, and remembering
            # the innermost enclosing key whose value is a quoted string or a { } block
            i = 0
            inq = False
            incomment = False
            stack = []           # list of (keyname, depth) for open braces
            depth = 0
            n = len(txt)
            line = 1
            # pre-tokenise words to find the key preceding each '{'
            lastword = ""
            words = []
            while i < n:
                ch = txt[i]
                if ch == "\n":
                    line += 1
                    incomment = False
                    i += 1; continue
                if incomment:
                    i += 1; continue
                if ch == "#" and not inq:
                    incomment = True; i += 1; continue
                if ch == '"':
                    if not inq:
                        # entering quoted string: the key is lastword
                        qkey = lastword
                        qstart_line = line
                        j = i + 1
                        while j < n and txt[j] != '"':
                            if txt[j] == "\n":
                                line += 1
                            j += 1
                        body = txt[i+1:j]
                        for m in re.finditer(r"\bchange_price\b", body):
                            ln = qstart_line + body[:m.start()].count("\n")
                            hits.append(dict(tree=tree, path=p, line=ln,
                                             ctx="quoted:%s" % qkey,
                                             stack=list(s[0] for s in stack)))
                        i = j + 1
                        continue
                if ch == "{":
                    stack.append((lastword, depth)); depth += 1; lastword = ""; i += 1; continue
                if ch == "}":
                    depth -= 1
                    if stack: stack.pop()
                    lastword = ""; i += 1; continue
                if ch.isalnum() or ch in "_.-":
                    j = i
                    while j < n and (txt[j].isalnum() or txt[j] in "_.-"):
                        j += 1
                    w = txt[i:j]
                    if w == "change_price":
                        hits.append(dict(tree=tree, path=p, line=line, ctx="bare",
                                         stack=list(s[0] for s in stack)))
                    lastword = w
                    i = j
                    continue
                i += 1

print("total textual change_price occurrences: %d" % len(hits))
from collections import Counter
print("by tree:", dict(Counter(h["tree"] for h in hits)))
q = [h for h in hits if h["ctx"] != "bare"]
print()
print("QUOTED-STRING occurrences: %d" % len(q))
for h in q:
    print("   %-70s L%-7d %s  stack=%s" % (os.path.relpath(h["path"], ROOT), h["line"], h["ctx"], h["stack"][-4:]))
print()
tt = [h for h in hits if h["ctx"] == "bare" and "tooltip" in h["stack"]]
print("BARE occurrences inside a tooltip = { } wrapper: %d" % len(tt))
for h in tt:
    print("   %-70s L%-7d stack=%s" % (os.path.relpath(h["path"], ROOT), h["line"], h["stack"][-5:]))
