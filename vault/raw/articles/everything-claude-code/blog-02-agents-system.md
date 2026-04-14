# Everything Claude Code 深度解析（二）：Agents 系统 —— 28 个专用子代理的设计艺术

> **系列导航：** [总览](./blog-01-overview-architecture.md) | **Agents系统** | [Skills系统](./blog-03-skills-system.md) | [Hooks与Rules](./blog-04-hooks-rules.md) | [Commands与持续学习](./blog-05-commands-learning.md) | [安全与跨平台](./blog-06-security-crossplatform.md)

---

## 一、为什么需要专用子代理？

在直接使用 Claude Code 时，一个常见的模式是：将一个大任务（比如"给我的 SaaS 应用添加用户认证"）直接扔给主 Agent，然后等待结果。这种方式有几个根本性的问题：

**问题一：上下文污染**

主 Agent 需要同时记住"正在实现哪个功能"、"数据库结构是什么"、"测试框架怎么用"、"安全检查清单"……一旦任务复杂，注意力被大量不相关信息占据，输出质量急剧下降。

**问题二：工具权限过度**

如果 Agent 拥有读取、写入、执行、网络访问的全部权限，一个意外的幻觉（Hallucination）就可能导致生产数据库被清空或敏感文件被删除。

**问题三：领域知识稀释**

一个通用 Agent 对代码审查、安全审计、数据库优化的理解都停留在"通识水平"，无法像专家一样深入。

ECC 的 Agents 系统通过**职责单一化（Single Responsibility）+ 工具最小化（Minimal Toolset）+ 专业知识注入（Domain Expertise Injection）**来解决这三个问题。

---

## 二、Agent 的数据结构

每个 Agent 都是一个 Markdown 文件，使用 YAML frontmatter 定义元数据：

```markdown
---
name: code-reviewer
description: Reviews code for quality, security, and maintainability.
              Called when the user asks for code review or quality analysis.
tools: Read, Grep, Glob, Bash
model: opus
---

You are a senior code reviewer with 15+ years of experience...

## Review Checklist
1. Code correctness
2. Security vulnerabilities
3. Performance implications
...
```

关键字段解析：

| 字段 | 作用 | 设计意图 |
|------|------|----------|
| `name` | Agent 标识符 | 主 Agent 通过名字委托任务 |
| `description` | 触发条件描述 | Claude Code 用于决策是否自动委托 |
| `tools` | 允许的工具列表 | 最小权限原则 |
| `model` | 使用的模型 | 复杂任务用 opus，简单任务用 sonnet |

---

## 三、28 个 Agents 全景图

ECC 的 28 个 Agent 可以按功能域分为六大类：

### 3.1 规划与设计类

| Agent | 文件 | 核心职责 | 工具权限 |
|-------|------|----------|----------|
| `planner` | planner.md | 功能实现规划，输出蓝图 | Read, Grep, Glob |
| `architect` | architect.md | 系统架构决策 | Read, Grep, Glob |
| `chief-of-staff` | chief-of-staff.md | 沟通分诊、草稿起草 | Read |
| `harness-optimizer` | harness-optimizer.md | ECC 线束配置调优 | Read, Write |

**设计亮点：** `planner` 和 `architect` 刻意被设计为**只读（Read-only）**角色——它们只分析、只规划，不执行任何文件写入或命令执行。这确保了规划阶段不会产生任何副作用，只有人类（或主 Agent）明确批准规划后，才进入执行阶段。

### 3.2 代码审查类（按语言分化）

| Agent | 适用语言/框架 |
|-------|-------------|
| `code-reviewer` | 通用（任何语言） |
| `typescript-reviewer` | TypeScript / JavaScript |
| `python-reviewer` | Python（PEP8、类型提示、安全） |
| `go-reviewer` | Go（惯用法、接口设计） |
| `java-reviewer` | Java / Spring Boot |
| `kotlin-reviewer` | Kotlin / Android / KMP |
| `rust-reviewer` | Rust（所有权、生命周期） |
| `cpp-reviewer` | C++（Core Guidelines 合规） |
| `database-reviewer` | SQL / Supabase 查询优化 |

**设计亮点：** 为什么不用一个通用 `code-reviewer` 就够了？因为每种语言都有其独特的"惯用法陷阱"：Rust 的所有权语义、Go 的显式错误处理、Kotlin 的协程模式……通用审查员只能做表面检查，专用审查员才能发现真正的深层问题。

每个语言专用 reviewer 的系统提示中都注入了大量领域特定知识：

```markdown
# rust-reviewer.md (系统提示片段)
You are a senior Rust engineer reviewing for:
- Ownership and borrowing correctness
- Lifetime annotations necessity
- Unsafe code justification
- Error handling patterns (Result/Option chains)
- Async/await correctness
- Memory safety guarantees
- Performance: avoid unnecessary clone(), Box allocation
```

### 3.3 错误修复类

| Agent | 适用场景 |
|-------|---------|
| `build-error-resolver` | 通用构建错误 |
| `go-build-resolver` | Go 编译/链接错误 |
| `java-build-resolver` | Maven/Gradle 构建失败 |
| `kotlin-build-resolver` | Kotlin/Gradle 构建错误 |
| `rust-build-resolver` | Rust 编译错误（borrow checker） |
| `cpp-build-resolver` | C++ CMake/Make 错误 |
| `pytorch-build-resolver` | PyTorch/CUDA 训练环境错误 |

**设计亮点：** 构建错误修复是一个高度重复、模式化的任务，非常适合专用 Agent。`pytorch-build-resolver` 的出现尤其有趣——它专门处理深度学习训练环境中的 CUDA 版本不兼容、显存溢出、分布式训练错误等高度专业化的问题。

### 3.4 测试与质量类

| Agent | 核心职责 |
|-------|---------|
| `tdd-guide` | 强制执行 TDD 工作流 |
| `e2e-runner` | Playwright E2E 测试生成与执行 |

`tdd-guide` 是 ECC 中哲学意义最强的 Agent。它不只是"帮你写测试"，而是会**拒绝**先写实现代码，坚持要求"先写失败测试"：

```markdown
# tdd-guide.md (核心约束)
NEVER write implementation before tests exist.
If asked to implement feature X:
1. Ask: "What test should fail first?"
2. Write the failing test
3. Confirm the test fails: `npm test` → RED
4. ONLY THEN write minimal implementation → GREEN
5. Refactor → IMPROVE
```

### 3.5 文档与运维类

| Agent | 核心职责 |
|-------|---------|
| `doc-updater` | 同步更新文档 |
| `docs-lookup` | API 文档查阅 |
| `refactor-cleaner` | 死代码清理 |

### 3.6 自主执行类

| Agent | 核心职责 |
|-------|---------|
| `loop-operator` | 自主循环任务执行 |
| `security-reviewer` | OWASP Top 10 安全审计 |

`loop-operator` 是 ECC 中最"激进"的 Agent——它被设计为可以**自主执行长期任务**，在没有人工干预的情况下持续工作。它配合 `/loop-start`、`/loop-status` 命令使用，适合 CI/CD 环境中的自动化修复流程。

---

## 四、工具权限设计：最小权限原则实践

ECC 的 Agents 严格遵循最小权限原则（Principle of Least Privilege）：

```
Agents 工具权限矩阵：

审查类 Agent：    [Read, Grep, Glob]           # 只读，不修改任何文件
规划类 Agent：    [Read, Grep, Glob]           # 同上
文档类 Agent：    [Read, Grep, Glob, Write]    # 可写文档文件
修复类 Agent：    [Read, Grep, Glob, Write, Bash]  # 可修改代码，可执行命令
执行类 Agent：    [Read, Write, Bash, WebFetch]   # 完整工具链
```

这不是偶然的——**工具权限就是能力边界，能力边界就是副作用范围**。一个只有 Read 权限的审查 Agent，即使出现幻觉，最坏的结果也只是给出错误建议，而不会真正修改代码库。

---

## 五、模型路由策略

ECC 为不同复杂度的任务设计了不同的模型选择策略：

```
任务复杂度 → 模型选择

简单任务（lint、格式化、简单Q&A）   → claude-haiku   (最快/最便宜)
中等任务（代码审查、测试生成）        → claude-sonnet  (默认，性价比最优)
复杂任务（架构设计、深度调试）        → claude-opus    (最强，按需使用)
```

`/model-route` 命令可以自动根据任务描述推荐模型，避免为简单任务花费过多 Token。

在 v1.8.0 引入的 **NanoClaw v2** 中，还提供了模型热切换、Skill 热加载、会话分支等高级功能。

---

## 六、主代理委托机制

Agents 的价值不只在于它们各自的能力，更在于**主代理如何决策委托**。

当用户触发 `/code-review` 命令时，背后的流程是：

```
用户：/code-review

主 Agent 决策过程：
1. 解析命令意图：需要代码审查
2. 检查可用 Agent：发现 code-reviewer、typescript-reviewer、python-reviewer
3. 检测当前文件类型：*.ts 文件
4. 选择最合适的 Agent：typescript-reviewer
5. 准备委托上下文：当前修改的文件列表、diff 内容
6. 委托给 typescript-reviewer
7. 收集结果，返回给用户
```

这个决策过程对用户透明，但在底层，**每次委托都是一个独立的子上下文窗口**，专注于单一任务，不受主会话历史的干扰。

---

## 七、实战：如何设计一个自定义 Agent

理解了 ECC 的 Agent 设计模式后，你可以为自己的项目创建定制 Agent：

```markdown
---
name: nextjs-reviewer
description: Reviews Next.js App Router code for performance,
             SEO, Server Components usage, and Hydration issues.
             Use when reviewing Next.js 14+ code changes.
tools: Read, Grep, Glob
model: sonnet
---

You are a Next.js App Router expert. Review code for:

## Performance Checks
- Server Components vs Client Components separation
- Dynamic imports and code splitting
- Image optimization (next/image usage)
- Metadata API usage for SEO

## Common Anti-patterns
- Unnecessary `use client` directives
- Waterfall data fetching patterns
- Missing loading.tsx / error.tsx boundaries
- Hydration mismatches

## Security
- Server Action input validation
- Exposed environment variables (NEXT_PUBLIC_ leakage)
- CORS configuration for API routes
```

将这个文件放入 `~/.claude/agents/nextjs-reviewer.md`，它就会在 Claude Code 中自动可用，当主 Agent 识别到 Next.js 相关任务时会自动委托。

---

## 八、数字背后的工程意义

ECC 为什么要有 28 个 Agent 而不是 5 个？

这不是为了看起来功能丰富，而是基于一个深刻的工程洞察：

> **专业化降低了每个 Agent 的上下文负载，从而显著提升了输出质量。**

一个通用审查 Agent 的系统提示可能需要 3000 个 Token 来涵盖所有语言的知识；而一个 TypeScript 专用审查 Agent 的系统提示只需要 800 个 Token，但质量更高。从 Token 经济学角度看，专业化实际上是更便宜的。

更重要的是，当 Agent 对自己的领域范围有清晰认知时，它更容易说"我不知道，你应该问其他 Agent"——这种**知道边界的能力**本身就是高质量 AI 系统的重要特征。

---

## 下一篇预告

[**第三篇：Skills 系统深度解析**](./blog-03-skills-system.md) —— 119 个 Skills 是什么？工作流定义格式、分类体系、以及"持续学习"如何从你的代码历史中自动生成新 Skills？

---

*本文基于 ECC v1.9.0 的公开源码整理。*
