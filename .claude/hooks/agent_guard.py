# -*- coding: utf-8 -*-
"""PreToolUse guard on Agent/Task launches for the per-good-trade audit loop.

Two jobs, both owner-directed (2026-08-22):

1. HARD BLOCK any subagent launch that would run on the fable model. An omitted `model` inherits
   the session model, and these sessions run ON fable -- so omission IS fable. `fork` inherits the
   parent model regardless of any override, so fork is blocked outright.

2. SURFACE THE PROMPTING RULES at launch time. On the first Agent call of each session the guard
   blocks once with the rules digest and asks for the identical call to be re-issued; on every
   model violation the digest rides along with the block. The full text lives in the auto-memory
   file `audit-agent-prompts-stay-broad.md`; the digest here is the checklist form.

Contract: exit 0 allows the call; exit 2 blocks it and feeds stderr back to the model.
Fails open on malformed input rather than wedging every launch.
"""
import json
import os
import sys

RULES = """MODEL LADDER (owner rule): every subagent runs exactly ONE tier below its launcher --
fable -> opus -> sonnet -> haiku. This session is fable, so top-level Agent calls set model "opus";
every brief must tell the agent its own children take the next tier down and to pass the ladder on.
Model is always explicit; fable and fork are always blocked.

PROMPTING RULES (digest of audit-agent-prompts-stay-broad.md -- reread it before launching):
- Method and format instructions stay. Findings instructions go. Never hint at what to find,
  which passages look suspect, or which rules to hunt (no R2/R3 hunts, no risk-ordered work).
- EXTRACTION (claims delta) = mechanical census: conventions, ID rules, columns, data-only
  report-back. NO inconsistency hunts, NO instrument-gap roll-ups, NO "anything that struck you".
  Per-row `unsourced` classification is in; aggregating it into a finding is out.
  Per the standing method it MAY receive: the frozen baseline and the mechanical diff.
- VALIDATION = empirical, per claim: claims + spec + install + saves + scripts; re-derive, never
  inherit; read files, not the document's quotes of them; run instruments; Status/Method/Evidence
  per claim. NO "check the repair is complete", NO quoted-retraction exemptions by fiat.
  It must NOT receive authorial artifacts: fixes lists, preconfirmation, applied-round notes.
- IMPLEMENTATION-CHECK (post-fix audit) is the ONE agent that gets the fix list AND the diff --
  that is its job, not contamination.
- Fan-out inside a subagent: children take the NEXT TIER DOWN (opus parent -> sonnet children ->
  haiku grandchildren), model always explicit, never fork, and the parent personally rechecks
  every REFUTED/PARTIAL a child returns before it lands.
- Report-backs ask for data (counts, IDs, verdicts), not impressions.
- Quarantine anything produced under a bad prompt; a mid-flight correction is not a re-run."""


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name", "") not in ("Agent", "Task"):
        return 0
    ti = data.get("tool_input") or {}
    model = ti.get("model")
    problems = []
    if ti.get("subagent_type") == "fork":
        problems.append("subagent_type 'fork' always inherits the parent model -- fable here. "
                        "Launch a fresh agent with an explicit model instead.")
    if model is None:
        problems.append("no `model` set. Omission inherits the session model, which is fable. "
                        "Set model explicitly (use \"opus\").")
    elif str(model).strip().lower() == "fable":
        problems.append("`model` is fable, which the owner has banned for subagents. Use \"opus\".")

    here = os.path.dirname(os.path.abspath(__file__))
    sid = "".join(c for c in str(data.get("session_id", "unknown"))[:64]
                  if c.isalnum() or c in "-_") or "unknown"
    marker = os.path.join(here, "_rules_shown_" + sid)

    if problems:
        sys.stderr.write("AGENT LAUNCH BLOCKED:\n- " + "\n- ".join(problems)
                         + "\n\n" + RULES + "\n")
        return 2

    if not os.path.exists(marker):
        try:
            with open(marker, "w") as f:
                f.write("shown")
        except OSError:
            pass
        sys.stderr.write("FIRST AGENT LAUNCH THIS SESSION -- not a violation (model is acceptable)."
                         " This one-time stop exists so the rules are in view at launch time."
                         " Re-issue the identical call to proceed.\n\n" + RULES + "\n")
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
