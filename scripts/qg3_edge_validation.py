#!/usr/bin/env python3
"""
Quality Gate 3: Phase 3 edge validation.
Three checks:
  1. EDGE INTEGRITY — verify all edge wikilinks resolve to existing claim files
  2. EDGE DENSITY  — compute edge counts per domain, flag orphans
  3. EDGE TYPE DISTRIBUTION — verify all edge types represented
"""

import os
import re
import sys
from collections import defaultdict

CLAIMS_DIR = os.path.expanduser("~/Projects/Personal/OSKG-IBD/notes/claims")

# Known edge type headings in claim files -> canonical edge type name
EDGE_HEADINGS = {
    "Depends on": "depends_on",
    "Supports": "supports",
    "Extends": "extends",
    "Operationalizes": "operationalizes",
    "Challenged by": "challenged_by",
    "Contradicts": "contradicts",
}

# Wikilink pattern: [[slug|description]]  or  [[slug]]
WIKILINK_RE = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')


def parse_claim(filepath):
    """Parse a claim file, returning (claim_slug, metadata, edges, domain)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Get claim slug from filename
    filename = os.path.basename(filepath)
    slug = filename.replace('.md', '')

    # Extract domain from tags (first tag starting with domain/)
    domain = "unknown"
    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        fm = frontmatter_match.group(1)
        for line in fm.split('\n'):
            m = re.match(r'\s*-\s*domain/(\S+)', line)
            if m:
                domain = m.group(1)
                break

    # Extract edges from the ## Edges section
    edges_match = re.search(r'## Edges\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    edges = defaultdict(list)
    if edges_match:
        edges_section = edges_match.group(1)
        current_type = None
        for line in edges_section.split('\n'):
            line_stripped = line.strip()
            # Check if this is a heading line
            heading_found = False
            for heading, etype in EDGE_HEADINGS.items():
                if line_stripped.startswith(f'**{heading}:**') or line_stripped.startswith(f'**{heading}**'):
                    current_type = etype
                    heading_found = True
                    # Extract wikilinks from the heading line itself
                    for match in WIKILINK_RE.finditer(line_stripped):
                        edges[current_type].append((match.group(1), line_stripped))
                    break
            if heading_found:
                continue
            # Check if this is a list item under the current heading
            if line_stripped.startswith('-') and current_type:
                for match in WIKILINK_RE.finditer(line_stripped):
                    edges[current_type].append((match.group(1), line_stripped))

    # Flatten edges into a simple list for density counting
    edge_count = sum(len(v) for v in edges.values())

    return slug, domain, edges, edge_count


def main():
    print("=" * 70)
    print("QUALITY GATE 3: Phase 3 Edge Validation")
    print("=" * 70)

    # Collect all claim files (exclude index files)
    claim_files = sorted([
        os.path.join(CLAIMS_DIR, f)
        for f in os.listdir(CLAIMS_DIR)
        if f.endswith('.md') and f.startswith('claim-')
    ])
    print(f"\nClaim files found: {len(claim_files)}")

    # Build set of valid slugs
    valid_slugs = set()
    for fp in claim_files:
        slug = os.path.basename(fp).replace('.md', '')
        valid_slugs.add(slug)

    # Parse all claims
    all_claims = {}
    for fp in claim_files:
        slug, domain, edges, edge_count = parse_claim(fp)
        all_claims[slug] = {
            'filepath': fp,
            'domain': domain,
            'edges': edges,
            'edge_count': edge_count,
        }

    # =========================================================================
    # CHECK 1: EDGE INTEGRITY
    # =========================================================================
    print("\n" + "=" * 70)
    print("CHECK 1: EDGE INTEGRITY — Wikilink Resolution")
    print("=" * 70)

    broken_edges = []
    total_edges = 0
    edge_type_counts = defaultdict(int)

    for slug, claim_data in all_claims.items():
        for etype, targets in claim_data['edges'].items():
            for target_slug, context in targets:
                total_edges += 1
                edge_type_counts[etype] += 1
                if target_slug not in valid_slugs:
                    broken_edges.append({
                        'source': slug,
                        'target': target_slug,
                        'type': etype,
                        'context': context.strip(),
                    })

    print(f"Total edges found: {total_edges}")
    print(f"Broken wikilinks: {len(broken_edges)}")

    if broken_edges:
        print("\n--- BROKEN EDGES ---")
        for be in broken_edges:
            print(f"  [{be['type']}] {be['source']} -> {be['target']}")
            print(f"    Context: {be['context']}")
    else:
        print("  PASS — All edge wikilinks resolve to existing claim files.")

    # =========================================================================
    # CHECK 2: EDGE DENSITY
    # =========================================================================
    print("\n" + "=" * 70)
    print("CHECK 2: EDGE DENSITY — Per-Domain Analysis")
    print("=" * 70)

    domain_counts = defaultdict(lambda: {'claims': 0, 'edges': 0})
    orphans = []

    for slug, claim_data in all_claims.items():
        dom = claim_data['domain']
        domain_counts[dom]['claims'] += 1
        domain_counts[dom]['edges'] += claim_data['edge_count']
        if claim_data['edge_count'] == 0:
            orphans.append(slug)

    print(f"\n{'Domain':<30} {'Claims':>8} {'Total Edges':>13} {'Edges/Claim':>12}")
    print("-" * 65)
    for dom in sorted(domain_counts.keys()):
        dc = domain_counts[dom]
        ratio = dc['edges'] / dc['claims'] if dc['claims'] > 0 else 0
        flag = " *** UNDER 1.0" if ratio < 1.0 else ""
        print(f"{dom:<30} {dc['claims']:>8} {dc['edges']:>13} {ratio:>11.2f}{flag}")

    total_claims = len(all_claims)
    avg_edges = total_edges / total_claims if total_claims > 0 else 0
    print(f"\n{'OVERALL':<30} {total_claims:>8} {total_edges:>13} {avg_edges:>11.2f}")

    print(f"\nOrphan claims (zero edges): {len(orphans)}")
    if len(orphans) <= 20:
        for o in sorted(orphans):
            print(f"  {o}")
    else:
        print(f"  (first 30 shown out of {len(orphans)})")
        for o in sorted(orphans)[:30]:
            print(f"  {o}")

    # =========================================================================
    # CHECK 3: EDGE TYPE DISTRIBUTION
    # =========================================================================
    print("\n" + "=" * 70)
    print("CHECK 3: EDGE TYPE DISTRIBUTION")
    print("=" * 70)

    expected_types = set(EDGE_HEADINGS.values())
    found_types = set(edge_type_counts.keys())
    missing = expected_types - found_types

    print(f"\n{'Edge Type':<25} {'Count':>8} {'%':>7}")
    print("-" * 42)
    for etype in sorted(expected_types):
        count = edge_type_counts.get(etype, 0)
        pct = (count / total_edges * 100) if total_edges > 0 else 0
        flag = ""
        if count == 0:
            flag = " *** MISSING"
        elif count <= 3:
            flag = " *** SPARSE (≤3)"
        print(f"{etype:<25} {count:>8} {pct:>6.1f}%{flag}")

    if missing:
        print(f"\nWARNING: Missing edge types: {', '.join(missing)}")

    # Specific flag for contradicts
    contradicts_count = edge_type_counts.get('contradicts', 0)
    if contradicts_count <= 3:
        print(f"\nNOTE: 'contradicts' edges are sparse ({contradicts_count}). "
              f"The graph may be missing the SIBO diagnostic debate or other "
              f"guideline conflicts. Review is warranted.")

    # =========================================================================
    # EXTRA: Connected vs orphaned claims by domain
    # =========================================================================
    print("\n" + "=" * 70)
    print("EXTRA: Orphan Distribution by Domain")
    print("=" * 70)

    domain_orphans = defaultdict(list)
    for slug in orphans:
        dom = all_claims[slug]['domain']
        domain_orphans[dom].append(slug)

    for dom in sorted(domain_orphans.keys()):
        total_in_domain = domain_counts[dom]['claims']
        num_orphans = len(domain_orphans[dom])
        pct = (num_orphans / total_in_domain * 100) if total_in_domain > 0 else 0
        print(f"  {dom}: {num_orphans}/{total_in_domain} orphaned ({pct:.1f}%)")

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    issues = []
    if broken_edges:
        issues.append(f"{len(broken_edges)} broken wikilink(s)")
    if orphans:
        issues.append(f"{len(orphans)} orphan claim(s) with zero edges")
    if contradicts_count <= 3:
        issues.append(f"sparse 'contradicts' edges ({contradicts_count}) — possible missed debates")
    for dom in domain_counts:
        ratio = domain_counts[dom]['edges'] / domain_counts[dom]['claims']
        if ratio < 1.0:
            issues.append(f"domain '{dom}' under 1.0 edges/claim ({ratio:.2f})")

    if issues:
        print("Issues found:")
        for i in issues:
            print(f"  - {i}")
        print(f"\n  FAIL — {len(issues)} issue(s) need attention.")
    else:
        print("  PASS — All checks passed.")

    return 0 if not broken_edges else 1


if __name__ == '__main__':
    sys.exit(main())
