# Blueprint: Solving Two-Step Equations — Undoing What Was Done to x

Working document for the author. Not shown to the learner.

## Brief

- **Learner:** an adult who is comfortable with whole-number arithmetic (add, subtract, multiply, divide, simple decimals such as 2.5) but never understood algebra. May half-remember "PEMDAS/BODMAS" and rules like "move it across and change the sign" without knowing why.
- **Destination:** solve equations like $3x + 5 = 20$ by undoing the operations in reverse order on both sides, explain each step, and check the answer.
- **Scope:** in — what an equation, an unknown and a solution are; reading $3x$; checking by substitution; build order vs. undo order; doing the same thing to both sides; equations of the form $ax + b = c$, $ax - b = c$; translating a short word problem; one transfer case with parentheses, $a(x - b) = c$. Out — negative numbers as answers or coefficients, fractions as coefficients, $x$ on both sides (optional peek only), inequalities, formal properties of equality by name.
- **Format:** Markdown. The learner needs prose, worked steps and pencil practice; running code would add nothing.
- **Assumptions made without asking:**
  - "Remembers arithmetic" means whole numbers and simple decimals; negative numbers are kept out of every essential part and every exercise answer.
  - The learner may never have seen "$3x$" notation, so it is taught from scratch.
  - No prior algebra vocabulary; every term (unknown, equation, solution, substitute, term, inverse operation) is introduced.
  - A single self-contained lesson of moderate length (roughly 30–45 minutes of reading plus practice) is wanted, not a course.
  - Dollar amounts in stories use "$" as currency; math is written with `$...$` delimiters, so story prices are written as "dollars" in words to avoid clashes with math rendering.
- **Sources read:** none external. Content is standard introductory algebra; every number is verified by exact computation (Python `fractions`) during the correctness audit.

## Central question

How can you find the unknown number in an equation like $3x + 5 = 20$ reliably — without guessing — and be sure your answer is right?

**Motivating problem:** You bought some notebooks at 3 dollars each and paid a 5-dollar delivery fee. The total was 20 dollars. How many notebooks did you buy? (Algebra writes this as $3x + 5 = 20$.)

## Learning outcomes

By the end, the learner can:

1. Check whether a given number is a solution of an equation by substituting it and comparing both sides.
2. Describe the "recipe" an equation applies to $x$ (its build order, including when parentheses change the order) and state the undo steps in reverse order.
3. Solve two-step equations of the form $ax + b = c$ and $ax - b = c$ by doing the same inverse operation to both sides, giving a reason for each step, and checking the result.
4. Turn a short word problem into a two-step equation, solve it, and check the answer against the story.
5. Adapt the method to an equation whose operations come in a different order, such as $5(x - 2) = 35$, and explain why the first undo step changes.

## Prerequisites

| Concept | Assumed or taught here? | Needed for |
|---|---|---|
| Whole-number arithmetic, simple decimals | assumed | everything |
| Multiplication before addition (order of operations) | taught (refreshed) in §2, used in §3 | substitution checks (E1), build order |
| Letter standing for an unknown number; $3x$ means $3 \times x$ | taught in §2 | everything after |
| Equation = statement that two sides are equal; solution; substitution check | taught in §2 | outcomes 1, 3 |
| Build order and undo in reverse; inverse operations; parentheses | taught in §3 | outcomes 2, 3, 5 |
| Same operation on both sides keeps an equation true; "term" (a bracket counts as one term) | taught in §4 | outcomes 3, 5 |
| Undoing subtraction by adding | taught in §6 (inverse pairs introduced in §3) | outcome 3 |
| Translating words to an equation | taught in §7 | outcome 4 |

Dependency order of taught concepts: letter & $3x$ → equation & solution → order of operations → substitution → build order / undo order / inverse operations → both-sides rule → full worked solution → subtraction case → word problems → transfer (parentheses).

## Sequence

| # | Section (working title) | Purpose | Why it comes next |
|---|---|---|---|
| 1 | Orientation | State the notebook problem, what we learn, outcomes, route | — |
| 2 | What $3x + 5 = 20$ is saying | Read the notation; define equation, solution; refresh multiply-before-add; check guesses by substitution; confront "3x = 35" | Nothing can be solved before the sentence can be read and an answer can be checked |
| 3 | The recipe hidden in the equation | Build order (from multiply-before-add) → undo in reverse with inverse operations; parentheses change the recipe; solve the running example by working backwards on numbers | Guessing is slow and fails for non-whole answers; the equation records what was done to $x$, so undoing it finds $x$ |
| 4 | Keeping both sides balanced | Turn mental "working backwards" into written steps that keep the equation true; balance model and its limits; define "term" | Working backwards in your head works here but leaves no record and does not scale; we need a written, checkable method |
| 5 | Solving $3x + 5 = 20$ step by step | Full worked example with goal/move/why/check; why subtract first (divide-first alternative); confront "divide only part of a side" and "the 3 crosses over as −3" | Now both ingredients (undo order + both-sides rule) exist, so combine them |
| 6 | When the recipe subtracts | Worked example $2x - 9 = 7$; non-whole answers are fine | Same method, one changed operation; shows the inverse pairing is general |
| 7 | From a story to an equation | Translation checklist; worked plumber example; return to the notebook story | The motivating problem was a story; learner must be able to produce the equation themselves |
| 8 | Practice | Independent, transfer and error-spotting exercises | All pieces are in place; test them without scaffolding |
| 9 | Optional peek: $x$ on both sides | Show where the recipe picture stops | Marked optional; not used by any exercise |
| 10 | Synthesis | Answer the central question using recipe + balance + check | Close the thread |

**Running example:** the notebook story / $3x + 5 = 20$. Introduced in §1; read and guessed at in §2 (guesses 4, 6, 5); solved by working backwards in §3; solved formally in §5; misconception demos in §5 use it; translation revisited in §7; final form in §10.

## Outcome alignment

| Outcome | Taught in | Worked example | Assessed by |
|---|---|---|---|
| 1 | §2 | Testing guesses for $3x + 5 = 20$ | E1, E7 |
| 2 | §3 | Recipe for $3x + 5 = 20$ and for $3(x + 5)$ | E2, E6 |
| 3 | §4, §5, §6 | $3x + 5 = 20$; $2x - 9 = 7$ | E3, E4, E7 |
| 4 | §7 | Plumber: $25h + 40 = 115$ | E5 |
| 5 | §3 (parentheses recipe), §4 (both-sides rule) | Recipe for $3(x + 5)$ (reading only; solving it is the transfer) | E6 |

## Misconceptions

| Misconception | Where it arises | How the lesson confronts it |
|---|---|---|
| $3x$ with $x = 5$ is "35" (juxtaposition read as digits) | §2, first time $3x$ appears | State it, show $3x$ means $3 \times 5 = 15$; E1(c) asks the learner to fix it |
| Do the operations in reading order: undo $\times 3$ first because it is "first" | §3 | Prediction prompt; reverse-order (socks/shoes) explanation; divide-first discussion in §5 |
| Dividing only part of a side: $3x + 5 = 20 \to x + 5 = 20 \div 3$ | §5 | Carry the error to $x = 1\tfrac{2}{3}$, substitute: gives 10, not 20 |
| "Move it across and change the sign" applied to the 3: $x = 20 - 5 - 3 = 12$ | §5 | Substitute 12: gives 41; explain the 3 multiplies, so its undo is divide; E7 is this error |
| Treating $5(x - 2)$ like $5x - 2$ (ignoring parentheses) | §3, E6 | Parentheses recipe in §3; E6 solution shows the wrong answer 7.4 and its failed check |

## Practice plan

| Id | Level (guided / independent / transfer / check) | Outcomes | Requires only |
|---|---|---|---|
| E1 | check | 1 | §2 |
| E2 | guided | 2 | §3 |
| E3 | guided | 3 | §3–§5 |
| E4 | independent | 3 | §3–§6 |
| E5 | independent | 4 | §7 (and §5–§6) |
| E6 | transfer | 2, 5 | §3 parentheses recipe, §4 both-sides rule |
| E7 | check | 1, 3 | §2, §5 misconception repair |

## Correctness risks

- Every substitution and every step in worked examples and solutions (guesses 17/23/20; $20 \div 3 = 6\tfrac23$ path giving 10; the "12" path giving 41; $x = 3.5$, $x = 2.5$; 7.4 wrong path giving 27).
- Divide-first alternative: $x + \tfrac53 = \tfrac{20}{3}$ gives $x = 5$.
- Optional peek: $3x + 5 = x + 9 \Rightarrow x = 2$.
- Order-of-operations statement ($3 \times 5 + 5 = 20$, not 30).
- Story arithmetic: notebooks 5; plumber 3 hours; cinema 5 tickets.
