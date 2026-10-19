# Residual networks

<!-- la:orientation -->
Why very deep networks were hard to train, and how residual connections helped.

<!-- la:outcomes -->
By the end you will be able to:

1. Describe the degradation problem.
2. Write the residual block equation.

<!-- la:misconception -->
> A tempting mistake: thinking degradation is overfitting. Training error rises too, so it is not.

<!-- la:worked-example -->
## A residual block by hand

With F(x) = 0 the block outputs x, so it can represent the identity easily.

<!-- la:exercise id=E1 outcomes=1 level=guided -->
**Try it.** Explain why training error rising rules out overfitting.

<!-- la:exercise id=E2 outcomes=2 level=independent -->
**Exercise 2.** Write y in terms of x and F.

<!-- la:synthesis -->
## Putting it together

Residual blocks make the identity easy, which eases optimisation of deep nets.

<!-- la:solutions -->
## Solutions

<!-- la:solution id=E1 -->
Overfitting lowers training error while raising test error.

<!-- la:solution id=E2 -->
y = F(x) + x.
