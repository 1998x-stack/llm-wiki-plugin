# Everything Claude Code 深度解析（五）：Commands 与持续学习 —— 从 60 个命令到自我进化的 AI 系统

> **系列导航：** [总览](./blog-01-overview-architecture.md) | [Agents系统](./blog-02-agents-system.md) | [Skills系统](./blog-03-skills-system.md) | [Hooks与Rules](./blog-04-hooks-rules.md) | **Commands与持续学习** | [安全与跨平台](./blog-06-security-crossplatform.md)

---

## 一、Commands：工作流的快捷键

如果说 Agents 是"专业工人"，Skills 是"操作手册"，那么 **Commands（斜杠命令）** 就是"工作台上的快捷键"——一个命令激活一套完整的工作流，让复杂操作变成肌肉记忆。

Claude Code 的原生斜杠命令只有少数几个，ECC 扩展到了 **60 个**，覆盖了软件开发的完整生命周期。

### Command 的数据结构

```markdown
---
name: plan
description: Create a detailed implementation plan before coding.
             Spawns planner + architect agents.
---

# /plan - Implementation Planning Workflow

## Steps
1. Analyze the request and existing codebase
2. Spawn planner agent for implementation blueprint
3. Spawn architect agent for system design decisions
4. Present structured plan for review before any code is written

## Output Format
- Feature breakdown
- File changes required
- Dependencies needed
- Risk assessment
- Estimated complexity

## Usage
/plan "Add user authentication with Google OAuth"
/plan "Refactor payment service to use Stripe webhooks"
```

---

## 二、60 个 Commands 分类全览

### 2.1 开发工作流类（核心日常）

| 命令 | 触发的工作流 | 典型使用场景 |
|------|------------|------------|
| `/plan` | 启动规划 Agent | 新功能开始前 |
| `/tdd` | TDD 工作流 | 任何需要写代码的任务 |
| `/code-review` | 代码审查 | PR 提交前 |
| `/build-fix` | 构建错误修复 | CI 失败时 |
| `/e2e` | E2E 测试生成 | 关键用户流实现后 |
| `/refactor-clean` | 死代码清理 | 功能稳定后的清理 |
| `/security-scan` | 安全审计 | 部署前 |
| `/update-docs` | 文档同步 | 接口变更后 |
| `/test-coverage` | 覆盖率分析 | 周期性质量检查 |

### 2.2 语言专用命令

| 命令 | 目标语言 |
|------|---------|
| `/go-review` | Go 代码审查 |
| `/go-test` | Go TDD 工作流 |
| `/go-build` | Go 构建错误修复 |
| `/python-review` | Python 代码审查（PEP8、类型提示） |

### 2.3 持续学习与知识管理

| 命令 | 功能 |
|------|------|
| `/learn` | 从当前会话中提取模式 |
| `/learn-eval` | 提取、评估后再保存（更严格） |
| `/instinct-status` | 查看已学习的 Instincts（附置信度） |
| `/instinct-import` | 导入他人的 Instincts |
| `/instinct-export` | 导出自己的 Instincts |
| `/evolve` | 将相关 Instincts 聚合成 Skill |
| `/prune` | 删除过期的低质量 Instincts |
| `/skill-create` | 从 Git 历史自动生成 Skills |

### 2.4 上下文与会话管理

| 命令 | 功能 |
|------|------|
| `/checkpoint` | 保存当前验证状态 |
| `/verify` | 运行验证回路 |
| `/sessions` | 管理会话历史 |
| `/compact` | 手动触发上下文压缩 |
| `/eval` | 对照标准评估输出质量 |

### 2.5 多代理编排（v1.4.0+）

| 命令 | 功能 |
|------|------|
| `/orchestrate` | 多代理协调 |
| `/multi-plan` | 多代理任务分解 |
| `/multi-execute` | 编排多代理并发执行 |
| `/multi-backend` | 后端多服务编排 |
| `/multi-frontend` | 前端多服务编排 |
| `/multi-workflow` | 全栈多服务工作流 |
| `/pm2` | PM2 服务生命周期管理 |

### 2.6 线束控制命令（v1.8.0+）

| 命令 | 功能 |
|------|------|
| `/harness-audit` | 审计线束可靠性、Eval 准备度和风险 |
| `/loop-start` | 启动受控自主循环执行 |
| `/loop-status` | 检查活跃循环状态和检查点 |
| `/quality-gate` | 对路径或整个仓库运行质量门控 |
| `/model-route` | 按复杂度和预算路由任务到合适模型 |

---

## 三、几个关键命令深度解析

### `/plan`：规划先于实现的强制工作流

```
用户：/plan "添加 Stripe 支付集成"

执行流程：
1. 主 Agent 解析请求意图
2. 委托 planner Agent：
   - 分析现有代码库结构
   - 识别需要修改的文件
   - 规划实现步骤
3. 委托 architect Agent：
   - 评估架构影响
   - 识别潜在的依赖冲突
   - 提出设计决策
4. 合并两个 Agent 的输出
5. 以结构化格式展示计划

输出示例：
## 实现计划：Stripe 支付集成

### 需要修改的文件
- src/api/payment.ts (新建)
- src/config/stripe.ts (新建)
- src/middleware/webhook.ts (新建)
- .env.example (更新)
- package.json (添加 stripe SDK)

### 实现步骤
1. 安装 @stripe/stripe-js SDK
2. 配置 Stripe 环境变量
3. 实现 PaymentService 类
4. 创建 webhook 处理中间件
5. 编写集成测试

### 风险评估
- 🟡 Stripe Webhook 签名验证需要特殊测试环境
- 🟡 PCI DSS 合规要求检查

是否确认这个计划？确认后开始 TDD 实现。
```

`/plan` 的核心价值是**防止 AI 在没有充分理解需求的情况下就开始写代码**。这是 AI 编程中最常见的质量问题根源之一。

### `/quality-gate`：生产准入的最后防线

```bash
/quality-gate .          # 对整个仓库运行质量门控
/quality-gate src/ --strict  # 严格模式，对 src 目录
```

`/quality-gate` 整合了所有质量检查：

```
Quality Gate 执行矩阵：

Layer 1: Build
  ✅ TypeScript 编译通过
  ✅ 无循环依赖
  
Layer 2: Tests
  ✅ 所有测试通过
  ✅ 覆盖率 ≥ 80%
  ✅ 无跳过的测试

Layer 3: Code Quality
  ✅ ESLint 无错误
  ✅ 无 console.log
  ✅ 无 TODO/FIXME（可配置）

Layer 4: Security
  ✅ 无已知漏洞依赖
  ✅ 无硬编码凭证
  ✅ OWASP 检查通过

Layer 5: Documentation
  ✅ 公开 API 有文档注释
  ✅ CHANGELOG 更新

Total Score: 45/45 → PASS
```

只有所有层级都通过，才允许进行 PR 或部署。

### `/harness-audit`：线束健康度检查

```bash
/harness-audit
```

这是 v1.8.0 引入的元工具，用于评估 ECC 自身的健康状态：

```
Harness Audit Report
====================
Reliability Score: 87/100
Eval Readiness:    74/100
Risk Score:        12/100 (越低越好)

Issues Found:
⚠️  session-start hook: fallback path 未测试
⚠️  3 个 Skills 超过 30 天未使用
❌  hooks.json: post:bash:coverage 正则表达式可能有误

Recommendations:
1. 运行 /verify 验证 hooks 配置
2. 运行 /prune 清理过期 Skills
3. 修复 coverage hook 的正则表达式
```

---

## 四、持续学习系统：Homunculus 灵感的 AI 自我进化

这是 ECC 最具创意，也最具深远意义的功能：**持续学习（Continuous Learning）系统**。

### 设计灵感：Homunculus 理论

Homunculus 是神经科学中的一个概念——大脑中存在一个"小人"，维护着身体的感觉地图，随着使用频率调整不同部位的表征比例（比如手指的神经映射远大于背部）。

ECC 的持续学习系统借鉴了这个思想：**系统对"常用模式"的表征随使用频率自动增强**。你越是重复某种编程模式，系统对它的认知越深，应用越精准。

### 学习系统的三个层次

```
Level 1: Session Extraction（会话内提取）
  每次会话结束后，自动分析：
  - 用了什么技术方案
  - 遇到了什么问题，如何解决
  - 写了什么模式的代码
  → 生成 raw Instincts（原始本能）

Level 2: Instinct Refinement（本能精炼）
  对 Instincts 进行置信度评分：
  - 出现频率高 → 置信度提升
  - 被手动确认 → 置信度提升
  - 在验证中失败 → 置信度下降
  - 30天未用 → 标记 expired
  → 精炼后的 Instincts

Level 3: Skill Evolution（技能进化）
  /evolve 命令将相关 Instincts 聚合：
  - 分析 Instincts 的语义相似性
  - 将高置信度、高相关性的 Instincts 合并
  → 生成结构化的 SKILL.md 文件
```

### Instinct 的数据结构

```markdown
---
instinct_id: inst_20260315_auth_pattern_001
created: 2026-03-15T09:23:41Z
source: session_extract
confidence: 0.82
tags: [authentication, jwt, security]
usage_count: 7
last_used: 2026-03-28T14:11:02Z
---

# Action
When implementing JWT authentication in TypeScript projects,
use httpOnly cookies instead of localStorage for token storage.

# Evidence
- Observed in 7 sessions across 3 different projects
- PR review in project-x flagged localStorage JWT as security risk
- Replaced with httpOnly cookies in 2 bug fixes

# Examples
```typescript
// AVOID: Vulnerable to XSS
localStorage.setItem('token', jwt);

// PREFER: httpOnly cookie (server-side)
res.cookie('auth_token', jwt, {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'strict',
  maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
});
```
```

注意 `confidence: 0.82` 字段——这是 ECC 与简单规则系统的关键区别。Instincts 有置信度，置信度反映了模式的可靠程度，防止低质量的单次观察被过度强调。

### `/learn` vs `/learn-eval`

ECC 提供了两种模式的学习提取：

**`/learn`（快速模式）：**
```bash
/learn  # 在会话进行中，随时提取当前的学习模式
```
直接将当前会话的观察保存为 Instinct，不经过额外评估。适合快速记录"刚发现一个好模式"的场景。

**`/learn-eval`（评估模式）：**
```bash
/learn-eval  # 提取 + 评估 + 置信度打分 + 再保存
```
会先将提取到的模式与现有的 Skills 和 Instincts 进行比较，评估：
- 是否与现有知识重复？
- 这个模式真的是好的实践吗？
- 置信度应该多少？

更严格，但质量更高。

### `/evolve`：Instincts 进化为 Skills

当积累了足够多的 Instincts 后，`/evolve` 命令会将它们聚合成结构化的 Skills：

```bash
/evolve  # 分析所有 Instincts，生成候选 Skill 列表

输出示例：
发现 3 个可进化的 Skill 候选：

1. react-state-patterns (12 Instincts 合并)
   - useState vs useReducer 决策框架
   - Context API 性能优化
   - Zustand 状态切片模式
   置信度: 0.91 → 建议进化为 Skill
   
2. api-error-handling (8 Instincts 合并)
   - 结构化错误响应格式
   - 错误码分类体系
   置信度: 0.78 → 建议进化为 Skill
   
3. git-commit-atomicity (5 Instincts 合并)
   置信度: 0.61 → 建议继续观察

是否进化候选 1 和 2？[y/n]
```

---

## 五、Instincts 的社区共享

ECC 的持续学习系统不只是个人工具，还支持团队协作：

```bash
# 导出你的 Instincts
/instinct-export
→ 生成 instincts-export-20260331.json

# 将 Instincts 分享给团队成员
# 团队成员导入
/instinct-import instincts-export-20260331.json

# 审查导入的 Instincts
/instinct-status --imported
```

这让团队能够共享"专家本能"——资深工程师积累的 Instincts 可以直接传递给新人，加速知识传递。

---

## 六、多代理编排：PM2 + 并行工作流

v1.4.0 引入的多代理命令系列，让 ECC 能够处理真正的大规模并行开发任务。

### `/multi-plan` + `/multi-execute` 模式

```bash
# Step 1: 分解任务
/multi-plan "完整实现用户管理模块"

输出：
任务分解为 4 个并行工作流：
1. [后端] API 端点实现
2. [后端] 数据库模型和迁移
3. [前端] 用户管理界面
4. [测试] 集成测试套件

并行可执行：[1,2,3] 并行，[4] 在 [1,2,3] 完成后执行

# Step 2: 并发执行
/multi-execute --parallel 1,2,3
```

### `/pm2`：长时运行服务的管理

对于需要运行多个服务的全栈应用（前端、后端、数据库、消息队列），`/pm2` 命令自动生成 PM2 配置：

```bash
/pm2  # 分析项目结构，自动生成 pm2 配置

生成的 ecosystem.config.js：
module.exports = {
  apps: [
    {
      name: 'api',
      script: 'src/index.ts',
      interpreter: 'ts-node',
      env: { PORT: 3001, NODE_ENV: 'development' }
    },
    {
      name: 'frontend',
      script: 'npm',
      args: 'run dev',
      cwd: './frontend',
      env: { PORT: 3000 }
    },
    {
      name: 'worker',
      script: 'src/worker.ts',
      instances: 2,
      exec_mode: 'cluster'
    }
  ]
};
```

---

## 七、SQLite 状态存储：v1.9.0 的基础设施升级

v1.9.0 引入了基于 SQLite 的状态存储，这是整个持续学习系统的数据基础：

```
~/.claude/
├── state.db              # SQLite 状态数据库
├── sessions/             # 会话 transcript 归档
└── skills/               # 生成的 Skills

state.db 的表结构：
┌──────────────────────────────────────────┐
│ instincts                                 │
├──────────────┬───────────────────────────┤
│ id           │ 唯一标识符                  │
│ content      │ Instinct 内容              │
│ confidence   │ 置信度 (0.0-1.0)           │
│ source       │ 来源会话 ID                │
│ tags         │ JSON 标签数组               │
│ usage_count  │ 使用次数                   │
│ created_at   │ 创建时间                   │
│ last_used    │ 最后使用时间               │
│ status       │ active/expired/pruned      │
└──────────────┴───────────────────────────┘
```

状态查询 CLI：
```bash
# 查询所有高置信度 Instincts
node scripts/state-query.js --type instincts --min-confidence 0.8

# 查询会话历史
node scripts/state-query.js --type sessions --last 10

# 查询 Skill 使用统计
node scripts/state-query.js --type skills --sort usage_count
```

---

## 八、一个完整的学习闭环

让我们串联起来，看一个完整的持续学习场景：

```
Day 1: 实现 JWT 认证
  → Agent 使用 httpOnly cookies
  → 会话结束：session-end hook 保存状态
  → /learn 提取 Instinct: "jwt-cookie-auth"，置信度 0.4

Day 3: 修复 JWT 安全漏洞
  → 同样的模式被强化
  → Instinct "jwt-cookie-auth" 置信度升到 0.65

Day 7: 代码审查时再次验证
  → /instinct-status 显示 7 次使用记录
  → 置信度 0.82

Day 14: /evolve
  → "jwt-cookie-auth" + 5个相关 Instincts 合并
  → 生成 Skill: auth-security-patterns/SKILL.md
  → 置信度 0.91，推荐在所有项目使用

Day 30+: 团队共享
  → /instinct-export 导出给新同事
  → 新同事 /instinct-import 立即获得这些最佳实践
```

这就是 ECC 的"自我进化"——不是隐喻，而是实实在在发生的知识积累和传播过程。

---

## 下一篇预告

[**第六篇：AgentShield 安全体系与跨平台支持**](./blog-06-security-crossplatform.md) —— ECC 的安全基因、AgentShield 如何扫描 102 种攻击向量、Token 优化策略，以及 Token 经济学在实际工程中的应用。

---

*本文基于 ECC v1.9.0 的公开源码整理。*
