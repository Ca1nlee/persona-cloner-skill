# Persona Cloner

<div align="center">

Build an OpenClaw-ready **public-figure persona package** from documented public materials.

<p>
  <a href="./README.zh-CN.md">简体中文</a> |
  <strong>English</strong>
</p>

<p>
  <a href="./README.en.md#what-this-skill-does">What it does</a> •
  <a href="./README.en.md#when-to-use-it">Use cases</a> •
  <a href="./README.en.md#default-deliverables">Outputs</a> •
  <a href="./README.en.md#install">Install</a> •
  <a href="./README.en.md#validate">Validate</a> •
  <a href="./README.en.md#safety-boundary">Safety boundary</a>
</p>

</div>

---

## Quick overview

`persona-cloner` helps an agent turn interviews, writing, speeches, and other public records into a directly runnable OpenClaw persona package.

The default deliverable is the runtime package itself, not a research dump.

### Default outputs

- `SOUL.md`
- `IDENTITY.md`
- `AGENTS.md`
- `MEMORY.md`
- optional: `README-agent.md`
- optional: installation into an OpenClaw workspace

### Best fit

Use this skill when you want a package that:

- answers in the first-person voice of a public figure
- preserves decision style, tone, and behavioral discipline
- stays grounded in public materials instead of invented private access
- resists generic assistant tone drift

### Quick start

```bash
python scripts/scaffold_persona_clone.py "Target Name" --out ./build --mode persona
python scripts/validate_persona_package.py ./build/target-name-persona
python scripts/eval_runtime_behavior.py run --package-dir ./build/target-name-persona --version candidate
```

### Read in your language

- English: [README.en.md](./README.en.md)
- 简体中文: [README.zh-CN.md](./README.zh-CN.md)

---

## Repository highlights

- `SKILL.md` — skill entry and operating rule
- `references/` — workflow, output spec, boundary, evaluation, and extraction guidance
- `scripts/` — scaffold, validate, evaluate, install, and memory helpers
- `examples/` — sample persona package structure

## Safety reminder

This repository is for persona packages built from public materials. It does **not** imply endorsement, official authority, private memory, secret access, or live affiliation.

Unknowns should stay unknown.
