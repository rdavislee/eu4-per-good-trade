// The tradenodes emitter (spec 2.4): generate 00_tradenodes.txt from the campaign start's
// Phi_w. Text-level surgery on the vanilla file so everything the mod does not own
// round-trips byte-faithfully (TESTING A3): only outgoing blocks, declaration order and end
// flags may differ; members/location/inland/color/ai flags/unrecognized keys are the original
// bytes untouched.
//
//   1. declaration order  = decreasing Phi_w marking order (sources first, ends last --
//      the engine's own convention, 0 violations by construction: every arc u->v has
//      order[v] < order[u], so u is emitted before v)
//   2. end=yes            = exactly the Phi_w sinks
//   3. link reversal      = move the outgoing block to the new source, reverse the path
//      token list, reverse the control PAIR list -- token reordering only, no float
//      reformatting
//   4. acyclicity is asserted BEFORE writing: the engine hard-crashes on a cyclic file
//      (EXCEPTION_STACK_OVERFLOW, spec 2.4), so an emitted cycle must never reach disk
#pragma once
#include <algorithm>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <vector>
#include "drain.h"
#include "gamedata.h"
#include "save.h"
#include "zipread.h"

namespace emit {

struct OutBlock {
    std::string raw;          // full span "\toutgoing={...}\n"
    std::string target;       // name= value
    std::vector<std::string> path_toks, control_toks;
};

struct NodeBlock {
    std::string name;
    std::string prefix;       // comments/blank lines preceding the block, kept attached
    std::string raw;          // full block "name={...}\n"
    std::vector<OutBlock> outgoing;
    std::vector<std::pair<size_t, size_t>> outgoing_spans;  // spans within raw
    std::pair<size_t, size_t> end_span{0, 0};               // "\tend=yes\n" span, len 0 if none
};

inline size_t match_brace_at(const std::string& s, size_t open) {
    int d = 0; bool inq = false;
    for (size_t k = open; k < s.size(); k++) {
        char c = s[k];
        if (c == '"') inq = !inq;
        else if (!inq) {
            if (c == '{') d++;
            else if (c == '}') { d--; if (d == 0) return k; }
        }
    }
    throw std::runtime_error("emit: unbalanced braces");
}

inline std::vector<std::string> block_tokens(const std::string& body) {
    std::vector<std::string> t;
    std::istringstream is(body);
    std::string x;
    while (is >> x) t.push_back(x);
    return t;
}

// parse the vanilla file into node blocks with outgoing/end spans located
inline std::vector<NodeBlock> parse_file(const std::string& text, std::string& head) {
    std::vector<NodeBlock> nodes;
    size_t pos = 0;
    std::string pending;
    head.clear();
    bool first = true;
    while (pos < text.size()) {
        // a node block starts at column 0: identifier={
        size_t ls = pos;
        size_t le = text.find('\n', ls);
        if (le == std::string::npos) le = text.size();
        std::string line = text.substr(ls, le - ls);
        size_t eq = line.find("={");
        bool is_node = !line.empty() && line[0] != '\t' && line[0] != '#' &&
                       eq != std::string::npos && eq > 0 &&
                       line.find_first_of(" \t") > eq;
        if (!is_node) {
            pending += text.substr(ls, le - ls + (le < text.size() ? 1 : 0));
            pos = le + 1;
            continue;
        }
        size_t open = text.find('{', ls);
        size_t close = match_brace_at(text, open);
        size_t bend = close + 1;
        if (bend < text.size() && text[bend] == '\n') bend++;
        NodeBlock nb;
        nb.name = line.substr(0, eq);
        if (first) { head = ""; first = false; }   // head stays empty; pending is the prefix
        nb.prefix = pending;
        pending.clear();
        nb.raw = text.substr(ls, bend - ls);
        // locate depth-1 outgoing blocks and the end=yes line inside raw
        size_t p = 0;
        while ((p = nb.raw.find("\n\toutgoing={", p)) != std::string::npos) {
            size_t o = nb.raw.find('{', p);
            size_t c = match_brace_at(nb.raw, o);
            size_t e = c + 1;
            if (e < nb.raw.size() && nb.raw[e] == '\n') e++;
            OutBlock ob;
            ob.raw = nb.raw.substr(p + 1, e - p - 1);   // spans "\toutgoing={...}\n"
            size_t nm = ob.raw.find("name=");
            if (nm == std::string::npos) throw std::runtime_error("outgoing without name");
            size_t ne = ob.raw.find('\n', nm);
            std::string nv = ob.raw.substr(nm + 5, ne - nm - 5);
            if (nv.size() >= 2 && nv.front() == '"') nv = nv.substr(1, nv.size() - 2);
            ob.target = nv;
            size_t pp = ob.raw.find("path={");
            if (pp != std::string::npos) {
                size_t po = ob.raw.find('{', pp);
                size_t pc = match_brace_at(ob.raw, po);
                ob.path_toks = block_tokens(ob.raw.substr(po + 1, pc - po - 1));
            }
            size_t cp = ob.raw.find("control={");
            if (cp != std::string::npos) {
                size_t co = ob.raw.find('{', cp);
                size_t cc = match_brace_at(ob.raw, co);
                ob.control_toks = block_tokens(ob.raw.substr(co + 1, cc - co - 1));
            }
            nb.outgoing_spans.push_back({p + 1, e - p - 1});
            nb.outgoing.push_back(std::move(ob));
            p = c;
        }
        size_t es = nb.raw.find("\n\tend=yes\n");
        if (es != std::string::npos) nb.end_span = {es + 1, 9};   // "\tend=yes\n"
        nodes.push_back(std::move(nb));
        pos = ls + (bend - ls);
    }
    return nodes;
}

// a reversed outgoing block in vanilla layout: token order reversed, tokens untouched
inline std::string reversed_block(const std::string& new_target, const OutBlock& ob) {
    std::string s = "\toutgoing={\n\t\tname=\"" + new_target + "\"\n";
    if (!ob.path_toks.empty()) {
        s += "\t\tpath={\n\t\t\t";
        for (auto it = ob.path_toks.rbegin(); it != ob.path_toks.rend(); ++it)
            s += *it + " ";
        s += "\n\t\t}\n";
    }
    if (!ob.control_toks.empty()) {
        if (ob.control_toks.size() % 2)
            throw std::runtime_error("emit: control list has odd token count");
        s += "\t\tcontrol={\n\t\t\t";
        for (size_t i = ob.control_toks.size(); i >= 2; i -= 2)
            s += ob.control_toks[i - 2] + " " + ob.control_toks[i - 1] + " ";
        s += "\n\t\t}\n";
    }
    s += "\t}\n";
    return s;
}

struct EmitResult {
    std::string text;
    int kept = 0, reversed = 0;
    std::vector<std::string> ends;
    int order_violations = 0;   // must be 0
};

// tn: parsed vanilla nodes (for indices); phi: the Phi_w solve on the same node order;
// vanilla_text: the shipped file's bytes
inline EmitResult generate(const gamedata::TradeNodes& tn, const drain::Result& phi,
                           const std::string& vanilla_text) {
    std::string head;
    std::vector<NodeBlock> blocks = parse_file(vanilla_text, head);
    if (blocks.size() != tn.order.size())
        throw std::runtime_error("emit: block count != node count");
    std::map<std::string, int> bidx;
    for (size_t i = 0; i < blocks.size(); i++) bidx[blocks[i].name] = int(i);

    // Phi_w directions per undirected edge
    std::set<std::pair<int, int>> dir(phi.directed.begin(), phi.directed.end());
    if (drain::has_cycle(tn.order.size(), phi.directed))
        throw std::runtime_error("emit: Phi_w contains a cycle -- refusing to emit "
                                 "(the engine hard-crashes on a cyclic file)");

    // per node: kept blocks (original order) + gained reversed blocks (by vanilla index)
    EmitResult er;
    std::vector<std::vector<std::string>> newout(blocks.size());
    struct Gain { int from_vidx; std::string text; };
    std::vector<std::vector<Gain>> gains(blocks.size());
    for (size_t bi = 0; bi < blocks.size(); bi++) {
        const NodeBlock& nb = blocks[bi];
        int a = tn.nidx.at(nb.name);
        for (const OutBlock& ob : nb.outgoing) {
            int b = tn.nidx.at(ob.target);
            if (dir.count({a, b})) {
                newout[bi].push_back(ob.raw);           // direction kept
                er.kept++;
            } else if (dir.count({b, a})) {
                Gain g{int(bi), reversed_block(nb.name, ob)};
                gains[bidx.at(ob.target)].push_back(g); // moves to the other endpoint
                er.reversed++;
            } else {
                throw std::runtime_error("emit: edge " + nb.name + "-" + ob.target +
                                         " undirected in Phi_w");
            }
        }
    }
    // ends: Phi_w sinks
    std::vector<int> od(tn.order.size(), 0);
    for (auto& [u, v] : phi.directed) od[u]++;
    std::set<std::string> ends;
    for (size_t i = 0; i < tn.order.size(); i++)
        if (od[i] == 0) ends.insert(tn.order[i]);
    er.ends.assign(ends.begin(), ends.end());

    // rebuild each block: original bytes with outgoing spans and end line replaced
    std::vector<std::string> rebuilt(blocks.size());
    for (size_t bi = 0; bi < blocks.size(); bi++) {
        const NodeBlock& nb = blocks[bi];
        std::sort(gains[bi].begin(), gains[bi].end(),
                  [](const Gain& x, const Gain& y) { return x.from_vidx < y.from_vidx; });
        // splice: walk raw, dropping outgoing spans and the end line, remembering where the
        // first outgoing block sat (or the members block) as the insertion anchor
        std::vector<std::pair<size_t, size_t>> cuts = nb.outgoing_spans;
        if (nb.end_span.second) cuts.push_back(nb.end_span);
        std::sort(cuts.begin(), cuts.end());
        size_t anchor = nb.outgoing_spans.empty()
                            ? std::string::npos
                            : nb.outgoing_spans.front().first;
        if (anchor == std::string::npos) {
            size_t m = nb.raw.find("\n\tmembers={");
            anchor = (m == std::string::npos) ? nb.raw.rfind("\n}") + 1 : m + 1;
        }
        std::string out;
        size_t p = 0;
        bool inserted = false;
        auto insert_payload = [&]() {
            for (auto& k : newout[bi]) out += k;
            for (auto& g : gains[bi]) out += g.text;
            inserted = true;
        };
        std::vector<std::pair<size_t, size_t>>::iterator ci = cuts.begin();
        while (p < nb.raw.size()) {
            if (p == anchor && !inserted) insert_payload();
            if (ci != cuts.end() && p == ci->first) {
                p += ci->second;                       // skip the cut span
                ++ci;
                continue;
            }
            // insert end=yes just before the final "}\n"
            out += nb.raw[p++];
        }
        if (!inserted) {
            // anchor sat inside a cut span; append before closing brace
            size_t cb = out.rfind("\n}");
            std::string payload;
            for (auto& k : newout[bi]) payload += k;
            for (auto& g : gains[bi]) payload += g.text;
            out.insert(cb + 1, payload);
        }
        if (ends.count(nb.name)) {
            size_t cb = out.rfind("\n}");
            out.insert(cb + 1, "\tend=yes\n");
        }
        rebuilt[bi] = nb.prefix + out;
    }

    // declaration order: decreasing Phi_w marking order
    std::vector<int> byorder;
    for (size_t i = 0; i < tn.order.size(); i++) byorder.push_back(int(i));
    std::sort(byorder.begin(), byorder.end(), [&](int x, int y) {
        return phi.order.at(x) > phi.order.at(y);
    });
    er.text = head;
    for (int ni : byorder) er.text += rebuilt[bidx.at(tn.order[ni])];

    // self-check: re-parse and verify adjacency == Phi_w, order violations == 0
    {
        std::string h2;
        std::vector<NodeBlock> chk = parse_file(er.text, h2);
        std::map<std::string, int> declpos;
        for (size_t i = 0; i < chk.size(); i++) declpos[chk[i].name] = int(i);
        std::set<std::pair<int, int>> got;
        for (auto& nb : chk) {
            for (auto& ob : nb.outgoing) {
                got.insert({tn.nidx.at(nb.name), tn.nidx.at(ob.target)});
                if (declpos.at(ob.target) < declpos.at(nb.name)) er.order_violations++;
            }
        }
        if (got != dir)
            throw std::runtime_error("emit: re-parsed adjacency does not equal Phi_w");
        std::set<std::string> gotends;
        for (auto& nb : chk) {
            size_t es = nb.raw.find("\n\tend=yes\n");
            if (es != std::string::npos) gotends.insert(nb.name);
        }
        if (gotends != ends)
            throw std::runtime_error("emit: re-parsed end flags do not equal Phi_w sinks");
        if (er.order_violations)
            throw std::runtime_error("emit: declaration-order violations present");
    }
    return er;
}

} // namespace emit
