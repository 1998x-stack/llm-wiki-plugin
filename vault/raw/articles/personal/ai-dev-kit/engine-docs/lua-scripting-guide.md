# UrhoX Lua 5.4 开发指南 - 补充文档

参考: [Lua 5.4 手册](https://www.lua.org/manual/5.4/)
---

## 📖 本文档内容

| 章节 | 说明 |
|------|------|
| eventData 访问详解 | tolua++ 绑定的详细示例 |
| NanoVG API 映射 | C API 与 Lua API 对照 |
| Box2D 脚底传感器 | 2D 平台跳跃常见问题 |
| 命名规范 | 代码风格指南 |
| 脚本组件模板 | 标准组件结构 |
| 常见错误信息 | 错误速查表 |
| Unicode 转义语法 | AI 生成代码高频错误 |

---

## ✅ eventData 访问方式详解

> CLAUDE.md 规则 #3 的补充说明

**正确格式**：`eventData["字段名"]:Get类型()`

```lua
-- 各类型的访问示例
function HandleMouseMove(eventType, eventData)
    local x = eventData["X"]:GetInt()
    local y = eventData["Y"]:GetInt()
    local dx = eventData["DX"]:GetFloat()
end

function HandleUpdate(eventType, eventData)
    local dt = eventData["TimeStep"]:GetFloat()
end

function HandleKeyDown(eventType, eventData)
    local key = eventData["Key"]:GetInt()
    local scancode = eventData["Scancode"]:GetInt()
end

function HandleCollision(eventType, eventData)
    local nodeA = eventData["NodeA"]:GetPtr("Node")
    local nodeB = eventData["NodeB"]:GetPtr("Node")
end
```

**⚠️ 常见错误**：
- ❌ `eventData:GetInt("X")` - 方法和参数位置反了
- ❌ `eventData.X` - 不能用点语法
- ❌ `eventData["X"]` - 缺少类型转换

**原理**：`eventData` 是 VariantMap（C++ 对象），通过 tolua++ 绑定到 Lua，必须先索引得到 Variant 对象，再调用类型转换方法。

---

## ✨ NanoVG API 映射规则

> NanoVG Lua API **完全对齐** C API（函数名和参数一致）

```lua
-- C API: nvgBeginPath(vg)
-- Lua API: 完全相同
nvgBeginPath(vg)

-- C API: nvgRect(vg, x, y, w, h)
-- Lua API: 完全相同
nvgRect(vg, 100, 100, 200, 150)

-- C API: nvgFillColor(vg, nvgRGBA(255, 0, 0, 255))
-- Lua API: 完全相同
nvgFillColor(vg, nvgRGBA(255, 0, 0, 255))
nvgFill(vg)
```

**详细文档**：[NanoVG C API](https://github.com/memononen/nanovg)（函数签名完全相同）

---

## ❌ Box2D 脚底传感器不触发碰撞事件

**场景**: 2D 平台跳跃游戏
**症状**: 按空格无法跳跃，地面检测失败，`onGround` 始终为 `false`

**✅ 正确方案：使用 `center` 属性偏移碰撞形状**

```lua
function CreatePlayer()
    playerNode_ = scene_:CreateChild("Player")
    playerNode_:SetPosition2D(0, 2)
    
    -- 创建刚体
    playerBody_ = playerNode_:CreateComponent("RigidBody2D")
    playerBody_.bodyType = BT_DYNAMIC
    playerBody_.fixedRotation = true
    
    -- 碰撞形状 #1: 玩家身体（位于中心）
    local bodyShape = playerNode_:CreateComponent("CollisionCircle2D")
    bodyShape.radius = 0.5
    bodyShape.friction = 0.0
    bodyShape.categoryBits = 2
    
    -- 碰撞形状 #2: 脚底传感器（使用 center 偏移）
    local footSensorShape = playerNode_:CreateComponent("CollisionCircle2D")
    footSensorShape.radius = 0.35
    footSensorShape.center = Vector2(0, -0.45)  -- ✅ 关键：用 center 偏移
    footSensorShape.trigger = true
    footSensorShape.categoryBits = 4
    footSensorShape.maskBits = 1
end
```

**关键要点**:
- ✅ 一个刚体可以有**多个碰撞形状**
- ✅ 使用 `center` 属性调整相对位置（不是子节点！）
- ✅ 碰撞分组 `categoryBits` 和 `maskBits` 用于过滤

**诊断方法**:
1. 在碰撞回调中添加 `print()` 检查事件是否触发
2. 按 Z 键启用物理调试显示
3. 确认传感器使用了 `center` 偏移

**完整示例**: `examples/04-box2d-platformer.lua`

---

## 📋 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 脚本文件 | `PascalCase.lua` | `PlayerController.lua` |
| 函数名 | `PascalCase` | `GetComponent`, `CreateChild` |
| 变量名 | `camelCase` | `playerHealth`, `maxSpeed` |
| 常量 | `UPPER_SNAKE_CASE` | `MAX_PLAYERS` |

---

## 📄 脚本组件模板

```lua
-- PlayerController.lua
-- 标准的 Urho3D Lua 脚本组件结构

function Start()
    -- 初始化
    self.speed = 5.0
    self.health = 100

    -- 缓存组件（避免每帧 GetComponent）
    self.body = self.node:GetComponent("RigidBody2D")
    self.sprite = self.node:GetComponent("AnimatedSprite2D")

    -- 订阅事件
    self:SubscribeToEvent("Update", "HandleUpdate")
end

function Stop()
    -- 清理
    self:UnsubscribeFromAllEvents()
end

function HandleUpdate(eventType, eventData)
    local timeStep = eventData["TimeStep"]:GetFloat()
    -- 游戏逻辑...
end
```

---

## 🔍 常见错误信息速查

| 错误信息 | 可能原因 | 解决方案 |
|---------|---------|---------|
| `Null pointer access` | 对象是 nil | 添加 nil 检查 |
| `Stack index X out of range` | 参数数量/类型错误 | 检查函数签名 |
| `attempt to index a nil value` | 对象未初始化 | 检查对象创建代码 |
| `Component not found` | 组件不存在 | 检查组件类型名称 |
| `Resource not found` | 资源路径错误 | 检查 asset_dirs 配置 |
| `missing '{' near '"\u...'` | Unicode 转义语法错误 | `\uXXXX` → `\u{XXXX}`，见下方说明 |

---

## ⚠️ Unicode 转义语法（AI 生成代码高频错误）

**错误信息**：`missing '{' near '"\u2'`

**原因**：Lua 5.4 的 Unicode 转义语法是 `\u{XXXX}`（花括号），**不是** JavaScript/JSON 风格的 `\uXXXX`。AI（LLM）生成代码时经常混淆这两种语法。

```lua
-- ❌ 错误：JavaScript/JSON 风格（Lua 不支持）
local star = "\u2605"
local heart = "\u2764"

-- ✅ 正确：Lua 5.4 花括号语法
local star = "\u{2605}"
local heart = "\u{2764}"

-- ✅ 也可以直接写 UTF-8 字符（文件须为 UTF-8 编码）
local star = "★"
local heart = "❤"
```

**建议**：遇到 Unicode 字符，优先直接写字符本身（如 `"★"`），避免转义语法问题。

---

## 📖 参考资料

1. **Urho3D Lua API**: https://urho3d.github.io/documentation/HEAD/_lua_scripting.html
2. **NanoVG C API**: https://github.com/memononen/nanovg
3. **Lua 5.4 手册**: https://www.lua.org/manual/5.4/

---

*最后更新: 2026-02-09*
