# Jacobi 迭代法：迭代求解线性方程组的先驱

## 1. 标题

**Jacobi 迭代法**（Jacobi Iterative Method）

亦称 **Jacobi 方法**、**同时位移法**（method of simultaneous displacements）。该方法由雅可比在研究线性方程组求解和对称矩阵特征值问题的背景下提出，是迭代线性代数（iterative linear algebra）的奠基性工作之一。

---

## 2. 作者/作者群

**卡尔·古斯塔夫·雅各布·雅可比**（Carl Gustav Jacob Jacobi, 1804--1851）

雅可比是 19 世纪最杰出的数学家之一，出生于普鲁士波茨坦（Potsdam）。他于 1825 年在柏林大学获得博士学位，随后在柯尼斯堡大学（Universitat Konigsberg）任教长达 18 年。雅可比的数学贡献极为广泛，涵盖椭圆函数（elliptic functions）、行列式理论（determinants）、数论、微分方程和力学等领域。

在线性代数方面，雅可比的贡献尤为深远。他系统发展了行列式理论，引入了雅可比矩阵（Jacobian matrix）的概念，并在求解线性方程组和特征值问题中提出了迭代方法。雅可比迭代法虽然以现代标准来看是一种简单的方法，但它标志着从直接法（direct methods）向迭代法（iterative methods）的范式转变，对后续数值线性代数的发展产生了深远影响。

雅可比英年早逝，年仅 46 岁便因天花去世。但他留下的数学遗产影响了整个 19 世纪下半叶乃至 20 世纪的数学发展。

---

## 3. 发表时间

**1845 年**

雅可比关于迭代方法的思想在 1845 年前后形成并传播，部分内容出现在他关于对称矩阵特征值问题的研究中。其关于线性方程组迭代求解的思想散见于多篇论文和讲义中。需要指出的是，雅可比并未以一篇独立论文的形式系统阐述"Jacobi 迭代法"——这个名称是后人对他方法的总结和命名。

他的相关工作主要见于：
- 1845 年发表的关于行列式和线性方程组的系列论文
- 关于旋转方法求特征值的工作（Jacobi eigenvalue algorithm），发表于 1846 年

---

## 4. 发表载体/文献背景

雅可比的相关工作散见于以下载体：

> C. G. J. Jacobi, "Uber eine neue Auflosungsart der bei der Methode der kleinsten Quadrate vorkommenden linearen Gleichungen", *Astronomische Nachrichten*, 22, 1845, pp. 297--306.

> C. G. J. Jacobi, "Uber ein leichtes Verfahren, die in der Theorie der Sacularstorungen vorkommenden Gleichungen numerisch aufzulosen", *Journal fur die reine und angewandte Mathematik*, 30, 1846, pp. 51--94.

后一篇论文主要涉及对称矩阵的特征值问题（通过旋转消去非对角元素），但其中蕴含的迭代思想与线性方程组的 Jacobi 迭代法一脉相承。

"Jacobi 迭代法"作为求解线性方程组的迭代方法，其系统化表述主要出现在 19 世纪后期和 20 世纪初的数值分析教材和综述文献中。这种方法的命名反映了学术界对雅可比在迭代方法领域先驱地位的认可。

---

## 5. 一句话总结

Jacobi 迭代法将线性方程组 $Ax = b$ 的系数矩阵分裂为对角部分与非对角部分，通过逐步迭代将每个分量的旧值替换为新值，在对角占优等条件下保证收敛到精确解。

---

## 6. 历史背景

### 6.1 线性方程组求解的悠久历史

线性方程组的求解是人类数学活动中最古老的问题之一。中国古代的《九章算术》（约公元 1 世纪）中就包含了使用"方程术"（本质上是消元法）求解联立线性方程组的方法。在欧洲，高斯在 1810 年前后系统化了消元法（Gaussian elimination），使之成为求解线性方程组的标准直接方法。

### 6.2 直接法的局限

然而，直接法在处理大规模方程组时面临严重的计算量问题。对于 $n$ 个未知数的方程组，高斯消元法需要大约 $\frac{2}{3}n^3$ 次算术运算。在没有计算机的 19 世纪，当 $n$ 稍大时（例如 $n = 10$ 或 $n = 20$），直接法的计算量就变得令人望而生畏。

更重要的是，在天文学和大地测量学中，经常需要求解由最小二乘法（method of least squares）产生的法方程组（normal equations）。这些方程组通常具有特殊结构——系数矩阵是对称正定的，且往往具有对角占优（diagonal dominance）或带状结构。利用这些结构特征来简化计算，是迭代方法的重要动机。

### 6.3 迭代法的萌芽

迭代法的基本思想很自然：与其一步到位地求出精确解（这在大规模问题中计算量巨大），不如从一个初始猜测出发，通过反复修正逐步逼近真解。每一步迭代的计算量远小于一次完整的消元，而且迭代过程可以在达到足够精度时随时终止。

雅可比正是在这种背景下提出了他的迭代方法。他的具体动机来自天文学中的摄动理论（perturbation theory）——计算行星轨道的长期摄动需要求解大规模线性方程组，而这些方程组恰好具有对角占优的结构。

### 6.4 计算文化的转变

19 世纪中叶正是数值方法从"手工计算的技巧"向"系统化理论"转变的时期。在此之前，数值方法主要是为了解决具体的计算问题而发明的临时工具。雅可比、高斯等人的工作开始将数值方法提升为具有理论基础的数学分支。

---

## 7. 核心问题定义

### 7.1 基本问题

Jacobi 迭代法试图求解的核心问题是**线性方程组**：

$$Ax = b$$

其中 $A$ 是 $n \times n$ 的非奇异系数矩阵，$b$ 是已知的 $n$ 维向量，$x$ 是待求的 $n$ 维未知向量。

### 7.2 矩阵分裂

Jacobi 方法的核心思想是将系数矩阵 $A$ 分裂（splitting）为：

$$A = D + L + U$$

其中：
- $D$ 是 $A$ 的**对角部分**（diagonal part），$D = \mathrm{diag}(a_{11}, a_{22}, \ldots, a_{nn})$
- $L$ 是 $A$ 的**严格下三角部分**（strictly lower triangular part）
- $U$ 是 $A$ 的**严格上三角部分**（strictly upper triangular part）

注意这里的 $L$ 和 $U$ 不是 LU 分解中的三角矩阵，而是原矩阵的直接分割。

### 7.3 迭代格式

将 $Ax = b$ 改写为 $Dx = b - (L + U)x$，得到迭代格式：

$$x^{(k+1)} = D^{-1}(b - (L + U)x^{(k)})$$

或者写成分量形式：

$$x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j \neq i} a_{ij} x_j^{(k)} \right), \quad i = 1, 2, \ldots, n$$

**核心问题**：这个迭代什么时候收敛？收敛速度如何？

---

## 8. 主要结论/方法/定理

### 8.1 Jacobi 迭代的算法描述

**算法：Jacobi 迭代法**

输入：系数矩阵 $A$，右端向量 $b$，初始猜测 $x^{(0)}$，收敛容差 $\varepsilon$

```
对 k = 0, 1, 2, ... 执行：
    对 i = 1, 2, ..., n 执行：
        x_i^{(k+1)} = (b_i - sum_{j≠i} a_ij * x_j^{(k)}) / a_ii
    如果 ||x^{(k+1)} - x^{(k)}|| < ε，则停止
输出：近似解 x^{(k+1)}
```

算法的关键特征是：在计算 $x^{(k+1)}$ 的所有分量时，完全使用上一步的旧值 $x^{(k)}$。这意味着所有分量的更新是**同时进行的**（simultaneous），各分量之间没有先后依赖关系。

### 8.2 迭代矩阵与谱半径

Jacobi 迭代可以写成矩阵形式：

$$x^{(k+1)} = B_J x^{(k)} + c_J$$

其中 $B_J = -D^{-1}(L + U) = I - D^{-1}A$ 是 **Jacobi 迭代矩阵**，$c_J = D^{-1}b$。

**定理（收敛的充要条件）**：Jacobi 迭代收敛当且仅当迭代矩阵 $B_J$ 的**谱半径**（spectral radius）$\rho(B_J) < 1$。谱半径定义为 $B_J$ 的所有特征值的模的最大值：

$$\rho(B_J) = \max_{1 \leq i \leq n} |\lambda_i(B_J)|$$

### 8.3 充分条件：对角占优

**定理（对角占优收敛定理）**：如果 $A$ 是**严格对角占优**（strictly diagonally dominant）的，即

$$|a_{ii}| > \sum_{j \neq i} |a_{ij}|, \quad \forall i = 1, 2, \ldots, n$$

则 Jacobi 迭代对任意初始值 $x^{(0)}$ 收敛。

直觉理解：对角占优意味着每个方程中，对角元素（主系数）远大于非对角元素之和。这意味着每个方程主要由一个未知数主导，迭代自然能够逐步收敛。

### 8.4 另一个充分条件：正定对称

**定理**：如果 $A$ 是对称正定的（symmetric positive definite），且 $2D - A$ 也是正定的（这等价于 $A$ 的对角元素"足够大"），则 Jacobi 迭代收敛。

### 8.5 收敛速度

Jacobi 迭代的**渐近收敛速率**（asymptotic rate of convergence）为：

$$R = -\log_{10} \rho(B_J)$$

每次迭代使误差大约减小为原来的 $\rho(B_J)$ 倍。当 $\rho(B_J)$ 接近 1 时，收敛非常缓慢；当 $\rho(B_J)$ 接近 0 时，收敛很快。

**误差估计**：

$$\|x^{(k)} - x^*\| \leq \rho(B_J)^k \|x^{(0)} - x^*\|$$

其中 $x^*$ 是真解。因此，要将误差减小到初始误差的 $10^{-p}$ 倍，大约需要 $k \approx p / R$ 次迭代。

### 8.6 加权 Jacobi 方法

在原始 Jacobi 方法的基础上，可以引入松弛参数 $\omega$：

$$x^{(k+1)} = (1 - \omega) x^{(k)} + \omega D^{-1}(b - (L + U)x^{(k)})$$

当 $\omega = 1$ 时退化为原始 Jacobi 方法。适当选择 $\omega$ 可以加速收敛。这为后来的 SOR（逐次超松弛）方法的发展埋下了伏笔。

---

## 9. 核心思想的直觉解释

### 9.1 "分而治之"的朴素思想

Jacobi 迭代法的核心直觉极为朴素：如果每个方程中，对角元素远大于其他系数，那么每个方程几乎可以独立地确定一个未知数。

考虑方程组：

$$10x_1 + x_2 + x_3 = 12$$
$$x_1 + 10x_2 + x_3 = 12$$
$$x_1 + x_2 + 10x_3 = 12$$

由于对角元素 10 远大于非对角元素 1，每个方程基本上由一个未知数主导。如果我们暂时忽略非对角项，可以得到粗略估计 $x_i \approx 12/10 = 1.2$。将这个估计代回去修正，可以得到更好的估计。反复迭代，就能逐步逼近真解 $x_1 = x_2 = x_3 = 1$。

### 9.2 "同时修正"的并行思想

Jacobi 方法的另一个重要特征是所有分量的**同时更新**。在计算 $x_i^{(k+1)}$ 时，使用的全部是上一步的旧值 $x_j^{(k)}$（$j \neq i$），而不是已经计算出的新值。

这一特征在 19 世纪看来或许只是一个自然选择，但在计算机时代，它获得了全新的意义——Jacobi 迭代天然适合**并行计算**（parallel computing）。每个分量的更新是独立的，可以分配给不同的处理器同时计算。

相比之下，Gauss-Seidel 方法虽然通常收敛更快（因为它立即使用最新的计算结果），但其顺序依赖性使得并行化更加困难。

### 9.3 不动点迭代的视角

从更抽象的角度看，Jacobi 迭代是一种**不动点迭代**（fixed-point iteration）。将方程 $Ax = b$ 改写为 $x = D^{-1}(b - (L+U)x) = g(x)$，Jacobi 迭代就是 $x^{(k+1)} = g(x^{(k)})$。

收敛的条件是映射 $g$ 是**压缩映射**（contraction mapping），即 $g$ 使点之间的距离缩小。在线性情形下，这等价于迭代矩阵的谱半径小于 1。

### 9.4 一个生活化的类比

想象一群人在合租一套公寓，他们需要协商每个人每月应该支付多少房租。每个人的房租取决于其他人的房租（例如，根据房间大小、使用面积等因素）。

**Jacobi 方法**相当于：每个人根据上一轮其他人报出的金额来计算自己这一轮应该支付的金额，然后所有人**同时**公布新金额。经过多轮这样的调整，最终会稳定在一个公平的分配方案上。

**Gauss-Seidel 方法**则相当于：按某个顺序逐个计算——第一个人先计算并公布自己的新金额，第二个人看到第一个人的新金额后再计算自己的，以此类推。

Jacobi 方法更"民主"（同时更新），Gauss-Seidel 方法更"高效"（利用最新信息），但 Jacobi 方法的同时性使得它更容易并行化。

---

## 10. 为什么这篇文献重要

### 10.1 迭代法范式的开创

Jacobi 迭代法的最大意义不在于方法本身的效率（事实上，后来的 Gauss-Seidel 方法和 SOR 方法在收敛速度上通常优于 Jacobi 方法），而在于它开创了**迭代求解线性方程组**的整个范式。

在 Jacobi 之前，线性方程组的求解几乎完全依赖直接法（如高斯消元）。Jacobi 方法表明：我们可以从一个猜测出发，通过简单的迭代过程逐步逼近真解。这一思想转变为后来整个迭代线性代数的发展奠定了基础。

### 10.2 矩阵分裂理论的源头

Jacobi 方法引入的矩阵分裂思想——将系数矩阵 $A$ 分解为 $A = M - N$，然后迭代 $Mx^{(k+1)} = Nx^{(k)} + b$——后来发展成为**矩阵分裂理论**（matrix splitting theory），成为分析各种迭代方法收敛性的统一框架。

Richard Varga 在 1962 年的经典专著 *Matrix Iterative Analysis* 中系统化了这一理论。

### 10.3 谱半径判据的先驱

Jacobi 迭代的收敛分析引出了**谱半径**（spectral radius）作为迭代方法收敛性判据的概念。谱半径 $\rho(B) < 1$ 作为迭代 $x^{(k+1)} = Bx^{(k)} + c$ 收敛的充要条件，是整个迭代方法理论的基石。

### 10.4 并行计算的先声

虽然 Jacobi 本人无法预见计算机的出现，但他方法中的"同时更新"特征使其成为并行计算时代最自然的线性方程组求解器之一。在现代超级计算机和 GPU 计算中，Jacobi 迭代及其变体因其天然的并行性而重获青睐。

---

## 11. 它解决了当时什么瓶颈

### 11.1 大规模方程组的计算瓶颈

19 世纪天文学和大地测量学中经常需要求解较大规模的线性方程组（在那个时代，$n = 10 \sim 20$ 就算"大规模"）。高斯消元法的 $O(n^3)$ 计算量在没有计算机的条件下是巨大的负担。

Jacobi 迭代法为这类问题提供了另一条路径：每次迭代的计算量仅为 $O(n^2)$（矩阵-向量乘法），如果矩阵稀疏则更少。对于对角占优的方程组，通常只需几次迭代就能达到足够的精度。

### 11.2 最小二乘法的法方程

高斯在天文学中广泛使用最小二乘法，由此产生的法方程组 $A^T A x = A^T b$ 具有对称正定的结构。雅可比的迭代方法正是为了高效求解这类结构化方程组而发展的。

### 11.3 摄动理论中的特征值问题

雅可比的另一个重要动机是天文学中的行星轨道摄动问题。这些问题最终归结为实对称矩阵的特征值计算。雅可比为此发展了"Jacobi 旋转法"（Jacobi eigenvalue algorithm），这是一种通过正交相似变换逐步对角化矩阵的迭代方法。虽然这是特征值问题而非线性方程组问题，但其迭代思想与 Jacobi 迭代法是一致的。

---

## 12. 它与前人工作的关系

### 12.1 高斯消元法的互补

雅可比的迭代方法与高斯的直接法形成了互补关系。高斯消元法提供精确解（在精确算术下），但计算量大；Jacobi 迭代法提供近似解，但每步计算量小，且可以在达到足够精度时提前终止。

这两种方法代表了求解线性方程组的两大哲学流派——直接法和迭代法——至今仍然并行发展。

### 12.2 与高斯-赛德尔方法的关系

几乎在 Jacobi 提出同时位移法的同时期，菲利普·路德维希·冯·赛德尔（Philipp Ludwig von Seidel, 1821--1896）在 1874 年提出了**逐次位移法**（method of successive displacements），即今天所称的 **Gauss-Seidel 方法**。

Gauss-Seidel 方法的迭代格式为：

$$x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j < i} a_{ij} x_j^{(k+1)} - \sum_{j > i} a_{ij} x_j^{(k)} \right)$$

与 Jacobi 方法的关键区别是：计算 $x_i^{(k+1)}$ 时，对于已经更新过的分量 $x_j^{(k+1)}$（$j < i$），使用最新值而非旧值。

Gauss-Seidel 方法通常比 Jacobi 方法收敛更快（当两者都收敛时），但其顺序依赖性使得并行化更加困难。两种方法的比较成为了迭代方法理论的经典话题。

需要指出的是，虽然 Gauss-Seidel 方法以高斯和赛德尔的名字命名，但高斯本人是否明确使用过这种迭代法存在学术争议。一些历史学家认为高斯在私人计算中可能使用过类似的方法，但没有明确的文献记录。

### 12.3 牛顿迭代法的线性化

从更广的视角看，Jacobi 迭代可以被视为牛顿迭代法（Newton's method）在线性问题上的特例。牛顿法的每步迭代需要求解一个线性方程组；如果这个线性方程组就是原问题本身（即问题已经是线性的），并且用一种特殊的近似方法（只取对角部分）来求解，就得到了 Jacobi 迭代。

---

## 13. 它对后续哪些方向产生了影响

### 13.1 Gauss-Seidel 方法与 SOR

Jacobi 方法最直接的后继者是 Gauss-Seidel 方法和**逐次超松弛法**（Successive Over-Relaxation, SOR）。SOR 方法由 David M. Young 在 1950 年的博士论文中提出，他证明了对于特定结构的矩阵（如离散化 Laplacian），存在最优的松弛参数 $\omega_{\text{opt}}$ 使收敛速度最大化。

Young 的工作可以被视为 Jacobi 迭代思想的一个深远发展。他的 *Iterative Solution of Large Linear Systems*（1971）是这一领域的经典专著。

### 13.2 块 Jacobi 方法与区域分解

将 Jacobi 方法中的标量分量推广为向量"块"，就得到**块 Jacobi 方法**（block Jacobi method）。在区域分解方法（domain decomposition methods）中，块 Jacobi 方法的思想被广泛采用——将计算域分割为多个子域，在每个子域上独立求解，然后交换边界信息，迭代至收敛。

这一思想在现代并行有限元分析中扮演着核心角色。

### 13.3 Krylov 子空间方法

虽然 Krylov 子空间方法（如共轭梯度法 CG、GMRES 等）在思路上与经典迭代法有本质区别，但它们的**预条件**（preconditioning）技术经常使用 Jacobi 分裂作为基础。

**Jacobi 预条件**（即 $M = D$）是最简单的预条件器，但在许多实际问题中效果出乎意料地好，尤其是当对角元素变化较大时。块 Jacobi 预条件、不完全分解预条件等更精细的技术都可以追溯到 Jacobi 分裂的思想。

### 13.4 多重网格方法

在多重网格方法（multigrid methods）中，Jacobi 迭代（及其加权变体）被广泛用作**光滑子**（smoother）。多重网格方法的核心思想是用粗网格校正来消除低频误差，用 Jacobi 或 Gauss-Seidel 迭代来消除高频误差。这种组合可以达到 $O(n)$ 的最优算法复杂度。

Jacobi 光滑子因其并行友好性，在现代高性能多重网格实现中特别受欢迎。

### 13.5 GPU 计算与并行求解器

在 GPU 计算时代，Jacobi 迭代因其天然的并行性而重新成为热门研究对象。GPU 拥有大量并行处理核心，非常适合执行 Jacobi 方法中的同时更新操作。

现代 GPU 稀疏线性代数库（如 NVIDIA 的 AmgX、cuSPARSE 等）中，Jacobi 迭代和加权 Jacobi 方法是核心组件之一。

### 13.6 异步迭代与分布式计算

经典 Jacobi 方法是**同步**的——所有分量同时从第 $k$ 步推进到第 $k+1$ 步。在分布式计算环境中，**异步 Jacobi 方法**（asynchronous Jacobi method）允许不同处理器使用不同"年代"的数据进行更新，避免了同步等待的开销。Chazan 和 Miranker（1969）证明了在一定条件下异步迭代仍然收敛。

### 13.7 对教材和课程体系的影响

Jacobi 迭代法在几乎所有数值分析教材中都占有重要位置。它通常是教科书中介绍的第一种迭代方法，因为其思想简单、分析透明。学生通过学习 Jacobi 方法，可以掌握迭代方法的基本概念——迭代矩阵、谱半径、收敛条件——这些概念构成了理解更复杂方法的基础。

---

## 14. 今天回看它的价值

### 14.1 概念的持久重要性

在今天的数值分析中，Jacobi 迭代法本身可能不再是高效求解大规模线性方程组的首选方法——它通常被 Krylov 子空间方法（如 CG、GMRES、BiCGSTAB）和多重网格方法所取代。然而，Jacobi 方法中的核心概念——矩阵分裂、谱半径判据、迭代收敛分析——仍然是理解所有迭代方法的基础。

### 14.2 并行计算中的复兴

如前所述，Jacobi 方法在并行计算时代获得了新生。在 GPU 和众核处理器（如 Intel Xeon Phi）上，Jacobi 方法的同时更新特性使其成为天然的并行算法。许多现代并行预条件器和光滑子都基于 Jacobi 分裂。

### 14.3 作为基准和教学工具

Jacobi 方法是评估新迭代方法的标准基准（benchmark）。任何新提出的迭代方法都需要与 Jacobi 方法（以及 Gauss-Seidel 方法）进行比较，以证明其优越性。

在教学中，Jacobi 方法是引入迭代思维的最佳切入点。它的简单性使得学生可以专注于迭代方法的核心概念，而不被复杂的算法细节所干扰。

### 14.4 在特定应用中的持续使用

在某些特定应用中，Jacobi 方法仍然是首选：

- **图像处理**：某些图像去噪和修复算法中使用 Jacobi 迭代
- **电路仿真**：大规模电路网络的直流分析
- **并行有限元**：作为区域分解预条件器的组成部分
- **机器学习**：某些优化算法的坐标下降（coordinate descent）变体与 Jacobi/Gauss-Seidel 有概念上的联系

---

## 15. 面向普通读者的通俗解释

### 15.1 一个调温的故事

想象你住在一栋楼里，每个房间都有一个独立的温控器。你的目标是让所有房间达到各自的目标温度。但是，房间之间有热传导——相邻房间的温度会互相影响。

**问题**：如何调节每个房间的温控器，使得所有房间同时达到目标温度？

**直接法**（高斯消元）相当于：列出所有房间温度之间的关系方程，一次性求解出每个温控器的设定值。如果房间数量多，这个计算量非常大。

**Jacobi 迭代法**相当于：
1. 先给每个温控器设一个初始值
2. 查看当前各房间的实际温度与目标的差距
3. 每个房间**独立地**调整自己的温控器（根据自己和邻居的当前温度）
4. 等一段时间让温度稳定
5. 重复步骤 2--4，直到所有房间都接近目标温度

关键点：步骤 3 中，每个房间是**同时、独立地**调整的。这就是 Jacobi 方法的"同时位移"特性。

### 15.2 为什么它能收敛

Jacobi 方法能收敛的条件是**对角占优**——每个房间自身的温控能力远大于邻居的影响。如果你自己房间的空调远比邻居对你的热影响强大，那么你自己的调整就能有效地让温度接近目标，邻居的影响只是小扰动。

如果邻居的影响太大（即矩阵不对角占优），Jacobi 方法可能不收敛——就像你怎么调空调也抵不过邻居的热量入侵。

### 15.3 与 Gauss-Seidel 方法的对比

继续上面的比喻。如果改为 Gauss-Seidel 方法：

1. 先调第 1 个房间的温控器
2. **立即**使用第 1 个房间的新温度来调第 2 个房间
3. 使用第 1、2 个房间的新温度来调第 3 个房间
4. 以此类推...

Gauss-Seidel 方法通常更快收敛（因为它使用了最新信息），但它有一个缺点：必须按顺序进行。在只有一个维修工的情况下这没问题，但如果你有多个维修工可以同时工作，Jacobi 方法就更高效了——每个维修工负责一个房间，大家同时调节。

这就是为什么 Jacobi 方法在现代并行计算中重新变得重要。

---

## 16. 阅读原文建议

### 16.1 原始文献

雅可比的原始论文以德文撰写，现代读者可能需要克服语言和符号障碍：

> C. G. J. Jacobi, "Uber eine neue Auflosungsart der bei der Methode der kleinsten Quadrate vorkommenden linearen Gleichungen", *Astronomische Nachrichten*, 22, 1845.

这篇论文的标题翻译为"关于最小二乘法中出现的线性方程组的一种新解法"，从标题即可看出雅可比的动机来自最小二乘法的应用。

### 16.2 推荐学习路径

1. **入门级**：从任何数值分析教材的"迭代方法"章节开始
   - Burden & Faires, *Numerical Analysis*, Chapter 7
   - Kincaid & Cheney, *Numerical Analysis*, Chapter 8

2. **中级**：系统学习迭代方法理论
   - Richard S. Varga, *Matrix Iterative Analysis*, 2nd ed., Springer, 2000
   - David M. Young, *Iterative Solution of Large Linear Systems*, Academic Press, 1971

3. **高级**：深入研究现代迭代方法与预条件技术
   - Yousef Saad, *Iterative Methods for Sparse Linear Systems*, 2nd ed., SIAM, 2003
   - Anne Greenbaum, *Iterative Methods for Solving Linear Systems*, SIAM, 1997

### 16.3 阅读重点

阅读 Jacobi 迭代相关文献时，建议特别关注：

- **谱半径**与收敛速度的关系——这是所有迭代方法分析的核心工具
- **对角占优**条件的实际意义——哪些实际问题会产生对角占优矩阵
- **Jacobi 与 Gauss-Seidel 的比较**——何时一种方法优于另一种
- **块方法的推广**——如何将标量迭代推广到块迭代
- **异步迭代**的收敛理论——现代并行计算中的重要话题

---

## 17. 局限性/历史局限

### 17.1 收敛速度慢

Jacobi 迭代的主要局限是收敛速度通常较慢，特别是对于来自偏微分方程离散化的大规模方程组。例如，对于 $n \times n$ 网格上的 Laplace 方程离散化，Jacobi 迭代的谱半径为 $\rho(B_J) = \cos(\pi/n) \approx 1 - \pi^2/(2n^2)$，这意味着将误差减小一个数量级大约需要 $O(n^2)$ 次迭代。

对比之下，SOR 方法在最优松弛参数下的谱半径为 $\rho(B_{\text{SOR}}) \approx 1 - 2\pi/n$，收敛速度快得多。共轭梯度法的迭代次数为 $O(n)$，多重网格法仅需 $O(1)$ 次迭代（即与问题规模无关）。

### 17.2 收敛条件的限制

Jacobi 迭代并非对所有非奇异线性方程组都收敛。对于不具有对角占优或其他特殊结构的矩阵，Jacobi 迭代可能发散。这限制了它的通用性。

### 17.3 不利用最新信息

与 Gauss-Seidel 方法相比，Jacobi 方法不利用最新计算出的分量值，这在串行计算环境中是一种浪费。每次迭代使用的信息"过时"了一步。

### 17.4 存储需求

Jacobi 方法需要同时存储旧的和新的迭代向量（$x^{(k)}$ 和 $x^{(k+1)}$），而 Gauss-Seidel 方法可以原地更新（in-place update），只需一份存储空间。对于非常大的问题，这个额外的存储开销可能是一个考虑因素。

### 17.5 历史文献的分散性

雅可比并没有在一篇系统的论文中完整阐述"Jacobi 迭代法"。他的相关思想散见于多篇论文和讲义中，且主要关注的是特征值问题而非线性方程组。"Jacobi 迭代法"这个名称更多是后人的总结和归纳。这使得追溯方法的确切起源变得困难。

### 17.6 理论的后置性

雅可比提出迭代方法时，矩阵理论和泛函分析尚未完全发展。谱半径、矩阵范数等概念要到 19 世纪后期和 20 世纪初才被严格定义。因此，Jacobi 方法的严格收敛理论是由后来的数学家（特别是 Perron、Frobenius、Varga 等人）建立的。

---

## 18. 延伸阅读建议

### 18.1 经典专著

1. **Richard S. Varga**, *Matrix Iterative Analysis*, 2nd revised and expanded edition, Springer, 2000.
   - 迭代方法理论的经典之作，系统阐述了矩阵分裂理论、谱半径判据和 SOR 理论。第一版于 1962 年出版，对迭代方法的理论发展产生了深远影响。

2. **David M. Young**, *Iterative Solution of Large Linear Systems*, Academic Press, 1971.
   - Young 的博士论文（1950）发展了 SOR 理论，这部专著是其成果的系统化总结。

3. **Yousef Saad**, *Iterative Methods for Sparse Linear Systems*, 2nd ed., SIAM, 2003.
   - 现代迭代方法的权威教材，覆盖了从经典迭代法到 Krylov 方法和预条件技术的完整内容。可在作者网站免费获取。

### 18.2 综述与历史研究

4. **Gene H. Golub & Charles F. Van Loan**, *Matrix Computations*, 4th ed., Johns Hopkins University Press, 2013.
   - 矩阵计算领域的圣经，第 11 章详细讨论了迭代方法。

5. **G. W. Stewart**, "The Decompositional Approach to Matrix Computation", *Computing in Science & Engineering*, 2(1), 2000.
   - 矩阵分解思想的历史综述，提供了理解 Jacobi 方法在更大背景中的位置的视角。

### 18.3 并行计算相关

6. **Andreas Frommer & Daniel B. Szyld**, "On Asynchronous Iterations", *Journal of Computational and Applied Mathematics*, 123, 2000, pp. 201--216.
   - 异步迭代方法的综述，包括异步 Jacobi 方法的收敛理论。

7. **Jack Dongarra et al.**, "High-Performance Computing: Clusters, Constellations, MPPs, and Future Directions", *Computing in Science & Engineering*, 7(2), 2005.

### 18.4 现代应用

8. **William L. Briggs, Van Emden Henson, & Steve F. McCormick**, *A Multigrid Tutorial*, 2nd ed., SIAM, 2000.
   - 多重网格方法教程，详细讨论了 Jacobi 光滑子在多重网格中的应用。

9. **Maxim Naumov et al.**, "AmgX: A Library for GPU Accelerated Algebraic Multigrid and Preconditioned Iterative Methods", *SIAM Journal on Scientific Computing*, 37(5), 2015.
   - NVIDIA 的 GPU 加速代数多重网格库，其中 Jacobi 迭代是核心组件。

---

## 19. 参考资料/实际引用文档

1. Jacobi, C. G. J. (1845). "Uber eine neue Auflosungsart der bei der Methode der kleinsten Quadrate vorkommenden linearen Gleichungen." *Astronomische Nachrichten*, 22, 297--306.

2. Jacobi, C. G. J. (1846). "Uber ein leichtes Verfahren, die in der Theorie der Sacularstorungen vorkommenden Gleichungen numerisch aufzulosen." *Journal fur die reine und angewandte Mathematik*, 30, 51--94.

3. Seidel, P. L. von (1874). "Uber ein Verfahren, die Gleichungen, auf welche die Methode der kleinsten Quadrate fuhrt, sowie lineare Gleichungen uberhaupt, durch successive Annaherung aufzulosen." *Abhandlungen der Bayerischen Akademie der Wissenschaften*, 11(3), 81--108.

4. Young, D. M. (1950). *Iterative Methods for Solving Partial Difference Equations of Elliptic Type*. PhD thesis, Harvard University.

5. Young, D. M. (1971). *Iterative Solution of Large Linear Systems*. Academic Press.

6. Varga, R. S. (1962). *Matrix Iterative Analysis*. Prentice-Hall. (2nd ed., Springer, 2000.)

7. Saad, Y. (2003). *Iterative Methods for Sparse Linear Systems*, 2nd ed. SIAM.

8. Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations*, 4th ed. Johns Hopkins University Press.

9. Chazan, D., & Miranker, W. (1969). "Chaotic Relaxation." *Linear Algebra and Its Applications*, 2(2), 199--222.

10. Frommer, A., & Szyld, D. B. (2000). "On Asynchronous Iterations." *Journal of Computational and Applied Mathematics*, 123(1--2), 201--216.

11. Briggs, W. L., Henson, V. E., & McCormick, S. F. (2000). *A Multigrid Tutorial*, 2nd ed. SIAM.

12. Greenbaum, A. (1997). *Iterative Methods for Solving Linear Systems*. SIAM.

13. Burden, R. L., & Faires, J. D. (2015). *Numerical Analysis*, 10th ed. Cengage Learning.

14. Stoer, J., & Bulirsch, R. (2002). *Introduction to Numerical Analysis*, 3rd ed. Springer.

---

**注**：本文旨在以学术严谨但通俗易懂的方式介绍 Jacobi 迭代法的历史、理论和影响。关于雅可比原始工作的确切内容和动机，学术界存在不同解读。文中采用了主流学术史的观点，但也指出了存在争议之处。"Jacobi 迭代法"的命名是后人对其方法的总结性称谓，这在 19 世纪数学史中是常见的现象。所有引用文献均为实际存在的出版物。
