import zipfile, os
p = r'C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\VANILLA_start.eu4'
z = zipfile.ZipFile(p)
raw = z.read("gamestate").decode("latin-1")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gamestate.txt")
with open(out, "w", encoding="latin-1") as f:
    f.write(raw)
print(len(raw), "chars written to", out)
print("pull_power occurrences:", raw.count("pull_power"))
