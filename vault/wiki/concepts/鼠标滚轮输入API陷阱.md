---
type: concept
status: active
confidence: high
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [UrhoX, Lua, 输入处理, API陷阱, 鼠标输入, Lua编程]
aliases: [mouseMove.z陷阱, mouseMoveWheel, 滚轮输入]
relates_to: [UrhoX Lua开发准则, UrhoX引擎]
supersedes: null
---
# 鼠标滚轮输入API陷阱

## 概述

在 [[UrhoX引擎|UrhoX]]/[[Urho3D]] Lua 中，`input.mouseMove` 返回 `IntVector2`（仅有 x、y），不含滚轮分量。滚轮值必须通过独立属性 `input.mouseMoveWheel` 获取，使用 `.z` 会得到 `nil` 并引发运算时崩溃。

## 关键内容

### 属性类型对照

| 属性 | 类型 | 说明 |
|------|------|------|
| `input.mouseMove` | `IntVector2` | 鼠标移动量（x、y） |
| `input.mouseMoveX` | `int` | 等同 `mouseMove.x` |
| `input.mouseMoveY` | `int` | 等同 `mouseMove.y` |
| `input.mouseMoveWheel` | `int` | 鼠标滚轮（**不是** `mouseMove.z`） |

### 错误用法

```lua
-- ❌ mouseMove 是 IntVector2，没有 .z，返回 nil
local wheel = input.mouseMove.z
if wheel ~= 0 then  -- 💥 attempt to perform arithmetic on a nil value
    scrollOffset = scrollOffset - wheel * 2
end
```

### 正确用法

```lua
-- ✅ 使用独立属性
local wheel = input.mouseMoveWheel
if wheel ~= 0 then
    scrollOffset = scrollOffset - wheel * 20
    scrollOffset = math.max(0, scrollOffset)
end

-- ✅ 或使用方法调用
local wheel = input:GetMouseMoveWheel()
```

### 为什么容易犯错

1. **命名误导**：`mouseMoveX`、`mouseMoveY`、`mouseMoveWheel` 共享前缀，暗示都是 `mouseMove` 的组件
2. **跨引擎知识迁移**：SDL 旧版本和部分 Web 框架用 3D 向量表示鼠标移动，`.z` 确实是滚轮
3. **文档缺失**：引擎文档原先未在鼠标输入章节提及滚轮用法

### 根因类别

- 知识/经验不足（可通过学习改进）
- 上下文理解错误（跨引擎知识错误迁移）

### 防御性编码建议

- 对可能为 `nil` 的值先检查再运算
- 不确定属性是否存在时，查阅 `engine-docs/api/input.md`
- 避免对 API 属性做"命名模式推断"

## 来源

- [[raw/articles/personal/ai-dev-kit/coding-insights/API-Usage/mouse-wheel-not-on-mousemove.md]] — UrhoX Lua 编程陷阱文档（2026-02-08）

## 相关

- [[UrhoX Lua开发准则]] — relates_to
- [[UrhoX引擎]] — relates_to
