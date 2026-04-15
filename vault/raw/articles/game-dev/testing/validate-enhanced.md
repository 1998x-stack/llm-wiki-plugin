---
summary: "Enhanced validate mode: interactive Gym-style protocol, Lua assertion framework, benchmark runner"
status: in_progress
last_updated: "2026-04-02"
read_when:
  - "working on validate mode"
  - "working on benchmark or testing"
  - "adding input injection or interactive validation"
  - "writing game validation tests"
related_paths:
  - "engine/Source/Tools/UrhoXRuntime/**"
  - "tools/generators/gen_runtime.py"
  - "engine/bin/Data/urhox-libs/UI/Core/UI.lua"
  - "engine/bin/Data/urhox-libs/UI/Core/Widget.lua"
---

# UrhoX Validate Mode 增强计划

**目标**: 将 UrhoX validate 模式从"烟雾测试"升级为"完整的游戏验证框架"，核心是一个 **Gym-style 交互式验证协议**——AI 逐帧控制引擎、观测场景树 + UI 树、注入输入、做出断言。

**动机**: 当前 validate 模式只能验证"脚本加载 + N 帧无 crash"，无法检测游戏是否真正运行（可能只停在封面画面）。参考 GameDevBench（CMU/Princeton, 132 个 Godot 游戏开发任务的 benchmark）和 TITAN（GPT-4o 驱动的自动游戏测试框架）的设计，我们需要一个分层递进的验证体系。

**优先级**: P1

---

## 目录

- [1. 现状分析](#1-现状分析)
- [2. 架构设计](#2-架构设计)
- [3. Phase 1：增强被动观测](#3-phase-1增强被动观测)
- [4. Phase 2：交互式验证协议（Gym-style）](#4-phase-2交互式验证协议gym-style)
- [5. Phase 3：Lua 断言框架](#5-phase-3lua-断言框架)
- [6. Phase 4：Benchmark Runner](#6-phase-4benchmark-runner)
- [7. JSON Report 格式](#7-json-report-格式)
- [8. 文件清单](#8-文件清单)
- [9. 实施顺序与依赖](#9-实施顺序与依赖)
- [附录 A：GameDevBench 关键设计借鉴](#附录-a-gamedevbench-关键设计借鉴)
- [附录 B：TITAN 可用洞察](#附录-b-titan-可用洞察)

---

## 1. 现状分析

### 1.1 已有能力

| 能力 | 实现状态 | 位置 |
|------|---------|------|
| `-validate` 标志 | ✅ 已实现 | `UrhoXRuntime.cpp:165` |
| `-validate-frames=N` | ✅ 默认 60 | `UrhoXRuntime.cpp:168` |
| `-validate-timeout=N` | ✅ 默认 30s | `UrhoXRuntime.cpp:170` |
| `-validate-output=path` | ✅ JSON 输出 | `UrhoXRuntime.cpp:172` |
| `-graphicsheadless` | ✅ NOOP 渲染 | `Engine.cpp:290-294` |
| 错误收集与分类 | ✅ lua/resource/engine | `UrhoXRuntimeValidate.cpp:37-98` |
| Shader 错误过滤 | ✅ NOOP 模式预期 | `UrhoXRuntimeValidate.cpp:64-68` |
| 场景状态查询 | ✅ node/component 计数 | `UrhoXRuntimeValidate.cpp` `ValidateSceneState()` |
| 超时处理 | ✅ 写 TIMEOUT report | `UrhoXRuntimeValidate.cpp:105-111` |
| 退出码 | ✅ 0=PASS, 1=FAIL | `UrhoXRuntimeValidate.cpp:201` |

### 1.2 关键缺口

| 缺口 | 影响 |
|------|------|
| **无输入能力** | 游戏停在标题画面，60 帧空转 |
| **无交互式控制** | AI 无法逐帧观测状态、根据反馈决定下一步操作 |
| **无逐帧指标** | 不知道游戏是"活着"还是"冻住了" |
| **无 UI 树观测** | 看不到 Widget 布局，无法知道"按钮在哪里" |
| **场景查询太浅** | 只有 node/component 总数，无法检查具体节点/属性 |
| **无断言框架** | 无法验证"节点 X 是否存在"、"属性 Y 是否正确" |
| **无 benchmark runner** | 无法批量测试数百个 AI 生成的脚本 |
| **无防作弊沙盒** | AI 可以读取测试条件并硬编码通过 |

### 1.3 Input 子系统现状

- `Input::SetKey()` / `Input::SetMouseButton()` — **private**，未暴露给 Lua
- `Input::MessageAdaptation_SetKey()` — **public C++** 但不在 Lua pkg 中
- `Input::HandleSDLEvent()` — 处理 SDL 事件，internal
- validate 模式下 `SDL_VIDEODRIVER=dummy`，SDL 初始化但不产生事件
- **结论**: 需要新建输入注入路径，最安全的方式是通过 `SDL_PushEvent` 注入原生 SDL 事件

---

## 2. 架构设计

### 2.1 分层验证体系

```
┌─────────────────────────────────────────────────────────────┐
│  L0: 静态分析（语法检查，不运行引擎）                         │
│  - Lua 语法解析                                              │
│  - 资源引用检查                                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  L1: 加载验证（批处理模式，不需要输入）                       │
│  - 脚本加载无错误                                            │
│  - Start() 执行无 crash                                     │
│  - 场景创建成功 + 逐帧状态监控 + 停滞检测                    │
│  ← Phase 1 的能力范围（增强版 -validate）                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  L2: 交互式验证（Gym-style 协议）                             │
│  - AI 逐帧控制引擎（step + observe）                         │
│  - 观测场景树 + UI 树（结构化 JSON，非截图）                  │
│  - 模拟输入（tap/key/touch → SDL 事件）                      │
│  - AI 根据观测结果决定下一步操作                              │
│  ← Phase 2 的目标（-validate-interactive）                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  L3: 结构化断言（引擎侧 Lua 测试脚本）                       │
│  - 节点存在性、属性值、组件配置检查                           │
│  - 运行时行为断言（输入 → 状态变化）                         │
│  ← Phase 3 的目标（-validate-test，类似 GameDevBench test.gd）│
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  L4: Benchmark Runner（批量测试 + 防作弊沙盒）                │
│  - 沙盒环境创建                                              │
│  - AI Agent 编写代码                                         │
│  - 通过 L1/L2/L3 任意组合验证                                │
│  - 结果汇总与统计                                            │
│  ← Phase 4 的目标（类似 GameDevBench 的 benchmark_runner）    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 核心架构：Gym-style 交互协议

引擎变成一个 **环境（Environment）**，外部 AI 是 **代理（Agent）**：

```
AI Agent (Python/任意语言)           UrhoX Runtime (C++)
   │                                      │
   ├─ {"cmd":"observe"} ────────────────►  │
   │◄─ {scene_tree, ui_tree, errors} ───  │  观测当前状态
   │                                      │
   ├─ {"cmd":"step",                      │
   │    "dt":0.016,                       │
   │    "input":{"tap":{"x":400,"y":420}} │
   │   } ──────────────────────────────►  │  注入输入 + 推进 1 帧
   │                                      ├─ SDL_PushEvent(tap)
   │                                      ├─ Engine::RunFrame(0.016)
   │                                      ├─ 收集 scene + UI 状态
   │◄─ {frame, scene_tree, ui_tree} ───   │  返回新状态
   │                                      │
   │  (AI 思考，不限时间)                  │
   │                                      │
   ├─ {"cmd":"step", "dt":0.016,          │
   │    "input":{"keys_down":["W"]}} ──►  │  继续操作
   │◄─ {frame, scene_tree, ui_tree} ───   │
   │                                      │
   ├─ {"cmd":"finish"} ────────────────►  │
   │◄─ {result, report} ──────────────    │  最终报告
   └──────────────────────────────────────┘
```

**关键优势**：AI 看到上一帧的场景树 + UI 树再决定下一帧做什么——不是盲打预编排序列。

### 2.3 核心设计决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 控制模型 | **Gym-style 交互协议**（stdin/stdout JSON） | AI 可响应式操作，吃掉预编排输入和 auto-play 两种模式 |
| 观测方式 | **场景树 + UI 树 JSON**（非截图） | 结构化、零 GPU 成本、比截图更精确 |
| 输入注入 | **SDL_PushEvent**（引擎侧） | 游戏脚本无感知，行为与真实输入一致 |
| 帧推进 | **AI 指定 dt**（非引擎自动 tick） | AI 完全控制时间步长，确定性可重现 |
| 验证方式 | **确定性断言**（非 LLM-as-judge） | GameDevBench 明确拒绝视觉评分/LLM 判断 |
| 断言语言 | **Lua**（与游戏脚本同语言） | 无需额外工具链；可访问完整引擎 API |
| 测试隔离 | **沙盒 + 测试注入**（仿 GameDevBench） | 防止 AI 读取测试条件作弊 |
| JSON 兼容 | **不需要**（系统未上线） | 直接用最终格式，不保留 version 字段 |

---

## 3. Phase 1：增强被动观测

**目标**: 不改变 CLI 接口，丰富 JSON report 数据，检测"游戏是否活着"。

**改动范围**: `UrhoXRuntimeValidate.cpp`, `ValidationCollector.h`

### 3.1 多帧状态快照

在多个时间点采样场景状态（而非仅在最后一帧），检测场景是否在变化。

**采样点**: frame 1, frame 10, frame N/2, frame N（validate-frames 的最后一帧）

**每帧快照数据**:

```cpp
struct StateSnapshot {
    int frame;
    String phase;          // "load", "init", "run", "scene"
    float frameDurationMs; // 该帧耗时
    int nodeCount;
    int componentCount;
    uint32_t stateHash;    // 场景状态指纹（见 3.2）
};
```

**实现**: 扩展 `ValidateSceneState()` 为 `CaptureStateSnapshot(int frame)`，在 `HandleValidateUpdate` 中按帧号触发。

### 3.2 场景状态指纹

计算场景树的轻量 hash，用于检测状态变化：

```lua
-- 注入的 Lua 代码
local function stateHash(node, depth)
    local h = 0
    -- 混入节点名 + 位置（粗粒度） + 子节点数 + 组件数
    h = h + #node:GetName()
    local pos = node:GetPosition()
    h = h + math.floor(pos.x * 10) + math.floor(pos.y * 10) + math.floor(pos.z * 10)
    h = h + node:GetNumChildren() * 7
    h = h + node:GetNumComponents() * 13
    if depth < 3 then  -- 只遍历前 3 层，避免性能问题
        for i = 0, math.min(node:GetNumChildren() - 1, 19) do  -- 最多 20 子节点
            h = h + stateHash(node:GetChild(i), depth + 1)
        end
    end
    return h
end
```

### 3.3 逐帧耗时监控

在 `HandleValidateUpdate` 中记录每帧的 `timeStep`，检测异常：

```cpp
// 在 HandleValidateUpdate 中
float frameDurationMs = timeStep * 1000.0f;

// 记录最大帧耗时
if (frameDurationMs > validationCollector_->maxFrameTimeMs_)
    validationCollector_->maxFrameTimeMs_ = frameDurationMs;

// 检测 spike（>500ms = 可能死循环）
if (frameDurationMs > 500.0f)
{
    validationCollector_->RecordError("engine",
        String("Frame time spike: ") + String(frameDurationMs) + "ms",
        validateFrameCounter_);
}
```

### 3.4 停滞检测

比较首尾两次快照的 `stateHash`，判断场景是否在变化：

```cpp
bool sceneStalled = (snapshots_.Size() >= 2 &&
    snapshots_.Front().stateHash == snapshots_.Back().stateHash &&
    snapshots_.Front().nodeCount == snapshots_.Back().nodeCount);
```

### 3.5 组件类型普查

扩展场景查询，统计组件类型分布：

```lua
local componentTypes = {}
local function census(node)
    for i = 0, node:GetNumComponents() - 1 do
        local comp = node:GetComponent(i)
        local typeName = comp:GetTypeName()
        componentTypes[typeName] = (componentTypes[typeName] or 0) + 1
    end
    for i = 0, node:GetNumChildren() - 1 do
        census(node:GetChild(i))
    end
end
```

输出示例: `{"StaticModel": 5, "RigidBody": 3, "AnimationController": 1, "Light": 2}`

### 3.6 Update 函数检测

检查游戏是否定义了 `Update` 函数（没有 Update = 静态场景）：

```lua
local hasUpdate = type(Update) == "function"
```

### 3.7 JSON Report 新增字段

```json
{
  "state_snapshots": [
    {"frame": 1, "phase": "init", "nodes": 3, "components": 5, "hash": 12345, "frame_time_ms": 8.2},
    {"frame": 10, "phase": "run", "nodes": 12, "components": 25, "hash": 67890, "frame_time_ms": 4.1},
    {"frame": 30, "phase": "run", "nodes": 12, "components": 25, "hash": 67890, "frame_time_ms": 3.8},
    {"frame": 60, "phase": "run", "nodes": 12, "components": 25, "hash": 67890, "frame_time_ms": 4.0}
  ],
  "scene_stalled": true,
  "max_frame_time_ms": 8.2,
  "update_defined": false,
  "component_census": {"StaticModel": 5, "RigidBody": 3, "Light": 2}
}
```

**工作量**: ~150-200 行 C++ + ~50 行 Lua

---

## 4. Phase 2：交互式验证协议（Gym-style）

**目标**: 引擎不自动 tick，外部 AI 通过 stdin/stdout JSON 协议逐帧控制——传入 timeStep + 输入事件，引擎返回场景树 + UI 树。

**改动范围**: `UrhoXRuntime.h/cpp`, 新增 `ValidateInteractive.h/cpp`, `ValidateInputInjector.h/cpp`

### 4.1 CLI 参数

```
-validate-interactive
```

与 `-validate` 互斥。进入交互模式后，引擎完成脚本加载 + `Start()`，然后阻塞等待 stdin 命令。

### 4.2 协议定义

#### 命令：observe（只读，不推进帧）

```json
→ {"cmd": "observe"}
← {
    "frame": 0,
    "scene": { ... },
    "ui": { ... },
    "errors": []
  }
```

#### 命令：step（注入输入 + 推进 1 帧）

```json
→ {"cmd": "step", "dt": 0.016, "input": {
    "tap": {"x": 400, "y": 420},
    "keys_down": ["W", "SPACE"],
    "keys_up": ["A"]
  }}
← {
    "frame": 1,
    "scene": { ... },
    "ui": { ... },
    "errors": []
  }
```

#### 命令：finish（生成报告 + 退出）

```json
→ {"cmd": "finish"}
← {
    "result": "PASS",
    "duration_ms": 1234,
    "frames_completed": 15,
    "phases": { ... },
    "missing_resources": [],
    "summary": { ... }
  }
```

#### input 字段格式

| 字段 | 类型 | 说明 | SDL 映射 |
|------|------|------|----------|
| `tap` | `{x, y}` | 点击（自动产生 down+up） | `SDL_MOUSEBUTTONDOWN` + `SDL_MOUSEBUTTONUP` |
| `click` | `{x, y, button}` | 点击指定按钮 | 同 tap |
| `keys_down` | `string[]` | 按下的键 | `SDL_KEYDOWN` |
| `keys_up` | `string[]` | 释放的键 | `SDL_KEYUP` |
| `touch` | `{x, y, action, finger}` | 触摸事件 | `SDL_FINGERDOWN/MOTION/UP` |
| `mouse_move` | `{x, y}` | 鼠标移动 | `SDL_MOUSEMOTION` |

多种输入可在同一个 step 中组合。

### 4.3 观测：场景树序列化

```lua
-- 引擎注入的 Lua 代码，序列化场景树
local function serializeNode(node, depth)
    if not node or depth > 4 then return nil end
    local pos = node:GetPosition()
    local n = {
        name = node:GetName(),
        pos = {math.floor(pos.x*10)/10, math.floor(pos.y*10)/10, math.floor(pos.z*10)/10},
        enabled = node:IsEnabled(),
    }
    -- 组件列表
    local numComps = node:GetNumComponents()
    if numComps > 0 then
        n.components = {}
        for i = 0, numComps - 1 do
            local comp = node:GetComponent(i)
            table.insert(n.components, {type = comp:GetTypeName()})
        end
    end
    -- 子节点（限制数量避免爆炸）
    local numChildren = node:GetNumChildren()
    if numChildren > 0 then
        n.children = {}
        for i = 0, math.min(numChildren - 1, 29) do
            table.insert(n.children, serializeNode(node:GetChild(i), depth + 1))
        end
        if numChildren > 30 then
            n.children_truncated = numChildren
        end
    end
    return n
end
```

输出示例：

```json
{
  "scene": {
    "name": "Scene",
    "children": [
      {
        "name": "Player",
        "pos": [0.0, 1.0, 0.0],
        "enabled": true,
        "components": [
          {"type": "RigidBody"},
          {"type": "CharacterController"},
          {"type": "AnimatedModel"}
        ]
      },
      {
        "name": "Ground",
        "pos": [0.0, 0.0, 0.0],
        "components": [{"type": "StaticModel"}, {"type": "CollisionShape"}]
      }
    ]
  }
}
```

### 4.4 观测：UI 树序列化

基于 `UI.GetRoot()` 的 Widget 树（`urhox-libs/UI/Core/Widget.lua`）：

```lua
-- Widget 树序列化
-- Widget 结构：._className (类型), .id, .props (属性), .children[] (子 Widget)
-- 布局：widget:GetAbsoluteLayout() → {x, y, w, h} (屏幕坐标)

local function serializeWidget(w, depth)
    if not w or depth > 5 then return nil end
    if w.props.visible == false then return nil end  -- 跳过隐藏元素
    local l = w:GetAbsoluteLayout()
    local node = {
        type = w._className,                        -- "Button", "Label", "Panel", ...
        id = w.id,                                   -- 用户指定的 id（可为 nil）
        rect = {                                     -- 屏幕绝对坐标
            math.floor(l.x), math.floor(l.y),
            math.floor(l.w), math.floor(l.h)
        },
    }
    -- 只输出有用的 props
    if w.props.text then node.text = w.props.text end
    if w.props.placeholder then node.placeholder = w.props.placeholder end
    if w.props.disabled then node.disabled = true end
    if w.props.checked ~= nil then node.checked = w.props.checked end
    if w.props.value ~= nil then node.value = w.props.value end

    -- 子 Widget
    if #w.children > 0 then
        node.children = {}
        for _, child in ipairs(w.children) do
            local serialized = serializeWidget(child, depth + 1)
            if serialized then
                table.insert(node.children, serialized)
            end
        end
        if #node.children == 0 then node.children = nil end
    end
    return node
end

-- 调用入口
local uiRoot = UI and UI.GetRoot and UI.GetRoot()
local uiTree = uiRoot and serializeWidget(uiRoot, 0) or nil
```

输出示例：

```json
{
  "ui": {
    "type": "Panel",
    "rect": [0, 0, 800, 600],
    "children": [
      {
        "type": "Button",
        "id": "startBtn",
        "text": "Start Game",
        "rect": [350, 400, 100, 40]
      },
      {
        "type": "Label",
        "text": "Score: 0",
        "rect": [10, 10, 80, 20]
      }
    ]
  }
}
```

**AI 看到 `"Button"` 在 `[350,400,100,40]`，发一个 `{"tap":{"x":400,"y":420}}` 就能点它。** 不需要截图。

### 4.5 引擎侧主循环改造

```cpp
// ValidateInteractive.h
class ValidateInteractive
{
public:
    ValidateInteractive(Engine* engine, LuaScript* luaScript, ValidationCollector* collector);

    /// 进入交互模式主循环（阻塞，直到收到 finish 命令或 stdin 关闭）
    void Run();

private:
    /// 读取一行 stdin，解析为 JSON 命令
    JSONValue ReadCommand();
    /// 写 JSON 响应到 stdout
    void WriteResponse(const JSONValue& response);

    /// 处理各命令
    JSONValue HandleObserve();
    JSONValue HandleStep(const JSONValue& cmd);
    JSONValue HandleFinish();

    /// 收集场景树 + UI 树观测
    JSONValue CollectObservation();
    /// 注入输入事件
    void InjectInput(const JSONValue& input);

    Engine* engine_;
    LuaScript* luaScript_;
    ValidationCollector* collector_;
    int frameCounter_{0};
    float elapsed_{0.0f};
};
```

**关键实现**：`HandleStep` 中调用 `Engine::RunFrame()`：

```cpp
JSONValue ValidateInteractive::HandleStep(const JSONValue& cmd)
{
    float dt = cmd["dt"].GetFloat();
    if (dt <= 0.0f) dt = 1.0f / 60.0f;

    // 1. 注入输入到 SDL 事件队列
    if (cmd.Contains("input"))
        InjectInput(cmd["input"]);

    // 2. 设置 override dt，推进 1 帧
    engine_->SetNextTimeStep(dt);  // 需要新增此方法
    engine_->RunFrame();

    // 3. 收集状态
    frameCounter_++;
    elapsed_ += dt;

    return CollectObservation();
}
```

**`Engine::SetNextTimeStep(float dt)`**：新增方法，在下一次 `RunFrame` 中使用指定 dt 而非自动计算。实现：在 `Engine` 中加一个 `overrideTimeStep_` 字段，`RunFrame` 开头检查并使用。

### 4.6 SDL 输入注入（与原 Phase 2 相同）

```cpp
// ValidateInputInjector.h — 从 JSON 命令注入 SDL 事件
class ValidateInputInjector
{
public:
    /// 从 JSON input 对象注入所有事件
    void InjectFromJSON(const JSONValue& input);

private:
    void PushSDLKeyEvent(SDL_Keycode keycode, SDL_Scancode scancode, bool pressed);
    void PushSDLMouseButtonEvent(int x, int y, Uint8 button, bool pressed);
    void PushSDLMouseMotionEvent(int x, int y);
    void PushSDLTouchEvent(float x, float y, int finger, Uint32 type);

    static SDL_Keycode ResolveKeyName(const String& name);
};
```

Key 映射表：

```cpp
static HashMap<String, SDL_Keycode> keyNameMap = {
    {"W", SDLK_w}, {"A", SDLK_a}, {"S", SDLK_s}, {"D", SDLK_d},
    {"SPACE", SDLK_SPACE}, {"RETURN", SDLK_RETURN}, {"ESCAPE", SDLK_ESCAPE},
    {"UP", SDLK_UP}, {"DOWN", SDLK_DOWN}, {"LEFT", SDLK_LEFT}, {"RIGHT", SDLK_RIGHT},
    {"TAB", SDLK_TAB}, {"LSHIFT", SDLK_LSHIFT},
    {"E", SDLK_e}, {"F", SDLK_f}, {"Q", SDLK_q}, {"R", SDLK_r},
    {"1", SDLK_1}, {"2", SDLK_2}, /* ... */
};
```

### 4.7 observe 参数控制

大场景/复杂 UI 的观测可能很大，支持参数裁剪：

```json
{"cmd": "observe", "max_depth": 3, "max_children": 10, "include_components": false}
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `max_depth` | 4 | 场景/UI 树最大遍历深度 |
| `max_children` | 30 | 每个节点最多序列化子节点数 |
| `include_components` | true | 是否输出组件列表 |
| `include_ui` | true | 是否输出 UI 树 |

### 4.8 交互模式如何吃掉预编排输入 + auto-play

| 原方案 | 交互模式下的等价实现 |
|--------|---------------------|
| `-validate-input=scenario.json` | 外部 Python 读 JSON，逐帧发 step 命令 |
| `OnValidateAutoPlay(frame)` | 不需要——AI 自己决定操作，不需要游戏脚本配合 |
| 预置 scenario 文件 | Python 侧的策略脚本（tap-center, wasd 等） |

**批处理模式（-validate）仍保留**，用于不需要 AI 交互的简单 L1 验证。两种模式互补：

```
L1 快速烟雾测试:  ./UrhoXRuntime main.lua -validate -validate-frames=60
L2 交互式验证:    ./UrhoXRuntime main.lua -validate-interactive
```

**工作量**: ~500-600 行 C++（含 Engine::SetNextTimeStep、stdin/stdout 协议、场景/UI 序列化），~100 行 Lua

---

## 5. Phase 3：Lua 断言框架（不变）

**目标**: 提供类似 GameDevBench `test.gd` 的结构化测试能力，用 Lua 编写测试脚本，验证游戏的具体行为。

**设计灵感**: GameDevBench 的 test.gd 使用 9 类断言模式（节点存在、属性值、信号连接、资源路径、脚本源码、Shader 代码、运行时行为、粒子系统、环境渲染）。我们需要 UrhoX Lua 等价物。

### 5.1 CLI 参数

```
-validate-test=path/to/test.lua
```

测试脚本在游戏脚本加载完成后、validate 帧循环开始前执行。测试脚本可以：
- 访问全局 `scene` 变量
- 使用完整的引擎 Lua API
- 调用断言辅助函数
- 输出 `VALIDATION_PASSED` 或 `VALIDATION_FAILED`

### 5.2 测试运行时序

```
Frame 0:  游戏脚本 ExecuteFile + Start()
Frame 1:  [如果有 -validate-test] 加载并执行 validate_helpers.lua
Frame 2:  [如果有 -validate-test] 执行 test.lua
Frame 3+: 正常 validate 帧循环（收集错误、输入注入等）
最后帧:   ValidateSceneState + 检查 test.lua 的结果
```

### 5.3 断言辅助库 (validate_helpers.lua)

```lua
-- engine/bin/Data/Validate/validate_helpers.lua
-- 引擎内置的测试辅助函数，自动加载到 validate 环境

local V = {}
local issues = {}
local passed = true

-- 基础断言
function V.fail(msg)
    passed = false
    table.insert(issues, msg)
    log:Write(LOG_ERROR, "__VALIDATE_ASSERT__:FAIL:" .. msg)
end

function V.assert(condition, msg)
    if not condition then V.fail(msg) end
    return condition
end

-- 节点存在性（GameDevBench Category A）
function V.assertNodeExists(path, expectedType)
    local node = scene:GetChild(path, true)  -- recursive search
    if not node then
        V.fail("Node '" .. path .. "' not found")
        return nil
    end
    if expectedType then
        -- 检查是否有指定类型的组件（UrhoX 的"节点类型"由组件决定）
        local comp = node:GetComponent(expectedType)
        if not comp then
            V.fail("Node '" .. path .. "' missing component: " .. expectedType)
            return nil
        end
    end
    return node
end

-- 组件存在性
function V.assertHasComponent(node, typeName)
    if type(node) == "string" then node = scene:GetChild(node, true) end
    if not node then V.fail("Node is nil"); return nil end
    local comp = node:GetComponent(typeName)
    if not comp then
        V.fail("Node '" .. node:GetName() .. "' missing component: " .. typeName)
    end
    return comp
end

-- 属性值检查（GameDevBench Category B）
function V.assertPosition(node, expected, tolerance)
    tolerance = tolerance or 0.1
    if type(node) == "string" then node = scene:GetChild(node, true) end
    if not node then V.fail("Node is nil"); return end
    local pos = node:GetPosition()
    local dist = (pos - expected):Length()
    if dist > tolerance then
        V.fail(string.format("Node '%s' position (%.1f,%.1f,%.1f) != expected (%.1f,%.1f,%.1f), dist=%.2f",
            node:GetName(), pos.x, pos.y, pos.z, expected.x, expected.y, expected.z, dist))
    end
end

function V.assertScale(node, expected, tolerance)
    tolerance = tolerance or 0.01
    if type(node) == "string" then node = scene:GetChild(node, true) end
    if not node then V.fail("Node is nil"); return end
    local scale = node:GetScale()
    local dist = (scale - expected):Length()
    if dist > tolerance then
        V.fail(string.format("Node '%s' scale (%.2f,%.2f,%.2f) != expected",
            node:GetName(), scale.x, scale.y, scale.z))
    end
end

-- 近似比较辅助（GameDevBench 的 _float_matches / _color_close / approx_vec3）
function V.approxEqual(a, b, tolerance)
    tolerance = tolerance or 0.001
    return math.abs(a - b) <= tolerance
end

function V.approxVec3(a, b, tolerance)
    tolerance = tolerance or 0.1
    return (a - b):Length() <= tolerance
end

function V.approxColor(a, b, tolerance)
    tolerance = tolerance or 0.01
    return math.abs(a.r - b.r) <= tolerance
       and math.abs(a.g - b.g) <= tolerance
       and math.abs(a.b - b.b) <= tolerance
       and math.abs(a.a - b.a) <= tolerance
end

-- 资源检查（GameDevBench Category D）
function V.assertMaterial(node, materialPath)
    if type(node) == "string" then node = scene:GetChild(node, true) end
    if not node then V.fail("Node is nil"); return end
    local model = node:GetComponent("StaticModel") or node:GetComponent("AnimatedModel")
    if not model then V.fail("Node has no model component"); return end
    local mat = model:GetMaterial(0)
    if not mat then
        V.fail("Node '" .. node:GetName() .. "' has no material")
    elseif not mat:GetName():find(materialPath) then
        V.fail("Node '" .. node:GetName() .. "' material is " .. mat:GetName() .. ", expected " .. materialPath)
    end
end

-- 子节点数量检查
function V.assertChildCount(node, expected)
    if type(node) == "string" then node = scene:GetChild(node, true) end
    if not node then V.fail("Node is nil"); return end
    local count = node:GetNumChildren()
    if count ~= expected then
        V.fail(string.format("Node '%s' has %d children, expected %d",
            node:GetName(), count, expected))
    end
end

-- 物理检查
function V.assertHasRigidBody(node, isDynamic)
    local rb = V.assertHasComponent(node, "RigidBody")
    if rb and isDynamic ~= nil then
        local mass = rb:GetMass()
        if isDynamic and mass <= 0 then
            V.fail("RigidBody should be dynamic (mass > 0)")
        elseif not isDynamic and mass > 0 then
            V.fail("RigidBody should be static (mass = 0)")
        end
    end
    return rb
end

-- 最终结果
function V.finish()
    if passed then
        log:Write(LOG_INFO, "__VALIDATE_TEST__:PASSED")
    else
        log:Write(LOG_INFO, "__VALIDATE_TEST__:FAILED:" .. table.concat(issues, "; "))
    end
end

-- 导出
_G.V = V
return V
```

### 5.4 测试脚本示例

```lua
-- test.lua (对应一个具体游戏任务的验证脚本)

-- 1. 场景结构检查
V.assert(scene ~= nil, "Scene must exist")
V.assertNodeExists("Player", "CharacterController")
V.assertNodeExists("MainCamera", "Camera")
V.assertNodeExists("Ground", "StaticModel")

-- 2. 属性检查
V.assertPosition("Player", Vector3(0, 1, 0), 1.0)  -- 玩家在原点附近
V.assertHasRigidBody("Player", true)                 -- 动态刚体

-- 3. 组件配置
local light = V.assertNodeExists("DirectionalLight", "Light")
if light then
    local lightComp = light:GetComponent("Light")
    V.assert(lightComp:GetLightType() == LIGHT_DIRECTIONAL, "Must be directional light")
end

-- 4. 材质检查
V.assertMaterial("Ground", "Materials/Terrain")

-- 5. 子节点结构
V.assert(scene:GetNumChildren() >= 3, "Scene must have at least 3 child nodes")

-- 6. 输出结果
V.finish()
```

### 5.5 引擎侧集成

```cpp
// 在 UrhoXRuntimeValidate.cpp
void UrhoXRuntime::ExecuteValidationTest()
{
    auto* luaScript = GetSubsystem<LuaScript>();
    if (!luaScript) return;

    // 1. 加载辅助库
    String helpersPath = "Validate/validate_helpers.lua";
    luaScript->ExecuteFile(helpersPath);

    // 2. 加载测试脚本
    if (!luaScript->ExecuteFile(validateTestScript_))
    {
        validationCollector_->RecordError("lua",
            "Failed to load test script: " + validateTestScript_,
            validateFrameCounter_);
        return;
    }

    // 3. 解析结果（通过 log message 拦截）
    // __VALIDATE_TEST__:PASSED 或 __VALIDATE_TEST__:FAILED:reason
}
```

### 5.6 与 GameDevBench 断言模式的对应关系

| GameDevBench 断言类型 | UrhoX Lua 等价 | 覆盖 |
|----------------------|---------------|------|
| 节点存在 | `V.assertNodeExists(path, type)` | ✅ |
| 属性值 | `V.assertPosition()`, `V.assertScale()` | ✅ |
| 信号连接 | `V.assertEventHandler(node, event, handler)` | ⏳ 可扩展 |
| 资源路径 | `V.assertMaterial(node, path)` | ✅ |
| 脚本源码 | `io.open() + string.find()` | ✅ 原生 Lua |
| Shader 代码 | `mat:GetTechnique():GetPass():GetShader()` | ⏳ 需要 API |
| 运行时行为 | 需要帧间断言（见下文） | ⏳ Phase 3b |
| 粒子系统 | `V.assertHasComponent("ParticleEmitter")` | ✅ |
| 环境渲染 | Zone/Light 属性检查 | ✅ 通过组件 API |

### 5.7 Phase 3b: 帧间断言（运行时行为验证）

GameDevBench 的高级测试会跨帧验证行为（输入 → await → 检查状态变化）。UrhoX 等价方案：

```lua
-- test.lua 中定义帧回调
function ValidateFrame(frame)
    if frame == 5 then
        -- 输入已通过 scenario.json 在 frame 5 注入了 tap
        -- 在 frame 6 检查响应
    elseif frame == 6 then
        local player = scene:GetChild("Player", true)
        V.assert(player ~= nil, "Player should exist after tap")
        -- 验证游戏响应了输入
    elseif frame == 30 then
        local player = scene:GetChild("Player", true)
        local pos = player:GetPosition()
        V.assert(pos.z > 1.0, "Player should have moved forward after WASD input")
    end
end
```

引擎在每个 validate 帧调用 `ValidateFrame(frameCounter)`（如果该函数存在）。

**工作量**: ~300 行 C++ + ~200 行 Lua (helpers)

---

## 6. Phase 4：Benchmark Runner

**目标**: Python 编写的批量测试编排器，仿 GameDevBench 架构，支持沙盒隔离、AI Agent 集成、结果汇总。

**位置**: `tools/benchmark/` (独立于引擎代码)

### 7.1 目录结构

```
tools/benchmark/
├── urhox_bench/
│   ├── __init__.py
│   ├── runner.py             # BenchmarkRunner 主类
│   ├── solver_base.py        # BaseSolver 抽象类
│   ├── solver_claude.py      # Claude Code agent
│   ├── solver_factory.py     # Solver 注册/工厂
│   ├── sandbox.py            # 沙盒环境管理
│   ├── validator.py          # 验证结果解析
│   └── utils/
│       ├── constants.py
│       ├── data_types.py     # TaskResult, ValidationResult
│       └── prompts.py        # Prompt 模板
├── tasks/                    # 任务目录（scaffold 版本）
│   ├── task_0001/
│   │   ├── task_config.json  # {"instruction": "...", "category": "...", "difficulty": "..."}
│   │   ├── scripts/
│   │   │   ├── main.lua      # 不完整的游戏脚本
│   │   │   └── test.lua      # 测试脚本（沙盒中排除）
│   │   ├── scenarios/
│   │   │   └── test.json     # 输入注入场景（沙盒中排除）
│   │   └── resources/        # 资源文件
│   └── ...
├── tasks_gt/                 # Ground truth（完整解答）
│   └── task_0001/
│       └── scripts/
│           └── main.lua      # 正确实现
├── tasks.yaml                # 任务列表
├── pyproject.toml
└── README.md
```

### 7.2 任务流程（仿 GameDevBench）

```python
class BenchmarkRunner:
    def run_task(self, task_name: str) -> TaskResult:
        task_dir = self.tasks_dir / task_name

        # Step 1: 创建沙盒
        sandbox_dir = self._create_sandbox(task_dir)
        # 排除: test.lua, test.json, task_config.json(仅保留 instruction)

        # Step 2: AI Agent 在沙盒中编写/修改代码
        solver = SolverFactory.create(self.agent, self.model)
        solver_result = solver.solve_task(sandbox_dir, task_config["instruction"])

        # Step 3: 创建验证环境
        validation_dir = self._create_validation_env(sandbox_dir, task_dir)
        # 从 task_dir 注入 test.lua 和 test.json

        # Step 4: 运行 UrhoX validate
        validation_result = self._run_validation(validation_dir)

        # Step 5: 清理
        shutil.rmtree(sandbox_dir)
        shutil.rmtree(validation_dir)

        return TaskResult(task_name, solver_result, validation_result)
```

### 6.3 验证执行（两种模式）

**模式 A: 批处理（L1 快速烟雾测试）**

```python
def _run_validation_batch(self, validation_dir: Path) -> ValidationResult:
    cmd = [
        str(self.runtime_path), "main.lua",
        "-graphicsheadless", "-validate",
        f"-validate-frames={self.validate_frames}",
        f"-validate-timeout={self.validate_timeout}",
        f"-validate-output={validation_dir / 'report.json'}",
        f"-validate-test={validation_dir / 'scripts/test.lua'}",
        f"-tapcode_dir={validation_dir}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
    report = json.loads((validation_dir / "report.json").read_text())
    return ValidationResult(success=report["result"] == "PASS", report=report)
```

**模式 B: 交互式（L2 AI 驱动验证）**

```python
def _run_validation_interactive(self, validation_dir: Path) -> ValidationResult:
    proc = subprocess.Popen(
        [str(self.runtime_path), "main.lua",
         "-graphicsheadless", "-validate-interactive",
         f"-tapcode_dir={validation_dir}"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
    )
    # AI agent 逐帧交互
    state = self._send_cmd(proc, {"cmd": "observe"})
    for frame in range(self.validate_frames):
        action = self.play_strategy.decide(state)  # AI/规则 决定输入
        state = self._send_cmd(proc, {"cmd": "step", "dt": 0.016, "input": action})
    report = self._send_cmd(proc, {"cmd": "finish"})
    return ValidationResult(success=report["result"] == "PASS", report=report)
```

Runner 根据任务配置选择模式：简单任务用批处理，复杂任务用交互式。

### 6.4 沙盒排除规则

```python
SANDBOX_EXCLUDE = {
    "files": {"test.lua", "test.json", "task_config.json", "task_validation.md"},
    "patterns": ["*.log", "*.bak"],
    "dirs": {".git", ".backup", "__pycache__"},
}
```

沙盒中创建精简的 `task_config.json`，仅含 `instruction` 字段。

### 6.5 结果汇总

```json
{
  "summary": {
    "total_tasks": 50,
    "passed": 32,
    "failed": 15,
    "errors": 3,
    "success_rate": 68.1,
    "agent": "claude-code",
    "model": "claude-opus-4-6"
  },
  "by_category": {
    "gameplay": {"total": 20, "passed": 15, "rate": 75.0},
    "graphics": {"total": 15, "passed": 8, "rate": 53.3},
    "ui": {"total": 10, "passed": 6, "rate": 60.0},
    "physics": {"total": 5, "passed": 3, "rate": 60.0}
  },
  "cost": {
    "total_usd": 12.50,
    "avg_per_task_usd": 0.25
  },
  "tasks": [
    {
      "name": "task_0001",
      "success": true,
      "category": "gameplay",
      "solver_duration_s": 45.2,
      "validate_result": "PASS",
      "validate_report": { /* ... full JSON report ... */ }
    }
  ]
}
```

**工作量**: ~800-1000 行 Python

---

## 7. JSON Report 格式

系统未上线，不需要向后兼容。直接使用最终格式。

### 7.1 批处理模式报告（-validate）

```json
{
    "script": "main.lua",
    "result": "PASS",
    "duration_ms": 1234,
    "frames_completed": 60,
    "phases": {
        "load":  {"result": "PASS", "errors": []},
        "init":  {"result": "PASS", "errors": []},
        "run":   {"result": "PASS", "errors": []},
        "scene": {"result": "PASS", "errors": [], "node_count": 12, "component_count": 25, "scene_exists": true}
    },
    "state_snapshots": [
        {"frame": 1,  "nodes": 3,  "components": 5,  "hash": 12345, "frame_time_ms": 8.2},
        {"frame": 30, "nodes": 12, "components": 25, "hash": 67890, "frame_time_ms": 3.8},
        {"frame": 60, "nodes": 12, "components": 25, "hash": 67890, "frame_time_ms": 4.0}
    ],
    "scene_stalled": false,
    "max_frame_time_ms": 8.2,
    "update_defined": true,
    "component_census": {"StaticModel": 5, "RigidBody": 3, "Light": 2, "Camera": 1},
    "test_result": "PASSED",
    "test_assertions": {"total": 8, "passed": 8, "failed": 0},
    "test_issues": [],
    "missing_resources": [],
    "summary": {"lua_errors": 0, "resource_errors": 0, "engine_errors": 0, "total_errors": 0}
}
```

### 7.2 交互模式逐帧响应（-validate-interactive）

每次 `step`/`observe` 返回：

```json
{
    "frame": 5,
    "scene": {
        "name": "Scene",
        "children": [
            {"name": "Player", "pos": [3.2, 1.0, 5.1], "components": [{"type": "RigidBody"}]},
            {"name": "Enemy", "pos": [10.0, 0.0, 5.0], "components": [{"type": "StaticModel"}]}
        ]
    },
    "ui": {
        "type": "Panel",
        "rect": [0, 0, 800, 600],
        "children": [
            {"type": "Button", "id": "startBtn", "text": "Start Game", "rect": [350, 400, 100, 40]},
            {"type": "Label", "text": "Score: 100", "rect": [10, 10, 80, 20]}
        ]
    },
    "errors": []
}
```

`finish` 命令返回与批处理模式相同格式的完整报告。

---

## 8. 文件清单

### 8.1 修改的文件

| 文件 | Phase | 改动 |
|------|-------|------|
| `engine/Source/Tools/UrhoXRuntime/UrhoXRuntime.h` | 1,2,3 | 新增成员变量和方法声明 |
| `engine/Source/Tools/UrhoXRuntime/UrhoXRuntime.cpp` | 1,2,3 | 参数解析、事件订阅、交互模式入口 |
| `engine/Source/Tools/UrhoXRuntime/UrhoXRuntimeValidate.cpp` | 1,3 | 多帧快照、测试脚本执行 |
| `engine/Source/Tools/UrhoXRuntime/ValidationCollector.h` | 1 | StateSnapshot 结构、新字段 |
| `engine/Source/Tools/UrhoXRuntime/CMakeLists.txt` | 2 | 新增源文件 |
| `engine/Source/Urho3D/Engine/Engine.h` | 2 | `SetNextTimeStep()` 方法声明 |
| `engine/Source/Urho3D/Engine/Engine.cpp` | 2 | `SetNextTimeStep()` 实现 |
| `docs/guides/runtime-validate-mode.md` | 1,2,3 | 文档更新 |

### 8.2 新增的文件

| 文件 | Phase | 说明 |
|------|-------|------|
| `engine/Source/Tools/UrhoXRuntime/ValidateInteractive.h` | 2 | 交互模式主循环 |
| `engine/Source/Tools/UrhoXRuntime/ValidateInteractive.cpp` | 2 | stdin/stdout 协议 + 场景/UI 序列化 |
| `engine/Source/Tools/UrhoXRuntime/ValidateInputInjector.h` | 2 | SDL 输入注入器 |
| `engine/Source/Tools/UrhoXRuntime/ValidateInputInjector.cpp` | 2 | SDL 事件构造 |
| `engine/bin/Data/Validate/validate_helpers.lua` | 3 | 断言辅助库 |
| `engine/bin/Data/Validate/serialize_scene.lua` | 2 | 场景树序列化 |
| `engine/bin/Data/Validate/serialize_ui.lua` | 2 | Widget 树序列化 |
| `tools/benchmark/` (整个目录) | 4 | Benchmark runner (Python) |

---

## 9. 实施顺序与依赖

```
Phase 1 ──────────────────► Phase 2 ──────────────────► Phase 3
增强被动观测                  交互式验证协议                Lua 断言框架
(~2 天)                       (~5 天)                       (~3 天)
无依赖                        依赖 Phase 1                  可与 Phase 2 并行

Phase 1-3 完成后 ─────────► Phase 4
                              Benchmark Runner
                              (~5 天)
                              依赖 Phase 1-3
```

| Phase | 预计工作量 | 可独立交付 | PR 策略 |
|-------|-----------|-----------|---------|
| Phase 1 | 2 天 | ✅ 是 | 单独 PR |
| Phase 2 | 5 天 | ✅ 是 | 单独 PR（核心工作量） |
| Phase 3 | 3 天 | ✅ 是 | 单独 PR |
| Phase 4 | 5 天 | ✅ 是 | 单独 PR（tools/ 目录） |

**总工作量**: ~15 天

---

## 附录 A：GameDevBench 关键设计借鉴

### A.1 防作弊沙盒（直接采用）

GameDevBench 的沙盒设计是防止 AI agent 读取测试条件的核心机制：

1. 复制任务目录到 `/tmp`
2. **排除**: `test.gd`, `test.tscn`, `task_config.json`（替换为仅含 instruction 的精简版）, `.log`, `.md`, 隐藏文件
3. Agent 在沙盒中工作
4. Agent 完成后，复制结果到新目录，从原始任务目录注入测试文件
5. 在注入了测试文件的目录中运行验证

**我们的适配**: 将 `test.gd`/`test.tscn` 替换为 `test.lua`/`test.json`，其余逻辑完全相同。

### A.2 断言模式分类（参考设计）

GameDevBench 133 个测试中使用了 9 类断言模式：

| 类型 | 使用频率 | UrhoX 等价难度 |
|------|---------|---------------|
| A: 节点存在 | 100+ | 低 — `scene:GetChild()` |
| B: 属性值 | 85+ | 低 — 组件 getter |
| C: 信号连接 | 17 | 中 — 需要事件系统 API |
| D: 资源路径 | 85 | 低 — `GetName()` |
| E: 脚本源码 | 12 | 低 — `io.open()` |
| F: Shader 代码 | 5 | 中 — 需 shader API |
| G: 运行时行为 | 42 | 高 — 需帧间断言 |
| H: 粒子系统 | 9 | 低 — 组件属性 |
| I: 环境渲染 | 17 | 低 — Zone/Light API |

### A.3 性能数据参考

| 指标 | GameDevBench | 启示 |
|------|-------------|------|
| 最强 agent 成功率 | 59.1% (GPT-5.3 Codex) | AI 写游戏仍然很难 |
| 图形类任务最难 | 31.6% | 视觉/空间推理是瓶颈 |
| 视觉反馈提升 | 14-42% | 给 agent 截图能力很重要 |
| 框架影响 > 模型影响 | 同模型差 3-18% | agent 工具链设计很关键 |

---

## 附录 B：TITAN 可用洞察

### B.1 采纳的概念

| TITAN 概念 | 我们的适配 | Phase |
|-----------|-----------|-------|
| 状态抽象 | 场景树 + UI 树 JSON 序列化（比截图更好） | 2 |
| 感知-动作循环 | Gym-style step/observe 协议 | 2 |
| 进度停滞检测 | `scene_stalled` 字段 + 状态 hash | 1 |
| 执行时间监控 | 逐帧耗时 + spike 检测 | 1 |
| 动作模板 | 输入注入事件类型（tap/key/touch） | 2 |

### B.2 不采纳的概念

| TITAN 概念 | 不采纳理由 |
|-----------|-----------|
| GPT-4o 视觉感知 | 我们有场景树 + UI 树直接访问，比截图更精确且零成本 |
| LLM 反射推理 | 交互协议让 AI 自己决定策略，不需要引擎内嵌推理 |
| 跨运行覆盖记忆 | 每个 AI 游戏只测一次 |
| RAG 动作过滤 | 每个游戏都不同，无法建库 |

### B.3 TITAN 数据参考

| 指标 | TITAN | 对我们的意义 |
|------|-------|-------------|
| 95% 任务完成率 | 自主 agent 能力上限 |
| 73% 状态覆盖 | 远超人类 QA (34%) |
| 82% bug 检出 | 人类只有 18% |
| 30% 误报率 | 可接受但需要人工复核 |
| 20 帧停滞阈值 | 可参考的停滞检测参数 |

---

*最后更新: 2026-04-02*
