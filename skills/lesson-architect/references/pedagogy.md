# Pedagogy for Authored Lessons

How to turn a blueprint into a lesson a learner can follow without filling in missing steps. Read before drafting.

## Contents

1. The learning thread
2. Orientation
3. Ordering by dependency
4. Transitions
5. Concrete, abstract, and the bridge between them
6. Analogies and their boundaries
7. Worked examples that teach reasoning
8. Practice: worked → guided → independent
9. Hints and solutions
10. Misconceptions
11. Synthesis
12. Essential versus optional
13. Formatting that survives rendering
14. Anti-patterns

## 1. The learning thread

A lesson is one argument, not a collection of facts. The **central question** is the thread; each section either supplies a piece the answer needs or tests that the piece is in place. When drafting a section, be able to finish the sentence "The learner needs this now because…". If you cannot, the section is digression: cut it, move it, or mark it optional.

A **running example** is the cheapest way to keep the thread visible. Introduce it in the opening, return to it after each new idea ("here is what that buys us on our problem"), and solve it fully near the end. Change it only on purpose, and say why (usually to show transfer).

## 2. Orientation

The first screen answers three questions in plain language:

- **What** are we learning? One or two sentences, no undefined jargon.
- **Why** does it matter? A concrete problem the learner can feel, ideally the running example.
- **Where** is this going? The destination as observable outcomes, and a short route map ("first we…, then…, finally…").

State who the lesson is for and what it assumes, so a learner can tell immediately whether to start elsewhere.

Write the outcomes in plain words the learner already knows. If an outcome must name a term the lesson will teach, give it a short gloss there or say plainly that each term will be explained before it is needed; the "introduce before use" rule applies to *relying* on a term, not to previewing it.

## 3. Ordering by dependency

List the concepts the destination requires and draw the "needs" arrows between them. Teach in an order where every arrow points backwards. Typical failures:

- Using a symbol in an example before defining it.
- Defining a term in passing inside a sentence about something else, then relying on it heavily.
- Presenting a method, then later explaining the idea that motivates it.
- Exercises that need a fact only mentioned in a footnote or optional section.

Introduce a term with its meaning first and its name second ("the amount left over after… — we call this the *residual*"). Define notation where it is first used, and restate it briefly if it returns after a long gap.

## 4. Transitions

Each major section opens with one or two sentences that link backwards and forwards: what we now have, what is still missing, and how this section supplies it. This is not a ritual heading; it is the reason the section exists. Vary the wording. A useful test: delete the section title and check that the opening still tells the reader why they are here.

## 5. Concrete, abstract, and the bridge between them

Default order for new ideas: a specific case the learner can compute or picture, then the general pattern, then the formal statement, then back to a new specific case. Skip the concrete opening only when the learner already has a firm concrete model.

The bridge matters more than either end. After an intuition, show precisely which part of the formal statement captures it ("the 'pull back' we felt corresponds to the minus sign in…"). After a formal step, say what it means in the running example. Never let an analogy or picture *replace* the reasoning; it can only motivate or illustrate it.

Show the important intermediate steps. A step is important if a learner at the stated level could not produce it without help. When skipping routine algebra or code, say what was skipped.

## 6. Analogies and their boundaries

Use an analogy only when its causal structure matches the target. Immediately state:

- what the analogy gets right;
- where it breaks, preferably with a case where it predicts the wrong thing.

An analogy without a boundary becomes a misconception.

## 7. Worked examples that teach reasoning

A worked example teaches a *decision process*, not an answer. For each step, make visible:

- the goal of the step;
- why this move (and not a tempting alternative) serves that goal;
- a quick check that the step is valid.

Explain **why the method fits** the problem: which feature of the problem tells you to reach for it. Learners rarely fail at executing a known method; they fail at recognizing when it applies.

Insert short **self-explanation prompts** ("Before reading on: why can we divide both sides by 3 here?") at the decision points. Keep the answer immediately below for worked examples; the point is to make the learner think, not to test them.

## 8. Practice: worked → guided → independent

Sequence practice by fading support:

1. **Worked example** — fully reasoned, as above.
2. **Guided practice** — a near-identical problem with the structure given and key steps left for the learner; one or two prompts.
3. **Independent practice** — a fresh problem with no scaffolding in the statement.
4. **Transfer** (where appropriate) — change a *governing condition* (the constraint, the data shape, the tempo, the assumption), not just the surface story, so the learner must decide whether and how the method still applies.

Short **checks** (level `check`) can appear anywhere, including inside teaching sections before guided practice: quick comprehension questions or error-spotting tasks that confirm a just-taught idea landed.

Transfer is not a licence to require new material. The changed condition must be resolvable by reasoning with ideas the lesson taught, and the lesson should already have shown *what to check* when conditions change (e.g. "find the order the steps were done" before an exercise where brackets reorder them).

Every exercise must be solvable with what the lesson taught. Tag each exercise with the outcomes it assesses, and make sure every outcome is assessed at least once. Prefer producing an answer or an explanation over recognizing one; when you do use multiple choice, make every distractor a mistake someone would actually make, and vary the position of the correct option.

Include a **prediction** before any experiment, demonstration, or reveal: asking the learner to commit to an expectation makes the result informative.

## 9. Hints and solutions

Keep exercise statements clean. Put hints and full solutions in a separate block after the exercises (or in collapsed `<details>` blocks), so a learner can attempt first. Every exercise needs a solution; independent and transfer exercises should also have at least one hint (the checker warns otherwise). Hints are graded: the first narrows the problem without naming the operation; a later hint names the next decision; the solution shows full reasoning, plus the most likely wrong answer and why it is wrong.

## 10. Misconceptions

For the topic, name the misconceptions that a learner at this level actually holds. For each: state it fairly, show a case where it gives the wrong result, explain the correct model, and if possible include an exercise that would catch it. Place the repair where the misconception would naturally arise, not in an appendix.

## 11. Synthesis

End by answering the central question in a few paragraphs, explicitly using the pieces built: "We started by asking…; we saw that…; therefore…". Revisit the running example in its final form. Then name what the learner can now do (the outcomes, in their words), the boundary of what this lesson covered, and one sensible next step.

A bullet list of every heading is not a synthesis.

## 12. Essential versus optional

Mark optional depth clearly (an "Optional:" prefix, a collapsed `<details>` block, or a clearly labelled section). Optional material may never be required by an exercise or by a later essential section.

## 13. Formatting that survives rendering

- Put step structure (goal / move / why / check) on separate list items or separate paragraphs; consecutive lines merge into one paragraph in Markdown.
- In lessons that use `$...$` math, write currency as "5 dollars" or escape it (`\$5`) so renderers do not treat it as math.
- For fill-in blanks, use `[ ? ]` in prose or `\square` inside math; avoid unreadable raw-LaTeX spacing tricks.
- Check that display math, tables, and `<details>` blocks render (blank line after `<summary>…</summary>`).

## 14. Anti-patterns

- **Encyclopedic sprawl:** many facts, no destination. Fix: cut anything that does not serve the central question.
- **Abrupt jumps:** a new idea appears with no stated reason. Fix: add the transition, or move the section.
- **Template monotony:** every section has the same "Definition / Example / Quiz" sub-headings. Fix: let the content decide the shape.
- **Answer-display examples:** steps shown without why. Fix: add the goal and justification for each step.
- **Quiz padding:** recall questions that test vocabulary rather than the outcomes. Fix: tie every exercise to an outcome; remove the rest.
- **Teacher-facing voice:** "Students will…", timings, classroom logistics. Fix: address the learner directly.
- **Analogy as explanation:** a story where the mechanism should be. Fix: add the formal link and the analogy's boundary.
