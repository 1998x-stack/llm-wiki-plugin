# Mutation 系统与策略预设

> **源文件**: `src/gep/mutation.js`（通过 `src/evolve.js` 调用）
> **核心职责**: 将信号列表转化为带风险级别的显式变更指令，并施加安全约束
> **设计理念**: "让所有进化决策可审计、可回溯、可拒绝"

---

## 1. Mutation 对象完整结构

Mutation 是 GEP 中的**一等公民**，每次进化循环都必须产生一个 Mutation 对象：

```json
{
  "type": "Mutation",
  "id": "mut_1709876543210",
  "category": "repair",
  "trigger_signals": [
    "log_error",
    "errsig:TypeError: Cannot read property 'id' of undefined at evolve.js:891"
  ],
  "target": "gene:error_handling_robust",
  "expected_effect": "reduce runtime errors, increase stability, and lower failure rate",
  "risk_level": "low"
}
```

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✓ | 固定为 `"Mutation"` |
| `id` | string | ✓ | `mut_` + Unix 时间戳（毫秒）|
| `category` | enum | ✓ | `repair` / `optimize` / `innovate` |
| `trigger_signals` | string[] | ✓ | 触发本次 Mutation 的信号列表（去重后）|
| `target` | string | ✓ | 变更目标（如 `gene:xxx`，`behavior:protocol`）|
| `expected_effect` | string | ✓ | 人类可读的预期效果描述 |
| `risk_level` | enum | ✓ | `low` / `medium` / `high` |

---

## 2. 类别（category）决策树

```js
// src/gep/mutation.js:55
function mutationCategoryFromContext({ signals, driftEnabled }) {
  // 1. 有错误信号 → 修复优先
  if (hasErrorishSignal(signals)) return 'repair';

  // 2. 启用漂变 → 探索模式
  if (driftEnabled) return 'innovate';

  // 3. 有机会信号 → 创新
  if (hasOpportunitySignal(signals)) return 'innovate';

  // 4. 策略预设要求创新
  try {
    const strategy = require('./strategy').resolveStrategy();
    if (strategy && strategy.innovate >= 0.5) return 'innovate';
  } catch (_) {}

  // 5. 默认 → 优化
  return 'optimize';
}
```

**错误信号判定**（`hasErrorishSignal`）：
```js
const errorSignals = ['log_error', 'recurring_error', 'repair_loop_detected',
                      'failure_loop_detected', 'consecutive_failure_streak'];
```

**机会信号判定**（`hasOpportunitySignal`）：
```js
const opportunitySignals = ['user_feature_request', 'user_improvement_suggestion',
                            'capability_gap', 'perf_bottleneck', 'external_opportunity',
                            'force_innovation_after_repair_loop', 'empty_cycle_loop_detected'];
```

---

## 3. 各类别的默认预期效果

```js
// src/gep/mutation.js:71
function expectedEffectFromCategory(category) {
  if (category === 'repair')
    return 'reduce runtime errors, increase stability, and lower failure rate';
  if (category === 'optimize')
    return 'improve success rate and reduce repeated operational cost';
  if (category === 'innovate')
    return 'explore new strategy combinations to escape local optimum';
  return 'improve agent behavior';
}
```

---

## 4. 风险级别（risk_level）赋值逻辑

### 4.1 默认赋值

| 类别 | 默认风险 | 理由 |
|------|---------|------|
| `repair` | `low` | 最小化变更，修复已知问题 |
| `optimize` | `low` | 保守改进 |
| `innovate` | `medium` | 探索性，影响未知 |
| `innovate` + `allowHighRisk=true` | `high` | 显式许可的大规模重构 |

### 4.2 Blast Radius 风险矩阵

| 风险级别 | 典型文件数 | 典型行数 | 推荐校验策略 |
|---------|----------|---------|------------|
| `low` | 1–3 | < 50 | 局部模块测试 |
| `medium` | 3–10 | 50–200 | 完整测试套件 |
| `high` | 10+ | 200+ | 多阶段校验 + 人工审核 |

---

## 5. 两条硬安全规则

### 规则 1：禁止 innovate + 高风险人格

```js
// src/gep/mutation.js:134
const highRiskPersonality = isHighRiskPersonality(personalityState);
if (base.category === 'innovate' && highRiskPersonality) {
  base.category = 'optimize';
  base.expected_effect = 'safety downgrade: optimize under high-risk personality';
  base.risk_level = 'low';
  base.trigger_signals.push('safety:avoid_innovate_with_high_risk_personality');
}
```

**高风险人格定义**：
```js
function isHighRiskPersonality(p) {
  const rigor = p?.rigor ?? null;
  const riskTol = p?.risk_tolerance ?? null;
  if (rigor != null && rigor < 0.5)    return true;  // 严谨度不足
  if (riskTol != null && riskTol > 0.6) return true;  // 风险容忍度过高
  return false;
}
```

**逻辑**：严谨度低的 Agent 更容易犯错，此时叠加创新变更会放大风险，强制降级为保守的 optimize。

### 规则 2：高风险变更需要"安全人格"

```js
// src/gep/mutation.js:142
if (base.risk_level === 'high' && !isHighRiskMutationAllowed(personalityState)) {
  base.risk_level = 'medium';
  base.trigger_signals.push('safety:downgrade_high_risk');
}

function isHighRiskMutationAllowed(p) {
  const rigor = p?.rigor || 0;
  const riskTol = p?.risk_tolerance || 1;
  return rigor >= 0.6 && riskTol <= 0.5;  // 高严谨 + 低冒险
}
```

**逻辑**：只有严谨度高且风险容忍度低的稳健 Agent，才被允许执行高风险大范围变更。

---

## 6. 三个 Mutation 示例

### 6.1 典型修复 Mutation

```json
{
  "type": "Mutation",
  "id": "mut_1709876543210",
  "category": "repair",
  "trigger_signals": [
    "log_error",
    "errsig:TypeError: Cannot read property 'id' of undefined"
  ],
  "target": "gene:error_handling_robust",
  "expected_effect": "reduce runtime errors, increase stability, and lower failure rate",
  "risk_level": "low"
}
```

### 6.2 典型创新 Mutation

```json
{
  "type": "Mutation",
  "id": "mut_1709876654321",
  "category": "innovate",
  "trigger_signals": [
    "user_feature_request:add support for CSV export",
    "capability_gap"
  ],
  "target": "gene:feature_expansion",
  "expected_effect": "explore new strategy combinations to escape local optimum",
  "risk_level": "medium"
}
```

### 6.3 安全降级 Mutation（规则 1 触发）

```json
{
  "type": "Mutation",
  "id": "mut_1709876765432",
  "category": "optimize",
  "trigger_signals": [
    "user_feature_request:refactor authentication system",
    "safety:avoid_innovate_with_high_risk_personality"
  ],
  "target": "behavior:protocol",
  "expected_effect": "safety downgrade: optimize under high-risk personality (rigor=0.4)",
  "risk_level": "low"
}
```

---

## 7. Mutation 生命周期

```
1. BUILD    buildMutation() → 根据信号、Gene、人格构造 Mutation 对象
2. VALIDATE isValidMutation() → 检查 schema 合规性
3. EMBED    嵌入 GEP Prompt → LLM 使用 Mutation 作为变更指令
4. EXECUTE  LLM 执行变更（FilePatches）
5. RECORD   EvolutionEvent 中记录完整 Mutation + blast_radius + outcome
6. LEARN    记忆图更新信号-基因-结果因果链路
```

---

## 8. 策略预设（EVOLVE_STRATEGY）完整参考

策略预设通过 `src/gep/strategy.js` 的 `resolveStrategy()` 函数解析：

| 策略名 | repair 权重 | optimize 权重 | innovate 权重 | 适用场景 |
|--------|-----------|-------------|--------------|---------|
| `balanced` | 0.4 | 0.3 | 0.3 | 日常运行（默认）|
| `innovate` | 0.1 | 0.1 | 0.8 | 功能开发期 |
| `harden` | 0.5 | 0.4 | 0.1 | 生产强化 / 稳定性冲刺 |
| `repair-only` | 1.0 | 0.0 | 0.0 | 紧急修复，禁止任何创新 |
| `early-stabilize` | 0.6 | 0.3 | 0.1 | 新 Agent 上线初期 |
| `steady-state` | 0.2 | 0.6 | 0.2 | 系统成熟期，以优化为主 |
| `auto` | 动态 | 动态 | 动态 | 根据信号分布自动调整 |

**策略影响 Mutation 决策的入口**：
```js
// 在 mutationCategoryFromContext 中
const strategy = resolveStrategy();
if (strategy.innovate >= 0.5) return 'innovate';
```

**使用方式**：
```bash
# 环境变量
EVOLVE_STRATEGY=harden node index.js --loop

# 或持久化到 .env
echo "EVOLVE_STRATEGY=steady-state" >> .env
```

---

## 9. 人格状态（PersonalityState）与 Mutation 的联动

人格状态是一个**多维度连续空间**，在进化循环中随历史结果动态更新：

| 维度 | 范围 | 含义 | 对 Mutation 的影响 |
|------|------|------|-----------------|
| `rigor` | 0~1 | 严谨程度 | < 0.5 触发安全降级 |
| `risk_tolerance` | 0~1 | 风险容忍度 | > 0.6 触发安全降级；<= 0.5 才允许 high-risk |
| `curiosity` | 0~1 | 探索倾向 | 影响 innovate 意图的激活阈值 |
| `patience` | 0~1 | 耐心程度 | 影响循环退避时长 |
| `confidence` | 0~1 | 自信度 | 影响重用历史 Capsule vs 重新探索的倾向 |

人格状态会随每次进化结果发生自然选择（成功 → 强化相关特质，失败 → 降低对应维度）。
