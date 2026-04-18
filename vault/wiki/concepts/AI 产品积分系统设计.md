---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["产品设计", "AI工程"]
aliases: ["AI Credit System", "积分定价", "Usage-Based Pricing for AI"]
relates_to:
  - target: "[[资源与能力差异]]"
    type: relates_to
    confidence: 0.6
  - target: "[[令牌计数（Token Counting）]]"
    type: depends_on
    confidence: 0.7
supersedes: null
---

# AI 产品积分系统设计

## 概述
AI 产品（[[Manus]]、v0.dev、Lovable、Bolt、[[Cursor]]、Replit、Builder.io 等）采用的积分/Credits 定价体系深度分析，涵盖五种定价模式、核心设计原则、工程架构实现及行业共性痛点。

## 关键内容

1. **五种定价模式**：
   - 纯订阅（Flat Fee）：ChatGPT Plus $20/月，成本可预期但厂商难控重度用户
   - 按用量计费（Usage-Based）：[[OpenAI]] API，线性公平但用户焦虑
   - 订阅+积分混合（Hybrid）：v0.dev、Lovable、[[Cursor]]，保底收入+控制超量
   - 结果导向（Outcome-Based）：Intercom Fin $0.99/成功解决，价值对齐但"成功"定义复杂
   - 分层积分+每日刷新（Tiered+Daily Refresh）：[[Manus]]，保持日活但 Agent 任务成本黑盒

2. **行业共性痛点——"赌博感"**：几乎所有积分制 AI 产品都面临核心矛盾——用户提交任务时不知道消耗多少积分，事后才知道代价。"I feel like I'm gambling every time I submit a prompt."

3. **Agent 循环耗积分特有问题**：AI 陷入错误修复循环（fix→re-error→fix），每轮消耗积分但没有解决问题，缺乏"检测到循环→暂停"机制。

4. **上下文成本隐性计费**：v0 将聊天历史、文件上传、知识库注入都计为输入 token，导致同一个问题多次询问消耗远超预期，长对话上下文积累使后续每次请求更贵。

5. **v0 迁移教训**：2025 年 5 月从固定月费（近乎无限使用）切换至 token 计费体系，引发社区强烈反弹。核心教训：从旧模式迁移需提前 30 天通知、提供对比说明、给老用户过渡期额外积分、提供使用量估算器、开放 30 天双模式。

6. **Builder.io 最佳实践**：统一货币（所有 AI 操作共用一套积分）、Rollover with Cap（滚存上限为月度额度 2×）、差[[异化]]推理（简单请求消耗少，复杂任务消耗多）、实时状态指示器。

7. **十大设计原则**：
   - 积分≠Token，需要抽象层（用户看到 50 积分，内部 150K input + 80K output tokens）
   - 执行前必须显示预估成本（置信区间而非精确值）
   - 设置消耗上限/看门狗机制（检测循环→暂停）
   - 每日刷新机制（[[Manus]] 每日 300 积分保证轻度用户每天可用）
   - Rollover 与生命周期管理（促销>月度>购买，滚存上限防无限积累）
   - 模型分级+用户自主选择（快速/标准/深度模式，用户选而非系统自动决定）
   - 任务模式隔离计费（Chat Mode 低消耗 vs Agent Mode 高消耗）
   - 使用量可视化仪表盘（趋势图、详细日志、团队视图）
   - 弹性追加与防断线设计（余额<20%警告，耗尽给 24 小时宽限期）
   - 定价切换的用户教育 SOP

8. **工程架构**：核心数据模型（credit_wallets + credit_ledger append-only 账本 + credit_grants）、原子性积分扣减（悲观锁/乐观锁防并发超额）、Rollover 策略实现、基于历史数据或 LLM 复杂度评分的预估成本实现。

## 来源
- [[AI 产品积分系统设计深度分析]] — Manus/v0.dev/行业横向对比/可借鉴设计原则

## 相关
- [[资源与能力差异]] — relates_to
- [[令牌计数（Token Counting）]] — depends_on
