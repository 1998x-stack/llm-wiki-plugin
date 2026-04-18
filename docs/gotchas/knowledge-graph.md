# Knowledge Graph Notes

> From docs/gotchas.md #9

---

## 9. 概率论系列与数值分析系列的跨域连接

**已建立的跨域链接（值得注意）：**
- `[[快速傅里叶变换]]` <-> `[[切比雪夫多项式]]`（DCT/谱方法联系）
- `[[Perron-Frobenius定理]]` <-> `[[马尔可夫链]]`（平稳分布存在性）
- `[[谱半径]]` <-> `[[Jacobi迭代法]]`（收敛条件）
- `[[条件数]]` <-> `[[后向误差分析]]`（Wilkinson 传承链）
- `[[CFL条件]]` <-> `[[刘易斯·弗赖·理查森]]`（天气预报失败的根因）

**待补充的跨域连接：**
- `[[中心极限定理]]` <-> `[[正态分布]]`（概率论 <-> 统计学）
- `[[马尔可夫链]]` <-> `[[Krylov子空间方法]]`（两者都与幂法和谱理论相关）
- `[[布朗运动]]`（待创建）<-> `[[偏微分方程]]` / `[[有限元方法]]`

---

## 修复清单（remaining items）

| 优先级 | 任务 |
|--------|------|
| 高 | 完成 ingest files 14-16（file 13 已完成） |
| 中 | 修复断链 `[[马尔可夫]]` -> `[[安德烈·马尔可夫]]` |
| 中 | 修复断链 `[[切比雪夫不等式]]` -> 已创建的同名页面 |
| 低 | 创建 `[[离散傅里叶变换]]` concept 页面 |
| 低 | 标准化来源节格式（bare string -> `[[raw/...]]`）|

---

## #2 — M2: 1552 wiki 页面未映射到任何 topic map

**Status**: New (2026-04-18)

`.claude/topic-to-wiki.json` 仅覆盖 35 个页面，而 wiki 实际有 1566 个页面。`maps/*.md` 虽然列出了更多页面（通过 `[[wikilink]]`），但 `topic-to-wiki.json` 是权威映射源，导致 M2 检查报告 872+ 页面"不属于任何 map"。

**When it bites**: 每次批量 ingest 创建新页面后，新页面自动不被映射。`wiki:reindex` 的 subagent 只分析部分页面生成 topic 映射，覆盖度极低。

**Workaround/Fix**: 运行 `wiki:reindex` 重建 topic-to-wiki.json（但 subagent 覆盖度仍然有限）。或将 M2 检查改为基于 `maps/*.md` 文件中的 `[[wikilink]]` 而非仅依赖 `topic-to-wiki.json`。
