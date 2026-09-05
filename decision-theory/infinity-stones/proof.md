# Proofs: the recurring-production disarmament model

See [README.md](README.md) for the scenario credit, interpretation, related
work, and claim limits. All propositions below refer only to this model.

## 1. Probability space and objective

While armed, catastrophe has constant hazard `lambda > 0`. The alive state has
unit flow reward. A handover is instantaneous and fails with probability
`q in [0,1]`; failure is absorbing with reward zero. On success, a catastrophe-free
pause lasts `R > 0` almost surely, where `E[R]=mu` is positive and finite. Then
the system returns to the same armed state. Every pause is an independent draw
from the known law of `R`. All handover trials and armed-state exponential
clocks are independent of each other and of the pauses.

For `beta > 0`, the objective is

\[
U=E\left[\int_0^T e^{-\beta t}\,dt\right],
\]

where `T` is the time to the absorbing catastrophe and `T=infinity` is allowed.
This is expected discounted safe time, bounded by `1/beta`. It is not the
unweighted probability of eventual catastrophe. There are no decision-relevant
observations during an armed waiting period; known past iid outcomes convey
no information about future episodes. Policies are nonanticipating and cannot
condition on unobserved future trials.

Write `L=E[e^(-beta R)]`; then `0<L<1`. Positive iid pauses with positive finite
mean cannot accumulate infinitely many episodes in finite time almost surely.

## 2. Exact policy values and threshold

**Proposition 1.** Keeping forever has value

\[
K=\frac1{\beta+\lambda}.
\]

Repeated immediate handover has value

\[
A=\frac{(1-q)(1-L)}{\beta[1-(1-q)L]}.
\]

Moreover `A >= K` if and only if

\[
q\leq Q_\beta(R)=\frac{\lambda(1-L)}{\beta+\lambda(1-L)}.
\]

*Proof.* Keeping has survival probability `exp(-lambda t)`, giving the integral
for `K`. Conditional on a successful handover, the first pause has expected
reward `(1-L)/beta`, followed by continuation value discounted by `L`.
Thus `A=(1-q)[(1-L)/beta+LA]`. The coefficient `(1-q)L` is strictly less than
one, giving the unique expression above, including `q=0` and `q=1`.
The denominator of `A-K` is positive and its numerator is

\[
\lambda(1-L)-q[\beta+\lambda(1-L)].
\]

This proves the equivalence. Equality means indifference. □

For an exponential return time with rate `rho`, `L=rho/(beta+rho)`, and

\[
Q_\beta=\frac{\lambda}{\beta+\lambda+\rho}.
\]

## 3. Waiting and randomization cannot improve the stationary choice

**Proposition 2.** Among the admissible policies described in Section 1, the
optimal value is `max(K,A)`. A policy achieving it either keeps forever or
hands over immediately at every return. At the threshold both are optimal.

*Proof.* Let `V` be a candidate continuation value when the system returns
armed, and set `J(V)=(1-q)[(1-L)/beta+LV]`. If the next handover occurs after
`t` safe armed years, its value is

\[
K+e^{-(\beta+\lambda)t}[J(V)-K].
\]

The factor runs from one at `t=0` to zero at `t=infinity`, so the supremum over
waiting times is `max(K,J(V))`. Random waiting averages these quantities and
cannot improve the supremum. With no incoming information, independent
randomization exhausts the additional choices during an armed wait. After a
return the process regenerates; past history cannot improve a known iid law.

The Bellman operator `B(V)=max(K,J(V))` has contraction factor `(1-q)L<1`.
Its unique fixed point is `max(K,A)`: if `A>=K`, `J(A)=A`; if `A<=K`,
`J(K)-K=[1-(1-q)L](A-K)<=0`. The corresponding stationary policy attains the
fixed point. □

This is a fully observed stationary decision problem, not a proof that waiting
cannot help when trust is learned, technology improves, or preferences change.

## 4. Return-time variability and sharp bounds

Define `Q(l)=lambda(1-l)/[beta+lambda(1-l)]`. Direct differentiation gives

\[
Q'(l)=-\frac{\lambda\beta}{[\beta+\lambda(1-l)]^2}<0.
\]

**Proposition 3 (convex-order comparison).** If `R1 <=cx R2` (every integrable
convex function has no larger expectation under `R1`), then
`Q_beta(R1)>=Q_beta(R2)`. In particular, a deterministic pause of length `mu`
maximizes the threshold among all laws of mean `mu`.

*Proof.* The function `r -> exp(-beta r)` is strictly convex. Convex order
gives `L1<=L2`; decreasing `Q` reverses the inequality. Jensen gives
`exp(-beta mu)<=L`, with equality exactly for a constant pause. □

**Theorem 4 (sharp bounded-support identification).** Suppose
`0<a<mu<b<infinity`. Over every law with `a<=R<=b` and mean `mu`, the set of
possible thresholds is exactly the closed interval

\[
\left[Q(L_{\max}),\ Q(e^{-\beta\mu})\right],\qquad
L_{\max}=\frac{b-\mu}{b-a}e^{-\beta a}
          +\frac{\mu-a}{b-a}e^{-\beta b}.
\]

*Proof.* The convex graph lies below the chord through its endpoints:

\[
e^{-\beta r}\leq\frac{b-r}{b-a}e^{-\beta a}
                   +\frac{r-a}{b-a}e^{-\beta b}.
\]

Taking expectations gives `L<=Lmax`. This is the one-dimensional classical
Edmundson–Madansky bound. Jensen supplies the other endpoint. The law assigning
probabilities `(b-mu)/(b-a)` and `(mu-a)/(b-a)` to `a` and `b` attains `Lmax`;
the constant law attains `exp(-beta mu)`. Mixing those two laws preserves both
mean and support and interpolates `L` continuously between its endpoints.
Since `Q` is continuous and strictly decreasing, every displayed threshold is
attained. □

If `mu=a`, `mu=b`, or `a=b=mu`, the only possible law is constant and the
interval collapses to a point. Equality at either threshold is weak preference,
not strict dominance. For `q` strictly between the two endpoints, two
admissible laws yield strict opposite preferences.

**Corollary 5 (a guaranteed minimum pause).** If `R>=a>0` and `E[R]=mu>a`
but no finite upper bound is imposed, the sharp infimum is
`Q(exp(-beta a))`, which is positive.

*Proof.* Since `R>=a`, `L<=exp(-beta a)`. Put probability `1-epsilon` at `a`
and `epsilon` at `a+(mu-a)/epsilon`. This has mean `mu` and its transform tends
to `exp(-beta a)`. Thus the bound is approached, although for `mu>a` it is not
attained. If `mu=a`, the law is constant and the same value is attained. □

## 5. Mean-only information provides no positive robust threshold

**Theorem 6.** Fix `lambda,beta,mu>0`. Then

\[
\inf_{R>0\ {\rm a.s.},\ E[R]=\mu}Q_\beta(R)=0.
\]

Consequently, for every `q>0`, some positive, finite-support return law with
that mean makes repeated handover strictly worse than keeping forever.

*Proof.* For `0<epsilon<1`, put mass `1-epsilon` at
`a_epsilon=epsilon mu`, and mass `epsilon` at

\[
b_\epsilon=\frac{\mu-(1-\epsilon)\epsilon\mu}{\epsilon}.
\]

Both points are positive and the mean is exactly `mu`. The transform is

\[
L_\epsilon=(1-\epsilon)e^{-\beta\epsilon\mu}
             +\epsilon e^{-\beta b_\epsilon}\longrightarrow1.
\]

Hence `Q(Lepsilon)->0`. Every individual threshold is positive because
`R>0` almost surely, so zero is an infimum, not an attained threshold.
Given `q>0`, choose epsilon with `Q(Lepsilon)<q`, then use Proposition 1. □

The unknown-law adversary is allowed to choose a different law for each
`beta` or proposed `q`; it does not change the law across episodes within a
single model. This distinction is essential. A uniformly positive lower bound
on pauses prevents the construction, as Corollary 5 shows.

## 6. Patience versus distributional ambiguity

**Theorem 7.** For each fixed positive return law with finite mean `mu`,

\[
\lim_{\beta\downarrow0}Q_\beta(R)
=\frac{\lambda\mu}{1+\lambda\mu}.
\]

The two orders of limiting and taking the mean-only infimum disagree:

\[
\lim_{\beta\downarrow0}\inf_{E[R]=\mu}Q_\beta(R)=0,
\qquad
\inf_{E[R]=\mu}\lim_{\beta\downarrow0}Q_\beta(R)
=\frac{\lambda\mu}{1+\lambda\mu}>0.
\]

*Proof.* We have
`(1-L)/beta = E[(1-exp(-beta R))/beta] -> E[R]=mu` by dominated convergence:
the integrand tends to `R` and is between zero and `R`. Substitution into
`Q=lambda[(1-L)/beta]/[1+lambda[(1-L)/beta]]` proves the pointwise limit.
Theorem 6 proves the first displayed infimum is zero at every positive beta.
The other order takes the common pointwise limit before the infimum. □

At `beta=0`, for `q>0`, the expected number of successful pauses before a
failed handover is `(1-q)/q`. Independence gives mean survival
`(1-q)mu/q`; keeping gives `1/lambda`. Their exact threshold is therefore
`lambda mu/(1+lambda mu)`, agreeing with the limit. If `q=0`, repeated handover
has infinite mean survival. These are safe-time comparisons, not comparisons
of eventual catastrophe probability, which is one under either policy when
`lambda,q>0` and returns recur forever.

If all admissible laws additionally satisfy `R<=b` for one common finite `b`,
the convergence is uniform, since

\[
0\leq\mu-\frac{1-L}{\beta}
\leq\frac{\beta E[R^2]}2\leq\frac{\beta b\mu}2.
\]

Thus the gap disappears with a common ceiling. The mean-only result exploits
a family of tails without uniform integrability, not a paradox in a fixed
model or a claim that a tiny discount rate always changes the decision.

## 7. A different custodian assumption changes the theorem

Suppose one permanent custodian is perfectly safe with probability `1-q` and
fails the first handover otherwise. Once the first handover succeeds, all
future handovers succeed with certainty. Then `A_persistent=(1-q)/beta`, so

\[
A_{\rm persistent}\geq K
\quad\Longleftrightarrow\quad q\leq\frac{\lambda}{\beta+\lambda}.
\]

The entire return-time law disappears. This countermodel prevents reading the
independent-episode theorem as a universal statement about a single person's
trustworthiness. Permanent removal of production gives the same policy value
because it eliminates later handovers altogether.

## 8. Mathematical provenance

The proofs use standard renewal/discounting arguments and classical convex
bounds. We claim neither those methods nor the underlying disarmament
commitment problem as new. Our proposed contribution is their explicit
recurring-disarmament specialization, its sharp information requirements,
and the noncommuting patience/ambiguity limits. See
[research-log.md](research-log.md#related-work-and-novelty) for sources and the
limits of the novelty search.
