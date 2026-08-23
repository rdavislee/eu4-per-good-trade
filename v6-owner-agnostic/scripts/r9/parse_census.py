# -*- coding: utf-8 -*-
"""Parse claims-delta-round9.md into scripts/r9/rows.json (census order)."""
import io, os, json, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SRC = os.path.join(ROOT, 'claims-delta-round9.md')
BS = chr(92)
SENT = '\x00'

def split_row(s):
    s = s.strip()
    if s.startswith('|'): s = s[1:]
    if s.endswith('|'): s = s[:-1]
    s = s.replace(BS + '|', SENT)
    return [p.strip().replace(SENT, BS + '|') for p in s.split('|')]

rows = []
table = None
hdr = None
for line in io.open(SRC, encoding='utf-8'):
    st = line.strip()
    if st.startswith('## '):
        name = st[3:].split('—')[0].strip()
        table = name.split()[0]
        hdr = None
        continue
    if not st.startswith('|'):
        continue
    parts = split_row(st)
    if all(set(p) <= set('-: ') for p in parts) and parts:
        continue
    if parts and parts[0] == 'ID':
        hdr = parts
        continue
    if hdr is None:
        continue
    if not re.match(r'^Y\d{3,4}$', parts[0] or ''):
        continue
    d = dict(zip(hdr, parts))
    d['_table'] = table
    d['_raw'] = st
    rows.append(d)

ids = [r['ID'] for r in rows]
print('rows', len(rows), 'distinct', len(set(ids)))
from collections import Counter
c = Counter(ids)
print('dupes', [k for k,v in c.items() if v>1])
print('by table', Counter(r['_table'] for r in rows))
json.dump(rows, io.open(os.path.join(ROOT,'scripts','r9','rows.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=0)
