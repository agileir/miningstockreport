from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("verdict", "0005_company_tier"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompanyQueue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ticker", models.CharField(max_length=20)),
                ("exchange", models.CharField(
                    choices=[
                        ("TSXV", "TSX Venture (TSXV)"),
                        ("TSX", "Toronto Stock Exchange (TSX)"),
                        ("ASX", "Australian Securities Exchange (ASX)"),
                        ("OTC", "OTC Markets"),
                        ("NYSE", "NYSE / NYSE American"),
                        ("LSE", "London Stock Exchange (LSE)"),
                        ("OTHER", "Other"),
                    ],
                    max_length=10,
                )),
                ("name", models.CharField(blank=True, max_length=200)),
                ("primary_commodity", models.CharField(blank=True, max_length=50)),
                ("country", models.CharField(
                    blank=True, max_length=100,
                    help_text="Country of primary operations",
                )),
                ("status", models.CharField(
                    choices=[
                        ("pending", "Pending verification"),
                        ("active", "Active — ready to promote"),
                        ("promoted", "Promoted to Company"),
                        ("delisted", "Delisted"),
                        ("acquired", "Acquired"),
                        ("out_of_scope", "Out of scope (exchange)"),
                        ("rejected", "Rejected"),
                    ],
                    db_index=True, default="pending", max_length=20,
                )),
                ("source", models.CharField(
                    blank=True, max_length=100,
                    help_text=(
                        "Where this ticker was sourced from (e.g. 'miningfeeds.com/gold')."
                    ),
                )),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("company", models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name="queue_entries",
                    to="verdict.company",
                    help_text="Set when this queue entry is promoted to a Company record.",
                )),
            ],
            options={
                "verbose_name": "Company queue entry",
                "verbose_name_plural": "Company queue",
                "ordering": ["status", "ticker"],
                "unique_together": {("ticker", "exchange")},
            },
        ),
        migrations.AddIndex(
            model_name="companyqueue",
            index=models.Index(fields=["status", "exchange"], name="verdict_com_status_cb3f39_idx"),
        ),
    ]
