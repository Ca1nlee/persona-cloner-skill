# Output Specification

## A. Default deliverable: runtime package

The normal output of this skill is a **minimal runnable OpenClaw persona package**.

```text
persona-name/
├── SOUL.md
├── IDENTITY.md
├── AGENTS.md
├── MEMORY.md
└── README-agent.md   # optional but recommended
```

If the user wants it installed immediately, also run:

```bash
python scripts/install_runtime_agent.py <built-agent-dir> <target-workspace>
```

## B. Runtime file intent

- `SOUL.md`: stable inner architecture, worldview, values, voice boundaries, output-discipline defaults
- `IDENTITY.md`: concise self-definition plus compact source boundary
- `AGENTS.md`: operating rules, priorities, refusal behavior, response style, response-shape controls
- `MEMORY.md`: durable, behavior-shaping memory only
- `README-agent.md`: short scope note, evidence basis, and runtime notes

## C. Mandatory runtime control layer

Every shipped runtime must include a control layer that resists generic assistant drift.
At minimum the package must specify:
- response length policy
- verdict-first policy
- expansion only on demand
- anti-lecture policy
- anti-assistant-tone policy
- bluntness / restraint tuning

Recommended placement:
- durable style defaults in `SOUL.md`
- operational response rules in `AGENTS.md`

## D. Internal build rail: optional

Use the larger package shape only when maintenance, traceability, or evaluation matters.

```text
persona-name/
├── SOUL.md
├── IDENTITY.md
├── AGENTS.md
├── MEMORY.md
├── README-agent.md
├── 01-source-pack/
├── 02-extraction/
├── eval/
├── memory/
├── references/
└── examples/
```

## E. Product rule

Do not force the internal rail into the user-facing deliverable by default.

Use this decision rule:
- **default**: ship the minimal runtime package
- **optional**: retain the internal rail for important or maintained personas

## F. Naming guidance

Prefer neutral names like:
- `[person]-agent`
- `[person]-persona`
- `[person]-runtime`

Avoid names that imply:
- official endorsement
- private access
- deception
- fake continuity claims
