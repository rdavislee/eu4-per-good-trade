// Install-side data: the defines parser (spec 2.9's first deliverable), prices,
// the static-modifier reads (GP_COEFF and the four province-state modifiers, spec 1.3/2.3),
// and the tradenodes file (adjacency, members, path/control render data, flags -- spec 2.2 item 1).
#pragma once
#include <algorithm>
#include <cmath>
#include <filesystem>
#include <map>
#include <set>
#include <string>
#include <vector>
#include "pdx.h"
#include "zipread.h"   // for read_file

namespace gamedata {

namespace fs = std::filesystem;

// ---------------------------------------------------------------- defines ----
// defines.lua is one Lua table: NDefines = { NGame = { KEY = value, ... }, ... }.
// common/defines/*.lua override single keys as `NDefines.NGroup.KEY = value` lines, applied
// in sorted filename order (spec 2.2 item 3). difficulty_*.lua are engine-applied only for
// their difficulty setting; they are parsed but held separately and NOT merged by default.
struct Defines {
    std::map<std::string, std::string> base;                       // "NGame.START_DATE" -> raw value
    std::map<std::string, std::map<std::string, std::string>> difficulty;  // file stem -> overrides

    std::string get_str(const std::string& key) const {
        auto it = base.find(key);
        if (it == base.end()) throw std::runtime_error("define not found: " + key);
        return it->second;
    }
    double get(const std::string& key) const { return std::stod(get_str(key)); }
};

inline std::string strip_lua_comments(const std::string& text) {
    std::string out; out.reserve(text.size());
    bool inq = false;
    for (size_t i = 0; i < text.size(); i++) {
        char c = text[i];
        if (c == '\n') { inq = false; out.push_back(c); continue; }
        if (c == '"') inq = !inq;
        if (!inq && c == '-' && i + 1 < text.size() && text[i + 1] == '-') {
            while (i < text.size() && text[i] != '\n') i++;
            out.push_back('\n');
            continue;
        }
        out.push_back(c);
    }
    return out;
}

inline void parse_defines_table(const std::string& text, std::map<std::string, std::string>& out) {
    // tokenizer for the subset actually used: identifiers, numbers, strings, { } = ,
    std::string s = strip_lua_comments(text);
    std::vector<std::string> toks;
    size_t i = 0, n = s.size();
    while (i < n) {
        char c = s[i];
        if (isspace((unsigned char)c) || c == ',') { i++; continue; }
        if (c == '"') {
            size_t j = s.find('"', i + 1);
            if (j == std::string::npos) j = n - 1;
            toks.push_back(s.substr(i, j - i + 1)); i = j + 1;
        } else if (c == '{' || c == '}' || c == '=') {
            toks.push_back(std::string(1, c)); i++;
        } else {
            size_t j = i;
            while (j < n && !isspace((unsigned char)s[j]) && s[j] != '{' && s[j] != '}' &&
                   s[j] != '=' && s[j] != ',' && s[j] != '"') j++;
            toks.push_back(s.substr(i, j - i)); i = j;
        }
    }
    // expect: NDefines = { GROUP = { KEY = VALUE ... } ... }
    std::vector<std::string> path;
    for (size_t t = 0; t < toks.size(); t++) {
        if (toks[t] == "}") { if (!path.empty()) path.pop_back(); continue; }
        if (t + 1 < toks.size() && toks[t + 1] == "=") {
            const std::string& key = toks[t];
            if (t + 2 < toks.size() && toks[t + 2] == "{") {
                path.push_back(key); t += 2;
            } else if (t + 2 < toks.size()) {
                std::string val = toks[t + 2];
                if (val.size() >= 2 && val.front() == '"' && val.back() == '"')
                    val = val.substr(1, val.size() - 2);
                // path is like ["NDefines","NGame"]; store as "NGame.KEY"
                if (path.size() >= 2)
                    out[path[1] + "." + key] = val;
                t += 2;
            }
        }
    }
}

inline void parse_defines_overrides(const std::string& text, std::map<std::string, std::string>& out) {
    // lines of the form: NDefines.NGroup.KEY = value
    std::string s = strip_lua_comments(text);
    size_t pos = 0;
    while (pos < s.size()) {
        size_t eol = s.find('\n', pos);
        if (eol == std::string::npos) eol = s.size();
        std::string line = s.substr(pos, eol - pos);
        pos = eol + 1;
        size_t d = line.find("NDefines.");
        if (d == std::string::npos) continue;
        size_t eq = line.find('=', d);
        if (eq == std::string::npos) continue;
        std::string lhs = line.substr(d + 9, eq - d - 9);
        std::string rhs = line.substr(eq + 1);
        auto trim = [](std::string& x) {
            while (!x.empty() && isspace((unsigned char)x.back())) x.pop_back();
            size_t b = 0; while (b < x.size() && isspace((unsigned char)x[b])) b++;
            x = x.substr(b);
        };
        trim(lhs); trim(rhs);
        if (rhs.size() >= 2 && rhs.front() == '"' && rhs.back() == '"')
            rhs = rhs.substr(1, rhs.size() - 2);
        size_t dot = lhs.find('.');
        if (dot == std::string::npos) continue;
        out[lhs.substr(0, dot) + "." + lhs.substr(dot + 1)] = rhs;   // "NGroup.KEY"
    }
}

inline Defines load_defines(const std::string& eu4_root) {
    Defines d;
    parse_defines_table(zipread::read_file(eu4_root + "/common/defines.lua"), d.base);
    std::vector<fs::path> files;
    fs::path dir = fs::path(eu4_root) / "common" / "defines";
    if (fs::exists(dir))
        for (auto& e : fs::directory_iterator(dir))
            if (e.path().extension() == ".lua") files.push_back(e.path());
    std::sort(files.begin(), files.end());
    for (auto& f : files) {
        std::string stem = f.stem().string();
        if (stem.rfind("difficulty_", 0) == 0) {
            parse_defines_overrides(zipread::read_file(f.string()), d.difficulty[stem]);
        } else {
            parse_defines_overrides(zipread::read_file(f.string()), d.base);
        }
    }
    return d;
}

// ----------------------------------------------------------------- prices ----
inline std::map<std::string, double> load_prices(const std::string& eu4_root) {
    auto root = pdx::parse(zipread::read_file(eu4_root + "/common/prices/00_prices.txt"));
    std::map<std::string, double> prices;
    for (auto& p : root->kv) {
        if (p.first.empty() || !p.second.is_node()) continue;
        std::string bp = p.second.node->get_str("base_price", "1.0");
        prices[p.first] = std::stod(bp);
    }
    return prices;
}

// trade-good index order from 00_tradegoods.txt: save slot k <-> good index k-1 (spec 1.8)
inline std::vector<std::string> load_goods_order(const std::string& eu4_root) {
    auto root = pdx::parse(zipread::read_file(eu4_root + "/common/tradegoods/00_tradegoods.txt"));
    std::vector<std::string> order;
    for (auto& p : root->kv)
        if (!p.first.empty() && p.second.is_node()) order.push_back(p.first);
    return order;
}

// ------------------------------------------------- static modifiers (1.3) ----
struct StaticMods {
    double gp_coeff;                            // provincial_production_size.trade_goods_size
    std::map<std::string, double> state_goods_mod;   // devastation/prosperity/occupied/under_siege
};

inline StaticMods load_static_mods(const std::string& eu4_root) {
    auto root = pdx::parse(zipread::read_file(
        eu4_root + "/common/static_modifiers/00_static_modifiers.txt"));
    StaticMods sm{};
    const pdx::Value* pps = root->get("provincial_production_size");
    if (!pps || !pps->is_node())
        throw std::runtime_error("provincial_production_size not found - re-derive GP_COEFF");
    std::string tg = pps->node->get_str("trade_goods_size");
    if (tg.empty())
        throw std::runtime_error("provincial_production_size carries no trade_goods_size");
    sm.gp_coeff = std::stod(tg);
    for (const char* key : {"devastation", "prosperity", "occupied", "under_siege"}) {
        const pdx::Value* blk = root->get(key);
        if (!blk || !blk->is_node())
            throw std::runtime_error(std::string("static modifier not found: ") + key);
        std::string v = blk->node->get_str("trade_goods_size_modifier");
        if (v.empty())
            throw std::runtime_error(std::string(key) + " carries no trade_goods_size_modifier");
        sm.state_goods_mod[key] = std::stod(v);
    }
    return sm;
}

// -------------------------------------------------------------- tradenodes ---
struct Outgoing {
    std::string name;
    std::vector<int> path;
    std::vector<double> control;
};
struct TradeNode {
    std::string name;
    int location = 0;
    bool inland = false, end = false;
    std::string ai_will_propagate;              // raw value or empty
    std::vector<int> members;
    std::vector<Outgoing> outgoing;
    std::vector<std::string> keys;              // every key present, for round-trip checks
};
struct TradeNodes {
    std::vector<TradeNode> nodes;               // in declaration order
    std::vector<std::string> order;             // names in declaration order
    std::map<std::string, int> nidx;
    std::vector<std::pair<int, int>> edges_und; // sorted unique (min,max) pairs
    std::vector<std::vector<int>> und;          // adjacency in declaration order of outgoing blocks
    std::map<int, int> pnode;                   // province -> node index
};

inline TradeNodes parse_tradenodes(const std::string& text) {
    auto root = pdx::parse(text);
    TradeNodes tn;
    for (auto& p : root->kv) {
        if (p.first.empty() || !p.second.is_node()) continue;
        const pdx::Node& b = *p.second.node;
        TradeNode nd;
        nd.name = p.first;
        nd.location = atoi(b.get_str("location", "0").c_str());
        nd.inland = b.get_str("inland") == "yes";
        nd.end = b.get_str("end") == "yes";
        nd.ai_will_propagate = b.get_str("ai_will_propagate_through_trade");
        if (const pdx::Value* mem = b.get("members"); mem && mem->is_node())
            for (auto& v : mem->node->values()) nd.members.push_back(atoi(v.c_str()));
        for (const pdx::Node* og : b.getall("outgoing")) {
            Outgoing o;
            o.name = og->get_str("name");
            if (const pdx::Value* pv = og->get("path"); pv && pv->is_node())
                for (auto& v : pv->node->values()) o.path.push_back(atoi(v.c_str()));
            if (const pdx::Value* cv = og->get("control"); cv && cv->is_node())
                for (auto& v : cv->node->values()) o.control.push_back(std::stod(v));
            nd.outgoing.push_back(std::move(o));
        }
        for (auto& kvp : b.kv) if (!kvp.first.empty()) nd.keys.push_back(kvp.first);
        tn.nidx[nd.name] = int(tn.nodes.size());
        tn.order.push_back(nd.name);
        tn.nodes.push_back(std::move(nd));
    }
    int N = int(tn.nodes.size());
    tn.und.assign(N, {});
    std::set<std::pair<int, int>> es;
    for (int a = 0; a < N; a++) {
        for (auto& o : tn.nodes[a].outgoing) {
            auto it = tn.nidx.find(o.name);
            if (it == tn.nidx.end()) throw std::runtime_error("outgoing to unknown node " + o.name);
            int b = it->second;
            tn.und[a].push_back(b);
            tn.und[b].push_back(a);
            es.insert({std::min(a, b), std::max(a, b)});
        }
    }
    tn.edges_und.assign(es.begin(), es.end());
    for (int i = 0; i < N; i++)
        for (int pid : tn.nodes[i].members) tn.pnode[pid] = i;
    return tn;
}

inline TradeNodes load_tradenodes(const std::string& path) {
    return parse_tradenodes(zipread::read_file(path));
}

} // namespace gamedata
