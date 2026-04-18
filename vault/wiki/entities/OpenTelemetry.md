---
type: entity
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["技术", "工具", "可观测性", "工具与框架"]
aliases: [OTLP, OpenTelemetry Protocol]
relates_to:
  - target: "[[Codex配置系统]]"
    type: uses
    confidence: 0.75
supersedes: null
---

# OpenTelemetry

开源可观测性框架，提供标准化的遥测数据采集、导出和分析能力，支持 traces、metrics、logs 三种信号类型。

## 概述

CNCF 旗下的统一可观测性标准，定义了 OTLP（OpenTelemetry Protocol）作为遥测数据传输协议，被广泛应用于[[分布式系统]]的监控和调试。

## 关键内容

1. **三种信号类型**：Traces（请求链路追踪）、Metrics（指标聚合）、Logs（结构化日志），统一采集框架
2. **OTLP 协议**：标准的遥测数据传输协议，默认 gRPC 端口 4317，HTTP 端口 4318
3. **在 [[Codex CLI|Codex]] 中的集成**：[[Codex CLI]] 通过 `[telemetry]` 配置段支持 OTLP exporter，自动记录 session_id、model、tool call 耗时、approval 决策等事件，便于审计和性能分析

## 来源

- [[raw/articles/ai-tools/codex/08_codex_config_system.md]] — Codex CLI 深度解析 Vol.8：Config System

## 相关

- [[Codex配置系统]] — uses
- [[Codex CLI]] — uses
