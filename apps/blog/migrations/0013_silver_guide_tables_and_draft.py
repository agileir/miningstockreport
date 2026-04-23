"""
Insert 4 inline HTML tables into the silver investor guide (seeded in 0012)
at specific anchor points, and set the post's status to DRAFT so it does
not publish until external charts/graphics have been added.

Tables inserted:
  #3  Silver Demand by Category         — after the "Demand" subsection
  #6  Investment Vehicle Comparison     — at the start of §5 (Ways to Invest)
  #10 Our Silver Coverage Status        — inside §10 (Coverage roadmap)
  #15 Position Sizing Framework         — inside §8 (Portfolio Construction)

Idempotent: re-running checks for a unique HTML-comment marker before
each insert and skips if already present.
"""
from django.db import migrations


TITLE_PREFIX = "Investing in Silver:"


TABLE_3_DEMAND = """
<!-- SILVER_TABLE_DEMAND -->
<div class="table-responsive my-4">
  <table class="table table-dark table-sm border-secondary small align-middle">
    <caption class="text-secondary small">Silver demand by category, 2025 approximate figures. Total annual demand roughly 1,000 million ounces.</caption>
    <thead class="text-secondary text-uppercase">
      <tr>
        <th>Category</th>
        <th class="text-end">Annual Demand (Moz)</th>
        <th class="text-end">Share</th>
        <th>Key Driver</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="text-white">Photovoltaic solar</td>
        <td class="text-end">~200</td>
        <td class="text-end">~20%</td>
        <td class="text-secondary">Solar panel metallization paste</td>
      </tr>
      <tr>
        <td class="text-white">Other industrial (EV, 5G, medical, electronics)</td>
        <td class="text-end">~350</td>
        <td class="text-end">~35%</td>
        <td class="text-secondary">Battery mgmt, high-voltage contacts, medical</td>
      </tr>
      <tr>
        <td class="text-white">Jewelry</td>
        <td class="text-end">~200</td>
        <td class="text-end">~20%</td>
        <td class="text-secondary">India and China dominate</td>
      </tr>
      <tr>
        <td class="text-white">Investment (bars, coins, ETF holdings)</td>
        <td class="text-end">~200</td>
        <td class="text-end">~20%</td>
        <td class="text-secondary">Sentiment-driven, most volatile</td>
      </tr>
      <tr>
        <td class="text-white">Other (photography, silverware, misc.)</td>
        <td class="text-end">~50</td>
        <td class="text-end">~5%</td>
        <td class="text-secondary">Slowly declining category</td>
      </tr>
    </tbody>
  </table>
</div>
""".strip()


TABLE_6_VEHICLES = """
<!-- SILVER_TABLE_VEHICLES -->
<div class="table-responsive my-4">
  <table class="table table-dark table-sm border-secondary small align-middle">
    <caption class="text-secondary small">Primary silver investment vehicles — cost, liquidity, and practical trade-offs.</caption>
    <thead class="text-secondary text-uppercase">
      <tr>
        <th>Vehicle</th>
        <th>Cost</th>
        <th>Liquidity</th>
        <th>Counterparty</th>
        <th>Best For</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="text-white">Physical bullion (coins, bars)</td>
        <td>10-25% retail premium; storage 0-1%/yr</td>
        <td>Moderate</td>
        <td class="text-secondary">None (self-custody)</td>
        <td class="text-secondary">Financial-system-failure hedging</td>
      </tr>
      <tr>
        <td class="text-white">SLV (iShares Silver Trust)</td>
        <td>0.50% ER</td>
        <td>Highest</td>
        <td class="text-secondary">BlackRock / JPMorgan custody</td>
        <td class="text-secondary">Default tactical price exposure</td>
      </tr>
      <tr>
        <td class="text-white">SIVR (abrdn Physical Silver)</td>
        <td>0.30% ER</td>
        <td>Moderate</td>
        <td class="text-secondary">abrdn / HSBC custody</td>
        <td class="text-secondary">Lower-cost tactical exposure</td>
      </tr>
      <tr>
        <td class="text-white">PSLV (Sprott Physical Silver Trust)</td>
        <td>0.60% ER; trades at premium/discount to NAV</td>
        <td>Moderate</td>
        <td class="text-secondary">Sprott (fully allocated)</td>
        <td class="text-secondary">Allocated silver without physical hassle</td>
      </tr>
      <tr>
        <td class="text-white">Wheaton Precious Metals (TSX:WPM)</td>
        <td>Equity; no expense ratio</td>
        <td>High</td>
        <td class="text-secondary">Corporate (streaming book)</td>
        <td class="text-secondary">Low-variance leverage to silver price</td>
      </tr>
      <tr>
        <td class="text-white">SIL (Global X Silver Miners ETF)</td>
        <td>0.65% ER</td>
        <td>High</td>
        <td class="text-secondary">Global X</td>
        <td class="text-secondary">Senior + mid-tier miner basket</td>
      </tr>
      <tr>
        <td class="text-white">SILJ (ETFMG Junior Silver Miners)</td>
        <td>0.69% ER</td>
        <td>Moderate</td>
        <td class="text-secondary">ETFMG</td>
        <td class="text-secondary">Junior / developer-heavy basket</td>
      </tr>
      <tr>
        <td class="text-white">Individual silver mining equities</td>
        <td>Trading costs only</td>
        <td>Varies</td>
        <td class="text-secondary">Operating company</td>
        <td class="text-secondary">Highest operating leverage, highest variance</td>
      </tr>
    </tbody>
  </table>
</div>
""".strip()


TABLE_10_COVERAGE = """
<!-- SILVER_TABLE_COVERAGE -->
<div class="table-responsive my-4">
  <table class="table table-dark table-sm border-secondary small align-middle">
    <caption class="text-secondary small">Silver equities on our Verdict Framework coverage list as of April 2026.</caption>
    <thead class="text-secondary text-uppercase">
      <tr>
        <th>Ticker</th>
        <th>Company</th>
        <th>Primary</th>
        <th>Status</th>
        <th>Verdict</th>
        <th class="text-end">Composite</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="text-warning fw-bold">TSX:GGD</td>
        <td class="text-white">GoGold Resources Inc.</td>
        <td>Silver</td>
        <td><span class="badge bg-success">Scored</span></td>
        <td><span class="badge bg-warning text-dark">WATCH</span></td>
        <td class="text-end text-white">21/25</td>
      </tr>
      <tr>
        <td class="text-warning fw-bold">TSX:FR</td>
        <td class="text-white">First Majestic Silver Corp.</td>
        <td>Silver</td>
        <td><span class="badge bg-secondary">Queued</span></td>
        <td class="text-secondary">—</td>
        <td class="text-end text-secondary">—</td>
      </tr>
      <tr>
        <td class="text-warning fw-bold">TSX:MAG</td>
        <td class="text-white">MAG Silver Corp.</td>
        <td>Silver</td>
        <td><span class="badge bg-secondary">Queued</span></td>
        <td class="text-secondary">—</td>
        <td class="text-end text-secondary">—</td>
      </tr>
      <tr>
        <td class="text-warning fw-bold">TSX:PAAS</td>
        <td class="text-white">Pan American Silver Corp.</td>
        <td>Silver</td>
        <td><span class="badge bg-secondary">Queued</span></td>
        <td class="text-secondary">—</td>
        <td class="text-end text-secondary">—</td>
      </tr>
      <tr>
        <td class="text-warning fw-bold">TSX:AYA</td>
        <td class="text-white">Aya Gold &amp; Silver Inc.</td>
        <td>Silver</td>
        <td><span class="badge bg-secondary">Queued</span></td>
        <td class="text-secondary">—</td>
        <td class="text-end text-secondary">—</td>
      </tr>
      <tr>
        <td class="text-warning fw-bold">TSX:FVI</td>
        <td class="text-white">Fortuna Mining Corp.</td>
        <td>Silver</td>
        <td><span class="badge bg-secondary">Queued</span></td>
        <td class="text-secondary">—</td>
        <td class="text-end text-secondary">—</td>
      </tr>
      <tr>
        <td class="text-warning fw-bold">TSX:SVM</td>
        <td class="text-white">Silvercorp Metals Inc.</td>
        <td>Silver</td>
        <td><span class="badge bg-secondary">Queued</span></td>
        <td class="text-secondary">—</td>
        <td class="text-end text-secondary">—</td>
      </tr>
      <tr>
        <td class="text-warning fw-bold">TSX:EDR</td>
        <td class="text-white">Endeavour Silver Corp.</td>
        <td>Silver</td>
        <td><span class="badge bg-secondary">Queued</span></td>
        <td class="text-secondary">—</td>
        <td class="text-end text-secondary">—</td>
      </tr>
    </tbody>
  </table>
</div>
""".strip()


TABLE_15_SIZING = """
<!-- SILVER_TABLE_SIZING -->
<div class="table-responsive my-4">
  <table class="table table-dark table-sm border-secondary small align-middle">
    <caption class="text-secondary small">Relative position sizing — silver vs gold at equivalent risk contribution. Silver's structural volatility is roughly 1.5-2x gold's.</caption>
    <thead class="text-secondary text-uppercase">
      <tr>
        <th>Conviction Level</th>
        <th>Gold Position (% portfolio)</th>
        <th>Silver Position (% portfolio)</th>
        <th>Rationale</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="text-white">High-conviction BUY</td>
        <td>3% - 5%</td>
        <td>2% - 3%</td>
        <td class="text-secondary">Silver at ~60-70% of equivalent gold size</td>
      </tr>
      <tr>
        <td class="text-white">Moderate WATCH</td>
        <td>1% - 2%</td>
        <td>0.5% - 1%</td>
        <td class="text-secondary">Smaller sizing for silver's higher variance</td>
      </tr>
      <tr>
        <td class="text-white">Speculative / exploration</td>
        <td>0.5% - 1%</td>
        <td>0.25% - 0.5%</td>
        <td class="text-secondary">Half-size baseline for higher-risk exposure</td>
      </tr>
      <tr>
        <td class="text-white">Starter position</td>
        <td>0.25% - 0.5%</td>
        <td>0.1% - 0.25%</td>
        <td class="text-secondary">Exploratory scale, build conviction first</td>
      </tr>
    </tbody>
  </table>
</div>
""".strip()


# Anchor strings MUST match the post body exactly. If the body is edited
# such that an anchor changes, the migration will raise rather than silently
# skipping.
ANCHORS = [
    {
        "marker": "<!-- SILVER_TABLE_DEMAND -->",
        "anchor": (
            "The residual 5% covers photography (declining but still real in medical "
            "and aerospace film), silverware, and miscellaneous applications.</p>"
        ),
        "table": TABLE_3_DEMAND,
    },
    {
        "marker": "<!-- SILVER_TABLE_VEHICLES -->",
        "anchor": '<h3 id="physical-silver">Physical Silver</h3>',
        "table": TABLE_6_VEHICLES,
        "insert_before": True,
    },
    {
        "marker": "<!-- SILVER_TABLE_COVERAGE -->",
        "anchor": (
            "Currently scored: GoGold Resources (TSX:GGD) at 21/25 WATCH. The highest-"
            "scoring silver name on our coverage, with a factor mix that technically "
            "clears the BUY threshold.</p>"
        ),
        "table": TABLE_10_COVERAGE,
    },
    {
        "marker": "<!-- SILVER_TABLE_SIZING -->",
        "anchor": (
            "The silver positions will feel smaller in dollar terms but will contribute "
            "equivalent portfolio volatility.</p>"
        ),
        "table": TABLE_15_SIZING,
    },
]


def apply(apps, schema_editor):
    import re
    from apps.blog.models import Post

    try:
        post = Post.objects.get(title__startswith=TITLE_PREFIX)
    except Post.DoesNotExist:
        return

    body = post.body

    for spec in ANCHORS:
        marker = spec["marker"]
        anchor = spec["anchor"]
        table = spec["table"]

        if marker in body:
            continue  # already inserted

        # Build a regex where every whitespace run in the anchor matches \s+.
        # This makes the match resilient to line-break reflow in the body.
        pattern_str = r"\s+".join(re.escape(token) for token in anchor.split())
        pattern = re.compile(pattern_str)
        match = pattern.search(body)
        if not match:
            raise ValueError(f"Anchor not found for {marker}: {anchor[:60]}...")

        found_text = match.group(0)
        if spec.get("insert_before"):
            replacement = f"{table}\n\n{found_text}"
        else:
            replacement = f"{found_text}\n\n{table}"

        body = body[:match.start()] + replacement + body[match.end():]

    # Set to draft so the post does not publish until graphics are added.
    post.body = body
    post.status = "draft"
    post.save(update_fields=["body", "status"])


def reverse(apps, schema_editor):
    import re
    from apps.blog.models import Post

    try:
        post = Post.objects.get(title__startswith=TITLE_PREFIX)
    except Post.DoesNotExist:
        return

    body = post.body
    # Strip each injected table block using the marker and its closing </div>
    for marker in [
        "<!-- SILVER_TABLE_DEMAND -->",
        "<!-- SILVER_TABLE_VEHICLES -->",
        "<!-- SILVER_TABLE_COVERAGE -->",
        "<!-- SILVER_TABLE_SIZING -->",
    ]:
        pattern = re.compile(
            re.escape(marker) + r".*?</div>\s*",
            re.DOTALL,
        )
        body = pattern.sub("", body)

    post.body = body
    post.status = "published"
    post.save(update_fields=["body", "status"])


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0012_seed_silver_investor_guide"),
    ]
    operations = [
        migrations.RunPython(apply, reverse),
    ]
