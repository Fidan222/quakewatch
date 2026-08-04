# QuakeWatch

A data pipeline that grabs earthquake data from USGS, cleans the messy parts, and summarizes it with AI.

## What it does

Pulls real earthquake data every run:
- Fetch from USGS (last hour of earthquakes)
- Validate each one (skip bad data, duplicates, missing fields)
- Store clean records in SQLite
- Use Claude to write a summary in English

## Why I built it this way

Real data sucks. Magnitudes are missing, IDs show up twice, coordinates are garbage sometimes. This handles that stuff instead of crashing.

Also — each part is separate. Fetch, validate, store, summarize. If something breaks, you know exactly where.

## How to run

```bash
git clone https://github.com/Fidan222/quakewatch.git
cd quakewatch
python3 -m venv venv
source venv/bin/activate
pip install requests python-dotenv anthropic
# Add your API key to .env
python summarize_quakes.py
```

## What it does that's not obvious

- API timeouts? Retries. Doesn't crash.
- Bad magnitude? Rejected, logged.
- Same earthquake twice? Deduped by ID.
- Missing coordinates? Skipped.

## Next

- Schedule it to run every 5 min
- Add a map dashboard
- Track summaries over time