---
type: concept
status: active
confidence: 0.78
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 游戏开发, 游戏引擎]
aliases: [CryEngine Lua, Lumberyard Lua, 实体脚本, CryEntity]
relates_to:
  - target: "[[Lua脚本宿主模式]]"
    type: implements
    confidence: 0.85
  - target: "[[游戏引擎架构]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Lua C API 绑定层]]"
    type: uses
    confidence: 0.75
supersedes: null
---
# CryEngine 实体脚本系统

## 概述
CryEngine（及其派生引擎 [[Amazon]] Lumberyard）通过 Lua 实体脚本驱动游戏对象行为，实体属性在编辑器中以 Properties 表暴露，生命周期回调、FlowGraph 节点和 AI 状态机均以 Lua 实现。

## 关键内容

### 实体脚本结构
CryEngine 实体脚本以一个同名全局 table 定义：

```lua
MyEntity = {
    Properties = {
        bEnabled = 1,     -- bool（通过初始值类型推断编辑器控件类型）
        fSpeed   = 5.0,   -- float
        nMaxCount = 10,   -- int
        sName = "default" -- string
        Attack = { fDamage = 25.0 }  -- 嵌套属性组
    }
}
```

属性值在编辑器中可直接调整，引擎通过类型推断（数值前缀：b/f/n/s）决定控件类型。

### 生命周期回调

| 回调 | 时机 |
|------|------|
| `OnInit(self)` | 实体初始化（关卡加载或运行时生成） |
| `OnReset(self)` | 编辑器进入游戏模式/退出时重置属性 |
| `OnUpdate(self, dt)` | 每帧更新（需在 OnInit 中启用更新） |
| `OnCollision(self, hit)` | 碰撞事件（hit.pos, hit.normal, hit.damage） |
| `Event_OnActivate(self)` | FlowGraph 激活输入节点时触发 |

典型模式：`OnInit` 调 `OnReset`，`OnReset` 从 Properties 同步运行时状态（实现编辑器属性修改即时生效）。

### FlowGraph 集成
实体可作为 FlowGraph 节点，输入/输出通过 `Event_*` 回调绑定：
- `OnFlowgraphActivation(nodeID, inputs)` — 接收激活信号和输入数据
- 实体脚本通过 FlowGraph 与关卡逻辑（触发器、门、机关）解耦连接

### AI 状态机
`SetupState(stateMachine)` 定义 AI 行为状态机：

```lua
stateMachine:SetDefaultState("Idle")
stateMachine:AddState{
    name = "Idle",
    OnEnter = function(self)
        AI.SetBehaviorVariable(self.id, "IsAlert", false)
    end,
    transitions = {
        {to="Alert", condition=function(self)
            return AI.GetBehaviorVariable(self.id, "ThreatDetected")
        end}
    }
}
```

状态机以声明式 table 定义，条件函数在每帧轮询，满足条件时自动迁移状态。

### 与其他引擎的对比
CryEngine 实体脚本的独特之处在于：属性系统（Properties 表→编辑器控件）、FlowGraph 可视化逻辑连接、AI 行为变量桥接，三者协同工作，是 AAA 引擎 Lua 集成的典型"数据驱动 + 脚本逻辑"混合方案。

## 来源
- [[engine-integration]] — 游戏引擎集成参考文档，CryEngine/Lumberyard 实体脚本结构与 AI 状态机示例

## 相关
- [[Lua脚本宿主模式]] — CryEngine 实体脚本属于引擎嵌入 Lua 的宿主模式，生命周期由引擎驱动
- [[游戏引擎架构]] — CryEngine 代表 AAA 级 C++ 引擎 + Lua 脚本层架构
- [[Lua C API 绑定层]] — CryEngine 内部通过 C API 将引擎函数注册给 Lua 实体脚本
