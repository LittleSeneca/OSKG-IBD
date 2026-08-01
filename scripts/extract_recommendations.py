#!/usr/bin/env python3
"""
Extract individual recommendation claims from clinical guideline recommendation tables.
Parses | R# | Population | Recommendation | Strength | Quality | tables (5-column)
and   | R# | Recommendation | Strength | Quality | tables (4-column).

Each individual recommendation becomes a discrete claim file.
"""
import re, os
from pathlib import Path

BASE = "/home/littleseneca/Projects/Personal/OSKG-IBD"
CLAIMS_DIR = f"{BASE}/notes/claims"
os.makedirs(CLAIMS_DIR, exist_ok=True)

def grade_to_confidence(quality):
    mapping = {
        'high': 'very-high',
        'moderate': 'high',
        'low': 'medium',
        'very low': 'low-medium',
        'very-low': 'low-medium',
    }
    q = quality.strip().lower().replace('*', '')
    return mapping.get(q, 'medium')

def write_rec_claim(rec_num, rec_text, strength, quality, population, source_note, source_citation, cfg):
    """Write a single recommendation claim file."""
    claim_id = f"{cfg['source_slug']}-rec{rec_num}"
    slug = f"{cfg['source_slug']}-r{rec_num}-{rec_text[:50].lower()}"
    slug = re.sub(r'[^a-z0-9-]', '-', slug)[:80].strip('-')

    confidence = grade_to_confidence(quality)
    
    tags = ["type/claim", "oskg-ibd", "domain/clinical-guidelines"]
    tags.extend(cfg.get('topic_tags', []))
    tags.extend(cfg.get('evidence_tags', []))
    tags.extend(cfg.get('scholars', []))
    tags.append(cfg['source_tag'])
    tags.append('society/' + cfg.get('society', 'unknown'))
    tags.append('methodology/grade')

    tag_lines = "\n  - ".join(tags)
    
    quality_label = quality.strip()
    evidence_text = f"GRADE quality of evidence: **{quality_label}**. Strength of recommendation: **{strength}**."
    pop_text = population.strip() if population else 'Not specified'
    statement = rec_text[:200]

    content = f"""---
tags:
  - {tag_lines}
claim_id: "{claim_id}"
statement: "{statement}"
confidence: "{confidence}"
confidence_rationale: "GRADE quality: {quality_label}. Strength: {strength}."
claim_type: "therapeutic"
source_note: "[[{source_note}]]"
created: 2026-08-01
updated: 2026-08-01
status: active
---

# {claim_id}: {rec_text[:120]}

**Source:** [[{source_note}]] — {source_citation}

## The Claim

**Recommendation {rec_num}** ({strength}, quality: {quality_label})

{rec_text}

**Target population:** {pop_text}

## Evidence

{evidence_text}

See source note for full evidence evaluation, supporting trial references, and cross-guideline comparison.

## Confidence

**Rating:** {confidence}
**Rationale:** Based on GRADE quality rating of {quality_label} and recommendation strength: {strength}.

## Stakes

Individual recommendation-level analysis. See source note for clinical implications.

## Disagreement

**Who disagrees:** See source note for inter-guideline comparison.

**Alternative reading:** Not documented.

## Edges

<!-- Populate during cross-source edge pass -->

**Depends on:**

**Supports:**

**Contradicts:**

**Challenged by:**

## Assessment

Individual recommendation extracted from guideline table. See source note for full clinical assessment.
"""
    path = os.path.join(CLAIMS_DIR, f"claim-{slug}.md")
    if os.path.exists(path):
        return None
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

def extract_recs_from_table(text):
    """Parse recommendation table rows. Handles both 4-column and 5-column formats."""
    recs = []
    for line in text.split('\n'):
        # Strip markdown formatting
        line = line.strip()
        if not line.startswith('|'):
            continue
        
        # Split by pipes
        parts = [p.strip() for p in line.split('|')]
        # Remove leading/trailing empty strings
        parts = [p for p in parts if p]
        
        if len(parts) < 4:
            continue
        
        # First part should look like R# or a number
        first = parts[0]
        if not re.match(r'^R?\d+[a-z]?$', first):
            continue
        
        rec_num = re.sub(r'^R', '', first)
        
        if len(parts) == 4:
            # Format: | R# | Recommendation | Strength | Quality |
            rec_text = parts[1]
            strength = parts[2]
            quality = parts[3].replace('**', '')
            population = ''
        elif len(parts) == 5:
            # Format: | R# | Population | Recommendation | Strength | Quality |
            population = parts[1]
            rec_text = parts[2]
            strength = parts[3]
            quality = parts[4].replace('**', '')
        else:
            continue
        
        # Validate strength/quality
        strength_clean = strength.strip().title()
        if strength_clean not in ['Strong', 'Conditional', 'Weak']:
            continue
        
        # Skip header rows
        if rec_text.lower() in ['recommendation', 'population']:
            continue
        
        recs.append((rec_num, rec_text, strength_clean, quality, population))
    
    return recs

# ============================================================
# Guideline configurations
# ============================================================

GUIDELINES = [
    {
        "path": f"{BASE}/notes/clinical-guidelines/ACG Crohn's 2018 - Lichtenstein.md",
        "source_slug": "acg-cd2018",
        "source_tag": "source/acg-crohns-2018",
        "society": "acg",
        "scholars": ["scholar/lichtenstein"],
        "topic_tags": ["topic/crohns-disease", "topic/grade", "topic/treatment"],
        "evidence_tags": ["evidence/clinical-guideline"],
        "source_note": "ACG Crohn's 2018 - Lichtenstein",
        "source_citation": "Lichtenstein et al. — ACG Clinical Guideline: Crohn's Disease (2018)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/ACG UC 2019 - Rubin.md",
        "source_slug": "acg-uc2019",
        "source_tag": "source/acg-uc-2019",
        "society": "acg",
        "scholars": ["scholar/rubin"],
        "topic_tags": ["topic/ulcerative-colitis", "topic/grade", "topic/treatment"],
        "evidence_tags": ["evidence/clinical-guideline"],
        "source_note": "ACG UC 2019 - Rubin",
        "source_citation": "Rubin et al. — ACG Clinical Guideline: Ulcerative Colitis (2019)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/AGA UC 2020 - Feuerstein.md",
        "source_slug": "aga-uc2020",
        "source_tag": "source/aga-uc-2020",
        "society": "aga",
        "scholars": ["scholar/feuerstein"],
        "topic_tags": ["topic/ulcerative-colitis", "topic/grade", "topic/treatment"],
        "evidence_tags": ["evidence/clinical-guideline"],
        "source_note": "AGA UC 2020 - Feuerstein",
        "source_citation": "Feuerstein et al. — AGA Clinical Practice Guidelines: UC (2020)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/AGA Crohn's 2021 - Feuerstein.md",
        "source_slug": "aga-cd2021",
        "source_tag": "source/aga-crohns-2021",
        "society": "aga",
        "scholars": ["scholar/feuerstein"],
        "topic_tags": ["topic/crohns-disease", "topic/grade", "topic/treatment"],
        "evidence_tags": ["evidence/clinical-guideline"],
        "source_note": "AGA Crohn's 2021 - Feuerstein",
        "source_citation": "Feuerstein et al. — AGA Clinical Practice Guidelines: Crohn's Disease (2021)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/ECCO Crohn's Medical 2020 - Torres.md",
        "source_slug": "ecco-cd2020",
        "source_tag": "source/ecco-crohns-2020",
        "society": "ecco",
        "scholars": ["scholar/torres"],
        "topic_tags": ["topic/crohns-disease", "topic/grade", "topic/treatment"],
        "evidence_tags": ["evidence/clinical-guideline"],
        "source_note": "ECCO Crohn's Medical 2020 - Torres",
        "source_citation": "Torres et al. — ECCO Guidelines: Crohn's Disease Medical Treatment (2020)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/ECCO UC Therapeutics 2022 - Raine.md",
        "source_slug": "ecco-uc2022",
        "source_tag": "source/ecco-uc-2022",
        "society": "ecco",
        "scholars": ["scholar/raine"],
        "topic_tags": ["topic/ulcerative-colitis", "topic/grade", "topic/treatment"],
        "evidence_tags": ["evidence/clinical-guideline"],
        "source_note": "ECCO UC Therapeutics 2022 - Raine",
        "source_citation": "Raine et al. — ECCO Guidelines: UC Therapeutics (2022)",
    },
]

total_recs = 0
total_written = 0

for cfg in GUIDELINES:
    note_name = Path(cfg['path']).name
    print(f"\n{'='*60}")
    print(f"Extracting: {note_name}")
    print(f"{'='*60}")
    
    with open(cfg['path'], 'r', encoding='utf-8') as f:
        text = f.read()
    
    recs = extract_recs_from_table(text)
    print(f"  Found {len(recs)} recommendations")
    
    skipped = 0
    written = 0
    for rec_num, rec_text, strength, quality, population in recs:
        path = write_rec_claim(
            rec_num, rec_text, strength, quality, population,
            cfg['source_note'], cfg['source_citation'],
            {k: v for k, v in cfg.items() if k != 'path'}
        )
        if path:
            written += 1
            total_written += 1
        else:
            skipped += 1
        total_recs += 1
    
    print(f"  Written: {written}, Skipped (existing): {skipped}")

print(f"\n{'='*60}")
print(f"TOTAL NEW CLAIMS: {total_written}")
print(f"Total recs found: {total_recs}")
print(f"{'='*60}")
