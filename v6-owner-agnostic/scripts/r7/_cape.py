import os,sys,collections,itertools
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import N, ORDER, NIDX
import measure6 as M
r = M.ph()          # aggregate Phi_w drain result
d = r["dirs"] if isinstance(r,dict) and "dirs" in r else None
print(type(r), list(r.keys())[:20] if isinstance(r,dict) else '')
