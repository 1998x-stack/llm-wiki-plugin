# Compound Engineering 深度解析
> Every Inc 出品 · 作者：Kieran Klaassen & Claude · GitHub: EveryInc/compound-engineering-plugin

---

## 目录
1. [哲学内核：复利工程的本质](#philosophy)
2. [主循环：Plan → Work → Review → Compound](#main-loop)
3. [核心工作流命令（23个）](#workflow-commands)
4. [智能体矩阵（35+个 Agents）](#agent-matrix)
5. [技能库（40+个 Skills）](#skills-library)
6. [文件系统约定与知识积累机制](#filesystem)
7. [插件生态与跨平台兼容](#plugin-ecosystem)
8. [架构设计深度剖析](#architecture)
9. [实战工作流示例](#workflow-example)
10. [优势、局限与适用场景](#assessment)

---

## 1. 哲学内核：复利工程的本质 {#philosophy}

### 核心命题

**Compound Engineering 的根本思想只有一句话：**

> *"每一个工程工作单元，应该让后续工作更轻松——而不是更困难。"*

这与传统软件工程的熵增规律形成直接对抗。大多数代码库随时间推移变得越来越难以维护——每个功能都注入新的复杂度，10年后团队花更多时间与系统搏斗，而非在其上构建。

### 复利思维的逆转

| 传统工程 | 复利工程 |
|---------|---------|
| Bug 修复 → 修复当前问题 | Bug 修复 → **消灭整类未来 Bug** |
| 功能开发 → 增加复杂度 | 功能开发 → **教会系统新能力** |
| 代码审查 → 一次性质量检查 | 代码审查 → **提取可复用模式** |
| 经验 → 留在高级工程师头脑中 | 经验 → **编码进 CLAUDE.md 和 agents** |
| 每次开发 = 从零开始 | 每次开发 = **站在前人肩膀上** |

### 起源背景

Compound Engineering 诞生于 Every Inc 构建 **Cora**（AI 秘书产品）的实战过程中。Kieran Klaassen 团队在数百个 PR 的磨砺中，逐步将个人生产力技巧系统化，形成了这套完整方法论。

Every Inc 目前用同一套系统运营 **5个产品**（Cora、Monologue、Sparkle、Spiral、Every.to），每个产品配备**单人工程团队**。这是这套方法论最有力的现实证明。

### "80/20 时间分配原则"

```
计划(Plan) + 审查(Review) = 80% 工程师时间
执行(Work) + 积累(Compound) = 20% 工程师时间
```

这与传统直觉相反——传统上"写代码"占大多数时间，但复利工程认为：**思考发生在代码写之前和之后，代码只是思考的输出**。

---

## 2. 主循环：Plan → Work → Review → Compound {#main-loop}

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPOUND ENGINEERING 主循环                    │
│                                                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌───────────┐  │
│  │  PLAN    │───▶│   WORK   │───▶│  REVIEW  │───▶│ COMPOUND  │  │
│  │          │    │          │    │          │    │           │  │
│  │理解需求  │    │设置隔离  │    │多智能体  │    │捕获方案   │  │
│  │研究代码库│    │执行计划  │    │并行审查  │    │建立索引   │  │
│  │外部调研  │    │运行验证  │    │优先级排序│    │更新系统   │  │
│  │设计方案  │    │跟踪进度  │    │解决问题  │    │验证学习   │  │
│  │验证计划  │    │处理问题  │    │捕获模式  │    │持续积累   │  │
│  └──────────┘    └──────────┘    └──────────┘    └───────────┘  │
│        ▲                                               │         │
│        └───────────────────────────────────────────────┘         │
│                        循环，每次都更强                            │
└─────────────────────────────────────────────────────────────────┘
```

### Step 1: Plan（计划）

**目标**：将模糊想法转化为精确蓝图。

执行动作：
- **理解需求**：构建什么？为何构建？有什么约束？
- **研究代码库**：类似功能如何实现？现有模式是什么？
- **外部调研**：框架文档说什么？业界最佳实践是什么？
- **设计方案**：采用什么方法？哪些文件需要修改？
- **验证计划**：方案自洽吗？完整吗？

触发命令：`/ce:brainstorm` → `/ce:plan`

**深度模式（ultrathink）**：自动触发 `/deepen-plan`，派生 **40+ 个并行研究智能体**进行深度调研。

### Step 2: Work（执行）

**目标**：Agent 按计划实施，开发者监督关键节点。

执行动作：
- **设置隔离**：创建 Git worktree（仓库隔离副本），并行开发互不干扰
- **执行计划**：Agent 逐步实现每个任务
- **运行验证**：每次变更后运行测试、lint、类型检查
- **跟踪进度**：检查完成情况，更新剩余任务
- **处理问题**：遇到阻塞时，适应性调整计划

关键洞察：**如果信任计划，就不需要盯着每一行代码。**

触发命令：`/ce:work`

### Step 3: Review（审查）

**目标**：在代码合并前捕获问题，更重要的是提取下一轮的学习材料。

执行动作：
- **多智能体并行审查**：14+ 个专业审查员同时检验代码
- **优先级排序**：P1（必须修复）/ P2（应该修复）/ P3（锦上添花）
- **解决发现**：Agent 基于审查反馈修复问题
- **验证修复**：确认修复正确且完整
- **捕获模式**：记录错误防止再次发生

触发命令：`/ce:review PR#123`

### Step 4: Compound（积累）——最重要的一步

**目标**：将单次功能开发，转化为让系统持续变强的飞轮。

```
传统开发：Plan → Work → Review → [结束，知识蒸发]
复利工程：Plan → Work → Review → Compound → [知识结晶，系统变强]
```

执行动作：
- **捕获方案**：什么奏效了？什么失败了？可复用的洞察是什么？
- **建立可检索性**：添加 YAML frontmatter，打上正确的元数据、标签、分类
- **更新系统**：
  - 将新模式写入 `CLAUDE.md`（Agent 每次会话必读）
  - 需要时创建新的专业 Agent
  - 更新技能库
- **验证学习**：下次系统能自动捕获这类问题吗？

触发命令：`/ce:compound`、`/ce:compound-refresh`

---

## 3. 核心工作流命令（23个）{#workflow-commands}

### 3.1 主循环命令

#### `/ce:ideate` — 创意发现

**功能**：通过发散性构想和对抗性过滤，发现项目的高影响力改进机会。

**设计哲学**：不是执行已知任务，而是**发现值得做的任务**。使用"对抗性过滤"机制淘汰弱想法，只保留真正值得投入的方向。

**适用场景**：产品路线图规划、技术债清理优先级、新功能构思。

---

#### `/ce:brainstorm` — 结构化头脑风暴

**功能**：在正式计划前，探索需求和实现方案。

**工作机制**：
1. 进行轻量级代码库调研
2. 逐一提问（一次只问一个问题），澄清目的、用户、约束、边界情况
3. AI 提出多种方案，供开发者选择
4. 将决策存入 `docs/brainstorms/` 用于移交给 `/ce:plan`

**关键设计**：问题是**逐一**提出的，而非一次性轰炸，降低认知负担。

---

#### `/ce:plan` — 智能计划生成

**功能**：将功能需求转化为有代码库实际根基的结构化实施计划。

**并行研究架构**（同时派生 3 个 Agent）：
```
/ce:plan 触发
    ├── repo-research-analyst      → 分析代码库模式和约定
    ├── framework-docs-researcher  → 查找框架文档和最佳实践  
    └── best-practices-researcher  → 收集业界标准
                ↓
    spec-flow-analyzer             → 分析用户流和边界情况
                ↓
    合并输出：结构化计划（含受影响文件、实施步骤）
```

**置信度门控**：计划生成后有自动置信度检查，低置信度时触发额外调研。

**Ultrathink 模式**：自动运行 `/deepen-plan`，派生 **40+ 并行研究 Agent**。

---

#### `/ce:work` — 自主代码执行

**功能**：Agent 系统性地执行工作项。

**四阶段执行流程**：

```
Phase 1: Quick Start
  └── 创建 Git worktree（隔离工作环境）
  └── 设置分支

Phase 2: Execute  
  └── 逐任务实现，带进度追踪
  └── 每步验证（测试/lint/类型检查）

Phase 3: Quality Check（可选）
  └── 派生 5+ 个审查 Agent（Rails/TS/安全/性能等）

Phase 4: Ship It
  └── 运行 lint
  └── 创建 PR（含自适应描述）
```

---

#### `/ce:review` — 专家委员会审查

**功能**：让 14+ 个专业 Agent 并行审查你的 PR。

**并行审查架构**：

```
/ce:review PR#123
    ├── 安全层
    │   ├── security-sentinel      (OWASP Top 10, 注入攻击, 认证漏洞)
    │   └── security-lens-reviewer (计划级安全评估)
    │
    ├── 性能层
    │   ├── performance-oracle     (N+1查询, 缺失索引, 缓存机会)
    │   └── performance-reviewer   (运行时性能 + 置信度校准)
    │
    ├── 架构层
    │   ├── architecture-strategist      (系统设计决策, 组件边界)
    │   └── pattern-recognition-specialist (设计模式, 反模式, 代码异味)
    │
    ├── 数据层
    │   ├── data-integrity-guardian  (迁移, 事务边界, 引用完整性)
    │   └── data-migration-expert   (ID映射, 回滚安全, 生产验证)
    │
    ├── 质量层
    │   ├── code-simplicity-reviewer  (YAGNI, 不必要复杂度)
    │   ├── correctness-reviewer      (逻辑错误, 边界情况, 状态bug)
    │   ├── maintainability-reviewer  (耦合, 复杂度, 命名, 死代码)
    │   └── testing-reviewer          (测试覆盖漏洞, 弱断言)
    │
    ├── 框架专项层
    │   ├── kieran-rails-reviewer   (Rails约定, Turbo Streams)
    │   ├── kieran-python-reviewer  (PEP 8, 类型提示, Pythonic风格)
    │   ├── kieran-typescript-reviewer (类型安全, 现代ES模式)
    │   └── dhh-rails-reviewer      (37signals约定, 简单性优先)
    │
    └── 部署层
        ├── deployment-verification-agent (Go/No-Go检查清单)
        └── reliability-reviewer         (生产可靠性, 故障模式)
                    ↓
    合并 + 去重 + 优先级排序 → 单一统一报告
```

**去重管道**：多个 Agent 可能发现同类问题，系统自动合并，避免重复修复。

**置信度门控**：每个 Agent 都输出置信度分数，低置信度发现会降级处理。

---

#### `/ce:compound` — 知识结晶

**功能**：将已解决的问题文档化，让团队知识持续积累。

**输出结构**：

```yaml
# docs/solutions/2026-04-fix-n-plus-one-query.md
---
title: "解决 User 关联的 N+1 查询"
category: performance
tags: [activerecord, eager-loading, sql]
solved_at: 2026-04-12
confidence: high
---

## 问题
加载用户列表时触发 N+1 查询...

## 方案
使用 includes(:profile, :posts) 预加载...

## 可复用洞察
凡涉及 has_many 的列表视图，必须检查 eager loading...

## 防止再发
在 CLAUDE.md 中添加：每次实现列表视图，必须审查 N+1...
```

**可检索性设计**：YAML frontmatter 使未来会话能够通过语义搜索找到过去的解决方案。

---

#### `/ce:compound-refresh` — 知识更新

**功能**：刷新过时或已漂移的学习记录，决定是保留、更新、替换还是归档。

**决策树**：
```
对于每条学习记录：
  ├── 仍然准确？        → 保留（更新时间戳）
  ├── 部分准确？        → 更新（补充新情况）  
  ├── 已被更好方案替代？ → 替换（保留历史引用）
  └── 完全过时？        → 归档（不删除，用于历史追溯）
```

---

### 3.2 Git 工作流命令

| 命令 | 功能描述 |
|------|---------|
| `git-commit` | 生成传达价值的提交信息（非描述性的"fix bug"，而是"防止用户数据在并发写入时丢失"） |
| `git-commit-push-pr` | 一键提交 + 推送 + 开 PR，带自适应描述；也可更新现有 PR 描述 |
| `git-clean-gone-branches` | 清理远程追踪分支已删除的本地分支 |
| `git-worktree` | 管理 Git worktrees，支持并行开发（多功能同时进行互不干扰） |

### 3.3 工作流工具命令

| 命令 | 功能描述 |
|------|---------|
| `/changelog` | 为最近合并的 PR 生成吸引人的变更日志 |
| `/feature-video` | 录制功能演示视频（GIF/终端录制/截图），添加到 PR 描述 |
| `/reproduce-bug` | 使用日志和控制台复现 Bug |
| `/resolve-pr-feedback` | 并行解决 PR 审查反馈 |
| `/sync` | 跨机器同步 Claude Code 配置 |
| `/test-browser` | 对 PR 影响的页面运行浏览器测试 |
| `/test-xcode` | 使用 XcodeBuildMCP 在模拟器上构建/测试 iOS 应用 |
| `/onboarding` | 生成 `ONBOARDING.md` 帮助新贡献者理解代码库 |
| `/todo-resolve` | 并行解决 todos |
| `/todo-triage` | 分类整理待办，分优先级 |

### 3.4 实验性命令

#### `/lfg` — Let's F***ing Go（全自主工程）

**功能**：完整自主工程工作流，从需求到 PR，无需人工干预。

**工作流程**：
```
需求输入 → 自动计划 → 自动实施 → 自动审查 → 自动提PR
```

⚠️ **风险提示**：全自主模式下，开发者是"PR 守门人"，批准或拒绝 Agent 提出的整个 PR。

#### `/slfg` — Swarm LFG（集群模式）

**功能**：带并行执行的全自主工作流，多个 Agent 同时工作。

---

## 4. 智能体矩阵（35+ Agents）{#agent-matrix}

### 4.1 代码审查智能体（27个）

这是 Compound Engineering 最核心的竞争力来源——**专业化程度**。

#### 安全专项

**`security-sentinel`**
- 职责：扫描 OWASP Top 10、SQL 注入、XSS、CSRF、身份验证缺陷、授权绕过
- 设计理念：每次审查都假设攻击者视角，不漏过任何可利用漏洞
- 特色：见过所有 SQL 注入变体，认证漏洞无处遁形

**`security-reviewer`**
- 职责：可利用漏洞 + 置信度校准
- 与 sentinel 区别：更关注置信度评分，避免误报

---

#### 性能专项

**`performance-oracle`**
- 职责：N+1 查询、缺失数据库索引、缓存机会、算法瓶颈
- 特色：在你还在读 PR 的时候，它已经发现了 N+1 查询
- 检测范围：数据库查询、内存分配、CPU 密集型操作

**`performance-reviewer`**
- 职责：运行时性能 + 置信度校准
- 特色：区分"确定的性能问题"和"可能的性能问题"，减少噪声

---

#### 架构专项

**`architecture-strategist`**
- 职责：评估系统设计决策、组件边界、依赖方向
- 检测：循环依赖、错误的抽象层次、单体化倾向

**`pattern-recognition-specialist`**
- 职责：识别设计模式、反模式、跨变更集的代码异味
- 特色：不只看单个文件，看变更集整体的模式走向

**`adversarial-reviewer`**
- 职责：构建失败场景，跨组件边界压力测试实现
- 设计哲学：假设实现是错的，尝试找出它如何失败

---

#### 数据专项

**`data-integrity-guardian`**
- 职责：验证数据库迁移、事务边界、引用完整性
- 特色：防止迁移造成数据损坏，检查外键约束完整性

**`data-migration-expert`**
- 职责：验证 ID 映射是否与生产匹配，检查值交换错误
- 特色：专门检查那种在开发环境看不出但生产环境会炸的数据问题

**`data-migrations-reviewer`**
- 职责：迁移安全性 + 置信度校准
- 检查：回滚安全性、零停机部署兼容性

**`schema-drift-detector`**
- 职责：检测 PR 中无关的 schema.rb 变更
- 特色：防止无意中带入其他分支的 schema 变更混入当前 PR

---

#### 框架专项

**`kieran-rails-reviewer`**（超级高级 Rails 开发者）
- 职责：Rails 约定、Turbo Streams 模式、"复杂度不如重复"哲学
- 特色：零妥协地执行约定，是你团队里那个最严格的高级工程师

**`dhh-rails-reviewer`**
- 职责：从 DHH 视角审查 Rails 代码
- 关注：Rails 约定、简单性、避免过度工程、Omakase 栈
- 特色：WWDHD（What Would DHH Do？）——一个内置的 37signals 品味过滤器

**`kieran-python-reviewer`**
- 职责：PEP 8 合规、类型提示、Pythonic 惯用法

**`kieran-typescript-reviewer`**
- 职责：类型安全、现代 ES 模式、Clean Architecture

**`julik-frontend-races-reviewer`**
- 职责：审查 JavaScript/Stimulus 代码中的竞态条件
- 特色：专注于异步操作的时序问题，这类 bug 极难重现

---

#### 质量专项

**`code-simplicity-reviewer`**
- 职责：YAGNI 原则执行、不必要复杂度标记、可读性检查
- 哲学：最简单的正确实现总是正确的起点

**`correctness-reviewer`**
- 职责：逻辑错误、边界情况、状态 bug

**`maintainability-reviewer`**
- 职责：耦合度、圈复杂度、命名质量、死代码

**`testing-reviewer`**
- 职责：测试覆盖漏洞、弱断言
- 特色：不只检查覆盖率数字，检查测试是否真的测了有意义的行为

**`project-standards-reviewer`**
- 职责：检查代码是否符合 `CLAUDE.md` 和 `AGENTS.md` 中定义的项目标准

---

#### 部署专项

**`deployment-verification-agent`**
- 职责：为高风险数据变更创建 Go/No-Go 部署检查清单
- 输出：预部署检查清单 + 部署后验证步骤 + 回滚计划

**`reliability-reviewer`**
- 职责：生产可靠性和故障模式分析
- 检查：单点故障、降级策略、超时处理

---

### 4.2 文档审查智能体（7个）

用于审查计划、设计文档、规格说明——在代码编写**之前**就捕获问题。

| Agent | 职责 |
|-------|------|
| `coherence-reviewer` | 检查文档内部一致性、矛盾项、术语漂移 |
| `design-lens-reviewer` | 检查缺失的设计决策、交互状态、AI Slop 风险 |
| `feasibility-reviewer` | 评估技术方案能否在现实中存活 |
| `product-lens-reviewer` | 质疑问题框架、评估范围决策、发现目标对齐问题 |
| `scope-guardian-reviewer` | 挑战不合理的复杂度、范围蔓延、过早抽象 |
| `security-lens-reviewer` | 在计划层面评估安全漏洞（认证、数据、API） |
| `adversarial-document-reviewer` | 质疑前提、暴露未陈述假设、压力测试决策 |

**关键洞察**：在计划文档上运行这些 Agent，比在代码上修复问题便宜 10 倍。

---

### 4.3 研究智能体（6个）

| Agent | 职责 |
|-------|------|
| `best-practices-researcher` | 收集外部最佳实践和案例 |
| `framework-docs-researcher` | 研究框架文档和最佳实践 |
| `git-history-analyzer` | 分析 git 历史和代码演进 |
| `issue-intelligence-analyst` | 分析 GitHub Issues，发现重复出现的痛点 |
| `learnings-researcher` | 在已积累的机构知识中搜索相关过去方案 |
| `repo-research-analyst` | 研究仓库结构和约定 |

**`learnings-researcher` 的特殊价值**：这是复利机制的核心执行者。它能在 `docs/solutions/` 中搜索语义相关的过去解决方案，将历史经验自动注入当前工作流。

---

### 4.4 设计智能体（3个）

| Agent | 职责 |
|-------|------|
| `design-implementation-reviewer` | 验证 UI 实现是否与 Figma 设计匹配 |
| `design-iterator` | 通过系统性迭代优化 UI |
| `figma-design-sync` | 同步 Web 实现与 Figma 设计 |

---

### 4.5 工作流智能体（4个）

| Agent | 职责 |
|-------|------|
| `bug-reproduction-validator` | 系统性复现和验证 Bug 报告 |
| `lint` | 对 Ruby 和 ERB 文件运行 lint 和代码质量检查 |
| `pr-comment-resolver` | 处理 PR 评论并实施修复 |
| `spec-flow-analyzer` | 分析用户流，识别规格说明中的漏洞 |

---

## 5. 技能库（40+ Skills）{#skills-library}

### 5.1 技能 vs 智能体：架构区分

```
Skills（技能）：领域专业知识，按需调用
  └── 类比：参考手册 / 最佳实践文档
  └── 触发方式：/slash 命令 或 自动触发

Agents（智能体）：执行特定工作的专业子 Agent
  └── 类比：专门的团队成员
  └── 触发方式：由 Skills/命令派生，通常不直接调用
```

### 5.2 开发框架技能

**`agent-native-architecture`**
- 内容：使用 prompt-native 架构构建 AI Agent 的完整指南
- 核心概念：Action Parity + Context Parity
  - Action Parity：Agent 能执行人类能执行的所有操作
  - Context Parity：Agent 看到的上下文与人类一样丰富
- 价值：防止构建出"半个 Agent"——只能做部分动作的伪自主系统

**`dhh-rails-style`**
- 内容：DHH 和 37signals 风格的 Ruby/Rails 编写指南
- 核心原则：约定优于配置、Rails Way、Omakase 栈选择
- 实用价值：确保 Agent 生成的代码风格与团队约定一致

**`frontend-design`**
- 内容：创建生产级前端界面的完整指南
- 包含：设计系统、组件模式、样式约束

**`dspy-ruby`**
- 内容：使用 DSPy.rb 构建类型安全 LLM 应用
- 场景：在 Rails 应用中集成 LLM 功能

**`andrew-kane-gem-writer`**
- 内容：遵循 Andrew Kane 模式编写 Ruby Gem
- 特色：将特定工程师的代码品味编码为可调用的专业知识

### 5.3 内容与协作技能

**`every-style-editor`**
- 功能：按照 Every 的风格指南审查文案
- 价值：确保 Agent 生成的内容符合品牌声音

**`proof`**
- 功能：通过 Proof 协作编辑器创建、编辑和分享文档
- 场景：团队协作写作工作流集成

**`todo-create`**
- 功能：基于文件的 Todo 追踪系统
- 输出格式：`todos/001-ready-p1-fix-auth.md`

### 5.4 自动化工具技能

**`agent-browser`**
- 功能：使用 Vercel 的 agent-browser CLI 进行浏览器自动化
- 安装：`npm install -g agent-browser && agent-browser install`
- 能力：浏览器操作、截图、表单填写、测试自动化

**`gemini-imagegen`**
- 功能：使用 Google Gemini API 生成和编辑图像
- 场景：自动生成 PR 演示图、文档插图

**`orchestrating-swarms`**
- 内容：多 Agent 集群编排的完整指南
- 涵盖：并行任务分配、结果合并、错误处理

**`rclone`**
- 功能：上传文件到 S3、Cloudflare R2、Backblaze B2 等云存储

### 5.5 Beta 实验技能

**`/lfg`** 和 **`/slfg`**：见第 3.4 节实验性命令。

---

## 6. 文件系统约定与知识积累机制 {#filesystem}

### 6.1 项目文件结构

```
your-project/
├── CLAUDE.md                    ← 最重要的文件（每次会话必读）
│   ├── 项目概述和技术栈
│   ├── 编码约定和偏好
│   ├── 从历次问题学到的模式
│   └── Agent 行为指令
│
├── AGENTS.md                    ← Agent 特定配置（可选）
│
├── docs/
│   ├── brainstorms/             ← /ce:brainstorm 输出
│   │   └── 2026-04-feature-x.md
│   ├── solutions/               ← /ce:compound 输出（已分类）
│   │   ├── performance/
│   │   │   └── n-plus-one-eager-loading.md
│   │   ├── security/
│   │   │   └── csrf-protection-pattern.md
│   │   └── architecture/
│   │       └── service-object-extraction.md
│   └── plans/                   ← /ce:plan 输出
│       └── 2026-04-add-notifications.md
│
└── todos/                       ← /todo-triage 和 review 发现
    ├── 001-ready-p1-fix-auth.md
    ├── 002-pending-p2-add-tests.md
    └── 003-review-p3-refactor-mailer.md
```

### 6.2 CLAUDE.md 的机制

`CLAUDE.md` 是整个系统的"大脑"：

```markdown
# Project: Cora

## Stack
- Ruby 3.3, Rails 8.0, Turbo/Stimulus
- PostgreSQL 16, Redis 7
- Deployed on Fly.io

## Code Conventions
- Use service objects for business logic > 3 steps
- Prefer includes() over joins() for association loading
- Always add database indexes for foreign keys

## Learned Patterns (from /ce:compound)
- 2026-03: User associations ALWAYS need eager loading. 
  Check bullet_gem output before any list view PR.
- 2026-02: Background jobs must be idempotent. 
  Add unique job keys for all Sidekiq jobs.

## Agent Instructions
- Run security-sentinel on every PR touching auth/
- Always use git-worktrees for features > 2 days
```

**关键洞察**：`CLAUDE.md` 是**活文档**，随每次 `/ce:compound` 增长，系统智能持续提升。

### 6.3 Solutions 积累机制（机构记忆）

`docs/solutions/` 是整个复利引擎的核心存储：

```
每次 /ce:compound：
  → 产生一个 markdown 文件
  → 带 YAML frontmatter（可机器检索）
  → 存入分类目录

每次 /ce:plan：
  → learnings-researcher 自动搜索 docs/solutions/
  → 将相关过去方案注入当前计划上下文
  → 防止重复解决已解决的问题
```

这是真正的"飞轮效应"：**每次解决问题都让下次更快**。

### 6.4 Todos 优先级系统

```
文件命名格式：{序号}-{状态}-{优先级}-{描述}.md

状态：ready / pending / blocked / done
优先级：p1（必须）/ p2（应该）/ p3（锦上添花）

示例：
  001-ready-p1-fix-csrf-vulnerability.md
  002-pending-p2-add-rate-limiting.md
  003-review-p3-refactor-user-model.md
```

---

## 7. 插件生态与跨平台兼容 {#plugin-ecosystem}

### 7.1 支持的 AI 编码工具

```
compound-plugin sync --target [target]

支持的目标平台：
  ├── claude    → Claude Code（原生插件市场）
  ├── opencode  → OpenCode
  ├── codex     → OpenAI Codex CLI
  ├── pi        → Pi Agent
  ├── droid     → Factory Droid
  ├── copilot   → GitHub Copilot
  ├── gemini    → Gemini CLI
  ├── windsurf  → Windsurf
  ├── kiro      → Kiro
  ├── qwen      → Qwen（通义千问）
  ├── openclaw  → OpenClaw（skills only）
  └── all       → 自动检测所有工具
```

### 7.2 安装方式

**Claude Code（最简方式）**：
```bash
claude /plugin marketplace add https://github.com/EveryInc/every-marketplace
claude /plugin install compound-engineering
```

**NPM 通用安装器**：
```bash
bunx @every-env/compound-plugin install compound-engineering --to [target]
```

**分支安装（测试实验性功能）**：
```bash
bunx @every-env/compound-plugin install compound-engineering \
  --to codex \
  --branch feat/new-agents
```

### 7.3 与 Every 生态的集成

Every Inc 还维护其他相关插件：
- **`every-cotulla`**：知识型工作的 AI 工作流（头脑风暴、计划、审查、执行、学习积累）
- **`openclaw-railway-template`**：OpenClaw 在 Railway 上的部署模板

---

## 8. 架构设计深度剖析 {#architecture}

### 8.1 核心架构决策

**决策 1：Skills 触发 Agents，而非直接调用**

```
用户 → /ce:review → skill 读取规则 → 派生专业 agents → 合并结果
```

这种间接层的价值：
- Skill 定义**策略**（何时派生哪些 Agent）
- Agent 定义**专业知识**（如何执行特定任务）
- 分离使两者可以独立进化

**决策 2：并行 > 串行**

几乎所有需要多方面分析的任务，都采用并行 Agent 架构：
- `/ce:plan` → 3 个研究 Agent 并行
- `/ce:review` → 14+ 个审查 Agent 并行
- 去重管道在合并时运行

并行设计将审查时间从"14个Agent × 2分钟"降低到"大约2分钟"。

**决策 3：置信度门控**

每个 Agent 输出置信度分数。低置信度发现：
- 不会触发强制修复
- 以不同优先级标记
- 减少审查疲劳（噪声管理）

**决策 4：知识持久化**

所有工作成果存入文件系统（而非 Agent 上下文）：
- 超越单次会话的限制
- 支持跨 Agent、跨会话的知识检索
- 可被版本控制，支持团队共享

### 8.2 与其他 Agent 框架的对比

| 维度 | Compound Engineering | LangGraph | CrewAI |
|------|---------------------|-----------|--------|
| 编排方式 | Prompt-native（Markdown 定义） | Code-native（Python 定义） | Code-native（Python 定义） |
| 持久化 | 文件系统 | State Graph | 无内置 |
| 复用机制 | CLAUDE.md + docs/solutions | 图节点 | 自定义 |
| 学习能力 | /ce:compound 显式积累 | 无内置 | 无内置 |
| 上手门槛 | 低（Markdown 文件） | 中（Python 代码） | 中（Python 代码） |
| 定制深度 | 中（受 Markdown 限制） | 高（完整编程能力） | 高 |

### 8.3 "Agent-Native Architecture" 的深意

`agent-native-architecture` skill 揭示了 CE 的设计哲学：

```
传统软件架构的假设：
  人类 → 点击/输入 → 系统响应

Agent-Native 架构的假设：
  Agent → 工具调用 → 系统响应

要求：
  Action Parity：Agent 能做的 == 人类能做的
  Context Parity：Agent 看到的 == 人类看到的
```

这解释了为什么 CE 如此重视：
- Git worktrees（Agent 需要隔离的工作空间）
- 丰富的文件上下文（CLAUDE.md、docs/）
- 结构化输出格式（Todos 命名约定）

---

## 9. 实战工作流示例 {#workflow-example}

### 示例：添加邮件通知功能

```
Day 1: 计划阶段（约 30 分钟）

/ce:brainstorm 为用户评论添加邮件通知
  → Agent 逐一提问：
    Q: 什么触发通知？
    Q: 用户能控制哪些通知？
    Q: 实时发送还是摘要？
  → 输出到 docs/brainstorms/email-notifications.md

/ce:plan 根据头脑风暴结果制定实施计划
  → 3 个 Agent 并行：
    - repo-research: 发现已有 ActionMailer 设置
    - framework-docs: Rails 8 的 Mailbox 新特性
    - best-practices: 邮件延迟发送的标准实践
  → 生成结构化计划，含 7 个实施步骤

---

Day 1: 执行阶段（约 1-2 小时，Agent 自主运行）

/ce:work
  Phase 1: 创建 git worktree feature/email-notifications
  Phase 2: 
    ✓ 创建 UserNotificationMailer
    ✓ 添加 notifications 数据库表和迁移
    ✓ 创建 NotificationPreference 模型
    ✓ 添加 after_create 回调
    ✓ 编写 RSpec 测试
    ✓ 添加邮件预览
  Phase 3: 启动 5 个审查 Agent（quality check）
  Phase 4: 运行 rubocop，创建 PR #142

---

Day 2: 审查阶段（约 10 分钟）

/ce:review PR#142
  → 14 个 Agent 并行审查（约 2 分钟）
  → 合并报告：
    [P1] security-sentinel: missing CSRF protection on unsubscribe endpoint
    [P1] data-integrity-guardian: migration missing index on user_id
    [P2] performance-oracle: N+1 query in notification list view
    [P2] testing-reviewer: missing test for concurrent notification creation
    [P3] code-simplicity-reviewer: mailer method could use yield pattern

/resolve-pr-feedback
  → Agent 并行处理所有 P1/P2 发现
  → 重新运行测试
  → 更新 PR 描述

---

Day 2: 积累阶段（约 5 分钟）

/ce:compound
  → 生成 docs/solutions/security/unsubscribe-csrf-protection.md
  → 生成 docs/solutions/performance/notification-list-n-plus-one.md
  → 更新 CLAUDE.md：
    "邮件相关功能，必须检查：
     1. Unsubscribe 端点的 CSRF 保护
     2. 通知列表的 eager loading
     3. 并发通知创建的幂等性"
```

**结果**：下次任何邮件相关功能开发，`learnings-researcher` 会自动在计划阶段找到这些文档，防止重蹈覆辙。

---

## 10. 优势、局限与适用场景 {#assessment}

### 核心优势

| 优势 | 详情 |
|------|------|
| **知识积累飞轮** | 每次工作都让系统更聪明，真正的复利效应 |
| **最丰富的审查生态** | 35+ 专业 Agent，覆盖面广度和深度均领先 |
| **并行 Agent 架构** | 审查速度快，多维度不互相阻塞 |
| **文档优先设计** | 计划、解决方案、学习全部文件化，可检索 |
| **哲学清晰** | Plan → Work → Review → Compound 循环有完整理论支撑 |
| **跨平台兼容** | 支持 12+ 个 AI 编码工具 |
| **框架无关** | 不绑定特定语言或框架 |

### 局限与挑战

| 局限 | 详情 |
|------|------|
| **初始设置成本** | 需要建立 CLAUDE.md、docs/ 目录结构 |
| **Rails/Ruby 偏向** | 许多 Agent（DHH、Kieran）专门为 Rails 设计，其他栈需自定义 |
| **复利需要时间** | 前几次使用感觉不到复利效应，需要积累 |
| **Agent 数量管理** | 35+ Agent 的维护和升级成本不低 |
| **TDD 不强制** | 与 Superpowers 不同，CE 不强制测试驱动开发 |

### 最适合的场景

✅ **强烈推荐**：
- 长期运营的 Rails/Ruby 产品
- 单人或小团队维护多个产品
- 希望系统性积累团队知识的工程组织
- 代码质量要求高的产品（SaaS、金融、医疗）
- 已有成熟代码库需要持续改进的团队

⚠️ **谨慎选择**：
- 纯粹的快速原型阶段（复利需要时间）
- 非 Rails 栈（需要大量自定义 Agent）
- 个人学习项目（系统相对复杂）

---

## 附录：数字一览

| 指标 | 数值 |
|------|------|
| GitHub ⭐ | ~12,700（增长中） |
| Forks | ~976 |
| 专业 Agents | 35+ |
| Skills | 40+ |
| 支持工具平台 | 12+ |
| 核心循环步骤 | 4 |
| 并行审查 Agent 数 | 14+ |
| 时间分配比 | Plan+Review 80% / Work+Compound 20% |
| 许可证 | MIT |
| 主要语言 | Markdown + YAML |

---

*分析基于 2026 年 4 月 EveryInc/compound-engineering-plugin `main` 分支公开信息*
