# 并发 Ingest Loop 支持

## 概述

为了支持多个 ingest loop 同时运行，引入了临时状态文件机制。现在可以同时运行多个 claude 或 qwen 引擎的 ingest loop，每个都有自己的状态文件。

## 新架构

- 旧版：`.claude/ingest-loop.local.md` 和 `.claude/ingest-loop-qwen.local.md`
- 新版：`tmp/ingest-loop.local.<n>.md` 和 `tmp/ingest-loop-qwen.<n>.local.md`

其中 `<n>` 是实例编号，从 1 开始递增。

## 功能脚本

1. **setup-ingest-loop.sh** - 自动查找下一个可用编号并创建状态文件
2. **setup-ingest-loop-qwen.sh** - 自动查找下一个可用编号并创建 Qwen 状态文件
3. **list-ingest-loops.sh** - 列出所有活动的并发循环实例
4. **cancel-ingest-loop.sh** - 取消特定的循环实例

## 工作流程

1. 当启动一个新的 ingest loop 时，设置脚本会扫描 tmp 目录
2. 查找第一个可用的编号（例如，如果没有 .1 或 .2，则使用 .1）
3. 创建相应编号的状态文件
4. 各个循环实例独立运行，互不影响

## 状态文件命名约定

- Claude 引擎: `tmp/ingest-loop.local.<n>.md`
- Qwen 引擎: `tmp/ingest-loop-qwen.<n>.local.md`

## 兼容性

- 旧的状态文件将继续工作但不受新的并发管理工具监控
- 旧的状态文件仍会按原计划在完成后被删除
- 新的并发系统完全向后兼容现有功能