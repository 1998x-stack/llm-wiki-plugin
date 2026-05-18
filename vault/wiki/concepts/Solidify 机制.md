---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [Evolver, 安全机制, 代码进化, AI工程]
aliases: ["Evolver Solidify", "Evolver 固化机制"]
relates_to:
  - target: "[[Evolver]]"
    type: part_of
  - target: "[[GEP]]"
    type: part_of
  - target: "[[Mutation]]"
    type: implements
  - target: "[[Evolver 安全模型]]"
    type: part_of
supersedes: null
---

# Solidify 机制

## 概述
[[Evolver]] 的固化机制，负责在允许代码自进化的同时，验证并固化进化的代码变更，确保系统稳定性。

## 关键内容

1. **核心功能**：
   - 解析 LLM 输出的 FilePatches（[[unified diff|统一差异格式]]）
   - 执行多层安全检查和验证
   - 应用变更并固化到代码库
   - 记录 EvolutionEvent 和更新记忆图

2. **安全门检查**：
   - 基因验证命令白名单（只允许 node/npm/npx）
   - 禁止命令替换（反引号和 $()）
   - 禁止 Shell 操作符（&、|、; 等）
   - 作用域锁定在[[仓库]]根目录
   - 每条命令最长 180 秒超时

3. **固化流程**：
   - 解析 FilePatches → [[受保护文件机制|受保护文件]]检查 → 应用变更 → [[计算]] [[Blast Radius 控制|Blast Radius]] → 执行验证命令 → 提交变更 → 构建 Capsule → 记录事件

## 来源
- [[Evolver 安全模型与 Solidify 机制]] — 第 1-7 节

## 相关
- [[Evolver]] — part_of
- [[GEP]] — part_of
- [[Mutation]] — implements
- [[Evolver 安全模型]] — extends