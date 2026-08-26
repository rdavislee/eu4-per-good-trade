// SENDING A MERCHANT TO THE NODE THE PLAN CHOSE (spec 3.14; the frontier model's last link).
//
// frontier::plan says where a country's k merchants should stand. aiwire can only write a
// placement where a merchant already IS; a planned node with no merchant there is counted as
// g_wants_move and nothing happens -- 1,005 of them on tick 7, against 8 placed. This file is the
// mechanic that closes that gap: dispatch the country's free (or worst-placed) merchant to the
// planned node through the engine's own send-merchant command, so it physically travels, posts,
// and acquires a trade record there that syncrec can then set to steer.
//
// Everything below the constants is engine-fact-free: the token, Execute RVA, payload layout and
// posting path come from the send-merchant trace (Q1-Q5) and are filled in from it. Until they
// are, install() refuses and the AI keeps counting wants_move -- it never posts a guessed command.
#pragma once
#include <windows.h>
#include <cstdint>
#include <fstream>
#include <map>
#include <string>
#include <vector>
#include "livetrade.h"
#include "aiwire.h"

namespace envoy {

// ---- FROM THE TRACE. Zero means "not yet established"; install() refuses on any zero. ----
constexpr uint32_t  CMD_TOKEN        = 0;        // send-merchant command token id
constexpr uintptr_t CMD_VTABLE       = 0;        // its vtable RVA
constexpr uintptr_t CMD_EXECUTE      = 0;        // Execute RVA (vtable slot +0x48 for steer; confirm)
constexpr size_t    CMD_SIZE         = 0;        // operator new size
constexpr int       CMD_COUNTRY      = 0;        // offset of the 8-byte country handle
constexpr int       CMD_NODE         = 0;        // offset of the destination node index
constexpr int       CMD_ENVOY        = 0;        // offset of the envoy/merchant id, if any
constexpr int       CMD_MODE         = 0;        // offset of collect(0)/transfer(1), if any
constexpr bool      NODE_IS_1BASED   = false;    // def+0xD8 style (1-based) vs array index

inline bool established() {
    return CMD_TOKEN && CMD_VTABLE && CMD_SIZE && CMD_COUNTRY && CMD_NODE;
}

inline uint64_t g_sent = 0, g_refused = 0;
inline std::string g_log;

// Post a send-merchant for `country_index` toward `node` (field index -> engine node). Returns
// false and touches nothing if the command is not established or any input fails validation.
inline bool send(int country_index, uintptr_t node_obj, int merchant_id, std::ofstream* lg) {
    if (!established()) { g_refused++; return false; }
    (void)country_index; (void)node_obj; (void)merchant_id; (void)lg;
    // Filled in from the trace:
    //   1. handle = *(uint64*)(record+0x10) for this country at ANY node it has a record, or from
    //      the country object (0xD01A0 accessor) -- never synthesised.
    //   2. cmd = operator new(CMD_SIZE); *(void**)cmd = base+CMD_VTABLE; token at its slot;
    //      handle at CMD_COUNTRY; node id at CMD_NODE (1-based if NODE_IS_1BASED);
    //      envoy id at CMD_ENVOY; mode=1 (transfer) at CMD_MODE.
    //   3. post via the same path the UI uses (IGI->vtbl[0x80] -> [[rcx]+0x30]) or call Execute
    //      directly if the trace shows the gate would drop a DLL-posted command in single-player.
    return false;
}

// One pass per AI tick: for each country, for each planned node with no merchant standing there,
// send its least profitable merchant (or a free one) there. Damped by the same dwell floor as
// aiwire so a merchant is not bounced every cadence.
inline int dispatch_wants(std::ofstream* lg) {
    if (!established()) return 0;
    (void)lg;
    return 0;
}

inline bool install(const std::string& logpath, std::string* err) {
    g_log = logpath;
    if (!established()) {
        if (err) *err = "send-merchant command not established (token/vtable/size/offsets are 0)";
        return false;
    }
    return true;
}

} // namespace envoy
