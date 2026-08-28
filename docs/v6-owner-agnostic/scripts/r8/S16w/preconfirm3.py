# -*- coding: utf-8 -*-
"""Independent measurement of the round-3 values (fixes-round3.md R01-R12).

Nothing here reads the specification. Every figure is computed from the install, from the
1444 save, or from the reference implementation in this directory.

Sections:
  A  R01  max base_tax over counted provinces, and total development there
  B  R02  razed-hangzhou / razed-beijing edge flips on Phi_w
  C  R03  the deleted v5.0 apparatus, reconstructed on the v6.0 province table
  D  R04  the two tax-tooltip schemas, as arithmetic
  E  R06-R12  node relabelling, on a five-phase reimplementation parameterised by node order,
              validated against drain.py on Phi_w first (the precondition fixes-round3.md sets)

Run:  python preconfirm3.py            (all sections)
      python preconfirm3.py relabel    (section E only)
"""
import os, sys, re, zipfile, collections, importlib.util
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

from solver import (N, ORDER, NIDX, EDGES_UND, ROWS, PROV, PRICES,
                    GOODS_PRODUCED_FACTOR, TAX_COEFF, ON_STARTUP_DEVASTATION)
from drain import run_drain, NODEW

SAVE = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                    "Europa Universalis IV", "save games", "VANILLA_start.eu4")
V5ABD = os.path.abspath(os.path.join(HERE, "..", "..", "v5-owner-agnostic", "scripts",
                                     "_audit_b_drain.py"))

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])


def cw(alpha=1.5, w=None):
    w = W if w is None else w
    t = (w / w.max()) ** alpha
    n = np.zeros(N); np.add.at(n, PN, t)
    return n / n.sum()


def b_w(alpha=1.5, w=None):
    return np.full(N, 1.0 / N) - cw(alpha, w)


def sinks_named(directed):
    od = collections.Counter(u for u, _ in directed)
    return sorted(ORDER[i] for i in range(N) if od[i] == 0)


# ------------------------------------------------------------------ A. R01 ---
def section_a():
    print("=" * 96); print("A.  R01  max base_tax over counted provinces"); print("=" * 96)
    counted = [r["pid"] for r in ROWS]
    print("  counted provinces (owner + in a trade node)      %d" % len(counted))
    hist = [(PROV[p]["base_tax"], p) for p in counted]
    mx = max(hist)[0]
    ties = sorted(p for bt, p in hist if bt == mx)
    print("  max base_tax, history parse                      %g at %s" % (mx, ties))
    for p in ties:
        s = PROV[p]
        print("    pid %d  base_tax %g  base_production %g  base_manpower %g  total development %g"
              % (p, s["base_tax"], s["base_production"], s.get("base_manpower", 0.0),
                 s["base_tax"] + s["base_production"] + s.get("base_manpower", 0.0)))
    dev = [(PROV[p]["base_tax"] + PROV[p]["base_production"] + PROV[p].get("base_manpower", 0.0), p)
           for p in counted]
    print("  max total development over counted               %g at pid %d"
          % (max(dev)[0], max(dev)[1]))
    # the save is the primary source; the history parse is a derived artefact
    raw = zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")

    def matchbrace(s, i):
        d = 0; k = i; inq = False
        while k < len(s):
            c = s[k]
            if c == '"': inq = not inq
            elif not inq:
                if c == "{": d += 1
                elif c == "}":
                    d -= 1
                    if d == 0: return k
            k += 1
        return len(s) - 1
    i = raw.index(chr(10) + "provinces={"); j = raw.index("{", i)
    body = raw[j + 1:matchbrace(raw, j)]
    cs = set(counted); best = []
    for m in re.finditer(r"^-(\d+)=\{", body, re.M):
        pid = int(m.group(1))
        if pid not in cs: continue
        st = body.index("{", m.start()); rec = body[st + 1:matchbrace(body, st)]

        def f(k):
            g = re.search(r"^\t\t" + k + r"=([\d.]+)", rec, re.M)
            return float(g.group(1)) if g else 0.0
        best.append((f("base_tax"), f("base_tax") + f("base_production") + f("base_manpower"), pid))
    best.sort(reverse=True)
    print("  save gamestate, counted provinces, top 4:        %s" % (best[:4],))
    print("  save gamestate, max total development:           %s"
          % (sorted(((t, p) for _, t, p in best), reverse=True)[:3],))


# ------------------------------------------------------------------ B. R02 ---
def section_b():
    print(); print("=" * 96); print("B.  R02  razed-node edge flips on Phi_w"); print("=" * 96)
    base = run_drain(b_w()); BD = set(base["directed"])
    NW = np.zeros(N); np.add.at(NW, PN, W)
    print("  baseline sinks %-42s edges %d/%d" % (sinks_named(BD), len(BD), len(EDGES_UND)))
    for node in ("hangzhou", "beijing"):
        w2 = W.copy()
        w2[[i for i, r in enumerate(ROWS) if r["node"] == node]] = 0.0
        r2 = run_drain(b_w(1.5, w2)); ND = set(r2["directed"])
        print("  zero %-9s node wealth %6.1f  sinks %-52s flips %d"
              % (node, NW[NIDX[node]], sinks_named(ND), len(BD ^ ND) // 2))


# ------------------------------------------------------------------ C. R03 ---
def section_c():
    print(); print("=" * 96); print("C.  R03  v5.0's deleted apparatus on the v6.0 field"); print("=" * 96)
    # v5-owner-agnostic/scripts/solver.py:59-73, verbatim
    LOCAL_TAX_MOD = {"gems": 0.15}
    LOCAL_TV_MOD = {"incense": 0.10}
    MON_FLAT = {8: 3.0, 684: 0.5, 1821: 0.5, 1822: 0.5, 2145: 0.5}
    MON_GPMOD = {262: 0.10}
    MON_TVMOD = {684: 0.1, 1821: 0.1, 1822: 0.1, 2145: 0.1}
    PERM_FLAT = {6: 2.0, 362: 2.0, 363: 2.0, 370: 1.0, 371: 1.0,
                 387: 3.0, 542: 4.0, 2151: 2.5, 2316: 2.0, 4316: 2.0}
    FLAT = dict(MON_FLAT); FLAT.update(PERM_FLAT)
    off = on = 0.0; touched = []; gems = incense = 0
    for r in ROWS:
        pid, g = r["pid"], r["good"]
        price = PRICES.get(g, 0.0)
        off += r["tax"] + r["prod_income"]
        gp2 = (r["gp"] + FLAT.get(pid, 0.0)) * (1.0 + MON_GPMOD.get(pid, 0.0))
        on += (TAX_COEFF * PROV[pid]["base_tax"] * (1.0 + LOCAL_TAX_MOD.get(g, 0.0))
               + gp2 * price * (1.0 + LOCAL_TV_MOD.get(g, 0.0) + MON_TVMOD.get(pid, 0.0)))
        if (g in LOCAL_TAX_MOD or g in LOCAL_TV_MOD or pid in FLAT
                or pid in MON_GPMOD or pid in MON_TVMOD):
            touched.append(pid)
        gems += (g == "gems"); incense += (g == "incense")
    print("  world wealth, apparatus off                      %.2f" % off)
    print("  world wealth, apparatus on                       %.2f" % on)
    print("  delta                                            %.2f" % (on - off))
    print("  delta as %% of the apparatus-off total            %.4f%%" % (100 * (on - off) / off))
    print("  delta as %% of the apparatus-on total             %.4f%%" % (100 * (on - off) / on))
    proj = (set(FLAT) | set(MON_GPMOD) | set(MON_TVMOD)) & set(r["pid"] for r in ROWS)
    print("  touched provinces                                %d  = %d gems + %d incense + %d project/permanent - %d overlap"
          % (len(touched), gems, incense, len(proj),
             gems + incense + len(proj) - len(touched)))


# ------------------------------------------------------------------ D. R04 ---
def section_d():
    print(); print("=" * 96); print("D.  R04  the two tooltip schemas as arithmetic"); print("=" * 96)
    def trunc2(x): return int(x * 100) / 100.0
    for bt in (6, 2):
        print("  base_tax %-2d   trunc(bt x 0.0833333) = %.2f     trunc(bt / 12) = %.2f"
              % (bt, trunc2(bt * 0.0833333), trunc2(bt / 12.0)))
    print("  multipliers m with trunc(6m)=0.49 and trunc(2m)=0.16:  m in [0.0816667, 0.0833333)")
    print("  0.0833333 in that interval: %s      1/12 = %.9f in it: %s"
          % (0.0816667 <= 0.0833333 < 1.0 / 3 / 4, 1 / 12,
             0.0816667 <= 1 / 12.0 < 0.08333333333333333))
    print("  0.49 x 1.25 = %.4f -> trunc %.2f, round %.2f ;  6 x 0.0833333.. x 1.25 = %.5f -> %.2f"
          % (0.49 * 1.25, int(0.49 * 1.25 * 100) / 100, round(0.49 * 1.25, 2),
             6 / 12 * 1.25, int(6 / 12 * 1.25 * 100) / 100))


# ------------------------------------------------------------- E. R06-R12 ---
def load_abd():
    spec = importlib.util.spec_from_file_location("abd", V5ABD)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def section_e(seeds=(4242, 7, 999, 1, 20250821), trials=100):
    print(); print("=" * 96)
    print("E.  R06-R12  node relabelling on Phi_w"); print("=" * 96)
    abd = load_abd()
    bw = b_w()
    base = run_drain(bw); BD = set(base["directed"])
    print("  drain.py    core %d  edges %d/%d  promotions %d  fallbacks %d  sinks %s"
          % (len(base["core"]), len(BD), len(EDGES_UND), len(base["promotions"]),
             len(base["fallbacks"]), sinks_named(BD)))
    r0 = abd.drain(list(ORDER), list(EDGES_UND), bw, wealth=list(NODEW))
    A0 = set(r0["directed"])
    print("  instrument  core %d  edges %d/%d  promotions %d  fallbacks %d  sinks %s"
          % (len(r0["core"]), len(A0), len(EDGES_UND), len(r0["promos"]), len(r0["fbs"]),
             sorted(ORDER[i] for i in r0["sinks"])))
    print("  VALIDATION: edges agreeing %d of %d ; orientation sets identical %s"
          % (len(BD & A0), len(EDGES_UND), BD == A0))
    if BD != A0:
        print("  instrument rejected - not proceeding"); return
    BASE_SINKS = frozenset(sinks_named(BD))

    allrows = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        changed = 0; moved = []; sameset = 0
        holds = collections.Counter(); cnt = collections.Counter()
        distinct = set(); fbs = 0
        for _ in range(trials):
            p = rng.permutation(N)
            e2 = sorted(set(tuple(sorted((int(p[u]), int(p[v])))) for u, v in EDGES_UND))
            b2 = np.zeros(N); w2 = np.zeros(N); nm = [None] * N
            for i in range(N):
                b2[p[i]] = bw[i]; w2[p[i]] = NODEW[i]; nm[p[i]] = ORDER[i]
            r = abd.drain(nm, e2, b2, wealth=list(w2))
            inv = {int(p[i]): i for i in range(N)}
            D = set((inv[u], inv[v]) for u, v in r["directed"])
            assert len(D) == len(EDGES_UND)
            sk = frozenset(ORDER[inv[i]] for i in r["sinks"])
            fbs += len(r["fbs"])
            if D != BD: changed += 1
            moved.append(len(BD ^ D) // 2)
            if sk == BASE_SINKS: sameset += 1
            for s in sk: holds[s] += 1
            cnt[len(sk)] += 1
            distinct.add(sk)
        print()
        print("  --- seed %d, %d trials ---" % (seed, trials))
        print("  R06 orientation changed                          %d/%d" % (changed, trials))
        print("  R07 mean edges moving (of 159)                   %.2f   (min %d max %d)"
              % (float(np.mean(moved)), min(moved), max(moved)))
        print("  R08 returns the baseline set %-23s %d/%d" % ("{english_channel,hangzhou}", sameset, trials))
        print("  R09 hangzhou is an end                           %d/%d" % (holds["hangzhou"], trials))
        print("  R10 english_channel is an end                    %d/%d" % (holds["english_channel"], trials))
        print("  R11 every other end holder                       %s"
              % [(k, v) for k, v in holds.most_common() if k not in ("hangzhou", "english_channel")])
        print("  R12 sink-count distribution                      %s  (range %d-%d, mode %d)"
              % (dict(sorted(cnt.items())), min(cnt), max(cnt),
                 cnt.most_common(1)[0][0]))
        print("      distinct sink sets %d ; fallbacks fired %d" % (len(distinct), fbs))
        allrows.append((seed, changed, float(np.mean(moved)), sameset, holds["hangzhou"],
                        holds["english_channel"], dict(holds), dict(cnt)))
    print()
    print("  pooled over %d seeds x %d trials = %d relabellings" % (len(seeds), trials,
                                                                    len(seeds) * trials))
    tot = collections.Counter(); tcnt = collections.Counter()
    for _, _, _, _, _, _, h, c in allrows:
        tot.update(h); tcnt.update(c)
    print("  end holders pooled  %s" % tot.most_common())
    print("  sink counts pooled  %s" % dict(sorted(tcnt.items())))
    print("  hangzhou pooled     %d/%d" % (tot["hangzhou"], len(seeds) * trials))
    print("  channel  pooled     %d/%d" % (tot["english_channel"], len(seeds) * trials))
    print("  mean edges moving pooled %.2f" % np.mean([r[2] for r in allrows]))
    print("  baseline set pooled %d/%d" % (sum(r[3] for r in allrows), len(seeds) * trials))


# --------------------------------------------------------------- F. T02/T04 ---
# the 22 European nodes the spec's own sensitivity note enumerates (1.6)
EURO_NODES = ["english_channel", "north_sea", "baltic_sea", "white_sea", "novgorod", "lubeck",
              "rheinland", "saxony", "wien", "krakow", "pest", "venice", "ragusa", "genua",
              "champagne", "bordeaux", "valencia", "sevilla", "constantinople", "crimea",
              "kiev", "kazan"]


def _relabel_runs(abd, bw, trials, seed):
    """yield (sink-name frozenset, directed-set-in-original-labels) per relabelling"""
    rng = np.random.default_rng(seed)
    for _ in range(trials):
        p = rng.permutation(N)
        e2 = sorted(set(tuple(sorted((int(p[u]), int(p[v])))) for u, v in EDGES_UND))
        b2 = np.zeros(N); w2 = np.zeros(N); nm = [None] * N
        for i in range(N):
            b2[p[i]] = bw[i]; w2[p[i]] = NODEW[i]; nm[p[i]] = ORDER[i]
        r = abd.drain(nm, e2, b2, wealth=list(w2))
        inv = {int(p[i]): i for i in range(N)}
        yield (frozenset(ORDER[inv[i]] for i in r["sinks"]),
               set((inv[u], inv[v]) for u, v in r["directed"]))


def section_f(trials=60, seed=4242):
    print(); print("=" * 96)
    print("F.  T02 the Europe table under relabelling / T04 the razed-China row under relabelling")
    print("=" * 96)
    abd = load_abd()
    import pdx
    EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
    eurp = set(int(x) for x in pdx.values(
        pdx.load(os.path.join(EU4, "map", "continent.txt")).get("europe")))
    eur = [i for i, r in enumerate(ROWS) if r["pid"] in eurp]
    print("  European counted provinces (map/continent.txt)      %d" % len(eur))
    ES = set(EURO_NODES)
    for k in (1.00, 1.02, 1.56, 2.00):
        w = W.copy(); w[eur] *= k
        bw = b_w(1.5, w)
        shipped = sinks_named(run_drain(bw)["directed"])
        holds = collections.Counter(); neur = []; nasia = []; cnt = collections.Counter()
        for sk, _ in _relabel_runs(abd, bw, trials, seed):
            for s in sk: holds[s] += 1
            neur.append(len([s for s in sk if s in ES]))
            nasia.append(len([s for s in sk if s not in ES]))
            cnt[len(sk)] += 1
        print("  x%.2f  shipped order %-46s" % (k, shipped))
        print("        %d relabellings: mean European ends %.2f, mean non-European ends %.2f, count %s"
              % (trials, float(np.mean(neur)), float(np.mean(nasia)), dict(sorted(cnt.items()))))
        print("        no non-European end in %d/%d ; end holders %s"
              % (sum(1 for x in nasia if x == 0), trials, holds.most_common(8)))
    # T04
    print()
    w2 = W.copy()
    w2[[i for i, r in enumerate(ROWS) if r["node"] == "hangzhou"]] = 0.0
    bw0 = b_w(); bwR = b_w(1.5, w2)
    base_runs = list(_relabel_runs(abd, bw0, 100, seed))
    razed_runs = list(_relabel_runs(abd, bwR, 100, seed))
    hz_base = sum(1 for sk, _ in base_runs if "hangzhou" in sk)
    hz_raz = sum(1 for sk, _ in razed_runs if "hangzhou" in sk)
    moved = sum(1 for (a, _), (b, _) in zip(base_runs, razed_runs) if a != b)
    lost = sum(1 for (a, _), (b, _) in zip(base_runs, razed_runs)
               if "hangzhou" in a and "hangzhou" not in b)
    flips = [len(da ^ db) // 2 for (_, da), (_, db) in zip(base_runs, razed_runs)]
    print("  T04, 100 relabellings, same permutation applied to both fields:")
    print("      hangzhou an end, baseline field           %d/100" % hz_base)
    print("      hangzhou an end, razed field              %d/100" % hz_raz)
    print("      sink set differs baseline vs razed        %d/100" % moved)
    print("      hangzhou held an end and then lost it     %d/100" % lost)
    print("      edge flips baseline->razed: mean %.1f min %d max %d"
          % (float(np.mean(flips)), min(flips), max(flips)))


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "a"): section_a()
    if which in ("all", "b"): section_b()
    if which in ("all", "c"): section_c()
    if which in ("all", "d"): section_d()
    if which in ("all", "relabel", "e"): section_e()
