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
        help_text="Average grade across the deposit in grams per tonne.",
    )
    recovery_pct = forms.DecimalField(
        label="Metallurgical recovery (%)",
        min_value=Decimal("10"),
        max_value=Decimal("100"),
        decimal_places=1,
        max_digits=4,
        initial=Decimal("90.0"),
        help_text="Percentage of contained gold expected to be recovered during processing. Typical 85-95% for heap leach, 90-96% for CIL/CIP.",
    )

    # ── Operating inputs ──
    opex_per_tonne = forms.DecimalField(
        label="Opex per tonne processed ($/t)",
        min_value=0,
        decimal_places=2,
        max_digits=8,
        initial=Decimal("40.00"),
        help_text="All-in operating cost per tonne milled: mining + processing + G&A.",
    )
    capex_millions = forms.DecimalField(
        label="Initial capex ($M)",
        min_value=0,
        decimal_places=2,
        max_digits=10,
        initial=Decimal("500.00"),
        help_text="Upfront capital for mine construction. Sustaining capex not modeled in V1.",
    )
    mine_life_years = forms.IntegerField(
        label="Mine life (years)",
        min_value=1,
        max_value=50,
        initial=10,
    )

    # ── Financial inputs ──
    discount_rate_pct = forms.DecimalField(
        label="Discount rate (%)",
        min_value=Decimal("0"),
        max_value=Decimal("25"),
        decimal_places=2,
        max_digits=5,
        initial=Decimal("8.00"),
        help_text="Typically 5% for a producer, 8% for a developer, 10%+ for an explorer.",
    )
    shares_outstanding_m = forms.DecimalField(
        label="Shares outstanding, fully diluted (M)",
        min_value=Decimal("0.1"),
        decimal_places=3,
        max_digits=12,
        initial=Decimal("100.000"),
        help_text="Millions of shares fully diluted, including warrants and options.",
    )

    # ── Study stage ──
    stage = forms.ChoiceField(
        label="Study stage",
        choices=STAGE_CHOICES,
        initial="PFS",
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
