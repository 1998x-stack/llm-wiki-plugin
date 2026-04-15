# Codex CLI 深度解析 Vol.8：Config System — 分层配置的工程设计

> **组件定位**：Config System 是 Codex CLI 的"神经系统"，控制每一个可调行为。它不是一个简单的配置文件，而是一个**多层继承、可版本化、环境感知**的配置管理体系。

---

## 1. 核心设计原则

Codex 配置系统遵循以下原则：

```
1. 分层覆盖（Layer Override）
   系统级 < 用户级 < 团队级 < 项目级 < Profile < 命令行

2. Git 友好（Versionable）
   项目级配置在 .codex/ 下，可提交到 Git

3. 环境感知（Profile Switching）
   dev / staging / prod 使用不同 Profile

4. 显式优于隐式（Explicit over Implicit）
   重要设置（sandbox、approval）必须显式声明
```

---

## 2. 配置层次结构

```
优先级（低 → 高）：

Layer 1: 系统级（只读）
  /etc/codex/config.toml
  → 企业 IT 管理员设置，用户不可覆盖

Layer 2: 用户级（主要配置文件）
  ~/.codex/config.toml
  → 个人偏好：默认模型、沙箱级别、MCP 服务器

Layer 3: 团队级（项目根目录）
  {project}/.codex/config.toml
  → 团队共享配置，提交到 Git
  → 包含：ExecPolicy 规则、AGENTS.md、MCP 服务器

Layer 4: 子目录覆盖
  {project}/src/auth/.codex/config.toml
  → 特定目录的专属配置（如更严格的沙箱）

Layer 5: Profile（命名配置集）
  ~/.codex/config.toml [profiles.strict]
  → 按场景切换：codex -p strict

Layer 6: 命令行 flags（最高优先级）
  codex --model gpt-5.4 -c sandbox_mode='"danger-full-access"'
  → 单次执行覆盖，不影响配置文件
```

---

## 3. 核心配置项详解

### 3.1 模型与 Provider

```toml
# 基本模型配置
model = "gpt-5.4"
model_provider = "openai"    # openai | oss（本地 Ollama）

# 本地模型（OSS）
model_provider = "oss"
# 需要 Ollama 已运行：ollama serve
# codex --oss 等价于 -c model_provider="oss"

# Review 时使用不同模型（独立 Agent，可用更便宜的模型）
[review]
model = "gpt-5.4-mini"
```

### 3.2 沙箱与审批（核心安全配置）

```toml
# 沙箱模式
sandbox_mode = "workspace-write"  # read-only | workspace-write | danger-full-access

# 工作区写模式的细节配置
[sandbox_workspace_write]
network_access = false        # 是否允许网络（默认禁止）
exclude_tmp = false           # 是否从可写根排除 /tmp
exclude_tmpdir = false        # 是否从可写根排除 $TMPDIR
extra_writable_roots = [      # 额外允许写的目录
  "/tmp/build_cache"
]

# 审批策略
approval_policy = "on-request"
# 精细配置：
approval_policy = { granular = {
  sandbox_approval = true,       # 需要逃出沙箱时询问
  rules = true,                  # execpolicy prompt 规则触发时询问
  mcp_elicitations = true,       # MCP 请求额外权限时询问
  request_permissions = false,   # 自动拒绝 request_permissions
  skill_approval = true,         # Skill 脚本执行时询问
} }
```

### 3.3 Profile 系统

```toml
# 全局默认
model = "gpt-5.4"
sandbox_mode = "workspace-write"
approval_policy = "on-request"

# 严格模式（安全审查）
[profiles.strict]
sandbox_mode = "read-only"
approval_policy = "untrusted"
model = "gpt-5.4"

# 自动化模式（CI 使用）
[profiles.auto]
sandbox_mode = "danger-full-access"
approval_policy = "never"
model = "gpt-5.4-mini"   # 快速便宜

# 探索模式（学习新代码库）
[profiles.explore]
sandbox_mode = "read-only"
approval_policy = "never"  # 只读，直接放行
```

```bash
# 切换 profile
codex -p strict "审查这段代码是否有安全漏洞"
codex -p auto "批量生成所有模块的测试"
codex -p explore "解释这个 codebase 的架构"
```

### 3.4 Shell 环境策略

```toml
[shell_environment_policy]
inherit = "core"              # none | core（只继承 PATH/HOME 等基础）| all（全部）
exclude = ["AWS_*", "AZURE_*", "*SECRET*", "*PASSWORD*"]
include_only = ["PATH", "HOME", "GOPATH", "GITHUB_TOKEN"]

# 注入固定值
set = { NODE_ENV = "test", CI = "true" }
```

### 3.5 AGENTS.md — 项目级 Agent 指令

```toml
# 控制 AGENTS.md 的搜索行为
[project]
agents_md_max_bytes = 65536       # 最大读取字节数
agents_md_fallback_names = [      # AGENTS.md 不存在时的备选文件名
  "CLAUDE.md", "COPILOT_INSTRUCTIONS.md"
]
project_root_markers = [          # 项目根目录标识文件
  ".git", "package.json", "Cargo.toml", "go.mod"
]
trust = "trusted"                 # trusted | untrusted（不信任的项目跳过项目级 .codex/）
```

**AGENTS.md 的内容示例：**
```markdown
# Project: MyApp

## 技术栈
- Go 1.22, Gin framework
- PostgreSQL + sqlx
- 部署到 Kubernetes

## 代码规范
- 所有公开函数必须有 godoc 注释
- 错误处理：使用 errors.Wrap，不使用 fmt.Errorf
- 测试：表驱动测试，覆盖率 > 80%

## 禁止操作
- 不要修改 internal/legacy/ 下的代码（维护期）
- 不要删除 migration 文件
- 不要修改 .env.example 的格式
```

---

## 4. 配置的动态覆盖

### 4.1 命令行 -c 标志

```bash
# -c 使用 TOML 语法解析
codex -c model='"gpt-5.4-mini"' "快速问题"
codex -c sandbox_workspace_write.network_access=true "需要网络的任务"
codex -c 'shell_environment_policy.include_only=["PATH","HOME"]' "隔离执行"

# 点号访问嵌套键
codex -c mcp_servers.context7.enabled=false "不用 context7"
```

### 4.2 环境变量

```bash
# 覆盖配置文件路径
export CODEX_CONFIG_PATH="$HOME/.codex/prod_config.toml"

# 常用 env 覆盖（部分配置支持）
export OPENAI_API_KEY="sk-..."
export CODEX_MODEL="gpt-5.4"
```

---

## 5. Feature Flags

Codex 用 feature flag 管理实验性功能：

```bash
# 查看所有 feature flags
codex features list

# 启用/禁用（持久化到 config.toml）
codex features enable unified_exec
codex features disable shell_snapshot

# Profile 级 feature flag
codex -p myprofile features enable some_feature
# → 写入该 profile 而非全局 config
```

**当前 Feature Flags（示例）：**

| Flag | 状态 | 功能 |
|------|------|------|
| `unified_exec` | Stable | 统一执行引擎 |
| `shell_snapshot` | Beta | 执行前 shell 状态快照 |
| `multi_agents` | Stable | subagent 工具集 |
| `lifecycle_hooks` | Dev | hooks.json 生命周期钩子 |
| `chatgpt_apps` | Experimental | ChatGPT Apps/connectors 支持 |

---

## 6. 可观测性配置（Telemetry）

```toml
[telemetry]
exporter = "otlp"   # none | otlp（OpenTelemetry）| console
endpoint = "http://localhost:4317"
service_name = "codex-cli"
env_tag = "dev"

# 自动记录的事件：
# - 每次 run 的 session_id、model、sandbox/approval 设置
# - 每次 tool call 及其耗时
# - approval 决策记录
```

---

## 7. 配置系统减少不确定性的机制

| 不确定性场景 | Config System 的应对 |
|------------|---------------------|
| 不同团队成员配置不一致 | 项目级 config.toml 提交 Git |
| 切换环境忘记调整设置 | Profile 系统：一条命令切换完整配置集 |
| 临时测试破坏了配置 | 命令行 -c 只影响单次执行，不修改文件 |
| 密钥被意外传给子进程 | shell_environment_policy 过滤 |
| 不知道当前生效的配置 | `/status` 命令展示生效配置摘要 |
| 新功能行为不可预期 | Feature flags 逐步启用，控制暴露范围 |

---

## 8. 工程哲学摘要

> **好的配置系统是"约定优于配置"和"显式优于隐式"的平衡点。**
>
> Codex 的 Config System 在大多数情况下有合理的默认值（不需要配置），
> 但在安全关键决策（sandbox_mode、approval_policy）上强制显式声明。
>
> 分层设计让个人、团队、企业在同一套配置体系上各取所需：
> - 个人：`~/.codex/config.toml` 设置偏好
> - 团队：`.codex/config.toml` 提交 Git 统一规范
> - 企业：`/etc/codex/config.toml` 强制合规策略

---

*下一篇：Vol.9 — 工程哲学总论：从不确定性到确定性的系统设计*
