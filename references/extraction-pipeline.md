# Extraction Pipeline

Use this reference when converting source material into persona files.
The rule is simple: **every shipped claim must be traceable to reviewed source material.**

## 1. Pipeline stages
1. inventory sources in `01-source-pack/sources.csv`
2. create one worksheet per source in `01-source-pack/worksheets/`
3. extract signals for five target layers
4. merge only evidence-backed claims in `02-extraction/master-merge.md`
5. promote merged claims into package files

## 2. The five required target layers
Every source worksheet must extract evidence for:
- persona core
- worldview map
- decision rules
- contradiction handling
- memory injection candidates

## 3. Worksheet rule
A worksheet is not a summary.
It must produce behaviorally useful claims, including:
- what the source reveals
- what behavior it predicts
- what caveat or contradiction remains
- whether the claim is strong enough to promote

## 4. Merge rule
Promote only claims that are:
- repeated
- explicit enough to change future behavior
- scoped when time/context matters
- tagged with evidence level and source IDs

## 5. Promotion rule by file
- `references/persona-core.md`: stable temperament, motivation, identity anchors, boundary instincts
- `references/worldview-map.md`: beliefs, values, lenses, non-negotiables
- `references/decision-rules.md`: heuristics, default tradeoffs, reversal conditions, stress behavior
- `references/contradiction-handling.md`: tensions, time evolution, honest ambiguity
- `MEMORY.md`: durable entries only

## 6. Helper script
Use:

```bash
python scripts/extract_persona_pipeline.py "Target Name" --workspace <package-dir>
```

If `sources.csv` changes later, sync missing worksheets with:

```bash
python scripts/extract_persona_pipeline.py "Target Name" --workspace <package-dir> --sync
```

## 7. Failure mode to avoid
Do not jump from source quotes straight to polished persona prose.
That produces style mimicry, not an inspectable persona package.
