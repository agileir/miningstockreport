"""
Seed a long-form silver investor guide. Comprehensive reference piece, not
a listicle. post_type="guide" so the TOC sidebar populates from the H2s.

Publish date 2026-05-20 (a week after the copper guide). Adjust in admin
or via shell if earlier publication is desired.
"""
from datetime import datetime, timezone as dt_timezone
from django.db import migrations


SILVER_GUIDE_BODY = """
<p>Silver is not just cheap gold. The two metals are grouped together in most retail investor
conversations, held in the same ETF categories, and discussed under the same "precious metals"
umbrella — but the macro drivers, the investment vehicles, and the risk profiles genuinely
differ. A reader who understands why they differ, and sizes their silver allocation
accordingly, ends up with a precious-metals portfolio that behaves better across cycles than
one that treats silver as a gold proxy.</p>

<p>This guide walks through silver as an investment in 2026: the market as it sits, the
commodity dynamics driving prices, the different ways to take exposure, how we apply the
5-factor Verdict Framework to silver mining equities, and how to size a silver allocation
within a broader precious-metals sleeve. It is long-form reference material rather than a
ranked list. Read it end-to-end, or use the in-page navigation to jump to the section that
matters most for the decision you are about to make.</p>

<h2 id="why-silver-is-different">Why Silver Is Not Just Cheap Gold</h2>

<p>Gold is primarily a monetary asset. Its price responds most strongly to real interest rates,
central-bank reserve flows, and safe-haven demand during financial-system stress. Industrial
uses of gold — electronics, medical, dentistry — account for roughly 8% of annual demand, so
industrial cycles barely move the gold price.</p>

<p>Silver is both. Roughly half of annual silver demand is industrial: photovoltaic solar
cells, electrical contacts in electric vehicles and electronics, medical applications,
antibacterial coatings. The other half is monetary and ornamental: bullion, coins, ETFs, and
jewelry. That dual composition means silver responds to two separate sets of news flow. A
strong monthly Chinese manufacturing PMI print is irrelevant to gold but genuinely moves silver.
A sovereign central-bank reserve announcement that re-rates gold may not touch silver.</p>

<p>The practical consequence for portfolio construction: silver and gold are complements, not
substitutes. Holding both is diversification across different macro exposures. Holding only
silver because "it has more upside" misses the asymmetry of the two monetary layers. Holding
only gold because "it is less volatile" misses the industrial thesis that has been the
structural demand story of the past five years.</p>

<h3 id="the-volatility-gap">The Volatility Gap</h3>

<p>Silver is structurally more volatile than gold. On monthly returns over the past thirty
years, silver's standard deviation is roughly 1.5 to 2 times gold's. Upside beta during
gold-positive cycles is typically higher for silver; downside beta during corrections is also
higher. This "silver gives leverage to the gold price" framing is broadly true but incomplete —
the leverage is asymmetric, with the industrial demand layer adding or subtracting from the
monetary beta depending on the cycle.</p>

<p>For position-sizing purposes: if your gold positions are sized at 3% of portfolio each,
equivalent-risk silver positions should typically sit at 2% each. The volatility differential
is real, and not accounting for it is how investors end up with de facto silver-heavy
allocations they did not consciously choose.</p>

<h2 id="market-dynamics">The Silver Market: Supply, Demand, and the Deficit Era</h2>

<p>Global silver supply runs at roughly 1,000 million ounces per year — 825 million from mine
production and another 175 million from recycling. Demand, over the past four years, has been
running higher. The deficit has been persistent enough — 2021, 2022, 2023, and 2024 all
printed supply deficits — that it has become the central narrative of the current cycle.
Above-ground stocks have been drawn down to meet the shortfall, which cannot continue
indefinitely.</p>

<h3 id="supply-side">Supply: Where Silver Actually Comes From</h3>

<p>The top silver-producing countries in 2026, in approximate rank order: Mexico at roughly
6,300 tonnes per year, followed by China, Peru, Poland, Chile, Australia, Russia, Bolivia, and
Argentina. Mexico's dominance is the defining feature of silver supply — a single
jurisdiction produces about 24% of global mine output. That concentration drives both the
opportunity (Mexican silver producers are plentiful and investable) and the risk (jurisdictional
policy shifts in Mexico can materially move global supply).</p>

<p>A structural nuance of silver supply that often gets missed: roughly 70% of mine silver
production comes as a byproduct of lead, zinc, copper, or gold mining, not from primary silver
mines. This means silver mine output responds to demand for other metals as much as to silver
prices. Lead-zinc mines run full-out during construction cycles regardless of where the silver
price sits; gold mines with silver credits produce silver as a function of gold economics.
Primary silver mines — where silver is the main revenue source — make up about 30% of global
supply and are where silver-price elasticity actually lives.</p>

<p>Recycling contributes a meaningful ~17% of total supply. Unlike gold, where recycled
jewelry and bars dominate the secondary supply, silver recycling is concentrated in
industrial recovery — electronic waste, spent catalysts, photovoltaic panel end-of-life, and
medical imaging. Recycling volumes respond to price with a lag and are more sensitive to the
industrial-collection economics than to spot silver.</p>

<h3 id="demand-side">Demand: The Photovoltaic Revolution</h3>

<p>Silver demand breaks down into four categories. Industrial demand accounts for roughly 55%
of annual consumption. Within industrial, photovoltaic solar cells have grown from a minor
use case in the early 2010s to the single largest industrial silver application in 2025-2026 —
roughly 200 million ounces per year of silver are now embedded in new solar panel production.
The electrical-vehicle transition is a smaller but growing component, with silver content in
EV electronics, battery management systems, and high-voltage contacts.</p>

<p>Jewelry demand accounts for roughly 20% of annual consumption, anchored by India and China
as the largest markets. Silver jewelry demand has been remarkably stable over decades,
responding less to price than gold jewelry does — silver is affordable enough that price is
not the primary constraint on purchasing decisions.</p>

<p>Investment demand — bullion bars, coins, and silver ETF holdings — accounts for roughly 20%
of annual demand, with meaningful variability year-to-year. This is the most volatile demand
component and the most sensitive to macro sentiment. A year of strong risk-off sentiment can
add 50-80 million ounces to investment demand; a year of equity-market exuberance can
subtract the same amount.</p>

<p>The residual 5% covers photography (declining but still real in medical and aerospace
film), silverware, and miscellaneous applications.</p>

<h3 id="deficit-math">What the Deficit Means (and What It Doesn't)</h3>

<p>A supply deficit sounds dramatic but the mechanics deserve precision. A 150-200 million-
ounce annual deficit is drawn from above-ground stocks — warehouse inventories at the LBMA,
CME COMEX depositories, unallocated holdings at banks, and unreported private hoards. Those
stocks have been drawn down but are not zero. Silver is not going to run out next year because
of the deficit; what the deficit does is put continuous upward pressure on the price until the
economics re-balance supply and demand.</p>

<p>Re-balancing can happen from either side. Supply can respond: primary silver mines can
restart, byproduct silver from other metal mines can increase. Demand can moderate: if the
silver price rises enough, solar-panel manufacturers will thrift silver content through
metallization-efficiency gains, industrial users will substitute where possible, and investment
demand may pull back from higher prices. The current cycle's price trajectory will be
determined by which response happens first.</p>

<h2 id="price-drivers">What Actually Moves Silver Prices</h2>

<p>Five variables dominate silver-price dynamics, and separating them helps a reader interpret
news flow appropriately.</p>

<h3 id="real-rates-usd">Real Interest Rates and the US Dollar</h3>

<p>Silver, like gold, responds to real interest rates and dollar direction. A rising real-rate
environment puts downward pressure on both metals; a weakening dollar puts upward pressure.
The mechanism is the same as for gold — neither metal pays a coupon, so the opportunity cost
of holding them rises and falls with real yields. Silver's response magnitude tends to be
larger than gold's, both up and down, due to its higher base volatility.</p>

<h3 id="industrial-activity">Industrial Activity and Chinese PMI</h3>

<p>Chinese manufacturing PMI is the single most predictive short-cycle indicator for silver
prices. When Chinese industrial activity accelerates, silver demand from electronics,
photovoltaic manufacturing, and industrial applications rises. A trailing-three-month PMI
above 52 typically correlates with silver outperformance versus gold; a reading below 48
correlates with underperformance. The correlation is not perfect but it is strong enough that
investors who ignore it leave alpha on the table.</p>

<h3 id="solar-pv-pace">Solar Photovoltaic Buildout Pace</h3>

<p>Annual global solar PV installations have grown from roughly 100 GW in 2018 to over
400 GW in 2025, with policy-driven support in China, India, the EU, and the US pushing further
growth. Each gigawatt of solar capacity embeds roughly 10 to 15 tonnes of silver, depending on
cell technology. A 400 GW install year translates into 4,000 to 6,000 tonnes of silver demand
from solar alone, or 130-200 million ounces. Policy announcements, tariff decisions, and
cell-efficiency breakthroughs that affect solar deployment pace move silver-price expectations
materially.</p>

<h3 id="gold-silver-ratio-driver">The Gold-Silver Ratio as a Mean-Reverting Signal</h3>

<p>The gold-silver ratio — gold price divided by silver price — has trading properties that
many investors use as a standalone signal. Historical range sits between 50 and 100, with
excursions to both extremes during specific regimes. When the ratio is above 80, contrarian
investors treat silver as cheap relative to gold and tilt allocation toward silver. When the
ratio is below 60, they tilt the opposite direction. The ratio has real mean-reversion
characteristics over multi-year windows, though it can stay at extremes for longer than
leveraged positions can wait out.</p>

<h3 id="retail-speculation">Retail Speculation and Futures Positioning</h3>

<p>Silver has a long history of concentrated speculative positioning — the 1980 Hunt brothers
episode, the 2011 peak, the early 2021 "silver squeeze" attempt via Reddit-coordinated retail
buying. CFTC Commitment of Traders data showing extreme non-commercial long positioning
typically precedes corrections; extreme short positioning precedes rallies. The signal is not
precise enough to time trades to the week but over multi-month windows it is a useful
overlay.</p>

<h2 id="gold-silver-ratio">The Gold-Silver Ratio: The Single Most Important Allocation Tool</h2>

<p>If you take one tool away from this guide, take the gold-silver ratio. It is the cleanest
signal available for deciding how to weight silver versus gold within a precious-metals
allocation.</p>

<p>The ratio reflects the relative price of gold and silver in the same currency: one ounce of
gold costs how many ounces of silver. The historical average over the past fifty years sits
around 65. The long-run average over the past century is closer to 55. During periods when
silver is perceived as a monetary metal alongside gold, the ratio tends toward the lower end
of the range. During periods when silver is seen primarily as an industrial commodity, the
ratio drifts higher.</p>

<p>Extreme readings mark meaningful opportunities. The March 2020 COVID-crash spike to roughly
125 preceded the 2020-2021 silver outperformance that narrowed the ratio back under 70. The
1980 Hunt-brothers-era spike to under 20 preceded a multi-year silver underperformance as the
ratio normalised. Every major ratio extreme over the past forty years has eventually mean-
reverted, usually within three years of the extreme print.</p>

<p>The operational use: when the ratio is above 90, a contrarian investor shifts toward silver
within their precious-metals allocation. When it is below 50, they shift back toward gold.
The ratio can remain at extremes for twelve to eighteen months, so position sizing should
reflect patience — this is not a short-horizon trade. But over multi-year windows, trading
around gold-silver ratio extremes has been one of the most reliable alpha sources in
precious-metals investing.</p>

<h2 id="investment-vehicles">Ways to Invest in Silver</h2>

<p>Unlike gold, silver's price-to-weight ratio and industrial use mix create different
practical considerations across investment vehicles. Understanding the trade-offs matters
more for silver than for gold because the "wrong" vehicle for the investor's actual objective
is easier to accidentally choose.</p>

<h3 id="physical-silver">Physical Silver</h3>

<p>Physical silver takes three forms: bullion bars (100 oz and 1,000 oz sizes for institutional,
1 oz and 10 oz for retail), coins (Silver Eagles, Maple Leafs, Britannias), and rounds
(generic medallion-style bullion). Retail premiums over spot for 1-oz products typically run
10-25%, compared to 3-5% for gold equivalents. The premium is driven by manufacturing and
distribution economics, not margin — silver's lower price per ounce means fixed costs
(minting, packaging, retail markup) are a larger percentage of the total.</p>

<p>Storage is the other consideration that differs from gold. A $100,000 silver allocation
weighs roughly 75 pounds at current prices and takes meaningful physical space. Home storage
is impractical for allocations above moderate sizes; bank safe-deposit boxes may have size
restrictions; allocated storage at bullion dealers carries annual fees of 0.5-1.0% of holdings.
Physical silver is the right choice for the specific use case of financial-system-failure
hedging but is more cumbersome than physical gold at equivalent dollar allocation.</p>

<h3 id="silver-etfs">Silver ETFs and ETPs</h3>

<p>Three silver ETFs dominate the retail market. SLV (iShares Silver Trust) is the largest,
most liquid, and lowest-cost at 0.50% expense ratio — it is the default choice for tactical
silver exposure in a brokerage account. SIVR (abrdn Physical Silver Shares) is similar in
structure with a 0.30% expense ratio, smaller fund size, and slightly wider bid-ask spreads.
PSLV (Sprott Physical Silver Trust) is structured as a closed-end trust with fully allocated
silver holdings — it trades at premiums and discounts to NAV (typically 0-5%), offers
redemption rights for silver delivery above a minimum threshold, and is often preferred by
investors who specifically want allocated silver without the operational complexity of
physical holdings.</p>

<p>For most investors wanting silver-price exposure without direct physical ownership, SLV
is the right default. The fund's size means the bid-ask spread is effectively zero in retail
volumes, and the counterparty risk is acceptable for most portfolio-allocation use cases.
PSLV is the right choice when the underlying thesis includes a specific concern about silver-
ETF custody arrangements.</p>

<h3 id="silver-streaming">Silver Streaming and Royalty Companies</h3>

<p>Silver streaming companies — Wheaton Precious Metals is the dominant name, with Triple Flag
Precious Metals and Sandstorm Gold as smaller peers — earn revenue by financing silver
production at other companies' mines in exchange for the right to purchase silver output at
pre-agreed prices (typically $4-5 per ounce, well below spot). The model structurally earns
high margins, avoids operational risk, and provides leveraged exposure to silver prices with
lower variance than direct mining equity.</p>

<p>For investors seeking silver-price exposure as a portfolio anchor — rather than speculative
upside — silver streaming names are often the best risk-adjusted vehicle. Wheaton in particular
holds meaningful silver exposure within a broader precious-metals stream portfolio, giving
investors silver-price leverage with single-name diversification.</p>

<h3 id="silver-miners">Silver Mining Equities</h3>

<p>Silver mining equities deliver the highest operating leverage to silver prices and the
highest variance. The major and mid-tier silver-primary producers — Pan American Silver,
Fortuna Mining, First Majestic Silver, Endeavour Silver, Silvercorp Metals, Aya Gold & Silver,
MAG Silver, Hecla Mining, Coeur Mining — give investors direct exposure to mine-level
economics. A silver producer with $18/oz all-in sustaining costs at a $85/oz spot silver
price earns roughly $67 per ounce of margin; at $50/oz spot it earns $32 per ounce — so small
movements in spot silver translate into large changes in earnings.</p>

<p>Development-stage and exploration-stage silver juniors add exploration and permitting
optionality on top of the price exposure. These names can deliver 5-10x returns in strong
silver-price cycles but can also go to zero if a financing goes poorly or a technical-study
outcome disappoints. The Verdict Framework we apply to gold juniors applies equally to silver
juniors, with the same five factors and the same scoring rubric.</p>

<h3 id="silver-miner-etfs">Silver Miner ETFs</h3>

<p>SIL (Global X Silver Miners ETF) and SILJ (ETFMG Prime Junior Silver Miners ETF) provide
basket exposure to silver equities. SIL holds the senior and mid-tier producers plus streaming
companies; SILJ skews toward junior developers and explorers with higher-variance holdings.
Expense ratios are 0.65-0.70% for both. These are reasonable choices for investors who want
silver-equity exposure without single-name selection, and they pair well with physical silver
or silver ETFs for a diversified silver-exposure allocation.</p>

<h2 id="verdict-framework-silver">How We Apply the Verdict Framework to Silver Equities</h2>

<p>Our 5-factor Verdict Framework applies to silver mining equities with minor emphasis
shifts from how we score gold juniors. Same factors, same scoring scale, different data
sources and jurisdictional weights.</p>

<p>Factor 1, management skin-in-the-game, works identically. Insider ownership percentage,
recent open-market insider buying (SEDI for Canadian issuers, SEC Form 4 filings for US
issuers), share-issuance discipline, and prior-venture track record. The scoring rubric is
unchanged.</p>

<p>Factor 2, project geology quality, requires silver-specific inputs. Grade is typically
measured in grams per tonne silver for underground mines and grams per tonne silver-equivalent
for polymetallic operations. A high-grade silver deposit produces at 300+ g/t silver; a
mid-grade heap-leach operation may run at 80-150 g/t. Metallurgy matters acutely for silver —
recovery rates on sulphide silver ores can vary from 70% to 95% depending on mineralogy and
processing route, and the difference between a 75% recovery and a 90% recovery can completely
change project economics.</p>

<p>Factor 3, capital structure health, is scored the same way. Fully-diluted share count
relative to the asset, warrant overhang, dilution history, working-capital runway. Silver
juniors historically run tighter cap tables than gold juniors because the financing environment
has been less frothy — but this varies cyclically and should be checked per name.</p>

<p>Factor 4, catalyst proximity, also identical in methodology. Near-term resource updates,
engineering studies, permitting milestones, offtake agreements. Silver projects tend to have
faster permitting timelines than gold projects in the same jurisdictions — smaller footprint,
less water intensity, simpler closure — which works in favor of catalyst scoring relative to
gold peers.</p>

<p>Factor 5, comparable acquisition value, requires a silver-specific comparable-transactions
set. Silver M&A comps are sparser than gold — fewer deals per year, higher proportion of
cross-commodity deals (silver producer acquired by gold major, silver stream sold to
diversified royalty company) — so the acquisition-value score for silver equities tends to be
more reliant on streaming-multiple benchmarks than on direct M&A.</p>

<h3 id="covered-silver-names">Our Silver Coverage</h3>

<p>GoGold Resources (TSX:GGD) is our only silver-primary name with a published scorecard as
of April 2026, carrying a 21/25 WATCH verdict. The WATCH rather than BUY reflects an
editorial override on commodity-mix considerations rather than a factor-level weakness —
technically the composite clears the BUY threshold. Los Ricos (Mexico) is the development
asset; Parral (Mexico) is the producing cash-flow base. Geology scored 5/5; catalyst scored
5/5.</p>

<p>The senior silver peer set — Aya Gold & Silver, MAG Silver, Pan American Silver, Fortuna
Mining, Silvercorp Metals, Endeavour Silver, First Majestic Silver — sits in our research
queue with scoring targeted for the 2026 coverage cycle. Gold-silver polymetallic names where
silver is meaningful but not primary (Dundee Precious Metals, certain gold-silver projects
in the Golden Triangle) will be scored under gold-primary classifications but flagged for
silver-exposure cross-reference.</p>

<h2 id="jurisdictions">Silver Mining Jurisdictions: Geography of Supply</h2>

<p>Silver production is more geographically concentrated than gold. Understanding where
individual silver-equity operations sit, and what the jurisdictional trade-offs look like, is
essential to selecting silver names.</p>

<h3 id="mexico">Mexico: The Dominant Jurisdiction</h3>

<p>Mexico produces roughly 24% of global mine silver output and hosts the largest share of
investable silver-primary producers. Fresnillo District, Zacatecas, Durango, and Chihuahua
host world-class silver mines — Juanicipio, La Herradura, San Julian, Saucito, and many
others. Mexican silver producers benefit from mature mining infrastructure, experienced local
workforce, and established regulatory frameworks — but have also faced policy headwinds in
recent years with the 2022-era AMLO-era tightening of new concessions and a slower permitting
environment for greenfield projects.</p>

<p>For investors: Mexican silver exposure is unavoidable in any meaningful silver-equity
allocation. The jurisdictional risk is real and priced into valuations. Diversifying across
multiple Mexican-operating names reduces single-operator risk without eliminating the
underlying jurisdictional exposure.</p>

<h3 id="peru-bolivia">Peru, Bolivia, and the Andean Belt</h3>

<p>Peru is the second-largest silver producer globally, with multiple polymetallic operations
and a smaller set of silver-primary producers. Peruvian jurisdictional risk has cycled through
different regimes over the past decade — mining-royalty debates, permitting-reform cycles,
community-consultation requirements — and current conditions are cautiously stable. Bolivia is
a smaller producer with higher jurisdictional risk. Neither country hosts the volume of
investable silver equities that Mexico does, but specific names (Fortuna Mining's Peruvian
operations, Pan American's Huaron mine) provide meaningful exposure.</p>

<h3 id="canada">Canada and the Golden Triangle Overlap</h3>

<p>Canadian silver production is mostly byproduct — lead-zinc mines, gold-silver polymetallic
operations in British Columbia's Golden Triangle. The Golden Triangle hosts Skeena Resources'
Eskay Creek restart (gold-silver), and historic operations like Silvertip. For investors
specifically seeking Canadian-jurisdiction silver exposure, the options are polymetallic gold-
silver names rather than silver-primary producers.</p>

<h3 id="other-jurisdictions">Other Jurisdictions: Australia, Poland, Russia</h3>

<p>Australia hosts meaningful silver byproduct production at lead-zinc operations (Cannington
and others) but few silver-primary investable names. Poland's KGHM is a major silver producer
as a copper byproduct — a unique supply source that responds to copper economics rather than
silver price directly. Russia is a significant producer but is effectively uninvestable for
Western portfolios due to sanctions and market-access restrictions.</p>

<h2 id="portfolio-construction">Portfolio Construction: How to Size a Silver Allocation</h2>

<p>The practical question for most investors is: given I have decided to hold some silver,
how much, and in what form?</p>

<p>For a diversified portfolio with a broad precious-metals allocation of 10-20% of total
value, silver typically represents 20-40% of the precious-metals sleeve — so 2-8% of total
portfolio value. The range is wide because it depends on: the investor's view on industrial
demand (more bullish = higher silver allocation), their read on the gold-silver ratio (wider
ratio = higher silver allocation as a mean-reversion bet), and their volatility tolerance
(higher tolerance = higher silver).</p>

<p>Within the silver allocation itself, a reasonable default construction: 30-40% in physical
silver or a silver ETF (SLV or PSLV), 20-30% in silver streaming equity (Wheaton Precious
Metals is the dominant choice), 30-40% in silver mining equities split across senior producers
and developers. This balance gives exposure to the silver-price move across multiple vehicles
with different risk profiles, without concentrating the allocation in any single name or
vehicle type.</p>

<p>Position-sizing within silver equities should respect the volatility differential versus
gold equities. If gold junior positions are sized at 3% of portfolio each, silver junior
positions should typically sit at 1.5-2% each. The silver positions will feel smaller in
dollar terms but will contribute equivalent portfolio volatility.</p>

<p>Rebalancing cadence: annual is usually sufficient. Silver positions can run meaningfully
above or below target allocation for twelve-month periods, and trying to rebalance more
frequently typically generates transaction costs without meaningful risk-reduction benefit.
The exception: if the gold-silver ratio hits a historical extreme (below 50 or above 90), a
tactical rebalance to lean into the mean-reversion trade can deliver alpha.</p>

<h2 id="risks">Risks Specific to Silver Investing</h2>

<p>Silver carries four risk categories worth naming explicitly — most overlap with gold risks
but silver's industrial demand layer adds a unique exposure.</p>

<p>First, higher volatility than gold. Silver positions will experience larger drawdowns in
gold-negative cycles and larger rallies in gold-positive cycles. Investors who do not size
positions for this asymmetry end up either panicked out of losses or over-concentrated by
gains. Plan position sizes at the outset assuming 30-40% annual volatility and adjust the
allocation to the level you can genuinely hold through that variance.</p>

<p>Second, industrial demand cyclicality. Chinese manufacturing slowdowns, European
industrial contraction, and solar-PV deployment slowdowns all pressure the industrial side of
silver demand. In a global recession with a concurrent commodity down-cycle, silver can
underperform gold meaningfully because its industrial demand layer declines even as its
monetary demand layer holds or rises. This is the scenario the gold-silver ratio widens to
80+ during.</p>

<p>Third, technological substitution risk in photovoltaics. The largest single silver demand
category is solar-cell manufacturing, and solar-cell silver content has been actively thrifted
by panel manufacturers over the past decade — grams of silver per cell has declined through
metallization-paste efficiency improvements and alternative-metal experimentation. A
breakthrough in copper-based or nickel-based cell metallization could reduce silver content
per cell further. This risk is slow-moving but real. It does not go away with a single panel
generation's product launch.</p>

<p>Fourth, jurisdictional concentration risk. Mexico's dominance of silver supply means any
meaningful silver-equity portfolio carries Mexican jurisdictional exposure. Diversification
across operators does not eliminate it. Investors should size their total Mexican-jurisdiction
exposure across the full portfolio (including gold names with Mexican operations) to ensure
the concentration sits within acceptable bounds.</p>

<h2 id="whats-covered">What's on Our Coverage and What's Coming</h2>

<p>Our silver coverage is lighter than our gold coverage by design — the framework started
with gold juniors because that is where rigorous analysis was thinnest relative to promotional
research. Silver is actively being expanded through 2026.</p>

<p>Currently scored: GoGold Resources (TSX:GGD) at 21/25 WATCH. The highest-scoring silver
name on our coverage, with a factor mix that technically clears the BUY threshold.</p>

<p>Queued for research in 2026: Aya Gold & Silver (Morocco), MAG Silver (Mexico Juanicipio JV
with Fresnillo), Pan American Silver (Americas senior producer), Fortuna Mining (Americas
mid-tier), Silvercorp Metals (China, Ecuador), Endeavour Silver (Mexico, Chile), First
Majestic Silver (Mexico). Each will get a full scorecard with factor-by-factor notes at its
company hub page — /companies/&lt;slug&gt;/ — as research capacity clears through the queue.</p>

<p>Gold-silver polymetallic coverage continues under the gold-primary classification where
the company files its primary commodity as gold. Readers seeking silver-byproduct exposure
within the gold coverage universe should cross-reference the individual scorecards.</p>

<h2 id="conclusion">Using This Guide: A Practical Checklist</h2>

<p>If you're building silver exposure from scratch, a reasonable sequence: first decide your
total precious-metals allocation as a percentage of portfolio. Second, split between gold and
silver based on your read of the gold-silver ratio and your view on industrial demand — 60/40
gold-heavy is a reasonable default for most investors, tilting toward silver when the ratio
sits above 80. Third, within silver, split across physical/ETF, streaming, and mining equity
per the construction outlined above. Fourth, size positions respecting silver's higher
volatility. Fifth, rebalance annually unless the gold-silver ratio hits an extreme reading
that warrants tactical action.</p>

<p>If you are building from an existing precious-metals portfolio, the question is usually
whether to rebalance toward silver from an overweight gold allocation. The gold-silver ratio
reading is the most useful input. Do the work on individual silver-equity names before sizing
positions — read the covered-company scorecards at miningstockreport.com/companies/, check
the factor-level notes, and pay particular attention to capital structure and jurisdictional
mix.</p>

<p>The Verdict Framework is not a substitute for doing the work. It is a structured read on
the work already done. Silver equities require the same discipline as gold equities: read the
43-101 technical report, check the insider filings, calculate your own P/NAV against a price
deck you actually believe, and size positions to reflect what you are willing to lose if a
specific thesis breaks. Precious metals investing rewards patience and punishes conviction
that is not grounded in the underlying numbers. This guide is a starting point — the
scorecards are where the specific-name work lives.</p>
""".strip()


GUIDE_DATA = {
    "title": "Investing in Silver: A Comprehensive Guide for Stocks, Bullion, and Portfolio Allocation",
    "slug_hint": "silver-investor-guide-2026",
    "pillar_slug": "investing-guides",
    "meta_title": "Silver Investing Guide 2026: Stocks, Bullion, Framework",
    "meta_description": (
        "Silver as a dual monetary-industrial commodity, the gold-silver ratio, silver "
        "mining equities, and portfolio construction. Long-form guide."
    ),
    "excerpt": (
        "Silver is not just cheap gold. This long-form guide walks through the silver market "
        "as it sits in 2026, the supply-demand dynamics driving prices, the different ways to "
        "take exposure, how we apply the 5-factor Verdict Framework to silver equities, and "
        "how to size a silver allocation within a broader precious-metals portfolio."
    ),
    "answer_capsule": (
        "Silver is both a monetary asset and an industrial commodity — roughly 55% of annual "
        "demand is industrial (photovoltaics, EV electronics, medical) versus 20% for "
        "investment and 20% for jewelry. The silver market has been in structural deficit "
        "from 2021 through 2024-2025. Silver responds to real interest rates and the US "
        "dollar like gold, but also to Chinese manufacturing PMI and solar PV installation "
        "pace. The gold-silver ratio is the most reliable allocation tool for deciding the "
        "silver-to-gold tilt within a precious-metals portfolio."
    ),
    "key_takeaways": [
        "Silver is a dual monetary-industrial commodity — different drivers than gold, not a substitute",
        "Roughly 55% of silver demand is industrial; photovoltaic solar is the largest single category",
        "The silver market has run structural supply deficits from 2021 through 2024-2025",
        "The gold-silver ratio is the most useful allocation tool: above 80 favors silver, below 60 favors gold",
        "Mexico produces roughly 24% of global mine silver — jurisdictional concentration is real",
        "Silver equities carry roughly 1.5-2x the volatility of gold equities; size positions accordingly",
        "GoGold Resources is the only silver-primary name currently scored on our Verdict Framework at 21/25",
    ],
    "faq_items": [
        {
            "question": "Is silver just a leveraged bet on gold?",
            "answer": (
                "No. Gold is primarily a monetary commodity driven by real rates, central-bank "
                "demand, and safe-haven flows. Silver is both a monetary asset and an "
                "industrial commodity, with 55% of annual demand coming from photovoltaic, "
                "electronics, medical, and other industrial applications. The two metals "
                "respond to different news flow, and an investor who holds both is "
                "diversifying across macro exposures rather than doubling down on one."
            ),
        },
        {
            "question": "What is the gold-silver ratio and how should I use it?",
            "answer": (
                "The gold-silver ratio is the price of one ounce of gold expressed in ounces "
                "of silver. Historical range sits between 50 and 100, with long-run average "
                "around 55-65. Contrarian investors use extremes as allocation signals: when "
                "the ratio is above 80, silver is cheap relative to gold and deserves a "
                "higher share of a precious-metals allocation. When it is below 60, gold "
                "deserves the tilt. The ratio mean-reverts over multi-year windows."
            ),
        },
        {
            "question": "What are the best ways to invest in silver?",
            "answer": (
                "Four practical vehicles. Physical silver (coins, bars, allocated storage) for "
                "financial-system-failure hedging. Silver ETFs (SLV, SIVR, PSLV) for tactical "
                "price exposure. Silver streaming companies (Wheaton Precious Metals as the "
                "dominant name) for lower-variance structural silver-price participation. "
                "Silver mining equities for the highest operating leverage and highest "
                "variance. Most diversified silver allocations combine multiple vehicles."
            ),
        },
        {
            "question": "Why is silver demand driven by solar panels?",
            "answer": (
                "Photovoltaic solar cells use silver paste for electrical contacts and "
                "connections. Each gigawatt of installed solar capacity embeds roughly 10 to "
                "15 tonnes of silver, depending on cell technology. Global solar installations "
                "reached over 400 gigawatts per year in 2025, making PV the single largest "
                "industrial silver demand category — roughly 200 million ounces per year. "
                "Policy-driven support for solar buildout in China, the EU, India, and the US "
                "has structurally lifted silver demand."
            ),
        },
        {
            "question": "How much silver should my portfolio hold?",
            "answer": (
                "For a diversified portfolio with a 10-20% precious-metals allocation, silver "
                "typically represents 20-40% of the precious-metals sleeve — 2-8% of total "
                "portfolio value. The right allocation within that range depends on your view "
                "on industrial demand, your read of the gold-silver ratio, and your "
                "volatility tolerance. Rebalance annually unless the gold-silver ratio hits a "
                "historical extreme."
            ),
        },
        {
            "question": "Why does Mexico dominate silver production?",
            "answer": (
                "Mexico produces roughly 24% of global mine silver output — more than any "
                "other country. The dominance is geological (rich epithermal silver vein "
                "systems in Zacatecas, Durango, Chihuahua, and Fresnillo districts) and "
                "historical (five centuries of continuous silver mining experience). Most "
                "investable silver-primary producers have meaningful Mexican exposure. "
                "Jurisdictional risk is real and priced into valuations, but unavoidable in "
                "any meaningful silver-equity allocation."
            ),
        },
        {
            "question": "Which silver stocks do you cover?",
            "answer": (
                "Currently scored on our Verdict Framework: GoGold Resources (TSX:GGD) at "
                "21/25 WATCH. Queued for coverage through 2026: Aya Gold & Silver, MAG "
                "Silver, Pan American Silver, Fortuna Mining, Silvercorp Metals, Endeavour "
                "Silver, and First Majestic Silver. Gold-silver polymetallic names continue "
                "to be scored under gold-primary classifications with silver exposure flagged "
                "in individual scorecards."
            ),
        },
    ],
    "published_at": datetime(2026, 5, 20, 10, 0, 0, tzinfo=dt_timezone.utc),
    "body": SILVER_GUIDE_BODY,
}


def seed_silver_guide(apps, schema_editor):
    from apps.blog.models import Post, Pillar
    from apps.accounts.models import User

    try:
        author = User.objects.get(username="chaugen")
    except User.DoesNotExist:
        return

    if Post.objects.filter(title=GUIDE_DATA["title"]).exists():
        return

    pillar = Pillar.objects.filter(slug=GUIDE_DATA["pillar_slug"]).first()
    Post.objects.create(
        title=GUIDE_DATA["title"],
        author=author,
        excerpt=GUIDE_DATA["excerpt"],
        answer_capsule=GUIDE_DATA["answer_capsule"],
        key_takeaways=GUIDE_DATA["key_takeaways"],
        body=GUIDE_DATA["body"],
        faq_items=GUIDE_DATA["faq_items"],
        pillar=pillar,
        post_type="guide",
        status="published",
        is_premium=False,
        published_at=GUIDE_DATA["published_at"],
        meta_title=GUIDE_DATA["meta_title"],
        meta_description=GUIDE_DATA["meta_description"],
    )


def reverse_seed(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    Post.objects.filter(title=GUIDE_DATA["title"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0011_seed_commodity_guides"),
    ]
    operations = [
        migrations.RunPython(seed_silver_guide, reverse_seed),
    ]
