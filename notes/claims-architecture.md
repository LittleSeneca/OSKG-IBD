---
tags: [type/architecture, oskg-ibd, phase-2, claims]
created: 2026-08-01
related: ["[[Claims Index]]", "[[../Notes Index]]", "[[claims-progress]]"]
---

# Claims Architecture — OSKG-IBD

Design document for Phase 2: extracting structured claim nodes from Phase 1 reading notes into the knowledge graph.

## Claim File Format

Every claim is a standalone markdown file in `notes/claims/` with YAML frontmatter and structured sections.

### Frontmatter

```yaml
---
tags:
  - type/claim
  - oskg-ibd
  - topic/<primary-topic>       # REQUIRED: 1-4 topic tags
  - topic/<secondary-topic>
  - evidence/<evidence-type>    # REQUIRED: 1-3 evidence tags
  - scholar/<scholar-slug>      # REQUIRED: 1+ scholar tags
  - source/<source-slug>        # REQUIRED: exactly one
  - domain/<domain>             # REQUIRED: one of pathophysiology, diagnosis, treatment, microbiome, nutrition, clinical-guidelines, history
claim_id: "<id>"               # REQUIRED: format <source-slug>-<claim-num>
statement: "<one sentence>"     # REQUIRED
confidence: "<rating>"          # REQUIRED: very-high | high | medium-high | medium | low-medium | low | debatable
confidence_rationale: "<one sentence>"
claim_type: "<type>"            # definitional | mechanistic | therapeutic | diagnostic | dietary | epidemiological | methodological
source_note: "[[<chapter-note-filename>]]"
created: 2026-08-01
updated: 2026-08-01
status: active
---
```

### Body Sections

```
# <claim_id>: <statement>

**Source:** [[<chapter-note>]] — <Author>, *<Title>* (<Year>)

## The Claim

<Full claim statement with direct quote from the chapter note.>

## Evidence

<Structured evidence — bullet points, tables, narrative. Copied from chapter note.>

## Confidence

**Rating:** <rating>
**Rationale:** <one sentence>

## Stakes

<What's at stake.>

## Disagreement

**Who disagrees:** <named scholars or guidelines>
**Alternative reading:** <counter-position>

## Edges

**Depends on:**
<!-- Claims this one requires to be true -->

**Supports:**
<!-- Claims this one provides evidence for -->

**Contradicts:**
<!-- Claims that cannot be true if this one is -->

**Challenged by:**
<!-- Evidence or arguments that weaken this claim -->

## Assessment

<Arron's evaluation from the chapter note.>
```

## Claim ID Convention

Format: `<source-slug>-<claim-num>`

The `source-slug` is a compact abbreviation of the source, and `claim-num` is a zero-padded number within that source.

### Source Slug Registry

**Tier 1 — Textbooks**

| Source Slug | Source |
|-------------|--------|
| `yamada-ibd62` | Yamada 7E Ch62: IBD Pathogenesis |
| `yamada-uc63` | Yamada 7E Ch63: UC Clinical Manifestations and Management |
| `yamada-cd64` | Yamada 7E Ch64: Crohn's Disease Management |
| `yamada-surg65` | Yamada 7E Ch65: Surgical Treatment of IBD |
| `yamada-ucdx63` | Yamada 7E Ch63: UC Diagnosis |
| `yamda-cddx64` | Yamada 7E Ch64: Crohn's Disease Diagnosis |
| `yamada-sibo58` | Yamada 7E Ch58: Bacterial Overgrowth |
| `steinhart-drug` | Steinhart 2018 Ch7: Drug Therapy |
| `steinhart-surg` | Steinhart 2018 Ch8: Surgical Treatment |

**Tier 1 — Microbiome & SIBO**

| Source Slug | Source |
|-------------|--------|
| `pimentel-ch1` | Pimentel 2022: Intro + Ch1 IBS/SIBO Overlap |
| `pimentel-ch2` | Pimentel 2022: Ch2 Gut Anatomy and MMC |
| `pimentel-ch3` | Pimentel 2022: Ch3 Gut Microbiome |
| `pimentel-ch4` | Pimentel 2022: Ch4 Food Poisoning Autoimmunity |
| `pimentel-ch5` | Pimentel 2022: Ch5 SIBO Definition and Diagnosis |
| `pimentel-ch6` | Pimentel 2022: Ch6 Three Pillars of SIBO Management |
| `pimentel-ch9` | Pimentel 2022: Ch9 Refractory SIBO |
| `pimentel-ch10` | Pimentel 2022: Ch10-11 Probiotics, FMT, and Myths |
| `pimentel-evol` | Pimentel 2006: SIBO Theory Evolution 2006-2022 |

**Tier 2 — Nutrition & Dietary**

| Source Slug | Source |
|-------------|--------|
| `gottschall-fw` | Gottschall 1994: Foreword |
| `gottschall-ch12` | Gottschall 1994: Ch1-2 Origins and Scientific Evidence |
| `gottschall-ch35` | Gottschall 1994: Ch3-5 The Vicious Cycle Mechanism |
| `gottschall-ch910` | Gottschall 1994: Ch9-10 Implementing the SCD |
| `foote-cookbook` | Foote 2020: Crohn's Disease Cookbook |
| `thompson-een` | Thompson 2013: Elemental Diet Protocol |
| `sarna-sibo-diet` | Sarna 2021: Healing SIBO Dietary Protocol |
| `pimentel-lfe` | Pimentel 2022: Low-Fermentation Eating |
| `campbell-gaps` | Campbell-McBride: GAPS Protocol |
| `ballantyne-paleo` | Ballantyne 2013: The Paleo Approach |
| `myers-autoimmune` | Myers 2015: The Autoimmune Solution |

**Tier 2 — Microbiome Context**

| Source Slug | Source |
|-------------|--------|
| `sarna-sibo-guide` | Sarna 2021: Healing SIBO Patient Guide |
| `lapine-cookbook` | LaPine 2021: SIBO Made Simple Cookbook |
| `chutkan-found` | Chutkan: Intro Ch1-3 Foundations |
| `chutkan-dysbiosis` | Chutkan: Ch5 Dysbiosis |
| `chutkan-rewild` | Chutkan: Ch11 Rewilding Illness |

**Tier 3 — Clinical Guidelines**

| Source Slug | Source |
|-------------|--------|
| `acg-cd2018` | ACG Crohn's Disease 2018 (Lichtenstein) |
| `acg-uc2019` | ACG Ulcerative Colitis 2019 (Rubin) |
| `acg-sibo2020` | ACG SIBO 2020 (Pimentel) |
| `aga-sibo2020` | AGA SIBO 2020 (Quigley) |
| `aga-uc2020` | AGA UC 2020 (Feuerstein) |
| `aga-cd2021` | AGA Crohn's 2021 (Feuerstein) |
| `ecco-diag2019` | ECCO Diagnostic 2019 (Maaser) |
| `ecco-cd2020` | ECCO Crohn's Medical 2020 (Torres) |
| `ecco-uc2022` | ECCO UC Therapeutics 2022 (Raine) |
| `rome-sibo2017` | Rome Foundation SIBO Report 2017 |
| `bsg-ibd2019` | BSG IBD 2019 (Lamb) |

**Tier 4 — Adjacent & Context**

| Source Slug | Source |
|-------------|--------|
| `sonnenburg-gut` | Sonnenburg 2015: The Good Gut |
| `marya-inflamed` | Marya/Patel 2021: Inflamed |
| `context-microbiome` | Enders/Mayer/Bulsiewicz/Yong context note |

## Tag Taxonomy

### Topic Tags

Use 1-4 topic tags per claim to classify what the claim is about.

**Disease and Condition**
- `topic/ibd` — Inflammatory Bowel Disease (general)
- `topic/crohns-disease` — Crohn's disease specifically
- `topic/ulcerative-colitis` — Ulcerative colitis specifically
- `topic/ibd-u` — IBD unclassified/indeterminate
- `topic/sibo` — Small Intestinal Bacterial Overgrowth
- `topic/imo` — Intestinal Methanogen Overgrowth
- `topic/ibs` — Irritable Bowel Syndrome
- `topic/fgid` — Functional GI disorders

**Pathophysiology**
- `topic/pathogenesis` — Disease causation and development
- `topic/genetics` — Genetic susceptibility, GWAS, NOD2, ATG16L1
- `topic/immune-dysregulation` — Innate/adaptive immunity, cytokines
- `topic/epithelial-barrier` — Intestinal permeability, tight junctions
- `topic/microbiome` — Gut microbial ecology
- `topic/dysbiosis` — Microbial imbalance
- `topic/inflammation` — Inflammatory pathways
- `topic/autoimmunity` — Autoimmune mechanisms, anti-vinculin, CdtB

**Diagnosis**
- `topic/diagnosis` — Diagnostic approaches (general)
- `topic/endoscopy` — Colonoscopy, endoscopy, mucosal assessment
- `topic/imaging` — CTE, MRE, ultrasound
- `topic/biomarkers` — Fecal calprotectin, CRP, serology
- `topic/breath-testing` — Hydrogen/methane breath tests
- `topic/histology` — Tissue pathology
- `topic/differential-diagnosis` — Distinguishing between conditions

**Treatment**
- `topic/treatment` — Treatment approaches (general)
- `topic/pharmacology` — Drug therapy (general)
- `topic/5-asa` — Mesalamine, sulfasalazine
- `topic/corticosteroids` — Prednisone, budesonide
- `topic/immunomodulators` — Thiopurines, methotrexate
- `topic/biologics` — Biologic therapies (general)
- `topic/anti-tnf` — Infliximab, adalimumab
- `topic/anti-integrin` — Vedolizumab, natalizumab
- `topic/anti-il12-23` — Ustekinumab
- `topic/jak-inhibitors` — Tofacitinib, upadacitinib
- `topic/antibiotics` — Rifaximin, metronidazole, ciprofloxacin
- `topic/surgery` — Colectomy, IPAA, strictureplasty
- `topic/probiotics` — Probiotic supplementation
- `topic/fmt` — Fecal microbiota transplantation
- `topic/therapeutic-drug-monitoring` — TDM, drug levels, antibodies

**Dietary Intervention**
- `topic/diet` — Dietary intervention (general)
- `topic/scd` — Specific Carbohydrate Diet
- `topic/low-fodmap` — Low-FODMAP diet
- `topic/lfe` — Low-Fermentation Eating
- `topic/elemental-diet` — Elemental/enteral nutrition
- `topic/gaps` — Gut and Psychology Syndrome diet
- `topic/paleo` — Paleo/autoimmune protocol
- `topic/ssfg` — SIBO Specific Food Guide
- `topic/carbohydrate-malabsorption` — Disaccharidase deficiency
- `topic/microbial-fermentation` — Bacterial fermentation of substrate

**Clinical Approach**
- `topic/treat-to-target` — Mucosal healing as treatment goal
- `topic/step-up-vs-top-down` — Treatment sequencing strategy
- `topic/mucosal-healing` — Endoscopic remission
- `topic/risk-stratification` — Predicting disease course
- `topic/mdt` — Multidisciplinary team approach
- `topic/quality-of-life` — Patient-reported outcomes

**Epidemiology**
- `topic/epidemiology` — Incidence, prevalence, risk factors
- `topic/environmental-triggers` — Smoking, diet, antibiotics, pollution
- `topic/social-determinants` — Socioeconomic, racial, geographic factors

**Methodology**
- `topic/grade` — GRADE evidence assessment
- `topic/clinical-trial-design` — RCT methodology
- `topic/guideline-comparison` — Cross-guideline analysis

### Evidence Tags

Use 1-3 evidence tags per claim.

- `evidence/meta-analysis` — Systematic review with meta-analysis
- `evidence/rct` — Randomized controlled trial
- `evidence/cohort` — Prospective or retrospective cohort study
- `evidence/case-control` — Case-control study
- `evidence/case-series` — Case series or registry data
- `evidence/observational` — Cross-sectional or epidemiological
- `evidence/clinical-guideline` — Guideline recommendation
- `evidence/expert-consensus` — Expert opinion without formal grading
- `evidence/mechanistic` — In vitro, animal model, or biochemical pathway
- `evidence/gwas` — Genome-wide association study
- `evidence/animal-model` — Mouse/animal colitis models
- `evidence/systematic-review` — Systematic review without meta-analysis

### Scholar Tags

- `scholar/ananthakrishnan` — Ashwin Ananthakrishnan (MGH)
- `scholar/xavier` — Ramnik Xavier (Broad Institute/Harvard)
- `scholar/podolsky` — Daniel Podolsky (UTSW)
- `scholar/steinhart` — A. Hillary Steinhart (Mount Sinai Toronto)
- `scholar/pimentel` — Mark Pimentel (Cedars-Sinai)
- `scholar/rezaie` — Ali Rezaie (Cedars-Sinai)
- `scholar/gottschall` — Elaine Gottschall
- `scholar/sarna` — Phoebe Lapine (writing as Sarna)
- `scholar/lapine` — Phoebe Lapine
- `scholar/thompson` — Margaret Thompson
- `scholar/foote` — Amanda Foote
- `scholar/chutkan` — Robynne Chutkan
- `scholar/sonnenburg` — Justin and Erica Sonnenburg
- `scholar/campbell-mcbride` — Natasha Campbell-McBride
- `scholar/ballantyne` — Sarah Ballantyne
- `scholar/myers` — Amy Myers
- `scholar/marya` — Rupa Marya
- `scholar/patel` — Raj Patel
- `scholar/lichtenstein` — Gary Lichtenstein
- `scholar/rubin` — David Rubin
- `scholar/feuerstein` — Joseph Feuerstein
- `scholar/quigley` — Eamonn Quigley
- `scholar/torres` — Joana Torres
- `scholar/raine` — Tim Raine
- `scholar/maaser` — Christian Maaser
- `scholar/lamb` — Christopher Lamb
- `scholar/enders` — Giulia Enders
- `scholar/mayer` — Emeran Mayer
- `scholar/bulsiewicz` — Will Bulsiewicz
- `scholar/yong` — Ed Yong

### Domain Tags

One per claim, indicating which knowledge domain this claim belongs to.

- `domain/pathophysiology`
- `domain/diagnosis`
- `domain/treatment`
- `domain/microbiome`
- `domain/nutrition`
- `domain/clinical-guidelines`
- `domain/history`

### Source Tags

Exactly one per claim, mapping to the source. Values are the same as the source slug registry above.

## Slug Convention

Claim file slugs are descriptive, hyphenated phrases capturing the core assertion. Rules:

1. Lowercase, hyphens between words
2. Must be unique within `notes/claims/`
3. Capture the core assertion, not the source
4. Begin with `claim-` prefix for graph navigability

Examples:
- `claim-ibd-loss-of-immune-tolerance-commensal-flora`
- `claim-gwas-200-loci-modest-heritability`
- `claim-nod2-strongest-cd-susceptibility-gene`
- `claim-mucosal-healing-treatment-goal`
- `claim-5asa-effective-uc-disappointing-cd`
- `claim-sibo-not-infection-impaired-clearance`
- `claim-three-gas-model-symptom-profiles`

## Confidence Rating Scale

Standardized from the reading notes:

| Rating | Meaning |
|--------|---------|
| `very-high` | Multiple independent converging lines of evidence; replicated RCTs or meta-analyses; no meaningful dissent |
| `high` | Strong evidence from well-conducted studies; minor debate on details but broad consensus |
| `medium-high` | Good evidence with some gaps; one or two key studies with reasonable alternative interpretations |
| `medium` | Moderate evidence; conflicting data or single-source support; plausible but not established |
| `low-medium` | Limited evidence; pilot studies, mechanistic plausibility, or expert opinion without strong data |
| `low` | Weak evidence; anecdotal, theoretical, or contradicted by better studies |
| `debatable` | Active controversy with reasonable arguments on multiple sides; evidence does not clearly favor one position |

## Claim Types

- `definitional` — Defines what a condition, mechanism, or concept IS
- `mechanistic` — Explains HOW something works (pathway, causal chain)
- `therapeutic` — Claims about treatment efficacy, safety, or strategy
- `diagnostic` — Claims about test accuracy, interpretation, or utility
- `dietary` — Claims about dietary interventions or food-microbiome interactions
- `epidemiological` — Claims about incidence, prevalence, risk factors, or population patterns
- `methodological` — Claims about evidence quality, trial design, or research methods
- `comparative` — Claims that directly compare two or more approaches/sources

## Intra-Batch Edge Types

Edges connect claims within and across sources:

- `supports` — Claim A provides evidence for Claim B
- `contradicts` — Claim A and Claim B cannot both be true
- `extends` — Claim A refines or extends Claim B
- `depends_on` — Claim A requires Claim B to be true
- `operationalizes` — Claim A provides practical implementation of theoretical Claim B
- `challenges` — Claim A weakens but does not fully contradict Claim B
- `qualifies` — Claim A adds important limitations or context to Claim B

## Batch Extraction Plan

Batches ordered by structural priority: extract foundational claims first so later batches can edge to them.

| Batch | Domain(s) | Notes | Est. Claims |
|-------|-----------|-------|-------------|
| 1 | Pathophysiology + Diagnosis | Yamada Ch62, Ch63dx, Ch64dx | 25 |
| 2 | Treatment | Steinhart Ch7-8, Yamada Ch63tx, Ch64tx, Ch65surg | 34 |
| 3 | Clinical Guidelines | All 11 guidelines | 125 |
| 4 | Microbiome & SIBO | All 17 notes | 60 |
| 5 | Nutrition | All 11 dietary notes | 51 |
| 6 | History + Tier 4 | Inflamed, Sonnenburg, context notes | ~10 |

After all batches: tag enrichment pass, cross-source edge pass, quality review.
