#!/usr/bin/env python3
"""Build Neo4j Cypher from merged normalized geology KG JSON."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


LABEL_ZH = {
    "Deposit": "矿床",
    "DepositType": "矿床类型",
    "Element": "元素",
    "ElementGroup": "元素组",
    "GeochemicalAnomaly": "地球化学异常",
    "GeologicalEvent": "地质事件",
    "GeologicalInterface": "地质界面",
    "GeologicalTime": "地质时代",
    "KGEntity": "知识实体",
    "LithologicalUnit": "岩性单元",
    "Location": "位置",
    "MetallogenicUnit": "成矿单元",
    "Mineral": "矿物",
    "MineralizedLayer": "矿化层",
    "OccurrenceState": "赋存状态",
    "OreBody": "矿体",
    "StratigraphicUnit": "地层单元",
    "WeatheringProfile": "风化剖面",
}

REL_ZH = {
    "ADSORBED_BY": "被吸附于",
    "BELONGS_TO_UNIT": "属于",
    "CARRIES_ELEMENT": "携带元素",
    "CONTAINS_MINERAL": "含有矿物",
    "ENRICHED_IN": "富集于",
    "FORMED_BY_WEATHERING_OF": "由风化形成",
    "FORMED_DURING": "形成于",
    "HAS_ANOMALY": "具有异常",
    "HAS_DEPOSIT_TYPE": "矿床类型",
    "HOSTED_IN": "赋存于",
    "LEACHED_FROM": "淋滤自",
    "LOCATED_IN": "位于",
    "LOCATED_ON_INTERFACE": "位于界面",
    "OCCURS_AS": "以此形式出现",
    "OCCURS_IN_PROFILE": "出现在剖面",
    "OVERLIES": "上覆于",
    "PART_OF_PROFILE": "属于剖面",
    "UNDERLIES": "下伏于",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-json", required=True, help="Merged normalized JSON path")
    parser.add_argument("--output-cypher", required=True, help="Output Cypher path")
    parser.add_argument("--summary-out", help="Optional export summary JSON path")
    parser.add_argument("--display-zh-out", help="Optional Neo4j display update Cypher path")
    parser.add_argument("--entity-confidence-min", type=float, default=0.9)
    parser.add_argument("--relation-confidence-min", type=float, default=0.9)
    parser.add_argument(
        "--safe-predicates",
        help="Comma-separated predicate allowlist. Default: all predicates.",
    )
    parser.add_argument(
        "--include-review-flags",
        action="store_true",
        help="Include entities/relations touched by review_flags.",
    )
    parser.add_argument(
        "--keep-unconnected-entities",
        action="store_true",
        help="Keep filtered entities even if no exported relation references them.",
    )
    return parser.parse_args()


def escape_str(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
    )


def cypher_value(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str):
        return f"'{escape_str(value)}'"
    if isinstance(value, list):
        return "[" + ", ".join(cypher_value(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{" + ", ".join(f"{key}: {cypher_value(val)}" for key, val in value.items()) + "}"
    raise TypeError(f"Unsupported value type: {type(value)!r}")


def rel_type(predicate: str) -> str:
    step1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", predicate)
    step2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", step1)
    return step2.upper()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_display_cypher(output_path: Path) -> None:
    lines = [
        "// Add Chinese display properties for Neo4j Desktop / Query visualization.",
        "MATCH (n:KGEntity)",
        "SET",
        "  n.display_zh = coalesce(n.name, n.original_text, n.kg_id),",
        "  n.`中文名称` = coalesce(n.name, n.original_text, n.kg_id),",
        "  n.`实体类型中文` =",
        "    CASE",
    ]
    for label, zh in LABEL_ZH.items():
        if label == "KGEntity":
            continue
        lines.append(f"      WHEN '{label}' IN labels(n) THEN '{zh}'")
    lines.extend(
        [
            "      ELSE '知识实体'",
            "    END,",
            "  n.`原文中文` = coalesce(n.original_text, n.name, n.kg_id),",
            "  n.`置信度中文` = n.confidence;",
            "",
            "MATCH ()-[r]->()",
            "SET",
            "  r.relation_zh =",
            "    CASE type(r)",
        ]
    )
    for rel, zh in REL_ZH.items():
        lines.append(f"      WHEN '{rel}' THEN '{zh}'")
    lines.extend(
        [
            "      ELSE type(r)",
            "    END,",
            "  r.`关系中文` = r.relation_zh,",
            "  r.`关系类型中文` = coalesce(r.predicate, type(r)),",
            "  r.`证据句中文` = coalesce(r.first_evidence_sentence, ''),",
            "  r.`证据页码中文` = coalesce(r.evidence_pages, []),",
            "  r.`证据批次中文` = coalesce(r.evidence_batches, []),",
            "  r.`置信度中文` = r.confidence;",
            "",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_json)
    output_path = Path(args.output_cypher)
    summary_path = Path(args.summary_out) if args.summary_out else None
    display_path = Path(args.display_zh_out) if args.display_zh_out else None

    data = load_json(input_path)
    safe_predicates = None
    if args.safe_predicates:
        safe_predicates = {item.strip() for item in args.safe_predicates.split(",") if item.strip()}

    flagged_ids = set()
    if not args.include_review_flags:
        for item in data.get("review_flags", []):
            flag = item.get("flag", item)
            target_id = flag.get("target_id")
            if target_id:
                flagged_ids.add(target_id)

    base_entities = []
    excluded_entities = []
    for entity in data.get("entities", []):
        reasons = []
        if entity.get("confidence", 0.0) < args.entity_confidence_min:
            reasons.append("entity_confidence_below_threshold")
        if entity.get("id") in flagged_ids:
            reasons.append("entity_or_source_has_review_flag")
        if reasons:
            excluded_entities.append({"id": entity.get("id"), "reason": ",".join(reasons)})
        else:
            base_entities.append(entity)

    base_entity_ids = {entity["id"] for entity in base_entities}

    relations = []
    excluded_relations = []
    for rel in data.get("relations", []):
        reasons = []
        if rel.get("confidence", 0.0) < args.relation_confidence_min:
            reasons.append("relation_confidence_below_threshold")
        if safe_predicates is not None and rel.get("predicate") not in safe_predicates:
            reasons.append("predicate_not_in_safe_set")
        if rel.get("id") in flagged_ids:
            reasons.append("relation_or_source_has_review_flag")
        if rel.get("subject_id") not in base_entity_ids or rel.get("object_id") not in base_entity_ids:
            reasons.append("endpoint_entity_filtered")
        if reasons:
            excluded_relations.append({"id": rel.get("id"), "reason": ",".join(reasons)})
        else:
            relations.append(rel)

    if args.keep_unconnected_entities:
        entities = base_entities
    else:
        used_entity_ids = {rel["subject_id"] for rel in relations} | {rel["object_id"] for rel in relations}
        entities = [entity for entity in base_entities if entity["id"] in used_entity_ids]

    lines = [
        "// Neo4j import generated from merged normalized geology KG JSON",
        f"// Source: {input_path.name}",
        "CREATE CONSTRAINT kg_entity_id IF NOT EXISTS FOR (n:KGEntity) REQUIRE n.kg_id IS UNIQUE;",
        "",
    ]

    for entity in sorted(entities, key=lambda item: item["id"]):
        label = entity["label"]
        props = {
            "kg_id": entity["id"],
            "name": entity.get("name", ""),
            "entity_type": label,
            "original_text": entity.get("original_text", ""),
            "aliases": entity.get("aliases", []),
            "confidence": entity.get("confidence"),
            "source_batches": entity.get("source_batches", []),
            "source_entity_ids": entity.get("source_entity_ids", []),
        }
        props.update(entity.get("properties", {}))
        lines.append(f"MERGE (n:KGEntity:`{label}` {{kg_id: {cypher_value(entity['id'])}}})")
        lines.append(f"SET n += {cypher_value(props)};")
        lines.append("")

    for rel in sorted(relations, key=lambda item: item["id"]):
        evidence = rel.get("evidence", [])
        rel_props = {
            "kg_id": rel["id"],
            "predicate": rel["predicate"],
            "confidence": rel.get("confidence"),
            "evidence_pages": [item.get("page_num") for item in evidence if item.get("page_num") is not None],
            "evidence_batches": [item.get("batch") for item in evidence if item.get("batch")],
            "evidence_count": len(evidence),
            "first_evidence_sentence": evidence[0].get("sentence", "") if evidence else "",
            "source_relation_ids": rel.get("source_relation_ids", []),
        }
        rel_props.update(rel.get("properties", {}))
        lines.append(
            f"MATCH (s:KGEntity {{kg_id: {cypher_value(rel['subject_id'])}}}), "
            f"(o:KGEntity {{kg_id: {cypher_value(rel['object_id'])}}})"
        )
        lines.append(
            f"MERGE (s)-[rel:{rel_type(rel['predicate'])} {{kg_id: {cypher_value(rel['id'])}}}]->(o)"
        )
        lines.append(f"SET rel += {cypher_value(rel_props)};")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")

    if display_path:
        display_path.parent.mkdir(parents=True, exist_ok=True)
        build_display_cypher(display_path)

    if summary_path:
        summary = {
            "source": input_path.name,
            "policy": {
                "entity_confidence_min": args.entity_confidence_min,
                "relation_confidence_min": args.relation_confidence_min,
                "include_review_flags": args.include_review_flags,
                "safe_predicates": sorted(safe_predicates) if safe_predicates is not None else "ALL",
                "keep_unconnected_entities": args.keep_unconnected_entities,
            },
            "counts": {
                "entities_total": len(data.get("entities", [])),
                "relations_total": len(data.get("relations", [])),
                "entities_exported": len(entities),
                "relations_exported": len(relations),
                "entities_excluded": len(excluded_entities),
                "relations_excluded": len(excluded_relations),
                "review_flags_total": len(data.get("review_flags", [])),
            },
            "excluded_entities_sample": excluded_entities[:10],
            "excluded_relations_sample": excluded_relations[:10],
        }
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(
        {
            "output_cypher": str(output_path),
            "display_zh_out": str(display_path) if display_path else None,
            "summary_out": str(summary_path) if summary_path else None,
            "entities_exported": len(entities),
            "relations_exported": len(relations),
        },
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
