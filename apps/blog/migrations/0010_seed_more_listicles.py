"""
Seed listicles 6-20 (the remaining 5 from the original 10, plus 10 new).
Also creates placeholder Company records for any tickers mentioned in the
new listicles that weren't already on the coverage list — those are flagged
with needs_research=True so the research agent can pick them up and
generate full scorecards.

Publish schedule: one per day from 2026-04-28 through 2026-05-12, continuing
the daily cadence after the 5 listicles seeded in migration 0009.
"""
from datetime import timedelta, datetime, timezone as dt_timezone
from django.db import migrations


# ────────────────────────────────────────────────────────────────────────
# New Company placeholders — created with needs_research=True so the
# research agent picks them up for scoring. All are well-known Canadian
# gold/silver producers or royalty companies that the listicles reference.
# ────────────────────────────────────────────────────────────────────────
NEW_COMPANIES = [
    # Mid-tier / major gold producers
    {"ticker": "NGT", "exchange": "TSX",  "name": "Newmont Corporation",      "primary_commodity": "Gold",   "jurisdiction": "Global"},
    {"ticker": "BTO", "exchange": "TSX",  "name": "B2Gold Corp.",             "primary_commodity": "Gold",   "jurisdiction": "Mali, Philippines, Namibia"},
    {"ticker": "AGI", "exchange": "TSX",  "name": "Alamos Gold Inc.",         "primary_commodity": "Gold",   "jurisdiction": "Canada, Mexico"},
    {"ticker": "WDO", "exchange": "TSX",  "name": "Wesdome Gold Mines Ltd.",  "primary_commodity": "Gold",   "jurisdiction": "Quebec, Ontario"},
    {"ticker": "LUG", "exchange": "TSX",  "name": "Lundin Gold Inc.",         "primary_commodity": "Gold",   "jurisdiction": "Ecuador"},
    {"ticker": "MUX", "exchange": "TSX",  "name": "McEwen Mining Inc.",       "primary_commodity": "Gold",   "jurisdiction": "USA, Canada, Mexico, Argentina"},
    # Silver producers / polymetallic
    {"ticker": "AYA", "exchange": "TSX",  "name": "Aya Gold & Silver Inc.",   "primary_commodity": "Silver", "jurisdiction": "Morocco"},
    {"ticker": "MAG", "exchange": "TSX",  "name": "MAG Silver Corp.",         "primary_commodity": "Silver", "jurisdiction": "Mexico"},
    {"ticker": "PAAS","exchange": "TSX",  "name": "Pan American Silver Corp.","primary_commodity": "Silver", "jurisdiction": "Americas"},
    {"ticker": "FVI", "exchange": "TSX",  "name": "Fortuna Mining Corp.",     "primary_commodity": "Silver", "jurisdiction": "Americas, West Africa"},
    {"ticker": "SVM", "exchange": "TSX",  "name": "Silvercorp Metals Inc.",   "primary_commodity": "Silver", "jurisdiction": "China, Ecuador"},
    {"ticker": "EDR", "exchange": "TSX",  "name": "Endeavour Silver Corp.",   "primary_commodity": "Silver", "jurisdiction": "Mexico, Chile"},
    # Royalty / streaming
    {"ticker": "WPM", "exchange": "TSX",  "name": "Wheaton Precious Metals Corp.", "primary_commodity": "Gold", "jurisdiction": "Global (royalty)"},
    {"ticker": "OR",  "exchange": "TSX",  "name": "Osisko Gold Royalties Ltd.",    "primary_commodity": "Gold", "jurisdiction": "Global (royalty)"},
    # BC explorer / developer
    {"ticker": "ARTG","exchange": "TSXV", "name": "Artemis Gold Inc.",        "primary_commodity": "Gold",   "jurisdiction": "British Columbia"},
]


# ────────────────────────────────────────────────────────────────────────
# Listicles 6-20
# ────────────────────────────────────────────────────────────────────────
LISTICLES = [
    # ──────────────── #6 — Management ────────────────
    {
        "title": "Junior Gold Miners with the Best Management: Insider Ownership in 2026",
        "meta_title": "Best Management in Junior Gold Mining 2026",
        "meta_description": (
            "Ten gold equities scoring 4/5 or 5/5 on management in our Verdict Framework. "
            "Insider ownership and alignment ranked for April 2026."
        ),
        "pillar_slug": "investing-guides",
        "excerpt": (
            "Management skin-in-the-game is the single factor most strongly correlated with "
            "outcomes in junior mining. Ten companies that scored 4/5 or 5/5 on our management "
            "factor in April 2026, ranked."
        ),
        "answer_capsule": (
            "Ten gold equities scored 4/5 or 5/5 on the management factor of our Verdict Framework "
            "in April 2026. Franco-Nevada, G2 Goldfields, and Collective Mining scored a perfect "
            "5/5. Amex Exploration, Fury Gold Mines, Heliostar Metals, Probe Gold, Snowline Gold, "
            "Integra Resources, and Osisko Development rounded out the top ten at 4/5."
        ),
        "key_takeaways": [
            "Management factor is weighted heavily because poor alignment rarely self-corrects",
            "Three companies scored a perfect 5/5: Franco-Nevada, G2 Goldfields, Collective Mining",
            "Insider open-market buying and meaningful option discipline are the primary signals",
            "A high management score does not guarantee execution — but a low score usually breaks theses",
            "Seven of the top ten have a composite score of 19 or higher",
        ],
        "ranked_items": [
            {"rank": 1, "name": "Franco-Nevada Corp.", "ticker": "TSX:FNV", "company_slug": "franco-nevada-corp",
             "summary": "Management 5/5. Decades-long track record of disciplined capital allocation, "
                        "no debt, and consistent insider alignment. The gold standard for the factor — literally."},
            {"rank": 2, "name": "G2 Goldfields Inc.", "ticker": "TSX:GTWO", "company_slug": "g2-goldfields-inc",
             "summary": "Management 5/5. Meaningful insider open-market buying. Seasoned Guyana "
                        "operator with track record on prior South American ventures."},
            {"rank": 3, "name": "Collective Mining Ltd.", "ticker": "TSX:CNL", "company_slug": "collective-mining-ltd",
             "summary": "Management 5/5. The highest-scoring team on a project (Guayabales, Colombia) "
                        "the framework scores 2/5 on geology — a pattern worth noting when evaluating teams."},
            {"rank": 4, "name": "Amex Exploration Inc.", "ticker": "TSXV:AMX", "company_slug": "amex-exploration-inc",
             "summary": "Management 4/5. Aligned ownership and disciplined share issuance through the "
                        "Perron resource-definition cycle."},
            {"rank": 5, "name": "Fury Gold Mines Limited", "ticker": "TSX:FURY", "company_slug": "fury-gold-mines-limited",
             "summary": "Management 4/5. The balanced-4 BUY. Insider ownership supported by "
                        "a pragmatic approach to portfolio prioritisation across Quebec and Newfoundland."},
            {"rank": 6, "name": "Heliostar Metals Ltd.", "ticker": "TSXV:HSTR", "company_slug": "heliostar-metals-ltd",
             "summary": "Management 4/5. A producer-developer team running Mexican operations as "
                        "a cash-flow base for exploration. Rare discipline on the TSX-V."},
            {"rank": 7, "name": "Probe Gold Inc.", "ticker": "TSX:PRB", "company_slug": "probe-gold-inc",
             "summary": "Management 4/5. Quebec-focused team with meaningful insider positions "
                        "and a measured financing cadence through exploration advance."},
            {"rank": 8, "name": "Snowline Gold Corp.", "ticker": "TSX:SGD", "company_slug": "snowline-gold-corp",
             "summary": "Management 4/5. Yukon-focused discovery story carried through discovery "
                        "and delineation phases with a stable team and disciplined capital raises."},
            {"rank": 9, "name": "Integra Resources Corp.", "ticker": "TSXV:ITR", "company_slug": "integra-resources-corp",
             "summary": "Management 4/5. Idaho-focused developer with a team that has steered "
                        "the DeLamar project through multiple engineering study iterations without dilutive misfires."},
            {"rank": 10, "name": "Osisko Development Corp.", "ticker": "TSXV:ODV", "company_slug": "osisko-development-corp",
             "summary": "Management 4/5. Carries the Osisko-group pedigree. Cariboo Gold "
                        "project in BC managed through permitting and engineering with operator-grade discipline."},
        ],
        "body": """
<h2>Why the management factor is weighted heavily</h2>
<p>Of the five factors in the Verdict Framework, management is the one where the score tends to
persist. A broken cap table can be fixed through a disciplined financing. A deficient geology
score can improve with drilling. A weak catalyst score improves naturally as milestones approach.
A management score of 2/5 rarely climbs to 4/5 on the same team — people don't change who they
are, and the incentive structure of a junior mining company does not reward behavioral shifts
once they're established.</p>

<p>That's why we weight the factor the way we do. The other four factors describe the asset and
the company's current state. Management describes the probability that the company's decisions
over the next 24–36 months will compound toward or away from the asset's potential.</p>

<h2>What we actually score</h2>
<p>Four public data points drive the score. First, insider ownership as a percentage of the fully
diluted share count, sourced from the most recent management information circular. Second, recent
open-market insider buying on SEDI — shares purchased on the public market, distinct from option
exercises and participation in financings. Third, share-issuance discipline: have prior financings
been done at punitive discounts to VWAP with excessive warrant coverage, or at reasonable terms.
Fourth, the track record of prior ventures the current team has operated.</p>

<p>A 5/5 score requires all four to be strong. A 4/5 requires three of the four with no red flags.
A 3/5 is the median — fine, but nothing to write home about. A 2/5 or 1/5 lands on companies
where one or more of the four points is actively a problem.</p>

<h2>What a high management score does not guarantee</h2>
<p>It does not guarantee execution. Collective Mining is a useful example: the team scored 5/5,
but the underlying geology of Guayabales scored 2/5 at the time of the last scorecard. No amount
of management alignment changes the rocks in the ground. A strong team on a weak asset typically
produces a slow bleed rather than a catastrophe — the team navigates financings carefully, the
project makes incremental progress, but the value inflection never arrives because the asset
doesn't support one.</p>

<p>The interesting cases are the inverse: strong asset, weak management. Those are where the
framework will sometimes issue an AVOID verdict even when a composite score looks decent — a
single-factor score of 1 on management triggers AVOID regardless of the composite. The rationale
is simple. A strong asset in weak hands gets diluted away before it delivers.</p>

<h2>How to use this list</h2>
<p>Start with the management-strong names when evaluating sector-adjacent juniors. If you're
looking at a new TSX-V gold name and its management score would be lower than anyone on this
list, the burden of proof for owning it is higher. A strong-management name usually trades at
a premium to comparable-asset peers for a reason.</p>
""",
        "faq_items": [
            {"question": "What does a 5/5 management score mean?",
             "answer": "It means meaningful insider ownership as a percentage of fully-diluted shares, recent open-market insider buying, a history of non-dilutive or reasonably-priced financings, and a track record on prior ventures. All four must be in place. Three companies in our coverage universe hold a 5/5 as of April 2026."},
            {"question": "Why does the framework weight management heavily?",
             "answer": "Because management behavior rarely self-corrects. Capital structure issues, geological disappointments, and catalyst delays all tend to resolve over time. A team with weak incentive alignment typically stays weak — and compounds the damage over subsequent financings."},
            {"question": "How do you distinguish insider buying from option exercises?",
             "answer": "SEDI (in Canada) distinguishes transaction codes. Open-market purchases are coded differently from option exercises and automatic-plan dispositions. Only real open-market purchases count toward the factor score."},
            {"question": "Can a high-management-score company still fail?",
             "answer": "Yes. Collective Mining scored 5/5 on management and 2/5 on geology. Strong teams on weak assets typically produce a slow grind, not a catastrophe — but they don't produce the value inflection a junior miner exists to deliver."},
        ],
    },
    # ──────────────── #7 — Capital Structure ────────────────
    {
        "title": "Best-Capitalized Junior Gold Miners: Clean Cap Tables in 2026",
        "meta_title": "Best-Capitalized Junior Gold Miners 2026: Clean Cap Tables",
        "meta_description": (
            "Ten gold equities scoring 4/5 or 5/5 on capital structure in our Verdict Framework. "
            "Cap tables, warrant overhang, runway ranked."
        ),
        "pillar_slug": "investing-guides",
        "excerpt": (
            "Clean cap tables are rare in junior mining. Ten names that scored 4/5 or 5/5 on the "
            "capital structure factor of our Verdict Framework in April 2026, sorted by composite."
        ),
        "answer_capsule": (
            "Ten gold or gold-adjacent equities scored 4/5 or 5/5 on capital structure in April 2026: "
            "Franco-Nevada and Collective Mining and Mako Mining at 5/5, plus GoGold Resources, "
            "Fury Gold Mines, Heliostar Metals, Equinox Gold, Integra Resources, Probe Gold, "
            "Snowline Gold, and Western Copper and Gold at 4/5. The factor captures warrant "
            "overhang, dilution history, and working-capital runway."
        ),
        "key_takeaways": [
            "Capital structure is the factor that converts good theses into bad returns when it breaks",
            "A 5/5 capital score requires clean warrant status, low dilution pace, and 12+ months of runway",
            "Mako Mining is the only TSX-V junior scoring 5/5 on capital — a rarity on that exchange",
            "Mid-tier Equinox Gold is on the list — producers sometimes mask weaker cap discipline than juniors",
            "Low P/NAV combined with a 2/5 capital score is almost always a value trap",
        ],
        "ranked_items": [
            {"rank": 1, "name": "Franco-Nevada Corp.", "ticker": "TSX:FNV", "company_slug": "franco-nevada-corp",
             "summary": "Capital 5/5. No debt, diversified royalty portfolio, consistent cash generation. The cleanest structure on any gold equity we score."},
            {"rank": 2, "name": "GoGold Resources Inc.", "ticker": "TSX:GGD", "company_slug": "gogold-resources-inc",
             "summary": "Capital 4/5. Silver-primary (Mexico). Managed the Parral and Los Ricos expansion without excessive dilution — rare for a mid-cycle developer."},
            {"rank": 3, "name": "Fury Gold Mines Limited", "ticker": "TSX:FURY", "company_slug": "fury-gold-mines-limited",
             "summary": "Capital 4/5. Clean share count through multiple exploration cycles. Warrant overhang is manageable relative to the portfolio size."},
            {"rank": 4, "name": "Heliostar Metals Ltd.", "ticker": "TSXV:HSTR", "company_slug": "heliostar-metals-ltd",
             "summary": "Capital 4/5. Mexican production funds the exploration program. Low dependence on equity issuance is the differentiator."},
            {"rank": 5, "name": "Mako Mining Corp.", "ticker": "TSXV:MKO", "company_slug": "mako-mining-corp",
             "summary": "Capital 5/5. The outlier on the TSX-V. Positive operating cash flow from San Albino (Nicaragua) has allowed near-zero dilution through recent cycles."},
            {"rank": 6, "name": "Equinox Gold Corp.", "ticker": "TSX:EQX", "company_slug": "equinox-gold-corp",
             "summary": "Capital 4/5. Americas-focused mid-tier. Leverage is manageable and warrant overhang from the M&A history has largely worked through."},
            {"rank": 7, "name": "Integra Resources Corp.", "ticker": "TSXV:ITR", "company_slug": "integra-resources-corp",
             "summary": "Capital 4/5. Multiple years of runway through engineering studies on DeLamar. Quiet discipline relative to peer developers."},
            {"rank": 8, "name": "Probe Gold Inc.", "ticker": "TSX:PRB", "company_slug": "probe-gold-inc",
             "summary": "Capital 4/5. Quebec-focused. Share issuance cadence through resource definition has kept fully-diluted share count within a reasonable band."},
            {"rank": 9, "name": "Snowline Gold Corp.", "ticker": "TSX:SGD", "company_slug": "snowline-gold-corp",
             "summary": "Capital 4/5. Yukon. Carried discovery and early resource work without forcing dilution through drill seasons."},
            {"rank": 10, "name": "Western Copper and Gold Corporation", "ticker": "TSX:WRN", "company_slug": "western-copper-and-gold-corporation",
             "summary": "Capital 4/5. The Casino project has permitting costs that have been managed without punitive raises."},
        ],
        "body": """
<h2>Why capital structure is the boring factor that decides outcomes</h2>
<p>A junior miner exists to convert capital into discovery, discovery into resources, resources
into development, development into production. At every stage, the primary risk is not that the
geology will fail — it's that the company will run out of cash before it gets to the next
milestone, and will have to raise money at punitive terms to survive. Capital structure is how
we score whether a company is positioned to avoid that outcome.</p>

<p>Four inputs drive the capital score. Fully-diluted share count relative to the asset (bigger
assets can carry bigger share counts). Warrant overhang — how many out-of-the-money or
near-the-money warrants are outstanding and what's their strike pattern. Dilution history — has
the company raised at progressively better or worse terms over its history. And working-capital
runway — how many months of general and administrative expenses plus exploration/development
spend can current cash cover at the current burn rate.</p>

<h2>Why producers can show up on a cap-table list</h2>
<p>Equinox Gold and Franco-Nevada on this list are worth thinking about. Producers generate cash
flow, which means the burn-rate input flips from negative to positive. But producers also carry
debt, and a producer with $500M of debt against $600M of EBITDA has a structurally different
capital posture than a debt-free junior with $10M of cash and a 3-year runway. The framework
treats both on the same 5-point scale because both can be bankrupted by the same structural
problem: running out of liquidity before the next milestone.</p>

<p>Mako Mining is the more interesting case on this list. Mako is the only TSX-V junior scoring
5/5 on capital — a rarity on an exchange where most names are pre-revenue and funded through
successive equity raises. The difference is San Albino's operating cash flow, which converts Mako
from a capital-consuming explorer into a self-funding producer-developer. That category —
TSX-V producer-developer — is small and worth tracking specifically.</p>

<h2>The low-cap-score trap</h2>
<p>The worst combination in junior mining is a high composite score on geology and catalyst
combined with a low score on capital. Those companies usually look like "a great project waiting
for the right financing" — but the right financing rarely arrives, and when it does, it arrives
at terms that transfer most of the remaining value to the financier. Check the capital score
before anchoring on P/NAV or catalyst math. A 2/5 capital score in combination with a low P/NAV
is almost always a value trap, not a bargain.</p>

<h2>How the list evolves</h2>
<p>Capital scores move most often. A single clean financing can upgrade a name from 2/5 to 3/5 or
3/5 to 4/5 in one quarter. Similarly, a punitive raise can degrade a 4/5 to 3/5 overnight.
Expect composition changes each quarter as cap tables shift with financing activity.</p>
""",
        "faq_items": [
            {"question": "What does a 5/5 capital structure score mean?",
             "answer": "A clean share count relative to the asset, minimal warrant overhang, a history of non-dilutive financings (or at least reasonably-priced ones), and 12+ months of working-capital runway. Three of our covered companies hold 5/5 as of April 2026."},
            {"question": "Is a low P/NAV with a strong capital score a buy signal?",
             "answer": "It's a better signal than a low P/NAV alone. Weak capital often explains a low P/NAV — the market is pricing in future dilution. A low P/NAV with a 4/5 or 5/5 capital score suggests the discount is driven by a different factor (jurisdiction, catalyst timing, or simple mis-pricing)."},
            {"question": "Why doesn't every producer score 4/5 or 5/5 on capital?",
             "answer": "Producers can carry debt that offsets operating cash flow. A mid-tier with leveraged operations in weaker jurisdictions can score 2/5 or 3/5 even with hundreds of millions of EBITDA — the framework is tier-agnostic and applies the same liquidity-and-alignment rubric to producers as to explorers."},
            {"question": "How fast can a capital score change?",
             "answer": "One quarter. A single clean financing can lift a score from 2/5 to 3/5. A punitive raise (deep discount to VWAP, excessive warrant coverage) can drop a score by a point overnight. Expect the list to churn each quarter."},
        ],
    },
    # ──────────────── #8 — Catalyst ────────────────
    {
        "title": "Gold Stocks Near Their Next Big Catalyst: 2026 Watchlist",
        "meta_title": "Gold Stocks Near Their Next Catalyst 2026",
        "meta_description": (
            "Ten gold equities with catalyst scores of 4/5 or 5/5. Drill results, resource "
            "updates, PEA/PFS milestones coming in 2026."
        ),
        "pillar_slug": "market-commentary",
        "excerpt": (
            "Ten companies where the framework's catalyst factor scored 4/5 or 5/5 in April 2026. "
            "The next material news event — drill result, resource update, PEA/PFS, permit — is "
            "within a 12-month window."
        ),
        "answer_capsule": (
            "Ten gold-focused equities score 4/5 or higher on catalyst proximity in April 2026. "
            "Amex Exploration, G2 Goldfields, GoGold Resources, Heliostar Metals, and 1911 Gold "
            "scored a perfect 5/5. Franco-Nevada, Fury, Probe, Snowline, and Mako fill out the "
            "4/5 tier. All are within 12 months of a material news event."
        ),
        "key_takeaways": [
            "Catalyst score of 5/5 means a material news event within 12 months — direction not guaranteed",
            "Five companies currently hold a 5/5 catalyst score",
            "Missed catalysts are often more damaging to share price than never having one",
            "Drill results are the most common catalyst; PEA/PFS and permits are slower but more material",
            "Catalyst-heavy names carry binary event risk — position-size accordingly",
        ],
        "ranked_items": [
            {"rank": 1, "name": "Amex Exploration Inc.", "ticker": "TSXV:AMX", "company_slug": "amex-exploration-inc",
             "summary": "Catalyst 5/5. Resource update pending on Perron (Quebec). The next material milestone is on the calendar and credibility is high."},
            {"rank": 2, "name": "G2 Goldfields Inc.", "ticker": "TSX:GTWO", "company_slug": "g2-goldfields-inc",
             "summary": "Catalyst 5/5. Aggressive drill program in Guyana with multi-rig cadence. Regular assay flow is the thesis engine."},
            {"rank": 3, "name": "GoGold Resources Inc.", "ticker": "TSX:GGD", "company_slug": "gogold-resources-inc",
             "summary": "Catalyst 5/5. Los Ricos (Mexico) development progression plus ongoing resource additions from Parral."},
            {"rank": 4, "name": "Heliostar Metals Ltd.", "ticker": "TSXV:HSTR", "company_slug": "heliostar-metals-ltd",
             "summary": "Catalyst 5/5. Mexican producer-developer with a busy 2026 schedule of drill releases and a permitting milestone at Ana Paula."},
            {"rank": 5, "name": "1911 Gold Corporation", "ticker": "TSXV:AUMB", "company_slug": "1911-gold-corporation",
             "summary": "Catalyst 5/5. Rice Lake (Manitoba). Exploration cadence is tight and the next resource-relevant result is imminent at the time of scoring."},
            {"rank": 6, "name": "Franco-Nevada Corp.", "ticker": "TSX:FNV", "company_slug": "franco-nevada-corp",
             "summary": "Catalyst 4/5. Quarterly earnings are the periodic catalyst; acquisition-level catalysts are less predictable but regularly announced."},
            {"rank": 7, "name": "Fury Gold Mines Limited", "ticker": "TSX:FURY", "company_slug": "fury-gold-mines-limited",
             "summary": "Catalyst 4/5. Quebec and Newfoundland portfolio generating ongoing exploration results. No single blockbuster pending but consistent news flow."},
            {"rank": 8, "name": "Probe Gold Inc.", "ticker": "TSX:PRB", "company_slug": "probe-gold-inc",
             "summary": "Catalyst 4/5. Quebec. Resource-definition drilling on Novador complex generates regular assay flow."},
            {"rank": 9, "name": "Snowline Gold Corp.", "ticker": "TSX:SGD", "company_slug": "snowline-gold-corp",
             "summary": "Catalyst 4/5. Valley project (Yukon). Drilling continues on the flagship plus satellite targets."},
            {"rank": 10, "name": "Mako Mining Corp.", "ticker": "TSXV:MKO", "company_slug": "mako-mining-corp",
             "summary": "Catalyst 4/5. San Albino (Nicaragua) production updates plus exploration from adjacent concessions."},
        ],
        "body": """
<h2>What a catalyst score actually measures</h2>
<p>The catalyst factor of the Verdict Framework scores the proximity of the next material news
event that can move a company's share price. Materiality is defined by the framework itself:
drill results that could define or expand a resource, resource estimates and updates, preliminary
economic assessments (PEA), pre-feasibility studies (PFS), feasibility studies (FS), permit
decisions, offtake agreements, and strategic financings. Routine quarterly updates and press
releases that don't change the underlying technical case do not count.</p>

<p>A 5/5 catalyst score means the next material event is within 12 months — typically within
6 months — and is credibly signposted by management guidance or clearly implied by the work
program. A 4/5 score widens the window to 12–18 months or reflects a multi-milestone program
where the catalyst density is high without any single event dominating.</p>

<h2>Why catalyst-heavy names are not for everyone</h2>
<p>Catalysts are bidirectional. A 5/5 catalyst score tells you the next event is close. It does
not tell you whether that event will be positive. The worst outcomes in junior mining — short-term
50%+ drawdowns on well-owned names — almost always follow a missed or disappointing catalyst,
not a permitting delay or a macro event. Size catalyst-heavy positions smaller than balance-sheet
or geology-anchored positions for this reason.</p>

<p>A useful rule of thumb: double the position size you'd own on a 3/5 catalyst name (background
newsflow only) should probably be halved on a 5/5 catalyst name (imminent binary). The expected
value can be the same; the path to realising it is wider.</p>

<h2>Catalyst type matters</h2>
<p>Not all catalysts carry equal weight. Ranked roughly by materiality:</p>
<ul>
  <li><strong>Feasibility study</strong> — the most material catalyst a developer can deliver.
  A positive FS establishes project economics and unlocks the financing path to production.</li>
  <li><strong>Resource update</strong> — a new NI 43-101 resource estimate that expands tonnes or
  grade (or reclassifies ounces from inferred to indicated) materially re-prices the asset.</li>
  <li><strong>PEA / PFS</strong> — preliminary and pre-feasibility studies rank below FS but still
  shift the NPV and sensitivity math that drives P/NAV calculations.</li>
  <li><strong>Drill results</strong> — high-impact drill results (especially step-out holes on
  virgin ground or infill on well-understood systems) can move share prices 20–40% in a day.</li>
  <li><strong>Permit decisions</strong> — slow, binary, and materially important for developers.
  A positive permit decision can re-rate a project by the full permitting-risk discount.</li>
  <li><strong>Offtake / strategic investment</strong> — validation events that signal industrial
  demand or major-company interest.</li>
</ul>

<h2>How the list evolves</h2>
<p>Catalyst scores naturally decay. A 5/5 today is often a 3/5 in six months because the catalyst
has been delivered and the next material event is further out. Expect this list to turn over
almost completely every two quarters.</p>
""",
        "faq_items": [
            {"question": "What's the difference between a 4/5 and a 5/5 catalyst score?",
             "answer": "5/5 means the next material event is within 6 months or is credibly on the calendar. 4/5 widens the window to 12–18 months or reflects a multi-milestone program where the catalyst density is high without any single dominating event."},
            {"question": "Can a high catalyst score predict share price direction?",
             "answer": "No. It predicts timing, not direction. The framework scores catalyst proximity and materiality — whether the catalyst delivers a positive or negative outcome depends on the underlying technical work, which is scored separately in the geology factor."},
            {"question": "What happens to a company's catalyst score after a catalyst delivers?",
             "answer": "It typically drops by one or two points. A 5/5 catalyst score after a resource update lands is often a 3/5 three months later because the next material event is now further out. Expect the list to turn over every two quarters."},
            {"question": "Which catalyst type moves share prices the most?",
             "answer": "In order of typical materiality: feasibility studies, resource updates, PEA/PFS, high-impact drill results, permit decisions, and strategic investments. A positive feasibility study can double a developer's share price; a missed drill result can halve it."},
        ],
    },
    # ──────────────── #9 — Acquisition Value ────────────────
    {
        "title": "Most Undervalued Mining Stocks: The Acquisition-Value Play in 2026",
        "meta_title": "Most Undervalued Mining Stocks 2026: Acquisition Value",
        "meta_description": (
            "Seven gold equities scoring 4/5 on acquisition value. Trading at meaningful discounts "
            "to comparable M&A transactions in April 2026."
        ),
        "pillar_slug": "investing-guides",
        "excerpt": (
            "The framework scores acquisition value by benchmarking a company's current valuation "
            "against comparable M&A transactions in the same commodity and jurisdiction. Seven "
            "names scored 4/5 in April 2026."
        ),
        "answer_capsule": (
            "Seven gold equities scored 4/5 on the acquisition-value factor in April 2026: Amex "
            "Exploration, Fury Gold Mines, Western Copper and Gold, Probe Gold, Integra Resources, "
            "Calibre Mining, and Cartier Resources. Each trades at a meaningful discount to comparable "
            "transactions in its commodity and jurisdiction."
        ),
        "key_takeaways": [
            "Acquisition value benchmarks a company against trailing 24-month comparable M&A transactions",
            "A 4/5 score means a meaningful implied takeout premium to current trading price",
            "The factor does not predict that a takeover will happen — only that the math supports one",
            "Quebec and Yukon dominate the list — both are active M&A jurisdictions",
            "Combined with a catalyst score of 4+, acquisition value becomes a time-bound thesis",
        ],
        "ranked_items": [
            {"rank": 1, "name": "Amex Exploration Inc.", "ticker": "TSXV:AMX", "company_slug": "amex-exploration-inc",
             "summary": "Acquisition value 4/5. Perron (Quebec) comps strongly against recent Abitibi-region transactions. Grade and scale both support an in-region takeout premium."},
            {"rank": 2, "name": "Fury Gold Mines Limited", "ticker": "TSX:FURY", "company_slug": "fury-gold-mines-limited",
             "summary": "Acquisition value 4/5. Diversified Quebec + Newfoundland portfolio of projects any of which could attract a consolidator. P/NAV of 0.55x reinforces the discount."},
            {"rank": 3, "name": "Western Copper and Gold Corporation", "ticker": "TSX:WRN", "company_slug": "western-copper-and-gold-corporation",
             "summary": "Acquisition value 4/5. Casino (Yukon) is one of the largest undeveloped copper-gold-moly assets in North America. Major-company M&A focus on large-scale copper anchors the score."},
            {"rank": 4, "name": "Probe Gold Inc.", "ticker": "TSX:PRB", "company_slug": "probe-gold-inc",
             "summary": "Acquisition value 4/5. Novador complex (Quebec) scale and location — near existing mill infrastructure — support a strategic-premium framing."},
            {"rank": 5, "name": "Integra Resources Corp.", "ticker": "TSXV:ITR", "company_slug": "integra-resources-corp",
             "summary": "Acquisition value 4/5. DeLamar (Idaho, USA) heap-leach project at a valuation below recent USA heap-leach comparable transactions."},
            {"rank": 6, "name": "Calibre Mining Corp.", "ticker": "TSX:CXB", "company_slug": "calibre-mining-corp",
             "summary": "Acquisition value 4/5. Multi-asset producer across Nicaragua and Nevada. The asset mix trades below what any single buyer would pay for the components."},
            {"rank": 7, "name": "Cartier Resources Inc.", "ticker": "TSXV:ECR", "company_slug": "cartier-resources-inc",
             "summary": "Acquisition value 4/5. Chimo Mine (Quebec). Historic mine with modern drill targets at a valuation well below recent Abitibi brownfield transactions."},
        ],
        "body": """
<h2>What the acquisition-value factor actually measures</h2>
<p>The acquisition-value factor scores a company's current valuation against the comparable-sales
universe — the trailing 24 months of M&A transactions in the same commodity and, ideally, the
same jurisdiction. The framework maintains a rolling comparables table that feeds this factor.
Every time a junior miner is acquired, the transaction metrics get logged: price per ounce
in the ground, P/NAV multiple paid, payment currency, premium to the prior 30-day VWAP,
resource category at close. Those metrics become the denominator against which our covered
companies are benchmarked.</p>

<p>A 4/5 score means a meaningful implied takeout premium — typically 30-60% — to the current
trading price based on where comparable assets have transacted. A 5/5 would require an extreme
mispricing, which the market usually closes before the framework picks it up; that's why there
are no 5/5 acquisition-value scores in our April 2026 universe.</p>

<h2>What the factor is not</h2>
<p>It is not a prediction that a takeover will happen. The math supports one; the corporate action
requires a specific buyer with a specific strategic rationale and capital at the right point in
its own cycle. Most 4/5 acquisition-value companies never get acquired. What they tend to do
instead is re-rate closer to comparable-transaction pricing organically as the market catches
up to the disconnect, or as management delivers a catalyst that makes the mispricing untenable.</p>

<p>The factor is also not a safety net. If the broader sector re-prices down — a gold-price
correction, a jurisdictional risk event — acquisition-value anchors drop along with everything
else. The factor captures relative mispricing, not absolute value.</p>

<h2>Why Quebec keeps showing up</h2>
<p>Three of the seven names on this list are in Quebec: Amex, Probe Gold, and Cartier. That's not
coincidental. Quebec has been the single most active M&A jurisdiction in junior gold over the
trailing 24 months, which means the comparable-transactions set is rich, recent, and directly
applicable. When a framework says a Quebec gold junior trades at a 40% discount to comp
transactions, that math rests on actual recent deals rather than dated or cross-jurisdictional
analogs.</p>

<h2>Combining with other factors</h2>
<p>An acquisition-value score by itself is a static snapshot. Combined with a catalyst score of
4/5 or 5/5, it becomes a time-bound thesis: the company trades at a discount today, a catalyst
is due within 12 months, and the catalyst is the most plausible trigger for the valuation to
close. Amex Exploration (acq 4, catalyst 5), Probe Gold (acq 4, catalyst 4), and Fury Gold Mines
(acq 4, catalyst 4) each fit that pattern. That combination is where this factor becomes most
actionable for a position.</p>
""",
        "faq_items": [
            {"question": "What counts as a comparable transaction?",
             "answer": "M&A transactions over the trailing 24 months in the same commodity (gold, copper, silver) and ideally the same jurisdiction. The framework prioritises transactions where the target's resource category and development stage match the company being scored."},
            {"question": "Does a 4/5 acquisition value score mean the company will be acquired?",
             "answer": "No. It means the math supports a takeout at a premium. Actual M&A requires a buyer with a specific strategic rationale and capital at the right point in their cycle. Most 4/5 names re-rate organically rather than get acquired."},
            {"question": "Why are there no 5/5 acquisition-value scores?",
             "answer": "A 5/5 would require an extreme mispricing — typically 70%+ implied takeout premium. The market usually closes those before our framework picks them up. A 4/5 (30-60% implied premium) is the highest score we see in practice."},
            {"question": "How does acquisition value interact with P/NAV?",
             "answer": "P/NAV uses engineering-study NAV; acquisition value uses recent M&A pricing. They answer different questions. A low P/NAV with a 4/5 acquisition value is the strongest combined signal — the engineering math and the transaction math both point the same direction."},
        ],
    },
    # ──────────────── #10 — Royalty & Streaming ────────────────
    {
        "title": "Royalty and Streaming Stocks: Why Franco-Nevada Still Earns a BUY",
        "meta_title": "Royalty and Streaming Gold Stocks 2026: Franco-Nevada Explained",
        "meta_description": (
            "Royalty and streaming companies offer gold exposure without operational risk. "
            "Why Franco-Nevada rates BUY on our framework."
        ),
        "pillar_slug": "investing-guides",
        "excerpt": (
            "Franco-Nevada is the only royalty or streaming company currently on our active "
            "coverage list, and it holds a BUY verdict. Here's why the model rates so well on "
            "our framework — and how the broader royalty peer set compares."
        ),
        "answer_capsule": (
            "Franco-Nevada holds a 21/25 BUY verdict on the Verdict Framework as of April 2026. "
            "The royalty and streaming model — no operational risk, no per-project capex, "
            "portfolio-diversified cash flow — structurally scores well on capital structure "
            "(5/5) and management (5/5). Wheaton Precious Metals and Osisko Gold Royalties are "
            "the primary peers; neither has been scored yet."
        ),
        "key_takeaways": [
            "Royalty and streaming companies earn a share of mine revenue without operational risk",
            "Franco-Nevada scores 5/5 on both management and capital structure",
            "The model trades at a P/NAV premium (1.12x for FNV) because operational risk is absent",
            "Royalty names are the defensive anchor in a gold portfolio, not the leveraged bet",
            "Major peers — Wheaton, Osisko Royalties, Sandstorm, Triple Flag — sit outside our current coverage",
        ],
        "ranked_items": [
            {"rank": 1, "name": "Franco-Nevada Corp.", "ticker": "TSX:FNV", "company_slug": "franco-nevada-corp",
             "summary": "Composite 21/25 BUY. No debt, diversified royalty portfolio across gold, copper, oil and gas, and precious-metal streams. The defensive anchor in a precious-metals portfolio."},
            {"rank": 2, "name": "Wheaton Precious Metals Corp.", "ticker": "TSX:WPM", "company_slug": "wheaton-precious-metals-corp",
             "summary": "Not yet scored on the framework. Primary gold and silver streaming company with a globally diversified stream portfolio. Coverage is queued for next research cycle."},
            {"rank": 3, "name": "Osisko Gold Royalties Ltd.", "ticker": "TSX:OR", "company_slug": "osisko-gold-royalties-ltd",
             "summary": "Not yet scored on the framework. Canadian-anchored royalty portfolio with notable positions on Canadian Malartic (Agnico-run) and other Quebec assets. Queued for coverage."},
        ],
        "body": """
<h2>Why the royalty and streaming model scores well</h2>
<p>A royalty company receives a percentage of revenue or net profits from a mining operation in
exchange for an upfront payment that helped finance the mine. A streaming company pays for the
right to purchase a percentage of a mine's metal production at a pre-agreed price, typically well
below spot. Both models earn a share of mine economics without taking the operational risk of
actually operating the mine. No capital expenditures per project, no labor cost, no cost
overruns, no environmental permits. The operator takes those risks; the royalty or streaming
company takes the price risk on the underlying commodity.</p>

<p>Structurally, that makes the model score well on our framework. Capital structure (5/5) is
natural — royalty companies rarely need to raise equity because they fund new royalties from
cash flow. Management (5/5) reflects the long-run discipline required: royalty companies that
over-pay for streams during bull markets blow up; the ones that build durable portfolios have
typically had decades of measured deal-making. Franco-Nevada is the archetypal example.</p>

<h2>The trade-off: premium valuation</h2>
<p>Royalty and streaming companies almost universally trade at P/NAV premiums — Franco-Nevada
at 1.12x, Wheaton Precious Metals historically above 1.5x, Osisko Royalties around 1.0–1.2x. The
premium is earned: absence of operational risk and smooth cash flows are worth paying for in a
portfolio context. But it caps upside in a gold bull run. Where a leveraged developer might
triple in a 50% gold price move, a royalty company typically moves 40-60%.</p>

<p>That's not a bug; it's the value proposition. Royalty companies are the defensive anchor in a
precious-metals portfolio. They deliver positive operating leverage to the gold price without
the operational tail risks that periodically turn producer-only portfolios upside down.</p>

<h2>How to think about the royalty peer set</h2>
<p>Four names dominate the gold-focused royalty and streaming universe: Franco-Nevada, Wheaton
Precious Metals, Osisko Gold Royalties, and (to a lesser extent) Triple Flag Precious Metals and
Sandstorm Gold. Each has a different portfolio mix, diversification profile, and jurisdictional
tilt. Franco-Nevada is the most diversified by commodity (gold, copper, precious, oil and gas);
Wheaton is more concentrated in silver streams; Osisko Royalties is heaviest in Canadian assets,
particularly Quebec; Triple Flag and Sandstorm sit at smaller scale but with higher organic
growth optionality.</p>

<p>Only Franco-Nevada has been scored on our framework as of April 2026. Wheaton and Osisko
Royalties are queued for next research cycle. Full scorecards will be published as they're
completed.</p>

<h2>When a royalty allocation makes sense</h2>
<p>A simple framework: if your junior mining exposure is structurally volatile and concentrated
(3-5 positions, explorer and developer stage), a 15-25% allocation to a royalty name smooths
returns meaningfully without sacrificing gold-price participation. If your exposure is broader
(10+ positions with a producer base), the marginal diversification benefit of adding a royalty
name drops. Royalty allocation is most valuable for the concentrated, higher-variance
portfolio.</p>
""",
        "faq_items": [
            {"question": "What's the difference between a royalty and a stream?",
             "answer": "A royalty company receives a percentage of revenue or net profits from a mine. A streaming company pays for the right to purchase a percentage of the mine's metal at a pre-agreed (usually deeply-discounted) price. Both avoid operational capex and labor risk; the difference is in how the contract is structured."},
            {"question": "Why does Franco-Nevada trade at a P/NAV premium?",
             "answer": "Because operational risk and capex risk are absent. A streaming or royalty company's NAV is derived from its expected share of mine production, not from operating a mine itself. That cleaner risk profile earns a valuation premium."},
            {"question": "Can a royalty company lose money?",
             "answer": "Yes. Royalty and streaming companies that over-pay for streams during bull markets can end up locked into contracts whose IRR falls below cost of capital if the underlying commodity price declines or production misses. Discipline on capital deployment is the primary factor separating great royalty companies from mediocre ones."},
            {"question": "Should I own a royalty company or a junior gold explorer?",
             "answer": "They're not substitutes. A royalty company is the defensive anchor — lower volatility, positive gold-price leverage, capital-preservation-first. A junior explorer is the speculative bet — higher variance, dilution risk, binary outcomes. Most precious-metals portfolios have room for both."},
        ],
    },
    # ──────────────── #11 — Quebec ────────────────
    {
        "title": "Best Quebec Gold Mining Stocks 2026: Abitibi to James Bay Ranked",
        "meta_title": "Best Quebec Gold Mining Stocks 2026 Ranked",
        "meta_description": (
            "Six Quebec gold juniors on our Verdict Framework coverage ranked for 2026. "
            "Amex, Probe, Fury, Azimut, Cartier, Kenorland."
        ),
        "pillar_slug": "company-verdicts",
        "excerpt": (
            "Quebec is Canada's most active gold jurisdiction — and our most densely covered. "
            "Six Quebec-operating gold juniors on our Verdict Framework coverage list, ranked by "
            "composite score."
        ),
        "answer_capsule": (
            "Six Quebec gold equities on our April 2026 coverage list, ranked: Amex Exploration "
            "(21/25, BUY), Probe Gold (19/25, WATCH), Fury Gold Mines (20/25, BUY — portfolio "
            "spans Quebec and Newfoundland), Azimut Exploration (17/25, WATCH), Cartier Resources "
            "(17/25, WATCH), and Kenorland Minerals (16/25, WATCH). Wesdome Gold Mines (TSX:WDO) is "
            "a Quebec producer queued for coverage."
        ),
        "key_takeaways": [
            "Quebec is the densest gold jurisdiction in our coverage — six scored names",
            "Abitibi Greenstone Belt drives most of the geological value",
            "Two Quebec names hold BUY verdicts: Amex Exploration and Fury Gold Mines",
            "Quebec's flow-through financing structure keeps junior cap tables functional",
            "Wesdome Gold Mines is a Quebec mid-tier producer not yet scored by our framework",
        ],
        "ranked_items": [
            {"rank": 1, "name": "Amex Exploration Inc.", "ticker": "TSXV:AMX", "company_slug": "amex-exploration-inc",
             "summary": "21/25 BUY. Perron project (Abitibi). Geology 5/5, catalyst 5/5. The highest-scoring pure Quebec name in our coverage."},
            {"rank": 2, "name": "Fury Gold Mines Limited", "ticker": "TSX:FURY", "company_slug": "fury-gold-mines-limited",
             "summary": "20/25 BUY. Portfolio spans Quebec and Newfoundland. Balanced 4-across the framework. P/NAV of 0.55x."},
            {"rank": 3, "name": "Probe Gold Inc.", "ticker": "TSX:PRB", "company_slug": "probe-gold-inc",
             "summary": "19/25 WATCH. Novador complex (Val-d'Or district). Management 4/5 and capital 4/5 — a quality setup held back by a geology score of 3/5."},
            {"rank": 4, "name": "Azimut Exploration Inc.", "ticker": "TSXV:AZM", "company_slug": "azimut-exploration-inc",
             "summary": "17/25 WATCH. Multi-project prospect generator across Quebec. Partner-funded exploration model that conserves capital."},
            {"rank": 5, "name": "Cartier Resources Inc.", "ticker": "TSXV:ECR", "company_slug": "cartier-resources-inc",
             "summary": "17/25 WATCH. Chimo Mine (Abitibi). Historic high-grade mine with modern drill targets. P/NAV of 0.56x."},
            {"rank": 6, "name": "Kenorland Minerals Ltd.", "ticker": "TSXV:KLD", "company_slug": "kenorland-minerals-ltd",
             "summary": "16/25 WATCH. Multi-project exploration across Quebec and elsewhere. Management 4/5 and capital 4/5 — geology 2/5 is the holdback on a 5-to-10x optionality thesis."},
            {"rank": 7, "name": "Wesdome Gold Mines Ltd.", "ticker": "TSX:WDO", "company_slug": "wesdome-gold-mines-ltd",
             "summary": "Not yet scored on the framework. Quebec-Ontario mid-tier producer. Eagle River and Kiena mines in production. Queued for next research cycle."},
        ],
        "body": """
<h2>Why Quebec dominates junior gold in Canada</h2>
<p>Quebec combines three structural advantages that no other Canadian jurisdiction matches
simultaneously. First, the geology: the Abitibi Greenstone Belt hosts some of the richest gold
mineralisation in the world, and the James Bay region to the north is adding an active
discovery layer. Second, the permitting and taxation framework: Quebec's Plan Nord and flow-
through financing structures keep junior cap tables functional through multi-year exploration
cycles. Third, the operating environment: experienced workforce, mature mill infrastructure,
and road, rail, and hydroelectric access that dramatically lower the unit cost of any project
built in the province.</p>

<p>Those structural factors translate into our coverage density. Six of our 39 actively scored
companies operate primarily in Quebec — the single highest concentration by jurisdiction — and
most of the mid-tier Canadian gold producers (Agnico Eagle, Eldorado, Alamos, Wesdome) run
flagship operations there.</p>

<h2>What the Quebec list tells you</h2>
<p>The Abitibi is concentrated in the top of our Quebec list. Amex at 21/25 on Perron sits within
driving distance of several producing mills, which is part of why its acquisition-value score
(4/5) is so strong. Cartier's Chimo Mine is in the same district. Probe Gold's Novador complex
is in the Val-d'Or area. The geological quality — grade, continuity, metallurgy — tends to be
high across Abitibi names, and the in-region comparable-transactions set is deep enough to
support robust acquisition-value scoring.</p>

<p>Outside Abitibi, the coverage thins. Azimut's prospect generator model operates across multiple
Quebec regions including James Bay. Kenorland has projects in Quebec and Ontario. Fury Gold's
Eau Claire project sits in Quebec but its flagship Committee Bay is in Nunavut. The pattern is
clear: the further from Abitibi, the harder it is to reproduce the combination of grade and
infrastructure that drives top scores.</p>

<h2>The biggest coverage gap</h2>
<p>Wesdome Gold Mines (TSX:WDO) is the most important name not currently on our active coverage
list. Wesdome operates the Eagle River mine in Ontario and the Kiena mine in Quebec — producing
mid-tier ounces with strong all-in sustaining cost economics. It is the closest thing to a pure-
play Canadian gold producer in the mid-tier and deserves a scorecard. Coverage is queued.</p>

<h2>Flow-through financing: the Quebec advantage</h2>
<p>Quebec's flow-through share program allows companies to issue shares whose proceeds must be
spent on Canadian exploration expenses, with the tax deductions flowing through to the
shareholder. Combined with the Quebec tax credit layer, flow-through financing can effectively
subsidize up to 40% of exploration spending for the end investor. That translates into cleaner
junior cap tables: companies issue fewer pure-equity shares per dollar raised because the
flow-through structure delivers more exploration spend per share issued.</p>

<p>This is why Quebec juniors tend to score higher on the capital-structure factor than equivalent-
stage juniors in other Canadian jurisdictions. The financing infrastructure is part of the edge.</p>
""",
        "faq_items": [
            {"question": "Why are there so many Quebec gold juniors on your coverage list?",
             "answer": "Quebec combines world-class geology (Abitibi and James Bay), mature mining infrastructure, and Canada's most supportive flow-through financing framework. That combination produces more scorable junior gold equities per dollar of capital deployed than any other Canadian jurisdiction."},
            {"question": "What's the Abitibi Greenstone Belt?",
             "answer": "A 400-kilometer-long Archean-age volcanic and sedimentary rock formation straddling the Quebec-Ontario border. It hosts over 100 gold deposits discovered to date and has produced more than 160 million ounces of gold since mining began in the 1900s. Still actively producing and discovering."},
            {"question": "Is Wesdome Gold Mines on your watchlist?",
             "answer": "Wesdome is not yet on our active coverage list — the scorecard is queued for next research cycle. It is the closest thing to a pure-play Canadian gold mid-tier producer and will be scored shortly."},
            {"question": "What's flow-through financing and why does it matter?",
             "answer": "A Canadian tax structure that lets junior mining companies issue shares whose proceeds must be spent on exploration, with the tax deductions flowing to the shareholder. Combined with Quebec's provincial tax credits, flow-through effectively subsidises exploration spending — keeping junior cap tables cleaner than equivalent-stage juniors in other jurisdictions."},
        ],
    },
    # ──────────────── #12 — Nevada ────────────────
    {
        "title": "Best Nevada Gold Mining Stocks 2026: Walker Lane and Carlin Trend Ranked",
        "meta_title": "Best Nevada Gold Mining Stocks 2026",
        "meta_description": (
            "Five Nevada gold juniors on our Verdict Framework coverage for 2026. "
            "Borealis, i-80 Gold, Minera Alamos, Nevada King."
        ),
        "pillar_slug": "company-verdicts",
        "excerpt": (
            "Nevada remains the United States' most important gold jurisdiction. Four Nevada-"
            "operating gold juniors on our active coverage list in April 2026, plus one mid-tier "
            "producer queued for scoring."
        ),
        "answer_capsule": (
            "Four Nevada gold juniors on our April 2026 coverage list: Borealis Mining (17/25, "
            "WATCH), Minera Alamos (17/25, WATCH), i-80 Gold (15/25, WATCH), and Nevada King Gold "
            "(12/25, AVOID). McEwen Mining is a Nevada mid-tier producer queued for next research "
            "cycle coverage."
        ),
        "key_takeaways": [
            "Nevada consistently produces more gold than any US state and one of the most globally",
            "The Carlin Trend and Walker Lane are the two dominant exploration belts",
            "None of our Nevada names currently holds a BUY verdict — the highest is 17/25",
            "Permitting timelines in Nevada are shorter than most Canadian jurisdictions",
            "Borealis trades at 0.44x P/NAV — the deepest discount in our universe",
        ],
        "ranked_items": [
            {"rank": 1, "name": "Borealis Mining Company Limited", "ticker": "TSXV:BOGO", "company_slug": "borealis-mining-company-limited",
             "summary": "17/25 WATCH. Nevada gold project. Management 4/5 and catalyst 4/5 combine with a P/NAV of 0.44x — deepest discount in our universe."},
            {"rank": 2, "name": "Minera Alamos Inc.", "ticker": "TSXV:MAI", "company_slug": "minera-alamos-inc",
             "summary": "17/25 WATCH. Management 4/5 and capital 4/5. Nevada and Mexico portfolio; a rare TSX-V developer-producer with clean cap table."},
            {"rank": 3, "name": "i-80 Gold Corp.", "ticker": "TSX:IAU", "company_slug": "i-80-gold-corp",
             "summary": "15/25 WATCH. Multi-project Nevada developer. Catalyst 4/5 reflects active milestones; capital 2/5 is the drag on the composite."},
            {"rank": 4, "name": "Nevada King Gold Corp.", "ticker": "TSXV:NKG", "company_slug": "nevada-king-gold-corp",
             "summary": "12/25 AVOID. Management 4/5. Geology 2/5 and acquisition value 1/5 are the drags. An AVOID based on the framework's factor math, not on management quality."},
            {"rank": 5, "name": "McEwen Mining Inc.", "ticker": "TSX:MUX", "company_slug": "mcewen-mining-inc",
             "summary": "Not yet scored on the framework. Nevada, Mexico, Argentina, Canada operations. Gold Bar (Nevada) and Fox Complex (Ontario). Queued for coverage."},
        ],
        "body": """
<h2>Why Nevada matters for gold investors</h2>
<p>Nevada produces roughly 70% of US gold output and is among the top five gold-producing
jurisdictions globally. Two exploration belts dominate: the Carlin Trend in north-central Nevada,
home to some of the world's largest sediment-hosted gold deposits, and the Walker Lane stretching
from western Nevada into eastern California, hosting epithermal-style gold-silver mineralisation.
Both belts have active producers, active development, and an ongoing exploration layer.</p>

<p>For junior gold investors, Nevada offers three practical advantages over other US
jurisdictions. First, permitting timelines are shorter — the state's Division of Environmental
Protection and the federal Bureau of Land Management can move faster than permitting bodies in
Colorado, Idaho, or Alaska. Second, infrastructure is mature: roads, power, water rights, and
experienced workforce are widely available. Third, the comparable-transactions set is deep,
which supports robust acquisition-value scoring for in-state juniors.</p>

<h2>Why no Nevada BUY verdict</h2>
<p>The highest-scoring Nevada names on our list sit at 17/25 (WATCH). That's not because Nevada
juniors are structurally worse than Quebec juniors — they aren't. It's because the specific
names we've scored currently have factor mixes that plateau at 17. Borealis has strong management
and catalyst scores but its acquisition-value sits at 3/5 and capital at 3/5. Minera Alamos has
a clean capital structure but catalyst sits at 3/5. Small factor shifts on any of these names
could push them to 18 or 19.</p>

<p>We expect Nevada coverage to expand in 2026. McEwen Mining is queued; a handful of other Nevada
developers are in the research queue. The goal is a five-to-seven-name Nevada universe that
supports deeper jurisdictional analysis than the current four-company set.</p>

<h2>The Nevada King AVOID</h2>
<p>Nevada King is instructive for investors trying to understand how the framework issues an
AVOID verdict. Management scored 4/5 — insider alignment is in place, and the team has relevant
Nevada experience. But geology scored 2/5 at the time of the last scorecard, and acquisition
value scored 1/5. The composite (12/25) lands in AVOID territory not because any one factor is
catastrophically broken, but because the asset-side factors aren't keeping up with the team's
alignment. The Atlanta project continues drilling; a meaningful resource disclosure could move
the score.</p>

<h2>Jurisdictional trade-off with Canada</h2>
<p>Nevada vs Quebec is the most common jurisdictional choice for USA-Canada gold investors. The
trade-offs:</p>
<ul>
  <li><strong>Permitting speed</strong> — Nevada faster, typically by 12-24 months to mine start-up.</li>
  <li><strong>Geology</strong> — Comparable; both host world-class systems.</li>
  <li><strong>Financing</strong> — Quebec's flow-through structure gives Canadian-listed juniors an edge.</li>
  <li><strong>Infrastructure cost</strong> — Nevada slightly cheaper; Quebec has hydroelectric power advantage.</li>
  <li><strong>Labor</strong> — Both experienced; Nevada has higher turnover historically.</li>
</ul>
""",
        "faq_items": [
            {"question": "Why is Nevada such a prolific gold jurisdiction?",
             "answer": "Two major exploration belts host billions of ounces of gold mineralisation: the Carlin Trend (sediment-hosted gold deposits) and the Walker Lane (epithermal gold-silver). Combined with mature mining infrastructure and relatively fast permitting, Nevada has produced more US gold than any other state for decades."},
            {"question": "Is Nevada's permitting really faster than Canada's?",
             "answer": "Generally yes, typically by 12-24 months to mine start-up. State and federal permitting processes are mature and well-understood. That said, federal land withdrawals and environmental challenges can still add multi-year delays on specific projects."},
            {"question": "Why doesn't any Nevada name hold a BUY verdict?",
             "answer": "The highest-scoring Nevada juniors in our April 2026 coverage sit at 17/25 — one factor point below the BUY threshold of 18. The gap is typically on catalyst or acquisition-value scores, either of which could move up in subsequent quarterly scoring."},
            {"question": "What's the difference between the Carlin Trend and the Walker Lane?",
             "answer": "Geologically different systems. The Carlin Trend hosts sediment-hosted (Carlin-type) gold deposits — generally finer-grained, lower-grade, but very large tonnage. The Walker Lane hosts epithermal gold-silver vein systems — higher grade, narrower mineralisation, more selective mining. Different capex profiles and different operator skills required."},
        ],
    },
    # ──────────────── #13 — Yukon ────────────────
    {
        "title": "Best Yukon Mining Stocks 2026: Gold and Copper in Canada's North",
        "meta_title": "Best Yukon Mining Stocks 2026: Gold and Copper",
        "meta_description": (
            "Three Yukon mining equities on our Verdict Framework plus Victoria Gold queued. "
            "Banyan, Snowline, Western Copper ranked for 2026."
        ),
        "pillar_slug": "company-verdicts",
        "excerpt": (
            "The Yukon has become Canada's most interesting frontier jurisdiction — home to the "
            "Snowline/Valley discovery, the Banyan AurMac deposit, and Western Copper's Casino "
            "project. Three scored names plus one queued for coverage."
        ),
        "answer_capsule": (
            "Three Yukon mining equities on our April 2026 coverage list: Snowline Gold (19/25, "
            "WATCH), Western Copper and Gold (19/25, WATCH — copper-gold-moly), and Banyan Gold "
            "(18/25, WATCH). Victoria Gold (TSX:VGCX) is queued for research cycle coverage. "
            "The Yukon is Canada's most active exploration jurisdiction by dollars per square kilometre."
        ),
        "key_takeaways": [
            "Three Yukon names on coverage with composite scores of 18/25 or higher — unusually dense",
            "Snowline Gold's Valley discovery is one of Canada's most significant recent gold discoveries",
            "Western Copper's Casino project is the largest undeveloped copper-gold asset in the Yukon",
            "Banyan Gold's AurMac project is a heap-leach-amenable bulk-tonnage target",
            "Victoria Gold's Eagle mine suspension is a cautionary tale on operating risk",
        ],
        "ranked_items": [
            {"rank": 1, "name": "Snowline Gold Corp.", "ticker": "TSX:SGD", "company_slug": "snowline-gold-corp",
             "summary": "19/25 WATCH. Valley project, Tintina Gold Belt. Management 4/5, catalyst 4/5. The post-discovery delineation drilling has been the Canadian junior gold story of 2024-2026."},
            {"rank": 2, "name": "Western Copper and Gold Corporation", "ticker": "TSX:WRN", "company_slug": "western-copper-and-gold-corporation",
             "summary": "19/25 WATCH. Casino project. Geology 5/5 — one of North America's largest undeveloped copper-gold-moly deposits. Permitting is the rate limiter."},
            {"rank": 3, "name": "Banyan Gold Corp.", "ticker": "TSXV:BYN", "company_slug": "banyan-gold-corp",
             "summary": "18/25 WATCH. AurMac project. Bulk-tonnage heap-leach-amenable target with capital 4/5 and catalyst 4/5. Resource growth is the primary thesis."},
            {"rank": 4, "name": "Victoria Gold Corp.", "ticker": "TSX:VGCX", "company_slug": "victoria-gold-corp",
             "summary": "Not yet scored. Operated the Eagle mine until a heap-leach failure in June 2024. Restart and environmental remediation ongoing. Queued for coverage once the operational picture clarifies."},
        ],
        "body": """
<h2>Why the Yukon has become Canada's most active exploration jurisdiction</h2>
<p>The Yukon combines three factors that together have pulled an outsized share of junior mining
capital over the last five years. First, world-class geology across multiple belts — the Tintina
Gold Belt (Snowline, Banyan, Western Copper all in or adjacent to it), the Selwyn Basin, and
the Klondike placer-and-lode trend. Second, relative infrastructure maturity compared to Nunavut
or the Northwest Territories, with road access to most significant projects and the Whitehorse
service base. Third, a regulatory environment that is defined but still workable, without the
layered provincial-federal complexity that can slow projects in other Canadian jurisdictions.</p>

<p>The practical result: when you see major Canadian juniors announce exploration budgets, an
outsized share is deployed in the Yukon relative to the province's share of Canadian land area.
Our coverage density reflects this — three of 39 covered companies operate primarily in the
Yukon, a higher rate than British Columbia despite BC's deeper historical mining base.</p>

<h2>The Snowline story</h2>
<p>Snowline Gold's Valley discovery deserves specific attention because it is the Canadian junior
gold story of the last two years. The Valley deposit is a reduced intrusion-related gold system
(RIRGS) — a relatively rare geological type that can host large-scale, heap-leach-amenable bulk
tonnage mineralisation at economically compelling grades. Subsequent delineation drilling has
expanded the system materially. The composite score of 19/25 reflects a balanced 4-across the
factor mix — not one standout but no weaknesses either. The P/NAV of 0.89x says the market has
largely priced the re-rating from exploration upside already.</p>

<h2>The Casino project</h2>
<p>Western Copper and Gold's Casino project is the polar opposite of Snowline in project profile.
Casino is a large-scale copper-gold-moly porphyry — billions of pounds of copper, supported by
gold and moly credits — where the economics work even at mid-cycle copper prices. The geology
score of 5/5 reflects asset quality; the catalyst score of 3/5 reflects a permitting timeline
measured in years rather than quarters. Casino is a patience asset, not a drill-result story.</p>

<h2>The Victoria Gold lesson</h2>
<p>Victoria Gold operated the Eagle mine in the Yukon until a heap-leach failure in June 2024
resulted in mine suspension, an environmental containment response, and a change in control.
The event is the single most important reminder in recent Canadian gold mining that operating
risk is real even in well-understood jurisdictions. Victoria is queued for scoring on our
framework, but the operational picture needs to clarify before a scorecard is published. We do
not score companies in active crisis-response mode because the factor math is unreliable.</p>

<h2>What's not on the list</h2>
<p>Several smaller Yukon-focused juniors — Sitka Gold, White Gold, Rackla Metals, Fury Gold's
Committee Bay project (technically Nunavut, not Yukon) — sit outside our active coverage. Sitka
is already on our Company records with needs-research flagged. Others will be added as research
capacity allows. The Yukon universe is broader than the three scored names above.</p>
""",
        "faq_items": [
            {"question": "Why is the Yukon so active for junior mining exploration?",
             "answer": "World-class geology across multiple belts (Tintina, Selwyn, Klondike), relative infrastructure maturity with road access to most significant projects, and a regulatory environment that is workable without the layered provincial-federal complexity of southern Canadian jurisdictions."},
            {"question": "What is a reduced intrusion-related gold system (RIRGS)?",
             "answer": "A relatively rare geological setting where gold mineralisation is associated with reduced (low-oxidation) intrusive rocks. RIRGS deposits can host large-scale, bulk-tonnage, heap-leach-amenable mineralisation at economically compelling grades. Snowline's Valley discovery is one of the most significant recent Canadian RIRGS systems."},
            {"question": "When will Victoria Gold be scored on the framework?",
             "answer": "When the operational picture post-Eagle-mine-suspension clarifies enough to produce reliable factor scoring. We do not score companies in active crisis-response mode because the underlying disclosures and comparable transactions are unstable."},
            {"question": "Is the Yukon a better junior mining jurisdiction than British Columbia?",
             "answer": "Different trade-offs. Yukon exploration capital has outpaced BC per square kilometre in recent years, driven by less regulatory layering and high-impact discoveries. BC has more mature infrastructure and a deeper mill base for producers. The right answer depends on project stage — Yukon favours exploration, BC favours development-to-production transitions."},
        ],
    },
    # ──────────────── #14 — British Columbia ────────────────
    {
        "title": "Best British Columbia Mining Stocks 2026: Golden Triangle to Vancouver Island",
        "meta_title": "Best British Columbia Mining Stocks 2026 Ranked",
        "meta_description": (
            "Five BC mining equities in our coverage, from Osisko Development's Cariboo Gold "
            "to NorthIsle on Vancouver Island. 2026 rankings."
        ),
        "pillar_slug": "company-verdicts",
        "excerpt": (
            "British Columbia is Canada's second-most-active gold jurisdiction and home to the "
            "Golden Triangle, one of North America's highest-grade gold regions. Five scored BC "
            "mining equities plus several queued for coverage."
        ),
        "answer_capsule": (
            "Five British Columbia mining equities on our April 2026 coverage list: Osisko "
            "Development (18/25, WATCH), Canagold Resources (17/25, WATCH), NorthIsle Copper and "
            "Gold (15/25, WATCH — Vancouver Island), Enduro Metals (9/25, AVOID), and Collective "
            "Mining — which is headquartered in Canada but operates in Colombia. Artemis Gold, "
            "Skeena Resources, and Scottie Resources are queued for coverage."
        ),
        "key_takeaways": [
            "The Golden Triangle hosts some of North America's highest-grade gold mineralisation",
            "Osisko Development's Cariboo Gold project is the highest-scoring BC name on coverage",
            "Vancouver Island adds copper-gold exposure via NorthIsle's North Island project",
            "BC permitting is slower than Nevada but faster than the Northwest Territories",
            "Artemis Gold's Blackwater project is the most significant BC developer not yet scored",
        ],
        "ranked_items": [
            {"rank": 1, "name": "Osisko Development Corp.", "ticker": "TSXV:ODV", "company_slug": "osisko-development-corp",
             "summary": "18/25 WATCH. Cariboo Gold project. Management 4/5 with Osisko-group pedigree. P/NAV of 2.15x — market has already priced in development progression."},
            {"rank": 2, "name": "Canagold Resources Ltd.", "ticker": "TSX:CCM", "company_slug": "canagold-resources-ltd",
             "summary": "17/25 WATCH. BC gold project. Geology 5/5 — standout asset quality. Capital 2/5 is the drag; P/NAV of 0.59x reflects the discount."},
            {"rank": 3, "name": "NorthIsle Copper and Gold Inc.", "ticker": "TSXV:NCX", "company_slug": "northisle-copper-and-gold-inc",
             "summary": "15/25 WATCH. North Island project (Vancouver Island). Copper-gold porphyry. Capital 4/5 is the factor strength; P/NAV 1.17x."},
            {"rank": 4, "name": "Enduro Metals Corporation", "ticker": "TSXV:ENDR", "company_slug": "enduro-metals-corporation",
             "summary": "9/25 AVOID. Northwestern BC. Geology 1/5 is the primary drag. Framework sees no clear path to re-rating without a project pivot or new discovery."},
            {"rank": 5, "name": "Artemis Gold Inc.", "ticker": "TSXV:ARTG", "company_slug": "artemis-gold-inc",
             "summary": "Not yet scored. Blackwater project (BC interior) — one of the largest gold developments in construction in Canada. Queued for next research cycle."},
            {"rank": 6, "name": "Skeena Resources Limited", "ticker": "TSX:SKE", "company_slug": "skeena-resources-limited",
             "summary": "Not yet scored. Eskay Creek Gold-Silver Project (BC Golden Triangle). Historic high-grade asset in restart. Queued for coverage."},
            {"rank": 7, "name": "Scottie Resources Corp.", "ticker": "TSXV:SCOT", "company_slug": "scottie-resources-corp",
             "summary": "Not yet scored. Golden Triangle explorer. High-grade targets in an active exploration region. Queued for coverage."},
        ],
        "body": """
<h2>BC's three distinct mining regions</h2>
<p>British Columbia is too large and too geologically diverse to treat as a single jurisdiction.
Three regions dominate the mining equity landscape. The Golden Triangle in the northwest hosts
some of North America's highest-grade gold-silver mineralisation — Eskay Creek (Skeena), Brucejack
(Newcrest/Newmont), Red Chris, and active explorers in between. The BC interior hosts larger-
scale disseminated gold systems — Artemis Gold's Blackwater, Osisko Development's Cariboo Gold,
and the historic Mount Polley operation. Vancouver Island and the coastal region host copper-
gold porphyry systems — NorthIsle's North Island, historic Island Copper, and related targets.</p>

<p>Each region has different cost profiles, different typical deposit types, and different
permitting realities. Grouping them into a single "BC mining" category obscures more than it
reveals.</p>

<h2>The Golden Triangle's structural advantage</h2>
<p>The Golden Triangle runs roughly 500 kilometres along the BC-Alaska border between Stewart and
Atlin. The region hosts world-class deposits including Eskay Creek, one of the highest-grade gold
deposits ever mined commercially, and Brucejack, another high-grade underground operation that
operated at the top decile of the global grade curve. Two structural factors support the area:
exceptional grade (meaning high-margin economics even at modest gold prices) and the Northwest
Transmission Line, which delivered grid power to previously-stranded deposits.</p>

<p>Our coverage of the Golden Triangle is currently light — Skeena (queued) and Scottie (queued)
are the two active names, and neither has a published scorecard yet. Expanding Golden Triangle
coverage is a 2026 research priority.</p>

<h2>The Cariboo region and Osisko Development</h2>
<p>The Cariboo region in central BC has a mining history stretching back to the 1860s placer gold
rush. Osisko Development's Cariboo Gold project aggregates multiple historic underground mines
with modern exploration overlays, targeting a 200,000+ ounce-per-year operation. The composite
score of 18/25 reflects management pedigree (4/5) and steady development progression, offset by
a P/NAV of 2.15x — the market has already priced in the permitting and construction path.</p>

<h2>NorthIsle and the Vancouver Island copper story</h2>
<p>NorthIsle Copper and Gold's North Island project sits on historic Island Copper ground — the
former BHP operation that produced for three decades. The porphyry system extends beyond the
historic pit, and NorthIsle has been delineating both extensions and satellite zones. The 15/25
score is held back by a geology score of 3/5 (respectable, not standout) and catalyst of 3/5
(long-cycle resource work rather than imminent milestones). For investors specifically seeking
BC-jurisdiction copper exposure, it is the primary scored name.</p>

<h2>The biggest gaps in our BC coverage</h2>
<p>Artemis Gold's Blackwater project is the most significant BC gold development not yet on our
framework. Blackwater is in construction, with first production expected in 2025-2026 depending
on ramp. It will be one of the largest new Canadian gold producers and deserves a scorecard.
Skeena's Eskay Creek restart is the second priority. Both are queued and will be scored in
upcoming research cycles.</p>
""",
        "faq_items": [
            {"question": "What is the Golden Triangle?",
             "answer": "A 500-km mineralised belt running along the BC-Alaska border, hosting some of North America's highest-grade gold-silver deposits including Eskay Creek, Brucejack, and Red Chris. Characterised by exceptional grade (high-margin economics) and relatively recent grid-power access via the Northwest Transmission Line."},
            {"question": "Why is Artemis Gold not on your coverage list yet?",
             "answer": "Artemis is queued for the next research cycle. The Blackwater project is one of the largest new Canadian gold developments in construction and deserves a scorecard — coverage has simply not caught up with the company's stage yet. It will be added in upcoming research."},
            {"question": "Is BC permitting slower than Nevada or Quebec?",
             "answer": "Generally yes for large-scale projects, though faster than federal permitting in the Yukon or Northwest Territories. BC's Environmental Assessment process and First Nations consultation add time that mature Nevada or Quebec projects often avoid. That said, timeline is predictable — 3-5 years for a typical mid-scale project is common."},
            {"question": "Why the focus on Osisko Development?",
             "answer": "It's the highest-scoring pure-BC name currently on our active coverage. Management pedigree from the Osisko group, Cariboo Gold project in active development, and factor balance across the five scoring inputs. Not a BUY, but a structurally-sound WATCH."},
        ],
    },
    # ──────────────── #15 — High-Grade Geology ────────────────
    {
        "title": "High-Grade Gold Mining Stocks: Top Geology Scores on the Verdict Framework",
        "meta_title": "High-Grade Gold Mining Stocks 2026: Top Geology",
        "meta_description": (
            "Ten gold and precious-metal equities scoring 4/5 or 5/5 on geology in our Verdict "
            "Framework. Grade, category, metallurgy ranked."
        ),
        "pillar_slug": "investing-guides",
        "excerpt": (
            "The geology factor scores the rocks — grade, resource category, continuity, and "
            "metallurgy. Ten companies scoring 4/5 or 5/5 in April 2026, led by five perfect 5/5 "
            "scores."
        ),
        "answer_capsule": (
            "Ten gold and precious-metal equities score 4/5 or 5/5 on geology in April 2026. Five "
            "hold a perfect 5/5: Amex Exploration, Canagold Resources, Equinox Gold, GoGold Resources, "
            "and Western Copper and Gold. Fury Gold Mines, Heliostar Metals, Integra Resources, "
            "Liberty Gold, and Snowline Gold round out the 4/5 tier."
        ),
        "key_takeaways": [
            "Geology is the factor most directly tied to a project's fundamental value",
            "Five 5/5 geology scores — the highest-conviction asset-quality signal we issue",
            "High grade is the most important driver, but tonnage, metallurgy, and continuity all factor in",
            "High geology score does not guarantee a high composite — asset quality with weak team is common",
            "The geology factor is the slowest to change — it reflects the rocks in the ground",
        ],
        "ranked_items": [
            {"rank": 1, "name": "Amex Exploration Inc.", "ticker": "TSXV:AMX", "company_slug": "amex-exploration-inc",
             "summary": "Geology 5/5. Perron project high-grade gold system in the Abitibi. Grade and continuity both top-tier; resource is growing."},
            {"rank": 2, "name": "Canagold Resources Ltd.", "ticker": "TSX:CCM", "company_slug": "canagold-resources-ltd",
             "summary": "Geology 5/5. New Polaris (BC) high-grade underground historic mine. Asset quality is the standout; weaker capital structure is what holds the composite back."},
            {"rank": 3, "name": "Equinox Gold Corp.", "ticker": "TSX:EQX", "company_slug": "equinox-gold-corp",
             "summary": "Geology 5/5. Multi-mine producer portfolio across the Americas; geology score reflects aggregate reserves and mine-life visibility."},
            {"rank": 4, "name": "GoGold Resources Inc.", "ticker": "TSX:GGD", "company_slug": "gogold-resources-inc",
             "summary": "Geology 5/5. Los Ricos silver-gold (Mexico). Strong grade, strong continuity, supportive metallurgy. The best silver asset on our coverage."},
            {"rank": 5, "name": "Western Copper and Gold Corporation", "ticker": "TSX:WRN", "company_slug": "western-copper-and-gold-corporation",
             "summary": "Geology 5/5. Casino copper-gold-moly (Yukon). Scale is the story — billions of pounds of copper plus gold and moly credits."},
            {"rank": 6, "name": "Fury Gold Mines Limited", "ticker": "TSX:FURY", "company_slug": "fury-gold-mines-limited",
             "summary": "Geology 4/5. Quebec-Newfoundland portfolio with optionality across multiple projects. No single flagship but diversified quality."},
            {"rank": 7, "name": "Heliostar Metals Ltd.", "ticker": "TSXV:HSTR", "company_slug": "heliostar-metals-ltd",
             "summary": "Geology 4/5. Mexican producing mines plus Ana Paula development. Production track record validates the resource base."},
            {"rank": 8, "name": "Integra Resources Corp.", "ticker": "TSXV:ITR", "company_slug": "integra-resources-corp",
             "summary": "Geology 4/5. DeLamar heap-leach-amenable gold (Idaho). Scale plus metallurgy combine for strong score."},
            {"rank": 9, "name": "Liberty Gold Corp.", "ticker": "TSX:LGD", "company_slug": "liberty-gold-corp",
             "summary": "Geology 4/5. Black Pine oxide gold (Idaho). Good continuity and heap-leach metallurgy."},
            {"rank": 10, "name": "Snowline Gold Corp.", "ticker": "TSX:SGD", "company_slug": "snowline-gold-corp",
             "summary": "Geology 4/5. Valley project (Yukon). RIRGS system with strong grade-tonnage combination and ongoing resource expansion."},
        ],
        "body": """
<h2>What the geology factor actually measures</h2>
<p>Four inputs drive the geology score. First, grade — measured in grams per tonne for gold and
silver, percent for base metals. Grade determines whether a deposit can be mined economically at
a given commodity price. Second, resource category — the progression from inferred (widely-spaced
drill data, lowest confidence) to indicated (tighter-spaced, moderate confidence) to measured
(tight-spaced, high confidence). Higher-category ounces earn higher scores because they carry less
geological uncertainty. Third, metallurgy — whether the deposit can be economically processed.
A high-grade deposit with complex metallurgy (gold locked in sulphide, or with significant
deleterious elements) scores worse than a lower-grade deposit with simple metallurgy. Fourth,
continuity — whether the mineralisation holds together in three dimensions or is erratic and
pocketed.</p>

<p>A 5/5 score requires all four to be strong. Amex (Perron), Canagold (New Polaris), and GoGold
(Los Ricos) score 5/5 because their grade, resource category, metallurgy, and continuity all
clear high bars. Western Copper scores 5/5 on a different axis — grade is modest but tonnage and
co-product credits combine to produce exceptional project-level economics.</p>

<h2>Why geology is the hardest factor to change</h2>
<p>The other four factors change over quarters or years. Geology changes over decades, and mostly
through new exploration. A company cannot improve its geology score by better management
decisions — the rocks are what the rocks are. What can happen is that a new discovery on the
same property adds to the resource, or that infill drilling moves ounces from inferred to
indicated, or that metallurgical testwork resolves a processing concern. Those are slow, capital-
intensive changes.</p>

<p>This is why the geology score is the most persistent signal in the framework. If a company
has scored 4/5 or 5/5 on geology, it is very likely to still score 4/5 or 5/5 a year later,
barring a negative resource revision (which does happen, especially on early-stage
resources with narrow drill spacing).</p>

<h2>High geology but weak overall — the pattern to watch</h2>
<p>Canagold is instructive. The New Polaris project scores 5/5 on geology — the asset is
high-quality. But the composite is only 17/25 (WATCH) because capital structure scores 2/5,
which weights the composite down. This is the classic "great project in a constrained package"
pattern. A disciplined financing can lift the capital score from 2/5 to 3/5 or 4/5, which would
push the composite well into BUY territory. Investors willing to bet on the capital-side repair
mechanism can size into names like this ahead of the re-rating event.</p>

<p>The inverse pattern — strong management and capital, weak geology — is harder to resolve
because geology is slow to change. Collective Mining (management 5/5, geology 2/5) is the
clearest example in our coverage.</p>

<h2>Grade alone is not the story</h2>
<p>Retail investors often fixate on grade ("ounces per tonne") as the headline measure of geological
quality. Grade matters, but it's one of four inputs. A 25 g/t gold deposit with complex metallurgy
and erratic continuity can mine worse than a 1.5 g/t deposit with simple metallurgy and bulk
continuity. Heap-leach-amenable oxide gold at 0.8 g/t — the Liberty Gold and Integra Resources
profile — scores well on metallurgy and continuity even if grade alone would suggest otherwise.
Read the 43-101 beyond the grade number.</p>
""",
        "faq_items": [
            {"question": "What does a 5/5 geology score mean?",
             "answer": "Strong grade, high-category resource (indicated-plus measured exceeding inferred), simple or well-understood metallurgy, and good continuity. All four inputs must clear high bars. Five companies hold 5/5 in our April 2026 coverage — Amex, Canagold, Equinox, GoGold, and Western Copper."},
            {"question": "Is grade the most important input to the geology score?",
             "answer": "It's one of four. Grade, resource category, metallurgy, and continuity all factor in. A high-grade deposit with poor metallurgy can score worse than a moderate-grade deposit with simple processing. Read the 43-101 beyond the headline grade number."},
            {"question": "Why does Canagold score 5/5 on geology but only 17/25 overall?",
             "answer": "Canagold's New Polaris is a high-quality asset (geology 5/5), but capital structure scores only 2/5, which pulls the composite down. This 'great project in a constrained package' pattern is common. Capital can typically be fixed through a disciplined financing; geology cannot be fixed easily."},
            {"question": "Can geology scores go down over time?",
             "answer": "Yes, though less often than they go up. Negative resource revisions — where a resource estimate is reduced due to new drilling, updated geology, or reclassification — can drop a geology score. These are most common on early-stage resources with narrow drill spacing. Producing mines rarely see negative geology revisions."},
        ],
    },
    # ──────────────── #16 — Mid-Tier / Major Producers ────────────────
    {
        "title": "Mid-Tier and Major Gold Producers: What the Framework Says About the Big Names",
        "meta_title": "Mid-Tier and Major Gold Producers 2026: Framework Coverage",
        "meta_description": (
            "Canadian gold producers — Agnico, Barrick, Newmont, Kinross and more. Framework "
            "read and the coverage roadmap for 2026."
        ),
        "pillar_slug": "company-verdicts",
        "excerpt": (
            "The major and mid-tier gold producers are the gold sector's defensive anchor. "
            "Framework coverage is thin here today — Franco-Nevada and Equinox Gold are the only "
            "actively scored names. Here's our coverage roadmap for the senior names."
        ),
        "answer_capsule": (
            "The major and mid-tier gold producer universe relevant to Canadian investors includes "
            "Agnico Eagle, Barrick Gold, Newmont, Kinross, Alamos Gold, B2Gold, Wesdome, Lundin "
            "Gold, Equinox Gold, and Franco-Nevada. Only Franco-Nevada (21/25, BUY) and Equinox "
            "(19/25, WATCH) are currently scored on our Verdict Framework. The remaining names are "
            "queued for research."
        ),
        "key_takeaways": [
            "Senior gold producers are the defensive anchor — lower volatility, dividend support",
            "Only two senior names are currently scored on the framework",
            "Framework scoring of producers uses the same 5-factor rubric as juniors",
            "Producer geology scores tend to be high (operating reserves) but cap structure varies",
            "Coverage expansion to senior names is a 2026 research priority",
        ],
        "ranked_items": [
            {"rank": 1, "name": "Franco-Nevada Corp.", "ticker": "TSX:FNV", "company_slug": "franco-nevada-corp",
             "summary": "21/25 BUY. Royalty and streaming major. The defensive anchor — no operational risk, no per-project capex. Trades at 1.12x P/NAV."},
            {"rank": 2, "name": "Equinox Gold Corp.", "ticker": "TSX:EQX", "company_slug": "equinox-gold-corp",
             "summary": "19/25 WATCH. Mid-tier producer across Americas. Geology 5/5; capital 4/5. P/NAV 0.64x reflects operational-complexity discount."},
            {"rank": 3, "name": "Agnico Eagle Mines Ltd.", "ticker": "TSX:AEM", "company_slug": "agnico-eagle-mines-ltd",
             "summary": "Not yet scored. Global senior gold producer with flagship Malartic (Quebec) and multi-jurisdiction operations. Best-in-class operator by reputation. Queued."},
            {"rank": 4, "name": "Barrick Gold Corp.", "ticker": "TSX:ABX", "company_slug": "barrick-gold-corp",
             "summary": "Not yet scored. The original Canadian gold senior; global operations. Rebranded to Barrick Mining Corp. in early 2026 reflecting copper diversification. Queued."},
            {"rank": 5, "name": "Newmont Corporation", "ticker": "TSX:NGT", "company_slug": "newmont-corporation",
             "summary": "Not yet scored. World's largest gold producer by output following the Newcrest acquisition. Global operations. Queued for coverage."},
            {"rank": 6, "name": "Kinross Gold Corp.", "ticker": "TSX:K", "company_slug": "kinross-gold-corp",
             "summary": "Not yet scored. Senior gold producer with US, Canada, Chile, Mauritania, and Brazil operations. Tasiast (Mauritania) is the flagship. Queued."},
            {"rank": 7, "name": "Alamos Gold Inc.", "ticker": "TSX:AGI", "company_slug": "alamos-gold-inc",
             "summary": "Not yet scored. Canadian-focused mid-tier producer. Young-Davidson (Ontario) and Mulatos/Island Gold are the flagships. Queued."},
            {"rank": 8, "name": "B2Gold Corp.", "ticker": "TSX:BTO", "company_slug": "b2gold-corp",
             "summary": "Not yet scored. Senior producer with Mali, Philippines, Namibia operations; Goose project in Canada in development. Queued."},
            {"rank": 9, "name": "Wesdome Gold Mines Ltd.", "ticker": "TSX:WDO", "company_slug": "wesdome-gold-mines-ltd",
             "summary": "Not yet scored. Quebec-Ontario pure-Canadian mid-tier producer. Eagle River and Kiena mines. Queued for next research cycle."},
            {"rank": 10, "name": "Lundin Gold Inc.", "ticker": "TSX:LUG", "company_slug": "lundin-gold-inc",
             "summary": "Not yet scored. Single-asset Fruta del Norte operation (Ecuador). Low-cost, high-margin producer. Queued for coverage."},
        ],
        "body": """
<h2>Why producer coverage is lighter than junior coverage</h2>
<p>The Verdict Framework was built to fill the rigorous-analysis gap in the junior mining
universe, where sell-side coverage is thin and promotional research is dense. The senior gold
producers — Agnico, Barrick, Newmont, Kinross, Alamos, B2Gold — are covered extensively by
institutional sell-side desks, with multiple banks publishing full models and weekly notes on
each. The marginal value of another voice covering Agnico Eagle is low.</p>

<p>That said, the same framework that scores a TSX-V explorer can score a global senior with
small adjustments. Producer geology scoring uses reserves and mine life instead of
exploration-stage resources. Capital scoring incorporates debt levels and cash-flow
sustainability rather than runway-to-next-milestone. Management scoring weighs capital
allocation track record more heavily than founder-CEO alignment. The rubric is the same; the
emphasis shifts.</p>

<h2>The two senior names we do score</h2>
<p>Franco-Nevada at 21/25 (BUY) is the royalty and streaming major. The 5/5 scores on management
and capital structure reflect the model itself — no operational risk, no per-project capex,
decades of disciplined deal-making. Investors who want gold-price exposure without operational
tail risk should own Franco-Nevada or a direct peer (Wheaton Precious Metals, Osisko Gold
Royalties, Triple Flag, Sandstorm).</p>

<p>Equinox Gold at 19/25 (WATCH) is the Americas-focused mid-tier producer. Geology scores 5/5 —
the reserves are real and the mine life visibility is good. Capital scores 4/5 post-integration
work. The composite sits below BUY because catalyst score (4/5) and acquisition value (3/5) don't
quite clear the thresholds for a full 5-across. Equinox is our closest thing to a representative
producer in active coverage.</p>

<h2>What the coverage roadmap looks like</h2>
<p>Senior producer coverage is a 2026 research priority. The queue in approximate order:
<strong>Agnico Eagle</strong> (Quebec flagship plus global operations, arguably best-in-class operator);
<strong>Wesdome</strong> (pure-Canadian mid-tier, under-covered by retail);
<strong>Barrick Gold</strong> (global major, rebranded to Barrick Mining in early 2026);
<strong>Alamos Gold</strong> (Canadian-focused mid-tier);
<strong>Lundin Gold</strong> (single-asset low-cost Ecuadorian producer);
<strong>Newmont</strong> (post-Newcrest integration story);
<strong>Kinross</strong> (multi-jurisdiction senior);
<strong>B2Gold</strong> (Mali-anchored senior with Canada development).</p>

<p>Scorecards will be published as research is completed through 2026. Each one lives at the
company's hub page — /companies/&lt;slug&gt;/ — with full factor breakdown and analyst summary.</p>

<h2>How to think about producer allocation</h2>
<p>Senior producers are the defensive anchor in a gold portfolio. Lower volatility than juniors,
dividend support in many cases, and positive gold-price leverage without the binary-event risk
of single-asset developers. The trade-off is capped upside in a gold bull run — a senior
producer participating in a 40% gold-price move typically delivers 30-50% equity returns, versus
3-10x on a leveraged junior. That bounded upside is the point, not the bug.</p>

<p>For a precious-metals allocation of any size, the typical construction is 30-50% in senior
producers and royalty names, balanced with 20-40% in mid-tier developers and the remainder in
higher-variance exploration names. The senior producer layer smooths returns during sector
drawdowns and funds rebalancing into higher-variance names after major corrections.</p>
""",
        "faq_items": [
            {"question": "Why haven't you scored the major gold producers yet?",
             "answer": "The framework was built to fill the rigorous-analysis gap in the junior mining universe where sell-side coverage is thin. Senior producers are covered extensively by institutional sell-side. That said, we are expanding senior coverage through 2026 — Agnico Eagle and Wesdome are the current priorities."},
            {"question": "Does the framework work for producers or only for juniors?",
             "answer": "It works for both with minor emphasis shifts. Geology uses reserves instead of exploration-stage resources. Capital incorporates debt levels and cash-flow sustainability. Management weights capital-allocation track record more heavily. Same 5-factor rubric, same 1-5 scoring."},
            {"question": "Which major gold producer should I start with?",
             "answer": "For operational quality and jurisdictional discipline, Agnico Eagle is widely considered best-in-class. For defensive exposure, Franco-Nevada (royalty) is the structural choice. For leveraged mid-tier exposure, Equinox Gold is the closest thing to a representative mid-tier we score."},
            {"question": "What's the difference between a senior producer and a mid-tier producer?",
             "answer": "Rough market-cap thresholds: majors above ~C$20B (Newmont, Barrick, Agnico), mid-tier C$3-20B (Kinross, B2Gold, Alamos, Equinox, Lundin Gold), junior producers below that. Production volume, mine diversification, and balance-sheet scale track with the tiers but not perfectly."},
        ],
    },
    # ──────────────── #17 — WATCH upgrade candidates ────────────────
    {
        "title": "One Factor Away From a BUY: WATCH-Rated Gold Stocks with Upgrade Potential",
        "meta_title": "WATCH-Rated Gold Stocks With BUY Upgrade Potential 2026",
        "meta_description": (
            "Ten WATCH-rated gold equities at composite 18-21 — one factor from BUY on our "
            "Verdict Framework. April 2026 ranked."
        ),
        "pillar_slug": "company-verdicts",
        "excerpt": (
            "The most actionable list in the framework: WATCH-rated names where a single factor "
            "upgrade would push them into BUY territory. Ten companies, what's holding them back, "
            "and what would change."
        ),
        "answer_capsule": (
            "Ten WATCH-rated gold and silver equities in April 2026 with composite scores between "
            "18 and 21 — each within one factor point of a BUY verdict. GoGold Resources (21/25), "
            "Equinox Gold (19/25), Integra Resources (19/25), Mako Mining (19/25), Probe Gold "
            "(19/25), Snowline Gold (19/25), Western Copper (19/25), Banyan Gold (18/25), "
            "Collective Mining (18/25), and Calibre Mining (18/25)."
        ),
        "key_takeaways": [
            "A BUY requires composite 18+ with no factor below 3 — several WATCH names are close",
            "GoGold at 21/25 WATCH is the most unusual — an editorial override on a technically-BUY composite",
            "The most common missing factor is catalyst (needs a near-term milestone) or acquisition value",
            "One catalyst delivery can flip a WATCH to BUY inside a single quarter",
            "Upgrade-candidate lists are high-turnover — expect quarterly composition changes",
        ],
        "ranked_items": [
            {"rank": 1, "name": "GoGold Resources Inc.", "ticker": "TSX:GGD", "company_slug": "gogold-resources-inc",
             "summary": "21/25 WATCH — silver-primary. Composite clears the BUY threshold; the WATCH is an editorial override on commodity-mix considerations. Factor mix: 4/5/4/5/3."},
            {"rank": 2, "name": "Equinox Gold Corp.", "ticker": "TSX:EQX", "company_slug": "equinox-gold-corp",
             "summary": "19/25 WATCH. Factor mix 3/5/4/4/3. Either a management score upgrade (post-integration track record) or an acquisition-value upgrade (post-operational de-risking) would take this to BUY."},
            {"rank": 3, "name": "Integra Resources Corp.", "ticker": "TSXV:ITR", "company_slug": "integra-resources-corp",
             "summary": "19/25 WATCH. Factor mix 4/4/4/3/4. A catalyst upgrade on the DeLamar engineering-study pathway is the most plausible path to BUY."},
            {"rank": 4, "name": "Mako Mining Corp.", "ticker": "TSXV:MKO", "company_slug": "mako-mining-corp",
             "summary": "19/25 WATCH. Factor mix 3/4/5/4/3. Management upgrade (from 3 to 4) would lift composite to 20 and comfortably into BUY."},
            {"rank": 5, "name": "Probe Gold Inc.", "ticker": "TSX:PRB", "company_slug": "probe-gold-inc",
             "summary": "19/25 WATCH. Factor mix 4/3/4/4/4. A geology upgrade (resource category or continuity progression) is the path — most plausible on continued Novador drilling."},
            {"rank": 6, "name": "Snowline Gold Corp.", "ticker": "TSX:SGD", "company_slug": "snowline-gold-corp",
             "summary": "19/25 WATCH. Factor mix 4/4/4/4/3. Acquisition-value upgrade on new Valley delineation comparable-transactions data would take it to BUY."},
            {"rank": 7, "name": "Western Copper and Gold Corporation", "ticker": "TSX:WRN", "company_slug": "western-copper-and-gold-corporation",
             "summary": "19/25 WATCH. Factor mix 3/5/4/3/4. Catalyst upgrade on the Casino permitting timeline is the most likely trigger — though the timeline works against near-term BUY conversion."},
            {"rank": 8, "name": "Banyan Gold Corp.", "ticker": "TSXV:BYN", "company_slug": "banyan-gold-corp",
             "summary": "18/25 WATCH. Factor mix 4/3/4/4/3. Geology upgrade on AurMac resource continuity or grade would push composite to 19+."},
            {"rank": 9, "name": "Collective Mining Ltd.", "ticker": "TSX:CNL", "company_slug": "collective-mining-ltd",
             "summary": "18/25 WATCH. Factor mix 5/2/5/4/2. Geology is the hard constraint at 2/5 — requires material new discovery to move. The most work-intensive upgrade path on the list."},
            {"rank": 10, "name": "Calibre Mining Corp.", "ticker": "TSX:CXB", "company_slug": "calibre-mining-corp",
             "summary": "18/25 WATCH. Factor mix 3/4/3/4/4. Management or capital upgrade would push this across. Both are achievable inside a quarter."},
        ],
        "body": """
<h2>Why this list matters</h2>
<p>Upgrade-candidate lists are the most actionable output of any scoring framework. A BUY-rated
name is already at its rating — the market is arguably pricing it in. A WATCH-rated name one
factor away from a BUY is where the conversion event itself drives the price action. If you
can anticipate which factor will move first and when, you can position ahead of the re-rating.</p>

<p>The ten names above are all WATCH-rated with composite scores of 18-21 in April 2026. Each is
within a single factor upgrade of crossing into BUY territory. The article below walks through
what factor needs to change for each, and what the triggering event typically looks like.</p>

<h2>The anomaly at the top</h2>
<p>GoGold at 21/25 is the unusual entry. A composite of 21 with no factor below 3 would typically
map to BUY per the framework's standing rule. The WATCH is an editorial override — the analyst
team applied judgment on commodity-mix considerations (silver-primary in a gold-anchored coverage
universe) and jurisdictional timing. Whether the override persists into the next scoring cycle
is a question the framework answers in the next scorecard, not this listicle. From a positioning
standpoint, treat GoGold as functionally BUY-rated.</p>

<h2>The most common upgrade path: catalyst delivery</h2>
<p>Five of the ten names are held back by a catalyst score of 3/5 or a related factor dependent
on near-term news. Catalyst upgrades happen naturally — a drill result lands, a resource update
gets published, a permitting milestone clears. The positioning question is which upgrades are
closest in time. Integra Resources has engineering-study milestones pending on DeLamar. Probe
Gold has continued Novador drilling. Snowline has ongoing Valley delineation with potential for
a material resource update.</p>

<p>The names where catalyst is the limiter but the timeline is long (Western Copper's Casino
permitting is measured in years) are structurally different. The math can still support a
position, but the path to a BUY conversion is longer and the intervening periods tend to be
rangebound.</p>

<h2>The harder upgrades: geology and management</h2>
<p>Collective Mining stands out as the most work-intensive upgrade case. The management factor is
5/5 and capital is 5/5 — both maximal. Geology sits at 2/5, and that's what's holding the
composite at 18. A geology upgrade requires either material new discovery (a genuinely new zone
or deposit style) or a substantial resource update that reclassifies ounces. Neither happens
inside a quarter. If you own Collective on this thesis, the timeline is likely a year or two.</p>

<p>Management upgrades are also slow. Banyan and Mako could both lift through management upgrades,
but management factor scores rarely move on quarterly cadence — they tend to move in response
to multi-year track records, major insider-buying events, or team changes. Position sizing
should reflect the timeline difference.</p>

<h2>How to use this list in a position</h2>
<p>Upgrade-candidate names typically trade at a small discount to directly-comparable BUY-rated
peers. The discount represents the probability-weighted difference between being BUY and being
WATCH. If you believe the upgrade is likely within 6-12 months, that discount is
the return. A portfolio that holds two or three upgrade candidates alongside the BUY-rated core
typically captures most of the re-rating return without requiring perfect single-name timing.</p>
""",
        "faq_items": [
            {"question": "What triggers a BUY verdict?",
             "answer": "A composite score of 18 or higher out of 25, with no single factor scored below 3. Both conditions must hold. Five companies currently meet the bar; ten more sit at composite 18 or above but miss on a single factor."},
            {"question": "Why is GoGold listed as WATCH if its composite is 21?",
             "answer": "The WATCH is an editorial override. The composite technically clears the BUY threshold, but the analyst team applied judgment on commodity-mix and timing factors that the rubric doesn't explicitly score. Whether the override persists gets resolved in the next scorecard, not in a listicle."},
            {"question": "How often do WATCH-to-BUY upgrades happen?",
             "answer": "Historically, about two to four per quarter across our coverage universe. Catalyst-driven upgrades are fastest (a single drill result or resource update can flip a composite). Geology and management upgrades are slower, often taking multiple quarters."},
            {"question": "Is buying an upgrade candidate ahead of the conversion a good strategy?",
             "answer": "It can be, if your conviction on which factor will move first is genuinely informed. The discount to comparable BUY-rated peers is typically small — 10-20%. The alpha comes from correctly identifying the trigger, not from owning the basket passively."},
        ],
    },
    # ──────────────── #18 — Americas ex-Canada ────────────────
    {
        "title": "Junior Gold Miners in the Americas: Guyana, Mexico, Nicaragua and Beyond",
        "meta_title": "Junior Gold Miners in Americas 2026: Guyana, Mexico, Nicaragua",
        "meta_description": (
            "Eight gold equities operating across Latin America and the Caribbean — ranked "
            "on the Verdict Framework for April 2026."
        ),
        "pillar_slug": "company-verdicts",
        "excerpt": (
            "Eight companies on our coverage list operating in the Americas outside Canada — "
            "Mexico, Guyana, Nicaragua, Colombia, Brazil, and the Dominican Republic. Ranked by "
            "Verdict Framework composite score."
        ),
        "answer_capsule": (
            "Eight gold-focused equities operate in the Americas outside Canada on our April 2026 "
            "coverage list. Heliostar Metals (Mexico, BUY 20/25) and G2 Goldfields (Guyana, BUY "
            "20/25) lead. Mako Mining, Calibre Mining (both Nicaragua), and Collective Mining "
            "(Colombia) are the mid-tier picks. GoldMining Inc. (Brazil), Omai Gold (Guyana) follow. "
            "Precipitate Gold (Dominican Republic, AVOID) and Max Resource (Colombia copper, AVOID) "
            "trail."
        ),
        "key_takeaways": [
            "Mexico and Guyana host the only two BUY-rated Americas juniors — Heliostar and G2",
            "Nicaragua (Mako, Calibre) has become a quietly-important producer jurisdiction",
            "Jurisdictional risk varies sharply even within Americas ex-Canada",
            "The framework scores jurisdiction indirectly through capital and catalyst factors",
            "Two AVOIDs on the list — both on factor math rather than pure jurisdictional risk",
        ],
        "ranked_items": [
            {"rank": 1, "name": "Heliostar Metals Ltd.", "ticker": "TSXV:HSTR", "company_slug": "heliostar-metals-ltd",
             "summary": "20/25 BUY. Mexico. Producer-developer with active drill program funded by cash flow. The best-in-class Mexican junior on coverage."},
            {"rank": 2, "name": "G2 Goldfields Inc.", "ticker": "TSX:GTWO", "company_slug": "g2-goldfields-inc",
             "summary": "20/25 BUY. Guyana. Management 5/5 and catalyst 5/5. The Guyana gold story of the last three years."},
            {"rank": 3, "name": "Mako Mining Corp.", "ticker": "TSXV:MKO", "company_slug": "mako-mining-corp",
             "summary": "19/25 WATCH. Nicaragua. San Albino producer with 5/5 capital structure. The rare self-funding TSX-V junior."},
            {"rank": 4, "name": "Calibre Mining Corp.", "ticker": "TSX:CXB", "company_slug": "calibre-mining-corp",
             "summary": "18/25 WATCH. Nicaragua and Nevada. Multi-asset producer with acquisition-value 4/5. The most diversified name on the list."},
            {"rank": 5, "name": "Collective Mining Ltd.", "ticker": "TSX:CNL", "company_slug": "collective-mining-ltd",
             "summary": "18/25 WATCH. Colombia. Management 5/5 and capital 5/5 — the highest-quality team exposure outside Canada. Geology 2/5 is the project-level constraint."},
            {"rank": 6, "name": "GoldMining Inc.", "ticker": "TSX:GOLD", "company_slug": "goldmining-inc",
             "summary": "15/25 WATCH. Brazil portfolio. The classic in-ground-ounces holding company. P/NAV 0.78x."},
            {"rank": 7, "name": "Omai Gold Mines Corp.", "ticker": "TSXV:OMG", "company_slug": "omai-gold-mines-corp",
             "summary": "15/25 WATCH. Guyana. Historic Omai mine restart story. P/NAV 3.64x reflects market anticipation of a restart milestone."},
            {"rank": 8, "name": "Max Resource Corp.", "ticker": "TSXV:MAX", "company_slug": "max-resource-corp",
             "summary": "11/25 AVOID. Colombia copper. The CESAR project scores poorly on geology and management; jurisdiction is a factor but not the primary driver of the AVOID."},
            {"rank": 9, "name": "Precipitate Gold Corp.", "ticker": "TSXV:PRG", "company_slug": "precipitate-gold-corp",
             "summary": "9/25 AVOID. Dominican Republic. Geology 1/5 and acquisition value 1/5. A project-level AVOID, not a country-level one."},
        ],
        "body": """
<h2>Why an Americas-ex-Canada framing makes sense</h2>
<p>Canadian investors tend to split the precious metals universe into Canada and "everywhere
else" — with "everywhere else" lumped together under generic jurisdictional-risk discount. That
framing is too coarse. Mexico, Guyana, Nicaragua, Ecuador, and Brazil have different regulatory
regimes, different fiscal terms, different permitting realities, and different historical
track records. A gold project in Mexico is structurally different from one in Nicaragua, which
is different from Guyana or Colombia. Grouping them all under "LatAm risk" misses the real
jurisdictional picture.</p>

<p>That said, for portfolio construction purposes, there is value in thinking about Americas
ex-Canada as a single basket — because the ex-Canada names collectively offer different
macro exposure than pure Canadian gold. Currency effects, commodity-price beta, and the
political calendar all differ from pure-Canadian exposure. A 15-25% allocation to Americas
ex-Canada gold names is a reasonable diversification layer for a Canadian-anchored portfolio.</p>

<h2>Mexico: the quiet producer jurisdiction</h2>
<p>Mexico remains the most important gold-silver mining jurisdiction outside Canada and the US
by operator count. Heliostar is the only Mexican name in our BUY-rated list, but GoGold (silver)
also operates primarily in Mexico. Capital-allocation discipline among Mexican-operating juniors
tends to be good — they've had to be, given the more challenging financing environment than
comparable TSX-listed Canadian operators. The trade-off is higher political risk around mining
concessions, illustrated by the 2022 AMLO-era regulatory tightening.</p>

<h2>Guyana: the hottest gold story of the 2020s</h2>
<p>Guyana has emerged as one of the most active gold exploration jurisdictions globally over the
last five years, driven by the Omai mine district's rediscovery and a series of major
transactions (G2 Goldfields' parent transactions, Zijin's involvement). Our coverage includes
G2 (BUY) and Omai Gold (WATCH, WATCH-adjacent). The geological potential is real; the
jurisdictional maturity is still developing, which shows up in permitting timelines and
infrastructure scarcity.</p>

<h2>Nicaragua: the producer's jurisdiction</h2>
<p>Nicaragua hosts two of our WATCH-rated producers — Mako Mining and Calibre Mining. Both operate
producing mines with mature local workforces and established regulatory relationships. The
political risk discount that has historically applied to Central American mining has narrowed as
operational track records have lengthened. For investors looking for producer-stage gold exposure
outside Canada, the Nicaragua names are worth the research time.</p>

<h2>Colombia, Brazil, and the rest</h2>
<p>Colombia (Collective, Max Resource) offers exceptional geological potential combined with
complex regulatory evolution. Collective's Guayabales exploration work has drawn major-company
interest; Max Resource has scored AVOID on project-specific factors, not jurisdictional ones.</p>

<p>Brazil (GoldMining Inc.) has a mature mining framework but a high tax burden and historically
complex permitting. GoldMining is structured as an in-ground-ounces holding company, which
differs from the operator model of most names on this list.</p>

<p>Ecuador (Lundin Gold, not yet scored), Peru, and other Andean jurisdictions have meaningful
gold-and-copper exposure that we will add to coverage as research capacity allows.</p>

<h2>The two AVOIDs</h2>
<p>Both Max Resource and Precipitate Gold carry AVOID verdicts — and both are driven by project-
specific factor scores (geology, management, acquisition value), not by jurisdictional
categorisation. A company can operate in a reasonable jurisdiction and still score AVOID if the
project and team factors don't support a higher verdict. Conversely, a company can operate in
a jurisdiction the market discounts heavily and still earn a BUY if the underlying factors are
strong. The framework separates those signals.</p>
""",
        "faq_items": [
            {"question": "Do you score jurisdictional risk directly?",
             "answer": "Not as a separate factor. Jurisdictional risk bleeds into the capital and catalyst scores (via financing access and permit timelines) and into acquisition value (via comparable-transaction sets). A higher-risk jurisdiction that produces smooth capital raises and reasonable timelines may actually score better than a 'safer' jurisdiction with slower fundamentals."},
            {"question": "Why is Nicaragua on the coverage list when it has political risk?",
             "answer": "Because our Nicaragua-operating companies (Mako, Calibre) have multi-year producer track records with mature operational and regulatory relationships. The jurisdictional risk exists and is discounted into valuations, but the project-level factors are real and scoreable."},
            {"question": "Is Mexico still an attractive mining jurisdiction after the AMLO-era tightening?",
             "answer": "For operators with established concessions and mature local relationships, yes. New concessions and mineral-claim expansions have become more complex. Heliostar's Mexican operations and GoGold's Los Ricos development have both continued to advance, suggesting incumbents retain meaningful optionality."},
            {"question": "When will Lundin Gold be scored?",
             "answer": "Lundin Gold is on the research queue. Its single-asset Fruta del Norte operation (Ecuador) is one of the world's lowest-cost gold mines by quartile AISC, which makes it an important benchmark for any Ecuador or high-grade underground comparison. Coverage is planned for 2026."},
        ],
    },
    # ──────────────── #19 — Gold-Silver Polymetallic ────────────────
    {
        "title": "Gold-Silver Polymetallic Mining Stocks for 2026: Silver Exposure Within a Gold Portfolio",
        "meta_title": "Gold-Silver Polymetallic Mining Stocks 2026",
        "meta_description": (
            "GoGold leads our silver-primary coverage. Peer silver majors — Aya, MAG, Pan "
            "American, Fortuna, Endeavour — queued for scoring. April 2026 roundup."
        ),
        "pillar_slug": "investing-guides",
        "excerpt": (
            "Silver deserves portfolio allocation distinct from gold — the macro drivers differ. "
            "GoGold Resources is our leading silver-primary scorecard. The senior silver peer set "
            "is queued for framework coverage."
        ),
        "answer_capsule": (
            "Silver and gold-silver polymetallic exposure is lighter on our coverage than pure "
            "gold. GoGold Resources holds a 21/25 WATCH score as of April 2026 — the only silver-"
            "primary name currently scored. Aya Gold & Silver, MAG Silver, Pan American Silver, "
            "Fortuna Mining, Silvercorp, Endeavour Silver, and First Majestic are queued for the "
            "next research cycle."
        ),
        "key_takeaways": [
            "Silver responds to different macro drivers than gold — industrial plus monetary demand",
            "GoGold Resources scores 21/25 on our framework with geology 5/5 and catalyst 5/5",
            "The senior silver peer set is queued for framework coverage in 2026",
            "Gold-silver ratio cycles are a real portfolio construction input",
            "Silver equity volatility is structurally higher than gold equity volatility",
        ],
        "ranked_items": [
            {"rank": 1, "name": "GoGold Resources Inc.", "ticker": "TSX:GGD", "company_slug": "gogold-resources-inc",
             "summary": "21/25 WATCH. Silver-primary (Mexico). Los Ricos development plus Parral production. Geology 5/5, catalyst 5/5. The highest-scoring silver name on our coverage."},
            {"rank": 2, "name": "Aya Gold & Silver Inc.", "ticker": "TSX:AYA", "company_slug": "aya-gold-and-silver-inc",
             "summary": "Not yet scored. Morocco-focused silver producer with the Zgounder mine and development pipeline. Queued for coverage in 2026."},
            {"rank": 3, "name": "MAG Silver Corp.", "ticker": "TSX:MAG", "company_slug": "mag-silver-corp",
             "summary": "Not yet scored. Joint-venture interest in the Juanicipio silver mine (Mexico) with Fresnillo. One of the highest-grade silver operations globally. Queued."},
            {"rank": 4, "name": "Pan American Silver Corp.", "ticker": "TSX:PAAS", "company_slug": "pan-american-silver-corp",
             "summary": "Not yet scored. Senior silver producer with operations across the Americas post-Yamana acquisition. Queued for coverage."},
            {"rank": 5, "name": "Fortuna Mining Corp.", "ticker": "TSX:FVI", "company_slug": "fortuna-mining-corp",
             "summary": "Not yet scored. Mid-tier silver-gold producer with operations in Americas and West Africa. Queued for coverage."},
            {"rank": 6, "name": "Endeavour Silver Corp.", "ticker": "TSX:EDR", "company_slug": "endeavour-silver-corp",
             "summary": "Not yet scored. Mexico and Chile silver producer. Pyrenees project in Chile is the growth leg. Queued."},
            {"rank": 7, "name": "Silvercorp Metals Inc.", "ticker": "TSX:SVM", "company_slug": "silvercorp-metals-inc",
             "summary": "Not yet scored. China and Ecuador silver producer. Distinct jurisdictional exposure relative to the Mexico-heavy silver universe. Queued."},
            {"rank": 8, "name": "First Majestic Silver Corp.", "ticker": "TSX:FR", "company_slug": "first-majestic-silver-corp",
             "summary": "Not yet scored. Mexico-focused silver producer with operational track record across multiple mines. Already on company records — queued for scorecard."},
        ],
        "body": """
<h2>Why silver deserves its own portfolio allocation</h2>
<p>Gold and silver are often grouped as "precious metals," but their macro drivers are
meaningfully different. Gold is primarily a monetary commodity — it responds to real interest
rates, central-bank buying, safe-haven demand, and currency debasement narratives. Silver is
a monetary commodity too, but it has a substantial industrial demand component: photovoltaic
solar panels, electronics, electric vehicle contacts, and photography (declining but still
meaningful). That industrial demand layer introduces correlation with manufacturing activity
and grid-buildout capex that gold simply doesn't have.</p>

<p>The practical consequence: silver often moves less than gold in a risk-off episode (lower
monetary premium) but more than gold in a cyclical expansion (higher industrial beta). Silver
equities tend to be more volatile than gold equities for the same reason. A portfolio construction
view that says "silver is just leveraged gold" captures some of the truth but misses the
industrial demand angle.</p>

<h2>The gold-silver ratio and what it means</h2>
<p>The gold-silver ratio — gold price divided by silver price — has cycled between roughly 50
and 100 over the past two decades, with extreme moves to 120+ in crisis conditions. A high ratio
(>80) historically implies silver is "cheap" relative to gold; a low ratio (<60) implies
silver is rich. Contrarian investors use the ratio as an allocation signal between gold and
silver equities. The framework does not score the ratio directly, but it's a reasonable input
for sizing between gold and silver holdings.</p>

<h2>Our silver coverage today</h2>
<p>GoGold Resources is currently our only silver-primary scorecard at 21/25. The composite clears
the BUY threshold but the WATCH rating reflects editorial considerations around silver's distinct
macro behavior within a gold-anchored framework. Los Ricos (Mexico) is the development asset;
Parral (Mexico) is the producing cash-flow base. Geology scores 5/5; catalyst scores 5/5. From
a pure-framework-math perspective, GoGold is the strongest silver-primary name in our universe.</p>

<h2>The senior silver peer set we don't yet score</h2>
<p>Seven senior silver names are queued for coverage: Aya Gold & Silver (Morocco), MAG Silver
(Mexico, Juanicipio joint venture with Fresnillo), Pan American Silver (Americas), Fortuna
Mining (Americas and West Africa), Endeavour Silver (Mexico and Chile), Silvercorp Metals
(China and Ecuador), and First Majestic Silver (Mexico). These names span the spectrum from
high-grade single-asset operators (MAG) to multi-asset regional producers (Pan American,
Fortuna). Each will get a scorecard in the 2026 coverage cycle.</p>

<p>Until the scorecards are published, these names are best evaluated against the general
framework principles — but without the specific factor scoring that makes direct comparison
possible. Read individual company 43-101s and financial filings for the primary analysis;
scorecards will follow.</p>

<h2>How to size silver within a precious-metals portfolio</h2>
<p>Rough construction guidance: for a 20-30% precious-metals allocation in a broader portfolio,
silver typically represents 20-40% of the precious-metals sleeve. That is, 4-12% of total portfolio
exposure. The actual allocation within that range should track gold-silver ratio dynamics —
more silver when the ratio is high (silver cheap), less silver when the ratio is low. Position
sizing within silver should reflect the higher volatility profile: if your gold position sizing
is 3-5% per name, silver positions should sit at 2-3% per name to equalise risk contribution.</p>
""",
        "faq_items": [
            {"question": "How is silver different from gold as an investment?",
             "answer": "Gold is primarily a monetary commodity driven by real rates, central-bank buying, and safe-haven demand. Silver is a monetary commodity plus an industrial commodity — photovoltaics, electronics, EVs. That dual demand structure makes silver respond differently to macro cycles than gold."},
            {"question": "What's the gold-silver ratio and why does it matter?",
             "answer": "Gold price divided by silver price. Historically cycles between 50 and 100. A high ratio (>80) implies silver is cheap relative to gold; a low ratio (<60) implies silver is rich. Some investors use the ratio to size gold versus silver allocations."},
            {"question": "Why doesn't the framework score more silver names?",
             "answer": "Coverage capacity. The framework was built starting with gold juniors where the analytical gap was largest. Senior silver producers are covered by institutional sell-side and haven't been research-priority for our small-retail-investor focus. We are expanding silver coverage through 2026."},
            {"question": "Which silver stock is the best buy right now?",
             "answer": "Of our currently-scored coverage, GoGold Resources (21/25 WATCH) is the only silver-primary name with a published scorecard. From a pure-framework-math view, it is the highest-scoring silver equity on our coverage. The senior silver peer set is queued — scorecards in 2026 will enable direct comparison."},
        ],
    },
    # ──────────────── #20 — TSX Senior Board ────────────────
    {
        "title": "Top TSX Senior Board Gold Mining Stocks for 2026",
        "meta_title": "Top TSX Gold Mining Stocks 2026: Senior Board Ranked",
        "meta_description": (
            "Ten TSX senior board gold equities ranked on our Verdict Framework for 2026. "
            "Franco-Nevada, Fury, G2 Goldfields, and more."
        ),
        "pillar_slug": "company-verdicts",
        "excerpt": (
            "Ten gold and gold-adjacent equities listed on the TSX senior board (not the Venture), "
            "ranked by our Verdict Framework composite score. The TSX-V list is a separate "
            "listicle — this one covers the senior board."
        ),
        "answer_capsule": (
            "Ten TSX senior board gold and gold-adjacent equities on our April 2026 coverage "
            "list: Franco-Nevada (21/25, BUY), GoGold Resources (21/25, WATCH — silver), Fury "
            "Gold Mines (20/25, BUY), G2 Goldfields (20/25, BUY), Equinox Gold (19/25, WATCH), "
            "Probe Gold (19/25, WATCH), Snowline Gold (19/25, WATCH), Western Copper and Gold "
            "(19/25, WATCH), Calibre Mining (18/25, WATCH), and Liberty Gold (17/25, WATCH)."
        ),
        "key_takeaways": [
            "TSX senior board listings have stricter disclosure thresholds than the Venture",
            "Three TSX BUYs: Franco-Nevada, Fury Gold Mines, G2 Goldfields",
            "TSX senior-board liquidity is meaningfully deeper than TSX-V — positions size easier",
            "Seven names score 19 or higher — senior board quality is visible",
            "The producer-to-explorer mix is broader on TSX than on TSX-V",
        ],
        "ranked_items": [
            {"rank": 1, "name": "Franco-Nevada Corp.", "ticker": "TSX:FNV", "company_slug": "franco-nevada-corp",
             "summary": "21/25 BUY. Royalty and streaming major. The defensive anchor."},
            {"rank": 2, "name": "GoGold Resources Inc.", "ticker": "TSX:GGD", "company_slug": "gogold-resources-inc",
             "summary": "21/25 WATCH. Silver-primary. Mexican operations. Editorial override keeps the technical-BUY composite at WATCH."},
            {"rank": 3, "name": "Fury Gold Mines Limited", "ticker": "TSX:FURY", "company_slug": "fury-gold-mines-limited",
             "summary": "20/25 BUY. Quebec and Newfoundland portfolio. Balanced 4-across with P/NAV of 0.55x."},
            {"rank": 4, "name": "G2 Goldfields Inc.", "ticker": "TSX:GTWO", "company_slug": "g2-goldfields-inc",
             "summary": "20/25 BUY. Guyana. Management 5/5 and catalyst 5/5."},
            {"rank": 5, "name": "Equinox Gold Corp.", "ticker": "TSX:EQX", "company_slug": "equinox-gold-corp",
             "summary": "19/25 WATCH. Mid-tier producer across Americas. Geology 5/5."},
            {"rank": 6, "name": "Probe Gold Inc.", "ticker": "TSX:PRB", "company_slug": "probe-gold-inc",
             "summary": "19/25 WATCH. Novador complex, Quebec. Management 4/5 and capital 4/5."},
            {"rank": 7, "name": "Snowline Gold Corp.", "ticker": "TSX:SGD", "company_slug": "snowline-gold-corp",
             "summary": "19/25 WATCH. Valley project, Yukon. Balanced 4-across with acquisition value as the one gap."},
            {"rank": 8, "name": "Western Copper and Gold Corporation", "ticker": "TSX:WRN", "company_slug": "western-copper-and-gold-corporation",
             "summary": "19/25 WATCH. Casino project, Yukon copper-gold-moly. Geology 5/5."},
            {"rank": 9, "name": "Calibre Mining Corp.", "ticker": "TSX:CXB", "company_slug": "calibre-mining-corp",
             "summary": "18/25 WATCH. Multi-asset producer, Nicaragua and Nevada."},
            {"rank": 10, "name": "Liberty Gold Corp.", "ticker": "TSX:LGD", "company_slug": "liberty-gold-corp",
             "summary": "17/25 WATCH. Black Pine oxide gold project (Idaho, USA). Geology 4/5."},
        ],
        "body": """
<h2>TSX senior board vs TSX-V — what the listing venue tells you</h2>
<p>The TSX senior board and the TSX Venture (TSX-V) serve different ends of the mining capital
spectrum. The TSX senior requires audited financials, minimum market cap ($10M for mining),
minimum public float, and ongoing continuous-disclosure obligations that are stricter than
Venture. The Venture is designed for earlier-stage companies with smaller floats and less
institutional coverage. Both are legitimate junior mining venues, but the senior board brings
liquidity depth, institutional eligibility (many Canadian pension funds cannot hold Venture
listings), and a quality threshold that screens out the weakest names.</p>

<p>For a retail investor looking to build a position of any size, the TSX senior board list
above is the more practical starting point. Liquidity is meaningfully deeper — you can build
a C$50K position in any of these names without moving the market, which is not always true on
the Venture. The trade-off is fewer "explorer-stage" optionality plays; the Venture remains
where the highest-variance, earliest-stage discoveries live.</p>

<h2>What the TSX list reveals</h2>
<p>Three BUYs on the TSX senior board — Franco-Nevada, Fury, G2 Goldfields — represents
meaningful quality density. The TSX-V BUY list is shorter in our coverage (Amex Exploration and
Heliostar Metals are both TSX-V). This pattern reflects the structural selection bias of the
senior board: companies that graduate from TSX-V to TSX have typically cleared their most severe
capital-structure and geological risks, which the framework rewards in the capital and geology
factors.</p>

<p>That said, the senior board is not uniformly stronger. Liberty Gold at 17/25 and Calibre
Mining at 18/25 are solid but unremarkable; STLLR Gold at 14/25 (not on this list) is a
reminder that the senior board contains names across the full framework range, including some
that sit below a TSX-V top-10 list.</p>

<h2>The producer-explorer mix on the TSX</h2>
<p>The TSX senior board of gold equities hosts a broader stage mix than the Venture. Calibre
Mining and Equinox Gold are multi-mine producers. Franco-Nevada is a royalty major. Fury, Probe,
and Liberty are developers. Snowline is a late-stage explorer-discovery story. The Venture
would have a tighter skew toward explorer stage. Investors looking for producing cash-flow
exposure should lean TSX senior; investors looking for discovery-stage optionality should lean
TSX-V.</p>

<h2>How to use this list alongside the TSX-V list</h2>
<p>The two listicles are complements, not competitors. A reasonably-sized gold portfolio might
include 2-3 names from the TSX senior list (for liquidity and quality anchor) and 2-3 names
from the TSX-V list (for exploration-stage optionality). The combined basket captures both the
defensive quality of the senior board and the higher-variance upside of the Venture. Position
sizing should differ — senior-board positions can be 2-3x larger than Venture positions
at equivalent conviction, given the liquidity and risk-profile differences.</p>
""",
        "faq_items": [
            {"question": "What's the difference between TSX and TSX Venture?",
             "answer": "TSX is the senior board with stricter financial and disclosure thresholds, deeper liquidity, and institutional eligibility. TSX Venture is designed for earlier-stage companies with smaller floats and less institutional coverage. Many Canadian pension funds cannot hold Venture listings; most can hold TSX."},
            {"question": "Why is GoGold on the TSX rather than TSX-V?",
             "answer": "GoGold graduated to the TSX senior board as the Los Ricos project advanced from exploration to development stage and the market capitalisation grew. Producers and advanced developers typically graduate from the Venture to the senior board as they mature."},
            {"question": "Should I prefer TSX stocks over TSX-V stocks for mining exposure?",
             "answer": "For liquidity and quality-anchor exposure, yes. For discovery-stage upside, no. Most balanced gold portfolios hold both — TSX senior for the liquid core positions and TSX-V for higher-variance exploration bets. Position sizing should differ to reflect liquidity and risk profile."},
            {"question": "Do TSX-listed stocks trade in the US?",
             "answer": "Most TSX senior board mining names also trade on the OTC market in the US, and some have dual NYSE American listings. Liquidity on the primary TSX listing is typically deeper than the US secondary listing, so Canadian-dollar-based investors should trade on TSX directly when possible."},
        ],
    },
]


def seed_more_listicles(apps, schema_editor):
    # Import live models so custom save() (word_count) runs.
    from apps.blog.models import Post, Pillar
    from apps.verdict.models import Company
    from apps.accounts.models import User

    # ── Step 1: Create new Company placeholders ──
    for data in NEW_COMPANIES:
        if Company.objects.filter(ticker=data["ticker"], exchange=data["exchange"]).exists():
            continue
        Company.objects.create(
            ticker=data["ticker"],
            exchange=data["exchange"],
            name=data["name"],
            primary_commodity=data.get("primary_commodity", ""),
            jurisdiction=data.get("jurisdiction", ""),
            needs_research=True,
            data_filled=False,
        )

    # ── Step 2: Author lookup ──
    try:
        author = User.objects.get(username="chaugen")
    except User.DoesNotExist:
        return

    # ── Step 3: Publish schedule — start the day after the last listicle from 0009 ──
    # 0009 seeded through 2026-04-27. Continue from 2026-04-28 at 10:00 UTC.
    start = datetime(2026, 4, 28, 10, 0, 0, tzinfo=dt_timezone.utc)

    # ── Step 4: Create listicles ──
    for i, data in enumerate(LISTICLES):
        if Post.objects.filter(title=data["title"]).exists():
            continue
        pillar = Pillar.objects.filter(slug=data["pillar_slug"]).first()
        Post.objects.create(
            title=data["title"],
            author=author,
            excerpt=data["excerpt"],
            answer_capsule=data["answer_capsule"],
            key_takeaways=data["key_takeaways"],
            body=data["body"],
            faq_items=data["faq_items"],
            ranked_items=data["ranked_items"],
            pillar=pillar,
            post_type="listicle",
            status="published",
            is_premium=False,
            published_at=start + timedelta(days=i),
            meta_title=data.get("meta_title", ""),
            meta_description=data.get("meta_description", ""),
        )


def reverse_seed(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    Company = apps.get_model("verdict", "Company")
    titles = [d["title"] for d in LISTICLES]
    Post.objects.filter(title__in=titles).delete()
    new_tickers = [d["ticker"] for d in NEW_COMPANIES]
    Company.objects.filter(
        ticker__in=new_tickers,
        scorecards__isnull=True,
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0009_seed_listicles"),
        ("verdict", "0005_company_tier"),
    ]
    operations = [
        migrations.RunPython(seed_more_listicles, reverse_seed),
    ]
