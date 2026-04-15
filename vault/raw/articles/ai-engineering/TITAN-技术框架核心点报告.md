**TITAN-技术框架核心点报告**

***TITAN*** *— Testing Intelligent Trigger Agent for Novel bugs
基于 LangGraph + Qwen LLM 的自动化游戏测试智能体*

**1. 系统总览**

|  |
| --- |
| Plaintext ┌─────────────────────────────────────────────────────────────────┐ │ TITAN Agent (Python) │ │ │ │ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐ │ │ │ Perceive │→ │ Decide │→ │ Execute │→ │ Monitor │ │ │ │ 感知抽象 │ │ LLM推理 │ │ 动作执行 │ │ 诊断预言机 │ │ │ └──────────┘ └──────────┘ └──────────┘ └───────────────┘ │ │ ↑ ↑ │ │ │ │ ┌────────┐ ┌────────┐ │ │ │ │Reflect │←──── stuck ───────│Router │ │ │ │ │ LLM反思 │ └────────┘ │ │ │ └────────┘ │ │ │ └───────────────────────────────────────────┘ │ │ │ ↑ │ │ JSON ↓ │ JSON │ ├─────────────────────────────────────────────────────────────────┤ │ stdin/stdout 同步协议 │ ├─────────────────────────────────────────────────────────────────┤ │ Luna Engine (C + Lua) │ │ │ │ SDL2 渲染 ←→ Lua 游戏逻辑 ←→ \_getTestState() 状态导出 │ │ │ │ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐ │ │ │ Snake │ │ Tetris │ │ Flappy │ │ Breakout │ │Asteroids │ │ │ └────────┘ └────────┘ └────────┘ └──────────┘ └──────────┘ │ │ ┌────────┐ │ │ │ 2048 │ │ │ └────────┘ │ └─────────────────────────────────────────────────────────────────┘ |

**核心定位**: TITAN 是一个 **LLM 驱动的黑盒游戏测试智能体**。它不修改游戏代码，而是通过标准化的 JSON 协议与游戏进程通信，像人类测试员一样"玩"游戏，同时运行多个诊断预言机(Oracle)检测 Bug。

**2. 核心技术点一: 同步帧协议 (Sync Frame Protocol)**

**2.1 设计动机**

LLM 推理耗时 1-3 秒，而游戏帧率 60 FPS。异步模式下，LLM 还在思考时游戏已经结束。**同步协议让游戏"冻结"等待智能体决策**。

**2.2 协议时序**

|  |
| --- |
| Plaintext Luna Engine TITAN Agent  │ │  │── update(1/60) ──→ │  │── draw() ──→ │  │── emit state JSON ──────────────────→ │ ← 读取初始状态  │ │  │ ┌─ BLOCK (fgets) ─┐ │ ← LLM 推理 (任意时长)  │ │ 等待 stdin 输入 │ │  │ └──────────────────┘ │  │ │  │ ←──────── {"action":"keypressed", ───│ ← 发送动作  │ "key":"up"} │  │ │  │── process key ──→ │  │── update(1/60) ──→ │  │── draw() ──→ │  │── emit state JSON ──────────────────→ │ ← 读取结果  │ │  │ ┌─ BLOCK ─┐ │  │ │ 等待... │ │  │ ... ... |

**2.3 关键设计决策**

|  |  |  |
| --- | --- | --- |
| 决策 | 选择 | 原因 |
| 时间步长 | 固定 dt = 1/60s | 消除真实时间依赖，测试结果可复现 |
| I/O 模式 | 阻塞式 fgets() | 游戏帧率完全由智能体驱动 |
| 帧推进 | 1 命令 = 1 帧 | 精确控制，无帧跳过 |
| 空推进 | {"action":"tick"} | 允许不按键只观察的帧 |

**2.4 协议消息格式**

**Engine → Agent (stdout):**

|  |
| --- |
| JSON {  "type": "state",  "frame": 42,  "dt": 0.0166667,  "fps": 0.0,  "game\_state": { /\* 游戏特定状态 \*/ },  "error": null } |

**Agent → Engine (stdin):**

|  |
| --- |
| JSON {"action": "keypressed", "key": "up"} // 按键 {"action": "tick"} // 空推进 {"action": "screenshot", "path": "/tmp/x.bmp"} // 截图 {"action": "quit"} // 退出 |

**2.5 实现要点**

|  |
| --- |
| C // src/main.c — engine\_test\_loop() static void engine\_test\_loop(void) {  const double fixed\_dt = 1.0 / 60.0; // 固定时间步长   // 1. 运行初始帧，发射状态  engine.dt = fixed\_dt;  luna\_call\_callback(L, "update", 1, 0);  luna\_call\_callback(L, "draw", 0, 0);  test\_emit\_state(L); // Agent 可立即读取   // 2. 同步循环: 阻塞等待 → 处理 → 推进 → 发射  while (engine.running) {  char line[4096];  if (!fgets(line, sizeof(line), stdin)) break; // 阻塞!  test\_process\_line(L, line);  engine.dt = fixed\_dt;  luna\_call\_callback(L, "update", 1, 0);  luna\_call\_callback(L, "draw", 0, 0);  test\_emit\_state(L); // 1 命令 → 1 帧 → 1 状态  } } |

**3. 核心技术点二: LangGraph 状态机 (Agentic Workflow)**

**3.1 状态图结构**

|  |
| --- |
| Plaintext  ┌──────────────────────────────────────┐  │ │  ▼ │  ┌──────────┐ │  ┌──→ │ perceive │ ← tick() 推进一帧, 读取状态 │  │ └────┬─────┘ │  │ ▼ │  │ ┌──────────────────┐ │  │ │ optimize\_actions │ ← 基于状态过滤可用动作 │  │ └───────┬──────────┘ │  │ ▼ │  │ ┌──────────┐ │  │ │ decide │ ← 每 N 步调用 LLM 选择动作 │  │ └────┬─────┘ │  │ ▼ │  │ ┌──────────┐ │  │ │ execute │ ← send\_key() + read\_state() │  │ └────┬─────┘ │  │ ▼ │  │ ┌──────────┐ ┌──────────┐ │  │ │ monitor │──────→│ should\_ │ │  │ └──────────┘ │ continue │ │  │ └────┬─────┘ │  │ │ │  │ ┌────────────┼────────────┐ │  │ ▼ ▼ ▼ │  │ "perceive" "reflect" "report" │  │ │ │ │ │  └──────────────┘ │ ┌─┴─┐ │  ▼ │END│ │  ┌──────────┐ └───┘ │  │ reflect │───────────────┘  │ LLM 反思 │  └──────────┘ |

**3.2 状态定义 (TitanState)**

|  |
| --- |
| Python class TitanState(TypedDict):  # 环境  game\_name: str # "snake" | "tetris" | ...  config: dict # 游戏配置 (动作空间, 知识, 阈值)  driver: GameDriver # Luna 子进程管理器  llm: QwenClient # LLM 客户端   # 感知  frame\_data: dict # 引擎原始帧数据 (dt, fps, game\_state)  game\_state: dict | None # 游戏状态 (score, lives, position, ...)  abstract\_text: str # 自然语言状态描述 (给 LLM 的输入)   # 决策  actions: list[str] # 当前可用动作列表  chosen\_action: str # LLM 选择的动作   # 记忆  history: list[dict] # 滑动窗口: 最近 50 步 (防止上下文爆炸)  findings: list[dict] # 发现的所有问题  reflections: list[dict] # LLM 反思记录   # 控制  stuck\_counter: int # 连续无分数变化的步数  last\_score: float # 上一步得分  total\_steps: int # 累计步数  max\_steps: int # 最大步数限制  done: bool # 终止标志 |

**3.3 节点职责**

|  |  |  |
| --- | --- | --- |
| 节点 | 核心逻辑 | I/O |
| **perceive** | driver.tick() → 推进1帧 + 状态抽象 | 发送 tick, 读取 JSON, 生成自然语言 |
| **optimize\_actions** | 过滤当前状态下可用的动作 | game\_over → 只留 restart; start → 只留 space |
| **decide** | 每 N 步调用 LLM 选动作 (中间步复用上次选择) | LLM API 调用 (temperature=0.3) |
| **execute** | send\_key() → 读取结果 → 更新历史 | 发送按键, 读取状态, stuck 计数 |
| **monitor** | 运行诊断预言机 (crash/error/performance) | 纯内存检查 |
| **reflect** | LLM 分析为什么卡住 + 截图取证 | LLM API 调用 (temperature=0.2) |
| **report** | 标记 done=True | 无 I/O |

**3.4 条件路由 (should\_continue)**

|  |
| --- |
| Python def should\_continue(state: TitanState) -> str:  if state.get("done"): return "report"  if state["total\_steps"] >= state["max\_steps"]: return "report"  if state["stuck\_counter"] >= config["stuck\_threshold"]: return "reflect"  return "perceive" # 继续循环 |

**4. 核心技术点三: LLM 推理策略**

**4.1 频率控制 — 节省 API 调用**

|  |
| --- |
| Python DEFAULT\_LLM\_INTERVAL = 5 # 每 5 步调用一次 LLM  def decide\_node(state):  if step % DEFAULT\_LLM\_INTERVAL == 0 and len(actions) > 1:  chosen = decide\_action(llm, ...) # LLM 推理  else:  chosen = state["chosen\_action"] # 复用上次决策 |

**效果**: 300 步测试只需 ~60 次 LLM 调用，而非 300 次。

**4.2 决策提示词**

|  |
| --- |
| Plaintext System: 你是 TITAN, 自动化游戏测试智能体。目标是探索不同游戏状态, 发现 Bug。  游戏知识: {snake 的规则说明}  规则: 选一个动作, 探索不同状态, game over 时重启。  只回复动作名。  User: 当前状态: Snake game. Score: 30. Head at (12, 10), moving right. Food at (15, 8).  可用动作: up, down, left, right  最近 5 步历史: Step 25: right → score=30, Step 26: right → score=30, ...  选择下一个动作:  LLM → "up" |

**4.3 反思机制 — 卡住时的深度分析**

当 stuck\_counter >= stuck\_threshold (默认 20 步无分数变化) 时触发:

|  |
| --- |
| Plaintext System: 你是 TITAN, 分析为什么卡住了。  输出 JSON: {analysis, strategy, suspected\_bug, bug\_description}  User: 已经玩了 150 步, 连续 20 步没有分数变化。  当前状态: ...  最近 10 步操作和结果: ...  LLM → {  "analysis": "蛇在角落里循环移动, 无法接近食物",  "strategy": "尝试向食物方向移动, 避免重复路径",  "suspected\_bug": false,  "bug\_description": ""  } |

**如果 suspected\_bug: true**, 自动记录为 logic\_bug Finding，附带截图证据。

**4.4 LLM 客户端**

|  |
| --- |
| Python # 通过百炼 (Bailian/DashScope) API 调用 Qwen class QwenClient:  base\_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"  model = "qwen-turbo"  timeout = 60s   # OpenAI 兼容协议: POST /chat/completions  # 自动统计: total\_calls, total\_tokens |

**5. 核心技术点四: 诊断预言机系统 (Bug Detection Oracles)**

**5.1 预言机架构**

|  |
| --- |
| Plaintext Frame Data ──→ ┌──────────────┐ ──→ [Finding, Finding, ...]  │ CrashOracle │ crash / lua\_error (critical) Game State ──→ ├──────────────┤  │ HangOracle │ hang (important)  ├──────────────┤  │ LogicOracle │ logic\_bug (important)  ├──────────────┤  │ PerfOracle │ performance (minor)  └──────────────┘ |

**5.2 四个预言机详解**

**CrashOracle — 崩溃检测**

|  |
| --- |
| Plaintext 检测目标: 进程崩溃 + Lua 运行时错误 检测方式:  1. driver.is\_alive() == false → crash (critical)  2. frame\_data["type"] == "error" → lua\_error (critical) 证据收集: stderr 输出 / Lua 错误消息 + 回调函数名 |

**HangOracle — 卡死检测**

|  |
| --- |
| Plaintext 检测目标: 游戏状态完全冻结 检测方式: 对 game\_state 做 JSON 序列化后 hash  - 连续 N 帧 hash 相同 → hang (important)  - 默认阈值: 60 帧 重置机制: 报告后清零, 避免重复报告 |

**LogicOracle — 逻辑异常检测**

|  |
| --- |
| Plaintext 检测目标: 违反游戏规则的状态转换 检测规则:  1. 分数减少 (所有游戏分数只增不减) → logic\_bug  2. 生命值增加 (不应自然增加) → logic\_bug 状态跟踪: 保存 prev\_state 和 prev\_score 做帧间对比 |

**PerformanceOracle — 性能检测**

|  |
| --- |
| Plaintext 检测目标: 帧时间异常飙高 检测方式: dt > 0.1s (100ms) → performance (minor) 限制: 只报告前 3 次, 避免刷屏 注意: 同步模式下 dt 固定为 1/60, 此预言机主要检测 Lua 逻辑耗时 |

**5.3 Finding 数据结构**

|  |
| --- |
| Python {  "type": "crash" | "lua\_error" | "hang" | "logic\_bug" | "performance",  "severity": "critical" | "important" | "minor",  "step": 42,  "description": "Score decreased from 100 to 80",  "evidence": {"prev\_score": 100, "current\_score": 80} } |

**6. 核心技术点五: 状态感知与抽象 (Perception Layer)**

**6.1 三层状态转换**

|  |
| --- |
| Plaintext Lua 游戏对象 ──→ JSON 结构化数据 ──→ 自然语言描述 ──→ LLM 输入  (引擎内部) (\_getTestState) (abstract\_state) (prompt) |

**6.2 Lua 状态导出 (每个游戏实现 \_getTestState())**

|  |  |  |
| --- | --- | --- |
| 游戏 | 关键状态字段 | 决策关键信息 |
| **Snake** | snake[], food, dir, score, speed, game\_over | 蛇头→食物的相对位置, 移动方向 |
| **Tetris** | board[][], current\_type/x/y/rot, next\_type, lines\_cleared | 当前方块位置, 下一个方块类型 |
| **Flappy** | bird\_y, bird\_vy, pipes[], state, score | 鸟的高度/速度, 最近管道的间隙位置 |
| **Breakout** | paddle\_x, ball\_x/y, ball\_stuck, brick\_count, lives | 球和挡板的相对位置 |
| **Asteroids** | ship\_x/y/angle, asteroids\_count, bullets\_count, lives | 飞船朝向, 小行星数量 |
| **2048** | grid[4][4], score, best\_score, won, game\_over | 最大方块值, 空格数量 |

**6.3 自然语言抽象 (Python)**

|  |
| --- |
| Python # 原始 JSON: {"snake": [{"x":12,"y":10}], "food": {"x":15,"y":8}, "dir": {"x":1,"y":0}, "score": 30}  # 抽象为: "Snake game. Score: 30. Snake length: 3. Head at (12, 10), moving right.  Food at (15, 8). Grid: 20x20. Speed: 8 moves/sec. Game over: False." |

**设计原则**: 只保留决策相关信息，省略渲染细节，降低 Token 消耗。

**6.4 动态动作空间过滤**

|  |
| --- |
| Python def get\_actions(game\_name, config, game\_state):  if game\_over: return [restart\_key] # 只能重启  if state == "start": return ["space"] # 只能开始  if state == "ready": return ["space"] # 只能发球  return config["actions"] # 全部动作 |

**7. 核心技术点六: 游戏知识注入 (Per-Game Knowledge)**

**7.1 知识配置体系**

每个游戏有独立配置文件 (titan/game\_configs/<game>.py)，包含:

|  |
| --- |
| Python CONFIG = {  "name": "snake",  "path": "games/snake",  "actions": ["up", "down", "left", "right"], # 动作空间  "restart\_key": "r", # 重启键  "max\_steps": 500, # 默认最大步数  "stuck\_threshold": 30, # 反思触发阈值  "knowledge": """ # LLM 知识注入  Snake game on 20x20 grid.  Arrow keys change direction.  Eating food = +10 score.  Hitting wall or self = game over.  Speed increases with length.  """, } |

**7.2 知识注入方式**

知识文本作为 LLM System Prompt 的一部分注入，让 LLM 理解:

* 游戏规则和目标
* 操作方式和效果
* 可能的 Bug 表现

**8. 核心技术点七: 报告生成系统**

**8.1 输出文件**

|  |
| --- |
| Plaintext titan/ ├── reports/ │ └── 2026-03-26\_143052-snake-analysis.md # Markdown 分析报告 ├── logs/ │ └── 2026-03-26\_143052-snake.jsonl # 逐帧操作日志 /tmp/titan/ ├── screenshots/snake/ │ ├── reflect\_step\_150.bmp # 反思时截图 │ └── final.bmp # 最终截图 └── titan.log # 运行日志 |

**8.2 报告内容**

|  |
| --- |
| Markdown # TITAN Analysis Report: SNAKE  ## Summary | Metric | Value | |-------------------|-------| | Total steps | 300 | | Final score | 120 | | Max score reached | 150 | | Issues found | 2 | | Critical issues | 0 | | Important issues | 1 | | Minor issues | 1 | | Reflections | 3 |  ## Issues Found ### Issue 1: [IMPORTANT] logic\_bug Step: 142 Description: Score decreased from 150 to 120 Evidence: {"prev\_score": 150, "current\_score": 120}  ## Reflections Step 80: 蛇在角落循环移动... Step 120: 食物似乎生成在蛇身上...  ## Action Distribution | Action | Count | Percentage | |--------|-------|-----------| | right | 98 | 32.7% | | up | 75 | 25.0% | | down | 72 | 24.0% | | left | 55 | 18.3% | |

**9. 关键数据流**

**9.1 单步执行流 (每步 2 帧)**

|  |
| --- |
| Plaintext 步骤 N:   [perceive] tick() ──→ Game 推进 1 帧 ──→ 状态 JSON ──→ 自然语言抽象  │  [decide] LLM(状态 + 动作列表 + 历史) ──→ "up" │  │  [execute] send\_key("up") ──→ Game 处理按键, 推进 1 帧 ──→ 新状态  │  [monitor] 检查: 崩溃? 卡死? 逻辑异常? 性能? ──→ Findings  │  [route] done? → report | stuck? → reflect | → 步骤 N+1 |

**9.2 API 调用效率**

|  |
| --- |
| Plaintext 300 步测试:  - LLM 调用次数: ~60 (每 5 步 1 次) + 反思次数  - 每次调用 Token: ~200-500  - 总 Token: ~20,000  - 总耗时: ~2-5 分钟 (取决于 LLM 延迟) |

**10. 文件结构总览**

|  |
| --- |
| Plaintext game\_engine/ ├── src/main.c # 引擎主程序 (含同步测试循环) ├── src/luna.h # LunaEngine 全局结构体 │ ├── games/ │ ├── snake/main.lua # 各游戏 + \_getTestState() │ ├── tetris/main.lua │ ├── flappy/main.lua │ ├── breakout/main.lua │ ├── asteroids/main.lua │ └── 2048/main.lua │ ├── titan/ │ ├── \_\_init\_\_.py │ ├── config.py # 路径/API/阈值 配置 │ ├── llm\_client.py # Qwen LLM 客户端 (百炼 API) │ ├── game\_driver.py # Luna 子进程管理 (JSON IPC) │ ├── perception.py # 6 个游戏状态抽象器 │ ├── action.py # 动作空间过滤 + LLM 格式化 │ ├── reasoning.py # 决策/反思 Prompt 模板 │ ├── graph.py # LangGraph 状态机 (7 节点) │ ├── diagnosis.py # 4 个诊断预言机 │ ├── reporter.py # Markdown 报告生成 │ ├── main.py # CLI 入口 (--game/--all/--steps) │ └── game\_configs/ │ ├── \_\_init\_\_.py # 配置注册表 │ ├── snake.py │ ├── tetris.py │ ├── flappy.py │ ├── breakout.py │ ├── asteroids.py │ └── puzzle2048.py │ ├── scripts/ │ ├── titan-run.sh # 单游戏测试 │ ├── titan-run-all.sh # 全部游戏测试 │ └── titan-test.sh # 7 阶段单元测试 │ └── tests/  ├── test\_protocol.py # Stage 1: 引擎协议测试  ├── test\_states.py # Stage 2: 游戏状态导出测试  ├── test\_driver.py # Stage 3: Python 驱动器测试  ├── test\_perception.py # Stage 4: 感知+动作测试  ├── test\_agent.py # Stage 5: LangGraph 测试  ├── test\_diagnosis.py # Stage 6: 诊断预言机测试  └── test\_full\_pipeline.py # Stage 7: 全流水线测试 |

**11. 技术栈**

|  |  |  |
| --- | --- | --- |
| 层次 | 技术 | 版本/说明 |
| 游戏引擎 | C11 + Lua 5.4 + SDL2 | Luna Engine (Love2D 风格) |
| 智能体框架 | LangGraph | StateGraph 状态机 |
| LLM | Qwen (通义千问) | 通过百炼 DashScope API |
| HTTP 客户端 | httpx | OpenAI 兼容协议 |
| IPC | stdin/stdout JSON Lines | 同步阻塞模式 |
| 进程管理 | subprocess.Popen | 管道通信 |
| 报告格式 | Markdown + JSONL | 人类可读 + 机器可解析 |

**12. 设计原则总结**

1. **同步优于异步**: 阻塞式协议确保 LLM 有充足推理时间，游戏永远不会"跑在前面"
2. **固定 dt 保证可复现**: 消除真实时间依赖，相同输入序列产生相同结果
3. **频率控制节省成本**: 每 5 步调 1 次 LLM，中间复用上次决策
4. **滑动窗口防爆炸**: 历史记录只保留最近 50 步，避免 Token 无限增长
5. **预言机模式解耦**: 每个 Bug 检测器独立实现，可单独启用/禁用/扩展
6. **知识注入而非硬编码**: 游戏规则通过配置文件注入 LLM，新游戏只需加配置
7. **状态抽象降噪**: JSON → 自然语言，只保留决策相关信息
8. **证据链完整**: Finding + 截图 + 日志 + 反思，形成完整的 Bug 证据链