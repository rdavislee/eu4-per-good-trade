# -*- coding: utf-8 -*-
import io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "overrides.json")
ov = json.load(io.open(p, encoding="utf-8"))
IMPL = ("Rechecked personally against the implementation rather than the document's restatement. "
        "`solver.py`'s wealth path is exactly `tax = TAX_COEFF * base_tax * (1 + tmod)` (line 158) with "
        "`tmod` drawn from `STATE_TAX_MOD`, which is `{}` (line 89), plus `prod_income = gp * price` "
        "(line 159) where `gp = GP_COEFF * base_production * (1 + sum of the four province-state goods "
        "modifiers)`. A tree-wide grep of `solver.py` for autonomy, production efficiency, ideas, "
        "estates, government reforms and technology finds no occurrence anywhere on that path; `owner` "
        "appears only as an inclusion filter at line 144 (\"Counts a province when it has an owner and "
        "lies in a trade node\"). There is no modifier classifier left to police. Fresh run: "
        "`round6.py` prints `solver.LIVE_STATE_MODS = ('devastation',)` and "
        "`solver.STATE_TAX_MOD = {} (empty: no modifier reaches the tax term)`, and `verify6.py` "
        "asserts behaviourally that \"0 of 2472 counted provinces disagree with TAX_COEFF*base_tax\".")
ov.update({
"Y001": {"claim": "v6.0 makes owner-agnosticism true by construction rather than by a rule that has to be policed",
         "verdict": "CONFIRMED", "method": "file read (`solver.py` wealth path) + measurement (`round6.py`, `verify6.py`)",
         "ev": IMPL},
"Y002": {"claim": "The substantive change of v6.0 is to SS1.3: wealth is a function of the province's development, its trade good and its own current condition, and of nothing else",
         "verdict": "CONFIRMED", "method": "file read (`solver.py` wealth path) + measurement (`round6.py`, `verify6.py`)",
         "ev": IMPL + " The three inputs the path reads are precisely base_tax/base_production (development), price(good(p)) (the trade good) and the four static condition modifiers."},
"Y003": {"claim": "The two-test modifier classifier and everything it governed - trade-good modifiers, great projects, permanent province modifiers, buildings, centres of trade and DLC conditionality - are deleted, along with the whole-install sweep that maintained them",
         "verdict": "CONFIRMED", "method": "file read (`solver.py`, `apparatus6.py`; tree-wide search for the sweep script)",
         "ev": IMPL + " The deleted classifier's constants survive only in `apparatus6.py`, held frozen and imported by `measure6.py` purely to price what was removed (105.30 ducats over 89 provinces); nothing in the wealth path reads them. The whole-install sweep script `audit_modifiers.py` exists only under `../v4-owner-agnostic/scripts/` and has no counterpart in this tree."},
})
json.dump(ov, io.open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("overrides:", len(ov))
