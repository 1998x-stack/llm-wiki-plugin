---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [技术, 工具]
aliases: [Codex Config System, Codex配置]
relates_to:
  - target: "[[Codex CLI]]"
    type: implements
    confidence: 0.95
  - target: "[[ExecPolicy]]"
    type: uses
    confidence: 0.8
  - target: "[[Codex沙箱系统]]"
    type: uses
    confidence: 0.8
  - target: "[[MCP协议层]]"
    type: uses
    confidence: 0.75
supersedes: null
---

# Codex配置系统

[[Codex CLI]] 的"神经系统"，控制每一个可调行为。不是简单的配置文件，而是一个**多层继承、可版本化、环境感知**的配置管理体系。

## 四大设计原则

1. **分层覆盖**：系统级 < 用户级 < 团队级 < 项目级 < Profile < 命令行
2. **Git 友好**：项目级配置在 `.codex/` 下，可提交版本控制
3. **环境感知**：dev/staging/prod 使用不同 Profile
4. **显式优于隐式**：安全关键配置（sandbox、approval）必须显式声明

## 配置层次（6 层）

| 层 | 路径 | 说明 |
|---|------|------|
| L1 系统级 | `/etc/codex/config.toml` | 企业 IT 管理员，用户不可覆盖 |
| L2 用户级 | `~/.codex/config.toml` | 个人偏好：默认模型、沙箱、MCP 服务器 |
| L3 团队级 | `{project}/.codex/config.toml` | 提交 Git，团队共享 |
| L4 子目录 | `{project}/src/auth/.codex/config.toml` | 特定目录专属配置 |
| L5 Profile | `~/.codex/config.toml [profiles.xxx]` | 按场景切换 |
| L6 命令行 | `codex -c key=value` | 单次覆盖，不影响配置文件 |

## 核心配置项

**模型**：`model = "gpt-5.4"` / `model_provider = "openai"` 或 `"oss"`（本地 Ollama）

**沙箱与审批**：
```toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"
# 精细 approval：
approval_policy = { granular = { mcp_elicitations = true, rules = true } }
```

**AGENTS.md**：项目根目录的项目级 Agent 指令文件（类似 CLAUDE.md），包含技术栈说明、代码规范、禁止操作等。Codex 启动时自动读取注入上下文。

**Shell 环境策略**：精细控制哪些 env var 传递给子进程，防止密钥泄露（默认自动排除含 `KEY/SECRET/TOKEN` 的变量）。

## Profile 系统

```toml
[profiles.strict]    # codex -p strict
sandbox_mode = "read-only"
approval_policy = "untrusted"

[profiles.auto]      # codex -p auto（CI 使用）
sandbox_mode = "danger-full-access"
approval_policy = "never"

[profiles.explore]   # codex -p explore
sandbox_mode = "read-only"
approval_policy = "never"
```

一条命令切换完整的配置集合。

## 动态覆盖

```bash
codex -c model='"gpt-5.4-mini"' "快速问题"               # 单次覆盖
codex -c sandbox_workspace_write.network_access=true "需要网络"
codex -c 'shell_environment_policy.include_only=["PATH"]' "隔离执行"
```

## Feature Flags

管理实验性功能：`unified_exec`（Stable）、`shell_snapshot`（Beta）、`multi_agents`（Stable）、`lifecycle_hooks`（Dev）。通过 `codex features enable/disable` 控制，持久化到 config.toml。

## 工程哲学

> **"约定优于配置"和"显式优于隐式"的平衡点**。大多数情况有合理默认值，安全关键决策强制显式声明。分层设计让个人、团队、企业在同一套体系上各取所需。

## 来源

- `raw/articles/ai-tools/codex/08_codex_config_system.md`
