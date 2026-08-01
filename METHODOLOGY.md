---
tags:
  - type/meta
  - methodology
  - oskg-ibd
created: 2026-08-01
updated: 2026-08-01
related:
  - "[[Home]]"
  - "[[Book Guide]]"
  - "[[Paper Guide]]"
---

# METHODOLOGY — OSKG-IBD

How the IBD/SIBO knowledge graph is built. Pipeline, claim format, edge types, domain-specific challenges, and the legal basis for the extraction pipeline.

---

## 1. Project Identity

**OSKG-IBD** is an open-source knowledge graph connecting Inflammatory Bowel Disease (Crohn's disease and ulcerative colitis) with Small Intestinal Bacterial Overgrowth (SIBO/IMO). It decomposes textbooks, clinical practice guidelines, microbiome science, and landmark clinical trials into discrete, verifiable claims with typed edges.

**Why IBD and SIBO together?** IBD patients with persistent symptoms despite endoscopic remission are increasingly found to have concurrent SIBO. The microbiome is the bridge between the two conditions. Yet the clinical literature treats them as separate specialties (gastroenterology vs motility/functional GI). This graph makes the connections explicit.

**A note on controversy:** SIBO sits at the intersection of established gastroenterology and functional medicine. Its definition is contested, its diagnostic methods are debated, and treatment approaches range from FDA-approved antibiotics to herbal protocols studied in small trials. This graph captures that tension — contradictory edges are a feature, not a bug. Confidence ratings are especially important here.

---

## 2. OSKG Principles

1. **Every claim is traceable to a source.** No claim exists without a `source_note` field pointing to the reading note from which it was extracted.
2. **The graph decomposes, not summarizes.** Claims are the smallest verifiable unit — a single assertion with a confidence rating.
3. **Edges carry semantics.** `supports`, `contradicts`, `extends`, `depends_on` — each relationship type has specific meaning.
4. **Confidence is explicit.** Every claim has a `confidence` field (high/medium/low) grounded in the evidence type.
5. **The pipeline is sequential.** Phase N+1 depends on the completeness of Phase N.

---

## 3. Pipeline

| Phase | Artifact | Description |
|-------|----------|-------------|
| 0 | Acquisition | Sources identified, acquired, extracted to plain text. Books via libgen; guidelines via direct download; papers via open access or institutional access. |
| 1 | Reading Notes | Chapter-by-chapter / section-by-section analysis of every Tier 1-3 source. Cross-referenced against other sources. Claims identified inline with `### Claim N:` headings. |
| 2 | Claims Extraction | Discrete claim nodes extracted into individual files under `notes/claims/`. Each claim has slug, source, confidence, typed edges. Intra-batch edges added. Chapter notes updated with `claims_status: extracted` frontmatter and compact claim summaries. Tag enrichment applied (1-2 topic tags per claim). |
| 3 | Cross-Source Edges | Claims connected across sources via typed edges. Three-pass strategy: topic-tag clustering → LLM batch edge detection → apply-and-verify. |
| 4 | Synthesis | Hinge inventory, cascade trees, convergence points, contradiction clusters, structural gaps. Evidence briefs on focused questions. |
| 5 | Capstone | Culminating synthesis: what does the evidence show about the IBD-SIBO connection? What does it not show? |

### Quality Gates

Every phase has a quality gate at its completion. If the gate finds failures, a cleanup task is spawned to fix them before the next phase can begin.

| Gate | Phase | What It Checks | Cleanup Trigger |
|------|-------|---------------|-----------------|
| QG0 | Phase 0 | All sources acquired, extracted, correctly filed. No missing or corrupt files. | Reacquire failed sources. Fix extraction issues. |
| QG1 | Phase 1 | Tag audit (project, classification, source-key, tier tags on every note). Index updates. Source progress tables. | Fix missing/wrong tags. Update stale indexes. |
| QG2 | Phase 2 | Claim frontmatter audit (slug, source, tags, confidence, source_note). Wikilink verification (edge links and source_note links resolve). Tag enrichment. | Repair YAML parse errors. Fix broken wikilinks. Add missing tags. |
| QG3 | Phase 3 | All edge wikilinks resolve. Edge type distribution. Edge density across domains. | Repair broken edges. Add missing cross-domain edges. |
| QG4 | Phase 4 | Cascade tree completeness. Structural gap coverage. All hinges link to claims. | Fill gaps. Add missing hinges. |
| QG5 | Phase 5 | Every capstone claim traces to a claim node or primary source. No orphan assertions. | Trace and link unlinked claims. |

---

## 4. Claim Format

Each claim is a self-contained markdown file under `notes/claims/`:

```yaml
---
slug: claim-ibd-001
source: "[[../microbiome/Pimentel - Ch 1 The SIBO Hypothesis]]"
tags: [oskg-ibd, type/claim, source/pimentel-microbiome-connection, topic/sibo-definition, topic/ibs, evidence/clinical-research, tier-1]
confidence: high
source_note: "[[../microbiome/Pimentel - Ch 1 The SIBO Hypothesis]]"
claims_status: extracted
---

# claim-ibd-001

**Statement:** SIBO is defined as the presence of ≥10³ colony-forming units per mL of jejunal aspirate, which represents the overgrowth of colonic-type bacteria in the small intestine.

**Confidence:** High — established by peer-reviewed literature and adopted by ACG and AGA clinical guidelines, though the threshold is debated (some use ≥10⁵ CFU/mL).

**Supports:** [[claim-ibd-010]] (breath testing as surrogate for aspirate culture)

**Contradicts:** [[claim-ibd-007]] (threshold debate: some argue ≥10⁵ is the correct cutoff)

**Related Questions:** [[SIBO diagnostic criteria]]
```

### Edge Types

| Type | Semantics | Example |
|------|-----------|---------|
| `supports` | Claim A provides evidence for Claim B | Rifaximin trial supports antibiotic efficacy claim |
| `contradicts` | Claim A is in tension with Claim B | Herbal therapy study contradicts antibiotic-only treatment claim |
| `extends` | Claim A adds specificity to Claim B | IMO subtype extends SIBO classification |
| `depends_on` | Claim A assumes Claim B is true | Breath test interpretation depends_on aspirate culture being the gold standard |
| `operationalizes` | Claim A provides a method for measuring/testing Claim B | Lactulose breath test operationalizes SIBO diagnosis |

### Confidence Ratings

| Rating | Criteria |
|--------|----------|
| **High** | Multiple RCTs or meta-analyses; clinical guideline consensus; textbook-level established fact |
| **Medium** | Single RCT or observational studies; guideline recommendation with moderate evidence grade; mechanistic plausibility without direct confirmation |
| **Low** | Expert opinion; case series; patient-reported outcomes; mechanistic speculation; ongoing debate |

Medical domains benefit from explicit confidence ratings more than professional/operational domains (like vCISO) because the evidence hierarchy (RCT > cohort > case-control > case series > expert opinion) is well-established and directly applicable.

---

## 5. Domain Adaptation

### Source Types

| Dimension | OSKG-vCISO (Template) | OSKG-IBD (This Project) |
|-----------|----------------------|------------------------|
| Source type | Technical books, standards, whitepapers | Clinical textbooks, patient guides, clinical practice guidelines, RCTs |
| Evidence type | Architectural/prescriptive | Empirical — RCTs, meta-analyses, observational studies, mechanistic research |
| Consensus maturity | Mature (established frameworks) | Mixed — IBD treatment is mature; SIBO diagnosis is actively debated |
| Temporality | Evolving (cloud, DevOps) | Rapidly evolving (microbiome science, biologics) |
| Primary sources | NIST, CIS, ISO | ACG/AGA/ECCO clinical practice guidelines |
| Claims nature | Prescriptive (how to do security) | Mixed — descriptive (pathophysiology) and prescriptive (treatment guidelines) |

### Knowledge Categories

The `notes/` subdirectories reflect the domain's knowledge categories:

| OSKG-vCISO | OSKG-IBD | Rationale |
|-----------|----------|-----------|
| `notes/grc/` | `notes/pathophysiology/` | Core mechanisms — the "why" of the disease |
| `notes/architecture/` | `notes/diagnosis/` | How we know what's wrong — structural assessment |
| `notes/secops/` | `notes/treatment/` | What we do about it — active intervention |
| — | `notes/microbiome/` | The bridge between IBD and SIBO — unique to this domain |
| — | `notes/nutrition/` | Diet as intervention — a major domain in IBD/SIBO not present in vCISO |
| `notes/leadership/` | `notes/clinical-guidelines/` | Authoritative frameworks that define standard of care |
| `notes/history/` | `notes/history/` | Evolution of understanding (same concept, different content) |

### Evidence Hierarchy

This domain introduces an explicit evidence hierarchy not present in prior OSKGs:

| Level | Evidence Type | Confidence |
|-------|--------------|------------|
| I | Meta-analysis of multiple RCTs | High |
| II | Single well-designed RCT | High-Medium |
| III | Well-designed cohort or case-control | Medium |
| IV | Case series, case reports | Low-Medium |
| V | Expert opinion, mechanistic reasoning | Low |

Clinical practice guidelines use this hierarchy (via GRADE or similar) to grade their recommendations. The graph inherits these grades where available.

---

## 6. Domain-Specific Challenges

### SIBO: Contested Definition

The Rome Foundation, ACG, and AGA disagree on SIBO diagnostic criteria. The Rome Foundation emphasizes jejunal aspirate (≥10³ CFU/mL) as the gold standard but notes it's rarely used clinically. The ACG guideline acknowledges breath testing as practical but specifies it has ~60-70% sensitivity. AGA is more cautious, noting "the definition remains controversial and true prevalence unknown."

**Graph strategy:** Extract all three positions as claims with `contradicts` edges. Do not resolve the controversy — map it. The graph's value is in documenting where authorities diverge.

### IBD-SIBO Overlap

IBD patients can have SIBO-like symptoms from strictures, fistulae, or altered motility (all IBD complications) — not necessarily from bacterial overgrowth. Distinguishing true SIBO from IBD-mimics is clinically difficult.

**Graph strategy:** Tag claims about SIBO-in-IBD separately (`topic/sibo-in-ibd`). Cross-reference breath test result claims with stricture/fistula claims to surface the diagnostic ambiguity.

### Evolving Terminology

In 2020, the ACG guideline introduced "Intestinal Methanogen Overgrowth (IMO)" to replace "methane-dominant SIBO" because methanogens (Methanobrevibacter smithii) are archaea, not bacteria. Not all sources use the new terminology.

**Graph strategy:** Tag some claims with both `topic/sibo-methane` and `topic/imo` where the clinical concept is the same but the terminology differs. Add `extends` edges from IMO claims to earlier methane-SIBO claims.

### Patient-Guide vs Clinical Textbook

Books like Steinhart (patient-facing) and Sarna/LaPine (patient cookbooks) make different claims than Sleisenger (clinical reference). Patient guides are more likely to recommend dietary interventions; clinical texts emphasize pharmacological evidence.

**Graph strategy:** Source-tier tagging (`tier-1` for textbooks, `tier-2` for patient guides). Cross-reference patient-guide claims against clinical guideline claims to surface evidence gaps in patient recommendations.

---

## 7. Fair Use and Copyright

This project is a research and educational tool. The pipeline extracts and transforms copyrighted works: clinical textbooks, patient guides, and research papers.

**Four-factor fair use analysis:**

1. **Purpose and character:** Transformative. The knowledge graph decomposes full texts into discrete, tagged, edge-linked claim nodes. It does not reproduce the original works in readable form.
2. **Nature of the work:** Primarily factual and scientific. Clinical textbooks and guidelines have thinner copyright protection than creative works. Patient guides blend factual medical information with protected expression — extraction targets the former.
3. **Amount used:** Minimal per claim. Each claim is a single assertion, typically 1-3 sentences. The graph as a whole covers the corpus but no individual claim reproduces more than a fragment.
4. **Market effect:** Negligible. The graph is not a substitute for the original works (it cannot be read as a book). It serves a different purpose — evidence synthesis across sources.

**Practices:**
- Source PDFs and full-text files (`sources/books/_fulltext/`, `sources/papers/_pdfs/`, `sources/guidelines/_pdfs/`) are gitignored and never committed.
- Every claim links to its source chapter via wikilink.
- The graph does not claim to replace the original works. It is a research tool built on them.

---

## 8. ORKG Alignment

This project draws from the Open Research Knowledge Graph (ORKG) methodology. Key alignments:

| OSKG-IBD Concept | ORKG Equivalent |
|-----------------|-----------------|
| Claim | Contribution |
| Edge type (`supports`, `contradicts`) | Property |
| Confidence rating | Confidence score |
| Tag system | Research field / predicate |
| Evidence brief | Comparison |

---

## 9. Convergence Argument

The knowledge graph's value is in the convergence points it surfaces — places where multiple independent sources arrive at the same conclusion, and places where they don't.

**Expected convergence:** Biologics are superior to 5-ASA for moderate-to-severe IBD; rifaximin is effective for SIBO; diet impacts symptoms but not mucosal healing.

**Expected divergence:** SIBO diagnostic criteria; breath test vs aspirate; herbal vs antibiotic efficacy; role of probiotics in SIBO; whether SIBO is a cause or consequence of IBD.

---

## 10. Why This Matters

IBD is a chronic, incurable condition affecting millions. SIBO is underdiagnosed and increasingly recognized as a contributor to persistent GI symptoms. The clinical literature on each is vast but siloed. A knowledge graph that connects the two — that maps where the evidence converges and where it diverges — is a tool for both patients and clinicians navigating a complex, evolving evidence landscape.

---

## 11. Related Documents

- [[Book Guide]] — Source corpus and acquisition plan
- [[Paper Guide]] — Research papers and landmark trials
- `sources/guidelines/Guidelines Index.md` — Clinical practice guidelines
- `notes/Notes Index` — Entry point for all knowledge domains
- `notes/claims/Claims Index` — Extracted claim nodes (Phase 2+)
