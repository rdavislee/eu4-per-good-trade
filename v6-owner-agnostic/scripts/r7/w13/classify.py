from collections import defaultdict

BASE = {
 'grain':2.5,'wine':2.5,'wool':2.5,'cloth':3,'fish':2.5,'fur':2,'salt':3,'naval_supplies':2,
 'copper':3,'gold':0,'iron':3,'slaves':2,'ivory':4,'tea':2,'chinaware':3,'spices':3,
 'coffee':3,'cotton':3,'sugar':3,'tobacco':3,'cocoa':4,'silk':4,'tropical_wood':2,'dyes':4,
 'livestock':2,'incense':2.5,'glass':3,'gems':4,'paper':3.5,'coal':10,'cloves':8,'unknown':0,
}
TRADEABLE = [g for g in BASE if g not in ('gold','unknown')]
print('tradeable goods count:', len(TRADEABLE))

rows = []
with open('census2_full.tsv', encoding='utf-8') as f:
    f.readline()
    for line in f:
        parts = line.rstrip('\n').split('\t')
        tree,file,ln,tg,key,val = parts
        if val == 'None' or tg == 'None':
            continue
        rows.append((tg, float(val)))

min_val = defaultdict(lambda: 0.0)  # most negative single value per good (default 0 = no negative event)
has_neg = defaultdict(bool)
for tg, val in rows:
    if val < 0:
        has_neg[tg] = True
        if val < min_val[tg]:
            min_val[tg] = val

below = []
exact = []
neg_not_reach = []
none_neg = []
for g in TRADEABLE:
    base = BASE[g]
    mv = min_val[g]
    floor_price = base * (1.0 + mv)  # mv is negative or 0
    if not has_neg[g]:
        none_neg.append((g, base))
    else:
        if floor_price < 2.0 - 1e-9:
            below.append((g, base, mv, floor_price))
        elif abs(floor_price - 2.0) < 1e-9:
            exact.append((g, base, mv, floor_price))
        else:
            neg_not_reach.append((g, base, mv, floor_price))

print()
print('BELOW 2.0 (%d):' % len(below))
for g,base,mv,fp in sorted(below, key=lambda x: x[3]):
    print(f'  {g}: base={base} min_single_value={mv} floor={fp:.4f}')

print()
print('EXACT 2.0 (%d):' % len(exact))
for g,base,mv,fp in exact:
    print(f'  {g}: base={base} min_single_value={mv} floor={fp:.4f}')

print()
print('NEGATIVE BUT NOT REACHING 2.0 (%d):' % len(neg_not_reach))
for g,base,mv,fp in sorted(neg_not_reach, key=lambda x: x[3]):
    print(f'  {g}: base={base} min_single_value={mv} floor={fp:.4f}')

print()
print('NO NEGATIVE EVENT AT ALL (%d):' % len(none_neg))
for g,base in none_neg:
    print(f'  {g}: base={base}')

print()
print('Partition (below, exact, negnotreach, none):', len(below), len(exact), len(neg_not_reach), len(none_neg))
