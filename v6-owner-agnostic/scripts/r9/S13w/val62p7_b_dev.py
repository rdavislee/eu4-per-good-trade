import os, re, sys
from collections import defaultdict
ROOT = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
HP = os.path.join(ROOT, "history", "provinces")
DATE = (1444,11,11)

def le(d):
    return d <= DATE

tok_re = re.compile(r'#.*')
date_re = re.compile(r'^\s*(\d+)\.(\d+)\.(\d+)\s*=\s*\{')

def parse_province(path):
    txt = open(path, encoding='latin-1').read()
    txt = tok_re.sub('', txt)
    # split top-level: base state + dated blocks
    lines = txt.split('\n')
    state = {'owner': None, 'bt':0.0,'bp':0.0,'bm':0.0,'city':False}
    # we process sequentially: base assignments at depth 0, dated blocks applied if date<=DATE
    i=0
    depth=0
    cur_date=None
    block_depth=0
    events=[]  # (date, list of lines)
    base_lines=[]
    buf=None
    for ln in lines:
        if buf is None:
            m=date_re.match(ln)
            if m:
                d=(int(m.group(1)),int(m.group(2)),int(m.group(3)))
                buf=[]
                cur_date=d
                block_depth=ln.count('{')-ln.count('}')
                rest = ln[ln.index('{')+1:]
                buf.append(rest)
                if block_depth<=0:
                    events.append((cur_date, '\n'.join(buf))); buf=None
                continue
            base_lines.append(ln)
        else:
            block_depth += ln.count('{')-ln.count('}')
            if block_depth<=0:
                # strip trailing }
                idx = ln.rfind('}')
                buf.append(ln[:idx])
                events.append((cur_date,'\n'.join(buf)))
                buf=None
            else:
                buf.append(ln)
    def apply(chunk):
        for m in re.finditer(r'([a-zA-Z_]+)\s*=\s*([^\s{}=]+)', chunk):
            k,v=m.group(1),m.group(2)
            if k=='owner': state['owner']=v.strip('"')
            elif k=='base_tax': state['bt']=float(v)
            elif k=='base_production': state['bp']=float(v)
            elif k=='base_manpower': state['bm']=float(v)
            elif k=='add_base_tax': state['bt']+=float(v)
            elif k=='add_base_production': state['bp']+=float(v)
            elif k=='add_base_manpower': state['bm']+=float(v)
            elif k=='is_city': state['city']= v.strip('"')=='yes'
    apply('\n'.join(base_lines))
    for d,chunk in sorted(events, key=lambda x:x[0]):
        if le(d): apply(chunk)
    return state

dev=defaultdict(float)
provstate={}
for fn in sorted(os.listdir(HP)):
    if not fn.endswith('.txt'): continue
    m=re.match(r'^(\d+)', fn)
    if not m: continue
    pid=int(m.group(1))
    st=parse_province(os.path.join(HP,fn))
    provstate[pid]=st
    if st['owner']:
        dev[st['owner']] += st['bt']+st['bp']+st['bm']

rows=sorted(dev.items(), key=lambda kv:-kv[1])
print("countries with dev >= 150 (caravan base >= 50):")
n=0
for c,d in rows:
    if d>=150: n+=1; print(f"  {c} dev={d:g} caravan={d/3:.2f}")
print("count:", n)
print()
print("next 12 below 150:")
for c,d in rows[n:n+12]:
    print(f"  {c} dev={d:g} caravan={d/3:.2f} short={100*(150-d)/150:.2f}%")
