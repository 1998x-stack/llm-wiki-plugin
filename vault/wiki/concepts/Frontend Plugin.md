---
type: concept
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [frontend, plugin, react, component-library, AI工程]
aliases: ["Frontend Plugin", "jezweb Frontend Plugin"]
relates_to:
  - target: "[[jezweb/claude-skills]]"
    type: part_of
  - target: "[[Tailwind CSS v4]]"
    type: uses
  - target: "[[shadcn/ui]]"
    type: uses
  - target: "[[React]]"
    type: uses
  - target: "[[Design Review]]"
    type: includes
  - target: "[[Tailwind CSS v4]]"
    type: uses
  - target: "[[React 19]]"
    type: uses
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# Frontend Plugin

## 概述
[[jezweb-claude-skills|jezweb/claude-skills]] 项目中的前端插件集合，包含 10 个专门针对前端开发的[[Skills|技能]]，涵盖从主题[[Configuration|配置]]到完整页面生成的完整工作流。

## 关键内容
1. **核心组成**：包含 tailwind-theme-builder、shadcn-ui、react-patterns、design-review、landing-page、product-showcase、react-native、design-loop、design-system、walkthrough-video 等 10 个核心[[Skills|技能]]，形成了完整的前端开发工具链。

2. **依赖关系**：[[Skills]] 之间有明确的依赖顺序，如 tailwind-theme-builder 为基础，shadcn-ui 基于主题[[Configuration|配置]]，react-patterns 提供组件设计模式。这种依赖链确保了工作流程的一致性。

3. **落地页生成**：提供 landing-page 和 product-showcase 等高阶[[Skills|技能]]，可根据描述直接生成完整的页面，采用输出驱动的设计方式。

4. **质量保证**：通过 design-review [[Skills|技能]]提供系统性的设计质量检查，按优先级输出改进建议，覆盖对比度、可访问性等关键指标，分为Critical、High、Medium三个级别。

5. **错误预防**：特别关注前端开发中的常见陷阱，如 [[Tailwind CSS v4|Tailwind v4]] 的[[Configuration|配置]]变更（移除tailwind.config.ts，在CSS中[[Configuration|配置]]）、CSS变量需加hsl()包装、tw-animate-css缺失等8个documented errors。

6. **架构模式**：实现了[[Tailwind CSS v4|Tailwind v4]]的强制四步架构模式（导入基础→定义CSS变量→映射到utility类→应用基础样式），确保主题[[Configuration|配置]]的一致性。

7. **安装方式**：通过 `/plugin marketplace add jezweb/claude-skills` 和 `/plugin install frontend@jezweb-skills` 命令安装。

## 来源
- [[04_jezweb_claude_skills_frontend]] — Frontend Plugin 完整结构解析

## 相关
- [[jezweb/claude-skills]] — 所属项目
- [[Tailwind CSS v4]] — 使用的技术
- [[shadcn/ui]] — 使用的组件库
- [[React]] — 使用的框架