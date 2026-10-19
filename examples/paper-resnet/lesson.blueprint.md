# Blueprint: Reading the ResNet paper — why stacking layers failed, and how residual learning fixed it

Working document for the author. Not shown to the learner.

## Brief

- **Learner:** knows what a neural-network layer, a training loss, and gradient descent are. Has never read a research paper. Does not know convolutional networks in detail.
- **Destination:** the learner can explain the problem the ResNet paper attacks (degradation), how a residual block works (Eqn. 1 and 2), what evidence the paper offers and which comparisons are fair, and where the paper's claims stop — and can then read the paper itself with a map.
- **Scope:**
  - *In:* §1 motivation; the degradation problem (Fig. 1, Fig. 4, Table 2); the construction argument; §3.1–3.2 (Eqn. 1, 2); just enough CNN vocabulary to read §3.3, Table 1, Fig. 3, Fig. 5; shortcut options A/B/C (Table 3); bottleneck block (Fig. 5 right); CIFAR-10 experiments (Fig. 6, Fig. 7, Table 6); headline ImageNet results (Tables 3–5); authors' hedges and open problems; how to read a paper.
  - *Out:* detection/localization pipelines in the appendices (Faster R-CNN, RPN, box refinement) beyond one sentence; training-recipe details (§3.4) beyond what is needed for fairness arguments; later follow-up papers (not read, not cited); implementing ResNet in code.
- **Format:** Markdown. This is a paper reading; the learner's work is reasoning about claims, small hand calculations, and tables, which prose serves better than a notebook (SKILL.md: "Never force a notebook onto … most paper readings").
- **Assumptions made without asking:**
  - "Know what a layer is" = can read $W x$ (matrix times vector) and knows a nonlinearity is applied after it. ReLU is re-defined anyway.
  - The learner is comfortable with percentages and multiplying small numbers; no calculus beyond "gradient descent follows the slope of the loss" is needed. Backpropagation is described in words only.
  - The learner wants understanding of the ideas and the evidence, not the ability to reproduce the training runs.
  - Basic machine-learning vocabulary not in the stated background (training vs. test error, overfitting, validation set, top-1/top-5 error, vanishing gradients) is taught briefly, since the paper's argument depends on it.
- **Sources read:** K. He, X. Zhang, S. Ren, J. Sun, "Deep Residual Learning for Image Recognition", arXiv:1512.03385v1 [cs.CV], 10 Dec 2015, https://arxiv.org/abs/1512.03385 — full text read from the provided PDF/plain-text extraction (all 12 pages, including appendices A–C). No other source consulted. References cited *inside* the paper (e.g. [16] batch normalization, [21] 10-crop testing, [41] VGG) were not read and are only mentioned as "the paper cites…".

## Central question

Why did simply making a network deeper make it *worse* — even on the data it was trained on — and how does re-writing each few layers as "input plus a learned correction" let 100+-layer networks train and gain accuracy?

**Motivating problem:** the paper's own pair (Table 2, Fig. 4): a 34-layer plain network has higher error than an 18-layer one, although (§4.1) "the solution space of the 18-layer plain network is a subspace of that of the 34-layer one". Adding identity-shortcut connections — with zero extra parameters — reverses that ordering. This 18-vs-34 pair is the running example.

## Learning outcomes

By the end, the learner can:

1. Explain the degradation problem and tell it apart from overfitting and from vanishing gradients, using training- versus test-error evidence.
2. Compute the output of a residual building block (Eqn. 1) on small numbers, and explain why driving its weights to zero gives an identity mapping while a plain block gives zero.
3. Decide whether a shortcut can be an identity or needs a projection (Eqn. 2), and count the extra parameters each shortcut option costs.
4. Judge which comparison in the paper's tables supports a given claim, and whether that comparison is controlled (same depth, parameters, and computation).
5. Sort statements about ResNet into reported results, the authors' arguments/hypotheses/conjectures, and claims the paper does not make.

## Prerequisites

| Concept | Assumed or taught here? | Needed for |
|---|---|---|
| Layer as $W x$ followed by a nonlinearity | assumed | Eqn. 1, toy block |
| Training loss, gradient descent | assumed | degradation, optimization difficulty |
| How a paper is organized; citation brackets; hedge words | taught in Part 1 ("How to read this paper") | locating claims; outcome 5 |
| Image classification, ImageNet, CIFAR-10, top-1/top-5 error | taught in Part 2 ("The puzzle") | reading tables |
| Training vs. test (validation) error; overfitting | taught in Part 2 ("The puzzle") | outcome 1 |
| Vanishing/exploding gradients (in words + toy product) | taught in Part 2 ("The puzzle") | outcome 1, misconception M3 |
| Batch normalization (one-sentence role only) | taught in Part 2 ("The puzzle") | paper's argument against vanishing gradients |
| Identity mapping; the construction argument | taught in Part 3 ("Deeper should never be worse") | the key insight |
| ReLU $\sigma$ | taught (re-defined) in Part 4 ("The residual block") | Eqn. 1 toy example |
| Residual function $F(x) := H(x) - x$; Eqn. 1 | taught in Part 4 ("The residual block") | outcome 2 |
| Convolution layer, channels, feature map, stride, 1×1 conv, pooling, FLOPs, parameter count $k\cdot k\cdot C_{in}\cdot C_{out}$ | taught in Part 5 ("Just enough about convolutional networks") | outcome 3, Table 1, Fig. 5 |
| Projection shortcut $W_s$ (Eqn. 2); options A/B/C; bottleneck block | taught in Part 6 ("When the shapes don't match") | outcome 3 |
| Controlled comparison; ensemble; single run vs. mean±std | taught in Part 7 ("The evidence") | outcome 4 |

Dependency order of taught concepts: paper map & hedge words → error types (train/test, overfitting, top-k) → vanishing gradients & BN → degradation → identity mapping & construction argument → ReLU & residual reformulation (Eqn. 1) → CNN vocabulary & parameter counting → projection shortcuts (Eqn. 2), options A/B/C, bottleneck → evidence & fair comparison → limitations.

## Sequence

| Lesson part | Section (working title) | Purpose | Why it comes next |
|---|---|---|---|
| Orientation | Orientation | What/why/who; outcomes; route; label legend (paper vs. ours) | — |
| Part 1 | How to read this paper | Map of the paper's sections; citation brackets; the hedge-word ladder | The learner has never read a paper, and every later section cites §/Table/Fig. |
| Part 2 | The puzzle: deeper got worse | Vocabulary for errors; degradation (Fig. 1, Table 2); not overfitting; not (per authors) vanishing gradients; worked diagnosis; E1 | Problem before mechanism: a learner must feel the puzzle before any equation. |
| Part 3 | Deeper should never be worse | Identity mapping; construction argument; "it's the optimizer, not the capacity" | Turns the puzzle into a precise claim the mechanism can target. |
| Part 4 | The residual block | $H$, $F$, Eqn. 1, Fig. 2; toy 2-D block worked example; zero weights → identity; analogy with boundary; E2 | Now we know what's hard (finding identity-like solutions), so we can show a re-parameterization that makes it the default. |
| Part 5 | Just enough about convolutional networks | Conv vocabulary and parameter counting; Table 1 layer counts (18, 34); worked example on which ResNet-34 shortcuts can be identities (conv2_x vs. conv3_1) | Real ResNet blocks are convolutional; Eqn. 1 needs matching shapes, which only make sense once channels/stride are known. |
| Part 6 | When the shapes don't match | Eqn. 2; options A/B/C; bottleneck (Fig. 5); 50/101/152-layer counts; CIFAR 6n+2 | Applies the CNN vocabulary to the one place Eqn. 1 breaks. |
| Part 7 | The evidence | Table 2/Fig. 4 controlled comparison; Table 3 A/B/C; deeper ResNets (Tables 3–5); CIFAR-10 (Fig. 6, Table 6); Fig. 7 responses; how to read a table caption | Mechanism before results: now every row of the tables means something. |
| Part 8 | Where the claims stop | Authors' stated limits vs. our own, labelled separately; optional gradient-path interpretation | Evidence has been seen; now we bound it. |
| Practice | Practice | E3–E7 | All pieces are in place; practice fades support. |
| Synthesis | Synthesis | Answer the central question; revisit 18 vs. 34; next step (reading route through the real paper) | Closes the thread. |
| — | Hints & solutions; Sources | Separated from statements | — |

**Running example:** the 18-layer vs. 34-layer ImageNet pair. Introduced in Part 2 (Table 2 plain: 27.94 vs 28.54), reframed in Part 3 (34 = 18 + extra layers; subspace remark), given shortcuts in Parts 4–6 (16 blocks, 3 shape-changing shortcuts, option A has no extra parameters), resolved with evidence in Part 7 (ResNet: 27.88 vs 25.03), revisited in synthesis. A second, hand-sized toy (a 2-D vector through a two-layer block) carries the mechanism in Part 4.

## Outcome alignment

| Outcome | Taught in | Worked example | Assessed by |
|---|---|---|---|
| 1 | Part 2, Part 3 | "Diagnosing Fig. 1" (Part 2) | E1 (guided), E5 (transfer) |
| 2 | Part 4 | 2-D residual block vs. plain block (Part 4) | E2 (guided) |
| 3 | Part 5, Part 6 | Shortcut at conv3_1 of ResNet-34 (Part 5) | E3 (independent), E4 (transfer) |
| 4 | Part 7 | Table 2 as a controlled comparison (Part 7 prose walk-through) | E6 (independent) |
| 5 | Part 1, Part 7, Part 8 | Hedge ladder applied to §1/§3.1 sentences (Part 1) | E7 (check) |

## Misconceptions

| Misconception | Where it arises | How the lesson confronts it |
|---|---|---|
| M1: "The deeper net is worse because it overfits." | Part 2 | Training error is *also* higher (Fig. 1 left, Fig. 4 left); overfitting predicts low training / high test error. E1, E5. |
| M2: "The deeper plain net simply cannot represent a good enough function." | Part 3 | Construction argument (§1) and subspace remark (§4.1): it *can* represent the shallower solution; the solver doesn't find it. Toy: plain block with $W_1=W_2=I$ is an identity on non-negative inputs. |
| M3: "ResNets work because shortcuts fix vanishing gradients." | Part 2 and Part 8 | Paper §4.1 argues degradation is "unlikely to be caused by vanishing gradients" (BN; healthy gradient norms). Optional box presents the gradient-path view as *our interpretation*, not the paper's claim. E7. |
| M4: "Shortcuts help because they add parameters." | Part 7 | Option A adds zero parameters (Table 2 caption; §3.2); A/B/C differences are small (Table 3). |
| M5: "A model has one error number; two tables disagreeing means a mistake." | Part 7 | ResNet-34 B is 24.52 top-1 in Table 3 (10-crop) but 21.84 in Table 4 (caption says "single-model results" without naming the protocol; our reading is the §3.4 multi-scale "best results" protocol — hedged as such in the lesson). Read the caption and protocol. |

## Practice plan

| Id | Level | Outcomes | Requires only |
|---|---|---|---|
| E1 | guided | 1 | Part 2 (train/test error, overfitting, degradation) |
| E2 | guided | 2 | Part 4 (ReLU, Eqn. 1, toy worked example) |
| E3 | independent | 3 | Part 5 (param count, stride, 1×1 conv), Part 6 (Eqn. 2, options A/B/C) |
| E4 | transfer | 3 | Part 5 (param count), Part 6 (bottleneck, projection) |
| E5 | transfer | 1 | Part 2 (overfitting vs degradation), Part 7 (Table 6 numbers given in the statement) |
| E6 | independent | 4 | Part 7 (controlled comparison, Tables 2–3) |
| E7 | check | 5 | Part 1 (hedge ladder), Part 2, Part 7, Part 8 |

## Correctness risks

- Every number quoted from Tables 1–6, §3.3, §4.1, §4.2, §4.3 and the abstract — re-check against the text.
- Derived numbers: 28.54−25.03 = 3.51 (paper: "3.5%"); 27.88−25.03 = 2.85 (paper: "2.8%"); 3.6/19.6 ≈ 18%; 152/19 = 8; 6.0/21.2 ≈ 28%; layer counts from Table 1 block counts; 6n+2 for n ∈ {3,5,7,9,18,200}; 16 − 3 = 13 projections.
- Toy calculations: 2-D residual block (worked example and E2); conv parameter counts (73,728; 8,192; 147,456; 69,632; 65,536; 135,168, ratio ≈ 1.94); toy gradient products 0.8^30 and 1.2^30. Verify all with Python.
- Hedges to preserve: "We hypothesize" (§1), "suggests … might" (§3.1), "may help to precondition" (§3.1), "We argue … unlikely" and "We conjecture" (§4.1), "support our basic motivation … might be generally closer to zero" (§4.2), "We argue that this is because of overfitting" (§4.2), "we expect" (§1), footnote 2 "still an open question".
- Domain facts not from the paper (top-1/top-5 definitions, conv parameter formula, ReLU definition, overfitting definition): mark as our explanation and check against standard knowledge.
- Do not describe [21]'s 10-crop protocol in detail (not read).
