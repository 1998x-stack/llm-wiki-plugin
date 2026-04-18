---
type: entity
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["游戏引擎", "材质库", "3D渲染", "PBR", "UrhoX", "游戏开发"]
aliases: [UrhoX预制材质, UrhoX Material Library]
relates_to: [PBR材质系统, UrhoXCLI]
supersedes: null
entity_type: tool
---

# UrhoX材质库

## 概述
[[UrhoX引擎|UrhoX]] 引擎内置 35+ 预制 PBR 材质，覆盖地面、墙面、自然、石材、金属、木材、布料、建筑、特殊等类别。

## 关键内容
1. **使用方式**：通过 `cache:GetResource("Material", res_uri)` 以 UUID 路径加载预制材质，如 `uuid://Hw7_CePj4QdSOcXIloCyqlTu`（方块地砖）。
2. **材质分类**：flooring（地面：方块地砖、石板铺装、赤陶地砖、城市人行道）、wall（墙面：红砖墙）、nature（草地、沙子、土壤）、stone（大理石、花岗岩、岩石）、metal（抛光/拉丝/做旧金属）、wood（木材、木栅栏、拼花木地板）、fabric（皮革、海军蓝斜纹布）、building（混凝土、石膏墙面）、special（玻璃、碳纤维、陶瓷、橡胶、喷漆）。
3. **程序化材质规则**：纯色/无贴图材质必须使用 `Techniques/PBR/PBRNoTexture.xml`（不透明）或 `Techniques/PBR/PBRNoTextureAlpha.xml`（透明）；水面使用预制实例 `Materials/SingleLayerWater.xml`；禁止使用需要贴图的 `PBRMetallicRough*`、`PBRDiff*` 系列做程序化材质。
4. **场景推荐**：厨房（BlockFlooring01+Plaster01+Granite01）、客厅（WoodParquet01+Plaster01+Leather01）、工业（Concrete01+BrickWall01+Metal01-05）、城市（UrbanSidewalk01+Concrete01）。

## 来源
- [[raw/articles/personal/ai-dev-kit/.claude/skills/materials/SKILL]] — UrhoX 材质库完整索引与使用指南

## 相关
- [[PBR材质系统]] — uses
- [[UrhoXCLI]] — part_of
