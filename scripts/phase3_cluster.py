#!/usr/bin/env python3
"""
Phase 3 Pass 1: Topic-tag clusterer for IBD/SIBO knowledge graph.

Groups 476 claims by (domain, primary_topic, claim_type) then splits oversized
clusters using sub-topic heuristics suitable for the clinical domain.

Strategy:
  - Primary axis: domain/ (7 domains)
  - Secondary: most specific topic tag (lowest global frequency)
  - Split oversized (>25) therapeutic clusters by drug-class keywords
  - Merge small clusters (<5) within same domain using adjacency scoring
"""

import os
import re
import json
from collections import Counter, defaultdict
from pathlib import Path

CLAIMS_DIR = Path("/home/littleseneca/Projects/Personal/OSKG-IBD/notes/claims")
OUTPUT_DIR = Path("/home/littleseneca/Projects/Personal/OSKG-IBD/scripts/manifests")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MAX_SIZE = 35
MIN_SIZE = 5

# Drug class keyword patterns for splitting oversized therapeutic clusters
DRUG_CLASS_PATTERNS = [
    ("5-ASA / aminosalicylates", re.compile(r'\b(5-?ASA|mesalazine|mesalamine|sulfasalazine|olsalazine|balsalazide|aminosalicylate)\b', re.I)),
    ("corticosteroids", re.compile(r'\b(corticosteroid|prednisolone|prednisone|budesonide|steroid|MMX)\b', re.I)),
    ("thiopurines / immunomodulators", re.compile(r'\b(thiopurine|azathioprine|mercaptopurine|methotrexate|MTX|immunomodulator|ciclosporin|tacrolimus|mycophenolate)\b', re.I)),
    ("anti-TNF biologics", re.compile(r'\b(anti-?TNF|infliximab|adalimumab|golimumab|CT-P13|biosimilar)\b', re.I)),
    ("anti-integrin / anti-IL biologics", re.compile(r'\b(vedolizumab|anti-?integrin|ustekinumab|anti-?IL|anti-?IL-?12|anti-?IL-?23)\b', re.I)),
    ("JAK inhibitors", re.compile(r'\b(JAK|tofacitinib|upadacitinib|filgotinib|Janus)\b', re.I)),
    ("antibiotics", re.compile(r'\b(antibiotic|ciprofloxacin|metronidazole|rifaximin|metronidazole)\b', re.I)),
    ("surgery / colectomy", re.compile(r'\b(surgery|colectomy|ileal.pouch|IPAA|resection|laparoscopic|post.?operative|ileo?anal|pouchitis|stoma)\b', re.I)),
    ("diagnosis / monitoring", re.compile(r'\b(diagnos|test|screen|monitor|endoscop|colonoscop|surveillance|biomarker|calprotectin|fecal|histolog|biopsy)\b', re.I)),
    ("maintenance / treat-to-target", re.compile(r'\b(maintenance|maintain|remission|relapse|treat.to.target|STRIDE|mucosal.healing|step.up|top.down)\b', re.I)),
    ("pregnancy / special populations", re.compile(r'\b(pregnan|breast.?feed|lactation|pediatric|elderly)\b', re.I)),
]

# Topic adjacency map
TOPIC_ADJACENCY = {
    "topic/ibd": ["topic/crohns-disease", "topic/ulcerative-colitis", "topic/pathogenesis", "topic/genetics"],
    "topic/crohns-disease": ["topic/ibd", "topic/ulcerative-colitis", "topic/fistula", "topic/ileocaecal-cd", "topic/surgery"],
    "topic/ulcerative-colitis": ["topic/ibd", "topic/crohns-disease", "topic/asuc", "topic/colectomy"],
    "topic/pathogenesis": ["topic/genetics", "topic/immune-dysregulation", "topic/microbiome", "topic/epithelial-barrier"],
    "topic/genetics": ["topic/pathogenesis", "topic/immune-dysregulation"],
    "topic/immune-dysregulation": ["topic/pathogenesis", "topic/genetics", "topic/autoimmunity"],
    "topic/sibo": ["topic/microbiome", "topic/ibs", "topic/breath-testing", "topic/imo", "topic/methane", "topic/hydrogen-sulfide"],
    "topic/microbiome": ["topic/sibo", "topic/dysbiosis", "topic/probiotics", "topic/fmt", "topic/microbial-fermentation"],
    "topic/ibs": ["topic/sibo", "topic/breath-testing", "topic/microbiome"],
    "topic/imo": ["topic/sibo", "topic/methane", "topic/breath-testing"],
    "topic/breath-testing": ["topic/sibo", "topic/imo", "topic/diagnosis", "topic/methane", "topic/hydrogen-sulfide"],
    "topic/treatment": ["topic/biologics", "topic/immunomodulators", "topic/corticosteroids", "topic/antibiotics",
                        "topic/5-asa", "topic/surgery", "topic/treat-to-target", "topic/step-up-vs-top-down",
                        "topic/induction-therapy", "topic/maintenance-therapy"],
    "topic/biologics": ["topic/anti-tnf", "topic/anti-integrin", "topic/anti-il12-23", "topic/jak-inhibitors",
                        "topic/biosimilars", "topic/therapeutic-drug-monitoring"],
    "topic/anti-tnf": ["topic/biologics", "topic/infliximab", "topic/biosimilars", "topic/therapeutic-drug-monitoring"],
    "topic/anti-integrin": ["topic/biologics", "topic/vedolizumab"],
    "topic/anti-il12-23": ["topic/biologics"],
    "topic/jak-inhibitors": ["topic/biologics", "topic/tofacitinib", "topic/jak-inhibitor"],
    "topic/immunomodulators": ["topic/thiopurines", "topic/methotrexate", "topic/corticosteroids"],
    "topic/corticosteroids": ["topic/immunomodulators", "topic/induction-therapy", "topic/corticosteroid-sparing"],
    "topic/antibiotics": ["topic/treatment", "topic/sibo", "topic/rifaximin", "topic/herbal-antimicrobials"],
    "topic/5-asa": ["topic/mesalazine", "topic/mesalamine", "topic/mucosal-healing"],
    "topic/surgery": ["topic/colectomy", "topic/laparoscopic-resection", "topic/postoperative-recurrence", "topic/fistula", "topic/ileocaecal-cd"],
    "topic/diagnosis": ["topic/imaging", "topic/endoscopy", "topic/biomarkers", "topic/breath-testing",
                        "topic/histology", "topic/differential-diagnosis"],
    "topic/imaging": ["topic/endoscopy", "topic/mri", "topic/diagnosis", "topic/histology"],
    "topic/endoscopy": ["topic/imaging", "topic/diagnosis", "topic/histology", "topic/mucosal-healing"],
    "topic/biomarkers": ["topic/diagnosis", "topic/mucosal-healing", "topic/therapeutic-drug-monitoring"],
    "topic/diet": ["topic/elemental-diet", "topic/scd", "topic/low-fodmap", "topic/lfe", "topic/gaps",
                   "topic/paleo", "topic/carbohydrate-malabsorption", "topic/een"],
    "topic/elemental-diet": ["topic/diet", "topic/een", "topic/scd"],
    "topic/scd": ["topic/diet", "topic/elemental-diet", "topic/carbohydrate-malabsorption"],
    "topic/carbohydrate-malabsorption": ["topic/diet", "topic/scd", "topic/low-fodmap", "topic/microbial-fermentation"],
    "topic/grade": ["topic/guideline-recommendation", "topic/treatment", "topic/diagnosis", "topic/imaging"],
}


def parse_frontmatter(text):
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}, []
    fm_text = m.group(1)
    data = {}
    tags = []
    current_key = None
    for line in fm_text.split('\n'):
        kv = re.match(r'^(\w[\w_]*):\s*(.*)', line)
        if kv:
            current_key = kv.group(1)
            val = kv.group(2).strip().strip('"').strip("'")
            data[current_key] = val
        elif current_key and line.strip().startswith('- '):
            val = line.strip()[2:].strip().strip('"').strip("'")
            if current_key == 'tags':
                tags.append(val)
    return data, tags


def load_claims():
    claims = []
    for fname in os.listdir(CLAIMS_DIR):
        if not fname.endswith('.md') or fname == 'Claims Index.md':
            continue
        slug = fname.replace('.md', '')
        path = CLAIMS_DIR / fname
        with open(path) as f:
            content = f.read()
        fm, tags = parse_frontmatter(content)
        if 'claim_id' not in fm:
            continue

        topic_tags = [t for t in tags if t.startswith('topic/')]
        domain_tags = [t for t in tags if t.startswith('domain/')]
        domain = domain_tags[0] if domain_tags else 'unknown'

        claims.append({
            'slug': slug,
            'claim_id': fm.get('claim_id', ''),
            'statement': fm.get('statement', ''),
            'claim_type': fm.get('claim_type', ''),
            'topics': topic_tags,
            'domain': domain,
            'source_note': fm.get('source_note', ''),
            'confidence': fm.get('confidence', ''),
        })

    # Compute topic frequencies for "most specific" selection
    topic_freq = Counter()
    for c in claims:
        for t in c['topics']:
            topic_freq[t] += 1

    for c in claims:
        if c['topics']:
            c['primary_topic'] = min(c['topics'], key=lambda t: topic_freq.get(t, 0))
        else:
            c['primary_topic'] = 'topic/unknown'

    return claims, topic_freq


def classify_drug_class(claim):
    """For therapeutic claims, classify by drug class from statement text."""
    stmt = claim['statement'].lower()
    for label, pattern in DRUG_CLASS_PATTERNS:
        if pattern.search(stmt):
            return label
    # Try claim_id for clues
    cid = claim['claim_id'].lower()
    for label, pattern in DRUG_CLASS_PATTERNS:
        if pattern.search(cid):
            return label
    return "general / other"


def make_label(claims):
    topics = Counter()
    types = Counter()
    for c in claims:
        topics[c['primary_topic']] += 1
        types[c['claim_type']] += 1
    top_topic = topics.most_common(1)[0][0].replace('topic/', '')
    top_type = types.most_common(1)[0][0]
    return f"{top_topic} ({top_type})"


def score_merge(small_info, candidate_info):
    score = 0
    if candidate_info['domain'] != small_info['domain']:
        return 0
    score += 3  # same domain
    if candidate_info['primary_topic'] == small_info['primary_topic']:
        score += 3
    elif small_info['primary_topic'] in TOPIC_ADJACENCY:
        if candidate_info['primary_topic'] in TOPIC_ADJACENCY[small_info['primary_topic']]:
            score += 2
    if candidate_info['claim_type'] == small_info['claim_type']:
        score += 1
    return score


def split_oversized(group):
    """For oversized clusters (>MAX_SIZE), try drug-class splitting first, then claim_type."""
    if len(group) <= MAX_SIZE:
        return [group]

    # For therapeutic claims, try drug-class splitting
    if group[0]['claim_type'] == 'therapeutic':
        dc_groups = defaultdict(list)
        for c in group:
            dc = classify_drug_class(c)
            dc_groups[dc].append(c)
        if len(dc_groups) > 1:
            result = []
            for dc, dc_group in dc_groups.items():
                if len(dc_group) > MAX_SIZE:
                    # Still too large — split by source (claim_id prefix)
                    src_groups = defaultdict(list)
                    for c2 in dc_group:
                        src = c2['claim_id'].split('-r')[0] if '-r' in c2['claim_id'] else 'other'
                        src_groups[src].append(c2)
                    for sg in src_groups.values():
                        result.append(sg)
                else:
                    result.append(dc_group)
            return result

    # Fallback: split by claim_type
    ct_groups = defaultdict(list)
    for c in group:
        ct_groups[c['claim_type']].append(c)
    result = []
    for ct, ct_group in ct_groups.items():
        if len(ct_group) > MAX_SIZE:
            result.extend(split_oversized(ct_group))
        else:
            result.append(ct_group)
    return result


def cluster_claims(claims):
    # Step 1: group by (domain, primary_topic)
    raw_groups = defaultdict(list)
    for c in claims:
        key = (c['domain'], c['primary_topic'])
        raw_groups[key].append(c)

    clusters = []
    for (domain, topic), group in raw_groups.items():
        # Split oversized groups
        sub_clusters = split_oversized(group)
        clusters.extend(sub_clusters)

    # Step 2: iterative merge for small clusters
    for iteration in range(5):
        smalls = [(i, cl) for i, cl in enumerate(clusters) if len(cl) < MIN_SIZE]
        if not smalls:
            break

        candidates = [(i, cl) for i, cl in enumerate(clusters) if len(cl) >= MIN_SIZE]
        consumed = set()

        for si, small in smalls:
            best_score = -1
            best_target = None
            small_info = {
                'domain': small[0]['domain'],
                'primary_topic': small[0]['primary_topic'],
                'claim_type': small[0]['claim_type'],
            }
            for ci, cand in candidates:
                cand_info = {
                    'domain': cand[0]['domain'],
                    'primary_topic': cand[0]['primary_topic'],
                    'claim_type': cand[0]['claim_type'],
                }
                score = score_merge(small_info, cand_info)
                if score > best_score:
                    best_score = score
                    best_target = ci

            if best_target is not None and best_score >= 0:
                clusters[best_target].extend(small)
                consumed.add(si)

        clusters = [cl for i, cl in enumerate(clusters) if i not in consumed]
        if not consumed:
            break

    # Fallback: merge remaining orphans into largest cluster
    orphans = [cl for cl in clusters if len(cl) < MIN_SIZE]
    if orphans and clusters:
        largest_idx = max(range(len(clusters)), key=lambda i: len(clusters[i]))
        for orphan in orphans:
            clusters[largest_idx].extend(orphan)
        clusters = [cl for cl in clusters if len(cl) >= MIN_SIZE]

    return clusters


def main():
    claims, topic_freq = load_claims()
    print(f"Loaded {len(claims)} claims from {len(set(c['source_note'] for c in claims))} sources")

    clusters = cluster_claims(claims)

    # Build manifest
    manifest_clusters = []
    total_slugs = set()
    total_pairs = 0

    for i, cl in enumerate(clusters):
        slugs = [c['slug'] for c in cl]
        total_slugs.update(slugs)
        n = len(slugs)
        pairs = n * (n - 1) // 2
        total_pairs += pairs
        label = make_label(cl)
        manifest_clusters.append({
            "id": f"cluster-{i:03d}",
            "label": label,
            "size": n,
            "domain": cl[0]['domain'],
            "primary_topic": cl[0]['primary_topic'],
            "candidate_pairs": pairs,
            "claim_slugs": sorted(slugs),
        })

    assert len(total_slugs) == len(claims), f"Slug count mismatch: {len(total_slugs)} vs {len(claims)}"

    cluster_stats = [{
        "id": c["id"], "label": c["label"], "size": c["size"],
        "candidate_pairs": c["candidate_pairs"]
    } for c in manifest_clusters]

    manifest = {
        "version": "1.0",
        "project": "OSKG-IBD",
        "total_claims": len(claims),
        "total_clusters": len(clusters),
        "total_candidate_pairs": total_pairs,
        "cluster_stats": sorted(cluster_stats, key=lambda x: -x['size']),
        "clusters": sorted(manifest_clusters, key=lambda x: -x['size']),
    }

    out_path = OUTPUT_DIR / "phase3_clusters.json"
    with open(out_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\nClusters: {len(clusters)}")
    print(f"Candidate pairs: {total_pairs} ({100*(1-total_pairs/(len(claims)*(len(claims)-1)/2)):.1f}% reduction from {len(claims)*(len(claims)-1)//2} brute-force)")
    print(f"Orphan claims (singletons): {sum(1 for cl in clusters if len(cl) == 1)}")
    print(f"Average cluster size: {len(claims)/len(clusters):.1f}")
    print(f"Max cluster size: {max(len(cl) for cl in clusters)}")
    print(f"Min cluster size: {min(len(cl) for cl in clusters)}")
    print(f"\nManifest written to {out_path}")

    print("\nTop 15 clusters by size:")
    for s in manifest['cluster_stats'][:15]:
        print(f"  {s['id']}: {s['label']} — {s['size']} claims, {s['candidate_pairs']} pairs")


if __name__ == '__main__':
    main()
