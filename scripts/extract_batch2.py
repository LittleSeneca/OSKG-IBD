#!/usr/bin/env python3
"""Batch 2 claim extraction: Treatment notes (Steinhart + Yamada)."""
import re
import os
import sys
from pathlib import Path

BASE = "/home/littleseneca/Projects/Personal/OSKG-IBD"
CLAIMS_DIR = f"{BASE}/notes/claims"
os.makedirs(CLAIMS_DIR, exist_ok=True)

def standardize_confidence(conf_text):
    if not conf_text: return "medium"
    conf = conf_text.strip().upper()
    mapping = {
        "VERY HIGH": "very-high", "HIGH": "high",
        "MEDIUM-HIGH": "medium-high", "MEDIUM": "medium",
        "LOW-MEDIUM": "low-medium", "LOW": "low",
        "DEBATABLE": "debatable",
    }
    for key, val in mapping.items():
        if key in conf: return val
    return "medium"

def get_topic_tags(text, config):
    tags = []
    t = text.lower()
    tags.append("topic/treatment")
    tags.append("topic/ibd")
    
    kw_map = [
        (["5-asa", "mesalamine", "sulfasalazine", "mesalazine"], "topic/5-asa"),
        (["corticosteroid", "steroid", "prednisone", "budesonide", "hydrocortisone"], "topic/corticosteroids"),
        (["immunomodulator", "thiopurine", "azathioprine", "6-mp", "mercaptopurine", "methotrexate", "cyclosporine"], "topic/immunomodulators"),
        (["biologic", "anti-tnf", "infliximab", "adalimumab", "certolizumab", "golimumab"], "topic/biologics"),
        (["anti-tnf", "tnf inhibitor", "tnf-alpha"], "topic/anti-tnf"),
        (["vedolizumab", "anti-integrin", "natalizumab", "integrin"], "topic/anti-integrin"),
        (["ustekinumab", "anti-il-12", "anti-il12/23", "il-12/23"], "topic/anti-il12-23"),
        (["jak inhibitor", "tofacitinib", "upadacitinib", "janus kinase"], "topic/jak-inhibitors"),
        (["antibiotic", "rifaximin", "metronidazole", "ciprofloxacin"], "topic/antibiotics"),
        (["surgery", "surgical", "colectomy", "ipaa", "strictureplasty", "resection", "ostomy"], "topic/surgery"),
        (["probiotic"], "topic/probiotics"),
        (["fmt", "fecal transplant", "microbiota transplantation"], "topic/fmt"),
        (["therapeutic drug monitoring", "tdm", "drug level", "antibody"], "topic/therapeutic-drug-monitoring"),
        (["treat-to-target", "mucosal healing", "tight control", "stride"], "topic/treat-to-target"),
        (["top-down", "step-up", "accelerated step"], "topic/step-up-vs-top-down"),
        (["mucosal healing", "endoscopic remission"], "topic/mucosal-healing"),
        (["risk stratification", "disease course", "prognostic"], "topic/risk-stratification"),
        (["crohn"], "topic/crohns-disease"),
        (["ulcerative colitis", "uc "], "topic/ulcerative-colitis"),
    ]
    for keywords, tag in kw_map:
        if any(kw in t for kw in keywords):
            if tag not in tags: tags.append(tag)
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
        (["systematic review"], "evidence/systematic-review"),
        (["cohort", "longitudinal", "prospective", "observational"], "evidence/cohort"),
        (["clinical trial", "controlled trial"], "evidence/rct"),
        (["mechanistic", "pathway", "molecular", "in vitro"], "evidence/mechanistic"),
        (["expert consensus", "key concept"], "evidence/expert-consensus"),
    ]
    for keywords, tag in kw_map:
        if any(kw in t for kw in keywords):
            if tag not in tags: tags.append(tag)
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
        # Aggressively strip anything that isn't alphanumeric or hyphen
        clean = ''.join(c for c in w if c.isalnum() or c == '-')
        if clean and clean not in stop and len(clean) > 2:
            key_words.append(clean)
    
    slug_words = key_words[:7]
    if not slug_words:
        slug_words = ["claim"]
    slug = '-'.join(slug_words)
    slug = f"claim-{slug}"
    # Remove any remaining non-alphanumeric/hyphen chars
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')
    if len(slug) > 80:
        slug = slug[:80].rstrip('-')
    return slug

def extract_sections(claim_block):
    sections = {}
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
    tags = ["type/claim", "oskg-ibd"]
    full_text = statement + ' ' + sections.get('evidence', '')
    tags.extend(get_topic_tags(full_text, config))
    tags.extend(get_evidence_tags(full_text, config))
    tags.extend(config.get('scholars', []))
    tags.append(config['source_tag'])
    tags.append(f"domain/{config['domain']}")
    
    confidence = standardize_confidence(sections.get('confidence_raw', ''))
    ctype = "therapeutic"
    
    evidence_text = sections.get('evidence', 'See source note.')
    stakes_text = sections.get('stakes', 'See source note.')
    disag_text = sections.get('disagreement', 'Not documented.')
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


# === Batch 2 Configuration ===

BATCH2 = [
    {
        "path": f"{BASE}/notes/treatment/Steinhart 2018 - Ch7 Drug Therapy.md",
        "source_slug": "steinhart-drug",
        "source_tag": "source/steinhart-crohns-colitis",
        "domain": "treatment",
        "source_type": "textbook",
        "scholars": ["scholar/steinhart"],
        "source_note": "Steinhart 2018 - Ch7 Drug Therapy",
        "source_citation": "Steinhart — Crohn's and Colitis: Understanding and Managing IBD, 3E (2018), Ch 7",
    },
    {
        "path": f"{BASE}/notes/treatment/Steinhart 2018 - Ch8 Surgical Treatment.md",
        "source_slug": "steinhart-surg",
        "source_tag": "source/steinhart-crohns-colitis",
        "domain": "treatment",
        "source_type": "textbook",
        "scholars": ["scholar/steinhart"],
        "source_note": "Steinhart 2018 - Ch8 Surgical Treatment",
        "source_citation": "Steinhart — Crohn's and Colitis: Understanding and Managing IBD, 3E (2018), Ch 8",
    },
    {
        "path": f"{BASE}/notes/treatment/Yamada 7E - Ch63 UC Clinical Manifestations and Management.md",
        "source_slug": "yamada-uc63",
        "source_tag": "source/yamada-textbook",
        "domain": "treatment",
        "source_type": "textbook",
        "scholars": ["scholar/ananthakrishnan"],
        "source_note": "Yamada 7E - Ch63 UC Clinical Manifestations and Management",
        "source_citation": "Yamada's Textbook of Gastroenterology, 7E (2022), Ch 63",
    },
    {
        "path": f"{BASE}/notes/treatment/Yamada 7E - Ch64 Crohn's Disease Management.md",
        "source_slug": "yamada-cd64",
        "source_tag": "source/yamada-textbook",
        "domain": "treatment",
        "source_type": "textbook",
        "scholars": ["scholar/ananthakrishnan"],
        "source_note": "Yamada 7E - Ch64 Crohn's Disease Management",
        "source_citation": "Yamada's Textbook of Gastroenterology, 7E (2022), Ch 64",
    },
    {
        "path": f"{BASE}/notes/treatment/Yamada 7E - Ch65 Surgical Treatment of IBD.md",
        "source_slug": "yamada-surg65",
        "source_tag": "source/yamada-textbook",
        "domain": "treatment",
        "source_type": "textbook",
        "scholars": ["scholar/ananthakrishnan"],
        "source_note": "Yamada 7E - Ch65 Surgical Treatment of IBD",
        "source_citation": "Yamada's Textbook of Gastroenterology, 7E (2022), Ch 65",
    },
]

total = 0
for cfg in BATCH2:
    n = process_note(cfg)
    total += n

print(f"\n=== BATCH 2 COMPLETE: {total} claims extracted ===")
