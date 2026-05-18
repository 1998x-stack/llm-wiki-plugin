---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ide-integration, authentication, security, AI工程]
aliases: ["桥接模式", "IDE桥接"]
relates_to: 
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[JWT认证]]"
    type: uses
  - target: "[[零信任架构]]"
    type: implements
supersedes: null
---

# Bridge Mode

## 概述
Bridge Mode是[[Claude Code]]与IDE插件之间的通信桥接机制，使用JWT认证实现安全的进程间通信。

## 关键内容

1. **架构特点**：
   - [[Claude Code]]终端进程作为[[服务]]端
   - IDE扩展（[[VS Code]]插件等）作为客户端
   - 采用松耦合的桥接架构而非紧耦合

2. **安全设计**：
   - 使用JWT（[[JWT token|JSON Web Token]]）进行身份验证
   - 体现[[零信任架构]]思想：即使在同一台机器上也不默认信任
   - 实现安全隔离，防止IDE扩展直接访问[[Claude Code]]内部状态

3. **优势**：
   - IDE无关性：同一后端可连接多种IDE
   - 独立生命周期：[[Claude Code]]进程崩溃不影响IDE
   - 安全隔离：限制IDE扩展对内部状态的访问

## 来源
- [[Claude Code 源码泄露深度解析（四）：多智能体协调器——Coordinator Mode 与 Agent Swarms]] — 原文第175-195行

## 相关
- [[Claude Code]] — relates_to
- [[JWT认证]] — uses
- [[零信任架构]] — implements