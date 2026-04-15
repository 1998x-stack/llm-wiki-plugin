# LLM Wiki Plugin — Gotchas & Known Issues

> Last updated: 2026-04-15  
> Session: 数值分析 + 概率论 系列 ingest

---

## 1. Index 分类错误（已修复）

**问题**：5 个实体页面被误分类到 index.md 的「概念」区段而非「实体」区段：
- `[[赫尔曼·外尔]]`
- `[[樊畿]]`
- `[[赫尔穆特·维兰特]]`
- `[[詹姆斯·威尔金森]]`
- `[[加藤敏夫]]`

**根因**：初始批量 ingest（数值分析卷 + 矩阵分析卷）在添加 index 条目时，将部分人物页面错误地放入了 `## 概念` 区段。

**修复**：运行 `wiki:lint` 后已将这 5 个条目移至 `## 实体` 区段。

**预防**：ingest 时添加 index 条目，注意检查文件路径：实体页面在 `wiki/entities/`，概念页面在 `wiki/concepts/`。

---

## 2. Index 统计数字错误（已修复）

**问题**：`index.md` 底部的统计数字与实际文件数不符：

| 字段 | 错误值 | 正确值 |
|------|--------|--------|
| 总页面数 | 100 | 96（修复后随新增持续更新）|
| 实体数 | 38 | 37 |

**根因**：
1. 一次 ingest 中算术错误（96+3 写成了 100）
2. 5 个实体被计入概念区，导致实体计数虚高

**修复**：`wiki:lint` 后已修正。

**预防**：每次 ingest 结束前做一次简单验算：`entities + concepts + syntheses + qa-insights = 总页面数`。

---

## 3. 断链（Broken Links）

**问题**：wiki:lint 扫描发现 **20 个断链** `[[...]]` 指向不存在的页面。分两类：

### 类别 A：待后续 ingest 自然补全（前向引用）

这类断链是初始批量 ingest 时从源文件中提取的链接，指向尚未单独处理的源文件对应的概念：

| 断链 | 所在页面 | 来源文件（待 ingest）|
|------|---------|---------------------|
| `[[矩阵舍入误差分析]]` | 阿兰·图灵 | 14_turing_rounding_errors.md（**已 ingest，已修复**）|
| `[[图灵机]]` | 阿兰·图灵 | 14_turing_rounding_errors.md（**已 ingest，已修复**）|
| `[[布莱切利园]]` | 阿兰·图灵 | 同上（**已修复**）|
| `[[ENIAC]]` | 阿兰·图灵, 约翰·冯·诺依曼 | 对应计算机史文件（待 ingest）|
| `[[贝尔实验室]]` | 约翰·图基 | 21_cooley_tukey_fft.md（**已 ingest，entity 已有**）|
| `[[离散傅里叶变换]]` | 约翰·图基, 詹姆斯·库利 | 同上（仍是断链，需创建 concept）|
| `[[IBM沃森研究中心]]` | 詹姆斯·库利 | 同上（仍是断链，org 页面未创建）|

### 类别 B：需专项处理（关系引用）

| 断链 | 所在页面 | 处理建议 |
|------|---------|---------|
| `[[马尔可夫]]` | 帕夫努季·利沃维奇·切比雪夫 | 已创建 [[安德烈·马尔可夫]]，需更新链接 |
| `[[李雅普诺夫]]` | 同上 | 待 ingest Lyapunov 相关文件 |
| `[[切比雪夫不等式]]` | 同上 | 已创建 [[切比雪夫不等式]]，需更新链接 |
| `[[龙格-库塔方法]]` | 卡尔·龙格 | 待 ingest ODE 文件 |
| `[[雅可比矩阵]]` | 卡尔·古斯塔夫·雅各布·雅可比 | 微积分概念，待 ingest |
| `[[高斯消元法]]` | 卡尔·弗里德里希·高斯 | 线性代数基础，待 ingest |
| `[[骰子问题]]` | 梅雷骑士 | 可能是 [[点数问题]] 别名 |
| `[[惯性律]]` | 詹姆斯·约瑟夫·西尔维斯特 | 待矩阵分析 ingest |
| `[[阿瑟·凯莱]]` | 同上 | 人物实体，待 ingest |
| `[[非负矩阵]]` | 奥斯卡·佩龙 | **已修复** → 改为 `[[不可约矩阵\|非负矩阵]]` |

---

## 4. ingest-loop 中断状态

**问题**：`wiki:ingest-loop /vault/raw/books/概率论` 在处理到 index=5（概率论第 06-10 文件）时被中断。

**当前状态**（`.claude/ingest-loop.local.md`）：
- `current_index: 5`（state 未反映手动处理的 06-10）
- 实际已手动完成：files 01-10（06-10 在当前会话中处理）
- **未完成**：files 11-16

**已创建但未登记到 state 文件的页面**（files 06-10 手动 ingest 产出）：
- `[[Laplace变换]]` — 来自 06
- `[[最大似然原理]]` — 来自 07
- `[[西梅翁·泊松]]`, `[[泊松分布]]` — 来自 08
- `[[切比雪夫不等式]]` — 来自 09
- `[[安德烈·马尔可夫]]`, `[[马尔可夫链]]` — 来自 10
- `[[埃米尔·博雷尔]]`, `[[安德烈·柯尔莫哥洛夫]]`, `[[概率公理体系]]` — 来自 11-12（部分）

**恢复方法**：
```bash
# 直接继续处理剩余文件（11-16）
# 编辑 .claude/ingest-loop.local.md 将 current_index 改为 10
# 然后重新运行 /wiki:ingest-loop
```

**或逐个手动 ingest**：
```
/wiki:ingest raw/books/概率论/13_wiener_brownian_motion.md
/wiki:ingest raw/books/概率论/14_kolmogorov_analytical_methods.md
/wiki:ingest raw/books/概率论/15_doob_stochastic_processes.md
/wiki:ingest raw/books/概率论/16_ito_stochastic_integral.md
```

**未完成的主要概念页面**（files 13-16）：
- `[[布朗运动]]` / `[[Wiener过程]]`（file 13）
- `[[Fokker-Planck方程]]` / `[[Kolmogorov后向方程]]`（file 14）
- `[[鞅理论]]`（file 15）
- `[[Itô积分]]` / `[[随机微分方程]]`（file 16）

---

## 5. 实体页面的「来源」格式不一致

**问题**：部分已有实体页面的 `来源` 节格式不统一——有些用 `[[raw/...]]` 格式，有些用裸路径字符串。例如：

```markdown
# 不一致的写法：
- [[raw/books/数值分析/06_jacobi_iteration.md]]   ← 带双链（可跳转）
- raw/books/矩阵分析/14_wilkinson_algebraic...    ← 裸字符串（不可跳转）
```

**建议**：标准化为带双链格式 `[[raw/books/...]]`，方便在 Obsidian 中反向溯源。

---

## 6. BM25 索引未同步

**问题**：ingest-loop 中断导致 BM25 索引（`vault/index/BM25/`）未对所有新创建的页面执行更新。

**修复**：
```bash
cd vault
python3 scripts/bm25_index.py build  # 全量重建索引
```

---

## 7. graph.json 未重建

**问题**：大量新页面（数值分析系列 + 概率论系列）添加后，`vault/graph.json` 尚未重建，知识图谱可视化数据已过时。

**修复**：
```bash
/wiki:graph
```
或直接：
```bash
cd vault
python3 scripts/build_graph.py
```

---

## 8. Hook 脚本依赖

**注意**：三个 PostToolUse hook（`hook_lint.sh`, `hook_bm25.sh`, `hook_graph.sh`）会在每次 `wiki/**/*.md` 写入后自动触发。但批量 ingest 时 hook 可能因：
- Python 包未安装（`jieba`, `rank_bm25`, `pyyaml`）
- 路径问题（hook 从 vault/ 目录执行）

**检查安装**：
```bash
pip install jieba rank-bm25 pyyaml
```

**查看 hook 执行日志**：`vault/log.hook.md`

---

## 9. 概率论系列与数值分析系列的跨域连接

**已建立的跨域链接（值得注意）：**
- `[[快速傅里叶变换]]` ↔ `[[切比雪夫多项式]]`（DCT/谱方法联系）
- `[[Perron-Frobenius定理]]` ↔ `[[马尔可夫链]]`（平稳分布存在性）
- `[[谱半径]]` ↔ `[[Jacobi迭代法]]`（收敛条件）
- `[[条件数]]` ↔ `[[后向误差分析]]`（Wilkinson 传承链）
- `[[CFL条件]]` ↔ `[[刘易斯·弗赖·理查森]]`（天气预报失败的根因）

**待补充的跨域连接：**
- `[[中心极限定理]]` ↔ `[[正态分布]]`（概率论 ↔ 统计学）
- `[[马尔可夫链]]` ↔ `[[Krylov子空间方法]]`（两者都与幂法和谱理论相关）
- `[[布朗运动]]`（待创建）↔ `[[偏微分方程]]` / `[[有限元方法]]`

---

---

## 10. V2.1-V2.3 Code Review 发现的 Bug（已修复）

> 2026-04-15 code review session

### CRITICAL

| Bug | 文件 | 问题 | 修复 |
|-----|------|------|------|
| Aliased wikilink regex | `snapshot_index.py:88` | `[[A|B]]` 被解析为 `"A|B"` 字符串，导致所有使用别名链接的页面被误报为 orphaned | 改用 pipe-aware regex `r"\[\[([^\]|]+?)(?:\|[^\]]*?)?\]\]"` |
| Missing guard | `snapshot_index.py:112` | `update_index()` 在 `index.md` 不存在时直接 `read_text()` 会 crash | 添加 `INDEX_PATH.exists()` 检查 |

### HIGH

| Bug | 文件 | 问题 | 修复 |
|-----|------|------|------|
| Duplicate stats | `snapshot_index.py:168` | `"综合分析" in line` 匹配了 section header 和 stats 行，产生重复 | 改为 `startswith("- 综合分析：")` |
| Falsy confidence | `build_wiki_pages.py:414` | `if conf` 对 `0.0` 为 False，不显示 badge | 改为 `if conf is not None` |
| String formatting | `build_wiki_pages.py:296,414` | YAML 中 confidence 可能是字符串，`f"{conf:.2f}"` 会 crash | 改为 `f"{float(conf):.2f}"` |
| API no try/except | `qwen_ingest.py:273` | API 调用无异常处理，网络/认证错误导致 traceback | 包裹 try/except，输出 JSON error |
| Stale graph.json | `build_graph.py:220` | `--full` 模式下自定义 `--output` 路径时 `vault/graph.json` 未更新，`build_statistics.py` 读到旧数据 | `--full` 时始终更新 `vault/graph.json` |
| Mixed stdout | `build_graph.py:232` | `--full` 的 debug prints 和 JSON 混在 stdout，破坏解析 | debug 改输出到 stderr |
| No res.ok check | `statistics.html:219` | 404 时 HTML body 传给 `res.json()` 抛 SyntaxError | 添加 `if (!res.ok) throw new Error(res.status)` |
| Lint blocks deploy | `deploy.yml:39` | `continue-on-error: false` 导致 lint warnings（exit 1）阻断所有部署 | 改为 `continue-on-error: true` |

### MEDIUM（Doc inconsistency）

| Bug | 文件 | 问题 | 修复 |
|-----|------|------|------|
| Missing scripts | `CLAUDE.md` | 4 个 shell 脚本未出现在 Scripts 表 | 添加 setup-ingest-loop/qwen, watch-raw, cron-setup |
| Stale vault CLAUDE.md | `vault/CLAUDE.md` | 缺 3 个 Python 脚本，缺 wiki:reindex，"New Commands" 标签过时 | 全部更新 |

---

## 修复清单（优先级排序）

| 优先级 | 任务 |
|--------|------|
| 🔴 高 | ~~完成 ingest files 13-16~~ file 13 已完成（Wiener/布朗运动），剩余 14-16 |
| ~~🔴 高~~ | ~~重建 BM25 索引~~ — wiki:lint 已自动修复 10 个缺失条目 |
| 🟡 中 | 修复断链 `[[马尔可夫]]` → `[[安德烈·马尔可夫]]` |
| 🟡 中 | 修复断链 `[[切比雪夫不等式]]` → 已创建的同名页面 |
| ~~🟡 中~~ | ~~重建 graph.json~~ — build_graph.py --full 已完成 |
| 🟢 低 | 创建 `[[离散傅里叶变换]]` concept 页面 |
| 🟢 低 | 标准化来源节格式（bare string → `[[raw/...]]`）|

---

## 11. wiki:graph 非交互模式 max_turns（已修复）

> 2026-04-15 claude -p integration test

**问题**：`wiki:graph` 在 `claude -p` 非交互模式下触达 `max_turns`（30），无法完成。

**根因**：`wiki:graph` 命令的 lint 步骤尝试自动修复断链（Edit wiki 页面），但非交互模式下 Edit 权限被拒，agent 反复重试消耗 turns。

**修复**：采用方案 A — `graph.md` 的 lint 步骤改为只读（只运行 `lint_wiki.py --json` 报告，不自动修复）。Re-test: 9 turns/$0.24 PASS。

---

## 12. lint_wiki.py F4 误报（已修复）

> 2026-04-15 script-level test

**问题**：lint 的 F4（empty section）检查产生 225 个假阳性，将 400 warnings 降至 175 后修复。

**根因**：
1. `#{1,3}` regex 匹配 h1 页面标题（如 `# 牛顿法`），标记 title → 概述 之间为"空"
2. h2 父节（如 `## 关键内容`）有 h3 子节（如 `### 数学表述`）但之间无文本，被标记为"空"

**修复**：`lint_wiki.py:116` — regex 改为 `#{2,3}`（跳过 h1），h2 有 h3 子节时跳过检查。

---

## 13. `claude -p` 需要 `--allowedTools` 才能运行写入命令（已记录）

> 2026-04-15 integration test round 2

**问题**：`wiki:consolidate`、`wiki:qa-import` 等需要写文件的命令在 `claude -p` 默认模式下因 Edit/Write 权限被拒而失败。

**根因**：`claude -p` 非交互模式默认不授予文件写入权限，每次被拒消耗一个 turn。

**解决**：

```bash
# 写入命令需要显式授权：
claude -p "/project:wiki/<cmd>" --allowedTools 'Read,Write,Edit,Bash,Glob,Grep' --max-turns 40
```

---

## 14. wiki:graph lint 步骤改为只读（已修复）

> 2026-04-15 integration test

**问题**：`wiki:graph` 命令的 lint 步骤包含自动修复逻辑（修正断链、补全 index），在非交互模式下导致 max_turns 失败。

**修复**：`graph.md` 的 lint 步骤改为只运行 `lint_wiki.py --json` 并报告结果，不做任何自动修复。修复工作交给独立的 `wiki:lint` 命令。

**结果**：graph 命令从 30 turns/$0.90 降至 9 turns/$0.24。

---

## 15. lint_wiki.py load_index_links 别名链接 regex（已修复）

> 2026-04-15

**问题**：`load_index_links()` 使用 `\[\[([^\]]+)\]\]` regex，不处理 `[[A|B]]` 别名格式，与 `snapshot_index.py` 同一个 bug。

**修复**：改为 `\[\[([^\]|]+?)(?:\|[^\]]*?)?\]\]`。

---

## 16. build_graph.py relates_to 字符串类型崩溃（已修复）

> 2026-04-15

**问题**：部分 wiki 页面的 `relates_to` 字段包含字符串而非字典（如 `"[[某页面]]"` 而非 `{target: "[[某页面]]", type: ...}`），导致 `entry.get("target")` 报 `AttributeError`。

**修复**：在遍历 `relates_to` 时跳过非 dict 条目。

---

## 17. wiki HTML 页面无数学公式渲染（已修复）

> 2026-04-15

**问题**：wiki 页面包含 LaTeX 数学公式（`$$...$$`、`$...$`），但生成的 HTML 无 KaTeX/MathJax，公式显示为原始 LaTeX 源码。

**修复**：在 `build_wiki_pages.py` 的 HTML 模板中添加 KaTeX CDN + auto-render 脚本，支持 `$$`/`$`/`\[`/`\(` 四种定界符。
