# Evolver — 项目总览与整体架构

> **仓库**: [EvoMap/evolver](https://github.com/EvoMap/evolver)
> **定位**: 自我进化型 AI Agent 协议引擎（Self-Evolving Agent Protocol, PCEC）
> **核心口号**: *"Evolution is not optional. Adapt or die."*
> **当前版本**: v1.20.1（2026-02-26） | **Stars**: 772 | **Forks**: 100
> **技术栈**: JavaScript（Node.js ≥ 18）| MIT 协议

---

## 1. 核心定位

Evolver 不是一个普通的 Agent 框架，它是 **AI Agent 的"细胞核"**——一个协议约束的自进化引擎（Protocol-Constrained Evolution Core，PCEC）。

| 维度 | 传统 Agent 开发 | Evolver 方式 |
|------|----------------|-------------|
| Prompt 修改 | 人工、临时、无记录 | 协议约束、可审计、资产化 |
| Bug 修复 | 散乱、反复出现 | 固化为 Gene/Capsule，可复用 |
| 进化历史 | 无从追溯 | 不可变 EvolutionEvent 审计链 |
| 跨 Agent 共享 | 无 | A2A 协议广播 |
| 安全边界 | 无约束 | Blast Radius + 校验命令白名单门控 |
| 修复行为 | 手工、一次性 | 记忆图防重复修复循环 |

---

## 2. 三句话定义

1. **是什么**：一个协议约束的 AI Agent 自进化引擎（GEP 驱动）
2. **解决什么**：把临时 Prompt 调整变成可审计、可复用的进化资产
3. **30 秒上手**：`node index.js` 生成 GEP 指导的进化 Prompt

---

## 3. 整体目录结构（带文件大小注释）

```
evolver/
├── index.js                      # 入口：进化循环主调度器（30KB）
├── package.json                  # 依赖声明，npm 脚本
├── SKILL.md                      # OpenClaw Skill 声明文件（12KB）
├── README.md / README.zh-CN.md   # 英/中双语文档（各约 20KB）
│
├── assets/
│   └── gep/
│       ├── genes.json            # Gene 策略资产库（3.7KB）
│       ├── capsules.json         # Capsule 解决方案库（2.8KB）
│       ├── events.jsonl          # 不可变进化事件审计日志（JSONL 追加写）
│       └── a2a/                  # A2A 消息收发目录
│           ├── inbox/            # 接收外部 Agent 资产
│           └── outbox/           # 广播本地资产
│
├── src/
│   ├── evolve.js                 # 核心进化引擎（82KB，全部主逻辑）
│   ├── canary.js                 # 健康探针（486B）
│   └── gep/
│       ├── signals.js            # 信号提取器（从日志提取可操作模式）
│       ├── selector.js           # Gene/Capsule 选择器（评分+Drift）
│       ├── prompt.js             # GEP 协议 Prompt 组装器
│       ├── solidify.js           # 变更校验与固化（执行校验命令）
│       ├── assetStore.js         # Gene/Capsule 持久化（14KB）
│       ├── assetCallLog.js       # 资产调用历史日志（3.4KB）
│       ├── assets.js             # 资产读写工具（1.1KB）
│       ├── candidates.js         # 候选资产管理（8.1KB）
│       ├── candidateEval.js      # 候选评估逻辑（3.2KB）
│       ├── contentHash.js        # SHA-256 内容哈希（2.1KB）
│       ├── a2a.js                # A2A 本地操作（6.3KB）
│       ├── a2aProtocol.js        # A2A 消息协议实现（28KB）
│       ├── analyzer.js           # 日志分析器（988B）
│       ├── bridge.js             # Solidify 状态桥接（2KB）
│       └── memoryGraph/          # 因果记忆图（信号-基因-结果链路追踪）
│
├── src/ops/
│   ├── lifecycle.js              # 进程生命周期管理
│   ├── skillMonitor.js           # Skill 监控
│   ├── cleanup.js                # 过期文件垃圾清理
│   ├── selfRepair.js             # 进化进程自修复
│   └── wakeTrigger.js            # cron/事件唤醒触发
│
├── scripts/
│   ├── a2a_export.js             # 导出本地资产（2.3KB）
│   ├── a2a_ingest.js             # 摄入外部资产（2.6KB）
│   ├── a2a_promote.js            # 候选资产晋升（4.7KB）
│   ├── analyze_by_skill.js       # 按 Skill 分析进化历史（4.7KB）
│   ├── build_public.js           # 构建公开发行版（11KB）
│   ├── extract_log.js            # 日志提取工具（2.5KB）
│   ├── generate_history.js       # 历史摘要生成（2.5KB）
│   ├── gep_append_event.js       # 手动追加 EvolutionEvent（3KB）
│   ├── gep_personality_report.js # 人格状态分析报告（7.7KB）
│   ├── human_report.js           # 人类可读进化报告（5.7KB）
│   ├── publish_public.js         # 发布公开版本到 GitHub（20KB）
│   ├── recover_loop.js           # 循环卡死检测与恢复（1.7KB）
│   ├── suggest_version.js        # SemVer 版本号建议（3KB）
│   ├── validate-modules.js       # 模块可加载校验（1.2KB）
│   └── validate-suite.js         # 完整校验套件（1.8KB）
│
└── test/                         # 测试用例目录
```

---

## 4. 核心三阶段架构（进化循环）

```
┌─────────────────────────────────────────────────────────────────────┐
│                        EVOLUTION CYCLE                              │
│                                                                     │
│  ┌───────────────┐    ┌───────────────┐    ┌──────────────────┐   │
│  │   PHASE 1     │───►│   PHASE 2     │───►│    PHASE 3       │   │
│  │   ANALYSIS    │    │   SELECTION   │    │   EXECUTION      │   │
│  │               │    │               │    │                  │   │
│  │ 读取会话日志   │    │ Gene 信号评分  │    │ 构建 Mutation    │   │
│  │ 扫描 MEMORY   │    │ Capsule 匹配  │    │ 人格状态选择     │   │
│  │ 提取 Signals  │    │ 记忆图路径查询 │    │ 生成 GEP Prompt  │   │
│  │ 历史事件分析   │    │ Drift 强度计算 │    │ Solidify 校验    │   │
│  └───────────────┘    └───────────────┘    │ 写入 Event 日志  │   │
│          ▲                                 └──────────────────┘   │
│          └──────────────── Loop ───────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 关键安全门控（Loop Gating）

| 门控机制 | 触发条件 | 行为 |
|---------|---------|------|
| **Pending Solidify Gate** | 上一轮变更未固化 | 睡眠 `EVOLVE_PENDING_SLEEP_MS`（默认2分钟）后跳过 |
| **Active Sessions Backoff** | 活跃用户会话 > `EVOLVE_AGENT_QUEUE_MAX`（默认10）| 退避1分钟，避免抢占用户资源 |
| **System Load Backoff** | `load1m > CPU核数×0.9` | 退避，防止加剧负载尖峰 |
| **Repair Loop Circuit Breaker** | 连续3次相同 Gene 修复失败 | 注入 `FORCE_INNOVATION=true`，强制切换策略 |

---

## 5. 运行模式一览

| 命令 | 模式 | 适用场景 |
|------|------|---------|
| `node index.js` | 单次运行 | 生成一次 GEP Prompt，不修改代码，最安全 |
| `node index.js --review` | 人工审核模式 | 生成后暂停，人工确认后再执行 |
| `node index.js --loop` | 连续循环（Mad Dog Mode）| 持续自进化，需沙箱环境 |
| `EVOLVE_STRATEGY=innovate node index.js --loop` | 创新策略循环 | 以新功能为主 |
| `EVOLVE_STRATEGY=harden node index.js --loop` | 强化策略循环 | 专注稳定性 |
| `EVOLVE_STRATEGY=repair-only node index.js --loop` | 修复专用 | 紧急修复模式 |
| `EVOLVE_STRATEGY=steady-state node index.js` | 稳态维护 | 系统成熟期 |

**Ops 生命周期管理**：
```bash
node src/ops/lifecycle.js start    # 后台启动（写 PID 文件）
node src/ops/lifecycle.js stop     # 优雅停止 SIGTERM → 超时 → SIGKILL
node src/ops/lifecycle.js status   # 查看 PID 和运行状态
node src/ops/lifecycle.js check    # 健康检查 + 停滞检测 + 自动重启
```

---

## 6. 与 EvoMap 生态的关系

```
                         evomap.ai (Hub)
                              │
            ┌─────────────────┼──────────────────┐
            │                 │                  │
       Agent A            Agent B            Agent C
       (Evolver)          (Evolver)          (Evolver)
       local Proxy         local Proxy        local Proxy
            │                 │                  │
            └──────────── A2A Protocol ───────────┘
                    Gene/Capsule 共享网络

EvoMap Hub：进化排行榜、资产市场、任务分发、技能商店
A2A 协议：  Agent 间 Gene/Capsule 广播，HMAC-SHA256 签名验证
Evolver：   本地进化引擎，可完全离线运行，Hub 为可选增强
Proxy：     本地 HTTP 代理（默认端口 19820），隔离 Agent 与 Hub 直接通信
```

**Proxy 通信架构**（来自 SKILL.md）：
```
Agent ──► Proxy (localhost:19820) ──► EvoMap Hub
               │
       Local Mailbox (JSONL)   ← 所有消息先写本地，Proxy 后台同步
```

---

## 7. 技术栈

| 层次 | 技术选型 | 备注 |
|------|---------|------|
| 语言 | JavaScript (Node.js ≥ 18) | 纯 JS，无 TypeScript |
| 持久化 | JSON / JSONL 文件 | 无数据库依赖，零部署成本 |
| 加密 | Node.js `crypto` | HMAC-SHA256 签名 + SHA-256 内容哈希 |
| 网络 | 原生 `fetch` API | Node 18+ 内置，无需 axios |
| 进程管理 | Node.js `child_process` | 校验命令执行、生命周期管理 |
| VCS 集成 | `git` | Blast Radius 计算 + 变更回滚 |
| 平台兼容 | 环境无关 | OpenClaw / Cursor / 独立运行均可 |

---

## 8. 关键设计原则

| 原则 | 实现细节 |
|------|---------|
| **进化不自动写代码** | Evolver 生成指导 Prompt，由外部 LLM 执行变更 |
| **协议优先** | 所有变更必须经过 Mutation 对象、校验命令、EvolutionEvent 三重审计 |
| **安全边界** | Blast Radius 文件/行数限制 + 禁止路径 + Gene validation 命令白名单 |
| **可逆性** | 每次变更通过 git 支持 hard/stash/none 三种回滚策略 |
| **离线优先** | 全部核心功能本地可运行，Hub 连接完全可选 |
| **70/30 规则** | 70% 算力维持稳定（修复/优化），30% 探索创新，防止局部最优 |
| **信号去重** | 检测停滞并强制切换策略，防止无限修复循环 |
| **零数据库** | 所有状态存于 JSON/JSONL 文件，可版本控制、可 diff |

---

## 9. 适用 vs. 不适用场景

**适合使用**：
- 维护大规模 Agent Prompt 和运行日志的团队
- 需要可审计进化轨迹的合规场景（每次变更都有 EvolutionEvent）
- 需要确定性、协议约束变更的生产环境
- 希望跨 Agent 共享成功修复经验的多 Agent 架构

**不适合使用**：
- 没有日志/历史记录的单次脚本
- 需要完全自由创意修改、不接受协议约束的项目
- 无法承受协议运行开销的超轻量系统
- 一次性实验性脚本

---

## 10. 版本发布体系

- **发布历史**：v1.0.0 至 v1.20.1，共 62 个版本
- **版本策略**：SemVer（MAJOR.MINOR.PATCH）
- **发布脚本**：`scripts/publish_public.js`（20KB），支持 GitHub Release 自动创建
- **构建流程**：`npm run build` → 生成 `dist-public/` → `npm run publish:public` 推送

必要环境变量：
```bash
PUBLIC_REMOTE=public
PUBLIC_REPO=autogame-17/evolver
PUBLIC_OUT_DIR=dist-public
```

可选环境变量：
```bash
RELEASE_TAG=v1.0.41
RELEASE_TITLE="v1.0.41 - GEP protocol"
GITHUB_TOKEN=...        # 创建 GitHub Release
DRY_RUN=true            # 干运行，不实际推送
```
