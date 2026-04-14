# Hoffman--Wielandt 定理（1953）：正规矩阵特征值扰动的最优估计

## 作者

**Alan J. Hoffman**（1924--2021）与 **Helmut W. Wielandt**（1910--2001）

## 发表时间与刊物

1953 年发表于 *Duke Mathematical Journal*，第 20 卷，第 37--39 页。论文题为 *"The variation of the spectrum of a normal matrix"*。全文仅三页，却成为矩阵扰动理论中被引用最广泛的经典之一。

## 一句话概括

对于两个正规矩阵 A 与 B，其特征值在最优配对下的平方距离之和不超过矩阵差 A - B 的 Frobenius 范数的平方，从而为正规矩阵的特征值整体扰动给出了最优且不可改进的估计。

---

## 一、历史背景

二十世纪五十年代是数值线性代数学科孕育和成形的关键时期。第二次世界大战期间及战后，电子计算机的出现使大规模矩阵计算从纯理论设想变为工程实践。在此之前，矩阵特征值的计算主要依赖手工方法和小规模案例。然而，随着 ENIAC（1945）和后续计算机的投入使用，工程师和物理学家开始面临一个迫切的问题：当矩阵的元素因测量误差、数值截断或物理扰动而发生微小变化时，其特征值会发生多大的偏移？这一问题的精确回答，对于结构力学中的振动分析、量子力学中的能级计算以及控制理论中的稳定性判断都至关重要。

在此之前，Hermann Weyl 于 1912 年在研究线性偏微分方程特征值渐近分布时，已经证明了 Hermite 矩阵的逐个特征值扰动不等式：对于两个 n 阶 Hermite 矩阵 A 和 B，按升序排列的特征值满足 |lambda_i(A) - lambda_i(B)| <= ||A - B||_2。这一结果虽然精彩，但它处理的是单个特征值的偏移，并不提供所有特征值整体偏移的最优控制。当矩阵不再是 Hermite 的，而仅仅是正规矩阵（即满足 AA* = A*A 的矩阵）时，特征值可以是复数，此时特征值之间没有自然的排序关系。如何在复平面上找到两组特征值之间的"最优配对"，使得配对距离之和最小，这本身就是一个非平凡的组合优化问题。

正是在这一时代背景下，两位来自不同学术传统的数学家展开了合作。Alan J. Hoffman 于 1950 年在 Garrett Birkhoff 指导下从哥伦比亚大学获得博士学位，随后在普林斯顿高等研究院做博士后研究，之后加入美国国家标准局应用数学部门，后转入 IBM Watson 研究中心。他的研究兴趣涵盖线性规划、组合优化和矩阵理论，是 *Linear Algebra and its Applications* 期刊的创刊主编。Helmut Wielandt 则是德国数学家，1935 年在柏林大学获得博士学位，师从 Issai Schur 的学术圈。他在置换群理论方面成就卓著，同时也对矩阵分析做出了深刻贡献。战争期间，Wielandt 从事气象学、密码学和空气动力学相关的数值研究，其中涉及的振动问题使他接触到特征值的数值计算，他后来回忆说，这些经历让他认识到"抽象工具在解决具体问题中的适用性"以及"数值计算中意想不到的困难和非同寻常的责任"。战后，他先后在美因茨大学和图宾根大学任教。

两位学者的合作结合了 Hoffman 在线性规划和凸组合方面的洞察力与 Wielandt 在矩阵分析方面的深厚功力，催生出了这个仅三页却影响深远的定理。

值得一提的是，五十年代初正是矩阵扰动理论从零散结果走向系统化的转折期。A. M. Ostrowski 在同一时期也在研究矩阵特征值的定位与扰动问题，而 J. H. Wilkinson 则从实际计算出发，逐步建立起舍入误差分析的完整框架。Hoffman--Wielandt 定理的发表恰好处于这一学科蓬勃发展的起点。1960 年 Mirsky 的综述文章对正规矩阵的扰动问题进行了系统梳理，将 Hoffman--Wielandt 定理置于更广阔的理论语境中。到 1965 至 1966 年间，Kato 的《算子扰动理论》和 Wilkinson 的《代数特征值问题》相继出版，标志着矩阵扰动理论进入成熟期，而 Hoffman--Wielandt 定理则作为该领域的基石之一被永久确立。

---

## 二、核心问题

Hoffman--Wielandt 定理所要回答的核心问题可以精确表述如下：

设 A 是一个 n 阶正规矩阵，B = A + E 是对 A 的扰动。A 的特征值为 lambda_1, lambda_2, ..., lambda_n，B 的特征值为 mu_1, mu_2, ..., mu_n（均为复数）。**是否存在特征值之间的一一对应（排列）pi，使得配对后的特征值偏移在某种整体度量下受到矩阵差 E 的有效控制？**

这一问题的难度在于三个层面。首先，对于一般正规矩阵，特征值是复数，不存在如实数那样的自然排序，因此必须在 n! 种可能的配对中寻找最优的那一个。其次，我们需要的不是单个特征值的偏移估计，而是所有特征值偏移的整体估计，这需要选择合适的"整体度量"。最后，我们希望所得到的界是最优的（tight），即存在使等号成立的情形，否则估计就不具有根本性意义。

---

## 三、主要定理与结果

**定理（Hoffman--Wielandt, 1953）.** 设 A 和 B 是两个 n 阶正规矩阵，A 的特征值为 lambda_1, ..., lambda_n，B 的特征值为 mu_1, ..., mu_n。则存在 {1, 2, ..., n} 上的排列 pi，使得

$$\sum_{i=1}^{n} |\lambda_i - \mu_{\pi(i)}|^2 \leq \|A - B\|_F^2$$

其中 ||*||_F 表示 Frobenius 范数，定义为 ||M||_F = (Tr(M*M))^{1/2}。

等价地，该定理可以写成最小化形式：

$$\min_{\pi \in S_n} \sum_{i=1}^{n} |\lambda_i - \mu_{\pi(i)}|^2 \leq \|A - B\|_F^2$$

其中 S_n 是 n 元对称群（即所有排列的集合）。

**等号成立的条件：** 当且仅当 A 和 B 可以被同一酉矩阵同时对角化时，即 A 和 B 交换（AB = BA）时，等号成立。此时两个矩阵共享一组公共的特征向量基底，扰动矩阵 E = B - A 在公共特征基下也是对角的，Frobenius 范数恰好等于特征值差的平方和。

**特殊情形：** 当 A 和 B 都是 Hermite 矩阵时，特征值都是实数，可以按升序排列。此时自然排列（即 pi 为恒等排列）就是最优配对，定理退化为

$$\sum_{i=1}^{n} (\lambda_i - \mu_i)^2 \leq \|A - B\|_F^2$$

这给出了 Weyl 不等式的一个整体加强版本。

---

## 四、核心方法

Hoffman 和 Wielandt 的证明以其精炼和优雅著称，仅用三页便完成了全部论证。其核心方法可以分解为以下几个关键步骤：

**第一步：酉对角化。** 由于 A 和 B 都是正规矩阵，存在酉矩阵 U 和 V，使得 A = U * diag(lambda_1, ..., lambda_n) * U* 以及 B = V * diag(mu_1, ..., mu_n) * V*。这里 diag 表示对角矩阵，U* 表示 U 的共轭转置。

**第二步：Frobenius 范数的酉不变性。** Frobenius 范数满足 ||M||_F = ||UMV||_F 对任意酉矩阵 U, V 成立。利用这一性质，将 ||A - B||_F^2 展开后，可以将问题转化为涉及酉矩阵 W = U*V 的表达式。

**第三步：构造双随机矩阵。** 定义矩阵 S，其元素为 S_{ij} = |W_{ij}|^2。由于 W 是酉矩阵，其行和列的模平方和均为 1，因此 S 是一个双随机矩阵（doubly stochastic matrix），即所有元素非负，且每行每列之和为 1。展开后得到

$$\|A - B\|_F^2 = \sum_{i,j} S_{ij} |\lambda_i - \mu_j|^2$$

**第四步：Birkhoff--von Neumann 定理的应用。** 目标函数 Phi(S) = sum_{i,j} S_{ij} * |lambda_i - mu_j|^2 是 S 的线性函数。而全体双随机矩阵构成一个紧凸多面体（Birkhoff 多面体）。根据 Birkhoff--von Neumann 定理，该多面体的顶点恰好是所有置换矩阵。由于线性函数在紧凸集上的最小值必在某个顶点处取得，因此存在一个排列 pi，使得

$$\sum_{i=1}^{n} |\lambda_i - \mu_{\pi(i)}|^2 = \min_{\sigma \in S_n} \sum_{i=1}^{n} |\lambda_i - \mu_{\sigma(i)}|^2 \leq \Phi(S) = \|A - B\|_F^2$$

这一证明的精妙之处在于，它将矩阵扰动理论中的分析问题，通过酉不变性和双随机矩阵的凸几何性质，优雅地转化为组合优化中的匹配问题。Birkhoff--von Neumann 定理本身的证明又依赖于 Hall 婚配定理（即二部图中完美匹配的存在条件），从而在线性代数、凸分析和组合数学之间建立了深刻的联系。

值得注意的是，Hoffman 本人对 Birkhoff--von Neumann 定理（即双随机矩阵的凸包表示）也有独立贡献，这一学术积累为本定理的发现提供了关键灵感。从方法论的角度来看，这一证明开创了"通过凸松弛将离散组合问题化为连续优化问题"的范式，该范式后来成为组合优化和运筹学中的标准技术，影响远超矩阵理论本身。

---

## 五、重要性与影响

Hoffman--Wielandt 定理是矩阵扰动理论中最基本的结果之一，其重要性可以从多个维度加以理解。

首先，它给出的是**最优的**（sharp/tight）估计。等号可以达到这一事实意味着，在正规矩阵的框架内，不可能找到比 Frobenius 范数更紧的整体特征值扰动界。这赋予了该定理以"终极性"——它不仅是一个有用的上界，更是一个精确的刻画。

其次，该定理将**分析问题与组合问题**统一起来。特征值扰动属于矩阵分析（或算子理论）的范畴，而最优配对问题本质上是组合优化中的指派问题（assignment problem）。Hoffman 和 Wielandt 巧妙地利用 Birkhoff--von Neumann 定理搭建了两者之间的桥梁，这种跨领域的联系在此后的数学研究中反复出现。

再次，该定理为**数值特征值算法的误差分析**提供了理论基础。在实际计算中，浮点运算引入的舍入误差相当于对矩阵的微小扰动。Hoffman--Wielandt 不等式保证了，对于正规矩阵，所有计算得到的特征值的整体误差不会超过扰动的 Frobenius 范数，这为 QR 算法等现代特征值算法的后向误差分析提供了核心工具。

最后，该定理在**概率和统计**中也有深远影响。在随机矩阵理论中，它被用于证明经验谱分布的收敛性（如 Wigner 半圆律的证明中的截断论证），因为它保证了矩阵的 Frobenius 范数扰动可以精确控制特征值的整体偏移。

---

## 六、解决了什么瓶颈

在 Hoffman--Wielandt 定理之前，矩阵特征值扰动理论的主要工具是 Weyl 不等式（1912）。Weyl 不等式对 Hermite 矩阵给出了逐个特征值的扰动估计：

$$|\lambda_i(A) - \lambda_i(B)| \leq \|A - B\|_2$$

其中 ||*||_2 是谱范数（即最大奇异值）。这一结果虽然强大，但存在几个局限：

1. **单个 vs. 整体：** Weyl 不等式控制的是每个特征值的偏移，但将所有这些逐个估计简单求和会产生过于粗糙的整体估计。例如，对 n 个不等式平方求和得到 sum |lambda_i - mu_i|^2 <= n * ||E||_2^2，而 Hoffman--Wielandt 给出的是 sum <= ||E||_F^2。由于 ||E||_F^2 <= n * ||E||_2^2，Hoffman--Wielandt 不等式严格更强。

2. **仅限 Hermite 矩阵：** Weyl 不等式依赖于特征值的实数排序，因此本质上仅适用于 Hermite（或实对称）矩阵。而 Hoffman--Wielandt 定理适用于所有正规矩阵，包括酉矩阵和斜 Hermite 矩阵等特征值为复数的情形。

3. **配对问题：** 对于复特征值，不存在自然排序，Weyl 不等式无法直接推广。Hoffman--Wielandt 定理通过引入最优排列（配对）的概念，巧妙地绕过了排序困难。

因此，Hoffman--Wielandt 定理真正解决的瓶颈是：**如何在 Frobenius 范数的意义下，对正规矩阵的所有特征值给出整体的、最优的、与配对无关（通过优化配对实现）的扰动估计。**

---

## 七、与前人工作的关系

Hoffman--Wielandt 定理深深植根于二十世纪前半叶矩阵理论的丰富传统中：

**Hermann Weyl（1912）：** 如前所述，Weyl 的特征值扰动不等式是最早的系统性结果。Hoffman--Wielandt 定理可以视为 Weyl 不等式从"逐点估计"到"整体估计"、从"谱范数"到"Frobenius 范数"、从"Hermite 矩阵"到"正规矩阵"的全面推广。

**John von Neumann（1937）：** von Neumann 的迹不等式指出，对于任意 n 阶复矩阵 A 和 B，其奇异值分别为 alpha_1 >= ... >= alpha_n 和 beta_1 >= ... >= beta_n 时，|Tr(AB)| <= sum_i alpha_i * beta_i。该不等式的证明技术——特别是对酉矩阵的分析和双随机矩阵的使用——与 Hoffman--Wielandt 定理的证明方法一脉相承。

**Garrett Birkhoff（1946）与 von Neumann：** 双随机矩阵的凸包表示定理（即双随机矩阵是置换矩阵的凸组合）是 Hoffman--Wielandt 定理证明的核心工具。Hoffman 作为 Birkhoff 的博士生，自然熟悉这一结果，并将其创造性地应用于特征值扰动问题。

**Wielandt（1950）：** Wielandt 在非负矩阵的 Perron--Frobenius 理论方面给出了新的优雅证明，展示了他在矩阵分析方面的深厚功力。他从非负矩阵理论转向一般矩阵的扰动分析，Hoffman--Wielandt 定理是这一转型的标志性成果。

**V. B. Lidskii（1950）：** Lidskii 在同一时期独立研究了对称矩阵和与积的特征值关系，给出了特征值差的优超（majorization）不等式。Lidskii 不等式可以视为 Weyl 不等式的细化，而 Hoffman--Wielandt 不等式则提供了 Frobenius 范数意义下的另一种整体刻画。这两条路线在后来的矩阵分析中汇合，共同构成了特征值扰动理论的基石。

---

## 八、对后续工作的影响

Hoffman--Wielandt 定理发表后，在多个方向上激发了深入的后续研究：

**Bauer--Fike 定理（1960）：** Friedrich L. Bauer 和 C. T. Fike 将特征值扰动分析从正规矩阵推广到一般可对角化矩阵。他们的定理指出，若 A = V * Lambda * V^{-1}，则 A + E 的每个特征值 mu 至少距某个 lambda_i 不超过 kappa_p(V) * ||E||_p，其中 kappa_p(V) = ||V||_p * ||V^{-1}||_p 是特征向量矩阵的条件数。对于正规矩阵，V 是酉矩阵，kappa(V) = 1，Bauer--Fike 定理退化为经典扰动界。这一工作明确揭示了非正规性（non-normality）对特征值灵敏度的影响。

**Tosio Kato 的算子扰动理论（1966）：** Kato 在其里程碑式的专著 *Perturbation Theory for Linear Operators* 中，将包括 Hoffman--Wielandt 定理在内的有限维矩阵扰动结果系统地推广到无穷维 Hilbert 空间上的算子。Kato 的理论为量子力学中的微扰论提供了严格的数学基础。

**随机矩阵理论：** 在 Wigner、Marchenko--Pastur 等人建立的随机矩阵理论中，Hoffman--Wielandt 不等式是证明经验谱分布收敛的标准工具之一。例如，在证明 Wigner 半圆律时，需要对随机矩阵进行截断和中心化处理，Hoffman--Wielandt 不等式保证了这些操作不会本质改变特征值的整体分布。Anderson、Guionnet 和 Zeitouni 在其经典教材 *An Introduction to Random Matrices* 中将该定理作为基础工具之一加以阐述。

**无穷维推广：** Bhatia 和 Friedland（1994）将 Hoffman--Wielandt 不等式推广到 Hilbert--Schmidt 算子（即迹类算子的推广），证明了类似的特征值配对不等式在无穷维空间中依然成立。

**最优输运理论的联系：** Hoffman--Wielandt 不等式的左端实际上等于两个经验谱测度之间 Wasserstein 距离（2-Wasserstein 距离）的平方乘以 n。这一观察将矩阵扰动理论与最优输运理论联系起来，为后者在谱理论中的应用提供了自然框架。

---

## 九、现代价值

在当代数学与应用科学中，Hoffman--Wielandt 定理继续发挥着核心作用：

**数值线性代数：** 现代特征值算法（如 QR 算法、分治法、Jacobi 方法）的后向误差分析都依赖于 Hoffman--Wielandt 类型的扰动界。算法的数值稳定性证明往往归结为：算法输出的特征值是某个近似矩阵的精确特征值，而该近似矩阵与原矩阵之差的 Frobenius 范数可控。

**统计学中的协方差矩阵估计：** 在高维统计中，样本协方差矩阵是总体协方差矩阵的扰动。Hoffman--Wielandt 不等式为分析样本特征值与总体特征值之间的偏差提供了基本工具，特别是在 spiked covariance model 等框架下。

**机器学习与数据科学：** 谱聚类（spectral clustering）、主成分分析（PCA）和核方法（kernel methods）的稳定性分析都依赖于特征值扰动理论。Hoffman--Wielandt 不等式保证了当数据矩阵受到噪声干扰时，谱方法提取的特征不会发生剧烈跳变，从而为算法的鲁棒性提供了理论保障。

**量子信息与量子计算：** 在量子纠错和量子通道的分析中，密度矩阵（正半定 Hermite 矩阵）的特征值扰动直接关系到保真度（fidelity）和纠缠度量的连续性。Hoffman--Wielandt 不等式在这些量子信息度量的稳定性证明中扮演关键角色。

**网络科学与图谱理论：** 在复杂网络分析中，图的邻接矩阵或拉普拉斯矩阵的特征值编码了网络的拓扑性质（如连通性、社区结构和扩展性）。当网络发生局部扰动（如边的增删）时，Hoffman--Wielandt 不等式可以精确控制谱变化的幅度，从而为动态网络的稳定性分析和社区检测算法的鲁棒性证明提供理论支撑。

**信号处理与系统辨识：** 在自适应滤波和系统辨识领域，待估计的系统矩阵只能通过有噪声的观测数据间接获得。Hoffman--Wielandt 不等式为评估估计矩阵的特征值（即系统极点）与真实系统极点之间的偏差提供了直接工具。特别是在 MUSIC 和 ESPRIT 等基于子空间的方向估计算法中，信号协方差矩阵的特征值分析是核心步骤，该不等式为算法精度的理论分析提供了必要的扰动界。

---

## 十、通俗解读

想象一个有 n 位乘客的航班，每位乘客都有一个指定的座位。现在由于某种原因（比如航空公司系统错误），所有乘客的座位号都发生了变化。问题是：能否重新安排一种对应方式，使得每位乘客从原座位到新座位的"移动距离"的总平方和尽可能小？

Hoffman--Wielandt 定理告诉我们的就是这样一件事。矩阵 A 的特征值是"原始座位"，矩阵 B 的特征值是"新座位"。矩阵差 E = B - A 代表"系统错误的严重程度"（用 Frobenius 范数衡量）。定理保证：无论特征值如何移动，总存在一种"最优重排方式"（即排列 pi），使得所有乘客的总移动距离平方和不超过系统错误的总量。

更直观地说：如果你只是轻轻推了一下矩阵（小扰动），那么特征值整体上也只能轻轻移动一点。不会出现某些特征值突然"飞到天边"的情况——至少在正规矩阵的世界里是如此。

我们还可以用另一个比喻来理解证明中 Birkhoff--von Neumann 定理的角色。假设有 n 位工人和 n 项任务，将工人 i 分配到任务 j 的"代价"为 |lambda_i - mu_j|^2。问题是：如何安排一一对应的分配方案，使得总代价最小？这正是经典的指派问题（assignment problem）。Hoffman--Wielandt 定理的证明表明，通过放松整数约束（允许每位工人以一定比例分配到多项任务），最优解恰好在某个"纯分配方案"（即排列）处取得。这一从连续优化到离散优化的转化，正是 Birkhoff--von Neumann 定理的精髓所在。

这个比喻也帮助我们理解为何该定理不适用于非正规矩阵。在正规矩阵的"航班"中，座椅排列整齐、互不干扰（特征向量正交）；而在非正规矩阵的"航班"中，座椅可能彼此纠缠（特征向量近乎平行），一个微小的推动可能导致连锁反应，使某些"乘客"被弹射到很远的位置。举一个具体的例子：考虑 2 阶 Jordan 块 J = [[0, 1], [0, 0]]，其唯一特征值为 0。但矩阵 J + epsilon * [[0, 0], [1, 0]] 的特征值为正负 sqrt(epsilon)。当 epsilon 很小时，sqrt(epsilon) 远大于 epsilon，这就是非正规性导致的特征值"放大效应"。

---

## 十一、阅读指南

对于希望深入理解 Hoffman--Wielandt 定理的读者，建议按以下路径阅读：

**入门阶段：**
- 首先阅读 Roger A. Horn 和 Charles R. Johnson 的 *Matrix Analysis*（第二版，2013），该书第 6 章系统介绍了特征值扰动理论，并以清晰的方式呈现了 Hoffman--Wielandt 定理。
- 同时可参考 G. W. Stewart 和 Ji-guang Sun 的 *Matrix Perturbation Theory*（1990），该书从数值分析的角度系统梳理了矩阵扰动结果。

**进阶阶段：**
- Rajendra Bhatia 的 *Matrix Analysis*（1997，Springer GTM 169）是这一领域的权威专著，深入探讨了特征值扰动的各种推广和变体，并将其置于优超理论（majorization）的统一框架下。
- 阅读原始论文：Hoffman 和 Wielandt 的三页论文语言简洁、论证精炼，是数学写作的典范，非常值得细读。

**进阶阶段（补充）：**
- 原始论文可以通过 Project Euclid 在线获取（https://projecteuclid.org/euclid.dmj/1077465066）。建议在阅读教科书版本后再回到原文，体会 Hoffman 和 Wielandt 如何用最少的篇幅完成最精炼的论证。
- 对于希望了解双随机矩阵和 Birkhoff--von Neumann 定理背景的读者，Marshall、Olkin 和 Arnold 合著的 *Inequalities: Theory of Majorization and Its Applications*（第二版，2011）提供了全面的参考。

**拓展阶段：**
- Terence Tao 在 UCLA 254A 课程讲义中对 Weyl 不等式、Lidskii 不等式和 Hoffman--Wielandt 不等式进行了统一而现代的处理，特别是展示了这些结果与 Courant--Fischer 极小极大原理之间的深刻联系。
- 对于随机矩阵方向的应用，推荐 Anderson、Guionnet 和 Zeitouni 的 *An Introduction to Random Matrices*（2010），其中定理 2.1.19 即为 Hoffman--Wielandt 不等式，在后续章节的谱收敛证明中被反复使用。
- 对于非正规矩阵扰动理论的进一步探索，推荐 Trefethen 和 Embree 的 *Spectra and Pseudospectra*（2005），该书深入讨论了伪谱的概念如何弥补经典特征值扰动理论在非正规情形下的不足。

---

## 十二、局限性

尽管 Hoffman--Wielandt 定理影响深远，但它有明确的适用边界：

**正规性假设是本质性的。** 该定理要求两个矩阵都是正规矩阵。对于非正规矩阵（如 Jordan 块、亏损矩阵），特征值可以对扰动极其敏感。经典的反例是 n 阶 Jordan 块 J_n：一个大小为 epsilon 的扰动可以导致特征值偏移 epsilon^{1/n}，远大于 epsilon 本身。在这种情况下，需要使用 Bauer--Fike 定理（涉及特征向量矩阵的条件数）或伪谱（pseudospectra）等更精细的工具。

**仅给出整体估计。** Hoffman--Wielandt 不等式控制的是所有特征值偏移的 l^2 范数（Frobenius 意义），但不直接给出单个特征值的偏移控制。对于单个特征值的最坏情形估计，Weyl 不等式或 Bauer--Fike 定理可能更为适用。

**不提供配对的具体构造。** 定理保证最优排列的存在性，但不提供高效算法来找到这个排列。实际上，最优配对问题是一个指派问题，可以用匈牙利算法（Hungarian algorithm）在 O(n^3) 时间内求解，但定理本身并不涉及算法层面。

**对非方阵和广义特征值问题不直接适用。** 矩形矩阵的奇异值扰动和广义特征值问题的扰动需要单独的理论处理，尽管 Hoffman--Wielandt 思想可以（并已经）被推广到这些情形。

**不反映特征向量的扰动。** 该定理仅涉及特征值的偏移，对特征向量（或不变子空间）的扰动不提供任何信息。特征向量的扰动分析需要 Davis--Kahan 正弦定理等专门工具，后者给出了不变子空间之间夹角的扰动界。在许多应用中（如主成分分析和谱聚类），特征向量的稳定性往往比特征值的稳定性更为关键，此时仅依赖 Hoffman--Wielandt 定理是不够的。

**范数的限制。** Hoffman--Wielandt 不等式选用 Frobenius 范数（即 l^2 范数）来度量特征值的整体偏移。对于其他范数（如 l^1 范数或 l^infinity 范数），需要不同的工具。例如，Weyl 不等式给出的是 l^infinity 范数（逐个特征值最大偏移）的控制，而 Lidskii 不等式则提供了更精细的优超关系。不同的应用场景可能需要不同范数下的扰动界。

---

## 十三、延伸阅读

1. **Weyl, H.** (1912). Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen. *Mathematische Annalen*, 71(4), 441--479. [特征值扰动理论的先驱工作]

2. **Bauer, F. L. & Fike, C. T.** (1960). Norms and exclusion theorems. *Numerische Mathematik*, 2(1), 137--141. [将扰动分析推广到非正规可对角化矩阵]

3. **Kato, T.** (1966). *Perturbation Theory for Linear Operators*. Springer. [将有限维扰动理论系统推广到无穷维算子]

4. **Bhatia, R.** (1997). *Matrix Analysis*. Springer, GTM 169. [矩阵分析的现代经典，深入讨论特征值扰动与优超理论]

5. **Stewart, G. W. & Sun, J.** (1990). *Matrix Perturbation Theory*. Academic Press. [从数值分析角度系统梳理矩阵扰动理论]

6. **Bhatia, R. & Friedland, S.** (1994). The Hoffman-Wielandt inequality in infinite dimensions. *Proceedings - Mathematical Sciences*, 104(3), 483--494. [Hoffman--Wielandt 不等式的 Hilbert--Schmidt 算子推广]

7. **Tao, T.** (2010). 254A, Notes 3a: Eigenvalues and sums of Hermitian matrices. *Lecture notes, UCLA*. [对 Weyl、Lidskii 和 Hoffman--Wielandt 不等式的现代统一处理]

8. **Anderson, G. W., Guionnet, A. & Zeitouni, O.** (2010). *An Introduction to Random Matrices*. Cambridge University Press. [随机矩阵理论中 Hoffman--Wielandt 定理的应用]

---

## 十四、参考文献

- Hoffman, A. J. & Wielandt, H. W. (1953). The variation of the spectrum of a normal matrix. *Duke Mathematical Journal*, 20(1), 37--39.

- von Neumann, J. (1937). Some matrix-inequalities and metrization of matric-space. *Tomsk University Review*, 1, 286--300.

- Birkhoff, G. (1946). Three observations on linear algebra. *Revista de la Universidad Nacional de Tucuman, Serie A*, 5, 147--151.

- Weyl, H. (1912). Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen. *Mathematische Annalen*, 71(4), 441--479.

- Lidskii, V. B. (1950). The proper values of the sum and product of symmetric matrices. *Doklady Akademii Nauk SSSR*, 75, 769--772.

- Mirsky, L. (1975). A trace inequality of John von Neumann. *Monatshefte fur Mathematik*, 79(4), 303--306.

- Bauer, F. L. & Fike, C. T. (1960). Norms and exclusion theorems. *Numerische Mathematik*, 2(1), 137--141.

- Kato, T. (1966). *Perturbation Theory for Linear Operators*. Springer-Verlag.

- Bhatia, R. (1997). *Matrix Analysis*. Springer, Graduate Texts in Mathematics 169.

- Stewart, G. W. & Sun, J. (1990). *Matrix Perturbation Theory*. Academic Press.

- Horn, R. A. & Johnson, C. R. (2013). *Matrix Analysis* (2nd ed.). Cambridge University Press.

- Wielandt, H. (1996). *Mathematische Werke / Mathematical Works, Vol. 2: Linear Algebra and Analysis*. Walter de Gruyter. (Eds. B. Huppert & H. Schneider)

---

*本文写作参考了上述原始文献及相关学术资源，力求在学术严谨性与可读性之间取得平衡。*
