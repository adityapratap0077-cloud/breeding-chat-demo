"""Manual verification: ask the 5 required questions against the local server
and print questions + answers + rows used. Run while app.py is serving."""
import json
import urllib.request

QUESTIONS = [
    # 1. ranking query
    "Which aman-season varieties are salt tolerant, ranked by saline yield?",
    # 2. comparison query
    "Compare Pokkali and FL478",
    # 3. threshold filter
    "Which varieties held yield above 4 t/ha under salinity in boro season?",
    # 4. Saltol / markers
    "What is the Saltol QTL and which varieties carry it?",
    # 5. out of scope (must not hallucinate)
    "What wheat varieties tolerate salinity?",
]

for i, q in enumerate(QUESTIONS, 1):
    req = urllib.request.Request(
        "http://127.0.0.1:8471/api/chat",
        data=json.dumps({"question": q}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode())
    print("=" * 70)
    print("Q%d: %s" % (i, q))
    print("mode:", data["mode"], "| rows:",
          ", ".join(r["variety"] for r in data["rows_used"]) or "none")
    print("-" * 70)
    print(data["answer"])
    print()
