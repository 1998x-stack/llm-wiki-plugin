# Claude 开发者平台的高级工具使用

> **原文**：[Introducing advanced tool use on the Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use)
> **发布日期**：2025 年 11 月 24 日
> **类别**：工具使用 · API 功能 · 开发者平台

---

## 摘要

本文介绍了 Anthropic 开发者平台的高级工具使用功能，包括并行工具调用、工具选择控制和更丰富的工具定义能力。这些功能使开发者能够构建更高效、更精确的 Agent 系统，是平台能力的重要升级。

---

## 一、并行工具调用（Parallel Tool Use）

### 1.1 顺序 vs 并行

**顺序工具调用**（旧行为）：
```
Turn 1: Claude 调用 get_weather("北京")
Turn 2: 收到天气结果，调用 get_weather("上海")
Turn 3: 收到天气结果，综合两者回答
```

**并行工具调用**（新能力）：
```
Turn 1: Claude 同时调用 get_weather("北京") 和 get_weather("上海")
Turn 2: 同时收到两个结果，综合回答
```

**延迟改善**：原本需要 N 次网络往返的操作，现在只需 1 次——对于多步骤任务，延迟可降低 50-80%。

### 1.2 Claude 如何决定是否并行

Claude 会分析工具调用之间是否存在依赖关系：
- **独立查询**（可并行）：查询不同城市的天气、查询不同产品的价格
- **依赖查询**（必须顺序）：先搜索用户 ID，再用 ID 查询用户详情

这种判断是模型层面的推理，不需要开发者显式声明依赖关系。

---

## 二、工具选择控制

### 2.1 tool_choice 参数

新增的 `tool_choice` 参数让开发者精确控制工具选择行为：

```python
# 让 Claude 自己决定是否使用工具（默认）
tool_choice={"type": "auto"}

# 强制 Claude 使用至少一个工具
tool_choice={"type": "any"}

# 强制使用特定工具
tool_choice={"type": "tool", "name": "get_weather"}

# 完全不使用工具（即使定义了工具）
tool_choice={"type": "none"}
```

### 2.2 应用场景

**强制使用特定工具**：
- 确保 Agent 总是将计划写入文件（`tool_choice={"type": "tool", "name": "save_plan"}`）
- 确保格式化输出总是通过专用工具（避免直接文本输出的格式不一致）

**禁用工具**：
- 在对话的特定阶段只需要文本响应
- 降低成本（工具定义消耗 token，禁用时节省）

---

## 三、更丰富的工具定义

### 3.1 工具结果缓存

对于返回相同结果的工具调用（如获取配置、查询静态数据），可以启用工具结果缓存：

```python
tools=[{
    "name": "get_config",
    "description": "获取系统配置",
    "input_schema": {...},
    "cache_control": {"type": "ephemeral"}  # 在会话内缓存结果
}]
```

### 3.2 工具错误处理

新的工具结果格式支持更丰富的错误信息：

```python
# 成功
{
    "type": "tool_result",
    "tool_use_id": "toolu_01",
    "content": "Weather: 25°C, sunny"
}

# 失败（Claude 可以据此适应策略）
{
    "type": "tool_result", 
    "tool_use_id": "toolu_01",
    "is_error": true,
    "content": "API rate limit exceeded. Retry after 60 seconds."
}
```

Claude 会根据错误类型调整策略：等待重试、使用备用工具、或告知用户。

---

## 四、工具的高级模式

### 4.1 工具链（Tool Chaining）

结合并行工具调用和顺序依赖，Claude 可以自动构建复杂的工具调用图：

```
用户："分析一下 Apple 和 Google 最近的股价，并与整体市场对比"

Claude 的工具调用计划：
Step 1（并行）：
  - get_stock_price("AAPL")
  - get_stock_price("GOOGL")  
  - get_market_index("S&P500")

Step 2（依赖 Step 1 结果）：
  - calculate_correlation(aapl_data, market_data)
  - calculate_correlation(googl_data, market_data)

Step 3（综合所有结果）：
  - 生成分析报告
```

### 4.2 工具组合模式

**分工专业化**：不同工具处理不同类型的数据
- `read_file` 工具：读取文件
- `execute_code` 工具：处理数据
- `write_file` 工具：保存结果

**验证循环**：工具调用 → 检查结果 → 决定是否重试

---

## 五、性能考量

### 5.1 工具 token 成本

工具定义消耗 token——大型工具集的成本不可忽视：

优化策略：
- 按功能分组，每次只提供相关工具（减少 token 消耗）
- 使用 `tool_choice={"type": "none"}` 在不需要工具的步骤跳过工具定义

### 5.2 并行 vs 顺序的选择

并行工具调用节省延迟，但每个工具调用都有网络开销。对于快速、轻量级的工具，顺序调用可能总延迟更低（避免并行协调开销）。

---

## 六、结论

高级工具使用功能是 Anthropic 开发者平台向"生产级 Agent 基础设施"演进的重要一步。并行工具调用直接解决了 Agent 的延迟瓶颈，工具选择控制给了开发者精确的行为控制，更丰富的工具定义让错误处理和缓存成为可能。

这些功能共同推动 Agent 从"实验室玩具"走向"可靠的生产工具"。

---

*本文分析基于 Anthropic Engineering Blog 原文，写于 2026 年 4 月。*
