# Francis QR 算法：计算所有特征值的迭代杰作

## 1. 标题

**The QR Transformation: A Unitary Analogue to the LR Transformation**
（QR 变换：LR 变换的酉类比）

Part I 发表于 *The Computer Journal*，1961 年，第 4 卷第 3 期，第 265—271 页。
Part II（"A Unitary Analogue to the LR Transformation—Part 2"）发表于 *The Computer Journal*，1962 年，第 4 卷第 4 期，第 332—345 页。

---

## 2. 作者/作者群

**John G. F. Francis**（约翰·弗朗西斯），英国数学家/工程师。

Francis 的人生故事是计算数学史上最引人注目的传奇之一。与大多数数值分析领域的奠基者不同，Francis 在发表这两篇开创性论文时并非学术界人士。他当时是一位年轻的工程师，在国家物理实验室（National Physical Laboratory, NPL）和随后的计算机公司 Ferranti 工作。据后来的考证，Francis 在发表这两篇论文时大约 27 岁——对于提出"20 世纪十大算法之一"来说，这是一个令人惊叹的年龄。

更为传奇的是，Francis 在发表这两篇论文后几乎完全离开了学术界和数值分析领域。他转入了其他工业和咨询工作，很长时间以来，数值分析社区甚至不确定他是否还健在。直到 2007 年左右，数值分析历史学家才重新找到 Francis，确认他仍在世。Gene Golub 等人为追踪 Francis 的下落做出了不小的努力。

Francis 的 QR 算法是独立提出的。几乎同时，苏联数学家 **Vera Nikolaevna Kublanovskaya**（韦拉·尼古拉耶夫娜·库布兰诺夫斯卡娅，1920—2012）也独立发现了基本上相同的算法，她的论文于 1961 年发表在苏联期刊上。Kublanovskaya 在列宁格勒（今圣彼得堡）的斯捷克洛夫数学研究所工作，是苏联数值线性代数学派的重要代表。由于语言障碍和冷战时期的信息隔离，两人的工作完全独立。

在数值分析的历史叙述中，QR 算法通常被称为"Francis QR 算法"，但也有许多文献同时提及 Kublanovskaya 的独立贡献。

---

## 3. 发表时间

Francis 的两篇论文分别发表于 1961 年和 1962 年。Kublanovskaya 的论文也发表于 1961 年。

---

## 4. 发表载体/文献背景

*The Computer Journal* 是英国计算机学会（British Computer Society）的官方期刊，创刊于 1958 年。在 1960 年代，它是计算机科学和数值分析领域的重要发表平台，发表了大量有影响力的论文。

Kublanovskaya 的论文发表于 *Zhurnal Vychislitel'noi Matematiki i Matematicheskoi Fiziki*（《计算数学与数学物理杂志》），这是苏联计算数学领域的顶级期刊。

Francis 的工作直接受到 Heinz Rutishauser 的 LR 算法（1958 年提出）的启发。LR 算法使用 LU 分解（而非 QR 分解）来迭代求解特征值，但它在数值稳定性方面存在缺陷——LU 分解可能需要主元选取，而主元选取会破坏相似变换的结构。Francis 的洞察是：将 LR 算法中的 LU 分解替换为 QR 分解，就可以获得一个数值稳定的算法。论文标题中的"Unitary Analogue to the LR Transformation"正是指这种从 LU 到 QR 的替换——将非酉的（LU）操作替换为酉的（QR）操作。

1960 年代初，矩阵特征值计算是数值分析中最活跃的研究方向之一。Householder 变换（1958）提供了将矩阵化为 Hessenberg 形式的高效方法，为特征值迭代算法的高效实现铺平了道路。剩下的关键问题是：如何设计一个可靠、高效的迭代算法，从 Hessenberg 矩阵出发，计算所有特征值。Francis 的 QR 算法正是对这一问题的完美回答。

---

## 5. 一句话总结

**通过反复执行 QR 分解和逆序重组（$A_k = Q_k R_k$，$A_{k+1} = R_k Q_k$），矩阵逐步收敛到 Schur 形式（上三角矩阵），从而揭示所有特征值——位移策略保证了快速收敛。**

---

## 6. 历史背景

矩阵特征值问题——给定方阵 $A$，求满足 $Ax = \lambda x$ 的标量 $\lambda$（特征值）和非零向量 $x$（特征向量）——是数学和工程中最基本的计算问题之一。它出现在结构工程（振动分析）、量子力学（薛定谔方程的离散化）、控制理论（系统稳定性分析）、统计学（主成分分析）等众多领域。

在 QR 算法出现之前，计算矩阵特征值的方法可以大致分为几类：

**幂迭代方法（Power Iteration）**。这是最古老的方法之一：反复用矩阵乘以一个向量，向量会逐渐对齐到最大特征值对应的特征向量方向。然而，这种方法每次只能求出一个特征值（最大的那个），效率低下。反幂迭代（inverse iteration）和位移幂迭代（shifted power iteration）可以改进这一点，但仍然不够高效。

**Jacobi 方法（1846）**。对于对称矩阵，Jacobi 方法通过反复的平面旋转将矩阵逐步对角化。虽然这个方法在理论上是收敛的，但它的收敛速度是线性的（每步只能减少一点点非对角元素），对于大矩阵来说太慢了。不过值得一提的是，Jacobi 方法在并行计算环境中近年来获得了复兴。

**LR 算法（Rutishauser, 1958）**。Heinz Rutishauser 提出的 LR 算法是 QR 算法的直接前驱。LR 算法的基本思想是：对矩阵 $A$ 进行 LU 分解 $A = LR$（此处 $L$ 是下三角，$R$ 是上三角），然后将因子反序相乘得到 $A' = RL$。重复这一过程，$A'$ 会逐步趋向上三角形式，对角线元素就是特征值。然而，LR 算法有一个严重的缺点：LU 分解可能需要主元选取，而主元选取会破坏相似变换的性质——$A'$ 不再与 $A$ 相似，因此特征值可能不守恒。

Francis 的突破在于认识到：**将 LR 算法中的 LU 分解替换为 QR 分解，就可以完全避免数值稳定性问题**。由于 QR 分解总是存在的（不需要主元选取），而且 $Q$ 是正交矩阵（条件数为 1），QR 算法在数值上是完美稳定的。

更进一步，Francis 的第二篇论文引入了**隐式位移**（implicit shift）技术，这是 QR 算法实用化的关键。位移策略将收敛速度从线性提高到立方（对称矩阵）或至少二次（一般矩阵），使得 QR 算法在实际计算中极其高效。

---

## 7. 核心问题定义

给定一个 $n \times n$ 的实矩阵 $A$，核心问题是：

**如何高效、可靠地计算 $A$ 的所有 $n$ 个特征值（包括可能的复特征值）？**

更精确地说，目标是通过正交相似变换将 $A$ 化为实 Schur 形式：

$$Q^T A Q = T$$

其中 $T$ 是拟上三角矩阵（quasi-upper triangular matrix）——对角线上的块要么是 $1 \times 1$ 的（对应实特征值），要么是 $2 \times 2$ 的（对应共轭复特征值对）。$T$ 的对角块直接给出了 $A$ 的所有特征值。

这个问题的困难之处在于：

1. **特征值可能是复数**，即使矩阵 $A$ 是实矩阵
2. **需要同时求所有特征值**，而不是只求一个或几个
3. **需要数值稳定性**——算法不能因为舍入误差而给出错误的结果
4. **需要高效率**——计算量应该是 $O(n^3)$ 或更好（经过 Hessenberg 预处理后，单步为 $O(n^2)$）

Abel-Ruffini 定理告诉我们，对于 $n \geq 5$，一般的 $n$ 次多项式没有求根公式。由于矩阵的特征值就是其特征多项式的根，这意味着不可能有一个**有限步**的算法来精确计算所有特征值。因此，特征值计算本质上必须是迭代的——需要通过逐步逼近来求得。

QR 算法正是这样一种迭代方法，它以优雅的方式实现了这一目标。

---

## 8. 主要结论/方法/定理

**基本 QR 迭代**。QR 算法的基本形式非常简洁：

给定矩阵 $A_0 = A$，对 $k = 0, 1, 2, \ldots$：
1. 对 $A_k$ 进行 QR 分解：$A_k = Q_k R_k$
2. 反序重组：$A_{k+1} = R_k Q_k$

注意 $A_{k+1} = R_k Q_k = Q_k^T (Q_k R_k) Q_k = Q_k^T A_k Q_k$，所以 $A_{k+1}$ 与 $A_k$ 正交相似。因此，所有 $A_k$ 具有相同的特征值。

**关键定理**：在适当的条件下（特征值的模互不相同），$A_k$ 收敛到上三角矩阵（即 Schur 形式），对角线元素就是特征值，按模从大到小排列。

**位移策略**。基本 QR 迭代的收敛速度取决于特征值模的比值。如果两个特征值的模非常接近，收敛会非常慢。位移策略通过以下修改加速收敛：

给定位移量 $\mu_k$（接近某个特征值的估计），对 $k = 0, 1, 2, \ldots$：
1. 分解：$A_k - \mu_k I = Q_k R_k$
2. 重组：$A_{k+1} = R_k Q_k + \mu_k I$

同样地，$A_{k+1}$ 与 $A_k$ 正交相似。位移量 $\mu_k$ 的选择是算法效率的关键。

**Wilkinson 位移**。对于对称矩阵，James Wilkinson 提出了一种特别有效的位移选择策略。考虑 $A_k$ 的右下 $2 \times 2$ 子矩阵

$$\begin{pmatrix} a & b \\ b & c \end{pmatrix}$$

Wilkinson 位移 $\mu_k$ 取为这个 $2 \times 2$ 矩阵的两个特征值中更接近 $c$ 的那个。这一选择保证了立方收敛速度（cubic convergence）。

**隐式 QR 步（Implicit QR Step）**。Francis 的第二篇论文引入了一个至关重要的实现技巧——隐式 QR 步。对于已经化为 Hessenberg 形式的矩阵，不需要显式地计算 QR 分解。利用**隐式 Q 定理**（Implicit Q Theorem），只需要知道 $Q$ 的第一列，就可以通过一系列"追赶"（chasing）操作隐式地完成整个 QR 步。

具体地，对于带位移的 QR 步 $A - \mu I = QR$，$Q$ 的第一列与 $A - \mu I$ 的第一列成比例。利用这一信息，可以构造一个 Householder 变换 $P_0$ 使得 $P_0$ 的第一列与 $Q$ 的第一列相同。然后，$P_0^T A P_0$ 会产生一个"凸起"（bulge）——在 Hessenberg 结构中多出的一些非零元素。通过一系列后续的 Householder 变换将这个"凸起"沿矩阵对角线"追赶"到右下角并消除，就完成了一个隐式 QR 步。

**双重隐式位移（Double Implicit Shift）**。对于实矩阵可能有共轭复特征值对的情况，Francis 提出了双重位移策略：同时使用 $2 \times 2$ 子矩阵的两个特征值作为位移，执行两步 QR 迭代的等效操作。由于两个位移是共轭复数，合并后的操作完全在实数域内完成，避免了复数运算。这一技巧在实际实现中极为重要。

---

## 9. 核心思想的直觉解释

QR 算法的核心思想可以通过以下直觉来理解。

想象一个旋转的陀螺。陀螺绕一个轴旋转——这个轴的方向就是"主方向"。如果你多次观察这个陀螺的运动（对应于多次矩阵乘法），陀螺的行为会越来越明显地体现出它的主方向。

在矩阵的世界中，特征值和特征向量就是矩阵"内在结构"的体现。QR 算法通过反复的"分解-重组"操作，逐步让矩阵的内在结构"浮现"出来。

更具体地说，$n$ 步 QR 迭代的效果等价于对 $A^n$ 做 QR 分解。而 $A^n$ 的列空间会逐步对齐到 $A$ 的主要不变子空间（dominant invariant subspace）。这就是为什么迭代后的矩阵会逐步趋向上三角形式——特征值按模的大小排序，"浮"到对角线上。

位移策略的直觉则更加巧妙。通过减去一个接近某个特征值的位移量 $\mu$，矩阵 $A - \mu I$ 的最小特征值（即 $\lambda - \mu$，其中 $\lambda$ 是最接近 $\mu$ 的特征值）变得非常小。这相当于将一个特征值"拉到"接近零的位置，使得收敛极快——如同用磁铁吸引一个特定的铁球，使它迅速到位。

打一个比方：QR 算法就像是在筛沙子。每次"筛"一下（一步 QR 迭代），较大的颗粒就会逐渐上浮，较小的颗粒逐渐下沉。最终，所有颗粒按大小排好序——这就是矩阵收敛到上三角形式的过程。位移策略就像是用不同大小的筛孔来加速特定大小颗粒的分离。

---

## 10. 为什么这篇文献重要

QR 算法被列入"20 世纪十大算法"（由 SIAM News 在 2000 年评选）之中，与快速傅里叶变换（FFT）、单纯形法、蒙特卡洛方法等并列。这一殊荣说明了它的非凡地位。以下几个方面进一步阐明了其重要性：

**解决了核心计算问题**。矩阵特征值计算是科学计算中最基本的问题之一。QR 算法提供了一个通用、可靠、高效的解决方案——它适用于任意方阵（对称或非对称、实数或复数），能够计算所有特征值，且在数值上是稳定的。在 QR 算法之前，没有任何方法能同时满足这些要求。

**数值稳定性的典范**。QR 算法完全基于正交变换（Householder 反射或 Givens 旋转），因此具有理想的数值稳定性。Wilkinson 的后向误差分析（backward error analysis）表明：QR 算法计算的特征值是原始矩阵的一个小扰动的精确特征值。换句话说，QR 算法的误差完全可以归因于输入数据中不可避免的不确定性。

**优雅的数学结构**。QR 算法的数学结构极为优美。它与许多深刻的数学理论有联系：Schur 分解、矩阵不变子空间理论、齐次空间上的动力系统等。特别是，QR 迭代可以被理解为 Grassmann 流形上的一种自然迭代，这一观点揭示了算法收敛性的深层原因。

**实践中的普及**。QR 算法（的各种优化变体）是当今所有通用特征值计算软件的核心。从 EISPACK（1970 年代）到 LAPACK（1990 年代至今），从 MATLAB 到 NumPy，每当你调用特征值计算函数时，底层运行的几乎肯定是 QR 算法或其变体。

**Francis 的传奇经历**。一位非学术界的年轻工程师独立提出了 20 世纪最重要的算法之一，然后几乎完全消失在历史中——这个故事本身就具有传奇色彩，提醒我们伟大的数学贡献可以来自意想不到的地方。

---

## 11. 它解决了当时什么瓶颈

**瓶颈一：LR 算法的数值不稳定性**。Rutishauser 的 LR 算法在概念上是优雅的，但在数值实现中存在严重问题。LU 分解可能需要主元选取，而主元选取会破坏相似变换的性质。对于某些矩阵，LR 算法甚至无法进行（例如，当前导主子式为零时）。QR 算法通过使用 QR 分解（总是存在且数值稳定）完全解决了这一问题。

**瓶颈二：缺乏通用的特征值算法**。在 QR 算法之前，不同类型的矩阵（对称vs.非对称、实数vs.复数）需要不同的特征值算法。Jacobi 方法仅适用于对称矩阵；幂迭代方法一次只能求一个特征值。QR 算法提供了一个统一的框架，适用于所有类型的矩阵。

**瓶颈三：收敛速度**。基本的 QR 迭代（不带位移）的收敛速度可能很慢，特别是当特征值的模接近时。Francis 引入的位移策略——特别是隐式双重位移——将收敛速度提高到了实践中几乎总是令人满意的水平。对于对称矩阵，Wilkinson 位移保证了立方收敛。

**瓶颈四：复特征值的处理**。实矩阵可能有共轭复特征值对。如何在完全实数运算中处理这一情况？Francis 的双重隐式位移策略巧妙地解决了这个问题：通过同时使用一对共轭复数位移，两步 QR 迭代的合并效果完全在实数域内，最终得到实 Schur 形式中的 $2 \times 2$ 对角块。

---

## 12. 它与前人工作的关系

**Rutishauser 的 LR 算法（1958）**。QR 算法直接脱胎于 LR 算法。Heinz Rutishauser 的 LR 算法使用 LU 分解进行迭代：$A = LR$，$A' = RL$。Francis 的创新在于将 LU 替换为 QR——一个看似简单的替换，却带来了本质性的改进。正如论文标题所明示的，QR 变换是 LR 变换的"酉类比"。Rutishauser 本人后来也认可了 QR 算法的优越性，并在后续工作中转向了 QR 方法。

**Householder 变换（1958）**。Householder 提出的正交反射方法是 QR 算法高效实现的关键前提。在应用 QR 算法之前，首先通过 Householder 变换将矩阵化为上 Hessenberg 形式，这将每步 QR 迭代的计算量从 $O(n^3)$ 降低到 $O(n^2)$。没有 Householder 的预处理，QR 算法的实际效率将大打折扣。

**Givens 旋转（1954）**。Givens 旋转是 Householder 变换的替代工具。在 QR 算法的每一步中，对 Hessenberg 矩阵的 QR 分解可以使用 Givens 旋转来完成，每次消去一个次对角线元素。这在隐式 QR 步中的"追赶"操作中特别有用。

**幂迭代与反幂迭代**。QR 算法可以被理解为多个反幂迭代（inverse iteration）的同步进行。从数学上说，$k$ 步 QR 迭代后的正交因子 $Q_1 Q_2 \cdots Q_k$ 的列张成了与矩阵 $A^k$ 的列空间相关的不变子空间——这正是幂迭代所追求的目标，但 QR 算法同时对所有特征向量进行追踪，而不仅仅是主特征向量。

**Jacobi 方法（1846）**。Jacobi 方法是正交变换对角化矩阵的先驱。QR 算法可以看作是 Jacobi 方法思想的升华——同样使用正交变换，但通过更高效的迭代策略（而非逐个消元素）来实现收敛。

**Kublanovskaya 的独立发现（1961）**。Vera Kublanovskaya 在苏联独立提出了基本上相同的 QR 迭代方法。这种独立发现在科学史上并不罕见——它表明 QR 算法是时代发展的自然产物，而非某个人凭空的灵感。两人的工作从不同的角度证实了 QR 迭代思想的正确性和重要性。

---

## 13. 它对后续哪些方向产生了影响

QR 算法的影响几乎渗透到了数值线性代数和科学计算的每一个角落。

**EISPACK 和 LAPACK**。QR 算法的第一个标准化实现出现在 EISPACK（Eigensystem Package，1970 年代）中，由 B. S. Garbow、J. M. Boyle、J. J. Dongarra 和 C. B. Moler 等人开发。此后，LAPACK（1990 年代）继承并改进了这些实现。LAPACK 中的 `DHSEQR`（双重隐式位移 QR 算法处理上 Hessenberg 矩阵）是当今最广泛使用的特征值计算例程。

**MATLAB 和 NumPy 等高级软件**。MATLAB 的 `eig` 函数和 NumPy 的 `numpy.linalg.eig` 底层都调用 LAPACK 的 QR 算法实现。因此，全世界每天有数以百万计的特征值计算在使用 Francis 发明的算法。

**对称矩阵的分治算法（Divide-and-Conquer）**。Cuppen（1981）提出了一种替代 QR 算法的特征值计算方法——分治算法。该方法对于大型对称三对角矩阵可以比 QR 算法更快。然而，分治算法的可靠实现在很大程度上借鉴了 QR 算法的数值分析经验，并且 QR 算法仍然作为分治算法中小块矩阵处理的子程序使用。

**MRRR 算法（Multiple Relatively Robust Representations）**。Dhillon 和 Parlett（2004）提出的 MRRR 算法是另一种先进的特征值/特征向量计算方法，在某些情况下比 QR 算法更高效。但同样，MRRR 算法的理论基础和数值分析框架深受 QR 算法传统的影响。

**SVD 计算**。QR 算法的思想直接影响了 SVD 的迭代计算方法。Golub-Reinsch 算法（1970）——计算 SVD 的标准方法——本质上是将 QR 迭代应用于双对角矩阵。隐式位移和"追赶"技巧在 SVD 计算中同样发挥着关键作用。

**控制理论和系统识别**。在控制理论中，系统的稳定性由系统矩阵的特征值决定。QR 算法使得大规模控制系统的稳定性分析成为可能。此外，QR 分解在卡尔曼滤波的数值稳定实现中也起着核心作用。

**量子化学和凝聚态物理**。在量子化学的 Hartree-Fock 计算和密度泛函理论中，需要反复求解大型矩阵的特征值。QR 算法（以及其对称变体和 Krylov 子空间方法的组合）是这些计算的核心工具。

**Google PageRank**。虽然 PageRank 的计算主要使用幂迭代方法（因为网页链接矩阵极为稀疏和庞大），但 QR 算法为理解幂迭代的收敛性和改进提供了理论基础。

---

## 14. 今天回看它的价值

在 QR 算法提出 60 余年后的今天，这一算法仍然具有不可替代的价值。

**作为稠密矩阵特征值计算的金标准**，QR 算法至今没有被完全超越。虽然对于大型稀疏矩阵，Krylov 子空间方法（Lanczos、Arnoldi、LOBPCG 等）通常更为合适，但对于中小规模的稠密矩阵（$n$ 从几十到几千），QR 算法仍然是最可靠、最高效的选择。

**在机器学习和数据科学中的间接应用**。主成分分析（PCA）、谱聚类（spectral clustering）、图拉普拉斯特征分解——这些现代数据分析技术的核心都涉及特征值计算。对于中等规模的数据集，底层使用的往往就是 QR 算法。

**算法可靠性的标杆**。经过 Wilkinson、Golub、Parlett 等人数十年的深入分析和工程实践，QR 算法（特别是 LAPACK 中的实现）已经达到了极高的可靠性水平。它很少失败，即使在极端的测试用例上也能给出令人满意的结果。这种可靠性使它成为其他特征值算法的比较基准。

**对算法设计哲学的影响**。QR 算法的成功展示了几个重要的算法设计原则：(1) 正交变换优于非正交变换；(2) 位移策略可以极大加速迭代收敛；(3) 隐式实现可以在保持等价性的同时提高效率和稳定性。这些原则已经成为数值算法设计的一般准则。

**Francis 的故事作为科学史的教训**。一位年轻的非学术界工程师发明了如此重要的算法，然后几乎消失在历史中——这个故事提醒我们，伟大的贡献可以来自意想不到的地方，也提醒学术共同体应该更好地认可和保存这些贡献。

---

## 15. 面向普通读者的通俗解释

想象你是一位矿工，面前有一块巨大的混合矿石，里面包含多种金属（金、银、铜等），你想要把它们分离出来。

**特征值**就好比矿石中不同金属的含量和性质——它们是"隐藏"在矩阵中的核心信息。

**QR 算法**就像是一台精密的分选机。你把矿石放进机器，机器运转一次（一步 QR 迭代），矿石中不同金属的分布就会更有序一些——重的金属沉下去，轻的浮上来。反复运转多次，不同的金属就会逐步完全分离。

**位移策略**就好比你调节分选机的参数，让它特别针对某种金属进行分选。比如你知道矿石中可能有黄金，你就把机器调到特别适合分离黄金的模式——这样黄金很快就被分出来了。然后你再调到适合银的模式，把银分出来。这比使用一个固定模式逐步分离所有金属要快得多。

**Householder 预处理**则像是在放入分选机之前先把矿石粗碎——这不改变矿石的成分（特征值不变），但让分选机的工作效率大大提高。

为什么这个算法如此重要？因为"从矿石中提取金属"——也就是从矩阵中提取特征值——是科学和工程中最常见的计算任务之一。无论是分析桥梁是否会在风中振动（结构工程），还是发现数据中的隐藏模式（机器学习），都需要计算矩阵的特征值。QR 算法是完成这一任务最可靠、最高效的工具，至今仍然如此。

---

## 16. 阅读原文建议

Francis 的两篇原始论文写得相当技术性，但思路清晰。以下建议可能有助于阅读：

**预备知识**：
- 线性代数：特征值和特征向量、QR 分解、正交矩阵、Schur 分解
- 矩阵计算基础：Hessenberg 矩阵、Householder 变换
- 基本的迭代法概念：收敛速度、位移策略

**推荐阅读路径**：
1. 先阅读 Part I，理解基本 QR 迭代的思想和与 LR 算法的关系
2. 再阅读 Part II，重点理解隐式位移和双重位移技巧
3. 结合现代教科书来补充数值分析细节（特别是收敛性证明和后向误差分析）

**更友好的替代材料**：
- Golub, G. H. and Van Loan, C. F. *Matrix Computations*. 4th ed. Johns Hopkins University Press, 2013. 第 7 章和第 8 章详细讨论了 QR 算法。
- Trefethen, L. N. and Bau, D. *Numerical Linear Algebra*. SIAM, 1997. 第 28—29 讲以极其清晰的方式讲解了 QR 算法。
- Watkins, D. S. *The Matrix Eigenvalue Problem: GR and Krylov Subspace Methods*. SIAM, 2007. 深入讨论了 QR 算法及其各种变体。
- Parlett, B. N. *The Symmetric Eigenvalue Problem*. Prentice-Hall, 1980. (Reprinted by SIAM, 1998.) 对称情况的经典参考。

**历史和传记材料**：
- Golub, G. H. and Uhlig, F. "The QR algorithm: 50 years later, its genesis by John Francis and Vera Kublanovskaya and subsequent developments." *IMA Journal of Numerical Analysis*, 29(3):467--485, 2009. 详细记录了 QR 算法的发明故事和 Francis 的经历。

---

## 17. 局限性/历史局限

**不适用于大规模稀疏矩阵**。QR 算法的标准实现要求矩阵是稠密的（或已经化为 Hessenberg 形式）。对于大规模稀疏矩阵（如有限元离散化产生的矩阵），QR 算法不实用——它会破坏稀疏结构，计算量和存储量都太大。对于这类问题，Krylov 子空间方法（Lanczos、Arnoldi、IRAM 等）是标准选择。

**仅在一定条件下保证收敛**。虽然 QR 算法在实践中几乎总是收敛的，但严格的收敛性理论需要一些假设——例如特征值具有不同的模。对于具有相同模的特征值（如共轭复数对），需要特殊处理（双重位移策略）。在极少数病态情况下，QR 算法可能收敛缓慢，需要额外的策略（如异常位移，exceptional shift）。

**计算量仍然是 $O(n^3)$**。对于标准 QR 算法，即使使用 Hessenberg 预处理，总计算量仍然是 $O(n^3)$（多步 $O(n^2)$ 的迭代）。对于只需要少数几个特征值的情况，这不如 Krylov 方法高效。

**与分治算法和 MRRR 的竞争**。对于对称三对角矩阵的特征值问题，Cuppen 的分治算法和 Dhillon-Parlett 的 MRRR 算法在某些情况下比 QR 算法更快，特别是当同时需要特征向量时。LAPACK 中已经将分治算法（DSYEVD）和 MRRR（DSYEVR）作为对称特征值问题的默认和推荐算法。

**Francis 论文的技术难度**。Francis 的原始论文虽然思想深刻，但某些推导比较简略，对于现代读者来说可能不够详细。后续的教科书（特别是 Golub-Van Loan 和 Watkins 的著作）提供了更为详细和清晰的讲解。

---

## 18. 延伸阅读建议

**核心教科书**：
- Golub, G. H. and Van Loan, C. F. *Matrix Computations*. 4th ed. Johns Hopkins University Press, 2013. 第 7—8 章。这是学习 QR 算法及其变体的首选参考。
- Trefethen, L. N. and Bau, D. *Numerical Linear Algebra*. SIAM, 1997. 第 24—29 讲。以直观、清晰的方式讲解特征值算法。
- Parlett, B. N. *The Symmetric Eigenvalue Problem*. SIAM, 1998. 对称情况的权威参考。
- Watkins, D. S. *The Matrix Eigenvalue Problem: GR and Krylov Subspace Methods*. SIAM, 2007. 深入讨论 QR 算法的现代观点。

**LR 算法的原始文献**：
- Rutishauser, H. "Solution of eigenvalue problems with the LR-transformation." *NBS Applied Mathematics Series*, 49:47--81, 1958.

**Kublanovskaya 的论文（英译）**：
- Kublanovskaya, V. N. "On some algorithms for the solution of the complete eigenvalue problem." *USSR Computational Mathematics and Mathematical Physics*, 1(3):637--657, 1962. (Original Russian paper 1961.)

**QR 算法的历史**：
- Golub, G. H. and Uhlig, F. "The QR algorithm: 50 years later, its genesis by John Francis and Vera Kublanovskaya and subsequent developments." *IMA Journal of Numerical Analysis*, 29(3):467--485, 2009.

**20 世纪十大算法**：
- Cipra, B. A. "The best of the 20th century: Editors name top 10 algorithms." *SIAM News*, 33(4):1--2, 2000.

**替代算法**：
- Cuppen, J. J. M. "A divide and conquer method for the symmetric tridiagonal eigenproblem." *Numerische Mathematik*, 36(2):177--195, 1981.
- Dhillon, I. S. and Parlett, B. N. "Multiple representations to compute orthogonal eigenvectors of symmetric tridiagonal matrices." *Linear Algebra and its Applications*, 387:1--28, 2004.

---

## 19. 参考资料/实际引用文档

1. Francis, J. G. F. "The QR Transformation: A Unitary Analogue to the LR Transformation—Part 1." *The Computer Journal*, 4(3):265--271, 1961.

2. Francis, J. G. F. "The QR Transformation—Part 2." *The Computer Journal*, 4(4):332--345, 1962.

3. Kublanovskaya, V. N. "On some algorithms for the solution of the complete eigenvalue problem." *Zhurnal Vychislitel'noi Matematiki i Matematicheskoi Fiziki*, 1(4):555--570, 1961.

4. Rutishauser, H. "Solution of eigenvalue problems with the LR-transformation." *NBS Applied Mathematics Series*, 49:47--81, 1958.

5. Golub, G. H. and Van Loan, C. F. *Matrix Computations*. 4th ed. Johns Hopkins University Press, 2013.

6. Trefethen, L. N. and Bau, D. *Numerical Linear Algebra*. SIAM, 1997.

7. Parlett, B. N. *The Symmetric Eigenvalue Problem*. Prentice-Hall, 1980. (Reprinted by SIAM, 1998.)

8. Watkins, D. S. *The Matrix Eigenvalue Problem: GR and Krylov Subspace Methods*. SIAM, 2007.

9. Golub, G. H. and Uhlig, F. "The QR algorithm: 50 years later, its genesis by John Francis and Vera Kublanovskaya and subsequent developments." *IMA Journal of Numerical Analysis*, 29(3):467--485, 2009.

10. Cipra, B. A. "The best of the 20th century: Editors name top 10 algorithms." *SIAM News*, 33(4):1--2, 2000.

11. Wilkinson, J. H. *The Algebraic Eigenvalue Problem*. Oxford University Press, 1965.

12. Householder, A. S. "Unitary triangularization of a nonsymmetric matrix." *Journal of the ACM*, 5(4):339--342, 1958.
