from django.db import migrations


def seed_pillars(apps, schema_editor):
    Pillar = apps.get_model("blog", "Pillar")
    pillars = [
        {"name": "Due Diligence", "slug": "due-diligence",
         "description": "How to evaluate junior mining stocks: reading technical reports, NI 43-101, geology fundamentals, and resource estimation.",
         "sort_order": 1},
        {"name": "Company Verdicts", "slug": "company-verdicts",
         "description": "In-depth junior mining company analysis with scored verdicts using the 5-factor Verdict Framework.",
         "sort_order": 2},
        {"name": "Market Intelligence", "slug": "market-intelligence",
         "description": "Macro analysis, catalyst calendars, M&A activity, and market trends affecting junior mining stocks.",
         "sort_order": 3},
        {"name": "Market Commentary", "slug": "market-commentary",
         "description": "Weekly market commentary, portfolio updates, and sector analysis for junior mining investors.",
         "sort_order": 4},
    ]
    for p in pillars:
        Pillar.objects.get_or_create(slug=p["slug"], defaults=p)


def reverse_seed(apps, schema_editor):
    Pillar = apps.get_model("blog", "Pillar")
    Pillar.objects.filter(slug__in=[
        "due-diligence", "company-verdicts", "market-intelligence", "market-commentary"
    ]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_pillar_and_more"),
    ]
    operations = [
        migrations.RunPython(seed_pillars, reverse_seed),
    ]
