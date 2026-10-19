# Reading the ResNet Paper: Why Stacking Layers Failed, and How Residual Learning Fixed It

<!-- la:orientation -->
This lesson walks you through one famous research paper: *Deep Residual Learning for Image Recognition* by Kaiming He, Xiangyu Zhang, Shaoqing Ren and Jian Sun (arXiv:1512.03385, December 2015). The paper introduced **residual networks (ResNets)**: networks in which every few layers learn only a *correction* to their input, and the input itself is passed around those layers and added back.

Why it matters: before this paper, people had found something strange. If you took a network that trained well and made it deeper by adding more layers, it could get *worse* — and not just on new data, but on the very data it was trained on. The paper's own example is a pair of image classifiers with 18 and 34 layers: the 34-layer one had the higher error (Table 2). The paper explains why that is surprising, proposes a small architectural change, and shows that with it the 34-layer network beats the 18-layer one, and that networks with 152 layers train well. That 18-versus-34 pair is our running example; we will come back to it in every part.

**Who this is for:** you know what a neural-network layer is (multiply the input by a weight matrix, apply a nonlinearity), what a training loss is, and that gradient descent adjusts weights to reduce the loss. You have never read a research paper, and you don't know convolutional networks in detail — both are taught here, only as far as this paper needs. No calculus is needed beyond "gradient descent follows the slope of the loss".

<!-- la:outcomes -->
By the end of this lesson you will be able to:

1. Explain the *degradation problem* and tell it apart from overfitting and from vanishing gradients, using training- versus test-error evidence.
2. Compute the output of a residual building block (the paper's Eqn. 1) on small numbers, and explain why driving its weights to zero gives an identity mapping while a plain block gives zero.
3. Decide whether a shortcut connection can be an identity or needs a projection (Eqn. 2), and count the extra parameters each shortcut option costs.
4. Judge which comparison in the paper's tables supports a given claim, and whether that comparison is controlled (same depth, parameters, and computation).
5. Sort statements about ResNet into reported results, the authors' arguments, hypotheses and conjectures, and claims the paper does not make.

Don't worry if some of these words are new — *degradation*, *residual block*, *identity mapping*, *shortcut*, *projection*, *controlled comparison* and the rest are each explained before the lesson relies on them.

**The route:** first, a map of how a research paper is built and how authors signal certainty (Part 1). Then the puzzle — deeper networks getting worse (Part 2) — and the argument that this should be impossible in principle (Part 3). With the puzzle sharp, we meet the residual block and compute one by hand (Part 4). Next, just enough about convolutional networks (Part 5) to see where the simple form of the block needs adjusting (Part 6). Only then do we look at the evidence (Part 7) and at where the paper's claims stop (Part 8). Practice and a synthesis close the lesson.

**How to tell the paper's voice from ours.** Throughout, statements are labelled:

- **From the paper (§…, Table …):** what the authors report or claim, with its location so you can check it. Quotes are verbatim.
- **Toy example (ours):** a simplification invented for this lesson. The paper contains no such numbers.
- **Our interpretation:** our reading of why something works or what it implies. Reasonable, but not something the paper states.
- **Limitation:** split into those *stated by the authors* and those *we* identify.

Section signs (§) always refer to the paper's sections, never to this lesson's parts.

## Part 1 — How a research paper is built, and how to hear its certainty

You will be quoting this paper constantly, so we start with how to find your way around it and how to tell a measured result from a guess.

A research paper is an argument with a fixed shape: *here is a problem → here is our idea → here is the evidence → here is what remains open*. This paper follows that shape closely:

| Part of the paper | What it does | What you'll use it for |
|---|---|---|
| Abstract | One-paragraph summary of the whole argument and headline numbers | Deciding whether to read on |
| §1 Introduction | The problem (degradation), the idea (residual learning), the main results | The puzzle, Parts 2–4 |
| §2 Related Work | Earlier ideas the authors build on or differ from | Mostly skippable on a first read |
| §3 Deep Residual Learning | The mechanism: §3.1 the idea, §3.2 the equations, §3.3 the architectures, §3.4 training details | Parts 4–6 |
| §4 Experiments | §4.1 ImageNet, §4.2 CIFAR-10 and analysis, §4.3 object detection | Part 7 |
| References | Numbered list of cited works | Decoding `[41]` and similar |
| Appendices A–C | Details of the detection and localization competition systems | Out of scope here |

Numbers in square brackets are citations: "VGG nets [41]" means "the VGG networks, described in item 41 of the reference list" (Simonyan and Zisserman, 2015). You don't need to read cited papers to follow this one, and this lesson did not read them either; when the paper relies on one, we say "the paper cites…".

**The certainty ladder.** Authors choose verbs carefully, and those verbs tell you how much weight a sentence can bear. From strongest to weakest, as used in this paper:

| Wording | What it signals | Example in this paper |
|---|---|---|
| "Table 3 shows…", "we obtain…", "has 3.6 billion FLOPs" | A measured result | The error rates in Tables 2–6 |
| "We argue that…", "we attribute this to…" | A reasoned explanation the authors believe but did not directly test | §4.1, on vanishing gradients |
| "…suggests…", "…indicates…", "…support our basic motivation…" | Evidence *consistent with* an idea | §3.1, §4.1, §4.2 (Fig. 7) |
| "We hypothesize…", "We conjecture…" | A proposed explanation, offered for testing | §1, §4.1 |
| "We expect…", "may…", "will be studied in the future" | A prediction or open question, not tested in this paper | §1, §4.1, §4.2 |

Here is the ladder applied to two sentences from §1, as a model for how you will read the rest:

- "the 34-layer ResNet exhibits considerably lower training error" (§4.1) — a *measurement*, shown in Fig. 4. You can check it against the figure.
- "We hypothesize that it is easier to optimize the residual mapping than to optimize the original, unreferenced mapping." (§1) — a *hypothesis*. The whole paper is built around it, and the experiments are consistent with it, but no experiment proves it. When you retell the paper, keep the word "hypothesize".

<!-- la:misconception -->
> **A tempting mistake:** "If it's in a published paper, it's an established fact." Most sentences in a paper are not results; they are explanations, guesses, and expectations wrapped around a few measurements. Retelling "we hypothesize X" as "the paper proved X" changes the claim. The correct habit: for every claim, ask *which table or figure measures this?* — and if none does, keep the authors' hedge.

## Part 2 — The puzzle: deeper networks got worse

With the map in hand, we can state the problem the paper attacks. First we need a few words for measuring how well a network does, because the whole puzzle rests on *which* error went up.

**The task.** In *image classification*, a network receives an image and must name which of a fixed list of classes it shows. The paper's main dataset is **ImageNet**: "1000 classes", trained on "1.28 million training images" and "evaluated on the 50k validation images", with a final result "on the 100k test images" (§4.1). Its second dataset is **CIFAR-10**: "50k training images and 10k testing images in 10 classes" (§4.2), each image only 32×32 pixels.

**Two kinds of error.** *Training error* is the fraction of training images the network gets wrong — images it has learned from. *Test error* (or *validation error*, when measured on a held-out set used during development) is the fraction wrong on images it has never seen. ImageNet results are also reported as **top-1** and **top-5** error: the network ranks all 1000 classes, top-1 error counts an image as wrong if the correct class is not the network's first choice, and top-5 error counts it wrong only if the correct class is not among its five highest-ranked choices. (These definitions are standard in the field; the paper uses the terms without defining them.)

**Overfitting** is the familiar way for a bigger model to disappoint: it fits the training images very well — low training error — but has learned quirks of those specific images, so its test error is high. *The signature of overfitting is a gap: low training error, higher test error.* Keep that signature in mind; it is the key to the whole puzzle.

**Why go deeper at all?** From the paper (§1): "Recent evidence [41, 44] reveals that network depth is of crucial importance", and leading ImageNet results used models "with a depth of sixteen [41] to thirty [16]" layers. So the paper asks (§1): "Is learning better networks as easy as stacking more layers?"

### The first obstacle, already mostly solved: vanishing gradients

When gradient descent updates an early layer of a deep network, the gradient for that layer is computed by backpropagation, which multiplies together one factor per layer between it and the loss. **Toy example (ours):** if each of 30 layers contributed a factor of about 0.8, the product would be $0.8^{30} \approx 0.0012$ — the early layers would barely learn (*vanishing* gradients). With a factor of 1.2 per layer it would be $1.2^{30} \approx 237$ — wild, unstable steps (*exploding* gradients). Real gradients are matrices, not single numbers, but the multiplication-through-many-layers intuition is the point.

**From the paper (§1):** this problem "has been largely addressed by normalized initialization [23, 9, 37, 13] and intermediate normalization layers [16], which enable networks with tens of layers to start converging". The normalization layers of [16] are **batch normalization (BN)**: a layer, placed after each weight layer, that rescales the values it receives to a standard spread during training. The paper uses BN "right after each convolution and before activation" (§3.4) — a *convolution* is the kind of weight layer these image networks use; Part 5 explains it. You need only one fact about BN for this lesson: it keeps the signal passing through the network from shrinking to nothing.

### The second obstacle, the one this paper is about: degradation

**From the paper (§1):** "When deeper networks are able to start converging, a *degradation* problem has been exposed: with the network depth increasing, accuracy gets saturated (which might be unsurprising) and then degrades rapidly. Unexpectedly, such degradation is not caused by overfitting, and adding more layers to a suitably deep model leads to higher *training* error".

Fig. 1 of the paper shows it on CIFAR-10 with two "plain" networks — ordinary stacks of layers, no tricks — of 20 and 56 layers. The caption reads: "The deeper network has higher training error, and thus test error."

<!-- la:worked-example -->
### Diagnosing Fig. 1: is this overfitting?

*Goal:* decide whether the 56-layer network in Fig. 1 is worse because it overfits.

1. **Pick the right evidence.** Overfitting is a statement about the *gap* between training and test error, so we must look at training error, not just test error. Fig. 1 conveniently has both: training error on the left, test error on the right.
2. **State what overfitting would predict.** If the 56-layer net overfit, it would fit the training images *at least as well* as the 20-layer net (lower or equal training error) but do worse on test images.
3. **Compare with what is observed.** The caption says the deeper network "has higher training error, and thus test error". Its training error is *higher*. That contradicts step 2's prediction.
4. **Conclude, and check against the authors.** The deeper network is not worse because it memorized; it is worse at *fitting the training data at all*. That is exactly the paper's claim: degradation "is not caused by overfitting" (§1).

*Before reading on:* why does the caption say "and *thus* test error"? — Because if a network can't even fit its training images, there is no reason to expect it to do better on unseen ones; the higher test error is a consequence of the higher training error, not a separate failure.

<!-- la:misconception -->
> **A tempting mistake:** "A deeper net that does worse must be overfitting — it has more parameters." This is the explanation most people reach for, and it is a good one for the *usual* failure. But overfitting predicts *lower* training error for the bigger model, and Fig. 1 (left) and Fig. 4 (left) show *higher* training error. The correct model: degradation is an **optimization** failure — training didn't find good weights — not a **generalization** failure.

**The running example.** The paper sees the same thing on ImageNet. **From the paper (Table 2, §4.1):** top-1 validation error of the 18-layer plain net is **27.94%**; of the 34-layer plain net, **28.54%**. Fig. 4 (left) shows why: "the 34-layer plain net has higher training error throughout the whole training procedure" (§4.1). Footnote 3 adds that training for three times as many iterations "still observed the degradation problem".

### "Isn't this just vanishing gradients again?"

A natural guess. **From the paper (§4.1):** "We argue that this optimization difficulty is unlikely to be caused by vanishing gradients. These plain networks are trained with BN [16], which ensures forward propagated signals to have non-zero variances. We also verify that the backward propagated gradients exhibit healthy norms with BN." And the 34-layer plain net still reaches "competitive accuracy (Table 3), suggesting that the solver works to some extent."

So what *is* the cause? Here the paper is honest that it doesn't know: "We conjecture that the deep plain nets may have exponentially low convergence rates, which impact the reducing of the training error. The reason for such optimization difficulties will be studied in the future." (§4.1). Notice where those sentences sit on the certainty ladder: "argue", "unlikely", "conjecture", "will be studied". Many popular retellings say "ResNets solved vanishing gradients"; this paper does not say that.

<!-- la:exercise id=E1 outcomes=1 level=guided -->
**Try it (guided).** Two pairs of networks were trained on the same images. The numbers are invented for this exercise.

| Pair | Shallower net: training / test error | Deeper net: training / test error |
|---|---|---|
| Pair 1 | 6% / 10% | 9% / 13% |
| Pair 2 | 6% / 10% | 1% / 14% |

For each pair: (a) which net has the lower *training* error? (b) which has the lower *test* error? (c) using the signature of overfitting, decide whether the deeper net is suffering from overfitting or from degradation.

## Part 3 — Deeper should never be worse (in principle)

We now know *that* the deeper plain network is worse on its own training data. This part shows why that is genuinely strange — strange enough that it points straight at the fix.

An **identity mapping** is a function that returns its input unchanged: $I(x) = x$. A layer (or a few layers) that computes an identity mapping is a pass-through: whatever comes in goes out.

**From the paper (§1):** "Let us consider a shallower architecture and its deeper counterpart that adds more layers onto it. There exists a solution by construction to the deeper model: the added layers are identity mapping, and the other layers are copied from the learned shallower model. The existence of this constructed solution indicates that a deeper model should produce no higher training error than its shallower counterpart."

Unpacked step by step:

1. Train the shallow network; it reaches some training error, say $e$.
2. Build the deeper network by inserting extra layers, and set every extra layer to the identity. Copy all other weights from the shallow network.
3. Every image now flows through exactly the same computation as before — the extra layers change nothing — so this deeper network also has training error $e$.
4. So *some* setting of the deeper network's weights achieves $e$. The best setting can only be as good or better.

For the running example, the paper makes the same point directly: the 34-layer plain net has higher training error "even though the solution space of the 18-layer plain network is a subspace of that of the 34-layer one" (§4.1). A *solution space* is the set of all functions a network can compute by choosing its weights; "subspace" means every function the 18-layer net can compute, the 34-layer net can compute too.

So the deeper network is not *incapable* of matching the shallow one. **From the paper (§1):** "experiments show that our current solvers on hand are unable to find solutions that are comparably good or better than the constructed solution (or unable to do so in feasible time)." A *solver* here is the training procedure — stochastic gradient descent (SGD) with backpropagation — gradient descent on small random batches of examples, with the gradients computed layer by layer from the loss backwards.

<!-- la:misconception -->
> **A tempting mistake:** "The deeper plain network just can't express as good a function as the shallow one." The construction above shows it *can* — it can always copy the shallow net and pass the result through. The failure is in *finding* those weights by gradient descent. The correct model: degradation is about what training **finds**, not what the network **can represent**. This distinction is the heart of the paper.

Which part of the constructed solution might be hard to find? **From the paper (§3.1):** "The degradation problem suggests that the solvers might have difficulties in approximating identity mappings by multiple nonlinear layers." Note the hedges: "suggests", "might". This is the authors' diagnosis, and the next part is their cure: if identity mappings are hard for a stack of layers to learn, rebuild the stack so that the identity is the easiest thing of all.

## Part 4 — The residual block: learn the correction, not the whole thing

Part 3 left us with a target: make "do nothing" (the identity) trivially easy for a group of layers. This part shows the paper's reformulation, computes one block by hand, and connects it back to that target.

**The notation, in the paper's own symbols (§3.1).** Focus on "a few stacked layers (not necessarily the entire net)". Let

- $x$ be the input to the first of these layers (a vector of numbers);
- $H(x)$ be the "desired underlying mapping" — whatever function we would *like* these layers to compute;
- $F(x) := H(x) - x$ be the **residual**: the difference between what we want and what we already have. (The paper writes $F$ in a calligraphic font, $\mathcal{F}$; it is the same symbol.)

Rearranging, $H(x) = F(x) + x$. Instead of asking the layers to produce $H(x)$ directly, the paper asks them to produce only $F(x)$, and adds $x$ back afterwards. This requires $x$ and $F(x)$ to have the same dimensions, so the addition makes sense; Part 6 deals with what happens when they don't.

**From the paper (§1):** "We hypothesize that it is easier to optimize the residual mapping than to optimize the original, unreferenced mapping. To the extreme, if an identity mapping were optimal, it would be easier to push the residual to zero than to fit an identity mapping by a stack of nonlinear layers."

**The building block (§3.2, Fig. 2).** Formally, the block is

$$
y = F(x, \{W_i\}) + x \qquad \text{(Eqn. 1)}
$$

where $\{W_i\}$ are the weights of the stacked layers and $y$ is the block's output. In Fig. 2 the stack has two layers, so $F = W_2\,\sigma(W_1 x)$, where $\sigma$ is **ReLU** (rectified linear unit), applied entry by entry: $\sigma(v) = \max(0, v)$, which keeps positive numbers and replaces negative numbers by 0. Biases are omitted "for simplifying notations". The "$+\,x$" is done by a **shortcut connection** — a wire that skips the stacked layers — followed by element-wise addition. Finally, "We adopt the second nonlinearity after the addition (i.e., $\sigma(y)$, see Fig. 2)", so the block's final output is $\sigma(y)$.

```
            x ──────────────────────────────┐
            │                               │  identity shortcut
      weight layer  (W1)                    │  (no weights)
            │                               │
          ReLU                              │
            │                               │
      weight layer  (W2)                    │
            │                               │
          F(x) ─────────────────────► (+) ◄─┘
                                       │
                                     ReLU
                                       │
                                  output σ(F(x) + x)
```

A *plain* block is the same picture without the shortcut: its output is $\sigma(F(x)) = \sigma(W_2\,\sigma(W_1 x))$.

<!-- la:paper-claim -->
> **From the paper (§1, §3.2): the shortcut is free.** "Identity shortcut connections add neither extra parameter nor computational complexity." The only extra work is the element-wise addition, which the paper calls "negligible". This matters later: it lets the authors compare plain and residual networks with "the same number of parameters, depth, width, and computational cost" (§3.2).

<!-- la:worked-example -->
### Computing one block by hand: residual versus plain

**Toy example (ours).** We use two-dimensional vectors so every number fits on a line. Input and weights:

$$
x = \begin{pmatrix} 2 \\ 1 \end{pmatrix}, \quad
W_1 = \begin{pmatrix} 0.5 & -1 \\ 1 & 0 \end{pmatrix}, \quad
W_2 = \begin{pmatrix} 0.1 & 0 \\ 0 & -0.2 \end{pmatrix}
$$

*Goal:* compute the residual block's output, compare it with a plain block that has the same weights, then see what each block does when its weights are zero.

1. **First layer, $W_1 x$.** Each output entry is a row of $W_1$ times $x$: $0.5\cdot 2 + (-1)\cdot 1 = 0$ and $1\cdot 2 + 0\cdot 1 = 2$. So $W_1 x = (0, 2)$. *Why this first:* $F$ is computed inside-out, exactly as written in $W_2\,\sigma(W_1 x)$.
2. **ReLU, $\sigma(W_1 x)$.** No entry is negative, so nothing changes: $(0, 2)$. *Check:* ReLU only ever turns negatives into 0.
3. **Second layer, $F = W_2\,\sigma(W_1 x)$.** $0.1\cdot 0 + 0\cdot 2 = 0$ and $0\cdot 0 + (-0.2)\cdot 2 = -0.4$. So $F(x) = (0, -0.4)$. This is the *residual*: the correction the block proposes.
4. **Add the shortcut, $y = F(x) + x$ (Eqn. 1).** $(0 + 2,\; -0.4 + 1) = (2, 0.6)$. *Why add rather than replace:* the shortcut carries $x$ around the layers untouched; the layers only nudge it.
5. **Final ReLU, $\sigma(y)$.** Both entries are positive, so the output is $(2, 0.6)$ — recognisably the input $(2, 1)$, with the second entry pulled down.
6. **Same weights, plain block.** Without the shortcut the output is $\sigma(F(x)) = \sigma((0, -0.4)) = (0, 0)$. The input has vanished entirely; the plain block's output depends only on what the layers compute.

*Now set every weight to zero.* Residual block: $F(x) = W_2\,\sigma(W_1 x) = (0,0)$, so $y = x$ and the output is $\sigma(x) = (2, 1)$ — **the identity**. Plain block: output $\sigma(0) = (0, 0)$ — **the zero mapping**.

*Before reading on: why is $\sigma(x) = x$ here?* — Because $x$ has no negative entries. In the paper's design every block ends with a ReLU (Fig. 2), so the input to the next block is never negative, and the final ReLU leaves it unchanged. (This last step is our observation about the architecture, not a sentence from the paper.)

*Could the plain block be an identity too?* Yes: with $W_1 = W_2 = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$, the plain block outputs $\sigma(\sigma(x)) = x$ for any non-negative $x$. So both blocks *can* represent the identity — which is exactly Part 3's point. The difference is *where* the identity sits: for the residual block it is at "all weights zero"; for the plain block it is at one particular non-zero setting that training has to discover.

**From the paper (§3.1)** — this is precisely their argument, with its hedges: "With the residual learning reformulation, if identity mappings are optimal, the solvers may simply drive the weights of the multiple nonlinear layers toward zero to approach identity mappings."

**From the paper (§3.1), the realistic case.** "In real cases, it is unlikely that identity mappings are optimal, but our reformulation may help to precondition the problem. If the optimal function is closer to an identity mapping than to a zero mapping, it should be easier for the solver to find the perturbations with reference to an identity mapping, than to learn the function as a new one." To *precondition* a problem means to restate it so that a solver reaches the answer more easily, without changing the answer; §2 relates this to classic numerical methods that solve for residuals between coarse and fine versions of a problem. *Perturbations* are small changes.

<!-- la:interpretation -->
> **Our interpretation.** A useful way to hold this: a residual block's "default" behaviour is to pass its input through, and its weights describe *departures* from that default. A plain block has no default — every useful behaviour, including "pass it through", must be built from scratch by its weights. If good deep networks mostly need each block to make modest adjustments, the residual parameterization starts training much closer to the answer. This is a reading of §3.1's hypothesis, not a proof of it; the paper offers it as motivation and then checks a prediction of it (Part 7, Fig. 7).

**An analogy, with its limits.** A residual block is like *editing a draft* rather than *writing from scratch*: the draft ($x$) is handed to you, and your job ($F$) is to propose changes; "make no changes" is effortless. What the analogy gets right: the starting point is the input, and doing nothing is free. Where it breaks: (1) an editor knows what a good text looks like, while gradient descent is just following slopes — the analogy says nothing about *why* finding the edits should be easier; that is the paper's hypothesis, not a consequence of the picture; (2) nothing in Eqn. 1 forces $F$ to be small — the "edit" can rewrite the draft completely; (3) the block computes $F$ *from* $x$ in one go, rather than revising in rounds.

**One more detail from §3.2.** The stacked part $F$ needs at least two layers to matter: "if $F$ has only a single layer, Eqn.(1) is similar to a linear layer: $y = W_1 x + x$, for which we have not observed advantages." The paper's blocks use two or three layers.

<!-- la:exercise id=E2 outcomes=2 level=guided -->
**Try it (guided).** Use the same two-layer residual block (Eqn. 1 with $F = W_2\,\sigma(W_1 x)$ and a final ReLU) with

$$
x = \begin{pmatrix} 1 \\ 3 \end{pmatrix}, \quad
W_1 = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}, \quad
W_2 = \begin{pmatrix} 0.5 & 0 \\ 0 & 0.5 \end{pmatrix}.
$$

Follow the worked example's steps: (a) $W_1 x$; (b) $\sigma(W_1 x)$; (c) $F(x)$; (d) $y = F(x) + x$; (e) the block's output $\sigma(y)$; (f) the output of a plain block with the same weights; (g) name one change to the weights that makes this residual block output exactly $x$ for every non-negative input.

## Part 5 — Just enough about convolutional networks

Eqn. 1 adds $x$ and $F(x)$ entry by entry, so the two must have exactly the same shape. In our toy they were both 2-number vectors. In the real ResNet they are image-shaped blocks of numbers whose shape *changes* as data flows through the network — and to see where, you need the vocabulary of convolutional networks. The paper says its vector notation is "for simplicity" and that Eqn. 1 applies equally to convolutional layers, with "element-wise addition … performed on two feature maps, channel by channel" (§3.2). This part teaches only what is needed to read the architecture figures and tables. (The definitions here are standard background, not claims of the paper.)

**Images and feature maps.** A colour image is a grid of pixels, height × width, with 3 numbers per pixel (red, green, blue). Each of those per-pixel number slots is a **channel**. After a layer processes the image, the result is again a grid of positions with some number of channels — called a **feature map**. The paper writes sizes like "56×56" for the grid and "64-d" or "64" for the number of channels.

**Convolutional layer.** A convolutional ("conv") layer with 3×3 *filters* computes each output number from a 3×3 patch of neighbouring positions, across *all* input channels, as a weighted sum. Two things make it different from the fully-connected layers you know:

- the same weights are reused ("slid") at every position of the grid;
- each filter produces one output channel, so "3x3 conv, 64" in Fig. 3 means 64 filters, giving 64 output channels.

So a conv layer is still "weights times inputs, then a nonlinearity" — just organized so that each output looks at a small neighbourhood and the weights are shared across positions.

**Counting a conv layer's weights.** One filter has $k \times k \times C_{in}$ weights ($k$ = filter size, $C_{in}$ = input channels). With $C_{out}$ filters:

$$
\text{weights} = k \cdot k \cdot C_{in} \cdot C_{out}
$$

(ignoring biases and BN's two numbers per channel, which are tiny by comparison). Because each weight is used once at every output position, a conv layer's multiply-adds are about weights × (output height × output width). The paper reports computation as **FLOPs**, which it explicitly counts as "multiply-adds" (§3.3).

**Stride.** A conv with *stride 2* moves its filter two positions at a time, so the output grid has half the height and half the width. Fig. 3 marks such layers "/2".

**1×1 convolution.** With $k = 1$, a conv layer looks at a single position: it mixes the channels at each position independently, like a small fully-connected layer applied at every pixel. Its weight count is $C_{in}\cdot C_{out}$.

**Pooling.** *Max pooling* replaces each small patch by its largest value (Table 1's "3×3 max pool, stride 2"). *Global average pooling* averages each channel over the whole grid, leaving one number per channel. The paper's networks end with global average pooling and "a 1000-way fully-connected layer with softmax" (§3.3), which turns those numbers into a score for each class.

**The plain network the paper builds on (§3.3, Fig. 3 middle).** It "mostly ha[s] 3×3 filters" and follows two rules: "(i) for the same output feature map size, the layers have the same number of filters; and (ii) if the feature map size is halved, the number of filters is doubled so as to preserve the time complexity per layer." Downsampling is done by convs "that have a stride of 2". **From the paper (§3.3):** the 34-layer baseline "has 3.6 billion FLOPs (multiply-adds), which is only 18% of VGG-19 (19.6 billion FLOPs)" — VGG-19 being an earlier, widely used 19-layer network [41].

**The running example, layer by layer (Table 1).** The 34-layer network is: one 7×7 conv with 64 filters and stride 2 ("conv1"), a max pool, then four *stages* of 3×3 conv pairs — 3 pairs at 56×56 with 64 channels ("conv2_x"), 4 pairs at 28×28 with 128 ("conv3_x"), 6 pairs at 14×14 with 256 ("conv4_x"), 3 pairs at 7×7 with 512 ("conv5_x") — then average pooling and the 1000-way fully-connected layer. Counting weighted layers: $1 + 2\times(3+4+6+3) + 1 = 34$. The 18-layer network has 2 pairs per stage: $1 + 2\times(2+2+2+2) + 1 = 18$. Table 1's caption: "Downsampling is performed by conv3_1, conv4_1, and conv5_1 with a stride of 2" — that is, by the first layer of each stage after the first.

The *residual* 34-layer network (Fig. 3 right) is the same stack with "a shortcut connection … added to each pair of 3×3 filters" (§4.1). Each pair plus its shortcut is one residual block, so ResNet-34 has $3+4+6+3 = 16$ blocks and 16 shortcuts.

<!-- la:worked-example -->
### Which of ResNet-34's shortcuts can be a plain identity?

*Goal:* for two blocks of ResNet-34, decide whether Eqn. 1 can be used as written, and count what the block's convolutions cost.

**Block A: any block inside conv2_x.** Both convs are "3×3, 64" on a 56×56 grid, no stride.

1. *Shapes.* Input: 56×56 with 64 channels. Each conv keeps the grid (no stride) and outputs 64 channels, so $F(x)$ is also 56×56×64. *Why check this first:* Eqn. 1 is an element-wise sum, so equal shapes is the one requirement.
2. *Verdict.* Shapes match, so the identity shortcut works: $y = F(x) + x$, adding zero weights.
3. *Cost of $F$.* Each conv: $3\cdot 3\cdot 64\cdot 64 = 36{,}864$ weights; the pair: $73{,}728$. The shortcut adds 0, as §3.2 promised.

**Block B: the first block of conv3_x ("conv3_1").** Its first conv is "3×3, 128" with stride 2; its second is "3×3, 128".

1. *Shapes.* Input: 56×56×64 (the output of conv2_x). The stride-2 conv halves the grid to 28×28 and produces 128 channels; the second conv keeps 28×28×128. So $F(x)$ is 28×28×128, while $x$ is 56×56×64.
2. *Verdict.* The shapes differ in *both* grid size and channels, so $F(x) + x$ is undefined. Eqn. 1 cannot be used as written here. *Quick check:* the same happens at conv4_1 and conv5_1, so exactly 3 of the 16 shortcuts face this problem; the other 13 are like Block A.

How the paper repairs Block B is the subject of the next part.

<!-- la:optional -->
<details>
<summary>Optional: why "double the filters when halving the grid" keeps time per layer constant</summary>

A 3×3 conv's multiply-adds are about $9 \cdot C_{in}\cdot C_{out} \cdot (\text{height}\times\text{width})$. Halving height and width divides the positions by 4; doubling both $C_{in}$ and $C_{out}$ multiplies $C_{in}\cdot C_{out}$ by 4. The two cancel. Check: a 3×3, 64→64 conv on 56×56 and a 3×3, 128→128 conv on 28×28 both cost $9\cdot 64\cdot 64\cdot 3136 = 9\cdot 128\cdot 128\cdot 784 \approx 115.6$ million multiply-adds. This is our arithmetic illustrating rule (ii) of §3.3; nothing later depends on it.

</details>

## Part 6 — When the shapes don't match: projection shortcuts and the bottleneck

Part 5 found that 3 of ResNet-34's 16 shortcuts connect tensors of different shapes. This part gives the paper's two repairs, compares their cost, and then introduces the block design the paper uses for its deepest networks — where the cost of shortcuts suddenly matters a great deal.

**From the paper (§3.2):** when dimensions differ, "we can perform a linear projection $W_s$ by the shortcut connections to match the dimensions":

$$
y = F(x, \{W_i\}) + W_s x \qquad \text{(Eqn. 2)}
$$

$W_s$ is a weight matrix on the shortcut — a *projection* — chosen so that $W_s x$ has the same shape as $F(x)$. In a convolutional network this is "done by 1×1 convolutions", and "when the shortcuts go across feature maps of two sizes, they are performed with a stride of 2" (§3.3). A projection has weights, so it is no longer free.

**The three options (§3.3, §4.1).** The paper tests three ways to handle shortcuts in ResNet-34:

- **(A)** "zero-padding shortcuts are used for increasing dimensions, and all shortcuts are parameter-free": the shortcut stays an identity, takes every other position (stride 2) to shrink the grid, and fills the missing extra channels with zeros. No extra parameters at all.
- **(B)** "projection shortcuts are used for increasing dimensions, and other shortcuts are identity": only the 3 shape-changing shortcuts get a 1×1 projection.
- **(C)** "all shortcuts are projections": all 16 shortcuts get one, including the 13 where shapes already match.

The paper's stated preference (§3.2): "the identity mapping is sufficient for addressing the degradation problem and is economical, and thus $W_s$ is only used when matching dimensions."

**The bottleneck block (§4.1, Fig. 5 right).** For the 50-, 101- and 152-layer networks, "[b]ecause of concerns on the training time that we can afford", the authors replace each two-layer block by a three-layer one: "1×1, 3×3, and 1×1 convolutions, where the 1×1 layers are responsible for reducing and then increasing (restoring) dimensions, leaving the 3×3 layer a bottleneck with smaller input/output dimensions." In Fig. 5 (right) the block's input and output have 256 channels; the first 1×1 conv squeezes them to 64, the 3×3 conv works at 64, and the last 1×1 conv restores 256. The paper notes that Fig. 5's ordinary block (left, 64 channels) and bottleneck block (right, 256 channels) "have similar time complexity". Footnote 4 adds that the bottleneck choice "is mainly due to practical considerations".

**From the paper (§4.1):** "The parameter-free identity shortcuts are particularly important for the bottleneck architectures. If the identity shortcut in Fig. 5 (right) is replaced with projection, one can show that the time complexity and model size are doubled, as the shortcut is connected to the two high-dimensional ends." You will check this claim yourself in Exercise 4.

**The deeper networks (Table 1, §4.1).** ResNet-50 replaces each two-layer block of the 34-layer net with a three-layer bottleneck block (stages of 3, 4, 6, 3 blocks: $3\times 16 + 2 = 50$ layers) and uses option B. ResNet-101 and ResNet-152 use more blocks (3, 4, 23, 3 and 3, 8, 36, 3), giving $3\times 33 + 2 = 101$ and $3\times 50 + 2 = 152$ layers. Their computation (Table 1): 3.8, 7.6 and 11.3 billion FLOPs. **From the paper (§4.1):** "the 152-layer ResNet (11.3 billion FLOPs) still has lower complexity than VGG-16/19 nets (15.3/19.6 billion FLOPs)."

**The CIFAR-10 networks (§4.2).** For the small dataset the paper uses a simpler family: a first 3×3 conv, then three stages of $2n$ layers on 32×32, 16×16 and 8×8 grids with 16, 32 and 64 filters, then global average pooling and a 10-way fully-connected layer — "totally $6n+2$ stacked weighted layers". Shortcuts join pairs of 3×3 layers ($3n$ shortcuts), and "we use identity shortcuts in all cases (i.e., option A), so our residual models have exactly the same depth, width, and number of parameters as the plain counterparts." With $n = 3, 5, 7, 9$ this gives 20, 32, 44 and 56 layers; $n = 18$ gives 110; $n = 200$ gives 1202.

## Part 7 — The evidence

You now know the problem, the hypothesis, and the machinery. That is the order in which evidence becomes meaningful: a table of error rates says little until you know which networks differ in which way. This part reads the paper's main tables and figures and asks of each one: *what exactly was changed, and what was held fixed?*

### The running example, resolved (Table 2, Fig. 4)

*Predict first.* The plain 18- and 34-layer nets scored 27.94% and 28.54% top-1 error. Now add an identity shortcut to every pair of layers (option A: no new parameters). If the residual hypothesis is right, what should happen to the ordering of 18 versus 34 layers? Commit to an answer before reading on.

<!-- la:paper-claim -->
> **From the paper (Table 2):** top-1 error (%, 10-crop testing) on ImageNet validation.
>
> | | plain | ResNet |
> |---|---|---|
> | 18 layers | 27.94 | 27.88 |
> | 34 layers | 28.54 | 25.03 |
>
> The caption states: "Here the ResNets have no extra parameter compared to their plain counterparts." (*10-crop testing* averages the network's predictions over 10 crops of each test image; the paper cites [21] for the protocol.)

How to read it, one comparison at a time:

- **Down the ResNet column:** 27.88 → 25.03. With shortcuts, the deeper network is better, by $27.88 - 25.03 = 2.85$ percentage points. The paper (§4.1): "the situation is reversed with residual learning – the 34-layer ResNet is better than the 18-layer ResNet (by 2.8%)". More importantly, "the 34-layer ResNet exhibits considerably lower training error and is generalizable to the validation data" (Fig. 4 right). That is the degradation problem going away: "This indicates that the degradation problem is well addressed in this setting".
- **Across the 34-layer row:** 28.54 → 25.03, a drop of $3.51$ points; the paper says "ResNet reduces the top-1 error by 3.5% (Table 2), resulting from the successfully reduced training error (Fig. 4 right vs. left)".
- **Across the 18-layer row:** 27.94 vs 27.88, nearly equal. The paper: the 18-layer nets "are comparably accurate … but the 18-layer ResNet converges faster" — when a network is "not overly deep", SGD already finds good solutions for the plain net, and the shortcuts mainly speed up early training.

*Why this comparison is trustworthy:* within each row, the plain and residual networks have the same depth, the same layers, the same number of parameters, and (except for the negligible additions) the same computation — the paper made the shortcuts free precisely so this comparison would be "fair" (§3.2). Only one thing differs: the shortcuts. A comparison that changes exactly one thing is called **controlled**; it is the strongest kind of evidence a table can offer.

### Is it just the extra parameters? (Table 3, options A/B/C)

> **From the paper (Table 3):** ImageNet validation error (%, 10-crop), top-1 / top-5: plain-34 **28.54 / 10.02**; ResNet-34 A **25.03 / 7.76**; ResNet-34 B **24.52 / 7.46**; ResNet-34 C **24.19 / 7.40**.

The authors' reading (§4.1), with its verbs: "all three options are considerably better than the plain counterpart. B is slightly better than A. We argue that this is because the zero-padded dimensions in A indeed have no residual learning. C is marginally better than B, and we attribute this to the extra parameters introduced by many (thirteen) projection shortcuts. But the small differences among A/B/C indicate that projection shortcuts are not essential for addressing the degradation problem." The "thirteen" is the 13 same-shape shortcuts that only option C turns into projections.

<!-- la:misconception -->
> **A tempting mistake:** "Residual networks win because the shortcuts add capacity." Option A adds *no* parameters, and it already closes most of the gap: plain-34 → A is 3.51 points of top-1 error, while A → C, which adds 16 projections, is only $25.03 - 24.19 = 0.84$ more. The correct model: the gain comes from *how* the layers are parameterized (learning a residual around an identity), not from having more weights.

### Going much deeper on ImageNet (Tables 3, 4, 5)

> **From the paper (Table 3, 10-crop, top-1 / top-5):** ResNet-50 **22.85 / 6.71**; ResNet-101 **21.75 / 6.05**; ResNet-152 **21.43 / 5.71**. For comparison, VGG-16 **28.07 / 9.33**.
>
> **From the paper (§4.1):** "The 50/101/152-layer ResNets are more accurate than the 34-layer ones by considerable margins (Table 3 and 4). We do not observe the degradation problem and thus enjoy significant accuracy gains from considerably increased depth."
>
> **From the paper (Table 4, §4.1):** the 152-layer ResNet's best single-model result is **19.38%** top-1 and **4.49%** top-5 validation error. **(Table 5, abstract):** an *ensemble* — six models of different depth whose predictions are combined (§4.1) — reaches **3.57%** top-5 error on the ImageNet test set, which "won the 1st place in ILSVRC 2015" (the ImageNet competition).

<!-- la:misconception -->
> **A tempting mistake (reading tables):** "ResNet-34 B has a top-1 error of 24.52% — no wait, Table 4 says 21.84%, so the paper contradicts itself." Both numbers are in the paper, for the same model. Table 3's caption says "10-crop testing"; Table 4's caption says "single-model results" and does not name the protocol, but §3.4 says that "[f]or best results" the authors use a fully-convolutional form and "average the scores at multiple scales". Different testing protocols give different numbers; the difference here is most likely that (our reading — the paper does not compare the two tables explicitly). The habit to build: **read the caption before the number**, and only compare numbers measured the same way.

### The same story on a different dataset (CIFAR-10: Fig. 6, Table 6)

If degradation were a quirk of ImageNet, the fix might be too. **From the paper (§4.2):** with plain nets of 20, 32, 44 and 56 layers, "[t]he deep plain nets suffer from increased depth, and exhibit higher training error when going deeper" (Fig. 6 left; "The error of plain-110 is higher than 60% and not displayed"). The ResNets "manage to overcome the optimization difficulty and demonstrate accuracy gains when the depth increases" (Fig. 6 middle). Since these use option A, plain and residual nets again have identical parameter counts — another controlled comparison.

> **From the paper (Table 6):** CIFAR-10 test error (%): ResNet-20 **8.75** (0.27M parameters), ResNet-32 **7.51** (0.46M), ResNet-44 **7.17** (0.66M), ResNet-56 **6.97** (0.85M), ResNet-110 **6.43** (1.7M). For ResNet-110 the paper ran training 5 times and reports "best (mean±std)": **6.43 (6.61±0.16)**.

Going to 110 layers needed one adjustment: the initial learning rate of 0.1 was "slightly too large to start converging", so training began at 0.01 "until the training error is below 80% (about 400 iterations)" and then returned to 0.1 (§4.2).

### Testing a prediction of the hypothesis (Fig. 7)

The residual hypothesis makes a checkable prediction: if good blocks only need to nudge their input, then the learned residual functions $F$ should produce *small* outputs. **From the paper (§4.2, Fig. 7):** measuring the standard deviation (spread) of each 3×3 layer's outputs "after BN and before other nonlinearity (ReLU/addition)", "ResNets have generally smaller responses than their plain counterparts. These results support our basic motivation (Sec.3.1) that the residual functions might be generally closer to zero than the non-residual functions." Also, "the deeper ResNet has smaller magnitudes of responses … When there are more layers, an individual layer of ResNets tends to modify the signal less."

Notice the verbs: the results "support" a motivation that residuals "might" be close to zero. Fig. 7 is evidence *consistent with* the hypothesis — it does not show that small residuals are *why* training is easier.

### Beyond classification (§4.3, briefly)

**From the paper (§4.3, Table 8):** using the same object-detection system (Faster R-CNN) and swapping VGG-16 for ResNet-101 raises the COCO detection score mAP@[.5, .95] from 21.2 to 27.2 — "a 6.0% increase … which is a 28% relative improvement" ($6.0 / 21.2 \approx 0.28$). The paper attributes this "solely" to the learned representations, because "[t]he detection implementation … of using both models is the same". (mAP is a standard detection accuracy score; you don't need its definition for this lesson.)

## Part 8 — Where the claims stop

Evidence tells you what was shown; this part collects what was *not*. We separate the limits the authors themselves state from the ones we see, because confusing the two would put words in the authors' mouths.

<!-- la:limitations -->
### Limitations stated by the authors

1. **The core idea is a hypothesis.** "We hypothesize that it is easier to optimize the residual mapping" (§1). The experiments are consistent with it; the paper never claims to prove it.
2. **An open question underneath.** §3.1 starts from the hypothesis that "multiple nonlinear layers can asymptotically approximate complicated functions"; footnote 2: "This hypothesis, however, is still an open question."
3. **The cause of degradation is unknown.** "We conjecture that the deep plain nets may have exponentially low convergence rates … The reason for such optimization difficulties will be studied in the future." (§4.1)
4. **Too deep stops helping.** The 1202-layer CIFAR-10 ResNet ($n = 200$) trains fine — training error "<0.1%" — but its test error, **7.93%** (Table 6), is worse than the 110-layer net's **6.43%** "although both have similar training error". The authors: "there are still open problems on such aggressively deep models … We argue that this is because of overfitting. The 1202-layer network may be unnecessarily large (19.4M) for this small dataset." They used no dropout or maxout (standard regularizers): "combining with stronger regularization may improve results, which we will study in the future." (§4.2)
5. **Generality is expected, not shown.** "we expect that it is applicable in other vision and non-vision problems" (§1). Every experiment in the paper is on images.
6. **Not every block shape helps.** A single-layer $F$ showed no advantage (§3.2).

### Limitations we identify (our reading, not the paper's)

1. **Mostly single training runs.** Only ResNet-110 reports repeated runs (std 0.16 points on CIFAR-10). On ImageNet, differences like A vs B (0.51 points) or B vs C (0.33) come with no reported run-to-run spread, so they should be read as "small", which is how the paper itself treats them.
2. **Fig. 7 is consistent with, not proof of, the mechanism.** Smaller residual responses are what the hypothesis predicts, but other explanations could produce them too; the paper does not run an experiment that isolates *why* residual nets optimize better.
3. **The very deep ImageNet comparisons change more than depth.** ResNet-50/101/152 differ from ResNet-34 in depth *and* block design (bottleneck) *and* shortcut option (B). Footnote 4 says plain bottleneck nets also degrade, but gives no numbers.
4. **Comparisons with other methods are not controlled.** Tables 3–5 and the detection results compare whole systems that differ in architecture, depth, and computation. They show ResNets are strong; on their own they don't show which ingredient is responsible — that job is done by Table 2, Table 3's A/B/C rows, and Fig. 6.

<!-- la:optional -->
<details>
<summary>Optional: a gradient-based reading you will meet elsewhere (our interpretation, not this paper's argument)</summary>

<!-- la:interpretation -->
For a single number, if $y = F(x) + x$ then $\frac{dy}{dx} = \frac{dF}{dx} + 1$: the shortcut contributes a "+1" to the slope, so even if $\frac{dF}{dx}$ is small, the signal from the loss has a direct path back through every block. Many later explanations of ResNets lean on this picture. Be careful attributing it to *this* paper: here the authors argue that their plain networks did **not** suffer from vanishing gradients (BN, "healthy norms", §4.1), and they frame the benefit as easier optimization via preconditioning (§3.1). Keep the two stories apart, and label the gradient one as interpretation when you use it.

</details>

## Practice

These exercises check the outcomes, with less support than the guided ones. Try each fully before opening the hints and solutions at the end; the hints narrow the problem without giving the method away.

<!-- la:exercise id=E3 outcomes=3 level=independent -->
**Exercise 3 — the shortcut at conv3_1.** In ResNet-34, the first block of conv3_x takes a 56×56×64 input. Its first conv is 3×3 with 128 filters and stride 2; its second is 3×3 with 128 filters.
(a) How many weights do the block's two conv layers have in total?
(b) Under option A, how many weights does this block's shortcut add?
(c) Under option B, the shortcut is a 1×1 conv from 64 to 128 channels with stride 2. How many weights does it add, and what fraction is that of the block's conv weights from (a)?
(d) For the *second* block of conv3_x (28×28×128 in and out), which of options A, B, C give it a projection shortcut, and why?

<!-- la:exercise id=E4 outcomes=3 level=transfer -->
**Exercise 4 — does a projection really double the bottleneck?** Take the bottleneck block of Fig. 5 (right): 256-channel input and output on a 56×56 grid; layers 1×1 (256→64), 3×3 (64→64), 1×1 (64→256).
(a) Count its conv weights, and compare with the ordinary 64-channel block of Fig. 5 (left), which you counted in Part 5. Does the paper's "similar time complexity" hold?
(b) Replace the identity shortcut with a 1×1 projection from 256 to 256 channels. By what factor do the weights grow? Does this agree with §4.1's "doubled"?
(c) In the ordinary 64-channel block, a 1×1 projection shortcut (64→64) would add what fraction? Explain the difference using the phrase "the two high-dimensional ends".

<!-- la:exercise id=E5 outcomes=1 level=transfer -->
**Exercise 5 — a different failure at 1202 layers.** On CIFAR-10, ResNet-110 (1.7M parameters) and ResNet-1202 (19.4M parameters) reach "similar training error" (the 1202-layer net's is below 0.1%), but test errors of 6.43% and 7.93% (Table 6). Is the 1202-layer network suffering from degradation? From what, according to the authors — and how certain are they? Name one experiment that could test their explanation.

<!-- la:exercise id=E6 outcomes=4 level=independent -->
**Exercise 6 — which evidence supports which claim?** For each claim, name the table rows (or figure) that bear on it, say whether that comparison is controlled, and say whether it supports the claim.
(a) "Adding identity shortcuts — and nothing else — lowers the error of a 34-layer network."
(b) "With shortcuts, a deeper network can be more accurate than a shallower one."
(c) "ResNet-152 beats VGG-16 because of residual learning."
(d) "Projection shortcuts are essential for fixing degradation."

<!-- la:exercise id=E7 outcomes=5 level=check -->
**Exercise 7 — sort the statements.** Label each as **R** (a result the paper reports, with its location), **A** (the authors' argument, hypothesis, conjecture, or expectation — say which), or **N** (not claimed by the paper).
1. The 34-layer plain net has higher training error than the 18-layer plain net throughout training.
2. Deep plain nets may have exponentially low convergence rates.
3. It is easier to optimize a residual mapping than the original mapping.
4. ResNets work because the shortcuts fix the vanishing-gradient problem.
5. Residual learning will also work for non-vision problems.
6. The 1202-layer ResNet tests worse than the 110-layer one because it overfits.

## Putting it together: why deeper failed, and why residuals fixed it

<!-- la:synthesis -->
We started by asking why simply making a network deeper made it worse — even on its own training data — and how rewriting each few layers as "input plus a learned correction" changes that.

The pieces now fit together. **The failure is in training, not in capacity.** The deeper plain network has *higher training error* (Fig. 1, Fig. 4 left), which rules out overfitting; the paper argues it is also unlikely to be vanishing gradients, since BN keeps forward signals and backward gradients healthy (§4.1). And by the construction argument (§1), the deeper network *could* match the shallower one by setting its extra layers to the identity. So SGD is failing to find a solution that exists — and the authors suspect (§3.1, "suggests … might") that identity-like mappings are exactly what a stack of nonlinear layers finds hard to learn.

**The fix moves the identity to the easiest place.** A residual block computes $y = F(x, \{W_i\}) + x$ (Eqn. 1). With all weights at zero it is already the identity — as you computed by hand — whereas a plain block at zero outputs nothing. The layers now learn only the departure from "pass it through", which the authors *hypothesize* is easier to optimize (§1) and which, if good blocks need only small departures, acts as a preconditioner (§3.1). Identity shortcuts cost nothing, and where shapes change a cheap projection (Eqn. 2) or zero-padding fills the gap; keeping shortcuts as identities matters most in bottleneck blocks, where a projection would roughly double the cost.

**The running example, in its final form.** Plain: 18 layers 27.94%, 34 layers 28.54% — deeper is worse. Residual, with *not one extra parameter*: 27.88% and 25.03% — deeper is better by 2.85 points, with "considerably lower training error" (Table 2, Fig. 4). The same reversal appears on CIFAR-10 (Fig. 6), the residual responses are small as the hypothesis predicts (Fig. 7), and depth keeps paying off up to 152 layers on ImageNet (Tables 3–5).

**And where it stops.** Why residual learning is easier remains a hypothesis; the cause of degradation is a conjecture; at 1202 layers the benefit runs out, which the authors argue is overfitting; and generality beyond vision is expected, not shown.

You can now explain the degradation problem and separate it from overfitting and vanishing gradients; compute a residual block and say why zero weights mean identity; decide when a shortcut needs a projection and what it costs; judge which table comparison supports which claim; and tell the paper's results from its hypotheses. This lesson did not cover the training recipe (§3.4) in depth, the detection and localization systems (§4.3, appendices), or any later work on residual networks.

**Next step: read the paper itself.** A good first pass, using your map from Part 1: the Abstract → Fig. 1 → §1 → §3.1–3.2 with Fig. 2 → §4.1 up to and including Table 3 and Fig. 4 → §4.2 with Fig. 6 and Fig. 7. Skip §2, §3.4 and the appendices on the first read. As you go, mark each sentence on the certainty ladder.

<!-- la:solutions -->
## Hints and solutions

<!-- la:hint id=E1 -->
**Hint for Exercise 1.** Overfitting is about a *gap*. Which pair has a deeper net that fits its training data *better* than the shallow net?

<!-- la:solution id=E1 -->
**Solution to Exercise 1.**
*Pair 1:* (a) the shallower net (6% < 9%); (b) the shallower net (10% < 13%); (c) the deeper net is worse *on its training data*, so it is not overfitting — overfitting would show lower training error. This is **degradation**, the pattern of Fig. 1.
*Pair 2:* (a) the deeper net (1% < 6%); (b) the shallower net (10% < 14%); (c) the deeper net fits training data better but does worse on new images: the signature of **overfitting**.
*Common wrong answer:* calling both pairs overfitting because in both the deeper net has higher test error. Test error alone cannot tell the two apart; you need training error too.

<!-- la:hint id=E2 -->
**Hint for Exercise 2.** In step (b), one entry of $W_1 x$ is negative — what does ReLU do to it? For (g), look at the worked example's "set every weight to zero" paragraph: which single matrix, if zero, makes $F(x)$ zero?

<!-- la:solution id=E2 -->
**Solution to Exercise 2.**
(a) $W_1 x = (1\cdot 1 + 0\cdot 3,\; 0\cdot 1 + (-1)\cdot 3) = (1, -3)$.
(b) $\sigma(W_1 x) = (1, 0)$ — ReLU replaces $-3$ by 0.
(c) $F(x) = W_2\,(1, 0) = (0.5, 0)$.
(d) $y = F(x) + x = (1.5, 3)$.
(e) $\sigma(y) = (1.5, 3)$: the input $(1, 3)$ with its first entry nudged up.
(f) Plain block: $\sigma(F(x)) = \sigma((0.5, 0)) = (0.5, 0)$ — the second input entry, 3, is lost entirely.
(g) Set $W_2 = 0$ (or $W_1 = 0$). Then $F(x) = 0$, $y = x$, and $\sigma(x) = x$ because $x$ is non-negative.
*Common wrong answer:* skipping the ReLU between the layers, i.e. computing $W_2 W_1 x = (0.5, -1.5)$ and then $y = (1.5, 1.5)$. The nonlinearity between the layers is part of $F$.

<!-- la:hint id=E3 -->
**Hint 1 for Exercise 3.** Before counting anything, write down the shape (grid × channels) going into and coming out of each conv. The cost of a conv depends only on its filter size and its channel counts.

**Hint 2.** Use $k\cdot k\cdot C_{in}\cdot C_{out}$ for each conv; the first conv's $C_{in}$ is the *input's* channel count. For (d), the decision is whether the second block's input and output shapes match — and which option projects even when they do.

<!-- la:solution id=E3 -->
**Solution to Exercise 3.**
(a) First conv: $3\cdot 3\cdot 64\cdot 128 = 73{,}728$. Second: $3\cdot 3\cdot 128\cdot 128 = 147{,}456$. Total $221{,}184$.
(b) Zero. Option A keeps an identity shortcut, sampling every other position (stride 2) and padding the 64 missing channels with zeros.
(c) $1\cdot 1\cdot 64\cdot 128 = 8{,}192$ weights, about $8{,}192 / 221{,}184 \approx 3.7\%$ of the block's conv weights — cheap.
(d) Only option C. Its input and output are both 28×28×128, so an identity works; A and B use identities wherever shapes match, and only C makes *every* shortcut a projection.
*Common wrong answer:* using 128 as $C_{in}$ for the first conv (giving 147,456 twice). The first conv still reads the 64-channel output of conv2_x.

<!-- la:hint id=E4 -->
**Hint 1 for Exercise 4.** Both blocks run on a 56×56 grid, so comparing their weight counts also compares their multiply-adds (Part 5). Count each of the bottleneck's three layers separately, watching which channel counts each one connects.

**Hint 2.** A 1×1 conv from $a$ to $b$ channels has $a\cdot b$ weights. For (c), the deciding question is which channel count the shortcut connects in each block, compared with the width the block's own layers mostly work at.

<!-- la:solution id=E4 -->
**Solution to Exercise 4.**
(a) Bottleneck: $256\cdot 64 + 3\cdot 3\cdot 64\cdot 64 + 64\cdot 256 = 16{,}384 + 36{,}864 + 16{,}384 = 69{,}632$. Ordinary block: $2\cdot 3\cdot 3\cdot 64\cdot 64 = 73{,}728$. On the same grid, multiply-adds scale the same way, so the two are indeed similar (the bottleneck is about 6% cheaper) — consistent with "similar time complexity" (§4.1).
(b) Projection: $256\cdot 256 = 65{,}536$. New total $69{,}632 + 65{,}536 = 135{,}168$, a factor of about $1.94$ — "doubled", as §4.1 says, to within rounding.
(c) A 64→64 projection is $4{,}096$ weights, about $5.6\%$ of $73{,}728$. The difference: the bottleneck's shortcut connects the 256-channel input to the 256-channel output — "the two high-dimensional ends" — so its cost grows with $256^2$, while the block's own layers mostly work at 64 channels. In the ordinary block, the shortcut and the layers work at the same width, so the shortcut is relatively cheap. This is why §4.1 says identity shortcuts are "particularly important" for bottleneck designs.
*Common wrong answer:* counting the 3×3 layer as $3\cdot 3\cdot 256\cdot 64$ (using the block's outer width), which gives $180{,}224$ and makes the bottleneck look far costlier than the ordinary block. The 3×3 layer sits between the two 1×1 layers, so it connects 64 channels to 64.
*What changed from Exercise 3:* the block shape. The same projection idea that cost 3.7% there costs about 94% here; whether a projection is affordable depends on where in the block the shortcut sits.

<!-- la:hint id=E5 -->
**Hint 1 for Exercise 5.** Before naming a cause, compare the two networks' *training* errors. Which of the two patterns from Part 2 — degradation or overfitting — does that match?

**Hint 2.** Now find the verb the authors use for their explanation in §4.2 and place it on the certainty ladder (Part 1). For the experiment: if their explanation were right, what change to the 1202-layer net's training should lower its test error?

<!-- la:solution id=E5 -->
**Solution to Exercise 5.** Not degradation: degradation means the deeper net has *higher training error*, but here training errors are similar (and very low). Similar training error with worse test error is the overfitting signature. The authors' explanation is overfitting, but at the "argue" level of the certainty ladder: "We argue that this is because of overfitting. The 1202-layer network may be unnecessarily large (19.4M) for this small dataset" (§4.2) — a reasoned explanation, not a tested one. Experiments that could test it: retrain the 1202-layer net with stronger regularization such as dropout or maxout (the authors note these are used for the best results on CIFAR-10 and that "combining with stronger regularization may improve results", §4.2) and see whether its test error falls to or below 6.43%; or repeat both trainings several times to confirm the 1.5-point gap exceeds run-to-run spread (ResNet-110's std is 0.16, but only one 1202-layer result is reported).
*Common wrong answer:* "degradation, because the deeper net is worse." Degradation is defined by *training* error going up with depth; here training errors are similar, so a worse test error points elsewhere.

<!-- la:hint id=E6 -->
**Hint 1 for Exercise 6.** For each claim, ask: in the rows I'm comparing, what else differs besides the thing the claim is about?

**Hint 2.** Then decide whether the claim is about a *difference* ("A beats B") or a *cause* ("because of X"). A cause needs rows that differ only in X.

<!-- la:solution id=E6 -->
**Solution to Exercise 6.**
(a) Table 2, 34-layer row (plain 28.54 vs ResNet 25.03), or Table 3 plain-34 vs ResNet-34 A (top-5 10.02 vs 7.76); Fig. 4. **Controlled**: option A adds no parameters, and depth, width and computation are the same. **Supports** the claim.
(b) Table 2 ResNet column (18 layers 27.88 → 34 layers 25.03); also Table 6 on CIFAR-10 (ResNet-20 8.75 → ResNet-110 6.43) and Table 3 (ResNet-34 → 50 → 101 → 152). 18 vs 34 differ only in depth (same design, same shortcut option); 34 vs 50/101/152 also change the block (bottleneck) and option (B). **Supports** the claim; the 18-vs-34 and CIFAR comparisons are the cleanest.
(c) Table 3: VGG-16 28.07 vs ResNet-152 21.43 top-1. **Not controlled**: depth, block design and computation (15.3 vs 11.3 billion FLOPs) all differ. It supports "ResNet-152 is more accurate than VGG-16", not "*because of* residual learning". The causal part needs a plain-vs-residual comparison like (a).
(d) Table 3 A/B/C: 25.03 / 24.52 / 24.19, against plain-34 at 28.54. Controlled among themselves (only the shortcut type differs). **Does not support** the claim — it contradicts it: option A, with no projections at all, already gets most of the improvement; the paper concludes projections "are not essential" (§4.1).
*Common wrong answer for (c):* "yes, Table 3 shows it". A bigger number gap is not a controlled comparison.

<!-- la:solution id=E7 -->
**Solution to Exercise 7.**
1. **R** — Fig. 4 (left), described in §4.1.
2. **A, conjecture** — "We conjecture that the deep plain nets may have exponentially low convergence rates" (§4.1).
3. **A, hypothesis** — "We hypothesize that it is easier to optimize the residual mapping…" (§1). Results such as Table 2, Fig. 6 and Fig. 7 are consistent with it but do not prove it.
4. **N** — the paper argues the opposite for its plain nets: degradation is "unlikely to be caused by vanishing gradients" (§4.1). (A gradient-path story exists elsewhere; see the optional box in Part 8, labelled as interpretation.)
5. **A, expectation** — "we expect that it is applicable in other vision and non-vision problems" (§1); untested in this paper.
6. **R + A** — the numbers are reported (Table 6: 7.93% vs 6.43%); the "because it overfits" is the authors' argument ("We argue that this is because of overfitting", §4.2).
*Common wrong answer:* marking 3 as R because the paper is "about" it. Being the paper's central idea does not make it a measured result.

<!-- la:sources -->
## Sources

- K. He, X. Zhang, S. Ren, J. Sun. *Deep Residual Learning for Image Recognition*. arXiv:1512.03385v1 [cs.CV], 10 December 2015. https://arxiv.org/abs/1512.03385 — the only source used. All quotes, section/figure/table/equation references and numbers in this lesson come from version 1 of this paper.
- Works cited inside the paper (e.g. [16] batch normalization, [21] 10-crop testing, [41] VGG) were **not** read for this lesson; they are mentioned only as "the paper cites…".
- Background definitions (top-1/top-5 error, overfitting, ReLU, convolution weight counts) are standard textbook material stated from this lesson's author's background knowledge, not taken from a specific source.
