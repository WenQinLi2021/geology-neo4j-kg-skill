# Workflow

## Recommended Folder Layout

Use or approximate this structure:

```text
project/
  schema/
  extractions/
  normalization/
  neo4j_export/
  sources/
```

## Batch Pipeline

### 1. Scope and ontology

- Fix graph goal and domain boundary first.
- Reuse the existing schema unless the new report repeatedly forces a new class.
- Keep v1 small and evidence-heavy.

### 2. Source ingestion

- Prefer original PDF over screenshots or copied snippets.
- Work in batches of `1-3` coherent reports.
- Preserve original filenames and report metadata.

### 3. Chunk extraction

- Extract by page range, section, or fact-dense chunk.
- Output JSON batches into `extractions/`.
- Keep one chunk per output object to simplify tracing and rework.

### 4. Merge and normalization

- Merge new batches with the current normalized file in `normalization/`.
- Produce:
  - merged JSON
  - entity map or alias map when useful
  - short merge report with counts and major decisions

### 5. Review gate

Before export, identify:

- low-confidence entities
- low-confidence relations
- ambiguous normalizations
- conflicting source claims
- ontology mismatches

Put them in `review_flags`.

### 6. Export gate

Export only the slice requested by the user:

- `high-confidence facts only`
- `include review flags`
- `all merged facts`

For most production use, default to:

- entity confidence `>= 0.90`
- relation confidence `>= 0.90`
- exclude `review_flags`
- prune unconnected entities

### 7. Neo4j import

- Generate Cypher from normalized JSON.
- Prefer file-based import over copy-paste for long Cypher.
- For Neo4j Desktop, use the DBMS-local `cypher-shell` and `-f file.cypher`.

## Team Operating Pattern

Best recurring prompt from users:

```text
Continue the geology KG with this batch of reports.
Read the reports, extract to the current schema, merge with the existing normalized graph, keep review flags for uncertain items, and export a Neo4j-ready high-confidence Cypher increment.
```

## Output Checklist

Each serious batch should end with:

- source reports identified
- extraction batch files saved
- normalization counts
- review flag count and reasons
- export counts
- exact import file paths

