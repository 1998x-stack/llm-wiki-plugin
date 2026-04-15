# Obsidian Brain Schema

你是这个知识库的维护者。你的职责是将源材料编译为结构化的知识页面，维护知识之间的连接和一致性，管理记忆的晋升和衰减，发现模式、标记矛盾、填补空白。

## 架构

```
vault/
├── _schema/    系统规则（你正在读的文件）
├── _memory/    四层记忆系统
├── raw/        不可变源材料（只读）
├── wiki/       LLM 生成的知识页面
├── journal/    个人日记/思考/判断/成长
├── templates/  模板
├── index.md    内容目录
└── log.md      操作日志
```

## 核心原则

1. **raw/ 只读**：源材料不可变，LLM 永远不修改 raw/ 中的文件
2. **wiki/ LLM 拥有**：所有 wiki 页面由 LLM 创建和维护，人类只读
3. **journal/ 人类拥有**：个人思考由人类写入，LLM 辅助链接和分析
4. **Links over folders**：优先使用 [[双链]] 组织关系，而非文件夹层级
5. **Bottom-up**：结构自然浮现，不预设分类体系
6. **所有操作写 log.md**：可追溯、可审计

## Frontmatter 规范

所有 wiki/ 页面必须包含以下 frontmatter：

```yaml
---
type: entity | concept | synthesis | qa-insight | source-summary
status: draft | active | stale | archived
confidence: 0.0-1.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_accessed: YYYY-MM-DD
source_count: N
tags: []
aliases: []
relates_to: []
supersedes: null
---
```

### relates_to 格式

```yaml
relates_to:
  - target: "[[页面名]]"
    type: uses | depends_on | contradicts | caused | extends | implements | supersedes
    confidence: 0.0-1.0
```

每个页面最多 10 个关系。

### tags 规则

最多 8 个大类横切标签。当前已定义标签：
- `技术` `研究` `工作` `学习` `游戏` `个人` `工具` `方法论`

不要创建新标签，除非现有标签确实无法覆盖。

## 操作手册

### Ingest

1. 读取 raw/ 中的源文件（完整阅读，不要跳过）
2. 判断内容涉及哪些实体和概念
3. 对于每个实体/概念：
   - 如果 wiki/ 中已有对应页面 → 更新该页面，追加新信息
   - 如果没有 → 创建新页面，使用 templates/wiki-page.md 模板
4. 检查新信息是否与已有页面矛盾 → 如有，用 supersedes 机制处理
5. 同步 index.md：执行 `python3 scripts/snapshot_index.py --update`（index.md 是计算产物）
6. 追加 log.md：记录本次 ingest 的操作

### Query

1. 读取 index.md 定位相关页面
2. 读取相关页面，沿 relates_to 扩展搜索范围
3. 综合所有信息回答问题
4. 如果答案有价值（综合了 3+ 个页面的信息），自动创建为新 wiki 页面
5. 回答时引用来源页面：`来源：[[页面名]]`

### Lint

检查以下问题并自动修复可修复项：
1. **孤页**：wiki/ 中没有任何入链的页面 → 尝试找到相关页面并添加链接
2. **矛盾**：两个页面对同一事实有不同描述 → 用 supersedes 标记旧的
3. **过期内容**：confidence < 0.3 的页面 → 标记为 stale
4. **缺失链接**：页面提到的概念没有加 [[链接]] → 自动添加
5. **空页面**：有 frontmatter 但没有实质内容 → 标记为 draft
6. 生成 lint 报告追加到 log.md

### 质量标准

wiki 页面必须满足：
- 有完整的 frontmatter（所有必要字段）
- 概述部分不超过 200 字
- 至少有 1 个来源链接
- 至少有 1 个 relates_to 关系
- 中文为主，专有名词保留英文

## 记忆系统

见 `_memory/` 目录。四层：Working → Episodic → Semantic → Procedural。

### 记忆 vs Wiki 边界规则

`_memory/semantic/` 和 `wiki/syntheses/` 服务不同目的，**严禁重复**：

| 层 | 存放位置 | 内容类型 | 示例 |
|----|---------|---------|------|
| **Semantic Memory** | `_memory/semantic/` | 单一事实性声明（不跨主题） | "Python 3.10+ 支持 match 语句" |
| **Syntheses** | `wiki/syntheses/` | 跨主题综合分析（连接 3+ 个概念） | "矩阵谱理论的统一叙事" |

- `wiki:crystallize` 只写入 `_memory/working/` 和可选的 `wiki/syntheses/`
- `wiki:consolidate` 负责 working → episodic → semantic 的晋升和衰减
- 如果一个洞见跨越 3+ 个已有概念 → 放 syntheses/
- 如果一个洞见是单一事实确认 → 放 semantic/
- **决不**将同一信息同时放入两个位置

晋升规则：
- Working → Episodic：会话结束时自动压缩
- Episodic → Semantic：一个观察在 3+ 个 episode 中重复出现
- Semantic → Procedural：一个行为模式在 5+ 个语义记忆中被发现

衰减规则（Ebbinghaus）：
- slow（半衰期 180 天）：架构决策、核心概念
- medium（半衰期 60 天）：一般事实
- fast（半衰期 14 天）：临时 bug、短期观察
- confidence < 0.3 → 标记 stale

## 隐私

- journal/ 中的内容是私人的，不要在 wiki:query 结果中暴露具体日记内容
- 可以引用 journal 中的判断和反思的结论，但不引用原文
- raw/ 中标记为 private 的文件不进行 ingest
