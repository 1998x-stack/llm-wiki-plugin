---
type: concept
status: active
confidence: 0.8
created: 2026-04-19
updated: 2026-04-19
last_accessed: 2026-04-19
source_count: 1
tags: [数据结构, 算法, 安全]
aliases: [Trie, 字典树, 前缀树]
relates_to:
  - target: "[[ExecPolicy]]"
    type: implements
    confidence: 0.95
  - target: "[[Codex CLI]]"
    type: uses
    confidence: 0.7
supersedes: null
---

# 前缀树（Trie）

一种树形数据结构，按序列元素逐层分支，用于高效的前缀匹配。在 [[ExecPolicy]] 中，规则在加载时构建为前缀树，实现 O(k) 时间的命令匹配（k = 命令 token 数）。

## 关键内容

1. **在 [[ExecPolicy]] 中的结构**：
   ```
   git
   ├── log      → allow
   ├── status   → allow
   ├── push
   │   ├── --force  → forbidden
   │   └── *        → prompt
   └── commit   → prompt
   ```
   每个命令 token 是树的一层节点，叶子节点标注决策（allow/prompt/forbidden）。

2. **优先级规则**：
   - **更长前缀优先**：`git push --force` 匹配到更深的 `--force` 节点，优先于浅层的 `push` 节点
   - **first-match**：同层多个规则时，先匹配者生效
   - **无匹配 fallback**：树中无路径时，回退到 `approval_policy` 全局设置

3. **为什么选 Trie 而非正则/字符串匹配**：
   - O(k) 确定性匹配，无回溯，无性能退化
   - 天然支持"更具体规则优先"的语义
   - 易于可视化和调试（树结构直观）
   - 加载时一次性构建，执行时纯读取，零运行时开销

4. **与 host_executable 的结合**：Trie 匹配命令前缀后，`--resolve-host-executables` 进一步验证可执行文件的绝对路径，防止 PATH 欺骗攻击。

## 来源

- [[raw/articles/ai-tools/codex/04_codex_execpolicy.md]] — 第 3.1 节：前缀树匹配

## 相关

- [[ExecPolicy]] — implements，ExecPolicy 规则评估的核心数据结构
- [[Codex CLI]] — uses，通过 ExecPolicy 间接使用
