import os, re
from collections import Counter

INSTALL = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
TREES = ["events", "missions", "decisions", "common", "history"]

TOKEN_RE = re.compile(r'\bchange_price\s*=\s*\{')

def in_string_flags(text):
    """Return a boolean array: for each char index, whether it is inside a double-quoted string."""
    flags = bytearray(len(text))
    in_str = False
    for i, ch in enumerate(text):
        flags[i] = 1 if in_str else 0
        if ch == '"':
            in_str = not in_str
    return flags

records = []

for tree in TREES:
    base = os.path.join(INSTALL, tree)
    if not os.path.isdir(base):
        continue
    for root, dirs, files in os.walk(base):
        for fn in files:
            if not fn.lower().endswith('.txt'):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, INSTALL)
            try:
                with open(path, encoding='cp1252', errors='replace') as f:
                    text = f.read()
            except Exception as e:
                continue
            hits = list(TOKEN_RE.finditer(text))
            if not hits:
                continue
            flags = in_string_flags(text)
            for m in hits:
                pos = m.start()
                lineno = text.count('\n', 0, pos) + 1
                inside_quote = bool(flags[pos])
                # find nearest enclosing key= "..." context by looking backward for the last unmatched quote-opening line context
                # grab some context: 200 chars before
                ctx_start = max(0, pos-400)
                ctx = text[ctx_start:pos]
                records.append({
                    'tree': tree, 'file': rel, 'line': lineno,
                    'inside_quote': inside_quote,
                    'pos': pos,
                })

print("total:", len(records))
inside = [r for r in records if r['inside_quote']]
print("inside a double-quoted string:", len(inside))
for r in inside:
    print(" ", r['tree'], r['file'], r['line'])
