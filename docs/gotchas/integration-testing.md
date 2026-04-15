# Integration Testing Issues

> From docs/gotchas.md #11-14

---

## 11. wiki:graph 非交互模式 max_turns（已修复）

> 2026-04-15 claude -p integration test

**问题**：`wiki:graph` 在 `claude -p` 非交互模式下触达 `max_turns`（30），无法完成。

**根因**：`wiki:graph` 命令的 lint 步骤尝试自动修复断链（Edit wiki 页面），但非交互模式下 Edit 权限被拒，agent 反复重试消耗 turns。

**修复**：采用方案 A — `graph.md` 的 lint 步骤改为只读（只运行 `lint_wiki.py --json` 报告，不自动修复）。Re-test: 9 turns/$0.24 PASS。

---

## 12. lint_wiki.py F4 误报（已修复）

> 2026-04-15 script-level test

**问题**：lint 的 F4（empty section）检查产生 225 个假阳性，将 400 warnings 降至 175 后修复。

**根因**：
1. `#{1,3}` regex 匹配 h1 页面标题（如 `# 牛顿法`），标记 title -> 概述 之间为"空"
2. h2 父节（如 `## 关键内容`）有 h3 子节（如 `### 数学表述`）但之间无文本，被标记为"空"

**修复**：`lint_wiki.py:116` — regex 改为 `#{2,3}`（跳过 h1），h2 有 h3 子节时跳过检查。

---

## 13. `claude -p` 需要 `--allowedTools` 才能运行写入命令（已记录）

> 2026-04-15 integration test round 2

**问题**：`wiki:consolidate`、`wiki:qa-import` 等需要写文件的命令在 `claude -p` 默认模式下因 Edit/Write 权限被拒而失败。

**根因**：`claude -p` 非交互模式默认不授予文件写入权限，每次被拒消耗一个 turn。

**解决**：

```bash
# 写入命令需要显式授权：
claude -p "/wiki:<cmd>" --allowedTools 'Read,Write,Edit,Bash,Glob,Grep' --max-turns 40
```

---

## 14. wiki:graph lint 步骤改为只读（已修复）

> 2026-04-15 integration test

**问题**：`wiki:graph` 命令的 lint 步骤包含自动修复逻辑（修正断链、补全 index），在非交互模式下导致 max_turns 失败。

**修复**：`graph.md` 的 lint 步骤改为只运行 `lint_wiki.py --json` 并报告结果，不做任何自动修复。修复工作交给独立的 `wiki:lint` 命令。

**结果**：graph 命令从 30 turns/$0.90 降至 9 turns/$0.24。
