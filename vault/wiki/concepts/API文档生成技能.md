---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [技能, 文档生成, API, "Claude Code", 文档处理]
aliases: ["API Documentation Generator Skill", "api-documentation-generator", "API Doc Generator Skill"]
relates_to: []
supersedes: null
---

# API文档生成技能

## 概述
API文档生成[[Skills|技能]]是[[Claude Code]]的一个自动化[[Skills|技能]]，用于从源[[代码生成]]全面且准确的API文档。适用于创建或更新API文档、生成[[OpenAPI]]规范，或在用户提到API文档、端点或说明时使用。

## 关键内容
1. **可生成内容**：
   - [[OpenAPI]] / [[Swagger]] 规范
   - API 端点文档
   - SDK 使用示例
   - 集成指南
   - 错误码参考
   - 认证指南

2. **文档结构**：
   - 每个端点应包含描述、参数表格、响应格式
   - 提供详细的错误响应示例
   - 包含多种语言的调用示例（cURL、JavaScript、[[Python]]等）
   - 参数表格包含名称、类型、是否必填、说明等信息

3. **使用场景**：
   - 生成API端点的完整文档
   - 创建SDK使用示例
   - 生成[[OpenAPI]]/[[Swagger]]规范文件
   - 提供多种编程语言的调用示例
   - 包含认证和[[错误处理]]指南

## 来源
- [[raw/assets/claude-howto/03-skills/doc-generator/SKILL.md]] — API文档生成技能的原始定义

## 相关
- [[API文档生成器]] — 相关的API文档生成工具
- [[Skills]] — Claude Code技能系统
- [[API]] — 应用程序接口
- [[OpenAPI]] — API规范格式
- [[Swagger]] — API文档工具
- [[MCP Prompts]] — 相关提示技术

## relates_to
relates_to:
  - target: "[[API文档生成器]]"
    type: implements
    confidence: 0.9
  - target: "[[Skills]]"
    type: part_of
    confidence: 0.9
  - target: "[[API]]"
    type: documents
    confidence: 0.95
  - target: "[[OpenAPI]]"
    type: generates
    confidence: 0.85
  - target: "[[Swagger]]"
    type: generates
    confidence: 0.85
  - target: "[[MCP Prompts]]"
    type: uses
    confidence: 0.7