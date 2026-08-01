---
tags: [type/synthesis, oskg-ibd, phase-4]
created: 2026-08-01
related: ["[[Synthesis Index]]", "[[../evidence-briefs/Evidence Briefs Index]]", "[[../questions/Questions Index]]"]
---

# Phase 4 Synthesis: Structural Analysis of the IBD Knowledge Graph

**Date:** 2026-08-01
**Graph size:** 476 claims, 174 typed edges, 267 connected claims, 209 orphans
**Components:** 307 (no giant component), 94 small isolated clusters

---

## 1. What the Graph Reveals

### The Treatment Guideline Spine

The graph coalesces around treatment guideline claims, which form the largest connected clusters. Three guideline claims emerge as the top structural hinges:

1. **5-ASA maintenance efficacy** (acg-uc2019-8): supported by 3 independent sources (ACG Crohn's, ECCO Crohn's, ECCO UC), the most converged-upon claim type. Represents the foundational pharmacotherapy consensus across guidelines.

2. **Corticosteroid induction vs. maintenance paradox** (aga-cd2021-7): the graph captures the tension in how guidelines handle steroids -- recommended for induction, strongly recommended against for maintenance. This dual role makes it a structural bridge between acute and chronic treatment recommendations.

3. **Oral 5-ASA with low-quality evidence** (ecco-uc2022-3): the strongest cascade tree (depth 3), connecting 5-ASA induction to Crohn's disease inefficacy to budesonide positioning. Illustrates how the graph encodes therapeutic reasoning chains.

### Deep Structural Fragmentation

**307 connected components with no giant component.** This is the defining structural characteristic of the graph. The 174 edges are insufficient to create a unified knowledge structure. Instead, the graph consists of:

- **94 small clusters** (2-5 claims each): typically a guideline recommendation pair (e.g., ACG UC recommendation + its ECCO equivalent) or a micro-theme (e.g., three claims about thiopurine induction across guidelines)
- **209 orphans**: claims with zero edges, including the entire nutritional/dietary corpus (SCD claims, most Pimentel and Gottschall claims) and the full ACG Crohn's guideline recommendation set

**Why this matters:** The graph is not wrong -- it is accurate at the level of what could be connected. But 174 edges across 476 claims is fundamentally too sparse. A clinically useful knowledge graph should connect pathophysiology to diagnosis to treatment within domains, and dietary interventions to mechanistic rationale across domains. This graph has abundant content but minimal structure.

### What Connected Well

The analysis identified **2 convergence points** (3+ independent sources supporting the same claim) and **94 guideline-guideline pair clusters.** The strongest pattern is *cross-guideline alignment*: when the same recommendation appears in ACG and ECCO, these claims were consistently connected via `supports` edges. This captured the real-world consensus across guideline bodies and is the graph's most structurally sound contribution.

**Example:** The thiopurine induction cluster (claims from ACG UC 2019, AGA UC 2020, and ECCO UC 2022 all converging on "against thiopurine monotherapy for induction") forms a 5-claim component. Similarly, the vedolizumab positioning cluster (5 claims, 4 sources) captures the guideline consensus on second-line biologic choice.

### What Remained Orphaned

**The entire dietary/nutritional domain** (77 claims) is almost entirely disconnected from the treatment guideline domain. There is no path in the graph from a Gottschall SCD claim to an ACG treatment recommendation. The dietary graph is a separate archipelago: diet-to-diet edges exist (SCD → elemental diet), but diet-to-guideline edges are absent.

**Topic sparsity analysis** confirms this: `topic/pathogenesis` (10 claims, avg 0.0 edges), `topic/fistula` (4 claims, avg 0.0 edges), `topic/genetics` (10 claims, avg 0.3 edges) are nearly invisible in the graph structure despite having substantial claim content. The graph connects what is easy to connect (guideline recommendations that map naturally onto each other) and leaves orphaned what is hard to connect (mechanistic claims, dietary interventions, epidemiological observations).

**The SIBO diagnostic debate** (ACG vs. AGA vs. Rome on breath test thresholds, herbal vs. antibiotic efficacy) -- flagged in the task as a target contradiction cluster -- is notably underconnected. The 1 contradiction edge found (BSG vs. ACG on mesalazine chemoprevention) is structurally isolated (zero camp members on either side). The SIBO debate exists as claims in the graph but does not exist as edges connecting the debate positions.

### Cascade Trees Are Shallow

The cascade trees (downstream dependency chains from top hinges) rarely exceed depth 1-2. The deepest chain (depth 3) traces: 5-ASA induction → Crohn's 5-ASA inefficacy → budesonide positioning. This is not a bug -- it reflects the actual structure of the graph, which has policy-guideline edges but few mechanistic-depth edges. To get cascade depth, the graph would need more `depends_on` edges connecting clinical recommendations to the epidemiological, pathophysiological, and mechanistic claims that justify them.

---

## 2. Domain-Specific Findings

### Evidence Briefs (Three Written)

Three evidence briefs were written in response to focused clinical questions:

1. **[EB-SIBO-IBD-Symptoms]:** **Low confidence** that SIBO directly contributes to IBD symptoms. The evidence is circumstantial (shared microbiota alterations, IBS-IBD symptom overlap) but the Keohane 2010 finding that IBS symptoms in IBD patients usually represent subclinical inflammation, not a separate SIBO process, is the most clinically significant data point.

2. **[EB-Diet-Comparison]:** **Low confidence** for differential efficacy. All three diets (SCD, low-FODMAP, LFE) likely work through the same mechanism (reducing fermentable substrate). Low-FODMAP has the best formal evidence (in IBS, not SIBO), SCD has the strongest mechanistic narrative, and LFE has the simplest implementation. No head-to-head trial exists. The SCD + low-FODMAP intersection may be the optimal starting point.

3. **[EB-Treat-to-Target]:** **Medium confidence** for the paradigm itself, **low confidence** for specific targets. The symptom-inflammation disconnect is settled science. IBD as a progressive disease provides biological urgency. But no RCT has compared treat-to-target against symptom-based management. The paradigm is consensus-driven rather than trial-proven -- a precautionary principle judgment.

### Open Questions (Three Documented)

Three research questions were formalized: [[SIBO-IBD-contribution]], [[SIBO-diet-comparison]], and [[treat-to-target-evidence]]. Each specifies what a definitive study would look like and why it matters clinically. These are genuine unknowns that the graph surfaces but cannot answer.

---

## 3. Structural Gaps: What Should Be in the Graph

### Missing Edge Types

The graph's edge construction focused on cross-guideline alignment (supports, extends). What is systematically missing:

- **Mechanism-to-treatment edges** (depends_on): no edges connect the SIBO pathophysiology claims (motility, MMC, bacterial overgrowth mechanisms) to treatment recommendations (rifaximin, prokinetics)
- **Epidemiology-to-recommendation edges**: SIBO prevalence data exists as claims but is not connected to clinical testing recommendations
- **Diet-to-disease edges**: the dietary domain is a separate archipelago. No edges connect SCD claims to IBD treatment outcomes
- **Contradiction edges**: only 1 found (vs. a target of several, including the SIBO diagnostic debate, herbal vs. antibiotic efficacy, and SIBO as cause vs. consequence of IBD)

### Missing Domain Connections

| Gap | Claims Present | Edges Absent |
|-----|---------------|--------------|
| SIBO → IBD symptom pathway | Both domains have substantial claims | Zero direct connection |
| Dietary therapy → guideline recommendation | SCD, low-FODMAP, LFE all claimed | Zero diet-to-guideline edges |
| Pathogenesis genetics → treatment targets | NOD2, ATG16L1, autophagy claims exist | Zero edges to biologic therapy positioning |
| Microbiome alterations → antibiotic therapy | 16S rRNA profiling claims exist | Thin (2 edges total) |
| Pediatric IBD | Not in the graph | — |

### Topic Sparsity

Fifteen topics have ≥3 claims with average under 2 edges per claim. The most severely under-connected topics (`topic/pathogenesis`: 10 claims, 0.0 avg edges; `topic/fistula`: 4 claims, 0.0 avg edges) represent clinical knowledge that exists in the graph as claims but is invisible to graph traversal because it was never connected during Phase 3.

---

## 4. Limitations of This Analysis

1. **174 edges is not a knowledge graph.** At this edge density (0.37 edges per claim), the analysis is a census of fragmentation rather than a structural analysis. Many of the standard metrics (betweenness centrality, articulation points, cascade depth) are meaningful in densely connected graphs but produce trivial results in a graph this sparse.

2. **Phase 3 methodology favored guideline-to-guideline edges.** The edge construction process naturally connected claims that map easily (same recommendation in different guidelines) and left orphaned claims that require cross-domain reasoning (dietary mechanism → clinical outcome, epidemiology → testing protocol). This is methodologically honest but produced a graph with systematic gaps.

3. **The "giant component" is a goal, not a finding.** The fact that no giant component formed means the graph cannot support the kinds of analyses (cross-domain hinge detection, long cascade tracing) that Phase 4 is designed to perform. Building the edges to create a giant component is the work of a future Phase 3 extension, not a Phase 4 interpretation.

4. **Evidence briefs synthesize from claims, not edges.** The three evidence briefs draw on the full claim corpus but do not rely heavily on edge structure (because the edges that would connect the briefs' subject matter are mostly absent). This limits how much the graph structure contributes to the synthesis.

---

## 5. Recommendations for Phase 5

1. **Focus the capstone on what the graph does well:** cross-guideline treatment consensus. The 94 guideline-pair clusters are real, verifiable, and clinically useful. A capstone that maps the consensus treatment algorithms across ACG, AGA, ECCO, and BSG for UC and CD induction/maintenance would be the graph's strongest contribution.

2. **Document the SIBO diagnostic debate narratively.** The contradiction edges are too sparse for camp analysis, but the individual claims on breath test validity (Rome 2017 vs. ACG 2020 vs. Pimentel 2022) form a coherent narrative that can be captured in a synthesis document even without dense graph edges.

3. **Flag the dietary domain for Phase 3 extension.** The diet-to-guideline gap is the largest structural hole in the graph. A targeted edge construction pass connecting SCD/low-FODMAP/LFE claims to the treatment guideline spine (via depends_on edges to mechanisms like "reduce fermentable substrate") would dramatically improve graph connectivity.

4. **Accept the current edge density as a Phase 3 output, not a Phase 4 problem.** Phase 3 produced 174 edges from 36 clusters. Adding edges to reach a useful structural density is a Phase 3 task, not a Phase 4 interpretation task. The Phase 4 analysis correctly identifies what the graph is: a collection of guideline-alignment clusters with substantial orphaned content.

---

## 6. Artifacts Produced

| Artifact | Path | Description |
|----------|------|-------------|
| Analysis script | `scripts/phase4_analysis.py` | Pure Python, re-runnable |
| JSON output | `scripts/phase4_analysis.json` | Full structured results |
| Text report | `scripts/phase4_analysis_output.txt` | Human-readable report |
| Evidence brief 1 | `notes/evidence-briefs/EB-SIBO-IBD-Symptoms.md` | SIBO-IBD symptom contribution |
| Evidence brief 2 | `notes/evidence-briefs/EB-Diet-Comparison.md` | SCD vs. low-FODMAP vs. LFE |
| Evidence brief 3 | `notes/evidence-briefs/EB-Treat-to-Target.md` | Treat-to-target justification |
| Question 1 | `notes/questions/SIBO-IBD-contribution.md` | SIBO in IBD research gap |
| Question 2 | `notes/questions/SIBO-diet-comparison.md` | Diet comparison research gap |
| Question 3 | `notes/questions/treat-to-target-evidence.md` | Treat-to-target evidence gap |
| This synthesis | `notes/synthesis/Phase-4-Synthesis.md` | Structural analysis report |
