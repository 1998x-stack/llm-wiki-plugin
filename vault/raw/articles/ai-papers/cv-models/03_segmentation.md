# ✂️ 图像分割模型深度分析（2025）

> **核心任务**：对图像进行像素级理解，将图像划分为有意义的区域。  
> **2025 最大范式转变**：SAM（Segment Anything）系列重塑了分割领域，从封闭类别分割走向开放世界零样本分割。

---

## 1. 分割任务分类体系

```
图像分割
├── 语义分割 (Semantic Segmentation)
│     每个像素分配一个类别标签（如"天空"、"道路"）
│     代表：SegFormer, HRNet, DeepLab v3+
│
├── 实例分割 (Instance Segmentation)
│     区分同类别的不同个体（每只猫都有独立掩码）
│     代表：Mask R-CNN, YOLO-seg, SOLO
│
├── 全景分割 (Panoptic Segmentation)
│     语义分割 + 实例分割的统一
│     代表：Panoptic FPN, Mask2Former, OMG-Seg
│
├── 交互式分割 (Interactive Segmentation)
│     用户点击/框选，模型输出精确掩码
│     代表：SAM / SAM2 / SAM3（零样本提示驱动）
│
├── 视频目标分割 (Video Object Segmentation, VOS)
│     跨帧追踪目标的像素级掩码
│     代表：SAM2, XMem, DEVA
│
└── 特域分割
      医学影像分割（CT/MRI/超声）
      遥感图像分割
      伪装目标分割
```

---

## 2. SAM 系列（Segment Anything Models）

### 2.1 SAM（原版，Meta AI，2023年4月）

**革命性意义：**
- 第一个能够"分割任意对象"的通用基础模型
- 无需类别标签，零样本泛化
- 三种提示方式：点击（正/负点）、矩形框、粗略掩码

**架构：**
```
Image Encoder   : ViT-H（重型，主要计算量）
Prompt Encoder  : 位置编码（点/框）+ 文本投影
Mask Decoder    : 轻量 Transformer，< 4ms
```

**训练数据：SA-1B**
```
11 亿个掩码，1100 万张图像
完全自动化数据引擎（模型辅助标注）
迄今最大的分割数据集
```

**速度局限（vs YOLO）：**
```
SAM-B (Base):    
  参数量  91M  
  延迟    ~50ms（仅Decoder）但Image Encoder耗时更长
  
YOLOv8n-seg:    
  参数量  3.3M（SAM的1/28）
  延迟    ~1.5ms（1069× 快于 SAM-B）

SAM 优势：零样本能力；YOLO 优势：速度与部署效率
```

---

### 2.2 SAM 2（Meta AI，2024年7月，ICLR 2025 论文）

**核心改进：统一图像+视频分割**

**架构革新：**
```
新增 Streaming Memory 流式记忆机制：
  ┌─────────────────────────────────────┐
  │  Memory Encoder  →  Memory Bank     │
  │  (存储历史帧特征)                    │
  │                                     │
  │  Memory Attention                   │
  │  (当前帧 attention 历史帧)           │
  │                                     │
  │  Occlusion Head                     │
  │  (预测目标是否被遮挡)                │
  └─────────────────────────────────────┘

实时推理：44 FPS on NVIDIA A100
```

**训练数据：SA-V**
```
35.5M 掩码（视频掩码）
50.9K 段视频
比任何已有视频分割数据集多 53×
```

**性能提升：**
```
交互次数：比 SAM1 少 3×（更少点击完成分割）
VOS 基准：全面超越此前 SOTA
图像分割：与 SAM1 相当或更好
```

**SAM 2 型号规格：**

| 型号 | 参数量 | 速度(ms) | 精度 | 适用 |
|------|--------|---------|------|------|
| SAM2-tiny (t) | ~38M | 最快 | ★★★ | 边缘推理、嵌入式 |
| SAM2-small (s) | ~46M | 快 | ★★★☆ | 生产部署平衡 |
| SAM2-base+ (b+) | ~80M | 中 | ★★★★ | 默认推荐 |
| SAM2-large (l) | ~224M | 慢 | ★★★★★ | 精度优先研究 |

**核心应用：**
- ✅ 视频目标追踪分割（自动传播帧间）
- ✅ 交互式标注工具（替代人工精标）
- ✅ 医学图像半自动分割
- ✅ 自动驾驶数据标注管线（TIER IV 实现 40× 加速）
- ✅ AR 场景理解

---

### 2.3 SAM 3（最新版，2025年）

**主要改进：**
```
重新设计架构与训练流程（更高效）
伪装目标分割（Camouflaged Object Detection）能力显著提升
  - SAM/SAM2 在伪装场景常产生错误/无意义掩码
  - SAM3 能基本定位伪装目标（边界仍需 SAM3-Adapter 精化）

医学图像分割能力提升
性能更强但参数更精简
```

**SAM3-Adapter（配套方案）：**
```
轻量 Adapter 模块 + SAM3 骨干
在以下任务建立新 SOTA：
  - 伪装目标分割（COD10K、CAMO、CHAMELEON）
  - 医学图像分割（细胞、器官）
  - 阴影检测（Shadow Instance Detection）
```

---

### 2.4 Grounded SAM 2（集成方案）

```
= GroundingDINO（文本提示检测）+ SAM 2（精确分割）

能力：用文本描述分割视频中的任意对象
  例："追踪并分割红色轿车"→ 全程跟踪掩码

工作流：
  文字描述 → GroundingDINO 定位 → 生成 bbox 提示
  bbox 提示 → SAM 2 Decoder → 精确像素掩码
  Memory 传播 → 视频帧间传播

开源实现：github.com/IDEA-Research/Grounded-SAM-2
```

---

## 3. 语义分割专项模型

### 3.1 SegFormer（NVIDIA，2021，仍广泛使用）
```
架构：Mix Transformer (MiT) + 轻量 All-MLP Decoder
特色：无位置编码（分辨率自适应），推理速度快
B5 版本在 ADE20K: mIoU 51.0%
适用：自动驾驶场景理解、工业语义分析
```

### 3.2 Mask2Former（Meta AI，2022）
```
统一架构处理三类分割任务（语义/实例/全景）
核心：Masked Attention（遮罩注意力聚焦前景）
全景分割 COCO: PQ 57.8
适用：复杂场景多类别分割
```

### 3.3 OMG-Seg（2024-2025，10合1统一框架）
```
OMG = One Model for General Segmentation
单模型覆盖10种分割任务：
  语义、实例、全景
  交互式（SAM 风格）、目标检测、关键点
  指代分割（Referring）、开放词汇
  视频实例、视频全景

架构：基于 Mask2Former，增加任务路由与统一 Decoder
意义：端到端多任务，显著降低部署复杂度
```

---

## 4. 实例分割模型

### 4.1 Mask R-CNN 系列（经典两阶段）
```
架构：Faster R-CNN + Mask Head
输出：bbox + 类别 + 像素掩码
精度：COCO 40%+ AP（ResNet-101 FPN）
缺点：速度慢（~5 FPS on V100），两阶段开销

改进版：
  Cascade Mask R-CNN → 更高精度
  QueryInst         → Transformer Query
  Mask Dino         → DINO 骨干
```

### 4.2 YOLO-seg 系列（实时实例分割）
```
YOLOv8-seg / YOLO11-seg
  = 检测头 + 原型掩码 + 掩码系数预测
  
速度：~15-30 FPS on V100（比 SAM 快数百倍）
精度：COCO ~40% mask AP
适用：实时视频分析、安防、工业质检
```

---

## 5. HRNet（高分辨率网络，2019，仍是语义分割主干之一）
```
核心思想：始终维持高分辨率特征表示
对比其他网络：其他网络编码时逐渐降分辨率
HRNet 特点：
  - 并行多分辨率子网络
  - 跨分辨率频繁融合
  - 从不丢弃高分辨率特征

精度：ADE20K 语义分割 mIoU 45.1 (HRNet-W48)
适用：精细边界分割、密集预测任务
缺点：计算量大，速度不如 SegFormer
```

---

## 6. 医学图像分割专项

### 6.1 挑战与特点
```
医学图像 vs 自然图像的差异：
  - 模态多样：CT / MRI / 超声 / 病理切片
  - 色彩信息弱，边界模糊
  - 标注稀缺，专业知识门槛高
  - 类内变化大（个体器官差异）
  - 标注 3D 体积数据（而非2D图像）
```

### 6.2 主流方案

| 模型 | 特点 | 适用 |
|------|------|------|
| nnU-Net | 自动超参调整的医学标准基线 | 各类医学分割任务 |
| SAM2 Fine-tuned | BioSAM-2, FS-MedSAM2, RadSAM2 | 半自动医学标注 |
| TransUNet | Transformer + U-Net 混合 | 腹部器官分割 |
| SwinUNet | 纯 Swin Transformer | 高精度医学分割 |
| MedSAM | SAM 在医学数据上微调 | 通用医学分割适配 |

**SAM2 医学微调关键发现（2025研究）：**
```
• 影响分割精度的关键因素：
  目标大小（小目标 < 大目标）
  位置（边缘 vs 中心）
  结构复杂度（规则 vs 不规则）
  与周围组织的对比度

• 微调后提升（BTCV 腹部数据集）：
  Dice ↑ 约 15-25%（比零样本基线）
  
• 乳腺超声：DSC 99.22%（专项微调后）
```

---

## 7. 全景视角：分割任务大比较

| 维度 | SAM2 | YOLO-seg | Mask2Former | SegFormer | OMG-Seg |
|------|------|---------|------------|---------|---------|
| 任务范围 | 交互式/VOS | 实例 | 三合一 | 语义 | 全任务(10合1) |
| 零样本能力 | ★★★★★ | ★★ | ★★★ | ★★ | ★★★ |
| 推理速度 | ★★★ | ★★★★★ | ★★★ | ★★★★ | ★★★ |
| 精度 | ★★★★★ | ★★★★ | ★★★★★ | ★★★★ | ★★★★ |
| 无类别限制 | ✅ | ❌ | ❌ | ❌ | ✅(开放词汇版) |
| 视频支持 | ✅ | ❌ | ❌ | ❌ | ✅ |
| 部署难度 | 中 | 低 | 中 | 低 | 高 |

---

## 8. FastSAM & MobileSAM（轻量化方案）

### FastSAM（YOLO Everything）
```
原理：用 YOLO 实例分割 + 点/框提示 模拟 SAM 功能
速度：比 SAM 快 50×
精度：低于 SAM（牺牲边界精度）
适用：资源受限场景的近似替代
```

### MobileSAM
```
参数：5.7M（SAM-B 的 1/16）
图像编码器：TinyViT（蒸馏自 ViT-H）
速度：~10ms（单图，CPU 可运行）
适用：移动端/嵌入式 SAM 部署
```

---

## 9. 自动标注流水线（重要工程应用）

```
传统标注流水线（人工）：
  图像 → 人工逐像素勾勒 → 质检 → 入库
  速度：~30 分钟/张（实例分割）

基于 SAM2 的自动标注流水线（TIER IV 案例）：
  图像 → YOLOv8 检测框 → 作为 SAM2 提示
  → SAM2 生成精确掩码
  → 质量过滤 + 人工审核
  速度提升：40×（从 30min → 45sec）
  精度：IoU 无下降（TensorRT 优化后）

适用于：
  自动驾驶数据标注（行人/车辆/道路）
  工业质检（缺陷像素级定位）
  医学图像预标注辅助
```

---

## 10. 选型决策树

```
需要分割？
│
├─ 有固定类别 & 需要实时？
│    └─ YES → YOLO11-seg（最快实例分割）
│
├─ 需要零样本 & 交互式？
│    └─ YES → SAM2-base+（最佳通用选择）
│              SAM3-Adapter（特殊场景如伪装/医学）
│
├─ 语义分割（整体场景理解）？
│    └─ YES → SegFormer-B5（速度精度均衡）
│
├─ 全景分割（检测+语义+实例全覆盖）？
│    └─ YES → Mask2Former 或 OMG-Seg
│
├─ 视频追踪分割？
│    └─ YES → SAM2（流式内存跨帧追踪）
│
├─ 资源极度受限（手机/嵌入式）？
│    └─ YES → MobileSAM 或 FastSAM
│
└─ 医学图像？
     └─ YES → nnU-Net（标准基线）
               + SAM2 微调（半自动标注）
```

---

*数据来源：Meta SAM2 论文（ICLR 2025）、Ultralytics Docs、OMG-Seg 论文、SAM3-Adapter（arXiv 2511.19425）、医学SAM2研究（EJoRAI 2025）*
