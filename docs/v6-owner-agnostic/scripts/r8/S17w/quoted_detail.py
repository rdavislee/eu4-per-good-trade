import os, re, io

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"

files_positions = [
    (r"missions\DOM_Britain_Missions.txt", 19731),
    (r"missions\KoK_Byzantine_Missions.txt", 43401),
    (r"missions\KoK_Persia_Missions.txt", 83828),
    (r"missions\KoK_Persia_Missions.txt", 83946),
    (r"missions\KoK_Persia_Missions.txt", 84063),
    (r"missions\KoK_Yemen_Missions.txt", 18074),
    (r"missions\WOC_Italian_Missions.txt", 57224),
]

for rel, pos in files_positions:
    fp = os.path.join(EU4, rel)
    raw = io.open(fp, encoding="latin-1", errors="replace").read()
    body = re.sub("#[^\n]*", "", raw)
    # print a window around the change_price block (which starts somewhere after pos)
    cp_pos = body.find("change_price", pos)
    window = body[cp_pos-40:cp_pos+200]
    print("====", rel, "@raw", pos)
    print(window)
    print()
