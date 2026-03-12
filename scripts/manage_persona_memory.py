#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from textwrap import dedent


CANDIDATE_TEMPLATE = {
    "id": "MEM-0001",
    "type": "fact",
    "claim": "",
    "behavioral_impact": "",
    "evidence_level": "Strong",
    "source_ids": ["S1"],
    "durable": True,
    "status": "proposed",
    "conflicts_with": [],
    "merge_strategy": "keep_latest|keep_both_scoped|replace_old|reject",
    "notes": "",
}

MEMORY_SECTIONS = {
    "fact": "Durable facts",
    "preference": "Stable preferences",
    "example": "Canonical examples / stories",
    "relationship": "Relationships and affiliations",
    "refusal": "Refusal and boundary memory",
    "boundary": "Refusal and boundary memory",
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def ensure_files(root: Path) -> tuple[Path, Path, Path]:
    memory = root / "MEMORY.md"
    candidates = root / "memory" / "candidates.jsonl"
    changelog = root / "memory" / "CHANGELOG.md"
    snapshots = root / "memory" / "snapshots"
    snapshots.mkdir(parents=True, exist_ok=True)

    if not memory.exists():
        write(
            memory,
            dedent(
                """
                # MEMORY.md

                ## Durable facts

                ## Stable preferences

                ## Canonical examples / stories

                ## Relationships and affiliations

                ## Refusal and boundary memory
                """
            ),
        )
    if not changelog.exists():
        write(
            changelog,
            "# Memory changelog\n\n",
        )
    candidates.parent.mkdir(parents=True, exist_ok=True)
    candidates.touch(exist_ok=True)
    return memory, candidates, changelog


def add_candidate(root: Path, payload: dict) -> Path:
    _, candidates, _ = ensure_files(root)
    with candidates.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return candidates


def render_entry(payload: dict) -> str:
    return dedent(
        f"""
        ### {payload['id']} - {payload['claim']}
        - Type: {payload['type']}
        - Why it matters behaviorally: {payload['behavioral_impact']}
        - Evidence level: {payload['evidence_level']}
        - Source IDs: {', '.join(payload.get('source_ids', []))}
        - Conflict note: {', '.join(payload.get('conflicts_with', [])) or 'none'}
        - Version note: promoted {datetime.now().date().isoformat()}
        """
    ).strip()


def insert_under_section(memory_text: str, section: str, block: str) -> str:
    heading = f"## {section}"
    if heading not in memory_text:
        memory_text = memory_text.rstrip() + f"\n\n{heading}\n"
    idx = memory_text.index(heading) + len(heading)
    remainder = memory_text[idx:]
    next_section = remainder.find("\n## ")
    if next_section == -1:
        section_body = remainder.rstrip() + "\n\n" + block + "\n"
        return memory_text[:idx] + section_body
    prefix = remainder[:next_section].rstrip() + "\n\n" + block + "\n"
    suffix = remainder[next_section:]
    return memory_text[:idx] + prefix + suffix


def snapshot_memory(root: Path, memory_path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    snap = root / "memory" / "snapshots" / f"MEMORY-{stamp}.md"
    write(snap, memory_path.read_text(encoding="utf-8"))
    return snap


def append_changelog(changelog: Path, line: str) -> None:
    with changelog.open("a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")


def apply_candidate(root: Path, candidate_id: str) -> tuple[Path, Path]:
    memory, candidates, changelog = ensure_files(root)
    items = []
    target = None
    with candidates.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            if item.get("id") == candidate_id:
                target = item
            items.append(item)
    if not target:
        raise SystemExit(f"Candidate not found: {candidate_id}")
    if not target.get("durable", False):
        raise SystemExit("Candidate is not durable; do not promote into MEMORY.md")

    snapshot = snapshot_memory(root, memory)
    text = memory.read_text(encoding="utf-8")
    section = MEMORY_SECTIONS.get(target.get("type", "fact"), "Durable facts")
    text = insert_under_section(text, section, render_entry(target))
    write(memory, text)

    target["status"] = "accepted"
    target["accepted_at"] = datetime.now().isoformat(timespec="seconds")
    with candidates.open("w", encoding="utf-8") as f:
        for item in items:
            if item.get("id") == candidate_id:
                item = target
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    append_changelog(
        changelog,
        f"- {datetime.now().date().isoformat()} accepted {candidate_id} into `{section}` | merge={target.get('merge_strategy')} | conflicts={','.join(target.get('conflicts_with', [])) or 'none'} | snapshot={snapshot.name}",
    )
    return memory, snapshot


def init_policy(root: Path) -> Path:
    policy = root / "memory" / "MEMORY-POLICY.md"
    if policy.exists():
        return policy
    write(
        policy,
        dedent(
            """
            # Persona memory policy

            ## Promote into MEMORY.md only if all are true
            - evidence level is Strong or clearly bounded Moderate
            - claim changes future behavior, not just biography completeness
            - claim is durable across time or deliberately scoped by time
            - no private, leaked, or speculative content

            ## Do not promote
            - one-off hot takes
            - temporary plans
            - weak inferences about psychology
            - copyright-heavy passages

            ## Conflict handling
            - `keep_both_scoped`: both entries stay, each with date/context scope
            - `replace_old`: newer or better-evidenced entry supersedes old one
            - `reject`: candidate stays in log, not in MEMORY.md

            ## Required versioning
            - snapshot MEMORY.md before every accepted change
            - append a changelog line for every accepted or rejected decision
            - never silently overwrite a durable memory
            """
        ),
    )
    return policy


def main() -> int:
    parser = argparse.ArgumentParser(description="Propose and version durable memory updates for a twin")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("--root", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("--root", required=True)
    p_add.add_argument("--id", required=True)
    p_add.add_argument("--type", required=True)
    p_add.add_argument("--claim", required=True)
    p_add.add_argument("--behavioral-impact", required=True)
    p_add.add_argument("--evidence-level", required=True)
    p_add.add_argument("--source-ids", required=True, help="Comma-separated")
    p_add.add_argument("--durable", action="store_true")
    p_add.add_argument("--conflicts-with", default="")
    p_add.add_argument("--merge-strategy", default="keep_latest")
    p_add.add_argument("--notes", default="")

    p_apply = sub.add_parser("apply")
    p_apply.add_argument("--root", required=True)
    p_apply.add_argument("--id", required=True)

    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()

    if args.cmd == "init":
        ensure_files(root)
        path = init_policy(root)
        print(path)
        return 0

    if args.cmd == "add":
        ensure_files(root)
        init_policy(root)
        payload = dict(CANDIDATE_TEMPLATE)
        payload.update(
            {
                "id": args.id,
                "type": args.type,
                "claim": args.claim,
                "behavioral_impact": args.behavioral_impact,
                "evidence_level": args.evidence_level,
                "source_ids": [s.strip() for s in args.source_ids.split(",") if s.strip()],
                "durable": bool(args.durable),
                "conflicts_with": [s.strip() for s in args.conflicts_with.split(",") if s.strip()],
                "merge_strategy": args.merge_strategy,
                "notes": args.notes,
            }
        )
        out = add_candidate(root, payload)
        print(out)
        return 0

    memory, snapshot = apply_candidate(root, args.id)
    print(json.dumps({"memory": str(memory), "snapshot": str(snapshot)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
