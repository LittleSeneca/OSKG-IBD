#!/usr/bin/env python3
"""Phase 3c: Analyze SIBO claims for contradiction discovery."""
import os, re, json
from collections import defaultdict

CLAIMS_DIR = os.path.expanduser("~/Projects/Personal/OSKG-IBD/notes/claims")

claims = []
for filename in sorted(os.listdir(CLAIMS_DIR)):
    if not filename.startswith('claim-') or not filename.endswith('.md'):
        continue
    filepath = os.path.join(CLAIMS_DIR, filename)
    with open(filepath, 'r') as f:
        content = f.read()
    
    slug = filename.replace('.md', '')
    fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    fm = fm_match.group(1) if fm_match else ""
    
    cid_match = re.search(r'claim_id:\s*["\']?([^"\'\n]+)', fm)
    claim_id = cid_match.group(1).strip() if cid_match else slug
    
    stmt_match = re.search(r'statement:\s*"(.+?)"', fm, re.DOTALL)
    statement = stmt_match.group(1).strip() if stmt_match else ""
    
    conf_match = re.search(r'confidence:\s*"?(\S+?)"?\s*$', fm, re.MULTILINE)
    confidence = conf_match.group(1).strip() if conf_match else ""
    
    topic_tags = []
    for m in re.finditer(r'-\s*topic/(\S+)', fm):
        topic_tags.append(m.group(1))
    
    scholar = ""
    sch_match = re.search(r'-\s*scholar/(\S+)', fm)
    if sch_match:
        scholar = sch_match.group(1)
    
    source = ""
    src_match = re.search(r'-\s*source/(\S+)', fm)
    if src_match:
        source = src_match.group(1)
    
    # Extract statement from body too if frontmatter statement is empty
    if not statement:
        # Try extracting from the main claim line
        h1_match = re.search(r'^# .+?: (.+)$', content, re.MULTILINE)
        if h1_match:
            statement = h1_match.group(1).strip()
    
    claims.append({
        'slug': slug,
        'claim_id': claim_id,
        'statement': statement[:300],
        'confidence': confidence,
        'scholar': scholar,
        'source': source,
        'topic_tags': topic_tags,
        'is_sibo': 'sibo' in content.lower() or 'sibo' in slug.lower(),
    })

print(f"Total claims: {len(claims)}")
print(f"SIBO-related: {sum(1 for c in claims if c['is_sibo'])}")

# Group SIBO claims by source
camps = defaultdict(list)
for c in claims:
    if c['is_sibo']:
        key = c['source'] or c['scholar'] or 'unknown'
        camps[key].append(c)

for camp, clist in sorted(camps.items(), key=lambda x: -len(x[1])):
    print(f"\n{'='*60}")
    print(f"SOURCE: {camp} ({len(clist)} claims)")
    print(f"{'='*60}")
    for c in clist:
        tags = ', '.join(c['topic_tags'][:6])
        print(f"\n  SLUG: {c['slug']}")
        print(f"  CLAIM_ID: {c['claim_id']}")
        print(f"  SCHOLAR: {c['scholar']} | CONFIDENCE: {c['confidence']}")
        print(f"  TOPICS: {tags}")
        print(f"  STATEMENT: {c['statement'][:200]}")
