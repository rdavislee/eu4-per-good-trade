import io,re
t=io.open("fixes-round11.md",encoding="utf-8").read()
rows=dict((m.group(1),m.group(3)) for m in re.finditer(r"^\| (A\d) \| ([^|]*) \| (.*?) \|$", t, re.M))
old={
"A1":"\u00a72.8's income-balance bullet: the reconstruction count corrected to what the instrument shows \u2014 the save-based reconstruction reproduces the engine's `local_value` **digit-for-digit on 57 of the 79 nodes that carry the field** (under \u00a71.3's truncation convention; `cape_of_good_hope` carries no field), and runs **3.4% low** in aggregate, the shortfall concentrated in New World nodes. \"58 of 80\" goes \u2014 both routes to it admit a node that fails the test it names. The same count in \u00a72.8's A8 sentence and any echo corrected together.",
"A2":"\u00a73.4's parenthetical: \"The aggregate graph reads neither quantity\" is corrected to what \u00a71.3's own note (added the same round) says \u2014 the aggregate reads **neither `V_g` nor production income**: `\u03a6_w` is built from \u00a71.3's wealth field, which carries \u00a71.3's `trade_value(p)` as a summand \u2014 the orientation-side quantity, not \u00a71.8's `inject`.",
"A4":"\u00a73.16 item 1's supersession clause marked as the inference it is: 1.16's L42 introduces States & Territories; that the system **supersedes** the 75% floor is an inference from the archive \u2014 territories carry autonomy in place of the overseas rule, and the floor appears in no later note \u2014 not a quoted sentence. The introduction quote (1.8 L40) stays verbatim.",
"A5":"\u00a71.12's `our_from_this` gloss marked at its source: \"read as the country's own take \u2014 an inference from the widget's name; no localisation key, tooltip or label sibling names it\".",
"A7":"**Spec edit, the \u00a71.9 treatment.** \u00a72.3's \"Treasure-fleet diversion and caravan power are both DLC-conditional\" is marked at its actual scope: the conditionality is **engine-side, named by no shipped file** (the adjacent sentence already documents the absence \u2014 no file gates the grant mechanic or the diversion), and **unprobed pending the `dlc_load.json` toggle run**. The readable-when-inert half and the key-on-the-flag design instruction are unchanged.",
}
for k in ("A1","A2","A4","A5","A7"):
    print("%s byte-identical to closed text : %s" % (k, rows.get(k)==old[k]))
a3=rows.get("A3",""); a6=rows.get("A6","")
print("A3 names Barcelona pid 213      :", "**Barcelona, pid 213**" in a3)
print("A3 keeps 57/79 and 245 cells    :", "57 of the 79 nodes that carry it" in a3 and "245 singleton (node, good) cells" in a3)
print("A6 covers item 19 preamble too  :", "\u00a72.7 item 19's own preamble" in a6)
print("rows present                    :", sorted(rows))
