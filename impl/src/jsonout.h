// Tiny JSON writer with shortest-round-trip double formatting (the C++ analogue of
// Python's repr), for the orientation dumps compare.py diffs against the reference.
#pragma once
#include <charconv>
#include <cstdio>
#include <string>
#include <vector>

namespace jsonout {

inline std::string fmt_double(double v) {
    char buf[64];
    auto res = std::to_chars(buf, buf + sizeof(buf), v);
    return std::string(buf, res.ptr);
}

inline std::string escape(const std::string& s) {
    std::string out;
    for (char c : s) {
        if (c == '"' || c == '\\') { out.push_back('\\'); out.push_back(c); }
        else if (c == '\n') out += "\\n";
        else out.push_back(c);
    }
    return out;
}

struct Writer {
    std::string buf;
    void raw(const std::string& s) { buf += s; }
    void str(const std::string& s) { buf += '"'; buf += escape(s); buf += '"'; }
    void num(double v) { buf += fmt_double(v); }
    void num(int v) { buf += std::to_string(v); }
    // key helpers for object contexts
    void key(const std::string& k) { str(k); buf += ':'; }
};

} // namespace jsonout
