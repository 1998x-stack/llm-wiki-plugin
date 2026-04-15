---
description: "重建知识库索引，按主题分类到 maps/ 目录"
---

# wiki:reindex

将 index.md 拆分为按主题分类的索引文件，存储在 maps/ 目录下。

## 流程

1. **执行重建脚本**
   - 执行：`Bash: cd vault && python3 scripts/build_reindex.py`
   - 解析 JSON 输出获取分类信息

2. **报告分类结果**
   - 读取每个 maps/*.md 文件
   - 报告：
     - 主题名称和页面数量
     - 总页面数
     - 与上一次快照的差异（如有）

3. **完整性验证**
   - 读取 `maps/tmp.snapshot.json`
   - 对比 wiki/ 目录下实际文件
   - 检查是否有遗漏或多余的页面
   - 如有问题 → 报告并建议修复

4. **更新 log.md**
   - 追加条目：
     ```
     ## [YYYY-MM-DD HH:MM] reindex
     - 重建索引: N 个页面, M 个主题分类
     - 分类: 数值分析(15), 概率论(12), ...
     ```
