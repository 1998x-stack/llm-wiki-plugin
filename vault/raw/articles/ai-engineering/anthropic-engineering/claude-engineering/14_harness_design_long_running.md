# 长时运行应用开发的 Harness 设计

> **原文**：[Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
> **发布日期**：2026 年 3 月 24 日
> **类别**：Harness 工程 · 长时任务 · Agent 基础设施

---

## 摘要

本文是 [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) 的深化版本，专注于**应用开发场景**下的 Harness 设计。文章不仅讨论了通用的 Harness 原则，还针对"持续的软件开发任务"提供了具体的架构模式、状态管理策略和人机协作协议。

---

## 一、应用开发场景的特殊挑战

长时运行的**应用开发任务**与一般长时任务相比，有额外的复杂性：

### 1.1 代码库状态的积累性

代码库不像临时文件——每一步修改都积累：
- 早期的架构决策会约束后期的实现
- Bug 引入后可能在多处代码中蔓延
- 重构需要理解整个代码历史

这要求 Harness 不只维护"当前状态"，还要维护**决策历史**。

### 1.2 多层次验证的需求

应用开发有多层次的正确性标准：
- 语法正确性（代码是否编译）
- 单测通过（功能是否如期工作）
- 集成测试（组件交互是否正确）
- 端到端测试（用户流程是否完整）

Harness 需要在每个检查点运行适当层次的验证。

---

## 二、核心 Harness 组件

### 2.1 特性追踪器（Feature Tracker）

```json
{
  "features": [
    {
      "id": "auth-01",
      "name": "用户认证",
      "status": "in_progress",
      "subtasks": [
        {"id": "auth-01-a", "name": "JWT 实现", "status": "complete"},
        {"id": "auth-01-b", "name": "刷新 Token", "status": "in_progress"},
        {"id": "auth-01-c", "name": "登出流程", "status": "pending"}
      ],
      "tests": ["test_auth.py::test_jwt_valid", "test_auth.py::test_refresh"],
      "checkpoints": ["2026-03-24T10:00:00Z"],
      "blockers": []
    }
  ]
}
```

### 2.2 上下文传递协议

会话交接时，Harness 生成标准化的上下文包：

```markdown
# 开发进度摘要（会话交接）

## 已完成功能
- 用户认证（JWT + 基本刷新）
- 商品目录 API（CRUD 完整）

## 当前进行中
- 购物车功能（70% 完成）
  - ✅ 添加商品
  - ✅ 移除商品
  - 🔄 数量更新（进行中）
  - ⏳ 清空购物车（待开始）

## 关键架构决策
- 使用 PostgreSQL 而非 SQLite（理由：生产环境考虑）
- JWT 有效期 15 分钟 + 刷新 Token 7 天
- 所有 API 返回统一的 {data, error, meta} 格式

## 已知问题
- [auth-bug-01] 并发刷新 Token 请求可能产生竞争条件（已记录，暂缓）
- [perf-01] 商品列表查询在 1000+ 商品时 N+1 问题（需要优化）

## 下一步
1. 完成购物车数量更新功能
2. 添加购物车持久化测试
3. 开始订单创建 API
```

### 2.3 智能检查点触发

不是固定时间间隔触发检查点，而是基于语义事件：

```python
def should_create_checkpoint(agent_action):
    CHECKPOINT_TRIGGERS = [
        "feature_complete",      # 完成一个完整功能
        "tests_pass",            # 测试套件通过
        "breaking_change",       # 引入破坏性变更
        "architecture_decision", # 做出重要架构决策
        "context_threshold",     # 上下文窗口 > 70%
    ]
    return agent_action.type in CHECKPOINT_TRIGGERS
```

---

## 三、人机协作协议

### 3.1 三级自主权模型

```
级别 1（完全自主）：日常编码任务
- 添加新功能实现
- 编写测试
- 修复明确的 Bug
→ Agent 自主执行，记录到日志

级别 2（请求确认）：架构性决策
- 添加新依赖
- 修改核心数据结构
- 重构模块
→ Agent 暂停，展示方案，等待人工确认

级别 3（强制人工介入）：高风险操作
- 删除现有功能
- 修改数据库 schema
- 变更认证逻辑
→ Agent 停止，明确请求人工审查
```

### 3.2 中断与恢复

**用户可以在任何时候中断 Agent**，Harness 保证：
- 当前进行中的操作会安全完成或回滚
- 进度状态立即持久化
- 用户可以查看中断点的完整代码状态
- 恢复后 Agent 能从中断点继续（而非重新开始）

---

## 四、质量保障集成

### 4.1 持续验证循环

```
Agent 修改代码 
    → 自动运行单测（快速）
    → 通过？→ 继续下一步
    → 失败？→ 自动进入修复循环
        → 修复尝试 1
        → 修复尝试 2  
        → 超过 3 次失败？→ 触发级别 2 协议（请求确认）
```

### 4.2 技术债务追踪

```markdown
# 技术债务日志

| ID | 问题 | 严重程度 | 估计工作量 | 状态 |
|----|------|----------|------------|------|
| TD-001 | 购物车 N+1 查询 | 中 | 4h | 待处理 |
| TD-002 | 认证竞争条件 | 高 | 8h | 已记录 |
| TD-003 | 缺少 API 速率限制 | 低 | 2h | 待处理 |
```

Harness 确保技术债务在上下文切换时不会丢失。

---

## 五、深度辨析：Harness 工程的第一性原理

### 5.1 状态的三种形态

在应用开发 Harness 中，需要管理三类状态：

**即时状态**（上下文窗口内）：当前正在处理的代码、测试结果、当前错误

**短期状态**（检查点文件）：进行中的功能、最近的决策、活跃的 Bug

**长期状态**（Git 历史 + 文档）：架构演化、所有已做决策的原因、完整测试历史

好的 Harness 使每种状态的信息能在需要时高效访问。

### 5.2 与持续集成（CI）的类比

应用开发 Harness 本质上是"为 AI Agent 定制的 CI/CD 系统"：
- 检查点 ≈ CI 构建
- 特性追踪器 ≈ 项目管理工具
- 验证循环 ≈ 测试流水线
- 人机协作协议 ≈ 代码审查流程

理解这个类比有助于借鉴 CI/CD 领域 20 年积累的最佳实践。

---

## 六、实践建议

1. **设计时考虑会话边界**：假设每 2-3 小时需要一次上下文重置，围绕这个设计状态持久化
2. **让测试充当接口**：在并行开发前先写测试，测试即规范
3. **显式追踪技术债务**：不要依赖 Agent 记住"暂缓处理"的问题
4. **人工介入点要明确**：在 Harness 设计阶段决定哪些操作需要人工确认，而非临时决定

---

*本文分析基于 Anthropic Engineering Blog 原文，写于 2026 年 4 月。*
