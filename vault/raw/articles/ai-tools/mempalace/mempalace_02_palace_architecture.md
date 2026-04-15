# MemPalace 深度解析（二）：记忆宫殿架构

> **Wing · Room · Hall · Drawer · Tunnel · Closet**——六层结构，让 AI 的记忆从"搜索"变成"导航"

---

## 0. 古希腊修辞师的秘密

公元前 477 年，诗人西蒙尼德斯正在赴宴，突然被人叫出去。就在他踏出门的那一刻，宴会厅轰然倒塌，所有宾客罹难。

事后，当局要求他辨认每一具遗体。西蒙尼德斯闭上眼睛，回想起自己在宴会厅里看到的每一张脸——他们坐在哪里、靠近哪根柱子、身边有谁。凭借这种空间记忆，他准确辨认了所有人。

这就是**记忆宫殿（Method of Loci）**技术的起源。

两千五百年后，MemPalace 把这个技术移植进了 AI 记忆系统的工程架构里。

---

## 1. 为什么结构能带来 34% 的提升？

在讲六层结构之前，先理解这个关键数字：

**从扁平向量搜索（60.9%）到宫殿结构检索（94.8%），提升了 34 个百分点。**

原因在于"检索范围收窄"：

```
传统 RAG 检索：
  问题 → 全库语义搜索 → 返回 Top-K

MemPalace 检索：
  问题 → 识别 Wing（缩小到某人/某项目）
       → 识别 Room（缩小到某主题）
       → 识别 Hall（缩小到某类型）
       → 在 Drawer 中精确搜索
```

每一级缩窄，都在剪枝不相关的噪声。最终在 Drawer 里搜索的候选集，已经是高度相关的子集。这比在数百万条记录里做全局语义搜索，精准得多。

---

## 2. 六层结构详解

### 2.1 Wing（翼）——最顶层的域

**Wing 是人、项目、或宏观话题。**

```
palace/
├── my_app/          ← 项目 Wing
├── alice/           ← 人物 Wing  
├── emotions/        ← 默认话题 Wing
├── technical/       ← 默认话题 Wing
├── identity/        ← 默认话题 Wing
├── family/          ← 默认话题 Wing
└── creative/        ← 默认话题 Wing
```

MemPalace 在安装时会自动为你检测 Wing，你也可以通过 `mempalace.yaml` 手动配置。

**设计意图**：你和 Alice 的对话、你和 Bob 的对话、你的 myapp 项目，三者永远不会混淆。Wing 是最强的隔离边界。

---

### 2.2 Room（房间）——Wing 内的主题分区

每个 Wing 内部被分割成多个 Room，代表不同的主题领域。

**对于项目 Wing**，Room 映射到代码结构：

```
my_app Wing
├── auth/
├── billing/
├── deployment/
├── api/
└── general/
```

**对于对话 Wing**，Room 由关键词评分决定（完全无 LLM 调用）：

```python
ROOM_KEYWORDS = {
    "technical":    ["code", "python", "api", "bug", "function", "class", 
                     "module", "database", "query", "server", ...],  # 13个关键词
    "architecture": ["system", "design", "pattern", "structure", 
                     "microservice", "component", ...],               # 10个关键词
    "planning":     ["roadmap", "sprint", "milestone", "deadline", 
                     "priority", "goal", ...],                        # 10个关键词
    "decisions":    ["decided", "chose", "because", "tradeoff",
                     "alternative", "reason", ...],                   # 10个关键词
    "problems":     ["error", "issue", "broken", "failed", "bug",
                     "slow", "crash", ...],                           # 10个关键词
}
```

评分逻辑：对每条内容的前 2000 个字符计算各分类命中关键词数量，最高分的分类成为 Room。没有任何匹配则归入 `general`。

**检测优先级（4级级联）**：
```
1. 文件夹路径（/auth/ → auth room）
2. 文件名（auth.py → auth room）
3. 内容关键词评分
4. 默认 → "general"
```

---

### 2.3 Hall（大厅）——记忆类型的分类

每个 Room 内部有 **5 个标准 Hall**，代表信息的性质：

| Hall | 含义 | 示例 |
|------|------|------|
| `facts` | 客观事实 | "项目使用 PostgreSQL 14" |
| `events` | 发生过的事件 | "2025-11 完成了身份验证模块重构" |
| `discoveries` | 发现与洞见 | "DataLoader 可以解决 N+1 问题" |
| `preferences` | 偏好与风格 | "团队偏好函数式组件而非类组件" |
| `advice` | 建议与经验 | "部署前务必跑完 E2E 测试" |

Hall 的作用是在检索时提供**类型过滤**能力：如果你问"有哪些关于部署的建议"，系统可以直接聚焦到 `advice` Hall，而不是全量搜索。

---

### 2.4 Drawer（抽屉）——原始内容的最终存储单元

**Drawer 是最终存储单元，存的是原始文本，一字不改。**

切块参数：
- **块大小**：800 字符
- **重叠**：100 字符（防止切块边界截断关键信息）
- **切块策略**：优先在段落边界切，保证语义完整性

每个 Drawer 有完整的元数据：

```json
{
  "wing": "my_app",
  "room": "auth",
  "hall": "decisions",
  "source_file": "~/chats/2025-11-12.json",
  "chunk_index": 3,
  "timestamp": "2025-11-12T14:23:00",
  "added_by": "convo_miner",
  "content": "...原始文本内容..."
}
```

**去重机制**：通过 MD5 hash 防止重复存储相同内容。

---

### 2.5 Tunnel（隧道）——跨域连接

**Tunnel 是 MemPalace 最有创意的设计之一。**

当同一个 Room 名称（如 `auth`）出现在两个或更多 Wing 中时，系统自动在它们之间建立 Tunnel：

```
my_app Wing
└── auth Room ←───────── Tunnel ─────────→ client_portal Wing
                                                  └── auth Room
```

这意味着：当你在查询 `my_app` 的认证问题时，系统会自动发现"哦，`client_portal` 项目里也有关于 auth 的讨论"，并把它一并带出来。

**这解决了传统 RAG 无法跨域发现关联的问题——不需要人为建立连接，结构自然涌现。**

---

### 2.6 Closet（壁橱）——AAAK 压缩摘要

每个 Room 还有一个 Closet，存放用 **AAAK 方言**（见第三篇）压缩过的摘要。

Closet 的作用是**快速导航**：AI 先读 Closet（极小的 token 消耗），判断这个 Room 里大致有什么，再决定是否深入 Drawer 取原文。

```
Room
├── Closet（AAAK 摘要，~120 tokens 可加载数月上下文）
└── Drawers（原始文本，按需按需取）
```

这就是 MemPalace 的 4 级渐进式加载系统的核心——**先地图，再导航，再详情**。

---

## 3. 整体结构图

```
Palace（整个记忆系统）
│
├── Wing: my_app（项目）
│   ├── Room: auth
│   │   ├── Hall: facts
│   │   ├── Hall: decisions
│   │   ├── Closet（AAAK 摘要）
│   │   └── Drawers（原始块 × N）
│   ├── Room: billing
│   │   └── ...
│   └── Tunnel ──────────────────────────┐
│                                         │
├── Wing: client_portal（另一个项目）      │
│   ├── Room: auth  ←────────────────────┘
│   │   └── ...
│   └── ...
│
└── Wing: alice（人物）
    ├── Room: technical
    ├── Room: planning
    └── ...
```

---

## 4. 工程实现要点

### Room 检测器的两个实现

**本地文件**（`room_detector_local.py`）：
- ~60 个关键词到 Room 的映射规则
- 路径优先 → 文件名次之 → 内容评分兜底
- 支持交互式确认，用户可以修改分配，保存到 `mempalace.yaml`

**对话内容**（`convo_miner.py`）：
- 5 大分类，合计 ~56 个关键词
- 只扫描前 2000 字符（速度优先）
- 无 LLM 调用，纯关键词统计

### Tunnel 的生成时机

Tunnel 在 `mempalace status` 命令执行时自动计算，遍历所有 Wing 的 Room 名称，建立重名 Room 之间的连接索引。这是一次性的静态计算，不需要实时维护。

---

## 5. 设计哲学的统一性

六层结构表面上是复杂的，但底层逻辑是一致的：

1. **人类记忆是空间性的**：我们通过位置找到信息，而不是通过内容特征搜索
2. **层级收窄优于全局搜索**：每一层都在剪枝噪声
3. **结构是免费的精度提升**：34% 的提升没有用任何额外的模型调用，纯靠组织方式

这正是 MemPalace 名字的含义——**不是在数据库里搜索，而是在宫殿里导航**。

---

*下一篇：[MemPalace 深度解析（三）：AAAK 方言——30× 压缩，零信息损耗]*
