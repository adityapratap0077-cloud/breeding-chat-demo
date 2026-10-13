"""LLM answering over retrieved rows via the OmniRoute gateway.

Strict grounding: the model only sees the retrieved rows and is instructed to
answer from them, cite numbers, and say plainly when the data does not cover
the question. The gateway key is read from its 0600 file and never logged.
"""
import json
import os
import time
import urllib.error
import urllib.request

GATEWAY_URL = "http://localhost:20128/v1/chat/completions"
KEY_PATH = os.path.expanduser("~/workspace/vendor/omniroute/.gateway-key")
# Primary model; fallbacks tried in order on HTTP/transport errors.
# gemini-3.1-flash-lite is the reliable default (groq free tier 403s under
# repeated use). groq models kept as fallbacks.
MODELS = ["gemini/gemini-3.1-flash-lite",
          "groq/openai/gpt-oss-120b", "groq/openai/gpt-oss-20b"]
TIMEOUT_S = 90

SYSTEM = """You are a demo assistant for a salt-tolerant rice breeding dataset.
You are given table rows of published trial data. Rules:

1. Answer ONLY from the provided rows. Every number you state must appear in
   the rows. Never invent yields, scores, thresholds, or seasons.
2. If a row's cell is blank, say that value is not in the dataset — do not
   fill it in from general knowledge.
3. Values come from different studies, seasons, and trial conditions and are
   not strictly comparable row-to-row. Say this when comparing.
4. Keep answers short: 2-6 sentences plus the key numbers. Name the variety,
   the number, and the condition (e.g. "5.5 t/ha under salt stress").
5. If the rows do not cover the question, say so in one sentence and suggest
   what the dataset does cover. Never answer off-dataset questions from
   general knowledge.
6. Column meanings: tolerance_class describes the SALT-TOLERANCE level only,
   never yield. Yield figures come only from yield_normal_tha and
   yield_saline_tha. A blank cell means the value is not in the dataset.
7. No markdown tables. Plain sentences are fine.
"""


def _rows_text(rows):
    # Essential columns only — keeps prompts small for rate-limited upstreams.
    cols = ["variety", "developer", "release_year", "season",
            "yield_normal_tha", "yield_saline_tha", "salinity_tolerance_dsm",
            "tolerance_class", "ses_score", "key_qtl", "notes", "sources"]
    lines = []
    for r in rows:
        parts = [c + ": " + (r.get(c) or "-").strip() for c in cols
                 if (r.get(c) or "").strip()]
        lines.append(" | ".join(parts))
    return "\n".join(lines)


def _retry_after_seconds(err_body):
    """Honor the gateway's retry_after hint when present."""
    try:
        d = json.loads(err_body)
        ra = d.get("error", {}).get("retry_after")
        if isinstance(ra, (int, float)) and 0 < ra <= 120:
            return ra
    except Exception:
        pass
    return None


def answer(question, rows, note):
    """Return the assistant's answer string. Raises RuntimeError on failure."""
    if note in ("empty question",):
        return "Please ask a question about the rice varieties in the dataset."

    with open(KEY_PATH, encoding="utf-8") as f:
        key = f.read().strip()

    if not rows:
        user_msg = (
            "Question: " + question + "\n\n"
            "Retrieved rows: NONE. The dataset has no rows matching this question.\n"
            "Answer in one or two sentences: say the demo dataset does not cover "
            "this, and briefly say what it does cover (salt-tolerant rice varieties, "
            "yields, SES scores, Saltol marker info from published IRRI/BRRI/BINA trials)."
        )
    else:
        user_msg = (
            "Retrieved dataset rows:\n" + _rows_text(rows) + "\n\n"
            "Question: " + question
        )

    last_err = None
    for model in MODELS:
        body = json.dumps({
            "model": model,
            "temperature": 0.2,
            "max_tokens": 400,
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": user_msg},
            ],
        }).encode()

        req = urllib.request.Request(
            GATEWAY_URL,
            data=body,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer " + key},
            method="POST",
        )
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
                    payload = json.loads(resp.read().decode())
                try:
                    return payload["choices"][0]["message"]["content"].strip()
                except (KeyError, IndexError, TypeError):
                    last_err = "unexpected LLM response shape"
                    break
            except urllib.error.HTTPError as e:
                try:
                    err_body = e.read().decode()
                except Exception:
                    err_body = ""
                last_err = "HTTP %s: %s" % (e.code, err_body[:120])
                wait = _retry_after_seconds(err_body)
                if wait and attempt < 2:
                    time.sleep(wait + 1)
                    continue
                break
            except Exception as e:
                last_err = "%s: %s" % (type(e).__name__, str(e)[:120])
                break
    raise RuntimeError("LLM request failed: %s" % last_err)
