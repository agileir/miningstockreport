"""
NAV calculation module — commodity-agnostic DCF core with per-commodity
revenue helpers. Used by /tools/nav-calculator/ (gold), plus copper,
silver, and polymetallic variants.

Methodology (unchanged across commodities):
  1. Weight raw resource tonnage by category confidence (inferred 0.20,
     indicated 0.65, measured 0.90, probable 0.90, proven 1.00).
  2. For each tonne of ore processed, compute the gross revenue per tonne
     from the sum of commodity contributions (grade × recovery × price,
     converted to the appropriate price unit).
  3. Run a simple DCF on the risk-weighted tonnage at each revenue-per-
     tonne scenario.
  4. Apply study-stage haircut (PEA 0.70, PFS 0.85, FS 1.00).

Simplifications: no corporate tax, no sustaining capex, no inflation,
no royalties/NSRs. All acknowledged in the UI disclaimer.
"""
from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Dict, Optional


# ────────────────────────────────────────────────────────────────────────
# Unit conversions
# ────────────────────────────────────────────────────────────────────────
GRAMS_PER_TROY_OZ = Decimal("31.1035")       # g → oz troy
POUNDS_PER_TONNE  = Decimal("2204.6226")     # t → lb (metric tonne)


def grams_per_tonne_to_oz_per_tonne(gpt: Decimal) -> Decimal:
    """g/t → troy oz / tonne. Applies to gold and silver."""
    return gpt / GRAMS_PER_TROY_OZ


def pct_grade_to_lb_per_tonne(pct: Decimal) -> Decimal:
    """% grade → pounds / tonne. Applies to copper."""
    return (pct / Decimal("100")) * POUNDS_PER_TONNE


# ────────────────────────────────────────────────────────────────────────
# Category and stage adjustments
# ────────────────────────────────────────────────────────────────────────
CATEGORY_WEIGHTS: Dict[str, Decimal] = {
    "inferred":  Decimal("0.20"),
    "indicated": Decimal("0.65"),
    "measured":  Decimal("0.90"),
    "probable":  Decimal("0.90"),
    "proven":    Decimal("1.00"),
}


STAGE_MULTIPLIERS: Dict[str, Decimal] = {
    "FS":  Decimal("1.00"),
    "PFS": Decimal("0.85"),
    "PEA": Decimal("0.70"),
}


# ────────────────────────────────────────────────────────────────────────
# Resource-body inputs (shared across all commodity tools)
# ────────────────────────────────────────────────────────────────────────
@dataclass
class ResourceInputs:
    tonnes_inferred:  Decimal = Decimal("0")
    tonnes_indicated: Decimal = Decimal("0")
    tonnes_measured:  Decimal = Decimal("0")
    tonnes_probable:  Decimal = Decimal("0")
    tonnes_proven:    Decimal = Decimal("0")

    def gross_tonnes(self) -> Decimal:
        return (
            self.tonnes_inferred + self.tonnes_indicated + self.tonnes_measured
            + self.tonnes_probable + self.tonnes_proven
        )

    def risk_weighted_tonnes(self) -> Decimal:
        return (
            self.tonnes_inferred  * CATEGORY_WEIGHTS["inferred"]
            + self.tonnes_indicated * CATEGORY_WEIGHTS["indicated"]
            + self.tonnes_measured  * CATEGORY_WEIGHTS["measured"]
            + self.tonnes_probable  * CATEGORY_WEIGHTS["probable"]
            + self.tonnes_proven    * CATEGORY_WEIGHTS["proven"]
        )


# ────────────────────────────────────────────────────────────────────────
# Financial / operational inputs (shared)
# ────────────────────────────────────────────────────────────────────────
@dataclass
class OperationalInputs:
    opex_per_tonne:       Decimal      # USD per tonne processed
    capex_millions:       Decimal      # USD millions
    mine_life_years:      int
    discount_rate_pct:    Decimal      # 0-100
    shares_outstanding_m: Decimal      # millions
    stage:                str          # "PEA" | "PFS" | "FS"


# ────────────────────────────────────────────────────────────────────────
# Per-commodity revenue math
# ────────────────────────────────────────────────────────────────────────
def gold_or_silver_revenue_per_tonne(grade_gpt: Decimal, recovery_pct: Decimal, price_per_oz: Decimal) -> Decimal:
    """Revenue per processed tonne for gold or silver."""
    oz_per_tonne = grams_per_tonne_to_oz_per_tonne(grade_gpt)
    recovery = recovery_pct / Decimal("100")
    return oz_per_tonne * recovery * price_per_oz


def copper_revenue_per_tonne(grade_pct: Decimal, recovery_pct: Decimal, price_per_lb: Decimal) -> Decimal:
    """Revenue per processed tonne for copper."""
    lb_per_tonne = pct_grade_to_lb_per_tonne(grade_pct)
    recovery = recovery_pct / Decimal("100")
    return lb_per_tonne * recovery * price_per_lb


# ────────────────────────────────────────────────────────────────────────
# Core DCF — commodity-agnostic
# ────────────────────────────────────────────────────────────────────────
def _nav_per_share_from_revenue(
    tonnes: Decimal,
    revenue_per_tonne: Decimal,
    op: OperationalInputs,
) -> Decimal:
    """
    Run simple DCF: total revenue spread across mine life, annual opex
    subtracted, discounted, less capex, divided by shares outstanding.
    """
    if tonnes <= 0 or op.mine_life_years <= 0 or op.shares_outstanding_m <= 0:
        return Decimal("0")

    gross_revenue  = tonnes * revenue_per_tonne
    annual_revenue = gross_revenue / Decimal(op.mine_life_years)
    annual_opex    = (tonnes / Decimal(op.mine_life_years)) * op.opex_per_tonne
    annual_cf      = annual_revenue - annual_opex

    r = op.discount_rate_pct / Decimal("100")
    discount_factor = Decimal("1") + r
    npv = Decimal("0")
    for t in range(1, op.mine_life_years + 1):
        npv += annual_cf / (discount_factor ** t)

    nav = npv - (op.capex_millions * Decimal("1000000"))
    shares = op.shares_outstanding_m * Decimal("1000000")
    return nav / shares


# ────────────────────────────────────────────────────────────────────────
# Matrix output (rows = risk scenarios × columns = price scenarios)
# ────────────────────────────────────────────────────────────────────────
@dataclass
class Scenario:
    label: str
    description: str
    tonnage_basis: str   # "gross" or "risk-weighted"
    apply_stage: bool
    highlight: bool = False


SCENARIOS: List[Scenario] = [
    Scenario(
        label="Gross NAV (unadjusted)",
        description="Theoretical maximum — all resource categories at 100%, no stage haircut. Reference only.",
        tonnage_basis="gross",
        apply_stage=False,
    ),
    Scenario(
        label="Category-weighted NAV",
        description="Resource categories discounted by confidence (inferred 20%, indicated 65%, measured/probable 90%, proven 100%). No stage haircut.",
        tonnage_basis="risk-weighted",
        apply_stage=False,
    ),
    Scenario(
        label="Stage-adjusted NAV (recommended)",
        description="Category-weighted AND stage-discounted (PEA 70%, PFS 85%, FS 100%). The number to anchor on for position sizing.",
        tonnage_basis="risk-weighted",
        apply_stage=True,
        highlight=True,
    ),
]


def calculate_nav_matrix(
    res: ResourceInputs,
    op: OperationalInputs,
    price_scenarios: List[Dict],
) -> List[Dict]:
    """
    `price_scenarios` is a list of dicts, each containing:
      {"label": str, "revenue_per_tonne": Decimal, "display_value": str}

    Returns a list of rows, each with:
      - label, description, highlight
      - values: list of {label, display_value, nav_per_share}
    """
    gross_t = res.gross_tonnes()
    weighted_t = res.risk_weighted_tonnes()
    stage_mult = STAGE_MULTIPLIERS.get(op.stage, Decimal("1.00"))

    rows = []
    for scenario in SCENARIOS:
        tonnes = gross_t if scenario.tonnage_basis == "gross" else weighted_t
        stage_factor = stage_mult if scenario.apply_stage else Decimal("1")

        values = []
        for col in price_scenarios:
            rev = col.get("revenue_per_tonne")
            if rev is None or rev <= 0:
                nav_ps = None
            else:
                nav_ps = _nav_per_share_from_revenue(tonnes, rev, op) * stage_factor
            values.append({
                "label": col["label"],
                "display_value": col.get("display_value", ""),
                "nav_per_share": nav_ps,
            })

        rows.append({
            "label": scenario.label,
            "description": scenario.description,
            "tonnage_basis": scenario.tonnage_basis,
            "apply_stage": scenario.apply_stage,
            "highlight": scenario.highlight,
            "values": values,
        })

    return rows


# ────────────────────────────────────────────────────────────────────────
# Backward-compat wrapper for the original gold-only calculator
# ────────────────────────────────────────────────────────────────────────
@dataclass
class NavInputs:
    """Legacy dataclass used by /tools/nav-calculator/ (gold-only)."""
    tonnes_inferred:      Decimal
    tonnes_indicated:     Decimal
    tonnes_measured:      Decimal
    tonnes_probable:      Decimal
    tonnes_proven:        Decimal
    grade_gpt:            Decimal
    recovery_pct:         Decimal
    opex_per_tonne:       Decimal
    capex_millions:       Decimal
    mine_life_years:      int
    discount_rate_pct:    Decimal
    shares_outstanding_m: Decimal
    stage:                str


def calculate_nav_matrix_gold_legacy(inp: NavInputs, prices: List[Dict]) -> List[Dict]:
    """Legacy entry point — takes NavInputs + price dicts and builds the matrix."""
    res = ResourceInputs(
        tonnes_inferred=inp.tonnes_inferred, tonnes_indicated=inp.tonnes_indicated,
        tonnes_measured=inp.tonnes_measured, tonnes_probable=inp.tonnes_probable,
        tonnes_proven=inp.tonnes_proven,
    )
    op = OperationalInputs(
        opex_per_tonne=inp.opex_per_tonne, capex_millions=inp.capex_millions,
        mine_life_years=inp.mine_life_years, discount_rate_pct=inp.discount_rate_pct,
        shares_outstanding_m=inp.shares_outstanding_m, stage=inp.stage,
    )
    price_scenarios = []
    for col in prices:
        price = col.get("price")
        if price and price > 0:
            rev = gold_or_silver_revenue_per_tonne(inp.grade_gpt, inp.recovery_pct, price)
        else:
            rev = None
        price_scenarios.append({
            "label": col["label"],
            "revenue_per_tonne": rev,
            "display_value": f"${price:,.0f}" if price else "",
        })
    return calculate_nav_matrix(res, op, price_scenarios)
