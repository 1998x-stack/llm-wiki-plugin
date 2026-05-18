---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [gsd, xml, prompt-engineering, structured-prompt, 机器学习]
aliases: [XML Plan, XML 结构化 Prompt, XML Plan System, XML 结构化计划]
relates_to:
  - target: "[[GSD]]"
    type: part_of
  - target: "[[Prompt Engineering]]"
    type: extends
supersedes: null
---

# XML 结构化 Prompt

## 概述
XML 结构化 Prompt 是 GSD 系统中使用的结构化任务定义格式，采用 XML 标签而非自然语言段落来描述任务，确保每个标签有明确职责，提高 [[Claude_Code|Claude]] 处理任务的准确性。

## 关键内容

1. **基本结构**：
   ```xml
   <task type="auto">
     <n>创建用户登录 API 端点</n>
     <files>src/app/api/auth/login/route.ts</files>
     <action>
       使用 jose 处理 JWT（禁用 jsonwebtoken——CommonJS 兼容问题）。
       从 users 表验证凭证，密码用 bcrypt 比对。
       成功后设置 httpOnly cookie，不在响应体中返回 token。
       失败统一返回 401，不透露具体原因（防枚举攻击）。
     </action>
     <verify>
       curl -X POST localhost:3000/api/auth/login \
         -d '{"email":"t@t.com","password":"correct"}' | grep -E "200|Set-Cookie"
     </verify>
     <done>有效凭证返回 200 + Set-Cookie；无效凭证返回 401</done>
   </task>
   ```

2. **标签职责**：
   - `<n>`：任务名称，同时也是 git commit 名称
   - `<files>`：指定操作的文件路径，消除路径猜测
   - `<action>`：具体执行的操作说明
   - `<verify>`：Claude 会真正运行的验证命令
   - `<done>`：任务完成的语义判断标准

3. **核心优势**：
   - 每个标签有明确职责，避免歧义
   - 结构化格式便于解析和处理
   - 验证命令确保任务完成质量
   - 与 git 提交集成，便于追踪

4. **设计理念**：
   - 从自然语言段落转向结构化 XML 格式
   - 提供精确的执行指引，减少误解
   - 与版本控制系统紧密结合

## 来源
- [[GSD 深度解析 · 第一篇：Context Rot 与上下文工程]] — 原文介绍

## 相关
- [[GSD]] — part_of
- [[Prompt Engineering]] — extension
- [[波次并行执行]] — related_to