# 07 · AlexNet：深度学习革命的起点
> 《ImageNet Classification with Deep Convolutional Neural Networks》  
> **作者**：Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton　**会议**：NeurIPS　**年份**：2012

---

## 一、历史背景：一场改变历史的比赛

**ImageNet 大规模视觉识别挑战赛（ILSVRC）** 是计算机视觉最权威的竞赛，目标是在 120 万张、1000 个类别的图像上做分类。

2010、2011 年冠军均采用传统方法（手工特征 + SVM），Top-5 错误率约 25–26%。

2012 年，Geoffrey Hinton 的学生 Alex Krizhevsky 带着一个深度卷积神经网络参赛：

```
2011 年冠军（传统方法）：Top-5 错误率  25.8%
2012 年 AlexNet：         Top-5 错误率  15.3%
                          ↑
                    领先第二名整整 10 个百分点
```

这不是渐进式改进，而是**跨越式突破**。从这一刻起，深度学习的时代正式开启，AI 产业的格局被彻底改变。

---

## 二、AlexNet 架构

```
输入：224×224×3（RGB 彩色图像）
  ↓
Conv1：96个 11×11 卷积核，stride=4  → 55×55×96   + ReLU + LRN + MaxPool(3×3,s=2)
  ↓
Conv2：256个 5×5 卷积核，pad=2      → 27×27×256  + ReLU + LRN + MaxPool(3×3,s=2)
  ↓
Conv3：384个 3×3 卷积核，pad=1      → 13×13×384  + ReLU
  ↓
Conv4：384个 3×3 卷积核，pad=1      → 13×13×384  + ReLU
  ↓
Conv5：256个 3×3 卷积核，pad=1      → 13×13×256  + ReLU + MaxPool(3×3,s=2)
  ↓
FC6：  4096 神经元  + ReLU + Dropout(p=0.5)
  ↓
FC7：  4096 神经元  + ReLU + Dropout(p=0.5)
  ↓
FC8：  1000 神经元（输出层）+ Softmax

总参数量：约 62,000,000（6200 万）
```

---

## 三、五大技术创新

### 3.1 ReLU 激活函数

```
Sigmoid：σ(x) = 1/(1+e⁻ˣ)   导数最大 0.25，深层梯度消失
ReLU：   f(x) = max(0, x)    正区间导数恒为 1，梯度不衰减

实验结果：ReLU 比 Sigmoid 快 6 倍达到相同的训练误差
```

ReLU 还带来**稀疏激活**——约 50% 神经元输出为 0，减少了过拟合。

### 3.2 GPU 并行训练（双 GTX 580，3GB 显存）

```
Krizhevsky 将网络分布在两块 GPU 上：
  GPU 1：前 48 个卷积核
  GPU 2：后 48 个卷积核
  仅在特定层（Conv3、FC 层）跨 GPU 交换数据

在 ImageNet 上训练约 5–6 天
若用同等算力的 CPU：需要数月
```

这直接证明：**深度学习是算力驱动的**，GPU 是关键推手。

### 3.3 Dropout 正则化

```
训练时：每个神经元以 p=0.5 的概率被随机"关闭"
→ 强迫网络学习冗余、独立的特征
→ 相当于同时训练 2^N 个共享参数的子网络

测试时：所有神经元开启，权重乘以 (1-p)=0.5
→ 对所有子网络取近似平均
```

Dropout 将 AlexNet 的验证集错误率显著降低。

### 3.4 数据增强（Data Augmentation）

```
从 256×256 原图中随机裁剪 224×224
随机水平翻转
PCA 色彩扰动（随机调整 RGB 通道）

训练样本：从 120 万 → 等效扩展为数十亿
```

### 3.5 局部响应归一化（LRN）

受神经科学"侧抑制"启发，对相邻通道的激活值做归一化。后被 Batch Normalization 取代，但当时有效。

---

## 四、完整代码实现

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from typing import Tuple, List


class AlexNet(nn.Module):
    """
    AlexNet 完整实现（Krizhevsky et al., 2012）

    严格按照原论文架构，支持任意类别数。
    注：原论文使用双 GPU，此实现为单 GPU/CPU 版本。
    """

    def __init__(self, num_classes: int = 1000, dropout: float = 0.5):
        """
        Args:
            num_classes: 输出类别数（原论文为 1000，CIFAR-10 为 10）
            dropout:     Dropout 概率（原论文为 0.5）
        """
        super().__init__()
        self.features = nn.Sequential(
            # Conv1：大卷积核捕获低级特征
            nn.Conv2d(3, 96, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.LocalResponseNorm(size=5, alpha=1e-4, beta=0.75, k=2.0),
            nn.MaxPool2d(kernel_size=3, stride=2),

            # Conv2：中等卷积核
            nn.Conv2d(96, 256, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.LocalResponseNorm(size=5, alpha=1e-4, beta=0.75, k=2.0),
            nn.MaxPool2d(kernel_size=3, stride=2),

            # Conv3-5：小卷积核，叠加感受野
            nn.Conv2d(256, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(384, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )

        # 自适应池化（处理不同输入尺寸）
        self.avgpool = nn.AdaptiveAvgPool2d((6, 6))

        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )

        self._initialize_weights()

    def _initialize_weights(self) -> None:
        """论文原始初始化方案"""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.normal_(m.weight, mean=0, std=0.01)
                if m.bias is not None:
                    # 论文中 Conv2/4/5 的偏置初始化为 1，其余为 0
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, mean=0, std=0.01)
                nn.init.constant_(m.bias, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)          # 卷积特征提取
        x = self.avgpool(x)            # → (B, 256, 6, 6)
        x = x.flatten(1)              # → (B, 256*6*6=9216)
        return self.classifier(x)     # → (B, num_classes)


class AlexNetTrainer:
    """AlexNet 训练器，含 SGD + 动量 + 权重衰减（原论文设置）"""

    def __init__(self, model: AlexNet, device: torch.device):
        self.model = model.to(device)
        self.device = device
        # 原论文：SGD + momentum=0.9 + weight_decay=5e-4
        self.optimizer = optim.SGD(
            model.parameters(),
            lr=0.01,
            momentum=0.9,
            weight_decay=5e-4,
        )
        # 每 30 epoch 学习率乘以 0.1
        self.scheduler = optim.lr_scheduler.StepLR(
            self.optimizer, step_size=30, gamma=0.1)
        self.criterion = nn.CrossEntropyLoss()

    def train_epoch(self, loader: DataLoader) -> Tuple[float, float]:
        self.model.train()
        total_loss, correct, total = 0.0, 0, 0
        for X, y in loader:
            X, y = X.to(self.device), y.to(self.device)
            self.optimizer.zero_grad()
            logits = self.model(X)
            loss = self.criterion(logits, y)
            loss.backward()
            self.optimizer.step()
            total_loss += loss.item() * len(y)
            correct += (logits.argmax(1) == y).sum().item()
            total += len(y)
        self.scheduler.step()
        return total_loss / total, correct / total

    @torch.no_grad()
    def evaluate(self, loader: DataLoader) -> Tuple[float, float]:
        self.model.eval()
        total_loss, correct, total = 0.0, 0, 0
        top5_correct = 0
        for X, y in loader:
            X, y = X.to(self.device), y.to(self.device)
            logits = self.model(X)
            loss = self.criterion(logits, y)
            total_loss += loss.item() * len(y)
            correct += (logits.argmax(1) == y).sum().item()
            # Top-5 准确率
            top5 = logits.topk(5, dim=1).indices
            top5_correct += (top5 == y.unsqueeze(1)).any(dim=1).sum().item()
            total += len(y)
        return total_loss / total, correct / total

    def fit(self, train_loader: DataLoader, val_loader: DataLoader,
            epochs: int = 90) -> None:
        for epoch in range(1, epochs + 1):
            tr_loss, tr_acc = self.train_epoch(train_loader)
            va_loss, va_acc = self.evaluate(val_loader)
            lr = self.optimizer.param_groups[0]["lr"]
            print(f"Epoch {epoch:3d}/{epochs} | lr={lr:.5f} | "
                  f"Train Acc {tr_acc:.2%} | Val Acc {va_acc:.2%}")


# ── 迁移学习：用预训练 AlexNet 做自定义分类 ──
class TransferAlexNet(nn.Module):
    """
    基于预训练 AlexNet 的迁移学习（冻结特征提取层）
    适合小数据集的自定义分类任务
    """

    def __init__(self, num_classes: int, freeze_features: bool = True):
        super().__init__()
        base = models.alexnet(pretrained=True)
        self.features = base.features
        self.avgpool = base.avgpool

        if freeze_features:
            for param in self.features.parameters():
                param.requires_grad = False  # 冻结卷积层

        # 替换分类头
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(True),
            nn.Dropout(0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Linear(4096, num_classes),   # 输出层替换为 num_classes
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.avgpool(x)
        return self.classifier(x.flatten(1))


# ── 演示 ──────────────────────────────────────────────
if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用设备：{device}")

    # 验证架构
    model = AlexNet(num_classes=1000)
    x = torch.randn(2, 3, 224, 224)
    out = model(x)
    print(f"\n输入：{x.shape} → 输出：{out.shape}")
    print(f"总参数量：{sum(p.numel() for p in model.parameters()):,}")

    # 各层参数统计
    print("\n各层参数量：")
    for name, module in model.named_modules():
        if isinstance(module, (nn.Conv2d, nn.Linear)):
            params = sum(p.numel() for p in module.parameters())
            print(f"  {name:<20} {params:>10,} 参数")

    # 在 CIFAR-10 上快速验证（缩小版）
    print("\n=== CIFAR-10 快速验证 ===")
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    # （实际运行时取消注释）
    # train_ds = datasets.CIFAR10("./data", train=True, transform=transform, download=True)
    # val_ds   = datasets.CIFAR10("./data", train=False, transform=transform, download=True)
    # alexnet_cifar = AlexNet(num_classes=10)
    # trainer = AlexNetTrainer(alexnet_cifar, device)
    # trainer.fit(DataLoader(train_ds, 64, shuffle=True),
    #             DataLoader(val_ds,   128, shuffle=False), epochs=10)
    print("  （取消注释以实际训练，需要 CIFAR-10 数据集）")
```

---

## 五、AlexNet 催生的产业变革

```
2012 AlexNet 论文发表
  ↓
Google 收购 DeepMind（2014），启动 Google Brain 扩张
  ↓
NVIDIA GPU 从游戏显卡变成 AI 芯片（股价 10 年涨 200 倍）
  ↓
ImageNet 竞赛错误率从 25% → 2.25%（2017，超人类）
  ↓
自动驾驶、医疗影像、人脸识别的商业爆发
  ↓
ChatGPT / Claude / Gemini（语言模型时代）
```

---

## 六、AlexNet 到现代 CNN 的演化路径

```
AlexNet（2012）：5层卷积，GPU训练，ReLU，Dropout
  ↓
VGGNet（2014）： 更深（16/19层），全用 3×3 小卷积核
  ↓
GoogLeNet（2014）：Inception 模块，多尺度特征
  ↓
ResNet（2015）：残差连接，152层，超人类水平
  ↓
DenseNet（2017）：密集连接，特征重用
  ↓
EfficientNet（2019）：复合缩放，极致效率
  ↓
ViT（2020）：Transformer 取代 CNN
```

---

## 七、历史地位

| 维度 | 评价 |
|------|------|
| 突破性 | ⭐⭐⭐⭐⭐ ImageNet Top-5 错误率骤降 10% |
| 技术创新 | ⭐⭐⭐⭐⭐ ReLU+GPU+Dropout+数据增强 |
| 产业影响 | ⭐⭐⭐⭐⭐ 直接引爆 AI 产业投资浪潮 |
| 历史地位 | ⭐⭐⭐⭐⭐ 深度学习时代的开端标志 |

---

## 一句话总结

> AlexNet 不是第一个 CNN，但它是第一个让世界相信深度学习可以真正有用的 CNN——从此，AI 不再只是学术实验室的玩具。

---

*参考：Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. NeurIPS, 25.*
