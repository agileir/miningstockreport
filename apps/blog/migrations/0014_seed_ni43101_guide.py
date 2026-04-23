"""
Seed the long-form NI 43-101 investor guide under the Due Diligence pillar.

Status is DRAFT so the post does not publish until the editorial team has
replaced the inline <aside class="editor-note"> placeholders with real
graphics, photos, tables, and videos. Every placeholder is kept verbatim
in the body so the production team can see exactly where each asset is
meant to sit.

Pillar: due-diligence (already seeded in 0003).
"""
from django.db import migrations


NI43101_GUIDE_BODY = """
<p>If you buy mining stocks without reading 43-101 reports, you are gambling. Full stop.
The technical report is the single most important disclosure document in the junior
mining world — it is where geology meets engineering meets economics, and it is the
document that separates projects worth billions from projects worth nothing. Yet most
retail investors either ignore these reports completely or skim the first page, read
the NPV headline, and move on.</p>

<p>That is a catastrophic mistake. Professional analysts, portfolio managers, and mining
engineers spend days (sometimes weeks) dissecting a single technical report before
committing capital. They know where the truth is hidden, which sections companies use to
bury bad news, and which numbers are worth trusting versus which are marketing fluff
dressed up in technical language.</p>

<p>This guide will teach you to read an NI 43-101 the way a professional does. By the end,
you should be able to open any technical report and, within two to three hours, form an
independent view on whether the project is economic, whether the numbers are credible,
and whether the stock is worth owning.</p>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Hero image]</strong><br>
  Split-screen photo: a raw drill core on the left, a financial model/spreadsheet on the
  right, with a 43-101 report cover in the middle.<br>
  <em>Caption:</em> "The 43-101 translates rocks into cash flows. Learning to read it is
  the single highest-ROI skill in mining investing."
</aside>

<h2 id="what-ni-43101-is">Part 1: What NI 43-101 Actually Is — And Why It Exists</h2>

<p>NI 43-101 stands for <strong>National Instrument 43-101 — Standards of Disclosure for
Mineral Projects</strong>. It is a Canadian securities rule administered by the Canadian
Securities Administrators (CSA) that governs how publicly listed mining companies (on the
TSX, TSX-V, CSE) must disclose technical information about their mineral projects.</p>

<p>The rule was born out of the <strong>Bre-X scandal</strong> in 1997. Bre-X Minerals was
a Calgary-based company that claimed to have discovered the world's largest gold deposit
at Busang in Indonesia. The company's market cap briefly exceeded $6 billion before
investigators discovered that the drill core samples had been salted — literally sprinkled
with gold from a jeweller's file. The stock went to zero, pensioners lost their savings,
and a lead geologist fell (or was pushed) from a helicopter over the Indonesian jungle.</p>

<p>NI 43-101 was implemented in 2001 as a direct response. It mandates three things:</p>

<ol>
  <li>Technical information must be prepared by or under the supervision of a
  <strong>Qualified Person (QP)</strong> — an accredited geologist or engineer with at
  least five years of relevant experience.</li>
  <li>All material technical information disclosed in news releases, websites, or investor
  presentations must be supported by a publicly filed technical report.</li>
  <li>Resources and reserves must be reported using <strong>CIM Definition Standards</strong>
  — a standardized classification system that makes projects comparable.</li>
</ol>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Table: Comparable global disclosure regimes]</strong><br>
  4-column table comparing NI 43-101 (Canada), JORC Code (Australia), SAMREC (South Africa),
  and SK-1300 (USA). Rows: QP equivalent, resource categories, reserve categories,
  jurisdictional scope. Useful because investors often see projects reported under multiple
  codes.
</aside>

<p>The key insight: <strong>43-101 is a disclosure standard, not a quality standard.</strong>
A project can have a compliant 43-101 report and still be a terrible investment. The report
tells you what the QP believes is true — it does not tell you whether the project will make
money. Your job as an investor is to read the document skeptically.</p>

<h2 id="qualified-person">Part 2: The Qualified Person — Who Wrote This Thing?</h2>

<p>Before you read a single word of the technical content, <strong>flip to the signature
page and the QP disclosures</strong>. Professional analysts do this first. Always.</p>

<p>You are looking for:</p>

<ul>
  <li><strong>Who is the QP?</strong> Are they an employee of the company (an "internal QP")
  or an independent consultant? Internal QPs are allowed for certain filings but independent
  QPs carry more weight, especially for PEAs, PFSs, and FSs.</li>
  <li><strong>What firm do they work for?</strong> Tier-one engineering firms — SRK
  Consulting, AMC, Wood, WSP (formerly Golder), Ausenco, Hatch, BBA, DRA, Lycopodium,
  Roscoe Postle (now SLR Consulting), Mining Plus, Behre Dolbear — have reputations to
  protect. A report from SRK is not automatically correct, but it carries more credibility
  than a report from a one-person shop no one has heard of.</li>
  <li><strong>What's the QP's specialty?</strong> A 43-101 is a team document. You want a
  geologist signing off on resources, a mining engineer signing off on the mine plan, a
  metallurgist signing off on recovery, and so on. Be suspicious when a single QP signs
  off on everything — especially for a complex project.</li>
  <li><strong>History.</strong> Google the QP's name. Have they been involved in previous
  projects that went sideways? Have they been sanctioned by their professional association?</li>
</ul>

<blockquote class="pro-tip">
  <strong>Pro tip.</strong> A useful rule — if the QP list includes SRK, AMC, SLR, or Wood
  for the resource estimate, take the numbers seriously. If the resource was estimated
  in-house by a company geologist with no independent review, add a significant discount
  until the project is advanced further.
</blockquote>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Annotated screenshot]</strong><br>
  Screenshot of a real QP certificate page from a well-known project (redact names if
  needed), with annotations pointing to: name, designation (P.Geo, P.Eng), firm,
  independence statement, site visit date.
</aside>

<h2 id="report-anatomy">Part 3: The 27-Section Anatomy of a 43-101</h2>

<p>Every technical report follows the same skeleton. Understanding this structure is the
first big unlock — once you know where information lives, you can navigate a 300-page
report in minutes.</p>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Full-page infographic — CRITICAL]</strong><br>
  "The 43-101 Report Anatomy" — a vertical flowchart showing all 27 sections grouped into
  four colour-coded blocks: <strong>Context</strong> (1–6), <strong>Geology &amp; Drilling</strong>
  (7–12), <strong>Resource to Economics</strong> (13–22), and <strong>Conclusions</strong>
  (23–27). For each section include a one-line "what's in it" description and a star
  rating (1–5) for investor importance. This is the map investors will refer to repeatedly.
</aside>

<p>The 27 sections, in order:</p>

<ol>
  <li>Summary</li>
  <li>Introduction</li>
  <li>Reliance on Other Experts</li>
  <li>Property Description and Location</li>
  <li>Accessibility, Climate, Local Resources, Infrastructure, Physiography</li>
  <li>History</li>
  <li>Geological Setting and Mineralization</li>
  <li>Deposit Types</li>
  <li>Exploration</li>
  <li>Drilling</li>
  <li>Sample Preparation, Analyses, and Security</li>
  <li>Data Verification</li>
  <li>Mineral Processing and Metallurgical Testing</li>
  <li>Mineral Resource Estimates</li>
  <li>Mineral Reserve Estimates</li>
  <li>Mining Methods</li>
  <li>Recovery Methods</li>
  <li>Project Infrastructure</li>
  <li>Market Studies and Contracts</li>
  <li>Environmental Studies, Permitting, Social or Community Impact</li>
  <li>Capital and Operating Costs</li>
  <li>Economic Analysis</li>
  <li>Adjacent Properties</li>
  <li>Other Relevant Data and Information</li>
  <li>Interpretation and Conclusions</li>
  <li>Recommendations</li>
  <li>References</li>
</ol>

<p>For a <strong>resource-stage</strong> project (no economic study yet), sections 15–22
are typically absent or placeholders. For a <strong>Preliminary Economic Assessment
(PEA)</strong>, <strong>Pre-Feasibility Study (PFS)</strong>, or <strong>Feasibility
Study (FS)</strong>, all 27 sections are required and filled out.</p>

<p>Now let's go through the sections that matter most, in the order a professional analyst
reads them.</p>

<h2 id="analyst-reading-order">Part 4: The Analyst's Reading Order — Don't Start at Page One</h2>

<p>Here is a counterintuitive truth: professionals almost never read a 43-101 cover to
cover in page order. They jump around, because they know where the signal is and where
the noise is. Here is the typical reading order I use and most analysts I know use
something similar:</p>

<ol>
  <li><strong>Section 1 (Summary)</strong> — to get the pitch.</li>
  <li><strong>Section 25 (Interpretation &amp; Conclusions)</strong> — to see what the QP
  themselves flag as risks.</li>
  <li><strong>Section 14 (Resource Estimate)</strong> — to stress-test the orebody.</li>
  <li><strong>Section 22 (Economic Analysis)</strong> — to see if the money math works.</li>
  <li><strong>Section 21 (Capex/Opex)</strong> — to test whether the economics are credible.</li>
  <li><strong>Section 13 + 17 (Metallurgy &amp; Recovery)</strong> — to see if the metal
  actually comes out.</li>
  <li><strong>Section 16 (Mining Methods)</strong> — to test the mine plan assumptions.</li>
  <li><strong>Sections 11–12 (QA/QC and Data Verification)</strong> — to trust the data.</li>
  <li><strong>Section 20 (Environmental &amp; Permitting)</strong> — to find fatal flaws.</li>
  <li><strong>Sections 4–6 (Property, Access, History)</strong> — for political and
  logistical context.</li>
</ol>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Visual]</strong><br>
  A numbered circular diagram showing "The Analyst's Reading Path" with arrows indicating
  the order above. Could be styled as a treasure-hunt map.
</aside>

<p>Let's dig into each of these.</p>

<h2 id="section-1-summary">Part 5: Section 1 — The Summary (Read Skeptically)</h2>

<p>The Summary is the company's best foot forward. It is what goes into investor
presentations and press releases. Treat it like a movie trailer — useful, but not the
movie.</p>

<p>What you want from the Summary on a first pass:</p>

<ul>
  <li><strong>Commodity</strong> and deposit type (gold, copper-gold porphyry, VMS, SEDEX
  lead-zinc, lithium brine, nickel sulfide, uranium, etc.).</li>
  <li><strong>Location</strong> (country, province, distance from infrastructure).</li>
  <li><strong>Stage</strong> (exploration, resource, PEA, PFS, FS, construction, production).</li>
  <li><strong>Resource size and grade.</strong></li>
  <li><strong>Economic headlines</strong> (NPV, IRR, initial capex, payback, mine life).</li>
  <li><strong>Commodity price assumptions.</strong></li>
</ul>

<p>Write these down in a notebook or spreadsheet before reading further. You will revisit
them and often find they disagree with the detail elsewhere in the report.</p>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Investor template / downloadable]</strong><br>
  A blank "Project Snapshot Worksheet" investors can download — rows for the above
  bullets, plus columns for "From Summary" vs "From Detail" vs "My Adjusted Value." This
  turns reading into a structured exercise.
</aside>

<p>A warning: the Summary will always quote the most favourable case. If there's a base
case and an upside case, the Summary features the upside case. If the mine plan includes
both open-pit and underground phases, the Summary averages them to hide a high-cost
underground tail. Read with this in mind.</p>

<h2 id="section-14-resources">Part 6: Section 14 — The Mineral Resource Estimate</h2>

<p>This is the heart of the report. The resource estimate answers the question:
<strong>how much metal is in the ground, and how confident are we in that number?</strong></p>

<h3 id="resource-classification">Resource Classification: Inferred, Indicated, Measured</h3>

<p>CIM defines three resource categories based on geological confidence:</p>

<ul>
  <li><strong>Inferred</strong> — the lowest confidence. Based on limited drilling; quantity
  and grade are estimated with "low level of confidence." You cannot base a mine plan or
  an economic study (other than a PEA) on inferred ounces. Many juniors' resources are
  70%+ inferred — that is a flashing yellow light.</li>
  <li><strong>Indicated</strong> — moderate confidence. Drilling is dense enough that
  continuity of grade is reasonably assumed. This is the minimum category that supports
  a PFS or FS reserve conversion.</li>
  <li><strong>Measured</strong> — highest confidence. Tight drill spacing, typically at
  spacing that allows grade variability to be well understood. Rare in early-stage
  projects.</li>
</ul>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Diagram — CRITICAL]</strong><br>
  The classic "CIM Reporting Pyramid" — a pyramid showing Exploration Results → Inferred
  Resource → Indicated Resource → Measured Resource → Probable Reserve → Proven Reserve,
  with arrows and "modifying factors" labeled. This is the single most important concept
  diagram in the entire guide.
</aside>

<h3 id="section-14-lookfor">What to Look For</h3>

<p>When you get to Section 14, extract:</p>

<ol>
  <li><strong>Tonnes, grade, and contained metal</strong> for each category, reported
  separately. Never accept "total resource" that combines measured, indicated, and
  inferred into one number — that is a presentation trick.</li>
  <li><strong>Cut-off grade.</strong> The cut-off is the minimum grade at which rock is
  considered ore. It is the single biggest lever in the entire report. A gold deposit
  reported at 0.3 g/t cut-off will look enormous; the same deposit at 0.5 g/t cut-off may
  be half the size. Professionals always ask: "is the cut-off grade realistic at the
  assumed mining method and commodity price?"</li>
  <li><strong>Commodity price assumption</strong> for the cut-off calculation. If gold is
  spot-priced at $2,300/oz and the resource is calculated using $1,950/oz, the reported
  resource is conservative — good. If it is calculated at $2,600/oz, the resource is
  aggressive — be wary.</li>
  <li><strong>Drill spacing and interpolation method.</strong> Ordinary kriging, inverse
  distance weighting (IDW2 or IDW3), and nearest neighbour are the common methods. You do
  not need to be a geostatistician, but you do want to check that the QP discusses search
  ellipses, variography, and block size.</li>
  <li><strong>Sensitivity tables.</strong> Good reports show resource tonnage and grade at
  multiple cut-off grades. This lets you see how fragile the number is.</li>
</ol>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Table format example]</strong><br>
  Example resource table with cut-off sensitivity: columns = cut-off grades (0.3, 0.4, 0.5,
  0.6 g/t); rows = Measured tonnes, M grade, Indicated tonnes, I grade, Inferred tonnes,
  I grade, Total contained ounces at each cut-off.<br>
  <em>Annotate:</em> "Watch the curve — if tonnage falls by 60% when cut-off rises 0.1 g/t,
  the deposit is marginal."
</aside>

<h3 id="section-14-redflags">Red Flags in Section 14</h3>

<ul>
  <li>High inferred percentage (>50% of total resource) in a PEA or PFS.</li>
  <li>Cut-off grade far below the industry norm for the deposit type.</li>
  <li>Very wide drill spacing being used to support an Indicated classification.</li>
  <li>No independent review of the resource estimate.</li>
  <li>A large jump in resource tonnage between consecutive reports with minimal new
  drilling (suggests methodology change, not real growth).</li>
</ul>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Graphic]</strong><br>
  Annotated 3D block model image (most reports include one — the coloured "iso-shell"
  renderings). Highlight where Measured, Indicated, and Inferred blocks are spatially —
  Inferred blocks are usually on the edges and at depth.<br>
  <em>Caption:</em> "Visualizing where confidence lives — and where it doesn't."
</aside>

<h2 id="section-15-reserves">Part 7: Section 15 — Mineral Reserves (PFS and FS Only)</h2>

<p>A <strong>reserve</strong> is the subset of a resource that has been demonstrated to
be economically mineable after applying "modifying factors" — metallurgy, mining method,
processing, dilution, mining recovery, capital and operating costs, metal prices, royalties,
permitting, environmental, legal, political, marketing.</p>

<ul>
  <li><strong>Probable Reserve</strong> ← converted from Indicated Resource.</li>
  <li><strong>Proven Reserve</strong> ← converted from Measured Resource.</li>
  <li><strong>Inferred Resource cannot be converted to reserve. Ever.</strong> This is a
  regulatory bright line.</li>
</ul>

<p>When reading Section 15, extract:</p>

<ul>
  <li>The <strong>conversion ratio</strong> — what percentage of the Indicated Resource
  became Probable Reserve? A 75–90% conversion is typical and healthy. If it's 100%, be
  suspicious. If it's below 50%, the deposit has continuity or grade problems.</li>
  <li>The <strong>dilution and mining recovery assumptions.</strong> Open-pit dilution is
  typically 3–10%; underground dilution can be 10–25% or higher depending on mining
  method. Mining recovery is often 90–95% open-pit, 85–95% underground.</li>
  <li>The <strong>reserve grade versus resource grade.</strong> Reserve grade is almost
  always lower than resource grade because of dilution. If reserve grade exceeds resource
  grade, something is wrong (or a higher cut-off was used to high-grade the mine plan).</li>
</ul>

<h2 id="metallurgy">Part 8: Sections 13 and 17 — Metallurgy and Recovery (Where Projects Die Quietly)</h2>

<p>This is where many retail investors check out. Do not. Metallurgy is where a surprising
number of projects fail.</p>

<p><strong>Recovery</strong> is the percentage of metal in the ore that ends up in the
final concentrate or doré bar. If your gold deposit has 90% recovery, a tonne of rock
grading 1 g/t produces 0.9 g/t of saleable gold. If recovery drops to 70% because of
refractory mineralogy, the same deposit is worth 22% less — and often uneconomic.</p>

<p>What to look for:</p>

<ol>
  <li><strong>Metallurgical test work stage.</strong> Bottle roll tests and bench-scale
  leach tests are early-stage. Locked-cycle flotation tests and pilot plant tests are
  late-stage and far more credible.</li>
  <li><strong>Sample representativeness.</strong> Did metallurgical samples come from
  across the deposit, or just from the high-grade core? Small, non-representative samples
  produce flattering recoveries that won't hold up in production.</li>
  <li><strong>Deleterious elements.</strong> Arsenic (in gold), uranium (in copper
  concentrates), fluorine, mercury, bismuth — these attract smelter penalties or outright
  rejection. A good report discusses them openly.</li>
  <li><strong>Refractory ore.</strong> If the word "refractory" appears, read carefully.
  Refractory gold ore requires pressure oxidation, roasting, or bio-leach — all expensive.
  Refractory ore in a PEA with a simple CIL flowsheet is a red flag.</li>
  <li><strong>Concentrate grade and smelter terms.</strong> For base metals, the
  concentrate grade (e.g., 25% copper, 55% zinc) determines smelter treatment and refining
  charges, which dramatically affect realized prices.</li>
</ol>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Flowchart]</strong><br>
  A simplified process flow diagram template — "Ore → Crush → Grind → Flotation/Leach →
  Concentrate/Doré → Smelter/Refinery → Metal." Overlay typical recovery losses at each
  stage. Teaches investors where the metal "leaks."
</aside>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Photo]</strong><br>
  Real photo of a flotation bank, CIL tank, or SAG mill with labels. Most investors have
  never seen a processing plant — showing them physical context builds intuition.
</aside>

<h2 id="mining-methods">Part 9: Section 16 — Mining Methods</h2>

<p>This section describes how the ore will be extracted. The two broad categories are:</p>

<ul>
  <li><strong>Open pit</strong> — cheaper per tonne, higher dilution, lower grade
  tolerated. Think large porphyry coppers, most heap-leach golds.</li>
  <li><strong>Underground</strong> — higher cost per tonne, more selective, higher grade
  required. Sub-level caving, long-hole stoping, cut-and-fill, block caving are the main
  methods.</li>
</ul>

<p>Key things to check:</p>

<ul>
  <li><strong>Strip ratio</strong> (for open pits): tonnes of waste moved per tonne of
  ore. A 2:1 strip ratio is lean; 8:1 is heavy; above 12:1 starts to compromise economics.</li>
  <li><strong>Mining rate</strong> (tonnes per day or per year). Is it plausible given the
  deposit geometry and the planned fleet?</li>
  <li><strong>Mining cost per tonne.</strong> Open-pit mining in Canada or Australia
  typically runs $2.50–$5.00/t of material moved; underground can be $40–$120/t depending
  on method and depth.</li>
  <li><strong>Pit slope angles.</strong> Overly aggressive slopes (steeper than 50°)
  without geotechnical backing can fail catastrophically. Failures cost lives and years.</li>
  <li><strong>Ramp-up schedule.</strong> How long from first ore to steady-state
  production? Twelve to 24 months is normal; anything faster is optimistic.</li>
</ul>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Cross-section diagram]</strong><br>
  A typical mine cross-section showing open-pit ramps, pit walls, ore zones, and waste
  dumps. Second diagram for underground — showing shaft, decline, stopes, and backfill.
  These are almost universally included in technical reports — pull from a real example
  and annotate.
</aside>

<h2 id="capex-opex-economics">Part 10: Sections 21 and 22 — Capex, Opex, and the Economic Model</h2>

<p>This is where all the geology and engineering resolves into a number that either
attracts capital or doesn't.</p>

<h3 id="capital-costs">Capital Costs (Section 21)</h3>

<p><strong>Initial capex</strong> is the money needed to build the mine and get it to
commercial production. <strong>Sustaining capex</strong> is the ongoing capital needed to
keep it running (fleet replacement, tailings expansions, pit pushbacks).</p>

<p>When reading capex, watch for:</p>

<ul>
  <li><strong>Accuracy level.</strong> PEA-level capex is ±30–50%. PFS-level is ±25%.
  FS-level is ±15%. Treat a PEA capex estimate as a very rough number — history shows
  final construction capex typically comes in 20–50% above the PEA estimate, often more
  for complex projects in difficult jurisdictions.</li>
  <li><strong>Contingency percentage.</strong> PEAs often use 15–20% contingency. FS
  should use 10–15% on engineered costs. If contingency is under 10%, the engineer is
  being aggressive.</li>
  <li><strong>Owner's costs.</strong> Often 5–10% of capex. If missing or suspiciously
  low, add 8% yourself.</li>
  <li><strong>EPCM or EPC assumption.</strong> Engineering/Procurement/Construction
  Management is the common contract structure; it exposes the owner to cost overruns.</li>
  <li><strong>Exclusions.</strong> Read the fine print — working capital, closure bonding,
  import duties, and pre-production operating costs are sometimes excluded.</li>
</ul>

<h3 id="operating-costs">Operating Costs (Section 21)</h3>

<p>Operating cost is usually reported in three ways:</p>

<ol>
  <li><strong>$/tonne milled</strong> — useful for comparing processing efficiency.</li>
  <li><strong>$/tonne of ore or ore+waste moved</strong> — useful for mining efficiency.</li>
  <li><strong>$/oz (or $/lb) of payable metal</strong> — the headline number; includes
  mining, processing, G&amp;A, and refining.</li>
</ol>

<p>For gold, pay close attention to two metrics:</p>

<ul>
  <li><strong>Cash cost per ounce</strong> — a legacy measure, now largely replaced.</li>
  <li><strong>All-In Sustaining Cost (AISC) per ounce</strong> — includes cash costs +
  sustaining capex + reclamation + corporate G&amp;A allocated to the mine. AISC is the
  number that matters. A gold mine with AISC below $1,200/oz is healthy at today's
  prices. Above $1,600/oz and margins are thin.</li>
</ul>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Chart]</strong><br>
  Global gold cost curve — AISC on y-axis, cumulative production on x-axis, with major
  mines plotted and a dotted line showing the project in question. Teaches investors to
  think about cost positioning, not absolute cost.
</aside>

<h3 id="economic-analysis">Economic Analysis (Section 22)</h3>

<p>This section is the DCF model summary. Key outputs:</p>

<ul>
  <li><strong>NPV (Net Present Value).</strong> Usually reported at 5%, 8%, and 10%
  discount rates. Professionals focus on <strong>NPV at 8% after-tax</strong> as the
  reference figure for most mining projects (higher discount rates for jurisdictional
  risk, lower for Tier 1 jurisdictions).</li>
  <li><strong>IRR (Internal Rate of Return).</strong> For a PFS or FS, an after-tax IRR
  below 15% is borderline; 20–30% is attractive; above 40% you should ask why it's so
  high and what commodity price assumption is driving it.</li>
  <li><strong>Payback period.</strong> How long to recover the initial capex? Four years
  or less is strong; over six years is risky.</li>
  <li><strong>Mine life.</strong> Long-life assets (15+ years) trade at premium multiples.
  Short-life (5–7 years) trade at discounts unless exploration upside is clear.</li>
  <li><strong>LOM (Life-of-Mine) production profile.</strong> Look for smooth, level
  production versus a front-loaded curve that drops off a cliff.</li>
</ul>

<h3 id="commodity-price">The Commodity Price Assumption — The Single Most Important Number</h3>

<p>Every economic model uses a set of long-term commodity prices. <strong>This single
assumption can make or break the project.</strong> A gold project modeled at $2,400/oz
looks spectacular; the same project at $1,800/oz may have negative NPV.</p>

<p>Professionals do three things:</p>

<ol>
  <li><strong>Recalculate the economics at spot prices</strong> and at consensus long-term
  prices (typically published by major banks).</li>
  <li><strong>Run sensitivity.</strong> Every 43-101 economic section should include an
  NPV sensitivity table showing NPV at ±10%, ±20% commodity prices, capex, and opex. If
  that table is missing, demand it before buying the stock.</li>
  <li><strong>Compare the assumption to current spot.</strong> If the report uses prices
  well above current spot (e.g., $2,700/oz gold when spot is $2,300), treat the NPV
  headline as marketing.</li>
</ol>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Tornado chart — CRITICAL]</strong><br>
  NPV Sensitivity Tornado Chart — horizontal bars showing NPV impact of ±20% in: gold
  price, capex, opex, grade, recovery, discount rate, exchange rate. Biggest bars at top.
  Investors should build this for every project they own.
</aside>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Interactive tool / downloadable]</strong><br>
  A downloadable "NPV recalculator" spreadsheet that takes LOM production, capex, opex,
  tax rate, and lets the user swap in their own commodity price. This teaches the concept
  hands-on.
</aside>

<h2 id="qaqc">Part 11: Sections 11 and 12 — QA/QC and Data Verification (Boring but Critical)</h2>

<p>After Bre-X, regulators became obsessive about sample integrity. Sections 11 and 12
describe how samples were collected, handled, transported, assayed, and verified.</p>

<p>What you are looking for:</p>

<ul>
  <li><strong>Chain of custody.</strong> Were samples sealed at the drill rig? Transported
  by company staff or independent couriers? Stored securely?</li>
  <li><strong>Insertion of standards, blanks, and duplicates</strong> at regular intervals
  (typically 1-in-20 standards, 1-in-20 blanks, 1-in-20 duplicates). This is the QA/QC
  program. If the report does not describe the program in detail, it is a red flag.</li>
  <li><strong>Lab used.</strong> Tier-one labs include SGS, ALS, Bureau Veritas, Intertek,
  Actlabs. Lesser-known labs can be credible too, but check.</li>
  <li><strong>QP site visit.</strong> The QP must physically visit the site. The report
  will state the date and duration. A multi-day site visit with core review is meaningful;
  a half-day fly-in is concerning for a material project.</li>
  <li><strong>Twin drill holes.</strong> These are holes drilled next to original holes to
  verify results. Their presence signals a serious program.</li>
</ul>

<p>This section is where salting, fraud, and sloppy work are (or are not) caught. It is
unglamorous reading, but it is where the foundation of every other number in the report
lives. A billion-dollar NPV built on contaminated assay data is worth zero.</p>

<h2 id="environmental">Part 12: Section 20 — Environment, Permitting, and Social Licence</h2>

<p>Increasingly, this is where projects die — not in the geology, but in the permitting
and community.</p>

<p>Check for:</p>

<ul>
  <li><strong>Stage of environmental baseline studies.</strong> Early-stage projects may
  have minimal baseline; PFS and FS require multiple seasons of hydrology, water quality,
  flora/fauna, and air studies.</li>
  <li><strong>Tailings management approach.</strong> Conventional tailings, dry-stack,
  paste backfill, in-pit deposition — each has cost and risk implications. After Brumadinho
  (2019) and Mount Polley (2014), tailings dam risk is a first-order concern for every
  institutional investor.</li>
  <li><strong>Permitting timeline.</strong> How many permits are required, at what levels
  (federal, state/provincial, municipal), and what is the realistic timeline? In Canada, a
  federal impact assessment can take 3–5 years; in Peru, social licence negotiations can
  take a decade.</li>
  <li><strong>Indigenous and community agreements.</strong> Are there signed Impact Benefit
  Agreements (IBAs) or community development agreements? The absence of a signed agreement
  is a major risk even if permitting is progressing.</li>
  <li><strong>Closure and reclamation cost.</strong> Is it adequately estimated and bonded?</li>
</ul>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Photo]</strong><br>
  A real tailings dam photo (or rendering) showing the scale, with annotations for
  embankment, spillway, starter dam, and water pond. Most retail investors have no mental
  model of what a tailings facility looks like.
</aside>

<h2 id="pea-pfs-fs">Part 13: PEA vs PFS vs FS — Knowing Where You Are on the Curve</h2>

<p>Understanding the economic study stage is essential because each stage has different
rules, different accuracy, and different investor implications.</p>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Comparison table — CRITICAL]</strong><br>
  Table with columns: Attribute | PEA | PFS | FS. Rows: Inferred resources allowed? (Yes /
  No / No); Capex accuracy (±30–50% / ±25% / ±15%); Opex accuracy (±25% / ±20% / ±10%);
  Engineering level (Conceptual / 10–30% / 40–70%+); Metallurgy (Bench-scale OK /
  Locked-cycle req. / Pilot plant often req.); Typical cost to produce ($0.5–$3M /
  $3–$15M / $15–$100M+); Bankable for debt? (No / Rarely / Yes); Stock reaction positive
  (Usually sharp run / Mild re-rate / Often sells off, news priced in). This is the
  reference table readers will screenshot.
</aside>

<p>A <strong>PEA</strong> is a marketing document with a technical wrapper. It is
designed to tell a story. The project has not been engineered in any meaningful sense.
PEA NPVs are almost always the highest NPV the project will ever report because they
include inferred ounces, use optimistic assumptions, and have not yet encountered
engineering reality.</p>

<p>A <strong>PFS</strong> (Pre-Feasibility Study) removes inferred ounces, applies real
engineering to the mine plan, and uses bench-scale-plus metallurgy. PFS NPVs typically
come in below the PEA NPV — sometimes dramatically so. This is where optimism meets
gravity.</p>

<p>An <strong>FS</strong> (Feasibility Study, sometimes "DFS" for Definitive) is bankable.
Engineering is 40–70%+ complete, contracts are in draft form, the tailings design is
final, permits are in hand or close, and metallurgy is validated at pilot scale. If banks
will lend against it, it's an FS.</p>

<p>The <strong>"PEA → PFS → FS fade"</strong> is real and well-documented. Academic
studies by professional bodies have shown that on average, FS NPVs come in 15–30% below
PEA NPVs for the same project, and actual operating economics after construction come in
another 10–20% below FS. Model this into your investment thinking.</p>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Chart]</strong><br>
  "PEA-to-Reality Fade" chart — aggregated data from 50+ projects showing PEA NPV / PFS
  NPV / FS NPV / Actual Year-3 Free Cash Flow, indexed to 100. Teaches the principle
  viscerally.
</aside>

<h2 id="analyst-toolkit">Part 14: The Analyst's Toolkit — What Professionals Calculate Themselves</h2>

<p>After reading the report, a professional analyst will produce their own numbers rather
than trust the company's. Here is what they typically compute:</p>

<ol>
  <li><strong>Independent NAV.</strong> Build a simple DCF using the company's production
  profile but the analyst's own commodity price, discount rate, and tax assumptions.
  Compare to the market cap.</li>
  <li><strong>P/NAV.</strong> Market cap divided by NAV. Developers trade at 0.3–0.7x
  P/NAV typically; producers 0.7–1.5x. Below 0.3x signals either a bargain or a
  market-perceived flaw.</li>
  <li><strong>EV per resource ounce.</strong> Enterprise value divided by contained
  ounces (often separated by category — EV per Measured+Indicated ounce is the most
  common comparable). Useful for cross-project comparables but limited by grade,
  jurisdiction, and stage differences.</li>
  <li><strong>Capex intensity.</strong> Initial capex per annual ounce of production.
  Low-capex-intensity projects (say, under $3,500/oz annual capacity for gold) are more
  likely to get built.</li>
  <li><strong>AISC margin.</strong> Commodity price minus AISC, times production — the
  cash profit engine of the mine.</li>
  <li><strong>Jurisdictional overlay.</strong> Apply a country risk discount. Tier 1
  (Canada, Australia, USA, Finland) = 0%. Tier 2 (Mexico, Peru, Chile, Brazil) = 10–20%.
  Tier 3 (DRC, Russia, Venezuela, parts of West Africa) = 30%+.</li>
</ol>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Downloadable]</strong><br>
  "The 43-101 Analyst Worksheet" — a one-page PDF/Excel with all of the above calculations
  pre-wired. Users paste in the numbers from Section 1 and Section 22, and the worksheet
  spits out P/NAV, EV/oz, capex intensity, AISC margin.
</aside>

<h2 id="red-flags">Part 15: The Red Flag Checklist</h2>

<p>After reading hundreds of 43-101s, patterns emerge. These are the signals that should
either disqualify a project or at least send you hunting for answers:</p>

<ul>
  <li>>50% inferred resources in a PEA or later-stage report.</li>
  <li>Commodity price assumption >10% above current spot without strong justification.</li>
  <li>Cut-off grade below industry norm to inflate resource tonnage.</li>
  <li>Single-lab assaying with no umpire lab check.</li>
  <li>Short QP site visit relative to project complexity.</li>
  <li>Internal QP only for a material project.</li>
  <li>Missing sensitivity tables for NPV.</li>
  <li>Refractory or complex metallurgy with bench-scale test work only.</li>
  <li>Strip ratio >10:1 not acknowledged as a cost risk.</li>
  <li>No signed community/IBA agreement in a jurisdiction where one is required.</li>
  <li>Large unexplained resource growth between consecutive technical reports.</li>
  <li>Contingency below 10%.</li>
  <li>Owner's costs missing or suspiciously low.</li>
  <li>Mine life &lt;7 years with no meaningful exploration upside.</li>
  <li>Tailings plan unclear or controversial.</li>
  <li>No independent review of the resource or economic model.</li>
</ul>

<p>Any one of these is not fatal. Three or more in the same report should make you put
the stock on your "no" pile until the next technical report addresses them.</p>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — One-page graphic]</strong><br>
  A "Red Flag Dashboard" — a scorecard where investors tick each flag, with a colour-coded
  total (0–3 green, 4–6 yellow, 7+ red). Shareable on social media.
</aside>

<h2 id="workflow">Part 16: Practical Workflow — How to Read Your First Report</h2>

<p>If you have never read a 43-101 cover-to-cover, here is a five-hour workflow that will
get you 80% of the professional signal:</p>

<p><strong>Hour 1 — Context.</strong> Read Section 1 (Summary) and Section 25
(Interpretation &amp; Conclusions). Write down the pitch and the risks in your own words.</p>

<p><strong>Hour 2 — The orebody.</strong> Read Section 14 (Resources) in detail. Build a
spreadsheet with tonnes, grade, contained metal by category, and cut-off sensitivity if
provided.</p>

<p><strong>Hour 3 — The economics.</strong> Read Sections 21 and 22. Pull out capex, opex,
AISC, NPV, IRR, payback, mine life, and every commodity price assumption. Compare
commodity prices to current spot.</p>

<p><strong>Hour 4 — The physical project.</strong> Read Sections 13, 16, and 17
(metallurgy, mining, processing). Understand the flowsheet. Identify any refractory,
high-dilution, or high-strip-ratio risk.</p>

<p><strong>Hour 5 — The risk layer.</strong> Read Section 20 (environment/permitting),
Sections 11–12 (QA/QC), and revisit Section 4 (property) for political context. Run the
red-flag checklist.</p>

<p>Then, and only then, read Sections 1 and 25 one more time. You will read them completely
differently the second time. That is the moment you have learned to read a 43-101.</p>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Flagship screencast/video — HIGH VALUE]</strong><br>
  A 25–35 minute screencast called "Reading a Real 43-101 — Start to Finish." Pick a
  mid-cap developer's PFS (publicly filed on SEDAR+), share the PDF on screen, and walk
  through the five-hour workflow in accelerated form. Pause on key tables and diagrams.
  End with the analyst's conclusion. This would be the flagship asset of the entire guide.
</aside>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Supporting video 1]</strong><br>
  A 5-minute "How to find every 43-101 ever filed" tutorial — walking through SEDAR+
  search filters, then showing how to download technical reports. Most retail investors
  don't know SEDAR+ exists.
</aside>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Supporting video 2]</strong><br>
  An "Interview with a QP" video — a short interview with a practicing QP (consulting
  geologist or engineer) discussing what <em>they</em> wish investors understood about
  technical reports. High credibility content.
</aside>

<h2 id="where-to-find">Part 17: Where to Find 43-101 Reports</h2>

<p>Every filed technical report is public. Here is where to look:</p>

<ul>
  <li><strong>SEDAR+</strong> (sedarplus.ca) — the Canadian securities regulator's filing
  system. Filter by company, then "Technical Report" document type. Free.</li>
  <li><strong>Company websites</strong> — most post the latest technical report under
  Investors → Technical Reports.</li>
  <li><strong>SEC EDGAR</strong> (sec.gov) — for dually-listed companies that file with
  the SEC as well (they'll file SK-1300 reports there, which are similar).</li>
</ul>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Screenshot walk-through]</strong><br>
  Step-by-step annotated screenshots of the SEDAR+ filing search — company name entry,
  filter selection, document list, download. Five screenshots in a carousel.
</aside>

<p>A pro tip: compare the <strong>current</strong> technical report to the
<strong>previous</strong> technical report (if one exists). Changes in cut-off grade,
mining method, resource estimation methodology, or commodity price assumption between
reports tell you a lot about what the company is hiding or pivoting from.</p>

<h2 id="mental-model">Part 18: The Final Mental Model</h2>

<p>After reading thousands of technical reports across a career, experienced mining
investors carry a simple mental model:</p>

<blockquote>
  <p>A 43-101 is a story about converting rocks into cash. Your job is to check every
  step of the conversion chain: are the rocks really there (resource), can we get them
  out (mining), can we extract the metal (metallurgy), can we sell it for more than it
  cost (economics), and can we actually build this thing in this jurisdiction (permitting
  and capex)?</p>
</blockquote>

<p>Every section of the report maps to one link in that chain. A project is only as
strong as its weakest link. Most failed mining projects failed at one specific link —
tailings permitting at Pebble, refractory metallurgy at countless gold juniors, community
opposition at Conga, cost overruns at virtually every megaproject built in the last 20
years, grade shortfall at dozens of producers post-startup.</p>

<p>If you learn to read a 43-101, you can find the weakest link before the market does.
That is the analyst's edge.</p>

<aside class="editor-note">
  <strong>[EDITOR PLACEHOLDER — Closing graphic]</strong><br>
  A clean, horizontal "Value Chain" infographic — Exploration → Resource → Engineering →
  Permitting → Finance → Construction → Operation → Cash — with the percentage of juniors
  that die at each stage. Sobering and clarifying.
</aside>

<h2 id="closing">Closing Note</h2>

<p>Learning to read 43-101 reports properly takes time — expect the first three or four
reports to feel overwhelming. By the fifth or sixth, patterns emerge. By the tenth, you
will be faster than 95% of retail investors and competitive with many junior analysts at
sell-side shops.</p>

<p>The payoff is enormous. Mining is one of the few asset classes where the amateur and
the professional are reading the same document, and where genuine disclosure rules mean
the truth is usually in the report — just buried in Section 14 or hidden in the footnotes
of Section 22. The investors who do the work outperform the ones who read headlines. That
has been true since Bre-X, and it will be true for as long as humans dig metal out of the
ground.</p>

<p>Bookmark this guide. Download a real 43-101 this weekend. Walk through the five-hour
workflow once. You will never look at a mining press release the same way again.</p>

<h2 id="asset-index">Appendix: Suggested Visual Assets Index (Editorial Reference)</h2>

<p>A consolidated index of every placeholder above, for the production team. Each entry
corresponds to an inline <code>&lt;aside class="editor-note"&gt;</code> block in the body
and should be replaced in place once the asset is produced.</p>

<ol>
  <li>Hero split-screen image (drill core + spreadsheet + report cover) — top of post.</li>
  <li>Comparable global disclosure regimes table — Part 1.</li>
  <li>Annotated QP certificate page — Part 2.</li>
  <li>"43-101 Report Anatomy" 27-section infographic — Part 3. <strong>Critical.</strong></li>
  <li>"Analyst's Reading Path" circular diagram — Part 4.</li>
  <li>"Project Snapshot Worksheet" downloadable — Part 5.</li>
  <li>CIM Reporting Pyramid diagram — Part 6. <strong>Critical.</strong></li>
  <li>Resource cut-off sensitivity table template — Part 6.</li>
  <li>Annotated 3D block model image — Part 6.</li>
  <li>Process flow diagram with recovery losses — Part 8.</li>
  <li>Flotation / CIL plant photo — Part 8.</li>
  <li>Open-pit + underground cross-section diagrams — Part 9.</li>
  <li>Global AISC cost curve chart — Part 10.</li>
  <li>NPV Sensitivity Tornado Chart — Part 10. <strong>Critical.</strong></li>
  <li>Downloadable NPV recalculator spreadsheet — Part 10.</li>
  <li>Tailings dam photo (annotated) — Part 12.</li>
  <li>PEA vs PFS vs FS comparison table — Part 13. <strong>Critical.</strong></li>
  <li>"PEA-to-Reality Fade" historical chart — Part 13.</li>
  <li>"43-101 Analyst Worksheet" downloadable — Part 14. <strong>Critical.</strong></li>
  <li>"Red Flag Dashboard" one-page scorecard — Part 15.</li>
  <li>25–35 min flagship screencast walking through a real PFS — Part 16.</li>
  <li>5-min "How to use SEDAR+" tutorial video — Part 17.</li>
  <li>QP interview video — Part 16.</li>
  <li>SEDAR+ step-by-step screenshot walk-through — Part 17.</li>
  <li>Final "Rocks to Cash" value chain infographic — Part 18.</li>
</ol>
""".strip()


GUIDE_DATA = {
    "title": "How to Read an NI 43-101 Report Like a Professional Mining Analyst",
    "pillar_slug": "investing-guides",
    "meta_title": "How to Read an NI 43-101: A Complete Investor's Guide",
    "meta_description": (
        "Learn to read NI 43-101 technical reports the way a professional mining analyst "
        "does. Section-by-section guide, red flags, and a 5-hour workflow for any report."
    ),
    "excerpt": (
        "The NI 43-101 technical report is the most important disclosure document in "
        "junior mining — and the one most retail investors skip. This long-form guide "
        "walks through the 27-section anatomy, the analyst's reading order, the key "
        "metrics to extract, the red flags to watch for, and a 5-hour workflow that "
        "gets you 80% of the professional signal on any report."
    ),
    "answer_capsule": (
        "An NI 43-101 is the standardized technical report every TSX / TSX-V / CSE "
        "mining issuer must file, written under the supervision of a Qualified Person "
        "and organized in 27 standard sections. Professionals read it in a specific "
        "non-linear order — Summary, then Conclusions, then Resources, then Economics, "
        "then Metallurgy — extracting tonnes, grade, cut-off, NPV, IRR, AISC, and "
        "commodity price assumptions, and cross-checking each number against the "
        "supporting detail. The goal is to identify the weakest link in the rocks-to-cash "
        "conversion chain before the market does."
    ),
    "key_takeaways": [
        "NI 43-101 is a disclosure standard, not a quality standard — compliant reports can still describe bad projects",
        "The Qualified Person (QP) and their firm tell you how much weight to put on the numbers",
        "The 27 sections follow a fixed structure — know the map and you can navigate any report in minutes",
        "Read in the analyst's order: Summary → Conclusions → Resources → Economics → Metallurgy → Mining",
        "Resource classification (Inferred, Indicated, Measured) governs what can and cannot be used in a reserve",
        "Cut-off grade and commodity price assumption are the single biggest levers in the whole document",
        "PEA NPVs fade into PFS NPVs into FS NPVs — 15–30% downward drift is the historical norm",
        "A 5-hour structured workflow gets a retail investor 80% of the professional signal on any report",
    ],
    "faq_items": [
        {
            "question": "What does NI 43-101 actually stand for?",
            "answer": (
                "National Instrument 43-101 — Standards of Disclosure for Mineral "
                "Projects. It is a Canadian securities rule introduced in 2001 after "
                "the Bre-X scandal, governing how TSX, TSX-V, and CSE-listed mining "
                "companies must disclose technical information. It mandates Qualified "
                "Person sign-off, publicly filed technical reports, and CIM Definition "
                "Standards for resource and reserve classification."
            ),
        },
        {
            "question": "Is NI 43-101 the same as JORC or SK-1300?",
            "answer": (
                "No, but they serve the same purpose under different jurisdictions. "
                "JORC is the Australian equivalent, SAMREC is South African, and "
                "SK-1300 is the US SEC equivalent adopted in 2021. All four regimes "
                "align on CIM-style resource and reserve categories, but differ on "
                "procedural requirements, QP definitions, and what is allowed in "
                "economic studies. Dual-listed companies often file reports under "
                "multiple standards."
            ),
        },
        {
            "question": "What's the difference between a resource and a reserve?",
            "answer": (
                "A mineral resource is a concentration of metal in the ground with "
                "reasonable prospects for eventual economic extraction, classified as "
                "Inferred, Indicated, or Measured based on geological confidence. A "
                "mineral reserve is the subset of that resource that has been "
                "demonstrated economic after applying modifying factors — mining "
                "method, metallurgy, costs, prices, permits. Only Indicated and "
                "Measured resources can be converted to Probable and Proven reserves. "
                "Inferred resources can never be converted to reserves."
            ),
        },
        {
            "question": "Which 43-101 sections should I read first?",
            "answer": (
                "Professional analysts read non-linearly. Start with Section 1 "
                "(Summary) for the pitch, then Section 25 (Interpretation and "
                "Conclusions) for the QP's own risk list, then Section 14 (Resources), "
                "then Section 22 (Economic Analysis), then Section 21 (Capex / Opex), "
                "then Sections 13 and 17 (Metallurgy and Recovery), then Section 16 "
                "(Mining Methods), then Sections 11–12 (QA/QC), and finally Section 20 "
                "(Environment / Permitting)."
            ),
        },
        {
            "question": "What is AISC and why does it matter?",
            "answer": (
                "All-In Sustaining Cost per ounce includes cash operating costs, "
                "sustaining capital, reclamation, and allocated corporate G&A. It is "
                "the most comprehensive cost metric for a gold mine and the one that "
                "matters for margin analysis. A gold project with AISC under $1,200/oz "
                "is healthy at current prices; above $1,600/oz margins are thin and the "
                "project is vulnerable to any gold price correction."
            ),
        },
        {
            "question": "What's the difference between a PEA, PFS, and FS?",
            "answer": (
                "A PEA (Preliminary Economic Assessment) is conceptual, allows Inferred "
                "resources, and has ±30–50% capex accuracy. A PFS (Pre-Feasibility "
                "Study) uses engineering and removes Inferred resources, with ±25% "
                "capex accuracy. An FS (Feasibility Study, sometimes DFS) is bankable, "
                "with 40–70%+ engineering completion and ±15% capex accuracy. PEA NPVs "
                "typically fade 15–30% into PFS and another 10–20% into FS."
            ),
        },
        {
            "question": "What are the biggest red flags in a 43-101?",
            "answer": (
                "Over 50% inferred resources in a PEA or later stage; commodity price "
                "assumption more than 10% above spot; cut-off grade far below industry "
                "norm; missing NPV sensitivity tables; refractory metallurgy with only "
                "bench-scale test work; contingency under 10%; owner's costs missing; "
                "no independent review of the resource estimate; and large unexplained "
                "resource growth between consecutive technical reports."
            ),
        },
        {
            "question": "Where can I actually download 43-101 reports?",
            "answer": (
                "SEDAR+ at sedarplus.ca is the free Canadian securities filing system "
                "where every NI 43-101 technical report is publicly available. Filter "
                "by company and document type = Technical Report. Most companies also "
                "host the latest report on their own Investors page. Dual-listed "
                "companies file SK-1300 versions with the SEC on EDGAR."
            ),
        },
    ],
    "body": NI43101_GUIDE_BODY,
}


def seed_ni43101_guide(apps, schema_editor):
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
        status="draft",
        is_premium=False,
        published_at=None,
        meta_title=GUIDE_DATA["meta_title"],
        meta_description=GUIDE_DATA["meta_description"],
    )


def reverse_seed(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    Post.objects.filter(title=GUIDE_DATA["title"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0013_silver_guide_tables_and_draft"),
    ]
    operations = [
        migrations.RunPython(seed_ni43101_guide, reverse_seed),
    ]
