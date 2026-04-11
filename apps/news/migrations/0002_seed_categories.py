from django.db import migrations


CATEGORIES = [
    {"name": "Gold & Silver", "slug": "gold-silver", "icon_class": "bi-gem", "sort_order": 1},
    {"name": "Copper & Base Metals", "slug": "copper-base-metals", "icon_class": "bi-minecart-loaded", "sort_order": 2},
    {"name": "Lithium & Battery Metals", "slug": "lithium-battery-metals", "icon_class": "bi-battery-charging", "sort_order": 3},
    {"name": "Exploration & Discovery", "slug": "exploration-discovery", "icon_class": "bi-binoculars", "sort_order": 4},
    {"name": "M&A & Deals", "slug": "mergers-acquisitions", "icon_class": "bi-briefcase", "sort_order": 5},
    {"name": "Market & Macro", "slug": "market-macro", "icon_class": "bi-graph-up-arrow", "sort_order": 6},
    {"name": "Uranium & Energy", "slug": "uranium-energy", "icon_class": "bi-lightning-charge", "sort_order": 7},
    {"name": "Opinion & Analysis", "slug": "opinion-analysis", "icon_class": "bi-chat-quote", "sort_order": 8},
]


def seed_categories(apps, schema_editor):
    NewsCategory = apps.get_model("news", "NewsCategory")
    for cat in CATEGORIES:
        NewsCategory.objects.get_or_create(slug=cat["slug"], defaults=cat)


def unseed_categories(apps, schema_editor):
    NewsCategory = apps.get_model("news", "NewsCategory")
    slugs = [c["slug"] for c in CATEGORIES]
    NewsCategory.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_categories, unseed_categories),
    ]
