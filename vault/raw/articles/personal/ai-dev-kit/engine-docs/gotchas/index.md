# 常见陷阱与注意事项 (Gotchas)

本目录记录 UrhoX/Urho3D 开发中**实际遇到并验证过**的坑。

> ⚠️ **重要原则**：只记录确定性遇到的问题，不要添加未验证的"常识"！

---

## 📁 模块索引

| 模块 | 文件 | 已记录问题数 |
|------|------|-------------|
| **物理系统** | [physics.md](physics.md) | 3 |
| **云服务（客户端专用）** | [client-cloud-score.md](../recipes/client-cloud-score.md) | 1 |
| **节点系统** | 本文档 | 1 |
| **相机系统** | [camera.md](camera.md) | 3 |
| **碰撞形状** | collision.md | 0（待补充） |
| **刚体** | rigidbody.md | 0（待补充） |
| **渲染** | rendering.md | 0（待补充） |
| **UI 系统** | ui.md | 0（待补充） |
| **脚本** | scripting.md | 0（待补充） |

> 📷 **相机使用指南**：详见 [recipes/camera.md](../recipes/camera.md)
> ⚠️ **相机陷阱**：详见 [camera.md](camera.md)（正交投影 orthoSize、GetScreenRay 等）

---

## 🔍 已知问题列表

### 物理系统 (Physics)

1. **Rolling Friction + Cylinder 不兼容** ✅ 已验证
   - **适用**：硬币、圆盘等圆面朝上的物体（不适用于轮子类侧面滚动）
   - **症状**：硬币斜着不倒 / 弹飞
   - **解决方案**：保持 rollingFriction = 0（不设置）

2. **Collision Margin 对小物体过大** ✅ 已验证
   - **适用**：硬币、棋子等小型物体（< 0.5m）
   - **症状**：碰撞体比视觉模型大一圈，物体"漂浮"
   - **解决方案**：`shape:SetMargin(0.01)`

3. **3D 角色控制器必须使用 KinematicCharacterController** ✅ 已验证
   - **适用**：3D 角色移动控制
   - **症状**：角色跳跃后碰到墙壁侧面会卡住（挂墙）
   - **错误做法**：RigidBody + SetLinearVelocity
   - **正确做法**：使用 KinematicCharacterController 组件

详见：[physics.md](physics.md)

### 云服务 (Cloud Score)

1. **GetRankList 返回的 player 字段是 number** ✅
   - AI 容易误认为是 string，实际是 number
   - 用于字符串操作时需要 `tostring()`

详见：[client-cloud-score.md](../recipes/client-cloud-score.md)（客户端专用，服务端暂不支持云变量）

### 节点系统 (Node)

1. **SetEnabled 不能隐藏子节点的渲染组件** ✅ 已验证
   - **适用**：有子节点层级结构的对象（角色、复合物体等）
   - **症状**：调用 `node:SetEnabled(false)` 后，子节点上的 StaticModel/AnimatedModel 仍然可见
   - **根本原因**：`Component:IsEnabledEffective()` 只检查**直接父节点**的 enabled 状态，不递归检查祖先节点
   - **解决方案**：使用 `node:SetDeepEnabled(false)` 递归禁用整个子树

   ```lua
   -- ❌ 错误：只禁用父节点，子节点组件仍然渲染
   employee.node:SetEnabled(false)
   
   -- ✅ 正确：递归禁用所有子节点
   employee.node:SetDeepEnabled(false)
   ```

---

## 📝 贡献指南

### 添加新问题的要求

**必须满足以下所有条件**：

1. ✅ **实际遇到**：在真实项目中遇到此问题
2. ✅ **可复现**：能稳定复现问题
3. ✅ **已验证解决**：测试过解决方案有效
4. ✅ **有测试数据**：提供具体的参数、现象、测试结果

### 格式模板

```markdown
### ⚠️ [问题标题]

**问题描述**：[简要描述]

**实际遇到场景**：[在哪个项目/哪个文件中遇到]

**症状**：
- [可观察的现象1]
- [可观察的现象2]

**测试数据**：[具体的参数值和对应表现]

**根本原因**：[技术分析]

**解决方案**：
\`\`\`lua
-- 经过验证的解决方案
\`\`\`

**验证记录**：[测试结果，如"修改后硬币正常倒下"]
```

### ❌ 不要添加的内容

- 没有实际遇到的"可能问题"
- 来自其他引擎/框架的"常识"
- 未经验证的"最佳实践"
- 没有测试数据的猜测

---

## 📅 更新日志

| 日期 | 内容 | 验证来源 |
|------|------|---------|
| 2026-02-05 | 正交相机 orthoSize 的 0.5 因子、GetScreenRay 无缓存 | TapCode-User_Workspace 缩放补偿调试 |
| 2026-02-05 | SetEnabled 不能隐藏子节点渲染，需用 SetDeepEnabled | RestroomSystem.lua 角色隐藏问题 |
| 2026-01-05 | 3D 角色控制器必须用 KinematicCharacterController | Down100Floors.lua 挂墙问题分析 |
| 2025-12-18 | 排行榜 playerId 是数字类型 | score-test.lua 实际测试 |
| 2024-12-09 | Rolling Friction + Cylinder 不兼容 | BearCoinPuhser.lua 实际测试 |
| 2024-12-09 | Collision Margin 对小物体过大 | BearCoinPuhser.lua 实际测试 |

---

**当前状态**：8 个已验证问题
**待验证问题**：0
