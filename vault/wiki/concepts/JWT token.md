---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [api, authentication, jwt, security, AI工程]
aliases: ["JWT token", "JSON Web Token"]
relates_to: []
supersedes: null
---

# JWT token

## 概述
JWT（JSON Web Token）是一种开放标准，用于在网络应用环境间安全地传递声明。在API认证中作为令牌使用。

## 关键内容

1. **用途**：作为API端点的认证方式，所有端点都需要JWT token才能访问
2. **实现方式**：token放在Authorization header中传输
3. **特性**：具有时效性，通常24小时后过期
4. **配套机制**：实现refresh token机制以维持用户会话

## 来源
- [[directory-api-CLAUDE]] — API模块规范

## 相关
- [[API模块规范]] — relates_to
- [[API认证]] — relates_to
- [[Refresh Token]] — relates_to