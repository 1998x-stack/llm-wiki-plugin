---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["AI工程"]
aliases: ["Progressive Disclosure", "渐进式上下文加载", "按需加载"]
relates_to:
  - target: "[[Agent Skills]]"
    type: implements
    confidence: 0.9
  - target: "[[上下文窗口]]"
    type: depends_on
    confidence: 0.85
  - target: "[[上下文压缩]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# 渐进式披露（Progressive Disclosure）

## 概述
Claude Code [[Agent Skills|Skills]] 的上下文管理策略——不一次性把所有内容塞进上下文，而是按需分三层加载：先看描述判断相关性，再加载 [[Agent Skills|SKILL.md]] 核心说明，最后按需加载脚本和辅助文件。

## 关键内容

1. **三层加载机制**：
   - **第一层：描述**——Claude 扫描技能目录，根据描述判断 skill 是否匹配当前任务
   - **第二层：[[Agent Skills|SKILL.md]]**——读取核心说明和指令
   - **第三层：支持文件**——如有需要，再加载脚本、模板、参考资料

2. **加载流程**：
   - Claude 扫描技能目录
   - 根据描述判断是否匹配当前任务
   - 读取 `SKILL.md`
   - 如有需要，再加载脚本和辅助文件

3. **设计动机**：[[上下文窗口]]有限，渐进式披露确保只加载当前任务真正需要的信息，避免上下文污染和 token 浪费。

4. **与[[上下文压缩]]的关系**：渐进式披露是"预防性"策略（不让不需要的信息进入上下文），[[上下文压缩]]是"补救性"策略（当上下文过长时压缩旧内容）。两者互补。

## 来源
- [[03-skills/README.md]] — Claude HowTo Agent Skills 指南

## 相关
- [[Agent Skills]] — implements
- [[上下文窗口]] — depends_on
- [[上下文压缩]] — relates_to
