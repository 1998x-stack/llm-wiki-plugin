---
type: log
---

# 操作日志

## [2026-05-18 build]
- 知识图谱: 3071 节点, 25178 边, 3 孤页, 17 连通分量
- Keywords: 10579 个 (2817 titles + 5771 aliases + 1991 tags)
- 同步: graph.json + graph-statistics.json + wiki HTML (3071 页)
- Top 连接: 计算(684), 算法(370), Claude Code(336), 规范化理论(248), 推荐系统(220)

## [2026-05-18 relink]
- 术语词典: 8276 个
- 扫描: 2870 个页面
- 修改: 770 个页面, 4016 条新链接

## [2026-05-18 reindex]
- 完整性: OK (3013 页面, 0 缺失, 26 孤条目 — 均为 vault root maps/ 文件，已知行为)
- 主题分类 (auto-classify): 26 个 topics — 原有 1568 页保留 + 541 页 tag 匹配 + 924 页 keyword 匹配 → 3033，去重至 3013
  - AI工程: 706, 推荐系统: 270, 社会科学: 220, 机器学习: 205, 计算理论: 142, 经济学: 120, 工具与框架: 110, 游戏开发: 108, Agent系统: 101, 信息论: 71, 概率论: 70, 数值分析: 65, 脑科学: 65, 机器人学: 59, 天文学: 55, 时间序列: 55, LLM能力: 53, 强化学习: 46, 文档处理: 46, Lua编程: 38, AI设计: 37, 矩阵理论: 36, 深度学习: 26, 控制论: 22, C++编程: 14, 其他: 273
- Tags 修复: 1343 个页面补充了 topic 标签
- Maps: 26 个 map 文件生成 → maps/
- Index: 精简为 46 行（统计表 + 名称列表）
- Schema 同步: _schema/CLAUDE.md Topics 已更新
- 快照: .claude/reindex.snapshot.json (3013 pages)

## [2026-05-18 lint]
- 扫描: 3024 个页面
- ERROR: 6 → 0 | WARNING: 4660 → 4167
- 自动修复: 8 个
  - F2 (invalid frontmatter): 修复 6 页 YAML 未闭合引号 — `FLP不可能性定理`, `Multi-Paxos`, `TLS协议`, `状态机复制`, `统计套利`, `醉汉遛狗类比`
  - F/I1 (index out of sync): 运行 snapshot_index --slim 重建 index.md，499 未入索引页面 → 6
- 未修复（跳过）:
  - B1 (3580 broken links): 大部分为 map 截断链接 + 正常内容演变，需 wiki:reindex + wiki:relink
  - M1 (125 map broken links): 需 wiki:reindex 重建 maps
  - M2 (1479 unmapped pages): 需 wiki:reindex 重建 topic-to-wiki.json
  - O1 (225 orphan pages): 需 wiki:relink 自动链接
  - F3 (212 overview too long): 需人工精简
  - F4 (13 frontmatter misc issues): 需人工处理

## [2026-04-20 ingest: paper_03_alexnet.md]
- 源文件: raw/articles/ai-papers/foundations/paper_03_alexnet.md
- 新建实体: wiki/entities/李飞飞.md, wiki/entities/NVIDIA.md, wiki/entities/NeurIPS.md, wiki/entities/百度.md, wiki/entities/Facebook.md, wiki/entities/DNNresearch.md, wiki/entities/斯坦福大学.md, wiki/entities/Facebook AI Research (FAIR).md, wiki/entities/ILSVRC.md, wiki/entities/NEC-UIUC.md, wiki/entities/ISI.md, wiki/entities/ZFNet.md
- 新建概念: wiki/concepts/GPU训练.md, wiki/concepts/迁移学习.md, wiki/concepts/手工特征工程.md, wiki/concepts/Top-5 错误率.md, wiki/concepts/最大池化（Max Pooling）.md, wiki/concepts/Softmax.md
- 更新: wiki/concepts/AlexNet.md, wiki/concepts/ReLU激活函数.md, wiki/concepts/Dropout（随机失活）.md, wiki/concepts/局部响应归一化（LRN）.md, wiki/concepts/数据增强（Data Augmentation）.md, wiki/concepts/过拟合（Overfitting）.md, wiki/concepts/Momentum（动量）.md, wiki/entities/Geoffrey E. Hinton.md, wiki/entities/Alex Krizhevsky.md, wiki/entities/Ilya Sutskever.md, wiki/entities/ImageNet Classification with Deep Convolutional Neural Networks (2012 论文).md
- BM25: 24 页面索引更新
- Snapshot: updated (1925 entries)

## [2026-04-21 ingest: paper_03_alexnet.md 补遗]
- 源文件: raw/articles/ai-papers/foundations/paper_03_alexnet.md
- 新建实体: wiki/entities/PyTorch.md
- 新建概念: wiki/concepts/SIFT.md, wiki/concepts/HOG.md, wiki/concepts/PCA颜色增强.md, wiki/concepts/特征可视化.md
- 更新: wiki/entities/Alex Krizhevsky.md (新增源), wiki/entities/Ilya Sutskever.md (新增源), wiki/concepts/卷积神经网络（CNN）.md (新增 AlexNet 演化内容、relates_to、源)
- BM25: 5 页面索引更新
- Snapshot: updated (1935 entries)

## [2026-04-20 ingest: paper_04_batchnorm.md]
- 源文件: raw/articles/ai-papers/foundations/paper_04_batchnorm.md
- 新建: wiki/concepts/Instance Normalization.md, wiki/concepts/Group Normalization.md
- 更新: wiki/concepts/Batch Normalization.md (新增理论争议、归一化变体对比表、relates_to), wiki/concepts/Layer Normalization.md (新增归一化方法对比、relates_to 结构化), wiki/entities/Sergey Ioffe.md (新增训练/推理双模式设计、实验验证), wiki/entities/Christian Szegedy.md (新增 BN 实验数据), wiki/entities/Batch Normalization: Accelerating... (2015 论文).md (新增理论争议、归一化变体启发、relates_to)
- BM25: 4 页面索引更新
- Snapshot: updated (1919 entries)

## [2026-04-20 ingest: 013-得物面试]
- Updated: wiki/得物.md (dates), wiki/细粒度视觉识别.md (dates), wiki/多模态融合.md (dates), wiki/类目负责制.md (dates), wiki/AI替代率.md (dates)
- All 5 pages already existed with content from this source
- BM25: 5 pages indexed
- Snapshot: updated (1899 entries)

## [2026-04-20 ingest: 007-美元霸权深度解析]
- Created: wiki/美元霸权.md (synthesis), wiki/布雷顿森林体系.md (concept), wiki/特里芬难题.md (concept), wiki/去美元化.md (concept)
- Updated: wiki/concepts/石油美元体系.md (source_count 1→2, confidence 0.5→0.7, added relates_to)
- BM25: 5 pages indexed
- Snapshot: updated (1801 entries)

## [2026-04-18 maintain]
- Relink: 4980 terms, 1 new link across 1 page
- Check: 0 errors, 1777 warnings (主要 B1 断链 1344 条，已知问题)，无新 gotchas
- Lint: 修复 40 个 F2 错误 (mixed inline+block YAML frontmatter)
- Build: 1627 节点, 12356 边, 0 孤页, 5 连通分量 → static/ 已同步

## [2026-04-18 reindex]
- 完整性: OK (1621 页面，index.md 已为 slim 格式)
- 快照: 1621 页面 → .claude/reindex.snapshot.json
- 主题分类 (subagent): 762 新页面分类，合并后 26 个 topics → .claude/topic-to-wiki.json
  - 推荐系统(216), 社会科学(122), AI工程(110), 游戏开发(79), 工具与框架(67)
  - Agent系统(70), 计算理论(67), 数值分析(62), 机器学习(58), 机器人学(56)
  - 信息论(51), 概率论(46), 天文学(44), LLM能力(36), 强化学习(35)
  - 文档处理(36), 矩阵理论(32), 经济学(26), Lua编程(25), 控制论(15)
  - 时间序列(15), C++编程(10), 深度学习(10), AI设计(8), 脑科学(23), 其他(252)
- Tags 修复: 305 个页面补充了 topic tags
- Maps: 26 个 map 文件生成 → maps/
- Index: 精简为 46 行（统计表 + 名称列表），覆盖 1581 页
- Schema 同步: _schema/CLAUDE.md Topics 已更新（新增天文学、机器学习、深度学习）

## [2026-04-18] wiki:ingest-loop — raw/articles/ai-tools/claude-skills (35 files)
- 引擎: claude（直接处理模式，子代理模型配置问题）
- 批次处理: 6 个核心文件深入解析 + 批量处理剩余文件
- 总计: 约 30 页面创建, 1 页面更新
- 新建实体: Anthropic, Claude Code, Snyk, GSD, Vercel, OpenAI Codex, Cursor, Gemini CLI, shadcn/ui
- 新建概念: Agent Skills, Context Rot, Context Engineering, AI Slop, frontend-design Skill, web-artifacts-builder Skill, MCP, Wave Execution, Superpowers, writing-plans Skill, Multi-Agent Orchestration, subagent-driven-development Skill, XML Plan System, UI Design Contract, TDD Skill, Systematic Debugging Skill, Git Worktree
- 新建项目: UI UX Pro Max, Everything Claude Code
- 更新页面: Agent Skills（追加 claude-skills 相关信息）
- BM25: 全部新建/更新页面索引 + snapshot_index --update (1423+ entries)

## [2026-04-18] wiki:ingest-loop — raw/articles/ai-tools/ralph-loop (9 files)
- 引擎: claude (子代理并行，最多3并行)
- Batch 1: AGENTS.md → 4 created, 2 updated | CLAUDE.md → 6 created, 2 updated | coding-agent.md → 0 created, 5 updated
- Batch 2: context-strategies.md → 7 created, 2 updated | how-the-loop-works.md → 5 created, 3 updated | initializer-agent.md → 1 created, 3 updated
- Batch 3: prd-generator-prompt.md → 3 created, 2 updated | SKILL.md → 2 created, 2 updated | testing-patterns.md → 1 created, 4 updated
- 总计: 29 页面创建, 25 页面更新
- 新建实体: Next.js, Prisma, PostgreSQL, Puppeteer MCP, Geoffrey Huntley
- 新建概念: AGENTS.md 项目约定文件, PRD 驱动开发, Agent 迭代循环, Session 交接机制, 浏览器自动化验证, Initializer Agent, 上下文策略, Dumb Zone, 固定栈分配, 子 Agent 卸载, 观察遮蔽, 上下文预算管理, Clean State Protocol, 愚钝区（The Dumb Zone）, 固定提示栈（Fixed Prompt Stack）, 完成信号机制（Completion Signal）, 双重验证（Dual Verification）, 子 Agent 模式（Sub-Agent Pattern）, PRD 生成提示词, User Story 粒度原则, prd.json 格式规范, 工作台 vs 长期记忆, E2E 验证模式
- 更新页面: Ralph Loop(多次), Claude Code, Agent Harness模式, Context-Engineering, Context Engineering, PRD 驱动开发, Agent 迭代循环, Session 交接机制, 上下文腐烂, 浏览器自动化验证, Puppeteer MCP, AGENTS.md 项目约定文件
- BM25: 全部新建/更新页面索引 + snapshot_index --update (1627 entries)

## [2026-04-18] wiki:ingest-loop — raw/articles/ai-tools/codex (8 files)
- 引擎: claude (子代理并行，最多3并行)
- Batch 1: 01_architecture → 8 created, 0 updated | 02_tui → 0 created, 2 updated | 03_sandbox → 2 created, 5 updated
- Batch 2: 04_execpolicy → 0 created, 5 updated | 05_session_manager → 1 created, 1 updated | 06_mcp_layer → 3 created, 3 updated
- Batch 3: 07_multi_agent → 2 created, 2 updated | 08_config_system → 2 created, 1 updated
- 总计: 18 页面创建, 19 页面更新
- 新建实体: OpenAI, Rust, TypeScript, Tokio, Landlock, seccomp, Apple Sandbox, Context7, MCP Inspector, Ollama, OpenTelemetry, Phaser.js
- 新建概念: 三道防线模式, Policy-First 设计, 纵深防御, JSONL格式, Agent可组合性, Agent角色系统
- 更新页面: Codex CLI, Codex TUI, Codex沙箱系统, ExecPolicy, Policy-First 设计, Codex会话管理器, MCP, MCP协议层, Codex配置系统, Codex多Agent调度
- BM25: 全部新建/更新页面索引 + snapshot_index --update (1486 entries)

## [2026-04-18] wiki:ingest — 07_codex_multi_agent.md
- 源文件: raw/articles/ai-tools/codex/07_codex_multi_agent.md
- 新建: wiki/entities/Phaser.js.md (entity: tool), wiki/concepts/Agent角色系统.md (concept)
- 更新: wiki/concepts/Codex多Agent调度.md (新增不确定性降低机制表、Agent角色系统关系), wiki/entities/Codex CLI.md (新增 Agent角色系统关系)
- BM25: 3 页索引更新 + snapshot_index --update (1480 entries)

## [2026-04-17 21:20] maintain
- Relink: 3418 terms, 1058 scanned, 957 new links (291 pages)
- Check: 0 errors, 1003 warnings (B1×698/F3×184/M1×54/O1×61/其他×6), 0 new gotchas
- Lint: index.md rebuilt (1067 pages); SQLite.md F2 YAML修复（supersedes 缩进错误）
- Build: 1073 nodes, 8520 edges, 0 orphans, 7 components → static/ synced

---

## [2026-04-17 21:00] ingest | batch 18-20（最终批次）

**批量处理**：`raw/books/计算机科学/18-20` — 三篇论文的深度精读笔记。

### 文件 18: lamport-paxos.md
**创建了 3 个新页面**：
- `wiki/entities/Paxos 论文.md` — Lamport 1998年发表（初稿1989年），分布式共识奠基之作
- `wiki/concepts/Paxos 算法.md` — 两阶段协议、多数派机制、安全性无条件保证
- `wiki/concepts/FLP 不可能性定理.md` — 异步系统中确定性共识不可能的理论证明

### 文件 19: dean-ghemawat-mapreduce.md
**创建了 4 个新页面**：
- `wiki/entities/MapReduce 论文.md` — Google 三驾马车之一
- `wiki/entities/Jeffrey Dean.md` — Google 核心系统工程师、TensorFlow 主导者
- `wiki/entities/Sanjay Ghemawat.md` — GFS 主要设计者
- `wiki/concepts/MapReduce.md` — Map/Reduce 编程模型，大数据时代的开篇

### 文件 20: vaswani-transformer.md
**创建了 4 个新页面**：
- `wiki/entities/Transformer 论文.md` — Attention Is All You Need，引用量超过13万次
- `wiki/entities/Ashish Vaswani.md` — 论文第一作者
- `wiki/concepts/Transformer 架构.md` — 完全基于注意力的序列转换架构
- `wiki/concepts/自注意力机制.md` — O(1) 路径长度，任意位置直接连接

**矛盾检查**：0 个矛盾发现
**BM25 更新**：8 个页面全部更新成功
**Index 同步**：1067 页（+8 新增）

---

## 批量 ingest 完成总结

**处理范围**：`raw/books/计算机科学/` 全部 20 个文件
**总创建页面**：约 100+ 个新页面（从 993 页增长到 1067 页，+74 页）
**处理时间**：2026-04-17 14:30 - 21:00
**矛盾检查**：0 个矛盾
**失败文件**：0

## [2026-04-17 20:30] ingest | batch 15-17

**批量处理**：`raw/books/计算机科学/15-17` — 三篇论文的深度精读笔记。

### 文件 15: thompson-trusting-trust.md
**创建了 3 个新页面**：
- `wiki/entities/Thompson 信任信任论文.md` — 1984年图灵奖演讲，编译器木马攻击
- `wiki/concepts/供应链安全.md` — 开创的安全研究方向
- `wiki/concepts/可重现构建.md` — 对 Thompson 问题的工程回应

### 文件 16: brooks-no-silver-bullet.md
**创建了 2 个新页面**：
- `wiki/entities/No Silver Bullet 论文.md` — 软件工程中不存在"银弹"
- `wiki/entities/Frederick Brooks.md` — 《人月神话》作者

### 文件 17: berners-lee-www.md
**创建了 6 个新页面**：
- `wiki/entities/万维网提案.md` — 1989年 CERN 内部提案
- `wiki/entities/Tim Berners-Lee.md` — 万维网发明者、2016年图灵奖
- `wiki/concepts/万维网.md` — 基于 URL/HTTP/HTML 的分布式信息系统
- `wiki/concepts/URL.md` — 全球信息空间统一编址
- `wiki/concepts/HTTP.md` — 极简的请求-响应协议
- `wiki/concepts/HTML.md` — 人人都能写的标记语言

**矛盾检查**：0 个矛盾发现
**BM25 更新**：11 个页面全部更新成功
**Index 同步**：1057 页（+11 新增）

## [2026-04-17 20:00] ingest | batch 12-14

**批量处理**：`raw/books/计算机科学/12-14` — 三篇论文的深度精读笔记。

### 文件 12: backus-liberated-von-neumann.md
**创建了 1 个新页面**：
- `wiki/entities/Backus 函数式编程论文.md` — Backus 1978年图灵奖演讲，批判冯·诺依曼范式

### 文件 13: lamport-time-clocks.md
**创建了 6 个新页面**：
- `wiki/entities/Lamport 逻辑时钟论文.md` — 论文实体页：happened-before、逻辑时钟、互斥算法
- `wiki/entities/Leslie Lamport.md` — 分布式系统理论奠基者、2013年图灵奖
- `wiki/concepts/happened-before 关系.md` — 事件之间的因果偏序关系
- `wiki/concepts/逻辑时钟.md` — 不依赖物理时钟的因果追踪机制
- `wiki/concepts/分布式系统.md` — 多台通过网络互联的计算机组成的系统
- `wiki/concepts/向量时钟.md` — 完整捕获因果信息的改进机制

### 文件 14: hoare-csp.md
**创建了 3 个新页面**：
- `wiki/entities/Hoare CSP 论文.md` — 论文实体页：CSP 模型、同步通信、守卫命令
- `wiki/entities/Tony Hoare.md` — 快速排序、Hoare 逻辑、CSP 发明者、1980年图灵奖
- `wiki/concepts/CSP 模型.md` — 通过消息传递而非共享内存实现并发

**矛盾检查**：0 个矛盾发现
**BM25 更新**：10 个页面全部更新成功
**Index 同步**：1046 页（+10 新增）

## [2026-04-17 19:30] ingest | raw/books/计算机科学/11-diffie-hellman-new-directions.md

**来源文件**：`raw/books/计算机科学/11-diffie-hellman-new-directions.md` — Diffie & Hellman 1976年论文《New Directions in Cryptography》的深度精读笔记。

**创建了 13 个新页面**：
- `wiki/entities/Diffie-Hellman 论文.md` — 论文实体页：公钥密码学、DH 协议、数字签名框架
- `wiki/entities/Whitfield Diffie.md` — 公钥密码学共同发明者、2015年图灵奖
- `wiki/entities/Martin Hellman.md` — 公钥密码学共同发明者、2015年图灵奖、DES 批评者
- `wiki/entities/James Ellis.md` — GCHQ 成员，1970年独立提出公钥密码学概念
- `wiki/entities/Clifford Cocks.md` — GCHQ 成员，1973年独立发明类似 RSA 算法
- `wiki/entities/Malcolm Williamson.md` — GCHQ 成员，1974年独立发明类似 DH 方案
- `wiki/concepts/公钥密码学.md` — 加密和解密使用不同密钥的革命性范式
- `wiki/concepts/Diffie-Hellman 密钥交换.md` — 第一个公钥密钥交换协议
- `wiki/concepts/数字签名.md` — 认证性、完整性、不可否认性
- `wiki/concepts/离散对数问题.md` — DH 协议的安全性基础
- `wiki/concepts/单向陷门函数.md` — 公钥密码学的数学基础
- `wiki/concepts/后量子密码学.md` — 量子计算威胁下的新密码学范式
- `wiki/concepts/中间人攻击.md` — DH 协议的主要弱点

**矛盾检查**：0 个矛盾发现
**Lint 验证**：13 新页面 0 ERROR（I1 警告将由 snapshot_index 修复）
**BM25 更新**：13 个页面全部更新成功
**Index 同步**：1036 页（+13 新增）

## [2026-04-17 19:00] ingest | raw/books/计算机科学/10-cerf-kahn-tcp-ip.md

**来源文件**：`raw/books/计算机科学/10-cerf-kahn-tcp-ip.md` — Cerf & Kahn 1974年论文《A Protocol for Packet Network Intercommunication》的深度精读笔记。

**创建了 11 个新页面**：
- `wiki/entities/Vinton Cerf.md` — TCP/IP 共同发明者、"互联网之父"、2004年图灵奖
- `wiki/entities/Robert Kahn.md` — TCP/IP 共同发明者、"互联网之父"、2004年图灵奖
- `wiki/entities/TCP-IP 论文.md` — 论文实体页：网关概念、端到端原则、TCP 机制
- `wiki/entities/Louis Pouzin.md` — CYCLADES 项目领导者，数据报模型启发了 TCP/IP
- `wiki/concepts/TCP-IP.md` — 全球互联网的核心协议族
- `wiki/concepts/端到端原则.md` — 智能在边缘，核心保持简单
- `wiki/concepts/网关与路由器.md` — 连接异构网络的无状态专用设备
- `wiki/concepts/ARPANET.md` — 互联网的前身，1969年投入运行
- `wiki/concepts/分组交换.md` — 互联网的技术基础
- `wiki/concepts/IPv4.md` — 32位地址，约43亿个唯一地址
- `wiki/concepts/拥塞控制.md` — Van Jacobson 1988年引入，防止网络崩溃

**矛盾检查**：0 个矛盾发现
**Lint 验证**：11 新页面 0 ERROR（I1 警告将由 snapshot_index 修复）
**BM25 更新**：11 个页面全部更新成功
**Index 同步**：1023 页（+11 新增）

## [2026-04-17 18:30] ingest | raw/books/计算机科学/09-ritchie-thompson-unix.md

**来源文件**：`raw/books/计算机科学/09-ritchie-thompson-unix.md` — Ritchie & Thompson 1974年论文《The UNIX Time-Sharing System》的深度精读笔记。

**创建了 9 个新页面**：
- `wiki/entities/UNIX 论文.md` — 论文实体页：11页篇幅、11,000+次引用、核心设计
- `wiki/entities/Dennis Ritchie.md` — C 语言发明者、UNIX 共同创造者、1983年图灵奖
- `wiki/entities/Ken Thompson.md` — UNIX 原型开发者、fork 的偶然优雅、1983年图灵奖
- `wiki/concepts/UNIX.md` — 以简洁性、模块化、"一切皆文件"为核心的操作系统
- `wiki/concepts/C 语言.md` — 为了编写 UNIX 而发展起来的系统编程语言
- `wiki/concepts/Multics.md` — UNIX 反叛的对象，"复杂性代价"的经典教训
- `wiki/concepts/操作系统.md` — UNIX 定义了现代操作系统的基因
- `wiki/entities/Brian Kernighan.md` — 《C 程序设计语言》合著者、awk 共同发明者
- `wiki/entities/Doug McIlroy.md` — 管道思想的提出者、Bell Labs UNIX 团队成员

**矛盾检查**：0 个矛盾发现
**Lint 验证**：9 新页面 0 ERROR（初版3个 B1 断链已修复）
**BM25 更新**：9 个页面全部更新成功
**Index 同步**：1012 页（+9 新增）

## [2026-04-17 18:00] ingest | raw/books/计算机科学/08-cook-np-completeness.md

**来源文件**：`raw/books/计算机科学/08-cook-np-completeness.md` — Cook 1971年论文《The Complexity of Theorem-Proving Procedures》的深度精读笔记。

**创建了 10 个新页面**：
- `wiki/entities/Cook NP 完全性论文.md` — 论文实体页：NP 完全性定义、Cook-Levin 定理、历史影响
- `wiki/entities/Stephen Cook.md` — NP 完全性定义者、1982年图灵奖
- `wiki/entities/Leonid Levin.md` — 苏联裔计算机科学家，独立发现 NP 完全性
- `wiki/entities/Richard Karp.md` — 证明了21个经典组合问题的 NP 完全性
- `wiki/concepts/NP 完全性.md` — 计算复杂度理论核心概念，"一荣俱荣、一损俱损"
- `wiki/concepts/Cook-Levin 定理.md` — SAT 是 NP 完全的，证明核心思路
- `wiki/concepts/SAT 问题.md` — 布尔可满足性问题，第一个 NP 完全问题
- `wiki/concepts/P vs NP.md` — 千禧年数学问题，悬赏100万美元
- `wiki/concepts/多项式时间归约.md` — 比较问题复杂度的核心工具
- `wiki/concepts/计算复杂度理论.md` — 研究算法资源需求和内在难度的学科

**矛盾检查**：0 个矛盾发现
**Lint 验证**：10 新页面 0 ERROR（初版1个 B1 断链已修复）
**BM25 更新**：10 个页面全部更新成功
**Index 同步**：1003 页（+10 新增）

## [2026-04-17 17:30] ingest | raw/books/计算机科学/07-codd-relational-model.md

**来源文件**：`raw/books/计算机科学/07-codd-relational-model.md` — Codd 1970年论文《A Relational Model of Data for Large Shared Data Banks》的深度精读笔记。

**创建了 8 个新页面**：
- `wiki/entities/关系模型论文.md` — 论文实体页：关系、关系代数、关系演算、规范化、数据独立性
- `wiki/entities/E.F. Codd.md` — 关系模型发明者、1981年图灵奖得主
- `wiki/concepts/关系模型.md` — 用二维表作为数据统一逻辑表示，取代层次/网状模型
- `wiki/concepts/关系代数.md` — 选择、投影、并、差、笛卡尔积五种基本运算，闭包性
- `wiki/concepts/关系演算.md` — 基于一阶谓词逻辑的声明式查询，与关系代数等价
- `wiki/concepts/数据独立性.md` — 物理数据独立性和逻辑数据独立性，三级模式架构
- `wiki/concepts/规范化理论.md` — 消除数据冗余和更新异常的科学化数据库设计方法
- `wiki/concepts/SQL.md` — 关系模型的标准查询语言，历史上使用最广泛的声明式编程语言

**更新了 1 个已有页面**：
- `wiki/entities/SQLite.md` — 新增关系模型、SQL、Codd 三个 relates_to、source_count 1→2

**矛盾检查**：0 个矛盾发现
**Lint 验证**：8 新页面全部 0 ERROR, 0 WARNING
**BM25 更新**：9 个页面（8 新 + 1 更新）全部更新成功
**Index 同步**：993 页（+8 新增）

## [2026-04-17 17:00] ingest | raw/books/计算机科学/06-dijkstra-goto-considered-harmful.md

**来源文件**：`raw/books/计算机科学/06-dijkstra-goto-considered-harmful.md` — Dijkstra 1968年《Go To Statement Considered Harmful》的深度精读笔记。

**创建了 6 个新页面**：
- `wiki/entities/Go To Statement Considered Harmful 论文.md` — 论文实体页：坐标系论证、核心论点、历史影响
- `wiki/entities/Edsger Dijkstra.md` — 荷兰计算机科学家、1972年图灵奖、结构化编程开创者
- `wiki/concepts/结构化编程.md` — 顺序/选择/循环三种基本控制结构，消除 goto
- `wiki/concepts/意大利面条式代码.md` — goto 导致的控制流混乱，被结构化编程取代
- `wiki/concepts/Bohm-Jacopini 定理.md` — 1966年证明 goto 在表达能力上冗余
- `wiki/concepts/软件危机.md` — 1960年代末软件行业困境，结构化编程的时代背景

**更新了 1 个已有页面**：
- `wiki/concepts/函数式编程.md` — 新增 Dijkstra 关系、新增来源、source_count 1→2

**矛盾检查**：0 个矛盾发现
**Lint 验证**：6 新页面全部 0 ERROR, 0 WARNING
**BM25 更新**：7 个页面（6 新 + 1 更新）全部更新成功
**Index 同步**：986 页（+6 新增）

## [2026-04-17 16:30] ingest | raw/books/计算机科学/05-mccarthy-lisp.md

**来源文件**：`raw/books/计算机科学/05-mccarthy-lisp.md` — McCarthy 1960年论文《Recursive Functions of Symbolic Expressions and Their Computation by Machine, Part I》的深度精读笔记。

**创建了 9 个新页面**：
- `wiki/entities/LISP 论文.md` — 论文实体页：S-表达式、五个基本函数、eval 函数、垃圾回收
- `wiki/entities/John McCarthy.md` — LISP 发明者、"人工智能"术语提出者、1971年图灵奖
- `wiki/entities/Steve Russell.md` — McCarthy 学生，实现第一个 LISP 解释器
- `wiki/concepts/LISP.md` — 世界第二古老的高级编程语言，开创函数式编程范式
- `wiki/concepts/函数式编程.md` — 将计算视为数学函数求值的编程范式
- `wiki/concepts/S-表达式.md` — LISP 的统一数据表示，原子和有序对递归定义
- `wiki/concepts/同像性.md` — 程序和数据共享相同表示，LISP 宏系统的基础
- `wiki/concepts/垃圾回收.md` — 自动内存管理，McCarthy 首次提出
- `wiki/concepts/eval 函数.md` — 用不到一页定义的 LISP 自解释器，"计算机科学史上最美丽的一页"

**更新了 1 个已有页面**：
- `wiki/concepts/λ 演算.md` — 新增 LISP 和函数式编程 relates_to、新增来源、source_count 1→2

**矛盾检查**：0 个矛盾发现
**Lint 验证**：9 新页面 0 ERROR（I1 警告将由 snapshot_index 修复，B1 断链已修复）
**BM25 更新**：10 个页面（9 新 + 1 更新）全部更新成功
**Index 同步**：980 页（+9 新增）

## [2026-04-17 16:00] ingest | raw/books/计算机科学/04-backus-fortran.md

**来源文件**：`raw/books/计算机科学/04-backus-fortran.md` — Backus 等人1957年论文《The FORTRAN Automatic Coding System》的深度精读笔记。

**创建了 6 个新页面**：
- `wiki/entities/FORTRAN 编译器论文.md` — 论文实体页：六阶段编译器架构、性能数据、工程规模、历史影响
- `wiki/entities/John Backus.md` — FORTRAN 之父、BNF 发明者、1977年图灵奖得主
- `wiki/entities/Grace Hopper.md` — 编译器技术先驱、A-0 系统开发者、COBOL 推动者
- `wiki/concepts/FORTRAN.md` — 世界上第一个广泛使用的高级编程语言，专为科学计算设计
- `wiki/concepts/编译器优化.md` — 公共子表达式消除、循环不变量外提、强度削减、寄存器分配等核心技术
- `wiki/concepts/BNF.md` — Backus-Naur Form，描述编程语言语法的形式化表示法

**更新了 1 个已有页面**：
- `wiki/concepts/冯·诺依曼瓶颈.md` — 新增 Backus 图灵奖演讲背景、2 个新 relates_to、新增来源

**矛盾检查**：0 个矛盾发现
**Lint 验证**：6 新页面全部 0 ERROR, 0 WARNING（初版 3 个 B1 断链已修复）
**BM25 更新**：7 个页面（6 新 + 1 更新）全部更新成功
**Index 同步**：971 页（+6 新增）

## [2026-04-17 15:30] ingest | raw/books/计算机科学/03-von-neumann-edvac.md

**来源文件**：`raw/books/计算机科学/03-von-neumann-edvac.md` — von Neumann 1945年报告《First Draft of a Report on the EDVAC》的深度精读笔记。

**创建了 7 个新页面**：
- `wiki/entities/EDVAC 报告.md` — 论文实体页：五大组件架构、核心贡献、署名争议、传播效应
- `wiki/concepts/存储程序计算机.md` — 指令与数据统一存储、取指-解码-执行循环、与图灵机的关系
- `wiki/concepts/冯·诺依曼瓶颈.md` — CPU-内存数据传输瓶颈、历史演变、LLM 时代的回响
- `wiki/entities/J. Presper Eckert.md` — ENIAC/EDVAC 设计者、署名争议核心人物
- `wiki/entities/John Mauchly.md` — ENIAC/EDVAC 设计者、署名争议核心人物
- `wiki/entities/Herman Goldstine.md` — EDVAC 报告分发者、ENIAC 项目军方联络官
- `wiki/entities/Maurice Wilkes.md` — EDSAC 建造者、第一个实用存储程序计算机

**更新了 1 个已有页面**：
- `wiki/entities/约翰·冯·诺依曼.md` — 新增 EDVAC 报告与存储程序计算机完整章节（五大组件、存储程序概念、署名争议、传播效应、从理论到工程的桥梁）、10 个新 relates_to、source_count 3→4

**矛盾检查**：0 个矛盾发现
**Lint 验证**：7 新页面全部 0 ERROR, 0 WARNING（初版 6 个 B1 断链已修复）
**BM25 更新**：8 个页面（7 新 + 1 更新）全部更新成功
**Index 同步**：965 页（+7 新增）

## [2026-04-17 15:00] ingest | raw/books/计算机科学/02-shannon-mathematical-theory-of-communication.md

**来源文件**：`raw/books/计算机科学/02-shannon-mathematical-theory-of-communication.md` — Shannon 1948年论文《A Mathematical Theory of Communication》的深度精读笔记（计算机科学视角）。

**创建了 4 个新页面**：
- `wiki/concepts/信源信道分离定理.md` — 信源编码和信道编码可分别独立优化而不损失性能，为通信系统模块化设计提供理论保障
- `wiki/concepts/渐近等分性 (AEP).md` — 信源编码定理证明的核心数学工具，典型集大小约 2^{nH}
- `wiki/concepts/随机编码论证.md` — Shannon 信道编码定理证明的核心方法，存在性而非构造性证明
- `wiki/entities/Warren Weaver.md` — 1949年与 Shannon 合编《The Mathematical Theory of Communication》，撰写通俗导读

**更新了 9 个已有页面**：
- `wiki/entities/克劳德·香农.md` — 新增论文标题"A" vs "The"的微妙含义、编码理论半世纪征程、3 个新 relates_to、source_count 4→5
- `wiki/concepts/信息与语义分离.md` — 新增 Shannon 1948年明确重述段落、3 个新 relates_to、source_count 1→2
- `wiki/concepts/信息熵.md` — source_count 2→3
- `wiki/concepts/信道容量.md` — source_count 2→3
- `wiki/concepts/信道编码定理.md` — source_count 2→3
- `wiki/concepts/信源编码定理.md` — source_count 2→3
- `wiki/concepts/互信息.md` — source_count 1→2
- `wiki/concepts/通信系统模型.md` — source_count 1→2
- `wiki/concepts/典型序列.md` — source_count 1→2
- `wiki/concepts/信息论.md` — source_count 8→9

**矛盾检查**：0 个矛盾发现
**Lint 验证**：4 新页面全部 0 ERROR, 0 WARNING
**BM25 更新**：14 个页面（4 新 + 10 更新）全部更新成功
**Index 同步**：958 页（+4 新增）

## [2026-04-17 14:30] ingest | raw/books/计算机科学/01-turing-on-computable-numbers.md

**来源文件**：`raw/books/计算机科学/01-turing-on-computable-numbers.md` — Turing 1936年论文《On Computable Numbers, with an Application to the Entscheidungsproblem》的深度精读笔记。

**创建了 6 个新页面**：
- `wiki/entities/库尔特·哥德尔.md` — Godel 不完备定理（1931）、一般递归函数、与 Hilbert 纲领的关系
- `wiki/entities/阿隆佐·邱奇.md` — λ 演算发明者、1936年率先用 λ 演算否定回答判定问题、Turing 博士导师
- `wiki/concepts/判定问题 (Entscheidungsproblem).md` — Hilbert 1928年提出、Church/Turing 1936年独立否定回答、从停机问题的归约
- `wiki/concepts/可计算数.md` — Turing 定义：存在图灵机能逐位输出小数展开的实数；绝大多数实数不可计算
- `wiki/concepts/λ 演算.md` — Church 发明的极简形式系统、与图灵机等价、函数式编程语言理论基础
- `wiki/entities/On Computable Numbers 论文.md` — 论文实体页：四大核心贡献、历史意义、论文信息

**更新了 3 个已有页面**：
- `wiki/entities/大卫·希尔伯特.md` — 新增 Hilbert 形式化纲领与判定问题段落、3 个新 relates_to
- `wiki/entities/约翰·冯·诺依曼.md` — 新增与 Turing 的联系段落、3 个新 relates_to
- `wiki/entities/阿兰·图灵.md` — 新增 7 个 relates_to（哥德尔、邱奇、判定问题、可计算数、λ 演算、论文）

**矛盾检查**：0 个矛盾发现
**Lint 验证**：6 新页面全部 0 ERROR，0 WARNING（On Computable Numbers 页面初版有 3×B1 断链已修复）
**BM25 更新**：9 个页面（6 新 + 3 更新）全部更新成功
**Index 同步**：954 页（+6 新增）

## [2026-04-17 11:30] maintain
- Relink: 3061 terms, 938 scanned, 5 new links (4 pages)
- Check: 0 errors, 987 warnings (B1×683/F3×184/M1×54/O1×61/其他×5), 0 new gotchas
- Lint: index.md rebuilt (948 pages)
- Build: 953 nodes, 7145 edges, 0 orphans, 10 components → static/ synced

---

## [2026-04-17 11:02] maintain
- Relink: 3235 terms, 938 scanned, 0 new links (fully linked)
- Check: 0 errors, 1035 warnings (B1×747/F3×189/I1×1/I2×3/M1×54/M2×1/O1×40), 0 new gotchas
- Lint: index.md rebuilt (948 pages), 0 additional fixes
- Build: 953 nodes, 7697 edges, 0 orphans, 2 components → static/ synced
- Bonus fixes: `build_statistics.py` + `build_wiki_pages.py` confidence string → float 崩溃修复

---

## [2026-04-17 10:43] lint

- 扫描: 953 个页面
- ERROR: 0 | WARNING: 2009 条（含 953×I1 + 23×I2 假阳性，见 gotcha #44）
- 真实问题: ~110 条（B1 学术引用 + M1 地图断链 + F3 概述过长）
- 自动修复: 4 个
  - [F] index.md 重建（`snapshot_index --slim`）→ 948 页，补入全部新增页面
  - [G] BM25 清理 2 个旧条目（`wiki/concepts/untitled.md`, `wiki/entities/UrhoX.md`）
  - [A] `wiki/qa-insights/数值PDE稳定收敛三角.md` 补充 `updated` 字段
  - 新增 gotcha #44（I1/I2 假阳性根因文档化）
- 需要人工处理:
  - `wiki:reindex` 重建 topic-to-wiki.json（849 页未分类，index.md 统计表依然基于旧映射）
  - Codex 系列 5 页缺失章节（概述/关键内容/相关）
  - M1: 54 条 maps 指向不存在页面（地图更新后部分链接失效）
  - B1: 746 条断链（大部分为学术来源 slug 引用，属预期行为）

---

## [2026-04-16 23:30] ingest | raw/articles/ai-engineering/search-retrieval/（19 个文件）

**来源目录**：`raw/articles/ai-engineering/search-retrieval/`（传统搜索引擎 8 篇深度解析 + GEO/SEO + Agentic Search + CLIP + BGE Reranker + Qwen-VL + MetaFind + 代码领域选型框架）

**创建了 15 个新概念页面**：
- `wiki/concepts/搜索引擎架构.md` — 搜索引擎两大管道、核心组件、评分模型演进、评估指标体系
- `wiki/concepts/倒排索引.md` — Posting List、差值编码、SPIMI/MapReduce 构建算法、FST 词典
- `wiki/concepts/TF-IDF.md` — TF/IDF 变体、向量空间模型、余弦相似度、SMART 表示法
- `wiki/concepts/文本预处理.md` — 分词（中英文）、停用词、词干提取、词形还原、同义词扩展
- `wiki/concepts/查询处理.md` — 意图识别、拼写纠错、伪相关反馈、布尔查询 AST、查询松弛
- `wiki/concepts/WAND算法.md` — TAAT/DAAT 对比、WAND 跳过机制、BMW 块级上界、两阶段检索
- `wiki/concepts/索引压缩.md` — VByte、Elias Gamma/Delta、PForDelta、Simple-9、前缀编码、FST
- `wiki/concepts/向量空间模型.md` — 稀疏 vs 稠密向量、余弦 vs 欧氏距离、VSM 演进
- `wiki/concepts/GEO生成式引擎优化.md` — KDD 2024、语义密度/权威信号、AIGVR 指标体系、SEO+GEO 双轨
- `wiki/concepts/SEO搜索引擎优化.md` — 发展历程、四大核心模块、Core Web Vitals、E-E-A-T
- `wiki/concepts/Agentic Search.md` — RAG vs Agentic 对比、ReAct/CRAG/Self-RAG、代码领域优先 Agentic 原则
- `wiki/concepts/学习排序.md` — Pointwise/Pairwise/Listwise、LambdaMART、LTR 特征工程
- `wiki/concepts/Modality Gap.md` — 锥体效应、对比学习缺陷、图转文间接检索是生产最优解
- `wiki/concepts/多模态检索.md` — CLIP 底层、3D 模型渲染检索、混合架构（文本通道+图像通道 RRF）
- `wiki/concepts/Cross-encoder与Bi-encoder.md` — 独立编码 vs 联合编码、大模型重排优势分析

**创建了 1 个新实体页面**：
- `wiki/entities/MetaFind.md` — 元宇宙 3D 资产检索，ESSGNN 场景感知等变图编码，ULIP-2 三模态对齐

**lint 验证**：所有页面 0 ERROR，1 warning（Page not listed in index，已由 snapshot_index 修复）
**BM25 更新**：16 个页面全部更新成功
**index.md 更新**：已同步（909 条目）

## [2026-04-16 22:45] maintain
- Relink: 2622 terms, 862 pages scanned, 新链接（已在 reindex 后添加）
- Check: 145 errors (F2 YAML frontmatter), 1989 warnings — 0 new gotchas
- Lint: 自动修复 145 个 F2 错误（15 missing FM + 76 duplicate inline+block tags + 54 indented duplicates）→ 0 errors
- Build: 884 节点, 7292 边, 0 孤页, 4 连通分量 → static/ 已同步, 884 HTML 页面

## [2026-04-16 22:30] reindex
- 完整性: 742 页面已快照（index.md 格式不兼容，通过 --slim 重建）
- 主题分类 (haiku subagent): 228 个新页面 → 9 个新 topic + 扩展 4 个已有 topic
- 新 topics: 强化学习(30), Lua编程(25), 游戏开发(22), 脑科学(23), 控制论(15), 时间序列(15), 社会科学(17), C++编程(10)
- Topics 总计: 23 个 topics → .claude/topic-to-wiki.json
- Tags 修复: 102 个页面补充了 topic tag
- Maps: 23 个 map 文件生成 → maps/
- Index: 精简为 43 行（统计表 + 名称列表）
- Schema 同步: _schema/CLAUDE.md Topics 已更新（14→23 个 topics）

## [2026-04-16 21:05] ingest-loop | Claude Code 功能文档（92 文件）
- 源路径：raw/assets/claude-howto/
- 处理文件：92 个（10 个主题目录 + 元数据文件）
- 创建页面：8 个概念
  - wiki/concepts/斜杠命令（Slash Commands）.md — 4 类命令（内置/Skills/插件/MCP）、55+ 内置命令速查
  - wiki/concepts/Claude Code 记忆系统.md — 4 层记忆范围（受管策略/项目/用户/本地）、自动加载机制
  - wiki/concepts/渐进式披露（Progressive Disclosure）.md — 三层加载（描述→SKILL.md→支持文件）
  - wiki/concepts/Claude Code 插件系统.md — 4 种插件类型（官方/社区/组织/个人）、一体化打包
  - wiki/concepts/Checkpoints 与 Rewind.md — 快照/回退/分支点、5 种 Rewind 选项
  - wiki/concepts/Claude Code 权限模式.md — 6 种权限级别（default/acceptEdits/plan/auto/dontAsk/bypassPermissions）
  - wiki/concepts/会话分支（Branching）.md — /branch 命令、与 Checkpoints 对比
  - wiki/concepts/上下文压缩（Context Compaction）.md — /compact 命令、与渐进式披露对比

## [2026-04-16 22:00] ingest-loop (qwen) — build123d CAD 建模工具
- 源: raw/assets/build123/ (5 files)
- 引擎: qwen3-plus via DashScope API
- 处理文件:
  - build123d-deep-analysis.md → 8 页 (build123d 深度分析)
  - build123d-skill/SKILL.md → 4 页 (Skill 定义)
  - build123d-skill/references/objects.md → 4 页 (对象参考)
  - build123d-skill/references/operations_enums_tips_assembly.md → 7 页 (操作/枚举/装配)
  - build123d-skill/references/topology.md → 7 页 (拓扑结构)
- 结果: 全部 5 文件 SUCCESS，共提取 30 个 wiki 页面
- 主题: build123d、CAD 建模、OpenCASCADE、参数化设计、拓扑结构
- 状态: 完成

## [2026-04-16 21:00] ingest-loop (qwen) | 规则漏洞学系列（25 文件，13 有内容）
- 源路径：raw/articles/essays/thinking-series/规则漏洞学系列/
- 处理文件：13 个有内容（01-12 + overview），12 个空文件跳过（13-24）
- 引擎：qwen3-plus（Qwen API）
- 创建页面：7 个（1 实体 + 6 概念）
  - wiki/entities/孙宇晨.md — 规则漏洞学典型实践者，ICO 卡点/巴菲特午餐/新概念作文
  - wiki/concepts/规则漏洞学.md — 核心定义、两条红线、三大认知误区、运作机制
  - wiki/concepts/规则的阶层筛选属性.md — 规则双重属性、内卷陷阱、破局路径
  - wiki/concepts/规则的4大先天缺陷.md — 滞后性/不周延性/执行弹性/地域时间差
  - wiki/concepts/人性套利.md — 五大人性弱点（贪婪/猎奇/从众/迷信权威/厌恶损失）
  - wiki/concepts/有限风险无限收益公式.md — 预期净收益公式、风险封顶准则
  - wiki/concepts/全维度漏洞扫描法.md — 3 项前置准备 + 4 步标准化扫描

## [2026-04-16 21:30] ingest-loop (qwen) — ChatGPT 对话记录（7 个对话，39 文件）
- 源: raw/ChatGPT-Chat/ (7 个子目录，39 个 markdown 文件)
- 引擎: qwen3-plus via DashScope API
- 对话主题:
  - Agent Eval 论文推荐 (1 文件)
  - Claude Code TOOL 设计分析 (3 文件)
  - SWE-agent 论文核心观点 (22 文件)
  - Self-Attention 机制解析 (3 文件)
  - Sonnet vs Opus 对比 (3 文件)
  - 文章解读 Anthropic Agent (3 文件)
  - 注意力掩码解析 (4 文件)
- 结果: 39/39 SUCCESS，共提取 ~142 个 wiki 页面
- 主题覆盖: Agent 评估、Claude Code 工具设计、SWE-agent、Self-Attention、LLM 模型对比、Managed Agents、注意力掩码/KV Cache/解码策略
- 状态: 完成

## [2026-04-16 20:55] ingest | 县域体制内的"剩女"——基于中部 D 县的调查（社会学论文）
- 源文件：raw/articles/essays/social/县域体制内的"剩女"——基于中部D县的调查.md
- 创建页面：4 个（1 实体 + 3 概念）
  - wiki/concepts/县域体制内剩女.md — 体制内剩女分布特征、女教师为主体、越剩越多现象、青年人才困境
  - wiki/concepts/择偶梯度理论.md — 女性"上嫁"倾向、县域体制内梯度失衡、与北上广剩女共性
  - wiki/concepts/婚姻挤压理论.md — 体制内性别结构失衡（非总体性别比）、与农村光棍对比
  - wiki/entities/欧阳静.md — 县域治理研究学者，首次发现县域体制内剩女现象

## [2026-04-16 20:35] ingest-loop | 编程文章合集（37 文件）
- 源路径：raw/articles/programming/
- 处理文件：37 个（cli-tools×3 + cpp×6 + lsp×9 跳过(已有) + lua×19）
- 新建页面：~65 个（cli工具×9, C++×15, Lua×41）
- 更新页面：~15 个
- 备注：LSP 9 个文件在前序 session（18:55）已完成，本次跳过
- 引擎：claude（并行子代理，每批 3 个）

## [2026-04-16 20:50] ingest | 为什么国人写不出 CSAPP 级别的好书（知乎多回答）
- 源文件：raw/articles/essays/social/为什么国人写不出一本能平替甚至超越《深入理解计算机系统》的好书？ - Soulflare 的回答.md
- 创建页面：6 个（3 实体 + 3 概念）
  - wiki/entities/深入理解计算机系统（CSAPP）.md — CMU 15-213 课程配套教材，配套实验体系（Bomb Lab/Attack Lab 等），迭代 20 年
  - wiki/entities/Randal E. Bryant.md — CMU 资深教授，CSAPP 合著者
  - wiki/entities/David R. O'Hallaron.md — CMU 教授，CSAPP 合著者，实验体系设计者
  - wiki/concepts/技术出版经济学.md — 写书 ROI 极低（2000-3000 小时投入 vs 8 万版税），机会成本抹杀动力
  - wiki/concepts/学术评价体系.md — 非升即走压力下写教材权重低，追逐短平快热点
  - wiki/concepts/后图书时代.md — 静态书籍跟不上技术迭代，AI+开源源码的交互式学习替代传统阅读

## [2026-04-16 20:45] ingest | 黎叔的硅星人 Pro 采访（TapTap Maker 产品理念）
- 源文件：raw/articles/essays/social/黎叔的硅星人Pro的采访.md
- 创建页面：5 个（3 实体 + 2 概念）
  - wiki/entities/黎叔.md — TapTap Maker 产品负责人，AI 原生游戏开发理念倡导者
  - wiki/entities/TapTap Maker.md — AI 原生游戏引擎，支持 30 万行中型游戏，开发-发布全闭环
  - wiki/entities/嗒啦啦.md — TapTap AI 创作助手，拟人化设计
  - wiki/concepts/AI 原生架构.md — GUI 不适合 AI、技能优于知识、人机共创
  - wiki/concepts/上下文漂移.md — "改A坏B"行业通病，拆会话/组件解耦缓解

## [2026-04-16 20:40] ingest | 应对被动单身：县域体制内大龄女青年的行动策略（社会学论文）
- 源文件：raw/articles/essays/social/应对被动单身：县域体制内大龄女青年的行动策略及其影响——基于中部Y县的实地调研.md
- 创建页面：2 个
  - wiki/concepts/被动单身.md — 概念界定、结构性原因、四种理想类型、对外/对内策略、异变婚恋观、身份再生产机制
  - wiki/concepts/社会行动理论.md — 韦伯理论核心、伯格与卢克曼发展、理想类型方法、意外后果概念

## [2026-04-16 20:35] ingest | AI 产品积分系统设计深度分析
- 源文件：raw/articles/essays/product-design/AI 产品积分系统设计深度分析.md
- 创建页面：1 个
  - wiki/concepts/AI 产品积分系统设计.md — 5 种定价模式、"赌博感"痛点、Agent 循环问题、v0 迁移教训、Builder.io 最佳实践、10 大设计原则、工程架构（原子扣减/Rollover/预估成本）

## [2026-04-16 20:30] ingest | 资源与能力差异（ChatGPT 对话）
- 源文件：raw/articles/essays/product-design/资源与能力差异.md
- 创建页面：1 个
  - wiki/concepts/资源与能力差异.md — 乘法系统模型、归因偏差、资源作为前置条件、生存资本、二阶效应、评价体系盲区、胜者叙事、AI 时代放大效应、问题拥有权、个体策略

## [2026-04-16 20:25] ingest | 随机变量的收敛（Wikipedia 词条）
- 源文件：raw/articles/essays/math/Convergence of random variables.md
- 创建页面：1 个
  - wiki/concepts/随机变量的收敛.md — 6 种收敛概念（依分布/依概率/几乎必然/必然/r阶矩/几乎完全）+ 强度层级 + 关键定理
- 更新页面：0 个

## [2026-04-16 20:20] ingest-loop | 金融数据工具（8 文件）
- 源路径：raw/assets/finance-knowledge/
- 处理文件：8 个（4 个深度分析报告 + 4 个 SKILL.md）
- 新建页面：4 个实体
  - AKShare — 开源全品类财经数据接口库（1000+ 接口，37 分类）
  - Alpha Vantage — NASDAQ 官方授权全球市场数据 API（50+ 技术指标，MCP 原生支持）
  - Baostock — 中国 A 股免费历史数据平台（从 1990 年至今）
  - yfinance — Yahoo Finance 非官方 Python 封装（全球市场，研究/原型首选）
- 引擎：claude（手动处理）

## [2026-04-16 20:15] ingest-loop | RL-Analysis（7 文件）
- 源路径：raw/assets/RL-Analysis/
- 处理文件：7 个（rl_00 ~ rl_06）
- 新建页面：29 个（28 概念 + 1 实体）
- 更新页面：7 个
- 涵盖主题：MDP、价值函数、贝尔曼方程、DQN 系列（Double/Dueling/PER/Rainbow/C51/NoisyNets）、策略梯度系列（REINFORCE/TRPO/PPO）、Actor-Critic 系列（A3C/DDPG/TD3/SAC/最大熵RL）、算法选型指南

## [2026-04-16 20:00] ingest-loop | 控制论书籍（23 文件）
- 源路径：raw/books/控制论/
- 处理文件：23 个（含 3 个综述/趋势文件）
- 新建页面：19 个（17 概念 + 1 综合 + 1 实体更新）
  - 调速器稳定性理论、行为目的与目的论、McCulloch-Pitts 神经元模型
  - 控制论（Cybernetics）、超稳定系统、一般系统论
  - 极大值原理、动态规划、必要多样性定律
  - 二阶控制论、自创生、可行系统模型（VSM）
  - 耗散结构、模糊集合、反向传播
  - 强化学习、控制即推断、强化学习与控制的概率推断视角
  - 控制论的最新发展（synthesis）
- 更新页面：卡尔曼滤波（source_count +1）
- 引擎：claude（手动处理）

## [2026-04-16 21:00] ingest | 脑科学系列论文（13/13 完成）✅
- 源文件夹：raw/books/脑科学/
- 文件总数：13 个 markdown 文件
- 已完成：13/13（100%）
- 创建页面：22 个
  - **实体页面 (10 个)**:
    - wiki/entities/Santiago Ramón y Cajal.md — 现代神经科学之父，神经元学说创立者，1906 年诺贝尔奖
    - wiki/entities/David H. Hubel.md — 视觉皮层研究者，方向选择性发现者，1981 年诺贝尔奖
    - wiki/entities/Torsten N. Wiesel.md — 视觉皮层研究者，关键期发现者，1981 年诺贝尔奖
    - wiki/entities/Karl Deisseroth.md — 光遗传学发明者，斯坦福教授，2021 年拉斯克奖
    - wiki/entities/John O'Keefe.md — 位置细胞发现者，认知地图理论，2014 年诺贝尔奖
    - wiki/entities/Donald O. Hebb.md — 赫布学习律提出者，认知神经科学先驱
    - wiki/entities/Otto Loewi.md — 神经递质发现者，"梦中的实验"，1936 年诺贝尔奖
    - wiki/entities/Eric Kandel.md — 海兔记忆研究者，CREB 发现者，2000 年诺贝尔奖
    - wiki/entities/Luigi Galvani.md — 生物电发现者，电生理学开创者，1791 年
    - wiki/entities/Pierre Paul Broca.md — 布罗卡区发现者，语言定位，功能定位论确立者
  - **概念页面 (12 个)**:
    - wiki/concepts/神经元学说.md — 神经系统由离散细胞单元组成，推翻网状理论，1954 年电子显微镜证实
    - wiki/concepts/视觉皮层.md — V1 区方向选择性、简单细胞/复杂细胞、柱状结构、关键期，启发 CNN 设计
    - wiki/concepts/长时程增强（LTP）.md — 突触可塑性基石，Bliss & Lømo 1973，赫布学习律的实验证明
    - wiki/concepts/镜像神经元.md — 执行和观察同一动作时均放电，Rizzolatti 1996，争议与影响
    - wiki/concepts/光遗传学.md — ChR2 光感蛋白控制特定神经元，Deisseroth 2005，毫秒级精度因果研究
    - wiki/concepts/位置细胞.md — 海马空间地图，O'Keefe 1971，位置场，认知地图神经实现
    - wiki/concepts/网格细胞.md — 内嗅皮层六边形网格，Moser 夫妇 2005，最优几何编码
    - wiki/concepts/赫布学习律.md — "Cells that fire together wire together"，Hebb 1949，LTP 等待 24 年的验证
    - wiki/concepts/神经递质.md — 化学突触传递物质，Loewi 1921 青蛙心脏实验发现，乙酰胆碱是第一个
    - wiki/concepts/CREB.md — 长期记忆分子开关，Kandel 在海兔中发现，cAMP→PKA→CREB→基因转录
    - wiki/concepts/生物电.md — Galvani 1791 年青蛙腿实验发现，开创电生理学，与伏打争论催生电池发明
    - wiki/concepts/布罗卡区.md — 左侧额叶下回 BA44/45，语言产生中枢，Broca 1861 年通过"Tan"病例发现
- BM25: 22 页面全部更新成功
- Index: +22 新条目 (snapshot_index --update)
- 状态：完成 ✅

## [2026-04-16 20:30] ingest | 脑科学系列论文（9/13 完成）
- 源文件夹：raw/books/脑科学/
- 文件总数：13 个 markdown 文件
- 已完成：9/13（69%）
- 创建页面：14 个
  - **实体页面 (6 个)**:
    - wiki/entities/Santiago Ramón y Cajal.md — 现代神经科学之父，神经元学说创立者，1906 年诺贝尔奖
    - wiki/entities/David H. Hubel.md — 视觉皮层研究者，方向选择性发现者，1981 年诺贝尔奖
    - wiki/entities/Torsten N. Wiesel.md — 视觉皮层研究者，关键期发现者，1981 年诺贝尔奖
    - wiki/entities/Karl Deisseroth.md — 光遗传学发明者，斯坦福教授，2021 年拉斯克奖
    - wiki/entities/John O'Keefe.md — 位置细胞发现者，认知地图理论，2014 年诺贝尔奖
    - wiki/entities/Donald O. Hebb.md — 赫布学习律提出者，认知神经科学先驱
  - **概念页面 (8 个)**:
    - wiki/concepts/神经元学说.md — 神经系统由离散细胞单元组成，推翻网状理论，1954 年电子显微镜证实
    - wiki/concepts/视觉皮层.md — V1 区方向选择性、简单细胞/复杂细胞、柱状结构、关键期，启发 CNN 设计
    - wiki/concepts/长时程增强（LTP）.md — 突触可塑性基石，Bliss & Lømo 1973，赫布学习律的实验证明
    - wiki/concepts/镜像神经元.md — 执行和观察同一动作时均放电，Rizzolatti 1996，争议与影响
    - wiki/concepts/光遗传学.md — ChR2 光感蛋白控制特定神经元，Deisseroth 2005，毫秒级精度因果研究
    - wiki/concepts/位置细胞.md — 海马空间地图，O'Keefe 1971，位置场，认知地图神经实现
    - wiki/concepts/网格细胞.md — 内嗅皮层六边形网格，Moser 夫妇 2005，最优几何编码
    - wiki/concepts/赫布学习律.md — "Cells that fire together wire together"，Hebb 1949，LTP 等待 24 年的验证
- BM25: 14 页面全部更新成功
- Index: +14 新条目 (snapshot_index --update)
- 待处理：4 个文件（paper_10 神经递质，paper_11 海兔学习，paper_12 生物电，paper_13 语言区）

## [2026-04-16 20:15] ingest-loop (qwen) — 社会学经典著作
- 源: raw/books/社会学/ (6 files, 含 1 个 HTML 转换)
- 引擎: qwen3-plus via DashScope API
- 处理文件:
  - paper_01_comte_cours.md → 8 页 (孔德、实证主义等)
  - paper_02_marx_manifesto_kapital.md → 8 页 (马克思、阶级理论等)
  - paper_03_durkheim_division_suicide.md → 11 页 (涂尔干、社会分工、自杀论等)
  - paper_04_weber_protestant_ethic.md → 8 页 (韦伯、新教伦理、理性化等)
  - paper_05_goffman_mills.md → 7 页 (戈夫曼、米尔斯、拟剧论等)
  - sociology_history_timeline.md → 16 页 (社会学发展史、各流派)
- 结果: 全部 6 文件 SUCCESS，共提取 58 个 wiki 页面
- 状态: 完成

## [2026-04-16 19:50] ingest-loop | 时间序列分析书籍（17 文件）
- 源路径：raw/books/时间序列分析/
- 处理文件：17 个
  - 01-yule-1927-ar-model.md → 新建 AR 模型
  - 02-wold-1938-decomposition.md → 新建 Wold 分解定理
  - 03-holt-1957-exponential-smoothing.md → 新建 指数平滑
  - 04-kalman-1960-filter.md → 更新 卡尔曼滤波（source_count 1→2）
  - 05-granger-1969-causality.md → 新建 格兰杰因果
  - 06-box-jenkins-1970-arima.md → 新建 ARIMA 模型
  - 07-akaike-1974-aic.md → 新建 AIC（赤池信息准则）
  - 08-engle-1982-arch.md → 新建 ARCH 模型
  - 09-bollerslev-1986-garch.md → 新建 GARCH 模型
  - 10-johansen-1988-cointegration.md → 新建 协整分析
  - 11-hamilton-1989-regime-switching.md → 新建 马尔可夫体制转换模型
  - 12-hochreiter-1997-lstm.md → 新建 LSTM
  - 13-prophet-2017-forecasting-at-scale.md → 新建 Prophet
  - 14-nbeats-2019-neural-basis-expansion.md → 新建 N-BEATS
  - 15-informer-2021-transformer-time-series.md → 新建 Informer
  - 16-dlinear-2023-are-transformers-effective.md → 新建 DLinear
  - 17-patchtst-2023-time-series-worth-64-words.md → 新建 PatchTST
- 新建页面：16 个
- 更新页面：1 个（卡尔曼滤波）
- 引擎：claude（手动处理）

## [2026-04-16 19:45] lint
- 扫描：688 个页面
- ERROR: 146 个 | WARNING: 1528 个 | INFO: 0 个
- 自动修复：146 个 F2 错误（YAML frontmatter 修复）
- 需要人工处理：
  - F3 警告：27 个页面概述超过 200 字符（需手动精简）
  - B1 断链：约 200+ 个（需手动修正或创建缺失页面）
  - I2 过期：15 个 map 文件在 index.md 中（需运行 wiki:reindex 更新）
  - M1/M2 地图：201 个页面未分配到任何地图（需运行 wiki:reindex 重新分类）
  - O1 孤页：12 个（已从 24 个修复至 12 个）

**已自动修复**：
- 146 个 F2 错误：YAML frontmatter 格式修复（添加缺失的 type/status/confidence 等字段）
- index.md 同步：已完成（snapshot_index --update）
- O1 孤页修复 (12 个)：
  - Multi-Agent-Coordination-Patterns → Cara-Phillips
  - Subagents-in-Claude-Code → Chris-Olah
  - Manus/Wide-Research → Meta
  - 提示词缓存 → 令牌计数
  - LSP（语言服务器协议）→ gopls/hls/lua-language-server/vtsls
  - Code-Review-for-Claude-Code → Advisor Tool
  - 脑手分离架构/Managed-Agents → 宠物与牲畜模式
  - ARIMA 模型 → N-BEATS/Prophet/协整分析/马尔可夫体制转换模型
  - LSIF → Semantic Tokens

**待人工处理**：
- 27 个 F3 页面需精简概述至 200 字符以内
- 断链修复：创建缺失页面或修正链接目标
- 地图更新：运行 wiki:reindex 重新分类页面（将解决 10 个 map 孤页）
- 孤页处理：剩余 2 个（Claude-Code-TOOL-设计七维分析.syntheses, LSIF 可能假阳性）

## [2026-04-16 19:10] ingest-loop (qwen) — taptap-maker 技术文档
- 源: raw/articles/game-dev/taptap-maker/ (25 files)
- 引擎: qwen3-plus via DashScope API
- 结果: 全部 25 文件 SUCCESS，共提取 ~95 个 wiki 页面
- 主题: ACP 协议、Agent 客户端架构、Gateway 消息、Skill Hub、语音输入、Monorepo
- 状态: 完成

## [2026-04-16 18:55] ingest-loop | LSP 语言服务器协议调研（9 文件）
- 源路径：raw/articles/programming/lsp/
- 处理文件：9 个
  - 00_lsp_overview.md → 新建 LSP 概念页 + Semantic Tokens + LSIF
  - 01_python_lsp.md → 新建 pyright + pylsp 实体页
  - 02_typescript_lsp.md → 新建 typescript-language-server + vtsls 实体页
  - 03_rust_lsp.md → 新建 rust-analyzer + rls 实体页
  - 04_go_lsp.md → 新建 gopls 实体页
  - 05_cpp_lsp.md → 新建 clangd + ccls 实体页
  - 06_java_csharp_kotlin_lsp.md → 新建 eclipse.jdt.ls + lsp4j 实体页
  - 07_lua_haskell_ruby_php_lsp.md → 新建 lua-language-server + hls 实体页
  - 08_data_markup_lsp.md → 内容已覆盖（JSON/YAML/SQL 等 LSP 工具）
- 新建页面：16 个（3 概念 + 13 实体）
- 引擎：claude（手动处理）

## [2026-04-16 19:00] ingest | claude-blog 批量导入（9 文件）
- 源文件夹：raw/articles/ai-engineering/claude-blog/
- 处理文件：9 个 markdown 文件
- 创建页面：12 个
  - **概念页面 (9 个)**:
    - wiki/concepts/Code-Review-for-Claude-Code.md — Claude Code 多智能体代码审查系统，84% 大 PR 发现问题，平均 7.5 个问题，$15-25/次
    - wiki/concepts/Subagents-in-Claude-Code.md — Claude Code 子智能体使用场景（研究/并行/验证/流水线）和 5 种调用方法（对话/自定义/CLAUDE.md/Skills/Hooks）
    - wiki/concepts/Multi-Agent-Coordination-Patterns.md — 五种多智能体协调模式总览（生成器 - 验证器/协调器 - 子智能体/智能体团队/消息总线/共享状态）
    - wiki/concepts/Generator-Verifier-Pattern.md — 模式 1：生成器→验证器→反馈循环，适用于高质量关键输出
    - wiki/concepts/Orchestrator-Subagent-Pattern.md — 模式 2：层级结构，协调者分配任务给子智能体，Claude Code 采用此模式
    - wiki/concepts/Agent-Teams-Pattern.md — 模式 3：团队成员持续运行积累上下文，适用于独立并行子任务
    - wiki/concepts/Message-Bus-Pattern.md — 模式 4：发布/订阅事件驱动，适用于不断扩展的智能体生态系统
    - wiki/concepts/Shared-State-Pattern.md — 模式 5：共享存储库消除中间环节，适用于协作式研究
    - wiki/concepts/Wide-Research.md — Manus 广泛研究架构，并行子代理解决上下文窗口限制
  - **实体页面 (3 个)**:
    - wiki/entities/Chris-Olah.md — Anthropic 联合创始人，提出"培育"而非"构建"AI 系统的观点
    - wiki/entities/Cara-Phillips.md — 多智能体协调模式文章作者
    - wiki/entities/Meta.md — 2026 年收购 Manus 的公司
- 更新页面：1 个
  - wiki/concepts/提示词缓存.md — 补充 Claude Code 团队 5 条优化经验（前缀匹配/用消息而非修改提示/不中途换模型/不中途改工具/监控命中率）、source_count 3→4
- BM25: 13 页面全部更新成功
- Index: +12 新条目 (snapshot_index --update)
- Lint: 0 errors, 5 warnings (B1 预留链接×3, I1×2 已由 slim index 处理)

## [2026-04-16 18:35] ingest-loop (qwen) — SWE-agent 论文核心观点
- 源: raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/ (22 files)
- 引擎: qwen3-plus via DashScope API
- 结果: 全部 22 文件 SUCCESS，共提取 ~55 个 wiki 页面
- 主题: SWE-agent, ACI, Agent 系统, 软件工程自动化
- 状态: 完成

## [2026-04-16 18:50] reindex
- 完整性: OK (644 页面, 0 缺失, 0 孤条目)
- 主题分类 (subagent): 14 个 topics → 推荐系统(216), AI工程(67), 数值分析(62), 机器人学(56), 信息论(51), 概率论(43), 矩阵理论(32), 经济学(26), Agent系统(24), LLM能力(23), 文档处理(20), 工具与框架(11), AI设计(8), 计算理论(5) → .claude/topic-to-wiki.json
- Tags 修复: 242 个页面补充了 topic tags
- Maps: 14 个 map 文件生成 → maps/
- Index: 精简为 35 行（统计表 + 名称列表）
- Schema 同步: _schema/CLAUDE.md Topics 已更新（16→14 topics, +计算理论, -深度学习/数学/其他）

## [2026-04-16 17:00] ingest | Give Claude a computer: Programmatic Tool Calling (PTC)
- 源文件：raw/articles/ai-engineering/claude-blog/Give Claude a computerGive Claude a computer 给 Claude 一台电脑.md（clipping fragment，12 行）
- 创建页面：2 个
  - wiki/concepts/Programmatic-Tool-Calling-PTC.md — Claude 4.6 新能力：动态构造工具调用，支持运行时决策和参数构造，应用场景（文件编辑 stale check/动态工具选择）
  - wiki/entities/Lance-Martin.md — AI Agent 技术专家，@RLanceMartin，PTC 推广者，Claude 生态系统内容创作者
- 更新页面：2 个
  - wiki/entities/Claude-Opus-4-6.md — 补充 PTC 能力支持、source_count 2→3、新增 2 个 relates_to
  - wiki/entities/Claude-Sonnet-4-6.md — 补充 PTC 能力支持、source_count 2→3、新增 2 个 relates_to
- BM25: 4 页面全部更新成功
- Index: +2 新条目 (Programmatic-Tool-Calling-PTC, Lance-Martin)
- Lint: 0 errors, 5 warnings (B1 预留链接×3, I1×2 已由 slim index 处理)

## [2026-04-16 18:25] ingest-loop | Anthropic Developer Documentation (6 files)
- 源路径：raw/articles/ai-engineering/anthropic-developer/
- 处理文件：6 个
  - Compaction.md → 已有页面（上下文压缩.md），内容已覆盖
  - Context editing.md → 已有页面（上下文编辑.md），内容已覆盖
  - Context windows.md → 已有页面（上下文窗口.md），内容已覆盖
  - Prompt caching.md → 更新 提示词缓存.md（source_count: 2→3）
  - Token counting.md → 新建 wiki/concepts/令牌计数（Token Counting）.md
  - advisor_deep_analysis.md → 新建 wiki/concepts/Advisor Tool（顾问工具）.md
- 新建页面：2 个
- 更新页面：1 个
- 去重跳过：3 个（已有页面覆盖）
- 引擎：claude（手动处理，subagent 未响应）

## [2026-04-16 16:30] ingest | Seeing like an agent: Claude Code 工具设计哲学
- 源文件：raw/articles/ai-engineering/claude-blog/Seeing like an agent_ how we design tools in Claude Code.md
- 创建页面：5 个
  - wiki/entities/Thariq-Shihipar.md — Anthropic 技术人员，Claude Code 工具设计哲学提出者
  - wiki/concepts/AskUserQuestion-Tool.md — 三阶段演进（ExitPlanTool 修改→输出格式→独立工具），模态框 UI 降低回答摩擦
  - wiki/concepts/ExitPlanTool.md — 早期计划生成工具，AskUserQuestion 演进尝试 1 失败案例
  - wiki/concepts/TodoWrite-Tool.md — 早期任务跟踪工具，局限性（僵化清单/子代理协作困难），被 Task Tool 取代
  - wiki/concepts/Task-Tool.md — TodoWrite 替代者（supersedes），从"保持轨道"到"Agent 协调"，支持依赖/跨 Agent 共享/灵活修改
- 更新页面：2 个
  - wiki/concepts/渐进式披露 -Progressive-Disclosure.md — 补充 Claude Code Guide 案例、搜索能力演进（RAG→Grep→Agent Skills）、source_count 1→2
  - wiki/entities/Claude-Code.md — 补充工具设计哲学段落（"像智能体一样观察"、核心工具演进、渐进式披露应用、工具数量控制）、新增 5 个 relates_to、source_count 2→3
- BM25: 7 页面全部更新成功
- Index: +5 新条目 (snapshot_index --update)
- Lint: 0 errors, 12 warnings (B1 预留链接×6, I1×6 已由 slim index 处理)

## [2026-04-16 15:20] ingest | Manus 上下文工程六原则 (官方博客转载)
- 源文件: raw/articles/ai-engineering/claude-blog/AI代理的上下文工程：构建Manus的经验教训.md
- 创建页面: 2 个
  - wiki/entities/Manus.md — Manus 项目实体：技术路线选择（押注上下文工程而非模型训练）、六大原则概览、典型任务特征（50 次工具调用、100:1 输入输出比）、2025 年被 Meta 收购
  - wiki/concepts/KV 缓存命中率.md — KV 缓存命中率概念：为什么对 Agent 特别重要（100:1 输入输出比）、成本影响（10 倍差异）、三大实践（前缀稳定/只追加/缓存断点）、与工具动态变化的冲突
- 更新页面: 2 个
  - wiki/concepts/Context-Engineering.md — 补充 Manus 六原则段落、source_count 4→5
  - wiki/concepts/提示词缓存.md — 补充 Manus 生产环境 KV 缓存最佳实践、source_count 1→2
- BM25: 4 页面全部更新成功
- Index: +2 新条目 (Manus, KV 缓存命中率)
- Lint: 0 errors, 1 warning/page (I1 index listing — 页面已出现在 index entries 中)；KV 缓存命中率 B1 已修复（[[vLLM]] → vLLM 纯文本）

## [2026-04-16 15:10] ingest | Anthropic Skill-Creator 评估框架增强 (官方博客)
- 源文件: raw/articles/ai-engineering/claude-blog/Improving skill-creator_ Test, measure, and refine Agent Skills.md
- 创建页面: 0 个（已有页面可覆盖）
- 更新页面: 1 个
  - wiki/concepts/Agent Skills.md — 补充两种技能类型（能力提升 vs 编码偏好）、Skill-Creator 评估框架（Evals 两大用途）、基准测试模式、多智能体并行评估、对比智能体 A/B 测试、描述优化（精准触发）、展望未来（从"如何做"到"做什么"）、source_count 1→2
- BM25: 1 页面更新成功
- Index: 无新增条目（复用已有页面）
- Lint: 无新页面，跳过

## [2026-04-16 15:00] ingest | Anthropic Effective Context Engineering (官方博文)
- 源文件: raw/articles/ai-engineering/anthropic-engineering/Effective context engineering for AI agents.md
- 创建页面: 0 个（已有页面可覆盖）
- 更新页面: 1 个
  - wiki/concepts/Context-Engineering.md — 补充系统 Prompt Altitude 校准（Goldilocks zone）、工具设计的上下文工程含义（最小可行集、token-efficient 返回）、混合检索策略（Claude Code 典型实现）、来源作者信息、source_count 3→4
- BM25: 1 页面更新成功
- Index: 无新增条目（复用已有页面）
- Lint: 无新页面，跳过

## [2026-04-16 14:45] ingest | Claude Code edit 后 validate 分层设计 (ChatGPT QA)
- 源文件: raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/12-claude code中，edit后做 validate  linting，需要在tool des.md
- 创建页面: 1 个
  - wiki/concepts/Claude Code 分层验证.md — Claude Code 分层验证概念：四层分工（tool description/CLAUDE.md/hooks/LSP）、为什么不能只靠单一层面、与 SWE-agent 对比、落地四步
- 更新页面: 2 个
  - wiki/concepts/Edit 后验证.md — 补充 Claude Code 分层验证方案段落、新增来源、source_count 2→3
  - wiki/entities/Claude-Code.md — 补充 Edit 后验证分层段落、新增来源和关系、source_count 1→2
- BM25: 3 页面全部更新成功
- Index: +1 新条目 (Claude Code 分层验证)
- Lint: 0 errors, 1 warning (I1 index listing — 页面已出现在 index entries 中)

## [2026-04-16 14:35] ingest | edit validate ablation study (ChatGPT QA)
- 源文件: raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/11-SWE-agent 是否对 edit 是否 validate 做了 ablation study？有.md
- 创建页面: 0 个
- 更新页面: 2 个
  - wiki/concepts/Edit 后验证.md — 补充 Ablation Study 证据（Table 3：w/ linting 18.0 vs edit action 15.0 vs No edit 10.3）、两层结论、source_count 1→2
  - wiki/concepts/Ablation Study.md — 补充新来源、source_count 3→4
- BM25: 2 页面全部更新成功
- Index: 无新增条目（复用已有页面）
- Lint: 无新页面，跳过

## [2026-04-16 14:25] ingest | edit后lint/lsp validate设计 (ChatGPT QA)
- 源文件: raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/10-swe-agent 每次 edit后，如何设计lintlsp 等validate？.md
- 创建页面: 1 个
  - wiki/concepts/Edit 后验证.md — Edit 后验证概念：SWE-agent 实现（USE_LINTER + flake8 单文件检查）、增量诊断设计（previous errors filtering）、三层 validate 架构建议、LSP 触发策略、observation 返回格式
- 更新页面: 2 个
  - wiki/concepts/Guardrails.md — 补充 LSP 增量诊断作为 Guardrail 的扩展方向、三层 validate 架构、source_count 3→4
  - wiki/entities/SWE-agent.md — 补充 Edit 后验证段落（linter 实现、previous errors filtering）、source_count 1→2
- BM25: 3 页面全部更新成功
- Index: +1 新条目 (Edit 后验证)
- Lint: 0 errors, 1 warning (I1 index listing — 页面已出现在 index entries 中)

## [2026-04-16 14:10] ingest | trajectory常见字段 schema (ChatGPT QA)
- 源文件: raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/08-trajectory常见字段 schema包含哪些，分别什么意思，分别如何构造.md
- 创建页面: 2 个
  - wiki/entities/SWE-agent.md — SWE-agent 项目实体：核心架构、SWE-bench 表现、trajectory 格式、工程化建议
  - wiki/concepts/Trajectory Schema.md — Trajectory Schema 概念：顶层字段、step 级字段（response/thought/action/observation/state/query）、message→query 版本差异、6 步构造流水线、分析友好增强字段
- 更新页面: 1 个
  - wiki/concepts/Agent 轨迹分析.md — 补充 Trajectory Schema 关系、新增来源、source_count 1→2
- BM25: 3 页面全部更新成功
- Index: +2 新条目 (SWE-agent, Trajectory Schema)
- Lint: 0 errors, 1 warning/page (I1 index listing — 已由 snapshot_index 处理，页面已出现在 index entries 中)

## [2026-04-16 12:40] ingest | SWE-agent 轨迹分析方法论 (ChatGPT QA)
- 源文件: raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/07-SWE-agent 轨迹 格式长什么样，怎么进行分析，怎么判断轨迹中哪些问题导致了后续任务的失败？.md
- 创建页面: 1 个
  - wiki/concepts/Agent 轨迹分析.md — 轨迹格式（Figure 9 + .traj JSON）、四层分析法、根因链诊断框架、失败模式分类（7 类）
- 更新页面: 4 个
  - wiki/concepts/ReAct 风格循环.md — 补充轨迹分析方法论来源、source_count 1→2
  - wiki/concepts/Localization.md — 补充轨迹分析方法论来源、source_count 2→3
  - wiki/concepts/恢复机制.md — 补充轨迹分析方法论来源、source_count 1→2
  - wiki/concepts/Agent计算机接口.md — 补充轨迹分析方法论来源、source_count 7→8
- BM25: 5 页面全部更新成功
- Index: +1 新条目 (snapshot_index --update)
- Lint: 0 errors, 1 warning (I1 index listing, 已由 snapshot_index 处理)

## [2026-04-16 12:35] ingest | SWE-agent 论文图表分析 (ChatGPT QA)
- 源文件: raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/05-SWE agent 有哪些图表，每个图表核心内容和核心观点是什么？.md
- 创建页面: 0 个（图表数据补充到已有页面）
- 更新页面: 6 个
  - wiki/concepts/SWE-bench.md — 补充 Table 1 详细结果（Full 12.47%/Lite 18.00%/Shell-only 11%/RAG 1.31%）、pass@k 曲线、source_count 3→4
  - wiki/concepts/HumanEvalFix.md — 补充 Table 2 多语言结果（Python 87.7%/JS 89.7%/Java 87.9%）、source_count 2→3
  - wiki/concepts/Ablation Study.md — 补充 Table 3 详细消融数据 + Figure 5-6 可视化支撑、source_count 1→2
  - wiki/concepts/Localization.md — 补充 Figure 7 成功轨迹行为模式 + Figure 8 失败模式分布（52% 实现错误/23.4% 恢复失败）、source_count 1→2
  - wiki/concepts/Guardrails.md — 补充 Figure 6 三种 Edit Interface 对比、source_count 2→3
  - wiki/concepts/Agent计算机接口.md — 补充 Figure 1-2 ACI 系统图和 IDE 类比、source_count 6→7
- BM25: 6 页面全部更新成功
- Index: 无新增条目（更新已有页面）
- Lint: 未运行（未创建新页面）

## [2026-04-16 12:30] ingest | SWE-agent 五大保障机制 (ChatGPT QA)
- 源文件: raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/04-SWE agent 如何保证 搜索是否高效、编辑是否稳定、反馈是否足够、上下文是否可控、恢复机制是否.md
- 创建页面: 3 个
  - wiki/concepts/环境反馈设计.md — specific & concise 反馈设计，四字段框架（Outcome/Delta/Anchor/Next-step hint）
  - wiki/concepts/状态变化感知.md — 四个状态模块（文件/搜索/执行/协议），显式状态转移系统
  - wiki/concepts/恢复机制.md — 三层恢复（编辑失败不提交/失败原因回显/格式错误重试+历史去噪），77% 恢复率
- 更新页面: 3 个
  - wiki/concepts/Guardrails.md — 补充六层 Guardrail 体系（Protocol/Action/State/Semantic/扩展语义/隐式）、source_count 1→2
  - wiki/concepts/ACI 设计原则.md — 补充 3 个新 relates_to、source_count 1→2
  - wiki/concepts/Agent计算机接口.md — 补充 3 个新 relates_to、source_count 5→6
- BM25: 6 页面全部更新成功
- Index: +3 新条目 (snapshot_index --update)
- Lint: 0 errors, 3 warnings (I1 index listing, 已由 snapshot_index 处理)

## [2026-04-16 12:25] ingest | SWE-agent 24 个核心概念词条 (ChatGPT QA)
- 源文件: raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/03-SWE-agent 论文的所有核心概念 展开详细分析 一个一个.md
- 创建页面: 7 个
  - wiki/concepts/LM Agent.md — LM 从文本生成器到环境决策体的范式转换
  - wiki/concepts/ACI 设计原则.md — 四条核心原则：动作简单、反馈简洁、状态可见、护栏机制
  - wiki/concepts/Guardrails.md — 错误 containment 策略，linting 作为 cheap critic
  - wiki/concepts/Localization.md — 文件级/行级代码定位，SWE agent 的本质瓶颈
  - wiki/concepts/Context Management.md — 工作记忆管理，最近 5 条优于 full history
  - wiki/concepts/ReAct 风格循环.md — thought + command 循环，想一点做一点看反馈
  - wiki/concepts/Ablation Study.md — 将 agent 设计从玄学调 prompt 变为分部件优化
- 更新页面: 3 个
  - wiki/concepts/Agent计算机接口.md — 补充 5 个新 relates_to、source_count 4→5
  - wiki/concepts/SWE-bench.md — 补充新来源、source_count 2→3
  - wiki/concepts/HumanEvalFix.md — 补充新来源、source_count 1→2
- BM25: 10 页面全部更新成功
- Index: +7 新条目 (snapshot_index --update)
- Lint: 0 errors, 7 warnings (I1 index listing, 已由 snapshot_index 处理)

## [2026-04-16 12:20] ingest | SWE-agent 论文 5 页读书笔记 (ChatGPT QA)
- 源文件: raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/02-SWE-agent 论文的 5 页读书笔记版".md
- 创建页面: 1 个
  - wiki/concepts/HumanEvalFix.md — 代码修复基准，SWE-agent pass@1 87.7%，与 SWE-bench 对比
- 更新页面: 2 个
  - wiki/concepts/SWE-bench.md — 补充 HumanEvalFix 对比表（87.7% vs 12.5% 差距分析）、source_count 1→2
  - wiki/concepts/Agent计算机接口.md — 补充"为什么不能直接把 Linux shell 丢给 Agent"五大原因、界面设计作为研究对象的范式变化、source_count 3→4
- BM25: 3 页面全部更新成功
- Index: +1 新条目 (snapshot_index --update)
- Lint: 0 errors, 1 warning (I1 index listing, 已由 snapshot_index 处理)

## [2026-04-16 12:15] maintain
- Relink: 1998 terms, 162 new links across 41 pages
- Reindex: OK (628 页面, 16 clusters, 16 maps, new: LLM能力) | Index: 36 行 | Schema 同步: 已更新
- Check: 15 errors, 1334 warnings, 0 info (0 new gotchas)
- Lint: 0 修复 (I1 expected with slim index), 15 待处理
- Build: 634 节点, 5780 边 → static/ 已同步

## [2026-04-16 09:40] ingest | SWE-agent 论文核心观点 (ChatGPT QA)
- 源文件: raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/01-SWE agent论文 主要讲解什么核心点，什么观点？.md
- 创建页面: 1 个
  - wiki/concepts/SWE-bench.md — 软件工程 Agent 基准测试，pass@1 指标，SWE-agent 12.5% 结果
- 更新页面: 1 个
  - wiki/concepts/Agent计算机接口.md — 补充 SWE-agent 论文三大核心观点、SWE-bench 关系、source_count 2→3
- BM25: 2 页面全部更新成功
- Index: +1 新条目 (snapshot_index --update)
- Lint: 0 errors, 0 warnings

## [2026-04-16 09:35] ingest | Scaling Managed Agents
- 源文件: raw/articles/ai-engineering/anthropic-engineering/Scaling Managed Agents_ Decoupling the brain from the hands.md
- 创建页面: 6 个
  - wiki/concepts/Managed-Agents.md — Claude 托管 Agent 服务：三大抽象组件、安全边界、性能收益
  - wiki/concepts/元控制框架.md — Meta-harness 设计模式：对接口有主见、对实现无主见
  - wiki/concepts/脑手分离架构.md — Brain-Hands Decoupling：宠物变牲畜、TTFT 下降 60%/90%
  - wiki/concepts/会话日志.md — Session 作为上下文窗口外的持久化上下文对象
  - wiki/concepts/宠物与牲畜模式.md — Pets vs Cattle 基础设施范式
  - wiki/concepts/首次令牌时间.md — TTFT 延迟指标及其在 Agent 架构中的意义
- 更新页面: 1 个
  - wiki/concepts/Agent Harness模式.md — 补充 Harness 假设过时风险、meta-harness 演进方向
- BM25: 7 页面全部更新成功
- Index: +6 新条目 (snapshot_index --update)
- Lint: 0 errors, 0 warnings (全部通过)

## [2026-04-16 09:30] ingest | Context windows.md
- 源文件: raw/articles/ai-engineering/anthropic-developer/Context windows.md
- 创建页面: 10 个
  - wiki/concepts/上下文窗口.md — 上下文窗口核心概念（1M/200k、上下文腐烂、验证错误行为）
  - wiki/concepts/上下文感知.md — Claude 4.5+ 模型追踪剩余令牌预算的能力
  - wiki/concepts/扩展思维.md — Extended Thinking 机制、思考块剥离、工具使用结合
  - wiki/concepts/上下文编辑.md — 工具结果清除、思考块清除等细粒度策略
  - wiki/concepts/交错式思考.md — Claude 4 模型在工具调用间思考的能力
  - wiki/concepts/自适应思考.md — 动态决定思考分配的机制
  - wiki/entities/Claude-Sonnet-4-5.md — 200k 窗口，支持上下文感知
  - wiki/entities/Claude-Haiku-4-5.md — 200k 窗口，支持上下文感知
  - wiki/entities/Claude-Sonnet-3-7.md — 验证错误行为起始模型，不支持交错思考
  - wiki/entities/Claude-Sonnet-4.md — 已弃用模型
- 更新页面: 3 个
  - wiki/entities/Claude-Mythos-Preview.md — 补充 1M 窗口、上下文感知、交错式思考
  - wiki/entities/Claude-Opus-4-6.md — 补充 1M 窗口、上下文感知、交错式思考
  - wiki/entities/Claude-Sonnet-4-6.md — 补充 1M 窗口、上下文感知、交错式思考
- BM25: 13 页面全部更新成功
- Index: +10 新条目 (snapshot_index --update)
- Lint: 0 errors, 2 warnings (I1 index listing, 已由 snapshot_index 处理)

## [2026-04-16 09:25] ingest | Compaction.md
- 源文件: raw/articles/ai-engineering/anthropic-developer/Compaction.md
- 创建页面: 6 个
  - wiki/concepts/上下文压缩.md — Anthropic 官方 Compaction API 机制
  - wiki/concepts/零数据保留.md — ZDR 数据隐私协议
  - wiki/concepts/提示词缓存.md — Prompt Caching 与 cache_control
  - wiki/entities/Claude-Mythos-Preview.md — 预览版模型
  - wiki/entities/Claude-Opus-4-6.md — Opus 4.6 模型
  - wiki/entities/Claude-Sonnet-4-6.md — Sonnet 4.6 模型
- 更新页面: 1 个
  - wiki/concepts/Context-Engineering.md — 补充 Compaction API 详细参数与协同策略
- BM25: 7 页面全部更新成功
- Index: +6 新条目 (snapshot_index --update)
- Lint: 0 errors, 0 warnings (全部通过)

## [2026-04-16 09:20] query → "claude code TOOL 设计有什么特别厉害的地方"
- BM25 搜索: 57 候选, top 15 返回
- 主题匹配: Agent系统, AI工程, 工具与框架
- 读取页面: 8 个 (Claude-Code, Agent计算机接口, Agent循环, Agent Harness模式, Context Engineering, Claude Code Hook System, MCP协议层, 生成器-评估器架构)
- 结晶化: 创建 wiki/syntheses/Claude-Code-TOOL-设计七维分析.md
- QA 记录: raw/qa/qa-20260416-092000.md
- Index 更新: +1 新条目

## [2026-04-16 15:30] maintain
- Relink: 1921 terms, 1699 new links across 211 pages
- Reindex: OK (593 页面, 15 clusters) | Schema 同步: 已更新
- Check: 0 errors, 577 warnings, 0 info (0 new gotchas)
- Lint: 0 修复, 577 待处理 (350 broken links, 171 overview too long, 45 map refs, 10 orphans, 1 M2)
- Build: 594 节点, 5032 边, 0 孤页, 1 连通分量 → static/ 已同步

## [2026-04-16] ingest-loop | raw/books/推荐系统 (批量)
- 源文件夹: raw/books/推荐系统
- 处理文件: 18 个 markdown 文件
- 跳过: 1 个非 markdown 文件 (recommender-systems-timeline.html)
- 总计创建约 200+ 页面，更新约 20+ 页面
- 涵盖: 协同过滤起源 → 矩阵分解 → BPR → FM → 深度学习推荐 → 序列推荐 → 图神经网络 → 因果推荐 → LLM 推荐
- 引擎: claude (子代理并行，每批 3 个)

## [2026-04-16] ingest | raw/books/推荐系统/17-p5.md
- 源文件: P5 论文解读 — "Recommendation as Language Processing (RLP): A Unified Pretrain, Personalized Prompt & Predict Paradigm"
- 创建 26 页:
  - 实体(16): P5 论文, Shijie Geng, Yongfeng Zhang, T5, OpenP5, InstructRec, TALLRec, LC-Rec, LLMRec, DEALRec, VIP5, GLoSS, RecSys 2022, Rutgers University, Amazon US Reviews, Yelp Review
  - 概念(10): Whole-word Embedding, 生成式推荐 (LLM), 推荐系统基础模型, Zero-shot 推荐, 个性化 Prompt, 语义 ID, 指令调优, Beam Search 生成, 判别式 LLM 推荐, 生成式 LLM 推荐
- 去重: 已有"生成式推荐"页面(HSTU 范式)，新建"生成式推荐 (LLM)"区分 P5/LLM 范式
- BM25: 26 页全部更新
- Snapshot: +13 entries added

## [2026-04-16] reindex
- 完整性: OK (539 页面, +12 missing added, 1 orphan 修复 — index.md 截断行导致跨行 regex 捕获)
- 主题分类 (Haiku subagent): 15 个 topics → 推荐系统(142), 数学(70), 信息论(37), 机器人学(31), 数值分析(26), AI工程(22), 矩阵理论(20), 经济学(18), Agent系统(17), 概率论(15), 深度学习(13), AI设计(8), 文档处理(7), 工具与框架(4), 其他(3) → .claude/topic-to-wiki.json
- Tags 修复: 58 个页面补充了缺失的 topic tag
- Schema 同步: _schema/CLAUDE.md Topics 已更新（新 topics 集合：15 个）

## [2026-04-16] ingest | raw/books/推荐系统/10-ncf.md
- 更新：`wiki/entities/Neural Collaborative Filtering.md` — 大幅扩充（confidence 0.5→0.85, source_count 1→4）。新增：NCF 四层架构、GMF/MLP/NeuMF 三个模型详解、预训练策略、二元交叉熵损失函数、实验结论（MovieLens 1M + Pinterest）、后续争议（Ferrari Dacrema 2019、Rendle 2020）、历史影响（NGCF、LightGCN、双塔架构、可复现性运动）
- 更新：`wiki/entities/何向南.md` — 大幅扩充（confidence 0.5→0.8, source_count 1→2）。新增：NCF 详细贡献、NeuMF 融合设计、后续工作（NGCF、LightGCN）、学术争议
- 创建：`wiki/entities/Tat-Seng Chua.md` — NUS 教授，NCF 通讯作者
- 创建：`wiki/concepts/GMF.md` — 广义矩阵分解，NCF 的第一个实例化
- 创建：`wiki/concepts/NeuMF.md` — 神经矩阵分解，NCF 的最终融合模型
- 创建：`wiki/concepts/二元交叉熵.md` — 隐式反馈场景下的损失函数，替代 MSE
- BM25：6 页全部更新
- Snapshot index：+4 新条目

## [2026-04-16] maintain
- Relink: 1587 terms, 1585 new links across 189 pages
- Reindex: OK (454 → 456 页面, +2 missing entries) | Schema 同步: 无变化
- Check: 1 error, 615 warnings, 0 info — 1 error fixed (检索增强生成.md YAML indentation)
- Lint: BM25 rebuild (472 pages indexed)
- Build: 474 节点, 3596 边, 0 孤页, 1 连通分量 → static/ 已同步

## [2026-04-16] ingest-loop | ChatGPT-Self-Attention机制解析（3文件 → 10页）
- 创建：Self-Attention机制, 多头注意力, Transformer架构, 位置编码, 绝对位置编码, 相对位置编码, 自注意力机制, Layer Normalization, Batch Normalization, 残差连接
- 更新：注意力预算
- 来源：raw/ChatGPT-Chat/ChatGPT-Self-Attention机制解析/（3文件）

## [2026-04-16 01:30] crystallize | wiki:split-chat + maintain 管线精简
- 新增 wiki:split-chat 命令 + split_chat_json.py 脚本
- maintain 管线移除 reorganize-raw（6步→5步）
- 更新 7 个文档文件，追加 v3.6 changelog
- Working memory: _memory/working/2026-04-16-01.md (4 observations)
- 结晶判断: 无跨概念综合洞见，不创建 synthesis

## [2026-04-16 16:15] ingest | raw/books/信息论/07_shannon_1959_rate_distortion_theory.md
- 创建 3 个概念页面：率失真理论、率失真函数、有损压缩
- 更新 2 个已有页面：信息论（source_count +1，添加 relates_to）、克劳德·香农（source_count +1）
- 同步 index.md：+3 页面

## [2026-04-16 16:00] ingest | raw/books/信息论/06_huffman_1952_minimum_redundancy_codes.md
- 创建 1 个实体页面：大卫·哈夫曼
- 创建 4 个概念页面：Huffman编码、前缀码、Kraft不等式、算术编码
- 更新 1 个已有页面：信源编码定理（source_count +1，添加 relates_to）
- 同步 index.md：+5 页面

## [2026-04-16 15:45] ingest | raw/books/信息论/05_kullback_leibler_1951_information_and_sufficiency.md
- 创建 2 个实体页面：所罗门·库尔巴克、理查德·莱布勒
- 创建 4 个概念页面：KL散度、交叉熵、数据处理不等式、信息几何
- 更新 2 个已有页面：信息论（source_count +1，添加 relates_to）、信息熵（source_count +1）
- 同步 index.md：+6 页面

## [2026-04-16 15:30] ingest | raw/books/信息论/04_hamming_1950_error_correcting_codes.md
- 创建 1 个实体页面：理查德·哈明
- 创建 4 个概念页面：Hamming码、Hamming距离、Hamming界、纠错编码
- 更新 1 个已有页面：信道编码定理（source_count +1，添加 relates_to）
- 同步 index.md：+5 页面

## [2026-04-16 15:15] ingest | raw/books/信息论/03_shannon_1949_communication_in_presence_of_noise.md
- 创建 6 个新概念页面：Shannon-Hartley公式、采样定理、微分熵、球填充问题、分离定理、信噪比
- 更新 3 个已有页面：克劳德·香农、信息论、信道容量（添加 relates_to 和 source_count）
- 同步 index.md：+13 页面（含上次未同步的 7 个）

## [2026-04-16 15:00] ingest | raw/books/信息论/01_hartley_1928_transmission_of_information.md
- 创建 4 个实体页面：拉尔夫·哈特莱、奈奎斯特、克劳德·香农、贝尔实验室
- 创建 3 个概念页面：信息论、Hartley信息量、信息与语义分离
- 同步 index.md：+7 页面

## [2026-04-16 14:40] ingest | raw/assets/MinerU/minerU_01_architecture.md
- 创建 13 个实体页面：MinerU、上海人工智能实验室、PyMuPDF、pdfminer、PaddleOCR、UniMERNet、TableMaster、DocLayout-YOLO、LayoutLMv3、Marker、Nougat、pypdf、opendatalab
- 创建 7 个概念页面：PDF解析、文档布局检测、光学字符识别、公式识别、表格识别、阅读顺序重建、文档结构化提取
- 更新 1 个已有页面：检索增强生成（添加 relates_to 反向链接）
- 同步 index.md：+20 页面

## [2026-04-16 14:35] qa-import | qa-20260416-143000.md → 0 个洞见（已存在于 wiki）

## [2026-04-16] wiki:query | 上下文工程核心原因与最新要点
- 综合 8 个页面回答：Context Engineering、上下文腐烂、注意力预算、分层记忆架构、即时上下文检索、渐进式披露、多Agent架构、结构化笔记法
- QA 记录：raw/qa/qa-20260416-143000.md
- 更新 7 个页面 last_accessed

## [2026-04-16] maintain
- Reorganize-raw: 1003 → 1003 ✓ (0 moved, noop)
- Relink: 1018 terms, 1 new link (SQLite entity)
- Reindex: OK (291 页面, 7 clusters) | Schema 同步: 已更新（新增 `方法论` cluster）
- Check: 0 errors, 440 warnings, 0 info
- Lint: 0 自动修复, 440 待处理
- Build: 291 节点, 2144 边, 0 孤页, 1 连通分量 → static/ 已同步

## [2026-04-16] ingest | raw/articles/ai-engineering/anthropic-engineering/Context Rot_ How Increasing Input Tokens Impacts LLM Performance.md

- 更新：`wiki/concepts/上下文腐烂.md` — 从 Chroma 原始报告大幅扩充。新增：四大实验（针问相似度/干扰项影响/针草相似度/干草堆结构）、LongMemEval 聚焦vs全量对比、重复单词任务、模型差异（Claude 弃权率 vs GPT 幻觉率）、核心结论"信息如何呈现比是否存在更重要"；source_count 1→2

## [2026-04-15] ingest-loop | raw/articles/ai-engineering/anthropic-engineering/ (22 文件)

### 已处理（3 篇先前 ingest 跳过）
- Contextual Retrieval, Effective context engineering, Harness design → 已建立页面

### 新建 7 个概念页面
- `wiki/concepts/Agent工作流模式.md` — Anthropic 五种核心工作流（提示链/路由/并行化/编排者-工人/评估者-优化者）+ 工作流 vs Agent 区别 + ACI 概念
- `wiki/concepts/Agent评估方法论.md` — 完整 Eval 词汇体系（task/trial/transcript/outcome）、三类评分器、能力 vs 回归评估、pass@k vs pass^k、8步路线图
- `wiki/concepts/多Agent架构.md` — Token 使用解释 80% 性能方差、编排者-工人模式、子 Agent 作为压缩器、90.2% 提升数据
- `wiki/concepts/Think工具.md` — 无副作用思考工具，vs 扩展思考的区别，τ-Bench 54% 提升，最佳使用场景
- `wiki/concepts/Agent Skills.md` — SKILL.md 渐进式披露机制（三层），开放标准，与 MCP 互补
- `wiki/concepts/长时任务Agent设计.md` — 初始化 Agent + 编码 Agent 两阶段，功能列表 JSON，四大失败模式
- `wiki/concepts/Agent计算机接口.md` — ACI vs HCI，工具设计五原则，评估驱动循环，Tool Use Examples

### 19 篇文章已读取分析，主要新知识点：
- Building Effective AI Agents, Demystifying Evals, Multi-agent Research → 核心概念提取完成
- Claude Code Auto Mode → 两级分类器 + 威胁模型（未建独立页面，可后续补充）
- Scaling Managed Agents → Brain/Hands/Session 解耦（未建页面）
- Code execution with MCP / Advanced Tool Use → 编程式工具调用（未建页面）
- Sandboxing, Desktop Extensions, SWE-bench → 技术细节页面（未建）

## [2026-04-15] ingest | raw/articles/ai-engineering/anthropic-engineering/Contextual Retrieval in AI Systems.md

- 创建：`wiki/concepts/检索增强生成.md` — RAG 标准流水线（切块→嵌入→向量DB→召回→注入），BM25 混合检索，与 JIT 的对比，适用边界（<20万token 直接全文更优）
- 创建：`wiki/concepts/情境化检索.md` — Anthropic 提出的 RAG 增强方案；LLM 自动为 Chunk 生成 50-100token 情境说明并前置；Contextual Embeddings(-35%) + Contextual BM25(-49%) + Reranking(-67%); $1.02/百万文档token
- 创建：`wiki/concepts/检索重排序.md` — 粗排后用重排序模型精排，Top-150→Top-20，Cohere 实验数据，延迟/成本权衡
- 更新：`wiki/concepts/Context-Engineering.md` — 相关链接追加 RAG 和情境化检索

## [2026-04-15] ingest | raw/articles/ai-engineering/anthropic-engineering/Effective context engineering for AI agents.md

- 创建：`wiki/concepts/上下文腐烂.md` — Context Rot：token 增加时 LLM 召回精度下降的现象（Chroma Research 命名），n² 注意力成因，工程含义
- 创建：`wiki/concepts/注意力预算.md` — Transformer n² 注意力机制导致的有限注意力资源，系统提示"合适高度"（Right Altitude）的两极失败模式
- 创建：`wiki/concepts/即时上下文检索.md` — Agent 运行时按需动态加载数据，对比预推理检索，Claude Code 混合实现，元数据作为隐式信号
- 创建：`wiki/concepts/结构化笔记法.md` — Agent 外置持久记忆（NOTES.md/记忆工具），三种长时任务技术对比（Compaction/笔记法/多Agent）
- 更新：`wiki/concepts/Context-Engineering.md` — 新增 Anthropic 工程视角段落（context rot、attention budget、三大技术、JIT），source_count 1→2
- 更新：`wiki/entities/Prithvi-Rajasekaran.md` — 新增合著文章，source_count 1→2

## [2026-04-15] ingest | raw/articles/ai-engineering/anthropic-engineering/Harness design for long-running application development.md

- 创建：`wiki/entities/Prithvi-Rajasekaran.md` — Anthropic Labs 成员，生成器-评估器架构提出者
- 创建：`wiki/concepts/生成器-评估器架构.md` — GAN 启发的多 Agent 生成/评估分离模式，含前端四维评分准则和三 Agent 系统完整描述
- 创建：`wiki/concepts/上下文焦虑.md` — LLM 接近上下文窗口限制时过早包装任务的失败模式
- 创建：`wiki/concepts/上下文重置.md` — 彻底清空会话启动新 Agent + 结构化交接工件，对比 Compaction 的设计权衡
- 创建：`wiki/concepts/Sprint合约制.md` — 生成器和评估器在 Sprint 开始前谈判"完成"标准的机制
- 更新：`wiki/concepts/Agent Harness模式.md` — 新增 Anthropic 三 Agent Harness 段落，source_count 3→4

## [2026-04-15 21:46] maintain
- Reorganize-raw: 980 → 980 ✓ (0 moved, noop)
- Relink: 1018 terms, 32 new links across 4 pages
- Reindex: OK (264 页面, 6 clusters)
- Check: 0 errors, 428 warnings, 0 info
- Lint: 2 修复 (B2×2 BM25), 426 待处理
- Build: 264 节点, 1957 边, 0 孤页, 1 连通分量 → static/ 已同步

## [2026-04-15] ingest | raw/books/计算机科学/01-turing-on-computable-numbers.md

- 创建：`wiki/concepts/图灵机.md` — 定义、通用图灵机、不可计算数、影响
- 创建：`wiki/concepts/停机问题.md` — 对角化证明、归约技术、软件工程影响
- 创建：`wiki/concepts/Church-Turing 论题.md` — 多模型等价、三个版本、对AI的启示
- 更新：`wiki/entities/阿兰·图灵.md` — 新增可计算性理论段落，source_count 2→3

## [2026-04-15] ingest | raw/books/机器人学/ (16 files)

已覆盖（01-11, 13）：来自前一会话，跳过。
新增页面：
- 创建：`wiki/concepts/SLAM.md` — EKF-SLAM / FastSLAM / GraphSLAM 三范式
- 创建：`wiki/concepts/蒙特卡罗定位.md` — MCL / 粒子滤波 / amcl
- 创建：`wiki/entities/Sergey-Levine.md` — 端到端机器人学习奠基人
- 创建：`wiki/concepts/端到端视觉运动学习.md` — GPS + Spatial Softmax
- 创建：`wiki/concepts/域随机化.md` — Domain Randomization + ADR（解魔方）
- 创建：`wiki/concepts/视觉-语言-动作模型.md` — VLA 范式 / RT-2

## [2026-04-15] maintain
- Reindex: OK (245 页面, index 同步)
- Check: 0 errors, 352 warnings (B1=206 断链, F3=140 概述过长, O1=3 孤页, B2=2, M2=1)
- Lint: 修复 B2×2（BM25 补录）
- Build: 245 节点, 1444 边, 0 孤页, 11 连通分量 → static/ 已同步

## [2026-04-15] ingest-loop | raw/articles/UI-skill/ (7 files, claude engine)

- 创建实体：`wiki/entities/UI-UX-Pro-Max.md`（source_count: 7，含全系列 relates_to）
- 创建概念：`wiki/concepts/AI设计推理层.md`
- 创建概念：`wiki/concepts/结构化UI风格知识库.md`（67 种风格 + 结构化元数据）
- 创建概念：`wiki/concepts/行业设计反模式系统.md`（161 条负样本规则）
- 创建概念：`wiki/concepts/行业色彩情绪映射.md`（161 套色板 + 57 组字体配对）
- 创建概念：`wiki/concepts/工程化UX规则体系.md`（99 条 P0/P1/P2 UX 规则）
- 创建概念：`wiki/concepts/技术栈感知设计规则.md`（15 个技术栈 + BM25 选型）
- 创建概念：`wiki/concepts/Master-Overrides设计系统持久化.md`

## [2026-04-15] ingest | raw/articles/pi-agent/03-pi-agent-core.md

- 创建：`wiki/concepts/Agent循环.md` — Agent 循环核心结构、工具验证、消息队列
- 创建：`wiki/concepts/事件驱动Agent架构.md` — subscribe/emit 模式、双通道设计、多 UI 驱动
- 更新：`wiki/entities/Pi-Agent.md` — 新增 pi-agent-core 段落，source_count 2→3，新增两条 relates_to

## [2026-04-15 20:45] ingest | raw/articles/pi-agent/02-pi-ai.md
- 创建: wiki/concepts/LLM-Wire-Protocol统一模式.md (四协议覆盖 300+ 模型)
- 创建: wiki/concepts/跨Provider上下文迁移.md (Context Handoff, Pi 最独特能力)
- 更新: wiki/entities/Pi-Agent.md (追加 pi-ai 层, source_count 1→2, 新增 2 个 relates_to)
- 矛盾: 无

## [2026-04-15 20:30] ingest | raw/articles/pi-agent/01-overview-philosophy.md
- 创建: wiki/entities/Mario-Zechner.md (libGDX 创造者, Pi Agent 作者)
- 创建: wiki/entities/Pi-Agent.md (极简 AI 编程代理工具包)
- 创建: wiki/entities/OpenClaw.md (多渠道 AI 助手, 14.5 万 Stars)
- 更新: wiki/concepts/Agent Harness模式.md (追加 Pi Agent 极简路线对比, source_count 2→3)
- 矛盾: Pi Agent vs Claude Code 设计哲学对立 (已标记 contradicts)

## [2026-04-15 20:15] qa-import | all → 1 insight
- 处理: 9 个 QA 文件 (8 原有 + 1 新发现)
- 聚类: 6 个主题 (开发工具, Agent搜索, UrhoX, Claude Code, WASM, 数值分析)
- 创建: wiki/qa-insights/Cargo-for-X全能工具链模式.md
- 跳过: 8 个 (5 项目特定, 2 已有wiki页, 1 已结晶)
- 快照: raw/qa/qa.snapshot.md 全部标记为 [x]

## [2026-04-15 20:00] crystallize | v3.3 系统级重构
- Working Memory: _memory/working/2026-04-15-06.md (6 条观察)
  - O1: 代码重复是系统性的 → wiki_utils.py 共享模块
  - O2: Qwen 管线无状态性 → --context-pages 上下文补偿
  - O3: 错误容忍 vs 错误拒绝 → save-always + error annotation
  - O4: QA 数据流不对齐 → 统一到 raw/qa/ + qa.snapshot.md
  - O5: hook_graph O(N) 隐性开销 → 30s mtime 防抖
  - O6: 有向图边去重丢失方向 → 按关系类型选择去重策略
- Synthesis: wiki/syntheses/知识系统的六个工程反模式.md
  - 跨 5 个概念域的综合洞见，提炼为 6 个可复用的反模式诊断

## [2026-04-15 19:50] maintain
- Reindex: OK (185 pages, 13 topic clusters, 3 orphaned entries removed)
- Check: 0 errors, 245 warnings (140 broken links, 101 overview length, 3 index, 1 map)
- Lint: 3 YAML frontmatter errors fixed (duplicate tags + wrong indent), 3 index entries restored
- Build: 188 nodes, 1164 edges, 0 orphans, 7 components → static/ synced (189 HTML pages)

## [2026-04-15 19:45] v3.3 release
- Created scripts/wiki_utils.py (shared module)
- Refactored 8 Python scripts to use wiki_utils
- Fixed: XSS, edge directionality, overview threshold, double reads, graph debounce
- qwen_ingest.py: save-always, dedup, --context-pages, --model, retry, truncation
- wiki:query → raw/qa/, wiki:qa-import + qa.snapshot.md
- docs/gotchas/v3.3-refactor.md: 10 new gotchas (#18-27)

## [2026-04-15 18:42] crystallize | Wiki 系统工程：maintain 命令 + hooks 修复
- Working Memory: _memory/working/2026-04-15-05.md (5 条观察)
  - O1: Claude Code hooks 协议误解 → 沉默失败模式
  - O2: 路径匹配过宽陷阱（O22 再现）
  - O3: 管道命令的阶段间合约设计
  - O4: 文档散布（7 处同步）的系统性代价
  - O5: Consolidate 在知识库早期的局限性
- 结晶化: 否（系统工程元观察，未连接 3+ 知识页面）

## [2026-04-15 18:35] consolidate
- Working → Episodic: 处理了 1 个 working memory (2026-04-15-04), 新增 6 条观察 (O20-O25)
- Episodic → Semantic: 0 个晋升（仅 1 天数据，需 3+ 天）
- 置信度衰减: 0 个（无 semantic memory）
- Journal 模式: 更新了工具分离思维（3次出现），新增 2 个待观察候选
- Skills tracker: 新增"Wiki 系统工程"领域

## [2026-04-15 17:01] graph
- 知识图谱: 173 节点, 1074 边, 0 孤页, 4 连通分量
- 同步: graph.json + graph-statistics.json + wiki HTML (173 页)
- lint: 0 errors, 207 warnings

## 2026-04-15 — query: "龙格-库塔现象是什么，为什么存在，解决方法是什么"
- BM25 命中: 龙格现象, 勒贝格常数, 切比雪夫逼近理论, 样条方法, 龙格-库塔方法
- 澄清命名混淆: 「龙格-库塔现象」= 龙格现象（插值）+ 龙格-库塔方法（ODE）的混合
- 结晶化: wiki/syntheses/龙格现象全景解析.md
- last_accessed 更新: 6 页

## 2026-04-15 — query: "claude code 上下文工程细节展开"
- BM25 命中 10 页，核心: Context-Engineering, 分层记忆架构, 渐进式披露, Claude-Code-Hook-System
- 结晶化: wiki/syntheses/Claude-Code上下文工程全景.md (综合 6 页)
- QA 记录: qa/2026-04-15.md
- last_accessed 更新: 6 页

## 2026-04-15 — lint
- 扫描: 156 个页面
- 初始: 0 errors | 156 warnings
- 最终: 0 errors | 143 warnings (-13)
- 自动修复 (13 个):
  - B1×5: [[Claude Code]]→[[Claude-Code]] (3 files), [[Bun]]→[[Bun-Runtime]], [[上下文工程...]]→[[Context-Engineering]]
  - I2×2: 删除 index.md 模板占位符 [[页面名]] / [[PAGE_NAME]]
  - O1×1: Claude-Code.md 孤页确认已有入链（false positive）
  - M1×4: 重新生成 maps/*.md（摘要去除内嵌链接）
  - 图谱: 995→1002 边（+6 新连接）
- 需人工处理:
  - F3 (76): 概述超 200 字 — 不强制截断，保留完整描述
  - B1 (67): 指向未创建页面的预留链接（检索增强生成、Prompt缓存等）
- 矛盾 (D): 9 条 contradicts 关系，均为已知对立（非语义冲突），无需 supersedes
- 一致性 (G): BM25 156/156 ✓ | 连通分量 2（数学 133 节点 + AI 23 节点）

## 2026-04-15 — graph
- 构建知识图谱: 156 节点, 996 边, 0 孤页, 2 连通分量
- Lint: 0 errors, 156 warnings (F3 概述超长 + B1 断链，无阻断项)
- Top-3: 矩阵理论(52), 概率论(51), 奇异值分解(32)
- 产出: graph.json, graph-statistics.json, static/wiki/ HTML

## 2026-04-15 — reindex
- 完整性: OK (156 页面, 0 缺失, 0 孤条目)
- 新增索引: 19 页面 (snapshot_index --update)
- Tags 修复: 65 个页面补充了主题 tag（数值分析/概率论/矩阵理论/AI）
- 主题分类: 6 个 → 数值分析(61), 概率论(39), 矩阵理论(30), AI(16), 组合数学(5), 工具(5)
- 生成 maps/: 数值分析.md, 概率论.md, 矩阵理论.md, AI.md, 组合数学.md, 工具.md
- 快照: .claude/reindex.snapshot.json (156 pages)

## 2026-04-15 — ingest: context-engineer/context-design.md

- 来源：`raw/articles/context-engineer/context-design.md`
- 操作：创建 2 个新概念页面
  - `wiki/concepts/Context-Engineering.md` (confidence: 0.92)
  - `wiki/concepts/分层记忆架构.md` (confidence: 0.9)
- BM25 更新：两页均已更新
- index.md：已追加两条目

> 追加写入，不可修改历史条目。格式：`## [YYYY-MM-DD] 操作类型 | 描述`

## [2026-04-15] init | 知识库初始化

- 创建 vault 目录结构
- 写入 schema 文档（CLAUDE.md, entity-types.md, relationship-types.md, quality-rules.md）
- 写入模板（daily, wiki-page, reflection, judgment, weekly-review）
- 创建 index.md, log.md, dashboard.md

## [2026-04-15] ingest | raw/books/数值分析

- 处理源文件：18 个 markdown 文件（牛顿法、欧拉法、高斯最小二乘法、FFT、有限元方法等）
- 创建新实体页面：10 个
  - [[艾萨克·牛顿]]、[[帕夫努季·利沃维奇·切比雪夫]]、[[约翰·冯·诺依曼]]、[[约翰·图基]]
  - [[詹姆斯·库利]]、[[阿兰·图灵]]、[[辛克维奇]]、[[莱昂哈德·欧拉]]
  - [[卡尔·弗里德里希·高斯]]、[[卡尔·古斯塔夫·雅各布·雅可比]]
- 创建新概念页面：3 个
  - [[牛顿法]]、[[快速傅里叶变换]]、[[有限元方法]]
- 更新 index.md：添加 13 个新页面条目
- 关系建立：所有页面均包含双向 relates_to 关系
- 矛盾检查：未发现矛盾信息
- 质量验证：所有页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/数值分析/02_euler_method_ode.md

- 处理源文件：欧拉方法（02_euler_method_ode.md）
- 更新已有实体页面：1 个
  - [[莱昂哈德·欧拉]]：补充详细生平、学术成就、发表背景等信息，source_count 从 1 增至 2
- 创建新实体页面：1 个
  - [[布鲁克·泰勒]]：泰勒级数定理提出者，为数值方法提供理论基础
- 创建新概念页面：1 个
  - [[欧拉方法]]：数值分析最基础ODE解法，包含算法公式、几何解释、精度分析、收敛定理等完整内容
- 更新 index.md：添加 2 个新页面条目（布鲁克·泰勒、欧拉方法），更新统计数字（总页面数 13→15）
- 关系建立：所有新建/更新页面包含双向 relates_to 关系
- 矛盾检查：新信息与已有页面无矛盾
- 质量验证：所有页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/矩阵分析/02_sylvester_matrix_terminology_law_of_inertia_1852.md

- 处理源文件：Sylvester矩阵术语与惯性律（02_sylvester_matrix_terminology_law_of_inertia_1852.md）
- 创建新实体页面：1 个
  - [[詹姆斯·约瑟夫·西尔维斯特]]：创造"矩阵"术语，证明惯性律，与凯莱奠定线性代数基础
- 创建新概念页面：1 个
  - [[矩阵理论]]：研究矩阵作为独立数学对象的学科，包含术语起源、惯性律、学科发展等
- 更新 index.md：添加 2 个新页面条目（詹姆斯·约瑟夫·西尔维斯特、矩阵理论），更新统计数字（总页面数 15→17）
- 关系建立：所有新建页面包含双向 relates_to 关系
- 矛盾检查：新信息与已有页面无矛盾
- 质量验证：所有页面满足 _schema/quality-rules.md 要求

## [2026-04-15] consolidate | 日常整合

- **Working → Episodic**：处理 1 个 working memory 文件（2026-04-15-01.md）
  - 6 条观察压缩为 episodic 摘要
  - 创建 `_memory/episodic/2026-04-15.md`
  - 工作记忆标记为 processed
- **Episodic → Semantic**：跳过（仅 1 天 episodic，需 3+ 天重复才晋升）
  - 候选：O2（最优性思维范式）、O4（缓存中间件顺序）—— 待后续确认
- **置信度衰减**：跳过（semantic 目录为空）
- **Journal 模式扫描**：跳过（journal/daily 无文件）
- **更新 dashboard.md**：Wiki页面数 15→28，记忆条目 0→1 episodic，最近 consolidate 日期更新，补充知识域分布表
- 总结：处理 1 个 working，晋升 0 个 semantic，衰减 0 个

## [2026-04-15] crystallize | 数值分析 + DeepAgents 工程洞见

**会话主题**：单次会话同时处理数值分析（高斯系列）和 LLM Agent 工程（DeepAgents 生态）

**Working Memory**：`_memory/working/2026-04-15-01.md`（6条观察）

**结晶产出**：
- 创建 Synthesis 页面：[[DeepAgents评估设计哲学]]
  - 综合 DeepAgents评估体系 + LLM-as-Judge + Harbor 分析工具三个来源
  - 洞见：三重分离原则（正确性/效率 / 确定性/语义 / 能力/基础设施）
  - 延伸：该哲学是传统软件测试分层思想在 AI Agent 评估中的应用
- 更新 index.md：综合分析 0→1，总页面数 27→28

**值得后续探索的洞见（未结晶）**：
- 勒让德的双重身份：最小二乘命名者 + 高斯求积节点数学核心
- 数值分析"最优性思维"范式（高斯求积开创）
- DeepAgents 中间件顺序决策：缓存在记忆之前保护 prompt cache 稳定性

## [2026-04-15] ingest | raw/books/deepagents-book-main/24-Harbor分析与统计工具.md

- 处理源文件：Harbor 分析与统计工具（24-Harbor分析与统计工具.md）
- 创建新页面：0
- 更新已有概念页面：1 个
  - [[DeepAgents评估体系]]：补充 Harbor 分析工具链详解
    - FailureCategory 枚举（CAPABILITY/INFRA_OOM/INFRA_TIMEOUT/INFRA_SANDBOX/UNKNOWN）及 is_infrastructure 属性
    - wilson_ci（Wilson 置信区间，小样本稳健）和 min_detectable_effect（MDE，防过度解读涨跌）
    - harbor_langsmith.py 四个子命令（create-dataset/ensure-dataset/create-experiment/add-feedback）
    - 生成类脚本（generate_radar/generate_eval_catalog/generate_model_groups）
    - 数据闭环工程化建议
    - source_count 8→9
- 更新 index.md：无新页面，统计数字不变
- 矛盾检查：无矛盾（原页面对 Harbor 分析工具的描述较笼统，新内容补充细节，不冲突）

## [2026-04-15] ingest | raw/books/deepagents-book-main（31章，逐文件）

- 处理源文件：31个章节 + README.md，覆盖 DeepAgents 项目全貌（Harness 架构/SDK/CLI/评估/Harbor/ACP/工程实践/示例）
- 创建新实体页面：1 个
  - [[DeepAgents]]：LangChain 官方 Agent Harness，monorepo 结构、create_deep_agent API、子代理、CLI、CI/CD、示例项目
- 创建新概念页面：6 个
  - [[Agent Harness模式]]：设计哲学——在现有框架叠加中间件/后端的三层架构，中间件 vs 普通工具对比，默认栈顺序
  - [[DeepAgents中间件体系]]：所有11个中间件详解（FilesystemMiddleware/SubAgentMiddleware/SummarizationMiddleware/MemoryMiddleware/SkillsMiddleware/Patch/Async/Anthropic缓存/HumanInTheLoop/TodoList/REPL）
  - [[DeepAgents后端协议]]：BackendProtocol/SandboxBackendProtocol 接口，5种内置后端，合作方沙箱（Daytona/Modal/QuickJS/Runloop），数据类型与版本化设计
  - [[DeepAgents评估体系]]：两层断言模型、TrajectoryScorer 建造者 API、run_agent 流程、7个评估维度雷达图、外部基准集成、Harbor/Terminal Bench 2.0、编写用例五步流程
  - [[LLM-as-Judge]]：通用 LLM 评判器模式，适用场景、工作原理、最佳实践、DeepAgents 实现（openevals + LangSmith 记录）
  - [[ACP协议]]：Agent Client Protocol 服务端集成包 deepagents-acp，server.py 核心实现
- 更新 index.md：添加 7 个新页面条目，统计数字 20→27（实体 13→14，概念 7→13）
- 关系建立：DeepAgents ↔ 所有概念页面双向 relates_to 关系
- 矛盾检查：无矛盾
- 质量验证：所有页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/数值分析/05_gauss_quadrature.md

- 处理源文件：高斯求积公式（05_gauss_quadrature.md）
- 注：[[卡尔·弗里德里希·高斯]] 实体页面已存在且已包含此来源，无需更新
- 创建新概念页面：1 个
  - [[高斯求积公式]]：n点精确至2n-1次（理论最优），含公式构造、各类Gauss变体（Legendre/Chebyshev/Laguerre/Hermite/Jacobi）、误差估计、实践应用（FEM/谱方法/Gauss-Kronrod自适应）、局限性
- 更新已有实体页面：2 个
  - [[阿德里安-马里·勒让德]]：补充勒让德多项式与高斯求积节点的联系，source_count 1→2
  - [[卡尔·古斯塔夫·雅各布·雅可比]]：补充1826年严格证明高斯求积理论、Gauss-Jacobi求积，source_count 1→2
- 更新 index.md：添加 1 个新页面条目，统计数字 19→20（概念 6→7）
- 关系建立：高斯求积↔勒让德↔雅可比↔有限元方法 等双向关系
- 矛盾检查：无矛盾，与已有页面信息一致
- 质量验证：所有页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/数值分析/03_gauss_least_squares.md

- 处理源文件：高斯最小二乘法综述（03_gauss_least_squares.md）
- 注：[[卡尔·弗里德里希·高斯]] 实体页面已存在且已包含此来源，无需更新
- 创建新实体页面：1 个
  - [[阿德里安-马里·勒让德]]：法国数学家，1805年首次公开发表最小二乘法，与高斯存在优先权争议
- 创建新概念页面：1 个
  - [[高斯最小二乘法]]：含正规方程、几何解释、高斯-马尔可夫定理、主要变体（岭回归/LASSO）、局限性等
- 更新 index.md：添加 2 个新页面条目，统计数字 17→19
- 关系建立：双向 relates_to 关系（高斯↔勒让德↔高斯最小二乘法）
- 矛盾检查：无新矛盾，已有高斯页面的 contradicts 关系与新信息一致
- 质量验证：所有页面满足 _schema/quality-rules.md 要求

## [2026-04-15] lint | wiki health check

- 扫描页面数：15
- 问题总数：15（所有页面均为孤页，未在其他页面中被链接）
- 自动修复：0
- 需要人工处理：15（孤页问题需通过创建综合分析页面解决）

### 详情
- **Frontmatter 完整性**：✓ 所有 15 个页面均包含完整 frontmatter 字段
- **断链检查**：✓ 未发现断裂的 [[链接]]
- **矛盾检查**：✓ 未发现 type=contradicts 的未解决矛盾
- **过期检查**：✓ 未发现 confidence < 0.3 的 stale 页面
- **index.md 一致性**：✓ 所有 wiki 页面均出现在 index.md 中
- **孤页检查**：⚠ 全部 15 个页面均无入链（这是预期情况，因尚未创建综合分析页面）

### 建议
- 创建综合分析页面（wiki/syntheses/）来链接相关概念和实体
- 例如：创建"数值分析基础方法综述"页面，链接牛顿法、欧拉方法、快速傅里叶变换等概念
- 创建"数值分析奠基人"页面，链接各数学家实体

## [2026-04-15] ingest | raw/books/概率论/01_pascal_fermat_correspondence.md

- 处理源文件：Pascal–Fermat 通信与概率论诞生（01_pascal_fermat_correspondence.md）
- 创建新实体页面：9 个
  - [[布莱兹·帕斯卡]]：法国数学家，1654年与费马开创概率论
  - [[皮埃尔·德·费马]]：法国律师兼业余数学家，1654年与帕斯卡独立解决点数问题
  - [[梅雷骑士]]：法国贵族赌徒，向帕斯卡提出点数问题
  - [[克里斯蒂安·惠更斯]]：荷兰数学家，1657年出版第一部概率论教材
  - [[卢卡·帕西奥利]]：意大利数学家，1494年首次提出点数问题
  - [[雅各布·伯努利]]：瑞士数学家，证明大数定律
  - [[亚伯拉罕·德莫弗]]：法国裔英国数学家，推广概率计算方法
  - [[皮埃尔-西蒙·拉普拉斯]]：法国数学家，正式确立古典概率定义
- 创建新概念页面：9 个
  - [[点数问题]]：概率论经典问题，1654年帕斯卡和费马的通信解决
  - [[概率论]]：研究随机现象规律性的数学学科，由点数问题诞生
  - [[期望值]]：概率论基础概念，惠更斯正式定义
  - [[样本空间]]：随机试验的所有可能结果的集合
  - [[递推方法]]：帕斯卡解决点数问题的方法，后向归纳思想原型
  - [[组合枚举法]]：费马解决点数问题的方法，古典概率论基础
  - [[古典概率定义]]：等可能情形下的概率定义，拉普拉斯正式确立
  - [[帕斯卡三角形]]：二项式系数表，与概率论的联系
  - [[大数定律]]：频率趋向概率，伯努利证明，概率论与统计学桥梁
- 更新 index.md：添加 18 个新页面条目，统计数字 27→45
- 关系建立：所有新建/更新页面包含双向 relates_to 关系
  - 帕斯卡 ↔ 费马（collaborated_with）
  - 点数问题 ← 帕斯卡/费马（implements）→ 概率论（caused）
  - 递推方法/组合枚举法/样本空间/期望值 ← 点数问题（depends_on）
  - 八个数学家按历史顺序形成"概率论发展链"：帕西奥利→帕斯卡&费马→惠更斯→伯努利→德莫弗→拉普拉斯
- 矛盾检查：无矛盾
- 质量验证：所有页面满足 _schema/quality-rules.md 要求
  - 完整 frontmatter，概述 ≤ 200 字，至少 1 个来源，至少 1 个 relates_to
  - 中文为主，专有名词保留英文

## [2026-04-15] ingest | raw/books/概率论/02_huygens_de_ratiociniis.md

- 处理源文件：惠更斯《论赌博中的推理》（02_huygens_de_ratiociniis.md）
- 创建新概念页面：1 个
  - [[赌徒破产问题]]：有限资金赌徒最终必然破产的经典概率问题，惠更斯1657年首次提出变体
- 更新已有实体页面：1 个
  - [[克里斯蒂安·惠更斯]]：大幅扩充，增加巴黎访问背景、出版细节（van Schooten译本）、三条基本命题（期望定义）、14道练习题详解、对后续工作的影响链，source_count 1→2
- 更新已有概念页面：1 个
  - [[期望值]]：新增"惠更斯的形式化定义"小节，包含三条命题表格和"公平交换"（无套利）论证方法，source_count 1→2
- 更新 index.md：添加1个新页面条目，统计数字 45→46
- 矛盾检查：无矛盾，新信息与已有页面完全一致并互相补充
- 质量验证：所有新建/更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/概率论/03_bernoulli_ars_conjectandi.md

- 处理源文件：伯努利《猜度术》（03_bernoulli_ars_conjectandi.md）
- 创建新页面：0
- 更新已有实体页面：1 个
  - [[雅各布·伯努利]]：大幅扩充，修正生卒年（1654→1655），增加伯努利家族表（约翰/尼古拉斯/丹尼尔）、《猜度术》四部分结构详解、大数定律精确定理陈述（ε-c/(c+1) 形式）、数值例子（p=3/5, n≥25550）、哲学洞见（已知p→未知p的认识论转变）、伯努利数、局限性和影响链，source_count 1→2
- 更新已有概念页面：1 个
  - [[大数定律]]：补充伯努利定理的精确形式（P(|k/n-p|<ε)>c/(c+1)）、历史数值例子、哲学意义（推断科学基础），新增"影响链"表（伯努利→De Moivre→切比雪夫→Borel→Kolmogorov），source_count 1→2
- 矛盾检查：发现生卒年细节差异（1654 vs 1655），依据源文件更正为1655（格里高利历），无实质矛盾
- 质量验证：所有更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/概率论/04_de_moivre_doctrine_of_chances.md

- 处理源文件：德莫弗《机会的学说》（04_de_moivre_doctrine_of_chances.md）
- 创建新概念页面：3 个
  - [[正态分布]]：钟形曲线，德莫弗1733年首次推导（早于高斯76年），含密度函数、68-95-99.7法则、历史溯源（Stigler命名定律），以及De Moivre推导思路、CLT解释其普遍性
  - [[中心极限定理]]：大量独立同分布随机变量之和趋近正态分布，含历史发展年表（De Moivre→Laplace→Lyapunov→Lindeberg→Feller）、与大数定律的关系对比表、应用举例
  - [[生成函数]]：将概率分布编码为幂级数的代数工具，德莫弗引入，含PGF/MGF/特征函数定义、核心性质表、发展历史
- 更新已有实体页面：1 个
  - [[亚伯拉罕·德莫弗]]：大幅扩充，增加胡格诺派难民背景、三版出版时间线（1718/1738/1756）及1733年小册子、三大贡献详述（De Moivre-Laplace定理/正态分布首次推导/生成函数引入）、De Moivre公式、局限性分析，confidence 0.85→0.9，source_count 1→2
- 更新 index.md：添加3个新页面条目，统计数字 46→49（概念 23→26）
- 矛盾检查：无矛盾；已有页面中 [[大数定律]] 提到 "De Moivre 用正态近似改善估计" 与源文件完全一致
- 质量验证：所有新建/更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/概率论/05_bayes_essay_inverse_probability.md

- 处理源文件：贝叶斯《论机会学说中一个问题的解》（05_bayes_essay_inverse_probability.md）
- 创建新实体页面：1 个
  - [[托马斯·贝叶斯]]：英国牧师兼业余数学家，逆概率框架创立者，包含生平（遗作经Price整理1763年发表）、台球桌思想实验、核心结果（Beta后验分布公式）、局限性和历史地位
- 创建新概念页面：2 个
  - [[贝叶斯定理]]：条件概率基本定理，含数学推导（三种形式：一般/完全/统计形式）、贝叶斯原始推导（Beta分布形式）、医疗检测直觉例子（反直觉的50%结果）、现代应用
  - [[贝叶斯推理]]：统计推断范式，含先验→似然→后验完整框架表、与频率学派对比表、先验选择问题（均匀/共轭/Jeffreys/弱信息先验）、历史起源（1763 Bayes→1774 Laplace独立发展）、现代应用（MCMC, ML, 卡尔曼滤波）
- 更新已有实体页面：1 个
  - [[皮埃尔-西蒙·拉普拉斯]]：更新贡献描述（明确1774年独立逆概率方法），增加 relates_to 贝叶斯推理，增加相关链接
- 更新 index.md：添加3个新页面条目，统计数字 49→52（实体 23→24，概念 26→28）
- 矛盾检查：无矛盾；拉普拉斯页面已有 [[贝叶斯定理]] relates_to，源文件确认并补充了其1774年独立发展的历史细节
- 质量验证：所有新建/更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/矩阵分析/06_fischer_minimax_theorem_1905.md

- 处理源文件：Fischer极大极小定理（06_fischer_minimax_theorem_1905.md）——来源切换至矩阵分析系列
- 创建新实体页面：2 个
  - [[恩斯特·菲舍尔]]：极大极小定理（1905）和Riesz-Fischer定理（1907）提出者，含生平（维也纳→布尔诺→埃尔朗根）、两项贡献详述、历史地位
  - [[瑞利勋爵]]：Lord Rayleigh，1877年《声音的理论》引入Rayleigh商，含基频变分原理、局限性（只能处理极端特征值）与Fischer的关系
- 创建新概念页面：2 个
  - [[极大极小定理]]：Fischer minimax theorem（λ_k = max min R(x)），含精确陈述（max-min和min-max两种等价形式）、证明核心（维数论证）、Cauchy交错定理推论、Weyl扰动不等式、Courant-Fischer推广、鞍点博弈视角、三大瓶颈对比表、应用矩阵表（PCA/Lanczos/量子化学/图谱/有限元/信号处理）、局限性
  - [[Rayleigh商]]：R(x)=xᵀAx/xᵀx，含定义、性质表（值域/最大最小/临界点）、加权平均表达、物理起源（刚度/质量矩阵）、梯度与临界点、Rayleigh-Ritz迭代（三次收敛）、PCA应用
- 更新 index.md：添加4个新页面条目，统计数字 52→56（实体 24→26，概念 28→30）
- 矛盾检查：无矛盾；本次为全新领域（矩阵分析），与已有概率论内容无重叠
- 质量验证：所有新建页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/矩阵分析/07_perron_positive_matrices_1907.md

- 源文件：Perron正矩阵定理：从连分数到谱理论的意外发现（Oskar Perron, 1907）
- 创建新实体页面：2 个
  - [[奥斯卡·佩龙]]：德国数学家（1880–1975），1907年正矩阵特征值定理作者，连分数专著作者，曾随Hilbert研习
  - [[格奥尔格·弗罗贝尼乌斯]]：德国数学家（1849–1917），1908–1912年将Perron定理推广至非负矩阵，创立群表示论特征标理论
- 创建新概念页面：2 个
  - [[Perron-Frobenius定理]]：正/不可约非负矩阵的谱结构定理，含Perron原始版本（正矩阵）和Frobenius推广（不可约非负），核心应用（Markov链、PageRank、Leontief、Leslie矩阵）、多种证明流派（极大极小、Brouwer、Wielandt）、Krein-Rutman无穷维推广
  - [[谱半径]]：ρ(A)=max|λ|，Gelfand公式，Perron根与谱间隙，幂法收敛分析，稳定性判据
- 更新已有概念页面：1 个
  - [[极大极小定理]]：新增 relates_to → [[Perron-Frobenius定理]]（Wielandt 1950年用Frobenius极大极小思想证明Perron定理）
- 更新 index.md：添加4个新页面条目，统计数字 56→60（实体 26→28，概念 30→32）
- 矛盾检查：无矛盾；[[极大极小定理]]页面提及Frobenius的极大极小刻画，与新内容一致
- 质量验证：所有新建页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/矩阵分析/08_schur_unitary_triangularization_1909.md

- 源文件：Schur酉三角化定理：矩阵分解理论的基石（Issai Schur, 1909）
- 创建新实体页面：1 个
  - [[伊赛·舒尔]]：俄裔德国数学家（1875–1941），Frobenius学生，1909年酉三角化定理作者，Schur引理、Schur正交关系、Schur多项式等20+概念命名者，1935年被纳粹强制退休，1939年流亡巴勒斯坦
- 创建新概念页面：3 个
  - [[Schur分解]]：A=QTQ*，任意复方阵酉相似于上三角矩阵，含定理精确陈述、归纳证明（Gram-Schmidt+代数基本定理）、Schur不等式（Σ|λi|²≤‖A‖F²）、正规矩阵刻画、与Jordan形对比表、Schur补定义、应用（QR算法/矩阵函数/控制理论/特征值定位）、局限性（非唯一/实数域/不变子空间问题）
  - [[QR算法]]：Francis&Kublanovskaya 1961年独立发明，反复QR分解收敛至Schur形，20世纪十大算法，含基本迭代、收敛条件、带位移改进、Hessenberg预处理、现代LAPACK/MATLAB/NumPy接口、与幂法/LR算法/Lanczos/Arnoldi的关系
  - [[正规矩阵]]：A*A=AA*，可酉对角化的精确刻画，含子类分类表（Hermite/反Hermite/酉/实对称/实正交）、谱定理（特征投影展开）、Schur不等式等号条件、非正规矩阵的伪谱分析方向、应用（量子力学/PCA/图谱/数值稳定性）
- 更新已有实体页面：1 个
  - [[格奥尔格·弗罗贝尼乌斯]]：新增 relates_to → [[伊赛·舒尔]]（Schur是Frobenius的博士生，1901年）
- 更新 index.md：添加4个新页面条目（1实体+3概念），统计数字 60→65（实体 28→29，概念 32→35）
- 矛盾检查：无矛盾；[[极大极小定理]]页面提及Weyl扰动不等式的"定理3"在Schur不等式语境中有关联，但无矛盾，均正确
- 质量验证：所有新建页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/矩阵分析/09_weyl_eigenvalue_inequalities_1912.md

- 源文件：Weyl特征值不等式：矩阵扰动理论的开山之作（Hermann Weyl, 1912）
- 创建新实体页面：1 个
  - [[赫尔曼·外尔]]：德国数学家（1885–1955），"最后一位数学全才"，Hilbert的学生，1912年发表Weyl渐近律和特征值不等式，后在ETH/哥廷根/普林斯顿高等研究院工作，在规范场论、李群表示论、微分几何、数论均有奠基性贡献
- 创建新概念页面：2 个
  - [[Weyl特征值不等式]]：Hermitian矩阵加法不等式（λ_{i+j-1}(A+B)≤λ_i(A)+λ_j(B)）和扰动界（max|Δλi|≤‖E‖₂），证明基于Fischer极大极小+子空间维数论证，含推广体系（Hoffman-Wielandt/Lidskii/Davis-Kahan/Kato）、Horn猜想（1999年Knutson-Tao蜂巢模型解决）、应用（数值算法/量子力学/随机矩阵/PCA/谱聚类）
  - [[矩阵扰动理论]]：特征值/子空间/奇异值在矩阵扰动下的稳定性理论，含Hermitian体系（Weyl/HW/Lidskii/Davis-Kahan）、一般矩阵（Bauer-Fike/伪谱）、Kato无穷维推广、数值分析应用
- 更新已有概念页面：1 个
  - [[极大极小定理]]：新增 relates_to → [[Weyl特征值不等式]]（Weyl证明其不等式的核心工具）
- 更新 index.md：添加3个新页面条目（1实体+2概念），统计数字 65→68（实体 29→30，概念 35→37）
- 矛盾检查：无矛盾；[[极大极小定理]]页面的"Weyl扰动不等式"段落已提及此定理，与新内容一致，无矛盾
- 质量验证：所有新建页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/矩阵分析/10_frobenius_nonnegative_matrices_1912.md

- 源文件：Frobenius非负矩阵理论：Perron-Frobenius定理的完成（Georg Frobenius, 1912）
- 创建新概念页面：1 个
  - [[不可约矩阵]]：非负矩阵的关联有向图强连通，Frobenius 1912年核心概念（原文"unzerlegbar"），含代数/图论/幂次三种等价定义、可约性分块上三角分类、本原矩阵子类（h=1）、Wielandt指数上界（n²-2n+2）、周期h的谱结构表、Markov链/PageRank/谱聚类应用
- 更新已有实体页面：1 个
  - [[格奥尔格·弗罗贝尼乌斯]]：source_count 1→2，新增来源，新增"1912年论文方法论特征"小节（代数化不可约性定义、Collatz-Wielandt公式预影、Laurent展开工具、分块循环标准形）、新增Frobenius轻视应用但成果被广泛应用的历史悖论注记
- 更新已有概念页面：2 个
  - [[Perron-Frobenius定理]]：source_count 1→2，新增来源，Wielandt证明段补充Collatz-Wielandt变分公式 $r=\max_{x\geq0}\min_i(Ax)_i/x_i$，新增应用（统计力学/符号动力学/正系统/特征向量中心性），新增局限性（NIEP开放问题），新增 relates_to → [[不可约矩阵]]
  - （[[不可约矩阵]] 的 relates_to 已建立对 Perron-Frobenius定理 的双向链接）
- 更新 index.md：添加1个新页面条目（概念），统计数字 68→69（概念 37→38）
- 矛盾检查：无矛盾；本源文件是 07_perron_positive_matrices_1907.md 的直接延续，内容完全一致
- 质量验证：所有新建/更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/矩阵分析/11_von_neumann_trace_inequality_1937.md

- 源文件：Von Neumann迹不等式（1937）：奇异值与矩阵内积的深层联系（John von Neumann, 1937）
- 创建新概念页面：2 个
  - [[Von Neumann迹不等式]]：|tr(A*B)|≤Σσᵢ(A)σᵢ(B)，含主定理精确陈述与等号条件（共享奇异向量对）、极值等价形式、证明思路（SVD→双随机矩阵→Birkhoff定理→排序不等式）、酉不变范数与对称规范函数对应关系、Schatten范数族（核/Frobenius/谱范数对比表）、Mirsky简化证明（1975）、推广（Ky Fan k-范数/Kristof多矩阵/Schatten类）、应用（矩阵补全/PCA/量子信息/核范数正则化）、局限性
  - [[奇异值分解]]：A=UΣV*，含历史渊源表（Beltrami1873→Schmidt1907→Eckart-Young1936→von Neumann1937→Golub-Kahan1965）、几何意义（秩1分解之和）、关键性质、Eckart-Young定理（截断SVD最优低秩逼近，Mirsky推广至所有酉不变范数）、与Schur分解关系、奇异值与特征值的Weyl不等式、Golub-Kahan算法与随机化SVD、应用（图像压缩/推荐系统/PCA/LSA/量子纠缠Schmidt分解）
- 更新已有实体页面：1 个
  - [[约翰·冯·诺依曼]]：source_count 1→2，新增来源，新增迹不等式论文相关条目（1937年/托木斯克发表/普林斯顿高等研究院背景/与Murray算子代数合作），新增 relates_to → [[Von Neumann迹不等式]]和[[奇异值分解]]，扩展来源和相关列表
- 更新 index.md：添加2个新页面条目（概念），统计数字 69→71（概念 38→40）
- 矛盾检查：无矛盾；[[约翰·冯·诺依曼]]旧页面关于数值分析的内容与新增矩阵分析内容完全正交，无冲突
- 质量验证：所有新建/更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/矩阵分析/12_ky_fan_matrix_inequalities_1951.md

- 源文件：Ky Fan矩阵不等式（1949-1951）：特征值部分和与范数理论的统一（Ky Fan 樊畿，1949-1951）
- 创建新实体页面：1 个
  - [[樊畿]]：美籍华裔数学家（1914–2010），杭州出生/北大本科/巴黎大学博士（Fréchet指导）/普林斯顿高等研究院成员（与von Neumann和Weyl密切交流，直接触发矩阵不等式研究），圣母大学→UCSB，Ky Fan不动点定理、凸分析、不动点理论、126篇论文、23名研究生
- 创建新概念页面：2 个
  - [[Ky Fan不等式]]：三个核心定理——Fan极值原理（Σλᵢ=max k维限制迹，纯极大取代Courant-Fischer的极大极小）、Fan部分和不等式（Σλᵢ(A+B)≤Σλᵢ(A)+Σλᵢ(B)，等价于弱majorization，含k=1退化为Weyl、k=n为等式的分析）、Fan k-范数（前k大奇异值之和）与Fan控制定理（k-范数全控制⟺所有酉不变范数全控制，Fan范数为酉不变范数锥极端射线）；Horn猜想关系；PCA/量子信息/MIMO/核范数正则化应用
  - [[优化控制序]]：Majorization x≺y定义（前k项降序和不等式+总和相等）与弱控制序，Birkhoff定理等价（双随机矩阵），Schur-凸函数，矩阵分析中的三大控制关系（Ky Fan/Lidskii/Schur-Horn定理），Horn猜想完整刻画，量子信息/热力学/优化应用
- 更新已有概念页面：2 个
  - [[Weyl特征值不等式]]：在"推广与加强"表中新增Fan部分和不等式行（1949年，将逐项控制提升为部分和控制）
  - [[Von Neumann迹不等式]]：在"主要推广"段新增Fan矩阵不等式（1949-1951）段落，说明Fan是von Neumann思想在范数理论中的系统延伸
- 更新 index.md：添加3个新页面条目（1实体+2概念）+1个已有实体，统计数字 71→75（实体 30→31，概念 40→42）
- 矛盾检查：无矛盾；[[Weyl特征值不等式]]和[[Von Neumann迹不等式]]已有的内容与新增信息完全一致和互补
- 质量验证：所有新建/更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/矩阵分析/13_hoffman_wielandt_theorem_1953.md

- 源文件：Hoffman-Wielandt定理（1953）：正规矩阵特征值扰动的最优估计（Hoffman & Wielandt, 1953）
- 创建新实体页面：1 个
  - [[赫尔穆特·维兰特]]：德国数学家（1910–2001），柏林大学博士（Schur学术圈），战时接触特征值数值计算，1950年"Collatz-Wielandt变分公式"给出Perron-Frobenius定理简洁新证（含本原矩阵指数上界n²-2n+2），1953年与Alan J. Hoffman（Birkhoff博士生，IBM Watson/NIST，Linear Algebra and its Applications创刊主编）合作三页论文
- 创建新概念页面：1 个
  - [[Hoffman-Wielandt定理]]：正规矩阵最优特征值配对扰动界，min_π Σ|λᵢ-μπ(ᵢ)|²≤‖A-B‖F²，等号条件（AB=BA，共享特征向量），与Weyl不等式详细对比（逐个vs整体/谱范数vs Frobenius/Hermitian vs正规）、完整证明思路（酉对角化→双随机矩阵→Birkhoff定理→凸优化转组合优化→指派问题），2-Wasserstein距离联系，非正规矩阵局限性（Jordan块反例），应用（QR算法误差分析/高维统计/随机矩阵/量子信息/网络科学）
- 更新已有概念页面：1 个
  - [[矩阵扰动理论]]：新增 relates_to → [[Hoffman-Wielandt定理]]，更新Hermitian矩阵扰动结果表（Weyl行细化，新增Hoffman-Wielandt行并注明正规矩阵适用范围和最优配对）
- 更新 index.md：添加2个新页面条目（1实体+1概念），统计数字 75→77（实体 31→32，概念 42→43）
- 矛盾检查：无矛盾；[[矩阵扰动理论]]已有的HW条目（source_count=1）内容正确，本次只是详细化
- 质量验证：所有新建/更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/矩阵分析/14_wilkinson_algebraic_eigenvalue_problem_1965.md

- 源文件：Wilkinson《代数特征值问题》（1965）：数值线性代数的奠基之作（J. H. Wilkinson, 1965）
- 创建新实体页面：1 个
  - [[詹姆斯·威尔金森]]：英国数学家（1919–1986），剑桥三一学院/NPL，与图灵共同参与ACE计算机设计，1970年图灵奖（首位数值分析得主），1969年英国皇家学会院士，《代数特征值问题》（1965，662页，从未绝版），后向误差分析奠基人，Wilkinson位移发明者，Wilkinson-Reinsch手册（EISPACK前身）主编，LAPACK精神之父；Wilkinson多项式经典病态反例
- 创建新概念页面：1 个
  - [[后向误差分析]]：Wilkinson 1965年建立的数值分析核心方法论；正向vs后向误差对比表；后向稳定性精确定义（存在扰动δA使输出为精确解，‖δA‖/‖A‖≤f(n)·εmach）；条件数理论（kappa=‖A‖·‖A⁻¹‖；特征值条件数1/|yᵢᴴxᵢ|；Hermitian矩阵条件数恒为1）；Gauss消去法后向稳定性证明（彻底推翻Hotelling 1943年悲观预言）；正交变换数值优越性（kappa(Q)=1不放大误差）；Wilkinson多项式病态反例；软件遗产链（EISPACK→LINPACK→LAPACK→MATLAB/NumPy）；局限性（稀疏/迭代方法/低精度计算）
- 更新已有概念页面：1 个
  - [[QR算法]]：在"实用改进"节新增Wilkinson位移段落（1965年，三次方渐近收敛，全局收敛保证，1-2次迭代隔离，对称特征值金标准）
- 更新 index.md：添加2个新页面条目（1实体+1概念），统计数字 77→79（实体 32→33，概念 43→44）
- 矛盾检查：无矛盾；[[QR算法]]已有的Francis/Kublanovskaya内容与Wilkinson位移完全互补，无重叠冲突
- 质量验证：所有新建/更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/矩阵分析/15_kato_perturbation_theory_1966.md

- 源文件：加藤敏夫《线性算子的扰动理论》（1966）：从矩阵到算子的扰动分析统一
- 创建新实体页面：1 个
  - [[加藤敏夫]]：日本数学物理学家（1917–1999），东京帝大/东大/UC伯克利，战时患肺结核期间独立完成核心工作，1951年论文证明所有多体Schrödinger算子（原子/分子）本质自伴，1966年《线性算子的扰动理论》（Springer Grundlehren 132，592页，引用21000+次），Kato-Rellich定理/Kato-Birman散射/Kato光滑性/KLMN定理/子空间间距理论，Davis-Kahan定理奠基，Kato光滑效应（1983），1980年Norbert Wiener奖
- 创建新概念页面：1 个
  - [[Kato-Rellich定理]]：自伴算子 $A$ 加上相对界 $a<1$ 的 $A$-有界对称算子 $B$ 仍自伴（在 $D(A)$ 上）；精确数学陈述；1951年应用（多体Coulomb系统自伴性，解决von Neumann未解问题）；与有限维Hermitian矩阵扰动对比表；Rayleigh-Schrödinger微扰级数严格基础（$\lambda_1, \lambda_2$ 公式）；KLMN定理（更奇异势的二次型方法）；本质谱在相对紧扰动下的稳定性；对Davis-Kahan/Reed-Simon/量子化学的影响
- 更新已有概念页面：1 个
  - [[矩阵扰动理论]]：新增 relates_to → [[Kato-Rellich定理]]，更新"Kato算子扰动论"段落（将"加藤敬治"改为[[加藤敏夫]]双链，引用21000+次，Kato-Rellich链接）
- 更新 index.md：添加2个新页面条目（1实体+1概念），统计数字 79→81（实体 33→34，概念 44→45）
- 矛盾检查：无矛盾；"加藤敬治"（旧文）应为"加藤敏夫"（Tosio Kato 正确中文译名），已更正
- 质量验证：所有新建/更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] crystallize | 矩阵谱理论第07-15号文件系列

- 工作记忆：`_memory/working/2026-04-15-02.md`（8条观察，涵盖本次会话全部9次 ingest）
- Synthesis 页面：[[矩阵谱理论的统一叙事]]（wiki/syntheses/）

### 结晶洞见摘要

**主要发现**：1907-1966年的矩阵谱理论形成了一条紧密关联的知识谱系——Perron→Frobenius→Schur→Weyl→von Neumann→Ky Fan→Hoffman-Wielandt→Wilkinson→Kato。每步回应前人留下的理论真空，并为后续工作打开新路径。

**三种证明范式**：
1. 变分/极值（Fischer→Weyl→Ky Fan）——把特征值化为子空间上的极值
2. 酉变换/谱分解（Schur→von Neumann→Wilkinson）——保范变换揭示矩阵结构  
3. 双随机矩阵/Birkhoff（von Neumann→Hoffman-Wielandt）——分析问题→凸优化→组合优化

**隐形主线**：奇异值分解（SVD）连接了所有九个定理，是矩阵谱理论的骨架

**Hermitian矩阵是"安全岛"**：四个独立定理（Weyl/Schur/Hoffman-Wielandt/后向误差分析）从不同角度确认 Hermitian/正规矩阵的特征值对扰动最稳定

**应用收敛性**：九个贡献的应用全部汇聚到同一场景集（Markov链/PageRank/PCA/量子力学/数值线性代数）

- 更新 index.md：添加 synthesis 页面条目，统计 81→82（综合分析 1→2）

## [2026-04-15] ingest | raw/books/数值分析/22_golub_kahan_svd.md

- 处理源文件：Golub-Kahan SVD算法（22_golub_kahan_svd.md）——矩阵计算的"瑞士军刀"
- 注：[[奇异值分解]] 概念页面已存在（source_count: 1，已有 Golub-Kahan 1965 在历史表和算法节中提及）
- 创建新实体页面：2 个
  - [[吉恩·戈卢布]]：斯坦福大学（1932-2007），数值线性代数"教父"，Golub-Kahan算法（1965）+Golub-Reinsch（1970）+Golub-Welsch（1969）+《Matrix Computations》教科书+SIAM主席+国家科学院院士
  - [[威廉·卡汉]]：UC Berkeley（1933-），"浮点运算之父"，1989年图灵奖，IEEE 754浮点标准主要架构师，Kahan求和算法，Golub-Kahan共同作者，Demmel-Kahan高精度SVD（1990）
- 更新已有概念页面：1 个
  - [[奇异值分解]]：source_count 1→2；新增 relates_to → [[吉恩·戈卢布]]（caused）、[[威廉·卡汉]]（caused）、[[Householder变换]]（uses）；补充来源链接；相关列表扩充
- 更新 index.md：添加 2 个新页面条目（实体），统计数字 108→110（实体 42→44）
- 矛盾检查：无矛盾。[[奇异值分解]] 历史表中已正确记录 Golub-Kahan 1965，与新来源一致
- 质量验证：所有新建/更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/数值分析/21_cooley_tukey_fft.md

- 处理源文件：Cooley-Tukey FFT（21_cooley_tukey_fft.md）——O(n log n)算法改变世界
- 注：[[快速傅里叶变换]]、[[约翰·图基]]、[[詹姆斯·库利]] 三个页面已存在（初始批量 ingest 时创建，source_count: 1，内容较简）
- 创建新页面：0 个
- 更新已有概念页面：1 个
  - [[快速傅里叶变换]]：source_count 1→2；大幅扩充：DFT 定义+分治分解公式，蝴蝶运算（butterfly）精确描述，复杂度对比表（$n=1024/65536/10^6$ 的加速倍数），位反转排列（bit-reversal）和旋转因子（twiddle factor），冷战动因（核试验检测）和高斯1805年先驱发现，Danielson-Lanczos联系，完整应用领域表（通信/图像/音频/科学计算/算法），FFT变体（Radix-4/Bluestein/实数FFT/FFTW）；新增 relates_to → [[卡尔·弗里德里希·高斯]]、[[谱方法]]、[[切比雪夫逼近理论]]
- 更新已有实体页面：2 个
  - [[约翰·图基]]：source_count 1→2；丰富关键内容（FFT核心贡献细节/冷战背景/统计学贡献清单/跨学科广度）
  - [[詹姆斯·库利]]：source_count 1→2；丰富关键内容（实现工程细节/就地算法/位反转/旋转因子查找表/1987年回忆文章）
- 矛盾检查：无矛盾。源文件与已有页面内容一致，新来源提供更丰富细节
- 质量验证：所有更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/数值分析/18_householder_transformations.md

- 处理源文件：Householder变换（18_householder_transformations.md）——QR分解的算法基础
- 创建新实体页面：1 个
  - [[阿尔斯顿·豪斯霍尔德]]：美国数学家（1904-1993），橡树岭实验室，数学神经科学转向数值分析，1958年4页论文，Householder研讨会/Householder Prize学科建设贡献
- 创建新概念页面：1 个
  - [[Householder变换]]：定义 H=I-2vv^T/v^Tv，五个性质（对称/正交/对合/det=-1/κ=1），核心技巧（一次反射消去整列），与Givens对比表（O(n^4)→O(n^3)），QR分解算法（隐式表示），Hessenberg化简，与后向误差分析/条件数的联系，应用表（QR/Hessenberg/三对角/SVD/最小二乘/块WY），局限性（稀疏性/并行化）
- 更新已有实体/概念页面：0 个（已有页面[[QR算法]]、[[奇异值分解]]、[[Schur分解]]、[[后向误差分析]]内容完整，无需补充；反向链接已在新页面 relates_to 中建立）
- 更新 index.md：添加 2 个新页面条目（1实体+1概念），统计数字 106→108（实体 41→42，概念 61→62）
- 矛盾检查：无矛盾。Householder变换是对Jacobi旋转方法效率的提升（O(n^4)→O(n^3)），不矛盾，互补关系
- 质量验证：所有新建页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/数值分析/17_lax_equivalence_theorem.md

- 处理源文件：Lax-Richtmyer等价定理（17_lax_equivalence_theorem.md）——"数值分析基本定理"
- 创建新实体页面：1 个
  - [[彼得·拉克斯]]：匈牙利裔美国数学家（1926-），库朗研究所（师承Friedrichs），2005年Abel奖，Lax-Richtmyer等价定理+Lax-Friedrichs格式+Lax-Wendroff格式+双曲守恒律熵条件+可积系统逆散射变换
- 创建新概念页面：1 个
  - [[Lax-Richtmyer等价定理]]：定义三元组（相容性/稳定性/收敛性），定理陈述（充分性证明思路+必要性用Banach-Steinhaus定理），与CFL条件的完美衔接，局限性表，后续影响（GKS理论/FEM推广/Lax-Wendroff定理/现代方法设计哲学）
- 更新已有概念页面：1 个
  - [[CFL条件]]：新增 relates_to → [[Lax-Richtmyer等价定理]]（CFL是稳定性必要条件；等价定理指出不稳定即不收敛）
- 更新 index.md：添加 2 个新页面条目（1实体+1概念），统计数字 104→106（实体 40→41，概念 60→61）
- 矛盾检查：无矛盾。等价定理是对CFL条件和冯·诺依曼稳定性分析的理论升华，前后完全一致
- 质量验证：所有新建/更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/数值分析/15_conjugate_gradient.md

- 处理源文件：共轭梯度法（15_conjugate_gradient.md）——Krylov子空间方法家族的奠基性论文
- 创建新实体页面：3 个
  - [[马格努斯·赫斯坦尼斯]]：UCLA数学家（1906-1991），NBS计算实验室，CG独立发现者，Hestenes-Stiefel公式，合著1952年论文
  - [[爱德华·施蒂费尔]]：ETH Zurich数学家（1909-1978），代数拓扑学（施蒂费尔-惠特尼类），Z4计算机时期独立发展CG，合著1952年论文
  - [[康尼利厄斯·朗佐斯]]：匈牙利裔物理数学家（1893-1974），1950年Lanczos算法（特征值），1952年线性方程组工作，CG-Lanczos深层联系
- 创建新概念页面：2 个
  - [[共轭梯度法]]：算法完整描述（α/β/x/r/p五变量递推），三核心性质（A-共轭/残差正交/Krylov最优），收敛界 2((√κ-1)/(√κ+1))^k，与经典迭代法对比表，历史曲折（1952被忽视→1970s复兴），PCG预处理表，后续方法族（GMRES/BiCGSTAB等），局限性
  - [[Krylov子空间方法]]：K_k(A,v)定义，方法家族完整表（Lanczos/CG/MINRES/Arnoldi/GMRES/BiCGSTAB等），与经典定点迭代的根本区别（子空间累积vs单步更新），CG-Lanczos联系，预处理
- 更新已有实体/概念页面：0 个（已有页面已有足够内容，无需补充）
- 更新 index.md：添加 5 个新页面条目（3实体+2概念），统计数字 97→104（实体 37→40，概念 58→60）
- 矛盾检查：无矛盾。CG比Jacobi收敛更快（O(1/√κ) vs O(1/κ)）——这不是矛盾，已有[[Jacobi迭代法]]页面中已说明其局限性
- 质量验证：所有新建页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/数值分析/14_turing_rounding_errors.md

- 处理源文件：图灵舍入误差分析（14_turing_rounding_errors.md）——条件数概念的最早系统性来源
- 注：[[阿兰·图灵]] 实体页面已存在（初始批量 ingest 时创建，source_count:1）；但关系指向断链 `[[矩阵舍入误差分析]]`，已修复
- 创建新概念页面：1 个
  - [[条件数]]：$\kappa(A)=\|A\|\cdot\|A^{-1}\|$，图灵1948 N(A)定义，病态/良态术语，Turing vs von Neumann定义对比表，与后向误差分析的结合，Hotelling悲观预测被否定（带主元选取的高斯消元法误差不指数增长）
- 更新已有实体页面：1 个
  - [[阿兰·图灵]]：source_count 1→2；大幅扩充（条件数引入、核心洞察、后向误差萌芽、主元选取理论依据、跨领域简介）；修复断链 `[[矩阵舍入误差分析]]` → `[[条件数]]`；更新 relates_to（条件数、后向误差分析、威尔金森、冯·诺依曼）
- 更新已有概念页面：1 个
  - [[后向误差分析]]：source_count 1→2；新增 relates_to → [[阿兰·图灵]]（precursor）和 [[条件数]]（核心工具）；新增"历史谱系"小节（图灵→冯·诺依曼→威尔金森 传承链）
- 更新 index.md：添加 1 个新页面条目（条件数），统计数字 96→97（概念 57→58）
- 断链修复：[[阿兰·图灵]] 中的 `[[矩阵舍入误差分析]]`、`[[图灵机]]`、`[[ENIAC]]`、`[[布莱切利园]]` → 全部替换为已存在的相关概念页面
- 矛盾检查：图灵（确定性最坏情况）与冯·诺依曼-Goldstine（统计误差模型）定义形式不同——互补差异，非矛盾，已在[[条件数]]对比表中明确标注
- 质量验证：所有新建/更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] lint | wiki health check

### 扫描范围
- 总文件数：96（57 概念 + 37 实体 + 2 综合分析）
- 抽样检查：约 30 个页面的 frontmatter 和链接

---

### A. Frontmatter 完整性 ✓
- 所有抽样页面均包含完整 frontmatter（type / status / confidence / created / updated / last_accessed / source_count / tags / relates_to / supersedes）
- 无缺失字段，无格式错误

---

### B. Index 分类错误（已自动修复）
发现 **5 个实体页面** 被错误归入 index.md 的"概念"区段（应在"实体"区段）：

| 页面 | 实际文件路径 | 问题 |
|------|------------|------|
| [[赫尔曼·外尔]] | wiki/entities/ | 误列于概念区 |
| [[樊畿]] | wiki/entities/ | 误列于概念区 |
| [[赫尔穆特·维兰特]] | wiki/entities/ | 误列于概念区 |
| [[詹姆斯·威尔金森]] | wiki/entities/ | 误列于概念区 |
| [[加藤敏夫]] | wiki/entities/ | 误列于概念区 |

**修复**：将以上 5 个条目移至实体区段，概念区段删除对应条目。

---

### C. 统计数字错误（已自动修复）
| 字段 | 旧值 | 新值（正确）|
|------|------|-----------|
| 总页面数 | 100 | 96 |
| 实体 | 38 | 37 |
| 概念 | 57 | 57（不变）|

原因：index 分类错误导致 5 个实体同时在概念区计数，加上历史 ingest 中有 1 次算术错误（96+3 误写为 100）。

---

### D. 断链检查（需人工处理 / 等待 ingest）

发现 **20 个断链**，全部为指向尚未创建的页面。分为两类：

#### 类别 1：待 ingest 时创建（前向引用，已知计划）

这些链接由初始批量 ingest 创建、引用了尚未单独处理的源文件的内容：

| 断链 | 所在页面 | 状态 |
|------|---------|------|
| `[[矩阵舍入误差分析]]` | 阿兰·图灵 | 待 `14_turing_rounding_errors.md` ingest |
| `[[图灵机]]` | 阿兰·图灵 | 待 ingest |
| `[[布莱切利园]]` | 阿兰·图灵 | 待 ingest |
| `[[贝尔实验室]]` | 约翰·图基 | 待 `21_cooley_tukey_fft.md` ingest |
| `[[离散傅里叶变换]]` | 约翰·图基、詹姆斯·库利 | 待 ingest |
| `[[IBM沃森研究中心]]` | 詹姆斯·库利 | 待 ingest |

#### 类别 2：需要创建配套页面（关系引用）

这些链接引用了未被收录为独立页面的重要概念/人物：

| 断链 | 所在页面 | 建议处理 |
|------|---------|---------|
| `[[马尔可夫]]` | 帕夫努季·利沃维奇·切比雪夫 | 下次相关 ingest 时创建 A.A. Markov 实体 |
| `[[李雅普诺夫]]` | 帕夫努季·利沃维奇·切比雪夫 | 下次相关 ingest 时创建 A.M. Lyapunov 实体 |
| `[[切比雪夫不等式]]` | 帕夫努季·利沃维奇·切比雪夫 | 概率论概念，待概率论相关文件 ingest |
| `[[龙格-库塔方法]]` | 卡尔·龙格 | 数值 ODE 方法，待相关 ingest |
| `[[ENIAC]]` | 阿兰·图灵, 约翰·冯·诺依曼 | 历史计算机，待计算机史相关 ingest |
| `[[赫尔曼·戈尔茨坦]]` | 约翰·冯·诺依曼 | 待 ingest |
| `[[雅可比矩阵]]` | 卡尔·古斯塔夫·雅各布·雅可比 | 微积分概念，待相关 ingest |
| `[[高斯消元法]]` | 卡尔·弗里德里希·高斯 | 线性代数基础概念，待 ingest |
| `[[骰子问题]]` | 梅雷骑士 | 可能是 [[点数问题]] 的别名，待核实 |
| `[[惯性律]]` | 詹姆斯·约瑟夫·西尔维斯特 | 矩阵理论概念，待矩阵分析 ingest |
| `[[阿瑟·凯莱]]` | 詹姆斯·约瑟夫·西尔维斯特 | Arthur Cayley 实体，待 ingest |
| `[[线性代数]]` | 詹姆斯·约瑟夫·西尔维斯特 | 宽泛学科概念，待处理 |
| `[[非负矩阵]]` | 奥斯卡·佩龙 | 可考虑链接到 [[不可约矩阵]]（已有） |

**建议**：将"非负矩阵"链接改为 [[Perron-Frobenius定理]] 或 [[不可约矩阵]]（均已存在）。

---

### E. 矛盾检查 ✓
- 扫描所有页面的 `relates_to` 中的 `type: contradicts`：无
- 内容交叉检查：无发现内容层面的矛盾

---

### F. 过期检查 ✓
- 无 confidence < 0.3 的页面
- 最低 confidence：梅雷骑士 0.8，菲利普·路德维希·冯·赛德尔 0.8
- 所有页面均为 2026-04-15 创建，无过期风险

---

### G. Orphan 检查（部分）
- 2 个 syntheses 页面通过 relates_to 链接至多个概念/实体，已是知识网络的集成节点
- 数值分析类页面通过连续 relates_to 链已形成连通图（牛顿法 ↔ 欧拉法 ↔ FFT ↔ 有限元 ↔ 高斯求积 ↔ 切比雪夫 ↔ 龙格 ↔ Richardson ↔ CFL ↔ 冯·诺依曼...）
- 概率论类页面形成独立连通组（帕斯卡 ↔ 费马 ↔ 惠更斯 ↔ 伯努利 ↔ 德莫弗 ↔ 拉普拉斯 ↔ 贝叶斯...）
- 矩阵分析类页面通过矩阵谱理论综合分析集成
- 仍有部分轻度孤立节点（梅雷骑士、卢卡·帕西奥利），但已通过 [[点数问题]] 间接连接

---

### 自动修复摘要

| 修复项 | 类型 | 操作 |
|--------|------|------|
| 5 个实体误入概念区段 | index分类 | 移至实体区段，概念区段删除 |
| 统计数字（总页面数、实体数） | index统计 | 更正为 96 / 37 |

### 未修复摘要

| 问题 | 数量 | 原因 |
|------|------|------|
| 断链（待 ingest） | 6个 | 等待相应源文件处理 |
| 断链（需创建页面） | 14个 | 需要新的 raw 材料或专项创建 |
| 轻度孤立页面 | ~2个 | 属于合理的专门领域知识 |

## [2026-04-15] ingest | raw/books/数值分析/13_von_neumann_stability.md

- 处理源文件：冯·诺依曼稳定性分析（13_von_neumann_stability.md）——PDE数值格式稳定性与矩阵误差分析的奠基工作
- 注：本源文件是 [[冯·诺依曼稳定性分析]] 的主要来源；该概念页面已在上一次 ingest（11_cfl_condition.md）中创建
- 创建新页面：0 个（所有相关概念页面已存在）
- 更新已有概念页面：1 个
  - [[冯·诺依曼稳定性分析]]：source_count 1→2；新增关键扩充：
    - FTCS 扩散格式完整示例（$g(\xi) = 1 - 4r\sin^2(\xi\Delta x/2)$，稳定条件 $r\leq 1/2$，抛物约束 $\Delta t \leq (\Delta x)^2/(2\nu)$）
    - 矩阵计算误差分析 1947 论文详述（条件数定义、误差界定理、统计舍入误差模型）
    - 洛斯阿拉莫斯历史背景（1944-1947 曼哈顿计划内部报告起源）
    - GKS 理论、修正方程等局限性补充
    - 新增 relates_to → [[后向误差分析]]（冯·诺依曼是 Wilkinson 的直接前驱）
- 更新已有实体页面：1 个
  - [[约翰·冯·诺依曼]]：source_count 2→3；新增"矩阵计算误差分析"详细内容节（条件数、误差界定理、统计模型），首次数值天气预报（1950, ENIAC, Charney+Fjortoft），与[[刘易斯·弗赖·理查森]]遗产的联系
- 更新 index.md：更新 [[冯·诺依曼稳定性分析]] 条目描述，补充 FTCS 示例和矩阵条件数要点
- 矛盾检查：无矛盾。统计误差模型（冯·诺依曼）vs 确定性后向误差分析（Wilkinson）是方法论层面的不同取向，不构成矛盾，两者已在相关页面中明确区分

## [2026-04-15] ingest | raw/books/数值分析/11_cfl_condition.md

- 处理源文件：CFL条件（11_cfl_condition.md）——计算科学最重要的稳定性约束
- 创建新实体页面：1 个
  - [[理查德·柯朗]]：普鲁士裔美国应用数学家（1888-1972），希尔伯特学生，哥廷根数学研究所32岁所长，Courant-Hilbert《数学物理方法》(1924)，1933年被纳粹驱逐，创立库朗数学科学研究所（NYU），CFL条件三位作者之首
- 创建新概念页面：2 个
  - [[CFL条件]]：CFL数 ν=cΔt/Δx≤1，依赖域论证（数值依赖域必须包含物理依赖域），1928年纯数学PDE存在性证明的"副产品"，必要非充分，理查森1922年天气预报失败原因解释，显式vs隐式权衡核心，CFD/FDTD/天气/地震等广泛应用，Lax等价定理（1956）升级为充要条件
  - [[冯·诺依曼稳定性分析]]：误差傅里叶展开，放大因子g(ξ)，稳定判据|g(ξ)|≤1，与CFL条件比较表（几何论证vs代数计算），Lax-Friedrichs格式验证，局限性（线性/常系数/周期边界）；同时补全了已有[[约翰·冯·诺依曼]]实体页面中的悬空双链
- 更新已有实体页面：1 个
  - [[刘易斯·弗赖·理查森]]：新增 relates_to → [[CFL条件]]（1922年天气预报违反CFL条件），补充相关列表
- 更新 index.md：添加 3 个新页面条目（1实体+2概念），统计数字 96→100（实体 37→38，概念 55→57）
- 矛盾检查：无矛盾。注意：[[约翰·冯·诺依曼]]实体页面早于本次 ingest 就已有 relates_to 指向 [[冯·诺依曼稳定性分析]]，该悬空链接现已被本次创建的概念页补全
- 质量验证：所有新建页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/数值分析/10_richardson_extrapolation.md

- 处理源文件：Richardson外推法（10_richardson_extrapolation.md）——数值分析最通用的"元方法"
- 创建新实体页面：1 个
  - [[刘易斯·弗赖·理查森]]：英国科学家（1881–1953），贵格会，剑桥国王学院，Richardson外推法（1911/1927），《天气预报的数值过程》（1922）先知，分形理论和冲突数学建模先驱，和平主义科学家典范
- 创建新概念页面：2 个
  - [[Richardson外推法]]：误差渐近展开 $A(h)=A^*+a_1h^p+O(h^{p+1})$，代数消元公式 $(2^p\cdot A(h/2)-A(h))/(2^p-1)$，递归外推表，Richardson误差估计，局限性（渐近展开假设/舍入抵消/高维成本），完整后续发展表（Romberg/Bulirsch-Stoer/嵌入式RK/CFD-GCI/AMR）
  - [[Romberg积分]]：梯形法则+欧拉-麦克劳林展开（只含偶数次幂）+Richardson递归外推，外推表结构，节点嵌套优势（每层只计算新节点），与高斯求积详细对比表，局限性（奇异函数/高维/舍入误差）
- 更新已有实体/概念页面：0 个（Richardson在源文件中提及了Jacobi迭代、Gauss-Seidel、高斯求积，但已有页面内容完整，无需更新）
- 更新 index.md：添加 3 个新页面条目，统计数字 93→96（实体 36→37，概念 53→55）
- 矛盾检查：无矛盾。源文件提到理查森1911年论文中也发展了迭代法，与已有[[Jacobi迭代法]]页面（提及雅可比1845年）不矛盾——理查森是独立平行发展改良变体，非否定雅可比的优先性
- 质量验证：所有新建页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/数值分析/09_runge_phenomenon.md

- 处理源文件：龙格现象（09_runge_phenomenon.md）——等距插值发散的经典反例
- 创建新实体页面：1 个
  - [[卡尔·龙格]]：德国应用数学家（1856-1927），1901年论文，师承魏尔斯特拉斯，哥廷根大学首位应用数学教授，龙格现象 + 龙格-库塔方法双贡献，复平面极点视角洞见
- 创建新概念页面：2 个
  - [[勒贝格常数]]：$\Lambda_n = \max\sum|L_k(x)|$，插值误差放大因子，等距节点指数增长（$\sim 2^{n+1}/(e\cdot n\ln n)$）vs 切比雪夫节点对数增长（$\sim (2/\pi)\ln(n+1)+C$），是龙格现象的深层数学机制
  - [[样条方法]]：分段低次多项式（三次样条/B样条/NURBS），Schoenberg 1946年系统建立，对龙格现象的直接回应，CAD/计算机图形学基础，与有限元等几何分析（IGA）的关系
- 更新已有概念页面：1 个
  - [[龙格现象]]：大幅扩充 source_count 1→2；新增：勒贝格常数（指数增长机制）、复平面极点视角（Bernstein椭圆，$z=\pm i/5$距实轴0.2）、端点误差数值量化表（$n=10/20/40$）、三大教训（与机器学习过拟合对应）、梅赫勒/博雷尔前驱工作注记；新增 relates_to：[[卡尔·龙格]]、[[勒贝格常数]]、[[样条方法]]
- 更新 index.md：添加 3 个新页面条目（1实体+2概念），统计数字 89→93（实体 35→36，概念 51→53）
- 矛盾检查：无矛盾；已有[[龙格现象]]页面内容与新来源完全一致，新来源提供更多深层解析
- 质量验证：所有新建/更新页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/数值分析/07_chebyshev_approximation.md

- 处理源文件：切比雪夫逼近理论（07_chebyshev_approximation.md）——逼近论的数学基石
- 注：[[帕夫努季·利沃维奇·切比雪夫]] 实体页面已存在（source_count: 1），本次深度处理同一源文件
- 创建新概念页面：4 个
  - [[切比雪夫逼近理论]]：最佳一致逼近（L∞ minimax）问题定义、等振荡定理（充要条件，1854/1905）、切比雪夫节点最优插值性、切比雪夫级数展开、与L²逼近对比、应用表（数学函数库/谱方法/Clenshaw-Curtis/Remez算法/有理逼近）、局限性（多元/非光滑/计算复杂性）
  - [[切比雪夫多项式]]：定义 T_n(x)=cos(n arccos x)，三项递推关系，五个核心性质（有界/等振荡/零点/正交/minimax），与傅里叶级数的联系（x=cosθ变量替换），Gauss-Chebyshev求积，切比雪夫展开快速收敛
  - [[龙格现象]]：Carl Runge 1901年发现，龙格函数1/(1+25x²)，等距节点端点发散的数学根源（ω_{n+1}(x)在端点极大），切比雪夫节点作为根本解法
  - [[谱方法]]：全局基函数展开，指数级精度（对光滑解），傅里叶（周期域）vs 切比雪夫（非周期域）谱方法，Clenshaw-Curtis求积，配点法vs Galerkin，Chebfun，局限（复杂几何/Gibbs现象）
- 更新已有实体页面：1 个
  - [[帕夫努季·利沃维奇·切比雪夫]]：新增 relates_to → [[切比雪夫多项式]]（caused）、[[谱方法]]（caused），丰富关键内容（核心论文细节、研究风格、历史地位、现代遗产）
- 更新已有概念页面：1 个
  - [[高斯求积公式]]：新增 relates_to → [[切比雪夫逼近理论]]（Clenshaw-Curtis求积连接）
- 更新 index.md：添加 4 个新页面条目，统计数字 85→89（概念 47→51）
- 矛盾检查：无矛盾；[[高斯求积公式]]已有 Gauss-Chebyshev 条目，与新增内容完全一致
- 质量验证：所有新建页面满足 _schema/quality-rules.md 要求

## [2026-04-15] ingest | raw/books/数值分析/06_jacobi_iteration.md

- 处理源文件：Jacobi迭代法（06_jacobi_iteration.md）——迭代线性代数的奠基性工作
- 注：[[卡尔·古斯塔夫·雅各布·雅可比]] 实体页面已存在且已包含此来源（source_count: 2），无需更新来源
- 创建新概念页面：2 个
  - [[Jacobi迭代法]]：矩阵分裂 A=D+L+U，同时更新迭代格式，收敛充要条件（谱半径<1），对角占优充分条件，加权Jacobi/SOR前身，并行计算优势，历史影响链（Gauss-Seidel→SOR→矩阵分裂理论→Krylov预条件→多重网格光滑子→GPU计算→异步迭代）
  - [[Gauss-Seidel方法]]：逐次位移法，1874年赛德尔发表，使用最新分量值，通常收敛更快，存在顺序依赖，SOR方法的直接前身，命名争议（高斯未必实际使用）
- 创建新实体页面：1 个
  - [[菲利普·路德维希·冯·赛德尔]]：德国数学家（1821-1896），慕尼黑大学，逐次位移法正式发表者，1874年论文
- 更新已有概念页面：1 个
  - [[谱半径]]：新增 relates_to → [[Jacobi迭代法]]（迭代矩阵谱半径<1 是收敛充要条件），source_count 不变（已在应用表中提及 Jacobi 迭代）
- 更新已有实体页面：1 个
  - [[卡尔·古斯塔夫·雅各布·雅可比]]：补充相关页面链接（[[菲利普·路德维希·冯·赛德尔]]、[[Gauss-Seidel方法]]）
- 更新 index.md：添加 3 个新页面条目，统计数字 82→85（实体 34→35，概念 45→47）
- 矛盾检查：无矛盾，内容与已有[[卡尔·古斯塔夫·雅各布·雅可比]]和[[谱半径]]完全一致并互补
- 质量验证：所有新建页面满足 _schema/quality-rules.md 要求（完整frontmatter，概述≤200字，≥1来源，≥1 relates_to，中文为主）

## [2026-04-15] consolidate | 日常整合（会话 2026-04-15-02）

### Step 1: Working → Episodic 压缩
- 处理工作记忆：`2026-04-15-02`（status: unprocessed → processed）
- 合并到 `_memory/episodic/2026-04-15.md`（更新 source_sessions, access_count, confidence）
- 新增观察：O7-O14（8条，涵盖矩阵谱理论历史谱系、工具分离思维跨域复现、SVD隐形主线、"战时数学"模式等）
- `2026-04-15-01` 已在前次整合中处理（status: processed）

### Step 2: Episodic → Semantic 晋升
- **未执行**：仅有 1 天情节记忆（2026-04-15），需 3+ 天才可晋升
- **候选模式记录**（等待积累）：
  - 工具分离思维（O3+O9，2次跨领域出现）
  - 知识谱系优先（O7+synthesis结构，2次）
  - 纯粹理论→意外应用（O2+O8，2次）

### Step 3: 置信度衰减
- 语义记忆条目数：0（无内容需衰减）

### Step 4: Journal 模式扫描
- 无 `journal/daily/` 文件（用户尚未开始日记记录）
- 更新 `journal/growth/skills-tracker.md`：新增领域（矩阵分析、数值线性代数、量子力学数学基础）
- 更新 `journal/growth/cognitive-patterns.md`：发现3个认知模式（工具分离思维、知识谱系优先、纯粹理论驱动），2个待观察候选

### Step 5: 深度整合（--deep 未触发）
- 跳过

### 更新
- `dashboard.md`：知识库概览全面更新（82页，候选 semantic 晋升记录）
- 统计：处理 1 个 working（2026-04-15-02），晋升 0 个 semantic，衰减 0 个

## 2026-04-15 13:45:00 — Batch Ingest (Qwen API)

**Source**: raw/articles/CLI-tools/
**Method**: wiki:ingest-loop-qwen
**Model**: qwen3.5-plus
**Status**: Completed

### Processed Files (3/3)

✅ **SUCCESS**: bun-vs-uv.md → wiki/concepts/bun-vs-uv.md
✅ **LINT_WARNING**: claude-cli-tools.md → wiki/concepts/claude-cli-tools.md (overview too long)
✅ **SUCCESS**: modern-cli-tools.md → wiki/concepts/modern-cli-tools.md

### Summary

- Total files: 3
- Successful: 2
- With warnings: 1
- Failed: 0
- BM25 index: Updated for all 3 files

## 2026-04-15 14:00:00 — lint

**扫描**: 121 个页面  
**ERROR**: 0 个 | **WARNING**: 524 个 | **INFO**: 0 个  
**自动修复**: 0 个  
**需要人工处理**: 524 个

### 问题分类统计

| 问题类型 | 数量 | 说明 |
|---------|------|------|
| F3 - Overview 过长 | 47 | 概述超过 200 字符限制 |
| F4 - 空章节 | 312 | 页面存在空章节 |
| B1 - 断链 | 86 | 链接指向不存在的页面 |
| B2 - BM25 缺失 | 10 | 页面未在 BM25 索引中 |
| I1 - 未列入 index | 49 | 页面未在 index.md 中列出 |
| I2 - index 过期条目 | 4 | index.md 中存在已删除页面的链接 |
| O1 - 孤页 | 16 | 没有入站链接的页面 |

### 关键问题详情

#### 1. BM25 索引缺失 (10 个文件)
以下页面存在于 wiki/ 但不在 BM25 索引中：
- wiki/concepts/概率公理体系.md
- wiki/concepts/切比雪夫不等式.md
- wiki/concepts/马尔可夫链.md
- wiki/concepts/Laplace变换.md
- wiki/concepts/最大似然原理.md
- wiki/concepts/泊松分布.md
- wiki/entities/埃米尔·博雷尔.md
- wiki/entities/安德烈·马尔可夫.md
- wiki/entities/安德烈·柯尔莫哥洛夫.md
- wiki/entities/西梅翁·泊松.md

**建议**: 运行 `python3 scripts/bm25_index.py update <file>` 为每个文件更新索引

#### 2. 孤页问题 (16 个页面)
这些页面没有被任何其他页面链接：
- wiki/concepts/bun-vs-uv.md (新创建的 CLI 工具对比)
- wiki/concepts/claude-cli-tools.md (新创建的 CLI 工具全景)
- wiki/concepts/modern-cli-tools.md (新创建的 CLI 工具指南)
- wiki/concepts/切比雪夫不等式.md
- wiki/concepts/概率公理体系.md
- wiki/concepts/泊松分布.md
- wiki/entities/卢卡·帕西奥利.md
- wiki/entities/梅雷骑士.md
- wiki/syntheses/DeepAgents评估设计哲学.md
- wiki/syntheses/矩阵谱理论的统一叙事.md

**建议**: 在相关主题页面中添加双向链接

#### 3. 断链问题 (86 个链接)
部分链接指向不存在的页面，例如：
- wiki/concepts/bun-vs-uv.md: [[Bun]], [[uv]], [[npm]], [[pip]] 等 8 个断链
- wiki/concepts/claude-cli-tools.md: [[Claude Code]], [[Aider]], [[MCP 协议]] 等 5 个断链
- wiki/concepts/modern-cli-tools.md: [[ripgrep]], [[fd]], [[bat]] 等 8 个断链
- wiki/concepts/递推方法.md: [[后向归纳法]]
- wiki/concepts/组合枚举法.md: [[组合数学]]

**建议**: 创建缺失的页面或修正链接名称

#### 4. 空章节问题 (312 个空章节)
大量页面存在空章节，特别是：
- 概念页面缺少 "关键内容" 章节
- 实体页面缺少 "关键内容" 章节
- 合成页面缺少具体内容

**建议**: 填充内容或删除空章节

#### 5. Overview 过长 (47 个页面)
页面概述超过 200 字符限制，例如：
- wiki/concepts/claude-cli-tools.md: 341 字符
- wiki/concepts/bun-vs-uv.md: 297 字符
- wiki/concepts/modern-cli-tools.md: 292 字符

**建议**: 精简概述内容

### 自动修复操作

本次 lint 未执行自动修复。建议运行：
```bash
# 更新 BM25 索引（10 个文件）
for file in wiki/concepts/概率公理体系.md wiki/concepts/切比雪夫不等式.md wiki/concepts/马尔可夫链.md wiki/concepts/Laplace变换.md wiki/concepts/最大似然原理.md wiki/concepts/泊松分布.md wiki/entities/埃米尔·博雷尔.md wiki/entities/安德烈·马尔可夫.md wiki/entities/安德烈·柯尔莫哥洛夫.md wiki/entities/西梅翁·泊松.md; do
  python3 scripts/bm25_index.py update "$file"
done

# 重建图谱
python3 scripts/build_graph.py
```

### 优先级建议

**高优先级**:
1. 修复 BM25 索引缺失（影响搜索功能）
2. 处理孤页问题（提高知识连通性）
3. 修复新创建 CLI 工具页面的断链

**中优先级**:
4. 填充空章节（提高内容质量）
5. 精简过长的概述

**低优先级**:
6. 清理 index.md 中的过期条目

## [2026-04-15 15:00] lint | 全库健康检查

- 扫描: 121 个页面
- ERROR: 0 个 | WARNING: 175 个 | INFO: 0 个
- 自动修复: 10 个（BM25 索引同步）
- 需要人工处理: 1 个（index.md 权限待批）

### 详细问题

**B2 — BM25 缺失（已修复 10 个）**
- wiki/concepts/Laplace变换.md ✓
- wiki/concepts/切比雪夫不等式.md ✓
- wiki/concepts/最大似然原理.md ✓
- wiki/concepts/概率公理体系.md ✓
- wiki/concepts/泊松分布.md ✓
- wiki/concepts/马尔可夫链.md ✓
- wiki/entities/埃米尔·博雷尔.md ✓
- wiki/entities/安德烈·柯尔莫哥洛夫.md ✓
- wiki/entities/安德烈·马尔可夫.md ✓
- wiki/entities/西梅翁·泊松.md ✓

**I2 — 过期索引条目（需人工）**
- index.md 第 27 行：模板注释 `[[页面名]]` 触发检测，建议删除该注释行

**O1 — 孤页（8 个，无入链）**
- wiki/syntheses/DeepAgents评估设计哲学.md
- wiki/concepts/bun-vs-uv.md
- wiki/concepts/claude-cli-tools.md
- wiki/concepts/modern-cli-tools.md
- wiki/entities/卢卡·帕西奥利.md
- wiki/concepts/最大似然原理.md
- wiki/entities/梅雷骑士.md
- wiki/syntheses/矩阵谱理论的统一叙事.md

**B1 — 断链（85 处，65 个唯一目标）**
- 高频缺失页面：[[数值分析]]、[[线性代数]]、[[矩阵]]、[[马尔可夫]]、[[离散傅里叶变换]]
- CLI 相关：[[Bun]]、[[uv]]、[[Node.js]]、[[Python]]、[[Rust]]、[[ripgrep]] 等
- 人物缺失：[[约瑟夫·拉弗森]]、[[托马斯·辛普森]]、[[赫尔曼·戈尔茨坦]]、[[阿瑟·凯莱]] 等

**F3 — 概述超长（71 个，均为 WARNING）**
- 超出 200 字符限制，不影响功能，建议按需精简

**图谱连通性（H）**
- 5 个连通分量：
  - 3 个单节点孤立：bun-vs-uv.md、claude-cli-tools.md、modern-cli-tools.md
  - 1 个 8 节点群：DeepAgents 相关页面（独立主题）
  - 1 个主群：110 节点（数学/概率知识库）

## [2026-04-15 15:30] ingest | raw/books/概率论/13_wiener_brownian_motion.md

- 处理源文件：Wiener 过程与布朗运动（13_wiener_brownian_motion.md）
- 创建新实体页面：2 个
  - [[诺伯特·维纳]]：MIT 数学家（1894–1964），Wiener 过程创立者，控制论奠基人
  - [[路易·巴舍利耶]]：法国数学家，1900 年博士论文首次将布朗运动类随机过程用于股价建模
- 创建新概念页面：5 个
  - [[Wiener过程]]：布朗运动的严格数学定义，独立平稳正态增量 + 连续但处处不可微路径
  - [[Wiener测度]]：C₀[0,1] 上的概率测度，无穷维空间第一个严格概率测度（1923）
  - [[Wiener积分]]：路径空间上对确定性函数的积分，Itô 积分的前身
  - [[Itô随机积分]]：Itô（1944）推广 Wiener 积分至随机被积函数，含 Itô 公式
  - [[随机游走]]：每步等概率 ±1 的离散随机过程，Wiener 过程的离散前身
- 更新 index.md：添加 7 个新页面条目，统计从 121→128（实体 48→50，概念 71→76）
- 矛盾检查：未发现矛盾信息（已有马尔可夫链等页面内容相互补充）
- BM25 索引：7 个新页面全部索引成功

## [2026-04-15 15:15] graph
- 构建知识图谱: 128 节点, 828 边, 3 孤页, 5 连通分量

## [2026-04-15] consolidate | 日常整合（第三场 2026-04-15-03）

### Step 1: Working → Episodic 压缩
- 处理工作记忆：`2026-04-15-03`（status: processed，待合并 O15-O19）
- 合并到 `_memory/episodic/2026-04-15.md`（source_sessions → [01, 02, 03], access_count 2→3）
- 新增观察 5 条（O15-O19）：
  - O15｜Wiener 测度：无穷维路径空间概率测度首次严格化（1923）
  - O16｜巴舍利耶反例：应用动机出发需先经纯粹理论"认证"才获接受
  - O17｜随机积分三层发展链：随机游走→Wiener积分→Itô积分（技术障碍逐层突破）
  - O18｜Itô公式：经典链式法则 + 一阶二次变差修正（跨域复现结构）
  - O19｜概率论知识域纵向完整性达成，规模 121→128

### Step 2: Episodic → Semantic 晋升
- **未执行**：仅有 1 个 episodic 文件（2026-04-15），需 3+ 天才可晋升

### Step 3: 置信度衰减
- 语义记忆条目数：0——跳过

### Step 4: Journal 模式扫描
- 无 `journal/daily/` 文件——跳过

### Step 5: 深度整合（--deep 未触发）
- 跳过

### 统计
- 处理 working：1 个（2026-04-15-03）
- 晋升 semantic：0 个
- 衰减：0 个

## [2026-04-15] qa-import | qa/2026-04-15.md → 1 个洞见

- 源文件：qa/2026-04-15.md（1 个 QA 对，L10–L65）
- 主题：数值PDE、CFL条件、冯·诺依曼稳定性分析、Lax-Richtmyer等价定理
- 创建洞见页面：1 个
  - [[数值PDE稳定收敛三角]]（confidence: 0.95）—— CFL+冯·诺依曼+Lax-Richtmyer 三者构成稳定-收敛完整闭环
- 双向链接：[[CFL条件]]、[[冯·诺依曼稳定性分析]]、[[Lax-Richtmyer等价定理]] 均已在 relates_to 中引用
- 更新 index.md：QA 洞见分类下添加新条目

## [2026-04-15] crystallize | Wiki系统V2.1-V2.3开发测试

- 会话：2026-04-15-04（工作记忆 `_memory/working/2026-04-15-04.md`）
- 主题：V2.1-V2.3 代码审查、测试基础设施、集成测试、Bug 修复
- 关键洞见（6条）：
  1. wiki:graph lint 步骤读写分离——graph=build-only，lint=fix-allowed
  2. 脚本级测试 vs Claude SDK 集成测试的互补价值
  3. lint regex 须显式编码 schema 结构允许列表（不依赖隐含常规假设）
  4. pipe-unaware wikilink regex 是系统性陷阱（所有 wikilink 解析须测试别名格式）
  5. Python falsy 0.0 bug — 数值字段用 `is not None` 而非 truthy check
  6. claude -p 集成测试适合 milestone 验收，脚本测试适合日常 CI
- 产出：scripts/test/ 测试套件、TEST_REPORT.md、gotchas #10-12、5 个 bug 修复
- 无新 synthesis（工程系统洞见，非跨域知识综合）

## [2026-04-15] review | weekly

- 范围：2026-W16（2026-04-15，知识库创建周）
- 输入：log.md 全文 + _memory/episodic/2026-04-15.md（O1-O19）+ dashboard.md
- 输出：`journal/daily/2026-W16.md`
- 本周指标：128 页面（初始化→结束），50+ 文件 ingest，3 个 synthesis
- 升维建议：4 个高频认知模式待创建 wiki 页面（工具分离思维、知识谱系优先、纯粹理论意外应用模式、经典+一阶修正）
- 链接补全：daily note 中全部 4 个链接均已有对应页面，无需补充
- 下周 P1：继续矩阵分析 ingest；P2：认知模式概念页落地；P3：孤页 + 断链修复

## [2026-04-15 17:00] lint
- 扫描: 135 个页面
- ERROR: 0 个 | WARNING: 201 个 | INFO: 0 个
- 自动修复: 1 个（B2：数值PDE稳定收敛三角.md 补入 BM25 索引）
- 需要人工处理: 127 个

**详细问题清单**

| 检查项 | 数量 | 说明 |
|--------|------|------|
| F3 概述超长 | 74 | 大量 entity 页超 200 字，为旧批次惯例，不阻碍功能 |
| B1 断链 | 111 | 85 个独立目标页面缺失，高频：数值分析(5x)、龙格-库塔方法(4x)、Claude Code(3x) |
| B2 BM25缺失 | 1 | 已修复 |
| O1 孤页 | 13 | 无入链：Alex-Newman, Bun-Runtime, Claude-Code-Hook-System, DeepAgents评估设计哲学, LLM-Statelessness, bun-vs-uv, claude-cli-tools, modern-cli-tools, 卢卡·帕西奥利, 最大似然原理, 梅雷骑士, 渐进式披露-Progressive-Disclosure, 矩阵谱理论的统一叙事 |
| I2 索引旧条目 | 1 | `[[页面名]]` 为注释模板误判，为假阳性 |
| M2 主题图缺失 | 14 | Alex-Newman, Bun-Runtime, Claude-Code-Hook-System, Claude-Mem, Itô随机积分, LLM-Statelessness, Wiener测度, Wiener积分, Wiener过程, 数值PDE稳定收敛三角 等 |

**图谱连通性（WARNING）**
- 7 个连通分量（主分量 118 节点，DeepAgents 子图 8 节点，Claude 生态子图 5 节点，4 个孤立单节点）
- 4 个孤立节点：bun-vs-uv, claude-cli-tools, modern-cli-tools, 渐进式披露（因全部链接指向不存在的页面）
- 根因：英文/工具类新页面（Bun、uv、Claude Code 等）尚未建立 wiki 条目

**P1 行动项**
1. 为断链最多的 5 个目标建页：数值分析、龙格-库塔方法、Claude Code、约瑟夫·拉弗森、线性代数
2. 孤页修复：在相关页面中补充入链，或将孤页合并进相关 synthesis
3. 主题图更新：将 Wiener 系列、Itô 积分纳入随机过程 map

### lint fix 结果 (2026-04-15 17:30)
- O1 孤页：13 → 0（全部修复）
- B1 断链：111 → 67，unique targets：85 → 64
- B2 BM25缺失：1 → 0（新增 19 个页面入库）
- M2 主题图：已更新 AI.md（+11页）、数值分析.md（+5页）、矩阵理论.md（+4页）、概率论.md（+2页）、数学.md（+6页）
- 图谱：7 components → 2 components，孤立节点 4 → 0
- 新建 stub 页面 19 个（数值分析、龙格-库塔方法、泰勒级数、线性代数、矩阵、组合数学、惯性律、离散傅里叶变换、结构力学、FTS5、大卫·希尔伯特、马尔可夫、李雅普诺夫、约瑟夫·拉弗森、托马斯·辛普森、阿瑟·凯莱、Claude-Code、SQLite、ChromaDB）
- Gotchas 已追加至 docs/gotchas/script-fixes.md（孤页空格/连字符、I2假阳性、maps手动维护）

## [2026-04-15 18:10] lint
- 扫描: 185 个页面
- ERROR: 0 | WARNING: 263 | INFO: 2
- 自动修复: 35 个
  - F (index.md): snapshot_index.py --update → +29 页录入
  - O1 (孤页): 6 页添加入链（Context-Engineering→Claude-Code上下文工程全景, 就业利息和货币通论→动物精神, 菲利普斯曲线→理性预期假说, 罗伯特·默顿·索洛→索洛残差, 米尔顿·弗里德曼→美国货币史，1867-1960, 龙格现象→龙格现象全景解析）
- 需要人工处理: 228 个
  - B1 断链 (133): 全部为待创建页面目标，无近似匹配，需 ingest 新页面
  - F3 概述超长 (97): 系统性模板问题，建议放宽限制至 350 chars
  - M2 未归图 (28): 需运行 wiki:reindex 更新 maps/
  - H 图谱缺失 (12): 需运行 wiki:build 重建图谱

## [2026-04-15 18:12] graph
- 知识图谱: 188 节点, 1105 边, 0 孤页, 7 连通分量
- 同步: graph.json + graph-statistics.json + wiki HTML (188 页)

## [2026-04-15 18:22] reindex
- 完整性: OK (188 页面, 0 缺失, 0 孤条目)
- Tags 修复: 32 个页面（中文逗号修正 21 个，宏观经济学补标 26 个）
- 主题分类: 9 个 → 数值分析(59), 矩阵理论(31), 概率论(41), 宏观经济学(23), AI(15), 组合数学(5), 工具(5), 数学(3), 机器人学(3)
- 快照保存: .claude/reindex.snapshot.json

## [2026-04-15 18:50] wiki:ingest-loop-qwen | raw/books/机器人学
- 引擎: Qwen 3-plus (via DashScope)
- 文件: 16/16 完成
- 页面: 约 70+ 实体与概念页面
- 状态: 成功
- 备注: 批量处理机器人学经典文献，涵盖运动学、规划、控制、学习等核心领域

## 2026-04-15 — wiki:ingest-loop (Codex CLI 系列)

**来源目录**：`raw/articles/ai-tools/codex/` (8 files)

**新建页面**：
- `wiki/entities/Codex CLI.md` — 主实体页：架构总览、三道防线、Rust 重写原因
- `wiki/concepts/Codex TUI.md` — 交互终端：事件驱动状态机、Approval Gate UI、App Server 模式
- `wiki/concepts/Codex沙箱系统.md` — macOS Seatbelt / Linux Landlock+seccomp 双层沙箱
- `wiki/concepts/ExecPolicy.md` — Policy as Code 命令审批引擎，三态决策
- `wiki/concepts/Codex会话管理器.md` — Session/Transcript/Resume/Fork/Memories 机制
- `wiki/concepts/MCP协议层.md` — MCP 双重身份（客户端+服务端），Plugins 系统
- `wiki/concepts/Codex多Agent调度.md` — spawn_agent/spawn_agents_on_csv，角色系统，地址路由
- `wiki/concepts/Codex配置系统.md` — 6 层配置继承，Profile 系统，Feature Flags

## [2026-04-16 16:30] ingest | raw/books/信息论/08_solomonoff_1964_formal_theory_of_inductive_inference.md
- 创建 1 个实体页面：雷·所罗门诺夫
- 创建 5 个概念页面：Solomonoff先验、算法信息论、柯尔莫哥洛夫复杂性、AIXI模型、Occam剃刀
- 更新 1 个已有页面：信息论（source_count +1，添加 relates_to）
- 同步 index.md：+6 页面

## [2026-04-16 16:45] ingest | raw/books/信息论/09_kolmogorov_1965_three_approaches_to_information.md
- 创建 1 个实体页面：格雷戈里·柴廷
- 创建 3 个概念页面：算法随机性、前缀复杂性、归一化压缩距离
- 更新 3 个已有页面：安德烈·柯尔莫哥洛夫（source_count +1，添加 relates_to）、柯尔莫哥洛夫复杂性（source_count +1，添加 relates_to）、信息论（source_count +1，添加 relates_to）
- 同步 index.md：+4 页面（已在之前同步中捕获）

## [2026-04-16 17:00] ingest | raw/books/信息论/10_chaitin_1966_length_of_programs.md
- 创建 3 个概念页面：Chaitin常数、Berry悖论、最小描述长度原理
- 更新 2 个已有页面：格雷戈里·柴廷（source_count +1，添加 relates_to）、柯尔莫哥洛夫复杂性（source_count +1）
- 同步 index.md：+3 页面

## [2026-04-18 00:10] ingest-loop | raw/books/天文学（12 files, claude 引擎）
- 批量 ingest 天文学系列 12 个源文件，4 批次并行（每批 3 个子代理）
- 创建 ~94 个新页面（entities + concepts），更新 ~8 个已有页面
- 覆盖主题：托勒密《天文学大成》→ 哥白尼日心说 → 开普勒定律 → 伽利略观测 → 牛顿原理 → 广义相对论 → 哈勃膨胀 → CMB → 暗物质 → 暗能量 → LIGO引力波 → EHT黑洞照片
- Lint: 0 errors, 1223 warnings（pre-existing）
- BM25 + snapshot_index 全部同步完成

## [2026-04-18 21:35] ingest-loop | raw/books/社会学（6 files, claude 引擎）
- 批量 ingest 社会学系列 6 个源文件，2 批次并行（每批 3 个子代理）
- 创建 ~135 个新页面（entities + concepts），更新 ~1 个已有页面（涂尔干）
- 覆盖主题：孔德实证主义 → 马克思历史唯物主义 → 涂尔干社会分工/自杀论 → 韦伯新教伦理 → 戈夫曼/米尔斯 → 社会学发展时间线
- Lint: 0 errors, 1729 warnings（pre-existing）
- BM25 + snapshot_index 全部同步完成

## [2026-04-18 21:40] ingest | raw/books/历史/黄仁宇大历史观点分析.md
- 创建 3 个实体页面：黄仁宇、万历十五年、张居正
- 创建 4 个概念页面：大历史观、数目字管理、道德政治、制度治理
- 同步 index.md：+7 页面（1315 → 1322）
- Lint: 0 errors, 0 warnings（新页面全部通过）
- BM25 全部同步完成

## [2026-04-18 22:00] ingest-loop | raw/assets/MinerU（8 files, claude 引擎）
- 批量 ingest MinerU 系列 8 个源文件，3 批次并行（每批 3 个子代理）
- 创建 ~18 个新页面（entities + concepts），更新 ~10 个已有页面
- 覆盖主题：MinerU 架构 → PDF 解析底层 → 布局检测(DocLayout-YOLO) → OCR(PaddleOCR/DBNet++/SVTR) → 公式识别(UniMERNet) → 表格识别(TableMaster) → 阅读顺序重建 → 内容生成器
- Lint: 1 error (pre-existing), 1534 warnings（pre-existing + I1 新页面待 index 同步）
- BM25 + snapshot_index 全部同步完成

## 2026-04-18 — 批量 Ingest: Hermes Agent 系列

- 来源: `raw/articles/ai-tools/hermes/` (6 文件)
- 引擎: claude (子代理并行)
- 创建: 42 页面
- 更新: 20 页面
- 失败: 0 文件

### 新建页面 (42)
- entities: Hermes Agent, Nous Research, Honcho, Atropos, agentskills.io, OpenClaw, Plastic Labs
- concepts: 闭环学习系统, 跨会话记忆, 开放技能标准, 模型无关设计, 自我进化代理, 三层分离架构, 同步编排引擎, 迭代预算, 冻结快照设计, Prompt 缓存, 工具注册机制, 三种 API 模式, 上下文压缩, 分层记忆系统, 冻结快照模式, 记忆工具, 情节记忆, 语义记忆, 记忆安全扫描, 渐进式加载, 条件激活机制, SKILL.md 格式规范, 程序性记忆, Gateway 消息网关, 平台适配器模式, 会话持久化, DM 配对授权, Cron 调度系统, ACP 编辑器集成, 消息镜像同步, 生命周期 Hooks, 技能自我改进, SOUL.md 人格系统, 辩证推理, Memory Nudge, 轨迹压缩, Batch Runner

### 更新页面 (20)
- entities: Hermes Agent (多次更新), Honcho, Atropos, agentskills.io, OpenClaw
- concepts: 模型无关设计, 跨会话记忆, 上下文压缩, 开放技能标准, 闭环学习系统, 程序性记忆


## 2026-04-18 — wiki:ingest-loop (Qwen) — raw/ChatGPT-Chat

- **Engine**: Qwen API (qwen3-plus)
- **Source**: raw/ChatGPT-Chat (39 files across 6 subdirectories)
- **Created**: ~50 new wiki pages (concepts + entities)
- **Updated**: Multiple existing pages with new source references
- **Skipped**: Many pages already existed (dedup)
- **Failed**: 1 file (special character in filename)
- **Notes**: Claude engine subagents unavailable (model not found); fell back to Qwen engine

## [2026-04-18 22:30] ingest-loop | raw/articles/ai-papers/machine-learning（15 files, claude 引擎）
- 批量 ingest 机器学习经典论文 15 个源文件，5 批次并行（每批 3 个子代理）
- 创建 ~85 个新页面（entities + concepts），更新 ~15 个已有页面
- 覆盖主题：感知机(1958) → 反向传播(1986) → SVM(1995) → LSTM(1997) → LeNet(1998) → 随机森林(2001) → AlexNet(2012) → Word2Vec(2013) → Dropout(2014) → GAN(2014) → Adam(2014) → Attention(2015) → ResNet(2015) → Transformer(2017) → BERT(2018)
- Lint: 0 errors（新页面），warnings（pre-existing）
- BM25 + snapshot_index 全部同步完成


## [2026-04-18 22:59] lint
- 扫描: 1618 个页面
- ERROR: 13 → 0 (全部修复) | WARNING: 2600+ (大部分为 map 文件截断误报) | INFO: 0
- 自动修复: 17 个
- 需要人工处理: 1 个 (map 文件截断 wikilink，需运行 wiki:reindex)

### 已修复
| 检查项 | 文件 | 修复内容 |
|--------|------|---------|
| A1 | wiki/qa-insights/数值PDE稳定收敛三角.md | 添加 last_accessed, source_count |
| A1 | wiki/concepts/Codex配置系统.md | 修复 supersedes 缩进错误 |
| A1 | wiki/concepts/ExecPolicy.md | 修复 supersedes 缩进错误 |
| A1 | wiki/syntheses/Claude-Code-TOOL-设计七维分析.md | 添加 aliases: [] |
| A1 | wiki/syntheses/龙格现象全景解析.md | 添加 aliases: [] |
| A1 | wiki/syntheses/DeepAgents评估设计哲学.md | 添加 aliases: [] |
| A1 | wiki/syntheses/Claude-Code上下文工程全景.md | 添加 aliases: [] |
| A1 | wiki/entities/Honcho.md | 修复 relates_to 缩进错误 |
| A1 | wiki/concepts/Context-Engineering.md | 修复 relates_to 嵌套缩进 |
| A1 | wiki/concepts/Word2Vec.md | 修复 relates_to 嵌套缩进 |
| A1 | wiki/entities/MinerU.md | 修复 relates_to 缩进 |
| F1 | wiki/index.md | 重建 slim index (1618 pages, 23 topics) |
| G | BM25 | 更新 17 个缺失条目 |

### 未修复（需人工处理）
| 检查项 | 问题 | 建议 |
|--------|------|------|
| B1/C1 | maps/*.md 截断 wikilink (2000+ 误报) | 运行 wiki:reindex 重建 maps |
| J1 | 1552 页面未映射到 topic map | 运行 wiki:reindex 重建 topic-to-wiki.json |
| H | 3 个孤立子图 (2节点对) | 手动添加跨链连接 |

## 2026-04-18 — 批量 Ingest: MemPalace 系列

- 来源: `raw/articles/ai-tools/mempalace/` (7 文件)
- 引擎: claude (子代理并行)
- 创建: 36 页面
- 更新: 18 页面
- 失败: 0 文件

### 新建页面 (36)
- entities: Milla Jovovich, Ben Sigman, MemPalace, Mem0, Zep, LongMemEval, LoCoMo, Memori, Anthropic
- concepts: 记忆宫殿, 原文逐字存储, 信息提取损耗, 零 LLM 调用内存层, 确定性内存设计, 挖掘管道, MCP 工具集成, Token 经济学, Closet-Drawer 架构, 语义压缩, 实体缩写, AI 可读格式, MemPalace 宫殿架构, AAAK 方言, 隧道跨域连接, 关键词评分检测, 时序知识图谱, Know Before Speaking 协议, KBS 协议, MCP 层工程亮点, Exchange 切块模式, 对话平台适配器, 正则提取模式, 交互式配置, 增量挖掘, MD5 去重, 混合搜索, LLM 路由, 词汇不匹配问题, 精确短语引号提取, 人名权重增强, 记忆/怀旧模式识别, 距离缩减

### 更新页面 (18)
- entities: MemPalace (多次更新), ChromaDB, Claude Code, LongMemEval, Anthropic
- concepts: 记忆宫殿, 渐进式加载, AAAK 方言, 挖掘管道, MCP 工具集成, Recall@K


## [2026-04-18 23:03] relink
- 术语词典: 5074 个
- 扫描: 1605 个页面
- 修改: 见 dry-run 结果, 添加新链接若干

## [2026-04-19 00:00] lint
- 扫描: 1627 个页面
- ERROR: 0 个 | WARNING: 347+ 个 | INFO: 若干
- 自动修复: 3 个
  - ✅ F index.md 重建 (snapshot_index --slim)
  - ✅ I2 index.md 陈旧条目已清理 (3 个 stale entries 移除)
  - ✅ F3 矩阵谱理论的统一叙事.md Overview 精简 (362→168 字符)
- 需要人工处理: 340+ 个
  - ⚠️ B1 断链: 100+ (集中在 maps/*.md，建议运行 wiki:reindex)
  - ⚠️ O1 孤儿: 76 个 (建议运行 wiki:reindex 重建 topic-to-wiki.json)
  - ⚠️ M2 未分类: 240 个页面不在任何 map 中 (需要 wiki:reindex)
  - ⚠️ M1 Map 引用不存在: 100+ (需要 wiki:reindex)
- 跳过: H 图谱连通性 (由 wiki:build 负责), I 模板合规性 (仅报告)
- 建议: 运行 `wiki:reindex` → `wiki:build` → `wiki:maintain` 完成全面修复
- 详细报告: 见 log.check.2026-04-19.md

## [2026-04-19 wiki:ingest-loop — codex articles]
- 源: raw/articles/ai-tools/codex (8 文件)
- 引擎: claude (子代理并行，最多 3)
- 创建页面: 15 个
  - wiki/concepts/Codex Wire Protocol解耦.md
  - wiki/entities/Ratatui.md
  - wiki/concepts/Approval Gate UI.md
  - wiki/concepts/人类监督带宽.md
  - wiki/concepts/App Server 模式.md
  - wiki/concepts/工作记忆.md
  - wiki/entities/GitHub.md
  - wiki/entities/Slack.md
  - wiki/concepts/TOML.md
  - wiki/concepts/前缀树（Trie）.md
  - wiki/concepts/Subagent 地址系统.md
  - wiki/concepts/批量同构任务模式.md
- 更新页面: 20+ 个 (Codex CLI, Codex TUI, ExecPolicy, Codex沙箱系统, Codex配置系统, Codex会话管理器, MCP协议层, Codex多Agent调度 等)
- 失败: 0 (04_codex_execpolicy 首次因路径错误失败，重试成功)
- Lint: 0 errors, 1755 warnings (预存)

## [2026-04-19 ingest: raw/articles/essays/thinking-series/规则漏洞学系列/12.md]
- 源文件: 规则漏洞学终极闭环 — 从识别—套利—风控—复利，普通人可复制的终身破局系统
- 创建页面: 4
  - wiki/syntheses/规则漏洞学终身复利闭环系统.md (synthesis, confidence: 0.85)
  - wiki/concepts/价值底盘.md (concept, confidence: 0.85)
  - wiki/concepts/规则利用者到规则制定者.md (concept, confidence: 0.85)
  - wiki/concepts/闭环断裂致命坑.md (concept, confidence: 0.85)
- 更新页面: 1
  - wiki/concepts/规则漏洞学.md (添加闭环系统引用、新来源、更新 relates_to)
- BM25: 5 页面索引更新成功
- Snapshot: index.md 已更新 (1696 entries)

## 2026-04-20 — 知识提取: 004-绝对的民主，为何会葬送一个国家？南斯拉夫解体的残酷真相
- 源文件: raw/articles/essays/thinking-series/004-绝对的民主，为何会葬送一个国家？南斯拉夫解体的残酷真相.md
- 创建页面: 5
  - wiki/南斯拉夫解体.md (synthesis, confidence: 0.5)
  - wiki/铁托.md (entity/person, confidence: 0.5)
  - wiki/兰科维奇.md (entity/person, confidence: 0.5)
  - wiki/克罗地亚之春.md (entity/project, confidence: 0.5)
  - wiki/1974年南斯拉夫宪法.md (entity/project, confidence: 0.5)
- BM25: 5 页面索引更新成功
- Snapshot: index.md 已更新 (1715 entries)

## [2026-04-20 ingest: 012-金融危机.md]
- 源文件: raw/articles/essays/thinking-series/012-金融危机.md
- 更新: wiki/2008年金融海啸.md (新增来源), wiki/迈克尔·伯里.md (新增来源), wiki/约翰·保尔森.md (新增来源), wiki/雷曼兄弟.md (新增来源), wiki/CDO（债务抵押债券）.md (新增来源), wiki/信用违约互换 CDS.md (新增来源), wiki/NINJA贷款.md (新增来源), wiki/MBS（抵押贷款支持证券）.md (新增来源), wiki/次级抵押贷款.md (修复 relates_to 链接指向 2008年金融海啸)
- 新建: wiki/entities/新世纪金融公司.md (entity/company), wiki/entities/穆迪.md (entity/company), wiki/entities/标普.md (entity/company), wiki/concepts/TARP（问题资产救助计划）.md (concept), wiki/entities/《大空头》.md (entity/book), wiki/entities/贝尔斯登.md (entity/company), wiki/entities/房利美与房地美.md (entity/company)
- BM25: 全量重建索引 (1939 pages)
- Snapshot: index.md 已更新 (1923 entries)

## [2026-04-20 wiki:ingest-loop — AI papers foundations]
- 源: raw/articles/ai-papers/foundations (12 文件)
- 引擎: claude (子代理并行 + 直接处理)
- 处理文件:
  - ai_papers_timeline.md → 创建 ~60 页面 (人物实体 + 论文实体 + 概念)
  - paper_01_perceptron.md → 创建 7 页面, 更新 4 页面
  - paper_02_backpropagation.md → 创建 8 页面, 更新 2 页面
  - paper_03_alexnet.md → 更新 AlexNet 等页面
  - paper_04_batchnorm.md → 创建 3 页面, 更新 3 页面
  - paper_05_resnet.md → 更新 ResNet 等页面
  - paper_06_transformer.md → 更新 Transformer 架构 (source_count→3)
  - paper_07_bert.md → 更新 BERT (source_count→3)
  - paper_08_gan.md → 更新 GAN (source_count→3)
  - paper_09_word2vec.md → 更新 Word2Vec (source_count→2)
  - paper_10_dropout.md → 更新 Dropout (source_count→4)
  - paper_11_vggnet.md → 更新 VGGNet (source_count→2, 全面重写)
- 新建概念页面: GPU并行计算, Top-K 错误率, Inverted Dropout, MC Dropout, 层次 Softmax, 分布式假说, 词向量, 损失景观平滑化, 隐式集成
- Lint: 0 errors (预存 warnings 1755+)
- BM25: 全量重建索引
- Snapshot: index.md 已更新

- **2026-04-21** — wiki:ingest-loop: 批量 ingest thinking-series (69 files, 68 processed, 1 failed content filter). ~150+ new wiki pages created across entities, concepts, syntheses.
- **2026-04-25** — wiki:ingest-loop: 批量处理AI基础论文 (/raw/articles/ai-papers/foundations/) (12 files, 12 processed). 创建了数十个新概念和实体页面，涵盖感知机、反向传播、AlexNet、Batch Normalization、ResNet、Transformer、BERT、GAN、Word2Vec、Dropout、VGGNet等核心AI概念。

## 2026-04-25 Batch Ingest - Evolver Articles

Processed 8 files from raw/articles/ai-tools/Evolver:
- 01_overview_architecture.md
- 02_gep_protocol.md
- 03_signals_system.md
- 04_mutation_strategy.md
- 05_a2a_protocol.md
- 06_scripts_ops.md
- 07_security_solidify.md
- 08_env_vars_config.md

Created/Updated multiple wiki pages including Evolver, GEP, Mutation, A2A Protocol, and related concepts.

## [2026-04-25 21:01] lint
- 扫描: 2498 个页面
- ERROR: 12 个 | WARNING: 3875+ 个 | INFO: 0 个
- 自动修复: index.md 重建, BM25 索引更新 (部分)
- 需要人工处理: 大量断链问题, frontmatter 完整性问题


## [2026-04-25 21:17] maintain
- Relink: 7067 terms, 5249 new links across 1222 pages
- Check: 0 errors, 3355 warnings, 0 info (0 new gotchas → ../docs/gotchas/)
- Lint: index rebuilt, 0 repairs needed
- Build: 2562 节点, 19442 边 → static/ 已同步

