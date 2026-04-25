"""
Seed TSXV dormant-shell candidates to CompanyQueue.

Targeted scan: 30 lowest-market-cap TSXV mining issuers from the TMX
March 2026 export ($150k - $1M market cap), Yahoo Finance volume-checked
on 2026-04-24. Of 30 candidates, 27 confirmed as dormant shells
(<$1k/day avg 5-day dollar volume). 3 had thin-but-real volume and
were left out (NED, INFM, DG — flagged for active-research consideration
in a future batch).

These names are listed but not actively trading. Useful for tracking
potential RTO (Reverse Takeover) candidates — clean shells with
exchange listing intact.
"""
from django.db import migrations


SOURCE = "TMX TSXV Mining Issuers March 2026 (shell candidate scan 2026-04-24)"


SHELLS = [
    {"ticker": "JHC",  "name": "Jinhua Capital Corporation",          "mcap_m": 0.15, "px": 0.025, "vol": 0},
    {"ticker": "SML",  "name": "Southstone Minerals Limited",         "mcap_m": 0.16, "px": 0.010, "vol": 0},
    {"ticker": "PGP",  "name": "Power Group Projects Corp.",          "mcap_m": 0.25, "px": 0.020, "vol": 0},
    {"ticker": "AVX",  "name": "Altair Resources Inc.",               "mcap_m": 0.29, "px": 0.010, "vol": 0},
    {"ticker": "EON",  "name": "EON Lithium Corp.",                   "mcap_m": 0.35, "px": 0.020, "vol": 0},
    {"ticker": "NTB",  "name": "New Tymbal Resources Ltd.",           "mcap_m": 0.36, "px": 0.040, "vol": 0},
    {"ticker": "IRI",  "name": "IEMR Resources Inc.",                 "mcap_m": 0.47, "px": 0.015, "vol": 0},
    {"ticker": "KLM",  "name": "Kermode Resources Ltd.",              "mcap_m": 0.51, "px": 0.010, "vol": 6},
    {"ticker": "HAWK", "name": "Hawkeye Gold & Diamond Inc.",         "mcap_m": 0.52, "px": 0.045, "vol": 90},
    {"ticker": "WMS",  "name": "Western Metallica Resources Corp.",   "mcap_m": 0.55, "px": 0.040, "vol": 322},
    {"ticker": "BIGT", "name": "Big Tree Carbon Inc.",                "mcap_m": 0.60, "px": 0.010, "vol": 430},
    {"ticker": "RTM",  "name": "RT Minerals Corp.",                   "mcap_m": 0.63, "px": 0.055, "vol": 0},
    {"ticker": "TKU",  "name": "Tarku Resources Ltd.",                "mcap_m": 0.63, "px": 0.010, "vol": 0},
    {"ticker": "DCY",  "name": "Discovery-Corp Enterprises Inc.",     "mcap_m": 0.67, "px": 0.070, "vol": 0},
    {"ticker": "ALT",  "name": "Alturas Minerals Corp.",              "mcap_m": 0.73, "px": 0.015, "vol": 108},
    {"ticker": "GER",  "name": "Glen Eagle Resources Inc.",           "mcap_m": 0.73, "px": 0.010, "vol": 0},
    {"ticker": "VAX",  "name": "Vantex Resources Ltd.",               "mcap_m": 0.77, "px": 0.150, "vol": 300},
    {"ticker": "VCV",  "name": "Vatic Ventures Corp.",                "mcap_m": 0.83, "px": 0.025, "vol": 0},
    {"ticker": "WRI",  "name": "Waseco Resources Inc.",               "mcap_m": 0.83, "px": 0.020, "vol": 0},
    {"ticker": "ATI",  "name": "Altai Resources Inc.",                "mcap_m": 0.84, "px": 0.035, "vol": 0},
    {"ticker": "PWH",  "name": "Purewave Hydrogen Corp.",             "mcap_m": 0.89, "px": 0.025, "vol": 0},
    {"ticker": "AVR",  "name": "Avaron Mining Corp.",                 "mcap_m": 0.90, "px": 0.060, "vol": 0},
    {"ticker": "BST",  "name": "Bessor Minerals Inc.",                "mcap_m": 0.94, "px": 0.040, "vol": 0},
    {"ticker": "CTN",  "name": "Centurion Minerals Ltd.",             "mcap_m": 0.96, "px": 0.050, "vol": 40},
    {"ticker": "PWRO", "name": "Power One Resources Corp.",           "mcap_m": 1.00, "px": 0.025, "vol": 637},
    {"ticker": "LKY",  "name": "Lucky Minerals Inc.",                 "mcap_m": 1.01, "px": 0.005, "vol": 0},
    {"ticker": "HANS", "name": "Hanstone Gold Corp.",                 "mcap_m": 1.03, "px": 0.025, "vol": 102},
]


def seed(apps, schema_editor):
    CompanyQueue = apps.get_model("verdict", "CompanyQueue")
    for s in SHELLS:
        if CompanyQueue.objects.filter(ticker=s["ticker"], exchange="TSXV").exists():
            CompanyQueue.objects.filter(ticker=s["ticker"], exchange="TSXV").update(
                status="shell_candidate",
            )
            continue
        CompanyQueue.objects.create(
            ticker=s["ticker"],
            exchange="TSXV",
            name=s["name"],
            primary_commodity="",
            country="Canada",
            status="shell_candidate",
            source=SOURCE,
            notes=(
                f"TSXV mining shell. Mkt cap ~${s['mcap_m']:.2f}M. "
                f"5d avg dollar volume ~${s['vol']:,}/day at last px ${s['px']:.3f}. "
                f"Potential RTO candidate — verify share count, working capital, "
                f"and any stranded NOLs before considering."
            ),
        )


def reverse(apps, schema_editor):
    CompanyQueue = apps.get_model("verdict", "CompanyQueue")
    CompanyQueue.objects.filter(source=SOURCE, status="shell_candidate").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("verdict", "0013_shell_candidate_status_and_seed"),
    ]
    operations = [
        migrations.RunPython(seed, reverse),
    ]
