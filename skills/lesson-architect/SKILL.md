---
name: lesson-architect
description: >
  Designs and writes coherent, student-facing lessons as Markdown documents or
  executable Jupyter notebooks, using a blueprint, draft, continuity audit, and
  revision workflow. Use when the user asks to create a lesson, tutorial,
  explainer, or worked-example study guide on mathematics, a research paper,
  piano practice, or an unfamiliar technical topic, or asks to "teach me" a
  topic as a document or notebook. Also use for interactive tutoring when the
  user explicitly asks to be tutored, quizzed, or taught step by step in chat.
  Not for teacher-facing lesson plans, quick factual answers, or plain summaries.
license: Apache-2.0
---

# Lesson Architect

Produce lessons that are deliberately *taught*: every section has a reason to exist, arrives when the learner is ready for it, and moves toward one destination. Length, headings, and quizzes are not teaching quality.

## Choose the mode

- **Author mode (default).** Produce one complete standalone lesson file. Do not turn authoring into an interview.
- **Tutor mode (only when explicitly requested,** e.g. "tutor me", "quiz me", "teach me interactively"). Follow [references/tutor-mode.md](references/tutor-mode.md) and skip the file workflow below.

## Author workflow

### 1. Establish the brief

Pin down four things: **starting knowledge**, **destination** (what the learner should be able to do afterwards), **scope**, and **format**.

- Infer what you can from the request and any attached material.
- Ask at most one or two questions, and only when the answer would materially change the lesson (for example, "Have you used derivatives before?" for an optimization lesson). Otherwise state your assumptions and proceed. When you cannot ask (non-interactive runs), record assumptions in the blueprint's *Brief* and in the lesson's "Who this is for" line.
- Format: default to Markdown. Choose a Jupyter notebook only when the user asks for one or when running and modifying code is itself how the learner will learn. Never force a notebook onto material better served by prose (piano, most proofs, most paper readings).
- For a research paper, obtain and read the actual paper before planning. If you cannot access it, say so and do not teach claims you have not seen.

### 2. Write the blueprint before drafting

Fill [assets/blueprint-template.md](assets/blueprint-template.md) and save it beside the lesson as `<lesson-name>.blueprint.md` (unless the user asks for a single file; then keep it in working notes). It must contain:

- the central question and the motivating problem;
- 3–6 observable learning outcomes (the checker warns outside 2–8; aim for 3–6) ("compute…", "explain why…", "decide whether…");
- prerequisite concepts in dependency order, marking which are assumed and which this lesson teaches;
- the section sequence, each with its *purpose* and *why it comes next*;
- a running example, if one can carry the lesson;
- an outcome → where taught → where assessed table;
- the likely misconceptions to confront.

Before filling it, skim [references/pedagogy.md](references/pedagogy.md) and the matching section of [references/subject-adaptations.md](references/subject-adaptations.md): the blueprint's misconceptions and progression depend on them. The blueprint guides the work; the student never needs to see it.

### 3. Draft the lesson from the blueprint

Keep those references at hand while drafting. Start from [assets/lesson-template.md](assets/lesson-template.md) or [assets/notebook-template.ipynb](assets/notebook-template.ipynb). The templates carry invisible `<!-- la:... -->` markers that the structural checker reads; keep them, but write your own headings.

Non-negotiables:

1. Open with orientation: what we are learning, why it matters, where the lesson is going.
2. Introduce every term, symbol, and assumption before relying on it.
3. Each major section says, in a sentence or two, why it comes next.
4. Concrete before abstract when that helps; always connect intuition to the formal reasoning; state where an analogy stops working.
5. Worked examples show the *reasoning* for each step, not just the result. Explain both how a method works and why it is the right method here.
6. Practice progresses worked → guided → independent. Every exercise needs only what was taught. Hints and solutions live apart from the statements; independent and transfer exercises get at least one hint.
7. Name at least one real misconception and repair it.
8. Close with a synthesis that answers the central question using the pieces built.
9. Mark optional depth as optional.

### 4. Audit, in three separate passes

Follow [references/quality-review.md](references/quality-review.md).

1. **Structural check (automated):** `python3 <skill-dir>/scripts/check_lesson.py <lesson-file> --blueprint <lesson-name>.blueprint.md` (add `--kind paper` for papers; always add `--execute` for notebooks, and if Jupyter packages are unavailable report the notebook as not executed). Paths are relative to where you run it; the blueprint and `review.md` live beside the lesson. Passing it proves structure only.
2. **Continuity audit (teaching):** cold-read as the stated learner; trace every term and step to where it was introduced; check transitions, outcome coverage, and exercise prerequisites.
3. **Correctness audit (facts):** recompute calculations, run code in a clean kernel, check every paper claim against the paper, check musical facts. Put verification scripts in your working area, not in the student-facing lesson, and summarize what they checked in the delivery note (or `review.md`).

### 5. Revise, then deliver

Fix every gap found, re-run the checks, and deliver the lesson with a short note in your reply (not inside the lesson) listing: assumptions made, files written, what was verified (and how), and anything not verified or not executed.

## Paths

All paths above are relative to this skill's directory (`<skill-dir>`, typically `~/.copilot/skills/lesson-architect`). The checker uses only the Python standard library; `--execute` additionally needs `nbformat`, `nbclient`, and `ipykernel`.
