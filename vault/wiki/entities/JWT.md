---
type: tool
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [认证技术, 安全协议, AI工程]
aliases: ["JSON Web Token", "JWT", "JSON Web Tokens"]
relates_to:
  - target: "[[API模块规范]]"
    type: used_by
  - target: "[[认证机制]]"
    type: implements
  - target: "[[OAuth]]"
    type: compares_to
supersedes: null
---

# JWT

## 概述
[[JWT token|JSON Web Token]] (JWT)是一种开放标准(RFC 7519)，用于在网络应用环境间安全地传递声明。JWT是自包含的令牌，允许在各方之间传输信息并验证其完整性。

## 关键内容

1. **结构组成**：
   - Header：包含令牌类型和签名[[算法]]信息
   - Payload：包含声明(Claims)，即实际传输的数据
   - Signature：用于验证消息未被篡改，并在使用私钥签名时确认发送方的身份

2. **使用特点**：
   - 无状态：[[服务]]器不需要存储会话信息
   - 可自我验证：令牌包含必要的验证信息
   - 广泛采用：被大量现代应用和API所使用

3. **应用场景**：
   - 身份认证：用户登录后获取JWT，后续请求携带该令牌
   - 信息交换：在各方之间安全地传输信息
   - API访问控制：作为访问令牌进行[[Permissions|权限]]验证

4. **生命周期**：
   - JWT通常具有过期时间，如API规范中提到的24小时过期机制
   - 需要实现refresh token机制来延长会话

## 来源
- [[directory-api-CLAUDE]] — 在API模块规范中提到使用JWT进行认证

## 相关
- [[API模块规范]] — used_by
- [[认证机制]] — implements
- [[OAuth]] — compares_to