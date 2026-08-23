import os, re

INSTALL = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
TREES = ["events", "missions", "decisions", "common", "history"]

TOKEN_RE = re.compile(r'\bchange_price\s*=\s*\{')
KEY_BEFORE_BRACE_RE = re.compile(r'([A-Za-z_][A-Za-z0-9_.]*)\s*=\s*\{\s*$')

def in_string_flags(text):
    flags = bytearray(len(text))
    in_str = False
    for i, ch in enumerate(text):
        flags[i] = 1 if in_str else 0
        if ch == '"':
            in_str = not in_str
    return flags

def immediate_parent_key(text, hit_pos):
    """Scan backward from hit_pos, balancing braces, to find the enclosing '{' and
    the key token immediately preceding it."""
    depth = 0
    i = hit_pos - 1
    n = len(text)
    while i >= 0:
        c = text[i]
        if c == '}':
            depth += 1
        elif c == '{':
            if depth == 0:
                # this is the enclosing open brace; find the key before it
                # text[:i+1] ends right after '{'
                before = text[:i+1]
                m = KEY_BEFORE_BRACE_RE.search(before)
                if m:
                    return m.group(1), i
                else:
                    return None, i
            else:
                depth -= 1
        i -= 1
    return None, -1

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
            except Exception:
                continue
            hits = list(TOKEN_RE.finditer(text))
            if not hits:
                continue
            flags = in_string_flags(text)
            for m in hits:
                pos = m.start()
                lineno = text.count('\n', 0, pos) + 1
                inside_quote = bool(flags[pos])
                parent_key, parent_pos = immediate_parent_key(text, pos)
                records.append({
                    'tree': tree, 'file': rel, 'line': lineno,
                    'inside_quote': inside_quote,
                    'parent_key': parent_key,
                })

print("total:", len(records))
not_quoted = [r for r in records if not r['inside_quote']]
print("not inside quotes:", len(not_quoted))

from collections import Counter
pk_counts = Counter(r['parent_key'] for r in not_quoted)
print("immediate parent key distribution among non-quoted hits:")
for k,v in pk_counts.most_common(30):
    print(" ", k, v)

# specifically look for tooltip wrapper
tooltip_wrapped = [r for r in not_quoted if r['parent_key'] == 'tooltip']
print()
print("non-quoted hits whose immediate parent key is 'tooltip':", len(tooltip_wrapped))
for r in tooltip_wrapped:
    print(" ", r['tree'], r['file'], r['line'])
