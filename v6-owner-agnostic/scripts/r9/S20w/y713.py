import json, collections
PROV = {int(k): v for k, v in json.load(open("prov1444.json")).items()}
dev = collections.Counter()
for pid, s in PROV.items():
    owner = s.get("owner")
    if not owner:
        continue
    dev[owner] += (s.get("base_tax") or 0) + (s.get("base_production") or 0) + (s.get("base_manpower") or 0)

CARAVAN_FACTOR = 3.0
CAP = 50.0
rows = []
for tag, d in dev.items():
    raw = d / CARAVAN_FACTOR
    pct_of_cap = raw / CAP
    rows.append((tag, d, raw, pct_of_cap))
rows.sort(key=lambda r: -r[3])

at_cap = [r for r in rows if r[2] >= CAP]
print("countries with raw dev/3 >= 50 (at cap from dev alone):", len(at_cap))
for r in at_cap:
    print("  %s dev=%.1f raw=%.2f pct_of_cap=%.3f" % r)

print()
print("next 10 below cap (closest approach):")
below = [r for r in rows if r[2] < CAP]
for r in below[:10]:
    shortfall_pct = 1 - r[3]
    print("  %s dev=%.1f raw=%.2f pct_of_cap=%.3f shortfall_pct=%.3f" % (r[0], r[1], r[2], r[3], shortfall_pct))

print()
for tag in ("BUR", "KOR", "TIM", "POR"):
    if tag in dev:
        d = dev[tag]
        raw = d / CARAVAN_FACTOR
        print(tag, "dev=%.2f raw=%.3f pct_of_cap=%.4f shortfall_pct=%.4f" % (d, raw, raw/CAP, 1-raw/CAP))
    else:
        print(tag, "NOT FOUND in owner tags")
