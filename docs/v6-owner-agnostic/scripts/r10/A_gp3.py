import zipfile, re, os
SG = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                  "Europa Universalis IV", "save games", "VANILLA_start.eu4")
raw = zipfile.ZipFile(SG).read("gamestate").decode("latin-1")
m = re.search(r"num_of_goods_produced=\{", raw)
i = m.start()
print("--- context before ---")
print(raw[max(0, i-1500):i+400].replace("\r", ""))
