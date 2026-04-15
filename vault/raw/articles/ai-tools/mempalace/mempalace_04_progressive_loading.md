# MemPalace 深度解析（四）：4 级渐进式加载系统

> Token 预算管理的工程实现——从全局地图到精确原文，按需按量加载

---

## 0. 问题：你不可能把所有记忆都塞进上下文

假设你积累了两年的 AI 对话记录，涵盖数十个项目和数百次技术决策。如果把所有这些内容全部塞进每次 AI 会话的上下文窗口：

- GPT-4o 的 128k token 上限会立刻爆满
- 即使上下文够长，无关信息会稀释 AI 的注意力
- 每次调用的成本会变得无法接受

这是所有长期记忆系统都必须面对的核心工程问题：**如何在有限的 Token 预算内，精准地注入最相关的记忆？**

MemPalace 的答案是 **4 级渐进式加载（Progressive Loading）**。

---

## 1. 四个级别的定义

```
Level 1: Palace Overview（宫殿鸟瞰）
         ↓ 需要更多？
Level 2: Wing Summary（翼摘要）
         ↓ 需要更多？
Level 3: Room + Closet（房间 + AAAK 导航）
         ↓ 需要更多？
Level 4: Drawer Content（抽屉原文）
```

每一级都比上一级消耗更多 token，但提供更精细的信息。AI Agent 从第一级开始，根据任务需要，逐级深入，直到找到所需的信息为止。

---

## 2. Level 1：Palace Overview（宫殿鸟瞰）

**消耗 token：极低（约 50~100 tokens）**

Level 1 只告诉 AI：**你的记忆宫殿里有哪些翼（Wing），每个翼大概有什么。**

输出形态（示意）：

```
PALACE STATUS:
Wings: my_app(auth,billing,deploy,api), 
       alice(technical,planning,personal),
       client_portal(auth,frontend,infra),
       emotions(reflections,goals)
Tunnels: my_app.auth ↔ client_portal.auth
Last updated: 2026-04-01
```

这相当于给 AI 一张建筑平面图：有哪几栋楼，每栋楼大概是什么用途。

**典型触发时机**：每次 AI Agent 启动时，`mempalace_status` 工具自动注入这段内容。AI 由此知道自己"拥有"哪些记忆，可以在回答问题前决定是否需要深入查询。

---

## 3. Level 2：Wing Summary（翼摘要）

**消耗 token：低（约 100~200 tokens/翼）**

Level 2 展开某一个 Wing 的全貌：这个翼里有哪些 Room、每个 Room 的最近活动时间、大致内容方向。

```
WING: my_app
Rooms:
  auth (last: 2026-03-15, 23 drawers): JWT, OAuth2, Redis blacklist
  billing (last: 2026-02-28, 18 drawers): Stripe, webhooks, refund logic
  deploy (last: 2026-03-20, 31 drawers): K8s, CI/CD, rollback procedures
  api (last: 2026-03-18, 27 drawers): REST design, rate limiting, versioning
```

**典型触发时机**：当用户问题涉及特定项目（"my_app 的部署流程是什么"），AI 先展开相应翼的摘要，确认信息存在，再决定是否进入具体 Room。

---

## 4. Level 3：Room + Closet（房间 + AAAK 导航）

**消耗 token：中等（约 120~300 tokens/房间）**

Level 3 是 MemPalace 最核心的设计层。它加载：
1. 该 Room 的所有 Hall 分类信息
2. Closet 中的 AAAK 压缩摘要

```
ROOM: my_app.deploy

HALLS:
  facts: k8s v1.28, 3 node cluster, blue-green deploy
  events: 2026-03-20 prod rollback after v2.3.1 OOM
  discoveries: health check timeout=30s prevents false rollback
  preferences: always tag images with git SHA, never :latest
  advice: !run db migrations separately before pod update

CLOSET (AAAK):
  deploy@MAP: k8s+3n, bg_deploy; 
  evt:2026-03-20>rollback[v2.3.1,OOM]
  disc:hc_to=30s[anti-false-rb]; 
  pref:img_tag=sha,!latest
  adv:!db_mig>pod_update
```

**这是"按图索骥"的关键层**：AI 读完 Closet 之后，已经知道这个 Room 里有什么决策、什么事件、什么建议。它可以直接回答用户的问题，也可以判断"我需要第 3 个 drawer 的原文来获取更多细节"。

**注意**：Closet 的 AAAK 内容压缩了整个 Room 的导航信息，但**不是原文**。如果用户需要完整的推理链，必须进入 Level 4。

---

## 5. Level 4：Drawer Content（抽屉原文）

**消耗 token：高（约 300~800 tokens/抽屉）**

Level 4 加载特定 Drawer 的完整原始内容，一字不改。

```
DRAWER: my_app.deploy.events.drawer_047
Source: ~/chats/2026-03-20_production_incident.json
Chunk: 3/7
Timestamp: 2026-03-20 14:23:00

[用户]: 刚才 v2.3.1 触发了 OOM，整个 pod 组重启了。我们要不要回滚？
[AI]: 建议立即回滚到 v2.3.0。OOM 的根因需要分析，但不应该在生产环境上
      等待。回滚步骤：
      1. kubectl rollout undo deployment/my-app
      2. 确认 v2.3.0 的 pod 健康后再检查日志
      3. 在 staging 用 v2.3.1 复现 OOM...
[用户]: 好，已经回滚了。发现是新版本的图片处理器在高并发下内存泄漏...
```

**这才是"不丢失推理链"的根本保障**——你能看到完整的对话，包括当时的决策背景、备选方案、最终选择的原因。

---

## 6. 渐进式加载的 Token 预算示意

```
一次典型的 Agent 对话：

 启动时：
  └─ Level 1: Palace Overview ........... ~80 tokens（自动注入）

 问题识别阶段：
  └─ Level 2: my_app Wing Summary ........ ~150 tokens

 导航阶段：
  └─ Level 3: deploy Room + Closet ........ ~250 tokens

 精确检索阶段：
  └─ Level 4: Drawer #047 (原文) ......... ~500 tokens

 合计：约 980 tokens（远低于将所有记忆塞入上下文）

 对比：直接全量注入 my_app 所有内容
  → 99 drawers × 400 tokens avg ≈ 39,600 tokens
```

**渐进式加载节省了 ~97.5% 的 Token 消耗，同时保持了精确检索的能力。**

---

## 7. "Know Before Speaking" 协议

MemPalace 在 `mempalace_status` 工具的每次响应中，都会注入一段软约束指令：

```
BEFORE RESPONDING about any person, project, or past event:
call mempalace_kg_query or mempalace_search FIRST.
```

这是一个行为约束协议，确保 AI 不会在没有查询记忆的情况下凭训练数据回答问题。虽然这依赖 LLM 遵循指令，但实践中大模型对 System Prompt 中的此类强制协议遵从度很高。

这个设计确保了渐进式加载不仅是一个"有了就用"的可选功能，而是 Agent 工作流中的强制步骤。

---

## 8. 知识图谱层（Temporal KG）

除了四级加载，MemPalace 还维护了一个**时序知识图谱（Temporal Knowledge Graph）**，专门处理"会随时间变化的事实"：

```python
# 示例：某个事实在不同时间点的状态
{
  "entity": "my_app.deployment_strategy",
  "timeline": [
    {"date": "2025-06", "value": "蓝绿部署", "source": "drawer_012"},
    {"date": "2025-11", "value": "金丝雀发布", "source": "drawer_067"},
    {"date": "2026-02", "value": "回归蓝绿部署", "source": "drawer_089"}
  ]
}
```

当 AI 问"我们现在用什么部署策略"，时序图谱会自动返回最新状态，而不是混淆不同时间点的答案。传统 RAG 无法区分这种时序关系，MemPalace 通过 KG 层解决了这个问题。

---

## 9. 设计总结

| 级别 | 内容 | Token 消耗 | 典型场景 |
|------|------|-----------|---------|
| L1 Palace | 所有翼名 + Tunnel | ~80 | 每次启动自动注入 |
| L2 Wing | 翼内 Room 列表 + 时间 | ~150/翼 | 识别问题涉及哪个项目 |
| L3 Room+Closet | Hall 分类 + AAAK 摘要 | ~250/房间 | 确认信息位置，导航 |
| L4 Drawer | 原始对话文本 | ~500/块 | 需要完整推理链时 |

**核心思想**：信息需求是分层的。AI 在大多数情况下只需要"知道记忆在哪里"，而不需要"把记忆全部读一遍"。渐进式加载把这两种需求分离，让 Token 只花在真正需要的地方。

---

*下一篇：[MemPalace 深度解析（五）：三种挖掘管道——Projects / Convos / General]*
