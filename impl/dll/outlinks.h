// PER-OUTGOING-LINK VALUES (spec 1.12 "the value flowing in each direction along it"; test B3).
//
// The node window's outgoing tooltip does NOT read the incoming records we write. It calls
// 0xB56480, which walks the node's DEFINITION outgoing list and, for the i-th entry, reads the
// i-th int32 of a separate array hanging off the node:
//
//   00B564CF  mov  r13, [rcx+0xA8]        ; the node's definition
//   00B564D6  mov  rbx, [r13+0x98]        ; its outgoing entry list, stride 0x78
//   00B5650B  mov  rax, [rbx+0x30]        ; entry -> target definition
//   00B56513  movsxd rcx, [rax+0xDC]      ; target's province id -> target CTradeNode
//   00B5653C  mov  ecx, r9d               ; i = the entry's ORDINAL
//   00B5653F  mov  rax, [r8+0x88]         ; node+0x88 = per-outgoing-link value array
//   00B5654D  movsxd rdx, [rax+rcx*4]     ; value[i]   (int32 x1000)
//
// Two consequences. The per-destination figures are stale unless we write this array -- which is
// why `alexandria` showed "Outgoing -19.44" beside "=> venice: 0.00". And because the array is
// indexed by ordinal with NO bounds check, re-orienting the definition graph so that a node gains
// outgoing links while this array stays short reads past its end: an access violation at
// 0xB5654D, observed live.
#pragma once
#include <fstream>
#include <string>
#include <vector>
#include <functional>
#include <map>
#include <set>
#include <windows.h>
#include "livetrade.h"
#include "alledges.h"

namespace outlinks {

inline std::string g_log_inc;
inline int g_bail_empty=0, g_bail_big=0, g_bail_tmpl=0, g_bail_alloc=0,
           g_skip_same=0, g_rebuilt=0, g_nodes_seen=0;

constexpr int NODE_OUT_VALUES = 0x88;      // int32* begin
constexpr int NODE_OUT_VALUES_END = 0x90;  // int32* end

inline int count_of(uintptr_t node) {
    uintptr_t b = livetrade::rq(node + NODE_OUT_VALUES);
    uintptr_t e = livetrade::rq(node + NODE_OUT_VALUES_END);
    if (!b || e <= b || (e - b) > 4 * 512) return 0;
    return (int)((e - b) / 4);
}

// how many outgoing entries the DEFINITION currently declares
// public alias so other modules can resolve a definition to its node
inline uintptr_t node_of_def_pub(uintptr_t def) { return alledges::node_of_def(def); }

inline int def_out_count(uintptr_t node) {
    uintptr_t def = livetrade::fq(node + 0xA8);
    if (!def || !livetrade::validate_region(def + 0x98, 16)) return -1;
    uintptr_t b = livetrade::fq(def + 0x98), e = livetrade::fq(def + 0xA0);
    if (!b || e < b || (e - b) > 0x78 * 64) return -1;
    return (int)((e - b) / 0x78);
}

// Report every node whose value array is SHORTER than its declared outgoing list. Any such node
// is a live crash waiting for the tooltip or the value pass to walk it.
inline void audit(const std::string& logpath, const std::vector<livetrade::SimNode>& sim) {
    std::ofstream lg(logpath, std::ios::app);
    int bad = 0, checked = 0;
    for (auto& s : sim) {
        int dn = def_out_count(s.obj);
        if (dn < 0) continue;
        int vn = count_of(s.obj);
        checked++;
        if (vn < dn) {
            bad++;
            if (bad <= 8)
                lg << "   [outlinks] " << s.name << ": definition declares " << dn
                   << " outgoing but the value array holds " << vn << "\n";
        }
    }
    lg << "  [outlinks] " << bad << " of " << checked
       << " nodes have a value array SHORTER than their outgoing list (must be 0)" << "\n";
}


// --- the fix ---------------------------------------------------------------------------------
// Give the array exactly one slot per declared outgoing entry, and fill each slot with the value
// the model actually sends that way. Storage comes from the ENGINE's own allocator (0x1A332D4,
// the `operator new` the node window uses at 0x13D563B) so that if the engine ever frees the
// vector it is freeing a legitimate heap block rather than DLL static memory.
using FnNew = void* (__fastcall*)(size_t);
constexpr uintptr_t ENGINE_NEW = 0x1A332D4;

inline int32_t* resize(uintptr_t node, int n) {
    uintptr_t b = livetrade::rq(node + NODE_OUT_VALUES);
    int have = count_of(node);
    // "Long enough" is not enough. 0xB5654D and 0x13FC24D both read element [count] -- ONE PAST
    // THE END -- because they search for a reverse edge a DAG does not have and fall through with
    // index == count. An engine-owned buffer sized EXACTLY to the link count therefore faults on a
    // read the engine performs routinely. Only a buffer WE allocated is known to carry slack, so
    // reallocate anything else, even when its length already matches.
    static std::set<uintptr_t> ours;
    if (b && have >= n && ours.count(b)) return (int32_t*)b;
    if (n <= 0 || n > 64) return nullptr;
    // OVER-ALLOCATE. The engine reads ONE PAST THE END of this array as a matter of course:
    // 0x13FC1CD..0x13FC24D linear-searches the TARGET node's outgoing list for an entry pointing
    // back at the source (a reverse edge). The graph is a DAG, so that entry usually does NOT
    // exist, the search falls through with index == count, and 0x13FC24D reads element [count]
    // unguarded. On stock data that lands on adjacent heap and is silently tolerated. An
    // exactly-sized buffer turns it into an access violation -- which is precisely the crash that
    // appeared when this resize was introduced. SLACK entries keep the read in bounds.
    constexpr int SLACK = 8;
    auto alloc = (FnNew)(livetrade::module_base() + ENGINE_NEW);
    int32_t* buf = (int32_t*)alloc((size_t)(n + SLACK) * 4);
    if (!buf) return nullptr;
    for (int i = 0; i < n + SLACK; i++)
        buf[i] = (i < n && i < have && b) ? ((const int32_t*)b)[i] : 0;
    DWORD old = 0;
    if (!VirtualProtect((void*)(node + NODE_OUT_VALUES), 24, PAGE_READWRITE, &old)) return nullptr;
    *(uintptr_t*)(node + NODE_OUT_VALUES)     = (uintptr_t)buf;
    *(uintptr_t*)(node + NODE_OUT_VALUES_END) = (uintptr_t)(buf + n);
    ours.insert((uintptr_t)buf);
    // NOT +0x98: it was assumed to be the vector's capacity but never verified, and writing it
    // corrupted the node struct -- the node window's incoming/outgoing tooltips stopped
    // responding entirely. Leave it alone until it is identified.
    VirtualProtect((void*)(node + NODE_OUT_VALUES), 24, old, &old);
    return buf;
}

// Resolve the i-th outgoing entry of `node` to the CTradeNode it points at, exactly as 0xB56480
// does: entry+0x30 -> target definition, +0xDC -> its province, province+0xE8 -> the node.
inline uintptr_t out_target(uintptr_t node, int i) {
    uintptr_t def = livetrade::fq(node + 0xA8);
    if (!def) return 0;
    uintptr_t b = livetrade::fq(def + 0x98);
    if (!b) return 0;
    uintptr_t entry = b + (uintptr_t)i * 0x78;
    if (!livetrade::validate_region(entry + 0x30, 8)) return 0;
    uintptr_t tdef = livetrade::fq(entry + 0x30);
    if (!tdef || !livetrade::validate_region(tdef + 0xDC, 4)) return 0;
    int pid = livetrade::fi(tdef + 0xDC);
    uintptr_t g = livetrade::game_singleton();
    if (!g || pid < 0) return 0;
    uintptr_t provs = livetrade::rq(g + 0x1CA8);
    if (!provs) return 0;
    uintptr_t prov = provs + (uintptr_t)pid * 0x2E10;
    if (!livetrade::validate_region(prov + 0xE8, 8)) return 0;
    return livetrade::fq(prov + 0xE8);
}

// Write Sigma_g flow(n -> m) into the slot for every outgoing link of every node, so the node
// window's per-destination breakdown is the model's own away-flow and reconciles with the
// outgoing total. `gross` is the annual directed flow, field-indexed.

// defined below; declared here because install() drives it
inline int rebuild_incoming(uintptr_t node,
                            const std::map<std::pair<int,int>, double>& gross,
                            int self_f,
                            const std::function<int(uintptr_t)>& field_of_node);


// One node's per-edge OUTGOING figures, written into the slot array the map panels read
// (trade_route_branch/branch_income indexes node+0x88 by the link's ordinal). RAW model units --
// no scaling. With the node's `outgoing` written as the model's own conserved sum, the panels and
// the window are consistent by construction rather than by fitting one to the other.
inline int write_slots(uintptr_t node,
                       const std::map<std::pair<int, int>, double>& gross,
                       int self_f,
                       const std::function<int(uintptr_t)>& field_of_node) {
    int n = def_out_count(node);
    if (n <= 0) return 0;
    int32_t* buf = resize(node, n);
    if (!buf) return 0;
    for (int i = 0; i < n; i++) {
        double v = 0.0;
        int dst_f = field_of_node(out_target(node, i));
        if (self_f >= 0 && dst_f >= 0) {
            auto it = gross.find({self_f, dst_f});
            if (it != gross.end() && it->second > 0) v = it->second / 12.0;
        }
        buf[i] = (int32_t)(v * 1000.0 + 0.5);
    }
    return n;
}

// PHASE A -- run BEFORE install_aggregate.
//
// Give every incident link an incoming record carrying its toward-flow, so a node lists BOTH
// directions of every link it touches. This MUST happen before the aggregate write: the whole
// non-negativity guarantee is that outgoing is a function of what the node holds
// (out = (local + Sigma incoming) x forwarded_fraction, clamped). Rebuilding the records
// afterwards changes Sigma incoming out from under an `outgoing` already derived from the old
// value, and total = local + Sigma incoming - outgoing then goes negative -- which is exactly how
// the negatives appeared, twice.
inline int install_incoming(const std::vector<livetrade::SimNode>& sim,
                            const std::vector<std::string>& field_names,
                            const std::map<std::pair<int, int>, double>& gross,
                            const std::map<int, std::string>& id_to_name) {
    std::map<std::string, int> fidx;
    for (int i = 0; i < (int)field_names.size(); i++) fidx[field_names[i]] = i;
    auto field_of_node = [&](uintptr_t nd) -> int {
        if (!nd || !livetrade::validate_region(nd + 0x120, 4)) return -1;
        auto n = id_to_name.find(livetrade::fi(nd + 0x120));
        if (n == id_to_name.end()) return -1;
        auto f = fidx.find(n->second);
        return f == fidx.end() ? -1 : f->second;
    };
    int done = 0;
    g_bail_empty=g_bail_big=g_bail_tmpl=g_bail_alloc=g_skip_same=g_rebuilt=g_nodes_seen=0;
    for (auto& s : sim) {
        int self_f = field_of_node(s.obj);
        if (self_f < 0) continue;
        if (rebuild_incoming(s.obj, gross, self_f, field_of_node) > 0) done++;
    }
    if (!g_log_inc.empty()) {
        std::ofstream lg(g_log_inc, std::ios::app);
        lg << "  [incoming] seen=" << g_nodes_seen << " rebuilt=" << g_rebuilt
           << " unchanged=" << g_skip_same << " bail(empty=" << g_bail_empty
           << " big=" << g_bail_big << " tmpl=" << g_bail_tmpl
           << " alloc=" << g_bail_alloc << ")" << "\n";;
    }
    return done;
}

inline int install(const std::vector<livetrade::SimNode>& sim,
                   const std::vector<std::string>& field_names,
                   const std::map<std::pair<int, int>, double>& gross,
                   const std::map<int, std::string>& id_to_name) {
    std::map<std::string, int> fidx;
    for (int i = 0; i < (int)field_names.size(); i++) fidx[field_names[i]] = i;
    auto field_of_node = [&](uintptr_t nd) -> int {
        if (!nd || !livetrade::validate_region(nd + 0x120, 4)) return -1;
        auto n = id_to_name.find(livetrade::fi(nd + 0x120));
        if (n == id_to_name.end()) return -1;
        auto f = fidx.find(n->second);
        return f == fidx.end() ? -1 : f->second;
    };
    int wrote = 0;
    for (auto& s : sim) {
        int n = def_out_count(s.obj);
        if (n <= 0) continue;
        int32_t* buf = resize(s.obj, n);
        if (!buf) continue;
        int src_f = field_of_node(s.obj);
        // A live node the model does not own would otherwise get raw_sum == 0 and be given an even
        // 1/n split, destroying the engine's own steering distribution. resize() above is still
        // wanted (it is the crash fix); only the share write is skipped.
        if (src_f < 0) continue;

        // Pass 1: the model's raw away-flow on each drawn link, and their total.
        std::vector<double> raw((size_t)n, 0.0);
        double raw_sum = 0.0;
        for (int i = 0; i < n; i++) {
            int dst_f = field_of_node(out_target(s.obj, i));
            if (src_f >= 0 && dst_f >= 0) {
                auto it = gross.find({src_f, dst_f});
                if (it != gross.end() && it->second > 0) raw[i] = it->second / 12.0;
            }
            raw_sum += raw[i];
        }

        // Pass 2: SCALE them to sum to the node's own outgoing figure.
        //
        // The map panels (trade_route_branch / branch_income) read these slots and the node window
        // reads +0xBC, so writing raw model units here put "11" on the north_sea ->
        // english_channel panel while the window said "3". Forcing the WINDOW up to the raw sum is
        // not available: a node's away-flow on its DRAWN links can exceed local + recorded inflow,
        // because much of its inflow arrives against Phi_w and has no incoming record to live in
        // -- that drove 15 nodes to a negative displayed total. Scaling the PANELS down to the
        // window's figure keeps the model's proportions across edges, makes the panels sum to
        // exactly what the window shows, and cannot go negative, because +0xBC is already clamped
        // into [0, local + incoming] by install_aggregate.
        // NO rescaling. Scaling these by outgoing/raw_sum is what made the on-map panel read 2
        // beside a node-window row reading 10 for the same link. The panel array and the per-link
        // record now carry the identical canonical number.
        // node+0x88 is `steer_power`: one entry per outgoing link, in PER-MILLE (x1000), summing
        // to 1000. Established from the engine's own writers -- the monthly reset at 0xB51360 fills
        // it with 1000/count, and 0xB54D20 normalises accumulated steer power with
        // `imul eax,ecx,0x3e8 / idiv ebx`. Both readable saves confirm it: every node's
        // steer_power list sums to 1.000.
        //
        // It is what the outgoing tooltip turns into ducats:
        //     line_k = steer_permille[k] * node+0xC0 / 1e6      (0xB5653F..0xB56562)
        // so writing the model's per-link SHARES here makes each destination's figure the model's
        // own away-flow, and makes the lines sum to the outgoing header by construction.
        // Writing ducats here (an earlier attempt) put unrelated numbers on the outgoing side;
        // writing nothing left the engine's even 1000/count split, which is just as wrong.
        for (int i = 0; i < n; i++) {
            double share = (raw_sum > 1e-12) ? (raw[i] / raw_sum) : (1.0 / n);
            buf[i] = (int32_t)(share * 1000.0 + 0.5);
            wrote++;
        }
        // make the shares sum to exactly 1000 -- the engine's own normalisation truncates, and any
        // residue would show up as the tooltip lines not adding to the header
        {
            int tot = 0; for (int i = 0; i < n; i++) tot += buf[i];
            if (n > 0 && tot != 1000) {
                int bi = 0; for (int i = 1; i < n; i++) if (buf[i] > buf[bi]) bi = i;
                buf[bi] += (1000 - tot);
                if (buf[bi] < 0) buf[bi] = 0;
            }
        }

        // One incoming record per INCIDENT link, each carrying that link's toward-flow -- so a
        // node lists BOTH directions of every link it touches (north_sea showing lubeck and
        // english_channel on the incoming side as well as the outgoing side). This is orthogonal
        // to the scaling above: the records give the two-way view, the scaling keeps the totals
        // non-negative. Writing `outgoing` from the raw sum is what broke non-negativity before,
        // and is deliberately NOT done here.
        // NOT rebuild_incoming here. It repoints +0xF0/+0xF8 and refills every record, AFTER
        // install_aggregate has already derived `outgoing` from the old records -- so the UI's
        // local + Sigma incoming - outgoing was measured against a vector that no longer existed.
        // That is the negative-total bug. linkvalue::install owns entry+0x10 now.
    }
    return wrote;
}


// --- REVERSE INFLOW RECORDS (spec 1.12 "the value flowing in EACH direction along it") ---------
//
// The engine keeps ONE incoming record per DRAWN link, at the Phi_w destination. Under the
// per-good model a link drawn n->m routinely carries goods m->n as well, and that inflow has
// nowhere to live: node n has no incoming record for a link it points away along. The visible
// consequence is that a node's outgoing cannot be the sum of its own edge panels without the
// displayed total going negative -- north_sea showed "3.26" beside a 10-ducat panel, and forcing
// the two to agree drove 15 nodes negative in two ticks.
//
// So rebuild the vector with one record per INCIDENT link, each carrying that link's toward-flow.
// Record layout, read off live memory (stride 0x20):
//   +0x00 vtable   +0x08 a constant field (low dword 0x165)   +0x10 value (int32 x1000)
//   +0x18 the SOURCE definition
// A new record is a byte copy of an existing one with +0x10 and +0x18 replaced, so the vtable and
// whatever +0x08 means are carried over verbatim rather than guessed.
constexpr int NODE_IN_BEGIN = 0xF0, NODE_IN_END = 0xF8, NODE_IN_CAP = 0x100;
constexpr int REC_STRIDE = 0x20, REC_VALUE = 0x10, REC_SRCDEF = 0x18;

inline uint64_t g_rev_added = 0;

// every incident link of `node`, as (far definition, far node) pairs -- both list directions
inline void incident_defs(uintptr_t node, std::vector<std::pair<uintptr_t,uintptr_t>>& out) {
    uintptr_t def = livetrade::fq(node + 0xA8);
    if (!def) return;
    // De-duplicate. A link can appear in BOTH definition lists (relink's ALLOUT step appends
    // reverse-drawn links to the outgoing list after the incoming lists were rebuilt), and a
    // duplicated neighbour becomes TWO incoming records carrying the same toward-flow -- which
    // doubles that node's incoming, its held, and therefore the pool pass 10 pays out.
    std::set<uintptr_t> seen;
    auto add = [&](uintptr_t fdef) {
        uintptr_t fnode = alledges::node_of_def(fdef);
        if (!fdef || !fnode || fnode == node) return;
        if (!seen.insert(fdef).second) return;
        out.push_back({fdef, fnode});
    };
    // OUTGOING: 0x78-byte link entries, the target definition at +0x30.
    if (livetrade::validate_region(def + 0x98, 16)) {
        uintptr_t b = livetrade::fq(def + 0x98), e = livetrade::fq(def + 0xA0);
        if (b && e > b && (e - b) <= 0x78 * 64)
            for (uintptr_t p = b; p + 0x78 <= e; p += 0x78)
                if (livetrade::validate_region(p + 0x30, 8)) add(livetrade::fq(p + 0x30));
    }
    // INCOMING: an array of DEFINITION POINTERS, stride 8 -- NOT 0x78. Walking it with the
    // outgoing stride made the loop exit immediately on every node (a node has <= 10 links, so
    // p + 0x78 <= e is false at once), so the incoming half contributed NOTHING and each physical
    // link ended up with a record at only ONE end. Same trap already recorded in alledges.h.
    if (livetrade::validate_region(def + 0x80, 16)) {
        uintptr_t b = livetrade::fq(def + 0x80), e = livetrade::fq(def + 0x88);
        if (b && e > b && (e - b) <= 8 * 64)
            for (uintptr_t p = b; p + 8 <= e; p += 8)
                if (livetrade::validate_region(p, 8)) add(livetrade::fq(p));
    }
}

// Rebuild `node`'s incoming records so there is exactly one per incident link, carrying the
// model's toward-flow. Returns the number of records written, or -1 if it declined.
inline int rebuild_incoming(uintptr_t node,
                            const std::map<std::pair<int,int>, double>& gross,
                            int self_f,
                            const std::function<int(uintptr_t)>& field_of_node) {
    std::vector<std::pair<uintptr_t,uintptr_t>> inc;
    incident_defs(node, inc);
    g_nodes_seen++;
    if (inc.empty()) { g_bail_empty++; return -1; }
    if (inc.size() > 64) { g_bail_big++; return -1; }
    // Rebuild ONLY when the shape actually changes. Repointing every tick allocates a fresh engine
    // buffer per node and never frees the old one -- a steady leak. In the common case the vector
    // already has one record per incident link and only the VALUES change, and those are owned by
    // linkvalue::install, which runs after this.
    {
        // Skip only when the vector already holds records for exactly the SAME neighbours.
        // Comparing COUNTS alone was wrong: a node whose stock vector happens to have as many
        // in-drawn records as it has incident links passed this guard and never got records for
        // the links drawn OUT of it -- so value arriving along those had nowhere to live and was
        // dropped from incoming. That is the "reverse inflows are omitted" symptom, and it left
        // 52 of 271 directed inflows with no record at their destination.
        uintptr_t cb = livetrade::rq(node + NODE_IN_BEGIN), ce = livetrade::rq(node + NODE_IN_END);
        if (cb && ce >= cb && (size_t)((ce - cb) / REC_STRIDE) == inc.size()) {
            std::set<uintptr_t> want, have;
            for (auto& pr : inc) want.insert(pr.first);
            for (uintptr_t p = cb; p + REC_STRIDE <= ce; p += REC_STRIDE)
                have.insert(livetrade::fq(p + REC_SRCDEF));
            if (want == have) { g_skip_same++; return (int)inc.size(); }
        }
    }
    // A TEMPLATE record, cached process-wide. Bailing out when THIS node happens to have no
    // existing record (a source node, or one whose vector is empty) was the bug behind the
    // negative totals: the node kept Sigma incoming = 0 while still being given the model's full
    // `outgoing`, so local + 0 - outgoing went straight below zero. Any node's record serves as
    // the template -- only the vtable and the +0x08 constant are copied from it.
    static uint8_t tmpl[REC_STRIDE];
    static bool have_tmpl = false;
    uintptr_t ob = livetrade::rq(node + NODE_IN_BEGIN), oe = livetrade::rq(node + NODE_IN_END);
    if (!have_tmpl && ob && oe > ob && livetrade::validate_region(ob, REC_STRIDE)) {
        memcpy(tmpl, (const void*)ob, REC_STRIDE);
        have_tmpl = true;
    }
    if (!have_tmpl) { g_bail_tmpl++; return -1; }       // nothing anywhere to copy yet
    int n = (int)inc.size();
    auto alloc = (FnNew)(livetrade::module_base() + ENGINE_NEW);
    uint8_t* buf = (uint8_t*)alloc((size_t)n * REC_STRIDE);
    if (!buf) { g_bail_alloc++; return -1; }
    for (int i = 0; i < n; i++) {
        uint8_t* r = buf + (size_t)i * REC_STRIDE;
        memcpy(r, tmpl, REC_STRIDE);
        // value deliberately left at 0: linkvalue::install is the single owner of entry+0x10
        // and fills every record with the link's one canonical figure immediately after.
        *(int32_t*)(r + REC_VALUE)   = 0;
        *(int32_t*)(r + 0x14)        = 0;   // `add` (steering uplift): never inherit the template's
        *(uintptr_t*)(r + REC_SRCDEF) = inc[i].first;
    }
    DWORD old = 0;
    if (!VirtualProtect((void*)(node + NODE_IN_BEGIN), 24, PAGE_READWRITE, &old)) return -1;
    *(uintptr_t*)(node + NODE_IN_BEGIN) = (uintptr_t)buf;
    *(uintptr_t*)(node + NODE_IN_END)   = (uintptr_t)(buf + (size_t)n * REC_STRIDE);
    *(uintptr_t*)(node + NODE_IN_CAP)   = (uintptr_t)(buf + (size_t)n * REC_STRIDE);
    VirtualProtect((void*)(node + NODE_IN_BEGIN), 24, old, &old);
    g_rev_added += n; g_rebuilt++;
    return n;
}

} // namespace outlinks
