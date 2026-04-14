---
summary: "AI-friendly animation system with declarative config + code API for AI-generated animation logic"
related_paths:
  - engine/Source/Urho3D/Animation/**
last_updated: "2025-12-25"
---

# UrhoX AI-Friendly Animation System Design

> **设计目标**: 创建一个对 AI 编程友好的动画系统，采用声明式配置 + 代码 API 的方式，让 AI 能够直接生成和修改动画逻辑。

---

## 目录

1. [设计原则](#设计原则)
2. [Animation State Machine](#1-animation-state-machine)
3. [Blend Space](#2-blend-space)
4. [Animation Layer & Mask](#3-animation-layer--mask)
5. [Root Motion](#4-root-motion)
    - [4.5 AimOffset (程序化瞄准)](#45-aimoffset-程序化瞄准)
6. [Animation Events](#5-animation-events)
7. [Animation Graph](#6-animation-graph)
8. [完整示例](#7-完整示例)
9. [C++ 实现指南](#8-c-实现指南)
10. [调试支持](#9-调试支持)
    - [9.1-9.8 基础调试功能](#91-核心设计理念)
    - [9.9 条件表达式错误处理](#99-条件表达式错误处理)
    - [9.10 动画资源 Fallback 策略](#910-动画资源-fallback-策略)
    - [9.11-9.12 C++ 调试接口与快捷键](#911-c-调试接口)
11. [已知问题与限制](#10-已知问题与限制)
    - [10.1 BlendSpace 与 Layer BlendMode 的交互](#101-blendspace-与-layer-blendmode-的交互)

---

## 设计原则

### AI 友好的核心要求

| 原则 | 说明 |
|------|------|
| **声明式配置** | 使用 Lua Table 定义，AI 可直接生成 |
| **文本优先** | 所有配置均为文本格式，版本控制友好 |
| **语义清晰** | API 命名直观，参数含义明确 |
| **运行时可修改** | 支持动态添加/修改状态和转换 |
| **条件表达式** | 使用字符串表达式，AI 易于理解和生成 |
| **最小化样板代码** | 减少重复代码，聚焦业务逻辑 |

### 与传统系统对比

```
传统方式 (UE/Unity)          UrhoX AI-Friendly 方式
─────────────────────        ─────────────────────────
可视化节点编辑器      →      Lua Table 声明式配置
二进制资产文件        →      文本配置 + 代码 API
拖拽连线定义转换      →      字符串条件表达式
Editor-Only 修改      →      运行时动态修改
```

---

## 1. Animation State Machine

### 1.1 核心概念

```
┌─────────────────────────────────────────────────────────┐
│                  AnimationStateMachine                  │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐          │
│  │  State  │────►│  State  │────►│  State  │          │
│  │ (Idle)  │◄────│ (Walk)  │◄────│  (Run)  │          │
│  └─────────┘     └─────────┘     └─────────┘          │
│       │              │               │                 │
│       └──────────────┼───────────────┘                 │
│                      ▼                                 │
│               ┌─────────┐                              │
│               │  State  │  ← Any State Transition     │
│               │ (Jump)  │                              │
│               └─────────┘                              │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Lua API 定义

```lua
---@class AnimationStateMachine
---@field name string 状态机名称
---@field states table<string, AnimationState> 状态集合
---@field transitions AnimationTransition[] 转换规则
---@field parameters table<string, AnimationParameter> 参数定义
---@field currentState string 当前状态名
---@field defaultState string 默认状态名
---@field blendTime number 默认混合时间

---@class AnimationState
---@field name string 状态名称
---@field animation string|BlendSpace 动画资源或混合空间
---@field loop boolean 是否循环
---@field speed number 播放速度 (默认 1.0)
---@field startTime number 起始时间 (默认 0.0)
---@field blendInTime number 进入混合时间 (覆盖默认值)
---@field blendOutTime number 退出混合时间 (覆盖默认值)
---@field events AnimationEvent[] 状态事件
---@field onEnter function 进入回调
---@field onExit function 退出回调
---@field onUpdate function 更新回调

---@class AnimationTransition
---@field from string|string[] 源状态 ("*" 表示任意状态)
---@field to string 目标状态
---@field condition string 条件表达式
---@field priority number 优先级 (默认 0, 越高越优先)
---@field blendTime number 混合时间 (覆盖默认值)
---@field exitTime number 退出时间点 (0-1, nil 表示立即)
---@field interruptible boolean 是否可被打断 (默认 true)

---@class AnimationParameter
---@field type "float"|"int"|"bool"|"trigger" 参数类型
---@field default any 默认值
---@field min number 最小值 (仅数值类型)
---@field max number 最大值 (仅数值类型)
```

### 1.3 声明式配置示例

```lua
-- 创建角色移动状态机
local locomotionFSM = AnimationStateMachine.new({
    name = "CharacterLocomotion",
    defaultState = "Idle",
    blendTime = 0.2,

    -- 参数定义
    parameters = {
        speed       = { type = "float", default = 0, min = 0, max = 10 },
        direction   = { type = "float", default = 0, min = -180, max = 180 },
        isGrounded  = { type = "bool",  default = true },
        isJumping   = { type = "trigger" },  -- trigger 自动重置
        isFalling   = { type = "bool",  default = false },
        isDead      = { type = "bool",  default = false },
    },

    -- 状态定义
    states = {
        -- 基础移动状态
        {
            name = "Idle",
            animation = "Animations/Character/Idle.ani",
            loop = true,
        },
        {
            name = "Walk",
            animation = "Animations/Character/Walk.ani",
            loop = true,
            speed = 1.0,
        },
        {
            name = "Run",
            animation = "Animations/Character/Run.ani",
            loop = true,
            speed = 1.0,
        },

        -- 跳跃状态
        {
            name = "JumpStart",
            animation = "Animations/Character/JumpStart.ani",
            loop = false,
        },
        {
            name = "JumpLoop",
            animation = "Animations/Character/JumpLoop.ani",
            loop = true,
        },
        {
            name = "JumpLand",
            animation = "Animations/Character/JumpLand.ani",
            loop = false,
            blendInTime = 0.1,  -- 快速混合进入
        },

        -- 死亡状态
        {
            name = "Death",
            animation = "Animations/Character/Death.ani",
            loop = false,
            onEnter = function(self, fsm)
                -- 禁用角色控制
                fsm.owner:GetComponent("CharacterController"):SetEnabled(false)
            end,
        },
    },

    -- 转换规则
    transitions = {
        -- 移动状态转换
        { from = "Idle", to = "Walk", condition = "speed > 0.1 and speed <= 3.0" },
        { from = "Idle", to = "Run",  condition = "speed > 3.0" },
        { from = "Walk", to = "Idle", condition = "speed <= 0.1" },
        { from = "Walk", to = "Run",  condition = "speed > 3.0" },
        { from = "Run",  to = "Walk", condition = "speed <= 3.0 and speed > 0.1" },
        { from = "Run",  to = "Idle", condition = "speed <= 0.1" },

        -- 跳跃转换 (从任意地面状态)
        {
            from = {"Idle", "Walk", "Run"},
            to = "JumpStart",
            condition = "isJumping",  -- trigger 类型
            priority = 10,
        },
        {
            from = "JumpStart",
            to = "JumpLoop",
            condition = "true",  -- 动画播完自动转换
            exitTime = 1.0,      -- 等待动画播完
        },
        {
            from = "JumpLoop",
            to = "JumpLand",
            condition = "isGrounded",
        },
        {
            from = "JumpLand",
            to = "Idle",
            condition = "true",
            exitTime = 0.8,  -- 80% 时可以转换
        },

        -- 下落 (从任意状态)
        {
            from = "*",
            to = "JumpLoop",
            condition = "not isGrounded and not isFalling",
            priority = 5,
        },

        -- 死亡 (最高优先级，从任意状态)
        {
            from = "*",
            to = "Death",
            condition = "isDead",
            priority = 100,
            interruptible = false,  -- 不可被打断
        },
    },
})
```

### 1.4 运行时 API

```lua
-- 绑定到 AnimatedModel
locomotionFSM:Bind(animatedModel)

-- 更新参数 (每帧调用)
function Character:UpdateAnimation(dt)
    local velocity = self.body:GetLinearVelocity()
    local speed = Vector3(velocity.x, 0, velocity.z):Length()

    -- 设置参数
    locomotionFSM:SetFloat("speed", speed)
    locomotionFSM:SetFloat("direction", self:GetMoveDirection())
    locomotionFSM:SetBool("isGrounded", self:IsGrounded())

    -- Trigger 用法 (设置后自动重置)
    if input:GetKeyPress(KEY_SPACE) and self:IsGrounded() then
        locomotionFSM:SetTrigger("isJumping")
    end

    -- 更新状态机
    locomotionFSM:Update(dt)
end

-- 查询状态
local currentState = locomotionFSM:GetCurrentState()      -- "Walk"
local isInState = locomotionFSM:IsInState("JumpLoop")     -- true/false
local stateTime = locomotionFSM:GetStateTime()            -- 当前状态已播放时间
local normalizedTime = locomotionFSM:GetNormalizedTime()  -- 0-1 归一化时间

-- 强制转换 (忽略条件)
locomotionFSM:ForceState("Death")

-- 动态修改
locomotionFSM:AddState({
    name = "Swim",
    animation = "Animations/Character/Swim.ani",
    loop = true,
})
locomotionFSM:AddTransition({
    from = "*",
    to = "Swim",
    condition = "isInWater",
    priority = 20,
})

-- 移除状态/转换
locomotionFSM:RemoveState("Swim")
locomotionFSM:RemoveTransitionsTo("Swim")
```

### 1.5 条件表达式语法

```lua
-- 支持的表达式语法
"speed > 3.0"                           -- 比较
"speed >= 3.0 and isGrounded"           -- 逻辑与
"isJumping or isFalling"                -- 逻辑或
"not isDead"                            -- 逻辑非
"speed > 0.1 and speed <= 3.0"          -- 范围
"health <= 0"                           -- 参数支持负数
"abs(direction) > 90"                   -- 内置函数: abs, min, max, clamp
"stateTime > 0.5"                       -- 内置变量: stateTime, normalizedTime
"animationFinished"                     -- 内置条件: 动画是否播完
"true"                                  -- 常量 (用于 exitTime 转换)

-- 表达式解析示例
local expr = ConditionExpression.parse("speed > 3.0 and isGrounded")
local result = expr:Evaluate(parameters)  -- true/false
```

#### 预编译机制 (性能关键)

条件表达式在**创建时预编译**，运行时只做求值，避免每帧解析字符串。

```
┌─────────────────────────────────────────────────────────┐
│                 条件表达式生命周期                       │
│                                                         │
│  创建时 (一次性):                                       │
│  ┌─────────────┐    ┌─────────────┐    ┌────────────┐ │
│  │ 字符串      │ ─► │ 词法分析    │ ─► │ AST 节点树 │ │
│  │ "speed > 3" │    │ Tokenize    │    │ (缓存)     │ │
│  └─────────────┘    └─────────────┘    └────────────┘ │
│                                                         │
│  运行时 (每帧):                                         │
│  ┌────────────┐    ┌─────────────┐    ┌────────────┐ │
│  │ AST 节点树 │ ─► │ 查参数表    │ ─► │ bool 结果  │ │
│  │ (已缓存)   │    │ 求值计算    │    │            │ │
│  └────────────┘    └─────────────┘    └────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**实现原理**:

```cpp
class AnimationStateMachine
{
private:
    // 预编译的表达式缓存 (字符串 -> AST)
    HashMap<String, SharedPtr<ConditionExpression>> conditionCache_;

public:
    void AddTransition(const TransitionDefinition& trans)
    {
        // 创建时: 预编译条件表达式
        if (!conditionCache_.Contains(trans.condition))
        {
            auto expr = ConditionExpression::Parse(trans.condition);
            if (!expr)
            {
                // 解析失败，报错
                ReportConditionError(trans.condition, expr->GetError());
                return;
            }
            conditionCache_[trans.condition] = expr;
        }
        transitions_.Push(trans);
    }

    void EvaluateTransitions()
    {
        for (const auto& trans : transitions_)
        {
            // 运行时: 直接使用缓存的 AST 求值
            auto& expr = conditionCache_[trans.condition];
            if (expr->Evaluate(parameters_))  // O(n) 遍历 AST
            {
                TransitionTo(trans.toState);
                break;
            }
        }
    }
};
```

**AST 结构示例**:

```
表达式: "speed > 3.0 and isGrounded"

预编译后的 AST:
        ┌─────┐
        │ AND │
        └──┬──┘
      ┌────┴────┐
      ▼         ▼
  ┌───────┐  ┌──────────┐
  │   >   │  │ PARAM    │
  └───┬───┘  │isGrounded│
    ┌─┴─┐    └──────────┘
    ▼   ▼
┌──────┐ ┌─────┐
│PARAM │ │CONST│
│speed │ │ 3.0 │
└──────┘ └─────┘

运行时求值:
1. 查表: parameters["speed"] = 5.2
2. 计算: 5.2 > 3.0 = true
3. 查表: parameters["isGrounded"] = true
4. 计算: true AND true = true
```

**性能对比**:

| 方式 | 每帧开销 | 适用场景 |
|------|----------|----------|
| 每帧解析字符串 | ~100μs | ❌ 不可接受 |
| **预编译 + AST 求值** | ~0.5μs | ✅ 推荐 |
| 编译为字节码 | ~0.2μs | 可选优化 |

**缓存复用**:

```lua
-- 相同条件字符串共享同一个 AST
transitions = {
    { from = "Idle", to = "Walk", condition = "speed > 0.1" },
    { from = "Run",  to = "Walk", condition = "speed > 0.1" },  -- 复用同一个 AST
}
```

### 1.6 子状态机 (Sub-State Machine)

```lua
-- 复杂行为可以用子状态机组织
local combatFSM = AnimationStateMachine.new({
    name = "Combat",
    defaultState = "CombatIdle",

    states = {
        { name = "CombatIdle", animation = "CombatIdle.ani", loop = true },
        { name = "Attack1", animation = "Attack1.ani", loop = false },
        { name = "Attack2", animation = "Attack2.ani", loop = false },
        { name = "Attack3", animation = "Attack3.ani", loop = false },
        { name = "Block", animation = "Block.ani", loop = true },
    },

    transitions = {
        { from = "CombatIdle", to = "Attack1", condition = "attackTrigger" },
        { from = "Attack1", to = "Attack2", condition = "attackTrigger", exitTime = 0.6 },
        { from = "Attack2", to = "Attack3", condition = "attackTrigger", exitTime = 0.6 },
        { from = {"Attack1", "Attack2", "Attack3"}, to = "CombatIdle", condition = "true", exitTime = 1.0 },
        { from = "*", to = "Block", condition = "isBlocking", priority = 5 },
        { from = "Block", to = "CombatIdle", condition = "not isBlocking" },
    },

    parameters = {
        attackTrigger = { type = "trigger" },
        isBlocking = { type = "bool", default = false },
    },
})

-- 主状态机中引用子状态机
local mainFSM = AnimationStateMachine.new({
    name = "CharacterMain",
    defaultState = "Locomotion",

    states = {
        {
            name = "Locomotion",
            subStateMachine = locomotionFSM,  -- 引用子状态机
        },
        {
            name = "Combat",
            subStateMachine = combatFSM,
        },
    },

    transitions = {
        { from = "Locomotion", to = "Combat", condition = "isInCombat" },
        { from = "Combat", to = "Locomotion", condition = "not isInCombat" },
    },

    parameters = {
        isInCombat = { type = "bool", default = false },
    },
})
```

### 1.7 参数共享机制

子状态机与父状态机之间的参数共享是关键设计点。提供三种模式：

#### 模式对比

```
┌─────────────────────────────────────────────────────────┐
│              参数共享模式对比                            │
│                                                         │
│  模式 1: 共享上下文 (推荐)                              │
│  ┌─────────────────────────────────┐                   │
│  │      ParameterContext           │                   │
│  │  speed, direction, isGrounded   │                   │
│  │  isInCombat, attackTrigger ...  │                   │
│  └─────────────────────────────────┘                   │
│         ↑              ↑                               │
│     mainFSM      locomotionFSM                         │
│                                                         │
│  模式 2: 参数绑定                                       │
│  ┌──────────┐    binding    ┌──────────┐              │
│  │ mainFSM  │──────────────►│ childFSM │              │
│  │ speed    │───────────────│ speed    │              │
│  └──────────┘               └──────────┘              │
│                                                         │
│  模式 3: 参数继承                                       │
│  ┌──────────┐                                          │
│  │ mainFSM  │ (parent)                                 │
│  │ speed    │                                          │
│  └────┬─────┘                                          │
│       │ inherits                                        │
│  ┌────▼─────┐                                          │
│  │ childFSM │ (可访问 parent.speed)                    │
│  └──────────┘                                          │
└─────────────────────────────────────────────────────────┘
```

#### 模式 1: 共享参数上下文 (推荐)

```lua
-- 创建共享的参数上下文
local paramContext = ParameterContext.new({
    -- 所有状态机共享的参数
    speed       = { type = "float", default = 0 },
    direction   = { type = "float", default = 0 },
    isGrounded  = { type = "bool",  default = true },
    isInCombat  = { type = "bool",  default = false },
    attackTrigger = { type = "trigger" },
    isBlocking  = { type = "bool",  default = false },
})

-- 子状态机使用共享上下文
local locomotionFSM = AnimationStateMachine.new({
    name = "Locomotion",
    parameterContext = paramContext,  -- 使用共享上下文

    -- 不再需要单独定义 parameters
    -- 直接使用 paramContext 中的参数

    states = { ... },
    transitions = {
        { from = "Idle", to = "Walk", condition = "speed > 0.1" },
        ...
    },
})

local combatFSM = AnimationStateMachine.new({
    name = "Combat",
    parameterContext = paramContext,  -- 同一个上下文

    states = { ... },
    transitions = {
        { from = "CombatIdle", to = "Attack1", condition = "attackTrigger" },
        ...
    },
})

local mainFSM = AnimationStateMachine.new({
    name = "CharacterMain",
    parameterContext = paramContext,  -- 同一个上下文

    states = {
        { name = "Locomotion", subStateMachine = locomotionFSM },
        { name = "Combat", subStateMachine = combatFSM },
    },
    transitions = {
        { from = "Locomotion", to = "Combat", condition = "isInCombat" },
        ...
    },
})

-- 使用时只需更新一次
function Character:Update(dt)
    -- 更新共享上下文，所有状态机自动可见
    paramContext:SetFloat("speed", self.velocity:Length())
    paramContext:SetFloat("direction", self:GetMoveDirection())
    paramContext:SetBool("isGrounded", self:IsGrounded())

    mainFSM:Update(dt)
end
```

#### 模式 2: 参数绑定 (显式映射)

```lua
-- 子状态机定义自己的参数
local locomotionFSM = AnimationStateMachine.new({
    name = "Locomotion",

    parameters = {
        moveSpeed = { type = "float", default = 0 },  -- 内部命名
        moveDir   = { type = "float", default = 0 },
    },

    transitions = {
        { from = "Idle", to = "Walk", condition = "moveSpeed > 0.1" },
        ...
    },
})

-- 主状态机中显式绑定参数
local mainFSM = AnimationStateMachine.new({
    name = "CharacterMain",

    parameters = {
        speed     = { type = "float", default = 0 },
        direction = { type = "float", default = 0 },
        isInCombat = { type = "bool", default = false },
    },

    states = {
        {
            name = "Locomotion",
            subStateMachine = locomotionFSM,

            -- 参数绑定: 父参数 -> 子参数
            parameterBindings = {
                { from = "speed",     to = "moveSpeed" },  -- mainFSM.speed -> locomotionFSM.moveSpeed
                { from = "direction", to = "moveDir" },
            },
        },
    },
})

-- 更新父状态机参数，自动同步到子状态机
mainFSM:SetFloat("speed", 5.0)
-- locomotionFSM.moveSpeed 自动变为 5.0
```

#### 模式 3: 参数继承 (自动穿透)

```lua
-- 子状态机声明需要继承的参数
local locomotionFSM = AnimationStateMachine.new({
    name = "Locomotion",

    -- 继承父状态机的参数
    inheritParameters = true,

    -- 也可以指定继承哪些
    inheritParameters = { "speed", "direction", "isGrounded" },

    -- 子状态机自己的参数 (可选)
    parameters = {
        jumpTrigger = { type = "trigger" },  -- 仅子状态机使用
    },

    transitions = {
        -- 可以直接使用父状态机的参数
        { from = "Idle", to = "Walk", condition = "speed > 0.1" },
        -- 也可以使用自己的参数
        { from = "Walk", to = "Jump", condition = "jumpTrigger" },
    },
})

-- 主状态机
local mainFSM = AnimationStateMachine.new({
    name = "CharacterMain",

    parameters = {
        speed = { type = "float", default = 0 },
        direction = { type = "float", default = 0 },
        isGrounded = { type = "bool", default = true },
        isInCombat = { type = "bool", default = false },
    },

    states = {
        { name = "Locomotion", subStateMachine = locomotionFSM },
    },
})

-- 查询参数时自动向上查找
local speed = locomotionFSM:GetFloat("speed")
-- 如果 locomotionFSM 没有定义 speed，自动从 mainFSM 获取
```

#### 参数作用域规则

```lua
-- 参数查找顺序 (从内到外)
--
-- 1. 当前状态机的 parameters
-- 2. 共享的 parameterContext
-- 3. 父状态机的 parameters (如果 inheritParameters = true)
-- 4. 报错: Unknown parameter

-- 参数命名冲突处理
local locomotionFSM = AnimationStateMachine.new({
    parameterContext = sharedContext,

    parameters = {
        -- 覆盖共享上下文中的同名参数 (局部优先)
        speed = { type = "float", default = 0, scope = "local" },
    },

    -- 显式访问共享参数
    transitions = {
        { from = "A", to = "B", condition = "context.speed > 0.1" },  -- 共享上下文
        { from = "A", to = "C", condition = "speed > 0.1" },         -- 局部参数
    },
})
```

#### 双向同步 (高级)

```lua
-- 子状态机可以修改参数，同步回父状态机
local combatFSM = AnimationStateMachine.new({
    name = "Combat",
    inheritParameters = true,

    states = {
        {
            name = "Attack1",
            animation = "Attack1.ani",
            onEnter = function(self, fsm)
                -- 修改继承的参数
                fsm:SetBool("isAttacking", true)  -- 同步回父状态机
            end,
            onExit = function(self, fsm)
                fsm:SetBool("isAttacking", false)
            end,
        },
    },
})

-- 父状态机可以响应子状态机的参数变化
mainFSM:WatchParameter("isAttacking", function(name, oldVal, newVal)
    print("Attack state changed:", newVal)
end)
```

#### 推荐实践

```lua
-- ✅ 推荐: 使用共享上下文 (简单直观)
local ctx = ParameterContext.new({ ... })
local fsmA = AnimationStateMachine.new({ parameterContext = ctx, ... })
local fsmB = AnimationStateMachine.new({ parameterContext = ctx, ... })

-- ✅ 推荐: 复杂场景使用参数绑定 (显式可控)
{ parameterBindings = { { from = "speed", to = "moveSpeed" } } }

-- ⚠️ 谨慎: 参数继承可能导致隐式依赖
-- 适合简单的父子关系，不适合深层嵌套
```

---

## 2. Blend Space

### 2.1 设计决策：纯资源文件

BlendSpace 采用**纯资源文件**设计，不支持代码中动态创建。

```
┌─────────────────────────────────────────────────────────┐
│  设计理由:                                              │
│                                                         │
│  1. BlendSpace 配置通常是固定的 (美术决定)              │
│  2. 代码动态创建的需求很少                              │
│  3. 资源文件支持:                                       │
│     - 美术可视化编辑                                    │
│     - 版本控制                                          │
│     - 热重载                                            │
│     - ResourceCache 统一管理                            │
└─────────────────────────────────────────────────────────┘

工作流:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 美术编辑器  │ ─► │ .blendspace │ ─► │ 代码中引用  │
│ 可视化配置  │    │   资源文件  │    │   路径      │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 2.2 核心概念

```
┌─────────────────────────────────────────────────────────┐
│                    BlendSpace2D                         │
│                                                         │
│  Speed ▲                                                │
│    6   │     ×RunLeft    ×RunFwd    ×RunRight          │
│        │                                                │
│    3   │    ×WalkLeft   ×WalkFwd   ×WalkRight          │
│        │                                                │
│    0   │                 ×Idle                          │
│        └────────────────────────────────────►          │
│           -90           0           90     Direction    │
└─────────────────────────────────────────────────────────┘
```

### 2.3 资源文件格式 (.blendspace)

统一使用 `.blendspace` 扩展名，通过内部 `type` 字段区分类型。

#### 1D BlendSpace

```json
// MovementSpeed.blendspace
{
    "type": "BlendSpace1D",
    "name": "MovementSpeed",
    "parameter": "speed",
    "points": [
        { "value": 0, "animation": "Animations/Idle.ani" },
        { "value": 2, "animation": "Animations/Walk.ani" },
        { "value": 4, "animation": "Animations/Jog.ani" },
        { "value": 6, "animation": "Animations/Run.ani" },
        { "value": 8, "animation": "Animations/Sprint.ani", "speed": 1.2 }
    ]
}
```

#### 2D BlendSpace

```json
// Movement8Way.blendspace
{
    "type": "BlendSpace2D",
    "name": "Movement8Way",
    "parameterX": "direction",
    "parameterY": "speed",
    "interpolation": "triangular",
    "points": [
        { "x": 0, "y": 0, "animation": "Animations/Idle.ani" },

        { "x": 0,    "y": 2, "animation": "Animations/WalkFwd.ani" },
        { "x": 45,   "y": 2, "animation": "Animations/WalkFwdRight.ani" },
        { "x": 90,   "y": 2, "animation": "Animations/WalkRight.ani" },
        { "x": 135,  "y": 2, "animation": "Animations/WalkBwdRight.ani" },
        { "x": 180,  "y": 2, "animation": "Animations/WalkBwd.ani" },
        { "x": -135, "y": 2, "animation": "Animations/WalkBwdLeft.ani" },
        { "x": -90,  "y": 2, "animation": "Animations/WalkLeft.ani" },
        { "x": -45,  "y": 2, "animation": "Animations/WalkFwdLeft.ani" },

        { "x": 0,    "y": 5, "animation": "Animations/RunFwd.ani" },
        { "x": 45,   "y": 5, "animation": "Animations/RunFwdRight.ani" },
        { "x": 90,   "y": 5, "animation": "Animations/RunRight.ani" },
        { "x": 135,  "y": 5, "animation": "Animations/RunBwdRight.ani" },
        { "x": 180,  "y": 5, "animation": "Animations/RunBwd.ani" },
        { "x": -135, "y": 5, "animation": "Animations/RunBwdLeft.ani" },
        { "x": -90,  "y": 5, "animation": "Animations/RunLeft.ani" },
        { "x": -45,  "y": 5, "animation": "Animations/RunFwdLeft.ani" }
    ]
}
```

#### Aim Offset (加性混合)

```json
// AimOffset.blendspace
{
    "type": "AimOffset",
    "name": "AimOffset",
    "parameterX": "aimYaw",
    "parameterY": "aimPitch",
    "basePose": "Animations/AimCenter.ani",
    "blendMode": "additive",
    "points": [
        { "x": 0,   "y": 0,   "animation": "Animations/AimCenter.ani" },
        { "x": -90, "y": 0,   "animation": "Animations/AimLeft.ani" },
        { "x": 90,  "y": 0,   "animation": "Animations/AimRight.ani" },
        { "x": 0,   "y": 90,  "animation": "Animations/AimUp.ani" },
        { "x": 0,   "y": -90, "animation": "Animations/AimDown.ani" },
        { "x": -90, "y": 90,  "animation": "Animations/AimLeftUp.ani" },
        { "x": 90,  "y": 90,  "animation": "Animations/AimRightUp.ani" },
        { "x": -90, "y": -90, "animation": "Animations/AimLeftDown.ani" },
        { "x": 90,  "y": -90, "animation": "Animations/AimRightDown.ani" }
    ]
}
```

#### Direct Blend (直接权重控制)

直接通过参数控制每个动画的权重，适用于面部表情、Morph Target 等场景。

```json
// FacialExpression.blendspace
{
    "type": "DirectBlend",
    "name": "FacialExpression",
    "normalizeWeights": true,
    "animations": [
        { "animation": "Animations/Face/Neutral.ani", "weightParam": "neutralWeight" },
        { "animation": "Animations/Face/Happy.ani",   "weightParam": "happyWeight" },
        { "animation": "Animations/Face/Sad.ani",     "weightParam": "sadWeight" },
        { "animation": "Animations/Face/Angry.ani",   "weightParam": "angryWeight" },
        { "animation": "Animations/Face/Surprised.ani", "weightParam": "surprisedWeight" }
    ]
}
```

**使用示例**:

```lua
-- 直接设置权重参数
fsm:SetFloat("happyWeight", 0.7)
fsm:SetFloat("surprisedWeight", 0.3)
-- 结果: Happy 70% + Surprised 30%
```

**典型应用**:
- 面部表情混合
- 受伤/疲劳状态混合
- Morph Target 控制

### 2.4 在状态机中使用

```lua
-- 状态机中通过路径引用 BlendSpace 资源
local locomotionFSM = AnimationStateMachine.new({
    name = "Locomotion",
    defaultState = "Movement",

    states = {
        {
            name = "Movement",
            -- 引用 BlendSpace 资源文件路径
            blendSpace = "Animations/Movement8Way.blendspace",
            loop = true,
        },
        {
            name = "Jump",
            animation = "Animations/Jump.ani",
            loop = false,
        },
    },

    transitions = {
        { from = "Movement", to = "Jump", condition = "isJumping" },
        { from = "Jump", to = "Movement", condition = "isGrounded", exitTime = 0.8 },
    },

    parameters = {
        speed = { type = "float", default = 0 },
        direction = { type = "float", default = 0 },
        isJumping = { type = "trigger" },
        isGrounded = { type = "bool", default = true },
    },
})

-- 状态机自动:
-- 1. 加载 BlendSpace 资源
-- 2. 根据 parameters 中的 speed/direction 采样
-- 3. 应用混合权重到 AnimationController
```

### 2.5 C++ 实现

```cpp
// BlendSpace.h
namespace Urho3D
{

/// 混合权重结果
struct AnimationBlendWeight
{
    String animation;
    float weight;
    float speed = 1.0f;
};

/// BlendSpace 基类 (继承 Resource)
class URHO3D_API BlendSpaceBase : public Resource
{
    URHO3D_OBJECT(BlendSpaceBase, Resource);

public:
    explicit BlendSpaceBase(Context* context);

    /// Resource 接口
    bool BeginLoad(Deserializer& source) override;
    bool Save(Serializer& dest) const override;

    /// 采样 - 根据参数值返回动画权重列表
    virtual Vector<AnimationBlendWeight> Sample(
        const HashMap<String, float>& params) const = 0;

    /// 获取参数名
    virtual Vector<String> GetParameterNames() const = 0;

protected:
    String name_;
};

/// 1D BlendSpace
class URHO3D_API BlendSpace1D : public BlendSpaceBase
{
    URHO3D_OBJECT(BlendSpace1D, BlendSpaceBase);

public:
    bool BeginLoad(Deserializer& source) override;
    Vector<AnimationBlendWeight> Sample(
        const HashMap<String, float>& params) const override;
    Vector<String> GetParameterNames() const override;

private:
    String parameterName_;
    struct Point { float value; String animation; float speed; };
    Vector<Point> points_;  // 按 value 排序
};

/// 2D BlendSpace
class URHO3D_API BlendSpace2D : public BlendSpaceBase
{
    URHO3D_OBJECT(BlendSpace2D, BlendSpaceBase);

public:
    bool BeginLoad(Deserializer& source) override;
    Vector<AnimationBlendWeight> Sample(
        const HashMap<String, float>& params) const override;
    Vector<String> GetParameterNames() const override;

private:
    void BuildTriangulation();  // 构建 Delaunay 三角网格
    int FindContainingTriangle(float x, float y) const;
    Vector3 ComputeBarycentricCoords(float x, float y, int triIdx) const;

    String parameterNameX_;
    String parameterNameY_;
    struct Point { float x, y; String animation; float speed; };
    Vector<Point> points_;
    struct Triangle { unsigned i0, i1, i2; };
    Vector<Triangle> triangles_;  // 预计算的三角网格
};

} // namespace Urho3D
```

### 2.6 状态机集成

```cpp
// AnimationStateMachine 中处理 BlendSpace 状态
void AnimationStateMachine::UpdateBlendSpaceState(float timeStep)
{
    auto* blendSpace = GetSubsystem<ResourceCache>()->
        GetResource<BlendSpaceBase>(currentState_.blendSpacePath);

    if (!blendSpace)
        return;

    // 收集 BlendSpace 需要的参数
    HashMap<String, float> blendParams;
    for (const auto& paramName : blendSpace->GetParameterNames())
    {
        blendParams[paramName] = paramContext_->GetFloat(paramName);
    }

    // 采样获取权重
    auto weights = blendSpace->Sample(blendParams);

    // 应用到 AnimationController
    for (const auto& w : weights)
    {
        animController_->Play(w.animation, currentState_.layer, true, blendTime_);
        animController_->SetWeight(w.animation, w.weight);
        if (w.speed != 1.0f)
            animController_->SetSpeed(w.animation, w.speed);
    }
}
```

---

## 3. Animation Layer & Mask

### 3.1 核心概念

```
┌─────────────────────────────────────────────────────────┐
│                   Animation Layers                      │
│                                                         │
│  Layer 2: Additive    [AimOffset - 上半身]             │
│           ↓ Additive Blend                              │
│  Layer 1: Override    [Attack - 上半身]                │
│           ↓ Override Blend                              │
│  Layer 0: Base        [Locomotion - 全身]              │
│                                                         │
│  最终姿势 = Base + Override(masked) + Additive(masked) │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Avatar Mask 定义

```lua
---@class AvatarMask
---@field name string 蒙版名称
---@field bones table<string, number> 骨骼权重映射 (0-1)
---@field includeChildren boolean 是否包含子骨骼

-- 预定义蒙版
AvatarMask.FullBody = AvatarMask.new({
    name = "FullBody",
    bones = { ["Root"] = 1.0 },
    includeChildren = true,
})

AvatarMask.UpperBody = AvatarMask.new({
    name = "UpperBody",
    bones = {
        ["Spine"] = 1.0,
        ["Spine1"] = 1.0,
        ["Spine2"] = 1.0,
        ["Neck"] = 1.0,
        ["Head"] = 1.0,
        ["LeftShoulder"] = 1.0,
        ["RightShoulder"] = 1.0,
    },
    includeChildren = true,
})

AvatarMask.LowerBody = AvatarMask.new({
    name = "LowerBody",
    bones = {
        ["Hips"] = 1.0,
        ["LeftUpLeg"] = 1.0,
        ["RightUpLeg"] = 1.0,
    },
    includeChildren = true,
})

AvatarMask.LeftArm = AvatarMask.new({
    name = "LeftArm",
    bones = { ["LeftShoulder"] = 1.0 },
    includeChildren = true,
})

AvatarMask.RightArm = AvatarMask.new({
    name = "RightArm",
    bones = { ["RightShoulder"] = 1.0 },
    includeChildren = true,
})

-- 自定义蒙版
local weaponArmMask = AvatarMask.new({
    name = "WeaponArm",
    bones = {
        ["RightShoulder"] = 1.0,
        ["RightArm"] = 1.0,
        ["RightForeArm"] = 1.0,
        ["RightHand"] = 1.0,
        -- 渐变权重
        ["Spine2"] = 0.5,
        ["Spine1"] = 0.3,
        ["Spine"] = 0.1,
    },
    includeChildren = true,
})
```

### 3.3 Animation Layer 定义

```lua
---@class AnimationLayer
---@field name string 层名称
---@field index number 层索引 (0 = 基础层)
---@field blendMode "override"|"additive" 混合模式
---@field weight number 层权重 (0-1)
---@field mask AvatarMask 骨骼蒙版
---@field stateMachine AnimationStateMachine 该层的状态机

-- 创建多层动画系统
local characterAnimator = AnimationLayerController.new({
    name = "CharacterAnimator",

    layers = {
        -- 基础层: 全身移动
        {
            name = "Base",
            index = 0,
            blendMode = "override",
            mask = AvatarMask.FullBody,
            stateMachine = locomotionFSM,
        },

        -- 覆盖层: 上半身动作 (攻击、交互等)
        {
            name = "UpperBody",
            index = 1,
            blendMode = "override",
            weight = 0,  -- 默认禁用
            mask = AvatarMask.UpperBody,
            stateMachine = upperBodyFSM,
        },

        -- 加性层: 瞄准偏移
        {
            name = "AimLayer",
            index = 2,
            blendMode = "additive",
            weight = 0,
            mask = AvatarMask.UpperBody,
            stateMachine = aimFSM,
        },
    },
})

-- 运行时控制
characterAnimator:SetLayerWeight("UpperBody", 1.0)  -- 启用上半身层
characterAnimator:SetLayerWeight("AimLayer", 0.8)   -- 80% 瞄准权重

-- 平滑过渡层权重
characterAnimator:CrossfadeLayerWeight("UpperBody", 1.0, 0.3)  -- 0.3秒过渡到1.0
```

### 3.4 IK Pass (每层可选)

```lua
-- 在层定义中启用 IK
{
    name = "Base",
    index = 0,
    blendMode = "override",
    mask = AvatarMask.FullBody,
    stateMachine = locomotionFSM,

    -- IK 配置
    ikPass = {
        enabled = true,
        footIK = {
            enabled = true,
            heightOffset = 0.05,
            raycastDistance = 0.5,
        },
        handIK = {
            enabled = false,
        },
        lookAtIK = {
            enabled = true,
            target = nil,  -- 运行时设置
            weight = 1.0,
            bodyWeight = 0.3,
            headWeight = 0.8,
            eyesWeight = 0.5,
            clampWeight = 0.5,
        },
    },
}

-- 运行时控制 IK
characterAnimator:SetIKTarget("LookAt", targetPosition)
characterAnimator:SetIKWeight("LookAt", 1.0)
characterAnimator:SetIKTarget("LeftHand", doorHandlePosition)
characterAnimator:SetIKWeight("LeftHand", 1.0)
```

---

## 4. Root Motion

### 4.1 核心概念

```
┌─────────────────────────────────────────────────────────┐
│                     Root Motion                         │
│                                                         │
│  动画数据:                                              │
│  ┌─────────────────────────────────────┐               │
│  │ Frame 0    Frame 10   Frame 20     │               │
│  │   ○          ○──►       ○──────►   │  位移数据     │
│  │  pos(0,0)  pos(0.5,0) pos(1.2,0)  │               │
│  └─────────────────────────────────────┘               │
│                     ↓                                   │
│              Root Motion 提取                           │
│                     ↓                                   │
│  ┌─────────────────────────────────────┐               │
│  │  角色位移 = 动画驱动 (非代码驱动)    │               │
│  └─────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Root Motion 配置

```lua
---@class RootMotionConfig
---@field enabled boolean 是否启用根运动
---@field applyPosition boolean 应用位置
---@field applyRotation boolean 应用旋转
---@field lockY boolean 锁定 Y 轴 (不应用垂直位移)
---@field bakeIntoPose boolean 烘焙到姿势 (不移动角色)
---@field rootBone string 根骨骼名称 (默认 "Root")

-- 在状态中配置 Root Motion
local locomotionFSM = AnimationStateMachine.new({
    name = "Locomotion",

    -- 全局 Root Motion 设置
    rootMotion = {
        enabled = true,
        applyPosition = true,
        applyRotation = true,
        lockY = true,  -- 使用物理控制垂直运动
    },

    states = {
        {
            name = "Walk",
            animation = "Walk.ani",
            loop = true,
            -- 覆盖全局设置
            rootMotion = {
                enabled = true,
                applyPosition = true,
                applyRotation = false,  -- 走路不应用旋转
            },
        },
        {
            name = "Turn90Left",
            animation = "Turn90Left.ani",
            loop = false,
            rootMotion = {
                enabled = true,
                applyPosition = true,
                applyRotation = true,  -- 转向动画应用旋转
            },
        },
        {
            name = "Jump",
            animation = "Jump.ani",
            loop = false,
            rootMotion = {
                enabled = false,  -- 跳跃由物理控制
            },
        },
    },
})
```

### 4.3 Root Motion API

```lua
-- 获取 Root Motion 数据
local deltaPosition = animator:GetRootMotionDeltaPosition()  -- Vector3
local deltaRotation = animator:GetRootMotionDeltaRotation()  -- Quaternion

-- 手动应用 (如果需要自定义处理)
function Character:FixedUpdate(dt)
    if animator:IsRootMotionEnabled() then
        local delta = animator:GetRootMotionDeltaPosition()

        -- 自定义处理: 例如考虑地形坡度
        delta = self:AdjustForSlope(delta)

        -- 应用到角色控制器
        self.characterController:Move(delta)
    end
end

-- 混合 Root Motion 和代码控制
animator:SetRootMotionWeight(0.7)  -- 70% 动画, 30% 代码控制
```

### 4.4 Motion Warping (动画变形)

```lua
---@class MotionWarpingConfig
---@field enabled boolean
---@field targets MotionWarpTarget[]

---@class MotionWarpTarget
---@field name string 目标名称
---@field syncPoint number 同步时间点 (0-1)
---@field targetPosition Vector3 目标位置
---@field targetRotation Quaternion 目标旋转
---@field warpPosition boolean 变形位置
---@field warpRotation boolean 变形旋转

-- Motion Warping 示例: 攻击动画对准目标
local attackState = {
    name = "Attack",
    animation = "SwordAttack.ani",
    loop = false,

    motionWarping = {
        enabled = true,
        targets = {
            {
                name = "AttackTarget",
                syncPoint = 0.4,  -- 攻击命中时间点
                targetPosition = nil,  -- 运行时设置
                warpPosition = true,
                warpRotation = true,
            },
        },
    },
}

-- 运行时设置目标
animator:SetMotionWarpingTarget("AttackTarget", enemyPosition, enemyRotation)
animator:PlayState("Attack")
```

### 4.5 AimOffset (程序化瞄准)

程序化地旋转脊椎/脖子/头部骨骼，实现角色瞄准效果。在动画更新后应用，叠加在动画结果之上。

#### 核心概念

```
┌─────────────────────────────────────────────────────────┐
│                     AimOffset                            │
│                                                         │
│  输入: pitch (俯仰角), yaw (偏航角)                      │
│                                                         │
│        ↑ pitch (+)                                      │
│        │                                                │
│   ←────┼────→ yaw                                       │
│        │                                                │
│        ↓ pitch (-)                                      │
│                                                         │
│  骨骼链:                                                │
│  ┌──────┐    ┌──────┐    ┌──────┐                      │
│  │Spine │───►│ Neck │───►│ Head │                      │
│  │ 30%  │    │ 30%  │    │ 40%  │  ← 权重分配          │
│  └──────┘    └──────┘    └──────┘                      │
│                                                         │
│  最终效果: 各骨骼按权重分担总旋转量                      │
└─────────────────────────────────────────────────────────┘
```

#### 配置示例

```lua
-- 创建 AimOffset 组件
local aimOffset = characterNode:CreateComponent("AimOffset")

-- 配置骨骼链（权重之和建议为 1.0）
aimOffset:AddBone("Bip001 Spine1", 0.2, 0.2)   -- pitch权重, yaw权重
aimOffset:AddBone("Bip001 Spine2", 0.2, 0.2)
aimOffset:AddBone("Bip001 Neck", 0.3, 0.3)
aimOffset:AddBone("Bip001 Head", 0.3, 0.3)

-- 配置角度限制
aimOffset:SetMaxPitch(60.0)   -- 最大俯仰角 ±60°
aimOffset:SetMaxYaw(90.0)     -- 最大偏航角 ±90°

-- 配置平滑速度（值越大过渡越快，0 = 无平滑）
aimOffset:SetSmoothSpeed(10.0)

-- 启用
aimOffset:SetEnabled(true)
```

#### 运行时控制

```lua
-- 每帧更新目标角度
function UpdateAiming(timeStep)
    -- 计算相机方向与角色朝向的差值
    local characterYaw = characterNode:GetWorldRotation():YawAngle()
    local cameraYaw = cameraNode:GetWorldRotation():YawAngle()
    local cameraPitch = cameraNode:GetWorldRotation():PitchAngle()

    -- 设置相对于角色的瞄准角度
    local relativeYaw = cameraYaw - characterYaw
    -- 规范化到 -180 ~ 180
    while relativeYaw > 180 do relativeYaw = relativeYaw - 360 end
    while relativeYaw < -180 do relativeYaw = relativeYaw + 360 end

    aimOffset:SetTargetAngles(cameraPitch, relativeYaw)
end
```

#### Yaw 补偿

当动画本身有旋转（如持枪动画角色稍微侧身）时，可以设置 Yaw 补偿：

```lua
-- 补偿动画自带的 -15° 侧身
aimOffset:SetYawCompensation(-15.0)
```

> **注意**：这是一个过渡方案。理想情况下应该在运行时自动获取持枪动画的 Spine 骨骼偏移量，但实现较为复杂（需要在动画应用后、AimOffset 应用前读取骨骼旋转）。目前采用手动配置补偿值的方式。

#### 与 CharacterComponent 配合

`CharacterComponent` 在战斗模式下会自动使用 `AimOffset` 的 `maxYaw` 来限制角色旋转：

```cpp
// CharacterComponent.cpp
float maxYaw = aimOffset_ ? aimOffset_->GetMaxYaw() : 60.0f;

// 当相机 yaw 超出 maxYaw 范围时，角色才旋转
if (isMoving || Abs(yawDiff) > maxYaw)
{
    // 旋转角色
}
```

#### C++ API

```cpp
class AimOffset : public Component
{
public:
    // 骨骼配置
    void AddBone(const String& boneName, float pitchWeight, float yawWeight);
    void AddBone(const String& boneName, float weight);  // pitch/yaw 使用相同权重
    void RemoveBone(const String& boneName);
    void ClearBones();

    // 目标角度
    void SetTargetPitch(float pitch);
    void SetTargetYaw(float yaw);
    void SetTargetAngles(float pitch, float yaw);
    float GetTargetPitch() const;
    float GetTargetYaw() const;

    // 角度限制
    void SetMaxPitch(float maxPitch);
    void SetMaxYaw(float maxYaw);
    float GetMaxPitch() const;
    float GetMaxYaw() const;

    // 平滑
    void SetSmoothSpeed(float speed);
    float GetSmoothSpeed() const;

    // Yaw 补偿
    void SetYawCompensation(float compensation);
    float GetYawCompensation() const;

    // 启用/禁用
    void SetEnabled(bool enabled);
    bool IsEnabled() const;

    // 调试
    void DebugPrintBones() const;
};
```

#### 实现要点

1. **应用时机**：在 `E_SCENEDRAWABLEUPDATEFINISHED` 事件中应用，确保在动画更新之后
2. **旋转空间**：使用角色的世界坐标轴（右轴用于 pitch，上轴用于 yaw）
3. **平滑算法**：使用指数衰减 `factor = 1 - exp(-speed * dt)` 实现平滑过渡
4. **Yaw 补偿**：仅应用于第一个骨骼（通常是 Spine），不按权重分配

---

## 5. Animation Events

### 5.1 核心概念

```
┌─────────────────────────────────────────────────────────┐
│              Animation Event Timeline                   │
│                                                         │
│  ──●────────●─────────────●────────●──────────●──►     │
│    │        │             │        │          │   Time  │
│    │        │             │        │          │         │
│  Enter   FootStep      Attack   FootStep    Exit       │
│  State   (Sound)       (Damage) (Sound)     State      │
│                                                         │
│  ● = Event Trigger Point                               │
└─────────────────────────────────────────────────────────┘
```

### 5.2 事件定义

```lua
---@class AnimationEvent
---@field name string 事件名称
---@field time number 触发时间 (秒或归一化 0-1)
---@field normalized boolean 是否为归一化时间
---@field data table 事件数据
---@field callback function 回调函数

---@class AnimationEventState  -- 状态型事件 (有持续时间)
---@field name string 事件名称
---@field startTime number 开始时间
---@field endTime number 结束时间
---@field onEnter function 进入回调
---@field onUpdate function 更新回调
---@field onExit function 退出回调

-- 在状态中定义事件
local attackState = {
    name = "Attack",
    animation = "SwordAttack.ani",
    loop = false,

    -- 瞬时事件
    events = {
        {
            name = "PlaySound",
            time = 0.1,
            data = { sound = "Sounds/SwordSwing.wav" },
        },
        {
            name = "EnableDamage",
            time = 0.3,
            normalized = true,  -- 30% 动画时间点
        },
        {
            name = "DisableDamage",
            time = 0.5,
            normalized = true,
        },
        {
            name = "SpawnVFX",
            time = 0.35,
            normalized = true,
            data = {
                effect = "Effects/SwordSlash.xml",
                bone = "RightHand",
                offset = Vector3(0, 0, 0.5),
            },
        },
    },

    -- 状态型事件 (有持续时间)
    eventStates = {
        {
            name = "DamageWindow",
            startTime = 0.3,
            endTime = 0.5,
            normalized = true,
            onEnter = function(self, animator)
                self.weapon:EnableHitbox(true)
            end,
            onExit = function(self, animator)
                self.weapon:EnableHitbox(false)
            end,
        },
        {
            name = "SuperArmor",
            startTime = 0.2,
            endTime = 0.6,
            normalized = true,
            onEnter = function(self, animator)
                self.character:SetSuperArmor(true)
            end,
            onExit = function(self, animator)
                self.character:SetSuperArmor(false)
            end,
        },
    },
}
```

### 5.3 事件监听

```lua
-- 全局事件监听
animator:RegisterEventHandler("PlaySound", function(event, animator)
    local sound = event.data.sound
    audioManager:PlaySound(sound)
end)

animator:RegisterEventHandler("SpawnVFX", function(event, animator)
    local effect = event.data.effect
    local bone = event.data.bone
    local offset = event.data.offset

    local boneNode = animator:GetBoneNode(bone)
    local worldPos = boneNode:LocalToWorld(offset)

    effectManager:SpawnEffect(effect, worldPos)
end)

-- 状态特定事件监听
animator:RegisterStateEventHandler("Attack", "EnableDamage", function(event, animator)
    character:EnableWeaponDamage(true)
end)

-- 移除监听
animator:UnregisterEventHandler("PlaySound")
```

### 5.4 Foot IK 事件 (特殊)

```lua
-- 脚步事件自动生成 IK 调整
local walkState = {
    name = "Walk",
    animation = "Walk.ani",
    loop = true,

    footEvents = {
        {
            name = "LeftFoot",
            time = 0.0,
            foot = "LeftFoot",
        },
        {
            name = "RightFoot",
            time = 0.5,
            normalized = true,
            foot = "RightFoot",
        },
    },
}

-- 脚步事件处理
animator:RegisterEventHandler("FootStep", function(event, animator)
    local foot = event.data.foot
    local footBone = animator:GetBoneNode(foot)
    local footPos = footBone:GetWorldPosition()

    -- 播放脚步声
    local groundMaterial = physics:RaycastGround(footPos)
    audioManager:PlayFootstep(groundMaterial)

    -- 生成脚印
    decalManager:SpawnFootprint(footPos, groundMaterial)
end)
```

---

## 6. Animation Graph

### 6.1 核心概念

Animation Graph 是一个更高级的系统，允许组合多个节点进行复杂的动画处理。

```
┌─────────────────────────────────────────────────────────┐
│                   Animation Graph                       │
│                                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐            │
│  │ State   │───►│ Blend   │───►│ IK      │──► Output  │
│  │ Machine │    │ Space   │    │ Pass    │            │
│  └─────────┘    └─────────┘    └─────────┘            │
│       │              │              │                  │
│       └──────────────┴──────────────┘                  │
│                      │                                  │
│              ┌───────┴───────┐                         │
│              │   Parameters  │                         │
│              └───────────────┘                         │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Graph 节点定义

```lua
---@class AnimationGraphNode
---@field type string 节点类型
---@field name string 节点名称
---@field inputs table 输入连接
---@field outputs table 输出连接
---@field properties table 节点属性

-- 可用节点类型
local NodeTypes = {
    "StateMachine",      -- 状态机节点
    "BlendSpace1D",      -- 1D 混合空间
    "BlendSpace2D",      -- 2D 混合空间
    "AimOffset",         -- 瞄准偏移
    "LayerBlend",        -- 层混合
    "AdditiveBlend",     -- 加性混合
    "TwoBoneIK",         -- 双骨骼 IK
    "LookAtIK",          -- 注视 IK
    "FootIK",            -- 脚部 IK
    "BoneMask",          -- 骨骼蒙版
    "ModifyBone",        -- 骨骼修改
    "CopyBone",          -- 骨骼复制
    "Output",            -- 输出节点
}

-- 创建 Animation Graph
local characterGraph = AnimationGraph.new({
    name = "CharacterAnimationGraph",

    parameters = {
        speed = { type = "float", default = 0 },
        direction = { type = "float", default = 0 },
        aimYaw = { type = "float", default = 0 },
        aimPitch = { type = "float", default = 0 },
        isAiming = { type = "bool", default = false },
        lookAtTarget = { type = "vector3", default = Vector3.ZERO },
    },

    nodes = {
        -- 基础移动状态机
        {
            type = "StateMachine",
            name = "Locomotion",
            properties = {
                stateMachine = locomotionFSM,
            },
        },

        -- 瞄准层
        {
            type = "AimOffset",
            name = "AimOffset",
            properties = {
                aimOffset = aimOffsetDef,
                parameterX = "aimYaw",
                parameterY = "aimPitch",
            },
        },

        -- 层混合
        {
            type = "LayerBlend",
            name = "AimBlend",
            inputs = {
                base = "Locomotion",
                overlay = "AimOffset",
            },
            properties = {
                mask = AvatarMask.UpperBody,
                blendWeight = "isAiming",  -- 参数驱动权重
            },
        },

        -- 注视 IK
        {
            type = "LookAtIK",
            name = "LookAt",
            inputs = {
                pose = "AimBlend",
            },
            properties = {
                target = "lookAtTarget",
                weight = 0.8,
                bodyWeight = 0.2,
                headWeight = 0.8,
            },
        },

        -- 脚部 IK
        {
            type = "FootIK",
            name = "FootPlacement",
            inputs = {
                pose = "LookAt",
            },
            properties = {
                enabled = true,
                heightOffset = 0.05,
            },
        },

        -- 输出
        {
            type = "Output",
            name = "FinalPose",
            inputs = {
                pose = "FootPlacement",
            },
        },
    },
})

-- 绑定到模型
characterGraph:Bind(animatedModel)

-- 更新参数
function Character:Update(dt)
    characterGraph:SetFloat("speed", self.velocity:Length())
    characterGraph:SetFloat("direction", self:GetMoveDirection())
    characterGraph:SetBool("isAiming", self:IsAiming())
    characterGraph:SetVector3("lookAtTarget", self:GetLookAtTarget())

    characterGraph:Update(dt)
end
```

### 6.3 自定义节点

```lua
-- 注册自定义节点类型
AnimationGraph.RegisterNodeType({
    type = "SpringBone",
    name = "弹簧骨骼",

    properties = {
        bones = { type = "string[]", description = "受影响的骨骼" },
        stiffness = { type = "float", default = 0.5, min = 0, max = 1 },
        damping = { type = "float", default = 0.3, min = 0, max = 1 },
        gravity = { type = "vector3", default = Vector3(0, -9.8, 0) },
    },

    inputs = {
        pose = { type = "pose", required = true },
    },

    outputs = {
        pose = { type = "pose" },
    },

    -- 节点更新逻辑
    update = function(self, dt, context)
        local inputPose = self:GetInput("pose")
        local outputPose = inputPose:Clone()

        for _, boneName in ipairs(self.properties.bones) do
            local bone = outputPose:GetBone(boneName)
            -- 应用弹簧物理
            self:ApplySpringPhysics(bone, dt)
        end

        self:SetOutput("pose", outputPose)
    end,
})
```

---

## 7. 完整示例

### 7.1 第三人称角色动画系统

```lua
-- CharacterAnimator.lua
-- 完整的第三人称角色动画系统示例

local CharacterAnimator = class("CharacterAnimator")

function CharacterAnimator:Initialize(animatedModel, character)
    self.model = animatedModel
    self.character = character

    -- 创建移动混合空间
    self.moveBlendSpace = BlendSpace2D.new({
        name = "Movement",
        parameterX = "direction",
        parameterY = "speed",
        points = {
            { x = 0, y = 0, animation = "Idle.ani" },
            { x = 0, y = 2, animation = "WalkFwd.ani" },
            { x = 90, y = 2, animation = "WalkRight.ani" },
            { x = -90, y = 2, animation = "WalkLeft.ani" },
            { x = 180, y = 2, animation = "WalkBwd.ani" },
            { x = 0, y = 5, animation = "RunFwd.ani" },
            { x = 90, y = 5, animation = "RunRight.ani" },
            { x = -90, y = 5, animation = "RunLeft.ani" },
            { x = 180, y = 5, animation = "RunBwd.ani" },
        },
    })

    -- 创建基础状态机
    self.locomotionFSM = AnimationStateMachine.new({
        name = "Locomotion",
        defaultState = "Movement",
        blendTime = 0.2,

        parameters = {
            speed = { type = "float", default = 0 },
            direction = { type = "float", default = 0 },
            isGrounded = { type = "bool", default = true },
            jumpTrigger = { type = "trigger" },
            landTrigger = { type = "trigger" },
        },

        states = {
            {
                name = "Movement",
                animation = self.moveBlendSpace,
                loop = true,
            },
            {
                name = "JumpStart",
                animation = "JumpStart.ani",
                loop = false,
                rootMotion = { enabled = false },
            },
            {
                name = "Falling",
                animation = "Falling.ani",
                loop = true,
                rootMotion = { enabled = false },
            },
            {
                name = "Land",
                animation = "Land.ani",
                loop = false,
                blendInTime = 0.1,
            },
        },

        transitions = {
            { from = "Movement", to = "JumpStart", condition = "jumpTrigger" },
            { from = "JumpStart", to = "Falling", condition = "true", exitTime = 1.0 },
            { from = "Movement", to = "Falling", condition = "not isGrounded", priority = 5 },
            { from = "Falling", to = "Land", condition = "landTrigger" },
            { from = "Land", to = "Movement", condition = "true", exitTime = 0.7 },
        },
    })

    -- 创建上半身状态机 (攻击等)
    self.upperBodyFSM = AnimationStateMachine.new({
        name = "UpperBody",
        defaultState = "Empty",

        parameters = {
            attackTrigger = { type = "trigger" },
            reloadTrigger = { type = "trigger" },
        },

        states = {
            { name = "Empty", animation = nil },  -- 空状态
            {
                name = "Attack",
                animation = "SwordAttack.ani",
                loop = false,
                events = {
                    { name = "DamageStart", time = 0.3, normalized = true },
                    { name = "DamageEnd", time = 0.5, normalized = true },
                },
            },
            {
                name = "Reload",
                animation = "Reload.ani",
                loop = false,
            },
        },

        transitions = {
            { from = "Empty", to = "Attack", condition = "attackTrigger" },
            { from = "Attack", to = "Empty", condition = "true", exitTime = 1.0 },
            { from = "Empty", to = "Reload", condition = "reloadTrigger" },
            { from = "Reload", to = "Empty", condition = "true", exitTime = 1.0 },
        },
    })

    -- 创建层控制器
    self.layerController = AnimationLayerController.new({
        name = "CharacterLayers",

        layers = {
            {
                name = "Base",
                index = 0,
                blendMode = "override",
                mask = AvatarMask.FullBody,
                stateMachine = self.locomotionFSM,
            },
            {
                name = "UpperBody",
                index = 1,
                blendMode = "override",
                weight = 1.0,
                mask = AvatarMask.UpperBody,
                stateMachine = self.upperBodyFSM,
            },
        },
    })

    -- 绑定到模型
    self.layerController:Bind(self.model)

    -- 注册事件处理
    self:RegisterEventHandlers()
end

function CharacterAnimator:RegisterEventHandlers()
    self.layerController:RegisterEventHandler("DamageStart", function(event, animator)
        self.character:EnableWeaponDamage(true)
    end)

    self.layerController:RegisterEventHandler("DamageEnd", function(event, animator)
        self.character:EnableWeaponDamage(false)
    end)
end

function CharacterAnimator:Update(dt)
    local velocity = self.character:GetVelocity()
    local speed = Vector3(velocity.x, 0, velocity.z):Length()
    local direction = self.character:GetMoveDirection()
    local isGrounded = self.character:IsGrounded()

    -- 更新参数
    self.locomotionFSM:SetFloat("speed", speed)
    self.locomotionFSM:SetFloat("direction", direction)
    self.locomotionFSM:SetBool("isGrounded", isGrounded)

    -- 更新状态机
    self.layerController:Update(dt)
end

-- 外部调用接口
function CharacterAnimator:Jump()
    self.locomotionFSM:SetTrigger("jumpTrigger")
end

function CharacterAnimator:Land()
    self.locomotionFSM:SetTrigger("landTrigger")
end

function CharacterAnimator:Attack()
    self.upperBodyFSM:SetTrigger("attackTrigger")
end

function CharacterAnimator:Reload()
    self.upperBodyFSM:SetTrigger("reloadTrigger")
end

function CharacterAnimator:IsAttacking()
    return self.upperBodyFSM:IsInState("Attack")
end

return CharacterAnimator
```

### 7.2 AI 生成动画配置示例

AI 可以根据需求直接生成以下配置：

```lua
-- AI Prompt: "创建一个 NPC 巡逻动画系统，包含待机、行走、警觉、追击状态"

local npcPatrolFSM = AnimationStateMachine.new({
    name = "NPCPatrol",
    defaultState = "Idle",
    blendTime = 0.3,

    parameters = {
        speed = { type = "float", default = 0 },
        alertLevel = { type = "float", default = 0, min = 0, max = 1 },
        hasTarget = { type = "bool", default = false },
        isSearching = { type = "bool", default = false },
    },

    states = {
        {
            name = "Idle",
            animation = "NPC_Idle.ani",
            loop = true,
            onEnter = function(self, fsm)
                fsm.owner:StartIdleBehavior()
            end,
        },
        {
            name = "Patrol",
            animation = "NPC_Walk.ani",
            loop = true,
            rootMotion = { enabled = true },
        },
        {
            name = "Alert",
            animation = "NPC_AlertIdle.ani",
            loop = true,
            onEnter = function(self, fsm)
                fsm.owner:PlaySound("AlertSound")
            end,
        },
        {
            name = "Search",
            animation = "NPC_SearchWalk.ani",
            loop = true,
            rootMotion = { enabled = true },
        },
        {
            name = "Chase",
            animation = "NPC_Run.ani",
            loop = true,
            rootMotion = { enabled = true },
        },
    },

    transitions = {
        -- 正常巡逻
        { from = "Idle", to = "Patrol", condition = "speed > 0.1" },
        { from = "Patrol", to = "Idle", condition = "speed <= 0.1" },

        -- 警觉状态
        { from = {"Idle", "Patrol"}, to = "Alert", condition = "alertLevel > 0.3 and not hasTarget" },
        { from = "Alert", to = "Idle", condition = "alertLevel <= 0.1" },
        { from = "Alert", to = "Search", condition = "isSearching" },
        { from = "Search", to = "Alert", condition = "not isSearching and not hasTarget" },

        -- 追击状态
        { from = {"Alert", "Search"}, to = "Chase", condition = "hasTarget", priority = 10 },
        { from = "Chase", to = "Search", condition = "not hasTarget" },

        -- 紧急发现目标
        { from = {"Idle", "Patrol"}, to = "Chase", condition = "hasTarget and alertLevel > 0.8", priority = 20 },
    },
})
```

---

## 8. C++ 实现指南

### 8.0 架构决策：包装而非替换

新动画系统采用**包装模式**，在现有 `AnimationController` 基础上构建高层 API。

#### 架构图

```
┌───────────────────────────────────────────────────────────┐
│                    用户代码 (Lua/C++)                      │
└───────────────────────────────────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────────┐
│  新系统 (高层 API)                                        │
│  ┌─────────────────┐ ┌─────────────────┐ ┌────────────┐ │
│  │StateMachine     │ │BlendSpace       │ │Parameter   │ │
│  │- 状态管理       │ │- 1D/2D 混合     │ │Context     │ │
│  │- 条件转换       │ │- 权重计算       │ │- 参数表    │ │
│  │- 事件触发       │ │- 采样插值       │ │- 条件求值  │ │
│  └─────────────────┘ └─────────────────┘ └────────────┘ │
└───────────────────────────────────────────────────────────┘
                           │ 调用
                           ▼
┌───────────────────────────────────────────────────────────┐
│  原有系统 (底层引擎) - 保留复用                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │              AnimationController                     │ │
│  │  - Play / PlayExclusive    - SetWeight              │ │
│  │  - Fade / FadeOthers       - SetTime / SetSpeed     │ │
│  │  - Layer 管理 (0-255)      - SetStartBone (蒙版)    │ │
│  └─────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │              AnimatedModel                           │ │
│  │  - 骨骼变换       - 蒙皮计算       - 动画资源管理   │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘
```

#### 职责划分

| 层级 | 组件 | 职责 |
|------|------|------|
| **高层** | AnimationStateMachine | 状态逻辑、条件转换、参数管理 |
| **高层** | BlendSpace | 多动画混合权重计算 |
| **高层** | ParameterContext | 参数存储、条件表达式求值 |
| **底层** | AnimationController | 动画播放、时间控制、层混合 |
| **底层** | AnimatedModel | 骨骼变换、蒙皮渲染 |

#### 选择包装模式的原因

```
✅ 复用成熟代码
   - AnimationController 已经处理了复杂的混合、淡入淡出、层管理
   - 避免重复实现底层逻辑

✅ 降低风险
   - 底层动画系统已经过验证，稳定可靠
   - 新系统 bug 不会影响底层播放逻辑

✅ 渐进式迁移
   - 新旧 API 可以共存
   - 现有项目可以逐步迁移

✅ 保持灵活性
   - 特殊情况下可以直接使用 AnimationController
   - 不强制所有场景都走状态机
```

#### 组件关系

```cpp
// 新组件持有原有组件的引用
class AnimationStateMachine : public Component
{
private:
    // 包装而非替换
    WeakPtr<AnimationController> animController_;
    WeakPtr<AnimatedModel> animatedModel_;

    // 新增功能
    SharedPtr<ParameterContext> paramContext_;
    HashMap<String, StateDefinition> states_;
    Vector<TransitionDefinition> transitions_;
};
```

#### 典型调用流程

```cpp
void AnimationStateMachine::Update(float timeStep)
{
    // 1. 新系统: 求值条件，决定状态转换
    EvaluateTransitions();

    // 2. 新系统: 计算 BlendSpace 权重 (如果是 BlendSpace 状态)
    Vector<AnimationWeight> weights;
    if (currentState_.blendSpace)
        weights = currentState_.blendSpace->Sample(paramContext_);

    // 3. 调用原有系统: 执行实际的动画播放
    if (weights.Size() > 0)
    {
        for (const auto& w : weights)
        {
            animController_->Play(w.animation, currentState_.layer, true, blendTime_);
            animController_->SetWeight(w.animation, w.weight);
        }
    }
    else
    {
        animController_->PlayExclusive(
            currentState_.animation,
            currentState_.layer,
            currentState_.loop,
            blendTime_
        );
    }

    // 4. 新系统: 触发动画事件
    ProcessAnimationEvents(timeStep);
}
```

#### 用户可同时使用两套 API

```lua
-- 获取组件
local fsm = node:GetComponent("AnimationStateMachine")
local ctrl = node:GetComponent("AnimationController")

-- 日常使用: 高层 API
fsm:SetFloat("speed", 5.0)
fsm:SetTrigger("jump")

-- 特殊需求: 直接访问底层 API
ctrl:SetTime("HitReaction.ani", 0.0)   -- 重置动画时间
ctrl:SetSpeed("Walk.ani", 1.5)         -- 调整播放速度
ctrl:GetAnimationState("Run.ani")      -- 获取底层状态
```

### 8.1 核心类结构

```cpp
// AnimationStateMachine.h
namespace Urho3D
{

/// Animation parameter types
enum class AnimParamType
{
    Float,
    Int,
    Bool,
    Trigger
};

/// Animation parameter
struct AnimationParameter
{
    String name;
    AnimParamType type;
    Variant value;
    Variant defaultValue;
    float minValue = 0.0f;
    float maxValue = 1.0f;
};

/// Animation state definition
struct AnimationStateDefinition
{
    String name;
    String animationPath;          // or BlendSpace reference
    bool loop = true;
    float speed = 1.0f;
    float blendInTime = -1.0f;     // -1 means use default
    float blendOutTime = -1.0f;
    bool rootMotionEnabled = true;
    Vector<AnimationEventDef> events;
};

/// Animation transition definition
struct AnimationTransitionDefinition
{
    StringVector fromStates;       // "*" for any state
    String toState;
    String condition;              // Expression string
    int priority = 0;
    float blendTime = -1.0f;
    float exitTime = -1.0f;        // -1 means immediate
    bool interruptible = true;
};

/// Condition expression evaluator
class URHO3D_API ConditionExpression
{
public:
    static SharedPtr<ConditionExpression> Parse(const String& expression);
    bool Evaluate(const HashMap<String, AnimationParameter>& parameters) const;

private:
    // AST nodes for expression tree
    struct Node;
    SharedPtr<Node> root_;
};

/// Animation State Machine component
class URHO3D_API AnimationStateMachine : public Component
{
    URHO3D_OBJECT(AnimationStateMachine, Component);

public:
    explicit AnimationStateMachine(Context* context);
    ~AnimationStateMachine() override;

    static void RegisterObject(Context* context);

    // Configuration (from Lua table)
    void LoadFromLuaTable(lua_State* L, int tableIndex);
    void LoadFromJSON(const JSONValue& json);

    // Parameter API
    void SetFloat(const String& name, float value);
    void SetInt(const String& name, int value);
    void SetBool(const String& name, bool value);
    void SetTrigger(const String& name);

    float GetFloat(const String& name) const;
    int GetInt(const String& name) const;
    bool GetBool(const String& name) const;

    // State API
    const String& GetCurrentState() const { return currentState_; }
    bool IsInState(const String& stateName) const;
    float GetStateTime() const { return stateTime_; }
    float GetNormalizedTime() const;
    void ForceState(const String& stateName);

    // Dynamic modification
    void AddState(const AnimationStateDefinition& state);
    void RemoveState(const String& stateName);
    void AddTransition(const AnimationTransitionDefinition& transition);
    void RemoveTransitionsTo(const String& stateName);

    // Update
    void Update(float timeStep);

    // Root Motion
    Vector3 GetRootMotionDeltaPosition() const;
    Quaternion GetRootMotionDeltaRotation() const;

protected:
    void OnNodeSet(Node* node) override;

private:
    void EvaluateTransitions();
    void TransitionToState(const String& newState, float blendTime);
    void ResetTriggers();

    // State definitions
    HashMap<String, AnimationStateDefinition> states_;
    Vector<AnimationTransitionDefinition> transitions_;
    HashMap<String, AnimationParameter> parameters_;

    // Runtime state
    String currentState_;
    String previousState_;
    float stateTime_ = 0.0f;
    float transitionTime_ = 0.0f;
    float transitionDuration_ = 0.0f;

    // Cached components
    WeakPtr<AnimatedModel> animatedModel_;
    WeakPtr<AnimationController> animController_;

    // Condition evaluators (cached)
    HashMap<String, SharedPtr<ConditionExpression>> conditionCache_;
};

} // namespace Urho3D
```

### 8.2 Lua 绑定

```cpp
// AnimationStateMachineLua.cpp
static void RegisterAnimationStateMachine(lua_State* L)
{
    // AnimationStateMachine class
    luabridge::getGlobalNamespace(L)
        .beginNamespace("Urho3D")
        .beginClass<AnimationStateMachine>("AnimationStateMachine")
            // Factory
            .addStaticFunction("new", &CreateFromLuaTable)

            // Parameter setters
            .addFunction("SetFloat", &AnimationStateMachine::SetFloat)
            .addFunction("SetInt", &AnimationStateMachine::SetInt)
            .addFunction("SetBool", &AnimationStateMachine::SetBool)
            .addFunction("SetTrigger", &AnimationStateMachine::SetTrigger)

            // Parameter getters
            .addFunction("GetFloat", &AnimationStateMachine::GetFloat)
            .addFunction("GetInt", &AnimationStateMachine::GetInt)
            .addFunction("GetBool", &AnimationStateMachine::GetBool)

            // State queries
            .addFunction("GetCurrentState", &AnimationStateMachine::GetCurrentState)
            .addFunction("IsInState", &AnimationStateMachine::IsInState)
            .addFunction("GetStateTime", &AnimationStateMachine::GetStateTime)
            .addFunction("GetNormalizedTime", &AnimationStateMachine::GetNormalizedTime)
            .addFunction("ForceState", &AnimationStateMachine::ForceState)

            // Dynamic modification
            .addFunction("AddState", &AnimationStateMachine::AddStateFromLua)
            .addFunction("RemoveState", &AnimationStateMachine::RemoveState)
            .addFunction("AddTransition", &AnimationStateMachine::AddTransitionFromLua)

            // Binding
            .addFunction("Bind", &AnimationStateMachine::BindToModel)
            .addFunction("Update", &AnimationStateMachine::Update)

            // Root Motion
            .addFunction("GetRootMotionDeltaPosition", &AnimationStateMachine::GetRootMotionDeltaPosition)
            .addFunction("GetRootMotionDeltaRotation", &AnimationStateMachine::GetRootMotionDeltaRotation)
        .endClass()
        .endNamespace();
}

// Helper to create from Lua table
static AnimationStateMachine* CreateFromLuaTable(lua_State* L)
{
    // Expect table at top of stack
    if (!lua_istable(L, -1))
    {
        luaL_error(L, "AnimationStateMachine.new expects a table");
        return nullptr;
    }

    auto* context = GetContext(L);
    auto* fsm = new AnimationStateMachine(context);
    fsm->LoadFromLuaTable(L, lua_gettop(L));

    return fsm;
}
```

### 8.3 条件表达式解析器

```cpp
// ConditionExpression.cpp
// Simple expression parser supporting: and, or, not, >, <, >=, <=, ==, !=, (, )

class ExpressionParser
{
public:
    SharedPtr<ConditionExpression::Node> Parse(const String& expr)
    {
        tokens_ = Tokenize(expr);
        pos_ = 0;
        return ParseOr();
    }

private:
    Vector<Token> Tokenize(const String& expr);
    SharedPtr<Node> ParseOr();      // or
    SharedPtr<Node> ParseAnd();     // and
    SharedPtr<Node> ParseNot();     // not
    SharedPtr<Node> ParseCompare(); // >, <, >=, <=, ==, !=
    SharedPtr<Node> ParsePrimary(); // literals, identifiers, parentheses

    Vector<Token> tokens_;
    unsigned pos_ = 0;
};

bool ConditionExpression::Evaluate(const HashMap<String, AnimationParameter>& params) const
{
    return root_->Evaluate(params);
}

// Node types
struct ConditionExpression::Node
{
    virtual bool Evaluate(const HashMap<String, AnimationParameter>& params) const = 0;
};

struct BinaryOpNode : public Node
{
    enum Op { And, Or, Greater, Less, GreaterEq, LessEq, Equal, NotEqual };
    Op op;
    SharedPtr<Node> left, right;

    bool Evaluate(const HashMap<String, AnimationParameter>& params) const override
    {
        switch (op)
        {
        case And: return left->Evaluate(params) && right->Evaluate(params);
        case Or: return left->Evaluate(params) || right->Evaluate(params);
        // ... other operators
        }
    }
};

struct UnaryOpNode : public Node
{
    enum Op { Not };
    Op op;
    SharedPtr<Node> operand;

    bool Evaluate(const HashMap<String, AnimationParameter>& params) const override
    {
        if (op == Not)
            return !operand->Evaluate(params);
        return false;
    }
};

struct ParameterNode : public Node
{
    String paramName;

    bool Evaluate(const HashMap<String, AnimationParameter>& params) const override
    {
        auto it = params.Find(paramName);
        if (it != params.End())
        {
            if (it->second_.type == AnimParamType::Bool ||
                it->second_.type == AnimParamType::Trigger)
                return it->second_.value.GetBool();
            return it->second_.value.GetFloat() != 0.0f;
        }
        return false;
    }
};

struct LiteralNode : public Node
{
    Variant value;

    bool Evaluate(const HashMap<String, AnimationParameter>& params) const override
    {
        return value.GetBool();
    }
};
```

---

## 9. 调试支持

动画系统的调试支持是开发效率的关键。本章节设计了完整的调试工具链。

### 9.1 核心设计理念

```
┌─────────────────────────────────────────────────────────┐
│                    调试系统架构                          │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ 参数监视器  │  │ 状态可视化  │  │ 性能分析器  │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
│         │                │                │            │
│         └────────────────┼────────────────┘            │
│                          ▼                             │
│              ┌───────────────────┐                     │
│              │   AnimDebugger    │                     │
│              └───────────────────┘                     │
│                          │                             │
│         ┌────────────────┼────────────────┐           │
│         ▼                ▼                ▼           │
│    Console 输出     ImGui 面板      日志文件          │
└─────────────────────────────────────────────────────────┘
```

### 9.2 参数监视 API

```lua
---@class AnimationDebugger
---@field enabled boolean 是否启用调试
---@field logLevel "none"|"error"|"warning"|"info"|"verbose" 日志级别
---@field showOverlay boolean 是否显示屏幕覆盖层

-- 启用调试模式
fsm:SetDebugEnabled(true)

-- 打印当前所有参数
fsm:DebugPrintParameters()
-- 输出:
-- [AnimFSM:CharacterLocomotion] Parameters:
--   speed: 5.23 (float)
--   direction: 45.0 (float)
--   isGrounded: true (bool)
--   isJumping: false (trigger)

-- 监视特定参数变化
fsm:WatchParameter("speed", function(name, oldValue, newValue)
    print(string.format("[%s] %s: %.2f -> %.2f", os.time(), name, oldValue, newValue))
end)

-- 参数变化历史记录
fsm:EnableParameterHistory(true, 300)  -- 记录最近 300 帧
local history = fsm:GetParameterHistory("speed")
-- history = { {frame=1, value=0}, {frame=2, value=0.5}, ... }

-- 导出参数快照
local snapshot = fsm:ExportParameterSnapshot()
-- snapshot = { speed=5.23, direction=45.0, isGrounded=true, ... }

-- 导入参数快照 (用于重现问题)
fsm:ImportParameterSnapshot(snapshot)
```

### 9.3 状态转换调试

```lua
-- 打印当前状态信息
fsm:DebugPrintState()
-- 输出:
-- [AnimFSM:CharacterLocomotion] State:
--   Current: "Walk"
--   Previous: "Idle"
--   State Time: 1.234s
--   Normalized Time: 0.45
--   Is Transitioning: false

-- 监听状态转换事件
fsm:OnStateChanged(function(fromState, toState, transitionInfo)
    print(string.format("[StateChange] %s -> %s (blend: %.2fs)",
        fromState, toState, transitionInfo.blendTime))
end)

-- 打印所有可能的转换
fsm:DebugPrintTransitions()
-- 输出:
-- [AnimFSM:CharacterLocomotion] Transitions from "Walk":
--   -> "Idle" when "speed <= 0.1" [priority: 0]
--   -> "Run" when "speed > 3.0" [priority: 0]
--   -> "JumpStart" when "isJumping" [priority: 10]

-- 条件表达式调试
fsm:DebugEvaluateCondition("speed > 3.0 and isGrounded")
-- 输出:
-- [ConditionEval] "speed > 3.0 and isGrounded"
--   speed (5.23) > 3.0 → true
--   isGrounded → true
--   Result: true AND true → true

-- 转换历史记录
fsm:EnableTransitionHistory(true, 100)  -- 记录最近 100 次转换
local history = fsm:GetTransitionHistory()
-- history = {
--   { frame=100, from="Idle", to="Walk", condition="speed > 0.1", time=1.5 },
--   { frame=250, from="Walk", to="Run", condition="speed > 3.0", time=2.8 },
--   ...
-- }
```

### 9.4 可视化调试覆盖层

```lua
-- 启用屏幕覆盖层调试信息
fsm:SetDebugOverlay(true, {
    position = Vector2(10, 10),      -- 屏幕位置
    showParameters = true,            -- 显示参数
    showState = true,                 -- 显示状态
    showTransitions = true,           -- 显示可用转换
    showBlendWeights = true,          -- 显示混合权重
    fontSize = 14,
    backgroundColor = Color(0, 0, 0, 0.7),
})

-- 屏幕显示效果:
-- ┌─────────────────────────────────┐
-- │ [CharacterLocomotion]           │
-- │ State: Walk (1.23s)             │
-- │ ─────────────────────────       │
-- │ Parameters:                     │
-- │   speed: 2.45                   │
-- │   direction: 30.0               │
-- │   isGrounded: true              │
-- │ ─────────────────────────       │
-- │ Available Transitions:          │
-- │   → Idle (speed <= 0.1) ✗       │
-- │   → Run (speed > 3.0) ✗         │
-- │   → Jump (isJumping) ✗          │
-- │ ─────────────────────────       │
-- │ Blend Weights:                  │
-- │   Walk.ani: 1.0                 │
-- └─────────────────────────────────┘
```

### 9.5 骨骼与动画可视化

```lua
-- 骨骼调试显示
animator:SetDebugDrawSkeleton(true, {
    showBones = true,           -- 显示骨骼连线
    showBoneNames = true,       -- 显示骨骼名称
    showBoneAxes = true,        -- 显示骨骼坐标轴
    boneColor = Color.GREEN,
    selectedBoneColor = Color.YELLOW,
    axisLength = 0.1,
})

-- IK 调试显示
animator:SetDebugDrawIK(true, {
    showTargets = true,         -- 显示 IK 目标
    showChains = true,          -- 显示 IK 链
    showConstraints = true,     -- 显示约束范围
    targetColor = Color.RED,
    chainColor = Color.CYAN,
})

-- Root Motion 调试显示
animator:SetDebugDrawRootMotion(true, {
    showPath = true,            -- 显示运动轨迹
    showVelocity = true,        -- 显示速度向量
    pathLength = 60,            -- 轨迹帧数
    pathColor = Color.MAGENTA,
})

-- Blend Space 调试显示
blendSpace:SetDebugDraw(true, {
    showGrid = true,            -- 显示混合网格
    showPoints = true,          -- 显示采样点
    showCurrentPosition = true, -- 显示当前位置
    showWeights = true,         -- 显示各点权重
})

-- 屏幕绘制 Blend Space 2D 图
-- ┌─────────────────────────┐
-- │ Speed ▲                 │
-- │   6   │ ○   ○   ○      │
-- │       │                 │
-- │   3   │ ○   ●   ○      │  ← ● 当前位置
-- │       │     ↑           │
-- │   0   │     ○           │
-- │       └──────────► Dir  │
-- │        -90  0  90       │
-- └─────────────────────────┘
```

### 9.6 性能分析

```lua
-- 启用性能分析
fsm:SetProfilingEnabled(true)

-- 获取性能数据
local stats = fsm:GetProfilingStats()
-- stats = {
--   updateTime = 0.15,           -- Update 耗时 (ms)
--   conditionEvalTime = 0.05,    -- 条件求值耗时 (ms)
--   conditionEvalCount = 12,     -- 条件求值次数
--   blendingTime = 0.08,         -- 混合计算耗时 (ms)
--   activeAnimations = 3,        -- 活跃动画数
--   totalBones = 65,             -- 总骨骼数
--   animatedBones = 45,          -- 受动画影响的骨骼数
-- }

-- 打印性能报告
fsm:DebugPrintProfilingReport()
-- 输出:
-- [AnimFSM:CharacterLocomotion] Performance Report:
--   Update Time: 0.15ms (avg), 0.23ms (max)
--   Condition Evaluations: 12/frame
--   Active Animations: 3
--   Memory Usage: 2.3 KB
--
-- Hot Conditions (evaluated most often):
--   1. "speed > 0.1" - 4 times/frame
--   2. "isGrounded" - 3 times/frame

-- 动画混合权重分析
animator:DebugPrintBlendReport()
-- 输出:
-- [Animator] Blend Report:
--   Layer 0 (Base):
--     Walk.ani: weight=0.7, time=1.23s
--     Run.ani: weight=0.3, time=0.89s
--   Layer 1 (UpperBody):
--     Attack.ani: weight=1.0, time=0.45s
```

### 9.7 日志与录制

```lua
-- 配置日志输出
AnimationDebugger.SetLogConfig({
    level = "info",                    -- none, error, warning, info, verbose
    outputConsole = true,              -- 输出到控制台
    outputFile = true,                 -- 输出到文件
    filePath = "Logs/animation.log",   -- 日志文件路径
    includeTimestamp = true,           -- 包含时间戳
    includeFrameNumber = true,         -- 包含帧号
})

-- 日志输出示例:
-- [2025-12-25 10:30:45.123] [Frame:1234] [INFO] [CharacterLocomotion] State: Idle -> Walk
-- [2025-12-25 10:30:45.456] [Frame:1245] [INFO] [CharacterLocomotion] Param: speed = 3.5
-- [2025-12-25 10:30:45.789] [Frame:1256] [WARN] [CharacterLocomotion] Transition blocked: no valid path

-- 录制回放功能
fsm:StartRecording()
-- ... 游戏运行 ...
fsm:StopRecording()
local recording = fsm:GetRecording()

-- 保存录制数据
recording:SaveToFile("Recordings/animation_debug_001.json")

-- 加载并回放
local playback = AnimationRecording.LoadFromFile("Recordings/animation_debug_001.json")
playback:Play(fsm, {
    speed = 1.0,           -- 回放速度
    loop = false,          -- 是否循环
    startFrame = 0,        -- 起始帧
    endFrame = -1,         -- 结束帧 (-1 = 到末尾)
})

-- 逐帧调试
playback:Pause()
playback:StepForward()     -- 前进一帧
playback:StepBackward()    -- 后退一帧
playback:SeekToFrame(100)  -- 跳转到指定帧
```

### 9.8 断言与验证

```lua
-- 状态机配置验证
local errors = fsm:Validate()
if #errors > 0 then
    for _, err in ipairs(errors) do
        print("[ValidationError] " .. err)
    end
end
-- 可能的错误:
-- [ValidationError] State "Idle" referenced in transition but not defined
-- [ValidationError] Condition "speeed > 0" has unknown parameter "speeed"
-- [ValidationError] Circular transition detected: Walk -> Run -> Walk (with same conditions)

-- 运行时断言
fsm:SetAssertions({
    -- 断言: speed 不应该是负数
    { condition = "speed >= 0", message = "Speed should not be negative!" },
    -- 断言: 死亡状态应该是最终状态
    { condition = "not (currentState == 'Death' and stateTime > 5)",
      message = "Stuck in Death state for too long!" },
})

-- 断言触发时的回调
fsm:OnAssertionFailed(function(assertion, currentParams)
    print("[ASSERTION FAILED] " .. assertion.message)
    print("Current parameters: " .. json.encode(currentParams))
    -- 可选: 暂停游戏、保存快照等
end)
```

### 9.9 条件表达式错误处理

条件表达式是字符串，存在语法错误的可能。系统提供完善的错误报告机制。

#### 错误类型

```cpp
enum class ConditionErrorType
{
    None,                    // 无错误
    SyntaxError,             // 语法错误
    UnknownParameter,        // 未知参数
    TypeMismatch,            // 类型不匹配
    DivisionByZero,          // 除零错误
    InvalidOperator,         // 无效运算符
    UnbalancedParentheses,   // 括号不匹配
    InvalidFunctionCall,     // 无效函数调用
};

struct ConditionError
{
    ConditionErrorType type;
    String message;          // 错误描述
    String expression;       // 原始表达式
    int position;            // 错误位置 (字符索引)
    String suggestion;       // 修复建议
};
```

#### 解析时错误报告

```lua
-- 创建状态机时验证所有条件表达式
local fsm = AnimationStateMachine.new({
    -- ...
    transitions = {
        { from = "Idle", to = "Walk", condition = "speed >> 0.1" },  -- 语法错误
        { from = "Walk", to = "Run",  condition = "speeed > 3.0" },  -- 拼写错误
    },
    parameters = {
        speed = { type = "float", default = 0 },
    },
})

-- 自动输出解析错误:
-- [ConditionError] Syntax error in "speed >> 0.1"
--                                        ^^ (position: 6)
--   Invalid operator '>>'
--   Suggestion: Did you mean '>' or '>='?
--
-- [ConditionError] Unknown parameter in "speeed > 3.0"
--                                         ^^^^^^ (position: 0)
--   Parameter 'speeed' is not defined
--   Suggestion: Did you mean 'speed'?

-- 手动验证表达式
local result, error = ConditionExpression.Validate("speed > 3.0 and", parameters)
if error then
    print(error.message)     -- "Unexpected end of expression after 'and'"
    print(error.position)    -- 16
    print(error.suggestion)  -- "Expression incomplete, expected value after 'and'"
end
```

#### 运行时错误处理

```lua
-- 配置错误处理策略
fsm:SetErrorHandling({
    -- 解析错误策略
    onParseError = "log_and_disable",  -- "throw", "log_and_disable", "log_and_ignore"

    -- 求值错误策略
    onEvalError = "return_false",      -- "throw", "return_false", "return_true"

    -- 错误回调
    onError = function(error)
        -- 自定义处理
        Logger:Error("[AnimFSM] %s: %s", error.type, error.message)

        -- 开发模式下暂停游戏
        if IS_DEBUG then
            Debug:Pause()
            Debug:ShowErrorDialog(error)
        end
    end,
})

-- 运行时类型错误示例
fsm:SetFloat("isGrounded", 1.0)  -- 错误: isGrounded 是 bool 类型
-- 输出:
-- [ConditionWarning] Type mismatch for parameter 'isGrounded'
--   Expected: bool, Got: float (1.0)
--   Auto-converted: 1.0 -> true

-- 严格模式 (禁止自动类型转换)
fsm:SetStrictMode(true)
fsm:SetFloat("isGrounded", 1.0)
-- 抛出错误:
-- [ConditionError] Type mismatch: cannot assign float to bool parameter 'isGrounded'
```

#### 错误恢复与降级

```lua
-- 表达式解析失败时的降级策略
local fsm = AnimationStateMachine.new({
    transitions = {
        {
            from = "Idle",
            to = "Walk",
            condition = "speed > 0.1",
            -- 备用条件 (主条件解析失败时使用)
            fallbackCondition = "true",
        },
    },

    -- 全局降级策略
    errorFallback = {
        -- 解析失败的条件默认返回 false (不触发转换)
        parseErrorResult = false,
        -- 求值失败的条件默认返回 false
        evalErrorResult = false,
    },
})
```

#### 开发工具集成

```lua
-- IDE 风格的错误提示 (用于编辑器集成)
local diagnostics = fsm:GetDiagnostics()
for _, diag in ipairs(diagnostics) do
    print(string.format("%s:%d:%d: %s: %s",
        diag.source,      -- "transition[2].condition"
        diag.line,        -- 1
        diag.column,      -- 7
        diag.severity,    -- "error" / "warning" / "hint"
        diag.message      -- "Unknown parameter 'speeed'"
    ))
end

-- 输出 (LSP 兼容格式):
-- transition[2].condition:1:1: error: Unknown parameter 'speeed'
-- transition[2].condition:1:1: hint: Did you mean 'speed'?
```

### 9.10 动画资源 Fallback 策略

当动画资源缺失或加载失败时，系统提供多级 fallback 机制确保游戏不崩溃。

#### Fallback 层级

```
┌─────────────────────────────────────────────────────────┐
│              Animation Resource Fallback                │
│                                                         │
│  Level 1: 指定动画资源                                  │
│     ↓ (加载失败)                                        │
│  Level 2: 状态定义的 fallbackAnimation                  │
│     ↓ (未定义或加载失败)                                │
│  Level 3: 状态机全局 defaultAnimation                   │
│     ↓ (未定义或加载失败)                                │
│  Level 4: 系统内置 T-Pose / Bind Pose                  │
│     ↓ (骨骼不匹配)                                      │
│  Level 5: 冻结当前姿势 (不播放动画)                     │
└─────────────────────────────────────────────────────────┘
```

#### 状态级 Fallback

```lua
local fsm = AnimationStateMachine.new({
    states = {
        {
            name = "Walk",
            animation = "Animations/Character/Walk.ani",
            -- 主动画加载失败时的备选
            fallbackAnimation = "Animations/Character/Idle.ani",
            -- 备选也失败时的行为
            fallbackBehavior = "use_default",  -- "use_default", "freeze", "hide"
        },
        {
            name = "SpecialAttack",
            animation = "Animations/Character/SpecialAttack.ani",
            -- 可以指定多个备选 (按顺序尝试)
            fallbackAnimations = {
                "Animations/Character/Attack.ani",
                "Animations/Character/Idle.ani",
            },
        },
    },

    -- 状态机全局默认动画
    defaultAnimation = "Animations/Character/Idle.ani",

    -- 全局 fallback 行为
    fallbackBehavior = "freeze",  -- 所有 fallback 都失败时冻结姿势
})
```

#### 资源加载错误处理

```lua
-- 配置资源加载策略
fsm:SetResourceLoadingConfig({
    -- 预加载所有动画 (启动时)
    preloadAll = true,

    -- 异步加载
    asyncLoading = true,

    -- 加载超时 (毫秒)
    loadTimeout = 5000,

    -- 加载失败时的回调
    onLoadFailed = function(resourcePath, error)
        Logger:Warning("[AnimFSM] Failed to load animation: %s", resourcePath)
        Logger:Warning("  Error: %s", error.message)

        -- 返回 fallback 资源路径，或 nil 使用默认策略
        return nil
    end,

    -- 资源热重载支持 (开发模式)
    hotReload = IS_DEBUG,
    onHotReload = function(resourcePath)
        Logger:Info("[AnimFSM] Animation reloaded: %s", resourcePath)
    end,
})
```

#### 运行时资源检查

```lua
-- 验证所有动画资源是否存在
local missing = fsm:ValidateResources()
if #missing > 0 then
    for _, res in ipairs(missing) do
        print(string.format("[Missing] %s (used in state '%s')",
            res.path, res.stateName))
    end
end
-- 输出:
-- [Missing] Animations/Character/SpecialAttack.ani (used in state 'SpecialAttack')
-- [Missing] Animations/Character/Taunt.ani (used in state 'Taunt')

-- 运行时资源状态查询
local status = fsm:GetResourceStatus("Animations/Character/Walk.ani")
-- status = {
--   path = "Animations/Character/Walk.ani",
--   state = "loaded",        -- "loading", "loaded", "failed", "not_found"
--   fallbackUsed = false,    -- 是否正在使用 fallback
--   fallbackPath = nil,      -- 使用的 fallback 路径
--   error = nil,             -- 加载错误信息
-- }
```

#### Fallback 动画生成

```lua
-- 当没有任何可用动画时，自动生成占位动画
fsm:SetPlaceholderConfig({
    -- 启用占位动画生成
    enabled = true,

    -- 占位动画类型
    type = "t_pose",  -- "t_pose", "a_pose", "bind_pose", "procedural_idle"

    -- 程序化 Idle (轻微呼吸动作)
    proceduralIdle = {
        enabled = true,
        breathingSpeed = 0.5,
        breathingAmount = 0.02,
        swaySpeed = 0.3,
        swayAmount = 0.01,
    },

    -- 可视化提示 (开发模式)
    showWarningOverlay = IS_DEBUG,  -- 在角色上显示警告图标
    overlayColor = Color(1, 0, 1, 0.5),  -- 粉色半透明
})
```

#### BlendSpace 资源 Fallback

```lua
-- BlendSpace 中部分动画缺失的处理
local moveBlend = BlendSpace2D.new({
    name = "Movement",
    parameterX = "direction",
    parameterY = "speed",

    points = {
        { x = 0, y = 0, animation = "Idle.ani" },
        { x = 0, y = 3, animation = "Walk.ani" },
        { x = 0, y = 6, animation = "Run.ani" },      -- 假设此资源缺失
        { x = 90, y = 3, animation = "WalkRight.ani" },
    },

    -- BlendSpace 专用 fallback 策略
    fallbackStrategy = {
        -- 缺失点的处理方式
        missingPointBehavior = "interpolate_neighbors",
        -- "interpolate_neighbors": 从邻近点插值
        -- "use_nearest": 使用最近的有效点
        -- "use_fallback": 使用指定的 fallback 动画

        -- 指定 fallback (当使用 "use_fallback" 策略时)
        fallbackAnimation = "Idle.ani",

        -- 权重阈值 (低于此权重的缺失点不报错)
        warningThreshold = 0.1,
    },
})

-- 查询 BlendSpace 资源状态
local blendStatus = moveBlend:GetResourceStatus()
-- blendStatus = {
--   totalPoints = 4,
--   loadedPoints = 3,
--   failedPoints = 1,
--   failedList = {
--     { x = 0, y = 6, path = "Run.ani", error = "File not found" },
--   },
-- }
```

#### 日志与监控

```lua
-- Fallback 事件日志
fsm:OnFallbackUsed(function(event)
    Logger:Warning("[AnimFSM] Fallback triggered:")
    Logger:Warning("  State: %s", event.stateName)
    Logger:Warning("  Original: %s", event.originalPath)
    Logger:Warning("  Fallback: %s", event.fallbackPath)
    Logger:Warning("  Reason: %s", event.reason)

    -- 上报到监控系统
    Analytics:TrackEvent("animation_fallback", {
        state = event.stateName,
        original = event.originalPath,
        fallback = event.fallbackPath,
    })
end)

-- 统计信息
local stats = fsm:GetFallbackStats()
-- stats = {
--   totalFallbacks = 3,          -- 总 fallback 次数
--   uniqueResources = 2,         -- 涉及的资源数
--   mostFrequent = "Run.ani",    -- 最常触发 fallback 的资源
--   fallbackMap = {              -- 详细映射
--     ["Run.ani"] = { count = 2, fallback = "Walk.ani" },
--     ["SpecialAttack.ani"] = { count = 1, fallback = "Attack.ani" },
--   },
-- }
```

#### C++ 实现要点

```cpp
// AnimationResourceManager.h
class URHO3D_API AnimationResourceManager
{
public:
    /// 加载动画，支持 fallback 链
    SharedPtr<Animation> LoadAnimationWithFallback(
        const String& path,
        const Vector<String>& fallbacks,
        FallbackBehavior behavior = FallbackBehavior::UseDefault);

    /// 资源状态
    enum class ResourceState
    {
        NotLoaded,
        Loading,
        Loaded,
        Failed,
        UsingFallback
    };

    ResourceState GetResourceState(const String& path) const;

    /// Fallback 回调
    void SetFallbackCallback(std::function<void(const FallbackEvent&)> callback);

private:
    /// 生成占位动画
    SharedPtr<Animation> GeneratePlaceholderAnimation(
        Skeleton* skeleton,
        PlaceholderType type);

    /// 资源缓存
    HashMap<String, SharedPtr<Animation>> cache_;

    /// Fallback 映射 (原始路径 -> 实际使用的路径)
    HashMap<String, String> fallbackMap_;
};

// 使用示例
auto* anim = resourceManager->LoadAnimationWithFallback(
    "Animations/SpecialAttack.ani",
    { "Animations/Attack.ani", "Animations/Idle.ani" },
    FallbackBehavior::UseDefault
);

if (resourceManager->GetResourceState("Animations/SpecialAttack.ani")
    == ResourceState::UsingFallback)
{
    URHO3D_LOGWARNING("Using fallback animation for SpecialAttack");
}
```

### 9.11 C++ 调试接口

```cpp
// AnimationDebugger.h
class URHO3D_API AnimationDebugger
{
public:
    // 单例访问
    static AnimationDebugger& Get();

    // 全局调试开关
    void SetEnabled(bool enabled);
    bool IsEnabled() const;

    // 日志配置
    void SetLogLevel(LogLevel level);
    void SetLogOutput(LogOutput output, const String& path = "");

    // 注册状态机进行调试
    void RegisterStateMachine(AnimationStateMachine* fsm);
    void UnregisterStateMachine(AnimationStateMachine* fsm);

    // ImGui 调试窗口
    void DrawDebugWindow();

    // 命令行接口
    void RegisterConsoleCommands(Console* console);
};

// 控制台命令示例
// > anim_debug on                    -- 开启调试
// > anim_list                        -- 列出所有状态机
// > anim_inspect "CharacterLoco"     -- 检查特定状态机
// > anim_set speed 5.0               -- 设置参数
// > anim_force_state "Jump"          -- 强制切换状态
// > anim_record start                -- 开始录制
// > anim_record stop                 -- 停止录制
// > anim_playback "recording.json"   -- 回放录制

// ImGui 调试窗口
void AnimationDebugger::DrawDebugWindow()
{
    if (ImGui::Begin("Animation Debugger"))
    {
        // 状态机选择
        if (ImGui::BeginCombo("State Machine", currentFSM_->GetName().CString()))
        {
            for (auto* fsm : registeredFSMs_)
            {
                if (ImGui::Selectable(fsm->GetName().CString()))
                    currentFSM_ = fsm;
            }
            ImGui::EndCombo();
        }

        ImGui::Separator();

        // 当前状态
        ImGui::Text("Current State: %s", currentFSM_->GetCurrentState().CString());
        ImGui::Text("State Time: %.2fs", currentFSM_->GetStateTime());

        ImGui::Separator();

        // 参数编辑
        if (ImGui::CollapsingHeader("Parameters", ImGuiTreeNodeFlags_DefaultOpen))
        {
            for (auto& param : currentFSM_->GetParameters())
            {
                switch (param.second_.type)
                {
                case AnimParamType::Float:
                    {
                        float value = param.second_.value.GetFloat();
                        if (ImGui::SliderFloat(param.first_.CString(), &value,
                            param.second_.minValue, param.second_.maxValue))
                        {
                            currentFSM_->SetFloat(param.first_, value);
                        }
                    }
                    break;
                case AnimParamType::Bool:
                    {
                        bool value = param.second_.value.GetBool();
                        if (ImGui::Checkbox(param.first_.CString(), &value))
                        {
                            currentFSM_->SetBool(param.first_, value);
                        }
                    }
                    break;
                case AnimParamType::Trigger:
                    if (ImGui::Button(param.first_.CString()))
                    {
                        currentFSM_->SetTrigger(param.first_);
                    }
                    break;
                }
            }
        }

        // 转换列表
        if (ImGui::CollapsingHeader("Available Transitions"))
        {
            for (auto& trans : currentFSM_->GetTransitionsFrom(currentFSM_->GetCurrentState()))
            {
                bool canTransition = currentFSM_->EvaluateCondition(trans.condition);
                ImGui::TextColored(
                    canTransition ? ImVec4(0, 1, 0, 1) : ImVec4(1, 0, 0, 1),
                    "-> %s [%s] %s",
                    trans.toState.CString(),
                    trans.condition.CString(),
                    canTransition ? "✓" : "✗"
                );
            }
        }

        // 性能统计
        if (ImGui::CollapsingHeader("Performance"))
        {
            auto stats = currentFSM_->GetProfilingStats();
            ImGui::Text("Update Time: %.3f ms", stats.updateTime);
            ImGui::Text("Condition Evals: %d", stats.conditionEvalCount);
            ImGui::Text("Active Animations: %d", stats.activeAnimations);

            // 性能图表
            static float updateTimes[100] = {};
            static int offset = 0;
            updateTimes[offset] = stats.updateTime;
            offset = (offset + 1) % 100;
            ImGui::PlotLines("Update Time", updateTimes, 100, offset, nullptr, 0, 1.0f, ImVec2(0, 50));
        }
    }
    ImGui::End();
}
```

### 9.10 调试快捷键

```lua
-- 注册调试快捷键
input:RegisterDebugHotkeys({
    -- F1: 切换调试覆盖层
    { key = KEY_F1, action = function()
        local enabled = not fsm:IsDebugOverlayEnabled()
        fsm:SetDebugOverlay(enabled)
        print("Animation Debug Overlay: " .. (enabled and "ON" or "OFF"))
    end },

    -- F2: 打印当前状态
    { key = KEY_F2, action = function()
        fsm:DebugPrintState()
        fsm:DebugPrintParameters()
    end },

    -- F3: 切换骨骼显示
    { key = KEY_F3, action = function()
        local enabled = not animator:IsDebugDrawSkeletonEnabled()
        animator:SetDebugDrawSkeleton(enabled)
    end },

    -- F4: 暂停/继续动画
    { key = KEY_F4, action = function()
        local paused = not animator:IsPaused()
        animator:SetPaused(paused)
        print("Animation: " .. (paused and "PAUSED" or "PLAYING"))
    end },

    -- F5: 单帧步进 (暂停时)
    { key = KEY_F5, action = function()
        if animator:IsPaused() then
            animator:StepFrame()
        end
    end },

    -- F6: 开始/停止录制
    { key = KEY_F6, action = function()
        if fsm:IsRecording() then
            fsm:StopRecording()
            fsm:GetRecording():SaveToFile("debug_recording.json")
            print("Recording saved to debug_recording.json")
        else
            fsm:StartRecording()
            print("Recording started...")
        end
    end },
})
```

---

## 10. 已知问题与限制

### 10.1 BlendSpace 与 Layer BlendMode 的交互

#### 问题背景

在 Urho3D 动画系统中，`blendMode` 是 per-animation 的属性，而不是 per-layer 的属性。这导致了 BlendSpace 与 Layer BlendMode 之间存在一些复杂的交互问题。

#### BlendSpace 内部混合

BlendSpace 需要同时播放多个动画（如 Idle 30% + Walk 70%），并按权重混合。这要求内部动画使用 `ABM_ADDITIVE` 模式：

```
// BlendSpace 内部混合
result = Idle * 0.3 + Walk * 0.7  // 需要 ABM_ADDITIVE 实现
```

如果使用 `ABM_LERP`，结果是连续 lerp，混合效果不正确：

```
// ABM_LERP 的错误结果
result = lerp(lerp(base, Idle, 0.3), Walk, 0.7)  // 不是我们想要的效果
```

#### 普通动画与 BlendSpace 之间的过渡

当前实现采用精心设计的过渡策略：

| 阶段 | 普通动画 | BlendSpace | 说明 |
|------|----------|------------|------|
| 普通动画运行 | layer.blendMode | - | 正常播放 |
| 过渡中 | layer.blendMode, 淡出 | **ABM_LERP**, 淡入 | 双方平滑过渡 |
| 过渡完成瞬间 | weight=0 | weight=1, 切换到 ABM_ADDITIVE | 旧动画已无贡献 |
| BlendSpace 运行 | - | ABM_ADDITIVE（内部混合） | 正常播放 |

**设计要点**：

1. **过渡期间使用 ABM_LERP**：BlendSpace 在淡入时使用 ABM_LERP，与普通动画的过渡平滑
2. **过渡完成后才切换**：只有当过渡完成（普通动画 weight=0 完全淡出）时，才将 BlendSpace 切换到 ABM_ADDITIVE
3. **无跳变**：切换瞬间普通动画已经没有贡献，所以 blendMode 切换不会产生视觉跳变

```cpp
// AnimationStateMachine.cpp 中的过渡逻辑
AnimationBlendMode crossfadeMode = layer.runtime.blendSpaceCrossfadeActive
    ? ABM_LERP      // 过渡期间用 LERP
    : ABM_ADDITIVE; // 运行时用 ADDITIVE
```

#### 已知缺陷

**ABM_ADDITIVE 层过渡到 BlendSpace 时的 blendMode 不一致**

当 `layer.blendMode = ABM_ADDITIVE` 时，普通动画过渡到 BlendSpace 会出现 blendMode 不一致：

| 时刻 | 普通动画 | BlendSpace |
|------|----------|------------|
| 过渡前 | ABM_ADDITIVE, weight=1 | - |
| 过渡开始 | ABM_ADDITIVE, 淡出 | ABM_LERP, 淡入 |

过渡期间两种不同的 blendMode 同时作用，可能导致混合行为不连贯。

**影响范围**：仅当在 `blendMode = ABM_ADDITIVE` 的层上使用 BlendSpace 并与普通动画过渡时才会触发。这种配置在实际使用中很少见（ABM_ADDITIVE 层通常用于上半身叠加动画，很少使用 BlendSpace）。

---

## 附录

### A. API 速查表

| 类 | 方法 | 说明 |
|----|------|------|
| `AnimationStateMachine` | `new(config)` | 从配置创建状态机 |
| | `SetFloat/Int/Bool(name, value)` | 设置参数 |
| | `SetTrigger(name)` | 触发 Trigger |
| | `GetCurrentState()` | 获取当前状态名 |
| | `IsInState(name)` | 检查是否在指定状态 |
| | `ForceState(name)` | 强制切换状态 |
| | `Update(dt)` | 更新状态机 |
| `BlendSpace1D` | `new(config)` | 创建 1D 混合空间 |
| | `SetParameter(value)` | 设置混合参数 |
| `BlendSpace2D` | `new(config)` | 创建 2D 混合空间 |
| | `SetParameters(x, y)` | 设置混合参数 |
| `AvatarMask` | `new(config)` | 创建骨骼蒙版 |
| | `.FullBody/.UpperBody/...` | 预定义蒙版 |
| `AnimationLayerController` | `new(config)` | 创建层控制器 |
| | `SetLayerWeight(name, weight)` | 设置层权重 |
| | `CrossfadeLayerWeight(name, weight, time)` | 平滑过渡层权重 |

### B. 条件表达式语法

```
expression := or_expr
or_expr    := and_expr ("or" and_expr)*
and_expr   := not_expr ("and" not_expr)*
not_expr   := "not" not_expr | compare_expr
compare_expr := primary ((">" | "<" | ">=" | "<=" | "==" | "!=") primary)?
primary    := NUMBER | BOOL | IDENTIFIER | "(" expression ")"

IDENTIFIER := [a-zA-Z_][a-zA-Z0-9_]*
NUMBER     := [0-9]+("."[0-9]+)?
BOOL       := "true" | "false"
```

### C. 内置变量

| 变量 | 类型 | 说明 |
|------|------|------|
| `stateTime` | float | 当前状态已播放时间（秒） |
| `normalizedTime` | float | 归一化时间 (0-1) |
| `animationFinished` | bool | 动画是否播放完成 |

### D. 内置函数

| 函数 | 说明 |
|------|------|
| `abs(x)` | 绝对值 |
| `min(a, b)` | 最小值 |
| `max(a, b)` | 最大值 |
| `clamp(x, min, max)` | 限制范围 |

---

*文档版本: 1.0*
*最后更新: 2025-12-25*
