---
type: entity
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["技术", "工具", "AI基础设施", "工具与框架"]
aliases: [Ollama]
relates_to:
  - target: "[[Codex配置系统]]"
    type: uses
    confidence: 0.7
  - target: "[[OpenAI]]"
    type: compares_to
    confidence: 0.8
supersedes: null
---

# Ollama

本地大模型运行工具，支持在个人设备上部署和运行开源 LLM（如 Llama、Mistral、Qwen 等），通过本地 API 提供模型推理服务。

## 概述

开源的本地 LLM 推理框架，让用户无需云端 API 即可在本地运行开源大模型。通过 `ollama serve` 启动本地服务，兼容 [[OpenAI]] API 格式。

## 关键内容

1. **本地推理**：支持多种开源模型一键下载运行，自动处理量化、GPU 加速等底层细节
2. **[[OpenAI]] 兼容 API**：提供与 [[OpenAI]] 兼容的 REST API 接口，应用可通过切换 `model_provider = "oss"` 无缝切换到本地模型
3. **在 [[Codex CLI|Codex]] 中的集成**：[[Codex CLI]] 通过 `model_provider = "oss"` 配置项支持 Ollama 作为本地模型 Provider，需先运行 `ollama serve`

## 来源

- [[raw/articles/ai-tools/codex/08_codex_config_system.md]] — Codex CLI 深度解析 Vol.8：Config System

## 相关

- [[Codex配置系统]] — uses
- [[OpenAI]] — compares_to
- [[Codex CLI]] — uses
