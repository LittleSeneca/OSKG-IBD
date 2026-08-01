# OSKG-IBD — Progress Tracker

## Phase 3b: Edge Density Repair

**Date:** 2026-08-01
**Operator:** Arron

### Starting State (from QG3, 2026-08-01)
- 476 claims, 193 edges
- 311 orphans (65.3%)
- Edge density: 0.41 edges/claim
- All domains under 1.0

### Completed Work

#### Batch 1: grade+treatment cluster
Generated 217 smart candidate pairs across 6 batches from 103 orphan claims tagged with both grade and treatment. Used drug-class-based candidate generation with clinical scenario matching (minimum score threshold of 6).

| Batch | Candidate Pairs | Edges Found | Edge Types |
|-------|----------------|-------------|------------|
| batch01 | 40 (scores 8-13) | 27 edges | 19 extends, 5 supports, 3 depends_on |
| batch02 | 40 (scores 6-7) | 19 edges | 11 extends, 4 supports, 4 challenged_by |
| batch03 | 40 (score 6) | 15 edges | extends, supports |
| batch04 | 40 (score 6) | 25 edges | 23 extends, 2 supports |
| batch05 | 40 (score 6) | 14 edges | extends, supports |
| batch06 | 17 (score 6) | 10 edges | extends, supports |
| **Total** | **217** | **110 edges** | |

#### Batch 2: cd-treatment + uc-grade clusters
- cd-treatment: 6 pairs, 3 edges
- uc-grade: 12 pairs, 10 edges
- Total: 13 edges

#### Batch 3: cross-domain (microbiome, nutrition, diagnosis, pathophysiology)
Generated smart pairs using subtopic matching across different source books (excluding same-book intra-source pairs).

| Batch | Candidate Pairs | Edges Found |
|-------|----------------|-------------|
| crossdomain-batch01 | 30 | 16 edges |
| crossdomain-batch02 | 30 | 13 edges |
| crossdomain-batch03 | 30 | 14 edges |
| crossdomain-batch04 | 30 | 15 edges |
| crossdomain-batch05 | 30 | 12 edges |
| **Total** | **150** | **70 edges** |

### Final State

- **412 edges** across 476 claims (+219 edges from Phase 3b)
- **246 orphans** (51.7%, down from 65.3%)
- **Edge density:** 0.87 edges/claim (up from 0.41)
- **Broken wikilinks:** 0
- **65 orphans connected** (target was 100+; actual reduction from 311 to 246)

### Edge Type Distribution (Final)

| Edge Type | Before | After | Delta |
|-----------|--------|-------|-------|
| extends | 46 | 189 | +143 |
| supports | 86 | 112 | +26 |
| challenged_by | 36 | 60 | +24 |
| operationalizes | 18 | 22 | +4 |
| depends_on | 5 | 19 | +14 |
| contradicts | 2 | 10 | +8 |

### Per-Domain Analysis (Final)

| Domain | Claims | Edges | Edges/Claim | Orphan % |
|--------|--------|-------|-------------|----------|
| clinical-guidelines | 287 | 247 | 0.86 | 48.1% |
| microbiome | 73 | 39 | 0.53 | 58.9% |
| nutrition | 56 | 39 | 0.70 | 55.4% |
| treatment | 34 | 19 | 0.56 | 55.9% |
| diagnosis | 15 | 1 | 0.07 | 93.3% |
| pathophysiology | 10 | 67 | 6.70 | 0.0% |
| history | 1 | 0 | 0.00 | 100.0% |

### Notable Achievements

1. **Pathophysiology fully connected** (was 0 edges, now 67 edges — 6.7 edges/claim). Cross-domain edges bridged pathophysiology claims to microbiome and nutrition claims.
2. **Contradicts edges grew 5x** (2 → 10), surfacing SIBO diagnostic debates and guideline conflicts.
3. **Depends_on edges grew ~4x** (5 → 19), documenting guideline lineage.
4. **Grade+treatment cluster substantially connected**: clinical-guidelines domain went from 160 orphans (55.7%) to 138 (48.1%).

### Remaining Work

246 orphans remain (51.7%). The remaining orphans are predominantly:
- ACG CD 2018 claims without cross-guideline counterparts (many are negative recommendations like "do NOT use X")
- Microbiome claims from single-source books (Pimentel, Chutkan, Sonnenburg) without clear cross-source relationships
- Nutrition claims about specific dietary protocols (SCD, low-FODMAP, paleo) that don't overlap cleanly
- Diagnosis domain (14/15 still orphaned) — needs dedicated cross-domain bridging effort

Recommendation for Phase 3c (if needed): focus on diagnosis domain and remaining clinical-guidelines claims using entity-level matching (specific drugs, procedures) rather than topic-tag co-occurrence.

### Scripts Created

- `scripts/phase3b_generate_candidates.py` — Smart candidate pair generator using drug class + clinical scenario matching
- `scripts/phase3b_apply_batch.py` — Edge batch applier (appends to existing edges)
- `scripts/phase3b_crossdomain.py` — Cross-domain candidate generator using subtopic matching
- `scripts/manifests/phase3b_candidates/` — Candidate and edge batch files
