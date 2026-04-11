"""
Nightly cleanup of expired news links.

Usage:
    python manage.py cleanup_news

Cron:
    0 4 * * * cd /home/deploy/miningstock && venv/bin/python manage.py cleanup_news --settings=config.settings.production
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.news.models import NewsLink


class Command(BaseCommand):
    help = "Deactivate expired news links and delete old ones"

    def handle(self, *args, **options):
        now = timezone.now()
        cutoff = now - timedelta(days=30)

        # Deactivate expired links
        expired = NewsLink.objects.filter(
            is_active=True, expires_at__lt=now
        ).update(is_active=False)

        # Hard-delete links older than 30 days
        deleted, _ = NewsLink.objects.filter(created_at__lt=cutoff).delete()

        self.stdout.write(self.style.SUCCESS(
            f"Deactivated {expired} expired links, deleted {deleted} old links"
        ))
