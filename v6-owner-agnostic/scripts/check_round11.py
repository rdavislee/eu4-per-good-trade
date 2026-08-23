# -*- coding: utf-8 -*-
import io, os, re, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT = os.path.normpath(os.path.join(BASE, '..', 'docs', 'audit'))  # audit records moved here

def parse(path):
    tables = collections.OrderedDict()
    cur = None
    for ln in io.open(path, encoding='utf-8'):
        if ln.startswith('## '):
            cur = ln[3:].split(u'—')[0].strip()
            tables[cur] = []
        elif ln.startswith('| Y') and cur:
            body = re.sub(r'(?<!\\)\|$', '', re.sub(r'^\|', '', ln.strip()))
            tables[cur].append([x.strip() for x in re.split(r'(?<!\\)\|', body)])
    return tables

old = parse(os.path.join(AUDIT, 'claims-delta-round10.md'))
new = parse(os.path.join(AUDIT, 'claims-delta-round11.md'))
for k, v in new.items():
    print(k, len(v), 'cols', len(v[0]) if v else 0)

oldids = set(p[0] for t in old.values() for p in t)
newids = [p[0] for t in new.values() for p in t]
print('old ids', len(oldids), 'new ids', len(newids), 'distinct', len(set(newids)))
dupes = [i for i, c in collections.Counter(newids).items() if c > 1]
print('dupes', dupes)
print('lost (in old, not in new):', sorted(oldids - set(newids)))
print('added:', sorted(set(newids) - oldids, key=lambda x: int(x[1:])))

# every carried row keeps its claim wording
oldclaim = {}
for t in old.values():
    for p in t:
        oldclaim[p[0]] = p[2]
special = set(['Y1275','Y1158','Y1291','Y483','Y1326','Y1331','Y1341','Y1342','Y1352',
               'Y1159','Y541','Y616','Y783','Y1353'])
bad = 0
for p in new['UNCHANGED']:
    if p[2] != oldclaim[p[0]]:
        bad += 1
        print('WORDING CHANGED', p[0])
print('unchanged wording mismatches', bad)

# type preserved for unchanged rows
oldtype = {}
for name, t in old.items():
    for p in t:
        oldtype[p[0]] = p[3] if name == 'UNCHANGED' else (p[4] if name == 'NEW' else p[5])
bt = 0
for p in new['UNCHANGED']:
    if p[3] != oldtype[p[0]]:
        bt += 1
        print('TYPE CHANGED', p[0], oldtype[p[0]], '->', p[3])
print('type mismatches', bt)

# lines within document range and monotone in UNCHANGED
spec = io.open(os.path.join(BASE, 'per-good-trade-spec.md'), encoding='utf-8').read().split('\n')
n = len([l for l in spec]) - 1
prev = 0
oor = 0
for p in new['UNCHANGED']:
    L = int(p[-1])
    if L < prev:
        print('NON-MONOTONE', p[0], L, prev)
    prev = L
    if not (1 <= L <= n):
        oor += 1
        print('OUT OF RANGE', p[0], L)
print('spec lines', n, 'out of range', oor, 'max line', prev)

# vocabularies
types = collections.Counter()
for name, t in new.items():
    for p in t:
        types[p[3] if name == 'UNCHANGED' else (p[4] if name == 'NEW' else p[5])] += 1
print('types', dict(types))
