# Source Intake and Evidence Scoring

Use this file to decide whether a clone has enough evidence to exist and how far it is allowed to generalize.

## 1. Purpose

Do not start from admiration. Start from observable material.

The source intake process exists to answer four questions:
1. Is the target public enough to model safely?
2. Is there enough first-party evidence to support a reusable clone?
3. Which claims are strong enough to operationalize?
4. Where must the clone stay narrow or explicitly uncertain?

## 2. Minimum intake standard

Require a usable source pack before writing high-confidence rules.

Recommended minimum by mode:

| Mode | Minimum viable source pack | Ship threshold |
|---|---|---|
| Style | 5-10 first-party items with enough language samples | Clear recurring tone and structure |
| Framework | 8-20 sources, including 2-5 long-form or deep interviews | Clear repeated worldview and decision logic |
| Operator | Framework threshold plus 3-8 workflow-relevant artifacts | Clear repeated operating methods, not just opinions |

A source pack is usually a mix of:
- essays / blog posts / letters
- interviews / podcasts / talks
- threads / short posts with recurrence over time
- product essays / founder letters / public memos
- user-provided lawful excerpts with permission

## 3. Source priority ladder

Score sources by provenance first.

1. **Tier A — Primary long-form**
   - books/excerpts the user lawfully provides
   - blog posts, essays, letters, public memos, transcripts written or spoken by the target
   - long interviews where the target explains beliefs and tradeoffs
2. **Tier B — Primary short-form**
   - tweets, threads, public posts, Q&A replies, short clips
3. **Tier C — Faithful primary archives**
   - trustworthy transcripts, mirrors, archives of primary material
4. **Tier D — Secondary interpretation**
   - profiles, summaries, explainers, commentary
5. **Tier E — Unacceptable / no-ship**
   - leaks, private messages, scraped private communities, anonymous dumps, unattributed quote graphics

Default rule: use Tier D only to find Tier A/B/C, not to define the clone.

## 4. Per-source scoring

Score each source on five dimensions. Use 0-2 on each dimension.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Provenance | weak / unclear / secondary | primary but partial | direct, attributable primary source |
| Depth | short or thin | medium | deep explanation, tradeoffs, examples |
| Recurrence | isolated | somewhat echoed elsewhere | repeated across time or formats |
| Actionability | vague inspiration | some usable principles | concrete rules, workflows, or decisions |
| Freshness / fit | outdated or off-domain | partially relevant | relevant to intended use case |

**Raw source score = sum (0-10).**

Interpretation:
- **9-10**: anchor source
- **7-8**: strong supporting source
- **5-6**: contextual source
- **0-4**: weak / do not lean on for defining behavior

## 5. Claim evidence scoring

Score claims, not just sources.

Every material claim in the framework extraction should be marked:

### Strong
Use when at least one is true:
- supported by 2+ independent high-quality first-party sources, or
- directly stated in one high-quality primary source and repeatedly expressed elsewhere in practice

Allowed usage:
- can shape SOUL.md and AGENTS.md defaults
- can appear as explicit decision rules
- can guide expected behavior in evaluation prompts

### Moderate
Use when:
- supported by one good primary source or several narrower signals
- likely true but not broad enough to universalize

Allowed usage:
- can appear in framework extraction with scope notes
- can inform examples and tendencies
- should not become absolute language

### Weak
Use when:
- inferred from sparse or ambiguous evidence
- stylistically visible but not repeated enough

Allowed usage:
- note only as tentative hypothesis
- never use as a defining behavioral rule

### Unknown
Use when:
- evidence is absent, contradictory, or too thin

Allowed usage:
- say unknown
- narrow the clone
- ask for more material if the user wants higher fidelity

## 6. Coverage map

Before shipping, ensure the evidence pack covers the layers below.

| Layer | Need to know | Evidence target |
|---|---|---|
| Positioning | who they are and what domain the clone addresses | 2+ strong signals |
| Worldview | repeated beliefs and mental models | 3+ strong/moderate claims |
| Goal function | what they optimize for | 2+ strong/moderate claims |
| Decision rules | how they resolve tradeoffs | 3+ examples across contexts |
| Style markers | voice, structure, rhetoric | enough direct language samples |
| Workflows | repeatable steps or methods | only if operator mode |
| Anti-patterns | what they reject | repeated refusals or critiques |
| Boundaries | what remains unknown or unsafe | explicit uncertainty notes |

If 2 or more core layers remain weak, downgrade the clone mode or stop.

## 7. Stop / downgrade rules

Stop or narrow immediately when:
- the person is not sufficiently public
- evidence is mostly commentary rather than primary material
- the target changes position so often that no stable core emerges
- the request would require large copyrighted mimicry or extensive close paraphrase
- the user asks for deceptive impersonation, endorsement, or official-looking branding

Fallback options:
- domain-inspired expert agent
- framework synthesis without persona naming in the speaking voice
- style-light assistant with explicit limits

## 8. Intake table template

Use or adapt this table inside the clone package.

| ID | Source | Type | Tier | Date | Raw Score /10 | Key coverage | Notes / cautions |
|---|---|---|---|---|---:|---|---|
| S1 | Example essay | blog post | A | 2024-01-10 | 9 | worldview, goal function | strong anchor |
| S2 | Example interview | podcast transcript | A | 2023-07-18 | 8 | tradeoffs, style | supporting |

## 9. Claim table template

| Claim | Evidence level | Source IDs | Scope note | Contradictions / evolution |
|---|---|---|---|---|
| "Prefer small teams with high agency" | Strong | S1, S2, S6 | applies to startup building | none noted |

## 10. Practical heuristics

Use these heuristics while extracting:
- repeated operating advice matters more than one elegant quote
- explicit tradeoffs matter more than branding slogans
- contradictions are signal, not noise; date them and narrow scope
- language tics without worldview are not enough for a framework clone
- workflow claims require examples of execution, not just opinion

## 11. Ship rule

Do not ask: "Can I imitate this person?"

Ask: "What useful behavior can I justify from public evidence, and with what confidence?"