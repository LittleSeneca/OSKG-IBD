#!/usr/bin/env python3
"""
Update chapter notes with claims_status frontmatter and claim counts.
Lightweight pass: adds frontmatter metadata without replacing claim blocks.
The ### Claim N: block replacement is deferred to task t_c6076bcd.
"""
import os, re
from collections import defaultdict
from datetime import datetime

BASE = "/home/littleseneca/Projects/Personal/OSKG-IBD"
CLAIMS_DIR = f"{BASE}/notes/claims"

# Map each source note to its claims
note_claims = defaultdict(list)
for f in os.listdir(CLAIMS_DIR):
    if not f.startswith('claim-') or not f.endswith('.md'):
        continue
    path = os.path.join(CLAIMS_DIR, f)
    with open(path) as fh:
        content = fh.read()
    m = re.search(r'source_note: "\[\[(.+?)\]\]"', content)
    if m:
        note_name = m.group(1)
        m2 = re.search(r'claim_id: "(.+?)"', content)
        cid = m2.group(1) if m2 else '?'
        note_claims[note_name].append(cid)

# Find all reading notes
notes_dir = f"{BASE}/notes"
reading_notes = []
for root, dirs, files in os.walk(notes_dir):
    # Skip claims directory
    if 'claims' in root:
        continue
    for f in files:
        if f.endswith('.md') and f != 'Index.md' and 'Index' not in f and f != 'claims-progress.md' and f != 'claims-architecture.md':
            full_path = os.path.join(root, f)
            note_name = f.replace('.md', '')
            reading_notes.append((full_path, note_name))

print(f"Found {len(reading_notes)} reading notes")
print(f"Notes with claims: {len(note_claims)}")

updated = 0
skipped = 0
for note_path, note_name in reading_notes:
    claims = note_claims.get(note_name, [])
    
    with open(note_path, 'r') as fh:
        content = fh.read()
    
    # Check if already has claims_status
    if 'claims_status:' in content:
        skipped += 1
        continue
    
    # Find where to insert frontmatter (after the YAML closing ---)
    fm_end = content.find('---', 1)  # Find second ---
    if fm_end < 0:
        print(f"  SKIP: no frontmatter found in {note_name}")
        continue
    
    fm_end += 3  # After the closing ---
    
    # Determine what type of note this is
    is_reading_note = 'type/reading-note' in content[:500] or 'type/reading-note' in content
    
    if not is_reading_note:
        continue
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    if claims:
        claim_slugs = [f"claim-{cid}" for cid in claims]
        claims_list = '", "'.join(claim_slugs)
        new_fm = f"""claims_status: extracted
claims_extracted_date: {today}
claims_count: {len(claims)}
claims_files: ["{claims_list}"]
"""
    else:
        new_fm = f"""claims_status: pending
claims_extracted_date: {today}
claims_count: 0
claims_files: []
"""
    
    # Insert after frontmatter
    new_content = content[:fm_end] + '\n' + new_fm + content[fm_end:]
    
    with open(note_path, 'w') as fh:
        fh.write(new_content)
    
    if claims:
        print(f"  UPDATED: {note_name} ({len(claims)} claims)")
    updated += 1

print(f"\nUpdated: {updated} notes")
print(f"Skipped (already have claims_status): {skipped}")
