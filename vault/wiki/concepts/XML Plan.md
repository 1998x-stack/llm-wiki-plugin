---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: [gsd, workflow, planning, xml]
aliases: ["XML Plan", "PLAN.md", "GSD Plan"]
relates_to:
  - target: "[[GSD]]"
    type: part_of
  - target: "[[GSD Commands]]"
    type: uses
---

# XML Plan

## 概述
GSD 系统的结构化执行计划格式，使用 XML 标签定义任务，每个标签有明确职责，形成机器可读、人类可理解的原子执行单元。

## 关键内容

1. **XML 结构**：
   ```xml
   <task type="auto">
     <n>创建用户登录 API 端点</n>
     <files>src/app/api/auth/login/route.ts</files>
     <action>
       使用 jose 处理 JWT（禁用 jsonwebtoken）。
       从 users 表验证凭证，密码用 bcrypt 比对。
       成功后设置 httpOnly cookie，不在响应体中返回 token。
       失败统一返回 401，不透露具体原因。
     </action>
     <verify>
       curl -X POST localhost:3000/api/auth/login \
         -d '{"email":"t@t.com","password":"correct"}' | grep -E "200|Set-Cookie"
     </verify>
     <done>有效凭证返回 200 + Set-Cookie；无效凭证返回 401</done>
   </task>
   ```

2. **标签职责**：
   - `<n>`：任务名称（也是 git commit 名称）
   - `<files>`：涉及文件路径（消除猜测）
   - `<action>`：具体执行指令
   - `<verify>`：验证命令（Claude 会真正运行）
   - `<done>`：完成判断标准
   - `<depends_on>`：依赖关系（用于 DAG 分析）

3. **原子性原则**：
   - 每个 PLAN 文件包含 2-3 个任务
   - 可在干净 200k 上下文窗口内完成
   - 超过 150 个文件操作应拆分

4. **文件命名**：
   - `{phase}-{plan}-PLAN.md`
   - 例：`02-01-PLAN.md`（第 2 阶段第 1 个计划）

5. **验证维度**（plan-checker）：
   - 需求覆盖检查
   - 依赖合理性
   - 验证命令可执行性
   - 完成标准清晰度

## 来源
- [[01-overview-context-rot]] — Context Rot 与上下文工程
- [[03-core-workflow]] — 核心工作流

## 相关
- [[GSD]] — part_of
- [[GSD Commands]] — uses
- [[GSD Planning Directory]] — part_of
