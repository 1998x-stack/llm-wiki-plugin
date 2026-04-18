---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: [安全架构, 设计模式, Agent系统]
aliases: ["Policy-First Design", "策略优先设计"]
relates_to:
  - target: "[[Codex CLI]]"
    type: implements
    confidence: 0.95
  - target: "[[ExecPolicy]]"
    type: implements
    confidence: 0.95
  - target: "[[三道防线模式]]"
    type: extends
    confidence: 0.9
supersedes: null
---

# Policy-First 设计

一种安全架构设计哲学：**先声明策略，再执行**，而非"先执行再道歉"（act now, apologize later）。

## 关键内容

1. **核心流程**：
   ```
   [用户配置] approval_policy + sandbox_mode
            ↓
   [ExecPolicy] 每条命令过策略引擎
            ↓
   [Sandbox]  OS 内核强制执行
   ```

2. **两层独立但协同**：
   - **策略层** = "意图"：定义哪些操作被允许、需要审批、被禁止
   - **沙箱层** = "执行边界"：OS 内核强制限制实际能做什么
   - 即使策略层有漏洞，沙箱层兜底

3. **与硬编码的对比**：
   - 传统做法：安全逻辑硬编码在业务代码中（脆弱、难共享）
   - Policy-First：[[ExecPolicy|策略即代码]]（[[ExecPolicy|Policy as Code]]），可版本化、可测试、可团队共享

4. **在 [[Codex CLI]] 中的体现**：
   - [[ExecPolicy]] 作为独立的策略引擎 crate
   - 配置分层：Global → Team → Project → Profile
   - 策略规则以 TOML 文件定义，支持 Git 版本控制

## 工程智慧

> "把 AI 的不确定性关进[[操作系统]]的笼子里，用策略而非硬编码来定义笼子的大小。"

## 来源

- [[raw/articles/ai-tools/codex/01_codex_architecture_overview.md]] — 第 4.2 节 Policy-First 设计
- [[raw/articles/ai-tools/codex/04_codex_execpolicy.md]] — ExecPolicy 规则语法、前缀树匹配、规则层次

## 相关

- [[Codex CLI]] — 采用 Policy-First 设计的编码 Agent
- [[ExecPolicy]] — Policy-First 设计的具体实现
- [[三道防线模式]] — Policy-First 设计在防御架构中的具体化
