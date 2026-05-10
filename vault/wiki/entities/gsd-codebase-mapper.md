---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [gsd-agent, codebase-analysis, mapping]
aliases: ["gsd-codebase-mapper", "GSD Codebase Mapper", "GSD代码库分析智能体"]
relates_to: 
  - target: "[[GSD Framework]]"
    type: part_of
    confidence: 0.9
  - target: "[[GSD 多智能体编排架构]]"
    type: implements
    confidence: 0.9
  - target: "[[GSD Commands]]"
    type: supports_command
    confidence: 0.8
  - target: "[[Codex多Agent调度]]"
    type: compares_to
    confidence: 0.7
supersedes: null
---

# gsd-codebase-mapper

## 概述
GSD框架中的代码库分析智能体，专门负责对棕地（brownfield）项目进行全方位分析，为后续开发提供代码库理解基础。

## 关键内容

1. **四种并行分析模式**：
   - **gsd-stack-mapper**：分析技术栈 → 生成STACK.md
     - 分析package.json、Dockerfile、[[Configuration|配置]]文件
     - 输出技术栈清单（语言版本、框架版本、主要依赖）
   
   - **gsd-arch-mapper**：分析架构 → 生成ARCHITECTURE.md
     - 分析目录结构、模块划分、设计模式
     - 输出架构描述（是否monorepo、分层方式、关键抽象）
   
   - **gsd-convention-mapper**：分析约定 → 生成CONVENTIONS.md
     - 分析现有代码的命名规范、文件组织、注释风格
     - 输出约定清单（供[[gsd-planner]]在生成新代码时遵守）
   
   - **gsd-concern-mapper**：分析技术债务 → 生成CONCERNS.md
     - 分析已知TODO、deprecated代码、性能问题、安全风险
     - 输出技术债务列表（供规划时避开或处理）

2. **触发机制**：
   - 通过/gsd:map-codebase命令触发（专用于棕地项目）
   - 支持×4并行执行提高分析效率

3. **分析价值**：
   - 为新代码开发提供一致性指导
   - 识别现有项目的架构约束和约定
   - 发现潜在的技术债务和风险

## 来源
- [[raw/articles/ai-tools/claude-skills/04-multi-agent-orchestration.md]] — GSD多智能体编排架构详解

## 相关
- [[GSD Framework]] — 整体框架
- [[GSD 多智能体编排架构]] — 所属编排系统
- [[GSD Commands]] — 支持的命令