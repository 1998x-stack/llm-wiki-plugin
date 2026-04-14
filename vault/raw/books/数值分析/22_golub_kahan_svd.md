# Golub-Kahan 奇异值分解算法：矩阵计算的"瑞士军刀"

## 1. 标题

**"Calculating the Singular Values and Pseudo-Inverse of a Matrix"**
（计算矩阵的奇异值与伪逆）

## 2. 作者/作者群

**Gene Howard Golub (1932--2007)** 与 **William Morton Kahan (1933--)**。

Gene Golub 是斯坦福大学（Stanford University）计算机科学系教授，被广泛誉为数值线性代数领域的"教父"（godfather）。他在矩阵计算领域的贡献几乎无人能及：从奇异值分解到最小二乘问题，从矩阵函数到迭代方法，Golub 的工作奠定了现代矩阵计算的理论和算法基础。他曾担任 SIAM（Society for Industrial and Applied Mathematics）主席，是美国国家科学院（National Academy of Sciences）院士和美国艺术与科学院（American Academy of Arts and Sciences）院士。他与 Charles Van Loan 合著的教科书 *Matrix Computations* 被誉为数值线性代数领域的"圣经"，至今仍是该领域最重要的参考书。

William Kahan 是加州大学伯克利分校（UC Berkeley）的数学教授和计算机科学教授，被尊称为"浮点运算之父"（Father of Floating Point）。他对 IEEE 754 浮点运算标准的制定做出了决定性的贡献——这一标准至今仍是全球所有计算机处理浮点数的基础。Kahan 因其在数值分析和浮点运算方面的杰出贡献，于1989年获得了图灵奖（Turing Award）——计算机科学领域的最高荣誉。Kahan 对数值精度和计算可靠性有着近乎偏执的追求，这种态度深刻影响了整个计算科学界。

两位作者的合作堪称数值分析史上的黄金组合：Golub 的矩阵计算深度与 Kahan 的数值精度洞察力相结合，产生了一个既优雅又实用的算法。

## 3. 发表时间

**1965年**，发表于 *SIAM Journal on Numerical Analysis*，Series B，第2卷，第2期，第205--224页。

有趣的是，这篇论文与 Cooley-Tukey 的 FFT 论文发表在同一年。1965年可以说是计算数学历史上最辉煌的年份之一——两个改变世界的算法同时问世。

## 4. 发表载体/文献背景

*SIAM Journal on Numerical Analysis* 是工业与应用数学学会（SIAM）出版的旗舰期刊之一，专注于数值分析和科学计算领域的研究。该期刊创刊于1964年，Golub-Kahan 的论文发表在其创刊后的第二年，这本身就说明了当时数值分析领域正处于蓬勃发展的时期。

1960年代是数值线性代数的黄金时期。一方面，电子计算机的普及使得大规模矩阵计算成为可能和必要；另一方面，矩阵计算的理论基础——特别是关于数值稳定性和舍入误差分析的理论——正在被 Wilkinson、Kahan 等人系统地建立起来。在这个背景下，开发高效且数值稳定的矩阵分解算法成为了最紧迫的研究课题之一。

奇异值分解（Singular Value Decomposition, SVD）的数学理论早已存在——可以追溯到19世纪后期 Beltrami（1873年）和 Jordan（1874年）的工作。然而，直到 Golub 和 Kahan 的论文之前，并没有一个在实际计算中既高效又稳定的 SVD 算法。

## 5. 一句话总结

Golub 和 Kahan 提出了一种实用的两阶段算法来计算矩阵的奇异值分解：首先通过 Householder 变换将矩阵化为双对角形式（bidiagonalization），然后通过隐式 QR 类迭代计算双对角矩阵的奇异值，从而使 SVD 从一个理论概念变成了一个可靠的计算工具。

## 6. 历史背景

### 奇异值分解的数学起源

奇异值分解的数学理论有着深远的历史。1873年，意大利数学家 Eugenio Beltrami 首次提出了矩阵奇异值的概念。1874年，法国数学家 Camille Jordan 独立地发展了类似的理论。此后，英国数学家 James Joseph Sylvester（1889年）以及 Erhard Schmidt（1907年）分别在不同的数学语境中重新发现和推广了这一概念。Schmidt 将其推广到了无穷维空间（积分算子），为泛函分析中的谱理论奠定了基础。

然而，在很长一段时间内，SVD 主要是一个纯数学工具，用于矩阵理论和算子理论的研究。其计算实现在很大程度上被认为是困难且不实用的。

### 矩阵计算的发展

1960年代之前，矩阵计算领域已经取得了若干重要进展：

- **QR 分解**（1958--1961年）：由 John Francis 和 Vera Kublanovskaya 独立提出的 QR 算法为计算矩阵特征值提供了高效的迭代方法。
- **Householder 变换**（1958年）：Alston Householder 提出了一种基于正交反射的矩阵变换方法，可以高效地将矩阵化为三对角或 Hessenberg 形式。
- **Givens 旋转**（1954年）：Wallace Givens 提出了一种基于平面旋转的矩阵变换方法，适用于稀疏矩阵。
- **Wilkinson 的误差分析**（1960年代初）：James Wilkinson 系统地发展了矩阵计算中的舍入误差分析理论，为判断算法的数值稳定性提供了理论框架。

这些工具为 Golub-Kahan SVD 算法的诞生提供了必要的技术基础。

### 最小二乘问题与伪逆的需求

1960年代，最小二乘问题（least squares problem）在科学和工程中的应用日益广泛。当系数矩阵接近奇异（ill-conditioned）或者秩不足（rank-deficient）时，传统的正规方程方法（normal equations）会导致严重的数值不稳定。Moore-Penrose 伪逆（pseudoinverse）提供了最小二乘问题的理论最优解，但需要一个可靠的计算方法。SVD 正是计算伪逆的自然工具——这是 Golub 和 Kahan 开发 SVD 算法的直接动机之一，也是论文标题中包含"伪逆"的原因。

## 7. 核心问题定义

**核心问题**：给定一个 $m \times n$ 实矩阵 $A$（$m \geq n$），如何高效且数值稳定地计算其奇异值分解

$$A = U \Sigma V^T$$

其中：
- $U$ 是 $m \times m$ 正交矩阵（$U^T U = I$），其列向量称为左奇异向量
- $V$ 是 $n \times n$ 正交矩阵（$V^T V = I$），其列向量称为右奇异向量
- $\Sigma$ 是 $m \times n$ 对角矩阵，对角元素 $\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_n \geq 0$ 称为奇异值

**附带目标**：利用 SVD 计算矩阵 $A$ 的 Moore-Penrose 伪逆 $A^+$：

$$A^+ = V \Sigma^+ U^T$$

其中 $\Sigma^+$ 是将 $\Sigma$ 中非零对角元素取倒数得到的矩阵。

## 8. 主要结论/方法/定理

### 两阶段算法

Golub-Kahan 算法分为两个阶段：

**第一阶段：双对角化（Bidiagonalization）**

使用 Householder 变换将矩阵 $A$ 化为上双对角形式：

$$U_1^T A V_1 = B = \begin{pmatrix} d_1 & f_1 & & \\ & d_2 & f_2 & \\ & & \ddots & \ddots \\ & & & d_{n-1} & f_{n-1} \\ & & & & d_n \\ & & & & \\ & & & & \end{pmatrix}$$

其中 $B$ 是上双对角矩阵（只有主对角线和上副对角线有非零元素），$U_1$ 和 $V_1$ 是通过一系列 Householder 变换累积得到的正交矩阵。

这一步的计算量为 $O(mn^2)$（当 $m \gg n$ 时）或 $O(n^3)$（当 $m \approx n$ 时），且因为使用正交变换，数值稳定性有保证。

**第二阶段：双对角矩阵的 SVD（隐式 QR 迭代）**

对双对角矩阵 $B$ 进行迭代求解其奇异值。Golub 和 Kahan 提出了一种基于 QR 算法思想的迭代方法：

核心思想是考虑矩阵 $T = B^T B$，这是一个对称三对角矩阵。$T$ 的特征值就是 $B$ 的奇异值的平方。但关键的技巧是：不显式地形成 $B^T B$（这会导致精度损失——条件数平方），而是通过隐式位移的 QR 迭代直接在 $B$ 上操作。

每次迭代中：
1. 选择适当的位移 $\mu$（通常取 $T$ 右下角 $2 \times 2$ 子矩阵的较小特征值）
2. 通过一系列 Givens 旋转对 $B$ 进行变换，产生"追逐"（chasing）效果
3. 每个超对角元素最终趋向零，对应的对角元素收敛到奇异值

这种迭代通常具有三次（cubic）收敛速度，在实践中每个奇异值的收敛只需要少数几次迭代。

### Golub-Kahan 双对角化过程的细节

双对角化过程交替使用左乘和右乘 Householder 变换：

1. 首先用左 Householder 变换将第一列消为只有第一个元素非零
2. 然后用右 Householder 变换将第一行消为只有前两个元素非零
3. 接着用左 Householder 变换将第二列消为只有前两个元素非零
4. 如此交替进行，直到矩阵变成双对角形式

这个过程的巧妙之处在于：每一步消零都不会破坏前面步骤已经形成的结构。

### 伪逆的计算

一旦得到 SVD $A = U \Sigma V^T$，Moore-Penrose 伪逆的计算就变得直截了当：

$$A^+ = V \Sigma^+ U^T$$

其中 $\Sigma^+$ 通过将 $\Sigma$ 中大于某个阈值 $\epsilon$ 的奇异值取倒数、将小于 $\epsilon$ 的奇异值置零来获得。阈值的选择反映了对矩阵有效秩（numerical rank）的判断。

### 收敛性

Golub 和 Kahan 证明了他们的迭代算法具有良好的收敛性质。带有 Wilkinson 位移的隐式 QR 迭代在实践中表现出三次收敛速度，这意味着每次迭代大约将误差的有效数字增加三倍。

## 9. 核心思想的直觉解释

### SVD 的几何意义

SVD 的核心思想可以用一个简单的几何图像来理解。任何线性变换（矩阵乘法）都可以分解为三个基本操作的组合：

1. **旋转（或反射）**：$V^T$ 将输入向量在"输入空间"中旋转
2. **缩放**：$\Sigma$ 沿各坐标轴进行独立的拉伸或压缩
3. **旋转（或反射）**：$U$ 将结果在"输出空间"中旋转

换句话说，无论矩阵 $A$ 代表多么复杂的线性变换，SVD 都能揭示其本质：它不过是在某些特殊方向上的拉伸和旋转的组合。

形象地说，如果你把一个球体通过线性变换 $A$ 变换后，它会变成一个椭球体。SVD 告诉你这个椭球体的主轴方向（由 $U$ 和 $V$ 确定）和主轴长度（由奇异值 $\sigma_i$ 确定）。

### 双对角化的直觉

为什么要先化为双对角形式？这是因为对一般矩阵直接计算 SVD 太复杂了。双对角矩阵是矩阵可能具有的"最简单"的非对角结构——只有主对角线和一条副对角线上有非零元素。将矩阵化为这种形式后，SVD 计算变得简单得多。

这个策略类似于 QR 算法中先将矩阵化为 Hessenberg 形式：通过一次性的初始预处理（$O(n^3)$ 成本），大幅简化后续迭代步骤的工作量。

### 隐式方法的精妙之处

算法中最巧妙的部分是"隐式"计算。直觉上，我们想要计算 $B^T B$ 的特征值（因为它们就是奇异值的平方），但显式形成 $B^T B$ 会导致条件数平方——如果 $B$ 的条件数已经是 $10^8$，那么 $B^T B$ 的条件数就是 $10^{16}$，在双精度浮点运算（约16位有效数字）中几乎所有精度都会丢失。

Golub-Kahan 的隐式方法避免了这个陷阱：它在 $B$ 上直接操作，但产生的效果等价于对 $B^T B$ 进行 QR 迭代。这样，算法既利用了 QR 迭代的快速收敛性，又保持了直接处理 $B$ 的数值稳定性。这种"隐式"技巧是数值分析中最深刻的思想之一。

## 10. 为什么这篇文献重要

### SVD 的普适性

SVD 被称为矩阵计算的"瑞士军刀"（Swiss army knife），因为它可以用来解决几乎所有的矩阵计算问题：

| 应用 | SVD 的作用 |
|------|-----------|
| 线性方程组求解 | 通过伪逆给出最小范数解 |
| 最小二乘问题 | 给出稳定的最小二乘解，即使矩阵病态 |
| 低秩近似 | Eckart-Young 定理：SVD 给出最优低秩近似 |
| 矩阵的秩 | 非零奇异值的个数 = 矩阵的秩 |
| 条件数 | $\kappa(A) = \sigma_1 / \sigma_n$ |
| 矩阵范数 | $\|A\|_2 = \sigma_1$ |
| 数值秩判定 | 通过奇异值的衰减判断有效秩 |

没有 Golub-Kahan 算法（及其后续改进），SVD 将停留在理论层面，无法在实际计算中发挥这些作用。

### 开创实用矩阵分解的先河

Golub-Kahan 论文不仅解决了 SVD 的计算问题，还为矩阵分解算法的设计树立了范式：先通过正交变换将矩阵化为紧凑形式（如双对角形式），然后通过迭代方法求解简化问题。这一范式后来被广泛应用于其他矩阵分解问题。

### 对数值稳定性的重视

论文体现了 Golub 和 Kahan 对数值稳定性的高度重视。使用正交变换（而非消元法）进行双对角化，避免显式形成 $A^T A$——这些选择都是为了确保算法在浮点运算中的可靠性。这种对数值精度的严谨态度成为了数值线性代数研究的黄金标准。

## 11. 它解决了当时什么瓶颈

### 实际 SVD 计算的空白

在 Golub-Kahan 论文之前，虽然 SVD 的数学理论已经完善，但没有一个公认的、高效且稳定的计算算法。研究者们知道 SVD 在理论上很有用，但在实际计算中往往转而使用其他方法（如 QR 分解或正规方程），因为缺少实用的 SVD 算法。Golub-Kahan 算法填补了这个空白。

### 病态最小二乘问题

当最小二乘问题的系数矩阵接近奇异时，传统方法（特别是基于正规方程 $A^T A x = A^T b$ 的方法）会产生严重的数值误差。SVD 提供了处理这类问题的最稳定方法，而 Golub-Kahan 算法使得基于 SVD 的最小二乘求解在实际中可行。

### 伪逆的实际计算

Moore-Penrose 伪逆是处理不一致线性系统和秩亏线性系统的基本工具。Golub 和 Kahan 不仅解决了 SVD 的计算问题，还明确展示了如何通过 SVD 来可靠地计算伪逆，包括如何处理数值秩判定（通过奇异值阈值）的实际问题。

## 12. 它与前人工作的关系

### 与 Beltrami 和 Jordan 的关系

Beltrami（1873年）和 Jordan（1874年）建立了 SVD 的数学理论基础。Golub-Kahan 论文将这一理论从数学抽象变成了计算现实。

### 与 Householder 的关系

Alston Householder 1958年提出的 Householder 变换（Householder reflections）是 Golub-Kahan 双对角化步骤的核心工具。Householder 变换的数值稳定性和计算效率使得双对角化成为可能。

### 与 Francis 和 Kublanovskaya 的关系

John Francis（1961年）和 Vera Kublanovskaya（1961年）独立提出的 QR 算法是 Golub-Kahan 迭代步骤的思想来源。Golub 和 Kahan 巧妙地将 QR 算法的思想从对称特征值问题推广到了奇异值问题。

### 与 Wilkinson 的关系

James Wilkinson 的舍入误差分析理论为 Golub-Kahan 算法的数值稳定性分析提供了理论框架。Wilkinson 提出的位移策略（Wilkinson shift）后来也被应用到 SVD 迭代中以加速收敛。

### 与 Jacobi 的关系

Carl Gustav Jacob Jacobi 在1846年提出的 Jacobi 旋转方法可以看作是 SVD 算法的一种早期形式（对于对称矩阵，特征值分解和 SVD 密切相关）。然而，Jacobi 方法的收敛速度通常较慢。Golub-Kahan 算法通过双对角化预处理和隐式 QR 迭代实现了更快的收敛。

### 与 Eckart 和 Young 的关系

Eckart 和 Young 在1936年证明了一个重要定理：在 Frobenius 范数下，矩阵的最佳秩 $k$ 近似由保留最大的 $k$ 个奇异值和对应的奇异向量得到。这个定理赋予了 SVD 一个极为重要的应用——低秩近似——而 Golub-Kahan 算法使得这个应用在计算上成为可能。

## 13. 它对后续哪些方向产生了影响

### 算法改进与变体

Golub-Kahan 论文之后，SVD 算法持续得到改进：

- **Golub-Reinsch 算法**（1970年）：Golub 与 Christian Reinsch 合作，进一步优化了迭代步骤，改进了收敛判据和位移策略。这个版本被编入了 EISPACK 软件包。
- **Demmel-Kahan 算法**（1990年）：James Demmel 和 Kahan 提出了一种保证高相对精度的双对角 SVD 算法（dqds 算法），能够精确计算接近零的小奇异值。
- **分治 SVD 算法**：Gu 和 Eisenstat（1995年）等人发展了基于分治策略的 SVD 算法，在某些情况下比传统迭代方法更快。
- **随机化 SVD**：Halko, Martinsson 和 Tropp（2011年）提出了随机化算法来近似计算大规模矩阵的截断 SVD，特别适用于数据科学中的超大规模矩阵。

### LAPACK 和标准数值库

Golub-Kahan 算法（及其 Golub-Reinsch 改进版本）成为了标准数值线性代数库的核心组成部分。LINPACK、EISPACK、LAPACK 中的 SVD 实现都直接或间接地基于 Golub-Kahan 的思想。今天，MATLAB 的 `svd()` 函数、Python NumPy 的 `numpy.linalg.svd()`、R 的 `svd()` 等高级语言中的 SVD 实现，其底层算法都可以追溯到 Golub-Kahan 的工作。

### 主成分分析（PCA）

主成分分析是统计学和数据科学中最常用的降维方法。PCA 的数学本质就是对数据矩阵（或协方差矩阵）进行 SVD。Golub-Kahan 算法使得 PCA 能够应用于大规模数据集，这对统计学、机器学习和数据科学产生了深远影响。

### 潜在语义分析（LSA/LSI）

1990年代，Deerwester 等人提出了潜在语义分析（Latent Semantic Analysis, LSA）——也称为潜在语义索引（Latent Semantic Indexing, LSI）——用于自然语言处理中的文档检索和文本分析。LSA 的核心步骤就是对词-文档矩阵进行截断 SVD。这一应用使得 SVD 进入了自然语言处理领域，并为后来的主题模型等方法铺平了道路。

### 推荐系统

Netflix Prize 竞赛（2006--2009年）使得矩阵分解方法在推荐系统领域备受关注。SVD 及其变体（如 Simon Funk 的增量 SVD）成为协同过滤推荐系统的核心算法。这些方法通过对用户-物品评分矩阵进行低秩分解来预测用户的偏好。

### 图像压缩与处理

SVD 可以用于图像压缩：将图像矩阵进行 SVD，保留最大的若干个奇异值及其对应的奇异向量，就得到了图像的低秩近似。虽然这不是最实用的图像压缩方法（JPEG 使用 DCT），但它是理解图像信息结构的重要工具。

SVD 在图像去噪、图像修复、人脸识别（Eigenfaces 方法）等领域也有重要应用。

### 数值线性代数的教学范式

Golub-Kahan SVD 算法的两阶段结构——先简化后迭代——成为了数值线性代数教学中的经典范式，影响了整个领域的教学方式。

## 14. 今天回看它的价值

### 数据科学时代的核心工具

在今天的数据科学和机器学习时代，SVD 的重要性有增无减：

- **深度学习中的矩阵分析**：SVD 用于分析神经网络权重矩阵的结构，帮助理解网络的学习行为
- **模型压缩**：通过对权重矩阵进行低秩近似来压缩深度学习模型
- **自然语言处理**：词向量（Word Embeddings）的训练可以通过对共现矩阵的 SVD 来实现（GloVe 方法与 SVD 密切相关）
- **推荐系统**：矩阵分解仍然是推荐算法的基础方法之一

### 大规模 SVD 的持续需求

随着数据规模的爆炸性增长，大规模 SVD 计算（或其近似版本）的需求日益迫切。随机化 SVD 算法的发展正是这一需求的体现。Facebook 的 FAISS 库、Google 的 TensorFlow 等现代工具都包含了高效的 SVD 实现或近似。

### Gene Golub 的遗产

Gene Golub 的影响力远远超出了 SVD 算法本身。他培养了大量数值线性代数领域的研究人才，建立了斯坦福大学作为该领域世界中心的地位，并通过他的教科书 *Matrix Computations*（与 Van Loan 合著）影响了几代研究者和工程师。2007年 Golub 去世后，SIAM 设立了 Golub 讲座以纪念他的贡献。

### Kahan 的数值精度遗产

William Kahan 对浮点运算和数值精度的贡献同样具有持久的价值。IEEE 754 标准——他的主要成就之一——至今仍是全球所有计算机的浮点运算基础。他在 Golub-Kahan 论文中体现的对数值稳定性的追求，深刻影响了整个计算科学界对数值精度的态度。

## 15. 面向普通读者的通俗解释

### 什么是奇异值分解

想象你有一张照片。这张照片可以用一个数字矩阵来表示（每个像素对应一个数值）。奇异值分解告诉你一件惊人的事情：这个矩阵可以分解成若干个"层"的叠加。第一层捕捉了图像中最重要的信息，第二层次之，依此类推。

如果你只保留前几层，你仍然可以得到一个看起来和原图非常相似的图像，但存储空间大大减少。这就是 SVD 用于数据压缩的基本原理。

更一般地说，SVD 可以告诉你一组数据中什么是"重要的"，什么是"次要的"——这在数据分析中极为有用。

### 为什么需要一个算法

虽然"分解矩阵"听起来像是一个简单的数学操作，但在实际计算中，这涉及到大量的浮点运算，而浮点运算必然引入舍入误差。如果算法设计不当，这些微小的误差会逐步积累，最终导致计算结果完全不可靠。

Golub 和 Kahan 的贡献在于：他们设计了一种算法，既高效（不需要太多运算步骤）又稳定（舍入误差不会失控）。这使得 SVD 从一个数学理论变成了一个可以在计算机上可靠使用的实用工具。

### SVD 在生活中的应用

SVD 在你的日常生活中无处不在，虽然你可能从未听说过它：

- **Netflix 和 Spotify 的推荐**："你可能也喜欢..."——推荐系统的核心算法之一就是矩阵分解（SVD 的变体）。它通过分析你和其他用户的行为模式来预测你的偏好。
- **Google 搜索**：早期的搜索引擎使用 LSI（潜在语义索引）技术来理解搜索查询的含义，其核心就是 SVD。
- **人脸识别**：一些人脸识别系统使用 SVD 来提取面部特征（"特征脸"方法）。
- **噪声消除**：通过 SVD，可以将信号中的噪声成分（对应较小的奇异值）去除，保留有用信息。

## 16. 阅读原文建议

### 原始论文

Golub-Kahan 的原始论文约20页，包含了算法的完整描述和数值实验。论文的写作风格清晰而技术性强。

**阅读建议**：

1. **预备知识**：读者应当熟悉线性代数的基本概念——矩阵乘法、正交矩阵、特征值分解。了解 Householder 变换和 Givens 旋转会很有帮助。

2. **第一遍**：重点阅读引言和 SVD 的定义，理解论文要解决什么问题。

3. **第二遍**：仔细阅读双对角化部分，理解如何通过交替的左右 Householder 变换将矩阵化为双对角形式。

4. **第三遍**：研究迭代部分，理解隐式 QR 迭代如何在双对角矩阵上工作。

### 更好的入门资料

对于初学者，以下资料可能比原始论文更易理解：

- **Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations* (4th ed.). Johns Hopkins University Press.** 第8章对 SVD 算法有详尽的现代描述。
- **Trefethen, L. N., & Bau, D. (1997). *Numerical Linear Algebra*. SIAM.** 第4--5讲对 SVD 给出了极为清晰的数学介绍。

### 实践建议

1. 先用 MATLAB 或 Python 中的 `svd()` 函数体验 SVD 的功能（图像压缩、低秩近似）
2. 尝试手动计算一个 $3 \times 2$ 矩阵的 SVD
3. 实现 Householder 双对角化
4. 最后阅读原始论文，理解迭代步骤的细节

## 17. 局限性/历史局限

### 原始算法的局限

1. **收敛判据的选择**：原始论文中的收敛判据在某些边界情况下可能不够精确。后来的 Golub-Reinsch 改进版本提供了更完善的收敛判据。

2. **小奇异值的精度**：原始算法对于非常小的奇异值可能无法保证高相对精度。Demmel-Kahan 的后续工作（1990年）专门解决了这个问题。

3. **大规模稀疏矩阵**：Golub-Kahan 算法主要针对稠密矩阵设计。对于大规模稀疏矩阵，需要使用 Lanczos 双对角化等迭代方法来计算部分 SVD。

4. **并行化困难**：传统的 SVD 迭代算法不太适合大规模并行计算。分治 SVD 算法和随机化方法在一定程度上缓解了这个问题。

### 计算规模的限制

在1965年，计算机的内存和处理速度严重限制了可以处理的矩阵规模。论文中的数值实验仅涉及小矩阵。然而，算法本身的设计是可扩展的，随着计算机硬件的进步，同样的算法可以处理越来越大的矩阵。

### 与特征值分解的关系

论文中的 SVD 迭代方法本质上是将 SVD 问题转化为对称特征值问题（通过 $B^T B$ 或 $BB^T$）来处理的。后来的研究者发展了更直接的 SVD 迭代方法，进一步提高了效率和精度。

### 随机化方法的挑战

对于现代大数据应用中出现的超大规模矩阵（维度可达百万甚至更高），即使是优化过的 Golub-Kahan 算法也难以在合理时间内完成完整 SVD。随机化 SVD 方法（如 Halko 等人2011年的工作）提供了高效的近似替代方案，但它们只计算截断 SVD（前 k 个奇异值和奇异向量），而非完整分解。

## 18. 延伸阅读建议

### 教科书

1. **Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations* (4th ed.). Johns Hopkins University Press.**
   矩阵计算领域的权威教科书，对 SVD 算法有最详尽的讨论。

2. **Trefethen, L. N., & Bau, D. (1997). *Numerical Linear Algebra*. SIAM.**
   数值线性代数的优秀教材，对 SVD 的数学理论和算法有清晰的介绍。

3. **Demmel, J. W. (1997). *Applied Numerical Linear Algebra*. SIAM.**
   偏重应用的数值线性代数教材，包含 SVD 在实际问题中的应用讨论。

### 专题论文

4. **Golub, G. H., & Reinsch, C. (1970). "Singular Value Decomposition and Least Squares Solutions." *Numerische Mathematik*, 14, 403--420.**
   Golub-Reinsch 改进版 SVD 算法，成为了 EISPACK 和 LAPACK 中 SVD 实现的基础。

5. **Demmel, J. W., & Kahan, W. (1990). "Accurate Singular Values of Bidiagonal Matrices." *SIAM Journal on Scientific and Statistical Computing*, 11(5), 873--912.**
   关于如何精确计算小奇异值的重要工作。

6. **Halko, N., Martinsson, P. G., & Tropp, J. A. (2011). "Finding Structure with Randomness: Probabilistic Algorithms for Constructing Approximate Matrix Decompositions." *SIAM Review*, 53(2), 217--288.**
   随机化 SVD 算法的权威综述。

### 历史与传记

7. **Moler, C. (2008). "Gene Howard Golub, 1932--2007." *SIAM News*, 41(1).**
   对 Gene Golub 生平和学术贡献的纪念文章。

8. **Kahan, W. (1996). "IEEE Standard 754 for Binary Floating-Point Arithmetic." Lecture Notes.**
   Kahan 关于 IEEE 754 标准的讲义，反映了他对数值精度的深刻理解。

### 应用导向

9. **Wall, M. E., Rechtsteiner, A., & Rocha, L. M. (2003). "Singular Value Decomposition and Principal Component Analysis." In *A Practical Approach to Microarray Data Analysis*, 91--109. Springer.**
   SVD 与 PCA 在生物信息学中的应用。

## 19. 参考资料/实际引用文档

1. Golub, G. H., & Kahan, W. (1965). "Calculating the Singular Values and Pseudo-Inverse of a Matrix." *SIAM Journal on Numerical Analysis*, Series B, 2(2), 205--224.

2. Beltrami, E. (1873). "Sulle funzioni bilineari." *Giornale di Matematiche*, 11, 98--106.

3. Jordan, C. (1874). "Memoire sur les formes bilineaires." *Journal de Mathematiques Pures et Appliquees*, Deuxieme Serie, 19, 35--54.

4. Schmidt, E. (1907). "Zur Theorie der linearen und nichtlinearen Integralgleichungen." *Mathematische Annalen*, 63, 433--476.

5. Eckart, C., & Young, G. (1936). "The Approximation of One Matrix by Another of Lower Rank." *Psychometrika*, 1(3), 211--218.

6. Householder, A. S. (1958). "Unitary Triangularization of a Nonsymmetric Matrix." *Journal of the ACM*, 5(4), 339--342.

7. Francis, J. G. F. (1961). "The QR Transformation: A Unitary Analogue to the LR Transformation." *The Computer Journal*, 4(3), 265--271.

8. Golub, G. H., & Reinsch, C. (1970). "Singular Value Decomposition and Least Squares Solutions." *Numerische Mathematik*, 14, 403--420.

9. Demmel, J. W., & Kahan, W. (1990). "Accurate Singular Values of Bidiagonal Matrices." *SIAM Journal on Scientific and Statistical Computing*, 11(5), 873--912.

10. Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations* (4th ed.). Johns Hopkins University Press.

11. Trefethen, L. N., & Bau, D. (1997). *Numerical Linear Algebra*. SIAM, Philadelphia.

12. Halko, N., Martinsson, P. G., & Tropp, J. A. (2011). "Finding Structure with Randomness: Probabilistic Algorithms for Constructing Approximate Matrix Decompositions." *SIAM Review*, 53(2), 217--288.

13. Deerwester, S., Dumais, S. T., Furnas, G. W., Landauer, T. K., & Harshman, R. (1990). "Indexing by Latent Semantic Analysis." *Journal of the American Society for Information Science*, 41(6), 391--407.

14. Stewart, G. W. (1993). "On the Early History of the Singular Value Decomposition." *SIAM Review*, 35(4), 551--566.
