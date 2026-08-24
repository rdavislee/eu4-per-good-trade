// Minimal ZIP reader with an RFC 1951 (deflate) decompressor -- EU4 non-ironman saves are
// ZIP archives whose entries (gamestate/meta/ai) are deflate-compressed EU4txt.
// Self-contained: no zlib dependency. Verified against Python's zipfile on the readable saves
// (see impl selftest-zip).
#pragma once
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#include <fstream>
#include <stdexcept>

namespace zipread {

// ---------------------------------------------------------------- inflate ----
class Inflater {
public:
    // src: raw deflate stream. Returns decompressed bytes.
    static std::string inflate(const uint8_t* src, size_t n) {
        Inflater z(src, n);
        z.run();
        return std::move(z.out_);
    }

private:
    const uint8_t* src_; size_t n_;
    size_t pos_ = 0;       // byte position
    uint32_t bitbuf_ = 0; int bitcnt_ = 0;
    std::string out_;

    Inflater(const uint8_t* src, size_t n) : src_(src), n_(n) {}

    uint32_t bits(int count) {
        while (bitcnt_ < count) {
            if (pos_ >= n_) throw std::runtime_error("inflate: out of input");
            bitbuf_ |= uint32_t(src_[pos_++]) << bitcnt_;
            bitcnt_ += 8;
        }
        uint32_t v = bitbuf_ & ((1u << count) - 1);
        bitbuf_ >>= count; bitcnt_ -= count;
        return v;
    }

    struct Huff {
        // canonical Huffman decode tables: counts per length, symbols sorted
        std::vector<int> counts;   // counts[len]
        std::vector<int> symbols;  // symbols in canonical order
        void build(const std::vector<int>& lengths, int maxsym) {
            counts.assign(16, 0);
            for (int i = 0; i < maxsym; i++) counts[lengths[i]]++;
            counts[0] = 0;
            std::vector<int> offs(16, 0);
            for (int l = 1; l < 16; l++) offs[l] = offs[l - 1] + counts[l - 1];
            symbols.assign(maxsym, 0);
            for (int i = 0; i < maxsym; i++)
                if (lengths[i]) symbols[offs[lengths[i]]++] = i;
        }
    };

    int decode(const Huff& h) {
        int code = 0, first = 0, index = 0;
        for (int len = 1; len < 16; len++) {
            code |= int(bits(1));
            int count = h.counts[len];
            if (code - first < count) return h.symbols[index + (code - first)];
            index += count;
            first = (first + count) << 1;
            code <<= 1;
        }
        throw std::runtime_error("inflate: bad huffman code");
    }

    void stored_block() {
        bitbuf_ = 0; bitcnt_ = 0;                     // discard to byte boundary
        if (pos_ + 4 > n_) throw std::runtime_error("inflate: stored header");
        unsigned len = src_[pos_] | (src_[pos_ + 1] << 8);
        pos_ += 4;                                    // skip LEN + NLEN
        if (pos_ + len > n_) throw std::runtime_error("inflate: stored data");
        out_.append(reinterpret_cast<const char*>(src_ + pos_), len);
        pos_ += len;
    }

    void codes(const Huff& lencode, const Huff& distcode) {
        static const int lbase[] = {3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258};
        static const int lext[]  = {0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0};
        static const int dbase[] = {1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577};
        static const int dext[]  = {0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13};
        for (;;) {
            int sym = decode(lencode);
            if (sym < 256) { out_.push_back(char(sym)); continue; }
            if (sym == 256) return;
            sym -= 257;
            if (sym >= 29) throw std::runtime_error("inflate: bad length symbol");
            int len = lbase[sym] + int(bits(lext[sym]));
            int dsym = decode(distcode);
            if (dsym >= 30) throw std::runtime_error("inflate: bad distance symbol");
            size_t dist = size_t(dbase[dsym]) + bits(dext[dsym]);
            if (dist > out_.size()) throw std::runtime_error("inflate: distance too far");
            size_t from = out_.size() - dist;
            for (int i = 0; i < len; i++) out_.push_back(out_[from + i]);  // may overlap
        }
    }

    void fixed_block() {
        std::vector<int> lens(288);
        for (int i = 0; i < 144; i++) lens[i] = 8;
        for (int i = 144; i < 256; i++) lens[i] = 9;
        for (int i = 256; i < 280; i++) lens[i] = 7;
        for (int i = 280; i < 288; i++) lens[i] = 8;
        Huff lc; lc.build(lens, 288);
        std::vector<int> dl(30, 5);
        Huff dc; dc.build(dl, 30);
        codes(lc, dc);
    }

    void dynamic_block() {
        static const int ord[] = {16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15};
        int nlen = int(bits(5)) + 257;
        int ndist = int(bits(5)) + 1;
        int ncode = int(bits(4)) + 4;
        std::vector<int> cl(19, 0);
        for (int i = 0; i < ncode; i++) cl[ord[i]] = int(bits(3));
        Huff clc; clc.build(cl, 19);
        std::vector<int> lens(nlen + ndist, 0);
        int i = 0;
        while (i < nlen + ndist) {
            int sym = decode(clc);
            if (sym < 16) lens[i++] = sym;
            else if (sym == 16) {
                if (i == 0) throw std::runtime_error("inflate: repeat with no prior");
                int prev = lens[i - 1], rep = 3 + int(bits(2));
                while (rep-- && i < nlen + ndist) lens[i++] = prev;
            } else if (sym == 17) { int rep = 3 + int(bits(3)); while (rep-- && i < nlen + ndist) lens[i++] = 0; }
            else { int rep = 11 + int(bits(7)); while (rep-- && i < nlen + ndist) lens[i++] = 0; }
        }
        Huff lc; lc.build(lens, nlen);
        std::vector<int> dlens(lens.begin() + nlen, lens.end());
        Huff dc; dc.build(dlens, ndist);
        codes(lc, dc);
    }

    void run() {
        for (;;) {
            int last = int(bits(1));
            int type = int(bits(2));
            if (type == 0) stored_block();
            else if (type == 1) fixed_block();
            else if (type == 2) dynamic_block();
            else throw std::runtime_error("inflate: bad block type");
            if (last) break;
        }
    }
};

// ------------------------------------------------------------------- zip -----
inline std::string read_file(const std::string& path) {
    std::ifstream f(path, std::ios::binary);
    if (!f) throw std::runtime_error("cannot open " + path);
    std::string s((std::istreambuf_iterator<char>(f)), std::istreambuf_iterator<char>());
    return s;
}

inline uint32_t rd32(const std::string& s, size_t off) {
    return uint32_t(uint8_t(s[off])) | uint32_t(uint8_t(s[off + 1])) << 8 |
           uint32_t(uint8_t(s[off + 2])) << 16 | uint32_t(uint8_t(s[off + 3])) << 24;
}
inline uint16_t rd16(const std::string& s, size_t off) {
    return uint16_t(uint8_t(s[off])) | uint16_t(uint8_t(s[off + 1])) << 8;
}

// Extract one named entry from a ZIP archive (compress type 0 or 8 only).
inline std::string zip_entry(const std::string& path, const std::string& want) {
    std::string s = read_file(path);
    if (s.size() < 22) throw std::runtime_error("not a zip: " + path);
    // find EOCD (scan back over a possible comment)
    size_t eocd = std::string::npos;
    size_t lo = s.size() >= 22 + 65535 ? s.size() - 22 - 65535 : 0;
    for (size_t i = s.size() - 22; ; i--) {
        if (rd32(s, i) == 0x06054b50) { eocd = i; break; }
        if (i == lo) break;
    }
    if (eocd == std::string::npos) throw std::runtime_error("zip: no EOCD in " + path);
    uint16_t nent = rd16(s, eocd + 10);
    size_t cd = rd32(s, eocd + 16);
    for (uint16_t e = 0; e < nent; e++) {
        if (rd32(s, cd) != 0x02014b50) throw std::runtime_error("zip: bad central header");
        uint16_t method = rd16(s, cd + 10);
        uint32_t csize = rd32(s, cd + 20);
        uint16_t nlen = rd16(s, cd + 28), xlen = rd16(s, cd + 30), clen = rd16(s, cd + 32);
        uint32_t lho = rd32(s, cd + 42);
        std::string name = s.substr(cd + 46, nlen);
        cd += 46 + nlen + xlen + clen;
        if (name != want) continue;
        if (rd32(s, lho) != 0x04034b50) throw std::runtime_error("zip: bad local header");
        uint16_t lnlen = rd16(s, lho + 26), lxlen = rd16(s, lho + 28);
        size_t data = lho + 30 + lnlen + lxlen;
        if (method == 0) return s.substr(data, csize);
        if (method == 8)
            return Inflater::inflate(reinterpret_cast<const uint8_t*>(s.data()) + data, csize);
        throw std::runtime_error("zip: unsupported method");
    }
    throw std::runtime_error("zip: entry not found: " + want);
}

} // namespace zipread
