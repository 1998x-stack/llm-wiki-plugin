---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-20
last_accessed: 2026-04-16
source_count: 2
tags: [NanoVG, 分辨率, DPI, UrhoX, 渲染, 游戏开发]
aliases: [nvg分辨率模式, NanoVG分辨率适配, nvgBeginFrame分辨率]
relates_to: [设备像素比, PBR材质系统, UrhoX材质库]
supersedes: null
---
# NanoVG分辨率模式

## 概述
[[UrhoX引擎|UrhoX]] 引擎中 raw [[NanoVG]] 渲染的三种分辨率适配模式（A/B/C），决定 nvgBeginFrame 参数[[Configuration|配置]]与坐标系语义，需在调用 nvgBeginFrame 前选定，否则高 DPI 屏幕出现 UI 过小或模糊问题。

## 关键内容
1. **模式选择原则**：明确设计分辨率 → 模式A；未明确（默认）→ 模式B；模式C（物理像素）不推荐，仅用户强制要求时使用。三种模式为递进叠加关系：C（无缩放）→ B（+DPR）→ A（+设计缩放）。
2. **模式B（系统逻辑分辨率，默认）**：`nvgBeginFrame(vg, logicalW, logicalH, dpr)`，坐标单位为逻辑像素，输入坐标需除以 DPR。适合应用/工具向及快速原型，必须使用响应式布局。
3. **模式A（设计分辨率，进阶）**：在模式B基础上加 `nvgScale(vg, scale, scale)`，scale = `math.min(logicalW/designW, logicalH/designH)`（CONTAIN策略）。支持绝对布局（设计坐标系）与响应式（屏幕坐标系）混合，DPR 在[[计算]]中被约掉，本质是设计坐标到物理像素的直接映射。

## 来源
- [[raw/articles/personal/ai-dev-kit/.claude/skills/nvg-resolution-mode/SKILL.md]] — NanoVG 分辨率模式编写范式，UrhoX Lua AI 开发指南
- [[raw/articles/personal/ai-dev-kit/CLAUDE.md]] — UrhoX Lua AI 开发指南，规则 #0.8（分辨率模式选择表）

## 相关
- [[设备像素比]] — relates_to，DPR 是三种模式的核心变量
- [[等距柱状投影]] — relates_to
- [[UrhoX材质库]] — relates_to
