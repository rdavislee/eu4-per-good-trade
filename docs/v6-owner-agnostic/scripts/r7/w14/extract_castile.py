import zipfile, os
p = r'C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\Castile1444_12_22.eu4'
z = zipfile.ZipFile(p)
print(z.namelist())
raw = z.read("gamestate").decode("latin-1")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gamestate_castile.txt")
with open(out, "w", encoding="latin-1") as f:
    f.write(raw)
print(len(raw), "chars written")
meta = z.read("meta").decode("latin-1")
print(meta[:400])
