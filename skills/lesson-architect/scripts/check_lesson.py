#!/usr/bin/env python3
"""Structural checker for lesson-architect lessons (Markdown or Jupyter).

Checks presence, order, and alignment of the invisible <!-- la:... --> markers
plus a few hygiene rules. It does NOT judge teaching quality; see
references/quality-review.md for the continuity and correctness audits.

Usage:
  check_lesson.py LESSON.md [--kind paper] [--blueprint BLUEPRINT.md]
  check_lesson.py LESSON.ipynb [--execute] [--timeout 120]

Exit code 0 when no check FAILs (warnings allowed), 1 otherwise, 2 on usage errors.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

MARKER_RE = re.compile(r"<!--\s*la:([a-z-]+)((?:\s+[a-z]+=[^\s>]+)*)\s*-->")
ATTR_RE = re.compile(r"([a-z]+)=([^\s>]+)")
LEVELS = {"guided", "independent", "transfer", "check"}
KNOWN = {
    "orientation", "outcomes", "worked-example", "misconception", "exercise",
    "hint", "solution", "solutions", "synthesis", "optional", "sources",
    "paper-claim", "interpretation", "limitations", "predict", "interpret",
}
PLACEHOLDER_RE = re.compile(
    r"<(?!/?(?:details|summary|br|sup|sub|kbd|img|a|b|i|em|strong|code|span|div|p|hr|table|tr|td|th|ul|ol|li)\b)"
    r"[A-Z…][^<>$\n]{1,120}>"
)
PLACEHOLDER_WORDS_RE = re.compile(r"\b(TBD|lorem ipsum)\b|\{\{|\[insert", re.I)
TEACHER_RE = re.compile(
    r"\b(students will|the teacher|teacher notes?|instructor notes?|class period)\b", re.I
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def add(self, status: str, name: str, detail: str = "") -> None:
        self.rows.append((status, name, detail))

    def check(self, ok: bool, name: str, detail: str = "", warn: bool = False) -> None:
        self.add("PASS" if ok else ("WARN" if warn else "FAIL"), name, "" if ok else detail)

    @property
    def failed(self) -> bool:
        return any(s == "FAIL" for s, _, _ in self.rows)

    def print(self) -> None:
        for status, name, detail in self.rows:
            print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
        counts = Counter(s for s, _, _ in self.rows)
        print(
            f"\n{counts['PASS']} passed, {counts['WARN']} warnings, {counts['FAIL']} failed.\n"
            "Structural checks only: passing does not show the lesson teaches well. "
            "Run the continuity and correctness audits in references/quality-review.md."
        )


def strip_code_fences(text: str) -> str:
    """Blank out fenced code blocks so markers/headings inside code are ignored."""
    out, fence = [], None
    for line in text.splitlines():
        m = re.match(r"^\s*(```|~~~)", line)
        if m and fence is None:
            fence = m.group(1)
            out.append("")
            continue
        if fence and line.strip().startswith(fence):
            fence = None
            out.append("")
            continue
        out.append("" if fence else line)
    return "\n".join(out)


def parse_markers(text: str) -> list[dict]:
    markers = []
    for m in MARKER_RE.finditer(text):
        attrs = dict(ATTR_RE.findall(m.group(2) or ""))
        markers.append({"kind": m.group(1), "attrs": attrs, "pos": m.start(), "end": m.end()})
    return markers


def in_details(text: str, pos: int) -> bool:
    before = text[:pos]
    return before.count("<details") > before.count("</details>")


def outcomes_after(text: str, pos: int) -> list[str]:
    """Return the first numbered list after pos."""
    items, started = [], False
    for line in text[pos:].splitlines()[1:]:
        m = re.match(r"^\s*\d+[.)]\s+(.*)", line)
        if m:
            started = True
            items.append(m.group(1).strip())
        elif started and line.strip() and not line.startswith(" "):
            break
    return items


def check_common(text: str, rep: Report, kind: str, is_notebook: bool) -> list[dict]:
    prose = strip_code_fences(text)
    markers = parse_markers(prose)
    by = lambda k: [m for m in markers if m["kind"] == k]  # noqa: E731

    unknown = sorted({m["kind"] for m in markers} - KNOWN)
    rep.check(not unknown, "Only known la:* markers", f"unknown: {', '.join(unknown)}")

    headings = [HEADING_RE.match(l) for l in prose.splitlines()]
    h1 = [h for h in headings if h and len(h.group(1)) == 1]
    rep.check(bool(h1), "Has a title (H1)", "no '# ' heading found")

    leftovers = PLACEHOLDER_RE.findall(prose) + [m.group(0) for m in PLACEHOLDER_WORDS_RE.finditer(prose)]
    rep.check(not leftovers, "No unfilled template placeholders",
              f"found {len(leftovers)}: {', '.join(sorted(set(leftovers))[:5])}")

    # Orientation and outcomes
    orient = by("orientation")
    rep.check(bool(orient) and markers[0]["kind"] == "orientation",
              "Orientation marker present and first", "add <!-- la:orientation --> at the start")
    outs = by("outcomes")
    n_out = 0
    if not outs:
        rep.add("FAIL", "Learning outcomes listed", "missing <!-- la:outcomes --> before a numbered list")
    else:
        items = outcomes_after(prose, outs[0]["pos"])
        n_out = len(items)
        rep.check(n_out > 0, "Learning outcomes listed", "no numbered list after la:outcomes")
        if n_out:
            rep.check(2 <= n_out <= 8, f"Outcome count reasonable ({n_out})",
                      "aim for 2–8 observable outcomes", warn=True)

    # Worked examples, misconceptions
    worked = by("worked-example")
    rep.check(bool(worked), "Has a worked example", "add <!-- la:worked-example -->")
    rep.check(bool(by("misconception")), "Confronts a misconception", "add <!-- la:misconception -->")

    # Exercises
    exercises = by("exercise")
    rep.check(bool(exercises), "Has exercises", "no <!-- la:exercise ... --> markers")
    ids = [e["attrs"].get("id") for e in exercises]
    dupes = [i for i, c in Counter(ids).items() if c > 1]
    missing_id = sum(1 for i in ids if not i)
    rep.check(not dupes and not missing_id, "Exercise ids present and unique",
              f"duplicates: {dupes}; missing ids: {missing_id}")
    bad_levels = [e["attrs"].get("id") for e in exercises if e["attrs"].get("level") not in LEVELS]
    rep.check(not bad_levels, "Exercise levels valid", f"invalid/missing level on {bad_levels}")

    assessed: set[int] = set()
    bad_refs = []
    for e in exercises:
        for tok in filter(None, e["attrs"].get("outcomes", "").split(",")):
            if tok.isdigit() and 1 <= int(tok) <= max(n_out, 0):
                assessed.add(int(tok))
            else:
                bad_refs.append(f"{e['attrs'].get('id')}:{tok}")
    if n_out:
        unassessed = sorted(set(range(1, n_out + 1)) - assessed)
        rep.check(not unassessed, "Every outcome is assessed by an exercise",
                  f"outcomes never assessed: {unassessed}")
    rep.check(not bad_refs, "Exercise outcome references valid", f"bad refs: {bad_refs}")

    levels = [(e["pos"], e["attrs"].get("level")) for e in exercises]
    first_guided = min((p for p, l in levels if l == "guided"), default=None)
    first_indep = min((p for p, l in levels if l in ("independent", "transfer")), default=None)
    rep.check(first_guided is not None, "Has guided practice", "no level=guided exercise")
    rep.check(first_indep is not None, "Has independent practice", "no level=independent/transfer exercise")
    if first_guided is not None and first_indep is not None:
        rep.check(first_guided < first_indep, "Guided practice precedes independent practice",
                  "first independent exercise appears before first guided one")
    if worked and exercises:
        rep.check(worked[0]["pos"] < exercises[0]["pos"], "Worked example precedes first exercise",
                  "an exercise appears before any worked example")

    # Hints and solutions: exist, after exercise, separated from statements
    ex_pos = {e["attrs"].get("id"): e["pos"] for e in exercises}
    sol_area = by("solutions")
    sol_start = sol_area[0]["pos"] if sol_area else None
    sols = by("solution")
    sol_ids = {s["attrs"].get("id") for s in sols}
    no_sol = [i for i in ex_pos if i not in sol_ids]
    rep.check(not no_sol, "Every exercise has a solution", f"missing solutions: {no_sol}")
    hint_ids = {h["attrs"].get("id") for h in by("hint")}
    no_hint = [e["attrs"].get("id") for e in exercises
               if e["attrs"].get("level") in ("independent", "transfer") and e["attrs"].get("id") not in hint_ids]
    rep.check(not no_hint, "Independent/transfer exercises have hints", f"no hint for {no_hint}", warn=True)
    misplaced, orphans = [], []
    for m in sols + by("hint"):
        i = m["attrs"].get("id")
        if i not in ex_pos:
            orphans.append(f"{m['kind']}:{i}")
            continue
        separated = (sol_start is not None and m["pos"] > sol_start) or in_details(prose, m["pos"])
        if m["pos"] < ex_pos[i] or not separated:
            misplaced.append(f"{m['kind']}:{i}")
    rep.check(not orphans, "Hints/solutions refer to existing exercises", f"orphans: {orphans}")
    rep.check(not misplaced, "Hints/solutions separated from exercise statements",
              f"place after <!-- la:solutions --> or inside <details>: {misplaced}")
    if sol_start is not None and exercises:
        late = [e["attrs"].get("id") for e in exercises if e["pos"] > sol_start]
        rep.check(not late, "No exercise statements inside the solutions area", f"{late}")

    # Synthesis
    syn = by("synthesis")
    rep.check(bool(syn), "Has a synthesis", "add <!-- la:synthesis -->")
    if syn and worked:
        rep.check(syn[-1]["pos"] > worked[0]["pos"], "Synthesis comes after the teaching",
                  "synthesis marker precedes the first worked example")

    # Paper-specific
    if kind == "paper":
        for k in ("paper-claim", "interpretation", "limitations"):
            rep.check(bool(by(k)), f"Paper lesson marks {k.replace('-', ' ')}", f"add <!-- la:{k} -->")
        src = by("sources")
        has_url = bool(src) and bool(re.search(r"https?://", prose[src[0]["pos"]:]))
        rep.check(has_url, "Paper lesson lists sources with URLs", "add <!-- la:sources --> followed by URLs")

    # Hygiene
    rep.check(prose.count("$$") % 2 == 0, "Display-math delimiters balanced", "odd number of $$", warn=True)
    sub = Counter(h.group(2).strip().lower() for h in headings if h and len(h.group(1)) >= 2)
    repeated = [f"'{t}'×{c}" for t, c in sub.items() if c >= 3]
    rep.check(not repeated, "Sub-headings not mechanically repeated", ", ".join(repeated), warn=True)
    teacher = sorted({m.group(0).lower() for m in TEACHER_RE.finditer(prose)})
    rep.check(not teacher, "Student-facing voice", f"teacher-facing phrases: {teacher}", warn=True)
    return markers


def check_markdown(path: Path, args, rep: Report) -> None:
    text = path.read_text(encoding="utf-8")
    fences = len(re.findall(r"^\s*(```|~~~)", text, re.M))
    rep.check(fences % 2 == 0, "Code fences balanced", f"{fences} fence lines")
    check_common(text, rep, args.kind, is_notebook=False)


def check_notebook(path: Path, args, rep: Report) -> None:
    raw = path.read_text(encoding="utf-8")
    try:
        nb = json.loads(raw)
    except json.JSONDecodeError as e:
        rep.add("FAIL", "Notebook is valid JSON", f"{e} (is this Markdown renamed to .ipynb?)")
        return
    rep.add("PASS", "Notebook is valid JSON")
    ok = isinstance(nb, dict) and nb.get("nbformat") == 4 and isinstance(nb.get("cells"), list)
    rep.check(ok, "nbformat 4 structure", "missing nbformat=4 or cells list")
    if not ok:
        return
    try:
        import nbformat  # type: ignore

        nbformat.validate(nbformat.reads(raw, as_version=4))
        rep.add("PASS", "nbformat schema validation")
    except ImportError:
        rep.add("WARN", "nbformat schema validation", "nbformat not installed; skipped")
    except Exception as e:  # noqa: BLE001
        rep.add("FAIL", "nbformat schema validation", str(e).splitlines()[0])

    cells = nb["cells"]
    src = lambda c: "".join(c.get("source", "")) if isinstance(c.get("source"), list) else c.get("source", "")  # noqa: E731
    types = [c.get("cell_type") for c in cells]
    rep.check(types.count("code") >= 1 and types.count("markdown") >= 2,
              "Mix of markdown and code cells", f"{types.count('markdown')} md, {types.count('code')} code")
    with_out = [i for i, c in enumerate(cells) if c.get("cell_type") == "code" and (c.get("outputs") or c.get("execution_count"))]
    rep.check(not with_out, "Shipped without outputs (predictions stay genuine)",
              f"cells with outputs/execution counts: {with_out[:8]}", warn=True)

    # Prediction → experiment → interpretation cycles
    seq = []
    for c in cells:
        s = src(c)
        if c.get("cell_type") == "markdown":
            ks = [m["kind"] for m in parse_markers(s)]
            seq.append("P" if "predict" in ks else "I" if "interpret" in ks else "m")
        else:
            seq.append("C")
    broken, cycles = [], 0
    for i, t in enumerate(seq):
        if t != "P":
            continue
        rest = seq[i + 1:]
        j = next((k for k, x in enumerate(rest) if x == "C"), None)
        k_int = next((k for k, x in enumerate(rest) if x == "I"), None)
        nxt_p = next((k for k, x in enumerate(rest) if x == "P"), len(rest))
        if j is not None and k_int is not None and j < k_int < nxt_p:
            cycles += 1
        else:
            broken.append(i)
    rep.check(cycles >= 1, "Has predict → experiment → interpret cycle(s)", "no complete cycle")
    rep.check(not broken, "Every prediction is followed by an experiment and interpretation",
              f"incomplete cycles at cells {broken}")

    text = "\n\n".join(src(c) if c.get("cell_type") == "markdown" else "```python\n" + src(c) + "\n```" for c in cells)
    check_common(text, rep, args.kind, is_notebook=True)

    if args.execute:
        execute_notebook(path, args.timeout, rep)


def execute_notebook(path: Path, timeout: int, rep: Report) -> None:
    try:
        import nbformat  # type: ignore
        from nbclient import NotebookClient  # type: ignore
        from nbclient.exceptions import CellExecutionError  # type: ignore
    except ImportError:
        rep.add("WARN", "Executed in a clean kernel", "nbformat/nbclient not installed; NOT executed")
        return
    nb = nbformat.read(str(path), as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3",
                            resources={"metadata": {"path": str(path.parent)}})
    try:
        client.execute()
    except CellExecutionError as e:
        rep.add("FAIL", "Executed in a clean kernel", str(e).strip().splitlines()[-1][:300])
        return
    except Exception as e:  # noqa: BLE001
        rep.add("WARN", "Executed in a clean kernel", f"could not start kernel: {e}")
        return
    n = sum(1 for c in nb.cells if c.cell_type == "code")
    rep.add("PASS", f"Executed in a clean kernel ({n} code cells, no errors)")


def check_blueprint(path: Path, lesson_text: str, rep: Report) -> None:
    text = path.read_text(encoding="utf-8")
    need = ["central question", "learning outcomes", "prerequisites", "sequence",
            "outcome alignment", "misconceptions"]
    heads = {h.group(2).strip().lower() for h in map(HEADING_RE.match, text.splitlines()) if h}
    missing = [n for n in need if not any(h.startswith(n) for h in heads)]
    rep.check(not missing, "Blueprint has required sections", f"missing: {missing}")
    bp_out = re.search(r"^##\s+learning outcomes.*?$(.*?)(^##\s|\Z)", text, re.I | re.M | re.S)
    if bp_out:
        n_bp = len(re.findall(r"^\s*\d+[.)]\s+", bp_out.group(1), re.M))
        prose = strip_code_fences(lesson_text)
        lm = [x for x in parse_markers(prose) if x["kind"] == "outcomes"]
        n_lesson = len(outcomes_after(prose, lm[0]["pos"])) if lm else 0
        rep.check(n_bp == n_lesson, "Blueprint and lesson outcome counts match",
                  f"blueprint {n_bp}, lesson {n_lesson}", warn=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lesson", type=Path)
    ap.add_argument("--kind", choices=["general", "paper"], default="general")
    ap.add_argument("--blueprint", type=Path)
    ap.add_argument("--execute", action="store_true", help="execute notebook in a clean kernel")
    ap.add_argument("--timeout", type=int, default=120, help="per-cell timeout in seconds")
    args = ap.parse_args(argv)

    if not args.lesson.exists():
        print(f"error: {args.lesson} not found", file=sys.stderr)
        return 2
    rep = Report()
    print(f"Structural check: {args.lesson}\n")
    if args.lesson.suffix == ".ipynb":
        check_notebook(args.lesson, args, rep)
        lesson_text = ""
        if args.blueprint:
            try:
                nb = json.loads(args.lesson.read_text(encoding="utf-8"))
                lesson_text = "\n\n".join(
                    "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
                    for c in nb.get("cells", []) if c.get("cell_type") == "markdown")
            except (json.JSONDecodeError, KeyError):
                pass
    else:
        check_markdown(args.lesson, args, rep)
        lesson_text = args.lesson.read_text(encoding="utf-8")
    if args.blueprint:
        if args.blueprint.exists():
            check_blueprint(args.blueprint, lesson_text, rep)
        else:
            rep.add("FAIL", "Blueprint exists", str(args.blueprint))
    rep.print()
    return 1 if rep.failed else 0


if __name__ == "__main__":
    sys.exit(main())
