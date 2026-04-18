---
type: concept
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["agent-pattern", "verification", "state-consistency", "Agent系统"]
aliases: ["Dual Verification", "双重验证", "信号+状态交叉验证", "防撒谎验证"]
relates_to:
  - target: "[[完成信号机制（Completion Signal）]]"
    type: extends
  - target: "[[Ralph Loop]]"
    type: used_by
  - target: "[[PRD 驱动开发]]"
    type: depends_on
  - target: "[[Session 交接机制]]"
    type: relates_to
supersedes: null
---

# 双重验证（Dual Verification）

## 概述
双重验证是一种防止 Agent 虚假报告完成状态的交叉验证机制，通过同时检测[[完成信号机制（Completion Signal）|完成信号]]和验证 prd.json 实际状态，确保 Agent 的声明与实际进度一致。

## 关键内容

1. **核心问题**：Agent 可能会输出[[完成信号机制（Completion Signal）|完成信号]]但 prd.json 里还有未完成的 Story。原因包括：
   - Agent 误判任务已完成
   - Agent 在接近上下文极限时草率输出信号
   - Agent 实现有缺陷但自认为通过

2. **双重验证逻辑**：
   ```bash
   # Step 1: 检测文本信号
   if grep -q "$COMPLETION_SIGNAL" "$output_file"; then
     # Step 2: 验证 prd.json 实际状态 (防止 Agent 撒谎)
     if all_stories_complete; then
       echo "✅ VERIFIED: signal + prd both confirmed"
       exit 0
     else
       echo "⚠ Signal found but prd.json has pending stories, continuing..."
     fi
   fi
   ```

3. **验证的两个维度**：
   - **声明层**：Agent 输出的 `[[完成信号机制（Completion Signal）|<promise>COMPLETE</promise>]]` 信号——Agent 的"主观声明"
   - **事实层**：prd.json 中所有 Story 的 `passes: true` 状态——系统的"客观事实"

4. **不一致时的处理**：当信号存在但 prd.json 仍有 pending Story 时，系统不退出循环，而是继续启动下一个 Agent 实例。这确保了即使 Agent 误报，整体进度不会丢失。

5. **与 [[PRD 驱动开发]] 的关系**：双重验证依赖 prd.json 作为"唯一真实状态来源（Single Source of Truth）"。prd.json 的 `passes` 字段是客观验证的基础，而非 Agent 的主观判断。

6. **在 [[Ralph Loop]] 中的应用**：`ralph.sh` 外循环在每次迭代结束后执行双重验证。只有信号和 prd.json 同时确认完成，才 `exit 0` 退出整个循环。

7. **设计哲学**：信任但验证（Trust but Verify）。Agent 被设计为诚实工作，但系统层面必须有防错机制。这是自主 Agent 系统可靠性的关键保障。

## 来源
- [[raw/articles/ai-tools/ralph-loop/how-the-loop-works.md]] — Ralph Loop 核心原理深度解析

## 相关
- [[完成信号机制（Completion Signal）]] — extends（双重验证是完成信号机制的安全保障）
- [[Ralph Loop]] — used_by（Ralph Loop 外循环的核心验证逻辑）
- [[PRD 驱动开发]] — depends_on（依赖 prd.json 作为客观事实验证源）
- [[Session 交接机制]] — relates_to（prd.json 是交接文件之一，双重验证确保其可信度）
