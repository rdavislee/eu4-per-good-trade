import subprocess, re, sys
seeds = [0,1,2,3,4,5,606,607,2023,2024,2025,1000,2000,3000,42,100,200,300,400,500,606]
results = {}
for s in seeds:
    out = subprocess.run(["python","p3_relabel_seed.py",str(s)], capture_output=True, text=True).stdout
    fo = re.search(r"first-order only, LP_OPTS\s+per-good:\s*(\d+) of 290", out)
    fd = re.search(r"full cost, HiGHS default tol\s+per-good:\s*(\d+) of 290", out)
    results[s] = (int(fo.group(1)) if fo else None, int(fd.group(1)) if fd else None)
    print(s, results[s])
