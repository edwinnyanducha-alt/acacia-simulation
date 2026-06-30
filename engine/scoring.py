"""Scoring engine for Acacia Strategic Simulation."""

from typing import Dict, List, Any


def calculate_scores(decisions: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculate all 4 scoring dimensions from a group's decisions.
    
    decisions dict keys (Round 1):
        nda: int (55/60/65)
        green_space: int (10/20/30/40)
        monetisation: str (monetisation archetype name)
        infra: str (infrastructure approach)
        nbo: int (0/1/2 for each round)
        gov: int
        fin: int
    
    Round 2:
        debt_pct: int (0-100)
        partner_type: str
        dev_quality: str
    
    Round 3:
        shock_type: int (0-3)
        pivot: int (0=fight, 1=negotiate, 2=pivot)
    
    Round 4:
        offer: int (0=sell, 1=jv, 2=hold, 3=counter)
        dispute: int (0=vote, 1=mediate, 2=buyout, 3=court)
        constitution: int (0=no, 1=yes)
    """
    scores = {}
    
    # â”€â”€ REPUTATION (25%) â”€â”€
    rep = 50  # base
    
    # Green space bonus
    if decisions.get('green_space', 20) >= 35:
        rep += 20
    elif decisions.get('green_space', 20) > 25:
        rep += 10
    elif decisions.get('green_space', 20) < 20:
        rep -= 15
    
    # NDA bonus
    if decisions.get('nda', 60) == 55:
        rep += 10
    
    # NBO relationships
    nbo_rounds = sum([
        1 if decisions.get(f'nbo_r{i}', 0) == 2 else 0
        for i in range(1, 5)
    ])
    rep += nbo_rounds * 10
    
    # Lawsuit: if NBO ignored for 3+ rounds
    nbo_ignored = sum([
        1 if decisions.get(f'nbo_r{i}', 0) == 0 else 0
        for i in range(1, 5)
    ])
    if nbo_ignored >= 3:
        rep -= 25
    
    # Constitution
    if decisions.get('constitution', 0) == 1:
        rep += 15
    
    scores['reputation'] = rep
    
    # â”€â”€ IRR (30%) â”€â”€
    irr = 50  # base
    
    # Ground lease impact (from monetisation archetype)
    lease_share = { # approx lease % per archetype
        "Steward": 70, "Balanced": 40, "Developer": 20, "Speculator": 10,
    }.get(decisions.get('monetisation', 'Balanced'), 30)
    
    if lease_share >= 50:
        irr += 15
    elif lease_share > 30:
        irr += 5
    else:
        irr -= 5
    
    # Debt adjustment
    debt = decisions.get('debt_pct', 30)
    if debt <= 30:
        irr += 10
    elif debt >= 70:
        irr -= 10
    
    # NDA
    nda = decisions.get('nda', 60)
    if nda >= 65:
        irr += 10
    elif nda >= 60:
        irr += 5
    
    # FIN relationships
    fin_rounds = sum([
        1 if decisions.get(f'fin_r{i}', 0) == 2 else 0
        for i in range(1, 5)
    ])
    irr += fin_rounds * 5
    
    # Shock response
    pivot = decisions.get('pivot', 1)
    if pivot == 2:  # pivoted
        irr += 15
    elif pivot == 0:  # fought
        irr -= 15
    
    scores['irr'] = irr
    
    # â”€â”€ CASH VELOCITY (20%) â”€â”€
    vel = 50  # base
    
    # Sale % (from monetisation archetype)
    sale_share = {
        "Steward": 10, "Balanced": 30, "Developer": 60, "Speculator": 70,
    }.get(decisions.get('monetisation', 'Balanced'), 30)
    
    if sale_share >= 50:
        vel += 20
    elif sale_share > 30:
        vel += 10
    elif lease_share >= 50:
        vel -= 15  # too much lease = slow cash
    
    # External partner
    partner = decisions.get('partner_type', 'None')
    if partner in ('Minority', 'Majority', 'JV'):
        vel += 15
    
    # Infrastructure
    infra = decisions.get('infra', 'Phased')
    if infra == 'Just-in-time':
        vel += 10
    elif infra == 'Full upfront':
        vel -= 20
    
    # Debt speed
    if debt >= 70:
        vel += 15
    elif debt > 40:
        vel += 5
    elif debt <= 30:
        vel -= 5
    
    scores['velocity'] = vel
    
    # â”€â”€ RESILIENCE (25%) â”€â”€
    res = 50  # base
    
    # Shock survival
    if pivot == 2:
        res += 20
    elif pivot == 0:
        res -= 15
    
    # Dispute resolution
    dispute = decisions.get('dispute', 1)
    if dispute == 1:  # mediation
        res += 15
    elif dispute == 3:  # court
        res -= 15
    elif dispute == 2:  # buyout
        res += 10
    
    # Debt safety
    if debt == 0:
        res += 10
    elif debt >= 70:
        res -= 15
    
    # Constitution
    if decisions.get('constitution', 0) == 1:
        res += 15
    
    # Developer quality
    dev = decisions.get('dev_quality', 'Mid-tier')
    if dev == 'Premium':
        res += 10
    elif dev == 'Lowest bid':
        res -= 15
    
    scores['resilience'] = res
    
    # â”€â”€ WEIGHTED TOTAL â”€â”€
    scores['weighted_total'] = (
        scores['reputation'] * 0.25 +
        scores['irr'] * 0.30 +
        scores['velocity'] * 0.20 +
        scores['resilience'] * 0.25
    )
    
    # Clamp to reasonable range
    for k in scores:
        scores[k] = round(scores[k], 1)
    
    return scores
