# OSKG-IBD

An open-source knowledge graph for Inflammatory Bowel Disease (IBD) and Small Intestinal Bacterial Overgrowth (SIBO), built on the [OSKG methodology](https://github.com/LittleSeneca/OSKG-Methodology). Structured evidence synthesis connecting pathophysiology, diagnosis, treatment, microbiome science, clinical guidelines, and dietary interventions into a typed-claim graph.

## What This Is

A structured decomposition of the IBD/SIBO literature into discrete, verifiable claims with typed edges (supports, contradicts, extends, depends_on). Think of it as a machine-readable evidence map — every claim traces to its source, every edge documents the relationship between claims.

## Why IBD and SIBO

IBD affects millions globally. SIBO is increasingly recognized as a key driver of IBS symptoms and a potential co-morbidity in IBD patients with persistent symptoms despite remission. The literature spans gastroenterology, immunology, microbiology, nutrition science, and clinical guidelines — domains that rarely talk to each other. A knowledge graph bridges them.

SIBO is particularly interesting as a knowledge graph subject: its definition is contested, its diagnosis methods are debated, and its relationship to IBD is an active area of research. The graph captures this uncertainty explicitly via confidence ratings and contradictory edges.

## Pipeline

| Phase | Artifact |
|-------|----------|
| 0 | Source acquisition and extraction |
| 1 | Chapter/section reading notes |
| 2 | Claims extraction with intra-batch edges |
| 3 | Cross-source edge construction |
| 4 | Synthesis: hinge inventory, cascade trees, structural gaps |
| 5 | Capstone: evidence-grounded synthesis |

## Repo Structure

```
notes/
├── pathophysiology/    Disease mechanisms, genetics, immune dysfunction
├── diagnosis/          Endoscopy, biomarkers, breath testing
├── treatment/          Pharmacological, biologic, surgical
├── microbiome/         Gut flora, dysbiosis, SIBO/IMO mechanisms
├── nutrition/          Diet interventions, EEN, SCD, LFE
├── clinical-guidelines/ ACG, AGA, ECCO, Rome Foundation
├── history/            Evolution of IBD/SIBO understanding
├── claims/             Discrete claim nodes
├── evidence-briefs/    Synthesized evidence on specific questions
├── questions/          Open research questions
└── synthesis/          Capstone documents

sources/
├── books/              Textbooks and patient guides
├── guidelines/         Clinical practice guidelines
└── papers/             Research papers and reviews
```

See [BOOK-GUIDE.md](BOOK-GUIDE.md) for the full source corpus.

## License

This project is for research and educational purposes. Source texts remain under their original copyrights.
