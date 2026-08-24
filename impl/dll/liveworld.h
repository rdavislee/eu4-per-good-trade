// READ THE WORLD FROM LIVE MEMORY (spec 2.2: "The shipped DLL carries a second implementation
// ... reading live memory instead of save files"; "the DLL never reads a save").
//
// This is what makes the orientation MOVE. Until now the DLL built its wealth field from the
// 1444 start save, so every re-solve returned the same graphs no matter what happened in the
// campaign -- development growth, devastation, conquest and price changes were all invisible.
// Reading the live province table instead makes the monthly re-solve responsive, which is what
// tests F1 (a flip is honoured), F3 (owner changes move nothing day-of), F4 (war bites through
// devastation) and F5 (price crash) actually exercise.
//
// The province fields are exactly the ones spec 1.3 admits -- development, the trade good, and
// the province's own condition -- and nothing owner-derived, so the field stays owner-agnostic.
// The output is a save::SaveData, so field::build() and the whole solver path downstream are the
// SAME code the reference implementation runs (spec 2.8's cross-implementation requirement).
//
// Offsets (build 835bfdf8, see OFFSETS.md):
//   provinces = *(char**)(G+0x1CA8), INLINE array, stride 0x2E10, subscript == province id
//   count     = (*(char**)(G+0x1CB0) - *(char**)(G+0x1CA8)) / 0x2E10
//   +0x20 id · +0x3E4 base_tax · +0x3E8 base_production (int32 x1000) · +0x42C devastation
//   +0x458 CTradeGood* · +0x46F owner-validity byte · +0xE8 CTradeNode*
//   CTradeGood: +0x18 std::string name · +0x78 id · +0x7C base price
//   price table: *(char**)(*(void**)(G+0x25D0)+8) + i*0x38, current price at +4
#pragma once
#include <cstdint>
#include <map>
#include <string>
#include <vector>
#include "livetrade.h"
#include "../src/save.h"

namespace liveworld {

constexpr int PROV_STRIDE      = 0x2E10;
constexpr int PROV_ID          = 0x20;
constexpr int PROV_NODE        = 0xE8;
constexpr int PROV_BASE_TAX    = 0x3E4;
constexpr int PROV_BASE_PROD   = 0x3E8;
constexpr int PROV_DEVASTATION = 0x42C;
constexpr int PROV_GOOD        = 0x458;
constexpr int PROV_OWNER_VALID = 0x46F;
constexpr int GOOD_NAME        = 0x18;
constexpr int GOOD_ID          = 0x78;
constexpr int GOOD_BASE_PRICE  = 0x7C;

// MSVC std::string: [0x00] union { char buf[16]; char* ptr }, [0x10] size, [0x18] capacity.
// Long strings (capacity >= 16) live behind the pointer.
inline std::string read_std_string(uintptr_t s) {
    if (!livetrade::validate_region(s, 0x20)) return "";
    uint64_t size = (uint64_t)livetrade::fq(s + 0x10);
    uint64_t cap  = (uint64_t)livetrade::fq(s + 0x18);
    if (size > 4096) return "";
    if (cap >= 16) {
        uintptr_t p = livetrade::fq(s);
        if (!p || !livetrade::validate_region(p, size + 1)) return "";
        return std::string((const char*)p, (size_t)size);
    }
    char buf[17] = {0};
    memcpy(buf, (const void*)s, 16);
    return std::string(buf, (size_t)(size < 16 ? size : 15));
}

// good id -> lowercase name, read once from the trade-goods database each solve
inline std::map<int, std::string> read_good_names() {
    std::map<int, std::string> out;
    uintptr_t db = livetrade::rq(livetrade::module_base() + 0x242BE70);
    if (!db || !livetrade::validate_region(db + 0x10, 16)) return out;
    uintptr_t begin = livetrade::fq(db + 0x10), end = livetrade::fq(db + 0x18);
    if (!begin || end <= begin || (end - begin) > 8 * 512) return out;
    if (!livetrade::validate_region(begin, end - begin)) return out;
    for (uintptr_t p = begin; p + 8 <= end; p += 8) {
        uintptr_t g = livetrade::fq(p);
        if (!g || !livetrade::validate_region(g + GOOD_NAME, 0x20)) continue;
        int id = livetrade::ri(g + GOOD_ID);
        std::string nm = read_std_string(g + GOOD_NAME);
        if (!nm.empty()) out[id] = nm;
    }
    return out;
}

// current price per good NAME (after price events / change_price), from the live price table
inline std::map<std::string, double> read_prices(const std::map<int, std::string>& names) {
    std::map<std::string, double> out;
    uintptr_t g = livetrade::game_singleton();
    if (!g) return out;
    uintptr_t holder = livetrade::rq(g + 0x25D0);
    if (!holder || !livetrade::validate_region(holder + 8, 8)) return out;
    uintptr_t tbl = livetrade::fq(holder + 8);
    int32_t n = livetrade::ri(holder + 0x14);
    if (!tbl || n <= 0 || n > 512) return out;
    if (!livetrade::validate_region(tbl, (size_t)n * 0x38)) return out;
    for (int i = 0; i < n; i++) {
        auto it = names.find(i);
        if (it == names.end()) continue;
        out[it->second] = livetrade::fi(tbl + (uintptr_t)i * 0x38 + 4) / 1000.0;
    }
    return out;
}

struct WorldRead {
    save::SaveData sd;
    int provinces_seen = 0, owned = 0, with_good = 0;
    bool ok = false;
};

// Read every province the model counts (spec 1.3: owned, in a node, with a trade good).
inline WorldRead read_world() {
    WorldRead w;
    uintptr_t g = livetrade::game_singleton();
    if (!g) return w;
    uintptr_t base = livetrade::rq(g + 0x1CA8);
    uintptr_t endp = livetrade::rq(g + 0x1CB0);
    if (!base || endp <= base) return w;
    size_t span = endp - base;
    int count = (int)(span / PROV_STRIDE);
    if (count <= 0 || count > 20000) return w;
    if (!livetrade::validate_region(base, span)) return w;

    auto good_names = read_good_names();
    w.sd.current_prices = read_prices(good_names);

    for (int i = 0; i < count; i++) {
        uintptr_t p = base + (uintptr_t)i * PROV_STRIDE;
        int id = livetrade::fi(p + PROV_ID);
        if (id <= 0) continue;
        w.provinces_seen++;
        save::Province pr;
        pr.id = id;
        pr.has_owner = livetrade::fb(p + PROV_OWNER_VALID) != 0;
        if (!pr.has_owner) continue;                       // spec 1.3 counts owned provinces
        w.owned++;
        pr.base_tax        = livetrade::fi(p + PROV_BASE_TAX) / 1000.0;
        pr.base_production = livetrade::fi(p + PROV_BASE_PROD) / 1000.0;
        pr.devastation     = livetrade::fi(p + PROV_DEVASTATION) / 1000.0;
        uintptr_t gd = livetrade::fq(p + PROV_GOOD);
        if (gd && livetrade::validate_region(gd + GOOD_ID, 8)) {
            int gid = livetrade::ri(gd + GOOD_ID);
            auto it = good_names.find(gid);
            if (it != good_names.end()) { pr.trade_goods = it->second; w.with_good++; }
        }
        if (pr.trade_goods.empty()) continue;
        w.sd.provinces.push_back(std::move(pr));
    }
    w.ok = w.owned > 0 && w.with_good > 0;
    return w;
}

} // namespace liveworld
