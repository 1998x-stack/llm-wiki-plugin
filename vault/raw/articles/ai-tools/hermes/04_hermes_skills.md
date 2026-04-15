# Hermes Agent 深度解析 · 第四篇：Skills 系统 —— 程序性记忆与开放标准

> **系列导读**：如果说 MEMORY.md 是 Agent 的"陈述性记忆"（记住事实），那么 Skills 就是它的"程序性记忆"（记住怎么做）。本篇深入 Skills 的设计哲学、SKILL.md 格式规范、渐进式加载机制、条件激活系统，以及 agentskills.io 开放标准。

---

## 一、Skills 是什么？

Skills 是存储在文件系统中的**结构化知识文档**，Agent 可以按需加载。

想象你雇了一个新员工：
- **没有 Skills**：每次遇到 Git 分支冲突都要从头摸索
- **有 Skills**：第一次解决后，把流程写下来。下次直接翻笔记，又快又准

Hermes 就是那个会自己"写笔记"的员工。区别是这些笔记（Skills）是结构化的、可被机器读取的、Token 高效的。

### Skills vs MEMORY.md

| 维度 | MEMORY.md | Skills |
|---|---|---|
| 记忆类型 | 陈述性（Declarative） | 程序性（Procedural） |
| 存储内容 | 事实、偏好、环境信息 | 工作流、步骤、方法 |
| Token 成本 | 始终在 System Prompt（固定消耗） | 渐进式加载（按需消耗） |
| 生成方式 | Agent 在对话中自动积累 | Agent 从成功经验中主动创建 |
| 大小 | 严格限制（2,200 chars） | 无上限（可含参考文件） |
| 格式 | 自由文本，`§` 分隔 | 标准化 SKILL.md + 可选参考文件 |

---

## 二、渐进式加载（Progressive Disclosure）

这是 Skills 系统最重要的工程设计，解决了"技能库越大、Token 消耗越多"的矛盾。

### 三级加载模型

```
Level 0: skills_list()
  → 返回所有技能的 {name, description, category}
  → 约 3,000 tokens（无论有多少技能，固定消耗）

Level 1: skill_view(name)
  → 加载特定技能的完整 SKILL.md
  → 按需消耗（只在用到时）

Level 2: skill_view(name, path)
  → 加载技能目录中的特定参考文件
  → 按需消耗（只在用到时）
```

### 为什么固定 3,000 tokens？

Level 0 只包含名称和一行描述，不包含详细内容。无论你有 10 个还是 100 个技能，Level 0 目录的大小基本固定——因为每个技能只贡献约 30 tokens（名称 + 简短描述）的目录条目。

这意味着：**你可以积累上百个技能，而不用担心 Token 成本爆炸。**

### 实际工作流

```
用户请求："帮我给这个 API 项目配置 CI/CD"
       ↓
Agent 查看 Level 0 技能目录（始终可见）
       ↓
发现："github-actions-ci" 技能 —— 看起来相关
       ↓
调用 skill_view("github-actions-ci")  ← Level 1 加载
       ↓
获得完整的工作流、步骤、注意事项
       ↓
按照技能文档执行任务
```

---

## 三、SKILL.md 格式规范详解

### 完整格式

```markdown
---
name: deploy-to-k8s
description: 将 Docker 容器部署到 Kubernetes 集群，包含滚动更新和回滚流程
version: 1.2.0
platforms: [linux, macos]     # 可选：限制运行平台
metadata:
  hermes:
    tags: [kubernetes, docker, devops, deployment]
    category: devops
    fallback_for_toolsets: [web]    # 条件激活（见下文）
    requires_toolsets: [terminal]   # 条件激活
    config:                         # 可选配置项（存入 config.yaml）
      - key: k8s.namespace
        description: "目标 Kubernetes 命名空间"
        default: "production"
        prompt: "请输入 K8s 命名空间"
      - key: k8s.registry
        description: "容器镜像仓库地址"
        default: ""
        prompt: "容器镜像仓库（如 registry.example.com）"
required_environment_variables:
  - name: KUBECONFIG
    prompt: Kubernetes 配置文件路径
    help: "通常位于 ~/.kube/config，或通过 KUBECONFIG 环境变量指定"
    required_for: 所有 kubectl 操作
---

# Kubernetes 部署流程

## When to Use（何时使用）
- 将新版本的 Docker 镜像部署到 K8s 集群
- 执行滚动更新（Rolling Update）
- 紧急回滚到上一个版本

## Prerequisites（前提条件）
- kubectl 已安装并配置
- 目标集群可达（`kubectl cluster-info` 验证）
- 镜像已推送到仓库

## Procedure（步骤）

### 1. 验证部署前状态
```bash
kubectl get deployments -n {k8s.namespace}
kubectl get pods -n {k8s.namespace}
```

### 2. 执行部署
```bash
kubectl set image deployment/{APP_NAME} \
  {APP_NAME}={REGISTRY}/{APP_NAME}:{VERSION} \
  -n {k8s.namespace}
```

### 3. 监控滚动更新
```bash
kubectl rollout status deployment/{APP_NAME} -n {k8s.namespace}
```

### 4. 验证部署成功
```bash
kubectl get pods -n {k8s.namespace} | grep {APP_NAME}
```

## Rollback（回滚）
```bash
# 回滚到上一个版本
kubectl rollout undo deployment/{APP_NAME} -n {k8s.namespace}

# 回滚到特定版本
kubectl rollout undo deployment/{APP_NAME} --to-revision={N} -n {k8s.namespace}
```

## Pitfalls（常见问题）
- 镜像 Tag 使用 `latest` 会导致 K8s 不触发更新 —— 始终使用具体版本号
- 如果 Pod 无法拉取镜像，检查 ImagePullSecrets 是否正确配置
- `CrashLoopBackOff` 通常意味着应用启动错误，用 `kubectl logs {POD_NAME}` 排查

## Verification（验证）
部署成功的标志：
- `kubectl rollout status` 输出 `deployment "xxx" successfully rolled out`
- 所有 Pod 状态为 `Running`（`kubectl get pods`）
- 应用可通过 Service 正常访问
```

### 关键字段详解

**`name`**：技能的唯一标识符，也是斜杠命令的名称（`/deploy-to-k8s`）

**`description`**：Level 0 目录中展示的内容，**是 Agent 决定是否加载此技能的唯一依据**。写好 description 极其重要——它本质上是给 Agent 的"技能触发条件"。

**`version`**：支持语义化版本，Agent 自我改进时会递增

**`platforms`**：不匹配时，技能从目录、FTS5 索引、斜杠命令中完全隐藏

**`category`**：用于 Level 0 目录的分类展示

**`config`**：声明非密钥配置项，存入 `config.yaml`，技能加载时自动注入

---

## 四、条件激活机制（Conditional Activation）

这是 Skills 系统中最精巧的设计之一，让技能能够**根据当前工具可用性自动显示或隐藏**。

### 四种条件字段

| 字段 | 行为 |
|---|---|
| `fallback_for_toolsets: [web]` | 当 web toolset **不可用**时才显示（回退方案） |
| `fallback_for_tools: [web_search]` | 当特定工具不可用时才显示 |
| `requires_toolsets: [terminal]` | 只在 terminal toolset **可用**时显示 |
| `requires_tools: [execute_code]` | 只在特定工具可用时显示 |

### 经典案例：DuckDuckGo 回退技能

```yaml
# 内置的 duckduckgo-search 技能
metadata:
  hermes:
    fallback_for_toolsets: [web]
```

行为：
- 有 `FIRECRAWL_API_KEY` → web toolset 可用 → DuckDuckGo 技能**隐藏**（用更好的工具）
- 没有 API Key → web toolset 不可用 → DuckDuckGo 技能**自动出现**

用户不需要手动管理，条件激活自动处理。

### 另一个案例：需要终端的技能

```yaml
# 只有在有终端执行能力时才有意义的技能
metadata:
  hermes:
    requires_toolsets: [terminal]
```

在纯对话模式（没有 terminal toolset）下，这个技能自动隐藏——没有能力执行时，显示它只会造成混乱。

---

## 五、Skills 目录结构

```
~/.hermes/skills/                    # 唯一真实来源
├── devops/                          # 按 category 分目录
│   ├── kubernetes/
│   │   ├── SKILL.md                 # 主技能文档（必需）
│   │   ├── examples/                # 示例文件（可选）
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   └── reference/               # 参考文件（可选，Level 2 加载）
│   │       └── kubectl-cheatsheet.md
│   └── docker/
│       └── SKILL.md
├── mlops/
│   └── axolotl/
│       ├── SKILL.md
│       └── configs/                 # Level 2 参考文件
│           ├── llama3-qlora.yaml
│           └── training-tips.md
└── personal/                        # Agent 自动创建的技能
    ├── my-api-workflow/
    │   └── SKILL.md
    └── data-pipeline-pattern/
        └── SKILL.md
```

**Agent 创建的技能**默认存入 `personal/` 子目录，与社区技能和系统技能分开管理。

---

## 六、如何使用技能

### 方法 1：斜杠命令（最直接）

每个已安装的技能自动成为斜杠命令：

```bash
# 直接触发技能
/kubernetes-deploy APP_NAME=myapp VERSION=1.2.3

# 只加载技能，让 Agent 询问需要什么
/axolotl

# 技能名加具体任务描述
/github-pr-workflow create a PR for the auth refactor branch
```

### 方法 2：自然对话（Agent 自动判断）

```bash
hermes chat --toolsets skills -q "帮我用 axolotl 微调 Llama 3"
# Agent 看到 Level 0 目录，发现 axolotl 技能相关，自动加载
```

### 方法 3：指定工具集

```bash
# 仅用 skills 工具集，节省 Token（适合快速查询）
hermes chat --toolsets skills -q "你有哪些 devops 相关的技能？"
```

---

## 七、Skills 管理命令

### CLI 管理

```bash
hermes skills list              # 列出所有已安装技能
hermes skills show axolotl      # 查看特定技能详情
hermes skills install mlops/axolotl   # 从官方可选技能安装
hermes skills enable axolotl    # 在当前平台启用
hermes skills disable axolotl   # 在当前平台禁用
hermes skills edit axolotl      # 用编辑器打开技能文件
```

### 在对话中管理

```bash
# 列出技能
/skills list

# 查看技能
/skills show kubernetes-deploy

# Agent 自主创建技能（对话触发）
"把这次 k8s 部署的流程记录成一个技能"
```

---

## 八、Agent 自主创建技能

这是 Hermes 闭环学习的核心——Agent 不只是使用技能，它**创建技能**。

### 触发场景

```
场景：Agent 刚完成了一个复杂的多步数据迁移任务
       ↓
Agent 判断：这类任务可能再次出现
       ↓
Agent 主动决策：把这个工作流写成技能
       ↓
创建 ~/.hermes/skills/personal/postgres-migration/SKILL.md
       ↓
下次类似任务：直接用 /postgres-migration，不再从头摸索
```

### 触发条件（Agent 的内部判断）

Agent 在以下情况倾向于创建技能：
1. 成功完成了需要 4 步以上的工作流
2. 明确感知到"这类任务未来会重复"
3. 工作流中有容易出错的关键步骤
4. 用户说"把这个记下来"

### 自动创建技能的格式

Agent 会写出标准 SKILL.md，包含：
- 清晰的 `description`（供 Level 0 目录识别用）
- 完整的前提条件和步骤
- 踩过的坑（Pitfalls）
- 验证方法

---

## 九、agentskills.io 开放标准

Hermes Skills 兼容 [agentskills.io](https://agentskills.io) 开放规范，这意味着：

### 跨框架可移植

```
OpenClaw skill ──→ 迁移 ──→ Hermes skill ✅
Hermes skill   ──→ 导出 ──→ 其他兼容框架 ✅
```

### Skills Hub 社区生态

```bash
# 从 Skills Hub 安装社区技能
hermes skills hub search "fine-tuning"
hermes skills hub install mlops/axolotl
hermes skills hub install devops/terraform-workflow
```

社区用户贡献的技能：
- 都遵循相同的 SKILL.md 格式
- 经过 Skills Hub 审核
- 可以用 `hermes skills update` 更新到最新版

### 从 OpenClaw 迁移

```bash
hermes claw migrate              # 迁移 settings + memories + skills + API keys
hermes claw migrate --dry-run    # 预览，不实际执行
hermes claw migrate --preset user-data  # 只迁移用户数据，跳过密钥
hermes claw migrate --overwrite  # 覆盖已存在的冲突文件
```

---

## 十、Secure Setup on Load（安全按需配置）

技能可以声明所需的环境变量，而不会因为缺少它们就消失：

```yaml
required_environment_variables:
  - name: TENOR_API_KEY
    prompt: Tenor API Key（GIF 搜索）
    help: 从 https://developers.google.com/tenor 获取
    required_for: GIF 搜索功能
```

行为：
- 技能始终在 Level 0 目录中**可见**（不会因为缺少 Key 就隐藏）
- 在 CLI 中首次加载时，自动弹出配置提示
- 在消息平台（Telegram 等）中，提示用户用 `hermes setup` 或 `~/.hermes/.env` 配置
- 配置后，密钥自动传入 `execute_code` 和 `terminal` 沙盒，技能脚本可直接用 `$TENOR_API_KEY`

---

## 十一、技能系统的完整生命周期

```
┌─────────────────────────────────────────────────────────────────┐
│                       Skills 生命周期                            │
│                                                                 │
│  创建 ──→ 首次使用 ──→ 自我改进 ──→ 共享 / 迁移 ──→ 弃用删除    │
│   ↑                      │                                      │
│   └──── Agent 从经验中 ←──┘                                     │
│         自动创建                                                 │
└─────────────────────────────────────────────────────────────────┘

创建阶段：
  - Agent 从经验中自动创建
  - 用户手动编写
  - 从 Skills Hub 安装
  - 从 OpenClaw 迁移

使用阶段：
  - 斜杠命令触发
  - Agent 自动识别并加载
  - 渐进式加载（Level 0 → 1 → 2）

改进阶段：
  - Agent 发现步骤有误时自动更新
  - 版本号递增（1.0.0 → 1.1.0）
  - 用户显式编辑（hermes skills edit）

共享阶段：
  - 提交到 agentskills.io / Skills Hub
  - 通过 Git 分享给团队
  - 跨框架迁移
```

---

## 十二、小结

Skills 系统的设计精髓在于三点：

1. **程序性记忆外化**：把"怎么做"从模型的参数（无法修改）变成文件系统上的文档（可以修改、可以增长）

2. **Token 效率优先**：渐进式加载确保记忆库可以无限增长，而对每次对话的成本影响几乎固定

3. **开放标准避免孤岛**：agentskills.io 兼容性让技能成为可在框架间流通的资产，而非某个系统的私有数据

---

*下一篇：[第五篇：Gateway 消息网关 —— 14+ 平台统一接入架构](./05_hermes_gateway.md)*

*基于 2026 年 4 月版本 · GitHub: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)*
