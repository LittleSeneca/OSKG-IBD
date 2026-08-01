#!/usr/bin/env python3
"""
Phase 2c: Replace claim blocks with compact summaries and fix claims_files wikilinks.

Handles:
- ## Claim N: / ### Claim N: (standard explicit)
- ## BPA N: (AGA SIBO format)
- ## Structural Claim: (Yamada Ch58)
- Implicit notes: just fix claims_files wikilinks (no claim blocks to replace)

For each claim block, replaces the body content with:
    **Claim N —** Title → [[claim-slug]] | claim_id | Confidence: rating
"""

import os, re, json, sys
from datetime import date

PROJECT_DIR = os.path.expanduser("~/Projects/Personal/OSKG-IBD")
NOTES_DIR = os.path.join(PROJECT_DIR, "notes")
CLAIMS_DIR = os.path.join(NOTES_DIR, "claims")

# Load mapping
with open("/tmp/claim_id_to_slug.json") as f:
    mapping = json.load(f)

# Known confidence values to match
CONFIDENCE_PATTERNS = [
    r'VERY\s+HIGH', r'HIGH', r'MEDIUM[\s-]HIGH', r'MEDIUM', r'LOW[\s-]MEDIUM', r'LOW', r'DEBATABLE',
    r'VERY\s+LOW', r'MODERATE', r'STRONG', r'WEAK', r'CONDITIONAL', r'Not\s+graded',
]
CONFIDENCE_RE = re.compile(r'\*\*Confidence:\*\*\s*(' + '|'.join(CONFIDENCE_PATTERNS) + r')\b', re.IGNORECASE)
# Also handle "Confidence: VALUE" (without bold)
CONFIDENCE_PLAIN_RE = re.compile(r'^Confidence:\s*(' + '|'.join(CONFIDENCE_PATTERNS) + r')\b', re.IGNORECASE | re.MULTILINE)

def get_slug(cid_entry):
    """Map a claims_files entry to actual filename slug."""
    lookup = cid_entry
    if lookup.startswith("claim-"):
        lookup = lookup[6:]
    return mapping.get(lookup) or mapping.get(cid_entry)

def extract_confidence(body):
    """Extract confidence rating from claim body."""
    m = CONFIDENCE_RE.search(body)
    if m:
        return m.group(1).strip().upper()
    m = CONFIDENCE_PLAIN_RE.search(body)
    if m:
        return m.group(1).strip().upper()
    return "unknown"

def process_note(filepath):
    """Process a single note. Returns (updated, claim_count) or (False, 0) if skipped."""
    rel = os.path.relpath(filepath, NOTES_DIR)
    
    with open(filepath) as f:
        content = f.read()
    
    if 'claims_status: extracted' not in content:
        return False, 0
    
    m = re.search(r'claims_files:\s*\[([^\]]*)\]', content)
    if not m:
        return False, 0
    
    claims_ids = re.findall(r'"([^"]+)"', m.group(1))
    if not claims_ids:
        return False, 0
    
    # Find all explicit claim headings
    # Pattern: heading level, claim number/type, title
    heading_patterns = [
        (r'^## Claim (\d+):\s*(.+?)$', 'h2', 'Claim {num}'),
        (r'^### Claim (\d+):\s*(.+?)$', 'h3', 'Claim {num}'),
        (r'^## BPA (\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*):\s*(.+?)$', 'bpa_h2', 'BPA {num}'),
        (r'^## Structural Claim:\s*(.+?)$', 'structural', 'Structural Claim'),
    ]
    
    claim_matches = []
    for pattern, style, label_template in heading_patterns:
        for m in re.finditer(pattern, content, re.MULTILINE):
            if style == 'structural':
                num = '1'
                title = m.group(1).strip()
            else:
                num = m.group(1)
                title = m.group(2).strip()
            claim_matches.append((style, num, title, m.start(), m.end(), label_template))
    
    if not claim_matches:
        # Implicit note: no claim blocks to replace, just fix claims_files wikilinks
        slugs = [get_slug(cid) for cid in claims_ids]
        new_content = fix_frontmatter(content, slugs)
        if new_content != content:
            with open(filepath, 'w') as f:
                f.write(new_content)
            return True, len(claims_ids)
        return False, 0
    
    # Sort by position
    claim_matches.sort(key=lambda x: x[3])
    
    # Build replacements from end to front
    replacements = []
    new_slugs = []
    
    for idx, (style, num, title, h_start, h_end, label_template) in enumerate(claim_matches):
        label = label_template.format(num=num)
        heading_line = content[h_start:h_end]
        
        # Determine body end
        search_start = h_end
        possible_ends = []
        
        # Next claim heading
        for pattern, _, _ in heading_patterns:
            next_m = re.search(pattern, content[search_start:], re.MULTILINE)
            if next_m:
                possible_ends.append(search_start + next_m.start())
        
        # --- separator
        next_sep = re.search(r'^---\s*$', content[search_start:], re.MULTILINE)
        if next_sep:
            possible_ends.append(search_start + next_sep.start())
        
        # Assessment / Guideline Assessment section (any level)
        next_assessment = re.search(r'^#{2,4}\s+.*(?:Overall )?Assessment', content[search_start:], re.MULTILINE)
        if next_assessment:
            possible_ends.append(search_start + next_assessment.start())
        
        # For BPA, also stop at "Guideline Assessment"
        next_ga = re.search(r'^#{2,4}\s+.*Guideline Assessment', content[search_start:], re.MULTILINE)
        if next_ga:
            possible_ends.append(search_start + next_ga.start())
        
        body_end = min(possible_ends) if possible_ends else len(content)
        body = content[search_start:body_end]
        
        # Get claim_id and slug
        claim_id = claims_ids[idx] if idx < len(claims_ids) else "unknown"
        slug = get_slug(claim_id)
        new_slugs.append(slug)
        
        confidence = extract_confidence(body)
        
        # Determine heading prefix for replacement (keep original)
        # Build compact summary (heading + one line)
        compact = f"{heading_line}\n**{label} —** {title} → [[{slug}]] | {claim_id} | Confidence: {confidence}\n"
        
        # The replacement covers from start of heading to body_end
        # But we need to check: if the next thing is a --- separator, we should NOT include it
        # The body_end already stops BEFORE the separator. Good.
        replacements.append((h_start, body_end, compact))
    
    # Apply replacements from end to start
    result = content
    for start, end, repl in sorted(replacements, key=lambda x: x[1], reverse=True):
        result = result[:start] + repl + result[end:]
    
    # Fix claims_files frontmatter
    result = fix_frontmatter(result, new_slugs)
    
    if result != content:
        with open(filepath, 'w') as f:
            f.write(result)
        return True, len(claim_matches)
    
    return False, 0

def fix_frontmatter(content, slugs):
    """Replace claims_files array with [[wikilink]] format."""
    # Build new claims_files entries
    entries = ",\n".join(f'  "[[{s}]]"' for s in slugs if s)
    new_block = f'claims_files:\n{entries}'
    
    # Replace using regex
    result = re.sub(
        r'claims_files:\s*\[.*?\]',
        new_block,
        content,
        flags=re.DOTALL
    )
    return result

def verify_slugs(slugs):
    """Return list of slugs that don't resolve to real files."""
    missing = []
    for slug in slugs:
        if not slug:
            missing.append("(None)")
        else:
            claim_path = os.path.join(CLAIMS_DIR, slug + ".md")
            if not os.path.exists(claim_path):
                missing.append(slug)
    return missing

def main():
    notes = []
    for root, dirs, files in os.walk(NOTES_DIR):
        for fname in files:
            if not fname.endswith('.md'):
                continue
            if fname in ('Index.md', 'Notes Index.md', 'claims-progress.md', 'claims-architecture.md'):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath) as f:
                head = f.read(5000)
            if 'claims_status: extracted' in head:
                notes.append(fpath)
    
    print(f"Processing {len(notes)} notes...\n")
    
    updated = 0
    total_claims_processed = 0
    unresolved = []
    errors = []
    
    for fpath in sorted(notes):
        rel = os.path.relpath(fpath, NOTES_DIR)
        try:
            changed, count = process_note(fpath)
            if changed:
                updated += 1
                total_claims_processed += count
                print(f"  OK  {rel} ({count} claims)")
            else:
                # Verify: re-read and check claims_files
                with open(fpath) as f:
                    current = f.read()
                m = re.search(r'claims_files:\s*\[([^\]]*)\]', current)
                if m:
                    inner = m.group(1)
                    # Check if already has wikilinks
                    if '[[' in inner:
                        print(f"  OK  {rel} (already updated)")
                    else:
                        print(f"  ??  {rel} (no change, check manually)")
                else:
                    print(f"  OK  {rel} (no claims_files block)")
        except Exception as e:
            print(f"  ERR {rel}: {e}")
            errors.append((rel, str(e)))
    
    # Verification pass
    print(f"\n--- Verification ---")
    print(f"Checking all 47 notes for resolved wikilinks...")
    
    all_ok = True
    for fpath in sorted(notes):
        rel = os.path.relpath(fpath, NOTES_DIR)
        with open(fpath) as f:
            current = f.read()
        
        # Extract wikilinks from claims_files
        wikilinks = re.findall(r'\"\[\[(.*?)\]\]\"', current)
        missing = verify_slugs(wikilinks)
        if missing:
            print(f"  BAD {rel}: unresolved: {missing}")
            all_ok = False
    
    if all_ok:
        print("  All wikilinks resolve!")
    
    print(f"\nSummary: {updated} notes updated, {len(notes)-updated} unchanged, {len(errors)} errors")
    if errors:
        for rel, err in errors:
            print(f"  ERROR: {rel}: {err}")

if __name__ == '__main__':
    main()
