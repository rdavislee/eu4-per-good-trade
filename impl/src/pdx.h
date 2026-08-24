// Paradox-script tokenizer/parser -- the C++ counterpart of the reference's pdx.py.
// Produces a list of (key, value) pairs per block, since PDX files repeat keys
// (e.g. multiple `outgoing={}` blocks). Quote-aware comment stripping, latin-1 bytes
// passed through untouched.
#pragma once
#include <string>
#include <vector>
#include <memory>
#include <functional>
#include <stdexcept>

namespace pdx {

struct Node;
struct Value {
    std::string str;                 // set when leaf
    std::unique_ptr<Node> node;      // set when block
    bool is_node() const { return node != nullptr; }
};
using KV = std::pair<std::string, Value>;   // key is "" for bare (array) values

struct Node {
    std::vector<KV> kv;
    const Value* get(const std::string& key) const {
        for (auto& p : kv) if (p.first == key) return &p.second;
        return nullptr;
    }
    std::string get_str(const std::string& key, const std::string& def = "") const {
        const Value* v = get(key);
        return (v && !v->is_node()) ? v->str : def;
    }
    std::vector<const Node*> getall(const std::string& key) const {
        std::vector<const Node*> out;
        for (auto& p : kv) if (p.first == key && p.second.is_node()) out.push_back(p.second.node.get());
        return out;
    }
    // bare (keyless) leaf values in a block, e.g. members={ 1 2 3 }
    std::vector<std::string> values() const {
        std::vector<std::string> out;
        for (auto& p : kv) if (p.first.empty() && !p.second.is_node()) out.push_back(p.second.str);
        return out;
    }
};

inline std::string strip_comments(const std::string& text) {
    std::string out; out.reserve(text.size());
    bool inq = false, cut = false;
    for (char ch : text) {
        if (ch == '\n') { inq = false; cut = false; out.push_back(ch); continue; }
        if (cut) continue;
        if (ch == '"') inq = !inq;
        else if (ch == '#' && !inq) { cut = true; continue; }
        out.push_back(ch);
    }
    return out;
}

inline std::vector<std::string> tokenize(const std::string& text) {
    std::string s = strip_comments(text);
    std::vector<std::string> toks;
    size_t i = 0, n = s.size();
    auto isspace_ = [](char c) { return c == ' ' || c == '\t' || c == '\r' || c == '\n' || c == '\f' || c == '\v'; };
    while (i < n) {
        char c = s[i];
        if (isspace_(c)) { i++; continue; }
        if (c == '"') {
            size_t j = s.find('"', i + 1);
            if (j == std::string::npos) j = n - 1;
            toks.push_back(s.substr(i, j - i + 1));
            i = j + 1;
        } else if (c == '{' || c == '}' || c == '=') {
            toks.push_back(std::string(1, c)); i++;
        } else {
            size_t j = i;
            while (j < n && !isspace_(s[j]) && s[j] != '{' && s[j] != '}' && s[j] != '=') j++;
            toks.push_back(s.substr(i, j - i));
            i = j;
        }
    }
    return toks;
}

inline std::string unquote(const std::string& t) {
    if (t.size() >= 2 && t.front() == '"' && t.back() == '"') return t.substr(1, t.size() - 2);
    return t;
}

inline std::unique_ptr<Node> parse(const std::string& text) {
    std::vector<std::string> toks = tokenize(text);
    size_t pos = 0;
    // mirrors pdx.py parse_block: '=' skipped standalone; '{' after key opens block;
    // bare '{' opens an anonymous block; bare token is an array element.
    std::function<std::unique_ptr<Node>()> parse_block = [&]() -> std::unique_ptr<Node> {
        auto node = std::make_unique<Node>();
        while (pos < toks.size()) {
            const std::string& t = toks[pos];
            if (t == "}") { pos++; return node; }
            if (t == "=") { pos++; continue; }
            if (t == "{") {
                pos++;
                Value v; v.node = parse_block();
                node->kv.emplace_back("", std::move(v));
                continue;
            }
            std::string key = unquote(t);
            pos++;
            if (pos < toks.size() && toks[pos] == "=") {
                pos++;
                if (pos < toks.size() && toks[pos] == "{") {
                    pos++;
                    Value v; v.node = parse_block();
                    node->kv.emplace_back(std::move(key), std::move(v));
                } else {
                    Value v; v.str = unquote(toks[pos]);
                    node->kv.emplace_back(std::move(key), std::move(v));
                    pos++;
                }
            } else {
                Value v; v.str = key;
                node->kv.emplace_back("", std::move(v));
            }
        }
        return node;
    };
    return parse_block();
}

} // namespace pdx
