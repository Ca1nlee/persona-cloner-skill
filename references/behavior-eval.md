# Runtime Behavior Eval

Use this reference after the runtime files exist.
The goal is not to check file presence.
The goal is to check whether the generated agent **actually answers with the intended runtime discipline** instead of sliding back into generic base-model behavior.

## 1. What this eval is for

Use it to test whether the runtime agent is:
- verdict-first
- length-controlled
- resistant to lecture mode
- honest under uncertainty
- willing to expand only when asked
- free of generic assistant tone
- still recognizably consistent with the intended persona

This eval is about **behavior at answer time**.
It complements package validation and decision-fidelity evaluation.

## 2. Eval assets

Use:
- `eval/behavior-cases.json` as the canonical prompt suite
- `eval/behavior-rubric.md` as the scoring rule
- `eval/runs/<run-id>/behavior/<version>/` for captured outputs
- `eval/runs/<run-id>/behavior-report.md` for the scored result

## 3. Required case coverage

The suite must cover at least:
- ordinary judgment question -> test verdict-first
- long-explanation bait -> test anti-lecture and length control
- uncertainty question -> test uncertainty discipline
- follow-up question -> test expand-only-on-demand behavior
- assistant-tone trap -> test suppression of generic helper language

The default prompt set also checks persona consistency across the suite.

## 4. Required scoring dimensions

Score every case from 1-5 on:
- `length_control`
- `verdict_first`
- `anti_lecture`
- `uncertainty_discipline`
- `anti_assistant_tone`
- `persona_consistency`

## 5. Workflow

Default path: run the full loop in one command:

```bash
python scripts/eval_runtime_behavior.py run --package-dir <package-dir> --version candidate --model sub2api/gpt-5.4
```

What the script does automatically:
1. initializes `eval/behavior-cases.json` and `eval/behavior-rubric.md` if missing
2. creates a temporary OpenClaw agent bound to the target runtime package workspace
3. runs every prompt in `eval/behavior-cases.json` against the real runtime agent
4. stores raw captured answers in `eval/runs/<run-id>/behavior/<version>/`
5. applies heuristic scoring across the six dimensions
6. writes `eval/runs/<run-id>/behavior-report.md`
7. exits with `0` on PASS and `1` on FAIL

Optional lower-level commands still exist:

```bash
python scripts/eval_runtime_behavior.py init --eval-dir <package-dir>/eval --version candidate
python scripts/eval_runtime_behavior.py compare --eval-dir <package-dir>/eval --version candidate --run-id <run-id>
```

## 6. Pass / fail rule

Reject the runtime if any of these happen:
- any case average is below `4.0`
- any case has `verdict_first < 4`
- any case has `anti_assistant_tone < 4`
- the uncertainty case has `uncertainty_discipline < 4`
- the follow-up case has `anti_lecture < 4`
- the long-explanation bait case has `length_control < 4`
- any hard flag is triggered by the heuristic checks

Hard flags include:
- obvious assistant filler at the opening
- no clear answer up front on judgment questions
- fabricated certainty on the uncertainty case
- obvious over-expansion on the follow-up case

## 7. Heuristic layer

The script adds a small automatic check layer so the eval is not purely hand-wavy.
It does not replace human judgment.
It catches predictable failure modes such as:
- too many words for a short-answer case
- no direct answer in the opening lines
- assistant filler like "I'd be happy to", "it depends", "as an AI", "here's a breakdown"
- missing uncertainty markers when the prompt explicitly lacks evidence
- follow-up answers that become lectures instead of one controlled next layer

## 8. What to patch when scores fail

- low `length_control` -> tighten `SOUL.md` and `AGENTS.md` response ceilings
- low `verdict_first` -> rewrite opening-shape instructions in `AGENTS.md`
- low `anti_lecture` -> add stronger bans on preemptive teaching and backgrounding
- low `uncertainty_discipline` -> narrow claims and clarify unknown-handling rules in `SOUL.md`
- low `anti_assistant_tone` -> remove helper filler and customer-service phrasing from runtime instructions
- low `persona_consistency` -> fix persona core, worldview, and decision rules before voice polish

## 9. Principle

A runtime passes only if the delivered agent can survive a short prompt suite without immediately reverting to the default helpful-assistant voice.
Structure without behavior control does not count as done.
