# 文本预处理与分词
> Text Preprocessing & Tokenization — 深度解析系列 第 2 篇

---

## 1. 为什么文本预处理至关重要

搜索引擎的本质是**词条匹配（Term Matching）**。文本预处理决定了：
- 哪些词条会被索引（影响**召回率**）
- 词条如何归一化（影响**精确率**）
- 词条的粒度（影响**索引大小**）

**黄金法则：** 查询时的预处理步骤必须与索引时**完全一致**，否则查询词条永远无法命中索引词条。

```
索引时: "Running" → tokenize → normalize → stem → "run"
查询时: "runs"    → tokenize → normalize → stem → "run"
                                                    │
                                              匹配成功 ✓
```

---

## 2. 预处理完整流水线

```
原始文本: "The QUICK Brown FOX jumped over the lazy dogs!!!"
    │
    ▼ Step 1: 字符级清洗 (Character-level Cleaning)
"The QUICK Brown FOX jumped over the lazy dogs"
    │
    ▼ Step 2: 分词 (Tokenization)
["The", "QUICK", "Brown", "FOX", "jumped", "over", "the", "lazy", "dogs"]
    │
    ▼ Step 3: 大小写归一化 (Case Normalization)
["the", "quick", "brown", "fox", "jumped", "over", "the", "lazy", "dogs"]
    │
    ▼ Step 4: 停用词过滤 (Stop Word Removal)
["quick", "brown", "fox", "jumped", "lazy", "dogs"]
    │
    ▼ Step 5: 词形还原 / 词干提取 (Lemmatization / Stemming)
["quick", "brown", "fox", "jump", "lazi", "dog"]      ← Porter Stemmer
["quick", "brown", "fox", "jump", "lazy", "dog"]      ← Lemmatization
    │
    ▼ Step 6: 同义词扩展 (可选)
["quick"/"fast", "brown", "fox", "jump"/"leap", "lazy", "dog"]
    │
    ▼ 最终词条流 → 写入倒排索引
```

---

## 3. 分词（Tokenization）深度解析

### 3.1 空白分词（Whitespace Tokenizer）

最简单的分词策略，按空白字符切分：

```python
text = "Hello, world! This is a test."
tokens = text.split()
# → ["Hello,", "world!", "This", "is", "a", "test."]
# 问题：标点符号粘连
```

**问题：** 标点没有被正确分离，"world!" ≠ "world"。

---

### 3.2 标准分词（Standard Tokenizer）

按照 Unicode 规则进行分词，处理字母、数字和标点：

**规则：**
1. 字母序列 → 单独词条
2. 数字序列 → 单独词条
3. 标点符号 → 分隔符（不保留）
4. 连字符特殊处理（如 "state-of-the-art"）

```python
text = "Hello, world! C++ is great. U.S.A. is a country."

# 标准分词结果:
# ["Hello", "world", "C", "is", "great", "U.S.A", "is", "a", "country"]
# 注意: "U.S.A." 保留缩写，"C++" 的 "++" 被丢弃
```

**边界案例处理矩阵：**

| 输入 | 简单分词 | 标准分词 | 期望行为 |
|------|---------|---------|---------|
| `"can't"` | `["can't"]` | `["can", "t"]` | `["cannot"]` 或保留 |
| `"U.S.A."` | `["U.S.A."]` | `["U.S.A"]` | 保留缩写 ✓ |
| `"hello-world"` | `["hello-world"]` | `["hello", "world"]` | 取决于场景 |
| `"3.14"` | `["3.14"]` | `["3.14"]` | 保留数字 ✓ |
| `"C++"` | `["C++"]` | `["C"]` | 语言名需特殊处理 |
| `"2024-01-01"` | `["2024-01-01"]` | `["2024", "01", "01"]` | 日期需专用分词 |

---

### 3.3 中文分词（Chinese Tokenization）

中文没有天然的空格分隔符，是**最复杂的分词场景**。

#### 3.3.1 歧义问题举例

```
"南京市长江大桥" 
  → ["南京市", "长江", "大桥"]   # 解读1: 南京市的长江大桥
  → ["南京", "市长", "江大桥"]   # 解读2: 南京的市长江大桥（荒谬）
  → ["南京市长", "江大桥"]       # 解读3: 南京市长 江大桥（人名+桥）
```

#### 3.3.2 主流中文分词算法

**A. 基于词典的前向最大匹配（Forward Maximum Matching）**

```
词典: {南京, 南京市, 长, 长江, 大桥, 市长, 市, 长江大桥}
输入: "南京市长江大桥"

前向最大匹配（词典最长词为4字）:
步骤1: 尝试"南京市长" → 在词典中? 是 → 匹配
步骤2: 剩余"江大桥"
步骤3: 尝试"江大桥" → 不在词典
步骤4: 尝试"江大" → 不在词典
步骤5: 尝试"江" → 在词典
步骤6: 剩余"大桥" → 在词典

结果: ["南京市长", "江", "大桥"]  ← 错误！
```

**B. 基于隐马尔可夫模型（HMM）的分词**

将分词视为序列标注问题：
- 状态集合: `{B(Beginning), M(Middle), E(End), S(Single)}`
- 观测序列: 字符序列
- 转移概率: P(state_t | state_{t-1})
- 发射概率: P(char | state)

```
输入: 南  京  市  长  江  大  桥
状态: B   E   S   B   M   M   E
分词: [南京][市][长江大桥]  ← Viterbi算法求最优路径
```

**HMM 参数（以 jieba 为例的概念）：**

```python
# 转移概率矩阵示例（对数概率）
transitions = {
    'B': {'M': -0.916, 'E': -0.510},
    'M': {'M': -0.333, 'E': -1.157},
    'E': {'B': -0.539, 'S': -0.868},
    'S': {'B': -0.599, 'S': -0.631},
}
```

**C. 基于条件随机场（CRF）的分词**

CRF 是 HMM 的判别式版本，考虑更多特征：

```
特征函数示例:
f1(y_t, y_{t-1}, x, t) = [y_t==E AND x_t 是数字]
f2(y_t, y_{t-1}, x, t) = [y_t==B AND y_{t-1}==S]
f3(y_t, y_{t-1}, x, t) = [x_{t-1}x_t 是常见词前缀]
```

**D. 主流中文分词工具对比**

| 工具 | 算法 | 速度 | 准确率 | 特点 |
|------|------|------|-------|------|
| **jieba** | 前向最大匹配 + HMM | ★★★★ | ★★★ | 最流行，支持自定义词典 |
| **pkuseg** | CRF + 多领域模型 | ★★★ | ★★★★ | 北大出品，领域优化 |
| **thulac** | CRF | ★★★ | ★★★★ | 清华出品，词性标注 |
| **hanlp** | 深度学习 | ★★ | ★★★★★ | 功能最全，中文NLP生态 |
| **LTP** | BiLSTM-CRF | ★★ | ★★★★★ | 哈工大，工业级 |

---

### 3.4 N-gram 分词

将连续 N 个字符/词作为一个词条，适合处理拼写错误和部分匹配：

**字符级 N-gram（用于拼写容错）：**
```
词: "search"
Bi-gram (N=2): {se, ea, ar, rc, ch}
Tri-gram (N=3): {sea, ear, arc, rch}
```

**词级 N-gram（用于短语匹配）：**
```
句子: "machine learning is great"
Bi-gram: {machine learning, learning is, is great}
Tri-gram: {machine learning is, learning is great}
```

**N-gram 的权衡：**

| N 值 | 优势 | 劣势 |
|------|------|------|
| 1 (Unigram) | 索引最小 | 无法捕捉词序关系 |
| 2 (Bigram) | 捕捉相邻关系 | 索引扩大5-10倍 |
| 3 (Trigram) | 短语匹配能力强 | 索引扩大20-50倍 |

---

## 4. 大小写归一化（Case Normalization）

### 4.1 基础策略

```python
# 策略1: 全部小写（最常用）
"The Quick Brown Fox" → "the quick brown fox"

# 策略2: 大写转小写，保留缩写
"USA Today" → "usa today"  # 信息丢失！

# 策略3: TrueCase（预测正确大小写）
"usa today" → "USA Today"  # 使用ML模型还原
```

### 4.2 大小写折叠的复杂性

某些语言的大小写折叠并非简单的 `lower()`：

```python
# 土耳其语: 大小写折叠规则不同
"I" → "i"  (英语)
"I" → "ı"  (土耳其语，无点 i)

# 德语: ß 展开
"straße" → "strasse"  (搜索"strasse"应匹配"straße")

# 希腊语: 音调标记
"άνθρωπος" → "ανθρωπος"  (去除音调)
```

---

## 5. 停用词过滤（Stop Word Removal）

### 5.1 什么是停用词

停用词是在语言中**出现频率极高但语义贡献极低**的词语：

**英文常见停用词（共约 100-200 个）：**
```
a, an, the, is, are, was, were, be, been, being,
have, has, had, do, does, did, will, would, could, should,
in, on, at, to, for, with, by, of, from, ...
```

**中文常见停用词：**
```
的, 了, 是, 在, 我, 有, 和, 就, 不, 人, 都, 一, 一个,
上, 也, 很, 到, 说, 要, 去, 你, 会, 着, 没有, 看, 好, ...
```

### 5.2 为什么过滤停用词

| 动机 | 说明 |
|------|------|
| **减小索引体积** | "the" 出现在几乎所有文档中，其 posting list 极长 |
| **提升检索速度** | 跳过高频词的大型 posting list |
| **提升相关性** | 避免常见词影响 TF-IDF 评分 |

### 5.3 停用词过滤的风险

⚠️ 某些情况下**不应该**过滤停用词：

```
查询: "to be or not to be"  → 莎士比亚名句，全部是停用词
查询: "who is the president" → 停用词主导的问答查询
查询: "the office"           → 电视剧名称中含停用词
查询: "to do list"           → 短语含义依赖停用词

解决方案: 短语检索时保留停用词；使用位置索引；
          对命名实体识别后的结果不过滤停用词。
```

### 5.4 IDF 自动停用词检测

现代搜索引擎不依赖静态停用词列表，而是**通过 IDF 自动识别**：

```
IDF(t) = log(N / df_t)

当 df_t → N 时（出现在几乎所有文档中）：
IDF(t) → log(N/N) = log(1) = 0

IDF ≈ 0 的词条 → 自动获得极低权重 → 效果等同于被过滤
```

---

## 6. 词干提取（Stemming）

词干提取是一种**启发式规则**方法，将词语粗糙地截断为词根形式。

### 6.1 Porter Stemmer（最经典）

由 Martin Porter 于 1980 年提出，包含 5 组规则：

**基础概念：**
```
辅音序列: C = [consonant]+
元音序列: V = [vowel]+
词形结构: (VC)^m VCC* 其中 m 为量度
```

**规则示例（第 1 组 - 复数/过去式）：**

| 规则 | 条件 | 输入 → 输出 |
|------|------|------------|
| SSES → SS | - | caresses → caress |
| IES → I | - | ponies → poni |
| SS → SS | - | caress → caress |
| S → (删除) | 词干长度>0 | cats → cat |

**规则示例（第 2 组 - 动词形式）：**

| 输入 | Porter 词干 |
|------|------------|
| running | run |
| runner | runner（注意不是run！） |
| generalization | general |
| generalize | general |
| electricity | electr |
| electrical | electr |

**Porter Stemmer 完整示例：**
```python
from nltk.stem import PorterStemmer
ps = PorterStemmer()

words = ["running", "runs", "runner",
         "studies", "studying", "studied",
         "generalization", "generalizes"]

for w in words:
    print(f"{w:20s} → {ps.stem(w)}")

# running              → run
# runs                 → run
# runner               → runner    ← 注意！runner ≠ run
# studies              → studi
# studying             → studi
# studied              → studi
# generalization       → general
# generalizes          → general
```

### 6.2 Snowball Stemmer（改进版 Porter）

也叫 Porter2，修正了 Porter 的多个错误：

```python
from nltk.stem import SnowballStemmer
ss = SnowballStemmer("english")

print(ss.stem("generously"))  # → generous（Porter: → generous）✓
print(ss.stem("carefully"))   # → care（Porter: → care）✓
print(ss.stem("hopefully"))   # → hope（Porter: → hope）✗ 应为 hopeful
```

### 6.3 主流词干提取算法对比

| 算法 | 激进程度 | 错误率 | 特点 |
|------|---------|-------|------|
| **Porter** | 中等 | ~5% | 最经典，广泛使用 |
| **Snowball (Porter2)** | 中等 | ~3% | Porter 改进版 |
| **Lancaster** | 激进 | ~15% | 词干极短，过截断多 |
| **Lovins** | 激进 | ~12% | 最早的自动词干提取 |

**词干提取的典型错误：**

| 类型 | 示例 | 问题 |
|------|------|------|
| 过度截断 (Overstemming) | `general` ← `generalize` 和 `general` | 不相关词被合并 |
| 截断不足 (Understemming) | `operate` ≠ `operating`（Lancaster可能截断不一致） | 相关词未合并 |
| 无效词干 | `studi`（study的词干） | 产生无意义字符串 |

---

## 7. 词形还原（Lemmatization）

词形还原是基于**词典和语法分析**的精确归一化，返回词典中真实存在的基本形式（lemma）。

### 7.1 词干提取 vs 词形还原

| 对比维度 | 词干提取 | 词形还原 |
|---------|---------|---------|
| 方法 | 规则截断 | 词典查询 + 词性分析 |
| 速度 | ★★★★★ 极快 | ★★★ 较慢 |
| 准确性 | ★★★ 中等 | ★★★★★ 精确 |
| 词典依赖 | 无需词典 | 需要完整词形词典 |
| 结果 | 可能是非词 | 一定是真实词 |
| 需要词性 | 不需要 | 通常需要 |

**具体对比：**
```
词根提取 (Stemming):
  "better" → "better"       ← 未处理！
  "running" → "run"
  "am" → "am"               ← 未处理！

词形还原 (Lemmatization):
  "better" → "good"         ← 形容词比较级 → 原级
  "running" → "run"
  "am/is/are/was/were" → "be"  ← 动词屈折形式 → 原形
  "geese" → "goose"         ← 不规则复数 → 单数
```

### 7.2 WordNet Lemmatizer 实现原理

```python
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

lemmatizer = WordNetLemmatizer()

# 词性标签: n=名词, v=动词, a=形容词, r=副词
examples = [
    ("running", "v"),    # 动词
    ("better", "a"),     # 形容词
    ("geese", "n"),      # 名词
    ("worse", "a"),      # 形容词
    ("went", "v"),       # 动词（不规则过去式）
]

for word, pos in examples:
    lemma = lemmatizer.lemmatize(word, pos)
    print(f"{word:15s} ({pos}) → {lemma}")

# running         (v) → run
# better          (a) → good
# geese           (n) → goose
# worse           (a) → bad
# went            (v) → go
```

### 7.3 搜索引擎中的选择

**推荐策略：**
- **英文搜索引擎：** 词干提取（速度优先）+ 少量词形还原规则
- **问答系统/语义搜索：** 词形还原（准确性优先）
- **中文搜索引擎：** 词形变化少，主要依赖分词质量

---

## 8. 同义词扩展（Synonym Expansion）

### 8.1 索引时扩展 vs 查询时扩展

```
索引时扩展:
  文档: "I bought an automobile"
  扩展: automobile → {automobile, car, vehicle}
  索引: {automobile: [d1], car: [d1], vehicle: [d1]}
  优点: 查询 "car" 可以命中 d1
  缺点: 索引膨胀，准确性降低

查询时扩展:
  查询: "car"
  扩展: car → {car, automobile, vehicle}
  查询: automobile OR car OR vehicle
  优点: 索引不变，灵活控制
  缺点: 查询变慢，可能引入噪声
```

### 8.2 同义词来源

```
1. WordNet（英文本体词典）
   car → {automobile, auto, motorcar}

2. 人工构建的同义词词典（领域专用）
   ML, Machine Learning, 机器学习, 深度学习（上位词）

3. 词嵌入相似词（Word2Vec / GloVe）
   king → {queen, monarch, prince} (cosine > 0.7)

4. 搜索日志挖掘
   用户搜索 "cellphone" 后又搜 "mobile phone" → 同义词

5. 点击共现挖掘
   两个查询点击同一文档集合 → 候选同义词
```

---

## 9. 完整预处理代码实现

```python
import re
import unicodedata
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class TextAnalyzerConfig:
    """文本分析器配置"""
    lowercase: bool = True
    remove_punctuation: bool = True
    remove_numbers: bool = False
    stop_words: set = field(default_factory=set)
    stemmer: Optional[str] = "porter"    # None, "porter", "snowball"
    use_lemmatization: bool = False
    min_token_length: int = 2
    max_token_length: int = 50
    ngram_range: tuple = (1, 1)          # (min_n, max_n)

class TextAnalyzer:
    """
    完整的文本预处理分析器
    实现搜索引擎标准分析流水线
    """
    
    def __init__(self, config: TextAnalyzerConfig):
        self.config = config
        self._init_components()
    
    def _init_components(self):
        """初始化各处理组件"""
        # 词干提取器
        if self.config.stemmer == "porter":
            from nltk.stem import PorterStemmer
            self.stemmer = PorterStemmer()
        elif self.config.stemmer == "snowball":
            from nltk.stem import SnowballStemmer
            self.stemmer = SnowballStemmer("english")
        else:
            self.stemmer = None
        
        # 词形还原器
        if self.config.use_lemmatization:
            from nltk.stem import WordNetLemmatizer
            self.lemmatizer = WordNetLemmatizer()
        
        # 编译正则表达式（提前编译提升性能）
        self.punct_pattern = re.compile(r'[^\w\s]')
        self.number_pattern = re.compile(r'\b\d+\b')
        self.whitespace_pattern = re.compile(r'\s+')
    
    def normalize_unicode(self, text: str) -> str:
        """Unicode 归一化：全角→半角，分解组合字符"""
        # NFC: 预组合形式（常用）
        # NFD: 分解形式
        # NFKC: 兼容预组合（全角→半角）
        text = unicodedata.normalize('NFKC', text)
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """基础分词：按非字母数字字符分割"""
        # 处理连字符: state-of-the-art → state of the art
        text = text.replace('-', ' ')
        # 按空白分割
        tokens = self.whitespace_pattern.split(text.strip())
        # 清理每个 token 的边界标点
        tokens = [re.sub(r'^[^\w]+|[^\w]+$', '', t) for t in tokens]
        return [t for t in tokens if t]
    
    def remove_stop_words(self, tokens: List[str]) -> List[str]:
        """停用词过滤"""
        return [t for t in tokens if t not in self.config.stop_words]
    
    def apply_stemming(self, tokens: List[str]) -> List[str]:
        """词干提取"""
        if self.stemmer is None:
            return tokens
        return [self.stemmer.stem(t) for t in tokens]
    
    def filter_by_length(self, tokens: List[str]) -> List[str]:
        """按长度过滤词条"""
        return [
            t for t in tokens
            if self.config.min_token_length <= len(t) <= self.config.max_token_length
        ]
    
    def generate_ngrams(self, tokens: List[str]) -> List[str]:
        """生成 N-gram 词条"""
        min_n, max_n = self.config.ngram_range
        result = []
        for n in range(min_n, max_n + 1):
            for i in range(len(tokens) - n + 1):
                ngram = '_'.join(tokens[i:i+n])
                result.append(ngram)
        return result
    
    def analyze(self, text: str) -> List[str]:
        """
        完整分析流水线
        返回: 处理后的词条列表
        """
        # Step 1: Unicode 归一化
        text = self.normalize_unicode(text)
        
        # Step 2: 大小写归一化
        if self.config.lowercase:
            text = text.lower()
        
        # Step 3: 移除标点
        if self.config.remove_punctuation:
            text = self.punct_pattern.sub(' ', text)
        
        # Step 4: 移除数字
        if self.config.remove_numbers:
            text = self.number_pattern.sub(' ', text)
        
        # Step 5: 分词
        tokens = self.tokenize(text)
        
        # Step 6: 停用词过滤
        if self.config.stop_words:
            tokens = self.remove_stop_words(tokens)
        
        # Step 7: 词干提取 或 词形还原
        if self.config.use_lemmatization:
            tokens = [self.lemmatizer.lemmatize(t) for t in tokens]
        else:
            tokens = self.apply_stemming(tokens)
        
        # Step 8: 长度过滤
        tokens = self.filter_by_length(tokens)
        
        # Step 9: N-gram 生成
        if self.config.ngram_range != (1, 1):
            tokens = self.generate_ngrams(tokens)
        
        return tokens


# 使用示例
if __name__ == "__main__":
    import nltk
    # 加载英文停用词
    stop_words = set(nltk.corpus.stopwords.words('english'))
    
    config = TextAnalyzerConfig(
        lowercase=True,
        remove_punctuation=True,
        stop_words=stop_words,
        stemmer="porter",
        min_token_length=2,
    )
    
    analyzer = TextAnalyzer(config)
    
    text = "The QUICK Brown FOX Jumped over the Lazy Dogs!!!"
    result = analyzer.analyze(text)
    print(result)
    # → ['quick', 'brown', 'fox', 'jump', 'lazi', 'dog']
```

---

## 10. 性能优化技巧

### 10.1 批量处理
```python
# 避免每次创建新对象，重用已编译的正则
pattern = re.compile(r'[^\w\s]')  # 编译一次，使用多次

# 批量处理优于逐条处理
def analyze_batch(texts: List[str]) -> List[List[str]]:
    return [analyzer.analyze(t) for t in texts]  # 可进一步并行化
```

### 10.2 缓存常见词条
```python
from functools import lru_cache

@lru_cache(maxsize=100000)
def stem_cached(word: str) -> str:
    return stemmer.stem(word)  # 相同词只计算一次
```

### 10.3 并行处理
```python
from multiprocessing import Pool

def parallel_analyze(texts: List[str], n_workers: int = 4) -> List[List[str]]:
    with Pool(n_workers) as p:
        return p.map(analyzer.analyze, texts)
```

---

*© 传统搜索引擎深度解析系列 — 第 2 篇 / 8*
