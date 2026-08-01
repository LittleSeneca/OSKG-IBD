#!/usr/bin/env python3
"""
Extract claims from the 4 remaining unextracted reading notes:
  BSG IBD 2019, Pimentel 2006 evolution, Sarna 2021 guide, LaPine 2021 cookbook.

Each claim is a discrete, verifiable assertion with evidence text from the source note.
Claims are written as individual .md files under notes/claims/.
"""
import re, os
from pathlib import Path

BASE = "/home/littleseneca/Projects/Personal/OSKG-IBD"
CLAIMS_DIR = f"{BASE}/notes/claims"
os.makedirs(CLAIMS_DIR, exist_ok=True)

def write_claim(slug, claim_id, statement, source_note, source_citation, config):
    """Write a single claim file with full evidence."""
    domain = config.get('domain', 'clinical-guidelines')
    tags = ["type/claim", "oskg-ibd", f"domain/{domain}"]
    tags.extend(config.get('topic_tags', []))
    tags.extend(config.get('evidence_tags', ['evidence/expert-consensus']))
    tags.extend(config.get('scholars', []))
    tags.append(config['source_tag'])

    tag_lines = "\n  - ".join(tags)
    confidence = config.get('confidence', 'medium')
    claim_type = config.get('claim_type', 'therapeutic')
    evidence = config.get('evidence', '')
    stakes = config.get('stakes', '')
    assessment = config.get('assessment', '')
    contradiction = config.get('contradiction', '')
    alt_reading = config.get('alt_reading', '')

    # Clean slug
    slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())[:80].strip('-')
    if not slug:
        slug = f"implicit-{config['source_slug']}"

    # Escape statement for YAML
    stmt_clean = statement[:200].replace('\n', ' ').replace('"', "'")

    content = f"""---
tags:
  - {tag_lines}
claim_id: "{claim_id}"
statement: "{stmt_clean}"
confidence: "{confidence}"
confidence_rationale: "See source note for full evidence evaluation."
claim_type: "{claim_type}"
source_note: "[[{source_note}]]"
created: 2026-08-01
updated: 2026-08-01
status: active
---

# {claim_id}: {statement[:150]}

**Source:** [[{source_note}]] — {source_citation}

## The Claim

{statement}

## Evidence

{evidence}

## Confidence

**Rating:** {confidence}
**Rationale:** See source note for full evidence evaluation.

## Stakes

{stakes}

## Disagreement

**Who disagrees:** {contradiction or 'Not documented.'}

**Alternative reading:** {alt_reading or 'Not documented.'}

## Edges

<!-- Populate during cross-source edge pass -->

**Depends on:**

**Supports:**

**Contradicts:**

**Challenged by:**

## Assessment

{assessment}
"""
    path = os.path.join(CLAIMS_DIR, f"claim-{slug}.md")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


# ============================================================
# BSG IBD 2019 — Key GRADE Statements
# ============================================================
BSG_CLAIMS = []

bsg_base = {
    "domain": "clinical-guidelines",
    "source_tag": "source/bsg-ibd-2019",
    "scholars": ["scholar/lamb", "scholar/kennedy", "scholar/raine"],
    "source_note": "BSG IBD 2019 - Lamb",
    "source_citation": "Lamb et al. — BSG Consensus Guidelines on IBD (2019), Gut 68(Suppl 3):s1-s106",
    "source_slug": "bsg-ibd2019",
    "topic_tags": ["topic/ibd", "topic/treatment", "topic/guideline-recommendation"],
}

# 1. BSG unique scope claim
BSG_CLAIMS.append({
    **bsg_base,
    "claim_id": "bsg-ibd2019-1",
    "slug": "bsg-2019-unified-uc-cd-single-document",
    "statement": "The BSG 2019 guideline is the first major international IBD guideline to cover both ulcerative colitis and Crohn's disease in a single unified document, with 168 recommendations (135 GRADE statements + 33 Good Practice Recommendations) developed through a modified eDelphi consensus involving 81 clinicians and patients, informed by systematic review of 88,247 publications.",
    "confidence": "very-high",
    "claim_type": "definitional",
    "evidence": "The guideline explicitly states it was commissioned to replace the 2011 BSG IBD guidelines. The methodology section details: 54 thematic questions producing 414 clinical questions structured by PICO/PEO; systematic searches of Medline and EMBASE (March 2017, updated March 2018, with top-up searches to June 2019); 88,247 publications after deduplication included in the evidence base; modified eDelphi process with 81 clinicians and patients using a custom-built online platform; statements achieving ≥80% consensus after two rounds were GRADE-assessed by two independent, blinded GDG members.",
    "stakes": "The single-document scope enables consistent cross-disease recommendations (infection screening, drug monitoring, service delivery) that separate UC/CD guidelines cannot provide. The explicit NICE/NHS integration makes this directly implementable in the UK health system.",
    "assessment": "The most comprehensive IBD guideline by evidence-base size. The unified format is a structural strength: it eliminates the redundancy and occasional inconsistency of separate UC and CD guidelines. The patient participation as voting members of the Delphi process was progressive for 2019.",
})

# 2. Treatment target
BSG_CLAIMS.append({
    **bsg_base,
    "claim_id": "bsg-ibd2019-2",
    "slug": "bsg-statement-2-treatment-target-mucosal-healing",
    "statement": "Statement 2 (weak, very low): Symptomatic remission combined with mucosal healing should be the treatment target in UC. The guideline endorses the STRIDE paradigm: clinical remission (absence of rectal bleeding + normal bowel habit) combined with endoscopic remission (Mayo endoscopic subscore ≤1). Histological remission is associated with improved outcomes but is not yet a validated treatment target.",
    "confidence": "medium",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/treatment-target", "topic/mucosal-healing", "topic/endoscopy", "topic/stride"],
    "evidence": "95.7% agreement in eDelphi. The guideline cites the STRIDE consensus (Peyrin-Biroulet 2015) for the clinical + endoscopic remission paradigm. It acknowledges that histological remission is associated with improved outcomes but lacks standardized definition and prospective validation. The UCEIS is endorsed as the preferred endoscopic severity score, with UCEIS ≥7 predicting need for colectomy in ASUC. The guideline's position is more cautious than subsequent STRIDE-II (2021), which elevated histological healing to an adjunctive measure.",
    "stakes": "Treating to endoscopic targets rather than symptoms alone changes clinical practice: patients may continue or escalate therapy despite feeling well if endoscopic inflammation persists. Conversely, de-escalation based on symptoms alone risks undertreating subclinical inflammation.",
    "assessment": "The BSG's cautious position on histological healing (acknowledged but not endorsed as target) is appropriate given the evidence in 2019. STRIDE-II's 2021 update partially closed this gap.",
})

# 3. UC Induction — 5-ASA superiority
BSG_CLAIMS.append({
    **bsg_base,
    "claim_id": "bsg-ibd2019-3",
    "slug": "bsg-statement-3-5asa-induction-uc",
    "statement": "Statement 3 (strong, high): Mild-to-moderate UC should be managed with oral 5-ASA 2-3 g/day, with the addition of 5-ASA enemas rather than oral treatment alone. Combined oral + rectal 5-ASA is superior to monotherapy even in pancolitis (RR no remission 0.65, 95% CI 0.47-0.91).",
    "confidence": "very-high",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/5-asa", "topic/mesalamine", "topic/ulcerative-colitis", "topic/induction-therapy"],
    "evidence": "95.6% agreement. The RR of 0.65 (95% CI 0.47-0.91) for no remission with combined oral + rectal vs oral alone is cited from meta-analytic data. This recommendation has 'high' GRADE quality — one of the rare high-quality recommendations in the guideline — reflecting the strength and consistency of the 5-ASA evidence base.",
    "stakes": "Establishes the first-line standard of care for UC. Failure to use rectal therapy in addition to oral 5-ASA means undertreating patients who could achieve remission with a simple, low-risk intervention.",
    "assessment": "One of the strongest recommendations in the guideline. Consistent with ACG 2019 and ECCO 2022. The superiority of combined oral + rectal therapy is well-established and underappreciated in general practice.",
})

# 4. Tofacitinib positioning — key divergence from ACG
BSG_CLAIMS.append({
    **bsg_base,
    "claim_id": "bsg-ibd2019-4",
    "slug": "bsg-statement-11-tofacitinib-post-anti-tnf",
    "statement": "Statement 11 (strong, high): Tofacitinib can be used in induction and maintenance of UC in patients where anti-TNF treatment has failed. The BSG limits tofacitinib to post-anti-TNF failure, whereas ACG 2019 makes strong recommendations for tofacitinib in anti-TNF-naive patients.",
    "confidence": "high",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/tofacitinib", "topic/jak-inhibitor", "topic/biologic-sequencing", "topic/contradiction"],
    "evidence": "91.1% agreement. The BSG's conservative positioning: 'Tofacitinib can be used in induction and maintenance of UC in patients where anti-TNF treatment has failed' (Statement 11). This contrasts with ACG 2019 (Rubin) which recommended tofacitinib in anti-TNF-naive patients. The BSG's position anticipated the post-marketing safety concerns that led to the FDA's 2021 JAK inhibitor black-box warning. The guideline notes that the choice between biologics and tofacitinib should be determined by clinical factors, patient choice, cost, likely adherence, and local infusion capacity.",
    "stakes": "Tofacitinib positioning directly affects treatment sequencing for every moderate-to-severe UC patient. The BSG's more conservative approach protects patients from the thrombotic and cardiovascular risks that were subsequently identified, but may delay access to an effective oral therapy.",
    "contradiction": "ACG 2019 (Rubin) — recommended tofacitinib in anti-TNF-naive patients (strong recommendation). The FDA's 2021 black-box warning for JAK inhibitors validated the BSG's more conservative position.",
    "assessment": "The most important divergence between BSG and ACG in the 2019 guidelines. The BSG's conservative positioning proved prescient. This is a strong example of European regulatory caution vs. American therapeutic enthusiasm.",
})

# 5. ASUC rescue therapy
BSG_CLAIMS.append({
    **bsg_base,
    "claim_id": "bsg-ibd2019-5",
    "slug": "bsg-statement-18-asuc-rescue-infliximab-ciclosporin",
    "statement": "Statement 18 (strong, high): Patients failing IV steroids by day 3 for ASUC should receive rescue therapy with IV infliximab or ciclosporin (for patients who have not previously failed thiopurines). The CYSIF and CONSTRUCT trials showed no significant difference in colectomy rates or quality-adjusted survival between the two agents.",
    "confidence": "very-high",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/asuc", "topic/infliximab", "topic/ciclosporin", "topic/rescue-therapy", "topic/colectomy"],
    "evidence": "97.8% agreement. CYSIF trial (Laharie 2012, n=115): treatment failure at day 98: 60% ciclosporin vs 54% infliximab (NS). Colectomy at 98 days: 17% vs 21%. CONSTRUCT trial (2019, n=270): no difference in quality-adjusted survival, colectomy rates (29% vs 30% at 3 months; 35% vs 45% at 1 year), time to colectomy, serious adverse events, or death. Infliximab was associated with greater cost. The guideline notes the response plateau at 3-5 days — extending IV steroids beyond 7-10 days adds toxicity without benefit. Overall steroid response rate: 67% (meta-analysis of 1,991 patients). Mortality: 1%.",
    "stakes": "ASUC is life-threatening. The day 3 decision point is critical: delayed surgery in ASUC increases postoperative mortality. The guideline's algorithm (Figure 2) with day 3 surgical consultation for non-responders is the most clinically useful ASUC management framework of any guideline.",
    "assessment": "CYSIF and CONSTRUCT provide the strongest head-to-head evidence in UC therapeutics and justify genuine equipoise. Real-world UK practice heavily favors infliximab due to provider familiarity and simplicity of continuing it as maintenance. The guideline's emphasis on day 3 surgical consultation for non-responders cannot be overstated.",
})

# 6. Surgery for localized CD
BSG_CLAIMS.append({
    **bsg_base,
    "claim_id": "bsg-ibd2019-6",
    "slug": "bsg-statement-36-surgery-localized-ileocaecal-cd",
    "statement": "Statement 36 (weak, low): Laparoscopic resection should be considered as an alternative to medical therapy for localized ileocaecal Crohn's disease. The BSG guideline explicitly frames surgery as a valid primary treatment option for limited disease — not just a last resort.",
    "confidence": "medium",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/surgery", "topic/ileocaecal-cd", "topic/laparoscopic-resection", "topic/crohns-disease"],
    "evidence": "97.3% agreement. The guideline positions surgery alongside medical therapy as a primary option, reflecting the LIR!C trial and cost-effectiveness data. This contrasts with North American practice, where surgery is typically reserved for medically refractory disease. The European tradition of earlier surgical intervention for limited disease is supported by data showing excellent long-term outcomes and reduced cumulative immunosuppression exposure.",
    "stakes": "Challenges the 'biologics-first' paradigm. For a patient with a 5cm terminal ileal stricture, surgery may provide years of drug-free remission vs. a lifetime of biologic therapy. However, the risk of postoperative recurrence (endoscopic in 70-90% at 1 year without prophylaxis) must be weighed.",
    "contradiction": "North American guidelines (ACG 2018, AGA 2021) position surgery as a last resort after medical failure. The BSG's surgery-positive stance reflects European surgical culture and cost-effectiveness data rather than evidence of superiority.",
    "assessment": "May reflect UK surgical culture more than evidence superiority. Supported by cost-effectiveness data and the LIR!C trial, but the relatively weak recommendation (weak, low quality) appropriately reflects the limitations of the evidence base.",
})

# 7. Mesalazine NOT for CD
BSG_CLAIMS.append({
    **bsg_base,
    "claim_id": "bsg-ibd2019-7",
    "slug": "bsg-statement-42-mesalazine-not-for-cd",
    "statement": "Statement 42 (strong, moderate): Mesalazine should NOT be used for induction or maintenance of remission in Crohn's disease. This strong negative recommendation is consistent with ACG 2018.",
    "confidence": "very-high",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/mesalazine", "topic/5-asa", "topic/crohns-disease", "topic/maintenance-therapy", "topic/negative-recommendation"],
    "evidence": "97.7% agreement. The guideline cites multiple RCTs and meta-analyses showing no benefit of mesalazine over placebo for CD induction or maintenance. This is one of the strongest negative recommendations in the guideline, reflecting the consistency and quality of the evidence against mesalazine in CD.",
    "stakes": "Despite this strong recommendation and consistent evidence, mesalazine continues to be prescribed for CD in clinical practice — particularly by non-specialists. This recommendation directly addresses a common practice gap.",
    "assessment": "A strong, evidence-supported negative recommendation. The persistence of mesalazine prescribing for CD despite clear evidence of inefficacy reflects clinical inertia and the understandable desire to 'do something' with a low-toxicity agent.",
})

# 8. 5-ASA chemoprevention for CRC
BSG_CLAIMS.append({
    **bsg_base,
    "claim_id": "bsg-ibd2019-8",
    "slug": "bsg-statement-126-mesalazine-crc-chemoprevention",
    "statement": "Statement 126 (strong, moderate): UC/IBD-U patients with left-sided or more extensive disease should take mesalazine ≥2 g daily to reduce colorectal cancer risk. This is a uniquely strong chemoprevention recommendation not found in ACG guidelines at the same evidence level.",
    "confidence": "medium",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/colorectal-cancer", "topic/chemoprevention", "topic/mesalazine", "topic/5-asa", "topic/dysplasia"],
    "evidence": "95.5% agreement. The recommendation is supported by observational data showing reduced CRC risk with mesalazine maintenance therapy. However, the evidence is confounded by mucosal healing: patients who take mesalazine regularly are also those with better disease control, and it is unclear whether the chemopreventive effect is from the drug or from the healed mucosa. The guideline acknowledges this limitation but makes a strong recommendation nonetheless.",
    "stakes": "If mesalazine truly reduces CRC risk, every UC patient with extensive disease should be on it indefinitely — even those in deep remission who might otherwise consider stopping. If the effect is confounded by mucosal healing, the recommendation overtreats patients at low CRC risk.",
    "contradiction": "ACG guidelines do not make a formal recommendation for 5-ASA chemoprevention. The evidence is observational and confounded — is it the drug or the healed mucosa that reduces risk?",
    "assessment": "The strongest mesalazine chemoprevention recommendation of any major IBD guideline. Reflects the UK's long-standing practice. The confounding by mucosal healing is a genuine methodological concern that weakens the evidence base despite the strong recommendation.",
})

# 9. EEN in adult CD
BSG_CLAIMS.append({
    **bsg_base,
    "claim_id": "bsg-ibd2019-9",
    "slug": "bsg-statement-34-een-adult-cd",
    "statement": "Statement 34 (weak, low): Exclusive Enteral Nutrition (EEN) may be considered as an alternative to corticosteroids to induce remission in adults with CD, with appropriate dietetic support. EEN is as effective as corticosteroids in paediatric CD (73% remission on intention-to-treat basis) but evidence is weaker in adults.",
    "confidence": "low-medium",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/een", "topic/elemental-diet", "topic/nutrition", "topic/crohns-disease", "topic/corticosteroids"],
    "evidence": "The guideline acknowledges: 'EEN is as effective as corticosteroids in paediatric CD (73% remission on intention-to-treat basis) but evidence is weaker in adults.' Polymeric feeds are as effective as elemental feeds (Statement 35, strong, moderate). A minimum of 4-6 weeks is recommended; 10 days achieves symptomatic relief but mucosal healing takes up to 8 weeks. The weaker evidence in adults reflects lower adherence (taste fatigue, social restrictions) rather than lower biological efficacy.",
    "stakes": "EEN offers a non-immunosuppressive induction option for adults who wish to avoid corticosteroids. However, the practical challenges of 4-6 weeks of exclusive liquid nutrition limit real-world uptake. The guideline notes that limited dietetic access within MDTs restricts EEN availability.",
    "assessment": "The prominence of EEN in the BSG guideline (and its weaker status in North American guidelines) reflects the UK's greater clinical experience with dietary therapy. The weak recommendation for adults is appropriate given the adherence challenges.",
})

# 10. Biosimilar infliximab
BSG_CLAIMS.append({
    **bsg_base,
    "claim_id": "bsg-ibd2019-10",
    "slug": "bsg-statement-91-biosimilar-infliximab-ct-p13",
    "statement": "Statement 91 (strong, moderate): Biosimilar infliximab (CT-P13) may be used for induction and maintenance in CD and UC. The PANTS study showed no clinically meaningful differences between originator and biosimilar infliximab in efficacy or immunogenicity.",
    "confidence": "very-high",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/biosimilars", "topic/infliximab", "topic/ct-p13", "topic/anti-tnf", "topic/pants-study"],
    "evidence": "The PANTS 3-year observational cohort (1,601 CD patients) showed immunogenicity rates at week 54 of 26% for originator infliximab and 28% for biosimilar CT-P13 — not significantly different. Immunomodulator co-therapy reduced immunogenicity risk (HR 0.37, p<0.0001). NOR-SWITCH and real-world switching data support safety of transitioning from originator to biosimilar in stable patients. The guideline recommends recording biological treatments by brand name where biosimilars are available (GPR 31).",
    "stakes": "Biosimilar adoption reduces drug costs by 30-50%, expanding access to biologic therapy. In the NHS, biosimilar savings have funded expansion of biologic services to previously untreated patient populations.",
    "assessment": "The PANTS study is the largest real-world biosimilar immunogenicity dataset. The BSG's endorsement of CT-P13 with PANTS data provides stronger evidence for biosimilar equivalence than the NOR-SWITCH trial alone (which was not powered for IBD-specific outcomes).",
})

# 11. Service delivery — MDT
BSG_CLAIMS.append({
    **bsg_base,
    "claim_id": "bsg-ibd2019-11",
    "slug": "bsg-gpr27-ibd-mdt-model",
    "statement": "GPR 27: The IBD MDT should include a core membership of gastroenterologist, colorectal surgeon, IBD specialist nurse, radiologist, dietitian, histopathologist, and pharmacist — all with IBD expertise. The MDT is organized as a concentric-circle model: inner circle (present at all meetings), middle circle (attend when possible), outer circle (contribute through combined clinics or shared protocols).",
    "confidence": "medium",
    "claim_type": "definitional",
    "topic_tags": ["topic/service-delivery", "topic/mdt", "topic/ibd-nurse", "topic/nhs"],
    "evidence": "97.9% agreement. The guideline provides a concentric-circle MDT model (Figure 7). The inner circle consists of gastroenterologist, surgeon, IBD nurse, radiologist, dietitian, histopathologist, and pharmacist. The middle circle includes professionals who attend when possible. The outer circle contributes through combined clinics or shared protocols. Trainees sit in a grey circle as part of their education. GPR 28 requires a formal record of management decisions (100% agreement).",
    "stakes": "This is the only major IBD guideline to specify exact MDT composition with a concentric model. ACG/AGA guidelines have no equivalent section. The specification defines what an IBD service should look like, not just what treatments to use.",
    "assessment": "The service delivery section is the BSG guideline's most distinctive contribution. No other guideline specifies MDT composition and service infrastructure at this level of detail. These are aspirational standards for the NHS.",
})

# 12. Smoking and CD
BSG_CLAIMS.append({
    **bsg_base,
    "claim_id": "bsg-ibd2019-12",
    "slug": "bsg-statement-69-smoking-postoperative-cd",
    "statement": "Statement 69 (strong, moderate): All patients smoking after intestinal resection for CD should be actively encouraged to stop. Smoking is the strongest modifiable risk factor for postoperative recurrence (OR 2.5 for endoscopic, 2.0 for clinical recurrence).",
    "confidence": "very-high",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/smoking", "topic/crohns-disease", "topic/postoperative-recurrence", "topic/risk-factors"],
    "evidence": "100% agreement. The guideline cites meta-analytic data: OR 2.5 for endoscopic recurrence and 2.0 for clinical recurrence in smokers vs non-smokers post-resection. The TOPPIC trial showed thiopurines improved outcomes in smokers but did not confirm a wider postoperative role. The guideline's risk stratification for postoperative prophylaxis incorporates smoking as the highest-weight factor.",
    "stakes": "Smoking cessation is more effective than any pharmacologic prophylaxis for postoperative CD. Failure to address smoking in post-surgical patients means prescribing immunosuppression to treat a modifiable risk factor.",
    "assessment": "The one universally agreed-upon recommendation in CD. The 100% Delphi agreement reflects the strength of the smoking-CD evidence. No pharmacologic intervention approaches the effect size of smoking cessation on postoperative recurrence.",
})

# 13. Anti-TNF in pregnancy
BSG_CLAIMS.append({
    **bsg_base,
    "claim_id": "bsg-ibd2019-13",
    "slug": "bsg-statement-128-anti-tnf-pregnancy",
    "statement": "Statement 128 (weak, very low): IBD patients receiving anti-TNF therapy should be counselled about risks and benefits of continuing treatment throughout pregnancy. For patients with active disease or high risk of relapse, it may be advisable to continue throughout. For those with inactive disease who wish to discontinue, it may be reasonable to stop at the start of the third trimester.",
    "confidence": "low-medium",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/pregnancy", "topic/anti-tnf", "topic/biologics", "topic/breastfeeding"],
    "evidence": "97.7% agreement. Active IBD prior to conception is associated with poor pregnancy outcomes (premature delivery, low birth weight, spontaneous abortion). Anti-TNF in the third trimester increases transplacental transfer; infliximab levels are more variable than adalimumab. Low levels of biologics are detectable in breast milk but breastfed infants of mothers on biologics have similar infection rates and milestone achievement to non-exposed infants. BCG vaccination should be withheld until at least 6 months after birth, and rotavirus vaccine should not be given, for infants exposed in utero to biologic therapies (Statement 129).",
    "stakes": "The risk of untreated active IBD during pregnancy (preterm birth, low birth weight, spontaneous abortion) must be balanced against the theoretical risks of in utero biologic exposure. Discontinuing anti-TNF in a patient who then flares during pregnancy causes harm to both mother and fetus.",
    "assessment": "Pragmatic guidance reflecting the very low quality of evidence. The key principle — active disease is more dangerous than medication — is well-supported by observational data. The third-trimester discontinuation option for well-controlled patients is reasonable but requires close monitoring.",
})

# 14. STRIDE treatment target endorsement + GPR on annual review
BSG_CLAIMS.append({
    **bsg_base,
    "claim_id": "bsg-ibd2019-14",
    "slug": "bsg-statement-9-biologic-choice-moderate-severe-uc",
    "statement": "Statement 9 (strong, high/moderate): Patients requiring ≥2 corticosteroid courses in the past year, or who become corticosteroid-dependent or refractory, require escalation to thiopurines (moderate quality), anti-TNF therapy (high quality), vedolizumab (high quality), or tofacitinib (high quality). Choice should be determined by clinical factors, patient choice, cost, likely adherence, and local infusion capacity.",
    "confidence": "high",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/biologics", "topic/anti-tnf", "topic/vedolizumab", "topic/tofacitinib", "topic/corticosteroid-sparing"],
    "evidence": "96.6% agreement. The guideline explicitly lists cost as a determining factor alongside clinical factors and patient choice — reflecting the NHS single-payer context. The 'all options on the table' approach (thiopurines, anti-TNF, vedolizumab, tofacitinib as co-equal options post-steroid failure) differs from ACG 2019's stronger recommendations for individual agents without comparative sequencing guidance.",
    "stakes": "Corticosteroid dependence is a marker of inadequate disease control and predicts long-term complications. The guideline defines a clear steroid-sparing threshold (≥2 courses/year = escalation required).",
    "assessment": "The BSG's pluralistic approach to biologic choice is clinically realistic — there is no single 'best' biologic for all patients — but leaves clinicians without a decision algorithm. The explicit cost consideration is honest and reflects NHS resource constraints.",
})

print(f"\n{'='*60}")
print(f"EXTRACTING BSG IBD 2019 CLAIMS ({len(BSG_CLAIMS)} claims)")
print(f"{'='*60}")

for cfg in BSG_CLAIMS:
    path = write_claim(
        slug=cfg['slug'],
        claim_id=cfg['claim_id'],
        statement=cfg['statement'],
        source_note=cfg['source_note'],
        source_citation=cfg['source_citation'],
        config=cfg
    )
    print(f"  [{cfg['claim_id']}] {path.split('/')[-1]}")


# ============================================================
# Pimentel 2006 Evolution — Comparative Claims
# ============================================================
EVOL_CLAIMS = []

evol_base = {
    "domain": "microbiome",
    "source_tag": "source/pimentel-ibs-solution",
    "scholars": ["scholar/pimentel"],
    "source_note": "Pimentel 2006 - SIBO Theory Evolution 2006-2022",
    "source_citation": "Pimentel — A New IBS Solution (2006) vs The Microbiome Connection (2022)",
    "source_slug": "pimentel-evol",
    "topic_tags": ["topic/sibo", "topic/ibs", "topic/autoimmunity"],
}

# 1. Prevalence refinement
EVOL_CLAIMS.append({
    **evol_base,
    "claim_id": "pimentel-evol-1",
    "slug": "sibo-prevalence-84-vs-60-75-percent",
    "statement": "Pimentel's estimated SIBO prevalence in IBS decreased from 84% (2006, based on a 2003 double-blind study of 200+ patients at a tertiary referral center) to 60-75% (2022, incorporating broader epidemiological data). The initial estimate from a referral center was refined downward by population-level data.",
    "confidence": "high",
    "claim_type": "epidemiological",
    "evidence": "2006 book: 'In published studies, indirect measures of small bowel bacteria suggest that 84 percent of IBS sufferers have excessive quantities of bacteria typically found in the colon.' Cites Pimentel's 2003 double-blind study of 200+ subjects. 2022 book: presents 60-75% range, acknowledging that the initial referral-center estimate was biased upward by selection of more severely affected patients. The 2022 figure incorporates broader population-level data and is more conservative.",
    "stakes": "The prevalence estimate determines the clinical relevance of SIBO. At 84%, nearly all IBS is SIBO — breath testing is confirmatory. At 60%, a substantial minority of IBS has other causes. The downward refinement strengthens the argument for testing rather than empiric treatment.",
    "assessment": "A healthy example of scientific self-correction. The 2006 estimate was honest but biased by referral-center sampling. The 2022 estimate is more generalizable.",
})

# 2. CdtB-vinculin autoimmunity discovery
EVOL_CLAIMS.append({
    **evol_base,
    "claim_id": "pimentel-evol-2",
    "slug": "cdtb-vinculin-autoimmunity-discovery-2006-2022",
    "statement": "Between 2006 and 2022, Pimentel's group discovered the CdtB-vinculin autoimmunity mechanism: Campylobacter CdtB toxin → anti-CdtB antibodies → molecular mimicry with vinculin → anti-vinculin autoantibodies → MMC damage → SIBO. In 2006, the mechanism was unknown; by 2022, the full cascade had been characterized, validated in a 3000-patient study, and operationalized as a commercial blood test.",
    "confidence": "high",
    "claim_type": "mechanistic",
    "topic_tags": ["topic/autoimmunity", "topic/cdtd", "topic/vinculin", "topic/mechanism", "topic/food-poisoning"],
    "evidence": "2006 book: Pimentel was actively researching the toxin mechanism but had not identified CdtB: 'I am working with my colleagues at Cedars-Sinai conducting research to determine whether the toxin produced by...' — sentence trails off mid-page. Post-infectious IBS was recognized (European researchers since 1994) but the mechanism was unknown. 2022 book: Full CdtB-vinculin cascade described, validated in a blood test study of ~3000 patients. The IBS blood test (ibs-smart) detects anti-CdtB and anti-vinculin antibodies; ~60% of IBS-D/M test positive vs 20-30% who recall a heralding event in 2006.",
    "stakes": "The CdtB-vinculin mechanism transformed SIBO from a clinical observation to a molecularly defined disease pathway. It provides the mechanistic basis for the IBS blood test, gas-type-specific treatments, and the autoimmune framing of IBS.",
    "assessment": "The single most important evolutionary advance. This is translational research at its best: clinical observation (antibiotics improve IBS) → hypothesis (SIBO causes IBS) → mechanism (CdtB-vinculin autoimmunity) → diagnostic test → targeted treatment. The blood test's independent validation at multi-center scale will determine whether this narrative holds.",
})

# 3. Three-gas model and IMO
EVOL_CLAIMS.append({
    **evol_base,
    "claim_id": "pimentel-evol-3",
    "slug": "three-gas-model-imo-terminology-evolution",
    "statement": "Breath testing evolved from hydrogen-only measurement (2006) to a three-gas model (2022): hydrogen (H2, diarrhea-predominant), methane (CH4, now classified as IMO — intestinal methanogen overgrowth, an archaeal not bacterial condition), and hydrogen sulfide (H2S, diarrhea-predominant). Methane ≥10 ppm on breath test defines IMO, requiring different treatment (rifaximin + neomycin) than hydrogen-predominant SIBO.",
    "confidence": "high",
    "claim_type": "definitional",
    "topic_tags": ["topic/breath-testing", "topic/methane", "topic/hydrogen-sulfide", "topic/imo"],
    "evidence": "2006: breath testing measured only hydrogen. Methane was mentioned but not as a distinct diagnostic category. No hydrogen sulfide measurement. 2022: The three-gas model includes H2 (lactulose breath test, rise within 90 minutes), CH4 (≥10 ppm = IMO), and H2S (measured by trio-smart breath test). IMO is distinguished from SIBO: it's archaeal overgrowth (Methanobrevibacter smithii), not bacterial. Gas-type-specific antibiotic protocols developed: rifaximin for H2, rifaximin + neomycin for CH4, rifaximin + bismuth for H2S.",
    "stakes": "The IMO reclassification means that 'methane SIBO' is technically not SIBO — it's archaeal overgrowth. This has treatment implications: neomycin (or metronidazole) must be added to rifaximin for IMO; rifaximin alone is insufficient. The hydrogen sulfide measurement enables identification of a third gas type previously invisible to standard breath testing.",
    "assessment": "The three-gas model and IMO terminology represent the most important taxonomic refinement in SIBO diagnosis. The ecological competition model (hydrogen producers = foxes, methanogens = wolves) explains why methane-positive patients present with constipation and why eradication of methanogens can unmask hydrogen-predominant SIBO.",
})

# 4. Prokinetic optimization
EVOL_CLAIMS.append({
    **evol_base,
    "claim_id": "pimentel-evol-4",
    "slug": "prokinetic-optimization-erythromycin-prucalopride",
    "statement": "Prokinetic therapy evolved from erythromycin or tegaserod for 3 months (2006) to prucalopride as the preferred agent with a drug holiday strategy (2022). Serotonin agonists (prucalopride, tegaserod) prevent SIBO recurrence for 200+ days vs erythromycin's 'few months.' The rationale for nighttime dosing (targeting fasting MMC, not feeding motility) was established.",
    "confidence": "medium-high",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/prokinetics", "topic/prucalopride", "topic/mmc", "topic/relapse-prevention"],
    "evidence": "2006 protocol: erythromycin 50mg or tegaserod 2-6mg at bedtime for 3 months. 2022 protocol: prucalopride preferred; erythromycin, tegaserod, pyridostigmine, low-dose naltrexone as alternatives. Comparative study: serotonin agonists prevent SIBO for 200+ days vs erythromycin's few months. Drug holiday strategy developed for tachyphylaxis. Nighttime dosing targets the fasting MMC (migrating motor complex), which occurs primarily during sleep and between meals — not feeding motility.",
    "stakes": "Prokinetic therapy is Pillar 3 of Pimentel's SIBO management framework (prevention of recurrence). The superiority of serotonin agonists over erythromycin is not widely appreciated outside specialist SIBO practice. Tachyphylaxis management (drug holidays) prevents loss of efficacy over time.",
    "assessment": "The prokinetic optimization represents the most practical clinical advance. The nighttime dosing rationale and drug holiday strategy are simple interventions that significantly improve long-term outcomes.",
})

# 5. Treatment expectation refinement
EVOL_CLAIMS.append({
    **evol_base,
    "claim_id": "pimentel-evol-5",
    "slug": "treatment-expectation-refinement-2006-2022",
    "statement": "Treatment expectations evolved from 'antibiotics can almost completely relieve IBS symptoms' (2006) to five response categories (2022): one-and-done (~33% cure), relapse (~70% after initial response, treatable with repeat antibiotics), partial response (may respond to combination antibiotics or elemental diet), no response (may not have SIBO), and refractory (underlying cause not addressed).",
    "confidence": "high",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/treatment-outcomes", "topic/rifaximin", "topic/relapse"],
    "evidence": "2006: 'antibiotics can almost completely relieve IBS symptoms if successful in eliminating the intestinal bacteria.' 2022: five response categories based on clinical experience and TARGET 3 trial data. The 'one-and-done' category (~33%) reflects patients whose SIBO is cured with a single course. The relapse category (~70%) requires repeat treatment and prokinetic prevention. The partial response category may benefit from combination antibiotics or elemental diet. The refractory category suggests an unidentified underlying cause.",
    "stakes": "Unrealistic treatment expectations damage the therapeutic alliance. Patients who expect 'almost complete relief' and experience relapse may abandon effective treatment. The five-category framework sets appropriate expectations and provides a roadmap for management of incomplete response.",
    "assessment": "The most honest evolution in Pimentel's framework. The 2006 claim was aspirational; the 2022 framework is clinical reality. The 44% response rate in TARGET 3 is not dramatically better than the 35% response to neomycin in 2003 — the real advance is in managing expectations and treating relapse.",
})

# 6. What stayed the same
EVOL_CLAIMS.append({
    **evol_base,
    "claim_id": "pimentel-evol-6",
    "slug": "sibo-core-principles-unchanged-2006-2022",
    "statement": "Several core elements of Pimentel's SIBO framework remained unchanged between 2006 and 2022: (a) the MMC housekeeper wave as the central protective mechanism, (b) lactulose breath testing preferred over glucose, (c) elemental diet >80% effective, (d) the H. pylori/peptic ulcer analogy, (e) SIBO as a secondary phenomenon requiring treatment of the underlying cause, (f) IBS as organic not psychological, and (g) food poisoning (specifically Campylobacter) as the primary initiating event.",
    "confidence": "very-high",
    "claim_type": "mechanistic",
    "evidence": "Both books present these elements consistently. The MMC mechanism, lactulose preference, elemental diet efficacy (>80% in both), the H. pylori analogy, the secondary-phenomenon framing, the anti-stigma argument, and the food poisoning etiology are present in 2006 and reaffirmed in 2022. The stability of these core principles across 16 years and multiple research cycles strengthens their credibility.",
    "stakes": "The unchanged principles represent the bedrock of Pimentel's SIBO framework. If any of these were to be invalidated, the entire framework would need revision. Their stability across 16 years of research suggests they have survived empirical testing.",
    "assessment": "The stability of the core principles is reassuring but also reflects the limitations of the evidence base: these principles have not been independently validated at scale. The MMC mechanism, in particular, while biologically plausible, has not been directly demonstrated as the sole protective mechanism in vivo.",
})

# 7. Weakest advance — treatment efficacy
EVOL_CLAIMS.append({
    **evol_base,
    "claim_id": "pimentel-evol-7",
    "slug": "treatment-efficacy-modest-improvement-2006-2022",
    "statement": "Despite 16 years of mechanism discovery, SIBO treatment efficacy improved only modestly: rifaximin's 44% response rate in TARGET 3 (2015) is not dramatically better than neomycin's 35% response in the 2003 study. The real advance is in treatment specificity (gas-type matching) and prevention (prokinetic optimization), not in treatment efficacy.",
    "confidence": "high",
    "claim_type": "therapeutic",
    "evidence": "2003 double-blind study: neomycin 35% symptom improvement vs 11% placebo. Among those whose breath tests normalized, 75% had IBS improvement. 2015 TARGET 3 trial: rifaximin 44% response rate for IBS-D. The absolute improvement from 35% to 44% over 12 years is modest. The guideline notes that the real advances are in gas-type-specific protocol selection and prokinetic optimization for relapse prevention, not in the magnitude of antibiotic response.",
    "stakes": "This is the most sobering finding in the evolutionary analysis. It suggests that the ceiling of antibiotic monotherapy for SIBO may be ~40-50%, and that further mechanistic understanding alone will not improve outcomes — what is needed is better therapeutic agents or combination approaches.",
    "assessment": "The weakest evolutionary advance and the most honest observation. The 2006-2022 journey is a story of vastly improved understanding with only modestly improved treatment. This pattern (mechanism discovery outpacing therapeutic advance) is common in translational medicine but rarely stated so plainly.",
})

print(f"\n{'='*60}")
print(f"EXTRACTING PIMENTEL 2006 EVOLUTION CLAIMS ({len(EVOL_CLAIMS)} claims)")
print(f"{'='*60}")

for cfg in EVOL_CLAIMS:
    path = write_claim(
        slug=cfg['slug'],
        claim_id=cfg['claim_id'],
        statement=cfg['statement'],
        source_note=cfg['source_note'],
        source_citation=cfg['source_citation'],
        config=cfg
    )
    print(f"  [{cfg['claim_id']}] {path.split('/')[-1]}")


# ============================================================
# Sarna 2021 — Patient Guide Claims
# ============================================================
SARNA_CLAIMS = []

sarna_base = {
    "domain": "microbiome",
    "source_tag": "source/sarna-healing-sibo",
    "scholars": ["scholar/sarna", "scholar/siebecker"],
    "source_note": "Sarna 2021 - Healing SIBO Patient Guide",
    "source_citation": "Sarna — Healing SIBO (2021), Penguin Random House",
    "source_slug": "sarna-sibo-guide",
    "topic_tags": ["topic/sibo", "topic/treatment", "topic/herbal-antimicrobials"],
}

SARNA_CLAIMS.append({
    **sarna_base,
    "claim_id": "sarna-guide-1",
    "slug": "three-treatment-modalities-pharmaceutical-herbal-elemental",
    "statement": "Sarna presents three SIBO treatment modalities as co-equal options: pharmaceutical antibiotics (rifaximin ± neomycin, 10-14 day courses, gas-type-specific), herbal antimicrobials (oil of oregano, berberine, neem, allicin, 30-day courses, ~50% efficacy per retrospective study), and elemental diet (Vivonex or alternatives, 14 days, 80%+ efficacy for hydrogen SIBO).",
    "confidence": "medium",
    "claim_type": "therapeutic",
    "evidence": "Sarna Ch6 presents the three modalities. Herbal antimicrobial data is from a single retrospective study (cited but not named). Elemental diet >80% efficacy is consistent with Pimentel's data. The herbal antimicrobial efficacy claim (~50%) is based on clinical experience and one retrospective study — not RCT data. Sarna notes herbal protocols 'won't destroy the beneficial bacteria like conventional antibiotics do' — a claim Pimentel does not make but that is common in naturopathic SIBO literature.",
    "stakes": "The framing of herbal antimicrobials as co-equal with pharmaceutical antibiotics may create false equivalence. Herbal protocols have significantly less published evidence (one retrospective study vs multiple RCTs for rifaximin). However, for patients who cannot access or tolerate rifaximin, herbal protocols provide an evidence-informed alternative.",
    "assessment": "The three-modality framework is clinically useful but the evidence hierarchy must be maintained. The ~50% herbal efficacy claim should be caveated as low-quality evidence. The elemental diet's 80%+ efficacy is well-supported across multiple studies.",
})

SARNA_CLAIMS.append({
    **sarna_base,
    "claim_id": "sarna-guide-2",
    "slug": "sibo-relapse-management-multiple-treatment-rounds",
    "statement": "Sarna's relapse management approach acknowledges that 'most SIBO patients need more than one course of treatment or even one kind of treatment.' Key components: retesting with breath test 2-4 weeks post-antibiotics, prokinetic maintenance ('once you've cleared the overgrowth, you need to keep the small intestine clean with a prokinetic'), and psychological resilience ('SIBO is a marathon, not a sprint').",
    "confidence": "medium",
    "claim_type": "therapeutic",
    "topic_tags": ["topic/relapse", "topic/prokinetics", "topic/patient-management"],
    "evidence": "Sarna Ch7 details relapse management. The retesting interval (2-4 weeks) and prokinetic maintenance align with Pimentel's Pillar 3. The 'marathon, not a sprint' framing reflects the clinical reality that SIBO treatment is iterative — most patients require multiple antibiotic/herbal courses, dietary phases, and prokinetic adjustments before achieving sustained remission.",
    "stakes": "Normalizing multiple treatment rounds reduces patient discouragement and treatment abandonment. The prokinetic maintenance emphasis is critical: without it, relapse is nearly universal.",
    "assessment": "Sarna's relapse chapter is the most practically detailed in the SIBO literature for patients. The psychological dimension (managing expectations, building resilience) is absent from Pimentel's clinician-focused books and represents a genuine gap in conventional SIBO management.",
})

SARNA_CLAIMS.append({
    **sarna_base,
    "claim_id": "sarna-guide-3",
    "slug": "sibo-medicine-cabinet-symptom-remedies",
    "statement": "Sarna provides a 'SIBO Medicine Cabinet' of over-the-counter symptom relief options not covered in Pimentel's books: digestive bitters (gentian, dandelion), prokinetics (Iberogast, ginger, magnesium citrate), gas relief (activated charcoal, simethicone), pain/cramping (peppermint oil, CBD oil), and sleep/anxiety support (melatonin, magnesium glycinate, lemon balm).",
    "confidence": "low-medium",
    "claim_type": "therapeutic",
    "evidence": "Ch3. These remedies are based on clinical experience and traditional use rather than RCT data. Peppermint oil has the strongest evidence (calcium channel blocker mechanism, multiple IBS trials). Iberogast (STW 5) has some clinical trial evidence for functional dyspepsia. Most others are supported by anecdote and mechanism plausibility rather than controlled trials.",
    "stakes": "Symptom management remedies fill a practical gap in SIBO care — the period between starting treatment and achieving remission can be weeks to months. However, the risk is that patients substitute these remedies for evidence-based treatment or delay necessary medical evaluation.",
    "assessment": "A patient-centered contribution that acknowledges the lived experience of SIBO treatment. The evidence quality is low but the practical utility is high. These remedies should be positioned as adjunctive symptom management, not primary SIBO treatment.",
})

SARNA_CLAIMS.append({
    **sarna_base,
    "claim_id": "sarna-guide-4",
    "slug": "sarna-pimentel-alignment-differences",
    "statement": "Sarna's SIBO education (definition, three-gas model, MMC mechanism, food poisoning etiology, IBS-SIBO connection) is consistent with Pimentel's framework. Key differences: Sarna enthusiastically recommends herbal antimicrobials (Pimentel is cautiously open), adds naturopathic prokinetic options (Iberogast, ginger, magnesium), does not mention the IBS blood test, and de-emphasizes the autoimmunity mechanism in favor of patient empowerment.",
    "confidence": "high",
    "claim_type": "definitional",
    "topic_tags": ["topic/patient-education", "topic/practitioner-comparison"],
    "evidence": "Sarna's Ch1-2 SIBO education is sourced from Pimentel, Siebecker, and the SIBO SOS Summit expert network. The autoimmunity mechanism (CdtB-vinculin) is mentioned but not emphasized — a notable omission for a 2021 book, given that the mechanism had been published and the blood test was commercially available. The IBS blood test (ibs-smart) is not mentioned. Sarna's omission of the blood test may reflect the patient-advocate perspective: the test is expensive, not widely covered by insurance, and does not change the initial treatment approach.",
    "stakes": "The alignment on core SIBO concepts validates the Pimentel framework's penetration into patient education. The differences highlight the gap between research-center SIBO medicine (Cedars-Sinai) and community SIBO practice (naturopathic/functional medicine).",
    "assessment": "Sarna's book represents the 2021 SIBO consensus as disseminated to patients. Published between Pimentel 2006 and 2022, it incorporates the three-gas model and IMO concept but predates the 2022 book's treatment protocol refinements and lovastatin caution. The omission of the blood test is a significant gap for a 2021 publication.",
})

SARNA_CLAIMS.append({
    **sarna_base,
    "claim_id": "sarna-guide-5",
    "slug": "sibo-prevalence-78-percent-ibs-sarna",
    "statement": "Sarna cites 'up to 78 percent of people with IBS have SIBO' — splitting the difference between Pimentel's 2006 figure (84%) and his 2022 figure (60-75%). This reflects the 2021 consensus before the 2022 book's refinement.",
    "confidence": "medium",
    "claim_type": "epidemiological",
    "topic_tags": ["topic/sibo-prevalence", "topic/ibs"],
    "evidence": "Sarna cites the 78% figure without a specific source, placing it between Pimentel's 2006 (84%) and 2022 (60-75%) estimates. The 78% figure likely derives from the 2000s-era referral center studies that produced the higher estimates. By 2021, population-level data was beginning to suggest lower prevalence, but the 2022 book's refined range had not yet been published.",
    "stakes": "The prevalence estimate shapes clinical decision-making. At 78%, breath testing virtually all IBS patients is justified. At 60%, a more selective testing strategy may be appropriate.",
    "assessment": "Sarna's 78% reflects the transitional state of SIBO prevalence knowledge in 2021. The figure is outdated by 2022 standards but was reasonable at time of publication.",
})

print(f"\n{'='*60}")
print(f"EXTRACTING SARNA 2021 GUIDE CLAIMS ({len(SARNA_CLAIMS)} claims)")
print(f"{'='*60}")

for cfg in SARNA_CLAIMS:
    path = write_claim(
        slug=cfg['slug'],
        claim_id=cfg['claim_id'],
        statement=cfg['statement'],
        source_note=cfg['source_note'],
        source_citation=cfg['source_citation'],
        config=cfg
    )
    print(f"  [{cfg['claim_id']}] {path.split('/')[-1]}")


# ============================================================
# LaPine 2021 — Cookbook Claims
# ============================================================
LAPINE_CLAIMS = []

lapine_base = {
    "domain": "nutrition",
    "source_tag": "source/lapine-cookbook",
    "scholars": ["scholar/lapine"],
    "source_note": "LaPine 2021 - SIBO Made Simple Cookbook",
    "source_citation": "LaPine — SIBO Made Simple (2021), Hachette Go",
    "source_slug": "lapine-cookbook",
    "topic_tags": ["topic/sibo", "topic/diet", "topic/low-fodmap", "topic/scd"],
}

LAPINE_CLAIMS.append({
    **lapine_base,
    "claim_id": "lapine-cookbook-1",
    "slug": "multi-diet-recipe-tagging-five-sibo-protocols",
    "statement": "LaPine's recipes are tagged with compatibility across five SIBO dietary protocols: Low-FODMAP, SCD, SSFG (Siebecker's SIBO Specific Food Guide), Bi-phasic Diet (both phases), and Paleo. This is the only SIBO cookbook that systematically cross-references recipes across multiple dietary frameworks.",
    "confidence": "medium",
    "claim_type": "dietary",
    "evidence": "The book's 90+ recipes each carry dietary compatibility tags. The tagging system acknowledges that SIBO patients may cycle through different diets during different treatment phases (restriction, reintroduction, maintenance). LaPine's introduction explains the rationale: patients who start on SCD may later transition to low-FODMAP, and those on the Bi-phasic Diet may need Phase 1 (restrictive) and Phase 2 (expanded) options.",
    "stakes": "The multi-diet tagging system is pragmatically useful but implicitly acknowledges the field's lack of comparative dietary trial data. No single SIBO diet is universally effective, and patients often need to experiment across protocols. The tagging system provides a practical tool for navigating this uncertainty.",
    "assessment": "A practical contribution that reflects the maturity of the SIBO dietary landscape. The book's significance is in its demonstration that SIBO dietary management has matured enough to support a multi-protocol cookbook — a marker of the field's growth from niche clinical specialty to patient-accessible practice.",
})

LAPINE_CLAIMS.append({
    **lapine_base,
    "claim_id": "lapine-cookbook-2",
    "slug": "scd-low-fodmap-intersection-dietary-framework",
    "statement": "LaPine's approach combines SCD and low-FODMAP by finding their intersection: foods that are both SCD-legal (monosaccharides only, no disaccharides/polysaccharides) and low-FODMAP (restricted fermentable oligosaccharides, disaccharides, monosaccharides, and polyols). This intersection creates recipes that work for patients on either protocol.",
    "confidence": "medium",
    "claim_type": "dietary",
    "evidence": "The introductory chapters explain the SCD + low-FODMAP integration. SCD (Gottschall) restricts disaccharides and polysaccharides; low-FODMAP (Monash) restricts specific fermentable carbohydrates. The intersection of these two diets — foods legal on both — forms the basis of LaPine's recipe development. The integration is practical rather than theoretical: it does not resolve the tension between the two dietary frameworks (SCD is mechanism-based on disaccharidase deficiency; low-FODMAP is empiric based on fermentation patterns) but finds their common ground.",
    "stakes": "Dietary protocol selection in SIBO is largely empiric. A patient who responds to one diet may not respond to another. The SCD + low-FODMAP intersection provides a starting point that is compatible with both major SIBO dietary paradigms, reducing the risk of choosing the wrong protocol initially.",
    "assessment": "The SCD + low-FODMAP intersection is a pragmatic solution to the field's unresolved dietary protocol question. It does not advance the evidence base but provides a clinically useful starting point that honors both dietary traditions.",
})

LAPINE_CLAIMS.append({
    **lapine_base,
    "claim_id": "lapine-cookbook-3",
    "slug": "lapine-synthesis-not-primary-source",
    "statement": "LaPine's book is a synthesis of expert sources (Pimentel, Siebecker, Jacobi, Bulsiewicz, Sarna, Ruscio) rather than a source of original clinical recommendations. It is explicitly curated from the SIBO clinical consensus rather than presenting independent claims. The book's value to the knowledge graph is as a marker of dietary landscape maturity, not as primary evidence.",
    "confidence": "very-high",
    "claim_type": "definitional",
    "evidence": "LaPine's acknowledgments list the key SIBO experts she consulted. The introductory chapters synthesize existing SIBO education (definition, three-gas model, breath testing, dietary principles) consistent with the 2021 consensus. No original clinical recommendations or trial data are presented. The book is primarily a cookbook with patient education, not a clinical text.",
    "stakes": "Positioning LaPine correctly in the evidence hierarchy matters: it is a Tier 2 source (synthesis, context) not Tier 1 (primary evidence). Its claims should be verified against primary sources before being used to support clinical recommendations.",
    "assessment": "LaPine's book is valuable for what it represents — the maturation of the SIBO dietary landscape — not for what it contributes to the evidence base. It demonstrates that SIBO dietary management has achieved sufficient clinical consensus to support a consumer cookbook, which is itself evidence of the field's growth.",
})

print(f"\n{'='*60}")
print(f"EXTRACTING LAPINE 2021 COOKBOOK CLAIMS ({len(LAPINE_CLAIMS)} claims)")
print(f"{'='*60}")

for cfg in LAPINE_CLAIMS:
    path = write_claim(
        slug=cfg['slug'],
        claim_id=cfg['claim_id'],
        statement=cfg['statement'],
        source_note=cfg['source_note'],
        source_citation=cfg['source_citation'],
        config=cfg
    )
    print(f"  [{cfg['claim_id']}] {path.split('/')[-1]}")


total = len(BSG_CLAIMS) + len(EVOL_CLAIMS) + len(SARNA_CLAIMS) + len(LAPINE_CLAIMS)
print(f"\n{'='*60}")
print(f"TOTAL CLAIMS EXTRACTED: {total}")
print(f"  BSG IBD 2019: {len(BSG_CLAIMS)}")
print(f"  Pimentel 2006 Evolution: {len(EVOL_CLAIMS)}")
print(f"  Sarna 2021 Guide: {len(SARNA_CLAIMS)}")
print(f"  LaPine 2021 Cookbook: {len(LAPINE_CLAIMS)}")
print(f"{'='*60}")
