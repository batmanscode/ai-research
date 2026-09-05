# Research log

## 5 September 2026 — question and narrowing

Read the public [original scenario by CYBRDELIC](https://x.com/cybrdelic/status/2094237445240102951),
the [request to see any resulting work](https://x.com/cybrdelic/status/2095691559035457557),
and both visible branches. The [future-generations reply](https://x.com/thegoypride/status/2095517199322517879)
raises the cost of leaving the danger in place indefinitely. These are sources
of the question, not evidence for a mathematical result.

Initially considered a theorem about an unaccountable final custodian
defecting. Rejected it as the central contribution: with monopoly benefits
assumed to exceed destruction benefits, backward induction essentially restates
the assumption, and credible-commitment literature already covers the mechanism.

Also rejected a direct three-way ranking. Shield efficacy, coalition attacks,
elite incentives, welfare weights, and irreversible factory destruction are
unspecified. Supplying favorable assumptions could manufacture any answer.

The productive narrowing was **recurring production**: if destroying stock
does not destroy the ability to reproduce it, concentration risk is encountered
again. The mean time until recurrence is a tempting but insufficient summary.

## Derivation and attempted failure modes

1. Solved the exponential-return case first. It yields
   `q <= lambda/(beta+lambda+rho)`, but the Markov assumption conceals the
   distributional question.
2. Replaced exponential return with an arbitrary iid positive finite-mean
   pause. A renewal equation reduces the full law to its Laplace transform at
   the chosen discount rate.
3. Compared a fixed 20-year pause with 90% one-year / 10% 191-year pauses.
   Both have mean 20, but at the stated inputs the handover recommendation
   reverses. This is a mathematical counterexample to mean-only decision
   sufficiency, not a fitted real-world example.
4. Applied Jensen and the classical endpoint bound to get the entire sharp
   threshold interval under a mean and support constraint. Recognized this
   mathematical tool as Edmundson–Madansky; credited it explicitly.
5. Built a positive two-point law approaching a zero robust threshold with a
   fixed mean. Checked the construction does not require literal zero-length
   episodes or infinite-mean tails.
6. Checked the undiscounted limit. For any fixed law it depends only on the
   mean; taking the worst law first retains zero. This exposes the lack of
   uniformity in the family, rather than a paradox for a fixed world.
7. Checked a common positive minimum pause and common maximum pause. A floor
   restores a positive guarantee. A ceiling restores uniform patience limits.
8. Checked a permanent hidden custodian type. The recurrence penalty disappears
   entirely: this assumption is a countermodel to overbroad claims.
9. Audited waiting with the regenerative Bellman equation. No-learning,
   stationary waiting is dominated by immediate handover or keeping forever.
   This is not extended to Bayesian learning or improving institutions.

## Related work and novelty

Focused search checked primary publisher/author materials, arXiv records, and
Emergent Mind paper searches. Search phrases included disarmament with
commitment, temporary monopoly, rearmament, optimal stopping, renewal process,
Laplace transform, and convex order. Emergent Mind produced some relevant
verification/network papers but many unrelated keyword matches; lack of a
match is not evidence of novelty. This was not an exhaustive literature review.

| Source | What it already supplies | What this note does differently |
|---|---|---|
| [CYBRDELIC, original post, 31 Aug 2026](https://x.com/cybrdelic/status/2094237445240102951) | The stones/factories/concentrated-destruction thought experiment. | Supplies an explicit narrower stochastic model and proofs; credits the scenario. |
| [Jervis (1978), *Cooperation under the Security Dilemma*](https://www.cambridge.org/core/journals/world-politics/article/cooperation-under-the-security-dilemma/C8907431CCEFEFE762BFCA32F091C526) | Offense–defense distinctions and security competition. | Does not infer perfect blocking from deterrence; treats baseline hazard as an input. |
| [Bueno de Mesquita & Riker (1982), selective nuclear proliferation](https://journals.sagepub.com/doi/10.1177/0022002782026002005) | A proliferation/deterrence model conditional on retaliation assumptions. | Does not claim that diffusion universally prevents catastrophe. |
| [Walter (1997), *The Critical Barrier to Civil War Settlement*](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/S0020818397440110) | Vulnerability during disarmament, including gradual implementation and guarantors (pp. 338–340). | Does not claim the trust bottleneck as new; studies distributional information about recurring exposure. |
| [Powell (2006), *War as a Commitment Problem*](https://www.cambridge.org/core/journals/international-organization/article/abs/war-as-a-commitment-problem/65DFFF1CD73A16F7ED4EEF6D4F934608) | Formal commitment problems under shifts in bargaining power. | No strategic equilibrium or endogenous commitment mechanism is claimed here. |
| [Caro-Burnett, Galiani & Torrens (2023; revised 2026), *The Elusive Quest for Disarmed Peace*](https://www.nber.org/papers/w31343) | A dynamic contest model with investment, settlements, and elimination opportunities. | Our focus is a regenerative safety comparison, not a new explanation of arms races. Publisher abstract/model description checked; no complete proof audit of this paper is claimed. |
| [1946 Acheson–Lilienthal/Baruch proposals, primary State Department record](https://history.state.gov/historicaldocuments/frus1946v01/d434) | International control of dangerous production activities; context for stock versus capability. | No claim that centralized disarmament or production control was first conceived in the tweet. |
| [Gallager, MIT *Discrete Stochastic Processes*, Chapter 4](https://ocw.mit.edu/courses/6-262-discrete-stochastic-processes-spring-2011/931ffa0940899c27f34b71ad64fd2bb0_MIT6_262S11_chap04.pdf) | Renewal equations and Laplace-transform methods, particularly Section 4.6.1. | The recurrence algebra is standard; the model-specific interpretation and bounds are the proposed contribution. |
| [Boyd & Vandenberghe, *Convex Optimization*, Section 3.1.8](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf) | Jensen's inequality and convexity. | The direction of variability is an application, not a new inequality. |
| [Madansky (1959), *Bounds on the Expectation of a Convex Function of a Multivariate Random Variable*](https://www.jstor.org/stable/2237413); [Ben-Tal & Hochman (1972)](https://www.cambridge.org/core/journals/journal-of-applied-probability/article/more-bounds-on-the-expectation-of-a-convex-function-of-a-random-variable/198DE610197C1E94644B4FB4A058E5B8) | Classical upper/lower convex expectation bounds, including the endpoint chord bound. | Explicitly reused to identify the exact range of admissible handover thresholds. |

**Novelty status:** an original research note with proved results within its
stated model and a candidate application/synthesis contribution. No matching
disarmament-specific mean-only robustness result was found in this focused
pass, but this does not establish priority across probability, reliability,
operations research, or political economy. It would be incorrect to market
the renewal identity, Jensen's inequality, endpoint bound, or commitment
problem as discoveries. No conventional external peer review has occurred.

## Verification record

`verify.py` uses exact rational cross-multiplication for the threshold sign,
an independent calendar-time probability-flow computation with an explicit
discount-tail bound for policy values, finite distributions for convex-order
and endpoint checks, constructive mean-only witnesses, and Bellman value
iteration including delayed actions. `results/verification.json` contains the
deterministic counts, numerical examples, and maximum numerical discrepancy.
The browser's separate JavaScript implementation is checked against those
fixtures by `verify-web.cjs`.

Computer checks audit formulas and implementations. The written universal
proofs do not depend on sampled distributions or a finite search. Visual QA
and source-control status are recorded in the repository's playtest log.
