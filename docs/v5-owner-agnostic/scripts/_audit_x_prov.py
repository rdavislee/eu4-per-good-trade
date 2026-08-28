"""Independent 1444.11.11 province-state builder, straight from history/provinces."""
import os, sys, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _audit_x_pdx as P

EU4 = r'C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV'
START = (1444, 11, 11)
DATE = re.compile(r'^(\d{1,4})\.(\d{1,2})\.(\d{1,2})$')

SCALARS = {'owner','controller','base_tax','base_production','base_manpower','trade_goods',
           'is_city','center_of_trade','religion','culture','capital','hre','discovered_by',
           'native_size','native_ferocity','native_hostileness','citysize','unrest',
           'fort_15th','revolt_risk','seat_in_parliament','extra_cost'}

def build():
    d = os.path.join(EU4, 'history', 'provinces')
    out = {}
    for fn in os.listdir(d):
        m = re.match(r'^(\d+)\s*[-–]', fn)
        if not m:
            m = re.match(r'^(\d+)', fn)
            if not m: continue
        pid = int(m.group(1))
        b = P.parse_file(os.path.join(d, fn))
        st = {'pid': pid, 'file': fn, 'perm_mods': [], 'ptms': [], 'buildings': {},
              'add_prov_mods': [], 'great_projects': []}
        # undated first
        def apply(blk, dated):
            for k, v in blk:
                if k is None: continue
                if DATE.match(k or ''): continue
                if k == 'add_permanent_province_modifier' and isinstance(v, P.Blk):
                    st['perm_mods'].append((v.get('name'), dated))
                elif k == 'remove_province_modifier':
                    st['perm_mods'] = [x for x in st['perm_mods'] if x[0] != v]
                elif k == 'add_province_triggered_modifier':
                    st['ptms'].append((v, dated))
                elif k == 'add_province_modifier' and isinstance(v, P.Blk):
                    st['add_prov_mods'].append((v.get('name'), dated))
                elif k == 'add_great_project':
                    st['great_projects'].append(v)
                elif isinstance(v, P.Blk):
                    continue
                else:
                    st[k] = v
                    if k not in SCALARS and v in ('yes','no'):
                        st['buildings'][k] = v
        apply(b, None)
        dated = []
        for k, v in b:
            mm = DATE.match(k or '')
            if mm and isinstance(v, P.Blk):
                dt = (int(mm.group(1)), int(mm.group(2)), int(mm.group(3)))
                dated.append((dt, v))
        dated.sort(key=lambda x: x[0])
        for dt, v in dated:
            if dt <= START:
                apply(v, dt)
        out[pid] = st
    return out

if __name__ == '__main__':
    P_ = build()
    print('province history files parsed:', len(P_))
    owned = [p for p in P_.values() if p.get('owner') and p.get('is_city') == 'yes']
    print('owned & is_city=yes:', len(owned))
    print('with owner (any):', len([p for p in P_.values() if p.get('owner')]))
    print('is_city=yes (any):', len([p for p in P_.values() if p.get('is_city')=='yes']))
