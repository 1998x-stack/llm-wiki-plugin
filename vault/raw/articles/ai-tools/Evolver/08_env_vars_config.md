# Evolver 完整环境变量速查表与实战配置

> **配置文件**: 项目根目录 `.env` 文件或 shell export
> **文档来源**: `src/evolve.js`, `src/gep/a2aProtocol.js`, SKILL.md, 官方文档

---

## 1. 完整环境变量速查表

### 核心配置

| 变量 | 默认值 | 必填 | 说明 |
|------|--------|------|------|
| `A2A_NODE_ID` | 无 | Hub 必填 | EvoMap 节点身份（格式：`node_xxxxxxxxxxxx`，从 evomap.ai 注册）|
| `EVOLVE_STRATEGY` | `balanced` | - | 进化策略：`balanced/innovate/harden/repair-only/early-stabilize/steady-state/auto` |
| `AGENT_NAME` | `default` | - | Agent 名称，影响会话日志路径 |
| `EVOLVER_SESSION_SCOPE` | 无 | - | 会话隔离范围（按 channel/项目隔离进化状态）|

### 安全与限制

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `EVOLVE_ALLOW_SELF_MODIFY` | `false` | **危险** 允许修改 Evolver 自身源码，生产禁止开启 |
| `EVOLVER_ROLLBACK_MODE` | `hard` | 失败回滚策略：`hard`（git reset）/ `stash`（git stash）/ `none` |
| `EVOLVER_HARD_CAP_FILES` | `60` | 系统级单次进化最大文件数（覆盖 Gene 约束）|
| `EVOLVER_HARD_CAP_LINES` | `20000` | 系统级单次进化最大行数 |
| `A2A_MAX_FILES` | `5` | A2A 外部资产 blast radius 文件上限 |
| `A2A_MAX_LINES` | `200` | A2A 外部资产 blast radius 行数上限 |

### 性能与节流

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `EVOLVE_LOAD_MAX` | 自动（CPU×0.9）| 1分钟负载均值超过此值时退避（防止加剧负载）|
| `EVOLVE_AGENT_QUEUE_MAX` | `10` | 活跃用户会话数超过此值时退避（避免抢占用户资源）|
| `EVOLVE_AGENT_QUEUE_BACKOFF_MS` | `60000` | 队列满时退避等待时间（毫秒）|
| `EVOLVE_PENDING_SLEEP_MS` | `120000` | 等待上一轮 solidify 完成的睡眠时间（毫秒）|
| `EVOLVE_MIN_INTERVAL` | `120000` | 两次进化循环之间的最小间隔（毫秒）|

### 循环与模式控制

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `EVOLVE_LOOP` | `false` | 启用连续循环模式（等价于 `--loop` 参数）|
| `EVOLVE_BRIDGE` | `true` | 启用 sessions_spawn bridge 输出 |
| `RANDOM_DRIFT` | `false` | 启用随机漂变（逃离局部最优，等价于 `--drift`）|
| `FORCE_INNOVATION` | `false` | 强制创新意图（断路器自动设置，也可手动）|

### 调试与诊断

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `EVOLVE_EMIT_THOUGHT_PROCESS` | `false` | 在 Prompt 中输出推理过程（调试用）|
| `EVOLVE_PRINT_PROMPT` | `false` | 将生成的 GEP Prompt 打印到 stdout |

### A2A 网络

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `A2A_NODE_SECRET` | 自动（首次 hello 获取）| 64字符 hex HMAC 签名密钥 |
| `A2A_HUB_URL` | `https://evomap.ai` | EvoMap Hub API 地址 |
| `A2A_TRANSPORT` | `file` | 传输方式：`file`（本地离线）/ `http`（Hub 模式）|
| `A2A_DIR` | `assets/gep/a2a` | 文件传输目录 |
| `HEARTBEAT_INTERVAL_MS` | `360000` | Hub 心跳间隔（6 分钟）|
| `PROXY_ENABLED` | `1`（推荐）| 启用本地 Proxy |
| `PROXY_PORT` | `19820` | 本地 Proxy 端口 |

### Worker Pool（EvoMap 网络参与）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `WORKER_ENABLED` | 未设置 | 设为 `1` 启用 Worker 模式，参与任务队列 |
| `WORKER_DOMAINS` | 空 | 接受的任务域（逗号分隔，如 `repair,harden`）|
| `WORKER_MAX_LOAD` | `5` | 告知 Hub 的最大并发量（提示性，非本地强制）|

### Hub 搜索与资产复用

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `EVOLVER_REUSE_MODE` | `auto` | Hub 搜索优先模式：`auto`/`always`/`never` |
| `EVOLVER_MIN_REUSE_SCORE` | `0.72` | Hub 资产最低复用分（低于此分只作参考）|
| `EVOLVER_AUTO_PUBLISH` | `true` | 自动发布满足条件的进化结果到 Hub |
| `EVOLVER_DEFAULT_VISIBILITY` | `public` | 默认发布可见性：`public`/`private` |
| `EVOLVER_MIN_PUBLISH_SCORE` | `0.78` | 自动发布的最低 outcome.score |

### 报告与集成

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `EVOLVE_REPORT_TOOL` | `message` | 进化报告使用的工具（可替换为 `feishu-card`）|
| `EVOLVE_REPORT_DIRECTIVE` | 无 | 自定义报告指令模板（`__CYCLE_ID__` 占位符）|
| `INTEGRATION_STATUS_CMD` | 无 | 系统集成健康检查命令（如 ES 集群状态检查）|

### 自动 GitHub Issue 上报

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `EVOLVER_AUTO_ISSUE` | `true` | 启用持续失败自动上报 Issue |
| `EVOLVER_ISSUE_REPO` | `autogame-17/capability-evolver` | 上报目标 GitHub 仓库 |
| `EVOLVER_ISSUE_COOLDOWN_MS` | `86400000` | 同一错误的上报冷却时间（24小时）|
| `EVOLVER_ISSUE_MIN_STREAK` | `5` | 触发上报的最小连续失败次数 |
| `GITHUB_TOKEN` | 无 | GitHub PAT（repo 权限），Issue 上报需要 |

### 内存与状态路径

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MEMORY_DIR` | `<workspace>/memory` | 记忆目录 |
| `MEMORY_GRAPH_PATH` | `<evolution_dir>/memory_graph.jsonl` | 记忆图文件路径 |
| `MEMORY_GRAPH_PROVIDER` | `local` | 存储提供者：`local`/`remote` |
| `MEMORY_GRAPH_REMOTE_URL` | 无 | 远程记忆图服务 URL |
| `MEMORY_GRAPH_REMOTE_KEY` | 无 | 远程记忆图 API 密钥 |
| `EVOLVER_REPO_ROOT` | git 自动检测 | 仓库根目录（override）|
| `OPENCLAW_WORKSPACE` | 自动推算 | Workspace 根目录 |
| `EVOLUTION_DIR` | `<memory_dir>/evolution` | 进化状态目录 |
| `GEP_ASSETS_DIR` | `<repo_root>/assets/gep` | GEP 资产目录 |
| `SKILLS_DIR` | `<workspace>/skills` | Skills 目录 |

### 技能蒸馏器（Skill Distiller）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SKILL_DISTILLER` | `true` | 启用自动技能蒸馏（Capsule → Skill 提炼）|
| `DISTILLER_MIN_CAPSULES` | `10` | 触发蒸馏所需的最少 Capsule 数量 |
| `DISTILLER_INTERVAL_HOURS` | `24` | 蒸馏间隔（小时）|
| `DISTILLER_MIN_SUCCESS_RATE` | `0.7` | 蒸馏所需的最低成功率 |

### 公开发布（publish_public.js）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PUBLIC_REMOTE` | `public` | git remote 名称 |
| `PUBLIC_REPO` | 无 | 目标 GitHub 仓库（如 `autogame-17/evolver`）|
| `PUBLIC_OUT_DIR` | `dist-public` | 构建输出目录 |
| `PUBLIC_USE_BUILD_OUTPUT` | `true` | 使用 build 输出而非源目录 |
| `SOURCE_BRANCH` | `main` | 源分支 |
| `PUBLIC_BRANCH` | `main` | 目标分支 |
| `RELEASE_TAG` | 无 | 版本 Tag（如 `v1.0.41`）|
| `RELEASE_TITLE` | 无 | Release 标题 |
| `RELEASE_NOTES` | 无 | Release Notes 内容（直接写入）|
| `RELEASE_NOTES_FILE` | 无 | Release Notes 来源文件 |
| `RELEASE_SKIP` | `false` | 只推送，不创建 Release |
| `RELEASE_USE_GH` | `false` | 使用 `gh` CLI 替代 GitHub API |
| `PUBLIC_RELEASE_ONLY` | `false` | 只创建 Release，不推送（Tag 已存在）|
| `DRY_RUN` | `false` | 干运行，不实际执行 |

---

## 2. 实战配置方案

### 方案 A：本地离线安全模式（推荐入门）

```bash
# .env
EVOLVE_STRATEGY=harden
EVOLVER_ROLLBACK_MODE=stash
EVOLVER_HARD_CAP_FILES=10
EVOLVER_HARD_CAP_LINES=500
EVOLVE_ALLOW_SELF_MODIFY=false
# 不设置 A2A_NODE_ID，完全离线运行
```

```bash
# 手动单次运行，人工审核
node index.js --review
```

### 方案 B：定时沙箱强化（CI/CD 集成）

```bash
# .env
EVOLVE_STRATEGY=harden
EVOLVER_ROLLBACK_MODE=stash
EVOLVER_HARD_CAP_FILES=15

# cron（每天凌晨 3 点运行一次）
0 3 * * * cd /sandbox/evolver && EVOLVE_STRATEGY=harden node index.js 2>&1 | tee /tmp/evolver-$(date +%Y%m%d).log
```

### 方案 C：生产 Worker 节点（EvoMap 网络参与）

```bash
# .env
A2A_NODE_ID=node_xxxxxxxxxxxx         # 从 evomap.ai 注册获取
PROXY_ENABLED=1
PROXY_PORT=19820
WORKER_ENABLED=1
WORKER_DOMAINS=repair,harden
WORKER_MAX_LOAD=3
EVOLVE_STRATEGY=auto
EVOLVER_AUTO_PUBLISH=true
EVOLVER_MIN_PUBLISH_SCORE=0.82        # 高于默认，只发布高质量资产
EVOLVER_ROLLBACK_MODE=stash
EVOLVER_HARD_CAP_FILES=15
EVOLVER_AUTO_ISSUE=true
GITHUB_TOKEN=ghp_...
```

```bash
# 后台运行
node src/ops/lifecycle.js start

# 每小时健康检查
0 * * * * node /path/to/src/ops/lifecycle.js check
```

### 方案 D：紧急修复模式

```bash
# 遇到生产 Agent 持续报错时
EVOLVE_STRATEGY=repair-only node index.js --review
# 审核修复方案后再应用
```

### 方案 E：调试/诊断模式

```bash
# 打印完整 Prompt 到 stdout 进行分析
EVOLVE_PRINT_PROMPT=true EVOLVE_EMIT_THOUGHT_PROCESS=true node index.js 2>&1 | tee /tmp/debug.log
```

---

## 3. 常见配置陷阱

| 陷阱 | 症状 | 解决方案 |
|------|------|---------|
| `A2A_NODE_ID` 未设置但 `WORKER_ENABLED=1` | 节点 ID 每次变化，无法认领任务 | 在 evomap.ai 注册后设置固定 ID |
| `EVOLVE_ALLOW_SELF_MODIFY=true` 在生产 | Evolver 修改自身 Prompt 逻辑后级联失败 | 立即设为 `false`，执行 `git reset --hard` |
| `EVOLVER_ROLLBACK_MODE=none` | 失败变更残留，下次进化基于损坏状态 | 改为 `stash`，手动清理 stash |
| `EVOLVER_HARD_CAP_FILES=60`（默认）生产直用 | 单次进化改动 60 个文件，风险极高 | 生产环境设为 `10~15` |
| `--loop` 模式在非沙箱环境 | 读取其他 Agent 日志并尝试修复无关代码 | 严格隔离 `cwd`，使用 `EVOLVER_SESSION_SCOPE` |
| 不设置 `EVOLVE_PENDING_SLEEP_MS` 并快速重启 | Brain 和 Hand Agent 不同步，race condition | 保持默认 120000ms 或适当增大 |
