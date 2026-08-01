---
tags:
  - source/book-notes
  - oskg-ibd
  - pathophysiology
  - mechanism/genetics
  - mechanism/immune-dysfunction
  - mechanism/epithelial-barrier
  - mechanism/microbiome
  - scholars/ananthakrishnan
  - scholars/xavier
  - scholars/podolsky
  - tier-1
  - type/reading-note
  - source/yamada-textbook-7e
created: 2026-08-01
updated: 2026-08-01
confidence: high
source:
  title: "Yamada's Textbook of Gastroenterology, 7th Edition"
  author: "Ashwin N. Ananthakrishnan, Ramnik J. Xavier, Daniel K. Podolsky (Ch 62)"
  year: 2022
  publisher: "Wiley-Blackwell"
  local_file: "sources/books/Yamada-Textbook-Gastroenterology-7E-2022.txt"
related:
  - "[[Yamada 2022 - Ch63 Ulcerative Colitis Clinical Manifestations and Management]]"
  - "[[Yamada 2022 - Ch64 Crohn's Disease Clinical Manifestations and Management]]"
  - "[[Yamada 2022 - Ch66 Misc Colonic Disorders]]"
  - "[[../diagnosis/Diagnosis Index]]"
  - "[[../microbiome/Microbiome Index]]"
---
claims_status: extracted
claims_extracted_date: 2026-08-01
claims_count: 10
claims_files: ["claim-yamada-ibd62-1", "claim-yamada-ibd62-2", "claim-yamada-ibd62-3", "claim-yamada-ibd62-4", "claim-yamada-ibd62-5", "claim-yamada-ibd62-6", "claim-yamada-ibd62-7", "claim-yamada-ibd62-8", "claim-yamada-ibd62-9", "claim-yamada-ibd62-10"]


# Yamada 7E -- Ch 62: Inflammatory Bowel Diseases: Pathogenesis

This chapter is the definitive academic review of IBD pathogenesis as of 2022. Authored by three leading investigators (Ananthakrishnan at MGH, Xavier at the Broad Institute/Harvard, Podolsky at UTSW), it synthesizes two decades of GWAS, microbiome, and immunological research into a coherent multi-hit model: genetic susceptibility primes the host; environmental triggers and microbial dysbiosis disrupt homeostasis; barrier dysfunction and immune dysregulation sustain chronic inflammation. The chapter covers genetics (200+ loci), serology, epithelial barrier biology, innate and adaptive immunity, the gut microbiome, and environmental epidemiology. It is the single most important document in this knowledge graph for understanding why IBD develops.

---

## Claim 1: IBD arises from loss of immune tolerance to commensal flora in genetically susceptible individuals

**Author's claim:** "It is increasingly clear that a key pathogenic mechanism underlying development of IBD is the loss of tolerance and dysregulation of the immune response to commensal intestinal flora in genetically susceptible individuals. Thus, the pathogenesis of these complex diseases requires the interaction of host genetics, immune dysregulation, internal microenvironment (the gut microbiome), as well as the external environment."

**Evidence presented:** Twin concordance data: monozygotic concordance 30-35% for Crohn's disease vs 10-15% for ulcerative colitis, demonstrating genetics contributes more to CD but environment dominates both. Family history is the strongest risk factor: lifetime risk 5.2% for relatives of CD probands vs 1.6% for UC probands, with higher rates among Jews (7.8% and 4.5%). Rapid temporal changes in incidence over six decades and risk shifts with migration support environmental contribution. GWAS identification of 200+ risk loci provides the genetic architecture; microbiome studies (Pediatric RISK cohort, PROTECT cohort, Lloyd-Price longitudinal multi-omics) demonstrate dysbiosis patterns. The IL10-/- mouse develops colitis only in the presence of gut bacteria, not in germ-free conditions.

**Confidence:** VERY HIGH. This is the consensus model. Every major textbook and guideline (ECCO, AGA, ACG) frames IBD pathogenesis this way. The convergence of genetic, microbial, epidemiological, and animal model data is overwhelming.

**What's at stake:** This model unifies diverse findings under one framework. It also explains why no single therapeutic approach cures IBD: you can block TNF-α (infliximab) or IL-23 (ustekinumab) or modulate the microbiome (FMT), but without addressing the underlying genetic susceptibility and environmental triggers, the disease persists. It predicts that prevention will require environmental modification in at-risk genotypes.

**Who disagrees:** No meaningful scholarly disagreement with the broad framework. Debate centers on the relative weight of each component and the causal direction of microbiome changes (cause vs consequence of inflammation).

**Alternative reading:** An older model proposed IBD as primarily an autoimmune disease with specific autoantigens, analogous to rheumatoid arthritis or lupus. The serological data (ASCA, pANCA) and the efficacy of immunosuppressive biologics partially support this framing, but the absence of a consistent autoantigen, the microbial specificity of the serological markers, and the germ-free mouse data make the dysregulated-host-microbe-interaction model more persuasive.

**My assessment:** This is the foundation. Everything else in this knowledge graph -- diagnosis, treatment, diet -- operates within this framework. The critical insight is that IBD is not one disease but a final common pathway for multiple distinct genetic and environmental insults converging on intestinal inflammation.

---

## Claim 2: GWAS has identified over 200 risk loci, but genetics explains only a modest fraction of disease heritability

**Author's claim:** "In a large international collaborative study including over 75 000 patients with Crohn's disease, ulcerative colitis, and healthy controls, 163 distinct genetic risk loci were identified that met genome-wide significance thresholds... All risk loci together contributed to 13.6% of the risk of Crohn's disease, and an even smaller fraction of disease risk (7.5%) in ulcerative colitis."

**Evidence presented:** The Jostins et al. (2012) study of 75,000 individuals identified 163 loci. A subsequent expansion (de Lange et al. 2017) with 96,486 individuals added 38 more loci. Key findings: (a) 110/163 loci confer risk of both CD and UC, suggesting shared pathways; (b) 50 loci have identical effect sizes in both diseases; (c) NOD2 and PTPN22 have opposite effects -- both increase CD risk but are protective against UC; (d) the IL23R SNP with the largest effect in Europeans was not associated with disease in East Asians, while TNFSF15 effects were more prominent in East Asians, demonstrating ancestry-specific genetic architecture; (e) African-specific SNPs at ZNF649 and LSAMP were identified in separate cohorts.

**Confidence:** VERY HIGH. These findings come from massive, replicated GWAS with stringent significance thresholds (p < 5 x 10^-8). The multi-ancestry replication strengthens confidence.

**What's at stake:** The "missing heritability" problem: if genetics explains only 13.6% of CD risk, what explains the rest? Gene-environment interactions, rare variants with large effects (not captured by GWAS), epigenetic modifications, and the microbiome all become candidates. This shapes drug development strategy -- if the genetic signal is modest, targeting downstream inflammatory pathways (TNF, IL-23, JAK) may be more effective than targeting specific genetic defects.

**Who disagrees:** Some geneticists argue that GWAS underestimates heritability because common SNPs on genotyping arrays tag but do not capture the causal rare variants. Deep sequencing studies (Rivas et al. 2011, Huang et al. 2017) support this: fine mapping identified 18 causal variants with >95% certainty and additional rare protective variants in NOD2, CARD9, and IL23R. The "missing heritability" may be partially resolved by including these rare variants in risk models.

**My assessment:** The 13.6% figure is a lower bound. As fine mapping and whole-genome sequencing advance, the explained variance will increase. But the fundamental point stands: genetics alone is insufficient. The clinical implication is important -- genetic testing for IBD risk (commercial panels already exist for NOD2, ATG16L1) has limited predictive value and is not standard of care.

---

## Claim 3: NOD2 is the strongest CD susceptibility gene, functioning as an intracellular bacterial sensor whose loss impairs innate immunity

**Author's claim:** "NOD2 (nucleotide-binding oligomerization domain containing protein 2) on chromosome 16 was the first genetic variant associated with Crohn's disease, with three common polymorphisms, Arg702Trp, Gly908Arg, and Leu1007fsX1008... The main function of NOD2 is to act as an intracellular sensor of the peptidoglycan muramyl dipeptide (MDP) in the bacterial cell walls. Activation of NOD2 by its antigenic trigger results in a cascade of downstream activation, including nuclear factor-κB (NF-κB) and mitogen-activated protein kinase signaling."

**Evidence presented:** NOD2 variants are present in 30% of individuals of European ancestry with CD. Deep sequencing identified five additional rare variants (Rivas et al. 2011). NOD2 homozygosity or heterozygosity alone is not sufficient for disease -- penetrance requires additional factors. NOD2-deficient mice demonstrate impaired IL-23 production in response to MDP + TLR2 costimulation, suggesting cross-talk with the IL-23 pathway. In surgical specimens, the proportion of abnormal Paneth cells correlates with the cumulative burden of NOD2 risk alleles, and high proportions of abnormal Paneth cells predict shorter time to postoperative recurrence (VanDussen et al. 2014). NOD2 variants are rare and not associated with CD in East Asians, demonstrating ancestry-specific genetic architecture.

**Confidence:** VERY HIGH. NOD2 is the most replicated finding in IBD genetics. The functional mechanism (MDP sensing -> NF-κB activation -> cytokine production) is well-characterized.

**What's at stake:** NOD2 represents the clearest link between genetics and the "defective innate immunity" model of CD. If CD is fundamentally a failure of bacterial sensing and clearance (rather than an overactive immune response), then immunosuppression treats the consequence (inflammation) rather than the cause (bacterial persistence). This has therapeutic implications: strategies that enhance bacterial clearance (antibiotics, autophagy-enhancing drugs, Paneth cell restoration) might address root causes.

**Who disagrees:** The NOD2 story is largely settled. Debate exists about whether NOD2 variants cause CD through impaired NF-κB activation (loss of function) or through altered microbiome composition secondary to defective antimicrobial peptide secretion. The two mechanisms are not mutually exclusive.

**My assessment:** NOD2 is the poster child for CD genetics. But the clinical reality is sobering: 30% of European CD patients carry NOD2 variants, but the population prevalence of these variants is also high. NOD2 status alone has limited clinical utility for diagnosis or prognosis. The value is in understanding mechanism.

---

## Claim 4: The autophagy pathway (ATG16L1, IRGM, LRRK2) is central to CD pathogenesis through effects on Paneth cells and goblet cells

**Author's claim:** "Polymorphisms in several loci involved in autophagy, including ATG16L1, LRRK2, and IRGM, appear to play important roles in the pathogenesis of Crohn's disease... Defects in autophagy may interact with microbial triggers to induce an inflammatory response. Atg16L1 hypomorphic mice reared in a germ-free environment do not display the same Paneth cell abnormalities as conventionally reared mice. Exposure to murine norovirus infection in such mice results in abnormal Paneth cell number and function."

**Evidence presented:** Mice with hypomorphic Atg16l1 or deficient Atg5 in intestinal epithelial cells exhibit aberrant Paneth cell number and location and deficient antimicrobial peptide secretion. Identical defects are observed in biopsies from CD patients carrying the T300A variant of ATG16L1 (Cadwell et al. 2008). IRGM variants are associated with reduced IRGM expression in terminal ileum, upregulation of whole-blood TNF, and increased ileal lactoferrin. IRGM limits NLRP3 inflammasome activation and negatively regulates IL-1β maturation, limiting pyroptosis (Mehto et al. 2019). Cumulative burden of NOD2 + ATG16L1 variants acts additively to influence Paneth cell distribution and function. Variants also influence goblet cell morphology (Lassen et al. 2014, Pott et al. 2018).

**Confidence:** HIGH. The mechanistic chain (genetic variant -> autophagy defect -> Paneth cell dysfunction -> reduced antimicrobial peptide secretion -> altered microbial handling -> inflammation) is well-established in mouse models. Human biopsy data corroborate the Paneth cell phenotype.

**What's at stake:** This is the strongest evidence for a specific cellular mechanism linking a CD risk allele to a functional defect. The germ-free mouse experiment (Cadwell et al. 2010) is landmark: it proves that the ATG16L1 mutation alone does not cause pathology -- a viral trigger (murine norovirus) is required. This directly supports the multi-hit model. It also suggests that targeting specific viruses or restoring autophagy function could be therapeutic strategies.

**Who disagrees:** The relevance of murine norovirus as a model for human triggers is debated. Human norovirus is not established as an IBD trigger. The specific pathogen(s) interacting with ATG16L1 variants in humans remain unknown.

**Alternative reading:** The autophagy defects may contribute to CD primarily through effects on antigen presentation and adaptive immunity (dendritic cell autophagy influences MHC class II presentation of microbial antigens) rather than through Paneth cells specifically.

**My assessment:** The ATG16L1 story is the most mechanistically satisfying in IBD genetics because it connects a common variant to a cellular phenotype to a microbial interaction. The therapeutic implication -- that autophagy-enhancing drugs might treat CD -- is speculative but supported by the biology.

---

## Claim 5: The IL-23/Th17 pathway is the dominant effector pathway in CD, while UC is historically classified as Th2-mediated

**Author's claim:** "Th1 and Th17 cells play a role in the development of Crohn's disease. The intestinal mucosa of patients with Crohn's disease manifests increased concentrations of TNF-α and interferon (IFN)-γ... In contrast, ulcerative colitis has historically been presented as dependent on Th2-cell-mediated responses. Th2 cells are characterized by production of IL-4, IL-5, and IL-13."

**Evidence presented:** CD mucosa: increased TNF-α, IFN-γ, IL-2, IL-8. Th17 cells are elevated and overexpress IL-17A. Both risk and protective variants in IL23R exist. Ustekinumab (anti-p40 subunit shared by IL-12 and IL-23) is efficacious in both CD and UC (Feagan et al. 2016, Sands et al. 2019). UC mucosa: mucosal T cells produce more IL-5 than CD; NK T cells secrete more IL-13. However, "ulcerative colitis does not appear to be a purely Th2-mediated inflammatory disease" -- low IL-13 and IFN-γ dominance are observed in some patients. Secukinumab (anti-IL-17A) failed in CD and was associated with disease worsening (Hueber et al. 2012), suggesting IL-17A has protective as well as pro-inflammatory effects in the gut.

**Confidence:** HIGH for the Th1/Th17 role in CD. MEDIUM for the UC as Th2 classification -- the authors themselves note heterogeneity.

**What's at stake:** The Th1/Th17 vs Th2 distinction has driven drug development. Anti-TNF (infliximab, adalimumab) targets the Th1 pathway. Ustekinumab targets IL-12/23 (Th1/Th17). Tofacitinib targets JAK-STAT signaling downstream of multiple cytokines. The failure of anti-IL-17 in CD was a major surprise and revealed that IL-17 has protective mucosal functions -- a cautionary tale for reducing immunology to simple Th-subset dichotomies.

**Who disagrees:** The Th2 classification of UC is increasingly questioned. Transcriptomic analyses (Smillie et al. 2019, single-cell atlas of 366,650 cells from UC biopsies) reveal far more complexity: UC involves multiple cell types and pathways beyond the Th2 axis, including stromal and epithelial contributions. Some argue that UC and CD are better classified by the tissue response pattern (mucosal-limited vs transmural) than by T-cell subset.

**Alternative reading:** A unified model: both CD and UC involve mixed Th1/Th17 responses, with the difference being the anatomical distribution and depth of inflammation rather than the fundamental immunological mechanism. The "Th2 UC" model may reflect the fact that colonic mucosa has a different baseline immunological setpoint than ileal mucosa.

**My assessment:** The CD = Th1/Th17 model is well-supported and clinically validated (ustekinumab works). The UC = Th2 model is a simplification that the chapter authors themselves hedge on. The key takeaway for this knowledge graph: the immunological distinction between CD and UC is real but blurred, which explains why some therapies work for both diseases despite their different clinical phenotypes.

---

## Claim 6: Epithelial barrier dysfunction is genetically programmed in IBD and represents a primary defect, not just a consequence of inflammation

**Author's claim:** "Not only patients with inflammatory bowel disease but also their first-degree relatives demonstrate an alteration in intestinal permeability... Several of the IBD risk loci-associated genes, including CDH1, HNF4A, GNA12, MUC19, and ITLN1, play an important role in the maintenance of the intestinal epithelial barrier."

**Evidence presented:** First-degree relatives of IBD patients have increased intestinal permeability (referenced to studies 70-73). CDH1 polymorphisms produce truncated E-cadherin with defective plasma membrane localization and cytosolic accumulation, leading to defective goblet and Paneth cell maturation. HNF4A deletion causes spontaneous colitis in mice; IBD biopsies show reduced HNF4A expression. A polygenic barrier function risk score (128 barrier genes) was higher in IBD patients than controls -- PTGER4 most enriched in CD, HNF4A most enriched in UC. MUC1 and MUC4 remained dysregulated even after inflammation resolution, suggesting they are primary defects, not secondary to inflammation. In IBD, bacteria are found within the inner mucous layer (normally bacteria-free in healthy individuals). WFDC2 (an antiprotease) is downregulated in IBD -- it inhibits bacterial growth, preserves tight junctions, and prevents inflammatory cascades.

**Confidence:** HIGH. The convergence of genetic data (barrier gene risk loci), family studies (asymptomatic relatives have increased permeability), histological findings (bacteria in inner mucus layer), and mouse models (HNF4A deletion causes spontaneous colitis) makes this one of the most robust components of the pathogenesis model.

**What's at stake:** If barrier dysfunction is primary and genetically programmed, then therapies that restore barrier function (mucus restoration, tight junction enhancement, antiprotease replacement) could prevent disease in at-risk individuals. The barrier hypothesis also integrates diet into pathogenesis: dietary emulsifiers (referenced to Chassaing et al.) disrupt the mucus barrier and induce inflammation in animal models.

**Who disagrees:** Debate about whether barrier dysfunction causes inflammation or results from it. The family studies (asymptomatic relatives with increased permeability) and the persistent MUC1/MUC4 dysregulation after inflammation resolution argue for primacy. But increased permeability could also reflect subclinical inflammation in relatives who share environmental exposures.

**Alternative reading:** Barrier dysfunction is necessary but not sufficient -- it allows microbial antigens access to the immune system, but whether inflammation develops depends on the individual's immune response genetics and microbial composition. The barrier defect may be the "first hit" in some patients but not others.

**My assessment:** The barrier genetics are compelling and underappreciated in clinical practice. Gastroenterologists think about immune suppression; they don't think about barrier restoration. The MUC1/MUC4 persistence data is particularly significant because it suggests that even in endoscopic remission, the mucosal barrier may not be fully intact -- which could explain the high rate of relapse after treatment de-escalation.

---

## Claim 7: The gut microbiome in IBD shows reduced diversity with specific taxonomic shifts, and F. prausnitzii is a key protective species

**Author's claim:** "Patients with IBD demonstrate a reduction in diversity of microbiota compared to controls, primarily attributable to loss of anaerobic bacteria like Bacteroidetes... Faecalibacterium prausnitzii from ileal biopsies of Crohn's disease patients undergoing ileocecal resection is associated with higher rates of relapse, and intragastric administration of F. prausnitzii in mice was associated with amelioration of colitis."

**Evidence presented:** Key microbial patterns in IBD: reduced Firmicutes and Bacteroidetes, increased Proteobacteria and Actinobacteria (Frank et al. 2007). Enteroadherent invasive E. coli (AIEC) more common in ileal CD lesions. Fusobacterium nucleatum invasive strains isolated from inflamed IBD mucosa (Strauss et al. 2011). Reduced F. prausnitzii predicts postoperative CD recurrence (Sokol et al. 2008). F. prausnitzii supernatants have anti-inflammatory properties. Ruminococcus gnavus blooms co-occur with disease activity; a specific clade produces a pro-inflammatory glucorhamnan polysaccharide inducing TLR4-dependent TNF-α secretion (Henke et al. 2019). The Pediatric RISK cohort (Gevers et al. 2014, 447 treatment-naive CD patients) confirmed Enterobacteriaceae expansion and identified novel taxa (Veillonellaceae, Neisseriaceae, Fusobacteriaceae). The Lloyd-Price longitudinal multi-omics study (2019, 132 subjects, up to 24 time points) revealed periods of dysbiosis in 17% of samples (24% CD, 12% UC) and reduced SCFAs including butyrate during dysbiosis.

**Confidence:** HIGH for the association between dysbiosis and IBD. MEDIUM for causality -- most studies are cross-sectional or longitudinal-observational, not interventional. The germ-free mouse experiments (IL10-/- mice don't develop colitis without bacteria) prove that microbes are necessary, but whether specific dysbiosis patterns cause inflammation or result from it is harder to establish.

**What's at stake:** If specific microbial taxa (F. prausnitzii) are protective and others (AIEC, R. gnavus, F. nucleatum) are pathogenic, then microbiome-modifying therapies -- precision probiotics, FMT from healthy donors, bacteriophage therapy targeting pathobionts -- have a rational mechanistic basis. The Lloyd-Price study is important because it demonstrates that dysbiosis is intermittent, not constant, which has implications for when to sample and treat.

**Who disagrees:** Debate about whether dysbiosis is cause or consequence. The germ-free mouse experiments demonstrate necessity but not specificity -- any microbial colonization might trigger inflammation in a susceptible host, not just specific pathogens. Some argue that inflammation itself creates an oxidative environment that selects for aerotolerant taxa (Proteobacteria), making dysbiosis a downstream effect.

**My assessment:** This is probably not an either/or. The evidence supports bidirectionality: genetic defects (NOD2, ATG16L1) alter microbial handling, producing dysbiosis; dysbiosis then amplifies inflammation through reduced SCFA production, increased pathogen-associated molecular patterns, and mucus degradation. The question is whether correcting dysbiosis alone (without addressing genetics or immunity) can induce and maintain remission. The FMT trials in UC (Paramsothy et al. 2017) suggest partial efficacy, supporting a causal role for the microbiome.

---

## Claim 8: Smoking has a divergent effect on CD and UC -- the most consistently replicated environmental finding with mechanistic implications

**Author's claim:** "Current smokers have a twofold increase in risk of Crohn's disease... In contrast, former smoking is associated with substantial increase in risk of ulcerative colitis within 1 year of quitting, while current smoking appears to be protective."

**Evidence presented:** Meta-analyses consistently show smoking increases CD risk (OR ~2.0) and decreases UC risk. In established CD, smoking increases therapy escalation, surgery rates, and postoperative recurrence. In established UC, ongoing smoking is associated with milder disease and reduced colectomy rates. Mechanistic hypothesis: mononuclear cells from CD patients exposed to cigarette smoke demonstrate reduced protection from oxidative stress through reduced Hsp70 production (Bergeron et al. 2012); UC patients do not show this defect. The divergent effect is not seen in Asian cohorts, where smoking associations are weaker or absent (Ng et al. 2015).

**Confidence:** VERY HIGH for the epidemiological association. LOW for the mechanism -- why smoking protects against UC remains unclear.

**What's at stake:** Smoking is the single most actionable environmental risk factor. Smoking cessation prevents CD and worsens UC -- a clinical paradox that every gastroenterologist navigates. The different effect on CD vs UC is a powerful clue that the two diseases have fundamentally different initiating mechanisms despite shared genetic risk loci. If the mechanism could be isolated (nicotine? carbon monoxide? oxidative stress modulation?), it could yield a UC-specific therapy.

**Who disagrees:** No disagreement about the epidemiological association. The debate is purely mechanistic.

**Alternative reading:** Smoking may not be directly causal. The association could reflect confounding: people who smoke differ from non-smokers in diet, socioeconomic status, and other health behaviors. The temporal relationship (disease onset often precedes smoking cessation rather than follows it) complicates causal inference.

**My assessment:** The smoking paradox is the most tantalizing unsolved puzzle in IBD epidemiology. It's been known for decades and we still don't understand the mechanism. For clinical practice, the message is clear: CD patients must stop smoking; UC patients should not start smoking to treat their disease (the cardiovascular and cancer risks far outweigh any potential benefit).

---

## Claim 9: Very early-onset IBD (VEOIBD) represents a distinct monogenic subtype caused by loss-of-function mutations in immune pathways

**Author's claim:** "Very early-onset IBD represents a distinct phenotype where inflammatory bowel disease develops in children within the first few months of life... Three distinct homozygous mutations in genes encoding the IL-10 receptor (IL-10RA and IL-10RB) were identified, suggesting that distinct subtypes of IBD may be mediated through specific pathways."

**Evidence presented:** VEOIBD is characterized by pancolonic inflammation, high perianal involvement, medical therapy refractoriness, and rising incidence. Glocker et al. (2009) identified IL-10RA and IL-10RB mutations in nine patients through linkage analysis and candidate gene sequencing. Allogeneic stem cell transplant achieves sustained clinical remission in this subgroup (Kotlarz et al. 2012). Other VEOIBD variants include NADPH oxidase genes NOX1 and DUOX2 (Hayes et al. 2015, Parlato et al. 2017) and TRIM22 affecting NOD2 signaling (Li et al. 2017). The paradigm: "very early-onset disease may result from complete loss of gene function while adult-onset disease may reflect more subtle alterations in gene functions through SNPs" -- analogous to familial hypercholesterolemia (monogenic) vs polygenic dyslipidemia.

**Confidence:** HIGH. The IL-10R mutations in VEOIBD are a clear monogenic cause with a functional mechanism and a curative therapy (stem cell transplant). This is the cleanest demonstration of causality in the entire IBD genetics literature.

**What's at stake:** VEOIBD demonstrates that IBD is a syndrome with multiple distinct etiologies, not a single disease. The therapeutic implication is radical: for VEOIBD caused by IL-10R deficiency, stem cell transplant is curative (replacing the defective immune system), whereas for adult polygenic CD, immunosuppression manages but does not cure. This supports a precision medicine approach: genotype early, and if a monogenic cause is found, treat accordingly.

**Who disagrees:** None. The IL-10R story is settled. The debate concerns what fraction of VEOIBD is monogenic -- estimates range from 10-30% depending on how stringently "very early onset" is defined.

**My assessment:** VEOIBD is the proof of concept that genetic diagnosis can directly determine therapy in IBD. Most adult IBD is polygenic, so the clinical impact is limited to a small pediatric population. But as gene discovery continues, more monogenic IBD subtypes will likely be identified.

---

## Claim 10: The pathogenesis of IBD is a multi-stage process -- no single factor is sufficient

**Author's claim:** "It seems increasingly likely that development of IBD is a multistage process with genetic, environmental, and microbial associations, revealing key insights into the pathogenesis of these diseases. These spheres offer promising tools for early diagnosis, monitoring course, and predicting the natural history of IBD."

**Evidence presented:** This is the chapter's synthetic conclusion, integrating all preceding evidence. None of the individual factors alone explains disease: NOD2 homozygosity increases risk but is not sufficient; germ-free mice with genetic defects don't develop colitis; smoking increases CD risk in Europeans but the association is absent in Asian cohorts; microbial dysbiosis is intermittent, not constant. The chapter argues that clinically meaningful subclassification will require integrating genetics, microbiome, and environmental data -- a multi-omics approach.

**Confidence:** HIGH. The multi-hit model is the consensus framework.

**What's at stake:** If IBD requires multiple hits, preventing any one hit could prevent disease -- smoking cessation, vitamin D supplementation, dietary modification, avoidance of unnecessary antibiotics in early life. For established disease, the model suggests that effective treatment may need to address multiple pathways simultaneously, analogous to combination chemotherapy in cancer.

**Who disagrees:** The multi-hit model is consensus. Debate focuses on whether the hits must occur in a specific sequence (e.g., barrier defect first, then microbial trigger) or can occur in any order.

**My assessment:** This conclusion is well-supported by the evidence presented but is also unfalsifiable at present -- it's a framework, not a testable hypothesis. The clinical value is in justifying a multi-modal treatment approach: diet (environment), biologics (immune), and potentially microbiome-modifying therapies, rather than monotherapy.

---

## Chapter 62 Overall Assessment

| Claim | Confidence | Most Vulnerable To |
|-------|-----------|-------------------|
| Claim 1: Loss of tolerance to commensals in susceptible host | VERY HIGH | Discovery of a specific autoantigen driving IBD |
| Claim 2: GWAS identifies 200+ loci, explains <15% heritability | VERY HIGH | Larger sequencing studies may increase explained variance |
| Claim 3: NOD2 = strongest CD gene, intracellular MDP sensor | VERY HIGH | None -- this is settled |
| Claim 4: Autophagy pathway (ATG16L1, IRGM) central to CD | HIGH | Human viral trigger for ATG16L1 remains unidentified |
| Claim 5: CD = Th1/Th17, UC = Th2-like (with heterogeneity) | MEDIUM-HIGH | UC Th2 model is increasingly questioned by single-cell data |
| Claim 6: Epithelial barrier dysfunction is genetic and primary | HIGH | Barrier defect may reflect subclinical inflammation in relatives |
| Claim 7: Dysbiosis with reduced F. prausnitzii, expanded Proteobacteria | HIGH | Causality vs consequentiality of dysbiosis still debated |
| Claim 8: Smoking divergent effect on CD vs UC | VERY HIGH (epidemiology), LOW (mechanism) | Mechanism unknown |
| Claim 9: VEOIBD is monogenic (IL-10R) | HIGH | Fraction of VEOIBD that is monogenic debated |
| Claim 10: Multi-stage, multi-hit model | HIGH | Unfalsifiable as currently formulated |

**Strongest section:** The genetics section (Claims 2-4). The integration of GWAS data, functional annotation, deep sequencing, and ancestry-specific effects is comprehensive and authoritative. The NOD2-ATG16L1-Paneth cell axis is the most mechanistically satisfying story in IBD biology.

**Weakest section:** The environmental triggers section (Claim 8 and surrounding). The smoking data is epidemiologically robust but mechanistically empty. The dietary evidence is acknowledged as limited by the difficulty of studying pre-illness diet. The vitamin D data is intriguing but associative. The chapter's handling of environment is thinner than genetics or immunology, reflecting the state of the field.

**Cross-reference opportunities:** This chapter should be read alongside Ch 63 (UC clinical) and Ch 64 (CD clinical) to connect pathogenesis to clinical presentation. The microbiome section connects to the notes in notes/microbiome/. The environmental/ dietary triggers connect to the nutrition notes from Gottschall, Pimentel, and dietary intervention sources. The Th1/Th17 immunology connects to the mechanistic rationale for biologic therapies (anti-TNF, anti-IL-12/23, anti-integrin) covered in treatment notes.
