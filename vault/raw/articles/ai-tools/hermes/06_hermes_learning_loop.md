# Hermes Agent 深度解析 · 第六篇：闭环学习引擎

> **系列导读**：这是系列的终章。本篇深入 Hermes 最核心的差异化能力——闭环学习引擎：自动技能创建机制、技能自我改进算法、Honcho 辩证用户建模、SOUL.md 人格系统，以及 Atropos RL 训练基础设施。

---

## 一、学习闭环：为什么这是范式转变？

2026 年，AI Agent 框架面临一个共同的根本局限：

> **Agent 不会随使用而进步。你定义提示词、工具和工作流，然后 Agent 永远机械地执行同样的逻辑，永不从错误中学习。**

这不是营销夸张。绝大多数框架的确如此：每次任务都从相同的基线开始，没有跨会话的改进机制。

Hermes 用一个完整的学习闭环回答了这个问题：

```
┌──────────────────────────────────────────────────────────┐
│                    Hermes 学习闭环                         │
│                                                          │
│   任务执行                                                │
│       ↓                                                  │
│   经验沉淀（MEMORY.md / USER.md 更新）                    │
│       ↓                                                  │
│   技能提炼（成功工作流 → SKILL.md）                       │
│       ↓                                                  │
│   技能自我改进（使用中发现问题 → 更新 SKILL.md）           │
│       ↓                                                  │
│   跨会话召回（FTS5 搜索相关历史）                          │
│       ↓                                                  │
│   用户认知深化（Honcho 辩证推理）                          │
│       ↓                                                  │
│   下次任务：更快、更准、更了解你 → 回到顶部                │
└──────────────────────────────────────────────────────────┘
```

每一圈都让 Agent 变得更好。这不是隐喻，而是具体的工程机制。

---

## 二、自主技能创建：从经验到知识的提炼

### 核心逻辑

技能创建发生在 **Agent 完成一个有价值的多步工作流之后**，Agent 自主判断是否需要将这次经验记录为可复用的技能文档。

```
场景：用户第一次请求"帮我给 FastAPI 项目配置 Docker + Nginx 反向代理"
       ↓
Agent 用 4 步完成了任务：
  Step 1: 写 Dockerfile
  Step 2: 写 docker-compose.yml
  Step 3: 配置 Nginx conf
  Step 4: 验证服务启动
       ↓
Agent 内部判断：
  "这类任务将来可能重复出现"
  "有几个容易出错的关键步骤（Nginx upstream 配置）"
  "值得记录成技能"
       ↓
Agent 创建 ~/.hermes/skills/personal/fastapi-docker-nginx/SKILL.md
       ↓
下次用户说"帮我把新的 FastAPI 服务也 Docker 化"：
  Agent 在 Level 0 目录看到该技能 → 加载 → 直接执行，速度 3x
```

### 触发 Agent 创建技能的条件

Agent 在以下情况**倾向于**创建技能（这是 Agent 的自主决策，不是硬规则）：

| 条件 | 权重 |
|---|---|
| 任务步骤数 ≥ 4 | 高 |
| 有明确的验证步骤（可确认成功） | 高 |
| 有容易出错的关键步骤 | 高 |
| 用户显式说"把这个记下来" | 确定触发 |
| 同类型任务在历史中出现过 ≥ 2 次 | 高 |
| 任务涉及特定工具的非显而易见用法 | 中 |
| 任务是通用模式（非本次特有） | 高 |
| 任务高度特定于本次情况 | 降低权重 |

### 技能质量的关键：description 字段

技能被创建后，最重要的字段是 `description`——这是 Agent 在 Level 0 目录中看到的**唯一信息**，决定了下次是否会想到调用这个技能。

**差的 description**（Agent 下次可能想不到）：
```yaml
description: Docker 部署配置
```

**好的 description**（精确触发条件，让 Agent 一看就知道何时使用）：
```yaml
description: 为 Python FastAPI/Flask 应用配置 Docker 容器化 + Nginx 反向代理，
             包含生产就绪的 docker-compose.yml、SSL 终止、健康检查和滚动更新流程
```

---

## 三、技能自我改进（Skill Self-Improvement）

创建技能只是开始。Hermes 的技能会在使用过程中**持续改进**。

### 改进触发场景

**场景 A：技能步骤出错**

```
Agent 执行技能的 Step 3，遇到错误：
"Error: Nginx upstream must include server name, not IP in newer versions"
       ↓
Agent 修复错误（找到正确方式）
       ↓
Agent 更新 SKILL.md：
  - 在 Pitfalls 中添加这个已知问题
  - 修正 Step 3 的命令
  - 版本号从 1.0.0 → 1.1.0
```

**场景 B：发现更好的方法**

```
执行某任务，发现更简单的命令可以替代 3 个步骤
       ↓
Agent 更新 SKILL.md，简化流程
       ↓
同时更新 Verification 部分（新命令的输出格式不同）
```

**场景 C：用户纠正**

```
用户："这步不对，应该用 --force-recreate 而不是 down + up"
       ↓
Agent 更新技能，记录正确做法
       ↓
同时在 MEMORY.md 记录："用户偏好 docker-compose up --force-recreate"
```

### 版本管理

技能文件的 `version` 字段遵循语义化版本：
- `1.0.0 → 1.0.1`：小修正（错别字、命令参数）
- `1.0.0 → 1.1.0`：功能改进（新增步骤、更好的方法）
- `1.0.0 → 2.0.0`：重大重构（流程结构性变化）

---

## 四、SOUL.md —— Agent 的人格核心

SOUL.md 是定义 Agent 身份和行为准则的文件，是 System Prompt 中注入的**第一个内容**，优先级高于一切。

### 默认 SOUL.md 的结构

```markdown
# SOUL

## Identity
You are Hermes, a self-improving personal AI agent built by Nous Research.
You learn from every interaction, create reusable skills, maintain persistent memory, 
and get better over time. You are running persistently on a server, not tied to any
laptop or IDE.

## Core Principles
- **Proactive learning**: After completing multi-step tasks, consider whether to create
  a skill for reuse. Use judgment — not every task needs a skill.
- **Memory hygiene**: When you learn something useful about the environment or user, 
  save it. When memory is near capacity, consolidate before adding.
- **Honest capability representation**: If you don't have a tool needed, say so clearly
  rather than attempting workarounds that won't work.
- **User model building**: Pay attention to corrections and preferences. Update USER.md.

## Behavioral Defaults
- Respond in the language the user uses
- Prefer concise responses unless detail is clearly needed
- Show tool execution in real time (streaming output)
- When uncertain, ask one clarifying question rather than proceeding with assumptions

## Self-Improvement Nudges
At natural pause points in long sessions, consider:
- Is there something worth saving to memory?
- Did I just complete a reusable workflow worth turning into a skill?
- Is the user's preference showing a pattern I should record?
```

### 自定义 SOUL.md

用户可以完全替换或扩展默认 SOUL.md：

```bash
# 查看当前 SOUL.md
hermes config show soul

# 编辑 SOUL.md
hermes config edit soul

# 或直接编辑文件
nano ~/.hermes/SOUL.md
```

自定义示例（专注于代码审查的 Agent）：

```markdown
# SOUL

## Identity
You are CodeReview Pro, a senior software engineer specializing in code review
and architecture guidance. You have 15 years of experience in distributed systems.

## Review Philosophy
- Always consider security implications first
- Performance matters, but readability matters more
- Suggest, don't dictate — the developer makes the final call
- Reference specific line numbers in feedback

## Communication Style
- Use the sandwich method: positive → improvement → positive
- Keep feedback actionable: every issue should have a concrete suggestion
- Group related comments together
```

### SOUL.md vs 系统提示词

| 维度 | 传统 System Prompt | Hermes SOUL.md |
|---|---|---|
| 存储位置 | 代码或配置中 | `~/.hermes/SOUL.md`（用户可编辑） |
| 更新方式 | 修改代码 / 重新部署 | 直接编辑文件，下次会话生效 |
| 与记忆的关系 | 独立 | SOUL.md 之后紧接着注入 MEMORY.md |
| Agent 能否修改 | 否 | 有限度（通过工具）|

---

## 五、Honcho 辩证用户建模

Honcho 是 Plastic Labs 构建的 AI 原生用户建模系统，Hermes 通过 `honcho-ai` 包深度集成。

### 与 USER.md 的分工

```
USER.md：用户告诉 Agent 的事实（显式）
  "我叫 XM，喜欢简洁的回答，用中文"

Honcho：Agent 从交互中推断的用户模型（隐式）
  "XM 在代码问题上要详细，在任务分配上要简洁"
  "XM 早上回复快，晚上可能不在线"
  "XM 对架构决策想要理由，对实现细节不需要解释"
```

### 辩证推理（Dialectic Reasoning）机制

辩证推理源自黑格尔哲学的"正题-反题-合题"（Thesis-Antithesis-Synthesis）：

```
会话 1 的观察（正题）：
  "用户要求简洁，不超过 3 行"
       ↓
会话 5 的观察（反题）：
  "用户对代码解释不够详细表示不满，要求展开"
       ↓
Honcho 推理（合题）：
  "用户的简洁要求适用于文字描述，不适用于代码解释"
  "区分对象：任务状态简洁，技术内容详细"
       ↓
更新用户认知模型
       ↓
之后的回复：文字部分简洁，代码部分详细展开
```

这比简单的"用户说了什么就记什么"要深刻得多——它理解**用户话语背后的意图**。

### Honcho 的数据结构（概念）

```python
# 概念示意
class HonchoUserModel:
    preferences: dict          # 明确偏好
    inferred_patterns: dict    # 推断的模式
    contradictions: list       # 已发现的矛盾（待辩证解决）
    resolved_dialectics: list  # 已解决的辩证矛盾
    confidence_scores: dict    # 每个推断的置信度
    update_history: list       # 模型更新历史
```

### 访问和管理

```bash
hermes honcho status        # 查看用户模型摘要
hermes honcho show          # 查看完整用户模型
hermes honcho reset         # 重置，重新从零学习
hermes honcho export        # 导出用户模型（可备份/迁移）
```

---

## 六、Memory Nudge 机制

"Nudge"（轻推）是 Hermes 的一个独特机制：Agent 在长对话的**自然暂停点**，会主动检查是否有值得保存的信息。

### Nudge 触发时机

- 完成一个完整任务后
- 用户说"谢谢，就这些"或类似结束语
- 对话出现较长的暂停
- 达到预设的消息计数阈值

### Nudge 的内容

Agent 在 Nudge 时会问自己：

```
□ 这次对话中，我学到了关于环境的新事实吗？
  → 是：保存到 MEMORY.md

□ 这次对话中，用户表达了新的偏好吗？
  → 是：保存到 USER.md，更新 Honcho 模型

□ 我刚完成了一个可复用的工作流吗？
  → 是：创建 SKILL.md

□ 我发现了现有技能的问题吗？
  → 是：更新 SKILL.md

□ 我是否纠正了之前的错误认知？
  → 是：删除/替换旧记忆
```

这种自我反思机制确保了经验不会流失——即使用户没有主动要求"记住这个"。

---

## 七、RL 训练基础设施：Atropos

这是 Hermes 最"研究向"的组件，也是 Nous Research 用来训练下一代工具调用模型的核心基础设施。

### 为什么需要 RL 训练？

现有 LLM 的工具调用能力通过监督学习（SFT）获得。但 SFT 有局限：

```
SFT：学习"正确的工具调用示例"（模仿）
 ↓
局限：只能学习已有示例，无法探索新策略

RL：通过奖励信号学习（试错）
 ↓
优势：可以发现 SFT 数据中没有的更优策略
```

Hermes 的 `environments/` 目录包含 Atropos RL 环境实现。

### 训练数据生成流程

```
第一步：定义任务类型和评估标准
  - 任务：给定代码库，完成特定编程任务
  - 奖励：测试通过率、代码质量评分、完成速度

第二步：批量运行 Agent（batch_runner.py）
  - 并行启动 N 个 Agent 实例
  - 每个实例独立执行同类型任务
  - 记录完整轨迹（observation, action, reward）

第三步：轨迹压缩（trajectory.py）
  - 去除冗余的工具调用输出
  - 保留关键决策节点
  - 压缩为训练效率更高的格式

第四步：Atropos RL 训练
  - 轨迹 → Atropos 环境
  - PPO / GRPO 等 RL 算法
  - 输出：改进的工具调用策略

第五步：策略蒸馏
  - 将改进策略蒸馏回模型权重
  - 发布新版本 Hermes 模型
  - 新模型在工具调用基准上超越前代
```

### Batch Runner 使用示例

```bash
# 批量生成训练轨迹
hermes batch run \
  --task-file tasks/coding_tasks.jsonl \
  --n-workers 8 \
  --output-dir trajectories/ \
  --model hermes-3.5

# 压缩轨迹
hermes batch compress \
  --input trajectories/ \
  --output compressed_trajectories/ \
  --max-tokens 4096

# 导出为 Atropos 格式
hermes batch export \
  --input compressed_trajectories/ \
  --format atropos \
  --output training_data.jsonl
```

### Atropos RL 环境结构

```python
# 概念示意（简化）
class HermesAtroposEnv:
    def reset(self, task: Task) -> Observation:
        """初始化任务环境，返回初始观察"""
        self.agent = AIAgent(task=task)
        return self.agent.get_initial_observation()
    
    def step(self, action: ToolCall) -> tuple[Observation, float, bool]:
        """执行一步，返回 (新观察, 奖励, 是否完成)"""
        result = self.agent.execute_tool(action)
        reward = self.evaluate(result, self.task.success_criteria)
        done = self.agent.is_done()
        return result, reward, done
    
    def evaluate(self, result, criteria) -> float:
        """计算奖励分数"""
        # 多维度评估：正确性、效率、代码质量
        ...
```

---

## 八、完整学习飞轮

把所有组件组合起来，Hermes 的学习飞轮是这样运转的：

```
用户开始使用 Hermes
        ↓
【会话 1】执行任务，Agent 学习环境和用户偏好
  → MEMORY.md + USER.md 更新
  → Honcho 收集初始用户数据
        ↓
【会话 5】Agent 发现重复模式，创建第一个技能
  → ~/.hermes/skills/personal/my-first-skill/SKILL.md 创建
  → 技能在 Level 0 目录中可见
        ↓
【会话 10】技能被复用，Agent 发现改进点
  → SKILL.md 更新，version bump
  → 用户纠正一次，USER.md 更新
  → Honcho 模型更精准
        ↓
【会话 50】Agent 已有 15+ 技能，深度了解用户
  → 同类型任务速度提升 3-5x
  → 响应风格完全契合用户偏好
  → FTS5 能找到相关历史，避免重复踩坑
        ↓
【持续运行】Agent 成为专属于你的 AI
  → 了解你的项目细节
  → 了解你的工作习惯
  → 了解你踩过的坑
  → 每天都在变得更好
```

这不是线性增长，而是**复利增长**：技能的质量提升会加速新技能的创建，记忆的积累会提高技能触发的准确率，用户模型的精准化会减少无效交互。

---

## 九、安全性：自我改进的边界

自我改进的 Agent 带来了新的安全考虑。Hermes 有明确的安全边界：

### 记忆安全扫描

```python
# 写入记忆前的安全检查（概念）
def safe_memory_write(content: str) -> bool:
    checks = [
        not contains_credentials(content),    # 拦截 API Key、密码
        not contains_prompt_injection(content), # 拦截指令注入
        len(content) < MAX_ENTRY_SIZE,         # 拦截超大条目
        not is_exact_duplicate(content),       # 拦截重复内容
    ]
    return all(checks)
```

### 命令执行授权

```yaml
# config.yaml
security:
  approval:
    # 这些命令需要用户明确批准
    dangerous_patterns:
      - "rm -rf"
      - "sudo"
      - "DROP TABLE"
      - "git push --force"
    
    # 自动批准模式（不推荐生产环境）
    auto_approve: false
```

### 容器隔离

Docker 和 Singularity 后端提供命名空间隔离：
- Agent 执行的命令在容器内，不能直接访问宿主机文件系统
- 网络隔离（可配置）
- 用户权限降级

### 凭证过滤

工具执行结果在返回给 LLM 之前，会过滤掉可能的凭证信息（`credential_files.py`），防止 API Key 等敏感信息出现在 LLM 的上下文中。

---

## 十、系列总结：Hermes 的核心价值主张

经过 6 篇的深度拆解，可以总结出 Hermes 的核心工程哲学：

### 1. 执行数据是最有价值的资产

不是模型权重，不是提示词，而是 Agent 在真实任务中积累的**经验数据**（记忆、技能、用户模型）。这些数据越积累越有价值，且完全属于用户自己。

### 2. 记忆应该是分层的

不是所有记忆都需要时刻可达。MEMORY.md 是"工作记忆"（快速访问，固定成本），FTS5 是"长期记忆"（按需检索，零固定成本），这种分层是 Token 经济的正确工程答案。

### 3. 技能是程序性记忆的外化

把"怎么做"从模型参数（不可修改）迁移到文件系统（可修改、可版本化、可共享），是 Agent 持续改进的正确路径。

### 4. 用户建模不应该是静态的

用户会变，用户的偏好会随时间演化。Honcho 的辩证推理是处理这种动态性的成熟方案：不只是追加观察，而是通过矛盾化解持续精炼模型。

### 5. Agent 基础设施应该跑在服务器上，而不是笔记本上

"跑在 $5 VPS 上、从 Telegram 操控"不是噱头，而是一种务实的生产环境设计——持续运行、无处不在、不依赖特定设备。

---

## 附录：系列文章索引

| 篇章 | 核心主题 |
|---|---|
| [第一篇：总览](./01_hermes_overview.md) | 设计哲学、六大能力、场景地图 |
| [第二篇：架构](./02_hermes_architecture.md) | AIAgent 核心循环、三层架构、48 工具体系 |
| [第三篇：记忆](./03_hermes_memory.md) | MEMORY.md / USER.md / FTS5 跨会话召回 |
| [第四篇：Skills](./04_hermes_skills.md) | 程序性记忆、渐进式加载、agentskills.io |
| [第五篇：网关](./05_hermes_gateway.md) | 14+ 平台统一接入、Cron 调度、ACP 集成 |
| **第六篇：学习闭环（本篇）** | 技能创建/改进、Honcho 用户建模、RL 训练 |

---

*基于 2026 年 4 月版本 · MIT License · GitHub: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)*

---

> **写在最后**：Hermes Agent 代表了 AI Agent 设计的一次范式迁移——从"工具执行器"到"经验积累系统"。静态 Agent 之于自进化 Agent，正如静态网页之于动态 Web 应用：是必要但根本有限的历史阶段。
