---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [development-tools, javascript, debugging, AI工程]
aliases: ["Source Map", ".map file", "JavaScript Source Map"]
relates_to: 
  - target: "[[TypeScript]]"
    type: used_with
    confidence: 0.9
  - target: "[[Webpack]]"
    type: generated_by
    confidence: 0.8
  - target: "[[esbuild]]"
    type: generated_by
    confidence: 0.8
  - target: "[[Bun]]"
    type: generated_by
    confidence: 0.8
  - target: "[[Source Map 泄露事件]]"
    type: security_impact
    confidence: 0.9
supersedes: null
---

# Source Map

## 概述
Source Map 是一种开发工具技术，用于将压缩、编译或转换后的代码映射回原始源代码，便于调试时定位错误。

## 关键内容

1. **技术原理**：
   - 当使用 [[TypeScript]] 编写代码并通过 Bun/Webpack/esbuild 等工具打包为生产环境的压缩 JS 时，构建工具会生成 .map 文件
   - 作用是将压缩后难以阅读的代码映射回原始源码，方便调试时查看真正的报错位置
   - 内部结构包含 version、sources（源文件路径）、sourcesContent（源文件内容）和 mappings（位置映射）字段

2. **安全风险**：
   - sourcesContent 字段存储了所有原始文件的完整内容，包括注释、内部常量、系统提示词
   - 如果错误地将包含完整源码的 .map 文件部署到生产环境，可能导致源码泄露
   - [[Source Map 泄露事件]]就是此类安全问题的典型案例

3. **[[Configuration|配置]]要点**：
   - 生产环境中通常应禁用 Source Map 生成
   - 需要在 .npmignore 或类似[[Configuration|配置]]文件中排除 *.map 文件
   - 构建[[Configuration|配置]]中应明确关闭 source map 生成（如 Bun 打包器）

## 来源
- [[01_overview_architecture]] — 技术原理说明

## 相关
- [[TypeScript]] — used_with
- [[Webpack]] — generates
- [[esbuild]] — generates
- [[Bun]] — generates
- [[Source Map 泄露事件]] — security_impact