---
type: entity
entity_type: paper
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 3
tags: [推荐系统, CTR预估, 深度学习, 联合训练]
aliases: [Wide & Deep Learning, Wide and Deep, Wide & Deep Learning for Recommender Systems, Wide & Deep Learning for Recommender Systems 深度解读]
relates_to:
  - {target: Factorization Machines, type: extends}
  - {target: 特征交叉, type: uses}
  - {target: CTR 预估, type: implements}
  - {target: DeepFM, type: compares_to}
  - {target: 记忆与泛化, type: implements}
  - {target: 联合训练, type: uses}
  - {target: 交叉积变换, type: uses}
  - {target: 嵌入表示, type: uses}
  - {target: Heng-Tze Cheng, type: authored_by}
  - {target: Google, type: published_by}
  - {target: DLRS 2016, type: presented_at}
  - {target: RecSys 2016, type: presented_at}
  - {target: DCN, type: compares_to}
  - {target: xDeepFM, type: compares_to}
  - {target: AutoInt, type: compares_to}
  - {target: 推荐系统 Scaling Laws, type: influenced_by}
supersedes: null
---

# Wide & Deep

## 概述
[[Google]] 于 2016 年在 [[DLRS 2016]] 提出的推荐模型，通过[[联合训练]]线性模型（Wide）和深度神经网络（Deep），在统一框架内同时实现[[记忆与泛化]]能力，在 [[Google]] Play 应用推荐中提升下载率 3.9%。

## 关键内容

1. **Wide 部分（记忆）**：广义线性模型 $y = \mathbf{w}^T \mathbf{x} + b$，核心创新为[[交叉积变换]]（[[交叉积变换|Cross-product Transformation]]），通过 AND 逻辑构造用户已安装应用与候选应用的交叉特征（如 `AND(user_installed_app=Netflix, impression_app=Hulu)`），精确记忆历史共现模式。
2. **Deep 部分（泛化）**：[[多层感知机（MLP）|前馈神经网络]]，将高维稀疏分类特征映射为 32 维[[嵌入表示]]向量，拼接后经 3 层全连接层（ReLU 激活）学习高阶[[特征交叉|特征交互]]，通过嵌入空间传递性泛化到未见过的特征组合。
3. **[[联合训练]]机制**：数学表达为 $P(Y=1|\mathbf{x}) = \sigma(\mathbf{w}_{wide}^T [\mathbf{x}, \phi(\mathbf{x})] + \mathbf{w}_{deep}^T a^{(l_f)} + b)$，Wide 用 FTRL+L1 优化器（稀疏解），Deep 用 AdaGrad（自适应学习率），梯度从输出层同时[[反向传播]]到两组件。
4. **[[联合训练]] vs [[模型融合|集成学习]]**：[[模型融合|集成学习]]中各子模型独立训练、推理时组合预测；[[联合训练]]中两组件共享损失函数、同时优化，Wide 只需少量交叉特征补足 Deep 的记忆短板，实现模型紧凑和端到端优化。
5. **工业级工程实践**：训练数据超 5000 亿条样本，[[服务]] 10 亿+活跃用户和 100 万+应用；热启动机制用上一版模型权重初始化新模型，缩短更新延迟；推理时先检索筛选数百候选，Wide & Deep 在 10ms 内完成打分排序。
6. **实验效果**：离线 AUC 比 Wide 高 0.002、比 Deep 高 0.006；在线 A/B 测试下载率提升 3.9%（Deep 为 2.9%），在线提升远大于离线，因系统能通过[[记忆与泛化]]融合生成探索性推荐。
7. **局限性**：Wide 部分仍需[[手工特征工程]]（不可扩展、依赖领域知识）；Wide 与 Deep 仅在输出层耦合、特征表示层面交互有限；标准 DNN 对乘性[[特征交叉]]的学习效率存疑。
8. **历史影响**：开创"双路并行"模型架构[[规范化理论|范式]]，直接影响 [[DeepFM]]（2017，用 FM 替换 LR 消除[[特征工程（Feature Engineering）|手工特征]]）、DCN（2017，用 Cross Network 自动学习显式交叉）、x[[DeepFM]]（2018）、[[AutoInt]]（2019）、DCN-V2（2021）等后续工作；实现集成到 [[TensorFlow]] 的 `tf.estimator.DNNLinearCombinedClassifier`。
9. **与 FM 的关系**：从 FM 视角，Wide 部分对应 FM 的一阶线性项，Deep 部分对应 FM 二阶交互向高阶的自然推广。[[Factorization Machines]] 用低秩分解自动学习二阶交叉，Wide & Deep 通过 Wide 手工交叉 + Deep 隐式学习实现类似目标。
10. **作者信息**：论文共有 16 位作者，全部来自 [[Google]]，其中包括 [[Google Brain]] 团队的 Greg Corrado，第一作者为 [[Heng-Tze Cheng]]。
11. **推荐系统两难困境**：论文针对当时推荐系统的经典"两难困境"——线性模型善于记忆但拙于泛化，深度神经网络善于泛化但可能过度泛化——提出了解决方案。
12. **[[记忆与泛化]]定义**：论文严格定义了记忆（学习训练数据中频繁共现的特征或物品之间的相关性）和泛化（基于特征之间的传递性和相关性，探索训练数据中很少出现或从未出现的新特征组合）的概念。
13. **交叉特征的泛化盲区**：论文承认[[交叉积变换]]的根本局限性——对于训练数据中从未出现过的特征组合，交叉特征的值恒为 0，完全无法提供信息。
14. **现代视角**：在 LLM 时代，Wide & Deep 的思想仍然具有启发意义，[[RAG 系统]]中的"检索"组件类似于 Wide（记忆精确信息），"生成"组件类似于 Deep（灵活泛化），体现了相同的思想框架。

## 来源
- Heng-Tze Cheng et al. — Wide & Deep Learning for Recommender Systems, DLRS 2016 (arXiv:1606.07792)
- [Factorization Machines (Rendle 2010)](https://arxiv.org/abs/1209.3994)
- [DeepFM (Guo et al. 2017)](https://arxiv.org/abs/1703.04247)
- [[推荐系统/08-wide-and-deep]]

## 相关
- [[Factorization Machines]] — Wide 部分对应 FM 线性项
- [[特征交叉]] — Wide 部分建模方式
- [[CTR 预估]] — 主要应用场景
- [[DeepFM]] — 用 FM 替代手工交叉的后续工作
- [[记忆与泛化]] — 核心概念框架
- [[联合训练]] — 关键技术机制
- [[交叉积变换]] — Wide 组件核心操作
- [[嵌入表示]] — Deep 组件基础
- [[Heng-Tze Cheng]] — 第一作者
- [[Google]] — 发布机构
- [[DLRS 2016]] — 发表会议
- [[RecSys 2016]] — 同期会议
- [[DCN]] — 后续改进工作
- [[xDeepFM]] — 后续改进工作
- [[AutoInt]] — 后续改进工作
