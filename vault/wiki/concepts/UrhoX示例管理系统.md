---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 3
tags: ["UrhoX", "Lua", "示例系统", "YAML", "代码生成", "文档生成", "游戏开发"]
aliases: [示例系统, examples system, UrhoX示例库]
relates_to: [UrhoX引擎, UrhoX Lua开发准则, 游戏脚手架模式]
supersedes: null
---

# UrhoX示例管理系统

## 概述
[[UrhoX引擎|UrhoX]]示例管理系统以单一 YAML [[Configuration|配置]]文件统一管理 25 个 Lua 示例的元数据，并通过处理脚本自动生成多视图文档（按分类/难度索引 + API [[倒排索引|反向索引]]），为用户、开发者和 AI 助手提供结构化的示例查找能力。

## 关键内容
1. **核心文件结构**：`examples-config.yaml`（核心[[Configuration|配置]]，定义示例的源/目标文件、分类、难度、标题、描述、API、功能、标签）；`tools/process_examples.py`（处理脚本，加载验证[[Configuration|配置]]、复制示例文件、生成索引文档）。
2. **分类与难度**：10 个分类（3D图形、2D图形、3D/2D物理、UI、音频、网络、动画、导航、高级）；3 个难度级别（初级 beginner、中级 intermediate、高级 advanced）；共 25 个示例（初级6、中级11、高级8）。按分类：3D图形6、2D图形5、物理3D/3+2D/2、UI3、音频1、网络2、动画2、导航2、高级1。
3. **生成的文档视图**：`examples/index.md`（按分类/难度分组的主索引）；`examples/api-index.md`（API [[倒排索引|反向索引]]：列出使用特定 API 的所有示例），两份文档均在执行 `process_examples.py` 后自动生成。
4. **[[Configuration|配置]]字段规范**：每条示例需声明 `source`（源 `.lua` 文件名）、`target`（目标文件名）、`metadata.title`（中英双语）、`category`、`difficulty`、`description`、`features`（3-6条，动词开头）、`apis`（只列主要 API）、`concepts`（核心学习点）、`tags`（关键词）。可选字段：`line_count`、`dependencies`。
5. **文件命名规范**：目标文件名格式 `{两位序号}-{kebab-case}.lua`，如 `01-hello-world.lua`、`07-physics-3d.lua`。分类选择最相关的单一分类（3D物理示例 → `physics`，不是 `3d-graphics`）。
6. **难度评估标准**：Beginner（<200行，单一功能）；Intermediate（200-400行，多功能，中等复杂度）；Advanced（>400行，复杂系统，高级特性）。
7. **使用方式**：`--validate` 仅校验[[Configuration|配置]]（检查源文件存在性、分类/难度合法性、必填字段）；`--dry-run` 预览不写文件；无参数则正式处理（复制文件 + 生成文档）。
8. **AI 友好设计**：通过 `api-index.md` 可快速定位"使用某 API 的示例"；通过分类/难度过滤可推荐合适示例；结构化元数据方便 LLM 解析。双语标题支持中英文检索。
9. **扩展方式**：添加新示例只需编辑 `examples-config.yaml` 新增条目，再运行处理脚本即可，无需手动维护文档。支持自定义元数据字段（`related_examples`、`video_url`、`min_version`）和多语言扩展。
10. **关键约束**：生成的文档（`index.md`、`api-index.md`）不可手动编辑，下次运行脚本会覆盖。应通过修改[[Configuration|配置]]文件来控制生成内容。依赖 [[Python]] 3.6+ 和 PyYAML（`pip install pyyaml`）。

## 来源
- [[raw/articles/personal/ai-dev-kit/config/NEW_FEATURE_SUMMARY]] — UrhoX AI Dev Kit 示例系统新功能摘要（v1.0，2025-11-17）
- [[raw/articles/personal/ai-dev-kit/config/examples-config]] — examples-config.yaml 配置系统说明文档（v1.0，2025-11-17）
- [[raw/articles/personal/ai-dev-kit/config/示例系统说明]] — UrhoX示例系统使用说明（v1.0，2025-11-17）

## 相关
- [[UrhoX引擎]] — relates_to（宿主引擎）
- [[UrhoX Lua开发准则]] — relates_to（示例遵循的开发准则）
- [[游戏脚手架模式]] — relates_to（示例与脚手架协同使用）
