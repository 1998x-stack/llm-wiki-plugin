# GEP（Genome Evolution Protocol）— 基因进化协议完整分析

> **定位**：GEP 是 Evolver 的数据标准与协议规范，定义 AI Agent 如何通过"试验-校验-固化"循环获取新能力。
> **类比**：GEP 之于 Evolver，如同 git commit 协议之于版本控制——每次变更有标准结构、可追溯、可回滚。
> **实现路径**：`assets/gep/` + `src/gep/`

---

## 1. GEP 设计哲学

来自博客 [GEP Protocol Deep Dive](https://evomap.ai/blog/gep-protocol-deep-dive)：

> "DNA encodes organisms, Genes encode capabilities. Both evolve through selection, inheritance, and symbiosis."

GEP 的生物学类比：

| GEP 概念 | 生物学对应 | 具体含义 |
|---------|----------|---------|
| Gene | 基因 | 处理特定问题模式的原子化策略单元 |
| Capsule | 表现型记录 | 成功基因应用的"经验快照" |
| EvolutionEvent | 进化树节点 | 不可变的变更审计记录，通过 parent_id 构成谱系 |
| Mutation | 突变指令 | 带风险级别的显式变更对象 |
| Signals | 环境压力 | 从运行时观察提取的进化触发信号 |
| PersonalityState | 个体特征 | 影响变更倾向的 Agent 人格维度 |

---

## 2. 三类核心资产

### 2.1 Gene（基因）— 可复用策略模板

Gene 是 GEP 的"遗传单元"，定义针对特定信号模式的标准化处理策略。

**完整 JSON 结构**：
```json
{
  "type": "Gene",
  "id": "gene_gep_repair_from_errors",
  "category": "repair",
  "signals_match": [
    "error",
    "exception",
    "failed",
    "unstable"
  ],
  "preconditions": [
    "signals contains error-related indicators"
  ],
  "strategy": [
    "Extract structured signals from logs and user instructions",
    "Select an existing Gene by signals match (no improvisation)",
    "Estimate blast radius (files, lines) before editing",
    "Apply smallest reversible patch",
    "Validate using declared validation steps; rollback on failure",
    "Solidify knowledge: append EvolutionEvent, update Gene/Capsule store"
  ],
  "constraints": {
    "max_files": 20,
    "forbidden_paths": [".git", "node_modules"]
  },
  "validation": [
    "node scripts/validate-modules.js ./src/evolve ./src/gep/solidify",
    "node scripts/validate-modules.js ./src/gep/selector ./src/gep/memoryGraph"
  ]
}
```

**字段详解**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✓ | 固定为 `"Gene"` |
| `id` | string | ✓ | 全局唯一标识符 |
| `category` | enum | ✓ | `repair` / `optimize` / `innovate` |
| `signals_match` | string[] | ✓ | 触发此 Gene 的信号关键词列表 |
| `preconditions` | string[] | - | 人类可读的激活前提条件 |
| `strategy` | string[] | ✓ | 执行步骤列表 |
| `constraints.max_files` | number | ✓ | 单次进化最多修改文件数 |
| `constraints.forbidden_paths` | string[] | ✓ | 禁止修改的路径列表 |
| `validation` | string[] | ✓ | 固化前必须通过的校验命令 |

---

**内置三类 Gene 对比**：

| Gene ID | 类别 | 主要信号触发 | max_files | 激活前提 |
|---------|------|------------|-----------|---------|
| `gene_gep_repair_from_errors` | repair | `error`, `exception`, `failed`, `unstable` | 20 | 存在错误相关信号 |
| `gene_gep_optimize_prompt_and_assets` | optimize | `protocol`, `gep`, `prompt`, `audit`, `reusable` | 20 | 需要更严格可审计的协议输出 |
| `gene_gep_innovate_from_opportunity` | innovate | `user_feature_request`, `capability_gap`, `stable_success_plateau`, `perf_bottleneck` | 25 | 系统稳定且无 `log_error` |

**Gene 选择优先级**（`src/gep/selector.js`）：
1. **记忆图偏好**：高置信历史路径优先
2. **信号匹配分**：`匹配关键词数 / signals_match总数`
3. **类别优先**：Repair > Optimize > Innovate
4. **用户意图**：可显式覆盖

**Drift 强度**（模拟生物遗传漂变，逃离局部最优）：
```js
// 小种群 = 更强漂变
// Ne=1: intensity=1.0, Ne=25: intensity=0.2, Ne=100: intensity=0.1
intensity = Math.min(1, 1 / Math.sqrt(effectivePopulationSize))
```

---

### 2.2 Capsule（胶囊）— 成功解决方案快照

Capsule 是 Gene 成功应用后固化的"经验记录"，带真实结果追踪。

**完整 JSON 结构**：
```json
{
  "type": "Capsule",
  "schema_version": "1.5.0",
  "id": "capsule_1770477654236",
  "trigger": [
    "log_error",
    "errsig:**TOOLRESULT**: { \"status\": \"error\", \"tool\": \"exec\", \"error\": \"error: unknown command 'process'\" }",
    "windows_shell_incompatible",
    "perf_bottleneck"
  ],
  "gene": "gene_gep_repair_from_errors",
  "summary": "修复 exec 命令兼容性问题，变更 1 文件 / 2 行",
  "confidence": 0.85,
  "blast_radius": {
    "files": 1,
    "lines": 2
  },
  "outcome": {
    "status": "success",
    "score": 0.85
  },
  "success_streak": 2,
  "env_fingerprint": {
    "node_version": "v22.22.0",
    "platform": "linux",
    "arch": "x64",
    "os_release": "6.1.0-42-cloud-amd64",
    "evolver_version": "1.7.0",
    "cwd": ".",
    "captured_at": "2026-02-07T15:20:54.155Z"
  },
  "a2a": {
    "eligible_to_broadcast": true
  },
  "asset_id": "sha256:3eed0cd5038f9e85fbe0d093890e291e9b8725644c766e6cce40bf62d0f5a2e8"
}
```

**字段详解**：

| 字段 | 说明 |
|------|------|
| `schema_version` | 当前为 `"1.5.0"` |
| `trigger` | 触发此 Capsule 的信号列表（用于后续匹配） |
| `gene` | 使用的 Gene ID |
| `confidence` | 置信分（0~1），基于校验结果和 blast radius |
| `blast_radius` | 实际变更范围（files 和 lines） |
| `outcome.status` | `success` 或 `failed` |
| `success_streak` | 连续成功应用次数（用于广播资格判断） |
| `env_fingerprint` | 环境元数据（用于兼容性过滤） |
| `a2a.eligible_to_broadcast` | 是否满足 A2A 广播资格 |
| `asset_id` | SHA-256 内容哈希（去重 + 签名验证） |

---

**置信度计算**：
```js
const baseConfidence = 0.8;  // 校验通过基础分
const blastPenalty = Math.min(0.1, (files / 10) * 0.05);  // 变更越大扣分
confidence = baseConfidence - blastPenalty;
```

**A2A 广播资格**（三条全满足）：
```js
function isCapsuleBroadcastEligible(capsule) {
  if (capsule.outcome.score < 0.7)       return false;  // 分数不足
  if (capsule.blast_radius.files > 5)    return false;  // 变更太大
  if (capsule.blast_radius.lines > 200)  return false;  // 变更太大
  if (capsule.success_streak < 2)        return false;  // 尚未验证
  return true;
}
```

**外部 Capsule 置信度降级**：接收其他 Agent 的 Capsule 时，`confidence × 0.6`（环境差异保护）

**Capsule 重用评分公式**（`src/gep/hubSearch.js`）：
```
score = confidence × min(success_streak, 5) × (reputation / 100)
```
- `score >= 0.72`：注入 Prompt 作为参考
- `score >= 0.85`：直接复用，跳过本地推理

**Failed Capsule 记录**：校验失败时仍记录 Capsule（存入 `failed_capsules.json`），防止后续重复尝试同一失败方案。

---

### 2.3 EvolutionEvent（进化事件）— 不可变审计日志

EvolutionEvent 通过 `parent_id` 构成有向进化树，每个节点代表一次完整的进化循环。

**完整 JSONL 结构**：
```json
{
  "type": "EvolutionEvent",
  "id": "evt_1770477654237",
  "parent_id": "evt_1770477201173",
  "timestamp": "2026-02-07T15:20:54.236Z",
  "intent": "repair",
  "signals": ["log_error", "errsig:TypeError: Cannot read property..."],
  "genes_used": ["gene_gep_repair_from_errors"],
  "mutation": {
    "type": "Mutation",
    "id": "mut_1770477654200",
    "category": "repair",
    "trigger_signals": ["log_error"],
    "target": "gene:error_handling_robust",
    "expected_effect": "reduce runtime errors and increase stability",
    "risk_level": "low"
  },
  "outcome": {
    "status": "success",
    "score": 0.85
  },
  "blast_radius": {
    "files": 1,
    "lines": 2
  },
  "capsule_id": "capsule_1770477654236",
  "personality_snapshot": {
    "rigor": 0.8,
    "risk_tolerance": 0.3,
    "curiosity": 0.5
  }
}
```

**事件树示意**：
```
evt_0001 (root)
├── evt_0002 (repair - success)
│   └── evt_0003 (optimize - success)
│       └── evt_0005 (innovate - failed)
│           └── evt_0007 (repair - success)
└── evt_0004 (innovate - success)
    └── evt_0006 (optimize - success)
```

**审计能力**：
- 追溯任意能力的进化来源
- 计算每个 Gene 的历史成功率
- 检测修复循环（同一 Gene 连续失败）
- 合规场景下的完整变更审计

---

## 3. GEP 资产存储结构

```
assets/gep/
├── genes.json                # Gene 定义数组（可扩展）
├── capsules.json             # Capsule 数组（按时间追加）
├── events.jsonl              # 不可变事件日志（JSONL，只追加）
├── candidates.jsonl          # 本地实验候选（待固化）
├── external_candidates.jsonl # A2A 接收的外部资产（待审查）
├── failed_capsules.json      # 失败 Capsule（防重复）
└── a2a/
    ├── outbox/publish.jsonl  # 待广播消息
    └── inbox/publish.jsonl   # 已接收消息
```

---

## 4. GEP 协议约束

| 约束项 | 值 | 说明 |
|--------|-----|------|
| `constraints.max_files` | Gene 定义（repair: 20, innovate: 25）| 单次进化文件数上限 |
| `constraints.forbidden_paths` | `.git`, `node_modules` | 绝对禁止修改 |
| `validation` | 必须非空 | 无校验命令的 Gene 不合法 |
| 文档 Emoji | 仅允许 🧬 | 所有其他 Emoji 禁止出现在文档中 |
| 系统硬上限 | `EVOLVER_HARD_CAP_FILES=60`, `LINES=20000` | 覆盖 Gene 级别约束 |

---

## 5. GEP Prompt 输出规范（v1.10.3 STRICT）

LLM 被要求严格按顺序输出 5 个 JSON 对象：

```
1. Mutation        ← 本次变更指令（类别、风险、目标、预期效果）
2. PersonalityState ← 人格状态更新（rigor, risk_tolerance, curiosity 等）
3. EvolutionEvent  ← 完整进化事件记录（含 parent_id、blast_radius）
4. Capsule         ← 成功解决方案封装
5. FilePatches     ← 实际代码变更（unified diff 格式）
```

任何偏离此顺序或格式的输出都会导致 Solidify 拒绝。

---

## 6. GEP 与 MCP 的关系

引用官方博客：
> "MCP solved the connection problem between AI and the world. GEP opens the door to AI self-improvement."

| 协议 | 解决的问题 |
|------|----------|
| MCP（Model Context Protocol）| AI 与外部工具/服务的连接（Tool Use）|
| GEP（Genome Evolution Protocol）| AI 能力的持续自我改进（Self-Evolution）|

EvoMap 还维护了独立的 MCP Server：`EvoMap/gep-mcp-server`，将 GEP 工具暴露给 Claude Desktop、Cursor 等 MCP 客户端。
