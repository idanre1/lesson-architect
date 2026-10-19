# lesson-architect

A Copilot CLI agent skill that writes **student-facing lessons that are deliberately taught**, as Markdown documents or executable Jupyter notebooks, for mathematics, research papers, piano practice, and unfamiliar technical topics.

It replaces "detailed but disconnected" output with a fixed workflow:

**brief → blueprint → draft → structural check → continuity audit → correctness audit → revision**

- The **blueprint** (central question, observable outcomes, prerequisite order, a purpose for each section, outcome→exercise alignment, misconceptions) is written *before* drafting and saved beside the lesson.
- The **continuity audit** (can the stated learner follow it without filling gaps?) and the **correctness audit** (are claims, numbers, and code right?) are separate passes.
- An automated **structural checker** verifies required parts, ordering, and outcome coverage, and says every time that passing it does not prove teaching quality.

Two modes: **Author** (default; one complete lesson file, no interview) and **Tutor** (only when asked; interactive, diagnostic, evidence-based).

## Layout

```text
skills/lesson-architect/          ← the skill (this folder is what gets installed)
├── SKILL.md                      ← triggers + workflow (compact)
├── references/
│   ├── pedagogy.md               ← how to teach in an authored lesson
│   ├── subject-adaptations.md    ← papers, math, piano, technical, notebooks
│   ├── quality-review.md         ← structural/continuity/correctness audits, marker spec
│   └── tutor-mode.md             ← interactive mode
├── assets/
│   ├── blueprint-template.md
│   ├── lesson-template.md
│   └── notebook-template.ipynb   ← genuine nbformat-4 notebook
└── scripts/check_lesson.py       ← structural checker (stdlib; optional nbformat/nbclient)
examples/                         ← four sample lessons, each with blueprint + review
evals/                            ← evaluation cases, defective fixtures, runner
PROVENANCE.md                     ← sources inspected, ideas borrowed, licensing decisions
```

## Install (Copilot CLI, personal skill)

Verified against GitHub's docs ([Adding agent skills for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)) and Copilot CLI 1.0.81-11. Personal skills live in `~/.copilot/skills/<name>/`.

```bash
git clone https://github.com/idanre1/lesson-architect.git
cd lesson-architect
test -e ~/.copilot/skills/lesson-architect && echo "already exists; not overwriting" \
  || { mkdir -p ~/.copilot/skills && cp -r skills/lesson-architect ~/.copilot/skills/; }
copilot skill list | grep lesson-architect     # confirm discovery
```

In a running CLI session, use `/skills reload`, then `/skills info lesson-architect`.

**To update** after pulling changes: `rm -rf ~/.copilot/skills/lesson-architect && cp -r skills/lesson-architect ~/.copilot/skills/`.

Caveats:

- Do **not** use `copilot skill add skills/lesson-architect/SKILL.md`: for a file source the CLI copies only `SKILL.md`, dropping `references/`, `assets/`, and `scripts/`.
- `copilot skill add /path/to/lesson-architect/skills` (a *directory of skills*) also works and picks up edits live, but it writes the path into your Copilot settings.
- For a project-only install, copy the folder to `.github/skills/lesson-architect/` in that repository.

### Optional: notebook execution

The checker needs only Python 3.9+. To execute notebooks (`--execute`), use an environment with `nbformat`, `nbclient`, and `ipykernel`, for example:

```bash
uv venv ~/.venvs/lesson-architect && VIRTUAL_ENV=~/.venvs/lesson-architect uv pip install nbformat nbclient ipykernel
```

## Use

Copilot loads the skill automatically when a request matches its description, or explicitly with `/lesson-architect`:

```text
Use /lesson-architect to write a beginner Markdown lesson on solving two-step linear equations. I remember arithmetic but never understood algebra.

/lesson-architect Create a Jupyter notebook lesson on why 0.1 + 0.2 != 0.3 in Python. I know basic Python but not how numbers are stored.

/lesson-architect Teach me arXiv:1512.03385 (ResNet) as a Markdown lesson. I know layers, losses, and gradient descent, but not CNNs.

/lesson-architect A beginner piano practice lesson: I have a keyboard and want to play my first right-hand melody steadily.

/lesson-architect Tutor me interactively on eigenvectors. Ask me questions; don't write a file.
```

Each authored lesson is delivered with `<name>.blueprint.md` and a note stating assumptions, what was verified, and anything not executed.

Run the checker yourself:

```bash
python3 ~/.copilot/skills/lesson-architect/scripts/check_lesson.py lesson.md --blueprint lesson.blueprint.md
python3 ~/.copilot/skills/lesson-architect/scripts/check_lesson.py paper-lesson.md --kind paper
~/.venvs/lesson-architect/bin/python ~/.copilot/skills/lesson-architect/scripts/check_lesson.py lesson.ipynb --execute
```

## Evaluation

```bash
~/.venvs/lesson-architect/bin/python evals/run_evals.py   # plain python3 also works but skips notebook execution
```

- **Part A (automated, structural):** the four sample lessons must pass the checker (the notebook is executed in a clean kernel), and six defective fixtures (encyclopedic summary, misaligned practice, paper without claim separation, unfilled template, Markdown renamed `.ipynb`, crashing notebook) must be rejected for the expected reasons.
- **Part B (qualitative, recorded):** each sample has a `review.md` with continuity and correctness verdicts and evidence. The runner only checks that verdicts were recorded; the judgments themselves are human/agent review.

| Sample | Format | Folder |
|---|---|---|
| Two-step linear equations (beginner math) | Markdown | [examples/math-two-step-equations](examples/math-two-step-equations) |
| Floating-point numbers in Python (technical) | Jupyter | [examples/floating-point-notebook](examples/floating-point-notebook) |
| *Deep Residual Learning for Image Recognition* (paper) | Markdown | [examples/paper-resnet](examples/paper-resnet) |
| First right-hand melody (beginner piano) | Markdown | [examples/piano-first-melody](examples/piano-first-melody) |

## Limitations

- Structural checks cannot judge clarity, motivation, or fairness of exercises; those rest on the audits in `references/quality-review.md`, done by the same model that wrote the lesson unless you review them yourself.
- The sample lessons were produced by agents following the skill and then reviewed and revised; they have not been tested with real learners.
- The checker does not verify facts: paper quotes and numbers, calculations, and melodies are checked in the correctness audit, not automatically. In all four samples the first draft passed the checker while the audits still found real errors.
- Tutor mode is specified but not covered by automated evaluation.
- Piano lessons describe notes in letter names and rhythm values; the skill does not generate staff notation images.

## Provenance and license

See [PROVENANCE.md](PROVENANCE.md). Apache-2.0 (see [LICENSE](LICENSE)).
