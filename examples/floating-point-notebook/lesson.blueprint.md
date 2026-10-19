# Blueprint: Why `0.1 + 0.2 != 0.3` — how Python stores decimal numbers, and how to compare them safely

Working document for the author. Not shown to the learner.

## Brief

- **Learner:** comfortable writing basic Python (variables, loops, functions, `print`, f-strings); knows school fractions; knows nothing about how numbers are stored (no binary, no bits, no scientific notation in base 2).
- **Destination:** the learner can explain, down to the stored values, why `0.1 + 0.2 != 0.3`, and writes float comparisons with `math.isclose` (or switches to exact types) appropriately.
- **Scope:** *in* — binary fractions, which fractions terminate in a base, 53 significant bits, round-to-nearest (incl. ties-to-even), the "grid" model, ulp and relative spacing, `==` vs `math.isclose` (rel/abs tolerance), integers / `Fraction` / `Decimal` as exact alternatives. *Out* — bit-level layout (optional only), inf/NaN/overflow, subnormals, error analysis of long computations, catastrophic cancellation, compensated summation (mentioned as next steps only).
- **Format:** Jupyter notebook — the user asked for one, and running code is genuinely how the learner learns here: `Fraction(0.1)`, `math.ulp`, `math.nextafter` let the learner *see* stored values instead of trusting prose.
- **Assumptions made without asking:**
  - Python 3.9+ (needed for `math.ulp`, `math.nextafter`); verified on 3.14.
  - Learner knows fractions in lowest terms and prime factors at school level.
  - "Compare them safely" means: use `math.isclose` with justified tolerances, and know when to avoid floats entirely.
  - Standard library only (`math`, `fractions`, `decimal`, `sys`).
- **Sources read:**
  - Python tutorial, ch. 15 "Floating-Point Arithmetic: Issues and Limitations", https://docs.python.org/3/tutorial/floatingpoint.html (53 bits, `3602879701896397/2**55`, shortest repr since 3.1, `sum()` extended precision, `fsum`, `decimal`/`fractions` advice).
  - Python `math` module docs, https://docs.python.org/3/library/math.html (`isclose` formula and zero caveat, `ulp`, `nextafter`, both added in 3.9).
  - Built-in docstrings of `math.isclose`, `math.ulp`, `math.nextafter` in the verification interpreter.

## Central question

Why does Python say `0.1 + 0.2 == 0.3` is `False`, and how should I compare decimal-looking numbers in my code instead?

**Motivating problem:** `0.1 + 0.2 == 0.3` → `False`; and the everyday version: adding a 0.1 item ten times in a loop gives `0.9999999999999999`, so `total == 1.0` silently fails.

## Learning outcomes

By the end, the learner can:

1. Decide whether a decimal number such as `0.375` or `0.1` can be stored exactly in a Python `float`, and justify the answer by writing it as a binary fraction.
2. Reveal the exact value a `float` stores, and use it to explain step by step why a calculation such as `0.1 + 0.2` does not equal `0.3`.
3. Explain why the gap between neighbouring floats grows with the size of the number, and measure that gap with `math.ulp`.
4. Compare floats safely with `math.isclose`, choosing a relative and an absolute tolerance that fit the problem (including comparisons with zero).
5. Decide when to avoid floats entirely and use integers, `fractions.Fraction`, or `decimal.Decimal` instead.

## Prerequisites

| Concept | Assumed or taught here? | Needed for |
|---|---|---|
| Basic Python: loops, functions, strings, `print`, f-strings | assumed | all code |
| Fractions in lowest terms, prime factors | assumed | denominator rule (§3–4) |
| `==` compares values exactly | assumed (made explicit in §8) | the surprise, §8 |
| `Fraction` as an exact "magnifying glass"; passing a string vs a float | taught in §1 (setup), reinforced §4–5 | §4–9 |
| Fixed-digit storage forces rounding (decimal warm-up, 1/3) | taught in §3 | §4–5 |
| Binary place value; bit; repeated-doubling conversion | taught in §4 | §5, E1 |
| Denominator rule: terminates in base b iff denominator's prime factors divide b | taught in §3 (base 10), §4 (base 2) | E1, §5 |
| Significant digits / scientific notation; 53 significant bits | taught in §5 | §6–7 |
| Round to nearest; stored value revealed by `Fraction(x)` / `Decimal(x)`; shortest repr | taught in §5 | §6, E2 |
| Grid model; correctly rounded operations; ties-to-even; `math.nextafter`; ulp | taught in §6 | WE2, E2, E3 |
| Grid spacing proportional to magnitude; `math.ulp`; ~1.1e-16 relative error per rounding | taught in §7 | E3, §8 |
| Absolute vs relative tolerance; `math.isclose`; abs_tol near zero | taught in §8 | WE3, E4 |
| Integers-as-cents, `Fraction`, `Decimal(str)` vs `Decimal(float)`, Decimal's finite precision | taught in §9 | E5 |

Dependency order of taught concepts: fixed-digit rounding → binary place value → denominator rule → significant bits → round-to-nearest & stored value → grid model (+ ties, nextafter, ulp) → spacing grows with size → tolerances / isclose → exact alternatives.

## Sequence

| # | Section (working title) | Purpose | Why it comes next |
|---|---|---|---|
| 1 | Orientation + setup | Show the question, outcomes, route; import tools; introduce `Fraction` as exact | — |
| 2 | The surprise | Reproduce `0.1+0.2` and the loop total; repair "floats are random/buggy" | Learner must see the problem's exact shape before explaining it |
| 3 | Decimal warm-up | Fixed digits force rounding (1/3); denominator rule in base 10; analogy boundary | Builds the mechanism in a familiar base before switching base |
| 4 | Binary place value (WE1 + E1) | Read/write binary fractions, repeated doubling, 1/10 repeats | Need base 2 to see why 0.1 does not fit |
| 5 | What a float keeps | 53 significant bits, round to nearest, reveal stored values; repair "print shows exact value" | Infinite digits + finite storage ⇒ need to know where the cut is |
| 6 | Grid model and WE2 (0.1+0.2 fully) + E2 | Correctly rounded ops, ties-to-even, nextafter; solve running example | Have inputs' stored values; now need what `+` does |
| 7 | Grid spacing grows (E3) | `math.ulp`, relative spacing, ~16 sig. digits; repair "16 decimal places" | Safe comparison needs to know how far apart neighbours are |
| 8 | Comparing safely (WE3 + E4) | abs vs rel tolerance, `math.isclose`, abs_tol near zero; repair fixed `1e-9`, isclose-to-zero | Now the practical answer to "what to write instead of ==" |
| 9 | Exact alternatives (E5) | ints/cents, Fraction, Decimal(str); repair Decimal(0.1) and "Decimal is always exact" | Tolerances don't fit when exactness is required (money) |
| 10 | Optional: 64-bit layout, `sum()`/`fsum` | Depth for the curious | Optional, not required later |
| 11 | Check (E6) + Synthesis | Answer the central question from the pieces; revisit loop total; next steps | Closes the thread |
| 12 | Hints and solutions | Graded hints, full solutions with likely wrong answers | Kept apart from statements |

**Running example:** `0.1 + 0.2 == 0.3` (plus the loop total of ten 0.1s). Introduced §2; 0.1's binary expansion §4; stored values §5; fully solved in WE2 (§6); revisited in §8 (`isclose`) and §9 (Decimal/Fraction); final answer in synthesis, including the loop total ending one grid step below 1.0.

## Outcome alignment

| Outcome | Taught in | Worked example | Assessed by |
|---|---|---|---|
| 1 | §3, §4 | WE1: 0.375 and 0.1 in binary | E1 |
| 2 | §5, §6 | WE2: 0.1 + 0.2 to the last bit | E2, E6 |
| 3 | §6 (ulp defined), §7 | §7 experiment (gap table) | E3 |
| 4 | §8 | WE3: tolerances for the loop total and a zero check | E4 |
| 5 | §9 | §9 experiment (Decimal / Fraction / cents) | E5 |

## Misconceptions

| Misconception | Where it arises | How the lesson confronts it |
|---|---|---|
| Float arithmetic is random/buggy/sloppy | §2, right after the surprise | Re-run gives identical digits; IEEE 754 correctly rounded; cause is storage |
| `print(0.1)` shows `0.1`, so it's stored exactly | §5 | `Fraction(0.1)`, `Decimal(0.1)`; shortest-repr explanation; `0.30000000000000004` as evidence |
| Floats are accurate to ~16 decimal *places* (fixed absolute precision) | §7 | `float(123456789012345678)` → `...680`; ulp(1e17) = 16 |
| `abs(a - b) < 1e-9` works everywhere | §8 | Fails for 1e17 neighbours (too strict) and for 1e-12 vs 2e-12 (too loose) |
| `math.isclose` with defaults works for comparing with zero | §8 | `isclose(0.1+0.2-0.3, 0.0)` → False; docs formula explains; fix with abs_tol |
| `Decimal` makes everything exact / `Decimal(0.1)` is one tenth | §9 | `Decimal(0.1)` shows float's value; `Decimal(1)/3*3 != 1` |
| (minor) `round()` both sides fixes comparison | WE3 method selection | neighbouring floats 0.125 and 0.12500000000000003 round to 0.12 vs 0.13 |

## Practice plan

| Id | Level (guided / independent / transfer / check) | Outcomes | Requires only |
|---|---|---|---|
| E1 | guided | 1 | §3–4 (denominator rule, `binary_digits`, `Fraction(str)`) |
| E2 | guided | 2 | §5–6 (Fraction(x), grid model, nextafter, WE2 steps) |
| E3 | independent | 3 | §6 (ties-to-even), §7 (`math.ulp`, spacing) |
| E4 | independent | 4 | §8 (`math.isclose`, abs vs rel tolerance) |
| E5 | transfer | 5 | §9 (Decimal from strings, integer cents), §5 (Decimal(float) shows stored value) |
| E6 | check | 2 | §3–6 (explain in words) |

## Correctness risks

- Exact stored values: `Fraction(0.1) = 3602879701896397/2**55`; `Decimal(0.1)`, `Decimal(0.2)`, `Decimal(0.3)` digit strings.
- 0.1 + 0.2: exact sum of stored inputs is **exactly halfway** between stored 0.3 and the next float → tie → ties-to-even picks the upper (significand ...596 even vs ...595 odd). Must not claim "simply nearer".
- Grid spacing formula 2^(e−52) for x in [2^e, 2^(e+1)); ulp(0.3) = 2^-54, ulp(1.0) = 2^-52, ulp(1e17) = 16.
- `1e17 + 1 == 1e17` True; `1e17 + 9` → `1e17 + 16`; smallest k with `float(2**k) + 1.0 == float(2**k)` is 53 (tie case).
- `sum([0.1]*10) == 1.0` is **True** on Python ≥ 3.12 (extended-precision sum) → use an explicit `+=` loop for the running example.
- `math.isclose` formula and default tolerances; `isclose(x, 0.0)` false for nonzero x.
- `0.1 + 0.7`: inputs' errors, exact sum 0.75 ulp below stored 0.8; `1.1 + 2.2`: addition exact, error entirely from inputs.
- Till example must actually fail with floats: `19.99 + 4.70 + 0.70` → `25.389999999999997`.
- `round(0.125, 2)` vs `round(nextafter(0.125, 1), 2)` → 0.12 vs 0.13.
- `float(123456789012345678)` → `123456789012345680` (not a tie: remainder 14 mod 16).
- Every numeric claim in markdown cells is to be checked by executing code (see review.md).
