"""Retrieval over the breeding-trials dataset.

Plain-language question -> relevant rows. Deterministic, no LLM involved:
name matching, numeric threshold parsing, season / tolerance-class filters,
Saltol-marker queries, ranking queries, and out-of-scope detection.
"""
import csv
import os
import re

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "breeding_trials.csv")

# Aliases: normalized token -> canonical variety name as in the CSV.
ALIASES = {
    "brridhan47": "BRRI dhan47", "dhan47": "BRRI dhan47",
    "brridhan53": "BRRI dhan53", "dhan53": "BRRI dhan53",
    "brridhan54": "BRRI dhan54", "dhan54": "BRRI dhan54",
    "brridhan55": "BRRI dhan55", "dhan55": "BRRI dhan55",
    "brridhan61": "BRRI dhan61", "dhan61": "BRRI dhan61",
    "brridhan67": "BRRI dhan67", "dhan67": "BRRI dhan67",
    "brridhan40": "BRRI dhan40", "dhan40": "BRRI dhan40",
    "brridhan41": "BRRI dhan41", "dhan41": "BRRI dhan41",
    "brridhan52": "BRRI dhan52", "dhan52": "BRRI dhan52",
    "brridhan28": "BRRI dhan28", "dhan28": "BRRI dhan28",
    "binadhan8": "Binadhan-8", "bina8": "Binadhan-8",
    "binadhan10": "Binadhan-10", "bina10": "Binadhan-10",
    "pokkali": "Pokkali",
    "fl478": "FL478",
    "ir29": "IR29",
    "ir64": "IR64",
    "nonabokra": "Nona Bokra",
    "sr26b": "SR26B",
    "csr28": "CSR28",
}

DOMAIN_WORDS = [
    "rice", "variety", "varieties", "yield", "salin", "salt", "tolerant",
    "tolerance", "ses", "qtl", "marker", "boro", "aman", "aus", "dhan",
    "breeding", "trial", "paddy", "dsm", "hectare", "t/ha", "landrace",
    "pokkali", "fl478", "ir29", "ir64", "binadhan", "brri", "bina", "irri",
    "check", "donor", "chromosome",
]

OUT_OF_SCOPE_CROPS = ["wheat", "maize", "corn", "barley", "soybean", "cotton",
                      "sugarcane", "potato", "mustard", "lentil", "chickpea"]


def _salinity_nums(text):
    """dS/m tolerance numbers; years stripped so they cannot pollute."""
    clean = re.sub(r"\b(19|20)\d{2}\b", " ", text or "")
    return [float(x) for x in re.findall(r"\d+(?:\.\d+)?", clean)]


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _yield_nums(text):
    """Numbers inside a yield field. dS/m expressions (e.g. '8-12 dS/m') and
    years are removed first; every remaining number is a yield figure."""
    clean = re.sub(r"\b(19|20)\d{2}\b", " ", text or "")
    clean = re.sub(r"\d+(?:\.\d+)?\s*(?:-|–|to)\s*\d+(?:\.\d+)?\s*d\s*s\s*/?\s*m",
                   " ", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\d+(?:\.\d+)?\s*d\s*s\s*/?\s*m", " ", clean,
                   flags=re.IGNORECASE)
    return [float(x) for x in re.findall(r"\d+(?:\.\d+)?", clean)]


def load_rows():
    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    by_name = {r["variety"]: r for r in rows}
    for r in rows:
        r["_saline_nums"] = _yield_nums(r.get("yield_saline_tha", ""))
        r["_normal_nums"] = _yield_nums(r.get("yield_normal_tha", ""))
        r["_salinity_nums"] = _salinity_nums(r.get("salinity_tolerance_dsm", ""))
    # register aliases
    alias_map = {}
    for token, name in ALIASES.items():
        if name in by_name:
            alias_map[token] = name
    return rows, by_name, alias_map


def _mentioned_varieties(question, alias_map):
    q = _norm(question)
    found = []
    for token, name in sorted(alias_map.items(), key=lambda kv: -len(kv[0])):
        if token in q and name not in found:
            found.append(name)
    return found


def _threshold(question):
    """Parse 'above|over|at least|>=|more than X t/ha' -> (op, value).
    A number followed by dS/m is a salinity threshold, not a yield
    threshold, and is ignored here (handled by _salinity_ask)."""
    ql = question.lower()
    m = re.search(
        r"(above|over|more than|at least|minimum of|>=?|exceeding)\s*(\d+(?:\.\d+)?)\s*(?:t\s*/?\s*ha)?",
        ql,
    )
    if m:
        after = ql[m.end():m.end() + 8]
        if not re.match(r"\s*d\s*s\s*/?\s*m", after):
            return (">=", float(m.group(2)))
    m = re.search(
        r"yield[^.?!]{0,40}?(\d+(?:\.\d+)?)\s*t\s*/?\s*ha",
        question.lower(),
    )
    if m and any(w in ql for w in ["above", "over", "than", "at least", "minimum"]):
        return (">=", float(m.group(1)))
    return None


def _salinity_ask(question):
    m = re.search(r"(\d+(?:\.\d+)?)\s*d\s*s\s*/?\s*m", question.lower())
    if m:
        return float(m.group(1))
    return None


def retrieve(question):
    """Return dict: rows (list), mode, note. Never raises on odd input."""
    rows, by_name, alias_map = load_rows()
    q = question.lower().strip()
    if not q:
        return {"rows": [], "mode": "empty", "note": "empty question"}

    # Hard out-of-scope: other crops.
    if any(c in q for c in OUT_OF_SCOPE_CROPS):
        return {"rows": [], "mode": "out_of_scope",
                "note": "question is about a different crop"}

    named = _mentioned_varieties(question, alias_map)
    if named:
        return {"rows": [by_name[n] for n in named],
                "mode": "named", "note": "varieties named in question"}

    # Saltol / marker questions -> rows carrying QTL info + checks.
    if any(w in q for w in ["saltol", "qtl", "marker", "chromosome", "gene"]):
        marked = [r for r in rows if r.get("key_qtl", "").strip()]
        checks = [by_name[n] for n in ["IR29"] if n in by_name]
        seen = set()
        out = []
        for r in marked + checks:
            if r["variety"] not in seen:
                seen.add(r["variety"])
                out.append(r)
        return {"rows": out, "mode": "marker",
                "note": "rows carrying Saltol/QTL information"}

    # Season filter.
    season = None
    for s in ["boro", "aman", "aus"]:
        if s in q:
            season = s
            break

    # Tolerance-class filter. "Under salinity / in saline areas / salt stress"
    # implies the asker wants tolerant varieties even without the word.
    saline_context = any(w in q for w in ["under salinity", "in saline",
                                          "saline areas", "salt stress",
                                          "saline-prone"])
    want_tolerant = (any(w in q for w in ["tolerant", "tolerance"]) or
                     saline_context) and \
        "not" not in q and "sensitive" not in q and "susceptible" not in q
    want_sensitive = any(w in q for w in ["sensitive", "susceptible", "not tolerant"])

    pool = list(rows)
    if season:
        pool = [r for r in pool if season in r.get("season", "").lower()]
    if want_tolerant:
        pool = [r for r in pool if "tolerant" in r.get("tolerance_class", "").lower()
                and "not" not in r.get("tolerance_class", "").lower()]
    elif want_sensitive:
        pool = [r for r in pool if "sensitive" in r.get("tolerance_class", "").lower()]

    # Numeric yield threshold. In a salinity context the threshold applies to
    # saline yield only — a variety with no saline data must not qualify via
    # its normal-condition yield.
    thr = _threshold(question)
    if thr:
        op, val = thr
        def rep(r):
            if saline_context:
                nums = r["_saline_nums"]
            else:
                nums = r["_saline_nums"] or r["_normal_nums"]
            return min(nums) if nums else None
        pool = [r for r in pool if rep(r) is not None and rep(r) >= val]

    # Salinity-level ask: keep rows tolerating at least that level.
    sal = _salinity_ask(question)
    if sal and ("tolerat" in q or "survive" in q or "dS" in question or "ds" in q):
        pool = [r for r in pool
                if r["_salinity_nums"] and max(r["_salinity_nums"]) >= sal]

    # Ranking: sort by saline yield (fallback normal), descending. When the
    # question is about saline performance, rows without saline data sort last.
    if any(w in q for w in ["highest", "top", "best", "rank", "most"]) and \
            any(w in q for w in ["yield", "perform"]):
        saline_q = saline_context or "saline" in q
        def rep(r):
            if saline_q:
                return max(r["_saline_nums"]) if r["_saline_nums"] else -1
            nums = r["_saline_nums"] or r["_normal_nums"]
            return max(nums) if nums else -1
        pool = sorted(pool, key=rep, reverse=True)
        return {"rows": pool[:8], "mode": "ranking",
                "note": "ranked by reported yield (saline preferred)"}

    if season or want_tolerant or want_sensitive or thr or sal:
        return {"rows": pool[:10], "mode": "filtered",
                "note": "filtered by season/tolerance/threshold"}

    # Domain relevance check -> out of scope.
    if not any(w in q for w in DOMAIN_WORDS):
        return {"rows": [], "mode": "out_of_scope",
                "note": "no domain terms matched"}

    # Fallback: broad tolerant-variety listing, capped.
    general = [r for r in rows
               if "tolerant" in r.get("tolerance_class", "").lower()
               and "not" not in r.get("tolerance_class", "").lower()]
    return {"rows": general[:10], "mode": "general",
            "note": "general tolerant-variety listing"}
