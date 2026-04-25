"""
CSE mining batch 2 — 2 verified-active tickers seeded to CompanyQueue.

From the next 10 newest CSE listings after batch 1, only 2 cleared the
$1k/day avg dollar volume threshold (most newly-listed CSE names are
either too new for Yahoo to index or trading at zero/near-zero volume).
"""
from django.db import migrations


SOURCE = "thecse.com/industry/mining 2026-04-24 (batch 2)"


ENTRIES = [
    {"ticker": "GC",   "name": "Goldcana Resources Inc.",
     "primary_commodity": "Gold", "country": "Canada",
     "notes": "CSE Tier 2. Listed 2025-08-13. 5d avg $vol ~$1,022/day. Borderline-active."},
    {"ticker": "LIBR", "name": "Libra Energy Materials Inc.",
     "primary_commodity": "Lithium", "country": "Canada",
     "notes": "CSE Tier 2. Listed 2025-07-10. 5d avg $vol ~$6,890/day. Battery metals / lithium."},
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
    CompanyQueue.objects.filter(
        ticker__in=[r["ticker"] for r in ENTRIES],
        source=SOURCE,
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("verdict", "0010_seed_tmx_batch1"),
    ]
    operations = [
        migrations.RunPython(seed, reverse),
    ]
