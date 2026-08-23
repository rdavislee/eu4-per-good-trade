#!/bin/bash
# Round-11 probe for the §1.12 trade-UI slice (Y421-Y426, Y1265-Y1266, Y1289-Y1309).
# Re-run against the EU4 install to reproduce every primary-source quote used in
# scripts/r11/A_*.md grading notes.

EU4="/c/Program Files (x86)/Steam/steamapps/common/Europa Universalis IV"

echo "=== mapicons.gui: trade_small_mapicon / trade_big_mapicon total_value ==="
grep -n "trade_small_mapicon\|trade_big_mapicon" "$EU4/interface/mapicons.gui"
grep -n "name = \"total_value\"" "$EU4/interface/mapicons.gui"

echo
echo "=== tradeinterface.gui: all *_value / income / node-window numeric fields ==="
grep -n "name.*=.*\".*\(value\|income\)" -i "$EU4/interface/tradeinterface.gui"

echo
echo "=== our_from_this occurrences ==="
grep -n "our_from_this" "$EU4/interface/tradeinterface.gui"

echo
echo "=== incoming_nodes_listbox / outgoing_nodes_listbox positions ==="
grep -n -A4 "name = \"incoming_nodes_listbox\"\|name = \"outgoing_nodes_listbox\"" "$EU4/interface/tradeinterface.gui"

echo
echo "=== TradeNodeLink widget body (should be: 1 button, 1 label) ==="
awk '/name = "TradeNodeLink"/{f=1} f{print} f && /^\t\}$/{exit}' "$EU4/interface/tradeinterface.gui"

echo
echo "=== localisation search for our_from_this / OUR_FROM_THIS ==="
grep -rli "our_from_this" "$EU4/localisation/" 2>/dev/null
echo "(no hits = no localisation key tied to the field name)"

echo
echo "=== trade goods count (for the 'thirty-field' figure) ==="
grep -c "^[a-z_]* = {" "$EU4/common/tradegoods/00_tradegoods.txt"
