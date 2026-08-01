---
tags: [type/synthesis, oskg-ibd, phase-5, capstone]
created: 2026-08-01
related: ["[[Synthesis Index]]", "[[Phase-4-Synthesis]]", "[[../evidence-briefs/Evidence Briefs Index]]", "[[../questions/Questions Index]]"]
---

# Phase 5 Capstone: What the IBD-SIBO Knowledge Graph Shows

**Date:** 2026-08-01
**Graph state:** 476 claims, 174 typed edges, 267 connected claims, 209 orphans
**Sources:** 20+ books and clinical guidelines, spanning Gottschall (1994) to Pimentel (2022)

---

## 1. Introduction: What the Graph Is and Is Not

This knowledge graph integrates two literatures that rarely speak to each other: the clinical guideline corpus governing inflammatory bowel disease treatment (ACG, AGA, ECCO, BSG) and the SIBO/dietary/microbiome corpus spanning patient guides, popular science, and specialist monographs. The question driving the graph is whether these literatures, when read together, reveal clinically actionable patterns that neither reveals alone.

**What the graph does well:** It captures cross-guideline treatment consensus. The 94 guideline-guideline pair clusters are real, verifiable, and consistent with clinical practice. When ACG, AGA, and ECCO agree on a treatment recommendation, the graph reflects that consensus through `supports` and `extends` edges. The treatment algorithm for UC -- rectal 5-ASA for proctitis, combined oral+rectal 5-ASA for left-sided disease, corticosteroids for refractory cases, anti-TNF biologics for moderate-severe, vedolizumab or tofacitinib after anti-TNF failure -- emerges clearly from the connected claims.

**What the graph does not do:** It does not connect pathophysiology to treatment. The 209 orphan claims include almost the entire dietary corpus and the mechanistic SIBO literature. There is no edge path from a Gottschall carbohydrate-malabsorption claim to an ACG treatment recommendation. The SIBO diagnostic debate exists as claims but not as connected edges. The graph is a collection of well-connected guideline clusters surrounded by a vast archipelago of isolated claims -- accurate at the level of what was connected, incomplete at the level of what the source material contains.

**The capstone's method:** Every assertion below traces to a claim node. Evidence strength is qualified at three levels: *established* (multiple independent sources converge), *probable* (good evidence but reasonable alternatives exist), and *speculative* (one scholar's argument, not yet corroborated). Where the graph is silent, this capstone says so directly.

---

## 2. The Treatment Guideline Spine: Where the Evidence Converges

The treatment of inflammatory bowel disease is the best-connected domain in the graph. The four major guideline bodies -- ACG, AGA, ECCO, and BSG -- produce recommendations that cluster naturally into treatment algorithms. The graph's `supports` edges capture cross-guideline alignment at the recommendation level.

### 2.1 5-ASA: The Cornerstone of UC Treatment

The convergence on 5-aminosalicylates for ulcerative colitis is the strongest consensus signal in the graph.

**Rectal 5-ASA for proctitis.** [[acg-uc2019-5]] establishes rectal 5-ASA (1 g/d) as first-line therapy for proctitis, with combined oral + rectal 5-ASA superior to oral alone. The evidence grade is high (meta-analyses of multiple RCTs). [[ecco-uc2022-3]] makes the same recommendation, with the notable transparency that the strong recommendation rests on low-quality evidence -- a pattern seen throughout the UC guideline literature. The Yamada textbook network meta-analysis of 48 trials (8,020 patients) provides the largest data synthesis, confirming combined oral+rectal 5-ASA as the most effective induction strategy for mild-moderate UC [[yamada-uc63-1]].

**Evidence quality:** Established. Multiple independent meta-analyses, large network meta-analysis, strong recommendations across three guideline bodies.

**Maintenance.** [[ecco-uc2022-7]] strongly recommends oral 5-ASA ≥2 g/d and topical 5-ASA for distal disease as maintenance therapy. [[acg-uc2019-6]] adds that once-daily dosing is as effective as split dosing, improving adherence without sacrificing efficacy.

### 2.2 Corticosteroids: The Induction-Maintenance Paradox

The graph captures a structural tension in corticosteroid positioning that has clinical consequences.

**For induction: effective.** [[acg-cd2018-12]] states oral corticosteroids are effective for short-term symptom relief in moderate-severe Crohn's disease, but do not consistently achieve mucosal healing. [[ecco-cd2020-3]] confirms systemic corticosteroid efficacy for moderate-severe CD but emphasizes substantial toxicity. [[ecco-uc2022-11]] recommends oral prednisolone for moderate-severe UC induction. [[acg-uc2019-7]] positions budesonide MMX (a gut-targeted corticosteroid with lower systemic exposure) as preferred over prednisolone for 5-ASA-refractory mild-moderate UC.

**For maintenance: contraindicated.** [[acg-cd2018-47]] states corticosteroids should NOT be used for maintenance -- a strong recommendation across all guidelines. This is the structural paradox: corticosteroids work for induction but are harmful when continued.

**Evidence quality:** Established for induction efficacy and maintenance contraindication. The budesonide MMX positioning (preferred for mild-moderate, insufficient for severe) is probable, supported by one guideline body (ACG) but not universally adopted.

### 2.3 Biologics: Superiority for Moderate-Severe Disease

The biologic era has transformed IBD management, and the graph reflects a consistent hierarchy across guidelines.

**Anti-TNF as first biologic.** [[acg-uc2019-9]] recommends anti-TNF therapy (infliximab, adalimumab, golimumab) with high-quality evidence for UC induction. Combination infliximab + thiopurine is superior to either monotherapy. [[ecco-uc2022-9]] makes the same recommendation with strong endorsement, supported by network meta-analysis.

**Early biologic over step-up.** [[aga-cd2021-7]] recommends early biologic ± immunomodulator over step-up therapy for moderate-severe CD -- representing the paradigm shift away from the historical "5-ASA → corticosteroids → immunomodulators → biologics" ladder toward early effective therapy to prevent progressive bowel damage. This is particularly critical in CD, where [[ecco-cd2020-1]] frames the disease as progressive, requiring early intensive monitoring and individualized risk-stratified treatment.

**Second-line biologics.** [[acg-uc2019-25]] recommends vedolizumab for induction; [[acg-uc2019-35]] recommends continuing vedolizumab for maintenance. The graph captures vedolizumab's established position as second-line biologic after anti-TNF failure, with the gut-selective mechanism (gut-homing α4β7 integrin blockade) offering a safety advantage. [[vedolizumab-tofacitinib-effective-induction-including-anti-tnf-exposed-pat]] confirms efficacy in anti-TNF-exposed patients.

**Evidence quality:** Established for anti-TNF superiority over placebo (multiple RCTs). Probable for early biologic over step-up (observational data, biological rationale, guideline consensus, but no RCT randomizing early biologic against step-up). Probable for vedolizumab as preferred second-line (consistent guideline recommendations, limited head-to-head data).

### 2.4 Treat-to-Target: Consensus Paradigm, Low-Quality Targets

This is the graph's most philosophically interesting convergence. All major guidelines endorse treating to objective targets (endoscopic, imaging, or biomarker) rather than symptoms alone. The evidence is detailed in [[../evidence-briefs/EB-Treat-to-Target]].

**The symptom-inflammation disconnect.** [[acg-cd2018-2]] states the foundational premise: symptoms of Crohn's disease do not correlate well with active mucosal inflammation. This claim is a convergence point in the graph (3+ independent sources converge) and is the settled-science basis for the entire treat-to-target paradigm.

**The progressive disease model.** [[ecco-cd2020-1]] frames CD as a progressive disease where untreated inflammation causes cumulative bowel damage (strictures, fistulas, surgical resection) even when the patient feels well. The model provides biological urgency for preemptive, objective-monitoring-driven therapy.

**Specific targets: low-quality evidence.** [[acg-uc2019-3]] establishes mucosal healing (Mayo endoscopic subscore 0-1) as the treatment target, but the confidence rating is only medium and the evidence grade is low. [[bsg-ibd2019-2]] makes mucosal healing the target with weak recommendation and very low-quality evidence. [[ecco-diag2019-6]] documents the emerging endpoint of transmural healing (MRE/IUS), relevant for CD where mucosal-only assessment may miss deep disease.

**The paradox:** No guideline claims that treat-to-target is supported by high-quality evidence from randomized trials comparing treat-to-target against symptom-based care. The paradigm is consensus-driven -- a precautionary principle judgment that the observational data and biological rationale outweigh the absence of definitive trials. The graph captures this honestly: the paradigm is settled at the level of clinical reasoning but tentative at the level of specific targets.

**Evidence quality:** Established for the symptom-inflammation disconnect. Probable for the progressive disease model. Speculative for specific targets (Mayo 0 vs 1, endoscopic vs histologic, mucosal vs transmural).

---

## 3. The SIBO Diagnostic Controversy

SIBO diagnosis is the most contested area in the graph. Three major positions exist, each held by a different institutional actor, and the contradiction edges connecting these positions are sparse (only 1 contradiction edge exists in the graph, and it concerns mesalazine chemoprevention -- not SIBO diagnosis). The debate can only be reconstructed narratively from the individual claims.

### 3.1 Position A: Breath Testing Is Clinically Valid (ACG SIBO 2020)

[[acg-sibo2020-3]] (Pimentel et al.) recommends glucose or lactulose hydrogen breath testing for SIBO diagnosis in IBS, suspected motility disorders, and post-surgical patients. [[acg-sibo2020-5]] refines the framework: methane-positive breath testing (≥10 ppm) indicates intestinal methanogen overgrowth (IMO), not bacterial SIBO, requiring different treatment. [[acg-sibo2020-1]] provides the operational definition: "the presence of excessive numbers of bacteria in the small bowel causing gastrointestinal symptoms."

**The clinical basis:** Pimentel's 16-year dataset (2006-2022) shows that breath test results correlate with treatment response [[pimentel-evol-6]]. The MMC housekeeper wave, food poisoning etiology, elemental diet efficacy (>80%), and the H. pylori/peptic ulcer analogy have remained stable across two decades of research. The framework is internally consistent and clinically predictive.

**The weakness:** The evidence is primarily from a single research group. Independent validation of lactulose breath test sensitivity/specificity is limited. [[acg-sibo2020-4]] acknowledges (but does not formally grade) that jejunal aspirate culture -- the putative gold standard -- has significant limitations: the >10^5 CFU/mL cutoff was established from post-surgical diversion samples, not healthy controls.

### 3.2 Position B: The Evidence Base Is Fundamentally Weak (Rome 2017)

[[rome-sibo2017-4]] states the problem directly: "The role of SIBO in the pathogenesis of IBS is very controversial because the breath tests employed to establish this role have not been validated. Even the validity of the 'gold standard', jejunal cultures >10^5 cfu/ml with colonic-type bacteria, has been challenged."

The Rome report catalogs the empirical difficulties:

- **Posserud et al. (2007):** 162 IBS vs 42 controls, jejunal aspirate -- 4% of IBS >10^5 CFU/mL (same as controls). But at >5×10^3: 43% IBS vs 12% controls. The cutoff changes everything.
- **Pyleris et al. (2012):** 85 IBS, 150 non-IBS -- 37% IBS >10^3 CFU/mL vs 15.11% non-IBS.
- **Choung et al. (2011):** 148 IBS, duodenal aspirate -- 2% IBS >10^5 CFU/mL vs 10% in patients with other indications.

The core problem: **there is no accepted definition of what constitutes a normal small intestinal microbiota** [[rome-sibo2017-3]]. Without knowing what "normal" looks like at each segment of the small intestine, "overgrowth" cannot be objectively defined. Breath tests are proxies for a condition whose reference standard is itself contested.

### 3.3 Position C: The Definition Lacks Precision (AGA 2020)

[[aga-sibo2020-implicit-1]] (Quigley et al.) opens with: "The definition of SIBO lacks precision and consistency." [[aga-sibo2020-implicit-3]] elaborates: "A major impediment to our ability to accurately define SIBO is our limited understanding of normal small intestinal microbial populations."

The AGA Best Practice Advice occupies a middle position: SIBO is clinically real, breath testing has clinical utility, but the evidence base is insufficient for formal guideline recommendations. The AGA's implicit framing -- all statements are Best Practice Advice, not graded recommendations -- is itself a signal of the evidence quality.

### 3.4 Synthesis: What the Graph Shows About SIBO Diagnosis

The three positions are not contradictory at the level of individual facts. ACG, Rome, and AGA all agree that:

1. Jejunal aspirate culture is the historical gold standard but is impractical and has definitional problems [[acg-sibo2020-4]], [[rome-sibo2017-4]]
2. Breath testing is the clinically pragmatic alternative [[acg-sibo2020-3]], [[aga-sibo2020-implicit-3]]
3. The normal small intestinal microbiome is poorly characterized [[rome-sibo2017-3]], [[aga-sibo2020-implicit-3]]

The disagreement is about **threshold for clinical action.** ACG says breath testing is adequate for clinical decision-making (treat empirically based on breath test results). Rome says breath testing has not been validated against an accepted gold standard (treat based on clinical judgment, not breath test alone). AGA says the definitional problems are fundamental (more research needed before formal recommendations).

The graph does not resolve this disagreement. It documents it. The resolution would require independent, multi-center validation of breath testing against clinical outcomes -- a study design that the Rome report outlines but that no claim in the graph reports as having been conducted.

**Evidence quality:** The individual facts (breath test limitations, culture cutoff controversy, limited microbiome characterization) are established. The resolution of the clinical action threshold is unresolved.

---

## 4. Dietary Interventions: Evidence Hierarchy

The dietary domain is the most orphaned in the graph (77 claims, almost entirely disconnected from the treatment guideline spine). Yet it is also the domain where the graph's source material is richest, spanning practitioner guides, patient cookbooks, and mechanistic monographs.

### 4.1 Exclusive Enteral Nutrition (EEN): The Evidence Standard

EEN is the most rigorously evidenced dietary therapy in IBD, and the only dietary intervention recommended by formal clinical guidelines.

**Pediatric Crohn's: established efficacy.** [[thompson-een-1]] establishes elemental diet therapy as equivalent to corticosteroids for inducing remission in pediatric Crohn's, with superior mucosal healing. [[bsg-ibd2019-9]] confirms: "EEN is as effective as corticosteroids in paediatric CD (73% remission on intention-to-treat basis)." The evidence is meta-analysis-grade.

**Adult Crohn's: efficacy likely, compliance weak.** [[bsg-ibd2019-9]] gives EEN in adults a weak recommendation with low-quality evidence. The adult evidence is weaker due to lower adherence (taste fatigue, social restrictions) rather than lower biological efficacy. Polymeric feeds are as effective as elemental feeds, undermining the "elemental" rationale and suggesting the mechanism is bowel rest and/or dietary antigen elimination rather than amino acid predigestion.

**For SIBO: probable efficacy.** [[pimentel-ch6-4]] reports a 14-day elemental diet was more than 80% effective in treating SIBO (Pimentel's 2004 study). This is the dietary benchmark: if an oral diet approaches elemental-diet efficacy for breath test normalization, it becomes a first-line therapy.

**Evidence quality:** Established for pediatric Crohn's induction. Probable for adult Crohn's (efficacy likely, compliance is the barrier). Probable for SIBO (single-center data).

### 4.2 Low-FODMAP: Best Formal Evidence in IBS, Not SIBO

The low-FODMAP diet has the best RCT evidence of any elimination diet for IBS, with multiple trials showing symptom reduction. But the evidence is in IBS, not SIBO specifically, and not IBD.

**The gap:** No claim in the graph documents a low-FODMAP trial with SIBO-specific endpoints (breath test normalization, methane reduction). The Rome 2017 report [[rome-sibo2017-4]] discusses breath testing controversy but does not mention low-FODMAP for SIBO. ACG SIBO 2020 [[acg-sibo2020-2]] recommends dietary evaluation as part of SIBO management but does not specify a protocol.

**The limitation:** [[pimentel-lfe-1]] critiques low-FODMAP as "too restrictive (207 foods to avoid), reduces microbiome diversity, and was not designed for SIBO." The Monash protocol's elimination/reintroduction phases are research-validated for IBS but the food list was developed for IBS symptom patterns, not SIBO breath test patterns.

**Evidence quality:** Established for IBS symptom reduction. Speculative for SIBO-specific outcomes (breath test normalization, recurrence rates).

### 4.3 The Specific Carbohydrate Diet (SCD): Strongest Narrative, Weakest Formal Evidence

Gottschall's SCD (1994) is the oldest and most philosophically developed dietary protocol in the graph. The mechanistic narrative is compelling:

**The vicious cycle model.** [[gottschall-ch35-5]] articulates a five-step mechanism: carbohydrate malabsorption → increased luminal carbohydrates → microbial fermentation → acid and gas production → enterocyte injury → further carbohydrate malabsorption (vicious cycle). [[gottschall-ch12-2]] identifies the common denominator: restricting carbohydrates that gut bacteria can ferment.

**The historical lineage.** [[gottschall-ch12-3]] traces a through-line from Aretaeus (300 AD, celiac-type diarrhea treated with fasting) through Samuel Gee (1888, diet therapy for celiac) to the Haas banana diet (1924) to modern SCD. The intellectual tradition is rich but the evidence is case-report-level.

**The evidence gap.** Gottschall claims that "most cases begin to improve within three weeks" [[gottschall-ch910-3]], that the SCD "most often corrects malabsorption" [[gottschall-ch35-8]], and that "the connection between Crohn's disease and a sugar-rich diet is proved beyond reasonable doubt" [[gottschall-ch12-4]]. These are strong claims resting on weak evidence: 600 cited publications establish biological plausibility, but no RCT has tested SCD against placebo or comparator in IBD, IBS, or SIBO.

**The modernization.** [[lapine-cookbook-2]] demonstrates that SCD and low-FODMAP have a substantial intersection: foods that are both SCD-legal and low-FODMAP form a coherent dietary framework. This intersection is a pragmatic starting point that honors both traditions. [[sarna-sibo-diet-2]] integrates SCD principles with low-FODMAP and clinical SIBO experience in Dr. Siebecker's food guide.

**Evidence quality:** Speculative for SCD-specific efficacy. The mechanism is plausible, the case reports are numerous, but no controlled trial exists.

### 4.4 Low-Fermentation Eating (LFE): Simplest Protocol, No Published Trials

Pimentel and Rezaie's LFE (2022) represents the endpoint of the dietary evolution: SCD (1994, carbohydrate-structure-based) → low-FODMAP (2005, fermentation-tested) → Siebecker's SSFG (clinical hybrid) → LFE (2022, SIBO-specific, meal-timing-integrated).

**The two-rule structure.** [[pimentel-lfe-3]]: (1) Restrict products containing high levels of carbohydrates that are not easily digestible, and (2) eat only 2-3 meals per day with 4-5 hours between meals and no snacking. Rule 2 (meal spacing) is grounded in MMC physiology [[pimentel-ch2-1]] and is the protocol's most mechanistically grounded element.

**The evidence gap.** LFE has no published trials. The 80-90% improvement claim is from unpublished clinical experience at Cedars-Sinai [[pimentel-lfe-5]]. Pimentel himself states the limitation: "Diet alone won't cure SIBO. Even if you strictly follow low-fermentation eating, diet alone is not going to get rid of bacterial overgrowth" [[pimentel-lfe-5]]. Dietary therapy is positioned as supportive, not curative -- a management tool to control symptoms while treating the underlying dysmotility/infection.

**Evidence quality:** Speculative for efficacy. The protocol is mechanistically sound but untested.

### 4.5 GAPS and Paleo: Patient-Reported, No Formal Evidence

The GAPS diet (Campbell-McBride) and Paleo approaches (Ballantyne, Myers) occupy Tier 4 in the graph: adjacent frameworks with strong philosophical commitments and no controlled evidence.

**GAPS.** [[campbell-gaps-1]] asserts: "I have no doubt that all autoimmunity is born in the gut." The protocol includes an Introduction Diet with six progressive stages, a Full GAPS Diet, fermented foods as "the most potent probiotics," and detoxification protocols [[campbell-gaps-2]], [[campbell-gaps-3]], [[campbell-gaps-6]]. The claims are confident but rest on the author's clinical experience.

**The Autoimmune Solution (Myers).** [[myers-autoimmune-implicit-9]] asserts that genetic predisposition accounts for only 25% of autoimmune disease risk; the rest is environmental triggers that dietary and lifestyle modification can address. The framework is biologically plausible but untested.

**The Paleo Approach (Ballantyne).** [[ballantyne-paleo-implicit-8]] identifies intestinal permeability ("leaky gut") as the common pathway linking genetics, diet, and autoimmune disease. The mechanism is consistent with the epithelial barrier literature but the Paleo-diet-as-treatment evidence is absent from the graph.

**Evidence quality:** Speculative at best. These are patient experience and practitioner consensus, not clinical evidence. The claims are documented in the graph because they represent real patient-reported outcomes and clinical traditions, but they occupy the lowest tier of the evidence hierarchy.

### 4.6 Dietary Synthesis: A Common Mechanism

The most important insight from the dietary domain is that all effective dietary protocols likely work through the same mechanism: **reducing fermentable substrate reaching colonic bacteria.**

[[sarna-sibo-diet-1]] states it plainly: "All of these diets work for the same reason: They reduce the amount of fermentable carbohydrates you consume." [[gottschall-ch12-2]] identified the same mechanism in 1994 using different language (restricting carbohydrates that intestinal microbes can ferment). [[pimentel-lfe-5]] frames LFE as doing the same thing with a modern understanding of which carbohydrates are fermentable.

If the common mechanism hypothesis is correct, the choice between dietary protocols is driven by compliance, patient preference, and practitioner familiarity -- not evidence of differential efficacy. The practical question becomes not "which diet is best" but "which diet can this patient sustain."

The [[../evidence-briefs/EB-Diet-Comparison]] rates this as low confidence for direct comparison (no head-to-head trials exist) but high confidence for the common mechanism hypothesis (consistent across all major sources, mechanically plausible, consistent with elemental diet efficacy data).

---

## 5. The IBD-SIBO Relationship: What the Evidence Shows

The relationship between IBD and SIBO is the central question the graph was built to investigate. The answer, honestly, is that the evidence is suggestive but not conclusive.

### 5.1 SIBO Prevalence in IBD: Probable but Unvalidated

The most clinically significant claim in the graph on this question is [[pimentel-ch9-3]]: "We have shown that more than 50 percent of such patients [IBD with controlled inflammation but persistent symptoms] have SIBO." This is published data from Pimentel's group. If validated, it would change IBD management: breath testing and SIBO treatment would become standard practice for patients with persistent symptoms despite endoscopic remission, potentially avoiding unnecessary immunosuppression escalation.

**The mechanism is plausible.** IBD causes structural damage (strictures, fistulas, surgical anatomy) that impairs motility. IBD inflammation may damage the migrating motor complex, the small intestine's primary housekeeper mechanism [[pimentel-ch2-1]]. IBD patients receive frequent antibiotics, which alter the microbiome. All three factors -- altered anatomy, impaired MMC, and dysbiosis -- are established contributors to SIBO in other contexts.

**Independent validation is absent.** No claim in the graph from a non-Pimentel source reports SIBO prevalence in IBD patients using validated testing. The 50% figure needs replication.

### 5.2 SIBO as Epiphenomenon vs. Distinct Entity

The graph contains both positions, and both are defensible.

**SIBO as epiphenomenon.** [[acg-sibo2020-6]] states that SIBO is almost always an epiphenomenon -- the underlying cause (motility disorder, structural abnormality, immune deficiency) is the real disease. [[pimentel-ch6-1]] frames SIBO as "not a primary disease" but a consequence of impaired MMC function. Under this model, treating SIBO with antibiotics without addressing the underlying cause is palliative, not curative.

**SIBO as dysbiosis.** [[chutkan-dysbiosis-3]] collapses the distinction: "SIBO is really just another term for dysbiosis that occurs when large amounts of not-so-good bacteria take up residence in the small intestine." Under this model, SIBO is one manifestation of a broader microbiome disturbance, and the distinction between SIBO and IBS/functional dyspepsia/dysbiosis is semantic rather than biological.

**The continuum hypothesis.** [[rome-sibo2017-8]] proposes that IBS and IBD may exist on a continuum, with IBS and IBD at different ends of the inflammatory spectrum. The Keohane 2010 finding -- that IBD patients in "clinical remission" with IBS symptoms had elevated calprotectin, suggesting the IBS symptoms were actually undiagnosed subclinical inflammation -- is the most important data point. It suggests that what appears to be coexistent IBS/SIBO in IBD patients is often undiagnosed active IBD.

**Synthesis.** The question "is SIBO a distinct entity or one manifestation of dysbiosis?" is answerable only if we define the level of analysis. At the microbial ecology level, SIBO is clearly dysbiosis -- an alteration of the normal small intestinal microbial community. At the clinical level, SIBO is a useful diagnostic category because it directs treatment (antibiotics, prokinetics, dietary modification) that differs from IBD treatment (anti-inflammatories, immunosuppressants, biologics). The pragmatic answer is that SIBO is clinically useful even if it is not biologically unique.

**Evidence quality:** The epiphenomenon framing is established (consistent across ACG, AGA, and Pimentel). The continuum hypothesis is probable (Keohane 2010 is the strongest data point; Rome 2017 endorses it as a working hypothesis). The dysbiosis reframing is speculative (Chutkan is a single voice; the claim is philosophically coherent but not empirically demonstrated).

### 5.3 Does Treating SIBO in IBD Patients Improve Outcomes?

**The graph does not answer this question.** There is no claim documenting a trial of SIBO-directed therapy in IBD patients with SIBO-positive breath tests that measures IBD-specific outcomes (endoscopic inflammation, calprotectin, hospitalization, surgery).

The closest evidence is:
- [[pimentel-ch9-3]]: SIBO is present in >50% of IBD patients with persistent symptoms
- [[acg-sibo2020-7]]: rifaximin has 61-78% efficacy for SIBO treatment
- [[pimentel-lfe-5]]: dietary therapy reduces SIBO symptoms but does not cure SIBO

These three claims, when combined, suggest a clinical hypothesis: identify SIBO in IBD patients with persistent symptoms despite endoscopic remission, treat with rifaximin and/or dietary therapy, and expect symptomatic improvement. But the evidence chain is missing the final link: does treating SIBO improve IBD outcomes beyond symptom relief?

The [[../questions/SIBO-IBD-contribution]] formalizes this gap with a study design: a randomized trial of SIBO-directed therapy in IBD patients with breath-test-confirmed SIBO, measuring both symptom scores and endoscopic endpoints.

**Evidence quality:** The individual claims (SIBO prevalence in IBD, rifaximin efficacy, dietary symptom relief) are probable. The clinical outcome question is unresolved.

---

## 6. Prokinetics and SIBO Prevention: Modest Evidence, High Stakes

Prokinetic therapy is Pillar 3 of Pimentel's SIBO management framework (prevention of recurrence). The evidence is modest but the clinical stakes are high: SIBO recurrence after antibiotic treatment is common, and preventing recurrence is the difference between episodic treatment and chronic disease management.

**The prokinetic evolution.** [[pimentel-evol-4]] traces the evolution from erythromycin (antibiotic + prokinetic, limited by tachyphylaxis) or tegaserod (withdrawn for cardiac safety, reintroduced with restrictions) in 2006, to prucalopride (selective 5-HT4 agonist, better safety profile) as the preferred agent in 2022. Serotonin agonists prevent SIBO recurrence for 200+ days vs erythromycin's "few months."

**The nighttime dosing rationale.** Prokinetics are dosed at bedtime, not with meals. This targets the fasting MMC (migrating motor complex), which occurs during sleep and between meals -- not feeding motility. The rationale is mechanistic and elegant [[pimentel-ch2-1]].

**The evidence gap.** The prokinetic efficacy data is from Pimentel's group and has not been independently replicated at scale. The drug holiday strategy (cycling prokinetics to prevent tachyphylaxis) is clinically sensible but untested. Long-term prokinetic safety in SIBO patients (beyond 1-2 years) is not documented in the graph.

**Sarna's expanded options.** [[sarna-guide-2]] adds naturopathic prokinetics (Iberogast, ginger) and acknowledges that "most SIBO patients need more than one course of treatment." This is consistent with Pimentel's framework: SIBO management is chronic, not acute.

**Evidence quality:** The MMC mechanism is established. Prokinetic efficacy for SIBO prevention is probable (single-group data, biologically plausible, consistent clinical experience). Long-term efficacy and safety are speculative.

---

## 7. Unanswered Questions

The graph surfaces three categories of unanswered questions. Each is documented in the [[../questions/Questions Index]].

### 7.1 Questions the Graph Cannot Answer (No Evidence Exists)

**Is SIBO a distinct entity or one manifestation of dysbiosis?** The graph contains both positions but no evidence that distinguishes between them. Resolution requires a study comparing treatment response in patients diagnosed with "SIBO" (breath test criteria) vs "dysbiosis" (16S rRNA profiling criteria) to determine whether these are overlapping or distinct populations.

**Does treating SIBO in IBD patients improve outcomes beyond symptom relief?** No trial exists. The graph contains prevalence data, treatment efficacy data, and mechanistic rationale, but the final link -- does SIBO treatment change IBD outcomes? -- is absent. See [[../questions/SIBO-IBD-contribution]].

**What is the long-term efficacy of prokinetics for SIBO prevention?** The graph documents short-term efficacy (200+ days) from a single research group. Long-term data (>2 years) and independent replication are absent.

### 7.2 Questions the Graph Partially Answers (Evidence Exists but Is Contested)

**What is the optimal dietary protocol for SIBO?** The graph strongly suggests a common mechanism (reducing fermentable substrate) but cannot rank SCD, low-FODMAP, and LFE against each other. The practical guidance -- start with the SCD + low-FODMAP intersection, adapt based on compliance and symptom response -- is expert consensus, not evidence. See [[../questions/SIBO-diet-comparison]].

**Is treat-to-target justified by the evidence?** The graph shows that treat-to-target is consensus-driven, not trial-proven. The paradigm is clinically sensible but rests on precautionary reasoning. A definitive trial -- randomizing patients to treat-to-target vs symptom-based management -- would resolve the question but may be ethically challenging to conduct given the strength of expert consensus. See [[../questions/treat-to-target-evidence]].

### 7.3 Questions the Graph Answers (Evidence Is Established)

**Are biologics superior to step-up therapy for moderate-severe IBD?** Yes. The convergence across ACG, AGA, ECCO, and BSG is strong. Anti-TNF therapy is high-quality evidence for induction; combination therapy is superior to monotherapy; early biologic ± immunomodulator is recommended over step-up for high-risk patients.

**Does EEN induce remission in pediatric Crohn's?** Yes. Meta-analysis-grade evidence confirms EEN equivalence to corticosteroids with superior mucosal healing. The adult evidence is weaker due to compliance barriers, not biological inefficacy.

**Do symptoms correlate with mucosal inflammation in IBD?** No. The symptom-inflammation disconnect is settled science. Treating symptoms without objective inflammation data is demonstrably insufficient.

---

## 8. Evidence Confidence Summary

| Claim Domain | Confidence | Basis |
|-------------|-----------|-------|
| 5-ASA efficacy for mild-moderate UC | High | Network meta-analysis of 48 trials; strong recommendations across ACG, AGA, ECCO |
| Corticosteroid induction efficacy | High | Multiple RCTs; guideline consensus |
| Corticosteroid maintenance contraindication | High | Guideline consensus; toxicity data |
| Anti-TNF superiority for moderate-severe IBD | High | Multiple RCTs; network meta-analysis |
| Early biologic over step-up for high-risk CD | Medium | Guideline consensus; observational data; no RCT |
| Treat-to-target paradigm | Medium | Consensus-driven; symptom-inflammation disconnect is established |
| Specific treatment targets (Mayo 0 vs 1) | Low | Cohort studies; expert opinion |
| EEN for pediatric Crohn's induction | High | Multiple meta-analyses |
| EEN for adult Crohn's | Medium | Biological efficacy likely; compliance barrier |
| EEN/elemental diet for SIBO | Medium | Single-center data (>80% efficacy) |
| Low-FODMAP for IBS | High | Multiple RCTs |
| Low-FODMAP for SIBO | Low | No SIBO-specific trials |
| SCD for IBD/SIBO | Low | Case reports; mechanistic plausibility; no RCT |
| LFE for SIBO | Low | No published trials |
| GAPS/Paleo for autoimmunity | Very low | Patient-reported; practitioner consensus |
| SIBO breath test clinical validity | Medium for utility; low for diagnostic accuracy | Clinical correlation data exists; gold standard is contested |
| SIBO as epiphenomenon | Medium | Consensus across ACG and Pimentel |
| SIBO in IBD (>50% prevalence) | Low | Single-group data; needs replication |
| Prokinetics for SIBO prevention | Medium | Single-group data; short-term follow-up |
| Prokinetic long-term efficacy/safety | Very low | No data beyond 1-2 years |

---

## 9. Limitations of This Synthesis

1. **174 edges is not a knowledge graph.** This capstone synthesizes claims, not edge structure. The graph's structural analysis (Phase 4) identified fragmentation as the defining characteristic. Most assertions in this capstone are drawn from claims that are not structurally connected to each other through typed edges. The synthesis is accurate at the claim level but cannot draw on graph-theoretic insights (centrality, cascade chains, contradiction camp analysis) that a denser graph would enable.

2. **The dietary corpus is philosophically rich but empirically weak.** Gottschall's SCD, Campbell-McBride's GAPS, and Ballantyne's Paleo Approach are practitioner traditions with strong internal logic and passionate patient communities. They exist in the graph alongside clinical guidelines that require RCT-level evidence for a weak recommendation. The capstone must acknowledge both the intellectual tradition (which is real and clinically influential) and the evidence gap (which is equally real).

3. **The Pimentel concentration.** Claims from Pimentel's group dominate the SIBO domain (ACG SIBO 2020, The Microbiome Connection, A New IBS Solution). This is not methodological bias -- Pimentel is the most prolific and cited SIBO researcher. But it means the SIBO evidence base in the graph is largely from one research program. Independent replication would strengthen every claim.

4. **The graph does not contain pediatric IBD.** This is a significant gap. Pediatric IBD has distinct epidemiology, treatment paradigms (EEN first-line in Europe), and disease behavior. The exclusion means the capstone cannot address the pediatric-to-adult transition or the role of early-life microbiome interventions.

5. **No patient-reported outcomes are in the graph.** The graph contains practitioner claims about patient experience but does not contain direct patient data (quality of life surveys, symptom diaries, treatment satisfaction). A complete picture of the IBD-SIBO relationship would need the patient voice alongside the clinical evidence.

---

## 10. Recommendations for Future Work

1. **Phase 3 extension: connect diet to treatment guidelines.** The dietary archipelago (77 orphan claims) is the largest structural gap. Targeted edge construction connecting SCD/low-FODMAP/LFE claims to the treatment guideline spine via `depends_on` edges to mechanisms ("reduce fermentable substrate," "MMC restoration") would dramatically improve graph connectivity.

2. **Phase 3 extension: connect SIBO pathophysiology to clinical recommendations.** The SIBO mechanism claims (MMC impairment, vinculin autoimmunity, food poisoning etiology) exist as isolated nodes. Connecting them to treatment claims (prokinetics, rifaximin, dietary restriction) via `depends_on` edges would make the pathophysiological rationale visible in the graph structure.

3. **Acquire pediatric IBD sources.** The BSG guideline's EEN recommendation for pediatric CD and the Thompson elemental diet protocol reference pediatric data extensively. Adding a pediatric IBD guideline (ECCO/ESPGHAN) and pediatric-specific SIBO literature would close a significant domain gap.

4. **Add patient-reported outcome data.** Quality-of-life surveys, symptom tracking tools, and treatment satisfaction data from patient registries or systematic reviews would add the missing dimension of patient experience.

5. **Validate the Pimentel SIBO-in-IBD data.** The >50% prevalence claim is the most clinically actionable finding in the graph. A systematic search for independent validation studies (or their absence) would determine whether this claim is ready for clinical decision-making or remains an interesting but unvalidated finding.

---

## 11. Artifacts

| Artifact | Path | Description |
|----------|------|-------------|
| Phase 4 Synthesis | [[Phase-4-Synthesis]] | Structural analysis: hinges, cascades, gaps |
| Evidence Brief 1 | [[../evidence-briefs/EB-SIBO-IBD-Symptoms]] | SIBO-IBD symptom contribution |
| Evidence Brief 2 | [[../evidence-briefs/EB-Diet-Comparison]] | Dietary protocol comparison |
| Evidence Brief 3 | [[../evidence-briefs/EB-Treat-to-Target]] | Treat-to-target justification |
| Question 1 | [[../questions/SIBO-IBD-contribution]] | SIBO in IBD research gap |
| Question 2 | [[../questions/SIBO-diet-comparison]] | Diet comparison research gap |
| Question 3 | [[../questions/treat-to-target-evidence]] | Treat-to-target evidence gap |
| This Capstone | [[Phase-5-Capstone]] | Culminating synthesis |
