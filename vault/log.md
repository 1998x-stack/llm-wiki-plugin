---
type: log
---

# 操作日志

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
