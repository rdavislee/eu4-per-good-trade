# -*- coding: utf-8 -*-
"""Parse claims-delta-round8.md into rows and emit slice files for validation subagents."""
import io, os, re, json, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SRC = os.path.join(ROOT, 'claims-delta-round8.md')
OUTDIR = os.path.join(ROOT, 'scripts', 'r8', 'slices')
os.makedirs(OUTDIR, exist_ok=True)

BS = chr(92)
SENT = '\x00'


def split_row(s):
    s = s.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    s = s.replace(BS + '|', SENT)
    return [p.strip().replace(SENT, BS + '|') for p in s.split('|')]


rows = []
table = None
hdr = None
for line in io.open(SRC, encoding='utf-8'):
    s = line.rstrip('\n')
    if s.startswith('## '):
        table = s[3:].split('—')[0].strip().split('(')[0].strip()
        hdr = None
        continue
    if s.startswith('| ID |'):
        hdr = split_row(s)
        continue
    if s.startswith('| Y'):
        parts = split_row(s)
        if hdr and len(hdr) == len(parts):
            d = dict(zip(hdr, parts))
        else:
            d = {'ID': parts[0], '§': parts[1] if len(parts) > 1 else '', 'BAD': 1,
                 'nhdr': len(hdr or []), 'nparts': len(parts)}
        d['_table'] = table
        d['_raw'] = s
        rows.append(d)

bad = [r for r in rows if r.get('BAD')]
print('rows', len(rows), 'distinct', len(set(r['ID'] for r in rows)), 'bad', len(bad))
for r in bad:
    print('BAD', r['ID'], r.get('nhdr'), r.get('nparts'))

cnt = collections.Counter(r['§'] for r in rows)
with io.open(os.path.join(ROOT, 'scripts', 'r8', 'seccounts.txt'), 'w', encoding='utf-8') as f:
    for k, v in cnt.items():
        f.write('%s %d\n' % (k, v))

json.dump(rows, io.open(os.path.join(ROOT, 'scripts', 'r8', 'rows.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=0)

# ---- slice plan: (name, [(section, start_idx, end_idx_exclusive) ...]) ----
bysec = collections.OrderedDict()
for r in rows:
    bysec.setdefault(r['§'], []).append(r)

S = '§'
PLAN = [
    ('S01', [(S+'0', 0, 39)]),
    ('S02', [(S+'0', 39, 78)]),
    ('S03', [(S+'1.1', 0, 37)]),
    ('S04', [(S+'1.1', 37, 74)]),
    ('S05', [(S+'1.2', 0, 6), (S+'1.3', 0, 45)]),
    ('S06', [(S+'1.3', 45, 88), (S+'1.4', 0, 5)]),
    ('S07', [(S+'1.5', 0, 20), (S+'1.6', 0, 35)]),
    ('S08', [(S+'1.6', 35, 93)]),
    ('S09', [(S+'1.7', 0, 17), (S+'1.8', 0, 15), (S+'1.9', 0, 12)]),
    ('S10', [(S+'1.10', 0, 40), (S+'1.11', 0, 4), (S+'1.12', 0, 8)]),
    ('S11', [(S+'2.1', 0, 29), (S+'2.2', 0, 31)]),
    ('S12', [(S+'2.2a', 0, 17), (S+'2.3', 0, 30)]),
    ('S13', [(S+'2.3', 30, 53), (S+'2.4', 0, 31)]),
    ('S14', [(S+'2.5', 0, 6), (S+'2.6', 0, 10), (S+'2.7', 0, 34)]),
    ('S15', [(S+'2.8', 0, 49), (S+'2.9', 0, 11)]),
    ('S16', [(S+'3.1', 0, 7), (S+'3.2', 0, 38)]),
    ('S17', [(S+'3.3', 0, 20), (S+'3.4', 0, 5), (S+'3.5', 0, 19)]),
    ('S18', [(S+'3.6', 0, 24), (S+'3.7', 0, 9), (S+'3.8', 0, 14)]),
    ('S19', [(S+'3.9', 0, 29), (S+'3.10', 0, 24)]),
    ('S20', [(S+'3.11', 0, 14), (S+'3.12', 0, 9), (S+'3.13', 0, 37)]),
    ('S21', [(S+'3.14', 0, 15), (S+'3.15', 0, 35)]),
    ('S22', [(S+'3.16', 0, 24)]),
]

seen = set()
total = 0
for name, chunks in PLAN:
    out = []
    for sec, a, b in chunks:
        sub = bysec[sec][a:b]
        assert len(sub) == b - a, (name, sec, a, b, len(bysec[sec]))
        out.extend(sub)
    lines = []
    lines.append('# Slice %s  (%d claims)\n' % (name, len(out)))
    cur = None
    for r in out:
        if r['§'] != cur:
            cur = r['§']
            lines.append('\n## %s\n' % cur)
        lines.append('- **%s** [%s, type %s, spec line %s]%s' % (
            r['ID'], r['_table'], r.get('type', '?'), r.get('line', '?'),
            ('  provenance: ' + r['provenance']) if r.get('provenance') else ''))
        lines.append('  CLAIM: %s' % r.get('claim', '(none)'))
        if r.get('old → new'):
            lines.append('  CHANGE: %s' % r['old → new'])
        if r.get('rewording'):
            lines.append('  REWORDING: %s' % r['rewording'])
        lines.append('')
        seen.add(r['ID'])
        total += 1
    io.open(os.path.join(OUTDIR, name + '.md'), 'w', encoding='utf-8').write('\n'.join(lines))
    print(name, len(out))

print('total sliced', total, 'distinct', len(seen))
missing = set(r['ID'] for r in rows) - seen
print('missing', sorted(missing))
