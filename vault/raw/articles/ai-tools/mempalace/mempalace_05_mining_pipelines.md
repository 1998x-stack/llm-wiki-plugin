# MemPalace 深度解析（五）：三种挖掘管道

> Projects · Convos · General——把你的代码库、对话记录、任意文件转化为可检索的记忆

---

## 0. "挖掘"是什么？

MemPalace 的核心工作流分两个阶段：

```
Phase 1: Mine（挖掘）
  你的文件/对话 → 切块 → 分类 → 存入宫殿

Phase 2: Search（检索）  
  问题 → 定位 Wing/Room → 语义搜索 → 返回相关 Drawer
```

"挖掘"不是一次性的，你可以随时重新挖掘新内容，MemPalace 会通过 MD5 去重，只存储新增部分。

MemPalace 提供三种挖掘模式，分别面向不同的数据源：

| 模式 | 命令 | 数据源 |
|------|------|--------|
| `projects` | `mempalace mine ~/myapp` | 代码库、文档、笔记 |
| `convos` | `mempalace mine ~/chats/ --mode convos` | AI 对话导出文件 |
| `general` | `mempalace mine ~/docs/ --mode convos --extract general` | 任意文本，自动分类 |

---

## 1. Projects 模式：挖掘代码库和文档

### 1.1 触发条件

```bash
mempalace mine ~/projects/myapp
# 等同于 --mode projects（默认模式）
```

### 1.2 文件遍历

挖掘器会递归遍历目录，跳过以下内容：

```python
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 
             'dist', 'build', '.next', 'vendor'}
SKIP_EXTENSIONS = {'.pyc', '.exe', '.bin', '.jpg', '.png', ...}

SUPPORTED_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx',   # 代码
    '.md', '.txt', '.rst',                  # 文档
    '.json', '.yaml', '.yml', '.toml',      # 配置
    '.html', '.css', '.sql',                # 其他
    # 共 20 种扩展名
}
```

### 1.3 Room 检测（4 级级联）

```
优先级 1：路径匹配
  /auth/login.py → Room: auth
  /billing/stripe.py → Room: billing

优先级 2：文件名匹配
  deploy.sh → Room: deploy
  database.py → Room: database

优先级 3：内容关键词评分
  文件包含大量 "SELECT", "INSERT", "JOIN" → Room: database
  文件包含大量 "docker", "kubectl", "pod" → Room: deploy

优先级 4：兜底
  无匹配 → Room: general
```

内容关键词映射表约 60 条规则，涵盖常见的软件工程领域分类。

### 1.4 切块策略

```python
CHUNK_SIZE = 800        # 字符数
CHUNK_OVERLAP = 100     # 重叠字符数

# 优先在段落边界（\n\n）切块
# 如果段落太长，在句子边界（.  ?  !）切
# 最后兜底：硬截断到 800 字符
```

### 1.5 去重机制

```python
import hashlib

def should_store(content: str, existing_hashes: set) -> bool:
    h = hashlib.md5(content.encode()).hexdigest()
    if h in existing_hashes:
        return False  # 已存在，跳过
    existing_hashes.add(h)
    return True
```

每次挖掘前，先从 ChromaDB 加载所有现有 MD5，新内容只存不重复的块。

### 1.6 交互式确认

对于关键的 Room 分配决策，挖掘器支持交互模式：

```
文件: /src/payment/checkout.js
检测到 Room: billing
确认? [Y/n/edit] → 用户输入 edit → 改为 payment
```

用户的修改会保存到 `mempalace.yaml`，下次挖掘时记住该偏好。

---

## 2. Convos 模式：挖掘 AI 对话记录

这是 MemPalace 最有特色的模式——把你所有与 AI 的对话变成可检索的记忆。

### 2.1 支持的格式

MemPalace 内置了多个主流平台的对话导出格式适配器：

| 平台 | 导出格式 | 适配器 |
|------|---------|--------|
| Claude Code | `.jsonl` | `claude_code_adapter` |
| Claude.ai | `.json` | `claude_web_adapter` |
| ChatGPT | `conversations.json` | `chatgpt_adapter` |
| Slack | 频道导出 `.json` | `slack_adapter` |

### 2.2 统一格式化

所有适配器最终输出统一的中间格式：

```
> [用户消息]
[AI 回复]

> [用户消息]
[AI 回复]
```

`>` 标记代表用户输入，这个约定贯穿整个 convo_miner 的处理流程。

### 2.3 对话切块：Exchange 模式

Convos 模式的切块逻辑与 Projects 模式不同：

**Exchange 模式（优先）**：
每个"用户提问 + AI 回答"组合作为一个独立的 chunk。

```python
# 每个 exchange 是一个完整的问答对
chunks = split_by_exchanges(text)   # 按 ">" 分割
```

这确保了**上下文的语义完整性**——一个 chunk 里永远包含完整的一问一答，而不是把问题和答案拆开。

**兜底模式**：
如果 `>` 标记少于 3 个（不像对话格式），退回段落切块模式。

### 2.4 Room 检测（对话内容）

对话内容的 Room 检测与代码文件不同，用 5 类关键词评分：

```python
CONVO_ROOMS = {
    "technical": [
        "code", "python", "javascript", "api", "bug", "function", 
        "class", "module", "database", "query", "server", "deploy", "git"
    ],  # 13 个
    "architecture": [
        "system", "design", "pattern", "structure", "microservice",
        "component", "service", "interface", "abstraction", "layer"
    ],  # 10 个
    "planning": [
        "roadmap", "sprint", "milestone", "deadline", "priority",
        "goal", "timeline", "schedule", "release", "backlog"
    ],  # 10 个
    "decisions": [
        "decided", "chose", "because", "tradeoff", "alternative",
        "reason", "considering", "instead", "approach", "solution"
    ],  # 10 个
    "problems": [
        "error", "issue", "broken", "failed", "bug", "slow",
        "crash", "incorrect", "wrong", "not working"
    ],  # 10 个
}
```

只扫描每个 chunk 的前 2000 字符，按命中关键词数量排名，最高分 Room 胜出。

---

## 3. General 模式：通用文本自动分类提取

General 模式是最"智能"的挖掘模式，但"智能"来自规则，而非 LLM。

```bash
mempalace mine ~/docs/ --mode convos --extract general
```

### 3.1 5 种记忆类型的正则提取

General 模式用大量正则模式，从任意文本中提取 5 类记忆：

**decisions（决策）—— 20 个模式**：

```python
DECISION_PATTERNS = [
    r"let's use\b",
    r"we('ve)? decided (to|that)",
    r"going with\b",
    r"we('ll)? go with\b",
    r"chose to\b",
    r"because\b",
    r"the reason (is|was)\b",
    r"therefore\b",
    r"as a result\b",
    r"so we('re)?\b",
    # ... 还有 10 个
]
```

**preferences（偏好）—— 16 个模式**：

```python
PREFERENCE_PATTERNS = [
    r"prefer(s)?\b",
    r"(I|we) like\b",
    r"always (use|do|avoid)\b",
    r"never (use|do)\b",
    r"favorite\b",
    r"style is\b",
    # ...
]
```

**milestones（里程碑）—— 33 个模式**：

```python
MILESTONE_PATTERNS = [
    r"(just )?(finished|completed|shipped|released|launched)\b",
    r"(we('ve)?|I('ve)?) (done|built|created|implemented)\b",
    r"v\d+\.\d+",         # 版本号
    r"\bGA\b",            # General Availability
    r"(went|going) live\b",
    # ... 还有 28 个
]
```

**problems（问题）和 emotional_context（情绪上下文）** 各有类似数量的模式。

### 3.2 提取结果写入对应 Hall

提取后，每条内容根据分类写入对应的 Hall：

```
decisions → Hall: decisions
preferences → Hall: preferences  
milestones → Hall: events
problems → Hall: discoveries（记录发现的问题）
emotional_context → Hall: facts（情绪状态作为上下文事实）
```

### 3.3 General 模式的典型用途

```bash
# 挖掘个人日记
mempalace mine ~/journal/ --mode convos --extract general

# 挖掘项目会议记录
mempalace mine ~/meetings/ --mode convos --extract general

# 挖掘读书笔记
mempalace mine ~/notes/ --mode convos --extract general
```

---

## 4. 挖掘管道全流程对比

```
┌─────────────────────────────────────────────────────────────┐
│                    Projects 模式                             │
│                                                             │
│  目录树遍历 → 过滤扩展名 → 读取文件                           │
│      ↓                                                      │
│  Room 检测（路径→文件名→内容评分→general）                    │
│      ↓                                                      │
│  字符切块（800c + 100 overlap，段落优先）                     │
│      ↓                                                      │
│  MD5 去重 → ChromaDB 写入                                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Convos 模式                               │
│                                                             │
│  多平台导出 → 统一格式（> 标记）                               │
│      ↓                                                      │
│  Room 检测（5 类关键词评分，扫前 2000 字符）                   │
│      ↓                                                      │
│  Exchange 切块（问答对为单元）/ 段落兜底                      │
│      ↓                                                      │
│  MD5 去重 → ChromaDB 写入                                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    General 模式（在 Convos 基础上）           │
│                                                             │
│  正则提取（5 类记忆类型，合计 ~100 个模式）                    │
│      ↓                                                      │
│  按类型映射到对应 Hall                                        │
│      ↓                                                      │
│  MD5 去重 → ChromaDB 写入                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. 工程亮点

### 零 LLM 调用

整个挖掘管道，从文件读取到 ChromaDB 写入，**没有任何 LLM API 调用**。所有决策（Room 分类、内容分类、切块）都是确定性的规则运算。

这意味着：
- 挖掘速度不受 API 限速影响
- 挖掘成本为零（只需本地算力）
- 挖掘结果可复现

### 多次增量挖掘

MemPalace 支持随时追加挖掘，MD5 去重保证幂等性：

```bash
# 今天挖掘新的对话
mempalace mine ~/chats/2026-04-08.json --mode convos

# 明天再挖掘
mempalace mine ~/chats/2026-04-09.json --mode convos

# 不会有重复内容
```

### 可恢复的交互式配置

所有用户的 Room 分配决策都保存在 `mempalace.yaml`，格式简洁：

```yaml
room_overrides:
  "src/payment/checkout.js": payment
  "src/auth/session.py": auth
wing_aliases:
  "my_app": "MAP"
  "alice": "A"
```

---

## 6. 使用建议

对于 AI Agent 工程师，推荐的工作流：

1. **项目初始化**：对代码库跑一次 `projects` 模式
2. **对话归档**：每周导出一次 AI 对话，跑 `convos` 模式
3. **决策记录**：重要文档（需求文档、设计文档）用 `general` 模式提取决策和里程碑
4. **增量同步**：设置 cron job，自动挖掘新文件

```bash
# 每日自动挖掘（crontab 示例）
0 9 * * * mempalace mine ~/chats/ --mode convos
0 9 * * * mempalace mine ~/projects/myapp/
```

---

*下一篇：[MemPalace 深度解析（六）：MCP 工具集成——19 个工具如何赋能 AI Agent]*
