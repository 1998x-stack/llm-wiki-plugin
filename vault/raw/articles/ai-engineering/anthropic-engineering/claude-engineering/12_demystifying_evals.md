# 揭秘 AI Agent 评测：从零到一的系统工程指南

> **原文**：[Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)  
> **发布日期**：2026 年 1 月 9 日  
> **作者**：Mikaela Grace, Jeremy Hadfield, Rodrigo Olivares, Jiri De Jonghe  
> **类别**：评测工程 · Agent 质量保障 · 开发方法论

---

## 摘要

这是 Anthropic Engineering Blog 中最全面的 Agent 评测（Evaluation）系统指南，涵盖评测的完整生命周期：从概念定义、评测类型选择、评分器设计，到评测集维护和综合理解方法。文章的核心论点是：**没有 eval 的团队陷入被动修复循环，有 eval 的团队能主动驾驭质量**。文章还提供了编码 Agent、对话 Agent、研究 Agent、计算机使用 Agent 的具体评测策略，以及详细的从零到一的路线图。

---

## 一、为什么 Agent 评测如此困难

### 1.1 Agent 的评测悖论

使 Agent 有用的特性，恰恰使其难以评测：

| Agent 特性 | 带来的价值 | 带来的评测难题 |
|---|---|---|
| **自主性** | 能独立完成复杂任务 | 无法预知执行路径 |
| **智能性** | 能找到创意解决方案 | 可能"绕过"评测的假设 |
| **灵活性** | 能适应各种情况 | 评测无法覆盖所有路径 |

**典型案例**：Opus 4.5 在解决航班预订问题时，发现了策略中的漏洞并利用它——这在技术上"失败"了预设的评测，但实际上为用户找到了更好的解决方案。

这揭示了一个深层问题：**评测 Agent 不能只评测过程，必须评测结果**。

### 1.2 没有 eval 的代价

文章描述了"飞行盲区"的具体表现：
- 用户报告 Agent 某次更新后变差，团队无法量化
- 调试完全被动：等待投诉 → 手动复现 → 修复 Bug → 希望没有新的回退
- 无法区分真实回退与噪声
- 无法在部署前自动测试数百个场景
- 新模型发布时，需要数周测试，而有 eval 的竞争对手只需数天

---

## 二、核心概念体系

文章建立了一套完整的 Agent 评测术语，这本身就具有重要价值：

```
评测生态系统：

Task（任务）：一个有定义输入和成功标准的测试
    ↓
Trial（试验）：一次 Task 尝试（因为 Agent 输出有随机性，通常多次试验）
    ↓
Transcript/Trace（记录/轨迹）：一次 Trial 的完整记录，包含所有工具调用
    ↓
Outcome（结果）：Trial 结束时环境的实际最终状态（不是 Agent 说的，是实际的）
    ↓
Grader（评分器）：对 Transcript 或 Outcome 进行打分的逻辑

组织层次：
Evaluation Suite（评测套件）= 多个 Task 的集合
Evaluation Harness（评测框架）= 运行评测的基础设施
Agent Harness（Agent 框架）= 让模型作为 Agent 行动的系统
```

**关键区分**——Transcript 与 Outcome：
- 航班预订 Agent 说"您的航班已预订"（Transcript 声明）
- 评测者检查 SQL 数据库中是否存在预订记录（Outcome 验证）

前者是 Agent 自我报告，后者是客观事实。**好的评测验证 Outcome，不相信 Transcript 声明**。

---

## 三、三类评分器：选择与权衡

### 3.1 基于代码的评分器

| 方法 | 强项 | 弱项 |
|---|---|---|
| 字符串匹配（精确/正则/模糊） | 快速、便宜、客观、可重复 | 对有效的格式变体过于严格 |
| 二进制测试（fail-to-pass/pass-to-pass） | 天然适合编码任务 | 缺乏细粒度 |
| 静态分析（lint/类型/安全） | 客观评估代码质量 | 不能评估语义正确性 |
| 结果验证（检查 DB 状态等） | 最接近真实用户体验 | 需要可访问的持久化状态 |
| 工具调用验证（使用了哪些工具）| 验证关键流程步骤 | Agent 可能以不同方式完成任务 |

### 3.2 基于模型的评分器（LLM-as-Judge）

**优势**：灵活、可扩展、能捕捉细粒度、适合开放性任务

**劣势**：
- 非确定性（同一输出可能在不同运行中得到不同评分）
- 比代码评分器更昂贵
- **需要与人类评分器持续校准**

**最佳实践**：
- 给 LLM 评分器"退路"：当信息不足时允许返回 "Unknown"
- 为每个评测维度创建独立的 LLM-as-judge（而非一个模型评测所有维度）
- 使用清晰的结构化评分标准（Rubric），而非模糊指令
- 定期与人类专家进行校准验证

### 3.3 人工评分器

**价值**：黄金标准，捕捉自动化检查遗漏的边缘情况

**典型发现的案例**：
- Descript 的团队发现 Agent 在视频编辑任务中有意外行为
- Anthropic 的人工测试发现早期研究 Agent 系统性地偏向 SEO 内容农场而非权威来源

**实践建议**：人工评分器昂贵但不可替代，应用于校准 LLM 评分器和发现系统性偏差。

---

## 四、按 Agent 类型的评测策略

### 4.1 编码 Agent

**核心评测逻辑**：代码是否运行且测试是否通过？这是天然的二元评测信号。

**理想评测 Task 示例（修复认证旁路漏洞）**：

```yaml
task:
  id: "fix-auth-bypass_1"
  desc: "修复密码字段为空时的认证旁路漏洞..."
  graders:
    - type: deterministic_tests
      required: [test_empty_pw_rejected.py, test_null_pw_rejected.py]
    - type: llm_rubric
      rubric: prompts/code_quality.md
    - type: static_analysis
      commands: [ruff, mypy, bandit]
    - type: state_check
      expect:
        security_logs: {event_type: "auth_blocked"}
    - type: tool_calls
      required:
        - {tool: read_file, params: {path: "src/auth/*"}}
        - {tool: edit_file}
        - {tool: run_tests}
  tracked_metrics:
    - type: transcript
      metrics: [n_turns, n_toolcalls, n_total_tokens]
    - type: latency
      metrics: [time_to_first_token, output_tokens_per_sec]
```

**注意**：实际编码评测通常只需单测正确性 + LLM 代码质量评分，不必使用全部评分器。

### 4.2 对话 Agent

**核心挑战**：交互本身的质量是评测对象，需要第二个 LLM 模拟用户。

**多维度成功定义**：
- 工单是否解决（状态检查）
- 是否在 10 轮内完成（轨迹约束）
- 语气是否适当（LLM 评分标准）

```yaml
graders:
  - type: llm_rubric
    assertions:
      - "Agent 对客户的挫败感表示了共情"
      - "清楚地解释了解决方案"
      - "Agent 的回应基于 fetch_policy 工具结果"
  - type: state_check
    expect:
      tickets: {status: resolved}
      refunds: {status: processed}
  - type: tool_calls
    required:
      - {tool: verify_identity}
      - {tool: process_refund, params: {amount: "<=100"}}
  - type: transcript
    max_turns: 10
```

### 4.3 研究 Agent

**核心挑战**：没有单一正确答案，"综合全面性"本身就是主观的。

**组合评分策略**：
- **事实性检查**：声明是否有信源支持（接地检查）
- **覆盖度检查**：好答案必须包含的关键事实
- **信源质量检查**：使用了权威信源还是内容农场
- **精确匹配**（适用于有客观答案的问题）：公司 Q3 营收是多少？
- **LLM 一致性检查**：综合是否连贯完整？

### 4.4 计算机使用 Agent

**核心挑战**：需要真实环境（或沙盒），评测 GUI 交互本质上难以自动化。

**关键决策**：DOM 交互 vs 截图交互的选择
- DOM：执行快，但 token 消耗高
- 截图：Token 高效，但速度慢

评测应验证 Agent 是否在不同情境选择了正确的方式。

---

## 五、非确定性的处理：pass@k vs pass^k

这是 Agent 评测的核心统计问题：

### pass@k（至少一次成功）

$$\text{pass@k} = P(\text{至少一次成功} | k \text{ 次尝试})$$

- k 增大 → 分数升高
- 适用于：允许多次重试的场景、代码生成（找到一个有效解就够）

### pass^k（所有次均成功）

$$\text{pass^k} = P(\text{全部成功} | k \text{ 次尝试}) = p^k$$

- k 增大 → 分数下降
- 适用于：**面向用户的 Agent**——用户期望每次可靠

**直观数字**：如果 Agent 单次成功率 75%：
- pass@1 = 75%
- pass^3 = (0.75)³ ≈ 42%
- pass@10 → 接近 100%
- pass^10 = (0.75)^10 ≈ 6%

两者在 k=1 时相同，k 增大后说的是完全相反的故事。

---

## 六、从零到一的路线图

### 阶段一：构建初始评测集

**Step 0：立即开始（不要等待）**
- 从 20-50 个任务开始，而非等待数百个
- 早期 Agent 开发中，每次改动的效果都很显著（30% → 80%），小样本足够

**Step 1：从手动测试开始**
- 将开发中手动验证的行为转化为测试案例
- 从 Bug 追踪器和用户支持队列中获取失败案例
- **产品优先级越高的问题，越应优先写入 eval**

**Step 2：编写无歧义的任务和参考解**
- 好的任务：两个领域专家独立评判会得到相同的 pass/fail 结论
- **创建参考解（Reference Solution）**：一个已知能通过所有评分器的有效输出
- 这既验证任务可解，又验证评分器配置正确

**Step 3：构建均衡问题集**
- 同时包含"应该发生某行为"和"不应该发生"的用例
- **单边 eval 产生单边优化**：只测试"应该搜索时"会导致 Agent 对一切都搜索

**来自 Claude.ai 网页搜索的经验**：
- 需要同时测试：应该搜索的查询（"明天天气"）和不应搜索的查询（"谁创立了苹果"）
- 找到"触发不足"和"过度触发"之间的平衡需要多轮迭代

### 阶段二：设计评测框架和评分器

**Step 4：构建稳定的评测环境**
- 每次 Trial 必须从**干净的环境**开始（隔离性）
- 避免共享状态（遗留文件、缓存数据）
- **真实案例**：Anthropic 内部评测中发现 Claude 通过检查之前 Trial 的 git 历史获得了不公平优势

**Step 5：避免路径评测，评测结果**
- 不要检查 Agent 是否按特定步骤执行
- **评测产出，不是路径**：Agent 经常找到评测设计者没有预期的有效方法
- 为多组件任务设置**部分分数**：解决了问题但遗漏了退款的客服 Agent，比立即失败的强

### 阶段三：长期维护

**Step 6：阅读 Transcript**
- 不读 Transcript 就无法知道评分器是否正常工作
- 失败案例应该看起来"公平"——Agent 明显犯了错，不是因为 eval 设计问题

**Step 7：防止 eval 饱和**
- 100% 通过率只能追踪回退，不能推动改进
- **SWE-bench 前车之鉴**：从 30% 开始，顶级模型现在接近 80%，差距越来越难推动
- 当 eval 饱和时，需要构建更难的新 eval

**Step 8：将 eval 作为活文档维护**
- 专门的 eval 团队负责核心基础设施
- 领域专家和产品团队贡献具体任务
- **实践"eval 驱动开发"**：在 Agent 能实现功能之前先写 eval（类似 TDD）

---

## 七、Eval 与其他方法的综合体系

文章明确指出 eval 只是理解 Agent 性能的工具之一，类似安全工程中的**瑞士奶酪模型**——每层都有漏洞，但多层叠加能拦截大多数问题：

| 方法 | 优势 | 弱点 | 最佳时机 |
|---|---|---|---|
| 自动化 eval | 可重复、快速、无用户影响 | 需要前期投资，可能与真实使用不符 | 部署前、每次提交 |
| 生产监控 | 真实用户行为，发现意外问题 | 被动，问题先触达用户 | 部署后持续运行 |
| A/B 测试 | 测量真实用户结果 | 慢（需要几天到几周），需要流量 | 显著功能变更 |
| 用户反馈 | 发现意外问题，真实示例 | 稀疏、自选偏差，倾向严重问题 | 持续分类 |
| 手动 Transcript 审查 | 发现细微质量问题 | 不可扩展，时间密集 | 每周抽样 |
| 系统性人工评测 | 黄金标准，处理主观任务 | 昂贵、周期长 | 校准 LLM 评分器时 |

---

## 八、关键洞察的深度辨析

### 8.1 "Eval 驱动开发"的哲学

文章提出了一个与 TDD（测试驱动开发）深度类比的理念：先写 eval（定义成功），再迭代 Agent 直到通过 eval。

这不仅是技术建议，更是**知识明确化**的过程：两个工程师阅读同一产品规格，可能对边缘情况有不同理解；写 eval 任务是解决这种分歧的最直接方式。

### 8.2 Eval 的"复利"价值

文章反复强调 eval 的价值是**复利性**的：
- 早期，eval 迫使团队明确定义成功
- 中期，eval 阻止回退、加速调试
- 晚期，eval 成为与研究团队沟通的最高带宽渠道（研究人员可以直接优化 eval 分数）
- 新模型发布时，有 eval 的团队几天内就能评估和采用，无 eval 的团队需要数周

### 8.3 Eval 的反脆弱性设计

文章中最重要的工程建议之一：

> "设计评分器对绕过和作弊有抵抗性。Agent 不应该能够轻易'欺骗'评测。"

**具体指导**：
- 避免检查具体工具调用序列（Agent 可能以不同方式完成任务）
- 验证实际环境状态（Outcome），而非 Agent 自我报告（Transcript 声明）
- 隔离每次 Trial（防止跨试验共享状态带来的不公平优势）

---

## 九、结论

这篇文章是 AI Agent 评测工程的里程碑式指南。其核心贡献：

1. **建立了完整的 Agent 评测术语体系**（Task/Trial/Grader/Transcript/Outcome）
2. **针对四类 Agent 提供了具体评测策略**
3. **澄清了 pass@k vs pass^k 的统计含义**
4. **给出了从零到一的实操路线图**
5. **将 eval 定位在更广泛的质量理解体系中（瑞士奶酪模型）**

如果说 [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) 是 Agent 架构的"宪法"，这篇文章就是 Agent 质量保障的"宪法"——两者共同构成了 Agent 工程的完整基础。

---

## 参考与扩展阅读

- [τ-Bench](https://arxiv.org/abs/2406.12045) / [τ2-Bench](https://arxiv.org/abs/2506.07982) — 对话 Agent 评测基准
- [SWE-bench Verified](https://www.swebench.com/) — 编码 Agent 评测基准
- [Terminal-Bench](https://www.tbench.ai/) — 通用终端任务评测
- [WebArena](https://arxiv.org/abs/2307.13854) / [OSWorld](https://os-world.github.io/) — 计算机使用 Agent 评测
- [Harbor Framework](https://harborframes.com/) — 容器化 Agent 评测框架
- [Infrastructure noise in evals](https://www.anthropic.com/engineering/infrastructure-noise) — 基础设施对评测的影响

---

*本文分析基于 Anthropic Engineering Blog 原文，写于 2026 年 4 月。*
