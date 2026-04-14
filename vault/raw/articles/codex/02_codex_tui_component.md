# Codex CLI 深度解析 Vol.2：TUI — 交互式终端的设计哲学

> **组件定位**：TUI（Terminal UI）是 Codex CLI 的"驾驶舱"，不是简单的 REPL，而是一个完整的人机协同界面，承担实时审批、diff 预览、会话导航、多 Agent 状态展示等功能。

---

## 1. TUI 的本质问题

普通的命令行 chatbot 是**线性对话**：你输入 → 它输出 → 循环。  
Codex CLI TUI 要解决的是**并发 Agent 行为的可视化与控制**：

- Agent 正在后台执行多步工具调用
- 某一步需要人类审批
- 人类同时可能还在编辑 prompt
- 多个 subagent 并行跑不同任务

这要求 TUI 本质上是一个**事件驱动的状态机**，而不是传统的请求-响应界面。

---

## 2. TUI 的架构层次

```
┌─────────────────────────────────────────────────────────┐
│                      TUI 渲染层                           │
│   Ratatui / 原生终端  ─  全屏 alternate screen mode       │
├─────────────────────────────────────────────────────────┤
│                      事件处理层                           │
│   键盘输入  │  Agent 消息  │  Tool 结果  │  审批请求      │
├─────────────────────────────────────────────────────────┤
│                      状态管理层                           │
│   会话状态  │  Draft History  │  审批队列  │  Agent 树    │
├─────────────────────────────────────────────────────────┤
│                      Wire Protocol 接口                   │
│   ← codex-rs/core 通过 protocol crate 推送事件 →         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. 核心交互设计

### 3.1 Composer（输入框）

不是简单的文本输入，而是有以下能力：

```
┌─ Composer ──────────────────────────────────────────────┐
│ > 帮我重构 src/auth/ 目录，拆分出 oauth 模块...          │
│   [📎 screenshot.png]  [@context7]  [/skill:lua]        │
│                                                         │
│  Draft History: ↑↓ 浏览历史草稿（包含图片占位符）         │
└─────────────────────────────────────────────────────────┘
```

**关键能力：**
- 图片直接拖入（design spec、截图）
- `@` 引用 Skills、MCP 工具、代码片段
- Draft 历史：`Up/Down` 恢复之前的 prompt 草稿（包括未发送的图片附件）
- `Ctrl+L` 清屏不清上下文（≠ `/clear`，`/clear` 会开新 session）

### 3.2 实时 Diff 预览

Agent 提出文件修改时，TUI 直接渲染**语法高亮的 diff**：

```diff
--- a/src/auth/handler.go
+++ b/src/auth/handler.go
@@ -12,7 +12,7 @@
-func handleLogin(w http.ResponseWriter, r *http.Request) {
+func handleLogin(w http.ResponseWriter, r *http.Request) { // refactored
     token, err := validateOAuth(r)
```

用户可以：
- `[A]pprove` — 接受修改
- `[R]eject` — 拒绝并告诉 Agent 原因
- `/copy` — 复制最近完成的输出

### 3.3 Approval Gate UI

这是 TUI 最关键的人机协同节点：

```
╔══════════════════════════════════════════════════════════╗
║  ⚠  Codex wants to run:                                  ║
║                                                          ║
║   $ rm -rf dist/ && npm run build                        ║
║                                                          ║
║  [A] Allow once    [S] Allow session    [D] Deny         ║
╚══════════════════════════════════════════════════════════╝
```

**Approval 粒度（approval_policy）：**

| 模式 | 含义 | 适用场景 |
|------|------|---------|
| `untrusted` | 只允许已知安全的只读操作自动执行 | 新仓库/高风险环境 |
| `on-request` | Agent 遇到需要时才暂停询问（推荐交互模式）| 日常开发 |
| `never` | 全自动，不暂停（配合外部沙箱使用）| CI/自动化脚本 |
| `granular` | 精细到每类动作独立配置 | 高级定制 |

### 3.4 `/` 命令系统

TUI 内置斜杠命令，形成一套"内部 CLI"：

| 命令 | 功能 |
|------|------|
| `/model` | 切换模型（gpt-5.4 / gpt-5.3-codex / spark）|
| `/clear` | 清除上下文，开启新会话 |
| `/review` | 用独立 Agent 对当前代码做 Code Review |
| `/status` | 显示当前 Session ID、配置摘要 |
| `/copy` | 复制最近完成输出 |
| `/theme` | 预览并保存终端配色主题 |
| `/permissions` | 切换到只读模式（计划阶段不执行）|
| `/plugins` | 浏览已安装的 Codex Plugins |
| `/title` | 为当前 session 设置可读标题 |
| `/exit` | 关闭 TUI 会话 |

---

## 4. Alternate Screen 模式

TUI 默认使用终端的 **alternate screen buffer**（类似 vim 进入时终端清屏，退出时恢复）：

```
优点：
✓ 全屏体验，不污染 shell history
✓ 退出后终端恢复到启动前状态

缺点：
✗ 无法用 less/more 翻阅之前的输出
✗ 某些终端模拟器支持不完整

可通过 --no-alternate-screen 禁用：
  codex --no-alternate-screen
  tui.alternate_screen = false  # config.toml
```

---

## 5. App Server 模式

TUI 不是唯一的前端。Codex 支持 **App Server 模式**：

```bash
codex app-server  # 启动本地 WebSocket 服务器
```

这让 IDE Extension（VS Code）、桌面 App、以及未来的 Web 前端都能接入同一个 `core`。

```
┌──────────────────────────────────────────┐
│          codex-rs/core                    │
│    (会话状态、Agent 循环、工具执行)         │
└──────┬───────────┬───────────┬───────────┘
       │           │           │
   TUI 前端    App Server   IDE Extension
  (终端渲染)   (WebSocket)   (VS Code)
```

App Server 客户端可以：
- 发送 `!` shell 命令
- 监听文件系统变更
- 通过 bearer-token 鉴权连接远程 WebSocket

---

## 6. 减少不确定性的 TUI 设计

| 不确定性来源 | TUI 的应对设计 |
|-------------|--------------|
| Agent 执行了什么，我不知道 | 实时展示每个 tool call 和其输出 |
| 我不知道 Agent 要改哪些文件 | diff 预览在审批前可见 |
| Agent 误操作了，想撤销 | Session resume + git 快照回溯 |
| 多个任务并行，状态混乱 | `/title` 命名 session，parallel session 面板 |
| 不知道 Agent 用的什么模型 | `/status` 实时展示配置摘要 |
| Draft 写了一半，意外关闭 | Draft history 自动保存，Up/Down 恢复 |

---

## 7. 工程哲学摘要

> **TUI 的本质是"人类监督带宽的最大化"**。
>
> Agent 的速度远超人类审阅速度。TUI 的设计目标不是展示所有信息，
> 而是在关键决策点**精确呈现恰好需要的上下文**，让人类能在 2 秒内做出正确判断。

这背后的工程原则：
1. **最小化审批摩擦** — 常见的安全操作自动放行
2. **最大化审批信息** — 危险操作展示完整 diff + 命令意图
3. **可逆性优先** — 所有 session 有 transcript，所有文件改动可 git 回滚

---

*下一篇：Vol.3 — Sandbox System：把 AI 关进 OS 的笼子*
