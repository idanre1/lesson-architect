# Review: Reading "Deep Residual Learning for Image Recognition" (ResNet) — lesson.md

Source checked against: arXiv:1512.03385v1, extracted text `resnet.txt` (1420 lines) from the downloaded PDF. "l.N" below means line N of that extracted text. The figures themselves (curves) were not visible in the text extraction; figure statements were checked against captions and the paper's prose only.

## Structural check

Command (run from `examples/paper-resnet/`):

```
python3 ../../skills/lesson-architect/scripts/check_lesson.py lesson.md --kind paper --blueprint lesson.blueprint.md
```

- First draft: **33 passed, 0 warnings, 0 failed.**
- After the first round of audit revisions (items 1–7 below): 33 passed, 0 warnings, 0 failed.
- The skill's `check_lesson.py`, `references/pedagogy.md` and `references/quality-review.md` were updated by someone else during this task. Re-running the updated checker gave **33 passed, 1 warning**: `[WARN] Independent/transfer exercises have hints — no hint for ['E5']`. Fixed (items 8–10 below).
- Final: **34 passed, 0 warnings, 0 failed.**
- This only shows the required parts are present. The audits below found defects the checker could not.

## Continuity audit

| Check | Verdict | Evidence / fix |
|---|---|---|
| Every learning outcome is taught and assessed | Pass | O1 (degradation vs overfitting vs vanishing gradients): Part 2 + Part 3, worked "Diagnosing Fig. 1"; E1 (guided), E5 (transfer). O2 (compute a residual block; zero weights → identity): Part 4 worked toy; E2 (guided). O3 (when a projection is needed, what it costs): Part 5 worked example + Part 6; E3 (independent), E4 (transfer). O4 (which table comparison supports which claim): Part 7 Table 2 walk-through, M4/M5; E6 (independent). O5 (results vs hypotheses): Part 1 certainty ladder, used throughout, Part 8; E7 (check). Reverse check: no exercise assesses something no outcome names. |
| Exercises require no untaught concepts | Pass | E1: train/test error, overfitting, degradation (Part 2). E2: ReLU, Eqn. 1, plain vs residual (Part 4). E3: k·k·Cin·Cout, stride, 1×1 conv (Part 5); options A/B/C (Part 6). E4: bottleneck (Part 6), "multiply-adds ≈ weights × positions" (Part 5, essential text, not the optional box). E5: Table 6 numbers given in the statement; overfitting signature (Part 2); certainty ladder (Part 1). E6: controlled comparison (Part 7), Tables 2–3 (Part 7). E7: ladder (Part 1), §4.1 vanishing-gradient argument (Part 2), Part 8. None depends on the optional boxes. |
| Terminology and notation are introduced before use | Pass after fix | Term trace (first use → explanation): citation brackets (Part 1), ImageNet/CIFAR/top-1/top-5/validation (Part 2 vocabulary), overfitting, degradation, vanishing gradients (Part 2), BN (Part 2), identity mapping, solver/SGD (Part 3), H, F, ReLU σ, shortcut (Part 4), channel, feature map, conv, stride, 1×1, pooling, FLOPs, softmax (glossed in place), stage (Part 5), Ws, options A/B/C, bottleneck (Part 6), ensemble, mAP (glossed / explicitly marked as not needed), Faster R-CNN (glossed as "the same object-detection system") (Part 7). **Defects found:** (1) the BN gloss in Part 2 said "each channel's values" and quoted "after each convolution" before Part 5 defines channel/convolution; (2) "backpropagation" in Part 3 was not glossed. Both fixed (see Revisions). |
| Transitions preserve the learning thread | Pass | Each Part opens with a reason it comes next, e.g. Part 3: "We now know *that* the deeper plain network is worse on its own training data. This part shows why that is genuinely strange"; Part 4: "Part 3 left us with a target: make 'do nothing' (the identity) trivially easy"; Part 5: "Eqn. 1 adds x and F(x) entry by entry, so the two must have exactly the same shape … to see where, you need the vocabulary of convolutional networks"; Part 6: "Part 5 found that 3 of ResNet-34's 16 shortcuts connect tensors of different shapes"; Part 7: "a table of error rates says little until you know which networks differ in which way"; Part 8: "Evidence tells you what was shown; this part collects what was *not*." |
| Worked examples explain reasoning | Pass | Part 4 toy block: each step has a result and a "why" ("F is computed inside-out", "why add rather than replace"); method choice (compare to plain block, then zero weights) stated as the goal up front. Part 5 shortcut example: "why check this first: Eqn. 1 is an element-wise sum". Part 2 "Diagnosing Fig. 1" reasons from what overfitting would predict. |
| Followable without filling missing conceptual steps | Pass (one noted assumption) | Step trace of the toy block: every step uses only matrix-vector products and ReLU, both defined before use. The step "σ(x) = x because block inputs are non-negative" relies on an architectural observation; the lesson says so and labels it as ours. Part 5's shape reasoning uses only stride and channel definitions given just above it. |
| Analogy boundaries and misconceptions | Pass | One analogy (editing a draft, Part 4) with "What the analogy gets right" and three numbered "Where it breaks" points. Misconceptions confronted where they arise: M1 overfitting (Part 2, after Fig. 1), M2 "can't represent" (Part 3, after the construction argument), M3 vanishing gradients (Part 2, revisited in the Part 8 optional box), M4 "extra parameters" (Part 7, Table 3), M5 "two tables disagree" (Part 7, Table 4). Each is stated fairly, shown wrong with paper evidence, and caught by an exercise (E1/E5, E7, E7, E6(d), E6). |
| Synthesis answers the central question | Pass | Opens "We started by asking why simply making a network deeper made it worse … and how rewriting each few layers as 'input plus a learned correction' changes that", answers it in three steps (failure is in training; the fix makes identity the default; the evidence), revisits 18-vs-34 in final form (27.94/28.54 vs 27.88/25.03), states the boundary, the outcomes in plain words, and a next step (a reading route through the real paper). |
| Shape, voice, and optional depth | Pass | Headings are content-driven and varied (e.g. "Diagnosing Fig. 1: is this overfitting?", "Which of ResNet-34's shortcuts can be a plain identity?"); no teacher-facing phrasing (checker and manual read). Two optional `<details>` boxes (multiply-add arithmetic; gradient "+1" reading), neither used by any exercise or later section. Weakness: the lesson is long (~11,000 words). |

## Correctness audit

| Check | Verdict | Evidence / fix |
|---|---|---|
| Claims, calculations, and code checked | Pass after 3 fixes | All quotes and numbers attributed to the paper were checked against the text (scripted + manual), every derived/toy number recomputed in Python, hedges and labels inspected. Two non-verbatim quotes and one overstatement were fixed. No code in the lesson. Details in the rows below and the claim-by-claim table. |
| Quotes attributed to the paper | Pass after fix | Scripted check: every `"…"` segment in lesson.md normalized (ligatures, line-break hyphens, whitespace, ellipses split) and searched in resnet.txt; 144 segments matched. Remaining non-matches were inspected one by one: 6 were genuine paper quotes broken in the extraction by a page footer, interleaved table text or footnote marker "3" (l.92–105, 640–642, 652–656, 741–744, 830–851, 981–995) — all verbatim; the rest are the lesson's own phrases or misconception statements (not attributed to the paper). **Two defects:** the certainty-ladder table quoted "Table 2 shows…" (paper says "The results in Table 2 show", l.465) and "…support our motivation…" (paper: "support our basic motivation", l.964). Fixed. |
| Numbers attributed to the paper | Pass | Every decimal in lesson.md was searched in resnet.txt: all present except 0.0012, 0.28, 0.33, 0.51, 0.84, 1.94, 3.51, 3.7, 115.6 — each is our own derived/toy value, recomputed below. Table rows checked for correct model↔number pairing against Tables 2–6, 8 (claim table below). |
| Calculations | Pass | Recomputed in Python (pure Python; numpy absent): toy block F=(0,−0.4), y=(2,0.6), plain (0,0); E2 W1x=(1,−3), F=(0.5,0), y=(1.5,3), plain (0.5,0), wrong-path (0.5,−1.5)→(1.5,1.5); 0.8³⁰=0.00124, 1.2³⁰=237.4; 2·9·64·64=73,728; 9·64·128+9·128·128=221,184; 8,192/221,184=3.7%; bottleneck 69,632; (69,632+65,536)/69,632=1.94; 4,096/73,728=5.6%; 9·64·64·3136=9·128·128·784=115,605,504; differences 3.51, 0.06, 2.85, 0.84, 0.51, 0.33, 1.5; 3.6/19.6=0.18; 6.0/21.2=0.28; 6n+2 → 20/32/44/56/110/1202. |
| Hedges preserved | Pass | "We hypothesize" (§1, l.113), "suggests that the solvers might" (§3.1, l.223), "may help to precondition" (§3.1, l.230), "still an open question" (fn. 2, l.247), "We argue … unlikely" (§4.1, l.645), "We conjecture … may" (§4.1, l.653), "we expect" (§1, l.155), "We argue that this is because of overfitting … may be unnecessarily large" (§4.2, l.994–995), "support our basic motivation … might be generally closer to zero" (§4.2, l.964–966). None is upgraded to a result in the lesson; E7 tests exactly this. |
| Own interpretations labelled | Pass | "Our interpretation" callouts (Part 4 default-behaviour reading; Part 8 optional gradient-path box explicitly "not the paper's argument"); "Toy example (ours)"; "Limitations we identify (our reading, not the paper's)"; Table 3 vs Table 4 protocol explanation labelled "our reading"; non-negative block inputs labelled "our observation". |
| Domain facts | Pass, from background knowledge | Top-1/top-5 error, overfitting, ReLU, conv weight count k·k·Cin·Cout, stride, pooling, SGD/backprop glosses: standard definitions, stated in the lesson as standard background, not paper claims. |
| Sources | Pass | Only the paper is listed (arXiv URL actually used). Cited works ([16], [21], [41]) explicitly marked as not read. Reference [41] = Simonyan & Zisserman, ICLR 2015 confirmed in the reference list (l.1117). |

### Claim-by-claim check

| # | Lesson statement | Paper location | Verified quote / number |
|---|---|---|---|
| 1 | Nets up to 152 layers, 8× deeper than VGG | Abstract, l.15 | "depth of up to 152 layers—8× deeper than VGG nets" |
| 2 | Ensemble 3.57% top-5 on ImageNet test; 1st place ILSVRC 2015 | Abstract l.17–18; Table 5 | "3.57% error on the ImageNet test set"; "won the 1st place on the ILSVRC 2015 classification task"; Table 5 "ResNet (ILSVRC'15) 3.57" |
| 3 | COCO: 28% relative improvement | Abstract l.23; §4.3 l.1014–1015 | "a 6.0% increase in COCO's standard metric (mAP@[.5, .95]), which is a 28% relative improvement" |
| 4 | Vanishing gradients "largely addressed" by normalized init and BN | §1, l.71–75 | "has been largely addressed by normalized initialization [23, 9, 37, 13] and intermediate normalization layers [16]" |
| 5 | Degradation definition, not caused by overfitting | §1, l.78ff | "accuracy gets saturated (which might be unsurprising) and then degrades rapidly. Unexpectedly, such degradation is not caused by overfitting" |
| 6 | Construction argument; solvers can't find it | §1, l.86–105 | "solution by construction … identity mapping"; "our current solvers on hand are unable to find solutions that are comparably good or better than the constructed solution (or unable to do so in feasible time)" |
| 7 | Residual hypothesis | §1, l.113–117 | "We hypothesize that it is easier to optimize the residual mapping …"; "To the extreme, if an identity mapping were optimal…" |
| 8 | Generality is an expectation | §1, l.155 | "we expect that it is applicable in other vision and non-vision problems" |
| 9 | Solvers might have difficulty with identity | §3.1, l.223 | "suggests that the solvers might have difficulties in approximating identity mappings by multiple nonlinear layers" |
| 10 | Precondition; drive weights toward zero | §3.1, l.225–233 | "may simply drive the weights … toward zero"; "unlikely that identity mappings are optimal, but our reformulation may help to precondition the problem" |
| 11 | Eqn. 1, biases omitted, second ReLU after addition | §3.2 | y = F(x,{Wi}) + x; "for simplifying notations"; "We adopt the second nonlinearity after the addition (i.e., σ(y), see Fig. 2)" |
| 12 | Identity shortcuts free; same params/depth/width/cost | §1 l.125; §3.2 l.257 | "add neither extra parameter nor computational complexity"; "same number of parameters, depth, width, and computational cost (except for the negligible element-wise addition)" |
| 13 | Single-layer F: no advantage observed | §3.2, l.271 | "if F has only a single layer … y = W1x + x, for which we have not observed advantages" |
| 14 | Addition channel by channel on feature maps | §3.2, l.277 | "element-wise addition is performed on two feature maps, channel by channel" |
| 15 | Design rules (i)/(ii); stride-2 downsampling | §3.3, l.286–290 | "(i) for the same output feature map size, the layers have the same number of filters; and (ii) if the feature map size is halved, the number of filters is doubled so as to preserve the time complexity per layer" |
| 16 | 3.6 B FLOPs = 18% of VGG-19 (19.6 B) | §3.3, l.296 | "3.6 billion FLOPs (multiply-adds), which is only 18% of VGG-19 (19.6 billion FLOPs)" |
| 17 | Layer counts 18/34; downsampling at conv3_1, conv4_1, conv5_1 | Table 1, l.603–605 | Table 1 blocks [2,2,2,2] and [3,4,6,3]; caption "Down-sampling is performed by conv3_1, conv4_1, and conv5_1 with a stride of 2"; FLOPs 1.8/3.6/3.8/7.6/11.3 ×10⁹ |
| 18 | BN after each conv, before activation; "For best results" multi-scale | §3.4, l.440, l.449 | "right after each convolution and before activation"; "For best results, we adopt the fully-convolutional form … average the scores at multiple scales" |
| 19 | Table 2 numbers | Table 2, l.638 | plain-18 27.94, plain-34 28.54, ResNet-18 27.88, ResNet-34 25.03 (top-1, 10-crop, val) |
| 20 | Paper rounds to 2.8% and 3.5% | §4.1, l.668–669, l.715 | "(by 2.8%)"; "reduces the top-1 error by 3.5% (Table 2)" — exact differences 2.85 and 3.51 (ours) |
| 21 | Plain-34 higher training error throughout; subspace | §4.1, l.640–644 | "higher training error throughout the whole training procedure, even though the solution space of the 18-layer plain network is a subspace of that of the 34-layer one" |
| 22 | Not vanishing gradients (argued) | §4.1, l.645–650 | "We argue that this optimization difficulty is unlikely to be caused by vanishing gradients"; "backward propagated gradients exhibit healthy norms with BN" |
| 23 | Conjecture: exponentially low convergence rates | §4.1, l.653–656 | "We conjecture that the deep plain nets may have exponentially low convergence rates … will be studied in the future" |
| 24 | 3× more iterations still degrades | §4.1 fn. 3, l.674–676 | "We have experimented with more training iterations (3×) and still observed the degradation problem" |
| 25 | 18-layer nets comparably accurate; ResNet converges faster | §4.1, l.718–722 | "comparably accurate … but the 18-layer ResNet converges faster"; "not overly deep" |
| 26 | Shortcut per pair of 3×3 filters | §4.1, l.659–660 | "a shortcut connection is added to each pair of 3×3 filters as in Fig. 3 (right)" |
| 27 | Options A/B/C | §4.1, l.741–746 | "(A) zero-padding shortcuts are used for increasing dimensions, and all shortcuts are parameter-free"; (B) projections for increasing dimensions; (C) all projections |
| 28 | Table 3 rows | Table 3, l.689ff | VGG-16 28.07/9.33; plain-34 28.54/10.02; A 25.03/7.76; B 24.52/7.46; C 24.19/7.40; 50: 22.85/6.71; 101: 21.75/6.05; 152: 21.43/5.71 |
| 29 | Projections not essential; C's edge from 13 projections | §4.1, l.751–754 | "we attribute this to the extra parameters introduced by many (thirteen) projection shortcuts"; "projection shortcuts are not essential for addressing the degradation problem" |
| 30 | Bottleneck: similar complexity; projection would double cost | §4.1, l.757, l.768–772 | "similar time complexity"; "particularly important"; "the time complexity and model size are doubled" |
| 31 | 50/101/152 better by considerable margins, no degradation | §4.1, l.793 | "more accurate than the 34-layer ones by considerable margins … We do not observe the degradation problem" |
| 32 | Table 4: ResNet-34 B 21.84/5.71; ResNet-152 19.38/4.49 | Table 4, l.~698–703 | values match; caption "single-model results on the ImageNet validation set" (protocol not named — lesson hedges its explanation) |
| 33 | Ensemble of six models of different depth | §4.1, l.804 | "We combine six models of different depth to form an ensemble" |
| 34 | VGG-16/19 FLOPs 15.3/19.6 B; ResNet-152 11.3 B | §4.1, l.789–790; Table 1 | "the 152-layer ResNet (11.3 billion FLOPs) still has lower complexity than VGG-16/19 nets (15.3/19.6 billion FLOPs)" |
| 35 | CIFAR-10: 50k train, 10k test; 6n+2 layers; option A everywhere | §4.2, l.810–832 | "6n+2 stacked weighted layers" (l.825); "50k training images and 10k testing images in 10 classes" (l.810–811); "we use identity shortcuts in all cases (i.e., option A), so our residual models have exactly the same depth, width, and number of parameters" |
| 36 | Table 6 rows | Table 6, l.840–849 | 20: 0.27M 8.75; 32: 0.46M 7.51; 44: 0.66M 7.17; 56: 0.85M 6.97; 110: 1.7M 6.43 (6.61±0.16); 1202: 19.4M 7.93; "best (mean±std)" over 5 runs |
| 37 | ResNet-110 warm-up | §4.2, l.875–879 | "use 0.01 to warm up the training until the training error is below 80% (about 400 iterations), and then go back to 0.1" |
| 38 | Plain-110 error > 60% | Fig. 6 caption, l.925 | "The error of plain-110 is higher than 60% and not displayed" |
| 39 | Fig. 7: smaller responses support basic motivation | §4.2, l.963–966 | "ResNets have generally smaller responses than their plain counterparts. These results support our basic motivation … the residual functions might be generally closer to zero" |
| 40 | 1202 layers: <0.1% training error, worse test error, argued overfitting; no dropout/maxout | §4.2, l.977–1003 | "training error <0.1%"; "although both have similar training error. We argue that this is because of overfitting. The 1202-layer network may be unnecessarily large (19.4M)"; "we use no maxout/dropout"; "combining with stronger regularization may improve results" |
| 41 | COCO Table 8: 21.2 → 27.2; "solely" from representations | Table 8 l.990–991; §4.3 l.1014–1016 | VGG-16 21.2, ResNet-101 27.2 (mAP@[.5, .95]); "This gain is solely due to the learned representations" (l.1016) |

## Revisions made

1. **Correctness:** certainty-ladder table quoted "Table 2 shows…" — not verbatim. Replaced with the verbatim "Table 3 shows…" (l.747) and changed the example column to "The error rates in Tables 2–6".
2. **Correctness:** "…support our motivation…" → verbatim "…support our basic motivation…"; added §4.1 to that row's locations ("indicates", l.670/753).
3. **Continuity:** Part 2's BN gloss used "channel" and "convolution" before Part 5 defines them. Reworded to "rescales the values it receives" and added a forward gloss: "a *convolution* is the kind of weight layer these image networks use; Part 5 explains it."
4. **Continuity:** "SGD with backpropagation" (Part 3) now glossed: "gradient descent on small random batches of examples, with the gradients computed layer by layer from the loss backwards."
5. **Correctness (overstatement):** E5 solution said the authors "themselves suggest" dropout/maxout may help. The paper only says these are used for best results on CIFAR-10 and that "combining with stronger regularization may improve results" (§4.2). Reworded to quote that.
6. **Clarity:** Sources said definitions came from "the author's knowledge" (ambiguous with the paper's authors) → "this lesson's author's background knowledge".
7. **Blueprint:** lesson sections were referenced as "§3", "§5", etc., clashing with the paper's own § numbers and with the lesson's "Part N" headings. Renumbered all to "Part N"; corrected the Sequence rows (Table 1 layer counts and the conv2_x/conv3_1 worked example live in Part 5, not Part 6); hedged M5's "multi-scale" explanation of Table 4 as our reading, matching the lesson.
8. **Hints (updated skill guidance):** added the missing hint for E5 (transfer), which the updated checker flagged.
9. **Graded hints (updated pedagogy §9):** E3, E4, E5 and E6 now have two hints each — the first narrows the problem without naming the operation, the second names the next decision.
10. **Wrong answers (updated pedagogy §9):** added a "Common wrong answer" to E4 (counting the bottleneck's 3×3 layer at 256 channels → 180,224, verified in Python) and E5 (calling it degradation). E1–E3, E6, E7 already had one.
11. **Outcomes (updated pedagogy §3):** added one sentence after the outcome list saying that new terms in the outcomes (degradation, residual block, identity mapping, shortcut, projection, controlled comparison) are explained before the lesson relies on them.
12. Re-ran the checker after all revisions (34 passed, 0 warnings, 0 failed) and re-ran the quote and arithmetic checks over the changed text.

## Not verified / limitations

- **Figures were not inspected visually.** Statements about Fig. 1, 4, 6, 7 rely on their captions and the paper's prose; curve shapes were not read off the plots.
- **Table 4's testing protocol** is not named in its caption. The lesson's explanation (Table 3 = 10-crop; Table 4 likely the §3.4 multi-scale "best results" protocol) is inference and is labelled "our reading".
- **10-crop testing** is glossed from background knowledge; reference [21], which defines it, was not read.
- **Background definitions** (top-1/top-5, overfitting, ReLU, conv arithmetic, SGD, BN's role) are from general knowledge, not a cited source.
- **Text-extraction artefacts:** superscripts were flattened (e.g. "103-layer" in the extraction is 10³ in the PDF; FLOPs "3.6×109" = 3.6×10⁹). The lesson avoids quoting those strings. Footnote markers inside quotes (e.g. "training error 3") were dropped from the lesson's quotes.
- **Learner testing:** no real learner read the lesson; the continuity audit is a simulated cold read by the author.
- **Length:** ~11,200 words. That is long for one sitting; the route and optional boxes help, but a real learner may need two sessions.

## Independent spot-check (second reviewer)

- Re-matched the lesson's direct quotes and reported numbers against the arXiv v1 text with a normalising script. Every quote attributed to the paper is verbatim; the remaining mismatches were PDF-extraction artifacts (page-footer breaks, `W_s` subscripts, a table interrupting a sentence) checked by hand. Numbers checked: 3.57%, 19.38%, 4.49%, 7.93%, 6.43%, 1202 layers, the 3.5% top-1 reduction.
- Confirmed the hedges are preserved: "We argue … unlikely to be caused by vanishing gradients" and "We conjecture … exponentially low convergence rates".
- No changes were needed.
