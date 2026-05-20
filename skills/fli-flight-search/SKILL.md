---
name: fli-flight-search
description: Flight search and fare research using Fli, a Python CLI/MCP tool for Google Flights data. Use when the user asks to search flights, compare routes, find cheaper travel dates, apply airline/cabin/stop filters, or prepare a travel options report.
labels:
  - Travel
  - Research
---

# Fli Flight Search

Use this skill to help users search and compare public flight options through Fli. Fli provides a CLI, Python package, and MCP server for Google Flights data. Treat results as live travel research, not booking confirmation.

## Core Rules

- Ask for missing essentials before running a search: origin, destination, travel date or date range, passenger count, cabin class, one-way vs round trip, and any stop or airline preferences.
- Use IATA airport or city codes where possible, such as `JFK`, `LHR`, `SFO`, or `NYC`.
- Do not book, reserve, or purchase flights. Provide options and explain that prices and availability can change.
- Prefer concise comparison tables with price, airline, duration, stops, departure/arrival times, and major caveats.
- Save useful search outputs under `travel/<trip-slug>/` when the user wants a report or repeated comparison.

## Runtime

Run Fli through this skill's Python project so dependencies stay isolated:

```bash
uv run --project /fluso/user/workspace/skills/fli-flight-search fli --help
```

If `uv` or the command fails because dependencies are not prepared yet, report the blocker clearly. Do not install large unrelated browser or video dependencies for this skill.

## Flight Searches

For a fixed-date one-way or round-trip search:

```bash
uv run --project /fluso/user/workspace/skills/fli-flight-search fli flights JFK LHR 2026-10-25
```

Round trip:

```bash
uv run --project /fluso/user/workspace/skills/fli-flight-search fli flights JFK LHR 2026-10-25 --return 2026-11-02
```

Common filters:

```bash
uv run --project /fluso/user/workspace/skills/fli-flight-search fli flights JFK LHR 2026-10-25 \
  --return 2026-11-02 \
  --class ECONOMY \
  --stops ONE_STOP \
  --sort CHEAPEST \
  --currency USD \
  --language en-US \
  --country US
```

Use `--format json` when structured comparison is useful, but mention that Fli marks machine-readable JSON as experimental and the schema may change.

## Flexible-Date Searches

Use date search when the user wants the cheapest travel window:

```bash
uv run --project /fluso/user/workspace/skills/fli-flight-search fli dates JFK LHR \
  --from 2026-10-01 \
  --to 2026-10-31 \
  --duration 7 \
  --round \
  --sort \
  --currency USD
```

Summarize the best candidate dates and explain any tradeoffs such as inconvenient times, long layovers, or airline restrictions.

## Multi-City Searches

For multi-city trips, use one `--leg` per segment:

```bash
uv run --project /fluso/user/workspace/skills/fli-flight-search fli multi \
  --leg SEA,NRT,2026-12-26 \
  --leg NRT,HKG,2026-12-30 \
  --leg HKG,SEA,2027-01-05 \
  --class ECONOMY \
  --sort CHEAPEST
```

## MCP Usage

If the user asks for assistant-tool integration, Fli also exposes:

- `fli-mcp` for STDIO MCP clients
- `fli-mcp-http` for an HTTP MCP endpoint, normally at `http://127.0.0.1:8000/mcp/`

Inside Fluso, prefer direct CLI calls unless the user specifically needs MCP configuration.

## Output Quality

Before finishing:

- Confirm the query parameters used.
- Separate direct results from your recommendation.
- Mention when no results, rate limits, or upstream temporary failures affect confidence.
- Include the observed search time/date in reports.
- Avoid presenting flight data as guaranteed availability.
