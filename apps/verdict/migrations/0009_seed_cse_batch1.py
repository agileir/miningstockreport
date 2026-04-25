"""
Seed CompanyQueue with first batch of CSE mining listings verified as
active (>$500/day avg 5-day dollar volume on Yahoo Finance, symbol.CN).

Source: thecse.com/industry/mining export (2026-04-24). Full 366-row
list saved at research_queue/cse_mining_source.json for future batches.
Volume-check results at research_queue/cse_batch1_volume_check.json.

Of 15 newest-listed CSE mining tickers sampled:
  - 7 ACTIVE (seeded here with status=active)
  - 3 NOT FOUND on Yahoo (too new to index; retry next batch)
  - 2 LOW_VOL (<$500/day; skipped)
  - 2 NO_VOL (dormant; skipped)
  - 1 warrant (CAT.WT; not a share, skipped)
"""
from django.db import migrations


SOURCE = "thecse.com/industry/mining 2026-04-24"


ENTRIES = [
    {
        "ticker": "NUCA", "name": "Americas Uranium Corp.",
        "primary_commodity": "Uranium", "country": "Canada",
        "notes": "CSE Tier 2. Listed 2026-03-31. 5d avg volume ~7,223 shares @ $0.25 (~$1,806/day). Formerly Allied Strategic Resources."
    },
    {
        "ticker": "ICG", "name": "ICG Silver Gold Ltd.",
        "primary_commodity": "Silver", "country": "Canada",
        "notes": "CSE Tier 2. Listed 2026-03-31. 5d avg volume ~33,207 shares @ $0.50 (~$16,603/day). Strongest volume in the batch."
    },
    {
        "ticker": "OROG", "name": "Gold Orogen Resources Corp.",
        "primary_commodity": "Gold", "country": "Canada",
        "notes": "CSE Tier 2. Listed 2026-03-02. 5d avg volume ~141,432 shares @ $0.065 (~$9,193/day). High share volume, low price."
    },
    {
        "ticker": "BMT", "name": "Bahia Metals Corp.",
        "primary_commodity": "", "country": "Canada",
        "notes": "CSE Tier 2. Listed 2026-02-12. 5d avg volume ~20,200 shares @ $0.42 (~$8,484/day). Primary commodity to be filled by data-fill agent."
    },
    {
        "ticker": "MM", "name": "Maximus Metals Inc.",
        "primary_commodity": "", "country": "Canada",
        "notes": "CSE Tier 2. Listed 2026-02-06. 5d avg volume ~121,000 shares @ $0.26 (~$31,460/day). Primary commodity to be filled by data-fill agent."
    },
    {
        "ticker": "UG", "name": "Upside Gold Corp.",
        "primary_commodity": "Gold", "country": "Canada",
        "notes": "CSE Tier 2. Listed 2026-01-05. 5d avg volume ~27,448 shares @ $1.50 (~$41,172/day). Highest dollar volume in batch."
    },
    {
        "ticker": "STNG", "name": "Stinger Resources Inc.",
        "primary_commodity": "", "country": "Canada",
        "notes": "CSE Tier 2. Listed 2025-11-10. 5d avg volume ~9,920 shares @ $0.075 (~$744/day). Borderline active; thin trading."
    },
]


def seed(apps, schema_editor):
    CompanyQueue = apps.get_model("verdict", "CompanyQueue")
    for row in ENTRIES:
        if CompanyQueue.objects.filter(ticker=row["ticker"], exchange="CSE").exists():
            continue
        CompanyQueue.objects.create(
            ticker=row["ticker"],
            exchange="CSE",
            name=row["name"],
            primary_commodity=row.get("primary_commodity", ""),
            country=row.get("country", "Canada"),
            status="active",
            source=SOURCE,
            notes=row.get("notes", ""),
        )


def reverse(apps, schema_editor):
    CompanyQueue = apps.get_model("verdict", "CompanyQueue")
    tickers = [r["ticker"] for r in ENTRIES]
    CompanyQueue.objects.filter(ticker__in=tickers, exchange="CSE").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("verdict", "0008_add_cse_exchange"),
    ]
    operations = [
        migrations.RunPython(seed, reverse),
    ]
