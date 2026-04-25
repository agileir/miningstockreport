"""
TMX TSX/TSXV mining batch 2 — 14 verified-active tickers.

Top 15 by market cap from the new-only TMX pool, plus TECK retry as
TECK.B (the TSX dual-class voting ticker — root "TECK" doesn't index
on Yahoo because the company trades TECK.A and TECK.B separately).

Of 15 candidates: 13 active immediately, TECK active under TECK.B,
1 (FOM Foran Mining) returned NO_DATA on Yahoo and was deferred.
"""
from django.db import migrations


SOURCE = "TMX TSX/TSXV Mining Issuers March 2026 (batch 2)"


ENTRIES = [
    {"ticker": "TECK.B", "exchange": "TSX", "name": "Teck Resources Limited",
     "primary_commodity": "Copper", "jurisdiction": "Canada (BC)",
     "notes": "TSX senior. Mkt cap ~$35.3B. 5d avg $vol ~$81M (as TECK-B.TO on Yahoo). TSX dual-class — TECK.A is voting, TECK.B is the more-liquid common. Copper, zinc, met coal."},
    {"ticker": "AAUC", "exchange": "TSX", "name": "Allied Gold Corporation",
     "primary_commodity": "Gold", "jurisdiction": "West Africa, Egypt",
     "notes": "TSX senior. Mkt cap ~$5.6B. 5d avg $vol ~$18M. Sadiola, Bonikro, Kurmuk operations."},
    {"ticker": "WGX", "exchange": "TSX", "name": "Westgold Resources Limited",
     "primary_commodity": "Gold", "jurisdiction": "Australia",
     "notes": "TSX-listed (ASX-primary dual listing). Mkt cap ~$5.5B. 5d avg $vol ~$726k on TSX. WA gold operations."},
    {"ticker": "NGEX", "exchange": "TSX", "name": "NGEx Minerals Ltd.",
     "primary_commodity": "Copper", "jurisdiction": "Argentina, Chile",
     "notes": "TSX senior. Mkt cap ~$5.5B. 5d avg $vol ~$8M. Lunahuasi (Argentina) copper-gold-silver discovery."},
    {"ticker": "ARIS", "exchange": "TSX", "name": "Aris Mining Corporation",
     "primary_commodity": "Gold", "jurisdiction": "Colombia",
     "notes": "TSX senior. Mkt cap ~$5.3B. 5d avg $vol ~$18M. Segovia and Marmato operations in Colombia."},
    {"ticker": "PDN", "exchange": "TSX", "name": "Paladin Energy Ltd.",
     "primary_commodity": "Uranium", "jurisdiction": "Namibia, Canada",
     "notes": "TSX senior (ASX-primary). Mkt cap ~$5.0B. 5d avg $vol ~$1.8M on TSX. Langer Heinrich (Namibia) restart + Fission acquisition."},
    {"ticker": "PPTA", "exchange": "TSX", "name": "Perpetua Resources Corp.",
     "primary_commodity": "Gold", "jurisdiction": "Idaho, USA",
     "notes": "TSX senior. Mkt cap ~$4.9B. 5d avg $vol ~$5.3M. Stibnite gold-antimony project — strategic-metal exposure."},
    {"ticker": "ERO", "exchange": "TSX", "name": "Ero Copper Corp.",
     "primary_commodity": "Copper", "jurisdiction": "Brazil",
     "notes": "TSX senior. Mkt cap ~$3.9B. 5d avg $vol ~$16M. MCSA (Caraíba) and Tucumã copper operations in Brazil."},
    {"ticker": "CIA", "exchange": "TSX", "name": "Champion Iron Limited",
     "primary_commodity": "Iron Ore", "jurisdiction": "Quebec, Canada",
     "notes": "TSX senior (ASX-primary). Mkt cap ~$2.7B. 5d avg $vol ~$1.6M on TSX. Bloom Lake high-grade DR-pellet feed iron ore."},
    {"ticker": "IE", "exchange": "TSX", "name": "Ivanhoe Electric Inc.",
     "primary_commodity": "Copper", "jurisdiction": "USA",
     "notes": "TSX senior. Mkt cap ~$2.6B. 5d avg $vol ~$576k. Santa Cruz copper project (Arizona) plus Typhoon proprietary geophysics."},
    {"ticker": "USA", "exchange": "TSX", "name": "Americas Gold and Silver Corporation",
     "primary_commodity": "Silver", "jurisdiction": "Mexico, USA",
     "notes": "TSX senior. Mkt cap ~$2.3B. 5d avg $vol ~$14M. Cosalá (Mexico) and Galena (Idaho) operations."},
    {"ticker": "SXGC", "exchange": "TSX", "name": "Southern Cross Gold Consolidated Ltd.",
     "primary_commodity": "Gold", "jurisdiction": "Australia",
     "notes": "TSX senior (ASX-primary). Mkt cap ~$2.3B. 5d avg $vol ~$5.2M on TSX. Sunday Creek gold-antimony project (Victoria, AU)."},
    {"ticker": "LUNR", "exchange": "TSXV", "name": "LunR Royalties Corp.",
     "primary_commodity": "Gold", "jurisdiction": "Global (royalty)",
     "notes": "TSX-V. Mkt cap ~$2.1B. 5d avg $vol ~$2.3M. Royalty / streaming portfolio."},
    {"ticker": "ABRA", "exchange": "TSX", "name": "AbraSilver Resource Corp.",
     "primary_commodity": "Silver", "jurisdiction": "Argentina",
     "notes": "TSX senior (graduated from TSXV). Mkt cap ~$2.0B. 5d avg $vol ~$11M. Diablillos silver-gold project (Salta, AR)."},
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
    CompanyQueue.objects.filter(
        source=SOURCE,
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("verdict", "0011_seed_cse_batch2"),
    ]
    operations = [
        migrations.RunPython(seed, reverse),
    ]
