---
type: concept
status: active
confidence: 0.95
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 研究
- 计算理论
aliases:
- HTTP
- HyperText Transfer Protocol
- 超文本传输协议
relates_to:
- target: "[[万维网]]"
  type: implements
  confidence: 0.99
  note: 万维网的核心组件
- target: "[[Tim Berners-Lee]]"
  type: caused_by
  confidence: 0.99
  note: 发明者
- target: "[[URL]]"
  type: related_to
  confidence: 0.9
  note: HTTP 请求的目标
- target: "[[TCP-IP]]"
  type: depends_on
  confidence: 0.9
  note: 运行在 TCP/IP 之上
- target: "[[MCP（Model Context Protocol）]]"
  type: uses
  confidence: 0.8
  note: MCP 支持 HTTP 作为传输方式
supersedes: null
---

# HTTP

## 概述

HTTP（[[超文本传输协议]]）定义了 Web 客户端和[[服务]]器之间的通信规则，初始版本只有一个 GET 命令，是极简主义的典范。

## 关键内容

### HTTP/0.9

- 只有一个命令：`GET`
- 客户端发送 URL，[[服务]]器返回文档
- 没有认证、加密、缓存控制

### 设计哲学

- 极致的简单性：任何人都可以在几小时内实现 HTTP [[服务]]器
- 请求-响应模型：一问一答，无需复杂手续

### 后续发展

- **HTTP/1.0**：增加了 POST 方法、状态码、头字段
- **HTTP/1.1**：持久连接、管道化
- **HTTP/2**：多路复用、头部压缩
- **HTTP/3**：基于 QUIC 协议

## 来源

- [[raw/books/计算机科学/17-berners-lee-www.md]]

## 相关

- [[万维网]] — 核心组件
- [[Tim Berners-Lee]] — 发明者
- [[URL]] — 请求目标
- [[TCP-IP]] — 运行基础
- [[MCP（Model Context Protocol）]] — uses
