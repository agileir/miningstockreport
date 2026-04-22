"""
Seed 5 listicle posts with staggered publish dates (one per day starting
tomorrow from migration run time).

Content is anchored to the actual Verdict Framework scorecards on the site
as of the migration date. If you re-run this migration after the scorecards
shift, the copy will age — treat these posts as editorial, not live data.
"""
from datetime import timedelta
from django.db import migrations
from django.utils import timezone


LISTICLES = [
    # ────────────────────────────────────────────────────────────────────
    # Listicle 1 — BUY-Rated
    # ────────────────────────────────────────────────────────────────────
    {
        "title": "Best Junior Gold Mining Stocks for 2026: BUY-Rated on the Verdict Framework",
        "meta_title": "Best Junior Gold Mining Stocks 2026: BUY-Rated Picks",
        "meta_description": (
            "Five gold equities earned a BUY verdict on our 5-factor Verdict Framework "
            "in April 2026. Composite scores, P/NAV, and per-company reasoning."
        ),
        "pillar_slug": "company-verdicts",
        "excerpt": (
            "Five companies earned a BUY verdict from our 5-factor Verdict Framework in "
            "early 2026 — Amex Exploration, Franco-Nevada, Heliostar Metals, G2 Goldfields, "
            "and Fury Gold Mines. Here's what each one scored and why."
        ),
        "answer_capsule": (
            "As of April 2026, five gold equities on our coverage list hold a BUY verdict "
            "on the Verdict Framework: Amex Exploration (21/25), Franco-Nevada (21/25), "
            "Heliostar Metals (20/25), G2 Goldfields (20/25), and Fury Gold Mines (20/25). "
            "Each scored at least 3/5 on every one of the five factors — management, "
            "geology, capital structure, catalysts, and acquisition value."
        ),
        "key_takeaways": [
            "Only five of 39 covered companies earned a BUY verdict in the current review cycle",
            "The top composite score (21/25) is shared by Amex Exploration and Franco-Nevada",
            "Four of the five BUYs are primarily exposed to Canadian or near-shore Americas gold",
            "P/NAV ranges from 0.55x (Fury) to 1.87x (G2) — discount is not a prerequisite for a BUY",
            "A BUY is a framework score, not a price target or a recommendation to buy at any price",
        ],
        "ranked_items": [
            {
                "rank": 1, "name": "Amex Exploration Inc.", "ticker": "TSXV:AMX",
                "company_slug": "amex-exploration-inc",
                "summary": (
                    "Composite 21/25. Amex scores a perfect 5/5 on geology (Perron project grades "
                    "and continuity) and a 5/5 on catalyst proximity (imminent resource update). "
                    "P/NAV of 0.64x adds upside leverage. Capital structure (3/5) is the one factor "
                    "that prevented a full five-across."
                ),
            },
            {
                "rank": 2, "name": "Franco-Nevada Corp.", "ticker": "TSX:FNV",
                "company_slug": "franco-nevada-corp",
                "summary": (
                    "Composite 21/25. The outlier on this list — a royalty and streaming major, "
                    "not a junior by any reasonable definition. Scores 5/5 on both management "
                    "(decades-long track record) and capital structure (no debt, diversified "
                    "royalty book). Trades at a 1.12x P/NAV premium; upside is bounded but "
                    "downside is the most defensive on the list."
                ),
            },
            {
                "rank": 3, "name": "Heliostar Metals Ltd.", "ticker": "TSXV:HSTR",
                "company_slug": "heliostar-metals-ltd",
                "summary": (
                    "Composite 20/25. Heliostar is a rare producer-developer on the TSX-V — "
                    "cash-flowing Mexican ounces funding a development pipeline. Catalyst "
                    "score of 5/5 reflects a busy 2026 schedule of drill releases. P/NAV 1.21x."
                ),
            },
            {
                "rank": 4, "name": "G2 Goldfields Inc.", "ticker": "TSX:GTWO",
                "company_slug": "g2-goldfields-inc",
                "summary": (
                    "Composite 20/25. Management scored 5/5 — meaningful insider buying and a "
                    "seasoned Guyana operator. Catalyst 5/5 for an aggressive drill program. "
                    "P/NAV of 1.87x is the highest on this list, reflecting the market already "
                    "pricing in exploration success."
                ),
            },
            {
                "rank": 5, "name": "Fury Gold Mines Limited", "ticker": "TSX:FURY",
                "company_slug": "fury-gold-mines-limited",
                "summary": (
                    "Composite 20/25. The most discounted BUY on the list at 0.55x P/NAV. "
                    "Balanced 4-across the five factors — no factor standout, no factor weakness. "
                    "Quebec and Newfoundland gold portfolio with optionality in multiple projects."
                ),
            },
        ],
        "body": """
<h2>What a BUY verdict actually means</h2>
<p>A BUY verdict on the Verdict Framework is not a price target, a prediction, or a recommendation
to buy any company at any price. It is a structured read on how a company scores across five
independent factors: management skin-in-the-game, project geology quality, capital structure
health, catalyst proximity, and comparable acquisition value. Each factor is scored 1–5 from
public filings — SEDI insider transactions, NI 43-101 technical reports, management information
circulars, and the most recent quarterly MD&amp;As. A composite score of 18/25 or higher,
with no single factor below 3, earns the BUY.</p>

<p>By construction, BUYs are rare. Of the 39 junior and mid-tier equities we have scored as of
April 2026, five cleared the bar. Those are the companies above. Everything else lands on WATCH
(thesis is interesting but one or more factors need development) or AVOID (a factor is broken in
a way that rarely fixes itself — typically capital structure or management).</p>

<h2>What the BUYs have in common</h2>
<p>Three threads run through the five names:</p>
<ul>
  <li><strong>Management alignment is non-negotiable.</strong> Every BUY scored at least 4/5 on
  management. Franco-Nevada and G2 Goldfields scored 5/5. The framework weights management
  heavily because every other factor is downstream of the people running the company — a strong
  geological asset in the hands of a dilutive or unfocused team produces a worse outcome than a
  modest asset in disciplined hands.</li>
  <li><strong>Catalyst proximity is tight.</strong> Three of the five (Amex, Heliostar, G2) scored
  5/5 on catalyst. That means the next material news event — resource update, drill result, PEA
  completion, permit — is close enough to drive price action inside the next 12 months. The
  framework will not issue a BUY on a company whose next catalyst is more than 18 months out,
  regardless of how strong the other four factors look.</li>
  <li><strong>Jurisdictional clarity.</strong> Four of the five operate in Canada or near-shore
  Americas (Quebec, BC/Newfoundland, Guyana, Mexico). Heliostar is the only one in Mexico and
  Franco-Nevada's royalty book is globally diversified but Canadian-anchored. The framework
  doesn't explicitly penalise jurisdiction, but jurisdictional risk bleeds into the capital and
  catalyst scores via financing access and permit timelines.</li>
</ul>

<h2>How to read a BUY list</h2>
<p>A BUY rating concentrates investor attention on a name. It does not answer the two questions
every position-sizing decision depends on: <em>at what price</em>, and <em>how much</em>. The P/NAV
figures above give one read on the first question — Fury at 0.55x is structurally cheaper than
G2 at 1.87x — but a deep P/NAV discount is not a free lunch. Cheap companies are often cheap
because the market is pricing in a specific concern the framework is scoring generously (a pending
financing, a legal overhang, a project-sequencing problem). Read the individual scorecards, not
just the verdict, before acting on any list of this kind.</p>

<h2>What happens next</h2>
<p>Verdicts are re-scored on every material change. Any of the five names on this list could move
to WATCH next quarter if a catalyst misses, a financing arrives at a punitive structure, or a
management change pulls the alignment factor down. The list is maintained publicly — when a
name is demoted, the old scorecard is archived at a dated URL, and a new scorecard is published.
Nothing gets quietly rewritten. That is the point of keeping the scorecards versioned: the public
track record has to stay honest for the framework to mean anything.</p>
""",
        "faq_items": [
            {
                "question": "What does a BUY verdict on the Verdict Framework mean?",
                "answer": (
                    "A BUY verdict means a company scored 18 or higher out of 25 on the 5-factor "
                    "Verdict Framework with no single factor below 3. The factors are management "
                    "skin-in-the-game, project geology quality, capital structure health, catalyst "
                    "proximity, and comparable acquisition value. A BUY is a framework score, not a "
                    "price target or a specific recommendation to buy at any price."
                ),
            },
            {
                "question": "How often is this list updated?",
                "answer": (
                    "Verdicts are re-scored on every material change — a new drill result, a "
                    "financing, a management change, a catalyst miss. Expect the composition of "
                    "this list to change every quarter as scorecards are published. Dated scorecards "
                    "for each company are preserved as an accountability record."
                ),
            },
            {
                "question": "Why does Franco-Nevada appear on a junior mining list?",
                "answer": (
                    "Franco-Nevada is a royalty and streaming major, not a junior by any reasonable "
                    "definition. It appears on this list because the Verdict Framework is "
                    "tier-agnostic — any gold equity scored on the framework can appear based on "
                    "its composite score. Treat it as the defensive, low-volatility anchor rather "
                    "than a leveraged play."
                ),
            },
            {
                "question": "Is a lower P/NAV always better?",
                "answer": (
                    "No. A low P/NAV (below 0.5x) often signals a structural issue the market is "
                    "pricing in — pending dilution, permit risk, management credibility. The "
                    "framework scores acquisition value on comparable M&amp;A transactions, not "
                    "just the raw P/NAV number. A discounted P/NAV combined with a high composite "
                    "score is the combination to look for."
                ),
            },
            {
                "question": "Do you own positions in the BUY-rated names?",
                "answer": (
                    "Any position held by Mining Stock Report is disclosed on the watchlist at "
                    "miningstockreport.com/watchlist with entry price, target, and stop-loss. "
                    "We do not accept paid coverage or investor-relations contracts and do not "
                    "own positions we have not disclosed."
                ),
            },
        ],
    },
    # ────────────────────────────────────────────────────────────────────
    # Listicle 2 — Top TSX-V Gold Explorers
    # ────────────────────────────────────────────────────────────────────
    {
        "title": "Top TSX-V Gold Explorers Right Now: 10 to Watch in 2026",
        "meta_title": "Top TSX-V Gold Explorers 2026: 10 to Watch",
        "meta_description": (
            "Ten junior gold explorers on the TSX Venture that cleared the 5-factor Verdict "
            "Framework screen, ranked by composite score. Updated April 2026."
        ),
        "pillar_slug": "company-verdicts",
        "excerpt": (
            "Ten junior gold explorers on the TSX Venture exchange that cleared the 5-factor "
            "Verdict Framework screen. Ranked by composite score, from Amex Exploration at 21/25 "
            "down to the tied-at-17 group."
        ),
        "answer_capsule": (
            "The top ten TSX-V junior gold explorers by Verdict Framework score in April 2026 are "
            "Amex Exploration (21/25), Heliostar Metals (20/25), Integra Resources (19/25), "
            "Mako Mining (19/25), Osisko Development (18/25), Banyan Gold (18/25), 1911 Gold (17/25), "
            "Azimut Exploration (17/25), Borealis Mining (17/25), and Cartier Resources (17/25). "
            "All ten scored at least 17/25."
        ),
        "key_takeaways": [
            "The TSX-V remains the densest listing venue for rigorous junior gold exposure",
            "Quebec dominates the jurisdictional mix — four of the top ten operate there",
            "Heliostar is the only producer-developer on the list; the rest are pre-production",
            "Catalyst score of 4/5 or 5/5 is the most common feature across the ten",
            "Composite scores cluster tightly between 17 and 21 — the edge is in the factor mix",
        ],
        "ranked_items": [
            {
                "rank": 1, "name": "Amex Exploration Inc.", "ticker": "TSXV:AMX",
                "company_slug": "amex-exploration-inc",
                "summary": (
                    "21/25. Perron project, Abitibi, Quebec. Geology 5/5 — high-grade, good "
                    "continuity. Catalyst 5/5 — resource update pending. Only BUY-rated explorer "
                    "on this list."
                ),
            },
            {
                "rank": 2, "name": "Heliostar Metals Ltd.", "ticker": "TSXV:HSTR",
                "company_slug": "heliostar-metals-ltd",
                "summary": (
                    "20/25. Mexican producer-developer rather than pure explorer, but listed on "
                    "TSX-V. Producing cash flow funds an active drill program. The only BUY on "
                    "this list alongside Amex."
                ),
            },
            {
                "rank": 3, "name": "Integra Resources Corp.", "ticker": "TSXV:ITR",
                "company_slug": "integra-resources-corp",
                "summary": (
                    "19/25. DeLamar project in Idaho, USA. Strong on management (4/5), capital "
                    "structure (4/5), and acquisition value (4/5). Catalyst 3/5 — PEA/PFS work "
                    "in progress, next milestone measurable but not imminent."
                ),
            },
            {
                "rank": 4, "name": "Mako Mining Corp.", "ticker": "TSXV:MKO",
                "company_slug": "mako-mining-corp",
                "summary": (
                    "19/25. San Albino mine, Nicaragua. Capital structure 5/5 — one of the "
                    "cleanest cap tables among TSX-V gold juniors. Near-term cash-flow visibility "
                    "keeps the catalyst score at 4/5."
                ),
            },
            {
                "rank": 5, "name": "Osisko Development Corp.", "ticker": "TSXV:ODV",
                "company_slug": "osisko-development-corp",
                "summary": (
                    "18/25. Cariboo Gold project in BC. Management 4/5, geology 4/5, catalyst 4/5. "
                    "P/NAV 2.15x — the market is already paying for development progression, so "
                    "upside leverage is muted relative to earlier-stage peers."
                ),
            },
            {
                "rank": 6, "name": "Banyan Gold Corp.", "ticker": "TSXV:BYN",
                "company_slug": "banyan-gold-corp",
                "summary": (
                    "18/25. AurMac project in the Yukon. Capital structure 4/5 and catalyst 4/5. "
                    "Geology scored 3/5 — solid but not standout grades — which is what's holding "
                    "the composite at 18 rather than pushing it to 20+."
                ),
            },
            {
                "rank": 7, "name": "1911 Gold Corporation", "ticker": "TSXV:AUMB",
                "company_slug": "1911-gold-corporation",
                "summary": (
                    "17/25. Rice Lake project, Manitoba. Catalyst score 5/5 — imminent news is the "
                    "standout factor. P/NAV 1.77x reflects market optimism on the upcoming catalyst "
                    "set, with geology and capital both at 3/5 as the check on the composite."
                ),
            },
            {
                "rank": 8, "name": "Azimut Exploration Inc.", "ticker": "TSXV:AZM",
                "company_slug": "azimut-exploration-inc",
                "summary": (
                    "17/25. Multi-project Quebec explorer with a data-driven prospect-generation "
                    "model. Management 4/5 reflects disciplined capital allocation and partner "
                    "funding. Works best as a portfolio-style exposure to Quebec exploration optionality."
                ),
            },
            {
                "rank": 9, "name": "Borealis Mining Company Limited", "ticker": "TSXV:BOGO",
                "company_slug": "borealis-mining-company-limited",
                "summary": (
                    "17/25. Nevada gold project. Management 4/5, catalyst 4/5. P/NAV 0.44x — the "
                    "deepest discount among our TSX-V gold names. The low P/NAV says either the "
                    "market sees a structural issue our framework misses, or there is a real "
                    "opportunity waiting on the next catalyst cycle."
                ),
            },
            {
                "rank": 10, "name": "Cartier Resources Inc.", "ticker": "TSXV:ECR",
                "company_slug": "cartier-resources-inc",
                "summary": (
                    "17/25. Chimo Mine project, Quebec. Acquisition value 4/5 and catalyst 4/5. "
                    "P/NAV of 0.56x puts Cartier among the more discounted names in the top ten. "
                    "Historic high-grade mine with modern targets that have not yet been fully drilled."
                ),
            },
        ],
        "body": """
<h2>Why the TSX Venture still matters for junior gold investors</h2>
<p>The TSX-V is where junior mining capital actually gets formed. It is imperfect — the listing
venue has its share of zombies and low-signal names — but the combination of Canadian disclosure
rules (NI 43-101, SEDI insider filings, continuous disclosure requirements) and genuine retail
liquidity makes it the single most analysable exchange for junior mining equities globally.
Every name on this list files the same quality of technical report and the same insider
transaction summary, which means the Verdict Framework can be applied apples-to-apples.</p>

<p>What the framework can't tell you is which company's management will actually execute. The
scores above are a snapshot of what was true at the last scoring cycle — typically within the
last eight weeks. A strong-management 4/5 score can become a 2/5 after one capital raise done on
punitive terms; a 4/5 catalyst score becomes irrelevant if the catalyst misses. Treat the list as
a high-signal shortlist for your own work, not as a buy list you execute mechanically.</p>

<h2>The jurisdictional tilt</h2>
<p>Four of the top ten operate in Quebec (Amex, Azimut, Cartier, and — via its Newfoundland
portfolio — Fury, if we extended to TSX names). That concentration is not an accident. Quebec
combines premier geological endowment (the Abitibi Greenstone Belt), mature permitting
infrastructure, and provincial flow-through financing benefits that keep junior cap tables
functional through exploration cycles. If we reran this list constrained to Quebec-only
TSX-V names, the top three would be Amex, Azimut, and Cartier.</p>

<p>The remaining six are split between Canadian and international jurisdictions: Banyan in the
Yukon, 1911 in Manitoba, Borealis in Nevada, Integra in Idaho, Mako in Nicaragua, and Osisko
Development in BC. Nevada and Idaho share a USA-friendly permitting backdrop that Canadian
juniors increasingly choose; Mexican and Central American names carry jurisdictional risk the
framework scores but does not eliminate.</p>

<h2>Reading the composite score against the factor breakdown</h2>
<p>The listicle above sorts strictly by composite score. A better way to use the list is to cross-
reference against your own valuation preference. If you care most about balance-sheet health,
start with Mako Mining (capital 5/5). If you want the shortest path to a near-term catalyst,
start with Amex or 1911 Gold (catalyst 5/5). If you weight management alignment heaviest, the
top scorers (all 4/5 on management here) are Amex, 1911 Gold, Azimut, Banyan, Integra, Kenorland,
Minera Alamos, Newcore, and Osisko Development.</p>

<p>None of this replaces reading the underlying scorecards. Each company's dedicated page at
miningstockreport.com/companies/ carries the factor-by-factor breakdown with notes, the latest
analyst summary, and the valuation math. The ten names above cleared the framework screen; what
they do in your portfolio depends on the rest of the work you do before you size a position.</p>

<h2>What gets dropped from the list next</h2>
<p>Scores above 17 are the cutoff for the top ten today. Several names are within one factor
point of cracking into the top ten — Newcore Gold (17/25, Ghana), Minera Alamos (17/25, Nevada),
and Canagold (17/25, BC — TSX rather than TSXV) all sit at the border. A single factor upgrade
on any of them would displace one of the names currently at 17. Expect turnover at the bottom of
this list every quarter.</p>
""",
        "faq_items": [
            {
                "question": "What criteria did you use to select these TSX-V gold explorers?",
                "answer": (
                    "Primary listing on the TSX Venture exchange, gold as primary commodity, and a "
                    "composite score of 17/25 or higher on our 5-factor Verdict Framework. We also "
                    "require at least one published scorecard within the last six months so the "
                    "rating reflects current public filings."
                ),
            },
            {
                "question": "Why is Heliostar Metals on a list of explorers if it's a producer?",
                "answer": (
                    "Heliostar is a producer-developer rather than a pure explorer, but it lists on "
                    "the TSX Venture and runs an active exploration program funded by producing "
                    "cash flow. On an exchange where most names are pre-revenue, Heliostar is a "
                    "structurally different bet — and a stronger one on any factor where balance "
                    "sheet matters."
                ),
            },
            {
                "question": "Does a high catalyst score mean the stock will move soon?",
                "answer": (
                    "A 5/5 catalyst score means the next material public event — drill result, "
                    "resource update, PEA/PFS, permit decision — is within a 12-month window. It "
                    "does not predict direction. A missed catalyst is often more damaging than "
                    "never having one at all, so catalyst-heavy names carry binary event risk."
                ),
            },
            {
                "question": "How does this list differ from your BUY-rated list?",
                "answer": (
                    "The BUY-rated list is a cross-exchange, cross-tier shortlist of companies "
                    "scoring 18/25 or higher with no factor below 3. This list is TSX-V-only and "
                    "uses a composite cut-off of 17/25, so it includes WATCH-rated names with "
                    "strong composite scores where one factor is holding the verdict back."
                ),
            },
            {
                "question": "How often does this list turn over?",
                "answer": (
                    "Expect at least one or two changes per quarter as scorecards are re-issued. "
                    "The bottom of the list (names tied at 17/25) turns over most frequently — a "
                    "single factor upgrade on a bordering name displaces a bottom entry."
                ),
            },
        ],
    },
    # ────────────────────────────────────────────────────────────────────
    # Listicle 3 — P/NAV Discount
    # ────────────────────────────────────────────────────────────────────
    {
        "title": "Junior Gold Developers Ranked by P/NAV: Where the Discount Is Biggest in 2026",
        "meta_title": "Junior Gold P/NAV Rankings 2026: Biggest Discounts",
        "meta_description": (
            "Ten junior gold equities below or near 1x NAV in April 2026. P/NAV rankings with "
            "Verdict Framework scores to separate bargains from structural discounts."
        ),
        "pillar_slug": "investing-guides",
        "excerpt": (
            "Ten junior gold equities trading at or below 1x net asset value in April 2026, "
            "from Borealis Mining at 0.44x to Azimut Exploration at 1.01x. Where structural "
            "discounts meet genuine opportunity."
        ),
        "answer_capsule": (
            "As of April 2026, ten junior gold equities in our coverage universe trade at or "
            "below 1x P/NAV. The deepest discounts are Borealis Mining (0.44x), Fury Gold Mines "
            "(0.55x), Cartier Resources (0.56x), Canagold Resources (0.59x), and Newcore Gold "
            "(0.62x). P/NAV below 0.5x often signals a structural issue the market is pricing "
            "in, not a bargain."
        ),
        "key_takeaways": [
            "P/NAV is the ratio of share price to per-share net asset value from a 43-101 PEA/PFS/FS",
            "A P/NAV below 1.0x means the market is valuing the company below the engineering study",
            "Discounts below 0.5x are usually structural — dilution risk, permit overhang, or financing stress",
            "The best risk-adjusted signal is a low P/NAV combined with a high Verdict Framework composite score",
            "Fury Gold and Amex Exploration are the only BUY-rated names trading below 1x P/NAV",
        ],
        "ranked_items": [
            {
                "rank": 1, "name": "Borealis Mining Company Limited", "ticker": "TSXV:BOGO",
                "company_slug": "borealis-mining-company-limited",
                "summary": (
                    "0.44x P/NAV. Nevada gold project. Composite score 17/25 (WATCH). The deepest "
                    "discount on the list. Geology and acquisition value both score 3/5 — the "
                    "framework sees a respectable asset at a meaningful discount, but not a BUY."
                ),
            },
            {
                "rank": 2, "name": "Fury Gold Mines Limited", "ticker": "TSX:FURY",
                "company_slug": "fury-gold-mines-limited",
                "summary": (
                    "0.55x P/NAV. Quebec and Newfoundland gold portfolio. Composite 20/25 (BUY). "
                    "The most important entry on this list — a BUY-rated name trading at a meaningful "
                    "P/NAV discount. Balance across all five factors is the hallmark."
                ),
            },
            {
                "rank": 3, "name": "Cartier Resources Inc.", "ticker": "TSXV:ECR",
                "company_slug": "cartier-resources-inc",
                "summary": (
                    "0.56x P/NAV. Chimo Mine, Quebec. Composite 17/25 (WATCH). Acquisition value "
                    "4/5 — the framework sees comp transactions supporting a higher valuation than "
                    "the market. Catalyst 4/5 for drill results on historic high-grade targets."
                ),
            },
            {
                "rank": 4, "name": "Canagold Resources Ltd.", "ticker": "TSX:CCM",
                "company_slug": "canagold-resources-ltd",
                "summary": (
                    "0.59x P/NAV. BC gold project. Composite 17/25 (WATCH). Standout geology score "
                    "of 5/5 — the asset itself is top-quartile. Capital structure 2/5 is the weight "
                    "keeping the composite at 17 and likely the discount the market is pricing."
                ),
            },
            {
                "rank": 5, "name": "Newcore Gold Ltd.", "ticker": "TSXV:NCAU",
                "company_slug": "newcore-gold-ltd",
                "summary": (
                    "0.62x P/NAV. Enchi project, Ghana. Composite 17/25 (WATCH). Management 4/5 and "
                    "catalyst 4/5. Jurisdictional risk discount is visible in the P/NAV — Ghana is "
                    "not Quebec, and the framework does not explicitly score country but the market does."
                ),
            },
            {
                "rank": 6, "name": "Amex Exploration Inc.", "ticker": "TSXV:AMX",
                "company_slug": "amex-exploration-inc",
                "summary": (
                    "0.64x P/NAV. Perron project, Quebec. Composite 21/25 (BUY). The highest-scoring "
                    "name on this list and the second-highest composite overall — trading below "
                    "P/NAV despite a BUY verdict. The cleanest combination of quality-at-a-discount "
                    "on the list."
                ),
            },
            {
                "rank": 7, "name": "Equinox Gold Corp.", "ticker": "TSX:EQX",
                "company_slug": "equinox-gold-corp",
                "summary": (
                    "0.64x P/NAV. Mid-tier producer operating across the Americas. Composite 19/25 "
                    "(WATCH). Geology 5/5. The only mid-tier on this list — P/NAV discount at this "
                    "tier usually reflects operational-risk concerns (mine-level cost inflation, "
                    "jurisdictional mix) rather than junior-stage dilution."
                ),
            },
            {
                "rank": 8, "name": "GoldMining Inc.", "ticker": "TSX:GOLD",
                "company_slug": "goldmining-inc",
                "summary": (
                    "0.78x P/NAV. Brazil-focused portfolio. Composite 15/25 (WATCH). Classic "
                    "deep-value resource holding company — a basket of in-ground ounces rather than "
                    "a single-project story. Catalyst 3/5 reflects the lack of near-term single-asset "
                    "milestone."
                ),
            },
            {
                "rank": 9, "name": "Snowline Gold Corp.", "ticker": "TSX:SGD",
                "company_slug": "snowline-gold-corp",
                "summary": (
                    "0.89x P/NAV. Valley project, Yukon. Composite 19/25 (WATCH). Balanced 4-across "
                    "the factor mix with the exception of acquisition value (3/5). The P/NAV discount "
                    "is narrower than most on this list, which is a reasonable read on the "
                    "market's positive view of the asset."
                ),
            },
            {
                "rank": 10, "name": "Azimut Exploration Inc.", "ticker": "TSXV:AZM",
                "company_slug": "azimut-exploration-inc",
                "summary": (
                    "1.01x P/NAV. Multi-project Quebec prospect generator. Composite 17/25 (WATCH). "
                    "Trading essentially at NAV — no discount, no premium. The framework sees a "
                    "business model (partner-funded exploration) the market is valuing fairly."
                ),
            },
        ],
        "body": """
<h2>What P/NAV measures, and what it doesn't</h2>
<p>P/NAV — Price to Net Asset Value — is the ratio of the current share price to the per-share
net asset value derived from a company's most recent technical study (typically a PEA, PFS, or
feasibility study under the NI 43-101 standard). The NAV is the discounted after-tax cash flow of
the project at a specified gold price and discount rate, divided by fully-diluted shares
outstanding. A P/NAV of 1.0x means the market is paying exactly what the engineering study says
the asset is worth. Below 1.0x, the market is paying less. Above 1.0x, it is paying for expected
upside not captured in the study.</p>

<p>The metric has three well-known weaknesses. First, the NAV depends on the commodity price
assumption in the study — a study run at $2,100/oz gold will produce a different NAV than a study
run at $3,500/oz on the same project. Second, the discount rate assumption (usually 5% for a
producer, 8–10% for a developer) materially moves the output. Third, many juniors have no study
yet, which is why this list is ten names long instead of fifty. Use P/NAV as one input, not the
answer.</p>

<h2>Why low P/NAV is usually not the whole story</h2>
<p>The most discounted names on this list — Borealis at 0.44x, Fury at 0.55x, Cartier at 0.56x —
are discounted for discernible reasons. Borealis has scored well on our framework but sits in a
Nevada exploration setting where the market is waiting on a specific catalyst sequence before
re-rating. Cartier has a historic high-grade mine with modern drill targets not yet proven out.
Fury's discount is the most interesting because the composite score (20/25, BUY) says the
framework sees no structural issue — which either means the framework is wrong about a weakness
it's missing, or the market is wrong about discounting a balanced BUY. Those are the two
scenarios where P/NAV discounts become thesis-relevant.</p>

<p>Amex Exploration is the other entry worth flagging. At 0.64x and a composite of 21/25 (tied
for the highest score in our universe), it combines the cleanest factor mix with a double-digit
percent discount to engineering-study NAV. The near-term catalyst — resource update — is the
obvious trigger for a re-rating toward 1.0x or above. Whether that arrives in a quarter or a year
determines the IRR on the idea.</p>

<h2>How to combine P/NAV with the Verdict Framework</h2>
<p>The interaction matrix worth drawing:</p>
<ul>
  <li><strong>High composite + low P/NAV</strong> — the best setup. Two names on this list sit here:
  Amex and Fury. The framework sees quality; the market is paying a discount. Your job is to decide
  whether the market knows something the framework doesn't.</li>
  <li><strong>Medium composite + low P/NAV</strong> — the cautious entry point. Most of this list.
  The discount is real, the quality is acceptable but not exceptional, and the re-rating path
  requires a specific factor improvement (typically catalyst execution).</li>
  <li><strong>Low composite + low P/NAV</strong> — usually a value trap. A company with a 12/25
  composite trading at 0.4x P/NAV is cheap because one or more factors are broken. Without a
  specific thesis on why those factors will repair, the discount persists.</li>
  <li><strong>High composite + high P/NAV</strong> — the quality premium. G2 Goldfields at 1.87x
  and Osisko Development at 2.15x fall here. Upside requires positive catalyst delivery; any
  disappointment re-rates back to 1.0x quickly.</li>
</ul>

<h2>What this list does not include</h2>
<p>Several companies in our coverage universe have no P/NAV because they have no PEA or later-stage
study yet. Pre-PEA explorers can be exceptional investments — Snowline was one until its Valley
discovery work warranted a study — but they don't have a P/NAV input for this ranking. The
framework scores them on geology, management, capital, and catalyst; acquisition value is scored
on comp transactions rather than per-share NAV math.</p>

<p>Every company named above has a full scorecard at miningstockreport.com/companies/ with the
factor-by-factor breakdown and the current analyst summary. The P/NAV figures in this list
reflect the most recent scoring pass. NAV inputs are sensitive to commodity-price assumptions;
re-run the math against your own price deck before acting on any specific P/NAV number.</p>
""",
        "faq_items": [
            {
                "question": "What is P/NAV and how is it calculated?",
                "answer": (
                    "P/NAV is Price to Net Asset Value — the ratio of the current share price to "
                    "the per-share after-tax net present value of the company's flagship project "
                    "from its most recent NI 43-101 technical study (PEA, PFS, or FS). The NAV "
                    "depends on the commodity price and discount rate assumptions in the study."
                ),
            },
            {
                "question": "Is a P/NAV below 1.0x always a buy signal?",
                "answer": (
                    "No. Companies trade below 1.0x P/NAV for many reasons — pending dilution, "
                    "jurisdictional risk, permit overhang, management credibility concerns. The "
                    "discount reflects what the market sees that the engineering study doesn't "
                    "capture. Combine P/NAV with the 5-factor Verdict Framework score for a more "
                    "complete read."
                ),
            },
            {
                "question": "Why don't you include pre-PEA explorers on this list?",
                "answer": (
                    "Companies without a PEA or later-stage study don't have a published per-share "
                    "NAV, so no P/NAV can be calculated. Many pre-PEA explorers are excellent "
                    "investments — they just can't be ranked on this specific metric. See our "
                    "separate list of top TSX-V gold explorers for that universe."
                ),
            },
            {
                "question": "What gold price is assumed in these NAV figures?",
                "answer": (
                    "Each study uses a different assumption, typically a three-year trailing "
                    "average that lags the current price. Some assume $2,100–$2,300/oz, more "
                    "recent studies use $2,800–$3,200/oz. Always check the specific commodity-"
                    "price deck in the underlying 43-101 before comparing P/NAV figures across "
                    "companies."
                ),
            },
            {
                "question": "How does P/NAV differ from P/E for mining stocks?",
                "answer": (
                    "P/E is a standard earnings multiple, which is only useful for producers "
                    "generating current earnings. Developers and explorers have no earnings, so "
                    "P/NAV is the equivalent anchor metric — using future cash flow from the "
                    "technical study instead of current earnings. Producers can be evaluated on "
                    "both; developers and explorers really only on P/NAV."
                ),
            },
        ],
    },
    # ────────────────────────────────────────────────────────────────────
    # Listicle 4 — Copper
    # ────────────────────────────────────────────────────────────────────
    {
        "title": "Best Copper Mining Stocks for 2026: What the Verdict Framework Says",
        "meta_title": "Best Copper Mining Stocks 2026: Verdict Framework",
        "meta_description": (
            "Three copper-primary equities scored on our 5-factor Verdict Framework: Western "
            "Copper, NorthIsle Copper and Gold, and Max Resource. April 2026."
        ),
        "pillar_slug": "company-verdicts",
        "excerpt": (
            "Three copper-primary equities have been scored on the Verdict Framework as of April "
            "2026: Western Copper and Gold (19/25, WATCH), NorthIsle Copper and Gold (15/25, "
            "WATCH), and Max Resource Corp. (11/25, AVOID). Our copper coverage is lighter than "
            "our gold coverage — here's what we've seen so far, and where it's going next."
        ),
        "answer_capsule": (
            "Three copper-primary equities on our coverage list as of April 2026: Western Copper "
            "and Gold (19/25, WATCH) with the Casino project in the Yukon; NorthIsle Copper and "
            "Gold (15/25, WATCH) on Vancouver Island, BC; and Max Resource Corp. (11/25, AVOID) in "
            "Colombia. Coverage will expand through 2026 — this is the early read."
        ),
        "key_takeaways": [
            "Only three copper-primary equities have been scored — expect coverage to expand",
            "Western Copper's Casino project is the standout (19/25) on geology alone (5/5)",
            "Jurisdiction matters more for copper than for gold — capex is bigger, timeline is longer",
            "A BUY-rated copper name does not yet exist in our coverage as of April 2026",
            "Copper-adjacent names (gold-copper polymetallic) are scored under gold-primary listicles",
        ],
        "ranked_items": [
            {
                "rank": 1, "name": "Western Copper and Gold Corporation", "ticker": "TSX:WRN",
                "company_slug": "western-copper-and-gold-corporation",
                "summary": (
                    "Composite 19/25 (WATCH). The Casino project in the Yukon is one of North "
                    "America's largest undeveloped copper-gold-molybdenum deposits. Geology scores "
                    "a perfect 5/5 — the asset itself is world-class. Capital 4/5 and acquisition "
                    "value 4/5. Catalyst 3/5 — permit advancement is the rate-limiting step, not "
                    "a near-term drill cycle."
                ),
            },
            {
                "rank": 2, "name": "NorthIsle Copper and Gold Inc.", "ticker": "TSXV:NCX",
                "company_slug": "northisle-copper-and-gold-inc",
                "summary": (
                    "Composite 15/25 (WATCH). North Island project on Vancouver Island, BC. "
                    "Geology 3/5 — respectable but not standout. Capital structure 4/5 is the "
                    "factor strength. P/NAV 1.17x signals the market is paying roughly fair value "
                    "against the engineering study."
                ),
            },
            {
                "rank": 3, "name": "Max Resource Corp.", "ticker": "TSXV:MAX",
                "company_slug": "max-resource-corp",
                "summary": (
                    "Composite 11/25 (AVOID). CESAR copper project in northeastern Colombia. "
                    "Geology 2/5, management 2/5. The AVOID verdict reflects concerns on multiple "
                    "factors, not a single-factor failure. Included here because the framework is "
                    "not selective — every scored copper name appears in a copper listicle, "
                    "regardless of the verdict."
                ),
            },
        ],
        "body": """
<h2>Why our copper coverage is lighter than our gold coverage</h2>
<p>Mining Stock Report began with gold coverage for a defensible reason: gold juniors are
over-served by promotional research and under-served by rigorous analysis, and the Verdict
Framework was built to fill that gap. Copper has the opposite problem — the major equities
(Freeport, Southern Copper, First Quantum, Antofagasta) are covered by every sell-side desk, and
the juniors get less retail attention because copper projects require larger capex and longer
timelines to production than comparable gold projects.</p>

<p>That said, copper is a different kind of exposure than gold and the two should not be conflated.
Gold is a monetary commodity; copper is an industrial one. Gold prices respond to real rates,
central-bank buying, and safe-haven demand; copper responds to manufacturing PMI, EV and grid
buildout demand, and supply-side disruptions (Chilean water rights, African political stability,
Indonesian export policy). Having copper exposure alongside gold exposure is a portfolio
construction decision, not just a commodity substitution.</p>

<h2>The three copper names we have scored so far</h2>
<p>Only three companies in our coverage universe list copper as the primary commodity in their
filings — and one of them (Max Resource) carries an AVOID verdict. That is an honest read on where
our coverage currently stands. We do not publish filler listicles to bulk out a category; if we
have scored three names, we say three names.</p>

<p><strong>Western Copper and Gold</strong> is the one to study. The Casino project in the Yukon
hosts a resource measured in billions of pounds of copper, supported by gold and molybdenum
credits that turn the economics attractive even at mid-cycle copper prices. The framework scored
geology a full 5/5 — a rare outcome — and acquisition value 4/5 based on comparable transactions
in Canadian copper-gold porphyry assets. The composite of 19/25 missed a BUY verdict because the
catalyst score (3/5) reflects a permitting timeline measured in years, not quarters. That is
precisely the copper-specific pattern: the asset is the thesis, the catalyst is patience.</p>

<p><strong>NorthIsle Copper and Gold</strong> sits lower on the composite (15/25) because the
project is earlier-stage and the geology score reflects that. The factor strength is the capital
structure (4/5) — NorthIsle has managed its share count carefully through exploration cycles.
The P/NAV of 1.17x suggests the market has accepted the engineering study's NAV as a fair
starting point; upside requires resource expansion or grade uplift on the continuing drill
program.</p>

<p><strong>Max Resource</strong> is included in this list for completeness, not as a recommendation.
The AVOID verdict is grounded in the framework's factor scoring — geology 2/5, management 2/5.
A detailed reading is in the dedicated scorecard. A speculator may have a specific reason to look
past the framework's concerns; the framework itself does not.</p>

<h2>Copper-adjacent names we have scored elsewhere</h2>
<p>Several gold-primary companies carry meaningful copper exposure through polymetallic
gold-copper assets — Equinox Gold, for instance, produces copper at some of its operations as a
byproduct; Collective Mining's work in Colombia spans gold-silver-copper polymetallic targets.
Those names are scored in our gold-primary universe because their primary commodity filing
declares gold, but investors specifically building copper exposure should cross-reference the
individual scorecards. A BUY-rated polymetallic gold-copper name can sometimes deliver more
copper exposure per invested dollar than a middling copper-primary WATCH.</p>

<h2>What's next for our copper coverage</h2>
<p>Expect coverage expansion through mid-2026. Candidate names already in the research queue
include select copper-gold porphyry developers in the Americas and at least one copper-primary
name in a jurisdiction we have not yet covered. Scorecards are published as the work is
completed — no pre-announcement of who's next.</p>
""",
        "faq_items": [
            {
                "question": "Why is your copper coverage smaller than your gold coverage?",
                "answer": (
                    "Our framework was built first for gold juniors, where promotional research is "
                    "dense and rigorous analysis is thin. Copper juniors get less retail attention "
                    "and are less promotional, so the audience need is different. We are expanding "
                    "copper coverage through 2026 but will not publish filler scorecards to bulk "
                    "out the category."
                ),
            },
            {
                "question": "Is there a BUY-rated copper stock on your coverage list?",
                "answer": (
                    "Not as of April 2026. The highest-scoring copper name is Western Copper and "
                    "Gold at 19/25 (WATCH). The catalyst score of 3/5 — reflecting a multi-year "
                    "permitting timeline rather than near-term news — is what's holding the "
                    "composite short of a BUY."
                ),
            },
            {
                "question": "How should a gold-focused investor think about copper exposure?",
                "answer": (
                    "Gold and copper respond to different macro drivers. Gold moves on real rates, "
                    "central-bank buying, and safe-haven demand; copper responds to manufacturing "
                    "activity, EV and grid buildout demand, and supply-side disruptions. Copper "
                    "exposure is a portfolio construction decision, not a commodity substitution."
                ),
            },
            {
                "question": "Why is Max Resource on the list if it's AVOID-rated?",
                "answer": (
                    "The Verdict Framework is not selective — every copper-primary name we have "
                    "scored is included in a copper listicle regardless of verdict. Readers "
                    "weighing a speculation on Max Resource deserve to see where the framework "
                    "sees factor weakness, not just a curated list of names we like."
                ),
            },
            {
                "question": "Do you score gold-copper polymetallic names as copper?",
                "answer": (
                    "No. We use the company's self-declared primary commodity from their filings. "
                    "A gold-copper porphyry developer that lists gold as primary appears on our "
                    "gold coverage; a company that lists copper appears here. Cross-reference "
                    "individual scorecards if you want specific copper-byproduct exposure."
                ),
            },
        ],
    },
    # ────────────────────────────────────────────────────────────────────
    # Listicle 5 — AVOID
    # ────────────────────────────────────────────────────────────────────
    {
        "title": "Mining Stocks to Avoid in 2026: What the AVOID Verdicts Tell Investors",
        "meta_title": "Mining Stocks to Avoid 2026: Verdict Framework Analysis",
        "meta_description": (
            "Six mining equities got an AVOID verdict on our 5-factor Verdict Framework in April "
            "2026. What the framework sees, and what it doesn't."
        ),
        "pillar_slug": "company-verdicts",
        "excerpt": (
            "Six mining equities received an AVOID verdict on our Verdict Framework in April 2026. "
            "This is a framework-based read — a company can fail the scorecard on structural "
            "reasons while still delivering returns for a speculator. Here's what the framework sees."
        ),
        "answer_capsule": (
            "As of April 2026, six companies on our coverage list carry an AVOID verdict: Belmont "
            "Resources (8/25), Enduro Metals (9/25), Precipitate Gold (9/25), Max Resource (11/25), "
            "Crossroads Gold (12/25), and Nevada King Gold (12/25). An AVOID is a framework score "
            "— based strictly on how a company measures on management, geology, capital structure, "
            "catalyst, and acquisition value — not a prediction of future price action."
        ),
        "key_takeaways": [
            "An AVOID verdict means a composite score below 13/25 or a factor score of 1 on management or capital",
            "The framework scores public filings — it does not predict share price or trader outcomes",
            "Five of six AVOIDs are held back by weak geology (1–2/5) combined with other factors",
            "Four of six operate outside Canada, which correlates with but does not cause the AVOID",
            "A company can move off the AVOID list via a financing, management change, or new technical study",
        ],
        "ranked_items": [
            {
                "rank": 1, "name": "Belmont Resources Inc.", "ticker": "TSXV:BEA",
                "company_slug": "belmont-resources-inc",
                "summary": (
                    "Composite 8/25 (AVOID). The lowest-scoring company in our coverage universe. "
                    "Geology 1/5 and acquisition value 1/5 — the framework sees neither asset "
                    "quality nor comparable-transaction support. Management 2/5 and capital 2/5. "
                    "Re-rating would require a material change in project scope, not an incremental "
                    "improvement."
                ),
            },
            {
                "rank": 2, "name": "Enduro Metals Corporation", "ticker": "TSXV:ENDR",
                "company_slug": "enduro-metals-corporation",
                "summary": (
                    "Composite 9/25 (AVOID). British Columbia. Geology 1/5 is the primary drag. "
                    "Capital 2/5 and management 2/5 reinforce the pattern. The framework does "
                    "not see a clear path to a re-rating without a new discovery or a project pivot."
                ),
            },
            {
                "rank": 3, "name": "Precipitate Gold Corp.", "ticker": "TSXV:PRG",
                "company_slug": "precipitate-gold-corp",
                "summary": (
                    "Composite 9/25 (AVOID). Dominican Republic. Geology 1/5 and acquisition value "
                    "1/5. Catalyst 3/5 — drill programs continue — but the underlying resource "
                    "quality is the constraint. A new discovery could change the framework read "
                    "quickly; incremental infill drilling cannot."
                ),
            },
            {
                "rank": 4, "name": "Max Resource Corp.", "ticker": "TSXV:MAX",
                "company_slug": "max-resource-corp",
                "summary": (
                    "Composite 11/25 (AVOID). CESAR copper project, Colombia. Geology 2/5, management "
                    "2/5. The highest-scoring AVOID in our universe — closer to the bottom of "
                    "WATCH than to the bottom of AVOID. A financing on improved terms or a "
                    "resource-estimate upgrade could push it to WATCH."
                ),
            },
            {
                "rank": 5, "name": "Crossroads Gold Corp.", "ticker": "TSXV:CRG",
                "company_slug": "crossroads-gold-corp",
                "summary": (
                    "Composite 12/25 (AVOID). Victoria, Australia. Geology 1/5 and acquisition value "
                    "1/5. Management 4/5 is the standout — the framework rates the team well but the "
                    "project the team is working on scored weakly. A project pivot or new ground "
                    "acquisition is the most plausible path to a re-rating."
                ),
            },
            {
                "rank": 6, "name": "Nevada King Gold Corp.", "ticker": "TSXV:NKG",
                "company_slug": "nevada-king-gold-corp",
                "summary": (
                    "Composite 12/25 (AVOID). Nevada, USA. Management 4/5 — insider alignment is "
                    "in place. Geology 2/5 and acquisition value 1/5 are the drags. The Atlanta "
                    "project continues drilling; the framework will update the score on each "
                    "material resource disclosure."
                ),
            },
        ],
        "body": """
<h2>Important framing for this list</h2>
<p>An AVOID verdict on the Verdict Framework is a strict, structured read on how a company scores
across five factors at the time of the last scorecard. It is not a prediction of future share
price. It is not a commentary on any individual's character or effort. It is not a recommendation
to short the company. It is a framework output, nothing more.</p>

<p>The framework can be wrong. A speculator with a specific, time-bound thesis — a pending
acquisition rumor, a technical rebound setup, a catalyst the framework is under-scoring — can
absolutely make money on an AVOID-rated name. What the framework can't do is endorse that
speculation; the framework only reports what the public filings and comparable transactions say
about the factor mix. When those improve, the verdict improves.</p>

<h2>Why a company lands in AVOID</h2>
<p>An AVOID verdict has two triggers. The first is a composite score below 13 out of 25 — roughly,
when the average factor score drops below 2.6. The second is a single-factor score of 1 on either
management or capital structure, regardless of composite. Those two factors are weighted more
heavily because they are the ones that rarely self-repair: a broken management team doesn't fix
itself, and a broken cap table (excessive dilution, unmanageable warrant overhang) tends to get
worse, not better, as a company continues to need capital.</p>

<p>Looking at the six names on this list, four of the six have a factor score of 1 somewhere in
the mix. The other two (Max Resource at 11/25 and Nevada King at 12/25) land on AVOID via the
composite-score route — no single factor is at 1, but the overall mix averages below the threshold.
Nevada King is particularly instructive: its management score of 4/5 is as high as many BUY-rated
companies, but the geology (2/5) and acquisition value (1/5) scores pull the composite down.</p>

<h2>What could move a company off the AVOID list</h2>
<p>The framework updates on any material change. Concretely, these are the most common mechanisms
by which an AVOID-rated company can re-score to WATCH:</p>
<ul>
  <li><strong>A financing on improved terms.</strong> If a company with a capital-structure score
  of 2/5 closes a raise without warrants or at a shallower discount to VWAP than prior raises, the
  capital factor can move to 3/5. That alone can cross the composite threshold.</li>
  <li><strong>A management change or material insider alignment event.</strong> A new CEO with a
  track record, a large insider open-market purchase, or a refreshed board can move the management
  score up a point. Watch SEDI for the triggering filing.</li>
  <li><strong>A new discovery or resource upgrade.</strong> The geology factor is the hardest to
  move — it reflects the rocks in the ground — but a genuinely new discovery or a resource
  reclassification from inferred to indicated can shift the score.</li>
  <li><strong>A material change in comparable transactions.</strong> When the M&amp;A comps set
  changes — a new buyer enters the market, a new commodity-price regime re-prices deals — the
  acquisition-value factor can move on every name without any action by the company itself.</li>
</ul>

<h2>What AVOID does not mean</h2>
<p>It does not mean we believe the company will go to zero. Several of the names on this list have
delivered sharp rallies on specific catalysts that the framework did not anticipate. The framework
is a screening tool, not an omniscient judge.</p>

<p>It also does not mean the people running the company are doing anything wrong. Framework scores
reflect what public filings say — a company can have an excellent, ethical management team
executing correctly on a weak asset. The management factor captures alignment and track record,
not character. Several AVOID-rated companies have management scores of 4/5.</p>

<h2>How to use this list</h2>
<p>The most honest use is as a red-flag list when researching sector-adjacent names. If you are
looking at a new TSX-V gold or copper junior and you are about to build a position, check whether
it shares factor weaknesses with any name on this list. Common patterns — a 43-101 that skimps on
metallurgy, a cap table with multiple warrant tranches, a management team with prior unsuccessful
ventures — are cheaper to learn from an AVOID list than from your own losses.</p>

<p>The individual scorecards for each of these companies are published at
miningstockreport.com/companies/ with the factor-by-factor notes. Read them when you want the
reasoning, not just the verdict.</p>
""",
        "faq_items": [
            {
                "question": "What does an AVOID verdict mean on the Verdict Framework?",
                "answer": (
                    "An AVOID means a company scored below 13/25 on our 5-factor framework, or "
                    "scored a 1 on either the management or capital structure factor. It is a "
                    "framework-based read on public filings and comparable transactions — not a "
                    "prediction of share price, and not a recommendation to short the company."
                ),
            },
            {
                "question": "Can an AVOID-rated stock still go up?",
                "answer": (
                    "Yes. Short-term price action is driven by many factors the framework does not "
                    "score — technical setups, sector-wide moves, unexpected M&amp;A rumors, "
                    "catalyst surprises. The framework screens for structural factors that tend "
                    "to persist over quarters, not weekly price movements."
                ),
            },
            {
                "question": "How does a company get off the AVOID list?",
                "answer": (
                    "The most common mechanisms are a financing on improved terms (lifts the "
                    "capital score), a management change or material insider buying (lifts the "
                    "management score), a new discovery or resource upgrade (lifts the geology "
                    "score), or a change in the comparable-transaction set (lifts the acquisition "
                    "value score)."
                ),
            },
            {
                "question": "Are you saying these companies are fraudulent?",
                "answer": (
                    "Absolutely not. The Verdict Framework scores public filings against a rubric. "
                    "Several AVOID-rated companies have strong management teams with clean track "
                    "records — they are simply working on projects that score weakly on geology "
                    "or acquisition value. The framework measures fit, not integrity."
                ),
            },
            {
                "question": "Does the AVOID list get updated?",
                "answer": (
                    "Yes — every time a new scorecard is published for any of these companies, "
                    "their verdict is re-issued. Expect composition changes as drill results, "
                    "financings, and management developments move scores up or down. Historical "
                    "scorecards are archived at dated URLs as a public accountability record."
                ),
            },
        ],
    },
]


def seed_listicles(apps, schema_editor):
    # Import live models so custom save() logic (word_count computation) runs.
    from apps.blog.models import Post, Pillar
    from apps.accounts.models import User

    try:
        author = User.objects.get(username="chaugen")
    except User.DoesNotExist:
        return  # Author must exist before seeding; skip gracefully otherwise.

    now = timezone.now()
    # First listicle goes live tomorrow at 10:00 UTC; each subsequent one +1 day.
    start = (now + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)

    for i, data in enumerate(LISTICLES):
        pillar = Pillar.objects.filter(slug=data["pillar_slug"]).first()
        if Post.objects.filter(title=data["title"]).exists():
            continue  # Idempotent — don't duplicate on re-run.
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
    titles = [d["title"] for d in LISTICLES]
    Post.objects.filter(title__in=titles).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0008_seed_pillar_intros"),
    ]
    operations = [
        migrations.RunPython(seed_listicles, reverse_seed),
    ]
