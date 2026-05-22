# Schema

## Use This Reference

- Read this file when the task is ontology design, extraction, normalization, or relation naming.
- Reuse the current classes first. Extend only when repeated geology facts cannot be represented cleanly.

## Core Entity Labels

Use these labels in the current v1 workflow:

| Label | Chinese | Notes |
|---|---|---|
| `Deposit` | 矿床 | Generic deposit or mineralization target |
| `DepositType` | 矿床类型 | Genetic or descriptive deposit class |
| `MetallogenicUnit` | 成矿单元 | Belt, block, region, metallogenic domain |
| `Location` | 位置 | Administrative or place-name location |
| `GeologicalTime` | 地质时代 | Time unit or age |
| `GeologicalEvent` | 地质事件 | Eruption, weathering, sedimentation, tectonics |
| `StratigraphicUnit` | 地层单元 | Group, formation, member, ore horizon |
| `LithologicalUnit` | 岩性单元 | Rock or lithologic package |
| `GeologicalInterface` | 地质界面 | Contact, unconformity, weathering interface |
| `WeatheringProfile` | 风化剖面 | Profile-scale unit |
| `MineralizedLayer` | 矿化层 | Preferred carrier for enriched horizons |
| `OreBody` | 矿体 | Use only when the source explicitly treats it as an ore body |
| `Mineral` | 矿物 | Carrier or associated mineral |
| `Element` | 元素 | Single element or oxide metric |
| `ElementGroup` | 元素组 | REE, LREE, HREE, three-rare groupings |
| `OccurrenceState` | 赋存状态 | Adsorbed, oxide, independent mineral, etc. |
| `GeochemicalAnomaly` | 地球化学异常 | Enrichment, anomaly, distribution pattern |

## Core Relations

Use these predicates exactly unless the ontology is intentionally revised:

| Predicate | Chinese | Domain -> Range |
|---|---|---|
| `belongsToUnit` | 属于 | Deposit/Profile/Target -> MetallogenicUnit |
| `locatedIn` | 位于 | Any core entity -> Location |
| `hasDepositType` | 矿床类型 | Deposit -> DepositType |
| `hostedIn` | 赋存于 | Deposit/Layer/OreBody/Anomaly -> Lithology/Stratigraphy |
| `occursInProfile` | 出现在剖面 | Layer/Anomaly/ProfileSection -> WeatheringProfile |
| `partOfProfile` | 属于剖面 | ProfileSection -> WeatheringProfile |
| `overlies` | 上覆于 | Stratigraphy/Lithology/Layer -> Stratigraphy/Lithology |
| `underlies` | 下伏于 | Stratigraphy/Lithology/Layer -> Stratigraphy/Lithology |
| `locatedOnInterface` | 位于界面 | Layer/OreBody -> GeologicalInterface |
| `formedByWeatheringOf` | 由风化形成 | Profile/Lithology/Layer -> LithologicalUnit |
| `formedDuring` | 形成于 | Deposit/Layer/Profile/Event -> GeologicalTime |
| `enrichedIn` | 富集于 | Deposit/Layer/Lithology/Anomaly -> Element/ElementGroup |
| `containsMineral` | 含有矿物 | Layer/Lithology/OreBody -> Mineral |
| `carriesElement` | 携带元素 | Lithology/Mineral -> Element/ElementGroup |
| `occursAs` | 以此形式出现 | Element/ElementGroup -> OccurrenceState |
| `adsorbedBy` | 被吸附于 | Element/ElementGroup -> Mineral/Lithology |
| `leachedFrom` | 淋滤自 | Element/ElementGroup -> Lithology/Mineral |
| `hasAnomaly` | 具有异常 | Profile/Deposit/Stratigraphy -> GeochemicalAnomaly |

## Extraction JSON Contract

Each extraction chunk should produce one JSON object with these top-level keys:

- `doc_id`
- `doc_title`
- `chunk_id`
- `source_pages`
- `text`
- `entities`
- `relations`
- `review_flags`

### Entity shape

```json
{
  "id": "deposit_guizhou_west_weathering_crust_ree",
  "label": "Deposit",
  "name": "贵州西部玄武岩风化壳型稀土矿床",
  "original_text": "贵州西部玄武岩风化壳型稀土矿床",
  "aliases": [],
  "properties": {},
  "confidence": 0.96
}
```

### Relation shape

```json
{
  "id": "rel_001",
  "subject_id": "deposit_guizhou_west_weathering_crust_ree",
  "predicate": "hasDepositType",
  "object_id": "dtype_weathering_crust_rare_earth",
  "properties": {},
  "evidence": {
    "page_num": 5,
    "sentence": "近年来...已在玄武岩风化壳型稀土资源方面取得一些进展。",
    "start_offset": 0,
    "end_offset": 30
  },
  "confidence": 0.95
}
```

### Review flag shape

```json
{
  "type": "low_confidence_relation",
  "target_id": "rel_001",
  "reason": "The sentence implies an exploration direction rather than a validated fact."
}
```

## Confidence Rules

- `>= 0.90`: safe candidate for high-confidence export
- `0.80 - 0.89`: keep in normalized graph, review before export
- `< 0.80`: add `review_flags`; do not include in high-confidence export by default

## Normalization Rules

- Canonicalize ids, not just names.
- Keep `name` as the normalized label and preserve source spellings in `original_text` and `aliases`.
- Merge abbreviations only when source evidence supports equivalence.
- Keep evidence sentences and source ids through every merge round.
- Distinguish:
  - province vs region vs metallogenic belt
  - stratigraphic level vs lithologic descriptor
  - deposit vs deposit type

