---
tags: [type/index, oskg-ibd, claims]
created: 2026-08-01
updated: 2026-08-01
related: ["[[../Notes Index]]", "[[claims-architecture]]", "[[claims-progress]]"]
---

# Claims Index

Extracted claim nodes from Phase 2. Each claim is a single verifiable assertion in its own markdown file with slug, source, confidence rating, and typed edges.

## Status

**Phase 2 extraction: COMPLETE (target met).** 476 claims extracted from 47 reading notes across 7 domains (target: 400-600).

### Claims by Domain

| Domain | Source Count | Claim Count |
|--------|-------------|-------------|
| Pathophysiology | 1 source | 10 claims |
| Diagnosis | 2 sources | 15 claims |
| Treatment | 5 sources | 34 claims |
| Clinical Guidelines | 11 sources | ~270 claims |
| Microbiome & SIBO | 17 sources | 68 claims |
| Nutrition & Dietary | 11 sources | 77 claims |
| History & Context | 1 source | 1 claim |

### Claims by Source

See [[claims-progress]] for the full per-note extraction checklist.

### Quality Review Status

- [x] All 476 claim slugs unique
- [x] All source_note wikilinks resolve to real files
- [x] All confidence ratings use valid scale (very-high through debatable)
- [x] No template placeholder leaks
- [x] All claim files have ## Evidence section
- [x] 28 thin-evidence claims fixed (evidence text extracted from source notes)
- [x] claims_status frontmatter added to all 49 reading notes
- [ ] ### Claim N: block replacement in chapter notes (deferred to t_c6076bcd)
- [ ] Intra-batch edge construction (pending)
- [ ] Full tag enrichment pass (partial: 60 claims enriched)

### Pending

- **2 notes** with no claims (Microbiome Science Context, Sleisenger/Yamada Assessment — infrastructure notes)
- **Intra-batch edges** (supports, contradicts, extends, depends_on) — Phase 2b
- **Tag enrichment** — full pass to bring all claims to 3+ topic tags
- **Chapter note claim block replacement** — replace ### Claim N: blocks with compact wikilink summaries

## Conventions

See [[claims-architecture]] for the full design document. Key conventions:

- **Claim ID format:** `<source-slug>-<claim-num>` (e.g., `yamada-ibd62-1`) or `<source-slug>-rec<N>` (individual recommendation claims)
- **File slug prefix:** `claim-` (e.g., `claim-ibd-loss-of-immune-tolerance.md`)
- **Confidence scale:** very-high, high, medium-high, medium, low-medium, low, debatable
- **Required tags:** type/claim, oskg-ibd, topic/*, evidence/*, scholar/*, source/*, domain/*
- **Recommendation claims:** extracted from GRADE recommendation tables in clinical guidelines; use `-rec<N>` claim IDs
