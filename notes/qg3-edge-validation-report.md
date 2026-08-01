# Quality Gate 3: Phase 3 Edge Validation Report

**Date:** 2026-08-01
**Validator:** Arron (head of research)
**Script:** `scripts/qg3_edge_validation.py`

## Summary

| Check | Result | Detail |
|-------|--------|--------|
| Edge Integrity | **PASS** | 0 broken wikilinks out of 193 edges |
| Edge Density | **FAIL** | 0.41 edges/claim, 311 orphans (65.3%) |
| Edge Type Distribution | **PASS** | All 6 edge types represented; contradicts sparse (2) |

## Check 1: Edge Integrity

Scanned all 476 claim files. Extracted 193 edges from the `## Edges` section across 165 connected claims. Every edge wikilink resolves to an existing claim file in `notes/claims/`. Zero broken links.

**Edge type distribution confirmed:**

| Edge Type | Count | % |
|-----------|-------|---|
| supports | 86 | 44.6% |
| extends | 46 | 23.8% |
| challenged_by | 36 | 18.7% |
| operationalizes | 18 | 9.3% |
| depends_on | 5 | 2.6% |
| contradicts | 2 | 1.0% |

Note: The parent task (t_ec87d503) reported 174 edges. The current count of 193 reflects 19 additional edges (18 challenged_by, 1 contradicts) likely added during QG2 tag enrichment or Phase 2c chapter note updates. All 193 edges verified as resolving correctly.

## Check 2: Edge Density

### Per-Domain Analysis

| Domain | Claims | Edges | Edges/Claim |
|--------|--------|-------|-------------|
| clinical-guidelines | 287 | 122 | 0.43 |
| microbiome | 73 | 26 | 0.36 |
| nutrition | 56 | 29 | 0.52 |
| treatment | 34 | 16 | 0.47 |
| diagnosis | 15 | 0 | 0.00 |
| pathophysiology | 10 | 0 | 0.00 |
| history | 1 | 0 | 0.00 |
| **OVERALL** | **476** | **193** | **0.41** |

**Every domain is under the 1.0 edges/claim threshold.** Three domains (diagnosis, pathophysiology, history) have zero edges at all.

### Orphan Analysis

311 of 476 claims have zero outgoing edges (65.3%). Of these, an estimated 209 are true orphans (no edges in either direction), while ~102 are edge targets that don't originate any edges.

The largest orphan clusters by topic tag co-occurrence:

| Topic Pair | Orphan Claims | Opportunity |
|------------|---------------|-------------|
| grade + treatment | 103 | Guideline recommendations not connected across sources |
| crohns-disease + treatment | 59 | CD treatment recommendations unlinked |
| crohns-disease + grade | 56 | CD GRADE assessments unlinked |
| grade + ulcerative-colitis | 51 | UC GRADE assessments unlinked |
| microbiome + sibo | 22 | Natural cross-domain bridge — SIBO claims not connected to microbiome ones |
| anti-tnf + biologics | 20 | Biologic class claims not connected |
| ibs + microbiome | 17 | IBS-microbiome intersection unexploited |

## Check 3: Edge Type Distribution

All six edge types are represented in the graph. However:

- **contradicts is sparse (2 edges):** Both edges are the same reciprocal pair — BSG Statement 126 (mesalazine CRC chemoprevention) vs ACG UC 2019 (no proven chemopreventive agent). This is a genuine guideline contradiction recorded in Phase 3. No other contradictions have been identified, which is surprising given the SIBO diagnostic debate (breath testing vs culture, antibiotic treatment vs prokinetic approach) and the multiple competing dietary frameworks (SCD vs low-FODMAP vs paleo vs elemental).

- **depends_on is thin (5 edges):** Only 5 explicit dependency relationships across 476 claims. Given that later guidelines build on earlier ones (ECCO UC 2022 extends ACG UC 2019, which builds on AGA UC 2020), there should be more.

- **challenged_by grew from 18 to 36:** The largest post-Phase-3 growth. These reflect scholarly disputes where one source challenges another's finding without outright contradiction.

## Discrepancy with Parent Task

The parent task (t_ec87d503) reported 174 edges. Current count is 193. The 19-edge difference is:

| Edge Type | Parent | Current | Delta |
|-----------|--------|---------|-------|
| challenged_by | 18 | 36 | +18 |
| contradicts | 1 | 2 | +1 |
| All others | 155 | 155 | 0 |

Edges were likely enriched during QG2 (tag enrichment) or Phase 2c (chapter note updates with claims_status). No broken links from these additions — integrity remains perfect.

## Recommendations

1. **No integrity fixes needed** — zero broken wikilinks.

2. **Edge density repair required** — 311 orphans is too many for a quality gate task. A dedicated Phase 3b edge repair task should:
   - Prioritize the `grade + treatment` cluster (103 orphan claims — guideline recommendations)
   - Connect SIBO claims to microbiome claims (22-claim topic cluster)
   - Add depends_on edges for guideline lineage (ECCO 2022 -> ACG 2019 -> AGA 2020)
   - Connect diagnosis-domain claims (15 orphans, currently 100% disconnected)

3. **Contradiction discovery needed** — The SIBO diagnostic debate (breath testing sensitivity/specificity controversy, antibiotic vs prokinetic treatment philosophy, the Rome Foundation vs Pimentel et al. diagnostic criteria debate) should yield multiple contradict edges. Current count of 2 suggests these conflicts exist in the claims but haven't been surfaced as typed edges.

4. **Consider edge direction completeness** — 102 claims are edge targets but not sources. For a well-formed knowledge graph, many of these should reciprocate (e.g., if A supports B, B might extend A).

## Artifacts

- Validation script: `scripts/qg3_edge_validation.py`
- This report: `notes/qg3-edge-validation-report.md`
