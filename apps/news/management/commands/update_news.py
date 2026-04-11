"""
Management command to ingest curated news links from the Claude agent.

Usage:
    echo '[{"headline":"...", "url":"...", ...}]' | python manage.py update_news --source agent
    python manage.py update_news --file /tmp/news.json --source agent
"""
import json
import sys
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.news.models import NewsCategory, NewsLink, AddedBy, hash_url


# Categories that get shorter expiry (more time-sensitive)
SHORT_EXPIRY_SLUGS = {"market-macro"}
DEFAULT_EXPIRY_HOURS = 48
SHORT_EXPIRY_HOURS = 24
FEATURED_EXPIRY_HOURS = 72
MAX_FEATURED = 3


class Command(BaseCommand):
    help = "Ingest curated news links from JSON (stdin or file)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--source", choices=["agent", "manual"], default="agent",
            help="Who added these links",
        )
        parser.add_argument(
            "--file", type=str, default=None,
            help="Path to JSON file (reads stdin if omitted)",
        )

    def handle(self, *args, **options):
        source = options["source"]

        if options["file"]:
            with open(options["file"], "r") as f:
                raw = f.read()
        else:
            raw = sys.stdin.read()

        try:
            items = json.loads(raw)
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f"Invalid JSON: {e}"))
            return

        if not isinstance(items, list):
            self.stderr.write(self.style.ERROR("JSON must be an array of objects"))
            return

        now = timezone.now()
        categories = {c.slug: c for c in NewsCategory.objects.all()}
        created = 0
        skipped = 0

        for item in items:
            url = item.get("url", "").strip()
            headline = item.get("headline", "").strip()
            if not url or not headline:
                continue

            url_hash_val = hash_url(url)

            if NewsLink.objects.filter(url_hash=url_hash_val).exists():
                skipped += 1
                continue

            cat_slug = item.get("category_slug", "")
            category = categories.get(cat_slug)
            is_featured = item.get("is_featured", False)

            # Determine expiry
            if is_featured:
                expiry_hours = FEATURED_EXPIRY_HOURS
            elif cat_slug in SHORT_EXPIRY_SLUGS:
                expiry_hours = SHORT_EXPIRY_HOURS
            else:
                expiry_hours = DEFAULT_EXPIRY_HOURS

            NewsLink.objects.create(
                headline=headline,
                url=url,
                url_hash=url_hash_val,
                source_name=item.get("source_name", ""),
                category=category,
                snippet=item.get("snippet", ""),
                is_featured=is_featured,
                is_breaking=item.get("is_breaking", False),
                added_by=source,
                expires_at=now + timedelta(hours=expiry_hours),
            )
            created += 1

        # Auto-demote oldest featured if over limit
        featured_links = list(
            NewsLink.active.featured().values_list("id", flat=True)
        )
        if len(featured_links) > MAX_FEATURED:
            demote_ids = featured_links[MAX_FEATURED:]
            NewsLink.objects.filter(id__in=demote_ids).update(is_featured=False)
            self.stdout.write(f"Demoted {len(demote_ids)} older featured links")

        self.stdout.write(self.style.SUCCESS(
            f"Done: {created} created, {skipped} duplicates skipped"
        ))
