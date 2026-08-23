# -*- coding: utf-8 -*-
"""Cut rows.json into ~22 slices, section-contiguous, <=55 rows each."""
import io, os, json, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
rows = json.load(io.open(os.path.join(ROOT,'scripts','r9','rows.json'), encoding='utf-8'))
SEC = '\u00a7'
# census order is table order; regroup into document order by section then line
def seckey(s):
    t = s.replace(SEC,'').strip()
    parts = t.split('.')
    a = int(parts[0])
    b = parts[1] if len(parts)>1 else ''
    # 2.2a after 2.2
    suf = ''
    num = ''
    for ch in b:
        if ch.isdigit(): num += ch
        else: suf += ch
    return (a, int(num) if num else -1, suf)
for r in rows:
    r['_sk'] = seckey(r[SEC])
    try: r['_ln'] = int(r['line'])
    except Exception: r['_ln'] = 0
rows.sort(key=lambda r:(r['_sk'], r['_ln'], r['ID']))
groups = []
for r in rows:
    if groups and groups[-1][0]==r[SEC]: groups[-1][1].append(r)
    else: groups.append([r[SEC],[r]])
MAX=55
slices=[]; cur=[]
for sec, g in groups:
    i=0
    while i < len(g):
        room = MAX - len(cur)
        if room <= 0:
            slices.append(cur); cur=[]; room=MAX
        take = g[i:i+room]
        # avoid leaving a tiny tail: if remaining after take is 1-8 and fits, extend
        cur.extend(take); i += len(take)
    if len(cur) >= 40:
        slices.append(cur); cur=[]
if cur: slices.append(cur)
# merge any slice < 15 into neighbour
out=[]
for s in slices:
    if out and len(s) < 15 and len(out[-1])+len(s) <= 62:
        out[-1].extend(s)
    else:
        out.append(s)
slices = out
os.makedirs(os.path.join(ROOT,'scripts','r9','slices'), exist_ok=True)
manifest=[]
for i,s in enumerate(slices,1):
    name = 'S%02d' % i
    secs = sorted(set(r[SEC] for r in s), key=lambda x: seckey(x))
    path = os.path.join(ROOT,'scripts','r9','slices',name+'.md')
    with io.open(path,'w',encoding='utf-8') as f:
        f.write('# Slice %s - %d claims - sections %s\n\n' % (name, len(s), ', '.join(secs)))
        cursec=None
        for r in s:
            if r[SEC]!=cursec:
                cursec=r[SEC]
                f.write('\n## %s\n\n| ID | claim | type | provenance | spec line | status |\n|---|---|---|---|---|---|\n' % cursec)
            prov = r.get('provenance','') or ('(see old->new)' if r['_table'] in ('CHANGED','REWORDED') else '')
            claim = r['claim']
            extra = r.get('old \u2192 new') or r.get('rewording') or ''
            if extra:
                claim = claim + '  <br>**' + r['_table'] + ':** ' + extra
            f.write('| %s | %s | %s | %s | %s | %s |\n' % (r['ID'], claim, r.get('type',''), prov, r['line'], r['_table']))
    manifest.append({'slice':name,'n':len(s),'sections':secs,'ids':[r['ID'] for r in s]})
json.dump(manifest, io.open(os.path.join(ROOT,'scripts','r9','manifest.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('slices', len(slices), 'total', sum(len(s) for s in slices))
for m in manifest: print(m['slice'], m['n'], ' '.join(m['sections']))
