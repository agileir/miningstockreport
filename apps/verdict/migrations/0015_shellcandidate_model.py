from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("verdict", "0014_seed_tsxv_shell_candidates"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShellCandidate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ticker", models.CharField(max_length=20)),
                ("exchange", models.CharField(
                    choices=[
                        ("TSXV",  "TSX Venture (TSXV)"),
                        ("TSX",   "Toronto Stock Exchange (TSX)"),
                        ("CSE",   "Canadian Securities Exchange (CSE)"),
                        ("ASX",   "Australian Securities Exchange (ASX)"),
                        ("OTC",   "OTC Markets"),
                        ("NYSE",  "NYSE / NYSE American"),
                        ("LSE",   "London Stock Exchange (LSE)"),
                        ("OTHER", "Other"),
                    ],
                    max_length=10,
                )),
                ("name",    models.CharField(blank=True, max_length=200)),
                ("country", models.CharField(blank=True, default="Canada", max_length=100)),
                ("status",  models.CharField(
                    choices=[
                        ("dormant",       "Dormant (no recent volume)"),
                        ("watching",      "Watching (actively evaluating)"),
                        ("rto_completed", "RTO completed (became another company)"),
                        ("back_active",   "Resumed trading"),
                        ("delisted",      "Delisted from exchange"),
                        ("rejected",      "Not suitable for RTO"),
                    ],
                    db_index=True, default="dormant", max_length=20,
                )),
                ("last_known_price",    models.DecimalField(
                    blank=True, decimal_places=4, max_digits=10, null=True,
                    help_text="Last close price (CAD) at time of last verification.",
                )),
                ("avg_dollar_volume_5d", models.DecimalField(
                    blank=True, decimal_places=2, max_digits=14, null=True,
                    help_text="5-day avg dollar volume at time of last verification.",
                )),
                ("avg_share_volume_5d", models.PositiveBigIntegerField(
                    blank=True, null=True,
                    help_text="5-day avg share volume at time of last verification.",
                )),
                ("market_cap_cad", models.BigIntegerField(
                    blank=True, null=True,
                    help_text="Market cap in CAD at time of last verification.",
                )),
                ("listing_date", models.DateField(
                    blank=True, null=True,
                    help_text="When the shell first started trading on its exchange.",
                )),
                ("source", models.CharField(
                    blank=True, max_length=120,
                    help_text="Where this shell was identified (scan source + date).",
                )),
                ("notes", models.TextField(blank=True)),
                ("rto_target_name", models.CharField(
                    blank=True, max_length=200,
                    help_text="If RTO completed: the resulting company name.",
                )),
                ("verified_at", models.DateTimeField(
                    blank=True, null=True,
                    help_text="When the volume/price snapshot above was last refreshed.",
                )),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Shell candidate",
                "verbose_name_plural": "Shell candidates",
                "ordering": ["status", "exchange", "ticker"],
                "unique_together": {("ticker", "exchange")},
            },
        ),
        migrations.AddIndex(
            model_name="shellcandidate",
            index=models.Index(fields=["status", "exchange"], name="verdict_she_status_8f50a8_idx"),
        ),
    ]
