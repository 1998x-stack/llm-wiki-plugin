# LLM Wiki Plugin

> 基于 git worktree 的多类别 LLM Wiki 生成框架

## 架构

```
llm-wiki-plugin/
├── (main)          # master 分支 - 项目入口/索引
├── raw-data-agent  # worktree: agent 类 raw data (分支: raw-data-agent)
├── raw-data-dl     # worktree: 深度学习类 raw data (分支: raw-data-dl)
└── ...
```

## 用法

每个 worktree 是一个独立的分支，存放不同类别的 raw data。
从 raw data 生成对应的 wiki 内容。

### 添加新的 worktree

```bash
git worktree add raw-data-<category> -b raw-data-<category>
```
