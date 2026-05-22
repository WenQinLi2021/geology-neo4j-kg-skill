# Geology Neo4j KG Skill

面向地质科研报告知识抽取、融合与 Neo4j 导出的 Codex skill 打包仓库。

本仓库用于复用以下工作流：

- 地质报告读取与分批抽取
- 实体、关系、属性、证据链 JSON 输出
- 跨报告融合与规范化
- `review_flags` 争议项管理
- Neo4j Desktop / Aura 可执行 Cypher 导出

## 目录结构

```text
geology-neo4j-kg-skill-repo/
  docs/
    技术文档.md
  scripts/
    install_skill.ps1
  skills/
    geology-neo4j-kg/
```

## 快速安装

在 Windows PowerShell 中执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_skill.ps1
```

默认会把 skill 安装到：

```text
C:\Users\<你的用户名>\.codex\skills\geology-neo4j-kg
```

## 快速使用

在 Codex 中直接这样发起任务：

```text
Use $geology-neo4j-kg.
继续处理这批地质科研报告，按当前 schema 抽取、融合、保留 review_flags，并导出 Neo4j Desktop 可直接导入的 Cypher。
```

## 说明

- skill 正文在 [skills/geology-neo4j-kg/SKILL.md](skills/geology-neo4j-kg/SKILL.md)
- 中文技术文档在 [docs/技术文档.md](docs/技术文档.md)
- 一键安装脚本在 [scripts/install_skill.ps1](scripts/install_skill.ps1)

