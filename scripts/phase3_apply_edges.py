#!/usr/bin/env python3
"""
Phase 3 Pass 3: Apply cross-source edges to claim files.

Reads the combined edge JSON and patches the ## Edges section of each claim
file with typed wikilinks. Removes placeholder HTML comments.
"""

import json, re, os, sys
from pathlib import Path
from collections import defaultdict

CLAIMS_DIR = Path("/home/littleseneca/Projects/Personal/OSKG-IBD/notes/claims")
COMBINED_PATH = Path("/home/littleseneca/Projects/Personal/OSKG-IBD/scripts/manifests/phase3_edges/combined.json")

EDGE_HEADERS = {
    'depends_on': '**Depends on:**',
    'supports': '**Supports:**',
    'extends': '**Extends:**',
    'contradicts': '**Contradicts:**',
    'operationalizes': '**Operationalizes:**',
    'challenged_by': '**Challenged by:**',
}

# Which edge types go into which claim's file
# Format: (what claim_a gets, what claim_b gets)
EDGE_PLACEMENT = {
    'depends_on': ('nothing', 'depends_on'),       # claim_b depends on claim_a
    'supports': ('supports', 'nothing'),             # claim_a supports claim_b
    'extends': ('extends', 'nothing'),               # claim_a extends claim_b
    'contradicts': ('contradicts', 'contradicts'),   # both get contradicts
    'operationalizes': ('operationalizes', 'nothing'), # claim_a operationalizes claim_b
    'challenged_by': ('challenged_by', 'challenged_by'),  # both get challenged_by
}

HEADER_ORDER = ['depends_on', 'supports', 'extends', 'operationalizes', 'challenged_by', 'contradicts']


def apply_edges(edges):
    """Group edges by claim file and apply."""
    # Group: claim_slug -> [(edge_type, target_slug, rationale), ...]
    claim_edges = defaultdict(list)

    for e in edges:
        etype = e['edge_type']
        a, b = e['claim_a'], e['claim_b']
        rationale = e['rationale']

        placement = EDGE_PLACEMENT.get(etype, ('nothing', 'nothing'))

        # What claim_a gets
        if placement[0] != 'nothing':
            claim_edges[a].append((placement[0], b, rationale))

        # What claim_b gets
        if placement[1] != 'nothing':
            claim_edges[b].append((placement[1], a, rationale))

    # Apply to files
    modified = 0
    for slug, edges_list in claim_edges.items():
        path = CLAIMS_DIR / f"{slug}.md"
        if not path.exists():
            print(f"  WARNING: {slug}.md not found")
            continue

        with open(path) as f:
            content = f.read()

        # Find the ## Edges section
        edges_match = re.search(r'(## Edges\n)', content)
        if not edges_match:
            print(f"  WARNING: {slug}.md has no ## Edges section")
            continue

        # Group edges by type
        by_type = defaultdict(list)
        for etype, target, rationale in edges_list:
            # Truncate rationale for display text
            display = rationale[:120]
            by_type[etype].append(f'- [[{target}|{display}]]')

        # Build the new ## Edges section
        lines = ['## Edges', '']
        for header_key in HEADER_ORDER:
            header = EDGE_HEADERS[header_key]
            these_edges = by_type.get(header_key, [])
            lines.append(header)
            if these_edges:
                for edge_line in these_edges:
                    lines.append(edge_line)
            lines.append('')  # blank line after each section

        new_edges_section = '\n'.join(lines)

        # Replace the old edges section
        old_section_match = re.search(r'## Edges\n.*?(?=\n##|\n---|\Z)', content, re.DOTALL)
        if old_section_match:
            old_section = old_section_match.group(0)
            # Make sure we only replace the first occurrence
            content = content.replace(old_section, new_edges_section, 1)
        else:
            print(f"  WARNING: {slug}.md — cannot locate full edges section")
            continue

        with open(path, 'w') as f:
            f.write(content)

        modified += 1

    return modified, claim_edges


def main():
    with open(COMBINED_PATH) as f:
        edges = json.load(f)

    print(f"Applying {len(edges)} edges to claim files...")
    modified, claim_edges = apply_edges(edges)
    print(f"Modified {modified} claim files")

    # Stats
    edge_counts = [len(v) for v in claim_edges.values()]
    print(f"Claims with edges: {len(claim_edges)}")
    print(f"Edges per claim: min={min(edge_counts)}, max={max(edge_counts)}, avg={sum(edge_counts)/len(edge_counts):.1f}")

    # Top 10 densest claims
    by_density = sorted(claim_edges.items(), key=lambda x: -len(x[1]))
    print("\nTop 10 densest claims:")
    for slug, edges_list in by_density[:10]:
        print(f"  {slug[:60]}: {len(edges_list)} edges")


if __name__ == '__main__':
    main()
