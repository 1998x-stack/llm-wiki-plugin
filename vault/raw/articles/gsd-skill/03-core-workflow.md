# GSD 深度解析 · 第三篇
# 核心工作流：从想法到上线的完整链路

> **上一篇**：[第二篇——`.planning/` 上下文文件系统](./02-context-file-system.md)

---

## 一、工作流全貌

GSD 的标准开发周期是：

```
新项目初始化
/gsd:new-project
       │
       ▼
 ┌─────────────────────────────────────────┐
 │           对每个阶段循环：               │
 │                                         │
 │  /gsd:discuss-phase N  ← 捕获实现偏好   │
 │            │                            │
 │  /gsd:ui-phase N       ← UI 设计契约    │
 │  （仅有前端的阶段）                      │
 │            │                            │
 │  /gsd:plan-phase N     ← 研究 + 规划    │
 │            │                            │
 │  /gsd:execute-phase N  ← 并行执行       │
 │            │                            │
 │  /gsd:verify-work N    ← 人工验收       │
 │            │                            │
 │  /gsd:ship N           ← 创建 PR（可选）│
 └─────────────────────────────────────────┘
       │
       ▼
/gsd:audit-milestone    ← 里程碑审查
/gsd:complete-milestone ← 存档 + 打 Tag
       │
       ▼
/gsd:new-milestone      ← 下一个版本
```

本篇逐步解析每个命令的内部机制、触发的智能体、产生的文件、以及设计背后的理由。

---

## 二、`/gsd:new-project` — 项目初始化

### 内部流程

```
/gsd:new-project
       │
       ├─ 步骤1：提问（Questions）
       │   GSD 主智能体向你提问，直到完全理解你的想法：
       │   - 这个产品/工具/服务解决什么问题？
       │   - 目标用户是谁？
       │   - 技术偏好（语言、框架、托管平台）？
       │   - v1 的边界在哪里？
       │   - 有什么明确不做的？
       │   提问不是一次性的，而是持续深挖，直到 GSD 认为理解完整
       │
       ├─ 步骤2：领域研究（Research，可选但推荐）
       │   并行 spawn 研究子智能体：
       │   ├── 子智能体A：技术栈研究（选型建议、版本兼容）
       │   ├── 子智能体B：功能研究（类似产品实现方案）
       │   ├── 子智能体C：架构研究（最佳实践）
       │   └── 子智能体D：陷阱研究（常见错误、性能坑）
       │   输出：research/ 目录下的研究报告
       │
       ├─ 步骤3：需求提炼（Requirements）
       │   将对话中的信息整理为结构化需求：
       │   v1（本里程碑）/ v2（未来）/ out-of-scope（永不做）
       │   输出：REQUIREMENTS.md
       │
       └─ 步骤4：路线图生成（Roadmap）
           将 v1 需求分解为阶段，等待你审批
           输出：ROADMAP.md, PROJECT.md, STATE.md
```

### `--auto` 模式

如果你已经有 PRD 或想法文档：

```bash
/gsd:new-project --auto @prd.md
```

GSD 直接读取文档内容，跳过提问阶段，直接进行研究→需求→路线图。适合已有清晰规格的情况。

### 棕地项目的正确顺序

对于已有代码的项目，必须先分析代码库：

```bash
/gsd:map-codebase          # 并行分析现有代码（4 个子智能体）
/gsd:new-project           # 提问聚焦在"你要新增什么"
```

`map-codebase` 生成的 `codebase/` 目录（STACK.md, ARCHITECTURE.md, CONVENTIONS.md, CONCERNS.md）会被 `new-project` 读取，规划自动继承现有代码约定。

---

## 三、`/gsd:discuss-phase N` — 捕获实现偏好

### 为什么需要单独的 discuss 步骤？

ROADMAP.md 的阶段描述只有一两句话，例如：

> "Phase 2: 项目 CRUD 功能"

这句话没有回答任何实现问题：
- 删除是硬删除还是软删除？
- 列表页是分页还是虚拟滚动？
- 项目图片是上传到云存储还是存 URL？
- 是否需要拖拽排序？

如果不在执行前捕获这些决策，Claude 会自己做选择——结果"合理但不是你想要的"。

### discuss-phase 的内部流程

```
/gsd:discuss-phase N
       │
       ├─ 读取：ROADMAP.md 的第 N 阶段描述
       │        PROJECT.md（技术栈约束）
       │        codebase/（如果存在）
       │
       ├─ 分析阶段特性，识别"灰色地带"：
       │   ┌──────────────────────────────────────────────┐
       │   │ 阶段类型    → 识别的灰色地带类型             │
       │   ├──────────────────────────────────────────────┤
       │   │ 视觉/UI     → 布局、密度、交互、空状态       │
       │   │ API/后端    → 响应格式、错误码、分页策略     │
       │   │ 内容系统   → 结构、层级、搜索、过滤         │
       │   │ 数据处理   → 验证规则、转换逻辑、边界情况   │
       │   └──────────────────────────────────────────────┘
       │
       ├─ 逐一询问，你可以：
       │   - 给出明确答案（写入 CONTEXT.md 为决策）
       │   - 说"你来决定"（Claude 做出选择，同样写入）
       │   - 说"暂时跳过"（保留为开放项，Claude 执行时自行判断）
       │
       └─ 输出：phases/N-*/CONTEXT.md
```

### 两种 discuss 模式

**standard 模式（默认）**：从空白状态提问

```
GSD: 这个阶段涉及用户列表页，请问：
     1. 分页方式：传统分页（按钮翻页）还是无限滚动？
     2. 每页默认显示多少条记录？
     3. 是否需要搜索功能？
```

**assumptions 模式**（通过 `/gsd:settings` 开启）：先读代码再提假设

```
GSD: 根据现有代码库，我计划这样实现：
     1. 分页：使用 infinite scroll（参考已有的 PostList 组件）
     2. 每页 20 条（与 PostList 保持一致）
     3. 搜索：暂不实现（与 REQUIREMENTS 中 out-of-scope 一致）
     
     哪些判断需要修正？
```

assumptions 模式对熟悉代码库的开发者更高效——不需要从头回答所有问题，只需纠正 Claude 的误判。

### `--batch` 标志

默认是一问一答，如果想一次性看到所有问题：

```bash
/gsd:discuss-phase 2 --batch
```

GSD 会展示所有识别到的灰色地带，你可以批量回答，减少来回次数。

---

## 四、`/gsd:plan-phase N` — 研究 + 规划 + 验证

这是 GSD 工作流中技术含量最高的步骤。

### 内部流程

```
/gsd:plan-phase N
       │
       ├─ 读取：CONTEXT.md（你的实现偏好）
       │        REQUIREMENTS.md（本阶段的 v1 需求）
       │        PROJECT.md（技术约束）
       │
       ├─ 步骤1：并行领域研究（4 个子智能体，15-20 分钟）
       │   ├── gsd-stack-researcher
       │   │   研究本阶段涉及的库/框架的最佳实践
       │   ├── gsd-features-researcher
       │   │   研究功能实现方案，参考 CONTEXT.md 决策
       │   ├── gsd-architecture-researcher
       │   │   研究架构模式，与现有代码库架构保持一致
       │   └── gsd-pitfalls-researcher
       │       研究已知问题、版本陷阱、性能考量
       │   输出：合并为 RESEARCH.md
       │
       ├─ 步骤2：计划生成（gsd-planner）
       │   读取：PROJECT.md + REQUIREMENTS.md + CONTEXT.md + RESEARCH.md
       │   生成：2-3 个原子 XML 执行计划
       │   每个计划的规模：可以在一个 200k 上下文窗口内完成
       │   输出：N-01-PLAN.md, N-02-PLAN.md（等）
       │
       └─ 步骤3：计划验证循环（gsd-plan-checker）
           8 个维度验证（详见第五篇）
           ┌────────────────────────────────────┐
           │  PASS? ───Yes──→ 计划批准，流程继续 │
           │    │                               │
           │   No                               │
           │    │                               │
           │  gsd-planner 修订                  │
           │    │                               │
           │   最多循环 3 次                     │
           └────────────────────────────────────┘
           输出：最终批准的 N-M-PLAN.md 文件群
```

### 跳过特定步骤

```bash
/gsd:plan-phase 2 --skip-research   # 跳过领域研究（熟悉领域时节省时间）
/gsd:plan-phase 2 --skip-verify     # 跳过计划验证（快速迭代时）
```

---

## 五、`/gsd:execute-phase N` — 波次并行执行

这是 GSD 将所有前置工作转化为实际代码的步骤。

### 内部流程

```
/gsd:execute-phase N
       │
       ├─ 步骤1：依赖分析
       │   读取所有 N-M-PLAN.md
       │   分析 <depends_on> 标签，构建依赖 DAG
       │   将计划分组为"波次"
       │
       ├─ 步骤2：波次执行循环
       │   
       │   WAVE 1（独立计划，并行执行）
       │   ├── spawn gsd-executor A（200k 干净上下文）
       │   │   加载：PROJECT.md + N-01-PLAN.md
       │   │   执行：逐任务实现，每任务完成 git commit（--no-verify）
       │   │   输出：N-01-SUMMARY.md
       │   └── spawn gsd-executor B（200k 干净上下文）
       │       加载：PROJECT.md + N-02-PLAN.md
       │       执行：逐任务实现，每任务完成 git commit
       │       输出：N-02-SUMMARY.md
       │   
       │   等待 WAVE 1 全部完成
       │   
       │   WAVE 2（依赖 WAVE 1 的计划，并行执行）
       │   └── spawn gsd-executor C（200k 干净上下文）
       │       加载：PROJECT.md + N-03-PLAN.md
       │       （N-01/02 的结果已通过 git 提交可访问）
       │       输出：N-03-SUMMARY.md
       │
       └─ 步骤3：后验证（gsd-verifier）
           读取：PROJECT.md + REQUIREMENTS.md + 所有 SUMMARY.md
           检查：代码库是否实现了阶段目标
           ┌──────────────────────────────────────────────┐
           │  PASS → 输出 VERIFICATION.md（成功）         │
           │  FAIL → 输出 VERIFICATION.md（失败 + 诊断）  │
           │         问题被记录，/gsd:verify-work 时处理  │
           └──────────────────────────────────────────────┘
```

### 执行子智能体的隔离设计

每个 `gsd-executor` 子智能体：
- 拥有**独立的干净 200k 上下文**，不受其他子智能体影响
- 只接收：`PROJECT.md`（项目约束）+ 当前 `PLAN.md`（具体任务）
- 执行完成后退出，不积累历史状态
- 所有"背景知识"（库选型、架构决策）已蒸馏在 `<action>` 字段中

这是 GSD 能维持执行质量的关键：**每次执行都是第一次，没有上下文衰减**。

### Git 提交策略

执行过程中使用 `--no-verify` 跳过 pre-commit hooks（避免多个并行智能体触发 hook 争抢资源），波次结束后由编排者统一运行一次 hooks。

提交格式：
```bash
git commit -m "feat(02-01): implement project CRUD endpoints"
git commit -m "feat(02-01): add Zod validation for project schema"
git commit -m "test(02-01): add integration tests for project API"
```

---

## 六、`/gsd:verify-work N` — 人工验收测试

### 为什么需要人工验收？

自动化验证（gsd-verifier）检查的是"代码是否存在"和"测试是否通过"。它无法回答：

- 功能的使用体验是否符合你的期望？
- 交互细节是否正确？
- 边界情况下用户看到的是什么？

**你是唯一能判断"这是否是你想要的"的存在。**

### 内部流程

```
/gsd:verify-work N
       │
       ├─ 提取可测试的交付物清单
       │   读取：REQUIREMENTS.md（v1 需求）
       │         CONTEXT.md（实现偏好）
       │         VERIFICATION.md（自动验证结果）
       │   生成：具体可操作的验证步骤列表
       │
       ├─ 逐项引导你验证
       │   GSD: "请尝试用有效凭证登录，你能成功看到 Dashboard 吗？"
       │   你: "能" → ✅ 通过，继续下一项
       │   你: "不行，跳转到了 404" → ❌ 失败，记录问题
       │
       ├─ 失败项处理
       │   ├── 描述你观察到的现象
       │   ├── GSD spawn gsd-debugger 诊断根因
       │   │   读取：相关源代码 + PLAN.md + git diff
       │   │   输出：根因分析 + 修复建议
       │   └── 生成修复计划文件（可直接被 execute-phase 执行）
       │
       └─ 输出
           ├── phases/N-*/UAT.md（验收记录）
           └── 修复计划（如有失败项）
```

### 修复后的处理

如果 verify-work 发现问题并生成了修复计划：

```bash
/gsd:execute-phase N   # 执行修复计划（GSD 会识别新的修复计划文件）
/gsd:verify-work N     # 再次验收
```

这形成了一个封闭的**验收-修复-再验收**循环，直到所有项目通过。

---

## 七、`/gsd:ship N` — 创建 PR

```bash
/gsd:ship 2            # 为第 2 阶段创建 PR
/gsd:ship 2 --draft    # 创建草稿 PR
```

GSD 读取本阶段的所有 SUMMARY.md，自动生成包含以下内容的 PR 描述：
- 本阶段完成了什么
- 关键技术决策和理由
- 测试覆盖情况
- 相关需求 ID

如果你使用 `phase` 分支策略，GSD 会将当前 phase 分支 merge 到主分支并创建 PR。

---

## 八、`/gsd:complete-milestone` — 里程碑归档

```bash
/gsd:audit-milestone       # 验证里程碑达到定义完成（Definition of Done）
/gsd:complete-milestone    # 存档 + 打 release tag
```

`audit-milestone` 检查：
- 所有 v1 需求是否都通过了 UAT
- 是否有未完成的 PLAN 文件（执行了规划但未执行代码）
- 是否有 stub/placeholder 代码（Claude 承诺"后续实现"但未完成）

通过审查后，`complete-milestone` 将当前里程碑的所有规划文件归档到 `MILESTONES.md`，打 release tag（如 `v1.0.0`），清理临时文件。

---

## 九、`/gsd:next` — 自动推进

如果你不确定当前该执行哪个命令：

```bash
/gsd:next
```

GSD 读取所有状态文件（ROADMAP.md, STATE.md, phases/ 目录），分析当前位置，自动执行下一个逻辑步骤。

这是最懒人也最安全的使用方式——让 GSD 自己判断下一步。

---

## 十、快速路径：`/gsd:quick` 和 `/gsd:fast`

### `/gsd:quick` — 临时任务

对于不需要完整规划流程的小任务：

```bash
/gsd:quick
> 什么任务？ "修复登录按钮在移动 Safari 上不响应的 bug"
```

GSD 给你 GSD 质量保证（原子提交、状态追踪）但跳过大部分流程：
- 默认跳过：领域研究、plan-checker、post-verifier
- `--research` 标志：添加轻量研究步骤
- `--discuss` 标志：添加灰色地带讨论
- `--full` 标志：完整流程（计划验证 + 后验证）

这些标志可以组合：`/gsd:quick --discuss --research --full`

### `/gsd:fast` — 内联执行

对于极小的改动（修改错别字、更新配置值）：

```bash
/gsd:fast "将所有 console.log 替换为 logger.debug"
```

完全跳过计划生成，直接执行，但仍然提交代码。

---

## 十一、里程碑级别的工作流

完成一个里程碑后进入下一个：

```bash
/gsd:new-milestone "v2.0 协作功能"
```

`new-milestone` 的内部流程与 `new-project` 几乎相同，但 GSD 知道现有代码库的存在，提问聚焦在"新版本新增什么"，Seeds（前瞻想法）也会在此时检查触发条件。

---

## 小结

GSD 的工作流设计遵循两个核心原则：

**原则一：每个步骤单一职责**
- discuss 只捕获偏好，不做研究
- plan 只做研究和规划，不执行代码
- execute 只执行代码，不做决策
- verify 只做验收，不做研究

**原则二：信息在步骤间单向流动**
```
discuss → CONTEXT.md → plan → PLAN.md → execute → SUMMARY.md → verify → UAT.md
```

每个步骤消费上一步的产物，生成下一步的输入。上下文信息被精炼和结构化，而不是无差别地堆积。

下一篇，我们深入 GSD 的多智能体编排架构，了解 11 个专家子智能体是如何协同工作的。

---

*参考：[GSD GitHub](https://github.com/gsd-build/get-shit-done) · [USER-GUIDE.md](https://github.com/gsd-build/get-shit-done/blob/main/docs/USER-GUIDE.md)*
