---
type: entity
entity_type: tool
title: "uv"
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [工具, Python, 包管理器, 工具与框架]
aliases: ["uv包管理器", "astral/uv"]
relates_to:
  - target: "[[Bun-Runtime]]"
    type: compares_to
    confidence: 0.95
  - target: "[[Python]]"
    type: part_of
    confidence: 0.9
supersedes: null
---

# uv

## 概述
uv 是 Python 生态的一体化包 & 环境管理器，用 Rust 实现，由 Astral（Ruff 团队）开发，2024 年首发。定位为"Ca[[ripgrep|rg]]o for Python"，统一替代 pip + venv + pyenv + pipx + poetry 碎片化工具链。

## 关键内容

1. **性能基准**：JupyterLab 全量安装冷缓存比 pip 快 8-10x（2.6s vs 21.4s）；有缓存时快 80-115x（~0.2s）；`uv venv` 比 `python -m venv` 快 80x。
2. **功能覆盖**：包安装（替代 pip）、虚拟环境管理（`uv venv`）、跨平台依赖锁定（`uv.lock` TOML格式）、Python 版本管理（内置，无需 pyenv）、全局工具安装（`uv tool install` / `uvx`，替代 pipx）、项目初始化（`uv init`）、PEP 723 单文件脚本内联依赖、发布到 PyPI（`uv publish`）、Ca[[ripgrep|rg]]o-style Workspaces。
3. **架构设计**：全局 wheel 缓存 + CoW/硬链接；PubGrub 解析算法（确定性，跨平台）；人类可读 `uv.lock`（TOML）；内置 Python 安装管理。
4. **适用场景**：新建 Python 项目彻底告别碎片化工具链、CI/CD pip 安装成为瓶颈、AI/ML 工程（LangChain/FastAPI/LLM 管线）、多 Python 版本并存、Claude Code/AI agent 自动化 Python 项目。
5. **局限**：不处理系统级非 Python 依赖（CUDA/cuDNN 等仍需 Conda）；相比 Poetry 在 PyPI 发布语义版本管理上略弱；v0.9.x 仍在快速迭代阶段。

## 来源
- [[raw/articles/programming/cli-tools/bun-vs-uv.md]] — Bun vs uv 跨语言深度对比

## 相关
- [[Bun-Runtime]] — compares_to（JS 生态对标工具，同代精神）
- [[Python]] — part_of
