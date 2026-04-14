# 02 · nO 主循环（TAOR Loop）

> **核心命题**：Runtime 是"哑循环"，所有智能在模型里。
> 这是从"代码控制模型"到"模型控制循环"的根本范式转变。

---

## TAOR 循环模型

```
┌─────────────────────────────────────────────┐
│                                             │
│   Think（推理）                              │
│   → Claude 分析当前状态，决定下一步行动        │
│                       │                    │
│                       ▼                    │
│   Act（工具调用）                            │
│   → 调用 Bash / Edit / View / Task 等工具   │
│                       │                    │
│                       ▼                    │
│   Observe（观察结果）                        │
│   → 工具执行结果追加到消息历史                 │
│                       │                    │
│                       ▼                    │
│   Repeat（继续或终止）                       │
│   → 还有工具调用？继续循环                    │
│   → 纯文本响应？自然终止，返回用户            │
│                       │                    │
└───────────────────────┘                    │
                         └──────────────────►┘
```

---

## 完整伪代码实现

```python
def master_loop(user_input: str) -> str:
    """
    nO 主循环 - Claude Code 核心执行引擎
    设计原则：Runtime 是哑循环，智能在模型里
    """
    # 单一扁平消息历史（非树状/多线程）
    history: List[Message] = [
        Message(role="user", content=user_input)
    ]

    while True:
        # ① Think：调用 Claude API 推理
        response = claude_api(
            messages=history,
            tools=AVAILABLE_TOOLS,    # 工具定义注入
            system=load_claude_md(),  # CLAUDE.md 作为系统提示
        )

        # ② 自然终止条件（非任意迭代上限！）
        if not response.has_tool_calls:
            return response.text      # 纯文本响应 → 返回用户

        # ③ Act + Observe：顺序执行所有工具调用
        for tool_call in response.tool_calls:
            # Hooks: PreToolUse 检查（可能拦截）
            if not pre_tool_use_hook(tool_call):
                history.append(Message(role="tool_result",
                                       content="[Hook 拦截：操作被阻止]"))
                continue

            # 执行工具
            result = tool_engine.execute(tool_call)

            # Hooks: PostToolUse 检查（质量门、格式化）
            post_tool_use_hook(tool_call, result)

            # 追加到扁平消息历史
            history.append(Message(role="tool_result", content=result))

            # TodoWrite Reminder 注入（防止目标漂移）
            if todo_manager.has_active_todos():
                history.append(todo_manager.get_reminder())

        # ④ h2A 实时转向队列检查
        # 用户在 Agent 运行中途是否注入了新指令？
        while h2A_queue.has_message():
            steering_msg = h2A_queue.pop()
            history.append(Message(role="user", content=steering_msg))

        # ⑤ Repeat：继续循环
```

---

## 关键设计决策

| 决策 | 放弃的方案 | 降低的不确定性 |
|------|-----------|-------------|
| 单线程主循环 | 多 Agent 蜂群 | 状态竞争、行为不可预测 |
| 扁平消息历史 | 树状 / 多线程对话 | 调试困难、行为不透明 |
| 自然终止（无工具调用）| 固定迭代上限 | 过早终止（反模式）|
| 顺序工具执行 | 并发工具执行 | 顺序依赖问题、竞态条件 |

---

## h2A 实时转向缓冲队列

### 问题背景

传统 Agent 一旦开始执行就很难"中途纠偏"——
要么等它跑完（可能方向错了），要么完全重启（丢失上下文）。

### h2A 解决方案

```
用户界面层
    │ 用户在 Agent 执行中途输入新指令
    ▼
h2A 异步双缓冲队列
    │ 非阻塞写入（不中断当前工具执行）
    ▼
主循环在每次工具调用完毕后检查队列
    │ 发现转向消息 → 追加到历史 → 下次推理时生效
    ▼
Claude 在下一次 Think 阶段看到新指令
    │ 自然调整后续行动
    ▼
无需重启会话，保留完整上下文
```

### 典型场景

```bash
# 用户启动任务：重构认证模块
claude "重构 src/auth/ 目录下的认证逻辑"

# Agent 开始执行中...（正在分析文件）

# 用户发现方向不对，注入新指令
# （无需 Ctrl+C 重启，直接在输入框输入）
> "等等，先只处理 login.ts，其他文件暂不动"

# h2A 队列接收到转向指令
# 当前工具调用完成后，Claude 看到新指令
# 自动调整计划，聚焦 login.ts
```

---

## 上下文窗口经济学

### 消息历史增长模型

```
初始状态：用户指令（~100 tokens）
    │
    ▼ 每次工具调用
    ├── Tool Call 请求（~50 tokens）
    ├── Tool Result 返回（50~2000 tokens，取决于工具类型）
    └── System Reminder（~100 tokens，如有 TODO）
    │
    ▼ 随任务进行，历史持续增长
    │
    ▼ 达到 92% 上下文阈值
    │
    ▼ Compressor wU2 触发
    ├── 清除旧工具调用输出（优先）
    ├── 总结早期对话
    └── 保留：用户关键指令 + 代码片段 + CLAUDE.md 规则
```

### Token 消耗优化

```
MCP 工具搜索（Tool Search）：
    · 只加载工具名称（轻量）
    · 按需加载工具 Schema（重）
    → 即使 10+ 个 MCP 服务器，启动开销极小

Skills 按需加载：
    · 只加载 Skill 描述（轻量）
    · 按需加载完整 Skill 内容（重）
    → 上下文始终精简
```

---

## 反模式：三种失效的终止机制

```
❌ 反模式 1：任意迭代上限
while iteration < MAX_ITER:  # 错误！
    ...
问题：任务可能在第 8 次迭代就完成，也可能需要 50 次。
      固定上限要么过早截断，要么浪费。

❌ 反模式 2：自然语言终止判断
if "任务完成" in response.text:  # 错误！
    break
问题：LLM 可能用不同措辞表达完成，也可能错误地声称完成。

❌ 反模式 3：无终止条件
while True:  # 危险！
    response = claude_api(...)
    execute_tools(response)
    # 忘记检查 has_tool_calls
问题：模型返回纯文本时无法停止，无限循环。

✅ 正确做法：
while True:
    response = claude_api(...)
    if not response.has_tool_calls:  # 程序性检查，确定性
        return response.text          # 自然终止
    execute_tools(response)
```

---

## 会话持久化

```
每个会话存储路径：
~/.claude/sessions/<session-id>/
├── transcript.jsonl        # 完整消息历史（JSONL 格式）
└── metadata.json           # 会话元数据（模型、时间、项目路径等）

恢复机制：
claude /resume              # 列出所有会话
claude /resume <session-id> # 恢复特定会话
    → 触发 SessionEnd Hook（当前会话）
    → 触发 SessionStart Hook（目标会话）
    → 完整上下文恢复

大会话优化：
    · 超过 5MB 的会话历史使用内存效率更高的加载方式
    · 自动分块读取，避免一次性加载全部历史
```
