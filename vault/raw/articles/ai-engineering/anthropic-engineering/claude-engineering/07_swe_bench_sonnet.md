# 在 SWE-bench Verified 上树立新标杆：Claude 3.5 Sonnet 的编码 Agent 实践

> **原文**：[Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet](https://www.anthropic.com/engineering/swe-bench-sonnet)  
> **发布日期**：2025 年 1 月 6 日  
> **类别**：编码 Agent · Benchmark · 软件工程 AI

---

## 摘要

本文记录了 Anthropic 使用 Claude 3.5 Sonnet 在 SWE-bench Verified 上实现当时 SOTA 成绩（**49%**，后续迭代达到更高）的工程历程。文章不仅汇报了成绩，更深入剖析了 Agent 架构设计、工具优化策略和关键工程决策，是一篇将 benchmark 成绩与工程洞察紧密结合的优质文章。

---

## 一、SWE-bench Verified：评测背景

### 1.1 什么是 SWE-bench？

SWE-bench（Software Engineering Benchmark）是一个测试 AI 系统能否解决真实 GitHub Issue 的评测框架，由 Carlos E. Jiménez 等人于 2023 年提出：

- **任务形式**：给定真实 GitHub 仓库 + 描述 Bug/Feature 的 Issue，要求生成能通过测试套件的代码补丁
- **SWE-bench Verified**：经人工验证确保测试套件能可靠区分正确/错误解决方案的子集
- **评测难点**：需要跨文件理解、多步骤修改、与测试框架交互

### 1.2 为何重要？

SWE-bench 的设计让它比代码补全更接近真实软件工程工作：
- 真实开源仓库（Django、Flask、Sympy 等）
- 真实用户报告的 Bug
- 真实测试用于验证（而非模型自判断）

---

## 二、Agent 架构：工程决策的核心

### 2.1 基础架构

Claude Code 的 SWE-bench Agent 采用相对简单的单 Agent 架构：
- Claude 3.5 Sonnet 作为核心推理引擎
- 一套精心设计的工具集（文件读写、命令执行、搜索等）
- 无复杂的多 Agent 编排

这个设计选择体现了 Anthropic 一贯的"简单优于复杂"哲学——复杂的多 Agent 架构并未带来额外收益，单 Agent 配合优质工具就能达到 SOTA。

### 2.2 工具设计的深度优化

文章详细描述了一个关键工程发现——**工具优化比 prompt 优化花了更多时间**：

**发现的问题**：Agent 在从仓库根目录移动后，使用相对路径时出错

**解决方案**：修改工具定义，**要求始终使用绝对路径**

**效果**：模型随后"无懈可击"地使用此工具

这个案例完美体现了"poka-yoke"工具设计——通过修改接口设计使错误在结构上无法发生。

### 2.3 "think" 工具的集成

SWE-bench Agent 集成了 "think" 工具，专为代码调试场景定制：

```json
{
  "name": "think",
  "description": "当发现 Bug 的根因时，在此工具中对多种修复方案进行头脑风暴，评估哪种改动最简单有效。当收到测试结果时，头脑风暴修复失败测试的方法。",
  ...
}
```

实验（n=30 有 think 工具 vs n=144 无 think 工具）表明：think 工具平均提升性能 **1.6%**（Welch t 检验，p < 0.001，效应量 d=1.47）。

---

## 三、关键工程洞察

### 3.1 ACI（Agent-Computer Interface）的重要性

文章最有价值的工程洞察之一：在 SWE-bench 上，Anthropic 工程师花在**工具优化**上的时间多于花在**整体 prompt** 上的时间。

这证实了一个对 Agent 工程师的重要建议：工具接口设计（ACI）应该获得与用户界面设计（HCI）同等的工程重视度。

### 3.2 测试驱动的 Agent 工程

SWE-bench 任务的一个独特优势：**代码解决方案可以通过自动化测试验证**。

这形成了理想的 Agent 反馈循环：
```
生成补丁 → 运行测试 → 分析失败原因 → 修改策略 → 重试
```

测试结果提供了"ground truth"，让 Agent 能够客观评估自己的进展，而不是依赖模型的自我评判。

### 3.3 多文件修改的挑战

SWE-bench 任务常需要修改多个相互关联的文件：
- 主功能代码
- 测试文件
- 配置文件
- 文档

这需要 Agent 维护跨文件的全局上下文，是 long-horizon task 的一个缩影。

---

## 四、与其他评测的关联

### 4.1 SWE-bench 与 Terminal-Bench 的对比

| 维度 | SWE-bench | Terminal-Bench 2.0 |
|---|---|---|
| 任务类型 | 修复 GitHub Issues | 通用终端任务 |
| 资源敏感性 | 较低（+1.54% 在 5x RAM） | 较高（+6% 在 Uncapped） |
| 任务多样性 | 聚焦代码库 | 更广泛 |
| 验证方式 | 自动测试 | 任务完成检查 |

### 4.2 与行业竞争的关系

在 SWE-bench 上的竞争激烈，各大 AI 实验室都将 SWE-bench 成绩作为编码能力的重要指标。文章的发布标志着 Claude 在这一基准上取得领先地位（当时）。

---

## 五、深度辨析

### 5.1 SOTA 成绩的解读

达到 SOTA 固然重要，但文章更值得关注的是**如何达到**的工程洞察：

1. 简单单 Agent 架构就能达到 SOTA（复杂 ≠ 更好）
2. 工具设计质量比 prompt 复杂度更重要
3. "think" 工具的结构化推理空间带来稳定提升

### 5.2 评测局限性的诚实认识

SWE-bench 的局限：
- 仅覆盖特定 Python 开源项目
- "能通过测试"不等于"高质量的生产代码"
- 测试套件覆盖范围可能不全面

Anthropic 并未将 SWE-bench 分数作为万能指标，而是将其视为能力的一个测量维度。

### 5.3 对 Claude Code 产品的意义

SWE-bench 的成绩直接支撑了 Claude Code 产品的核心价值主张：Claude 不仅是代码补全工具，而是能够独立解决真实软件工程问题的 Agent。

---

## 六、对编码 Agent 工程师的建议

基于本文的工程洞察：

1. **测试先行**：为 Agent 提供验证机制，避免 Agent 自我评判
2. **绝对路径原则**：文件系统操作工具应设计为只接受绝对路径
3. **工具迭代重于 prompt 迭代**：找出 Agent 在工具使用上的系统性错误，修改工具接口而非 prompt
4. **引入 think 工具**：在代码调试类任务中显著提升成功率和一致性

---

## 参考与扩展阅读

- [SWE-bench Verified](https://www.swebench.com/) — 原始评测框架
- [Think 工具](https://www.anthropic.com/engineering/claude-think-tool) — SWE-bench 中 think 工具的详细分析
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — Agent 工具设计原则
- [Claude Code](https://www.anthropic.com/claude-code) — 产品落地

---

*本文分析基于 Anthropic Engineering Blog 原文，写于 2026 年 4 月。*
