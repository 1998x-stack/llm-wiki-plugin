---
type: entity
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [图形库, 矢量图形, 2D渲染, NanoVG, 游戏引擎]
aliases: [NanoVG矢量图形, nanovg]
relates_to: [UrhoX引擎, PBR材质系统]
supersedes: null
entity_type: tool
---

# NanoVG

## 概述
NanoVG 是小型 2D 矢量图形 C 库，[[UrhoX引擎|UrhoX]] 引擎完整集成，用于自定义图形绘制（粒子、图表、特效），不是通用 UI 方案。

## 关键内容
1. **渲染事件**：必须在 `NanoVGRender` 事件回调中调用 `nvgBeginFrame`/`nvgEndFrame`，不能在普通 Update 事件中绘制。
2. **字体创建**：`nvgCreateFont` 仅在 `Start()` 初始化时调用一次（多次调用会导致显存泄漏），句柄可复用；引擎内置 Emoji Fallback 机制，无需指定 Emoji 字体。
3. **适用场景**：自定义矢量图形、粒子、图表、特殊视觉效果、Canvas 自由绘制、纯 NanoVG 2D 游戏；UI/HUD/字幕/菜单应使用 `urhox-libs/UI` 组件，避免层级冲突。
4. **分辨率模式**：包含 raw NanoVG 调用的项目必须先确定分辨率模式（设计分辨率模式A / 系统逻辑分辨率模式B），通过 `GetWidth()/GetHeight()/GetDPR()` 获取屏幕参数。
5. **C API 对齐**：[[UrhoX引擎|UrhoX]] 中 NanoVG 函数签名与上游 C API 完全相同，可参考官方文档。

## 来源
- [[raw/articles/personal/ai-dev-kit/CLAUDE]] — UrhoX 开发指南中 NanoVG 使用规则（规则 #6、#7、#8）
- [[raw/articles/personal/ai-dev-kit/README]] — UrhoX AI Dev Kit 项目说明（NanoVG 作为 Canvas 替代方案核心特性）

## 相关
- [[UrhoX引擎]] — part_of
