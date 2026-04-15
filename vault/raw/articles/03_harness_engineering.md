# 第三阶段：Harness Engineering（驾驭工程）

> **定义**：设计以 AI Agent 为主体编码者的软件开发环境——包括约束系统、反馈循环、可观测性基础设施和熵管理机制——使 AI Agent 能够持续、自主地产出生产级代码，而人类转型为环境架构师（Environment Architect）。

---

## 一、诞生条件（Birth Conditions）

### 技术临界点

| 条件 | 内容 |
|------|------|
| Agent 能力跃迁 | Claude Sonnet 3.5 / GPT-4o 级别模型具备真正的多步骤代码规划能力 |
| 工具调用成熟 | Bash/File/Browser 工具链稳定，Agent 可完成完整开发循环 |
| 长上下文 + 高速推理 | 128K+ 窗口 + Streaming，单次任务可维持足够"工作记忆" |
| Agentic IDE 出现 | Cursor、Windsurf、Claude Code、Codex CLI 将 Agent 带入开发者日常工作流 |
| 规模化证明 | OpenAI Harness 团队：3 人 × 5 个月 = 100 万行代码 + 1500 PRs，零手写代码 |

### 认知临界点

```
旧范式失效信号：
"我花了 2 小时写 Context Engineering Prompt，
Agent 跑了 10 分钟，输出了 500 行意大利面代码，
我又花了 3 小时 review + 重构..."

新问题意识形成：
问题不是 Prompt 不够好，
问题是代码库本身对 Agent 不友好，
问题是没有机械化约束阻止 Agent 走错路，
问题是没有反馈系统告诉 Agent 它做错了。

→ "让 Agent 工作得更好"的方式
  不是优化 Prompt，
  而是优化 Agent 工作的环境。
```

### 社会触发因素
- AI 编码助手从"补全工具"进化为"自主 Agent"
- 初创公司/小团队面临"用 AI 实现 10x 生产力"的竞争压力
- 软件复杂度持续上升，人工 code review 成为瓶颈

---

## 二、5W2H 分析

### What — 是什么

Harness Engineering 是面向 **AI Agent 主导开发**的环境设计学科，核心包含三大支柱：

```
┌───────────────────────────────────────────────────────┐
│                  Harness Engineering                   │
├─────────────────┬─────────────────┬───────────────────┤
│  Context        │  Architectural  │   Entropy &        │
│  Engineering    │  Constraints    │   GC Management    │
│  (上下文工程)    │  (架构约束)      │   (熵管理)         │
├─────────────────┼─────────────────┼───────────────────┤
│ 文档可导航性     │ 依赖方向规则     │ 黄金原则定义       │
│ 渐进式信息披露   │ 边界解析强制     │ GC Agent 自动清理  │
│ 动态上下文注入   │ CI 门控约束      │ 代码质量分级       │
│ Agent 知识地图   │ 禁止循环依赖     │ 技术债检测         │
└─────────────────┴─────────────────┴───────────────────┘
```

### Why — 为什么

**核心洞察**：Agent 失败的根本原因不是 Prompt 不对，而是**环境不对**。

```
Agent 失败诊断树：
                    Agent 产出低质量代码
                           │
         ┌─────────────────┼──────────────────┐
         ▼                 ▼                  ▼
    缺少文档           缺少约束            缺少反馈
    （不知道该         （走了捷径但         （不知道
     遵循什么规范）      没有护栏阻止）       哪里错了）
         │                 │                  │
         ▼                 ▼                  ▼
   写 domain README    加 linter 规则      开放 CI 输出
   建 docs/_map.md     配 CI gate         给 Agent 看日志
```

**关键定理**："一条 linter 规则，一次编写，保护 100 万行代码；而人工 review，只能保护你看见的那几行。"

### Who — 谁在用

| 角色 | 转变 |
|------|------|
| 人类工程师 | 从"主要编码者"转型为"环境架构师" |
| Tech Lead | 从"审查代码"转型为"设计约束系统" |
| DevOps/Platform | CI/CD 管道需要为 Agent 工作流重新设计 |
| AI Agent | 成为真正的"主要编码者" |

### When — 什么时候

- **2024 Q2**：Claude Code Alpha，Agent 首次具备完整文件系统操作能力
- **2024 Q3**：OpenAI Codex CLI + Harness 团队案例公开
- **2024 Q4**：Harness Engineering 作为概念在 AI 工程社区正式传播
- **2025**：Claude Code GA + MCP 生态爆发，Harness 成为 AI-first 团队标配
- **2025+**：自治开发（Autonomous Development）成为行业议题

### Where — 应用场景

- **Greenfield 项目**：从零构建，完全以 Agent 为主要编码者
- **遗留代码库改造**：渐进式引入约束，逐步提升 Agent 自主度
- **大规模代码生成**：如 Roblox UGC、游戏 AI 内容生成管道
- **持续集成流水线**：Agent 在 CI 中自动修复 lint/test 失败
- **技术债清理**：GC Agent 定期扫描并修复历史违规

### How — 怎么做

#### 支柱一：上下文工程（Agent-Oriented Context Engineering）

```
核心原则："地图，不是手册"

错误做法：一个 5000 行的 AGENTS.md，
          塞满所有规则 → 挤占任务上下文 → Agent 无法有效利用

正确做法：可导航的知识结构
```

```bash
# 标准文档结构
docs/
├── _map.md                    # 全局导航地图（最重要）
├── golden-principles.md       # 5-10 条黄金原则（质量基准）
├── _quality-report.md         # 自动生成的质量报告
├── architecture/
│   ├── overview.md            # 系统架构概览
│   ├── layers.md              # 依赖分层定义
│   └── decisions/             # ADR（架构决策记录）
│       └── 001-use-postgres.md
└── domains/
    ├── auth/README.md         # 认证域文档
    ├── payment/README.md      # 支付域文档
    └── core/README.md         # 核心域文档
```

**渐进式信息披露（Progressive Disclosure）**：
```
Agent 请求 → _map.md 提供导航
           → Agent 找到相关 domain README
           → 只加载当前任务需要的信息
           → 任务完成，信息不再占用 context
```

#### 支柱二：架构约束（Mechanical Constraints）

**约束的核心原则：机械可验证，自动全局强制**

```
执行（CI 门控）           不执行（让 Agent 自决）
─────────────────         ──────────────────────
依赖方向                   使用哪个库
边界解析是否存在            内部实现风格
无循环依赖                  函数命名
跨引用有效性                文件内组织

原因：一条 linter 规则保护所有代码
      人工 review 只保护看见的代码
```

**依赖分层示例（TypeScript/Python 均适用）**：
```
Layer 4: API / Controllers     ← 只能向下依赖
    ↓
Layer 3: Application Services  ← 不能依赖 Layer 4
    ↓
Layer 2: Domain / Business     ← 不能依赖 Layer 3/4
    ↓
Layer 1: Core / Utils          ← 不能依赖任何业务层
```

```javascript
// dependency-cruiser 配置示例
module.exports = {
  forbidden: [{
    name: "no-circular",
    severity: "error",
    from: {},
    to: { circular: true }
  }, {
    name: "domain-cannot-depend-on-application",
    from: { path: "^src/domain/" },
    to: { path: "^src/application/" },
    severity: "error"
  }]
}
```

**边界解析强制（Boundary Parsing）**：
```python
# 所有外部数据必须在边界处解析和验证
# BAD（Agent 可能做的）：
def process(data):
    return data["user"]["id"]  # 直接访问，无验证

# GOOD（约束强制的）：
@dataclass
class UserEvent:
    user_id: str
    
    @classmethod
    def parse(cls, raw: dict) -> "UserEvent":
        return cls(user_id=raw["user"]["id"])
        
# CI 检查：每个模块入口必须有 parse() 方法
```

#### 支柱三：熵管理（Entropy & GC Management）

```
熵定律在代码库中的表现：
Agent 生成代码 → 代码累积 → 不一致性增加 → 质量下降
（就像热力学第二定律，系统自然趋向混乱）

反熵机制：GC Agent（垃圾收集代理）
```

**GC Agent 工作流**：
```
定时触发（每周/每次大 PR 后）
    ↓
读取 docs/golden-principles.md
    ↓
扫描代码库，检测违反原则的模式
    ↓
自动生成修复 PR
    ↓
Agent self-review → 通过 → 人工快速审批
    ↓
代码库质量维持在基准线以上
```

**质量分级系统**：
```
Grade A: 完全符合 golden-principles，无技术债
Grade B: 轻微不一致，不影响功能
Grade C: 存在已知违规，已记录为 tech debt
Grade D: 影响维护性的违规，需要优先修复
Grade F: 阻塞性问题，CI 应拒绝合并

GC Agent 目标：将 C/D 级代码自动升级到 B/A 级
```

#### 自治等级（Autonomy Levels）

```
Level 1 — 人工审核所有 PR
  Agent 编码 → 人类 Review 每一个 PR
  适用：刚开始引入 Agent，建立信任
  
Level 2 — 仅架构 PR 需要审核
  Agent 编码 → 结构测试通过 → 只有架构变更需要人工审核
  适用：约束系统建立后，Agent 行为可预测
  
Level 3 — Agent + CI 循环，人类只看高风险变更
  Agent 编码 → Agent self-review → CI 全自动 → 人类看高风险
  适用：Agent 自审能力成熟，错误率 < 5%
  
Level 4 — Agent 管理完整生命周期，人类设定目标
  人类：设定季度目标 → Agent：设计+编码+测试+部署+维护
  适用：整个工程组织 AI-native 化
```

### How Much — 规模/成本

| 维度 | 数据 |
|------|------|
| OpenAI Harness 案例 | 3 人 × 5 个月 = 100 万行代码 |
| 传统效率对比 | 相当于 30–50 名工程师的产出 |
| 约束建立成本 | 前期 1–2 周，一次建立，长期收益 |
| GC Agent 运行成本 | 每次扫描约 1–5 美元（API 成本） |
| 人工 Review 时间节省 | Level 3 后约节省 70% review 时间 |
| 代码质量（关键指标） | 技术债增长率 vs. 无 Harness 的对比 |

---

## 三、核心技术机理

### 为什么"约束"比"指令"更有效？

```
指令（Prompt）：
  "请遵循依赖倒置原则"
  → Agent 可能忘记 / 不理解 / 在复杂任务中优先级降低
  → 软约束，靠 Agent 自律

约束（Linter + CI）：
  dependency-cruiser 在 CI 中检查依赖方向
  → 违反 → CI 失败 → PR 无法合并
  → 硬约束，无需 Agent 自律
  
关键差异：
  约束是"不可能违反"的护栏
  指令是"应该遵守"的建议
```

### 反馈循环的信息论解释

```
Agent 没有反馈 = 盲目行动
            ↓
Agent 有 CI 输出 = 知道"哪里错了"
            ↓
Agent 有日志/测试结果 = 知道"为什么错了"
            ↓
Agent 有质量报告 = 知道"总体质量如何"

信息完备性 → Agent 自我纠正能力
        ↑
这是 Harness Engineering 的可观测性设计目标
```

### GC 的热力学类比

```
软件熵（Software Entropy）：
  代码库在持续开发中自然趋向混乱
  （不一致的命名/架构/模式）
  
GC Agent = 负熵注入器：
  持续识别熵增部分 → 标准化/统一 → 恢复秩序
  
关键：GC Agent 不修改功能逻辑，只修复结构性问题
     = 低风险、高价值的自动化
```

---

## 四、代表性工具生态

```
Agent 编码平台：
├── Claude Code（最强代码 Agent，支持 MCP）
├── Codex CLI（OpenAI，Harness 实践起源地）
├── Cursor / Windsurf（IDE 级别 Agent）
└── GitHub Copilot Workspace（PR 级别 Agent）

约束工具：
├── dependency-cruiser（JS/TS 依赖分析）
├── import-linter（Python 导入约束）
├── ArchUnit（Java 架构测试）
└── custom CI scripts（通用）

可观测性：
├── 标准 CI 输出（GitHub Actions / GitLab CI）
├── 日志系统（ELK / Datadog）
└── 测试覆盖率报告

文档管理：
└── 结构化 Markdown + ADR 规范
```

---

## 五、局限性与挑战

| 挑战 | 描述 | 当前状态 |
|------|------|------|
| 初始投资高 | 建立 Harness 环境需要前期架构设计 | 需要 1–2 周专注投入 |
| 模型能力波动 | Agent 更新可能改变行为模式 | 约束系统可对冲 |
| 数据库迁移风险 | DB Schema 变更仍需人工谨慎审核 | 需特殊审批流 |
| 跨领域依赖 | 多 Agent 并行时的状态冲突 | 编排层设计问题 |
| 创新 vs 约束 | 过度约束可能限制架构演进 | 约束需要版本化管理 |
| 遗留代码库 | 老代码库改造成本高 | 渐进式引入策略 |

---

## 六、历史地位

Harness Engineering 是 LLM 应用工程的**第三次范式跃迁**：

- 将人类从"主要编码者"解放为"环境设计者"
- 第一次让软件工程真正变成"设计 AI 工作的环境"而非"让 AI 帮人工作"
- 证明了"机械约束 > 语言指令"在 AI 工程中的核心价值
- 建立了 AI-native 软件开发的方法论基础

> **核心隐喻**：Harness Engineer = 赛道设计师。不驾驶赛车（Agent），不给赛车手建议（Prompt），而是设计赛道护栏（约束）、维修站（反馈系统）和赛道维护规范（GC），让赛车手（Agent）在正确的边界内跑出最快速度。
