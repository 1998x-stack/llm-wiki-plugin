# 🧠 经典 AI 论文完整时间线
> 从感知机到大语言模型——深度学习70年演进史

---

## 🕰️ 时间线总览

| 年份 | 论文 | 作者 | 核心贡献 | 领域 |
|------|------|------|----------|------|
| 1943 | A Logical Calculus of Ideas Immanent in Nervous Activity | McCulloch & Pitts | 第一个神经元数学模型 | 神经网络基础 |
| 1958 | The Perceptron: A Probabilistic Model for Information Storage | Rosenblatt | 感知机，第一个可学习神经网络 | 神经网络基础 |
| 1969 | Perceptrons | Minsky & Papert | 证明感知机局限性，引发第一次AI寒冬 | 理论 |
| 1986 | Learning Representations by Back-propagating Errors | Rumelhart, Hinton, Williams | 反向传播算法，深度学习基础 | 优化 |
| 1989 | Multilayer Feedforward Networks are Universal Approximators | Hornik et al. | 万能近似定理 | 理论 |
| 1992 | A Training Algorithm for Optimal Margin Classifiers | Boser et al. | 支持向量机 SVM | 机器学习 |
| 1997 | Long Short-Term Memory | Hochreiter & Schmidhuber | LSTM，解决梯度消失 | 序列模型 |
| 1998 | Gradient-Based Learning Applied to Document Recognition | LeCun et al. | LeNet-5，卷积神经网络成熟 | CNN |
| 2001 | Random Forests | Breiman | 随机森林 | 机器学习 |
| 2006 | Reducing the Dimensionality of Data with Neural Networks | Hinton & Salakhutdinov | 深度信念网络，深度学习复兴 | 表示学习 |
| 2009 | ImageNet: A Large-Scale Hierarchical Image Database | Deng et al. | ImageNet数据集，催生视觉革命 | 数据集 |
| 2012 | **ImageNet Classification with Deep CNNs (AlexNet)** | Krizhevsky, Sutskever, Hinton | AlexNet，深度学习革命元年 | CNN |
| 2013 | Efficient Estimation of Word Representations (Word2Vec) | Mikolov et al. | 词向量，NLP表示学习 | NLP |
| 2013 | Dropout: A Simple Way to Prevent Neural Networks from Overfitting | Srivastava et al. | Dropout正则化 | 正则化 |
| 2013 | Playing Atari with Deep Reinforcement Learning (DQN) | Mnih et al. | 深度强化学习 | RL |
| 2014 | Very Deep Convolutional Networks (VGGNet) | Simonyan & Zisserman | VGG，深度的力量 | CNN |
| 2014 | Going Deeper with Convolutions (GoogLeNet/Inception) | Szegedy et al. | Inception模块，多尺度特征 | CNN |
| 2014 | Generative Adversarial Nets (GAN) | Goodfellow et al. | 生成对抗网络 | 生成模型 |
| 2014 | Sequence to Sequence Learning with Neural Networks | Sutskever et al. | Seq2Seq，机器翻译革命 | NLP |
| 2014 | Neural Machine Translation by Jointly Learning to Align (Attention) | Bahdanau et al. | 注意力机制 | NLP |
| 2015 | **Batch Normalization** | Ioffe & Szegedy | 批归一化，训练加速神器 | 优化 |
| 2015 | **Deep Residual Learning for Image Recognition (ResNet)** | He et al. | 残差网络，解决深度退化 | CNN |
| 2015 | U-Net: Convolutional Networks for Biomedical Image Segmentation | Ronneberger et al. | U-Net，图像分割 | 分割 |
| 2015 | Fast R-CNN / Faster R-CNN | Girshick / Ren et al. | 目标检测里程碑 | 检测 |
| 2016 | You Only Look Once (YOLO) | Redmon et al. | 实时目标检测 | 检测 |
| 2016 | Deep Residual Networks (Identity Mappings) | He et al. | PreAct ResNet | CNN |
| 2016 | WaveNet: A Generative Model for Raw Audio | van den Oord et al. | 语音生成 | 生成模型 |
| 2017 | **Attention Is All You Need (Transformer)** | Vaswani et al. | Transformer，现代AI基石 | NLP |
| 2017 | Proximal Policy Optimization (PPO) | Schulman et al. | 强化学习主流算法 | RL |
| 2018 | **BERT: Pre-training of Deep Bidirectional Transformers** | Devlin et al. | BERT，预训练模型范式 | NLP |
| 2018 | Improving Language Understanding by Generative Pre-Training (GPT-1) | Radford et al. | GPT系列开山之作 | NLP |
| 2019 | Language Models are Unsupervised Multitask Learners (GPT-2) | Radford et al. | Zero-shot学习能力 | NLP |
| 2019 | XLNet: Generalized Autoregressive Pretraining | Yang et al. | 自回归预训练 | NLP |
| 2020 | Language Models are Few-Shot Learners (GPT-3) | Brown et al. | 千亿参数，涌现能力 | NLP |
| 2020 | Denoising Diffusion Probabilistic Models (DDPM) | Ho et al. | 扩散模型，图像生成新范式 | 生成模型 |
| 2021 | An Image is Worth 16x16 Words (ViT) | Dosovitskiy et al. | 视觉Transformer | 视觉 |
| 2021 | Learning Transferable Visual Models (CLIP) | Radford et al. | 图文对齐，零样本视觉 | 多模态 |
| 2021 | DALL-E: Zero-Shot Text-to-Image Generation | Ramesh et al. | 文生图第一代 | 生成模型 |
| 2022 | Training language models to follow instructions (InstructGPT) | Ouyang et al. | RLHF对齐，ChatGPT前身 | 对齐 |
| 2022 | High-Resolution Image Synthesis with LDMs (Stable Diffusion) | Rombach et al. | 潜在扩散模型 | 生成模型 |
| 2023 | LLaMA: Open and Efficient Foundation Language Models | Touvron et al. | 开源大模型 | NLP |
| 2023 | GPT-4 Technical Report | OpenAI | 多模态超大模型 | NLP |
| 2024 | DeepSeek-V2/V3/R1 | DeepSeek | 高效MoE架构，开源之光 | NLP |

---

## 📚 分析文章索引

| # | 论文 | 状态 |
|---|------|------|
| 01 | 感知机 Perceptron (1958) | ✅ |
| 02 | 反向传播 Backpropagation (1986) | ✅ |
| 03 | LeNet-5 (1998) | ✅ |
| 04 | AlexNet (2012) | ✅ |
| 05 | Word2Vec (2013) | ✅ |
| 06 | Dropout (2013) | ✅ |
| 07 | VGGNet (2014) | ✅ |
| 08 | GAN (2014) | ✅ |
| 09 | Attention 注意力机制 (2014) | ✅ |
| 10 | Batch Normalization (2015) | ✅ |
| 11 | ResNet (2015) | ✅ |
| 12 | Transformer (2017) | ✅ |
| 13 | BERT (2018) | ✅ |
| 14 | GPT 系列 (2018-2020) | ✅ |
| 15 | DDPM 扩散模型 (2020) | ✅ |
| 16 | ViT (2021) | ✅ |
| 17 | CLIP (2021) | ✅ |
| 18 | RLHF / InstructGPT (2022) | ✅ |

---

*按顺序逐篇深度解析，敬请期待 👇*
