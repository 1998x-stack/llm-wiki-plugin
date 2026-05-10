---
type: concept
status: active
confidence: 0.6
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: ["ai-engineering", "architecture-decision", "debate"]
aliases: ["Build Heavy Harness vs Trust The Model", "重Harness与信任模型之争"]
relates_to:
  - target: "[[Harness-Engineering]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Anthropic]]"
    type: relates_to
    confidence: 0.7
  - target: "[[OpenAI]]"
    type: relates_to
    confidence: 0.7
  - target: "[[Claude-Code]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# Build Heavy Harness vs Trust The Model

## 概述
AI Agent工程中的一个重要争议，涉及如何平衡Harness（执行环境）的复杂度与对模型能力的信任度。

## 关键内容

1. **Build Heavy Harness 阵营**：
   - 认为需要构建复杂的Harness来约束和引导AI Agent
   - 证据包括：[[OpenAI]]的百万行代码实验、[[Stripe]]的Minions Agent、LangChain和[[SWE-agent]]的数据
   - 强调确定性分析工具与LLM结合的重要性（IBM Research数据显示：纯LLM[[代码审查]]仅捕获45%错误，结合确定性工具后跃升至94%）
   - 通过Terminal Bench 2.0成绩从52.8%升至66.5%的案例证明Harness优化效果

2. **Trust The Model 阵营**：
   - 认为应采用"模型之上尽可能薄的包装层"的设计哲学
   - 以[[Anthropic]]的[[Claude Code]]团队为代表
   - 认为模型能力才是核心，Harness越轻越好
   - 认为较弱模型的复杂脚手架会被更强模型替代
   - METR研究发现基础脚手架与专门构建系统表现相当

3. **争议焦点**：
   - [[OpenAI]]研究员Noam Brown认为复杂脚手架会被更强模型替代
   - [[Martin Fowler]]质疑[[OpenAI]]文章缺乏对行为正确性的验证
   - 对遗留代码库改造代价的担忧

4. **综合观点**：
   - 模型确实在变强，一些过去需要精心构造的prompt现在可直接完成
   - 但Harness不会因此消失，如同编译器增强并未淘汰CI/CD
   - 架构规范和测试不会因Agent能力强而可以删除
   - 最优Harness厚度可能取决于项目规模和生命周期

5. **未来发展**：
   - 模型进化速度是否会快到让精心构建的Harness来不及发挥价值就过时
   - Harness形态会随模型能力变化而演化，但底层逻辑（自动化验证和约束）不变

## 来源
- [[Harness Engineering的本质是什么？ - riba2534 的回答]] — 关于两种理念争议的详细分析

## 相关
- [[Harness-Engineering]] — relates_to
- [[OpenAI]] — relates_to
- [[Anthropic]] — relates_to
- [[Claude-Code]] — relates_to
- [[Harness分层架构]] — relates_to
- [[AI-Agent-Architecture]] — relates_to