#!/usr/bin/env python3
"""Generate smart candidate pairs for microbiome/nutrition/diagnosis/pathophysiology orphans."""
import os, re, json, sys
from collections import defaultdict

CLAIMS_DIR = "notes/claims"

subtopics = {
    'sibo_diagnosis': r'\bdiagnos\b|\bdefinition\b|\btest\b|\bbreath\b|\bculture\b|\baspirate\b|\bgold.standard\b|\bcriteria\b',
    'sibo_treatment': r'\btreat|\bantibiotic|\brifaximin|\bherbal|\belemental|\bprokinetic|\bmanagement\b|\bpillar\b',
    'sibo_pathogenesis': r'\bpathogen|\bmechanism|\bfood.poisoning|\bautoimmun|\bmigrating.motor|\bMMC|\bclearance\b',
    'microbiome_composition': r'\bmicrobiome.composition|\bdysbiosis|\bdiversity|\bspecies\b|\bphyla\b|\bbacteria|\bmicrobial\b',
    'microbiome_therapy': r'\bprobiotic|\bFMT|\btransplant|\bprebiotic|\brestore\b|\brewild\b',
    'diet_intervention': r'\bdiet\b|\bSCD\b|\bFODMAP|\bcarbohydrate|\belemental.diet|\bpaleo\b|\bAIP\b|\blow.fermentation\b',
    'ibs_overlap': r'\bIBS\b|\birritable.bowel|\boverlap|\bconstipation|\bdiarrhea|\bbloating\b',
    'ibd_microbiome': r'\bIBD\b|\binflammatory.bowel|\bcrohn|\bcolitis\b',
}

def get_subtopics(text):
    text_lower = text.lower()
    matches = set()
    for label, pattern in subtopics.items():
        if re.search(pattern, text_lower, re.I):
            matches.add(label)
    return matches

def main():
    # Load all cross-domain orphans
    orphans = []
    for fname in os.listdir(CLAIMS_DIR):
        if not fname.endswith('.md') or not fname.startswith('claim-'):
            continue
        slug = fname.replace('.md', '')
        path = os.path.join(CLAIMS_DIR, fname)
        with open(path) as f:
            content = f.read()
        
        fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        fm_text = fm_match.group(1) if fm_match else ''
        
        domain = 'unknown'
        claim_id = ''
        statement = ''
        source_note = ''
        for line in fm_text.split('\n'):
            line = line.strip()
            if line.startswith('- domain/'):
                domain = line[2:].strip().strip('"').strip("'")
            elif line.startswith('claim_id:'):
                claim_id = line.split(':', 1)[1].strip().strip('"').strip("'")
            elif line.startswith('statement:'):
                statement = line.split(':', 1)[1].strip().strip('"').strip("'")
            elif line.startswith('source_note:'):
                raw = line.split(':', 1)[1].strip().strip('"').strip("'")
                source_note = raw.replace('[[', '').replace(']]', '')
        
        ec = 0
        em = re.search(r'## Edges\n(.*?)(?=\n##|\n---|\Z)', content, re.DOTALL)
        if em:
            for l in em.group(1).split('\n'):
                if l.strip().startswith('- [['):
                    ec += 1
        
        if ec > 0:
            continue
        
        target_domains = ['domain/microbiome', 'domain/nutrition', 'domain/diagnosis', 'domain/pathophysiology']
        if domain not in target_domains:
            continue
        
        claim_match = re.search(r'## The Claim\n\n(.*?)(?:\n##|\n---)', content, re.DOTALL)
        full_claim = claim_match.group(1).strip()[:500] if claim_match else statement[:500]
        
        ev_match = re.search(r'## Evidence\n\n(.*?)(?:\n##|\n---)', content, re.DOTALL)
        evidence = ev_match.group(1).strip()[:300] if ev_match else ''
        
        orphans.append({
            'slug': slug, 'claim_id': claim_id, 'statement': statement,
            'full_claim': full_claim, 'evidence': evidence,
            'source_note': source_note, 'domain': domain,
        })
    
    print(f"Cross-domain orphans: {len(orphans)}")
    
    # Classify
    for c in orphans:
        c['subtopics'] = get_subtopics(c['full_claim'] + ' ' + c['statement'])
    
    # Generate smart pairs
    pairs = []
    seen = set()
    for i, ca in enumerate(orphans):
        for j, cb in enumerate(orphans):
            if i >= j:
                continue
            if ca['source_note'] == cb['source_note']:
                continue
            
            ca_book = ca['source_note'].split(' - ')[0] if ' - ' in ca['source_note'] else ca['source_note']
            cb_book = cb['source_note'].split(' - ')[0] if ' - ' in cb['source_note'] else cb['source_note']
            if ca_book == cb_book:
                continue
            
            shared = ca['subtopics'] & cb['subtopics']
            if not shared:
                continue
            
            pair_key = tuple(sorted([ca['slug'], cb['slug']]))
            if pair_key in seen:
                continue
            seen.add(pair_key)
            
            pairs.append({
                'claim_a': {
                    'slug': ca['slug'], 'claim_id': ca['claim_id'],
                    'statement': ca['statement'], 'full_claim': ca['full_claim'][:400],
                    'evidence': ca['evidence'], 'source_note': ca['source_note'],
                    'domain': ca['domain'],
                },
                'claim_b': {
                    'slug': cb['slug'], 'claim_id': cb['claim_id'],
                    'statement': cb['statement'], 'full_claim': cb['full_claim'][:400],
                    'evidence': cb['evidence'], 'source_note': cb['source_note'],
                    'domain': cb['domain'],
                },
                'shared_subtopics': list(shared),
            })
    
    print(f"Smart pairs (different source/book, same subtopic): {len(pairs)}")
    
    batch_size = 30
    batches = [pairs[i:i+batch_size] for i in range(0, len(pairs), batch_size)]
    print(f"Batches: {len(batches)}")
    
    outdir = "scripts/manifests/phase3b_candidates"
    for i, batch in enumerate(batches[:5]):
        out_path = f"{outdir}/candidates_crossdomain_batch{i+1:02d}.json"
        with open(out_path, 'w') as f:
            json.dump({
                'batch_id': f'crossdomain-batch{i+1:02d}',
                'pair_count': len(batch),
                'pairs': batch,
            }, f, indent=2)
        print(f"  Wrote {out_path}: {len(batch)} pairs")

if __name__ == '__main__':
    main()
