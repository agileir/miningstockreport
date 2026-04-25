"""
Seed CompanyQueue with first batch of TSX/TSXV mining tickers verified
active (>$1000/day avg 5-day dollar volume on Yahoo Finance).

Source: TMX Group "Mining Companies Listed on TSX and TSXV" export
(March 2026 MM Issuers report). Full 1,082-row dataset saved at
research_queue/tmx_mining_source.json for future batches.

Of 1,082 TSX+TSXV mining issuers, 207 were already in our Company or
CompanyQueue tables (skipped). Of the 966 new tickers, batch 1 took
the top 15 by market cap. 14 verified active on Yahoo Finance; one
(TECK) deferred due to Yahoo class-A/B ticker split.
"""
from django.db import migrations


SOURCE = "TMX TSX/TSXV Mining Issuers March 2026"


ENTRIES = [
    {"ticker": "NTR",   "exchange": "TSX", "name": "Nutrien Ltd.",                      "primary_commodity": "Potash",   "jurisdiction": "Canada (SK)",
     "notes": "TSX senior. Mkt cap ~$50.5B. 5d avg $vol ~$138M. World's largest potash producer; classified as Mining by TMX."},
    {"ticker": "EDV",   "exchange": "TSX", "name": "Endeavour Mining plc",              "primary_commodity": "Gold",     "jurisdiction": "West Africa",
     "notes": "TSX senior. Mkt cap ~$20.2B. 5d avg $vol ~$52M. Burkina Faso / Côte d'Ivoire / Senegal operations."},
    {"ticker": "CDE",   "exchange": "TSX", "name": "Coeur Mining, Inc.",                "primary_commodity": "Silver",   "jurisdiction": "Americas",
     "notes": "TSX senior (US-domiciled). Mkt cap ~$16.7B. 5d avg $vol ~$8.9M. Silver-primary with meaningful gold byproduct."},
    {"ticker": "AG",    "exchange": "TSX", "name": "First Majestic Silver Corp.",       "primary_commodity": "Silver",   "jurisdiction": "Mexico",
     "notes": "TSX senior. Mkt cap ~$14.7B. 5d avg $vol ~$44M. Mexican silver producer."},
    {"ticker": "GMIN",  "exchange": "TSX", "name": "G Mining Ventures Corp.",           "primary_commodity": "Gold",     "jurisdiction": "Brazil",
     "notes": "TSX senior. Mkt cap ~$11.6B. 5d avg $vol ~$30M. Tocantinzinho gold project in Brazil."},
    {"ticker": "TFPM",  "exchange": "TSX", "name": "Triple Flag Precious Metals Corp.", "primary_commodity": "Gold",     "jurisdiction": "Global (royalty)",
     "notes": "TSX senior. Mkt cap ~$10.0B. 5d avg $vol ~$7.1M. Royalty / streaming company — gold-silver diversified stream book."},
    {"ticker": "SSRM",  "exchange": "TSX", "name": "SSR Mining Inc.",                   "primary_commodity": "Gold",     "jurisdiction": "Americas, Türkiye",
     "notes": "TSX senior. Mkt cap ~$8.8B. 5d avg $vol ~$17M. Multi-asset producer; post-Çöpler-incident recovery story."},
    {"ticker": "OLA",   "exchange": "TSX", "name": "Orla Mining Ltd.",                  "primary_commodity": "Gold",     "jurisdiction": "Mexico, USA",
     "notes": "TSX senior. Mkt cap ~$7.7B. 5d avg $vol ~$22M. Camino Rojo (Mexico) producer plus Musselwhite acquisition in Ontario."},
    {"ticker": "DSV",   "exchange": "TSX", "name": "Discovery Silver Corp.",            "primary_commodity": "Silver",   "jurisdiction": "Mexico, Canada",
     "notes": "TSX senior. Mkt cap ~$7.2B. 5d avg $vol ~$27M. Cordero (Mexico) silver development plus Porcupine gold acquisition."},
    {"ticker": "PRU",   "exchange": "TSX", "name": "Perseus Mining Limited",            "primary_commodity": "Gold",     "jurisdiction": "West Africa",
     "notes": "TSX senior (ASX-primary dual listing). Mkt cap ~$6.9B. 5d avg $vol ~$197k on TSX. Côte d'Ivoire / Ghana operations."},
    {"ticker": "EFR",   "exchange": "TSX", "name": "Energy Fuels Inc.",                 "primary_commodity": "Uranium",  "jurisdiction": "USA",
     "notes": "TSX senior. Mkt cap ~$6.1B. 5d avg $vol ~$35M. US uranium + rare-earth separation at White Mesa Mill."},
    {"ticker": "MAU",   "exchange": "TSX", "name": "Montage Gold Corp.",                "primary_commodity": "Gold",     "jurisdiction": "Côte d'Ivoire",
     "notes": "TSX senior. Mkt cap ~$5.8B. 5d avg $vol ~$13M. Koné project development in Côte d'Ivoire."},
    {"ticker": "KNT",   "exchange": "TSX", "name": "K92 Mining Inc.",                   "primary_commodity": "Gold",     "jurisdiction": "Papua New Guinea",
     "notes": "TSX senior. Mkt cap ~$5.8B. 5d avg $vol ~$17M. Kainantu mine (PNG) — high-grade gold producer."},
    {"ticker": "AII",   "exchange": "TSX", "name": "Almonty Industries Inc.",           "primary_commodity": "Tungsten", "jurisdiction": "South Korea, Portugal",
     "notes": "TSX senior. Mkt cap ~$5.7B. 5d avg $vol ~$18M. Tungsten producer — Sangdong (South Korea) ramp-up. Strategic-metal exposure."},
]


def seed(apps, schema_editor):
    CompanyQueue = apps.get_model("verdict", "CompanyQueue")
    for row in ENTRIES:
        if CompanyQueue.objects.filter(ticker=row["ticker"], exchange=row["exchange"]).exists():
            continue
        CompanyQueue.objects.create(
            ticker=row["ticker"],
            exchange=row["exchange"],
            name=row["name"],
            primary_commodity=row.get("primary_commodity", ""),
            country=row.get("jurisdiction", ""),
            status="active",
            source=SOURCE,
            notes=row.get("notes", ""),
        )


def reverse(apps, schema_editor):
    CompanyQueue = apps.get_model("verdict", "CompanyQueue")
    tickers = [r["ticker"] for r in ENTRIES]
    CompanyQueue.objects.filter(ticker__in=tickers, source=SOURCE).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("verdict", "0009_seed_cse_batch1"),
    ]
    operations = [
        migrations.RunPython(seed, reverse),
    ]
