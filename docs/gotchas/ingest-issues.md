# Ingest Issues Gotchas

内容摄取和索引相关的问题。

---

## #1 — M2: 240 页面未分类到任何 Map

**Status**: New (2026-04-19)

**问题描述**:

`lint_wiki.py` 报告 `240 pages not in any map`，包括：
- AI工程, AI设计, APPNP, Adam 论文, Agent-Teams-Pattern, Agent系统 等

**根因分析**:

1. **topic-to-wiki.json 过期**: 这些页面可能是在上次 `wiki:reindex` 之后新建的
2. **主题分配失败**: 某些页面可能因为语义不明确被 LLM 分配为"其他"主题
3. **Map 生成问题**: `build_maps.py` 可能遗漏了某些页面

**When it bites**:
- 用户通过 maps/ 浏览时找不到这些页面
- `wiki:query` 的主题扩展可能无法覆盖这些页面
- 知识组织结构不完整

**Workaround/Fix**:
```bash
wiki:reindex  # 重建 topic-to-wiki.json 和 maps/
```

**预防措施**:
- 新建页面后及时运行 `wiki:reindex`
- 或在 CI 流程中定期运行 reindex

---

## #2 — I2: index.md 陈旧条目

**Status**: New (2026-04-19)

**问题描述**:

`index.md` 包含 3 个陈旧条目：
- `[[Programming]]`
- `[[Robot Manipulators: Mathematics]]`
- `[[and Control]]`

**When it bites**:
- 索引与实际 wiki 内容不一致
- 用户点击这些链接会得到空页面

**Workaround/Fix**:
```bash
# 方法 1: 使用脚本更新
bash scripts/wiki.sh snapshot_index --update

# 方法 2: 作为 wiki:reindex 的一部分自动修复
wiki:reindex
```

**根因**: 页面被删除或重命名后，index.md 未同步更新。

---

## #3 — F3: Overview 章节长度超限

**Status**: New (2026-04-19)

**问题描述**:

根据 `_schema/CLAUDE.md` 质量标准，概述部分应不超过 200 字。

**违规页面**:
- `wiki/syntheses/矩阵谱理论的统一叙事.md`: Overview 362 字符

**When it bites**:
- 影响页面可读性
- 不符合 schema 规范
- 可能在模板渲染时被截断

**Workaround/Fix**:
1. 打开违规页面
2. 精简概述内容至 200 字符以内
3. 将详细内容移至 "关键内容" 章节

---
