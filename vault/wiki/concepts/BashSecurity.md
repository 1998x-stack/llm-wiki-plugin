---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [security, bash, ai-agent, threat-model, cli-tools, AI工程]
aliases: ["BashSecurity", "Bash安全机制", "命令注入防护", "Shell安全"]
relates_to:
  - target: "[[BashTool]]"
    type: implements
  - target: "[[Claude Code]]"
    type: protects
  - target: "[[Security Filter Layer]]"
    type: part_of
  - target: "[[Risk Grading System]]"
    type: part_of
  - target: "[[权限系统]]"
    type: complements
  - target: "[[客户端证明]]"
    type: part_of
  - target: "[[Killswitch]]"
    type: part_of
  - target: "[[遥测监控]]"
    type: part_of
supersedes: null
---

# BashSecurity

## 概述
BashSecurity是[[Claude Code]]中的一套综合安全机制，专门针对Bash工具执行时可能出现的各种安全威胁进行防范，包括命令注入、[[Permissions|权限]]提升、恶意脚本执行等。

## 关键内容
1. **多层防护体系**：
   - 第一层：BashSecurity（23项检查，专门Zsh威胁模型）
   - 第二层：[[权限模型]]（每次询问 → 本次允许 → 永久允许）
   - 第三层：用户确认UI（可视化风险）
   - 第四层：[[客户端证明]]（API层认证）
   - 第五层：Killswitch（远程熔断）
   - 第六层：遥测监控（发现异常模式）

2. **23项安全检查**：
   - 命令黑名单检查：防止执行危险命令（rm -rf, chmod, su, sudo等）
   - 参数验证：检测潜在的命令注入攻击
   - 路径规范化：防止路径遍历攻击
   - Zsh特有威胁防护：专门针对Zsh shell的独特安全问题
   - Unicode安全检查：防范Unicode欺骗和规范化问题
   - 管道与重定向分析：检测恶意的管道和重定向操作

3. **威胁模型**：
   - 模型生成恶意命令：AI可能生成具有破坏性的命令
   - 命令注入攻击：通过参数或输入注入额外命令
   - [[Permissions|权限]]提升：尝试获取更高[[Permissions|权限]]执行危险操作
   - 恶意脚本执行：执行下载或生成的恶意脚本

4. **[[纵深防御]]策略**：
   - 每一层单独都可能被绕过，但组合在一起，攻击成本极高
   - AI Agent的安全不能依赖单一机制，每个执行环节都需要独立的安全考量
   - 假设前一层已经被攻破的前提下设计下一层防御

## 来源
- [[Claude Code 源码泄露深度解析（八）：工程总结——从 512,000 行代码中提炼的 AI Agent 设计哲学]] — 66-82行
- [[]] — 

## 相关
- [[BashTool]] — implements
- [[Claude Code]] — protects
- [[Security Filter Layer]] — part_of
- [[Risk Grading System]] — part_of
- [[权限系统]] — complements
- [[客户端证明]] — part_of
- [[Killswitch]] — part_of
- [[遥测监控]] — part_of