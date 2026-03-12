# Persona Cloner Workflow

## Principle
Build inward, ship outward.
The runtime files are the product. The rest is support machinery.

## Fast path
Use this when the user mainly wants a working persona package.

1. Gather public materials.
2. Extract persona core, worldview, decision rules, voice habits, and durable memory.
3. Write `SOUL.md`, `IDENTITY.md`, `AGENTS.md`, and `MEMORY.md` with explicit anti-drift controls.
4. Add a compact source boundary.
5. Run behavior eval if the package is meant to be reused.
6. Hand off the runtime package.

## Full path
Use this when maintenance, auditability, or high-stakes release matters.

1. Scaffold the package.
2. Fill `references/` and source maps with real evidence.
3. Promote only stable findings into runtime files.
4. Keep `eval/` and `memory/` rails for regression and updates.
5. Validate.
6. Run runtime behavior eval.
7. Ship.

## Writing order
Recommended order:
1. `references/source-map.md`
2. `references/persona-core.md`
3. `references/worldview-map.md`
4. `references/decision-rules.md`
5. `SOUL.md`
6. `AGENTS.md`
7. `IDENTITY.md`
8. `MEMORY.md`
9. `README-agent.md`

## Runtime rules worth repeating
- First-person delivery is allowed and usually preferred.
- The runtime should not keep apologizing for existing.
- Put boundaries in the files, not in every answer.
- Ban generic assistant openings.
- Force verdict-first answers.
- Expand one layer at a time.
- Refuse fake private access.

## Commands

```bash
python scripts/scaffold_persona_clone.py "Target Name" --out <output-dir> --mode persona
python scripts/validate_persona_package.py <package-dir>
python scripts/eval_runtime_behavior.py run --package-dir <package-dir> --version candidate --model sub2api/gpt-5.4
```
