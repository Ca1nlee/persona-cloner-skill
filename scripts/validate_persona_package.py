#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

SEVERITIES = ("error", "warning", "note")
REQUIRED_ROOT_FILES = ["SOUL.md", "IDENTITY.md", "AGENTS.md", "MEMORY.md", "README-agent.md"]
REQUIRED_REFERENCE_FILES = {
    "persona-core": ["references/persona-core.md"],
    "worldview-map": ["references/worldview-map.md"],
    "decision-rules": ["references/decision-rules.md"],
    "contradiction-handling": ["references/contradiction-handling.md"],
    "memory-injection-spec": ["references/memory-injection-spec.md"],
    "identity-boundary-statement": ["references/identity-boundary-statement.md"],
    "output-discipline": ["references/output-discipline.md"],
    "source-map": ["references/source-map.md"],
    "framework-extraction": ["references/framework-extraction.md", "references/extraction-framework.md"],
}
REQUIRED_BOUNDARY_PATTERNS = [
    r"public (?:materials|evidence|record)",
    r"not (?:an )?official",
    r"not (?:an )?endorsed|no endorsement|official or endorsed",
    r"private access|private memor|unpublished|secret motive|backstage",
]
FORBIDDEN_SELF_DISTANCING = [r"digital\s+twin", r"digital\s+clone", r"virtual\s+version", r"persona\s+clone"]
SOURCE_PATTERNS = [r"\bS\d+\b", r"source ids?", r"evidence level", r"evidence"]
PLACEHOLDER_PATTERNS = [r"\bTODO\b", r"TBD", r"fill this", r"placeholder"]
DISCIPLINE_PATTERNS = [
    r"response length",
    r"verdict-first|lead with the (?:answer|conclusion|judgment|recommendation|refusal)",
    r"expand only on demand|expansion only on demand|expand only when",
    r"anti-lecture|do not .*lecture|do not turn .* into (?:a )?lesson",
    r"anti-assistant-tone|generic assistant filler|service tone|helper filler|customer-service",
    r"bluntness|restraint",
]

@dataclass
class Finding:
    severity: str
    code: str
    message: str

class Validator:
    def __init__(self, root: Path):
        self.root = root
        self.findings: list[Finding] = []

    def add(self, severity: str, code: str, message: str) -> None:
        self.findings.append(Finding(severity, code, message))

    def exists_any(self, candidates: Iterable[str]) -> Path | None:
        for candidate in candidates:
            path = self.root / candidate
            if path.exists():
                return path
        return None

    def read_text(self, rel: str) -> str:
        path = self.root / rel
        if not path.exists() or not path.is_file():
            return ""
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return path.read_text(encoding="utf-8", errors="ignore")

    def combined_core_text(self) -> str:
        parts = [self.read_text(name) for name in REQUIRED_ROOT_FILES]
        parts.extend(self.read_text(path) for path in [
            "references/identity-boundary-statement.md",
            "references/persona-core.md",
            "references/worldview-map.md",
            "references/decision-rules.md",
            "references/source-map.md",
            "references/framework-extraction.md",
            "references/evaluation-prompts.md",
        ])
        return "\n".join(part for part in parts if part)

    def validate(self) -> tuple[str, list[Finding]]:
        self.check_root_exists()
        if not self.root.exists():
            return "fail", self.findings
        self.check_required_files()
        self.check_required_references()
        self.check_examples_and_eval_prompts()
        self.check_source_boundary()
        self.check_output_discipline()
        self.check_evidence_trace()
        self.check_eval_track()
        self.check_memory_track()
        self.check_optional_traceability()
        self.check_placeholder_density()
        return self.verdict(), self.findings

    def check_root_exists(self) -> None:
        if not self.root.exists():
            self.add("error", "root_missing", f"Package directory does not exist: {self.root}")
        elif not self.root.is_dir():
            self.add("error", "root_not_dir", f"Package path is not a directory: {self.root}")

    def check_required_files(self) -> None:
        for rel in REQUIRED_ROOT_FILES:
            if not (self.root / rel).exists():
                self.add("error", "missing_required_file", f"Missing required root file: {rel}")

    def check_required_references(self) -> None:
        for label, candidates in REQUIRED_REFERENCE_FILES.items():
            if not self.exists_any(candidates):
                self.add("error", "missing_reference", f"Missing required reference for {label}: expected one of {', '.join(candidates)}")

    def check_examples_and_eval_prompts(self) -> None:
        examples_dir = self.root / "examples"
        prompt_file = self.root / "references" / "evaluation-prompts.md"
        if not examples_dir.exists() or not examples_dir.is_dir():
            self.add("error", "examples_missing", "Missing examples/ directory")
        else:
            example_docs = [p for p in examples_dir.glob("*.md") if p.name.lower() != "readme.md"]
            if not example_docs:
                self.add("error", "examples_empty", "examples/ exists but has no example markdown files")
            elif len(example_docs) < 2:
                self.add("warning", "examples_thin", "examples/ has fewer than 2 example files; quality bar may be underspecified")
        if not prompt_file.exists():
            self.add("error", "eval_prompts_missing", "Missing references/evaluation-prompts.md")

    def check_source_boundary(self) -> None:
        text = self.combined_core_text().lower()
        missing = [pattern for pattern in REQUIRED_BOUNDARY_PATTERNS if not re.search(pattern, text)]
        if missing:
            self.add("error", "boundary_incomplete", "Source-boundary language is incomplete; expected public-materials, non-official, non-endorsement, and no-private-access language")
        runtime_text = "\n".join(self.read_text(name) for name in REQUIRED_ROOT_FILES).lower()
        forbidden_hits = sorted({pattern for pattern in FORBIDDEN_SELF_DISTANCING if re.search(pattern, runtime_text)})
        if forbidden_hits:
            self.add("warning", "self_distancing_language", f"Runtime files still foreground self-distancing labels: {', '.join(forbidden_hits)}")

    def check_output_discipline(self) -> None:
        texts = "\n".join([self.read_text("SOUL.md"), self.read_text("AGENTS.md"), self.read_text("references/output-discipline.md")]).lower()
        missing = [pattern for pattern in DISCIPLINE_PATTERNS if not re.search(pattern, texts)]
        if missing:
            self.add("error", "output_discipline_missing", "Runtime output discipline is incomplete; expected explicit rules for length, verdict-first structure, expansion limits, anti-lecture, anti-assistant-tone, and bluntness/restraint")

    def check_evidence_trace(self) -> None:
        source_map = self.read_text("references/source-map.md")
        framework = self.read_text("references/framework-extraction.md")
        memory = self.read_text("MEMORY.md")
        evidence_hits = sum(1 for pattern in SOURCE_PATTERNS if re.search(pattern, "\n".join([source_map, framework, memory]), re.I))
        if evidence_hits < 2:
            self.add("error", "evidence_trace_missing", "Too little source/evidence trace. Package should show source IDs or evidence annotations, not empty shell docs")
        source_ids = set(re.findall(r"\bS\d+\b", "\n".join([source_map, framework, memory])))
        if not source_ids:
            self.add("error", "source_ids_missing", "No source IDs detected in source-map/framework/MEMORY files")
        elif len(source_ids) < 2:
            self.add("warning", "source_ids_thin", "Only one distinct source ID detected; coverage may be too thin")

    def check_eval_track(self) -> None:
        eval_dir = self.root / "eval"
        if not eval_dir.exists() or not eval_dir.is_dir():
            self.add("error", "eval_track_missing", "Missing eval/ directory")
            return
        if not (eval_dir / "cases.json").exists():
            self.add("error", "eval_cases_missing", "Missing eval/cases.json")
        else:
            try:
                cases = json.loads((eval_dir / "cases.json").read_text(encoding="utf-8"))
                if not isinstance(cases, list) or not cases:
                    self.add("error", "eval_cases_invalid", "eval/cases.json must contain a non-empty list")
            except Exception as exc:
                self.add("error", "eval_cases_invalid", f"Could not parse eval/cases.json: {exc}")
        if not (eval_dir / "rubric.md").exists():
            self.add("error", "eval_rubric_missing", "Missing eval/rubric.md")
        if not (eval_dir / "behavior-cases.json").exists():
            self.add("warning", "behavior_cases_missing", "Missing eval/behavior-cases.json; runtime answer behavior is not scaffolded for self-test")
        if not (eval_dir / "behavior-rubric.md").exists():
            self.add("warning", "behavior_rubric_missing", "Missing eval/behavior-rubric.md; runtime behavior scoring rule is absent")
        runs_dir = eval_dir / "runs"
        if not runs_dir.exists() or not runs_dir.is_dir():
            self.add("warning", "eval_runs_missing", "Missing eval/runs/ directory for regression history")

    def check_memory_track(self) -> None:
        memory_dir = self.root / "memory"
        if not memory_dir.exists() or not memory_dir.is_dir():
            self.add("error", "memory_track_missing", "Missing memory/ directory")
            return
        for rel in ["memory/MEMORY-POLICY.md", "memory/CHANGELOG.md", "memory/candidates.jsonl"]:
            if not (self.root / rel).exists():
                self.add("error", "memory_track_file_missing", f"Missing {rel}")
        snapshots = memory_dir / "snapshots"
        if not snapshots.exists() or not snapshots.is_dir():
            self.add("warning", "memory_snapshots_missing", "Missing memory/snapshots/ directory for version history")

    def check_optional_traceability(self) -> None:
        if not (self.root / "01-source-pack").exists():
            self.add("note", "source_pack_missing", "01-source-pack/ is absent; traceability still works if references/source-map.md is complete, but auditability is weaker")
        if not (self.root / "02-extraction").exists():
            self.add("note", "extraction_missing", "02-extraction/ is absent; merged-claims audit trail is not packaged")

    def check_placeholder_density(self) -> None:
        texts = {rel: self.read_text(rel) for rel in REQUIRED_ROOT_FILES + [
            "references/persona-core.md",
            "references/worldview-map.md",
            "references/decision-rules.md",
            "references/source-map.md",
            "references/framework-extraction.md",
        ]}
        placeholder_hits = []
        for rel, text in texts.items():
            if not text:
                continue
            count = sum(len(re.findall(pattern, text, re.I)) for pattern in PLACEHOLDER_PATTERNS)
            if count >= 3:
                placeholder_hits.append((rel, count))
        if placeholder_hits:
            details = ", ".join(f"{rel} ({count})" for rel, count in placeholder_hits)
            self.add("warning", "placeholder_heavy", f"Several core files still look scaffold-heavy: {details}")

    def verdict(self) -> str:
        severities = {finding.severity for finding in self.findings}
        if "error" in severities:
            return "fail"
        if "warning" in severities:
            return "pass_with_warnings"
        return "pass"


def render_terminal(verdict: str, findings: list[Finding], package_dir: Path) -> str:
    counts = {severity: 0 for severity in SEVERITIES}
    for finding in findings:
        counts[finding.severity] += 1
    lines = [
        f"Persona package validation: {package_dir}",
        f"Verdict: {verdict}",
        f"Counts: error={counts['error']} warning={counts['warning']} note={counts['note']}",
        "",
    ]
    if findings:
        for severity in SEVERITIES:
            group = [f for f in findings if f.severity == severity]
            if not group:
                continue
            lines.append(f"[{severity.upper()}]")
            for finding in group:
                lines.append(f"- {finding.code}: {finding.message}")
            lines.append("")
    else:
        lines.append("No findings. Package is ready on current checks.")
    return "\n".join(lines).rstrip() + "\n"


def render_markdown(verdict: str, findings: list[Finding], package_dir: Path) -> str:
    counts = {severity: 0 for severity in SEVERITIES}
    for finding in findings:
        counts[finding.severity] += 1
    lines = [
        "# Persona package validation report",
        "",
        f"- Package: `{package_dir}`",
        f"- Verdict: **{verdict}**",
        f"- Counts: error={counts['error']} warning={counts['warning']} note={counts['note']}",
        "",
    ]
    if not findings:
        lines.append("No findings. Package is ready on current checks.")
        return "\n".join(lines) + "\n"
    for severity in SEVERITIES:
        group = [f for f in findings if f.severity == severity]
        if not group:
            continue
        lines.append(f"## {severity}")
        lines.append("")
        for finding in group:
            lines.append(f"- **{finding.code}** — {finding.message}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a persona package for completeness, source boundaries, evidence trace, eval track, and memory versioning")
    parser.add_argument("package_dir", help="Path to the persona package directory")
    parser.add_argument("--report", help="Optional path to write a markdown report")
    parser.add_argument("--json", action="store_true", help="Also emit JSON after the human-readable report")
    args = parser.parse_args()

    root = Path(args.package_dir).expanduser().resolve()
    validator = Validator(root)
    verdict, findings = validator.validate()
    print(render_terminal(verdict, findings, root), end="")

    if args.report:
        report_path = Path(args.report).expanduser().resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_markdown(verdict, findings, root), encoding="utf-8")
        print(f"Markdown report written: {report_path}")

    if args.json:
        payload = {"package_dir": str(root), "verdict": verdict, "findings": [finding.__dict__ for finding in findings]}
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    return 1 if verdict == "fail" else 0

if __name__ == "__main__":
    raise SystemExit(main())
