---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["e2e-testing", "verification", "agent-pattern", "ralph-loop", "Agent系统"]
aliases: ["E2E Verification Pattern", "外部运行时验证", "端到端验证模式", "Testing Patterns"]
relates_to:
  - target: "[[Ralph Loop]]"
    type: part_of
  - target: "[[浏览器自动化验证]]"
    type: extends
  - target: "[[Puppeteer MCP]]"
    type: uses
  - target: "[[Agent Harness模式]]"
    type: part_of
  - target: "[[PRD 驱动开发]]"
    type: enables
  - target: "[[AGENTS.md 项目约定文件]]"
    type: uses
supersedes: null
---

# E2E 验证模式

## 概述
E2E 验证模式是一组面向 Agent 开发循环的外部运行时验证方法，核心原则是"外部验证，不信任自评估"——LLM 在查看自己写的代码时极易产生确认偏误，唯一可靠的验证是启动真实运行时、执行真实操作、验证真实结果。

## 关键内容

1. **核心原则：外部验证，不信任自评估**：
   - ❌ 错误：让 Agent 阅读自己写的代码并判断"应该能用"
   - ✅ 正确：启动真实浏览器/服务器，执行真实操作，验证真实结果
   - LLM 极容易在查看自己写的代码时产生确认偏误，必须通过外部运行时验证打破这一循环

2. **模式一：[[浏览器自动化验证]]（Dev-Browser Skill / [[Puppeteer MCP]]）**：
   - 最重要的验证手段，适用于所有前端 UI Story
   - 在 CLAUDE.md 中声明 Skill，引导 Agent 使用 dev-browser 或 [[Puppeteer MCP]]
   - 标准流程：打开 localhost:3000 → 模拟用户操作（点击、输入、提交）→ 截图检查 → 验证 acceptanceCriteria
   - [[Puppeteer MCP]] 工具链：`puppeteer_navigate`、`puppeteer_screenshot`、`puppeteer_fill`、`puppeteer_click`、`puppeteer_evaluate`

3. **模式一替代方案：Playwright 独立脚本验证**：
   - 使用 Python Playwright async API 编写独立验证脚本（如 `scripts/verify-story.py`）
   - 按 story-id 索引测试函数，支持单 Story 验证
   - 验证失败时自动保存截图（`debug-{story_id}.png`）辅助调试
   - 输出标准化结果：`RESULT: PASS` 或 `RESULT: FAIL — {error}`

4. **模式二：API 测试（curl 脚本链）**：
   - 对于 API Story，使用 curl 链验证（如 `scripts/verify-api.sh`）
   - 支持认证流程：先登录获取 token，再用 Bearer token 请求受保护端点
   - 响应验证：用 Python 一行脚本解析 JSON 并断言关键字段（如 `assert 'token' in d`）
   - 环境变量支持：`BASE_URL` 可配置，适配不同环境

5. **模式三：自动测试套件集成**：
   - 在 AGENTS.md 中记录测试命令，Agent 每次迭代后运行
   - 全量测试（迭代结束前）：`npm test`、`pytest -v`、`go test ./... -v`、`cargo test`
   - 单文件测试（开发过程中）：针对特定测试文件运行
   - 关键约束：完成 Story 后运行相关测试；破坏已有测试必须提交前修复；2 次尝试内无法修复则 `git revert`

6. **模式四：截图回归测试（Screenshot-Based Regression）**：
   - 保存截图作为回归基准，路径约定：`screenshots/[story-id]-[step].png`
   - 命名规范：`auth-001-register-form.png`、`auth-001-dashboard.png`
   - 用途：调试 + 未来回归对比
   - 清理策略：每次 PR 合并后清理 screenshots/ 目录

7. **验证失败处理树**：
   - 功能实现问题 → Attempt 2 修复 → 重新验证 → 2 次都失败 → `git revert` + 记录 BLOCKED + 下一个 Story
   - 环境问题（数据库连接失败、端口占用等）→ 修复环境 → `bash init.sh` → 重新验证
   - 测试脚本问题（测试本身有 bug）→ 修复测试脚本 → 记录到 AGENTS.md → 重新验证

8. **验证命令速查表**：
   - 前端 Story：`puppeteer_navigate` + `puppeteer_fill` + `puppeteer_click` + `puppeteer_screenshot`
   - API Story：`curl -X POST/GET/PUT/DELETE ... | python3 -c "import json,sys; ..."`
   - 数据库验证：Python 直接查询 session 计数
   - 完整测试套件：`npm test -- --passWithNoTests 2>&1 | tail -20`
   - 服务器健康检查：`curl -s http://localhost:3000 -o /dev/null -w "%{http_code}"`（期望 200）

## 来源
- [[raw/articles/ai-tools/ralph-loop/testing-patterns.md]] — Testing Patterns 完整文档（四种验证模式、失败处理树、命令速查表）

## 相关
- [[Ralph Loop]] — part_of（Ralph 系统的核心验证方法论）
- [[浏览器自动化验证]] — extends（本文是其上位概念，涵盖更多验证模式）
- [[Puppeteer MCP]] — uses（前端验证的底层工具）
- [[AGENTS.md 项目约定文件]] — uses（测试命令和规则记录载体）
- [[PRD 驱动开发]] — enables（验证通过是更新 passes 的前提条件）
- [[Agent Harness模式]] — part_of（Harness 的验证层设计）
