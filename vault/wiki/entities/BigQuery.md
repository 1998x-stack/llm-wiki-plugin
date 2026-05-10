---
type: tool
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [cloud-computing, big-data, analytics]
aliases: ["Google BigQuery", "谷歌大数据分析平台"]
relates_to:
  - target: "[[Data Scientist Agent]]"
    type: used_by
    confidence: 0.7
  - target: "[[SQL]]"
    type: supports
    confidence: 0.9
supersedes: null
---

# BigQuery

## 概述
[[Google]] Cloud的大[[数据分析]]平台，允许用户使用SQL查询海量数据集，无需管理基础设施，按需付费。

## 关键内容

1. **核心特性**：
   - 无[[服务]]器架构，无需管理基础设施
   - 大规模并行处理（MPP）架构
   - 按使用量付费模式
   - 与[[Google]] Cloud生态系统深度集成

2. **主要功能**：
   - 使用标准SQL进行[[数据分析]]
   - 支持多种数据导入导出方式
   - 内置机器学习功能（BigQuery ML）
   - 实时数据流处理能力

3. **常用命令**：
   - 运行查询：`bq query --use_legacy_sql=false 'SELECT ...'`
   - 导出结果：`bq query --use_legacy_sql=false --format=csv 'SELECT ...' > results.csv`
   - 查看表结构：`bq show --schema dataset.table`

## 来源
- [[data-scientist.md]] — BigQuery命令行工具使用方法

## 相关
- [[SQL]] — 查询语言
- [[数据分析]] — 应用领域
- [[Data Scientist Agent]] — 主要使用平台
- [[Google Cloud]] — 云平台