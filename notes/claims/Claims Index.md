---
tags: [type/index, oskg-ibd, claims]
created: 2026-08-01
updated: 2026-08-01
related: ["[[../Notes Index]]", "[[claims-architecture]]", "[[claims-progress]]"]
---

# Claims Index

Extracted claim nodes from Phase 2. Each claim is a single verifiable assertion in its own markdown file with slug, source, confidence rating, and typed edges.

## Status

**Phase 2 extraction: IN PROGRESS.** 303 claims extracted from 44 reading notes across 7 domains.

### Claims by Domain

| Domain | Source Count | Claim Count |
|--------|-------------|-------------|
| Pathophysiology | 1 source | 10 claims |
| Diagnosis | 2 sources | 15 claims |
| Treatment | 5 sources | 34 claims |
| Clinical Guidelines | 10 sources | 129 claims |
| Microbiome & SIBO | 14 sources | 68 claims |
| Nutrition & Dietary | 11 sources | 54 claims |
| History & Context | 1 source | 1 claim |

### Claims by Source

| Source Slug | Claims |
|-------------|--------|
| `acg-cd2018` | 28 |
| `acg-uc2019` | 18 |
| `ecco-uc2022` | 14 |
| `ecco-diag2019` | 13 |
| `rome-sibo2017` | 13 |
| `steinhart-drug` | 10 |
| `aga-uc2020` | 11 |
| `ecco-cd2020` | 11 |
| `yamada-ibd62` | 10 |
| `acg-sibo2020` | 9 |
| `aga-cd2021` | 8 |
| `gottschall-ch35` | 8 |
| `yamada-cd64` | 8 |
| `yamada-ucdx63` | 8 |
| `pimentel-ch1` | 7 |
| `pimentel-ch6` | 7 |
| `steinhart-surg` | 7 |
| `thompson-een` | 7 |
| `yamada-cddx64` | 7 |
| `foote-cookbook` | 7 |
| `campbell-gaps` | 6 |
| `chutkan-dysbiosis` | 6 |
| `pimentel-ch2` | 6 |
| `pimentel-ch5` | 6 |
| `yamada-uc63` | 6 |
| `chutkan-rewild` | 5 |
| `gottschall-ch12` | 5 |
| `gottschall-ch910` | 5 |
| `pimentel-ch3` | 5 |
| `pimentel-ch4` | 5 |
| `pimentel-ch9` | 5 |
| `pimentel-lfe` | 5 |
| `sarna-sibo-diet` | 5 |
| `chutkan-found` | 4 |
| `aga-sibo2020` | 4 |
| `gottschall-fw` | 3 |
| `pimentel-ch10` | 3 |
| `yamada-surg65` | 3 |
| `ballantyne-paleo` | 1 |
| `marya-inflamed` | 1 |
| `myers-autoimmune` | 1 |
| `sonnenburg-gut` | 1 |
| `yamada-sibo58` | 1 |

### Pending

- **4 notes** with implicit claims not yet extracted (BSG IBD 2019, Pimentel 2006 evolution, Sarna 2021 guide, LaPine 2021 cookbook, context note)
- **Quality review** (verify all slugs unique, wikilinks resolve, `## Evidence` section present, confidence ratings appropriate)
- **Chapter note updates** (add `claims_status: extracted` frontmatter, compact claim summaries)
- **Intra-batch edges** (supports, contradicts, extends, depends_on)
- **Tag enrichment** (add 1-2 topic tags per claim using co-occurrence affinity)

## Conventions

See [[claims-architecture]] for the full design document. Key conventions:

- **Claim ID format:** `<source-slug>-<claim-num>` (e.g., `yamada-ibd62-1`)
- **File slug prefix:** `claim-` (e.g., `claim-ibd-loss-of-immune-tolerance.md`)
- **Confidence scale:** very-high, high, medium-high, medium, low-medium, low, debatable
- **Required tags:** type/claim, oskg-ibd, topic/*, evidence/*, scholar/*, source/*, domain/*
