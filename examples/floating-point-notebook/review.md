# Review: Why `0.1 + 0.2 != 0.3` (lesson.ipynb)

Reviewed against `references/quality-review.md`. Learner: comfortable with basic Python; knows nothing about how numbers are stored. Verification interpreter: CPython 3.14.0 (nbformat, nbclient, ipykernel in a venv). The notebook itself imports only `math`, `sys`, `decimal`, `fractions`.

## Structural check

Command, from this directory:

```
python skills/lesson-architect/scripts/check_lesson.py lesson.ipynb --execute --blueprint lesson.blueprint.md
```

Final result: **36 passed, 0 warnings, 0 failed.** This includes nbformat schema validation, "shipped without outputs", the predict → experiment → interpret pairing (7 cycles), every outcome assessed, guided before independent practice, hints/solutions separated, clean-kernel execution (19 code cells, no errors), and blueprint outcome count matching (5 = 5).

The first full build also passed with 0 warnings. The audits below found the real defects, which the checker cannot see.

## Continuity audit

| Check | Verdict | Evidence / fix |
|---|---|---|
| Every learning outcome is taught and assessed | Pass | O1: taught in the decimal warm-up and binary sections, WE1 (0.375, 0.1), assessed by E1. O2: "What a float keeps" + grid model, WE2 (0.1 + 0.2 to the last bit), assessed by E2 and E6. O3: ulp defined in the grid model, gap table in "The grid gets coarser", assessed by E3. O4: "Comparing floats safely", WE3 (tolerances for the loop total and a zero check), assessed by E4. O5: "When close enough is not enough", assessed by E5. Reverse check: no exercise assesses anything outside the five outcomes (E6 is a verbal version of O2). |
| Exercises require no untaught concepts | Pass | E1: denominator rule, `binary_digits`, `Fraction("…")` (all taught before). E2: `Fraction(x)`, `math.nextafter`, `math.ulp`, WE2's steps. E3: `math.ulp`, spacing $2^{e-52}$, ties-to-even (all in the grid model). E4: `abs_tol`/`rel_tol` and the documented formula. E5: `Decimal` from text, `Decimal(float)` behaviour, whole cents; `sum()` of Decimals is ordinary Python. Nothing needed lives only in the optional `<details>` section. |
| Terminology and notation are introduced before use | Pass after fix | Term trace (first use → explanation): binary/base 2 (route preview → "Binary: place value"), bit (same), subscript 2 (same), denominator rule (warm-up), significant digits (§ "What a float actually keeps"), IEEE 754 (named in misconception 1, described as the standard fixing every result; double precision in §5), grid, correct rounding, round half to even, ulp, `nextafter` (all in the grid model, before WE2), absolute/relative tolerance (comparison section), cancellation (defined where mentioned in the synthesis). **Defects found and fixed:** (1) misconception 1 said "down to the last *binary* digit" before binary was introduced → "down to the very last digit"; (2) the orientation and the surprise interpretation spoke of the "17th significant digit" before significant digits were taught (and it was inaccurate, see correctness) → "about one part in $10^{16}$". |
| Transitions preserve the learning thread | Pass | Each section states why it comes next: warm-up "The cause turns out to be a problem you already know…"; binary "To see why `0.1` causes trouble we need to write fractions the way the computer does"; float storage "A computer has finite memory, so it has to stop somewhere"; grid model "We now have two facts… Together they give one small model"; spacing "To compare floats safely we need to know how far apart neighbours are in general"; comparison "What remains is the practical question…"; exact types "Sometimes, though, close is not acceptable". Running example (`0.1 + 0.2`, and the ten-step loop total) threads from the surprise through WE2, WE3 and the synthesis. |
| Worked examples explain reasoning | Pass after fix | All three WEs have a goal, a "Choosing the method" / "Why this kind" paragraph naming the rejected alternative (guessing place values; float subtraction for measuring error; `round()` both sides), a goal per step, and a check. **Defect found and fixed:** WE2 Step 4 jumped from "both neighbours lie between $2^{-2}$ and $2^{-1}$" to "each is a 53-bit whole number × $2^{-54}$"; added the missing link (move the point 52 places, cost $2^{-52}$, last bit is $b_{52}$). |
| Followable without filling missing conceptual steps | Pass | Re-read as the learner, top to bottom. Each prediction is answerable from what came before (e.g. the 0.5/0.625/0.3/0.7 prediction uses only the denominator rule; the gap-table prediction uses the 4-significant-digit calculator). The tie in WE2 is prepared by rule 4 of the grid model and by the decimal example (0.125 → 0.12). Analogies state their limits: the 4-digit calculator ("Where this warm-up stops matching": base, and digits after the point vs significant digits), the ruler ("ticks are not evenly spaced… the ruler also ends"). All seven planned misconceptions are confronted where they arise (random/buggy after the surprise; `print` shows the truth after `Decimal(0.1)`; 16 decimal places after the gap table; fixed `1e-9` and `isclose` to zero after the comparison experiment; `Decimal` is always exact after the Decimal experiment; `round()` in WE3). Synthesis answers the central question from the pieces and closes the loop-total thread. Headings are content-specific; no teacher-facing text; the optional section is marked and not used later. |

## Correctness audit

| Check | Verdict | Evidence / fix |
|---|---|---|
| Claims, calculations, and code checked | Pass after fix | **Code:** the notebook ran top to bottom in a clean kernel (checker `--execute`) and again via `exec` in one namespace; all five ```python solution blocks (E1–E5) were executed after the notebook cells, and every `# expected output` comment in them was compared with the real printed output. **Numeric claims:** a verification script asserted 98 claims taken from the markdown cells and solutions, 0 failures on Python 3.14.0. They include: `Fraction(0.1) = 3602879701896397/36028797018963968` (= $2^{55}$); `Decimal(0.1)` digit string, 55 digits after the point; excess $1/180143985094819840 \approx 5.55\times10^{-18}$; `Decimal(0.2)`/`Decimal(0.3)` above/below; 0.1 rounds up (bit 54 of the significand is 1 with later 1s); the exact sum of stored 0.1 and 0.2 is **exactly half a step** from each neighbour (tie), lower significand 5404319552844595 odd, upper …596 even; `0.1 + 0.2 - 0.3 == 2**-54`; `math.ulp(0.3) == 2**-54`; gap-table values (5.55e-17, 2.22e-16, 1.14e-13, 1.16e-10, 16) and relative gaps in (1.1e-16, 2.22e-16]; $2^{-53}\approx1.1\times10^{-16}$, $2^{53}\approx9\times10^{15}$; exponent range −1022…1023 and 53 significand bits (`sys.float_info`, `math.frexp`); max ≈ 1.8e308, smallest normal ≈ 2.2e-308; `int(float(123456789012345678)) == 123456789012345680`; `1e17 + 16` is the next float; the seven comparison results (T, F, T, T, T, F, F); `repr(nextafter(0.125, 1)) == '0.12500000000000003'` and `round` gives 0.12 vs 0.13; `Decimal("0.125")` half-even → 0.12; only 0.5 among 0.1…0.9 terminates in binary; hex strings for 0.1, 0.3, 0.1+0.2; `fsum([0.1, 0.2]) != 0.3`; `sum([0.1]*10) == 1.0` on ≥3.12; Decimal results (28-digit 1/3; `Decimal(0.1)+Decimal(0.2) != Decimal("0.3")`); E2 numbers (0.1 off by ≈5.6e-18, 0.7 by ≈4.4e-17, distances 1/4 and 3/4 of a step, 1.1 + 2.2 exact addition, 3.3000000000000003); E3 (ulp(1e17) = 16, `1e17+9` → `1.0000000000000002e+17`, smallest k = 53, spacing 1 at $2^{52}$ and 2 at $2^{53}$); E4 (default isclose fails 0 vs 0.0004; ulp(10000) ≈ 1.8e-12; `rel_tol=0.0005` accepts 5 m at 10 km); E5 (float loop 25.389999999999997, `Decimal(19.99)` digits, `Decimal(float)` total 25.38999999999999857003274428, cents total 2539). **Defect found and fixed:** "the errors sit in the 17th significant digit" was wrong for `0.9999999999999999` (it differs from 1 from the first digit onward; the relative error is ≈1.1e-16). Replaced in two cells by "about one part in $10^{16}$", which the script checks for both results. **Domain facts** checked against the Python tutorial ch. 15 and the `math` docs (both listed in the blueprint and actually read): `isclose` formula, defaults and zero caveat; `ulp`/`nextafter` added in 3.9; shortest repr; `sum()` extended precision since 3.12. IEEE 754 correct rounding and round-half-to-even default are from my own knowledge (standard, not looked up this session). **Sources:** the one URL in the notebook (tutorial ch. 15) was fetched; no invented URLs. |

## Revisions made

- E4 statement: "differ by **less than** half a millimetre" → "by **at most** half a millimetre", because `math.isclose` tests `<=`; the solution now matches the specification exactly.
- "17th significant digit" claim in the interpretation of the opening surprise and the matching sentence after the gap table: replaced with the verified "about one part in $10^{16}$" (correctness, and it used "significant digit" before the term was taught).
- Misconception 1: "last binary digit" → "very last digit" (term used before binary is introduced).
- WE2 Step 4: added the step showing why each neighbour of 0.3 is a 53-bit whole number × $2^{-54}$, so the even/odd test is justified rather than asserted.
- Verification found two failures in my own checking script (wrong expected count of solution blocks; a loop's three-line output compared as one line), not in the lesson; fixed the script, all 98 claims then passed.
- After every revision: rebuilt the notebook with nbformat, re-ran the claim verification (0 failures) and the structural checker with `--execute --blueprint` (36 passed, 0 warnings, 0 failed).

## Not verified / limitations

- Run only on CPython 3.14.0 on Linux. Behaviour that is version-dependent is flagged in the lesson (`sum()` ≥ 3.12; `math.ulp`/`nextafter` ≥ 3.9, guarded by an `assert`) but was not executed on 3.9–3.13.
- Markdown/LaTeX rendering (tables, `$…$`, `<details>`) was not visually inspected in Jupyter or VS Code; only delimiter balance (checker) and the source text were checked.
- The continuity audit was done by the author re-reading as the learner, not by a real novice; time-on-task is untested.
- The IEEE 754 statements (correct rounding of `+ - * /`, ties-to-even default, 1/11/52 bit layout) are standard facts checked indirectly by the code results, not against the standard's text.
- The verification script and build scripts were kept in the authoring session folder, not shipped with the example (the task restricted outputs to these three files).

## Independent spot-check (second reviewer)

- Re-executed the notebook in a clean kernel via the eval suite (`--execute`): it runs with no errors.
- Recomputed key claims independently: `0.1 + 0.2 == 0.30000000000000004`; `Fraction(0.1) == 3602879701896397/2**55`; `math.ulp(2.0**52) == 1.0` and `math.ulp(2.0**53) == 2.0`; `float(2**53) + 1 == float(2**53)`.
- No changes were needed.
