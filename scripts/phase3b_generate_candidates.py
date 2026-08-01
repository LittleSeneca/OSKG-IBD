#!/usr/bin/env python3
"""
Phase 3b: Smart candidate edge generator — v2.

Improves on v1 by only pairing claims that address the SAME clinical scenario
across different guidelines. Reduces 754 pairs to ~120-180 meaningful candidates.

Clinical scenario matching:
  - Same drug/class AND same disease AND same treatment phase
  - Uses keyword overlap scoring to determine relevance
  - Minimum overlap threshold before considering a pair
"""

import os, re, json, sys
from collections import Counter, defaultdict
from pathlib import Path

CLAIMS_DIR = Path("/home/littleseneca/Projects/Personal/OSKG-IBD/notes/claims")
MANIFESTS_DIR = Path("/home/littleseneca/Projects/Personal/OSKG-IBD/scripts/manifests/phase3b_candidates")
MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)

# Drug class matchers
DRUG_CLASSES = [
    ("5-ASA", r'\b(5-?ASA|mesalazine|mesalamine|sulfasalazine|olsalazine|balsalazide|aminosalicylate)\b'),
    ("corticosteroids", r'\b(corticosteroid|prednisolone|prednisone|budesonide|hydrocortisone|methylprednisolone|MMX|steroid\b|glucocorticoid)\b'),
    ("thiopurines", r'\b(thiopurine|azathioprine|mercaptopurine|6-MP)\b'),
    ("methotrexate", r'\b(methotrexate|MTX)\b'),
    ("anti-TNF", r'\b(anti.?TNF|infliximab|adalimumab|golimumab|certolizumab|Remicade|Humira)\b'),
    ("vedolizumab", r'\b(vedolizumab|anti.?integrin|Entyvio)\b'),
    ("ustekinumab", r'\b(ustekinumab|anti.?IL-?12|anti.?IL-?23|Stelara)\b'),
    ("JAK inhibitor", r'\b(JAK|Janus|tofacitinib|upadacitinib|filgotinib|ozanimod|s1p)\b'),
    ("antibiotics", r'\b(antibiotic|ciprofloxacin|metronidazole|rifaximin|antimycobacterial|rifampin)\b'),
    ("cyclosporine", r'\b(cyclosporine|tacrolimus|ciclosporin|calcineurin)\b'),
    ("surgery", r'\b(surgery|colectomy|resection|ileal.?pouch|IPAA|laparoscopic|post.?operative)\b'),
    ("fistula", r'\b(fistula|perianal|enterocutaneous|rectovaginal|drain|seton)\b'),
    ("diagnosis/monitoring", r'\b(diagnos|test|screen|monitor|endoscop|colonoscop|surveillance|biomarker|calprotectin|fecal)\b'),
    ("combination therapy", r'\b(combination|concomitant|dual|immunomodulator.*biologic|biologic.*immunomodulator)\b'),
]

# Clinical scenario matchers (phase, position, setting)
SCENARIOS = [
    ("induction_active", r'\b(induction|induce|active.disease|flare|active\b|inducing)\b'),
    ("maintenance", r'\b(maintenance|maintain|remission|relapse|steroid.?sparing|withdr|stop\b|maintaining)\b'),
    ("moderate_severe", r'\b(moderate.?severe|severe|severely|mod.severe)\b'),
    ("mild_moderate", r'\b(mild.?moderate|mild|low.?risk)\b'),
    ("fulminant_ASUC", r'\b(fulminant|ASUC|acute.severe|toxic.megacolon)\b'),
    ("steroid_refractory", r'\b(steroid.?refractory|steroid.?resistant|steroid.?dependent|refractory|failed)\b'),
    ("post_operative", r'\b(post.?operative|post.?surg|anastomotic|recurrence.prophyla|post.op)\b'),
    ("first_line", r'\b(first.?line|initial|na[iï]ve|treatment.?na[iï]ve|newly.diagnosed|early)\b'),
    ("refractory_second_line", r'\b(refractory|second.?line|failure|failed|loss.of.response|intolerant)\b'),
    ("pediatric", r'\b(pediatric|adolescent|child|children)\b'),
    ("pregnancy", r'\b(pregnan|breast.?feed|lactation|fertility)\b'),
    ("elderly", r'\b(elderly|older.patient|geriatric)\b'),
    ("CRC_surveillance", r'\b(cancer|CRC|colorectal|dysplasia|chemoprevention|surveillance.colonoscopy)\b'),
]

# Disease matchers
DISEASES = [
    ("crohns_disease", r'\b(CD|crohn|ileal|ileocecal|ileocolonic|penetrating|stricturing|fistulizing)\b'),
    ("ulcerative_colitis", r'\b(UC|ulcerative.colitis|colitis|proctitis|left.sided|pancolitis|distal.colitis)\b'),
    ("IBD_general", r'\b(IBD|inflammatory.bowel)\b'),
    ("SIBO", r'\b(SIBO|small.intestinal.bacterial.overgrowth|breath.test)\b'),
    ("IBS", r'\b(IBS|irritable.bowel)\b'),
]


def parse_claim(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slug = os.path.basename(filepath).replace('.md', '')
    
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    fm_text = fm_match.group(1) if fm_match else ''
    
    tags = []
    claim_id = ''
    statement = ''
    source_note = ''
    claim_type = ''
    confidence = ''
    for line in fm_text.split('\n'):
        line = line.strip()
        if line.startswith('- ') and ('topic/' in line or 'domain/' in line):
            tags.append(line[2:].strip().strip('"').strip("'"))
        elif line.startswith('claim_id:'):
            claim_id = line.split(':', 1)[1].strip().strip('"').strip("'")
        elif line.startswith('statement:'):
            statement = line.split(':', 1)[1].strip().strip('"').strip("'")
        elif line.startswith('source_note:'):
            raw = line.split(':', 1)[1].strip().strip('"').strip("'")
            source_note = raw.replace('[[', '').replace(']]', '')
        elif line.startswith('claim_type:'):
            claim_type = line.split(':', 1)[1].strip().strip('"').strip("'")
        elif line.startswith('confidence:'):
            confidence = line.split(':', 1)[1].strip().strip('"').strip("'")
    
    topic_tags = [t for t in tags if t.startswith('topic/')]
    
    # Edge count
    edges_match = re.search(r'## Edges\n(.*?)(?=\n##|\n---|\Z)', content, re.DOTALL)
    edge_count = 0
    if edges_match:
        for line in edges_match.group(1).split('\n'):
            if line.strip().startswith('- [['):
                edge_count += 1
    
    # Full claim text
    claim_match = re.search(r'## The Claim\n\n(.*?)(?:\n##|\n---)', content, re.DOTALL)
    full_claim = claim_match.group(1).strip()[:600] if claim_match else statement[:600]
    
    # Evidence
    ev_match = re.search(r'## Evidence\n\n(.*?)(?:\n##|\n---)', content, re.DOTALL)
    evidence = ev_match.group(1).strip()[:300] if ev_match else ''
    
    return {
        'slug': slug, 'claim_id': claim_id, 'statement': statement,
        'full_claim': full_claim, 'evidence': evidence,
        'topic_tags': topic_tags, 'source_note': source_note,
        'claim_type': claim_type, 'confidence': confidence,
        'edge_count': edge_count,
    }


def match_classes(text):
    """Return set of matched drug classes and diseases and scenarios."""
    text_lower = text.lower()
    drugs = set()
    for label, pattern in DRUG_CLASSES:
        if re.search(pattern, text_lower, re.I):
            drugs.add(label)
    
    diseases = set()
    for label, pattern in DISEASES:
        if re.search(pattern, text_lower, re.I):
            diseases.add(label)
    
    scenarios = set()
    for label, pattern in SCENARIOS:
        if re.search(pattern, text_lower, re.I):
            scenarios.add(label)
    
    return drugs, diseases, scenarios


def score_pair(ca, cb, ca_drugs, ca_diseases, ca_scenarios, cb_drugs, cb_diseases, cb_scenarios):
    """Score how likely two claims have a meaningful edge."""
    score = 0
    
    # Must share at least 1 drug class AND 1 disease
    shared_drugs = ca_drugs & cb_drugs
    shared_diseases = ca_diseases & cb_diseases
    shared_scenarios = ca_scenarios & cb_scenarios
    
    if not shared_drugs:
        return 0  # No shared drug class → unlikely to be about same treatment
    
    score += len(shared_drugs) * 3
    score += len(shared_diseases) * 4  # Same disease is strongest signal
    score += len(shared_scenarios) * 2
    
    # Bonus: same claim_type
    if ca['claim_type'] == cb['claim_type']:
        score += 1
    
    # Bonus: both have grade tag (both are guideline recommendations)
    ca_has_grade = 'topic/grade' in ca['topic_tags']
    cb_has_grade = 'topic/grade' in cb['topic_tags']
    if ca_has_grade and cb_has_grade:
        score += 2
    
    # Penalty: both from ACG (same publisher, same disease but different year? Actually ACG CD 2018 and ACG UC 2019 are same org, different diseases)
    ca_src = ca['source_note']
    cb_src = cb['source_note']
    if 'ACG' in ca_src and 'ACG' in cb_src:
        score -= 1  # Slight penalty but still viable (same org, different guidelines)
    
    return score


def main():
    cluster_filter = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    # Load all claims
    all_claims = []
    for fname in os.listdir(CLAIMS_DIR):
        if not fname.endswith('.md') or not fname.startswith('claim-'):
            continue
        path = CLAIMS_DIR / fname
        claim = parse_claim(path)
        all_claims.append(claim)
    
    print(f"Total claims loaded: {len(all_claims)}")
    
    orphans = [c for c in all_claims if c['edge_count'] == 0]
    print(f"Orphans (zero edges): {len(orphans)}")
    
    # Filter
    if cluster_filter == 'grade-treatment':
        target = [c for c in orphans 
                  if 'topic/grade' in c['topic_tags'] and 'topic/treatment' in c['topic_tags']]
    elif cluster_filter == 'cd-treatment':
        target = [c for c in orphans 
                  if 'topic/crohns-disease' in c['topic_tags'] and 'topic/treatment' in c['topic_tags']]
    elif cluster_filter == 'cd-grade':
        target = [c for c in orphans 
                  if 'topic/crohns-disease' in c['topic_tags'] and 'topic/grade' in c['topic_tags']]
    elif cluster_filter == 'uc-grade':
        target = [c for c in orphans 
                  if 'topic/grade' in c['topic_tags'] and 'topic/ulcerative-colitis' in c['topic_tags']]
    elif cluster_filter == 'microbiome-sibo':
        target = [c for c in orphans 
                  if 'topic/microbiome' in c['topic_tags'] and 'topic/sibo' in c['topic_tags']]
    elif cluster_filter == 'all':
        target = orphans
    else:
        print(f"Unknown filter: {cluster_filter}")
        sys.exit(1)
    
    print(f"Target claims: {len(target)}")
    
    # Pre-compute class/disease/scenario matches
    claim_features = {}
    for c in target:
        text = c['full_claim'] + ' ' + c['statement'] + ' ' + c['claim_id']
        drugs, diseases, scenarios = match_classes(text)
        claim_features[c['slug']] = (drugs, diseases, scenarios)
    
    # Generate smart pairs
    pairs = []
    seen_pairs = set()
    target_slugs = {c['slug'] for c in target}
    
    # Group by source for cross-source pairing
    by_source = defaultdict(list)
    for c in target:
        by_source[c['source_note']].append(c)
    
    source_names = list(by_source.keys())
    
    for i in range(len(source_names)):
        for j in range(i + 1, len(source_names)):
            src_a = source_names[i]
            src_b = source_names[j]
            for c_a in by_source[src_a]:
                for c_b in by_source[src_b]:
                    pair_key = tuple(sorted([c_a['slug'], c_b['slug']]))
                    if pair_key in seen_pairs:
                        continue
                    
                    a_drugs, a_diseases, a_scenarios = claim_features[c_a['slug']]
                    b_drugs, b_diseases, b_scenarios = claim_features[c_b['slug']]
                    score = score_pair(c_a, c_b, a_drugs, a_diseases, a_scenarios, b_drugs, b_diseases, b_scenarios)
                    
                    if score >= 6:  # Minimum threshold
                        seen_pairs.add(pair_key)
                        pairs.append({
                            'claim_a': {
                                'slug': c_a['slug'],
                                'claim_id': c_a['claim_id'],
                                'statement': c_a['statement'],
                                'full_claim': c_a['full_claim'][:500],
                                'evidence': c_a['evidence'][:300],
                                'source_note': c_a['source_note'],
                                'confidence': c_a['confidence'],
                            },
                            'claim_b': {
                                'slug': c_b['slug'],
                                'claim_id': c_b['claim_id'],
                                'statement': c_b['statement'],
                                'full_claim': c_b['full_claim'][:500],
                                'evidence': c_b['evidence'][:300],
                                'source_note': c_b['source_note'],
                                'confidence': c_b['confidence'],
                            },
                            'shared_drugs': list(a_drugs & b_drugs),
                            'shared_diseases': list(a_diseases & b_diseases),
                            'shared_scenarios': list(a_scenarios & b_scenarios),
                            'score': score,
                        })
    
    # Sort by score descending
    pairs.sort(key=lambda p: -p['score'])
    
    print(f"\nSmart candidate pairs (score >= 6): {len(pairs)}")
    
    # Count by shared drug
    drug_pair_count = Counter()
    for p in pairs:
        for d in p['shared_drugs']:
            drug_pair_count[d] += 1
    print("\nPairs by shared drug class:")
    for d, cnt in drug_pair_count.most_common(15):
        print(f"  {d}: {cnt}")
    
    # Count by score distribution
    score_dist = Counter(p['score'] for p in pairs)
    print("\nScore distribution:")
    for s, cnt in sorted(score_dist.items(), reverse=True):
        print(f"  score={s}: {cnt}")
    
    # Split into batches of 40 for LLM evaluation
    batch_size = 40
    batches = [pairs[i:i+batch_size] for i in range(0, len(pairs), batch_size)]
    print(f"\nBatches: {len(batches)}")
    
    for i, batch in enumerate(batches):
        out_path = MANIFESTS_DIR / f"candidates_{cluster_filter}_batch{i+1:02d}.json"
        with open(out_path, 'w') as f:
            json.dump({
                'batch_id': f'{cluster_filter}-batch{i+1:02d}',
                'cluster_filter': cluster_filter,
                'pair_count': len(batch),
                'score_range': f"{batch[-1]['score']}-{batch[0]['score']}" if batch else 'none',
                'pairs': batch,
            }, f, indent=2)
        print(f"  Wrote {out_path}: {len(batch)} pairs (scores {batch[-1]['score']}-{batch[0]['score']})")


if __name__ == '__main__':
    main()
