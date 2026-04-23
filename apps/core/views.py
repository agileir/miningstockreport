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
    from apps.core.nav_math import NavInputs, calculate_nav_matrix_gold_legacy
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
            matrix = calculate_nav_matrix_gold_legacy(inputs, price_columns)
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


def tools_index(request):
    """Directory page listing all calculator tools."""
    return render(request, "core/tools_index.html")


def _resource_inputs_from_form(cd):
    """Extract ResourceInputs from any base-form cleaned data dict."""
    from apps.core.nav_math import ResourceInputs
    from decimal import Decimal
    return ResourceInputs(
        tonnes_inferred  = cd.get("tonnes_inferred")  or Decimal("0"),
        tonnes_indicated = cd.get("tonnes_indicated") or Decimal("0"),
        tonnes_measured  = cd.get("tonnes_measured")  or Decimal("0"),
        tonnes_probable  = cd.get("tonnes_probable")  or Decimal("0"),
        tonnes_proven    = cd.get("tonnes_proven")    or Decimal("0"),
    )


def _op_inputs_from_form(cd):
    from apps.core.nav_math import OperationalInputs
    return OperationalInputs(
        opex_per_tonne       = cd["opex_per_tonne"],
        capex_millions       = cd["capex_millions"],
        mine_life_years      = cd["mine_life_years"],
        discount_rate_pct    = cd["discount_rate_pct"],
        shares_outstanding_m = cd["shares_outstanding_m"],
        stage                = cd["stage"],
    )


def nav_calculator_copper(request):
    """Copper NAV calculator — grade in %, price in $/lb."""
    from apps.core.forms import NavCalculatorCopperForm
    from apps.core.nav_math import copper_revenue_per_tonne, calculate_nav_matrix
    from apps.core.models import CommodityPrice

    initial = {}
    cu_price = CommodityPrice.objects.filter(name__icontains="copper").first()
    if cu_price:
        initial["price_value_1"] = cu_price.price
        initial["price_label_1"] = f"Current Spot ({cu_price.fetched_at.strftime('%Y-%m-%d')})"

    matrix = None
    price_columns = None
    inputs_summary = None

    if request.method == "POST":
        form = NavCalculatorCopperForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            res = _resource_inputs_from_form(cd)
            op = _op_inputs_from_form(cd)
            price_columns = form.get_price_columns()
            scenarios = []
            for col in price_columns:
                rev = copper_revenue_per_tonne(cd["grade_pct"], cd["recovery_pct"], col["price"])
                scenarios.append({
                    "label": col["label"],
                    "revenue_per_tonne": rev,
                    "display_value": f"${col['price']:,.2f}/lb",
                })
            matrix = calculate_nav_matrix(res, op, scenarios)
            inputs_summary = {
                "total_tonnes": res.gross_tonnes(),
                "stage": cd["stage"],
                "grade_pct": cd["grade_pct"],
                "recovery_pct": cd["recovery_pct"],
                "mine_life_years": cd["mine_life_years"],
                "discount_rate_pct": cd["discount_rate_pct"],
                "shares_outstanding_m": cd["shares_outstanding_m"],
            }
    else:
        form = NavCalculatorCopperForm(initial=initial)

    return render(request, "core/nav_calculator_copper.html", {
        "form": form,
        "matrix": matrix,
        "price_columns": price_columns,
        "inputs_summary": inputs_summary,
    })


def nav_calculator_silver(request):
    """Silver NAV calculator — grade in g/t, price in $/oz. Same math as gold."""
    from apps.core.forms import NavCalculatorSilverForm
    from apps.core.nav_math import gold_or_silver_revenue_per_tonne, calculate_nav_matrix
    from apps.core.models import CommodityPrice

    initial = {}
    ag_price = CommodityPrice.objects.filter(name__icontains="silver").first()
    if ag_price:
        initial["price_value_1"] = ag_price.price
        initial["price_label_1"] = f"Current Spot ({ag_price.fetched_at.strftime('%Y-%m-%d')})"

    matrix = None
    price_columns = None
    inputs_summary = None

    if request.method == "POST":
        form = NavCalculatorSilverForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            res = _resource_inputs_from_form(cd)
            op = _op_inputs_from_form(cd)
            price_columns = form.get_price_columns()
            scenarios = []
            for col in price_columns:
                rev = gold_or_silver_revenue_per_tonne(cd["grade_gpt"], cd["recovery_pct"], col["price"])
                scenarios.append({
                    "label": col["label"],
                    "revenue_per_tonne": rev,
                    "display_value": f"${col['price']:,.2f}/oz",
                })
            matrix = calculate_nav_matrix(res, op, scenarios)
            inputs_summary = {
                "total_tonnes": res.gross_tonnes(),
                "stage": cd["stage"],
                "grade_gpt": cd["grade_gpt"],
                "recovery_pct": cd["recovery_pct"],
                "mine_life_years": cd["mine_life_years"],
                "discount_rate_pct": cd["discount_rate_pct"],
                "shares_outstanding_m": cd["shares_outstanding_m"],
            }
    else:
        form = NavCalculatorSilverForm(initial=initial)

    return render(request, "core/nav_calculator_silver.html", {
        "form": form,
        "matrix": matrix,
        "price_columns": price_columns,
        "inputs_summary": inputs_summary,
    })


def nav_calculator_polymetallic(request):
    """Polymetallic (gold + copper + silver) NAV calculator."""
    from decimal import Decimal
    from apps.core.forms import NavCalculatorPolymetallicForm
    from apps.core.nav_math import (
        gold_or_silver_revenue_per_tonne, copper_revenue_per_tonne,
        calculate_nav_matrix,
    )

    matrix = None
    price_columns = None
    inputs_summary = None

    if request.method == "POST":
        form = NavCalculatorPolymetallicForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            res = _resource_inputs_from_form(cd)
            op = _op_inputs_from_form(cd)

            def compute_rev(gold_price, cu_price, ag_price):
                total = Decimal("0")
                if (cd.get("gold_grade_gpt") or 0) > 0 and gold_price and gold_price > 0:
                    total += gold_or_silver_revenue_per_tonne(
                        cd["gold_grade_gpt"], cd["gold_recovery_pct"], gold_price,
                    )
                if (cd.get("copper_grade_pct") or 0) > 0 and cu_price and cu_price > 0:
                    total += copper_revenue_per_tonne(
                        cd["copper_grade_pct"], cd["copper_recovery_pct"], cu_price,
                    )
                if (cd.get("silver_grade_gpt") or 0) > 0 and ag_price and ag_price > 0:
                    total += gold_or_silver_revenue_per_tonne(
                        cd["silver_grade_gpt"], cd["silver_recovery_pct"], ag_price,
                    )
                return total

            rev_base = compute_rev(
                cd.get("gold_price_base"), cd.get("copper_price_base"), cd.get("silver_price_base"),
            )
            rev_longterm = compute_rev(
                cd.get("gold_price_longterm"), cd.get("copper_price_longterm"), cd.get("silver_price_longterm"),
            )

            # Build display labels showing the price combo for each scenario.
            def combo_label(prefix, cd):
                parts = []
                if (cd.get("gold_grade_gpt") or 0) > 0:
                    parts.append(f"Au ${cd.get(f'gold_price_{prefix}') or 0:,.0f}")
                if (cd.get("copper_grade_pct") or 0) > 0:
                    parts.append(f"Cu ${cd.get(f'copper_price_{prefix}') or 0:,.2f}")
                if (cd.get("silver_grade_gpt") or 0) > 0:
                    parts.append(f"Ag ${cd.get(f'silver_price_{prefix}') or 0:,.0f}")
                return " · ".join(parts)

            price_columns = [
                {"label": "Base Case", "price": None},
                {"label": "Long-term Deck", "price": None},
            ]

            scenarios = [
                {
                    "label": "Base Case",
                    "revenue_per_tonne": rev_base if rev_base > 0 else None,
                    "display_value": combo_label("base", cd),
                },
                {
                    "label": "Long-term Deck",
                    "revenue_per_tonne": rev_longterm if rev_longterm > 0 else None,
                    "display_value": combo_label("longterm", cd),
                },
            ]

            matrix = calculate_nav_matrix(res, op, scenarios)
            inputs_summary = {
                "total_tonnes": res.gross_tonnes(),
                "stage": cd["stage"],
                "gold_grade_gpt": cd.get("gold_grade_gpt"),
                "copper_grade_pct": cd.get("copper_grade_pct"),
                "silver_grade_gpt": cd.get("silver_grade_gpt"),
                "mine_life_years": cd["mine_life_years"],
                "discount_rate_pct": cd["discount_rate_pct"],
                "shares_outstanding_m": cd["shares_outstanding_m"],
            }
    else:
        form = NavCalculatorPolymetallicForm()

    return render(request, "core/nav_calculator_polymetallic.html", {
        "form": form,
        "matrix": matrix,
        "inputs_summary": inputs_summary,
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
