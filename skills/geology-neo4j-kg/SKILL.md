---
name: geology-neo4j-kg
description: Build or extend geology-domain knowledge graphs from PDF, OCR, Word, and web reports, especially rare-earth, rare-metal, and metallogenic literature, using an evidence-backed workflow for ontology setup, batch extraction, normalization, review flags, and Neo4j Desktop/Aura export. Use when Codex needs to turn unstructured geology reports into JSON extractions, merged graph facts, or import-ready Cypher for Neo4j.
---

# Geology Neo4j KG

Use this skill to run a repeatable geology knowledge-graph pipeline:

1. lock ontology and extraction contract
2. extract entities, relations, properties, and evidence by batch
3. merge and normalize across reports
4. keep uncertain items in `review_flags`
5. export only the desired confidence slice to Neo4j

## Quick Start

- If the schema is not fixed yet, read [references/schema.md](references/schema.md) before extracting anything.
- If the user is sending a new batch of reports, read [references/workflow.md](references/workflow.md) and follow the batch pipeline in order.
- If the user wants prompt wording or reusable request templates, read [references/prompt-templates.md](references/prompt-templates.md).
- If normalized JSON already exists and the task is to create Neo4j import files, use `scripts/build_neo4j_cypher.py`.

## Working Rules

- Keep the ontology small in v1. Add classes only when repeated facts justify them.
- Preserve sentence-level evidence for every relation whenever possible.
- Prefer normalized JSON as the exchange layer; generate Cypher or CSV only after review and merge.
- Separate high-confidence facts from uncertain or inferred knowledge.
- Never silently drop ambiguities. Record them in `review_flags`.
- When adding new reports to an existing graph, merge into the current normalized JSON instead of exporting directly from raw extraction batches.

## Batch Workflow

### 1. Fix the extraction target

- Confirm graph goal: retrieval, analysis, or report support.
- Confirm scope: rare earth, rare metals, metallogenic belts, profiles, stratigraphy, or another bounded subset.
- Reuse the current ontology where possible. Read [references/schema.md](references/schema.md) for the existing rare-earth-oriented core.

### 2. Extract by chunk

- Work report-by-report and chunk-by-chunk, not whole-PDF in one step.
- Output one JSON object per chunk with:
  - source identifiers
  - `entities`
  - `relations`
  - `review_flags`
- Keep `name` as canonical form and `original_text` as source wording.
- Put measurements and grades in structured `properties`, not in labels or prose.

### 3. Normalize and merge

- Merge aliases, abbreviations, and alternate spellings into canonical ids.
- Keep region scale, stratigraphic level, and deposit scope distinct unless the text explicitly collapses them.
- Carry forward source batches, source ids, and evidence sentences.
- Exclude or flag facts when:
  - confidence is low
  - relation direction is unclear
  - ontology fit is uncertain
  - two reports conflict

### 4. Export to Neo4j

- Export from merged normalized JSON, not from raw extraction batches.
- Use `scripts/build_neo4j_cypher.py` for deterministic Cypher generation.
- By default:
  - keep only high-confidence facts
  - exclude targets touched by `review_flags`
  - prune unconnected entities
- Generate a separate display-update Cypher when the user wants Chinese display fields in Neo4j Desktop.

Example:

```powershell
@'
python "C:\Users\86180\.codex\skills\geology-neo4j-kg\scripts\build_neo4j_cypher.py" `
  --input-json "C:\path\to\roundX_merged_normalized.json" `
  --output-cypher "C:\path\to\roundX_high_confidence.cypher" `
  --summary-out "C:\path\to\roundX_high_confidence_summary.json" `
  --display-zh-out "C:\path\to\roundX_display_zh.cypher" `
  --entity-confidence-min 0.9 `
  --relation-confidence-min 0.9 `
  --safe-predicates "belongsToUnit,locatedIn,hasDepositType,hostedIn,occursInProfile,partOfProfile,overlies,underlies,locatedOnInterface,formedByWeatheringOf,formedDuring,enrichedIn,containsMineral,occursAs,adsorbedBy,leachedFrom,carriesElement,hasAnomaly"
 '@ | powershell
```

## Deliverables

For each formal batch, produce:

- extraction JSON batch files
- merged normalized JSON
- merge report with counts and key merge decisions
- import-ready Cypher
- export summary JSON
- optional Neo4j display-update Cypher

## References

- [references/schema.md](references/schema.md): ontology, JSON contract, confidence rules
- [references/workflow.md](references/workflow.md): operational pipeline, folder conventions, review policy
- [references/prompt-templates.md](references/prompt-templates.md): reusable prompts for planning, extraction, normalization, and export
