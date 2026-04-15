# GSD 深度解析 · 第一篇：Context Rot 与上下文工程

> **系列导读**：本系列共 7 篇，逐组件深度解析
> [get-shit-done (GSD)](https://github.com/gsd-build/get-shit-done)——
> 一套为 Claude Code 设计的轻量级元提示、上下文工程与规格驱动开发系统。
> 作者：TÂCHES，GitHub Stars 40k+，被 Amazon/Google/Shopify 工程师使用。

---

## 一、从一个真实困境说起

你用 Claude Code 开始一个新项目，前几个任务做得很漂亮——代码清晰、风格统一、逻辑严密。但随着对话越来越长，Claude 开始出现奇怪的退化：

- 它"忘了"你说过要用 PostgreSQL，悄悄换回了 SQLite
- 新生成的组件与前三个风格明显不一致
- 注释里出现了 "I'll omit the details for brevity"
- 你让它解释，它引用了"你之前的要求"，但你压根没说过那话

这不是 Claude 的 bug，这是 **Context Rot（上下文腐败）**——LLM 在上下文窗口逐渐填满后，生成质量系统性降级的物理现象。GSD 就是专门为对抗这个问题而生的工程框架。

---

## 二、Context Rot 的物理机制

### 2.1 上下文窗口的真实消耗速度

Claude Sonnet 4.x 拥有 200,000 token 的上下文窗口，但中型项目的开发会话很快就会填满它：

```
会话内容                           消耗 token 估算
────────────────────────────────────────────────────
初期设计讨论                       ~15,000
需求文档 + 技术选型                 ~8,000
阶段 1 完整代码（中等功能）         ~25,000
阶段 2 完整代码                    ~30,000
阶段 3 完整代码                    ~35,000
计划、总结、中间过程消息            ~40,000
────────────────────────────────────────────────────
合计                               ~153,000  ← 已用 76%
```

当上下文填满 50~60% 时，可以观察到 Claude 开始：

1. **注意力稀释**：早期关键决策（"用 jose 不用 jsonwebtoken"）被边缘化
2. **主动压缩**：生成更短更简单的代码，出现"为简洁起见省略"等信号
3. **风格漂移**：命名规范、错误处理方式开始不一致
4. **幻觉决策**：编造之前不存在的约定，假装记得某些设计决策

### 2.2 传统解决方案为什么失败

| 方法 | 核心思路 | 根本缺陷 |
|------|----------|----------|
| BMAD | 仿企业 Sprint 流程 | 引入 Jira/故事点/retrospective，solo 开发者无法承受 |
| Speckit | 规格文档驱动 | 规格静态，缺乏从规格到执行的自动化桥接 |
| 手动 `/clear` | 定期清空上下文 | 清空后完全失忆，无法跨会话恢复项目状态 |
| 超长 system prompt | 把所有信息塞进提示 | 自身就消耗大量 token，加速 Context Rot |
| CLAUDE.md | 项目根目录说明文档 | 对简单项目有效，对多阶段复杂项目控制力严重不足 |

---

## 三、GSD 的核心洞见：复杂度属于系统层

GSD 的作者 TÂCHES 是一位完全依赖 Claude Code 的独立开发者。他的核心洞见只有一句话：

> **"The complexity is in the system, not in your workflow."**
> **复杂度应该在系统里，不应该在工作流里。**

GSD 对外表现为几条简单命令，背后是精密的工程系统：

```
用户输入                          系统背后实际运行的
────────────────────────          ──────────────────────────────────────────
/gsd:new-project              →   问题提取 + 并行领域研究 + 需求边界界定
/gsd:discuss-phase 1          →   实现偏好捕获 + CONTEXT.md 结构化生成
/gsd:plan-phase 1             →   4 个并行研究智能体 + 计划验证循环（最多3次）
/gsd:execute-phase 1          →   DAG 依赖分析 + 波次并行执行 + 每任务原子提交
/gsd:verify-work 1            →   UAT 逐项引导 + 自动调试智能体诊断
```

---

## 四、GSD 的五大技术支柱

### 支柱 1：上下文工程（Context Engineering）

**提示词工程**关注单次调用的措辞；**上下文工程**关注多步骤系统中信息流的全局架构设计——这是本质上不同的两个层次。

GSD 的关键实现：**每个命令只加载它真正需要的文件**

```
计划阶段（plan-phase 子智能体加载）：
  ✅ PROJECT.md        项目愿景（≤3 页，精心压缩）
  ✅ REQUIREMENTS.md   版本化需求边界
  ✅ CONTEXT.md        当前阶段实现偏好
  ✅ RESEARCH.md       本阶段领域研究结论

执行阶段（execute-phase 子智能体加载）：
  ✅ PLAN.md           单个原子任务（XML，2-3 个任务）
  ✅ PROJECT.md        最小化项目上下文

永远不加载：
  ✗ 历史对话记录
  ✗ 其他阶段的代码
  ✗ 旧的设计讨论
  ✗ 已完成阶段的研究报告
```

每个子智能体拿到的是**干净的全量 200k token**，而非被历史垃圾污染的上下文。

### 支柱 2：XML 结构化 Prompt

GSD 的每个执行计划都是结构化 XML，而非自然语言段落：

```xml
<task type="auto">
  <n>创建用户登录 API 端点</n>
  <files>src/app/api/auth/login/route.ts</files>
  <action>
    使用 jose 处理 JWT（禁用 jsonwebtoken——CommonJS 兼容问题）。
    从 users 表验证凭证，密码用 bcrypt 比对。
    成功后设置 httpOnly cookie，不在响应体中返回 token。
    失败统一返回 401，不透露具体原因（防枚举攻击）。
  </action>
  <verify>
    curl -X POST localhost:3000/api/auth/login \
      -d '{"email":"t@t.com","password":"correct"}' | grep -E "200|Set-Cookie"
  </verify>
  <done>有效凭证返回 200 + Set-Cookie；无效凭证返回 401</done>
</task>
```

每个标签有明确职责：`<n>` 也是 git commit 名称；`<files>` 消除路径猜测；`<verify>` 是 Claude 会真正运行的命令；`<done>` 是任务完成的语义判断标准。

### 支柱 3：多智能体编排

```
主会话（编排者）                   子智能体（专家执行者）
─────────────────────────          ──────────────────────────────────
轻量，不做任何重型工作              各自拥有独立的干净 200k 上下文
协调顺序、等待、整合结果            深度专注于单一专业任务
主会话上下文保持在 30-40%           任务完成即退出，不积累历史垃圾
```

> *"Your main context window stays at 30-40%. The work happens in fresh
> subagent contexts."* — GSD README

### 支柱 4：原子 Git 提交

每个任务完成后立即独立提交：

```bash
abc123f feat(08-02): create POST /api/auth/register endpoint
def456g feat(08-02): implement bcrypt password hashing
hij789k feat(08-02): add email confirmation flow
lmn012o docs(08-02): complete user registration plan
```

三个实际价值：`git bisect` 精确定位失败任务；每个任务独立回滚；Claude 跨会话读取 `git log` 快速理解项目演化。

### 支柱 5：波次并行执行（Wave Execution）

GSD 分析 PLAN 文件间的依赖关系，构建 DAG，将可并行的计划放入同一"波次"：

```
WAVE 1（并行）              WAVE 2（并行）          WAVE 3
┌──────────┐ ┌──────────┐  ┌──────────┐ ┌──────┐  ┌──────────┐
│ Plan 01  │ │ Plan 02  │→ │ Plan 03  │ │ P04  │→ │ Plan 05  │
│User Model│ │Prod Model│  │Orders API│ │CartAPI│  │ Checkout │
└──────────┘ └──────────┘  └──────────┘ └──────┘  └──────────┘
```

**垂直切片比水平切片并行度高得多**：按功能端到端切分的计划，各模块之间相互独立，可以完全并行；按技术层次切分的计划，必须严格顺序执行。

---

## 五、GSD 的边界

**解决的问题：** 上下文腐败 / 风格漂移 / 幻觉任务 / 跨会话失忆 / 执行缺乏验证

**不解决的问题：** 坏需求 / 领域知识缺失 / 外部集成的本质复杂度 / 团队协作工作流

---

## 六、快速安装

```bash
# 安装（支持 Mac / Windows / Linux）
npx get-shit-done-cc@latest

# 验证（Claude Code 中运行）
/gsd:help

# 推荐启动方式（GSD 的预期使用方式）
claude --dangerously-skip-permissions
```

---

## 七、本系列路线图

| 篇次 | 主题 |
|------|------|
| **第一篇**（本文） | Context Rot 与上下文工程 |
| 第二篇 | 上下文文件系统：`.planning/` 目录的设计哲学 |
| 第三篇 | 核心工作流五步法：从想法到发布的完整链路 |
| 第四篇 | 多智能体编排架构：11 个专家智能体的协作机制 |
| 第五篇 | XML 结构化计划系统：8 维 plan-checker 与 Nyquist 验证层 |
| 第六篇 | UI 设计契约系统：6 柱评分与 shadcn 集成 |
| 第七篇 | 配置、安全与高级功能：Workstreams/Seeds/四层安全防御 |

---

*参考来源：[GSD GitHub 仓库](https://github.com/gsd-build/get-shit-done) ·
[USER-GUIDE.md](https://github.com/gsd-build/get-shit-done/blob/main/docs/USER-GUIDE.md)*
