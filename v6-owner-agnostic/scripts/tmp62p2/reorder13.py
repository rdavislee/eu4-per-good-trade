import re, sys, io

path = "validation-v62-part2.md"
text = io.open(path, encoding="utf-8").read()
lines = text.split("\n")

start = next(i for i,l in enumerate(lines) if l.startswith("## §1.3"))
end = next(i for i,l in enumerate(lines) if l.startswith("## §1.4"))
section = lines[start:end]

# header is first 4 lines: "## §1.3...", "", "| ID | ...", "|---|...|"
header = section[:4]
rows = [l for l in section[4:] if l.strip().startswith("| Y")]
print("num rows found:", len(rows))

rowmap = {}
for r in rows:
    m = re.match(r"\|\s*(Y\d+)\s*\|", r)
    rowmap[m.group(1)] = r

# desired order (by document line number, computed earlier)
order = """255 Y277
257 Y028
258 Y278
258 Y279
260 Y029
262 Y280
264 Y030
268 Y031
269 Y032
274 Y033
275 Y034
278 Y1083
279 Y1084
281 Y1085
283 Y281
286 Y035
287 Y036
288 Y037
289 Y282
291 Y283
294 Y038
294 Y284
298 Y039
298 Y040
302 Y285
303 Y041
306 Y042
307 Y043
308 Y044
310 Y045
313 Y286
314 Y287
315 Y288
316 Y289
317 Y290
321 Y291
322 Y046
325 Y047
327 Y048
328 Y049
334 Y050
337 Y979
341 Y051
343 Y054
348 Y053
349 Y1086
352 Y1087
352 Y981
356 Y1088
358 Y1089
361 Y980
366 Y1090
369 Y984
373 Y1091
374 Y1092
377 Y1093
379 Y058
384 Y059
385 Y060
386 Y061
391 Y062
394 Y063
397 Y064
399 Y065
403 Y066
406 Y067
408 Y068
411 Y069
413 Y070
415 Y071
420 Y293
424 Y294
425 Y295
427 Y296
429 Y072
430 Y297
431 Y073
432 Y074
435 Y298
438 Y299
440 Y075""".strip().split("\n")

ids_order = [o.split()[1] for o in order]
print("desired count:", len(ids_order))
missing = [i for i in ids_order if i not in rowmap]
extra = [i for i in rowmap if i not in ids_order]
print("missing from rowmap:", missing)
print("extra in rowmap not in order:", extra)

new_rows = [rowmap[i] for i in ids_order]
new_section = header + new_rows + [""]
new_lines = lines[:start] + new_section + lines[end:]
io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(new_lines))
print("rewritten, new total rows in file section:", len(new_rows))
