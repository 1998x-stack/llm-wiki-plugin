---
type: entity
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [validation, schema, javascript, typescript]
aliases: ["Zod", "Zod schema validation"]
relates_to: []
supersedes: null
---

# Zod

## 概述
Zod是一个用于模式验证的JavaScript/[[TypeScript]]库，提供运行时类型检查功能。

## 关键内容

1. **用途**：用于API请求的数据验证，在API开发中确保输入数据符合预期格式
2. **功能**：提供schema校验功能，能够对输入数据进行严格的类型和结构验证
3. **应用场景**：在API模块中用于校验输入参数，验证失败时返回400状态码并提供字段级别的错误详情

## 来源
- [[directory-api-CLAUDE]] — API模块规范

## 相关
- [[API模块规范]] — relates_to
- [[请求校验]] — relates_to