import zipfile
p = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\tutorial\eu4_tutorial_chapter10.eu4"
try:
    z = zipfile.ZipFile(p)
    print("ZIP entries:", z.namelist())
except Exception as e:
    print("not a zip:", e)
    with open(p, 'rb') as f:
        head = f.read(32)
        print(head)
