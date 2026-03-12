# persona-cloner

Build an OpenClaw-ready **public-figure persona package** from documented public materials.

## English

### What this skill does
`persona-cloner` helps an agent turn public interviews, writing, speeches, and other documented material into a runnable OpenClaw persona package. The default deliverable is a compact runtime folder with `SOUL.md`, `IDENTITY.md`, `AGENTS.md`, and `MEMORY.md`.

### When to use it
Use this skill when you want an agent to answer in the style and decision frame of a public figure, while keeping clear source boundaries and avoiding generic assistant drift.

### What it outputs
- A runtime persona package
- Optional source and evaluation rails for traceability
- Optional installation into an OpenClaw workspace

### Install into OpenClaw
1. Copy this folder into your OpenClaw `skills/` directory as `persona-cloner`.
2. Restart or reload OpenClaw if your setup requires it.
3. Ask for a public-figure persona package built from public materials.

### Validate the skill and its output
- Scaffold a package: `python scripts/scaffold_persona_clone.py "Target Name" --out ./build --mode persona`
- Validate a package: `python scripts/validate_persona_package.py ./build/target-name-persona`
- Run behavior eval: `python scripts/eval_runtime_behavior.py run --package-dir ./build/target-name-persona --version candidate`

### Safety boundary
This repo is for persona packages built from public materials. It does **not** grant private memory, secret access, endorsement, or live authority. Unknowns should stay unknown.

## 中文

### 这个 skill 是做什么的
`persona-cloner` 用来把公开人物的访谈、文章、演讲等公开材料，整理成一个可直接运行的 OpenClaw persona package。默认产物是一个精简运行目录，包含 `SOUL.md`、`IDENTITY.md`、`AGENTS.md`、`MEMORY.md`。

### 适用场景
当你希望代理以某位公开人物的表达风格、判断框架和边界来回答问题，同时又要严格限定在公开资料范围内、避免泛化成默认助手口吻时，就使用这个 skill。

### 输出内容
- 一个可运行的 persona package
- 可选的来源整理与评测目录
- 可选的 OpenClaw 安装步骤

### 如何安装到 OpenClaw
1. 将本目录复制到 OpenClaw 的 `skills/` 目录，并命名为 `persona-cloner`。
2. 如果你的环境需要，重启或重新加载 OpenClaw。
3. 直接提出“基于公开资料构建某位人物 persona package”的任务即可。

### 如何验证
- 生成脚手架：`python scripts/scaffold_persona_clone.py "Target Name" --out ./build --mode persona`
- 校验产物：`python scripts/validate_persona_package.py ./build/target-name-persona`
- 运行行为评测：`python scripts/eval_runtime_behavior.py run --package-dir ./build/target-name-persona --version candidate`

### 安全边界
本仓库只面向基于公开资料构建 persona package 的场景，不代表真实本人，不提供私有记忆、秘密信息、授权背书或实时权限；未知信息必须明确保持未知。
