# Geology Neo4j KG Skill

Codex skill for turning geology reports into reusable knowledge-graph assets for Neo4j.

## Overview

This repository packages a reusable workflow for:

- geology report ingestion
- ontology-first extraction
- entity / relation / evidence JSON output
- normalization and merge across reports
- `review_flags` handling for uncertain facts
- Neo4j Desktop / Aura Cypher export

It is designed for geology knowledge-graph projects, especially:

- rare earth
- rare metals
- metallogenic belts
- stratigraphic and lithologic analysis
- weathering profile and enrichment studies

## Repository Structure

```text
geology-neo4j-kg-skill-repo/
  docs/
    技术文档.md
  scripts/
    install_skill.ps1
  skills/
    geology-neo4j-kg/
```

## Installation

Run in PowerShell from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_skill.ps1
```

## Usage

Invoke the skill in Codex with:

```text
Use $geology-neo4j-kg.
Continue this geology knowledge-graph project with the new report batch.
Read the reports, extract to the current schema, merge into the normalized graph, preserve review_flags, and export a Neo4j Desktop-ready Cypher increment.
```

## Key Files

- [README.md](README.md): project homepage
- [docs/技术文档.md](docs/技术文档.md): Chinese technical delivery guide
- [skills/geology-neo4j-kg/SKILL.md](skills/geology-neo4j-kg/SKILL.md): skill definition
- [skills/geology-neo4j-kg/scripts/build_neo4j_cypher.py](skills/geology-neo4j-kg/scripts/build_neo4j_cypher.py): Cypher export script

## Notes

- The skill standardizes workflow; it does not replace domain expertise.
- For production graph imports, keep `review_flags` as a mandatory quality gate.
- For long-term collaboration, reuse the same schema and export rules across the team.

## License

This repository is released under the [MIT License](LICENSE).

