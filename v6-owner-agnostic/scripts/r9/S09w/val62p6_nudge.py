# -*- coding: utf-8 -*-
"""Reproduce the '29 goods x 6 random 1e-9 demand nudges' support-stability claim (S3.6)."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import drain
from solver import N, GOODS, PRICES, build_sc, EDGES_UND
from drain import phase0, phase2

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [gi for gi in range(len(GOODS)) if LIVE[gi]]
print("live goods:", len(GL))

rng = np.random.default_rng(12345)
NUDGES = 6
SCALE = 1e-9

worst_flow_moved = 0.0
support_changes = 0
total_trials = 0

for gi in GL:
    b0 = S[gi] - C[gi]
    core0, beta0, _ = phase0(b0)
    fa0, free0, net0, _ = phase2(core0, beta0)
    support0 = {}
    for ei in range(len(EDGES_UND)):
        support0[ei] = net0[ei] if ei in fa0 else 0.0
    for trial in range(NUDGES):
        noise = rng.normal(0, SCALE, size=N)
        noise -= noise.mean()
        b1 = b0 + noise
        core1, beta1, _ = phase0(b1)
        fa1, free1, net1, _ = phase2(core1, beta1)
        total_trials += 1
        for ei in range(len(EDGES_UND)):
            in0 = ei in fa0
            in1 = ei in fa1
            if in0 != in1:
                moved = abs(net1[ei] if in1 else 0.0) if not in0 else abs(net0[ei])
                support_changes += 1
                worst_flow_moved = max(worst_flow_moved, moved)

print("trials (goods x nudges):", total_trials)
print("support-membership changes:", support_changes)
print("largest |flow| on a changed edge:", worst_flow_moved)
print("any change moving > 1e-6 of flow:", worst_flow_moved > 1e-6)
