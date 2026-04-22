from django.db import migrations


COMPANY_VERDICTS_INTRO = """
<div class="row g-5">
  <div class="col-lg-7">
    <h2 class="text-white fw-bold h5 mb-3">How a Verdict Gets Written</h2>
    <p>
      A Company Verdict is the end product of the Verdict Framework applied to a single
      junior mining issuer. Every scorecard starts the same way: we pull the most recent
      NI 43-101 or JORC technical report, the last four quarterly MD&amp;As, the most
      recent management information circular, and the rolling six months of SEDI or
      equivalent insider filings. From those documents alone — never from a company deck
      or an IR call — each of the five factors is scored 1 to 5, summed into a composite
      out of 25, and mapped to one of three verdicts.
    </p>
    <p>
      BUY is reserved for composites of 18 or higher with no single factor below 3. WATCH
      is 13 to 17, or 18-plus with at least one factor that concerns us enough to withhold
      a position. AVOID is anything below 13, or any score where the capital-structure or
      management factor is scored 1 — because broken cap tables and broken incentives are
      the two things that never fix themselves in a junior mining company.
    </p>
    <p class="mb-0">
      Every verdict is dated. When material new information lands — a resource update,
      a financing, a management change, a catalyst miss — we publish a new scorecard on
      the same company rather than edit the old one. The history stays public so readers
      can see where a thesis bent and where it broke.
    </p>
  </div>
  <div class="col-lg-5">
    <div class="card bg-dark border-secondary h-100">
      <div class="card-body">
        <h3 class="text-warning fw-bold h6 mb-3">What to Expect in a Verdict Post</h3>
        <ul class="small ps-3 mb-0">
          <li class="mb-2">A one-paragraph answer capsule — verdict, composite score, P/NAV — at the top</li>
          <li class="mb-2">Factor-by-factor scoring with direct citations to the 43-101 page, SEDI filing, or circular table</li>
          <li class="mb-2">A named comparable-transactions table showing the acquisition-value math</li>
          <li class="mb-2">A catalyst calendar versus working-capital runway</li>
          <li class="mb-0">A disclosure line on any position the desk holds in the company</li>
        </ul>
      </div>
    </div>
  </div>
</div>
""".strip()


INVESTING_GUIDES_INTRO = """
<div class="row g-5">
  <div class="col-lg-7">
    <h2 class="text-white fw-bold h5 mb-3">Evergreen Guides for the Junior Mining Investor</h2>
    <p>
      The Investing Guides pillar is the reference library behind every scorecard on the
      site. If a Company Verdict is a decision on one company at a point in time, a guide
      is the methodology behind how that decision was reached — and how a reader can
      reproduce it on a company we haven't covered yet. Guides are written to be read in
      order or dipped into by topic: how to read a 43-101, how to calculate fully-diluted
      share count from first principles, how to build a catalyst calendar against
      working-capital runway, how to value an explorer with no resource yet using analog
      projects and land-package math.
    </p>
    <p>
      Every guide is anchored in public filings. Where a guide references a specific
      company, it uses that company only as a worked example — not as a recommendation.
      Guides are updated in place when the underlying data or regulatory framework shifts
      — and every update is timestamped so a reader can see what changed since the last
      version they read.
    </p>
    <p class="mb-0">
      The target reader is the self-directed investor who has been burned once by a
      newsletter pump, has $25K to $250K at risk in the junior space, and wants a durable
      framework instead of a tip sheet. If you already know how to read a metallurgy
      section and price a warrant, these guides will feel obvious. If you don't, they are
      the fastest way we know to get there.
    </p>
  </div>
  <div class="col-lg-5">
    <div class="card bg-dark border-secondary h-100">
      <div class="card-body">
        <h3 class="text-warning fw-bold h6 mb-3">Guide Threads</h3>
        <ul class="small ps-3 mb-0">
          <li class="mb-2"><strong class="text-white">Reading the Filings</strong> — 43-101, JORC, circulars, SEDI, insider transaction summaries</li>
          <li class="mb-2"><strong class="text-white">Valuation</strong> — P/NAV, comparable transactions, EV/resource, risk-adjusted DCF</li>
          <li class="mb-2"><strong class="text-white">Cap Tables</strong> — fully-diluted math, warrant overhang, dilution cycles</li>
          <li class="mb-2"><strong class="text-white">Catalysts</strong> — building a news calendar that lines up with financing runway</li>
          <li class="mb-0"><strong class="text-white">Position Sizing</strong> — what a 2%, 5%, and 10% position looks like in an explorer</li>
        </ul>
      </div>
    </div>
  </div>
</div>
""".strip()


MARKET_COMMENTARY_INTRO = """
<div class="row g-5">
  <div class="col-lg-7">
    <h2 class="text-white fw-bold h5 mb-3">The Weekly Read on the Junior Mining Market</h2>
    <p>
      Market Commentary is the pillar for everything that isn't a single-company
      scorecard or a methodology piece — the weekly read on where the sector is, what
      moved, and what it means for the companies we cover. Commentary pieces run in
      three formats: the weekly sector wrap, the monthly portfolio update, and the
      ad-hoc piece triggered by a specific catalyst — a gold-price move, a major M&amp;A
      transaction, a surprise Fed pivot, a commodity-specific supply shock.
    </p>
    <p>
      The editorial line here is the same as everywhere else on the site: we show our
      work, we cite our sources, and we tell readers what we did with our own capital
      in response. Commentary is not forecasting; we don't publish gold-price targets
      for twelve months out because nobody who has been honest about this sector for
      twenty years would. What we do publish is: what changed this week, which companies
      on the watchlist it most affects, and whether any open position had its thesis
      strengthened, weakened, or broken by the new information.
    </p>
    <p class="mb-0">
      Older commentary is preserved, not deleted. A piece from six months ago that got
      the macro set-up wrong stays up — with a comment linking to the correction. That
      is how a reader judges whether a research desk is worth following: not by the
      calls that worked, but by what they do with the ones that didn't.
    </p>
  </div>
  <div class="col-lg-5">
    <div class="card bg-dark border-secondary h-100">
      <div class="card-body">
        <h3 class="text-warning fw-bold h6 mb-3">What a Commentary Post Covers</h3>
        <ul class="small ps-3 mb-0">
          <li class="mb-2">The one or two things that actually moved the junior mining market this week</li>
          <li class="mb-2">Any watchlist impact — names added, names demoted, theses tightened</li>
          <li class="mb-2">Position updates on In Position names — including any changes to entry, target, or stop</li>
          <li class="mb-2">A read on the gold, copper, and uranium set-up as it affects the sector</li>
          <li class="mb-0">A transparent disclosure on any trades placed in the week</li>
        </ul>
      </div>
    </div>
  </div>
</div>
""".strip()


MARKET_INTELLIGENCE_INTRO = """
<div class="row g-5">
  <div class="col-lg-7">
    <h2 class="text-white fw-bold h5 mb-3">M&amp;A, Financings, and the Deal Flow That Drives the Sector</h2>
    <p>
      Market Intelligence is the pillar that tracks the sector's plumbing — the M&amp;A
      transactions, financings, strategic investments, and regulatory changes that drive
      the prices we see on the companies we cover. A scorecard tells a reader what a
      company is worth today. Market Intelligence tells them what the acquirer's next
      move is likely to look like, which financiers are writing cheques at what terms,
      and which jurisdictions are newly friendly or newly hostile.
    </p>
    <p>
      The core of this pillar is the rolling M&amp;A comparables table we maintain
      internally and publish in excerpt form. Every time a junior miner is acquired,
      we log the transaction metrics — price per ounce in the ground, P/NAV multiple
      paid, payment currency, premium to prior-thirty-day VWAP, resource category at
      close — and fold it into the acquisition-value factor scoring on every new
      scorecard. Financings get the same treatment: flow-through vs hard dollars,
      warrant coverage, discount to five-day VWAP, finder's fees, and any strategic
      investor taking a strategic stake rather than a pure financial position.
    </p>
    <p class="mb-0">
      Coverage skews toward the commodities we cover most — gold and silver primarily,
      copper and uranium secondarily, with lithium and rare earths flagged when they
      cross our screen. If you care about a single transaction and don't see it
      covered, the underlying data is in the comparables table and we will cite it
      in the next relevant scorecard.
    </p>
  </div>
  <div class="col-lg-5">
    <div class="card bg-dark border-secondary h-100">
      <div class="card-body">
        <h3 class="text-warning fw-bold h6 mb-3">Core Trackers</h3>
        <ul class="small ps-3 mb-0">
          <li class="mb-2">M&amp;A comparables — trailing twenty-four months, by commodity and jurisdiction</li>
          <li class="mb-2">Financing terms tracker — flow-through, hard-dollar, warrant coverage trends</li>
          <li class="mb-2">Strategic-investor moves — majors taking positions in juniors</li>
          <li class="mb-2">Permitting and regulatory read-through, jurisdiction by jurisdiction</li>
          <li class="mb-0">Quarterly catalyst calendar across the full coverage universe</li>
        </ul>
      </div>
    </div>
  </div>
</div>
""".strip()


PRICE_OF_GOLD_INTRO = """
<div class="row g-5">
  <div class="col-lg-7">
    <h2 class="text-white fw-bold h5 mb-3">The Price of Gold, and What It Does to the Juniors</h2>
    <p>
      The Price of Gold pillar is dedicated to the single commodity that drives most of
      the coverage universe on this site. It is not a gold-price prediction service and
      it does not publish price targets. What it does publish: the supply-and-demand
      framework that sets the floor and the ceiling, the real-rate and dollar dynamics
      that explain most of the variance month to month, the central-bank buying data
      that has been the structural bid since 2022, and — most importantly for readers
      here — what any given gold-price regime means for the producers, developers, and
      explorers on the watchlist.
    </p>
    <p>
      A gold price in the mid-three-thousands does not affect a high-grade underground
      producer the same way it affects a low-grade heap-leach developer. An explorer
      with no resource is barely sensitive to spot; the company is priced off
      discovery odds, not margin. We write the analysis so readers can separate the
      signal (what gold means for this specific company at this specific stage) from
      the noise (what gold means for the generic gold-bug asset allocation call).
    </p>
    <p class="mb-0">
      Coverage also extends to the gold-adjacent universe: gold-copper porphyry names,
      gold-silver polymetallic projects, and the royalty and streaming companies whose
      valuations move with gold but whose risk profiles don't. Each sub-universe gets
      its own valuation framework because each one responds to a gold-price move
      differently.
    </p>
  </div>
  <div class="col-lg-5">
    <div class="card bg-dark border-secondary h-100">
      <div class="card-body">
        <h3 class="text-warning fw-bold h6 mb-3">Recurring Coverage</h3>
        <ul class="small ps-3 mb-0">
          <li class="mb-2">Quarterly gold-price set-up — real rates, dollar, central-bank buying</li>
          <li class="mb-2">All-in sustaining cost curves for the producer coverage universe</li>
          <li class="mb-2">Gold-price sensitivity tables on every developer scorecard</li>
          <li class="mb-2">Exploration-stage gold equities — why they aren't as gold-sensitive as most retail investors assume</li>
          <li class="mb-0">Royalty &amp; streaming coverage — the gold-linked vehicle with the least operational risk</li>
        </ul>
      </div>
    </div>
  </div>
</div>
""".strip()


PILLAR_INTROS = {
    "company-verdicts":    COMPANY_VERDICTS_INTRO,
    "investing-guides":    INVESTING_GUIDES_INTRO,
    "market-commentary":   MARKET_COMMENTARY_INTRO,
    "market-intelligence": MARKET_INTELLIGENCE_INTRO,
    "price-of-gold":       PRICE_OF_GOLD_INTRO,
}


PILLAR_DEFAULTS = {
    "investing-guides": {
        "name": "Investing Guides",
        "description": "Evergreen guides for junior mining investors — how to read a 43-101, calculate fully-diluted share count, build a catalyst calendar, and value an explorer.",
        "sort_order": 5,
    },
    "price-of-gold": {
        "name": "Price of Gold",
        "description": "Analysis of the gold price and its effect on junior mining equities — supply-demand, real rates, central-bank buying, and company-level sensitivity.",
        "sort_order": 6,
    },
}


def seed_intros(apps, schema_editor):
    Pillar = apps.get_model("blog", "Pillar")
    for slug, intro in PILLAR_INTROS.items():
        defaults = PILLAR_DEFAULTS.get(slug, {})
        obj, _ = Pillar.objects.get_or_create(slug=slug, defaults=defaults)
        obj.intro_html = intro
        obj.save(update_fields=["intro_html"])


def reverse_seed(apps, schema_editor):
    Pillar = apps.get_model("blog", "Pillar")
    Pillar.objects.filter(slug__in=PILLAR_INTROS.keys()).update(intro_html="")


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0007_pillar_intro_html"),
    ]
    operations = [
        migrations.RunPython(seed_intros, reverse_seed),
    ]
