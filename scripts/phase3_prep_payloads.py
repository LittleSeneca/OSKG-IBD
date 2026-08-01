#!/usr/bin/env python3
"""
Phase 3 Pass 2 Prep: Extract claim payloads from cluster manifest.

For each cluster, reads full claim statements from the claim files
and produces a JSON payload file ready for LLM edge detection.
"""

import json, os, re
from pathlib import Path

CLAIMS_DIR = Path("/home/littleseneca/Projects/Personal/OSKG-IBD/notes/claims")
MANIFEST_PATH = Path("/home/littleseneca/Projects/Personal/OSKG-IBD/scripts/manifests/phase3_clusters.json")
PAYLOADS_DIR = Path("/home/littleseneca/Projects/Personal/OSKG-IBD/scripts/manifests/phase3_payloads")
PAYLOADS_DIR.mkdir(parents=True, exist_ok=True)


def read_full_statement(content):
    """Read the full claim from the body's ## The Claim section."""
    m = re.search(r'## The Claim\n\n(.*?)(?:\n\n|\n##|\n---)', content, re.DOTALL)
    if m:
        return m.group(1).strip()
    return None


def extract_evidence(content):
    """Extract evidence excerpt."""
    m = re.search(r'## Evidence\n\n(.*?)(?:\n\n|\n##|\n---)', content, re.DOTALL)
    if m:
        evidence = m.group(1).strip()
        # Truncate to ~300 chars for the payload
        if len(evidence) > 300:
            evidence = evidence[:300] + '...'
        return evidence
    return ''


def main():
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)

    total = 0
    for cluster in manifest['clusters']:
        cluster_id = cluster['id']
        claims = []
        for slug in cluster['claim_slugs']:
            path = CLAIMS_DIR / f"{slug}.md"
            if not path.exists():
                print(f"  WARNING: {slug}.md not found")
                continue
            with open(path) as f:
                content = f.read()

            # Extract frontmatter fields
            fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            fm_text = fm_match.group(1) if fm_match else ''
            fm = {}
            for line in fm_text.split('\n'):
                kv = re.match(r'^(\w[\w_]*):\s*["\']?(.*?)["\']?\s*$', line)
                if kv:
                    fm[kv.group(1)] = kv.group(2)

            # Full statement from body
            full_stmt = read_full_statement(content)
            if not full_stmt:
                full_stmt = fm.get('statement', '')

            evidence = extract_evidence(content)

            claims.append({
                'slug': slug,
                'claim_id': fm.get('claim_id', ''),
                'statement': full_stmt[:400] if len(full_stmt) > 400 else full_stmt,
                'claim_type': fm.get('claim_type', ''),
                'source_note': fm.get('source_note', ''),
                'confidence': fm.get('confidence', ''),
                'evidence_excerpt': evidence,
            })

        # Write cluster payload
        payload = {
            'cluster_id': cluster_id,
            'cluster_label': cluster['label'],
            'domain': cluster.get('domain', ''),
            'size': len(claims),
            'claims': claims,
        }

        out_path = PAYLOADS_DIR / f"{cluster_id}.json"
        with open(out_path, 'w') as f:
            json.dump(payload, f, indent=2)

        total += len(claims)
        print(f"  {cluster_id}: {len(claims)} claims → {out_path.name}")

    print(f"\nTotal: {total} claims across {len(manifest['clusters'])} payloads in {PAYLOADS_DIR}")


if __name__ == '__main__':
    main()
