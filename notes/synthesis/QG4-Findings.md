---
tags: [type/synthesis, oskg-ibd, quality-gate, phase-4]
created: 2026-08-01
related: ["[[Phase-4-Synthesis]]", "[[SIBO-Diagnostic-Debate]]", "[[../evidence-briefs/Evidence Briefs Index]]", "[[../questions/Questions Index]]"]
---

# Quality Gate 4: Phase 4 Synthesis Coherence

**Date:** 2026-08-01
**Status:** Complete with fixes. Four checks performed; two required substantive remediation; all gaps documented.

---

## QG4.1: Cascade Tree Completeness

**Check:** Verify every hinge claim appears in at least one cascade tree. Cascade trees should cover IBD diagnosis→treatment, SIBO diagnosis→treatment, and IBD+SIBO co-management.

**Finding: PASS (after remediation).** The original analysis capped cascade trees at top_n=6. Rerunning with top_n=15 produced cascade trees for all 15 hinges. However, the three target clinical pathways have uneven coverage:

| Clinical Pathway | Cascade Tree Coverage | Depth |
|-----------------|----------------------|-------|
| IBD diagnosis → treatment | Partially covered (5-ASA, corticosteroids, biologics, thiopurines) | 1-3 |
| SIBO diagnosis → treatment | **Not covered** -- no SIBO claims appear in the hinge inventory | N/A |
| IBD+SIBO co-management | **Not covered** -- zero edges connect the IBD and SIBO domains | N/A |

**Remediation:** Script fixed (`top_n=15`), JSON and text outputs regenerated.

**Root cause:** The graph's 174 edges are almost entirely guideline-to-guideline treatment edges (IBD domain). The SIBO domain has substantially fewer edges and the two domains have zero cross-domain edges. Cascade trees for SIBO pathways cannot be built from the current graph because the edges don't exist. This is a Phase 3 structural limitation, not a Phase 4 analysis omission.

**Cascade tree depth by hinge:**
- Depth 3: 1 hinge (ECCO 5-ASA induction → Crohn's inefficacy → budesonide)
- Depth 2: 3 hinges (thiopurine monotherapy, vedolizumab, AGA against 5-ASA)
- Depth 1: 4 hinges (Gottschall dietary mechanism, AGA biologic monotherapy, BSG ASUC rescue, Ballantyne paleo)
- Depth 0 (leaf): 7 hinges -- these have edges but zero downstream dependents

---

## QG4.2: Contradiction Clusters

**Check:** Verify the SIBO diagnostic debate is mapped (ACG vs AGA vs Rome on breath test thresholds, antibiotic vs herbal efficacy, SIBO as cause vs consequence of IBD). At minimum 3 major contradictions, each with 3+ claims per side.

**Finding: FAIL (remediated via narrative analysis).** The graph contains only 1 structural contradiction edge (BSG vs ACG on mesalazine chemoprevention) with zero camp members on either side. The three required contradiction clusters are entirely absent from the graph structure.

**Remediation:** Wrote [[SIBO-Diagnostic-Debate]], a narrative contradiction analysis mapping:
1. **Breath test validity:** ACG SIBO 2020 (pragmatic endorsement) vs AGA SIBO 2020 (diagnostic skepticism) vs Rome 2017 (methodological critique) vs Pimentel 2022 (clinical validation). 4 positions, 4+ claims per position.
2. **Antibiotic vs herbal efficacy:** ACG/Pimentel (antibiotic-first, rifaximin 61-78%) vs naturopathic/Sarna (herbal co-equality, ~50%) vs Rome (cautious, NNT=11). 3 positions, 3+ claims each.
3. **SIBO as cause vs consequence of IBD:** Pimentel (SIBO primary) vs ACG (SIBO is epiphenomenon) vs Rome bridging model (both directions possible). 3 positions, 3+ claims each.

**Structural note:** This narrative analysis documents the debate from the existing claims. The graph edges do not connect these positions. Building contradiction edges (Phase 3 extension) would make these debates structurally navigable. Priority edge pairs are identified in the analysis.

---

## QG4.3: Structural Gaps

**Check:** Cross-reference the gap analysis against questions/Questions Index.md. Verify every gap has a corresponding open question.

**Finding: PARTIAL PASS (remediated).** The original gap analysis identified 8+ structural gaps; only 3 had corresponding open questions.

**Remediation:** Added 3 new open questions:
- [[sibo-diagnostic-standard]] -- covering the SIBO diagnostic debate gap
- [[pathogenesis-treatment-gap]] -- covering the pathogenesis→treatment gap
- [[diet-guideline-gap]] -- covering the diet→guideline gap

Updated gap coverage map:

| Gap | Question | Status |
|-----|----------|--------|
| SIBO → IBD symptom pathway | SIBO-IBD-contribution | Covered |
| Dietary therapy → guidelines | diet-guideline-gap | Covered |
| Pathogenesis → treatment | pathogenesis-treatment-gap | Covered |
| SIBO diagnostic debate | sibo-diagnostic-standard | Covered |
| Diet comparison (head-to-head) | SIBO-diet-comparison | Covered |
| Treat-to-target evidence | treat-to-target-evidence | Covered |
| Microbiome → antibiotic therapy | Partially (sibo-diagnostic-standard) | Partial |
| Pediatric IBD | None | Uncovered |

The pediatric IBD gap is noted but not yet formalized as a question. The graph contains no pediatric-specific claims.

---

## QG4.4: Evidence Brief Completeness

**Check:** Verify the 3 planned evidence briefs exist and each cites at least 5 claims.

**Finding: PARTIAL PASS (remediated).** All 3 evidence briefs exist, but two were under the 5-claim threshold:

| Evidence Brief | Original Count | After Fix | Status |
|---------------|---------------|-----------|--------|
| EB-SIBO-IBD-Symptoms | 3 claims | 5 claims | PASS |
| EB-Diet-Comparison | 5 claims | 5 claims (unchanged) | PASS |
| EB-Treat-to-Target | 4 claims | 5 claims | PASS |

**Remediation:**
- EB-SIBO-IBD-Symptoms: Added [[claim-current-working-hypothesis-abnormal-microbiota-activate-mucosal|rome-sibo2017-7]] (host-microbial interactions) and [[claim-key-concept-most-common-symptom-sibo-bloating|acg-sibo2020-2]] (bloating as cardinal symptom)
- EB-Treat-to-Target: Added [[claim-disease-severity-must-incorporate-four-domains-patient-reported|acg-uc2019-2]] (four-domain severity model)

---

## Summary

| Check | Pre-Fix | Post-Fix | Root Cause |
|-------|---------|----------|------------|
| QG4.1 Cascade Trees | 6/15 hinges | 15/15 hinges, but SIBO pathways absent | Script cap; SIBO edges absent (Phase 3 gap) |
| QG4.2 Contradiction Clusters | 1 cluster | 3 clusters (narrative) | Phase 3 edge construction did not target contradictions |
| QG4.3 Structural Gaps | 3/8+ gaps covered | 6/8 gaps covered | Insufficient question formalization |
| QG4.4 Evidence Briefs | 2/3 under threshold | 3/3 passing | Initial drafting was claims-light |

**Residual issues requiring Phase 3 extension (not fixable in Phase 4 QG):**
1. Zero SIBO→IBD cross-domain edges (both cascade trees and contradictions require edges to be structurally navigable)
2. SIBO diagnostic debate edges (3 priority contradiction pairs identified in [[SIBO-Diagnostic-Debate]])
3. Diet→guideline edges (largest structural hole: 77 dietary claims disconnected from treatment spine)
4. Pathogenesis→treatment edges (10 mechanism claims with zero edges)
5. Pediatric IBD domain (no claims, no questions -- would require new source acquisition)

**Artifacts produced:**
- `scripts/phase4_analysis.py` -- updated (top_n=15)
- `scripts/phase4_analysis.json` -- regenerated
- `scripts/phase4_analysis_output.txt` -- regenerated
- `notes/synthesis/SIBO-Diagnostic-Debate.md` -- new narrative contradiction analysis
- `notes/questions/sibo-diagnostic-standard.md` -- new
- `notes/questions/pathogenesis-treatment-gap.md` -- new
- `notes/questions/diet-guideline-gap.md` -- new
- `notes/questions/Questions Index.md` -- updated (6 questions, gap coverage map)
- `notes/evidence-briefs/EB-SIBO-IBD-Symptoms.md` -- updated (5 claims)
- `notes/evidence-briefs/EB-Treat-to-Target.md` -- updated (5 claims)
