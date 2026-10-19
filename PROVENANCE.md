# Provenance

How `lesson-architect` was designed, what it learned from, and what was copied (nothing verbatim).

Inspection date: 2026-10-19.

## Sources inspected

### 1. Tutor skill — `JabariD/agent-skills`, `skills/tutor/`

- **URL:** https://github.com/JabariD/agent-skills/tree/main/skills/tutor
- **Commit inspected:** `4d715f0d0fb1fcaaff6750c95de861d70ad9b5a5` (2026-10-17)
- **Files read:** `README.md`, `skills/tutor/SKILL.md`, `references/teaching-loop.md`, `references/practice-and-assessment.md`, `references/self-check.md`; section outlines of `learning-program.md`, `learning-artifacts.md`, `sources.md`.
- **Relevance:** high. This matches the "Tutor" lead: first-principles teaching, practice, assessment, and course creation. It is designed for interactive tutoring and persistent courses, not for authoring standalone lesson documents.
- **License:** **none found.** The repository has no `LICENSE` file and the GitHub API reports no license. Under default copyright, no text from it may be reused.
- **Decision:** ideas only, re-expressed in original wording. No text, structure, or file copied.
- **Ideas that informed this skill** (general teaching principles, several of which the Tutor skill itself attributes to published research such as Bjork & Bjork on retrieval vs. storage strength):
  - Assisted or fluent performance is not evidence of mastery; prefer unseen problems and changed conditions as evidence (→ `references/tutor-mode.md`, "Evidence, not impressions").
  - Ask for an attempt or prediction before explaining when the learner has a foothold (→ tutor mode; predictions in notebooks).
  - A progressive hint ladder that discloses as little as possible before the answer (→ `pedagogy.md` §9, tutor mode).
  - Vary the *governing condition*, not just the surface story, when testing transfer (→ `pedagogy.md` §8, math "Transfer").
  - Literal explanation before analogy; analogies only when the causal structure matches (→ `pedagogy.md` §6, extended with explicit boundary statements).
  - Don't turn a simple request into an intake interview (→ `SKILL.md` step 1).
- **Not adopted:** persistent course files, ledgers, calibration scoring, spaced-retrieval scheduling. The brief excluded persistent learner databases.

### 2. "Lesson Plan Generator" — `Sallvainian/School-Year-25-26`

- **URL given:** https://github.com/Sallvainian/School-Year-25-26/tree/main/lesson-plan-generator/lesson-plan-generator
- **Result:** **not accessible.** The page and the GitHub API return 404, and the repository does not appear among the user's public repositories. It may have been deleted or made private.
- **What was seen:** only third-party marketplace copies of its description and partial `SKILL.md` text (mcpmarket.com and agentskills.in). These copies cannot be tied to a specific commit, file set, or license.
- **Decision:** not used as a source. Its visible ideas (Bloom's-verb objectives, 3–5 segments each with a transition, timed teacher procedure, .docx export) are either generic instructional-design practice or teacher-facing features this skill deliberately avoids. Nothing copied.

### 3. Lesson plan skill — `Dragon-01-you/lesson-plan-skill` (suggested alternative for source 2)

- **URL:** https://github.com/Dragon-01-you/lesson-plan-skill
- **Commit inspected:** `6a9e62b8ec89bd4301e9dc36f7bdf7feb2e2c891` (2026-08-06, branch `master`)
- **Files read:** `LICENSE`, `skills/lesson-plan/SKILL.md` (Chinese), `skills/lesson-plan/quality/checklist.md`, `scripts/quality-checker.py`, `skills/lesson-plan/evals/evals.json`; file listing of `references/`.
- **Relevance:** medium. It generates teacher-facing K-12 lesson plans in Chinese (timings, differentiation, classroom management). Its structural ideas transfer; its audience and format do not.
- **License:** MIT, © 2026 Dragon-01-you.
- **Decision:** ideas only; no text or code copied, so MIT's notice requirement is not triggered. Credited here anyway.
- **Ideas that informed this skill:**
  - Each misconception paired with the correct understanding (→ `la:misconception` blocks).
  - A separate student handout with teacher notes removed — taken further here: the lesson is student-facing from the start, and the blueprint is the separate author artifact.
  - Ask at most one question, choosing the parameter that most affects the design (→ `SKILL.md` step 1).
  - A machine-readable eval file per test case (→ `evals/cases.json`).
- **Counter-example adopted deliberately:** its `quality-checker.py` scores lessons by keyword presence (for example, whether the word for "misconception" appears) and reports a percentage "total score". This skill's checker instead verifies explicit markers, ordering, and outcome-to-exercise alignment, and states every time it runs that passing does not show teaching quality.

## Specifications consulted (conventions, not content)

- GitHub Docs, *Adding agent skills for GitHub Copilot CLI*: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills (personal skills in `~/.copilot/skills/<name>/SKILL.md`; required `name`/`description`; optional `license`; `/skills reload`, `/skills info`; `/<skill-name>` invocation).
- GitHub Docs, *About agent skills*: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- Agent Skills specification: https://agentskills.io/specification (name ≤ 64 chars and matches the directory; description ≤ 1024 chars; `references/`, `assets/`, `scripts/` layout; keep `SKILL.md` short and load references on demand).
- Local check: `copilot skill --help` and `copilot skill list` on GitHub Copilot CLI 1.0.81-11.

## Sample-lesson sources

- He, Zhang, Ren, Sun. *Deep Residual Learning for Image Recognition*. arXiv:1512.03385v1 (2015). https://arxiv.org/abs/1512.03385 — read in full for the research-paper sample; claims checked against the text (see `examples/paper-resnet/review.md`).

## License of this skill

Apache-2.0, matching this repository's `LICENSE`.
