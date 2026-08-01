---
tags:
  - type/meta
  - paper-guide
  - oskg-ibd
  - acquisition
created: 2026-08-01
updated: 2026-08-01
related:
  - "[[Book Guide]]"
  - "[[METHODOLOGY]]"
  - "[[sources/Sources Index]]"
---

# Paper Guide — OSKG-IBD

Research papers, systematic reviews, meta-analyses, and landmark clinical trials for the IBD/SIBO knowledge graph.

## Categories

| Category | Description | Treatment |
|----------|-------------|-----------|
| Guideline Papers | Journal versions of clinical guidelines (already listed in Guidelines Index) | Full extraction |
| Landmark Trials | RCTs that changed clinical practice | Full extraction of methods and results |
| Mechanistic Papers | Studies of pathophysiology and disease mechanisms | Targeted extraction |
| Review Papers | Systematic reviews and meta-analyses | Synthesis extraction |
| Methodological | Papers about diagnostic methods and their validation | Targeted extraction |

---

## SIBO: Diagnosis & Pathophysiology

| # | Title | First Author | Journal | Year | Status |
|---|-------|-------------|---------|------|--------|
| P1 | ACG Clinical Guideline: Small Intestinal Bacterial Overgrowth | Pimentel M | Am J Gastroenterol | 2020 | Acquired (see G3) |
| P2 | Small Intestinal Bacterial Overgrowth: A Comprehensive Review | Bures J | Gastroenterol Hepatol | 2010 | Acquired |
| P3 | Hydrogen and Methane-Based Breath Testing in GI Disorders: The North American Consensus | Rezaie A | Am J Gastroenterol | 2017 | Acquired |
| P4 | Methane, a Gas Produced by Enteric Bacteria, Slows Intestinal Transit and Augments Small Intestinal Contractile Activity | Pimentel M | Am J Physiol | 2006 | Acquired |

## SIBO: Treatment

| # | Title | First Author | Journal | Year | Status |
|---|-------|-------------|---------|------|--------|
| P5 | Rifaximin Therapy for Patients with IBS Without Constipation (TARGET 1 & 2) | Pimentel M | N Engl J Med | 2011 | Acquired |
| P6 | A 14-Day Elemental Diet Is Highly Effective in Normalizing the Lactulose Breath Test | Pimentel M | Dig Dis Sci | 2004 | Acquired (Sci-Hub browser extraction; PDF stub) |
| P7 | Herbal Therapy Is Equivalent to Rifaximin for the Treatment of SIBO | Chedid V | Glob Adv Health Med | 2014 | Acquired |

## IBD: Microbiome & Dysbiosis

| # | Title | First Author | Journal | Year | Status |
|---|-------|-------------|---------|------|--------|
| P8 | The Microbiome in Inflammatory Bowel Disease: Current Status and the Future Ahead | Kostic AD | Gastroenterology | 2014 | Acquired |
| P9 | The Intestinal Microbiota in Inflammatory Bowel Disease | Becker C (not Sartor) | ILAR J | 2015 | Acquired (Sci-Hub browser extraction; PDF stub) |
| P10 | The Role of Diet in the Pathogenesis and Management of Inflammatory Bowel Disease | Lewis JD | Gastroenterology | 2018 | Acquired |
| P11 | The Treatment-Naive Microbiome in New-Onset Crohn's Disease | Gevers D | Cell Host Microbe | 2014 | Acquired |

## IBD: Landmark Treatment Trials

| # | Title | First Author | Journal | Year | Status |
|---|-------|-------------|---------|------|--------|
| P12 | Infliximab, Azathioprine, or Combination Therapy for Crohn's Disease (SONIC) | Colombel JF | N Engl J Med | 2010 | Acquired |
| P13 | Infliximab for Induction and Maintenance Therapy for Ulcerative Colitis (ACT 1 & 2) | Rutgeerts P | N Engl J Med | 2005 | Acquired |
| P14 | Effect of Tight Control Management on Crohn's Disease (CALM) | Colombel JF | Lancet | 2017 | Partial — 1KB summary only. Full text paywalled; 3 Sci-Hub mirrors failed. Needs manual acquisition. |

## Diet & Nutritional Therapy

| # | Title | First Author | Journal | Year | Status |
|---|-------|-------------|---------|------|--------|
| P15 | Effects of Low-FODMAP Diet on Symptoms, Fecal Microbiome, and Markers of Inflammation in Patients With Quiescent IBD in a Randomized Trial | Cox SR | Gastroenterology | 2020 | Acquired |
| P16 | Crohn's Disease Exclusion Diet Plus Partial Enteral Nutrition Induces Sustained Remission (CDED) | Levine A | Gastroenterology | 2019 | Acquired (re-acquired via Sci-Hub; original file was wrong paper) |
| P17 | The Specific Carbohydrate Diet for Inflammatory Bowel Disease: A Systematic Review | Suskind DL | J Pediatr Gastroenterol Nutr | 2016 | Acquired * |

## SIBO-IBD Intersection

| # | Title | First Author | Journal | Year | Status |
|---|-------|-------------|---------|------|--------|
| P18 | Small Intestinal Bacterial Overgrowth in Crohn's Disease | Castiglione F | Inflamm Bowel Dis | 2013 | NOT FOUND — Paper not verifiable at this author/journal/year. Original download was a wrong paper (Vitamin D Selected Summaries). Needs replacement or removal. |
| P19 | Prevalence of SIBO in Patients with IBD: Systematic Review and Meta-Analysis | Shah A | Aliment Pharmacol Ther | 2019 | Acquired (Sci-Hub browser extraction; author/title/DOI confirmed. PAPER-GUIDE had incorrect journal/year) |

---

## Key Papers for Claims Extraction

The highest-priority papers for Phase 2:

1. **Pimentel (2020) — ACG SIBO Guideline.** Defines the current diagnostic and treatment standard. Every recommendation is a claim.
2. **Rezaie (2017) — North American Breath Test Consensus.** Defines test methodology and interpretation thresholds.
3. **Pimentel (2011) — TARGET 1 & 2.** The RCT evidence for rifaximin in SIBO/IBS.
4. **Colombel (2010) — SONIC.** Landmark RCT: combination therapy superiority in Crohn's.
5. **Colombel (2017) — CALM.** Treat-to-target vs symptom-based management. **Partial — full text not acquired.**
6. **Cox (2020) — Low-FODMAP in IBD.** The key diet-microbiome-symptoms trial.
7. **Shah (2019) — SIBO Prevalence Meta-Analysis.** The evidence synthesis on how common SIBO is in IBD. Journal corrected from Inflamm Bowel Dis.

---

## Acquisition

Papers are acquired via direct download from publisher websites. Most guideline-level papers are open access. Landmark NEJM/Lancet trials may require institutional access or Sci-Hub.

Papers go to `sources/papers/_pdfs/` (gitignored). After extraction to plain text, the text file goes to `sources/papers/` with the PDF filename as prefix.
