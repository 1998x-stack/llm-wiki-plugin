# 有效的长期运行 Agent Harness 设计

> **原文**：[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)  
> **发布日期**：2025 年 11 月 26 日  
> **类别**：Agent 工程 · Harness 设计 · 长时任务

---

## 摘要

本文探讨了为长时间运行的 AI Agent 构建高效 Harness（运行框架）的工程方法。Harness 是 Agent 与底层基础设施之间的接口层，负责状态管理、错误恢复、检查点和监控。文章提出了 Harness 设计的核心原则，特别关注跨多个上下文窗口维护 Agent 连贯性的挑战。

---

## 一、Harness 的定义与作用

Agent Harness 是包裹 LLM Agent 的工程层，负责：
- **状态持久化**：跨会话保存 Agent 进度
- **错误恢复**：在工具调用或 API 错误时优雅处理
- **检查点**：周期性保存状态，支持从中间点恢复
- **监控**：追踪 Agent 行为，便于调试
- **资源管理**：控制 token 消耗和 API 调用频率

没有良好的 Harness，长时运行 Agent 极易因单点故障导致整个任务失败。

---

## 二、长时任务的核心挑战

### 2.1 上下文窗口边界问题

长时任务最根本的挑战：任务执行时间往往超过单个上下文窗口所能承载的对话历史。

**具体表现**：
- 代码库迁移任务可能持续数小时
- 上下文窗口逼近限制后，早期决策被"遗忘"
- Agent 可能重复已完成的工作，或忘记重要约束

### 2.2 错误复合效应

Agent 的错误不像传统软件那样局部化：
- 单步错误可能导致 Agent 走上完全不同的路径
- 错误在多步迭代中积累放大
- 传统的"重启"策略成本极高（用户体验差 + 资源浪费）

---

## 三、Harness 设计的核心原则

### 3.1 初始化-编码循环（Initializer/Coding-agent Pattern）

**关键设计**：将长任务分解为"初始化"和"执行"两个分离的角色：

```
Initializer Agent：
- 理解完整任务
- 创建详细的任务规划文件（如 features.json）
- 设定检查点标准
- 生成 claude-progress.txt

Coding Agent（多实例）：
- 读取 claude-progress.txt 了解当前状态
- 执行下一步任务
- 更新进度文件
- 提交检查点
```

### 3.2 外化进度追踪

**核心实践**：使用文件系统作为外部记忆：

```
claude-progress.txt：
- 已完成的任务
- 当前进行中的任务
- 下一步计划
- 关键决策和约束
- 已知问题和阻塞点

features.json：
- 功能列表及状态
- 每个功能的完成标准
- 依赖关系
```

### 3.3 检查点策略

**原则**：不依赖 Agent 自我报告来决定是否达到检查点，而是通过**可验证的状态**判断。

```python
def is_checkpoint_reached(task_state):
    # 不好：Agent 说"我完成了X"
    # 好：检查可验证条件
    return (
        all_tests_pass(task_state) and
        code_compiles(task_state) and
        required_files_exist(task_state)
    )
```

### 3.4 防止过早声明完成

**常见失败模式**：Agent 在任务未完成时声明完成，尤其是在上下文即将用尽时。

**对策**：
- 在 Harness 中设置独立的完成验证机制
- 不信任 Agent 的自我报告，依赖客观验证
- 对"任务完成"设置强制确认步骤

---

## 四、会话间的状态传递

### 4.1 上下文压缩（Handoff）

当上下文接近限制时，Harness 应触发优雅的会话交接：

```
会话结束 → 压缩摘要：
1. 已完成工作概述
2. 当前代码状态
3. 下一步的明确指令
4. 关键约束和决策背景

新会话开始 → 加载：
1. 压缩摘要
2. 当前 claude-progress.txt
3. 相关代码文件（有选择地）
```

### 4.2 E2E 测试框架

长时 Agent 的 E2E 测试不同于传统软件测试：
- 不能只测试中间步骤（Agent 可能绕过任何特定路径）
- 需要测试最终状态是否满足需求
- 需要测试会话交接是否保持连贯性

---

## 五、深度辨析

### 5.1 Harness 与 Agent 能力的互补关系

优秀的 Harness 不是弥补 Agent 能力的不足，而是**释放** Agent 的能力：
- Agent 不需要追踪自己的状态（Harness 负责）
- Agent 可以专注于当前步骤的推理（而非全局管理）
- Agent 出错时 Harness 提供缓冲（而非直接失败）

### 5.2 与传统软件工程的类比

Harness 设计与分布式系统的 Saga 模式高度相似：
- 将长事务分解为可补偿的短步骤
- 每步成功后记录进度
- 失败时从最近检查点回滚或继续

这种类比为 Harness 工程师提供了丰富的已知解决方案库。

---

## 六、实践建议

1. **从小任务开始测试 Harness**：先用简单任务验证状态追踪和检查点逻辑
2. **设计可观察的中间状态**：确保每一步结束后状态可被独立验证
3. **为失败设计**：假设 Agent 会在任意点失败，Harness 必须能从该点恢复
4. **避免过度依赖 Agent 自我报告**：使用客观指标验证进度

---

*本文分析基于 Anthropic Engineering Blog 原文，写于 2026 年 4 月。*
