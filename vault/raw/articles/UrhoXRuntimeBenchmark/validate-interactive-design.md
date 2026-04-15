# Validate Interactive Mode 设计文档

**状态**: 设计中
**日期**: 2026-04-03

## 概述

在现有 `-validate` 被动验证模式基础上，新增 `-validate-interactive` 交互式验证模式。引擎变成 **Gym-style 环境**：外部 AI Agent 通过 stdin/stdout JSON 协议逐帧控制引擎——注入输入、推进帧、观测场景树 + UI 树。

**动机**: 当前 validate 模式只能验证"脚本加载 + N 帧无 crash"，无法检测游戏是否真正运行（可能停在封面画面）。交互模式让 AI 能模拟玩家操作，验证游戏的实际交互行为。

---

## 现有架构

当前 `-validate` 是被动观测者，寄生在引擎主循环上：

```
Engine 主循环 (不变):
  while (!exiting_) {
      RunFrame()                          // 引擎自己计算 dt，自己 tick
        → E_BEGINFRAME
          → Input::Update()               // 处理 SDL 事件队列
        → E_UPDATE
          → HandleValidateUpdate(timeStep) // validate 只是旁观者
            - 累加 elapsed
            - 超时检查
            - 等待脚本加载
            - 计帧 + Phase 推进
            - 到达目标帧数 → 查场景 → 生成报告 → 退出
        → E_POSTUPDATE
        → E_RENDERUPDATE
        → E_ENDFRAME
  }
```

特点：
- **不控制时间** — 引擎自动计算 dt
- **不注入输入** — 无任何输入能力
- **只看日志** — 通过 `E_LOGMESSAGE` 拦截 ERROR 级别日志
- **只查一次场景** — 最后一帧统计 node/component 数量

### 关键问题：HandleValidateUpdate 的事件挂载点

现有实现中 `HandleValidateUpdate` 挂在 `E_UPDATE` 上。这在被动模式下没问题，但对交互模式来说是**错误的时序**：

```
E_BEGINFRAME    → Input::Update() → SDL_PollEvent() 已经执行完了
E_UPDATE        → HandleValidateUpdate() ← 如果在这里注入 SDL 事件...
```

在 `E_UPDATE` 中调用 `SDL_PushEvent` 注入的事件，要等到**下一帧**的 `E_BEGINFRAME` 才会被 `Input::Update()` 消费，产生 **1 帧延迟**。

**解决方案**：交互模式下将核心逻辑挂到 `E_BEFOREBEGINFRAME`，在 `Input::Update()` 之前完成阻塞等待和输入注入，实现同帧零延迟闭环。

---

## 交互模式设计

### 启动阶段：Bootstrap → Ready → 交互循环

交互模式分两个阶段：**自动启动阶段**和**交互循环阶段**。

```
阶段一：自动启动（不阻塞 stdin，引擎正常 tick）
  ┌─────────────────────────────────────────────────┐
  │  Engine 正常 RunFrame()                          │
  │  → Bootstrap 异步下载/加载资源                    │
  │  → ExecuteFile(main.lua) 成功                    │
  │  → 执行 Start()                                  │
  │  → validateScriptLoaded_ = true                  │
  │                                                  │
  │  此时引擎主动输出 ready 消息：                     │
  │  stdout ← {"status":"ready", "scene":{...},      │
  │            "ui":{...}, "errors":[]}               │
  │                                                  │
  │  ready 消息即初始观测，agent 无需额外 observe      │
  └──────────────────────┬──────────────────────────┘
                         │
                         ▼
阶段二：交互循环（E_BEFOREBEGINFRAME 阻塞等待 stdin）
  ┌─────────────────────────────────────────────────┐
  │  每帧：                                          │
  │    E_BEFOREBEGINFRAME  阻塞读 stdin              │
  │    E_BEGINFRAME        Input 处理注入事件         │
  │    E_UPDATE            游戏逻辑                   │
  │    E_ENDFRAME          收集观测 → 写 stdout       │
  └─────────────────────────────────────────────────┘
```

**关键设计**：
- Bootstrap 阶段引擎自由 tick，不受 stdin 控制（否则异步加载无法推进）
- `validateScriptLoaded_` 是已有机制，Bootstrap 完成 + 脚本加载成功后设为 true
- `ready` 消息是引擎主动推送的，agent 收到后才开始发命令——**无需额外握手协议**
- `ready` 自带初始场景/UI 状态，相当于免费的第一次 observe

### 核心控制流

交互模式复用引擎原有主循环，不新建循环。通过事件回调在帧的两端插入阻塞点：

```
Engine 主循环 (不变):
  while (!exiting_) {
      RunFrame()
        → E_BEFOREBEGINFRAME ← [阻塞读 stdin + SetNextTimeStep + SDL_PushEvent]
        → E_BEGINFRAME
          → Input::Update()  ← 处理刚注入的 SDL 事件（同帧，零延迟）
        → E_UPDATE
          → 游戏逻辑响应输入
        → E_POSTUPDATE
          → 物理等后处理
        → E_RENDERUPDATE
        → E_ENDFRAME        ← [收集场景树 + UI 树 → 写 stdout]
  }
```

**一帧内完整闭环**：注入 → 处理 → 响应 → 观测，没有延迟。

### 时序详解

```
E_BEFOREBEGINFRAME:
  if !validateScriptLoaded_:
      return  // Bootstrap 未完成，引擎自由 tick，不阻塞

  1. 阻塞读 stdin（等待 agent JSON 命令）
  2. 解析命令：
     - "observe": 返回缓存的上一帧观测 → 写 stdout → 不推进帧
     - "step":    解析 dt + events
                  Engine::SetNextTimeStep(dt)     // override 帧步长
                  遍历 events[] → SDL_PushEvent()  // 注入输入
                  return（让引擎继续跑这一帧）
     - "finish":  生成最终报告 → 写 stdout → engine_->Exit()

E_BEGINFRAME:
  Input::Update() → SDL_PollEvent() 处理上面注入的事件

E_UPDATE ~ E_POSTUPDATE:
  游戏逻辑 + 物理运行，响应本帧输入

E_ENDFRAME:
  收集观测（缓存到 lastObservation_）：
    - 场景树：Scene::SaveJSON()
    - UI 树：C++ Lua C API 直接读 Widget 树
    - 错误列表：本帧新增的 LOG_ERROR
  写 stdout → JSON 响应
```

### observe 命令

`observe` 不推进帧，返回缓存的上一帧末尾观测（`lastObservation_`）。

- 初始状态：`ready` 消息已包含初始观测，agent 通常不需要在第一帧前 observe
- 后续帧：每次 `step` 在 `E_ENDFRAME` 都会更新缓存，`observe` 直接返回缓存

### 为什么不新建主循环

引擎原有 `while(!exit) RunFrame()` 循环内部做了大量工作（音频、网络、渲染管线等）。用 `E_BEFOREBEGINFRAME` + `E_ENDFRAME` 两个钩子在帧的两端操作，不侵入引擎核心，改动最小且最安全。

### 异常处理（重点：Linux 环境）

主要部署环境为 Linux 无显卡服务器，需要处理以下异常场景：

#### 1. stdin EOF（agent 进程意外退出）

Agent 被 kill、OOM、Python 异常退出时，`read(stdin)` 收到 EOF。

**处理**：生成当前报告 → 写到 stderr 或 `-validate-output` 文件 → 引擎以非 0 退出码退出（区分正常 finish）。

#### 2. 非法 JSON

Agent 发送格式错误的数据。

**处理（容错模式）**：写错误响应到 stdout → 继续等下一条命令，不退出。

```json
← {"error": "invalid JSON", "message": "parse error at position 42"}
```

Agent 可以重试或修正命令。不因为一条坏消息终止整个会话。

#### 3. Lua 运行时错误

Lua 错误不会 crash 进程，只触发 `LOG_ERROR`。

**处理**：正常收集到 `errors` 数组，在下一次 step/observe 响应中返回给 agent。Agent 自行判断是否继续。

#### 4. 引擎 crash（SIGSEGV 等）

主线程崩溃，引擎无法自救。

**处理**：agent 侧 `proc.stdout.readline()` 返回空字符串 → agent 知道引擎死了。引擎侧不做处理。

#### 5. 帧内死循环（RunFrame 不返回）

游戏脚本 Update() 死循环，`RunFrame` 永远不返回，引擎主线程卡住。

**处理**：引擎侧无法自救。靠 agent 侧 `subprocess` 的 timeout 参数 kill 进程，或 Linux 用 `timeout` 命令包裹：

```bash
timeout 60 ./UrhoXRuntime main.lua -graphicsheadless -validate-interactive ...
```

#### 6. stdout 缓冲（Linux 经典坑）

Linux 非 TTY 环境下 stdout 默认**全缓冲**，JSON 可能攒在内核缓冲区不 flush，导致 agent `readline()` 永久阻塞。

**处理**：interactive 模式启动时关闭 stdout 缓冲：

```cpp
// 进入 interactive 模式时
setvbuf(stdout, NULL, _IONBF, 0);  // 无缓冲
```

或者每次写 stdout 后显式 `fflush(stdout)`。推荐前者，一次设置，避免遗漏。

---

## 输入注入

### 可行性验证（已确认）

1. **SDL_VIDEODRIVER=dummy 下事件队列正常** — dummy driver 只影响渲染，SDL 事件队列独立工作
2. **Input 子系统始终创建** — `Engine.cpp` 中 `new Input(context_)` 无条件执行
3. **SDL_PollEvent 每帧调用** — `Input::HandleBeginFrame()` → `Update()` → `SDL_PollEvent()` 循环
4. **引擎已有 SDL_PushEvent 先例** — `Input.cpp` 触摸模拟功能中已用 `SDL_PushEvent` 注入事件

### 注入方式

通过 `SDL_PushEvent` 注入原生 SDL 事件。游戏脚本无感知，行为与真实输入一致。

必须使用 `-graphicsheadless`（不是 `-headless`），确保 Graphics + Input 子系统都正常初始化。

---

## 帧步长控制

Agent 在 `step` 命令中指定 `dt`（秒）。引擎通过 `Engine::SetNextTimeStep(dt)` override 自动计算的帧步长。

`Engine::SetNextTimeStep` **已存在**，无需新增。

阻塞期间真实时间流逝不影响游戏逻辑，因为 dt 完全由 agent 控制。

---

## 通信协议

### 传输方式

**stdin/stdout JSON**，每行一条 JSON（`\n` 分隔）。

选择理由：
- Agent 用 `subprocess.Popen` 启动引擎，管道自动建立
- 零依赖、跨平台、Linux 无显卡环境可用
- LSP、Chrome DevTools Protocol 等成熟协议使用相同模式

### 日志隔离（使用引擎自带 quiet mode）

引擎 Log 子系统已有 quiet mode（`-q` 参数），interactive 模式下直接复用：

| 输出通道 | quiet mode 行为 | interactive 模式用途 |
|----------|----------------|---------------------|
| **stdout** | 完全静默（无任何日志输出） | 专用于协议 JSON |
| **stderr** | 仅输出 ERROR 级别 | agent 可选读取，用于诊断 |
| **文件日志** | 不受影响，照常写入全量日志 | 事后排查完整记录 |

无需修改引擎 Log 类。agent 启动引擎时加 `-q` 即可：

```bash
./UrhoXRuntime main.lua -graphicsheadless -validate-interactive -q -skip_login -tapcode_dir=...
```

```python
# Agent 侧
proc = subprocess.Popen(
    ["./UrhoXRuntime", "main.lua",
     "-graphicsheadless", "-validate-interactive",
     "-q",              # stdout 留给协议 JSON
     "-skip_login", f"-tapcode_dir={project_dir}"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,   # 协议 JSON
    stderr=subprocess.PIPE,   # 引擎 ERROR 日志（可选读取）
    text=True,
)
```

### 超时保护

stdin 读取设置超时（如 60s），agent 进程 crash 时引擎不会永远阻塞。

---

## 协议格式

### Agent → Engine（stdin）

#### observe（只读，不推进帧）

```json
{"cmd": "observe"}
```

#### step（注入输入 + 推进 1 帧）

```json
{"cmd": "step", "dt": 0.016, "events": [
    {"type": "SDL_KEYDOWN", "sym": "SDLK_w"},
    {"type": "SDL_KEYUP", "sym": "SDLK_w"},
    {"type": "SDL_MOUSEBUTTONDOWN", "x": 400, "y": 420, "button": 1},
    {"type": "SDL_MOUSEBUTTONUP", "x": 400, "y": 420, "button": 1},
    {"type": "SDL_MOUSEMOTION", "x": 100, "y": 200},
    {"type": "SDL_FINGERDOWN", "x": 0.5, "y": 0.5, "fingerId": 0},
    {"type": "SDL_MOUSEWHEEL", "y": 1}
]}
```

`events` 使用原生 SDL 事件类型命名（SDL_KEYDOWN、SDL_MOUSEBUTTONDOWN 等），理由：
- SDL 是公开标准，AI 训练数据大量覆盖，减少幻觉
- JSON 字段与 `SDL_Event` 结构 1:1 映射，C++ 侧无需翻译层
- 可扩展——未来加任何 SDL 事件类型不改协议

高层便捷操作（如 "tap" = MOUSEBUTTONDOWN + MOUSEBUTTONUP）在 agent Python 侧封装，引擎只处理原始 SDL 事件。

`events` 可选，不传则只推进帧不注入输入。`dt` 可选，默认 `1.0/60.0`。

#### finish（生成报告 + 退出）

```json
{"cmd": "finish"}
```

### Engine → Agent（stdout）

#### step / observe 响应

```json
{
    "frame": 5,
    "scene": { /* Scene::SaveJSON 完整输出 */ },
    "ui": {
        "type": "Panel",
        "rect": [0, 0, 800, 600],
        "children": [
            {"type": "Button", "id": "startBtn", "text": "Start Game", "rect": [350, 400, 100, 40]},
            {"type": "Label", "text": "Score: 0", "rect": [10, 10, 80, 20]}
        ]
    },
    "errors": [
        {"category": "lua", "message": "attempt to index a nil value", "frame": 5}
    ]
}
```

#### finish 响应

复用现有 `GenerateValidationReport` 格式（phases、missing_resources、summary 等）。

---

## 观测

### 场景树

使用引擎内置 `Scene::SaveJSON`，完整序列化所有节点、组件及属性。暴力但完整，先不做数据量裁剪。

### UI 树

C++ 通过 Lua C API 直接操作 Lua 栈读取 Widget 树，构建 JSONValue：

```
C++ 侧流程：
1. lua_getglobal(L, "UI")              // UI 模块
2. lua_getfield(L, -1, "GetRoot")      // GetRoot 函数
3. lua_call(L, 0, 1)                   // 调用，root Widget 在栈顶
4. 递归遍历 Widget 的 Lua table：
   - lua_getfield → "_className"        → type（Button/Label/Panel...）
   - lua_getfield → "id"                → id
   - lua_getfield → "props"             → text/visible/disabled 等
   - 调用 GetAbsoluteLayout()           → rect {x, y, w, h}
   - lua_getfield → "children"          → 递归子节点
5. 直接构建 JSONValue，无字符串序列化开销
```

优势：不走 Lua→string→C++ 的中间路径，C++ 直接从栈上读数据写 JSON。Widget 结构固定，字段名已知。

### 错误列表

复用现有 `HandleValidateLogMessage` 机制，收集本帧新增的 `LOG_ERROR` 级别日志。

---

## SDL 事件映射

C++ 侧解析 JSON events 数组，逐条构造 `SDL_Event` 并 `SDL_PushEvent`：

| JSON type | SDL 事件类型 | 关键字段 |
|-----------|-------------|----------|
| `SDL_KEYDOWN` | `SDL_KEYDOWN` | `sym`（如 "SDLK_w"）→ `SDL_Keycode` |
| `SDL_KEYUP` | `SDL_KEYUP` | `sym` |
| `SDL_MOUSEBUTTONDOWN` | `SDL_MOUSEBUTTONDOWN` | `x`, `y`, `button`（1=左 2=中 3=右） |
| `SDL_MOUSEBUTTONUP` | `SDL_MOUSEBUTTONUP` | `x`, `y`, `button` |
| `SDL_MOUSEMOTION` | `SDL_MOUSEMOTION` | `x`, `y` |
| `SDL_MOUSEWHEEL` | `SDL_MOUSEWHEEL` | `x`, `y`（滚动方向） |
| `SDL_FINGERDOWN` | `SDL_FINGERDOWN` | `x`, `y`（0-1 归一化）, `fingerId` |
| `SDL_FINGERUP` | `SDL_FINGERUP` | `x`, `y`, `fingerId` |
| `SDL_FINGERMOTION` | `SDL_FINGERMOTION` | `x`, `y`, `fingerId` |

Key 名称解析：维护 `HashMap<String, SDL_Keycode>` 映射表（"SDLK_w" → `SDLK_w` 等）。

---

## 文件清单

### 修改的文件

| 文件 | 改动 |
|------|------|
| `engine/Source/Tools/UrhoXRuntime/UrhoXRuntime.h` | 新增 interactive 模式成员变量和方法声明 |
| `engine/Source/Tools/UrhoXRuntime/UrhoXRuntime.cpp` | `-validate-interactive` 参数解析、事件订阅 |
| `engine/Source/Tools/UrhoXRuntime/UrhoXRuntimeValidate.cpp` | interactive 模式的事件处理逻辑 |
| `engine/Source/Tools/UrhoXRuntime/ValidationCollector.h` | 新增逐帧错误追踪 |
| `engine/Source/Tools/UrhoXRuntime/CMakeLists.txt` | 新增源文件（如有） |

### 新增的文件

| 文件 | 说明 |
|------|------|
| `engine/Source/Tools/UrhoXRuntime/ValidateInputInjector.h` | SDL 事件注入器（JSON → SDL_Event → SDL_PushEvent） |
| `engine/Source/Tools/UrhoXRuntime/ValidateInputInjector.cpp` | 事件构造 + key 名称映射 |

---

## CLI 参数

```
-validate-interactive     启用交互式验证模式（与 -validate 互斥）
```

与 `-validate` 互斥。进入交互模式后，引擎完成脚本加载 + `Start()`，然后在 `E_BEFOREBEGINFRAME` 阻塞等待 stdin 命令。

仍然需要配合 `-graphicsheadless` 和 `-skip_login` 使用。

---

## Agent 侧示例（Python）

```python
import subprocess, json

proc = subprocess.Popen(
    ["./bin/UrhoXRuntime", "main.lua",
     "-graphicsheadless", "-validate-interactive",
     "-skip_login", "-tapcode_dir=/path/to/project"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL, text=True,
)

def send(cmd):
    proc.stdin.write(json.dumps(cmd) + "\n")
    proc.stdin.flush()
    return json.loads(proc.stdout.readline())

# 1. 观测初始状态
state = send({"cmd": "observe"})

# 2. 看到 Button，点击它
for widget in state.get("ui", {}).get("children", []):
    if widget.get("type") == "Button":
        cx = widget["rect"][0] + widget["rect"][2] // 2
        cy = widget["rect"][1] + widget["rect"][3] // 2
        state = send({"cmd": "step", "dt": 0.016, "events": [
            {"type": "SDL_MOUSEBUTTONDOWN", "x": cx, "y": cy, "button": 1},
            {"type": "SDL_MOUSEBUTTONUP", "x": cx, "y": cy, "button": 1},
        ]})
        break

# 3. 跑几帧观察变化
for _ in range(60):
    state = send({"cmd": "step", "dt": 0.016})

# 4. 结束
report = send({"cmd": "finish"})
print(report["result"])
```

---

*最后更新: 2026-04-03*
