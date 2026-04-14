# 04 · Hooks 系统（21 个生命周期事件）

> **核心命题**：Prompts suggest, Hooks guarantee.
> Hooks 是 Claude Code 将"概率性 LLM 行为"转化为"确定性执行"的核心机制。
> 它们运行在 LLM 之外，不受模型推理影响，每次执行方式完全一致。

---

## 概率合规 vs 确定性控制

| 方式 | 第 1 次 | 第 10 次 | 第 47 次（上下文耗尽后）| 可靠性 |
|------|---------|---------|----------------------|--------|
| CLAUDE.md 写"总要 Lint" | 遵守 | 遵守 | **可能跳过** | 概率性 |
| PostToolUse Hook 触发 Lint | **执行** | **执行** | **执行** | 确定性 |

---

## Hook 执行流程

```
Claude Code 执行 → 特定事件触发 → Matcher 正则评估
                                          │
                                    命中 Matcher？
                                    ├─ 否 → 跳过
                                    └─ 是 → 执行 Hook Handler
                                                │
                                          Handler 返回
                                          ├─ exit 0   → 允许继续
                                          ├─ exit 1   → 警告，继续
                                          └─ exit 2   → 【阻断】
```

---

## 全部 21 个生命周期事件

### 会话生命周期

| 事件 | 触发时机 | 可阻断 | 典型用途 |
|------|---------|-------|---------|
| `Setup` | `--init` / `--maintenance` 标志 | 否 | 仓库初始化、依赖安装 |
| `SessionStart` | 会话启动 / 恢复 / `/clear` / `/compact` | 否 | 注入环境上下文、注入当前分支信息 |
| `SessionEnd` | 会话退出 / SIGINT / 错误终止 | 否 | 导出指标、生成会话摘要 |

### 主对话循环

| 事件 | 触发时机 | 可阻断 | 典型用途 |
|------|---------|-------|---------|
| `UserPromptSubmit` | 用户提交后、Claude 处理前 | **是** | Prompt 校验、注入额外上下文 |
| `PreToolUse` | 工具调用前 | **是（最强）** | 安全门、危险命令阻断、输入改写 |
| `PermissionRequest` | Claude 请求工具权限时 | **是** | 自动授权受信命令 |
| `PostToolUse` | 工具成功执行后 | 否（事后）| 自动 Lint、测试触发、质量检查 |
| `PostToolUseFailure` | 工具执行失败后 | 否 | 错误日志、告警通知 |
| `Notification` | Claude 发送通知时（异步）| 否 | 桌面通知、Slack 告警 |
| `Stop` | Claude 完成当前响应时 | **是（exit 2）** | 强制继续工作（质量不达标时）|

### 子 Agent 生命周期

| 事件 | 触发时机 | 典型用途 |
|------|---------|---------|
| `SubagentStart` | 子 Agent 启动时 | DB 连接初始化、环境准备 |
| `SubagentStop` | 子 Agent 完成时 | 清理、汇总、质量验证 |

### 上下文维护

| 事件 | 触发时机 | 典型用途 |
|------|---------|---------|
| `PreCompact` | 上下文压缩触发前 | 保护关键信息不被压缩丢失 |
| `ConfigChange` | CLAUDE.md 或 rules/*.md 加载时 | 配置文件监控（仅观察，不可控制）|

### MCP & Elicitation

| 事件 | 触发时机 | 典型用途 |
|------|---------|---------|
| `Elicitation` | MCP 服务器发起结构化输入时 | 拦截并自动响应，无需用户弹窗 |
| `ElicitationResult` | 用户完成 Elicitation 输入后 | 修改或覆盖用户响应 |

---

## 四种处理器类型

| 类型 | 机制 | 可靠性 | 速度 | 适用场景 |
|------|------|--------|------|---------|
| `command` | Shell 脚本 | **确定性** | 最快 | 安全门、格式化、测试 |
| `http` | HTTP POST 到 URL | **确定性** | 快 | CI/CD webhook、审计、通知 |
| `prompt` | LLM 语义评估 | 概率性 | 慢（需 API 调用）| 代码质量语义分析 |
| `agent` | 多步骤 Agent 分析 | 概率性 | 最慢 | 综合代码审查、深度安全审计 |

> **核心原则**：安全边界用 `command`（确定性），质量评估可用 `prompt`（概率性）。
> 永远不要用概率性处理器保护硬性安全约束。

---

## Exit Code 规则

```bash
exit 0  → 允许继续执行（或省略 JSON 中的 decision 字段）
exit 1  → 记录非阻断错误，继续执行（警告）
exit 2  → 【阻断】：
          · 在 PreToolUse → 停止工具调用
          · 在 Stop       → 强制 Claude 继续工作
          · 在 UserPromptSubmit → 阻止 Prompt 提交
```

---

## 完整配置示例

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$CLAUDE_TOOL_INPUT\" | grep -qE 'rm -rf|DROP TABLE|git push --force' && exit 2 || exit 0",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "check_file_ownership.sh \"$CLAUDE_TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ],

    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\"",
            "timeout": 30
          },
          {
            "type": "command",
            "command": "npx eslint --fix \"$CLAUDE_TOOL_INPUT_FILE_PATH\"",
            "timeout": 30
          }
        ]
      }
    ],

    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"additionalContext\": \"Branch: '$(git branch --show-current)' | Uncommitted: '$(git status --short | wc -l)' files\"}'"
          }
        ]
      }
    ],

    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "run_tests.sh && exit 0 || exit 2"
          }
        ]
      }
    ]
  }
}
```

---

## 在 Skills / Agents Frontmatter 中使用 Hooks

```yaml
---
name: secure-operations
description: 带安全检查的操作技能
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
  Stop:                    # 在子 Agent 中自动转为 SubagentStop
    - hooks:
        - type: command
          command: "./scripts/validate-output.sh"
---
你是一个安全操作 Agent...
```

---

## HTTP Hook（外部服务集成）

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "https://security.internal/hooks/pre-bash",
            "timeout": 30,
            "headers": {
              "Authorization": "Bearer $SECURITY_TOKEN"
            },
            "allowedEnvVars": ["SECURITY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

**HTTP Hook 关键差异**：
- 4xx / 5xx 状态码只记录错误，不阻断（继续执行）
- 要实际阻断，必须返回 2xx + `{"decision": "block", "reason": "..."}`

---

## PreToolUse 高级控制：输入改写

```json
// PreToolUse Hook 可以修改工具输入（v2.0.10+）
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": {
      "command": "npm run lint -- --fix"  // 自动添加 --fix 参数
    },
    "additionalContext": "已自动添加 --fix 标志以符合项目规范"
  }
}
```

修改对模型透明：Claude 不知道输入被改写，保持对话一致性。

---

## 审计日志 Hook（合规场景）

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date -u +%Y-%m-%dT%H:%M:%SZ) | Session:${CLAUDE_SESSION_ID} | Tool:${CLAUDE_TOOL_NAME} | User:${USER}\" >> /var/log/claude-audit.log"
          }
        ]
      }
    ]
  }
}
```

---

## 三层 Hook 策略（生产推荐）

```
安全层（Command Hook，100% 确定性）
    · 阻止 rm -rf / DROP TABLE / git push --force
    · 保护受限文件（生产配置、密钥文件）
    · 强制 Lint（每次文件写入后）

质量层（Prompt Hook，智能评估）
    · 代码可读性评估
    · API 设计合理性检查
    · 潜在安全漏洞识别（语义层）

审计层（HTTP Hook，外部记录）
    · 所有工具调用日志写入 SIEM
    · CI/CD Pipeline 触发
    · Slack / 钉钉 任务完成通知
```
