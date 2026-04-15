# 论文精读 #05：残差网络 ResNet
## Deep Residual Learning for Image Recognition
**作者：Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun | 发表年份：2015 | 机构：Microsoft Research Asia**

---

## 🎯 一句话概括

> ResNet 用一个极其简单却深刻的"跳跃连接（Skip Connection）"思想，解决了深层神经网络的退化问题，让152层的超深网络成为可能，并以 **3.57% Top-5 错误率**夺得 ImageNet 2015 冠军——同年获得 CVPR 最佳论文，并成为 AI 历史上引用次数最多的论文之一。

---

## 🌍 时代背景：越深越差的怪现象

### 直觉与现实的矛盾

2014年，VGGNet 证明了"越深越好"：16层 VGG 比 8层 AlexNet 好得多。那是不是越深越好，一直堆到1000层呢？

研究者们发现了一个令人困惑的现象——**网络退化（Degradation）**：

```
Top-1 错误率（CIFAR-10 数据集）：

网络深度 | 错误率
---------|--------
  20 层  |  8.82%
  56 层  |  7.20%
 110 层  |  ← 应该更好吧？
  
实际结果：
  56层比20层好 ✅
  但 56层 比 110层 好！ ❌ （直觉上不应该）
```

这不是过拟合问题（过拟合的话训练错误率会很低，测试错误率高）。实测发现 **56层的训练错误率也比20层高！**

这说明深层网络本身更难优化，而不是泛化能力弱。

### 为什么深层网络更难优化？

理论上，56层网络可以通过让后36层变成恒等映射（identity）来达到至少和20层一样好的效果。但实验证明，**优化器找不到这个解**——深层网络的损失曲面太复杂。

---

## 💡 核心思想：残差学习

### 关键洞察

何恺明等人提出了一个绝妙的问题：

> 既然网络很难学习**恒等映射**（identity），何不直接**把输入加到输出上**，让网络只需要学习**残差**？

**传统块**学习的目标函数：$\mathcal{H}(x)$

**残差块**学习的目标函数：$\mathcal{F}(x) = \mathcal{H}(x) - x$，即 $\mathcal{H}(x) = \mathcal{F}(x) + x$

```
传统连接：                    残差连接（Skip Connection）：

输入 x                         输入 x
  │                              ├──────────────╮
  ▼                              ▼              │
Weight Layer                  Weight Layer      │（跳跃连接）
  │                              │              │
  ▼                              ▼              │
ReLU                           ReLU            │
  │                              │              │
  ▼                              ▼              │
Weight Layer                  Weight Layer      │
  │                              │              │
  ▼                              ╰──── + ◄──────╯
输出 H(x)                         │
                               ReLU
                                  │
                              输出 H(x) = F(x) + x
```

### 为什么残差更容易学习？

**情景1：这层啥都不需要做**
- 传统网络：需要学 $\mathcal{H}(x) = x$（恒等映射，不trivial）
- 残差网络：只需让 $\mathcal{F}(x) = 0$（把权重推向零，容易！）

**情景2：这层需要做一点小修改**
- 传统网络：需要精确学出目标分布
- 残差网络：只需学**与输入的差**（残差往往比较小，更好学）

**直觉类比**：
> 与其从零开始画一幅画（学完整映射），不如在草稿上改改（学残差）——后者容易得多。

---

## 🏗️ ResNet 架构详解

### 基本残差块（Basic Block）

用于 ResNet-18 和 ResNet-34：

```python
def basic_block(x):
    residual = x          # 保存输入
    
    out = Conv(x, 64, 3×3)
    out = BatchNorm(out)
    out = ReLU(out)
    
    out = Conv(out, 64, 3×3)
    out = BatchNorm(out)
    
    out = out + residual  # 关键：加回输入
    out = ReLU(out)
    return out
```

### 瓶颈块（Bottleneck Block）

用于更深的 ResNet-50/101/152，用 1×1 卷积降维/升维：

```
输入 (256 channels)
  ├────────────────────────────╮
  ▼                            │
1×1 Conv → 64 ch （降维）       │
  ↓                            │
3×3 Conv → 64 ch （主要学习）   │
  ↓                            │  Skip Connection
1×1 Conv → 256 ch（升维）       │
  ↓                            │
BatchNorm                      │
  ↓                            │
  + ◄──────────────────────────╯
  ↓
ReLU
  ↓
输出 (256 channels)
```

**参数量对比（相同通道数）：**
- Basic Block：$2 \times 3 \times 3 = 18$ 单位参数
- Bottleneck：$1 + 9 + 1 = 11$ 单位参数（节省40%）

### 各版本 ResNet 架构

| 版本 | 层数 | 参数量 | ILSVRC Top-5 | 特点 |
|------|------|-------|-------------|------|
| ResNet-18 | 18层 | 11.7M | ~10% | 最轻量 |
| ResNet-34 | 34层 | 21.8M | 7.73% | Basic Block |
| **ResNet-50** | **50层** | **25.6M** | **6.71%** | **最常用** |
| ResNet-101 | 101层 | 44.5M | 6.05% | 高精度 |
| ResNet-152 | 152层 | 60.2M | **4.49%** | 最深版本 |

---

## 📊 历史性的竞赛成绩

### ILSVRC 2015

| 排名 | 方法 | Top-5 错误率 |
|------|------|------------|
| 🥇 第一 | **ResNet（集成）** | **3.57%** |
| 🥈 第二 | Inception-v3 集成 | 4.94% |
| 人类表现 | - | ~5.1% |

**3.57% 低于人类水平（5.1%）！** 这是计算机视觉史上的里程碑——机器在ImageNet上首次超越人类。

### 同时获奖

- ✅ **ILSVRC 2015 图像分类第一**
- ✅ **ILSVRC 2015 目标检测第一**
- ✅ **ILSVRC 2015 图像定位第一**
- ✅ **COCO 2015 检测第一**
- ✅ **CVPR 2016 最佳论文**

史无前例的五冠王！

---

## 🔬 关键实验：证明残差连接的作用

### 实验1：有无残差连接的对比

在 CIFAR-10 上：

```
错误率（测试集）：

           | 有残差 | 无残差（Plain Network）
-----------|--------|----------------------
  20层      |  8.75% |  8.82%  （接近）
  32层      |  7.51% |  7.51%  （接近）
  44层      |  7.17% |  7.43%  ← 残差开始胜出
  56层      |  6.97% |  7.20%  ← 差距拉大
 110层      |  6.43% |  ≈6.97% ← 残差继续变好！Plain退化
1202层      |  7.93% |     崩溃
```

**关键发现**：
- Plain Network（无残差）在 56 层以上开始退化
- ResNet（有残差）即使到1202层依然能训练

### 实验2：残差学习的可视化

研究者分析了训练后残差函数 $\mathcal{F}(x)$ 的响应大小：

> 残差函数的响应普遍比非残差函数小，说明残差连接确实让网络"接近恒等映射"，权重矩阵大多学到的是小的扰动。

---

## 🌊 ResNet 的"降采样"处理

当输入输出维度不匹配时（如通道数翻倍、特征图尺寸减半），需要处理跳跃连接：

**选项A：补零（Zero Padding）** - 不增加参数
```
[x₁, x₂, ..., xₙ] → [x₁, x₂, ..., xₙ, 0, 0, ..., 0]
```

**选项B：1×1 投影卷积** - 增加参数，效果更好
```python
if self.downsample:
    residual = nn.Conv2d(in_ch, out_ch, kernel_size=1, stride=2)(x)
    residual = nn.BatchNorm2d(out_ch)(residual)
```

---

## 💻 完整 PyTorch 实现

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class BasicBlock(nn.Module):
    """ResNet-18/34 的基础块"""
    expansion = 1
    
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        # 当维度不匹配时，需要1×1卷积调整
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
    
    def forward(self, x):
        residual = self.shortcut(x)   # 跳跃路径
        
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        
        out = out + residual   # 关键：残差加法
        out = F.relu(out)
        return out


class Bottleneck(nn.Module):
    """ResNet-50/101/152 的瓶颈块"""
    expansion = 4
    
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        # 1×1: 降维
        self.conv1 = nn.Conv2d(in_channels, out_channels, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        # 3×3: 主要特征学习
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        # 1×1: 升维
        self.conv3 = nn.Conv2d(out_channels, out_channels * self.expansion, 1, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels * self.expansion)
        
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels * self.expansion:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels * self.expansion, 1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels * self.expansion)
            )
    
    def forward(self, x):
        residual = self.shortcut(x)
        
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        
        out = out + residual
        out = F.relu(out)
        return out


class ResNet(nn.Module):
    def __init__(self, block, num_blocks, num_classes=1000):
        super().__init__()
        self.in_channels = 64
        
        # 初始卷积层（stem）
        self.stem = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2, padding=1)
        )
        
        # 4个残差层
        self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=2)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=2)
        
        # 全局平均池化 + 分类头
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)
        
        # 权重初始化（He初始化）
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
    
    def _make_layer(self, block, out_channels, num_blocks, stride):
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for s in strides:
            layers.append(block(self.in_channels, out_channels, s))
            self.in_channels = out_channels * block.expansion
        return nn.Sequential(*layers)
    
    def forward(self, x):
        x = self.stem(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avgpool(x)
        x = x.flatten(1)
        x = self.fc(x)
        return x


def ResNet50(num_classes=1000):
    return ResNet(Bottleneck, [3, 4, 6, 3], num_classes)

def ResNet101(num_classes=1000):
    return ResNet(Bottleneck, [3, 4, 23, 3], num_classes)

def ResNet152(num_classes=1000):
    return ResNet(Bottleneck, [3, 8, 36, 3], num_classes)

# 验证
model = ResNet50()
x = torch.randn(2, 3, 224, 224)
out = model(x)
print(f"输出形状: {out.shape}")
params = sum(p.numel() for p in model.parameters())
print(f"参数量: {params:,}")  # ~25,557,032
```

---

## 🌟 ResNet 的深远影响

### 直接影响

| 后续工作 | 基于 ResNet | 改进点 |
|---------|------------|--------|
| ResNeXt (2017) | ResNet + 分组卷积 | 更宽，更高效 |
| WideResNet (2016) | 更宽的 ResNet | 减少深度，增加宽度 |
| DenseNet (2017) | 每层连到所有后续层 | 极致特征复用 |
| SENet (2017) | ResNet + 通道注意力 | ImageNet 2017冠军 |
| EfficientNet (2019) | 复合缩放 | 精度效率双优 |

### 超越视觉

残差连接的思想被迁移到几乎所有深度学习领域：
- **Transformer**：每个 Attention 和 FFN 块后都有残差连接
- **BERT/GPT**：完全依赖残差连接实现深度堆叠
- **U-Net**：跳跃连接用于图像分割
- **神经ODE**：把残差连接视为微分方程离散化

---

## 📐 理论视角：为什么残差连接有效？

### 视角1：梯度高速公路

残差连接提供了一条从输出层到输入层的**梯度直通车道**：

$$
\frac{\partial L}{\partial x} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial x} = \frac{\partial L}{\partial y} \cdot \left(1 + \frac{\partial \mathcal{F}(x)}{\partial x}\right)
$$

那个 "+1" 保证了梯度信号永远不会完全消失！

### 视角2：隐式集成

有研究者（Veit et al., 2016）认为，ResNet 相当于对指数级数量的"浅层路径"进行集成：

一个10层的 ResNet 包含 $2^{10} = 1024$ 条不同长度的路径。训练实际上是在优化这个"浅层网络集成"，比显式深层网络更容易。

### 视角3：损失曲面平滑化

Li et al.（2018）可视化了有无残差连接的损失曲面：
- **无残差**：损失曲面崎岖，充满尖锐的局部极小值
- **有残差**：损失曲面平滑，优化器容易找到好的路径

---

## 🎓 总结

| 维度 | 评价 |
|------|------|
| **历史地位** | ⭐⭐⭐⭐⭐ 最重要的架构创新之一 |
| **核心创新** | Skip Connection（跳跃/残差连接） |
| **竞赛成绩** | ImageNet 2015 五冠王，错误率3.57% |
| **影响范围** | 从CNN到Transformer，无处不在 |
| **引用次数** | 超过16万次，AI历史上最多引用之一 |

> **一句话总结**：ResNet 用"把输入加回输出"这一个简单加法，解开了深层网络优化的枷锁，开启了"超深网络"时代，并通过残差连接这个普适原则，影响了此后所有的深度学习架构。

---

*⬇️ 下一篇：Transformer (2017) —— "Attention is All You Need"，重写NLP的圣经*
