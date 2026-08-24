// The memory-track hook seams (spec 2.7, 2.9). Each is the point where the mod meets live engine
// memory. Several are now RESOLVED for build 835bfdf8 by the RE session (static disassembly +
// live hardware-breakpoint tracing + a research fan-out over the Clausewitz string→xref→.data
// method). All offsets below are RVAs into eu4.exe (add the live module base). A patch invalidates
// them (spec 2.5) -- re-derive by the AOB signatures.
//
// CONFIRMED (build 835bfdf8):
//   TRADENODE_DB_GLOBAL   eu4.exe+0x242B8C8  -- .data qword: ptr to the TradeNodeDatabase singleton
//                         (from the DB-init cluster at eu4.exe+0x2080DD, verified: [global] live
//                          resolves to the trade-node database object)
//   TRADENODE_DEF_VTABLE  eu4.exe+0x1C439D0  -- vtable of the CTradeNodeDefinition objects; a
//                         pointer-scan for it enumerates all 80 nodes; node name is an inline
//                         std::string (SSO) at object+0x10 (verified: 77 distinct node names read)
//   local_value  = *(int32*)( *(void**)(node+0xF8) + 0xB4 )  / 1000   (fixed-point x1000)
//   incoming_value cache at node+0x160 ; local_value cache at node+0x168  (serializer dirty ints)
//   SERIALIZER   eu4.exe+0x13CFFB7 (local_value), 0x13D239E (trade_goods_size) -- iterates every
//                node touching every saved field; the field-offset ground truth (r14 = CTradeNode)
//   MONTHLY_TICK eu4.exe+0x2F374D  -- the serial monthly-update dispatcher ("MonthlyUpdateSerial")
//   AOB (survive tooling rebuilds): TradeNodeDatabase init
//     "48 8D 15 ?? ?? ?? ?? 48 8D 4C 24 70 E8 ?? ?? ?? ?? 90 84 DB 74 0C"
//
// Once a signature/offset is filled in, hooks::install() resolves it; the remaining PENDING seams
// (per-good routing write-back, the node-window UI data sources) need the rest of the runtime
// CTradeNode field map (spec 2.9's schedule risk). Nothing here fabricates an offset.
#pragma once
#include <cstdint>
#include <string>
#include <vector>
#include "pattern.h"

namespace tradeoff {
// Confirmed RVAs for build 835bfdf8 (eu4.exe). Add live module base to use.
constexpr uintptr_t TRADENODE_DB_GLOBAL  = 0x242B8C8;   // .data: ptr to TradeNodeDatabase
constexpr uintptr_t TRADENODE_DEF_VTABLE = 0x1C439D0;   // CTradeNodeDefinition vtable
constexpr uintptr_t SERIALIZER_LOCALVAL  = 0x13CFFB7;   // local_value serializer (r14=CTradeNode)
constexpr uintptr_t SERIALIZER_TGS       = 0x13D239E;   // trade_goods_size serializer
constexpr uintptr_t MONTHLY_TICK         = 0x2F374D;    // monthly-update dispatcher (hook the tick)
constexpr int NODE_NAME_OFF   = 0x10;    // inline std::string (SSO) node name in the def object
constexpr int NODE_SUBOBJ_OFF = 0xF8;    // CTradeNode -> value sub-object
constexpr int SUB_LOCALVAL_OFF = 0xB4;   // sub-object -> local_value*1000 (int32)
constexpr int SUB_OUTGOING_OFF = 0xBC;   // sub-object -> outgoing_value*1000 (int32)

// ---------------------------------------------------------------------------------------
// THE NODE-WINDOW FIELD MAP (spec 1.12's six fields), recovered by disassembling the save
// serializer at eu4.exe+0x13CF000..0x13D0700 where r14 = the live CTradeNode. Each field is an
// int32 in FIXED-POINT x1000 (matching the engine's 1/1000 quantisation, spec 2.1). The
// serializer both computes the value and caches it in the node at the offset below, so these
// offsets are exactly what the DLL reads (spec 1.8) and overwrites (spec 2.6/1.12).
//
//   incoming_value  node+0x160   <- computed inflow
//   outgoing_value  node+0x164   <- [node+0xF8]+0xBC
//   local_value     node+0x168   <- [node+0xF8]+0xB4     (the inject basis, spec 1.8)
//   total_value     node+0x16C   <- computed
//   our_from_this   node+0x170   <- the country's own take (spec 1.12)
//   goods_produced_value  node+0x180  (serializer site eu4+0x13CF99C, via r13)
// Serializer sites: total 0x13CFC8C, outgoing 0x13CFDDF, local 0x13CFFB7, incoming 0x13D017E,
// our_from_this 0x13D03A1, piracy_value 0x13D068E, retention_power 0x13D24AC.
constexpr int NODE_INCOMING_VALUE = 0x160;   // all six are int32, value*1000
constexpr int NODE_OUTGOING_VALUE = 0x164;
constexpr int NODE_LOCAL_VALUE    = 0x168;
constexpr int NODE_TOTAL_VALUE    = 0x16C;
constexpr int NODE_OUR_FROM_THIS  = 0x170;
constexpr int NODE_GOODS_PRODUCED = 0x180;
constexpr double FIXED_POINT = 1000.0;       // engine stores these as value x 1000

// runtime map/render node class: vtable eu4.exe+0x1D82450, holds its definition ptr at +0x80,
// laid out at a 0x200 stride (one per trade node) -- discovered in-process by the injected DLL.
constexpr uintptr_t TRADENODE_RENDER_VTABLE = 0x1D82450;
constexpr int RENDER_DEFPTR_OFF = 0x80;

// =========================================================================================
// THE SIMULATION TRADE MODEL -- recovered by disassembling the monthly-update driver and the
// per-node calc passes. This is the authoritative path the DLL reads (spec 1.8) and writes
// (spec 2.6); the UI cache offsets above are the display side of the same numbers.
//
//   G   = *(void**)(base + GAME_SINGLETON)            the game-state singleton
//   mgr = G + TRADE_MANAGER_OFF                       CTradeManager (inline in G)
//   nodes: base=*(void**)(mgr+0x18), count=*(int32*)(mgr+0x24), stride 0x138
//     proof: 0xB4BD0F mov rbx,[rsi+0x18] / 0xB4BD13 movsxd rcx,[rsi+0x24] / imul rdi,rcx,0x138
//   calc order: *(void**)(mgr+0x30), count *(int32*)(mgr+0x3c), stride 8 (topological)
//
// Per-node (CTradeNode, 0x138 bytes) -- all int32 fixed-point x1000 unless noted:
//   +0xB0 gross local value      +0xB4 local_value (the inject basis, spec 1.8)
//   +0xB8 retention              +0xBC outgoing_value
//   +0xC4 privateer share        +0xCC accumulated total value
//   +0x120 node index/id         +0x124 dirty/active flag
//   +0xF0/+0xF8/+0x100  incoming-link vector (stride 0x20, value at +0x10)
//   +0x108/+0x110/+0x118  vector<int32> trade_goods_size -- the PER-GOOD produced quantity
//     proof: 0xB5177C  add [rcx+rdx*4], eax   with rcx=[node+0x108], rdx=good id
//     read good k:  base=*(int64*)(node+0x108); qty = *(int32*)(base + 4*k)
//     length:       N = (*(int64*)(node+0x110) - base) / 4
//
// Monthly update driver: fn_0xB4BA90(mgr). Pass 4 (0xB51360) clears/resizes the per-good array,
// pass 5 (0xB51500) fills it and computes local_value, pass 9 (0xB52160) is the flow pass that
// writes outgoing/retention. WRITE-BACK HOOK: 0xB4BF00, just after the flow pass, where rbx is
// the finalized CTradeNode* and rsi is the manager -- the natural place for spec 2.6's writes.
constexpr uintptr_t GAME_SINGLETON      = 0x233FE78;   // .data: ptr to the game state
constexpr int       TRADE_MANAGER_OFF   = 0x2198;      // G + this = CTradeManager
constexpr int       MGR_NODES_PTR       = 0x18;        // -> node array base
constexpr int       MGR_NODES_COUNT     = 0x24;        // int32 count
constexpr int       NODE_STRIDE         = 0x138;
constexpr int       MGR_CALCORDER_PTR   = 0x30;        // vector<CTradeNode*> in flow order
constexpr int       MGR_CALCORDER_COUNT = 0x3c;
constexpr int       SIM_LOCAL_VALUE     = 0xB4;        // int32 x1000
constexpr int       SIM_GROSS_LOCAL     = 0xB0;
constexpr int       SIM_RETENTION       = 0xB8;
constexpr int       SIM_OUTGOING_VALUE  = 0xBC;
constexpr int       SIM_PIRACY_SHARE    = 0xC4;
constexpr int       SIM_TOTAL_ACCUM     = 0xCC;
constexpr int       SIM_NODE_ID         = 0x120;
constexpr int       SIM_TGS_BEGIN       = 0x108;       // vector<int32> trade_goods_size
constexpr int       SIM_TGS_END         = 0x110;
constexpr int       SIM_INCOMING_BEGIN  = 0xF0;        // incoming links, stride 0x20, val +0x10
constexpr int       SIM_INCOMING_END    = 0xF8;
constexpr uintptr_t MONTHLY_UPDATE_FN   = 0xB4BA90;    // the real monthly trade update driver
constexpr uintptr_t WRITEBACK_HOOK      = 0xB4BF00;    // after the flow pass (rbx=node, rsi=mgr)
}

namespace hooks {

struct Seam {
    const char* name;
    const char* purpose;
    const char* signature;      // "" until found in the debugger session
    uintptr_t addr = 0;         // resolved by pat::find at attach if signature is set
    bool required_for_write;    // true = writing needs it; false = read-only path
};

// The seams, in the order spec 2.9's memory track lists them.
inline std::vector<Seam> seams() {
    return {
        // --- the monthly trade tick: where the mod recomputes and writes (spec 2.6) ---
        {"trade_tick", "monthly trade tick hook: solve per good, write node values (spec 2.6)",
         "", 0, true},
        // --- live produced quantity: inject_g(n) = trade_goods_size(n,g) x price (spec 1.8) ---
        {"node_trade_goods_size", "per-node trade_goods_size arrays -- the engine's produced "
         "quantity at node x good, the value the network routes (spec 1.8)", "", 0, false},
        {"node_value_fields", "the six node-window fields (incoming/local/total/outgoing/"
         "our_from_this/piracy) to overwrite with the per-good economy (spec 1.12)", "", 0, true},
        // --- merchant assignment: read for UI + shadow cadence, write for our placement (3.14) ---
        {"merchant_assignments", "per-country merchant node/link assignments -- read for the UI "
         "(C1-C5) and the shadow-vanilla cadence diff, write for our placement (spec 3.14)",
         "", 0, true},
        // --- trade power per country per node: powershare, propagation, eligibility (1.8/1.9) ---
        {"node_country_power", "per-node per-country trade power for powershare_C, propagation "
         "and per-good eligibility (spec 1.8, 1.9)", "", 0, false},
        // --- the nation-pair direction gates of spec 1.10, returned true at the call site ---
        {"direction_gates", "upstream/downstream nation-pair gates -> return true at the call "
         "site (spec 1.10, 2.5)", "", 0, true},
        // --- current prices in live memory (change_price applied) for inject and alpha ---
        {"current_prices", "live current_price per good for inject and alpha (spec 1.4, 1.8)",
         "", 0, false},
    };
}

struct InstallReport {
    int resolved = 0, pending = 0;
    std::vector<std::string> lines;
};

// resolve every seam whose signature is known; report the rest as pending. Never invents an
// address. Writing seams that stay pending keep the mod read-only.
inline InstallReport install(const pat::Module& m) {
    InstallReport r;
    for (Seam s : seams()) {
        if (s.signature && s.signature[0]) {
            uintptr_t a = pat::find(m, s.signature);
            if (a) {
                r.resolved++;
                r.lines.push_back(std::string("[ok]      ") + s.name + " @ " + std::to_string(a));
            } else {
                r.pending++;
                r.lines.push_back(std::string("[MISS]    ") + s.name +
                                  " -- signature set but not found (patch drift?)");
            }
        } else {
            r.pending++;
            r.lines.push_back(std::string("[pending] ") + s.name + " -- " + s.purpose);
        }
    }
    return r;
}

} // namespace hooks
