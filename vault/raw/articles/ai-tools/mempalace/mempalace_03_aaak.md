# MemPalace 深度解析（三）：AAAK 方言——为 AI 设计的压缩语言

> 不是为了人类可读，而是为了让 AI 在 120 个 token 内加载数月的上下文

---

## 0. 一个反直觉的问题

如果有人告诉你："我设计了一种新语言，专门给 AI 读，人类看起来会觉得很奇怪"——你的第一反应可能是：为什么不直接用 JSON？或者 XML？

AAAK（发音待定，"a whole story of its own"——官方如此表述）的答案是：**因为 AI 读的是 token，不是字节，而且 AI 天然理解英语语义——我们要利用这一点做有损压缩之外的无损压缩。**

---

## 1. AAAK 试图解决的问题

### 1.1 Closet 里要装什么？

回顾第二篇的架构：每个 Room 有一个 Closet，存放压缩摘要。AI 每次启动时，先读 Closet，判断各 Room 里有什么，再决定去哪个 Drawer 取原文。

Closet 的使命：**用最少的 token，传递最多的导航信息。**

如果 Closet 用普通英文写，信息密度不够高；如果用 JSON，结构性 token（括号、引号、冒号）会浪费大量空间；如果用二进制编码，AI 根本看不懂。

AAAK 走了第四条路：**保留英语的语义可理解性，但激进地删除冗余**。

### 1.2 token 经济学

普通英文的 token 效率：
```
"The user decided to use PostgreSQL because the team 
 had more experience with it than MySQL." 
→ 约 20 tokens，传递 1 个事实
```

AAAK 目标：
```
usr>psql[exp>mysql]
→ 约 5 tokens，传递同样的 1 个事实
```

**压缩比约 4:1（单条）。在大规模重复实体场景下，可以达到 30:1。**

---

## 2. AAAK 的设计原则

AAAK 不是一套完整的语法规范（至少在 v3.0.0 中还没有），但从 README 和代码中可以提炼出它的核心规则：

### 原则一：去掉所有助词、冠词、系动词

| 原文 | AAAK |
|------|------|
| "The user is using" | `usr>use` |
| "decided to" | `>` |
| "because of" | `[` |
| "in the context of" | `@` |
| "related to" | `~` |

### 原则二：用符号替代高频短语

| 符号 | 含义 |
|------|------|
| `>` | 使用/决定/转向 |
| `[reason]` | 原因/因为 |
| `@` | 上下文/场景 |
| `~` | 相关/关联 |
| `+` | 加上/以及 |
| `!` | 重要/警告 |
| `?` | 待确认/问题 |

### 原则三：实体缩写（重复实体的核心收益）

当某个实体（人名、项目名、技术名）在文档中反复出现时，AAAK 会在首次出现时建立缩写，后续全部使用缩写：

```
alice=A, bob=B, my_app=MAP, postgresql=PG, graphql=GQL
```

首次建立缩写的 token 开销是一次性的，之后每次使用都是极低代价。**这正是为什么 AAAK 在"重复实体的大规模场景"中才真正发挥 30:1 压缩优势**——单条短文本里实体重复次数少，收益有限。

### 原则四：保持 AI 可理解性

AAAK 的关键约束：**AI 不需要特殊解码器就能理解。**

因为 AAAK 本质上是"被激进压缩的英语"。大语言模型见过大量的速记、代码注释、学术缩写，面对 AAAK 这类结构化简写时，理解成本很低。

每次 AI Agent 启动时，MemPalace 会在 System Prompt 里注入一段 AAAK 字典说明，Agent 几秒内就掌握了当前会话的缩写体系。

---

## 3. AAAK 的实际形态：一个示例

原始对话记录（普通英文，约 180 tokens）：

```
Alice and Bob had a discussion about the authentication system 
for my_app. Alice preferred using JWT tokens because they are 
stateless and easier to scale horizontally. Bob raised concerns 
about token revocation, pointing out that we would need a 
blacklist. They decided to use JWT with Redis for the blacklist,
and Alice would implement it by the end of the sprint.
```

AAAK Closet 版本（约 30 tokens）：

```
A+B@MAP.auth: jwt>stateless+hscale[A]; revoke?+blacklist[B]
>jwt+redis_bl; A impl<sprint_end
```

AI 读到这段，能够理解：
- Alice 和 Bob 在 my_app 的 auth 房间讨论过 JWT
- Alice 主张 JWT（无状态、水平扩展）
- Bob 担心 revocation，提出黑名单
- 决策结果：JWT + Redis blacklist
- 执行者：Alice，截止：sprint 结束

**压缩比：180 → 30 tokens，约 6:1。实体大量重复的场景下可到 30:1。**

---

## 4. AAAK 的局限性（官方已承认）

MemPalace 在 README 中坦承了 AAAK 的一个重要局限：

> "AAAK token example was incorrect. We used a rough heuristic (len(text)//3) for token counts instead of an actual tokenizer. Real counts via OpenAI's tokenizer: the English example is 66 tokens, the AAAK example is 73. **AAAK does not save tokens at small scales** — it's designed for repeated entities at scale."

这是一个值得注意的诚实声明。**在短文本、低实体重复的场景里，AAAK 可能不省 token，甚至更多**。AAAK 的收益曲线是：

```
实体重复次数
     ↑
30:1 |                                    ●
     |                               ●
10:1 |                          ●
     |                     ●
 5:1 |               ●
     |          ●
 1:1 |●────────────────────────────────→ 
     0    5    10   20   50  100  200   重复次数
```

**AAAK 是为长期、大规模的实体积累而设计的，而非单次短对话场景。**

---

## 5. AAAK 在系统中的位置

```
挖掘阶段（mine）：
  原始内容 → 切块 → Drawer（存原文）
                  → 生成 AAAK 摘要 → Closet（存压缩版）

检索阶段（Agent 启动）：
  1. 读所有 Closet → 注入 System Prompt（极小 token）
  2. AI 理解导航地图
  3. 需要详情 → 调用 MCP 工具 → 读 Drawer（原文）
```

AAAK 只在 Closet 中使用，**Drawer 永远存原文，保证零信息损耗**。AAAK 是"导航地图"，不是"存储格式"。

---

## 6. 未来计划

官方 README 提到，下一个版本计划：

> "We'll add AAAK directly to the closets, which will be a real game changer — the amount of info in the closets will be much bigger, but it will take up far less space and far less reading time for your agent."

v3.0.0 中的 Closet 摘要还不是完整的 AAAK（是更接近人类可读的摘要）。真正全量 AAAK 化的 Closet 预计在下一版本实现，届时 30:1 压缩的承诺才会在实际产品中完全落地。

---

## 7. AAAK 的启示

AAAK 的设计思路，对 AI 工程师有一个重要的提示：

**为 AI 设计的数据格式，不必遵循为人类设计的可读性标准。**

- JSON 的括号、引号是给解析器看的
- Markdown 的 `**bold**` 是给渲染器看的
- AAAK 的目标受众是大语言模型的 attention 机制

当你的 System Prompt 或 RAG 上下文需要装入大量结构化信息时，AAAK 提供了一种思路：**保留语义，删除冗余，利用 LLM 对自然语言缩写的强泛化能力做无损压缩**。

---

*下一篇：[MemPalace 深度解析（四）：4 级渐进式加载系统——Token 预算管理的工程实现]*
