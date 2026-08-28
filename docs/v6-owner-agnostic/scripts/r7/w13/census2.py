import os, re, sys
from collections import Counter

INSTALL = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
TREES = ["events", "missions", "decisions", "common", "history"]

TOKEN_RE = re.compile(r'\bchange_price\s*=\s*\{')

def find_block(text, brace_open_pos):
    # brace_open_pos points at '{'
    depth = 1
    j = brace_open_pos + 1
    n = len(text)
    while depth > 0 and j < n:
        if text[j] == '{':
            depth += 1
        elif text[j] == '}':
            depth -= 1
        j += 1
    return text[brace_open_pos:j]

records = []  # dict per hit

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
                print("READ ERROR", path, e)
                continue
            for m in TOKEN_RE.finditer(text):
                brace_pos = m.end() - 1
                lineno = text.count('\n', 0, m.start()) + 1
                block = find_block(text, brace_pos)
                tg = re.search(r'trade_goods\s*=\s*(\S+)', block)
                key = re.search(r'\bkey\s*=\s*(\S+)', block)
                val = re.search(r'\bvalue\s*=\s*(-?[0-9.]+)', block)
                records.append({
                    'tree': tree, 'file': rel, 'line': lineno,
                    'trade_goods': tg.group(1) if tg else None,
                    'key': key.group(1) if key else None,
                    'value': float(val.group(1)) if val else None,
                })

print("total blocks matched with { }:", len(records))
c = Counter(r['tree'] for r in records)
for tree in TREES:
    print(f"  {tree}: {c.get(tree,0)}")

# history negatives
hist = [r for r in records if r['tree']=='history']
neg_hist = [r for r in hist if r['value'] is not None and r['value'] < 0]
print("history total:", len(hist), "negative:", len(neg_hist))
files_neg = Counter(r['file'] for r in neg_hist)
print("negative history blocks by file:")
for f,n in files_neg.items():
    print(" ", f, n)

# any history block missing value?
missing_val_hist = [r for r in hist if r['value'] is None]
print("history blocks w/ no parsed value:", len(missing_val_hist))
for r in missing_val_hist:
    print("  ", r)

with open("census2_full.tsv", "w", encoding="utf-8") as out:
    out.write("tree\tfile\tline\ttrade_goods\tkey\tvalue\n")
    for r in records:
        out.write(f"{r['tree']}\t{r['file']}\t{r['line']}\t{r['trade_goods']}\t{r['key']}\t{r['value']}\n")
print("wrote census2_full.tsv")
