# -*- coding: utf-8 -*-
"""Assemble scripts/r9/out/S*.md into validation-round9.md, in census order, with lead overrides."""
import io, os, re, json, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT = os.path.join(ROOT, 'scripts', 'r9', 'out')
BS = chr(92)
SENT = '\x00'
SEC = '\u00a7'

def split_row(s):
    s = s.strip()
    if s.startswith('|'): s = s[1:]
    if s.endswith('|'): s = s[:-1]
    s = s.replace(BS + '|', SENT)
    return [p.strip().replace(SENT, BS + '|') for p in s.split('|')]

rows = json.load(io.open(os.path.join(ROOT, 'scripts', 'r9', 'rows.json'), encoding='utf-8'))
manifest = json.load(io.open(os.path.join(ROOT, 'scripts', 'r9', 'manifest.json'), encoding='utf-8'))
order = []
for m in manifest: order.extend(m['ids'])
byid = {r['ID']: r for r in rows}
assert len(order) == len(rows), (len(order), len(rows))

graded = {}
dupes = []
for fn in sorted(os.listdir(OUT)):
    if not fn.endswith('.md'): continue
    for line in io.open(os.path.join(OUT, fn), encoding='utf-8'):
        if not line.startswith('| Y'): continue
        p = split_row(line)
        if len(p) < 5:
            print('SHORT ROW in', fn, p[:2], len(p)); continue
        m = re.match(r'^(Y\d{3,4})', p[0])
        if not m: continue
        cid = m.group(1)
        if cid in graded:
            dupes.append((cid, fn)); continue
        graded[cid] = {'claim': p[1], 'verdict': p[2].strip().upper().strip('*').replace(' (SCOPED)','').replace(' (AS SCOPED)',''),
                       'method': p[3], 'evidence': p[4], 'src': fn}

OV = os.path.join(ROOT, 'scripts', 'r9', 'overrides.json')
overrides = json.load(io.open(OV, encoding='utf-8')) if os.path.exists(OV) else {}
for cid, d in overrides.items():
    if cid in graded: graded[cid].update(d)
    else:
        graded[cid] = dict(d); graded[cid].setdefault('src', 'lead')
    graded[cid]['src'] = 'lead'

missing = [i for i in order if i not in graded]
extra = [i for i in graded if i not in set(order)]
print('graded', len(graded), 'of', len(order), '| missing', len(missing), '| extra', extra,
      '| dupes', dupes)
if missing: print('  missing:', missing)

VOK = ('CONFIRMED', 'PARTIAL', 'REFUTED', 'UNTESTABLE')
bad = {i: graded[i]['verdict'] for i in graded if graded[i]['verdict'] not in VOK}
if bad: print('  bad verdicts:', bad)

cnt = collections.Counter(graded[i]['verdict'] for i in order if i in graded)
print(dict(cnt))

if missing or bad or dupes:
    raise SystemExit('not assembling: fix the above first')

def cut(t, n=560):
    t = t.strip()
    if len(t) <= n:
        return t
    return t[:t.rfind(' ', 0, n)] + ' ...'


def secsort(s):
    t = s.replace(SEC, '').strip().split('.')
    a = int(t[0]); b = t[1] if len(t) > 1 else ''
    num = ''.join(c for c in b if c.isdigit()); suf = ''.join(c for c in b if not c.isdigit())
    return (a, int(num) if num else -1, suf)

with io.open(os.path.join(ROOT, 'validation-round9.md'), 'w', encoding='utf-8') as f:
    f.write('# Validation — Per-Good Trade Network Spec v6.4, round 9\n\n')
    f.write('**Document under test:** `per-good-trade-spec.md`, 2,190 lines, MD5 '
            '`0989f4dc54d31514123eed24f0aae5c5`, version stamp 6.4.\n\n')
    f.write('**Census validated:** `claims-delta-round9.md` — 1,077 rows '
            '(`Y001`–`Y1259`, 182 numbers in the span unused), every row graded here, one row per ID.\n\n')
    f.write('**Method.** Each claim was graded against primary sources — the EU4 1.37.5 install at\n'
            '`C:\\Program Files (x86)\\Steam\\steamapps\\common\\Europa Universalis IV`, its shipped saves and\n'
            'crash dumps, the readable saves, the reference implementation and instruments in `scripts\\`,\n'
            'and the prior-version directories `..\\v1-laplacian\\` … `..\\v5-owner-agnostic\\`. Measured\n'
            'figures were re-produced by running the instrument; file claims were settled by opening the\n'
            'file and quoting the line; derivations were graded step by step. Fresh instrument runs for\n'
            'this round are in `scripts\\r9\\` (`measure6.out`, `props6.out`, `epsilon6.out`, `europe.out`,\n'
            '`round6.out`, `final.out`, `verify6.out`, `redtest6.out`, `coverage6.out`, `fingerprint6.out`,\n'
            '`apparatus6.out`); probes written for this round are in `scripts\\r9\\` and its slice\n'
            'working directories. Twenty-two slices were graded by subagents against\n'
            '`scripts\\r9\\BRIEF.md`; **every PARTIAL and every REFUTED below was independently re-run or\n'
            're-read by the lead validator**, as were all 42 rows the round-9 delta touched (the 18\n'
            'CHANGED, the 1 REWORDED and the 23 NEW).\n\n')
    f.write('**Verdicts.** CONFIRMED = reproduced or verified as scoped. PARTIAL = part holds, part\n'
            'fails, or the claim outruns its evidence. REFUTED = the sources contradict it as scoped.\n'
            'UNTESTABLE = unsettleable with these materials; the row says what would settle it.\n\n---\n\n')
    cur = None
    for cid in sorted(order, key=lambda i: (secsort(byid[i][SEC]),
                                            int(byid[i]['line']) if str(byid[i]['line']).isdigit() else 0,
                                            i)):
        r = byid[cid]; g = graded[cid]
        if r[SEC] != cur:
            cur = r[SEC]
            f.write('\n## %s\n\n| ID | claim | verdict | method | evidence |\n|---|---|---|---|---|\n' % cur)
        f.write('| %s | %s | **%s** | %s | %s |\n' % (cid, g['claim'], g['verdict'], g['method'], g['evidence']))
    f.write('\n---\n\n## Summary\n\n| verdict | rows |\n|---|---|\n')
    for v in VOK:
        f.write('| %s | %d |\n' % (v, cnt.get(v, 0)))
    f.write('| **total** | **%d** |\n\n' % sum(cnt.values()))
    nonconf = [i for i in order if graded[i]['verdict'] != 'CONFIRMED']
    f.write('**Non-CONFIRMED rows: %d.**\n\n' % len(nonconf))
    for v in ('REFUTED', 'PARTIAL', 'UNTESTABLE'):
        ids = [i for i in sorted(nonconf, key=lambda i: (secsort(byid[i][SEC]), i)) if graded[i]['verdict'] == v]
        if not ids: continue
        f.write('### %s (%d)\n\n' % (v, len(ids)))
        for i in ids:
            f.write('- **%s** (%s) — %s\n' % (i, byid[i][SEC], cut(graded[i]['evidence'])))
        f.write('\n')
print('wrote validation-round9.md')
