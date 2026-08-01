#!/usr/bin/env python3
"""
Phase 3c — Batch 2: Additional contradiction and alignment edges.
Focus: Sarna-Pimentel bridge, IBS blood test vs Rome criteria,
       elemental diet consensus, and treatment philosophy nuance.
"""

import os
import re
from collections import defaultdict

CLAIMS_DIR = os.path.expanduser("~/Projects/Personal/OSKG-IBD/notes/claims")

EDGES_BATCH2 = [
    # ── Sarna-Pimentel alignment: bridge the two camps ──
    ("claim-sarna-pimentel-alignment-differences", "supports",
     "claim-sibo-core-principles-unchanged-2006-2022",
     "Sarna's independent patient-education framework validates the stability of Pimentel's core SIBO principles (MMC, food poisoning etiology, IBS-SIBO connection) across 16 years"),

    ("claim-sarna-pimentel-alignment-differences", "extends",
     "claim-treatment-expectation-refinement-2006-2022",
     "Sarna's 2021 protocol refines Pimentel's treatment expectation framework by adding naturopathic options (Iberogast, ginger, magnesium) and structured relapse management"),

    # ── Sarna adopts Pimentel's three-gas model ──
    ("claim-sarna-pimentel-alignment-differences", "depends_on",
     "claim-three-gas-model-imo-terminology-evolution",
     "Sarna's SIBO education framework depends on Pimentel's three-gas model and IMO terminology evolution (2006-2022) for its diagnostic structure"),

    # ── IBS blood test (Pimentel) vs Rome symptom-based criteria ──
    # Pimentel claims >90% diagnostic certainty via blood test
    ("claim-based-validation-study-almost-3000-patients-proved", "challenged_by",
     "claim-functional-gastrointestinal-disorders-fgids-defined-symptom-based-diagnost",
     "Pimentel's claim of >90% IBS diagnostic certainty via blood test (anti-CdtB/anti-vinculin) challenges Rome Foundation's symptom-based FGID diagnostic framework, which does not incorporate biomarkers"),

    ("claim-functional-gastrointestinal-disorders-fgids-defined-symptom-based-diagnost", "challenged_by",
     "claim-based-validation-study-almost-3000-patients-proved",
     "Rome Foundation's symptom-based FGID framework is challenged by Pimentel's validation of a blood test with >90% diagnostic certainty for IBS, suggesting biomarkers may replace symptom-based criteria"),

    # ── SIBO as epiphenomenon: ACG vs Pimentel's IBS-disease framing ──
    # ACG says SIBO is almost always an epiphenomenon
    # Pimentel says IBS IS SIBO in the majority
    ("claim-sibo-almost-always-epiphenomenon-underlying-cause-motility", "extends",
     "claim-notice-just-referred-ibs-disease-doesnt-ibs",
     "ACG's clinical framing that SIBO is almost always an epiphenomenon of an underlying cause extends Pimentel's argument that IBS should be reclassified from syndrome to disease: both recognize organic etiology"),

    # ── Elemental diet consensus ──
    # Both Pimentel and Sarna cite >80% elemental diet efficacy
    ("claim-our-study-published-years-ago-14-day-elemental", "supports",
     "claim-three-treatment-modalities-pharmaceutical-herbal-elemental",
     "Pimentel's 2007 elemental diet study (>80% efficacy) provides the evidence base for Sarna's inclusion of elemental diet as a co-equal treatment modality"),

    # ── SIBO treatment cycles: Sarna extends Pimentel's model ──
    ("claim-sibo-relapse-management-multiple-treatment-rounds", "extends",
     "claim-treatment-expectation-refinement-2006-2022",
     "Sarna's structured relapse management protocol (retesting at 2-4 weeks, rotating modalities) operationalizes Pimentel's observation that ~70% of patients relapse after initial treatment"),

    # ── Gottschall SCD mechanism vs modern microbiome science ──
    # Gottschall: SCD = elemental diet biochemically (LOW confidence)
    # Pimentel: SCD "ineffective for IBS" in clinical trial
    ("claim-pimentel-rezaie-survey-dietary-landscape-find-existing", "contradicts",
     "claim-specific-carbohydrate-diet-most-often-corrects-malabsorption",
     "Pimentel cites a clinical trial finding SCD did not relieve IBS symptoms vs low-FODMAP; Gottschall claims SCD corrects malabsorption and heals through monosaccharide provision — contradictory evidence about SCD efficacy"),

    # ── Campbell-McBride GAPS vs modern SIBO treatment ──
    ("claim-mainstream-approach-sibo-usual-try-kill-microbes", "challenged_by",
     "claim-prokinetic-optimization-erythromycin-prucalopride",
     "Campbell-McBride's framing of SIBO treatment as simply 'killing microbes' overlooks the prokinetic component of modern protocols that addresses the motility defect (the root cause in Pimentel's model)"),

    # ── Probiotics: Campbell-McBride GAPS uses them vs ACG says no evidence ──
    ("claim-most-potent-probiotics-use-gaps-nutritional-protocol", "challenged_by",
     "claim-probiotics-insufficient-evidence-sibo-treatment-fmt-carries",
     "Campbell-McBride recommends specific probiotics as part of GAPS protocol; ACG 2020 finds insufficient evidence for probiotics in SIBO treatment and cites a study suggesting they may cause harm"),

    # ── Rome 2017 acknowledges FGID-IBS bridge ──
    ("claim-possible-ibs-ibd-coexist-higher-expected-frequency", "supports",
     "claim-notice-just-referred-ibs-disease-doesnt-ibs",
     "Rome Foundation's 2017 acknowledgment that IBS and IBD may exist on a continuum supports Pimentel's argument that IBS has an organic, not merely functional, basis"),

    # ── LFE meal spacing (Pimentel) aligns with Sarna ──
    ("claim-cant-emphasize-enough-importance-keeping-gastrointestinal-tracts", "supports",
     "claim-space-your-meals-four-five-hours-apart",
     "Pimentel's emphasis on MMC cleaning waves during fasting provides the mechanistic foundation for Sarna's meal-spacing recommendation (4-5 hours between meals, no snacking)"),
]


def read_claim(slug):
    filename = f"{slug}.md"
    filepath = os.path.join(CLAIMS_DIR, filename)
    if not os.path.exists(filepath):
        return None, None
    with open(filepath, 'r') as f:
        return f.read(), filepath

def write_claim(slug, content):
    filename = f"{slug}.md"
    filepath = os.path.join(CLAIMS_DIR, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    return filepath

def has_edge(content, edge_type, target_slug):
    edges_section = re.search(r'## Edges\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if not edges_section:
        return False
    section_text = edges_section.group(1)
    
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
    
    heading_pattern = re.escape(heading)
    pattern = rf'{heading_pattern}\n(.*?)(?=\n\*\*|$)'
    match = re.search(pattern, section_text, re.DOTALL)
    if not match:
        return False
    
    return f'[[{target_slug}' in match.group(1)

def add_edge_to_claim(content, edge_type, target_slug, description):
    if has_edge(content, edge_type, target_slug):
        return None
    
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
    
    edges_section_match = re.search(r'(## Edges\n)', content)
    if not edges_section_match:
        return None
    
    heading_pattern = re.escape(heading)
    pattern = rf'({heading_pattern}\n)'
    match = re.search(pattern, content)
    if not match:
        return None
    
    insert_pos = match.end()
    edge_line = f"- [[{target_slug}|{description}]]\n"
    return content[:insert_pos] + edge_line + content[insert_pos:]


def main():
    print("=" * 70)
    print("PHASE 3c BATCH 2: Additional contradiction and alignment edges")
    print("=" * 70)
    
    stats = {
        'added': 0,
        'skipped_duplicate': 0,
        'skipped_missing_source': 0,
        'skipped_missing_target': 0,
        'by_type': defaultdict(int),
        'source_files_modified': set(),
    }
    
    by_source = defaultdict(list)
    for src_slug, etype, tgt_slug, desc in EDGES_BATCH2:
        by_source[src_slug].append((etype, tgt_slug, desc))
    
    for src_slug, edges in sorted(by_source.items()):
        content, filepath = read_claim(src_slug)
        if content is None:
            print(f"\n  MISSING SOURCE: {src_slug}")
            stats['skipped_missing_source'] += len(edges)
            continue
        
        modified = False
        for etype, tgt_slug, desc in edges:
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
            print(f"\n  + {src_slug}")
            for etype, tgt_slug, desc in edges:
                print(f"    {etype} → {tgt_slug}")
    
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"  Edges added:           {stats['added']}")
    print(f"  Skipped (duplicate):   {stats['skipped_duplicate']}")
    print(f"  Skipped (missing src): {stats['skipped_missing_source']}")
    print(f"  Skipped (missing tgt): {stats['skipped_missing_target']}")
    print(f"  Files modified:        {len(stats['source_files_modified'])}")
    print(f"\n  By edge type:")
    for etype, count in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
        print(f"    {etype}: {count}")
    
    return 0

if __name__ == '__main__':
    exit(main())
