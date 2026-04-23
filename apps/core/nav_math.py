"""
Pure-Python NAV calculation module for the /tools/nav-calculator/ feature.

No Django imports — this module is testable in isolation and reusable if
the calculator expands to multi-commodity or gets embedded in other views.

Methodology:
  1. Weight raw resource tonnage by category confidence (inferred 0.20,
     indicated 0.65, measured 0.90, probable 0.90, proven 1.00).
  2. Run a DCF on the risk-weighted ore body at the given commodity price,
     recovery, mine life, discount rate, opex, and capex.
  3. Apply a study-stage haircut to the final per-share NAV (PEA 0.70,
     PFS 0.85, FS 1.00) to reflect engineering precision of the inputs.
  4. Repeat across a price array for sensitivity reporting.

Simplifications in V1: no corporate tax, no sustaining capex, no
inflation, single commodity. These are acknowledged in the UI disclaimer
and are V2 extensions.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Dict


# Troy ounces per gram — used to convert grade in g/t to ounces per tonne.
GRAMS_PER_TROY_OZ = Decimal("31.1035")


# Default confidence weights by resource/reserve category.
# These are industry-accepted midpoints; a calculator user can override.
CATEGORY_WEIGHTS: Dict[str, Decimal] = {
    "inferred":  Decimal("0.20"),
    "indicated": Decimal("0.65"),
    "measured":  Decimal("0.90"),
    "probable":  Decimal("0.90"),  # probable RESERVES
    "proven":    Decimal("1.00"),  # proven RESERVES
}


# Study-stage multipliers. FS uses the study as reported; PFS/PEA apply
# additional haircuts reflecting economic-input precision.
STAGE_MULTIPLIERS: Dict[str, Decimal] = {
    "FS":  Decimal("1.00"),
    "PFS": Decimal("0.85"),
    "PEA": Decimal("0.70"),
}


@dataclass
class NavInputs:
    tonnes_inferred: Decimal
    tonnes_indicated: Decimal
    tonnes_measured: Decimal
    tonnes_probable: Decimal
    tonnes_proven: Decimal
    grade_gpt: Decimal          # grams per tonne
    recovery_pct: Decimal       # 0-100 (e.g. 90)
    opex_per_tonne: Decimal     # USD per tonne processed
    capex_millions: Decimal     # USD millions (initial capex)
    mine_life_years: int
    discount_rate_pct: Decimal  # 0-100 (e.g. 8)
    shares_outstanding_m: Decimal  # millions of shares fully diluted
    stage: str                  # "PEA" | "PFS" | "FS"


def _risk_weighted_tonnes(inp: NavInputs) -> Decimal:
    """Σ (category tonnes × confidence multiplier)."""
    return (
        inp.tonnes_inferred  * CATEGORY_WEIGHTS["inferred"]
        + inp.tonnes_indicated * CATEGORY_WEIGHTS["indicated"]
        + inp.tonnes_measured  * CATEGORY_WEIGHTS["measured"]
        + inp.tonnes_probable  * CATEGORY_WEIGHTS["probable"]
        + inp.tonnes_proven    * CATEGORY_WEIGHTS["proven"]
    )


def _gross_tonnes(inp: NavInputs) -> Decimal:
    """All categories at 100% — the theoretical maximum."""
    return (
        inp.tonnes_inferred + inp.tonnes_indicated + inp.tonnes_measured
        + inp.tonnes_probable + inp.tonnes_proven
    )


def _nav_per_share_at_price(
    tonnes: Decimal,
    inp: NavInputs,
    commodity_price: Decimal,
) -> Decimal:
    """
    Compute per-share NAV for a given ore-body tonnage at a given commodity
    price. Returns USD per share.

    Formula (simple DCF, no tax, no sustaining capex):
      recoverable_oz = tonnes × (grade_gpt / 31.1035) × recovery
      gross_revenue  = recoverable_oz × price
      annual_revenue = gross_revenue / mine_life
      annual_opex    = (tonnes / mine_life) × opex_per_tonne
      annual_cf      = annual_revenue - annual_opex
      npv            = Σ (annual_cf / (1+r)^t) for t in 1..mine_life
      nav            = npv - capex
      per_share      = nav / shares_outstanding
    """
    if tonnes <= 0 or inp.mine_life_years <= 0 or inp.shares_outstanding_m <= 0:
        return Decimal("0")

    recovery_frac = inp.recovery_pct / Decimal("100")
    recoverable_oz = tonnes * (inp.grade_gpt / GRAMS_PER_TROY_OZ) * recovery_frac
    gross_revenue = recoverable_oz * commodity_price  # USD

    annual_revenue = gross_revenue / Decimal(inp.mine_life_years)
    annual_opex    = (tonnes / Decimal(inp.mine_life_years)) * inp.opex_per_tonne
    annual_cf      = annual_revenue - annual_opex

    r = inp.discount_rate_pct / Decimal("100")
    discount_factor = Decimal("1") + r
    npv = Decimal("0")
    for t in range(1, inp.mine_life_years + 1):
        npv += annual_cf / (discount_factor ** t)

    nav = npv - (inp.capex_millions * Decimal("1000000"))
    shares = inp.shares_outstanding_m * Decimal("1000000")
    return nav / shares


@dataclass
class NavScenario:
    label: str
    description: str
    tonnage_basis: str   # "gross" or "risk-weighted"
    apply_stage: bool


SCENARIOS: List[NavScenario] = [
    NavScenario(
        label="Gross NAV (unadjusted)",
        description="Theoretical maximum — all resource categories at 100%, no stage haircut. Reference only.",
        tonnage_basis="gross",
        apply_stage=False,
    ),
    NavScenario(
        label="Category-weighted NAV",
        description="Resource categories discounted by confidence (inferred 20%, indicated 65%, measured/probable 90%, proven 100%). No stage haircut.",
        tonnage_basis="risk-weighted",
        apply_stage=False,
    ),
    NavScenario(
        label="Stage-adjusted NAV (recommended)",
        description="Category-weighted AND stage-discounted (PEA 70%, PFS 85%, FS 100%). The number to anchor on for position sizing.",
        tonnage_basis="risk-weighted",
        apply_stage=True,
    ),
]


def calculate_nav_matrix(
    inp: NavInputs,
    prices: List[Dict[str, Decimal]],
) -> List[Dict]:
    """
    Produce the full NAV matrix: rows = scenarios, columns = price benchmarks.

    `prices` is a list of dicts: [{"label": "Current Spot", "price": Decimal("4800")}, ...]

    Returns a list of rows, each with keys:
      - label, description, tonnage_basis, apply_stage
      - values: list of {label, price, nav_per_share} (same length as `prices`)
    """
    gross_t = _gross_tonnes(inp)
    weighted_t = _risk_weighted_tonnes(inp)
    stage_mult = STAGE_MULTIPLIERS.get(inp.stage, Decimal("1.00"))

    rows = []
    for scenario in SCENARIOS:
        tonnes = gross_t if scenario.tonnage_basis == "gross" else weighted_t
        stage_factor = stage_mult if scenario.apply_stage else Decimal("1")

        values = []
        for col in prices:
            price = col["price"]
            if price is None or price <= 0:
                nav_ps = None
            else:
                nav_ps = _nav_per_share_at_price(tonnes, inp, price) * stage_factor
            values.append({
                "label": col["label"],
                "price": price,
                "nav_per_share": nav_ps,
            })

        rows.append({
            "label": scenario.label,
            "description": scenario.description,
            "tonnage_basis": scenario.tonnage_basis,
            "apply_stage": scenario.apply_stage,
            "highlight": scenario.apply_stage,  # bold the "recommended" row
            "values": values,
        })

    return rows
