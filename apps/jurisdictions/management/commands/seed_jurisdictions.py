"""
Seed initial Jurisdiction risk assessments.

Idempotent — uses update_or_create keyed on (country, name).

Usage:
    python manage.py seed_jurisdictions
    python manage.py seed_jurisdictions --reset    # delete all first

Scoring inputs draw on the Fraser Institute Annual Survey of Mining Companies
(most recent), the World Bank Worldwide Governance Indicators, and recent
permitting / fiscal news. Re-run after each Fraser release.
"""
from datetime import date

from django.core.management.base import BaseCommand

from apps.jurisdictions.models import Jurisdiction, RegionType


# Scores: 1 = worst (most risk), 5 = best (least risk).
# Order: permitting, fiscal, political, infrastructure, community
SEED = [
    # ──────────── Canada ────────────
    {
        "name": "Saskatchewan", "country": "Canada", "country_code": "CA", "region_type": RegionType.PROVINCE,
        "scores": (5, 5, 5, 4, 4),
        "notes": {
            "permitting":     "Streamlined permitting; provincial mining ministry consistently ranked top globally.",
            "fiscal":         "Stable royalty regime; competitive corporate tax with Saskatchewan's industrial profile.",
            "political":      "Predictable conservative government; pro-resource policy continuity for over a decade.",
            "infrastructure": "Highway and rail access to most camps; some northern projects fly-in.",
            "community":      "Established consultation framework with First Nations; ongoing duty-to-consult disputes do occur.",
        },
        "summary": (
            "Saskatchewan is consistently the highest-scoring mining jurisdiction in the world on the Fraser "
            "Institute survey and is the gold standard for North American permitting predictability. The "
            "province hosts the world's premier uranium camp (Athabasca Basin), significant gold districts "
            "in the Trans-Hudson belt, and an emerging copper-gold scene. Royalty and tax regimes have been "
            "stable for decades and political risk is effectively zero — successive governments treat mining "
            "as core economic policy.\n\n"
            "The main constraints are remoteness for northern projects (no all-season road to several Athabasca "
            "deposits) and the same Indigenous consultation obligations that apply across Canada. Both are "
            "manageable with adequate planning."
        ),
    },
    {
        "name": "Quebec", "country": "Canada", "country_code": "CA", "region_type": RegionType.PROVINCE,
        "scores": (4, 4, 5, 5, 3),
        "notes": {
            "permitting":     "Strong technical staff at MERN; timelines can stretch on contested projects.",
            "fiscal":         "Plan Nord and Plan Quebecor have offered tax credits; recent royalty review modest.",
            "political":      "Stable Quebec governance; nationalisation rhetoric historically a non-issue for mining.",
            "infrastructure": "Hydro power abundant; rail and Route du Nord access to most camps.",
            "community":      "Significant First Nation and Innu consultation requirements; some camps blocked by community opposition.",
        },
        "summary": (
            "Quebec offers a rare combination of low-cost hydroelectric power, deep technical depth in the "
            "provincial regulator, and one of the most prolific gold belts in the world (Abitibi). Capital "
            "intensity is among the lowest in North America thanks to power costs and infrastructure access. "
            "Royalty and tax regimes are competitive and stable.\n\n"
            "The friction points are Indigenous consultation — particularly with Cree, Innu, and Algonquin "
            "First Nations — and recent legislative tightening around protected areas. Projects in active "
            "consultation generally proceed but on timelines longer than the headline permitting calendar."
        ),
    },
    {
        "name": "Ontario", "country": "Canada", "country_code": "CA", "region_type": RegionType.PROVINCE,
        "scores": (3, 4, 5, 5, 3),
        "notes": {
            "permitting":     "Provincial permitting capable but slow; Ring of Fire still in negotiation after 15+ years.",
            "fiscal":         "Stable mining tax (Ontario Mining Tax); no surprise changes.",
            "political":      "Stable; Ford government broadly pro-mining particularly for critical minerals.",
            "infrastructure": "Strong in southern/Sudbury basin; Ring of Fire access remains the unsolved problem.",
            "community":      "Treaty 9 and Robinson-Huron settlements are active; meaningful consultation costs.",
        },
        "summary": (
            "Ontario hosts world-class gold (Red Lake, Hemlo, Timmins), nickel-copper-PGE (Sudbury), and "
            "an emerging critical-minerals scene around the Ring of Fire chromite-nickel district. The "
            "fiscal regime is stable and the province has well-developed mining infrastructure outside the "
            "Far North.\n\n"
            "Permitting predictability is the weakness. The Ring of Fire has been 'imminent' for over a "
            "decade, and northern projects routinely face multi-year delays around access roads, environmental "
            "assessments, and Treaty 9 consultations. Established camps (Timmins, Red Lake) operate with "
            "standard Canadian timelines; greenfield projects in the Far North do not."
        ),
    },
    {
        "name": "British Columbia", "country": "Canada", "country_code": "CA", "region_type": RegionType.PROVINCE,
        "scores": (2, 3, 4, 4, 2),
        "notes": {
            "permitting":     "Among the slowest in Canada; reviews of major projects regularly exceed 5 years.",
            "fiscal":         "Mineral tax stable; provincial rates competitive but BC adds carbon tax exposure.",
            "political":      "NDP government has pursued tighter environmental and Indigenous rights legislation.",
            "infrastructure": "Strong port access (Stewart, Prince Rupert); northern grid expansion ongoing.",
            "community":      "DRIPA implementation has materially raised consultation costs; FN consent increasingly de-facto requirement.",
        },
        "summary": (
            "British Columbia hosts the Golden Triangle, the Toodoggone, and significant copper-gold "
            "porphyry endowment. The province's geological prospectivity is exceptional but it has become "
            "one of the more challenging Canadian jurisdictions to permit and operate in over the past "
            "decade.\n\n"
            "BC's adoption of the Declaration on the Rights of Indigenous Peoples Act (DRIPA) in 2019 has "
            "in practice raised the threshold for project approval — First Nations consent is now a "
            "near-prerequisite rather than a 'duty to consult' standard. Combined with environmental "
            "assessment timelines that regularly exceed five years, the jurisdiction works for well-funded "
            "developers with deep relationships and patient capital, and is hostile territory for "
            "underfinanced juniors."
        ),
    },
    {
        "name": "Yukon", "country": "Canada", "country_code": "CA", "region_type": RegionType.TERRITORY,
        "scores": (4, 4, 5, 2, 3),
        "notes": {
            "permitting":     "YESAB process is rigorous but predictable; clear timelines.",
            "fiscal":         "Federal-territorial royalty framework competitive and stable.",
            "political":      "Stable territorial governance; mining is core to economic policy.",
            "infrastructure": "Highway access to many districts but power and port logistics challenging.",
            "community":      "Final and Self-Government Agreements with most First Nations provide clarity but require active participation.",
        },
        "summary": (
            "Yukon is one of the more underrated Canadian mining jurisdictions. The Final Agreements signed "
            "with most Yukon First Nations provide a clearer consultation framework than exists in much of "
            "Canada — the rules of engagement are written down — and the territorial government has been "
            "consistently pro-mining for decades. White Gold, Coffee, and the Selwyn Basin host significant "
            "endowment.\n\n"
            "The binding constraint is infrastructure. Most projects require diesel power generation or "
            "new transmission lines, and several major districts have only seasonal road access. Capital "
            "intensity for greenfield development is therefore high relative to southern Canadian provinces."
        ),
    },
    {
        "name": "Northwest Territories", "country": "Canada", "country_code": "CA", "region_type": RegionType.TERRITORY,
        "scores": (3, 4, 5, 1, 3),
        "notes": {
            "permitting":     "Mackenzie Valley Resource Management Act framework; thorough but timelines vary.",
            "fiscal":         "Stable; competitive northern incentives apply.",
            "political":      "Stable territorial government; mining is the largest private-sector employer.",
            "infrastructure": "Most projects winter-road access only; ice-road logistics are seasonal and expensive.",
            "community":      "Multiple Land Claim agreements provide structure; Indigenous capacity for participation varies.",
        },
        "summary": (
            "The Northwest Territories has produced four world-class diamond mines and a long history of "
            "gold and base-metal production. The political and fiscal climate is stable, and modern Land "
            "Claim agreements give certainty over consultation processes.\n\n"
            "Infrastructure is the binding constraint and a near-monopoly on capital intensity discounts. "
            "Projects in the central NWT depend on winter ice roads from Yellowknife, with construction "
            "windows of only 8–10 weeks. Diesel power generation is the norm. The recent closures of the "
            "diamond operations have raised questions about whether the GNWT can sustain a critical mass "
            "of mining capacity through the next development cycle."
        ),
    },
    {
        "name": "Nunavut", "country": "Canada", "country_code": "CA", "region_type": RegionType.TERRITORY,
        "scores": (3, 4, 5, 1, 3),
        "notes": {
            "permitting":     "Nunavut Impact Review Board process is robust; can be lengthy on contested projects.",
            "fiscal":         "Stable royalty and tax framework.",
            "political":      "Stable territorial government; the Nunavut Land Claim governs most decisions.",
            "infrastructure": "All projects fly-in or barge-in; no road or rail access whatsoever.",
            "community":      "Inuit Impact and Benefit Agreements (IIBAs) required; framework established but case-by-case.",
        },
        "summary": (
            "Nunavut hosts the Meadowbank, Meliadine, and Hope Bay districts and has been a meaningful gold "
            "and base-metal producer for over a decade. The Nunavut Land Claim Agreement provides a clear "
            "framework for Inuit participation through IIBAs, and political risk is effectively zero.\n\n"
            "The cost of operating in Nunavut is extreme. Every input — fuel, supplies, food, labour — must "
            "fly or barge in during a short shipping window. Workforce attraction and retention are persistent "
            "challenges. Junior explorers without major-partner backing struggle to fund the multi-tens-of-"
            "millions required to test even a single target."
        ),
    },
    {
        "name": "Newfoundland and Labrador", "country": "Canada", "country_code": "CA", "region_type": RegionType.PROVINCE,
        "scores": (4, 4, 5, 3, 4),
        "notes": {
            "permitting":     "Provincial regulator is responsive; precedent exists for fast-tracked exploration.",
            "fiscal":         "Stable royalty regime; competitive corporate rates.",
            "political":      "Stable; mining is bipartisan economic priority.",
            "infrastructure": "Road and port access in most populated areas; Labrador interior is remote.",
            "community":      "Innu Nation and Nunatsiavut consultation generally constructive; established frameworks.",
        },
        "summary": (
            "Newfoundland and Labrador has emerged as one of Atlantic Canada's most active gold exploration "
            "jurisdictions, particularly along the Central Newfoundland gold belt. The province's regulatory "
            "framework is responsive, fiscal terms are stable, and political risk is minimal.\n\n"
            "Labrador's interior shares the infrastructure challenges of all northern Canadian projects, but "
            "Newfoundland-island projects benefit from highway access, electrical grid availability, and "
            "established service centres. Indigenous consultation processes with the Innu Nation and "
            "Nunatsiavut Government are well-established."
        ),
    },

    # ──────────── United States ────────────
    {
        "name": "Nevada", "country": "United States", "country_code": "US", "region_type": RegionType.STATE,
        "scores": (4, 5, 5, 5, 4),
        "notes": {
            "permitting":     "Federal BLM lead; state cooperation strong; timelines competitive globally.",
            "fiscal":         "Net-proceeds-of-minerals tax stable; competitive federal rates.",
            "political":      "Bipartisan support for mining; rule of law uncontested.",
            "infrastructure": "Excellent highways, rail, power; established mining service centres.",
            "community":      "Western Shoshone consultation processes; Tribal opposition exists at specific sites but rare.",
        },
        "summary": (
            "Nevada is the global benchmark for mining jurisdiction quality. The state hosts the Carlin and "
            "Cortez gold trends, world-class porphyry districts, and an emerging lithium scene around Clayton "
            "Valley and Thacker Pass. Permitting is predictable, the workforce is deep, infrastructure is "
            "excellent, and the state's Net Proceeds of Minerals tax has been stable for decades.\n\n"
            "Federal land issues — most Nevada mining occurs on BLM ground — introduce some procedural "
            "complexity that pure state jurisdictions avoid, but the BLM's Nevada offices are among the "
            "most experienced in the federal system. Junior capital flows here disproportionately because "
            "every other input is so well-handled."
        ),
    },
    {
        "name": "Alaska", "country": "United States", "country_code": "US", "region_type": RegionType.STATE,
        "scores": (3, 4, 5, 1, 3),
        "notes": {
            "permitting":     "State permits straightforward; federal NEPA reviews can stretch dramatically.",
            "fiscal":         "Mining licence tax and royalty competitive; production tax can be high.",
            "political":      "Stable but Pebble Mine veto demonstrated EPA can block projects post-permit.",
            "infrastructure": "Most projects fly-in or via shoulder-season barge; limited road and grid.",
            "community":      "Native Corporation framework is constructive; specific anti-mining campaigns at certain projects.",
        },
        "summary": (
            "Alaska has world-class endowment — Donlin, Pebble, Red Dog, Greens Creek — and a state political "
            "framework that broadly supports mining. The Alaska Native Claims Settlement Act creates a "
            "structurally constructive framework where Native Corporations are often partners rather than "
            "opponents.\n\n"
            "The headline risk is federal permitting unpredictability. The EPA's Pebble Mine veto under the "
            "Clean Water Act in 2023 — after 15+ years of state-level work — demonstrates that even fully "
            "state-permitted projects face residual federal-level political risk. Infrastructure is the other "
            "binding constraint: most projects require dedicated road, port, or pipeline build-out adding "
            "hundreds of millions to capex."
        ),
    },
    {
        "name": "Arizona", "country": "United States", "country_code": "US", "region_type": RegionType.STATE,
        "scores": (3, 5, 5, 5, 3),
        "notes": {
            "permitting":     "State permits efficient; federal land transfers and NEPA can be slow (Resolution).",
            "fiscal":         "Stable competitive corporate and severance rates.",
            "political":      "Stable; broadly pro-mining at state level.",
            "infrastructure": "Excellent — highways, rail, grid, established copper service centres.",
            "community":      "Apache and other Tribal opposition at specific sites (Oak Flat); broader social licence intact.",
        },
        "summary": (
            "Arizona is a Tier-1 copper jurisdiction with deep technical workforce, established infrastructure, "
            "and a fiscally stable state government. The southern Arizona porphyry belt is among the most "
            "endowed in the world.\n\n"
            "Resolution Copper, after 25+ years and pending land-transfer litigation, illustrates that even "
            "in Arizona federal lands and Apache Tribal opposition can stall world-class deposits indefinitely. "
            "Brownfield expansions and projects on private land proceed with normal North American timelines."
        ),
    },
    {
        "name": "Utah", "country": "United States", "country_code": "US", "region_type": RegionType.STATE,
        "scores": (4, 5, 5, 4, 4),
        "notes": {
            "permitting":     "State permitting efficient and well-resourced.",
            "fiscal":         "Stable competitive rates.",
            "political":      "Stable; conservative pro-business.",
            "infrastructure": "Strong; copper and base-metal services centred on Salt Lake.",
            "community":      "Limited Indigenous overlay relative to other western states; constructive framework.",
        },
        "summary": (
            "Utah is one of the most underrated US mining jurisdictions. The state government is "
            "consistently pro-business, permitting timelines are competitive, and the Salt Lake City "
            "industrial base provides strong service infrastructure. Bingham Canyon (Rio Tinto) anchors "
            "a long-established copper district and meaningful precious-metal endowment exists in the Tintic "
            "and Wasatch ranges."
        ),
    },
    {
        "name": "Idaho", "country": "United States", "country_code": "US", "region_type": RegionType.STATE,
        "scores": (3, 4, 5, 4, 4),
        "notes": {
            "permitting":     "State permits straightforward; federal reviews on USFS land can be lengthy.",
            "fiscal":         "Stable; competitive severance and corporate rates.",
            "political":      "Stable; broadly supportive at state level.",
            "infrastructure": "Adequate; northern Idaho service centres; some districts remote.",
            "community":      "Nez Perce and other Tribes engaged on specific projects; framework workable.",
        },
        "summary": (
            "Idaho hosts the Silver Valley (one of the largest historical silver districts in the world) and "
            "an emerging cobalt-gold scene in the Salmon-Challis region. State politics are stable and "
            "pro-mining. Federal USFS land permitting can stretch timelines but is workable with experienced "
            "operators."
        ),
    },

    # ──────────── Australia ────────────
    {
        "name": "Western Australia", "country": "Australia", "country_code": "AU", "region_type": RegionType.STATE,
        "scores": (4, 4, 5, 4, 4),
        "notes": {
            "permitting":     "DMIRS process well-resourced and predictable.",
            "fiscal":         "Royalty regime stable; minor adjustments rather than structural changes.",
            "political":      "Stable; mining is core to state economy and politics.",
            "infrastructure": "Excellent in the Pilbara and Kalgoorlie-Boulder; remote in northern Goldfields.",
            "community":      "Native Title processes are well-established but the 2020 Juukan Gorge incident has tightened expectations.",
        },
        "summary": (
            "Western Australia is the global heartland of listed junior mining capital alongside Vancouver "
            "and Toronto. The Pilbara, Eastern Goldfields, and Yilgarn craton host iron ore, gold, lithium, "
            "and base-metal endowment at scale. State permitting is professional and predictable, fiscal "
            "terms are stable, and the political environment treats mining as core economic policy.\n\n"
            "Native Title and Aboriginal Heritage Act processes are well-defined and add planning time but "
            "rarely block well-run projects. The 2020 Juukan Gorge incident and the subsequent legislative "
            "tightening have raised heritage standards across the state."
        ),
    },
    {
        "name": "Queensland", "country": "Australia", "country_code": "AU", "region_type": RegionType.STATE,
        "scores": (4, 3, 5, 4, 4),
        "notes": {
            "permitting":     "Capable state regulator; coal projects face higher scrutiny than metals.",
            "fiscal":         "Royalty changes in 2022 raised coal rates significantly; metals stable.",
            "political":      "Stable but Labor government has been less mining-friendly than past LNP terms.",
            "infrastructure": "Good in coal and base-metal regions; northern Queensland less developed.",
            "community":      "Native Title framework operational; community consultation costs typical of Australia.",
        },
        "summary": (
            "Queensland hosts Mount Isa, Cannington, and significant copper-gold-base-metal endowment. "
            "Infrastructure is strong in the established mining regions and the workforce is deep.\n\n"
            "The 2022 coal royalty increase under the previous Labor government — among the largest "
            "single-jurisdiction royalty hikes in recent memory — illustrated that fiscal stability "
            "in Queensland is not absolute. Metals royalties have not seen comparable changes but the "
            "precedent is now in the rearview mirror."
        ),
    },
    {
        "name": "New South Wales", "country": "Australia", "country_code": "AU", "region_type": RegionType.STATE,
        "scores": (3, 3, 5, 5, 3),
        "notes": {
            "permitting":     "Process well-resourced but increasingly slow on greenfield projects.",
            "fiscal":         "Royalty changes proposed periodically; coal levy in place.",
            "political":      "Stable; Labor state government less mining-supportive than LNP-era.",
            "infrastructure": "Excellent — Hunter Valley, Sydney basin, established rail and ports.",
            "community":      "Native Title and heritage requirements meaningful; specific project blockages in metro proximity.",
        },
        "summary": (
            "NSW is a long-established mining jurisdiction with excellent infrastructure and deep workforce. "
            "Permitting timelines have stretched on greenfield projects under the current Labor state "
            "government, and fiscal predictability is somewhat lower than WA."
        ),
    },
    {
        "name": "Northern Territory", "country": "Australia", "country_code": "AU", "region_type": RegionType.TERRITORY,
        "scores": (4, 4, 5, 2, 3),
        "notes": {
            "permitting":     "Streamlined process; Territory government actively supports mining.",
            "fiscal":         "Stable; competitive royalty regime.",
            "political":      "Stable; mining-supportive across both major parties.",
            "infrastructure": "Limited outside Darwin/Katherine; many projects fly-in.",
            "community":      "Aboriginal Land Rights Act creates clear framework; consent required for sacred-site work.",
        },
        "summary": (
            "The Northern Territory is one of the most underrated Australian mining jurisdictions. The "
            "Territory government actively courts mining investment, fiscal terms are stable, and the "
            "Aboriginal Land Rights Act provides a clearer consent framework than Native Title. The McArthur "
            "River, Tanami, and Pine Creek districts are well-established.\n\n"
            "Infrastructure is the binding constraint outside the Darwin-Katherine corridor. Most northern "
            "and central NT projects are fly-in or rely on dedicated road build-out."
        ),
    },

    # ──────────── Mexico (sub-national) ────────────
    # Federal context applies to all states: 2023 open-pit prohibition, suspension
    # of new concessions, tightened water rules, ongoing royalty creep. State-level
    # variation is driven mainly by security, infrastructure, and community dynamics.
    {
        "name": "Sonora", "country": "Mexico", "country_code": "MX", "region_type": RegionType.STATE,
        "scores": (2, 2, 3, 5, 3),
        "notes": {
            "permitting":     "Federal open-pit ban applies; state cooperation historically constructive on existing operations.",
            "fiscal":         "Federal royalty regime; no state-level surprises in recent cycles.",
            "political":      "Mining historically core to state economy; Morena state government less openly hostile than federal.",
            "infrastructure": "Excellent — US border, deep highway and rail network, established service industry around Hermosillo.",
            "community":      "Mostly constructive; Yaqui and other indigenous consultation issues at specific sites.",
        },
        "summary": (
            "Sonora is Mexico's largest mining state by output and hosts the country's most significant "
            "copper, gold, and silver districts (Cananea, Buenavista, La Herradura, Mulatos, Pinos Altos). "
            "The state borders Arizona and benefits from excellent transport, power, and labour-market "
            "infrastructure. Mining is historically central to state identity and politics, and state-level "
            "treatment of operating mines has been more constructive than the federal rhetoric suggests.\n\n"
            "The federal open-pit moratorium and concession freeze still apply — Sonora cannot insulate "
            "developers from those constraints — but for operating mines and projects already permitted, "
            "Sonora is the lowest-friction Mexican jurisdiction. Cartel violence has crept north over the "
            "past five years but remains less acute than in Sinaloa or Guerrero."
        ),
    },
    {
        "name": "Zacatecas", "country": "Mexico", "country_code": "MX", "region_type": RegionType.STATE,
        "scores": (2, 2, 2, 4, 3),
        "notes": {
            "permitting":     "Federal regime applies; state-level cooperation variable.",
            "fiscal":         "Federal royalty + standard state taxes; no major state surprises.",
            "political":      "Morena state government has tilted anti-mining; periodic friction with operating producers.",
            "infrastructure": "Mature highway and rail network; established mining service centres around Fresnillo.",
            "community":      "Generally constructive in established districts; ejido land negotiations standard.",
        },
        "summary": (
            "Zacatecas is the historic heart of Mexican silver and remains the country's largest silver "
            "producer (Fresnillo, Saucito, Peñasquito sits near the Zacatecas-Durango border). The state's "
            "mining workforce and service industry are deep, and infrastructure is well-developed across "
            "the silver belt.\n\n"
            "The current Morena-led state government has been more rhetorically hostile to mining than its "
            "predecessors and there have been specific frictions around water use and tax disputes with "
            "major producers. The federal-policy ceiling is the binding constraint on greenfield development."
        ),
    },
    {
        "name": "Chihuahua", "country": "Mexico", "country_code": "MX", "region_type": RegionType.STATE,
        "scores": (2, 2, 3, 4, 3),
        "notes": {
            "permitting":     "Federal regime applies; state administration generally pragmatic.",
            "fiscal":         "Federal royalty regime; no notable state-level surprises.",
            "political":      "Conservative state government less anti-mining than federal; relative continuity.",
            "infrastructure": "Strong — US border access, rail, mature mining services.",
            "community":      "Tarahumara consultation in Sierra Madre; ejido frameworks standard elsewhere.",
        },
        "summary": (
            "Chihuahua is one of Mexico's largest silver producers and hosts significant gold endowment "
            "(Palmarejo, Pinos Altos, La Cienega). The state borders Texas and New Mexico, with "
            "well-developed transport and power infrastructure. Successive PAN-led state governments have "
            "been more pragmatically pro-mining than the federal Morena administration.\n\n"
            "Sierra Madre operations face Tarahumara indigenous consultation requirements and elevated "
            "cartel-related security overhead in remote districts. Operations in the more accessible "
            "central and northern parts of the state run with normal North American operating profiles."
        ),
    },
    {
        "name": "Durango", "country": "Mexico", "country_code": "MX", "region_type": RegionType.STATE,
        "scores": (2, 2, 2, 3, 2),
        "notes": {
            "permitting":     "Federal regime applies; remote Sierra Madre projects face elevated friction.",
            "fiscal":         "Federal royalty regime.",
            "political":      "Mixed; Morena state government with mining-skeptic tilt.",
            "infrastructure": "Adequate around Durango City and silver belt; Sierra Madre districts remote.",
            "community":      "Tepehuán and other indigenous consultation; cartel presence in rural Sierra Madre districts.",
        },
        "summary": (
            "Durango is a meaningful silver and gold producer, with operations along the Sierra Madre "
            "Occidental (San Dimas, Topia, La Cienega cluster). Infrastructure is reasonable in the "
            "lowlands but the high-grade silver districts in the Sierra are remote, indigenous-titled, "
            "and have elevated cartel-related security exposure.\n\n"
            "The Sierra Madre districts have produced for over a century but the operating environment "
            "has tightened on multiple dimensions over the past decade — worse roads, more security "
            "spend, slower permitting, and higher community-relations costs."
        ),
    },
    {
        "name": "Guerrero", "country": "Mexico", "country_code": "MX", "region_type": RegionType.STATE,
        "scores": (2, 2, 1, 2, 1),
        "notes": {
            "permitting":     "Federal regime applies; project-level disputes routinely block development.",
            "fiscal":         "Federal royalty regime; community-level shakedown costs significant.",
            "political":      "Effectively cartel-controlled in rural mining districts; rule of law absent in many areas.",
            "infrastructure": "Limited; many mining districts accessible only via roads under cartel checkpoints.",
            "community":      "Active armed blockades; community 'consultations' often coerced by armed groups.",
        },
        "summary": (
            "Guerrero hosts Mexico's largest open-pit gold mine (Los Filos) and significant other gold "
            "endowment, but is one of the highest-risk operating environments in the Western Hemisphere. "
            "Cartel groups effectively control rural areas across much of the state; armed blockades, "
            "extortion of operations and contractors, and kidnapping of personnel are recurring features.\n\n"
            "Equinox Gold's multi-month 2023 blockade of Los Filos illustrated how community-level disputes "
            "can shut down a major operation even after federal and state permits are in place. The "
            "jurisdiction is investable only with very high country-risk premiums and significant security "
            "infrastructure."
        ),
    },
    {
        "name": "Sinaloa", "country": "Mexico", "country_code": "MX", "region_type": RegionType.STATE,
        "scores": (2, 2, 1, 3, 1),
        "notes": {
            "permitting":     "Federal regime applies; site-level friction high.",
            "fiscal":         "Federal royalty regime.",
            "political":      "Cartel power dominant in much of rural state; rule of law variable.",
            "infrastructure": "Strong coastal highway and rail; rural Sierra districts remote.",
            "community":      "Cartel-related extortion and security overhead routinely affect operations.",
        },
        "summary": (
            "Sinaloa hosts meaningful gold and silver endowment along the Sierra Madre Occidental but the "
            "state is the historic heartland of the Sinaloa Cartel and security risk is among the highest "
            "in Mexico. Operations face continuous extortion overhead, kidnapping risk for foreign "
            "personnel, and periodic forced shutdowns during cartel disputes.\n\n"
            "Coastal infrastructure is excellent and the federal regulatory framework is no worse than "
            "elsewhere in Mexico, but the security premium effectively prices the state out for most "
            "junior capital."
        ),
    },
    {
        "name": "Oaxaca", "country": "Mexico", "country_code": "MX", "region_type": RegionType.STATE,
        "scores": (1, 2, 2, 2, 1),
        "notes": {
            "permitting":     "Federal regime plus state-level community blockades; multiple projects effectively halted.",
            "fiscal":         "Federal royalty regime.",
            "political":      "Morena state government allied with anti-mining indigenous and community movements.",
            "infrastructure": "Limited in mining districts; many sites in remote indigenous-titled territory.",
            "community":      "One of Mexico's strongest organised anti-mining movements; multiple referendums against mining.",
        },
        "summary": (
            "Oaxaca has significant silver and gold endowment but is among the most challenging Mexican "
            "states for new mine development. The state has one of Latin America's most organised "
            "anti-mining indigenous and community movements, and several referendum-style processes have "
            "rejected mining at the municipal level.\n\n"
            "The Capulalpam de Méndez and surrounding Sierra Norte communities have been a flashpoint for "
            "over two decades. Multiple permitted projects have been blocked at the community-engagement "
            "stage despite federal approvals. For exploration-stage juniors, Oaxaca should be approached "
            "only with deep prior community work and a long timeline."
        ),
    },
    {
        "name": "San Luis Potosí", "country": "Mexico", "country_code": "MX", "region_type": RegionType.STATE,
        "scores": (2, 2, 3, 4, 3),
        "notes": {
            "permitting":     "Federal regime applies; state administration broadly pragmatic.",
            "fiscal":         "Federal royalty regime.",
            "political":      "Stable; less anti-mining tilt than several Morena-led states.",
            "infrastructure": "Strong highway and rail; central Mexico location with good logistics.",
            "community":      "Wixárika (Huichol) sacred-site issues at specific locations (Real de Catorce); otherwise standard.",
        },
        "summary": (
            "San Luis Potosí hosts meaningful silver, zinc, and copper endowment and benefits from a "
            "central-Mexico location with strong transport links. The state administration has been less "
            "rhetorically hostile to mining than several other Morena-led state governments.\n\n"
            "The Wixárika (Huichol) sacred-site claims around Real de Catorce have effectively blocked "
            "silver development in that specific district, but this is a localised rather than statewide "
            "dynamic. Operations elsewhere in the state run with standard Mexican operating profiles."
        ),
    },

    # ──────────── Latin America (other) ────────────
    {
        "name": "Peru", "country": "Peru", "country_code": "PE", "region_type": RegionType.COUNTRY,
        "scores": (2, 3, 2, 3, 2),
        "notes": {
            "permitting":     "MINEM process technically capable but social-licence delays are routine.",
            "fiscal":         "Royalty and tax stable but social-conflict-driven payments common.",
            "political":      "High political instability — multiple presidents in recent years; congressional gridlock.",
            "infrastructure": "Mature in established districts; greenfield access often via dedicated build-out.",
            "community":      "Community blockades are a structural risk; consulta previa often inadequate to prevent disputes.",
        },
        "summary": (
            "Peru hosts world-class copper, gold, silver, and zinc endowment — Antamina, Yanacocha, Cerro "
            "Verde, Las Bambas. The technical regulator (MINEM) is one of the most capable in Latin America "
            "and the country's macroeconomic management has historically been orthodox.\n\n"
            "The systemic risk is sub-national: community blockades have caused multi-month production "
            "shutdowns at Las Bambas, Antamina, and other large operations. Consulta previa processes often "
            "fail to prevent disputes from escalating, particularly in highland (Apurímac, Ayacucho, Puno) "
            "districts. Combined with chronic political instability at the national level, Peru remains a "
            "jurisdiction where deposit quality must compensate for elevated execution risk."
        ),
    },
    {
        "name": "Chile", "country": "Chile", "country_code": "CL", "region_type": RegionType.COUNTRY,
        "scores": (3, 3, 4, 4, 3),
        "notes": {
            "permitting":     "Capable but slow regulator; environmental review timelines have stretched.",
            "fiscal":         "Royalty reform 2023 raised top-end rates on copper producers materially.",
            "political":      "Stable democracy; centre-left government has tested (but not broken) the pro-mining consensus.",
            "infrastructure": "Excellent ports, power grid, and rail in copper belt; high desert water scarcity.",
            "community":      "Indigenous consultation framework codified; Atacameño and other community processes active.",
        },
        "summary": (
            "Chile is the world's largest copper producer and a Tier-1 mining jurisdiction by most metrics. "
            "Infrastructure is excellent, the technical workforce is deep, and the rule of law is the best "
            "in Latin America. The constitutional reform attempts of 2022–2023 failed and the existing "
            "framework remains intact.\n\n"
            "The 2023 mining royalty reform raised top-end effective tax rates on copper producers "
            "meaningfully and represents a real fiscal shift even if it falls short of the more aggressive "
            "proposals from earlier in the cycle. Water scarcity in the Atacama is increasingly the binding "
            "physical constraint on new development. Permitting timelines are longer than the historical "
            "norm."
        ),
    },
    {
        "name": "Argentina", "country": "Argentina", "country_code": "AR", "region_type": RegionType.COUNTRY,
        "scores": (2, 3, 3, 3, 3),
        "notes": {
            "permitting":     "Provincial-level permitting varies widely; San Juan and Salta accommodating, others restrictive.",
            "fiscal":         "Royalty stable but FX controls historically constrained capital movement; Milei reforms ongoing.",
            "political":      "Milei government has reduced FX restrictions and improved investment framework; durability uncertain.",
            "infrastructure": "Variable; Andean projects often need full build-out.",
            "community":      "Indigenous consultation framework varies by province.",
        },
        "summary": (
            "Argentina has world-class lithium endowment in the northwest (Salta, Jujuy, Catamarca) and "
            "significant copper-gold porphyry potential along the Andean arc. The Milei government's "
            "Régimen de Incentivo para Grandes Inversiones (RIGI) provides materially better fiscal and "
            "FX terms for qualifying large projects.\n\n"
            "Argentina's history of capital controls, currency crises, and policy reversals creates structural "
            "uncertainty over multi-year project timelines. The current reform direction is constructive but "
            "the durability of the framework across electoral cycles is the central question. Provincial-level "
            "variation remains significant — Mendoza and Chubut have effectively prohibited some forms of "
            "mining."
        ),
    },
    {
        "name": "Brazil", "country": "Brazil", "country_code": "BR", "region_type": RegionType.COUNTRY,
        "scores": (3, 3, 3, 3, 2),
        "notes": {
            "permitting":     "ANM and IBAMA processes capable but slow; tailings rules tightened post-Brumadinho.",
            "fiscal":         "CFEM royalty stable; broader tax reform under way.",
            "political":      "Stable democracy; Lula government less mining-friendly than Bolsonaro era.",
            "infrastructure": "Strong in iron-ore corridors; weaker in Amazon and inland districts.",
            "community":      "Indigenous land prohibitions extensive; FUNAI processes can block projects.",
        },
        "summary": (
            "Brazil is a major iron ore, gold, copper, and base-metal producer with established mining "
            "infrastructure in Minas Gerais, Pará, and Goiás. The post-Brumadinho regulatory tightening "
            "around tailings storage facilities has materially raised the bar for new development.\n\n"
            "Indigenous land issues are the single largest jurisdiction-specific risk for Brazilian mining. "
            "The constitutional protections and FUNAI consultation requirements over Indigenous reserves are "
            "extensive and have blocked or stalled significant projects in the Amazon. The Lula government's "
            "stance has been less accommodating than Bolsonaro's was."
        ),
    },
    {
        "name": "Ecuador", "country": "Ecuador", "country_code": "EC", "region_type": RegionType.COUNTRY,
        "scores": (2, 3, 2, 3, 2),
        "notes": {
            "permitting":     "Process exists but regularly blocked by referendums and constitutional challenges.",
            "fiscal":         "Royalty regime stable; windfall provisions occasionally proposed.",
            "political":      "High political instability; security situation deteriorated sharply 2023–2024.",
            "infrastructure": "Adequate around Andean districts; coastal and Amazon regions vary.",
            "community":      "Indigenous and community consultation processes frequently weaponised; referendums have blocked permitted projects.",
        },
        "summary": (
            "Ecuador has world-class porphyry copper-gold endowment along the Andean cordillera but the "
            "country has become one of the highest-risk Latin American mining jurisdictions. The 2023 "
            "Yasuní referendum (oil) and prior local-level mining referendums have demonstrated that fully "
            "permitted projects can be retroactively blocked through plebiscite mechanisms.\n\n"
            "The 2023–2024 deterioration in the country's security situation, with cartel violence reaching "
            "unprecedented levels, has added a material physical-security dimension to the country risk."
        ),
    },
    {
        "name": "Colombia", "country": "Colombia", "country_code": "CO", "region_type": RegionType.COUNTRY,
        "scores": (2, 3, 2, 3, 2),
        "notes": {
            "permitting":     "Permitting effectively frozen for many projects under the Petro government.",
            "fiscal":         "Royalty changes 2022; broader anti-extractivist policy shift.",
            "political":      "Petro government has openly opposed new mining; significant policy shift from prior decades.",
            "infrastructure": "Mature in established districts; security risk in some FARC-legacy regions.",
            "community":      "Community consulta processes increasingly hostile; ELN and dissident-FARC presence in mining regions.",
        },
        "summary": (
            "Colombia hosts significant gold, copper, and emerald endowment, but the political environment "
            "has shifted dramatically against mining since the 2022 election of the Petro government. "
            "Permitting for new projects has slowed effectively to a halt, royalty terms have tightened, "
            "and the rhetorical environment has been openly anti-extractive.\n\n"
            "Operating mines continue and a future government could reset the policy trajectory, but for the "
            "current political cycle Colombia is an extremely difficult place to advance development-stage "
            "projects."
        ),
    },
    {
        "name": "Guyana", "country": "Guyana", "country_code": "GY", "region_type": RegionType.COUNTRY,
        "scores": (3, 3, 4, 2, 3),
        "notes": {
            "permitting":     "GGMC process workable; small-scale mining dominant historically.",
            "fiscal":         "Royalty regime stable; competitive corporate rates.",
            "political":      "Stable democracy; oil boom has reshaped fiscal capacity but not mining policy.",
            "infrastructure": "Limited; jungle and savanna projects often fly-in or river-access only.",
            "community":      "Amerindian title regime functional; smaller-scale than other LatAm jurisdictions.",
        },
        "summary": (
            "Guyana hosts a meaningful gold endowment in the Guiana Shield, with a long history of artisanal "
            "and small-scale mining. The country has become significantly wealthier on the back of offshore "
            "oil discoveries since 2019, and the political environment around extractive industries has "
            "remained constructive.\n\n"
            "Infrastructure is the binding constraint — most projects require river access, dedicated road "
            "build-out, or fly-in operations. The regulatory framework is workable but smaller-scale than "
            "comparable LatAm jurisdictions."
        ),
    },

    # ──────────── Africa ────────────
    {
        "name": "Ghana", "country": "Ghana", "country_code": "GH", "region_type": RegionType.COUNTRY,
        "scores": (3, 3, 4, 2, 3),
        "notes": {
            "permitting":     "Minerals Commission capable; timelines workable.",
            "fiscal":         "Royalty regime largely stable; periodic gold-export levy proposals.",
            "political":      "Africa's most stable democracy; consistent peaceful transitions of power.",
            "infrastructure": "Adequate around established districts; rural greenfield projects need build-out.",
            "community":      "Community engagement processes generally functional; illegal mining (galamsey) a backdrop issue.",
        },
        "summary": (
            "Ghana is one of West Africa's most stable mining jurisdictions and Africa's second-largest gold "
            "producer. The political framework has been remarkably stable across multiple democratic "
            "transitions, and the regulatory regime is one of the most predictable on the continent.\n\n"
            "The galamsey (illegal artisanal) mining problem is the persistent jurisdiction-level challenge — "
            "it complicates community relations and creates security overhead at most operating mines. "
            "Infrastructure is workable in the Ashanti and Western regions but requires investment "
            "elsewhere."
        ),
    },
    {
        "name": "Mali", "country": "Mali", "country_code": "ML", "region_type": RegionType.COUNTRY,
        "scores": (1, 1, 1, 1, 1),
        "notes": {
            "permitting":     "Effectively frozen under junta; new mining code 2023 retroactively raised state participation.",
            "fiscal":         "2023 mining code increased state stake to 30% with retroactive application; tax disputes ongoing.",
            "political":      "Military junta in power since 2021; suspended ECOWAS membership; Russian mercenary presence.",
            "infrastructure": "Limited; transport via Côte d'Ivoire and Senegal corridors.",
            "community":      "Active jihadist insurgency in northern and central regions creates physical security risk.",
        },
        "summary": (
            "Mali was for two decades one of West Africa's premier gold districts and remains one of the "
            "continent's most prospective. The post-2021 deterioration has been severe: a military junta has "
            "consolidated power, ECOWAS membership has been suspended, and Wagner / Africa Corps Russian "
            "mercenary forces are deployed against jihadist insurgents across much of the country.\n\n"
            "The 2023 mining code raised state participation to 30% with retroactive provisions, leading to "
            "active disputes with Barrick (Loulo-Gounkoto), Resolute, and Hummingbird. Capital is exiting the "
            "jurisdiction. For new investment, Mali is currently uninvestable for most institutional capital."
        ),
    },
    {
        "name": "Burkina Faso", "country": "Burkina Faso", "country_code": "BF", "region_type": RegionType.COUNTRY,
        "scores": (2, 2, 1, 1, 2),
        "notes": {
            "permitting":     "Process technically functional but heavily impacted by deteriorating security.",
            "fiscal":         "Mining code revised; state stake increased.",
            "political":      "Military junta in power since 2022 coups; aligned with Mali and Niger AES bloc.",
            "infrastructure": "Limited; security situation has degraded transport corridors.",
            "community":      "Active jihadist insurgency controls significant rural territory.",
        },
        "summary": (
            "Burkina Faso has been one of West Africa's faster-growing gold producers but, like Mali, has "
            "deteriorated rapidly since the 2022 military coups. The country is now part of the Alliance of "
            "Sahel States (AES) bloc with Mali and Niger and has a Russian-aligned security posture.\n\n"
            "Operating mines continue to produce but security overhead is significant and several have "
            "experienced jihadist attacks on personnel and convoys. New investment is largely on hold."
        ),
    },
    {
        "name": "Tanzania", "country": "Tanzania", "country_code": "TZ", "region_type": RegionType.COUNTRY,
        "scores": (2, 2, 3, 2, 2),
        "notes": {
            "permitting":     "Workable; previous high-friction era under Magufuli largely behind.",
            "fiscal":         "Framework agreements with Barrick set precedent; royalty/tax disputes still possible.",
            "political":      "Stable but state-led economic agenda intervenes in mining periodically.",
            "infrastructure": "Adequate in Mwanza/Geita gold belt; rural projects vary.",
            "community":      "Established consultation framework but artisanal mining tensions persist.",
        },
        "summary": (
            "Tanzania has a meaningful gold endowment around Lake Victoria (Geita, Bulyanhulu, North Mara) "
            "and significant nickel and rare-earth potential. The Magufuli-era confrontations with Barrick "
            "and Acacia were eventually resolved but established a precedent that the state will intervene "
            "in royalty and tax structures unilaterally when politically convenient.\n\n"
            "The current operating environment is more constructive but the structural risk that the "
            "Magufuli template returns under future leadership remains a real consideration for long-dated "
            "investments."
        ),
    },
    {
        "name": "South Africa", "country": "South Africa", "country_code": "ZA", "region_type": RegionType.COUNTRY,
        "scores": (2, 2, 2, 3, 2),
        "notes": {
            "permitting":     "DMRE permitting backlog severe; timelines among the worst globally for new applications.",
            "fiscal":         "Royalty stable but BEE ownership requirements (Mining Charter) are a continuing fiscal cost.",
            "political":      "Stable democracy but ANC-led coalition; policy unpredictability around BEE and electricity.",
            "infrastructure": "Power crisis (Eskom load-shedding) is an ongoing operational drag.",
            "community":      "Community development obligations significant; Marikana legacy still informs sentiment.",
        },
        "summary": (
            "South Africa hosts the world's most prospective platinum group metals belt (Bushveld) and "
            "significant gold, manganese, chrome, and coal endowment. The country's mining workforce and "
            "technical depth are world-class. However, the operating environment has deteriorated steadily "
            "over the past 15 years.\n\n"
            "The DMRE permitting backlog is among the worst globally for new applications. Eskom load-shedding "
            "imposes meaningful production losses across the sector. Mining Charter ownership requirements "
            "(currently 30% historically disadvantaged ownership) impose significant ongoing capital costs. "
            "The country remains investable for established producers but is increasingly difficult for "
            "exploration-stage juniors."
        ),
    },
    {
        "name": "Democratic Republic of the Congo", "country": "Democratic Republic of the Congo", "country_code": "CD", "region_type": RegionType.COUNTRY,
        "scores": (1, 2, 1, 1, 1),
        "notes": {
            "permitting":     "Process exists but plagued by corruption and unilateral renegotiation.",
            "fiscal":         "2018 mining code raised royalties significantly with retroactive provisions.",
            "political":      "Tshisekedi government re-elected 2023 but eastern conflict ongoing; rule of law weak.",
            "infrastructure": "Limited; cobalt-copper belt has some rail/road but reliability poor.",
            "community":      "Artisanal mining (especially cobalt) creates material ESG and security overhead.",
        },
        "summary": (
            "The DRC hosts roughly 70% of the world's cobalt production and significant copper, tin, tantalum, "
            "and gold endowment. For battery-metal exposure, the jurisdiction is structurally important. The "
            "2018 mining code raised royalties materially and applied them retroactively to existing "
            "agreements.\n\n"
            "Eastern DRC remains an active conflict zone with M23 and other armed groups operating through "
            "much of the Kivu provinces. Artisanal cobalt mining creates significant ESG exposure that "
            "Western capital has become more sensitive to. Operations continue but on country-risk premiums "
            "that exceed almost any other jurisdiction."
        ),
    },

    # ──────────── Other ────────────
    {
        "name": "Finland", "country": "Finland", "country_code": "FI", "region_type": RegionType.COUNTRY,
        "scores": (4, 4, 5, 5, 4),
        "notes": {
            "permitting":     "TUKES regulator capable and predictable.",
            "fiscal":         "Stable EU-aligned tax regime.",
            "political":      "Stable EU democracy; mining is policy priority for critical minerals.",
            "infrastructure": "Excellent — grid, rail, ports across the country.",
            "community":      "Sami consultation in northern Lapland; framework workable.",
        },
        "summary": (
            "Finland is one of the highest-scoring jurisdictions on the Fraser Institute survey and has "
            "become a focal point for European critical-minerals investment. The country hosts world-class "
            "battery-metals endowment (Sotkamo, Kevitsa, Kemi) and the regulatory environment is among the "
            "most predictable in Europe.\n\n"
            "Sami Indigenous consultation requirements apply in Lapland but the framework is well-established "
            "and rarely a project blocker."
        ),
    },
    {
        "name": "Mongolia", "country": "Mongolia", "country_code": "MN", "region_type": RegionType.COUNTRY,
        "scores": (2, 2, 3, 2, 3),
        "notes": {
            "permitting":     "Process exists but politically charged for major projects.",
            "fiscal":         "Oyu Tolgoi renegotiations set precedent for unilateral fiscal changes on flagship projects.",
            "political":      "Democratic but volatile; mining policy has shifted multiple times.",
            "infrastructure": "Limited; coal/copper exports depend on Chinese-border logistics.",
            "community":      "Herder community concerns around water and land use a recurring friction point.",
        },
        "summary": (
            "Mongolia hosts the Oyu Tolgoi copper-gold complex and significant coal endowment. The country "
            "is a functioning democracy and the technical regulator is capable, but the multi-decade saga "
            "around Oyu Tolgoi's fiscal structure illustrates that flagship projects in Mongolia face "
            "ongoing political renegotiation pressure.\n\n"
            "Infrastructure is heavily oriented around the Chinese border (the dominant export market for "
            "both copper and coal) which creates concentrated logistical exposure. For deposits not located "
            "near existing transport corridors, capex requirements are high."
        ),
    },
]


class Command(BaseCommand):
    help = "Seed initial Jurisdiction risk assessments. Idempotent — re-runs update existing rows."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset", action="store_true",
            help="Delete all existing Jurisdiction rows before seeding.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            n = Jurisdiction.objects.count()
            Jurisdiction.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {n} existing jurisdictions."))

        created = updated = 0
        today = date.today()

        for row in SEED:
            permitting, fiscal, political, infrastructure, community = row["scores"]
            notes = row["notes"]
            obj, was_created = Jurisdiction.objects.update_or_create(
                country=row["country"],
                name=row["name"],
                defaults={
                    "country_code":         row["country_code"],
                    "region_type":          row["region_type"],
                    "permitting_score":     permitting,
                    "permitting_notes":     notes["permitting"],
                    "fiscal_score":         fiscal,
                    "fiscal_notes":         notes["fiscal"],
                    "political_score":      political,
                    "political_notes":      notes["political"],
                    "infrastructure_score": infrastructure,
                    "infrastructure_notes": notes["infrastructure"],
                    "community_score":      community,
                    "community_notes":      notes["community"],
                    "summary":              row["summary"].strip(),
                    "last_assessed_at":     today,
                    "is_published":         True,
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(SEED)} jurisdictions ({created} created, {updated} updated)."
        ))
