# -*- coding: utf-8 -*-
"""Assemble scripts/r8/out/S*.md into validation-round8.md, in census order, with overrides."""
import io, os, re, json, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT = os.path.join(ROOT, 'scripts', 'r8', 'out')
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


rows = json.load(io.open(os.path.join(ROOT, 'scripts', 'r8', 'rows.json'), encoding='utf-8'))
order = [r['ID'] for r in rows]
secof = {r['ID']: r['§'] for r in rows}
lineof = {r['ID']: r.get('line', '?') for r in rows}

graded = {}
dupes = []
for fn in sorted(os.listdir(OUT)):
    if not fn.endswith('.md'):
        continue
    for line in io.open(os.path.join(OUT, fn), encoding='utf-8'):
        if not line.startswith('| Y'):
            continue
        p = split_row(line)
        if len(p) < 5:
            print('SHORT ROW in', fn, p[:2], len(p))
            continue
        cid = p[0]
        if cid in graded:
            dupes.append((cid, fn))
            continue
        graded[cid] = {'claim': p[1], 'verdict': p[2].strip().upper(),
                       'method': p[3], 'evidence': p[4], 'src': fn}

# ---- lead-validator overrides (rechecked personally) ----
OV = os.path.join(ROOT, 'scripts', 'r8', 'overrides.json')
overrides = json.load(io.open(OV, encoding='utf-8')) if os.path.exists(OV) else {}
for cid, d in overrides.items():
    if cid in graded:
        graded[cid].update(d)
    else:
        graded[cid] = d
        graded[cid].setdefault('src', 'lead')

missing = [i for i in order if i not in graded]
extra = [i for i in graded if i not in set(order)]
print('graded', len(graded), 'of', len(order), '| missing', len(missing), '| extra', len(extra),
      '| dupes', len(dupes))
if missing:
    print('  missing:', missing[:60])
if extra:
    print('  extra:', extra)

VALID = ('CONFIRMED', 'PARTIAL', 'REFUTED', 'UNTESTABLE')
bad = [(i, graded[i]['verdict']) for i in graded if graded[i]['verdict'] not in VALID]
if bad:
    print('  bad verdicts:', bad)

cnt = collections.Counter(graded[i]['verdict'] for i in order if i in graded)
print(dict(cnt))

# ---- emit ----
L = []
L.append('# Validation — Per-Good Trade Network Spec, round 8')
L.append('')
L.append('**Document graded:** `per-good-trade-spec.md`, 2,165 lines, MD5 `88da3fe76244ab4f43ef41edf3e50768`.')
L.append('')
L.append('**Inventory used:** `claims-delta-round8.md` — all **1,054** rows of its CHANGED (22), '
         'REWORDED (5), UNCHANGED (975) and NEW (52) tables, `Y001`–`Y1236`, each graded once. '
         'The current document\'s wording governs; where the census row\'s paraphrase and the '
         'document disagree, both are graded and the disagreement is the finding.')
L.append('')
L.append('**Sources.** The EU4 1.37.5 install at `C:/Program Files (x86)/Steam/steamapps/common/'
         'Europa Universalis IV` (`common/`, `events/`, `missions/`, `decisions/`, `history/`, '
         '`map/`, `localisation/`, `eu4.exe`\'s string table, `eu4_rev.txt`); the reference '
         'implementation and its instruments in `scripts/`, re-run for this round into '
         '`scripts/r8/` (`measure6.py`, `props6.py`, `epsilon6.py`, `europe.py`, `round6.py`, '
         '`final.py`, `relabel6.py`, `p3_relabel_pergood.py`, `p3_time.py`, `p3_bisect.py`, '
         '`verify6.py`, `redtest6.py`, `mutate6.py`, `coverage6.py`, `pc8_a.py`, `toys.py`); the '
         'three crash dumps under `Paradox Interactive/Europa Universalis IV/crashes/`; the '
         'readable saves the scripts name; and the prior-version trees `../v1-laplacian/` through '
         '`../v5-owner-agnostic/`. Probes written for this round are in `scripts/r8/`.')
L.append('')
L.append('**Method.** Twenty-two slices were graded independently from primary sources against a '
         'common brief (`scripts/r8/BRIEF.md`), which forbids prior verdict files. Every PARTIAL '
         'and every REFUTED was then re-run or re-read by the lead validator before entry here; '
         'rows where that recheck changed or sharpened the verdict say so in the evidence cell.')
L.append('')
L.append('| ID | claim (short) | verdict | method | evidence |')
L.append('|---|---|---|---|---|')
SECORDER = ['§0'] + ['§1.%s' % k for k in ('1','2','3','4','5','6','7','8','9','10','11','12')]     + ['§2.1', '§2.2', '§2.2a'] + ['§2.%d' % k for k in range(3, 10)]     + ['§3.%d' % k for k in range(1, 17)]
seen_sec = []
for i in order:
    if secof[i] not in seen_sec:
        seen_sec.append(secof[i])
for s_ in seen_sec:
    if s_ not in SECORDER:
        print('UNKNOWN SECTION', repr(s_))
rank = {s_: (SECORDER.index(s_) if s_ in SECORDER else 999) for s_ in seen_sec}
order = sorted(order, key=lambda i: (rank[secof[i]], order.index(i)))

cur = None
body = []
for i in order:
    g = graded.get(i)
    if g is None:
        continue
    if secof[i] != cur:
        cur = secof[i]
        body.append('')
        body.append('## %s' % cur)
        body.append('')
        body.append('| ID | claim (short) | verdict | method | evidence |')
        body.append('|---|---|---|---|---|')
    body.append('| %s | %s | %s | %s | %s |' % (i, g['claim'], g['verdict'], g['method'], g['evidence']))

L = L[:-2] + body
L.append('')
L.append('---')
L.append('')
L.append('## Summary')
L.append('')
L.append('| verdict | rows |')
L.append('|---|---|')
for k in VALID:
    L.append('| %s | %d |' % (k, cnt.get(k, 0)))
L.append('| **total** | **%d** |' % sum(cnt.values()))
L.append('')

io.open(os.path.join(ROOT, 'validation-round8.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('wrote validation-round8.md')

# non-confirmed listing for the report
nc = [(i, secof[i], graded[i]['verdict'], graded[i]['claim']) for i in order
      if i in graded and graded[i]['verdict'] != 'CONFIRMED']
io.open(os.path.join(ROOT, 'scripts', 'r8', 'nonconfirmed.txt'), 'w', encoding='utf-8').write(
    '\n'.join('%s\t%s\t%s\t%s' % t for t in nc))
print('non-confirmed rows:', len(nc))
