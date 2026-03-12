# Persona Cloner

<div align="center">

Build an OpenClaw-ready **public-figure persona package** from documented public materials.

<p>
  <strong>English</strong> |
  <a href="./README.zh-CN.md">简体中文</a>
</p>

<p>
  <a href="./README.md">Home</a> •
  <a href="#what-this-skill-does">What it does</a> •
  <a href="#when-to-use-it">Use cases</a> •
  <a href="#default-deliverables">Outputs</a> •
  <a href="#install">Install</a> •
  <a href="#validate">Validate</a> •
  <a href="#safety-boundary">Safety boundary</a>
</p>

</div>

---

## What this skill does

`persona-cloner` turns public interviews, speeches, writing, and other documented materials into a directly runnable OpenClaw persona package.

The package is designed to answer as a specific public figure while keeping hard boundaries around evidence, uncertainty, and behavior.

The default product is the runtime package itself, not a verbose extraction archive.

## When to use it

Use this skill when you want to:

- build a runnable agent package for a public figure
- preserve voice, judgment patterns, and decision style
- ship a package that stays concise, verdict-first, and resistant to generic assistant drift
- keep source boundaries explicit without turning every answer into a disclaimer

## Default deliverables

A normal successful output is a compact persona package containing:

- `SOUL.md`
- `IDENTITY.md`
- `AGENTS.md`
- `MEMORY.md`
- optional: `README-agent.md`
- optional: installation into an OpenClaw workspace

Supporting materials in this repository also include:

- `references/` for workflow, output spec, source boundaries, and evaluation guidance
- `scripts/` for scaffolding, validation, evaluation, installation, and memory management
- `examples/` for a sample package layout

## Install

### Install as an OpenClaw skill

1. Copy this repository folder into your OpenClaw `skills/` directory as `persona-cloner`.
2. Restart or reload OpenClaw if your setup requires it.
3. Ask for a public-figure persona package built from public materials.

### Use the helper scripts directly

```bash
python scripts/scaffold_persona_clone.py "Target Name" --out ./build --mode persona
python scripts/install_runtime_agent.py ./build/target-name-persona <target-workspace>
```

## Validate

### Validate the package structure

```bash
python scripts/validate_persona_package.py ./build/target-name-persona
```

### Run runtime behavior evaluation

```bash
python scripts/eval_runtime_behavior.py run --package-dir ./build/target-name-persona --version candidate
```

### What validation is checking

The repository tooling focuses on whether the package:

- includes the required runtime files
- keeps source boundaries clear
- avoids foregrounding clone-style self-labels in runtime voice
- contains output-discipline rules such as verdict-first structure and anti-lecture behavior
- preserves evidence trace, evaluation files, and memory versioning rails where required

## Repository structure

```text
persona-cloner-skill/
├─ SKILL.md
├─ README.md
├─ README.en.md
├─ README.zh-CN.md
├─ references/
├─ scripts/
└─ examples/
```

## Safety boundary

This repository is for persona packages built from **public materials**.

It does **not** grant:

- private memory
- secret access
- backstage knowledge
- endorsement
- official authority
- live affiliation with the target person

If the public record is thin, the package should say so plainly.

Unknowns should stay unknown.
