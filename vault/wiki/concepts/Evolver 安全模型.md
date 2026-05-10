---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [Evolver, 安全机制, 代码进化]
aliases: ["Evolver 安全模型", "Evolver 安全框架"]
relates_to:
  - target: "[[Evolver]]"
    type: part_of
  - target: "[[Solidify 机制]]"
    type: part_of
  - target: "[[GEP]]"
    type: implements
supersedes: null
---

# Evolver 安全模型

## 概述
[[Evolver]] 基于"深度防御"理念的安全架构，通过多层独立安全边界防止失控的代码自进化破坏系统稳定性。

## 关键内容

1. **七层防御结构**：
   - 第一层：Gene 级约束（max_files / forbidden_paths / validation 声明）
   - 第二层：系统硬上限（EVOLVER_HARD_CAP_FILES=60 / LINES=20000）
   - 第三层：命令白名单（只允许 node/npm/npx，禁止 Shell 操作符）
   - 第四层：人格检查（[[Mutation]] 安全降级规则）
   - 第五层：[[受保护文件机制|受保护文件]]（[[Evolver]] 核心源码不可被自己修改）
   - 第六层：git 回滚（失败时 hard/stash 回滚）
   - 第七层：人工审核（--review 模式、A2A 晋升 --validated）

2. **执行[[Permissions|权限]][[矩阵]]**：
   - evolve.js：只读 git/进程查询，写 memory/assets/
   - gep/prompt.js：纯文本生成，无执行[[Permissions|权限]]
   - gep/selector.js：纯逻辑评分，无执行[[Permissions|权限]]
   - gep/solidify.js：执行基因验证命令，写入 events.jsonl
   - gep/a2aProtocol.js：写 outbox/，网络访问通过代理

3. **安全[[Configuration|配置]]推荐**：
   - EVOLVE_ALLOW_SELF_MODIFY=false（生产必需）
   - EVOLVER_ROLLBACK_MODE=stash（比 hard 更利于排查）
   - 人工审核模式（--review）避免直接 --loop

## 来源
- [[Evolver 安全模型与 Solidify 机制]] — 第 1-10 节

## 相关
- [[Evolver]] — part_of
- [[Solidify 机制]] — part_of
- [[GEP]] — implements