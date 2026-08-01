#!/usr/bin/env python3
"""Batch 3 claim extraction: Clinical Guidelines (11 guidelines, ~125 claims)."""
import re
import os
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
    domain = config.get('domain', 'clinical-guidelines')
    
    # Identify condition
    if any(w in t for w in ["crohn", "cd patient"]):
        tags.append("topic/crohns-disease")
    elif any(w in t for w in ["ulcerative colitis", "uc patient"]):
        tags.append("topic/ulcerative-colitis")
    elif any(w in t for w in ["sibo", "small intestinal bacterial", "breath test"]):
        tags.append("topic/sibo")
    elif any(w in t for w in ["ibd"]):
        tags.append("topic/ibd")
    
    # Diagnosis tags
    kw_diag = [
        (["endoscopy", "colonoscopy", "ileocolonoscopy", "mucosal healing"], "topic/endoscopy"),
        (["imaging", "cte", "mre", "mri", "ultrasound"], "topic/imaging"),
        (["biomarker", "calprotectin", "crp", "fecal", "serolog"], "topic/biomarkers"),
        (["breath test", "hydrogen", "methane", "lactulose", "glucose breath"], "topic/breath-testing"),
        (["histolog", "biopsy", "granuloma"], "topic/histology"),
        (["differential", "ibd-u", "indeterminate"], "topic/differential-diagnosis"),
    ]
    for keywords, tag in kw_diag:
        if any(kw in t for kw in keywords):
            if tag not in tags: tags.append(tag)
    
    # Treatment tags
    kw_tx = [
        (["5-asa", "mesalamine", "sulfasalazine"], "topic/5-asa"),
        (["steroid", "corticosteroid", "prednisone", "budesonide"], "topic/corticosteroids"),
        (["immunomodulator", "thiopurine", "azathioprine", "6-mp", "methotrexate"], "topic/immunomodulators"),
        (["biologic", "anti-tnf", "infliximab", "adalimumab"], "topic/biologics"),
        (["anti-tnf"], "topic/anti-tnf"),
        (["vedolizumab", "anti-integrin"], "topic/anti-integrin"),
        (["ustekinumab", "anti-il", "il-12/23"], "topic/anti-il12-23"),
        (["tofacitinib", "jak inhibitor", "upadacitinib"], "topic/jak-inhibitors"),
        (["antibiotic", "rifaximin", "metronidazole"], "topic/antibiotics"),
        (["surgery", "colectomy", "resection", "ipaa", "strictureplasty"], "topic/surgery"),
        (["therapeutic drug monitoring", "tdm", "drug level"], "topic/therapeutic-drug-monitoring"),
        (["treat-to-target", "tight control", "stride"], "topic/treat-to-target"),
        (["step-up", "top-down"], "topic/step-up-vs-top-down"),
        (["mucosal healing", "endoscopic remission"], "topic/mucosal-healing"),
    ]
    for keywords, tag in kw_tx:
        if any(kw in t for kw in keywords):
            if tag not in tags: tags.append(tag)
    
    # Other
    if any(w in t for w in ["grade", "evidence quality", "recommendation"]):
        if "topic/grade" not in tags: tags.append("topic/grade")
    if any(w in t for w in ["epidemiology", "incidence", "prevalence", "risk factor"]):
        tags.append("topic/epidemiology")
    if not tags: tags.append("topic/ibd")
    
    return tags[:5]

def get_evidence_tags(text, config):
    tags = ["evidence/clinical-guideline"]
    t = text.lower()
    kw = [
        (["meta-analysis"], "evidence/meta-analysis"),
        (["rct", "randomized"], "evidence/rct"),
        (["systematic review"], "evidence/systematic-review"),
        (["cohort", "observational"], "evidence/cohort"),
        (["expert consensus", "key concept", "not graded"], "evidence/expert-consensus"),
        (["very low quality", "low quality of evidence"], "evidence/expert-consensus"),
    ]
    for keywords, tag in kw:
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
        clean = ''.join(c for c in w if c.isalnum() or c == '-')
        if clean and clean not in stop and len(clean) > 2:
            key_words.append(clean)
    slug_words = key_words[:7]
    if not slug_words: slug_words = ["claim"]
    slug = '-'.join(slug_words)
    slug = f"claim-{slug}"
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')
    if len(slug) > 80: slug = slug[:80].rstrip('-')
    return slug

def extract_sections(claim_block):
    sections = {}
    stmt = re.search(r'(?:\*\*Author\'s claim:\*\*|\*\*Recommendation:\*\*)\s*"([^"]+)"', claim_block, re.DOTALL)
    if not stmt:
        stmt = re.search(r'(?:\*\*Author\'s claim:\*\*|\*\*Recommendation:\*\*)\s*(.+?)(?:\n\n|\*\*Confidence|\*\*GRADE|\*\*Evidence)', claim_block, re.DOTALL)
    if stmt:
        sections['statement'] = stmt.group(1).strip()
    
    ev = re.search(r'\*\*Evidence (?:presented|summary):\*\*\s*(.+?)(?=\*\*Confidence|\*\*GRADE|\*\*What\'s at stake|\*\*Comparison|\*\*My assessment)', claim_block, re.DOTALL)
    if ev: sections['evidence'] = ev.group(1).strip()
    
    grade = re.search(r'\*\*GRADE rating:\*\*\s*(.+?)(?=\n\n|\*\*)', claim_block, re.DOTALL)
    if grade: sections['grade'] = grade.group(1).strip()
    
    conf = re.search(r'\*\*Confidence:\*\*\s*(.+?)(?=\*\*What\'s at stake|\*\*Who disagrees|\*\*Alternative|\*\*My assessment)', claim_block, re.DOTALL)
    if conf: sections['confidence_raw'] = conf.group(1).strip()
    
    stakes = re.search(r'\*\*What\'s at stake:\*\*\s*(.+?)(?=\*\*Who disagrees|\*\*Alternative|\*\*My assessment)', claim_block, re.DOTALL)
    if stakes: sections['stakes'] = stakes.group(1).strip()
    
    disag = re.search(r'\*\*Who disagrees:\*\*\s*(.+?)(?=\*\*Alternative reading|\*\*My assessment)', claim_block, re.DOTALL)
    if disag: sections['disagreement'] = disag.group(1).strip()
    
    alt = re.search(r'\*\*Alternative reading:\*\*\s*(.+?)(?=\*\*My assessment)', claim_block, re.DOTALL)
    if alt: sections['alternative'] = alt.group(1).strip()
    
    # Comparison section (guidelines-specific)
    comp = re.search(r'\*\*Comparison against other guidelines:\*\*\s*(.+?)(?=\*\*My assessment)', claim_block, re.DOTALL)
    if comp: sections['comparison'] = comp.group(1).strip()
    
    assess = re.search(r'\*\*My assessment:\*\*\s*(.+?)$', claim_block, re.DOTALL)
    if assess: sections['assessment'] = assess.group(1).strip()
    
    return sections

def build_claim_file(slug, claim_id, claim_title, statement, sections, config):
    tags = ["type/claim", "oskg-ibd"]
    full_text = statement + ' ' + sections.get('evidence', '') + ' ' + sections.get('comparison', '')
    tags.extend(get_topic_tags(full_text, config))
    tags.extend(get_evidence_tags(full_text, config))
    tags.extend(config.get('scholars', []))
    tags.append(config['source_tag'])
    tags.append(f"domain/clinical-guidelines")
    tags.append(f"society/{config.get('society', 'unknown')}")
    
    confidence = standardize_confidence(sections.get('confidence_raw', ''))
    
    ctype = determine_type(full_text, config)
    
    evidence_text = sections.get('evidence', 'See source note.')
    # Append GRADE rating if present
    if sections.get('grade'):
        evidence_text = f"**GRADE rating:** {sections['grade']}\n\n{evidence_text}"
    if sections.get('comparison'):
        evidence_text += f"\n\n**Cross-guideline comparison:**\n{sections['comparison']}"
    
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

def determine_type(text, config):
    t = text.lower()
    if any(w in t for w in ["diagnos", "breath test", "endoscopy", "imaging", "biomarker", "calprotectin"]):
        return "diagnostic"
    if any(w in t for w in ["treat", "therapy", "drug", "surgery", "biologic", "antibiotic", "steroid"]):
        return "therapeutic"
    if any(w in t for w in ["define", "classification", "is a", "refers to"]):
        return "definitional"
    if any(w in t for w in ["epidemiology", "incidence", "prevalence", "risk factor"]):
        return "epidemiological"
    if any(w in t for w in ["grade", "recommendation", "evidence quality"]):
        return "methodological"
    return "therapeutic"

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
        
        print(f"  [{claim_num}] {claim_id}")
    
    return len(matches)


# === Batch 3 Configuration ===

BATCH3 = [
    {
        "path": f"{BASE}/notes/clinical-guidelines/ACG Crohn's 2018 - Lichtenstein.md",
        "source_slug": "acg-cd2018",
        "source_tag": "source/acg-crohns-2018",
        "society": "acg",
        "scholars": ["scholar/lichtenstein"],
        "source_note": "ACG Crohn's 2018 - Lichtenstein",
        "source_citation": "Lichtenstein et al. — ACG Clinical Guideline: Management of Crohn's Disease (2018)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/ACG UC 2019 - Rubin.md",
        "source_slug": "acg-uc2019",
        "source_tag": "source/acg-uc-2019",
        "society": "acg",
        "scholars": ["scholar/rubin"],
        "source_note": "ACG UC 2019 - Rubin",
        "source_citation": "Rubin et al. — ACG Clinical Guideline: Ulcerative Colitis (2019)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/ACG SIBO 2020 - Pimentel.md",
        "source_slug": "acg-sibo2020",
        "source_tag": "source/acg-sibo-2020",
        "society": "acg",
        "scholars": ["scholar/pimentel"],
        "source_note": "ACG SIBO 2020 - Pimentel",
        "source_citation": "Pimentel et al. — ACG Clinical Guideline: Small Intestinal Bacterial Overgrowth (2020)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/AGA SIBO 2020 - Quigley.md",
        "source_slug": "aga-sibo2020",
        "source_tag": "source/aga-sibo-2020",
        "society": "aga",
        "scholars": ["scholar/quigley"],
        "source_note": "AGA SIBO 2020 - Quigley",
        "source_citation": "Quigley et al. — AGA Clinical Practice Update: Small Intestinal Bacterial Overgrowth (2020)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/AGA UC 2020 - Feuerstein.md",
        "source_slug": "aga-uc2020",
        "source_tag": "source/aga-uc-2020",
        "society": "aga",
        "scholars": ["scholar/feuerstein"],
        "source_note": "AGA UC 2020 - Feuerstein",
        "source_citation": "Feuerstein et al. — AGA Clinical Practice Guidelines: Ulcerative Colitis (2020)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/AGA Crohn's 2021 - Feuerstein.md",
        "source_slug": "aga-cd2021",
        "source_tag": "source/aga-cd-2021",
        "society": "aga",
        "scholars": ["scholar/feuerstein"],
        "source_note": "AGA Crohn's 2021 - Feuerstein",
        "source_citation": "Feuerstein et al. — AGA Clinical Practice Guidelines: Crohn's Disease (2021)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/ECCO Diagnostic 2019 - Maaser.md",
        "source_slug": "ecco-diag2019",
        "source_tag": "source/ecco-diagnostic-2019",
        "society": "ecco",
        "scholars": ["scholar/maaser"],
        "source_note": "ECCO Diagnostic 2019 - Maaser",
        "source_citation": "Maaser et al. — ECCO-ESGAR Guideline for Diagnostic Assessment in IBD (2019)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/ECCO Crohn's Medical 2020 - Torres.md",
        "source_slug": "ecco-cd2020",
        "source_tag": "source/ecco-cd-2020",
        "society": "ecco",
        "scholars": ["scholar/torres"],
        "source_note": "ECCO Crohn's Medical 2020 - Torres",
        "source_citation": "Torres et al. — ECCO Guidelines on Crohn's Disease: Medical Management (2020)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/ECCO UC Therapeutics 2022 - Raine.md",
        "source_slug": "ecco-uc2022",
        "source_tag": "source/ecco-uc-2022",
        "society": "ecco",
        "scholars": ["scholar/raine"],
        "source_note": "ECCO UC Therapeutics 2022 - Raine",
        "source_citation": "Raine et al. — ECCO Guidelines on Ulcerative Colitis: Therapeutics (2022)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/Rome Foundation SIBO Report 2017.md",
        "source_slug": "rome-sibo2017",
        "source_tag": "source/rome-sibo-2017",
        "society": "rome",
        "scholars": ["scholar/pimentel"],
        "source_note": "Rome Foundation SIBO Report 2017",
        "source_citation": "Rome Foundation Working Team — SIBO: Rome Foundation Working Team Report (2017)",
    },
    {
        "path": f"{BASE}/notes/clinical-guidelines/BSG IBD 2019 - Lamb.md",
        "source_slug": "bsg-ibd2019",
        "source_tag": "source/bsg-ibd-2019",
        "society": "bsg",
        "scholars": ["scholar/lamb"],
        "source_note": "BSG IBD 2019 - Lamb",
        "source_citation": "Lamb et al. — BSG Consensus Guidelines on the Management of IBD (2019)",
    },
]

total = 0
for cfg in BATCH3:
    n = process_note(cfg)
    total += n

print(f"\n=== BATCH 3 COMPLETE: {total} claims extracted ===")
