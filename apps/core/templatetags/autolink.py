"""
Template filter that auto-links company names, tickers, and custom keyword
phrases to their detail pages.

Usage:
    {% load autolink %}
    {{ post.body|autolink }}
    {{ scorecard.analyst_summary|linebreaks|autolink }}

Rules:
- First occurrence of each phrase is linked; subsequent occurrences are left alone.
- Text already inside <a>, <h1>–<h6>, <script>, <code>, <pre> tags is skipped.
- Company names link on bare word-boundary match ("Goldmining Inc.").
- Tickers only link when prefixed with their exchange ("TSX:GOLD", "NYSE:ABX").
  This prevents common words that happen to be tickers (GOLD, FURY, ONYX) from
  over-linking generic mentions of the commodity or word.
- Custom phrases come from the AutoLink model (managed in Django admin).
- Matching is case-insensitive. Links use word boundaries to avoid partial matches.
- Results are cached for 5 minutes to avoid DB hits on every render.
"""
import re
from django import template
from django.core.cache import cache
from django.utils.safestring import mark_safe

register = template.Library()

# Tags whose inner content should never be modified
SKIP_TAGS = re.compile(
    r"<(a|h[1-6]|script|code|pre|style)\b[^>]*>.*?</\1>",
    re.DOTALL | re.IGNORECASE,
)

CACHE_KEY = "autolink_phrases"
CACHE_TTL = 300  # 5 minutes


def _get_phrases():
    """Return list of (compiled_regex, url, phrase_length) sorted longest-first."""
    phrases = cache.get(CACHE_KEY)
    if phrases is not None:
        return phrases

    from apps.verdict.models import Company
    from apps.core.models import AutoLink

    entries = []

    # Company names link bare; tickers require an exchange prefix to disambiguate
    # from generic mining vocabulary (GOLD, FURY, ONYX, etc.).
    for c in Company.objects.only("name", "ticker", "exchange", "slug"):
        url = c.get_absolute_url()
        if c.name:
            entries.append((c.name, url))
        if c.ticker and c.exchange:
            entries.append((f"{c.exchange}:{c.ticker}", url))

    # Custom editorial phrases
    for al in AutoLink.objects.filter(is_active=True).only("phrase", "target_url"):
        entries.append((al.phrase, al.target_url))

    # Sort longest phrase first to avoid partial matches
    entries.sort(key=lambda x: len(x[0]), reverse=True)

    # Compile regex for each — word-boundary match, case-insensitive
    compiled = []
    for phrase, url in entries:
        pattern = re.compile(
            r"(?<!\w)" + re.escape(phrase) + r"(?!\w)",
            re.IGNORECASE,
        )
        compiled.append((pattern, url, len(phrase)))

    cache.set(CACHE_KEY, compiled, CACHE_TTL)
    return compiled


@register.filter(name="autolink", is_safe=True)
def autolink(html):
    """Replace first occurrence of each known phrase with an internal link."""
    if not html:
        return html

    html = str(html)
    phrases = _get_phrases()
    if not phrases:
        return mark_safe(html)

    # Split HTML into protected regions (tags we skip) and free text regions.
    # We process only the free text regions.
    linked = set()  # track which URLs we've already linked to avoid double-linking

    # Build a map of protected character ranges
    protected = set()
    for m in SKIP_TAGS.finditer(html):
        protected.update(range(m.start(), m.end()))

    # Also protect all HTML tags themselves (< ... >) so we don't insert
    # links inside tag attributes
    for m in re.finditer(r"<[^>]+>", html):
        protected.update(range(m.start(), m.end()))

    for pattern, url, _ in phrases:
        if url in linked:
            continue

        match = pattern.search(html)
        if not match:
            continue

        # Find the first occurrence that is NOT in a protected range
        while match:
            span = range(match.start(), match.end())
            if not any(pos in protected for pos in span):
                break
            match = pattern.search(html, match.end())

        if not match:
            continue

        original = match.group(0)
        link = f'<a href="{url}" class="text-warning text-decoration-none">{original}</a>'
        # Replace only this specific occurrence
        html = html[:match.start()] + link + html[match.end():]

        # Update protected ranges: the new link tag is now protected
        new_protected_start = match.start()
        new_protected_end = match.start() + len(link)
        protected.update(range(new_protected_start, new_protected_end))

        linked.add(url)

    return mark_safe(html)
