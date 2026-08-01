---
tags:
  - source/guideline
  - oskg-ibd
  - clinical-guidelines
  - condition/sibo
  - diagnosis/breath-testing
  - methodology/breath-testing
  - society/rome-foundation
  - tier-3
  - source/report
  - type/reading-note
  - source/rome-sibo-2017
created: 2026-08-01
updated: 2026-08-01
confidence: high
source:
  title: "Intestinal Microbiota in Functional Bowel Disorders: A Rome Foundation Report"
  author: "Magnus Simrén, Giovanni Barbara, Harry J. Flint, Brennan M.R. Spiegel, Robin C. Spiller, Stephen Vanner, Elena F. Verdu, Peter J. Whorwell, Erwin G. Zoetendal"
  year: 2013
  journal: "Gut"
  volume: "62"
  pages: "159-176"
  doi: "10.1136/gutjnl-2012-302167"
  local_file: "sources/guidelines/G10_Rome_Foundation_SIBO_Report.txt"
guideline_type: working-team-report
grading_system: None (narrative review with expert clinical guidance)
related:
  - "[[ACG SIBO 2020 - Pimentel]]"
  - "[[AGA SIBO 2020 - Quigley]]"
  - "[[Rezaie Breath Test Consensus 2017]]"
  - "[[Pimentel 2022 - Low-Fermentation Eating]]"
---

# Rome Foundation Working Team Report: Intestinal Microbiota in Functional Bowel Disorders (Simrén et al., 2013)

A Rome Foundation Working Team Report published in *Gut* (2013). This is NOT a clinical practice guideline -- it is an academic synthesis and critical review commissioned by the Rome Foundation, the international authority on functional GI disorders (Rome I-IV diagnostic criteria for IBS, functional dyspepsia, etc.). The report predates both major SIBO guidelines (ACG and AGA, both 2020) by seven years and represents the functional GI perspective: SIBO is contextualized within the broader frame of gut microbiota-host interactions in functional bowel disorders, not treated as a standalone infectious/overgrowth condition. The report is markedly more skeptical of breath testing than later guidelines, devotes substantial space to microbiota characterization methodology, and emphasizes the gut-brain axis and visceral hypersensitivity as confounders in the SIBO-IBS debate.

**Critical context:** This report's nine-author working team includes leading functional GI researchers (Simrén, Barbara, Spiller, Whorwell) alongside microbial ecologists (Flint, Zoetendal). Eamonn Quigley -- lead author of the 2020 AGA SIBO Practice Update -- is acknowledged as a manuscript reviewer. The report's skeptical stance on breath testing and its emphasis on methodological limitations directly shaped the more cautious tone of the AGA 2020 document. Where the ACG 2020 guideline (Pimentel) is SIBO-forward and treatment-focused, this Rome report is mechanism-focused and methodology-conscious.

---

## The FGID Frame: Why This Report Reads Differently

### Claim 1: Functional bowel disorders are defined by symptoms in the absence of structural pathology; microbiota is one contributing factor among many -- not the sole explanation

**Author's claim:** "Functional gastrointestinal disorders (FGIDs) are defined by symptom-based diagnostic criteria that combine chronic or recurrent symptoms attributable to the GI tract in the absence of other pathologically-based disorders." The pathophysiological mechanisms are "incompletely known" and include "abnormal gastrointestinal motility, visceral hypersensitivity, altered brain-gut function, low-grade inflammation, psychosocial disturbance and intestinal microbes" -- microbiota is listed last among six contributing factors.

**Evidence presented:** The Rome III diagnostic criteria (Drossman 2006). The report emphasizes that FGIDs affect 10-20% of the population and are associated with poor health-related quality of life and substantial societal costs.

**Comparison against ACG/AGA:** The ACG 2020 guideline treats SIBO as a distinct clinical entity with specific diagnostic criteria, symptoms, and treatments. The AGA 2020 Practice Update is closer in spirit to this Rome report but still SIBO-centric in structure. This report's frame is fundamentally different: microbiota alterations are one element of FGID pathophysiology, and SIBO is one subset of microbiota alterations. The Rome frame prevents the reification of SIBO as *the* explanation for functional symptoms.

**My assessment:** This framing is methodologically more honest than the SIBO-first approach of the ACG guideline, but it is also less clinically actionable. A clinician with a bloating patient needs to decide whether to test for SIBO and whether to treat -- the Rome report's answer ("the evidence is unclear, the tests are unvalidated") is accurate but incomplete. This is the fundamental tension between academic functional GI medicine and clinical gastroenterology that runs through all three documents.

---

## Microbiota Fundamentals: The State of Knowledge in 2013

### Claim 2: The normal gut microbiota is vastly complex, mostly uncultured, and influenced by diet, transit, host genetics, and immune factors -- yet our understanding of the *small intestinal* microbiota specifically is in its infancy

**Author's claim:** "Most of the microbial diversity in the human GI tract is not currently represented by available cultured species." The small intestinal microbiota is particularly poorly characterized: "Culture-independent studies of the small intestinal microbiota are in their infancy."

**Evidence presented:** 
- The human gut contains ~10^14 microbial cells, outnumbering human cells 10:1, with a gradient from 10^1-10^3 bacteria/g in stomach/duodenum to 10^11-10^12 cells/g in colon
- Three phyla predominate in the colon: Firmicutes, Bacteroidetes, Actinobacteria; over 50 bacterial phyla described, of which 10 inhabit the colon
- The concept of three "enterotypes" (Arumugam et al. 2011) is discussed as a novel finding -- these clusters "do not vary by patient characteristics, such as nation, gender, age or body mass index"
- Diet profoundly shapes microbiota: African rural children on polysaccharide-rich diets vs. Italian city children on high-fat/high-protein diets show dramatic differences (De Filippo et al. 2010)
- FODMAPs as substrates for bacterial metabolism are mentioned but had "not yet been studied" for their microbiota-altering effects in 2013
- Transit speed directly affects microbiota: senna accelerates transit, increases SCFA production, reduces methanogens; loperamide does the opposite
- SCFAs (particularly propionate and butyrate) stimulate motility, "ensuring bacteria are propelled from the ileum to the colon" -- a bidirectional feedback loop between microbiota and host physiology

**Confidence:** HIGH for colonic microbiota characterization; LOW for small intestinal microbiota. The report is transparent about the knowledge gap in small bowel microbiology -- a gap that remains substantially unfilled in 2024.

**What's at stake:** If we don't know what "normal" small intestinal microbiota looks like -- in composition, quantity, and variability -- then "small intestinal bacterial overgrowth" is a diagnosis without a validated baseline. This is the single most important methodological criticism the Rome report levels, and it echoes through both the AGA 2020 and the ACG 2020 documents.

**My assessment:** Reading this in 2024, the 2013 state of knowledge is striking. The REIMAGINE study (Leite et al. 2019, cited in the 2020 guidelines) represents the progress the Rome report called for, but large-scale validation of small bowel microbiota norms is still pending. This claim holds up extremely well over time.

---

## Methodological Approaches: The Critical Toolkit

### Claim 3: Culture-independent molecular techniques (16S rRNA sequencing, metagenomics, metabolomics) represent a major advance over traditional culture, but each method has specific biases and limitations

**Author's claim:** "The arrival of new high-throughput sequencing approaches and 16S rRNA-based microarraying has further accelerated the supply of data... Although culturing may bias against bacteria that are hard to grow in the laboratory, PCR amplification biases against certain groups of gut bacteria."

**Evidence presented:** Table 1 provides a comprehensive comparison of detection methods:
- Cultivation: accurate species identification, but not representative (most gut bacteria unculturable)
- 16S rRNA cloning/Sanger sequencing: complete gene sequences, but cloning bias
- High-throughput sequencing: massive data generation, but short reads
- Fingerprinting (DGGE, TGGE): fast community comparison, but no direct phylogenetic link
- FISH: accurate cell enumeration, but dependent on 16S rRNA database quality
- qPCR: wide dynamic range, but database-dependent
- Phylogenetic microarrays: high-throughput profiling, but database-dependent
- Metagenomics (sequence-based): high-throughput gene discovery, but function mainly predicted
- Metagenomics (function-based): functional properties linked to DNA, but cloning host limitations
- Metatranscriptomics: direct information about microbial activity, but RNA extraction challenging
- Metaproteomics: direct activity information, but no uniform protocol
- Metabonomics/metabolomics: microbiota activity representation, but no direct link to specific microbes

**Box 1 (Key Messages):** "Breath tests are not validated to accurately detect small intestinal bacterial overgrowth." "Rapid molecular approaches have largely replaced cultural approaches for enumeration of the dominant GI tract microbiota."

**Comparison against ACG/AGA:** Neither the ACG nor AGA 2020 guidelines discuss microbiota characterization methodology in any detail. The Rome report's methodological depth reflects its academic audience and its goal of guiding future research rather than immediate clinical decision-making.

**My assessment:** This section is invaluable for understanding *why* the breath testing debate exists. The report's key methodological insight: breath testing sits at the bottom of the methodological hierarchy -- it measures gas production (an indirect metabolic readout) rather than identifying or enumerating microbes. Every method above it on the hierarchy (culture, 16S sequencing, metagenomics) is more direct but also more invasive, expensive, or technically demanding. The clinical challenge is that the least valid test (breath testing) is the most practical.

---

## SIBO and IBS: The Central Controversy

### Claim 4: The SIBO-IBS link is controversial because breath tests -- the basis for most positive studies -- have not been validated against an accepted gold standard

**Author's claim:** "The role of SIBO in the pathogenesis of IBS is very controversial because the breath tests employed to establish this role have not been validated. Even the validity of the 'gold standard', jejunal cultures >10^5 cfu/ml with colonic-type bacteria, has been challenged, largely because this cut-off was established from samples following surgical diversion." 

"The relevance of SIBO in IBS remains unclear due to methodological problems, influence of confounding factors and large differences between studies." (Box 2)

**Evidence presented (Table 2 -- 10 small bowel culture studies, 1969-2012):**
- Drasar & Shiner (1969): 13 diarrhea patients, jejunal capsule -- "no difference from controls"
- Posserud et al. (2007): 162 IBS vs 42 controls, jejunal aspirate -- 4% of IBS >10^5 CFU/mL (same as controls). But subanalysis using >5x10^3: 43% IBS vs 12% controls
- Kerckhoffs et al. (2009): 8 IBS, 9 controls -- "no different number diagnosed with SIBO using multiple definitions"
- Choung et al. (2011): 148 IBS, duodenal aspirate -- 2% IBS >10^5 CFU/mL vs 10% in patients with other indications
- Pyleris et al. (2012): 85 IBS, 150 non-IBS -- 37% IBS >10^3 CFU/mL vs 15.11% non-IBS (all investigated for UGI bleed)
- The glucose breath test has "poor sensitivity; misses distal SIBO" (Table 1)
- The lactulose breath test "may simply measure small intestinal transit time to caecum" (Table 1)

**The key physiological critique (Figure 3):** In a combined lactulose H2 breath test with Tc-99 scintigraphy, "Tc99 had already reached the caecum in large quantities before the H2 PPM level has reached the threshold for an abnormal test. This demonstrates that the increased H2 production results from fermentation by colonic bacteria, not by abnormal bacteria in the small intestine." In other words, the early hydrogen peak on lactulose breath testing -- used to diagnose SIBO -- is often just rapid transit to the colon, not small bowel bacterial overgrowth.

**Confounding factors identified:**
- PPI use: "Some studies suggest that PPI use might lead to symptomatic SIBO... but this depends on the tests employed and criteria applied"
- Altered motility
- Antibiotics, probiotics, prebiotics
- Dietary items such as FODMAPs
- All of these "could also influence microbiota in IBS patients and result in a potentially spurious association"

**Comparison against ACG/AGA:** This is the single area of greatest divergence from the ACG 2020 guideline. The ACG guideline recommends breath testing for SIBO diagnosis (conditional, very low evidence). The Rome report essentially says: breath tests are unvalidated, the gold standard (jejunal culture) is itself problematic, and the studies linking SIBO to IBS are confounded by transit time, PPIs, and diet. The AGA 2020 Practice Update occupies a middle position -- more skeptical than ACG, less skeptical than Rome. The Tc-99 scintigraphy data (Figure 3) showing that early H2 peaks reflect colonic fermentation is the most damning single piece of evidence against lactulose breath testing, and it is not prominently discussed in the ACG guideline.

**My assessment:** This is the most intellectually rigorous critique of SIBO breath testing in the literature prior to the 2020 guidelines. The Posserud study (43% IBS vs 12% controls using >5x10^3 CFU/mL threshold, but only 4% using >10^5) prefigures the 10^3 threshold debate that would be resolved by the North American Consensus in 2017. The report's skepticism has aged well: seven years later, both the ACG and AGA guidelines still rate breath testing recommendations as "very low quality of evidence." The methodological concerns raised here have not been resolved -- they have been acknowledged and worked around.

### Claim 5: Post-infectious IBS provides the strongest evidence for a causal role of microbiota in FGIDs -- but the mechanism involves immune activation and altered gut physiology, not simply bacterial overgrowth

**Author's claim:** "The most convincing evidence to date is the finding that functional dyspepsia and irritable bowel syndrome may develop in predisposed individuals following a bout of infectious gastroenteritis."

**Evidence presented:**
- Incidence of infective gastroenteritis: 19/100 person-years in the UK
- Bacterial causes: Campylobacter (10%), Salmonella (3%); viral (Norovirus/Rotavirus) account for ~1/3
- Onset of new IBS after gastroenteritis: 6-17% of IBS patients report this; an internet survey found 18%, with ~40% beginning while travelling
- Clinical features of PI-IBS: predominantly IBS-D
- Meta-analysis (18 studies): relative risk of developing IBS 1 year after bacterial gastroenteritis (mostly Shigella, Campylobacter, Salmonella): RR=6.5 (CI 2.6-15.4), an effect still apparent at 36 months: RR=3.9 (3.0-5.0)
- Viral gastroenteritis shows reduced PI-IBS incidence compared to bacterial -- "in keeping with the lesser tissue injury"
- Strongest risk factors: bacterial toxicity, prolonged diarrhea duration, rectal bleeding, fever
- Pathophysiology: acute enteritis associated with "prolonged increase in mucosal cytotoxic T lymphocytes and increase in enteroendocrine cells," increased 5HT-containing cells in IBS-D, visceral hypersensitivity
- Microbiota consequences of acute gastroenteritis: depletion of anaerobes (Bacteroides, Bifidobacterium, Lactobacillus, Eubacterium), alkalinization of stool pH, fall in SCFAs, 10^9 CFU/g of pathogens
- Antibiotics during acute gastroenteritis INCREASE risk of persistent symptoms: children post-Salmonella -- 9.5% on antibiotics reported vomiting/abdominal pain/diarrhea at 3 months vs 2.9% without antibiotics

**Mechanism proposed:** Gut infection → depletion of commensal anaerobes → reduced SCFA production → impaired colonic salt/water absorption → diarrhea phenotype. PLUS: immune activation (mast cells, T cells) → visceral hypersensitivity via histamine and tryptase release → pain. These "effects on gut physiology will impact on the gut microbiota environment" -- a bidirectional disruption.

**Comparison against ACG/AGA:** The ACG 2020 guideline does not discuss PI-IBS in any detail. The AGA 2020 guideline mentions post-infectious IBS in passing but does not develop it. This represents a genuine gap in the SIBO-focused guidelines: the strongest evidence for a microbiota role in IBS comes from post-infectious IBS, not from SIBO, yet the SIBO paradigm has displaced PI-IBS as the dominant microbiota-IBS narrative.

**My assessment:** This section is the report's strongest contribution. It provides a coherent alternative to the SIBO hypothesis: microbiota alterations in IBS are real, but they represent a complex dysbiosis involving immune activation, barrier dysfunction, and altered gut physiology -- not simply an overgrowth of bacteria in the wrong location. The finding that antibiotics during acute infection INCREASE the risk of persistent symptoms (9.5% vs 2.9%) is a powerful caution against the reflexive use of antibiotics for post-infectious gut symptoms, and it complicates the narrative that antibiotics are the logical treatment for microbiota-driven IBS.

### Claim 6: Faecal microbiota in IBS shows quantitative and qualitative alterations, but results are inconsistent across studies due to methodological heterogeneity, unstable microbiomes, and failure to link sampling to fluctuating symptoms

**Author's claim:** "Results from 16S rRNA-based microbiota profiling approaches demonstrate both quantitative and qualitative changes of mucosal and faecal gut microbiota, particularly in IBS." But "results to date are inconsistent and sometimes contradictory."

**Evidence presented (Table 3 -- 20 studies, 2002-2012):**
- Culture studies: decreased lactobacilli and bifidobacteria, increased facultative bacteria (Streptococcus, E. coli), higher anaerobes (Clostridium)
- Molecular studies: Proteobacteria and specific Firmicutes increased in multiple studies; other Firmicutes, Bacteroidetes, and bifidobacteria decreased
- Rajilic-Stojanovic et al. (2011): faecal microbiota of IBS patients could be grouped in a cluster "completely different from that of healthy controls"
- Jeffery et al. (2012): clustering of IBS patients into "normal-like" vs "abnormal" microbiota composition (increased Firmicutes:Bacteroidetes ratio), with association with symptom profile
- Multiple studies found decreased temporal stability in IBS faecal microbiomes vs controls
- Carroll et al. (2010): diminished microbial biodiversity in IBS-D faecal samples
- Parkes et al. (2012): expansion of mucosa-associated microbiota (mainly Bacteroides and Clostridia), with association with IBS subgroups and symptoms

**Reasons for inconsistency identified:**
- Different molecular techniques employed across studies
- "The use of single samples that are not linked to fluctuating symptoms (especially as studies suggest IBS faecal microbiomes are less stable)"
- Diet not controlled
- Phenotypic characterization of patients varies
- "Faecal samples do not necessarily reflect other parts of the GI tract"

**Comparison against ACG/AGA:** Neither 2020 guideline discusses faecal microbiota alterations in IBS in detail. The ACG guideline focuses on SIBO diagnosis and treatment. The AGA guideline focuses on the definitional and diagnostic challenges. The Rome report is unique in devoting substantial attention to the broader dysbiosis picture beyond SIBO.

**My assessment:** The inconsistency across studies is real and remains a problem in 2024. The key methodological insight -- that single-point faecal sampling in a condition with unstable microbiota and fluctuating symptoms is inherently limited -- is important and underappreciated in the clinical literature. The studies that cluster IBS patients into distinct microbiota profiles (Rajilic-Stojanovic, Jeffery) suggest that the heterogeneity is not just noise -- there may be genuine IBS subgroups with different microbiota signatures -- but larger longitudinal studies with symptom-linked sampling are needed.

### Claim 7: Host-microbial interactions in IBS involve immune activation, barrier dysfunction, and visceral hypersensitivity -- not simply gas production

**Author's claim:** "The current working hypothesis is that abnormal microbiota activate mucosal innate immune responses which increase epithelial permeability, activate nociceptive sensory pathways and dysregulate the enteric nervous system."

**Evidence presented:**
- Increased colonic mucosal expression of Toll-like receptor-4 (TLR4, recognizes bacterial lipopolysaccharides) in IBS (Brint et al. 2011)
- Increased titres of circulating anti-flagellin antibodies in IBS (Schoepfer et al. 2008) -- evidence of systemic immune response to luminal microbial antigens
- Low-grade activation of innate and adaptive mucosal immune response: increased activated mast cells, CD3+, CD4+, CD8+ T cells in both PI-IBS and non-specific IBS
- Mast cells located "in closer vicinity to mucosal innervation" and correlated with "severity and frequency of abdominal pain" (Barbara et al. 2004)
- Histamine and tryptase released from IBS mucosal biopsies evoked increased mesenteric sensory afferent activation and induced visceral hypersensitivity via histamine-1 and PAR-2 receptors when applied to recipient rats (Barbara et al. 2007, Cenac et al. 2007)
- Increased epithelial permeability in subgroups of IBS patients "could expose the immune system to an abnormal microbial antigenic load"
- Animal models: probiotics and their secreted products modulate intestinal smooth muscle contractility and visceral sensitivity
- Bidirectional brain-gut axis: stress induces shifts in bacterial composition accompanied by systemic cytokine response and increased permeability; microbiota can affect brain chemistry and behavior in animal models

**Comparison against ACG/AGA:** The ACG 2020 guideline is almost entirely focused on gas production as the mechanism of SIBO symptoms. The AGA 2020 document mentions immune activation briefly but does not develop it. The Rome report's detailed discussion of mast cells, barrier function, TLR4, and anti-flagellin antibodies represents a fundamentally different pathophysiological model -- one where symptoms are driven by host immune and neural responses to microbial signals, not by the physical distension of gas.

**My assessment:** This is the strongest section of the report and the one that most clearly distinguishes the Rome/functional GI perspective from the SIBO/infectious disease perspective. In the ACG model, the problem is bacterial fermentation → gas → bloating/distension. In the Rome model, the problem is microbial signals → immune activation → mast cell degranulation → visceral hypersensitivity → pain and altered motility. These are not mutually exclusive, but they lead to different treatment implications: the ACG model suggests antibiotics (kill the bacteria, stop the gas); the Rome model suggests immunomodulation, barrier repair, and neuromodulation may be equally or more important. The fact that rifaximin improves symptoms even in patients WITHOUT evidence of SIBO (discussed in the treatment section below) supports the Rome model.

---

## Overlap Syndromes: IBS, Celiac Disease, IBD, and Diverticulitis

### Claim 8: IBS symptoms can overlap with organic GI diseases (celiac disease, IBD, diverticulitis); microbiota may be a common factor linking functional and organic disorders

**Author's claim:** "It is possible that IBS and IBD coexist with a higher than expected frequency, or may exist on a continuum, with IBS and IBD at different ends of the inflammatory spectrum."

**Evidence presented:**
- Non-celiac gluten sensitivity: some IBS patients lack celiac antibodies and histology yet respond to gluten-free diet (Verdu et al. 2009, Biesiekierski et al. 2011, Carroccio et al. 2012)
- Mouse models: gluten induces innate immune activation, increased small intestinal permeability, neuromuscular dysfunction, and dysbiosis in the absence of autoimmunity
- IBS-like symptoms in IBD: common in patients in long-standing remission, or reported before IBD diagnosis
- A study of IBD patients in "clinical remission" with IBS symptoms found high calprotectin levels -- "suggesting that in most cases IBS symptoms are the result of undetected ongoing inflammation" (Keohane et al. 2010)
- Both IBS and IBD show faecal and mucosal-associated dysbiosis -- "it is tempting to raise the hypothesis that the intestinal microbiota may be a common factor in both diseases"
- Post-diverticulitis: high proportion of patients have persistent IBS-like symptoms despite absence of complications

**My assessment:** This section is clinically important but underdeveloped. The IBS-IBD overlap is extensively documented in the 2020s literature but was only beginning to be recognized in 2013. The report's hypothesis that microbiota is a common thread is prescient. The practical takeaway -- that IBS symptoms in IBD patients often reflect ongoing subclinical inflammation rather than a separate functional disorder -- has been confirmed by subsequent research.

---

## Treatment: Antibiotics, Probiotics, Prebiotics, Diet

### Claim 9: Rifaximin shows modest efficacy in IBS (NNT=11, therapeutic gain ~10% over placebo), but antibiotic resistance concerns and the self-limited nature of benefit warrant restricted use

**Author's claim:** "A short course of gut-specific antibiotics may have utility in some patients with IBS but we need to know more about predictors of treatment responsiveness, antibiotic resistance, the efficacy and safety of re-treatment schedules as well as the optimal dosing regimen."

**Evidence presented:**
- Three fully-published double-blind placebo-controlled trials of rifaximin in FBD (Sharara et al. 2006, Pimentel et al. 2008, Pimentel et al. 2011 -- TARGET 1 and 2 were not yet published at the time of this report)
- Symptom improvement, especially bloating and flatulence, for "approximately 10 weeks following treatment"
- "Therapeutic advantage over placebo around 10%"
- Doses: 600-2400 mg daily for 7-14 days across studies
- NNT for rifaximin 550 mg TID for 2 weeks: 11, compared with "4 for 'placebo without deception,' 7 for alosetron, 8 for linaclotide, and 14 for tegaserod"
- Concerns: antibiotic resistance (rifampin-resistant staphylococci documented), possible C. difficile infection (not yet a problem in published data)
- Neomycin was the original antibiotic choice but interest has shifted to rifaximin
- Mechanism: "amelioration of gas-related symptoms in patients occurred also in patients with no evidence of SIBO" (citing Sharara et al. 2006) -- this is a crucial point suggesting rifaximin's benefit may not require SIBO

**Comparison against ACG/AGA:** The ACG 2020 guideline reports 70.8% pooled rifaximin efficacy (Gatta & Scarpignato 2017 meta-analysis) with detailed antibiotic tables and efficacy percentages. The Rome report reports rifaximin data from only 3 trials with ~10% therapeutic gain. The difference reflects the 7-year gap and the maturation of the rifaximin evidence base (TARGET 1/2/3 were published 2011-2015). The Rome report's NNT of 11 for rifaximin -- lower efficacy than alosetron (NNT=7), linaclotide (NNT=8), and even placebo-without-deception (NNT=4) -- provides a sobering efficacy benchmark that the later ACG guideline's 70.8% pooled rate obscures.

**My assessment:** The Rome report's antibiotic section is notably restrained compared to the ACG 2020 guideline. It emphasizes the limitations rather than the opportunities. The observation that rifaximin benefits even non-SIBO patients (Sharara 2006) is the key mechanistic insight: if antibiotics work in patients without SIBO, then either (a) SIBO was present but undetected, or (b) rifaximin has effects beyond bacterial eradication (e.g., anti-inflammatory, modulation of colonic microbiota). The Rome report leans toward (b), consistent with its broader microbiota-immune-neural model rather than a narrow SIBO model.

### Claim 10: Probiotics have a modest but real evidence base in IBS, particularly Bifidobacterium infantis 35624; but trial quality is variable and publication bias is evident

**Author's claim:** "The majority of trials of probiotics in IBS show some degree of efficacy although some of the early studies were of very poor quality." "A recent systematic review reported that studies of poorer quality tended to show larger effects and published data indicate a publication bias, with non-reporting of negative effects in small trials."

**Evidence presented (Table 4 -- 25+ placebo-controlled trials):**
- ~75% of published trials were positive
- Bifidobacterium infantis 35624: positive in two trials (O'Mahony et al. 2005, Whorwell et al. 2006) -- the largest and best-designed studies
- Bifidobacterium lactis DN-173010: positive for digestive discomfort (Guyonnet et al. 2007) and for maximum distension/pain (Agrawal et al. 2009)
- Lactobacillus plantarum 299V: positive for flatulence (Nobaek et al. 2000) and pain (Niedzielin et al. 2001), but negative in a third study (Sen et al. 2002)
- Probiotic mixtures (VSL#3, Medilac DS, multiple 4-strain combinations): generally positive for bloating, flatulence, and global scores
- Several large, high-quality trials were NEGATIVE: Drouault-Holowacz et al. (2008), Simrén et al. (2010), Sondergaard et al. (2011)
- Only one study reported symptom deterioration (Ligaarden et al. 2010 -- L. plantarum MF1298)

**Key clinical guidance from the report:**
- "The strongest evidence is for Bifidobacterium infantis 35624 at a dose of 1x10^8 cfu/day taken for at least 4 weeks"
- Probiotics "should be tried, for a period of at least 1 month, at adequate doses before a judgement is made about the response to treatment" (Box 4)
- Patients should be warned that some probiotics may aggravate symptoms (citing Ligaarden 2010)

**Unresolved questions listed (15 specific unknowns):**
- Single organisms vs mixtures?
- Do mixtures contain competitive/antagonistic strains?
- Can probiotic foods and drinks be administered simultaneously?
- Optimal delivery systems, dosing regimens, duration?
- Frequency of host colonization?
- Which patient subgroups benefit from which organisms?
- Safety in immunocompromised populations?
- Mechanisms behind symptom improvement?

**Comparison against ACG/AGA:** The ACG 2020 guideline's Key Concept 12 states "there is a lack of consistent data to support recommending specific probiotics in the treatment of SIBO" -- and discusses probiotics largely as a risk (may cause SIBO/D-lactic acidosis). The Rome report is far more favorable: it recommends probiotics as a first-line trial for IBS, provides specific organism and dosing recommendations, and devotes an entire table to probiotic trial results. This is the starkest divergence between the functional GI perspective (probiotics are plausible and supported) and the SIBO-focused perspective (probiotics are unproven and potentially harmful). The AGA 2020 occupies a middle position.

**My assessment:** The Rome report's favorable probiotic stance reflects the composition of its working team (Whorwell and Barbara had conducted probiotic trials) and the functional GI tradition of using probiotics for IBS. The ACG guideline's probiotic skepticism reflects Pimentel's SIBO-focused paradigm where adding more bacteria to an overgrowth condition is counterintuitive. Both positions are defensible. The Rome report's detailed list of 15 unresolved questions about probiotics is still largely unanswered in 2024, which is remarkable given the explosive growth of the probiotic market.

### Claim 11: Prebiotics and synbiotics have theoretical appeal but essentially no reliable clinical trial data in IBS; dietary FODMAP reduction is promising but evidence is from a single research group

**Author's claim:** "Prebiotics and synbiotics should theoretically have the potential in treating functional gastrointestinal disorders but there are as yet no reliable data to support this view."

**Evidence presented:**
- Only ONE double-blind placebo-controlled trial of a prebiotic in IBS: a trans-galactooligosaccharide mixture that reduced symptoms and stimulated bifidobacteria (Silk et al. 2009) -- "clearly more research is required"
- Inulin and lactulose (prebiotics) increase flatulence, "making it unlikely they will help IBS patients"
- Synbiotic studies exist but "their design is not sufficiently robust to draw any firm conclusions"
- FODMAP reduction: "Reducing intake of fibre or FODMAPs is one of the simplest and safest ways of altering gut microbiota, which can lead to improvement in bloating and diarrhoea, an effect which may last for years." But "the evidence to support widespread use of FODMAP reduction in patients with IBS is limited and comes mainly from one research group" (the Monash group, Shepherd and Gibson)
- Bran aggravated symptoms in one RCT (Snook & Shepherd 1994); "excluding bran should help, and many patients believe this is true"
- Systematic exclusion diets "may also help but are laborious; targeted exclusion of regularly consumed suspects, such as dairy, wheat, fruit and vegetables, may be more practical"

**Comparison against ACG/AGA:** The ACG 2020 guideline acknowledges low FODMAP diets but finds "very low quality evidence" and does not make a formal dietary recommendation. The AGA 2020 guideline does not address diet in detail. The Rome report -- published 7 years earlier -- is actually more favorable toward dietary FODMAP reduction than the later guidelines, despite noting the evidence is from one research group. This reflects the Rome Foundation's comfort with dietary approaches (central to functional GI management) versus the pharmaceutical-intervention orientation of the US gastroenterology societies.

**My assessment:** The Rome report's cautious endorsement of FODMAP reduction has been vindicated by subsequent research. By 2024, low FODMAP diet is a first-line dietary intervention for IBS with multiple RCTs from independent groups. The report's 2013 warning about evidence coming from one research group was appropriate caution that stimulated the independent replication that followed.

---

## Clinical Guidance: Box 4 Recommendations

### Claim 12: The report provides seven general clinical recommendations that prioritize dietary evaluation, probiotic trials, and cautious antibiotic use -- with explicit acknowledgment that SIBO testing remains an "area of uncertainty"

**Box 4: Diagnostic and Therapeutic General Recommendations:**

1. "There is currently no clinically useful way of identifying whether the microbiota are disturbed in particular patients with IBS."
2. "Dietary evaluation and exclusion of possible sources of unabsorbable carbohydrates including FODMAPs and excessive fibre could be beneficial in select patients."
3. "Probiotics have a reasonable evidence base and should be tried, for a period of at least 1 month, at adequate doses before a judgement is made about the response to treatment."
4. "The utility of testing for SIBO in the setting of IBS remains an area of uncertainty."
5. "If SIBO is strongly suspected based on clinical presentation and testing is being considered, using stringent criteria for the glucose breath test or jejunal aspirate appear to be the best tests."
6. "Consideration should be given to discontinuing PPIs in those with SIBO."
7. "There is emerging evidence that non-absorbable antibiotics may have the potential to reduce symptoms in some patients with IBS."

**Additional clinical guidance from the text:**
- Rifaximin use "should be restricted to difficult cases since its widespread use could promote resistance"
- PPI discontinuation in selected IBS patients on PPIs "for unclear reasons, especially if their symptoms started with PPI therapy"
- Probiotics: B. infantis 35624, 1x10^8 CFU/day, at least 4 weeks is the best-evidenced specific recommendation
- Fiber: excluding bran may help; excessive fiber may aggravate symptoms

**Comparison against ACG/AGA:** This is where the fundamental difference in purpose becomes clearest. The ACG 2020 guideline provides 6 GRADE-rated recommendations with specific diagnostic thresholds and antibiotic dosing. The AGA 2020 provides 9 Best Practice Advice statements. The Rome report provides 7 "general recommendations" in a box -- deliberately framed as clinical guidance, not as guideline recommendations. The hierarchy is: Rome says "we don't know, but here's what seems reasonable"; AGA says "here's what experts advise, but the evidence is limited"; ACG says "here's what we recommend, conditional on very low evidence."

**Key differences in specific guidance:**
- **SIBO testing:** Rome says "area of uncertainty" -- glucose breath test or jejunal aspirate if testing is pursued. ACG says "we suggest breath testing" (conditional, very low evidence). AGA says breath tests "lack sensitivity and specificity."
- **Probiotics:** Rome says "should be tried" (strongest endorsement of the three). ACG says "lack of consistent data" (most skeptical). AGA says nothing specific.
- **Diet:** Rome provides the most specific dietary guidance (FODMAPs, fiber, exclusion diets). ACG is noncommittal. AGA does not address diet.
- **PPIs:** Rome and AGA both recommend considering PPI discontinuation in SIBO. ACG recommends against testing asymptomatic PPI users (different emphasis -- both acknowledge the PPI-SIBO association but draw different clinical conclusions).
- **Antibiotic scope:** Rome restricts rifaximin to "difficult cases." ACG recommends antibiotics as first-line SIBO treatment. AGA says "empiric" and "limited database."

**My assessment:** The Rome report's clinical guidance has aged remarkably well. Its cautious approach -- try diet first, then probiotics, reserve antibiotics for difficult cases, don't over-rely on breath testing -- is arguably closer to how most thoughtful clinicians actually manage suspected SIBO/IBS in 2024 than either the ACG guideline's antibiotic-forward approach or the AGA's diagnostic nihilism. The fact that this 2013 report's recommendations align with the evolved clinical consensus of 2024 suggests the Rome Foundation's functional GI perspective provides durable clinical wisdom even when the evidence base is thin.

---

## Future Research Recommendations

### Claim 13: The report identifies specific methodological and conceptual barriers to progress and outlines a research agenda that anticipates much of what followed in the subsequent decade

**Key research priorities identified:**

1. **Validation:** "The SIBO hypothesis in IBS remains a matter of debate because the breath tests and the small bowel culture techniques have not been validated." → Partially addressed by Rezaie North American Consensus (2017), but full validation remains incomplete.

2. **Confounding control:** Studies must account for "antibiotics or PPIs" and other confounders not addressed in existing literature. → Still a challenge in 2024.

3. **Sample size and heterogeneity:** "Larger sample size studies are of key importance" given the wide inter-individual variability of microbiota profiles. → Addressed by large microbiome consortia but still underpowered for IBS subgroup analyses.

4. **Symptom-linked sampling:** "Assessment of correlations between microbiota changes with patient's symptoms" with longitudinal sampling during remission, flares, stress, and post-intervention. → The most important methodological recommendation. Still rarely done in 2024.

5. **Site-specific characterization:** "Future work should better characterize microbial populations at the luminal and mucosal level which may differ substantially from faecal microbiota." → Addressed by REIMAGINE (Leite 2019) but large-scale small bowel mucosal microbiome characterization remains a frontier.

6. **Mechanistic studies:** Moving "beyond descriptive to mechanistic." The immune activation hypothesis "should now be substantiated by mechanistic and interventional studies." → Progress made (mast cell, barrier function, TLR studies) but causal pathways remain incompletely defined.

7. **Brain-gut-microbiota axis:** Bidirectional signaling demonstrated in rodents -- "need to be further explored to open new avenues of research in FBD." → Explosion of research in this area since 2013, validating this recommendation.

8. **Treatment predictors:** "We need to know more about predictors of treatment responsiveness" for antibiotics, probiotics, and dietary interventions. → Still largely unknown in 2024.

9. **Fecal transplantation:** Mentioned as an emerging concept for IBS -- "further research is needed." → Subsequent small RCTs have shown mixed results; remains experimental.

**My assessment:** This research agenda is remarkably prescient. Nearly every priority identified in 2013 has become a active research area by 2024, and most remain incompletely addressed. The report's call for longitudinal, symptom-linked sampling with mechanistic endpoints -- rather than single-timepoint association studies -- remains the single most important unmet need in the field.

---

## Report Assessment

| Claim | Summary | Confidence | Most Vulnerable To |
|-------|---------|-----------|-------------------|
| Claim 1 | FGIDs have multiple pathophysiological mechanisms; microbiota is one of six | HIGH | Reductionist models that attribute all IBS to SIBO |
| Claim 2 | Normal small intestinal microbiota is poorly characterized | HIGH | New large-scale small bowel microbiome characterization studies |
| Claim 3 | Molecular methods advance the field but each has limitations | HIGH | Technological developments rendering this taxonomy obsolete |
| Claim 4 | Breath tests are unvalidated; the SIBO-IBS link is controversial | HIGH | Consensus validation studies (partially addressed by 2017 North American Consensus) |
| Claim 5 | PI-IBS provides strongest evidence for microbiota-IBS link | HIGH | Alternative explanations for PI-IBS (persistent immune activation independent of microbiota) |
| Claim 6 | Faecal microbiota alterations in IBS are real but inconsistently reported | MEDIUM-HIGH | Larger, better-controlled studies failing to find consistent signals |
| Claim 7 | Host-microbial immune-neural interactions drive IBS symptoms | MEDIUM | Failure to demonstrate causality in human interventional studies |
| Claim 8 | IBS overlaps with organic GI diseases via shared microbiota mechanisms | LOW-MEDIUM | Calprotectin explaining IBS symptoms in IBD independently of microbiota |
| Claim 9 | Rifaximin has modest efficacy; antibiotic resistance is a concern | HIGH | Long-term safety data (still pending for repeated rifaximin courses) |
| Claim 10 | Probiotics have modest but real efficacy; B. infantis 35624 is best-evidenced | MEDIUM | Large high-quality negative trials (already some exist -- Simrén 2010, Sondergaard 2011) |
| Claim 11 | Prebiotics/synbiotics unproven; FODMAP reduction promising but evidence from one group | MEDIUM-HIGH (validated by subsequent research) | Independent replication of FODMAP trials (accomplished since 2013) |
| Claim 12 | Clinical guidance in Box 4: diet → probiotics → cautious antibiotics | MEDIUM | Evidence-based guideline development (ACG/AGA 2020 partially addressed this) |
| Claim 13 | Research agenda identifies key barriers and priorities | HIGH | None -- the agenda has held up well |

**Strongest sections:**
1. **The breath testing critique (Claim 4, Figure 3):** The Tc-99 scintigraphy data showing lactulose H2 peaks reflect colonic fermentation is the most definitive single piece of evidence in the SIBO literature against lactulose breath testing.
2. **Post-infectious IBS (Claim 5):** The most comprehensive treatment of PI-IBS in any of the major SIBO/functional GI documents, providing a coherent alternative to the SIBO hypothesis.
3. **Host-microbial immune-neural interactions (Claim 7):** The mast cell, barrier function, and visceral hypersensitivity data is the strongest articulation of the functional GI perspective on microbiota-driven symptoms.
4. **The research agenda (Claim 13):** Prescient identification of priorities that have driven the field for the subsequent decade.

**Weakest sections:**
1. **Overlap syndromes (Claim 8):** Underdeveloped. The IBS-IBD-celiac overlap is clinically important but the report only gestures at it.
2. **Antibiotic section (Claim 9):** Based on only 3 rifaximin trials (pre-TARGET 1/2/3). The evidence base has matured substantially since 2013, making this section dated.
3. **Dietary guidance:** FODMAP evidence characterized as "from one research group" -- the report could not anticipate the explosion of independent FODMAP research that followed.

**Key divergences from ACG SIBO 2020 (G3):**
1. **Breath testing:** Rome says "not validated"; ACG says "we suggest breath testing" (conditional, very low evidence). Fundamental disagreement on whether an unvalidated test should be recommended.
2. **Probiotics:** Rome says "should be tried" with specific organism/dose recommendation; ACG says "lack of consistent data" and warns of potential harm. Nearly opposite recommendations.
3. **Antibiotic scope:** Rome restricts to "difficult cases"; ACG recommends as first-line treatment. Different risk-benefit calculus.
4. **Pathophysiology:** Rome emphasizes immune-neural interactions and visceral hypersensitivity; ACG emphasizes gas production and fermentation. Complementary rather than contradictory, but lead to different treatment priorities.
5. **IMO nomenclature:** Rome does not address methane/archaea/methanogens as a separate entity. The IMO concept (Pimentel's signature contribution to the ACG guideline) has no precedent in this 2013 report.

**Key divergences from AGA SIBO 2020 (G4):**
1. **Probiotics:** Rome is substantially more favorable. The AGA is silent-to-skeptical; Rome actively recommends.
2. **SIBO definition:** Rome foregrounds the definitional problem as a methodological limitation; AGA foregrounds it as a clinical reality. Same concern, different framing.
3. **Treatment specificity:** Neither provides the antibiotic efficacy table that distinguishes the ACG guideline, but Rome provides more specific probiotic guidance while AGA provides better recurrence management advice.
4. **PI-IBS:** Rome devotes a major section to PI-IBS; AGA mentions it in passing. Rome has the richer model of how infection triggers chronic symptoms.

**The temporal dimension:** This 2013 report predates both 2020 guidelines by seven years. It is best understood as the foundational academic critique that the later clinical guidelines had to respond to. The ACG 2020 guideline -- with its GRADE ratings openly acknowledging "very low quality of evidence" for every breath testing recommendation -- implicitly concedes the Rome report's methodological critique even while recommending the tests. The AGA 2020 Practice Update -- more skeptical in tone, co-authored by a Rome report reviewer (Quigley) -- reads as a partial synthesis of the Rome critique with clinical pragmatism. The Rome report, unconstrained by the need to issue actionable recommendations, remains the most intellectually honest of the three documents.

**Cross-reference priority:** Read alongside G3 (ACG SIBO 2020) and G4 (AGA SIBO 2020) as a triad. The Rome report provides the methodological critique; the ACG guideline provides the clinical action plan; the AGA update provides the cautious middle path. Together they represent the full spectrum of expert opinion on SIBO and microbiota in functional GI disorders from 2013-2020.
