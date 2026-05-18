---
type: concept
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-19
last_accessed: 2026-04-19
source_count: 3
tags: [技术, 工具, Agent系统]
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
  - target: "[[Agent可组合性]]"
    type: enables
    confidence: 0.7
  - target: "[[Ollama]]"
    type: uses
    confidence: 0.7
  - target: "[[OpenTelemetry]]"
    type: uses
    confidence: 0.75
supersedes: null
---

# Codex配置系统

[[Codex CLI]] 的"神经系统"，控制每一个可调行为。不是简单的[[Configuration|配置]]文件，而是一个**多层继承、可版本化、环境感知**的[[Configuration|配置]]管理体系。

## 四大设计原则

1. **分层覆盖**：系统级 < 用户级 < 团队级 < 项目级 < Profile < 命令行
2. **Git 友好**：项目级[[Configuration|配置]]在 `.codex/` 下，可提交版本控制
3. **环境感知**：dev/staging/prod 使用不同 Profile
4. **显式优于隐式**：安全关键[[Configuration|配置]]（sandbox、approval）必须显式声明

## 配置层次（6 层）

| 层 | 路径 | 说明 |
|---|------|------|
| L1 系统级 | `/etc/codex/config.toml` | 企业 IT 管理员，用户不可覆盖 |
| L2 用户级 | `~/.codex/config.toml` | 个人偏好：默认模型、[[Claude Code 沙箱机制|沙箱]]、[[MCP 服务器]] |
| L3 团队级 | `{project}/.codex/config.toml` | 提交 Git，团队共享 |
| L4 子目录 | `{project}/src/auth/.codex/config.toml` | 特定目录专属[[Configuration|配置]] |
| L5 Profile | `~/.codex/config.toml [profiles.xxx]` | 按场景切换 |
| L6 命令行 | `codex -c key=value` | 单次覆盖，不影响[[Configuration|配置]]文件 |

## 核心配置项

**模型**：`model = "gpt-5.4"` / `model_provider = "openai"` 或 `"oss"`（本地 [[Ollama]]）

**Review 独立模型**：`[review]` 段可指定独立模型（如 `gpt-5.4-mini`），review 作为独立 Agent 可用更便宜的模型。

**[[Environment Variables|环境变量]]覆盖**：`CODEX_CONFIG_PATH` 可指定[[Configuration|配置]]文件路径，`CODEX_MODEL` 等部分[[Configuration|配置]]支持 env 直接覆盖。

**[[Claude Code 沙箱机制|沙箱]]与审批**：
```toml
sandbox_mode = "workspace-write"  # read-only | workspace-write | danger-full-access
# workspace-write 细节：
[sandbox_workspace_write]
network_access = false           # 是否允许网络（默认禁止）
exclude_tmp = false              # 是否从可写根排除 /tmp
exclude_tmpdir = false           # 是否从可写根排除 $TMPDIR
extra_writable_roots = [         # 额外允许写的目录
  "/tmp/build_cache"
]
# 审批策略
approval_policy = "on-request"
# 精细 approval：
approval_policy = { granular = {
  sandbox_approval = true,       # 需要逃出沙箱时询问
  rules = true,                  # execpolicy prompt 规则触发时询问
  mcp_elicitations = true,       # MCP 请求额外权限时询问
  request_permissions = false,   # 自动拒绝 request_permissions
  skill_approval = true,         # Skill 脚本执行时询问
} }
```

**AGENTS.md**：项目根目录的项目级 Agent 指令文件（类似 CLAUDE.md），包含技术栈说明、代码规范、禁止操作等。Codex 启动时自动读取注入上下文。

AGENTS.md 相关配置：
```toml
[project]
agents_md_max_bytes = 65536              # 最大读取字节数
agents_md_fallback_names = [             # AGENTS.md 不存在时的备选文件名
  "CLAUDE.md", "COPILOT_INSTRUCTIONS.md"
]
project_root_markers = [                 # 项目根目录标识文件
  ".git", "package.json", "Cargo.toml", "go.mod"
]
trust = "trusted"                        # trusted | untrusted（不信任的项目跳过项目级 .codex/）
```

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

管理实验性功能，通过 `codex features enable/disable` 控制，持久化到 config.toml：

| Flag | 状态 | 功能 |
|------|------|------|
| `unified_exec` | Stable | 统一执行引擎 |
| `shell_snapshot` | Beta | 执行前 shell 状态快照 |
| `multi_agents` | Stable | subagent 工具集 |
| `lifecycle_hooks` | Dev | hooks.json 生命周期钩子 |
| `chatgpt_apps` | Experimental | ChatGPT Apps/connectors 支持 |

## 可观测性配置（Telemetry）

```toml
[telemetry]
exporter = "otlp"   # none | otlp（[[OpenTelemetry]]）| console
endpoint = "http://localhost:4317"
service_name = "codex-cli"
env_tag = "dev"
```

自动记录事件：每次 run 的 session_id/model/sandbox/approval 设置、每次 tool call 及耗时、approval 决策记录。

## 不确定性应对机制

| 不确定性场景 | Config System 的应对 |
|------------|---------------------|
| 不同团队成员配置不一致 | 项目级 config.toml 提交 Git |
| 切换环境忘记调整设置 | Profile 系统：一条命令切换完整配置集 |
| 临时测试破坏了配置 | 命令行 -c 只影响单次执行，不修改文件 |
| 密钥被意外传给子进程 | shell_environment_policy 过滤 |
| 不知道当前生效的配置 | `/status` 命令展示生效[[Configuration|配置]]摘要 |
| 新功能行为不可预期 | Feature flags 逐步启用，控制暴露范围 |

## 工程哲学

> **"约定优于[[Configuration|配置]]"和"显式优于隐式"的平衡点**。大多数情况有合理默认值，安全关键决策强制显式声明。分层设计让个人、团队、企业在同一套体系上各取所需。

## 来源

- [[raw/articles/ai-tools/codex/08_codex_config_system.md]] — Codex CLI 深度解析 Vol.8：Config System（分层配置、Telemetry、不确定性应对）
- [[raw/articles/ai-tools/codex/06_codex_mcp_layer.md]] — MCP 配置与 Shell Environment Policy
