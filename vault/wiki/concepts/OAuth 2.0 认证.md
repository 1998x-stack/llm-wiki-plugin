---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [authentication, oauth, mcp, security, claude-code, AI工程]
aliases: ["OAuth 2.0", "OAuth Authentication", "MCP OAuth 2.0", "OAuth 2.0 认证协议"]
relates_to:
  - target: "[[MCP]]"
    type: secures
    confidence: 0.85
  - target: "[[HTTP 传输协议]]"
    type: supports
    confidence: 0.8
  - target: "[[安全注意事项]]"
    type: implements
    confidence: 0.9
  - target: "[[认证信息管理]]"
    type: enables
    confidence: 0.85
---
# OAuth 2.0 认证

## 概述
OAuth 2.0 认证协议在 MCP ([[Model Context Protocol]]) 中的应用，为 [[MCP 服务器]]提供标准化的身份验证和授权机制。

## 关键内容
1. **实现方式**：
   - 交互式认证流程：用户在 [[Claude_Code|Claude]] 中完成 OAuth 授权
   - 预[[Configuration|配置]]凭据：通过[[Environment Variables|环境变量]]或[[Configuration|配置]]文件预先[[Settings|设置]]令牌
   - 支持多种 OAuth 2.0 授权类型

2. **安全性**：
   - 令牌安全存储和传输
   - 支持令牌刷新机制
   - 最小[[Permissions|权限]]原则实施

3. **[[Configuration|配置]]方法**：
   ```toml
   [mcp_servers.protected_service]
   endpoint = "https://api.example.com/mcp"
   auth_method = "oauth2"
   auth_header = "Bearer ${ACCESS_TOKEN}"
   ```

4. **与 HTTP 传输结合**：
   - 通常与 [[HTTP 传输协议]]配合使用
   - 支持 bearer token 认证
   - 符合 REST API 安全最佳实践

5. **使用场景**：
   - 需要身份验证的外部[[服务]]（如 [[GitHub]]、数据库）
   - 企业内部受保护的 API
   - 需要用户授权的第三方[[服务]]

## 来源
- [[raw/assets/claude-howto/05-mcp/README.md]] — Claude How To MCP 认证方式介绍

## 相关
- [[MCP]] — secures
- [[HTTP 传输协议]] — supports
- [[安全注意事项]] — implements
- [[认证信息管理]] — enables
- [[环境变量]] — uses