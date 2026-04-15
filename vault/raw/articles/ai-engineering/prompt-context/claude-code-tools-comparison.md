# Claude Code 三大工具深度横向对比
> gstack · Superpowers · Compound Engineering
> 分析时间：2026 年 4 月

---

## 执行摘要

2026 年 Q1，Claude Code 生态爆发出三个标志性开源工具包，总 GitHub ⭐ 超过 24 万，引发全球开发者社区的广泛讨论。它们分别代表了 **AI 辅助开发的三种不同哲学**：

| 工具 | 作者 | 定位 | 核心哲学 |
|------|------|------|---------|
| **gstack** | Garry Tan（YC CEO） | 虚拟工程团队 | 角色分工 + 认知切换 |
| **Superpowers** | Jesse Vincent（Prime Radiant） | 方法论强制执行 | 纪律约束 + TDD 强制 |
| **Compound Engineering** | Kieran Klaassen（Every Inc） | 知识复利飞轮 | 积累效应 + 系统变强 |

**核心洞察**：这三个工具解决的是同一个问题的**不同维度**——如何让 Claude Code 产出更可靠、更高质量的软件。

---

## 一、背景与来源

### gstack
- **作者**：Garry Tan，Y Combinator 总裁兼 CEO
- **诞生**：2026 年 3 月 12 日在 SXSW 演讲后公开发布
- **起点**：Tan 的个人生产力工具，用于独自构建产品
- **声称产出**：60 天内 60 万行生产代码，平均每天 1 万行
- **争议**：获誉"God Mode"，同时被批评为"美化的提示词工程"
- **病毒式传播**：发布 48 小时内超过 1 万 ⭐，Product Hunt 趋势榜第一

### Superpowers
- **作者**：Jesse Vincent，开源社区老将（Perl 5 核心维护者、RT 作者、Keyboardio 联创）
- **诞生**：2025 年 10 月首次发布博客介绍，2026 年 1 月 15 日正式进入 Anthropic 官方插件市场
- **起点**：解决 Claude Code"有能力但无纪律"的问题
- **成就**：chardet 7.0.0 库使用该方法重写，性能提升 41 倍，准确率从 94.5% → 96.8%
- **社区**：官方进入 Anthropic 插件市场后加速增长，峰值每天增加约 2000 ⭐

### Compound Engineering
- **作者**：Kieran Klaassen + Claude（Every Inc）
- **诞生**：2026 年 2 月 14 日，随 Every.to 指南发布
- **起点**：运营 5 个产品（每个产品单人工程团队）的实战经验提炼
- **差异化**：唯一真正解决"知识积累"问题的工具

---

## 二、核心哲学深度对比

### 2.1 问题诊断

三个工具对"Claude Code 有什么问题"的回答根本不同：

```
gstack 认为：
  Claude Code 的问题是"认知角色混淆"
  → 同一个 Agent 既要当 CEO 又要当 QA，输出质量不稳定
  → 解法：强制认知分工，每次只扮演一个角色

Superpowers 认为：
  Claude Code 的问题是"缺乏纪律"
  → 有能力但跳过测试、忽略边界情况、草率实现
  → 解法：强制执行严格的方法论，不能跳步

Compound Engineering 认为：
  Claude Code 的问题是"知识无法积累"
  → 每次会话从零开始，无法从过去的错误中学习
  → 解法：构建知识积累飞轮，让系统越用越强
```

**洞察**：这三个诊断都是正确的，它们针对的是 Claude Code 的**不同痛点**。

### 2.2 核心工作流对比

**gstack 的工作流（角色轮换）**：
```
/office-hours   → 想清楚要做什么（YC partner 对话）
/autoplan       → CEO + Design + Eng 三重审查计划
[实现代码]
/review         → 工程审查（必选门控）
/qa             → 浏览器测试
/ship           → 同步主干 + 测试 + 开PR
/retro          → 团队复盘
```
特点：**人工触发、线性流程、角色明确**

---

**Superpowers 的工作流（强制方法论）**：
```
[自动触发 - 无需人工命令]
Brainstorm  → 苏格拉底式对话，挖掘真实需求
Spec        → 可供用户审读的规格说明（分块展示）
Plan        → 微任务分解（2-5 分钟每任务）
TDD         → 写测试 → 确认测试失败 → 写实现（不可跳过）
Subagent    → 多 Agent 并行执行任务列表
Review      → 代码审查员 Agent
Finalize    → 验收 + 文档更新
```
特点：**自动触发、强制约束、违规直接回退**

---

**Compound Engineering 的工作流（复利循环）**：
```
/ce:ideate      → 发现高价值机会
/ce:brainstorm  → 逐一提问澄清需求
/ce:plan        → 3 Agent 并行研究 + 置信度门控
/ce:work        → Git worktree 隔离 + 分阶段执行
/ce:review      → 14+ Agent 并行审查 + 去重合并
/ce:compound    ← 【核心差异点】将学习结晶化
                   下次计划自动引用过去方案
```
特点：**人工触发、持续积累、飞轮效应**

---

## 三、技术架构深度对比

### 3.1 实现范式

| 维度 | gstack | Superpowers | Compound Engineering |
|------|--------|-------------|---------------------|
| **实现技术** | Markdown + Bash 脚本 | Markdown + Node.js 脚本 | Markdown + YAML |
| **触发机制** | 用户手动 /命令 | 自动触发（Session Hook） | 用户手动 /命令 |
| **Agent 数量** | 23 个工具（非独立 Agent） | 多个子 Agent（规模较小） | 35+ 专业 Agent |
| **并行度** | 中（部分并行） | 高（子 Agent 并行） | 极高（14+ 同时审查） |
| **持久化** | .gstack/ 目录 + CLAUDE.md | Skills 文件 | docs/solutions/ + CLAUDE.md |
| **知识积累** | /learn 命令（会话级） | 隐式（Skills 迭代） | 显式飞轮（/ce:compound） |

### 3.2 Agent 设计哲学

**gstack：角色扮演（Role Play）**
```
角色不是真正独立的 Agent，而是 Claude 进入不同的"思维模式"：

/plan-ceo-review → Claude 扮演 CEO，用产品视角审查
/review          → Claude 扮演 Eng Manager，用工程视角审查
/qa              → Claude 扮演 QA，用测试视角审查

优点：轻量、快速、无 Agent 协调开销
缺点：同一个 Claude 实例，缺乏真正的认知独立性
```

**Superpowers：子 Agent 委派（Subagent Delegation）**
```
主 Agent 接收任务 → 分解为微任务 → 委派给子 Agent → 检查输出

code-reviewer 子 Agent → 审查实现
test-runner 子 Agent   → 执行测试
spec-validator 子 Agent → 验证是否符合规格

优点：真正的 Agent 独立性，可并行
缺点：协调开销，更复杂的错误处理
```

**Compound Engineering：专业委员会（Expert Panel）**
```
skill 策略层 → 派生专业 Agent 委员会

security-sentinel  + performance-oracle + 
architecture-strategist + data-integrity-guardian + 
kieran-rails-reviewer + dhh-rails-reviewer + ...
               ↓
         并行审查（~2分钟）
               ↓
         去重 + 合并 + 优先级排序
               ↓
         单一统一报告

优点：每个 Agent 真正专业化，覆盖面广
缺点：Agent 数量维护成本高
```

### 3.3 知识持久化对比

```
gstack 的知识持久化：
  ~/.gstack/projects/{project}/learnings/
  ├── session-2026-03-16-001.md
  └── session-2026-03-17-001.md
  
  /learn 命令：管理跨会话学习
  - 可审查、搜索、剪枝、导出
  - 学习随会话复合，gstack 对你的代码库越来越聪明
  
  限制：主要是模式和偏好，非结构化解决方案库

---

Superpowers 的知识持久化：
  技能文件本身是迭代的（Skills 可自我改进）
  Claude 有"感情日志"（feelings journal）用于反思
  
  限制：没有显式的"解决方案库"，积累是隐式的
  
---

Compound Engineering 的知识持久化：
  docs/solutions/{category}/{specific-problem}.md
  ├── performance/n-plus-one-eager-loading.md
  ├── security/csrf-unsubscribe-endpoint.md
  └── architecture/service-object-extraction.md
  
  YAML frontmatter 确保可机器检索
  learnings-researcher 自动注入历史方案到新计划
  
  这是三者中最系统化的知识积累机制
```

---

## 四、功能特性矩阵

### 4.1 核心功能覆盖

| 功能 | gstack | Superpowers | CE |
|------|:------:|:-----------:|:--:|
| **计划生成** | ✅ /autoplan | ✅ 自动 | ✅ /ce:plan |
| **代码执行** | ✅ 手动 | ✅ 子 Agent | ✅ /ce:work |
| **代码审查** | ✅ /review | ✅ code-reviewer | ✅ 14+ Agent |
| **安全审查** | ✅（内置） | ⚠️ 通过 review | ✅ 专门 Agent |
| **性能审查** | ⚠️ 有限 | ⚠️ 通过 review | ✅ 专门 Agent |
| **TDD 强制** | ❌ | ✅ 强制 | ⚠️ 鼓励但不强制 |
| **浏览器测试** | ✅ /qa + GStack Browser | ❌ | ✅ /test-browser |
| **知识积累** | ⚠️ /learn（会话级） | ⚠️ 隐式 | ✅ 显式飞轮 |
| **Git 工作流** | ✅ /ship | ⚠️ 基本 | ✅ 完整套件 |
| **设计审查** | ✅ /design-review | ❌ | ✅ 设计 Agent |
| **PR 管理** | ✅ 完整 | ⚠️ 基本 | ✅ 完整 |
| **Retro 复盘** | ✅ /retro | ❌ | ⚠️ 通过 compound |
| **多模型审查** | ✅ /codex（跨模型） | ❌ | ❌ |
| **iOS 测试** | ❌ | ❌ | ✅ /test-xcode |
| **图像生成** | ❌ | ❌ | ✅ gemini-imagegen |

### 4.2 平台兼容性

| 平台 | gstack | Superpowers | CE |
|------|:------:|:-----------:|:--:|
| Claude Code | ✅ | ✅（官方市场） | ✅ |
| OpenAI Codex CLI | ✅ | ✅（手动） | ✅ |
| Cursor | ✅ | ✅（内置市场） | ✅ |
| OpenCode | ✅ | ✅（手动） | ✅ |
| GitHub Copilot | ✅ | ❌ | ✅ |
| Gemini CLI | ✅ | ❌ | ✅ |
| Windsurf | ✅ | ❌ | ✅ |
| Factory Droid | ✅ | ❌ | ✅ |
| Kiro | ✅ | ❌ | ✅ |
| 支持平台数 | **8+** | **3** | **12+** |

**CE 在跨平台支持上领先，Superpowers 最为聚焦（Claude Code 为主）。**

---

## 五、使用体验深度对比

### 5.1 学习曲线

```
gstack：
  Day 1: 安装（git clone + ./setup）
  Day 1: 理解 6-9 个核心命令
  Day 1: 开始使用（几乎零门槛）
  Week 1: 掌握完整工作流
  Month 1: 个性化（添加自定义技能）
  
  学习曲线：██░░░░░░░░ 较低

---

Superpowers：
  Day 1: 安装（插件市场一键）
  Day 1: 阅读 Getting Started SKILL.md
  Day 1-3: 适应自动触发模式（需要心理转变）
  Week 1: 理解 TDD 强制流程
  Month 1: 习惯并获益
  
  关键转变点：从"我触发 Claude"到"Claude 自动启动工作流"
  学习曲线：████░░░░░░ 中等（主要是思维模式的转变）

---

Compound Engineering：
  Day 1: 安装（插件市场一键）
  Day 1-3: 建立项目文件结构
  Week 1: 学习完整命令集（23 个命令，35+ Agent）
  Week 2: 第一次感受到 /ce:compound 的价值
  Month 3+: 真正的复利效应开始显现
  
  学习曲线：██████░░░░ 较高（组件多，哲学深）
```

### 5.2 "第一次使用"体验对比

**gstack 第一次使用**：
```
$ cd my-project
$ /office-hours 我想给用户添加通知功能

Claude: 好的，让我作为 YC partner 和你一起想清楚这个功能...
[10 分钟后]
→ 清晰的产品方向

$ /autoplan
→ CEO + Design + Eng 三重审查计划
→ 5 分钟后，可执行的计划文档
```
**感受**：立即有用，像有了一个会问好问题的高级顾问。

---

**Superpowers 第一次使用**：
```
$ cd my-project
$ claude
[Superpowers 自动触发]

Claude: 我注意到你想开始一个新任务。在我们写任何代码之前，
        我需要理解你真正想解决的问题...
        
        请告诉我：当前的痛点是什么？[等待用户回答]
        → 再问一个问题...
        → 再问一个问题...
[规格说明生成]

Claude: 这是规格说明的第一部分（每块足够短，你能真正读完）...
        你同意这个设计方向吗？
```
**感受**：有点意外（没有输入命令就开始了），但流程清晰，像有了一个严格的技术负责人。

---

**Compound Engineering 第一次使用**：
```
$ cd my-project
$ /ce:brainstorm 为用户添加通知功能
→ 一系列澄清问题（逐一提问）
→ docs/brainstorms/notifications.md

$ /ce:plan 
→ 3 个 Agent 并行研究
→ 结构化计划（含置信度）

$ /ce:work
→ 4 阶段执行

$ /ce:review PR#142
→ 14 个 Agent 并行审查（2 分钟）
→ 统一报告

$ /ce:compound
→ 学习被结晶化
→ CLAUDE.md 更新
```
**感受**：流程完整且深度，第一次用时感受不到"复利"（因为还没有积累），但随时间推移会越来越强大。

---

## 六、适用场景与选型指南

### 6.1 人群画像

**gstack 最适合**：
- 🎯 **创始人/技术 CEO**：需要同时扮演 CEO、设计师、工程师
- 🎯 **独立开发者**：快速验证想法，从 0 到 1 构建产品
- 🎯 **全栈工程师**：需要跨越产品-设计-工程多个维度思考
- 🎯 **想立即上手**：无需深度配置，安装即用
- 🎯 **设计敏感的产品**：/design-review 和设计系统工具链

**Superpowers 最适合**：
- 🎯 **想要 TDD 纪律的团队**：强制测试驱动，不容妥协
- 🎯 **中型复杂项目**：需要结构化规格和微任务分解
- 🎯 **质量优先的产品**：宁可慢一点，也要测试覆盖完整
- 🎯 **曾经被 AI 生成的低质代码坑过的开发者**
- 🎯 **习惯结对编程风格**：苏格拉底式对话感觉像和高级工程师结对

**Compound Engineering 最适合**：
- 🎯 **长期运营的产品**：真正能享受复利效应（需要积累时间）
- 🎯 **小团队多产品**：Every Inc 模式（1人工程师 × 5 个产品）
- 🎯 **Rails/Ruby 技术栈**：Agent 生态最为完善
- 🎯 **重视知识管理的组织**：将机构知识编码为系统
- 🎯 **代码质量要求极高**：最全面的专业审查 Agent 矩阵

### 6.2 项目阶段选型

```
阶段一：0 → 1 原型（0-4 周）
  推荐：gstack ★★★  Superpowers ★★  CE ★

阶段二：1 → 10 快速迭代（1-6 个月）
  推荐：gstack ★★★  Superpowers ★★★  CE ★★

阶段三：10 → 100 规模化（6 个月以上）
  推荐：gstack ★★  Superpowers ★★★  CE ★★★★

阶段四：成熟产品维护（1 年以上）
  推荐：gstack ★  Superpowers ★★  CE ★★★★★
```

### 6.3 技术栈选型

| 技术栈 | 推荐 | 原因 |
|--------|------|------|
| Ruby on Rails | CE > gstack ≈ SP | DHH/Kieran Agent，Rails 专精 |
| Python | gstack ≈ CE > SP | CE 有 Python 专项 Agent |
| TypeScript | CE ≈ gstack > SP | CE 有 TS 专项 Agent |
| Go | gstack ≈ SP > CE | CE 的 Agent 主要针对 Rails |
| 任意栈原型 | gstack > SP ≈ CE | gstack 框架无关且快速 |

---

## 七、设计哲学深度比较

### 7.1 对"AI 角色"的不同理解

```
gstack 的理解：
  AI 是虚拟工程团队的成员
  每个成员有明确的角色和思维框架
  人类是"指挥官"，AI 执行特定角色
  
  隐喻：带着高级团队的一人公司

Superpowers 的理解：
  AI 是需要严格方法论约束的初级工程师
  方法论补偿 AI 天然缺乏的纪律性
  人类是"审核者"，AI 是"执行者"
  
  隐喻：严格带教体系下的实习工程师

Compound Engineering 的理解：
  AI 是知识系统的构建者和受益者
  每次工作既生产代码，又生产知识
  人类是"知识架构师"，AI 是"知识执行者"
  
  隐喻：能自我学习的工程系统
```

### 7.2 对"质量"的不同理解

**gstack**：质量 = 多角色视角的交叉验证
- CEO 问：值得做吗？
- Design 问：用户体验对吗？
- Eng 问：实现正确吗？
- QA 问：能测试证明吗？

**Superpowers**：质量 = 方法论的严格遵守
- 有测试 = 有质量的基础
- 规格说明通过 = 设计质量
- 代码审查通过 = 实现质量

**Compound Engineering**：质量 = 当前质量 + 系统质量提升
- 今天的 Bug 修复 = 明天的 Bug 预防
- 今天的审查发现 = 明天的编码规范
- 今天的解决方案 = 明天的参考文档

---

## 八、社区与生态比较

### 8.1 社区规模（2026 年 4 月）

| 指标 | gstack | Superpowers | CE |
|------|:------:|:-----------:|:--:|
| GitHub ⭐ | ~54,600 | ~121,000+ | ~12,700 |
| Forks | ~9,100 | 大量 | ~976 |
| 贡献者 | ~33 | 活跃社区 | ~50+ |
| Discord | ❌ | ✅ | ❌ |
| 官方市场 | ❌（非 Anthropic） | ✅（Anthropic 官方） | ✅ |
| PR 速度 | 快 | 快 | 快 |

**注意**：星数差异部分反映了作者影响力（Garry Tan 的网络效应）而非纯技术价值。

### 8.2 更新频率与维护

- **gstack**：高频更新，Garry Tan 几乎每天有新功能推文，版本迭代极快（60 天内 200+ commits）
- **Superpowers**：稳定迭代，Jesse Vincent 专注核心方法论，有配套实验室仓库（superpowers-lab）
- **CE**：活跃开发，社区贡献积极，有多个 PR 包含新 Agent 和 Skills

### 8.3 商业化路径

- **gstack**：完全免费，MIT 许可，YC 背书是最大的"营销资产"
- **Superpowers**：开源免费，Jesse Vincent 接受赞助，Prime Radiant 提供商业支持
- **CE**：开源免费，Every Inc 的内容和产品（Cora 等）是主要变现路径

---

## 九、技术创新亮点

### 每个工具最独特的创新点

**gstack 最独特**：

1. **GStack Browser（反机器人隐身浏览器）**
   - 真实 Chromium，~100ms 每命令
   - 自动模型路由：Sonnet 执行操作，Opus 分析结果
   - 一键从真实浏览器导入 Cookie（Chrome/Arc/Brave/Edge）
   - 打通了 AI 编码 + 浏览器测试的完整链路

2. **/codex 跨模型独立审查**
   - 通过 OpenAI Codex CLI 获得独立第二意见
   - 三种模式：review（通过/失败门控）、adversarial（对抗挑战）、open（开放咨询）
   - 跨模型发现的交叉验证是独特的质量保证机制

3. **团队模式（./setup --team）**
   - 全团队自动同步 gstack，通过 SessionStart hook 静默更新
   - 无需在 repo 中存储 gstack 文件

4. **自动计划链（/autoplan）**
   - 自动串联 CEO + Design + Eng 三重审查，表面上只需最终决策

---

**Superpowers 最独特**：

1. **TDD 强制执行机制（零妥协）**
   - 检测到代码写在测试前 → **删除代码，重新开始**
   - 这不是建议，是系统级约束
   - 在 AI 编码工具中，这是最强硬的质量门控

2. **苏格拉底式规格挖掘**
   - 不直接询问"你想要什么"，而是通过 Socratic 问答挖掘真实需求
   - 规格说明分块展示（每块足够短，确保用户真正阅读）
   - 解决了"用户说他想要 A，但实际需要 B"的根本问题

3. **自动触发的会话 Hook**
   - 不需要任何命令，Claude Code 启动后 Superpowers 自动激活
   - 通过 Session Hook 注入：系统自动读取 Getting Started SKILL.md
   - 这是三者中最"无摩擦"的激活机制

4. **微任务分解（2-5 分钟颗粒度）**
   - 将大任务分解到"热情的初级工程师也能执行"的粒度
   - 每个任务有明确的完成标准和验证步骤
   - 防止 Agent 迷失在大任务中

5. **Claude 的"感情日志"**
   - Claude 有私有日记，用于反思和自我调整
   - 让 Agent 能够"意识到"自己的错误模式并调整
   - 这是一个有趣的 metacognition 机制

---

**Compound Engineering 最独特**：

1. **置信度门控系统**
   - 每个 Agent 输出置信度分数
   - 低置信度 → 降级处理，减少噪声
   - 高置信度 → 强制修复
   - 三者中唯一有系统性"不确定性管理"的工具

2. **去重管道（Dedup Pipeline）**
   - 多个 Agent 发现同类问题时，自动合并
   - 避免开发者面对重复发现的"审查疲劳"
   - 这是工程细节上的成熟度体现

3. **/deepen-plan 超级研究模式**
   - 触发 40+ 个并行研究 Agent
   - 从代码库、框架文档、最佳实践三个维度同时研究
   - 对于复杂功能，这是目前最深度的自动化前期调研

4. **文档审查 Agent（7个）**
   - 在代码写之前就审查计划文档
   - `adversarial-document-reviewer` 专门质疑计划的前提假设
   - 将"评审"提前到最便宜的阶段

5. **显式知识积累飞轮**
   - YAML frontmatter 的机器可检索性
   - learnings-researcher 自动注入历史方案
   - 这是唯一真正解决"机构知识"问题的设计

---

## 十、综合评分

### 10.1 多维度评分（满分 10 分）

| 维度 | gstack | Superpowers | CE |
|------|:------:|:-----------:|:--:|
| **上手便捷性** | 9 | 8 | 6 |
| **代码质量保证** | 7 | 9 | 9 |
| **TDD / 测试** | 5 | 10 | 6 |
| **知识积累** | 6 | 5 | 10 |
| **审查深度** | 7 | 7 | 10 |
| **设计/产品思维** | 9 | 3 | 6 |
| **浏览器测试** | 9 | 3 | 7 |
| **跨平台支持** | 8 | 5 | 10 |
| **社区活跃度** | 9 | 9 | 7 |
| **长期价值** | 6 | 8 | 10 |
| **定制灵活性** | 8 | 7 | 9 |
| **个人/小团队** | 10 | 8 | 7 |
| **企业/大团队** | 6 | 8 | 9 |

### 10.2 终极推荐矩阵

```
你的情况                           → 推荐

"我是独立开发者，想快速验证想法"    → gstack
"我想要最严格的 TDD 纪律"          → Superpowers  
"我有长期产品，想建立知识体系"      → CE
"我是技术 CEO，需要产品+工程双视角" → gstack
"我的团队代码质量参差不齐"         → Superpowers
"我用 Rails 构建 SaaS"             → CE（或 CE + gstack）
"我第一次用 Claude Code"           → Superpowers（最自动化）
"我已经熟练用 Claude Code"         → CE（最系统化）
"我需要跨 AI 工具统一配置"         → CE（平台兼容最广）
"我需要浏览器自动化测试"           → gstack
"我想要多模型交叉验证"             → gstack（/codex）
```

---

## 十一、三者组合使用的可能性

### 11.1 理论上的组合价值

```
gstack + Superpowers：
  - gstack 负责产品思维（/office-hours, /autoplan）
  - Superpowers 负责代码纪律（TDD 强制，子 Agent）
  - 技术冲突：Superpowers 的交互式问答可能与 gstack 流程冲突

gstack + CE：
  - gstack 负责设计和产品审查（/design-review, CEO review）
  - CE 负责工程审查和知识积累（/ce:review, /ce:compound）
  - 这是最自然的组合：gstack 的产品视角 + CE 的工程深度

Superpowers + CE：
  - Superpowers 负责开发纪律（TDD，规格）
  - CE 负责知识积累（/ce:compound, learnings）
  - 潜在冲突：两套工作流可能互相干扰
```

### 11.2 "理想工具链"设想

如果可以自由组合，最强的配置可能是：

```
产品规划阶段：gstack /office-hours + /autoplan
需求澄清阶段：Superpowers 苏格拉底式对话
计划生成阶段：CE /ce:plan（40+ Agent 并行研究）
代码执行阶段：Superpowers TDD 子 Agent
代码审查阶段：CE /ce:review（14+ 专业 Agent 委员会）
知识积累阶段：CE /ce:compound
浏览器测试：gstack /qa
多模型验证：gstack /codex
```

当然，在实际中，工具之间的工作流冲突会使这种理想组合难以实现。

---

## 结论

**没有"最好的工具"，只有"最适合你场景的工具"。**

- 如果你想**立即生产力提升**，选 **gstack**
- 如果你想**代码质量从根本改善**，选 **Superpowers**  
- 如果你想**构建自我进化的工程系统**，选 **Compound Engineering**

最深刻的洞察是：这三个工具的爆火，证明了 2026 年 AI 编码的真正瓶颈**不再是模型能力**，而是**结构、纪律和知识管理**。Claude Code 本身已经足够强大；问题是如何以正确的方式使用它。

这三个工具，从三个不同的角度，各自给出了一个成熟的答案。

---

*对比基于 2026 年 4 月公开信息 | garrytan/gstack · obra/superpowers · EveryInc/compound-engineering-plugin*
