---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [技术, 工具]
aliases: [Codex ExecPolicy, 策略即代码, Policy as Code]
relates_to:
  - target: "[[Codex CLI]]"
    type: implements
    confidence: 0.95
  - target: "[[Codex沙箱系统]]"
    type: extends
    confidence: 0.9
  - target: "[[Codex TUI]]"
    type: uses
    confidence: 0.8
supersedes: null
---

# ExecPolicy

[[Codex CLI]] 的命令审批引擎，位于 [[Codex沙箱系统]] 之前。将"哪些命令允许、哪些需要审批、哪些禁止"从硬编码逻辑中解放出来，变成**可版本化、可测试、可共享的策略声明文件**——即 Policy as Code。

## 核心思想

传统做法是硬编码黑名单（脆弱、无法共享）。ExecPolicy 改为结构化规则文件（TOML），支持：
- 版本控制（提交到 Git 与团队共享）
- 内置单元测试（load time 自动验证）
- 三态决策：`allow` / `prompt` / `forbidden`

## 规则语法

每条规则包含以下字段（TOML 数组表格式）：`name`（规则名）、`prefix`（命令前缀匹配）、`decision`（allow/prompt/forbidden）、`justification`（原因说明）、`match`/`not_match`（load-time 单元测试用例）。

**前缀匹配语法**：prefix 数组内嵌套数组表示"或"——例如 `["git", "log/status/diff"]` 匹配三个 git 只读命令；`["npm/yarn", "install"]` 同时匹配 npm 和 yarn 的 install 命令。

## 三态决策

| 决策 | 行为 |
|------|------|
| `allow` | 直接放行，不触发审批弹窗 |
| `prompt` | 暂停，在 [[Codex TUI]] 显示 Approval Gate，等人类决策 |
| `forbidden` | 直接拒绝，并将 `justification`（含替代方案）返回给 LLM |

**`forbidden` 的工程价值**：LLM 收到 justification 后可自动纠错（如用 `--force-with-lease` 替代 `--force`），形成**自动纠错循环**。

## 规则评估机制

- **前缀树（Trie）匹配**：O(k) 时间（k = 命令 token 数），load 时构建
- **优先级**：更具体的规则优先（更长前缀）；同层 first-match
- **无匹配时**：fallback 到 `approval_policy` 全局设置
- **Host Executable 解析**：`--resolve-host-executables` 绑定绝对路径，防止 PATH 欺骗攻击

## 规则文件层次

```
/etc/codex/rules/           # 系统级（企业 IT 管理员）
{project}/.codex/rules/     # 项目级（提交 Git，团队共享）
~/.codex/rules/             # 用户级（个人偏好）
```

高优先级覆盖低优先级。项目级规则提交仓库，新成员 clone 后自动获得一致的安全策略。

## 与 approval_policy 的关系

```
approval_policy = "never"     # 全局全自动
+ rule: git push → prompt     # 具体规则覆盖全局
```

具体规则 > 全局 policy。

## 调试

```bash
# 检查命令会触发哪条规则（不实际执行）
codex execpolicy check --rules ~/.codex/rules/safe.rules git push --force
# → {"decision": "forbidden", "matched_rule": "...", "justification": "..."}
```

规则文件加载时 `match/not_match` 示例自动运行——规则错误在启动时就被捕获。

## 工程哲学

> **ExecPolicy 把安全策略从"运行时判断"变成了"编译时声明"**。规则在加载时验证，在执行时机械应用。没有临时判断，没有模糊地带。这是把"AI 会不会乱来"的不确定性转化为确定性的关键机制。

## 来源

- `raw/articles/ai-tools/codex/04_codex_execpolicy.md`
