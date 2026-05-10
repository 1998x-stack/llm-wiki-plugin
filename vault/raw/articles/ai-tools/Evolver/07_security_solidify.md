# Evolver 安全模型与 Solidify 机制

> **源文件**: `src/gep/solidify.js`（进化固化核心）
> **目标**: 在允许代码自进化的同时，防止失控的"进化"破坏系统稳定性

---

## 1. 安全设计哲学

Evolver 的安全模型基于"深度防御"，有多层独立的安全边界：

```
Layer 1: Gene 级约束    ← max_files / forbidden_paths / validation 声明
Layer 2: 系统硬上限    ← EVOLVER_HARD_CAP_FILES=60 / LINES=20000
Layer 3: 命令白名单    ← 只允许 node/npm/npx，禁止 Shell 操作符
Layer 4: 人格检查      ← Mutation 安全降级规则
Layer 5: 受保护文件    ← Evolver 核心源码不可被自己修改
Layer 6: git 回滚      ← 失败时 hard/stash 回滚
Layer 7: 人工审核      ← --review 模式、A2A 晋升 --validated
```

---

## 2. 组件执行权限矩阵

| 组件 | 主要职责 | 执行 Shell 命令？ | 写文件？ | 网络？ |
|------|---------|----------------|---------|-------|
| `src/evolve.js` | 读日志、选基因、构建 Prompt | 只读 git/进程查询 | 只写 memory/ 和 assets/ | 通过 Proxy |
| `src/gep/prompt.js` | 组装 GEP Prompt 字符串 | ✗ 纯文本生成 | ✗ | ✗ |
| `src/gep/selector.js` | 评分选择 Gene/Capsule | ✗ 纯逻辑 | ✗ | ✗ |
| `src/gep/solidify.js` | 校验并固化变更 | **✓ 执行 Gene validation 命令** | ✓ 写 events.jsonl 等 | ✗ |
| `src/gep/a2aProtocol.js` | A2A 消息构建 | ✗ | ✓ 写 outbox/ | ✓ 通过 Proxy |
| `index.js`（崩溃恢复）| 打印 sessions_spawn(...) | ✗ 只是文本输出 | ✗ | ✗ |

---

## 3. Gene Validation 命令安全门（5 条规则）

`solidify.js` 中的 `isValidationCommandAllowed()` 函数，执行校验命令前强制检查：

```js
function isValidationCommandAllowed(cmd) {
  // 规则 1: 命令前缀白名单
  if (!/^(node|npm|npx)\s/.test(cmd)) {
    return { allowed: false, reason: 'Command must start with node/npm/npx' };
  }

  // 规则 2: 禁止命令替换（backtick 和 $()）
  if (cmd.includes('`') || cmd.includes('$(')) {
    return { allowed: false, reason: 'Command substitution not allowed' };
  }

  // 规则 3: 禁止 Shell 操作符（去掉引号内容后检查）
  const stripped = cmd.replace(/(["'])(?:(?=(\\?))\2.)*?\1/g, '');
  if (/[;&|><]/.test(stripped)) {
    return { allowed: false, reason: 'Shell operators not allowed' };
  }

  // 规则 4: 超时限制（通过执行参数传入）
  // 每条命令最长 180 秒，超时自动终止

  // 规则 5: 作用域锁定
  // execSync(cmd, { cwd: REPO_ROOT })  ← 始终在仓库根目录执行

  return { allowed: true };
}
```

**实际执行示例**：
```js
for (const cmd of gene.validation) {
  const check = isValidationCommandAllowed(cmd);
  if (!check.allowed) {
    throw new Error(`Validation command rejected: ${check.reason}: ${cmd}`);
  }

  const result = execSync(cmd, {
    cwd: REPO_ROOT,
    timeout: 180 * 1000,
    encoding: 'utf8'
  });
}
```

---

## 4. Blast Radius 控制

### 4.1 多层上限

| 层次 | 来源 | 文件数上限 | 行数上限 |
|------|------|----------|---------|
| Gene 级别 | `gene.constraints.max_files` | repair: 20, innovate: 25 | 未设置 |
| 系统硬上限 | `EVOLVER_HARD_CAP_FILES/LINES` | 60（默认）| 20000（默认）|
| A2A 外部资产 | `A2A_MAX_FILES/LINES` | 5 | 200 |

> 系统硬上限始终覆盖 Gene 级别约束。

### 4.2 Blast Radius 计算方法

```js
// 通过 git diff --cached --shortstat 计算
function computeBlastRadius() {
  const output = execSync('git diff --cached --shortstat', { cwd: REPO_ROOT });
  // 示例输出: "2 files changed, 44 insertions(+), 12 deletions(-)"
  const match = output.match(/(\d+) files? changed(?:, (\d+) insertions)?(?:, (\d+) deletions)?/);
  return {
    files: parseInt(match?.[1] || '0'),
    insertions: parseInt(match?.[2] || '0'),
    deletions: parseInt(match?.[3] || '0'),
    lines: parseInt(match?.[2] || '0') + parseInt(match?.[3] || '0')
  };
}
```

### 4.3 超限处理

Blast Radius 超过任何层级的上限时：
1. 中止固化流程
2. 执行回滚（根据 `EVOLVER_ROLLBACK_MODE`）
3. 写入失败 EvolutionEvent
4. 若在循环模式，等待后进入下一轮

---

## 5. 受保护文件（Protected Files）

当 `EVOLVE_ALLOW_SELF_MODIFY=false`（默认值）时，以下文件进入保护名单，禁止进化修改：

```js
const PROTECTED_FILES = [
  'src/evolve.js',
  'src/gep/solidify.js',
  'src/gep/selector.js',
  'src/gep/prompt.js',
  'src/gep/signals.js',
  'src/gep/a2aProtocol.js',
  'index.js',
  'assets/gep/genes.json',  // 防止 Gene 定义被污染
  'assets/gep/events.jsonl', // 防止审计日志被篡改
];
```

**检测时机**：solidify.js 在执行 FilePatches 之前，检查变更文件列表是否包含受保护文件。

> **警告**（来自官方文档）：`EVOLVE_ALLOW_SELF_MODIFY=true` 可能导致 Evolver 引入 Bug 到自身 Prompt 生成逻辑，造成级联失败，需要人工干预恢复。仅用于受控实验。

---

## 6. 回滚策略

通过 `EVOLVER_ROLLBACK_MODE` 控制：

| 模式 | git 操作 | 适用场景 | 风险 |
|------|---------|---------|------|
| `hard`（默认）| `git reset --hard HEAD` | 需要完全干净的回滚 | 丢失所有未提交变更 |
| `stash` | `git stash` | 需要保留变更以供分析 | 可能积累 stash 堆栈 |
| `none` | 无操作 | 手动排查场景 | 变更保留，需人工处理 |

**回滚触发条件**：
1. Gene validation 命令失败（非零退出码）
2. Blast Radius 超过任何层级的上限
3. 尝试修改受保护文件
4. EvolutionEvent 写入失败（记忆图写入失败中止整个循环）

---

## 7. Solidify 完整流程

```
LLM 输出的 FilePatches
    ↓
┌── 1. 解析 FilePatches（unified diff 格式）
│
├── 2. 受保护文件检查（if EVOLVE_ALLOW_SELF_MODIFY=false）
│       ↓ 触及保护文件 → 中止 + 回滚
│
├── 3. 应用 FilePatches 到工作区
│
├── 4. 计算 Blast Radius（git diff --cached --shortstat）
│       ↓ 超限 → 中止 + 回滚
│
├── 5. 执行 Gene validation 命令（按顺序，每条最多 180s）
│       ↓ 任一失败 → 中止 + 回滚
│
├── 6. 提交变更（git commit）
│
├── 7. 构建 Capsule（含 blast_radius, env_fingerprint, outcome）
│
├── 8. 追加 EvolutionEvent 到 events.jsonl（如失败 → 中止整个循环）
│
├── 9. 更新 capsules.json
│
├── 10. 更新记忆图（信号-基因-结果链路）
│
└── 11. 检查 A2A 广播资格 → 如满足，写入 outbox/
```

---

## 8. 自动 GitHub Issue 上报

当检测到持续失败时，自动向上游仓库提交 Bug Report：

**触发条件**（全部满足）：
```js
// src/evolve.js
const shouldReport =
  consecutiveFailures >= EVOLVER_ISSUE_MIN_STREAK  // 默认 5
  && timeSinceLastReport > EVOLVER_ISSUE_COOLDOWN_MS // 默认 24h
  && process.env.EVOLVER_AUTO_ISSUE !== 'false'
  && process.env.GITHUB_TOKEN;  // 有 token
```

**敏感数据脱敏规则**（上报前清洗）：
```js
// 过滤以下内容
const REDACT_PATTERNS = [
  /ghp_[A-Za-z0-9]{36}/g,           // GitHub token
  /node_[a-f0-9]{12}/g,              // Node ID
  /[A-Za-z0-9+/]{40,}={0,2}/g,      // Base64 secrets
  /\/home\/\w+/g,                    // 本地用户路径
  /\/Users\/\w+/g,                   // macOS 路径
  /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g, // 邮箱
];
```

**Issue 内容**：
- 错误签名（`errsig:`）
- 连续失败次数和时间跨度
- 环境指纹（Node 版本、平台、Evolver 版本）
- 最近 3 条 EvolutionEvent 摘要（脱敏后）

---

## 9. sessions_spawn 输出说明

`index.js` 和 `evolve.js` 在崩溃恢复时向 stdout 输出：
```
sessions_spawn({"command": "node index.js --loop", "reason": "loop_recovery"})
```

**重要说明**：这是**纯文本输出到 stdout**，不是函数调用。是否被执行完全取决于宿主运行时（如 OpenClaw 平台的 session spawner）。Evolver 自身不执行 `sessions_spawn`。

---

## 10. 安全模型总结与实践建议

| 安全关注点 | 推荐配置 | 备注 |
|----------|---------|------|
| 防止自我修改 | `EVOLVE_ALLOW_SELF_MODIFY=false`（默认）| 生产必须保持 false |
| 回滚安全 | `EVOLVER_ROLLBACK_MODE=stash` | 比 hard 更利于排查 |
| Blast Radius | `EVOLVER_HARD_CAP_FILES=10`（生产收紧）| 默认 60 偏宽松 |
| Hub 凭证 | 不提供 `A2A_NODE_SECRET`/`GITHUB_TOKEN` | 先离线评估后再连接 |
| A2A 摄入 | 人工 review 后才 `--validated` 晋升 | 外部资产不自动生效 |
| 生产使用 | `node index.js --review`（启用人工审核）| 避免直接 `--loop` |
| 沙箱测试 | 独立 cwd，隔离 git 历史 | 防止读取其他 Agent 日志 |
