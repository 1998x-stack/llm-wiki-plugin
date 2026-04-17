---
type: entity
entity_type: paper
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [推荐系统, CTR预估, 深度学习, 联合训练]
aliases: [Wide & Deep Learning, Wide and Deep, Wide & Deep Learning for Recommender Systems]
relates_to:
  - {target: Factorization Machines, type: extends}
  - {target: 特征交叉, type: uses}
  - {target: CTR 预估, type: implements}
  - {target: DeepFM, type: compares_to}
  - {target: 记忆与泛化, type: implements}
  - {target: 联合训练, type: uses}
  - {target: 交叉积变换, type: uses}
  - {target: 嵌入表示, type: uses}
supersedes: null
---

# Wide & Deep

## 概述
[[Google]] 于 2016 年在 [[DLRS 2016]] 提出的推荐模型，通过[[联合训练]]线性模型（Wide）和深度神经网络（Deep），在统一框架内同时实现[[记忆与泛化]]能力，在 [[Google]] Play 应用推荐中提升下载率 3.9%。

## 关键内容

1. **Wide 部分（记忆）**：广义线性模型 $y = \mathbf{w}^T \mathbf{x} + b$，核心创新为[[交叉积变换]]（[[交叉积变换|Cross-product Transformation]]），通过 AND 逻辑构造用户已安装应用与候选应用的交叉特征（如 `AND(user_installed_app=Netflix, impression_app=Hulu)`），精确记忆历史共现模式。
2. **Deep 部分（泛化）**：前馈神经网络，将高维稀疏分类特征映射为 32 维[[嵌入表示]]向量，拼接后经 3 层全连接层（ReLU 激活）学习高阶[[特征交叉|特征交互]]，通过嵌入空间传递性泛化到未见过的特征组合。
3. **[[联合训练]]机制**：数学表达为 $P(Y=1|\mathbf{x}) = \sigma(\mathbf{w}_{wide}^T [\mathbf{x}, \phi(\mathbf{x})] + \mathbf{w}_{deep}^T a^{(l_f)} + b)$，Wide 用 FTRL+L1 优化器（稀疏解），Deep 用 AdaGrad（自适应学习率），梯度从输出层同时反向传播到两组件。
4. **[[联合训练]] vs [[模型融合|集成学习]]**：[[模型融合|集成学习]]中各子模型独立训练、推理时组合预测；[[联合训练]]中两组件共享损失函数、同时优化，Wide 只需少量交叉特征补足 Deep 的记忆短板，实现模型紧凑和端到端优化。
5. **工业级工程实践**：训练数据超 5000 亿条样本，服务 10 亿+活跃用户和 100 万+应用；热启动机制用上一版模型权重初始化新模型，缩短更新延迟；推理时先检索筛选数百候选，Wide & Deep 在 10ms 内完成打分排序。
6. **实验效果**：离线 AUC 比 Wide 高 0.002、比 Deep 高 0.006；在线 A/B 测试下载率提升 3.9%（Deep 为 2.9%），在线提升远大于离线，因系统能通过[[记忆与泛化]]融合生成探索性推荐。
7. **局限性**：Wide 部分仍需手工特征工程（不可扩展、依赖领域知识）；Wide 与 Deep 仅在输出层耦合、特征表示层面交互有限；标准 DNN 对乘性[[特征交叉]]的学习效率存疑。
8. **历史影响**：开创"双路并行"模型架构[[规范化理论|范式]]，直接影响 [[DeepFM]]（2017，用 FM 替换 LR 消除手工特征）、DCN（2017，用 Cross Network 自动学习显式交叉）、x[[DeepFM]]（2018）、[[AutoInt]]（2019）、DCN-V2（2021）等后续工作；实现集成到 [[TensorFlow]] 的 `tf.estimator.DNNLinearCombinedClassifier`。
9. **与 FM 的关系**：从 FM 视角，Wide 部分对应 FM 的一阶线性项，Deep 部分对应 FM 二阶交互向高阶的自然推广。[[Factorization Machines]] 用低秩分解自动学习二阶交叉，Wide & Deep 通过 Wide 手工交叉 + Deep 隐式学习实现类似目标。

## 来源
- Heng-Tze Cheng et al. — Wide & Deep Learning for Recommender Systems, DLRS 2016 (arXiv:1606.07792)
- [Factorization Machines (Rendle 2010)](https://arxiv.org/abs/1209.3994)
- [DeepFM (Guo et al. 2017)](https://arxiv.org/abs/1703.04247)

## 相关
- [[Factorization Machines]] — Wide 部分对应 FM 线性项
- [[特征交叉]] — Wide 部分建模方式
- [[CTR 预估]] — 主要应用场景
- [[DeepFM]] — 用 FM 替代手工交叉的后续工作
- [[记忆与泛化]] — 核心概念框架
- [[联合训练]] — 关键技术机制
- [[交叉积变换]] — Wide 组件核心操作
- [[嵌入表示]] — Deep 组件基础
