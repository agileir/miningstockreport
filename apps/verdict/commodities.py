"""
Registry of commodity-list pages: /list-{slug}-stocks/

Each entry drives a list view, the sitemap, the footer block, and the
SEO meta block on the rendered page. Match terms are checked
case-insensitively against Company.primary_commodity, so a company
tagged "Gold/Copper" surfaces on both the gold and copper lists.
"""

COMMODITIES = {
    "gold": {
        "display": "Gold",
        "h1": "List of Gold Mining Stocks",
        "match_terms": ["gold"],
        "meta_description": (
            "List of gold mining stocks rated by the Verdict Framework. Every "
            "company scored on management, geology, capital structure, catalysts, "
            "and acquisition value — BUY, WATCH, or AVOID."
        ),
        "intro": (
            "A curated list of gold mining stocks — junior explorers, developers, "
            "and producers — each rated on five factors using public-filings data "
            "and the most recent NI 43-101 technical report. Sorted by most "
            "recently scored. Click any ticker for the full scorecard."
        ),
    },
    "silver": {
        "display": "Silver",
        "h1": "List of Silver Mining Stocks",
        "match_terms": ["silver"],
        "meta_description": (
            "List of silver mining stocks rated by the Verdict Framework. Primary "
            "silver producers, developers, and explorers scored BUY, WATCH, or AVOID "
            "on five public-filings factors."
        ),
        "intro": (
            "Silver mining stocks rated by the Verdict Framework. Includes primary "
            "silver developers and producers, plus polymetallic deposits where "
            "silver carries meaningful revenue. Sorted by most recently scored."
        ),
    },
    "copper": {
        "display": "Copper",
        "h1": "List of Copper Mining Stocks",
        "match_terms": ["copper"],
        "meta_description": (
            "List of copper mining stocks rated by the Verdict Framework. "
            "Porphyry, sediment-hosted, and polymetallic copper deposits scored "
            "BUY, WATCH, or AVOID on five factors."
        ),
        "intro": (
            "Copper mining stocks — porphyry developers, sediment-hosted plays, "
            "and copper-gold polymetallic systems — rated by the Verdict "
            "Framework using the most recent NI 43-101 technical report. Sorted "
            "by most recently scored."
        ),
    },
    "uranium": {
        "display": "Uranium",
        "h1": "List of Uranium Mining Stocks",
        "match_terms": ["uranium"],
        "meta_description": (
            "List of uranium mining stocks rated by the Verdict Framework. "
            "Athabasca developers, ISR producers, and global explorers scored "
            "BUY, WATCH, or AVOID on five factors."
        ),
        "intro": (
            "Uranium mining stocks rated by the Verdict Framework. Coverage spans "
            "Athabasca Basin developers, ISR producers, and global exploration "
            "stories. Sorted by most recently scored."
        ),
    },
    "lithium": {
        "display": "Lithium",
        "h1": "List of Lithium Mining Stocks",
        "match_terms": ["lithium"],
        "meta_description": (
            "List of lithium mining stocks rated by the Verdict Framework. "
            "Hard-rock spodumene, brine, and clay-hosted lithium developers "
            "scored BUY, WATCH, or AVOID."
        ),
        "intro": (
            "Lithium mining stocks rated by the Verdict Framework. Includes "
            "hard-rock spodumene, brine, and clay-hosted projects across "
            "Canada, Australia, South America, and the United States. Sorted "
            "by most recently scored."
        ),
    },
    "nickel": {
        "display": "Nickel",
        "h1": "List of Nickel Mining Stocks",
        "match_terms": ["nickel"],
        "meta_description": (
            "List of nickel mining stocks rated by the Verdict Framework. "
            "Sulphide, laterite, and Class-1 battery-grade nickel developers "
            "scored BUY, WATCH, or AVOID."
        ),
        "intro": (
            "Nickel mining stocks rated by the Verdict Framework. Coverage "
            "includes sulphide deposits suitable for Class-1 battery-grade "
            "nickel sulphate and laterite producers serving the stainless market. "
            "Sorted by most recently scored."
        ),
    },
    "rare-earth": {
        "display": "Rare Earth",
        "h1": "List of Rare Earth Stocks",
        "match_terms": ["rare earth", "ree", "rare earths"],
        "meta_description": (
            "List of rare earth mining stocks rated by the Verdict Framework. "
            "Light and heavy REE developers across North America, Australia, "
            "and Africa scored BUY, WATCH, or AVOID."
        ),
        "intro": (
            "Rare earth mining stocks rated by the Verdict Framework. Coverage "
            "spans light REE (Nd, Pr) and heavy REE (Dy, Tb) developers across "
            "North America, Australia, and Africa, with particular attention to "
            "non-China supply security. Sorted by most recently scored."
        ),
    },
}


def get_commodity(slug: str):
    """Return the registry entry for a commodity slug, or None if unknown."""
    return COMMODITIES.get(slug)


def all_commodities():
    """Return an iterable of (slug, display_name) for navigation/footer use."""
    return [(slug, entry["display"]) for slug, entry in COMMODITIES.items()]
