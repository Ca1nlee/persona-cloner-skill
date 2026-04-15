---
name: persona-cloner
description: "Build an OpenClaw-ready public-figure persona package from public materials. Use when the user wants a directly runnable agent that answers as a specific person. Delivers runtime files (SOUL.md, IDENTITY.md, AGENTS.md, MEMORY.md) with behavioral controls to resist generic assistant voice drift."
user-invocable: true
triggers:
  - clone this persona
  - create an agent that talks like
  - build a persona for
  - make an AI version of
  - persona package for
  - public figure persona
  - create a persona agent
  - replicate this person's style
---

# Persona Cloner

Build the **runtime persona package first**.

Default user-facing output:
- `SOUL.md`
- `IDENTITY.md`
- `AGENTS.md`
- `MEMORY.md`
- optional: `README-agent.md`
- optional: install into an OpenClaw workspace

Do **not** make the internal extraction rail the product unless the user explicitly asks for provenance, evaluation history, or maintenance internals.

Read references only when needed:
- `references/workflow.md`
- `references/output-spec.md`
- `references/output-discipline.md`
- `references/acceptance-checklist.md`
- `references/source-intake.md`
- `references/persona-core.md`
- `references/worldview-map.md`
- `references/decision-rules.md`
- `references/contradiction-handling.md`
- `references/memory-injection-spec.md`
- `references/identity-boundary-statement.md`
- `references/decision-fidelity-eval.md`
- `references/behavior-eval.md`

Use scripts as internal helpers:
- `scripts/scaffold_persona_clone.py`
- `scripts/extract_persona_pipeline.py`
- `scripts/eval_decision_fidelity.py`
- `scripts/eval_runtime_behavior.py`
- `scripts/manage_persona_memory.py`
- `scripts/validate_persona_package.py`
- `scripts/install_runtime_agent.py`

## Deliverable rule

Default to the smallest honest package that can run well.

A normal successful delivery is:
- one folder containing `SOUL.md`, `IDENTITY.md`, `AGENTS.md`, `MEMORY.md`
- optionally `README-agent.md`
- optionally an install step using `scripts/install_runtime_agent.py`

## Core requirement

Every shipped runtime must contain explicit output-discipline rules:
- response length policy
- verdict-first policy
- expansion only on demand
- anti-lecture policy
- anti-assistant-tone policy
- bluntness / restraint tuning

Put these controls into the runtime artifacts themselves, mainly `SOUL.md` and `AGENTS.md`.

## Commands

```bash
python scripts/scaffold_persona_clone.py "Target Name" --out <output-dir> --mode persona
python scripts/install_runtime_agent.py <built-agent-dir> <target-workspace>
python scripts/validate_persona_package.py <package-dir>
python scripts/eval_runtime_behavior.py run --package-dir <package-dir> --version candidate --model sub2api/gpt-5.4
```

## Final reminder

This skill is for shipping a usable OpenClaw persona package. Internal complexity is allowed, but the default output should stay minimal, runnable, honest, behaviorally disciplined, and hard to wash out with generic assistant tone.
