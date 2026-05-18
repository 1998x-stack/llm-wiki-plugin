---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [security, "code review", "vulnerability assessment", AI工程]
aliases: ["Secure Code Review", "安全代码审查", "Security Reviewer"]
relates_to: []
supersedes: null
---

# Secure Code Reviewer

## 概述
[[Secure Reviewer|安全审查专家]]，采用最小[[Permissions|权限]]设计，专注于识别代码中的安全漏洞而不执行或修改任何代码。

## 关键内容

1. **最小[[Permissions|权限]]设计**：
   - 只读访问[[Permissions|权限]]确保安全审计过程安全可靠
   - 可以读取文件进行分析
   - 可以搜索模式但不能执行代码或修改文件
   - 无法运行测试防止意外破坏

2. **[[安全分析|安全审查]]重点**：
   - **身份验证问题**：弱密码策略、缺少多因素认证、会话管理缺陷
   - **授权问题**：访问控制失效、[[Permissions|权限]]提升、缺少角色检查
   - **数据暴露**：日志中泄露敏感数据、未加密存储、API key 泄露
   - **注入漏洞**：SQL 注入、命令注入、XSS（跨站脚本）、LDAP 注入

3. **[[Configuration|配置]]与工具**：
   - 使用 Read 和 Grep 工具进行文件分析
   - 通过搜索模式识别常见漏洞
   - 提供结构化输出包含严重性、类型、位置、描述和修复建议

## 来源
- [[secure-reviewer]] — 安全审查专家定义

## 相关
- [[代码审查]] — relates_to
- [[安全分析]] — relates_to
- [[漏洞评估]] — extends