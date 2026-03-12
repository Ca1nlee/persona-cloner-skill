# Memory Injection Spec

Use this file to decide what belongs in `MEMORY.md` and how it should be versioned.
Memory is for durable persona continuity, not random trivia.

## 1. Admission rule
Promote a memory candidate only if all are true:
- removing it would make future decisions less faithful
- it changes behavior, prioritization, or refusal patterns
- evidence is **Strong** or tightly scoped **Moderate**
- it is durable across time, or explicitly scoped by time/context
- it does not imply private continuity or hidden access

## 2. What MEMORY.md should contain

### 1. Stable facts
Only include durable, reusable facts such as:
- public biography points that affect self-modeling
- long-running projects or affiliations
- recurring relationships or reference figures
- known preferences that change decisions

### 2. Pattern memories
Include recurring examples that teach the persona package how the person reasons:
- canonical stories
- favorite examples
- recurring contrasts
- go-to critiques

### 3. Boundary memories
Include durable refusals and identity lines:
- topics they avoid claiming
- private areas they never pretend to know
- values they will not trade away casually

## 3. What MEMORY.md should not contain
- one-off hot takes
- speculative psychology
- private or leaked information
- large copyrighted passages
- temporary plans
- weakly inferred biographical trivia

## 4. Candidate workflow
1. add candidate to `memory/candidates.jsonl`
2. mark conflict metadata if it overlaps an existing entry
3. decide merge strategy: `keep_both_scoped`, `replace_old`, or `reject`
4. snapshot `MEMORY.md`
5. append accepted change to `memory/CHANGELOG.md`
6. only then promote into `MEMORY.md`

Use the helper script:

```bash
python scripts/manage_persona_memory.py add --root <package-dir> --id MEM-0001 --type fact --claim "..." --behavioral-impact "..." --evidence-level Strong --source-ids S1,S2 --durable
python scripts/manage_persona_memory.py apply --root <package-dir> --id MEM-0001
```

## 5. Conflict handling
When a new candidate conflicts with existing durable memory:
- `keep_both_scoped`: preserve both entries and add date/context boundaries
- `replace_old`: keep new entry, but preserve history in changelog and snapshot
- `reject`: keep candidate in the log for audit, but do not promote

Rule: never silently overwrite durable memory.

## 6. Memory entry schema

```markdown
### MEM-0001 - [short claim]
- Type: fact / preference / example / relationship / refusal / boundary
- Why it matters behaviorally:
- Evidence level:
- Source IDs:
- Conflict note:
- Version note:
```

## 7. Principle
A memory entry is justified only if it improves long-horizon behavioral fidelity.
If it merely decorates the biography, keep it out.
