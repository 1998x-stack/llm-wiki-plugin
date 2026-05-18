---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [code-diff, file-operations, version-control, ai-tools, AI工程]
aliases: ["unified diff", "unified diff format", "统一差异格式", "标准diff格式"]
relates_to: 
  - target: "[[Write-Tools]]"
    type: used_in
  - target: "[[AST-based diff]]"
    type: alternative_to
  - target: "[[Git]]"
    type: uses
  - target: "[[apply_patch]]"
    type: format_for
supersedes: null
---

# unified diff

## 概述
unified diff 是一种广泛使用的文本差异表示格式，使用标准的 `+` 和 `-` 符号来表示新增和删除的行，是大多数版本控制系统和代码工具的基础差异格式。

## 关键内容

1. **格式结构**：
   - `+` 表示新增行（通常显示为绿色）
   - `-` 表示删除行（通常显示为红色）
   - `@@` 表示差异块的行号范围（通常显示为青色）
   - 保留行（不变的上下文）用于定位差异位置

2. **在 [[Write-Tools]] 中的应用**：
   - `apply_patch` 工具使用统一差异格式执行文件修改
   - 作为 [[Approval Gate UI|Approval Gate]] 中 diff 展示的标准格式
   - [[Claude Code]] 避免使用此方式，优先推荐 str_replace，因为 LLM 对行号的准确性较差，导致 fuzz 不匹配造成 apply 失败率高

3. **主要缺点**：
   - **行号依赖性**：对行号准确性要求很高，当文件结构发生变化时容易出现不匹配
   - **格式敏感**：换行、缩进等格式变化可能导致差异[[计算]]错误
   - **语义盲区**：只考虑文本层面的变化，无法理解代码的语义结构

4. **使用场景**：
   - 版本控制系统（如 Git）的差异表示
   - [[代码审查]]中的变更展示
   - 文件内容比较工具
   - 某些 AI 工具的文件修改操作

## 来源
- [[write-tools.md]] — 三、三种写入策略的核心差异
- [[write-tools.md]] — 六、Approval Gate 与 Diff 展示
- [[write-tools.md]] — 八、横向对比

## 相关
- [[Write-Tools]] — used_in
- [[AST-based diff]] — alternative_to
- [[Git]] — uses
- [[apply_patch]] — format_for