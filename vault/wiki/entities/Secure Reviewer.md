---
type: tool
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [security, "code review", subagent, claude, AI工程]
aliases: ["安全审查专家", "Security Review Agent", "Secure Reviewer Agent"]
relates_to: []
supersedes: null
---

# Secure Reviewer

## 概述
一个专门的[[安全分析|安全审查]]子代理，专注于识别代码中的漏洞，采用最小[[Permissions|权限]]设计以确保审计过程的安全性。

## 关键内容

1. **设计原则**：
   - 采用最小[[权限模型]]，只允许读取和搜索操作
   - 无法执行代码、修改文件或运行测试
   - 确保审查过程不会意外破坏任何系统组件

2. **功能特性**：
   - 能够读取文件进行[[安全分析]]
   - 支持模式搜索识别潜在漏洞
   - 遵循OWASP标准进行漏洞分类
   - 提供结构化的安全报告输出

3. **[[安全分析|安全审查]]范围**：
   - **身份验证问题**：弱密码策略、缺失的多因素认证、会话管理缺陷
   - **授权问题**：访问控制失效、[[Permissions|权限]]提升、缺失的角色检查
   - **数据暴露**：敏感数据在日志中的泄露、未加密存储、API密钥暴露
   - **注入漏洞**：SQL注入、命令注入、XSS（跨站脚本）、LDAP注入

## 来源
- [[secure-reviewer]] — 子代理配置定义

## 相关
- [[Secure Code Reviewer]] — relates_to
- [[Subagent]] — implements
- [[安全分析]] — relates_to