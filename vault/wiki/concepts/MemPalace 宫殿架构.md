---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [memory-architecture, six-layer, spatial-organization, retrieval-optimization]
aliases: [Palace Architecture, 六层记忆结构, Wing-Room-Hall-Drawer-Tunnel-Closet]
relates_to:
  - MemPalace
  - 记忆宫殿
  - 渐进式加载
  - 隧道跨域连接
  - AAAK 方言
supersedes: null
---

# MemPalace 宫殿架构

## 概述
[[MemPalace]] 的六层空间记忆结构：Wing（域隔离）→ Room（主题分区）→ Hall（类型分类）→ Drawer（原始存储）→ [[隧道跨域连接|Tunnel]]（跨域连接）→ Closet（压缩摘要），实现检索准确率从 60.9% 到 94.8% 的提升。

## 关键内容
- **Wing（翼）**：最顶层域，代表人、项目或宏观话题。如 `my_app/`（项目 Wing）、`alice/`（人物 Wing）、`emotions/`（默认话题 Wing）。是最强的隔离边界，确保不同上下文永不混淆
- **Room（房间）**：Wing 内的主题分区。项目 Wing 映射到代码结构（auth、billing、deployment）；对话 Wing 通过关键词评分决定（5 大分类约 56 个关键词，无 LLM 调用）。检测优先级：文件夹路径 → 文件名 → 内容关键词评分 → 默认 general
- **Hall（大厅）**：每个 Room 内 5 个标准 Hall，代表信息性质：facts（客观事实）、events（发生的事件）、discoveries（发现与洞见）、preferences（偏好与风格）、advice（建议与经验）。提供类型过滤能力
- **Drawer（抽屉）**：最终[[记忆细胞|存储单元]]，存原始文本一字不改。块大小 800 字符，重叠 100 字符，优先段落边界切块。每个 Drawer 有完整元数据（wing、room、hall、source_file、timestamp 等），通过 MD5 hash 去重
- **[[隧道跨域连接|Tunnel]]（隧道）**：当同一 Room 名称出现在多个 Wing 中时自动建立跨域连接。解决传统 RAG 无法跨域发现关联的问题，结构自然涌现，无需人为建立连接
- **Closet（壁橱）**：存放 [[AAAK 方言]]压缩的摘要（~120 tokens 可加载数月上下文），用于快速导航。AI 先读 Closet 判断 Room 内容，再决定是否深入 Drawer 取原文
- **检索流程**：问题 → 识别 Wing（缩小到人/项目）→ 识别 Room（缩小到主题）→ 识别 Hall（缩小到类型）→ 在 Drawer 中精确搜索。每一级缩窄都在剪枝噪声

## 来源
- [mempalace_02_palace_architecture.md](/raw/articles/ai-tools/mempalace/mempalace_02_palace_architecture.md) — MemPalace 深度解析第二篇

## 相关
- [[MemPalace]] — part_of
- [[记忆宫殿]] — extends
- [[渐进式加载]] — implements
- [[隧道跨域连接]] — part_of
- [[AAAK 方言]] — uses
- [[分层记忆系统]] — compares_to
