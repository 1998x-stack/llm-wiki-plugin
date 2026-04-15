# 09 · Dropout：用随机遗忘换取持久记忆
> 《Dropout: A Simple Way to Prevent Neural Networks from Overfitting》  
> **作者**：Nitish Srivastava, Geoffrey Hinton, Alex Krizhevsky, Ilya Sutskever, Ruslan Salakhutdinov　**期刊**：JMLR　**年份**：2014

---

## 一、历史背景：神经网络的过拟合危机

深度神经网络拥有数百万参数，极易"死记硬背"训练数据——这叫**过拟合（Overfitting）**：

```
训练集准确率：99%
测试集准确率：65%   ← 泛化灾难
```

传统正则化方法：
- **L2 正则化**：惩罚大权重 `L + λ‖w‖²`
- **L1 正则化**：稀疏权重 `L + λ‖w‖₁`
- **Early Stopping**：验证集误差不再下降时停止训练

这些方法对深度网络效果有限。2014 年，Hinton 团队提出了一个出人意料的简单方案：

> **训练时，随机"杀死"一些神经元。**

---

## 二、Dropout 的核心机制

**训练时**：每个神经元以概率 p（通常 0.5）被随机置零：

```
正常前向传播：
  h = ReLU(W·x + b)          ← 所有神经元激活

Dropout 训练时（p=0.5）：
  mask ~ Bernoulli(1-p)        ← 每个位置独立随机 0 或 1
  h = ReLU(W·x + b) ⊙ mask   ← 被 drop 的神经元输出=0
```

**测试时**：所有神经元开启，权重乘以保留概率 (1-p)（期望值不变）：

```
h_test = ReLU(W·x + b) × (1-p)
```

现代实现用 **Inverted Dropout**（更高效）：训练时直接除以 (1-p)，测试时无需调整：

```
训练：h = ReLU(W·x + b) ⊙ mask / (1-p)
测试：h = ReLU(W·x + b)           ← 代码中切换 model.eval() 即可
```

---

## 三、为什么有效？三种解释

### 解释一：集成学习视角

```
网络有 N 个神经元，Dropout p=0.5
→ 每次训练前向传播，随机生成一个"薄"子网络
→ 共有 2^N 种可能的子网络（N=1000时，2^1000 种！）
→ 所有子网络共享参数（但只有参与的子集被更新）
→ 测试时权重缩放 ≈ 对所有子网络取几何平均

相当于同时训练了指数级数量的子模型并做集成！
```

### 解释二：减少神经元共适应

```
没有 Dropout：
  神经元 A 依赖神经元 B 来修正自己的错误 → "共谋"
  → A 单独无法正常工作 → 泛化差

有 Dropout：
  "你不能依赖你的邻居，因为它随时可能消失"
  → 每个神经元必须学习更鲁棒、更独立的特征
  → 每个特征探测器单独也有意义
```

### 解释三：类比有性生殖（Hinton 的原创比喻）

有性生殖（基因随机混合）比无性生殖（完全复制）更能防止"寄生基因"的传播。Dropout 是神经元层面的"基因混合"——防止少数神经元的过度特化（过拟合特征）主导整个网络。

---

## 四、Dropout 的变体

| 变体 | 说明 | 适用场景 |
|------|------|---------|
| **Standard Dropout** | 随机置零神经元 | 全连接层 |
| **Spatial Dropout** | 随机置零整个特征图通道 | CNN |
| **DropConnect** | 随机置零权重（而非神经元） | 全连接层 |
| **MC Dropout** | 测试时保持 Dropout 开启 → 估计不确定性 | 贝叶斯深度学习 |
| **DropPath/StochDepth** | 随机跳过整个残差块 | ResNet, ViT |
| **Attention Dropout** | 对注意力权重做 Dropout | Transformer |

---

## 五、完整代码实现

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
from typing import List, Tuple, Optional


class ManualDropout(nn.Module):
    """
    Inverted Dropout 手动实现（教学用）
    训练时：随机置零 + 缩放（除以保留概率）
    测试时：直接输出（不做任何操作）
    """

    def __init__(self, p: float = 0.5):
        """
        Args:
            p: 神经元被丢弃的概率（drop probability），不是保留概率
        """
        super().__init__()
        assert 0.0 <= p < 1.0, f"概率 p 必须在 [0, 1)，得到 {p}"
        self.p = p

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if not self.training or self.p == 0.0:
            return x  # 测试时直接返回

        keep_prob = 1.0 - self.p
        # 生成伯努利掩码：保留概率为 keep_prob
        mask = torch.bernoulli(torch.full_like(x, keep_prob))
        # Inverted Dropout：除以 keep_prob 保证期望值不变
        return x * mask / keep_prob

    def extra_repr(self) -> str:
        return f"p={self.p}"


class MLPWithDropout(nn.Module):
    """
    带 Dropout 的多层感知机
    对比实验：有/无 Dropout 的过拟合程度
    """

    def __init__(self, input_dim: int, hidden_dims: List[int],
                 output_dim: int, dropout_p: float = 0.5,
                 use_dropout: bool = True, use_bn: bool = False):
        """
        Args:
            input_dim:   输入维度
            hidden_dims: 各隐藏层维度列表
            output_dim:  输出维度
            dropout_p:   Dropout 概率
            use_dropout: 是否使用 Dropout
            use_bn:      是否使用 Batch Normalization（与 Dropout 对比）
        """
        super().__init__()
        layers: List[nn.Module] = []
        dims = [input_dim] + hidden_dims

        for i in range(len(dims) - 1):
            layers.append(nn.Linear(dims[i], dims[i + 1]))
            if use_bn:
                layers.append(nn.BatchNorm1d(dims[i + 1]))
            layers.append(nn.ReLU(inplace=True))
            if use_dropout:
                layers.append(ManualDropout(dropout_p))

        layers.append(nn.Linear(dims[-1], output_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class MCDropoutModel(nn.Module):
    """
    蒙特卡洛 Dropout（MC Dropout）
    测试时保持 Dropout 开启，通过多次前向传播估计预测不确定性
    Gal & Ghahramani (2016) 证明这等价于贝叶斯近似推断
    """

    def __init__(self, input_dim: int, hidden_dim: int,
                 output_dim: int, p: float = 0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(p),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(p),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

    def predict_with_uncertainty(self, x: torch.Tensor,
                                  n_samples: int = 50
                                  ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        MC Dropout：通过多次前向传播估计预测均值和不确定性

        Args:
            x:         输入数据
            n_samples: 采样次数（越多越准确，越慢）

        Returns:
            mean:     预测均值（置信预测）
            variance: 预测方差（不确定性估计）
        """
        self.train()  # 保持 Dropout 开启！关键
        with torch.no_grad():
            preds = torch.stack([self.net(x) for _ in range(n_samples)])
            # preds: (n_samples, batch_size, output_dim)
        self.eval()
        return preds.mean(dim=0), preds.var(dim=0)


def compare_dropout_effect():
    """对比实验：有/无 Dropout 在小数据集上的过拟合程度"""
    torch.manual_seed(42)

    # 生成小数据集（刻意过拟合场景）
    n_train, n_test = 200, 1000
    input_dim = 100
    X_train = torch.randn(n_train, input_dim)
    y_train = (X_train[:, 0] > 0).long()
    X_test  = torch.randn(n_test,  input_dim)
    y_test  = (X_test[:, 0] > 0).long()

    train_ds = TensorDataset(X_train, y_train)
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
    criterion = nn.CrossEntropyLoss()

    results = {}
    for label, use_dropout in [("无 Dropout", False), ("有 Dropout（p=0.5）", True)]:
        model = MLPWithDropout(input_dim, [512, 512, 512], 2,
                               dropout_p=0.5, use_dropout=use_dropout)
        opt = optim.Adam(model.parameters(), lr=1e-3)

        for epoch in range(100):
            model.train()
            for X, y in train_loader:
                loss = criterion(model(X), y)
                opt.zero_grad(); loss.backward(); opt.step()

        model.eval()
        with torch.no_grad():
            tr_acc = (model(X_train).argmax(1) == y_train).float().mean().item()
            te_acc = (model(X_test).argmax(1)  == y_test ).float().mean().item()

        results[label] = (tr_acc, te_acc)
        print(f"  {label}: 训练准确率 {tr_acc:.2%}，测试准确率 {te_acc:.2%}，"
              f"泛化差距 {(tr_acc - te_acc):.2%}")

    return results


# ── 演示 ──────────────────────────────────────────────
if __name__ == "__main__":
    # 手动 Dropout 功能验证
    print("=== Inverted Dropout 验证 ===")
    dropout = ManualDropout(p=0.5)
    x = torch.ones(1000, 100)

    dropout.train()
    out_train = dropout(x)
    print(f"  训练时 - 均值（期望≈1.0）：{out_train.mean():.4f}")
    print(f"  训练时 - 零值比例（期望≈0.5）：{(out_train == 0).float().mean():.4f}")

    dropout.eval()
    out_test = dropout(x)
    print(f"  测试时 - 均值（期望=1.0）：{out_test.mean():.4f}")

    # 过拟合对比实验
    print("\n=== Dropout 防止过拟合实验 ===")
    compare_dropout_effect()

    # MC Dropout 不确定性估计
    print("\n=== MC Dropout 不确定性估计 ===")
    mc_model = MCDropoutModel(input_dim=10, hidden_dim=64, output_dim=1)
    mc_model.eval()

    x_certain   = torch.zeros(5, 10)          # 接近训练分布中心
    x_uncertain = torch.randn(5, 10) * 5.0    # 远离训练分布

    mean_c, var_c = mc_model.predict_with_uncertainty(x_certain, n_samples=100)
    mean_u, var_u = mc_model.predict_with_uncertainty(x_uncertain, n_samples=100)

    print(f"  接近分布中心 - 预测方差（不确定性）：{var_c.mean():.4f}")
    print(f"  远离分布中心 - 预测方差（不确定性）：{var_u.mean():.4f}")
    print(f"  → 分布外数据不确定性更高（符合预期）")
```

---

## 六、Dropout 在现代深度学习的地位

尽管 Batch Normalization（2015）在卷积网络中逐渐承担了部分正则化作用，Dropout 在以下场景仍不可替代：

| 场景 | Dropout 的角色 |
|------|---------------|
| **全连接层** | 标配正则化，几乎所有大网络都用 |
| **Transformer** | 注意力权重 + 前馈层均有 Dropout |
| **强化学习** | 防止价值网络过拟合少量经验 |
| **贝叶斯估计** | MC Dropout 估计预测不确定性 |
| **小数据集** | 数据稀缺时 Dropout 效果最显著 |

---

## 七、历史地位

| 维度 | 评价 |
|------|------|
| 简洁性 | ⭐⭐⭐⭐⭐ 一行代码，极度简洁 |
| 理论深度 | ⭐⭐⭐⭐ 集成学习 + 贝叶斯近似多角度解释 |
| 实用性 | ⭐⭐⭐⭐⭐ 至今仍是深度学习标配 |
| 历史影响 | ⭐⭐⭐⭐⭐ AlexNet 能赢 ILSVRC 的关键因素之一 |

---

## 一句话总结

> Dropout 用"随机遗忘"换来了"持久记忆"——让神经网络学会了在不确定性中工作，就像人类在嘈杂环境中仍能保持专注。

---

*参考：Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., & Salakhutdinov, R. (2014). Dropout: a simple way to prevent neural networks from overfitting. JMLR, 15(1), 1929–1958.*
