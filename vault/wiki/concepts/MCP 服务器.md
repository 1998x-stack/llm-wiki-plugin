---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [MCP, 服务器, 工具集成, "Claude Code", AI工程]
aliases: ["MCP Server", "MCP 服务器"]
relates_to:
  - target: "[[MCP（Model Context Protocol）]]"
    type: implements
  - target: "[[外部工具集成]]"
    type: enables
  - target: "[[Claude Code]]"
    type: connects_to
supersedes: null
---

# MCP 服务器

## 概述
MCP [[服务]]器是实现 [[Model Context Protocol]] 的[[ROS (Robot Operating System)|中间件]][[服务]]，作为 [[Claude Code]] 与外部工具或数据源之间的桥梁，处理工具调用并将结果返回给 [[Claude_Code|Claude]]。

## 关键内容

1. **架构角色**：
   - 位于 [[Claude Code]] 和外部工具/数据源之间
   - 接收来自 [[Claude_Code|Claude]] 的工具调用请求
   - 将请求转发给对应的外部系统
   - 处理并格式化返回结果

2. **功能特性**：
   - 工具注册：支持动态注册可用工具
   - 请求路由：将工具调用准确路由到相应功能
   - 结果封装：将外部系统响应格式化为 MCP 标准格式
   - [[错误处理]]：统一处理异常情况

3. **[[Configuration|配置]]方式**：
   - 支持项目级和用户级[[Configuration|配置]]
   - 可通过[[Environment Variables|环境变量]]管理认证信息
   - 支持多种传输协议（HTTP、Stdio 等）
   - [[Configuration|配置]]可版本化管理

4. **安全管理**：
   - 通过最小[[Permissions|权限]]原则限制工具访问
   - 支持 [[OAuth 2.0 认证|OAuth 2.0]] 等认证方式
   - 可控制哪些工具对 [[Claude_Code|Claude]] 可用

5. **部署类型**：
   - 本地[[服务]]器：运行在开发者本地环境
   - 远程[[服务]]器：部署在独立[[服务]]器上
   - 云端[[服务]]：托管在云平台的 MCP [[服务]]

6. **管理命令**：
   - 添加/删除 MCP [[服务]]器
   - 列出已[[Configuration|配置]]的[[服务]]器
   - 获取[[服务]]器详细信息
   - 重置批准选择

## 来源
- [[claude-howto MCP 文档]] — 服务器概念说明

## 相关
- [[MCP（Model Context Protocol）]] — implements
- [[外部工具集成]] — enables
- [[Claude Code]] — connects_to
- [[MCP 传输方式]] — relates_to
- [[外部工具集成]] — relates_to
- [[GitHub 集成]] — relates_to