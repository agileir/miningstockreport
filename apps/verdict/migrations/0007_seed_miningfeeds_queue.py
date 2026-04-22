"""
Seed CompanyQueue with every ticker pulled from miningfeeds.com's commodity
report pages (gold, copper, silver, uranium) as of 2026-04-22.

Status values set per entry:
  - "promoted"     — ticker already has a Company record; FK linked
  - "active"       — Canadian-listed, verified active, ready to promote
  - "acquired"     — company absorbed into another entity
  - "delisted"     — no longer trading on a recognised exchange
  - "pending"      — status uncertain, needs manual verification
  - "out_of_scope" — non-Canadian listing (NYSE/ASX/AIM/AMEX/OTCBB)
"""
from django.db import migrations


QUEUE_DATA = [
    # ──────────────── Gold (miningfeeds.com/gold) ────────────────
    {"ticker": "AEM", "exchange": "NYSE", "name": "Agnico-Eagle Mines Ltd.", "primary_commodity": "Gold", "country": "Canada", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": "Also listed on TSX as AEM — covered via Canadian listing"},
    {"ticker": "NEM", "exchange": "NYSE", "name": "Newmont Corporation", "primary_commodity": "Gold", "country": "USA", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": "Also listed on TSX as NGT — covered via Canadian listing"},
    {"ticker": "FNV", "exchange": "TSX", "name": "Franco-Nevada Corp.", "primary_commodity": "Gold", "country": "Canada", "status": "promoted", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "ABX", "exchange": "NYSE", "name": "Barrick Gold Corp.", "primary_commodity": "Gold", "country": "Canada", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": "NYSE ticker is GOLD; TSX:ABX in DB covers Canadian listing"},
    {"ticker": "GFI", "exchange": "NYSE", "name": "Gold Fields Ltd.", "primary_commodity": "Gold", "country": "South Africa", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "KGC", "exchange": "NYSE", "name": "Kinross Gold Corp.", "primary_commodity": "Gold", "country": "Canada", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": "Also listed on TSX as K — covered via Canadian listing"},
    {"ticker": "EVN", "exchange": "ASX", "name": "Evolution Mining Limited", "primary_commodity": "Gold", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "AGI", "exchange": "TSX", "name": "Alamos Gold Inc.", "primary_commodity": "Gold", "country": "Canada", "status": "promoted", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "HMY", "exchange": "NYSE", "name": "Harmony Gold Mining Ltd.", "primary_commodity": "Gold", "country": "South Africa", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "BTO", "exchange": "TSX", "name": "B2Gold Corp.", "primary_commodity": "Gold", "country": "Canada", "status": "promoted", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "ALD", "exchange": "ASX", "name": "Allied Gold Mining PLC", "primary_commodity": "Gold", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "DEG", "exchange": "ASX", "name": "De Grey Mining Ltd.", "primary_commodity": "Gold", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "CDE", "exchange": "NYSE", "name": "Coeur Mining", "primary_commodity": "Gold", "country": "USA", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "ELD", "exchange": "TSX", "name": "Eldorado Gold Corp.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "IMG", "exchange": "TSX", "name": "IAMGOLD Corp.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "PRU", "exchange": "ASX", "name": "Perseus Mining Ltd.", "primary_commodity": "Gold", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "NGD", "exchange": "TSX", "name": "New Gold Inc.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/gold,copper", "notes": "Also listed on miningfeeds copper page"},
    {"ticker": "OGC", "exchange": "TSX", "name": "OceanaGold Corp.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "CGG", "exchange": "TSX", "name": "China Gold International Resources", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "TXG", "exchange": "TSX", "name": "Torex Gold Resources Inc.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "RRL", "exchange": "ASX", "name": "Regis Resources Limited", "primary_commodity": "Gold", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "SSL", "exchange": "TSX", "name": "Sandstorm Gold Ltd.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/gold", "notes": "Royalty / streaming"},
    {"ticker": "GOR", "exchange": "ASX", "name": "Gold Road Resources Limited", "primary_commodity": "Gold", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "RMS", "exchange": "ASX", "name": "Ramelius Resources Ltd.", "primary_commodity": "Gold", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "WAF", "exchange": "ASX", "name": "West African Resources Ltd.", "primary_commodity": "Gold", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "WDO", "exchange": "TSX", "name": "Wesdome Gold Mines Ltd.", "primary_commodity": "Gold", "country": "Canada", "status": "promoted", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "RED", "exchange": "ASX", "name": "Red 5 Ltd.", "primary_commodity": "Gold", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "CG", "exchange": "TSX", "name": "Centerra Gold Inc.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/gold", "notes": ""},
    {"ticker": "NG", "exchange": "TSX", "name": "NovaGold Resources Inc.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/gold", "notes": "Donlin project"},
    {"ticker": "OSK", "exchange": "TSX", "name": "Osisko Mining Corp.", "primary_commodity": "Gold", "country": "Canada", "status": "acquired", "source": "miningfeeds.com/gold", "notes": "Acquired by Gold Fields in 2024"},

    # ──────────────── Copper (miningfeeds.com/copper) ────────────────
    {"ticker": "SLS", "exchange": "TSX", "name": "Solaris Resources Inc.", "primary_commodity": "Copper", "country": "Canada", "status": "active", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "BHP", "exchange": "ASX", "name": "BHP Billiton Ltd.", "primary_commodity": "Copper", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": "Global diversified major"},
    {"ticker": "RIO", "exchange": "ASX", "name": "Rio Tinto Ltd.", "primary_commodity": "Copper", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": "Global diversified major"},
    {"ticker": "SCCO", "exchange": "NYSE", "name": "Southern Copper Corp.", "primary_commodity": "Copper", "country": "USA", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "FCX", "exchange": "NYSE", "name": "Freeport-McMoRan Inc.", "primary_commodity": "Copper", "country": "USA", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "NST", "exchange": "ASX", "name": "Northern Star Resources Ltd.", "primary_commodity": "Gold", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": "Gold-primary; mis-categorised"},
    {"ticker": "FM", "exchange": "TSX", "name": "First Quantum Minerals Ltd.", "primary_commodity": "Copper", "country": "Canada", "status": "active", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "IVN", "exchange": "TSX", "name": "Ivanhoe Mines Ltd.", "primary_commodity": "Copper", "country": "Canada", "status": "active", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "LUN", "exchange": "TSX", "name": "Lundin Mining Corp.", "primary_commodity": "Copper", "country": "Canada", "status": "active", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "CS", "exchange": "TSX", "name": "Capstone Copper Corp.", "primary_commodity": "Copper", "country": "Canada", "status": "active", "source": "miningfeeds.com/copper", "notes": "Formerly Capstone Mining"},
    {"ticker": "SFR", "exchange": "ASX", "name": "Sandfire Resources", "primary_commodity": "Copper", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "GMD", "exchange": "ASX", "name": "Genesis Minerals Limited", "primary_commodity": "Gold", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": "Gold-primary; mis-categorised"},
    {"ticker": "HBM", "exchange": "TSX", "name": "HudBay Minerals Inc.", "primary_commodity": "Copper", "country": "Canada", "status": "active", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "BVN", "exchange": "NYSE", "name": "Compañía de Minas Buenaventura", "primary_commodity": "Silver", "country": "Peru", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "IGO", "exchange": "ASX", "name": "Independence Group NL", "primary_commodity": "Nickel", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "ORA", "exchange": "TSX", "name": "Aura Minerals Inc.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/copper", "notes": "Gold-copper polymetallic; primary is gold"},
    {"ticker": "LTR", "exchange": "ASX", "name": "Liontown Resources Ltd.", "primary_commodity": "Lithium", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": "Lithium-primary; mis-categorised"},
    {"ticker": "CYL", "exchange": "ASX", "name": "Catalyst Metals Ltd.", "primary_commodity": "Gold", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "PNR", "exchange": "ASX", "name": "Pacific Niugini Ltd.", "primary_commodity": "Gold", "country": "PNG", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "ALS", "exchange": "TSX", "name": "Altius Minerals Corp.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/copper", "notes": "Royalty / streaming; multi-commodity"},
    {"ticker": "TKO", "exchange": "TSX", "name": "Taseko Mines Ltd.", "primary_commodity": "Copper", "country": "Canada", "status": "active", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "NDM", "exchange": "TSX", "name": "Northern Dynasty Minerals Ltd.", "primary_commodity": "Copper", "country": "Canada", "status": "active", "source": "miningfeeds.com/copper", "notes": "Pebble project (Alaska)"},
    {"ticker": "III", "exchange": "TSX", "name": "Imperial Metals Corp.", "primary_commodity": "Copper", "country": "Canada", "status": "active", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "ATX", "exchange": "TSXV", "name": "ATEX Resources Inc.", "primary_commodity": "Copper", "country": "Canada", "status": "active", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "RIO", "exchange": "TSXV", "name": "Rio Alto Mining Limited", "primary_commodity": "Gold", "country": "Canada", "status": "delisted", "source": "miningfeeds.com/copper", "notes": "Acquired by Tahoe Resources in 2015; Tahoe later acquired by Pan American Silver"},
    {"ticker": "ETG", "exchange": "TSX", "name": "Entrée Resources Ltd.", "primary_commodity": "Copper", "country": "Canada", "status": "active", "source": "miningfeeds.com/copper", "notes": "Formerly Entrée Gold; Oyu Tolgoi royalty"},
    {"ticker": "MLX", "exchange": "ASX", "name": "Metals X Limited", "primary_commodity": "Copper", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": ""},
    {"ticker": "SVM", "exchange": "ASX", "name": "Sovereign Metals Limited", "primary_commodity": "Rare Earth", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": "Different company from TSX:SVM (Silvercorp)"},
    {"ticker": "RXM", "exchange": "ASX", "name": "Rex Minerals Limited", "primary_commodity": "Copper", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/copper", "notes": ""},

    # ──────────────── Silver (miningfeeds.com/silver) ────────────────
    {"ticker": "PAAS", "exchange": "TSX", "name": "Pan American Silver Corp.", "primary_commodity": "Silver", "country": "Canada", "status": "promoted", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "DPM", "exchange": "TSX", "name": "Dundee Precious Metals Inc.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/silver", "notes": "Gold-silver polymetallic"},
    {"ticker": "HL", "exchange": "NYSE", "name": "Hecla Mining Company", "primary_commodity": "Silver", "country": "USA", "status": "out_of_scope", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "MAG", "exchange": "TSX", "name": "MAG Silver Corp.", "primary_commodity": "Silver", "country": "Canada", "status": "promoted", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "FVI", "exchange": "TSX", "name": "Fortuna Mining Corp.", "primary_commodity": "Silver", "country": "Canada", "status": "promoted", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "EDR", "exchange": "TSX", "name": "Endeavour Silver Corp.", "primary_commodity": "Silver", "country": "Canada", "status": "promoted", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "SVM", "exchange": "TSX", "name": "Silvercorp Metals Inc.", "primary_commodity": "Silver", "country": "Canada", "status": "promoted", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "GGD", "exchange": "TSX", "name": "GoGold Resources Inc.", "primary_commodity": "Silver", "country": "Canada", "status": "promoted", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "MUX", "exchange": "NYSE", "name": "McEwen Mining Inc.", "primary_commodity": "Gold", "country": "Canada", "status": "out_of_scope", "source": "miningfeeds.com/silver", "notes": "Also listed on TSX as MUX — covered via Canadian listing"},
    {"ticker": "MND", "exchange": "TSX", "name": "Mandalay Resources Corp.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "AAG", "exchange": "TSXV", "name": "Andean American Gold Corp.", "primary_commodity": "Gold", "country": "Canada", "status": "delisted", "source": "miningfeeds.com/silver", "notes": "Appears defunct on current market records"},
    {"ticker": "SVL", "exchange": "ASX", "name": "Silver Mines Limited", "primary_commodity": "Silver", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "CKG", "exchange": "TSXV", "name": "Chesapeake Gold Corp.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/silver", "notes": "Gold-silver polymetallic (Metates)"},
    {"ticker": "LODE", "exchange": "OTHER", "name": "Comstock Mining Inc.", "primary_commodity": "Gold", "country": "USA", "status": "out_of_scope", "source": "miningfeeds.com/silver", "notes": "NYSE American listing"},
    {"ticker": "IPT", "exchange": "TSXV", "name": "Impact Silver Corp.", "primary_commodity": "Silver", "country": "Canada", "status": "active", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "GORO", "exchange": "OTHER", "name": "Gold Resource Corp.", "primary_commodity": "Gold", "country": "USA", "status": "out_of_scope", "source": "miningfeeds.com/silver", "notes": "NYSE American listing"},
    {"ticker": "SSV", "exchange": "TSXV", "name": "Southern Silver Exploration Corp.", "primary_commodity": "Silver", "country": "Canada", "status": "active", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "MTH", "exchange": "ASX", "name": "Mithril Silver and Gold Limited", "primary_commodity": "Silver", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "XPL", "exchange": "OTHER", "name": "Solitario Exploration & Royalty", "primary_commodity": "Silver", "country": "USA", "status": "out_of_scope", "source": "miningfeeds.com/silver", "notes": "NYSE American listing"},
    {"ticker": "BCM", "exchange": "TSXV", "name": "Bear Creek Mining Corp.", "primary_commodity": "Silver", "country": "Canada", "status": "active", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "TUO", "exchange": "TSXV", "name": "Teuton Resources Corp.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/silver", "notes": "Golden Triangle royalty + explorer"},
    {"ticker": "ABI", "exchange": "TSXV", "name": "Abcourt Mines Inc.", "primary_commodity": "Silver", "country": "Canada", "status": "active", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "PZG", "exchange": "OTHER", "name": "Paramount Gold Nevada Corp.", "primary_commodity": "Gold", "country": "USA", "status": "out_of_scope", "source": "miningfeeds.com/silver", "notes": "NYSE American listing"},
    {"ticker": "SRL", "exchange": "TSXV", "name": "Salazar Resources Limited", "primary_commodity": "Copper", "country": "Canada", "status": "active", "source": "miningfeeds.com/silver", "notes": "Copper-gold, Ecuador operations"},
    {"ticker": "SBR", "exchange": "TSX", "name": "Silver Bear Resources Plc", "primary_commodity": "Silver", "country": "Canada", "status": "pending", "source": "miningfeeds.com/silver", "notes": "Russia exposure — verify current listing status"},
    {"ticker": "AGD", "exchange": "ASX", "name": "Austral Gold Limited", "primary_commodity": "Gold", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "RK", "exchange": "TSXV", "name": "Rockhaven Resources Ltd.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/silver", "notes": "Yukon gold"},
    {"ticker": "CRI", "exchange": "TSXV", "name": "Castle Resources Inc.", "primary_commodity": "Gold", "country": "Canada", "status": "active", "source": "miningfeeds.com/silver", "notes": ""},
    {"ticker": "EXN", "exchange": "TSX", "name": "Excellon Resources Inc.", "primary_commodity": "Silver", "country": "Canada", "status": "active", "source": "miningfeeds.com/silver", "notes": ""},

    # ──────────────── Uranium (miningfeeds.com/uranium) ────────────────
    {"ticker": "NXE", "exchange": "TSX", "name": "NexGen Energy Ltd.", "primary_commodity": "Uranium", "country": "Canada", "status": "active", "source": "miningfeeds.com/uranium", "notes": "Arrow deposit, Athabasca Basin"},
    {"ticker": "UEC", "exchange": "OTHER", "name": "Uranium Energy Corp.", "primary_commodity": "Uranium", "country": "USA", "status": "out_of_scope", "source": "miningfeeds.com/uranium", "notes": "OTCBB / NYSE American listing"},
    {"ticker": "DML", "exchange": "TSX", "name": "Fission Uranium Corp.", "primary_commodity": "Uranium", "country": "Canada", "status": "acquired", "source": "miningfeeds.com/uranium", "notes": "Acquired by Paladin Energy in 2024"},
    {"ticker": "DYL", "exchange": "ASX", "name": "Deep Yellow Ltd.", "primary_commodity": "Uranium", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/uranium", "notes": ""},
    {"ticker": "EBR", "exchange": "ASX", "name": "Eagle Bay Resources NL", "primary_commodity": "Uranium", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/uranium", "notes": ""},
    {"ticker": "BKY", "exchange": "ASX", "name": "Berkeley Resources Ltd.", "primary_commodity": "Uranium", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/uranium", "notes": ""},
    {"ticker": "POL", "exchange": "ASX", "name": "Polaris Metals NL", "primary_commodity": "Uranium", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/uranium", "notes": ""},
    {"ticker": "ENR", "exchange": "ASX", "name": "Encounter Resources Ltd.", "primary_commodity": "Uranium", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/uranium", "notes": ""},
    {"ticker": "UCU", "exchange": "TSXV", "name": "Ucore Rare Metals Inc.", "primary_commodity": "Rare Earth", "country": "Canada", "status": "active", "source": "miningfeeds.com/uranium", "notes": "Rare-earth primary; mis-categorised by miningfeeds"},
    {"ticker": "AZM", "exchange": "TSXV", "name": "Azimut Exploration Inc.", "primary_commodity": "Gold", "country": "Canada", "status": "promoted", "source": "miningfeeds.com/uranium", "notes": "Gold-primary in DB; miningfeeds categorised as uranium"},
    {"ticker": "AGC", "exchange": "ASX", "name": "Agincourt Resources Ltd.", "primary_commodity": "Uranium", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/uranium", "notes": ""},
    {"ticker": "ADN", "exchange": "ASX", "name": "Adelaide Resources Ltd.", "primary_commodity": "Uranium", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/uranium", "notes": ""},
    {"ticker": "TOE", "exchange": "ASX", "name": "Toro Energy Ltd.", "primary_commodity": "Uranium", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/uranium", "notes": ""},
    {"ticker": "RMR", "exchange": "TSXV", "name": "Rome Resources Ltd.", "primary_commodity": "Uranium", "country": "Canada", "status": "pending", "source": "miningfeeds.com/uranium", "notes": "Small-cap explorer; verify current status"},
    {"ticker": "PNN", "exchange": "ASX", "name": "Pepinnini Minerals Limited", "primary_commodity": "Uranium", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/uranium", "notes": ""},
    {"ticker": "BTT", "exchange": "TSXV", "name": "Bitterroot Resources Ltd.", "primary_commodity": "Uranium", "country": "Canada", "status": "pending", "source": "miningfeeds.com/uranium", "notes": "Small-cap explorer; verify current status"},
    {"ticker": "PEX", "exchange": "TSXV", "name": "Pacific Ridge Exploration Ltd.", "primary_commodity": "Copper", "country": "Canada", "status": "active", "source": "miningfeeds.com/uranium", "notes": "Copper-gold primary; mis-categorised by miningfeeds"},
    {"ticker": "CUL", "exchange": "ASX", "name": "Cullen Resources Ltd.", "primary_commodity": "Uranium", "country": "Australia", "status": "out_of_scope", "source": "miningfeeds.com/uranium", "notes": ""},
    {"ticker": "RRR", "exchange": "LSE", "name": "Red Rock Resources", "primary_commodity": "Uranium", "country": "UK", "status": "out_of_scope", "source": "miningfeeds.com/uranium", "notes": "AIM listing (LSE sub-market)"},
    {"ticker": "RJX-A", "exchange": "TSXV", "name": "RJK Explorations Ltd.", "primary_commodity": "Uranium", "country": "Canada", "status": "pending", "source": "miningfeeds.com/uranium", "notes": "Class-A share series; verify current status"},
]


def seed_queue(apps, schema_editor):
    CompanyQueue = apps.get_model("verdict", "CompanyQueue")
    Company = apps.get_model("verdict", "Company")

    for row in QUEUE_DATA:
        ticker = row["ticker"]
        exchange = row["exchange"]
        if CompanyQueue.objects.filter(ticker=ticker, exchange=exchange).exists():
            continue  # Idempotent

        company = None
        if row["status"] == "promoted":
            # Link to existing Company record if found
            company = Company.objects.filter(ticker=ticker, exchange=exchange).first()
            if company is None:
                # Fall back to ticker-only match (exchange may have been recorded differently)
                company = Company.objects.filter(ticker=ticker).first()

        CompanyQueue.objects.create(
            ticker=ticker,
            exchange=exchange,
            name=row.get("name", ""),
            primary_commodity=row.get("primary_commodity", ""),
            country=row.get("country", ""),
            status=row["status"],
            source=row.get("source", ""),
            notes=row.get("notes", ""),
            company=company,
        )


def reverse_seed(apps, schema_editor):
    CompanyQueue = apps.get_model("verdict", "CompanyQueue")
    pairs = [(r["ticker"], r["exchange"]) for r in QUEUE_DATA]
    for ticker, exchange in pairs:
        CompanyQueue.objects.filter(ticker=ticker, exchange=exchange).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("verdict", "0006_companyqueue"),
    ]
    operations = [
        migrations.RunPython(seed_queue, reverse_seed),
    ]
