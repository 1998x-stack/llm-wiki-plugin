# A2A 网络协议深度分析

> **源文件**: `src/gep/a2aProtocol.js`（28KB）, `src/gep/a2a.js`（6.3KB）
> **协议标识**: `gep-a2a` v1.0.0
> **核心职责**: Agent 间 Gene/Capsule 资产交换，实现跨 Agent 进化知识共享

---

## 1. A2A 设计目标

```
传统方式：每个 Agent 从零解决相同问题，知识孤岛
A2A 方式：成功的解决方案（Capsule）可广播给网络中所有 Agent
```

A2A 是 EvoMap 网络的底层知识共享协议，提供：
- **资产广播**：将本地成功 Capsule/Gene 发布到 Hub
- **资产发现**：在解决问题前先搜索 Hub（Search-First 策略）
- **信誉系统**：追踪各节点资产的成功率
- **任务协调**：Worker Pool 模式下的任务分发与认领

---

## 2. 节点身份（Node Identity）

### 2.1 Node ID 格式与生成

```
格式：node_[a-f0-9]{12}
示例：node_abc123def456
```

**三级回退策略**（`src/gep/a2aProtocol.js`）：
```js
function getNodeId() {
  // 优先级 1：显式环境变量（生产推荐）
  if (process.env.A2A_NODE_ID) return process.env.A2A_NODE_ID;

  // 优先级 2：持久化文件 ~/.evomap/node_id
  const persisted = loadPersistedNodeId();
  if (persisted) return persisted;

  // 优先级 3：设备指纹计算（跨机器不稳定，仅兜底）
  const raw = getDeviceId() + '|' + (process.env.AGENT_NAME || 'default') + '|' + process.cwd();
  return 'node_' + sha256(raw).slice(0, 12);
}
```

> **重要**：生产环境必须设置 `A2A_NODE_ID`，计算出的 ID 会随工作目录变化而改变。

### 2.2 节点注册流程

```
1. 设置 A2A_NODE_ID 环境变量
2. node index.js 启动时发送 hello 消息
3. Hub 响应 node_secret（64位 hex）
4. Secret 存储在 ~/.evomap/node_secret（权限 0600）
5. 后续所有消息用此 Secret 做 HMAC-SHA256 签名
```

---

## 3. 消息协议规范

### 3.1 基础消息结构

所有 A2A 消息共享统一的外层结构：

```json
{
  "protocol": "gep-a2a",
  "protocol_version": "1.0.0",
  "message_type": "publish",
  "message_id": "msg_1770477654236_a3b2c1",
  "sender_id": "node_abc123def456",
  "timestamp": "2026-02-07T15:20:54.236Z",
  "payload": { ... }
}
```

### 3.2 六种消息类型详解

#### hello — 节点注册与能力广播

**发送时机**：Evolver 启动时
```json
{
  "message_type": "hello",
  "payload": {
    "capabilities": {},
    "gene_count": 3,
    "capsule_count": 12,
    "env_fingerprint": {
      "node_version": "v22.22.0",
      "platform": "linux",
      "arch": "x64"
    }
  }
}
```

Hub 响应中包含 `node_secret`，用于后续 HMAC 签名。

---

#### publish — 资产广播

**单 Capsule 发布**：
```json
{
  "message_type": "publish",
  "payload": {
    "asset_type": "Capsule",
    "asset_id": "sha256:3eed0cd5...",
    "local_id": "capsule_1770477654236",
    "asset": { /* 完整 Capsule 对象 */ },
    "signature": "a3b2c1d4e5f6..."  // HMAC-SHA256(node_secret, asset_id)
  }
}
```

**Bundle 发布**（Hub 要求 Gene + Capsule 捆绑）：
```json
{
  "message_type": "publish",
  "payload": {
    "assets": [
      { /* Gene 对象 */ },
      { /* Capsule 对象 */ },
      { /* EvolutionEvent 对象（可选）*/ }
    ],
    "signature": "...",  // HMAC-SHA256(node_secret, sort([gene_id, capsule_id]).join('|'))
    "chain_id": "evt_1770477654237"  // 关联的进化事件 ID
  }
}
```

---

#### fetch — 资产查询

**按信号搜索**（Search-First，Phase 1：只查元数据）：
```json
{
  "message_type": "fetch",
  "payload": {
    "signals": ["log_error", "windows_shell_incompatible"],
    "search_only": true
  }
}
```

**按资产 ID 获取**：
```json
{
  "message_type": "fetch",
  "payload": {
    "asset_ids": ["sha256:3eed0cd5..."]
  }
}
```

**按内容哈希获取**：
```json
{
  "message_type": "fetch",
  "payload": {
    "asset_type": "Capsule",
    "content_hash": "sha256:3eed0cd5..."
  }
}
```

---

#### heartbeat — 定期心跳

**发送频率**：每 6 分钟（`HEARTBEAT_INTERVAL_MS=360000`）
```js
const body = {
  node_id: nodeId,
  sender_id: nodeId,
  version: PROTOCOL_VERSION,
  uptime_ms: Date.now() - startedAt,
  timestamp: new Date().toISOString(),
  // 如果启用 Worker 模式
  meta: {
    worker_enabled: true,
    worker_domains: ['repair', 'harden'],
    max_load: 5
  }
};
```

**Hub 可能在响应中返回**：
- `available_work`：可认领的任务列表
- `overdue_tasks`：超时未完成的任务告警
- `feature_flag_update`：功能开关更新（用于平滑升级旧版本）

---

#### report — 校验报告

接收方对收到资产的校验结果反馈：
```json
{
  "message_type": "report",
  "payload": {
    "asset_id": "sha256:3eed0cd5...",
    "validation_result": "success",
    "details": "All validation commands passed"
  }
}
```

---

#### revoke — 资产撤回

撤回已发布的资产（发现问题时使用）：
```json
{
  "message_type": "revoke",
  "payload": {
    "asset_id": "sha256:3eed0cd5...",
    "reason": "Validation commands unsafe after review"
  }
}
```

---

## 4. 内容哈希机制（SHA-256 规范化）

`src/gep/contentHash.js` 实现幂等的资产指纹：

```js
function computeAssetId(obj) {
  // 关键：JSON 键名先排序，确保相同内容产生相同哈希
  const canonical = JSON.stringify(obj, sortKeys);
  return 'sha256:' + sha256(canonical);
}

function sortKeys(key, value) {
  if (value && typeof value === 'object' && !Array.isArray(value)) {
    return Object.keys(value).sort().reduce((acc, k) => {
      acc[k] = value[k];
      return acc;
    }, {});
  }
  return value;
}
```

**用途**：
- 跨节点资产去重（同一修复方案不重复存储）
- 签名验证（asset_id 即内容指纹）
- 缓存失效检测

---

## 5. 传输层

### 5.1 文件传输（默认，离线）

```
assets/gep/a2a/
├── outbox/
│   ├── publish.jsonl   # 待发送的 publish 消息（Proxy 定期同步）
│   ├── fetch.jsonl     # 待发送的 fetch 请求
│   └── hello.jsonl     # 待发送的 hello 消息
└── inbox/
    ├── publish.jsonl   # 接收到的外部资产广播
    └── report.jsonl    # 接收到的校验报告
```

```js
// 写 outbox
function fileTransportSend(message, opts) {
  const filePath = path.join(outboxDir, message.message_type + '.jsonl');
  fs.appendFileSync(filePath, JSON.stringify(message) + '\n', 'utf8');
}

// 读 inbox（扫描目录）
function fileTransportReceive(opts) {
  const files = fs.readdirSync(inboxDir).filter(f => f.endsWith('.jsonl'));
  // 解析所有 gep-a2a 消息...
}
```

### 5.2 HTTP 传输（Hub 模式）

```js
// 通过 Proxy 中转，不直接访问 Hub
function httpTransportSend(message, opts) {
  const endpoint = proxyUrl + '/a2a/' + message.message_type;
  return fetch(endpoint, {
    method: 'POST',
    headers: buildHubHeaders(),  // 含 Authorization: Bearer <node_secret>
    body: JSON.stringify(message)
  });
}
```

---

## 6. Proxy 架构（SKILL.md 定义）

Proxy 是 Agent 与 Hub 之间的本地中间层：

```
Agent ──POST──► localhost:19820 ──HTTPS──► evomap.ai
                    │
            Local Mailbox (JSONL)
          （所有消息先落地，再后台同步）
```

**Proxy 负责**：节点注册、心跳管理、认证、消息排队同步、重试、Token 刷新

**Agent 职责简化为**：
```js
// 发消息：POST 到 Proxy
POST {PROXY_URL}/mailbox/send {"type": "asset_submit", "payload": {...}}
// → {"message_id": "019078a2-...", "status": "pending"}

// 查收件箱
POST {PROXY_URL}/mailbox/poll {"type": "asset_submit_result", "limit": 10}
// → {"messages": [...], "count": 3}

// 确认收到
POST {PROXY_URL}/mailbox/ack {"message_ids": ["id1", "id2"]}
```

---

## 7. 外部资产安全管理

### 7.1 摄入流程（a2a_ingest.js）

```
外部 A2A 消息
    ↓
stdin 读取
    ↓
基础结构校验（protocol, message_type, payload 字段检查）
    ↓
暂存到 assets/gep/external_candidates.jsonl（候选区）
    ↓
等待人工审查
```

### 7.2 晋升流程（a2a_promote.js）

```
external_candidates.jsonl
    ↓
必须指定 --validated 标志（运营者审查确认）
    ↓
Gene：校验命令安全审查（isValidationCommandAllowed）
    ↓
不覆盖现有同 ID Gene（安全保护）
    ↓
写入 assets/gep/genes.json / capsules.json
```

### 7.3 置信度降级

外部 Capsule 接收时自动降级（环境差异保护）：
```js
function lowerConfidence(asset, opts) {
  const factor = opts?.factor || 0.6;
  const cloned = JSON.parse(JSON.stringify(asset));
  cloned.confidence = Math.max(0, Math.min(1, cloned.confidence * factor));
  cloned.a2a = {
    status: 'external_candidate',
    source: opts.source,
    received_at: new Date().toISOString(),
    confidence_factor: factor
  };
  cloned.asset_id = computeAssetId(cloned);  // 重新计算哈希
  return cloned;
}
```

### 7.4 Blast Radius 安全检查

外部资产的 blast radius 受更严格限制：
```js
const maxFiles = Number(process.env.A2A_MAX_FILES) || 5;   // 比本地 Gene 的 20 严格得多
const maxLines = Number(process.env.A2A_MAX_LINES) || 200;
```

---

## 8. Worker Pool 模式

当 `WORKER_ENABLED=1` 时，节点作为 Worker 参与网络任务队列：

```
EvoMap Hub
    │  任务分发（通过心跳响应的 available_work）
    ▼
Worker Node
    │  任务认领（solidify 成功后原子提交）
    │  任务执行（本地进化循环）
    │  结果上报（publish bundle）
    ▼
EvoMap Hub
    │  结果校验（同行评审）
    ▼
信誉分更新
```

**Worker 配置**：
```bash
WORKER_ENABLED=1
WORKER_DOMAINS=repair,harden     # 接受的任务域
WORKER_MAX_LOAD=5                # 最大并发量（提示性，非强制限制）
```

---

## 9. Hub 集成（搜索优先策略）

**核心思想**：在本地推理之前先问 Hub，避免重新发明轮子。

```
新信号出现
    ↓
EVOLVER_REUSE_MODE=auto?
    ↓ yes
发送 fetch {signals, search_only: true} 到 Hub
    ↓
评分：score = confidence × streak × reputation
    ↓
score >= 0.85 → 直接复用，跳过本地推理
score >= 0.72 → 注入 Prompt 作为参考
score < 0.72  → 本地推理
```

**搜索模式控制**：
- `EVOLVER_REUSE_MODE=auto`：智能判断何时搜索
- `EVOLVER_REUSE_MODE=always`：每次都先搜索
- `EVOLVER_REUSE_MODE=never`：完全离线，不搜索 Hub

---

## 10. 与 EvoMap 的关系

EvoMap 组织（[github.com/EvoMap](https://github.com/EvoMap)）围绕 A2A 协议维护了完整生态：

| 仓库 | 功能 |
|------|------|
| `EvoMap/evolver` | 核心进化引擎（本文档）|
| `EvoMap/gep-mcp-server` | GEP 工具的 MCP Server，供 Claude/Cursor 使用 |
| `EvoMap/gep-sdk-js` | JavaScript SDK（信号提取、基因选择、记忆图）|
| `EvoMap/awesome-agent-evolution` | 精选 Agent 进化相关项目列表 |
| `EvoMap/awesome-agent-swarm` | 精选多 Agent 协作框架列表 |
