import re
doc = open("per-good-trade-spec.md", encoding="utf-8").read()

# A few plausible "what counts as a numeric token" delimitations.
patterns = {
    "bare digit runs (\d+)":            r"\d+",
    "digit runs incl decimals":          r"\d+(\.\d+)?",
    "digit runs incl decimals+commas":   r"[0-9][0-9,]*(\.[0-9]+)?",
    "digit runs incl sci/e-notation":    r"[0-9][0-9.,]*(?:e[+-]?[0-9]+)?",
    "digit runs w/ leading sign & pct":  r"[+-]?[0-9][0-9.,]*%?",
}
for name, pat in patterns.items():
    hits = re.findall(pat, doc)
    print("%-38s %d" % (name, len(hits)))
