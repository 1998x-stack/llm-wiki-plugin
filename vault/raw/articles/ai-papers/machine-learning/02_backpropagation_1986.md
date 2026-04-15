# 02 · 反向传播（Backpropagation）
> 《Learning Representations by Back-propagating Errors》  
> **作者**：David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams　**期刊**：Nature　**年份**：1986

---

## 一、历史背景

感知机的 XOR 危机之后，神经网络研究沉寂了十余年。多层网络在理论上可以解决非线性问题，但有一个根本难题：

> **中间隐藏层的权重该怎么训练？**

输出层的误差可以直接观察，但没人知道该"怪"哪一层的哪个权重。1986 年，Rumelhart、Hinton 和 Williams 在 *Nature* 上发表了这篇仅 4 页的论文，给出了彻底的答案：**把误差从输出层沿计算图逆向传播，用微积分链式法则计算每个权重对误差的贡献，然后梯度下降更新它。**

这篇论文直接开启了现代深度学习的大门。

---

## 二、核心思想：链式法则

设一个两层网络，损失函数 L 关于第一层权重 W₁ 的梯度：

```
∂L/∂W₁  =  (∂L/∂ŷ) · (∂ŷ/∂h) · (∂h/∂W₁)
               ↑输出误差     ↑输出层向后传    ↑局部梯度
```

这正是微积分中的**链式法则（Chain Rule）**，在神经网络语境下称为**反向传播（Backpropagation）**。

---

## 三、前向传播 vs 反向传播

```
前向传播（Forward Pass）：计算预测值与损失
─────────────────────────────────────────────
输入 x
  → 隐藏层：h = σ(W₁·x + b₁)
  → 输出层：ŷ = W₂·h + b₂
  → 损失：  L = ½(ŷ - y)²    (MSE)

反向传播（Backward Pass）：沿计算图逆向求梯度
─────────────────────────────────────────────
L
  → ∂L/∂ŷ  = ŷ - y
  → ∂L/∂W₂ = (ŷ - y) · hᵀ               ← 输出层权重梯度
  → ∂L/∂h  = W₂ᵀ · (ŷ - y)
  → ∂L/∂z₁ = ∂L/∂h ⊙ σ'(z₁)             ← 激活函数导数
  → ∂L/∂W₁ = ∂L/∂z₁ · xᵀ               ← 隐藏层权重梯度

权重更新：W ← W - η · ∂L/∂W
```

**关键洞见**：每一层只需知道"从上层传来的误差信号"和"自己局部的导数"，就能计算自己的梯度——完全局部化，可以无限叠加层数。

---

## 四、激活函数的关键作用

没有非线性激活函数，多层线性变换的叠加等价于单层线性变换，无法拟合复杂函数。

论文使用 **Sigmoid**：

```
σ(x) = 1 / (1 + e⁻ˣ)

σ'(x) = σ(x) · (1 - σ(x))    ← 导数形式优雅
```

**Sigmoid 的问题**：

```
σ'(x) 最大值仅为 0.25
多层相乘后：0.25ⁿ → 0（梯度消失）
深层网络训练极慢甚至无法训练
```

→ 后来被 **ReLU** 取代（AlexNet, 2012）：`f(x) = max(0, x)`，正区间导数恒为 1，梯度不衰减。

---

## 五、为什么反向传播是高效的？

**朴素方法**（数值微分）：

```
∂L/∂wⱼ ≈ [L(w + ε·eⱼ) - L(w)] / ε

对每个参数做一次前向传播 → O(N) 次前向传播（N 为参数量）
N = 百万级参数 → 不可接受
```

**反向传播**：

```
一次前向传播（记录中间值）+ 一次反向传播（利用链式法则复用）
= O(1) 次前向传播的计算量
→ 训练速度提升 N 倍（N 为参数量）！
```

---

## 六、完整代码实现

```python
import numpy as np
from typing import List, Tuple


def sigmoid(x: np.ndarray) -> np.ndarray:
    """Sigmoid 激活函数（论文原始激活）"""
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def sigmoid_grad(x: np.ndarray) -> np.ndarray:
    """Sigmoid 导数：σ'(x) = σ(x)·(1-σ(x))"""
    s = sigmoid(x)
    return s * (1.0 - s)


def relu(x: np.ndarray) -> np.ndarray:
    """ReLU 激活函数（现代替代）"""
    return np.maximum(0.0, x)


def relu_grad(x: np.ndarray) -> np.ndarray:
    """ReLU 导数"""
    return (x > 0).astype(float)


def mse_loss(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    """均方误差损失"""
    return float(((y_pred - y_true) ** 2).mean())


class Layer:
    """全连接层（含前向/反向传播）"""

    def __init__(self, in_dim: int, out_dim: int,
                 activation: str = "sigmoid"):
        # Xavier 初始化
        scale = np.sqrt(2.0 / (in_dim + out_dim))
        self.W = np.random.randn(in_dim, out_dim) * scale
        self.b = np.zeros(out_dim)
        self.activation = activation

        # 缓存（前向传播时记录，反向传播时使用）
        self._x: np.ndarray = None
        self._z: np.ndarray = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        """前向传播：h = activate(x·W + b)"""
        self._x = x
        self._z = x @ self.W + self.b
        if self.activation == "sigmoid":
            return sigmoid(self._z)
        elif self.activation == "relu":
            return relu(self._z)
        else:  # linear
            return self._z

    def backward(self, grad_out: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        反向传播：计算梯度

        Args:
            grad_out: 来自上层的梯度 ∂L/∂h，shape (batch, out_dim)

        Returns:
            grad_x: 传给下层的梯度 ∂L/∂x，shape (batch, in_dim)
            grad_W: 权重梯度 ∂L/∂W，shape (in_dim, out_dim)
            grad_b: 偏置梯度 ∂L/∂b，shape (out_dim,)
        """
        # 激活函数的局部梯度
        if self.activation == "sigmoid":
            local_grad = sigmoid_grad(self._z)      # σ'(z)
        elif self.activation == "relu":
            local_grad = relu_grad(self._z)
        else:
            local_grad = np.ones_like(self._z)

        delta = grad_out * local_grad               # ∂L/∂z = ∂L/∂h ⊙ σ'(z)
        grad_W = self._x.T @ delta                  # ∂L/∂W = xᵀ · δ
        grad_b = delta.sum(axis=0)                  # ∂L/∂b = Σδ
        grad_x = delta @ self.W.T                   # ∂L/∂x = δ · Wᵀ（传给前层）
        return grad_x, grad_W, grad_b


class MLP:
    """
    多层感知机（Multi-Layer Perceptron）
    用反向传播算法训练（Rumelhart et al., 1986）
    """

    def __init__(self, layer_dims: List[int], activation: str = "relu",
                 learning_rate: float = 0.01):
        """
        Args:
            layer_dims: 各层维度，如 [2, 64, 64, 1] 表示输入2维，两个64维隐藏层，1维输出
            activation: 隐藏层激活函数 ("sigmoid" | "relu")
            learning_rate: 学习率 η
        """
        self.lr = learning_rate
        self.layers: List[Layer] = []
        for i in range(len(layer_dims) - 1):
            act = activation if i < len(layer_dims) - 2 else "linear"
            self.layers.append(Layer(layer_dims[i], layer_dims[i + 1], act))

    def forward(self, X: np.ndarray) -> np.ndarray:
        """前向传播，依次通过每层"""
        h = X
        for layer in self.layers:
            h = layer.forward(h)
        return h

    def backward(self, y_pred: np.ndarray, y_true: np.ndarray) -> float:
        """
        反向传播：从输出层逐层向后计算梯度并更新权重

        Returns:
            loss: 当前批次的 MSE 损失
        """
        n = y_true.shape[0]
        loss = mse_loss(y_pred, y_true)

        # 输出层的梯度：∂(MSE)/∂ŷ = 2(ŷ-y)/n
        grad = 2.0 * (y_pred - y_true) / n

        # 逐层反向传播（从最后一层到第一层）
        for layer in reversed(self.layers):
            grad, grad_W, grad_b = layer.backward(grad)
            # SGD 更新
            layer.W -= self.lr * grad_W
            layer.b -= self.lr * grad_b

        return loss

    def train(self, X: np.ndarray, y: np.ndarray,
              epochs: int = 1000, batch_size: int = 32,
              verbose: bool = True) -> List[float]:
        """
        训练循环（Mini-batch SGD）

        Returns:
            loss_history: 每轮的平均损失
        """
        n = len(X)
        loss_history = []

        for epoch in range(epochs):
            # 随机打乱数据
            idx = np.random.permutation(n)
            X_shuf, y_shuf = X[idx], y[idx]

            epoch_loss = 0.0
            n_batches = 0
            for start in range(0, n, batch_size):
                X_batch = X_shuf[start:start + batch_size]
                y_batch = y_shuf[start:start + batch_size]

                y_pred = self.forward(X_batch)
                loss = self.backward(y_pred, y_batch)
                epoch_loss += loss
                n_batches += 1

            avg_loss = epoch_loss / n_batches
            loss_history.append(avg_loss)

            if verbose and (epoch + 1) % 200 == 0:
                print(f"  Epoch {epoch + 1:4d}/{epochs} | Loss: {avg_loss:.6f}")

        return loss_history

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.forward(X)


# ── 演示：解决 XOR（感知机无法完成，MLP + BP 可以）──
if __name__ == "__main__":
    np.random.seed(42)

    print("=== XOR 问题（MLP + 反向传播）===")
    X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y_xor = np.array([[0], [1], [1], [0]], dtype=float)

    # 网络：2 → 4 → 1，隐藏层用 sigmoid（论文原始设定）
    net = MLP([2, 4, 1], activation="sigmoid", learning_rate=1.0)
    losses = net.train(X_xor, y_xor, epochs=2000, batch_size=4, verbose=False)

    preds = net.predict(X_xor)
    print(f"  输入 → 原始输出 → 四舍五入")
    for xi, pi in zip(X_xor, preds):
        print(f"  {xi} → {pi[0]:.4f} → {round(pi[0])}")
    print(f"  最终 Loss: {losses[-1]:.6f}")

    print("\n=== 回归任务：拟合 sin(x) ===")
    X_reg = np.linspace(-np.pi, np.pi, 200).reshape(-1, 1)
    y_reg = np.sin(X_reg)

    net_reg = MLP([1, 64, 64, 1], activation="relu", learning_rate=1e-3)
    losses_reg = net_reg.train(X_reg, y_reg, epochs=1000, batch_size=32, verbose=True)

    y_hat = net_reg.predict(X_reg)
    mse = mse_loss(y_hat, y_reg)
    print(f"  最终 MSE: {mse:.6f}")
```

---

## 七、反向传播的深远影响

| 影响 | 说明 |
|------|------|
| **解锁多层网络训练** | 使 MLP 成为可能 |
| **统一的学习框架** | 任何可微函数都可用梯度下降训练 |
| **自动微分（AutoDiff）** | PyTorch/TensorFlow 的核心即 BP 的工程化实现 |
| **深度学习的基石** | 无论 CNN、RNN、Transformer，训练都依赖 BP |

---

## 八、历史地位

| 维度 | 评价 |
|------|------|
| 首创性 | ⭐⭐⭐⭐⭐ 使多层神经网络训练成为可能 |
| 理论深度 | ⭐⭐⭐⭐⭐ 链式法则的神经网络完整推导 |
| 实用性 | ⭐⭐⭐⭐⭐ 至今仍是所有深度学习的训练引擎 |
| 历史影响 | ⭐⭐⭐⭐⭐ 奠定现代 AI 的计算基础 |

---

## 一句话总结

> 反向传播是深度学习的"发动机"——没有它，神经网络只能停留在一层的平面世界。

---

*参考：Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). Learning representations by back-propagating errors. Nature, 323(6088), 533–536.*
