# Codex CLI 深度解析 Vol.5：Session Manager — Agent 记忆与上下文持久化

> **组件定位**：Session Manager 解决 Agent 的"失忆"问题。LLM 天然无状态，每次对话都是从零开始。Codex 通过持久化会话、Transcript 存储、Resume 机制，把 Agent 变成"有记忆的协作者"。

---

## 1. 核心问题：LLM 无状态 vs. 任务有状态

```
LLM 本身：
  每次 API 调用是独立的，没有内置记忆
  上下文窗口有限（即使 128k tokens 也有上限）
  
工程任务的特征：
  可能持续数小时甚至数天
  中途可能需要中断（开会、睡觉、切换任务）
  多步骤任务需要前一步的结果
  
Session Manager 的职责：
  在 LLM 无状态的基础上，构建有状态的任务上下文
```

---

## 2. Session 的数据结构

每个 Session 存储在 `~/.codex/sessions/<session_id>/` 下：

```
~/.codex/sessions/
└── 7f9f9a2e-1b3c-4c7a-9b0e-abcd12345678/
    ├── transcript.jsonl       # 完整对话记录（每行一条消息）
    ├── metadata.json          # Session 元数据
    ├── plan.json              # Agent 的任务计划快照
    └── approvals.log          # 人类审批记录
```

### 2.1 transcript.jsonl 格式

```jsonl
{"role":"user","content":"帮我重构 src/auth/ 目录","ts":1735000000}
{"role":"assistant","content":"我来分析当前结构...","tool_calls":[...],"ts":1735000010}
{"role":"tool","tool_use_id":"call_01","content":"<ls 输出>","ts":1735000011}
{"role":"assistant","content":"建议拆分为以下模块：...","ts":1735000020}
{"role":"user","content":"[APPROVAL] 同意执行文件重构","ts":1735000025}
```

**JSONL（JSON Lines）的选择原因：**
- 流式追加，不需要重写整个文件
- 崩溃安全：中断时只会丢失当前行，之前记录完整
- 可用 `jq` 直接分析：`cat transcript.jsonl | jq '.role'`

### 2.2 metadata.json

```json
{
  "session_id": "7f9f9a2e-1b3c-4c7a-9b0e-abcd12345678",
  "created_at": "2026-03-30T09:00:00Z",
  "workspace": "/Users/xm/myproject",
  "model": "gpt-5.4",
  "sandbox_mode": "workspace-write",
  "approval_policy": "on-request",
  "title": "重构 auth 模块",
  "parent_session_id": null,   // Fork 来源（若有）
  "git_commit": "a1b2c3d"      // 启动时的 HEAD commit
}
```

---

## 3. Resume 机制

### 3.1 Resume 的三种方式

```bash
# 方式 1：交互选择（展示最近会话列表）
codex resume

# 方式 2：直接跳到最近会话
codex resume --last

# 方式 3：指定 Session ID
codex resume 7f9f9a2e-1b3c-4c7a-9b0e-...

# 非交互模式（exec）的 resume
codex exec resume --last "继续上次的工作，现在处理 token 刷新逻辑"
```

### 3.2 Resume 的上下文恢复

Resume 时，Codex 不是简单地把整个 transcript 塞进上下文：

```
1. 加载 metadata.json（环境配置）
2. 读取 transcript.jsonl
3. 上下文压缩（若超过模型 context window）：
   - 保留所有 [APPROVAL] 记录（人类决策）
   - 保留关键 tool 结果（文件改动）
   - 压缩/摘要早期对话轮次
4. 注入 "continuation prompt"：
   "以下是之前会话的记录。继续执行用户的新指令..."
5. 恢复 approval_policy 和 sandbox_mode 设置
```

### 3.3 Resume 的不变量保证

```
原有 transcript → 只读，不修改
新的对话轮次   → 追加到 transcript
审批记录        → 原有审批在新 session 中依然有效

"Each resumed run keeps the original transcript,
 plan history, and approvals, so Codex can use
 prior context while you supply new instructions."
```

---

## 4. Fork 机制

Fork 让你从某个历史节点创建分支，尝试不同的解决方案：

```bash
codex resume --fork 7f9f9a2e-...
# 创建新 session，parent_session_id = 7f9f9a2e-...
# 原 session 保持不变，新 session 可以走不同路径
```

**工程场景：**
```
原 Session（已完成）：实现了方案 A
                      ↑
Fork ──────────────────┤
                       ├── Fork Session B：尝试更激进的重构
                       └── Fork Session C：保守修改，兼容旧接口
```

类比 Git 的分支，但在 Agent 对话层面操作。

---

## 5. Memories 系统

除 Session 之外，Codex 还有一个跨 Session 的**长期记忆层**：

```
~/.codex/memories/
├── workspace_prefs.md      # 工作区级偏好
└── global_knowledge.md     # 跨工作区知识
```

**Memories 的特殊保护：**  
在 `workspace-write` sandbox 模式下，`~/.codex/memories` 被自动添加到可写根路径。  
Agent 可以维护自己的记忆，但只能写到这个指定目录。

**Agent 更新记忆的方式：**  
Agent 通过工具调用写入 `~/.codex/memories/`，下次启动时，Codex 自动读取并注入到初始上下文。

---

## 6. Session 的生命周期

```
创建 (CREATE)
    │  用户首次运行 codex，或使用 /clear 开新会话
    ▼
活跃 (ACTIVE)
    │  对话进行中，实时 append transcript
    │
    ├── 中断 (INTERRUPTED)
    │     用户 Ctrl+C 或 /exit
    │     Session 自动保存，可 resume
    │
    ├── 完成 (COMPLETED)
    │     任务完成，用户主动结束
    │
    └── 超时 (TIMEOUT)
          长时间无活动，自动暂停
          
Resume → ACTIVE（从任何非活跃状态）
Fork   → 创建新的 ACTIVE Session（原 Session 不变）
Archive → 归档（从 session 列表隐藏，但数据保留）
```

---

## 7. exec 模式的 Session 管理

非交互的 `codex exec` 也有完整的 Session 管理：

```bash
# 非交互执行，结果流式输出到 stdout
codex exec "生成单元测试覆盖 src/auth/"

# 输出为 JSONL（适合脚本处理）
codex exec --output jsonl "重构 handler.go"

# 临时执行（不持久化到磁盘）
codex exec --ephemeral "快速回答：这个函数有什么问题？"
```

**--ephemeral 的工程价值：**  
CI/CD 环境中，不应该有 Session 残留。`--ephemeral` 保证执行后磁盘清洁。

---

## 8. Session 减少不确定性的方式

| 不确定性场景 | Session Manager 的应对 |
|------------|----------------------|
| 任务中途崩溃，进度丢失 | transcript.jsonl 流式写入，崩溃安全 |
| 上下文窗口超出限制 | 自动压缩，保留关键决策节点 |
| 不同方案需要并行探索 | Fork 机制创建分支 session |
| 重复告知 Agent 项目背景 | Resume 恢复完整上下文 |
| Agent "忘了"上次审批的决定 | approvals.log 持久化，resume 后有效 |
| 不知道 Agent 上次做了什么 | transcript 完整记录，可审计 |

---

## 9. 工程哲学摘要

> **Session Manager 的本质是在无状态 LLM 之上构建"可中断的工作记忆"。**
>
> 人类工程师可以中断工作去开会，回来后继续。
> Codex Session 让 AI Agent 也拥有同样的能力：
> 任何时刻中断，任何时刻恢复，上下文完整。
>
> 关键设计原则：**Transcript 只追加，不修改** — 这是系统可信任的基础。
> 审计、调试、恢复，都依赖这个不变性。

---

*下一篇：Vol.6 — MCP Layer：Agent 与外部世界的协议总线*
