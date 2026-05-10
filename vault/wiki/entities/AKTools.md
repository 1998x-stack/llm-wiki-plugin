---
type: entity
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: ["工具与框架", "API服务", "HTTP接口"]
aliases: ["AKTools", "AKTools HTTP API", "AKShare HTTP API", "FastAPI服务"]
relates_to:
  - target: "[[AKShare]]"
    type: extends
    confidence: 0.8
  - target: "[[FastAPI]]"
    type: built_with
    confidence: 0.9
  - target: "[[HTTP API]]"
    type: provides
    confidence: 0.9
  - target: "[[非Python环境]]"
    type: serves
    confidence: 0.8
  - target: "[[Agent系统]]"
    type: suitable_for
    confidence: 0.7
supersedes: null
entity_type: tool
---

# AKTools

## 概述
AK[[Tool System|Tools]]是[[AKShare]]提供的HTTP API层，基于FastAPI构建，允许非[[Python]]环境调用[[AKShare]]的数据接口。它将[[Python]]财经数据接口转换为RESTful API[[服务]]，便于Go/Java/Node等其他语言环境的系统集成。

## 关键内容

1. **安装部署**：通过`pip install aktools`安装，使用`python -m aktools`命令启动，默认运行在`http://127.0.0.1:8080`地址上，提供Web界面和API接口。

2. **调用方式**：可以通过HTTP请求直接调用[[AKShare]]的所有数据接口，例如`curl "http://127.0.0.1:8080/api/public/stock_zh_a_hist?symbol=000001&period=daily&start_date=20240101&end_date=20241231&adjust=qfq"`。

3. **架构设计**：基于FastAPI框架，提供异步高性能API[[服务]]，支持[[Swagger|Swagger UI]]文档界面，便于开发和调试。

4. **适用场景**：特别适合Agent系统、微[[服务]]架构、多语言混合开发环境，以及需要将财经数据[[服务]]暴露给外部系统的场景。

5. **集成优势**：解决了非[[Python]]环境无法直接使用[[AKShare]]的问题，实现了财经数据[[服务]]的跨语言共享，提升了系统的灵活性和可扩展性。

6. **Docker支持**：支持Docker一键部署，便于在容器环境中运行，适合Agent系统集成和生产环境部署。

## 来源
- [[raw/assets/finance-knowledge/akshare-skill/SKILL.md]] — AKTools HTTP API介绍
- [[raw/assets/finance-knowledge/akshare.md]] — AKShare深度分析报告

## 相关
- [[AKShare]] — extends
- [[FastAPI]] — built_with
- [[HTTP API]] — provides
- [[非Python环境]] — serves
- [[Agent系统]] — suitable_for