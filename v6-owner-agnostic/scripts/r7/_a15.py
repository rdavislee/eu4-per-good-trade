import os,sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); os.chdir(HERE)
import measure6 as M
for a in (1.0,1.4,1.5,1.6,1.62,1.63,1.7,2.0):
    r=M.ph(a); print("alpha_Phi=%-5s sinks=%s"%(a,sorted(M.sk(r))))
