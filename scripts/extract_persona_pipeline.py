#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from textwrap import dedent


SOURCE_HEADERS = [
    "source_id",
    "title",
    "url_or_path",
    "type",
    "tier",
    "date",
    "provenance_score",
    "depth_score",
    "recurrence_score",
    "actionability_score",
    "fit_score",
    "coverage",
    "notes",
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def ensure_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(SOURCE_HEADERS)
        writer.writerow(["S1", "", "", "essay/interview/thread/post/transcript", "A/B/C/D", "", 0, 0, 0, 0, 0, "persona-core;worldview", ""])


def write_source_template(path: Path, source_id: str) -> None:
    write(
        path,
        dedent(
            f"""
            # {source_id} extraction worksheet

            ## Source metadata
            - Source ID: {source_id}
            - Title:
            - URL / Path:
            - Type:
            - Date:
            - Tier:
            - Reviewer:

            ## High-signal excerpts
            - Excerpt 1:
            - Excerpt 2:
            - Excerpt 3:

            ## Structured extraction
            ### Persona core signals
            - temperament:
            - motivational engine:
            - identity anchors:
            - boundary instincts:

            ### Worldview map signals
            - repeated beliefs:
            - value hierarchy clues:
            - common lenses:
            - non-negotiables:

            ### Decision rules signals
            - heuristics:
            - default tradeoffs:
            - reversal conditions:
            - stress behavior:

            ### Contradiction handling signals
            - tensions inside this source:
            - tensions against other sources:
            - time-evolution clues:
            - what remains unresolved:

            ### Memory injection candidates
            - durable facts:
            - stable preferences:
            - recurring examples / stories:
            - refusal edges / boundary memories:

            ## Claim table
            | Claim | Layer | Evidence level | Behavioral use | Caveat |
            |---|---|---|---|---|
            | TODO | persona-core/worldview/decision/contradiction/memory | Strong / Moderate / Weak / Unknown | TODO | TODO |

            ## Merge recommendation
            - Keep:
            - Keep with caveat:
            - Reject:
            - Needs corroboration from:
            """
        ),
    )


def make_master_templates(root: Path, target: str) -> None:
    write(
        root / "01-source-pack" / "README.md",
        dedent(
            f"""
            # Source pack - {target}

            Fill `sources.csv` first.
            Then create or update one worksheet per source under `worksheets/`.

            Goal: force extraction from source -> persona layers, not source -> vibes.
            Required coverage:
            - persona core
            - worldview map
            - decision rules
            - contradiction handling
            - memory injection candidates
            """
        ),
    )
    ensure_csv(root / "01-source-pack" / "sources.csv")

    write(
        root / "02-extraction" / "master-merge.md",
        dedent(
            f"""
            # Master merge - {target}

            Merge only claims that survived worksheet review.

            ## Persona core
            | Claim | Evidence level | Source IDs | Why it matters | Contradiction / caveat |
            |---|---|---|---|---|
            | TODO | Strong | S1,S2 | TODO | TODO |

            ## Worldview map
            | Claim | Evidence level | Source IDs | Why it matters | Contradiction / caveat |
            |---|---|---|---|---|
            | TODO | Strong | S1,S2 | TODO | TODO |

            ## Decision rules
            | Rule | Evidence level | Source IDs | Trigger | Reversal condition |
            |---|---|---|---|---|
            | TODO | Strong | S1,S2 | TODO | TODO |

            ## Contradiction handling
            | Tension | Evidence A | Evidence B | Interpretation | Persona default |
            |---|---|---|---|---|
            | TODO | S1 | S4 | TODO | TODO |

            ## Memory candidates
            | Candidate | Type | Evidence level | Source IDs | Durable? | Reason |
            |---|---|---|---|---|---|
            | TODO | fact/preference/example/relationship/refusal | Strong | S1,S2 | yes/no | TODO |
            """
        ),
    )

    write(
        root / "02-extraction" / "promote-to-package.md",
        dedent(
            """
            # Promote to package

            Use this file to move merged claims into package files.

            ## references/persona-core.md
            - promote only stable behavior-system claims

            ## references/worldview-map.md
            - promote only beliefs / values / lenses that predict judgment

            ## references/decision-rules.md
            - promote only rules with repeated examples or explicit articulation

            ## references/contradiction-handling.md
            - promote unresolved tension, dated evolution, and default behavior under ambiguity

            ## MEMORY.md
            - promote only durable memory candidates
            - each entry must explain behavioral value and cite source IDs
            """
        ),
    )


def sync_from_csv(root: Path) -> None:
    csv_path = root / "01-source-pack" / "sources.csv"
    ensure_csv(csv_path)
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            source_id = (row.get("source_id") or "").strip()
            if not source_id:
                continue
            worksheet = root / "01-source-pack" / "worksheets" / f"{source_id}.md"
            if not worksheet.exists():
                write_source_template(worksheet, source_id)


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize or sync a source->persona extraction workspace")
    parser.add_argument("target", help="Target person name")
    parser.add_argument("--workspace", required=True, help="Path to the persona package or working directory")
    parser.add_argument("--sync", action="store_true", help="Only sync worksheets from existing sources.csv")
    args = parser.parse_args()

    root = Path(args.workspace).expanduser().resolve()
    if not args.sync:
        make_master_templates(root, args.target)
    sync_from_csv(root)
    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
