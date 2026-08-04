# 🌍 QuakeWatch

A data pipeline that grabs earthquake data from USGS, cleans the messy parts, and summarizes it with AI.

**🔗 Live demo:** https://quakewatch-ctbcdij43yvxhwnfeyyzfq.streamlit.app

---

## What it does

Pulls real earthquake data every run:

- **Fetch** — pulls the last hour of earthquakes from USGS
- **Validate** — checks each one, skips bad data, duplicates, and missing fields
- **Store** — saves clean records to SQLite
- **Summarize** — uses Claude to write a plain-English summary

---

## Why I built it this way

Real data is messy. Magnitudes go missing, the same event ID shows up twice, coordinates are garbage sometimes. This pipeline handles that instead of crashing.

Each part is also separate — fetch, validate, store, summarize. If something breaks, you know exactly where to look.

---

## What it handles (the not-so-obvious part)

| Problem | What it does |
|---|---|
| API times out | Retries — doesn't crash |
| Bad magnitude | Rejects it, logs why |
| Same earthquake twice | Dedupes by event ID |
| Missing coordinates | Skips the record |

---

## How to run it

```bash
git clone https://github.com/Fidan222/quakewatch.git
cd quakewatch
python3 -m venv venv
source venv/bin/activate
pip install requests python-dotenv anthropic
# Add your Anthropic API key to a .env file
python summarize_quakes.py
```

To run the dashboard:

```bash
python -m streamlit run app.py
```

---

## Tech stack

- **Python** — core logic
- **requests** — fetching data
- **SQLite** — local storage
- **Anthropic API (Claude)** — AI summaries
- **Streamlit** — dashboard

---

## What's next

- Schedule it to run automatically every few minutes
- Add a map to visualize earthquakes
- Track summaries over time to spot trends