#!/usr/bin/env python3
"""Extract claims from remaining notes with implicit/non-standard claim formats."""
import re, os
from pathlib import Path

BASE = "/home/littleseneca/Projects/Personal/OSKG-IBD"
CLAIMS_DIR = f"{BASE}/notes/claims"
os.makedirs(CLAIMS_DIR, exist_ok=True)

def write_claim(slug, claim_id, statement, config, extra_sections=None):
    """Write a single claim file."""
    tags = ["type/claim", "oskg-ibd", f"domain/{config['domain']}"]
    tags.extend(config.get('topic_tags', []))
    tags.extend(config.get('evidence_tags', ['evidence/expert-consensus']))
    tags.extend(config.get('scholars', []))
    tags.append(config['source_tag'])
    
    tag_lines = "\n  - ".join(tags)
    
    evidence = extra_sections.get('evidence', 'See source note.') if extra_sections else 'See source note.'
    stakes = extra_sections.get('stakes', 'See source note.') if extra_sections else 'See source note.'
    assess = extra_sections.get('assessment', 'See source note.') if extra_sections else 'See source note.'
    ctype = config.get('default_type', 'mechanistic')
    
    content = f"""---
tags:
  - {tag_lines}
claim_id: "{claim_id}"
statement: "{statement[:200].replace(chr(10), ' ')}"
confidence: "medium"
confidence_rationale: "Extracted from implicit claim structure in source note."
claim_type: "{ctype}"
source_note: "[[{config['source_note']}]]"
created: 2026-08-01
updated: 2026-08-01
status: active
---

# {claim_id}: {statement[:150]}

**Source:** [[{config['source_note']}]] — {config['source_citation']}

## The Claim

{statement}

## Evidence

{evidence}

## Confidence

**Rating:** medium
**Rationale:** See source note for full evidence evaluation.

## Stakes

{stakes}

## Disagreement

**Who disagrees:** Not documented for implicit claims.

**Alternative reading:** Not documented.

## Edges

<!-- Populate during cross-source edge pass -->

**Depends on:**

**Supports:**

**Contradicts:**

**Challenged by:**

## Assessment

{assess}
"""
    slug_clean = ''.join(c for c in slug if c.isalnum() or c == '-')
    if len(slug_clean) > 80: slug_clean = slug_clean[:80].rstrip('-')
    path = os.path.join(CLAIMS_DIR, f"claim-{slug_clean}.md")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

def extract_from_note(note_path, config):
    """Extract claims from a note with implicit structure."""
    with open(note_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    claims = []
    fname = Path(note_path).name
    
    # Strategy depends on source type
    if config.get('extract_pattern') == 'core-thesis':
        # Extract Core Thesis as one claim
        m = re.search(r'## Core Thesis\n\n(.+?)(?=\n## |\n---)', text, re.DOTALL)
        if m:
            thesis = m.group(1).strip()
            slug = 'core-thesis-' + config['source_slug'][:20]
            claims.append((slug, thesis))
    
    elif config.get('extract_pattern') == 'bpa':
        # AGA SIBO format: BPA N: headers
        bpa_matches = re.findall(r'^## (BPA \d+[^:]*):\s*(.+)$', text, re.MULTILINE)
        for i, (bpa_id, bpa_title) in enumerate(bpa_matches):
            slug = f"{config['source_slug']}-{bpa_id.lower().replace(' ', '-')}"
            # Get the paragraph after the BPA header
            pos = text.find(f'## {bpa_id}:')
            next_pos = len(text)
            for m2 in re.finditer(r'^## BPA', text, re.MULTILINE):
                if m2.start() > pos + len(bpa_id) + 10:
                    next_pos = m2.start()
                    break
            block = text[pos:next_pos]
            stmt_match = re.search(r'\*\*BPA [^:]+:\*\*\s*(.+?)(?=\n\n)', block, re.DOTALL)
            if stmt_match:
                claims.append((slug, bpa_id + ': ' + stmt_match.group(1).strip()))
            else:
                claims.append((slug, bpa_id + ': ' + bpa_title))
    
    elif config.get('extract_pattern') == 'structural-claim':
        # Yamada Ch58: "Structural Claim:" headers
        sc_matches = re.findall(r'^## Structural Claim:\s*(.+)$', text, re.MULTILINE)
        for i, title in enumerate(sc_matches):
            slug = f"structural-{config['source_slug']}-{i+1}"
            # Get the paragraph after
            pos = text.find(f'## Structural Claim: {title}')
            next_section = re.search(r'\n## ', text[pos+50:])
            end = pos + 50 + next_section.start() if next_section else len(text)
            block = text[pos:end]
            claims.append((slug, title))
    
    elif config.get('extract_pattern') == 'recommendations':
        # BSG IBD: Recommendations Summary section
        rec_match = re.search(r'### Recommendations Summary\n\n(.+?)(?=\n### |\n## [^R])', text, re.DOTALL)
        if rec_match:
            recs_text = rec_match.group(1)
            # Split into individual recommendations
            items = re.findall(r'(?:^|\n)(\d+\.\s+.+?)(?=\n\d+\.|\n\n\d+|\Z)', recs_text, re.DOTALL)
            for i, item_text in enumerate(items[:5]):  # cap at 5
                clean = item_text.strip()
                words = re.findall(r'[a-zA-Z]+', clean.lower())[:6]
                slug = '-'.join(words) if words else f"bsg-rec-{i+1}"
                claims.append((slug, clean[:300]))
    
    return claims

# === Configuration for remaining notes ===

IMPLICIT_NOTES = [
    # Tier 3 guidelines (high value, non-standard format)
    {
        "path": f"{BASE}/notes/clinical-guidelines/AGA SIBO 2020 - Quigley.md",
        "source_slug": "aga-sibo2020", "source_tag": "source/aga-sibo-2020",
        "domain": "clinical-guidelines", "extract_pattern": "bpa",
        "scholars": ["scholar/quigley"],
        "source_note": "AGA SIBO 2020 - Quigley",
        "source_citation": "Quigley et al. — AGA Clinical Practice Update: SIBO (2020)",
        "topic_tags": ["topic/sibo", "topic/diagnosis", "topic/breath-testing"],
        "default_type": "diagnostic",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/BSG IBD 2019 - Lamb.md",
        "source_slug": "bsg-ibd2019", "source_tag": "source/bsg-ibd-2019",
        "domain": "clinical-guidelines", "extract_pattern": "recommendations",
        "scholars": ["scholar/lamb"],
        "source_note": "BSG IBD 2019 - Lamb",
        "source_citation": "Lamb et al. — BSG Consensus Guidelines: IBD Management (2019)",
        "topic_tags": ["topic/ibd", "topic/treatment"],
        "default_type": "therapeutic",
    },
    # Tier 1: Yamada Ch58 (textbook chapter, has "Structural Claim" headers)
    {
        "path": f"{BASE}/notes/microbiome/Yamada Ch58 - Bacterial Overgrowth Textbook.md",
        "source_slug": "yamada-sibo58", "source_tag": "source/yamada-textbook",
        "domain": "microbiome", "extract_pattern": "structural-claim",
        "scholars": ["scholar/ananthakrishnan"],
        "source_note": "Yamada Ch58 - Bacterial Overgrowth Textbook",
        "source_citation": "Yamada's Textbook of Gastroenterology, 7E (2022), Ch 58",
        "topic_tags": ["topic/sibo", "topic/microbiome", "topic/diagnosis"],
        "default_type": "definitional",
    },
    # Tier 1: Pimentel 2006 evolution note
    {
        "path": f"{BASE}/notes/microbiome/Pimentel 2006 - SIBO Theory Evolution 2006-2022.md",
        "source_slug": "pimentel-evol", "source_tag": "source/pimentel-ibs-solution",
        "domain": "microbiome", "extract_pattern": "core-thesis",
        "scholars": ["scholar/pimentel"],
        "source_note": "Pimentel 2006 - SIBO Theory Evolution 2006-2022",
        "source_citation": "Pimentel — A New IBS Solution (2006) vs The Microbiome Connection (2022)",
        "topic_tags": ["topic/sibo", "topic/ibs", "topic/autoimmunity"],
        "default_type": "mechanistic",
    },
    # Tier 2-4: Whole-book notes (extract core thesis only)
    {
        "path": f"{BASE}/notes/microbiome/Sarna 2021 - Healing SIBO Patient Guide.md",
        "source_slug": "sarna-sibo-guide", "source_tag": "source/sarna-sibo-guide",
        "domain": "microbiome", "extract_pattern": "core-thesis",
        "scholars": ["scholar/sarna"],
        "source_note": "Sarna 2021 - Healing SIBO Patient Guide",
        "source_citation": "Lapine (Sarna) — SIBO Made Simple (2021)",
        "topic_tags": ["topic/sibo", "topic/diet", "topic/treatment"],
        "default_type": "therapeutic",
    },
    {
        "path": f"{BASE}/notes/microbiome/LaPine 2021 - SIBO Made Simple Cookbook.md",
        "source_slug": "lapine-cookbook", "source_tag": "source/lapine-cookbook",
        "domain": "nutrition", "extract_pattern": "core-thesis",
        "scholars": ["scholar/lapine"],
        "source_note": "LaPine 2021 - SIBO Made Simple Cookbook",
        "source_citation": "Lapine — SIBO Made Simple (2021), Cookbook",
        "topic_tags": ["topic/sibo", "topic/diet", "topic/low-fodmap", "topic/scd"],
        "default_type": "dietary",
    },
    {
        "path": f"{BASE}/notes/microbiome/The Good Gut - Sonnenburg 2015.md",
        "source_slug": "sonnenburg-gut", "source_tag": "source/sonnenburg-good-gut",
        "domain": "microbiome", "extract_pattern": "core-thesis",
        "scholars": ["scholar/sonnenburg"],
        "source_note": "The Good Gut - Sonnenburg 2015",
        "source_citation": "Sonnenburg & Sonnenburg — The Good Gut (2015)",
        "topic_tags": ["topic/microbiome", "topic/diet"],
        "default_type": "mechanistic",
    },
    {
        "path": f"{BASE}/notes/microbiome/Microbiome Science Context - Enders Mayer Bulsiewicz Yong.md",
        "source_slug": "context-microbiome", "source_tag": "source/context-microbiome-science",
        "domain": "microbiome", "extract_pattern": "core-thesis",
        "scholars": ["scholar/enders", "scholar/mayer", "scholar/bulsiewicz", "scholar/yong"],
        "source_note": "Microbiome Science Context - Enders Mayer Bulsiewicz Yong",
        "source_citation": "Enders, Mayer, Bulsiewicz, Yong — Microbiome Science Context (2015-2020)",
        "topic_tags": ["topic/microbiome", "topic/dysbiosis", "topic/diet"],
        "default_type": "mechanistic",
    },
    {
        "path": f"{BASE}/notes/history/Inflamed - Marya Patel 2021.md",
        "source_slug": "marya-inflamed", "source_tag": "source/marya-patel-inflamed",
        "domain": "history", "extract_pattern": "core-thesis",
        "scholars": ["scholar/marya", "scholar/patel"],
        "source_note": "Inflamed - Marya Patel 2021",
        "source_citation": "Marya & Patel — Inflamed: Deep Medicine and the Anatomy of Injustice (2021)",
        "topic_tags": ["topic/ibd", "topic/inflammation", "topic/social-determinants", "topic/epidemiology"],
        "default_type": "epidemiological",
    },
    {
        "path": f"{BASE}/notes/nutrition/The Paleo Approach - Ballantyne 2013.md",
        "source_slug": "ballantyne-paleo", "source_tag": "source/ballantyne-paleo-approach",
        "domain": "nutrition", "extract_pattern": "core-thesis",
        "scholars": ["scholar/ballantyne"],
        "source_note": "The Paleo Approach - Ballantyne 2013",
        "source_citation": "Ballantyne — The Paleo Approach (2013)",
        "topic_tags": ["topic/diet", "topic/paleo", "topic/autoimmunity"],
        "default_type": "dietary",
    },
    {
        "path": f"{BASE}/notes/nutrition/The Autoimmune Solution - Myers 2015.md",
        "source_slug": "myers-autoimmune", "source_tag": "source/myers-autoimmune-solution",
        "domain": "nutrition", "extract_pattern": "core-thesis",
        "scholars": ["scholar/myers"],
        "source_note": "The Autoimmune Solution - Myers 2015",
        "source_citation": "Myers — The Autoimmune Solution (2015)",
        "topic_tags": ["topic/diet", "topic/autoimmunity", "topic/sibo"],
        "default_type": "dietary",
    },
]

total = 0
for cfg in IMPLICIT_NOTES:
    print(f"\nProcessing: {Path(cfg['path']).name} (pattern: {cfg.get('extract_pattern')})")
    claims = extract_from_note(cfg['path'], cfg)
    
    for slug_orig, statement in claims:
        # Clean slug
        slug = re.sub(r'[^a-z0-9-]', '-', slug_orig.lower())[:70]
        slug = slug.strip('-')
        if not slug: slug = f"implicit-{cfg['source_slug']}-{total}"
        
        claim_id = f"{cfg['source_slug']}-implicit-{total+1}"
        
        path = write_claim(slug, claim_id, statement, cfg)
        total += 1
        print(f"  [{total}] {claim_id}")
    
    if not claims:
        print(f"  No claims extracted")

print(f"\n=== IMPLICIT CLAIMS EXTRACTED: {total} ===")
