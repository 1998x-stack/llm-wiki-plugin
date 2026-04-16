# mouseMove.z 获取滚轮值导致 nil 错误

**日期**: 2026-02-08
**分类**: API-Usage
**严重程度**: Medium
**游戏/项目**: 通用问题

---

## 🐛 问题现象 (Observed Behavior)

用户使用 `input.mouseMove.z` 获取鼠标滚轮值，运行时报错：

```
[ERROR] Execute Lua function failed: [string "main"]:523: attempt to perform arithmetic on a nil value (local 'wheel')
```

**复现步骤**：
1. 在 HandleUpdate 中使用 `input.mouseMove.z` 读取滚轮值
2. 滚动鼠标滚轮
3. 触发 nil 算术运算错误

**预期行为**: 获取到滚轮滚动量
**实际行为**: `.z` 返回 `nil`，导致后续算术运算崩溃

---

## 🔍 问题原因 (Root Cause Analysis)

`input.mouseMove` 返回的类型是 `IntVector2`（只有 `x` 和 `y`），**不是** `IntVector3`。

鼠标滚轮值需要通过**独立属性** `input.mouseMoveWheel` 获取。

### 为什么 AI 会犯这个错误？

API 命名形成了误导性模式：

| 属性 | 类型 | 说明 |
|------|------|------|
| `mouseMove` | `IntVector2` | 鼠标移动量（只有 x, y） |
| `mouseMoveX` | `int` | 鼠标移动 X（= mouseMove.x） |
| `mouseMoveY` | `int` | 鼠标移动 Y（= mouseMove.y） |
| `mouseMoveWheel` | `int` | 鼠标滚轮（**不是** mouseMove.z） |

`mouseMoveX`、`mouseMoveY`、`mouseMoveWheel` 的命名前缀相同，暗示它们都是 `mouseMove` 的组件。AI 自然推断 `.z` 就是滚轮值。

此外，在一些其他引擎/框架中（如 SDL 旧版本、某些 Web 框架），鼠标移动确实用 3D 向量表示，`.z` 就是滚轮。这属于跨引擎知识的错误迁移。

---

## ✅ 解决方案 (Solution)

### 错误做法 (Wrong Approach)

```lua
-- ❌ mouseMove 是 IntVector2，没有 .z 属性
local wheel = input.mouseMove.z
if wheel ~= 0 then  -- 💥 attempt to perform arithmetic on a nil value
    scrollOffset = scrollOffset - wheel * 2
end
```

### 正确做法 (Correct Approach)

```lua
-- ✅ 使用独立的 mouseMoveWheel 属性
local wheel = input.mouseMoveWheel
if wheel ~= 0 then
    scrollOffset = scrollOffset - wheel * 20
    scrollOffset = math.max(0, scrollOffset)
end

-- ✅ 或使用方法调用
local wheel = input:GetMouseMoveWheel()
```

---

## 💡 经验教训 (Lessons Learned)

1. **`mouseMove` 只有 x 和 y**：它是 `IntVector2`，不要假设有 `.z` 分量
2. **滚轮是独立属性**：使用 `input.mouseMoveWheel` 或 `input:GetMouseMoveWheel()`
3. **防御性编码**：对可能为 nil 的值先做检查再运算
4. **API 文档优先于猜测**：不确定属性是否存在时，应查阅 `engine-docs/api/input.md`

---

## 🤖 AI 局限性分析 (AI Limitations Analysis)

**问题性质分类**：
- [ ] LLM 根本局限（数学推理、空间想象等）
- [x] 知识/经验不足（可通过学习改进）
- [x] 上下文理解错误
- [ ] 其他

**具体原因**：
1. **跨引擎知识迁移错误**：AI 从 SDL、某些 Web 框架等的知识中推断 `.z` 是滚轮值
2. **文档缺失**：`input-controls.md` 的鼠标输入章节完全没有提及滚轮用法（已修复）
3. **命名误导**：`mouseMoveX/Y/Wheel` 的命名暗示它们都是 `mouseMove` 的组件

**改进措施**：
- 对 AI：已在 `input-controls.md` 的鼠标输入章节补充了滚轮子章节，包含 ⚠️ 警告
- 对引擎：API 继承自 Urho3D，命名改动成本高；可考虑长期添加 `input.mouseWheel` 别名
- 对文档：已补充完整的滚轮使用示例和常见场景

---

## 🔗 相关资源 (Related Resources)

- `engine-docs/api/input.md` - Input 模块完整 API（`mouseMoveWheel` 定义）
- `engine-docs/recipes/input-controls.md` - 输入指南（已补充滚轮章节）
