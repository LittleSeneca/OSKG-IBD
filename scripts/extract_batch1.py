#!/usr/bin/env python3
"""Batch 1 claim extraction: Yamada Ch62 (IBD Pathogenesis), Ch63 (UC Diagnosis), Ch64 (CD Diagnosis)."""
import re
import os
import sys
from pathlib import Path

BASE = "/home/littleseneca/Projects/Personal/OSKG-IBD"
CLAIMS_DIR = f"{BASE}/notes/claims"
os.makedirs(CLAIMS_DIR, exist_ok=True)

def standardize_confidence(conf_text):
    if not conf_text:
        return "medium"
    conf = conf_text.strip().upper()
    mapping = {
        "VERY HIGH": "very-high", "HIGH": "high",
        "MEDIUM-HIGH": "medium-high", "MEDIUM": "medium",
        "LOW-MEDIUM": "low-medium", "LOW": "low",
        "DEBATABLE": "debatable",
    }
    for key, val in mapping.items():
        if key in conf:
            return val
    return "medium"

def get_topic_tags(text, config):
    tags = []
    t = text.lower()
    domain = config.get('domain', '')
    
    if domain == "pathophysiology":
        tags.extend(["topic/ibd", "topic/pathogenesis"])
    elif domain == "diagnosis":
        tags.append("topic/diagnosis")
        if any(w in t for w in ["ulcerative colitis", "uc patient", "uc diagnosis"]):
            tags.append("topic/ulcerative-colitis")
        if any(w in t for w in ["crohn", "cd patient", "cd diagnosis"]):
            tags.append("topic/crohns-disease")
    
    kw_map = [
        (["genetic", "gwas", "loci", "heritability", "nod2", "atg16l1", "il23r", "risk allele"], "topic/genetics"),
        (["immune", "t cell", "th1", "th17", "cytokine", "tnf", "il-", "interleukin", "innate", "adaptive immunity"], "topic/immune-dysregulation"),
        (["barrier", "epithelial", "tight junction", "permeability", "leaky gut"], "topic/epithelial-barrier"),
        (["microbiome", "microbial", "dysbiosis", "flora", "commensal"], "topic/microbiome"),
        (["dysbiosis"], "topic/dysbiosis"),
        (["inflammat"], "topic/inflammation"),
        (["autoimmun", "anti-vinculin", "cdtb"], "topic/autoimmunity"),
        (["endoscopy", "colonoscopy", "mucosal healing", "mayo score", "uceis"], "topic/endoscopy"),
        (["cte", "mre", "imaging", "mri", "ct enterography"], "topic/imaging"),
        (["calprotectin", "crp", "biomarker", "serolog", "asca", "panca", "fecal"], "topic/biomarkers"),
        (["histolog", "biopsy", "granuloma", "architectural", "crypt"], "topic/histology"),
        (["differential", "distinguish", "ibd-u", "indeterminate", "mimic"], "topic/differential-diagnosis"),
        (["twin", "concordance", "family history", "epidemiology", "incidence", "prevalence", "smoking"], "topic/epidemiology"),
        (["environment", "trigger", "risk factor"], "topic/environmental-triggers"),
    ]
    for keywords, tag in kw_map:
        if any(kw in t for kw in keywords):
            if tag not in tags:
                tags.append(tag)
    
    return tags[:4]

def get_evidence_tags(text, config):
    tags = []
    t = text.lower()
    st = config.get('source_type', '')
    
    if st == "textbook":
        tags.append("evidence/systematic-review")
    
    kw_map = [
        (["meta-analysis", "meta analysis"], "evidence/meta-analysis"),
        (["randomized", "rct", "randomised"], "evidence/rct"),
        (["gwas", "genome-wide", "genetic loci", "fine mapping"], "evidence/gwas"),
        (["animal model", "mouse", "germ-free", "knockout", "il10-/-"], "evidence/animal-model"),
        (["cohort", "longitudinal", "prospective", "risk cohort"], "evidence/cohort"),
        (["in vitro", "biochemical", "pathway", "molecular"], "evidence/mechanistic"),
        (["expert consensus", "key concept", "not graded"], "evidence/expert-consensus"),
    ]
    for keywords, tag in kw_map:
        if any(kw in t for kw in keywords):
            if tag not in tags:
                tags.append(tag)
    
    return tags[:3]

def generate_slug(statement, claim_num, source_slug):
    stop = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'shall', 'to', 'of', 'in', 'for',
            'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
            'that', 'this', 'these', 'those', 'it', 'its', 'and', 'but', 'or',
            'not', 'no', 'than', 'then', 'also', 'very', 'such', 'each', 'all',
            'which', 'who', 'whom', 'what', 'when', 'where', 'how', 'some', 'any'}
    
    words = statement.lower().split()
    key_words = []
    for w in words:
        clean = w.strip('.,;:()[]{}""\'-')
        if clean and clean not in stop and len(clean) > 2:
            key_words.append(clean)
    
    slug_words = key_words[:7]
    slug = '-'.join(slug_words)
    slug = f"claim-{slug}"
    if len(slug) > 80:
        slug = slug[:80].rstrip('-')
    
    # Add source+claim suffix for uniqueness
    return slug

def extract_sections(claim_block):
    sections = {}
    # Extract quoted statement
    stmt = re.search(r'(?:\*\*Author\'s claim:\*\*|\*\*Recommendation:\*\*)\s*"([^"]+)"', claim_block, re.DOTALL)
    if not stmt:
        stmt = re.search(r'(?:\*\*Author\'s claim:\*\*|\*\*Recommendation:\*\*)\s*(.+?)(?:\n\n|\*\*Confidence|\*\*GRADE|\*\*Evidence)', claim_block, re.DOTALL)
    if stmt:
        sections['statement'] = stmt.group(1).strip()
    
    ev = re.search(r'\*\*Evidence (?:presented|summary):\*\*\s*(.+?)(?=\*\*Confidence|\*\*GRADE|\*\*What\'s at stake|\*\*Comparison|\*\*My assessment)', claim_block, re.DOTALL)
    if ev:
        sections['evidence'] = ev.group(1).strip()
    
    grade = re.search(r'\*\*GRADE rating:\*\*\s*(.+?)(?=\n\n|\*\*)', claim_block, re.DOTALL)
    if grade:
        sections['grade'] = grade.group(1).strip()
    
    conf = re.search(r'\*\*Confidence:\*\*\s*(.+?)(?=\*\*What\'s at stake|\*\*Who disagrees|\*\*Alternative|\*\*My assessment)', claim_block, re.DOTALL)
    if conf:
        sections['confidence_raw'] = conf.group(1).strip()
    
    stakes = re.search(r'\*\*What\'s at stake:\*\*\s*(.+?)(?=\*\*Who disagrees|\*\*Alternative|\*\*My assessment)', claim_block, re.DOTALL)
    if stakes:
        sections['stakes'] = stakes.group(1).strip()
    
    disag = re.search(r'\*\*Who disagrees:\*\*\s*(.+?)(?=\*\*Alternative reading|\*\*My assessment)', claim_block, re.DOTALL)
    if disag:
        sections['disagreement'] = disag.group(1).strip()
    
    alt = re.search(r'\*\*Alternative reading:\*\*\s*(.+?)(?=\*\*My assessment)', claim_block, re.DOTALL)
    if alt:
        sections['alternative'] = alt.group(1).strip()
    
    assess = re.search(r'\*\*My assessment:\*\*\s*(.+?)$', claim_block, re.DOTALL)
    if assess:
        sections['assessment'] = assess.group(1).strip()
    
    return sections

def build_claim_file(slug, claim_id, claim_title, statement, sections, config):
    tags = []
    tags.append("type/claim")
    tags.append("oskg-ibd")
    tags.extend(get_topic_tags(statement + ' ' + sections.get('evidence', ''), config))
    tags.extend(get_evidence_tags(statement + ' ' + sections.get('evidence', ''), config))
    tags.extend(config.get('scholars', []))
    tags.append(config['source_tag'])
    tags.append(f"domain/{config['domain']}")
    
    confidence = standardize_confidence(sections.get('confidence_raw', ''))
    
    ctype = "mechanistic"
    if config['domain'] == "diagnosis":
        ctype = "diagnostic"
    elif "define" in statement.lower()[:50]:
        ctype = "definitional"
    
    evidence_text = sections.get('evidence', 'See source note for full evidence presentation.')
    stakes_text = sections.get('stakes', 'See source note.')
    disag_text = sections.get('disagreement', 'Not documented in source note.')
    alt_text = sections.get('alternative', 'Not documented.')
    assess_text = sections.get('assessment', 'See source note.')
    conf_rationale = sections.get('confidence_raw', '')[:200]
    
    tag_lines = "\n  - ".join(tags)
    
    return f"""---
tags:
  - {tag_lines}
claim_id: "{claim_id}"
statement: "{statement[:200].replace(chr(10), ' ')}"
confidence: "{confidence}"
confidence_rationale: "{conf_rationale.replace(chr(10), ' ')}"
claim_type: "{ctype}"
source_note: "[[{config['source_note']}]]"
created: 2026-08-01
updated: 2026-08-01
status: active
---

# {claim_id}: {claim_title}

**Source:** [[{config['source_note']}]] — {config['source_citation']}

## The Claim

{statement}

## Evidence

{evidence_text}

## Confidence

**Rating:** {confidence}
**Rationale:** {conf_rationale}

## Stakes

{stakes_text}

## Disagreement

**Who disagrees:** {disag_text}

**Alternative reading:** {alt_text}

## Edges

<!-- Populate during batch review and cross-source edge pass -->

**Depends on:**

**Supports:**

**Contradicts:**

**Challenged by:**

## Assessment

{assess_text}
"""

def process_note(config):
    note_path = config['path']
    print(f"\nProcessing: {Path(note_path).name}")
    
    with open(note_path, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    # Find all claim headers (## Claim N: or ### Claim N:)
    pattern = re.compile(r'^(#{2,3})\s+Claim\s+(\d+):\s*(.+)$', re.MULTILINE)
    matches = list(pattern.finditer(full_text))
    
    if not matches:
        print(f"  WARNING: No claims found!")
        return 0
    
    print(f"  Found {len(matches)} claims")
    
    for i, match in enumerate(matches):
        claim_num = match.group(2)
        claim_title = match.group(3).strip()
        start = match.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(full_text)
        claim_block = full_text[start:end]
        
        sections = extract_sections(claim_block)
        statement = sections.get('statement', claim_title)
        
        slug = generate_slug(statement, claim_num, config['source_slug'])
        claim_id = f"{config['source_slug']}-{claim_num}"
        
        claim_content = build_claim_file(slug, claim_id, claim_title, statement, sections, config)
        
        claim_path = os.path.join(CLAIMS_DIR, f"{slug}.md")
        with open(claim_path, 'w', encoding='utf-8') as f:
            f.write(claim_content)
        
        print(f"  [{claim_num}] {claim_id} -> {slug}.md")
    
    return len(matches)


# === Batch 1 Configuration ===

BATCH1 = [
    {
        "path": f"{BASE}/notes/pathophysiology/Yamada 2022 - Ch62 IBD Pathogenesis.md",
        "source_slug": "yamada-ibd62",
        "source_tag": "source/yamada-textbook",
        "domain": "pathophysiology",
        "source_type": "textbook",
        "scholars": ["scholar/ananthakrishnan", "scholar/xavier", "scholar/podolsky"],
        "source_note": "Yamada 2022 - Ch62 IBD Pathogenesis",
        "source_citation": "Ananthakrishnan, Xavier, Podolsky — Yamada's Textbook of Gastroenterology, 7E (2022), Ch 62",
    },
    {
        "path": f"{BASE}/notes/diagnosis/Yamada 2022 - Ch63 Ulcerative Colitis Diagnosis.md",
        "source_slug": "yamada-ucdx63",
        "source_tag": "source/yamada-textbook",
        "domain": "diagnosis",
        "source_type": "textbook",
        "scholars": ["scholar/ananthakrishnan"],
        "source_note": "Yamada 2022 - Ch63 Ulcerative Colitis Diagnosis",
        "source_citation": "Yamada's Textbook of Gastroenterology, 7E (2022), Ch 63",
    },
    {
        "path": f"{BASE}/notes/diagnosis/Yamada 2022 - Ch64 Crohns Disease Diagnosis.md",
        "source_slug": "yamada-cddx64",
        "source_tag": "source/yamada-textbook",
        "domain": "diagnosis",
        "source_type": "textbook",
        "scholars": ["scholar/ananthakrishnan"],
        "source_note": "Yamada 2022 - Ch64 Crohns Disease Diagnosis",
        "source_citation": "Yamada's Textbook of Gastroenterology, 7E (2022), Ch 64",
    },
]

total = 0
for cfg in BATCH1:
    n = process_note(cfg)
    total += n

print(f"\n=== BATCH 1 COMPLETE: {total} claims extracted ===")
