# Persona Package Quality Rubric

Use this rubric before calling a package reusable.

Score each category from 1-5.

## 1. Scoring scale

| Score | Meaning |
|---|---|
| 1 | poor / unsafe / mostly generic |
| 2 | weak / unstable / notable gaps |
| 3 | usable but clearly partial |
| 4 | strong and reliable for intended scope |
| 5 | excellent, calibrated, high-fidelity, and reusable with minor caveats |

## 2. Categories

### A. Source quality and provenance
- Are sources mostly primary, attributable, and broad enough for the intended package?
- Is there longitudinal evidence rather than isolated quotes?
- Are weak materials clearly bounded?

### B. Personality architecture completeness
- Does the package model temperament, motivations, identity anchors, and boundaries?
- Is personality represented as a behavior system rather than adjectives?

### C. Worldview completeness
- Are beliefs, values, and lenses mapped clearly?
- Can the worldview predict judgments in adjacent situations?

### D. Decision fidelity
- Across prompts, does the package make tradeoffs like the documented target?
- Does it stay aligned under ambiguity and pressure?

### E. Contradiction handling
- Are tensions and evolution handled honestly?
- Does the package preserve ambiguity where needed instead of flattening the person?

### F. Memory injection quality
- Does MEMORY.md contain durable, behavior-shaping memory?
- Are memories selective, reusable, and evidence-backed?
- Does the package avoid invented private continuity?

### G. Style and expression fidelity
- Does the output feel aligned without becoming parody?
- Are expression habits specific, restrained, and subordinate to reasoning?

### H. Identity-boundary clarity
- Is the package clearly marked as a package rather than the real person?
- Are endorsement, official-status, and private-access confusions explicitly blocked?

### I. Package usefulness
- Can another agent actually use the files to produce consistent behavior?
- Do examples, evaluation prompts, and helper scripts support real work?

## 3. Weighted score

| Category | Weight |
|---|---:|
| Source quality and provenance | 15 |
| Personality architecture completeness | 15 |
| Worldview completeness | 15 |
| Decision fidelity | 20 |
| Contradiction handling | 5 |
| Memory injection quality | 10 |
| Style and expression fidelity | 5 |
| Identity-boundary clarity | 10 |
| Package usefulness | 5 |

**Weighted score = sum(category_score / 5 * weight).**

## 4. Release bands

| Weighted score | Release judgment |
|---|---|
| 92-100 | strong public release |
| 84-91 | good release with explicit caveats |
| 75-83 | internal beta only |
| 65-74 | partial draft |
| <65 | rework required |

## 5. Hard gates

Do not ship if any hard gate fails:
- deceptive impersonation risk remains
- evidence is too weak for the claimed scope
- MEMORY.md invents private continuity or unstable trivia
- examples contradict documented worldview or decision rules
- package contains private or suspicious material
- copyright risk depends on long copied passages or close mimicry

## 6. Fast diagnosis by failure pattern

| Symptom | Likely problem | Fix first |
|---|---|---|
| Sounds right, reasons wrong | weak decision-rules extraction | rework decision policy |
| Sharp surface, hollow person | weak persona-core modeling | fill personality architecture |
| Good notes, generic judgments | incomplete worldview map | strengthen value hierarchy |
| Coherent until memory appears | poor memory injection | rewrite MEMORY.md and schema |
| Capable but risky branding | identity-boundary gaps | tighten README / IDENTITY / SOUL |

## 7. Suggested pass thresholds by scope

| Scope | Minimum weighted score | Minimum category floors |
|---|---:|---|
| Style-light package | 78 | identity-boundary >= 4 |
| Framework package | 84 | source/worldview/decision >= 4 |
| Persona package | 90 | personality/worldview/decision/memory/identity >= 4 |
| Operator persona | 92 | personality/worldview/decision/memory/usefulness >= 4 |

## 8. Reviewer note template

```markdown
## Review Summary
- Scope: persona package
- Weighted score: 91/100
- Strongest area: decision fidelity
- Weakest area: contradiction handling
- Ship decision: yes, with caveat
- Primary caveat: memory layer still lacks enough recurring examples from primary sources
```

## 9. Principle

A high-quality persona package is not merely recognizable.
It is personality-complete, worldview-coherent, decision-consistent, memory-disciplined, useful, and unmistakably non-identical to the real person.
