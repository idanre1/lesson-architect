#!/usr/bin/env python3
"""Run the lesson-architect evaluation suite.

Part A (automated, structural): run check_lesson.py on every sample lesson
(must have no FAIL) and on every defective fixture (must FAIL the named checks).

Part B (qualitative, recorded): confirm each sample has a blueprint and a
review.md whose audit tables give a verdict for every qualitative check.
This only confirms the review was *recorded*; the verdicts themselves are
human/agent judgments and are not re-derived here.

Usage: python3 evals/run_evals.py   (use a Python with nbformat/nbclient/ipykernel
to execute notebooks; otherwise execution is reported as skipped)
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKER = ROOT / "skills" / "lesson-architect" / "scripts" / "check_lesson.py"


def run_checker(path: Path, kind: str, execute: bool, blueprint: Path | None = None) -> tuple[int, str]:
    cmd = [sys.executable, str(CHECKER), str(path), "--kind", kind]
    if execute:
        cmd.append("--execute")
    if blueprint is not None:
        cmd += ["--blueprint", str(blueprint)]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=path.parent)
    return p.returncode, p.stdout


def rows(output: str, status: str) -> list[str]:
    return [l for l in output.splitlines() if l.startswith(f"[{status}]")]


def main() -> int:
    cases = json.loads((ROOT / "evals" / "cases.json").read_text())
    problems: list[str] = []
    print("A. Structural checks (automated)\n")

    for c in cases["lessons"]:
        d = ROOT / c["dir"]
        lesson, bp = d / c["lesson"], d / (Path(c["lesson"]).stem + ".blueprint.md")
        if not lesson.exists():
            problems.append(f"{c['id']}: missing {lesson.relative_to(ROOT)}")
            print(f"  {c['id']:32} MISSING")
            continue
        code, out = run_checker(lesson, c["kind"], c.get("execute", False), bp if bp.exists() else None)
        fails, warns = rows(out, "FAIL"), rows(out, "WARN")
        status = "ok" if code == 0 else "FAIL"
        print(f"  {c['id']:32} {status:5} ({len(rows(out, 'PASS'))} pass, {len(warns)} warn, {len(fails)} fail)")
        for l in fails + warns:
            print(f"      {l}")
        if code != 0:
            problems.append(f"{c['id']}: structural failures")

    for f in cases["fixtures"]:
        code, out = run_checker(ROOT / f["path"], f["kind"], f.get("execute", False))
        fails, warns = "\n".join(rows(out, "FAIL")), "\n".join(rows(out, "WARN"))
        missing = [n for n in f.get("must_fail", []) if n not in fails]
        missing += [f"(warn) {n}" for n in f.get("must_warn", []) if n not in warns + fails]
        skipped_exec = f.get("execute") and "NOT executed" in out
        ok = code != 0 and not missing
        label = "rejected" if ok else ("SKIPPED" if skipped_exec else "NOT CAUGHT")
        print(f"  fixture {f['id']:24} {label}" + (f" — missing: {missing}" if missing else ""))
        if not ok and not skipped_exec:
            problems.append(f"fixture {f['id']}: expected failures not raised: {missing}")

    print("\nB. Qualitative review records (judgment recorded, not re-derived)\n")
    for c in cases["lessons"]:
        d = ROOT / c["dir"]
        review, bp = d / "review.md", d / (Path(c["lesson"]).stem + ".blueprint.md")
        if not bp.exists():
            problems.append(f"{c['id']}: no blueprint")
        if not review.exists():
            problems.append(f"{c['id']}: no review.md")
            print(f"  {c['id']:32} no review.md")
            continue
        text = review.read_text()
        verdicts = {}
        for check in cases["qualitative_checks"]:
            m = re.search(r"^\|\s*" + re.escape(check) + r"[^|]*\|\s*([^|]+?)\s*\|", text, re.M)
            verdicts[check] = m.group(1) if m else None
        absent = [k for k, v in verdicts.items() if not v or v in ("…", "...")]
        not_pass = {k: v for k, v in verdicts.items() if v and not re.match(r"(?i)pass", v)}
        print(f"  {c['id']:32} {len(verdicts) - len(absent)}/{len(verdicts)} verdicts recorded"
              + (f"; non-pass: {not_pass}" if not_pass else ""))
        if absent:
            problems.append(f"{c['id']}: review.md lacks verdicts for {absent}")

    print("\nStructural checks cannot establish teaching quality; see each review.md.")
    if problems:
        print("\nProblems:\n  " + "\n  ".join(problems))
        return 1
    print("\nAll evaluation cases behaved as expected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
