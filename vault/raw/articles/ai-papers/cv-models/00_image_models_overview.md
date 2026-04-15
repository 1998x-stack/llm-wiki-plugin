# 🗺️ 图像 AI 模型全景导览（2025）

> **研究视角**：从工程落地角度，系统梳理图像 AI 模型的 10 大功能类别，覆盖架构演进、SOTA 基准、选型建议与应用场景。

---

## 🧭 类别总览

| # | 类别 | 核心任务 | 2025 SOTA 代表 | 技术范式 |
|---|------|---------|----------------|---------|
| 1 | **图像生成** (Text-to-Image) | 从文本/噪声生成图像 | FLUX.2, SD 3.5, Imagen 4 | Diffusion Transformer |
| 2 | **目标检测** (Object Detection) | 定位并分类图像中的目标 | YOLOv12, RF-DETR, D-FINE | CNN+Attention / Transformer |
| 3 | **图像分割** (Segmentation) | 像素级理解，区域分割 | SAM2/SAM3, OMG-Seg, Mask2Former | 提示驱动 Foundation Model |
| 4 | **视觉语言模型** (VLM) | 图文联合理解与推理 | Gemini 2.5 Pro, GPT-4o, Qwen2.5-VL | 多模态大语言模型 |
| 5 | **图像超分** (Super Resolution) | 低分辨率→高分辨率重建 | Real-ESRGAN, SwinIR, DRCT | GAN / Diffusion / Transformer |
| 6 | **深度估计** (Depth Estimation) | 单目/双目深度图预测 | Depth Anything v3, Marigold, UniDepth | ViT / Diffusion |
| 7 | **姿态估计** (Pose Estimation) | 人体/物体关键点检测 | ViTPose, DWPose, MotionBERT | Transformer / HRNet |
| 8 | **图像编辑与修复** (Editing/Inpainting) | 局部修改、风格迁移、扩图 | FLUX Kontext, InstructPix2Pix, PowerPaint | Diffusion + ControlNet |
| 9 | **图像到3D** (Image-to-3D) | 单/多视角重建3D模型 | TripoSR, Zero123++, CRM, InstantMesh | 3D Diffusion / NeRF / 3DGS |
| 10 | **图像分类** (Classification) | 全局类别标签预测 | CLIP, CoCa, ConvNeXt V2, DINOv2 | ViT / 对比学习 |

---

## 🏗️ 技术演进时间线

```
2020    DETR (Transformer 首次用于检测)
2021    CLIP (对比学习视觉-语言对齐)
2022    Stable Diffusion (开源扩散模型革命)
        Segment Anything (SAM, Meta 零样本分割)
2023    GPT-4V / LLaVA (VLM 爆发)
        YOLOv8, YOLOv9 (实时检测优化)
2024    FLUX.1 (Diffusion Transformer, 取代 U-Net)
        SAM2 (图像+视频统一分割)
        InternVL2 / Qwen2.5-VL (开源VLM追平闭源)
2025    YOLOv12 (Area Attention 注意力检测)
        RF-DETR (>60% mAP, 首个突破 COCO 60分)
        FLUX.2 / FLUX Kontext (多参考一致性生成)
        SAM3 (更高精度伪装/医学分割)
        Depth Anything v3 (几何一致深度估计)
        Gemini 2.5 Pro (多模态推理 SOTA)
        Qwen3-VL (最新旗舰VLM)
```

---

## 🔑 关键技术范式对比

### 1. 扩散模型 vs. GAN vs. 自回归
| 范式 | 代表 | 优势 | 劣势 |
|------|------|------|------|
| Diffusion (U-Net) | SD 1.x~2.x | 生态丰富，LoRA 扩展性强 | 速度慢，U-Net 感受野受限 |
| Diffusion Transformer | FLUX, SD3 | 更强提示跟随，扩展性好 | 计算量大 |
| AR + Diffusion Hybrid | GLM-Image | 文字渲染强，语义精准 | 生态尚不成熟 |
| GAN | StyleGAN3 | 速度极快，面部特化强 | 多样性差，训练不稳定 |

### 2. CNN vs. Transformer 在检测/分割中的地位
```
纯CNN (YOLO早期版本)     → 快，但全局感受野弱
CNN+Attention (YOLOv12)  → 兼顾速度与语义理解
纯Transformer (DETR)     → 全局建模强，收敛慢
混合DETR (RT-DETR, RF-DETR) → 当前最佳精度-速度折中
```

### 3. Foundation Model 趋势
- **SAM 系列**：一个模型，零样本分割任意对象，成为分割领域的"预训练底座"
- **CLIP/DINOv2**：作为通用视觉编码器，被大量下游任务复用
- **VLM**：将"看图理解"与"语言推理"统一，向 AGI 视觉迈进

---

## 📊 模型规模 vs. 精度 全局分布

```
参数量  │ 小(<1B)          │ 中(1-10B)          │ 大(>10B)
───────────────────────────────────────────────────────────
生成    │ FLUX Schnell     │ SD 3.5 Medium      │ FLUX.2 dev (32B)
检测    │ YOLOv12-N(2.6M)  │ RF-DETR-B(29M)     │ RF-DETR-L(128M)
分割    │ MobileSAM(5.7M)  │ SAM2-B(80M)        │ SAM2-L(224M)
VLM     │ Phi3-Vision(4B)  │ Qwen2.5-VL-7B      │ Qwen2.5-VL-72B
```

---

## 🧩 开源 vs. 闭源对比

| 类别 | 顶级开源 | 顶级闭源 | 开源差距 |
|------|---------|---------|---------|
| 生成 | FLUX.2, SD 3.5 | Midjourney v7, Imagen 4 | 接近 |
| 检测/分割 | YOLOv12, SAM2 | - | 几乎无差距 |
| VLM | Qwen2.5-VL-72B, InternVL3 | GPT-4o, Gemini 2.5 | MMMU差4~8点 |
| 超分/深度 | RealESRGAN, DA3 | - | 几乎无差距 |

---

## 📂 子文档索引

| 文档 | 内容 |
|------|------|
| `01_image_generation.md` | 图像生成 · FLUX/SD/Midjourney/Imagen 全面对比 |
| `02_object_detection.md` | 目标检测 · YOLOv12/RF-DETR/D-FINE 深度剖析 |
| `03_segmentation.md` | 图像分割 · SAM生态/Mask2Former/OMG-Seg |
| `04_vlm.md` | 视觉语言模型 · GPT-4o/Gemini/Qwen-VL/InternVL |
| `05_super_resolution.md` | 图像超分 · ESRGAN/SwinIR/扩散超分 |
| `06_depth_estimation.md` | 深度估计 · Depth Anything/Marigold/UniDepth |
| `07_pose_estimation.md` | 姿态估计 · ViTPose/DWPose/3D姿态 |
| `08_image_editing.md` | 图像编辑 · FLUX Kontext/ControlNet/Inpainting |
| `09_image_to_3d.md` | 图像到3D · TripoSR/Zero123/3DGS重建 |
| `10_classification.md` | 图像分类 · CLIP/CoCa/ConvNeXt/DINOv2 |

---

*更新时间：2025 Q1 | 覆盖 ICLR 2025 / CVPR 2025 / NeurIPS 2024 关键成果*
