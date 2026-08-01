#!/usr/bin/env python3
"""Batch 4+5 claim extraction: Microbiome & SIBO + Nutrition notes."""
import re, os
from pathlib import Path

BASE = "/home/littleseneca/Projects/Personal/OSKG-IBD"
CLAIMS_DIR = f"{BASE}/notes/claims"
os.makedirs(CLAIMS_DIR, exist_ok=True)

def standardize_confidence(conf_text):
    if not conf_text: return "medium"
    conf = conf_text.strip().upper()
    mapping = {"VERY HIGH": "very-high", "HIGH": "high", "MEDIUM-HIGH": "medium-high",
               "MEDIUM": "medium", "LOW-MEDIUM": "low-medium", "LOW": "low", "DEBATABLE": "debatable"}
    for key, val in mapping.items():
        if key in conf: return val
    return "medium"

def get_topic_tags(text, config):
    tags = []
    t = text.lower()
    domain = config.get('domain', '')
    
    if domain == "microbiome":
        tags.append("topic/microbiome")
    elif domain == "nutrition":
        tags.append("topic/diet")
    
    kw = [
        (["sibo"], "topic/sibo"),
        (["imo", "methanogen"], "topic/imo"),
        (["ibs", "irritable bowel"], "topic/ibs"),
        (["crohn"], "topic/crohns-disease"),
        (["ulcerative colitis", "uc "], "topic/ulcerative-colitis"),
        (["ibd"], "topic/ibd"),
        (["dysbiosis"], "topic/dysbiosis"),
        (["microbiome", "microbiota", "microbial"], "topic/microbiome"),
        (["inflammat"], "topic/inflammation"),
        (["autoimmun", "anti-vinculin", "cdtb", "vinculin"], "topic/autoimmunity"),
        (["breath test", "hydrogen", "methane", "lactulose"], "topic/breath-testing"),
        (["food poison", "gastroenteritis", "campylobacter", "salmonella", "shigella"], "topic/autoimmunity"),
        (["mmc", "migrating motor complex", "motility", "cleaning wave", "housekeeper"], "topic/microbiome"),
        (["probiotic"], "topic/probiotics"),
        (["fmt", "fecal transplant"], "topic/fmt"),
        (["antibiotic", "rifaximin", "metronidazole"], "topic/antibiotics"),
        (["scd", "specific carbohydrate diet"], "topic/scd"),
        (["low-fodmap", "fodmap"], "topic/low-fodmap"),
        (["lfe", "low-fermentation"], "topic/lfe"),
        (["elemental diet", "een", "enteral nutrition", "formula"], "topic/elemental-diet"),
        (["gaps", "gut and psychology"], "topic/gaps"),
        (["paleo", "autoimmune protocol", "aip"], "topic/paleo"),
        (["ssfg", "sibo specific food"], "topic/ssfg"),
        (["carbohydrate", "disaccharidase", "malabsorption", "fermentation"], "topic/carbohydrate-malabsorption"),
        (["fermentation"], "topic/microbial-fermentation"),
        (["vicious cycle"], "topic/microbial-fermentation"),
        (["genetic", "gwas", "nod2"], "topic/genetics"),
        (["immune", "cytokine", "t cell", "th1", "th17"], "topic/immune-dysregulation"),
        (["barrier", "epithelial", "tight junction", "permeability", "leaky gut"], "topic/epithelial-barrier"),
        (["diagnos"], "topic/diagnosis"),
        (["treat", "therapy", "protocol", "management"], "topic/treatment"),
        (["epidemiology", "incidence", "prevalence"], "topic/epidemiology"),
    ]
    for keywords, tag in kw:
        if any(kw in t for kw in keywords):
            if tag not in tags: tags.append(tag)
    return tags[:5]

def get_evidence_tags(text, config):
    tags = []
    t = text.lower()
    st = config.get('source_type', '')
    if st == "textbook": tags.append("evidence/systematic-review")
    elif st == "guide": tags.append("evidence/expert-consensus")
    
    kw = [
        (["meta-analysis"], "evidence/meta-analysis"),
        (["rct", "randomized"], "evidence/rct"),
        (["systematic review"], "evidence/systematic-review"),
        (["cohort", "observational"], "evidence/cohort"),
        (["animal model", "mouse", "germ-free", "il10"], "evidence/animal-model"),
        (["in vitro", "biochemical", "pathway", "molecular"], "evidence/mechanistic"),
        (["expert consensus", "clinical experience"], "evidence/expert-consensus"),
        (["case series", "case report"], "evidence/case-series"),
        (["reimagine", "gwas"], "evidence/gwas" if "gwas" in t else "evidence/cohort"),
    ]
    for keywords, tag in kw:
        if any(kw in t for kw in keywords):
            if tag not in tags: tags.append(tag)
    if not tags: tags.append("evidence/expert-consensus")
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
    if stmt: sections['statement'] = stmt.group(1).strip()
    
    ev = re.search(r'\*\*Evidence (?:presented|summary):\*\*\s*(.+?)(?=\*\*Confidence|\*\*GRADE|\*\*What\'s at stake|\*\*Comparison|\*\*My assessment)', claim_block, re.DOTALL)
    if ev: sections['evidence'] = ev.group(1).strip()
    
    conf = re.search(r'\*\*Confidence:\*\*\s*(.+?)(?=\*\*What\'s at stake|\*\*Who disagrees|\*\*Alternative|\*\*My assessment)', claim_block, re.DOTALL)
    if conf: sections['confidence_raw'] = conf.group(1).strip()
    
    stakes = re.search(r'\*\*What\'s at stake:\*\*\s*(.+?)(?=\*\*Who disagrees|\*\*Alternative|\*\*My assessment)', claim_block, re.DOTALL)
    if stakes: sections['stakes'] = stakes.group(1).strip()
    
    disag = re.search(r'\*\*Who disagrees:\*\*\s*(.+?)(?=\*\*Alternative reading|\*\*My assessment)', claim_block, re.DOTALL)
    if disag: sections['disagreement'] = disag.group(1).strip()
    
    alt = re.search(r'\*\*Alternative reading:\*\*\s*(.+?)(?=\*\*My assessment)', claim_block, re.DOTALL)
    if alt: sections['alternative'] = alt.group(1).strip()
    
    assess = re.search(r'\*\*My assessment:\*\*\s*(.+?)$', claim_block, re.DOTALL)
    if assess: sections['assessment'] = assess.group(1).strip()
    
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
    ctype = config.get('default_type', 'mechanistic')
    if config['domain'] == 'nutrition': ctype = 'dietary'
    if any(w in full_text.lower() for w in ['diagnos', 'breath test']): ctype = 'diagnostic'
    if any(w in full_text.lower() for w in ['treat', 'therapy', 'antibiotic', 'protocol']): ctype = 'therapeutic'
    
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
    print(f"Processing: {Path(note_path).name}")
    
    with open(note_path, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    pattern = re.compile(r'^(#{2,3})\s+Claim\s+(\d+):\s*(.+)$', re.MULTILINE)
    matches = list(pattern.finditer(full_text))
    
    if not matches:
        print(f"  SKIP: No claim headers found")
        return 0
    
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
    
    print(f"  {len(matches)} claims")
    return len(matches)


# === Batch 4+5 Configuration ===

NOTES = [
    # --- Microbiome & SIBO (Batch 4) ---
    {"path": f"{BASE}/notes/microbiome/Pimentel 2022 - Intro Ch1 IBS and SIBO Overlap.md", "source_slug": "pimentel-ch1", "source_tag": "source/pimentel-microbiome-connection", "domain": "microbiome", "source_type": "textbook", "scholars": ["scholar/pimentel", "scholar/rezaie"], "source_note": "Pimentel 2022 - Intro Ch1 IBS and SIBO Overlap", "source_citation": "Pimentel & Rezaie — The Microbiome Connection (2022), Intro + Ch1"},
    {"path": f"{BASE}/notes/microbiome/Pimentel 2022 - Ch2 Gut Anatomy and MMC.md", "source_slug": "pimentel-ch2", "source_tag": "source/pimentel-microbiome-connection", "domain": "microbiome", "source_type": "textbook", "scholars": ["scholar/pimentel", "scholar/rezaie"], "source_note": "Pimentel 2022 - Ch2 Gut Anatomy and MMC", "source_citation": "Pimentel & Rezaie — The Microbiome Connection (2022), Ch 2"},
    {"path": f"{BASE}/notes/microbiome/Pimentel 2022 - Ch3 Gut Microbiome.md", "source_slug": "pimentel-ch3", "source_tag": "source/pimentel-microbiome-connection", "domain": "microbiome", "source_type": "textbook", "scholars": ["scholar/pimentel", "scholar/rezaie"], "source_note": "Pimentel 2022 - Ch3 Gut Microbiome", "source_citation": "Pimentel & Rezaie — The Microbiome Connection (2022), Ch 3"},
    {"path": f"{BASE}/notes/microbiome/Pimentel 2022 - Ch4 Food Poisoning Autoimmunity.md", "source_slug": "pimentel-ch4", "source_tag": "source/pimentel-microbiome-connection", "domain": "microbiome", "source_type": "textbook", "scholars": ["scholar/pimentel", "scholar/rezaie"], "source_note": "Pimentel 2022 - Ch4 Food Poisoning Autoimmunity", "source_citation": "Pimentel & Rezaie — The Microbiome Connection (2022), Ch 4"},
    {"path": f"{BASE}/notes/microbiome/Pimentel 2022 - Ch5 SIBO Definition and Diagnosis.md", "source_slug": "pimentel-ch5", "source_tag": "source/pimentel-microbiome-connection", "domain": "microbiome", "source_type": "textbook", "scholars": ["scholar/pimentel", "scholar/rezaie"], "source_note": "Pimentel 2022 - Ch5 SIBO Definition and Diagnosis", "source_citation": "Pimentel & Rezaie — The Microbiome Connection (2022), Ch 5"},
    {"path": f"{BASE}/notes/microbiome/Pimentel 2022 - Ch6 Three Pillars of SIBO Management.md", "source_slug": "pimentel-ch6", "source_tag": "source/pimentel-microbiome-connection", "domain": "microbiome", "source_type": "textbook", "scholars": ["scholar/pimentel", "scholar/rezaie"], "source_note": "Pimentel 2022 - Ch6 Three Pillars of SIBO Management", "source_citation": "Pimentel & Rezaie — The Microbiome Connection (2022), Ch 6"},
    {"path": f"{BASE}/notes/microbiome/Pimentel 2022 - Ch9 Refractory SIBO.md", "source_slug": "pimentel-ch9", "source_tag": "source/pimentel-microbiome-connection", "domain": "microbiome", "source_type": "textbook", "scholars": ["scholar/pimentel", "scholar/rezaie"], "source_note": "Pimentel 2022 - Ch9 Refractory SIBO", "source_citation": "Pimentel & Rezaie — The Microbiome Connection (2022), Ch 9"},
    {"path": f"{BASE}/notes/microbiome/Pimentel 2022 - Ch10-11 Probiotics FMT and Myths.md", "source_slug": "pimentel-ch10", "source_tag": "source/pimentel-microbiome-connection", "domain": "microbiome", "source_type": "textbook", "scholars": ["scholar/pimentel", "scholar/rezaie"], "source_note": "Pimentel 2022 - Ch10-11 Probiotics FMT and Myths", "source_citation": "Pimentel & Rezaie — The Microbiome Connection (2022), Ch 10-11"},
    {"path": f"{BASE}/notes/microbiome/The Microbiome Solution - Chutkan - Intro Ch1-3.md", "source_slug": "chutkan-found", "source_tag": "source/chutkan-microbiome-solution", "domain": "microbiome", "source_type": "guide", "scholars": ["scholar/chutkan"], "source_note": "The Microbiome Solution - Chutkan - Intro Ch1-3", "source_citation": "Chutkan — The Microbiome Solution (2015), Intro + Ch 1-3"},
    {"path": f"{BASE}/notes/microbiome/The Microbiome Solution - Chutkan - Ch5 Dysbiosis.md", "source_slug": "chutkan-dysbiosis", "source_tag": "source/chutkan-microbiome-solution", "domain": "microbiome", "source_type": "guide", "scholars": ["scholar/chutkan"], "source_note": "The Microbiome Solution - Chutkan - Ch5 Dysbiosis", "source_citation": "Chutkan — The Microbiome Solution (2015), Ch 5"},
    {"path": f"{BASE}/notes/microbiome/The Microbiome Solution - Chutkan - Ch11 Rewilding Illness.md", "source_slug": "chutkan-rewild", "source_tag": "source/chutkan-microbiome-solution", "domain": "microbiome", "source_type": "guide", "scholars": ["scholar/chutkan"], "source_note": "The Microbiome Solution - Chutkan - Ch11 Rewilding Illness", "source_citation": "Chutkan — The Microbiome Solution (2015), Ch 11"},
    
    # --- Nutrition (Batch 5) ---
    {"path": f"{BASE}/notes/nutrition/Gottschall 1994 - Foreword.md", "source_slug": "gottschall-fw", "source_tag": "source/gottschall-btv", "domain": "nutrition", "source_type": "guide", "scholars": ["scholar/gottschall"], "source_note": "Gottschall 1994 - Foreword", "source_citation": "Gottschall — Breaking the Vicious Cycle (1994), Foreword"},
    {"path": f"{BASE}/notes/nutrition/Gottschall 1994 - Ch1-2 Origins and Scientific Evidence.md", "source_slug": "gottschall-ch12", "source_tag": "source/gottschall-btv", "domain": "nutrition", "source_type": "guide", "scholars": ["scholar/gottschall"], "source_note": "Gottschall 1994 - Ch1-2 Origins and Scientific Evidence", "source_citation": "Gottschall — Breaking the Vicious Cycle (1994), Ch 1-2"},
    {"path": f"{BASE}/notes/nutrition/Gottschall 1994 - Ch3-5 The Vicious Cycle Mechanism.md", "source_slug": "gottschall-ch35", "source_tag": "source/gottschall-btv", "domain": "nutrition", "source_type": "guide", "scholars": ["scholar/gottschall"], "source_note": "Gottschall 1994 - Ch3-5 The Vicious Cycle Mechanism", "source_citation": "Gottschall — Breaking the Vicious Cycle (1994), Ch 3-5"},
    {"path": f"{BASE}/notes/nutrition/Gottschall 1994 - Ch9-10 Implementing the SCD.md", "source_slug": "gottschall-ch910", "source_tag": "source/gottschall-btv", "domain": "nutrition", "source_type": "guide", "scholars": ["scholar/gottschall"], "source_note": "Gottschall 1994 - Ch9-10 Implementing the SCD", "source_citation": "Gottschall — Breaking the Vicious Cycle (1994), Ch 9-10"},
    {"path": f"{BASE}/notes/nutrition/Foote 2020 - Crohn's Disease Cookbook.md", "source_slug": "foote-cookbook", "source_tag": "source/foote-cookbook", "domain": "nutrition", "source_type": "guide", "scholars": ["scholar/foote"], "source_note": "Foote 2020 - Crohn's Disease Cookbook", "source_citation": "Foote — Crohn's Disease AIP Cookbook (2020)"},
    {"path": f"{BASE}/notes/nutrition/Thompson 2013 - Elemental Diet Protocol.md", "source_slug": "thompson-een", "source_tag": "source/thompson-een", "domain": "nutrition", "source_type": "guide", "scholars": ["scholar/thompson"], "source_note": "Thompson 2013 - Elemental Diet Protocol", "source_citation": "Thompson — The IBD Remission Diet (2013)"},
    {"path": f"{BASE}/notes/nutrition/Sarna 2021 - Healing SIBO Dietary Protocol.md", "source_slug": "sarna-sibo-diet", "source_tag": "source/sarna-sibo-diet", "domain": "nutrition", "source_type": "guide", "scholars": ["scholar/sarna"], "source_note": "Sarna 2021 - Healing SIBO Dietary Protocol", "source_citation": "Lapine (Sarna) — SIBO Made Simple (2021), Dietary Protocol"},
    {"path": f"{BASE}/notes/nutrition/Pimentel 2022 - Low-Fermentation Eating.md", "source_slug": "pimentel-lfe", "source_tag": "source/pimentel-microbiome-connection", "domain": "nutrition", "source_type": "textbook", "scholars": ["scholar/pimentel", "scholar/rezaie"], "source_note": "Pimentel 2022 - Low-Fermentation Eating", "source_citation": "Pimentel & Rezaie — The Microbiome Connection (2022), LFE"},
    {"path": f"{BASE}/notes/nutrition/Gut and Physiology Syndrome - Campbell-McBride - GAPS Protocol.md", "source_slug": "campbell-gaps", "source_tag": "source/campbell-mcbride-gaps", "domain": "nutrition", "source_type": "guide", "scholars": ["scholar/campbell-mcbride"], "source_note": "Gut and Physiology Syndrome - Campbell-McBride - GAPS Protocol", "source_citation": "Campbell-McBride — Gut and Physiology Syndrome (2020), GAPS Protocol"},
]

total = 0
for cfg in NOTES:
    n = process_note(cfg)
    total += n

print(f"\n=== BATCHES 4+5 COMPLETE: {total} claims extracted ===")
