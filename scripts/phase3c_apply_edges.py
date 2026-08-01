#!/usr/bin/env python3
"""
Phase 3c: Add contradiction and challenged_by edges across SIBO diagnostic 
debate and competing scholarly camps.

Areas covered:
  1. SIBO breath testing controversy (Pimentel vs Rome Foundation vs AGA)
  2. SIBO treatment philosophy (antibiotics vs diet-first vs root-cause)
  3. Dietary frameworks (SCD vs LFE vs GAPS vs low-FODMAP)
  4. IBS-SIBO overlap (Pimentel vs Rome Foundation)
  5. Probiotic use (Rome Foundation vs ACG vs Pimentel)

Edge classification:
  - contradicts: mutually exclusive factual claims about the same phenomenon
  - challenged_by: disagreement in interpretation, emphasis, or scope
"""

import os
import re
from collections import defaultdict

CLAIMS_DIR = os.path.expanduser("~/Projects/Personal/OSKG-IBD/notes/claims")

# ─── Contradiction pairs ────────────────────────────────────────────

# Each entry: (source_slug, edge_type, target_slug, edge_description)
# Edge description is a short contextual label

EDGES_TO_ADD = [
    # ═══ AREA 1: Breath testing validity ═══
    
    # C1: Breath tests validated vs not validated
    # Pimentel maintains lactulose breath testing preferred and valid;
    # Rome Foundation says breath tests not validated, SIBO-IBS link controversial
    ("claim-sibo-core-principles-unchanged-2006-2022", "challenged_by",
     "claim-role-sibo-pathogenesis-ibs-controversial-because-breath",
     "Pimentel asserts breath testing is clinically valid; Rome 2017 challenges this, noting breath tests have not been validated against an accepted gold standard"),
    
    # Reciprocal
    ("claim-role-sibo-pathogenesis-ibs-controversial-because-breath", "challenged_by",
     "claim-sibo-core-principles-unchanged-2006-2022",
     "Rome 2017's critique of breath test validation is challenged by Pimentel's 16-year clinical dataset showing lactulose breath testing correlating with treatment response"),
    
    # C2: Culture as gold standard (Pimentel vs AGA) 
    # Pimentel: aspirate culture is traditional gold standard (even if flawed)
    # AGA: limited understanding of normal SI microbiome, "definition lacks precision"
    ("claim-culturing-technique-considered-gold-standard-sibo-diagnosis", "challenged_by",
     "claim-aga-sibo2020-bpa-5-6",
     "Pimentel acknowledges culture limitations but maintains it as traditional gold standard; AGA argues limited understanding of normal small intestinal populations prevents any gold standard claim"),
    
    ("claim-aga-sibo2020-bpa-5-6", "challenged_by",
     "claim-culturing-technique-considered-gold-standard-sibo-diagnosis",
     "AGA's claim that limited understanding undermines SIBO definition is challenged by Pimentel's argument that breath test treatment-response correlation provides clinical validity despite microbiological uncertainty"),
    
    # ═══ AREA 2: Antibiotics-first vs root-cause approach ═══
    
    # C3: Antibiotics cornerstone vs limited usefulness
    # ACG/Pimentel: antibiotics cornerstone of SIBO treatment
    # Gottschall: antibiotics have limited usefulness for chronic intestinal disorders
    ("claim-antibiotics-cornerstone-sibo-treatment-rifaximin-best-evidence", "contradicts",
     "claim-simple-approach-minimizing-undesirable-activities-intestinal-microbes",
     "ACG guideline establishes antibiotics as cornerstone of SIBO treatment; Gottschall argues antibiotics have limited usefulness for chronic intestinal disorders — mutually exclusive treatment philosophies"),
    
    ("claim-simple-approach-minimizing-undesirable-activities-intestinal-microbes", "contradicts",
     "claim-antibiotics-cornerstone-sibo-treatment-rifaximin-best-evidence",
     "Gottschall's claim that antibiotics are of limited usefulness directly contradicts the ACG guideline's recommendation that antibiotics are the cornerstone of SIBO treatment"),
    
    # C4: Kill-microbes approach vs root cause
    # Campbell-McBride: killing microbes misses root cause (low stomach acid, damaged gut lining)
    ("claim-mainstream-approach-sibo-usual-try-kill-microbes", "challenged_by",
     "claim-antibiotics-cornerstone-sibo-treatment-rifaximin-best-evidence",
     "Campbell-McBride argues the antibiotic approach treats symptoms not cause; ACG guideline demonstrates 61-78% rifaximin efficacy supporting antibiotics as first-line treatment"),
    
    ("claim-antibiotics-cornerstone-sibo-treatment-rifaximin-best-evidence", "challenged_by",
     "claim-mainstream-approach-sibo-usual-try-kill-microbes",
     "ACG's antibiotic-first recommendation is challenged by Campbell-McBride's argument that low stomach acid and damaged gut lining are root causes that antibiotics cannot address"),
    
    # ═══ AREA 3: Diet alone vs combined therapy ═══
    
    # C5: Diet cures vs Diet alone insufficient
    # Gottschall: SCD corrects malabsorption and heals gut
    # Pimentel: Diet alone won't cure SIBO
    ("claim-specific-carbohydrate-diet-most-often-corrects-malabsorption", "contradicts",
     "claim-diet-alone-wont-cure-sibo-even-you",
     "Gottschall claims SCD corrects malabsorption and can heal chronic intestinal disorders through carbohydrate restriction alone; Pimentel asserts diet alone cannot cure SIBO — contradictory positions on dietary monotherapy efficacy"),
    
    ("claim-diet-alone-wont-cure-sibo-even-you", "contradicts",
     "claim-specific-carbohydrate-diet-most-often-corrects-malabsorption",
     "Pimentel's position that diet alone won't cure SIBO directly contradicts Gottschall's foundational SCD claim that carbohydrate-restrictive diet corrects malabsorption and enables healing"),
    
    # C6: SCD mechanism challenged
    # Gottschall's claim that SCD = elemental diet equivalent (LOW confidence)
    # We leave existing challenged_by edge but add supporting edges from other diet claims
    # Note: claim-specific-carbohydrate-diet-most-often-corrects-malabsorption already has:
    #   challenged_by → claim-pimentel-rezaie-survey-dietary-landscape-find-existing
    
    # ═══ AREA 4: IBS-SIBO nosology (SIBO prevalence and IBS status) ═══
    
    # C7: IBS is disease vs IBS is symptom-based FGID
    # Pimentel: IBS is a disease, not a syndrome
    # Rome Foundation: FGIDs are defined by symptom criteria, no structural pathology
    ("claim-notice-just-referred-ibs-disease-doesnt-ibs", "contradicts",
     "claim-functional-gastrointestinal-disorders-fgids-defined-symptom-based-diagnost",
     "Pimentel asserts IBS is a disease with organic etiology (SIBO), not a syndrome; Rome Foundation defines FGIDs including IBS as symptom-based disorders diagnosed in the absence of structural pathology — contradictory nosological frameworks"),
    
    ("claim-functional-gastrointestinal-disorders-fgids-defined-symptom-based-diagnost", "contradicts",
     "claim-notice-just-referred-ibs-disease-doesnt-ibs",
     "The Rome Foundation symptom-based FGID framework is directly contradicted by Pimentel's argument that IBS is a disease with a defined organic cause (SIBO) and should be reclassified"),
    
    # C8: 75% SIBO in IBS vs link is controversial
    ("claim-our-research-found-about-three-quarters-patients-many", "challenged_by",
     "claim-role-sibo-pathogenesis-ibs-controversial-because-breath",
     "Pimentel's 75% SIBO-in-IBS claim is challenged by Rome Foundation's finding that the SIBO-IBS link is controversial because the breath tests underlying positive studies have not been validated"),
    
    ("claim-role-sibo-pathogenesis-ibs-controversial-because-breath", "challenged_by",
     "claim-our-research-found-about-three-quarters-patients-many",
     "Rome 2017's skepticism about the SIBO-IBS link is challenged by Pimentel's finding that ~75% of IBS patients at a major referral center have positive breath tests suggesting SIBO, with treatment response supporting the link"),
    
    # C9: SIBO prevalence figures  
    # Pimentel 2022: 60-75%; earlier figure was 84%
    # Sarna 2021: 78% — splitting the difference
    ("claim-sibo-prevalence-78-percent-ibs-sarna", "extends",
     "claim-our-research-found-about-three-quarters-patients-many",
     "Sarna's 78% prevalence figure splits the difference between Pimentel's 2006 estimate (84%) and 2022 estimate (60-75%), reflecting the 2021 consensus"),
    
    # ═══ AREA 5: Probiotics — help vs harmful vs insufficient evidence ═══
    
    # C10: Probiotics efficacy in IBS vs insufficient evidence for SIBO
    ("claim-majority-trials-probiotics-ibs-show-degree-efficacy", "challenged_by",
     "claim-probiotics-insufficient-evidence-sibo-treatment-fmt-carries",
     "Rome Foundation's finding that ~75% of probiotic trials in IBS show efficacy is challenged by ACG 2020's conclusion that probiotics have insufficient evidence for SIBO and may cause harm in some patients"),
    
    ("claim-probiotics-insufficient-evidence-sibo-treatment-fmt-carries", "challenged_by",
     "claim-majority-trials-probiotics-ibs-show-degree-efficacy",
     "ACG 2020's recommendation against probiotics for SIBO is challenged by Rome 2017's evidence that ~75% of probiotic trials in IBS show some degree of efficacy, particularly B. infantis 35624"),
    
    # C11: Prebiotics feed unwanted bacteria (Pimentel) vs Prebiotics have potential (Rome)
    ("claim-you-sibo-taking-prebiotic-actually-provide-food", "challenged_by",
     "claim-prebiotics-synbiotics-theoretically-potential-treating-functional-gastroin",
     "Pimentel warns that prebiotics may feed overgrown bacteria in SIBO patients; Rome 2017 notes prebiotics/synbiotics theoretically have potential for FGIDs, though reliable data is lacking"),
    
    ("claim-prebiotics-synbiotics-theoretically-potential-treating-functional-gastroin", "challenged_by",
     "claim-you-sibo-taking-prebiotic-actually-provide-food",
     "Rome 2017's theoretical support for prebiotics is challenged by Pimentel's clinical observation that prebiotics cause more bloating in SIBO patients and may feed unwanted overgrowth"),
    
    # C12: No good/bad bacteria framing vs probiotic trials
    ("claim-theres-really-thing-good-bad-native-bacteria", "challenged_by",
     "claim-majority-trials-probiotics-ibs-show-degree-efficacy",
     "Pimentel's assertion that 'good bacteria' is a misnomer in the GI tract challenges the probiotic trial framework where specific strains are posited as beneficial"),
    
    # ═══ AREA 6: Terminology/framework debates ═══
    
    # C13: SIBO definition precise (ACG) vs lacks precision (AGA)
    ("claim-sibo-defined-presence-excessive-numbers-bacteria-small", "challenged_by",
     "claim-aga-sibo2020-bpa-1",
     "ACG defines SIBO as a clinical syndrome with specific criteria; AGA challenges this, finding the definition lacks precision and consistency"),
    
    ("claim-aga-sibo2020-bpa-1", "challenged_by",
     "claim-sibo-defined-presence-excessive-numbers-bacteria-small",
     "AGA's critique of SIBO definitional imprecision is challenged by ACG's operational clinical definition linking excessive small bowel bacteria to GI symptoms"),
    
    # C14: SIBO as dysbiosis (Chutkan) vs SIBO has specific pathophys (Pimentel)
    ("claim-sibo-really-just-another-term-dysbiosis-occurs", "challenged_by",
     "claim-sibo-defined-presence-excessive-numbers-bacteria-small",
     "Chutkan frames SIBO as simply another term for dysbiosis; ACG defines SIBO as a distinct clinical syndrome requiring specific diagnostic criteria and treatment — these are different conceptual frameworks"),
    
    # ═══ AREA 7: Dietary framework competition ═══
    
    # C15: Sarna and Pimentel alignment on treatment approach
    # Sarna presents three modalities as co-equal (pharma, herbal, elemental)
    # Pimentel shows treatment paradigm evolved through his Cedars-Sinai research
    ("claim-three-treatment-modalities-pharmaceutical-herbal-elemental", "extends",
     "claim-treatment-expectation-refinement-2006-2022",
     "Sarna's three-modality framework operationalizes Pimentel's treatment expectation refinement by offering patients structured alternatives when rifaximin monotherapy fails"),
    
    # C16: Diets work same way (Sarna) vs LFE is right balance (Pimentel)
    # These are more complementary than contradictory — Sarna explains mechanism, Pimentel selects
    ("claim-diets-work-same-reason-they-reduce-amount", "supports",
     "claim-diet-alone-wont-cure-sibo-even-you",
     "Sarna's observation that all SIBO diets work by reducing fermentable carbohydrates explains why Pimentel's LFE diet achieves symptom control without curing the underlying overgrowth"),
    
    # C17: Campbell-McBride GAPS approach supports Gottschall 
    ("claim-mainstream-approach-sibo-usual-try-kill-microbes", "supports",
     "claim-simple-approach-minimizing-undesirable-activities-intestinal-microbes",
     "Campbell-McBride extends Gottschall's antibiotic skepticism by identifying specific root causes (low stomach acid, damaged gut lining) that antibiotics fail to address"),
    
    # ═══ AREA 8: Guideline lineage / evolution ═══
    
    # C18: AGA BPA recommendations operationalize Rome's cautious approach
    ("claim-aga-sibo2020-bpa-7-9", "extends",
     "claim-report-provides-seven-general-clinical-recommendations-prioritize",
     "AGA 2020 operationalizes Rome 2017's research agenda by providing specific clinical recommendations while maintaining caution about SIBO testing"),
    
    # C19: ACG 2020 operationalizes breath testing suggestions from Rome
    ("claim-glucose-lactulose-hydrogen-breath-testing-suggested-sibo", "operationalizes",
     "claim-graded-recommendation-discussed-reference-standard-significant-limitations",
     "ACG 2020 suggests breath testing for SIBO diagnosis while acknowledging the limitations of the reference standard that Rome 2017 documented"),
    
    # C20: Pimentel acknowledges SIBO definitional issues
    ("claim-culturing-technique-considered-gold-standard-sibo-diagnosis", "supports",
     "claim-aga-sibo2020-bpa-5-6",
     "Pimentel's detailed critique of aspirate culture limitations supports AGA's observation that limited understanding of normal small intestinal populations impedes SIBO definition"),
]


# ─── Helper functions ───────────────────────────────────────────────

def read_claim(slug):
    """Read a claim file, return (content, filepath) or (None, None)."""
    filename = f"{slug}.md"
    filepath = os.path.join(CLAIMS_DIR, filename)
    if not os.path.exists(filepath):
        return None, None
    with open(filepath, 'r') as f:
        return f.read(), filepath

def write_claim(slug, content):
    """Write updated claim content."""
    filename = f"{slug}.md"
    filepath = os.path.join(CLAIMS_DIR, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    return filepath

def has_edge(content, edge_type, target_slug):
    """Check if an edge to target_slug already exists under the given edge_type heading."""
    # Find the Edges section
    edges_section = re.search(r'## Edges\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if not edges_section:
        return False
    section_text = edges_section.group(1)
    
    # Map edge type to heading
    heading_map = {
        'depends_on': '**Depends on:**',
        'supports': '**Supports:**',
        'extends': '**Extends:**',
        'operationalizes': '**Operationalizes:**',
        'challenged_by': '**Challenged by:**',
        'contradicts': '**Contradicts:**',
    }
    heading = heading_map.get(edge_type)
    if not heading:
        return False
    
    # Find the section between this heading and the next heading
    heading_pattern = re.escape(heading)
    pattern = rf'{heading_pattern}\n(.*?)(?=\n\*\*|$)'
    match = re.search(pattern, section_text, re.DOTALL)
    if not match:
        return False
    
    block = match.group(1)
    return f'[[{target_slug}' in block

def add_edge_to_claim(content, edge_type, target_slug, description):
    """Add an edge to a claim's Edges section. Returns modified content or None if edge already exists."""
    
    if has_edge(content, edge_type, target_slug):
        return None  # Already exists, skip
    
    heading_map = {
        'depends_on': '**Depends on:**',
        'supports': '**Supports:**',
        'extends': '**Extends:**',
        'operationalizes': '**Operationalizes:**',
        'challenged_by': '**Challenged by:**',
        'contradicts': '**Contradicts:**',
    }
    heading = heading_map.get(edge_type)
    if not heading:
        return None
    
    # Find the heading in the Edges section
    edges_section_match = re.search(r'(## Edges\n)', content)
    if not edges_section_match:
        return None
    
    # Find the specific heading within Edges
    heading_pattern = re.escape(heading)
    pattern = rf'({heading_pattern}\n)'
    match = re.search(pattern, content)
    if not match:
        return None
    
    insert_pos = match.end()
    
    # Build the edge line
    edge_line = f"- [[{target_slug}|{description}]]\n"
    
    new_content = content[:insert_pos] + edge_line + content[insert_pos:]
    return new_content


def main():
    print("=" * 70)
    print("PHASE 3c: Contradiction discovery — edge application")
    print("=" * 70)
    
    stats = {
        'added': 0,
        'skipped_duplicate': 0,
        'skipped_missing_source': 0,
        'skipped_missing_target': 0,
        'errors': 0,
        'by_type': defaultdict(int),
        'source_files_modified': set(),
    }
    
    # Group by source slug for reporting
    by_source = defaultdict(list)
    for src_slug, etype, tgt_slug, desc in EDGES_TO_ADD:
        by_source[src_slug].append((etype, tgt_slug, desc))
    
    for src_slug, edges in sorted(by_source.items()):
        content, filepath = read_claim(src_slug)
        if content is None:
            print(f"\n  MISSING SOURCE: {src_slug}")
            stats['skipped_missing_source'] += len(edges)
            continue
        
        modified = False
        for etype, tgt_slug, desc in edges:
            # Verify target exists
            tgt_content, _ = read_claim(tgt_slug)
            if tgt_content is None:
                print(f"  MISSING TARGET: {tgt_slug} (from {src_slug})")
                stats['skipped_missing_target'] += 1
                continue
            
            new_content = add_edge_to_claim(content, etype, tgt_slug, desc)
            if new_content is None:
                stats['skipped_duplicate'] += 1
                continue
            
            content = new_content
            stats['added'] += 1
            stats['by_type'][etype] += 1
            modified = True
        
        if modified:
            write_claim(src_slug, content)
            stats['source_files_modified'].add(src_slug)
            print(f"\n  ✓ {src_slug}")
            for etype, tgt_slug, desc in edges:
                print(f"    + {etype} → {tgt_slug}")
    
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"  Edges added:           {stats['added']}")
    print(f"  Skipped (duplicate):   {stats['skipped_duplicate']}")
    print(f"  Skipped (missing src): {stats['skipped_missing_source']}")
    print(f"  Skipped (missing tgt): {stats['skipped_missing_target']}")
    print(f"  Errors:                {stats['errors']}")
    print(f"  Files modified:        {len(stats['source_files_modified'])}")
    print(f"\n  By edge type:")
    for etype, count in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
        print(f"    {etype}: {count}")
    
    return 0 if stats['errors'] == 0 else 1

if __name__ == '__main__':
    exit(main())
