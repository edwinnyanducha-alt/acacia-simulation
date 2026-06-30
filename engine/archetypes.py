"""Archetype definitions for Acacia Strategic Simulation."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Archetype:
    name: str
    colour: str
    hex_colour: str
    description: str
    win_condition: str
    secret_text: str
    default_bias: str
    
    # Default decisions that characterise the archetype
    default_nda: int = 55  # acres
    default_green: int = 40  # %
    default_monetisation: str = "Steward"  # 70/20/10 lease/jv/sale
    default_infra: str = "Just-in-time"
    default_debt: int = 0  # %
    default_partner: str = "None"
    default_dev: str = "Premium"
    default_nbo: int = 2  # 0=ignore, 1=admin, 2=strategic
    default_gov: int = 2
    default_fin: int = 1
    
    # Scoring weights
    starting_rep: int = 50
    starting_irr: int = 50
    starting_vel: int = 50
    starting_res: int = 50

ARCHETYPES: Dict[str, Archetype] = {
    "Stewards": Archetype(
        name="Stewards",
        colour="Green",
        hex_colour="#27AE60",
        description="Patient, family-controlled. The land is the family's soul.",
        win_condition="Retain more than 70% of the land after Round 4",
        secret_text=(
            "You represent the branch that worries about inter-generational wealth preservation. "
            "You believe the land should never be sold â€” it's the family's anchor asset. "
            "Ground leases are the only acceptable model. "
            "However, one family branch needs KES 50M within 6 months for a medical emergency. "
            "Generate liquidity or face a forced sale of some parcels."
        ),
        default_bias="Ground leases, 55 NDA, zero debt, strategic relationships",
        default_nda=55, default_green=40,
        default_monetisation="Steward",
        default_infra="Just-in-time",
        default_debt=0, default_partner="None", default_dev="Premium",
        default_nbo=2, default_gov=2, default_fin=1,
    ),
    "Developers": Archetype(
        name="Developers",
        colour="Blue",
        hex_colour="#2980B9",
        description="Aggressive, value-maximizing. The time to maximise value is now.",
        win_condition="Achieve at least KES 500M in cash distributions by end of Round 3",
        secret_text=(
            "You believe Nairobi's market cycle is at a peak â€” waiting is leaving money on the table. "
            "You know a senior County planning source has confirmed rezoning is likely in 18-24 months. "
            "A KES 10M fee can fast-track approvals through the County. "
            "And if Acacia buys the adjacent 3 acres (KES 120M), the family could triple their money. "
            "Do you pay the KES 10M fee? That decision has consequences."
        ),
        default_bias="Outright sales, 65 NDA, 50% debt, admin-only relationships",
        default_nda=65, default_green=15,
        default_monetisation="Developer",
        default_infra="Full upfront",
        default_debt=50, default_partner="None", default_dev="Mid-tier",
        default_nbo=0, default_gov=1, default_fin=0,
    ),
    "Rainmakers": Archetype(
        name="Rainmakers",
        colour="Gold",
        hex_colour="#D4A017",
        description="Partnership-oriented, capital-seeking. Connections and capital access.",
        win_condition="Secure an external institutional partner or SEZ designation by Round 4",
        secret_text=(
            "You have connections. A Pan-African DFI has expressed interest in a 30-40% JV for KES 2.5B. "
            "But Tatu City is actively poaching your target tenants with SEZ tax breaks. "
            "You have 6 months to differentiate Acacia or lose the anchor tenant. "
            "The DFI board meets in 30 days. You must submit a preliminary proposal within 2 weeks."
        ),
        default_bias="JVs, moderate debt, heavy relationship investment, partnerships",
        default_nda=60, default_green=30,
        default_monetisation="Balanced",
        default_infra="Phased",
        default_debt=40, default_partner="Minority", default_dev="Premium",
        default_nbo=2, default_gov=2, default_fin=2,
    ),
    "Gamblers": Archetype(
        name="Gamblers",
        colour="Red",
        hex_colour="#C0392B",
        description="Speculative, build-it-and-they'll-come. Speed above all.",
        win_condition="Phase 1 construction occupied by end of Round 3",
        secret_text=(
            "You believe Kenya's development trajectory is unstoppable and the biggest risk is being too cautious. "
            "Your financial analyst has confirmed that interest rates will drop 300bps in 12-18 months. "
            "If you lock debt NOW at current rates and refinance later, you save KES 200M+. "
            "The catch: you need to move fast before the rate drop is public knowledge. "
            "Build first, ask questions later."
        ),
        default_bias="Maximum debt, sell everything, full infrastructure upfront, ignore soft factors",
        default_nda=65, default_green=10,
        default_monetisation="Speculator",
        default_infra="Full upfront",
        default_debt=80, default_partner="Majority", default_dev="Lowest bid",
        default_nbo=0, default_gov=0, default_fin=0,
    ),
}

def get_archetype_by_colour(colour: str) -> Archetype:
    """Get archetype by colour name."""
    for a in ARCHETYPES.values():
        if a.colour.lower() == colour.lower():
            return a
    return list(ARCHETYPES.values())[0]
