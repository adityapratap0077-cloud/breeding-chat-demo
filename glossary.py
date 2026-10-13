"""Glossary for basic (non-variety-specific) questions.

Textbook-level background knowledge: units, scores, institutions, seasons,
breeding terms. These are general facts, NOT trial data — answers built from
this module are labeled as background so they are never confused with the
published trial figures in breeding_trials.csv.
"""

DEFINITIONAL = ("what is", "what are", "what was", "what does", "what do",
                "why", "how does", "how do", "how is", "how are",
                "explain", "define", "meaning of", "tell me about")

# Each entry: (keyword tuples, answer, definitional_only).
# definitional_only entries answer only "what is / why / how" style questions,
# so data questions mentioning the same words (e.g. "which boro varieties…")
# still reach the trial-data filters.
ENTRIES = [
    (("ds/m", "decisiemens", "electrical conductivity", "salinity unit",
      "measure salinity"),
     "Salinity in rice fields is measured as electrical conductivity (EC) in "
     "decisiemens per metre (dS/m). Roughly: below 2 dS/m is non-saline for "
     "rice, 2-4 is slight, 4-8 moderate, and above 8 high. Most rice suffers "
     "yield loss above 3-4 dS/m; the tolerant varieties in this dataset "
     "survive 8-14 dS/m at seedling stage. This is background knowledge, "
     "not trial data.",
     True),

    (("ses", "standard evaluation", "injury score", "scoring"),
     "SES is IRRI's Standard Evaluation System for rice: a 1-9 visual scale "
     "scoring salt-injury symptoms (leaf damage, survival). Lower is better — "
     "1-3 means tolerant, 4-6 moderately tolerant, 7-9 susceptible. Scores in "
     "this dataset come from hydroponic or field screening at stated "
     "salinity levels. This is background knowledge, not trial data.",
     True),

    (("saltol",),
     "Saltol is a major quantitative trait locus (QTL) for seedling-stage "
     "salinity tolerance on rice chromosome 1, originally mapped from the "
     "tolerant landrace Pokkali. It is associated with shoot Na+/K+ "
     "homeostasis under salt stress and has been introgressed into many "
     "breeding lines by marker-assisted selection. This is background "
     "knowledge, not trial data.",
     False),

    (("qtl", "quantitative trait"),
     "A QTL (quantitative trait locus) is a region of the genome associated "
     "with variation in a quantitative trait — one controlled by many genes, "
     "like yield or salt tolerance. Breeders use DNA markers linked to QTLs "
     "such as Saltol to select tolerant plants without waiting for field "
     "screening (marker-assisted selection). This is background knowledge, "
     "not trial data.",
     False),

    (("marker-assisted", "marker assisted", " mas "),
     "Marker-assisted selection (MAS) means selecting breeding plants by DNA "
     "markers linked to a desired trait (e.g. Saltol for salinity tolerance) "
     "instead of only by field performance. It speeds up breeding because "
     "selection can happen at the seedling stage in the lab. This is "
     "background knowledge, not trial data.",
     False),

    (("boro", "aman", "aus ", "growing season"),
     "Bangladesh and West Bengal grow rice in three seasons: aus "
     "(pre-monsoon, roughly April-August), aman (monsoon, July-December, "
     "mostly rainfed), and boro (dry winter season, November-May, fully "
     "irrigated). Salinity pressure is worst in boro in coastal areas, when "
     "river flows are low and seawater intrudes. This is background "
     "knowledge, not trial data.",
     True),

    (("brri", "bangladesh rice research"),
     "BRRI is the Bangladesh Rice Research Institute, the national institute "
     "that has released most of Bangladesh's modern rice varieties, including "
     "the salt-tolerant BRRI dhan47, 53, 54, 55, 61 and 67 in this dataset. "
     "This is background knowledge, not trial data.",
     True),

    (("bina", "nuclear agriculture"),
     "BINA is the Bangladesh Institute of Nuclear Agriculture, which "
     "developed salt-tolerant varieties such as Binadhan-8 and Binadhan-10 "
     "using mutation breeding alongside conventional methods. This is "
     "background knowledge, not trial data.",
     True),

    (("irri", "international rice research"),
     "IRRI is the International Rice Research Institute, headquartered at Los "
     "Banos, Philippines. It maintains the world rice genebank, developed "
     "the SES screening system, and released breeding lines such as FL478. "
     "This is background knowledge, not trial data.",
     True),

    (("landrace",),
     "A landrace is a traditional, farmer-selected crop population adapted to "
     "local conditions over centuries — genetically diverse, not formally "
     "bred. Pokkali (Kerala) and Nona Bokra are salt-tolerant rice landraces "
     "used as donors of tolerance genes in modern breeding. This is "
     "background knowledge, not trial data.",
     True),

    (("pokkali",),
     "Pokkali is a traditional salt-tolerant rice landrace from coastal "
     "Kerala, India. It is the original donor of the Saltol QTL on "
     "chromosome 1 and the tolerant parent of the breeding line FL478 "
     "(Pokkali x IR29). It is not grown for yield — its value is genetic. "
     "See the dataset for its screening scores. This is background "
     "knowledge, not trial data.",
     True),

    (("fl478",),
     "FL478 is a salt-tolerant recombinant inbred breeding line from the "
     "cross Pokkali x IR29, developed at IRRI. It carries Saltol on "
     "chromosome 1 and outperformed Pokkali at the seedling stage in some "
     "screenings. See the dataset for its scores. This is background "
     "knowledge, not trial data.",
     True),

    (("salt stress", "osmotic", "ion toxicity", "sodium", "hurt", "damage"),
     "Salinity hurts rice in two ways: first osmotic stress (salt in the soil "
     "makes it harder for roots to take up water), then ion toxicity as "
     "sodium accumulates in leaves, damaging photosynthesis. Tolerant "
     "varieties limit sodium transport to shoots (partly via Saltol-linked "
     "mechanisms) and maintain a healthy Na+/K+ balance. This is background "
     "knowledge, not trial data.",
     True),

    (("salinity",),
     "Salinity means how much salt is dissolved in soil or water. A little "
     "is natural, but too much salt makes it hard for rice roots to absorb "
     "water and slowly poisons the leaves. Farmers measure it in dS/m — "
     "most rice struggles above 3–4 dS/m. This is background knowledge, "
     "not trial data.",
     True),

    (("what is rice", "what is paddy", "define rice", "rice meaning",
      "about rice", "about paddy"),
     "Rice (Oryza sativa) is the staple food for more than half the world's "
     "people. 'Paddy' usually means rice still in its husk, or rice growing "
     "in a flooded field. This demo covers salt-tolerant rice varieties "
     "from published trials. This is background knowledge, not trial data.",
     True),

    (("what is a variety", "what is variety", "what are varieties",
      "cultivar", "define variety", "variety meaning"),
     "A variety (or cultivar) is a named, uniform line of a crop bred for "
     "specific traits — like BRRI dhan47, bred for salt tolerance. Farmers "
     "pick varieties suited to their soil, season and climate. This is "
     "background knowledge, not trial data.",
     True),

    (("what is a gene", "what is gene", "what is dna", "define gene",
      "gene meaning", "genome"),
     "A gene is a section of DNA carrying instructions for one trait, like "
     "grain size or salt tolerance. Rice has around 40,000 genes. Breeders "
     "track useful genes — such as Saltol — using DNA markers. This is "
     "background knowledge, not trial data.",
     True),

    (("what is breeding", "plant breeding", "define breeding",
      "breeding meaning"),
     "Plant breeding is selecting and crossing plants over generations to "
     "combine useful traits — for example, crossing a high-yielding variety "
     "with a salt-tolerant landrace. Modern breeders also use DNA markers "
     "to pick the right seedlings in the lab. This is background knowledge, "
     "not trial data.",
     True),

    (("germination",),
     "Germination is when a seed sprouts and starts growing. In salinity "
     "screening, seeds are germinated in salty water to see which lines "
     "survive — a quick first test before field trials. This is background "
     "knowledge, not trial data.",
     True),

    (("screening", "hydroponic", "field trial", "tested"),
     "Salinity tolerance is screened two main ways: hydroponic screening "
     "(seedlings grown in nutrient solution with added salt, scored by SES) "
     "is fast and uniform; field screening in saline soils reflects real "
     "conditions but varies with weather. A variety tolerant at seedling "
     "stage is not always tolerant at flowering — the dataset notes the "
     "stage where stated. This is background knowledge, not trial data.",
     True),

    (("t/ha", "tonnes per hectare", "yield unit", "what is yield"),
     "Rice yield is reported in tonnes per hectare (t/ha). In this dataset, "
     "'saline yield' means yield measured under salt stress in the cited "
     "trial, and 'non-saline yield' means yield without salinity — often the "
     "variety's potential or normal-condition yield. Figures from different "
     "studies are not directly comparable. This is background knowledge, "
     "not trial data.",
     True),

    (("hello", " hi ", " hey ", "greetings", "namaste", "good morning",
      "good afternoon", "good evening", "bye", "goodbye"),
     "Hello! Ask me about salt-tolerant rice varieties — which ones hold "
     "yield under salinity, how Pokkali compares to FL478, or what the "
     "Saltol marker is. I can also explain basics like dS/m, the SES score, "
     "or rice-growing seasons.",
     False),

    (("thank you", "thanks", "thankyou", "shukriya", "dhanyavad"),
     "You're welcome! Ask anytime — basic or advanced, I'm here for rice "
     "breeding questions.",
     False),

    (("who built", "who made", "who created", "your creator",
      "aditya pratap"),
     "I was built by Aditya Pratap, a final-year B.Sc. Biotechnology student "
     "at Bundelkhand University, India, as a demo of conversational search "
     "over published breeding-trial data. No affiliation with IRRI, BRRI, "
     "BINA or BRAC.",
     False),
]


def lookup(question):
    """Return a glossary answer string, or None if nothing matches."""
    qs = question.lower().strip()
    q = " " + qs + " "
    is_definitional = qs.startswith(DEFINITIONAL)
    for keywords, answer, def_only in ENTRIES:
        if def_only and not is_definitional:
            continue
        if any(k in q for k in keywords):
            return answer
    return None
