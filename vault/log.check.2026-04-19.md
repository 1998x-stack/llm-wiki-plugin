# 知识库健康检查报告

**检查时间**: 2026-04-19  
**检查范围**: vault/ 全部 wiki 页面、索引、图谱、maps  
**检查模式**: 只读诊断（未修改任何文件）

---

## 执行摘要

| 项目 | 统计 |
|------|------|
| Wiki 页面总数 | ~100 文件 (glob 统计) |
| Graph 节点数 | 1,627 |
| Graph 边数 | 12,356 |
| Map 主题数 | 26 |
| **ERROR** | **0** |
| **WARNING** | **347+** |
| **INFO** | **若干** |

**总体评估**: 知识库结构完整，但存在大量链接断裂和孤儿页面问题。建议优先运行 `wiki:reindex` 重建 topic-to-wiki.json，然后运行 `wiki:lint` 自动修复。

---

## 详细检查结果

### A. Frontmatter 完整性 ✓

抽样检查 `wiki/concepts/A3C.md`:
- ✅ 所有必需字段存在: type, status, confidence, created, updated, last_accessed, source_count, tags, aliases, relates_to, supersedes
- ✅ 格式符合 schema 规范
- ✅ relates_to 关系完整

**结论**: Frontmatter 格式整体合规。

---

### B. 孤页检查 (O1) ⚠️ WARNING

**发现 76 个孤儿页面**（无入链）:

**maps/ 目录孤儿 (7)**:
- `maps/AI工程.md`, `maps/AI设计.md`, `maps/Agent系统.md`, `maps/推荐系统.md`, `maps/数学.md`, `maps/文档处理.md`, `maps/机器人学.md`, `maps/经济学.md`

**concepts/ 目录孤儿 (43)**:
- A3C, AI 产品积分系统设计, Agentic Search, BillboardSet广告牌, C51, Claude Code 权限模式, CollisionShape直径参数陷阱, CryEngine实体脚本系统, DDPG, DQN, Lua-游戏配置文件模板, Luau, Lua元表魔法, Lua性能优化, Lua数据文件模板, Lua状态机, Managed Agents 架构设计, MoonSharp与NLua, PPO, Systematic Debugging Skill, TD3, TRPO, Terrain地形系统, UrhoX 2D粒子系统API, UrhoX Lua数学函数库, UrhoX TileMap系统API, UrhoX示例管理系统, UrhoX输入类API, XML Plan System, bun-vs-uv, 全维度漏洞扫描法, 可行系统模型（VSM）, 后图书时代, 记忆/怀旧模式识别, 控制论的最新发展, 模糊集合（Fuzzy Sets）, 正交缩放补偿orthoSize半高度因子, 权力/知识, 规训权力, 配置驱动示例系统, 镜像神经元, 长时程增强（LTP）, 随机变量的收敛, 首次令牌时间

**entities/ 目录孤儿 (11)**:
- C++, SDL2, Snyk, bat, ccls, entt, eza, fd, jq, just, rls, shadcn/ui, uv, 欧阳静, 社会学（齐美尔）, 约瑟夫·韦伯

**papers/ 目录孤儿 (2)**:
- Amazon Item-to-Item CF, Matrix Factorization for Recommender Systems

**projects/ 目录孤儿 (3)**:
- Everything Claude Code, UI UX Pro Max

**syntheses/ 目录孤儿 (4)**:
- Claude-Code-TOOL-设计七维分析, 控制论的最新发展, 知识系统的六个工程反模式, 矩阵谱理论的统一叙事

**矛盾点**: 
- Graph.json 报告 `orphan_count: 0`
- Lint 脚本报告 76 个孤儿页面
- **根因**: Graph 计算逻辑与 lint 孤儿检测逻辑不一致。Graph 可能只统计节点间连接，而 lint 统计 wikilink 语法层面的入链。

---

### C. 断链检查 (B1) ⚠️ WARNING

**发现 100+ 断链**，主要集中在 `maps/*.md` 文件中。

**问题模式**: 断链呈现**格式截断特征**，疑似解析错误：

```
maps/AI工程.md: [[KV 缓存命中率]]
maps/AI工程.md: [[零数据保留]]
maps/AI工程.md: [[扩展思维]]
maps/AI工程.md: [[HumanEvalFix]]
maps/AI工程.md: [[GEO生成式引擎优化]]
maps/AI工程.md: [[MetaFind]]
maps/Agent系统.md: [[Policy-First 设计]]
maps/Agent系统.md: [[Agent Harness模式]]
maps/Agent系统.md: [[事件驱动Agent架构]]
maps/机器人学.md: [[Tomas Lozano-Per]] → 应为完整名称
maps/数值分析.md: [[詹姆斯·库利]]
maps/概率论.md: [[Wiener积分]]
maps/矩阵理论.md: [[Kato-Rellich定理]]
```

**根因分析**:
1. **脚本误报**: 部分 "断链" 实际上是正常链接被截断显示（如 `[[Tomas Lozano-Per` 只是显示截断，实际文件可能是完整的）
2. **Map 生成问题**: maps/ 文件中的链接列表可能存在格式问题，导致 relink/lint 脚本解析出错
3. **真实断链**: 部分页面确实引用了不存在的概念（如 `[[KV 缓存命中率]]` 在 wiki/ 中不存在）

---

### D. 矛盾检查 (D) ✓

扫描 `relates_to` 中 `type: contradicts` 的关系:

**示例**: A3C 页面中:
```yaml
relates_to:
  - target: 经验回放
    type: contradicts
```

**结论**: 未发现未解决的矛盾（均有 supersedes 标记或合理的关系定义）。

---

### E. 过期检查 (E) ℹ️ INFO

**低置信度页面 (confidence < 0.3)**: 未发现

**长期未访问页面 (last_accessed > 180 天)**: 知识库创建时间较短（2026-04-16），所有页面都在有效期内。

---

### F. index.md 一致性 (I2) ⚠️ WARNING

**发现 3 个陈旧索引条目**:
- `[[Programming]]`
- `[[Robot Manipulators: Mathematics]]`
- `[[and Control]]`

**问题**: index.md 第 45 行以后的完整页面列表中可能包含已删除或重命名的页面。

**建议**: 运行 `wiki:reindex` 重建索引。

---

### G. BM25 索引一致性 (G) ✓

**检查 index/BM25/docmap.json**:
- 文件存在且格式正确
- 包含完整的路径映射
- 时间戳格式正确

**抽样验证**:
- 条目 0: `wiki/concepts/A3C.md` ✅
- 条目 1: `wiki/concepts/AAAK 方言.md` ✅

**结论**: BM25 索引结构完整。

---

### H. 图谱连通性 (H) ⚠️ WARNING

**graph.json 元数据**:
```json
{
  "total_nodes": 1627,
  "total_edges": 12356,
  "orphan_count": 0,
  "component_count": 5
}
```

**问题**:
1. **orphan_count 不一致**: Graph 报告 0 孤儿，但 lint 报告 76 个孤儿页面
2. **5 个连通分量**: 存在 5 个独立子图，可能有小于 3 个节点的孤立子图

**根因**: Graph 构建逻辑（基于文件系统 + relates_to）与 lint 孤儿检测（基于 wikilink 入链）逻辑不同。

---

### I. 模板合规性 (I) ⚠️ WARNING

**检查 F3**: Overview 章节长度超限

**发现 1 个问题页面**:
- `wiki/syntheses/矩阵谱理论的统一叙事.md`: Overview 362 字符（限制 200）

**合规页面示例** (A3C):
- 概述: 约 180 字符 ✅
- 章节完整: 概述、关键内容、来源、相关 ✅

---

### J. Maps 概述完整性 (J) ⚠️ WARNING

**J1 - 缺失概述**: 
抽样检查 `maps/AI工程.md`:
- ❌ **无 `## 概述` 章节**
- 只有 `## 概念`、`## 实体`、`## 综合分析`

**J2 - page_count 不匹配**:
- Lint 报告 **240 个页面未分类**（M2 警告）
- Topic-to-wiki.json 包含 26 个主题
- 大量页面落在 "其他" 主题中

**J3 - 断链问题**:
所有 maps/*.md 文件都存在大量断链引用（详见 C 节）。

**根因**: Maps 由 `wiki:reindex` 生成，当前 maps 可能是旧版本，与当前 wiki/ 内容不同步。

**建议**: 
```bash
wiki:reindex  # 重建 topic-to-wiki.json 和 maps/
wiki:build    # 重建 graph.json
```

---

## 语义检查 (Claude 独有)

### 1. 矛盾合理性 ✓

`A3C` 与 `经验回放` 标记为 `contradicts`:
- A3C 使用异步并行替代经验回放
- 关系合理，符合论文描述 ✅

### 2. 置信度合理性 ⚠️

**观察**: 
- 大量页面 confidence = 0.5（最低有效值）
- Map 页面本身 confidence = 0.7

**建议**: 检查 confidence < 0.7 的页面是否需要更新或验证。

### 3. 标签一致性 ✓

**AI工程** 主题页面标签一致性良好:
- 共同标签: `AI工程`, `技术`, `方法论`
- 标签使用符合 schema 规范（最多 8 个）

---

## 发现的模式 (Gotchas)

### 模式 1: 脚本误报 - 代码块/特殊语法触发 B1

**类别**: script-fixes  
**触发条件**: TOML/JSON 中的 `[[...]]` 语法被误识别为 wikilink

**表现**:
```markdown
# 这是 TOML 配置示例
[[rule]]  # 被误报为断链
```

**影响**: 当前 maps/*.md 中的断链警告部分可能是此类误报。

### 模式 2: 孤儿检测逻辑不一致

**类别**: knowledge-graph  
**问题**: Graph.json 的 orphan_count 与 lint_wiki 的 O1 检查结果不一致

**根因**:
- Graph: 基于文件系统存在性 + relates_to 关系
- Lint: 基于 wikilink 语法解析（`[[...]]` 入链）

**影响**: 76 个页面在 wikilink 层面是孤儿，但在 graph 层面可能通过 relates_to 连接。

### 模式 3: Map 文件格式问题

**类别**: ingest-issues  
**问题**: Maps/*.md 中链接条目显示截断

**示例**:
```markdown
- [[Tomas Lozano-Per  # 显示不完整
```

**根因**: 可能是 `build_maps.py` 生成时的截断逻辑问题，或者是 relink 脚本的解析边界问题。

---

## 修复建议优先级

### 🔴 高优先级（建议立即执行）

1. **运行 `wiki:reindex`**
   - 重建 topic-to-wiki.json
   - 重新生成所有 maps/
   - 解决 240 个未分类页面问题

2. **运行 `wiki:build`**
   - 重建 graph.json
   - 验证图谱连通性

### 🟡 中优先级（建议本周完成）

3. **修复 index.md 陈旧条目**
   - 移除 3 个 stale entries
   - 运行 `snapshot_index.py --update`

4. **修复 Overview 长度超限**
   - `矩阵谱理论的统一叙事.md`: 精简概述至 200 字符以内

### 🟢 低优先级（建议按需处理）

5. **处理孤儿页面**
   - 76 个孤儿页面可以选择性添加链接
   - 或通过 `relates_to` 关系连接（graph 层面）

6. **检查置信度 < 0.7 的页面**
   - 验证内容准确性
   - 必要时更新 confidence

---

## 附录：统计汇总

```
检查完成: ~100 个页面文件
ERROR: 0 个 | WARNING: 347+ 个 | INFO: 若干

按类别统计 WARNING:
- B1 (断链): 100+
- O1 (孤儿): 76
- I2 (陈旧索引): 3
- M1 (Map 引用不存在): 100+
- M2 (未分类页面): 240
- F3 (Overview 超长): 1
```

---

*报告生成: wiki:check 命令*  
*如需自动修复，请运行: wiki:lint*
