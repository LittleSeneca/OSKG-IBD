#!/usr/bin/env python3
"""
Phase 3 Pass 2 Verify: validate edge JSON files before application.

Checks:
  - Valid JSON
  - Required fields present (claim_a, claim_b, edge_type, rationale)
  - Valid edge_types
  - Slugs exist in payload directory
  - No intra-source edges (both claims from same document)
  - No duplicate unordered pairs
  - Rationale length
"""

import json, os, re, sys
from pathlib import Path
from collections import defaultdict

PAYLOADS_DIR = Path("/home/littleseneca/Projects/Personal/OSKG-IBD/scripts/manifests/phase3_payloads")

VALID_EDGE_TYPES = {'supports', 'contradicts', 'extends', 'depends_on', 'operationalizes', 'challenged_by'}


def load_payload_index():
    """Build {slug: {source_note, ...}} lookup from all payloads."""
    index = {}
    for fname in os.listdir(PAYLOADS_DIR):
        if not fname.endswith('.json'):
            continue
        with open(PAYLOADS_DIR / fname) as f:
            p = json.load(f)
        for claim in p.get('claims', []):
            slug = claim['slug']
            index[slug] = {
                'claim_id': claim.get('claim_id', ''),
                'source_note': claim.get('source_note', ''),
            }
    return index


def extract_document(source_note):
    """Extract document-level identifier from source_note wikilink."""
    # Remove [[ ]] and extract document name
    doc = source_note.replace('[[', '').replace(']]', '').strip()
    # Normalize: use everything before ' - ' as the document key
    # e.g., "ACG Crohn's 2018 - Lichtenstein" → "ACG Crohn's 2018"
    # But preserve enough to distinguish same-org docs
    return doc  # full title is the document key


def verify_edge_file(edge_path, payload_index):
    with open(edge_path) as f:
        try:
            edges = json.load(f)
        except json.JSONDecodeError as e:
            return [f"Invalid JSON: {e}"]

    if not isinstance(edges, list):
        return ["Root must be a JSON array"]

    errors = []
    seen_pairs = set()

    for i, edge in enumerate(edges):
        # Required fields
        for field in ('claim_a', 'claim_b', 'edge_type', 'rationale'):
            if field not in edge:
                errors.append(f"Edge {i}: missing field '{field}'")
                continue

        a, b = edge.get('claim_a', ''), edge.get('claim_b', '')
        etype = edge.get('edge_type', '')
        rationale = edge.get('rationale', '')

        # Valid edge type
        if etype not in VALID_EDGE_TYPES:
            errors.append(f"Edge {i}: invalid edge_type '{etype}'")

        # Slugs exist
        if a not in payload_index:
            errors.append(f"Edge {i}: slug '{a}' not found in payloads")
        if b not in payload_index:
            errors.append(f"Edge {i}: slug '{b}' not found in payloads")

        # Intra-source check
        if a in payload_index and b in payload_index:
            doc_a = extract_document(payload_index[a]['source_note'])
            doc_b = extract_document(payload_index[b]['source_note'])
            if doc_a == doc_b:
                errors.append(f"Edge {i}: INTRA-SOURCE — both claims from '{doc_a}'")

        # Duplicate check (unordered)
        pair = tuple(sorted([a, b]))
        if pair in seen_pairs:
            errors.append(f"Edge {i}: duplicate pair {pair}")
        seen_pairs.add(pair)

        # Rationale length
        if len(rationale) < 10:
            errors.append(f"Edge {i}: rationale too short ({len(rationale)} chars)")

    return errors


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <edge_file.json>")
        sys.exit(1)

    edge_path = Path(sys.argv[1])
    if not edge_path.exists():
        print(f"Edge file not found: {edge_path}")
        sys.exit(1)

    print(f"Loading payload index...")
    payload_index = load_payload_index()
    print(f"  {len(payload_index)} slugs indexed")

    print(f"\nVerifying {edge_path.name}...")
    errors = verify_edge_file(edge_path, payload_index)

    with open(edge_path) as f:
        edges = json.load(f)

    print(f"\n  Total edges: {len(edges)}")
    if errors:
        print(f"  ERRORS: {len(errors)}")
        for e in errors:
            print(f"    - {e}")
        sys.exit(1)
    else:
        # Stats
        type_counts = defaultdict(int)
        for e in edges:
            type_counts[e['edge_type']] += 1
        print(f"  Edge types: {dict(type_counts)}")
        print(f"  ALL CHECKS PASSED")


if __name__ == '__main__':
    main()
