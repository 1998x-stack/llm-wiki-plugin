# 物理系统 (Physics) - 已验证问题

> ⚠️ 本文档用于 AI Coding，只记录实际验证过的问题

---

## ⚠️ Rolling Friction + Cylinder 不兼容（硬币类物体）

**适用范围**：硬币、圆盘等**圆面朝上**的扁平圆柱体（不适用于轮子等侧面滚动）

**问题**：使用 `rollingFriction` 时，硬币倾斜后会"卡住"不倒或弹飞。

**原因**：Rolling Friction 设计用于轮子侧面滚动（接触点稳定）。硬币倾斜时边缘接触，曲率极小，力矩计算异常。

**解决方案**：

```lua
local body = node:CreateComponent("RigidBody")
body.friction = 0.7
body.angularDamping = 0.5
-- 不设置 rollingFriction（保持默认 0）

local shape = node:CreateComponent("CollisionShape")
shape:SetCylinder(1, 1) -- 这里不缩放，因为node的缩放会乘碰撞缩放，往往都会使用node缩放，所以一旦有node缩放这里就给默认值，否则可以设置缩放跟node视觉尺寸对齐
```

**测试数据**：

| rollingFriction | 结果 |
|-----------------|------|
| 0 | ✅ 正常 |
| 0.05 | ⚠️ 偶尔卡住 |
| 0.25+ | ❌ 斜着不倒 / 💥 弹飞 |

---

## ⚠️ Collision Margin 对小物体过大

**适用范围**：硬币、棋子等小型物体（直径 < 0.5m）

**问题**：Bullet 默认 margin (0.04m) 对小物体过大，碰撞体比视觉模型大很多，硬币"漂浮"。

**原因**：默认 margin 设计用于米级物体（人物 1.8m）。对于硬币厚度 0.03m，margin 会让厚度翻倍。

**解决方案**：

```lua
local shape = node:CreateComponent("CollisionShape")
shape:SetCylinder(diameter, height)
shape:SetMargin(0.01)  -- 缩小 margin
```

**数据对比**：

```
硬币厚度 0.03m：
- 默认 margin (0.04m)：碰撞厚度 0.11m (+267%)
- 调整后 (0.01m)：碰撞厚度 0.05m (+67%) ✅
```

---

## ✅ 硬币类小物体最佳实践

```lua
-- 黄金组合（两个关键点）
local body = node:CreateComponent("RigidBody")
body.mass = 0.05
body.friction = 0.7
body.angularDamping = 0.3-0.5
-- ❌ 不设置 rollingFriction

local shape = node:CreateComponent("CollisionShape")
shape:SetCylinder(1, 1)
shape:SetMargin(0.01)  -- ✅ 关键
```

---

## 🔴 3D 角色控制器必须使用 KinematicCharacterController

**问题**：使用动态 RigidBody + SetLinearVelocity 实现角色移动会导致"挂墙"（角色碰到墙壁侧面卡住不掉落）

**禁止的模式** ❌：

```lua
-- ❌ 动态刚体 + 每帧设置速度 = 挂墙
local body = node:CreateComponent("RigidBody")
body.mass = 1.0
-- Update 中
body:SetLinearVelocity(Vector3(moveDir.x * speed, vel.y, moveDir.z * speed))
```

**正确做法** ✅（参考 `templates/scaffold-3d-character.lua`）：

```lua
-- 1. 创建刚体（禁用移动，仅用于碰撞事件）
local body = node:CreateComponent("RigidBody")
body:SetCollisionLayerAndMask(CollisionLayerCharacter, CollisionMaskCharacter)
body.mass = 1
body:SetLinearFactor(Vector3.ZERO)   -- 关键：刚体不移动
body:SetAngularFactor(Vector3.ZERO)
body.collisionEventMode = COLLISION_ALWAYS

-- 2. 创建碰撞形状（胶囊体）
local shape = node:CreateComponent("CollisionShape")
shape:SetCapsule(0.7, 1.8, Vector3(0.0, 0.86, 0.0))

-- 3. 创建运动学角色控制器（实际控制移动）
local kinematicController = node:CreateComponent("KinematicCharacterController")
kinematicController:SetCollisionLayerAndMask(CollisionLayerKinematic, CollisionMaskKinematic)
kinematicController.jumpSpeed = 8.0

-- 4. 创建角色组件（高层封装，推荐）
local character = node:CreateComponent("CharacterComponent")
character:SetAirControlFactor(0.6)  -- 空中控制系数
```

**三个组件的职责**：

| 组件 | 职责 |
|------|------|
| `RigidBody` | 碰撞事件检测（LinearFactor=ZERO 禁用移动） |
| `KinematicCharacterController` | 实际控制角色移动、跳跃、台阶爬升 |
| `CharacterComponent` | 高层封装：输入处理、空中控制、动画参数 |

**CharacterComponent 关键属性**：

| 属性/方法 | 说明 |
|----------|------|
| `controls` | 输入控制（yaw, pitch, buttons） |
| `SetAirControlFactor(0-1)` | 空中控制系数 |
| `OnGround()` | 是否着地 |
| `IsJumping()` | 是否在跳跃 |
| `GetMoveSpeed()` | 获取移动速度（用于动画） |

**完整示例**：`templates/scaffold-3d-character.lua`

---

[返回索引](index.md)
