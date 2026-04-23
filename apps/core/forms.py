from decimal import Decimal

from django import forms


STAGE_CHOICES = [
    ("FS",  "Feasibility Study (FS) — study as reported"),
    ("PFS", "Pre-Feasibility Study (PFS) — 15% haircut"),
    ("PEA", "Preliminary Economic Assessment (PEA) — 30% haircut"),
]


class NavCalculatorForm(forms.Form):
    """
    NAV Calculator inputs — gold-only in V1. Inputs map directly to the
    NavInputs dataclass in apps.core.nav_math.
    """
    # ── Resource inputs (all in millions of tonnes) ──
    tonnes_inferred  = forms.DecimalField(label="Inferred resource (Mt)",  initial=0, min_value=0, decimal_places=3, max_digits=12, required=False)
    tonnes_indicated = forms.DecimalField(label="Indicated resource (Mt)", initial=0, min_value=0, decimal_places=3, max_digits=12, required=False)
    tonnes_measured  = forms.DecimalField(label="Measured resource (Mt)",  initial=0, min_value=0, decimal_places=3, max_digits=12, required=False)
    tonnes_probable  = forms.DecimalField(label="Probable reserves (Mt)",  initial=0, min_value=0, decimal_places=3, max_digits=12, required=False)
    tonnes_proven    = forms.DecimalField(label="Proven reserves (Mt)",    initial=0, min_value=0, decimal_places=3, max_digits=12, required=False)

    grade_gpt = forms.DecimalField(
        label="Grade (g/t gold)",
        min_value=Decimal("0.1"),
        decimal_places=3,
        max_digits=8,
        initial=Decimal("1.50"),
        required=False,
        help_text="Average grade across the deposit in grams per tonne. Leave blank to use a 1.50 g/t default.",
    )
    recovery_pct = forms.DecimalField(
        label="Metallurgical recovery (%)",
        min_value=Decimal("10"),
        max_value=Decimal("100"),
        decimal_places=1,
        max_digits=4,
        initial=Decimal("90.0"),
        required=False,
        help_text="Percentage of gold recovered. Typical 85-95% heap leach, 90-96% CIL/CIP. Blank defaults to 90%.",
    )

    # ── Operating inputs (all optional; defaults applied if blank) ──
    opex_per_tonne = forms.DecimalField(
        label="Opex per tonne processed ($/t)",
        min_value=0,
        decimal_places=2,
        max_digits=8,
        initial=Decimal("40.00"),
        required=False,
        help_text="All-in operating cost per tonne milled: mining + processing + G&A. Blank defaults to $40/t.",
    )
    capex_millions = forms.DecimalField(
        label="Initial capex ($M)",
        min_value=0,
        decimal_places=2,
        max_digits=10,
        initial=Decimal("500.00"),
        required=False,
        help_text="Upfront capital for mine construction. Blank defaults to $500M.",
    )
    mine_life_years = forms.IntegerField(
        label="Mine life (years)",
        min_value=1,
        max_value=50,
        initial=10,
        required=False,
    )

    # ── Financial inputs (all optional; defaults applied if blank) ──
    discount_rate_pct = forms.DecimalField(
        label="Discount rate (%)",
        min_value=Decimal("0"),
        max_value=Decimal("25"),
        decimal_places=2,
        max_digits=5,
        initial=Decimal("8.00"),
        required=False,
        help_text="Typically 5% for a producer, 8% for a developer, 10%+ for an explorer. Blank defaults to 8%.",
    )
    shares_outstanding_m = forms.DecimalField(
        label="Shares outstanding, fully diluted (M)",
        min_value=Decimal("0.1"),
        decimal_places=3,
        max_digits=12,
        initial=Decimal("100.000"),
        required=False,
        help_text="Millions of shares fully diluted, including warrants and options. Blank defaults to 100M.",
    )

    # ── Study stage ──
    stage = forms.ChoiceField(
        label="Study stage",
        choices=STAGE_CHOICES,
        initial="PFS",
        required=False,
        help_text="Pick the stage matching the underlying technical study. Stage haircut applied to the final risk-adjusted NAV.",
    )

    # ── Price benchmarks (up to 4) ──
    price_label_1 = forms.CharField(label="Price label 1", initial="Current Spot", max_length=40, required=False)
    price_value_1 = forms.DecimalField(label="Gold price 1 ($/oz)", min_value=0, decimal_places=2, max_digits=8, required=False)

    price_label_2 = forms.CharField(label="Price label 2", initial="3-Month Average", max_length=40, required=False)
    price_value_2 = forms.DecimalField(label="Gold price 2 ($/oz)", min_value=0, decimal_places=2, max_digits=8, required=False)

    price_label_3 = forms.CharField(label="Price label 3", initial="12-Month Average", max_length=40, required=False)
    price_value_3 = forms.DecimalField(label="Gold price 3 ($/oz)", min_value=0, decimal_places=2, max_digits=8, required=False)

    price_label_4 = forms.CharField(label="Price label 4", initial="Custom", max_length=40, required=False)
    price_value_4 = forms.DecimalField(label="Gold price 4 ($/oz)", min_value=0, decimal_places=2, max_digits=8, required=False)

    def clean(self):
        cleaned = super().clean()
        # Require at least one resource tonnage > 0
        total_tonnes = sum(
            (cleaned.get(f, 0) or Decimal("0")) for f in (
                "tonnes_inferred", "tonnes_indicated", "tonnes_measured",
                "tonnes_probable", "tonnes_proven",
            )
        )
        if total_tonnes <= 0:
            raise forms.ValidationError(
                "Enter at least one non-zero resource or reserve tonnage."
            )

        # Require at least one price column filled
        prices = [cleaned.get(f"price_value_{i}") for i in range(1, 5)]
        if not any(p and p > 0 for p in prices):
            raise forms.ValidationError(
                "Enter at least one gold price in the price-benchmark columns."
            )

        return cleaned

    def get_price_columns(self):
        """Return only the populated price columns in label/price form."""
        cols = []
        for i in range(1, 5):
            price = self.cleaned_data.get(f"price_value_{i}")
            label = self.cleaned_data.get(f"price_label_{i}") or f"Price {i}"
            if price and price > 0:
                cols.append({"label": label, "price": price})
        return cols


# ────────────────────────────────────────────────────────────────────────
# Shared base with resource + operational + financial fields. The three
# new commodity-specific forms below add commodity-particular grade /
# recovery / price inputs on top.
# ────────────────────────────────────────────────────────────────────────
class _BaseNavForm(forms.Form):
    tonnes_inferred  = forms.DecimalField(label="Inferred resource (Mt)",  initial=0, min_value=0, decimal_places=3, max_digits=12, required=False)
    tonnes_indicated = forms.DecimalField(label="Indicated resource (Mt)", initial=0, min_value=0, decimal_places=3, max_digits=12, required=False)
    tonnes_measured  = forms.DecimalField(label="Measured resource (Mt)",  initial=0, min_value=0, decimal_places=3, max_digits=12, required=False)
    tonnes_probable  = forms.DecimalField(label="Probable reserves (Mt)",  initial=0, min_value=0, decimal_places=3, max_digits=12, required=False)
    tonnes_proven    = forms.DecimalField(label="Proven reserves (Mt)",    initial=0, min_value=0, decimal_places=3, max_digits=12, required=False)

    opex_per_tonne = forms.DecimalField(
        label="Opex per tonne processed ($/t)",
        min_value=0, decimal_places=2, max_digits=8, initial=Decimal("25.00"),
        help_text="All-in operating cost per tonne milled: mining + processing + G&A.",
    )
    capex_millions = forms.DecimalField(
        label="Initial capex ($M)",
        min_value=0, decimal_places=2, max_digits=10, initial=Decimal("500.00"),
        help_text="Upfront capital for mine construction. Sustaining capex not modeled.",
    )
    mine_life_years = forms.IntegerField(
        label="Mine life (years)", min_value=1, max_value=50, initial=12,
    )
    discount_rate_pct = forms.DecimalField(
        label="Discount rate (%)",
        min_value=Decimal("0"), max_value=Decimal("25"),
        decimal_places=2, max_digits=5, initial=Decimal("8.00"),
    )
    shares_outstanding_m = forms.DecimalField(
        label="Shares outstanding, fully diluted (M)",
        min_value=Decimal("0.1"),
        decimal_places=3, max_digits=12, initial=Decimal("100.000"),
    )
    stage = forms.ChoiceField(
        label="Study stage", choices=STAGE_CHOICES, initial="PFS",
    )

    def clean(self):
        cleaned = super().clean()
        total_tonnes = sum(
            (cleaned.get(f, 0) or Decimal("0")) for f in (
                "tonnes_inferred", "tonnes_indicated", "tonnes_measured",
                "tonnes_probable", "tonnes_proven",
            )
        )
        if total_tonnes <= 0:
            raise forms.ValidationError(
                "Enter at least one non-zero resource or reserve tonnage."
            )
        return cleaned


class NavCalculatorCopperForm(_BaseNavForm):
    """Copper-specific: grade in %, price in $/lb."""
    grade_pct = forms.DecimalField(
        label="Copper grade (%)",
        min_value=Decimal("0.01"), decimal_places=3, max_digits=6,
        initial=Decimal("0.50"),
        help_text="Average copper grade. Typical range 0.2-2% for economic deposits.",
    )
    recovery_pct = forms.DecimalField(
        label="Metallurgical recovery (%)",
        min_value=Decimal("10"), max_value=Decimal("100"),
        decimal_places=1, max_digits=4, initial=Decimal("85.0"),
        help_text="Percentage of contained copper recovered during processing. Typical 80-92%.",
    )

    # Up to 4 price benchmarks
    price_label_1 = forms.CharField(label="Price label 1", initial="Current Spot", max_length=40, required=False)
    price_value_1 = forms.DecimalField(label="Copper price 1 ($/lb)", min_value=0, decimal_places=3, max_digits=8, required=False)
    price_label_2 = forms.CharField(label="Price label 2", initial="3-Month Average", max_length=40, required=False)
    price_value_2 = forms.DecimalField(label="Copper price 2 ($/lb)", min_value=0, decimal_places=3, max_digits=8, required=False)
    price_label_3 = forms.CharField(label="Price label 3", initial="12-Month Average", max_length=40, required=False)
    price_value_3 = forms.DecimalField(label="Copper price 3 ($/lb)", min_value=0, decimal_places=3, max_digits=8, required=False)
    price_label_4 = forms.CharField(label="Price label 4", initial="Long-term Deck", max_length=40, required=False)
    price_value_4 = forms.DecimalField(label="Copper price 4 ($/lb)", min_value=0, decimal_places=3, max_digits=8, required=False)

    def clean(self):
        cleaned = super().clean()
        prices = [cleaned.get(f"price_value_{i}") for i in range(1, 5)]
        if not any(p and p > 0 for p in prices):
            raise forms.ValidationError("Enter at least one copper price.")
        return cleaned

    def get_price_columns(self):
        cols = []
        for i in range(1, 5):
            price = self.cleaned_data.get(f"price_value_{i}")
            label = self.cleaned_data.get(f"price_label_{i}") or f"Price {i}"
            if price and price > 0:
                cols.append({"label": label, "price": price})
        return cols


class NavCalculatorSilverForm(_BaseNavForm):
    """Silver-specific: grade in g/t, price in $/oz. Same units as gold."""
    grade_gpt = forms.DecimalField(
        label="Silver grade (g/t)",
        min_value=Decimal("1"), decimal_places=2, max_digits=8,
        initial=Decimal("150.00"),
        help_text="Average silver grade. Typical range 50-500 g/t for economic silver deposits.",
    )
    recovery_pct = forms.DecimalField(
        label="Metallurgical recovery (%)",
        min_value=Decimal("10"), max_value=Decimal("100"),
        decimal_places=1, max_digits=4, initial=Decimal("82.0"),
        help_text="Typical 75-90% for silver; lower than gold due to more complex metallurgy.",
    )

    price_label_1 = forms.CharField(label="Price label 1", initial="Current Spot", max_length=40, required=False)
    price_value_1 = forms.DecimalField(label="Silver price 1 ($/oz)", min_value=0, decimal_places=2, max_digits=8, required=False)
    price_label_2 = forms.CharField(label="Price label 2", initial="3-Month Average", max_length=40, required=False)
    price_value_2 = forms.DecimalField(label="Silver price 2 ($/oz)", min_value=0, decimal_places=2, max_digits=8, required=False)
    price_label_3 = forms.CharField(label="Price label 3", initial="12-Month Average", max_length=40, required=False)
    price_value_3 = forms.DecimalField(label="Silver price 3 ($/oz)", min_value=0, decimal_places=2, max_digits=8, required=False)
    price_label_4 = forms.CharField(label="Price label 4", initial="Custom", max_length=40, required=False)
    price_value_4 = forms.DecimalField(label="Silver price 4 ($/oz)", min_value=0, decimal_places=2, max_digits=8, required=False)

    def clean(self):
        cleaned = super().clean()
        prices = [cleaned.get(f"price_value_{i}") for i in range(1, 5)]
        if not any(p and p > 0 for p in prices):
            raise forms.ValidationError("Enter at least one silver price.")
        return cleaned

    def get_price_columns(self):
        cols = []
        for i in range(1, 5):
            price = self.cleaned_data.get(f"price_value_{i}")
            label = self.cleaned_data.get(f"price_label_{i}") or f"Price {i}"
            if price and price > 0:
                cols.append({"label": label, "price": price})
        return cols


class NavCalculatorPolymetallicForm(_BaseNavForm):
    """
    Gold-copper-silver polymetallic deposits. Supports any combination —
    leave a grade at 0 to effectively ignore that commodity.

    Two price benchmarks per commodity (base + long-term) to keep the form
    manageable. The output matrix shows the two combined revenue scenarios.
    """
    # Gold
    gold_grade_gpt = forms.DecimalField(
        label="Gold grade (g/t)", min_value=0, decimal_places=3, max_digits=8,
        initial=Decimal("0.50"), required=False,
    )
    gold_recovery_pct = forms.DecimalField(
        label="Gold recovery (%)", min_value=0, max_value=Decimal("100"),
        decimal_places=1, max_digits=4, initial=Decimal("88.0"), required=False,
    )
    gold_price_base = forms.DecimalField(
        label="Gold base price ($/oz)", min_value=0, decimal_places=2, max_digits=8, initial=Decimal("4500.00"), required=False,
    )
    gold_price_longterm = forms.DecimalField(
        label="Gold long-term price ($/oz)", min_value=0, decimal_places=2, max_digits=8, initial=Decimal("3500.00"), required=False,
    )

    # Copper
    copper_grade_pct = forms.DecimalField(
        label="Copper grade (%)", min_value=0, decimal_places=3, max_digits=6,
        initial=Decimal("0.40"), required=False,
    )
    copper_recovery_pct = forms.DecimalField(
        label="Copper recovery (%)", min_value=0, max_value=Decimal("100"),
        decimal_places=1, max_digits=4, initial=Decimal("85.0"), required=False,
    )
    copper_price_base = forms.DecimalField(
        label="Copper base price ($/lb)", min_value=0, decimal_places=3, max_digits=8, initial=Decimal("5.50"), required=False,
    )
    copper_price_longterm = forms.DecimalField(
        label="Copper long-term price ($/lb)", min_value=0, decimal_places=3, max_digits=8, initial=Decimal("4.00"), required=False,
    )

    # Silver
    silver_grade_gpt = forms.DecimalField(
        label="Silver grade (g/t)", min_value=0, decimal_places=2, max_digits=8,
        initial=Decimal("0"), required=False,
    )
    silver_recovery_pct = forms.DecimalField(
        label="Silver recovery (%)", min_value=0, max_value=Decimal("100"),
        decimal_places=1, max_digits=4, initial=Decimal("75.0"), required=False,
    )
    silver_price_base = forms.DecimalField(
        label="Silver base price ($/oz)", min_value=0, decimal_places=2, max_digits=8, initial=Decimal("85.00"), required=False,
    )
    silver_price_longterm = forms.DecimalField(
        label="Silver long-term price ($/oz)", min_value=0, decimal_places=2, max_digits=8, initial=Decimal("55.00"), required=False,
    )

    def clean(self):
        cleaned = super().clean()
        # At least one commodity must have grade > 0
        grades = [
            cleaned.get("gold_grade_gpt") or Decimal("0"),
            cleaned.get("copper_grade_pct") or Decimal("0"),
            cleaned.get("silver_grade_gpt") or Decimal("0"),
        ]
        if not any(g > 0 for g in grades):
            raise forms.ValidationError(
                "Enter at least one non-zero commodity grade (gold, copper, or silver)."
            )
        return cleaned
