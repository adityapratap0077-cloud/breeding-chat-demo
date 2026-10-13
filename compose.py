"""Deterministic answer composer for the breeding-chat demo.

Used when the LLM gateway is unreachable (e.g. on public hosting). Every
sentence is built from retrieved dataset rows only — no generation, no
hallucination risk. A good fit for a scientific audience.
"""
import retriever

CAVEAT = ("Note: values come from different studies, seasons and trial "
          "conditions, so they are not strictly comparable row-to-row.")


def _clean(v):
    v = (v or "").strip()
    return v if v else None


def _row_facts(r):
    """One factual line per variety, only from non-blank cells."""
    bits = [r["variety"]]
    tc = _clean(r.get("tolerance_class"))
    if tc:
        bits.append("salt-tolerance: " + tc)
    sy = _clean(r.get("yield_saline_tha"))
    if sy:
        bits.append("saline yield " + sy)
    ny = _clean(r.get("yield_normal_tha"))
    if ny:
        bits.append("non-saline yield " + ny)
    st = _clean(r.get("salinity_tolerance_dsm"))
    if st:
        bits.append("tolerates " + st)
    ses = _clean(r.get("ses_score"))
    if ses:
        bits.append("SES " + ses)
    qtl = _clean(r.get("key_qtl"))
    if qtl:
        bits.append("QTL: " + qtl)
    season = _clean(r.get("season"))
    if season:
        bits.append(season + " season")
    return "; ".join(bits) + "."


def _top_number(r):
    """Best single yield figure for ranking display. Uses the retriever's
    own parser so years and dS/m expressions never leak in as yields."""
    for col in ("yield_saline_tha", "yield_normal_tha"):
        nums = retriever._yield_nums(r.get(col, ""))
        if nums:
            return "%s (%s)" % (max(nums), col.replace("yield_", "")
                                .replace("_tha", ""))
    return None


def compose(question, rows, mode, _note, glossary_text=None):
    if mode == "glossary":
        return glossary_text or "No background entry found for that question."
    if mode == "empty" or not (question or "").strip():
        return ("Please ask a question about the rice varieties in the "
                "demo dataset.")
    if mode == "out_of_scope":
        return ("This demo only covers salt-tolerant rice varieties — yields, "
                "salinity thresholds, SES screening scores and Saltol marker "
                "information from published IRRI, BRRI and BINA trials. "
                "It does not cover that topic.")
    if not rows:
        return ("The demo dataset has no rows matching that question. It "
                "covers 19 salt-tolerant rice varieties: released BRRI/BINA "
                "varieties, landrace donors such as Pokkali and Nona Bokra, "
                "breeding lines such as FL478, and checks such as IR29.")
    if mode == "named":
        lines = [_row_facts(r) for r in rows]
        return ("From the dataset:\n" + "\n".join(lines) + "\n" + CAVEAT)
    if mode == "marker":
        lines = []
        for r in rows:
            qtl = _clean(r.get("key_qtl"))
            if qtl:
                lines.append("%s — %s." % (r["variety"], qtl))
        if not lines:
            lines = [_row_facts(r) for r in rows]
        return ("Saltol/marker information in the dataset:\n" +
                "\n".join(lines) + "\n" + CAVEAT)
    # filtered / ranking / general: list with the headline number.
    lines = []
    for i, r in enumerate(rows, 1):
        top = _top_number(r)
        line = "%d. %s" % (i, r["variety"])
        if top:
            line += " — " + top + " t/ha"
        tc = _clean(r.get("tolerance_class"))
        if tc:
            line += " (%s)" % tc
        lines.append(line + ".")
    intro = {"ranking": "Ranked by reported yield (saline preferred):",
             "filtered": "Varieties matching your filters:",
             "general": ("The dataset doesn't hold that exact detail — it "
                         "covers salt-tolerant rice varieties (yields, "
                         "salinity thresholds, SES scores, Saltol info). "
                         "Here are the tolerant varieties:")}.get(
                 mode, "Matching varieties:")
    return intro + "\n" + "\n".join(lines) + "\n" + CAVEAT
