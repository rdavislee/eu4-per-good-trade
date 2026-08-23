import re
p = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\map\default.map"
txt = open(p, encoding="utf-8", errors="replace").read()
m = re.search(r"sea_starts\s*=\s*\{([^}]*)\}", txt, re.S)
seas = set(int(x) for x in m.group(1).split()) if m else set()
members = [789, 833, 1173, 1175, 1176, 1177, 1178, 1179, 1180, 1181, 1182, 1460, 1800, 2856, 2864, 2880, 4781, 4782, 4783, 4784]
sea_members = [x for x in members if x in seas]
land_members = [x for x in members if x not in seas]
print("sea_starts total count:", len(seas))
print("cape members that are sea:", sea_members)
print("cape members that are land:", land_members, "count", len(land_members))
