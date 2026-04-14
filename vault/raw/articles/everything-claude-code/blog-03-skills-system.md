# Everything Claude Code 深度解析（三）：Skills 系统 —— 119 个工作流定义与知识注入机制

> **系列导航：** [总览](./blog-01-overview-architecture.md) | [Agents系统](./blog-02-agents-system.md) | **Skills系统** | [Hooks与Rules](./blog-04-hooks-rules.md) | [Commands与持续学习](./blog-05-commands-learning.md) | [安全与跨平台](./blog-06-security-crossplatform.md)

---

## 一、Skill 是什么？为什么它不是 Agent 也不是 Rule？

在 ECC 的架构中，三个概念容易混淆：

- **Rule（规则）**：永远遵守的硬约束，例如"永远不要提交未测试的代码"
- **Agent（代理）**：执行特定任务的专用角色，有独立的上下文窗口
- **Skill（技能）**：工作流定义 + 领域知识的结合体，注入到 Agent 或主会话的上下文中

如果说 Agent 是"厨师"，Rule 是"餐厅操作规范"，那么 Skill 就是"食谱"——具体说明如何一步一步完成某项任务，以及在这个过程中需要知道哪些背景知识。

### Skill 的数据结构

```markdown
---
name: tdd-workflow
description: Test-Driven Development workflow for any language.
             Enforces RED-GREEN-REFACTOR cycle.
when_to_use: When implementing new features or fixing bugs
---

# TDD Workflow

## Core Cycle
1. **RED**: Write a failing test that defines desired behavior
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Improve code quality without breaking tests

## Language-Specific Tooling
### TypeScript
- Test runner: `jest` or `vitest`
- Coverage: `--coverage` flag
- Watch mode: `--watch`

### Python
- Test runner: `pytest`
- Coverage: `pytest-cov`
- Watch: `pytest-watch`

## Coverage Requirements
- Minimum 80% line coverage
- 100% for business logic functions
- Mock external services, not business logic
```

Skill 文件可以非常长（几百行），因为它们是真正的"知识文档"，而不只是简短的指令。

---

## 二、119 个 Skills 的分类体系

ECC 的 Skills 按领域分为以下几大类：

### 2.1 编码质量与 TDD 类（核心骨干）

| Skill | 描述 |
|-------|------|
| `tdd-workflow` | 通用 TDD 方法论 |
| `coding-standards` | 通用编码规范 |
| `verification-loop` | 构建→测试→Lint→类型检查→安全的五步验证 |
| `eval-harness` | Eval 驱动开发（测量 AI 输出质量） |
| `e2e-testing` | Playwright E2E 测试模式和 Page Object Model |
| `plankton-code-quality` | 写时代码质量强制（通过 Plankton Hooks） |

**深度解析：`verification-loop`**

这是 ECC 中最具价值的 Skill 之一。它定义了一个完整的代码质量验证流程：

```
Phase 1: Build Check
  → tsc --noEmit (TypeScript)
  → python -m py_compile (Python)
  → go build ./... (Go)
  
Phase 2: Test Suite
  → npm test (with --coverage)
  → pytest --cov (coverage >= 80%)
  → go test ./... -coverprofile
  
Phase 3: Linting
  → eslint / biome (TypeScript)
  → ruff / pylint (Python)
  → golangci-lint (Go)
  
Phase 4: Type Checking
  → tsc --strict (TypeScript)
  → mypy --strict (Python)
  
Phase 5: Security
  → npm audit (dependencies)
  → bandit (Python)
  → govulncheck (Go)

Result: ALL GREEN → Commit allowed
        ANY FAIL  → Fix and restart loop
```

### 2.2 架构与设计模式类

| Skill | 描述 |
|-------|------|
| `backend-patterns` | API 设计、数据库模式、缓存策略 |
| `frontend-patterns` | React/Next.js 组件模式 |
| `api-design` | REST API 分页、错误响应、版本控制 |
| `database-migrations` | Prisma/Drizzle/Django/Go 迁移模式 |
| `deployment-patterns` | CI/CD、Docker、健康检查、回滚 |
| `docker-patterns` | Compose 网络、数据卷、容器安全 |
| `postgres-patterns` | PostgreSQL 查询优化模式 |

**深度解析：`backend-patterns`**

这个 Skill 注入了大量实战经验，例如：

```markdown
## Repository Pattern
- Encapsulate data access behind standard interface
- Methods: findAll, findById, create, update, delete
- Business logic depends on abstract interface, NOT storage mechanism
- Benefits: testability, swap databases without changing business logic

## Caching Strategy
- Cache-aside pattern for read-heavy data
- Write-through for consistency-critical data
- Cache invalidation: event-driven over TTL when possible
- Never cache user session data in shared cache without namespacing

## API Error Responses
Always return structured errors:
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable message",
    "details": [...]  // optional field-level errors
  }
}
```

### 2.3 语言生态专用 Skills

每个主要语言生态都有完整的 Skills 套件：

**Go 生态：**
- `golang-patterns` — Go 惯用法、接口设计
- `golang-testing` — Go 测试模式、TDD、基准测试

**Python 生态：**
- `python-patterns` — Python 惯用法、类型提示
- `python-testing` — pytest、fixtures、mock
- `django-patterns` / `django-security` / `django-tdd` / `django-verification`

**Java 生态：**
- `springboot-patterns` / `springboot-security` / `springboot-tdd`
- `java-coding-standards` — Java 编码规范
- `jpa-patterns` — JPA/Hibernate 模式

**Swift 生态（Apple 开发者专享）：**
- `swift-actor-persistence` — 线程安全的 Swift 数据持久化
- `swift-protocol-di-testing` — 基于协议的依赖注入
- `swift-concurrency-6-2` — Swift 6.2 并发新特性
- `liquid-glass-design` — iOS 26 Liquid Glass 设计系统
- `foundation-models-on-device` — Apple 设备端 LLM

**C++ 生态：**
- `cpp-coding-standards` — C++ Core Guidelines 合规
- `cpp-testing` — GoogleTest、CMake/CTest

这里体现了 ECC 的一个重要价值：**把语言社区的最佳实践系统化地注入到 AI 的工作上下文中**。没有这些 Skills，Claude Code 对这些框架的使用可能停留在"能跑起来"的水平；有了这些 Skills，输出的代码直接接近"资深工程师 review 通过"的水平。

### 2.4 上下文管理与学习类

| Skill | 描述 |
|-------|------|
| `strategic-compact` | 手动压缩建议（何时/如何压缩上下文） |
| `iterative-retrieval` | 子代理的渐进式上下文精炼 |
| `continuous-learning` | 从会话中自动提取模式 |
| `continuous-learning-v2` | 基于置信度评分的本能学习 |
| `skill-stocktake` | 审计现有 Skills 和 Commands 质量 |

**深度解析：`strategic-compact`**

Claude Code 默认在上下文窗口使用 95% 时自动压缩。这个阈值太高了——在接近满载时压缩，往往会丢失大量关键上下文，导致后续任务质量下降。

`strategic-compact` 定义了一套更智能的压缩时机判断：

```markdown
## COMPACT - 应该压缩的时机
✅ 调研完成，即将开始实现
✅ 一个里程碑完成，开始下一个
✅ 调试完成，继续功能开发
✅ 某个失败的方向放弃，尝试新方向

## DO NOT COMPACT - 不应该压缩的时机
❌ 实现进行到一半（会丢失变量名、文件路径、部分状态）
❌ 跨多文件的重构进行中
❌ 复杂的并发调试进行中

## COMPRESS STRATEGY
在压缩前，先让 Agent 输出一个"状态摘要"：
- 已完成的工作
- 当前进度
- 待完成的任务
- 关键文件路径和变量
然后将这个摘要放在新会话的开头
```

### 2.5 安全审计类

| Skill | 描述 |
|-------|------|
| `security-review` | OWASP Top 10 安全检查清单 |
| `security-scan` | AgentShield 安全审计器集成 |
| `django-security` | Django 安全最佳实践 |
| `laravel-security` | Laravel 安全模式 |
| `perl-security` | Perl Taint 模式、安全 I/O |

`security-review` Skill 包含了一个详细的安全检查清单：

```markdown
## OWASP Top 10 Checklist

### A01: Broken Access Control
- [ ] Authentication on all sensitive endpoints
- [ ] Authorization checks (not just authentication)
- [ ] Principle of least privilege in DB queries
- [ ] IDOR vulnerability check

### A02: Cryptographic Failures  
- [ ] No plaintext sensitive data in logs
- [ ] Passwords hashed with bcrypt/argon2 (NOT MD5/SHA1)
- [ ] TLS enforced, HTTP redirected to HTTPS
- [ ] Secrets not in source code or .env committed

### A03: Injection
- [ ] Parameterized queries (NO string interpolation in SQL)
- [ ] Input validation and sanitization
- [ ] Output encoding (XSS prevention)
...
```

### 2.6 成本感知与 LLM 优化类

| Skill | 描述 |
|-------|------|
| `cost-aware-llm-pipeline` | LLM 成本优化、模型路由、预算跟踪 |
| `regex-vs-llm-structured-text` | 决策框架：何时用正则，何时用 LLM |
| `content-hash-cache-pattern` | SHA-256 内容哈希缓存（文件处理场景） |
| `mcp-server-patterns` | MCP 服务器设计模式 |

**深度解析：`cost-aware-llm-pipeline`**

这个 Skill 非常有实用价值，提供了一个 LLM 成本优化的系统方法：

```markdown
## Model Routing Decision Tree

Is this task deterministic/rule-based?
  YES → Don't use LLM (regex/code)
  NO ↓

Does it require real-time data?
  YES → Add retrieval step first
  NO ↓

Complexity level:
  Trivial (extraction/classification) → haiku
  Moderate (summarization/analysis)  → sonnet
  Complex (reasoning/architecture)   → opus

## Budget Guard Pattern
class LLMBudgetGuard:
    def __init__(self, daily_budget_usd: float):
        self.budget = daily_budget_usd
        self.spent = 0.0
    
    def check(self, estimated_tokens: int, model: str):
        cost = estimate_cost(estimated_tokens, model)
        if self.spent + cost > self.budget:
            raise BudgetExceeded(f"Would exceed ${self.budget}")
```

### 2.7 商业与内容类（v1.7.0 新增）

| Skill | 描述 |
|-------|------|
| `article-writing` | 无"AI味"的长文写作（基于提供的声音风格） |
| `content-engine` | 多平台社交内容和再利用工作流 |
| `market-research` | 来源可追溯的市场和竞争对手研究 |
| `investor-materials` | 融资路演 Deck、备忘录、金融模型 |
| `investor-outreach` | 个性化融资推广和跟进 |
| `frontend-slides` | 零依赖 HTML 演示文稿构建器 |

这一类 Skills 的出现说明 ECC 的定位已经超越了纯编程工具，开始覆盖创业者、产品经理等更广泛的知识工作者场景。

---

## 三、Skill 的运作机制：上下文注入 vs 命令触发

Skills 有两种激活方式：

### 方式一：通过 Commands 主动触发

```bash
/tdd           # 激活 tdd-workflow Skill
/security-scan # 激活 security-review + security-scan Skills
/code-review   # 激活对应的语言审查 Skill
```

### 方式二：配置到 CLAUDE.md 中永久注入

在项目的 `CLAUDE.md` 中引用 Skills：

```markdown
# Project: My SaaS App

## Always Active Skills
See: skills/tdd-workflow/SKILL.md
See: skills/security-review/SKILL.md
See: skills/backend-patterns/SKILL.md
```

这样，每次会话开始时，这些 Skills 的内容就会自动注入到上下文中，Agent 时刻具备这些知识，不需要每次手动触发。

---

## 四、Skill 生成系统：从代码历史自动学习

ECC 最有创意的功能之一是 `/skill-create` 命令——它能分析你的 Git 历史，自动生成 Skill：

```bash
/skill-create              # 分析当前仓库的 Git 历史
/skill-create --instincts  # 同时生成 Instincts（用于持续学习）
```

系统会分析：
- 高频 commit 模式（反映你常做什么）
- PR 中的 code review 评论（反映什么被认为是好代码）
- 修复 bug 的模式（反映常见陷阱）
- 代码结构演进（反映架构偏好）

然后自动生成类似这样的 Skill：

```markdown
---
name: project-auth-patterns
generated_from: git_history
confidence: 0.87
---

# Authentication Patterns for This Project

## JWT Token Handling
Based on 23 commits, this project:
- Stores JWT in httpOnly cookies (not localStorage)
- Refreshes tokens 5 minutes before expiry
- Uses RS256 (not HS256) for signing

## Role-Based Access Control
- Roles stored in `user_roles` table (not JWT payload)
- Always verify role in middleware, not business logic
```

这是 ECC 的"自定义化"杀手锏——它不只给你通用最佳实践，还学习**你的项目特有的最佳实践**。

---

## 五、Skill 质量控制：skill-stocktake

ECC 专门有一个 `/learn-eval` 命令和 `skill-stocktake` Skill 来管理 Skills 的质量：

```markdown
## skill-stocktake 检查清单

### 质量评分标准
- 描述是否清晰？(0-3分)
- 示例是否具体？(0-3分)
- 触发条件是否明确？(0-2分)
- 与其他 Skill 是否有重复？(0-2分)

### 自动清理规则
- 30天未使用 → 标记为 expired
- 置信度 < 0.3 → 标记为 low-quality
- 与高质量 Skill 重复率 > 70% → 标记为 redundant

### /prune 命令
删除所有 expired 状态的 pending instincts
```

---

## 六、Skills vs RAG 知识库：一个有趣的对比

作为一名 RAG 工程师，你可能会想：Skills 和 RAG 有什么区别？

| 维度 | RAG 知识库 | ECC Skills |
|------|------------|------------|
| 存储方式 | 向量数据库 | Markdown 文件 |
| 检索方式 | 语义相似度 | 显式引用/命令触发 |
| 更新方式 | 文档导入 | 手工编写/自动生成 |
| 适合内容 | 大量非结构化文档 | 精炼的工作流和模式 |
| 可解释性 | 低（黑盒检索） | 高（直接可读） |
| 精确度 | 中（依赖向量相似度） | 高（精确匹配） |

Skills 的核心优势是**可解释性和精确性**。当 Agent 遵循一个 Skill 工作时，开发者能够清楚地看到它在遵循什么规则；而 RAG 的检索结果往往不透明，难以 debug。

当然，对于真正的大规模文档库，RAG 仍然是必要的。ECC 的 `docs-lookup` Agent 就是用于文档检索的——但它对接的是真实的 MCP 文档服务，而不是内置的 RAG 系统。

---

## 七、实战：为你的项目创建定制 Skills

基于 ECC 的 Skill 格式，为自己的项目创建 Skill：

```markdown
---
name: taptap-game-api-patterns
description: API patterns specific to TapTap game platform integration.
             Use when implementing game listing, user auth, or review APIs.
---

# TapTap Game API Integration Patterns

## Authentication
- Use OAuth 2.0 with TapTap as provider
- Store tokens in Redis with TTL = token expiry - 5min buffer
- Never store raw tokens in DB, only hashed references

## Rate Limiting
- Game listing API: max 100 req/min per IP
- Always implement exponential backoff:
  retry_delay = min(2^attempt * 100ms, 10s) + jitter

## Error Handling
TapTap API error codes:
- 40001: Invalid token → trigger refresh flow
- 40301: Rate limited → back off 60s
- 50001: Server error → retry 3 times, then fail
```

将这个文件放入 `~/.claude/skills/taptap-game-api-patterns/SKILL.md`，即可在所有 TapTap 相关项目中共享使用。

---

## 下一篇预告

[**第四篇：Hooks 与 Rules 系统**](./blog-04-hooks-rules.md) —— ECC 最"魔法"的两个组件。Hooks 如何在工具调用前后自动执行程序化逻辑？Rules 的分层架构如何确保代码质量约束永不被绕过？

---

*本文基于 ECC v1.9.0 的公开源码整理。*
