# 🎨 图像生成模型深度分析（2025）

> **核心任务**：从文本描述（或噪声/参考图）生成高质量图像。  
> **技术主线**：扩散模型（Diffusion）已全面取代 GAN，Diffusion Transformer 正在取代 U-Net。

---

## 1. 技术架构谱系

### 1.1 扩散模型基本原理
```
正向过程（训练）: 真实图像 → 逐步加高斯噪声 → 纯噪声
反向过程（推理）: 纯噪声 → 逐步去噪 → 生成图像

关键改进：
  潜空间扩散 (LDM) → 在压缩的潜空间操作，大幅降低计算量
  CFG (分类器无关引导) → 文本控制质量与多样性的平衡
  Flow Matching → FLUX 的核心，更直接的概率路径，收敛更快
```

### 1.2 核心架构对比

| 架构 | 代表模型 | 骨干 | 条件注入方式 |
|------|---------|------|------------|
| LDM U-Net | SD 1.x / SDXL | ResNet+Cross-Attention | Cross-Attention on text tokens |
| DiT | SD 3, PixArt | Transformer | Adalayer-norm + Cross-Attn |
| Flow Matching DiT | FLUX.1/2 | MM-DiT | 文本与图像 token 联合建模 |
| AR + DiT Hybrid | GLM-Image | Autoregressive+DiT | LLM 生成语义 token，DiT 解码细节 |
| VAR (Next-Scale) | LlamaGen | AR Scale-up | 从粗到精逐尺度预测 |

---

## 2. 主流模型深度对比

### 2.1 FLUX 系列（Black Forest Labs）
> 由 Stability AI 原团队创建，2024-2025 年最具影响力的开源生成模型家族

**架构特点：**
- **MM-DiT（Mixed Multimodal DiT）**：文本 token 与图像 patch 在同一序列中联合注意力
- **Flow Matching**：替代 DDPM，训练路径更直接，推理步数少
- **双流 vs 单流混合**：早期层用双流（图文分离），后期层合并为单流

**FLUX 版本对比：**

| 版本 | 参数量 | 速度 | 质量 | 许可 | 特色 |
|------|--------|------|------|------|------|
| FLUX.1 [schnell] | 12B | 极快(1-4步) | ★★★☆ | Apache 2.0 | 本地原型开发 |
| FLUX.1 [dev] | 12B | 快(20-30步) | ★★★★ | 非商用 | 实验研究 |
| FLUX.1.1 [pro] | 12B | 快(6×加速) | ★★★★★ | 商用API | 当前最强Text2Img |
| FLUX.2 [dev] | 32B | 中 | ★★★★★ | 非商用 | 多参考一致性(最多10张) |
| FLUX.1 Kontext | 12B | 快 | ★★★★★ | 非商用 | 上下文感知图像编辑 |

**FLUX 核心优势：**
- ✅ 文字渲染能力业界领先（尤其英文）
- ✅ 提示词跟随精确（复杂多段提示词均可执行）
- ✅ 人体解剖正确率高（手部、面部、多人场景）
- ✅ 生态快速成熟（LoRA、ComfyUI 适配完善）
- ❌ 32B 版本本地部署需要大显存（≥40GB）

---

### 2.2 Stable Diffusion 系列（Stability AI）
> 开源生态最丰富，Civitai/Hugging Face 上存在数万个微调模型

**版本演进：**
```
SD 1.5 (2022)  → 512px, ResNet U-Net, LoRA 生态奠基
SDXL (2023)    → 1024px, 双ClipText编码器, 质量飞跃
SD 3 (2024)    → MM-DiT架构, 三文本编码器(CLIP×2+T5), 文字渲染改善
SD 3.5 Large (2024) → 8.1B参数, 当前开源最强SD变体
```

**SD 3.5 Large 技术细节：**
- 骨干：MM-DiT + QK-Norm + 改进型 Shift
- 文本编码：CLIP-L + CLIP-G + T5-XXL（三编码器融合）
- 分辨率：最高 2048px
- 缺点：高分辨率生成仍有构图崩溃问题

**社区生态（SD 独有）：**
- LoRA 微调：5-10 张图即可训练特定风格/人物
- Checkpoint 社区：DreamShaper、JuggernautXL、RealVisXL 等
- ControlNet：精确姿态/边缘/深度控制
- 平台：ComfyUI、A1111、Forge

---

### 2.3 Midjourney v7
> 商用闭源，艺术美感领域无可争议的王者

| 维度 | 表现 |
|------|------|
| 艺术风格多样性 | ⭐⭐⭐⭐⭐ 最强 |
| 摄影写实感 | ⭐⭐⭐⭐ |
| 提示词精确跟随 | ⭐⭐⭐ 较弱（有创意解读） |
| 文字渲染 | ⭐⭐⭐ 中等 |
| 价格 | $10-120/月订阅 |
| API | 无官方 API |
| 特色功能 | Permutations, Zoom, Pan, 个性化风格 |

---

### 2.4 Google Imagen 4 / Adobe Firefly 3
**Imagen 4 特点：**
- 超写实照片质感，皮肤纹理与光影最接近真实摄影
- 文字渲染能力同级最强（与 Ideogram 并列）
- 通过 Gemini 接口或 Vertex AI 访问

**Adobe Firefly 3：**
- 唯一经过完整版权合规训练（Adobe Stock 授权数据）
- 商业使用最安全，支持责任 AI 溯源（Content Credentials）
- 深度集成 Photoshop、Illustrator 工作流

---

### 2.5 DALL-E 3 / GPT Image 1.5（OpenAI）
- **提示词理解最强**：ChatGPT 会自动优化提示词再生成
- **指令跟随精确**：复杂构图、多对象场景执行能力强
- 通过 API 调用支持 Inpainting（`--use_mask`）
- 内置 C2PA 数字水印溯源

---

### 2.6 新兴中文特化模型
| 模型 | 机构 | 特色 |
|------|------|------|
| GLM-Image | 智谱AI | AR+DiT混合，中英双语文字渲染最强 |
| Qwen-Image | 阿里巴巴 | Qwen系列生态，API接入方便 |
| Z-Image-Turbo | 智谱 | 超快推理，媲美FLUX质量，Apache 2.0 |
| Kolors | 快手 | 中文文字渲染专项优化 |
| Seedream 4.0 | 字节跳动 | 国内商业平台领先品质 |

---

## 3. 综合性能横向对比

### 3.1 主要维度得分（满分5）

| 模型 | 写实感 | 艺术感 | 提示精确 | 文字渲染 | 生成速度 | 开源 | 价格 |
|------|--------|--------|---------|---------|---------|------|------|
| FLUX.1.1 Pro | 5 | 4 | 5 | 4 | 5(API) | ❌ | 按需 |
| FLUX.2 dev | 5 | 4 | 5 | 4 | 3 | ✅ | 免费 |
| Midjourney v7 | 4 | 5 | 3 | 3 | 4 | ❌ | 订阅 |
| SD 3.5 Large | 4 | 4 | 4 | 4 | 4(本地) | ✅ | 免费 |
| Imagen 4 | 5 | 3 | 4 | 5 | 3 | ❌ | API |
| DALL-E 3 / GPT-Img | 4 | 3 | 5 | 4 | 3 | ❌ | API |
| Ideogram v2 | 3 | 4 | 4 | 5 | 3 | ❌ | 按需 |
| GLM-Image | 3 | 3 | 4 | 5(中文) | 4 | ✅ | API |

### 3.2 ELO 排行榜（Artificial Analysis Text-to-Image Leaderboard）
```
🥇 Recraft V3           ELO: 1172
🥈 FLUX1.1 Pro Ultra    ELO: ~1160
🥉 Midjourney v7        ELO: ~1150
4. Ideogram v2          ELO: ~1140
5. Google Imagen 4      ELO: ~1135
6. DALL-E 3 HD          ELO: ~1110
7. FLUX1.1 Pro          ELO: ~1100
8. SD 3.5 Large         ELO: ~1080
```

---

## 4. 关键技术能力专项测评

### 4.1 文字渲染能力
```
级别    模型
★★★★★  Ideogram v2, Imagen 4, GLM-Image(中文)
★★★★   FLUX.1.1 Pro, SD 3.0/3.5, DALL-E 3
★★★    Midjourney v7, SDXL
★★      SD 1.5, SDXL早期版本
```

### 4.2 人体解剖准确性（手/面部）
```
★★★★★  FLUX 系列（行业最佳）
★★★★   SD 3.5 Large
★★★    DALL-E 3
★★★    Midjourney v7
★★      SD 1.5（严重手指畸变）
```

### 4.3 LoRA / 自定义微调支持
```
完整生态：SD 1.5/SDXL（数万 LoRA 可用）
良好支持：FLUX dev（LoRA 社区快速成长）
有限支持：SD 3.5
不支持  ：Midjourney, DALL-E, Imagen（闭源）
```

---

## 5. 架构趋势分析

### 5.1 Flow Matching 取代 DDPM
```python
# DDPM 传统方式：随机加噪路径
# Flow Matching：线性最优传输路径
# 优势：
# - 推理步数减少 50-80%（4步即可生成高质量图像）
# - 训练更稳定
# - 条件控制更精确
```

### 5.2 多参考一致性（FLUX.2 核心特性）
```
传统问题：每次生成都是随机采样，角色/商品无法保持一致
FLUX.2 方案：最多 10 张参考图同时输入
应用场景：
  - 品牌内容：同一产品不同场景的一致视觉
  - 角色设计：统一人物跨场景保持形象
  - 系列内容：连续剧情图的角色连贯性
```

### 5.3 原生多分辨率支持
```
FLUX / SD 3.x 支持任意宽高比输出（--aspect）
典型分辨率：
  1:1  → 1024×1024（社交媒体头像）
  9:16 → 768×1344（竖版短视频封面）
  16:9 → 1344×768（横版缩略图）
  2:3  → 832×1248（书籍封面/海报）
```

---

## 6. 生产部署选型建议

### 6.1 按场景选型矩阵

| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| 电商产品图（大批量） | FLUX.1.1 Pro API | 速度快、质量稳定、提示精确 |
| 艺术创意探索 | Midjourney v7 | 美感独特，出乎意料的创意解读 |
| 本地无限生成（研究） | FLUX.2 dev / SD 3.5 | 开源免费，ComfyUI 完整工作流 |
| 商业合规（广告/设计） | Adobe Firefly 3 | 版权授权最完整 |
| 中文海报/排版 | GLM-Image / Kolors | 中文文字渲染专项优化 |
| 游戏资产（角色/场景） | FLUX + LoRA | 可训练特定风格/世界观 |
| 营销素材批量生成 | FLUX.1 Schnell | 1-4步超速，降低成本 |

### 6.2 硬件要求参考

| 模型 | 推荐显存 | 最低显存 | 备注 |
|------|---------|---------|------|
| SD 1.5 | 6GB | 4GB | 最轻量，消费级 GPU |
| SDXL | 12GB | 8GB | 需 xformers 优化 |
| SD 3.5 Medium | 10GB | 8GB | - |
| SD 3.5 Large | 24GB | 16GB(int8) | - |
| FLUX.1 dev | 24GB | 12GB(int8/nf4) | - |
| FLUX.2 dev | 80GB | 40GB | 需要 A100/H100 |

---

## 7. 商业生态与定价

| 提供商 | 定价模式 | 参考价格 |
|--------|---------|---------|
| Black Forest Labs (FLUX) | 按图计费 | ~$0.04-0.08/图 |
| OpenAI (DALL-E 3) | API 按 token | ~$0.04/1024px |
| Google (Imagen 4) | Vertex AI | ~$0.02-0.10/图 |
| Midjourney | 订阅制 | $10-120/月 |
| Adobe Firefly | CC 订阅包含 | 信用点制 |
| Stability AI | API + 本地 | 按需 |
| SiliconFlow (FLUX) | 按图计费 | ~¥0.28/图 |

---

## 8. 未来趋势

1. **实时生成**：目标 < 1 秒生成，用于实时预览与游戏
2. **视频扩展**：FLUX 与 Sora/Veo 技术融合，图像→视频一致性生成
3. **可控性提升**：3D 感知控制（精确相机视角、光源位置）
4. **个性化微调**：低门槛 DreamBooth/LoRA，手机端可调
5. **原生多模态**：图、视频、音频在同一模型中联合生成

---

*参考来源：Black Forest Labs 技术博客、Stability AI 论文、Artificial Analysis Leaderboard、BentoML 开源指南（2025-2026）*
