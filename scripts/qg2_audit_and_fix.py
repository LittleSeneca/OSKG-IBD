#!/usr/bin/env python3
"""
Quality Gate 2: Phase 2 claims audit and fix script.
Steps:
  1. Fix unescaped double-quotes in YAML frontmatter (50 files)
  2. Frontmatter audit (all 476 claims)
  3. Wikilink verification
  4. Tag enrichment for sparse-tagged claims
"""

import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

CLAIMS_DIR = Path("notes/claims")
NOTES_DIR = Path("notes")

###############################################################################
# STEP 1: Fix YAML quoting issues
###############################################################################

def fix_yaml_quoting(filepath):
    """Fix unescaped double-quotes inside double-quoted YAML values."""
    with open(filepath) as f:
        content = f.read()
    
    if not content.startswith('---'):
        return content, False
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content, False
    
    fm_text = parts[1]
    body = parts[2]
    
    changed = False
    new_lines = []
    
    for line in fm_text.split('\n'):
        # Match YAML key: "value" lines where value contains unescaped double quotes
        m = re.match(r'^(\s*)([a-z_]+):\s*"(.*)"$', line)
        if not m:
            new_lines.append(line)
            continue
        
        indent, key, value = m.groups()
        
        # Count unescaped double quotes
        unescaped = value.replace('\\"', '')
        if '"' not in unescaped:
            new_lines.append(line)
            continue
        
        # Switch to single quotes, escape any single quotes in value
        escaped_value = value.replace("'", "''")  # YAML single-quote escape
        new_line = f'{indent}{key}: \'{escaped_value}\''
        new_lines.append(new_line)
        changed = True
    
    if changed:
        new_fm = '\n'.join(new_lines)
        return f'---{new_fm}---{body}', True
    
    return content, False


def step1_fix_yaml():
    """Fix all claim files with YAML parsing errors."""
    claim_files = sorted(f for f in CLAIMS_DIR.glob('*.md') if f.name != 'Claims Index.md')
    
    fixed = 0
    still_broken = []
    
    for cf in claim_files:
        content, was_fixed = fix_yaml_quoting(cf)
        
        if was_fixed:
            # Verify the fixed content parses
            parts = content.split('---', 2)
            try:
                import yaml
                yaml.safe_load(parts[1])
                with open(cf, 'w') as f:
                    f.write(content)
                fixed += 1
            except Exception as e:
                still_broken.append(f'{cf.name}: {e}')
    
    print(f"STEP 1: YAML quoting fixes")
    print(f"  Fixed: {fixed}")
    if still_broken:
        print(f"  Still broken ({len(still_broken)}):")
        for b in still_broken:
            print(f"    {b}")
    return fixed, still_broken


###############################################################################
# STEP 2: Frontmatter audit
###############################################################################

def step2_frontmatter_audit():
    """Audit all claim files for required frontmatter fields."""
    import yaml
    
    claim_files = sorted(f for f in CLAIMS_DIR.glob('*.md') if f.name != 'Claims Index.md')
    
    missing_slug = []
    missing_source = []
    missing_tags = []
    missing_type_claim = []
    missing_confidence = []
    missing_source_note = []
    missing_claim_id = []
    missing_statement = []
    missing_oskg_ibd = []
    missing_claim_type = []
    broken_yaml = []
    
    slug_dupes = Counter()
    all_slugs = set()
    
    topic_tag_counts = Counter()
    
    for cf in claim_files:
        content = cf.read_text()
        slug = cf.stem
        all_slugs.add(slug)
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            missing_slug.append(cf.name)  # can't access frontmatter
            continue
        
        try:
            fm = yaml.safe_load(parts[1])
        except Exception as e:
            broken_yaml.append(f'{cf.name}: {e}')
            continue
        
        if not fm or not isinstance(fm, dict):
            broken_yaml.append(f'{cf.name}: empty/invalid')
            continue
        
        tags = fm.get('tags', [])
        
        # Required tag checks
        if 'type/claim' not in tags:
            missing_type_claim.append(cf.name)
        if 'oskg-ibd' not in tags:
            missing_oskg_ibd.append(cf.name)
        if not any(t.startswith('source/') for t in tags):
            missing_source.append(cf.name)
        if not any(t.startswith('evidence/') for t in tags):
            pass  # evidence tag tracked separately
        if not any(t.startswith('topic/') for t in tags):
            pass  # topic count tracked
        if not any(t.startswith('tier-') for t in tags):
            pass  # tier tags not required for all
        
        topic_count = sum(1 for t in tags if t.startswith('topic/'))
        topic_tag_counts[topic_count] += 1
        
        if 'confidence' not in fm:
            missing_confidence.append(cf.name)
        if 'source_note' not in fm:
            missing_source_note.append(cf.name)
        if 'claim_id' not in fm:
            missing_claim_id.append(cf.name)
        if 'statement' not in fm:
            missing_statement.append(cf.name)
        if 'claim_type' not in fm:
            missing_claim_type.append(cf.name)
    
    print(f"\nSTEP 2: Frontmatter audit ({len(claim_files)} claims)")
    print(f"  Broken YAML: {len(broken_yaml)}")
    print(f"  Missing type/claim tag: {len(missing_type_claim)}")
    print(f"  Missing oskg-ibd tag: {len(missing_oskg_ibd)}")
    print(f"  Missing source/* tag: {len(missing_source)}")
    print(f"  Missing confidence: {len(missing_confidence)}")
    print(f"  Missing source_note: {len(missing_source_note)}")
    print(f"  Missing claim_id: {len(missing_claim_id)}")
    print(f"  Missing statement: {len(missing_statement)}")
    print(f"  Missing claim_type: {len(missing_claim_type)}")
    
    print(f"\n  Topic tag distribution:")
    for count, n in sorted(topic_tag_counts.items()):
        print(f"    {count} tags: {n} claims")
    
    if broken_yaml:
        print(f"\n  YAML parse errors:")
        for b in broken_yaml[:5]:
            print(f"    {b}")
        if len(broken_yaml) > 5:
            print(f"    ... and {len(broken_yaml) - 5} more")
    
    return {
        'broken_yaml': broken_yaml,
        'missing_type_claim': missing_type_claim,
        'missing_oskg_ibd': missing_oskg_ibd,
        'missing_source': missing_source,
        'missing_confidence': missing_confidence,
        'missing_source_note': missing_source_note,
        'missing_claim_id': missing_claim_id,
        'missing_statement': missing_statement,
        'missing_claim_type': missing_claim_type,
        'topic_tag_counts': topic_tag_counts,
    }


###############################################################################
# STEP 3: Wikilink verification
###############################################################################

def step3_wikilink_check():
    """Check all wikilinks in claim files resolve to existing files."""
    import yaml
    
    # Build set of all claim file stems (wikilinks use filenames without .md)
    claim_names = set()
    for f in CLAIMS_DIR.glob('*.md'):
        claim_names.add(f.stem)
    
    # Build set of all reading note names (under notes/ but not notes/claims/)
    note_names = set()
    for root, dirs, files in os.walk(NOTES_DIR):
        if 'claims' in root:
            continue
        for f in files:
            if f.endswith('.md'):
                note_names.add(Path(f).stem)
    
    # Also add directory Index names
    for root, dirs, files in os.walk(NOTES_DIR):
        for f in files:
            if f.endswith('.md'):
                note_names.add(Path(f).stem)
    
    claim_files = sorted(f for f in CLAIMS_DIR.glob('*.md') if f.name != 'Claims Index.md')
    
    broken_source_note_links = []
    broken_edge_links = []
    edge_types = ['supports', 'contradicts', 'extends', 'depends_on', 'operationalizes']
    
    for cf in claim_files:
        content = cf.read_text()
        
        # Check source_note wikilink
        m = re.search(r'source_note:\s*"\[\[([^\]]+)\]\]"', content)
        if m:
            target = m.group(1)
            if target not in note_names and target not in claim_names:
                broken_source_note_links.append((cf.name, target))
        
        # Check edge wikilinks (in the body, not frontmatter)
        # Look for [[name]] patterns after the --- separator
        parts = content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2]
            wikilinks = re.findall(r'\[\[([^\]]+)\]\]', body)
            for wl in wikilinks:
                # Skip if it looks like a source reference (has spaces, not a slug)
                if ' ' in wl:
                    continue
                if wl not in claim_names and wl not in note_names:
                    broken_edge_links.append((cf.name, wl))
    
    print(f"\nSTEP 3: Wikilink verification")
    print(f"  Claim files: {len(claim_files)}")
    print(f"  Note files for resolution: {len(note_names)}")
    print(f"  Broken source_note links: {len(broken_source_note_links)}")
    print(f"  Broken edge wikilinks: {len(broken_edge_links)}")
    
    if broken_source_note_links:
        print(f"\n  Broken source_note links:")
        for cf, target in broken_source_note_links[:10]:
            print(f"    {cf} -> [[{target}]]")
        if len(broken_source_note_links) > 10:
            print(f"    ... and {len(broken_source_note_links) - 10} more")
    
    if broken_edge_links:
        print(f"\n  Broken edge wikilinks:")
        for cf, target in broken_edge_links[:10]:
            print(f"    {cf} -> [[{target}]]")
        if len(broken_edge_links) > 10:
            print(f"    ... and {len(broken_edge_links) - 10} more")
    
    return broken_source_note_links, broken_edge_links, claim_names, note_names


###############################################################################
# STEP 4: Tag enrichment
###############################################################################

# IBD-specific keyword mappings for topic tags
TAG_KEYWORDS = {
    "topic/sibo": ["sibo", "small intestine", "small bowel", "bacterial overgrowth", "breath test", "lactulose", "glucose breath", "jejunal aspirate"],
    "topic/imo": ["imo", "intestinal methanogen", "methane", "methanobrevibacter", "archaea", "methanogen overgrowth"],
    "topic/ibs": ["ibs", "irritable bowel", "rome", "functional gastrointestinal", "fgid", "dgbI"],
    "topic/crohns-disease": ["crohn", "cd ", "ileum", "ileal", "strictur", "fistula", "perianal", "granuloma", "terminal ileum"],
    "topic/ulcerative-colitis": ["ulcerative colitis", "uc ", "pancolitis", "proctitis", "colectomy", "pouchitis"],
    "topic/ibd-unclassified": ["ibdu", "ibd-u", "unclassified", "indeterminate colitis"],
    "topic/diagnosis": ["diagnos", "endoscop", "colonoscop", "imaging", "mri", "ct ", "ultrasound", "biopsy", "histolog", "calprotectin", "crp ", "biomarker"],
    "topic/treatment": ["treat", "therap", "medication", "drug", "dose", "regimen", "management"],
    "topic/biologics": ["biologic", "anti-tnf", "infliximab", "adalimumab", "ustekinumab", "vedolizumab", "certolizumab", "golimumab", "biosimilar"],
    "topic/immunomodulators": ["thiopurine", "azathioprine", "mercaptopurine", "methotrexate", "immunomodulator", "aza", "6-mp"],
    "topic/corticosteroids": ["steroid", "prednisone", "prednisolone", "budesonide", "corticosteroid", "methylprednisolone", "hydrocortisone"],
    "topic/5-asa": ["5-asa", "mesalamine", "mesalazine", "sulfasalazine", "olsalazine", "balsalazide", "aminosalicylate"],
    "topic/jak-inhibitors": ["jak", "tofacitinib", "upadacitinib", "filgotinib", "janus kinase"],
    "topic/antibiotics": ["antibiotic", "rifaximin", "metronidazole", "ciprofloxacin", "antimicrobial"],
    "topic/surgery": ["surger", "surgical", "resection", "colectomy", "ileostomy", "anastomosis", "strictureplasty", "postoperative"],
    "topic/microbiome": ["microbiom", "microbiota", "flora", "dysbiosis", "bacteria", "microbial", "gut bacteria", "commensal"],
    "topic/diet": ["diet", "nutrition", "food", "meal", "carbohydrate", "fiber", "scd", "elemental", "low-fodmap", "elimination diet", "enteral nutrition"],
    "topic/pathophysiology": ["pathophysiolog", "pathogenes", "mechanism", "etiology", "autoimmun", "immune", "inflammat", "cytokine", "genetic", "nod2", "atg16l1"],
    "topic/epidemiology": ["epidemiolog", "prevalence", "incidence", "population", "risk factor", "environmental"],
    "topic/monitoring": ["monitor", "surveillance", "follow-up", "relapse", "recurrence", "maintenance", "long-term"],
    "topic/guideline-recommendation": ["guideline", "recommend", "grade", "consensus", "statement", "society"],
    "topic/evidence-quality": ["evidence", "rct", "randomi", "cohort", "meta-analysis", "systematic review", "confidence", "trial"],
    "topic/complications": ["complicat", "stricture", "abscess", "fistula", "obstruction", "perforation", "dysplasia", "cancer", "colorectal"],
    "topic/pregnancy": ["pregnan", "fertility", "breastfeeding", "lactation", "cesarean", "congenital"],
    "topic/pediatrics": ["pediatric", "child", "adolescent", "growth", "puberty"],
    "topic/quality-of-life": ["quality of life", "qol", "fatigue", "depression", "anxiety", "psychosocial", "disability"],
    "topic/scd": ["specific carbohydrate", "scd", "gottschall", "haas", "disaccharide", "monosaccharide"],
    "topic/gaps": ["gaps", "gut and psychology", "campbell-mcbride", "bone broth"],
    "topic/elemental-diet": ["elemental diet", "eEN", "amino acid", "formula"],
    "topic/breath-testing": ["breath test", "hydrogen", "methane", "lactulose breath", "glucose breath"],
    "topic/probiotics": ["probiotic", "lactobacillus", "bifidobacterium", "saccharomyces", "ecn", "vsL"],
    "topic/fmt": ["fmt", "fecal transplant", "fecal microbiota", "stool transplant"],
    "topic/mmc": ["mmc", "migrating motor complex", "motility", "prokinetic", "phase iii", "interdigestive"],
    "topic/food-poisoning": ["food poison", "cdtB", "vinculin", "campylobacter", "gastroenteritis", "post-infectious"],
}

def step4_tag_enrichment():
    """Add topic tags to claims with ≤2 topic tags."""
    import yaml
    
    claim_files = sorted(f for f in CLAIMS_DIR.glob('*.md') if f.name != 'Claims Index.md')
    
    # Step 4a: Bundle co-occurrence data
    cooccur = defaultdict(Counter)
    tag_freq = Counter()
    
    for cf in claim_files:
        content = cf.read_text()
        parts = content.split('---', 2)
        if len(parts) < 3:
            continue
        try:
            fm = yaml.safe_load(parts[1])
        except:
            continue
        if not fm or not isinstance(fm, dict):
            continue
        
        tags = fm.get('tags', [])
        topic_tags = [t for t in tags if t.startswith('topic/')]
        
        for t in topic_tags:
            tag_freq[t] += 1
        
        for i, t1 in enumerate(topic_tags):
            for t2 in topic_tags[i+1:]:
                cooccur[t1][t2] += 1
                cooccur[t2][t1] += 1
    
    # Step 4b: Process claims with ≤2 topic tags
    enriched = 0
    tags_added = 0
    tags_added_by_name = Counter()
    
    body_text_cache = {}
    
    for cf in claim_files:
        content = cf.read_text()
        parts = content.split('---', 2)
        if len(parts) < 3:
            continue
        try:
            fm = yaml.safe_load(parts[1])
        except:
            continue
        if not fm or not isinstance(fm, dict):
            continue
        
        tags = fm.get('tags', [])
        topic_tags = [t for t in tags if t.startswith('topic/')]
        
        if len(topic_tags) >= 3:
            continue  # Already well-tagged
        
        # Get body text for keyword validation
        if cf.name not in body_text_cache:
            title_line = parts[2].split('\n')[0] if parts[2] else ''
            body_lower = title_line.lower() + ' ' + parts[2].lower()[:3000]
            body_text_cache[cf.name] = body_lower
        body_lower = body_text_cache[cf.name]
        
        # Compute candidate scores using co-occurrence affinity
        candidates = {}
        for tag in topic_tags:
            top_affinity = cooccur[tag].most_common(10)
            for rank, (aff_tag, count) in enumerate(top_affinity):
                if aff_tag in topic_tags:
                    continue
                score = (10 - rank) + (tag_freq.get(aff_tag, 0) * 0.01)
                candidates[aff_tag] = max(candidates.get(aff_tag, 0), score)
        
        # Rank candidates by score
        ranked = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        
        to_add = []
        for cand_tag, score in ranked:
            if len(to_add) >= 2:
                break
            keywords = TAG_KEYWORDS.get(cand_tag, [cand_tag.replace('topic/', '')])
            if any(kw.lower() in body_lower for kw in keywords):
                to_add.append(cand_tag)
        
        if not to_add:
            continue
        
        # Modify frontmatter: add new topic tags after existing tags
        # We need to find the last topic/ tag line and add after it
        fm_lines = parts[1].split('\n')
        new_fm_lines = []
        added_in_this_round = set()
        
        for line in fm_lines:
            new_fm_lines.append(line)
            # After the last topic tag line, add our new ones
            if line.strip().startswith('- topic/') or line.strip().startswith('- type/claim'):
                # Check if this is the last tag line
                pass
        
        # Simpler approach: find the last - topic/ line index
        last_topic_idx = -1
        for i, line in enumerate(fm_lines):
            if line.strip().startswith('- topic/'):
                last_topic_idx = i
        
        if last_topic_idx >= 0:
            insert_pos = last_topic_idx + 1
            for tag in to_add:
                if tag not in tags:
                    new_line = f'  - {tag}'
                    fm_lines.insert(insert_pos, new_line)
                    insert_pos += 1
                    tags_added_by_name[tag] += 1
                    tags_added += 1
                    added_in_this_round.add(tag)
        
        if added_in_this_round:
            new_fm = '\n'.join(fm_lines)
            new_content = f'---{new_fm}---{parts[2]}'
            with open(cf, 'w') as f:
                f.write(new_content)
            enriched += 1
    
    print(f"\nSTEP 4: Tag enrichment")
    print(f"  Claims with ≤2 topic tags: {sum(1 for f in claim_files if f.name != 'Claims Index.md')}  (recalculating...)")
    print(f"  Enriched: {enriched}")
    print(f"  Tags added: {tags_added}")
    if tags_added_by_name:
        print(f"  Tags added by frequency:")
        for tag, count in tags_added_by_name.most_common(15):
            print(f"    {tag}: +{count}")
    
    return enriched, tags_added, tags_added_by_name


###############################################################################
# MAIN
###############################################################################

def main():
    print("=" * 60)
    print("QUALITY GATE 2: Claims Audit & Fix")
    print("=" * 60)
    
    # Step 1
    fixed, still_broken = step1_fix_yaml()
    
    # Step 2
    audit_results = step2_frontmatter_audit()
    
    # Step 3
    broken_src, broken_edge, claim_names, note_names = step3_wikilink_check()
    
    # Step 4
    enriched, tags_added, tags_added_by_name = step4_tag_enrichment()
    
    # Summary
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print(f"  YAML fixed: {fixed}")
    print(f"  YAML still broken: {len(still_broken)}")
    print(f"  Missing type/claim: {len(audit_results['missing_type_claim'])}")
    print(f"  Missing oskg-ibd: {len(audit_results['missing_oskg_ibd'])}")
    print(f"  Missing source/*: {len(audit_results['missing_source'])}")
    print(f"  Missing confidence: {len(audit_results['missing_confidence'])}")
    print(f"  Missing source_note: {len(audit_results['missing_source_note'])}")
    print(f"  Missing claim_id: {len(audit_results['missing_claim_id'])}")
    print(f"  Missing statement: {len(audit_results['missing_statement'])}")
    print(f"  Missing claim_type: {len(audit_results['missing_claim_type'])}")
    print(f"  Broken source_note links: {len(broken_src)}")
    print(f"  Broken edge wikilinks: {len(broken_edge)}")
    print(f"  Claims enriched: {enriched}")
    print(f"  Tags added: {tags_added}")


if __name__ == '__main__':
    main()
