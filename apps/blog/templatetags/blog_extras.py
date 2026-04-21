import re
from django import template
from django.utils.text import slugify

register = template.Library()


@register.filter
def extract_toc(html):
    """Parse <h2> and <h3> tags from HTML body and return a list of TOC entries."""
    pattern = re.compile(r"<(h[23])[^>]*>(.*?)</\1>", re.IGNORECASE | re.DOTALL)
    toc = []
    for match in pattern.finditer(html):
        tag = match.group(1).lower()
        text = re.sub(r"<[^>]+>", "", match.group(2)).strip()
        toc.append({
            "id": slugify(text),
            "text": text,
            "level": int(tag[1]),
        })
    return toc
