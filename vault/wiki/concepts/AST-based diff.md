---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [code-diff, ast, code-analysis, ai-tools, file-operations]
aliases: ["AST-based diff", "AST diff", "语法树差异检测", "抽象语法树差异"]
relates_to: 
  - target: "[[Write-Tools]]"
    type: compares_to
  - target: "[[Cursor]]"
    type: implemented_in
  - target: "[[unified diff]]"
    type: alternative_to
  - target: "[[Code Analysis]]"
    type: uses
supersedes: null
---

# AST-based diff

## 概述
AST-based diff（抽象语法树差异检测）是一种先进的代码差异检测技术，直接在语法树层面进行比较和合并，而不是基于行号的传统 diff 方式。

## 关键内容

1. **工作原理**：将代码解析为抽象语法树（AST），然后在树结构层面进行差异比较，能够理解代码的实际结构而非单纯的文本排列

2. **主要优势**：
   - **解决行号漂移问题**：传统 [[unified diff]] 严重依赖行号，当代码发生插入、删除时容易出现不匹配
   - **语义感知**：能够理解代码的真实结构，如函数、类、变量声明等
   - **更高的精度**：相比基于文本的 diff，能够更准确地识别代码变更的意图

3. **与传统 diff 的对比**：
   - **[[unified diff]]**：基于行号，容易受格式调整、插入删除等操作影响
   - **AST-based diff**：基于语法结构，不受代码格式变化影响，只关注语义变更

4. **应用领域**：
   - 现代 AI 代码编辑器（如 [[Cursor]]）的[[Write-Tools|文件写入机制]]
   - 代码合并工具
   - [[代码重构]]工具
   - 版本控制系统增强

5. **实现挑战**：
   - 需要为每种编程语言实现相应的解析器
   - [[计算]]复杂度相对较高
   - AST 标准化和归一化处理

## 来源
- [[write-tools.md]] — 八、横向对比

## 相关
- [[Write-Tools]] — relates_to
- [[Cursor]] — implemented_in
- [[unified diff]] — alternative_to
- [[Code Analysis]] — uses