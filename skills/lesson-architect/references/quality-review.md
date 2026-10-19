# Quality Review

Three separate passes, in this order. Each catches failures the others cannot. Record findings and fixes; deliver only after revision.

| Pass | Question it answers | Who/what does it |
|---|---|---|
| Structural check | Are the required parts present and in a sane order? | `scripts/check_lesson.py` (automated) |
| Continuity audit | Can the stated learner follow this without filling gaps? | You, reading as the learner |
| Correctness audit | Is everything true, computed right, and runnable? | You, with sources, recomputation, and execution |

**A passing structural check does not show the lesson teaches well.** It cannot tell whether an explanation is clear, a transition is meaningful, or an exercise is fair. Never report it as evidence of teaching quality.

## 1. Structural check

```bash
python3 <skill-dir>/scripts/check_lesson.py LESSON.md --blueprint LESSON.blueprint.md [--kind paper]
python3 <skill-dir>/scripts/check_lesson.py LESSON.ipynb --blueprint LESSON.blueprint.md --execute   # needs nbformat, nbclient, ipykernel
```

It reads invisible HTML-comment markers. Keep them in the lesson; they do not render. Place each marker immediately before the content it labels (before or after that section's heading — either works). In notebooks, markers are read per markdown cell, so a `la:predict` and the following `la:interpret` must be in separate cells with the experiment code cell between them.

| Marker | Meaning | Rule enforced |
|---|---|---|
| `<!-- la:orientation -->` | Start of the orientation | Required; first marker |
| `<!-- la:outcomes -->` | Next numbered list = learning outcomes | Required; 2–8 items recommended |
| `<!-- la:worked-example -->` | A fully reasoned worked example | ≥1; first one precedes the first exercise |
| `<!-- la:misconception -->` | A misconception and its repair | ≥1 |
| `<!-- la:exercise id=E1 outcomes=1,3 level=guided -->` | An exercise statement | levels: `guided`, `independent`, `transfer`, `check` (`check` = a quick comprehension question allowed anywhere, outside the guided → independent order); ≥1 guided before the first independent; every outcome assessed; ids unique |
| `<!-- la:hint id=E1 -->` | A hint for E1 | After E1; in the solutions area or a `<details>` block; warning if an independent/transfer exercise has none |
| `<!-- la:solution id=E1 -->` | Full solution for E1 | Required for every exercise; after E1; in the solutions area or a `<details>` block |
| `<!-- la:solutions -->` | Start of the hints-and-solutions area | Required unless every hint/solution is in `<details>` |
| `<!-- la:synthesis -->` | The closing synthesis | Required; after the first worked example |
| `<!-- la:optional -->` | Start of optional depth | Optional |
| `<!-- la:sources -->` | Sources list | Required with `--kind paper` (must contain a URL); include it in any lesson whose factual claims rely on outside sources (e.g. public-domain status of a melody, historical dates) |
| `<!-- la:paper-claim -->`, `<!-- la:interpretation -->`, `<!-- la:limitations -->` | Paper claim vs. explanation vs. limits | Each required at least once with `--kind paper`; mark every block that states what the paper says with `la:paper-claim` and every block of your own explanation/examples with `la:interpretation` |
| `<!-- la:predict -->`, `<!-- la:interpret -->` | Notebook prediction and interpretation cells | Notebook: ≥1 predict → code → interpret cycle; each predict is followed by code then interpret |

It also flags: missing title, leftover template placeholders, unbalanced code fences or `$$`, the same heading (level 2 or deeper) repeated three or more times (template monotony), teacher-facing phrasing, notebooks with stored outputs, and notebook cells that fail in a clean kernel (`--execute`).

## 2. Continuity audit (teaching quality)

Re-read the whole lesson as the stated learner, top to bottom, without using anything you know that the lesson has not yet said.

1. **Term and notation trace.** List every technical term and symbol in order of first appearance. For each, find where it is *explained* (not merely mentioned). Any term used before its explanation is a defect.
2. **Step trace.** In each worked example and derivation, check that every step follows from what was shown, using only taught ideas. Mark any step where the learner would have to supply a missing idea.
3. **Transition trace.** For each major section, quote the sentence that says why it comes next. If there isn't one, or it is generic ("Now let's look at…"), fix it.
4. **Outcome alignment.** Build a table: outcome → section(s) that teach it → exercise(s) that assess it. Every row needs both. Also check the reverse: does any exercise assess something no outcome names?
5. **Exercise prerequisites.** For each exercise, list what it requires. Each item must be taught in an essential (non-optional) section earlier in the lesson.
6. **Worked-example quality.** For each step, is there a reason as well as a result? Is method selection explained?
7. **Analogy boundaries and misconceptions.** Does every analogy say where it fails? Is each planned misconception actually confronted where it arises?
8. **Synthesis.** Does it answer the central question from the opening, using the lesson's pieces?
9. **Shape.** Are headings varied and content-driven? Is anything teacher-facing? Is optional depth marked and not required later?

## 3. Correctness audit (facts)

Separate from the teaching audit; a lesson can teach beautifully and be wrong.

- **Calculations:** recompute every number, ideally with code (exact arithmetic where possible). Check worked answers by substitution. For numeric claims in prose (e.g. "0.1 is stored as 0.1000000000000000055…"), write a short script that recomputes each one and asserts it; keep the script in your working area and report how many claims it checked.
- **Code:** run every snippet as shown; for notebooks execute top-to-bottom in a clean kernel. Record versions when behaviour is version-dependent.
- **Paper claims:** for each "the paper reports/claims" statement, locate the supporting sentence, table, or figure and confirm numbers and hedges match. Check that your own interpretations are labelled as such.
- **Domain facts:** definitions, names, dates, and conventions (e.g. piano finger numbers, note names, tempo marks) against a reliable source or your verified knowledge; if uncertain, say so in the lesson or remove the claim.
- **Sources:** every listed source was actually consulted; no invented URLs.

## 4. Revision loop

Fix every defect, then re-run the structural check and re-audit the parts you changed. Stop when the continuity and correctness audits find no defects that would block the stated learner.

## 5. Review record

For saved examples and evaluations, write `review.md` beside the lesson using this outline:

```markdown
# Review: <lesson>

## Structural check
<command run, result, warnings>

## Continuity audit
| Check | Verdict | Evidence / fix |
|---|---|---|
| Every learning outcome is taught and assessed | … | … |
| Exercises require no untaught concepts | … | … |
| Terminology and notation are introduced before use | … | … |
| Transitions preserve the learning thread | … | … |
| Worked examples explain reasoning | … | … |
| Followable without filling missing conceptual steps | … | … |
| Analogy boundaries and misconceptions | … | … |
| Synthesis answers the central question | … | … |
| Shape, voice, and optional depth | … | … |

## Correctness audit
| Check | Verdict | Evidence / fix |
|---|---|---|
| Claims, calculations, and code checked | … | <summary; details in rows below> |
| … one row per claim, calculation group, or code cell … | … | … |

## Revisions made
- …

## Not verified / limitations
- …
```
