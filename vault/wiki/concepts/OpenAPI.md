---
type: concept
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [API, 文档规范, 开放标准, AI工程]
aliases: ["OpenAPI Specification", "OpenAPI Specification", "Swagger", "OAS"]
relates_to: []
supersedes: null
---

# OpenAPI

## 概述
OpenAPI是一个开放标准，用于描述RESTful API。它提供了一种与语言无关的方式来描述API，使开发人员和[[计算]]机都能够发现和理解[[服务]]的功能，而无需访问源代码或网络流量检查。

## 关键内容
1. **规范定义**：
   - OpenAPI规范（OAS）定义了描述API的格式
   - 支持JSON和YAML两种格式
   - 包括路径、操作、参数、请求体、响应等API元素的描述
   - 支持安全定义、[[服务]]器信息、标签等功能

2. **主要用途**：
   - 自动生成API文档
   - 生成客户端SDK代码
   - API测试和验证
   - 促进API设计的标准化

3. **版本演进**：
   - OpenAPI 3.0引入了许多重要改进
   - 支持回调和链接功能
   - 改进了组件重用机制
   - 增强了安全性定义

## 来源
- [[API文档生成器]] — 使用OpenAPI作为输出格式之一

## 相关
- [[API]] — 应用程序接口
- [[Swagger]] — OpenAPI的前身及工具生态系统
- [[API文档生成器]] — 可以生成OpenAPI规范
- [[RESTful]] — API设计风格
- [[JSON Schema]] — 数据模式定义

## relates_to
relates_to:
  - target: "[[API]]"
    type: defines
    confidence: 0.9
  - target: "[[Swagger]]"
    type: successor_to
    confidence: 0.85
  - target: "[[API文档生成器]]"
    type: generated_by
    confidence: 0.8
  - target: "[[JSON Schema]]"
    type: incorporates
    confidence: 0.8