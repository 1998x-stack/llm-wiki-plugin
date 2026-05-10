---
type: concept
status: active
confidence: 0.95
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["人工智能", "机器学习", "神经网络"]
aliases: ["Deep Learning", "DL", "深度表示学习"]
relates_to:
  - target: "[[反向传播]]"
    type: depends_on
  - target: "[[多层感知机]]"
    type: extends
  - target: "[[卷积神经网络（CNN）]]"
    type: includes
supersedes: null
---

# 深度学习（Deep Learning）

## 概述
深度学习是机器学习的子领域，使用多层神经网络自动学习数据的分层表示，从原始输入中逐层提取越来越抽象的特征，无需手工设计特征。

## 关键内容
1. **核心思想**：传统机器学习依赖人工设计特征（如 SIFT、HOG），深度学习让网络自动学习特征。每一层学习一种表示：浅层学习边缘、纹理等低级特征，中层学习形状、部件等中级特征，深层学习语义概念等高级特征。这种分层表示学习是深度学习名称的由来。
2. **[[反向传播]]的奠基作用**：没有[[反向传播]]就没有深度学习。1986 年 Rumelhart、[[Geoffrey E. Hinton]] 和 Williams 的 [[Nature]] 论文证明了多层网络能学到有意义的内部表示——网络自动在隐藏层形成了"国籍"、"辈分"等抽象概念。这是深度学习从理论走向实践的关键一步。
3. **历史发展脉络**：
   - **1986-2012**：[[反向传播]]使[[多层感知机]]和[[循环神经网络（RNN）]]的训练成为可能，在语音识别、手写识别领域取得突破。[[LeNet-5]]（1998）展示了 CNN + [[反向传播]]在手写数字识别上的成功。
   - **2012 至今**：[[AlexNet]]（2012）用深层 CNN + GPU 引发图像识别革命。[[Transformer 架构]]（2017）结合[[注意力机制（Attention Mechanism）|注意力机制]]和[[反向传播]]重塑 NLP。[[BERT]]、GPT 等大[[Language-Model|语言模型]]将[[反向传播]]扩展到千亿参数规模。
4. **关键使能技术**：[[ReLU激活函数]]解决[[梯度消失]]、[[Dropout（随机失活）]]缓解[[过拟合（Overfitting）]]、[[Batch Normalization]]加速训练、[[Adam（自适应矩估计）]]等优化器提升收敛速度、GPU/TPU 提供算力支撑。
5. **与诺贝尔奖**：2024 年，[[Geoffrey E. Hinton]] 与 [[John Hopfield]] 因"利用人工神经网络实现机器学习的基础性发现"共同获得诺贝尔物理学奖，标志着深度学习获得了最高学术认可。

## 来源
- [[paper_02_backpropagation]] — 反向传播的历史影响章节

## 相关
- [[反向传播]] — depends_on
- [[多层感知机]] — extends
- [[卷积神经网络（CNN）]] — includes
- [[循环神经网络（RNN）]] — includes
- [[Transformer 架构]] — includes
- [[AlexNet]] — milestone
- [[LeNet-5]] — milestone
- [[BERT]] — milestone
- [[ReLU激活函数]] — enables
- [[梯度消失]] — challenges
- [[过拟合（Overfitting）]] — challenges
