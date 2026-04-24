"""
Add CSE (Canadian Securities Exchange) to the Exchange choices on both
Company and CompanyQueue models. No data migration needed — this only
updates the `choices` attribute of the existing CharField, so the DB
schema is unchanged. Existing rows remain valid.
"""
from django.db import migrations, models


EXCHANGE_CHOICES = [
    ("TSXV",  "TSX Venture (TSXV)"),
    ("TSX",   "Toronto Stock Exchange (TSX)"),
    ("CSE",   "Canadian Securities Exchange (CSE)"),
    ("ASX",   "Australian Securities Exchange (ASX)"),
    ("OTC",   "OTC Markets"),
    ("NYSE",  "NYSE / NYSE American"),
    ("LSE",   "London Stock Exchange (LSE)"),
    ("OTHER", "Other"),
]


class Migration(migrations.Migration):

    dependencies = [
        ("verdict", "0007_seed_miningfeeds_queue"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="exchange",
            field=models.CharField(choices=EXCHANGE_CHOICES, max_length=10),
        ),
        migrations.AlterField(
            model_name="companyqueue",
            name="exchange",
            field=models.CharField(choices=EXCHANGE_CHOICES, max_length=10),
        ),
    ]
