"""Implications library — narrative explanations for each decision."""

IMPLICATIONS = {
    # ── NDA ──
    "nda_55": (
        "By setting aside 10 acres as permanent green buffer, Belgo creates a 15% development reserve "
        "that dramatically reduces CC&R legal challenge risk. The trade-off: total saleable land drops 15%, "
        "reducing potential top-line revenue by approximately $80M at target pricing ($10M/acre). However, "
        "the premium positioning enabled by the buffer typically commands 15-20% higher per-acre pricing "
        "on remaining parcels, partially offsetting the volume loss."
    ),
    "nda_60": (
        "A balanced NDA of 60 acres preserves 5 acres of buffer while maintaining 92% of potential "
        "developable area. This is the pragmatic middle ground: enough green buffer to satisfy CC&R "
        "requirements and community expectations, without materially sacrificing revenue potential."
    ),
    "nda_65": (
        "Maximising developable area to 65 acres increases total potential revenue by ~$80M at target "
        "pricing. However, the absence of any development buffer increases CC&R legal vulnerability. "
        "If challenged, a court could order Belgo to set aside additional green space at the most "
        "inconvenient location, potentially disrupting the master plan."
    ),

    # ── GREEN SPACE ──
    "green_40": (
        "Forty percent green space positions Kitisuru Corporate Campus as a premier executive environment. "
        "This attracts the highest-quality tenants and commands 15-20% rental premium over standard "
        "commercial parks. Notable benchmarks: Apple Park (80%), GooglePlex (40%), Two Rivers (35%). "
        "The trade-off: reduced buildable area means lower total leasable square footage."
    ),
    "green_30": (
        "Thirty percent green space meets international best practice for corporate campuses. "
        "LEED Gold certification becomes achievable without sacrificing significant developable area. "
        "This is the minimum recommended by urban design standards for premium corporate environments."
    ),
    "green_20": (
        "Twenty percent green space meets minimum zoning requirements but positions the campus as "
        "'standard commercial' rather than 'premium executive.' Tenant quality and rental rates "
        "will reflect this positioning. Most Nairobi commercial developments operate at ~15-20% green space."
    ),
    "green_10": (
        "Ten percent green space maximises leasable area but creates a dense, hardscape environment. "
        "This may deter premium tenants who increasingly demand outdoor space and wellness amenities. "
        "Post-COVID, 40% of corporate tenants cite outdoor space as a top-3 decision factor in lease selection."
    ),

    # ── MONETISATION ──
    "mon_Steward": (
        "The Steward approach retains 90% of the land in family ownership while generating recurring "
        "ground lease income from Year 3. Annual lease revenue at 6% of land value yields approximately "
        "$3.6M/year on 46 leased acres, growing with inflation. The trade-off: first meaningful cash "
        "distribution to the family does not hit until Year 5-7. Total 20-year IRR depends on inflation-linked "
        "rent escalations of at least 3% annually. Nairobi prime real estate has averaged 4.2% annual "
        "appreciation over 20-year periods."
    ),
    "mon_Balanced": (
        "The Balanced approach provides near-term liquidity through 30% outright sales (generating ~$156M "
        "in Year 1-2) while retaining long-term income through 40% ground leases. The 30% JV component "
        "shares development upside with a partner but dilutes family control proportionally. This is the "
        "most flexible approach — it does not lock Belgo into a single monetisation strategy for the entire site."
    ),
    "mon_Developer": (
        "The Developer approach maximises near-term cash: 60% outright sales generate ~$312M in Year 1-2. "
        "The family receives substantial liquidity immediately but permanently cedes ownership of the sold "
        "parcels. At $10M/acre, 39 acres sold = $390M one-time. However, the 39 acres could have generated "
        "$3M+/year in ground lease income forever (capitalised value: $50M+ at 6% cap rate)."
    ),
    "mon_Speculator": (
        "The Speculator approach sells 70% outright — the maximum cash velocity. This generates ~$364M in "
        "Year 1-2 but leaves the family owning only ~20 acres after 4 rounds. The remaining ground lease "
        "income ($1.1M/year) is insufficient to sustain Belgo Holdings as an operating entity. This approach "
        "is essentially a land sale disguised as a development project."
    ),
    
    # ── INFRASTRUCTURE ──
    "infra_JIT": (
        "Just-in-time infrastructure is the lowest-risk approach. Roads and utilities are built only as "
        "tenants commit. The initial capital outlay is minimal (~KES 500M vs KES 3.2B for full upfront). "
        "The trade-off: construction timelines extend by 12-18 months as infrastructure must be completed "
        "before building construction can begin on each phase."
    ),
    "infra_Phased": (
        "Phased trunk infrastructure builds main arteries (water trunk, primary road spine, main power "
        "feeder) in Phase 1 at a cost of ~KES 1.8B. Secondary infrastructure is built as parcels sell. "
        "This balances speed (Phase 1 construction can begin Month 18) with capital efficiency (not all "
        "KES 3.2B needed upfront). This is the standard approach for developments of this scale."
    ),
    "infra_Full": (
        "Full upfront infrastructure costs KES 3.2B and requires debt financing unless the family has "
        "substantial liquidity. The advantage: parcels are 'shovel-ready' for immediate tenant construction, "
        "reducing time-to-revenue by 18 months. The risk: if tenant demand materialises slower than projected, "
        "Belgo carries KES 3.2B in debt with no income. Konza Technopolis provides a cautionary example."
    ),

    # ── RELATIONSHIPS ──
    "nbo_strategic": (
        "Investing KES 10M/round in neighbourhood relationships is the highest-return decision in the "
        "simulation: +10 reputation per round, lawsuit immunity, faster permits (-3 months), and premium "
        "brand perception. In real estate development, community opposition is the single most common "
        "cause of 18-24 month delays on projects of this scale. KES 30M over 3 rounds is cheap insurance "
        "against a delay that costs KES 200M+ in carry costs alone."
    ),
    "nbo_ignored": (
        "Ignoring the neighbourhood is the riskiest non-decision in the simulation. The Residents "
        "Association has legal standing to challenge the Change of Use approval. A court injunction can "
        "stop all construction. This is not hypothetical: in 2023, three Nairobi projects of comparable "
        "scale faced court-ordered delays averaging 18 months due to inadequate community engagement."
    ),
    "gov_strategic": (
        "Strategic partnership with the County Government unlocks faster permits (-6 months), opens the "
        "SEZ application pathway, and provides early warning of regulatory changes. The SEZ designation "
        "is particularly valuable: it would allow Belgo to offer 10% corporate tax for 10 years, directly "
        "matching Tatu City's competitive advantage."
    ),
    "fin_strategic": (
        "Strategic engagement with financial institutions yields 2% below-market interest rates, multiple "
        "bidders for tenders, and premium exit valuations. Each 'Strategic' FIN relationship adds +5 IRR "
        "points. Over the 20-year development horizon, a 2% interest rate differential on KES 2B in debt "
        "saves KES 400M+ in interest payments."
    ),
    
    # ── DEBT ──
    "debt_0": (
        "Zero debt means the family funds development entirely from equity. This is the safest approach "
        "(no default risk, no interest payments) but the slowest: development capacity is limited by "
        "available family capital. At KES 500M family equity, Phase 1 infrastructure costs (KES 1.8-3.2B) "
        "would need to be funded from land sales first, adding 2-3 years to the timeline."
    ),
    "debt_high": (
        "Debt above 70% LTV is considered aggressive leverage for a development project of this scale. "
        "While it accelerates construction (Phase 1 can start immediately), it leaves Belgo highly "
        "vulnerable to market shocks. If tenant demand softens or interest rates rise, debt service costs "
        "can consume 40-60% of gross income. A 300bps rate hike (the CBK's 2024 pattern) adds KES 96M/year "
        "in interest on KES 2.8B debt."
    ),
    
    # ── DEVELOPER QUALITY ──
    "dev_premium": (
        "Premium developers deliver on time and on budget, with proven track records on comparable projects. "
        "Their fees are 15-20% higher than market average, but schedule overruns (which cost 3-5%/month in "
        "carry costs) are virtually eliminated. For a KES 3.2B Phase 1, a 6-month delay costs KES 160-240M "
        "in carry costs — far outweighing any premium developer fee differential."
    ),
    "dev_lowest": (
        "The lowest-bid developer is the highest-risk choice. Cost overruns (20-40% above contract value), "
        "schedule delays (6-18 months), and quality defects are statistically more likely. In Kenya's "
        "construction market, 37% of lowest-bid contracts on commercial projects experience material "
        "disputes or delays (KAGB 2023 Construction Industry Report)."
    ),
    
    # ── EXIT / OFFER ──
    "offer_accept": (
        "Accepting the KES 88B ($1.1B) offer generates immediate liquidity for the family. At the target "
        "$10M/acre, this is a fair market price. However, it permanently ends Belgo's development journey. "
        "The family becomes cash-rich but asset-light. For context: 88 acres at $10M/acre = $880M. The "
        "$1.1B offer represents a 25% premium over current market pricing, reflecting the buyer's valuation "
        "of Belgo's development progress (Safaricom commitment, approved master plan, CC&Rs in place)."
    ),
    "offer_decline": (
        "Declining the $1.1B offer signals the family's commitment to the long-term vision. This decision "
        "is supported if the family believes the fully-developed campus (with Safaricom, ABSA, and future "
        "tenants) will be worth significantly more than $1.1B. The projected terminal value of the developed "
        "campus at stabilized occupancy is $1.8-2.4B (Year 15-20). The trade-off: 15-20 years of development "
        "risk, financing costs, and management effort."
    ),
    
    # ── CONSTITUTION ──
    "constitution_yes": (
        "Adopting a family constitution is the single most important governance decision Belgo can make. "
        "It establishes decision-making protocols for dispute resolution (the Round 4 scenario), sets rules "
        "for share transfers and buyouts, and creates a framework for inter-generational governance. "
        "Families with constitutions are 3x more likely to retain assets across 3+ generations (Family "
        "Business Institute, 2023). This is worth +15 resilience points for a reason."
    ),
    "constitution_no": (
        "Not having a constitution means every future dispute goes to the default legal framework: the "
        "Law of Succession Act (Cap 160). This is adversarial, expensive, and slow. A family dispute "
        "that could be resolved in 3 months via mediation (KES 5M) instead takes 2-5 years in court "
        "(KES 20M+ in legal fees). The Round 4 dispute scenario was designed to surface this exact risk."
    ),
}


def get_implication(key: str) -> str:
    """Get implication text by key. Returns generic message if key not found."""
    return IMPLICATIONS.get(key, f"(No detailed implication available for '{key}')")


def build_implications_from_decisions(decisions: dict) -> list:
    """Build a list of (decision_label, implication_text) from a group's decisions."""
    results = []
    
    key_map = {
        'nda': ('Net Developable Acres', f"nda_{decisions.get('nda', 60)}"),
        'green_space': ('Green Space', f"green_{decisions.get('green_space', 20)}"),
        'monetisation': ('Monetisation Approach', f"mon_{decisions.get('monetisation', 'Balanced')}"),
        'infra': ('Infrastructure Timing', f"infra_{decisions.get('infra', 'Phased').replace(' ', '_').replace('-', '_')}"),
        'debt_pct': ('Debt Level', 'debt_0' if decisions.get('debt_pct', 0) == 0 else 'debt_high' if decisions.get('debt_pct', 0) >= 70 else None),
        'dev_quality': ('Developer Quality', f"dev_{decisions.get('dev_quality', 'Mid-tier').lower().replace(' ', '_')}"),
        'constitution': ('Family Constitution', f"constitution_{'yes' if decisions.get('constitution', 1) == 1 else 'no'}"),
        'offer': ('Buyout Offer Response', 'offer_accept' if decisions.get('offer', 1) == 0 else 'offer_decline' if decisions.get('offer', 1) == 2 else None),
    }
    
    for key, (label, imp_key) in key_map.items():
        if imp_key and imp_key in IMPLICATIONS:
            results.append((label, IMPLICATIONS[imp_key]))
    
    # NBO relationship implication
    nbo_level = max([
        decisions.get(f'nbo_r{i}', 0) for i in range(1, 5)
    ])
    if nbo_level == 2:
        results.append(('NBO Relationship', IMPLICATIONS['nbo_strategic']))
    elif nbo_level == 0:
        results.append(('NBO Relationship (Ignored)', IMPLICATIONS['nbo_ignored']))
    
    # FIN relationship
    fin_level = max([
        decisions.get(f'fin_r{i}', 0) for i in range(1, 5)
    ])
    if fin_level == 2:
        results.append(('FIN Relationship', IMPLICATIONS['fin_strategic']))
    
    return results
