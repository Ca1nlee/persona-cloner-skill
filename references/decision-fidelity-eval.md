# Decision Fidelity Eval

Use this reference to compare two persona versions on the same prompt set.
The goal is not “which answer sounds cooler.”
The goal is: **which version behaves more like the documented person under tradeoff pressure.**

## 1. Eval assets
Use:
- `eval/cases.json` as the canonical prompt suite
- `eval/rubric.md` as the scoring rule
- `eval/runs/<run-id>/responses/<version>/` for captured outputs
- `eval/runs/<run-id>/regression-report.md` for the version comparison

## 2. Required dimensions
Score every case from 1-5 on:
- `persona_alignment`
- `worldview_alignment`
- `decision_alignment`
- `contradiction_handling`
- `memory_discipline`
- `boundary_clarity`

## 3. Required case coverage
The prompt set must cover at least:
- decision tradeoff
- worldview under pressure
- contradiction / time evolution
- memory use
- identity boundary / refusal

## 4. Comparison workflow
Initialize:

```bash
python scripts/eval_decision_fidelity.py init --eval-dir <package-dir>/eval --baseline v1 --candidate v2
```

Then:
1. run both versions on all cases
2. paste outputs into the generated response stubs
3. assign scores and notes for each version
4. compare:

```bash
python scripts/eval_decision_fidelity.py compare --eval-dir <package-dir>/eval --baseline v1 --candidate v2 --run-id <run-id>
```

## 5. Regression rule
Reject candidate `v2` if any of these happen:
- decision logic becomes more generic
- value hierarchy becomes less recognizable
- contradiction handling gets flatter or over-confident
- memory use becomes more theatrical or private-seeming
- boundary clarity weakens

## 6. What to patch when scores fall
- low `decision_alignment` -> rewrite `references/decision-rules.md`
- low `worldview_alignment` -> strengthen `references/worldview-map.md`
- low `contradiction_handling` -> improve `references/contradiction-handling.md`
- low `memory_discipline` -> prune and re-version `MEMORY.md`
- low `boundary_clarity` -> tighten `SOUL.md`, `IDENTITY.md`, `AGENTS.md`

## 7. Principle
A better persona package is one whose choices get harder to distinguish from the documented target's judgment system.
Voice imitation without decision fidelity does not count as progress.
