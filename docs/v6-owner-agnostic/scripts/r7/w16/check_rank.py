# -*- coding: utf-8 -*-
"""Compare RANK vs DRAIN vs LAP vs FLOW across all 29 live goods:
   - sink counts per good (RANK vs DRAIN)
   - net-producer sinks (s>c at a sink) per operator
   - orphan sinks: a sink for good g that g cannot reach via any DIRECTED path from a producer
   - specifically: genua as a cloves sink, and whether cloves ever reaches genua
   - top-demand alignment: share of top-K demand nodes that are RANK sinks vs DRAIN sinks
   - stranded demand under RANK: total demand at nodes RANK's orientation cannot route to
     (following the RANK monotone-descending-score direction, reachability from true producers)
"""
import numpy as np, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, orient
from rankop import S0, C0, GOODS_LIVE, GIDX, rank_score
from drain import run_drain, sinks_of as drain_sinks_of
from flowop import run_all as flow_run_all, sinks_of as flow_sinks_of

goods_live = GOODS_LIVE
GI = GIDX

# ---- RANK / LAP directed graphs, per good ----
RANK = {}
for g in goods_live:
    gi = GI[g]
    sc, emp, regions, wp = rank_score(gi)
    RANK[g] = dict(score=sc, dir=orient(sc))

# ---- DRAIN, per good ----
DRAIN = {}
for g in goods_live:
    gi = GI[g]
    b = S0[gi] - C0[gi]
    r = run_drain(b)
    DRAIN[g] = r

# ---- FLOW (pure min-cost, no sweep), per good, from flowop ----
FLOWR = flow_run_all()

def sinks(directed):
    od = collections.Counter(u for u, _ in directed)
    return set(i for i in range(N) if od[i] == 0)

print("=" * 90)
print("sink counts per good: RANK vs DRAIN vs LAP vs FLOW")
print("=" * 90)
tot_rank = tot_drain = tot_lap = tot_flow = 0
ratios = []
for g in goods_live:
    rk = sinks(RANK[g]["dir"])
    dr = sinks(DRAIN[g]["directed"])
    lp = sinks(RANK[g].get("lap_dir", [])) if False else None
    fl = sinks(FLOWR[g]["flow_dir"])
    lap_dir = orient(RANK[g]["score"]*0)  # placeholder, not used
    tot_rank += len(rk); tot_drain += len(dr); tot_flow += len(fl)
    if len(dr) > 0:
        ratios.append(len(rk) / len(dr))
    print("%-16s RANK=%3d DRAIN=%3d FLOW=%3d  ratio RANK/DRAIN=%.2f" %
          (g, len(rk), len(dr), len(fl), (len(rk)/len(dr) if len(dr) else float('nan'))))

print()
print("TOTALS across %d goods: RANK=%d DRAIN=%d FLOW=%d" % (len(goods_live), tot_rank, tot_drain, tot_flow))
print("mean per-good ratio RANK/DRAIN sinks: %.2f" % (sum(ratios)/len(ratios)))
print("overall ratio (sum RANK)/(sum DRAIN): %.2f" % (tot_rank/tot_drain))

print()
print("=" * 90)
print("net-producer sinks (a sink i with s[i] > c[i]) per operator, aggregated over goods")
print("=" * 90)
def net_producer_sinks(sset, gi):
    return [i for i in sset if S0[gi][i] > C0[gi][i]]

npr_rank = npr_drain = npr_flow = npr_lap = 0
for g in goods_live:
    gi = GI[g]
    rk = sinks(RANK[g]["dir"]); dr = sinks(DRAIN[g]["directed"]); fl = sinks(FLOWR[g]["flow_dir"])
    lp = sinks(orient(FLOWR[g]["phi"]))
    npr_rank += len(net_producer_sinks(rk, gi))
    npr_drain += len(net_producer_sinks(dr, gi))
    npr_flow += len(net_producer_sinks(fl, gi))
    npr_lap += len(net_producer_sinks(lp, gi))
print("net-producer sinks total: RANK=%d DRAIN=%d FLOW=%d LAP=%d (over %d goods)" %
      (npr_rank, npr_drain, npr_flow, npr_lap, len(goods_live)))

print()
print("=" * 90)
print("orphan sinks: RANK sink for g that g's flow/reachability from producers never reaches")
print("=" * 90)
def reachable_from_producers(directed, gi):
    adj = collections.defaultdict(list)
    for u, v in directed:
        adj[u].append(v)
    producers = [i for i in range(N) if S0[gi][i] > 0]
    seen = set(producers)
    q = collections.deque(producers)
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in seen:
                seen.add(y); q.append(y)
    return seen

total_orphans = 0
orphan_examples = []
for g in goods_live:
    gi = GI[g]
    rk_dir = RANK[g]["dir"]
    rk_sinks = sinks(rk_dir)
    reach = reachable_from_producers(rk_dir, gi)
    orphans = [i for i in rk_sinks if i not in reach]
    total_orphans += len(orphans)
    if orphans:
        orphan_examples.append((g, [ORDER[i] for i in orphans]))
print("total RANK orphan sinks across all goods:", total_orphans)
for g, names in orphan_examples[:10]:
    print(" ", g, "->", names)

# specifically: cloves / genua
gi_cloves = GI.get("cloves")
if gi_cloves is not None:
    rk_dir = RANK["cloves"]["dir"]
    rk_sinks_cloves = sinks(rk_dir)
    reach_cloves = reachable_from_producers(rk_dir, gi_cloves)
    genua_i = NIDX["genua"]
    print()
    print("cloves: is genua a RANK sink?", genua_i in rk_sinks_cloves,
          "| does cloves reach genua (via RANK-directed producer BFS)?", genua_i in reach_cloves)
    print("cloves producers:", [ORDER[i] for i in range(N) if S0[gi_cloves][i] > 0])

print()
print("=" * 90)
print("top-demand alignment: share of top-K demand nodes that are sinks, RANK vs DRAIN")
print("=" * 90)
for K in (5, 8, 10):
    rank_hits = drain_hits = 0
    total = 0
    for g in goods_live:
        gi = GI[g]
        c = C0[gi]
        topk = set(np.argsort(-c)[:K])
        rk = sinks(RANK[g]["dir"]); dr = sinks(DRAIN[g]["directed"])
        rank_hits += len(topk & rk)
        drain_hits += len(topk & dr)
        total += K
    print("K=%2d : RANK matches %d/%d = %.1f%%   DRAIN matches %d/%d = %.1f%%" %
          (K, rank_hits, total, 100*rank_hits/total, drain_hits, total, 100*drain_hits/total))

print()
print("=" * 90)
print("stranded demand under RANK: total demand share at nodes RANK cannot route TO from producers")
print("(monotone score = s-c descending: check whether high-demand nodes are actually reachable)")
print("=" * 90)
strand_fracs = []
for g in goods_live:
    gi = GI[g]
    rk_dir = RANK[g]["dir"]
    reach = reachable_from_producers(rk_dir, gi)
    c = C0[gi]
    total_c = c.sum()
    unreached_c = sum(c[i] for i in range(N) if i not in reach)
    strand_fracs.append(unreached_c/total_c if total_c else 0.0)
print("mean stranded-demand share under RANK across goods: %.4f" % (sum(strand_fracs)/len(strand_fracs)))
print("max stranded-demand share:", max(strand_fracs), "min:", min(strand_fracs))
print("per-good:", dict(zip(goods_live, [round(x,4) for x in strand_fracs])))
