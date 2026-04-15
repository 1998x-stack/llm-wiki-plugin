# Hartley (1928): Transmission of Information

## 论文基本信息

| 项目 | 内容 |
|------|------|
| **标题** | Transmission of Information |
| **作者** | Ralph Vinton Lyon Hartley (1888–1970) |
| **发表** | Bell System Technical Journal, Vol. 7, No. 3, pp. 535–563, July 1928 |
| **机构** | Bell Telephone Laboratories |
| **领域** | 通信理论 / 信息度量 |

---

## 研究背景

### 时代语境

1920 年代是电信工业高速发展的时期。无线电广播刚刚兴起（1920 年代初期第一批商业广播电台），跨大西洋电话电缆在规划中，电报网络覆盖全球。Bell 系统（AT&T 和贝尔实验室）是当时世界上最大的通信企业，其工程师们面临一个根本性的实际问题：**如何量化一个通信系统传输"信息"的能力？**

在 Hartley 之前，Harry Nyquist (1924) 已经在"Certain Factors Affecting Telegraph Speed"中分析了电报传输速度的物理限制，指出带宽为 W 的信道每秒最多传输 2W 个独立脉冲，并提到信息量与 log m 成正比（m 为信号电平数）。但 Nyquist 的分析主要面向工程实践，缺乏对"信息"概念本身的系统思考。

### 核心挑战

"信息"在 1928 年之前是一个日常词汇，每个人都觉得自己理解它，但没有人能给出精确的数学定义。工程师们在讨论通信系统容量时，混淆了多个不同层面的问题：

1. **物理层面**：信道能传输多少个不同的信号？
2. **语义层面**：消息"包含"了多少"意思"？
3. **实用层面**：接收者从消息中"获取"了多少"有用"的内容？

这三个层面的混淆导致了概念上的混乱，使得建立通信系统的统一度量变得不可能。

---

## 试图解决的问题

Hartley 的论文直接面对一个看似简单却深刻的问题：

> **能否建立一个客观的、与人类主观判断无关的信息度量？**

具体而言，他需要回答：
1. "信息"应该如何数学化定义？
2. 这个定义应该满足什么性质？
3. 如何用这个定义来比较不同通信系统的传输能力？

---

## 核心思想

### 1. 信息与语义的分离——最关键的认识论突破

Hartley 最深刻的贡献不在于具体的公式，而在于一个认识论层面的决断：**信息度量必须与消息的"意义"分离。**

他在论文中明确指出：

> "In any given communication the sender mentally selects a particular symbol and by some bodily motion, as of his vocal mechanism, causes the attention of the receiver to be directed to that particular symbol. By this process a certain amount of information is said to have been transmitted... The word 'information' is used here in a special sense... the information is measured by the logarithm of the number of available choices."

这一决定的深刻性在于它的反直觉：在日常理解中，"A 股今天涨了 5%"比"今天是星期三"包含更多"信息"，因为前者更"有用"。但 Hartley 认为，"有用性"是主观的、因人而异的、无法客观度量的。他选择了一个完全客观的标准：**信息量取决于发送者在多少个可能的消息中做出了选择。**

这一思路的正确性直到 Shannon (1948) 才被完全验证——Shannon 的信息熵本质上是 Hartley 度量的概率化推广。

### 2. 对数度量的必然性

Hartley 论证了为什么信息量应该用对数来度量，而不是直接用可选消息的数目。他的论证基于一个简单而有力的要求：**可加性**。

假设有两个独立的选择过程：第一个在 s₁ 个符号中选择，第二个在 s₂ 个符号中选择。总的选择数是 s₁ × s₂（乘积），但我们直觉上希望"两次选择的总信息量"等于两次选择的信息量之和。唯一满足这一性质的函数是对数：

**H = log(s₁ × s₂) = log s₁ + log s₂**

### 3. Hartley 信息量公式

对于一个使用 s 个不同符号、传输 n 个符号的通信系统，Hartley 定义信息量为：

**H = n · log s**

这里的底数可以任意选择（改变底数只是改变度量单位）。如果使用以 2 为底的对数，单位就是后来 Shannon 命名的"bit"——虽然 Hartley 并未使用这个名称。

### 4. 等概率假设的局限

Hartley 的度量隐含了一个重要假设：**所有符号被选择的概率相等。** 这在许多实际场景中显然不成立——英语中 'e' 出现的频率远高于 'z'，因此接收到 'z' 比接收到 'e' 应该传达更多信息。

正是这一局限性，为 Shannon (1948) 的概率化信息熵留下了空间。

---

## 关键公式及直觉解释

### Hartley 信息量

$$H = n \cdot \log s$$

**各符号含义**：
- H：信息量
- n：消息中的符号个数
- s：字母表大小（可用的不同符号数）
- log：对数（底数决定度量单位）

**直觉解释**：
- 如果你在 2 个选项中选择 1 个，信息量 = log 2 = 1（bit）
- 如果你在 4 个选项中选择 1 个，信息量 = log 4 = 2（bit）——等于做了 2 次二选一
- 如果你发送 10 个二进制符号，信息量 = 10 × log 2 = 10 bit
- 选择空间越大，一次选择传达的信息越多

**类比**：想象你在一个有 100 扇门的走廊中选择了一扇门。告诉别人"我选了第 37 号门"传达了 log₂ 100 ≈ 6.64 bit 的信息。如果走廊只有 2 扇门，"我选了左边"只传达了 1 bit。

### 与 Shannon 熵的关系

Shannon 信息熵：

$$H(X) = -\sum_{i=1}^{s} p_i \log p_i$$

当所有符号等概率（p_i = 1/s）时：

$$H(X) = -\sum_{i=1}^{s} \frac{1}{s} \log \frac{1}{s} = -s \cdot \frac{1}{s} \cdot \log \frac{1}{s} = \log s$$

这恰好就是 Hartley 的单符号信息量！因此 **Hartley 度量是 Shannon 熵在均匀分布下的特殊情况。**

---

## 理论贡献

### 1. 开创性的概念框架

Hartley 建立了信息度量的基本原则：
- **客观性**：信息量不依赖于人类对消息的主观解读
- **可加性**：独立消息的信息量可以相加
- **对数性**：信息量与可选消息数目的对数成正比

这些原则后来被 Shannon 完全继承，并在更一般的概率框架下重新推导。

### 2. "Hartley"度量单位

国际单位制中，当使用以 10 为底的对数时，信息量的单位被命名为"Hartley"（也称为 ban 或 dit）。1 Hartley = log₂ 10 ≈ 3.322 bit。虽然在实践中 bit（以 2 为底）更常用，但这一命名体现了对 Hartley 贡献的认可。

### 3. 工程方法论的范式

Hartley 展示了一种将模糊的工程概念转化为精确数学量的方法论，为整个通信工程学科的数学化奠定了范式。

---

## 历史影响

### 直接影响

1. **Shannon (1948)** 在"A Mathematical Theory of Communication"的开篇就引用了 Hartley 的工作，明确指出自己的理论是 Hartley 框架的概率化推广。

2. **Nyquist-Hartley-Shannon 链条**：三人的工作构成了一条清晰的思想链：Nyquist (1924) 分析了带宽与传输速率的关系 → Hartley (1928) 定义了信息量 → Shannon (1948, 1949) 统一了信息、噪声和信道容量。

### 间接影响

1. **信息与语义分离**的原则影响了 20 世纪的科学哲学，尤其是逻辑实证主义对"意义"的讨论。

2. Hartley 的论文启发了后来一系列将物理概念数学化的尝试——从 Fisher 信息量到量子信息论。

### 被忽视的方面

Hartley 的论文有一部分经常被忽视：他讨论了连续信号的信息度量问题，指出连续情况下可选项数目变为无穷，直接导致信息量趋于无穷。他正确地意识到这是一个根本性困难，但未能解决它。这个问题直到 Shannon 引入微分熵和信道容量概念后才得到解决。

---

## 现代视角

### 重新评价

从现代视角看，Hartley 1928 年的论文有以下几点值得重新评价：

1. **概念贡献超过技术贡献**：Hartley 的对数公式在技术上很简单，但其真正价值在于概念框架——将"信息"从日常语言提升为可度量的物理量。这一步的难度和重要性往往被低估。

2. **等概率假设的合理性**：在许多工程场景中（如加密后的数据流），等概率假设实际上是合理的。Hartley 度量并非"不正确"，只是不够一般。

3. **与 Rényi 熵的关系**：Hartley 熵等价于 Rényi 熵在 α = 0 时的取值，度量的是"支撑集的大小"。在密码学和安全性分析中，这一度量仍然有独立价值。

### 教学意义

Hartley 的论文是理解信息论的最佳入门点之一，因为它的推理完全不需要概率论知识，只需要基本的对数性质。它清晰地展示了"为什么要用对数"这一教学中最常见的问题的答案。

---

## 科普总结

想象你在给远方的朋友传达一条消息。你面前有一组可以选择的符号——可能是 26 个英文字母，可能是 10 个数字，也可能就是 0 和 1 两个二进制位。

Hartley 问了一个看似简单的问题：**你每选择一个符号，"传达"了多少"信息"？**

他的回答出人意料地优雅：信息量等于可选项数目的对数。如果你在 2 个选项中选择 1 个，传达了 1 bit 信息；在 4 个选项中选择 1 个，传达了 2 bit；在 1000 个选项中选择 1 个，大约传达了 10 bit。

为什么用对数而不是直接用选项数目？因为两次独立选择的信息应该"加起来"——如果你先在 4 个选项中选择（2 bit），再在 8 个选项中选择（3 bit），总共传达了 5 bit 信息。如果用选项数目（4 × 8 = 32），就需要乘法而不是加法，这在工程中很不方便。

Hartley 的另一个关键洞见是：**信息与"意义"无关。** 无论你选择的符号表达的是今天的天气还是随机的噪声，只要选择空间一样大，传达的信息量就一样多。

这一看似"无情"的定义，恰恰是使信息论成为普适科学的关键。正因为不关心"意义"，信息论才能同时应用于电话、电视、互联网、DNA 序列和黑洞物理。

Hartley 的工作是一扇门的开启。二十年后，Shannon 推开了整面墙。

---

## 参考资料

1. Hartley, R. V. L. (1928). "Transmission of Information." *Bell System Technical Journal*, 7(3), 535–563.
2. Nyquist, H. (1924). "Certain Factors Affecting Telegraph Speed." *Bell System Technical Journal*, 3(2), 324–346.
3. Shannon, C. E. (1948). "A Mathematical Theory of Communication." *Bell System Technical Journal*, 27(3), 379–423; 27(4), 623–656.
4. Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley-Interscience. Chapter 1.
5. Pierce, J. R. (1980). *An Introduction to Information Theory: Symbols, Signals and Noise* (2nd ed.). Dover Publications.
