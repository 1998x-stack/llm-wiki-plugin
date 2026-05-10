---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, claude-code, tool-system, sandbox]
aliases: ["Sandbox Mode", "沙箱模式"]
relates_to: []
supersedes: null
---

# Sandbox Mode

## 概述
[[Claude Code]]中的沙箱模式，用于在CI/CD等场景中限制工具执行环境，特别是限制网络访问以增强安全性。

## 关键内容

1. **网络访问控制**：
   - 通过init-firewall.sh脚本限制Bash工具的出站网络访问
   - 只允许白名单域名访问
   - 白名单包括api.anthropic.com、registry.npmjs.org、pypi.org、github.com等

2. **安全效果**：
   - 防止Agent意外访问生产API
   - 防止在CI环境中泄露生产凭证
   - 隔离测试环境与外部[[服务]]

3. **应用场景**：
   - CI/CD流水线中提供额外安全层
   - 在受控环境中测试代码变更
   - 防止意外的数据泄露或外部[[服务]]调用

## 来源
- [[03 · 工具生态系统（Tool Ecosystem）]] — 沙箱模式部分

## 相关
- [[Tool Ecosystem]] — 所属系统
- [[BashTool]] — 主要应用工具
- [[Security Filter Layer]] — 相关安全措施