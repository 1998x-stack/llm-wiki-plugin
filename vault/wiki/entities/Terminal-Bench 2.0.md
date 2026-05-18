---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: [benchmark, agentic-coding, evaluation, terminal, Agent系统]
aliases: ["Terminal-Bench 2.0", "TerminalBench 2.0", "Terminal-Bench"]
relates_to:
  - "[[SWE-bench]] — compares_to"
  - "[[Anthropic]] — participates_in"
  - "[[评测驱动开发]] — used_by"
  - "[[基础设施噪声]] — affected_by"
supersedes: null
---

# Terminal-Bench 2.0

## 概述
终端操作 Agentic 编码评测基准，为每个任务推荐 CPU 和 RAM 规格，用于评估 AI Agent 在真实终端环境中的问题解决能力。

## 关键内容
1. **资源规范设计**：2.0 版本引入了每任务推荐的 CPU 和 RAM 规格，但研究发现"规定资源 ≠ 一致执行"——执行方法论会改变 Benchmark 实际测量的内容。
2. **[[基础设施噪声]]实验**：[[Gian Segato]] 等在 [[Terminal-Bench]] 2.0 上进行了六种资源[[Configuration|配置]]的受控实验（1x → 1.5x → 2x → 3x → 4x → Uncapped），发现：
   - 基础设施错误率随资源增加单调下降：1x 时 5.8% → 3x 时 2.1% → Uncapped 时 0.5%
   - 总成功率提升：1x → Uncapped 达 **+6 个百分点**（p < 0.01）
   - 两阶段行为：3x 以下主要修复基础设施可靠性，3x 以上额外资源真正帮助 Agent 解决新任务
3. **典型案例**：`bn-fit-modify`（[[托马斯·贝叶斯|贝叶斯]]网络拟合）任务中，富资源策略可安装 pandas + networkx + scikit-learn，贫资源策略被迫使用标准库从零实现——不同资源[[Configuration|配置]]在评测不同的模型能力。
4. **校准建议**：推荐 3× requests 作为 limits 起点，可将基础设施错误率降低 2/3（5.8% → 2.1%，p < 0.001），同时成功率提升保持在噪声范围内（p = 0.40）。
5. **其他噪声来源**：时间效应（通过率随一天中的时段波动）、并发级别、出口带宽、集群健康度。

## 与 SWE-bench 的对比

| 维度 | [[SWE-bench]] | [[Terminal-Bench]] 2.0 |
|---|---|---|
| 任务类型 | 修复 [[GitHub]] Issues | 通用终端任务 |
| 资源敏感性 | 较低（+1.54% 在 5x RAM） | 较高（+6% 在 Uncapped） |
| 任务多样性 | 聚焦代码库 | 更广泛 |
| 验证方式 | 自动测试 | 任务完成检查 |

[[Terminal-Bench]] 2.0 对资源[[Configuration|配置]]更敏感（+6% vs [[SWE-bench]] 的 +1.54%），表明终端任务更依赖系统资源，而 [[SWE-bench]] 的代码修复任务对资源变化相对不敏感。

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/06_infrastructure_noise.md]] — Quantifying infrastructure noise in agentic coding evals
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/07_swe_bench_sonnet.md]] — SWE-bench 与 Terminal-Bench 对比
- [Terminal-Bench 2.0 官网](https://terminal-bench.com/)

## 相关
- [[SWE-bench]] — compares_to（交叉验证显示 SWE-Bench 效应更小，仅 1.54 个百分点）
- [[Anthropic]] — participates_in（Anthropic 在其 GKE 集群上运行该 Benchmark）
- [[基础设施噪声]] — affected_by（Terminal-Bench 2.0 是基础设施噪声研究的主要实验平台）
- [[Google Kubernetes Engine (GKE)]] — hosts_on（运行于 GKE 容器环境）
- [[评测驱动开发]] — used_by（用于评测驱动开发方法论的实证）
