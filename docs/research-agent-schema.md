# Research Agent — Scorecard JSON Schema

The agent writes one `research_queue/scorecard_<TICKER>_<YYYYMMDD>.json` file per company researched, then commits and pushes. The cron-driven `process_research_queue.sh` on production reads each file, creates a `VerdictScorecard` (and any `ShareInstrument` rows), then deletes the JSON.

This doc is the single source of truth for the JSON shape. Update the agent's prompt whenever this file changes.

---

## Full schema

```json
{
  "ticker": "MAXX",
  "exchange": "CSE",

  "management_score": 3,
  "management_notes": "...",
  "geology_score": 2,
  "geology_notes": "...",
  "capital_score": 4,
  "capital_notes": "...",
  "catalyst_score": 3,
  "catalyst_notes": "...",
  "acquisition_score": 2,
  "acquisition_notes": "...",

  "verdict": "WATCH",
  "analyst_summary": "...",
  "confidence": "high",

  "nav_per_share": 0.42,
  "current_price": null,

  "resource_measured": "1.2 Moz Au @ 1.5 g/t",
  "resource_indicated": "3.4 Moz Au @ 1.1 g/t",
  "resource_inferred": "0.8 Moz Au @ 0.9 g/t",
  "reserve_proven": "",
  "reserve_probable": "",

  "shares_issued_outstanding": 153200000,
  "shares_fully_diluted": 178500000,

  "share_instruments": [
    {"type": "warrant", "count": 12500000, "strike_price": 0.50, "expiry": "2027-06-30", "notes": "Tranche A — financing 2025-06"},
    {"type": "warrant", "count": 8000000, "strike_price": 0.75, "expiry": "2028-03-15", "notes": "Broker warrants"},
    {"type": "option", "count": 5000000, "strike_price": 0.25, "expiry": null, "notes": "Director options"}
  ]
}
```

---

## Field reference

### Required (existing)
- `ticker` — string, exchange ticker without suffix
- `exchange` — one of `TSX`, `TSXV`, `CSE`, `ASX`, `OTC`, `NYSE`, `LSE`
- `<factor>_score` — integer 1–5, for each of management / geology / capital / catalyst / acquisition
- `<factor>_notes` — string, the reasoning for the score (long-form is fine)
- `verdict` — `"BUY"`, `"WATCH"`, or `"AVOID"`
- `analyst_summary` — string, the published narrative
- `confidence` — `"high"` (publishes the scorecard) or `"low"` (saves but unpublished)

### Optional (existing)
- `nav_per_share` — number or null
- `current_price` — **ignored** by the processor (always re-fetched from Yahoo Finance). Safe to omit or send `null`.

### New — Resources & Reserves (all optional, all strings)
Free-form copy from the technical report. Empty string `""` if not reported. Include grade where the report does.

- `resource_measured` — e.g. `"1.2 Moz Au @ 1.5 g/t"`
- `resource_indicated` — e.g. `"3.4 Moz Au @ 1.1 g/t"`
- `resource_inferred` — e.g. `"850 koz Au @ 0.9 g/t"`
- `reserve_proven` — e.g. `"450 koz Au @ 1.8 g/t"`
- `reserve_probable` — e.g. `"1.1 Moz Au @ 1.4 g/t"`

For polymetallic projects, use the company's preferred equivalent string verbatim (e.g. `"10.5 Moz AgEq @ 120 g/t"`, `"85 kt CuEq @ 0.8%"`). Max 120 chars per field.

If a category is not reported in the technical report, use `""` (empty string), not a guess.

### New — Share Structure
- `shares_issued_outstanding` — integer count of shares (e.g. `153200000`), or `null` if unknown.
- `shares_fully_diluted` — integer count including all warrants and options, or `null` if unknown.
- `share_instruments` — array of warrant and option tranche objects. Empty array `[]` or omit entirely if unknown.

#### `share_instruments[]` object shape

| Field | Type | Required | Notes |
|---|---|---|---|
| `type` | `"warrant"` or `"option"` | yes | Lowercase. Anything else is dropped. |
| `count` | integer | yes | Number of warrants/options in this tranche |
| `strike_price` | number or null | optional | In the company's listing currency. `null` if unknown. |
| `expiry` | ISO date string `"YYYY-MM-DD"` or null | optional | `null` if unknown or perpetual |
| `notes` | string | optional | Short label, e.g. `"Tranche A"`, `"Broker warrants"`, `"Director options"` |

One object per tranche. Group warrants/options by strike + expiry — don't bundle different strikes into a single row. Director options can be bundled into one row if the strikes are similar.

---

## Behaviour notes

- All new fields are **optional**. The processor accepts old-format JSON without them — it just won't fill the new sidebar panels.
- The processor **deletes prior scorecards** for the ticker before creating the new one (this is intentional — only the current scorecard is canonical).
- `share_instruments` are **replaced wholesale** each run, not merged.
- Currency on `strike_price` is rendered in the template based on the company's `exchange` (TSX/TSXV → C$, ASX → A$, LSE → £, else US$). Send the raw decimal — don't include a currency symbol.

---

## Where to update the agent prompt

The research agent itself runs outside this repo (separate Claude Code session). Paste the schema block above into the agent's system prompt, replacing the previous JSON example. Make sure the prompt instructs the agent to:

1. Use empty string `""` for resource/reserve categories not reported (don't guess).
2. Use `null` for unknown share counts (don't guess).
3. Send `share_instruments: []` if it can't get a clean list — partial data is worse than no data.
4. Pull warrant/option details from the latest MD&A or AIF, not from press-release summaries.
