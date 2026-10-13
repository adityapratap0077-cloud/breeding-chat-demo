# Data sources — salt-tolerant rice demo dataset

Every row in `data/breeding_trials.csv` carries a `sources` column with one or
more of the keys below. Only published, checkable sources are used. Numbers are
facts extracted from these publications (not copied text). Where a value was
not found in any consulted source, the cell is left blank and the notes say so.

- **S1** — "Performances of Six Rice Varieties in Coastal Saline Soil of Bangladesh" (Wiley, 2025). Characteristics table for BRRI dhan28/47/67 (duration, height, yield, salinity thresholds). https://onlinelibrary.wiley.com/doi/10.1155/ioa/9525700
- **S2** — "Hope beyond salinity", The Daily Star (2009). BRRI dhan47 release (Jan 2007), 6.0–6.5 t/ha potential, 6 dS/m tolerance at flowering. https://www.thedailystar.net/news-detail-74553
- **S3** — Asian Journal of Agricultural and Horticultural Research (AJAHR). BRRI dhan47 parentage (IR 51511-B-34-B × TCCP 266-2-49-BB-3), 152-day duration, ~6.1 t/ha mean yield. https://journalajahr.com/index.php/AJAHR/article/download/322/632/508
- **S4** — BINA "SaltT Rice" presentation (Mirza Mofazzal Islam; slideshare). Released-variety fact sheets: Binadhan-8/10, BRRI dhan47/53/54/55 (season, duration, height, salinity thresholds, yields). https://www.slideshare.net/slideshow/saltt-rice/51015397
- **S5** — Ali et al., Bangladesh Rice Journal (BanglaJOL). Saline-area trial yields at Kalapara, Patuakhali, T. Aman 2013: BRRI dhan40 4.53, dhan41 4.36, dhan53 2.88, dhan54 4.30, dhan52 4.17 t/ha. https://banglajol.info/index.php/BRJ/article/download/37387/25311
- **S6** — Digital Herbarium of Crop Plants (BSMRAU). BRRI released-varieties register: release years, seasons, average yields (dhan47 2007/6.0, dhan53 2010/4.5, dhan54 2010/5.5, dhan55 2011/7.0, dhan61 2013/5.0, dhan40/41 2003/4.5, dhan52 2010/4.5). https://dhcrop.bsmrau.net/varieties-released/varieties-released-by-brri/
- **S7** — "Competitiveness of Winter Rice Varieties against Weed under Dry Direct Seeded Conditions" (SCIRP). Variety table with BRRI dhan47/55/67 and Binadhan-8/10 (release year, height, duration, yield, salt-tolerance flag). https://www.scirp.org/journal/paperabs?paperid=81491
- **S8** — BINA rice varieties fact sheet (bina.portal.gov.bd). Binadhan-10: released 2012, tolerates up to 12 dS/m, 5–6 t/ha under salt stress, 8.5 t/ha potential non-saline. http://bina.portal.gov.bd/sites/default/files/files/bina.portal.gov.bd/page/2fe324dc_6d39_455c_b522_15175672b318/Rice%20varieties%20-17.04.2016.pdf
- **S9** — BINA Biotechnology Division document. Binadhan-8: released 2010, 12–14 dS/m at seedling / 8–10 to maturity, 5.5 t/ha under salt stress, 8.0 t/ha potential non-saline. (Oracle Cloud object storage PDF, BINA office)
- **S10** — Kranto et al., "Evaluation for Salt Tolerance in Rice Using Multiple Screening Methods" (JAST, via academia.edu). Hydroponic SES scores at 8 dS/m: Pokkali 4.38 (tolerant), IR29 9.00 (susceptible). https://www.academia.edu/113952181/Evaluation_for_Salt_Tolerance_in_Rice_Using_Multiple_Screening_Methods
- **S11** — IRRI 231-line salinity screening (2026; via bioengineer.org). Tolerant checks CSR28 (3.7), FL478, Pokkali (injury < 4.5); Saltol QTL on chromosome 1 from Pokkali regulates Na+/K+ homeostasis. https://bioengineer.org/scientists-screen-231-rice-lines-to-find-hidden-salt-tolerance-beyond-the-famous-saltol-gene/
- **S12** — The Pharma Innovation Journal (2022). FL478 vs Pokkali salinity screening, Kerala polyhouse: FL478 SES 2.93 at 6 dS/m (outperformed Pokkali at seedling stage). https://www.thepharmajournal.com/archives/2022/vol11issue12/PartAN/11-12-334-357.pdf
- **S13** — IRRI Discussion Paper No. 22, "Screening manual" (knowledgebank.irri.org). SES table: Nona Bokra 3.0 (tolerant), IR29 7.0. http://www.knowledgebank.irri.org/ricebreedingcourse/documents/Screening_manual.pdf
- **S14** — Cereal Research Communications (via real.mtak.hu). SR26B noted as the most popular variety in coastal saline areas of eastern India. https://real.mtak.hu/37152/1/crc.2014.0045.pdf
- **S15** — "A successful salt-tolerant rice variety in Sreefalkathi Village", Rice Today (IRRI). IRRI–BRRI–BINA boro varieties (BRRI dhan47, BRRI dhan55, Binadhan-8, Binadhan-10): 5–7 t/ha non-saline, 3–5 t/ha in saline-prone areas; survive up to 10 dS/m. https://ricetoday.irri.org/a-successful-salt-tolerant-rice-variety-in-sreefalkathi-village/

## Compilation notes

- This is a demo dataset, not a research database. Values come from different
  studies, seasons, and trial conditions and are NOT directly comparable
  row-to-row; the `notes` column and the chat assistant both say this.
- Blank cells mean "not found in the consulted sources", never zero.
- Yield figures mix official potential yields, on-farm reports, and
  single-trial means — the source and context travel with each number.
- No affiliation with IRRI, BRRI, BINA, or BRAC is claimed anywhere.
