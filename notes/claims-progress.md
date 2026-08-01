---
tags: [type/tracker, oskg-ibd, phase-2, claims]
created: 2026-08-01
updated: 2026-08-01
related: ["[[claims-architecture]]", "[[Claims Index]]"]
---

# Claims Extraction Progress

Tracks Phase 2 claim extraction from all Phase 1 reading notes. Each note below maps to a batch; once extracted, claims are filed under `notes/claims/` and the note's frontmatter is updated with `claims_status: extracted`.

## Status Summary

- **Total reading notes:** 49
- **Claims extracted:** 476 (target: 400-600 ✓)
- **Notes with claims:** 47
- **Notes pending:** 2 (Microbiome Science Context, Sleisenger Yamada SIBO Source Assessment)
- **Intra-batch edges:** Pending
- **Tag enrichment:** Partial (60 sparse claims enriched)
- **Chapter note updates:** claims_status frontmatter added to all 49 notes; ### Claim N: block replacement deferred to t_c6076bcd

## Claims by Domain

| Domain | Source Count | Claim Count |
|--------|-------------|-------------|
| Pathophysiology | 1 source | 10 claims |
| Diagnosis | 2 sources | 15 claims |
| Treatment | 5 sources | 34 claims |
| Clinical Guidelines | 10 sources | ~270 claims |
| Microbiome & SIBO | 17 sources | 68 claims |
| Nutrition & Dietary | 11 sources | 54 claims |
| History & Context | 1 source | 1 claim |

## Batch 1: Pathophysiology + Diagnosis (Yamada 7E)

- [x] `notes/pathophysiology/Yamada 2022 - Ch62 IBD Pathogenesis.md` — 10 claims
- [x] `notes/diagnosis/Yamada 2022 - Ch63 Ulcerative Colitis Diagnosis.md` — 8 claims
- [x] `notes/diagnosis/Yamada 2022 - Ch64 Crohns Disease Diagnosis.md` — 7 claims

## Batch 2: Treatment (Steinhart + Yamada)

- [x] `notes/treatment/Steinhart 2018 - Ch7 Drug Therapy.md` — 10 claims
- [x] `notes/treatment/Steinhart 2018 - Ch8 Surgical Treatment.md` — 7 claims
- [x] `notes/treatment/Yamada 7E - Ch63 UC Clinical Manifestations and Management.md` — 6 claims
- [x] `notes/treatment/Yamada 7E - Ch64 Crohn's Disease Management.md` — 8 claims
- [x] `notes/treatment/Yamada 7E - Ch65 Surgical Treatment of IBD.md` — 3 claims

## Batch 3: Clinical Guidelines

- [x] `notes/clinical-guidelines/ACG Crohn's 2018 - Lichtenstein.md` — 88 claims (28 original + 60 recommendation-level)
- [x] `notes/clinical-guidelines/ACG UC 2019 - Rubin.md` — 67 claims (18 original + 49 recommendation-level)
- [x] `notes/clinical-guidelines/ACG SIBO 2020 - Pimentel.md` — 9 claims
- [x] `notes/clinical-guidelines/AGA SIBO 2020 - Quigley.md` — 4 claims
- [x] `notes/clinical-guidelines/AGA UC 2020 - Feuerstein.md` — 22 claims (11 original + 11 recommendation-level)
- [x] `notes/clinical-guidelines/AGA Crohn's 2021 - Feuerstein.md` — 12 claims (8 original + 4 recommendation-level)
- [x] `notes/clinical-guidelines/ECCO Diagnostic 2019 - Maaser.md` — 13 claims
- [x] `notes/clinical-guidelines/ECCO Crohn's Medical 2020 - Torres.md` — 11 claims
- [x] `notes/clinical-guidelines/ECCO UC Therapeutics 2022 - Raine.md` — 34 claims (14 original + 20 recommendation-level)
- [x] `notes/clinical-guidelines/Rome Foundation SIBO Report 2017.md` — 13 claims
- [x] `notes/clinical-guidelines/BSG IBD 2019 - Lamb.md` — 14 claims

## Batch 4: Microbiome & SIBO

- [x] `notes/microbiome/Pimentel 2022 - Intro Ch1 IBS and SIBO Overlap.md` — 7 claims
- [x] `notes/microbiome/Pimentel 2022 - Ch2 Gut Anatomy and MMC.md` — 6 claims
- [x] `notes/microbiome/Pimentel 2022 - Ch3 Gut Microbiome.md` — 5 claims
- [x] `notes/microbiome/Pimentel 2022 - Ch4 Food Poisoning Autoimmunity.md` — 5 claims
- [x] `notes/microbiome/Pimentel 2022 - Ch5 SIBO Definition and Diagnosis.md` — 6 claims
- [x] `notes/microbiome/Pimentel 2022 - Ch6 Three Pillars of SIBO Management.md` — 7 claims
- [x] `notes/microbiome/Pimentel 2022 - Ch9 Refractory SIBO.md` — 5 claims
- [x] `notes/microbiome/Pimentel 2022 - Ch10-11 Probiotics FMT and Myths.md` — 3 claims
- [x] `notes/microbiome/Pimentel 2006 - SIBO Theory Evolution 2006-2022.md` — 7 claims
- [x] `notes/microbiome/Yamada Ch58 - Bacterial Overgrowth Textbook.md` — 1 claim
- [x] `notes/microbiome/Sarna 2021 - Healing SIBO Patient Guide.md` — 5 claims
- [x] `notes/microbiome/LaPine 2021 - SIBO Made Simple Cookbook.md` — 3 claims
- [x] `notes/microbiome/The Microbiome Solution - Chutkan - Intro Ch1-3.md` — 4 claims
- [x] `notes/microbiome/The Microbiome Solution - Chutkan - Ch5 Dysbiosis.md` — 6 claims
- [x] `notes/microbiome/The Microbiome Solution - Chutkan - Ch11 Rewilding Illness.md` — 5 claims
- [x] `notes/microbiome/The Good Gut - Sonnenburg 2015.md` — 1 claim
- [ ] `notes/microbiome/Microbiome Science Context - Enders Mayer Bulsiewicz Yong.md` — pending (combined context)
- [ ] `notes/microbiome/Sleisenger Yamada SIBO Source Assessment.md` — skip (infrastructure)

## Batch 5: Nutrition & Dietary

- [x] `notes/nutrition/Gottschall 1994 - Foreword.md` — 3 claims
- [x] `notes/nutrition/Gottschall 1994 - Ch1-2 Origins and Scientific Evidence.md` — 5 claims
- [x] `notes/nutrition/Gottschall 1994 - Ch3-5 The Vicious Cycle Mechanism.md` — 8 claims
- [x] `notes/nutrition/Gottschall 1994 - Ch9-10 Implementing the SCD.md` — 5 claims
- [x] `notes/nutrition/Foote 2020 - Crohn's Disease Cookbook.md` — 7 claims
- [x] `notes/nutrition/Thompson 2013 - Elemental Diet Protocol.md` — 7 claims
- [x] `notes/nutrition/Sarna 2021 - Healing SIBO Dietary Protocol.md` — 5 claims
- [x] `notes/nutrition/Pimentel 2022 - Low-Fermentation Eating.md` — 5 claims
- [x] `notes/nutrition/Gut and Physiology Syndrome - Campbell-McBride - GAPS Protocol.md` — 6 claims
- [x] `notes/nutrition/The Paleo Approach - Ballantyne 2013.md` — 1 claim
- [x] `notes/nutrition/The Autoimmune Solution - Myers 2015.md` — 1 claim

## Batch 6: History + Tier 4

- [x] `notes/history/Inflamed - Marya Patel 2021.md` — 1 claim

## Session Log

### 2026-08-01 — Session 2 (Arron, run 23)
- Extracted 29 claims from 4 previously unextracted notes (BSG IBD 2019, Pimentel 2006 evolution, Sarna 2021 guide, LaPine 2021 cookbook)
- Extracted 144 individual recommendation claims from clinical guideline tables (ACG Crohn's, ACG UC, AGA UC, AGA Crohn's, ECCO UC)
- Fixed 28 thin-evidence claims (replaced "See source note." with extracted evidence)
- Added claims_status frontmatter to all 49 reading notes
- Quality review passed: all slugs unique, all wikilinks resolve, all confidence ratings valid, no placeholder leaks
- Tag enrichment: 60 sparse claims enriched with additional topic tags
- Total claims: 476 (target: 400-600 ✓)
- Scripts: extract_remaining.py, extract_recommendations.py, fix_thin_evidence.py, update_chapter_notes.py

### 2026-08-01 — Session 1 (Arron, run 21)
- Extracted 303 claims from 44 reading notes across 7 domains
- Extraction scripts: extract_batch1.py through extract_batch5.py, extract_implicit.py, extract_tier1.py
- 4 implicit-format notes remained unextracted; 28 thin-evidence claims identified
- Blocked for follow-up: quality review (t_36ae8419), chapter note updates (t_c6076bcd)
