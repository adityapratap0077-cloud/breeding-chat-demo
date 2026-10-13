# Salt-Tolerant Rice Breeding — Demo Query Assistant

A conversational chatbot over published salt-tolerant rice trial data.
Built as a student demo for Prof. Zeba Islam Seraj (BRAC University) and
Dr. Arif (BRAC agricultural research center).

## What it is

Ask plain-language questions ("which aman varieties held yield above 4 t/ha
under salinity?", "compare Pokkali and FL478", "what is the Saltol QTL?").
The backend retrieves the relevant rows from a compiled dataset of 43 rice
varieties and an LLM composes a grounded answer **only from those rows** —
it says plainly when the data does not cover a question.

## Honesty rules (built in)

- Every number comes from `data/breeding_trials.csv`; sources per row in `SOURCES.md`.
- Blank cell = "not found in consulted sources", never zero, never invented.
- Values come from different studies/seasons and are not strictly comparable —
  the assistant says this when comparing.
- The UI states it is a demo on published data and claims **no affiliation**
  with IRRI, BRRI, BINA, or BRAC.

## Run locally

```bash
cd ~/workspace/breeding-chat-demo
python3 app.py --port 8471
# open http://localhost:8471/
```

Stdlib only — no pip packages needed.

The chat API needs the OmniRoute gateway at `http://localhost:20128/v1`
(OpenAI-compatible). It reads the key from
`~/workspace/vendor/omniroute/.gateway-key` (0600, never logged).
If the gateway is down, the UI still shows the retrieved rows with a notice.

## Files

- `app.py` — stdlib HTTP server: serves the UI + `POST /api/chat`
- `retriever.py` — deterministic retrieval: variety-name matching, yield
  thresholds, season/tolerance filters, Saltol-marker queries, ranking,
  out-of-scope detection
- `llm.py` — grounded answering via the OmniRoute gateway (strict system
  prompt; model fallback chain; honors `retry_after`)
- `static/index.html` — chat UI (example questions, sources link, disclaimers)
- `data/breeding_trials.csv` — 43 varieties, real published numbers
- `SOURCES.md` — every source with title and URL
- `test_questions.py` — the 5-question verification suite

## Verified

5-question suite run against the live local server: ranking query, comparison
query, threshold filter, Saltol/marker query, and an out-of-scope question
(wheat) — the last correctly refused without hallucinating.

## Not done / known limits

- Not deployed anywhere (Aditya approves all deploys).
- 19 rows is a demo slice, not a database; several cells are blank where no
  published value was found.
- Retrieval is keyword/pattern based, not embeddings — unusual phrasings may
  fall back to the general tolerant-variety listing.
- LLM quality depends on the gateway's upstream providers (groq free tier
  rate-limits under heavy use; gemini-3.1-flash-lite is the primary).
