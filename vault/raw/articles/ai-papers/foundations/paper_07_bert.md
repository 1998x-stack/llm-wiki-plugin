# 论文精读 #07：BERT
## BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
**作者：Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova | 2018 | Google AI Language**

---

## 🎯 一句话概括

> BERT 用"完形填空"和"判断两句话是否相邻"两个自监督任务，在海量无标注文本上预训练双向 Transformer，然后用极少的标注数据微调到下游任务——在 11 项 NLP 基准上同时刷新 SOTA，开创了"预训练+微调"的现代 NLP 范式。

---

## 🌍 时代背景：从特征到预训练

### NLP 的"特征工程"时代困境

2018 年之前，NLP 任务的标准流程：

```
任务A（情感分析）：设计特征 → 训练分类器
任务B（命名实体识别）：设计不同特征 → 训练不同分类器
任务C（问答）：设计更不同特征 → 训练更不同分类器
```

每个任务独立训练，无法共享"语言理解"能力，且依赖大量人工标注数据。

### ELMo：预训练的曙光（2018年初）

ELMo（Embeddings from Language Models）用双向 LSTM 预训练得到词向量，下游任务拿来直接用——效果大幅提升。但 ELMo 的语言模型是**单向**的（从左到右或从右到左独立训练）。

### GPT-1：单向 Transformer 预训练（2018年中）

OpenAI 的 GPT-1 用单向 Transformer（只从左看到右）做语言模型预训练，微调后在多个任务上超越 ELMo。

但单向模型的问题：理解"bank"这个词，需要同时看左右上下文（"river bank"vs"bank account"），单向 Transformer 做不到。

### BERT 的关键问题

> 能不能同时用**左右两侧的上下文**来预训练 Transformer？

直接做双向语言模型（预测下一个词）行不行？——不行，因为"下一个词"已经在右侧上下文中，双向模型会"作弊"。

BERT 的解决方案：**换一个预训练任务！**

---

## 🏗️ BERT 架构

BERT 就是一个**多层双向 Transformer Encoder**（只用 Encoder，不用 Decoder）：

```
输入 Token 序列：
[CLS] 我 爱 [MASK] 国 [SEP] 北京是首都 [SEP]

每个 token 的输入嵌入 = Token嵌入 + 位置嵌入 + 句子段嵌入
                              ↓
             ┌────────────────────────────┐
             │  Transformer Encoder L1    │  ← 双向自注意力
             │  Transformer Encoder L2    │
             │          ...               │
             │  Transformer Encoder L12   │
             └────────────────────────────┘
                              ↓
             每个 token 的上下文感知表示

[CLS] 表示 → 下游分类任务
[MASK] 表示 → 预测被遮盖的词
```

**两个版本：**

| 版本 | 层数(L) | 隐层维度(H) | 注意力头(A) | 参数量 |
|------|---------|-----------|-----------|-------|
| BERT-base | 12 | 768 | 12 | **110M** |
| BERT-large | 24 | 1024 | 16 | **340M** |

---

## 🔑 预训练任务一：Masked Language Model（MLM）完形填空

### 核心思想

随机遮盖输入中 **15%** 的 token，让模型预测被遮盖的词。

```
原始句子：我 喜欢 吃 北京 烤鸭
         ↓ 随机遮盖 15%
输入模型：我 喜欢 [MASK] 北京 烤鸭
         ↓ 模型预测
目标输出：       "吃"      （被遮盖位置）
```

**为什么这个任务好？**
- 预测"吃"，模型必须同时理解左侧"我喜欢"和右侧"北京烤鸭"→ 强制**双向**理解
- 无需人工标注！直接用任意文本即可
- 等价于超大规模的"完形填空考试"

### 遮盖策略的细节

15% 的 token 中：
- **80%** 真正替换为 `[MASK]`
- **10%** 替换为随机词
- **10%** 保持原词不变

**为什么不全部替换为 [MASK]？**
因为下游任务中没有 `[MASK]` token，全部替换会造成预训练和微调的分布差异。随机词和保持原词迫使模型对每个 token 都保持警惕，不能"偷懒"。

---

## 🔑 预训练任务二：Next Sentence Prediction（NSP）句子关系判断

### 核心思想

给模型两个句子，判断第二句是不是第一句的下一句：

```
正例（IsNext = True，50%）：
[CLS] 我去了北京 [SEP] 那里的烤鸭很好吃 [SEP]

负例（NotNext = False，50%）：
[CLS] 我去了北京 [SEP] 量子力学是物理学分支 [SEP]（随机负采样）
```

目的：让模型理解**句间关系**，对问答（QA）和自然语言推理（NLI）任务有帮助。

*后续研究（RoBERTa）发现 NSP 任务实际帮助有限，可以去掉。*

---

## 🔄 输入表示的细节

```
Token：  [CLS]  我    爱   [MASK]  [SEP]  北京  是  首都  [SEP]
Token ID:  101   2344  1234   103    102   1345 ... ...    102

嵌入层（三者相加）：
Token Embedding:    每个词的语义向量        (30522维词表)
Position Embedding: 位置 0,1,2,3,4...     (可学习，非正弦)
Segment Embedding:  句子A用0，句子B用1     (区分两个句子)

最终输入 = Token_emb + Position_emb + Segment_emb
```

---

## 📊 预训练数据与训练规模

| 资源 | 规模 |
|------|------|
| BooksCorpus | 8亿词 |
| English Wikipedia | 25亿词 |
| **总计** | **33亿词** |
| 训练硬件 | 64 个 TPU v3（BERT-large） |
| 训练时间 | 4天 |
| 计算量 | 约 $10^{21}$ FLOPs |

---

## 🎯 下游任务微调：一个模型，11 个 SOTA

BERT 预训练后，只需在顶部添加简单的输出层，用少量标注数据微调：

### 场景一：句子分类

```
输入：[CLS] 这部电影太棒了 [SEP]
                ↓
        取 [CLS] 的表示
                ↓
         Linear → Softmax
                ↓
        正面/负面（情感分析）
```

### 场景二：序列标注（NER）

```
输入：[CLS] 张 三 在 北 京 [SEP]
               ↓
每个token的表示 → Linear
               ↓
        B-PER I-PER O B-LOC I-LOC
```

### 场景三：问答（SQuAD）

```
问题：李白是哪个朝代的诗人？
段落：李白（701年-762年），唐朝浪漫主义诗人...

输入：[CLS] 李白是哪个朝代的诗人 [SEP] 李白（701年）... [SEP]
               ↓
    预测答案的起始位置和结束位置
               ↓
        "唐朝"（span extraction）
```

---

## 📈 BERT 的压倒性成绩

### GLUE 综合基准（11项任务平均分）

| 模型 | GLUE Score |
|------|-----------|
| 人类基准 | 87.1 |
| GPT (2018) | 72.8 |
| **BERT-base** | **79.6** |
| **BERT-large** | **82.1** |

**BERT-large 超越之前所有模型平均 7.7 分！**

### SQuAD 1.1（阅读理解）

| 模型 | F1 |
|------|-----|
| 人类 | 91.2 |
| 之前 SOTA | 86.0 |
| **BERT-large（单模型）** | **93.2** |

**首次超越人类！**

---

## 🔬 BERT 学到了什么？解释性研究

### 注意力头的专业化

研究者发现不同的注意力头学到了不同的语言学知识：

```
头 #1-2：   关注相邻词（局部语法）
头 #3-5：   关注句法依存关系
头 #6-8：   关注指代关系（"it" → "animal"）
头 #9-12：  关注语义关系
```

### 不同层的语言学层次

```
浅层 (1-4层):   词法/形态（词性标注、命名实体）
中层 (5-8层):   句法（依存关系、成分结构）
深层 (9-12层):  语义（语义角色、共指消解）
```

这和人类语言处理的层次结构高度吻合！

---

## 💻 使用 HuggingFace 微调 BERT

```python
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
import torch
from torch.utils.data import Dataset

# 1. 加载预训练 BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForSequenceClassification.from_pretrained(
    'bert-base-chinese',
    num_labels=2  # 正面/负面情感
)

# 2. 数据集
class SentimentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=128):
        self.encodings = tokenizer(
            texts,
            truncation=True,
            padding='max_length',
            max_length=max_len,
            return_tensors='pt'
        )
        self.labels = torch.tensor(labels)
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        return {
            'input_ids': self.encodings['input_ids'][idx],
            'attention_mask': self.encodings['attention_mask'][idx],
            'labels': self.labels[idx]
        }

# 3. 训练
train_texts = ["这个产品很好用", "太差劲了，浪费钱", "物美价廉推荐"]
train_labels = [1, 0, 1]

train_dataset = SentimentDataset(train_texts, train_labels, tokenizer)

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    learning_rate=2e-5,          # BERT 微调关键：学习率要小！
    warmup_steps=100,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)
trainer.train()

# 4. 推理
def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    pred = logits.argmax(-1).item()
    return "正面" if pred == 1 else "负面"

print(predict_sentiment("这款手机性价比超高！"))  # 正面
print(predict_sentiment("客服态度极差，不推荐"))   # 负面
```

---

## 🌊 BERT 的影响：百模大战

BERT 发布后，NLP 进入"预训练竞赛"时代：

| 模型 | 机构 | 时间 | 关键改进 |
|------|------|------|---------|
| **RoBERTa** | Facebook | 2019 | 去掉 NSP，更大数据，更久训练 |
| **ALBERT** | Google | 2019 | 参数共享，大幅减少参数 |
| **DistilBERT** | HuggingFace | 2019 | 知识蒸馏，小而快 |
| **XLNet** | Google/CMU | 2019 | 自回归+置换语言模型 |
| **SpanBERT** | Facebook | 2019 | 遮盖连续片段 |
| **MacBERT** | 哈工大讯飞 | 2020 | 中文MLM改进 |
| **ERNIE** | 百度 | 2019 | 引入知识图谱 |

---

## 🆚 BERT vs GPT：两种范式的分野

| 维度 | BERT | GPT |
|------|------|-----|
| **架构** | Transformer Encoder | Transformer Decoder |
| **方向** | 双向 | 单向（从左到右） |
| **预训练任务** | MLM（完形填空） | 语言模型（预测下一词） |
| **擅长任务** | 理解（分类、NER、QA） | 生成（翻译、摘要、对话） |
| **使用方式** | 预训练→微调 | 预训练→提示/微调 |
| **代表应用** | 搜索引擎、文本分类 | ChatGPT、代码生成 |

这两条路线后来发展成了整个大模型生态的两大分支。

---

## 🎓 总结

| 维度 | 评价 |
|------|------|
| **历史地位** | ⭐⭐⭐⭐⭐ 现代 NLP 分水岭 |
| **核心创新** | 双向 MLM 预训练 + 微调范式 |
| **竞赛成绩** | 11 项 GLUE/SQuAD 任务同时刷新 SOTA |
| **影响范围** | 搜索引擎、语音助手、机器翻译 |
| **哲学意义** | "语言理解"可以从无标注文本中自监督学习 |

> **一句话总结**：BERT 用"完形填空"这个小学生都会的任务，教会了机器深度理解语言——它证明了只要预训练任务设计得好，无标注的海量文本本身就是最好的老师。

---
*⬇️ 下一篇：GAN 生成对抗网络 (2014) —— 两个神经网络的博弈游戏，开创生成式AI新纪元*
