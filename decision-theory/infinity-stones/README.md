# Who gets the Infinity Stones?

## A sharp robustness bound for repeated risky disarmament

**Research note · 5 September 2026 · Silly Goose Research Labs**

[Interactive explanation](website/index.html) · [Complete proof](proof.md) ·
[Verification](verify.py) · [Results](results/verification.json) ·
[Research log and novelty audit](research-log.md) · [Citation](CITATION.cff)

**Scenario credit:** [CYBRDELIC (@cybrdelic), 31 August 2026](https://x.com/cybrdelic/status/2094237445240102951).
Their thought experiment asks whether factory-made Infinity Stones should be
destroyed, widely distributed, or retained by an elite, when destruction
requires concentrating them in one person's hands. Their
[follow-up request to see the work](https://x.com/cybrdelic/status/2095691559035457557)
prompted this note. This credits the originating idea; it does not imply that
CYBRDELIC coauthored, reviewed, or endorses our formal model. Thanos is a
mnemonic for the temporary custodian, not a claim about Marvel canon.

## The finding in ordinary language

Suppose handing over the stones has a chance of catastrophe. A successful
handover destroys today's stones, but the factories may eventually bring them
back, requiring another risky handover. How reliable does the custodian need
to be?

**Knowing only the average time until the stones return is not enough.** With
any positive exponential discount rate, no positive handover-failure
probability can be certified as preferable to continued distributed ownership
for *every* return-time distribution with that average. Frequent early
comebacks, balanced by rare very long pauses, defeat any such guarantee.

This is a worst-case information limit. It does **not** mean disarmament is
always worse. Once we know the earliest and latest possible comeback, we obtain
a **sharp, attainable interval** for the acceptable handover risk. A guaranteed
minimum pause also gives a positive bound even without a maximum pause.

## A concrete reversal

These are illustrative inputs, not estimates of weapons or AI risk:

- distributed ownership has catastrophe hazard `lambda = 0.02` per year;
- each handover independently fails with probability `q = 0.15`;
- the objective is expected safe years weighted by `exp(-0.03 t)`;
- the mean return time is 20 years in every row.

| How the factories return | Maximum acceptable q | Weighted safe years after handing over | Compare with keeping the stones: 20.00 |
|---|---:|---:|---|
| Always after 20 years | 23.12% | 23.96 | Handover is better |
| Exponential return time, mean 20 | 20.00% | 22.67 | Handover is better |
| 90% after 1 year; 10% after 191 years | 7.76% | 13.90 | Keeping is better |

The mean, handover risk, baseline hazard, and objective are identical. Only the
distribution of return times changes. Because we value the timing of safe
years, a rare distant reprieve does not compensate equally for frequent early
exposure to another handover.

## Model and exact result

Let `lambda > 0` be the catastrophe hazard while the stones remain distributed,
`beta > 0` the exponential discount rate, and `q in [0,1]` the independent
catastrophe probability of each instantaneous handover. After a successful
handover, there is no catastrophe risk until production returns after an iid
positive time `R` with finite mean `mu`. At each return, the same choice is
available again. The return times, handover failures, and armed-state
catastrophe clock are independent. There is no new information, technical
progress, other payoff, or strategic choice of production timing.

For `L = E[exp(-beta R)]`, define

\[
Q(L)=\frac{\lambda(1-L)}{\beta+\lambda(1-L)}.
\]

Repeated immediate handover gives at least as many expected discounted safe
years as keeping the stones forever **if and only if** `q <= Q(L)`.
For this known, stationary model, delaying or randomizing handovers cannot
improve on the better of those two policies. The full derivation and its
precise information assumptions are in [proof.md](proof.md).

If `0 < a < mu < b`, `a <= R <= b`, and `E[R]=mu`, then the exact threshold interval is

\[
Q(L_{\max})\leq Q(L)\leq Q(e^{-\beta\mu}),\qquad
L_{\max}=\frac{b-\mu}{b-a}e^{-\beta a}
          +\frac{\mu-a}{b-a}e^{-\beta b}.
\]

If the mean equals either bound, the only possible pause is constant.
For the strict interior case, the worst case puts all mass at the two endpoints; the best case is a fixed
pause of `mu`. Both are admissible, and mixtures attain every intermediate
threshold. Below the lower endpoint, handover is weakly better for every
admissible distribution. Above the upper endpoint, it is strictly worse for
every distribution. Strictly between them, knowing the mean and limits still
leaves opposite decisions possible.

With a known floor `R >= a > 0` but no ceiling and `mu > a`, the sharp infimum
is `Q(exp(-beta a))`. With only a positive mean and no uniform positive floor,
the infimum is zero. The mean-only result needs access to both arbitrarily
short pauses and arbitrarily long compensating tails.

## A second result: patience and uncertainty do not commute

If the entire distribution is fixed and we take `beta` to zero, the threshold
converges to `lambda mu / (1 + lambda mu)`. That is also the threshold for
undiscounted expected survival, which depends only on the mean return time.

But at **every positive** discount rate, the worst threshold over *all*
positive return-time distributions with that mean is zero. Consequently,

\[
\lim_{\beta\downarrow0}\inf_{E[R]=\mu}Q_\beta(R)=0
\quad\ne\quad
\inf_{E[R]=\mu}\lim_{\beta\downarrow0}Q_\beta(R)
=\frac{\lambda\mu}{1+\lambda\mu}.
\]

This is a nonuniform limit, not a discontinuity for any single fixed return
law. Allowing the worst-case distribution to change as patience increases is
what produces the difference. A common finite upper bound removes this gap.

## What is—and is not—new here

The proposed contribution is the **disarmament-specific decision frontier,
sharp information bounds, and patience/ambiguity separation in this explicit
recurring-production model**, together with a reproducible counterexample to
mean-only reasoning. These are proved conditional statements, not simulation
conjectures. The model and combination were developed for this note; global
priority has **not** been established and the note has not had conventional
external peer review.

Renewal equations, geometric sums, Jensen's inequality, convex order, and the
endpoint bound are established mathematics. The sharp bounded-support step is
an application of the classical Edmundson–Madansky bound, **not a new
probability inequality**. The broader disarmament commitment problem is also
old. See the [source-by-source novelty audit](research-log.md#related-work-and-novelty).

## Boundaries that change the answer

- **Fresh risk each time:** `q` is an independent failure risk per handover.
  It is not a once-and-for-all hidden personality trait of the same immortal
  custodian. With a permanently safe custodian with probability `1-q`, and a
  permanently unsafe one otherwise, the threshold instead becomes
  `lambda / (beta + lambda)`, independent of return times.
- **No measured parameters:** the numbers illustrate logic, not real-world
  forecasts. `lambda` is a hazard, not exactly an annual probability; the
  one-year event probability is `1-exp(-lambda)`.
- **One objective:** discounted safe time does not encode liberty, inequality,
  prosperity, voluntary consent, or heterogeneous risk preferences. Failure
  treats death and permanent domination as the same absorbing bad state.
- **A narrower question:** we compare a distributed baseline with repeated
  stock destruction. We do not derive a three-way game-theoretic equilibrium
  or rank elite rule; neither elite incentives nor shield engineering are
  modeled. A universal three-way answer would require those additional inputs.
- **Perfect blocking:** if it really removes *all* catastrophe risk so that
  `lambda=0`, a positive-risk handover cannot improve this safety-only
  objective. Perfect defense is not mutually assured destruction.
- **The factories survive:** permanent verified elimination of production is
  outside the finite-return model. It gives the separate one-handover threshold
  `lambda / (beta + lambda)`.
- **Timing is known statistically:** actors know the return law; observing
  past pauses does not teach them an unknown parameter. Learning, improving
  institutions, costly waiting, correlated episodes, and state-dependent
  hazards may create worthwhile delays. Our no-delay statement excludes them.
- **More variance alone is insufficient:** the monotonic theorem concerns a
  mean-preserving spread (convex order), not every pair ranked by variance.

## Reproduce

Python 3, standard library only:

```bash
python3 decision-theory/infinity-stones/verify.py
python3 decision-theory/infinity-stones/verify.py --output /tmp/infinity-stones.json
node decision-theory/infinity-stones/verify-web.cjs
```

The checker compares closed-form values with a time-domain probability-flow
calculation and a certified tail bound, verifies threshold algebra with exact
rational arithmetic, searches bounded-support distributions, checks endpoint
attainment and the mean-preserving construction, and writes deterministic
browser fixtures. Computation supports the implementation; the all-distribution
claims are established by the written proofs.

Serve `website/` as a static root. It has no runtime API, external model,
dependency, database, or external font requirement. Its declared public slug is
`infinity-stones`; declaring it does not deploy it.
