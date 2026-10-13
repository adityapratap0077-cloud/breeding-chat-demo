# Conversational Query Layer for Rice Breeding Trial Data: Synopsis

## The problem

Salt-tolerance breeding programs generate large volumes of trial data:
variety performance across seasons, salinity thresholds, SES screening scores,
and marker information such as the Saltol QTL. This data typically lives in
spreadsheets, PDFs, and scattered publications. Answering a simple question,
for example which aman-season varieties held yield above 4 t/ha under
salinity, or how Pokkali compares with FL478, requires manual digging through
those files each time.

## The solution

A conversational query layer: researchers ask plain-language questions and
get answers with the actual numbers, drawn from the underlying data. No
spreadsheet work, no manual cross-referencing.

## How it works

The demo has three parts:

1. **Compiled dataset.** 19 rice varieties (released BRRI and BINA
   salt-tolerant varieties, landrace donors such as Pokkali and Nona Bokra,
   breeding lines such as FL478, and standard checks such as IR29), with
   yields under saline and non-saline conditions, salinity thresholds, SES
   scores, and Saltol marker information. Every value is taken from published
   IRRI, BRRI, and BINA trial tables; each row cites its source. Blank cells
   mean the value was not found in the consulted sources.
2. **Deterministic retrieval.** A question is parsed for variety names, yield
   thresholds, seasons, tolerance classes, and marker terms, and the matching
   rows are pulled from the dataset. No guessing.
3. **Grounded answering.** A language model (accessed through my own
   self-hosted AI gateway, no third-party data sharing) composes the answer
   strictly from the retrieved rows. It is instructed to cite the numbers,
   to say when values come from different studies and are not strictly
   comparable, and to state plainly when the dataset does not cover a
   question rather than invent an answer.

## Current status

A working demo is live: a simple chat interface over the compiled dataset,
verified with ranking, comparison, threshold, marker, and out-of-scope
questions — https://breeding-chat-demo.vercel.app. It is a demonstration
on published data, built by a final-year B.Sc. Biotechnology student, and
claims no affiliation with IRRI, BRRI, BINA, or BRAC.

## The ask

To make this useful for BRAC's breeding programs, the layer needs to run on
real program data rather than published tables. What would help:

- The typical format of your marker and trial data (file types, columns,
  approximate size), so the demo can be rebuilt around your actual workflow.

Contact: Aditya Pratap, final-year B.Sc. (Hons) Biotechnology,
Bundelkhand University, India.
