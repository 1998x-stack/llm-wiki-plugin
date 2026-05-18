---
type: synthesis
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 3
aliases: []
tags: [AI, Agent, 评估, 设计哲学, 软件工程, Agent系统]
synthesizes:
  - "[[DeepAgents评估体系]]"
  - "[[LLM-as-Judge]]"
  - "[[DeepAgents]]"
relates_to:
  - target: "[[DeepAgents评估体系]]"
    type: synthesizes
    confidence: 0.95
  - target: "[[LLM-as-Judge]]"
    type: synthesizes
    confidence: 0.9
  - target: "[[DeepAgents]]"
    type: synthesizes
    confidence: 0.9
supersedes: null
---

# DeepAgents 评估设计哲学：三重分离原则

## 洞见

[[DeepAgents]] 的评估体系建立在**三条核心分离线**上，每条分离线都针对一个常见的"评估混淆陷阱"：

---

## 第一分离：正确性 vs 效率

**混淆陷阱**：将"多走了一步"等同于"做错了"，导致探索性行为被惩罚，Agent 趋向保守策略。

**解法**：两层断言模型
- **成功断言（SuccessAssertion）** → 正确性，任一失败 = `pytest.fail`（测试红）
- **效率断言（EfficiencyAssertion）** → 期望步数/工具调用形态，失败 = 仅写入 LangSmith，不报红

**设计哲学**：正确性是门槛，效率是优化方向。不混淆两者，才能既坚持质量底线，又容纳 Agent 在探索中学习的空间。

---

## 第二分离：确定性 vs 语义

**混淆陷阱**：用子串匹配衡量语义等价（漏报），或用 [[LLM-as-Judge|LLM Judge]] 评估固定格式（成本浪费）。

**解法**：双轨成功断言
- **确定性断言**：`final_text_contains`、`file_equals` → 事实性短答案、精确文件内容，成本低、可复现
- **语义断言**（[[LLM-as-Judge]]）：`llm_judge(*criteria)` → 语义正确性、风格、推理完整性，默认 `claude-sonnet-4-6` 评判

**设计哲学**：先问"规则能否表达"，再决定是否需要 LLM。Judge 是最后手段，不是默认选项。准则粒度要细——一条准则一个可[[判定问题]]，失败时 comment 才能定位。

---

## 第三分离：能力 vs 基础设施

**混淆陷阱**：[[Claude Code 沙箱机制|沙箱]] OOM / 超时导致的失败被统计为"模型能力退步"，污染横向对比数据。

**解法**：结构化失败分类（`FailureCategory`）
- `CAPABILITY`：模型能力/策略问题（无基础设施信号）
- `INFRA_OOM / INFRA_TIMEOUT / INFRA_SANDBOX`：基础设施问题
- `is_infrastructure` 属性，在报表中单独分层统计

辅助工具：
- **Wilson 置信区间**：小样本下比正态近似更稳健
- **最小可检测效应（MDE）**：防止在 90 题规模上对 1~2 题涨跌过度解读

**设计哲学**：评估的对象是模型能力，不是运行环境的稳定性。分层之后，才能让改进信号从噪声中浮现。

---

## 整体观察

三重分离背后有一个共同的元原则：**明确你在测什么，不要把不同维度混在一起**。

| 分离 | 避免的混淆 | 代价 | 收益 |
|------|-----------|------|------|
| 正确性 vs 效率 | 把多步探索等同于失败 | 需要维护两类断言 | Agent 有空间探索，能力评估不因效率偏差失真 |
| 确定性 vs 语义 | 过度依赖 LLM（贵）或过度依赖子串（漏） | 需要判断每个准则的表达方式 | 成本与覆盖率的[[帕累托]]最优 |
| 能力 vs 基础设施 | 环境失败污染模型分数 | 需要失败分类器 + 统计工具 | 改进信号从噪声中浮现，横向对比有意义 |

---

## 延伸：这一哲学的普适性

三重分离不是 [[DeepAgents]] 独有的发明，而是**好的软件测试哲学在 AI 评估领域的应用**：
- 正确性/效率分离 ≈ 功能测试 vs 性能测试的分层
- 确定性/语义分离 ≈ [[单元测试]] vs 用户验收测试的粒度选择
- 能力/环境分离 ≈ 应用 bug vs 基础设施 bug 的分类

AI Agent 评估的特殊性在于：Agent 的"轨迹"天然是随机的、多步的，比传统软件的输入/输出更难断言——因此需要更精细的分离设计来抵御各种混淆来源。

## 来源
- [[DeepAgents评估体系]]
- [[LLM-as-Judge]]
- [[DeepAgents]]
