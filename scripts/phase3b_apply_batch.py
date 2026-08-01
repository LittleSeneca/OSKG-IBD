#!/usr/bin/env python3
"""
Phase 3b: Apply edge batch to claim files.

Reads an edge JSON file and patches the ## Edges section of each claim
file with typed wikilinks. Appends to existing edges rather than replacing.
"""

import json, re, os, sys
from pathlib import Path
from collections import defaultdict

CLAIMS_DIR = Path("/home/littleseneca/Projects/Personal/OSKG-IBD/notes/claims")

EDGE_HEADERS = {
    'depends_on': '**Depends on:**',
    'supports': '**Supports:**',
    'extends': '**Extends:**',
    'contradicts': '**Contradicts:**',
    'operationalizes': '**Operationalizes:**',
    'challenged_by': '**Challenged by:**',
}

EDGE_PLACEMENT = {
    'depends_on': ('nothing', 'depends_on'),
    'supports': ('supports', 'nothing'),
    'extends': ('extends', 'nothing'),
    'contradicts': ('contradicts', 'contradicts'),
    'operationalizes': ('operationalizes', 'nothing'),
    'challenged_by': ('challenged_by', 'challenged_by'),
}

HEADER_ORDER = ['depends_on', 'supports', 'extends', 'operationalizes', 'challenged_by', 'contradicts']


def apply_batch(edge_file):
    with open(edge_file) as f:
        edges = json.load(f)
    
    print(f"Processing {len(edges)} edges from {edge_file}")
    
    # Group edges by claim slug
    claim_edges = defaultdict(list)
    for e in edges:
        etype = e['edge_type']
        a, b = e['claim_a'], e['claim_b']
        rationale = e['rationale']
        
        placement = EDGE_PLACEMENT.get(etype, ('nothing', 'nothing'))
        
        if placement[0] != 'nothing':
            claim_edges[a].append((placement[0], b, rationale))
        if placement[1] != 'nothing':
            claim_edges[b].append((placement[1], a, rationale))
    
    # Apply to claim files
    modified = 0
    skipped = 0
    
    for slug, edges_list in claim_edges.items():
        path = CLAIMS_DIR / f"{slug}.md"
        if not path.exists():
            print(f"  WARNING: {slug}.md not found — skipping")
            skipped += 1
            continue
        
        with open(path) as f:
            content = f.read()
        
        # Group new edges by type
        new_by_type = defaultdict(list)
        for etype, target, rationale in edges_list:
            display = rationale[:120]
            new_by_type[etype].append(f'- [[{target}|{display}]]')
        
        # Find the ## Edges section
        edges_match = re.search(r'## Edges\n(.*?)(?=\n##|\n---|\Z)', content, re.DOTALL)
        
        if not edges_match:
            print(f"  WARNING: {slug}.md has no ## Edges section")
            skipped += 1
            continue
        
        edges_section = edges_match.group(1)
        
        # For each edge type, find the existing header and append
        new_section_lines = []
        current_pos = 0
        
        # Parse existing section to find where headers are
        existing_lines = edges_section.split('\n')
        
        # Rebuild: for each header in order, collect existing + new entries
        rebuilt = []
        for header_key in HEADER_ORDER:
            header = EDGE_HEADERS[header_key]
            # Find existing entries for this type
            existing_entries = []
            in_section = False
            for line in existing_lines:
                stripped = line.strip()
                if stripped.startswith(header):
                    in_section = True
                    existing_entries.append(line.rstrip())
                    continue
                if in_section:
                    if stripped.startswith('**') and ':**' in stripped:
                        in_section = False
                    elif stripped.startswith('- [['):
                        existing_entries.append(line.rstrip())
            
            # Add header if not present
            if not any(l.strip().startswith(header) for l in existing_lines):
                rebuilt.append(header)
                rebuilt.append('')
            else:
                rebuilt.extend(existing_entries)
            
            # Add new edges
            if header_key in new_by_type:
                for edge_line in new_by_type[header_key]:
                    rebuilt.append(edge_line)
                rebuilt.append('')
            elif not existing_entries:
                rebuilt.append('')
        
        new_section = '## Edges\n' + '\n'.join(rebuilt)
        
        # Replace in content
        old_section = edges_match.group(0)
        content = content.replace(old_section, new_section, 1)
        
        with open(path, 'w') as f:
            f.write(content)
        
        modified += 1
    
    print(f"Modified {modified} claim files, {skipped} skipped")
    return modified


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <edge_file.json>")
        sys.exit(1)
    
    apply_batch(sys.argv[1])
