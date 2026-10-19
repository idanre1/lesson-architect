# Solving Two-Step Equations: Undoing What Was Done to $x$

<!-- la:orientation -->
This lesson teaches you to find an unknown number in an equation such as $3x + 5 = 20$ — not by guessing, but by a short method you can explain step by step and check yourself.

Here is the kind of problem it solves. You ordered some notebooks at 3 dollars each, and there was a 5-dollar delivery fee on top. The total came to 20 dollars. How many notebooks did you order? You can probably work this out in your head. Algebra writes the same situation as $3x + 5 = 20$, and the point of this lesson is to see *why* the head-method works, so that it keeps working when the numbers are not friendly and you cannot just "see" the answer.

**Who this is for:** adults who are comfortable with everyday arithmetic — adding, subtracting, multiplying, dividing, and simple decimals like 2.5. No algebra is assumed: every symbol and word is explained when it first appears. Negative numbers are not needed anywhere.

<!-- la:outcomes -->
By the end of this lesson you will be able to:

1. Check whether a number is a solution of an equation by substituting it in and comparing the two sides.
2. Describe the "recipe" an equation applies to $x$, in order, and list the steps that undo it in reverse order — including when brackets change the order.
3. Solve equations like $3x + 5 = 20$ and $2x - 9 = 7$ by doing the same undo step to both sides, giving a reason for each step, and checking your answer.
4. Turn a short word problem into an equation like these, solve it, and check the answer against the story.
5. Adapt the method to an equation whose steps come in a different order, such as $5(x - 2) = 35$, and explain why the first step changes.

If some words or symbols in that list mean nothing to you yet, that is expected: each one is explained before you need it.

**The route:** first we learn to *read* $3x + 5 = 20$ and to *check* a possible answer. Then we see the equation as a recipe that was applied to an unknown number, and find the number by running the recipe backwards. Next we learn the one rule that makes this legal on paper — do the same thing to both sides — and put everything together on the notebook problem. Finally we handle subtraction, word problems, and a changed recipe, and practice.

## What $3x + 5 = 20$ is actually saying

Before we can solve anything, we need to be able to read the sentence and to recognise a correct answer when we have one. That is what this section gives you.

**The letter.** In the notebook story, the number of notebooks is unknown. Rather than writing "the number of notebooks" over and over, algebra uses a letter to stand for it. The letter $x$ is traditional, but any letter works. A number we do not know yet, written as a letter, is called an **unknown** (you will also hear *variable*). The letter is a stand-in for a *number*, not an abbreviation for a thing: $x$ means "how many notebooks", not "notebooks".

**Writing $3x$.** "3 times the unknown" could be written $3 \times x$, but the multiplication sign looks too much like the letter $x$. So algebra simply writes the number against the letter: $3x$ means $3 \times x$. You will also sometimes see a raised dot, $3 \cdot x$, meaning the same thing.

<!-- la:misconception -->
> **A tempting mistake: reading $3x$ as digits.** If $x$ is 5, it is natural to read $3x$ as "35", the way 3 next to 5 makes thirty-five in ordinary numbers. But in algebra, a number written against a letter always means *multiply*: when $x = 5$, $3x = 3 \times 5 = 15$. The digits rule only applies to two digits written together, like 35; it never applies to a number next to a letter.

**The equals sign.** $3x + 5 = 20$ is a complete sentence: "3 times the unknown, plus 5, *is the same number as* 20." A statement that two amounts are equal is called an **equation**. The part to the left of $=$ is the **left side**, the part to the right is the **right side**. The equals sign does not mean "and the answer is"; it means *both sides are the same amount*. That reading becomes important in a moment.

So, in story terms: (price per notebook × number of notebooks) + delivery fee = total. That is exactly $3x + 5 = 20$.

**What counts as an answer.** A number that makes the equation a *true* statement when you put it in place of the letter is called a **solution**. Putting a number in place of the letter is called **substituting** it.

<!-- la:worked-example -->
### Testing guesses on the notebook problem

Let's test some guesses for $3x + 5 = 20$. For each one, the goal is the same: work out the left side with that number in place of $x$, and see whether it equals the right side, 20.

- **Guess $x = 4$.** Left side: $3 \times 4 + 5 = 12 + 5 = 17$. Is $17 = 20$? No. So 4 is not a solution — and 17 is too small, so we need a bigger number.
- **Guess $x = 6$.** Left side: $3 \times 6 + 5 = 18 + 5 = 23$. Is $23 = 20$? No — too big now.
- **Guess $x = 5$.** Left side: $3 \times 5 + 5 = 15 + 5 = 20$. Is $20 = 20$? Yes. So $x = 5$ is the solution: you ordered 5 notebooks.

Notice the order we used for the left side: multiply first ($3 \times 5$), *then* add 5. That is arithmetic's standard agreement: multiplication and division are done *before* addition and subtraction (you may remember this as PEMDAS or BODMAS). So $3 \times 5 + 5$ is $15 + 5 = 20$, and not $3 \times 10 = 30$. The next section turns this order into the key to solving.

This substitution check is worth keeping forever, even once you have a better method: it is how you *prove* an answer is right. But guessing as a way of *finding* answers has two problems. It can take many tries, and if the answer is not a whole number — for $2x + 1 = 8$ the answer turns out to be 3.5 — you could guess whole numbers all day and never land on it. We need a method that goes straight to the answer.

<!-- la:exercise id=E1 outcomes=1 level=check -->
**Quick check (Exercise 1).**

(a) Is $x = 4$ a solution of $2x + 7 = 15$?

(b) Is $x = 3$ a solution of $5x - 4 = 10$?

(c) Sam says that when $x = 2$, $4x$ equals 42. What is $4x$ really, and what did Sam do?

## The recipe hidden inside the equation

We can now read the equation and check an answer. What is still missing is a way to *find* the answer directly. The key idea: the left side, $3x + 5$, is a set of instructions that was carried out on the unknown number. If we know the instructions and the final result, we can run them backwards.

**Reading the instructions in order.** You just saw that multiplication is done before addition. So the left side of $3x + 5 = 20$ is a two-step **recipe** applied to the unknown:

1. Start with the unknown number $x$.
2. Multiply it by 3.
3. Add 5.
4. The result is 20.

You can picture it as a machine: $x \to [\times 3] \to [+5] \to 20$.

**Undoing the recipe.** Each operation has an opposite that cancels it out:

- adding 5 is undone by subtracting 5 (and subtracting is undone by adding);
- multiplying by 3 is undone by dividing by 3 (and dividing is undone by multiplying).

An operation that undoes another is called its **inverse operation**.

> **Before reading on:** to get back from 20 to $x$, which step do you undo first — the "multiply by 3" or the "add 5"?

The *last* thing done to $x$ was "add 5", so that is the first thing to undo. Think of getting dressed: you put on socks, then shoes; to undress you take off the shoes first, then the socks. Undoing happens in **reverse order**.

So we run the machine backwards: $20 \to [-5] \to 15 \to [\div 3] \to 5$.

- Undo "add 5": $20 - 5 = 15$. This 15 is what $3x$ must have been.
- Undo "multiply by 3": $15 \div 3 = 5$. This is $x$.

We get $x = 5$ — the same answer the guessing found, but with no guessing.

**Where the socks-and-shoes picture stops.** It tells you the *order* of undoing, and nothing else. It does not tell you which operation undoes which (that is the inverse-operation list above), and it only works because $x$ appears *once* in the equation, so there is a single chain of steps to unwind. If $x$ appeared on both sides — say $3x + 5 = x + 9$ — there would be no single chain to reverse. That case is beyond this lesson (there is an optional peek near the end).

**Brackets change the recipe.** Brackets (also called parentheses) mean "do this part first" — they override the multiply-before-add agreement. A number written right against a bracket means multiply, just as with a letter, so the expression $3(x + 5)$ means $3 \times (x + 5)$: first add 5 to $x$, *then* multiply the result by 3. Its recipe is $x \to [+5] \to [\times 3]$, so it is undone in the reverse order: divide by 3 first, then subtract 5. Same ingredients as $3x + 5$, opposite order — and so the opposite undo order. The rule never changes: **find the order the steps were done, then undo them last-first.**

<!-- la:exercise id=E2 outcomes=2 level=guided -->
**Try it (Exercise 2).** For each equation, fill in the recipe and the undo steps, then run the undo steps on the right-hand number to find $x$.

(a) $4x + 1 = 29$. Recipe: $x \to [\,?\,] \to [\,?\,] \to 29$. Undo, last step first: $29 \to [\,?\,] \to\ ?\ \to [\,?\,] \to x$.

(b) $6x - 2 = 40$. Recipe: $x \to [\,?\,] \to [\,?\,] \to 40$. Undo, last step first: $40 \to [\,?\,] \to\ ?\ \to [\,?\,] \to x$.

(For (b), remember from the list above that subtracting is undone by adding.)

## Keeping both sides balanced

Running the recipe backwards in your head works for $3x + 5 = 20$. But it leaves no written trail, so when an answer is wrong you cannot see where it went wrong, and it gets shaky as problems grow. Algebra writes the same undo steps as a sequence of equations, each one true, each one simpler than the last. This section supplies the single rule that makes those steps allowed.

**The rule.** An equation says the two sides are the same amount. If you do *the same thing to both sides* — add the same number, subtract the same number, multiply by the same number, or divide by the same number (anything except zero) — they are still the same amount. So the new equation is still true, and it has the same solution.

That is all "solving" is: applying the undo steps from the recipe, each one to *both* sides at once.

**A picture: a balance scale.** Imagine the left side and the right side as two pans of a perfectly balanced scale. Taking 5 off the left pan alone would tip it; taking 5 off *both* pans keeps it level. Likewise, if you split each pan into 3 equal parts and keep one part from each, the pans still balance.

**Where the balance picture stops.** It is good for adding, subtracting, and splitting into equal parts, but it breaks down outside friendly cases: a real pan cannot hold a negative weight, so subtracting more than a pan holds has no physical meaning, even though the arithmetic rule still works. And dividing by zero is never allowed — it has no meaning at all — which no scale picture will warn you about. In this lesson you will only divide by numbers like 2, 3, 4, so that never arises. Trust the rule; use the scale only as a reminder of *why* "both sides" matters.

**One more word.** The pieces of a side that are joined by $+$ or $-$ are called **terms**. The left side of $3x + 5$ has two terms, $3x$ and $5$; the right side, $20$, has one. Anything inside brackets counts as a single piece: $3(x + 5)$ is one term, because the brackets glue $x + 5$ together. "Do the same thing to both sides" means do it to each side *as a whole* — and, when dividing, that means dividing *every* term on that side. That detail is exactly where the most common mistake happens, as you are about to see.

## Solving $3x + 5 = 20$ step by step

We now have both ingredients: the recipe tells us *which* undo step comes next, and the both-sides rule tells us *how* to apply it on paper. Here they are together on the notebook problem.

<!-- la:worked-example -->
### The notebook problem, written out

**Recognise the type.** The unknown appears once, and two things were done to it: multiplied by 3, then 5 added. That is a two-step recipe, so we undo two steps, last-first.

**Step 1 — undo the last operation (the $+5$).**

*Goal:* get $3x$ alone on the left.

*Move:* subtract 5 from both sides.

$$3x + 5 - 5 = 20 - 5$$

$$3x = 15$$

On the left, adding 5 and then subtracting 5 cancel each other out, leaving just $3x$; on the right, $20 - 5 = 15$.

*Why this move:* the $+5$ was the last thing done to $x$, so it is the first to undo; subtracting is the inverse of adding; and we do it to both sides so the equation stays true.

*Quick check:* "3 times the number is 15" — that matches the story: after the 5-dollar fee is removed, the notebooks themselves cost 15 dollars.

**Step 2 — undo the multiplication.**

*Goal:* get $x$ alone.

*Move:* divide both sides by 3. Algebra often writes division with a fraction bar: $\frac{15}{3}$ means $15 \div 3$.

$$\frac{3x}{3} = \frac{15}{3}$$

$$x = 5$$

On the left, "3 times a number, divided by 3" gives back the number, so $\frac{3x}{3}$ is just $x$; on the right, $15 \div 3 = 5$.

*Why this move:* "times 3" is undone by "divide by 3"; both sides again.

**Step 3 — check by substituting.** Put $x = 5$ into the *original* equation: $3 \times 5 + 5 = 15 + 5 = 20$. The left side equals the right side, so $x = 5$ is the solution. You ordered 5 notebooks.

> **Before reading on:** why subtract first, and not divide by 3 first?

Dividing first is not *illegal* — it is just messier. If you divide both sides by 3, you must divide *every* term on the left, the 5 as well: you get $x + 5 \div 3 = 20 \div 3$, that is $x + 1\tfrac{2}{3} = 6\tfrac{2}{3}$. Subtracting $1\tfrac{2}{3}$ from both sides still gives $x = 5$, but you had to work with fractions for no reason. Undoing in reverse order (subtract, then divide) keeps the numbers whole. That is why "last-done, first-undone" is the method of choice here.

<!-- la:misconception -->
> **A tempting mistake: dividing only part of a side.** A very common slip is to divide the $3x$ and the 20 by 3 but forget the 5: $x + 5 = 20 \div 3 = 6\tfrac{2}{3}$, which leads to $x = 6\tfrac{2}{3} - 5 = 1\tfrac{2}{3}$.
> Check it: $3 \times 1\tfrac{2}{3} + 5 = 5 + 5 = 10$ (three lots of $1\tfrac{2}{3}$ is $3 + 2 = 5$), not 20. Wrong.
> The repair: dividing a side means dividing *all* of it — every term. The cleanest way to avoid the problem is to follow the recipe order: get rid of the $+5$ first, so that by the time you divide, there is only one term left on that side.

<!-- la:misconception -->
> **A tempting mistake: "move it across and change the sign" — for everything.** Some people remember a shortcut: move a number to the other side and flip its sign. Applied to *both* numbers in $3x + 5 = 20$, it gives $x = 20 - 5 - 3 = 12$.
> Check it: $3 \times 12 + 5 = 36 + 5 = 41$, not 20. Wrong.
> The repair: the shortcut is only a summary of "do the inverse operation to both sides". The 5 is *added*, so its inverse is subtracting — the shortcut happens to work there. But the 3 is *multiplying* $x$, so its inverse is *dividing* by 3, not subtracting 3. If you always ask "what operation was done, and what undoes it?", you never need the shortcut.

<!-- la:exercise id=E3 outcomes=3 level=guided -->
**Try it (Exercise 3).** Solve $4x + 7 = 31$ by filling in the gaps, then check.

- Step 1: the last thing done to $x$ was [ ? ], so [ ? ] both sides: $4x =$ [ ? ].
- Step 2: $x$ was multiplied by [ ? ], so [ ? ] both sides: $x =$ [ ? ].
- Check: $4 \times$ [ ? ] $+\ 7 =$ [ ? ]. Does it equal 31?

## When the recipe subtracts

So far, the recipe always *added* a number. If it subtracts instead, nothing new is needed: the inverse of subtracting is adding, and everything else stays the same. One example makes this concrete.

<!-- la:worked-example -->
### Solving $2x - 9 = 7$

**Read the recipe:** $x \to [\times 2] \to [-9] \to 7$. Undo last-first: add 9, then divide by 2.

**Step 1 — undo the $-9$.** Add 9 to both sides:

$$2x - 9 + 9 = 7 + 9$$

$$2x = 16$$

*Why:* subtracting 9 is undone by adding 9; both sides, so the equation stays true. (Notice that the "change the sign" shortcut *does* agree here, because it is a plus/minus pair.)

**Step 2 — undo the $\times 2$.** Divide both sides by 2: $x = 16 \div 2 = 8$.

**Check:** $2 \times 8 - 9 = 16 - 9 = 7$. ✓

**Answers need not be whole numbers.** Earlier we said guessing would never find the answer to $2x + 1 = 8$. The method has no trouble: subtract 1 from both sides to get $2x = 7$, then divide both sides by 2 to get $x = 3.5$. Check: $2 \times 3.5 + 1 = 7 + 1 = 8$. ✓ The method does not care whether the answer is whole; it just follows the recipe backwards.

## From a story to an equation

The notebook problem started life as a story, and so do most real uses of this method. So far the equation has been handed to you; this section shows how to build it yourself, so that you can tackle a problem that arrives in words.

A dependable routine:

1. **Name the unknown.** Decide what number you are looking for and give it a letter. Choosing a letter that reminds you of it (like $h$ for hours) is fine.
2. **Write the recipe from the story.** What is multiplied by the unknown? What is added or subtracted once, regardless of the unknown?
3. **Set it equal to the total** given in the story.
4. **Solve** by undoing last-first on both sides.
5. **Check against the story,** not only the equation — this also catches mistakes in step 2.

<!-- la:worked-example -->
### The plumber's bill

*A plumber charges a 40-dollar call-out fee plus 25 dollars for every hour of work. Your bill was 115 dollars. How many hours did the plumber work?*

1. **Unknown:** the number of hours. Call it $h$.
2. **Recipe:** each hour costs 25, so the hours cost $25h$ (that is, $25 \times h$). The call-out fee of 40 is added once, however long the job takes. Cost: $25h + 40$.
3. **Equation:** $25h + 40 = 115$.
4. **Solve.** The recipe is $h \to [\times 25] \to [+40] \to 115$, so undo the $+40$ first: subtract 40 from both sides, $25h = 75$. Then undo the $\times 25$: divide both sides by 25, $h = 3$.
5. **Check against the story:** 3 hours at 25 dollars is 75 dollars, plus the 40-dollar call-out fee is 115 dollars. ✓ The plumber worked 3 hours.

The same routine is exactly where $3x + 5 = 20$ came from: $x$ = number of notebooks, each notebook adds 3 (so $3x$), the delivery fee adds 5 once, and the total is 20.

**Why it helps to spot the "once" amount.** In each story there is one amount that is charged per item (it gets multiplied by the unknown) and one that is charged once (it gets added or subtracted). Sorting the story's numbers into these two roles is most of the work.

## Practice: solving on your own

These exercises check every outcome without hand-holding. Try each one fully before looking at the hints and solutions at the end; use a hint first if you are stuck, and always finish by checking your answer by substitution.

<!-- la:exercise id=E4 outcomes=3 level=independent -->
**Exercise 4.** Solve each equation and check your answer.

(a) $7x - 3 = 39$

(b) $4x + 3 = 13$

<!-- la:exercise id=E5 outcomes=4 level=independent -->
**Exercise 5.** A cinema charges 12 dollars per ticket, plus a 4-dollar booking fee charged once per order. Your order cost 64 dollars. Write an equation for the number of tickets, solve it, and check your answer against the story.

<!-- la:exercise id=E6 outcomes=2,5 level=transfer -->
**Exercise 6.** Solve $5(x - 2) = 35$ and check your answer. Then explain, in a sentence, why the first step here is different from the first step for $5x - 2 = 35$.

<!-- la:exercise id=E7 outcomes=1,3 level=check -->
**Exercise 7.** Here is someone's solution:

> $4x + 6 = 30$, so moving the 6 and the 4 across: $x = 30 - 6 - 4 = 20$.

Without solving the equation first, show that 20 is wrong. Then find the mistake, and give the correct solution.

<!-- la:optional -->
<details>
<summary>Optional: a peek at what comes next — <i>x</i> on both sides</summary>

Nothing in this lesson's exercises needs this; it is here to show where the recipe picture runs out.

In $3x + 5 = x + 9$, the unknown appears on both sides, so there is no single chain of steps to unwind — the socks-and-shoes picture has nothing to say. But the both-sides rule still works. Subtract $x$ from both sides (you are allowed to subtract the unknown itself, because it is just a number we have not found yet): $3x - x + 5 = 9$, and since three lots of a number take away one lot leaves two lots, that is $2x + 5 = 9$. Now it is an ordinary two-step equation: subtract 5 to get $2x = 4$, divide by 2 to get $x = 2$. Check: left side $3 \times 2 + 5 = 11$, right side $2 + 9 = 11$. ✓

The lesson to take away: the *recipe* idea tells you the order for a single chain; the *both-sides* rule is the deeper idea that keeps working when the recipe picture does not.

</details>

## Putting it together: why the method works

<!-- la:synthesis -->
We started by asking how to find the unknown in $3x + 5 = 20$ reliably, without guessing, and how to be sure the answer is right. Here is the answer, built from the pieces of this lesson.

First, an equation is a statement that two amounts are equal, and the left side of $3x + 5 = 20$ is a *recipe* applied to an unknown number: multiply by 3, then add 5. Second, to recover the number you undo the recipe *in reverse order* using inverse operations — subtract 5, then divide by 3 — because the last thing done is the first thing to undo. Third, the both-sides rule makes each undo step legal on paper: doing the same operation to both sides of a true equation keeps it true, as long as you never divide by zero and you apply the operation to every term of a side. Finally, substitution closes the loop: putting the answer back into the original equation proves it is right.

On the notebook problem that gives: $3x + 5 = 20 \;\to\; 3x = 15 \;\to\; x = 5$, and the check $3 \times 5 + 5 = 20$. Five notebooks.

You can now read equations like these, check a proposed answer, solve two-step equations with $+$ or $-$, build one from a short story, and adapt when brackets change the order of the recipe. This lesson did not cover negative numbers, equations with fractions as the multiplier, or the unknown appearing on both sides (beyond the optional peek). A sensible next step is exactly that last one: equations like $3x + 5 = x + 9$, where the both-sides rule carries you further than the recipe picture can.

<!-- la:solutions -->
## Hints and solutions

<!-- la:solution id=E1 -->
**Solution to Exercise 1.**

(a) Substitute $x = 4$: $2 \times 4 + 7 = 8 + 7 = 15$. The left side equals the right side, so yes, 4 is a solution.

(b) Substitute $x = 3$: $5 \times 3 - 4 = 15 - 4 = 11$. Since $11 \ne 10$ ($\ne$ means "is not equal to"), no, 3 is not a solution. (A common slip is to forget the $-4$ and compare 15 with 10; always work out the whole left side — multiply first, then subtract — before comparing.)

(c) $4x$ means $4 \times x$, so when $x = 2$, $4x = 4 \times 2 = 8$. Sam wrote the 4 and the 2 side by side as digits, which is the "reading $3x$ as digits" mistake.

<!-- la:solution id=E2 -->
**Solution to Exercise 2.**

(a) Recipe: $x \to [\times 4] \to [+1] \to 29$. Undo last-first: $29 \to [-1] \to 28 \to [\div 4] \to 7$. So $x = 7$. (Check: $4 \times 7 + 1 = 29$.)

(b) Recipe: $x \to [\times 6] \to [-2] \to 40$. Undo last-first: $40 \to [+2] \to 42 \to [\div 6] \to 7$. So $x = 7$. (Check: $6 \times 7 - 2 = 40$.)

The most likely wrong move is undoing in reading order — dividing first. For (a), $29 \div 4 = 7.25$, then $7.25 - 1 = 6.25$; check: $4 \times 6.25 + 1 = 26$, not 29.

<!-- la:hint id=E3 -->
**Hint for Exercise 3.** Read the left side as a recipe: what happens to $x$ first, and what happens to it last?

<!-- la:solution id=E3 -->
**Solution to Exercise 3.**
- Step 1: the last thing done to $x$ was *adding 7*, so *subtract 7 from* both sides: $4x = 31 - 7 = 24$.
- Step 2: $x$ was multiplied by *4*, so *divide* both sides *by 4*: $x = 24 \div 4 = 6$.
- Check: $4 \times 6 + 7 = 24 + 7 = 31$. ✓

A likely wrong answer is $x = 20$, from "moving" the 4 across as $-4$: $31 - 7 - 4 = 20$. Its check, $4 \times 20 + 7 = 87$, shows it is wrong.

<!-- la:hint id=E4 -->
**Hint for Exercise 4.** In each, the unknown has been multiplied and then had something added or taken away. Which of those happened last? (Second hint: for (b), the answer is not a whole number — that is fine.)

<!-- la:solution id=E4 -->
**Solution to Exercise 4.**

(a) Recipe: $\times 7$, then $-3$. Undo the $-3$ by adding 3 to both sides: $7x = 42$. Undo the $\times 7$ by dividing both sides by 7: $x = 6$. Check: $7 \times 6 - 3 = 42 - 3 = 39$. ✓ (A likely wrong answer is $x = 36 \div 7$, from *subtracting* 3 instead of adding; it does not even come out whole, which is a warning sign — and its check fails.)

(b) Recipe: $\times 4$, then $+3$. Subtract 3 from both sides: $4x = 10$. Divide both sides by 4: $x = 10 \div 4 = 2.5$. Check: $4 \times 2.5 + 3 = 10 + 3 = 13$. ✓

<!-- la:hint id=E5 -->
**Hint for Exercise 5.** Sort the story's numbers: which amount is charged for every ticket, and which is charged only once? The first gets multiplied by the unknown.

<!-- la:solution id=E5 -->
**Solution to Exercise 5.**

Unknown: the number of tickets, $t$. Each ticket costs 12, so tickets cost $12t$; the booking fee 4 is added once. Equation: $12t + 4 = 64$.

Subtract 4 from both sides: $12t = 60$. Divide both sides by 12: $t = 5$.

Check against the story: 5 tickets at 12 dollars is 60 dollars, plus the 4-dollar fee is 64 dollars. ✓ You bought 5 tickets.

A likely wrong answer: treating the fee as per ticket, $(12 + 4)t = 64$, gives $t = 4$; but then the order would cost $4 \times 12 + 4 = 52$ dollars, not 64 — the story check catches it.

<!-- la:hint id=E6 -->
**Hint for Exercise 6.** Brackets mean "do this first". Write out the recipe for $5(x - 2)$ in the order the steps happen, then undo last-first.

<!-- la:solution id=E6 -->
**Solution to Exercise 6.**

Recipe: $x \to [-2] \to [\times 5] \to 35$. The *last* step was multiplying by 5, so undo it first: divide both sides by 5, giving $x - 2 = 7$. Then undo the $-2$ by adding 2 to both sides: $x = 9$.

Check: $5 \times (9 - 2) = 5 \times 7 = 35$. ✓

Why the first step differs: in $5x - 2$, $x$ is multiplied first and 2 is subtracted last, so you would add 2 first. In $5(x - 2)$, the brackets make the subtraction happen first and the multiplication last, so the multiplication is undone first.

A likely wrong answer comes from ignoring the brackets and treating it as $5x - 2 = 35$: add 2 to get $5x = 37$, so $x = 7.4$. Check in the real equation: $5 \times (7.4 - 2) = 5 \times 5.4 = 27$, not 35.

<!-- la:solution id=E7 -->
**Solution to Exercise 7.**

Showing 20 is wrong: substitute it, $4 \times 20 + 6 = 80 + 6 = 86$, which is not 30.

The mistake: moving the 6 across as $-6$ is fine (adding 6 is undone by subtracting 6), but the 4 is *multiplying* $x$, so it must be undone by *dividing* by 4, not by subtracting 4.

Correct solution: subtract 6 from both sides, $4x = 24$; divide both sides by 4, $x = 6$. Check: $4 \times 6 + 6 = 24 + 6 = 30$. ✓
