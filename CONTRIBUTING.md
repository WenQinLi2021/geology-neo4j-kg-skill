# Contributing

## Scope

This repository contains a reusable Codex skill for geology knowledge-graph production. Contributions should improve one or more of the following:

- ontology stability
- extraction consistency
- normalization quality
- Neo4j export reliability
- team onboarding and documentation

## Before You Change Anything

Please keep these principles aligned:

1. Do not expand the ontology unless repeated report evidence justifies it.
2. Keep evidence chains traceable.
3. Do not mix low-confidence facts into the default production export.
4. Prefer improving reusable templates and scripts over ad hoc project-specific edits.

## Recommended Contribution Areas

- refine `schema.md`
- improve `workflow.md`
- add better prompt templates
- improve `build_neo4j_cypher.py`
- strengthen documentation and examples

## Contribution Workflow

1. Identify the problem clearly.
2. Make the smallest change that improves repeatability.
3. Test the affected skill or script with a realistic artifact.
4. Update related documentation when behavior changes.

## Script Changes

If you modify:

- `skills/geology-neo4j-kg/scripts/build_neo4j_cypher.py`

then verify:

- Cypher is still syntactically valid
- export counts remain explainable
- high-confidence filtering still works
- `review_flags` behavior is preserved

## Documentation Changes

If you modify:

- `README.md`
- `README_EN.md`
- `docs/技术文档.md`
- `skills/geology-neo4j-kg/references/*`

then keep terminology consistent across Chinese and English descriptions.

## Pull Request Guidance

A good change should answer:

- What problem does this solve?
- Does it change ontology, export policy, or only documentation?
- Does it affect existing team workflows?
- What should reviewers verify?

