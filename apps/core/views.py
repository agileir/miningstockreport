from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from apps.accounts.models import User
from apps.blog.models import Post
from apps.videos.models import Video
from apps.verdict.models import VerdictScorecard
from apps.watchlist.models import WatchlistItem, WatchlistStatus


def home(request):
    recent_posts = Post.objects.filter(
        status=Post.Status.PUBLISHED, published_at__lte=timezone.now()
    ).select_related("author").order_by("-published_at")[:6]

    featured_videos    = Video.objects.filter(is_featured=True).order_by("-published_at")[:3]
    recent_verdicts    = (VerdictScorecard.objects.filter(is_published=True)
                          .select_related("company").order_by("-scored_at")[:4])
    watchlist_snapshot = (WatchlistItem.objects
                          .filter(status__in=[WatchlistStatus.WATCHING, WatchlistStatus.POSITION])
                          .select_related("company", "company__price_cache")
                          .order_by("-added_at")[:6])

    return render(request, "core/home.html", {
        "recent_posts":        recent_posts,
        "featured_videos":     featured_videos,
        "recent_verdicts":     recent_verdicts,
        "watchlist_snapshot":  watchlist_snapshot,
    })


def about(request):
    return render(request, "core/about.html")


def author_profile(request, username):
    """Author profile page with Person schema for E-E-A-T."""
    author = get_object_or_404(User, username=username, is_staff=True)
    recent_posts = Post.objects.filter(
        author=author, status=Post.Status.PUBLISHED, published_at__lte=timezone.now()
    ).order_by("-published_at")[:10]
    return render(request, "core/author_profile.html", {
        "author": author,
        "recent_posts": recent_posts,
    })


def methodology(request):
    return render(request, "core/methodology.html")


def disclaimer(request):
    return render(request, "core/disclaimer.html")


def nav_calculator(request):
    """
    Risk-adjusted NAV calculator for junior mining companies. Applies
    resource-category confidence weights and study-stage haircuts to
    produce a matrix of per-share NAV estimates across multiple gold-
    price benchmarks.
    """
    from apps.core.forms import NavCalculatorForm
    from apps.core.nav_math import NavInputs, calculate_nav_matrix
    from apps.core.models import CommodityPrice

    # Pre-populate current spot price from CommodityPrice if available.
    initial = {}
    gold_price = CommodityPrice.objects.filter(name__icontains="gold").first()
    if gold_price:
        initial["price_value_1"] = gold_price.price
        initial["price_label_1"] = f"Current Spot ({gold_price.fetched_at.strftime('%Y-%m-%d')})"

    matrix = None
    price_columns = None
    inputs_summary = None

    if request.method == "POST":
        form = NavCalculatorForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            inputs = NavInputs(
                tonnes_inferred  = cd.get("tonnes_inferred")  or 0,
                tonnes_indicated = cd.get("tonnes_indicated") or 0,
                tonnes_measured  = cd.get("tonnes_measured")  or 0,
                tonnes_probable  = cd.get("tonnes_probable")  or 0,
                tonnes_proven    = cd.get("tonnes_proven")    or 0,
                grade_gpt            = cd["grade_gpt"],
                recovery_pct         = cd["recovery_pct"],
                opex_per_tonne       = cd["opex_per_tonne"],
                capex_millions       = cd["capex_millions"],
                mine_life_years      = cd["mine_life_years"],
                discount_rate_pct    = cd["discount_rate_pct"],
                shares_outstanding_m = cd["shares_outstanding_m"],
                stage                = cd["stage"],
            )
            price_columns = form.get_price_columns()
            matrix = calculate_nav_matrix(inputs, price_columns)
            inputs_summary = {
                "total_tonnes": sum((
                    inputs.tonnes_inferred, inputs.tonnes_indicated,
                    inputs.tonnes_measured, inputs.tonnes_probable,
                    inputs.tonnes_proven,
                )),
                "stage": cd["stage"],
                "grade_gpt": cd["grade_gpt"],
                "recovery_pct": cd["recovery_pct"],
                "mine_life_years": cd["mine_life_years"],
                "shares_outstanding_m": cd["shares_outstanding_m"],
                "discount_rate_pct": cd["discount_rate_pct"],
            }
    else:
        form = NavCalculatorForm(initial=initial)

    return render(request, "core/nav_calculator.html", {
        "form": form,
        "matrix": matrix,
        "price_columns": price_columns,
        "inputs_summary": inputs_summary,
        "current_gold_price": gold_price,
    })


def robots_txt(request):
    """
    Dynamic robots.txt — blocks staging/dev crawling, allows prod.
    Explicitly references sitemap location for crawlers.
    """
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Disallow: /api/",
        "Allow: /",
        "",
        "# AI Platform Crawlers — explicitly allowed",
        "User-agent: GPTBot",
        "Allow: /",
        "",
        "User-agent: ChatGPT-User",
        "Allow: /",
        "",
        "User-agent: PerplexityBot",
        "Allow: /",
        "",
        "User-agent: ClaudeBot",
        "Allow: /",
        "",
        "User-agent: anthropic-ai",
        "Allow: /",
        "",
        "User-agent: Google-Extended",
        "Allow: /",
        "",
        f"Sitemap: {settings.SITE_URL}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def llms_txt(request):
    """
    /llms.txt — emerging standard for AI crawlers (Perplexity, ChatGPT, Anthropic).
    Tells AI engines what this site is, what content is authoritative,
    and which pages are most valuable to index for citations.
    """
    content = f"""# {settings.SITE_NAME}

> {settings.SITE_TAGLINE}

Mining Stock Report provides independent research and analysis on junior mining
stocks, with a focus on the TSX Venture, ASX, and OTC markets. All analysis is
produced by a single analyst using a consistent 5-factor scoring framework
(the Verdict Framework) grounded in NI 43-101 / JORC technical reports.

## Key pages

- Homepage: {settings.SITE_URL}/
- Verdict Framework (company scorecards): {settings.SITE_URL}/companies/
- Current watchlist: {settings.SITE_URL}/watchlist/
- Analysis archive: {settings.SITE_URL}/analysis/
- Mining News Wire: {settings.SITE_URL}/news/
- About: {settings.SITE_URL}/about/
- Methodology & Disclosure: {settings.SITE_URL}/about/methodology/
- Sitemap: {settings.SITE_URL}/sitemap.xml

## Content categories

- Due Diligence: How to read technical reports, evaluate geology, assess management
- Company Verdicts: Scored deep-dives on individual junior mining companies
- Market Intelligence: Sector macro, catalyst calendars, M&A analysis
- Accountability: Public portfolio tracking, position updates, loss post-mortems

## Methodology

The Verdict Framework scores each company 1-5 on five factors:
1. Management skin-in-the-game
2. Project geology quality (NI 43-101 / JORC resource classification)
3. Capital structure health
4. Catalyst proximity
5. Comparable acquisition value (P/NAV vs peer transactions)

Composite score out of 25 drives a BUY, WATCH, or AVOID verdict.

## Licensing

Content is copyright {settings.SITE_NAME}. Short excerpts with attribution are
permitted. Full reproduction requires written permission.
"""
    return HttpResponse(content, content_type="text/plain; charset=utf-8")


def handler404(request, exception):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)
