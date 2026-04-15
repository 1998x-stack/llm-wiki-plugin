# 01 · 感知机（Perceptron）
> 《The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain》  
> **作者**：Frank Rosenblatt　**期刊**：Psychological Review　**年份**：1958

---

## 一、历史背景

1950 年代，人工智能刚刚诞生。康奈尔大学心理学家 Frank Rosenblatt 受麦卡洛克-匹兹神经元模型（1943）启发，提出了一个根本性问题：

> **"大脑是如何从经验中存储和提取信息的？"**

1957 年，他在 Cornell 航空实验室搭建了世界第一台可学习机器——**Mark I Perceptron**：一台拥有 400 个光敏传感器、可识别 20×20 像素图像的物理装置，权重由数百个可手动调节的电位器实现。

---

## 二、核心结构

感知机对单个神经元做了最简洁的数学抽象：

```
        x₁ ──w₁──┐
        x₂ ──w₂──┤
        x₃ ──w₃──┼──→  Σ(wᵢxᵢ) + b  ──→  sign(·)  ──→  ŷ ∈ {-1, +1}
        ...       │
        xₙ ──wₙ──┘
```

**数学表达**：

```
ŷ = sign(w · x + b)
```

| 符号 | 含义 |
|------|------|
| **x** | 输入特征向量（如像素灰度值） |
| **w** | 权重向量（可学习参数） |
| **b** | 偏置项（bias） |
| **sign** | 符号函数：正数→+1，负数→-1 |

**几何直觉**：感知机在特征空间中寻找一个**超平面**（2D 中是直线）将两类样本分开：

```
    +  +  +   │   -  -
    +  +  +   │   -  -   ← 决策边界：w·x + b = 0
    +  +  +   │   -  -
```

---

## 三、感知机学习规则

这是感知机最革命性的部分——**权重通过错误自动修正**：

```
初始化：w = 0，b = 0

重复直到收敛：
  for 每个训练样本 (xᵢ, yᵢ)：
    ŷ = sign(w · xᵢ + b)
    if ŷ ≠ yᵢ：           ← 预测错误
      w ← w + η · yᵢ · xᵢ   ← 权重更新
      b ← b + η · yᵢ         ← 偏置更新
```

η 是**学习率**，控制每次更新的步长。

| 情况 | 真实标签 | 预测 | 更新方向 |
|------|---------|------|---------|
| 误判为负 | +1 | -1 | 把 w 向 x 方向推 |
| 误判为正 | -1 | +1 | 把 w 远离 x 方向推 |
| 预测正确 | 任意 | 正确 | **不更新** |

**直觉类比**：就像考试做错题老师纠正你——错了就改，对了维持不动。

---

## 四、收敛定理

Rosenblatt 严格证明了：

> **若训练数据线性可分，感知机学习算法在有限步内必然收敛。**

**收敛步数上界**：若样本最大范数为 R，最近点到决策边界距离为 γ，则更新次数不超过：

```
T ≤ (R / γ)²
```

数据越"容易分"（γ 越大），收敛越快。

---

## 五、致命局限：XOR 问题

1969 年，Minsky 和 Papert 出版《感知机》（Perceptrons），证明了：

> **单层感知机无法解决线性不可分问题，如 XOR（异或）。**

| x₁ | x₂ | XOR |
|----|----|-----|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

```
     ×   ●

     ●   ×       ← × 和 ● 无法用一条直线分开
```

这直接导致神经网络研究进入长达十余年的"AI 寒冬"。

---

## 六、从感知机到现代神经网络的演化

```
感知机（1958）
  │  加隐藏层 + 非线性激活
  ↓
多层感知机 MLP（1980s）
  │  + 反向传播 + 更深的层
  ↓
深度神经网络（2000s+）
  │  + 卷积 / 注意力 / 残差连接
  ↓
现代大模型（GPT、Claude、BERT...）
```

现代神经网络每个神经元本质上都是感知机：

```python
# PyTorch 中一个线性层
output = torch.relu(weight @ input + bias)
#                   ↑ 感知机的加权求和   ↑ 非线性激活（比 sign 更平滑）
```

---

## 七、完整代码实现

```python
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional


class Perceptron:
    """
    经典感知机实现（Rosenblatt, 1958）

    采用感知机学习规则（Perceptron Learning Rule）：
      w ← w + η · y · x  （预测错误时更新）

    仅适用于线性可分数据，线性可分时保证有限步收敛。
    """

    def __init__(self, learning_rate: float = 0.1, max_iter: int = 1000):
        """
        Args:
            learning_rate: 学习率 η，控制每次权重更新步长
            max_iter: 最大迭代轮数，防止不可分数据无限循环
        """
        self.lr = learning_rate
        self.max_iter = max_iter
        self.w: Optional[np.ndarray] = None
        self.b: float = 0.0
        self.errors_per_epoch: list = []

    def fit(self, X: np.ndarray, y: np.ndarray) -> "Perceptron":
        """
        训练感知机。

        Args:
            X: 训练数据，shape (n_samples, n_features)
            y: 标签，值为 +1 或 -1，shape (n_samples,)

        Returns:
            self
        """
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)
        self.b = 0.0
        self.errors_per_epoch = []

        for epoch in range(self.max_iter):
            errors = 0
            for xi, yi in zip(X, y):
                y_pred = self._predict_single(xi)
                if y_pred != yi:
                    # 感知机学习规则：错了就更新
                    self.w += self.lr * yi * xi
                    self.b += self.lr * yi
                    errors += 1
            self.errors_per_epoch.append(errors)
            if errors == 0:
                print(f"  收敛于第 {epoch + 1} 轮，共更新 {sum(self.errors_per_epoch)} 次")
                break
        else:
            print(f"  警告：达到最大迭代次数 {self.max_iter}，可能数据不可分")

        return self

    def _predict_single(self, x: np.ndarray) -> int:
        """对单个样本预测"""
        return 1 if np.dot(self.w, x) + self.b >= 0 else -1

    def predict(self, X: np.ndarray) -> np.ndarray:
        """批量预测"""
        return np.array([self._predict_single(x) for x in X])

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """计算准确率"""
        return (self.predict(X) == y).mean()


# ── 演示：线性可分数据 ──
def demo_linearly_separable():
    np.random.seed(42)
    X_pos = np.random.randn(50, 2) + [2, 2]    # 正类：均值 (2,2)
    X_neg = np.random.randn(50, 2) + [-2, -2]   # 负类：均值 (-2,-2)
    X = np.vstack([X_pos, X_neg])
    y = np.array([1] * 50 + [-1] * 50)

    model = Perceptron(learning_rate=0.1, max_iter=100)
    model.fit(X, y)
    print(f"  测试准确率：{model.score(X, y):.2%}")
    print(f"  学到的权重：w={model.w.round(3)}，b={model.b:.3f}")


# ── 演示：XOR（线性不可分，感知机失败）──
def demo_xor():
    X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y_xor = np.array([-1, 1, 1, -1])

    model = Perceptron(learning_rate=0.1, max_iter=50)
    model.fit(X_xor, y_xor)
    print(f"  XOR 准确率：{model.score(X_xor, y_xor):.2%}（无法收敛，预期 < 100%）")


if __name__ == "__main__":
    print("=== 线性可分数据 ===")
    demo_linearly_separable()

    print("\n=== XOR 不可分数据 ===")
    demo_xor()
```

---

## 八、历史地位

| 维度 | 评价 |
|------|------|
| 首创性 | ⭐⭐⭐⭐⭐ 第一个可学习的人工神经网络 |
| 理论贡献 | ⭐⭐⭐⭐⭐ 收敛定理 + 权重更新规则 |
| 实用性 | ⭐⭐⭐ 仅限线性可分问题 |
| 历史影响 | ⭐⭐⭐⭐⭐ 现代深度学习的直接起源 |

Frank Rosenblatt 于 1971 年在 43 岁时因船难不幸离世，未能亲眼看到深度学习的复兴。但他播下的种子，在半个世纪后改变了整个人类文明的走向。

---

## 一句话总结

> 感知机的伟大不在于它能做什么，而在于它证明了**机器可以从错误中学习**——这是人工智能最根本的信念。

---

*参考：Rosenblatt, F. (1958). The perceptron: a probabilistic model for information storage and organization in the brain. Psychological review, 65(6), 386.*
