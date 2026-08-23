import os,sys
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); os.chdir(HERE)
import flowop
from flowop import ARCS
import measure6 as M
from solver import ORDER
print("--- shipped tie-break cost ---")
for a in (1.5,2.0):
    print("  alpha_Phi=%s sinks=%s"%(a,sorted(M.sk(M.ph(a)))))
flowop.TIE_COST = np.ones(len(ARCS))
import importlib, drain
importlib.reload(drain); import measure6
print("--- unit arc costs (v6.0's Phase 2) ---")
for a in (1.5,2.0):
    r=drain.run_drain(np.full(M.N,1.0/M.N)-M.cv(a))
    sk,_=drain.sinks_of(r["directed"])
    print("  alpha_Phi=%s sinks=%s"%(a,sorted(ORDER[i] for i in sk)))
