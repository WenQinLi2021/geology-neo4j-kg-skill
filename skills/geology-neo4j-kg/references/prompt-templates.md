# Prompt Templates

Use these templates directly or adapt them.

## 1. Plan ontology first

```text
Use $geology-neo4j-kg.
Before extracting anything, design the minimum ontology for this geology knowledge-graph project.
Target: a Neo4j v1 that can be imported within two weeks.
Output:
1. entity classes
2. relation classes
3. unique-key strategy
4. evidence fields
5. extraction granularity
```

## 2. Extract from a report chunk

```text
Use $geology-neo4j-kg.
Using the current schema, extract entities, relations, properties, and review flags from this report chunk.
Output JSON only. Do not explain.
```

## 3. Normalize a batch

```text
Use $geology-neo4j-kg.
Merge these extraction JSON batches into the existing normalized graph.
Unify canonical names, merge aliases, preserve evidence, and list every ambiguous normalization in review_flags.
Return:
1. merged normalized JSON
2. entity merge decisions
3. counts summary
```

## 4. Export a safe import slice

```text
Use $geology-neo4j-kg.
Export the merged normalized graph to Neo4j Cypher.
Rules:
- entity confidence >= 0.9
- relation confidence >= 0.9
- exclude anything touched by review_flags
- keep only low-dispute factual relations
Also produce an export summary.
```

## 5. Continue an existing graph

```text
Use $geology-neo4j-kg.
Continue the existing geology knowledge graph with this new report batch.
Read the reports, extract to the current schema, merge into the normalized graph, preserve review flags, and output a Neo4j Desktop-ready Cypher increment.
```

