# Scripts 工具集与 Ops 运维模块完整分析

> **目录**: `scripts/`（15 个工具脚本）+ `src/ops/`（5 个运维模块）
> **定位**: 围绕进化循环核心的辅助工具链，涵盖资产管理、发布、报告、运维

---

## 一、Scripts 工具集（scripts/）

### 1. a2a_export.js — A2A 资产导出（2.3KB）

**功能**：将本地满足广播资格的 Capsule/Gene 导出为 A2A publish 消息，写入 `outbox/publish.jsonl`

**执行条件**：
- `outcome.score >= 0.7`
- `blast_radius.files <= 5 && lines <= 200`
- `success_streak >= 2`

**使用场景**：
```bash
node scripts/a2a_export.js
# 导出高置信度 Capsule 到 outbox，Proxy 后台同步到 Hub
```

---

### 2. a2a_ingest.js — 外部资产摄入（2.6KB）

**功能**：从 stdin 读取外部 A2A 消息，做基础结构校验后暂存为候选。

**输入格式**：JSONL（每行一条 gep-a2a 消息）

**处理流程**：
```
stdin → 解析 JSON → 验证 protocol/message_type 字段
     → 暂存到 assets/gep/external_candidates.jsonl
     → 输出摄入统计（N 条成功 / M 条失败）
```

**使用场景**：
```bash
cat received_a2a_messages.jsonl | node scripts/a2a_ingest.js
```

---

### 3. a2a_promote.js — 候选资产晋升（4.7KB）

**功能**：将 `external_candidates.jsonl` 中的候选资产晋升为本地 Gene/Capsule 库。

**安全机制**（三道门）：
1. 必须指定 `--validated` 标志（人工审查确认）
2. Gene 的 `validation` 命令逐条经 `isValidationCommandAllowed()` 审查
3. 同 ID 的本地 Gene 不会被覆盖（防止污染）

**使用场景**：
```bash
# 查看待晋升的候选
node scripts/a2a_promote.js --list

# 审查后晋升（必须 --validated）
node scripts/a2a_promote.js --validated --id capsule_1770477654236

# 晋升所有已校验候选
node scripts/a2a_promote.js --validated --all
```

---

### 4. analyze_by_skill.js — 按 Skill 分析（4.7KB）

**功能**：按 Skill 维度统计进化历史，帮助识别哪些 Skill 最需要优化。

**输出统计项**：
- 每个 Skill 的修复次数
- 修复成功率
- 最常用 Gene
- 平均 blast radius
- 最近进化时间

**使用场景**：
```bash
node scripts/analyze_by_skill.js
# 输出：
# Skill: evolver | repairs: 12 | success_rate: 83% | top_gene: gene_gep_repair_from_errors
# Skill: gep     | repairs: 5  | success_rate: 100% | top_gene: gene_gep_optimize_prompt_and_assets
```

---

### 5. build_public.js — 公开发行版构建（11KB）

**功能**：构建去除私密信息的公开发行版，输出到 `dist-public/`。

**处理内容**：
- 移除内部配置（`~/.evomap/node_id`、`node_secret` 等引用）
- 脱敏本地路径
- 移除或替换私有 Hub URL
- 保留所有核心逻辑和文档

**环境变量**：
```bash
PUBLIC_REMOTE=public
PUBLIC_REPO=autogame-17/evolver
PUBLIC_OUT_DIR=dist-public
PUBLIC_USE_BUILD_OUTPUT=true
```

**使用场景**：
```bash
npm run build
# 等价于：node scripts/build_public.js
```

---

### 6. extract_log.js — 日志提取（2.5KB）

**功能**：从 OpenClaw 会话文件（`~/.openclaw/agents/.../sessions/*.jsonl`）提取原始日志文本。

**处理逻辑**：
- 读取 JSONL 格式的会话文件
- 提取 `tool_result`、`user`、`assistant` 等字段的文本内容
- 合并输出为纯文本，供信号分析使用

**使用场景**：
```bash
node scripts/extract_log.js ~/.openclaw/agents/myagent/sessions/2026-04-22.jsonl
```

---

### 7. generate_history.js — 历史摘要生成（2.5KB）

**功能**：根据 `assets/gep/events.jsonl` 生成进化历史摘要。

**输出内容**：
- 总进化次数、成功/失败分布
- 按 intent 分类统计（repair/optimize/innovate）
- 最近10次进化摘要（时间、Gene、结果）
- 进化树结构（parent_id 追踪）

**使用场景**：
```bash
node scripts/generate_history.js > evolution_history.md
```

---

### 8. gep_append_event.js — 手动追加事件（3KB）

**功能**：手动向 `events.jsonl` 追加 EvolutionEvent，用于测试或手工记录进化结果。

**使用场景**：
```bash
# 测试时伪造历史事件
echo '{"type":"EvolutionEvent","id":"evt_test_001",...}' | node scripts/gep_append_event.js

# 或直接通过参数
node scripts/gep_append_event.js --file event.json
```

---

### 9. gep_personality_report.js — 人格状态报告（7.7KB）

**功能**：分析 PersonalityState 的历史变化趋势，生成可读报告。

**报告内容**：
- 当前人格各维度数值（rigor, risk_tolerance, curiosity, patience, confidence）
- 各维度过去 N 个循环的变化趋势（折线图 ASCII）
- 与进化结果的相关性分析（高 rigor → 更多成功？）
- 安全降级触发统计（规则1/规则2 各触发几次）
- 建议：当前人格适合的策略预设

**使用场景**：
```bash
node scripts/gep_personality_report.js
# 定期运行，了解 Agent 人格演化方向
```

---

### 10. human_report.js — 人类可读报告（5.7KB）

**功能**：生成面向操作者的 Markdown 进化总结，适合定期 review。

**报告章节**：
```markdown
## 进化总览
- 总循环数、成功率、平均 blast radius

## 信号分布
- 最常见信号 Top 10（本周）

## Gene 使用统计
- 各 Gene 使用次数和成功率

## 重大里程碑
- 首次成功的 innovate 事件
- 最高分 Capsule

## 建议
- 当前策略是否需要调整？
- 是否有广播候选？
```

**使用场景**：
```bash
# 每周 review 时运行
node scripts/human_report.js > weekly_report.md
```

---

### 11. publish_public.js — 公开版本发布（20KB）

**功能**：完整的发布流程脚本：构建 → 推送 → 打 Tag → 创建 GitHub Release。

**执行流程**：
```
1. 检查 git 状态（工作区必须干净）
2. 运行 build_public.js 构建 dist-public/
3. 推送到 PUBLIC_REMOTE/PUBLIC_BRANCH
4. 如果设置 RELEASE_TAG：
   a. 创建 git tag
   b. 调用 GitHub API 创建 Release（或使用 gh CLI）
   c. 上传 Release Notes
```

**关键环境变量**：
```bash
PUBLIC_REMOTE=public                    # git remote 名称
PUBLIC_REPO=autogame-17/evolver         # GitHub 仓库
PUBLIC_BRANCH=main                      # 目标分支
RELEASE_TAG=v1.20.1                     # 版本号
RELEASE_TITLE="v1.20.1 - GEP protocol" # Release 标题
RELEASE_NOTES_FILE=CHANGELOG.md         # Release Notes 来源
GITHUB_TOKEN=ghp_...                    # GitHub PAT（repo 权限）
DRY_RUN=true                            # 干运行，不实际发布
RELEASE_SKIP=true                       # 只推送，不创建 Release
RELEASE_USE_GH=true                     # 使用 gh CLI 替代 API
PUBLIC_RELEASE_ONLY=true                # 只创建 Release（Tag 已存在）
```

---

### 12. recover_loop.js — 循环恢复（1.7KB）

**功能**：检测进化循环是否停滞（长时间无 EvolutionEvent 写入），并尝试恢复。

**停滞判定逻辑**：
- 读取 `events.jsonl` 最后一条事件的时间戳
- 如果超过阈值（如 2 小时）无新事件，认为循环停滞
- 尝试重启循环进程（`node index.js --loop`）

**使用场景**：
```bash
# 加入 cron，定期检查
*/30 * * * * node /path/to/scripts/recover_loop.js
```

---

### 13. suggest_version.js — 版本号建议（3KB）

**功能**：基于最近的 EvolutionEvent 分析变更类型，建议下一个 SemVer 版本号。

**决策逻辑**：
```
有 MAJOR 变更（breaking change 信号）→ MAJOR+1.0.0
有 innovate 类别成功 → MINOR+1
只有 repair/optimize 成功 → PATCH+1
```

**使用场景**：
```bash
node scripts/suggest_version.js
# 输出：当前版本 v1.20.0 → 建议 v1.20.1（PATCH 修复）
```

---

### 14. validate-modules.js — 模块可加载校验（1.2KB）

**功能**：检查指定 Node.js 模块文件是否能被 `require()` 加载且无语法错误。

**实现原理**：
```js
for (const modulePath of args) {
  try {
    delete require.cache[require.resolve(modulePath)];
    require(modulePath);
    console.log('ok:', modulePath);
  } catch (e) {
    console.error('FAIL:', modulePath, e.message);
    process.exit(1);
  }
}
```

**在 Gene validation 中的用途**：
```json
"validation": [
  "node scripts/validate-modules.js ./src/evolve ./src/gep/solidify",
  "node scripts/validate-modules.js ./src/gep/selector ./src/gep/memoryGraph"
]
```

> **这是最常见的 Gene 校验命令**，确保进化不引入语法错误或循环 require。

---

### 15. validate-suite.js — 完整校验套件（1.8KB）

**功能**：依次运行所有核心模块的 validate-modules 检查，返回总体 pass/fail。

**检查列表**（示例）：
```
./src/evolve
./src/gep/signals
./src/gep/selector
./src/gep/prompt
./src/gep/solidify
./src/gep/assetStore
./src/gep/a2aProtocol
./src/gep/memoryGraph
```

**使用场景**：
```bash
# 手动 CI 前检查
node scripts/validate-suite.js
# Exit 0: All modules OK
# Exit 1: Module X failed to load: SyntaxError
```

---

## 二、Ops 运维模块（src/ops/）

### 1. lifecycle.js — 进程生命周期管理

**完整命令集**：

```bash
# 启动进化循环（后台运行，写入 PID 文件）
node src/ops/lifecycle.js start
# → 启动 `node index.js --loop` 子进程
# → PID 写入 ~/.evomap/evolver.pid

# 优雅停止
node src/ops/lifecycle.js stop
# → 发送 SIGTERM
# → 等待 5 秒
# → 如未退出，发送 SIGKILL

# 查看状态
node src/ops/lifecycle.js status
# → 输出：running (PID 12345) / stopped

# 健康检查
node src/ops/lifecycle.js check
# → 检查 PID 是否存活
# → 检查最近进化事件时间（停滞检测）
# → 如停滞超过阈值，自动重启
```

---

### 2. skillMonitor.js — Skill 监控

**功能**：监控 Workspace 中各 Skill 的健康状态，检测失效 Skill 并告警。

**监控项**：
- Skill 的 `SKILL.md` 是否存在
- 声明的入口文件是否可加载
- 最近是否被成功调用

---

### 3. cleanup.js — 垃圾清理

**功能**：清理过期的临时文件，防止磁盘膨胀。

**清理目标**：
- `memory/evolution/` 下超过 N 天的旧 GEP Prompt 文件
- `assets/gep/a2a/outbox/` 下已同步的消息文件
- `assets/gep/external_candidates.jsonl` 中已处理的候选

---

### 4. selfRepair.js — 进化进程自修复

**功能**：检测进化进程异常退出（非0退出码），执行基础修复后重启。

**修复逻辑**：
1. 检查最后一条 EvolutionEvent 是否为失败
2. 如果失败：回滚最近变更（`git stash`）
3. 清除可能损坏的状态文件
4. 重新启动进化循环

---

### 5. wakeTrigger.js — 唤醒触发

**功能**：响应外部事件唤醒沉睡中的进化循环。

**触发条件**：
- cron 计划时间到达
- 接收到来自 EvoMap Hub 的 `wake` 消息（通过 Proxy mailbox）
- 检测到新的会话日志写入

---

## 三、工具链协作关系

```
                    日常运行
                       │
              node index.js --loop
                       │
              ┌────────┴────────┐
              │                 │
         进化成功           进化失败
              │                 │
    gep_append_event      recover_loop（自动重启）
    a2a_export（广播）    validate-suite（诊断）
    human_report（周报）   gep_personality_report（分析）
              │
         达到广播条件
              │
    ┌─────────┴──────────┐
    │                    │
a2a_export           发布流程
（导出到 outbox）    build_public
                     publish_public
                     suggest_version（版本号建议）

外部资产接收：
a2a_ingest（摄入）→ [人工审查] → a2a_promote（晋升 --validated）
```
