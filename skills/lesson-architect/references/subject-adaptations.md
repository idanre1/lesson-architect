# Subject Adaptations

Read the section that matches the lesson. Each adapts the general workflow; none replaces it.

## Research papers

**Goal:** the learner can explain what problem the paper addresses, how its central mechanism works, what evidence supports its claims, and where those claims stop.

1. **Read the actual paper first.** Fetch it (arXiv, publisher, or a file the user provides). Record the exact title, authors, venue/year, and version or URL in the blueprint. If you can only access the abstract, say so and restrict the lesson to what you have read.
2. **Problem before mechanism.** Teach the motivating problem and the prerequisite ideas (with the learner's assumed background) before any equation from the paper. A learner should understand *why anyone would want* the mechanism before seeing it.
3. **Mechanism before results.** Introduce the paper's notation in the paper's own symbols, define each one, and connect each equation to the motivating problem.
4. **Separate four kinds of statement**, and make the separation visible in the lesson (labels, call-outs, or explicit phrasing):
   - *The paper claims / reports* — with a section, table, figure, or equation reference.
   - *Explanatory example* — your toy example or simplification, not from the paper.
   - *Interpretation* — your reading of why it works or what it implies.
   - *Limitations and open questions* — those stated by the authors and those you identify, labelled separately.
5. **Do not upgrade conjectures to facts.** If the authors say "we conjecture" or "we hypothesize", keep that hedge.
6. **Numbers must be traceable.** Every reported number in the lesson cites the table/section it came from. Re-check each against the paper during the correctness audit.
7. **Quote exactly or paraphrase.** Text in quotation marks must match the paper verbatim; verify with a script against the extracted text (PDF extraction splits text across page footers and tables, so check failures by hand). If a figure or table cannot be read (e.g. plots lost in extraction), describe only what the caption and body text state, and say so.
8. **Scope the lesson.** Teach the central mechanism and the evidence for it; summarize secondary experiments in an optional section rather than covering every table.
9. **Sources section:** the paper itself, plus any other source you actually used. Never list a source you did not read.

Typical progression: motivating problem → prerequisite ideas → the paper's key insight in plain words → the mechanism, formally → a hand-sized example → the evidence → limitations → synthesis → practice that asks the learner to reason with the idea (predict an outcome, critique a claim, apply the mechanism to a variant).

## Mathematics

**Goal:** the learner can recognize when a method applies, carry it out with reasons, check the answer, and adapt to a changed problem.

For each method taught, cover:

1. **Problem meaning** — what is being asked, in words and in a concrete instance; what a solution would look like.
2. **Method selection** — which features of the problem point to this method; what tempting alternative fails and why.
3. **Derivation** — why the method works (from things already taught), with intermediate steps.
4. **Worked solution** — every step with its goal and justification; finish by checking the answer (substitute back, estimate, units, special cases).
5. **Transfer** — a changed problem where one governing condition differs; discuss whether and how the method adapts.

Rules:

- Define every symbol before use. Use consistent notation throughout.
- Write mathematics in standard Markdown math (`$...$` inline, `$$...$$` display), and keep it readable without rendering (avoid deeply nested macros).
- Recompute every calculation during the correctness audit, preferably with code (e.g. Python's `fractions` for exact arithmetic).
- For beginners, prefer exact small numbers and a model the learner can picture (balance, number line, area) — and state the model's limits.

## Piano and other physical skills

**Goal:** the learner can perform a defined musical task to an observable standard and knows how to practice toward it.

Progression:

1. **Musical goal** — what the learner will be able to play and what it should sound like (tempo, evenness, dynamics, connection between notes).
2. **Component skills** — the smallest separable skills the goal needs (posture and hand shape, note location, finger numbers, pulse, a specific motion). Teach each with what to do, what it should feel and sound like, and the most common fault.
3. **Focused practice** — one component at a time, slow, with a concrete method (counting aloud, a metronome setting, hands separately, short loops, a set number of clean repetitions).
4. **Integration** — combine components gradually (two notes → a group → a phrase; hands separately → hands together) and say what to do when combining breaks something.
5. **Self-checks** — observable criteria the learner can judge alone: e.g. "plays the phrase three times in a row at ♩ = 60 with no stops", "a phone recording shows even note lengths", "wrist stays level when viewed in a mirror".

Rules:

- Use standard conventions only: letter names, the standard piano finger numbers (thumb = 1 … little finger = 5), standard rhythm values and tempo markings. Do not invent notation. If a staff image would be needed and you cannot produce correct standard notation, present the music as a plain table — one row per bar, columns for letter names, finger numbers, and beats per note — and say that it is a table, not notation.
- Verify melodies against a source (a public-domain score or several independent arrangements), say which version you use when versions differ, and give the public-domain reasoning (composer/publication dates) in the sources section.
- State instrument assumptions briefly: where middle C is, that an 88-key piano or a 61-key keyboard both work, and to switch off transpose/octave shift on digital keyboards.
- Do not reproduce copyrighted scores or lyrics. Use exercises you compose (scales, five-finger patterns, simple original phrases) or melodies clearly in the public domain, and say which.
- Include rest and safety guidance: stop if anything hurts; tension is a fault to fix, not effort to push through.
- Practice instructions must be concrete enough to follow at the instrument without interpretation.
- Markdown is the right format; a notebook adds nothing here.

## General technical topics

**Goal:** the learner holds a working mental model and can predict system behaviour from it, then use the implementation details correctly.

1. **Mental model first.** Before APIs, flags, or code, give a model of the moving parts: what state exists, what operations change it, what is guaranteed and what is not. Keep it small enough to hold in mind.
2. **Predict from the model.** Ask the learner to use the model to predict a behaviour, then show the real behaviour.
3. **Each detail hangs on the model.** When introducing an implementation detail, say which part of the model it realises or which limitation of the model it addresses. Details that do not connect to the model are probably optional.
4. **Show failure modes.** The model's value is clearest where naive expectations fail; demonstrate one and explain it through the model.
5. **Verify code.** Every code snippet must run as shown (or be clearly marked as pseudocode). Pin versions or state assumptions when behaviour differs across versions.

### When to use a notebook

Use a Jupyter notebook when running, changing, and observing code is how the learner will learn. Each experiment cycle in the notebook should be:

1. **Explanation** (markdown) — the idea being tested.
2. **Prediction** (markdown) — the learner writes down what they expect, before running.
3. **Experiment** (code) — short, focused, runnable top-to-bottom.
4. **Interpretation** (markdown) — what happened, and how the mental model explains it (including when it contradicts the prediction).
5. **Practice** (markdown + code stub) — a modified experiment the learner writes.

Rules:

- Use code only when it contributes to learning; explanation stays in markdown cells.
- Prefer the standard library; if a package is needed, install it in a clearly marked setup cell and say why it is needed.
- Ship the notebook **without outputs** so predictions are genuine; execute a copy in a clean kernel to verify, and report any cell that was not executed and why.
- Practice cells contain stubs (`...` or `# your code here`) that do not crash the notebook when run unchanged; keep worked solutions in a separate markdown section at the end (or in collapsed `<details>` blocks).
