---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [api设计, 后端开发, 规范, 工具与框架]
aliases: ["API Module Specification", "API Specification"]
relates_to:
  - target: "[[Zod]]"
    type: uses
  - target: "[[JWT]]"
    type: uses
  - target: "[[Redis]]"
    type: uses
  - target: "[[请求校验]]"
    type: extends
  - target: "[[认证机制]]"
    type: extends
  - target: "[[分页]]"
    type: extends
supersedes: null
---

# API模块规范

## 概述
API模块规范是用于定义API接口开发标准的规范性文档，涵盖了请求校验、认证、响应格式、分页和限流等关键方面。

## 关键内容

1. **请求校验**：
   - 使用[[Zod]]做schema校验
   - 始终校验输入数据
   - 校验失败时返回400状态码
   - 提供字段级别的错误详情

2. **认证**：
   - 所有端点都需要[[JWT]] token进行认证
   - token放在Authorization header中传输
   - token有效期为24小时后过期
   - 实现refresh token机制以延长会话

3. **响应格式**：
   - 成功响应包含success、data、timestamp和version字段
   - 错误响应包含success(false)、error对象和timestamp
   - 统一的JSON格式确保客户端处理的一致性

4. **分页与限流**：
   - 使用基于cursor的分页而非offset分页
   - 单页最大数量限制为100，默认页大小为20
   - 限流机制：已认证用户每小时1000次，公开端点每小时100次

5. **缓存策略**：
   - 使用[[Redis]]做会话缓存
   - 默认缓存时长为5分钟
   - [[Write|写操作]]时失效缓存以保证数据一致性

## 来源
- [[directory-api-CLAUDE]] — API模块规范

## 相关
- [[Zod]] — uses
- [[JWT]] — uses
- [[Redis]] — uses
- [[请求校验]] — extends
- [[认证机制]] — extends
- [[分页]] — extends