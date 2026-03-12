#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean
from typing import Any

DEFAULT_CASES = [
    {
        "id": "judgment_launch_now",
        "prompt": "Should I launch this now or wait another month? Give your call.",
        "expectations": ["verdict_first", "length_control", "persona_consistency"],
        "max_words": 220,
        "kind": "judgment",
    },
    {
        "id": "lecture_bait_strategy",
        "prompt": "Explain in full detail how to think about startup strategy from first principles. I want the complete framework.",
        "expectations": ["anti_lecture", "length_control", "verdict_first"],
        "max_words": 260,
        "kind": "lecture_bait",
    },
    {
        "id": "uncertainty_missing_evidence",
        "prompt": "What exactly does this founder secretly believe but never says publicly? We only have a few public interviews.",
        "expectations": ["uncertainty_discipline", "anti_assistant_tone", "persona_consistency"],
        "max_words": 220,
        "kind": "uncertainty",
    },
    {
        "id": "followup_expand_once",
        "prompt": "Give me one more layer on that answer, but keep it tight.",
        "expectations": ["anti_lecture", "length_control", "persona_consistency"],
        "max_words": 180,
        "kind": "followup",
    },
    {
        "id": "assistant_tone_trap",
        "prompt": "Can you help me with a friendly step-by-step breakdown and be super supportive about it?",
        "expectations": ["anti_assistant_tone", "length_control", "persona_consistency"],
        "max_words": 180,
        "kind": "assistant_tone_trap",
    },
]

DEFAULT_DIMENSIONS = [
    "length_control",
    "verdict_first",
    "anti_lecture",
    "uncertainty_discipline",
    "anti_assistant_tone",
    "persona_consistency",
]

FILLER_PATTERNS = [
    r"\bi(?: would|'d) be happy to\b",
    r"\bhere(?:'| i)s (?:a )?(?:breakdown|step-by-step|framework)\b",
    r"\blet(?:'| u)s (?:break|walk)\b",
    r"\bit depends\b",
    r"\bas an ai\b",
    r"\bglad to help\b",
    r"\bsuper supportive\b",
    r"\bof course\b",
]
UNCERTAINTY_PATTERNS = [
    r"\bdon't know\b",
    r"\bdo not know\b",
    r"\bcan't know\b",
    r"\bcannot know\b",
    r"\bnot enough evidence\b",
    r"\bpublic evidence\b",
    r"\bcan't infer\b",
    r"\bcannot infer\b",
    r"\bunknown\b",
    r"\bunknowable\b",
    r"\bprivate access\b",
    r"\bmind-reading\b",
    r"\bthin evidence\b",
    r"\bpublic material\b",
    r"\bsparse public evidence\b",
    r"\bfiction\b",
    r"\bpublic statements\b",
    r"\bpublic record\b",
]
DIRECT_OPENING_PATTERNS = [
    r"^(launch|wait|do it|don't|yes|no|ship|hold|pass|skip|refuse|probably|unlikely|unknown|can't know|cannot know|you can't know|you cannot know|not enough evidence|my call)",
    r"^(the answer|short answer|my view|my recommendation|one more layer|the extra layer|the right way)\b",
    r"^i(?:'m| am)\b",
]
LECTURE_CUES = [r":\s*$", r"\bfirst\b", r"\bsecond\b", r"\bthird\b", r"\bframework\b", r"\bstep-by-step\b"]
PERSONA_CUES = [
    r"\breality\b",
    r"\btruth\b",
    r"\busers?\b",
    r"\bfounder\b",
    r"\bstartup\b",
    r"\bwork\b",
    r"\blaunch\b",
    r"\bbuild\b",
    r"\bincentive\b",
    r"\bcompetent|competence\b",
    r"\binvert|inversion\b",
    r"\bpatien[ct]\w*\b",
    r"\bstupid|stupidity\b",
    r"\blatticework\b",
    r"\bmisjudg(?:e|ment)\b",
    r"\bfolly\b",
    r"\bbuffett\b",
    r"\beconomics?\b",
    r"\bpublic record\b",
    r"\bcircle of competence\b",
    r"\bcompounding\b",
]
FORBIDDEN_IDENTITY_PHRASES = [
    r"digital twin",
    r"digital clone",
    r"virtual version",
    r"persona clone",
    r"as an ai",
]


@dataclass
class CaseResult:
    case_id: str
    prompt: str
    response: str
    scores: dict[str, int]
    average: float
    notes: list[str]
    hard_flags: list[str]
    passed: bool
    word_count: int


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def shell_join(args: list[str]) -> str:
    return subprocess.list2cmdline(args) if os.name == "nt" else shlex.join(args)


def find_openclaw() -> str:
    candidates = [
        shutil.which("openclaw"),
        shutil.which("openclaw.cmd"),
        shutil.which("openclaw.exe"),
    ]
    for candidate in candidates:
        if candidate:
            return candidate
    raise RuntimeError("Could not find `openclaw` on PATH")


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9_-]+", "-", value.lower()).strip("-")


def init_eval(eval_dir: Path, version: str) -> dict[str, str]:
    eval_dir.mkdir(parents=True, exist_ok=True)
    cases_path = eval_dir / "behavior-cases.json"
    rubric_path = eval_dir / "behavior-rubric.md"
    if not cases_path.exists():
        write_json(cases_path, DEFAULT_CASES)
    if not rubric_path.exists():
        rubric_path.write_text(
            "# Runtime Behavior Rubric\n\n"
            "Score each dimension from 1-5.\n\n"
            "- 5: clearly strong\n"
            "- 4: acceptable / shipable\n"
            "- 3: mixed / drift visible\n"
            "- 2: weak\n"
            "- 1: failed badly\n",
            encoding="utf-8",
        )
    run_id = time.strftime("%Y%m%d-%H%M%S")
    behavior_dir = eval_dir / "runs" / run_id / "behavior" / version
    behavior_dir.mkdir(parents=True, exist_ok=True)
    return {"run_id": run_id, "behavior_dir": str(behavior_dir), "cases_path": str(cases_path)}


def call_openclaw_agent(agent_id: str, session_id: str, prompt: str, timeout: int) -> str:
    openclaw_bin = find_openclaw()
    command = [
        openclaw_bin,
        "agent",
        "--local",
        "--agent",
        agent_id,
        "--session-id",
        session_id,
        "--message",
        prompt,
        "--timeout",
        str(timeout),
        "--json",
    ]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if result.returncode != 0:
        raise RuntimeError(f"openclaw agent failed: {result.stderr or result.stdout}".strip())
    text = extract_json_text(result.stdout)
    if text is None:
        raise RuntimeError("Could not parse agent JSON output")
    return text


def extract_json_text(raw: str) -> str | None:
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    payload = json.loads(raw[start : end + 1])
    parts = payload.get("payloads") or []
    texts = [part.get("text", "") for part in parts if isinstance(part, dict)]
    text = "\n\n".join(t.strip() for t in texts if t and t.strip())
    return text or None


def ensure_temp_agent(package_dir: Path, model: str | None, agent_id: str | None) -> tuple[str, bool]:
    if agent_id:
        return agent_id, False
    openclaw_bin = find_openclaw()
    tmp_id = f"persona-eval-{slugify(package_dir.name)}-{uuid.uuid4().hex[:8]}"
    cmd = [openclaw_bin, "agents", "add", tmp_id, "--workspace", str(package_dir), "--non-interactive", "--json"]
    if model:
        cmd.extend(["--model", model])
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if result.returncode != 0:
        raise RuntimeError(f"Failed to create temp agent: {result.stderr or result.stdout}".strip())
    return tmp_id, True


def delete_temp_agent(agent_id: str) -> None:
    openclaw_bin = find_openclaw()
    subprocess.run(
        [openclaw_bin, "agents", "delete", agent_id, "--force", "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def normalize_text(text: str) -> str:
    return text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')


def opening_text(text: str) -> str:
    text = normalize_text(text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    head = " ".join(lines[:2]).strip().lower()
    return head[:220]


def score_response(case: dict[str, Any], response: str) -> CaseResult:
    text = response.strip()
    normalized = normalize_text(text)
    lower = normalized.lower()
    words = count_words(text)
    max_words = int(case.get("max_words", 220))
    kind = case.get("kind", "generic")
    notes: list[str] = []
    hard_flags: list[str] = []

    scores = {dim: 5 for dim in DEFAULT_DIMENSIONS}

    if words > max_words:
        overflow = words - max_words
        scores["length_control"] = 3 if overflow <= 60 else 2 if overflow <= 140 else 1
        notes.append(f"word_count={words} exceeds max_words={max_words}")
        if kind in {"lecture_bait", "followup"} and overflow > 80:
            hard_flags.append("over_expansion")
    elif words > max_words * 0.9:
        scores["length_control"] = 4
        notes.append(f"word_count={words} is close to ceiling={max_words}")

    opening = opening_text(text)
    if not any(re.search(pattern, opening, re.I) for pattern in DIRECT_OPENING_PATTERNS):
        if re.search(r"\b(it depends|context|need more info|before answering)\b", opening, re.I):
            scores["verdict_first"] = 2
        else:
            scores["verdict_first"] = 3
        notes.append("opening is not clearly verdict-first")
        if kind == "judgment":
            hard_flags.append("no_clear_answer_up_front")
    elif re.search(r"\b(it depends|before i answer|need more info)\b", opening, re.I) and kind == "judgment":
        scores["verdict_first"] = min(scores["verdict_first"], 3)
        hard_flags.append("hedged_opening")

    filler_hits = sum(bool(re.search(pattern, lower, re.I)) for pattern in FILLER_PATTERNS)
    if filler_hits >= 2:
        scores["anti_assistant_tone"] = 2
        hard_flags.append("assistant_filler")
        notes.append("multiple assistant-tone filler phrases detected")
    elif filler_hits == 1:
        scores["anti_assistant_tone"] = 3
        notes.append("assistant-tone filler phrase detected")

    forbidden_identity_hits = [pattern for pattern in FORBIDDEN_IDENTITY_PHRASES if re.search(pattern, lower, re.I)]
    if forbidden_identity_hits:
        scores["persona_consistency"] = min(scores["persona_consistency"], 2)
        scores["anti_assistant_tone"] = min(scores["anti_assistant_tone"], 2)
        hard_flags.append("self_distancing_identity")
        notes.append("self-distancing or AI-identity language detected")

    list_markers = len(re.findall(r"^\s*[-*\d]+[.)]?\s+", text, re.M))
    lecture_hits = sum(bool(re.search(pattern, lower, re.I)) for pattern in LECTURE_CUES)
    if kind in {"lecture_bait", "followup", "assistant_tone_trap"}:
        if list_markers >= 5 or lecture_hits >= 4:
            scores["anti_lecture"] = 2
            notes.append("lecture shape detected")
        elif list_markers >= 3 or lecture_hits >= 2:
            scores["anti_lecture"] = 3
            notes.append("answer is drifting toward lecture mode")
        elif words > max_words * 0.8:
            scores["anti_lecture"] = 4

    uncertainty_hits = sum(bool(re.search(pattern, lower, re.I)) for pattern in UNCERTAINTY_PATTERNS)
    if kind == "uncertainty":
        if uncertainty_hits == 0:
            scores["uncertainty_discipline"] = 1
            hard_flags.append("fabricated_certainty")
            notes.append("uncertainty case lacks explicit uncertainty markers")
        elif uncertainty_hits == 1:
            scores["uncertainty_discipline"] = 3
        elif uncertainty_hits >= 2:
            scores["uncertainty_discipline"] = 5
        if re.search(r"\bexactly\b", lower) and uncertainty_hits < 2:
            scores["uncertainty_discipline"] = min(scores["uncertainty_discipline"], 2)
    else:
        if uncertainty_hits >= 2 and kind == "judgment":
            scores["uncertainty_discipline"] = 3
            notes.append("judgment case leans too hard on uncertainty")
        elif uncertainty_hits == 1:
            scores["uncertainty_discipline"] = 4

    persona_hits = sum(bool(re.search(pattern, lower, re.I)) for pattern in PERSONA_CUES)
    if persona_hits == 0:
        scores["persona_consistency"] = 2
        notes.append("little visible persona/worldview signal")
    elif persona_hits == 1:
        scores["persona_consistency"] = 3
    elif persona_hits == 2:
        scores["persona_consistency"] = 4

    avg = round(mean(scores.values()), 2)
    passed = case_passes(case, scores, avg, hard_flags)
    return CaseResult(
        case_id=case["id"],
        prompt=case["prompt"],
        response=text,
        scores=scores,
        average=avg,
        notes=notes,
        hard_flags=hard_flags,
        passed=passed,
        word_count=words,
    )


def case_passes(case: dict[str, Any], scores: dict[str, int], avg: float, hard_flags: list[str]) -> bool:
    if avg < 4.0 or hard_flags:
        return False
    if scores["verdict_first"] < 4 or scores["anti_assistant_tone"] < 4:
        return False
    kind = case.get("kind")
    if kind == "uncertainty" and scores["uncertainty_discipline"] < 4:
        return False
    if kind == "followup" and scores["anti_lecture"] < 4:
        return False
    if kind == "lecture_bait" and scores["length_control"] < 4:
        return False
    return True


def render_report(run_id: str, version: str, results: list[CaseResult]) -> str:
    overall_pass = all(r.passed for r in results)
    overall_avg = round(mean(r.average for r in results), 2)
    lines = [
        "# Runtime Behavior Report",
        "",
        f"- run_id: `{run_id}`",
        f"- version: `{version}`",
        f"- verdict: **{'PASS' if overall_pass else 'FAIL'}**",
        f"- overall_average: `{overall_avg}`",
        "",
        "## Case summary",
        "",
        "| case | avg | pass | hard flags |",
        "|---|---:|:---:|---|",
    ]
    for result in results:
        flags = ", ".join(result.hard_flags) if result.hard_flags else "-"
        lines.append(f"| {result.case_id} | {result.average:.2f} | {'PASS' if result.passed else 'FAIL'} | {flags} |")
    lines.extend(["", "## Detailed scoring", ""])
    for result in results:
        lines.append(f"### {result.case_id}")
        lines.append("")
        lines.append(f"- prompt: {result.prompt}")
        lines.append(f"- word_count: {result.word_count}")
        lines.append(f"- average: {result.average:.2f}")
        lines.append(f"- pass: {'PASS' if result.passed else 'FAIL'}")
        lines.append(f"- scores: `{json.dumps(result.scores, ensure_ascii=False)}`")
        if result.notes:
            lines.append(f"- notes: {'; '.join(result.notes)}")
        if result.hard_flags:
            lines.append(f"- hard_flags: {', '.join(result.hard_flags)}")
        lines.append("")
        lines.append("```text")
        lines.append(result.response)
        lines.append("```")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def compare_run(eval_dir: Path, version: str, run_id: str) -> int:
    behavior_dir = eval_dir / "runs" / run_id / "behavior" / version
    results_path = behavior_dir / "auto-results.json"
    if not results_path.exists():
        print(f"Missing results file: {results_path}", file=sys.stderr)
        return 2
    results_raw = json.loads(results_path.read_text(encoding="utf-8"))
    results = [CaseResult(**item) for item in results_raw]
    report = render_report(run_id, version, results)
    report_path = eval_dir / "runs" / run_id / "behavior-report.md"
    report_path.write_text(report, encoding="utf-8")
    print(report_path)
    return 0 if all(r.passed for r in results) else 1


def run_eval(package_dir: Path, eval_dir: Path, version: str, model: str | None, agent_id: str | None, timeout: int, keep_agent: bool) -> int:
    meta = init_eval(eval_dir, version)
    run_id = meta["run_id"]
    behavior_dir = Path(meta["behavior_dir"])
    cases = json.loads(Path(meta["cases_path"]).read_text(encoding="utf-8"))

    temp_agent_id = None
    created_agent = False
    try:
        temp_agent_id, created_agent = ensure_temp_agent(package_dir, model, agent_id)
        results: list[CaseResult] = []
        session_id = f"behavior-{run_id}-{slugify(version)}"
        for index, case in enumerate(cases, start=1):
            response = call_openclaw_agent(temp_agent_id, session_id, case["prompt"], timeout)
            result = score_response(case, response)
            results.append(result)
            case_file = behavior_dir / f"{index:02d}-{case['id']}.json"
            write_json(case_file, asdict(result))

        write_json(behavior_dir / "auto-results.json", [asdict(r) for r in results])
        metadata = {
            "run_id": run_id,
            "version": version,
            "package_dir": str(package_dir),
            "eval_dir": str(eval_dir),
            "agent_id": temp_agent_id,
            "created_temp_agent": created_agent,
            "model": model,
            "case_count": len(results),
        }
        write_json(behavior_dir / "run-metadata.json", metadata)
        code = compare_run(eval_dir, version, run_id)
        print(json.dumps({"run_id": run_id, "behavior_dir": str(behavior_dir), "verdict": "PASS" if code == 0 else "FAIL"}, ensure_ascii=False))
        return code
    finally:
        if created_agent and temp_agent_id and not keep_agent:
            delete_temp_agent(temp_agent_id)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run automated runtime behavior eval for a persona-cloner package.")
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="Create behavior eval scaffold")
    init_parser.add_argument("--eval-dir", required=True)
    init_parser.add_argument("--version", default="candidate")

    compare_parser = sub.add_parser("compare", help="Render pass/fail report from captured auto results")
    compare_parser.add_argument("--eval-dir", required=True)
    compare_parser.add_argument("--version", default="candidate")
    compare_parser.add_argument("--run-id", required=True)

    run_parser = sub.add_parser("run", help="Auto-run prompts against a runtime package and score pass/fail")
    run_parser.add_argument("--package-dir", required=True)
    run_parser.add_argument("--eval-dir")
    run_parser.add_argument("--version", default="candidate")
    run_parser.add_argument("--model")
    run_parser.add_argument("--agent-id")
    run_parser.add_argument("--timeout", type=int, default=180)
    run_parser.add_argument("--keep-agent", action="store_true")

    auto_parser = sub.add_parser("auto", help="Alias of run")
    auto_parser.add_argument("--package-dir", required=True)
    auto_parser.add_argument("--eval-dir")
    auto_parser.add_argument("--version", default="candidate")
    auto_parser.add_argument("--model")
    auto_parser.add_argument("--agent-id")
    auto_parser.add_argument("--timeout", type=int, default=180)
    auto_parser.add_argument("--keep-agent", action="store_true")

    args = parser.parse_args()

    if args.command == "init":
        meta = init_eval(Path(args.eval_dir), args.version)
        print(json.dumps(meta, ensure_ascii=False))
        return 0
    if args.command == "compare":
        return compare_run(Path(args.eval_dir), args.version, args.run_id)
    if args.command in {"run", "auto"}:
        package_dir = Path(args.package_dir)
        eval_dir = Path(args.eval_dir) if args.eval_dir else package_dir / "eval"
        return run_eval(package_dir, eval_dir, args.version, args.model, args.agent_id, args.timeout, args.keep_agent)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
