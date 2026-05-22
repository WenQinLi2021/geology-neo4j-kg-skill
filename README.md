# Geology Neo4j KG Skill

Codex skill for turning geology reports into reusable knowledge-graph assets for Neo4j.

This repository packages a team-ready workflow for:

- geology report ingestion
- ontology-first extraction
- entity / relation / evidence JSON output
- cross-report normalization and merge
- `review_flags` management for uncertain facts
- Neo4j Desktop / Aura Cypher export

It is especially suitable for rare earth, rare metal, metallogenic, stratigraphic, weathering-profile, and related geology knowledge-graph projects.

## Why This Repository Exists

Most geology knowledge-graph projects get stuck in one of these places:

- extraction prompts are not standardized
- entity and relation naming drift across reports
- uncertain facts are mixed into production imports
- Neo4j import files are generated inconsistently

This skill turns that ad hoc process into a repeatable pipeline:

```text
source reports
-> extraction JSON
-> normalization / merge
-> review flags
-> Neo4j-ready Cypher
```

## What You Get

This repository includes:

- a reusable Codex skill: `skills/geology-neo4j-kg`
- a Chinese technical guide for team onboarding
- a PowerShell installer for local Codex skill installation
- a tested Cypher export script for merged normalized graph JSON

## Repository Structure

```text
geology-neo4j-kg-skill-repo/
  docs/
    技术文档.md
  scripts/
    install_skill.ps1
  skills/
    geology-neo4j-kg/
      SKILL.md
      agents/
      references/
      scripts/
```

## Installation

### Windows PowerShell

Run from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_skill.ps1
```

By default, the skill is installed to:

```text
C:\Users\<your-user>\.codex\skills\geology-neo4j-kg
```

### Custom install path

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_skill.ps1 `
  -TargetRoot "D:\TeamCodexSkills"
```

## Quick Start

After installation, invoke the skill in Codex like this:

```text
Use $geology-neo4j-kg.
Continue this geology knowledge-graph project with the new report batch.
Read the reports, extract to the current schema, merge into the normalized graph, preserve review_flags, and export a Neo4j Desktop-ready Cypher increment.
```

## Typical Use Cases

- Build a rare-earth knowledge graph from PDF reports
- Merge multiple metallogenic reports into one normalized graph
- Export only high-confidence facts for Neo4j import
- Keep low-confidence or disputed items out of production imports
- Reuse a standard schema and prompt set across a research team

## Core Workflow

The skill is designed around a stable team workflow:

1. Define the ontology first
2. Extract entities, relations, properties, and evidence by chunk
3. Normalize names, aliases, and cross-report duplicates
4. Record uncertain items in `review_flags`
5. Export a filtered Neo4j import slice

## Main Components

### Skill definition

- [skills/geology-neo4j-kg/SKILL.md](skills/geology-neo4j-kg/SKILL.md)

This is the main skill entry. It tells Codex when to use the skill and how to run the workflow.

### References

- [skills/geology-neo4j-kg/references/schema.md](skills/geology-neo4j-kg/references/schema.md)
- [skills/geology-neo4j-kg/references/workflow.md](skills/geology-neo4j-kg/references/workflow.md)
- [skills/geology-neo4j-kg/references/prompt-templates.md](skills/geology-neo4j-kg/references/prompt-templates.md)

These documents define the ontology, operating workflow, and reusable prompt patterns.

### Export script

- [skills/geology-neo4j-kg/scripts/build_neo4j_cypher.py](skills/geology-neo4j-kg/scripts/build_neo4j_cypher.py)

This script converts merged normalized graph JSON into import-ready Neo4j Cypher and optional display-update Cypher.

### Team documentation

- [docs/技术文档.md](docs/技术文档.md)

Chinese technical documentation for installation, triggering, workflow, and team reuse.

## Example Export Command

```powershell
python ".\skills\geology-neo4j-kg\scripts\build_neo4j_cypher.py" `
  --input-json "C:\path\to\roundX_merged_normalized.json" `
  --output-cypher "C:\path\to\roundX_high_confidence.cypher" `
  --summary-out "C:\path\to\roundX_high_confidence_summary.json" `
  --display-zh-out "C:\path\to\roundX_display_zh.cypher" `
  --entity-confidence-min 0.9 `
  --relation-confidence-min 0.9 `
  --safe-predicates "belongsToUnit,locatedIn,hasDepositType,hostedIn,occursInProfile,partOfProfile,overlies,underlies,locatedOnInterface,formedByWeatheringOf,formedDuring,enrichedIn,containsMineral,occursAs,adsorbedBy,leachedFrom,carriesElement,hasAnomaly"
```

## Recommended Team Pattern

Use this repository as a shared production template:

- researchers provide new report batches
- Codex uses the skill to extract and normalize
- the team imports only reviewed, confidence-filtered Cypher
- domain experts review `review_flags` separately

This keeps the graph:

- traceable
- reviewable
- incrementally extensible

## Notes

- The skill does not replace geology expertise.
- It does make the extraction, normalization, and export workflow much more consistent.
- For production use, treat `review_flags` as a required quality gate, not an optional extra.

## License / Reuse

If you reuse or extend this repository internally, keep the schema, prompt templates, and export policy aligned so different team members do not drift into incompatible graph structures.
