# Review: Solving Two-Step Equations — Undoing What Was Done to $x$

Lesson: `lesson.md` · Blueprint: `lesson.blueprint.md` · Learner: adult, comfortable with arithmetic, no algebra.

## Structural check

Command (run from this directory):

```bash
python3 ../../skills/lesson-architect/scripts/check_lesson.py lesson.md --blueprint lesson.blueprint.md
```

- First draft: **29 passed, 0 warnings, 0 failed.**
- After all revisions (final run): **29 passed, 0 warnings, 0 failed.**

The checker only confirms markers, order, and alignment (e.g. every outcome tagged on some exercise, guided before independent, solutions separated). It passed on the first draft even though the continuity audit below then found eight real defects — so this result is not evidence of teaching quality.

## Continuity audit

Done as a cold read in the role of the stated learner, top to bottom, after the first checker run.

**Term and notation trace** (first use → where explained):
unknown / $x$ (§2 "The letter") · $3x$ = $3 \times x$, $\cdot$ (§2) · equation, left/right side, $=$ as "same amount" (§2) · solution, substituting (§2) · multiply-before-add, PEMDAS/BODMAS (§2 worked example, **moved here in revision** — originally §3, after E1 needed it) · recipe and the machine arrows $x \to [\times 3] \to \dots$ (§3) · inverse operation (§3) · brackets, number-against-bracket = multiply (§3; the multiply meaning was **added in revision**) · both-sides rule (§4) · term, bracket counts as one term (§4; bracket clause **added in revision**) · fraction bar as division (§5; **moved before first use in revision**) · $\ne$ (E1 solution; definition **added in revision**) · $h$, $t$ as other letters (§7, "any letter works" stated in §2). Outcome list in the orientation uses terms before they are taught; a sentence telling the learner this is expected was **added in revision**.

**Transition trace** (opening sentence of each major section):
- §2: "Before we can solve anything, we need to be able to read the sentence and to recognise a correct answer…"
- §3: "We can now read the equation and check an answer. What is still missing is a way to *find* the answer directly."
- §4: "Running the recipe backwards in your head works… But it leaves no written trail…"
- §5: "We now have both ingredients: the recipe tells us *which* undo step comes next, and the both-sides rule tells us *how*…"
- §6: "So far, the recipe always *added* a number. If it subtracts instead, nothing new is needed…"
- §7: "The notebook problem started life as a story… this section shows how to build it yourself."
- Practice: "These exercises check every outcome without hand-holding…"
- Synthesis: "We started by asking how to find the unknown in $3x + 5 = 20$ reliably…"

**Outcome alignment:**

| Outcome | Taught in | Assessed by |
|---|---|---|
| 1 Check a solution by substitution | §2 (worked example: testing guesses) | E1, E7 |
| 2 Describe recipe / reverse undo order (incl. brackets) | §3 | E2, E6 |
| 3 Solve $ax \pm b = c$ with reasons and check | §4, §5, §6 | E3, E4, E7 |
| 4 Word problem → equation → solve → check | §7 (plumber) | E5 |
| 5 Adapt when order differs, e.g. $5(x-2)=35$ | §3 (brackets recipe for $3(x+5)$), §4 (bracket is one term), §5 ($\frac{3x}{3} = x$) | E6 |

Reverse check: no exercise assesses anything outside these outcomes (E1(c) assesses the "$3x$ as digits" misconception, which is part of outcome 1's reading of $3x$).

**Exercise prerequisites:**
- E1 needs: substitution, $3x$ meaning, multiply-before-add → all in §2 (the last one only after revision).
- E2 needs: recipe, inverse pairs incl. subtract↔add, reverse order → §3.
- E3 needs: E2's ideas + both-sides rule → §3–§5.
- E4 needs: subtraction case, non-whole answers → §6.
- E5 needs: translation routine, "per item" vs "once" amounts → §7.
- E6 (transfer) needs: brackets recipe and undo order (§3), bracket = one term (§4), dividing a multiplied quantity gives it back (§5). It deliberately requires *combining* these on a case not worked in full — that is the changed governing condition.
- E7 needs: substitution (§2) and the "change the sign" misconception repair (§5).
None depends on the optional section.

| Check | Verdict | Evidence / fix |
|---|---|---|
| Every learning outcome is taught and assessed | Pass | Table above; every row has a teaching section and ≥1 exercise. Outcome 5 is taught as a principle plus a recipe-reading example rather than a full worked solution — intentional so E6 is genuine transfer. |
| Exercises require no untaught concepts | Pass after revision | Draft E1 needed multiply-before-add, which was only taught in §3 (after E1); moved into §2. Draft E6 needed "a bracketed expression is one term" to avoid dividing $x$ and 2 separately by 5; added to §4. Draft E1(b) solution mentioned $5 \times (3-4)$ (brackets and a negative, both untaught at that point); rewritten. |
| Terminology and notation are introduced before use | Pass after revision | Trace above. Fixed: fraction bar explained after its first display; $\ne$ undefined; "number against a bracket means multiply" unstated; outcomes list previews untaught symbols (added reassurance sentence). |
| Transitions preserve the learning thread | Pass | Each major section's opening sentence quoted above states what we have, what is missing, and what the section supplies; the running example $3x + 5 = 20$ appears in §1, §2, §3, §5, §7, synthesis. |
| Worked examples explain reasoning | Pass after revision | Each step in §5 has Goal / Move / Why / Quick check; method choice (subtract before divide, and why dividing first is legal but messier) is explained with a self-explanation prompt. Fixed: the draft did not say *why* $3x + 5 - 5$ becomes $3x$ or *why* $\frac{3x}{3}$ becomes $x$ — both now stated. The plumber example is more compact (steps 1–5 of the routine) but each move still carries its reason. |
| Followable without filling missing conceptual steps | Pass, with a caveat | After the fixes I could not find a step the stated learner must supply. Caveat: mixed numbers ($1\tfrac{2}{3}$) appear in the divide-first discussion and a misconception box; I assumed an adult with arithmetic can follow them (a "three lots of $1\tfrac23$ is $3 + 2 = 5$" aid was added). Not tested on a real learner. |
| Analogies state their limits | Pass | Socks-and-shoes: gives only order, not which inverse; fails when $x$ appears twice. Balance scale: no negative weights, says nothing about divide-by-zero. Machine picture's limit shown in the optional peek. |
| Misconceptions confronted where they arise | Pass | "$3x$ = 35" at first use of $3x$ (§2, and E1(c)); "undo in reading order" via prediction prompt in §3 and divide-first discussion in §5; "divide only part of a side" and "move it across and flip the sign" in §5, each carried to a wrong answer and refuted by substitution (E7 targets the second); ignoring brackets in E6's solution. |
| Synthesis answers the central question | Pass | Answers "how, reliably, and how to be sure" using recipe → reverse undo → both-sides rule → substitution, revisits $3x + 5 = 20 \to x = 5$, states boundaries and next step. |
| Shape: varied headings, student voice, optional marked | Pass | Headings are content-named; no repeated sub-headings; optional peek is in a `<details>` labelled "Optional" and no exercise or later essential section needs it. |
| Rendering / readability without a renderer | Pass after revision | Draft had consecutive lines (`*Goal:*`/`*Move:*`, `(a)`/`(b)`, solution lines) that Markdown would merge into one paragraph; paragraph breaks inserted. Draft blanks `\underline{\quad}` and `[\ \ ?\ \ ]` were unreadable as raw text; replaced with `[ ? ]` / `[\,?\,]`. Currency is written as "dollars" to avoid clashes with `$` math delimiters. |

## Correctness audit

| Check | Verdict | Evidence / fix |
|---|---|---|
| Claims, calculations, and code checked | Pass | Two independent Python checks, both using `fractions.Fraction` for exact arithmetic (see below). No code in the lesson. Mathematical claims (inverse operations; doing the same operation to both sides preserves equality except division by zero; multiply-before-add convention; brackets first) are standard and stated without overreach. |
| Every worked answer verified by substitution | Pass | $3x+5=20 \Rightarrow 5$; $2x-9=7 \Rightarrow 8$; $2x+1=8 \Rightarrow 3.5$; $25h+40=115 \Rightarrow 3$; optional $3x+5=x+9 \Rightarrow 2$ (both sides 11). |
| Every exercise solution verified | Pass | E1 (15 ✓; 11 ≠ 10; $4x = 8$); E2 (7, 7); E3 (6); E4 (6, 2.5); E5 (5); E6 (9); E7 (6). |
| Every "wrong answer" in misconceptions/solutions really is wrong, with the stated value | Pass | $1\tfrac23 \to 10$; $12 \to 41$; E2 divide-first $7.25 \to 6.25 \to 26$; E3 $20 \to 87$; E4a $36/7$ not whole and fails; E5 $t=4 \to 52$; E6 $7.4 \to 27$; E7 $20 \to 86$. |
| Divide-first alternative really gives the same answer | Pass | $x + \tfrac53 = \tfrac{20}{3} \Rightarrow x = 5$. |

**Verification method.**

1. *Hand-listed checks:* a Python script with `from fractions import Fraction` asserting 33 facts — every guess, every solving step, every check, every wrong-path value listed in the table above, the divide-first route, and the optional example. Result: 33/33 OK.
2. *Automated sweep:* a second script extracted every `$...$` / `$$...$$` math span from `lesson.md`, kept those that are purely numeric equality chains (e.g. `3 \times 6 + 5 = 18 + 5 = 23`, mixed numbers via `\tfrac`, `\frac`), and evaluated every part exactly. Result: 38 chains evaluated; the only non-equal ones are the two deliberate questions "Is $17 = 20$?" and "Is $23 = 20$?", which the lesson answers "No". The sweep was run on the final text; the hand-listed checks encode the numbers independently of the file and still match it (the only numeric change in revision was the added "$3 + 2 = 5$" aid, which both cover).

## Revisions made

1. **Order of operations moved earlier.** Multiply-before-add (and PEMDAS/BODMAS) is now stated in §2's worked example, because E1 needs it; §3 now refers back to it instead of introducing it.
2. **Outcomes preview reassurance.** Added a sentence after the outcome list saying unfamiliar symbols will be explained before they are needed.
3. **Brackets imply multiplication.** §3 now says a number written against a bracket means multiply, and that brackets override multiply-before-add.
4. **A bracket is one term.** §4's definition of "term" now says bracketed groups count as a single term — needed so that E6's "divide both sides by 5" is unambiguous.
5. **Worked-example step justifications.** §5 now explains why $3x + 5 - 5$ leaves $3x$ and why $\frac{3x}{3}$ is $x$; the fraction-bar notation is explained *before* the display that uses it.
6. **Mixed-number aid.** The "divide only part of a side" box now shows how $3 \times 1\tfrac23 = 5$.
7. **Untaught notation removed from a solution.** E1(b)'s solution no longer mentions $5 \times (3-4)$ (brackets and a negative); $\ne$ is defined where used.
8. **Optional peek gap.** Explained $3x - x = 2x$ ("three lots take away one lot").
9. **Raw-text readability.** Replaced LaTeX blank macros in E2/E3 with readable `[ ? ]` boxes; added a reminder in E2 that subtracting is undone by adding.
10. **Markdown paragraph merging.** Inserted blank lines so Goal/Move/Why/Check lines, (a)/(b)/(c) parts, and solution paragraphs render separately; separated E3's "likely wrong answer" sentence from the preceding list.
11. **Blueprint updated** to match: order of operations now taught in §2; "bracket counts as one term" added to the §4 prerequisite row.

After the revisions the structural checker was re-run (29/0/0) and both calculation scripts were re-run (all OK); the changed passages were re-read against the term trace.

## Not verified / limitations

- **No real learner tested.** The continuity audit is my own cold read in the learner's role; it cannot fully simulate someone who never understood algebra. The places most likely to cause friction are the mixed numbers in §5 and the transfer exercise E6.
- **Rendering not visually inspected.** Math was written for GitHub-style `$...$` rendering; I did not render it in a browser. `\tfrac`, `\frac`, `\ne`, `\to`, `\,` are standard MathJax/KaTeX.
- **No external sources.** Content is standard introductory algebra from my own knowledge; no references were consulted or listed, so the lesson has no Sources section.
- **Assumption about negatives:** the lesson avoids negative numbers entirely; a learner who meets $3x + 20 = 5$ is told only that negatives are out of scope (synthesis), not how to handle them.
- **Timing** ("30–45 minutes") in the blueprint is an estimate, not measured.
