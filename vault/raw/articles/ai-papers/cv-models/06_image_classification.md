# 🏷️ 图像分类模型深度分析（2025）

> **核心任务**：给整张图像分配类别标签（单标签 or 多标签）。  
> **2025 地位**：图像分类是基础任务，但 CLIP/DINOv2 等视觉编码器已成为更广泛下游任务的骨干，"分类"边界模糊化。

---

## 1. 技术演进脉络

```
传统机器学习 (SIFT + SVM)
  ↓
深度 CNN 时代：
  AlexNet (2012) → VGG → GoogLeNet → ResNet (2015) → EfficientNet (2019)
  
Vision Transformer 时代：
  ViT (2020) → DeiT → Swin Transformer (2021) → ConvNeXt → MaxViT (2022)
  
多模态/对比学习时代：
  CLIP (2021) → ALIGN → BLIP → CoCa → SigLIP (2023)
  
自监督预训练时代：
  MAE (2022) → DINOv2 (2023) → I-JEPA (2023)
  
2024-2025：
  ConvNeXt V2 → InternViT-6B（超大视觉编码器）
  → 分类本身退位，特征提取器价值更大
```

---

## 2. 主流分类模型深度分析

### 2.1 CLIP（OpenAI，2021，仍是最广泛使用的）

**架构：双塔 + 对比学习**
```
图像编码器（ViT 或 ResNet）
     ↕  余弦相似度对比
文本编码器（Transformer）

训练：4亿图文对，最大化匹配对相似度、最小化不匹配对

零样本分类流程：
  1. 准备类别文字描述："a photo of a {class}"
  2. 编码所有类别文字 → 文本特征向量
  3. 编码输入图像 → 图像特征向量
  4. 计算图像与每个类别的余弦相似度
  5. 选择相似度最高的类别
```

**关键特性：**
- ✅ 零样本分类（无需任何微调）
- ✅ 任意类别名称（开放词汇）
- ✅ 特征可直接用于检索、分割、生成引导
- ✅ ImageNet 零样本精度 76.2%（ViT-L/14）
- ❌ 细粒度任务（区分相似物种）弱于专门训练模型

**变体与改进：**
```
CLIP ViT-B/32  → 轻量快速
CLIP ViT-L/14  → 标准高精度
CLIP ViT-L/14@336px → 高分辨率

OpenCLIP：开源复现，支持更多数据集
SigLIP (Google)：改用 Sigmoid 损失，减少内存，精度更高
MetaCLIP：回归原始CLIP数据策略，可复现
```

---

### 2.2 DINOv2（Meta，2023）

**最强通用视觉特征提取器之一**

```
训练方式：自监督 + 蒸馏
  - 不使用任何标签
  - 自监督 DINO（教师-学生蒸馏）
  - 额外加入监督信号（有标注数据）

数据：LVD-142M（精选自142M张图像）

特点：
  - 特征不专属于分类，可直接用于检测/分割/深度估计
  - 比 CLIP 更强的局部特征（精确到边缘）
  - 浮现出语义分割能力（无需分割标签训练）

型号：
  DINOv2-S (21M), DINOv2-B (86M), DINOv2-L (307M), DINOv2-G (1.1B)

ImageNet 线性探测：
  DINOv2-G: 86.5%（仅线性分类头，特征不微调）
```

**DINOv2 下游应用（重要）：**
```
RF-DETR: DINOv2 作为检测骨干，COCO SOTA
语义分割：DINOv2 特征 + 线性头，ADE20K 47%+ mIoU
深度估计：DINOv2 + DPT 头，Depth Anything 系列骨干
图像检索：相似图像搜索
```

---

### 2.3 CoCa（Google，2022）

**最强图像分类精度（有监督）**
```
架构：CLIP 图像编码器 + 文本 Decoder（两个loss）
  - 对比损失（同 CLIP）
  - 字幕生成损失（新增）

训练数据：ALIGN + LAION（约44亿图文对）

ImageNet Fine-tuned Top-1: 91.0%（当时最高）
ImageNet 零样本: 86.3%

特点：
  结合了 CLIP 的对比能力 + 生成能力
  可直接输出图像描述
```

---

### 2.4 ConvNeXt V2（Meta + 学术界，2023）

**纯 CNN 最强图像分类模型**
```
架构演进：
  ConvNeXt V1：卷积"transformer化"（组归一化、GELU、倒置瓶颈）
  ConvNeXt V2：新增 FCMAE（全卷积掩码自编码器）预训练

特点：
  - 比 ViT 推理更快（无需注意力）
  - 训练稳定，对小数据集友好
  - ConvNeXt V2-H: ImageNet top-1 88.9%（无EMA）

变体：
  Tiny (28M) → Small → Base → Large → Huge (660M)
  从移动端到服务器全覆盖
```

---

### 2.5 EfficientNet V2（Google，2021）

**效率与精度的黄金均衡**
```
NAS（神经架构搜索）优化架构
关键创新：
  - 渐进式训练（小图→大图）
  - 混合 MBConv + Fused-MBConv
  - 参数利用率极高

EfficientNetV2-L: ImageNet 85.7%（Params: 120M）
EfficientNetV2-S: ImageNet 83.9%（Params: 21M）← 移动部署首选

对比：比 EfficientNet V1 快 6×，准确率更高
```

---

### 2.6 Swin Transformer（Microsoft，2021）

**层次化 ViT，检测/分割的通用骨干**
```
关键创新：
  局部窗口注意力（减少计算量 O(n) vs O(n²)）
  移位窗口（跨窗信息交流）
  层次化特征图（类似 ResNet FPN 兼容性）

Swin-L: ImageNet 87.3%
用途：
  ✅ 作为检测/分割骨干（兼容 FPN 多尺度）
  ✅ SwinIR 超分模型骨干
  不如 ViTPose 在姿态估计中通用
```

---

## 3. 零样本 vs 有监督分类

### 3.1 零样本分类能力排行
```
ImageNet Zero-Shot Top-1:
  SigLIP-So400M  ：83.2%（当前最强开源零样本）
  CLIP ViT-L/14  ：76.2%
  MetaCLIP      ：76.2%（CLIP 的可复现版本）
  OpenCLIP ViT-H ：78.0%
  ALIGN         ：76.4%
```

### 3.2 有监督微调精度排行（ImageNet Top-1）
```
CoCa（Fine-tuned）  ：91.0%（ViT-G）
ViT-G/14 JFT       ：90.5%
SwinV2-G           ：90.2%
ConvNeXt V2-H      ：88.9%（纯CNN最强）
EfficientNetV2-XL  ：87.3%

注：ImageNet 预测精度接近人类天花板（~95% 争议）
2025 的竞争更多在于域外泛化和少样本学习
```

---

## 4. 特殊分类任务

### 4.1 细粒度分类（Fine-Grained）
```
任务：区分相似子类（200种鸟类、120种狗）
挑战：类内差异小，类间差异微
方案：
  注意力机制（聚焦判别区域）
  部分感知：先检测关键部位再分类
  代表：WS-DAN, ALIGN（ALIGN 在细粒度好于CLIP）
数据集：CUB-200, Stanford Dogs, Aircraft
```

### 4.2 医学图像分类
```
特殊挑战：数据稀少、标注昂贵、类别不平衡
常用策略：
  迁移学习（从 ImageNet 预训练）
  对比学习（BioViL, MedCLIP）
  病理切片：分块分类 → 多实例聚合（MIL）

代表模型：
  CheXpert（胸片14类）
  REMEDIS（Google Health图像迁移学习）
  BioMedCLIP（医学图文对预训练）
```

### 4.3 多标签分类
```
场景：一张图有多个类别（"海滩 + 人 + 日落"）
方法：
  去除最后 Softmax，改为 Sigmoid（独立类别概率）
  标签相关性建模（GCN、Transformer 图结构）
代表：ASL（Asymmetric Loss），ML-Decoder
```

### 4.4 长尾分类
```
问题：数据集中大多数类样本极少（幂律分布）
方案：
  重采样（过采样稀少类）
  损失重加权（focal loss 扩展）
  CLIP 零样本作为辅助（不依赖训练数据量）
```

---

## 5. 视觉预训练范式对比

| 方法 | 代表 | 监督信号 | 优势 | 劣势 |
|------|------|---------|------|------|
| 监督分类 | ResNet, EfficientNet | 标签 | 特定任务精度高 | 需大量标注 |
| 对比学习 | CLIP, SigLIP | 图文配对（弱监督） | 零样本强，通用特征 | 细粒度弱 |
| 自监督 MAE | ViT-MAE | 掩码重建（无监督） | 数据效率高 | 特征泛化性 |
| 自监督DINO | DINOv2 | 蒸馏（无监督） | 局部特征最强 | 训练复杂 |
| 生成式 | CoCa, BLIP-2 | 生成+对比 | 既能分类又能描述 | 计算量大 |

---

## 6. 工程选型指南

### 6.1 按需求选型

| 需求 | 推荐模型 | 理由 |
|------|---------|------|
| 有固定类别 + 大量标注 | EfficientNetV2-S/M | 速度精度均衡，易部署 |
| 零样本分类（任意类别） | SigLIP / CLIP ViT-L | 无需训练，灵活 |
| 作为下游任务特征 | DINOv2-L / G | 最强通用视觉特征 |
| 移动端轻量 | EfficientNetV2-S, MobileNetV3 | 参数少，LiteRT 可用 |
| 最高分类精度（预算不限） | CoCa ViT-G | ImageNet 91% |
| 开源纯 CNN | ConvNeXt V2-B/L | 纯卷积，部署简单 |

### 6.2 微调策略

```
策略 1：线性探测（Linear Probe）
  冻结预训练骨干
  只训练最后分类头
  数据量：100-1000张/类
  适合：快速验证特征质量

策略 2：完整微调（Full Fine-tuning）
  解冻所有层
  使用小学习率（1e-5 ~ 1e-4）
  数据量：1000张+/类
  适合：追求最高精度

策略 3：LoRA / Parameter-Efficient
  仅训练少量适配层
  用于 ViT 类大模型
  数据量：100张+/类

策略 4：Few-Shot（少样本）
  CLIP + 少量样例，无需训练
  5-shot CoOp 方案：仅训练文本提示词
```

---

## 7. 2025-2026 分类领域趋势

1. **分类退出中心舞台**：VLM 已将"分类"融入通用理解，专项分类模型减少
2. **DINOv2 作为万能骨干**：用于检测/分割/深度/分类的统一预训练源
3. **零样本成为标配**：CLIP 系的零样本能力让标注成本大幅降低
4. **视频级理解**：从单帧分类扩展到视频动作识别（VideoMAE、TimeSformer）
5. **3D 分类**：从2D图像分类扩展到3D点云分类（PointBERT、Point-MAE）

---

*数据来源：Papers With Code ImageNet Leaderboard，CLIP 论文，DINOv2 论文（Meta），CoCa 论文（Google），Efficient SR/Classification 2025 surveys*
