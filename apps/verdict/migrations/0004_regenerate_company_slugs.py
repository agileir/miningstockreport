"""
Data migration: regenerate Company slugs from the name field.

Companies created before the AI agent filled in names got autoslug
fallback slugs like 'company-1', 'company-16', etc.  Now that names
are populated, regenerate proper slugs (e.g. 'banyan-gold-corp').
"""

from django.db import migrations
from django.utils.text import slugify


def regenerate_slugs(apps, schema_editor):
    Company = apps.get_model("verdict", "Company")
    used_slugs = set()

    for company in Company.objects.all():
        if not company.name:
            # No name to slug from — skip
            used_slugs.add(company.slug)
            continue

        base_slug = slugify(company.name)
        if not base_slug:
            used_slugs.add(company.slug)
            continue

        # Ensure uniqueness
        slug = base_slug
        counter = 2
        while slug in used_slugs or (
            Company.objects.filter(slug=slug).exclude(pk=company.pk).exists()
        ):
            slug = f"{base_slug}-{counter}"
            counter += 1

        company.slug = slug
        company.save(update_fields=["slug"])
        used_slugs.add(slug)


def noop(apps, schema_editor):
    pass  # No reverse — old slugs are not worth preserving


class Migration(migrations.Migration):

    dependencies = [
        ("verdict", "0003_company_data_filled_alter_exchange_name"),
    ]

    operations = [
        migrations.RunPython(regenerate_slugs, noop),
    ]
