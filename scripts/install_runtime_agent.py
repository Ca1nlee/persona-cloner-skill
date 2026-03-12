#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

RUNTIME_FILES = [
    "SOUL.md",
    "IDENTITY.md",
    "AGENTS.md",
    "MEMORY.md",
]
OPTIONAL_FILES = [
    "README-agent.md",
]


def copy_file(src_root: Path, dst_root: Path, name: str, overwrite: bool) -> str:
    src = src_root / name
    if not src.exists():
        return f"skip missing {name}"

    dst = dst_root / name
    if dst.exists() and not overwrite:
        return f"skip existing {name}"

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return f"copied {name}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy a built persona-cloner runtime package into an OpenClaw workspace"
    )
    parser.add_argument("source_dir", help="Directory containing built runtime files")
    parser.add_argument("target_workspace", help="Target OpenClaw workspace directory")
    parser.add_argument(
        "--include-readme",
        action="store_true",
        help="Also copy README-agent.md when present",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing target files",
    )
    args = parser.parse_args()

    source_dir = Path(args.source_dir).expanduser().resolve()
    target_workspace = Path(args.target_workspace).expanduser().resolve()

    if not source_dir.exists() or not source_dir.is_dir():
        raise SystemExit(f"Source directory does not exist: {source_dir}")

    missing_required = [name for name in RUNTIME_FILES if not (source_dir / name).exists()]
    if missing_required:
        raise SystemExit(
            "Source directory is missing required runtime files: " + ", ".join(missing_required)
        )

    target_workspace.mkdir(parents=True, exist_ok=True)

    results: list[str] = []
    for name in RUNTIME_FILES:
        results.append(copy_file(source_dir, target_workspace, name, args.overwrite))

    if args.include_readme:
        for name in OPTIONAL_FILES:
            results.append(copy_file(source_dir, target_workspace, name, args.overwrite))

    print(f"Installed runtime package from {source_dir} -> {target_workspace}")
    for line in results:
        print(f"- {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
