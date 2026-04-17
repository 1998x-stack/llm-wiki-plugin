# CollisionShape 尺寸参数使用直径而非半径

**日期**: 2026-01-06
**分类**: API-Usage
**严重程度**: Medium
**游戏/项目**: 通用问题

---

## 🐛 问题现象 (Observed Behavior)

AI 生成的物理碰撞体代码中，`CollisionShape` 的尺寸参数经常被错误地当作**半径**使用，但实际上这些 API 要求的是**直径**。

**预期行为**：碰撞体大小与可视模型匹配  
**实际行为**：碰撞体只有预期大小的一半

---

## 🔍 问题原因 (Root Cause Analysis)

查看 `CollisionShape.pkg` 的 API 定义：

```lua
void SetSphere(float diameter, ...)
void SetCylinder(float diameter, float height, ...)
void SetCapsule(float diameter, float height, ...)
void SetCone(float diameter, float height, ...)
```

**关键点**：所有这些函数的第一个参数都是 `diameter`（直径），而不是 `radius`（半径）。

AI 容易犯错的原因：
1. **命名习惯**：许多图形/物理库使用半径作为参数（如 Unity 的 SphereCollider.radius）
2. **直觉偏差**：程序员在描述圆形/球形时习惯用半径思考
3. **参数名不可见**：调用时只传值 `SetSphere(0.5)`，不容易发现应该是直径

---

## ✅ 解决方案 (Solution)

### 错误做法 (Wrong Approach)
```lua
-- ❌ 错误：把直径参数当半径用，导致碰撞体只有一半大小
local shape = node:CreateComponent("CollisionShape")
local radius = 0.5
shape:SetSphere(radius)  -- 实际创建的是直径0.5的球，半径只有0.25！
```

### 正确做法 (Correct Approach)
```lua
-- ✅ 正确：明确使用直径
local shape = node:CreateComponent("CollisionShape")
local radius = 0.5
local diameter = radius * 2  -- 转换为直径
shape:SetSphere(diameter)    -- 创建半径0.5的球体碰撞体

-- 或者直接使用直径思维
shape:SetSphere(1.0)  -- 直径1.0 = 半径0.5
```

### 各 API 的正确用法速查

| API | 参数说明 | 示例 |
|-----|---------|------|
| `SetSphere(diameter)` | 直径 | `SetSphere(1.0)` = 半径0.5的球 |
| `SetCylinder(diameter, height)` | 直径, 高度 | `SetCylinder(1.0, 2.0)` = 半径0.5、高2.0的圆柱 |
| `SetCapsule(diameter, height)` | 直径, 高度 | `SetCapsule(1.0, 2.0)` = 半径0.5的胶囊 |
| `SetCone(diameter, height)` | 直径, 高度 | `SetCone(1.0, 2.0)` = 底面半径0.5的圆锥 |

---

## 💡 经验教训 (Lessons Learned)

1. **牢记 UrhoX 的约定**：`CollisionShape` 的圆形相关参数统一使用**直径**，不是半径
2. **代码审查要点**：看到 `SetSphere`、`SetCylinder`、`SetCapsule`、`SetCone` 时，检查传入值是否为直径
3. **命名技巧**：在代码中使用 `diameter` 变量名，增加可读性和正确性

---

## 🤖 AI 局限性分析 (AI Limitations Analysis)

**问题性质分类**：
- [ ] LLM 根本局限（数学推理、空间想象等）
- [x] 知识/经验不足（可通过学习改进）
- [ ] 上下文理解错误
- [ ] 其他

**改进建议**：
- **对 AI**：在生成 CollisionShape 代码时，明确注释参数是直径还是半径
- **对引擎**：考虑提供 `SetSphereByRadius()` 等别名函数，减少误用
- **对文档**：在 API 文档中突出强调"diameter"参数

---

## 🔗 相关资源 (Related Resources)

- 源码定义：`engine/Source/Urho3D/LuaScript/pkgs/Physics/CollisionShape.pkg`
- C++ 实现：`engine/Source/Urho3D/Physics/CollisionShape.cpp`

