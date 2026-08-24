// Non-ironman save parser (spec 2.2 item 2): province owner, base_tax, base_production,
// trade good, devastation (the engine applied on_startup itself, so the save carries the
// result directly); the per-node trade_goods_size arrays (the engine's produced quantity
// lives at node level); and current prices from the change_price block.
//
// Targeted quote-aware block scanning rather than a full parse -- the gamestate is ~34 MB and
// the reference reads it the same way (solver.py _rolled_trade_goods, measure6 _inject_weights).
#pragma once
#include <map>
#include <string>
#include <vector>
#include "zipread.h"

namespace save {

struct Province {
    int id = 0;
    std::string owner, controller, trade_goods;
    double base_tax = 0, base_production = 0, devastation = 0;
    bool has_owner = false;
};

struct NodeEcon {
    std::string name;                    // from definitions="..."
    std::vector<double> goods_size;      // trade_goods_size slots (slot k <-> good index k-1)
    double local_value = 0, total = 0, outgoing = 0, current = 0, retention = 0;
    bool has_local_value = false;
};

struct SaveData {
    std::string date;
    std::vector<Province> provinces;     // in save order (ascending id)
    std::map<std::string, double> current_prices;
    std::vector<NodeEcon> nodes;         // in save order
};

// matching close brace, quote-aware (mirrors the reference's mb())
inline size_t match_brace(const std::string& s, size_t open) {
    int d = 0; bool inq = false;
    for (size_t k = open; k < s.size(); k++) {
        char c = s[k];
        if (c == '"') inq = !inq;
        else if (!inq) {
            if (c == '{') d++;
            else if (c == '}') { d--; if (d == 0) return k; }
        }
    }
    return s.size() - 1;
}

inline std::string unquote(const std::string& v) {
    if (v.size() >= 2 && v.front() == '"' && v.back() == '"') return v.substr(1, v.size() - 2);
    return v;
}

// value of `key=` on a line indented with exactly `tabs` tabs inside blk; "" if absent
inline std::string field_at(const std::string& blk, const std::string& key, int tabs) {
    std::string needle = "\n" + std::string(tabs, '\t') + key + "=";
    size_t i = blk.find(needle);
    if (i == std::string::npos) return "";
    size_t st = i + needle.size();
    if (st < blk.size() && blk[st] == '{') return "";      // block value, not a scalar
    size_t e = st;
    while (e < blk.size() && blk[e] != '\n' && blk[e] != '\r' && blk[e] != ' ' && blk[e] != '\t') e++;
    return unquote(blk.substr(st, e - st));
}

inline SaveData parse_gamestate(const std::string& raw) {
    if (raw.rfind("EU4txt", 0) != 0)
        throw std::runtime_error("not an EU4txt gamestate (ironman or binary save?)");
    SaveData sd;
    {
        size_t i = raw.find("\ndate=");
        if (i != std::string::npos) {
            size_t e = raw.find('\n', i + 1);
            sd.date = raw.substr(i + 6, e - i - 6);
        }
    }
    // ------------------------------------------------------------ provinces --
    size_t pi = raw.find("\nprovinces={");
    if (pi == std::string::npos) throw std::runtime_error("no provinces block");
    size_t popen = raw.find('{', pi);
    size_t pclose = match_brace(raw, popen);
    // records: "\n-<id>={"
    size_t cur = popen + 1;
    while (cur < pclose) {
        size_t r = raw.find("\n-", cur);
        if (r == std::string::npos || r >= pclose) break;
        size_t idstart = r + 2, k = idstart;
        while (k < pclose && isdigit((unsigned char)raw[k])) k++;
        if (k == idstart || k + 1 >= pclose || raw[k] != '=' || raw[k + 1] != '{') { cur = r + 2; continue; }
        int id = atoi(raw.substr(idstart, k - idstart).c_str());
        size_t bopen = k + 1;
        size_t bclose = match_brace(raw, bopen);
        std::string blk = raw.substr(bopen, bclose - bopen + 1);
        Province p; p.id = id;
        p.owner = field_at(blk, "owner", 2);
        p.has_owner = !p.owner.empty();
        p.controller = field_at(blk, "controller", 2);
        p.trade_goods = field_at(blk, "trade_goods", 2);
        std::string bt = field_at(blk, "base_tax", 2);
        std::string bp = field_at(blk, "base_production", 2);
        std::string dv = field_at(blk, "devastation", 2);
        if (!bt.empty()) p.base_tax = std::stod(bt);
        if (!bp.empty()) p.base_production = std::stod(bp);
        if (!dv.empty()) p.devastation = std::stod(dv);
        sd.provinces.push_back(std::move(p));
        cur = bclose + 1;
    }
    // --------------------------------------------------------- change_price --
    size_t ci = raw.find("\nchange_price={");
    if (ci != std::string::npos) {
        size_t copen = raw.find('{', ci);
        size_t cclose = match_brace(raw, copen);
        size_t c2 = copen + 1;
        while (c2 < cclose) {
            size_t r = raw.find("\n\t", c2);
            if (r == std::string::npos || r >= cclose) break;
            size_t nstart = r + 2, k = nstart;
            while (k < cclose && (islower((unsigned char)raw[k]) || raw[k] == '_')) k++;
            if (k > nstart && k + 1 < cclose && raw[k] == '=' && raw[k + 1] == '{') {
                std::string good = raw.substr(nstart, k - nstart);
                size_t bopen = k + 1, bclose = match_brace(raw, bopen);
                std::string blk = raw.substr(bopen, bclose - bopen + 1);
                size_t cp = blk.find("current_price=");
                if (cp != std::string::npos)
                    sd.current_prices[good] = std::stod(blk.substr(cp + 14));
                c2 = bclose + 1;
            } else {
                c2 = r + 2;
            }
        }
    }
    // ---------------------------------------------------------------- trade --
    size_t ti = raw.find("\ntrade={");
    if (ti != std::string::npos) {
        size_t topen = raw.find('{', ti);
        size_t tclose = match_brace(raw, topen);
        size_t c2 = topen + 1;
        while (c2 < tclose) {
            size_t r = raw.find("\n\tnode={", c2);
            if (r == std::string::npos || r >= tclose) break;
            size_t bopen = r + 7;                       // the '{'
            size_t bclose = match_brace(raw, bopen);
            std::string blk = raw.substr(bopen, bclose - bopen + 1);
            NodeEcon ne;
            ne.name = unquote(field_at(blk, "definitions", 2));
            std::string lv = field_at(blk, "local_value", 2);
            if (!lv.empty()) { ne.local_value = std::stod(lv); ne.has_local_value = true; }
            std::string s;
            if (!(s = field_at(blk, "total", 2)).empty()) ne.total = std::stod(s);
            if (!(s = field_at(blk, "outgoing", 2)).empty()) ne.outgoing = std::stod(s);
            if (!(s = field_at(blk, "current", 2)).empty()) ne.current = std::stod(s);
            if (!(s = field_at(blk, "retention", 2)).empty()) ne.retention = std::stod(s);
            size_t g = blk.find("trade_goods_size={");
            if (g != std::string::npos) {
                size_t go = blk.find('{', g);
                size_t gc = match_brace(blk, go);
                std::string body = blk.substr(go + 1, gc - go - 1);
                size_t q = 0;
                while (q < body.size()) {
                    while (q < body.size() && isspace((unsigned char)body[q])) q++;
                    size_t e = q;
                    while (e < body.size() && !isspace((unsigned char)body[e])) e++;
                    if (e > q) ne.goods_size.push_back(std::stod(body.substr(q, e - q)));
                    q = e;
                }
            }
            sd.nodes.push_back(std::move(ne));
            c2 = bclose + 1;
        }
    }
    return sd;
}

inline SaveData load(const std::string& save_path) {
    return parse_gamestate(zipread::zip_entry(save_path, "gamestate"));
}

} // namespace save
