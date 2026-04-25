"""
Add SHELL_CANDIDATE status to CompanyQueue and seed initial CSE shell list.

Shell candidates are CSE-listed mining companies that are still actively
listed on the exchange but have effectively dormant trading volume — the
classic profile for a Reverse Takeover (RTO) target. Tracked here so
they're searchable later when looking for clean shells.

Initial seed: 13 confirmed shells from CSE volume analysis on 2026-04-24:
  - 8 from a sample of the 24 oldest CSE mining listings (10-year-old
    listings with high dormant-shell rates)
  - 5 from the prior batch-1 / batch-2 active-ticker analysis (newer
    listings that are nominally listed but have <$1k/day avg volume)

The shells column in research_queue/cse_shell_candidates.json holds the
volume metrics captured at scan time.
"""
from django.db import migrations, models


STATUS_CHOICES = [
    ("pending",         "Pending verification"),
    ("active",          "Active — ready to promote"),
    ("promoted",        "Promoted to Company"),
    ("shell_candidate", "Shell candidate (dormant; potential RTO)"),
    ("delisted",        "Delisted"),
    ("acquired",        "Acquired"),
    ("out_of_scope",    "Out of scope (exchange)"),
    ("rejected",        "Rejected"),
]


SOURCE = "thecse.com/industry/mining 2026-04-24 (shell candidate scan)"


SHELLS = [
    {"ticker": "JJJ",  "name": "37 Capital Inc.",                     "since": "2015-09-01", "px": 0.045, "vol": 981},
    {"ticker": "CACR", "name": "The Canadian Chrome Company Inc.",    "since": "2015-09-01", "px": 0.010, "vol": 818},
    {"ticker": "UE",   "name": "Urano Energy Corp.",                  "since": "2015-09-02", "px": 0.080, "vol": 784},
    {"ticker": "AWR",  "name": "Aurwest Resources Corporation",       "since": "2015-09-09", "px": 0.015, "vol": 443},
    {"ticker": "PSE",  "name": "Pasinex Resources Limited",           "since": "2015-09-11", "px": 0.080, "vol": 840},
    {"ticker": "RXM",  "name": "Rockex Mining Corporation",           "since": "2015-09-14", "px": 0.035, "vol": 0},
    {"ticker": "ACRE", "name": "American Critical Elements Inc.",     "since": "2015-09-17", "px": 0.110, "vol": 0},
    {"ticker": "TAI",  "name": "Talmora Diamond Inc.",                "since": "2015-09-24", "px": 0.020, "vol": 0},
    {"ticker": "ELYX", "name": "Elysian Mineral Exploration Corp.",   "since": "2026-04-02", "px": 0.250, "vol": 62},
    {"ticker": "BEAU", "name": "Beaumont Exploration Corp.",          "since": "2026-02-26", "px": 0.200, "vol": 20},
    {"ticker": "C",    "name": "Commodore Metals Corp.",              "since": "2025-09-29", "px": 0.500, "vol": 0},
    {"ticker": "SL",   "name": "Super Lithium Corp.",                 "since": "2025-09-03", "px": 0.600, "vol": 0},
    {"ticker": "AA",   "name": "Avventura Resources Ltd.",            "since": "2025-08-26", "px": 0.090, "vol": 92},
]


def seed(apps, schema_editor):
    CompanyQueue = apps.get_model("verdict", "CompanyQueue")
    for s in SHELLS:
        if CompanyQueue.objects.filter(ticker=s["ticker"], exchange="CSE").exists():
            # Already in queue under a different status — flip to shell_candidate
            qs = CompanyQueue.objects.filter(ticker=s["ticker"], exchange="CSE")
            qs.update(status="shell_candidate")
            continue
        CompanyQueue.objects.create(
            ticker=s["ticker"],
            exchange="CSE",
            name=s["name"],
            primary_commodity="",
            country="Canada",
            status="shell_candidate",
            source=SOURCE,
            notes=(
                f"CSE Tier 2 mining shell. Listed since {s['since']}. "
                f"5d avg dollar volume ~${s['vol']:,}/day at last px ${s['px']:.3f}. "
                f"Potential RTO candidate — check share count, cap structure, and any "
                f"residual cash before considering."
            ),
        )


def reverse(apps, schema_editor):
    CompanyQueue = apps.get_model("verdict", "CompanyQueue")
    CompanyQueue.objects.filter(
        source=SOURCE,
        status="shell_candidate",
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("verdict", "0012_seed_tmx_batch2"),
    ]

    operations = [
        migrations.AlterField(
            model_name="companyqueue",
            name="status",
            field=models.CharField(
                choices=STATUS_CHOICES,
                db_index=True,
                default="pending",
                max_length=20,
            ),
        ),
        migrations.RunPython(seed, reverse),
    ]
