---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, claude-skills, frontend, react, engineering, 工具与框架]
aliases: [web-artifacts-builder, web-artifacts-builder skill]
entity_type: tool
relates_to:
  - target: "[[Agent Skills]]"
    type: implements
  - target: "[[frontend-design Skill]]"
    type: complements
  - target: "[[shadcn/ui]]"
    type: uses
  - target: "[[React]]"
    type: uses
supersedes: null
---

# web-artifacts-builder Skill

## 概述
web-artifacts-builder 是一个用于构建复杂前端 artifacts 的 [[Claude_Code|Claude]] [[Skills|Skill]]，专门处理需要状态管理、路由和 shadcn/ui 组件的复杂 [[React]] 应用，与专注于设计哲学的 [[frontend-design Skill]] 形成互补关系。

## 关键内容

1. **核心功能**：
   - 专门用于构建复杂的 [[React]] artifacts，而非简单的单文件 HTML/JSX
   - 支持状态管理、路由和 shadcn/ui 组件
   - 将多组件 [[React]] 应用打包成单个可分享的 HTML 文件

2. **技术栈**：
   - [[React]] 18 + [[TypeScript]] + Vite 开发环境
   - Parcel + html-inline 打包成单文件 HTML
   - [[Tailwind CSS]] 3.4.1 样式框架
   - 预[[Configuration|配置]] 40+ shadcn/ui 组件及 Radix UI 基础依赖
   - 支持路径别名 `@/` [[Configuration|配置]]

3. **工作流程**：
   - 初始化项目：使用 `bash scripts/init-artifact.sh <project-name>`
   - 开发 artifact：编写业务代码，利用预[[Configuration|配置]]的工具链
   - 打包：运行 `bash scripts/bundle-artifact.sh` 生成单个 HTML 文件
   - 分享：通过 `present_files` 工具展示给用户

## 来源
- [[web-artifacts-builder Skill 深度解析]] — 深度调查文档

## 相关
- [[Agent Skills]] — Claude 的各种技能工具
- [[Claude Connectors]] — Claude 连接外部工具的方式
- [[frontend-design Skill]] — 互补的设计哲学技能