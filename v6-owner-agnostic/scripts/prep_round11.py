# -*- coding: utf-8 -*-
"""Build the old->new line map from round11.diff and the carried-row set."""
import re, json, io, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT = os.path.normpath(os.path.join(BASE, '..', 'docs', 'audit'))  # audit records moved here
diff = io.open(os.path.join(AUDIT, 'round11.diff'), encoding='utf-8').read().split('\n')
old = io.open(os.path.join(AUDIT, 'per-good-trade-spec-v6.5-round11-frozen.md'), encoding='utf-8').read().split('\n')
new = io.open(os.path.join(BASE, 'per-good-trade-spec.md'), encoding='utf-8').read().split('\n')

hunks = []
i = 0
while i < len(diff):
    m = re.match(r'^@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@', diff[i])
    if m:
        os_, ol, ns, nl = int(m.group(1)), int(m.group(2) or 1), int(m.group(3)), int(m.group(4) or 1)
        body = []
        j = i + 1
        while j < len(diff) and not diff[j].startswith('@@'):
            body.append(diff[j])
            j += 1
        hunks.append((os_, ol, ns, nl, body))
        i = j
    else:
        i += 1

mapping = {}
oldptr = newptr = 1
mismatch = 0
for os_, ol, ns, nl, body in hunks:
    while oldptr < os_:
        mapping[oldptr] = newptr
        if old[oldptr - 1] != new[newptr - 1]:
            mismatch += 1
        oldptr += 1; newptr += 1
    for line in body:
        if line.startswith(' '):
            mapping[oldptr] = newptr
            if old[oldptr - 1] != new[newptr - 1]:
                mismatch += 1
            oldptr += 1; newptr += 1
        elif line.startswith('-'):
            mapping[oldptr] = None
            oldptr += 1
        elif line.startswith('+'):
            newptr += 1
while oldptr <= len(old):
    mapping[oldptr] = newptr
    if oldptr <= len(old) and newptr <= len(new) and old[oldptr - 1] != new[newptr - 1]:
        mismatch += 1
    oldptr += 1; newptr += 1
print('hunks', len(hunks), 'mismatches', mismatch,
      'deleted', len([k for k, v in mapping.items() if v is None]))

rows = []
cur = None
for ln in io.open(os.path.join(AUDIT, 'claims-delta-round10.md'), encoding='utf-8'):
    if ln.startswith('## '):
        cur = ln[3:].split(u'—')[0].strip()
    elif ln.startswith('| Y') and cur:
        body = ln.strip()
        body = re.sub(r'^\|', '', body)
        body = re.sub(r'(?<!\\)\|$', '', body)
        p = [x.strip() for x in re.split(r'(?<!\\)\|', body)]
        rows.append([cur, p])

rank = {'UNCHANGED': 0, 'CHANGED': 1, 'REWORDED': 2, 'NEW': 3}
recs = []
for i, (t, p) in enumerate(rows):
    typ = p[3] if t == 'UNCHANGED' else (p[4] if t == 'NEW' else p[5])
    recs.append(dict(id=p[0], sec=p[1], claim=p[2], typ=typ, old=int(p[-1]), src=t, idx=i))

manual = {'Y637': 1734, 'Y1158': 852, 'Y1159': 854, 'Y376': 855, 'Y483': 1319, 'Y541': 1516,
          'Y576': 1551, 'Y1286': 854, 'Y1291': 960, 'Y1315': 1319, 'Y1316': 1319, 'Y1317': 1319,
          'Y1318': 1319, 'Y1328': 1551, 'Y1329': 1551, 'Y1330': 1551, 'Y1331': 1551, 'Y1332': 1551,
          'Y1333': 1551, 'Y1341': 1734, 'Y1342': 1736, 'Y1351': 2216, 'Y1352': 2218, 'Y1353': None,
          'Y1354': 2221}
changed_line = {'Y1275': 820, 'Y1326': 1503, 'Y616': 1693, 'Y783': 2190}
for r in recs:
    if r['id'] in manual:
        r['new'] = manual[r['id']]
    else:
        v = mapping.get(r['old'])
        assert v is not None, r
        r['new'] = v
    if r['id'] in changed_line:
        r['new'] = changed_line[r['id']]

special = set(['Y1275', 'Y1158', 'Y1291', 'Y483', 'Y1326', 'Y1331', 'Y1341', 'Y1342', 'Y1352',
               'Y1159', 'Y541', 'Y616', 'Y783', 'Y1353'])
unch = [r for r in recs if r['id'] not in special]
unch.sort(key=lambda r: (r['new'], rank[r['src']], r['idx']))
prev = 0
for r in unch:
    assert r['new'] >= prev
    prev = r['new']
json.dump(unch, io.open(os.path.join(BASE, 'unch.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('carried unchanged', len(unch), 'total prior rows', len(recs))
