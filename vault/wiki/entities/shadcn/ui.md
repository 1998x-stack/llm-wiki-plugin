---
type: tool
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [frontend, ui-library, react, tailwind, AI设计]
aliases: ["shadcn/ui", "shadcn"]
relates_to:
  - target: "[[React]]"
    type: uses
  - target: "[[Tailwind CSS v4]]"
    type: uses
  - target: "[[web-artifacts-builder Skill]]"
    type: uses
  - target: "[[jezweb/claude-skills]]"
    type: used_by
---

# shadcn/ui

## 概述
基于 Radix UI primitives 和 Tailwind CSS 的 React UI 组件库，以可复用、可定制的方式提供 40+ 组件，被 web-artifacts-builder Skill 完整预配置。

## 关键内容

1. **技术基础**：
   - Radix UI primitives（无障碍基础组件）
   - Tailwind CSS（样式框架）
   - React 18

2. **核心组件**（非完整列表）：
   - Layout: Card, Separator, AspectRatio
   - Forms: Button, Input, Textarea, Checkbox, Radio, Select, Switch, Slider
   - Overlays: Dialog, AlertDialog, Popover, Tooltip, Sheet, HoverCard
   - Navigation: Tabs, Menubar, NavigationMenu, Command
   - Feedback: Alert, Badge, Progress, Skeleton, Toast
   - Data: Table, Calendar, ScrollArea

3. **设计系统**：
   - CSS 变量主题系统（浅色/深色模式）
   - `--background`, `--foreground`, `--primary`, `--secondary`
   - `--accent`, `--destructive`, `--border`, `--input`, `--ring`
   - `--radius` 圆角控制

4. **使用方式**：
   ```tsx
   import { Button } from "@/components/ui/button"
   import { Card, CardContent } from "@/components/ui/card"
   ```

5. **工具函数**：
   ```typescript
   // cn() 合并 Tailwind 类名
   import { cn } from "@/lib/utils"
   cn("bg-red-500", "text-white", isActive && "font-bold")
   ```

## 来源
- [[03_web_artifacts_builder_skill]] — web-artifacts-builder Skill 解析
- [[04_jezweb_claude_skills_frontend]] — jezweb/claude-skills shadcn-ui 详解
- shadcn/ui 官方文档

## 相关
- [[React]] — uses
- [[Tailwind CSS v4]] — uses
- [[Radix UI]] — uses
- [[web-artifacts-builder Skill]] — uses
