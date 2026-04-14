# Strassen 快速矩阵乘法：打破 O(n^3) 的思维定式

## 1. 标题

**"Gaussian Elimination is Not Optimal"**
（高斯消元法不是最优的）

## 2. 作者/作者群

**Volker Strassen (1936--2022)**。

Volker Strassen 是德国数学家，先后任教于多所欧洲大学，最终在德国康斯坦茨大学（Universitat Konstanz）和瑞士苏黎世大学（Universitat Zurich）担任教授。他是代数复杂性理论（algebraic complexity theory）和概率算法（probabilistic algorithms）领域的开拓者之一。

Strassen 的学术兴趣极为广泛，横跨纯数学与理论计算机科学。除了快速矩阵乘法之外，他还在以下领域做出了重要贡献：

- **Strassen 大整数乘法算法**（1971年）：与 Arnold Schonhage 合作提出了 Schonhage-Strassen 算法，将大整数乘法的复杂度降低到 $O(n \log n \log \log n)$
- **概率素性检验**（1977年）：与 Robert Solovay 合作提出了 Solovay-Strassen 素性检验算法，这是最早的概率算法之一
- **代数复杂性理论**：为研究代数计算的内在复杂度建立了理论框架

Strassen 于2003年获得了 Cantor 奖章（Georg Cantor Medal），于2008年获得了 Knuth 奖（Donald E. Knuth Prize）——计算机科学领域的重要荣誉，表彰其对算法理论的杰出贡献。

## 3. 发表时间

**1969年**，发表于 *Numerische Mathematik*，第13卷，第4期，第354--356页。

这篇论文极为简短——仅有3页。然而，其影响力与篇幅之间的反差堪称惊人。这3页纸不仅改变了矩阵计算领域，还催生了一个全新的数学分支——代数复杂性理论。

## 4. 发表载体/文献背景

*Numerische Mathematik* 是由 Springer 出版的国际数值数学期刊，创刊于1959年，由数值分析领域的多位领军人物共同创办。该期刊是数值分析和计算数学领域最负盛名的学术出版物之一。

1960年代末期，计算机科学正在经历一个重要的理论转型期。一方面，算法复杂性理论正在被 Hartmanis、Stearns、Blum、Cook 等人系统地建立起来；另一方面，数值分析作为一门实用学科，主要关注的是算法的数值稳定性和实际效率，对计算复杂度的理论下界关注较少。

在这个背景下，矩阵乘法是一个被普遍认为"已经解决"的问题。两个 $n \times n$ 矩阵的乘法需要 $n^3$ 次乘法和 $n^2(n-1)$ 次加法——这是根据矩阵乘法的定义直接得到的。几乎所有人都认为这是不可改进的：$n^3$ 就是矩阵乘法的内在复杂度。Strassen 的论文彻底颠覆了这一认知。

## 5. 一句话总结

Strassen 发现了一种巧妙的方法，用7次乘法（而非通常的8次）完成 $2 \times 2$ 矩阵的乘法，并通过递归应用这一技巧，将 $n \times n$ 矩阵乘法的复杂度从 $O(n^3)$ 降低到 $O(n^{\log_2 7}) \approx O(n^{2.807})$，首次证明了矩阵乘法的"显然"复杂度 $O(n^3)$ 并非最优。

## 6. 历史背景

### 矩阵乘法的基本定义

矩阵乘法是线性代数中最基本的运算之一。给定两个 $n \times n$ 矩阵 $A = (a_{ij})$ 和 $B = (b_{ij})$，它们的乘积 $C = AB$ 定义为：

$$c_{ij} = \sum_{k=1}^{n} a_{ik} b_{kj}$$

按照这个定义，计算 $C$ 的每个元素需要 $n$ 次乘法和 $n-1$ 次加法；总共 $n^2$ 个元素需要 $n^3$ 次乘法和 $n^2(n-1)$ 次加法。

### 矩阵乘法的普遍性

矩阵乘法几乎出现在所有科学和工程计算中：

- **线性方程组求解**：高斯消元法的核心操作本质上是矩阵乘法
- **线性代数分解**（LU、QR、SVD 等）：都涉及大量矩阵乘法
- **图论**：邻接矩阵的幂次方可以计算图中的路径数
- **动态规划**：许多动态规划问题可以表示为矩阵乘法
- **多项式乘法**：两个多项式的乘法等价于一种特殊矩阵（Toeplitz 矩阵）的乘法

由于矩阵乘法的无处不在，任何对其效率的改进都会对计算科学产生广泛的连锁影响。

### "O(n^3) 是最优的"——一个普遍的错觉

在 Strassen 之前，几乎没有人认真思考过矩阵乘法是否可以在少于 $n^3$ 次乘法的情况下完成。这种思维定式有一个看似合理的理由：矩阵乘法的定义本身就包含 $n^3$ 项——每个 $c_{ij}$ 是 $n$ 个乘积项之和，共有 $n^2$ 个 $c_{ij}$。要减少乘法次数，似乎需要跳过某些必要的计算，而这显然会导致结果不正确。

然而，Strassen 的洞察力在于认识到：虽然不能跳过任何必要的信息，但可以通过巧妙地重组计算，让某些乘法的结果被多次重复利用，从而减少总的乘法次数——代价是增加一些加法运算。由于在大多数计算模型中，加法比乘法更"廉价"，这种权衡是有利的。

### 2x2 矩阵乘法的常规方法

考虑两个 $2 \times 2$ 矩阵的乘法：

$$\begin{pmatrix} c_{11} & c_{12} \\ c_{21} & c_{22} \end{pmatrix} = \begin{pmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{pmatrix} \begin{pmatrix} b_{11} & b_{12} \\ b_{21} & b_{22} \end{pmatrix}$$

按定义计算需要8次乘法和4次加法：

$$c_{11} = a_{11}b_{11} + a_{12}b_{21}$$
$$c_{12} = a_{11}b_{12} + a_{12}b_{22}$$
$$c_{21} = a_{21}b_{11} + a_{22}b_{21}$$
$$c_{22} = a_{21}b_{12} + a_{22}b_{22}$$

问题是：能否用少于8次乘法来完成这个计算？

## 7. 核心问题定义

**核心问题**：$n \times n$ 矩阵乘法的最低计算复杂度是什么？特别是，能否突破 $O(n^3)$ 的"自然"复杂度？

更精确地说，令 $\omega$ 表示矩阵乘法指数（matrix multiplication exponent）——即矩阵乘法可以在 $O(n^\omega)$ 次算术运算内完成的最小 $\omega$ 值。显然 $\omega \geq 2$（因为至少需要读取 $2n^2$ 个输入元素和写入 $n^2$ 个输出元素）。问题是：$\omega = 3$（如常规算法所示），还是 $\omega$ 可以更小？

Strassen 的论文给出了确定的答案：$\omega < 3$。

## 8. 主要结论/方法/定理

### Strassen 的7次乘法技巧

Strassen 发现，$2 \times 2$ 矩阵乘法可以只用7次乘法来完成（但需要更多的加法和减法）。他定义了以下7个辅助乘积：

$$m_1 = (a_{11} + a_{22})(b_{11} + b_{22})$$
$$m_2 = (a_{21} + a_{22}) \cdot b_{11}$$
$$m_3 = a_{11} \cdot (b_{12} - b_{22})$$
$$m_4 = a_{22} \cdot (b_{21} - b_{11})$$
$$m_5 = (a_{11} + a_{12}) \cdot b_{22}$$
$$m_6 = (a_{21} - a_{11})(b_{11} + b_{12})$$
$$m_7 = (a_{12} - a_{22})(b_{21} + b_{22})$$

然后，乘积矩阵的元素可以表示为：

$$c_{11} = m_1 + m_4 - m_5 + m_7$$
$$c_{12} = m_3 + m_5$$
$$c_{21} = m_2 + m_4$$
$$c_{22} = m_1 - m_2 + m_3 + m_6$$

可以直接验证这些公式的正确性（虽然验证过程需要一些耐心的代数展开）。

关键的一点是：这里只用了7次乘法（$m_1$ 到 $m_7$），而非常规方法的8次。代价是加法和减法的次数从4次增加到了18次。

### 递归应用：分块矩阵

Strassen 的真正力量在于将这一技巧递归应用于大矩阵。对于 $n \times n$ 矩阵（$n = 2^k$），将其分成 $2 \times 2$ 的分块矩阵，每个"块"是一个 $n/2 \times n/2$ 的子矩阵。然后用上述7次乘法公式——只不过现在 $a_{ij}$、$b_{ij}$、$m_i$ 都是矩阵而非标量。

递推关系为：

$$T(n) = 7 \cdot T(n/2) + O(n^2)$$

其中 $O(n^2)$ 项来自矩阵加法和减法。根据主定理，解为：

$$T(n) = O(n^{\log_2 7}) = O(n^{2.807...})$$

### 复杂度的改进

对比：
- 常规算法：$O(n^3) = O(n^{3.000})$
- Strassen 算法：$O(n^{2.807})$

虽然从指数上看改进不大（3.000 降到 2.807），但对于大矩阵来说，差异是显著的：

| 矩阵规模 n | $n^3$ | $n^{2.807}$ | 加速比 |
|-----------|-------|-------------|--------|
| 100 | $10^6$ | $4.1 \times 10^5$ | 2.4x |
| 1000 | $10^9$ | $2.5 \times 10^8$ | 4.0x |
| 10000 | $10^{12}$ | $6.5 \times 10^{10}$ | 15.4x |

### 论文标题的深意

论文的标题 "Gaussian Elimination is Not Optimal" 远不止是一个关于高斯消元法的陈述。Strassen 证明了矩阵乘法可以在亚立方时间内完成，而高斯消元法（以及 LU 分解等基于矩阵乘法的操作）的复杂度也相应地可以降低。更深层的含义是：即使是最"自然"、最"显而易见"的算法，也可能不是最优的——这对整个算法设计领域都是一个深刻的提醒。

## 9. 核心思想的直觉解释

### 乘法与加法的权衡

Strassen 算法的核心直觉是一种**权衡**（trade-off）：用更多的加法来换取更少的乘法。

在通常的理解中，乘法和加法似乎同样"基本"。但从复杂性理论的角度看，它们是不同的：乘法是"非线性"操作，具有更高的代数复杂度；加法是"线性"操作，在某种意义上更为"廉价"。

Strassen 的技巧本质上是：通过巧妙地组合输入元素（用加法），构造出更"有信息量"的中间量，使得7次乘法就足以提取出结果矩阵的所有4个元素所需的信息。

### 一个更简单的类比

考虑一个更简单的例子来说明同样的思想。假设你需要计算 $z_1 = (a+b)(c+d)$ 和 $z_2 = (a+b)(c-d)$。

直接计算需要2次乘法。但如果你先计算 $s = a + b$，然后计算 $p = s \cdot c$ 和 $q = s \cdot d$，那么 $z_1 = p + q$，$z_2 = p - q$——仍然是2次乘法。这里没有节省。

但考虑计算 $ac$ 和 $bd$。常规方法需要2次乘法。现在考虑：

$$m_1 = (a+b)(c+d) = ac + ad + bc + bd$$
$$m_2 = ac$$
$$m_3 = bd$$

从 $m_2$ 和 $m_3$ 可以直接得到 $ac$ 和 $bd$（2次乘法）。但如果你还需要 $ad + bc$，那么 $m_1 - m_2 - m_3 = ad + bc$——只需要3次乘法就得到了 $ac$、$bd$ 和 $ad + bc$，而常规方法需要4次乘法。这就是 Karatsuba 乘法（1962年）的核心思想——也是 Strassen 在矩阵乘法中使用的同类技巧的前身。

### 为什么是7而不是更少

自然的问题是：$2 \times 2$ 矩阵乘法能否用6次或更少的乘法完成？

1971年，Hopcroft 和 Kerr 证明了：在非交换的情况下（矩阵乘法是非交换的），$2 \times 2$ 矩阵乘法至少需要7次乘法。因此，Strassen 的7次乘法是最优的——至少对于 $2 \times 2$ 的情况而言。

## 10. 为什么这篇文献重要

### 打破了一个根深蒂固的认知

Strassen 的结果之所以如此震撼，是因为它推翻了一个被普遍接受了几十年甚至上百年的"常识"。几乎所有的数学家和计算机科学家都认为矩阵乘法需要 $O(n^3)$ 次运算——这不是一个有争议的猜想，而是一个被认为"显而易见"的事实。

Strassen 证明了这个"事实"是错误的。这不仅仅是一个技术上的改进，更是一次认知上的革命：它提醒整个科学界，"显而易见"的算法不一定是最优的，任何关于计算复杂度下界的断言都需要严格的证明。

### 催生了代数复杂性理论

Strassen 的工作直接推动了代数复杂性理论（algebraic complexity theory）的发展。这一分支专门研究代数计算问题的内在复杂度——例如，执行某种代数运算最少需要多少次基本操作？这个方向产生了大量深刻的数学结果和未解问题。

### 开启了 omega 猜想的追求

Strassen 将矩阵乘法指数 $\omega$ 的上界从3降低到了 $\log_2 7 \approx 2.807$。此后，改进 $\omega$ 的上界成为了理论计算机科学中最引人注目的研究方向之一：

| 年份 | 研究者 | $\omega$ 上界 |
|------|--------|--------------|
| 常规 | -- | 3.000 |
| 1969 | Strassen | 2.807 |
| 1978 | Pan | 2.796 |
| 1979 | Bini et al. | 2.780 |
| 1981 | Schonhage | 2.548 |
| 1986 | Strassen | 2.479 |
| 1990 | Coppersmith & Winograd | 2.376 |
| 2012 | Williams | 2.3729 |
| 2014 | Le Gall | 2.3728 |
| 2024 | Duan, Wu, Zhou | 2.371339 |

最终目标是确定 $\omega = 2$ 是否可能——即矩阵乘法是否可以在（本质上）二次时间内完成。这仍然是理论计算机科学中最重要的开放问题之一。

### 深远的哲学影响

Strassen 的结果对计算科学的思维方式产生了深远影响。它教导我们：

- 不要因为某个算法看起来"自然"就认为它是最优的
- 计算的本质可能比我们直觉认为的更加微妙
- 即使是最基本的计算问题，也可能隐藏着意想不到的结构

## 11. 它解决了当时什么瓶颈

### 理论层面

Strassen 的主要贡献是理论性的：他证明了矩阵乘法的代数复杂度严格小于 $n^3$。这不是一个"工程优化"，而是一个关于计算本质的数学发现。

在此之前，没有人能够证明矩阵乘法的复杂度下界大于 $O(n^2)$（显然需要至少读取所有输入元素），也没有人能给出小于 $O(n^3)$ 的上界。Strassen 通过构造性地给出一个亚立方算法，明确地缩小了这个差距。

### 实际层面

虽然 Strassen 算法的理论意义大于实践意义，但它确实在某些场景下具有实际价值：

- 对于足够大的矩阵（通常 $n > 100$ 到 $n > 1000$，取决于硬件），Strassen 算法确实比常规算法更快
- 在某些科学计算和工程应用中，矩阵乘法是性能瓶颈，即使是中等幅度的加速也有显著的实际价值

### 连锁效应

由于矩阵乘法是许多其他算法的子程序，Strassen 的结果意味着这些算法的复杂度也可以相应降低：

- **矩阵求逆**：$O(n^\omega)$（与矩阵乘法同阶）
- **行列式计算**：$O(n^\omega)$
- **LU 分解**：$O(n^\omega)$
- **线性方程组求解**：$O(n^\omega)$

## 12. 它与前人工作的关系

### 与 Karatsuba 的关系

1962年，Anatoly Karatsuba 发现了大整数乘法的一种类似技巧：将两个 $n$ 位整数的乘法从 $O(n^2)$ 降低到 $O(n^{\log_2 3}) \approx O(n^{1.585})$。Karatsuba 的核心思想与 Strassen 的完全类似——通过巧妙的加减法组合，将3次"小"乘法代替原来需要的4次。

Strassen 算法可以被看作是 Karatsuba 思想在矩阵乘法领域的推广。但矩阵乘法的非交换性（$AB \neq BA$）使得问题更加复杂，Strassen 的发现也因此更加令人印象深刻。

### 与 Winograd 的关系

Shmuel Winograd 在1960年代末和1970年代初对矩阵乘法的代数复杂度进行了深入研究。他证明了 $2 \times 2$ 矩阵乘法在交换环上至少需要7次乘法，从而证明了 Strassen 的算法在 $2 \times 2$ 情况下是最优的。

Winograd 还提出了 Strassen 算法的一个变体，将加法次数从18次减少到15次（仍然是7次乘法），使得算法在实际中更为高效。

### 与经典矩阵理论的关系

Strassen 的工作与经典矩阵分析（如 Gauss、Cayley 等人的工作）形成了有趣的对比。经典理论关注矩阵运算的数学性质（如行列式、特征值、范数），而 Strassen 关注的是计算这些运算所需的最少操作数——一个本质上不同的问题。

### 与计算复杂性理论的关系

Strassen 的工作与当时正在蓬勃发展的计算复杂性理论有深刻的联系。1960年代，Hartmanis 和 Stearns 建立了时间复杂度的基本理论，Cook 和 Karp 即将提出 P 与 NP 问题。Strassen 的矩阵乘法结果可以被视为代数复杂性——复杂性理论的一个重要分支——的奠基性成果。

## 13. 它对后续哪些方向产生了影响

### $\omega$ 猜想的追求

如前所述，改进矩阵乘法指数 $\omega$ 的上界成为了理论计算机科学中持续半个世纪的重要研究方向。

1979年，Bini 等人引入了"近似秩"（border rank / approximate rank）的概念，利用"退化"（degeneration）技术进一步降低了 $\omega$ 的上界。

1986年，Strassen 本人提出了"激光方法"（laser method），这是一种基于张量分解的系统化技术，用于构造快速矩阵乘法算法。

1990年，Don Coppersmith 和 Shmuel Winograd 使用改进的激光方法将 $\omega$ 的上界降低到约2.376——这个界保持了超过20年。

2012年，Virginia Vassilevska Williams 使用新的组合技术将上界微小地改进到约2.3729。此后，Alman、Williams、Le Gall 以及 Duan、Wu、Zhou 等研究者继续推动着上界的逐步下降。

然而，$\omega = 2$ 是否可达仍然是一个开放问题。许多研究者猜测 $\omega = 2$，但也有人持怀疑态度。

### 代数复杂性理论

Strassen 的工作催生了代数复杂性理论这一数学分支。该理论研究的核心问题包括：

- **双线性映射的复杂度**：矩阵乘法是一种双线性映射（bilinear map），其复杂度等价于某个张量（tensor）的秩。张量秩的计算和估计成为了一个核心的研究主题。
- **电路复杂度**：代数电路（arithmetic circuit）可以计算多项式函数。给定一个多项式，最小的电路规模是多少？
- **P vs VP 问题**：代数版本的 P vs NP 问题，被认为是理论计算机科学中最深刻的开放问题之一。

### 张量分解

矩阵乘法可以用一个三阶张量来表示。Strassen 的发现表明，这个张量的秩（即分解为秩一张量之和所需的最少项数）小于8（实际上等于7）。这一观察推动了张量分解理论的发展，而张量分解在机器学习（如张量网络、CP分解）、量子信息和信号处理等领域有广泛应用。

### 实际实现与优化

虽然 Strassen 算法的渐近复杂度优于常规算法，但在实际实现中，其优势取决于矩阵规模和硬件特性。研究者们广泛研究了以下实际问题：

- **交叉点（crossover point）**：Strassen 算法在多大的矩阵规模下才比常规算法更快？这取决于硬件特性、缓存大小等因素，通常在 $n = 100$ 到 $n = 1000$ 之间。
- **数值稳定性**：Strassen 算法涉及大量的加减法操作，可能导致数值误差的累积。对于需要高精度的应用，这是一个需要考虑的因素。
- **缓存效率**：Strassen 算法的递归结构可以更好地利用现代处理器的缓存层次结构。
- **并行实现**：Strassen 算法的递归结构天然适合并行计算。

### GPU 和深度学习中的矩阵乘法

在深度学习时代，矩阵乘法（或更一般的张量运算）是神经网络训练和推理的核心计算。现代 GPU（如 NVIDIA 的 A100、H100）包含专用的矩阵乘法单元（Tensor Cores），针对特定规模的矩阵乘法进行了硬件级优化。

虽然 Tensor Cores 通常使用常规的 $O(n^3)$ 算法（因为对于 GPU 支持的较小矩阵块，常规算法更高效且更易于硬件实现），Strassen 的思想仍然在更高层面上影响着矩阵乘法的实现策略——例如，在多个 GPU 之间分配大规模矩阵乘法时。

### 通信复杂度

Strassen 类算法在分布式计算中还有一个重要优势：它们可以减少处理器之间的通信量。在现代高性能计算中，通信（数据传输）往往比计算更昂贵。Ballard 等人的研究（2012年）表明，Strassen 类算法不仅减少了算术运算数，还减少了通信量——这在分布式系统中是一个重要优势。

## 14. 今天回看它的价值

### 理论价值永存

Strassen 算法的最深远影响是理论性的：它证明了"显然最优"的算法可能不是最优的。这一教训在今天仍然具有指导意义——每当我们面对一个看似"已经解决"的计算问题时，都应该质问：真的不能做得更好吗？

### 实际应用的演变

在实际应用中，Strassen 算法的地位经历了有趣的演变：

- **1970--1980年代**：主要被视为理论成果，实际应用有限
- **1990--2000年代**：随着矩阵规模的增大和计算架构的变化，开始在某些高性能计算应用中被采用
- **2010年代至今**：在特定场景下（如大规模科学计算、某些机器学习训练任务）使用 Strassen 算法或其变体

值得注意的是，许多现代高性能数学库（如 Intel MKL、GotoBLAS/OpenBLAS）在内部对足够大的矩阵自动使用 Strassen 算法。

### 对新一代算法研究的启示

Strassen 的工作方法——通过巧妙的代数恒等式来减少基本运算次数——启发了许多后续的快速算法研究。例如：

- **快速多项式乘法**：基于 FFT 和 NTT 的 $O(n \log n)$ 算法
- **快速整数乘法**：从 Karatsuba 到 Schonhage-Strassen 到 Harvey-van der Hoeven 的一系列改进
- **快速图算法**：利用矩阵乘法加速图论中的基本算法（如传递闭包、最短路径、匹配等）

### $\omega = 2$ 猜想的现状

关于矩阵乘法指数 $\omega$ 是否等于2，至今仍是一个开放问题。2024年，Duan、Wu 和 Zhou 将上界改进到约 2.371339。然而，从 2.371 到 2.000 之间仍然有巨大的鸿沟，现有的技术（包括激光方法及其改进）似乎难以弥合这一差距。

一些研究者提出了"群论方法"（group-theoretic approach），试图通过利用有限群的表示论来构造快速矩阵乘法算法。Cohn 和 Umans（2003年）表明，如果存在具有某些特殊性质的有限群，那么 $\omega = 2$ 就是可达的。然而，这些特殊群是否存在仍然是一个未解的问题。

## 15. 面向普通读者的通俗解释

### 矩阵乘法是什么

你可以把矩阵想象成一个数字表格。两个矩阵"相乘"意味着按照一种特定的规则从两个表格中提取信息，生成一个新的表格。这种运算在科学、工程、经济学甚至社交网络分析中都极为常见。

### 为什么 Strassen 的发现令人震惊

想象你有一个固定的食谱，告诉你做一道菜需要8个鸡蛋。如果有人告诉你，通过巧妙地混合和分配这些鸡蛋，实际上只需要7个就能做出完全一样的菜——你可能会很惊讶。

Strassen 做了类似的事情，但在数学领域。他发现，通过巧妙地组合加法和减法，可以将 $2 \times 2$ 矩阵乘法所需的基本乘法运算从8次减少到7次。

这个发现之所以重要，不仅仅是因为节省了1次乘法，而是因为这个技巧可以反复使用——当你将大矩阵分成小块时，每一层都节省了 $1/8$ 的乘法。这些节省层层累积，对于大矩阵来说，最终可以节省可观的计算量。

### 这对你意味着什么

Strassen 的发现对我们日常使用的技术有间接但重要的影响。每当计算机进行大规模数据处理——从天气预报到视频游戏中的3D图形渲染——矩阵乘法都是核心计算之一。任何对矩阵乘法效率的改进都会让这些应用运行得更快。

更重要的是，Strassen 的故事告诉我们一个通用的教训：不要假设"显而易见的方法"就是最好的方法。在任何领域，都可能存在更聪明的解决方案——只要我们有足够的创造力去发现它。

## 16. 阅读原文建议

### 原始论文

Strassen 的原始论文仅有3页，语言简洁、数学符号紧凑。对于有基本线性代数背景的读者来说，论文本身是可以直接阅读的。

**阅读建议**：

1. **第一遍**：理解论文的主要结论——$2 \times 2$ 矩阵乘法可以用7次乘法完成

2. **第二遍**：手工验证7个辅助乘积 $m_1$ 到 $m_7$ 的正确性——将 $c_{11}$、$c_{12}$、$c_{21}$、$c_{22}$ 的表达式展开，确认它们确实等于标准矩阵乘法的结果

3. **第三遍**：理解递归的应用——为什么 $2 \times 2$ 的结果可以推广到 $n \times n$ 矩阵

### 预备知识

- **矩阵乘法**：理解矩阵乘法的定义
- **分块矩阵**：理解矩阵可以被分成"块"，块之间的乘法遵循与标量相同的规则（但要注意非交换性）
- **递归和分治**：理解如何通过递归地应用一个技巧来获得渐近复杂度的改进
- **主定理**：用于分析分治算法复杂度的基本工具

### 延伸阅读路线

1. 先阅读 Strassen 原始论文
2. 阅读 Cohn 和 Umans (2003) 的综述，了解 $\omega$ 猜想的现状
3. 阅读 Blaser (2013) 的教科书 *Fast Matrix Multiplication*，获得该领域的全面视角
4. 如果对代数复杂性理论感兴趣，可以继续阅读 Burgisser, Clausen, Shokrollahi (1997) 的 *Algebraic Complexity Theory*

## 17. 局限性/历史局限

### 数值稳定性问题

Strassen 算法的一个主要实际问题是数值稳定性。由于算法涉及大量的加减法操作，可能导致灾难性消去（catastrophic cancellation）——两个相近的大数相减产生严重的精度损失。

Higham 和 Demmel 等人的分析表明，Strassen 算法的数值误差界比常规算法更差。对于对精度要求很高的应用（如某些物理模拟），这可能是一个严重的限制。

### 实际效率的问题

1. **交叉点问题**：对于小矩阵，Strassen 算法的常数因子（主要来自额外的加减法和递归开销）使其比常规算法更慢。只有当矩阵足够大时，渐近复杂度的优势才能体现。

2. **内存开销**：递归实现需要额外的临时存储空间用于中间矩阵。虽然可以通过仔细的实现减少内存开销，但这增加了实现的复杂性。

3. **缓存不友好性**：朴素的递归实现可能导致频繁的缓存未命中。需要通过"缓存感知"（cache-aware）或"缓存遗忘"（cache-oblivious）的实现策略来缓解这一问题。

### 理论上更优但实际不可行的算法

后续的 $\omega$ 上界改进（如 Coppersmith-Winograd 算法及其后继者）虽然在渐近意义上优于 Strassen 算法，但它们的常数因子极大——大到在任何实际可见的矩阵规模下都无法胜过常规算法甚至 Strassen 算法。

这揭示了理论复杂度与实际效率之间的巨大鸿沟：一个渐近最优的算法不一定是实际最快的算法。

### 非方阵和结构化矩阵

Strassen 的原始算法针对的是方阵（$n \times n$）乘法。虽然可以推广到非方阵，但推广并不总是高效的。此外，对于具有特殊结构的矩阵（如稀疏矩阵、对称矩阵、Toeplitz 矩阵），利用结构特性的专用算法可能比 Strassen 算法更为高效。

### $\omega = 2$ 的可达性

虽然 $\omega = 2$ 是一个被广泛讨论的猜想，但也有论据暗示它可能是不可达的，或者即使可达，实现 $O(n^{2+\epsilon})$ 复杂度的算法可能需要天文数字般的常数因子，使其在实际中毫无用处。

## 18. 延伸阅读建议

### 教科书

1. **Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.**
   第4章和第28章分别讨论了分治算法和矩阵运算，包括 Strassen 算法。

2. **Burgisser, P., Clausen, M., & Shokrollahi, M. A. (1997). *Algebraic Complexity Theory*. Springer.**
   代数复杂性理论的全面教材，深入讨论了矩阵乘法复杂度。

3. **Blaser, M. (2013). *Fast Matrix Multiplication*. In *Theory of Computing*, Graduate Surveys 5.**
   对快速矩阵乘法领域的现代综述。

### 重要论文

4. **Karatsuba, A. A., & Ofman, Yu. (1962). "Multiplication of Many-Digital Numbers by Automatic Computers." *Doklady Akademii Nauk SSSR*, 145(2), 293--294.**
   Karatsuba 快速整数乘法算法——Strassen 思想的先驱。

5. **Coppersmith, D., & Winograd, S. (1990). "Matrix Multiplication via Arithmetic Progressions." *Journal of Symbolic Computation*, 9(3), 251--280.**
   长期保持 $\omega$ 最佳上界的经典论文。

6. **Williams, V. V. (2012). "Multiplying Matrices Faster than Coppersmith-Winograd." *Proceedings of the 44th ACM Symposium on Theory of Computing (STOC)*, 887--898.**
   打破 Coppersmith-Winograd 记录的重要工作。

7. **Cohn, H., & Umans, C. (2003). "A Group-Theoretic Approach to Matrix Multiplication." *Proceedings of the 44th Annual IEEE Symposium on Foundations of Computer Science (FOCS)*, 438--449.**
   提出了利用群论方法证明 $\omega = 2$ 的框架。

### 实际实现

8. **Higham, N. J. (1990). "Exploiting Fast Matrix Multiplication Within the Level 3 BLAS." *ACM Transactions on Mathematical Software*, 16(4), 352--368.**
   讨论了在实际数值库中使用 Strassen 算法的实现策略和数值稳定性。

9. **Huang, J., Smith, T. M., Henry, G. M., & van de Geijn, R. A. (2016). "Strassen's Algorithm Reloaded." *Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis (SC'16)*.**
   关于在现代高性能计算架构上实现 Strassen 算法的最新研究。

## 19. 参考资料/实际引用文档

1. Strassen, V. (1969). "Gaussian Elimination is Not Optimal." *Numerische Mathematik*, 13(4), 354--356.

2. Karatsuba, A. A., & Ofman, Yu. (1962). "Multiplication of Many-Digital Numbers by Automatic Computers." *Doklady Akademii Nauk SSSR*, 145(2), 293--294.

3. Winograd, S. (1971). "On Multiplication of 2 x 2 Matrices." *Linear Algebra and Its Applications*, 4(4), 381--388.

4. Hopcroft, J. E., & Kerr, L. R. (1971). "On Minimizing the Number of Multiplications Necessary for Matrix Multiplication." *SIAM Journal on Applied Mathematics*, 20(1), 30--36.

5. Coppersmith, D., & Winograd, S. (1990). "Matrix Multiplication via Arithmetic Progressions." *Journal of Symbolic Computation*, 9(3), 251--280.

6. Williams, V. V. (2012). "Multiplying Matrices Faster than Coppersmith-Winograd." *Proceedings of the 44th ACM Symposium on Theory of Computing (STOC)*, 887--898.

7. Le Gall, F. (2014). "Powers of Tensors and Fast Matrix Multiplication." *Proceedings of the 39th International Symposium on Symbolic and Algebraic Computation (ISSAC)*, 296--303.

8. Duan, R., Wu, H., & Zhou, R. (2024). "Faster Matrix Multiplication via Asymmetric Hashing." *Proceedings of the 65th Annual IEEE Symposium on Foundations of Computer Science (FOCS)*.

9. Cohn, H., & Umans, C. (2003). "A Group-Theoretic Approach to Matrix Multiplication." *Proceedings of the 44th Annual IEEE Symposium on Foundations of Computer Science (FOCS)*, 438--449.

10. Higham, N. J. (1990). "Exploiting Fast Matrix Multiplication Within the Level 3 BLAS." *ACM Transactions on Mathematical Software*, 16(4), 352--368.

11. Burgisser, P., Clausen, M., & Shokrollahi, M. A. (1997). *Algebraic Complexity Theory*. Springer, Berlin.

12. Pan, V. Ya. (1980). "New Fast Algorithms for Matrix Operations Based on Strassen's Algorithm." *SIAM Journal on Computing*, 9(2), 321--342.

13. Schonhage, A. (1981). "Partial and Total Matrix Multiplication." *SIAM Journal on Computing*, 10(3), 434--455.

14. Ballard, G., Demmel, J., Holtz, O., & Schwartz, O. (2012). "Minimizing Communication in Numerical Linear Algebra." *SIAM Journal on Matrix Analysis and Applications*, 32(3), 866--901.
