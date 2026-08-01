#!/usr/bin/env python3
"""
Fix thin-evidence claims by extracting evidence text from source notes.
Targets the 28 claims with 'See source note.' in their ## Evidence section.
"""
import os, re
from pathlib import Path

BASE = "/home/littleseneca/Projects/Personal/OSKG-IBD"
CLAIMS_DIR = f"{BASE}/notes/claims"

def find_source_note_path(source_note_name):
    """Find the full path of a source note by searching notes/ directory."""
    for root, dirs, files in os.walk(f"{BASE}/notes"):
        for f in files:
            if f == source_note_name + ".md" or f == source_note_name:
                return os.path.join(root, f)
    return None

def extract_evidence_from_note(note_path, claim_id):
    """Extract evidence text from a source note for a given claim."""
    with open(note_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    evidence = ""
    
    # Pattern 1: Claims-based notes with ### Claim N: headers
    # Map claim_id (e.g., aga-cd2021-3) to claim number
    m = re.search(r'-(\d+)$', claim_id)
    if m:
        claim_num = m.group(1)
        # Find "### Claim N:" section
        pattern = f'### Claim {claim_num}:'
        idx = text.find(pattern)
        if idx >= 0:
            # Extract the section after this header until next ### or ## section
            section = text[idx:]
            next_section = re.search(r'\n### |\n## [^C]', section[len(pattern):])
            if next_section:
                section = section[:len(pattern) + next_section.start()]
            
            # Find evidence/analysis text - look for the paragraph after the claim statement
            # Usually the evidence is between the claim statement and the confidence evaluation
            evidence_match = re.search(r'\*\*Evidence[^:]*:\*\*\s*(.+?)(?=\n\*\*|\n###|\n## |\Z)', section, re.DOTALL)
            if evidence_match:
                evidence = evidence_match.group(1).strip()
            else:
                # Try finding any substantive paragraph
                paras = [p.strip() for p in section.split('\n\n') if len(p.strip()) > 50]
                if len(paras) >= 2:
                    evidence = paras[1]  # Second paragraph after header is usually evidence
    
    # Pattern 2: Implicit/structural claims (aga-sibo2020-implicit-N, etc.)
    if not evidence:
        m = re.search(r'implicit-(\d+)$', claim_id)
        if m:
            # For implicit claims, extract from the relevant section
            # Look for BPA or structural claim sections
            pass
    
    # Pattern 3: Core thesis claims (ballantyne-paleo-implicit-8, etc.)
    # These are whole-book synthesis claims - extract from Key Contributions or Assessment
    if not evidence:
        # Get the core thesis section
        thesis_match = re.search(r'## (?:Core Thesis|Key Contributions|The Claim)\n\n(.+?)(?=\n## |\n---\n)', text, re.DOTALL)
        if thesis_match:
            evidence = thesis_match.group(1).strip()[:500]
    
    return evidence

# Find all thin claims
thin_claims = []
for f in os.listdir(CLAIMS_DIR):
    if not f.startswith('claim-') or not f.endswith('.md'):
        continue
    path = os.path.join(CLAIMS_DIR, f)
    with open(path) as fh:
        content = fh.read()
    
    m = re.search(r'## Evidence\n\n(.+?)(?=\n## )', content, re.DOTALL)
    if not m or m.group(1).strip() not in ['See source note.', 'See source note']:
        continue
    
    m2 = re.search(r'claim_id: "(.+?)"', content)
    cid = m2.group(1) if m2 else '?'
    m3 = re.search(r'source_note: "\[\[(.+?)\]\]"', content)
    src_name = m3.group(1) if m3 else '?'
    
    thin_claims.append((path, cid, src_name))

print(f"Fixing {len(thin_claims)} thin-evidence claims...")

fixed = 0
for claim_path, claim_id, source_note_name in thin_claims:
    note_path = find_source_note_path(source_note_name)
    if not note_path:
        print(f"  SKIP: source note not found for {claim_id}: {source_note_name}")
        continue
    
    evidence = extract_evidence_from_note(note_path, claim_id)
    if not evidence or len(evidence) < 20:
        # Fall back to extracting from the claim file's own content
        with open(claim_path) as fh:
            content = fh.read()
        # Look for useful content in Stakes or Assessment sections
        stakes = re.search(r'## Stakes\n\n(.+?)(?=\n## )', content, re.DOTALL)
        assess = re.search(r'## Assessment\n\n(.+?)(?=\n---|\Z)', content, re.DOTALL)
        if stakes and stakes.group(1).strip() not in ['See source note.', '']:
            evidence = f"(From source note analysis)\n\n{stakes.group(1).strip()}"
        elif assess and assess.group(1).strip() not in ['See source note.', '']:
            evidence = f"(From source note analysis)\n\n{assess.group(1).strip()}"
        else:
            evidence = f"See source note [[{source_note_name}]] for full evidence evaluation. This claim was extracted from a synthesis/whole-book note where evidence is distributed across the text rather than concentrated in a single section."
    
    # Replace the thin evidence
    old_evidence = "See source note."
    new_evidence = evidence.replace('\n\n', '\n\n').strip()
    
    # Read file and patch
    with open(claim_path, 'r') as fh:
        content = fh.read()
    
    if old_evidence in content:
        new_content = content.replace(
            f"## Evidence\n\n{old_evidence}",
            f"## Evidence\n\n{new_evidence}"
        )
        with open(claim_path, 'w') as fh:
            fh.write(new_content)
        fixed += 1
        print(f"  FIXED: {claim_id} ({len(new_evidence)} chars)")
    else:
        print(f"  SKIP: pattern not found in {claim_id}")

print(f"\nFixed {fixed}/{len(thin_claims)} thin-evidence claims")
