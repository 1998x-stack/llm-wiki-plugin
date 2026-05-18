---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [API, 文档工具, 开放标准, 工具与框架]
aliases: ["Swagger Framework", "Swagger Tools", "Swagger UI", "Swagger Editor"]
relates_to: []
supersedes: null
---

# Swagger

## 概述
Swagger是一套开源工具，用于设计、构建、文档化和使用RESTful Web[[服务]]。Swagger现在是[[OpenAPI]] Initiative的一部分，其规范已演进为[[OpenAPI]]规范。

## 关键内容
1. **工具集组成**：
   - Swagger UI：API文档可视化界面
   - Swagger Editor：在线编辑器，用于编写[[OpenAPI]]规范
   - Swagger Codegen：根据[[OpenAPI]]规范生成客户端和[[服务]]端代码
   - Swagger Inspector：API测试和验证工具

2. **主要优势**：
   - 提供交互式API文档
   - 支持实时API测试
   - 自动生成多种编程语言的客户端SDK
   - 促进API设计的规范化

3. **与[[OpenAPI]]的关系**：
   - Swagger最初创建了Swagger规范
   - 后来贡献给[[OpenAPI]] Initiative并更名为[[OpenAPI]]规范
   - Swagger工具继续支持[[OpenAPI]]规范

## 来源
- [[API文档生成器]] — 可以生成Swagger格式的文档

## 相关
- [[OpenAPI]] — Swagger规范的演进和标准化
- [[API文档生成器]] — 可以生成Swagger格式的文档
- [[API]] — RESTful API
- [[Swagger UI]] — Swagger的可视化工具

## relates_to
relates_to:
  - target: "[[OpenAPI]]"
    type: predecessor_to
    confidence: 0.9
  - target: "[[API文档生成器]]"
    type: generated_by
    confidence: 0.8
  - target: "[[API]]"
    type: documents
    confidence: 0.9