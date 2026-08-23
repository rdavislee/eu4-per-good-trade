import re

def parse_blocks(fname):
    txt = open(fname, encoding='utf-8').read()
    # find country tag blocks: 2-3 uppercase/digit tag = { ... } at top indent level (single tab)
    pattern = re.compile(r'\n\t\t([A-Z][A-Z0-9]{1,2})=\{\n((?:[^{}]|\{[^{}]*\})*?)\n\t\t\}')
    results = []
    for m in pattern.finditer(txt):
        tag = m.group(1)
        body = m.group(2)
        fields = {}
        for line in body.splitlines():
            line = line.strip()
            mm = re.match(r'([a-z_]+)=([\-0-9.a-zA-Z"]+)', line)
            if mm:
                fields[mm.group(1)] = mm.group(2)
        results.append((tag, fields))
    return results

import sys
fname = sys.argv[1]
res = parse_blocks(fname)
print("total country blocks found:", len(res))
for tag, f in res:
    print(tag, f)
