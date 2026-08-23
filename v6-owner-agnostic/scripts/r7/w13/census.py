import os, re, sys

INSTALL = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
TREES = ["events", "missions", "decisions", "common", "history"]

# match "change_price" as a bare token followed by optional whitespace and '='
TOKEN_RE = re.compile(r'\bchange_price\s*=')

results = []  # (tree, relpath, lineno, col, context_line)

for tree in TREES:
    base = os.path.join(INSTALL, tree)
    if not os.path.isdir(base):
        print("MISSING TREE", tree)
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
                print("READ ERROR", path, e)
                continue
            for m in TOKEN_RE.finditer(text):
                lineno = text.count('\n', 0, m.start()) + 1
                line_start = text.rfind('\n', 0, m.start()) + 1
                line_end = text.find('\n', m.start())
                if line_end == -1:
                    line_end = len(text)
                line = text[line_start:line_end]
                results.append((tree, rel, lineno, line.strip()))

print("TOTAL textual change_price tokens:", len(results))
from collections import Counter
c = Counter(r[0] for r in results)
for tree in TREES:
    print(f"  {tree}: {c.get(tree,0)}")

with open(os.path.join(os.path.dirname(__file__), "census_hits.tsv"), "w", encoding="utf-8") as out:
    for tree, rel, lineno, line in results:
        out.write(f"{tree}\t{rel}\t{lineno}\t{line}\n")

print("wrote census_hits.tsv with", len(results), "rows")
