#!/usr/bin/env python3
"""Reproduce the note's numerical evidence using Python's standard library.

Written proofs establish universal claims. This program audits the algebra,
the counterexample, the bounds, and browser fixtures by independent routes.
No network, model, or secret is required. Output is deterministic.
"""

import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path
import random


def pause_reward(beta, law):
    """E[integral_0^R exp(-beta t) dt], with a stable beta=0 limit."""
    if beta == 0:
        return math.fsum(p * t for t, p in law)
    return math.fsum(p * (-math.expm1(-beta * t)) / beta for t, p in law)


def threshold(lam, beta, law):
    h = pause_reward(beta, law)
    return lam * h / (1 + lam * h)


def handover_value(beta, q, law):
    h = pause_reward(beta, law)
    denominator = q + (1 - q) * beta * h
    return (1 - q) * h / denominator if denominator else math.inf


def calendar_value(beta, q, law, horizon):
    """Independent probability flow in calendar time; integer positive delays.

    Propagate handover-event probability to actual return dates. Subtract
    failures at each date and integrate the surviving probability between
    dates. No Laplace transform or geometric-cycle formula is used here.
    Remaining reward is at most exp(-beta*horizon)/beta.
    """
    assert beta > 0 and all(int(t) == t and t > 0 for t, _ in law)
    events = [0.0] * (horizon + 1)
    events[0] = 1.0
    alive = 1.0
    pieces = []
    unit_integral = -math.expm1(-beta) / beta
    for day in range(horizon):
        attempts = events[day]
        alive -= attempts * q
        assert alive >= -1e-12
        for delay, probability in law:
            due = day + int(delay)
            if due <= horizon:
                events[due] += attempts * (1 - q) * probability
        pieces.append(max(0, alive) * math.exp(-beta * day) * unit_integral)
    return math.fsum(pieces), math.exp(-beta * horizon) / beta


def bounded_laws(a, mu, b):
    return [(mu, 1.0)], [(a, (b - mu) / (b - a)), (b, (mu - a) / (b - a))]


def mean_only_law(mu, epsilon):
    a = epsilon * mu
    b = (mu - (1 - epsilon) * a) / epsilon
    return [(a, 1 - epsilon), (b, epsilon)]


def run():
    rng = random.Random(20260905)
    counts = {}

    # Exact rational algebra: use h=lambda/beta and L as independent rationals.
    # Cross-multiplication avoids testing only a rewritten implementation.
    exact = 0
    for i in range(1, 21):
        h = F(i, 7)
        for k in range(21):
            ell = F(k, 21)
            cutoff = h * (1 - ell) / (1 + h * (1 - ell))
            for j in range(21):
                q = F(j, 20)
                w = (1 - q) * (1 - ell) / (1 - (1 - q) * ell)
                keep = 1 / (1 + h)
                assert (w >= keep) == (q <= cutoff)
                assert ((w - keep) * (1 + h) * (1 - (1 - q) * ell)
                        == h * (1 - ell) - q * (1 + h * (1 - ell)))
                exact += 1
    counts['exact_rational_threshold_cases'] = exact

    lam, beta, mu, q = .02, .03, 20, .15
    fixture_laws = {
        'reliable': [(20, 1.0)],
        'uneven': [(1, .9), (191, .1)],
    }
    fixtures = []
    for name, law in fixture_laws.items():
        analytical = handover_value(beta, q, law)
        numerical, tail = calendar_value(beta, q, law, 1500)
        assert numerical - 1e-10 <= analytical <= numerical + tail + 1e-10
        fixtures.append({'name': name, 'law': law, 'mean': math.fsum(t*p for t,p in law),
                         'threshold': threshold(lam,beta,law), 'handover_value': analytical,
                         'calendar_value': numerical, 'calendar_tail_bound': tail})
    assert fixtures[0]['threshold'] > q > fixtures[1]['threshold']
    assert fixtures[0]['handover_value'] > 1/(beta+lam) > fixtures[1]['handover_value']
    h_exp = 1/(beta + 1/mu)
    exponential = {'name':'exponential', 'mean':mu,
                   'threshold':lam/(beta+lam+1/mu),
                   'handover_value':(1-q)*h_exp/(q+(1-q)*beta*h_exp)}

    # Independent calendar-time checks cover q=0, q=1, multiple delays and rates.
    calendar_checks = 0
    maximum_calendar_error = 0.0
    for law in [[(1,1.0)],[(3,.4),(19,.6)],[(1,.2),(7,.3),(29,.5)],[(20,1.0)]]:
        for discount in [.02,.05,.1]:
            for failure in [0,.01,.15,.7,1]:
                analytical = handover_value(discount,failure,law)
                numerical, tail = calendar_value(discount,failure,law,math.ceil(35/discount))
                err = abs(analytical-numerical)
                maximum_calendar_error = max(maximum_calendar_error,err)
                assert numerical-1e-10 <= analytical <= numerical+tail+1e-10
                calendar_checks += 1
    counts['calendar_probability_flow_cases'] = calendar_checks + len(fixtures)

    # Bounded-support checks and mean-preserving spreads; not just variance.
    bound_cases = 0
    for _ in range(1000):
        a = rng.uniform(.1,5)
        b = a+rng.uniform(1,100)
        points = [rng.uniform(a,b) for _ in range(5)]
        weights = [rng.random() for _ in points]
        total = sum(weights)
        law = list(zip(points,[w/total for w in weights]))
        mean = math.fsum(t*p for t,p in law)
        det, ends = bounded_laws(a,mean,b)
        rate = rng.uniform(.001,.2)
        discount = rng.uniform(.001,.2)
        lower, middle, upper = [threshold(rate,discount,x) for x in [ends,law,det]]
        assert lower-1e-12 <= middle <= upper+1e-12
        # Spread each atom to its endpoints, preserving each conditional mean.
        spread = []
        for t,p in law:
            d=min(t-a,b-t)/2
            spread.extend([(t-d,p/2),(t+d,p/2)])
        assert threshold(rate,discount,spread) <= middle+1e-12
        for mix in [0,.25,.5,.75,1]:
            blended = [(t,p*mix) for t,p in det]+[(t,p*(1-mix)) for t,p in ends]
            value = threshold(rate,discount,blended)
            assert lower-1e-12 <= value <= upper+1e-12
        bound_cases += 1
    counts['bounded_support_and_convex_order_cases'] = bound_cases

    # Mean-only witness: every distribution remains positive and finite support.
    witnesses=[]
    for eps in [.1,.01,.001,.0001,.00001,.000001]:
        law=mean_only_law(mu,eps)
        assert all(t>0 for t,_ in law)
        assert math.isclose(math.fsum(t*p for t,p in law),mu,rel_tol=1e-13)
        witnesses.append({'epsilon':eps,'law':law,'threshold':threshold(lam,beta,law)})
    assert all(x['threshold']>y['threshold'] for x,y in zip(witnesses,witnesses[1:]))
    assert witnesses[-1]['threshold'] < 2e-6
    counts['positive_mean_only_witnesses']=len(witnesses)

    # Fixed-law patience limit and the exact undiscounted formula.
    undiscounted=lam*mu/(1+lam*mu)
    limit_checks=[]
    for name,law in fixture_laws.items():
        assert math.isclose(threshold(lam,0,law),undiscounted,rel_tol=1e-14)
        assert math.isclose(handover_value(0,q,law),(1-q)*mu/q,rel_tol=1e-14)
        values=[threshold(lam,d,law) for d in [.03,.003,.00003,.00000003]]
        assert all(x<y for x,y in zip(values,values[1:]))
        assert abs(values[-1]-undiscounted)<1e-6
        limit_checks.append({'name':name,'thresholds':values})

    # Fixed-point value iteration allows keeping or handing over at each return.
    # Add independent deterministic and randomized waiting actions.
    policy_checks=0
    for law in fixture_laws.values():
        h=pause_reward(beta,law)
        ell=1-beta*h
        for failure in [.01,.15,.3,.8,1]:
            keep=1/(beta+lam)
            expected=max(keep,handover_value(beta,failure,law))
            v=0.0
            for _ in range(2000):
                j=(1-failure)*(h+ell*v)
                choices=[keep]+[keep+math.exp(-(beta+lam)*t)*(j-keep) for t in [0,1,5,20,100]]
                v_new=max(choices)
                if abs(v_new-v)<1e-13:break
                v=v_new
            assert math.isclose(v_new,expected,abs_tol=1e-10)
            policy_checks+=1
    counts['bellman_policy_cases']=policy_checks

    # A known positive floor has a positive infimum, not the mean-only zero.
    floor=1
    floor_limit=threshold(lam,beta,[(floor,1)])
    floor_values=[]
    for eps in [.1,.01,.001,.000001]:
        law=[(floor,1-eps),(floor+(mu-floor)/eps,eps)]
        value=threshold(lam,beta,law)
        assert value>floor_limit
        floor_values.append(value)
    assert abs(floor_values[-1]-floor_limit)<1e-6

    return {'schema_version':1,'status':'pass','seed':20260905,
            'evidence_scope':'Numerical and exact-algebra implementation checks; written proofs establish universal claims.',
            'counts':counts,'parameters':{'lambda':lam,'beta':beta,'mu':mu,'q':q},
            'keep_value':1/(beta+lam),'fixtures':fixtures,'exponential_fixture':exponential,
            'maximum_calendar_error':maximum_calendar_error,'mean_only_witnesses':witnesses,
            'undiscounted_threshold':undiscounted,'fixed_law_patience_checks':limit_checks,
            'positive_floor_threshold_infimum':floor_limit,
            'persistent_custodian_threshold':lam/(beta+lam)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=run()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'counts':result['counts'],
                      'maximum_calendar_error':result['maximum_calendar_error']},indent=2))
