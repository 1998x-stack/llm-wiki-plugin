---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [Evolver, 代码变更, 风险控制]
aliases: ["Blast Radius", "爆炸半径", "变更范围控制"]
relates_to:
  - target: "[[Evolver]]"
    type: part_of
  - target: "[[Solidify 机制]]"
    type: uses
  - target: "[[GEP]]"
    type: part_of
supersedes: null
---

# Blast Radius 控制

## 概述
[[Evolver]] 中的变更影响范围控制机制，用于限制代码进化过程中的变更幅度，防止过度修改。

## 关键内容

1. **多层上限控制**：
   - 基因级别：gene.constraints.max_files（repair: 20, innovate: 25）
   - 系统硬上限：EVOLVER_HARD_CAP_FILES/LINES（默认 60 文件，20000 行）
   - A2A 外部资产：A2A_MAX_FILES/LINES（默认 5 文件，200 行）

2. **[[计算]]方法**：
   - 通过 git diff --cached --shortstat [[计算]]
   - 返回文件数、插入行数、删除行数和总行数
   - 示例输出："2 files changed, 44 insertions(+), 12 deletions(-)"

3. **超限处理**：
   - 中止固化流程
   - 根据 EVOLVER_ROLLBACK_MODE 执行回滚
   - 写入失败 EvolutionEvent
   - 在循环模式下等待后进入下一轮

## 来源
- [[Evolver 安全模型与 Solidify 机制]] — 第 4 节

## 相关
- [[Evolver]] — part_of
- [[Solidify 机制]] — uses
- [[GEP]] — part_of